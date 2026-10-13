# Plan — Cột hành động màn "Danh sách đề nghị nhập kho"

Nhánh `gop_db` · @namdangit · Redmine "[ERP => HRM] Phiếu đề nghị nhập kho - Danh sách"

## Phase 1 — Cột hành động đầy đủ + gom menu (FE-only)

### FE — `hrm-client/pages/finance/warehouse-import-requests/index.vue`
- [x] Cột Mã phiếu → `nuxt-link` `class="v2-cell-link field-line"` trỏ `/finance/warehouse-import-requests/{id}`
- [x] Thay cột hành động bằng `<V2BaseRowActions :actions="getRowActions(item)" @action="handleRowAction">`
- [x] `getRowActions(item)`: Sửa · Tạo phiếu nhập kho · Từ chối(danger) · In · Hủy(danger), mỗi nút `visible` theo cờ BE
- [x] `handleRowAction`: edit→push edit · create_import→goCreateWarehouseImport (deep-link ERP) · deny→openDenyModal · print→printItem · cancel→openCancelModal
- [x] `goCreateWarehouseImport`: `window.open(${tp_url}/admin/warehouse/warehouse_imports/create?warehouse_import_request_id=${id})`, thiếu TP_URL → toast lỗi
- [x] Modal `base-confirm-modal` từ chối (textarea lý do bắt buộc, `@event=submitDeny`) + hủy (`@event=submitCancel`)
- [x] `ReportPrintPreviewModal` + `reportPrintPreviewMixin` cho nút In (`printItem` → `openPrintDetail`)
- [x] Dọn import cũ (`V2BaseIconButton`, `goDetail`, `confirmCancel` msgBoxConfirm), thêm component/mixin mới
- [x] Giữ LF (file gốc LF, 0 CR)

### BE
- [x] Không đổi — `WarehouseImportRequestResource` đã trả đủ 5 cờ (dùng chung list + detail)

### Verify
- [x] Playwright: bơm 4 mock row đủ tổ hợp cờ → xác nhận số nút inline, gom menu ⋮, nội dung menu (Từ chối/In/Hủy), Mã phiếu là link, nút danger
- [ ] Commit/push — **CHỜ user duyệt** (chưa được yêu cầu)

### Checkpoint — 2026-09-19
Vừa hoàn thành: FE cột hành động đầy đủ + gom menu ⋮ + Mã phiếu link + verify Playwright (mock, không đụng DB).
Đang làm dở: không.
Bước tiếp theo: chờ user duyệt commit/push.
Blocked:
