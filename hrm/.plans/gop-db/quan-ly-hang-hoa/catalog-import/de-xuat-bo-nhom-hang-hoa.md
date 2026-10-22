# Đề xuất: bỏ Nhóm hàng hoá (`groups`), chuyển sang cây phân loại mới (16/10/2026)

User chốt 16/10: *"Nhóm hàng hoá sau khi chuyển đổi xong sẽ bỏ đi"*. Tài liệu này là ĐỀ XUẤT — chưa có code.
Nguồn: khảo sát code HRM + ERP (2 agent, 16/10), số đo DB `hrm_erp_giacty`, `nhom-hang-sang-loai-sp.md`.

## 1. Bài toán
- Nhóm hàng (893 nhóm) ↔ Loại SP (957 loại trong cây mới) là **nhiều–nhiều** (file "Quan hệ HH": 1.691 cặp; 277 nhóm ↔ >1 loại).
  ⇒ KHÔNG thay `group_id` bằng `product_type_id` 1–1 được. Mọi chỗ đang "theo nhóm" phải chọn lại căn cứ:
  theo **hàng hoá** (`products.product_type_id`) hoặc theo **một cấp của cây** (Loại SP / Nhóm SP / Nhóm CN / Tính chất).
- Feature lên prod MỘT lần ⇒ bỏ nhóm phải xong trong cùng đợt, hoặc tách đợt riêng SAU go-live (xem §6 câu Q1).

## 2. Chỗ đang dùng nhóm hàng — phân 6 loại

### A. Thuộc tính hàng kế thừa từ nhóm (ERP đọc lúc chạy)
| Thuộc tính `groups.*` | Dùng ở | Trên `product_types` | Dev |
|---|---|---|---|
| `vat_percent(_tax_rate_id)` | VAT dự phòng khi hàng trống VAT (popup tìm hàng ERP `SearchController:894,1701,2054`); job dội VAT xuống hàng; HRM `TaxRateService:87-104` dội xuống nhóm | CÓ `vat_percent_tax_rate_id` | 879 nhóm có |
| `long_stock_days` | Báo cáo Tồn lâu ERP (`Product.php:6822-6874`, INNER theo nhóm) | CÓ | 751 nhóm có |
| `must_serial` | Bắt serial khi lập biên bản bàn giao ERP (`HandoverAcceptanceRecordStoreRequest:62-90`) | CÓ `serial_required` | 0 nhóm bật |
| `rate_liquidation` | Giá thanh lý dự phòng; BG thanh lý / định giá **ghi đè** tỷ lệ theo nhóm (`LiquidationQuotation:51`, `CostFixingQuotation:51`) | **KHÔNG CÓ** | 0 nhóm (hàng có riêng: 1.251) |
| `checksheet_id` | Phiếu kiểm tra (checksheet) gắn theo nhóm (`Tech/Checksheet.php:74-105`) | **KHÔNG CÓ** | 0 nhóm |
| barcode/ingredient/warning/user_manual | in tem — đường đang chạy đã đọc `product_types` (`Product::barcodeInfoOf`) | CÓ | — |

### B. Cấu hình nghiệp vụ khoá theo nhóm
| Cấu hình | Bảng | Dev |
|---|---|---|
| Hệ số công lắp đặt (CSKH, ERP `WrAssignTask:936`) | `benefit_rate_has_group_products` | 0 dòng |
| Cấu hình hệ số Assign | `assign_benefit_rate_has_groups` | 0 dòng |
| Số thợ theo hạng mục / công khoán | `contract_rows.product_groups` (JSON) | 8 dòng `[null]` |
| Nhóm lỗi thiết bị | `device_error_has_group_product` | 0 dòng |
| **Nhóm máy** — phụ tùng "dùng cho nhóm máy X" + picker lọc theo nhóm của máy | `productables` (morph `App\Model\Product\Group`) | **3.968 dòng** |
| Danh mục CRM (`categ_id`) đồng bộ theo nhóm | `ModuleMapping(Group)` | ? |

### C. Cột "chụp" nhóm trên dòng chứng từ (lịch sử)
`contract_products` 32 · `quotation_products` 155 · `firm_contract_promotions` 4.091 · `firm_quotation_promotions` 2.061 ·
`service_has_products` 4.896 · `handover_acceptance_record_products` 0 · `root_contract_products` 0 · `project_contract_products` 0.

### D. Bộ lọc / báo cáo / xuất Excel
ERP: ~10 truy vấn báo cáo kho lọc `p.group_id`; **~30 INNER JOIN `groups`** (StockTransferReport, MarketCommodity*, ProductExportDetail) ⇒
hàng không nhóm biến mất im lặng; ~111 blade có ô lọc nhóm. HRM: lọc thiết bị KH (`CustomerManagerService`), lỗi thiết bị
(+ export), tra tồn bán được, dự án sản phẩm.

### E. Catalog
`product_group_classifies` (nhóm → Lĩnh vực/Chương/Mục/Tiểu mục, 1.019 dòng) — HRM BOM hiện Lĩnh vực/Chương, option gói dịch vụ,
ERP lọc catalog. Thay bằng `product_business_catalogs` (hàng ↔ Tiểu mục, đã có, 21 dòng) — nối việc import catalog.

### F. Dữ liệu gốc / màn
`products.group_id` 45.890 · `product_templates.group_id` 29.813 · `tmp_products` 1.957 · `attribute_groups.group_id` 2.434
(thuộc tính theo nhóm — đã có `product_type_attributes`) · màn Nhóm hàng ERP đã khoá (`productMovedToHrm`), còn `groups.searchData`
cho select2 màn Dịch vụ / Lỗi thiết bị · CRUD/import nhóm ERP · `CompanySyncErp:171` (kiểm lại có phải nhóm hàng).

## 3. Nguyên tắc chuyển
1. **Căn cứ gốc = Loại SP của từng hàng** (`products.product_type_id`). Điền xong cho toàn bộ hàng đang dùng là điều kiện TRƯỚC mọi bước sau.
2. Bảng cầu tạm `group_product_type` (1.691 cặp từ file) — chỉ dùng lúc chuyển đổi, xoá cùng `groups`.
3. **Thuộc tính (A)**: chuyển sang Loại SP; giá trị điền từ nhóm qua bảng cầu — các nhóm của 1 loại cùng giá trị thì lấy, khác nhau ⇒ danh sách xung đột cho nghiệp vụ chọn.
4. **Cấu hình "áp dụng cho nhóm" (B)**: nhóm G ⇒ mọi Loại SP nối với G (mở rộng an toàn cho quy tắc "áp dụng"). Quy tắc có ràng buộc "1 nhóm chỉ thuộc 1 cấu hình" ⇒ loại nối với 2 nhóm thuộc 2 cấu hình khác nhau = xung đột, liệt kê.
   Riêng **Nhóm máy** (3.968 liên kết): đổi sang "dùng cho Loại SP" — picker lọc theo Loại SP của máy.
5. **Cột chụp (C)**: bỏ FK, ngừng ghi, hiển thị chuyển sang Loại SP của hàng; xoá cột khi xoá bảng (lịch sử nhóm không giữ — xác nhận Q4).
6. **Lọc/báo cáo (D)**: đổi sang lọc theo cây (đề xuất chọn được Nhóm SP / Loại SP — 957 loại quá mịn cho báo cáo); INNER JOIN → theo `product_type_id`.
7. **Xoá**: ngừng ghi `group_id` mọi nơi ⇒ bỏ 13 FK ⇒ xoá cột ⇒ xoá `groups`, `attribute_groups`, `product_group_classifies`, màn/route/model nhóm.

