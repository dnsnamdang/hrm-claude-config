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
