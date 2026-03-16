import frappe
import re

frappe.init(site="intrepid.localhost")
frappe.connect()

# Map item_group to webshop-friendly display names
group_descriptions = {
    "Cups & Containers": "Food-grade cups, lids, and multi-compartment containers for takeaway and food service.",
    "Cutlery & Utensils": "Disposable plastic spoons, forks, and sporks for catering and food service.",
    "Straws":             "Paper and plastic straws — individually wrapped, bulk, and eco-friendly options.",
    "Gloves":             "Disposable plastic gloves for food handling and hygiene.",
    "Trays & Pans":       "Aluminum catering trays and baking pans in a variety of sizes.",
    "Foam Products":      "Styrofoam containers and food packaging for hot and cold items.",
}

items = [
    ("PP-UCUP-12OZ",    "PP U-Cup 12oz (20 Packs × 50 Pcs)"),
    ("PP-UCUP-16OZ",    "PP U-Cup 16oz (20 Packs × 50 Pcs)"),
    ("BENTO-MW-BT1",    "Bento Microwave Box BT-1 3-Compartment (12 Packs × 50 Pcs)"),
    ("SPORK-WHT-BNW",   "Plastic Spork White (100 Packs × 25 Pcs)"),
    ("SPOON-SM-WHT",    "Plastic Spoon Small White (100 Packs × 25 Pcs)"),
    ("FORK-SM-WHT",     "Plastic Fork Small White (100 Packs × 25 Pcs)"),
    ("GLOVES-PE-CLR",   "Disposable PE Plastic Gloves Clear (100 Boxes × 100 Pcs)"),
    ("STRAW-6MM-KRAFT", "Paper Straw 6mm Kraft Individually Wrapped (100 Packs × 100 Pcs)"),
    ("STRAW-12MM-WHT",  "Paper Straw 12mm Pointed White Individually Wrapped (24 Packs × 100 Pcs)"),
    ("BSTRAW-85-WHT",   "Bending Straw 8.5 Inch White (100 Packs × 100 Pcs)"),
    ("BSTRAW-85-IW",    "Bending Straw 8.5 Inch White Individually Wrapped (50 Packs × 100 Pcs)"),
    ("STYRO-SB1",       "Styrofoam Container SB1 Multi (Bundle of 500 Pcs)"),
    ("ALUM-2220",       "Aluminum Catering Tray #2220 (200 Pcs per Carton)"),
    ("ALUM-2700",       "Aluminum Catering Tray #2700 (200 Pcs per Carton)"),
    ("ALUM-3578",       "Aluminum Catering Tray #3578/64 (100 Pcs per Carton)"),
    ("ALUM-3000",       "Aluminum Catering Tray #3000 (200 Pcs per Carton)"),
]

def make_route(web_item_name):
    slug = web_item_name.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug).strip("-")
    return slug

for item_code, web_item_name in items:
    # Skip if already published
    if frappe.db.exists("Website Item", {"item_code": item_code}):
        print(f"Already published: {item_code}")
        continue

    item = frappe.get_doc("Item", item_code)

    wi = frappe.new_doc("Website Item")
    wi.item_code       = item_code
    wi.item_name       = item.item_name
    wi.web_item_name   = web_item_name
    wi.item_group      = item.item_group
    wi.stock_uom       = item.stock_uom
    wi.published       = 1
    wi.route           = make_route(web_item_name)
    wi.short_description = group_descriptions.get(item.item_group, "")

    wi.insert(ignore_permissions=True)
    print(f"Published: {item_code} → /shop/{wi.route}")

frappe.db.commit()
print("\nDone! All items published to webshop.")
