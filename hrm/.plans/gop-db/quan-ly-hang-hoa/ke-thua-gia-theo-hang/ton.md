# Kế thừa giá bán theo hãng — tồn đã chốt

> 24/10/2026 · @namdangit · nhánh `gop_db`. Design: `design.md`.

## Spec user (24/10, nguyên văn ý)

Bỏ nguyên tắc **không hỏi giá chéo giữa các công ty**, cho phép kế thừa giá từ công ty quản lý hàng hoá theo hãng.
1. Màn mới **Giá bán theo hãng sx** (menu Quản lý giá - CTKM): chọn cách cài đặt *Chọn hãng tự xây dựng giá bán* /
   *Chọn hãng kế thừa giá theo công ty quản lý*; đủ lịch sử chỉnh sửa.
2. Logic giá:
   - A lấy hàng của B về, hàng thuộc hãng **cần tính giá** ⇒ logic hiện có (YCHG hoặc Chuyển KD không tính giá).
   - Hàng thuộc hãng **kế thừa** ⇒ nhập đủ thông tin quản trị ⇒ cho chuyển Đang kinh doanh ⇒ lưu giá A = giá công ty quản
     lý ⇒ công ty quản lý đổi giá, định mức đàm phán (ĐMGG) thì A đổi theo. **Giá vốn không kế thừa.**
   - Hỏi giá hàng kế thừa ⇒ mặc định gửi sang công ty quản lý xử lý từ PTKD trở đi ⇒ giá tính xong áp cho mọi công ty
     đang kế thừa.
   - Hàng kế thừa vẫn hiện ở màn Cập nhật giá của công ty kế thừa nhưng **không được sửa giá**.

## Chốt (24/10/2026)

| # | Câu | Chốt |
|---|---|---|
| Q1 | Phạm vi cài đặt | **Mỗi công ty tự cài** cho công ty đang làm; hãng chưa cài = tự xây dựng (giữ hành vi hiện tại) |
| Q2 | "Công ty quản lý" | **Theo từng mã**: công ty tạo mã (`products.company_id`). Hàng công ty mình tạo luôn tự tính giá |
| Q3 | Giá trị kế thừa | **6 giá bán + ĐMGG + giá hiệu lực** (giá hẹn ngày), theo từng ĐVT. TMĐT chép nguyên số. Giá vốn không |
| Q4 | Sang Đang KD | **Bấm nút** "Chuyển kinh doanh (kế thừa giá)" theo dòng + hàng loạt + xác nhận (khuôn Chuyển KD không tính giá); hàng kế thừa trạng thái 1 ẩn nút *Không tính giá* + *Lập YCHG* |
| Q5 | Công ty quản lý chưa có giá thật | **Cho chuyển, nhận giá 0**; có giá sau thì tự đổi theo |
| Q6 | Lúc đồng bộ | **Ngay khi giá công ty quản lý được áp** (G4 sửa thẳng · G5 duyệt xong · PTG áp · cron giá hiệu lực); giá chờ duyệt chưa đổi; công ty kế thừa **không duyệt lại**; lịch sử giá công ty kế thừa ghi "Kế thừa từ <công ty>" |
| Q7 | Giá vốn công ty kế thừa | **Ngoài phạm vi** — user: "Giá vốn sẽ tự tính theo luồng riêng". Đợt này không ghi / không đổi giá vốn công ty kế thừa |
| Q8 | YCHG lẫn hàng | **Tự tách phiếu khi Gửi**: hàng tự tính giá ở lại phiếu công ty mình; hàng kế thừa tách YCHG riêng thuộc **từng công ty quản lý** (người lập vẫn là mình); PTKD/XNK/KTMH/duyệt giá của công ty quản lý; người lập xem + nhận thông báo phiếu tách (ngoại lệ duy nhất của "chỉ thấy công ty mình") |
| Q9 | Công ty quản lý khoá hàng | **Giữ giá cuối, vẫn bán**; hỏi giá hàng đó bị chặn ("Công ty quản lý đã ngừng kinh doanh hàng này"); khôi phục thì chạy tiếp |
| Q10 | Đổi Tự XD ⇒ Kế thừa | **Ghi đè ngay, có xác nhận** (popup "N hàng đang kinh doanh sẽ đổi sang giá công ty quản lý"); hàng 1 theo luồng mới; hàng 2/5 (YCHG đã gửi) ⇒ **chặn đổi**, liệt kê phiếu |
| Q11 | Đổi Kế thừa ⇒ Tự XD | **Giữ giá cuối thành giá riêng**, ngừng đồng bộ; YCHG tách đang chạy vẫn chạy, áp giá chỉ cho công ty quản lý + công ty còn kế thừa |
| Q12 | Quyền | **Quyền mới riêng** "Cài đặt giá bán theo hãng" (nhóm Tài chính, id mới, seeder riêng) |
| Q13 | Cách cài | **Chế độ + danh sách ngoại lệ**: "Chọn hãng tự xây dựng" (mặc định kế thừa, danh sách = tự tính) / "Chọn hãng kế thừa" (mặc định tự tính, danh sách = kế thừa). Chưa cài = "Chọn hãng kế thừa" + rỗng. Đổi chế độ hỏi xác nhận số hàng đổi giá (Q10/Q11) |
