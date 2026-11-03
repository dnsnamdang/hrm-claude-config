# Nghi lỗi code phát hiện khi xuất tài liệu — CHƯA kiểm, CHƯA sửa

Ghi lại để rà cùng user sau khi xuất xong tài liệu. Mỗi dòng: màn · mô tả · nguồn (agent / TC liên quan).
Kiểm xong ghi kết luận: ✅ lỗi thật (đã sửa / task) · ❌ không phải lỗi · ❓ cần nghiệp vụ chốt.

## Đợt 1 — Danh mục kho (02/11/2026)

| # | Màn | Nghi lỗi | TC / ghi chú | Kết luận |
|---|---|---|---|---|
| 1 | Kho vật lý | Xoá kho đã có nhà kho chỉ ẩn kho (xoá mềm); nhà/dãy/vị trí con vẫn hiện ở màn con vì phạm vi theo công ty không loại kho đã xoá; mã/tên kho đó không dùng lại được | TC_01.007, TC_06.003 | |
| 2 | Kho vật lý | Dev không có kho nào có lịch sử; kho EG_LN có người cập nhật 26/10 mà lịch sử rỗng → kiểm ghi lịch sử khi sửa | | |
| 3 | Kế hoạch kiểm kê theo vị trí, Kiểm kê theo vị trí, Biên bản xử lý thừa thiếu | Form vẫn cho chọn kho đã Khoá, kể cả kho ERP đã xoá | | |
| 4 | Quy chế ↔ YC xuất hàng | Ô "Kho khuyến mại" ở Quy chế lưu id kho VẬT LÝ, YC xuất hàng đọc như id kho KẾ TOÁN | | |
| 5 | Hợp đồng vận chuyển | Popup Cập nhật kho không chặn kho Khoá ở BE; nhiều ô lọc kho liệt kê cả kho ERP đã xoá | | |
| 6 | 7 danh mục kho | Import: FE chặn 500 dòng, BE không gắn giới hạn 500 như danh mục khác (cho tới 1000) | | |
| 7 | Kho vật lý | Cột Hành động trong Tuỳ chỉnh cột bị khoá hẳn (không kéo được), khác màn khác | nhỏ | |
| 8 | Kho kế toán | Import "Nhập xuất thẳng = Có" vẫn lưu Địa chỉ (popup thì bỏ); mã kho vật lý bị bỏ qua không báo | | |
| 9 | Kho kế toán | Ô Kho vật lý cho chọn kho của MỌI công ty (như ERP) — cần chốt | ❓ nghiệp vụ | |
| 10 | Kho kế toán | Mở khoá được khi kho vật lý cha đang khoá | | |
| 11 | Kho kế toán | Popup Xem chi tiết hiện placeholder "Nhập mô tả" ở ô Mô tả trống | nhỏ | |
| 12 | Nhà kho, Khoang | Ô Trạng thái (và Số dãy ở Nhà kho) bị khoá ở popup Sửa nhưng KHÔNG có icon ⓘ | quy ước ô khoá phải có ⓘ | |
| 13 | Nhà kho | Lịch sử `test_123` có mốc "Mở khoá" cùng phút Tạo mới — không thấy đường code sinh ra | dữ liệu cũ? | |
| 14 | Dãy | Tạo mới / Import với Trạng thái = Khoá vẫn lưu, khoang + vị trí sinh kèm lại Hoạt động | TC_04.017 | |
| 15 | Dãy, Khoang, Vị trí | Mở khoá chỉ kiểm cha gần nhất (không kiểm nhà kho / kho) → mở khoá được dưới kho đang khoá | | |
| 16 | Dãy | Dãy Hoạt động dưới nhà kho đã Khoá vẫn Sửa được (dev: D2 thuộc "N10 - Test") | | |
| 17 | Dãy, Vị trí | Cột Ngày tạo / Ngày cập nhật không sắp xếp được (BE có hỗ trợ), khác Kho vật lý | | |
| 18 | Dãy | Xem chi tiết: Số khoang hiện "0", bảng để trống; Import: lỗi "Bị trùng trong file" đứng sau lỗi theo cột | nhỏ | |
| 19 | Khoang | Bộ lọc: chọn Kho → Dãy (bỏ qua Nhà kho) → đổi Kho thì Dãy không reset, bảng rỗng (`handleFilterChange` spaces/index.vue) | TC_02.004, có từ bản cũ | |
| 20 | Khoang | Mã có khoảng trắng đầu/cuối báo đỏ ở FE, BE thì tự cắt | | |
| 21 | Khoang | Kho / nhà kho cha bị khoá mà câu báo vẫn là "Dãy "<tên>" đã bị khóa…" | | |
| 22 | Khoang | Câu "Không thể khóa khoang khi vẫn còn danh mục con đang hoạt động." — nên nói "vị trí" | | |
| 23 | Vị trí | Vị trí cũ có mã chứa khoảng trắng / chữ có dấu không Sửa được gì (Sửa vẫn kiểm luật mã mới) | TC_04.018 | |
| 24 | Vị trí | File mẫu Import: dòng hướng dẫn cột Loại vị trí lệch câu chữ các cột khác | nhỏ | |
| 25 | Kiện | Thứ tự "007" bị báo "Nhập số nguyên lớn hơn 0" (đã thấy ở Validate Import trên dev) | TC_10.008 sẽ Failed | |
| 26 | Kiện | Sửa Thứ tự kiện đã gắn lô hàng xuất kho → đổi tên kiện, lô giữ tên cũ (code ghi là chủ đích) | BR-04 | |

## Đợt 2 — Báo cáo (02/11/2026)

| # | Màn | Nghi lỗi | TC / ghi chú | Kết luận |
|---|---|---|---|---|
| 27 | Hàng có thể bán theo CT | Popup Hàng đang về: link PNK-… mở sang ERP dù HRM đã có `/finance/warehouse-imports/{id}` (`utils/stock-voucher-link.js`) | PU-003 | |
| 28 | Hàng có thể bán theo CT | Bỏ trống ô Kho → vẫn cộng kho vật lý đang khoá (vd HN-KNXT) dù ô Kho không cho chọn kho đó | F-002, F-003 | |
| 29 | Hàng có thể bán theo CT | Hàng đang về cộng SL theo ĐVT trên chứng từ, không quy đổi về ĐVT cơ bản (ERP cũng vậy) → hàng đặt theo thùng/hộp sai số | SL-008, PU-005 | |
| 30 | Hàng có thể bán theo CT | Ẩn nhóm "Theo từng kho" rồi xuất Excel → file mất cột kho dù trường vẫn tích; popup Xuất luôn tích đủ 16 trường, không theo cột đang hiện | EX-006, EX-001 | |
| 31 | Hàng có thể bán theo CT | Tuỳ chỉnh cột ghi "kéo ☰ để đổi thứ tự" nhưng thứ tự cột cố định | COT-001, nhỏ | |
| 32 | Hàng có thể bán theo CT | Popup có dòng SL = 0 (vd PDNNK-08411): 3 nguồn nhập kho không lọc SL > 0 | PU-001 | |
| 33 | Hàng có thể bán theo CT | Ô Hàng hoá chỉ tìm hàng công ty đang làm việc kể cả khi lọc công ty khác | F-008 | |
| 34 | Hàng có thể bán theo CT | Không phân quyền: ai đăng nhập cũng xem số mọi công ty + xuất Excel (đã chốt 02/10 — xác nhận lại) | Q-02, ❓ | |
| 35 | CP vận chuyển theo NVKD | Lọc "Hợp đồng" bỏ sót chuyến (vd TPHP_HTCXK_00411 có HĐ trên cột, lọc đúng mã ra 0; "HĐ" sót 16 chuyến) — còn bắt HĐ trên bút toán phải khớp | TC_02.015–016, BR-05 | |
| 36 | CP vận chuyển theo NVKD | Lọc "Đối tượng chịu phí" mất hẳn 140 chuyến không có YC xuất hàng (~320,2 tr); vẫn tính cước nguyên chuyến, không tách theo đối tượng | TC_02.017, ❓ | |
| 37 | CP vận chuyển theo NVKD | Xuất Excel lấy cả chữ đã gõ mà chưa Enter → file lệch màn (suy từ code) | TC_06.011 | |
| 38 | CP vận chuyển theo NVKD | Excel gộp 2 phòng trùng tên (gom theo tên, không theo mã) | nhỏ | |
| 39 | Đối chiếu công nợ 1 KH | API popup hàng hoá theo mã phiếu KHÔNG kiểm phạm vi quyền — đoán mã là xem được | TC-ROLE-07, TC_05.001 | |
| 40 | Đối chiếu công nợ 1 KH | Số dư cuối kỳ dòng HĐ không trừ ĐCCN giảm → cộng dòng HĐ ≠ Tổng cộng (code: giữ y ERP) | TC_03.004, TC_04.006–007 | |
| 41 | Đối chiếu công nợ 1 KH | Dòng chứng từ lấy 3 TK cố định không lọc theo KH, dòng HĐ lấy 131 + TK con → có thể lệch | TC_03.001, TC_03.005 | |
| 42 | Đối chiếu công nợ 1 KH | Đầu kỳ lọc Công ty/Phòng/Bộ phận theo bút toán, phát sinh lọc theo hồ sơ hiện tại người tạo HĐ → Tổng cộng lệch khi dùng ô lọc này | TC_02.014–015 | |
| 43 | Đối chiếu công nợ 1 KH | Tìm nhanh so cả chứng từ trước kỳ → giữ HĐ không có chứng từ khớp | TC_02.011 | |
| 44 | Đối chiếu / Tổng hợp theo NV | Ô 0 ở Tổng cộng: màn in "0", Excel/bản in để trống; tooltip ⓘ nhắc chữ "ERP" | TC_06.006–007, TC_01.004 | |
| 45 | Đối chiếu công nợ 1 KH | Bản in: số HĐ dài tràn sang ô bên | TC_06.007, nhỏ | |
| 46 | Tổng hợp CN theo NV, Chi tiết CN KH | Xuất Excel kỳ 1 tháng không lọc thêm → dev 502 sau ~7–8s (lọc thêm thì xuất được) | TC_VI.004, X-007 | |
| 47 | Tổng hợp CN theo NV | Cột Khách hàng trống nhiều dòng HĐ (mã KH 13703, 18575, 2288 không có trong danh mục KH) | TC_III.001 — dữ liệu? | |
| 48 | Tổng hợp CN theo NV | Số dư đầu kỳ dòng Tổng cộng bỏ qua tìm nhanh (HRM thêm), Số dư cuối kỳ, Ngày nghiệm thu; ô Số HĐ: dòng khớp đúng, đầu kỳ Tổng cộng tìm gần đúng | TC_III.006, TC_II.006, TC_II.009 | |
| 49 | Tổng hợp CN theo NV, Chi tiết CN KH | Liệt kê cả HĐ không phát sinh trong kỳ (25,302 dòng, phần lớn toàn 0) — màn Đối chiếu đã bỏ loại này | TC_III.010, S-008, ❓ | |
| 50 | Tổng hợp CN theo NV | Mẫu in không có cột Trả lại tiền thừa → "còn nợ cuối kỳ" không khớp công thức khi có phiếu chi trả khách | TC_V.008 | |
| 51 | Chi tiết CN KH | Popup dòng khách không áp lọc Số dư cuối kỳ + tìm nhanh → lệch số vừa bấm (dev 89THUPTR-62: 1,380,623,222 vs 1,595,658,222) | O-008 | |
| 52 | Chi tiết CN KH | Popup ĐCCN gồm cả khai báo đầu kỳ NCC + phiếu thu; popup Hàng hoá tính cả bên Có khai báo đầu kỳ (giữ y ERP) | O-009, BR-07 | |
| 53 | Chi tiết CN KH | Lọc Số HĐ: đầu kỳ lấy HĐ chứa chuỗi, cột khác khớp đúng; Tổng cộng không áp Dư nợ/Dư có + tìm nhanh (giữ y ERP) | S-007, L-006 | |

## Đợt 3 — Phiếu nghiệp vụ (02/11/2026)

| # | Màn | Nghi lỗi | TC / ghi chú | Kết luận |
|---|---|---|---|---|
| 54 | Khai báo đầu kỳ công nợ | Popup "Chọn hợp đồng" đánh "Đã khai báo" theo HỢP ĐỒNG bất kể tài khoản → form không khai được cùng HĐ với TK thứ 2 (quy tắc trùng là HĐ + TK; import thì làm được) | TC_04.004, TC_05.004 | |
| 55 | Khai báo đầu kỳ công nợ | Lọc popup ghi "Hợp đồng/Đơn hàng thúc đẩy bán" nhưng cột trên dòng hiện "… thanh lý" | TC_04.007 sẽ Failed | |
| 56 | Khai báo đầu kỳ công nợ | Ô lọc Loại hợp đồng có 2 dòng cùng tên "Hợp đồng mua trong nước" (2 loại khác nhau) | TC_02.004 | |
| 57 | Khai báo đầu kỳ công nợ | Không khai báo nào trên dev có lịch sử, kể cả mã EG.CNĐKHĐ.00001/00002 (HRM sinh 12–16/10) → kiểm ghi "Tạo mới" | TC_05.006 | |
| 58 | Khai báo đầu kỳ công nợ | Tiền tố mã đổi "ETEK GREEN" → "EG" và đánh số lại từ 00001 khi mã công ty đổi | BR-03, TC_10.001 | |
| 59 | Khai báo đầu kỳ công nợ | Xuất Excel khi rỗng không tải file (checklist TPE: rỗng vẫn xuất logo + tên cột) | TC_08.004 | |
| 60 | Khai báo đầu kỳ công nợ | File mẫu import có 2 dòng ví dụ giống hệt → nạp nguyên file mẫu báo trùng | TC_07.001 | |
| 61 | Khai báo đầu kỳ công nợ | Ô Khách hàng tìm cả SĐT nhưng placeholder chỉ ghi mã/tên; Công nợ trống FE không chặn, BE mới báo | TC_04.003, TC_09.003, nhỏ | |
| 62 | Khai báo đầu kỳ CN NCC | Trang Thêm: ô Loại tiền, Loại dư, Tài khoản quá hẹp, giá trị bị cắt "U…", "D…" | TC_04.009, TC_04.016 | |
| 63 | Khai báo đầu kỳ CN NCC | Import: Loại tiền sai mã báo thêm "Tỷ giá – Bắt buộc phải nhập" (1 lỗi gốc ra 2 câu) | TC_07.002 | |
| 64 | Khai báo đầu kỳ CN NCC | Tiền tố mã + Ngày tính công nợ theo công ty người đăng nhập, tổ chức khai báo theo người lập HĐ → có thể lệch công ty | TC_04.007, TC_04.009 | |
| 65 | Phiếu huỷ hàng giữ KT | Trang Thêm: tên KH dài làm bảng Chi tiết tràn, đẩy cột ĐVT + nút xoá ra ngoài | TC_IV.017 | |
| 66 | Phiếu huỷ hàng giữ KT | Chi tiết: ô Ghi chú trống hiện placeholder "Nhập ghi chú" | TC_IX.008, nhỏ | |
| 67 | Phiếu huỷ hàng giữ KT | Không quyền vẫn mở được trang Thêm bằng đường dẫn (chỉ chặn khi tải dữ liệu) | TC-ROLE-04 | |
| 68 | Phiếu huỷ hàng giữ KT | Nhân viên hiển thị 3 kiểu khác nhau (Thêm / Chi tiết / danh sách) — trái khuôn "Tên - Mã phòng - Mã NV" | nhỏ | |
| 69 | Phiếu huỷ hàng giữ KT | Bản in DS: "Ngày lập/Người lập" ≠ màn "Ngày tạo/Người tạo", 5 cột cố định, không giới hạn dòng (661); "huỷ"/"hủy" lẫn lộn | TC_XII.005 | |
| 70 | Phiếu huỷ hàng giữ KT | Nhân viên bị huỷ hàng nhận thông báo nhưng không mở được phiếu nếu thiếu quyền "Quản lý giữ hàng" | TC_XI.003, ❓ | |
| 71 | Khai báo tồn kho đầu kỳ | Xuất Excel cột "Người nhập/Ngày nhập" ≠ danh sách "Người tạo/Ngày tạo" | TC_08.001 | |
| 72 | Khai báo tồn kho đầu kỳ | Form Thêm: ô Kho chỉ nạp kho công ty đang làm việc, đổi Công ty không nạp lại → bị chặn "Kho không thuộc công ty đã chọn" | TC_04.002, TC_04.016 | |
| 73 | Khai báo tồn kho đầu kỳ | Nút "Chọn hàng hóa" bị làm mờ thay vì ẩn | TC_04.001 | |
| 74 | Khai báo tồn kho đầu kỳ | Import khớp hàng theo cả mã + tên → thiếu tên ra 2 lỗi "Thiếu Tên hàng" + "Hàng hóa không tồn tại" | TC_07.002 | |
| 75 | Phiếu nhập kho | Ai đăng nhập cũng mở + lưu nhóm Phiếu xếp hàng của phiếu người khác (chỉ xét trạng thái) | TC_05.001 | |
| 76 | Phiếu nhập kho | Phiếu nhập hàng đổi PNK sang Đang/Đã hạch toán không ghi lịch sử PNK (dev PNK-11604 lịch sử rỗng) | TC_08.001, TC_09.004 | |
| 77 | Phiếu nhập kho | Xuất Excel rỗng vẫn tải file + báo thành công; bản in SL chẵn in "9.00"; nút Tạo mới hiện cả với người không phải thủ kho | TC_09.003, TC_09.001, TC_04.002 | |
| 78 | Phiếu nhập kho | Chưa thấy code đưa PNK về Chờ duyệt khi phiếu nhập hàng bị xoá/huỷ | ❓ nghiệp vụ | |
| 79 | Phiếu điều chuyển hàng | Hộp "Thông tin chưa lưu" KHÔNG BAO GIỜ hiện ở Thêm/Sửa: `ProductTransferForm.vue` gọi `markFormSaved()` lúc mở + mixin đọc `formSubmit` (form tên `form`) — đã thử trên dev | TC_04.011 | |
| 80 | Phiếu điều chuyển hàng | Quản trị mở được phiếu Đang tạo của người khác bằng đường dẫn (DS và chi tiết xét quyền khác nhau) | TC-ROLE-04/05 | |
| 81 | Phiếu điều chuyển hàng | Ô Công ty/Phòng ban/Bộ phận hiện với mọi người (cờ quyền gán cứng) — BE vẫn giới hạn | TC_02.007 | |
| 82 | Phiếu điều chuyển hàng | Kho xuất không có tồn kế toán → duyệt báo lỗi 500 chung, không chỉ dòng hàng | TC_06 | |
| 83 | Yêu cầu mua dịch vụ | Ô tìm nhanh "Tìm theo số phiếu" không lọc (BE không xử lý) — đã thử dev: vẫn 103/103 | TC II-001 | |
| 84 | Yêu cầu mua dịch vụ | Sắp xếp Ngày cập nhật không đổi thứ tự (BE không nhận cột) | TC III-002 | |
| 85 | Yêu cầu mua dịch vụ | Hộp "Thông tin chưa lưu" không hiện ở Tạo/Sửa (cùng nguyên nhân #79) — đã thử dev | TC IV-013 | |
| 86 | Yêu cầu mua dịch vụ | Ban KS duyệt giá không nhập được Giá duyệt + lưu phiếu không gửi giá duyệt → Giá duyệt/Thành tiền duyệt = 0 (suy từ code) | TC VI-004 | |
| 87 | Yêu cầu mua dịch vụ | Gửi duyệt nhận SL + Giá đề xuất = 0 (phiếu 0 đồng); in phiếu chỉ có cột giá duyệt khi Đã duyệt; in DS 9 cột cố định | TC IV-005, TC VII-002 | |

## Phát hiện khi làm lại testcase (03/11/2026)

| # | Màn | Nghi lỗi / điểm cần QA xác nhận | TC / ghi chú | Kết luận |
|---|---|---|---|---|
| 88 | Nhiều màn (danh mục kho, báo cáo, phiếu) | GHI NHỚ BỘ LỌC: TC cũ ghi "rời màn quay lại trong 10 phút vẫn giữ bộ lọc"; agent đọc code thấy rời sang màn khác là xoá bộ lọc (chỉ giữ khi vào trang chi tiết riêng; báo cáo: tab mới trong 10 phút thì giữ) → TC mới viết theo code, CHƯA thử trình duyệt. Khai báo đầu kỳ: phần lưu bộ lọc nằm trong component con, nghi không chạy khi vào chi tiết rồi quay lại | nhóm TÌM KIẾM & LỌC mục "Lưu trạng thái" | ❓ |
| 89 | 7 danh mục kho | "Mở khoá bản ghi đã bị người khác xoá" — nghi hiện câu tiếng Anh "Item Not Found!" | nhóm KHÓA / MỞ KHÓA | |
| 90 | Khai báo đầu kỳ công nợ | Đang sửa thì phát sinh chứng từ: câu báo "Khai báo đã phát sinh chứng từ, không được sửa." dưới ô Tài khoản (TC cũ ghi nhầm câu của Xoá) | đã sửa TC | |
