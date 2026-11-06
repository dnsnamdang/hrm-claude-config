# Plan: Port "Hợp đồng bán đầu kỳ" ERP → HRM

**Spec:** `.plans/hd-ban-dau-ky/design.md`
**Worktree:** `HRM/.worktrees/hrm-api-hdbdk` + `HRM/.worktrees/hrm-client-hdbdk`, nhánh `feature/hd-ban-dau-ky`
**Khuôn HRM:** BE scope/quyền theo `Modules/Finance/Entities/BillProductivitySettlementQuarter` + trait `Entities/Concerns/ChecksEmployeePermission`; lịch sử theo `BillProductivitySettlementQuarterHistoryService`; FE danh sách/import/in/lịch sử theo `pages/finance/accounts/index.vue`, form theo khuôn `pages/assign/customers`.

## Trạng thái
- Bắt đầu: 2026-11-04 · Tiến độ: 4/4 — XONG, đã merge + push `develop` 05/11/2026 (hrm-api `1f0ad33e6`, hrm-client `fdbb5f5b5`); worktree hdbdk đã xoá

## Global constraints
- Ghi bảng ERP `opening_contracts` có sẵn, không migration. Chuỗi morph giữ `App\Model\Accounting\OpeningContract`.
- 4 quyền mới type 23 qua `$this->perm([...])` trong `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`, không `id`. Không chạy full `permission:sync`.
- Nhãn "Người tạo"/"Ngày tạo"; số en-US; ngày `dd/mm/yyyy`.
- FE: `V2Base*`, `V2Footer`, `unsavedChangesMixin`, "Lưu và tiếp tục", `CreatorInfoLine`, 4 mixin danh sách + `ColumnCustomizationModal`, filter `floating`, thao tác xong về danh sách, 404 → `/pages/extras/404`.

## Phase 1 — Backend
- [x] **T1 Entity + quyền + CRUD** — mở ghi entity; `OpeningContractService` (list/scope/show/store/update/destroy, canView/isCanEdit/isCanDelete theo design §2), FormRequest (unique trong công ty), Resource, Controller, routes, 4 quyền seeder. Feature test: scope 4 cấp + của mình, unique theo công ty, chặn sửa/xoá khi có khai báo/hạch toán, 404 khi !canView.
- [x] **T2 Import + Export + In + Lịch sử** — import (validate toàn bộ, lỗi → không ghi, câu ERP), `export-rows`, `print-data` (template 467), `OpeningContractHistoryService` + `CatalogHistoryService::TABLES`.

## Phase 2 — Frontend
- [x] **T3 Danh sách + form + chi tiết + menu** — `pages/sale/opening-contracts/{index,add,_id/index,_id/edit}.vue` + `components/OpeningContractForm.vue`; menu `sale-hub.js`; `utils/contract-link.js`.

## Phase 3 — Kiểm
- [x] **T4** Đối chiếu ERP + checklist skill, Playwright: danh sách/lọc → tạo → sửa → lịch sử → xuất/in → import → xoá; chặn sửa/xoá HĐ đã khai báo công nợ.

## Phase 4 — Bug Redmine 06/11/2026
- [x] **#12050 Danh sách**: ô tìm chỉ theo số hợp đồng (BE keyword chỉ `opening_contracts.code`), placeholder `Tìm theo số hợp đồng`, nút "Tạo mới", bỏ nút Xem ở cột Hành động.
- [x] **#12053 Tạo/Sửa**: tiêu đề `Thông tin chung`, placeholder `Nhập số hợp đồng`, Địa chỉ/SĐT luôn hiện (ô khoá), tự điền khi chọn khách qua `GET opening-contracts/customer-contact/{customerId}`. Cỡ chữ nhãn/ô đo đúng chuẩn 12px; "chỉnh size chữ" hiểu là tiêu đề in hoa.
- [x] **#12054 Lịch sử**: `components/assign/SystemInfoSection.vue` (DÙNG CHUNG, user chốt 06/11): khối Trước/Sau 2 cột, thẻ giãn hết chiều rộng, popup hẹp tự xuống hàng; dòng ngắn giữ bề rộng theo nội dung.
- [x] **#12055 Import**: file mẫu còn 3 cột (Số hợp đồng, Ngày ký, Mã khách hàng); báo lỗi riêng từng trường trống; bỏ so sánh tên/địa chỉ/SĐT.

## Checkpoint
- 2026-11-04: `vendor/bin/phpunit Modules/Finance/Tests/Feature/OpeningContractApiTest.php` → OK 9 tests / 64 assertions
  (chặn sửa/xoá khi đã khai báo công nợ / hạch toán được phủ bằng feature test).
- Playwright (API :8003 + client :3003 dựng riêng từ worktree, đã tắt): danh sách 2.228 dòng, mỗi lần vào màn / đổi trang / sort / tìm / Làm mới
  đều chỉ **1 request**; sort Ngày ký asc → desc; validate rỗng đỏ cả 3 ô; tạo (id 2673) → về danh sách; chi tiết
  (Sửa · Xóa · Quay lại = khớp dòng: Xem · Sửa · menu Xóa/Lịch sử); sửa → về danh sách; Lịch sử ghi Tạo mới + Thay đổi
  Ghi chú; Xuất Excel (modal chọn trường 7/8) tải file; In danh sách = popup xem trước khổ ngang; Import mở modal, tải
  file mẫu `Mau_import_hop_dong_ban_dau_ky.xlsx`; Xóa qua popup xác nhận → "Xóa thành công". Bản ghi test đã xoá.
- 2 lỗi FE tự phát hiện & đã sửa ở `index.vue`: (1) `:sortBy` truyền tên trường BE nên bấm lần 2 không bao giờ sang desc →
  computed `tableSortBy` map ngược `SORT_FIELD_MAP`; (2) response cũ về muộn đè `currentPage` → watcher bảng bắn thêm
  `page-change` (3 request/thao tác) → `loadSeq` chỉ nhận response mới nhất.
- 2026-11-06: `OpeningContractApiTest` → OK 12 tests / 77 assertions. Playwright 127.0.0.1:3000: #12050, #12053, #12055 (cột mẫu + map dòng; không import thật), #12054 (dữ liệu Lịch sử giả lập bằng route, 2 cột 359px cùng hàng, dòng ngắn không giãn).

- 2026-11-06: đã commit local trên develop, api `ecbb395c8` / client `5ee34182a`, chưa push.
