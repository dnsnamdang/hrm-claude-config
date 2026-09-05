# -*- coding: utf-8 -*-
"""Sinh file testcase Excel cho man "Phieu uy nhiem chi" (phan he Tai chinh).

Nguon doc code 04/09/2026 (nhanh gop_db):
  BE  Modules/Finance/Routes/api.php (:326-352)
      Modules/Finance/Http/Controllers/V1/BillPaymentAuthorizationController.php
      Modules/Finance/Entities/BillPaymentAuthorization/*.php
      Modules/Finance/Http/Requests/BillPaymentAuthorization/*.php (nguyen van thong bao loi)
      Modules/Finance/Services/BillPaymentAuthorization{Service,WriteService,
                                AccountingService,EmployeeAccountingService,HistoryService}.php
      Modules/Finance/Transformers/BillPaymentAuthorizationResource/*.php
      Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php (:1163, :1275-1276)
  FE  hrm-client/pages/finance/bill-payment-authorizations/{index,create}.vue
      .../_id/{index,edit}.vue
      .../components/{BillPaymentAuthorizationForm,PaymentRequestSearchModal}.vue
      hrm-client/pages/finance/bill-payments/components/PaymentEmployeeTable.vue (dung chung)
      hrm-client/components/subsystem-menu/finance.js (:94)
  Anh that: unc_shots/ (cong dev hrm-crm.eteksofts.com, 04/09/2026)

Chay:  python .plans/gop-db/finance-bill-payment-authorization/gen_testcase.py
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", ".claude", "skills",
                                "testcase-documenter", "assets"))
from tc_engine import build  # noqa: E402

OUT = os.path.join(HERE, "testcase.xlsx")
MODULE = "Phiếu ủy nhiệm chi"

MENU = "Phân hệ Tài chính > Quản lý tiền > Thanh toán tiền mặt > Phiếu ủy nhiệm chi"

# ════════════════════════════════════════════════════ 1. KHỐI MÔ TẢ (9 mục)
DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Phiếu ủy nhiệm chi là chứng từ kế toán ghi nhận khoản tiền doanh nghiệp chi ra BẰNG HÌNH "
     "THỨC CHUYỂN KHOẢN. Đây là bản song sinh chuyển khoản của Phiếu chi tiền: cùng lập từ Phiếu "
     "đề nghị thanh toán đang ở trạng thái Chờ tạo phiếu chi, nhưng chỉ nhận những đề nghị có "
     "hình thức thanh toán là chuyển khoản (Phiếu chi tiền lấy các đề nghị tiền mặt).\n"
     "Màn hình cho phép: xem danh sách, lọc, lập phiếu (Lưu nháp hoặc Lưu và duyệt), sửa và xóa "
     "phiếu nháp, xem chi tiết, xem lịch sử thay đổi.\n"
     "Màn hình phục vụ HAI luồng lập phiếu khác hẳn nhau:\n"
     "- Luồng lập TỪ phiếu đề nghị (6 loại chi: Chi trả nhà cung cấp, Chi trả lại khách hàng, "
     "Chi thưởng NVKD, Chi thưởng thực hiện hợp đồng, Chi khác, Thanh toán chi phí vận chuyển "
     "NCC): kế toán chọn phiếu đề nghị trong cửa sổ tra cứu, hệ thống tự kéo toàn bộ thông tin "
     "và các dòng chi tiết về, kế toán chỉ chốt lại số tiền duyệt chi và khai tài khoản chuyển "
     "tiền.\n"
     "- Luồng Chi thu nhập cho nhân viên: lập TRỰC TIẾP, không qua đề nghị. Kế toán chọn phòng "
     "ban, hệ thống tự hút số thu nhập còn phải trả của từng nhân viên phòng đó từ sổ kế toán.\n"
     "KHÁC hẳn Phiếu chi tiền: màn này KHÔNG có bước gửi duyệt / duyệt / hủy, KHÔNG có in, "
     "KHÔNG có xuất Excel. Bấm 'Lưu và duyệt' là phiếu vào sổ kế toán ngay lập tức và không sửa "
     "được nữa.\n"
     "Đường dẫn màn hình: " + MENU + " (đường dẫn trực tiếp: /finance/bill-payment-authorizations). "
     "Chỉ có duy nhất MỘT mục menu trỏ vào màn này."),

    ("2. Đối tượng được tính / hiển thị",
     "Danh sách hiển thị phiếu ủy nhiệm chi theo phạm vi quyền của người đăng nhập:\n"
     "- Là quản trị hệ thống, hoặc có quyền 'Xem tất cả phiếu ủy nhiệm chi của tổng công ty': "
     "thấy phiếu của mọi công ty.\n"
     "- Có quyền 'Xem tất cả phiếu ủy nhiệm chi của công ty': thấy phiếu thuộc công ty của mình, "
     "cộng thêm phiếu do chính mình lập và phiếu do chính mình duyệt (kể cả ở công ty khác).\n"
     "- Không có quyền nào trong hai quyền trên: chỉ thấy phiếu do chính mình lập hoặc chính "
     "mình duyệt.\n"
     "Chỉ có HAI trạng thái được dùng trong thực tế: 'Đang tạo' (phiếu nháp) và 'Đã hạch toán'.\n"
     "Ô lọc Loại chi liệt kê 6 loại: Chi trả nhà cung cấp, Chi trả lại khách hàng, Chi thưởng "
     "NVKD, Chi thưởng thực hiện hợp đồng, Chi khác, Thanh toán chi phí vận chuyển NCC."),

    ("3. Đối tượng bị ẩn / không tính",
     "- PHIẾU NHÁP CỦA NGƯỜI KHÁC LUÔN BỊ ẨN, kể cả với quản trị hệ thống và người có quyền xem "
     "toàn tổng công ty. Chỉ người lập mới nhìn thấy phiếu nháp của mình.\n"
     "- Hai trạng thái 'Chờ duyệt' và 'Hủy' tuy vẫn có tên trong hệ thống nhưng KHÔNG có thao "
     "tác nào tạo ra chúng, nên không xuất hiện trong ô lọc Trạng thái và cũng không có phiếu "
     "nào mang trạng thái đó.\n"
     "- Ô lọc Loại chi CỐ Ý KHÔNG có 'Chi thu nhập cho nhân viên' (giữ đúng hệ thống cũ), dù "
     "phiếu loại đó vẫn lập được và vẫn hiện trong danh sách.\n"
     "- Cửa sổ Chọn phiếu đề nghị chi chỉ liệt kê phiếu đề nghị đang ở trạng thái Chờ tạo phiếu "
     "chi VÀ có hình thức thanh toán là chuyển khoản. Đề nghị tiền mặt không bao giờ xuất hiện "
     "ở đây (chúng thuộc màn Phiếu chi tiền).\n"
     "- Ô lọc Loại chi trong cửa sổ đó chỉ có 4 loại: Chi trả nhà cung cấp, Chi trả lại khách "
     "hàng, Chi thưởng thực hiện hợp đồng, Thanh toán chi phí vận chuyển NCC."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Cặp ô 'Ngày lập từ' / 'Ngày lập đến' lọc theo NGÀY TẠO PHIẾU ỦY NHIỆM CHI (đúng cột 'Ngày "
     "tạo' trên lưới), KHÔNG phải ngày hạch toán và cũng không phải ngày lập phiếu đề nghị.\n"
     "Khoảng ngày lấy CẢ HAI ĐẦU MÚT: chọn từ 01/08 đến 31/08 thì phiếu tạo đúng ngày 01/08 và "
     "đúng ngày 31/08 đều được tính.\n"
     "Chỉ điền một đầu: điền mỗi 'từ' thì lấy từ ngày đó trở về sau; điền mỗi 'đến' thì lấy từ "
     "ngày đó trở về trước.\n"
     "KHÔNG có bộ lọc theo Ngày hạch toán và KHÔNG có bộ lọc theo khoảng số tiền (giữ đúng hệ "
     "thống cũ)."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Một phiếu ủy nhiệm chi gồm 3 tầng:\n"
     "1) Thông tin chung: phiếu đề nghị nguồn, loại chi, tài khoản có / tài khoản nợ, ngày hạch "
     "toán, tỷ giá, phương thức thanh toán, ngân hàng chuyển và số tài khoản chuyển khoản.\n"
     "2) Bảng Chi tiết: mỗi dòng là một đơn hàng / hợp đồng cần chi, có số tiền đề nghị chi và "
     "số tiền duyệt chi. Riêng phiếu Chi thu nhập cho nhân viên thì mỗi dòng là MỘT NHÂN VIÊN, "
     "và bảng có 2 tab: 'Chi tiết' (tổng số tiền chi cho từng người) và 'Chi tiết vụ việc' (tách "
     "tổng đó thành 5 khoản: Chênh lệch lương, Hoa hồng tháng, Hoa hồng quý, Thưởng quý, Tiền "
     "vận chuyển).\n"
     "3) Khối bút toán trong sổ kế toán, chỉ sinh ra khi bấm 'Lưu và duyệt'.\n"
     "Quan hệ với phiếu đề nghị: một phiếu ủy nhiệm chi trỏ về đúng MỘT phiếu đề nghị thanh "
     "toán. Chiều ngược lại KHÔNG bị chặn — xem mục 9."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Cột 'Số tiền duyệt chi' trên lưới danh sách = TỔNG số tiền duyệt chi (đã quy đổi sang "
     "đồng Việt Nam) của mọi dòng chi tiết trong phiếu.\n"
     "- Dòng 'Tổng cộng' cuối bảng chi tiết cộng dồn cả 4 cột tiền (đề nghị chi và duyệt chi, ở "
     "cả cột nguyên tệ lẫn cột quy đổi).\n"
     "- Với phiếu Chi thu nhập cho nhân viên: tổng 5 khoản của một nhân viên ở tab 'Chi tiết vụ "
     "việc' phải bằng đúng ô 'Số tiền chi' của nhân viên đó ở tab 'Chi tiết' (chênh lệch cho "
     "phép tối đa 0,5 đồng); lệch thì hệ thống chặn không cho duyệt.\n"
     "- Không có cơ chế gộp trùng: mỗi dòng chi tiết là một dòng độc lập, kể cả khi hai dòng "
     "cùng trỏ về một hợp đồng.\n"
     "- ⚠️ Riêng bút toán bên CÓ khi ghi sổ kế toán KHÔNG cộng dồn — xem mục 9."),

    ("7. Phân quyền cấp",
     "Ba tên quyền liên quan tới màn này (chép đúng tên hiển thị trong phần Phân quyền):\n"
     "1) 'Xem tất cả phiếu ủy nhiệm chi của tổng công ty' — thấy phiếu của mọi công ty.\n"
     "2) 'Xem tất cả phiếu ủy nhiệm chi của công ty' — thấy phiếu của công ty mình, cộng phiếu "
     "mình lập và phiếu mình duyệt.\n"
     "3) 'Kế toán thanh toán' — quyền lập / sửa / xóa phiếu, mở được cửa sổ Chọn phiếu đề nghị "
     "chi và lấy được số liệu thu nhập nhân viên. Đây là quyền dùng chung cho nhiều màn của "
     "phân hệ Tài chính, không phải quyền riêng của màn này.\n"
     "KHÔNG CÓ quyền duyệt riêng: ai lập được phiếu thì bấm 'Lưu và duyệt' là ghi thẳng vào sổ "
     "kế toán.\n"
     "Điều kiện SỬA và XÓA giống hệt nhau và phải đủ CẢ BA: phiếu đang ở trạng thái 'Đang tạo' + "
     "người thao tác đúng là người đã lập phiếu + có quyền 'Kế toán thanh toán'. Quản trị hệ "
     "thống CỐ Ý không được miễn trừ ba điều kiện này."),

    ("8. Cách tính các ô thống kê",
     "- Dòng 'Hiển thị a–b / N' dưới lưới: a là số thứ tự bản ghi đầu trang hiện tại, b là bản "
     "ghi cuối trang, N là tổng số phiếu khớp bộ lọc và khớp phạm vi quyền của người đăng nhập.\n"
     "- Ô 'Số dòng/trang' có 5 mức: 5, 10, 20, 50, 100; mặc định 10.\n"
     "- Cột 'Số tiền duyệt chi': tổng tiền duyệt chi quy đổi của phiếu, hiển thị có dấu ngăn "
     "hàng nghìn, không có phần thập phân.\n"
     "- Ô 'Tỷ giá' ở form: mặc định 1; khi phiếu đề nghị nguồn dùng ngoại tệ thì tỷ giá lấy theo "
     "phiếu đề nghị và ô mở ra cho sửa. Cột tiền quy đổi = số tiền nguyên tệ × tỷ giá, tự tính "
     "lại ngay khi đổi tỷ giá.\n"
     "- Dòng 'Tổng cộng' của bảng chi tiết: cộng theo cột, tính cả những dòng có số tiền bằng 0."),

    ("9. Ghi chú đọc bảng",
     "6 cái bẫy dễ chấm sai của màn này — đọc trước khi chạy test:\n"
     "1) ⚠️ BÚT TOÁN BÊN CÓ = SỐ TIỀN DÒNG CUỐI, KHÔNG PHẢI TỔNG. Với phiếu có nhiều dòng chi "
     "tiết, khi duyệt xong hệ thống ghi bút toán bên Có bằng đúng số tiền của DÒNG CUỐI trong "
     "bảng chi tiết. Đây là hành vi CỐ Ý giữ y hệt hệ thống cũ (đã đo trên dữ liệu thật và được "
     "chốt giữ nguyên) — CHẤM ĐẠT, không ghi lỗi.\n"
     "2) ⚠️ MỘT PHIẾU ĐỀ NGHỊ CÓ THỂ LẬP ĐƯỢC NHIỀU PHIẾU ỦY NHIỆM CHI. Cửa sổ chọn đề nghị "
     "không loại bỏ đề nghị đã có phiếu ủy nhiệm chi (khác màn Phiếu chi tiền). Cố ý giữ giống "
     "hệ thống cũ.\n"
     "3) ⚠️ PHIẾU LOẠI 'CHI KHÁC' DUYỆT XONG KHÔNG SINH BÚT TOÁN NÀO. Cố ý, giống hệ thống cũ.\n"
     "4) ⚠️ NGÀY HẠCH TOÁN KHÔNG ĐƯỢC NHỎ HƠN NGÀY HÔM NAY khi bấm 'Lưu và duyệt' — kể cả ở màn "
     "Sửa. Phiếu nháp lưu hôm qua, hôm nay mở ra bấm 'Lưu và duyệt' mà quên đổi ngày là bị chặn: "
     "đúng thiết kế. Riêng đường 'Lưu nháp' thì ngày quá khứ vẫn lưu được.\n"
     "5) Dấu ngăn hàng nghìn không đồng nhất: ô số tiền trong form và trong cửa sổ chọn đề nghị "
     "dùng dấu phẩy, còn cột 'Số tiền duyệt chi' trên lưới danh sách dùng dấu chấm. Ghi nhận là "
     "điểm lệch hiển thị, không phải lỗi tính toán.\n"
     "6) Nhãn cột lưới là 'Ngày tạo' / 'Người tạo' nhưng nhãn ô lọc là 'Khoảng ngày lập' / "
     "'Người lập' — cùng một dữ liệu, cố ý đặt lệch tên, không phải lỗi.\n"
     "Hai cột 'Số tiền duyệt chi' và 'Ngày hạch toán' MẶC ĐỊNH ẨN, phải bật trong cửa sổ 'Tuỳ "
     "chỉnh cột' mới thấy; hệ thống ghi nhớ lựa chọn này theo từng người dùng."),
]

# ════════════════════════════════════════════════════ 2. SECTION PHÂN QUYỀN
ROLE_TCS = [
    ("01", "Người có quyền xem toàn tổng công ty thấy phiếu mọi công ty", "P0",
     "Tài khoản A có quyền 'Xem tất cả phiếu ủy nhiệm chi của tổng công ty', thuộc công ty 4. "
     "Toàn hệ thống có 2.587 phiếu của nhiều công ty, trong đó có 1 phiếu nháp do người khác lập.",
     "1. Đăng nhập bằng tài khoản A\n"
     "2. Vào " + MENU + "\n"
     "3. Đọc dòng 'Hiển thị a–b / N' dưới lưới",
     "—",
     "- Tổng N = 2.586 (toàn bộ phiếu trừ 1 phiếu nháp của người khác)\n"
     "- Lưới có phiếu của nhiều công ty khác nhau\n"
     "- ⚠️ Phiếu nháp của người khác KHÔNG xuất hiện dù tài khoản có quyền rộng nhất"),

    ("02", "Người có quyền xem theo công ty chỉ thấy phiếu công ty mình", "P0",
     "Tài khoản B có quyền 'Xem tất cả phiếu ủy nhiệm chi của công ty', thuộc công ty 4; công ty "
     "4 có 2 phiếu; tài khoản B chưa lập và chưa duyệt phiếu nào ở công ty khác.",
     "1. Đăng nhập bằng tài khoản B\n"
     "2. Vào " + MENU + "\n"
     "3. Đọc tổng số bản ghi\n"
     "4. Bật cột 'Công ty' trong bộ lọc nâng cao và thử chọn một công ty khác",
     "Công ty: chọn một công ty không phải công ty 4",
     "- Tổng = 2 phiếu\n"
     "- Chọn lọc sang công ty khác cho kết quả rỗng, hiển thị 'Không có dữ liệu phù hợp bộ lọc.'\n"
     "- Không có thông báo lỗi, không treo trang"),

    ("03", "Người không có quyền xem nào chỉ thấy phiếu của chính mình", "P0",
     "Tài khoản C không có cả hai quyền xem, đã lập 3 phiếu (2 đã hạch toán, 1 nháp), chưa duyệt "
     "phiếu của ai.",
     "1. Đăng nhập bằng tài khoản C\n"
     "2. Vào " + MENU + "\n"
     "3. Đối chiếu danh sách với 3 phiếu đã lập",
     "—",
     "- Đúng 3 phiếu, tất cả đều do tài khoản C lập\n"
     "- Không thấy bất kỳ phiếu nào của người khác"),

    ("04", "Người đã duyệt phiếu vẫn mở lại được phiếu đó", "P1",
     "Tài khoản D không có quyền xem theo cấp nào, nhưng trước đó đã bấm 'Lưu và duyệt' một "
     "phiếu ở công ty khác.",
     "1. Đăng nhập bằng tài khoản D\n"
     "2. Vào màn danh sách\n"
     "3. Tìm phiếu đã duyệt bằng ô 'Mã phiếu'",
     "Mã phiếu: mã của phiếu tài khoản D đã duyệt",
     "- Phiếu vẫn nằm trong danh sách\n"
     "- Bấm mã phiếu mở được màn chi tiết, không bị từ chối quyền"),

    ("05", "Phiếu nháp của người khác luôn bị ẩn, kể cả với quản trị hệ thống", "P0",
     "Tài khoản E là quản trị hệ thống. Tài khoản C đã lưu 1 phiếu nháp mã TPE.UNC0826.00013.",
     "1. Đăng nhập bằng tài khoản E\n"
     "2. Vào màn danh sách\n"
     "3. Gõ TPE.UNC0826.00013 vào ô tìm nhanh rồi bấm Tìm kiếm\n"
     "4. Gõ thẳng đường dẫn màn chi tiết của phiếu đó vào thanh địa chỉ",
     "Ô tìm nhanh: TPE.UNC0826.00013",
     "- Danh sách rỗng, hiện 'Không có dữ liệu phù hợp bộ lọc.'\n"
     "- Mở bằng đường dẫn trực tiếp: hệ thống từ chối, báo không có quyền xem phiếu này\n"
     "- ⚠️ Quản trị hệ thống CŨNG bị chặn — đây là thiết kế, không phải lỗi"),

    ("06", "Quyền 'Kế toán thanh toán' cho phép lập phiếu", "P0",
     "Tài khoản F có quyền 'Kế toán thanh toán'. Có ít nhất 1 phiếu đề nghị thanh toán chuyển "
     "khoản đang ở trạng thái Chờ tạo phiếu chi.",
     "1. Đăng nhập bằng tài khoản F\n"
     "2. Vào màn danh sách, bấm nút 'Tạo mới'\n"
     "3. Bấm vào ô 'Số phiếu đề nghị' để mở cửa sổ chọn đề nghị\n"
     "4. Chọn 1 phiếu đề nghị, khai đủ ô bắt buộc, bấm 'Lưu nháp'",
     "Loại chi: Chi trả nhà cung cấp",
     "- Cửa sổ chọn đề nghị mở được và có dữ liệu\n"
     "- Lưu thành công, hệ thống báo thêm phiếu thành công và quay về danh sách\n"
     "- Phiếu mới nằm đầu danh sách, trạng thái 'Đang tạo'"),

    ("07", "Không có quyền 'Kế toán thanh toán' thì không lập được phiếu", "P0",
     "Tài khoản G có quyền 'Xem tất cả phiếu ủy nhiệm chi của công ty' nhưng KHÔNG có quyền 'Kế "
     "toán thanh toán'.",
     "1. Đăng nhập bằng tài khoản G\n"
     "2. Vào màn danh sách, bấm 'Tạo mới'\n"
     "3. Bấm vào ô 'Số phiếu đề nghị'\n"
     "4. Chọn Loại chi rồi bấm 'Lưu nháp'",
     "—",
     "- Cửa sổ chọn đề nghị KHÔNG mở được dữ liệu, hệ thống báo không có quyền xem danh sách "
     "phiếu đề nghị chi\n"
     "- Bấm Lưu: hệ thống từ chối, báo không có quyền lập phiếu ủy nhiệm chi\n"
     "- Không có phiếu nào được tạo ra"),

    ("08", "Nút Sửa chỉ hiện khi đủ cả ba điều kiện", "P0",
     "Tài khoản F có quyền 'Kế toán thanh toán' và đang có 1 phiếu nháp do chính mình lập, 1 "
     "phiếu đã hạch toán do chính mình lập.",
     "1. Đăng nhập bằng tài khoản F\n"
     "2. Vào danh sách, quan sát cột 'Hành động' của 2 phiếu trên",
     "—",
     "- Phiếu nháp: có đủ 3 biểu tượng Sửa (bút chì), Xóa (thùng rác), Lịch sử (đồng hồ)\n"
     "- Phiếu đã hạch toán: CHỈ có biểu tượng Lịch sử\n"
     "- ⚠️ Không có nút xám mờ — nút không dùng được thì bị ẩn hẳn"),

    ("09", "Có quyền nhưng không phải người lập thì không sửa được", "P0",
     "Tài khoản H có quyền 'Kế toán thanh toán' và quyền xem toàn tổng công ty. Phiếu "
     "TPE.UNC0826.00013 ở trạng thái 'Đang tạo' do tài khoản khác lập.",
     "1. Đăng nhập bằng tài khoản H\n"
     "2. Tìm phiếu TPE.UNC0826.00013",
     "Ô tìm nhanh: TPE.UNC0826.00013",
     "- Phiếu không hiện ra vì là phiếu nháp của người khác\n"
     "- Gõ thẳng đường dẫn màn Sửa của phiếu đó: hệ thống chặn, không mở được form Sửa"),

    ("10", "Người lập có quyền nhưng phiếu đã hạch toán thì không sửa được", "P0",
     "Tài khoản F có quyền 'Kế toán thanh toán', đã lập phiếu TPE.UNC0826.00012 và phiếu này ở "
     "trạng thái 'Đã hạch toán'.",
     "1. Đăng nhập bằng tài khoản F\n"
     "2. Mở màn chi tiết TPE.UNC0826.00012\n"
     "3. Quan sát các nút ở chân màn\n"
     "4. Gõ thẳng đường dẫn màn Sửa của phiếu này",
     "—",
     "- Chân màn chi tiết CHỈ có nút 'Quay lại'\n"
     "- Gõ đường dẫn màn Sửa: hệ thống tự đưa về màn xem chi tiết, không cho vào form"),

    ("11", "Quản trị hệ thống KHÔNG được miễn trừ ở Sửa và Xóa", "P0",
     "Tài khoản E là quản trị hệ thống nhưng KHÔNG có quyền 'Kế toán thanh toán'; tài khoản E tự "
     "lập 1 phiếu nháp (nếu lập được) hoặc dùng phiếu nháp do chính tài khoản E lập trước đó.",
     "1. Đăng nhập bằng tài khoản E\n"
     "2. Mở phiếu nháp của chính mình\n"
     "3. Quan sát chân màn",
     "—",
     "- ⚠️ Quản trị hệ thống lập được phiếu (được miễn trừ ở bước lập) NHƯNG nút 'Sửa' và 'Xóa' "
     "vẫn ẩn nếu thiếu quyền 'Kế toán thanh toán' — đây là thiết kế siết chặt có chủ đích"),

    ("12", "Lấy số liệu thu nhập nhân viên đòi quyền 'Kế toán thanh toán'", "P0",
     "Tài khoản G không có quyền 'Kế toán thanh toán'.",
     "1. Đăng nhập bằng tài khoản G, mở form Tạo mới\n"
     "2. Chọn Loại chi = 'Chi thu nhập cho nhân viên'\n"
     "3. Chọn một phòng ban ở ô 'Phòng ban'",
     "Loại chi: Chi thu nhập cho nhân viên; Phòng ban: PHÒNG KINH DOANH",
     "- Hệ thống từ chối, báo không có quyền xem số liệu thu nhập nhân viên\n"
     "- Bảng chi tiết không nạp dòng nào\n"
     "- ⚠️ Đây là dữ liệu lương thưởng nên phải chặn ở cả phía máy chủ, không chỉ ẩn nút"),

    ("13", "Xem chi tiết phiếu ngoài phạm vi quyền", "P1",
     "Tài khoản C không có quyền xem theo cấp nào. Phiếu TPE.UNC0826.00011 đã hạch toán, do "
     "người khác lập, ở công ty khác.",
     "1. Đăng nhập bằng tài khoản C\n"
     "2. Gõ thẳng đường dẫn màn chi tiết của TPE.UNC0826.00011 vào thanh địa chỉ",
     "—",
     "- Hệ thống từ chối, báo không có quyền xem phiếu ủy nhiệm chi này\n"
     "- Không hiện bất kỳ số liệu nào của phiếu"),

    ("14", "Vượt giao diện: gọi thẳng chức năng Thêm khi thiếu quyền", "P0",
     "Tài khoản G không có quyền 'Kế toán thanh toán'. Dành cho tester kỹ thuật.",
     "1. Đăng nhập bằng tài khoản G, lấy phiên đăng nhập\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Thêm phiếu ủy nhiệm chi, bỏ qua giao diện\n"
     "3. Kiểm tra danh sách phiếu sau khi gọi",
     "Dữ liệu gửi: một phiếu hợp lệ đầy đủ trường",
     "- Hệ thống từ chối, báo không có quyền lập phiếu ủy nhiệm chi\n"
     "- Không có phiếu nào được tạo, không có bút toán nào sinh ra"),

    ("15", "Vượt giao diện: sửa phiếu của người khác", "P0",
     "Tài khoản H có quyền 'Kế toán thanh toán'. Phiếu nháp TPE.UNC0826.00013 do tài khoản khác "
     "lập. Dành cho tester kỹ thuật.",
     "1. Đăng nhập bằng tài khoản H\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Sửa lên phiếu TPE.UNC0826.00013\n"
     "3. Mở lại phiếu bằng tài khoản người lập để đối chiếu",
     "Dữ liệu gửi: đổi ô Lý do chi",
     "- Hệ thống từ chối, báo chỉ sửa được phiếu ủy nhiệm chi ở trạng thái Đang tạo do chính "
     "mình lập\n"
     "- Nội dung phiếu giữ nguyên, không có dòng lịch sử thay đổi nào được ghi"),

    ("16", "Vượt giao diện: sửa phiếu đã hạch toán", "P0",
     "Tài khoản F là người lập phiếu TPE.UNC0826.00012 và phiếu đã ở trạng thái 'Đã hạch toán'. "
     "Dành cho tester kỹ thuật.",
     "1. Đăng nhập bằng tài khoản F\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Sửa lên phiếu này\n"
     "3. Đối chiếu lại số bút toán trong sổ kế toán trước và sau",
     "Dữ liệu gửi: đổi Số tiền duyệt chi của dòng đầu",
     "- Hệ thống từ chối với đúng câu 'Chỉ sửa được phiếu ủy nhiệm chi ở trạng thái Đang tạo do "
     "chính bạn lập'\n"
     "- ⚠️ Số bút toán trong sổ kế toán KHÔNG đổi — điểm quan trọng nhất của nhóm này"),

    ("17", "Vượt giao diện: xóa phiếu đã hạch toán", "P0",
     "Tài khoản F là người lập phiếu đã hạch toán TPE.UNC0826.00012. Dành cho tester kỹ thuật.",
     "1. Đăng nhập bằng tài khoản F\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Xóa lên phiếu này\n"
     "3. Mở lại danh sách",
     "—",
     "- Hệ thống từ chối, báo chỉ xóa được phiếu ở trạng thái Đang tạo do chính mình lập\n"
     "- Phiếu vẫn còn nguyên trong danh sách, các dòng chi tiết còn nguyên"),

    ("18", "Vượt giao diện: lấy số liệu thu nhập nhân viên phòng ban khác công ty", "P1",
     "Tài khoản F có quyền 'Kế toán thanh toán', thuộc công ty 4. Dành cho tester kỹ thuật.",
     "1. Đăng nhập bằng tài khoản F\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng lấy số liệu thu nhập nhân viên, truyền "
     "một phòng ban thuộc công ty khác",
     "Phòng ban: một phòng thuộc công ty 1",
     "- Kết quả trả về rỗng (không rò rỉ số liệu lương của công ty khác)\n"
     "- Không báo lỗi hệ thống"),

    ("19", "Vượt giao diện: lấy số liệu thu nhập nhân viên nhưng bỏ trống phòng ban", "P2",
     "Tài khoản F có quyền 'Kế toán thanh toán'. Dành cho tester kỹ thuật.",
     "1. Dùng công cụ kiểm thử API gọi chức năng lấy số liệu thu nhập nhân viên, không truyền "
     "phòng ban",
     "—",
     "- Hệ thống báo 'Không tìm thấy phòng ban'\n"
     "- Không trả về dòng dữ liệu nào"),

    ("20", "Mục menu hiện với mọi người vào được phân hệ Tài chính", "P2",
     "Tài khoản C không có quyền xem theo cấp nào nhưng vào được phân hệ Tài chính.",
     "1. Đăng nhập bằng tài khoản C\n"
     "2. Mở menu Quản lý tiền > Thanh toán tiền mặt",
     "—",
     "- Mục 'Phiếu ủy nhiệm chi' vẫn hiển thị trong menu\n"
     "- Bấm vào mở được màn danh sách, chỉ là danh sách rỗng hoặc chỉ có phiếu của chính mình\n"
     "- ⚠️ Menu không bị ẩn theo quyền; phạm vi dữ liệu mới là thứ được kiểm soát"),
]

# ════════════════════════════════════════════════════ 3. SECTION NGHIỆP VỤ
S1 = [
    (1, "Mở màn danh sách từ menu", "P0",
     "Tài khoản có quyền xem toàn tổng công ty; hệ thống có 2.586 phiếu trong phạm vi.",
     "1. Đăng nhập\n2. Chọn phân hệ Tài chính\n3. Bấm menu 'Quản lý tiền'\n"
     "4. Trong nhóm 'THANH TOÁN TIỀN MẶT' bấm 'Phiếu ủy nhiệm chi'",
     "—",
     "- Tiêu đề thanh trên cùng: 'Danh sách phiếu ủy nhiệm chi'\n"
     "- Khối 'Bộ lọc danh sách' ở trên, khối 'Danh sách phiếu ủy nhiệm chi' ở dưới\n"
     "- Lưới hiện 10 dòng đầu, dòng thông tin 'Hiển thị 1–10 / 2586'"),

    (2, "Chỉ có một lối vào màn hình", "P1",
     "Nhóm menu 'Quản lý tiền' của phân hệ Tài chính có 2 nhóm con và 7 chức năng.",
     "1. Mở menu 'Quản lý tiền'\n2. Đếm các mục trỏ tới màn Phiếu ủy nhiệm chi\n"
     "3. Duyệt các nhóm menu còn lại của phân hệ Tài chính",
     "—",
     "- Chỉ đúng MỘT mục menu trỏ vào màn này, nằm trong nhóm 'THANH TOÁN TIỀN MẶT'\n"
     "- ⚠️ Màn không có các chế độ xem khác nhau như một số màn phiếu khác — mọi người đều vào "
     "cùng một danh sách, chỉ khác phạm vi dữ liệu"),

    (3, "Vào bằng đường dẫn trực tiếp", "P1",
     "Tài khoản có quyền xem toàn tổng công ty, đang ở màn khác.",
     "1. Gõ /finance/bill-payment-authorizations vào thanh địa chỉ\n2. Nhấn Enter",
     "—",
     "- Màn danh sách mở bình thường, dữ liệu và phạm vi giống hệt khi vào từ menu"),

    (4, "Thêm tham số lạ vào đường dẫn", "P1",
     "Tài khoản có quyền xem toàn tổng công ty (2.586 phiếu).",
     "1. Gõ /finance/bill-payment-authorizations?type=all vào thanh địa chỉ\n"
     "2. Đọc tổng số bản ghi\n3. Thử tiếp ?type=abc123",
     "—",
     "- Hệ thống bỏ qua tham số lạ, vẫn hiển thị đúng 2.586 phiếu\n"
     "- KHÔNG lỗi, KHÔNG lộ thêm dữ liệu ngoài phạm vi quyền"),

    (5, "Bố cục thanh công cụ", "P1",
     "Tài khoản bất kỳ vào được màn.",
     "1. Quan sát khối 'Danh sách phiếu ủy nhiệm chi'",
     "—",
     "- Bên phải tiêu đề có đúng 2 nút: 'Tạo mới' và một nút biểu tượng cột (chú thích khi rê "
     "chuột: 'Cấu hình cột hiển thị')\n"
     "- ⚠️ KHÔNG có nút Xuất Excel, KHÔNG có nút In, KHÔNG có nút Import — đúng thiết kế"),

    (6, "Khối bộ lọc mặc định thu gọn", "P1",
     "Vào màn lần đầu trên trình duyệt sạch.",
     "1. Vào màn danh sách\n2. Quan sát khối 'Bộ lọc danh sách'",
     "—",
     "- Chỉ hiện ô tìm nhanh với gợi ý 'Tìm theo mã phiếu ủy nhiệm chi...', nút 'Tìm kiếm', nút "
     "'Làm mới'\n- Các ô lọc chi tiết đang ẩn; nút mở mang chữ 'Tìm kiếm nâng cao'"),

    (7, "Danh sách rỗng", "P1",
     "Tài khoản không có quyền xem theo cấp nào và chưa lập phiếu nào.",
     "1. Vào màn danh sách",
     "—",
     "- Lưới hiện đúng câu 'Không có dữ liệu phù hợp bộ lọc.'\n"
     "- Dòng thông tin hiển thị 'Không có phiếu nào.'\n- Trang không lỗi, nút Tạo mới vẫn còn"),

    (8, "Trạng thái đang tải", "P2",
     "Mạng chậm hoặc dữ liệu lớn.",
     "1. Vào màn danh sách và quan sát ngay khi trang vừa mở",
     "—",
     "- Trong lúc chờ, lưới hiện 'Đang tải dữ liệu...'\n- Khi có dữ liệu thì thay bằng các dòng phiếu"),
]

S2 = [
    (1, "Tìm nhanh theo mã phiếu — khớp đầy đủ", "P0",
     "Tồn tại phiếu TPE.UNC0826.00014 trong phạm vi xem.",
     "1. Gõ TPE.UNC0826.00014 vào ô tìm nhanh\n2. Bấm 'Tìm kiếm'",
     "Ô tìm nhanh: TPE.UNC0826.00014",
     "- Đúng 1 dòng kết quả, cột 'Mã phiếu' hiển thị đúng mã vừa gõ"),

    (2, "Tìm nhanh theo một đoạn mã", "P0",
     "Tháng 08/2026 có 14 phiếu mang tiền tố TPE.UNC0826.",
     "1. Gõ UNC0826 vào ô tìm nhanh\n2. Nhấn Enter",
     "Ô tìm nhanh: UNC0826",
     "- Mọi dòng trả về đều có mã chứa đoạn UNC0826\n- Số dòng khớp đúng số phiếu tháng 08/2026 "
     "nằm trong phạm vi xem"),

    (3, "Ô tìm nhanh không tự tìm khi đang gõ", "P1",
     "Danh sách đang hiển thị đủ bản ghi.",
     "1. Gõ vài ký tự vào ô tìm nhanh\n2. Chờ 5 giây, KHÔNG bấm gì",
     "Ô tìm nhanh: UNC",
     "- Danh sách KHÔNG đổi khi chỉ gõ\n- Chỉ khi bấm 'Tìm kiếm' hoặc nhấn Enter danh sách mới lọc lại"),

    (4, "Xoá nhanh nội dung ô tìm", "P2",
     "Ô tìm nhanh đang có nội dung và danh sách đã lọc.",
     "1. Bấm dấu × trong ô tìm nhanh",
     "—",
     "- Ô trống trở lại và danh sách quay về đầy đủ bản ghi"),

    (5, "Mở và đóng bộ lọc nâng cao", "P0",
     "Đang ở màn danh sách.",
     "1. Bấm 'Tìm kiếm nâng cao'\n2. Đếm số ô lọc hiện ra\n3. Bấm 'Ẩn tìm kiếm nâng cao'",
     "—",
     "- Hiện đủ 11 ô: Mã phiếu, Mã phiếu đề nghị chi, Loại chi, Trạng thái, Người lập, Người đề "
     "nghị, Công ty, Phòng ban, Bộ phận, Ngày lập từ, Ngày lập đến\n"
     "- Nút đổi chữ thành 'Ẩn tìm kiếm nâng cao' khi đang mở, bấm lại thì thu gọn"),

    (6, "Ô 'Mã phiếu' của bộ lọc nâng cao độc lập với ô tìm nhanh", "P1",
     "Có phiếu TPE.UNC0826.00014 và phiếu TPE.UNC0826.00013 trong phạm vi xem.",
     "1. Gõ UNC0826 vào ô tìm nhanh\n2. Mở bộ lọc nâng cao, gõ 00014 vào ô 'Mã phiếu'\n"
     "3. Bấm 'Tìm kiếm'",
     "Ô tìm nhanh: UNC0826; Mã phiếu: 00014",
     "- Kết quả phải thoả CẢ HAI điều kiện: chỉ còn TPE.UNC0826.00014\n"
     "- ⚠️ Hai ô này không đè lên nhau, chúng cộng dồn điều kiện"),

    (7, "Lọc theo mã phiếu đề nghị chi", "P0",
     "Phiếu TPE.UNC0826.00014 lập từ đề nghị TPE.DNTT0726.00240.",
     "1. Mở bộ lọc nâng cao\n2. Gõ TPE.DNTT0726.00240 vào ô 'Mã phiếu đề nghị chi'\n"
     "3. Bấm 'Tìm kiếm'",
     "Mã phiếu đề nghị chi: TPE.DNTT0726.00240",
     "- Trả về đúng những phiếu ủy nhiệm chi lập từ đề nghị đó\n"
     "- Cột 'Mã phiếu đề nghị chi' của mọi dòng đều hiển thị đúng mã vừa lọc"),

    (8, "Danh sách giá trị của ô lọc Loại chi", "P0",
     "Đang mở bộ lọc nâng cao.",
     "1. Bấm ô 'Loại chi'\n2. Liệt kê toàn bộ lựa chọn",
     "—",
     "- Đúng 6 lựa chọn: Chi trả nhà cung cấp, Chi trả lại khách hàng, Chi thưởng NVKD, Chi "
     "thưởng thực hiện hợp đồng, Chi khác, Thanh toán chi phí vận chuyển NCC\n"
     "- ⚠️ KHÔNG có 'Chi thu nhập cho nhân viên' — cố ý giữ giống hệ thống cũ, dù phiếu loại đó "
     "vẫn hiện trong danh sách"),

    (9, "Lọc theo Loại chi", "P0",
     "Trong phạm vi xem có nhiều phiếu 'Chi trả nhà cung cấp' và ít nhất 1 phiếu loại khác.",
     "1. Chọn Loại chi = 'Chi trả nhà cung cấp'",
     "Loại chi: Chi trả nhà cung cấp",
     "- Danh sách lọc lại NGAY khi chọn, không cần bấm Tìm kiếm\n"
     "- Mọi dòng đều có cột 'Loại chi' = 'Chi trả nhà cung cấp'"),

    (10, "Danh sách giá trị của ô lọc Trạng thái", "P0",
     "Đang mở bộ lọc nâng cao.",
     "1. Bấm ô 'Trạng thái'\n2. Liệt kê lựa chọn",
     "—",
     "- Đúng 2 lựa chọn: 'Đang tạo' và 'Đã hạch toán'\n"
     "- ⚠️ KHÔNG có 'Chờ duyệt' và 'Hủy' — hai trạng thái này không có thao tác nào tạo ra"),

    (11, "Lọc theo trạng thái Đang tạo", "P0",
     "Tài khoản đang đăng nhập có đúng 1 phiếu nháp do chính mình lập.",
     "1. Chọn Trạng thái = 'Đang tạo'",
     "Trạng thái: Đang tạo",
     "- Chỉ hiện phiếu nháp của chính người đang đăng nhập\n"
     "- Không lẫn phiếu nháp của người khác"),

    (12, "Lọc theo Người lập", "P0",
     "Tài khoản DNS Admin đã lập 14 phiếu trong phạm vi xem.",
     "1. Chọn Người lập = DNS Admin",
     "Người lập: DNS Admin",
     "- Mọi dòng có cột 'Người tạo' = DNS Admin\n- Số dòng khớp số phiếu người đó lập"),

    (13, "Lọc theo Người đề nghị", "P0",
     "Có ít nhất 1 phiếu lập từ đề nghị do Vũ Thị Nhài lập.",
     "1. Chọn Người đề nghị = Vũ Thị Nhài",
     "Người đề nghị: Vũ Thị Nhài",
     "- Mọi dòng có cột 'Người đề nghị' = Vũ Thị Nhài\n"
     "- ⚠️ 'Người đề nghị' là người lập PHIẾU ĐỀ NGHỊ, khác 'Người tạo' là người lập phiếu ủy "
     "nhiệm chi — hai cột này thường khác nhau"),

    (14, "Lọc theo Công ty", "P0",
     "Trong phạm vi xem có phiếu của ít nhất 2 công ty.",
     "1. Chọn Công ty = một công ty có phiếu",
     "Công ty: công ty đang có phiếu",
     "- Chỉ còn phiếu của công ty đã chọn\n- Tổng số bản ghi giảm đúng theo số phiếu công ty đó"),

    (15, "Lọc theo Phòng ban và Bộ phận", "P1",
     "Trong phạm vi xem có phiếu thuộc nhiều phòng ban.",
     "1. Chọn Phòng ban = một phòng đang có phiếu\n2. Chọn tiếp Bộ phận",
     "Phòng ban: PHÒNG KẾ TOÁN TÀI VỤ",
     "- Danh sách thu hẹp theo đúng phòng ban / bộ phận của người lập phiếu\n"
     "- Hai ô cộng dồn điều kiện với nhau"),

    (16, "Lọc theo khoảng ngày lập — cả hai đầu mút", "P0",
     "Có phiếu tạo đúng ngày 21/08/2026 và phiếu tạo đúng ngày 28/08/2026.",
     "1. Chọn Ngày lập từ = 21/08/2026\n2. Chọn Ngày lập đến = 28/08/2026",
     "Ngày lập từ: 21/08/2026; Ngày lập đến: 28/08/2026",
     "- ⚠️ Phiếu tạo ĐÚNG ngày 21/08 và ĐÚNG ngày 28/08 đều nằm trong kết quả\n"
     "- Phiếu tạo ngày 20/08 và 29/08 bị loại\n"
     "- Ô ngày hiển thị dạng ngày/tháng/năm"),

    (17, "Chỉ điền một đầu của khoảng ngày", "P1",
     "Có phiếu tạo trước và sau ngày 27/08/2026.",
     "1. Chỉ chọn Ngày lập từ = 27/08/2026, để trống ô đến\n2. Làm mới rồi chỉ chọn Ngày lập đến "
     "= 22/08/2026",
     "Ngày lập từ: 27/08/2026 · Ngày lập đến: 22/08/2026",
     "- Lần 1: chỉ phiếu tạo từ 27/08/2026 trở về sau\n"
     "- Lần 2: chỉ phiếu tạo từ 22/08/2026 trở về trước"),

    (18, "Khoảng ngày đảo ngược", "P2",
     "Đang ở màn danh sách.",
     "1. Chọn Ngày lập từ = 28/08/2026\n2. Chọn Ngày lập đến = 21/08/2026",
     "Ngày lập từ: 28/08/2026; Ngày lập đến: 21/08/2026",
     "- Kết quả rỗng, hiện 'Không có dữ liệu phù hợp bộ lọc.'\n- Không lỗi, không treo trang"),

    (19, "Kết hợp nhiều ô lọc", "P0",
     "Có ít nhất 1 phiếu thoả đồng thời: loại Chi trả nhà cung cấp, trạng thái Đã hạch toán, "
     "người lập DNS Admin, tạo trong tháng 08/2026.",
     "1. Chọn lần lượt Loại chi, Trạng thái, Người lập và khoảng ngày lập\n2. Đọc tổng bản ghi",
     "Loại chi: Chi trả nhà cung cấp; Trạng thái: Đã hạch toán; Người lập: DNS Admin; "
     "Ngày lập từ 01/08/2026 đến 31/08/2026",
     "- Mọi điều kiện được cộng dồn (thoả TẤT CẢ mới hiện)\n"
     "- Tổng bản ghi khớp số đếm thủ công trên dữ liệu"),

    (20, "Nút Làm mới xoá hết điều kiện", "P0",
     "Đang có 4 ô lọc được đặt giá trị và danh sách đang thu hẹp.",
     "1. Bấm 'Làm mới'",
     "—",
     "- Mọi ô lọc trở về trống, ô tìm nhanh trống\n- Danh sách quay về đủ bản ghi trong phạm vi quyền\n"
     "- Trang quay về trang 1"),

    (21, "Ghi nhớ bộ lọc khi rời màn rồi quay lại", "P1",
     "Đã đặt Loại chi = 'Chi khác' rồi mở màn chi tiết một phiếu.",
     "1. Đặt bộ lọc\n2. Bấm vào mã phiếu để mở chi tiết\n3. Bấm 'Quay lại'",
     "Loại chi: Chi khác",
     "- Bộ lọc vừa đặt vẫn còn nguyên, không phải chọn lại\n"
     "- Hệ thống chỉ ghi nhớ trong khoảng 10 phút và chỉ khi còn ở trong màn này"),

    (22, "Cài đặt bộ lọc — bật tắt và sắp xếp ô lọc", "P1",
     "Đang ở màn danh sách.",
     "1. Bấm 'Cài đặt bộ lọc'\n2. Bỏ tích ô 'Bộ phận'\n3. Bấm 'Lưu'\n4. Mở lại bộ lọc nâng cao",
     "Bỏ tích: Bộ phận",
     "- Cửa sổ liệt kê 10 mục lọc có thể bật tắt và kéo đổi thứ tự\n"
     "- Sau khi lưu, ô 'Bộ phận' không còn trong bộ lọc nâng cao\n"
     "- Bấm 'Khôi phục mặc định' đưa về đủ 10 mục"),
]

S3 = [
    (1, "Đủ cột mặc định trên lưới", "P0",
     "Tài khoản chưa từng đổi cấu hình cột.",
     "1. Vào màn danh sách\n2. Cuộn ngang hết bảng và đọc tên từng cột",
     "—",
     "- 11 cột hiện mặc định theo thứ tự: STT, Mã phiếu, Mã phiếu đề nghị chi, Loại chi, Người "
     "đề nghị, Ngày tạo, Người tạo, Ngày cập nhật, Người cập nhật, Trạng thái, Hành động\n"
     "- ⚠️ Hai cột 'Số tiền duyệt chi' và 'Ngày hạch toán' MẶC ĐỊNH ẨN"),

    (2, "Bật hai cột ẩn mặc định", "P0",
     "Đang ở màn danh sách với cấu hình cột mặc định.",
     "1. Bấm nút biểu tượng cột bên phải nút 'Tạo mới'\n2. Tích 'Số tiền duyệt chi' và 'Ngày "
     "hạch toán'\n3. Bấm 'Lưu'",
     "—",
     "- Cửa sổ có tiêu đề 'Tuỳ chỉnh cột'\n"
     "- Sau khi lưu, hai cột xuất hiện trên lưới với số tiền có dấu ngăn hàng nghìn"),

    (3, "Ba cột bị khoá không tắt được", "P0",
     "Đang mở cửa sổ 'Tuỳ chỉnh cột'.",
     "1. Thử bỏ tích cột 'STT'\n2. Thử bỏ tích 'Mã phiếu'\n3. Thử bỏ tích 'Hành động'\n"
     "4. Thử kéo đổi vị trí 3 cột đó",
     "—",
     "- Cả 3 cột có biểu tượng ổ khoá, không bỏ tích được và không kéo được\n"
     "- Rê chuột hiện chú thích 'Cột bắt buộc — không thể ẩn hoặc đổi vị trí'"),

    (4, "Kéo đổi thứ tự cột", "P1",
     "Đang mở cửa sổ 'Tuỳ chỉnh cột'.",
     "1. Kéo cột 'Trạng thái' lên trên cột 'Ngày tạo'\n2. Bấm 'Lưu'",
     "—",
     "- Lưới hiển thị đúng thứ tự vừa kéo"),

    (5, "Cấu hình cột được nhớ sau khi tải lại trang", "P1",
     "Vừa lưu cấu hình cột ở bước trước.",
     "1. Nhấn F5 tải lại trang\n2. Đăng xuất rồi đăng nhập lại, mở lại màn",
     "—",
     "- Cấu hình cột giữ nguyên cho tài khoản đó\n- Tài khoản khác không bị ảnh hưởng"),

    (6, "Sắp xếp mặc định", "P0",
     "Danh sách vừa mở, chưa bấm sắp xếp.",
     "1. Đọc cột 'Ngày tạo' của 10 dòng đầu",
     "—",
     "- Sắp xếp theo Ngày tạo giảm dần: phiếu mới nhất đứng đầu\n"
     "- Mũi tên sắp xếp đang bám ở tiêu đề cột 'Ngày tạo'"),

    (7, "Sắp xếp theo Mã phiếu", "P1",
     "Danh sách có nhiều hơn 1 trang.",
     "1. Bấm tiêu đề cột 'Mã phiếu'\n2. Bấm lần nữa",
     "—",
     "- Lần 1 sắp xếp tăng dần, lần 2 giảm dần\n- Thứ tự áp dụng trên TOÀN BỘ dữ liệu, không chỉ trang hiện tại"),

    (8, "Sắp xếp theo Số tiền duyệt chi", "P0",
     "Đã bật cột 'Số tiền duyệt chi'; danh sách có phiếu tiền lớn và phiếu 0 đồng.",
     "1. Bấm tiêu đề cột 'Số tiền duyệt chi' để sắp xếp giảm dần\n2. Bấm lần nữa để tăng dần",
     "—",
     "- Giảm dần: phiếu 51,111,111,111 đứng trước phiếu 1,006,319,600\n"
     "- Tăng dần: phiếu 0 đồng (phiếu nháp chưa nhập tiền) đứng đầu"),

    (9, "Sắp xếp theo các cột còn lại", "P1",
     "Đã bật đủ cột.",
     "1. Lần lượt bấm tiêu đề 'Trạng thái', 'Ngày hạch toán', 'Ngày cập nhật'",
     "—",
     "- Cả 3 cột sắp xếp được cả hai chiều\n"
     "- Các cột không có mũi tên (Mã phiếu đề nghị chi, Loại chi, Người đề nghị, Người tạo, "
     "Người cập nhật) thì bấm KHÔNG có tác dụng — đúng thiết kế"),

    (10, "Đổi số dòng mỗi trang", "P0",
     "Danh sách có 2.586 phiếu.",
     "1. Chọn 'Số dòng/trang' = 100\n2. Đếm số dòng hiển thị\n3. Đổi lại về 5",
     "Số dòng/trang: 100, sau đó 5",
     "- Chọn 100: lưới hiện 100 dòng, dòng thông tin 'Hiển thị 1–100 / 2586'\n"
     "- Chọn 5: lưới hiện 5 dòng, số trang tăng lên tương ứng"),

    (11, "Chuyển trang", "P0",
     "Danh sách nhiều trang, đang ở trang 1.",
     "1. Bấm số trang 2\n2. Bấm nút về trang cuối\n3. Bấm nút về trang đầu",
     "—",
     "- Dữ liệu đổi đúng theo trang, dòng 'Hiển thị a–b / N' cập nhật đúng\n"
     "- Ở trang 1 hai nút lùi bị mờ; ở trang cuối hai nút tiến bị mờ"),

    (12, "Lọc xong quay về trang 1", "P1",
     "Đang ở trang 3 của danh sách.",
     "1. Chọn một điều kiện lọc bất kỳ",
     "Trạng thái: Đã hạch toán",
     "- Danh sách nhảy về trang 1 của kết quả mới, không giữ trang 3 cũ"),

    (13, "Liên kết mã phiếu và mã đề nghị", "P0",
     "Dòng đầu là TPE.UNC0826.00014, lập từ đề nghị TPE.DNTT0726.00240.",
     "1. Bấm vào mã phiếu ở cột 'Mã phiếu'\n2. Quay lại, bấm vào mã ở cột 'Mã phiếu đề nghị chi'",
     "—",
     "- Bấm mã phiếu: mở màn chi tiết phiếu ủy nhiệm chi TRONG CÙNG TAB\n"
     "- Bấm mã đề nghị: mở màn chi tiết Phiếu đề nghị thanh toán ở TAB MỚI\n"
     "- Phiếu Chi thu nhập cho nhân viên hiển thị dấu — ở cột này vì không có đề nghị nguồn"),

    (14, "Hiển thị màu trạng thái", "P1",
     "Danh sách có cả phiếu 'Đang tạo' và 'Đã hạch toán'.",
     "1. Quan sát cột 'Trạng thái'",
     "—",
     "- 'Đã hạch toán' hiện nhãn nền xanh lá\n- 'Đang tạo' hiện nhãn xám\n"
     "- Chữ trong nhãn đúng tên trạng thái, không viết tắt"),
]

S4 = [
    (1, "Giá trị điền sẵn khi mở form Tạo mới", "P0",
     "Tài khoản có quyền 'Kế toán thanh toán'. Hôm nay là 04/09/2026.",
     "1. Bấm 'Tạo mới'\n2. Đọc từng ô trên khối 'Thông tin chung'",
     "—",
     "- Tiêu đề màn: 'Thêm phiếu ủy nhiệm chi'\n"
     "- Loại chi điền sẵn 'Chi trả nhà cung cấp'; Ngày hạch toán điền sẵn 04/09/2026; Tỷ giá "
     "điền sẵn 1; Hình thức thanh toán hiện 'CK' và khoá không sửa được\n"
     "- Các ô còn lại để trống, ô Loại tiền / Người đề nghị / Phòng ban / Lý do chi hiện gợi ý "
     "'Theo phiếu đề nghị'\n- Bảng Chi tiết hiện 'Chưa chọn phiếu đề nghị chi'"),

    (2, "Ô Loại chi trên form có đủ 7 loại", "P0",
     "Đang ở form Tạo mới, chưa chọn phiếu đề nghị.",
     "1. Bấm ô 'Loại chi'\n2. Liệt kê lựa chọn",
     "—",
     "- Đúng 7 lựa chọn: Chi trả nhà cung cấp, Chi trả lại khách hàng, Chi thưởng NVKD, Chi thu "
     "nhập cho nhân viên, Chi thưởng thực hiện hợp đồng, Chi khác, Thanh toán chi phí vận chuyển "
     "NCC\n- ⚠️ Nhiều hơn ô lọc ngoài danh sách (6 loại) đúng một loại: 'Chi thu nhập cho nhân viên'"),

    (3, "Ô Loại chi không xoá trắng được", "P1",
     "Đang ở form Tạo mới.",
     "1. Rê chuột vào ô 'Loại chi' tìm dấu × để xoá lựa chọn",
     "—",
     "- Không có dấu × — chỉ đổi được sang loại khác, không bỏ trống được"),

    (4, "Mở cửa sổ chọn phiếu đề nghị chi", "P0",
     "Có 66 phiếu đề nghị đang Chờ tạo phiếu chi theo hình thức chuyển khoản.",
     "1. Bấm vào ô 'Số phiếu đề nghị'",
     "—",
     "- Mở cửa sổ 'Chọn phiếu đề nghị chi', dòng phụ đề ghi 'Chỉ phiếu Chờ tạo phiếu chi, hình "
     "thức chuyển khoản'\n"
     "- Bảng có 7 cột: STT, Mã phiếu đề nghị, Loại chi, Khách hàng / Nhà cung cấp, Số tiền, "
     "Người lập, Ngày lập\n- Dòng thông tin 'Hiển thị 1–10 / 66 phiếu'"),

    (5, "Cửa sổ chọn đề nghị chỉ có đề nghị chuyển khoản", "P0",
     "Trong hệ thống có cả đề nghị tiền mặt và đề nghị chuyển khoản đang Chờ tạo phiếu chi.",
     "1. Mở cửa sổ chọn đề nghị\n2. Đối chiếu danh sách với danh sách bên màn Phiếu chi tiền",
     "—",
     "- Danh sách ở đây và danh sách bên màn Phiếu chi tiền KHÔNG có mã nào trùng nhau\n"
     "- ⚠️ Đây là điểm phân biệt duy nhất giữa hai màn — chấm kỹ"),

    (6, "Bộ lọc trong cửa sổ chọn đề nghị", "P0",
     "Cửa sổ đang mở với 66 phiếu.",
     "1. Bấm ô 'Loại chi' trong cửa sổ, liệt kê lựa chọn\n2. Chọn 'Chi trả nhà cung cấp'\n"
     "3. Gõ một mã vào ô 'Mã phiếu đề nghị', bấm 'Tìm kiếm'\n4. Chọn một 'Người lập'",
     "Loại chi: Chi trả nhà cung cấp",
     "- Ô Loại chi CHỈ có 4 lựa chọn: Chi trả nhà cung cấp, Chi trả lại khách hàng, Chi thưởng "
     "thực hiện hợp đồng, Thanh toán chi phí vận chuyển NCC\n"
     "- Chọn loại chi hoặc người lập thì tìm ngay; ô gõ tay phải bấm 'Tìm kiếm' hoặc Enter\n"
     "- Nút 'Làm mới' xoá hết điều kiện trong cửa sổ"),

    (7, "Chọn một phiếu đề nghị và kiểm tra dữ liệu tự điền", "P0",
     "Đề nghị TPE.DNTT0826.00018 của nhà cung cấp CÔNG TY CỔ PHẦN CÔNG NGHỆ HỢP LONG, 1 dòng chi "
     "tiết trị giá 50,000 nguyên tệ.",
     "1. Trong cửa sổ, bấm vào dòng TPE.DNTT0826.00018\n2. Đọc lại toàn bộ form",
     "—",
     "- Ô 'Số phiếu đề nghị' hiện đúng mã vừa chọn, cửa sổ tự đóng\n"
     "- Tài khoản có tự điền '1121 - Tiền Việt Nam'; Tài khoản nợ tự điền '3311 - Phải trả cho "
     "người bán ngắn hạn'\n"
     "- Loại tiền, Tỷ giá, Người đề nghị, Phòng ban, Lý do chi, Nhà cung cấp được điền theo phiếu "
     "đề nghị và ở chế độ chỉ đọc\n"
     "- Hiện thêm khối 'TÀI KHOẢN NHẬN TIỀN' với Số tài khoản, Tên tài khoản, Tên ngân hàng, Chi "
     "nhánh, Thành phố\n"
     "- Bảng Chi tiết nạp đúng số dòng của đề nghị, cột 'Số tiền duyệt chi' điền sẵn BẰNG ĐÚNG "
     "'Số tiền đề nghị chi'"),

    (8, "Chọn đề nghị xong thì Loại chi bị khoá", "P0",
     "Vừa chọn xong một phiếu đề nghị loại Chi trả nhà cung cấp.",
     "1. Thử bấm vào ô 'Loại chi' để đổi sang loại khác",
     "—",
     "- Ô 'Loại chi' đã khoá, không đổi được\n"
     "- Muốn đổi loại phải bỏ phiếu đề nghị và làm lại từ đầu"),

    (9, "Nhà cung cấp nước ngoài hiện thêm hai khối ngân hàng", "P1",
     "Đề nghị TPE.DNTT0726.00240 của nhà cung cấp nước ngoài, tiền tệ USD.",
     "1. Chọn phiếu đề nghị đó\n2. Cuộn xuống khối ngân hàng",
     "—",
     "- Hiện 2 nhóm: 'NGÂN HÀNG' và 'NGÂN HÀNG TRUNG GIAN', mỗi nhóm có Số tài khoản, Tài khoản, "
     "Tên ngân hàng, Swift Code, IBAN Number, Địa chỉ\n"
     "- Hiện thêm ô 'Phí' (ví dụ 'Phí chia sẻ cho 2 bên')\n"
     "- Khối 'TÀI KHOẢN NHẬN TIỀN' KHÔNG hiện với nhà cung cấp nước ngoài"),

    (10, "Chọn phương thức thanh toán", "P0",
     "Đang ở form đã chọn đề nghị.",
     "1. Bấm ô 'Phương thức thanh toán'\n2. Liệt kê lựa chọn và chọn 'Tiền tự có'",
     "Phương thức thanh toán: Tiền tự có",
     "- Đúng 2 lựa chọn: 'Tiền tự có' và 'Tiền vay'"),

    (11, "Chọn ngân hàng chuyển tự điền tên và lọc số tài khoản", "P0",
     "Doanh nghiệp có 32 tài khoản ngân hàng, trong đó 9 tài khoản thuộc ngân hàng MB.",
     "1. Chọn 'Ngân hàng chuyển' = MB\n2. Bấm ô 'Số tài khoản chuyển khoản' và đếm lựa chọn",
     "Ngân hàng chuyển: MB - Ngân hàng Thương mại Cổ phần Quân đội",
     "- Ô số tài khoản chỉ còn 9 lựa chọn của ngân hàng MB\n"
     "- Hệ thống KHÔNG tự chọn giúp vì có nhiều hơn 1 tài khoản\n"
     "- ⚠️ Nếu ngân hàng chỉ có ĐÚNG 1 tài khoản và phương thức là 'Tiền tự có' thì hệ thống tự "
     "chọn luôn tài khoản đó"),

    (12, "Đổi ngân hàng chuyển thì xoá số tài khoản đang chọn", "P1",
     "Đã chọn ngân hàng MB và một số tài khoản của MB.",
     "1. Đổi 'Ngân hàng chuyển' sang VIETCOMBANK",
     "Ngân hàng chuyển: VIETCOMBANK",
     "- Ô 'Số tài khoản chuyển khoản' bị xoá trắng, không giữ tài khoản cũ của MB\n"
     "- Danh sách lựa chọn đổi sang tài khoản của VIETCOMBANK"),

    (13, "Sửa số tiền duyệt chi trên dòng chi tiết", "P0",
     "Dòng chi tiết có 'Số tiền đề nghị chi' = 50,000 nguyên tệ, tỷ giá 2,564.",
     "1. Sửa ô 'Số tiền duyệt chi' của dòng thành 30,000\n2. Đọc cột quy đổi và dòng Tổng cộng",
     "Số tiền duyệt chi: 30,000",
     "- Cột quy đổi tự tính lại = 30,000 × 2,564\n- Dòng 'Tổng cộng' cập nhật theo"),

    (14, "Đổi tỷ giá thì tính lại toàn bảng", "P1",
     "Bảng chi tiết có 2 dòng, tiền tệ là ngoại tệ.",
     "1. Đổi ô 'Tỷ giá (VND)' sang một giá trị khác\n2. Đọc lại cột quy đổi của cả 2 dòng và "
     "dòng Tổng cộng",
     "Tỷ giá: 25,000",
     "- Cột quy đổi của MỌI dòng tính lại theo tỷ giá mới\n- Dòng Tổng cộng khớp với tổng các dòng"),

    (15, "Nhập ghi chú cho dòng chi tiết", "P2",
     "Bảng chi tiết có ít nhất 1 dòng.",
     "1. Gõ nội dung vào ô 'Ghi chú' của dòng\n2. Lưu nháp rồi mở lại phiếu",
     "Ghi chú: Chuyển đợt 1",
     "- Nội dung ghi chú được lưu và hiện lại đúng khi mở lại phiếu"),

    (16, "Chuyển sang Loại chi 'Chi thu nhập cho nhân viên'", "P0",
     "Đang ở form Tạo mới, chưa chọn phiếu đề nghị.",
     "1. Chọn Loại chi = 'Chi thu nhập cho nhân viên'\n2. Đọc lại toàn bộ form",
     "Loại chi: Chi thu nhập cho nhân viên",
     "- ẨN các ô: Số phiếu đề nghị, Tài khoản nợ, Ngày hạch toán, Phương thức thanh toán\n"
     "- HIỆN thêm: 'Người nhận' (bắt buộc), 'Phòng ban' dạng chọn với gợi ý 'Chọn phòng ban chi' "
     "(bắt buộc), 'Lý do chi' chuyển thành ô nhập tay (bắt buộc)\n"
     "- Tài khoản có bị khoá ở '1121 - Tiền Việt Nam'; Loại tiền khoá ở VietNamDong; Tỷ giá = 1\n"
     "- Người đề nghị điền sẵn tên người đang đăng nhập\n"
     "- Bảng chi tiết hiện 'Chưa chọn phòng ban chi — chọn phòng ban để hệ thống lấy số liệu thu "
     "nhập nhân viên.'"),

    (17, "Chọn phòng ban để hút số liệu nhân viên", "P0",
     "Phòng ban PHÒNG KINH DOANH có nhân viên còn số dư thu nhập chưa chi.",
     "1. Chọn 'Phòng ban' = PHÒNG KINH DOANH\n2. Chờ bảng nạp xong",
     "Phòng ban: PHÒNG KINH DOANH",
     "- Trong lúc chờ hiện 'Đang lấy số liệu nhân viên...'\n"
     "- Bảng nạp mỗi nhân viên một dòng, kèm cột Số dư, Số tiền chi, Tài khoản, Tên ngân hàng, "
     "Chi nhánh\n- Nhân viên không còn khoản nào thì không xuất hiện"),

    (18, "Phòng ban không có số liệu", "P1",
     "Chọn một phòng ban không có nhân viên nào còn số dư thu nhập.",
     "1. Chọn phòng ban đó",
     "Phòng ban: một phòng không có số dư",
     "- Bảng hiện 'Không có dữ liệu phù hợp'\n- Vẫn thấy đủ tiêu đề cột, không lỗi trang"),

    (19, "Hai tab của bảng nhân viên", "P0",
     "Bảng nhân viên đã có dữ liệu.",
     "1. Đọc tab 'Chi tiết'\n2. Chuyển sang tab 'Chi tiết vụ việc'",
     "—",
     "- Tab 'Chi tiết': ô tích 'Cần thanh toán', STT, Số tài khoản nợ, Tên tài khoản, Nhân viên, "
     "Số dư, Số tiền chi, Tài khoản, Tên ngân hàng, Chi nhánh, dòng Tổng cộng\n"
     "- Tab 'Chi tiết vụ việc': nhóm 'Số dư' và nhóm 'Số tiền chi', mỗi nhóm 5 khoản Chênh lệch "
     "lương, Hoa hồng tháng, Hoa hồng quý, Thưởng quý, Tiền vận chuyển kèm cột Tổng cộng\n"
     "- ⚠️ Đúng 5 khoản, KHÔNG có khoản 'Chi phí khác' — cố ý khác màn Phiếu chi tiền, vì khoản "
     "đó nếu có thì tiền nhập vào sẽ không bao giờ vào sổ kế toán"),

    (20, "Bỏ tích 'Cần thanh toán' của một nhân viên", "P0",
     "Bảng nhân viên có ít nhất 3 dòng, mặc định tất cả đều được tích.",
     "1. Bỏ tích ô đầu dòng của nhân viên thứ hai\n2. Quan sát dòng đó\n3. Lưu nháp rồi mở lại phiếu",
     "—",
     "- Dòng bị mờ đi, mọi ô nhập của dòng bị khoá\n"
     "- Sau khi lưu, dòng đó KHÔNG được ghi vào phiếu\n"
     "- Ô tích đầu bảng cho phép chọn / bỏ chọn tất cả cùng lúc"),

    (21, "Khoá ô nhập khi chưa khai tổng số tiền chi", "P0",
     "Nhân viên A đang có 'Số tiền chi' = 0 ở tab 'Chi tiết'.",
     "1. Sang tab 'Chi tiết vụ việc', thử gõ vào 5 ô khoản của nhân viên A\n"
     "2. Quay lại tab 'Chi tiết', nhập 'Số tiền chi' = 5,000,000\n3. Sang lại tab vụ việc",
     "Số tiền chi: 5,000,000",
     "- Trước khi khai tổng: 5 ô khoản bị khoá\n- Sau khi khai tổng: 5 ô mở ra cho nhập"),

    (22, "Tài khoản nợ dòng đầu áp cho mọi dòng", "P1",
     "Bảng nhân viên có 4 dòng, tài khoản nợ mỗi dòng đang là giá trị mặc định.",
     "1. Đổi 'Số tài khoản nợ' của DÒNG ĐẦU TIÊN sang một tài khoản khác\n2. Đọc cột đó ở 3 dòng còn lại",
     "—",
     "- Cả 3 dòng còn lại tự đổi theo dòng đầu\n"
     "- Đổi tài khoản nợ ở dòng thứ hai trở đi thì chỉ đổi riêng dòng đó"),

    (23, "Mở màn Sửa từ danh sách", "P0",
     "Có phiếu nháp TPE.UNC0826.00013 do chính người đang đăng nhập lập.",
     "1. Ở cột 'Hành động' bấm biểu tượng bút chì của dòng đó",
     "—",
     "- Mở màn 'Sửa phiếu ủy nhiệm chi', dữ liệu nạp đúng phiếu\n"
     "- Hiện thêm 3 ô chỉ đọc: 'Mã phiếu', 'Người lập', 'Ngày lập'\n"
     "- Ô 'Loại chi' bị khoá, không đổi được ở màn Sửa"),

    (24, "Ngày hạch toán nạp đúng ở màn Sửa", "P0",
     "Phiếu nháp có Ngày hạch toán = 28/08/2026.",
     "1. Mở màn Sửa phiếu đó\n2. Đọc ô 'Ngày hạch toán'",
     "—",
     "- Ô hiển thị đúng 28/08/2026 theo định dạng ngày/tháng/năm\n"
     "- ⚠️ Kiểm kỹ với ngày có phần ngày lớn hơn 12 (ví dụ 28) — đây là chỗ từng sai"),

    (25, "Ngày hạch toán không chọn được ngày quá khứ", "P0",
     "Hôm nay là 04/09/2026, đang ở form Tạo mới.",
     "1. Bấm ô 'Ngày hạch toán' mở lịch\n2. Thử chọn ngày 03/09/2026",
     "—",
     "- Mọi ngày trước hôm nay bị làm mờ, không bấm chọn được\n"
     "- Chọn được từ 04/09/2026 trở đi"),

    (26, "Cảnh báo chưa lưu khi rời form", "P0",
     "Đang ở form Tạo mới và đã chọn một phiếu đề nghị.",
     "1. Bấm nút 'Quay lại' ở chân form",
     "—",
     "- Hiện cửa sổ 'Thông tin chưa lưu' với nội dung 'Bạn có thông tin chưa lưu. Có chắc chắn "
     "muốn thoát?'\n- Nút 'Thoát' (đỏ) rời màn, nút 'Ở lại' đóng cửa sổ và giữ nguyên dữ liệu"),

    (27, "Không cảnh báo khi chưa sửa gì", "P1",
     "Vừa mở form Tạo mới, chưa chạm vào ô nào.",
     "1. Bấm 'Quay lại'",
     "—",
     "- Về thẳng màn danh sách, KHÔNG hỏi gì"),

    (28, "Không cảnh báo sau khi lưu thành công", "P1",
     "Vừa bấm 'Lưu nháp' và hệ thống báo thành công.",
     "1. Quan sát điều hướng",
     "—",
     "- Tự về màn danh sách, không hiện cửa sổ 'Thông tin chưa lưu'"),

    (29, "Màn xem chi tiết chỉ đọc", "P0",
     "Phiếu TPE.UNC0826.00014 đã hạch toán.",
     "1. Bấm mã phiếu để mở chi tiết\n2. Thử gõ vào các ô",
     "—",
     "- Tiêu đề: 'Chi tiết phiếu ủy nhiệm chi: TPE.UNC0826.00014'\n"
     "- Mọi ô chỉ đọc, không gõ được, không mở được cửa sổ chọn đề nghị\n"
     "- Chân màn chỉ có nút 'Quay lại'\n- Cuối trang có khối 'Lịch sử' đang thu gọn"),

    (30, "Số liệu màn chi tiết khớp dữ liệu gốc", "P0",
     "Phiếu TPE.UNC0826.00014: đề nghị TPE.DNTT0726.00240, tiền tệ USD, tỷ giá 26,510, 1 dòng "
     "chi tiết 37,960 USD.",
     "1. Mở màn chi tiết\n2. Đối chiếu từng ô với phiếu đề nghị nguồn",
     "—",
     "- Số phiếu đề nghị, Loại chi, Ngày hạch toán, Người đề nghị, Phòng ban, Lý do chi, Nhà "
     "cung cấp khớp phiếu đề nghị\n"
     "- Bảng chi tiết: 1 dòng 'ZELL 0726 HP', đề nghị chi 37,960 USD tương đương 1,006,319,600 "
     "đồng, duyệt chi bằng đúng số đó\n- Dòng 'Tổng cộng' khớp"),

    (31, "Xem lịch sử thay đổi từ danh sách", "P1",
     "Phiếu bất kỳ trong danh sách.",
     "1. Bấm biểu tượng đồng hồ ở cột 'Hành động'",
     "—",
     "- Mở cửa sổ 'Lịch sử thay đổi' kèm dòng 'Phiếu: <mã phiếu>'\n"
     "- Phiếu chưa từng bị sửa thì hiện 'Chưa có lịch sử thao tác nào.'\n"
     "- Nút 'Đóng' đóng cửa sổ\n- ⚠️ Nút Lịch sử LUÔN hiện với mọi dòng, kể cả phiếu đã hạch toán"),

    (32, "Xem lịch sử ngay trong màn chi tiết", "P1",
     "Đang ở màn chi tiết một phiếu đã từng bị sửa.",
     "1. Bấm 'Xem lịch sử' ở khối 'Lịch sử' cuối trang",
     "—",
     "- Khối mở ra, hiện các lần thay đổi với giá trị cũ và giá trị mới\n"
     "- Có nút 'Làm mới' và 'Thu gọn'\n"
     "- Nội dung giống hệt cửa sổ Lịch sử mở từ danh sách"),
]

S5 = [
    (1, "Lưu nháp chỉ cần chọn Loại chi", "P0",
     "Tài khoản có quyền 'Kế toán thanh toán'. Vừa mở form Tạo mới, chưa nhập gì ngoài giá trị "
     "điền sẵn.",
     "1. Bấm ngay nút 'Lưu nháp'",
     "—",
     "- Lưu thành công, hệ thống báo thêm phiếu thành công và quay về danh sách\n"
     "- Phiếu mới có mã dạng <mã công ty>.UNC<tháng năm>.<5 chữ số>, ví dụ TPE.UNC0926.00001\n"
     "- Trạng thái 'Đang tạo', cột 'Số tiền duyệt chi' hiển thị 0\n"
     "- ⚠️ Đường 'Lưu nháp' CỐ Ý chỉ bắt buộc Loại chi — các ô còn lại trống vẫn lưu được"),

    (2, "Lưu nháp không đụng sổ kế toán và không đổi trạng thái đề nghị", "P0",
     "Đề nghị TPE.DNTT0826.00018 đang ở trạng thái Chờ tạo phiếu chi.",
     "1. Lập phiếu từ đề nghị đó và bấm 'Lưu nháp'\n2. Mở màn Phiếu đề nghị thanh toán, tra lại "
     "trạng thái của TPE.DNTT0826.00018\n3. Kiểm tra sổ kế toán",
     "—",
     "- Phiếu đề nghị VẪN ở trạng thái Chờ tạo phiếu chi\n"
     "- KHÔNG có bút toán nào được sinh ra"),

    (3, "Lưu nháp được với ngày hạch toán trong quá khứ", "P0",
     "Phiếu nháp lập từ hôm qua có Ngày hạch toán = ngày hôm qua.",
     "1. Mở màn Sửa phiếu nháp đó\n2. Không đổi gì, bấm 'Lưu nháp'",
     "—",
     "- Lưu thành công, không báo lỗi ngày\n"
     "- ⚠️ Cùng phiếu đó bấm 'Lưu và duyệt' thì bị chặn — xem trường hợp bên dưới"),

    (4, "Hộp xác nhận trước khi Lưu và duyệt", "P0",
     "Đang ở form Tạo mới.",
     "1. Bấm 'Lưu và duyệt'",
     "—",
     "- Hiện cửa sổ 'Xác nhận lưu và duyệt' với nội dung 'Bạn đồng ý lưu và duyệt?'\n"
     "- Có nút 'Xác nhận' và nút 'Hủy'\n- Bấm 'Hủy' thì đóng cửa sổ, không lưu gì"),

    (5, "Lưu và duyệt với form trống báo đủ lỗi", "P0",
     "Vừa mở form Tạo mới, chưa nhập gì.",
     "1. Bấm 'Lưu và duyệt'\n2. Bấm 'Xác nhận'",
     "—",
     "- Hiện thông báo đỏ ở góc phải 'Vui lòng kiểm tra lại dữ liệu nhập'\n"
     "- 6 ô viền đỏ kèm chữ 'Bắt buộc nhập' ngay dưới ô: Số phiếu đề nghị, Tài khoản có, Tài "
     "khoản nợ, Phương thức thanh toán, Ngân hàng chuyển, Số tài khoản chuyển khoản\n"
     "- Bảng chi tiết cũng có dòng lỗi 'Bắt buộc nhập'\n- KHÔNG có phiếu nào được tạo"),

    (6, "Lưu và duyệt đầy đủ dữ liệu", "P0",
     "Đã chọn đề nghị TPE.DNTT0826.00018, đã chọn phương thức thanh toán, ngân hàng chuyển và số "
     "tài khoản chuyển khoản, ngày hạch toán là hôm nay.",
     "1. Bấm 'Lưu và duyệt'\n2. Bấm 'Xác nhận'",
     "—",
     "- Hệ thống báo duyệt phiếu thành công và quay về danh sách\n"
     "- Phiếu mới có trạng thái 'Đã hạch toán'\n"
     "- Cột 'Hành động' của phiếu này CHỈ còn biểu tượng Lịch sử"),

    (7, "Duyệt xong thì phiếu đề nghị đổi trạng thái", "P0",
     "Đề nghị TPE.DNTT0826.00018 đang ở trạng thái Chờ tạo phiếu chi.",
     "1. Lập phiếu ủy nhiệm chi từ đề nghị đó và 'Lưu và duyệt'\n"
     "2. Mở màn Phiếu đề nghị thanh toán, tra trạng thái đề nghị\n3. Mở lại cửa sổ chọn đề nghị "
     "ở form Tạo mới",
     "—",
     "- Đề nghị KHÔNG còn ở trạng thái Chờ tạo phiếu chi\n"
     "- Đề nghị đó không còn xuất hiện trong cửa sổ chọn đề nghị"),

    (8, "Duyệt xong thì số duyệt chi được đẩy về phiếu đề nghị", "P0",
     "Dòng chi tiết có đề nghị chi 50,000 nhưng duyệt chi chỉ 30,000.",
     "1. Lưu và duyệt phiếu\n2. Mở màn chi tiết phiếu đề nghị nguồn, đọc cột số tiền duyệt chi",
     "Số tiền duyệt chi: 30,000",
     "- Phiếu đề nghị hiển thị số duyệt chi = 30,000 đúng theo phiếu ủy nhiệm chi"),

    (9, "Ngày hạch toán quá khứ bị chặn khi duyệt", "P0",
     "Phiếu nháp lập hôm qua, ngày hạch toán là ngày hôm qua. Hôm nay mở lại.",
     "1. Mở màn Sửa phiếu\n2. Không đổi ngày, bấm 'Lưu và duyệt' rồi 'Xác nhận'",
     "—",
     "- Ô 'Ngày hạch toán' viền đỏ, báo 'Ngày hạch toán không được nhỏ hơn ngày hôm nay'\n"
     "- Phiếu VẪN ở trạng thái 'Đang tạo', không có bút toán nào\n"
     "- ⚠️ Đây là thiết kế CỐ Ý, KHÔNG ghi lỗi. Đổi ngày sang hôm nay rồi duyệt lại thì thành công"),

    (10, "Bút toán bên Có bằng số tiền dòng cuối", "P0",
     "Phiếu có 3 dòng chi tiết, số tiền duyệt chi lần lượt 1,500,000 · 1,381,440 · 1,677,240 "
     "(tổng 4,558,680).",
     "1. Lưu và duyệt phiếu\n2. Tra sổ kế toán các bút toán sinh ra từ phiếu này",
     "—",
     "- Sinh 3 bút toán bên Nợ, mỗi dòng chi tiết một bút toán\n"
     "- Sinh 1 bút toán bên Có với số tiền 1,677,240 (bằng dòng CUỐI), KHÔNG phải 4,558,680\n"
     "- ⚠️ CHẤM ĐẠT — đây là hành vi cố ý giữ y hệt hệ thống cũ, đã được chốt bằng văn bản"),

    (11, "Phiếu loại Chi khác duyệt xong không sinh bút toán", "P1",
     "Có phiếu đề nghị loại 'Chi khác' đang Chờ tạo phiếu chi, hình thức chuyển khoản.",
     "1. Lập phiếu ủy nhiệm chi từ đề nghị đó\n2. Lưu và duyệt\n3. Tra sổ kế toán",
     "Loại chi: Chi khác",
     "- Phiếu chuyển sang 'Đã hạch toán' bình thường\n"
     "- ⚠️ KHÔNG có bút toán nào sinh ra — cố ý giống hệ thống cũ, CHẤM ĐẠT"),

    (12, "Duyệt phiếu Chi thu nhập cho nhân viên", "P1",
     "Phiếu loại 4 với 2 nhân viên, mỗi người đã khai đủ Số tiền chi và 5 khoản khớp tổng.",
     "1. Bấm 'Lưu và duyệt' rồi 'Xác nhận'\n2. Tra sổ kế toán",
     "—",
     "- Lưu thành công, phiếu chuyển 'Đã hạch toán'\n"
     "- Mỗi nhân viên sinh 5 bút toán theo 5 khoản, cộng thêm 2 bút toán tổng\n"
     "- Khoản có giá trị 0 không sinh bút toán"),

    (13, "Tổng 5 khoản lệch với số tiền chi", "P0",
     "Nhân viên A có 'Số tiền chi' = 5,000,000 nhưng tổng 5 khoản ở tab vụ việc chỉ 3,000,000.",
     "1. Bấm 'Lưu và duyệt' rồi 'Xác nhận'",
     "—",
     "- Hệ thống chặn với thông báo 'Tổng số tiền chi theo mã vụ việc và tổng số tiền đề nghị "
     "chi khác nhau!'\n- Không lưu, không sinh bút toán"),

    (14, "Phiếu đã hạch toán không mở được màn Sửa", "P0",
     "Phiếu TPE.UNC0826.00012 đã hạch toán, do chính người đang đăng nhập lập.",
     "1. Mở màn chi tiết\n2. Gõ thẳng đường dẫn màn Sửa của phiếu này",
     "—",
     "- Chân màn chi tiết chỉ có 'Quay lại'\n- Gõ đường dẫn màn Sửa thì bị tự đưa về màn chi tiết"),
]

S6 = [
    (1, "Xóa phiếu nháp từ danh sách", "P0",
     "Người đang đăng nhập có quyền 'Kế toán thanh toán' và có phiếu nháp TPE.UNC0826.00013 do "
     "chính mình lập.",
     "1. Bấm biểu tượng thùng rác ở cột 'Hành động'\n2. Đọc nội dung cửa sổ xác nhận",
     "—",
     "- Cửa sổ 'Xác nhận xóa' với nội dung: Bạn có chắc muốn xóa phiếu ủy nhiệm chi "
     "'TPE.UNC0826.00013'?\n- Có nút 'Xóa' (đỏ) và nút 'Hủy'"),

    (2, "Bấm Hủy trong cửa sổ xác nhận", "P0",
     "Cửa sổ 'Xác nhận xóa' đang mở.",
     "1. Bấm 'Hủy'",
     "—",
     "- Cửa sổ đóng, phiếu vẫn còn nguyên trong danh sách\n- Không có thông báo nào"),

    (3, "Xác nhận xóa", "P0",
     "Cửa sổ 'Xác nhận xóa' đang mở cho phiếu nháp.",
     "1. Bấm 'Xóa'",
     "—",
     "- Hệ thống báo xóa thành công\n- Phiếu biến mất khỏi danh sách, tổng bản ghi giảm 1\n"
     "- Các dòng chi tiết của phiếu cũng bị xoá theo, không để lại dòng mồ côi"),

    (4, "Xóa từ màn chi tiết", "P0",
     "Đang ở màn chi tiết một phiếu nháp của chính mình.",
     "1. Bấm nút 'Xóa' ở chân màn\n2. Bấm 'Xóa' trong cửa sổ xác nhận",
     "—",
     "- Xóa thành công, hệ thống báo xóa phiếu ủy nhiệm chi thành công\n- Tự quay về màn danh sách"),

    (5, "Xóa phiếu nháp không trả trạng thái đề nghị về cũ", "P1",
     "Phiếu nháp lập từ đề nghị TPE.DNTT0826.00018; đề nghị vẫn đang Chờ tạo phiếu chi.",
     "1. Xóa phiếu nháp\n2. Tra lại trạng thái phiếu đề nghị",
     "—",
     "- Đề nghị vẫn Chờ tạo phiếu chi (vì lúc lưu nháp cũng chưa hề đổi trạng thái)\n"
     "- Đề nghị vẫn chọn được trong cửa sổ chọn đề nghị"),

    (6, "Không xóa được phiếu đã hạch toán", "P0",
     "Phiếu đã hạch toán do chính mình lập.",
     "1. Quan sát cột 'Hành động' và chân màn chi tiết",
     "—",
     "- Không có nút Xóa ở cả hai nơi"),

    (7, "Xóa phiếu đã bị người khác xoá trước đó", "P1",
     "Mở 2 tab cùng màn danh sách; tab 1 và tab 2 cùng thấy phiếu nháp X.",
     "1. Ở tab 1 xóa phiếu X thành công\n2. Sang tab 2 (chưa tải lại) bấm Xóa phiếu X",
     "—",
     "- Hệ thống báo dữ liệu đã thay đổi, không treo trang\n- Danh sách tự tải lại và không còn phiếu X"),
]

S7 = [
    (1, "Màn hình không có chức năng In và Xuất Excel", "P1",
     "Đang ở màn danh sách và màn chi tiết một phiếu đã hạch toán.",
     "1. Rà toàn bộ nút trên thanh công cụ danh sách\n2. Rà cột 'Hành động' của các dòng\n"
     "3. Rà chân màn chi tiết",
     "—",
     "- Không có nút In, không có nút Xuất Excel ở bất kỳ vị trí nào\n"
     "- ⚠️ Đây là thiết kế CỐ Ý giữ giống hệ thống cũ, KHÔNG ghi lỗi thiếu chức năng"),
]

S8 = [
    (1, "Số tiền duyệt chi vượt số tiền đề nghị chi", "P0",
     "Dòng chi tiết có 'Số tiền đề nghị chi' = 442,800.",
     "1. Gõ 999,999,999 vào ô 'Số tiền duyệt chi' của dòng đó\n2. Rời khỏi ô",
     "Số tiền duyệt chi: 999,999,999",
     "- Ô viền đỏ, hiện chữ đỏ ngay dưới ô: Không được lớn hơn số tiền đề nghị chi (442,800)\n"
     "- Bấm Lưu nháp hoặc Lưu và duyệt đều bị chặn, thông báo nêu rõ số thứ tự dòng đang sai"),

    (2, "Nhiều dòng cùng vượt số đề nghị", "P1",
     "Bảng có 3 dòng, dòng 1 và dòng 3 bị nhập vượt.",
     "1. Bấm 'Lưu nháp'",
     "—",
     "- Thông báo nêu đúng các dòng đang sai, ví dụ: Số tiền duyệt chi ở dòng 1, 3 đang lớn hơn "
     "số tiền đề nghị chi\n- Không lưu"),

    (3, "Nhập số âm vào số tiền duyệt chi", "P1",
     "Dòng chi tiết đang có số tiền hợp lệ.",
     "1. Gõ -5000 vào ô 'Số tiền duyệt chi'\n2. Rời khỏi ô",
     "Số tiền duyệt chi: -5000",
     "- Ô tự đưa về 0\n- Cột quy đổi và dòng Tổng cộng cập nhật theo"),

    (4, "Số tiền duyệt chi bằng 0 khi duyệt", "P0",
     "Phiếu lập từ đề nghị loại Chi trả nhà cung cấp, dòng duy nhất có số tiền duyệt chi = 0.",
     "1. Bấm 'Lưu và duyệt' rồi 'Xác nhận'",
     "Số tiền duyệt chi: 0",
     "- Ô viền đỏ, báo 'Phải lớn hơn 0'\n- Không lưu"),

    (5, "Nhập chữ vào ô số tiền", "P1",
     "Đang ở bảng chi tiết.",
     "1. Gõ chữ 'abc' vào ô 'Số tiền duyệt chi'",
     "Số tiền duyệt chi: abc",
     "- Ô không nhận ký tự chữ, giữ nguyên giá trị số cũ hoặc để trống\n- Không lỗi trang"),

    (6, "Tỷ giá bằng 0 với phiếu ngoại tệ", "P0",
     "Phiếu lập từ đề nghị dùng ngoại tệ.",
     "1. Xoá ô 'Tỷ giá (VND)' và nhập 0\n2. Bấm 'Lưu và duyệt' rồi 'Xác nhận'",
     "Tỷ giá: 0",
     "- Ô tỷ giá viền đỏ, báo 'Nhập số lớn hơn 0'\n- Không lưu"),

    (7, "Tỷ giá khoá khi tiền tệ là đồng Việt Nam", "P1",
     "Phiếu lập từ đề nghị dùng đồng Việt Nam.",
     "1. Thử sửa ô 'Tỷ giá (VND)'",
     "—",
     "- Ô bị khoá ở giá trị 1, không sửa được"),

    (8, "Bỏ trống Người nhận ở phiếu Chi thu nhập cho nhân viên", "P0",
     "Loại chi = 'Chi thu nhập cho nhân viên', đã chọn phòng ban, bảng có dữ liệu.",
     "1. Để trống ô 'Người nhận'\n2. Bấm 'Lưu và duyệt' rồi 'Xác nhận'",
     "—",
     "- Ô 'Người nhận' viền đỏ, báo bắt buộc nhập\n- Không lưu"),

    (9, "Bỏ trống Lý do chi ở phiếu Chi thu nhập cho nhân viên", "P0",
     "Loại chi = 'Chi thu nhập cho nhân viên', đã điền Người nhận và Phòng ban.",
     "1. Để trống 'Lý do chi'\n2. Bấm 'Lưu và duyệt' rồi 'Xác nhận'",
     "—",
     "- Ô 'Lý do chi' viền đỏ, báo bắt buộc nhập\n- Không lưu"),

    (10, "Bỏ trống Phòng ban ở phiếu Chi thu nhập cho nhân viên", "P0",
     "Loại chi = 'Chi thu nhập cho nhân viên', chưa chọn phòng ban.",
     "1. Điền Người nhận và Lý do chi\n2. Bấm 'Lưu và duyệt' rồi 'Xác nhận'",
     "—",
     "- Ô 'Phòng ban' viền đỏ, báo bắt buộc nhập\n"
     "- Bảng chi tiết cũng báo bắt buộc nhập vì chưa có dòng nào"),

    (11, "Lưu nháp phiếu Chi thu nhập cho nhân viên khi form còn trống", "P1",
     "Vừa chọn Loại chi = 'Chi thu nhập cho nhân viên', chưa nhập gì thêm.",
     "1. Bấm 'Lưu nháp'",
     "—",
     "- Lưu thành công, phiếu vào danh sách với trạng thái 'Đang tạo'\n"
     "- ⚠️ Đường lưu nháp không chạy các luật bắt buộc — đúng thiết kế"),

    (12, "Mở lại phiếu nháp trống rồi lưu nháp lần nữa", "P0",
     "Phiếu nháp lưu ở bước trên, các ô tài khoản còn để trống.",
     "1. Mở màn Sửa phiếu đó\n2. Bấm 'Lưu nháp' ngay",
     "—",
     "- Lưu lại thành công, KHÔNG báo lỗi 'Không tồn tại' ở ô tài khoản\n"
     "- ⚠️ Đây là chỗ từng lỗi: mở lại phiếu nháp trống rồi lưu tiếp phải chạy trơn"),

    (13, "Số tiền chi vượt số dư của nhân viên", "P0",
     "Nhân viên A có 'Số dư' = 2,000,000.",
     "1. Gõ 9,000,000 vào ô 'Số tiền chi' của nhân viên A\n2. Rời khỏi ô",
     "Số tiền chi: 9,000,000",
     "- Ô tự kẹp về đúng 2,000,000\n- Dòng Tổng cộng cập nhật theo"),

    (14, "Khoản âm ở phiếu Chi thu nhập cho nhân viên", "P1",
     "Nhân viên B có khoản 'Chênh lệch lương' ở cột Số dư là số âm (khoản truy thu).",
     "1. Nhập số âm vào ô khoản đó, giá trị tuyệt đối nhỏ hơn số dư\n2. Nhập tiếp một số dương "
     "vào cùng ô đó",
     "Chênh lệch lương: -500,000 rồi 500,000",
     "- Số âm cùng dấu với số dư thì hợp lệ, giữ nguyên\n"
     "- Số dương ngược dấu với số dư thì bị kẹp về 0"),

    (15, "Ô Số tiền chi khoá khi nhân viên không còn số dư", "P1",
     "Nhân viên C có 'Số dư' = 0.",
     "1. Thử gõ vào ô 'Số tiền chi' của nhân viên C",
     "—",
     "- Ô bị khoá, không nhập được"),

    (16, "Ghi chú dài", "P2",
     "Đang ở bảng chi tiết.",
     "1. Gõ một chuỗi rất dài (trên 300 ký tự) vào ô 'Ghi chú'\n2. Lưu nháp và mở lại",
     "Ghi chú: chuỗi dài trên 300 ký tự",
     "- Hệ thống lưu được hoặc cắt về đúng giới hạn, KHÔNG báo lỗi hệ thống, KHÔNG mất phiếu"),

    (17, "Nhập ngày hạch toán bằng tay sai định dạng", "P1",
     "Đang ở form Tạo mới.",
     "1. Gõ tay '32/13/2026' vào ô 'Ngày hạch toán'\n2. Rời khỏi ô",
     "Ngày hạch toán: 32/13/2026",
     "- Ô không nhận giá trị vô lý, trở về trống hoặc giữ ngày cũ\n- Không lỗi trang"),

    (18, "Ngày hạch toán ngày 13 trở đi trong tháng", "P0",
     "Hôm nay là ngày 13 hoặc muộn hơn trong tháng.",
     "1. Chọn ngày hạch toán = hôm nay (ví dụ 28/08/2026)\n2. Khai đủ dữ liệu, bấm 'Lưu và duyệt'",
     "Ngày hạch toán: 28/08/2026",
     "- Lưu thành công\n"
     "- ⚠️ Đây là chỗ từng lỗi nặng: màn không lưu được từ ngày 13 hàng tháng vì đọc nhầm thứ tự "
     "ngày và tháng. Phải test lại mỗi lần có thay đổi liên quan tới ngày"),
]

S9 = [
    (1, "Hai người cùng lập phiếu từ một đề nghị", "P0",
     "Kế toán X và kế toán Y cùng thấy đề nghị TPE.DNTT0826.00018 đang Chờ tạo phiếu chi.",
     "1. X mở cửa sổ chọn đề nghị, chọn TPE.DNTT0826.00018, Lưu nháp\n"
     "2. Y mở cửa sổ chọn đề nghị và tìm đúng mã đó",
     "—",
     "- ⚠️ Đề nghị VẪN xuất hiện với Y và Y vẫn lập được phiếu thứ hai từ đề nghị đó\n"
     "- Đây là điểm hở CỐ Ý giữ giống hệ thống cũ — CHẤM ĐẠT, nhưng ghi chú nhắc nghiệp vụ tự "
     "kiểm soát để không chi hai lần"),

    (2, "Đề nghị đã có phiếu đã hạch toán", "P0",
     "Đề nghị TPE.DNTT0826.00018 đã có một phiếu ủy nhiệm chi ở trạng thái 'Đã hạch toán'.",
     "1. Mở cửa sổ chọn đề nghị và tìm mã đó",
     "—",
     "- Đề nghị KHÔNG còn xuất hiện, vì trạng thái của nó đã rời khỏi Chờ tạo phiếu chi"),

    (3, "Hai tab cùng sửa một phiếu nháp", "P1",
     "Mở 2 tab cùng màn Sửa phiếu nháp X.",
     "1. Tab 1 đổi Lý do chi rồi Lưu nháp\n2. Tab 2 (chưa tải lại) đổi Ghi chú rồi Lưu nháp\n"
     "3. Mở lại phiếu",
     "—",
     "- Cả 2 lần lưu đều chạy, lần lưu SAU ghi đè lần trước\n"
     "- Lịch sử thay đổi ghi nhận đủ 2 lần sửa"),

    (4, "Duyệt phiếu ở tab này rồi sửa ở tab kia", "P0",
     "Mở 2 tab cùng màn Sửa phiếu nháp X.",
     "1. Tab 1 bấm 'Lưu và duyệt' thành công\n2. Tab 2 bấm 'Lưu nháp'",
     "—",
     "- Tab 2 bị từ chối, hệ thống báo chỉ sửa được phiếu ở trạng thái Đang tạo do chính mình "
     "lập\n- Phiếu giữ nguyên trạng thái 'Đã hạch toán' và giữ nguyên bút toán đã ghi"),

    (5, "Duyệt hai lần liên tiếp", "P0",
     "Đang ở màn Sửa một phiếu nháp.",
     "1. Bấm 'Lưu và duyệt' rồi 'Xác nhận'\n2. Bấm nút quay lại của trình duyệt về màn Sửa\n"
     "3. Bấm 'Lưu và duyệt' lần nữa",
     "—",
     "- Lần hai bị từ chối\n- ⚠️ Sổ kế toán KHÔNG có bút toán trùng — kiểm bằng cách đếm số bút "
     "toán của phiếu trước và sau"),

    (6, "Mã phiếu không trùng khi lập đồng thời", "P1",
     "Hai kế toán cùng công ty bấm Lưu gần như cùng lúc.",
     "1. X và Y cùng bấm 'Lưu nháp' trong vòng 1 giây\n2. So sánh mã phiếu của 2 phiếu vừa tạo",
     "—",
     "- Hai mã khác nhau, số cuối tăng liên tiếp\n- Không có thông báo lỗi trùng mã"),

    (7, "Xóa phiếu trong khi người khác đang mở màn chi tiết", "P1",
     "X đang mở màn chi tiết phiếu nháp của chính X ở tab 1; tab 2 cũng của X mở danh sách.",
     "1. Tab 2 xóa phiếu đó\n2. Tab 1 bấm nút 'Sửa'",
     "—",
     "- Hệ thống báo dữ liệu đã thay đổi và đưa về danh sách, không treo trang"),
]

S10 = [
    (1, "Luồng đầy đủ: lập nháp, sửa, duyệt", "P0",
     "Kế toán có quyền 'Kế toán thanh toán'. Có đề nghị chuyển khoản đang Chờ tạo phiếu chi.",
     "1. Tạo mới, chọn phiếu đề nghị, chọn phương thức thanh toán, ngân hàng chuyển, số tài "
     "khoản chuyển khoản\n2. Bấm 'Lưu nháp'\n3. Mở lại phiếu bằng nút Sửa, đổi số tiền duyệt chi "
     "của dòng đầu\n4. Bấm 'Lưu và duyệt' rồi 'Xác nhận'\n5. Mở màn chi tiết và khối Lịch sử",
     "Số tiền duyệt chi dòng 1: nhỏ hơn số đề nghị",
     "- Bước 2 tạo phiếu 'Đang tạo', bước 4 chuyển 'Đã hạch toán'\n"
     "- Sau bước 4 phiếu không sửa / xóa được nữa\n"
     "- Khối Lịch sử ghi đủ: lần tạo, lần sửa số tiền, lần chuyển trạng thái"),

    (2, "Luồng đầy đủ: lập nháp rồi xóa", "P0",
     "Kế toán có quyền 'Kế toán thanh toán'.",
     "1. Tạo mới, chọn đề nghị, Lưu nháp\n2. Kiểm tra tổng bản ghi danh sách\n"
     "3. Xóa phiếu vừa lập\n4. Kiểm tra lại tổng bản ghi và trạng thái phiếu đề nghị",
     "—",
     "- Tổng bản ghi tăng 1 rồi giảm 1 về đúng số ban đầu\n"
     "- Phiếu đề nghị nguồn vẫn Chờ tạo phiếu chi và chọn lại được"),

    (3, "Luồng đầy đủ phiếu Chi thu nhập cho nhân viên", "P0",
     "Phòng ban có ít nhất 2 nhân viên còn số dư thu nhập.",
     "1. Tạo mới, chọn Loại chi = 'Chi thu nhập cho nhân viên'\n"
     "2. Điền Người nhận, Lý do chi, chọn Phòng ban\n3. Bỏ tích 1 nhân viên không cần chi\n"
     "4. Nhập Số tiền chi cho nhân viên còn lại, sang tab vụ việc tách đủ 5 khoản khớp tổng\n"
     "5. Chọn ngân hàng chuyển và số tài khoản chuyển khoản\n6. Lưu và duyệt\n"
     "7. Mở lại màn chi tiết",
     "—",
     "- Phiếu lưu thành công, trạng thái 'Đã hạch toán'\n"
     "- Màn chi tiết chỉ hiện nhân viên đã tích, không hiện nhân viên đã bỏ tích\n"
     "- Sổ kế toán ghi bút toán theo từng khoản và 2 bút toán tổng"),

    (4, "Đối chiếu song song với hệ thống cũ", "P0",
     "Hai hệ thống chạy trên cùng cơ sở dữ liệu ở máy phát triển; cùng một tài khoản đăng nhập.",
     "1. Mở màn Phiếu ủy nhiệm chi ở hệ thống mới, ghi tổng bản ghi\n"
     "2. Mở màn tương ứng ở hệ thống cũ với cùng tài khoản, ghi tổng bản ghi\n"
     "3. So từng dòng của trang 1",
     "—",
     "- Tổng bản ghi bằng nhau (trừ đúng phần phiếu nháp của người khác mà hệ thống mới cố ý ẩn)\n"
     "- Mã phiếu, loại chi, số tiền, trạng thái của từng dòng khớp nhau\n"
     "- ⚠️ Lệch phải truy nguyên trước khi ghi lỗi — đã có lần lệch chỉ vì tài khoản chưa được "
     "cấp quyền ở hệ thống mới"),

    (5, "Đối chiếu bút toán với hệ thống cũ", "P0",
     "Chọn 5 phiếu cũ đã hạch toán từ hệ thống cũ.",
     "1. Với mỗi phiếu, liệt kê bút toán bên Nợ và bên Có trong sổ kế toán\n"
     "2. So số dòng, số tiền, tài khoản đối ứng",
     "—",
     "- Số dòng và số tiền khớp tuyệt đối với hệ thống cũ\n"
     "- Bút toán bên Có bằng số tiền dòng cuối ở CẢ HAI hệ thống"),

    (6, "Xem lại toàn màn sau khi làm hết luồng", "P1",
     "Vừa chạy xong các luồng ở trên.",
     "1. Mở lại màn danh sách, bấm 'Làm mới'\n2. Mở màn chi tiết vài phiếu vừa thao tác\n"
     "3. Mở bảng điều khiển lỗi của trình duyệt",
     "—",
     "- Danh sách, số liệu, trạng thái đều đúng\n"
     "- Không có lỗi đỏ nào trong bảng điều khiển lỗi của trình duyệt"),
]

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", S1),
    ("II", "BỘ LỌC & TÌM KIẾM", S2),
    ("III", "DANH SÁCH, SẮP XẾP & PHÂN TRANG", S3),
    ("IV", "LẬP PHIẾU, SỬA & XEM CHI TIẾT", S4),
    ("V", "LƯU NHÁP & LƯU VÀ DUYỆT", S5),
    ("VI", "XÓA", S6),
    ("VII", "XUẤT EXCEL / IN", S7),
    ("VIII", "RÀNG BUỘC NHẬP LIỆU", S8),
    ("IX", "CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI", S9),
    ("X", "E2E FLOW", S10),
]

build(output_file=OUT, sheet_name="Trang tính1",
      feature_name="Phiếu ủy nhiệm chi - Cập nhật ngày 04/09/2026",
      module_name=MODULE,
      description_block=DESCRIPTION_BLOCK, role_tcs=ROLE_TCS, sections=SECTIONS)
