import frappe

frappe.init(site="intrepid.localhost")
frappe.connect()

# (item_code, short_description, web_long_description)
items = [
    (
        "PP-UCUP-12OZ",
        "Clear 12oz plastic U-cup. 1 Carton = 20 Packs × 50 Pcs (1,000 pcs/carton).",
        "<p>Clear polypropylene U-shaped drinking cup, 12oz capacity.</p><ul><li><strong>1 Carton</strong> = 20 Packs × 50 Pcs = <strong>1,000 pcs total</strong></li><li><strong>1 Pack</strong> = 50 pcs</li><li>Suitable for cold beverages, smoothies, and milktea</li><li>Food-grade, BPA-free PP material</li></ul>"
    ),
    (
        "PP-UCUP-16OZ",
        "Clear 16oz plastic U-cup. 1 Carton = 20 Packs × 50 Pcs (1,000 pcs/carton).",
        "<p>Clear polypropylene U-shaped drinking cup, 16oz capacity.</p><ul><li><strong>1 Carton</strong> = 20 Packs × 50 Pcs = <strong>1,000 pcs total</strong></li><li><strong>1 Pack</strong> = 50 pcs</li><li>Ideal for large-format cold drinks, boba, and iced beverages</li><li>Food-grade, BPA-free PP material</li></ul>"
    ),
    (
        "BENTO-MW-BT1",
        "3-compartment microwave-safe bento box with clear lid. 1 Carton = 12 Packs × 50 Pcs (600 pcs/carton).",
        "<p>Microwave-safe bento box with 3 compartments and a secure clear lid.</p><ul><li><strong>1 Carton</strong> = 12 Packs × 50 Pcs = <strong>600 pcs total</strong></li><li><strong>1 Pack</strong> = 50 pcs</li><li>Ideal for meal prep, catering, and food delivery</li><li>Leak-resistant lid, microwave and freezer safe</li></ul>"
    ),
    (
        "SPORK-WHT-BNW",
        "White disposable plastic spork. 1 Carton = 100 Packs × 25 Pcs (2,500 pcs/carton).",
        "<p>Lightweight white plastic spork — spoon and fork combined.</p><ul><li><strong>1 Carton</strong> = 100 Packs × 25 Pcs = <strong>2,500 pcs total</strong></li><li><strong>1 Pack</strong> = 25 pcs</li><li>Ideal for desserts, salads, and takeaway meals</li></ul>"
    ),
    (
        "SPOON-SM-WHT",
        "White disposable plastic spoon (small). 1 Carton = 100 Packs × 25 Pcs (2,500 pcs/carton).",
        "<p>Small white disposable plastic spoon, suitable for soups, desserts, and condiments.</p><ul><li><strong>1 Carton</strong> = 100 Packs × 25 Pcs = <strong>2,500 pcs total</strong></li><li><strong>1 Pack</strong> = 25 pcs</li></ul>"
    ),
    (
        "FORK-SM-WHT",
        "White disposable plastic fork (small). 1 Carton = 100 Packs × 25 Pcs (2,500 pcs/carton).",
        "<p>Small white disposable plastic fork, ideal for catering, food stalls, and takeaway.</p><ul><li><strong>1 Carton</strong> = 100 Packs × 25 Pcs = <strong>2,500 pcs total</strong></li><li><strong>1 Pack</strong> = 25 pcs</li></ul>"
    ),
    (
        "GLOVES-PE-CLR",
        "Clear disposable PE plastic gloves. 1 Carton = 100 Boxes × 100 Pcs (10,000 pcs/carton).",
        "<p>Clear polyethylene disposable gloves for food handling and hygiene use.</p><ul><li><strong>1 Carton</strong> = 100 Boxes × 100 Pcs = <strong>10,000 pcs total</strong></li><li><strong>1 Box</strong> = 100 pcs</li><li>One-size-fits-most, ambidextrous</li><li>Food-safe, latex-free</li></ul>"
    ),
    (
        "STRAW-6MM-KRAFT",
        "6mm kraft paper straw, individually wrapped. 1 Carton = 100 Packs × 100 Pcs (10,000 pcs/carton).",
        "<p>Eco-friendly 6mm kraft paper drinking straw, individually wrapped for hygiene.</p><ul><li><strong>1 Carton</strong> = 100 Packs × 100 Pcs = <strong>10,000 pcs total</strong></li><li><strong>1 Pack</strong> = 100 pcs</li><li>Biodegradable and compostable</li><li>Suitable for cold drinks — holds shape for up to 2 hours</li></ul>"
    ),
    (
        "STRAW-12MM-WHT",
        "12mm pointed white paper straw, individually wrapped. 1 Carton = 24 Packs × 100 Pcs (2,400 pcs/carton).",
        "<p>Wide 12mm pointed white paper straw, individually wrapped. Ideal for bubble tea and thick drinks.</p><ul><li><strong>1 Carton</strong> = 24 Packs × 100 Pcs = <strong>2,400 pcs total</strong></li><li><strong>1 Pack</strong> = 100 pcs</li><li>Biodegradable and compostable</li><li>Pointed tip for sealed cups</li></ul>"
    ),
    (
        "BSTRAW-85-WHT",
        "8.5 inch white flexible bending straw. 1 Carton = 100 Packs × 100 Pcs (10,000 pcs/carton).",
        "<p>Standard 8.5 inch white plastic bending straw with flexible neck.</p><ul><li><strong>1 Carton</strong> = 100 Packs × 100 Pcs = <strong>10,000 pcs total</strong></li><li><strong>1 Pack</strong> = 100 pcs</li><li>Suitable for juices, soft drinks, and hospital use</li></ul>"
    ),
    (
        "BSTRAW-85-IW",
        "8.5 inch white bending straw, individually wrapped. 1 Carton = 50 Packs × 100 Pcs (5,000 pcs/carton).",
        "<p>8.5 inch white plastic bending straw, individually wrapped for hygiene.</p><ul><li><strong>1 Carton</strong> = 50 Packs × 100 Pcs = <strong>5,000 pcs total</strong></li><li><strong>1 Pack</strong> = 100 pcs</li><li>Ideal for restaurants, hotels, and catering where hygiene is a priority</li></ul>"
    ),
    (
        "STYRO-SB1",
        "Styrofoam food container SB1 multi-use. 1 Bundle = 500 pcs.",
        "<p>Styrofoam SB1 food container for hot and cold food packaging.</p><ul><li><strong>1 Bundle</strong> = <strong>500 pcs</strong></li><li>Excellent heat and cold retention</li><li>Lightweight and stackable</li><li>Suitable for rice meals, soups, and takeaway food</li></ul>"
    ),
    (
        "ALUM-2220",
        "Aluminum catering tray #2220. 1 Carton = 200 pcs.",
        "<p>Heavy-duty aluminum foil catering tray #2220, ideal for baking, roasting, and food service.</p><ul><li><strong>1 Carton</strong> = <strong>200 pcs</strong></li><li>Oven, grill, and freezer safe</li><li>Disposable — no washing required</li><li>Perfect for catering events and food delivery</li></ul>"
    ),
    (
        "ALUM-2700",
        "Aluminum catering tray #2700. 1 Carton = 200 pcs.",
        "<p>Heavy-duty aluminum foil catering tray #2700, larger size for big batch cooking and catering.</p><ul><li><strong>1 Carton</strong> = <strong>200 pcs</strong></li><li>Oven, grill, and freezer safe</li><li>Disposable — no washing required</li></ul>"
    ),
    (
        "ALUM-3578",
        "Aluminum catering tray #3578/64. 1 Carton = 100 pcs.",
        "<p>Aluminum foil catering tray #3578/64, suitable for medium-sized portions and baked goods.</p><ul><li><strong>1 Carton</strong> = <strong>100 pcs</strong></li><li>Oven, grill, and freezer safe</li><li>Disposable — no washing required</li></ul>"
    ),
    (
        "ALUM-3000",
        "Aluminum catering tray #3000. 1 Carton = 200 pcs.",
        "<p>Heavy-duty aluminum foil catering tray #3000, ideal for roasting, baking, and large catering orders.</p><ul><li><strong>1 Carton</strong> = <strong>200 pcs</strong></li><li>Oven, grill, and freezer safe</li><li>Disposable — no washing required</li></ul>"
    ),
]

for item_code, short_desc, long_desc in items:
    wi_name = frappe.db.get_value("Website Item", {"item_code": item_code}, "name")
    if wi_name:
        frappe.db.set_value("Website Item", wi_name, {
            "short_description": short_desc,
            "web_long_description": long_desc,
        })
        print(f"✓ {item_code}")

frappe.db.commit()
print("\nDone! All descriptions updated.")
