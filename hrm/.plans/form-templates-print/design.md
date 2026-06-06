# In mẫu phiếu (bản trống) — assign/form-templates

> Người phụ trách: @khoipv
> Ngày brainstorm: 2026-06-06
> Loại: Feature nhỏ — thuần Frontend (hrm-client)

## 1. Mục tiêu

Bổ sung chức năng **in mẫu phiếu thu thập thông tin ở dạng bản trống** từ màn quản lý mẫu phiếu `assign/form-templates`. Người dùng in ra phiếu giấy để đi khảo sát và điền tay tại hiện trường.

Nút "In mẫu phiếu" xuất hiện ở **2 nơi**:

- Màn **danh sách** (`pages/assign/form-templates/index.vue`): row action trên từng dòng, đặt **cạnh nút "Sửa"**.
- Màn **xem chi tiết** (`pages/assign/form-templates/_id/index.vue`): button trong màn xem.

## 2. Scope & quyết định lớn

- **Thuần FE.** Không sửa Backend, không thêm permission, không migration. Tái dùng API có sẵn `GET assign/form-templates/{id}` (đã trả `sections/groups/questions`).
- **Tạo component IN riêng** `hrm-client/components/FormTemplatePrintSheet.vue` — copy layout từ `SurveyPrintSheet.vue`, **KHÔNG sửa** component dùng chung `SurveyPrintSheet.vue`.
- **Cơ chế in:** modal preview chứa `FormTemplatePrintSheet` + nút "In" → `window.open()` + `window.print()` (tái dùng pattern `formTabInput.printModalPDF`). Component tự cung cấp `getPrintStyles()` (A4, Times New Roman) và `$refs.printArea`.

## 3. Layout phiếu in (bản trống)

### Tiêu đề
**THÔNG TIN KHẢO SÁT** (giữ nguyên như SurveyPrintSheet)

### Header thông tin (thứ tự + nguồn giá trị)

| # | Trường | Giá trị khi in |
|---|--------|----------------|
| 1 | Tên khách hàng | *(trống)* |
| 2 | Tên dự án | *(trống)* |
| 3 | Mã dự án | *(trống)* |
| 4 | Phân loại | *(trống)* |
| 5 | Nhóm ngành | **điền từ mẫu phiếu** (`scope_name`) |
| 6 | Nhóm giải pháp | **điền từ mẫu phiếu** (`industry_name`) |
| 7 | **Ngày khảo sát** *(MỚI)* | *(trống)* |
| 8 | Người khảo sát | *(trống)* |

**Bỏ so với SurveyPrintSheet:** Giai đoạn dự án, Ứng dụng, Địa chỉ dự án.

### Bảng "Nội dung khảo sát"

- 3 cột:
  1. **STT**
  2. **NỘI DUNG**
  3. **Đáp án/giá trị thu thập cho tôi** *(đổi tên từ "Thông tin thu thập")*
- Cột đáp án (cột 3): **để trống hoàn toàn** ở MỌI dòng (section / group / question / child question). Không placeholder, không checkbox, không dòng kẻ — chỉ là ô trắng để viết tay.
- Quy ước đánh số giữ nguyên: Section = A, B, C… / Group = I, II, III… / Question = 1, 2, 3… / Child = 1.1, 1.2…
- Câu hỏi required vẫn hiển thị dấu `(*)` ở cột NỘI DUNG.

## 4. Luồng dữ liệu

### Màn chi tiết
Data `sections` đã có sẵn (load qua `GET assign/form-templates/{id}` trong `_id/index.vue`). Bấm "In mẫu phiếu" → mở modal preview ngay với data hiện có.

### Màn danh sách
Row chỉ có metadata, **chưa có `sections`**. Bấm "In mẫu phiếu" → gọi `GET assign/form-templates/{id}` lấy đầy đủ `sections` → mở modal preview.

## 5. Phạm vi hiển thị nút

- Row action "In mẫu phiếu" hiển thị cho **mọi trạng thái** mẫu phiếu (Nháp / Hoạt động / Khoá) — vì in được áp dụng với mọi mẫu. Vị trí: ngay cạnh "Sửa mẫu".
- Màn chi tiết: button luôn hiển thị.

## 6. Files dự kiến

| File | Loại | Mô tả |
|------|------|-------|
| `hrm-client/components/FormTemplatePrintSheet.vue` | MỚI | Component render phiếu in bản trống (header + bảng 3 cột) + `getPrintStyles()` |
| `hrm-client/pages/assign/form-templates/index.vue` | SỬA | Thêm row action "In mẫu phiếu" + modal preview + fetch detail + hàm in |
| `hrm-client/pages/assign/form-templates/_id/index.vue` | SỬA | Thêm button "In mẫu phiếu" + modal preview + hàm in |

## 7. Edge cases

- Mẫu phiếu chưa có section/câu hỏi → in ra phiếu chỉ có header + bảng rỗng (header bảng vẫn hiển thị).
- Câu hỏi type=parent có children → in lồng cấp 1.1, 1.2 như SurveyPrintSheet.
- Section chứa group vs section chứa question trực tiếp → xử lý cả 2 nhánh (mutually exclusive).

## 8. Không làm (YAGNI)

- Không sửa `SurveyPrintSheet.vue` dùng chung.
- Không thêm endpoint/permission/migration.
- Không xuất PDF qua BE — chỉ in qua trình duyệt.
- Không in hàng loạt nhiều mẫu cùng lúc.
