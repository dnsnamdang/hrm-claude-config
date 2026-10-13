# Đợt 2-C4 — Tồn trước khi lập plan

> 08/10/2026 · gộp từ `c4-khao-sat-be.md` (Q1–Q7) + `c4-khao-sat-fe.md` (Q1–Q4), bỏ trùng.
> Luật cao nhất: `chot.md` (G6, G7, G9a, §35b-4, L1–L7). Hỏi LẦN LƯỢT; chưa trả lời hết thì không lập plan.

## A. Đã có chốt / kỹ thuật — không hỏi

- §35b-4: chỉ xoá được hàng *Đang nhập thông tin*, của công ty mình tạo, **chưa công ty nào lấy về**, chưa phát sinh chứng từ ⇒ công ty tạo xoá hàng đã có công ty khác lấy về = chặn (FE ẩn nút — thay FE Q4).
- Hàng sửa khi Ngừng KD: đổi 403 → **423** theo G6 + CLAUDE.md HRM (`ProductWriteService::authorize`), sửa ca test cũ theo.
- Phân biệt dòng ERP/HRM khi gỡ: `created_by IS NULL` = dòng ERP (dòng hệ số cũ) ⇒ trả `status NULL`, giữ `coefficient`.
- Endpoint đề xuất: `DELETE /products/{id}` (tạo ⇒ xoá cứng 20 bước, lấy về ⇒ gỡ) · `PUT /{id}/lock` · `PUT /{id}/unlock` · cờ `can_delete`/`can_lock`/`can_unlock`. Không migration, không seeder.
- UI tự chốt T1–T9 (`c4-khao-sat-fe.md` §4); mockup gần như không có 2-C4 (11 lệch L1–L11).

## B. Hỏi user

| # | Câu | ⭐ | Trả lời |
|---|---|---|---|
| Q1 | Xác nhận G6: chỉ khoá 3→4, mở về 3; hàng cũ chưa có dòng ⇒ sinh dòng coef 1 status 4 (giá popup ERP mã đó làm tròn nghìn) | đồng ý |  ✅ theo ⭐ (08/10) |
| Q2 | "Chưa phát sinh chứng từ" quét những bảng nào (153 cột FK 0,3–0,7s/mã; thêm 139 cột không FK 2,8–9,4s/mã) | FK + ~50 bảng không FK HRM đang dùng |  ✅ theo ⭐ (08/10) |
| Q3 | Nút Xóa ở danh sách hiện theo cờ nào | cờ nhẹ (trạng thái + chủ + chưa ai lấy về); kiểm chứng từ đầy đủ khi bấm, chặn thì báo lý do |  ✅ theo ⭐ (08/10) |
| Q4 | Công ty lấy về được gỡ ở trạng thái nào | chỉ khi của mình = 1 |  ✅ theo ⭐ (08/10) |
| Q5 | Gỡ có dọn NCC + 4 ô quản trị + catalog của mình | dọn hết |  ✅ theo ⭐ (08/10) |
| Q6 | Hàng đang là "Máy dùng cho"/phụ kiện của hàng khác (chiều ngược, không FK) | chặn xoá + báo lý do |  ✅ theo ⭐ (08/10) |
| Q7 | Xoá/khoá hàng loạt | không, từng dòng |  ✅ theo ⭐ (08/10) |
| Q8 | Quyền khoá/mở khoá/xoá | 1652, không quyền mới |  ✅ theo ⭐ (08/10) |
| Q9 | Xoá cứng có xoá tệp S3 | không |  🔄 **xoá tệp S3 không còn dòng nào trỏ tới** (sau khi xoá DB, kiểm mọi chỗ tham chiếu URL) (08/10) |

> 08/10 user làm rõ (khi hỏi Q1): hệ số giá sẽ bỏ sau chuyển đổi, mỗi công ty tự xây giá theo Cấu hình chính sách giá bán nội bộ ⇒ làm tròn nghìn do sinh dòng coef 1 chỉ là hệ quả tạm (tiền đề #8 SO-CHOT).

**08/10/2026: user chốt đủ Q1–Q9.** Đổi so với ⭐: Q9. Tiếp: lập `c4-plan.md`.

> 08/10 lúc xin "làm": user chọn **"Làm - Bỏ ko cần xoá S3"** ⇒ Q9 về lại ⭐ (không xoá S3).
