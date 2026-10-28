# -*- coding: utf-8 -*-
"""Huong dan luong + cach kiem tang/giam so lieu tren bao cao cho 3 man ERP:
Phieu nhap kho dieu chinh kiem ke, Phieu nhap kho cho bao thua thieu, Phieu bao hang thua thieu nhap kho.

Noi dung lay tu 3 bo testcase cung cap thu muc erp/.plans (section Chuan bi du lieu + Tang/giam bao cao).
Chay: python gen_word.py  ->  Huong dan kiem so lieu - 3 man nhap kho.docx
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "_hdsd_van_xuoi"))
from hdsd_van_xuoi import HdsdVanXuoi, cap_nhat_truong  # noqa: E402

OUT = os.path.join(HERE, "Huong dan kiem so lieu - 3 man nhap kho.docx")

M_THE_KHO = "Kho > Báo cáo kho > Thẻ kho"
M_XNT = "Kho > Báo cáo kho > Tổng hợp xuất nhập tồn"
M_TON_KHO = "Kho > Báo cáo kho > Báo cáo tồn theo kho"
M_TON_TH = "Kho > Báo cáo kho > Báo cáo tồn kho tổng hợp theo mặt hàng"
M_XNT_KT = "Kế toán > Hàng hoá - Dịch vụ - Vận chuyển > Báo cáo hàng tồn kho > Tổng hợp xuất nhập tồn"
M_KK = "Kho > Kiểm kho > Kiểm kê theo hàng hóa"
M_PNKDC = "Kho > Nhập kho > Phiếu nhập kho điều chỉnh kiểm kê"
M_CHO = "Kho > Nhập kho > Phiếu nhập kho chờ báo thừa, thiếu"
M_BAO = "Kho > Nhập kho > Phiếu báo hàng thừa, thiếu nhập kho"

d = HdsdVanXuoi("Kiểm tra số liệu 3 màn nhập kho")

# =====================================================================
d.h1("TỔNG QUAN")
d.h2("1. Mục đích tài liệu")
d.p("Tài liệu hướng dẫn tester đi đúng luồng để có dữ liệu test và cách kiểm số liệu tăng, giảm trên các báo cáo "
    "kho của ERP cho 3 màn:")
d.bullet("Phiếu nhập kho điều chỉnh kiểm kê: ", "nhập hàng THỪA phát hiện khi kiểm kê, có cộng tồn kho.")
d.bullet("Phiếu nhập kho chờ báo thừa, thiếu: ", "danh sách phiếu nhập kho mua hàng có số thực nhập khác số đề nghị, "
         "đang chờ lập phiếu báo. Màn chỉ để xem, không ghi số liệu.")
d.bullet("Phiếu báo hàng thừa, thiếu nhập kho: ", "phiếu báo lệch số cho phiếu nhập kho ở màn trên, gửi người duyệt "
         "xử lý. Phiếu báo KHÔNG làm thay đổi tồn kho.")
d.p("Mỗi màn có bộ testcase riêng (file Excel). Tài liệu này gom phần dùng chung: luồng tạo dữ liệu, cách ghi số và "
    "đối chiếu báo cáo, các lỗi ERP thường gặp khi kiểm số.")

d.h2("2. Nguyên tắc kiểm tăng, giảm số liệu")
d.p("Mọi phép kiểm số đi theo đúng 3 bước:")
d.table([
    ["Bước", "Việc làm", "Lưu ý"],
    ["1. Ghi số nền", "Mở báo cáo, chọn bộ lọc (kho, hàng, công ty, khoảng ngày), bấm tìm và ghi lại số ở cột cần "
     "kiểm vào bảng ghi số (Phần 3).", "Chụp màn hình kèm bộ lọc để đối chiếu về sau."],
    ["2. Thao tác", "Thực hiện đúng 1 thao tác trên phiếu với số lượng cụ thể (ví dụ Gửi duyệt phiếu có H1 thừa 3 Cái).",
     "Không làm thêm phiếu khác của cùng hàng, cùng kho trong lúc kiểm."],
    ["3. So sánh", "Mở lại báo cáo với ĐÚNG bộ lọc ở bước 1, so với số nền.", "Kết quả = số nền cộng / trừ đúng số "
     "lượng của thao tác, đúng cột."],
], widths=[1.2, 3.2, 2.1])
d.note("Đơn vị tính: ", "báo cáo kho tính theo ĐƠN VỊ CƠ BẢN của hàng. Hàng có đơn vị quy đổi (ví dụ 1 Thùng = 24 Chai) "
       "thì nhập 2 Thùng phải tăng 48 Chai. Nên chọn ít nhất 1 hàng có hệ số quy đổi lớn hơn 1 để bắt lỗi quy đổi.")
d.note("Ngày ghi số: ", "số được ghi vào ngày thực hiện thao tác (ngày Gửi duyệt, ngày gửi phiếu nhập kho), không theo "
       "ngày kiểm kê hay ngày đề nghị. Khi lọc theo khoảng ngày phải bao gồm ngày hôm nay.")
d.note("Kho dùng chung: ", "môi trường dev có nhiều người cùng test. Nên chọn hàng ít giao dịch và kiểm ngay sau thao "
       "tác; nếu số lệch, mở Thẻ kho xem có chứng từ lạ của người khác chen vào không.")

d.h2("3. Các báo cáo dùng để kiểm")
d.table([
    ["Báo cáo", "Đường dẫn menu", "Cột kiểm", "Thay đổi khi nào"],
    ["Thẻ kho", M_THE_KHO, "Từng dòng chứng từ: Nhập, Xuất, Lô, Vị trí; SL tồn cuối",
     "Khi hàng thực sự vào / ra kho vật lý. Mỗi phiếu là 1 dòng chứng từ."],
    ["Tổng hợp xuất nhập tồn (kho)", M_XNT, "Tồn đầu kỳ, Nhập trong kỳ, Xuất trong kỳ, Tồn cuối kỳ",
     "Cùng lúc với Thẻ kho."],
    ["Báo cáo tồn theo kho", M_TON_KHO, "SL tồn", "Cùng lúc với Thẻ kho (riêng hàng quy đổi có lỗi, xem mục 1.4)."],
    ["Báo cáo tồn kho tổng hợp theo mặt hàng", M_TON_TH, "SL tồn", "Cùng lúc với Thẻ kho."],
    ["Tổng hợp xuất nhập tồn (kế toán)", M_XNT_KT, "SL Nhập trong kỳ", "Chỉ khi KẾ TOÁN hạch toán (Lưu và duyệt), "
     "không đổi lúc thủ kho gửi phiếu."],
], widths=[1.4, 2.1, 1.5, 1.5])
d.p("Phân biệt quan trọng: tồn kho VẬT LÝ (4 báo cáo đầu, menu Kho) đổi ngay khi thủ kho gửi phiếu; tồn kho KẾ TOÁN "
    "(báo cáo cuối, menu Kế toán) chỉ đổi khi kế toán duyệt hạch toán.")

d.h2("4. Tài khoản cần chuẩn bị")
d.table([
    ["Tài khoản", "Vai trò", "Quyền cần gán"],
    ["TK", "Thủ kho, người kiểm kê, người lập phiếu", "Thủ kho; Xử lý phiếu kiểm kê hàng hóa; Tạo phiếu báo hàng thừa, "
     "thiếu nhập kho; Xem xử lý thừa thiếu nhập kho theo công ty; Xem phiếu nhập kho điều chỉnh kiểm kê - theo công ty; "
     "Xem báo cáo tồn kho theo công ty"],
    ["KT", "Kế toán kho", "Kế toán kho; Xem báo cáo tồn kho kế toán theo công ty"],
    ["BKS", "Ban kiểm soát", "Ban kiểm soát duyệt kết quả kiểm kê"],
    ["DUYET", "Người duyệt phiếu báo", "Duyệt phiếu báo hàng thừa, thiếu nhập kho; Tạo xử lý hàng thiếu nhập kho"],
], widths=[1.0, 1.9, 3.6])
d.note("Lưu ý: ", "cả 4 tài khoản cùng thuộc 1 công ty (ví dụ TPE). Gán quyền xong phải đăng xuất và đăng nhập lại.")

# =====================================================================
d.h1("PHẦN 1: PHIẾU NHẬP KHO ĐIỀU CHỈNH KIỂM KÊ")
d.h2("1.1. Luồng nghiệp vụ")
d.p("Phiếu này không tạo tay từ danh sách (nút Tạo mới mở trang trống). Phiếu chỉ sinh ra từ một phiếu kiểm kê có hàng "
    "THỪA, theo luồng sau:")
d.table([
    ["Bước", "Ai", "Ở đâu", "Thao tác", "Kết quả"],
    ["1", "TK", M_KK, "Tạo mới: chọn Ngày kiểm kê, Kho, Công ty thuê kho, thêm hàng + vị trí + lô, thêm thành viên, "
     "bấm 'Lưu & gửi'", "Phiếu kiểm kê 'Đang kiểm'"],
    ["2", "TK", "Như trên, bánh răng > 'Cập nhật kết quả'", "Nhập Thực kiểm LỚN HƠN tồn hệ thống, đính file kết quả, "
     "bấm 'Gửi duyệt'", "Phiếu kiểm kê 'Chờ KT duyệt'"],
    ["3", "BKS", "Như trên, bánh răng > 'Duyệt'", "Bấm 'Duyệt'", "Có chênh lệch: 'Chờ xử lý'. Không chênh lệch: "
     "'Hoàn thành' (không lập phiếu nhập được)"],
    ["4", "TK", "Như trên, bánh răng > 'Xử lý'", "Bấm 'Tạo phiếu nhập kho điều chuyển'", "Mở trang lập phiếu, bảng "
     "Chi tiết tự nạp các dòng thừa, số lượng không sửa được"],
    ["5", "TK", "Trang lập phiếu", "Nhập Ghi chú, đính kèm file (bắt buộc), bấm 'Lưu' hoặc 'Gửi duyệt'",
     "'Lưu': phiếu 'Đang tạo', CHƯA cộng tồn. 'Gửi duyệt': phiếu 'Chờ duyệt', CỘNG TỒN KHO VẬT LÝ NGAY, sinh lô "
     "'NHAPDIEUCHINH-'"],
    ["6", "KT", "Chờ duyệt > Hàng hóa - dịch vụ - vận chuyển > Nhập hàng > Phiếu nhập kho điều chỉnh kiểm kê chờ duyệt",
     "Bấm 'Tạo phiếu nhập hàng', rồi 'Lưu' hoặc 'Lưu và duyệt'", "'Lưu': 'Đang hạch toán'. 'Lưu và duyệt': "
     "'Đã hạch toán', CỘNG TỒN KHO KẾ TOÁN"],
], widths=[0.6, 0.7, 1.5, 1.9, 1.8])
d.note("Ghi nhận hành vi ERP: ", "màn không có Xóa, Hủy hay Không duyệt. Đã Gửi duyệt thì số tồn không tự giảm lại; "
       "muốn trả số phải lập phiếu xuất ở màn khác.")

d.h2("1.2. Chuẩn bị dữ liệu")
d.p("Chọn 4 hàng đang có tồn tại cùng một kho (ví dụ kho LN), không có phiếu nhập / xuất dở dang. Có thể xem tồn trên "
    "Thẻ kho, hoặc nhờ người hỗ trợ chạy câu truy vấn số 3 trong thư mục bộ testcase của màn này.")
d.table([
    ["Hàng", "Đặc điểm", "Kết quả kiểm kê cần nhập", "Dùng để kiểm"],
    ["H1", "Đơn vị Cái, hệ số 1", "Thực kiểm = tồn + 3 (thừa 3)", "Tăng 3 Cái trên mọi báo cáo kho"],
    ["H2", "Có đơn vị Thùng = 24 Chai", "Kiểm theo Thùng, thừa 2 Thùng", "Tăng 48 Chai (bắt lỗi quy đổi)"],
    ["H3", "Có ở 2 vị trí V1, V2", "V1 thừa 4, V2 thiếu 4 (tổng bằng 0)", "Không vào phiếu nhập, số không đổi"],
    ["H4", "Bất kỳ", "Thiếu 2", "Không vào phiếu nhập (đi phiếu xuất điều chỉnh)"],
], widths=[0.6, 1.6, 2.2, 2.1])
d.p("Trên dev có thể đã có sẵn phiếu kiểm kê ở trạng thái 'Chờ xử lý' còn hàng thừa: nhờ người hỗ trợ chạy câu truy vấn "
    "số 1. Dữ liệu local khi khảo sát không có phiếu nào như vậy, nên nhiều khả năng phải tự đi luồng ở mục 1.1.")

d.h2("1.3. Kiểm tăng, giảm trên báo cáo")
d.p("Ví dụ dưới đây dùng phiếu P2 lập từ phiếu kiểm kê ở mục 1.2: H1 thừa 3 Cái, H2 thừa 2 Thùng (48 Chai), kho LN, "
    "công ty TPE.")
d.table([
    ["Thao tác", "Báo cáo", "Kỳ vọng so với số nền"],
    ["TK bấm 'Lưu' (nháp)", "Cả 4 báo cáo kho", "Không đổi. Thẻ kho không có dòng của phiếu nháp"],
    ["TK bấm 'Gửi duyệt' P2", "Thẻ kho", "Thêm 1 dòng chứng từ số phiếu P2, ngày hôm nay, Lô 'NHAPDIEUCHINH-', "
     "cột Nhập: H1 +3, H2 +48 Chai"],
    ["", "Tổng hợp xuất nhập tồn (kho)", "Nhập trong kỳ và Tồn cuối kỳ: H1 +3, H2 +48. Tồn đầu kỳ, Xuất trong kỳ "
     "không đổi"],
    ["", "Báo cáo tồn theo kho", "SL tồn: H1 +3, H2 +48 (thực tế ERP chỉ +2, lỗi)"],
    ["", "Tổng hợp xuất nhập tồn (kế toán)", "Không đổi"],
    ["", "H3 trên mọi báo cáo", "Không đổi"],
    ["KT bấm 'Lưu' phiếu nhập hàng", "Tổng hợp xuất nhập tồn (kế toán)", "Không đổi"],
    ["KT bấm 'Lưu và duyệt'", "Tổng hợp xuất nhập tồn (kế toán)", "SL Nhập trong kỳ: H1 +3, H2 +48"],
    ["", "Thẻ kho, Tổng hợp xuất nhập tồn (kho)", "Không đổi thêm (không bị cộng lần 2)"],
], widths=[1.7, 2.0, 2.8])
d.note("Kiểm ngày ghi số: ", "lọc Tổng hợp xuất nhập tồn (kho) theo tháng của ngày kiểm kê (nếu khác tháng) sẽ KHÔNG "
       "thấy số của P2; lọc tháng hiện tại mới thấy.")

d.h2("1.4. Lỗi ERP đã biết khi kiểm số")
d.bullet("Báo cáo tồn theo kho không quy đổi: ", "H2 nhập 2 Thùng chỉ tăng 2, trong khi Thẻ kho và Tổng hợp xuất nhập "
         "tồn tăng 48. Ghi Failed ở TC tương ứng.")
d.bullet("Hai tab cùng lập từ 1 phiếu kiểm kê: ", "ra 2 phiếu, tồn bị cộng 2 lần (Thẻ kho có 2 dòng, Nhập tăng 6).")
d.bullet("Phiếu kiểm kê nhiều kho: ", "chỉ lập được phiếu nhập cho 1 kho, kho còn lại không lập được, phiếu kiểm kê "
         "kẹt ở 'Đang xử lý'.")
d.bullet("Bộ lọc danh sách: ", "các ô Kho, mã hàng, tên hàng, Từ ngày, Đến ngày không có tác dụng.")

# =====================================================================
d.h1("PHẦN 2: CHỜ BÁO THỪA, THIẾU VÀ PHIẾU BÁO HÀNG THỪA, THIẾU")
d.h2("2.1. Luồng nghiệp vụ")
d.p("Hai màn này đi liền nhau. Một phiếu nhập kho vào danh sách 'chờ báo' khi đủ cả 4 điều kiện:")
d.bullet("Trạng thái 'Đã hạch toán'.", None)
d.bullet("Là loại nhập MUA: mua nước ngoài, mua ngoài, mua nước ngoài (mới), mua trong nước, mua trong nước (HĐNT), "
         "mua trong nước (TỰ DO + HÃNG).", None)
d.bullet("Có ít nhất 1 dòng SL thực nhập khác SL đề nghị (thiếu hoặc thừa đều tính).", None)
d.bullet("Chưa có phiếu báo nào gắn với phiếu nhập kho đó, ở bất kỳ trạng thái nào.", None)
d.table([
    ["Bước", "Ai", "Ở đâu", "Thao tác", "Kết quả"],
    ["1", "Kinh doanh / mua hàng", "Kế toán > Hàng hoá - Dịch vụ - Vận chuyển > Nhập hàng > Yêu cầu nhập hàng",
     "Tạo yêu cầu loại mua trong nước, H1 SL 10, kho nhận LN, đi hết luồng duyệt", "Sinh phiếu đề nghị nhập kho"],
    ["2", "TK", "Kho > Nhập kho > Phiếu đề nghị nhập kho, bánh răng > 'Tạo phiếu nhập kho'",
     "Chọn vị trí, nhập SL thực nhập 8 (lệch với 10), gửi phiếu", "Phiếu nhập kho P1 'Chờ duyệt'. Tồn kho vật lý "
     "tăng 8 NGAY LÚC NÀY. P1 chưa vào danh sách chờ báo"],
    ["3", "KT", "Kho > Nhập kho > Phiếu nhập kho, bánh răng > 'Tạo phiếu nhập hàng'", "Hoàn tất phân bổ, bấm "
     "'Lưu & Duyệt'", "P1 'Đã hạch toán', xuất hiện ở màn chờ báo"],
    ["4", "TK", M_CHO + ", bánh răng > 'Báo hàng thừa thiếu'", "Nhập Diễn giải, đính kèm file (bắt buộc), bấm 'Lưu' "
     "hoặc 'Lưu & gửi'", "'Lưu': 'Đang tạo'. 'Lưu & gửi': 'Chờ xử lý', gửi thông báo người duyệt. P1 rời màn chờ báo"],
    ["5", "DUYET", "Trang chủ, tab 'Phê duyệt', ô 'Phiếu báo thừa - thiếu nhập kho cần xử lý'", "Bấm 'Không duyệt' "
     "(bắt buộc ghi chú) hoặc 'Xử lý'", "'Không duyệt': người lập sửa rồi gửi lại. 'Xử lý': mở trang lập Phiếu xử lý "
     "hàng thiếu nhập kho, lưu xong phiếu báo thành 'Đã xử lý'"],
], widths=[0.6, 0.85, 1.75, 1.65, 1.65])
d.note("Ghi nhận hành vi ERP: ", "phiếu báo chỉ có hàng THỪA không lập được phiếu xử lý (ERP chưa có luồng xử lý hàng "
       "thừa), nên đứng mãi ở 'Chờ xử lý'.")

d.h2("2.2. Chuẩn bị dữ liệu")
d.p("Cách nhanh: nhờ người hỗ trợ chạy câu truy vấn số 1 trong thư mục bộ testcase màn Phiếu báo hàng thừa, thiếu. Kết "
    "quả là các phiếu nhập kho đang chờ báo, kèm số dòng thiếu / thừa. Khi khảo sát dữ liệu local có 15 phiếu như vậy "
    "(công ty TPE, kho LN và PTT, ví dụ PNK-08334). Mở màn chờ báo, gõ số phiếu để chắc chắn phiếu có hiện.")
d.p("Nếu cần tự tạo, đi luồng mục 2.1 để có bộ phiếu sau:")
d.table([
    ["Phiếu", "Cách tạo", "Dùng để"],
    ["P1", "H1 đề nghị 10, thực nhập 8, hạch toán", "Phiếu THIẾU, đi trọn luồng báo và xử lý"],
    ["P2", "H2 đề nghị 5, thực nhập 7, hạch toán", "Phiếu THỪA"],
    ["P3", "H1 đề nghị 10, nhập đủ 10, hạch toán", "Đối chứng: KHÔNG vào màn chờ báo"],
    ["P4", "Loại 'Nhập hàng bán trả lại', có lệch", "Đối chứng: không phải nhập mua nên KHÔNG vào màn chờ báo"],
    ["P5", "Có lệch nhưng kế toán chỉ bấm 'Lưu'", "Đối chứng: chưa hạch toán nên chưa vào màn chờ báo"],
], widths=[0.7, 2.9, 2.9])
d.note("Dùng lại phiếu: ", "phiếu nhập kho đã có phiếu báo sẽ rời màn chờ báo. Muốn test lại, xóa phiếu báo đang ở "
       "'Đang tạo' hoặc 'Không duyệt' (do chính mình lập), phiếu nhập kho sẽ quay lại.")

d.h2("2.3. Kiểm số phiếu trên màn chờ báo")
d.p("Màn chờ báo không ghi số liệu nên kiểm bằng TỔNG SỐ BẢN GHI ở chân bảng. Mở " + M_CHO + ", lọc Kho LN, ghi lại "
    "tổng số bản ghi là N rồi thực hiện thao tác:")
d.table([
    ["Thao tác", "Tổng số bản ghi sau thao tác"],
    ["KT bấm 'Lưu & Duyệt' phiếu nhập hàng của P1 (có lệch)", "N + 1, P1 hiện ở dòng đầu"],
    ["KT chỉ bấm 'Lưu' phiếu nhập hàng của P5", "N (không đổi)"],
    ["Hạch toán P3 (khớp số) hoặc P4 (không phải nhập mua)", "N (không đổi)"],
    ["Lập phiếu báo cho P1, kể cả chỉ bấm 'Lưu'", "N - 1, không còn P1"],
    ["Xóa phiếu báo của P1", "N + 1, P1 quay lại, còn nút 'Báo hàng thừa thiếu'"],
    ["Người duyệt bấm 'Không duyệt' phiếu báo của P2", "N (không đổi), P2 KHÔNG quay lại"],
], widths=[3.9, 2.6])

d.h2("2.4. Đối chứng: phiếu báo không làm đổi tồn kho")
d.p("Tồn kho vật lý đã được ghi theo SL THỰC NHẬP ngay lúc thủ kho gửi phiếu nhập kho. Phần thiếu chưa từng vào kho nên "
    "phiếu báo và phiếu xử lý không cần ghi tồn. Kiểm như sau (hàng H1, kho LN):")
d.table([
    ["Thao tác", "Báo cáo", "Kỳ vọng so với số nền"],
    ["TK gửi phiếu nhập kho P1 (đề nghị 10, nhập 8)", "Báo cáo tồn theo kho, cột SL tồn", "+8 (không phải +10)"],
    ["", "Thẻ kho", "Thêm dòng chứng từ P1, cột Nhập 8"],
    ["KT hạch toán P1 (Lưu & Duyệt)", "Báo cáo tồn theo kho", "Không đổi"],
    ["", "Tổng hợp xuất nhập tồn (kế toán)", "Nhập trong kỳ +8"],
    ["Lập phiếu báo P1, 'Lưu & gửi'", "Báo cáo tồn kho tổng hợp theo mặt hàng, Báo cáo tồn theo kho", "Không đổi"],
    ["", "Thẻ kho", "Không có dòng chứng từ nào mang số phiếu báo (dạng 'TPE_BHNK-')"],
    ["Không duyệt / Xóa phiếu báo", "Mọi báo cáo kho", "Không đổi"],
    ["Lập và duyệt phiếu xử lý, phương án 'Trả hàng'", "Mọi báo cáo kho", "Không đổi"],
    ["Nhà cung cấp giao bù, kho lập phiếu nhập kho mới 2 Cái", "Thẻ kho, Báo cáo tồn theo kho", "Thêm dòng nhập mới, "
     "SL tồn +2"],
], widths=[2.2, 2.2, 2.1])

d.h2("2.5. Ô đếm 'cần xử lý' ở trang chủ")
d.p("Đăng nhập tài khoản DUYET, mở trang chủ, tab 'Phê duyệt', ghi số ở ô 'Phiếu báo thừa - thiếu nhập kho cần xử lý' "
    "là K (ô ẩn nghĩa là 0). Sau mỗi thao tác tải lại trang chủ:")
d.table([
    ["Thao tác", "Ô đếm"],
    ["TK lập phiếu báo, chỉ bấm 'Lưu'", "K (không đổi)"],
    ["TK bấm 'Lưu & gửi'", "K + 1"],
    ["DUYET bấm 'Không duyệt'", "Trở về K"],
    ["DUYET bấm 'Xử lý' và lưu phiếu xử lý", "Giảm 1, phiếu rời danh sách duyệt, phiếu báo 'Đã xử lý'"],
], widths=[3.9, 2.6])
d.p("Màn " + "'Tình trạng trả hàng thiếu nhập kho' (menu Mua hàng > Xử lý hàng thừa - thiếu) chỉ có dòng của hàng khi "
    "phiếu xử lý phương án 'Trả hàng' đã hoàn tất; phiếu báo đơn thuần không làm hiện dòng nào.")

d.h2("2.6. Lỗi ERP đã biết khi kiểm số")
d.bullet("Lệch phần lẻ: ", "dòng đề nghị 10, thực nhập 9.6 không lên màn chờ báo vì hệ thống làm tròn cả 2 số rồi mới so.")
d.bullet("Danh sách phiếu báo: ", "hiện phiếu của mọi công ty, không theo quyền xem; bấm vào Số phiếu công ty khác ra "
         "trang không tìm thấy. Lọc 'Từ ngày' làm bảng trống.")
d.bullet("Danh sách duyệt và ô đếm lệch nhau: ", "danh sách duyệt hiện phiếu 'Chờ xử lý' của mọi công ty, ô đếm chỉ đếm "
         "công ty mình.")
d.bullet("Sửa phiếu báo rồi lưu: ", "mất đơn giá các dòng, phiếu xử lý lập sau đó thiếu đơn giá và thành tiền.")
d.bullet("Xóa phiếu xử lý: ", "phiếu báo vẫn 'Đã xử lý', không lập lại phiếu xử lý được.")

# =====================================================================
d.h1("PHẦN 3: BẢNG GHI SỐ KHI KIỂM")
d.p("In bảng dưới hoặc chép ra Excel, mỗi phép kiểm 1 dòng. Cột 'Kỳ vọng' = Số nền cộng / trừ số lượng của thao tác. "
    "Số sau khác Kỳ vọng thì ghi Failed, kèm ảnh chụp báo cáo trước và sau.")
rows = [["TC", "Báo cáo / bộ lọc", "Hàng", "Số nền", "Thao tác", "Kỳ vọng", "Số sau", "Đạt"]]
rows.append(["Ví dụ", "Thẻ kho, kho LN, TPE, đầu tháng đến hôm nay", "H1", "120", "Gửi duyệt P2, thừa 3", "123", "123",
             "Đạt"])
rows += [["", "", "", "", "", "", "", ""] for _ in range(10)]
d.table(rows, widths=[0.5, 1.6, 0.5, 0.6, 1.3, 0.7, 0.6, 0.6])

d.save(OUT)
print("Da tao:", OUT)
print("So trang:", cap_nhat_truong(OUT))
