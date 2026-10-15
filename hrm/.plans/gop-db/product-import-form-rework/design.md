# Design (tổng) — Rework form Tạo/Sửa Phiếu nhập hàng (HRM Finance)

Nhánh: `gop_db`. Màn: `pages/finance/product-imports/` (HRM). Nguồn nghiệp vụ: ERP
`warehouse/product_imports` (Controller `Warehouse\ProductImportsController`, view
`resources/views/warehouse/product_imports/form.blade.php`).

Spec chi tiết theo cụm: `design-phase{N}.md`. Tài liệu này chỉ giữ scope + hiện trạng + quyết định chung.

## Yêu cầu user (2026-10-08)

> "phiếu nhập hàng form tạo mới có ô cho phép chọn phiếu nhập kho và thay đổi được phiếu, thông tin
> các trường thay đổi tuỳ theo loại nhập hàng, box chi tiết chứa thông tin hàng hoá cũng vậy, các tab
> cũng vậy, các cột trong tab hàng hoá cũng vậy sẽ thay đổi theo loại nhập hàng. Rà soát lại phiếu
> nhập hàng đã port từ ERP sang HRM và sửa lại logic cho đúng, tôi muốn giống hết kể cả bố cục form…
> chỗ danh mục kho kế toán ở đây lấy không cần quyền."

Làm rõ thêm:
- Ảnh chụp chỉ để minh hoạ 2 màn đang khác nhau — **phải tự rà soát ERP, port đầy đủ & chính xác
  TẤT CẢ các loại** (không chỉ 2 loại trong ảnh).
- "Làm từng bước, tạo task, làm từ từ" → chia cụm, verify từng cụm.

## Quyết định chung (đã chốt với user)

1. **Độ trung thành UI = Hướng A** (user chốt 2026-10-08): giống ERP về **nghiệp vụ & cấu trúc
   thông tin** (đủ trường/tab/cột/dòng hạch toán, động theo loại, đặt đúng nhóm) nhưng **dựng bằng
   component HRM** (V2Base*, V2Footer, badge HRM, số kiểu `1,234,567.89`). KHÔNG bê nguyên bố cục
   AngularJS của ERP. Theo skill `erp-to-hrm-screen`: ERP = nguồn nghiệp vụ, HRM = nguồn giao diện.

2. **Phạm vi loại** = **8 loại TẠO TAY của ERP** (constant.js `IMPORT_TYPES`):
   `2` Mua trong nước · `3` Mượn trả lại · `4` Bán trả lại · `9` Nhập bán mượn trả lại ·
   `11` Mua nước ngoài mới · `14` Nhập gửi · `15` Mua trong nước tự do · `99` Khác.
   10 loại còn lại (5,6,7,8,10,12,13,16,17,20) ERP **tự sinh từ luồng khác**, KHÔNG tạo tay ở màn
   này → không đưa vào form tạo tay (trừ khi user yêu cầu khác).

3. **Chia cụm, verify từng cụm** (user chốt "làm từ từ"):
   - **Cụm 1** — Khung động + loại `4` (loại HRM đang chạy). Dựng lại form chuẩn HRM, nút đổi PNK,
     khung tab/cột/hạch toán điều khiển theo `import_type`; trước mắt chỉ nuôi loại 4 cho khỏi vỡ.
   - **Cụm 2** — Nhóm mua trong nước: `2`, `15`, `99`.
   - **Cụm 3** — Nhóm nước ngoài & mượn/gửi: `11`, `3`, `9`, `14`.

4. **Danh mục kho kế toán KHÔNG cần quyền**: trên `gop_db` endpoint
   `ProductImportController::accountingWarehouses` **đã ungated sẵn** (không check permission). Nếu
   còn lỗi "không tải được danh mục" → nguyên nhân là **dữ liệu** (phiếu nguồn thiếu
   `warehouse_id`/`company_id`, hoặc lọc hàng ký gửi), KHÔNG phải quyền → điều tra data, không sửa quyền.

## Hiện trạng port HRM (điểm phải sửa)

- BE `ProductImportService` là **stub có chủ đích**: `buildDetailsByType()` chỉ có case
  `BAN_TRA_LAI` (type 4), mọi loại khác **ném 422** ("… chưa được hỗ trợ ở HRM"). `store()` chặn
  type≠4. Creatable list chỉ có 4.
- FE `ProductImportForm.vue`: 3 tab cứng + 1 bộ cột, **không động theo `import_type`**; PNK pick xong
  **không đổi được** (thiếu nút mở lại modal); dùng `<select>`/`<input>` thô + thanh nút tự chế (lệch
  V2Base/V2Footer).

## Nền tảng gop_db (bắt buộc nhớ)

- DB gộp, KHÔNG `mysql2`. `auth()->id()` = 1 employee id. Trùng tên bảng → ưu tiên bảng ERP.
- Màn trong `Modules/Finance`; route group `/product-imports` KHÔNG middleware spatie (role ERP
  `model_type='App\Employee'`) → gate store/update nằm trong Service.

## Map loại → tab / bảng / hạch toán (tóm tắt từ ERP — chi tiết ở design-phase)

| Loại | Tên | Bảng HH biến thể | Ghi chú đặc thù |
|---|---|---|---|
| 4 | Bán trả lại | mặc định (C) | DT 5212, kho 1561/157, GV 632, CK 5211, GG 5213, thuế 33311 |
| 2 | Mua trong nước | VAT (B) | có 3311 / kho 1561 / thuế 1331 / CP 1562 |
| 15 | Mua trong nước tự do | VAT (B) | gần type 2; phân bổ theo giữ (allocation_all) |
| 99 | Khác | mặc định (C) | linh hoạt |
| 11 | Mua nước ngoài mới | nước ngoài (A) | ngoại tệ/currency; allocation_all |
| 3 | Mượn trả lại | mặc định (C) | — |
| 9 | Nhập bán mượn trả lại | mặc định (C) | giống nhóm bán/mượn |
| 14 | Nhập gửi | mặc định (C) + cột hạn gửi | CHỈ kho ký gửi (consignment) |

Cờ dẫn xuất (ERP `ProductImport.blade.php`): `is_foreign = type∈{1,11}`; `has_inland_cost = type≠3`;
`has_delivery = transition_type==2`; `showListedPrice type∈{4,9,13}`; `allocation_all type∈{11,15,2,16}`.
