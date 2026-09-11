# Plan — Chuẩn hoá màn Danh sách yêu cầu xây dựng giá theo skill `list-page`

Người phụ trách: @khoipv · Nhánh: `gop_db`
Spec chi tiết: `docs/superpowers/specs/gop-db/2026-09-07-pricing-request-list-page-standard-design.md`

## Phase 1 — Backend (`hrm-api`)

- [x] 1.1 `PricingRequestController` — whitelist `SORTABLE_COLUMNS` (10 khoá, nhận cả dạng
      `*_text` FE dùng) + `applySort()` chốt `id desc` (trước là `orderBy($request->sort_field)` trần)
- [x] 1.2 Tách `buildListQuery()` dùng CHUNG cho `index()` và `export()` — file xuất không bao giờ
      lệch phạm vi quyền / bộ lọc với thứ người dùng đang nhìn
- [x] 1.3 Tìm nhanh thêm **Người yêu cầu** (`orWhereHas('creator.info')`, dùng EXISTS chứ không join
      để không phình câu COUNT)
- [x] 1.4 `PricingRequest::getStatusList()` — 6 mã màu quy về **bảng 9 mã chuẩn**
      (`#9E9E9E` → `#64748B` · `#FF9800` → `#D97706` · `#03A9F4` → `#2563EB` · `#009688` → `#16A34A` ·
      `#EF4444` → `#DC2626`); thêm quan hệ `updater()` + hàm `isDraftOwnedByCurrentUser()`
- [x] 1.5 `PricingRequestResource` — khoá PHẲNG cho bảng + file (`bom_code`, `bom_name`,
      `project_code`, `project_name`, `customer_name`, `quotation_code`), `updater_name`,
      ngày `d/m/Y H:i` + `deadline_text` `d/m/Y`, cờ `is_can_edit` / `is_can_delete`
- [x] 1.6 `DetailPricingRequestResource` — thêm `is_can_edit` / `is_can_delete` (cùng nguồn)
- [x] 1.7 `ExportColumnRegistry::COLUMNS['pricing_requests']` — 20 cột
- [x] 1.8 Route + `export()` mới (`DynamicExport` + `resolve()`), đặt TRƯỚC route `/{id}` để không
      bị nuốt thành id

## Phase 2 — Frontend danh sách (`pages/assign/pricing-requests/index.vue`)

- [x] 2.1 Bộ lọc: `V2BaseFilterPanel` → `V2BaseSmartFilterPanel` + schema 5 ô (2 ô select remote
      render bằng slot), bỏ `title`/`subtitle`, placeholder "Chọn <trường>"
- [x] 2.2 `ignoredFields` thành computed dùng `textFilterKeys()`
- [x] 2.3 Mã YCBG → `nuxt-link` vào màn chi tiết (`.v2-cell-link`), bỏ popup chi tiết khỏi màn này
- [x] 2.4 Cột `actions` cuối bảng + `V2BaseRowActions` (Sửa · Xóa · Tạo báo giá), gỡ dãy icon
      nhét dưới Mã YCBG; bỏ hành động "Xem"
- [x] 2.5 **Thêm hành động Xóa** (endpoint `DELETE` đã có sẵn, FE chưa từng gọi) + popup xác nhận
- [x] 2.6 Thêm cột Ngày tạo · Người cập nhật · Ngày cập nhật; ô ghép `MÃ - Tên` cho BOM list và Dự án
- [x] 2.7 Bật `fixed-layout` + khai `width` = `minWidth` cho ĐỦ 16 cột theo 4 bậc
- [x] 2.8 `columnCustomizationMixin` (`columnScreenKey: 'pricing_requests'`) thay logic merge tự viết
      (bản cũ trả thẳng `columnFields` đã lưu → mất hết `width` / `align` / `sortable` khai trong code)
- [x] 2.9 **Thêm nút Xuất Excel** + `exportFieldsMixin` + `ExportFieldsModal` + `runExport()`
- [x] 2.10 `created()`: `fetchData()` bắn đầu tiên; thêm `loadSeq`; khôi phục bộ lọc trước khi gọi;
      watcher reset trang 1; `handleSort` chỉ đổi `filters`
