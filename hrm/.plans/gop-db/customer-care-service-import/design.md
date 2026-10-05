# Import Excel — màn Danh mục gói bảo dưỡng

**Người phụ trách:** @khoipv — 2026-09-22
**Nhánh:** `gop_db` (cả 2 repo, code thẳng trên nhánh này)
**Spec đầy đủ:** [docs/superpowers/specs/gop-db/2026-09-22-customer-care-service-import-design.md](../../../docs/superpowers/specs/gop-db/2026-09-22-customer-care-service-import-design.md)
**Plan:** [plan.md](plan.md)

---

## Mục tiêu

Khai báo hàng loạt gói bảo dưỡng (`/customer-care/services`) bằng 1 file Excel nhiều sheet,
thay vì gõ tay từng gói trên form (mỗi gói hiện phải nhập tay bảng nội dung kiểm tra ×
cấp bảo dưỡng, hệ số theo công ty và danh sách hàng hoá).

## Bối cảnh

Feature `catalog-import-export` (13 màn danh mục) đã **loại màn này ra khỏi scope** vì
"trang tạo có bảng chi tiết, file phẳng không chở được". Lần này làm riêng cho màn gói bảo
dưỡng với file **nhiều sheet** — user chốt 2026-09-22.

## Quyết định đã chốt

| # | Quyết định |
| --- | --- |
| Q1 | File mẫu **5 sheet**, khoá nối giữa các sheet là **Mã gói**. KHÔNG kèm sheet "Danh mục tham chiếu" (user chốt 22/09) — tên danh mục tra ở chính màn danh mục, gõ sai thì Validate chỉ rõ dòng |
| Q2 | **KHÔNG đính kèm PDF trong luồng import** (user chốt 22/09 sau khi chạy thử): gói import xong để trống hồ sơ, người dùng vào màn Sửa bổ sung file sau. Form tạo/sửa tay vẫn bắt buộc PDF — ràng buộc đó nằm ở `ServiceRequest`, import gọi thẳng service nên không đi qua |
| Q3 | Import **chỉ thêm mới**. Mã/tên trùng (trong file hoặc trong DB) → dòng đó báo "Đã tồn tại", các gói hợp lệ vẫn được tạo. Không upsert |
| Q4 | Modal **riêng** `ServiceImportModal.vue` dựng trên khuôn popup dùng chung **`V2BaseModal`** (skill `modal-popup` mục 0), bên trong **dùng lại nguyên** `V2BaseImportToolbar` + `V2BaseImportTable` → UI/thao tác giống hệt 15 màn kia mà KHÔNG sửa component dùng chung. Button theo `button-convention` (Import Excel = cam `ri-upload-line`; footer `tertiary`, Đóng cuối); popup gắn `unsavedModalMixin` |
| Q5 | Mỗi hạng mục kiểm tra phải khai **đủ mọi cấp** đã khai ở sheet 2 — đúng ràng buộc `maintains.*.levels.*.note_maintenance_ids` của `ServiceRequest` |
| Q6 | Sheet 4 (hệ số theo công ty) và sheet 5 (hàng hoá) **không bắt buộc**, để trống vẫn import được |
| Q7 | Ghi dữ liệu bằng cách gọi lại `ServiceService::store()` sẵn có (không `Service::create()` thẳng) để `logCatalogCreate()` vẫn chạy → Lịch sử thay đổi không thủng |
| Q8 | Đối chiếu danh mục (công ty, cấp, ghi chú kiểm tra, ĐVT, nhóm hàng, mã hàng) theo **tên/mã, không phân biệt hoa thường**. **Không** tự tạo danh mục mới — tên lạ là lỗi dòng |
| Q9 | Gói tạo qua import ở trạng thái **Hoạt động** (khuôn `store()`, giống tạo tay) |
| Q10 | Nút Import gate đúng quyền **`Thêm danh mục gói bảo dưỡng`** (bằng nút Tạo mới); không đủ quyền thì **ẩn** nút |

## Cấu trúc file mẫu `Mau_import_goi_bao_duong.xlsx`

Mỗi sheet: dòng 1 tiêu đề (cột bắt buộc có ` *`), dòng 2 gợi ý, dữ liệu **từ dòng 3**.

| Sheet | Bảng đích | Cột |
| --- | --- | --- |
| `1. Gói bảo dưỡng` | `services` | Mã gói * · Tên gói * · Công ty quản lý * · VAT (%) · Định mức đàm phán giá (%) · Hệ số giá bán · Ghi chú |
| `2. Cấp bảo dưỡng` | `service_levels` | Mã gói * · Cấp bảo dưỡng * · Định mức công * · Hệ số công nghệ · Giá bán cơ sở · Gợi ý hàng hoá |
| `3. Nội dung kiểm tra` | `service_maintains` + `service_maintain_levels` | Mã gói * · STT hạng mục * · Nội dung kiểm tra bảo dưỡng * · ĐVT * · SL * · Cấp bảo dưỡng * · Ghi chú kiểm tra * |
| `4. Hệ số theo công ty` | `company_service_coefficients` | Mã gói * · Công ty * · Hệ số * |
| `5. Hàng hoá` | `service_has_products` | Mã gói * · Mã hàng * · Nhóm hàng * |

## ⚠️ GOTCHA

- **`service_levels.benefit_coefficient` NOT NULL, không default** — ô "Hệ số công nghệ" bỏ trống
  mà truyền `null` là SQL nổ 1048 (đã dính khi test import trên trình duyệt 22/09, gói thứ 3 rớt).
  Trống → quy về **1**. `base_price` nullable nên trống giữ `null`.
- Tên cột file mẫu bám **chữ trên màn** (`ServiceFormComponent`), không bám
  `ServiceRequest::attributes()` — 2 nơi gọi khác nhau.

- **Dấu phẩy trong ô số là dấu THẬP PHÂN** (bài học màn `costs`) — không strip phẩy khi đọc
  VAT / hệ số / giá cơ sở.
- `service_levels` lấy từ `maintains[0].levels` trong khuôn ERP → sheet 2 phải sinh đúng
  `levels` của hạng mục đầu tiên, nếu không định mức công/giá cơ sở rơi mất.
- `Service::setCodeAttribute()` tự viết hoa mã — so trùng phải `LOWER(TRIM())` cả 2 vế.
- Gói import xong có `attachments = null`. Mở màn **Sửa** rồi bấm Lưu thì `ServiceRequest` đòi
  file PDF (`required_without_all`) → người dùng buộc phải đính kèm ở lần sửa đầu tiên.
- `V2BaseImportModal` chỉ đọc 1 sheet (`Data` hoặc sheet đầu) → luồng này dùng helper riêng
  `import-multi-sheet-helper.js`, KHÔNG sửa `parseExcelFile()` (15 màn đang chạy).
- Mỗi gói một `DB::transaction` riêng — 1 gói lỗi không kéo đổ cả lô.
