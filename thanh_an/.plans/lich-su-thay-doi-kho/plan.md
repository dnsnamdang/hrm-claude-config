# Lịch sử thay đổi — phân hệ Kho — Plan

> Người phụ trách: @khoipv · Bắt đầu: 26/11/2026
> Design: [design.md](design.md) · Spec: [docs/superpowers/specs/2026-11-26-lich-su-thay-doi-kho-design.md](../../docs/superpowers/specs/2026-11-26-lich-su-thay-doi-kho-design.md)

## Chốt với user (26/11/2026)
- Phạm vi: **Phiếu nhập kho + Phiếu đề nghị xuất kho + danh mục Kho + danh mục Kho kế toán**
- Component: **port SystemInfoSection / SystemInfoValue / popup lịch sử từ hrm vào `hrm-thanhan-client/components/` (dùng chung, component MỚI)** + helper BE dựng DTO
- Trường track: **ghi đầy đủ hết như hrm** — mọi trường đầu phiếu, bảng con dạng khóa bảng (hàng hóa, lô/HSD, seri, file đính kèm) thêm / xóa / sửa
- Quyền xem: **ai vào được màn là xem được**, không thêm quyền
- 2 nơi: popup Lịch sử ở ⋮ màn danh sách + khối Lịch sử ở màn chi tiết / popup Xem (y hệt nhau)

## Phase 1 — Khảo sát
- [x] 1a. Đọc mẫu hrm: `SystemInfoSection.vue`, `SystemInfoValue.vue`, `CatalogHistoryModal.vue`, `CatalogHistoryService` (diff + khóa bảng)
- [x] 1b. Đọc luồng lưu dns: `WarehouseReceiptService` (create/update/send/recall/return/approve), service ĐNXK, service Kho, Kho kế toán
- [x] 1c. Viết spec chi tiết + design tóm tắt

## Phase 2 — BE
- [x] 2a. Migration: `old_value`/`new_value` cho `warehouse_receipt_logs`, `warehouse_export_request_logs`; bảng mới `catalog_histories` (index, không FK)
- [x] 2b. Engine dùng chung `app/CommonServices/EntityHistoryService.php` (port lõi hrm: diff, khóa bảng, DTO, filter-options, logCatalog/catalogLogs)
- [x] 2c. PNK: `historySnapshot()` + ghi diff ở save (update/send/approve), recall, return
- [x] 2d. ĐNXK: tách `displayProducts()` từ `detail()`, `historySnapshot()` + ghi diff ở save/send, recall, return
- [x] 2e. Kho vật lý / Kho kế toán: snapshot + log create/update ở `updateOrCreate`, lock/unlock ở toggleStatus
- [x] 2f. `WarehouseHistoryService` + `WarehouseHistoryController` + route `histories/{type}/{id}` và `/filter-options`
- [x] 2g. Verify bằng script PHP (transaction + rollback): sửa từng trường / thêm-bớt dòng / gửi / trả lại → đọc DTO

## Phase 3 — FE
- [x] 3a. Port `components/history/SystemInfoSection.vue`, `SystemInfoValue.vue`, `EntityHistoryModal.vue`
  - `endpointBase` mặc định `warehouse/histories`; `params` ghép query string (store dns chỉ nhận URL chuỗi)
  - Thêm method `refresh()` — màn cha gọi sau thao tác sinh log
- [x] 3b. PNK `ReceiptForm.vue`: thay `.rc-timeline` bằng khối Lịch sử (thu gọn mặc định, `applyDetail` gọi refresh); bỏ LOG_ICONS/logIcon/logsDesc + CSS cũ
- [x] 3c. ĐNXK `ExportRequestDetail.vue`: tab Lịch sử dùng khối Lịch sử (`v-if` theo tab, hide-header + mở sẵn); bỏ `.er-timeline`/`.er-empty`
- [x] 3d. ⋮ "Lịch sử" ở 4 danh sách — `EntityHistoryModal` id riêng từng màn; tiêu đề "Lịch sử: <số phiếu>" (danh mục chỉ "<tên>" — theo chuẩn hrm, sửa 26/11/2026)
- [x] 3e. Popup Xem Kho / Kho kế toán: khối Lịch sử cuối body (`v-if="isView && recordId"`)
- [x] 3f. e2e `pnk-gui-nhap-thong-tin.js`: helper `readHistory()` mở khối rồi đọc `.si-body` (không tự chạy)
- [x] 3g. Kiểm cú pháp: vue-template-compiler + babel parse 11 file OK; 5 trang dev :3001 trả 200 không lỗi build

## Phase 4 — Skill
- [x] 4a. Tạo skill `.claude/skills/entity-history/SKILL.md` bản dns (port từ hrm `entity-history`, theo code thật: `EntityHistoryService`, bảng log riêng + `catalog_histories`, `components/history/*`) (user hỏi 26/11/2026)
- [x] 4b. Sửa các dòng "dns không có SystemInfoSection / CatalogHistoryModal / audit log" ở skill `modal-popup`, `button-convention`, `catalog-popup`, `list-page` → trỏ sang `entity-history`

### Checkpoint — 2026-11-26
Vừa hoàn thành: Phase 3 FE (3a–3g)
Đang làm dở: —
Bước tiếp theo: user test tay trên trình duyệt (PNK / ĐNXK chi tiết, ⋮ Lịch sử 4 danh sách, popup Xem Kho / Kho kế toán)
Blocked:

### Checkpoint — 2026-11-26 (skill)
Vừa hoàn thành: Phase 4 — skill `entity-history` bản dns + sửa 4 skill liên quan; tiêu đề popup lịch sử danh mục đổi sang chỉ tên
Đang làm dở: —
Bước tiếp theo: user test tay; đẩy thay đổi skill qua PR repo `hrm-claude-config` (tài sản chung)
Blocked:
