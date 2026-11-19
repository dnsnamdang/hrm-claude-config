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

## Xác nhận sau go-live code (26/10/2026)

- **Q13 giữ nguyên 2 chế độ.** Cách dùng thật: TPSG, TPHP, TPV kế thừa 100% ⇒ "Chọn hãng tự xây dựng" + danh sách rỗng (hãng mới tự kế thừa); các công ty khác "Chọn hãng kế thừa" + vài hãng.
- **Q2 giữ nguyên:** nguồn giá = công ty tạo mã (công ty quản lý mã hàng), KHÔNG cố định TPE. Vd TPHP nhận giá TPSG cho 1.054 mã TPSG tạo, giá EG cho 1.967 mã EG tạo (số liệu dump prod 21/10).

## Đợt 2 — 28/10/2026: Lưu chạy nền + đổi cách khai báo + hệ số kế thừa

Spec user (28/10): (1) Lưu cài đặt khối lượng lớn bị 504 (sự cố prod 27/10). (2) Có hãng / mã hàng kế thừa phải nhân hệ số:
**giá bán = giá công ty quản lý × hệ số**. (3) Cách khai báo hiện tại khó hiểu ⇒ đổi 2 lựa chọn + thêm khai báo hệ số khác 1.

| # | Câu | Chốt |
|---|---|---|
| R1 | Sửa 504 | **Tăng `fastcgi_read_timeout` nginx bộ tpe ngay (gỡ tạm) ⇒ chuyển Lưu sang Job nền** (1 transaction trong job: chế độ + giá đổi cùng lúc commit; màn báo đang áp + chặn lưu lần 2) |
| R2 | Đổi tên 2 lựa chọn | **"Tự xây dựng giá bán riêng theo công ty"** (= chế độ 1 cũ; danh sách = hãng ngoại lệ **kế thừa**) · **"Kế thừa giá bán theo công ty quản lý hàng"** (= chế độ 2 cũ; danh sách = hãng ngoại lệ **tự tính giá**). Chỉ đổi nhãn — luật, dữ liệu, mã `mode` giữ nguyên |
| R3 | Kế thừa xét theo gì | **Vẫn theo hãng** (danh sách mã chỉ để khai hệ số, không có ngoại lệ kế thừa theo mã) |
| R4 | Hệ số gắn theo | **Công ty kế thừa** (công ty đang làm) — khai rồi áp cho mọi nguồn hàng từ các công ty khác; không theo cặp nguồn → đích |
| R5 | Mức khai | **Theo hãng hoặc theo mã hàng**; ưu tiên **mã > hãng > 1** |
| R6 | Loại giá nhân | **1 hệ số chung** cho cả 6 loại giá (kể cả TMĐT) + giá hiệu lực. ĐMGG không nhân |
| R7 | Làm tròn | **Theo cách làm tròn giá chung đang áp dụng**: `CompanyPriceBackfill::scalePrice` (hệ số ≠ 1 ⇒ `round(giá × k / 1000) × 1000`, như ERP). **Giá 1 đ giữ nguyên, không nhân** |
| R8 | Ô hệ số | Số thập phân **tối đa 2 chữ số** sau dấu chấm (đổi từ 1 → 2 ngày 29/10), ~~cho nhập < 1~~ → **chỉ cho > 1** (29/10, T2: giữ luật sàn giá 21/10 — giá công ty lấy về không thấp hơn giá công ty tạo mã) |
