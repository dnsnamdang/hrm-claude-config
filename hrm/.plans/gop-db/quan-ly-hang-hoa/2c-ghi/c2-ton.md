# Đợt 2-C2 — Tồn trước khi lập plan

> 08/10/2026 · gộp từ `c2-khao-sat-be.md` (Q1–Q4) + `c2-khao-sat-fe.md` (Q1–Q4), bỏ trùng.
> Luật cao nhất: `chot.md`. Hỏi LẦN LƯỢT từng câu; chưa trả lời hết thì không lập plan code.

## A. Hướng kỹ thuật đề xuất (từ khảo sát BE) — không phải câu hỏi

- `POST products/take` gate 1652, ≤100 mã; mã không hợp lệ (status ≠ 1, hàng của mình, đã có dòng status NOT NULL) ⇒ bỏ qua + báo lý do, lấy phần còn lại.
- Dòng hệ số cũ `status NULL` ⇒ UPDATE status, **giữ `coefficient`**; chưa có dòng ⇒ `insertOrIgnore` coef 1. Không dùng `upsert` (đè hệ số cũ).
- `PUT products/{id}/admin-data` cho công ty lấy về: chỉ 4 ô quản trị + NCC + catalog; gửi field ngoài ⇒ 403 (kể cả `tech_coefficient` — T6). `PUT {id}` đầy đủ giữ cho công ty tạo. `GET edit` nới + trả `edit_scope`.
- Không migration, không seeder.

## B. Tự chốt thuần UI (FE T1–T8 trong `c2-khao-sat-fe.md` §4)

Lấy về 1 dòng = icon ở menu hành động (khi `can_take_back`) · ô tick chỉ ở dòng lấy được, quá 100 cảnh báo · `$confirm` cho cả 1 dòng lẫn hàng loạt · tab Thông tin ở chế độ lấy về hiện chỉ đọc bằng 5 component chi tiết 2-B · Hệ số công nghệ khoá · Lưu chỉ gửi phần admin.

## C. Hỏi user

| # | Câu | ⭐ đề xuất | Trả lời |
|---|---|---|---|
| Q1 | Lấy về 803 mã đã có dòng hệ số cũ (Cty 2/3/4 đang bán thật ở ERP) ⇒ trạng thái gì? | 1 Đang nhập thông tin như mọi mã | ✅ 1 (08/10) |
| Q2 | 4 ô quản trị lúc lấy về ghi gì? | chép giá trị đang hiện từ cột chung `products` (bảo hành, ĐV bảo hành, tồn tối thiểu); Chính sách KD trống | 🔄 **để trống hết** (08/10) — chấp nhận cột Bảo hành/Tồn tối thiểu đổi từ có giá trị → trống sau khi lấy về |
| Q3 | Cho lấy về hàng mà công ty tạo còn ở *Đang nhập thông tin*? | cho | 🔄 **CHỈ hàng công ty tạo đang kinh doanh** (08/10) — trạng thái của công ty tạo (suy theo 2-B) = 3; hàng công ty tạo còn 1/2/4 ⇒ bỏ qua + báo lý do |
| Q4 | 17.512 hàng `products.status = 0` ở Kho dữ liệu | lọc bỏ hẳn (giữ 7 mã status 2/5 như ERP) | ✅ lọc bỏ (08/10) |
| Q5 | Công ty lấy về Lưu tab Quản trị có bắt buộc ≥ 1 Tiểu mục (như C1)? | có | ✅ có (08/10) — chỉ khi Lưu form, lấy về không bắt buộc |
| Q6 | Popup "Xem hàng hoá Công ty khác" ở màn Nhập thông tin làm trong 2-C2? | làm sau; đặt nút chuyển sang Kho dữ liệu | ✅ làm sau + nút chuyển trang (08/10) |
| Q7 | Công ty tạo sửa lớp chung ⇒ công ty lấy về thấy ngay, không thông báo | chấp nhận | ✅ chấp nhận (08/10) |

**08/10/2026: user chốt đủ Q1–Q7.** Đổi so với ⭐: Q2 (để trống), Q3 (chỉ hàng công ty tạo đang kinh doanh). Tiếp: lập `c2-plan.md`.
