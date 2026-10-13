# T0 — Mockup luồng tính giá 4 chứng từ (11/10/2026) — ✅ USER DUYỆT 11/10/2026

> Duyệt kèm 6 điểm tự chốt còn hiệu lực (1–4, 7, 8). Từ đây là mốc đối chiếu khi code; muốn đổi giao diện thì mở vòng mới và ghi rõ.

File: `mockup-luong-tinh-gia.html` (mở trực tiếp bằng file://, không cần server).
Dựng từ bản chốt Phase 2 `../man-danh-muc-hang-hoa/mockup-luong-xay-dung-hang-hoa.html` — **bản đó giữ nguyên**,
file này chỉ đổi phần tính giá theo `ton.md` Q1–Q18. Các màn hàng hoá khác không đổi.

## Đã đổi / thêm

| Chỗ | Nội dung |
|---|---|
| Menu | Cụm tính giá: **Yêu cầu hỏi giá · Yêu cầu tính giá · Phiếu tính giá** (bỏ menu Kết quả — Q20). YCTG / PTG ẩn với người không có quyền XNK / Tính giá / 1092 |
| Thanh trên | Ô **Đăng nhập với** (điều khiển demo): Trần Thị Bình (KD) · Ngô Thị Lan (PTKD) · Nguyễn Văn An (XNK Launch) · Lê Minh Cường (XNK Bosch) · Phạm Quốc Dũng (KTMH + 1092) |
| Màn Nhập thông tin / Đang kinh doanh | Nút **Lập yêu cầu hỏi giá** (Q1a, Q15). Màn Dữ liệu công ty: nút đổi thành **Tiến độ tính giá** (mở YCHG đang chứa hàng) |
| YCHG danh sách | Cột nhóm `x/n nhóm đã tính giá`, bung dòng nhóm: XNK tiếp nhận · YCTG/PTG/link KQ · trạng thái nhóm · nút theo nhóm (Duyệt / Không có giá / Lập YCTG / Huỷ duyệt, chỉ đúng XNK được phân công) |
| YCHG form | Bảng gom nhóm cha–con (La Mã / 1-2-3), ĐVT liệt kê đủ, trạng thái hàng, giá bán lẻ hiện hành, cảnh báo "đang có người hỏi giá" ở phiếu khác. Nhóm chưa phân công XNK ⇒ dòng đỏ + **chặn gửi** (Q3). Xem: PTKD Duyệt / Không duyệt, ghi chú duyệt + lịch sử |
| YCTG form | 2 tab Hàng hoá · Chi phí; mỗi dòng = hàng × ĐVT (Q9); XNK nhập giá NCC / tiền tệ / tỉ giá / thuế / chi phí; KTMH: **Tính giá** / **Không duyệt** (lý do bắt buộc) |
| PTG form | Kế thừa YCTG, 3 tab; hệ số theo G4 (sửa Bán lẻ ghi đè 4 loại 2–5; TMĐT = Bán lẻ × 1,3 khoá); ghi chú dòng không ghi đè `products.note`; chụp chính sách khi lưu. Công ty bật quy chế (demo ETEK POWER) ⇒ **Chờ duyệt giá** + khối mô phỏng màn Duyệt giá bán; từ chối ⇒ mở lại |
| Kết quả tính giá | ~~màn riêng~~ ⇒ (11/10, Q20 cách A) **bảng "Giá bán mới" hiện ngay dưới nhóm đã tính giá trong YCHG** + nút In kết quả; link "Xem giá bán mới" ở danh sách YCHG / PTG / thông báo đều cuộn tới đúng nhóm. Chỉ giá bán |
| Bản in | Popup xem trước cho cả 4 chứng từ (Q17) |
| 1092 | Giá vốn công ty quản lý + giá mua suy ra từ giá vốn hiện "—" khi không có 1092 (Q12) |
| Sơ đồ luồng | Mục lục màn + bước 2 viết lại theo 4 chứng từ |

## Đã đo bằng Playwright (1440px, console chỉ lỗi favicon)

| Kiểm | Kết quả |
|---|---|
| Mọi hàng Chờ / Đang tính giá ở TÂN PHÁT truy về đúng 1 YCHG mở | 4/4 |
| Gửi YCHG có hàng Donaldson (chưa phân công) | toast nêu tên hãng, **không lưu**, vẫn ở form; bỏ mã đó gửi được, hàng mới ⇒ Chờ tính giá bán |
| Gate | Bình: chỉ In/Quay lại · Lan: Duyệt/Không duyệt · Cường không có nút ở nhóm Launch ("Chờ Nguyễn Văn An duyệt") · An: Duyệt/Không có giá → Lập YCTG/Huỷ duyệt · Bình: menu YCTG/PTG ẩn |
| YCTG | thiếu giá ⇒ "Chưa nhập giá NCC cho 2 dòng (hàng × ĐVT)"; 1.200 USD × 26.600 = 31.920.000, thuế 10% = 35.112.000 |
| PTG | giá nhập kho 13.072.620 (= 316 EURO × 31.900 × 1,1 + 62,2 EURO chi phí × 31.900) · hệ số Bán lẻ 1,5 lan 4 loại · sửa riêng Đại lý 1 không lan ngược · TMĐT 16.340.800 × 1,3 = 21.243.040 |
| TÂN PHÁT (tắt quy chế) | duyệt ⇒ PTG Đã duyệt, YCTG/YCHG Đã tính giá, hàng Đang kinh doanh, sinh KQ, chính sách được chụp |
| ETEK POWER (bật quy chế) | duyệt ⇒ Chờ duyệt giá, hàng Đang tính giá, chưa có KQ · từ chối ⇒ Giá bị từ chối + nút Lưu mở lại · duyệt ⇒ áp giá + KQ |
| 1092 | An: "Giá vốn ETEK POWER: —", dòng giá vốn popup Tạm tính "— — —" · Dũng: 168,000,000 |
| Bố cục | trang không tràn ngang (1440 = 1440) · nút cuối cụm lề phải 0, cách nhau 12px · bảng rộng cuộn ngang trong khung (1640/1356, 1960/1356) |
| Hồi quy | 8 màn cũ + form hàng hoá mở được; luồng bấm thật Nhập thông tin → Lập YCHG → popup chọn 3 mã → Lưu nháp đạt |

Ảnh: `anh-mockup/t0-*.png`.

🐞 Tự bắt khi dựng: (1) chèn ô "Đăng nhập với" làm mất thẻ đóng `.top` ⇒ cả thân trang lọt vào thanh trên, trang tràn 1.521px;
(2) `.sp` chỉ có `flex:1` khi nằm trong `.tp-head` ⇒ cụm nút chân form dồn trái; (3) giá bán lẻ hàng sinh tự động hiện số thô;
(4) ô chọn vai bị nâng cấp thành select tìm kiếm ⇒ trống chữ.

## Điểm mockup tự chốt — cần user soát

1. Nhóm XNK "Không có giá" / "Huỷ duyệt" là nhóm **đóng**; YCHG xong khi mọi nhóm đóng hoặc đã tính giá (hết nhóm có giá ⇒ "Không có giá"). Hàng mới của nhóm đóng ⇒ về Đang nhập thông tin.
2. PTKD Không duyệt ⇒ hàng mới cả phiếu về Đang nhập thông tin; người lập sửa, gửi lại.
3. KTMH Không duyệt YCTG ⇒ YCTG mở lại cho XNK; hàng giữ trạng thái.
4. YCTG có thêm trạng thái "Đang tính giá" (đã có PTG nháp) và "Chờ duyệt giá" — không chép lỗi ERP gán "Đã duyệt" khi PTG mới lưu nháp.
5. ~~KQ không có số phiếu~~ — hết hiệu lực (Q20: không còn màn KQ riêng).
6. ~~Thêm menu Kết quả tính giá~~ — hết hiệu lực (Q20).
7. Danh sách YCHG: phiếu Đang tạo / Không duyệt chỉ người lập thấy (giữ như ERP).
8. Nút "Lập yêu cầu tính giá" ở đầu danh sách YCTG mở popup chọn **nhóm đang chờ mình lập**; "Tạo phiếu tính giá" mở popup chọn YCTG Chờ tính giá (khuôn ERP).

## Sửa 11/10 — Kết quả tính giá về YCHG (Q20)

Đo Playwright: menu còn 3 mục tính giá, không còn `sc-kq` · Bình mở PYCHG-04027 thấy khối "Giá bán mới" 12 dòng (2 ĐVT × 6 loại),
không có chữ Giá NCC / Giá nhập kho / Chi phí, số YCTG/PTG là chữ thường (không link vì không có quyền) · bấm "Xem giá bán mới"
ở danh sách ⇒ mở YCHG, khối nằm trong khung nhìn · KTMH duyệt PTG-03121 ⇒ khối hiện dưới nhóm Launch của PYCHG-04030, nhóm
Fusheng chưa xong thì không có khối; cột "Giá bán lẻ hiện hành" = giá Bán lẻ mới (16,340,800). Console chỉ lỗi favicon.
Ảnh `anh-mockup/t0-hg-ket-qua-trong-nhom.png`.

## Sửa 11/10 — drill giá là dòng con của mã hàng (góp ý user)

Giá bán mới không còn là một khối chung cuối nhóm (lặp lại STT / Tên / Mã). Nay:
- **Dòng nhóm** (cha): "Giá bán mới áp ngày … · người tính giá · YCTG · PTG" + nút **In kết quả** (thay chỗ nút duyệt nhóm).
- **Dưới từng mã hàng**: bảng con chỉ còn `ĐVT · Loại giá · Giá mới · Định mức đàm phán giá · Ngày hiệu lực` (gộp ô ĐVT).

Đo: bảng con 5 cột, 12 dòng (2 ĐVT × 6 loại), không chứa mã hàng; nằm ngay sau dòng mã hàng; không tràn ô; trang 1440 không tràn ngang;
"Giá bán lẻ hiện hành" = Bán lẻ mới 41,743,800 (sửa lệch dữ liệu demo). Ảnh `anh-mockup/t0-hg-ket-qua-trong-nhom.png`.

### Sửa tiếp 11/10 — drill nhỏ gọn (góp ý user: header kiểu bảng chính nhìn rối)
- Bảng drill trải **từ cột Mã hàng tới cột cuối** (chỉ lùi sau cột STT): đo mép trái 145 = mép cột Mã hàng, mép phải 1427 = mép cột cuối.
- Bỏ header teal: tiêu đề cột chữ xám 11px, nền trong suốt, không gạch chân; viền trái xanh lá 2px, nền #f7fdf9.
- **Mỗi ĐVT một dòng, 6 loại giá là 6 cột** (Bán lẻ · Theo lô · Đại lý cấp 1/2/3 · TMĐT); ĐMGG là chữ phụ 10.5px dưới giá; bỏ cột "Ngày hiệu lực" (ngày áp đã ở dòng nhóm).
- Hàng 2 ĐVT: khối drill cao 109px (trước 12 dòng ~440px).

### Sửa tiếp 11/10 — chế độ xem "Chi tiết kết quả" ở YCHG + YCTG (góp ý user)
- Nút **Chi tiết kết quả** ↔ **Ẩn chi tiết kết quả** ở đầu card bảng hàng (YCHG: card "Hàng hoá hỏi giá"; YCTG: card "Chi tiết", kèm chữ "Giá bán mới áp ngày …").
  Chỉ hiện khi phiếu có nhóm / dòng đã áp giá. **Mặc định TẮT** (drill ẩn); mở phiếu khác thì về tắt.
- Bật ⇒ drill của mọi hàng đã có giá; mỗi drill có nút **× Ẩn** riêng; hàng đang ẩn có link **▸ Hiện giá mới** (YCHG: ô Giá bán lẻ hiện hành; YCTG: ô ĐVT).
  Link "Xem giá bán mới" (danh sách / PTG / thông báo) tự bật chế độ xem.
- YCTG: drill dưới từng dòng hàng × ĐVT, **bỏ cột ĐVT** (dòng đã là ĐVT); bảng chính rộng 1.640px nên drill **ghim vừa khung nhìn** (sticky) —
  đo: cách mép trái 48px (sau cột STT), mép phải 0, nút Ẩn trong khung cả trước và sau khi cuộn ngang 200px.
- PTG không có drill.
- 🐞 Tự bắt: link "Hiện giá mới" đặt ở ô Thành tiền sau thuế bị `tinhBang` ghi đè `textContent` ⇒ mất link; chuyển sang ô ĐVT.
- Đo: YCHG mặc định 0 drill → bật 1 → ẩn 1 còn 0 + có link → hiện lại 1 → tắt 0; nhóm chưa xong không có nút. YCTG-03147: bật 2 drill → ẩn 1 còn 1 + link; YCTG chưa có giá không có nút.
Ảnh `anh-mockup/t0-yctg-chi-tiet-ket-qua.png`.
