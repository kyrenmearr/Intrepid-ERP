import frappe

frappe.init(site="intrepid.localhost")
frappe.connect()

# Ensure UOMs exist
for uom_name in ["PCK", "PC"]:
    if not frappe.db.exists("UOM", uom_name):
        u = frappe.new_doc("UOM")
        u.uom_name = uom_name
        u.insert(ignore_permissions=True)
        print(f"Created UOM: {uom_name}")

# (item_code, stock_uom, pck_per_ctn, pc_per_pck)
# conversion_factor = 1 / qty_per_ctn  (how many CTN/BDL is 1 PCK or 1 PC)
items_uom = [
    # Cups
    ("PP-UCUP-12OZ",    "CTN",  20,   50),   # 20 PCK x 50 PC = 1000 PC/CTN
    ("PP-UCUP-16OZ",    "CTN",  20,   50),
    # Containers
    ("BENTO-MW-BT1",    "CTN",  12,   50),   # 12 PCK x 50 PC = 600 PC/CTN
    # Cutlery
    ("SPORK-WHT-BNW",   "CTN", 100,   25),   # 100 PCK x 25 PC = 2500 PC/CTN
    ("SPOON-SM-WHT",    "CTN", 100,   25),
    ("FORK-SM-WHT",     "CTN", 100,   25),
    # Straws
    ("STRAW-6MM-KRAFT", "CTN", 100,  100),   # 100 PCK x 100 PC = 10000 PC/CTN
    ("STRAW-12MM-WHT",  "CTN",  24,  100),   # 24 PCK x 100 PC = 2400 PC/CTN
    ("BSTRAW-85-WHT",   "CTN", 100,  100),
    ("BSTRAW-85-IW",    "CTN",  50,  100),   # 50 PCK x 100 PC = 5000 PC/CTN
    # Gloves (BX = box, treated as PCK)
    ("GLOVES-PE-CLR",   "CTN", 100,  100),   # 100 BX x 100 PC = 10000 PC/CTN
    # Alum Trays (no inner pack, sold by PC directly)
    ("ALUM-2220",       "CTN",  None, 200),  # 200 PC/CTN
    ("ALUM-2700",       "CTN",  None, 200),
    ("ALUM-3578",       "CTN",  None, 100),
    ("ALUM-3000",       "CTN",  None, 200),
    # Styro (BDL stock UOM, no inner pack)
    ("STYRO-SB1",       "BDL",  None, 500),  # 500 PC/BDL
]

for item_code, stock_uom, pck_per_ctn, pc_per_pck in items_uom:
    item = frappe.get_doc("Item", item_code)

    # Clear existing UOM conversions (except stock UOM row)
    item.uoms = [row for row in item.uoms if row.uom == stock_uom]

    if pck_per_ctn:
        pc_per_ctn = pck_per_ctn * pc_per_pck
        item.append("uoms", {
            "uom": "PCK",
            "conversion_factor": round(1 / pck_per_ctn, 8)
        })
        item.append("uoms", {
            "uom": "PC",
            "conversion_factor": round(1 / pc_per_ctn, 8)
        })
        print(f"{item_code}: 1 PCK = {round(1/pck_per_ctn,4)} {stock_uom} | 1 PC = {round(1/pc_per_ctn,6)} {stock_uom}")
    else:
        # No PCK level — just PC
        item.append("uoms", {
            "uom": "PC",
            "conversion_factor": round(1 / pc_per_pck, 8)
        })
        print(f"{item_code}: 1 PC = {round(1/pc_per_pck,6)} {stock_uom}")

    item.save(ignore_permissions=True)

frappe.db.commit()
print("\nDone! UOM conversions applied to all items.")
