# Fix: export kiểm kê 500 - HTML không escape (DOMDocument fail)

## Bug
admin/warehouse/self_inventories/{id}/export lỗi 500: 'Failed to load ... as a DOM Document'. Ca: 777, product 16211 tên 'xe tải & Bus'.

## Root cause
SelfInventory::getProductTableAttribute() nối giá trị data vào HTML KHÔNG escape → ký tự & (và <,>) làm HTML malformed → PhpSpreadsheet DOMDocument::loadHTMLFile trả false (libxml prod nghiêm hơn) → 500. Reproduce prod: libxml báo 'htmlParseEntityRef: no name' (dấu &).

## Fix (phương án a)
Escape toàn bộ trường text trong getProductTableAttribute bằng e(): product_name, code, unit_name, position->code, company->code, lot->lot_number, unit->name, note. KHÔNG escape formatCurrency/qty (số).

## Tasks
- [ ] Escape tất cả trường text trong getProductTableAttribute + php -l
- [ ] User test export 777

## Branch: master
