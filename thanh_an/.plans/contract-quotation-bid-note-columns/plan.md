# Plan — Thêm cột "Ghi chú báo giá" + "Ghi chú thầu" + đổi tên "Ghi chú hợp đồng" (màn hợp đồng)

Phụ trách: @khoipv
Màn: `contract/contract/add` (dùng chung `GeneralComponent` → edit `_id`/detail/approve cùng component)
Tham chiếu pattern: `.plans/bid-package-quotation-note-column/plan.md` (làm y hệt bên gói thầu)

## Bối cảnh / Quyết định (chốt với user)
- Hiện tại màn HĐ có 1 cột `note` (label "Ghi chú"), textarea **sửa được** = ghi chú hợp đồng.
- Yêu cầu tách thành 3 cột:
  1. **Ghi chú báo giá** (`note_quotation`) — cột mới, **read-only**, lấy từ `note` bên báo giá. **Lưu DB**.
  2. **Ghi chú thầu** (`note_bid_package`) — cột mới, **read-only**, lấy từ `bid_package_products.note`. **Lưu DB**.
  3. **Ghi chú hợp đồng** (`note`) — cột note hiện tại, **đổi label** thành "Ghi chú hợp đồng", vẫn sửa được.
- Quyết định phụ (theo precedent gói thầu, cần flag cho user): khi tạo HĐ từ báo giá/thầu → **note (ghi chú HĐ) để trống**, không seed từ nguồn nữa (nguồn đã nằm ở 2 cột read-only). Tránh trùng lặp.

## BE
- [x] Migration `2026_07_03_000002_add_note_columns_to_contract_products_table` — `text('note_quotation')->nullable()->after('note')` + `text('note_bid_package')->nullable()->after('note_quotation')` (chỉ cột, không FK) — ĐÃ CHẠY
- [x] `ContractProduct::$fillable` thêm `note_quotation`, `note_bid_package` (bắt buộc: `fill()` bị chặn bởi fillable dù `$guarded=[]`)
- [x] Chạy migrate OK (verify SHOW COLUMNS: cả 2 cột text/nullable)
- Save: `ContractService::syncGroups` dùng `$itemProduct->fill($product)->save()` → tự lưu 2 cột sau khi thêm fillable
- Resource: `ContractDetailResource` trả `products` là model thô → edit/detail/approve tự có 2 cột

## FE — `contract/contract/components/ProductComponent.vue`
- [x] `columns`: thêm 2 field `note_quotation` (label "Ghi chú báo giá") + `note_bid_package` (label "Ghi chú thầu") **trước** field `note`; đổi label `note` → "Ghi chú hợp đồng" (đều isVisible)
- [x] Template body: thêm 2 nhánh read-only (`<span style="white-space: pre-line">`) cho `note_quotation` + `note_bid_package` trước nhánh `note`
- [x] Width class: thêm `note_quotation`, `note_bid_package` = `td-width-200`
- [x] Export Excel (`exportCurrentGroupsToExcel`): header thay "Ghi chú" bằng 3 header ("Ghi chú báo giá","Ghi chú thầu","Ghi chú hợp đồng"); row thay `product.note` bằng `note_quotation`,`note_bid_package`,`note`
- [x] Import (`handleImportSuccess`): map preserve `note_quotation`/`note_bid_package` ở cả 2 nhánh (nhóm cũ/nhóm mới)
- Merge cột (getFields) dùng `this.columns` → user đã lưu cấu hình cũ vẫn tự có cột mới đúng vị trí

## FE — `contract/contract/components/GeneralComponent.vue`
- [x] `addNegotiation` (map products theo nguồn): set theo `data.type`
  - type 1 (từ gói thầu): `note_bid_package = pro.note || ''`; `note_quotation = pro.note_quotation || ''`; `note = ''`
  - type 2 (từ báo giá): `note_quotation = pro.note || ''`; `note_bid_package = ''`; `note = ''`
  - type 3/4/5 (từ dự án) / khác: `note_quotation = ''`; `note_bid_package = ''`; giữ `note`

## Verify (user test trình duyệt)
- [ ] Tạo HĐ từ báo giá → "Ghi chú báo giá" đúng (read-only), "Ghi chú thầu" trống, "Ghi chú hợp đồng" trống & sửa được
- [ ] Tạo HĐ từ gói thầu → "Ghi chú thầu" đúng, "Ghi chú báo giá" đúng (nếu gói thầu đã có note_quotation), "Ghi chú hợp đồng" trống
- [ ] Lưu → mở lại (edit/detail) → cả 3 cột đúng
- [ ] Xuất Excel → 3 cột ghi chú đúng thứ tự/nội dung

## Import Excel (bổ sung theo yêu cầu user)
- Bối cảnh: file mẫu `static/hanghoa_hopdong.xlsx` (43 cột, cũ) **khác hẳn** file XUẤT Excel (48 cột) → parser `ProductContractImport` đọc lệch cột (giá đọc nhầm cột "Đơn giá báo giá", note đọc nhầm cột NCC).
- [x] Rebuild `static/hanghoa_hopdong.xlsx` khớp CHÍNH XÁC layout export (48 cột, header + width + dòng nhóm mẫu + dòng hàng mẫu). Backup file cũ ở scratchpad.
- [x] Parser `Modules/Payroll/ExcelImports/ProductContractImport.php` chỉnh index đọc theo export: price=`row[16]` (Đơn giá bán Gồm VAT), owner=`row[21]`, producer=`row[22]`, tech=`row[24]`, note=`row[45]` (Ghi chú hợp đồng). **KHÔNG đọc** `row[43]` (ghi chú báo giá) + `row[44]` (ghi chú thầu).
- [x] FE `handleImportSuccess`: giữ `note_quotation`/`note_bid_package` theo product_id qua map (từ groups hiện tại) + kho bền `noteQuotationStore`/`noteBidPackageStore` (watcher tích lũy) → import không xóa 2 cột dù reset groups.
- [x] Verify end-to-end (tinker + file test sản phẩm thật VT-XN-001): price=100000 (đúng cột Q/E16), qty=5, unit=Túi, note="Ghi chu HD dung" (E45, BỎ QUA giá trị điền ở AR/AS), parser không trả note_quotation → FE dùng store. PASS.
- ⚠️ Lưu ý behavior change: parser trước đọc giá ở cột "Đơn giá báo giá", giờ đọc "Đơn giá bán (Gồm VAT)" cho khớp export. Cần user xác nhận đúng ý.

## Bugfix import — mất cột giá vốn / đơn giá báo giá / đơn giá chào thầu (2026-07-03)
- Triệu chứng (user): chọn gói thầu 352 → export → điền đơn giá bán → import → mất giá vốn, đơn giá báo giá, đơn giá chào thầu.
- Root cause: `ProductContractImport` hardcode `price_min/max/cost/pre_contract = 0` và KHÔNG set `price_quotation`/`price_bid_package` (chỉ đọc `price`=E16). Export ghi giá trị thật vào E10–E15 → import thay groups → mất. (Đối chiếu: parser gói thầu ĐỌC `price_cost`=row[11], `price_bid_package`=row[15] từ file → pattern chuẩn là đọc từ file.)
- [x] Fix parser: đọc E10–E15 từ file → `price_max`=row[10], `price_min`=row[11], `price_cost`=row[12], `price_pre_contract`=row[13], `price_quotation`=row[14], `price_bid_package`=row[15]; output đủ 6 field.
- [x] Verify end-to-end (VT-XN-001, điền K–Q): parser trả price_max=10, price_min=20, price_cost=30, price_pre_contract=40, price_quotation=50, price_bid_package=60, price=100000. PASS.
- FE `handleImportSuccess` (cả 2 nhánh) đã map sẵn 6 field này → tự giữ sau khi parser trả về.
- Bug tiếp (2 hàng TB-KHAC-3324/3325 vẫn mất giá vốn): file export CÓ giá vốn 528tr/132tr (cột M/index12, parser đọc đúng). Nhưng `handleImportSuccess` gọi `updatePrice` (dòng 2340/2426) → hàm này TÍNH LẠI price_min/max/cost từ mảng `prices` (is_price_capital theo unit_id), fallback `|| ''`. 2 hàng này master KHÔNG có giá vốn khớp ĐVT → bị ghi đè rỗng (các hàng khác có nên không mất).
- [x] Fix `updatePrice`: khi không tìm thấy trong mảng `prices` thì GIỮ NGUYÊN giá trị hiện có (`foundX ? foundX.price : pro.price_x || ''`) cho cả price_min/max/cost → không xóa giá trị từ file/nguồn. Áp dụng cho cả import lẫn đổi ĐVT (không mất data).
- Yêu cầu rõ hơn của user: "giá vốn phải giữ nguyên từ thầu sang" — không được tính lại từ master khi import (kể cả khi master CÓ giá khác).
- [x] Fix triệt để: thêm cờ `keepPrices` cho `updatePrice(gIndex,pIndex,keepPrices=false)`. Khi `true` → BỎ QUA toàn bộ khối tính lại price_min/max/cost từ master, chỉ tính `price_difference_coefficient` từ giá file. 2 chỗ gọi trong `handleImportSuccess` (nhóm cũ dòng 2348, nhóm mới dòng 2435) truyền `true` → giá vốn/min/max giữ nguyên đúng từ file (= từ gói thầu). Đổi ĐVT (default false) giữ hành vi tính lại + preserve-on-no-match.

### Checkpoint — 2026-07-03
Vừa hoàn thành: Toàn bộ BE (migration + fillable) + FE (3 cột ghi chú: template/width/export/import + addNegotiation) + Import (rebuild file mẫu khớp export + parser align + FE store giữ 2 cột ghi chú) + Bugfix parser đọc đủ 6 cột giá tham chiếu. Verify end-to-end PASS.
Đang làm dở: (không)
Bước tiếp theo: User test trình duyệt (tạo HĐ từ báo giá/gói thầu; xuất Excel; sửa file rồi import lại kiểm 2 cột ghi chú không đổi).
Blocked: Cần user xác nhận: (1) để trống "Ghi chú hợp đồng" khi tạo từ nguồn; (2) parser đọc giá ở cột "Đơn giá bán (Gồm VAT)".
