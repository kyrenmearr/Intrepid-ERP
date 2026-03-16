# Intrepid Solutions ERP

ERPNext v15 setup for Intrepid Solutions — packaging and food service supplies distributor.

## Stack
- ERPNext v15 (Frappe Framework v15)
- Frappe Webshop
- MariaDB 12.2.2
- Redis 8.6.1
- Python 3.11 / Node 23

## Local Setup

### Prerequisites
```bash
brew install mariadb redis
pip install frappe-bench
bench init ~/Desktop/frappe-bench --frappe-branch version-15
```

### Start bench
```bash
cd ~/Desktop/frappe-bench
PATH="$HOME/.local/bin:$HOME/Desktop/frappe-bench/env/bin:$PATH" ~/.local/bin/bench start
```

### Access
- Admin: http://localhost:8000 — `Administrator` / `admin`
- Shop: http://localhost:8000/shop

---

## Repository Structure

```
scripts/                        # Data import scripts (run once on fresh setup)
  import_henwil.py              # Batch 1 — Henwil Marketing items (packaging)
  import_henwil_batch2.py       # Batch 2 — extended product range
  import_henwil_batch3.py       # Batch 3 — additional items
  add_uom_conversions.py        # UOM conversions (CTN → PCK → PC)
  add_selling_prices.py         # Selling prices (10/15/30% markup tiers)
  publish_to_webshop.py         # Publish items to public webshop
  update_descriptions.py        # Product descriptions with pack/carton info

customizations/webshop/         # Modified Frappe Webshop files
  templates/generators/item/
    item_add_to_cart.html       # UOM selector (CTN/PCK/PC) on product page
  public/js/
    shopping_cart.js            # Passes selected UOM to quotation
  shopping_cart/
    cart.py                     # update_cart accepts uom param, matches by item+uom
  doctype/website_item/
    website_item.py             # Listing shows PCK price by default
```

## Webshop Customizations

### UOM selector on PDP
- Defaults to PCK on product detail pages
- Dynamically fetches price per UOM on click
- Each UOM creates a separate line in the quotation
- CTA resets correctly when switching UOMs

### Pricing
- Supplier: Henwil Marketing (buying price list)
- Selling: Standard Selling (CTN 10% / PCK 15% / PC 30% markup)
- Currency: PHP

## Running Import Scripts

```bash
cd ~/Desktop/frappe-bench
./env/bin/python -c "
import os, sys
os.chdir('/Users/eclairifyy/Desktop/frappe-bench')
sys.path.insert(0, 'apps/frappe')
sys.path.insert(0, 'apps/erpnext')
sys.path.insert(0, 'apps/webshop')
import frappe
frappe.init(site='intrepid.localhost', sites_path='sites')
frappe.connect()
exec(open('scripts/SCRIPT_NAME.py').read())
"
```
