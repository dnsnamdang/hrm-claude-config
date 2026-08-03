# Đổi định dạng tiền tệ luồng quản lý dự án — Design

> Phụ trách: @dnsnamdang · Branch: `tpe-develop-assign`

## Mục tiêu
Chuẩn hoá định dạng số tiền trên luồng **quản lý báo giá/BOM/dự án** (module Assign, KHÔNG gồm màn báo cáo):
- Phân cách **hàng nghìn = ","**
- Phân cách **thập phân = "."**
(kiểu en-US; hiện đang dùng vi-VN: nghìn="." thập phân=",").

## Phạm vi (chốt với user)
- **Màn**: Báo giá (tạo/sửa/xem/in/list + submit modal), BOM (builder editor/table), tab báo giá dự án TKT, cấu hình duyệt giá báo giá. **KHÔNG** đụng màn Báo cáo (report).
- **Cả ô NHẬP tiền** (V2BaseCurrencyInput) — gõ số cũng theo `,` nghìn / `.` thập phân (nhất quán hiển thị ↔ nhập).

## Quyết định
| Vấn đề | Quyết định |
|---|---|
| Hiển thị | `Intl.NumberFormat`/`toLocaleString` đổi locale `'vi-VN'` → `'en-US'` (chỉ dòng format SỐ, giữ nguyên `toLocaleDateString('vi-VN')`) |
| Ô nhập | Sửa `V2BaseCurrencyInput` (chỉ dùng trong Assign): format thousands `,`, decimal `.`; parse bỏ `,`, giữ `.` |
| product-project | Không đổi (hiển thị raw, không format locale) |
| Excel export | Không đổi (summary đã dùng `,` nghìn; line-item raw) |
| BE | `QuotationService::fmtNum` (log đổi giá) `.`→`,` nghìn cho đồng bộ |
| Công thức | Giữ nguyên — chỉ đổi dấu phân cách hiển thị |

## File đụng
- FE hiển thị (9 dòng): `quotations/index.vue`, `quotations/_id/edit.vue`, `quotations/_id/index.vue`, `components/assign/quotation/QuotationPrintPreview.vue`, `QuotationSubmitModal.vue`, `bom-list/components/BomBuilderEditor.vue`, `BomBuilderTableCard.vue`, `prospective-projects/components/ProspectiveProjectQuotationsTab.vue`, `settings/price-approval/index.vue`.
- FE input: `components/V2BaseCurrencyInput.vue` (Assign-only).
- BE: `Modules/Assign/Services/QuotationService.php` (fmtNum).
- Không migration/permission.