## 4. Lộ trình đề xuất
| Bước | Nội dung | Phụ thuộc |
|---|---|---|
| 0 | Nhập cây 4 cấp (file sửa theo `can-sua-cay-phan-loai-1610.xlsx`) | nghiệp vụ sửa file |
| 1 | Gán Loại SP cho hàng: (a) sheet hàng theo mã (7.984 khớp) ⇒ (b) nhóm 1–1 qua bảng cầu ⇒ (c) còn lại xuất danh sách cho nghiệp vụ | bước 0 |
| 2 | Thuộc tính (A): thêm `rate_liquidation`, `checksheet_id` vào `product_types` (nếu giữ nghiệp vụ); điền từ nhóm; ERP/HRM đọc từ Loại SP | bước 1 |
| 3 | Cấu hình (B) đổi khoá sang Loại SP + chuyển dữ liệu (đo prod trước) | bước 1 |
| 4 | Lọc/báo cáo (D) HRM + ERP | bước 1 |
| 5 | Catalog (E) theo `product_business_catalogs` | import catalog |
| 6 | Ngừng ghi, bỏ FK, xoá cột/bảng/màn (C, F) | 2–5 |

## 5. Rủi ro
- Hàng chưa gán Loại SP (hiện: 20.398 hàng đang dùng ngoài sheet hàng) ⇒ mất VAT dự phòng, rơi khỏi báo cáo, không được hệ số công.
- Số liệu dev ≠ prod (cấu hình B trên dev gần rỗng) ⇒ đo lại trên prod trước khi chốt cách chuyển dữ liệu.
- ERP nhiều chỗ (111 blade, ~40 truy vấn) ⇒ khối lượng lớn nhất nằm ở ERP.

## 6. Câu hỏi cho user (hỏi lần lượt)
- Q1. Bỏ nhóm trong CÙNG đợt go-live Chuyển đổi hàng hoá, hay đợt riêng sau? (cùng đợt ⇒ go-live lùi; đợt sau ⇒ nhóm sống song song 1 thời gian, hàng mới tạo trên HRM không có nhóm.)
- Q2. 20.398 hàng đang dùng ngoài sheet hàng: gán theo nhóm 1–1 (một phần) + nghiệp vụ gán tay phần còn lại?
- Q3. `rate_liquidation` / `checksheet_id` theo nhóm: còn dùng không? (dev 0 nhóm có giá trị) — bỏ hẳn hay chuyển sang Loại SP?
- Q4. Cột nhóm trên chứng từ cũ (C): bỏ hẳn lịch sử nhóm, hay chép tên nhóm thành chữ để báo cáo cũ còn đọc được?
- Q5. Báo cáo lọc theo cấp nào của cây (Nhóm SP / Loại SP / cả hai)?

