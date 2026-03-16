import frappe
import re

frappe.init(site="intrepid.localhost")
frappe.connect()

# --- New Item Groups ---
new_groups = [
    ("Beverages",           "Products"),
    ("Paper & Eco Products","Products"),
    ("Food Products",       "Products"),
    ("Bags & Packaging",    "Products"),
]
for group_name, parent in new_groups:
    if not frappe.db.exists("Item Group", group_name):
        ig = frappe.new_doc("Item Group")
        ig.item_group_name = group_name
        ig.parent_item_group = parent
        ig.insert(ignore_permissions=True)
        print(f"Created group: {group_name}")

# Ensure extra UOMs exist
for uom_name in ["BX", "POUCH", "LTR", "KG"]:
    if not frappe.db.exists("UOM", uom_name):
        u = frappe.new_doc("UOM")
        u.uom_name = uom_name
        u.insert(ignore_permissions=True)
        print(f"Created UOM: {uom_name}")

# --- Items ---
# (item_code, item_name, item_group, stock_uom, buy_price,
#  pck_per_ctn, pc_per_pck, short_desc, long_desc)
# pck_per_ctn=None if stock_uom is already PCK/BX/POUCH
items = [
    # ── Paper Cups ──────────────────────────────────────────────────────────
    ("PAPER-CUP-8OZ-BLK",
     "Paper Cups Double 8oz Plain Black/TG/CTN [20PCK X 25PC]",
     "Paper & Eco Products", "CTN", 1775.00, 20, 25,
     "Black double-walled 8oz paper cup. 1 Carton = 20 Packs × 25 Pcs (500 pcs/carton).",
     "<ul><li><strong>1 Carton</strong> = 20 Packs × 25 Pcs = <strong>500 pcs total</strong></li><li><strong>1 Pack</strong> = 25 pcs</li><li>Double-walled insulation for hot beverages</li></ul>"),

    # ── Bagasse ──────────────────────────────────────────────────────────────
    ("BAGASSE-PLATE-9",
     "Bagasse Plate Round 9in Natural/Earthpack/CTN [10PCK X 50PC]",
     "Paper & Eco Products", "CTN", 2250.00, 10, 50,
     "Natural bagasse round plate 9in. 1 Carton = 10 Packs × 50 Pcs (500 pcs/carton).",
     "<ul><li><strong>1 Carton</strong> = 10 Packs × 50 Pcs = <strong>500 pcs total</strong></li><li><strong>1 Pack</strong> = 50 pcs</li><li>100% compostable sugarcane fibre</li></ul>"),

    ("STRAW-BAG-6MM",
     "Bagasse Straw Ind. Wrap 6mm x 8in Flat/Earthpack/PCK [100PC]",
     "Paper & Eco Products", "PCK", 100.00, None, 100,
     "Bagasse flat straw 6mm x 8in, individually wrapped. 1 Pack = 100 pcs.",
     "<ul><li><strong>1 Pack</strong> = 100 pcs</li><li>100% compostable bagasse material</li><li>Individually wrapped for hygiene</li></ul>"),

    # ── Kraft Bowls ──────────────────────────────────────────────────────────
    ("BOWL-KRAFT-500ML",
     "Kraft Salad Bowl 500ML/TG/CTN [12PCK X 50PC]",
     "Paper & Eco Products", "CTN", 2778.00, 12, 50,
     "Kraft salad bowl 500ml. 1 Carton = 12 Packs × 50 Pcs (600 pcs/carton).",
     "<ul><li><strong>1 Carton</strong> = 12 Packs × 50 Pcs = <strong>600 pcs total</strong></li><li><strong>1 Pack</strong> = 50 pcs</li><li>Eco-friendly kraft paper, microwave safe</li></ul>"),

    ("LID-KRAFT-BOWL",
     "Lid for Kraft Bowl 500/750/1000ML/TG/CTN [12PCK X 50PC]",
     "Paper & Eco Products", "CTN", 1890.00, 12, 50,
     "Clear lid for kraft bowls 500/750/1000ml. 1 Carton = 12 Packs × 50 Pcs (600 pcs/carton).",
     "<ul><li><strong>1 Carton</strong> = 12 Packs × 50 Pcs = <strong>600 pcs total</strong></li><li><strong>1 Pack</strong> = 50 pcs</li><li>Fits 500ml, 750ml, and 1000ml kraft bowls</li></ul>"),

    ("BOWL-KRAFT-750ML",
     "Kraft Salad Bowl 750ML/TG/Jay-Z/PCK [50PC]",
     "Paper & Eco Products", "PCK", 254.00, None, 50,
     "Kraft salad bowl 750ml. 1 Pack = 50 pcs.",
     "<ul><li><strong>1 Pack</strong> = 50 pcs</li><li>Eco-friendly kraft paper, microwave safe</li></ul>"),

    # ── Paper Bags & Packaging ───────────────────────────────────────────────
    ("SBAG-TINY-TRANS",
     "Shopping Bag Tiny Transparent/Viking/PCK",
     "Bags & Packaging", "PCK", 26.00, None, None,
     "Tiny transparent shopping bag. Sold per pack.",
     "<ul><li>Sold per pack</li><li>Transparent HDPE material</li></ul>"),

    ("SBAG-MED-TRANS",
     "Shopping Bag Medium Transparent/Viking/PCK",
     "Bags & Packaging", "PCK", 47.00, None, None,
     "Medium transparent shopping bag. Sold per pack.",
     "<ul><li>Sold per pack</li><li>Transparent HDPE material</li></ul>"),

    ("CUP-CARRIER-HD",
     "Plastic HD Single Cup Carrier Plain/PCK [APX.100PC]",
     "Bags & Packaging", "PCK", 41.00, None, 100,
     "Single cup carrier, heavy duty plastic. 1 Pack ≈ 100 pcs.",
     "<ul><li><strong>1 Pack</strong> ≈ 100 pcs</li><li>Heavy duty HDPE, fits most cup sizes</li></ul>"),

    ("BURGER-POUCH-6X6",
     "Paper L-Pouch Burger 6x6in White/3M/PCK [100PC]",
     "Paper & Eco Products", "PCK", 60.00, None, 100,
     "White paper burger pouch 6x6in. 1 Pack = 100 pcs.",
     "<ul><li><strong>1 Pack</strong> = 100 pcs</li><li>Grease-resistant lining</li><li>Suitable for burgers, sandwiches, and snacks</li></ul>"),

    ("FOOD-BOX-750CC",
     "Paper Food Box LB2 750CC Laminated White/Ecoliving/PCK",
     "Paper & Eco Products", "PCK", 88.00, None, None,
     "750cc laminated white paper food box. Sold per pack.",
     "<ul><li>Sold per pack</li><li>Laminated interior — moisture and grease resistant</li><li>Suitable for rice meals, noodles, and takeaway</li></ul>"),

    # ── Straws ───────────────────────────────────────────────────────────────
    ("STRAW-21CM-BLK",
     "Hard Straw 21cm Ind. PP Wrap Pointed Black/IP/PCK [100PC]",
     "Straws", "PCK", 36.00, None, 100,
     "Black pointed hard PP straw 21cm, individually wrapped. 1 Pack = 100 pcs.",
     "<ul><li><strong>1 Pack</strong> = 100 pcs</li><li>Individually wrapped, hard polypropylene</li><li>21cm pointed tip for sealed cups and boba</li></ul>"),

    # ── Utensils ─────────────────────────────────────────────────────────────
    ("SPORK-WHT-VIP",
     "Plastic Spork White/VIP/CTN [100PCK X 25PC]",
     "Cutlery & Utensils", "CTN", 1200.00, 100, 25,
     "White plastic spork. 1 Carton = 100 Packs × 25 Pcs (2,500 pcs/carton).",
     "<ul><li><strong>1 Carton</strong> = 100 Packs × 25 Pcs = <strong>2,500 pcs total</strong></li><li><strong>1 Pack</strong> = 25 pcs</li></ul>"),

    ("CHOPSTICK-BM-PP",
     "Bamboo Chopstick Twin 21cm (in PP Film)/TG/PCK [100PC]",
     "Cutlery & Utensils", "PCK", 91.00, None, 100,
     "Twin bamboo chopsticks 21cm in PP wrap. 1 Pack = 100 pairs.",
     "<ul><li><strong>1 Pack</strong> = 100 pairs</li><li>Individually PP-wrapped for hygiene</li><li>Natural bamboo, disposable</li></ul>"),

    # ── Cups & Containers ────────────────────────────────────────────────────
    ("MW-HINGE-60ML",
     "MW Hinged Cup 60ML (P2)/Lucky Star/PCK [50PC]",
     "Cups & Containers", "PCK", 47.00, None, 50,
     "Microwave-safe hinged cup 60ml. 1 Pack = 50 pcs.",
     "<ul><li><strong>1 Pack</strong> = 50 pcs</li><li>Microwave-safe, hinged lid</li><li>Ideal for sauces, condiments, and small portions</li></ul>"),

    # ── Gloves ───────────────────────────────────────────────────────────────
    ("GLOVES-VNL-BLK",
     "Gloves Vinyl Large Black/Med-Aid/BX [100PC]",
     "Gloves", "BX", 159.00, None, 100,
     "Black vinyl large gloves. 1 Box = 100 pcs.",
     "<ul><li><strong>1 Box</strong> = 100 pcs</li><li>Latex-free vinyl, powder-free</li><li>Large size, food-safe</li></ul>"),

    # ── Beverages ────────────────────────────────────────────────────────────
    ("MILK-UHT-1L-JRS",
     "Milk UHT Full Cream 1L/Jersey/CTN [12PCK]",
     "Beverages", "CTN", 870.00, 12, 1,
     "Jersey full cream UHT milk 1L. 1 Carton = 12 pcs.",
     "<ul><li><strong>1 Carton</strong> = <strong>12 pcs (12 litres)</strong></li><li>Full cream UHT, long shelf life</li><li>Jersey brand</li></ul>"),

    ("MILK-UHT-1L-CON",
     "Milk UHT Full Cream 1L/Conaprole/CTN [12LTR]",
     "Beverages", "CTN", 930.00, 12, 1,
     "Conaprole full cream UHT milk 1L. 1 Carton = 12 pcs.",
     "<ul><li><strong>1 Carton</strong> = <strong>12 pcs (12 litres)</strong></li><li>Full cream UHT, long shelf life</li><li>Conaprole brand (Uruguay)</li></ul>"),

    ("MILK-UHT-35-MV",
     "Milk UHT Full Cream 3.5% 1L/Mlekovita/CTN [12LTR]",
     "Beverages", "CTN", 882.00, 12, 1,
     "Mlekovita full cream 3.5% UHT milk 1L. 1 Carton = 12 pcs.",
     "<ul><li><strong>1 Carton</strong> = <strong>12 pcs (12 litres)</strong></li><li>3.5% fat content, full cream UHT</li><li>Mlekovita brand (Poland)</li></ul>"),

    ("OAT-MILK-1L-OS",
     "Oat Milk Barista Blend 1L/Oatside/CTN [6LTR]",
     "Beverages", "CTN", 715.00, 6, 1,
     "Oatside barista blend oat milk 1L. 1 Carton = 6 pcs.",
     "<ul><li><strong>1 Carton</strong> = <strong>6 pcs (6 litres)</strong></li><li>Barista-grade oat milk, froths well</li><li>Plant-based, dairy-free</li></ul>"),

    ("GATA-400ML",
     "Fresh Gata 400ML/Coco Mama/CTN [24POUCH]",
     "Beverages", "CTN", 1650.00, None, 24,
     "Coco Mama fresh coconut cream 400ml. 1 Carton = 24 pouches.",
     "<ul><li><strong>1 Carton</strong> = <strong>24 pouches</strong></li><li>Fresh coconut cream, no preservatives</li></ul>"),

    ("GATA-200ML",
     "Fresh Gata 200ML/Coco Mama/POUCH",
     "Beverages", "POUCH", 34.50, None, None,
     "Coco Mama fresh coconut cream 200ml pouch. Sold per pouch.",
     "<ul><li>Sold per pouch (200ml)</li><li>Fresh coconut cream, no preservatives</li></ul>"),

    # ── Food Products ────────────────────────────────────────────────────────
    ("CREAM-250ML-JRS",
     "All Purpose Cream 250ML/Jersey/CTN [24PCK]",
     "Food Products", "CTN", 1314.00, 24, 1,
     "Jersey all purpose cream 250ml. 1 Carton = 24 pcs.",
     "<ul><li><strong>1 Carton</strong> = <strong>24 pcs</strong></li><li>All-purpose cooking and whipping cream</li><li>Jersey brand</li></ul>"),

    ("CHEESE-240G-BT",
     "Cheese Sliced 240G (24PC)/Bigtime/PCK",
     "Food Products", "PCK", 67.00, None, 24,
     "Bigtime sliced cheese 240g. 1 Pack = 24 slices.",
     "<ul><li><strong>1 Pack</strong> = 24 slices (240g)</li><li>Ready-to-use sliced cheese</li></ul>"),

    ("CREAMER-FCC40",
     "FCC40 Premium Non Dairy Creamer/PCK [1KG]",
     "Beverages", "PCK", 155.00, None, None,
     "FCC40 non-dairy creamer powder 1kg. Sold per pack.",
     "<ul><li>Sold per pack (1kg)</li><li>Premium non-dairy creamer for coffee and beverages</li></ul>"),
]

CTN_MARKUP  = 1.10
PCK_MARKUP  = 1.15
PC_MARKUP   = 1.30
BX_MARKUP   = 1.15
POUCH_MARKUP = 1.20

def make_route(name):
    slug = name.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")
    return slug

def fmt_money(rate):
    return "₱ {:,.2f}".format(rate)

def upsert_price(item_code, price_list, uom, rate, selling, buying):
    filters = {"item_code": item_code, "price_list": price_list, "uom": uom}
    if selling:
        filters["selling"] = 1
    if buying:
        filters["buying"] = 1
    existing = frappe.db.get_value("Item Price", filters, "name")
    if existing:
        frappe.db.set_value("Item Price", existing, "price_list_rate", rate)
    else:
        ip = frappe.new_doc("Item Price")
        ip.item_code = item_code
        ip.price_list = price_list
        ip.selling = 1 if selling else 0
        ip.buying = 1 if buying else 0
        ip.currency = "PHP"
        ip.uom = uom
        ip.price_list_rate = rate
        ip.insert(ignore_permissions=True)

for (item_code, item_name, item_group, stock_uom,
     buy_price, pck_per_ctn, pc_per_pck,
     short_desc, long_desc) in items:

    # Ensure stock UOM exists
    if not frappe.db.exists("UOM", stock_uom):
        u = frappe.new_doc("UOM")
        u.uom_name = stock_uom
        u.insert(ignore_permissions=True)

    # Create Item
    if not frappe.db.exists("Item", item_code):
        item = frappe.new_doc("Item")
        item.item_code = item_code
        item.item_name = item_name
        item.item_group = item_group
        item.stock_uom = stock_uom
        item.is_stock_item = 1
        item.include_item_in_manufacturing = 0

        # UOM conversions
        if stock_uom == "CTN":
            if pck_per_ctn and pc_per_pck:
                item.append("uoms", {"uom": "PCK", "conversion_factor": round(1 / pck_per_ctn, 8)})
                item.append("uoms", {"uom": "PC",  "conversion_factor": round(1 / (pck_per_ctn * pc_per_pck), 8)})
            elif pc_per_pck:  # no PCK level
                item.append("uoms", {"uom": "PC",  "conversion_factor": round(1 / pc_per_pck, 8)})
        elif stock_uom in ("PCK", "BX") and pc_per_pck:
            item.append("uoms", {"uom": "PC", "conversion_factor": round(1 / pc_per_pck, 8)})

        item.insert(ignore_permissions=True)
        print(f"Created item: {item_code}")
    else:
        print(f"Skipped (exists): {item_code}")

    # Buying price (Henwil Marketing)
    upsert_price(item_code, "Henwil Marketing", stock_uom, buy_price, selling=False, buying=True)

    # Selling prices (Standard Selling)
    if stock_uom == "CTN":
        sell_ctn = round(buy_price * CTN_MARKUP, 2)
        upsert_price(item_code, "Standard Selling", "CTN", sell_ctn, selling=True, buying=False)
        if pck_per_ctn:
            sell_pck = round((buy_price / pck_per_ctn) * PCK_MARKUP, 2)
            upsert_price(item_code, "Standard Selling", "PCK", sell_pck, selling=True, buying=False)
        if pc_per_pck:
            total_pc = (pck_per_ctn * pc_per_pck) if pck_per_ctn else pc_per_pck
            sell_pc = round((buy_price / total_pc) * PC_MARKUP, 2)
            upsert_price(item_code, "Standard Selling", "PC", sell_pc, selling=True, buying=False)
    elif stock_uom in ("PCK", "BX"):
        sell_pck = round(buy_price * PCK_MARKUP, 2)
        upsert_price(item_code, "Standard Selling", stock_uom, sell_pck, selling=True, buying=False)
        if pc_per_pck:
            sell_pc = round((buy_price / pc_per_pck) * PC_MARKUP, 2)
            upsert_price(item_code, "Standard Selling", "PC", sell_pc, selling=True, buying=False)
    elif stock_uom == "POUCH":
        sell_pouch = round(buy_price * POUCH_MARKUP, 2)
        upsert_price(item_code, "Standard Selling", "POUCH", sell_pouch, selling=True, buying=False)

    # Publish to Webshop
    if not frappe.db.exists("Website Item", {"item_code": item_code}):
        wi = frappe.new_doc("Website Item")
        wi.item_code         = item_code
        wi.item_name         = item_name
        wi.web_item_name     = item_name
        wi.item_group        = item_group
        wi.stock_uom         = stock_uom
        wi.published         = 1
        wi.on_backorder      = 1
        wi.website_warehouse = "Stores - KPS"
        wi.route             = make_route(item_name)
        wi.short_description = short_desc
        wi.web_long_description = long_desc
        wi.insert(ignore_permissions=True)
        print(f"  → Published to webshop")

frappe.db.commit()
print("\nBatch 2 import complete.")
