# Plan — Chuẩn hoá màn Danh sách hợp đồng theo skill `list-page`

Người phụ trách: @khoipv · Nhánh: `gop_db`
Spec chi tiết: `docs/superpowers/specs/gop-db/2026-09-07-contract-list-page-standard-design.md`

## Phase 1 — Backend (`hrm-api`)

- [x] 1.1 `Contract::getStatusList()` — **10/10 mã màu** cũ nằm ngoài bảng chuẩn, quy về đúng nhóm
      của bảng 9 mã màu (nhiều trạng thái cùng nhóm thì dùng chung 1 mã — đúng chủ ý bảng chuẩn)
- [x] 1.2 `Contract` — thêm quan hệ `updater()` + 3 hàm điều kiện thao tác
      (`isEditableStatus` / `isApprovableStatus` / `isLiquidatableStatus`); xoá dùng lại accessor
      `is_can_delete` đã có, KHÔNG khai hàm thứ hai cùng nghĩa
- [x] 1.3 `ContractResource` — 4 cờ `is_can_edit` / `is_can_delete` / `is_can_approve` /
      `is_can_liquidate` = **quyền AND trạng thái**; quyền hỏi đúng 1 lần cho cả trang (static cache)
      thay vì 4 truy vấn mỗi dòng
- [x] 1.4 `ContractResource` — `updater_name`, `updated_at`, và 3 ngày dạng chữ
      (`sign_date_text` / `effective_date_text` / `expiry_date_text`, `d/m/Y`)
- [x] 1.5 `ContractController` — tách `buildListQuery()` dùng chung index/export; whitelist sắp xếp
      nhận thêm khoá `*_text` của FE; **chốt `id desc`** ở cuối (trước chỉ `orderBy` 1 cột)
- [x] 1.6 `ExportColumnRegistry::COLUMNS['contracts']` — 13 cột
- [x] 1.7 Route + `export()` mới (`DynamicExport` + `resolve()`), đặt TRƯỚC route `/{id}`

## Phase 2 — Frontend (`pages/assign/contracts/index.vue`)

- [x] 2.1 Bộ lọc: `V2BaseFilterPanel` → `V2BaseSmartFilterPanel`; nhóm Công ty/Phòng ban/Bộ phận/
      Người lập khai thành MỘT field `org` (4 ô, `resetKeys` đủ 4 khoá) đúng quy tắc gom nhóm
- [x] 2.2 Bộ lọc trạng thái liệt kê **đủ 10 trạng thái** (bản cũ chỉ 4 → không lọc được các bước
      xuất hàng / quyết toán dù dữ liệu thật có đủ)
- [x] 2.3 `ignoredFields` thành computed dùng `textFilterKeys()`
- [x] 2.4 Mã hợp đồng → `nuxt-link` (`.v2-cell-link`), bỏ icon "Xem chi tiết" nhét cạnh mã
- [x] 2.5 Cột `actions` cuối bảng + `V2BaseRowActions`: Sửa · Xóa · Duyệt · Thanh lý; "Duyệt" và
      "Thanh lý" khai `to` (điều hướng chi tiết), "Không duyệt" KHÔNG đưa vào danh sách
- [x] 2.6 Thêm 5 cột: Ngày hết hiệu lực · Giá trị phát sinh · Người tạo · Ngày tạo · Người/Ngày cập nhật
- [x] 2.7 Bật `fixed-layout` + khai `width` = `minWidth` cho ĐỦ 15 cột theo 4 bậc
- [x] 2.8 `columnCustomizationMixin` (`columnScreenKey: 'contracts'`) — màn này **chưa từng có**
      cấu hình cột hiển thị
- [x] 2.9 **Thêm nút Xuất Excel** + `exportFieldsMixin` + `ExportFieldsModal` + `runExport()`
- [x] 2.10 `created()`: `fetchData()` bắn đầu tiên; thêm `loadSeq`; khôi phục bộ lọc trước khi gọi;
      `handleReset` không còn gọi API 2 lần (bản cũ vừa để watcher bắn vừa tự gọi)
- [x] 2.11 Bỏ `'—'` trong ô + trong `formatDate`/`formatMoney`; bỏ `font-weight-bold`; màu chữ theo
      màn mẫu `/assign/customers` (`field-line text-dark font-weight-normal`)

## Phase 3 — Kiểm chứng

- [x] 3.1 Compile SFC — OK
- [x] 3.2 Đối chiếu tự động: 15/15 cột đủ `width`+`minWidth`, có slot, map được sang cột xuất file;
      `exportFields` FE ↔ registry BE **13 = 13, cùng thứ tự**
- [x] 3.3 Smoke test API trên **42 hợp đồng thật**: index 200 (47 query/10 dòng), trả đủ trường mới;
      4 khoá sort đổi đúng thứ tự + key lạ rơi về mặc định; lọc `status=6` ra 6 dòng;
      export 200 → file .xlsx **49 dòng = 42 dữ liệu + 7 dòng khung**; `fields=` lọc đúng, key lạ bị loại
- [x] 3.4 Kiểm cờ thao tác theo TỪNG trạng thái (giả lập có đủ 4 quyền để tách riêng phần điều kiện
      trạng thái): Đang tạo → sửa + xoá · Chờ duyệt → sửa + duyệt · Có hiệu lực → thanh lý · còn
      lại không nút nào. Với tài khoản thật không có 4 quyền đó → **tất cả false (fail-closed)**
- [x] 3.5 Đối chiếu điều kiện hiện nút giữa danh sách và màn chi tiết (skill mục 7.2) — khớp nhau
- [ ] 3.6 User tự mở trình duyệt kiểm tra (theo memory: không tự test Playwright)

## Ngoài phạm vi

- Hành động **"Lịch sử"** — module Assign chưa có `LogsCatalogHistory` (hợp đồng có bảng
  `contract_histories` riêng, đang dùng ở màn chi tiết).
- Màn chi tiết `_id/index.vue` vẫn tự dựng khối nút thay vì `V2Footer` (skill mục 7.2) — điều kiện
  hiện nút đã khớp danh sách nên đợt này không dựng lại.

### Checkpoint — 2026-09-07
Vừa hoàn thành: Phase 1 (7 việc BE) + Phase 2 (11 việc FE) + 3.1→3.5.
Đang làm dở: không có.
Bước tiếp theo: user mở trình duyệt kiểm tra `/assign/contracts` (task 3.6).
Blocked: không.
