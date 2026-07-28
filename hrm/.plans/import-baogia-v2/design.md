# Import báo giá v2 — Tóm tắt thiết kế

> Spec chi tiết: `docs/superpowers/specs/2026-07-23-import-baogia-v2-design.md`
> Nguồn spec: [Google Doc](https://docs.google.com/document/d/1YMDCqQGG3FJQCEk7iUM1Xge0kB_nUrPu/edit) (bản cập nhật 2026-07-23)
> Feature cha liên quan: `.plans/baogia-copy-export-import/`
> Phụ trách: @manhcuong

## Mục tiêu
Nâng cấp import/copy/export báo giá theo tài liệu mới: cột ẩn ID, luồng Update/Insert/Cross-import, mã hàng tạm theo "Hàng hóa dự án", partial import cho BOM, và các bổ sung copy/popup lỗi/export.

## Quyết định lớn đã chốt

### 1. Cột ẩn định danh (nền tảng)
File Excel mang **3 định danh ẩn**: **Line ID** (từng dòng), **ID Báo Giá nguồn**, **BOMList ID nguồn**. Export ghi ra, import đọc vào để phân luồng. Hiện code map theo **Mã hàng** → phải đổi sang map theo **Line ID**.

### 2. Phân luồng import (đọc ID Báo Giá ẩn) — popup chọn phương thức
| Case | Báo giá độc lập | Báo giá kế thừa BOM |
|---|---|---|
| **File của chính báo giá này / File trống** | Popup chọn: ① Từng phần (giữ dòng vắng) / ② Thay thế hoàn toàn | Mặc định **từng phần** (giữ dòng vắng, KHÔNG có option xóa) |
| **Cross-import** (ID Báo Giá ≠ hiện tại) | Popup chọn: ① Sao chép từng phần (giữ dòng cũ + append) / ② Thay thế hoàn toàn (xóa hết + insert) | Cùng BOM ID → cross-import từng phần (tuân thủ khóa cấu trúc). Khác BOM ID → **chặn cứng** |

- **Update**: Line ID khớp → UPDATE; trống → INSERT; dòng vắng → GIỮ (nếu chọn từng phần).
- **Cross-import**: luôn **xóa sạch Line ID** file (thuộc báo giá nguồn) → ép INSERT clone. Hàng tạm clone nguyên xi text, **không query Master Data**.
- Câu cảnh báo cũ "xóa & thay thế toàn bộ" ở Giai đoạn 1 → **bỏ**, thay bằng popup chọn phương thức ở Bước 2.

### 3. Mã hàng tạm → "Hàng hóa dự án" (chỉ báo giá độc lập)
"Hàng hóa dự án" = **view ảo union** `bom_list_products` (BOM tổng hợp đã duyệt) + `quotation_product_prices` (báo giá độc lập duyệt/trúng thầu) theo dự án — **không có bảng riêng** (xem memory `reference_hang_hoa_du_an_union_view`).
Mã hàng tạm là **tự sinh** → mã user nhập trong file **chỉ là "nhãn gom nhóm"** (đánh dấu các dòng là cùng 1 hàng), **BỊ VỨT** khi lưu, KHÔNG phải mã đích.
**Mã tự sinh** (= `ma-hang-tam-backend`): `HHBG`+pad(id,6) cho báo giá (`quotation_product_prices`), `HHB`+pad(id,6) cho BOM — theo `id` dòng, unique toàn cục. (`TMP-26-00001` trong doc chỉ là ví dụ format.)
**GOM (Rule 3) — chốt 2026-07-23 + đã code+test**: `saveDirectProduct` VỨT mã user nhập, tự sinh HHBG; các dòng CÙNG nhãn dùng CHUNG 1 mã (dòng đầu sinh HHBG → `$gomMap[nhãn]=HHBG` → dòng sau tái dùng). Verify DB: 2 dòng nhãn SP-DUP2 → cùng `HHBG002222`, vứt SP-DUP2 ✓. Update (price_id) giữ mã cũ; mã trống → mỗi dòng HHBG riêng.
- **Rule 1** mã đã tồn tại (trong view Hàng hóa dự án, theo dự án) → giữ mã, map data từ bản ghi đó (không sinh mới).
- **Rule 2** trống / chưa tồn tại + xuất hiện 1 lần → sinh mã theo nguyên tắc hiện tại (`HHBG`+id) + tạo bản ghi mới (ngầm định qua `quotation_product_prices`).
- **Rule 3** cùng mã (nhãn) chưa tồn tại xuất hiện **N lần** trong file:
  - Thông tin GIỐNG hệt (6 định danh: Tên/ĐVT/Model/TH/XX/TSKT + Giá nhập + Giá bán + VAT) → sinh **1** mã tự sinh chung (`HHBG`+id dòng đầu) gán cho cả N dòng.
  - Thông tin KHÁC → 🔴 lỗi chặn: "Mã hàng [X] xuất hiện ở nhiều dòng nhưng có sự khác biệt về thông tin định danh hoặc Giá nhập/Giá bán."

→ Gộp feature `ma-hang-tam-backend` (cơ chế mã tự sinh HHBG/HHB theo id) vào Phase 3 này.

### 4. Báo giá kế thừa BOM (Source_Type=BOMLIST)
- **Partial import**: dòng có trong file → UPDATE theo Line ID; dòng vắng → **giữ nguyên, KHÔNG xóa** (đảo logic hiện tại đang báo lỗi "thiếu mã BOM").
- Hàng gốc BOM: **khóa cứng** Mã/Tên/Model/ĐVT/TSKT/SL; chỉ cho sửa Đơn giá/GG/Ghi chú.
- Dòng mới: chỉ cho thêm **Dịch vụ**; thêm Hàng hóa → **chặn** + báo lỗi.

### 5. Sao chép báo giá (bổ sung)
- Popup review 4 loại: 🔴 Ngừng KD (+ khóa nút Gửi duyệt tới khi hàng active), 🟡 Đổi giá, 🟡 Đổi VAT, 🔵 Cấu trúc "(Bỏ qua)". Rỗng → skip popup.
- Đổi Dự án → xóa thông tin KH cũ + nạp KH theo dự án mới; **detach BOM** (BOM tổng hợp để trống → V2 thành báo giá độc lập).
- Tỷ giá lấy ERP hiện tại; hiệu lực auto-calc (ERP hàng hóa vs cấu hình dự án, ngày đến trước).

### 6. Popup lỗi import
Grid cuộn (Dòng Excel | Tên cột sai | Mô tả) + 3 nút **Sao chép lỗi / Tải File lỗi / Đóng**.

### 7. Export
Bỏ nút "Xuất file trắng"; giữ 1 nút "Xuất dữ liệu hiện tại" (tên file `[Mã_BG]_[DDMMYYYY].xlsx`). "Tải file mẫu" trong popup Import vẫn giữ (sheet `import_10790_KGG/_GG_tong/_GG_mat_hang` + `huong_dan_10790`).

### 8. Phân quyền validate (creator-based — thống nhất 4 màn)
Giá vốn hàng tạm hiện khi **có quyền "Xem giá vốn hàng hóa" HOẶC là người tạo báo giá** (`created_by == auth`). Hàng ERP: theo quyền. Áp cho **cả 4 màn**: import / copy / export / xem-sửa. (Trước đây từng để "temp luôn hiện" theo tài liệu — đã REVERT về creator-based theo chốt 2026-07-23; cần sửa mục "Phân quyền validate" trong Google Doc cho khớp.)
- Import `gateCost` = `canViewCost || (!isErp && isCreator)` ✓ (đã sửa)
- Export `canSeeCostOf` = `canViewCost || (!isErp && isCreator)` ✓ (đã sửa)
- View/sửa `DetailQuotationResource::canSeePrice` = `canViewCost || (!isErp && isCreator)` (đã đúng sẵn, không đụng)

### 9. Dịch vụ giá vốn
- Đã có % giá vốn ERP: giá nhập = giá bán × %; chưa có: lấy user nhập → khi Lưu, tính % thực tế cập nhật ngược Master Data ERP.

## Downstream / rủi ro
- Export phải thêm cột ẩn ID → mọi file mẫu + round-trip đổi.
- Đổi cơ chế map Mã hàng → Line ID: ảnh hưởng cả `validateDirectRows` + `validateBomRows` + save.
- Cross-import/full-replace đụng luật "cấm xóa vật tư BOM" — cần đặc tả kỹ giao thoa.
