# Plan — Biên bản bàn giao sơ bộ (ERP → HRM) — @khoipv

Spec: `docs/superpowers/specs/gop-db/2026-11-04-bien-ban-ban-giao-so-bo-design.md` · Tóm tắt: `design.md`

## Quyết định user chốt (04/11/2026)
- Quyền: **y ERP, không quyền** — ai đăng nhập cũng xem/tạo/sửa/xoá/duyệt mọi biên bản.
- Lỗi ERP: **sửa cả HRM lẫn ERP** — (1) Xoá chạy được (xoá cứng khi Đang tạo / Từ chối); (2) Duyệt / Từ chối
  chỉ khi Chờ duyệt; (3) popup phiếu xuất kho chỉ lấy phiếu cùng công ty người tạo.
- Menu: **cả 2 chỗ như ERP** — CSKH › Hồ sơ công việc + CSKH › Chăm sóc khách hàng › "Phiếu CSKH".
- **Có In danh sách + In biên bản** (mẫu HRM tự dựng; ERP không có).

## Phase 1 — BE (`Modules/CustomerCare`)
- [x] T1 Entity `HandoverRecord` + `HandoverRecordProduct` (bảng ERP sẵn có, không migration)
- [x] T2 `HandoverRecordService`: danh sách/lọc/sort, meta, chi tiết, edit-data, xoá, duyệt/từ chối, lịch sử, popup PXK + dữ liệu PXK
- [x] T3 `HandoverRecordStoreService` + `HandoverRecordRequest`: tạo/sửa, validate PXK (trạng thái, cùng KH, cùng cty), hàng lấy từ lô PXK
- [x] T4 `HandoverRecordPrintService`: in danh sách + in biên bản (letterhead công ty người tạo — bảng không có company_id)
- [x] T5 `HandoverRecordNotifier`: Gửi duyệt → người duyệt; Duyệt/Từ chối → người tạo; prefix `BBBGSB` vào `NotificationMeta::OBJECT_LABELS`
- [x] T6 Controller + route `/v1/customer-care/handover-records`; đăng ký `ExportColumnRegistry` + `CatalogHistoryService::TABLES`
- [x] T7 Verify: php -l + smoke test API trong transaction rollback

## Phase 2 — FE (`pages/customer-care/handover-records`)
- [x] T8 `index.vue` danh sách (lọc, sort, cấu hình cột, xuất, in, lịch sử)
- [x] T9 `HandoverRecordForm.vue` dùng chung Tạo/Sửa/Chi tiết + popup chọn PXK + bảng hàng; `create.vue`, `_id/edit.vue`, `_id/index.vue`
- [x] T10 Menu CSKH: Hồ sơ công việc + "Phiếu CSKH"
- [x] T11 Verify compile (vue-template-compiler + babel)

## Phase 3 — ERP (repo `D:\laragon\www\erp`, nhánh gop_db, không commit)
- [x] T12 Thêm `delete()` controller, chặn Duyệt/Từ chối ngoài Chờ duyệt (BE + blade show), popup PXK cùng công ty

## Phase 4 — Tài liệu
- [x] T13 design.md + spec đầy đủ, STATUS

### Checkpoint — 2026-11-04
Vừa hoàn thành: T1–T13. BE `php -l` sạch + smoke test API thật qua HTTP kernel (transaction rollback, notifier giả):
meta, popup PXK (lọc mã / cùng KH / loại đã chọn / khác cty → 422), validate (thiếu ô, khác KH, hàng lạ, PXK cty khác),
tạo `BBBGSB-0001`, danh sách, edit-data, Gửi duyệt thiếu file 422 / có file 200, sửa / xoá khi Chờ duyệt 409, duyệt
status lạ 400, Từ chối 200, Duyệt lần 2 409, chi tiết + cờ, in biên bản, in / xuất danh sách, lịch sử 4 mốc, xoá cứng
sạch 3 bảng, id lạ 404. FE compile (vue-template-compiler + babel) sạch, grep quy chuẩn sạch. ERP `php -l` sạch.
Đang làm dở: không
Bước tiếp theo: user bấm thử trình duyệt (danh sách → tạo chọn nhiều PXK → gửi duyệt có file PDF → duyệt/từ chối → sửa → xoá); bấm thử ERP sau khi vá.
Blocked:

## Phase 5 — Test Playwright local (04/11/2026, user yêu cầu)
- [x] T14 E2E trên `127.0.0.1:3000`, tài khoản DNS Admin (id 13), người duyệt = chính mình. Script: scratchpad `pw_bbbgsb/e2e.js` + `e2e2.js`.
  PASS: danh sách (cột, Thêm mới, bảng trống) · validate Lưu trống (2 ô đỏ cùng lúc) · popup PXK (tìm mã; lần 2 chỉ còn phiếu cùng KH, loại phiếu đã chọn) ·
  gộp SL 2 phiếu (8 + 10 = 18) · ô Khách hàng · Lưu và tiếp tục (form reset + toast) · Lưu → danh sách Đang tạo · Sửa nạp SL đã lưu · bỏ 1 phiếu dựng lại bảng ·
  Gửi duyệt thiếu file báo lỗi · upload PDF S3 · Gửi duyệt · chi tiết Chờ duyệt (Duyệt / Từ chối / In, không Sửa / Xóa) · In biên bản · Từ chối · chi tiết Từ chối (Sửa / Xóa) ·
  tìm nhanh + Làm mới · In danh sách · menu dòng + popup Lịch sử · Xóa từ danh sách · Tạo + Gửi duyệt ngay → Duyệt → Đã duyệt có Ngày duyệt · chi tiết Đã duyệt hết nút ghi ·
  link Sửa phiếu Đã duyệt → 404 · id lạ → 404 · khối Lịch sử chi tiết (mở ra) + popup danh sách đủ mốc · thông báo Chờ duyệt / Từ chối / Đã duyệt có sinh.
  Dọn theo id (3, 4, 5, 6): 6 bảng liên quan về 0. Còn để lại 3 file PDF test trên S3 folder `handover_record` (không xoá được qua app).
  Quan sát nhỏ (chưa sửa): ô Số lượng căn trái chữ (class `text-right` không ăn vào input bên trong); khối File đính kèm ở chế độ xem cột Dung lượng trống.

## Phase 6 — Bố cục form (04/11/2026, user yêu cầu)
- [x] T15 Người duyệt · Ngày tính bảo hành · Phiếu xuất kho lên cùng 1 dòng (`col-md-4` mỗi ô); màn Chi tiết dời Trạng thái + Ngày duyệt xuống dòng dưới.
  Verify: compile OK + Playwright chụp màn Tạo (chỉ mở, không lưu) — 3 ô cùng `top = 117px`.
- [x] T16 Popup chọn phiếu xuất kho bỏ cột Hành động (user yêu cầu 04/11/2026) → bấm vào DÒNG là chọn (khuôn `borrow-sell-requests/ContractPickerModal`);
  bắt click ở vỏ popup (`data-pick-id`), không sửa `V2BaseDataTable` dùng chung; mã phiếu vẫn là link tab mới (`.stop`, không chọn).
  Verify Playwright (không lưu): không còn cột/nút, con trỏ bàn tay, bấm mã → tab mới không chọn, bấm dòng → chọn + đóng popup + bảng hàng có dòng.
- [x] T17 Ô Khách hàng thu về `col-md-4` (user yêu cầu 04/11/2026); màn Chi tiết đổi Trạng thái / Ngày duyệt sang `col-md-4` để dòng 2 = Trạng thái · Ngày duyệt · Khách hàng. Verify compile OK.
- [x] T18 Commit + push develop (04/11/2026, user yêu cầu): hrm-api `4168dde79` (merge `51dd5e96e`), hrm-client `9c5e59719` (merge `7c906c1e7`).
  Chỉ commit file của màn này — các file `handover-acceptance-records` / `HandoverAcceptanceRecord*` đang sửa dở (feature BB nghiệm thu) để nguyên.
  Sau merge: php -l + smoke API (rollback) + compile FE pass. Repo ERP chưa commit (chờ user).
