import frappe, re

frappe.init(site="intrepid.localhost")
frappe.connect()

CTN_MARKUP   = 1.10
PCK_MARKUP   = 1.15
PC_MARKUP    = 1.30
BX_MARKUP    = 1.15
POUCH_MARKUP = 1.20
OTHER_MARKUP = 1.15

# Ensure UOMs
for u in ["BAG","CAN","TUB","RM","GAL","KG"]:
    if not frappe.db.exists("UOM", u):
        frappe.new_doc("UOM").update({"uom_name": u}).insert(ignore_permissions=True)
        print(f"Created UOM: {u}")

def make_route(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")

def upsert_price(item_code, price_list, uom, rate, selling, buying):
    f = {"item_code": item_code, "price_list": price_list, "uom": uom}
    if selling: f["selling"] = 1
    if buying:  f["buying"]  = 1
    existing = frappe.db.get_value("Item Price", f, "name")
    if existing:
        frappe.db.set_value("Item Price", existing, "price_list_rate", rate)
    else:
        ip = frappe.new_doc("Item Price")
        ip.update({"item_code": item_code, "price_list": price_list,
                   "selling": 1 if selling else 0, "buying": 1 if buying else 0,
                   "currency": "PHP", "uom": uom, "price_list_rate": rate})
        ip.insert(ignore_permissions=True)

def create_item(item_code, item_name, item_group, stock_uom, buy_price,
                pck_per_ctn=None, pc_per_pck=None, short_desc="", long_desc="",
                markup_override=None):
    if frappe.db.exists("Item", item_code):
        print(f"Skip (exists): {item_code}")
    else:
        if not frappe.db.exists("UOM", stock_uom):
            frappe.new_doc("UOM").update({"uom_name": stock_uom}).insert(ignore_permissions=True)
        item = frappe.new_doc("Item")
        item.update({"item_code": item_code, "item_name": item_name,
                     "item_group": item_group, "stock_uom": stock_uom,
                     "is_stock_item": 1, "include_item_in_manufacturing": 0})
        if stock_uom == "CTN":
            if pck_per_ctn and pc_per_pck:
                item.append("uoms", {"uom": "PCK", "conversion_factor": round(1/pck_per_ctn, 8)})
                item.append("uoms", {"uom": "PC",  "conversion_factor": round(1/(pck_per_ctn*pc_per_pck), 8)})
            elif pc_per_pck:
                item.append("uoms", {"uom": "PC",  "conversion_factor": round(1/pc_per_pck, 8)})
        elif stock_uom in ("PCK","BX","BAG","RM") and pc_per_pck:
            item.append("uoms", {"uom": "PC", "conversion_factor": round(1/pc_per_pck, 8)})
        item.insert(ignore_permissions=True)
        print(f"Created: {item_code}")

    # Buying price
    upsert_price(item_code, "Henwil Marketing", stock_uom, buy_price, selling=False, buying=True)

    # Selling prices
    m = markup_override or {}
    if stock_uom == "CTN":
        upsert_price(item_code, "Standard Selling", "CTN",
                     round(buy_price * m.get("CTN", CTN_MARKUP), 2), True, False)
        if pck_per_ctn:
            upsert_price(item_code, "Standard Selling", "PCK",
                         round((buy_price/pck_per_ctn) * m.get("PCK", PCK_MARKUP), 2), True, False)
        if pc_per_pck:
            total_pc = (pck_per_ctn * pc_per_pck) if pck_per_ctn else pc_per_pck
            upsert_price(item_code, "Standard Selling", "PC",
                         round((buy_price/total_pc) * m.get("PC", PC_MARKUP), 2), True, False)
    elif stock_uom in ("PCK","BX","BAG","RM"):
        upsert_price(item_code, "Standard Selling", stock_uom,
                     round(buy_price * m.get(stock_uom, PCK_MARKUP), 2), True, False)
        if pc_per_pck:
            upsert_price(item_code, "Standard Selling", "PC",
                         round((buy_price/pc_per_pck) * m.get("PC", PC_MARKUP), 2), True, False)
    else:
        upsert_price(item_code, "Standard Selling", stock_uom,
                     round(buy_price * m.get(stock_uom, OTHER_MARKUP), 2), True, False)

    # Webshop
    if not frappe.db.exists("Website Item", {"item_code": item_code}):
        wi = frappe.new_doc("Website Item")
        wi.update({"item_code": item_code, "item_name": item_name, "web_item_name": item_name,
                   "item_group": item_group, "stock_uom": stock_uom, "published": 1,
                   "on_backorder": 1, "website_warehouse": "Stores - KPS",
                   "route": make_route(item_name),
                   "short_description": short_desc, "web_long_description": long_desc})
        wi.insert(ignore_permissions=True)
        print(f"  → Webshop")

# ── NEW ITEMS ────────────────────────────────────────────────────────────────

# Paper Cups & Lids
create_item("PAPER-CUP-8OZ-KRF",
    "Paper Cups Double 8oz Plain Kraft White/TG/CTN [20PCK X 25PC]",
    "Paper & Eco Products", "CTN", 1775.00, 20, 25,
    "White kraft double-walled 8oz paper cup. 1 Carton = 20 Packs × 25 Pcs (500 pcs/carton).",
    "<ul><li><strong>1 Carton</strong> = 20 Packs × 25 Pcs = <strong>500 pcs total</strong></li><li><strong>1 Pack</strong> = 25 pcs</li><li>Double-walled, kraft exterior, suitable for hot beverages</li></ul>")

create_item("LID-8OZ-RIPPLE",
    "Lids Ripple Double 8oz Black/TG/CTN [20PCK X 25PC]",
    "Paper & Eco Products", "CTN", 690.00, 20, 25,
    "Black ripple lid for double 8oz cups. 1 Carton = 20 Packs × 25 Pcs (500 pcs/carton).",
    "<ul><li><strong>1 Carton</strong> = 20 Packs × 25 Pcs = <strong>500 pcs total</strong></li><li><strong>1 Pack</strong> = 25 pcs</li><li>Fits double-wall 8oz paper cups</li></ul>")

# Kraft & Paper Packaging
create_item("BOAT-TRAY-K3",
    "Kraft Boat Tray #3/PLB/PCK [250PC]",
    "Paper & Eco Products", "PCK", 600.00, None, 250,
    "Kraft boat tray #3. 1 Pack = 250 pcs.",
    "<ul><li><strong>1 Pack</strong> = 250 pcs</li><li>Kraft paper, grease-resistant</li><li>Ideal for fries, snacks, and street food</li></ul>")

create_item("FOOD-BOX-700CC",
    "Paper Food Box LB2 700CC B/S White/TG/PCK [25PC]",
    "Paper & Eco Products", "PCK", 130.00, None, 25,
    "700cc laminated white paper food box B/S. 1 Pack = 25 pcs.",
    "<ul><li><strong>1 Pack</strong> = 25 pcs</li><li>Laminated interior — moisture and grease resistant</li></ul>")

create_item("TISSUE-PRECUT-2K",
    "Tissue Pre-Cut Folded 2000 Sheets Mixed White/Insti/PCK",
    "Paper & Eco Products", "PCK", 97.00, None, 2000,
    "Pre-cut folded tissue 2000 sheets. 1 Pack = 2,000 sheets.",
    "<ul><li><strong>1 Pack</strong> = 2,000 sheets</li><li>Mixed white, pre-cut and folded</li><li>Suitable for restaurants and food service</li></ul>")

# Bottles & Containers
create_item("PET-BOTTLE-500ML",
    "PET Cylindrical Bottle 500ML with Black Cap/DW/BAG [100PC]",
    "Cups & Containers", "BAG", 1080.00, None, 100,
    "Clear PET cylindrical bottle 500ml with black cap. 1 Bag = 100 pcs.",
    "<ul><li><strong>1 Bag</strong> = 100 pcs</li><li>Clear PET, food-safe</li><li>Suitable for juices, sauces, and beverages</li></ul>")

create_item("MW-HINGE-60ML-DW",
    "MW Hinged Cup 60ML/DW/PCK [50PC]",
    "Cups & Containers", "PCK", 69.00, None, 50,
    "Microwave-safe hinged cup 60ml (DW). 1 Pack = 50 pcs.",
    "<ul><li><strong>1 Pack</strong> = 50 pcs</li><li>Microwave-safe, hinged lid</li><li>Ideal for sauces, condiments, and small portions</li></ul>")

# Bags
create_item("SBAG-LGE-TRANS",
    "Shopping Bag Large Transparent/Viking/PCK",
    "Bags & Packaging", "PCK", 78.00, None, None,
    "Large transparent shopping bag. Sold per pack.",
    "<ul><li>Sold per pack</li><li>Transparent HDPE material, large size</li></ul>")

create_item("GBAG-PE-XL",
    "GBAG PE Roll 30x37 (XL) Black/5E/RM [100PC]",
    "Bags & Packaging", "RM", 345.00, None, 100,
    "XL black PE garbage bag roll 30x37in. 1 Roll = 100 pcs.",
    "<ul><li><strong>1 Roll</strong> = 100 pcs</li><li>Heavy-duty polyethylene, XL size 30x37in</li></ul>")

# Food Products
create_item("PEPPER-CORN-100G",
    "Black Pepper Corn 100G/Golden Spices/PCK",
    "Food Products", "PCK", 124.75, None, None,
    "Whole black peppercorns 100g. Sold per pack.",
    "<ul><li>100g per pack</li><li>Golden Spices brand</li></ul>")

create_item("MARGARINE-1KG",
    "Margarine/Sunrise/PCK [1KG]",
    "Food Products", "PCK", 93.00, None, None,
    "Sunrise margarine 1kg. Sold per pack.",
    "<ul><li>1kg per pack</li><li>Sunrise brand, all-purpose margarine</li></ul>")

create_item("TRU-MAYO-35L",
    "Tru Mayo 3.5L/Rogers/TUB",
    "Food Products", "TUB", 353.00, None, None,
    "Rogers Tru Mayo 3.5L tub. Sold per tub.",
    "<ul><li>3.5 litres per tub</li><li>Rogers brand, all-purpose mayonnaise</li></ul>")

create_item("HOT-SAUCE-1GAL",
    "Hot Sauce 1GAL/Golden/CTN [4GAL]",
    "Food Products", "CTN", 713.00, None, 4,
    "Golden hot sauce 1 gallon. 1 Carton = 4 gallons.",
    "<ul><li><strong>1 Carton</strong> = 4 gallons</li><li>Golden brand hot sauce</li></ul>")

create_item("BANANA-KETCHUP-1G",
    "Banana Ketchup 1GAL/Cooks/GAL",
    "Food Products", "GAL", 90.00, None, None,
    "Cooks banana ketchup 1 gallon. Sold per gallon.",
    "<ul><li>1 gallon per unit</li><li>Cooks brand banana ketchup</li></ul>")

create_item("MUSH-400G-CAN",
    "Mushrooms Whole 400G/Da Ling/CAN",
    "Food Products", "CAN", 42.25, None, None,
    "Da Ling whole mushrooms 400g. Sold per can.",
    "<ul><li>400g per can</li><li>Da Ling brand, whole mushrooms in brine</li></ul>")

create_item("BEEF-CUBE-120G",
    "BLN Savers Beef Cubes 120G/Knorr/BX",
    "Food Products", "BX", 71.50, None, None,
    "Knorr BLN Savers beef cubes 120g. Sold per box.",
    "<ul><li>120g per box</li><li>Knorr brand beef bouillon cubes</li></ul>")

create_item("CHICKEN-CUBE-600G",
    "BLN Chicken Cubes 600G/Knorr/PCK",
    "Food Products", "PCK", 332.00, None, None,
    "Knorr BLN chicken cubes 600g. Sold per pack.",
    "<ul><li>600g per pack</li><li>Knorr brand chicken bouillon cubes</li></ul>")

# Beverages
create_item("MATCHA-1KG",
    "Artisanal Japanese Matcha Powder 1KG/PCK",
    "Beverages", "PCK", 365.00, None, None,
    "Artisanal Japanese matcha powder 1kg. Sold per pack.",
    "<ul><li>1kg per pack</li><li>Artisanal grade, suitable for lattes and baking</li></ul>")

create_item("TEA-ASSAM-600G",
    "Assam Black Tea Bag 10x60G/Casa/PCK",
    "Beverages", "PCK", 232.00, None, None,
    "Casa Assam black tea bags 10x60g. Sold per pack.",
    "<ul><li>10 × 60g tea bags per pack (600g total)</li><li>Casa brand Assam black tea</li></ul>")

# Gloves (Safehand brand)
create_item("GLOVES-VNL-SH",
    "Gloves Vinyl Large Black/Safehand/BX [100PC]",
    "Gloves", "BX", 159.00, None, 100,
    "Safehand black vinyl large gloves. 1 Box = 100 pcs.",
    "<ul><li><strong>1 Box</strong> = 100 pcs</li><li>Latex-free vinyl, powder-free, food-safe</li><li>Safehand brand</li></ul>")

# ── EXISTING ITEMS — update buying PCK prices ────────────────────────────────
print("\nUpdating buying PCK prices on existing items...")

# SPORK-WHT-BNW: PCK buying = 15.00
upsert_price("SPORK-WHT-BNW", "Henwil Marketing", "PCK", 15.00, selling=False, buying=True)
print("✓ SPORK-WHT-BNW PCK buying price → 15.00")

# LID-KRAFT-BOWL: PCK buying = 163.00
upsert_price("LID-KRAFT-BOWL", "Henwil Marketing", "PCK", 163.00, selling=False, buying=True)
print("✓ LID-KRAFT-BOWL PCK buying price → 163.00")

# GATA-400ML: POUCH buying = 65.75
upsert_price("GATA-400ML", "Henwil Marketing", "POUCH", 65.75, selling=False, buying=True)
upsert_price("GATA-400ML", "Standard Selling", "POUCH", round(65.75 * POUCH_MARKUP, 2), selling=True, buying=False)
print("✓ GATA-400ML POUCH buying price → 65.75")

frappe.db.commit()
print("\nBatch 3 import complete.")
