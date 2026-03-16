import frappe

frappe.init(site="intrepid.localhost")
frappe.connect()

# --- Item Groups ---
groups = [
    ("Cups & Containers", "Products"),
    ("Cutlery & Utensils", "Products"),
    ("Straws", "Products"),
    ("Gloves", "Products"),
    ("Trays & Pans", "Products"),
    ("Foam Products", "Products"),
]
for group_name, parent in groups:
    if not frappe.db.exists("Item Group", group_name):
        ig = frappe.new_doc("Item Group")
        ig.item_group_name = group_name
        ig.parent_item_group = parent
        ig.insert(ignore_permissions=True)
        print(f"Created item group: {group_name}")

# --- Supplier ---
if not frappe.db.exists("Supplier", "Henwil Marketing"):
    sup = frappe.new_doc("Supplier")
    sup.supplier_name = "Henwil Marketing"
    sup.supplier_group = "All Supplier Groups"
    sup.supplier_type = "Company"
    sup.insert(ignore_permissions=True)
    print("Created supplier: Henwil Marketing")

# --- Price List ---
if not frappe.db.exists("Price List", "Henwil Marketing"):
    pl = frappe.new_doc("Price List")
    pl.price_list_name = "Henwil Marketing"
    pl.buying = 1
    pl.selling = 0
    pl.currency = "PHP"
    pl.enabled = 1
    pl.insert(ignore_permissions=True)
    print("Created price list: Henwil Marketing")

# --- Items ---
# (item_code, item_name, item_group, uom, buying_price)
items = [
    ("PP-UCUP-12OZ",   "PP U-CUP 12OZ (95-360U) CLR/IP/CTN [20PCK X 50PC]",               "Cups & Containers",   "CTN",  960.00),
    ("PP-UCUP-16OZ",   "PP U-CUP 16 OZ CLR/FH/CTN [20PCK X 50PC]",                         "Cups & Containers",   "CTN",  1530.00),
    ("GLOVES-PE-CLR",  "GLOVES PLASTIC BY BOX PE CLR/SAFEHAND/CTN [100BX X 100PC]",         "Gloves",              "CTN",  2750.00),
    ("BENTO-MW-BT1",   "BENTO MW BT-1 (3-COMP) B/R W/CLR LID/BXN/CTN [12PCK X 50PC]",     "Cups & Containers",   "CTN",  4680.00),
    ("SPORK-WHT-BNW",  "PLASTIC SPORK WHT/BNW/CTN [100PCK X 25PC]",                        "Cutlery & Utensils",  "CTN",  1395.00),
    ("SPOON-SM-WHT",   "PLASTIC SPOON SMALL WHT/MEGATOP/CTN [100PCK X 25PC]",               "Cutlery & Utensils",  "CTN",  830.00),
    ("FORK-SM-WHT",    "PLASTIC FORK SMALL WHT/MEGATOP/CTN [100PCK X 25PC]",                "Cutlery & Utensils",  "CTN",  830.00),
    ("STYRO-SB1",      "STYRO SB1 (S1) MULTI./BDL [500PC/1]",                              "Foam Products",       "BDL",  810.00),
    ("STRAW-6MM-KRAFT","PAPER STRAW IND. WRAP 6MM KRAFT/EARTHPACK/CTN [100PCK X 100PC]",   "Straws",              "CTN",  7475.00),
    ("STRAW-12MM-WHT", "PAPER STRAW IND. WRAP 12MM POINTED WHT/EARTHPACK/CTN [24PCK X 100PC]", "Straws",          "CTN",  4200.00),
    ("BSTRAW-85-WHT",  "BENDING STRAW 8.5 INCH WHT/FH/CTN [100PCK X 100PC]",              "Straws",              "CTN",  1350.00),
    ("BSTRAW-85-IW",   "BENDING STRAW IND. WRAP 8.5 INCH WHT/DW/CTN [50PCK X 100PC]",    "Straws",              "CTN",  1600.00),
    ("ALUM-2220",      "ALUM CATER TRAY #2220/MARC/CTN [200PC]",                            "Trays & Pans",        "CTN",  3700.00),
    ("ALUM-2700",      "ALUM CATER TRAY #2700/MARC/CTN [200PC]",                            "Trays & Pans",        "CTN",  4100.00),
    ("ALUM-3578",      "ALUM CATER TRAY #3578/64/TG/CTN [100PC]",                           "Trays & Pans",        "CTN",  2250.00),
    ("ALUM-3000",      "ALUM CATER TRAY #3000/MARC/CTN [200PC]",                            "Trays & Pans",        "CTN",  4300.00),
]

for item_code, item_name, item_group, uom, price in items:
    # Create UOM if missing
    if not frappe.db.exists("UOM", uom):
        u = frappe.new_doc("UOM")
        u.uom_name = uom
        u.insert(ignore_permissions=True)

    # Create Item
    if not frappe.db.exists("Item", item_code):
        item = frappe.new_doc("Item")
        item.item_code = item_code
        item.item_name = item_name
        item.item_group = item_group
        item.stock_uom = uom
        item.is_stock_item = 1
        item.include_item_in_manufacturing = 0
        item.insert(ignore_permissions=True)
        print(f"Created item: {item_code}")
    else:
        print(f"Skipped (exists): {item_code}")

    # Create Supplier Item Price
    existing_price = frappe.db.exists("Item Price", {
        "item_code": item_code,
        "price_list": "Henwil Marketing",
        "buying": 1
    })
    if not existing_price:
        ip = frappe.new_doc("Item Price")
        ip.item_code = item_code
        ip.price_list = "Henwil Marketing"
        ip.buying = 1
        ip.selling = 0
        ip.currency = "PHP"
        ip.price_list_rate = price
        ip.insert(ignore_permissions=True)
        print(f"  → Price set: PHP {price:,.2f}")

frappe.db.commit()
print("\nDone! All items and Henwil Marketing prices imported.")
