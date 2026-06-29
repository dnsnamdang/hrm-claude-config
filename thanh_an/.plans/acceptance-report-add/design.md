# Design (tóm tắt) — Màn thêm mới Biên bản nghiệm thu

**Phụ trách:** @khoipv
**Spec đầy đủ:** `docs/superpowers/specs/2026-06-16-acceptance-report-add-design.md`

## Mục tiêu
Dựng `pages/contract/acceptance_report/add.vue` — wizard 3 bước, hỗ trợ **5 loại nghiệm thu**,
validate SL & giá trị theo hạn mức HĐ. Tách nhiều component con.

## Quyết định lớn
- Làm đủ **5 loại** (thang / tonghd / cthd / mathang / luyke).
- UI **lai**: layout demo + base component dự án.
- API thật: `category/contracts` (list) + `category/contracts/{id}` (hàng hóa). Lũy kế **tạm = 0**,
  nút Lưu **build payload + stub**.

## Cấu trúc component
add.vue (container) → Step1SelectContract + ContractSummary → Step2Config → Step3Detail
(switch 5 form trong `components/forms/`) + AcceptanceFooter + GoodsPickerModal; logic chung ở `helpers.js`.

## Không làm lần này
Endpoint lưu thật, lũy kế thật, index/sửa/duyệt, Excel, xem trước bản in.