- [x] 2.11 Màu chữ trong ô theo màn mẫu `/assign/customers`
      (`field-line text-dark font-weight-normal`)

## Phase 3 — Sửa 3 lỗi CÓ SẴN (chức năng chết)

- [x] 3.1 `handleReset()` gọi `this.loadData()` — hàm không tồn tại → bấm "Làm mới" ném TypeError,
      ô lọc bị xoá nhưng danh sách giữ nguyên kết quả cũ
- [x] 3.2 Nút "Sửa nháp" ở danh sách không bao giờ hiện: FE so `item.created_by` mà Resource
      không trả khoá đó → `Number(undefined)` = NaN. Nay đọc cờ `is_can_edit` của máy chủ
- [x] 3.3 Màn **Sửa** (`_id/edit.vue`) khoá toàn bộ form + báo "Yêu cầu đã gửi, không thể sửa" với
      MỌI phiếu: `$store.state.auth?.user?.id` không tồn tại (module `auth` chỉ có `currentUser`).
      Màn **chi tiết** (`_id/index.vue`) cùng lỗi → nút Sửa không hiện. Nay cả 2 đọc `is_can_edit`
- [x] 3.4 Màn chi tiết thêm nút **Xóa** cho khớp hành động ngoài danh sách (skill mục 7.2), xong
      điều hướng về danh sách (mục 7.3)
- [x] 3.5 Màn chi tiết + màn sửa: bỏ `'—'` ở ô rỗng (mục 3b-3) và bỏ `.text-muted` (class này ra
      màu ĐỎ, mục 3b-2) → dùng `.v2-hint` xám #6b7280

## Phase 4 — Kiểm chứng

- [x] 4.1 Compile SFC 3 file — OK
- [x] 4.2 Đối chiếu tự động: 16/16 cột đủ `width`+`minWidth`, có slot, map được sang cột xuất file;
      `exportFields` FE ↔ registry BE **20 = 20, cùng thứ tự**
- [x] 4.3 Smoke test API trên DỮ LIỆU THẬT tạo trong transaction rồi rollback (bảng
      `pricing_requests` đang rỗng): index 200 · 5 khoá sort đổi đúng thứ tự, key lạ rơi về mặc định ·
      tìm nhanh theo mã và theo tên người yêu cầu đều ra đúng · export ra .xlsx thật (kể cả khi
      0 dòng) · `fields=` lọc đúng, key lạ bị loại. **Sau rollback bảng về 0 dòng.**
- [x] 4.4 Kiểm cờ quyền 3 chiều: phiếu nháp của mình → `is_can_edit = true`; phiếu đã gửi → `false`;
      phiếu nháp của người khác → `false` (fail-closed)
- [ ] 4.5 User tự mở trình duyệt kiểm tra (theo memory: không tự test Playwright)

## ⚠️ Chờ user quyết (chưa sửa)

Người có quyền **"Xây dựng giá bán theo công ty/phòng"** KHÔNG thấy phiếu nháp của chính mình:
nhánh phạm vi ở `index()` thay hẳn điều kiện "của tôi" bằng `whereIn('status', [2..6])`, mà nháp là
status 1. Sửa chỉ cần thêm `orWhere('created_by', auth()->id())` vào nhóm ngoài — nhưng đó là **đổi
phạm vi dữ liệu người dùng nhìn thấy**, không tự quyết.

## Ngoài phạm vi

- Hành động **"Lịch sử"** — module Assign chưa có `LogsCatalogHistory`.
- Màn chi tiết `_id/index.vue` vẫn tự dựng khối nút thay vì `V2Footer` (skill mục 7.2) — đợt này
  chỉ sửa cờ điều kiện + thêm nút Xóa cho khớp danh sách, chưa dựng lại theo `V2Footer`.

### Checkpoint — 2026-09-07
Vừa hoàn thành: Phase 1 (8 việc BE) + Phase 2 (11 việc FE) + Phase 3 (5 lỗi có sẵn) + 4.1→4.4.
Đang làm dở: không có.
Bước tiếp theo: user mở trình duyệt kiểm tra `/assign/pricing-requests` (task 4.5) và quyết việc
phạm vi phiếu nháp của người có quyền xây dựng giá.
Blocked: không.