## 7. User chốt (18/10/2026)
- **Q1 = Chia 2.** Cùng go-live: bước 1 (gán Loại SP cho toàn bộ hàng) + A (VAT dự phòng, `long_stock_days` sang Loại SP) + D (~30 báo cáo ERP INNER JOIN `groups` ⇒ theo `product_type_id`). Đợt sau go-live: B (cấu hình theo nhóm), C (cột chụp nhóm trên chứng từ), E (catalog), F (xoá bảng/cột/màn). Nhóm cũ sống song song tới đợt sau.
- **Q2 = chưa chốt cách gán.** User: *"Tôi gửi file danh mục 4 cấp ⇒ xử lý trước"* — làm bước 0 (nhập cây 4 cấp từ file mới của user) trước, rồi mới quyết cách gán Loại SP cho 20.398 hàng ngoài sheet. Q3–Q5 hỏi tiếp sau khi xử lý file.
- 18/10 (sau khi rà file 17/10 — xem README): **Q2 ⇒ user yêu cầu xuất Excel hàng nhóm c + d** để tự xử lý. File `hang-can-gan-loai-sp-C-D-1810.xlsx` (bản chép `~/Desktop/`; sinh lại: `python3 -I xuat_hang_c_d.py <file17> <groups.tsv> <inuse.tsv> <out>`): sheet C 14.507 hàng / 266 nhóm (18/10 user chỉnh: chỉ 2 cột sát nhau "Nhóm hàng hoá cũ" – "Loại hàng hoá"; ô chọn mỗi nhóm chỉ gồm Loại của nhóm đó, cảnh báo nếu gõ ngoài), sheet D 2.045 hàng / 202 nhóm, sheet "Cây 4 cấp" 968 Loại; cột vàng "Loại SP (chọn)" có danh sách chọn. Chờ user gửi lại file đã điền ⇒ rồi hỏi Q3–Q5. (Nhóm 1–1 = 3.846 hàng, chưa xuất — mặc định gán tự động theo nhóm, chưa chốt.)
- 19/10: bản "mỗi hàng × Loại 1 dòng" ra 370.755 dòng (17 MB — nhóm 2283 "Nhóm chung chưa phân loại" 147 Loại × 1.474 hàng) ⇒ user: **"Xử lý 4 cấp phân loại trước ⇒ nhóm để sau"**. Việc gán Loại cho hàng nhóm c/d TẠM GÁC; file Desktop hiện là bản 370.755 dòng (chưa dùng).
- 19/10 ghi thêm (mục F `attribute_groups`): form hàng HRM tab "Thông số kỹ thuật" › khối "Thuộc tính theo loại sản phẩm" đọc `product_type_attributes` (API `attributes-by-type`), KHÔNG đọc nhóm; nhóm chỉ còn dùng ở form hàng ERP cũ (đã khoá) + `ImportProductAttribute` ERP. Sau import cây: `product_type_attributes` = 0 ⇒ mọi Loại mới hiện "Loại sản phẩm này chưa khai thuộc tính". Có thể chuyển 2.434 liên kết nhóm–thuộc tính (644 nhóm, 427 thuộc tính) sang Loại qua bảng cầu — chưa hỏi user. Giá trị thuộc tính của hàng (`attribute_products` 51.128 dòng / 17.736 hàng) không phụ thuộc nhóm.
- 19/10 tách 307 nhóm DB chưa có trong file 17/10 ⇒ `nhom-chua-co-loai-1910.xlsx` (bản chép Desktop; sinh lại `tach_nhom_chua_co_loai.py`): khoá 2 (1999 "Nhóm xóa 26", 2535 "Phòng sơn sấy xe bus" — 0 hàng) · hoạt động không có hàng 53 · chỉ hàng đã xoá 50 (199 hàng) · còn hàng đang dùng 202 (2.045 hàng dùng) ⇒ chỉ 202 nhóm cần nghiệp vụ map Loại.
- **20/10 — Q2 user chốt:** *"Chỉ xử lý các nhóm đã mapping 1-1 với Loại ⇒ còn lại chờ cập nhật dần"*. Gán tự động cho hàng thuộc nhóm cũ ứng ĐÚNG 1 Loại (b — 3.846 hàng đang dùng theo số 18/10); hàng nhóm c (nhóm ↔ nhiều Loại, 14.507) + d (nhóm chưa có Loại, 2.045) ĐỂ TRỐNG Loại, nghiệp vụ cập nhật dần trên màn Hàng hoá. Trạng thái giacty 20/10: 0/28.378 hàng đang dùng có Loại; cây 6/48/282/968; `product_type_attributes` 0. Còn hỏi: nhóm a (7.980 hàng có Loại ghi theo mã trong file 17/10) có gán không.
- **20/10 — nhóm a user chốt "Gán theo file":** 7.980 hàng có mã trong file 17/10 gán Loại ghi theo mã (ưu tiên file khi lệch với suy theo nhóm). Tổng gán đợt go-live = a + b ≈ 11.826/28.378 hàng đang dùng; c + d ≈ 16.552 để trống, cập nhật dần.
- **20/10 — VAT (mục A), user:** *"VAT ở nhóm chỉ có tác dụng update hàng loạt cho hàng hoá, bản thân mỗi mã hàng đã lưu VAT riêng rồi"*. Đo giacty: 27.443/28.378 hàng đang dùng có VAT riêng; **935 hàng trống VAT** (916 có nhóm VAT>0) — ERP popup tìm hàng dự phòng VAT nhóm cho đúng nhóm này (`Common/SearchController.php:856,1703,2065`, `vat ?: group->vat`; dòng :1265 không dự phòng). Hàng VAT = 0: 0 hàng (nếu có sẽ bị `?:` coi như trống). ⇒ VAT KHÔNG cần chuyển sang Loại SP; chỉ còn xử lý 935 hàng trống (đang hỏi).
- **20/10 — 935 hàng trống VAT, user chốt "Chép VAT nhóm vào hàng 1 lần":** trước go-live ghi VAT nhóm vào hàng trống (916 trên giacty — đo lại prod); 19 hàng nhóm cũng trống ⇒ danh sách cho nghiệp vụ. Sau đó ERP bỏ dự phòng `group->vat_percent` (3 chỗ SearchController). Bước ghi dữ liệu hỏi riêng.
- **20/10 — Số ngày tồn lâu, user chốt "Theo Loại SP, thiếu thì mặc định 180":** điền 180 cho 968 Loại (sửa được từng Loại); báo cáo Tồn lâu ERP (`Product.php:6798/6830`, `ProductInfo.php:3466/3499`, `ProductTemplate.php:6357` — đang INNER JOIN `groups`, `g.long_stock_days != null`) đọc theo Loại của hàng, hàng chưa có Loại ⇒ 180. Số đo giacty: 748 nhóm 180 · 3 nhóm 60 (2526/2527/2528 EM, 9 hàng) · 142 nhóm trống (4.890 hàng đang dùng — sẽ BẮT ĐẦU vào báo cáo).
- **20/10 — Báo cáo (mục D), user chốt "LEFT JOIN, giữ ô lọc Nhóm":** go-live chỉ đổi ~30 INNER JOIN `groups` → LEFT JOIN (hàng không nhóm vẫn hiện, cột Nhóm trống); ô lọc Nhóm (~111 blade, ~10 truy vấn `p.group_id`) giữ nguyên; đổi sang lọc theo cây ở đợt sau (Q5 hỏi lúc đó).
- **20/10 — Q3, user chốt "Bỏ hẳn, đo prod trước":** không thêm `rate_liquidation`/`checksheet_id` vào Loại SP; ERP ngừng đọc 3 thuộc tính nhóm (`rate_liquidation`, `checksheet_id`, `must_serial`) khi xoá nhóm (đợt sau). Tỷ lệ thanh lý theo hàng (887 hàng có), serial theo Loại (`serial_required`). Điều kiện: prod cũng 0 nhóm dùng — khác 0 thì hỏi lại.

