# Plan — Fix phiếu con chuyển duyệt sai phòng ban

Repo `TanPhatDev`, nhánh `master`. @junfoke

## Phase 1 — Điều tra

- [x] Tái hiện: lọc DAISEN + nhân viên ra 3 phiếu, lọc DAISEN + phòng KV4 rỗng (ảnh user gửi)
- [x] Đọc `OrderReportProcessService::filter` — nhân viên lọc `created_by`, phòng lọc `department_id`
- [x] Tìm nguồn `department_id`: hook `created` của `RootOrderRequest` ghi đè bằng `Auth::user()`
- [x] Khoanh luồng tách mã lẻ: `RootOrderRequestService::switchApprove()` copy từ phiếu cha rồi bị đè
- [x] Kiểm chứng DB dev `erp_dev_30_01_26`: 18/18 phiếu con sai phòng (=46 XNK)
- [x] Kiểm chứng prod (user chạy SQL): 3 phiếu đúng như dự đoán; 351/371 sai phòng, 59 sai công ty

## Phase 2 — Sửa code

- [x] `app/Model/Order/RootOrderRequest.php` — hook `created` chỉ set khi `empty()`
- [x] `app/Services/OrderReports/OrderReportProcessService.php` — `ror.is_part` → `ror.part_id`
- [x] `php -l` 2 file, kiểm tra line ending không đổi

## Phase 3 — Verify

- [x] Test trên DB dev: giả lập duyệt tách mã lẻ, xác nhận phiếu con giữ phòng của phiếu cha
- [x] Kiểm tra luồng tạo phiếu mới bình thường vẫn được gán phòng/công ty (không hồi quy)

## Phase 4 — Vá dữ liệu cũ

- [x] Gửi user script UPDATE (theo phiếu cha) + nhắc backup; user tự chạy trên prod
- [x] User chạy vá trên prod 09/09/2026: 351 dòng lượt 1 + 5 dòng lượt 2 (chuỗi tách 3 cấp), con_lech = 0

### Checkpoint — 09/09/2026
Vừa hoàn thành: sửa 2 file (hook `RootOrderRequest::created` chỉ gán khi `department_id` còn trống;
`OrderReportProcessService` `is_part`→`part_id`). php -l sạch, CRLF nguyên vẹn (783/783 và
1035/1035 dòng có CR), diff 11+/4-.
Verify DB dev `erp_dev_30_01_26` bằng tinker + transaction rollback (KHÔNG đổi dữ liệu):
- Mô phỏng switchApprove (người duyệt phòng 46/cty 1, phiếu cha phòng 108/cty 4) → phiếu con giữ
  đúng phòng 108 / cty 4.
- Phiếu tạo mới thường → vẫn lấy phòng 46 / cty 1 của người tạo (không hồi quy).
- End-to-end qua `OrderReportProcessService::getData`: lọc phòng 108 với PDH-00411, trước khi vá
  = 0 dòng, sau UPDATE (trong transaction) = 3 dòng. Rollback xong DB dev vẫn 18 bản ghi lệch.
Đang làm dở: không có.
Bước tiếp theo: user backup prod → chạy UPDATE vá 351 phiếu → verify màn báo cáo (DAISEN +
Phòng KD Khu vực 4 phải ra PDH-07140/07148/07208). CHƯA commit.
Blocked: không có quyền truy cập DB prod nên không tự chạy được UPDATE.

### Checkpoint — 09/09/2026 (vá dữ liệu prod xong)
Vừa hoàn thành: user tự chạy trên prod theo quy trình đã gửi.
- Bước 0: 371 phiếu con, 351 dòng cần sửa. Backup `root_order_requests_bak_20260909` 7362/7362 dòng.
- Lượt UPDATE 1: đúng 351 dòng, đối chiếu backup 351 dòng khác / 0 dòng không phải phiếu con.
  3 phiếu gốc của ca lỗi (PDH-07140/07148/07208) về đúng phòng 109 (KV4), công ty 4.
- Còn 5 dòng lệch: **KHÔNG phải phiếu mới** mà là **chuỗi tách 3 cấp** (con → cha → ông:
  PDH-06277→06258→06202…). Trong 1 câu UPDATE self-join, MySQL đọc phòng của cha TRƯỚC khi chính
  cha được vá → cấp cháu bị WHERE loại ra, mỗi lượt chỉ lan được 1 cấp.
  ⇒ Chạy lại đúng câu UPDATE thêm 1 lượt (5 dòng) là con_lech = 0.
- Code KHÔNG dính lỗi nhiều cấp: phiếu con copy phòng của cha ngay lúc tạo, cha lúc đó đã đúng.
Bước tiếp theo: deploy 2 file code lên prod (chưa deploy thì phiếu tách mới lại sai tiếp);
giữ bảng backup vài ngày rồi DROP. CHƯA commit code.
Blocked: không có.
