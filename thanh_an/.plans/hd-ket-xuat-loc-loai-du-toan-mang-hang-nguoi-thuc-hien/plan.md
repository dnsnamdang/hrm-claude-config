# Plan — HĐ đã kết xuất: lọc Loại dự toán, Mảng hàng hóa, Người thực hiện HĐ

> @khoipv — Bắt đầu 27/10/2026
> Màn: `hrm-thanhan-client/pages/supply/contract_render/index.vue` · BE: `Modules/Supply/Services/RenderedContractService.php`

## Quyết định
- **Loại dự toán**: `projects.project_type` của dự toán gắn HĐ (`contracts.project_id`); HĐ lập từ gói thầu không có `project_id` → lấy `bid_packages.project_type` (cùng mã 1–3). 6 loại theo `Project::ProjectType` (Trong thầu · Ngoài thầu · Nhảy thầu · HĐ Cho/Tặng · HĐ Đặt/Mượn · HĐ Nguyên tắc). Chọn 1. Gói thầu để trống loại → HĐ không khớp loại nào.
- **Mảng hàng hóa**: bảng `contract_array_product_ids` (1 HĐ nhiều mảng) — HĐ có mảng đã chọn. Chọn 1, option lấy từ mảng của các HĐ đã kết xuất.
- **Người thực hiện HĐ**: `contracts.created_by` (người lập; bàn giao HĐ ghi đè trường này — cùng nghĩa "NV thực hiện HĐ" ở BC dự án). Chọn 1, option lấy từ người lập của các HĐ đã kết xuất.
- ~~Chỉ thêm bộ lọc, không thêm cột bảng / trường Excel.~~ → 27/10/2026 user yêu cầu thêm 3 cột, **mặc định chưa tick**; Excel có 3 trường tương ứng.

## Phase 1 — BE
- [x] `getList()`: tham số `project_type`, `array_product_id`, `creator_id` (1 giá trị)
- [x] `filterOptions()`: trả thêm `array_products`, `creators`

## Phase 2 — FE
- [x] `constants.js`: `PROJECT_TYPE_OPTIONS`
- [x] `index.vue`: 3 ô select chọn 1 trong `filterFields`, khai khoá ở `initialStateForm`, nạp option (kể cả khi bộ lọc đã lưu có giá trị)

## Phase 3 — Thêm 3 cột (mặc định ẩn)
- [x] BE `getList()`: `project_type_value` (hằng `PROJECT_TYPE_SQL` dùng chung với bộ lọc), `array_product_names` (GROUP_CONCAT), `creator_name` (subquery)
- [x] BE `RenderedContractResource`: `project_type`, `project_type_name`, `array_product_names`, `creator_name`
- [x] FE `allColumns`: 3 cột sau "Cty thực hiện", `isVisible: false` + slot hiển thị
- [x] FE `exportFields`: thêm 3 trường

## Phase 4 — Thu nhỏ cột
- [x] Mã HĐ 150px → 130px (mã dài nhất 11 ký tự + icon phụ lục), Cty thực hiện 130px → 110px (mã cty ≤ 4 ký tự)
- [x] User yêu cầu "nhỏ nhất có thể": Mã HĐ → 110px (chữ 12px + lề 8px×2 + icon PL 18px); Cty thực hiện → 100px (vừa đủ tiêu đề 1 dòng — user KHÔNG muốn tiêu đề xuống dòng, đã bỏ bản 75px + header 2 dòng)
- [x] Đổi tên cột "Cty thực hiện" → "Cty TH", thu về 65px (vừa tiêu đề + mã cty ≤ 4 ký tự). Ô lọc + trường Excel giữ tên "Cty thực hiện"

## Phase 5 — Icon thao tác
- [x] ~~"Lịch sử tiếp nhận" trùng icon `ri-history-line` với "Lịch sử kết xuất" → đổi icon~~ (đã thử `ri-user-received-line`, `ri-file-user-line`) → user chốt: trả lại `ri-history-line` cho "Lịch sử tiếp nhận"
- [x] Bỏ nút + popup "Lịch sử kết xuất" ở màn HĐ đã kết xuất: xoá action `render-history`, `openRenderHistory()`, `renderHistoryContractId`, xoá file `pages/supply/contract_render/components/RenderSupplyHistoryModal.vue`. Màn Hợp đồng (`pages/contract/contract`) vẫn giữ "Lịch sử kết xuất"; API `category/contracts/{id}/render-supply-history` giữ nguyên (màn Hợp đồng đang dùng)

### Checkpoint — 27/10/2026
Vừa hoàn thành: Phase 1 + 2 + 3 + 4
Đang làm dở:
Ghi chú: user yêu cầu đổi từ chọn nhiều → chọn 1 (27/10/2026)
Bước tiếp theo: user test trên trình duyệt (chọn từng ô → có request, kết quả đúng)
Blocked:
