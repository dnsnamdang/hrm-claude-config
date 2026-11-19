# -*- coding: utf-8 -*-
"""Testcase man "Bao cao chi tiet hieu qua gop theo chuyen xe" (HRM: phan he Van chuyen > nhom Bao cao van chuyen).

User yeu cau 29/10/2026: testcase Excel kieu doi chieu cheo ERP - HRM - tao du lieu (chuyen xe + phieu hach toan chuyen
xe co but toan Cong lai xe / Xang xe / Chi phi khac / Ve cau duong, Cuoc can phan bo) roi mo bao cao o CA 2 he thong de so.
Nguon da doc:
  - HRM FE: hrm-client/pages/transport/trip-gross-reports/{detail,by-vehicle}/index.vue, pages/transport/components/
    {TransportReportPage, TransportReportTable, TransportReportSummary, TransportItemModal, DrillNum, InfoTip}.vue,
    configs/tripGross.js (DETAIL, BY_VEHICLE), format.js, components/subsystem-menu/transport.js,
    components/report/V2BaseReportPrintModal.vue, utils/mixins/reportPrintPreviewMixin.js, V2BaseSmartFilterPanel.vue
  - HRM BE: Modules/Finance Http/Controllers/V1/{TripGrossReportController, TransportReportController},
    Services/DriverCostReport/{TripGrossReportService, TripAccountingQuery, TripGrossReportPrintService,
    TransportReportPrintService, DriverCostReportService}, Services/Concerns/ResolvesReportPeriod, Routes/api.php,
    Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php, Tests/Feature/TripReportsApiTest.php
  - ERP: TanPhatDev ReportController::detailEffectiveByDriver*, AccountDetail::detailEffectiveByDriverSearchData
    (dong 5428-5611), reports/detail_effective_by_driver.blade.php, EffectiveByDriverReport.blade.php,
    DeliveryTripAccountingController + DeliveryTripAccountingService (but toan cong lai xe), delivery_trip_accounting/
    approve/company.blade.php + formJs.blade.php (cong thuc dinh muc), layouts/topmenubar.blade.php
  - Plan: hrm-claude-config/hrm/.plans/gop-db/van-chuyen-bao-cao/plan.md muc "3 bao cao con lai (26/10/2026)"
Chay: python gen_testcase_hieu-qua-gop-chuyen-xe.py
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "..", ".claude", "skills", "testcase-documenter", "assets"))
from tc_engine import build  # noqa: E402

NGAY = "29/10/2026"
TEN = "Báo cáo chi tiết hiệu quả gộp theo chuyến xe"
MODULE = "BC chi tiết hiệu quả gộp theo chuyến xe"


def L(*lines):
    return "\n".join(lines)


def T(n, func, prio, pre, steps, data, exp):
    def j(x):
        return x if isinstance(x, str) else L(*x)
    return (n, func, prio, j(pre), j(steps), j(data), j(exp))


def R(suffix, func, prio, pre, steps, data, exp):
    t = T("0", func, prio, pre, steps, data, exp)
    return (suffix,) + t[1:]


# ------------------------------------------------------------------ đường bấm
HRM_MENU = "HRM: vào phân hệ Vận chuyển > nhóm \"Báo cáo vận chuyển\" > bấm \"Báo cáo chi tiết hiệu quả gộp theo chuyến xe\""
HRM_XE = "HRM: vào phân hệ Vận chuyển > nhóm \"Báo cáo vận chuyển\" > bấm \"Báo cáo hiệu quả gộp xe vận tải\""
HRM_LX = ("HRM: vào phân hệ Vận chuyển > nhóm \"Báo cáo vận chuyển\" > bấm \"Báo cáo chi tiết chi phí vận chuyển theo "
          "lái xe\"")
ERP_MENU = ("ERP: menu Kho > \"Vận chuyển - Bốc xếp\" > nhóm \"Báo cáo vận chuyển\" > bấm \"Báo cáo chi tiết hiệu quả "
            "gộp theo chuyến xe\"")
ERP_CXCH = "ERP: menu Kho > \"Vận chuyển - Bốc xếp\" > bấm \"Chuyến xe chở hàng\""
HRM_CXK = "HRM: vào phân hệ Vận chuyển > nhóm \"Chuyến xe\" > bấm \"Chuyến xe khác\""
ERP_CHO_HT = "ERP: menu Kế toán > nhóm \"Vận chuyển\" > bấm \"Chuyến xe chở hàng chờ hạch toán\""
ERP_CHO_HT_K = "ERP: menu Kế toán > nhóm \"Vận chuyển\" > bấm \"Chuyến xe khác chờ hạch toán\""
KY_D = "Kỳ: Tuỳ chọn, Thời gian: từ ngày D đến ngày D (D = ngày lập dữ liệu mẫu)"

# ------------------------------------------------------------------ số liệu mẫu
# HT-TEST01 (chuyến xe chở hàng CX-TEST01, xe 29C-TEST1, LX-A): KM 200/230/30/15%; Cước 5,000,000;
#   Công lái xe 800,000 + Xăng 1,200,000 + Chi phí khác 150,000 + Vé cầu đường 100,000 = 2,250,000; CTP 300,000 KHÔNG tính
#   Lãi gộp 2,750,000
# HT-TEST02 (chuyến xe khác CXK-TEST02, xe 29C-TEST1, LX-A, tuyến không có sẵn 50 km 1 chiều): KM 50/60/10/20%;
#   Cước 900,000; 200,000 + 300,000 + 37,500 + 450,000 = 987,500; Lãi gộp -87,500 (chuyến lỗ)
# HT-TEST03 (chuyến xe chở hàng CX-TEST03, xe 29C-TEST2, LX-B công ty B): KM 100/90/-10/-10%; Cước 3,000,000;
#   360,000 + 540,000 + 67,500 + 50,000 = 1,017,500; Lãi gộp 1,982,500
# 29C-TEST1: 2 chuyến; KM 250/290/40/16%; Cước 5,900,000; CP 3,237,500; LG 2,662,500
# 29C-TEST2: 1 chuyến; KM 100/90/-10/-10%; Cước 3,000,000; CP 1,017,500; LG 1,982,500
# TỔNG: 3 chuyến, 2 xe; KM 350/380/30/8.57%; Cước 8,900,000; CP 4,255,000; LG 4,645,000
# Chuyến xe chở hàng 2 (LG 4,732,500) · Chuyến xe khác 1 (LG -87,500) · Chuyến lỗ 1 (LG -87,500)

DU_LIEU = L(
    "Dữ liệu mẫu dùng xuyên suốt (lập ngày D, ghi mã thật vào cột Ghi chú nếu hệ thống tự sinh mã khác):",
    "- Công ty A, Công ty B: 2 công ty có sẵn. LX-A: nhân viên lái xe Công ty A. LX-B: nhân viên lái xe Công ty B.",
    "- TK-TCT: có quyền \"Xem báo cáo vận chuyển theo công ty theo tổng công ty\" (không phải Super admin).",
    "- TK-CT-A: nhân viên Công ty A, có quyền \"Xem báo cáo vận chuyển theo công ty\".",
    "- TK-KT-A: kế toán Công ty A, KHÔNG có 2 quyền trên; là người lập và duyệt HT-TEST01, HT-TEST02.",
    "- TK-KT-B: kế toán Công ty B, KHÔNG có 2 quyền trên; là người lập và duyệt HT-TEST03.",
    "- TK-Z: nhân viên Công ty A, không có quyền nào, chưa từng lập phiếu hạch toán chuyến xe.",
    "- Xe 29C-TEST1, 29C-TEST2, 29C-TEST3: dòng xe DX-TEST, tải trọng TT-TEST, giá nhiên liệu của xe 20,000 đồng/lít.",
    "- Tuyến đường TD-TEST: 100 km. Bảng giá hiệu lực của dòng xe DX-TEST / tải trọng TT-TEST: Công lái xe 4,000 "
    "đồng/km, định mức xăng 0.3 lít/km, Chi phí khác 750 đồng/km.",
    "- CX-TEST01 (chuyến xe chở hàng): xe 29C-TEST1, lái xe LX-A, tuyến TD-TEST, Đi 2 chiều, Km lúc đi 10,000, Km lúc "
    "về 10,230, Km duyệt 200, Cước vận chuyển thực tế 5,000,000 (công ty không trả phần nào), Vé cầu đường 100,000, "
    "Công tác phí 300,000. Phiếu hạch toán HT-TEST01 bấm \"Lưu và duyệt\" ngày D. Phiếu hiện: Công lái xe 800,000, Chi "
    "phí xăng xe 1,200,000, Chi phí khác 150,000, Vé cầu đường 100,000, Công tác phí 300,000.",
    "- CXK-TEST02 (chuyến xe khác): xe 29C-TEST1, lái xe LX-A, kiểu \"Tuyến không có sẵn\" (Điểm đầu: Kho TEST, Điểm "
    "cuối: Công trình TEST), Số Km 50, KHÔNG đi 2 chiều, Km lúc đi 20,000, Km lúc về 20,060, Km duyệt 50, Cước thực tế "
    "900,000, Vé cầu đường 450,000. Phiếu HT-TEST02 \"Lưu và duyệt\" ngày D: Công lái xe 200,000, Chi phí xăng xe "
    "300,000, Chi phí khác 37,500, Vé cầu đường 450,000.",
    "- CX-TEST03 (chuyến xe chở hàng): xe 29C-TEST2, lái xe LX-B, tuyến TD-TEST, 1 chiều, Km lúc đi 5,000, Km lúc về "
    "5,090, Km duyệt 90, Cước 3,000,000, Vé cầu đường 50,000. Phiếu HT-TEST03 \"Lưu và duyệt\" ngày D: Công lái xe "
    "360,000, Chi phí xăng xe 540,000, Chi phí khác 67,500, Vé cầu đường 50,000.",
    "- CX-TEST04: xe 29C-TEST3, lái xe LX-A, Cước 2,000,000; phiếu HT-TEST04 chỉ bấm \"Lưu\" (trạng thái Đang tạo, "
    "CHƯA hạch toán).",
    "- Nếu định mức thật trên môi trường test khác, ghi lại số hiện ở các nhãn Công lái xe / Chi phí xăng xe / Chi phí "
    "khác / Vé cầu đường của từng phiếu rồi tính lại số mong đợi theo đúng công thức ở mục 8.",
)

KQ_MAU = L(
    "Kết quả mong đợi của bộ dữ liệu mẫu (kỳ chỉ có dữ liệu mẫu):",
    "- Dòng HT-TEST01: KM định mức 200, KM thực chạy 230, Chênh lệch 30, % 15%, Cước 5,000,000, Chi phí lái xe "
    "2,250,000, Lãi gộp 2,750,000.",
    "- Dòng HT-TEST02: 50 / 60 / 10 / 20%, Cước 900,000, Chi phí 987,500, Lãi gộp -87,500.",
    "- Dòng HT-TEST03: 100 / 90 / -10 / -10%, Cước 3,000,000, Chi phí 1,017,500, Lãi gộp 1,982,500.",
    "- Biển số 29C-TEST1: 2 chuyến, 250 / 290 / 40 / 16%, Cước 5,900,000, Chi phí 3,237,500, Lãi gộp 2,662,500.",
    "- Biển số 29C-TEST2: 1 chuyến, 100 / 90 / -10 / -10%, Cước 3,000,000, Chi phí 1,017,500, Lãi gộp 1,982,500.",
    "- TỔNG: 3 chuyến, 2 xe, 350 / 380 / 30 / 8.57%, Cước 8,900,000, Chi phí 4,255,000, Lãi gộp 4,645,000.",
    "- Khối Chuyến xe: Tất cả chuyến 3; Chuyến xe chở hàng 2 (số nhỏ 4,732,500); Chuyến xe khác 1 (số nhỏ -87,500); "
    "Chuyến lỗ 1 (số nhỏ -87,500).",
)

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng", L(
        "Màn HRM \"Báo cáo chi tiết hiệu quả gộp theo chuyến xe\" (chuyển từ ERP, cùng tên) cho biết từng chuyến xe đem "
        "về bao nhiêu: Cước của chuyến so với chi phí lái xe (Công lái xe, Xăng xe, Chi phí khác, Vé cầu đường) và quãng "
        "đường định mức so với thực chạy.",
        "Bảng dạng cây: mỗi nhóm là 1 xe (biển số), mỗi dòng con là 1 chuyến (1 phiếu hạch toán chuyến xe). Có khối tổng "
        "hợp đầu trang, dòng TỔNG, popup danh sách chuyến khi bấm con số, In báo cáo, Xuất Excel.",
        "Báo cáo CHỈ ĐỌC. ERP và HRM ở môi trường test dùng CHUNG dữ liệu: phiếu hạch toán lập ở ERP thì HRM thấy ngay.",
        DU_LIEU,
    )),
    ("2. Đối tượng được tính / hiển thị", L(
        "Một chuyến được lên báo cáo khi ĐỦ các điều kiện:",
        "- Là phiếu hạch toán chuyến xe chở hàng hoặc phiếu hạch toán chuyến xe khác ở trạng thái \"Đã hạch toán\" (đã bấm "
        "\"Lưu và duyệt\").",
        "- Phiếu có ít nhất 1 bút toán Công lái xe / Xăng xe / Chi phí khác / Vé cầu đường CÓ gắn lái xe, ngày hạch toán "
        "nằm trong kỳ, lái xe đó thuộc phạm vi quyền của người xem (mục 7) và khớp ô Lái xe nếu có chọn.",
        "- Khớp các ô lọc trên chuyến: Phiếu hạch toán (chứa chuỗi gõ), Tải trọng xe, Dòng xe, Tuyến đường, Biển số xe "
        "(biển số ghi trên chuyến).",
        "Khi phiếu đã được chọn: Chi phí lái xe cộng MỌI bút toán 4 loại trên của phiếu, KỂ CẢ bút toán không gắn lái xe "
        "và bút toán của lái xe khác.",
        "Chuyến thiếu xe / tải trọng / dòng xe vẫn hiện (nhóm \"Chưa có biển số\" nếu không xác định được biển số).",
    )),
    ("3. Đối tượng bị ẩn / không tính", L(
        "- Phiếu hạch toán ở trạng thái \"Đang tạo\" (mới bấm \"Lưu\", chưa hạch toán).",
        "- Phiếu có ngày hạch toán ngoài kỳ đã chọn.",
        "- Phiếu chỉ có bút toán KHÔNG gắn lái xe (không có bút toán nào gắn lái xe để chọn phiếu).",
        "- Phiếu không có bút toán nào trong 4 loại Công lái xe / Xăng xe / Chi phí khác / Vé cầu đường.",
        "- Bút toán Công tác phí: KHÔNG cộng vào Chi phí lái xe (y ERP).",
        "- Phiếu mà mọi bút toán gắn lái xe đều nằm ngoài phạm vi quyền (lái xe công ty khác / bút toán người khác lập).",
        "- Chuyến xe chưa lập phiếu hạch toán.",
    )),
    ("4. Bộ lọc thời gian áp dụng cho", L(
        "Ô Kỳ lọc theo NGÀY HẠCH TOÁN của bút toán gắn lái xe trên phiếu hạch toán chuyến xe (gợi ý trên ô: \"Lọc theo "
        "NGÀY HẠCH TOÁN của phiếu hạch toán chuyến xe.\").",
        "Lựa chọn: Tuần này, Tháng này (mặc định), Tháng trước, Năm nay, Tuỳ chọn (hiện thêm ô Thời gian chọn từ ngày - "
        "đến ngày, tính trọn ngày đầu và ngày cuối).",
        "Cột \"Thời gian\" trên bảng lại là NGÀY CẬP NHẬT phiếu hạch toán (như ERP) - thường trùng ngày hạch toán nhưng "
        "có thể khác nếu phiếu được sửa sau khi hạch toán.",
        "ERP lọc theo Từ ngày / Đến ngày trên NGÀY CẬP NHẬT phiếu (khác biệt đã chốt, mục 9).",
    )),
    ("5. Cấu trúc dữ liệu / cây phân cấp", L(
        "Cây 2 cấp: Biển số xe (nhóm, đánh số La mã I, II, III...) > Phiếu hạch toán (dòng chuyến, đánh số 1, 2, 3...).",
        "- Cột tên: \"Biển số xe / Phiếu hạch toán\" kèm ô chọn cấp muốn bung: \"Chỉ xe\" / \"Đến từng chuyến xe\" (mặc "
        "định Đến từng chuyến xe - mở sẵn cả cây).",
        "- Các cột: Số chuyến, Thời gian, Tải trọng tính cước, Dòng xe tính cước, Xe chạy thực tế, Chuyến xe, Tuyến đường, "
        "Lái xe, KM định mức, KM thực chạy, Chênh lệch (KM), % Chênh lệch, Cước, Chi phí lái xe, Lãi gộp.",
        "- Cột chữ (Thời gian ... Lái xe) chỉ có ở dòng chuyến; cột số có ở cả dòng biển số và dòng chuyến; Số chuyến chỉ "
        "ở dòng biển số và dòng TỔNG.",
        "- Biển số nhóm = biển số của xe chạy thực tế; xe không có thì lấy biển số ghi trên chuyến.",
        "- Thứ tự: biển số Z đến A; trong 1 xe, chuyến có ngày hạch toán mới trước.",
        "- Mã phiếu (dòng chuyến) và tên Chuyến xe là đường link mở màn tương ứng của ERP ở tab mới (đúng loại chuyến xe "
        "chở hàng / chuyến xe khác).",
    )),
    ("6. Quy tắc cộng dồn / deduplicate", L(
        "- 1 phiếu hạch toán = 1 dòng chuyến, dù phiếu có nhiều bút toán / nhiều lái xe (cột Lái xe ghi các tên cách nhau "
        "dấu phẩy, dạng \"Họ tên - Mã nhân viên\").",
        "- Dòng biển số = cộng các dòng chuyến của xe đó; dòng TỔNG = cộng TOÀN BỘ dữ liệu đã lọc, không theo trang.",
        "- Mỗi xe chỉ 1 dòng dù có cả chuyến xe chở hàng và chuyến xe khác (ERP BC xe vận tải tách 2 dòng - khác biệt đã "
        "chốt).",
        "- % Chênh lệch ở dòng biển số / TỔNG tính lại trên tổng km, KHÔNG cộng dồn % của từng chuyến.",
    )),
    ("7. Phân quyền cấp", L(
        "Màn không chặn ở menu: ai vào phân hệ Vận chuyển cũng mở được; quyền quyết định PHẠM VI dữ liệu (nhóm quyền "
        "\"Báo cáo vận chuyển\"):",
        "- \"Xem báo cáo vận chuyển theo công ty theo tổng công ty\" (và Super admin): mọi công ty; ô Công ty mở, để trống "
        "= tất cả, chọn 1 công ty = lọc theo công ty của LÁI XE trên bút toán.",
        "- \"Xem báo cáo vận chuyển theo công ty\": chỉ bút toán có lái xe thuộc công ty của mình; ô Công ty khoá ở công "
        "ty mình.",
        "- Không có 2 quyền trên: chỉ bút toán do CHÍNH MÌNH lập; ô Công ty khoá ở công ty mình.",
        "Hai quyền trên dùng chung cho 2 báo cáo chi phí vận chuyển theo lái xe và báo cáo hiệu quả gộp xe vận tải.",
    )),
    ("8. Cách tính các ô thống kê", L(
        "- Cước = Cước cần phân bổ của chuyến (Cước vận chuyển thực tế trừ phần công ty trả).",
        "- Chi phí lái xe = Công lái xe + Xăng xe + Chi phí khác + Vé cầu đường của phiếu (gồm cả bút toán không gắn lái "
        "xe; KHÔNG gồm Công tác phí). Lãi gộp = Cước - Chi phí lái xe.",
        "- Trên phiếu ERP: Công lái xe = đơn giá công lái xe x Km duyệt; Chi phí xăng xe = giá nhiên liệu x định mức xăng x "
        "Km duyệt; Chi phí khác = đơn giá chi phí khác x Km duyệt; Vé cầu đường = số nhập trên chuyến.",
        "- KM định mức = km của tuyến x 2 nếu đi 2 chiều; chuyến xe khác không có tuyến: Số Km nhập trên chuyến (x 2 nếu "
        "2 chiều). KM thực chạy = Km lúc về - Km lúc đi. Chênh lệch = KM thực chạy - KM định mức.",
        "- % Chênh lệch = Chênh lệch / KM định mức x 100 (định mức 0 thì để trống).",
        "- Khối tổng hợp: dòng tiêu đề \"Kỳ <kỳ> (theo ngày hạch toán) · <N> chuyến · <M> xe · Lãi gộp <X>\". Khối "
        "\"Chuyến xe\": Tất cả chuyến; Chuyến xe chở hàng / Chuyến xe khác (chỉ hiện khi có, số nhỏ = lãi gộp của loại "
        "đó); Chuyến lỗ = số chuyến lãi gộp âm (thẻ màu đỏ, chỉ hiện khi có). Khối \"Hiệu quả gộp\": Cước, Chi phí lái xe, "
        "Lãi gộp (đỏ nếu âm). Khối \"Quãng đường\": KM định mức, KM thực chạy, Chênh lệch và % Chênh lệch (2 ô sau chỉ "
        "hiện khi khác 0).",
        "- Ô \"Hiển thị a-b / N xe\" dưới bảng: phân trang theo SỐ XE (nhóm biển số), không theo số chuyến.",
        KQ_MAU,
    )),
    ("9. Ghi chú đọc bảng", L(
        "- Định dạng số chuẩn quốc tế: dấu phẩy ngăn hàng nghìn, dấu chấm thập phân (8.57%). Ở dòng chuyến, tiền bằng 0 để "
        "TRỐNG (ERP in \"-\"); % thiếu định mức để trống.",
        "- Ô gõ \"Phiếu hạch toán\" chỉ lọc khi bấm Enter hoặc \"Tìm kiếm\"; các ô chọn đổi là tải lại ngay.",
        "- Bộ lọc KHÔNG được ghi nhớ: tải lại trang là về mặc định (Kỳ Tháng này). Chỉ \"Cài đặt bộ lọc\" (ẩn / hiện ô) "
        "được lưu theo người dùng. Bảng không có nút cấu hình cột; chọn cột chỉ có ở bước In.",
        "- In / Xuất Excel / popup luôn dùng bộ lọc của báo cáo ĐANG HIỂN THỊ (lần tải thành công gần nhất).",
        "- Bản in tối đa 2,000 dòng; Xuất Excel luôn đủ cột, đủ mọi xe, bung hết chuyến.",
        "KHÁC BIỆT ĐÃ CHỐT ERP - HRM (khi đối chiếu, gặp các điểm này ghi \"khác biệt đã chốt, không ghi lỗi\"):",
        "- K1. HRM dựng cây Biển số > chuyến + dòng biển số + khối tổng hợp + popup; ERP là danh sách phẳng 20 dòng/trang.",
        "- K2. HRM gộp 1 dòng / biển số cho cả chuyến xe chở hàng lẫn chuyến xe khác (ERP BC xe vận tải tách 2 dòng).",
        "- K3. Kỳ HRM theo NGÀY HẠCH TOÁN; ERP theo NGÀY CẬP NHẬT phiếu (dữ liệu thật 26/10/2026 trùng 100%).",
        "- K4. Chi phí lái xe HRM cộng cả bút toán KHÔNG gắn lái xe (ERP BC chi tiết bỏ, ERP BC xe vận tải có cộng).",
        "- K5. Lọc Lái xe / phạm vi công ty: HRM dùng để CHỌN phiếu rồi cộng mọi bút toán của phiếu; ERP chỉ cộng bút toán "
        "của lái xe / công ty đó.",
        "- K6. Cột Lái xe HRM ghi đủ mọi lái xe của phiếu (\"Họ tên - Mã\"); ERP chỉ 1 tên.",
        "- K7. HRM vẫn hiện chuyến thiếu xe / tải trọng / dòng xe; ERP bỏ hẳn các chuyến đó.",
        "- K8. Thứ tự: HRM theo biển số Z-A rồi ngày hạch toán mới trước; ERP theo ngày cập nhật mới trước.",
        "- K9. ERP bắt buộc Từ ngày / Đến ngày rồi bấm Lọc; HRM có sẵn kỳ Tháng này. ERP làm tròn xuống Chênh lệch (KM) "
        "về số nguyên, ô 0 in \"-\"; HRM giữ 2 số lẻ, tiền 0 để trống.",
        "- K10. HRM thêm cột Chuyến xe (link), nút In báo cáo; ERP không có In. ERP Xuất Excel từ 200 dòng trở lên thì gửi "
        "mail; HRM luôn tải file ngay.",
        "- K11. % Chênh lệch dòng TỔNG cả 2 bên đều tính trên tổng km (KHÔNG cộng dồn %) - phải BẰNG nhau; HRM thêm dòng "
        "biển số cũng tính trên tổng km. Tổng KM định mức bằng 0: ERP lỗi, HRM để trống.",
        "- Nhóm TC \"dùng công cụ kiểm thử API gọi thẳng chức năng\" dành cho tester kỹ thuật.",
    )),
]

# ================================================================== TC-ROLE
ROLE_TCS = [
    R("00", "Menu hiện cho mọi tài khoản vào được phân hệ Vận chuyển", "P1",
      ["Đã có dữ liệu mẫu (mục 1)", "TK-Z không có quyền nào của nhóm Báo cáo vận chuyển"],
      ["1. Đăng nhập HRM bằng TK-Z", "2. Mở phân hệ Vận chuyển, mở nhóm \"Báo cáo vận chuyển\"",
       "3. Bấm \"Báo cáo chi tiết hiệu quả gộp theo chuyến xe\""],
      "TK-Z",
      ["- Mục menu hiện, bấm vào mở được màn, không báo không có quyền",
       "- Màn hiện dòng \"Không có chuyến xe nào khớp bộ lọc.\" vì TK-Z chưa lập bút toán nào",
       "- Khối tổng hợp: \"0 chuyến · 0 xe · Lãi gộp 0\"",
       "- Ô Công ty khoá ở công ty của TK-Z"]),
    R("01", "Quyền theo tổng công ty xem mọi công ty", "P0",
      ["Dữ liệu mẫu (mục 1)", "TK-TCT có quyền \"Xem báo cáo vận chuyển theo công ty theo tổng công ty\""],
      ["1. Đăng nhập HRM bằng TK-TCT", "2. " + HRM_MENU, "3. Chọn " + KY_D, "4. Để trống ô Công ty"],
      ["Công ty: (trống)", "Kỳ: Tuỳ chọn D - D"],
      ["- Thấy cả 29C-TEST1 (HT-TEST01, HT-TEST02) và 29C-TEST2 (HT-TEST03)",
       "- Ô Công ty MỞ, chọn được mọi công ty đang hoạt động",
       "- Số liệu khớp kết quả mong đợi ở mục 8 (TỔNG 3 chuyến, Cước 8,900,000, Lãi gộp 4,645,000) nếu kỳ chỉ có dữ "
       "liệu mẫu"]),
    R("02", "Quyền theo tổng công ty chọn Công ty B", "P0",
      ["Như TC-ROLE-01"],
      ["1. Đăng nhập TK-TCT, mở báo cáo, chọn " + KY_D, "2. Ô Công ty chọn Công ty B"],
      "Công ty: Công ty B",
      ["- Chỉ còn 29C-TEST2 / HT-TEST03 (lái xe LX-B thuộc Công ty B)",
       "- Không còn HT-TEST01, HT-TEST02 (lái xe LX-A thuộc Công ty A)",
       "- Ô Lái xe bị xoá giá trị cũ, danh sách Lái xe chỉ còn nhân viên Công ty B",
       "- Lưu ý: lọc theo công ty của LÁI XE, không theo công ty của người lập phiếu"]),
    R("03", "Quyền theo công ty chỉ xem lái xe công ty mình", "P0",
      ["Dữ liệu mẫu", "TK-CT-A thuộc Công ty A, có quyền \"Xem báo cáo vận chuyển theo công ty\""],
      ["1. Đăng nhập HRM bằng TK-CT-A", "2. " + HRM_MENU, "3. Chọn " + KY_D],
      "TK-CT-A",
      ["- Thấy 29C-TEST1 với HT-TEST01, HT-TEST02 (lái xe LX-A Công ty A)",
       "- KHÔNG thấy HT-TEST03 (lái xe LX-B Công ty B) dù TK-CT-A không lập phiếu nào",
       "- Ô Công ty hiện Công ty A, bị khoá (mờ), không có nút xoá",
       "- TỔNG: 2 chuyến, 1 xe, Cước 5,900,000, Chi phí 3,237,500, Lãi gộp 2,662,500"]),
    R("04", "Không quyền chỉ thấy bút toán mình lập", "P0",
      ["Dữ liệu mẫu", "TK-KT-A không có 2 quyền của nhóm, đã lập và duyệt HT-TEST01, HT-TEST02"],
      ["1. Đăng nhập HRM bằng TK-KT-A", "2. " + HRM_MENU, "3. Chọn " + KY_D],
      "TK-KT-A",
      ["- Thấy HT-TEST01, HT-TEST02 (do chính TK-KT-A lập)",
       "- KHÔNG thấy HT-TEST03 (TK-KT-B lập)",
       "- Ô Công ty khoá ở Công ty A",
       "- Đăng nhập TK-KT-B làm lại: chỉ thấy HT-TEST03"]),
    R("05", "Super admin xem như quyền tổng công ty", "P1",
      ["Dữ liệu mẫu", "TK-SA là Super admin HRM, không được gán riêng 2 quyền của nhóm"],
      ["1. Đăng nhập TK-SA", "2. Mở báo cáo, chọn " + KY_D],
      "TK-SA",
      ["- Thấy đủ 3 phiếu mẫu như TK-TCT", "- Ô Công ty mở, chọn được mọi công ty"]),
    R("06", "Tài khoản quyền công ty gọi thẳng chức năng với công ty khác", "P1",
      ["TK-CT-A (quyền theo công ty, Công ty A)", "Dành cho tester kỹ thuật"],
      ["1. Dùng công cụ kiểm thử API gọi thẳng chức năng xem báo cáo, xuất Excel và in của màn này bằng phiên đăng nhập "
       "TK-CT-A, truyền thêm công ty = Công ty B, cùng kỳ D - D"],
      "Công ty: Công ty B",
      ["- Hệ thống BỎ QUA công ty truyền lên, vẫn trả dữ liệu lái xe Công ty A (HT-TEST01, HT-TEST02)",
       "- KHÔNG lộ HT-TEST03 ở cả báo cáo, file Excel và bản in"]),
    R("07", "Không quyền gọi thẳng popup danh sách / Xuất Excel danh sách", "P1",
      ["TK-Z (không quyền, không lập phiếu nào)", "Dành cho tester kỹ thuật"],
      ["1. Dùng công cụ kiểm thử API gọi thẳng chức năng danh sách chuyến của popup, Xuất Excel danh sách và In danh "
       "sách bằng phiên TK-Z, truyền biển số 29C-TEST1"],
      "Biển số xe: 29C-TEST1",
      ["- Danh sách rỗng (0 chuyến), file Excel không có dòng chuyến nào",
       "- Không lộ dữ liệu của người khác dù biết biển số"]),
]

# ================================================================== I. HIỂN THỊ TRANG & TRUY CẬP
S1 = [
    T("001", "Mở màn từ menu Vận chuyển", "P0",
      ["Đăng nhập TK-TCT", "Kỳ Tháng này có dữ liệu"],
      ["1. " + HRM_MENU],
      "-",
      ["- Tiêu đề tab trình duyệt: \"Báo cáo chi tiết hiệu quả gộp theo chuyến xe\"",
       "- Khung lọc tiêu đề \"Bộ lọc báo cáo chi tiết hiệu quả gộp theo chuyến xe\" kèm biểu tượng chữ i \"MỤC ĐÍCH BÁO "
       "CÁO\"",
       "- Bên phải khung lọc có 2 nút \"In báo cáo\" và \"Xuất Excel\"",
       "- Ô Kỳ mặc định \"Tháng này\"; các ô: Kỳ, Công ty, Lái xe, Phiếu hạch toán, Tải trọng xe, Dòng xe, Tuyến đường, Biển "
       "số xe",
       "- Báo cáo tự tải, không cần bấm Tìm kiếm"]),
    T("002", "Khối tổng hợp đầu trang", "P0",
      ["Dữ liệu mẫu, TK-TCT", KY_D],
      ["1. Mở báo cáo, chọn kỳ như tiền điều kiện", "2. Quan sát khối tổng hợp"],
      "-",
      ["- Dòng tiêu đề: \"Kỳ từ D đến D (theo ngày hạch toán) · 3 chuyến · 2 xe · Lãi gộp 4,645,000\"",
       "- Khối \"Chuyến xe\" (tiêu đề phụ \"Lãi gộp 4,645,000\"): Tất cả chuyến 3 chuyến; Chuyến xe chở hàng 2 (4,732,500); "
       "Chuyến xe khác 1 (-87,500); Chuyến lỗ 1 (-87,500) màu đỏ",
       "- Khối \"Hiệu quả gộp\": Cước 8,900,000; Chi phí lái xe 4,255,000; Lãi gộp 4,645,000",
       "- Khối \"Quãng đường\": KM định mức 350 km; KM thực chạy 380 km; Chênh lệch 30 km; % Chênh lệch 8.57%"]),
    T("003", "Nút Thu gọn / Mở rộng khối tổng hợp", "P2",
      ["Đang xem báo cáo có dữ liệu"],
      ["1. Bấm \"Thu gọn\" ở góc phải khối tổng hợp", "2. Bấm \"Mở rộng\""],
      "-",
      ["- Bước 1: 3 khối số ẩn, chỉ còn dòng tiêu đề kỳ; nút đổi thành \"Mở rộng\"",
       "- Bước 2: 3 khối hiện lại, số không đổi, không tải lại báo cáo"]),
    T("004", "Chú thích biểu tượng chữ i ở tiêu đề cột và khối", "P1",
      ["Đang xem báo cáo"],
      ["1. Rê chuột lên biểu tượng chữ i ở các cột KM định mức, KM thực chạy, Chênh lệch (KM), % Chênh lệch, Cước, Chi phí "
       "lái xe, Lãi gộp, Thời gian", "2. Rê lên biểu tượng ở khối Chuyến xe, Hiệu quả gộp, Quãng đường và ở dòng TỔNG"],
      "-",
      ["- Cước: \"Cước cần phân bổ ghi trên chuyến xe\"",
       "- Chi phí lái xe: \"Tổng bút toán Công lái xe + Xăng xe + Chi phí khác + Vé cầu đường của phiếu hạch toán\" và "
       "\"Gồm cả bút toán không gắn lái xe; không gồm Công tác phí\"",
       "- % Chênh lệch: có dòng \"Dòng xe / TỔNG tính trên tổng km, không cộng dồn %\"",
       "- Thời gian: \"Ngày cập nhật phiếu hạch toán chuyến xe (như ERP)\" và \"Kỳ báo cáo lọc theo NGÀY HẠCH TOÁN\"",
       "- Khối Chuyến xe: \"Bấm vào con số để mở danh sách chuyến\"",
       "- Dòng TỔNG: \"Dòng TỔNG tính trên toàn bộ dữ liệu đã lọc, không theo trang\"",
       "- Không chú thích nào bị che, chữ đọc được"]),
    T("005", "Lối vào từ BC hiệu quả gộp xe vận tải - giữ kỳ và biển số", "P0",
      ["Dữ liệu mẫu, TK-TCT"],
      ["1. " + HRM_XE, "2. Chọn " + KY_D, "3. Bấm vào biển số 29C-TEST1 ở dòng xe"],
      "Biển số: 29C-TEST1",
      ["- Mở TAB MỚI màn \"Báo cáo chi tiết hiệu quả gộp theo chuyến xe\"",
       "- Ô Kỳ = Tuỳ chọn, Thời gian = D đến D (giữ đúng kỳ của BC xe vận tải)",
       "- Ô Biển số xe = 29C-TEST1, bảng chỉ còn nhóm 29C-TEST1 với HT-TEST01, HT-TEST02",
       "- Số chuyến / Cước / Chi phí lái xe / Lãi gộp của nhóm = đúng dòng 29C-TEST1 ở BC xe vận tải (2 / 5,900,000 / "
       "3,237,500 / 2,662,500)",
       "- Rê chuột lên biển số ở BC xe vận tải hiện \"Mở báo cáo chi tiết của xe 29C-TEST1 ở tab mới\""]),
    T("006", "Lối vào từ BC xe vận tải với kỳ có sẵn và có chọn công ty", "P1",
      ["Dữ liệu mẫu, TK-TCT"],
      ["1. " + HRM_XE + ", Kỳ: Tháng này, Công ty: Công ty A", "2. Bấm biển số 29C-TEST1"],
      ["Kỳ: Tháng này", "Công ty: Công ty A"],
      ["- Tab mới: Kỳ = Tháng này, Công ty = Công ty A, Biển số = 29C-TEST1",
       "- Ngay lần tải đầu đã áp đủ Công ty A (không hiện dữ liệu tất cả công ty rồi mới lọc lại)"]),
    T("007", "Lối vào có công ty khi người xem không có quyền tổng công ty", "P1",
      ["TK-CT-A (quyền theo công ty)", "Nhận đường link tab chi tiết do TK-TCT gửi (kèm Công ty B, biển số 29C-TEST2)"],
      ["1. Đăng nhập TK-CT-A, dán đường link vào trình duyệt"],
      "-",
      ["- Ô Công ty vẫn khoá ở Công ty A (bỏ qua Công ty B trong link)",
       "- Không thấy HT-TEST03 (lái xe Công ty B); bảng báo \"Không có chuyến xe nào khớp bộ lọc.\"",
       "- Đường link chỉ là cách mở màn, KHÔNG cấp thêm quyền"]),
    T("008", "Giá trị lạ trên thanh địa chỉ khi mở từ BC xe vận tải", "P2",
      ["Đang ở tab chi tiết mở từ BC xe vận tải"],
      ["1. Trên thanh địa chỉ, sửa giá trị biển số thành chữ \"abc\" và giá trị kỳ thành \"xyz\", bấm Enter"],
      "-",
      ["- Màn mở bình thường, không lỗi",
       "- Kỳ về mặc định Tháng này, ô Biển số xe trống, hiện dữ liệu theo phạm vi quyền",
       "- Không lộ thêm dữ liệu ngoài phạm vi quyền"]),
    T("009", "Xe không xác định được biển số", "P2",
      ["Có 1 phiếu hạch toán đã hạch toán mà chuyến không gắn xe và không ghi biển số (lấy dữ liệu thật nếu có, không có "
       "thì ghi Pending)"],
      ["1. Mở báo cáo đúng kỳ của phiếu đó"],
      "-",
      ["- Phiếu nằm trong nhóm \"Chưa có biển số\", vẫn được cộng vào TỔNG",
       "- Ở BC xe vận tải, dòng \"Chưa có biển số\" KHÔNG có link mở báo cáo chi tiết"]),
    T("010", "Kỳ không có dữ liệu", "P1",
      ["TK-TCT"],
      ["1. Chọn Kỳ Tuỳ chọn, Thời gian 01/01/2020 - 02/01/2020"],
      "Thời gian: 01/01/2020 - 02/01/2020",
      ["- Bảng hiện \"Không có chuyến xe nào khớp bộ lọc.\"",
       "- Dòng TỔNG hiện số 0 (màu nhạt), % Chênh lệch để trống; Số chuyến 0 KHÔNG bấm được",
       "- Khối tổng hợp: \"0 chuyến · 0 xe · Lãi gộp 0\"; khối Chuyến xe chỉ còn \"Tất cả chuyến 0\"; khối Quãng đường "
       "không có ô Chênh lệch / % Chênh lệch",
       "- Không còn thanh phân trang"]),
]

# ================================================================== II. BỘ LỌC & TÌM KIẾM
S2 = [
    T("001", "Kỳ Tuần này / Tháng trước / Năm nay", "P1",
      ["Dữ liệu mẫu lập ngày D, TK-TCT"],
      ["1. Lần lượt chọn Kỳ: Tuần này, Tháng trước, Năm nay", "2. Quan sát dòng tiêu đề khối tổng hợp và bảng"],
      ["Tuần này", "Tháng trước", "Năm nay"],
      ["- Tuần này: tiêu đề \"Kỳ tuần này (theo ngày hạch toán)\", có 3 phiếu mẫu",
       "- Tháng trước: tiêu đề \"Kỳ tháng <tháng trước>/<năm> (theo ngày hạch toán)\", KHÔNG có phiếu mẫu",
       "- Năm nay: tiêu đề \"Kỳ năm <năm>\", có 3 phiếu mẫu",
       "- Đổi Kỳ là báo cáo tải lại ngay, không cần bấm Tìm kiếm"]),
    T("002", "Kỳ Tuỳ chọn chưa đủ 2 ngày", "P1",
      ["TK-TCT"],
      ["1. Chọn Kỳ: Tuỳ chọn", "2. Ô Thời gian chỉ chọn ngày bắt đầu", "3. Bấm \"Tìm kiếm\""],
      "Thời gian: chỉ có ngày bắt đầu",
      ["- Bước 1: hiện thêm ô \"Thời gian\" ngay sau ô Kỳ; báo cáo CHƯA tải lại",
       "- Bước 3: thông báo đỏ \"Chọn đủ ngày bắt đầu và ngày kết thúc của kỳ Tuỳ chọn.\"",
       "- Báo cáo đang hiện giữ nguyên, không xoá trắng"]),
    T("003", "Kỳ Tuỳ chọn tính trọn ngày đầu và ngày cuối", "P0",
      ["Dữ liệu mẫu hạch toán ngày D"],
      ["1. Chọn Kỳ Tuỳ chọn D - D", "2. Đổi thành (D-1) - (D-1)", "3. Đổi thành (D+1) - (D+1)"],
      ["D - D", "D-1 - D-1", "D+1 - D+1"],
      ["- Bước 1: có đủ 3 phiếu mẫu (phiếu duyệt lúc cuối ngày D vẫn lên)",
       "- Bước 2 và 3: KHÔNG có phiếu mẫu nào (ngày hạch toán ngoài kỳ không lên)"]),
    T("004", "Đổi Kỳ khỏi Tuỳ chọn xoá ngày đã chọn", "P2",
      ["Đang ở Kỳ Tuỳ chọn D - D"],
      ["1. Đổi Kỳ sang Tháng này", "2. Đổi lại Tuỳ chọn"],
      "-",
      ["- Bước 1: ô Thời gian biến mất, báo cáo theo tháng này",
       "- Bước 2: ô Thời gian hiện lại TRỐNG (không lọc ngầm theo ngày cũ)"]),
    T("005", "Ô Công ty: đổi công ty xoá Lái xe đang chọn", "P1",
      ["TK-TCT, đã chọn Lái xe LX-A"],
      ["1. Ô Công ty chọn Công ty B", "2. Mở ô Lái xe", "3. Bấm nút xoá (x) ở ô Công ty"],
      "Công ty B",
      ["- Bước 1: ô Lái xe bị xoá giá trị; báo cáo tải lại theo Công ty B",
       "- Bước 2: danh sách Lái xe chỉ còn nhân viên Công ty B, dạng \"Mã - Họ tên\"",
       "- Bước 3: về tất cả công ty, danh sách Lái xe đủ mọi công ty",
       "- Rê lên ô Công ty có gợi ý \"Công ty của lái xe trên bút toán hạch toán chuyến xe.\""]),
    T("006", "Lọc Lái xe", "P0",
      ["Dữ liệu mẫu, TK-TCT, " + KY_D],
      ["1. Ô Lái xe chọn LX-A", "2. Đổi sang LX-B"],
      ["Lái xe: LX-A", "Lái xe: LX-B"],
      ["- LX-A: còn 29C-TEST1 với HT-TEST01, HT-TEST02; TỔNG 2 chuyến, Cước 5,900,000, Chi phí 3,237,500",
       "- LX-B: còn 29C-TEST2 với HT-TEST03; TỔNG 1 chuyến, Cước 3,000,000, Chi phí 1,017,500",
       "- Danh sách Lái xe gồm MỌI nhân viên của công ty (không chỉ lái xe)"]),
    T("007", "Lọc Lái xe trên phiếu có nhiều lái xe - chi phí tính cả phiếu", "P1",
      ["Chọn 1 phiếu thật có từ 2 lái xe trở lên ở cột Lái xe (2 tên cách nhau dấu phẩy)",
       "Ghi lại Chi phí lái xe của phiếu khi không lọc"],
      ["1. Mở báo cáo đúng kỳ của phiếu, không lọc Lái xe, ghi Chi phí lái xe của phiếu",
       "2. Ô Lái xe chọn lái xe thứ nhất", "3. Đổi sang lái xe thứ hai"],
      "-",
      ["- Ở cả bước 2 và 3, phiếu vẫn hiện 1 dòng với Chi phí lái xe BẰNG số ở bước 1 (cộng mọi bút toán của phiếu)",
       "- Cột Lái xe vẫn ghi đủ 2 tên",
       "- Lưu ý: ERP chỉ cộng bút toán của lái xe đang lọc - khác biệt đã chốt K5"]),
    T("008", "Lọc Phiếu hạch toán bằng một phần mã, chờ Enter", "P0",
      ["Dữ liệu mẫu, TK-TCT, " + KY_D],
      ["1. Ô Phiếu hạch toán gõ \"TEST0\" (không bấm Enter)", "2. Bấm Enter",
       "3. Đổi thành mã đầy đủ của HT-TEST02 và bấm \"Tìm kiếm\"", "4. Gõ \"  TEST02  \" có dấu cách 2 đầu, bấm Enter"],
      ["TEST0", "<mã HT-TEST02>"],
      ["- Bước 1: báo cáo CHƯA đổi; ô gợi ý \"Mã phiếu hạch toán chuyến xe\"",
       "- Bước 2: còn các phiếu có mã chứa \"TEST0\" (không phân biệt hoa thường)",
       "- Bước 3: còn đúng HT-TEST02 trong nhóm 29C-TEST1",
       "- Bước 4: dấu cách 2 đầu được bỏ, kết quả như bước 3"]),
    T("009", "Lọc Phiếu hạch toán có ký tự đặc biệt", "P2",
      ["TK-TCT"],
      ["1. Ô Phiếu hạch toán gõ \"%\" bấm Enter", "2. Gõ \"_\" bấm Enter"],
      ["%", "_"],
      ["- Không lỗi, chỉ hiện phiếu có mã thật sự chứa ký tự đó (thường là không có)",
       "- KHÔNG hiện toàn bộ phiếu"]),
    T("010", "Lọc Tải trọng xe và Dòng xe", "P1",
      ["Dữ liệu mẫu, TK-TCT, " + KY_D, "Có tải trọng / dòng xe khác TT-TEST / DX-TEST không có chuyến trong kỳ"],
      ["1. Ô Tải trọng xe chọn TT-TEST", "2. Đổi Tải trọng sang một tải trọng khác", "3. Xoá Tải trọng, ô Dòng xe chọn "
       "DX-TEST"],
      ["Tải trọng xe: TT-TEST", "Dòng xe: DX-TEST"],
      ["- Bước 1 và 3: hiện đủ 3 phiếu mẫu (lọc theo tải trọng / dòng xe TÍNH CƯỚC ghi trên chuyến)",
       "- Bước 2: không còn phiếu mẫu",
       "- Danh sách chỉ gồm tải trọng / dòng xe đang hoạt động, sắp theo tên"]),
    T("011", "Lọc Tuyến đường", "P1",
      ["Dữ liệu mẫu, TK-TCT, " + KY_D],
      ["1. Ô Tuyến đường chọn TD-TEST"],
      "Tuyến đường: TD-TEST",
      ["- Còn HT-TEST01 (29C-TEST1) và HT-TEST03 (29C-TEST2)",
       "- HT-TEST02 (chuyến xe khác tuyến không có sẵn) KHÔNG hiện",
       "- TỔNG: 2 chuyến, 2 xe, Cước 8,000,000, Chi phí 3,267,500, Lãi gộp 4,732,500"]),
    T("012", "Lọc Biển số xe", "P0",
      ["Dữ liệu mẫu, TK-TCT, " + KY_D],
      ["1. Ô Biển số xe chọn 29C-TEST2"],
      "Biển số xe: 29C-TEST2",
      ["- Chỉ còn nhóm 29C-TEST2 với HT-TEST03",
       "- TỔNG = dòng nhóm: 1 chuyến, 100 / 90 / -10 / -10%, Cước 3,000,000, Chi phí 1,017,500, Lãi gộp 1,982,500",
       "- Khối tổng hợp \"1 chuyến · 1 xe\"; khối Chuyến xe không có ô Chuyến xe khác và ô Chuyến lỗ"]),
    T("013", "Kết hợp nhiều ô lọc", "P1",
      ["Dữ liệu mẫu, TK-TCT, " + KY_D],
      ["1. Lái xe LX-A, Biển số 29C-TEST1, Phiếu hạch toán gõ mã HT-TEST01, bấm Enter",
       "2. Đổi Biển số sang 29C-TEST2"],
      "-",
      ["- Bước 1: còn đúng HT-TEST01: KM 200 / 230 / 30 / 15%, Cước 5,000,000, Chi phí 2,250,000, Lãi gộp 2,750,000",
       "- Bước 2: \"Không có chuyến xe nào khớp bộ lọc.\" (các điều kiện là VÀ)"]),
    T("014", "Nút Xóa lọc", "P0",
      ["TK-CT-A đang lọc: Kỳ Tuỳ chọn D - D, Lái xe LX-A, Biển số 29C-TEST1, Phiếu hạch toán \"TEST\""],
      ["1. Bấm \"Xóa lọc\"", "2. Làm lại bằng TK-TCT đã chọn Công ty B"],
      "-",
      ["- Bước 1: mọi ô về mặc định (Kỳ Tháng này, các ô khác trống); ô Công ty VẪN khoá ở Công ty A; báo cáo tải lại",
       "- Bước 2: ô Công ty về trống (tất cả công ty)"]),
    T("015", "Cài đặt bộ lọc: ẩn ô đang có giá trị", "P2",
      ["TK-TCT đang lọc Biển số 29C-TEST1"],
      ["1. Bấm \"Cài đặt bộ lọc\"", "2. Bỏ hiện ô Biển số xe, lưu", "3. Tải lại trang (F5)", "4. Bật lại ô Biển số xe"],
      "-",
      ["- Bước 2: ô Biển số xe biến mất và giá trị 29C-TEST1 bị bỏ (không lọc ngầm bằng ô đã ẩn)",
       "- Bước 3: ô vẫn ẩn (cài đặt ẩn / hiện được lưu theo người dùng)",
       "- Bước 4: ô hiện lại, trống"]),
    T("016", "Bộ lọc không được ghi nhớ khi tải lại trang", "P1",
      ["TK-TCT"],
      ["1. Chọn Kỳ Tuỳ chọn D - D, Lái xe LX-A", "2. Tải lại trang (F5)", "3. Thoát ra màn khác rồi vào lại qua menu"],
      "-",
      ["- Bước 2 và 3: bộ lọc về mặc định (Kỳ Tháng này, Lái xe trống)",
       "- Ghi nhận đúng thiết kế hiện tại: màn không ghi nhớ bộ lọc"]),
    T("017", "Đổi nhiều ô lọc liên tiếp thật nhanh", "P2",
      ["Dữ liệu mẫu, TK-TCT"],
      ["1. Trong vòng 2 giây chọn Biển số 29C-TEST1 rồi ngay lập tức đổi sang 29C-TEST2", "2. Chờ ít nhất 3 giây"],
      "-",
      ["- Bảng hiện đúng dữ liệu của lựa chọn CUỐI (29C-TEST2), không bị kết quả 29C-TEST1 về sau đè lên",
       "- Trong lúc tải, báo cáo cũ mờ đi, không nháy trắng màn"]),
]

# ================================================================== III. DANH SÁCH, CÂY & PHÂN TRANG
S3 = [
    T("001", "Cây mở sẵn đến từng chuyến khi vào màn", "P0",
      ["Dữ liệu mẫu, TK-TCT, " + KY_D],
      ["1. Mở báo cáo, quan sát tiêu đề cột tên và bảng"],
      "-",
      ["- Tiêu đề cột: \"Biển số xe / Phiếu hạch toán\" kèm ô chọn cấp đang là \"Đến từng chuyến xe\", cùng 1 hàng",
       "- Nhóm I. 29C-TEST2 > 1. HT-TEST03; nhóm II. 29C-TEST1 > 1. HT-TEST02 hoặc HT-TEST01 theo ngày hạch toán mới trước",
       "- Dòng TỔNG nằm đầu bảng, ngay dưới tiêu đề"]),
    T("002", "Ô chọn cấp Chỉ xe / Đến từng chuyến xe", "P1",
      ["Như TC_03.001"],
      ["1. Ô chọn cấp chọn \"Chỉ xe\"", "2. Chọn lại \"Đến từng chuyến xe\""],
      "-",
      ["- Bước 1: chỉ còn dòng biển số, mũi tên ở mỗi dòng hướng đóng; số liệu dòng biển số và TỔNG không đổi",
       "- Bước 2: mọi nhóm bung lại đủ chuyến",
       "- Đổi cấp KHÔNG tải lại báo cáo (không mờ màn)"]),
    T("003", "Mũi tên bung / thu từng xe", "P1",
      ["Cấp \"Đến từng chuyến xe\""],
      ["1. Bấm mũi tên ở dòng 29C-TEST1", "2. Bấm lại"],
      "-",
      ["- Bước 1: chỉ nhóm 29C-TEST1 thu lại (rê chuột thấy \"Hiện các chuyến xe\"), nhóm khác giữ nguyên",
       "- Bước 2: nhóm bung lại (rê chuột thấy \"Ẩn các chuyến xe\")"]),
    T("004", "Đổi trang / đổi lọc áp lại đúng cấp đang chọn", "P2",
      ["Có hơn 10 xe trong kỳ (dùng Kỳ Năm nay dữ liệu thật), đang chọn cấp \"Chỉ xe\""],
      ["1. Bấm sang trang 2", "2. Đổi Kỳ sang Tháng này"],
      "-",
      ["- Trang 2 và kết quả sau khi đổi kỳ vẫn ở cấp \"Chỉ xe\" (chỉ dòng biển số)"]),
    T("005", "Nội dung dòng chuyến HT-TEST01", "P0",
      ["Dữ liệu mẫu, TK-TCT, " + KY_D],
      ["1. Quan sát dòng HT-TEST01 trong nhóm 29C-TEST1"],
      "-",
      ["- Thời gian: ngày D (dd/mm/yyyy); Số chuyến: trống",
       "- Tải trọng tính cước: TT-TEST; Dòng xe tính cước: DX-TEST; Xe chạy thực tế: \"29C-TEST1 - TT-TEST - DX-TEST\"",
       "- Chuyến xe: tên CX-TEST01 (link); Tuyến đường: TD-TEST; Lái xe: \"<Họ tên LX-A> - <Mã LX-A>\"",
       "- KM định mức 200; KM thực chạy 230; Chênh lệch (KM) 30; % Chênh lệch 15%",
       "- Cước 5,000,000; Chi phí lái xe 2,250,000; Lãi gộp 2,750,000"]),
    T("006", "Dòng chuyến xe khác không có tuyến", "P1",
      ["Dữ liệu mẫu"],
      ["1. Quan sát dòng HT-TEST02"],
      "-",
      ["- Tuyến đường ghi \"Kho TEST - Công trình TEST\" (điểm đầu - điểm cuối)",
       "- KM định mức 50 (Số Km nhập trên chuyến, 1 chiều); KM thực chạy 60; Chênh lệch 10; % 20%",
       "- Lãi gộp -87,500"]),
    T("007", "Thứ tự biển số và thứ tự chuyến", "P1",
      ["Dữ liệu mẫu, TK-TCT, " + KY_D, "HT-TEST02 duyệt SAU HT-TEST01 trong ngày D"],
      ["1. Quan sát thứ tự các nhóm và các chuyến trong 29C-TEST1"],
      "-",
      ["- Biển số xếp Z đến A: 29C-TEST2 đứng trước 29C-TEST1",
       "- Trong 29C-TEST1: chuyến có ngày hạch toán mới hơn đứng trước; cùng ngày thì mã phiếu lớn hơn đứng trước"]),
    T("008", "Đánh số STT nhóm La mã liên tục qua các trang", "P2",
      ["Kỳ có 25 xe (dùng Kỳ Năm nay dữ liệu thật), 20 xe / trang"],
      ["1. Xem trang 1", "2. Sang trang 2"],
      "-",
      ["- Trang 1: nhóm I đến XX; trang 2 bắt đầu XXI",
       "- Dòng chuyến trong mỗi nhóm đánh lại từ 1"]),
    T("009", "Phân trang theo số xe", "P1",
      ["Kỳ Năm nay có 25 xe (dữ liệu thật)"],
      ["1. Quan sát dưới bảng", "2. Đổi số dòng / trang sang 10, rồi 50", "3. Đang ở trang 3 (10 dòng) đổi Biển số chỉ còn 1 "
       "xe"],
      "-",
      ["- Chữ \"Hiển thị 1-20 / 25 xe\"; lựa chọn số dòng: 10, 20, 50, 100",
       "- Đổi số dòng / trang về trang 1",
       "- Mỗi trang đủ chuyến của các xe trên trang (bung chuyến không đẩy chuyến sang trang khác)",
       "- Bước 3: tự về trang 1, không hiện trang trống"]),
    T("010", "Dòng TỔNG không theo trang", "P0",
      ["Kỳ Năm nay có hơn 20 xe"],
      ["1. Ghi dòng TỔNG ở trang 1", "2. Sang trang 2 so lại", "3. Cộng tay cột Cước của tất cả dòng biển số qua mọi trang"],
      "-",
      ["- Dòng TỔNG giống hệt ở mọi trang",
       "- TỔNG Cước = tổng Cước của mọi dòng biển số qua mọi trang; tương tự Chi phí lái xe, Lãi gộp, 3 cột km"]),
    T("011", "Link mã phiếu và tên chuyến mở ERP ở tab mới", "P0",
      ["Dữ liệu mẫu, đã đăng nhập ERP trên cùng trình duyệt"],
      ["1. Bấm mã HT-TEST01", "2. Bấm mã HT-TEST02", "3. Bấm tên chuyến ở cột Chuyến xe của 2 dòng đó"],
      "-",
      ["- Bước 1: tab mới mở phiếu hạch toán chuyến xe CHỞ HÀNG HT-TEST01 trên ERP; rê chuột thấy \"Mở <mã> ở tab mới\"",
       "- Bước 2: tab mới mở phiếu hạch toán chuyến xe KHÁC HT-TEST02 trên ERP",
       "- Bước 3: tab mới mở đúng màn xem chuyến CX-TEST01 / CXK-TEST02",
       "- Tab báo cáo giữ nguyên bộ lọc và cấp đang mở"]),
    T("012", "Ô 0 và ô thiếu số liệu", "P1",
      ["Có 1 chuyến thật có Cước 0 hoặc KM định mức 0 (tuyến không có km) - lấy dữ liệu thật, không có thì ghi Pending"],
      ["1. Quan sát dòng chuyến đó và dòng biển số của nó"],
      "-",
      ["- Dòng chuyến: Cước 0 để TRỐNG (không in 0, không in \"-\"); % Chênh lệch để trống khi KM định mức 0",
       "- Dòng biển số / TỔNG: số 0 in \"0\" màu nhạt"]),
    T("013", "Định dạng số", "P1",
      ["Dữ liệu mẫu"],
      ["1. Quan sát các cột số của HT-TEST02 và dòng TỔNG"],
      "-",
      ["- Chi phí 987,500 (dấu phẩy ngăn nghìn); Lãi gộp -87,500 (dấu trừ phía trước)",
       "- % TỔNG 8.57% (dấu chấm thập phân, tối đa 2 số lẻ); cột số căn phải"]),
    T("014", "Tiêu đề bảng dính khi cuộn, cuộn ngang", "P2",
      ["Kỳ Năm nay nhiều xe, màn hình 1366px"],
      ["1. Cuộn dọc bảng xuống cuối", "2. Cuộn ngang sang cột Lãi gộp"],
      "-",
      ["- Hàng tiêu đề cột luôn dính trên cùng khi cuộn dọc",
       "- Có thanh cuộn ngang ở cả trên và dưới bảng; tiêu đề cột tên không rớt dòng",
       "- Tên dài ở Xe chạy thực tế / Tuyến đường / Lái xe xuống dòng, không đè cột bên cạnh"]),
]

# ================================================================== IV. KIỂM SỐ THEO LUỒNG PHÁT SINH
S4 = [
    T("001", "Ghi số nền trước khi lập dữ liệu", "P0",
      ["Chưa lập dữ liệu mẫu", "TK-TCT ở HRM và ERP"],
      ["1. " + HRM_MENU + ", Kỳ: Tháng này, chụp khối tổng hợp và dòng TỔNG",
       "2. Lọc Biển số 29C-TEST1, rồi 29C-TEST2, chụp lại", "3. " + ERP_MENU + ", Từ ngày / Đến ngày = đầu tháng - cuối "
       "tháng, bấm Lọc, chụp dòng Tổng cộng"],
      "-",
      ["- Có số nền 2 bên để các TC sau so phần TĂNG",
       "- 29C-TEST1, 29C-TEST2 chưa có chuyến nào trong kỳ"]),
    T("002", "Lập chuyến xe chở hàng và phiếu hạch toán HT-TEST01", "P0",
      ["Đã có số nền", "Có Bảng giá hiệu lực vận chuyển (ERP chặn \"Chưa có bảng giá hiệu lực !\" nếu thiếu)"],
      ["1. " + ERP_CXCH + ": tạo CX-TEST01 (xe 29C-TEST1, lái xe LX-A, tuyến TD-TEST, Đi 2 chiều, chọn phiếu xuất kho cần "
       "chở, Vé cầu đường 100,000, Công tác phí 300,000)",
       "2. Xác nhận xe xuất phát với Km lúc đi 10,000; kết thúc chuyến với Km lúc về 10,230; duyệt chuyến, Cước vận "
       "chuyển thực tế 5,000,000",
       "3. " + ERP_CHO_HT + ": lập phiếu cho CX-TEST01, Km duyệt 200, chia cước 5,000,000 vào các phiếu xuất",
       "4. Kiểm các nhãn ở khối lái xe rồi bấm \"Lưu và duyệt\" (xác nhận nếu hỏi)"],
      ["Km duyệt: 200", "Cước vận chuyển thực tế: 5,000,000", "Vé cầu đường: 100,000", "Công tác phí: 300,000"],
      ["- Khối lái xe hiện: Công lái xe: 800,000; Chi phí xăng xe: 1,200,000; Chi phí khác: 150,000; Vé cầu đường: "
       "100,000; Công tác phí: 300,000",
       "- Nếu tổng cước chia khác 5,000,000, ERP báo \"Tổng cước đã chia không bằng tổng cước vận chuyển thực tế\" và không "
       "lưu",
       "- Lưu xong, phiếu HT-TEST01 trạng thái \"Đã hạch toán\""]),
    T("003", "HT-TEST01 lên báo cáo HRM đúng từng cột", "P0",
      ["Đã làm TC_04.002"],
      ["1. HRM mở báo cáo, " + KY_D + ", Biển số 29C-TEST1"],
      "Biển số xe: 29C-TEST1",
      ["- Nhóm 29C-TEST1 có 1 chuyến HT-TEST01",
       "- KM định mức 200 (100 x 2 chiều); KM thực chạy 230 (10,230 - 10,000); Chênh lệch 30; % Chênh lệch 15%",
       "- Cước 5,000,000",
       "- Chi phí lái xe 2,250,000 = 800,000 + 1,200,000 + 150,000 + 100,000",
       "- Lãi gộp 2,750,000",
       "- Dòng biển số và dòng TỔNG trùng dòng chuyến"]),
    T("004", "Công tác phí KHÔNG được tính vào Chi phí lái xe", "P0",
      ["Đã có HT-TEST01 (Công tác phí 300,000)"],
      ["1. Xem dòng HT-TEST01 trên HRM", "2. Mở phiếu HT-TEST01 trên ERP xem bảng bút toán"],
      "Công tác phí: 300,000",
      ["- Phiếu ERP có bút toán Công tác phí 300,000 gắn LX-A",
       "- Chi phí lái xe trên báo cáo = 2,250,000 (KHÔNG phải 2,550,000)",
       "- Lãi gộp = 2,750,000 (KHÔNG phải 2,450,000)"]),
    T("005", "Phiếu hạch toán Đang tạo không lên báo cáo", "P0",
      ["Đã có số nền", "CX-TEST04 (xe 29C-TEST3, Cước 2,000,000) đã duyệt chuyến"],
      ["1. " + ERP_CHO_HT + ": lập phiếu HT-TEST04 cho CX-TEST04, chỉ bấm \"Lưu\"",
       "2. HRM mở báo cáo " + KY_D + ", Biển số 29C-TEST3"],
      "Biển số xe: 29C-TEST3",
      ["- Phiếu HT-TEST04 ở trạng thái \"Đang tạo\"",
       "- Báo cáo HRM: \"Không có chuyến xe nào khớp bộ lọc.\"",
       "- Bỏ lọc Biển số: TỔNG không tăng 2,000,000 so với trước khi lập HT-TEST04"]),
    T("006", "Chuyến xe khác lỗ hiện ở thẻ Chuyến lỗ", "P0",
      ["Đã có HT-TEST01"],
      ["1. " + HRM_CXK + ": bấm \"Tạo chuyến xe khác\" CXK-TEST02 (kiểu Tuyến không có sẵn, Điểm đầu Kho TEST, Điểm cuối "
       "Công trình TEST, Số Km 50, KHÔNG tick Đi 2 chiều, xe 29C-TEST1, lái xe LX-A, Cước thực tế 900,000, Vé cầu "
       "đường 450,000)",
       "2. Duyệt xe xuất phát (Km lúc đi 20,000), Kết thúc chuyến xe (Km lúc về 20,060), Duyệt",
       "3. " + ERP_CHO_HT_K + ": lập phiếu HT-TEST02, Km duyệt 50, bấm \"Lưu và duyệt\"",
       "4. HRM mở báo cáo " + KY_D + ", Biển số 29C-TEST1"],
      ["Cước thực tế: 900,000", "Km duyệt: 50"],
      ["- Phiếu ERP hiện: Công lái xe 200,000; Chi phí xăng xe 300,000; Chi phí khác 37,500; Vé cầu đường 450,000",
       "- Dòng HT-TEST02: KM 50 / 60 / 10 / 20%, Cước 900,000, Chi phí lái xe 987,500, Lãi gộp -87,500",
       "- Khối Chuyến xe có ô \"Chuyến lỗ\" màu đỏ: 1 chuyến, số nhỏ -87,500",
       "- Khối Chuyến xe có ô \"Chuyến xe khác\" 1 (số nhỏ -87,500) và \"Chuyến xe chở hàng\" 1 (2,750,000)"]),
    T("007", "Dòng biển số cộng 2 loại chuyến, % tính trên tổng km", "P0",
      ["Đã có HT-TEST01, HT-TEST02"],
      ["1. HRM báo cáo " + KY_D + ", Biển số 29C-TEST1, quan sát dòng nhóm"],
      "-",
      ["- 29C-TEST1 chỉ có 1 dòng nhóm (không tách chuyến xe chở hàng / chuyến xe khác)",
       "- Số chuyến 2; KM định mức 250; KM thực chạy 290; Chênh lệch 40",
       "- % Chênh lệch 16% (= 40 / 250 x 100), KHÔNG phải 35% (15% + 20%) và KHÔNG phải 17.5% (trung bình)",
       "- Cước 5,900,000; Chi phí lái xe 3,237,500; Lãi gộp 2,662,500"]),
    T("008", "Chuyến của xe khác, lái xe công ty khác", "P0",
      ["Đã có HT-TEST01, HT-TEST02"],
      ["1. " + ERP_CXCH + ": tạo CX-TEST03 (xe 29C-TEST2, lái xe LX-B, tuyến TD-TEST 1 chiều), Km lúc đi 5,000, Km lúc "
       "về 5,090, Cước 3,000,000, Vé cầu đường 50,000",
       "2. TK-KT-B lập HT-TEST03 Km duyệt 90, \"Lưu và duyệt\"",
       "3. HRM (TK-TCT) mở báo cáo " + KY_D],
      ["Km duyệt: 90", "Cước: 3,000,000"],
      ["- Phiếu ERP: Công lái xe 360,000; Chi phí xăng xe 540,000; Chi phí khác 67,500; Vé cầu đường 50,000",
       "- Dòng HT-TEST03: KM 100 / 90 / -10 / -10%, Cước 3,000,000, Chi phí 1,017,500, Lãi gộp 1,982,500",
       "- Chênh lệch âm hiển thị -10, % -10%"]),
    T("009", "Dòng TỔNG và khối tổng hợp với đủ 3 chuyến mẫu", "P0",
      ["Đã có HT-TEST01, 02, 03; số nền đã ghi ở TC_04.001"],
      ["1. HRM báo cáo " + KY_D + " (không lọc khác)", "2. Nếu ngày D có phiếu thật khác, đổi sang so phần TĂNG với số nền"],
      "-",
      ["- Dòng TỔNG (hoặc phần tăng): Số chuyến 3; KM định mức 350; KM thực chạy 380; Chênh lệch 30; Cước 8,900,000; Chi "
       "phí lái xe 4,255,000; Lãi gộp 4,645,000",
       "- % TỔNG = 8.57% (30 / 350 x 100) khi kỳ chỉ có dữ liệu mẫu; khi có dữ liệu thật thì = Chênh lệch TỔNG / KM định "
       "mức TỔNG x 100",
       "- Khối tổng hợp khớp TC_01.002; dòng TỔNG = cộng 2 dòng biển số"]),
    T("010", "Bút toán không gắn lái xe vẫn cộng vào chi phí", "P0",
      ["Phiếu HT-TEST05 (xe 29C-TEST3 hoặc 1 phiếu thật có sẵn), đã hạch toán ngày D, Cước 2,000,000, có bút toán gắn LX-B "
       "tổng 1,017,500 VÀ 1 bút toán Xăng xe 200,000 KHÔNG gắn nhân viên (nhờ kỹ thuật chỉ ra phiếu thật có bút toán xăng "
       "không gắn lái xe - dữ liệu thật có khoảng 1,605 bút toán như vậy)"],
      ["1. HRM báo cáo đúng kỳ, lọc đúng biển số của phiếu", "2. Mở phiếu trên ERP, cộng tay các bút toán Công lái xe / Xăng "
       "xe / Chi phí khác / Vé cầu đường"],
      "-",
      ["- Chi phí lái xe của dòng = 1,217,500 (= 1,017,500 + 200,000); Lãi gộp 782,500",
       "- Cột Lái xe chỉ ghi LX-B (bút toán không gắn nhân viên không thêm tên)",
       "- ERP BC chi tiết cùng phiếu ra Chi phí 1,017,500 - khác biệt đã chốt K4, không ghi lỗi"]),
    T("011", "Phiếu chỉ có bút toán không gắn lái xe không lên", "P1",
      ["1 phiếu đã hạch toán mà mọi bút toán Công lái xe / Xăng xe / Chi phí khác / Vé cầu đường đều KHÔNG gắn nhân viên "
       "(chuyến không có lái xe công ty) - lấy dữ liệu thật, không có thì ghi Pending"],
      ["1. HRM báo cáo đúng kỳ và biển số của phiếu", "2. Gõ mã phiếu vào ô Phiếu hạch toán, bấm Enter"],
      "-",
      ["- Không có dòng của phiếu đó (phiếu được chọn nhờ bút toán CÓ lái xe)",
       "- ERP BC chi tiết cũng không có phiếu này"]),
    T("012", "Phiếu ngoài kỳ không lên", "P0",
      ["Đã có 3 phiếu mẫu hạch toán ngày D"],
      ["1. Kỳ Tuỳ chọn từ ngày 1 của tháng trước đến ngày D-1", "2. Kỳ Tháng trước"],
      "-",
      ["- Cả 2 bước: không có HT-TEST01, 02, 03",
       "- Dòng TỔNG khác TC_04.009 đúng bằng phần của 3 phiếu mẫu (nếu kỳ có giao nhau)"]),
    T("013", "Kỳ theo ngày hạch toán chứ không theo ngày cập nhật", "P2",
      ["1 phiếu thật có ngày cập nhật khác ngày hạch toán (phiếu được sửa sau khi hạch toán) - nhờ kỹ thuật chỉ ra; không "
       "có thì ghi Pending (dữ liệu 26/10/2026 trùng 100%)"],
      ["1. HRM chọn kỳ chứa ngày hạch toán nhưng không chứa ngày cập nhật", "2. Đổi kỳ chứa ngày cập nhật nhưng không chứa "
       "ngày hạch toán"],
      "-",
      ["- Bước 1: phiếu CÓ trên báo cáo, cột Thời gian ghi ngày cập nhật (nằm ngoài kỳ)",
       "- Bước 2: phiếu KHÔNG có",
       "- ERP ngược lại (lọc theo ngày cập nhật) - khác biệt đã chốt K3"]),
    T("014", "Khối Quãng đường ẩn Chênh lệch khi bằng 0", "P2",
      ["Một kỳ / bộ lọc có tổng KM thực chạy đúng bằng tổng KM định mức (vd lọc 1 chuyến thật có chênh lệch 0)"],
      ["1. Lọc để chỉ còn chuyến đó, quan sát khối Quãng đường"],
      "-",
      ["- Khối Quãng đường chỉ còn KM định mức và KM thực chạy, không có ô Chênh lệch / % Chênh lệch",
       "- Dòng chuyến: Chênh lệch (KM) hiện 0, % Chênh lệch hiện 0%"]),
    T("015", "Hạch toán lại sau khi sửa số trên phiếu", "P1",
      ["HT-TEST03 đã lên báo cáo với Chi phí 1,017,500 (nếu ERP cho sửa phiếu đã hạch toán; không cho thì ghi Pending)"],
      ["1. Trên ERP sửa HT-TEST03: Km duyệt 100, Lưu và duyệt", "2. HRM bấm Tìm kiếm lại"],
      "Km duyệt: 100",
      ["- Chi phí lái xe đổi thành 1,125,000 (= Km duyệt 100 x (4,000 + 6,000 + 750) đồng/km + vé cầu đường 50,000); "
       "Lãi gộp 1,875,000",
       "- KHÔNG bị cộng 2 lần bút toán cũ và mới",
       "- Sau TC này đưa Km duyệt về 90 để các TC khác giữ số mẫu"]),
]

# ================================================================== V. POPUP DANH SÁCH CHUYẾN
S5 = [
    T("001", "Mở popup từ ô Tất cả chuyến", "P0",
      ["Dữ liệu mẫu, TK-TCT, " + KY_D],
      ["1. Bấm số 3 ở ô \"Tất cả chuyến\" của khối Chuyến xe"],
      "-",
      ["- Popup \"Bạn đang xem: Tất cả chuyến xe\", dòng phụ \"3 chuyến · Cước: 8,900,000 · Lãi gộp: 4,645,000 · Kỳ từ D "
       "đến D\"",
       "- Cột: Biển số xe, Thời gian, Phiếu hạch toán, Chuyến xe, Tuyến đường, Lái xe, KM định mức, KM thực chạy, Cước, "
       "Chi phí lái xe, Lãi gộp",
       "- Ô tìm \"Tìm biển số / phiếu / chuyến / tuyến / lái xe…\", ô \"Chọn biển số xe\", ô \"Chọn loại chuyến\"",
       "- Bên phải hiện \"3 / 3 chuyến\""]),
    T("002", "Mở popup từ ô Chuyến xe chở hàng / Chuyến xe khác", "P1",
      ["Như TC_05.001"],
      ["1. Bấm số 2 ở ô \"Chuyến xe chở hàng\"", "2. Đóng, bấm số 1 ở ô \"Chuyến xe khác\""],
      "-",
      ["- Bước 1: tiêu đề \"Chuyến xe chở hàng\", 2 dòng HT-TEST01, HT-TEST03; KHÔNG còn ô \"Chọn loại chuyến\"",
       "- Bước 2: tiêu đề \"Chuyến xe khác\", 1 dòng HT-TEST02"]),
    T("003", "Mở popup từ ô Chuyến lỗ", "P0",
      ["Như TC_05.001"],
      ["1. Bấm số 1 ở ô \"Chuyến lỗ\""],
      "-",
      ["- Tiêu đề \"Chuyến lỗ (lãi gộp âm)\", chỉ 1 dòng HT-TEST02, Lãi gộp -87,500",
       "- Dòng phụ \"1 chuyến · Cước: 900,000 · Lãi gộp: -87,500 · Kỳ ...\""]),
    T("004", "Mở popup từ số chuyến của dòng biển số và dòng TỔNG", "P0",
      ["Như TC_05.001"],
      ["1. Bấm số 2 ở cột Số chuyến dòng 29C-TEST1", "2. Đóng, bấm số 3 ở dòng TỔNG"],
      "-",
      ["- Bước 1: tiêu đề \"29C-TEST1\", 2 dòng; KHÔNG còn ô \"Chọn biển số xe\"; rê chuột lên số thấy \"Xem danh sách: "
       "29C-TEST1\"",
       "- Bước 2: tiêu đề \"Tất cả chuyến xe\", 3 dòng; rê chuột thấy \"Xem danh sách: toàn bộ báo cáo\"",
       "- Số dòng popup = đúng con số đã bấm"]),
    T("005", "Popup giữ đúng bộ lọc màn chính", "P0",
      ["TK-TCT, " + KY_D + ", Lái xe LX-A"],
      ["1. Bấm số ở ô Tất cả chuyến"],
      "Lái xe: LX-A",
      ["- Popup chỉ có HT-TEST01, HT-TEST02 (đúng bộ lọc đang hiển thị), \"2 / 2 chuyến\""]),
    T("006", "Tìm trong popup không phân biệt dấu, hoa thường", "P1",
      ["Popup Tất cả chuyến xe đang mở (3 dòng)"],
      ["1. Gõ \"29c-test2\"", "2. Gõ \"cong trinh\" (không dấu)", "3. Gõ một phần tên LX-A không dấu"],
      ["29c-test2", "cong trinh"],
      ["- Bước 1: còn HT-TEST03, \"1 / 3 chuyến\"",
       "- Bước 2: còn HT-TEST02 (tuyến \"Kho TEST - Công trình TEST\")",
       "- Bước 3: còn HT-TEST01, HT-TEST02",
       "- Xuất hiện nút Xoá lọc (biểu tượng làm mới); bấm vào thì về 3 / 3"]),
    T("007", "Lọc chọn trong popup", "P1",
      ["Popup Tất cả chuyến xe (3 dòng)"],
      ["1. Ô \"Chọn biển số xe\" chọn 29C-TEST1", "2. Ô \"Chọn loại chuyến\" chọn Chuyến xe khác"],
      "-",
      ["- Danh sách lựa chọn chỉ gồm giá trị có trong chính popup (29C-TEST1, 29C-TEST2; Chuyến xe chở hàng, Chuyến xe "
       "khác)",
       "- Bước 1: 2 dòng; bước 2: 1 dòng HT-TEST02",
       "- Dòng phụ đầu popup vẫn tính trên toàn bộ 3 chuyến; số \"x / 3 chuyến\" đổi theo lọc"]),
    T("008", "Sắp xếp trong popup", "P1",
      ["Popup Tất cả chuyến xe (dùng Kỳ Năm nay để có nhiều dòng)"],
      ["1. Bấm tiêu đề Lãi gộp 2 lần", "2. Bấm tiêu đề Thời gian", "3. Bấm tiêu đề Lái xe"],
      "-",
      ["- Lãi gộp: tăng dần rồi giảm dần theo GIÁ TRỊ số (âm đứng đầu khi tăng dần)",
       "- Thời gian: theo đúng thứ tự ngày (không theo chữ dd/mm)",
       "- Lái xe: theo bảng chữ tiếng Việt; ô trống luôn xuống cuối",
       "- Sắp xếp áp trên tập đang lọc"]),
    T("009", "Phân trang popup và mở lại popup", "P2",
      ["Popup có hơn 20 dòng (Kỳ Năm nay)"],
      ["1. Sang trang 2, gõ ô tìm, sắp theo Cước", "2. Đóng popup, mở lại cùng ô số"],
      "-",
      ["- Phân trang tại chỗ, không tải lại",
       "- Mở lại: sạch trạng thái - trang 1, ô tìm trống, không sắp xếp"]),
    T("010", "Link trong popup và nút Đóng", "P1",
      ["Popup Tất cả chuyến xe"],
      ["1. Bấm mã phiếu HT-TEST02 ở cột Phiếu hạch toán", "2. Bấm tên chuyến ở cột Chuyến xe", "3. Bấm \"Đóng\""],
      "-",
      ["- Bước 1, 2: mở tab mới đúng phiếu / chuyến trên ERP, popup vẫn mở",
       "- Bước 3: popup đóng, báo cáo giữ nguyên"]),
    T("011", "Con số 0 không bấm được", "P2",
      ["Kỳ không có dữ liệu"],
      ["1. Bấm vào số 0 ở ô Tất cả chuyến và ở Số chuyến dòng TỔNG"],
      "-",
      ["- Số 0 hiện chữ thường, không gạch chân, bấm không mở popup"]),
]

# ================================================================== VI. XUẤT EXCEL / IN
S6 = [
    T("001", "Xuất Excel đúng bộ lọc, đủ mọi trang và mọi chuyến", "P0",
      ["Kỳ Năm nay có hơn 20 xe; đang xem trang 1, cấp \"Chỉ xe\""],
      ["1. Bấm \"Xuất Excel\"", "2. Mở file tải về"],
      "-",
      ["- Tải ngay file \"bao_cao_chi_tiet_hieu_qua_gop_theo_chuyen_xe.xlsx\"",
       "- Tiêu đề \"BÁO CÁO CHI TIẾT HIỆU QUẢ GỘP THEO CHUYẾN XE\", dòng điều kiện \"Kỳ năm <năm> (theo ngày hạch toán)\"",
       "- Có dòng TỔNG, ĐỦ mọi xe (không chỉ 20 xe trang 1) và BUNG HẾT chuyến dù màn đang ở cấp Chỉ xe",
       "- Đủ 15 cột như bảng; số là số thật (cộng được bằng hàm SUM, không bị báo số dạng chữ)",
       "- TỔNG trong file = dòng TỔNG trên màn"]),
    T("002", "Xuất Excel với dữ liệu mẫu và nhiều ô lọc", "P0",
      ["Dữ liệu mẫu, TK-TCT"],
      ["1. Lọc " + KY_D + ", Lái xe LX-A, Biển số 29C-TEST1", "2. Bấm Xuất Excel"],
      "-",
      ["- File chỉ có nhóm 29C-TEST1 với HT-TEST01, HT-TEST02; số liệu khớp TC_04.007",
       "- Dòng điều kiện ghi kỳ và các ô đang lọc: \"Kỳ từ D đến D (theo ngày hạch toán) · Nhân viên: <tên LX-A> · Biển số "
       "xe: 29C-TEST1\"",
       "- Lưu ý: ô Lái xe ghi nhãn \"Nhân viên\" trong dòng điều kiện (xem ghi chú nghi vấn)"]),
    T("003", "Xuất Excel dùng bộ lọc đang hiển thị", "P1",
      ["Báo cáo đang hiển thị theo Biển số 29C-TEST2"],
      ["1. Ô Phiếu hạch toán gõ \"TEST01\" nhưng KHÔNG bấm Enter", "2. Bấm Xuất Excel"],
      "-",
      ["- File theo đúng báo cáo đang hiện (29C-TEST2, HT-TEST03), không áp chữ \"TEST01\" chưa tìm"]),
    T("004", "Xuất Excel theo phạm vi quyền", "P0",
      ["TK-CT-A, " + KY_D],
      ["1. Bấm Xuất Excel"],
      "-",
      ["- File chỉ có HT-TEST01, HT-TEST02; KHÔNG có HT-TEST03", "- Dòng điều kiện không ghi Công ty"]),
    T("005", "In bảng tổng hợp có chọn cột", "P0",
      ["Dữ liệu mẫu, TK-TCT, " + KY_D],
      ["1. Bấm \"In báo cáo\"", "2. Giữ lựa chọn \"In bảng tổng hợp\", bỏ chọn các cột Tải trọng tính cước, Dòng xe tính "
       "cước, Xe chạy thực tế", "3. Bấm \"In\""],
      "-",
      ["- Cửa sổ \"In báo cáo\" có 2 lựa chọn: \"In bảng tổng hợp\" (\"Đúng bảng đang xem, đủ mọi trang và mọi chuyến xe, "
       "kèm dòng TỔNG.\") và \"Danh sách chuyến xe\"",
       "- Ghi chú \"Cột STT và Biển số xe / Phiếu hạch toán luôn được in.\"; mở ra là đã tick hết cột",
       "- Bản xem trước \"Xem trước báo cáo chi tiết hiệu quả gộp theo chuyến xe\": tiêu đề in hoa, logo công ty, dòng "
       "điều kiện, dòng TỔNG, nhóm 29C-TEST2 / 29C-TEST1 với các chuyến, KHÔNG có 3 cột đã bỏ",
       "- Số trên bản in khớp màn hình"]),
    T("006", "Bỏ hết cột rồi bấm In", "P1",
      ["Cửa sổ In báo cáo đang mở"],
      ["1. Bỏ \"Chọn tất cả\"", "2. Bấm \"In\"", "3. Đóng rồi mở lại cửa sổ"],
      "-",
      ["- Bước 2: báo đỏ \"Vui lòng chọn ít nhất 1 cột để in\", cửa sổ KHÔNG đóng, không in",
       "- Bước 3: về mặc định (In bảng tổng hợp, chọn đủ cột)"]),
    T("007", "In Danh sách chuyến xe", "P1",
      ["Dữ liệu mẫu, " + KY_D],
      ["1. In báo cáo, chọn \"Danh sách chuyến xe\" (\"Mỗi dòng 1 chuyến (phiếu hạch toán), đúng bộ lọc báo cáo hiện "
       "tại.\")", "2. Giữ đủ cột, bấm In"],
      "-",
      ["- Bản xem trước \"Xem trước danh sách chuyến xe\", tiêu đề \"DANH SÁCH CHUYẾN XE — HIỆU QUẢ GỘP\"",
       "- 3 dòng, có cột Loại chuyến (Chuyến xe chở hàng / Chuyến xe khác)",
       "- Dòng đếm \"3 chuyến · Cước: 8,900,000 · Chi phí lái xe: 4,255,000 · Lãi gộp: 4,645,000 VND\""]),
    T("008", "In danh sách và Xuất Excel danh sách từ popup", "P0",
      ["Popup Tất cả chuyến xe đang mở, ô Chọn biển số xe = 29C-TEST1"],
      ["1. Bấm \"In danh sách\", giữ đủ cột, bấm In", "2. Bấm \"Xuất Excel danh sách\""],
      "-",
      ["- Bước 1: cửa sổ chỉ chọn cột (đúng các cột đang hiện trên popup); bản in chỉ 2 dòng của 29C-TEST1, có ghi phạm vi "
       "\"Tất cả chuyến xe\"",
       "- Bước 2: tải file \"danh_sach_chuyen_xe_hieu_qua_gop_<ngày>.xlsx\" chỉ 2 dòng của 29C-TEST1, ĐỦ cột (kể cả cột "
       "không hiện trên popup), có dòng TỔNG cuối",
       "- Số dòng In / Excel = số dòng popup đang hiện"]),
    T("009", "In / Excel từ popup khi ô tìm gõ không dấu", "P1",
      ["Popup Tất cả chuyến xe, ô tìm gõ \"cong trinh\" (popup còn 1 dòng HT-TEST02)"],
      ["1. Bấm \"Xuất Excel danh sách\"", "2. Bấm \"In danh sách\" > In"],
      "Tìm: cong trinh",
      ["- File Excel và bản in PHẢI có đúng 1 dòng HT-TEST02 như popup",
       "- Dòng điều kiện có \"Tìm: \"cong trinh\"\"",
       "- Nếu file / bản in ra 0 dòng thì ghi Failed (xem ghi chú nghi vấn về tìm không dấu)"]),
    T("010", "Vượt mức in 2,000 dòng", "P2",
      ["Kỳ Năm nay (hoặc Tuỳ chọn cả năm trước) có hơn 2,000 dòng xe + chuyến"],
      ["1. In báo cáo > In bảng tổng hợp > In"],
      "-",
      ["- Bản xem trước báo \"Danh sách có <N> dòng, vượt mức in tối đa 2,000 dòng nên chưa in được. ...\"",
       "- Xuất Excel cùng bộ lọc vẫn tải được đủ dòng"]),
    T("011", "Bấm In / Xuất Excel khi báo cáo chưa tải xong lần đầu", "P2",
      ["Mạng chậm (giả lập mạng chậm trong trình duyệt)"],
      ["1. Mở màn và bấm ngay \"Xuất Excel\" khi báo cáo chưa hiện", "2. Bấm \"In báo cáo\""],
      "-",
      ["- Thông báo đỏ \"Báo cáo chưa tải xong, vui lòng thử lại.\", không tải file, không mở cửa sổ in"]),
]

# ================================================================== VII. ĐỐI CHIẾU ERP - HRM
S7 = [
    T("001", "Mở báo cáo ERP cùng kỳ, cùng tài khoản", "P0",
      ["Dữ liệu mẫu", "TK-TCT có cùng quyền ở ERP"],
      ["1. " + ERP_MENU, "2. Bấm Lọc khi chưa nhập ngày", "3. Từ ngày = Đến ngày = D, bấm Lọc"],
      "Từ ngày: D, Đến ngày: D",
      ["- Bước 2: nút Lọc bị mờ, không bấm được (ERP bắt buộc 2 ngày) - HRM có sẵn kỳ Tháng này (K9)",
       "- Bước 3: ERP hiện danh sách phẳng có HT-TEST01, HT-TEST02, HT-TEST03 (và phiếu thật cùng ngày nếu có)"]),
    T("002", "So số chuyến ERP và HRM", "P0",
      ["ERP và HRM cùng kỳ D - D, cùng TK-TCT, không lọc khác"],
      ["1. Đếm tổng số dòng ERP (theo phân trang)", "2. So với Số chuyến dòng TỔNG HRM"],
      "-",
      ["- Số dòng ERP = Số chuyến TỔNG HRM",
       "- Được lệch CHỈ khi có chuyến thiếu xe / tải trọng / dòng xe (HRM có, ERP mất - K7) hoặc phiếu có ngày cập nhật khác "
       "ngày hạch toán (K3); khi lệch phải chỉ ra đúng phiếu"]),
    T("003", "So từng chuyến: Cước, Chi phí lái xe, Lãi gộp", "P0",
      ["Như TC_07.002"],
      ["1. Với HT-TEST01, 02, 03 so từng cột giữa ERP và HRM"],
      "-",
      ["- Cước: 5,000,000 / 900,000 / 3,000,000 cả 2 bên",
       "- Chi phí lái xe: 2,250,000 / 987,500 / 1,017,500 cả 2 bên",
       "- Lãi gộp: 2,750,000 / -87,500 / 1,982,500 cả 2 bên",
       "- Phiếu hạch toán, Tải trọng tính cước, Dòng xe tính cước, Xe chạy thực tế, Tuyến đường trùng nhau"]),
    T("004", "So từng chuyến: KM và % chênh lệch", "P0",
      ["Như TC_07.002"],
      ["1. So 4 cột km của 3 phiếu mẫu"],
      "-",
      ["- KM định mức 200 / 50 / 100; KM thực chạy 230 / 60 / 90 cả 2 bên",
       "- Chênh lệch 30 / 10 / -10; % 15% / 20% / -10% cả 2 bên",
       "- Với chuyến thật có chênh lệch lẻ (vd 12.5 km): ERP làm tròn xuống 12, HRM ghi 12.5 - K9, không ghi lỗi"]),
    T("005", "So dòng tổng ERP và dòng TỔNG HRM", "P0",
      ["Như TC_07.002"],
      ["1. So dòng \"Tổng cộng\" ERP với dòng TỔNG HRM"],
      "-",
      ["- KM định mức, KM thực chạy, Chênh lệch, Cước, Chi phí lái xe, Lãi gộp BẰNG nhau (350 / 380 / 30 / 8,900,000 / "
       "4,255,000 / 4,645,000 nếu kỳ chỉ có dữ liệu mẫu)",
       "- % Chênh lệch tổng BẰNG nhau (8.57%): cả 2 đều tính trên tổng km, không cộng dồn % (K11)"]),
    T("006", "Đối chiếu kỳ dài trên dữ liệu thật", "P1",
      ["Dữ liệu thật, TK-TCT"],
      ["1. HRM Kỳ Năm nay; ERP Từ ngày 01/01/<năm> đến 31/12/<năm>", "2. So số chuyến, Cước, Chi phí lái xe, Lãi gộp ở "
       "dòng tổng"],
      "-",
      ["- Cước, số chuyến khớp (trừ trường hợp K3, K7)",
       "- Chi phí lái xe HRM LỚN HƠN ERP đúng bằng tổng bút toán không gắn lái xe (K4); nhờ kỹ thuật xác nhận con số chênh",
       "- Tham chiếu: đối chiếu năm 2026 ngày 26/10 ra 1,203 chuyến, 13 xe, Cước 662,727,172, Chi phí 431,531,553 (HRM)"]),
    T("007", "Khác biệt hiển thị cây và dòng biển số", "P1",
      ["Như TC_07.002"],
      ["1. So cách trình bày 2 bên"],
      "-",
      ["- HRM: cây Biển số > chuyến, dòng biển số cộng sẵn, khối tổng hợp, popup; ERP: danh sách phẳng 20 dòng / trang, "
       "không có dòng biển số",
       "- Khác biệt đã chốt K1, K2, không ghi lỗi"]),
    T("008", "Khác biệt thứ tự dòng", "P2",
      ["Như TC_07.002"],
      ["1. So thứ tự HT-TEST01, 02, 03 trên 2 bên"],
      "-",
      ["- ERP: theo ngày cập nhật mới trước (không theo biển số)",
       "- HRM: 29C-TEST2 trước 29C-TEST1, trong xe chuyến mới trước",
       "- Khác biệt đã chốt K8, không ghi lỗi"]),
    T("009", "Khác biệt cột Lái xe khi phiếu nhiều lái xe", "P2",
      ["Phiếu thật có từ 2 lái xe trở lên (như TC_02.007)"],
      ["1. So cột Lái xe 2 bên"],
      "-",
      ["- ERP chỉ 1 tên; HRM ghi đủ các tên \"Họ tên - Mã\" cách nhau dấu phẩy",
       "- Khác biệt đã chốt K6, không ghi lỗi"]),
    T("010", "Khác biệt lọc Lái xe và phạm vi công ty với phiếu nhiều lái xe", "P1",
      ["Phiếu thật có 2 lái xe thuộc 2 công ty khác nhau (nếu không có thì ghi Pending)"],
      ["1. Cả 2 bên lọc Lái xe là lái xe thứ nhất", "2. Cả 2 bên đăng nhập tài khoản quyền theo công ty của lái xe thứ nhất"],
      "-",
      ["- ERP: Chi phí lái xe chỉ gồm bút toán của lái xe thứ nhất / công ty đó",
       "- HRM: Chi phí lái xe gồm MỌI bút toán của phiếu",
       "- Khác biệt đã chốt K5, không ghi lỗi; Cước 2 bên vẫn bằng nhau"]),
    T("011", "Khác biệt Chi phí khi có bút toán không gắn lái xe", "P0",
      ["Phiếu HT-TEST05 như TC_04.010"],
      ["1. So dòng HT-TEST05 ERP và HRM"],
      "-",
      ["- ERP: Chi phí lái xe 1,017,500, Lãi gộp 982,500",
       "- HRM: Chi phí lái xe 1,217,500, Lãi gộp 782,500",
       "- Chênh đúng 200,000 = bút toán Xăng xe không gắn lái xe; khác biệt đã chốt K4, không ghi lỗi"]),
    T("012", "Đối chiếu theo từng ô lọc", "P1",
      ["Dữ liệu mẫu, cùng kỳ D - D"],
      ["1. Lần lượt lọc cả 2 bên: Lái xe LX-A; Phiếu hạch toán \"TEST0\"; Tải trọng TT-TEST; Dòng xe DX-TEST; Tuyến đường "
       "TD-TEST; Biển số 29C-TEST1", "2. So số dòng và dòng tổng sau mỗi lần lọc"],
      "-",
      ["- Số dòng và Cước / Chi phí / Lãi gộp tổng bằng nhau ở mọi ô lọc",
       "- Tuyến đường TD-TEST: cả 2 bên còn HT-TEST01, HT-TEST03; Biển số 29C-TEST1: còn HT-TEST01, HT-TEST02"]),
    T("013", "Đối chiếu phạm vi quyền 2 bên", "P0",
      ["Dữ liệu mẫu, TK-CT-A và TK-KT-A có cùng quyền ở 2 hệ thống"],
      ["1. Đăng nhập lần lượt TK-CT-A, TK-KT-A ở cả ERP và HRM, cùng kỳ D - D"],
      "-",
      ["- TK-CT-A: 2 bên đều có HT-TEST01, HT-TEST02, không có HT-TEST03",
       "- TK-KT-A: 2 bên đều chỉ có HT-TEST01, HT-TEST02",
       "- ERP: TK-CT-A, TK-KT-A không thấy ô Công ty; HRM: ô Công ty hiện nhưng khoá"]),
    T("014", "Đối chiếu file Excel 2 bên", "P1",
      ["Dữ liệu mẫu, cùng kỳ D - D"],
      ["1. ERP bấm \"Xuất excel\"", "2. HRM bấm \"Xuất Excel\"", "3. So 3 phiếu mẫu và dòng tổng"],
      "-",
      ["- Số liệu 3 phiếu và dòng tổng bằng nhau",
       "- ERP từ 200 dòng trở lên thì báo gửi file qua mail; HRM luôn tải ngay (K10)",
       "- HRM có thêm dòng biển số và cột Chuyến xe"]),
]

# ================================================================== VIII. ĐỐI CHIẾU NỘI BỘ HRM
S8 = [
    T("001", "TỔNG BC chi tiết = TỔNG BC hiệu quả gộp xe vận tải", "P0",
      ["Dữ liệu mẫu + dữ liệu thật, TK-TCT"],
      ["1. " + HRM_MENU + ", Kỳ Tháng này", "2. " + HRM_XE + ", cùng Kỳ, cùng Công ty", "3. So dòng TỔNG và khối tổng hợp"],
      "Kỳ: Tháng này",
      ["- Số chuyến, KM định mức, KM thực chạy, Chênh lệch, % Chênh lệch, Cước, Chi phí lái xe, Lãi gộp BẰNG nhau",
       "- Số xe ở khối tổng hợp bằng nhau; thẻ Chuyến lỗ bằng nhau"]),
    T("002", "Từng xe của BC xe vận tải = dòng biển số của BC chi tiết", "P0",
      ["Như TC_08.001"],
      ["1. Chọn 3 xe bất kỳ (gồm 29C-TEST1) ở BC xe vận tải", "2. So với dòng biển số cùng xe ở BC chi tiết"],
      "-",
      ["- 29C-TEST1: 2 chuyến, Cước 5,900,000, Chi phí 3,237,500, Lãi gộp 2,662,500, 16% ở cả 2 báo cáo",
       "- 2 xe còn lại: mọi cột số bằng nhau",
       "- BC xe vận tải không có dòng chuyến (bảng 1 cấp, cột tên \"Biển số xe\")"]),
    T("003", "Bấm biển số ở BC xe vận tải - số khớp dòng xe", "P1",
      ["Xe thật có chuyến mà xe chạy thực tế khác biển số ghi trên chuyến (nếu có; không có thì ghi Pending)"],
      ["1. Ở BC xe vận tải bấm biển số của xe đó", "2. So Số chuyến ở tab chi tiết với số ở dòng xe"],
      "-",
      ["- Số chuyến và tiền ở tab chi tiết PHẢI bằng dòng xe đã bấm",
       "- Nếu tab chi tiết ít chuyến hơn thì ghi Failed (xem ghi chú nghi vấn: nhóm theo biển số xe chạy thực tế, ô lọc theo "
       "biển số ghi trên chuyến)"]),
    T("004", "Đối chiếu với BC chi tiết chi phí vận chuyển theo lái xe", "P1",
      ["Dữ liệu mẫu, TK-TCT, " + KY_D],
      ["1. " + HRM_LX + ", cùng kỳ", "2. So dòng HT-TEST01 (lái xe LX-A) với dòng HT-TEST01 ở BC hiệu quả gộp"],
      "-",
      ["- BC theo lái xe: Công lái xe 800,000, Xăng xe 1,200,000, Chi phí khác 150,000, Vé cầu đường 100,000, Công tác "
       "phí 300,000; cột Cộng 2,250,000 (không gồm Công tác phí)",
       "- Cộng của BC theo lái xe = Chi phí lái xe của BC hiệu quả gộp = 2,250,000",
       "- KM định mức / thực chạy của phiếu 1 lái xe bằng nhau ở 2 báo cáo"]),
    T("005", "Tổng chi phí 2 báo cáo lệch đúng bằng bút toán không gắn lái xe", "P1",
      ["Dữ liệu thật Kỳ Tháng này, TK-TCT"],
      ["1. Ghi Tổng Cộng của BC tổng hợp / chi tiết chi phí vận chuyển theo lái xe", "2. Ghi TỔNG Chi phí lái xe của BC "
       "hiệu quả gộp cùng kỳ"],
      "-",
      ["- Chi phí lái xe (hiệu quả gộp) = Cộng (theo lái xe) + tổng bút toán Công lái xe / Xăng xe / Chi phí khác / Vé cầu "
       "đường KHÔNG gắn lái xe của các phiếu đã lên báo cáo",
       "- Lưu ý: BC theo lái xe tách phiếu nhiều lái xe thành nhiều dòng nên KM có thể cộng nhiều lần - chỉ so km với phiếu "
       "1 lái xe"]),
]

# ================================================================== IX. CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI
S9 = [
    T("001", "2 tab với bộ lọc khác nhau", "P2",
      ["TK-TCT"],
      ["1. Tab 1 lọc Biển số 29C-TEST1, tab 2 lọc 29C-TEST2", "2. Ở tab 1 bấm Xuất Excel và In báo cáo"],
      "-",
      ["- File và bản in của tab 1 chỉ có 29C-TEST1, không lẫn bộ lọc tab 2"]),
    T("002", "Dữ liệu đổi trong lúc đang mở báo cáo", "P1",
      ["HRM đang mở báo cáo " + KY_D + " (3 chuyến mẫu)"],
      ["1. Trên ERP lập và \"Lưu và duyệt\" thêm 1 phiếu cho xe 29C-TEST2 ngày D", "2. Ở HRM chưa làm gì, mở popup Tất cả "
       "chuyến", "3. Bấm \"Tìm kiếm\""],
      "-",
      ["- Bước 2: popup lấy dữ liệu mới nhất (có thể đã thấy 4 chuyến) trong khi khối tổng hợp còn 3 - chấp nhận được",
       "- Bước 3: khối tổng hợp, bảng, popup đều thành 4 chuyến, số khớp nhau"]),
    T("003", "Đóng popup trong lúc đang tải", "P2",
      ["Kỳ Năm nay nhiều dữ liệu, mạng chậm"],
      ["1. Bấm ô Tất cả chuyến rồi bấm Đóng ngay", "2. Bấm ô Chuyến lỗ"],
      "-",
      ["- Popup Chuyến lỗ chỉ hiện chuyến lỗ, không bị dữ liệu Tất cả chuyến của lượt trước đè vào"]),
    T("004", "Phạm vi quyền thay đổi giữa chừng", "P2",
      ["TK-CT-A đang mở báo cáo"],
      ["1. Quản trị gỡ quyền \"Xem báo cáo vận chuyển theo công ty\" của TK-CT-A", "2. TK-CT-A bấm Tìm kiếm (đăng nhập lại "
       "nếu hệ thống yêu cầu)"],
      "-",
      ["- Sau khi quyền có hiệu lực: chỉ còn bút toán do TK-CT-A tự lập (thường là không có)",
       "- Không lỗi, không treo trang"]),
]

# ================================================================== X. E2E FLOW
S10 = [
    T("001", "Từ lập chuyến đến đối chiếu 3 báo cáo", "P0",
      ["Chưa có dữ liệu mẫu, có số nền (TC_04.001)"],
      ["1. Lập CX-TEST01 + HT-TEST01, CXK-TEST02 + HT-TEST02, CX-TEST03 + HT-TEST03 như mục 1",
       "2. Mở BC chi tiết hiệu quả gộp " + KY_D + ", kiểm 3 dòng chuyến, 2 dòng biển số, dòng TỔNG, khối tổng hợp",
       "3. Mở BC xe vận tải cùng kỳ, bấm 29C-TEST1", "4. Mở ERP cùng kỳ so 3 phiếu", "5. Xuất Excel, In bảng tổng hợp"],
      "-",
      ["- Mọi số khớp kết quả mong đợi mục 8 ở cả 3 nơi (BC chi tiết, BC xe vận tải, ERP)",
       "- Tab mở từ BC xe vận tải đúng kỳ và biển số",
       "- Excel và bản in cùng số với màn hình"]),
    T("002", "Vòng đời phiếu: Đang tạo, Đã hạch toán", "P1",
      ["Có CX-TEST04 + HT-TEST04 đang ở trạng thái Đang tạo (TC_04.005)"],
      ["1. Kiểm báo cáo chưa có HT-TEST04", "2. Trên ERP mở HT-TEST04, bấm \"Lưu và duyệt\" (chia đủ cước 2,000,000)",
       "3. HRM bấm Tìm kiếm, lọc Biển số 29C-TEST3"],
      "-",
      ["- Bước 1: không có",
       "- Bước 3: có HT-TEST04, Cước 2,000,000, Chi phí lái xe = tổng 4 nhãn Công lái xe / Chi phí xăng xe / Chi phí "
       "khác / Vé cầu đường hiện trên phiếu, Lãi gộp = hiệu",
       "- TỔNG tăng đúng bằng dòng HT-TEST04"]),
]

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", S1),
    ("II", "BỘ LỌC & TÌM KIẾM", S2),
    ("III", "DANH SÁCH, CÂY BIỂN SỐ & PHÂN TRANG", S3),
    ("IV", "KIỂM SỐ THEO LUỒNG PHÁT SINH", S4),
    ("V", "POPUP DANH SÁCH CHUYẾN", S5),
    ("VI", "XUẤT EXCEL / IN", S6),
    ("VII", "ĐỐI CHIẾU ERP - HRM", S7),
    ("VIII", "ĐỐI CHIẾU NỘI BỘ HRM", S8),
    ("IX", "CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI", S9),
    ("X", "E2E FLOW", S10),
]

if __name__ == "__main__":
    build(output_file=os.path.join(HERE, "testcase - BC chi tiet hieu qua gop theo chuyen xe.xlsx"),
          sheet_name="Trang tính1",
          feature_name=TEN + " - Cập nhật ngày " + NGAY,
          module_name=MODULE,
          description_block=DESCRIPTION_BLOCK, role_tcs=ROLE_TCS, sections=SECTIONS)
