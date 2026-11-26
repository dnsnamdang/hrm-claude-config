# Check: Kết xuất báo giá sang Thầu / HĐ — clear Tài liệu đính kèm, Hình ảnh, Thông tin bổ sung có ảnh hưởng logic không?

- Người phụ trách: @khoipv
- Bắt đầu: 26/11/2026
- Màn: `/plan/quotation/:id/render` (dùng chung `pages/plan/quotation/components/GeneralComponent.vue` với `isRender`)

## Câu hỏi
Ở màn báo giá, khi kết xuất sang thầu / hợp đồng muốn clear 3 khối: Tài liệu đính kèm (`quotations.attachments`), Hình ảnh (`quotations.images`), Thông tin bổ sung (`note`). Có ảnh hưởng logic đang chạy không?

## Kết luận
**Không ảnh hưởng logic nghiệp vụ** (trạng thái, gói thầu, HĐ, in, thông báo).

1. Kết xuất (`QuotationService::render`, ~dòng 837) chỉ đổi trạng thái báo giá + dự toán, lưu nhóm "Báo cáo tiến độ" (`quotation_attachments`) và "Thư mời" (`quotation_attachment_invitations`) — KHÔNG đọc/ghi `attachments`, `images`, `note`.
2. Gói thầu tạo từ báo giá (`bid_package/add.vue` → `appendQuotation`) KHÔNG chép 3 trường này. Tài liệu của gói thầu là bảng riêng `bid_package_attachments`.
3. HĐ tạo từ báo giá:
   - Ngoài thầu (`contract/add.vue` → `addNegotiation`, GeneralComponent.vue:2383) gán `bid_package_attachments = data.attachments` → Tài liệu đính kèm của báo giá đang hiện nhầm ở tab "Kết quả thầu" của form tạo HĐ (chỉ hiển thị, không lưu — `ContractDetailResource:213` lấy từ gói thầu). Clear thì tab này trống → đúng hơn.
   - Loại 3/4/5 (`onQuotationChange`) chép `note` nhưng `note` báo giá luôn null (xem mục 5).
   - Phụ lục giá (`contract_annex_price` GeneralComponent:1026) cùng kiểu — chỉ hiển thị.
4. In báo giá (`QuotationController::print`) không dùng 3 trường này.
5. Phát hiện: `quotations` KHÔNG có cột `note` (không có trong `$fillable`) → "Thông tin bổ sung" chỉ được chép từ dự toán lúc tạo, không bao giờ lưu; mở lại báo giá luôn trống. Clear trường này = không làm gì.
6. Lưu ý nếu làm: chỉ set JSON `attachments` / `images` = [] (hoặc ẩn khối trên màn kết xuất), KHÔNG xoá file S3 — link file chép nguyên từ dự toán (`addProject`) nên dự toán đang dùng chung file.

## Task
- [x] Trace luồng kết xuất + tạo gói thầu / HĐ / phụ lục từ báo giá
- [x] Kiểm DB local: `quotations` có `attachments`, `images`, `attached_files`, không có `note`
- [x] User chốt 26/11/2026: làm trên `master`, khi kết xuất sang Thầu / HĐ thì clear 3 thông tin (phương án a)
- [x] BE `QuotationService::render`: kết xuất sang Thầu (loại 1) / HĐ (loại 2, 4, 5, 6) → `attachments = []`, `images = []` (Hủy thì giữ; `note` không có cột nên không cần xử lý; không xoá file S3)
- [x] Test local (rollback, fake queue/notification): BG-310 Thầu → att 2→[] img []; BG-311 HĐ → att 2→[]; BG-311 Hủy → giữ nguyên. DB local không có BG loại 4/5/6 có tài liệu (cùng nhánh code). `php -l` OK.
- [x] Commit + push `master` repo API: `6407dca7` (theo yêu cầu user 26/11/2026)
- [x] Merge `master` → `thanhan-dev` (local, merge commit `1320687c`, không xung đột, chưa push)
- [ ] Deploy API (không migration) + user test tay

### Checkpoint — 26/11/2026
Vừa hoàn thành: clear `attachments` + `images` của báo giá khi kết xuất sang Thầu / HĐ (`Modules/Category/Services/QuotationService.php`, hàm `render`, ngay sau nhánh Hủy)
Đang làm dở: —
Bước tiếp theo: deploy API, user test tay màn `/plan/quotation/:id/render`
Blocked:

## Dọn dữ liệu cũ (yêu cầu 26/11/2026)
Xoá Tài liệu đính kèm + Hình ảnh của các báo giá ĐÃ kết xuất sang Thầu / HĐ trước bản sửa `6407dca7`.
- Điều kiện: `status` thuộc nhóm sau kết xuất — 4 Đã lập HĐ, 7 Đã gửi thầu, 8 Đã lập gói thầu, 9 Chuyển HĐ, 10 Đang lập HĐ, 11 Đang lập gói thầu, 17 Gói thầu bị hủy, 18 Gói thầu đã kết xuất, 19 Hủy HĐ, 20 Từ chối lập gói thầu. Không lấy 12 Hủy (kết xuất với kết quả Hủy).
- Không dựa vào `rendered_at` (dữ liệu cũ có thể thiếu nếu chưa chạy backfill). Local: mọi BG ở các trạng thái trên đều có `rendered_at`; 2 BG có `rendered_at` nhưng đã quay về 3/5 (BG-331, BG-335) không có tài liệu/ảnh → bỏ qua.
- [x] Seeder `database/seeders/ClearQuotationAttachmentsAfterRenderSeeder.php` (chỉ set JSON = [], không xoá file S3; in số lượng + mã BG đã xoá)
- [x] Test local trong transaction rollback: 87 BG được xoá (trước: 83 có tài liệu, 5 có ảnh → sau 0/0); BG trạng thái khác giữ nguyên (90 tài liệu / 7 ảnh); chạy lần 2 → 0 BG. `php -l` OK.
- [x] Commit + push `master` repo API: `798a622b`
- [ ] Deploy → chạy `php artisan db:seed --class=ClearQuotationAttachmentsAfterRenderSeeder`

### Checkpoint — 26/11/2026
Vừa hoàn thành: seeder dọn Tài liệu đính kèm + Hình ảnh của BG đã kết xuất, test rollback đạt
Đang làm dở: —
Bước tiếp theo: deploy API, backup cột attachments/images rồi chạy seeder trên server
Blocked:
