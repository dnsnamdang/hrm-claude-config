# SRS + Testcase — luồng Chuyển đổi hàng hoá

Yêu cầu user 16/10/2026: xuất SRS + testcase đúng chuẩn dự án, giải thích quyền + logic, đủ case, tập trung case giá bán;
bắt đầu từ màn **Hàng hoá nhập thông tin** + tạo / sửa / khoá / xoá hàng. Các màn tiếp theo (Cập nhật giá bán, Duyệt giá bán,
YC hỏi giá, YC tính giá, Phiếu tính giá…) làm sau theo yêu cầu.

## Đã xong
- [x] Màn Hàng hoá nhập thông tin (+ Tạo / Sửa / Chi tiết / Xoá / Khoá-Mở khoá / Lập YCHG / Xuất Excel)
  - `SRS - Hàng hoá nhập thông tin.docx` — 10 chức năng, 25 BR (BR-14…BR-23 về giá), selfcheck khớp bản mẫu
  - `testcase - Hàng hoá nhập thông tin.xlsx` — 177 TC, P0 44%, section IX Giá bán 25 TC
  - Generator: `gen_srs.py`, `gen_testcase.py`; ảnh `hang-hoa_shots/` (Playwright 3031, tài khoản E2E Assign)
  - Ảnh danh sách dùng dữ liệu minh hoạ (DB dev không có hàng 1/2/5, Loại SP rỗng); popup Mở khoá dựng lại bằng component thật
- Phát hiện khi chụp: N166–N169 (ghi ở `../viec-con-lai.md` mục A1/A2)
- [x] Màn Cập nhật giá bán (Tài chính › Quản lý giá - CTKM › Giá bán, quyền 1657) — 16/10/2026
  - `SRS - Cập nhật giá bán.docx` — 7 chức năng (Xem DS · Tìm kiếm lọc · Cập nhật giá · Giá hiệu lực · Gửi duyệt · Lịch sử giá ·
    Công thức lắp ráp), 24 BR (BR-03…BR-11, BR-17…BR-19 về giá), srs_selfcheck khớp bản mẫu + Bước 4 OK
  - `testcase - Cập nhật giá bán.xlsx` — 122 TC (11 TC-ROLE), P0 44%, section VI Giá bán 20 TC
  - Generator: `gen_srs_cap-nhat-gia-ban.py`, `gen_testcase_cap-nhat-gia-ban.py`; ảnh `cap-nhat-gia-ban_shots/` (Playwright 3031,
    E2E Assign — có sẵn 1657 ở Cty 1, KHÔNG tạo role tạm; DB không ghi gì)
  - Minh hoạ trên trình duyệt (không đổi DB): khối bị khoá (chặn request Lưu, trả câu Ngừng KD), nút + popup Gửi duyệt (8 công ty
    đều tắt duyệt giá). Ảnh popup Lịch sử dùng lại ảnh thật lúc kiểm G4 (DB dev không còn dòng lịch sử giá)
  - Mục lục docx CHƯA cập nhật số trang (Word đang mở trên máy — bước cập nhật mục lục của lib sẽ tắt Word); chạy lại với
    `SRS_UPDATE_TOC=1` khi Word đã đóng, hoặc chuột phải mục lục → Update Field
  - Phát hiện khi làm (ứng viên cho `../viec-con-lai.md`, chưa sửa code):
    1. TMĐT lúc mới tải hiện giá trong CSDL, không phải giá công thức (trái T5 ghi ở `utils/productPriceModel.js`): TEWI-AQUA
       TMĐT 0 / Giá công thức 0 dù Bán lẻ 341,000,000; sửa bất kỳ ô nào thì TMĐT nhảy lên 443,300,000 và lưu là ghi luôn
    2. Nhảy tới ô lỗi (Giá vốn) cuộn ngang làm ô Giá vốn nằm 29px dưới cột dính “ĐVT · Lưu” (đo: ô left 576 < cột dính right 605),
       chữ lỗi bị che (“…ắt buộc phải nhập”)
    3. Ô Giá mới hiện giá bị TỪ CHỐI; công ty lưu thẳng chỉ sửa 1 ô rồi Lưu là áp luôn giá bị từ chối (kế thừa ERP) — cần
       nghiệp vụ xác nhận
    4. Màn KHÔNG áp quyền 1092 Xem giá vốn (đúng chốt mockup 09/10: 1657 gồm xem giá vốn) — ghi rõ trong SRS để khỏi hiểu nhầm
    5. FE ghim hệ số TMĐT 1.3 (`ECOM`), máy chủ đọc cấu hình từng công ty — cấu hình khác 1.3 thì số trên màn lệch số lưu
    6. Dòng đếm ghi “tại công ty đang làm việc” thay vì tên công ty khi tài khoản không có danh sách công ty (gặp ở E2E Assign)

- [x] Màn Duyệt giá bán (Tài chính › Quản lý giá - CTKM › Giá bán, quyền 1658; lối phụ Chờ duyệt › Giá bán chờ duyệt ›
  Hàng hoá chờ duyệt giá bán; deep-link thông báo [GIA]; ERP Chờ duyệt › Duyệt giá bán (HRM)) — 16/10/2026
  - `SRS - Duyệt giá bán.docx` — 8 chức năng (Xem DS · Tìm kiếm lọc · Sửa giá đề nghị · Duyệt · Không duyệt · Hàng loạt ·
    Xuất Excel · Lịch sử giá), 22 BR (BR-04…BR-11, BR-17 về giá), srs_selfcheck khớp bản mẫu + Bước 4 OK
  - `testcase - Duyệt giá bán.xlsx` — 125 TC (13 TC-ROLE), P0 47%, section VI Giá bán 18 TC
  - Generator: `gen_srs_duyet-gia-ban.py`, `gen_testcase_duyet-gia-ban.py`; ảnh `duyet-gia-ban_shots/` (Playwright 3031, E2E Assign —
    có sẵn 1658 + 1092 + 1657 ở Cty 1, KHÔNG tạo role tạm; DB không ghi gì, đếm roles/rhp/ehr giữ 130/20967/1718)
  - DB dev KHÔNG có yêu cầu duyệt nào ⇒ ảnh danh sách / popup / thông báo là MINH HOẠ (chặn API trên trình duyệt, 3 yêu cầu dựng
    từ hàng thật TEWI-AQUA, SULI-…-NO14, -NO12); mọi lệnh Duyệt / Không duyệt bị chặn trên trình duyệt (0 request tới máy chủ).
    Ảnh thật: màn rỗng, menu 2 lối vào, popup Lịch sử (rỗng) + ảnh timeline G4 dùng lại
  - Mục lục docx CHƯA cập nhật số trang (Word đang mở) — chuột phải mục lục → Update Field, hoặc `SRS_UPDATE_TOC=1`
  - Phát hiện khi làm (ứng viên cho `../viec-con-lai.md`, chưa sửa code):
    1. Không duyệt với lý do > 2000 ký tự: popup đã đóng, mất lý do, toast tiếng Anh “The given data was invalid.” (FE không
       chặn độ dài, `handleError` toast `body.message`; lỗi `approve_comment` không có chỗ hiện)
    2. Màn Duyệt KHÔNG tính lại TMĐT khi người duyệt sửa giá Bán lẻ (và không lan Bán lẻ sang 4 loại giá) — lệch quy tắc TMĐT =
       Bán lẻ × 1.3 mà máy chủ ép ở nhánh lưu thẳng; cần nghiệp vụ chốt
    3. Hệ số → giá ở dòng giá hiệu lực màn Duyệt làm tròn TRĂM (`coefToPrice`), màn Cập nhật làm tròn ĐỒNG (BR-11 SRS Cập nhật)
    4. Ẩn giá vốn không nhất quán: bảng / Excel ẩn khi thiếu 1092; popup Lịch sử chỉ ẩn khi thiếu CẢ 1657 lẫn 1092
    5. Popup Duyệt ghi “giá vốn đề nghị ghi vào công ty công ty đang làm việc.” khi không đọc được tên công ty (cùng gốc mục 6
       của màn Cập nhật giá bán)
    6. Không duyệt hàng loạt không báo số yêu cầu bị bỏ qua do người khác đã xử lý (Duyệt hàng loạt có báo)
    7. (thẩm mỹ) Lỗi “Không được vượt quá 2 chữ số trước dấu phẩy” ở cột Hệ số 72px xuống dòng từng chữ (cao ~190px)
    - Đã có sẵn, không ghi lại: N169(a) duyệt vẫn áp giá cho hàng bị khoá

- [x] Màn Yêu cầu hỏi giá (Bán hàng › Yêu cầu › Hàng hóa › YC hỏi giá; lối phụ: nút Lập yêu cầu hỏi giá ở Hàng hoá nhập thông
  tin / Hàng đang kinh doanh / Hàng tạm, link YCHG ở YCTG / PTG, thông báo [YCHG]) — 16/10/2026
  - `SRS - Yêu cầu hỏi giá.docx` — 16 chức năng (Xem DS · Tìm kiếm lọc · Cài đặt lọc/cột · Tạo · Chọn hàng hoá · Thêm/sửa hàng tạm ·
    Sửa · Xem chi tiết · Xoá · PTKD duyệt · PTKD từ chối · PTKD duyệt hàng tạm · XNK duyệt nhóm/Lập YCTG · XNK không có giá/Huỷ duyệt ·
    Xem giá bán mới · In phiếu/In kết quả), 22 BR (BR-08…BR-11 về giá), srs_selfcheck khớp bản mẫu + Bước 4 OK
  - Phân quyền: KHÔNG cần quyền để lập/xem/sửa/xoá/in (phạm vi V1 người lập — nháp/Không duyệt, V2 cả công ty — phiếu đã gửi, V3 công
    ty khác = không thấy); Q1 1662 PTKD, Q2 1663 XNK (+ phải là người mua phân công hiện hành), Q3 1664 / Q4 1092 chỉ mở link YCTG,
    Q5 1652 sửa hàng tạm người khác tạo
  - `testcase - Yêu cầu hỏi giá.xlsx` — 135 TC (14 TC-ROLE), P0 50%, section VI Giá bán 18 TC
  - Generator: `gen_srs_yc-hoi-gia.py`, `gen_testcase_yc-hoi-gia.py`; ảnh `yc-hoi-gia_shots/` (Playwright 3031, E2E Assign)
  - Role tạm TMP_SRS_YCHG_1662 (id 129856, chỉ 1662 Cty 1) để chụp THẬT nút PTKD — ĐÃ GỠ + cache:forget, đếm roles/rhp/ehr về
    130/20967/1718. Mọi lệnh ghi bị chặn trên trình duyệt (DB không đổi — đã đối chiếu PYCHG-04280/4282/4287)
  - Dữ liệu THẬT: danh sách 2.560 phiếu Cty 1, form Tạo + popup + màn hàng hoá, PYCHG-04280 (PTKD), PYCHG-04283 + PTG-03178 (giá bán
    mới, in kết quả), trang 404 phiếu người khác. MINH HOẠ (sửa phản hồi trên trình duyệt): dòng Đang tạo của mình (Sửa/Xoá), thông báo
    duyệt thành công, nút XNK (tài khoản không phải XNK phân công), form Sửa phiếu Không duyệt, hàng tạm + form Duyệt hàng tạm
    (DB dev không có hàng tạm, cây Loại SP rỗng ⇒ không tạo được hàng tạm)
  - Mục lục docx CHƯA cập nhật số trang (Word đang mở) — chuột phải mục lục → Update Field, hoặc `SRS_UPDATE_TOC=1`
  - Phát hiện khi làm (ứng viên cho `../viec-con-lai.md`, chưa sửa code):
    1. (giao diện, đo DOM) Bung dòng nhóm có chữ “Chờ <tên XNK> duyệt” làm cột Hành động giãn 100 → 186px, bảng 1222px > khung 1139px ⇒
       cuộn ngang, cột Hành động bị che một phần (1440px)
    2. Màn Hàng đang kinh doanh: khi hiện dải “Có N hàng hoá đang kinh doanh chưa xếp catalog” (slot toolbar của V2BaseDataTable) thì
       thanh hàng loạt (slot left-actions — “Đã chọn N hàng hoá”, Lập yêu cầu hỏi giá, Bỏ chọn, Xếp catalog) KHÔNG bao giờ hiện
       (V2BaseDataTable `v-if toolbar / v-else-if left-actions`). Đã tick 2 hàng, không có thanh; nút đầu bảng vẫn dùng được
    3. Form Sửa phiếu Không duyệt không hiện lý do PTKD từ chối (khối Ghi chú duyệt & lịch sử chỉ ở màn Chi tiết)
    4. Ô lọc “XNK tiếp nhận” lọc theo XNK ghi trên nhóm (lúc gửi/duyệt), còn cột hiện XNK phân công HIỆN HÀNH với nhóm chưa có YCTG ⇒
       đổi phân công sau khi gửi là 2 bên lệch
    5. Cột / ô lọc “PTKD duyệt” chứa cả người TỪ CHỐI (approver ghi cả khi từ chối) — nhãn dễ hiểu nhầm
    6. (nhẹ) Ô lọc “Người tạo” liệt kê cả người chỉ có phiếu nháp / Không duyệt (người xem không thấy các phiếu đó)
    7. (môi trường) Bản in local không có letterhead — đã biết (ERP_URL), không phải lỗi màn

- [x] Màn Yêu cầu tính giá (Bán hàng › Yêu cầu › Hàng hóa › YC tính giá, menu isShow 1663 | 1664 | 1092; lối phụ: nút Lập YCTG ở
  dòng nhóm YCHG (Chi tiết + danh sách), Tạo mới + popup Chọn nhóm, thông báo [YCTG], link YCTG ở YCHG / PTG) — 16/10/2026
  - `SRS - Yêu cầu tính giá.docx` — 14 chức năng (Xem DS · Tìm kiếm lọc · Cài đặt lọc/cột · Tạo · Chọn nhóm · Nhập chi phí · Sửa ·
    Xem chi tiết · Xoá · Gửi tính giá · KTMH từ chối · Tính giá / Xem PTG · Xem giá bán mới · In), 20 BR (BR-07, BR-15, BR-16 về giá),
    srs_selfcheck khớp bản mẫu + Bước 4 OK
  - Phân quyền: XEM cần 1 trong 3 quyền 1663 / 1664 / 1092 (không có ⇒ menu ẩn, “Bạn không có quyền xem yêu cầu tính giá”, mở thẳng ⇒
    404); Q1 1663 lập (kèm là XNK phân công hiện hành), sửa / gửi / xoá YCTG mình lập (không xét lại phân công); Q2 1664 Từ chối + Tính
    giá + nhận thông báo; Q3 1092 chỉ thêm giá vốn công ty quản lý ở cột Chính sách giá nội bộ (thiếu ⇒ “—”, máy chủ không trả số).
    Phạm vi: nháp chỉ người lập; còn lại cả công ty; công ty khác không thấy
  - `testcase - Yêu cầu tính giá.xlsx` — 127 TC (15 TC-ROLE), P0 50%, section VI Giá 21 TC. Bộ kiểm “1 ô nhiều ý 1 dòng” báo 1 ô
    G51 là báo nhầm (tên “Nguyễn Thị Thanh Trà - HN_XNK - 12210394” có dấu “ - ”)
  - Generator: `gen_srs_yc-tinh-gia.py`, `gen_testcase_yc-tinh-gia.py`; ảnh `yc-tinh-gia_shots/` (Playwright 3031, E2E Assign)
  - Role tạm TMP_SRS_YCTG_1663_1664 (id 129857, 1663 + 1664 Cty 1) để chụp THẬT nút Tạo mới + popup Chọn nhóm — ĐÃ GỠ + cache:forget,
    đếm roles/rhp/ehr về 130/20967/1718. Mọi lệnh ghi bị chặn trên trình duyệt; YCTG Cty 1 vẫn 3:4 · 4:2285 · 5:19 · 1:1
  - Dữ liệu THẬT: menu, danh sách 2.305 YCTG Cty 1, lọc, cấu hình cột, popup rỗng (không được phân công), PYCTG-03162 (EURO, 3 chi phí,
    kết quả, in), PYCTG-01939 (2 ĐVT), 02786 (Không duyệt), 01403 (nhóm Huỷ duyệt), 00177 (PTG nháp người khác ẩn), 02874 (nháp người khác
    ⇒ 404). MINH HOẠ (sửa phản hồi trên trình duyệt): popup có nhóm, form Tạo (dòng thật của PYCTG-02257), lỗi / gợi ý giá / chi phí /
    xác nhận / rời màn, Chờ tính giá với KTMH (Tính giá, Từ chối), form Sửa, hộp Xoá, 3 kiểu cột Chính sách có / không 1092, không quyền
    xem. DB dev KHÔNG có YCTG Chờ tính giá / Chờ duyệt giá, không có chính sách giá nội bộ cho công ty mua
  - Mục lục docx CHƯA cập nhật số trang (Word đang mở) — chuột phải mục lục → Update Field, hoặc `SRS_UPDATE_TOC=1`
  - Phát hiện khi làm (ứng viên cho `../viec-con-lai.md`, chưa sửa code):
    1. (hỏi nghiệp vụ) Lưu nháp YCTG Không duyệt ⇒ về Đang tạo (`fill()` ghi status theo send): mất dòng lý do, người khác không còn
       thấy, và XOÁ được ⇒ trái T4-Q3 (“Không duyệt chỉ sửa rồi gửi lại”, nhóm có YCTG 5 không Huỷ duyệt được)
    2. Thuật ngữ 1 thao tác KTMH 4 chữ: nút “Từ chối”, trạng thái “Không duyệt”, lịch sử “KTMH không duyệt”, thông báo “[YCTG] Yêu cầu
       làm lại” (bảng thông báo ở `luong-tinh-gia/design.md` ghi “[YCTG] Không duyệt”); thông báo gửi ghi “Chờ duyệt” trong khi trạng thái là “Chờ tính giá”
    3. Lỗi máy chủ khoá `rows` (“Nhóm không còn hàng hoá nào có đơn vị tính”) không có chỗ hiện trên form ⇒ bấm Lưu không thấy gì
    4. Câu lỗi số quá lớn lệch: màn “Không hợp lệ”, máy chủ “Không được lớn hơn 999,999,999,999.” (Giá NCC, Tỉ giá)
    5. Cột Chi phí: màn Chi tiết tính lại từ tỉ lệ, bản in lấy số đã lưu ⇒ phiếu cũ ERP lệch (PYCTG-03162 Bảo hiểm 0.04%: màn 4,021 /
       in 4,398; tổng 1,958,654 / 1,959,031)
    6. (nhẹ) Không quyền xem: 2 toast trùng “Bạn không có quyền xem yêu cầu tính giá” (danh sách + bộ lọc); ô lọc Thương hiệu / Hãng /
       Người tạo lấy cả YCTG nháp người khác (cùng kiểu N185)

- [x] Màn Phiếu tính giá (Tài chính › Quản lý giá - CTKM › Giá bán › Phiếu tính giá, menu isShow 1663 | 1664 | 1092; lối phụ: nút Tính
  giá ở YCTG, Tạo mới + popup Chọn yêu cầu tính giá, Xem phiếu tính giá ở YCTG, thông báo [PTG]) — 16/10/2026
  - `SRS - Phiếu tính giá.docx` — 15 chức năng (Xem DS · Tìm kiếm lọc · Cài đặt lọc/cột · Lập · Chọn YCTG · Số đầu vào · Tính giá bán ·
    Tạm tính · Sửa · Xem chi tiết · Xoá · Lưu và duyệt · Lưu và gửi duyệt / gửi lại · Xem giá bán mới · In phiếu / In kết quả), 25 BR
    (10 BR GIÁ: BR-06…BR-10, BR-12…BR-15, BR-19), srs_selfcheck khớp bản mẫu + Bước 4 OK (15 = 15 = 15, đánh số liên tục)
  - Phân quyền: XEM cần 1 trong 3 quyền 1663 / 1664 / 1092; Q2 1664 lập (mọi YCTG Chờ tính giá của công ty, không xét phân công) + sửa /
    xoá / Lưu và duyệt / gửi duyệt PTG MÌNH lập; Q3 1092 chỉ che giá vốn CÔNG TY QUẢN LÝ (khối chính sách, popup Tạm tính) — máy chủ
    không trả số; giá nhập kho / giá bán của PTG không che. Phạm vi: nháp chỉ người lập; còn lại cả công ty; công ty khác không thấy
  - `testcase - Phiếu tính giá.xlsx` — 121 TC (15 TC-ROLE), P0 52%, section VI Giá 23 TC. Bộ kiểm thuật ngữ báo 7 “400/404” là báo
    nhầm (số tiền 19,400 / 10,080,400…) — đã soát bằng regex chặt hơn: 0 mã HTTP thật
  - Generator: `gen_srs_phieu-tinh-gia.py`, `gen_testcase_phieu-tinh-gia.py`; ảnh `phieu-tinh-gia_shots/` (Playwright 3031, E2E Assign)
  - Role tạm TMP_SRS_PTG_1664 (id 129858, chỉ 1664 Cty 1) để chụp THẬT nút Tạo mới + popup rỗng — ĐÃ GỠ + cache:forget, đếm roles/rhp/ehr
    về 130/20967/1718. Mọi lệnh ghi bị chặn trên trình duyệt (route.fulfill); PTG Cty 1 vẫn 1:2285 · 3:1, YCTG Cty 1 vẫn 3:4 · 4:2285 · 5:19 · 1:1
  - Dữ liệu THẬT: menu, danh sách 2.285 PTG, lọc (4 trạng thái), cấu hình cột, popup rỗng, PTG-03178 (3 tab, lịch sử, in, in kết quả,
    Xem giá bán mới → PYCHG-04283), PTG-01959 (2 ĐVT), PTG-02618 (TMĐT 2 dòng giá hiệu lực), PTG-00215 nháp người khác → 404, danh sách
    không có Tạo mới khi thiếu 1664. MINH HOẠ (sửa phản hồi trên trình duyệt): popup có YCTG, form Lập (khung dựng từ PTG-01959 thật —
    phép tính thật của màn: 1,61 × 465,360 → 749,200; chi phí khác 34,640 → 500,000; hệ số 1,8 → 900,000, TMĐT 1,170,000), lỗi / xác
    nhận / thành công, công ty bật quy chế duyệt (dev cả 8 công ty tắt), Chờ duyệt giá / Giá bị từ chối (PTG-03170), Đang tạo của mình
    (Sửa / Xóa), chính sách + Tạm tính TPSG có / không 1092 (dev không có chính sách cho hàng công ty khác), chặn chéo, không quyền xem
  - Mục lục docx CHƯA cập nhật số trang (Word đang mở) — chuột phải mục lục → Update Field, hoặc `SRS_UPDATE_TOC=1`
  - Phát hiện khi làm (ứng viên cho `../viec-con-lai.md`, chưa sửa code):
    1. Màn PTG dùng câu của YCTG: thiếu cả 3 quyền → toast “Bạn không có quyền xem yêu cầu tính giá” (đo: 2 toast trùng); nhóm đóng →
       “Nhóm hàng đã đóng, yêu cầu tính giá chỉ còn xem.” (`PriceCalculateAccess` gọi lại `PriceCalculateRequestAccess`)
    2. TMĐT hiện 2 dòng “giá sẽ áp dụng” khi PTG đã lưu giá hiệu lực (máy chủ lưu giá hiệu lực TMĐT suy từ Bán lẻ, FE nạp lại thành dòng
       nhập được + thêm dòng suy ra). Màn Sửa đo: dòng đầu 4 ô nhập MỞ nhưng máy chủ bỏ qua số của loại TMĐT ⇒ sửa mà không ăn. Thấy thật
       ở PTG-02618; mọi PTG HRM lưu có giá hiệu lực Bán lẻ sẽ dính khi mở lại
    3. (giao diện, đo DOM 1440px) Popup Chọn yêu cầu tính giá: bảng 841px trong khung 726px (popup 800px) ⇒ nút Chọn (left 1116) nằm ngoài
       khung (right 1083), phải cuộn ngang mới bấm được; cột Ngày lập bị cắt
    4. Màn Chi tiết + bản in TÍNH LẠI chi phí từ tỉ lệ ⇒ giá nhập kho hiển thị lệch giá vốn đã áp với phiếu ERP cũ (PTG-03178: màn / in
       13,108,667, đã lưu + đã áp 13,108,986; Bảo hiểm 4,147 / 4,466) — cùng gốc N190
    5. (hỏi nghiệp vụ) Giá nhập kho (= giá vốn ghi cho công ty phiếu khi áp) hiện cho mọi người có 1663 / 1664 kể cả thiếu 1092, bản in cũng
       in — chỉ giá vốn công ty QUẢN LÝ được che
    6. (hỏi nghiệp vụ) Lưu và duyệt / gửi duyệt ghi đè “Lý do sửa giá” của ĐVT thành “Phiếu tính giá PTG-x”, mất lý do cũ
    7. Lệch tài liệu: t5-plan ghi xoá PTG người khác “403”, code trả “Trạng thái đã bị thay đổi. Vui lòng load lại trang” (PTG không phải
       nháp) / “Không tìm thấy phiếu tính giá” (nháp); C20 ghi cột Hành động có “Xem” — code không có (bấm số phiếu)
    8. (dữ liệu ERP, không phải lỗi màn) 3.079 dòng giá Bán lẻ của PTG Cty 1 có giá hiệu lực 1 đ / hệ số 0 / ngày 31/12/2026 ⇒ Chi tiết hiện
       “giá sẽ áp dụng” 1 đ
    9. (nhẹ) Ô chọn ngày giá hiệu lực mở đè chữ lỗi “Bắt buộc phải chọn” khi nhảy tới lỗi
    - Đã có sẵn, không ghi lại: N189 (câu lỗi số quá lớn FE / BE lệch)

### Tổng hợp bộ SRS + testcase luồng Chuyển đổi hàng hoá (6 màn — xong 16/10/2026)
| # | Màn | SRS | Testcase | Chức năng | BR | TC (ROLE) | P0 |
|---|---|---|---|---|---|---|---|
| 1 | Hàng hoá nhập thông tin | `SRS - Hàng hoá nhập thông tin.docx` | `testcase - Hàng hoá nhập thông tin.xlsx` | 10 | 25 | 177 | 44% |
| 2 | Cập nhật giá bán | `SRS - Cập nhật giá bán.docx` | `testcase - Cập nhật giá bán.xlsx` | 7 | 24 | 122 (11) | 44% |
| 3 | Duyệt giá bán | `SRS - Duyệt giá bán.docx` | `testcase - Duyệt giá bán.xlsx` | 8 | 22 | 125 (13) | 47% |
| 4 | Yêu cầu hỏi giá | `SRS - Yêu cầu hỏi giá.docx` | `testcase - Yêu cầu hỏi giá.xlsx` | 16 | 22 | 135 (14) | 50% |
| 5 | Yêu cầu tính giá | `SRS - Yêu cầu tính giá.docx` | `testcase - Yêu cầu tính giá.xlsx` | 14 | 20 | 127 (15) | 50% |
| 6 | Phiếu tính giá | `SRS - Phiếu tính giá.docx` | `testcase - Phiếu tính giá.xlsx` | 15 | 25 | 121 (15) | 52% |
| | **Tổng** | 6 file | 6 file | **70** | **138** | **807** | |

Generator: `gen_srs*.py` / `gen_testcase*.py` cùng thư mục; ảnh `*_shots/`. Mọi docx CHƯA cập nhật mục lục (Word đang mở).

### Checkpoint — 2026-10-16 (Phiếu tính giá)
Vừa hoàn thành: SRS + testcase màn Phiếu tính giá (màn 5/5 — hết loạt). Bước tiếp theo: chờ user duyệt; đưa các phát hiện vào
`../viec-con-lai.md` khi user đồng ý; cập nhật mục lục 6 file docx khi Word đóng.

### Checkpoint — 2026-10-16 (YC tính giá)
Vừa hoàn thành: SRS + testcase màn Yêu cầu tính giá (màn 4/5). Bước tiếp theo: PTG.

### Checkpoint — 2026-10-16 (YC hỏi giá)
Vừa hoàn thành: SRS + testcase màn Yêu cầu hỏi giá (màn 3/5). Bước tiếp theo: YCTG → PTG.

### Checkpoint — 2026-10-16 (Duyệt giá bán)
Vừa hoàn thành: SRS + testcase màn Duyệt giá bán (màn 2/5). Bước tiếp theo: YCHG → YCTG → PTG.

### Checkpoint — 2026-10-16 (Cập nhật giá bán)
Vừa hoàn thành: SRS + testcase màn Cập nhật giá bán (màn 1/5 đợt này). Bước tiếp theo: Duyệt giá bán → YCHG → YCTG → PTG.

### Checkpoint — 2026-10-16 (wrap up)
Vừa hoàn thành: SRS + testcase màn Hàng hoá nhập thông tin (thư mục này).
Đang làm dở: không.
Bước tiếp theo: chờ user duyệt nội dung; màn kế tiếp của luồng (đề xuất: Cập nhật giá bán → Duyệt giá bán → YCHG → YCTG → PTG). Muốn ảnh danh sách bằng dữ liệu thật thì cần nhập cây phân loại cho DB dev (B6).
Blocked:
