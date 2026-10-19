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

## Phase 5 — Redmine #11708 (15/10) — chỉnh màn danh sách
- [x] 1. Nhà cung cấp / Tên dịch vụ thành 2 ô lọc gõ tay (`supplier` khớp tên + mã NCC, `cost_name` theo dòng chi tiết); bỏ 2 thứ này khỏi ô tìm nhanh + placeholder
- [x] 2. Bộ lọc Trạng thái: GIỮ 2 giá trị (user chốt 15/10) — ERP hiện 5 trạng thái của phiếu YÊU CẦU nhưng lọc theo id trên cột trạng thái phiếu hạch toán (lọc sai)
- [x] 3. Ô khoảng ngày đã chọn thì ẩn icon lịch — sửa CHUNG `V2BaseFloatingField` (`.ff--range`) + `V2BaseFilterFieldControl` (bản boxed), user đồng ý sửa chung
- [x] 4. Bỏ sort cột Trạng thái (FE + `SORTABLE_COLUMNS`)
- [x] 5. Thêm cột Người cập nhật / Ngày cập nhật (sort được) vào bảng + Excel (`ExportColumnRegistry`), quan hệ `employee_update`
- [x] Compile FE + smoke test HTTP kernel (lọc NCC/tên DV, keyword không còn khớp NCC, sort updatedAt, export 200)
- [ ] User kiểm trên trình duyệt (icon lịch, 2 ô lọc mới, 2 cột mới)

## Phase 6 — Redmine #11712 (15/10) — Xuất Excel
- [x] Số hợp đồng toàn chữ số (HĐNT bảo hiểm `1812000`) bị thành ô SỐ, căn phải → class `Modules/Finance/Exports/BuyServiceAccountingListExport` (con của `DynamicExport` dùng chung, KHÔNG sửa class chung) ép cột `code` / `request_code` / `contract_code` về chuỗi; controller dùng class mới
- [x] Dựng file thật + đọc lại: mã toàn số = `s`, giữ số 0 đầu, ô tiền vẫn `n`; endpoint export 200

## Phase 7 — Redmine #11713 (15/10) — Tạo mới + rà câu lỗi
- [x] 1. TK có mặc định 3311 ngay lúc mở màn Tạo (ERP class JS `before()` account_has = 99 — đúng nghiệp vụ, không phải lỗi); lấy `default_account_has` từ catalogs
- [x] 2. Lưu nháp chỉ bắt Phiếu yêu cầu (FE + FormRequest `$required` theo status); rule định dạng / SL vượt vẫn chặn; cột NOT NULL ghi 0/'' khi trống như ERP, show trả null
- [x] 3. Popup chọn phiếu yêu cầu: mã phiếu là link tab mới, `size="lg"` (thêm prop `size` cho SourcePickerModal, mặc định xl); chữ nút đã nowrap từ #11703
- [x] 4. Số đơn bảo hiểm là link cổng ERP `/admin/insurance/form-insurance/{id}/show`
- [x] 5+6. File của phiếu yêu cầu hiện ngay khi chọn (nhóm pendingFiles `inherited`, gỡ được, không xoá S3); (*) File đính kèm theo "Kèm hóa đơn"; BE bỏ tự gộp file lúc tạo — lưu đúng danh sách FE gửi
- [x] Rà câu lỗi: BE thêm `messages()` mẫu `<Tên> – <Nội dung>` (lang vi không kèm tên trường); sửa "Tổng thanh toán – Phải lớn hơn 0 trước khi duyệt" FE+BE; lỗi đó loại bảo hiểm thêm V2BaseError dưới bảng; lỗi `saveAccountDetail` thêm tiền tố
- [x] Test HTTP kernel (rollback, kiểm lại count 49): nháp trống 200, duyệt trống 422 đủ tiền tố, nháp sai định dạng 422
- [ ] Chưa sửa: câu lỗi chọn file của AttachmentSection dùng chung (`File "x" không thuộc định dạng cho phép`) thiếu tiền tố — chờ user
- [ ] User kiểm trên trình duyệt
- [x] Phản hồi #5 (16/10): chữ trong ô lệch 12/13px — ô link `.v2-linked-field` (dùng chung, 13px) cạnh ô `V2BaseInput`/`V2BaseSelect` cỡ sm (12px). Ép 12px trong `<style scoped>` của `BuyServiceAccountingForm.vue`, KHÔNG sửa class chung (30 file dùng)

## Phase 8 — Redmine #11714 (15/10) — Lịch sử: File đính kèm
- [x] Khoá ảo `attachments_list` (chuỗi TÊN tệp, in lại cả danh sách cũ → mới, không mở được) → `attachment_rows` dạng BẢNG giữ NGUYÊN URL (khuôn màn Yêu cầu #11706): chỉ in nhóm "File đính kèm thêm mới / đã xóa", tên file bấm được xem trước (SystemInfoValue sẵn có, không sửa FE)
- [x] `CatalogHistoryService::TABLES` thêm nhãn `attachment_rows`, giữ `attachments_list` cho log cũ
- [x] Test HTTP kernel (rollback, count 49): tạo 2 file → thêm 1 → xoá 1 → lưu lại không đổi = đúng 2 dòng (1 thêm, 1 xoá), không log rác
- [ ] Log CŨ (đã ghi trước sửa) vẫn hiện dạng chuỗi tên tệp, không bấm được — không sửa dữ liệu log cũ

## Phase 9 — Redmine #11715 (15/10) — Chi tiết
- [x] 1. Khối Hạch toán đọc `account_details.money_value` (giữ số lẻ) thay `money_value_exchange` (ERP làm tròn khi ghi sổ) → khớp Tổng thanh toán khối Chi tiết; chỉ đổi HIỂN THỊ, không đụng dữ liệu sổ. 149 bút toán đều VND tỷ giá 1
- [x] 2. Nhãn ô ghi chú thống nhất "Diễn giải" cho cả 2 loại: form (Tạo/Sửa/Chi tiết), bản in ROW_4 loại bảo hiểm, câu lỗi BE — khớp Lịch sử (vốn luôn "Diễn giải")
- [ ] Màn Yêu cầu hạch toán vẫn đổi nhãn theo loại (Diễn giải / Ghi chú) như ERP — chưa đụng, chờ user

### Checkpoint — 2026-10-12 17:10
Vừa hoàn thành: port BE + FE + test Playwright màn Hạch toán mua dịch vụ, dọn dữ liệu test.
Đang làm dở: không.
Bước tiếp theo: khởi động lại dev server rồi kiểm 4 sửa ở màn Yêu cầu; gán quyền 1703-1705 cho vai trò; chạy 3 dòng seeder trên dev/prod.
Blocked: dev server 3000 không nhận thay đổi file cũ (watcher).
