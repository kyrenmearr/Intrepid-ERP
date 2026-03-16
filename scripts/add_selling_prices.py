import frappe

frappe.init(site="intrepid.localhost")
frappe.connect()

# --- Selling Price List ---
if not frappe.db.exists("Price List", "Standard Selling"):
    pl = frappe.new_doc("Price List")
    pl.price_list_name = "Standard Selling"
    pl.selling = 1
    pl.buying = 0
    pl.currency = "PHP"
    pl.enabled = 1
    pl.insert(ignore_permissions=True)
    print("Created price list: Standard Selling")

# Markup tiers
CTN_MARKUP = 1.10
PCK_MARKUP = 1.15
PC_MARKUP  = 1.30

# (item_code, stock_uom, buy_per_ctn, pck_per_ctn, pc_per_pck)
# pck_per_ctn=None means no PCK level
items = [
    ("PP-UCUP-12OZ",    "CTN",  960.00,  20,  50),
    ("PP-UCUP-16OZ",    "CTN",  1530.00, 20,  50),
    ("BENTO-MW-BT1",    "CTN",  4680.00, 12,  50),
    ("SPORK-WHT-BNW",   "CTN",  1395.00, 100, 25),
    ("SPOON-SM-WHT",    "CTN",  830.00,  100, 25),
    ("FORK-SM-WHT",     "CTN",  830.00,  100, 25),
    ("GLOVES-PE-CLR",   "CTN",  2750.00, 100, 100),
    ("STRAW-6MM-KRAFT", "CTN",  7475.00, 100, 100),
    ("STRAW-12MM-WHT",  "CTN",  4200.00, 24,  100),
    ("BSTRAW-85-WHT",   "CTN",  1350.00, 100, 100),
    ("BSTRAW-85-IW",    "CTN",  1600.00, 50,  100),
    ("STYRO-SB1",       "BDL",  810.00,  None, 500),
    ("ALUM-2220",       "CTN",  3700.00, None, 200),
    ("ALUM-2700",       "CTN",  4100.00, None, 200),
    ("ALUM-3578",       "CTN",  2250.00, None, 100),
    ("ALUM-3000",       "CTN",  4300.00, None, 200),
]

def round2(val):
    return round(val, 2)

def upsert_price(item_code, uom, rate):
    existing = frappe.db.get_value("Item Price", {
        "item_code": item_code,
        "price_list": "Standard Selling",
        "uom": uom,
        "selling": 1
    }, "name")
    if existing:
        frappe.db.set_value("Item Price", existing, "price_list_rate", rate)
        print(f"  Updated {uom}: PHP {rate:,.2f}")
    else:
        ip = frappe.new_doc("Item Price")
        ip.item_code = item_code
        ip.price_list = "Standard Selling"
        ip.selling = 1
        ip.buying = 0
        ip.currency = "PHP"
        ip.uom = uom
        ip.price_list_rate = rate
        ip.insert(ignore_permissions=True)
        print(f"  Added {uom}: PHP {rate:,.2f}")

for item_code, stock_uom, buy_ctn, pck_per_ctn, pc_per_pck in items:
    print(f"\n{item_code}")

    # CTN / BDL price
    ctn_sell = round2(buy_ctn * CTN_MARKUP)
    upsert_price(item_code, stock_uom, ctn_sell)

    if pck_per_ctn:
        cost_pck = buy_ctn / pck_per_ctn
        pck_sell = round2(cost_pck * PCK_MARKUP)
        upsert_price(item_code, "PCK", pck_sell)
        pc_per_ctn = pck_per_ctn * pc_per_pck
    else:
        pc_per_ctn = pc_per_pck

    cost_pc = buy_ctn / pc_per_ctn
    pc_sell = round2(cost_pc * PC_MARKUP)
    upsert_price(item_code, "PC", pc_sell)

frappe.db.commit()
print("\nDone! All selling prices imported.")
