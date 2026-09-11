# Plan — Chuẩn hoá màn "Báo giá chờ duyệt" theo skill `list-page`

Người phụ trách: @khoipv · Nhánh: `gop_db`
Spec chi tiết: `docs/superpowers/specs/gop-db/2026-09-08-quotation-pending-approval-list-page-standard-design.md`

## Phase 1 — Backend (`hrm-api`)

- [x] 1.1 `QUOTATION_SORTABLE_COLUMNS` bổ sung 4 khoá đang bị bỏ sót: `submitted_at` (khoá sắp xếp
      MẶC ĐỊNH của màn này), `customer_name`, `price_approval_level`, `status`
- [x] 1.2 `QuotationResource::submitted_at` format `d/m/Y H:i` ở BE (đang trả chuỗi ISO thô, buộc
      FE tự nhập `dayjs` format lại)
- [x] 1.3 `QuotationController::pendingApprovalExport()` + route
      `assign/quotations/pending-approval/export` (đặt cạnh route `/pending-approval`, TRƯỚC `/{id}`),
      dùng `DynamicExport` + registry `quotations`, nhận `fields=`

## Phase 2 — Frontend (`pages/assign/quotations/pending-approval/index.vue`)

- [x] 2.1 Bộ lọc: `V2BaseFilterPanel` → `V2BaseSmartFilterPanel` (6 mục, bỏ `title`/`subtitle`)
- [x] 2.2 Thêm các ô lọc máy chủ đã nhận mà FE chưa bày: **Công ty · Phòng ban · Bộ phận · Người
      lập báo giá** (1 nhóm `org`, 4 ô) · Giai đoạn dự án · Ngày tạo từ/đến — tổng **6 mục**.
      Ô **Khách hàng KHÔNG bày**: cần select2-remote (bảng 42k khách hàng), mà ô tìm nhanh đã
      tìm theo `customer_name` sẵn
- [x] 2.3 Tách cột gộp "Mã BG • BOM" → `quotationCode` (`nuxt-link`, sticky + locked) + `bomInfo`
      (ghép "MÃ - Tên" 1 dòng); gỡ nút "Xem và duyệt" khỏi ô đó
- [x] 2.4 Cột `actions` **cuối bảng** + `V2BaseRowActions`: **Duyệt** (điều hướng) + **Lịch sử phê
      duyệt** (dùng lại `QuotationHistoryModal`); bỏ "Xem"
- [x] 2.5 Cấp duyệt: `V2BaseBadge :color="item.approval_level_color"` — bỏ 2 class tự chế
      `.badge-level-2` / `.badge-level-3` (nền đậm chữ trắng, mã màu cứng)
- [x] 2.6 Bật `fixed-layout` + khai `width` = `minWidth` cho đủ **17 cột**; thêm 9 cột theo màn
      `/assign/quotations` (Loại báo giá · Giai đoạn · Tiền tệ · Tổng giá trị · Ngày tạo ·
      Người/Ngày cập nhật…)
- [x] 2.7 `columnCustomizationMixin` (`columnScreenKey: 'quotations_pending_approval'`) thay
      `getFields`/`updateColumns`/`defaultTableColumns` viết tay
- [x] 2.8 `exportFieldsMixin` + `ExportFieldsModal` + `runExport()` — màn này trước KHÔNG có xuất file
- [x] 2.9 `ignoredFields` thành computed dùng `textFilterKeys`; `handleReset` không gọi 2 lượt;
      `loadSeq` chống response về trễ; `$safeLoadingStart/Finish`
- [x] 2.10 Thứ tự request: `fetchData()` bắn TRƯỚC (trước đây `await Promise.all([...])` chặn 2
      request không liên quan); options bộ lọc + cấu hình cột nạp nền
- [x] 2.11 Bỏ `'N/A'` / `font-weight-bold` / `V2BaseTitleSubInfo` / `V2BaseCodeTitle`; ô dữ liệu
      dùng `field-line text-dark font-weight-normal`
- [x] 2.12 Bỏ `head()` nạp lại CSS remixicon từ CDN (dự án đã có sẵn) và bỏ `dayjs` (BE format)

## Phase 3 — Kiểm chứng

- [x] 3.1 Compile SFC (`vue-template-compiler` + babel)
- [x] 3.2 Đối chiếu tự động: 17 cột đủ `width` = `minWidth` + có slot render; `exportFields` FE ↔
      registry BE khớp; 0 chỗ `'N/A'` / `font-weight-bold` / `javascript:void(0)` / `field-line` trần
- [x] 3.3 Smoke test API trên **dữ liệu thật** (13 báo giá trong hàng chờ của tài khoản test):
      danh sách · 5 khoá sort mới sinh đúng `ORDER BY` + key lạ về mặc định · lọc cấp duyệt (4 + 9)
      / dự án / tìm nhanh · `submitted_at` đã format `24/07/2026 11:03` · export `fields=`
- [ ] 3.4 User tự mở trình duyệt kiểm tra (theo memory: không tự test Playwright)

## Ngoài phạm vi

- Màn chi tiết `/assign/quotations/{id}` (nơi thực sự bấm Duyệt / Từ chối) — giữ nguyên.
- `QuotationService::getPendingApproval()` phần gate quyền TP / BGĐ — giữ nguyên.
- 2 cột "Người duyệt" / "Ngày duyệt": **đã bỏ** sau khi đo trên đúng truy vấn của màn (0/13 dòng
  có dữ liệu) — xem mục "Điểm đáng nhớ" của design.md.

### Checkpoint — 2026-09-08
Vừa hoàn thành: Phase 1 (3 việc BE) + Phase 2 (12 việc FE) + 3.1 → 3.3.
Đang làm dở: không có.
Bước tiếp theo: user mở trình duyệt kiểm tra `/assign/quotations/pending-approval` (task 3.4).
Blocked: không — DB dev có 13 báo giá trong hàng chờ duyệt của tài khoản test.
