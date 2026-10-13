# Hạch toán mua dịch vụ — Plan

> @khoipv · nhánh `develop` (con `gop_db`, KHÔNG tạo nhánh, KHÔNG commit)
> Spec: `docs/superpowers/specs/gop-db/2026-10-12-buy-service-accounting-design.md`

## Phase 0 — Khảo sát + chốt
- [x] Khảo sát ERP controller/model/blade/JS class + DB gộp
- [x] Chốt với user: 3 cấp quyền · Sửa/Xoá như ERP · bút toán y ERP
- [x] Spec + design + plan

## Phase 1 — BE
- [x] Quyền 1703-1705 vào `PermissionsTableSeeder` + insert local (firstOrCreate, KHÔNG gán vai trò)
- [x] Entity `BuyServiceAccounting/{BuyServiceAccounting, Detail, DetailRequest}` (cờ quyền, searchByFilter, sort cột ảo Tổng thanh toán)
- [x] Helper dùng chung `Account::selfAndChildIds()` (port ERP `getAccountChild`); `buyServiceRequestInfo()` của service Yêu cầu đổi public để dùng lại
- [x] Service đọc + ghi + ghi sổ (`BuyServiceAccountingService`) — khoá phiếu yêu cầu, kiểm SL ≤ SL yêu cầu, bút toán y ERP, cộng accounted_qty / đơn bảo hiểm → 4
- [x] FormRequest + Controller + Route (`checkPermission:Hạch toán mua dịch vụ` cho ghi + nguồn form) + ExportColumnRegistry + mẫu in 430/431 + catalog_histories TABLES
- [x] Smoke test HTTP kernel (rollback): 42/42 mục — list/sort/keyword, show + 3 bút toán, 422 (thiếu ô, TK 642 thiếu mã phí, TK 154 thiếu vụ việc, vượt SL), nháp → yêu cầu 3, chặn phiếu thứ 2, duyệt → 3 bút toán cân + 4 ref + yêu cầu 4, 409 sửa/xoá phiếu đã duyệt, in/xuất/lịch sử, loại bảo hiểm nháp/xoá/duyệt
- [x] Test âm quyền (tiến trình riêng): emp 200 / 970 không quyền → list chỉ phiếu mình, show phiếu người khác 403, catalogs/store/delete 403

## Phase 2 — FE
- [x] `pages/finance/buy-service-accountings/` index · create · _id/edit · _id/index + Form + AccountingServiceTable + InsuranceAccountingTable + AccountingEntriesTable (dùng lại SourcePickerModal, InsuranceSection, AttachmentSection)
- [x] Màn Yêu cầu: nút "Hạch toán" → `/finance/buy-service-accountings/create?buy_service_accounting_request_id=`
- [x] Menu Bán hàng › Mua dịch vụ + Tài chính › Mua dịch vụ
- [x] Compile + grep checklist skill erp-to-hrm-screen

## Phase 3 — Test Playwright (user yêu cầu 12/10)
- [x] Danh sách: 48 phiếu, tìm nhanh, sort Tổng thanh toán, phân trang, số dòng/trang (sửa lỗi gọi API 2 lần), bộ lọc Trạng thái / Loại / Người tạo, Làm mới, Xuất Excel (popup chọn trường + file), In danh sách, Cấu hình cột, Lịch sử, 404
- [x] Tạo loại 2 từ URL nút Hạch toán: đổ đúng dữ liệu, validate inline (TK nợ, SL vượt, Mã phí khi TK 642), Lưu nháp, Sửa đơn giá, Lưu và duyệt + popup xác nhận → bút toán + trạng thái yêu cầu + accounted_qty + lịch sử 3 mốc + in phiếu
- [x] Loại 1: chọn qua popup, TK cố định, Lưu nháp, Xoá từ danh sách → yêu cầu về Chờ duyệt
- [x] Cảnh báo chưa lưu (sửa lỗi `markFormSaved()` lúc mở màn — áp cả form màn Yêu cầu), Lưu và tiếp tục
- [x] Dọn dữ liệu test về baseline (48 / 61 / 61, 149 bút toán, yêu cầu 39-45-67 = 2, accounted_qty 0, catalog_histories)
- [ ] Kiểm trên trình duyệt 4 sửa ở thư mục màn Yêu cầu (nút Hạch toán, InsuranceSection `showServiceTable`, cảnh báo chưa lưu, đổi số dòng) — dev server cổng 3000 không build lại file CŨ, cần khởi động lại `nuxt`

## Phase 4 — Chỉnh theo user (13/10)
- [x] Bỏ chú thích ⓘ ở Tài khoản nợ / Tài khoản có (loại bảo hiểm)
- [x] Lấy đúng như ERP: danh sách 12 cột ERP (bỏ Công ty / Phòng ban / Diễn giải, Người tạo trước Ngày tạo), bỏ ô lọc Người tạo, Excel 11 cột ERP, màn chi tiết bỏ ô Ngày hạch toán

### Checkpoint — 2026-10-12 17:10
Vừa hoàn thành: port BE + FE + test Playwright màn Hạch toán mua dịch vụ, dọn dữ liệu test.
Đang làm dở: không.
Bước tiếp theo: khởi động lại dev server rồi kiểm 4 sửa ở màn Yêu cầu; gán quyền 1703-1705 cho vai trò; chạy 3 dòng seeder trên dev/prod.
Blocked: dev server 3000 không nhận thay đổi file cũ (watcher).