### Phạm vi go-live sau các chốt 20/10 (chưa code — mỗi bước xin phép riêng)
1. Gán Loại SP: a (7.980, theo mã file 17/10, ưu tiên file) + b (3.846, nhóm 1–1). c + d để trống.
2. Chép VAT nhóm vào ~916 hàng trống VAT (đo prod); 19 hàng nhóm cũng trống ⇒ danh sách nghiệp vụ. ERP bỏ dự phòng VAT nhóm (3 chỗ SearchController).
3. `product_types.long_stock_days` = 180 cho 968 Loại; báo cáo Tồn lâu ERP (5 chỗ) đọc theo Loại, thiếu ⇒ 180.
4. ~30 báo cáo ERP INNER JOIN `groups` → LEFT JOIN; ô lọc Nhóm giữ.
Đợt sau: B cấu hình theo nhóm (Nhóm máy 3.968 liên kết…), C cột chụp (Q4), E catalog, F xoá bảng/cột/màn + 3 thuộc tính Q3, lọc theo cây (Q5).
Còn mở chưa hỏi: chuyển 2.434 liên kết `attribute_groups` (nhóm–thuộc tính) sang `product_type_attributes` qua bảng cầu (form hàng HRM đọc thuộc tính theo Loại — hiện 0 ⇒ mọi Loại "chưa khai thuộc tính").
- **20/10 — user: "chuyển luôn thuộc tính + Nhóm máy từ nhóm sang loại qua mapping Nhóm - Loại".** Bảng ghép = file 17/10 sheet `NewERP Green Power` (cột I ID nhóm cũ × cột E Loại): 587 nhóm · 1.696 cặp · 309 nhóm 1–1; tên Loại khớp `product_types` 100%. Đo (giacty, `do_chuyen_thuoc_tinh_nhom_may.py <file17> <thư mục tsv>`):
  - **Thuộc tính** (`attribute_groups` 2.434 liên kết / 644 nhóm / 427 thuộc tính → `product_type_attributes`): 1.779 liên kết / 452 nhóm có trong bảng ghép ⇒ 2.861 cặp Loại–thuộc tính trên 642 Loại; 235 Loại nhận từ >1 nhóm, 215 trong đó các nhóm nguồn có bộ thuộc tính KHÁC nhau; **655 liên kết / 192 nhóm không có trong bảng ghép**.
  - **Nhóm máy** (`productables` morph `App\Model\Product\Group` 3.968; còn dùng 3.430 liên kết / 2.455 hàng phụ tùng / 168 nhóm máy; ERP picker lọc theo `group_id` của MÁY — `Common/SearchController.php:694,911,1132,1353,1575,1964`; HRM form `machine_group_ids` `ProductFormResource:106`): 3.163 liên kết / 136 nhóm có trong bảng ghép ⇒ 6.184 cặp hàng–Loại (×2,0); **267 liên kết / 32 nhóm / 240 hàng không có trong bảng ghép**. Nhóm rộng: 2283 "Nhóm chung chưa phân loại" 147 Loại · 2294 "PT, VTTT cho phòng sơn, phòng chà" 75 · 2388 27 · 2480 16 · 2475 15.
- **20/10 — user chốt: thuộc tính + Nhóm máy CHỈ chuyển nhóm có 1 Loại** (nhóm → đúng 1 Loại trong bảng ghép; 309 nhóm), phần còn lại user xử lý dần. Số đo (`do_chuyen_1_1.py`): **Thuộc tính** 995/2.434 liên kết / 252 nhóm ⇒ 957 cặp Loại–thuộc tính / 234 Loại (11 Loại nhận từ 2+ nhóm 1–1, bộ khác nhau ⇒ gộp hợp). **Nhóm máy** 1.592/3.430 liên kết còn dùng / 79 nhóm / 1.215 hàng phụ tùng. Liên kết qua nhóm nhiều Loại / nhóm chưa có Loại giữ nguyên ở nhóm.
- **20/10 — lọc phụ tùng "dùng cho máy X", user chốt "Theo Loại HOẶC theo Nhóm":** ERP picker (6 chỗ `Common/SearchController`) hiện phụ tùng gắn Loại của máy HOẶC gắn Nhóm của máy. Liên kết nhóm 1–1 đã chép sang Loại thì XOÁ khỏi nhóm (1 nguồn, tránh lệch khi sửa); liên kết nhóm nhiều Loại / chưa có Loại giữ ở nhóm tới khi user xử lý. HRM form hàng cần thêm ô "Dùng cho Loại máy" cạnh `machine_group_ids` (morph mới cho `product_types` — chốt tên lúc làm).

### Phạm vi go-live cập nhật 20/10 (thêm 5–6 vào danh sách 1–4 ở trên)
5. Thuộc tính: nhóm có 1 Loại ⇒ chép `attribute_groups` sang `product_type_attributes` (957 cặp / 234 Loại, gộp hợp).
6. Nhóm máy: nhóm có 1 Loại ⇒ chuyển `productables` Group → Loại (1.592 liên kết / 1.215 hàng), xoá bản nhóm; ERP picker lọc Loại OR Nhóm; HRM form thêm ô Loại máy.
- **20/10 16:20 — SỬA SỐ VAT:** "935 hàng trống VAT" ở trên SAI (đếm `= ''` trên cột decimal khớp cả VAT 0). Đúng: **363 hàng đang dùng VAT NULL** — 346 nhóm VAT > 0 (chép), 17 nhóm VAT 0 (danh sách). ERP không cast `vat_percent` ⇒ "0.00" là có VAT, chỉ NULL mới dự phòng nhóm.
- **20/10 — user: go-live tối 20/10 19h.** Gói dữ liệu: `golive-2010/` (README + `golive_bo_nhom_2010.sql` + `ds-hang-vat-trong.xlsx`). Nhóm máy + code ERP chưa vào gói.
