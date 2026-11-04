# -*- coding: utf-8 -*-
"""Testcase man "Danh sach can hach toan chi phi van chuyen nhanh" (HRM: phan he Tai chinh > nhom Nhap hang; port ERP
Ke toan > Hang hoa - Dich vu - Van chuyen > Nhap hang). Kieu doi chieu cheo ERP - HRM (2 he thong dung CHUNG du lieu).

Nguon da doc (04/11/2026):
  - Spec: docs/superpowers/specs/gop-db/2026-11-02-hach-toan-cpvc-nhanh-design.md; .plans/gop-db/hach-toan-cpvc-nhanh/{design,plan}.md
  - HRM FE: hrm-client/pages/finance/fast-delivery-accountings/{index.vue, components/constants.js},
    components/subsystem-menu/finance.js (dong 159), components/V2BaseCompanyDepartmentFilter.vue, V2BaseDataTable.vue,
    utils/mixins/filterStateMixin.js, plugins/axios.js,
    pages/finance/bill-adjust-depts/{create.vue, components/BillAdjustDeptForm.vue, AccountingDetailTable.vue, ContractPickerModal.vue}
  - HRM BE: Modules/Finance/Http/Controllers/V1/FastDeliveryAccountingController.php,
    Services/FastDelivery/FastDeliveryAccountingService.php, Services/BillAdjustDeptSourceService.php (fromFastDelivery,
    guardFastDeliveryOnCreate, onBillCreated, onBillDeleted), Services/BillAdjustDeptWriteService.php, Routes/api.php (936-939,
    1317-1360), Entities/BillAdjustDept/BillAdjustDept.php; Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php (1978-1984)
  - ERP: TanPhatDev app/Services/OrderReports/FastDeliveryService.php, Order/OrderReportController.php (741-817),
    IncomeExpenditure/BillAdjustDeptController.php (create 131-160, store 232-250, delete 385-410),
    views orders/reports/fast_delivery.blade.php, orders/buy_contract2/form.blade.php (tab "Phan bo chi phi van chuyen nhanh"),
    layouts/topmenubar.blade.php (842, 1019, 1838), routes/web.php 2159-2162, 6577
  - Mau: .plans/gop-db/chuyen-xe-khac/testcase/gen_testcase_chuyen-xe-khac.py
Khuon: build_chuan (tab "13. DM quoc gia", chot 03/11/2026), loai bao_cao.
Chay: python3 gen_testcase_hach-toan-cpvc-nhanh.py
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "..", ".claude", "skills", "testcase-documenter", "assets"))
from tc_chuan import build_chuan  # noqa: E402

NGAY = "04/11/2026"
TEN = "Danh sách cần hạch toán chi phí vận chuyển nhanh"
MODULE = "Hạch toán CPVC nhanh"


def L(*lines):
    return "\n".join(lines)


def X(s):
    """Đổi tên 2 hệ thống sang ngôn ngữ nghiệp vụ (đồng bộ bộ "Công nợ đầu kỳ theo KH - HĐ"):
    ERP -> "hệ thống cũ", HRM -> "hệ thống mới"; viết hoa chữ đầu khi đứng đầu ý / đầu câu."""
    import re
    s = s.replace("ERP - HRM", "hệ thống cũ - hệ thống mới")
    s = re.sub(r"\bERP\b", "hệ thống cũ", s)
    s = re.sub(r"\bHRM\b", "hệ thống mới", s)
    # đầu dòng, sau "- ", sau "1. ", sau dấu chấm câu / "(" thì viết hoa
    s = re.sub(r"(^|\n|^- |\n- |\n  |\d\. |[.:;] |\()(hệ thống)", lambda m: m.group(1) + "Hệ thống", s)
    return s


def T(n, func, prio, pre, steps, data, exp):
    def j(x):
        return X(x if isinstance(x, str) else L(*x))
    return (n, X(func), prio, j(pre), j(steps), j(data), j(exp))


# ------------------------------------------------------------------ đường bấm
M = 'HRM: vào phân hệ Tài chính > nhóm "Nhập hàng" > bấm "Danh sách cần hạch toán chi phí vận chuyển nhanh"'
E = ('ERP: menu Kế toán > "Hàng hoá - Dịch vụ - Vận chuyển" > nhóm "Nhập hàng" > bấm "Danh sách cần hạch toán chi phí '
     'vận chuyển nhanh", bấm "Lọc"')
E_KD = 'ERP: menu Kinh doanh > "Thông báo" > bấm "Danh sách cần hạch toán chi phí vận chuyển nhanh"'
E_MH = ('ERP: menu Mua hàng > "Báo cáo" > nhóm "Báo cáo mua hàng" > bấm "Danh sách cần hạch toán chi phí vận chuyển '
        'nhanh"')
PKT_H = 'HRM: phân hệ Tài chính > nhóm "Sổ tổng hợp" > bấm "Phiếu kế toán"'
PKT_E = 'ERP: menu Kế toán > "Sổ tổng hợp" > bấm "Phiếu kế toán"'
SO_E = 'ERP: menu Kế toán > "Sổ tổng hợp" > bấm "Sổ chi tiết các tài khoản"'
PNH_H = 'HRM: phân hệ Tài chính > nhóm "Nhập hàng" > bấm "Phiếu nhập hàng"'
PNH_E = 'ERP: menu Kế toán > "Hàng hoá - Dịch vụ - Vận chuyển" > nhóm "Nhập hàng" > bấm "Phiếu nhập hàng"'
HDM_E = 'ERP: menu Mua hàng > "Nhập khẩu" > nhóm "Mua hàng nhập khẩu" > bấm "Hợp đồng mua hàng"'
TAB_CPVC = 'tab "Phân bố chi phí vận chuyển nhanh"'
TAO = 'bấm nút "Tạo phiếu kế toán" trên thanh công cụ của bảng'
LOC = 'mở bảng lọc (nút Bộ lọc cạnh ô tìm nhanh)'

MSG_CHON = "Vui lòng chọn ít nhất một mục để tạo phiếu kế toán"
MSG_DOI = "Trạng thái đã bị thay đổi. Vui lòng load lại trang"
MSG_KQ_HT = "Bạn không có quyền thực hiện thao tác này"
MSG_KQ_KTTT = "Bạn không có quyền thực hiện chức năng này"
MSG_LON = "Dữ liệu quá lớn, vui lòng lọc theo điều kiện cụ thể hơn!"

# ------------------------------------------------------------------ số liệu mẫu
# Thứ tự lập dòng giao nhanh: G1, G2, G3, G4, G5, G6, P1 (HRM xếp theo thứ tự này).
# Phạm vi: TCT 7 (G1-G6, P1) | CT-A 6 (trừ G4) | PB-A1 4 (G1, G3, G5, P1) | BP-A1a 3 (G1, G3, P1) | NV-A1 3 | NV-A2 2 (G2, G6)
# Chưa hạch toán Công ty A: G1, G2, G5, G6, P1 = 5. Đã hạch toán: G3.
# Ngày lập phiếu nhập: 01/11 G5 | 02/11 G2, G3 | 03/11 G1 (15:00), G4, G6, P1 (dùng PNH-T1).
# Số dòng hàng (ERP đếm theo dòng hàng): G1 2, G2 1, G3 1, G4 1, G5 3, G6 1, P1 1 = 10.
# Quy đổi: G1 1,250 x 25,350 = 31,687,500 | P1 100 x 25,350 = 2,535,000 | G2 85,000 x 168 = 14,280,000
#          G5 320.5 x 25,350 = 8,124,675 | G4 730 x 27,850 = 20,330,500 | G6 1,800,000 VNĐ tỷ giá 1.

DU_LIEU = L(
    "Dữ liệu mẫu dùng xuyên suốt (hệ thống tự sinh mã thì ghi mã thật vào cột Ghi chú):",
    "- Công ty A: phòng PB-A1 (bộ phận BP-A1a, BP-A1b), phòng PB-A2. Công ty B.",
    "- Nhân viên chịu phí: NV-A1 (Công ty A, PB-A1, BP-A1a), NV-A2 (Công ty A, PB-A2), NV-A3 (Công ty A, PB-A1, BP-A1b), "
    "NV-B1 (Công ty B). NV-A1, NV-A2 có tài khoản đăng nhập, KHÔNG có quyền nào của màn. NV-KHO: thủ kho lập phiếu nhập.",
    "- Danh mục Tiền tệ (đang dùng): VNĐ; USD tỷ giá 25,350; JPY tỷ giá 168; EURO tỷ giá 27,850.",
    "- Tài khoản (đều KHÔNG phải Super Admin; mỗi tài khoản đăng nhập được cả ERP và HRM):",
    "  TK-TCT: Công ty A, quyền Hạch toán chi phí vận chuyển nhanh + Hạch toán chi phí vận chuyển nhanh - Xem theo tổng "
    "công ty + Kế toán thanh toán.",
    "  TK-KT, TK-KT2: Công ty A, phòng PB-A2, quyền Hạch toán chi phí vận chuyển nhanh + Hạch toán chi phí vận chuyển "
    "nhanh - Xem theo công ty + Kế toán thanh toán.",
    "  TK-CT: Công ty A, chỉ Hạch toán chi phí vận chuyển nhanh - Xem theo công ty.",
    "  TK-PB: Công ty A, phòng PB-A1, chỉ Hạch toán chi phí vận chuyển nhanh - Xem theo phòng ban.",
    "  TK-BP: Công ty A, PB-A1, bộ phận BP-A1a, chỉ Hạch toán chi phí vận chuyển nhanh - Xem theo bộ phận.",
    "  TK-KTTT0: Công ty A, Hạch toán chi phí vận chuyển nhanh + Xem theo công ty, KHÔNG có Kế toán thanh toán.",
    "  TK-Z: không có quyền nào, không chịu phí dòng nào.",
    "- Dòng giao nhanh: lập ở ERP trên " + HDM_E[5:] + ", " + TAB_CPVC + " (Người chịu phí, Khách hàng, Chi phí theo "
    "khách hàng, Hàng hóa); HĐ mua ở trạng thái Đã duyệt. Phiếu nhập hàng loại \"Nhập hàng mua nước ngoài(mới)\" lập từ "
    "Yêu cầu nhập hàng của HĐ mua, trạng thái Đã hoàn thành, có dòng hàng của đúng khách hàng (lập ở ERP hoặc HRM đều được).",
    "  G1: HĐ mua HDM-T1 (USD), NV-A1, KH-T01, 1,250 USD, hàng HH-01 + HH-02; phiếu nhập PNH-T1 lập 03/11/2026 15:00 "
    "(NV-KHO). Chưa hạch toán.",
    "  G2: HDM-T2 (JPY), NV-A2, KH-T02, 85,000 JPY, HH-03; PNH-T2 lập 02/11/2026 09:00. Chưa hạch toán.",
    "  G3: HDM-T3 (VNĐ), NV-A1, KH-T03, 2,500,000 VNĐ, HH-04; PNH-T3 lập 02/11/2026. ĐÃ hạch toán bằng phiếu kế toán "
    "PKT-T3 (Đã duyệt, người duyệt TK-TCT).",
    "  G4: HDM-B1 (EURO), NV-B1 (Công ty B), KH-T01, 730 EURO, HH-05; PNH-B1 lập 03/11/2026. Chưa hạch toán.",
    "  G5: HDM-T5 (USD), NV-A3, KH-T08, 320.5 USD, 3 hàng HH-06, HH-07, HH-08; PNH-T5 lập 01/11/2026. Chưa hạch toán.",
    "  G6: HDM-T6 (VNĐ), NV-A2, KH-T02, 1,800,000 VNĐ, HH-10; PNH-T6 lập 03/11/2026. Chưa hạch toán.",
    "  P1: HDM-T1-PL1 là Phụ lục bổ sung của HDM-T1 (USD), NV-A1, KH-T01, 100 USD, HH-09; KHÔNG có phiếu nhập riêng, "
    "dùng PNH-T1 của HĐ cha. Chưa hạch toán.",
    "  Không lên danh sách: N1 HDM-N1 Chờ duyệt (NV-A1, KH-T04, có phiếu nhập hoàn thành); N2 HDM-N2 Đã duyệt, phiếu "
    "nhập PNH-N2 còn Đang tạo; N3 HDM-N3 Đã duyệt, chưa có phiếu nhập; N4 HDM-N4 Đã duyệt, dòng giao nhanh khách KH-T06 "
    "nhưng phiếu nhập chỉ có hàng của KH-T07; N5 HDM-N5 Đã duyệt, phiếu nhập loại \"Nhập hàng mua trong nước\".",
    "- Kết quả bộ mẫu (thứ tự lập G1, G2, G3, G4, G5, G6, P1): TK-TCT 7 dòng; TK-KT / TK-CT 6 (không có G4); TK-PB 4 "
    "(G1, G3, G5, P1); TK-BP 3 (G1, G3, P1); NV-A1 3 (G1, G3, P1); NV-A2 2 (G2, G6); TK-Z 0.",
    "- Môi trường có sẵn dữ liệu thật thì N = số dòng bộ mẫu + số dòng thật cùng phạm vi; đối chiếu bằng cùng tài khoản "
    "trên ERP.",
)

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng", L(
        "Màn HRM \"Danh sách cần hạch toán chi phí vận chuyển nhanh\" (chuyển từ ERP) giúp kế toán tìm các khoản chi phí "
        "giao nhanh do khách hàng chịu, ghi trên Hợp đồng mua (" + TAB_CPVC + "), hàng ĐÃ VỀ KHO (đã có Phiếu nhập "
        "hàng hoàn thành) mà chưa hạch toán; tick chọn rồi bấm \"Tạo phiếu kế toán\" để lập phiếu Nợ tài khoản 35241 / Có "
        "tài khoản 811. Có Xuất Excel.",
        "ERP và HRM dùng CHUNG dữ liệu: dòng giao nhanh, phiếu nhập, phiếu kế toán lập / duyệt / xoá ở hệ thống này thì hệ "
        "thống kia thấy ngay. Hợp đồng mua chỉ lập được ở ERP (HRM chưa có màn Hợp đồng mua, link mở ERP).",
        "Lối vào HRM: 1 mục menu \"Danh sách cần hạch toán chi phí vận chuyển nhanh\" (phân hệ Tài chính > nhóm Nhập hàng).",
        DU_LIEU,
    )),
    ("2. Đối tượng được tính / hiển thị", L(
        "Một dòng giao nhanh LÊN danh sách khi đủ cả 3 điều kiện:",
        "- Hợp đồng mua (hoặc Phụ lục bổ sung) ở trạng thái Đã duyệt.",
        "- Có Phiếu nhập hàng loại \"Nhập hàng mua nước ngoài(mới)\" trạng thái Đã hoàn thành, lập từ Yêu cầu nhập hàng của "
        "chính HĐ mua đó (Phụ lục: tính theo HĐ cha).",
        "- Phiếu nhập đó có dòng hàng của ĐÚNG khách hàng của dòng giao nhanh.",
        "Cả dòng Chưa hạch toán lẫn Đã hạch toán đều hiện (lọc bằng ô Trạng thái).",
        "Phạm vi theo quyền xem của người đăng nhập, so với nhân viên CHỊU PHÍ của dòng:",
        "- Xem theo tổng công ty: mọi dòng. Xem theo công ty: nhân viên chịu phí cùng công ty người xem.",
        "- Xem theo phòng ban: cùng phòng ban người xem. Xem theo bộ phận: cùng bộ phận người xem.",
        "- Không có quyền xem nào: chỉ dòng mà chính mình là nhân viên chịu phí.",
        "Cột Trạng thái hiện theo PHIẾU KẾ TOÁN gắn dòng: Đang tạo (xám), Đã duyệt (xanh lá), Hủy (đỏ); chưa có phiếu: "
        "Chưa hạch toán (vàng).",
    )),
    ("3. Đối tượng bị ẩn / không tính", L(
        "- HĐ mua Chờ duyệt / Đang tạo / Đã hủy (mẫu N1).",
        "- Chưa có phiếu nhập, hoặc phiếu nhập chưa Đã hoàn thành (N2, N3), hoặc phiếu nhập loại khác (N5).",
        "- Phiếu nhập không có dòng hàng của khách hàng của dòng giao nhanh (N4).",
        "- Dòng ngoài phạm vi quyền xem (mục 2), KỂ CẢ khi người dùng tự chọn công ty / phòng ban khác ở bộ lọc.",
        "- Không ẩn dòng đã hạch toán, không ẩn dòng gắn phiếu kế toán Hủy (Hủy phiếu không gỡ dòng, giống ERP).",
    )),
    ("4. Bộ lọc thời gian áp dụng cho", L(
        "Ô \"Ngày nhập\" (1 ô chọn khoảng ngày) lọc theo NGÀY LẬP Phiếu nhập hàng của dòng, KHÔNG theo ngày HĐ mua, "
        "không theo ngày hạch toán. Tính trọn ngày: từ 00:00:00 ngày đầu tới 23:59:59 ngày cuối.",
        "ERP có 2 ô Từ ngày / Đến ngày và so Đến ngày ở 00:00 nên MẤT phiếu nhập lập trong chính ngày Đến ngày (HRM đã sửa, "
        "user đồng ý 02/11/2026).",
    )),
    ("5. Cấu trúc dữ liệu / cây phân cấp", L(
        "Bảng 12 cột: STT, Nhân viên chịu phí (mã - tên), Phiếu nhập (link), Khách hàng (mã - tên), Hàng hóa (tên + dòng "
        "\"Mã hàng: ...\"), Chi phí KH (số + loại tiền HĐ mua), Hạch toán (ô tick), Phiếu kế toán (link), Hợp đồng mua (link "
        "mở ERP), Người tạo (người lập PHIẾU NHẬP), Người duyệt (người duyệt PHIẾU KẾ TOÁN), Trạng thái.",
        "Mỗi hàng hoá 1 dòng bảng; các ô khác GỘP DỌC theo dòng giao nhanh (G5 có 3 hàng thì gộp 3 dòng).",
        "Thanh công cụ: Tạo phiếu kế toán (chỉ khi có quyền), Xuất Excel, Cấu hình cột. Bảng lọc: ô tìm nhanh + Công ty, "
        "Phòng ban, Bộ phận, Nhân viên, Ngày nhập, Trạng thái, Khách hàng, Phiếu kế toán, Hợp đồng, Người duyệt.",
        "Phiếu kế toán sinh ra: mỗi dòng giao nhanh = 1 nhóm định khoản 2 dòng (Nợ 35241 / Có 811, cùng số tiền, đối tượng "
        "là khách hàng của dòng).",
    )),
    ("6. Quy tắc cộng dồn / deduplicate", L(
        "- 1 dòng danh sách = 1 tổ hợp (HĐ mua, Nhân viên chịu phí, Khách hàng). Phụ lục là HĐ mua riêng nên ra dòng riêng (P1).",
        "- 1 dòng giao nhanh có nhiều phiếu nhập: vẫn 1 dòng, hiện phiếu nhập lập trước; hàng hoá KHÔNG lặp (ERP lặp hàng "
        "hoá theo số phiếu nhập).",
        "- Tick chỉ có tác dụng trong trang đang xem; đổi trang / đổi lọc thì mất tick (giống ERP).",
        "- Dòng đã hạch toán hoặc đã gắn phiếu kế toán: ô Hạch toán tick sẵn và KHOÁ.",
        "- Lưu phiếu kế toán: mọi dòng đã chọn chuyển Đã hạch toán + gắn phiếu ngay ở bước Lưu nháp (chưa cần duyệt).",
        "- Xoá phiếu kế toán (Đang tạo) trên HRM: các dòng trả về Chưa hạch toán. Hủy phiếu (chỉ ERP có): dòng VẪN đã hạch toán.",
    )),
    ("7. Phân quyền cấp", L(
        "Tên quyền nguyên văn (nhóm \"Hạch toán chi phí vận chuyển nhanh\", phân hệ Tài chính):",
        "- Hạch toán chi phí vận chuyển nhanh: hiện nút \"Tạo phiếu kế toán\", được tick dòng; khi lưu phiếu kế toán hệ "
        "thống kiểm lại quyền này.",
        "- Hạch toán chi phí vận chuyển nhanh - Xem theo tổng công ty / - Xem theo công ty / - Xem theo phòng ban / - Xem "
        "theo bộ phận: phạm vi danh sách + Excel (mục 2). Có nhiều quyền thì lấy quyền rộng nhất.",
        "- Kế toán thanh toán (quyền của màn Phiếu kế toán): BẮT BUỘC để lưu được phiếu kế toán.",
        "Menu KHÔNG chặn theo quyền: ai cũng mở được màn, không có quyền xem thì chỉ thấy dòng mình chịu phí (giống ERP).",
        "Quyền tra theo TÊN: gán ở ERP hay ở HRM đều có hiệu lực ở cả 2 hệ thống. Super Admin có mọi quyền.",
    )),
    ("8. Cách tính các ô thống kê", L(
        "- Chi phí KH = \"Chi phí theo khách hàng\" trên " + TAB_CPVC + " của HĐ mua, kèm loại tiền của HĐ mua; số chuẩn "
        "quốc tế, tối đa 2 số lẻ (1,250 USD; 320.5 USD; 85,000 JPY).",
        "- Phiếu kế toán nạp từ màn: ô \"Chi phí vận chuyển nhanh\" = \"<số dòng đã chọn> dòng\"; Loại tiền = loại tiền HĐ "
        "mua của dòng ĐẦU (dòng lập trước) - giống ERP, không chặn khi các dòng khác loại tiền; VNĐ thì Tỷ giá 1; ngoại tệ "
        "thì Tỷ giá lấy từ danh mục Tiền tệ; loại tiền không có trong danh mục đang dùng thì để trống cho người dùng chọn.",
        "- Mỗi dòng giao nhanh: Nợ 35241 = Chi phí KH, Có 811 = Chi phí KH; cột quy đổi VNĐ = nguyên tệ x tỷ giá "
        "(G1: 1,250 x 25,350 = 31,687,500; G2: 85,000 x 168 = 14,280,000; P1: 100 x 25,350 = 2,535,000).",
        "- Ô \"Hiển thị a–b / N\" dưới bảng: a, b là số thứ tự dòng giao nhanh đầu / cuối trang; N = tổng số DÒNG GIAO "
        "NHANH khớp lọc + phạm vi (không phải số dòng hàng hoá).",
        "- Excel: STT theo dòng giao nhanh; Chi phí KH dạng chữ \"<số> <loại tiền>\" giữ 2 số lẻ; Đã hạch toán = \"Đã hạch "
        "toán\" / \"Chưa hạch toán\".",
    )),
    ("9. Ghi chú đọc bảng", L(
        "- Số theo chuẩn quốc tế (phẩy ngăn nghìn, chấm thập phân). Ô rỗng để TRỐNG, không in dấu gạch.",
        "- Màn tự tải khi mở; mặc định 10 dòng giao nhanh / trang; thứ tự theo thứ tự lập dòng giao nhanh (cũ trước); "
        "không có cột sắp xếp.",
        "- Ô tìm nhanh, Phiếu kế toán, Hợp đồng: gõ xong bấm Enter / nút Tìm kiếm mới lọc; các ô chọn lọc ngay.",
        "- Lưu phiếu kế toán bị chặn khi dòng đã hạch toán / không còn đủ điều kiện, báo \"" + MSG_DOI + "\".",
        "KHÁC BIỆT ĐÃ CHỐT ERP - HRM (gặp thì ghi \"khác biệt đã chốt, không ghi lỗi\"):",
        "- K1. HRM chỉ 1 mục menu (Tài chính > Nhập hàng). ERP có 3 lối vào: Kinh doanh > Thông báo; Kế toán > Hàng hoá - "
        "Dịch vụ - Vận chuyển > Nhập hàng; Mua hàng > Báo cáo > Báo cáo mua hàng (cùng 1 danh sách).",
        "- K2. HRM tự tải khi mở và Làm mới thì tải lại đủ phạm vi; ERP phải bấm Lọc, Làm mới xoá trắng bảng.",
        "- K3. Đến ngày lấy hết ngày (HRM sửa lỗi ERP mất phiếu nhập trong ngày cuối).",
        "- K4. Nhiều phiếu nhập: HRM không lặp hàng hoá (ERP lặp).",
        "- K5. Phân trang HRM 10 dòng giao nhanh / trang, N = số dòng giao nhanh, STT liên tục qua trang, 1 dòng không bị "
        "xé sang 2 trang. ERP 30 dòng HÀNG / trang, tổng = số dòng hàng (bộ mẫu TK-TCT: HRM 7, ERP 10), STT đánh lại từ 1 "
        "mỗi trang, dòng nhiều hàng có thể bị xé.",
        "- K6. Thứ tự HRM cố định theo thứ tự lập; ERP không cố định.",
        "- K7. Ô rỗng HRM để trống (ERP in \"-\"); badge Đang tạo HRM màu xám (ERP đỏ).",
        "- K8. HRM thêm ô tìm nhanh (mã HĐ mua, mã phiếu nhập, mã / tên khách); 1 ô Ngày nhập thay 2 ô Từ ngày / Đến ngày.",
        "- K9. Thiếu quyền Hạch toán: HRM ẨN nút Tạo phiếu kế toán; bấm khi chưa tick thì báo \"" + MSG_CHON + "\". ERP để "
        "nút mờ.",
        "- K10. Link Phiếu nhập / Phiếu kế toán mở màn HRM; Hợp đồng mua mở ERP.",
        "- K11. Excel HRM có popup chọn trường, khoảng ngày ghép vào dòng tiêu đề, Chi phí KH giữ 2 số lẻ (ERP làm tròn số "
        "nguyên: 320.5 thành 321); nút Xuất Excel luôn hiện, không có dữ liệu thì báo (ERP mờ nút).",
        "- K12. Lưu phiếu kế toán HRM chặn dòng đã hạch toán / không đủ điều kiện và chặn người thiếu quyền Hạch toán; ERP "
        "không kiểm (2 người lập được 2 phiếu cho 1 dòng, phiếu sau ghi đè liên kết).",
        "- K13. Xoá phiếu kế toán trên HRM trả dòng về Chưa hạch toán; xoá trên ERP KHÔNG trả (dòng kẹt: tick khoá, không "
        "có phiếu, badge Chưa hạch toán, lọc Đã hạch toán vẫn ra) - hiện tượng ERP, HRM chỉ hiển thị lại đúng dữ liệu.",
        "- K14. Không có chức năng sửa Diễn giải / trạng thái / file từng dòng (ERP có sẵn nhưng không có nút nào gọi).",
        "- Lưu ý: tab ERP và HRM dùng chung dữ liệu, chạy TC theo thứ tự trong nhóm; TC làm thay đổi trạng thái dòng thì ghi "
        "lại mã phiếu kế toán vào Ghi chú để TC sau dùng.",
    )),
]

# ================================================================== I. HIỂN THỊ TRANG & TRUY CẬP
S1 = [
    T("001", "Mở màn từ menu: bố cục màn", "P0",
      ["TK-KT (Công ty A, quyền Hạch toán + Xem theo công ty)", "Bộ mẫu mục 1 đã có"],
      ["1. Đăng nhập HRM bằng TK-KT", "2. " + M],
      "-",
      ["- Tiêu đề tab trình duyệt và tiêu đề bảng: \"Danh sách cần hạch toán chi phí vận chuyển nhanh\"",
       "- Ô tìm nhanh có gợi ý \"Tìm theo mã HĐ mua, phiếu nhập, khách hàng\"",
       "- Thanh công cụ theo thứ tự: \"Tạo phiếu kế toán\", \"Xuất Excel\", nút Cấu hình cột (biểu tượng cột)",
       "- Cột theo thứ tự: STT, Nhân viên chịu phí, Phiếu nhập, Khách hàng, Hàng hóa, Chi phí KH, Hạch toán, Phiếu kế "
       "toán, Hợp đồng mua, Người tạo, Người duyệt, Trạng thái"]),
    T("002", "Màn tự tải dữ liệu ngay khi mở", "P1",
      ["TK-KT", "Bộ mẫu mục 1"],
      ["1. " + M, "2. Không bấm nút nào, quan sát bảng"],
      "-",
      ["- Bảng tự hiện 6 dòng giao nhanh: G1, G2, G3, G5, G6, P1; ô \"Hiển thị 1–6 / 6\"",
       "- Khác ERP (K2): ERP mở màn ra bảng \"Chưa có dữ liệu\", phải bấm Lọc - khác biệt đã chốt, không ghi lỗi"]),
    T("003", "HRM 1 lối vào, ERP 3 lối vào cùng một danh sách", "P1",
      ["TK-KT", "Bộ mẫu mục 1"],
      ["1. " + M + ", ghi số dòng", "2. " + E, "3. " + E_KD + ", bấm Lọc", "4. " + E_MH + ", bấm Lọc",
       "5. Trên HRM tìm mục cùng tên ở phân hệ Mua hàng, nhóm Thông báo của Bán hàng"],
      "-",
      ["- Bước 2-4: 3 lối vào ERP ra cùng một danh sách, cùng các dòng G1, G2, G3, G5, G6, P1",
       "- Bước 5: HRM chỉ có 1 mục ở Tài chính > Nhập hàng (K1 - khác biệt đã chốt, không ghi lỗi)",
       "- Danh sách HRM bước 1 có đúng các dòng như ERP"]),
    T("004", "Mở bằng đường link lọc sẵn Chưa hạch toán", "P1",
      ["TK-KT", "Bộ mẫu: G3 Đã hạch toán, còn lại Chưa hạch toán"],
      ["1. " + M, "2. Trên thanh địa chỉ thêm điều kiện trạng thái bằng 0 (dạng đường link \"việc cần làm\" của ERP), Enter"],
      "Điều kiện trạng thái: 0",
      ["- Ô Trạng thái trong bảng lọc tự chọn \"Chưa hạch toán\"",
       "- Bảng có G1, G2, G5, G6, P1; KHÔNG có G3",
       "- Đường link thắng bộ lọc đã chọn trước đó (đã chọn Đã hạch toán thì vẫn ra Chưa hạch toán)"]),
    T("005", "Sửa tay điều kiện trạng thái thành giá trị lạ", "P2",
      ["TK-KT đang mở màn bằng đường link lọc sẵn ở TC_01.004"],
      ["1. Trên thanh địa chỉ đổi giá trị trạng thái thành chữ \"abc\", Enter"],
      "Điều kiện trạng thái: abc",
      ["- Màn không lỗi, ô Trạng thái để trống, hiện đủ 6 dòng trong phạm vi",
       "- Không lộ dòng ngoài phạm vi (không có G4)"]),
    T("006", "Gộp ô theo hàng hoá", "P0",
      ["TK-KT", "G5 có 3 hàng HH-06, HH-07, HH-08"],
      ["1. " + M, "2. Quan sát dòng G5"],
      "-",
      ["- Cột Hàng hóa tách 3 dòng, mỗi dòng 1 tên hàng, bên dưới chữ \"Mã hàng: HH-06\" (HH-07, HH-08)",
       "- 11 cột còn lại (STT, Nhân viên chịu phí, Phiếu nhập, Khách hàng, Chi phí KH, Hạch toán, Phiếu kế toán, Hợp đồng "
       "mua, Người tạo, Người duyệt, Trạng thái) gộp thành 1 ô cao 3 dòng",
       "- Nền xen kẽ theo dòng giao nhanh, không theo dòng hàng"]),
    T("007", "Định dạng cột Chi phí KH theo loại tiền HĐ mua", "P0",
      ["TK-TCT", "Bộ mẫu: G1 1,250 USD, G2 85,000 JPY, G3 2,500,000 VNĐ, G4 730 EURO, G5 320.5 USD"],
      ["1. Đăng nhập TK-TCT", "2. " + M, "3. Đọc cột Chi phí KH từng dòng"],
      "-",
      ["- G1 \"1,250 USD\"; G2 \"85,000 JPY\"; G3 \"2,500,000 VNĐ\"; G4 \"730 EURO\"; G5 \"320.5 USD\"",
       "- Căn phải, phẩy ngăn nghìn, chấm thập phân, không có \".00\" thừa",
       "- Lưu ý: ERP hiện \"320.5 USD\" (màn) - so file Excel ở TC_06.009"]),
    T("008", "Ô rỗng để trống", "P1",
      ["TK-KT", "G1 chưa có phiếu kế toán, chưa có người duyệt"],
      ["1. " + M, "2. Quan sát dòng G1 cột Phiếu kế toán, Người duyệt", "3. " + E + ", cùng dòng"],
      "-",
      ["- HRM: 2 ô để TRỐNG, không có dấu \"-\"",
       "- ERP: in \"-\" (K7 - khác biệt đã chốt, không ghi lỗi)"]),
    T("009", "Nhãn và màu cột Trạng thái", "P1",
      ["TK-TCT", "G1 chưa có phiếu; G3 gắn PKT-T3 Đã duyệt; có 1 dòng gắn phiếu Đang tạo (sau TC_07.003) và 1 dòng "
       "gắn phiếu Hủy (sau TC_07.015)"],
      ["1. " + M, "2. Quan sát cột Trạng thái"],
      "-",
      ["- Chưa có phiếu: \"Chưa hạch toán\" nền vàng",
       "- Phiếu Đang tạo: \"Đang tạo\" nền xám (ERP đỏ - K7, khác biệt đã chốt, không ghi lỗi)",
       "- Phiếu Đã duyệt: \"Đã duyệt\" xanh lá; Phiếu Hủy: \"Hủy\" đỏ"]),
    T("010", "Dòng đã hạch toán: ô Hạch toán tick sẵn và khoá", "P0",
      ["TK-KT", "G3 Đã hạch toán (PKT-T3)"],
      ["1. " + M, "2. Bấm vào ô Hạch toán của G3", "3. Bấm vào ô Hạch toán của G1"],
      "-",
      ["- G3: ô đã tick, mờ, bấm không đổi",
       "- G1: ô trống, bấm thì tick được, bấm lần nữa bỏ tick",
       "- Giống ERP: dòng đã hạch toán tự tick + khoá"]),
    T("011", "Danh sách rỗng", "P1",
      ["TK-Z không có quyền nào, không chịu phí dòng nào"],
      ["1. Đăng nhập TK-Z", "2. " + M],
      "-",
      ["- Bảng hiện \"Không có dữ liệu phù hợp.\"; dưới bảng \"Không có dòng nào.\"",
       "- Không có nút \"Tạo phiếu kế toán\"; vẫn có \"Xuất Excel\", Cấu hình cột"]),
    T("012", "Phân trang mặc định", "P1",
      ["TK-TCT", "Bộ mẫu: 7 dòng giao nhanh, 10 dòng hàng"],
      ["1. " + M, "2. Quan sát dưới bảng"],
      "-",
      ["- \"Số dòng/trang:\" mặc định 10; danh sách chọn 5, 10, 20, 50, 100",
       "- \"Hiển thị 1–7 / 7\"; chỉ 1 trang",
       "- Khác ERP (K5): ERP 30 dòng hàng / trang - khác biệt đã chốt, không ghi lỗi"]),
    T("013", "Đổi số dòng/trang: cắt trang theo dòng giao nhanh", "P0",
      ["TK-TCT", "Thứ tự: G1 (2 hàng), G2, G3, G4, G5 (3 hàng), G6, P1"],
      ["1. " + M, "2. Chọn Số dòng/trang = 5"],
      "Số dòng/trang: 5",
      ["- Về trang 1: G1, G2, G3, G4, G5 (9 dòng hàng), STT 1 tới 5; \"Hiển thị 1–5 / 7\"",
       "- G5 hiện đủ 3 hàng ở trang 1, KHÔNG bị xé sang trang 2",
       "- Có 2 trang"]),
    T("014", "Chuyển trang: STT liên tục", "P1",
      ["Đang ở TC_01.013 (5 dòng / trang)"],
      ["1. Bấm trang 2", "2. Bấm nút trang trước", "3. Bấm nút trang cuối rồi trang đầu"],
      "-",
      ["- Trang 2: G6 STT 6, P1 STT 7; \"Hiển thị 6–7 / 7\"",
       "- Ở trang 1 nút trang trước / trang đầu mờ; ở trang 2 nút trang sau / trang cuối mờ",
       "- Khác ERP (K5): ERP đánh STT lại từ 1 mỗi trang - khác biệt đã chốt, không ghi lỗi"]),
    T("015", "Tổng N đếm theo dòng giao nhanh, so với ERP", "P0",
      ["TK-TCT", "Bộ mẫu 7 dòng giao nhanh / 10 dòng hàng"],
      ["1. " + M + ", đọc N", "2. " + E + ", đọc tổng ở thanh phân trang"],
      "-",
      ["- HRM N = 7 (số dòng giao nhanh)",
       "- ERP thanh phân trang tính 10 (số dòng hàng); số DÒNG GIAO NHANH ERP hiện trên bảng = 7, cùng các dòng như HRM",
       "- Lệch tổng là K5 - khác biệt đã chốt, không ghi lỗi; lệch số dòng giao nhanh là lỗi"]),
    T("016", "Thứ tự mặc định, không có cột sắp xếp", "P1",
      ["TK-TCT", "Dòng giao nhanh lập theo thứ tự G1, G2, G3, G4, G5, G6, P1"],
      ["1. " + M, "2. Bấm vào tiêu đề cột Chi phí KH, Khách hàng"],
      "-",
      ["- Thứ tự: G1, G2, G3, G4, G5, G6, P1 (lập trước đứng trước), mở lại màn vẫn đúng thứ tự này",
       "- Bấm tiêu đề cột không đổi thứ tự, không có biểu tượng mũi tên sắp xếp",
       "- ERP không cố định thứ tự (K6 - khác biệt đã chốt, không ghi lỗi)"]),
    T("017", "Đang ở trang 2 thì đổi lọc quay về trang 1", "P1",
      ["TK-TCT đang ở trang 2 (5 dòng / trang)"],
      ["1. " + LOC, "2. Chọn Trạng thái = Chưa hạch toán"],
      "Trạng thái: Chưa hạch toán",
      ["- Tự quay về trang 1: G1, G2, G4, G5, G6 (STT 1-5); \"Hiển thị 1–5 / 6\"",
       "- Trang 2: P1"]),
]

# ================================================================== II. TÌM KIẾM & LỌC DANH SÁCH
S2 = [
    T("001", "Tìm nhanh theo mã HĐ mua (một phần)", "P0",
      ["TK-KT", "HDM-T1 và phụ lục HDM-T1-PL1"],
      ["1. " + M, "2. Gõ vào ô tìm nhanh, bấm Enter"],
      "Từ khoá: HDM-T1",
      ["- Ra 2 dòng: G1 (HDM-T1) và P1 (HDM-T1-PL1)",
       "- \"Hiển thị 1–2 / 2\""]),
    T("002", "Tìm nhanh theo mã phiếu nhập", "P1",
      ["TK-KT", "PNH-T1 dùng cho G1 và P1"],
      ["1. Gõ vào ô tìm nhanh, Enter"],
      "Từ khoá: PNH-T1",
      ["- Ra G1 và P1 (cùng hiện Phiếu nhập PNH-T1)"]),
    T("003", "Tìm nhanh theo mã / tên khách, không phân biệt hoa thường", "P1",
      ["TK-KT", "KH-T02 tên \"Công ty TNHH Khách Test 02\" có G2, G6"],
      ["1. Gõ \"kh-t02\", Enter", "2. Xoá, gõ \"khách test 02\", Enter"],
      ["Từ khoá 1: kh-t02", "Từ khoá 2: khách test 02"],
      ["- Cả 2 lần ra G2, G6", "- Không ra dòng của khách khác"]),
    T("004", "Từ khoá không tồn tại", "P1",
      ["TK-KT"],
      ["1. Gõ vào ô tìm nhanh, Enter"],
      "Từ khoá: ZZZ-KHONG-CO",
      ["- Bảng \"Không có dữ liệu phù hợp.\"", "- Xoá từ khoá, Enter: hiện lại đủ 6 dòng"]),
    T("005", "Ký tự đặc biệt không làm ra toàn bộ danh sách", "P1",
      ["TK-KT"],
      ["1. Gõ \"%\", Enter", "2. Gõ \"_\", Enter", "3. Gõ \"HDM-T1'\", Enter"],
      ["Từ khoá: %", "Từ khoá: _", "Từ khoá: HDM-T1'"],
      ["- Lần 1, 2: 0 dòng (ký tự được tìm đúng nghĩa đen, không thành \"mọi giá trị\")",
       "- Lần 3: 0 dòng, màn không lỗi"]),
    T("006", "Khoảng trắng đầu / cuối từ khoá", "P2",
      ["TK-KT"],
      ["1. Gõ từ khoá có 2 khoảng trắng hai đầu, Enter"],
      "Từ khoá: \"  HDM-T2  \"",
      ["- Ra G2 như khi gõ \"HDM-T2\""]),
    T("007", "Ô tìm nhanh chỉ lọc khi Enter / bấm Tìm kiếm", "P2",
      ["TK-KT"],
      ["1. Gõ \"HDM-T2\", chưa bấm Enter, chờ 3 giây", "2. Bấm Enter"],
      "Từ khoá: HDM-T2",
      ["- Bước 1: bảng chưa đổi (vẫn 6 dòng)", "- Bước 2: còn G2"]),
    T("008", "Lọc Công ty", "P0",
      ["TK-TCT (Xem theo tổng công ty)"],
      ["1. " + M, "2. " + LOC, "3. Chọn Công ty = Công ty B", "4. Chọn lại Công ty = Công ty A"],
      ["Công ty: Công ty B", "Công ty: Công ty A"],
      ["- Công ty B: chỉ G4 (NV-B1)", "- Công ty A: G1, G2, G3, G5, G6, P1",
       "- Lọc theo công ty của NHÂN VIÊN CHỊU PHÍ, không theo công ty khách hàng"]),
    T("009", "Bộ lọc dây chuyền Phòng ban > Bộ phận > Nhân viên", "P1",
      ["TK-TCT"],
      ["1. Chọn Công ty A, Phòng ban PB-A1", "2. Chọn thêm Bộ phận BP-A1b", "3. Bỏ Bộ phận, mở ô Nhân viên"],
      ["Phòng ban: PB-A1", "Bộ phận: BP-A1b"],
      ["- Bước 1: G1, G3, G5, P1", "- Bước 2: chỉ G5 (NV-A3)",
       "- Ô Bộ phận chỉ liệt kê bộ phận của PB-A1; ô Nhân viên chỉ liệt kê nhân viên thuộc lựa chọn phía trên",
       "- Đổi Công ty thì Phòng ban, Bộ phận, Nhân viên tự xoá"]),
    T("010", "Lọc Nhân viên chịu phí", "P1",
      ["TK-TCT"],
      ["1. Chọn Nhân viên = NV-A1"],
      "Nhân viên: NV-A1",
      ["- Ra G1, G3, P1", "- So ERP cùng điều kiện: cùng 3 dòng"]),
    T("011", "Lọc Ngày nhập 1 ngày", "P0",
      ["TK-TCT", "Ngày lập phiếu nhập: G2, G3 ngày 02/11/2026; G1 (15:00), G4, G6, P1 ngày 03/11/2026; G5 01/11/2026"],
      ["1. Ô Ngày nhập chọn 02/11/2026 đến 02/11/2026", "2. Đổi thành 01/11/2026 đến 03/11/2026"],
      ["Ngày nhập: 02/11/2026 - 02/11/2026", "Ngày nhập: 01/11/2026 - 03/11/2026"],
      ["- Lần 1: G2, G3", "- Lần 2: đủ 7 dòng",
       "- Lọc theo ngày lập phiếu nhập, không theo ngày HĐ mua"]),
    T("012", "Đến ngày lấy hết ngày (HRM sửa lỗi ERP)", "P0",
      ["TK-TCT", "PNH-T1 (G1, P1) lập 03/11/2026 15:00"],
      ["1. HRM: Ngày nhập 03/11/2026 đến 03/11/2026", "2. " + E + ", Từ ngày 03/11/2026, Đến ngày 03/11/2026, Lọc"],
      "Ngày nhập: 03/11/2026 - 03/11/2026",
      ["- HRM: G1, G4, G6, P1 (phiếu nhập lập trong ngày 03/11 đều ra)",
       "- ERP: 0 dòng vì so Đến ngày ở 00:00 (K3) - HRM đúng; hiện tượng ERP, không ghi lỗi HRM",
       "- ERP phải chọn Đến ngày 04/11/2026 mới ra 4 dòng trên"]),
    T("013", "Lọc Trạng thái Chưa hạch toán", "P0",
      ["TK-KT", "Chưa hạch toán Công ty A: G1, G2, G5, G6, P1"],
      ["1. Chọn Trạng thái = Chưa hạch toán"],
      "Trạng thái: Chưa hạch toán",
      ["- Ra 5 dòng G1, G2, G5, G6, P1; ô Hạch toán đều trống, tick được",
       "- Cột Trạng thái đều \"Chưa hạch toán\""]),
    T("014", "Lọc Trạng thái Đã hạch toán", "P0",
      ["TK-KT", "G3 Đã hạch toán"],
      ["1. Chọn Trạng thái = Đã hạch toán", "2. Bỏ chọn Trạng thái"],
      "Trạng thái: Đã hạch toán",
      ["- Lần 1: chỉ G3, ô tick sẵn khoá, Phiếu kế toán PKT-T3, Người duyệt TK-TCT, Trạng thái \"Đã duyệt\"",
       "- Bỏ chọn: hiện lại cả 6 dòng"]),
    T("015", "Lọc Khách hàng: gõ tối thiểu 2 ký tự", "P1",
      ["TK-TCT", "KH-T01 có G1, G4, P1"],
      ["1. Bấm ô Khách hàng, gõ \"K\"", "2. Gõ thêm \"H-T01\"", "3. Chọn KH-T01", "4. Bấm nút x xoá ô Khách hàng"],
      "Khách hàng: KH-T01",
      ["- Bước 1: chưa có gợi ý (cần ít nhất 2 ký tự)", "- Bước 2: có gợi ý KH-T01",
       "- Bước 3: lọc ngay, ra G1, G4, P1", "- Bước 4: hiện lại đủ 7 dòng"]),
    T("016", "Lọc Phiếu kế toán theo một phần mã", "P1",
      ["TK-KT", "G3 gắn PKT-T3 (mã thật ghi ở Ghi chú)"],
      ["1. Ô Phiếu kế toán gõ 4 ký tự cuối của mã PKT-T3, Enter", "2. Gõ \"%\", Enter"],
      "Phiếu kế toán: <4 ký tự cuối mã PKT-T3>",
      ["- Lần 1: G3", "- Lần 2: 0 dòng (không ra mọi dòng có phiếu)",
       "- Gợi ý ô: \"Nhập mã phiếu kế toán\""]),
    T("017", "Lọc Hợp đồng gồm cả phụ lục", "P1",
      ["TK-KT"],
      ["1. Ô Hợp đồng gõ \"HDM-T1\", Enter", "2. Gõ \"PL1\", Enter"],
      ["Hợp đồng: HDM-T1", "Hợp đồng: PL1"],
      ["- Lần 1: G1, P1", "- Lần 2: chỉ P1", "- Gợi ý ô: \"Nhập mã hợp đồng\""]),
    T("018", "Lọc Người duyệt phiếu kế toán", "P1",
      ["TK-KT", "PKT-T3 (G3) do TK-TCT duyệt"],
      ["1. Ô Người duyệt chọn TK-TCT", "2. Chọn một nhân viên chưa duyệt phiếu nào"],
      "Người duyệt: TK-TCT",
      ["- Lần 1: chỉ G3", "- Lần 2: 0 dòng"]),
    T("019", "Người duyệt đã nghỉ việc vẫn chọn được", "P2",
      ["Một phiếu kế toán gắn dòng giao nhanh do nhân viên NV-NGHI duyệt, nay NV-NGHI đã nghỉ việc"],
      ["1. Ô Người duyệt gõ tên NV-NGHI"],
      "Người duyệt: NV-NGHI",
      ["- Có NV-NGHI trong danh sách chọn (ERP cho chọn cả nhân viên nghỉ việc)",
       "- Chọn xong ra đúng dòng do NV-NGHI duyệt"]),
    T("020", "Kết hợp nhiều điều kiện", "P1",
      ["TK-TCT"],
      ["1. Chọn Công ty A, Trạng thái Chưa hạch toán, Ngày nhập 03/11/2026 - 03/11/2026, Khách hàng KH-T01"],
      ["Công ty: Công ty A", "Trạng thái: Chưa hạch toán", "Ngày nhập: 03/11/2026 - 03/11/2026", "Khách hàng: KH-T01"],
      ["- Ra G1, P1 (G4 bị loại vì Công ty B)", "- \"Hiển thị 1–2 / 2\"",
       "- ERP cùng điều kiện (Đến ngày 04/11/2026): cùng 2 dòng"]),
    T("021", "Làm mới xoá điều kiện và tải lại", "P1",
      ["TK-KT đang lọc ở TC_02.013 và từ khoá \"HDM\""],
      ["1. Bấm \"Làm mới\" trên bảng lọc", "2. " + E + ", đặt vài điều kiện, bấm nút Làm mới"],
      "-",
      ["- HRM: mọi ô lọc và ô tìm nhanh xoá trắng; bảng tải lại đủ 6 dòng, về trang 1",
       "- ERP: xoá điều kiện và xoá trắng bảng, phải bấm Lọc lại (K2 - khác biệt đã chốt, không ghi lỗi)"]),
    T("022", "Không chọn được công ty ngoài phạm vi", "P0",
      ["TK-KT (Xem theo công ty, Công ty A)"],
      ["1. " + LOC, "2. Mở ô Công ty", "3. Tìm khách hàng KH-T01 (có G4 của Công ty B)"],
      "Khách hàng: KH-T01",
      ["- Ô Công ty chỉ có Công ty A",
       "- Bước 3: ra G1, P1; KHÔNG có G4 (dòng Công ty B không lộ dù lọc theo khách)"]),
    T("023", "Tải lại trang thì bộ lọc về mặc định", "P2",
      ["TK-KT đang lọc Trạng thái = Đã hạch toán"],
      ["1. Bấm F5", "2. Lọc lại, mở sang màn khác trong cùng tab rồi quay lại màn"],
      "-",
      ["- Sau F5 và sau khi quay lại: ô Trạng thái trống, bảng hiện đủ 6 dòng",
       "- Lưu ý: màn không có trang chi tiết riêng (các link mở tab mới) nên không ghi nhớ bộ lọc; ghi Ghi chú nếu nghiệp "
       "vụ muốn giữ"]),
]

# ================================================================== III. SỐ LIỆU BÁO CÁO
S3 = [
    T("001", "Dòng giao nhanh mới lập, chưa có phiếu nhập: chưa lên", "P0",
      ["TK-KT", "Chưa có HDM-T1"],
      ["1. " + HDM_E + ", tạo HĐ HDM-T1 loại tiền USD, " + TAB_CPVC + ": Người chịu phí NV-A1, Khách hàng KH-T01, "
       "Chi phí theo khách hàng 1,250, Hàng hóa HH-01, HH-02; duyệt HĐ", "2. " + M + ", tìm \"HDM-T1\"", "3. " + E],
      ["Người chịu phí: NV-A1", "Khách hàng: KH-T01", "Chi phí theo khách hàng: 1,250", "Hàng hóa: HH-01, HH-02"],
      ["- HRM và ERP đều KHÔNG có HDM-T1 (hàng chưa về kho)"]),
    T("002", "Hoàn thành phiếu nhập trên HRM: dòng lên cả 2 hệ thống", "P0",
      ["Đã chạy TC_03.001", "Yêu cầu nhập hàng của HDM-T1 có hàng cho KH-T01"],
      ["1. " + PNH_H + ", lập phiếu nhập loại \"Nhập hàng mua nước ngoài(mới)\" từ Yêu cầu nhập hàng của HDM-T1, có hàng "
       "của KH-T01, hoàn thành phiếu (ghi mã PNH-T1)", "2. " + M + ", tìm \"HDM-T1\"", "3. " + E + ", Hợp đồng HDM-T1"],
      "Loại phiếu nhập: Nhập hàng mua nước ngoài(mới)",
      ["- HRM: có G1, Phiếu nhập PNH-T1, Chi phí KH \"1,250 USD\", Trạng thái \"Chưa hạch toán\"",
       "- ERP: có đúng dòng đó (cùng dữ liệu)"]),
    T("003", "Hoàn thành phiếu nhập trên ERP: HRM thấy ngay", "P0",
      ["HDM-T2 (JPY) đã duyệt, dòng giao nhanh NV-A2, KH-T02, 85,000, HH-03; chưa có phiếu nhập"],
      ["1. " + PNH_E + ", lập và hoàn thành phiếu nhập PNH-T2 cho HDM-T2, có hàng của KH-T02",
       "2. " + M + " (TK-KT), tìm \"HDM-T2\""],
      "-",
      ["- HRM có G2 ngay, không cần thao tác gì thêm: PNH-T2, \"85,000 JPY\", Chưa hạch toán",
       "- Cột Người tạo = người lập PNH-T2 (NV-KHO)"]),
    T("004", "Đối chiếu từng cột một dòng giữa ERP và HRM", "P0",
      ["TK-KT", "G1 đủ dữ liệu (TC_03.002)"],
      ["1. " + E + ", tìm dòng HDM-T1", "2. " + M + ", tìm \"HDM-T1\"", "3. So từng cột"],
      "-",
      ["- Nhân viên chịu phí \"NV-A1 - <tên>\", Phiếu nhập PNH-T1, Khách hàng \"KH-T01 - <tên>\", Hàng hóa HH-01, HH-02 "
       "(mỗi hàng có dòng \"Mã hàng: ...\"), Chi phí KH \"1,250 USD\", Hợp đồng mua HDM-T1, Người tạo NV-KHO, Trạng thái "
       "Chưa hạch toán: GIỐNG nhau 2 bên",
       "- Khác trình bày đã chốt: ô rỗng HRM trống / ERP \"-\" (K7)"]),
    T("005", "Đối chiếu số dòng theo phạm vi từng tài khoản", "P0",
      ["Bộ mẫu mục 1; TK-TCT, TK-KT, TK-PB, TK-BP, NV-A1, NV-A2"],
      ["1. Lần lượt đăng nhập từng tài khoản: " + M + ", ghi danh sách dòng", "2. Cùng tài khoản: " + E + ", ghi danh sách dòng"],
      "-",
      ["- TK-TCT 7; TK-KT 6 (không G4); TK-PB 4 (G1, G3, G5, P1); TK-BP 3 (G1, G3, P1); NV-A1 3 (G1, G3, P1); NV-A2 2 "
       "(G2, G6)",
       "- Từng tài khoản: tập dòng HRM TRÙNG ERP",
       "- Tổng ở thanh phân trang ERP đếm theo dòng hàng (K5), không so con số đó"]),
    T("006", "HĐ mua chưa duyệt không lên", "P0",
      ["N1: HDM-N1 Chờ duyệt, có dòng giao nhanh NV-A1, KH-T04 và phiếu nhập hoàn thành"],
      ["1. " + M + " (TK-TCT), tìm \"HDM-N1\"", "2. " + E + ", Hợp đồng HDM-N1", "3. ERP duyệt HDM-N1, tải lại HRM"],
      "-",
      ["- Bước 1, 2: không có dòng HDM-N1 ở cả 2 bên",
       "- Bước 3: HRM xuất hiện dòng HDM-N1 (KH-T04), Chưa hạch toán"]),
    T("007", "Phiếu nhập chưa hoàn thành không lên", "P0",
      ["N2: HDM-N2 Đã duyệt, phiếu nhập PNH-N2 Đang tạo"],
      ["1. " + M + " (TK-TCT), tìm \"HDM-N2\"", "2. Hoàn thành PNH-N2 (HRM hoặc ERP)", "3. Tải lại màn HRM và ERP"],
      "-",
      ["- Bước 1: không có HDM-N2", "- Bước 3: cả 2 bên có dòng HDM-N2, Phiếu nhập PNH-N2"]),
    T("008", "Chưa có phiếu nhập không lên", "P1",
      ["N3: HDM-N3 Đã duyệt, chưa lập phiếu nhập"],
      ["1. " + M + " (TK-TCT), tìm \"HDM-N3\"", "2. " + E + ", Hợp đồng HDM-N3"],
      "-",
      ["- Cả 2 bên không có HDM-N3"]),
    T("009", "Phiếu nhập không có hàng của đúng khách không lên", "P1",
      ["N4: dòng giao nhanh KH-T06; phiếu nhập của HDM-N4 chỉ có hàng của KH-T07"],
      ["1. " + M + " (TK-TCT), Hợp đồng \"HDM-N4\"", "2. " + E + ", cùng điều kiện"],
      "Hợp đồng: HDM-N4",
      ["- Cả 2 bên 0 dòng", "- Khi phiếu nhập khác của HDM-N4 có hàng KH-T06 hoàn thành thì dòng mới lên"]),
    T("010", "Phiếu nhập loại khác không lên", "P1",
      ["N5: phiếu nhập của HDM-N5 loại \"Nhập hàng mua trong nước\", Đã hoàn thành"],
      ["1. " + M + " (TK-TCT), Hợp đồng \"HDM-N5\"", "2. " + E + ", cùng điều kiện"],
      "Hợp đồng: HDM-N5",
      ["- Cả 2 bên 0 dòng (chỉ tính loại Nhập hàng mua nước ngoài(mới))"]),
    T("011", "Phụ lục dùng phiếu nhập của HĐ cha", "P0",
      ["P1: HDM-T1-PL1 là Phụ lục bổ sung của HDM-T1, dòng giao nhanh NV-A1, KH-T01, 100 USD; không có phiếu nhập riêng"],
      ["1. " + M + " (TK-KT), Hợp đồng \"PL1\"", "2. " + E + ", Hợp đồng PL1"],
      "Hợp đồng: PL1",
      ["- Cả 2 bên có 1 dòng: Hợp đồng mua HDM-T1-PL1, Phiếu nhập PNH-T1 (của HĐ cha), Chi phí KH \"100 USD\"",
       "- P1 là dòng RIÊNG, không gộp với G1"]),
    T("012", "HĐ mua bị hủy thì dòng biến mất cả 2 bên", "P1",
      ["G6 (HDM-T6) đang hiện, Chưa hạch toán"],
      ["1. " + HDM_E + ", hủy HDM-T6", "2. Tải lại màn HRM (TK-KT) và ERP"],
      "-",
      ["- Cả 2 bên không còn G6", "- Mở lại HĐ (duyệt lại) thì G6 hiện lại"]),
    T("013", "Một dòng có 2 phiếu nhập: không lặp hàng hoá", "P0",
      ["G1 đã có PNH-T1; lập thêm PNH-T1B (hoàn thành, sau PNH-T1) cho HDM-T1 có hàng KH-T01"],
      ["1. " + M + " (TK-KT), tìm \"HDM-T1\"", "2. " + E + ", Hợp đồng HDM-T1"],
      "-",
      ["- HRM: G1 vẫn 1 dòng, Phiếu nhập PNH-T1 (lập trước), Hàng hóa đúng 2 dòng HH-01, HH-02",
       "- ERP: cũng 1 dòng PNH-T1 nhưng Hàng hóa lặp 4 dòng (K4 - khác biệt đã chốt, không ghi lỗi)",
       "- Lọc Ngày nhập theo ngày của PNH-T1B vẫn ra G1"]),
    T("014", "Dòng của công ty khác chỉ người xem tổng công ty thấy", "P0",
      ["G4: NV-B1 (Công ty B)"],
      ["1. TK-TCT: " + M, "2. TK-KT: " + M, "3. TK-KT: " + E],
      "-",
      ["- TK-TCT thấy G4; TK-KT KHÔNG thấy G4 ở cả HRM lẫn ERP"]),
    T("015", "Người tạo là người lập phiếu nhập", "P1",
      ["G2: HĐ do nhân viên mua hàng NV-MH lập, phiếu nhập PNH-T2 do NV-KHO lập"],
      ["1. " + M + ", xem cột Người tạo của G2"],
      "-",
      ["- Người tạo = NV-KHO (người lập phiếu nhập), KHÔNG phải NV-MH", "- ERP hiện cùng giá trị"]),
    T("016", "Sửa chi phí trên HĐ mua thì danh sách cập nhật", "P1",
      ["G5 chưa hạch toán, 320.5 USD"],
      ["1. " + HDM_E + ", sửa HDM-T5 " + TAB_CPVC + ": Chi phí theo khách hàng = 330.25 (duyệt lại nếu cần)",
       "2. Tải lại màn HRM và ERP"],
      "Chi phí theo khách hàng: 330.25",
      ["- HRM G5 Chi phí KH \"330.25 USD\"; ERP cùng số",
       "- Sau TC trả lại 320.5 để các TC sau dùng đúng số"]),
]

# ================================================================== IV. XEM CHI TIẾT
S4 = [
    T("001", "Bấm mã Phiếu nhập mở màn HRM", "P1",
      ["TK-KT có quyền xem phiếu nhập hàng của Công ty A"],
      ["1. " + M, "2. Bấm mã PNH-T1 ở dòng G1"],
      "-",
      ["- Mở TAB MỚI màn chi tiết Phiếu nhập hàng PNH-T1 của HRM; tab danh sách giữ nguyên",
       "- ERP bấm cùng mã mở màn ERP (K10 - khác biệt đã chốt)"]),
    T("002", "Bấm mã Phiếu kế toán mở màn HRM", "P1",
      ["G3 gắn PKT-T3"],
      ["1. Bấm mã PKT-T3 ở dòng G3"],
      "-",
      ["- Tab mới mở màn chi tiết Phiếu kế toán PKT-T3 của HRM, trạng thái Đã duyệt, có 2 dòng Nợ 35241 / Có 811 "
       "2,500,000"]),
    T("003", "Bấm mã Hợp đồng mua mở ERP", "P1",
      ["G1 thuộc HDM-T1"],
      ["1. Bấm mã HDM-T1 ở cột Hợp đồng mua"],
      "-",
      ["- Tab mới mở màn xem Hợp đồng mua HDM-T1 trên ERP (HRM chưa có màn này)",
       "- " + TAB_CPVC + " có dòng NV-A1, KH-T01, 1,250"]),
    T("004", "Không có quyền xem phiếu nhập: link không lộ dữ liệu", "P2",
      ["NV-A1 (không quyền xem phiếu nhập hàng nào), chịu phí G1"],
      ["1. Đăng nhập NV-A1", "2. " + M, "3. Bấm PNH-T1"],
      "-",
      ["- Danh sách vẫn hiện G1 (dòng mình chịu phí)",
       "- Màn phiếu nhập tự áp quyền của nó: báo không có quyền / không tìm thấy, không hiện nội dung phiếu"]),
]

# ================================================================== V. TÙY CHỈNH CỘT
S5 = [
    T("001", "Mở Cấu hình cột", "P1",
      ["TK-KT"],
      ["1. " + M, "2. Bấm nút Cấu hình cột (gợi ý \"Cấu hình cột hiển thị\")"],
      "-",
      ["- Popup liệt kê đủ 12 cột theo thứ tự trên bảng",
       "- STT, Hàng hóa, Hạch toán không bỏ chọn được (khoá)"]),
    T("002", "Ẩn cột và giữ sau khi tải lại", "P1",
      ["TK-KT"],
      ["1. Bỏ chọn Người tạo, Người duyệt, lưu", "2. Bấm F5", "3. Mở lại Cấu hình cột, chọn lại 2 cột"],
      "-",
      ["- Bước 1: bảng không còn 2 cột, các cột khác giữ nguyên gộp ô",
       "- Bước 2: vẫn ẩn", "- Bước 3: 2 cột hiện lại đúng vị trí"]),
    T("003", "Ẩn cột không ảnh hưởng tick và tạo phiếu", "P2",
      ["TK-KT đã ẩn Phiếu kế toán, Trạng thái"],
      ["1. Tick G6", "2. " + TAO],
      "-",
      ["- Mở form \"Tạo phiếu kế toán\" nạp đúng G6 (như TC_07.007)"]),
    T("004", "Cấu hình cột riêng từng tài khoản", "P2",
      ["TK-KT đã ẩn Người tạo; TK-KT2 chưa đổi gì"],
      ["1. Đăng nhập TK-KT2", "2. " + M],
      "-",
      ["- TK-KT2 vẫn thấy đủ 12 cột"]),
]

# ================================================================== VI. XUẤT DANH SÁCH EXCEL
S6 = [
    T("001", "Popup chọn trường xuất", "P1",
      ["TK-KT"],
      ["1. " + M, "2. Bấm \"Xuất Excel\""],
      "-",
      ["- Popup \"Chọn trường xuất Excel\" tick sẵn 9 trường: Nhân viên chịu phí, Phiếu nhập, Khách hàng, Hàng hóa, Mã "
       "hàng, Chi phí KH, Đã hạch toán, Diễn giải, Người cập nhật",
       "- Không có trường Hạch toán, Phiếu kế toán, Hợp đồng mua, Người tạo, Người duyệt, Trạng thái (giống file ERP)"]),
    T("002", "Xuất đủ trường: cấu trúc file", "P0",
      ["TK-KT, không lọc"],
      ["1. Bấm \"Xuất Excel\", giữ đủ trường, bấm xuất", "2. Mở file"],
      "-",
      ["- Báo \"Xuất Excel thành công\"; tên file danh_sach_can_hach_toan_chi_phi_van_chuyen_nhanh.xlsx",
       "- Đầu file có thông tin công ty của TK-KT, tiêu đề \"DANH SÁCH CẦN HẠCH TOÁN CHI PHÍ VẬN CHUYỂN NHANH\"",
       "- 10 cột: STT, Nhân viên chịu phí, Phiếu nhập, Khách hàng, Hàng hóa, Mã hàng, Chi phí KH, Đã hạch toán, Diễn giải, "
       "Người cập nhật",
       "- G5 chiếm 3 dòng (HH-06, HH-07, HH-08); các cột trừ Hàng hóa, Mã hàng gộp ô 3 dòng; STT theo dòng giao nhanh 1-6"]),
    T("003", "Nội dung từng cột trong file", "P0",
      ["File ở TC_06.002"],
      ["1. Đọc dòng G1, G3, G5"],
      "-",
      ["- G1: \"NV-A1 - <tên>\", PNH-T1, \"KH-T01 - <tên>\", HH-01 / HH-02 tách 2 dòng, Mã hàng HH-01 / HH-02, Chi phí "
       "KH \"1,250 USD\", Đã hạch toán \"Chưa hạch toán\"",
       "- G3: \"2,500,000 VNĐ\", \"Đã hạch toán\"", "- G5: \"320.5 USD\"",
       "- Ô Diễn giải, Người cập nhật trống nếu dòng chưa có"]),
    T("004", "File theo bộ lọc và phạm vi", "P0",
      ["TK-KT (Công ty A)"],
      ["1. Lọc Trạng thái Chưa hạch toán", "2. Xuất Excel"],
      "Trạng thái: Chưa hạch toán",
      ["- File có G1, G2, G5, G6, P1; KHÔNG có G3 (đã hạch toán), KHÔNG có G4 (Công ty B)",
       "- Số dòng giao nhanh trong file = N trên màn (5)"]),
    T("005", "Tiêu đề file có khoảng ngày", "P1",
      ["TK-TCT"],
      ["1. Ngày nhập 02/11/2026 - 03/11/2026", "2. Xuất Excel"],
      "Ngày nhập: 02/11/2026 - 03/11/2026",
      ["- Tiêu đề \"DANH SÁCH CẦN HẠCH TOÁN CHI PHÍ VẬN CHUYỂN NHANH (TỪ NGÀY 02/11/2026 ĐẾN NGÀY 03/11/2026)\"",
       "- File có G1, G2, G3, G4, G6, P1; không có G5",
       "- ERP in khoảng ngày ở dòng riêng (K11 - khác biệt đã chốt)"]),
    T("006", "Bỏ bớt trường", "P1",
      ["TK-KT"],
      ["1. Xuất Excel, bỏ tick Diễn giải, Người cập nhật, Mã hàng", "2. Mở file"],
      "-",
      ["- File còn STT, Nhân viên chịu phí, Phiếu nhập, Khách hàng, Hàng hóa, Chi phí KH, Đã hạch toán",
       "- Gộp ô theo hàng hoá vẫn đúng"]),
    T("007", "Không có dữ liệu thì báo", "P1",
      ["TK-KT"],
      ["1. Tìm nhanh \"ZZZ-KHONG-CO\"", "2. Bấm Xuất Excel, xuất"],
      "Từ khoá: ZZZ-KHONG-CO",
      ["- Báo \"Không có dữ liệu để xuất\", không tải file",
       "- ERP mờ nút Xuất excel khi bảng rỗng (K11 - khác biệt đã chốt)"]),
    T("008", "Từ 2,000 dòng hàng trở lên thì chặn", "P1",
      ["Môi trường có từ 2,000 dòng hàng giao nhanh đủ điều kiện trở lên (dùng TK-TCT; dữ liệu nhỏ thì bỏ qua, ghi Ghi chú)"],
      ["1. Không lọc gì, bấm Xuất Excel, xuất"],
      "-",
      ["- Báo \"" + MSG_LON + "\", không tải file",
       "- Lọc hẹp lại (dưới 2,000 dòng hàng) thì xuất được"]),
    T("009", "So file Excel HRM với ERP", "P1",
      ["TK-TCT, không lọc"],
      ["1. Xuất Excel HRM", "2. " + E + ", bấm \"Xuất excel\"", "3. So 2 file"],
      "-",
      ["- Cùng tập dòng, cùng nhân viên, phiếu nhập, khách, hàng, trạng thái",
       "- Chi phí KH G5: HRM \"320.5 USD\", ERP \"321 USD\" (ERP làm tròn - K11, khác biệt đã chốt, không ghi lỗi)"]),
    T("010", "Bấm Xuất Excel liên tục", "P2",
      ["TK-KT"],
      ["1. Bấm Xuất Excel, xuất, rồi bấm lại ngay khi chữ tiến độ đang hiện"],
      "-",
      ["- Trong lúc xuất có chữ tiến độ \"Đang chuẩn bị dữ liệu…\", nút Xuất Excel không bấm được",
       "- Chỉ tải 1 file"]),
]

# ================================================================== VII. RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC
S7 = [
    T("001", "Bấm Tạo phiếu kế toán khi chưa tick dòng nào", "P0",
      ["TK-KT"],
      ["1. " + M, "2. " + TAO],
      "-",
      ["- Báo \"" + MSG_CHON + "\"", "- Không chuyển màn"]),
    T("002", "Tick 2 dòng USD: form phiếu kế toán nạp đúng", "P0",
      ["TK-KT", "G1 1,250 USD, P1 100 USD, Chưa hạch toán; USD tỷ giá 25,350"],
      ["1. " + M, "2. Tick G1, P1", "3. " + TAO],
      "-",
      ["- Chuyển sang màn \"Tạo phiếu kế toán\"; ô \"Chi phí vận chuyển nhanh\" = \"2 dòng\"; không hiện ô Phiếu yêu cầu "
       "điều chỉnh công nợ",
       "- Loại tiền USD, Tỷ giá (VND) 25,350",
       "- Bảng định khoản 4 dòng: nhóm 1: 35241 Phát sinh nợ 1,250 (quy đổi 31,687,500) / 811 Phát sinh có 1,250; nhóm 2: "
       "35241 nợ 100 (2,535,000) / 811 có 100; Mã khách KH-T01 cả 4 dòng",
       "- Không có nút thêm / xoá dòng định khoản",
       "- ERP cùng 2 dòng ra cùng số (đối chiếu)"]),
    T("003", "Lưu nháp: dòng chuyển đã hạch toán ngay", "P0",
      ["Đang ở form TC_07.002"],
      ["1. Chọn Ngày hạch toán 04/11/2026, bấm \"Lưu nháp\"", "2. " + M + ", tìm \"HDM-T1\""],
      "Ngày hạch toán: 04/11/2026",
      ["- Báo \"Thêm mới thành công.\", về danh sách Phiếu kế toán; phiếu mới trạng thái Đang tạo (ghi mã PKT-01)",
       "- G1, P1: ô Hạch toán tick sẵn + khoá, Phiếu kế toán PKT-01, Trạng thái \"Đang tạo\", Người duyệt trống",
       "- Lọc Chưa hạch toán: không còn G1, P1"]),
    T("004", "Hạch toán ở HRM thì ERP cập nhật", "P0",
      ["Đã chạy TC_07.003"],
      ["1. " + E + ", Trạng thái Chưa hạch toán, Lọc", "2. Bỏ Trạng thái, tìm Hợp đồng HDM-T1", "3. " + PKT_E + ", mở PKT-01"],
      "-",
      ["- Bước 1: không còn G1, P1", "- Bước 2: G1, P1 ô tick khoá, Phiếu kế toán PKT-01, badge Đang tạo",
       "- Bước 3: PKT-01 có đúng 4 dòng định khoản, loại tiền USD"]),
    T("005", "Lưu và duyệt: ghi bút toán, đối chiếu ERP", "P0",
      ["TK-KT có Kế toán thanh toán", "G2 85,000 JPY Chưa hạch toán; JPY tỷ giá 168"],
      ["1. Tick G2, " + TAO, "2. Nhập Ngày hạch toán 04/11/2026, Diễn giải \"Hạch toán CPVC nhanh HDM-T2\", diễn giải 2 "
       "dòng định khoản; bấm \"Lưu và duyệt\", xác nhận", "3. " + M + ", xem G2", "4. " + SO_E + ", tài khoản 35241 và 811, "
       "ngày 04/11/2026"],
      ["Diễn giải: Hạch toán CPVC nhanh HDM-T2", "Ngày hạch toán: 04/11/2026"],
      ["- Báo \"Duyệt phiếu kế toán thành công.\" (ghi mã PKT-02)",
       "- G2: Phiếu kế toán PKT-02, Người duyệt TK-KT, Trạng thái \"Đã duyệt\"",
       "- Sổ chi tiết ERP: 35241 phát sinh nợ 85,000 JPY (14,280,000 VNĐ), 811 phát sinh có cùng số, đối tượng KH-T02, "
       "chứng từ PKT-02",
       "- ERP danh sách: G2 Đã duyệt, Người duyệt TK-KT"]),
    T("006", "Loại tiền ngoại tệ không bị ép VNĐ", "P0",
      ["G5 320.5 USD"],
      ["1. Tick G5, " + TAO],
      "-",
      ["- Loại tiền USD (KHÔNG phải VNĐ), Tỷ giá 25,350; nợ 35241 320.5, quy đổi 8,124,675",
       "- Bấm \"Quay lại\" không lưu: G5 vẫn Chưa hạch toán"]),
    T("007", "Dòng VNĐ: tỷ giá 1", "P1",
      ["G6 1,800,000 VNĐ Chưa hạch toán"],
      ["1. Tick G6, " + TAO],
      "-",
      ["- Loại tiền VNĐ, Tỷ giá 1, không có cột quy đổi ngoại tệ",
       "- Nợ 35241 1,800,000 / Có 811 1,800,000, khách KH-T02"]),
    T("008", "Loại tiền không có trong danh mục đang dùng", "P1",
      ["G5 (USD) Chưa hạch toán; tạm tắt loại tiền USD trong danh mục Tiền tệ (bật lại sau TC)"],
      ["1. Tick G5, " + TAO, "2. Bấm \"Quay lại\" không lưu"],
      "-",
      ["- Ô Loại tiền TRỐNG để người dùng chọn (giống ERP), các dòng định khoản vẫn nạp 320.5",
       "- Bấm Lưu và duyệt khi chưa chọn Loại tiền thì báo \"Bạn chưa nhập đầy đủ thông tin.\""]),
    T("009", "Tick 2 dòng khác loại tiền: lấy theo dòng đầu", "P1",
      ["G5 (USD, lập trước) và G6 (VNĐ) Chưa hạch toán"],
      ["1. Tick G6 rồi G5, " + TAO, "2. Bấm \"Quay lại\" không lưu"],
      "-",
      ["- Loại tiền USD theo dòng LẬP TRƯỚC (G5), không theo thứ tự tick",
       "- Dòng G6 nạp 1,800,000 nhưng tính theo USD - giống ERP, không chặn",
       "- Lưu ý: nghiệp vụ nên tick các dòng cùng loại tiền; ghi Ghi chú nếu muốn chặn"]),
    T("010", "Popup chọn hợp đồng ở dòng giao nhanh", "P1",
      ["KH-T01 có HĐ bán HDB-01 do NV-A1 lập, HDB-02 do NV-A2 lập, HĐ dịch vụ bảo hành HDV-01 do NV-A1 lập, HĐ mua của "
       "KH-T01", "Form TC_07.002 đang mở (G1)"],
      ["1. Ở dòng 35241 của G1, mở popup chọn Đơn hàng/Hợp đồng", "2. Ở một phiếu kế toán tạo tay, dòng khách KH-T01, mở "
       "popup"],
      "-",
      ["- Bước 1: chỉ HDB-01 và HDV-01 (hợp đồng bán của khách do NV-A1 - nhân viên chịu phí - lập); không có HDB-02, "
       "không có HĐ mua",
       "- Bước 2: popup giữ như cũ (có HDB-02)"]),
    T("011", "Tick mất khi đổi trang", "P1",
      ["TK-TCT, 5 dòng / trang; G4 (trang 1) Chưa hạch toán"],
      ["1. Tick G4", "2. Sang trang 2, tick G6", "3. Quay về trang 1", "4. " + TAO],
      "-",
      ["- Bước 3: G4 không còn tick (tick chỉ có tác dụng trong trang đang xem, giống ERP)",
       "- Bước 4: báo \"" + MSG_CHON + "\", không chuyển màn"]),
    T("012", "Tick mất khi đổi bộ lọc", "P2",
      ["TK-KT, G5 Chưa hạch toán"],
      ["1. Tick G5", "2. Chọn Trạng thái Chưa hạch toán", "3. " + TAO],
      "-",
      ["- Bước 2: G5 hết tick", "- Bước 3: báo \"" + MSG_CHON + "\""]),
    T("013", "Xoá phiếu kế toán trên HRM: dòng về Chưa hạch toán", "P0",
      ["PKT-01 Đang tạo (G1, P1) do TK-KT lập"],
      ["1. " + PKT_H + ", xoá PKT-01", "2. " + M + ", tìm \"HDM-T1\"", "3. " + E + ", Hợp đồng HDM-T1"],
      "-",
      ["- Báo \"Xóa thành công.\"",
       "- HRM và ERP: G1, P1 Chưa hạch toán, ô tick mở, Phiếu kế toán trống",
       "- Tick G1, P1 tạo lại phiếu được bình thường"]),
    T("014", "Xoá phiếu kế toán trên ERP: dòng kẹt (hiện tượng ERP)", "P1",
      ["Tạo lại phiếu cho G1 trên HRM (Lưu nháp, mã PKT-03)"],
      ["1. " + PKT_E + ", xoá PKT-03", "2. " + M + ", tìm \"HDM-T1\"", "3. Lọc Trạng thái Đã hạch toán"],
      "-",
      ["- HRM hiện đúng dữ liệu ERP để lại: G1 ô tick khoá, Phiếu kế toán trống, badge \"Chưa hạch toán\"; vẫn ra khi lọc "
       "Đã hạch toán",
       "- Hiện tượng ERP (K13): ERP xoá phiếu không trả dòng về; không ghi lỗi HRM",
       "- Muốn hạch toán lại phải nhờ quản trị trả trạng thái dòng; ghi Ghi chú"]),
    T("015", "Hủy phiếu kế toán trên ERP không gỡ dòng", "P1",
      ["G5 hạch toán bằng PKT-04 Đang tạo (lập ở HRM)"],
      ["1. " + PKT_E + ", Hủy PKT-04", "2. " + M + ", xem G5"],
      "-",
      ["- G5: Phiếu kế toán PKT-04, Trạng thái \"Hủy\" (đỏ), ô tick khoá, không tạo phiếu mới được",
       "- Giống ERP (user chốt 02/11/2026), không ghi lỗi"]),
    T("016", "Duyệt trên ERP phiếu lập ở HRM", "P0",
      ["PKT-05 Đang tạo do TK-KT lập ở HRM cho G6"],
      ["1. " + PKT_E + ", mở PKT-05, duyệt (người duyệt TK-TCT)", "2. " + M + ", xem G6"],
      "-",
      ["- G6: Trạng thái \"Đã duyệt\", Người duyệt TK-TCT",
       "- Lọc Người duyệt TK-TCT ra G3, G6"]),
    T("017", "Hạch toán ở ERP thì HRM cập nhật", "P0",
      ["Dòng mới G7 (HDM-T7, NV-A2, KH-T02, 500 USD, phiếu nhập hoàn thành) Chưa hạch toán"],
      ["1. " + E + ", tick G7, bấm \"Tạo phiếu kế toán\", lưu phiếu trên ERP", "2. " + M + " (TK-KT), tìm \"HDM-T7\""],
      "-",
      ["- HRM: G7 ô tick khoá, Phiếu kế toán = mã ERP vừa lập, Trạng thái theo phiếu",
       "- Lọc Chưa hạch toán không còn G7"]),
    T("018", "Hai người cùng lập phiếu cho 1 dòng trên HRM", "P0",
      ["TK-KT và TK-KT2 cùng mở danh sách; G5 Chưa hạch toán (gỡ phiếu ở TC_07.015 hoặc dùng dòng mới)"],
      ["1. TK-KT tick G5, mở form Tạo phiếu kế toán", "2. TK-KT2 tick G5, mở form", "3. TK-KT Lưu nháp",
       "4. TK-KT2 Lưu nháp"],
      "-",
      ["- Bước 3: \"Thêm mới thành công.\"",
       "- Bước 4: báo \"" + MSG_DOI + "\", form không đóng, KHÔNG tạo phiếu thứ 2",
       "- " + PKT_H + ": chỉ có 1 phiếu của TK-KT gắn G5"]),
    T("019", "Đang mở form HRM thì ERP hạch toán trước", "P0",
      ["Một dòng Chưa hạch toán bất kỳ trong phạm vi TK-KT (ghi mã HĐ mua vào Ghi chú)"],
      ["1. TK-KT trên HRM tick dòng, mở form Tạo phiếu kế toán", "2. TK-KT2 trên ERP tick cùng dòng, lưu phiếu ERP",
       "3. TK-KT bấm Lưu nháp trên HRM"],
      "-",
      ["- HRM báo \"" + MSG_DOI + "\", không tạo phiếu",
       "- Dòng giữ phiếu ERP, không bị ghi đè"]),
    T("020", "HRM lưu trước, ERP lưu sau (hiện tượng ERP)", "P1",
      ["Dòng Chưa hạch toán; TK-KT2 đã mở form tạo phiếu trên ERP cho dòng đó"],
      ["1. TK-KT hạch toán dòng trên HRM (Lưu nháp)", "2. TK-KT2 lưu form ERP đang mở", "3. " + M + ", xem dòng"],
      "-",
      ["- ERP vẫn lưu được (ERP không kiểm - K12), dòng chuyển sang gắn phiếu ERP; phiếu HRM bước 1 còn nhưng không còn "
       "gắn dòng",
       "- Hiện tượng ERP, không ghi lỗi HRM; ghi mã 2 phiếu vào Ghi chú để kế toán xử lý"]),
    T("021", "Danh sách cũ trên HRM, dòng đã được hạch toán ở ERP", "P0",
      ["TK-KT mở danh sách HRM lúc dòng G5 còn Chưa hạch toán, KHÔNG tải lại"],
      ["1. Trên ERP hạch toán G5", "2. Trên HRM (màn cũ) tick G5, bấm Tạo phiếu kế toán", "3. Bấm Lưu nháp"],
      "-",
      ["- Form vẫn mở và nạp G5",
       "- Lưu: báo \"" + MSG_DOI + "\", không tạo phiếu; tải lại danh sách thấy G5 đã hạch toán"]),
    T("022", "Dòng mất điều kiện trong lúc form đang mở", "P1",
      ["G6 Chưa hạch toán"],
      ["1. TK-KT tick G6, mở form", "2. Trên ERP hủy HDM-T6", "3. TK-KT Lưu nháp"],
      "-",
      ["- Báo \"" + MSG_DOI + "\", không tạo phiếu, G6 không bị đánh dấu hạch toán",
       "- Duyệt lại HDM-T6 để các TC sau dùng"]),
    T("023", "Sửa phiếu kế toán Đang tạo không đổi dòng gắn", "P1",
      ["PKT-06 Đang tạo gắn G6 (lập ở HRM)"],
      ["1. " + PKT_H + ", sửa PKT-06: đổi Diễn giải, Lưu nháp", "2. " + M + ", xem G6"],
      "Diễn giải: Sửa thử",
      ["- Báo \"Cập nhật thành công.\", không báo \"" + MSG_DOI + "\"",
       "- G6 vẫn gắn PKT-06, Trạng thái Đang tạo"]),
    T("024", "Bấm Lưu nháp liên tục", "P1",
      ["Form tạo phiếu cho G5 đang mở"],
      ["1. Bấm \"Lưu nháp\" 2 lần thật nhanh"],
      "-",
      ["- Chỉ 1 phiếu được tạo; không có báo \"" + MSG_DOI + "\" ở lần bấm thứ 2 (nút khoá khi đang lưu)"]),
    T("025", "Lưu và tiếp tục không nạp lại dòng vừa hạch toán", "P0",
      ["Form tạo phiếu cho G5 đang mở"],
      ["1. Nhập Ngày hạch toán, bấm \"Lưu và tiếp tục\"", "2. Quan sát form mới"],
      "-",
      ["- Báo \"Thêm mới thành công.\", ở lại màn Tạo phiếu kế toán",
       "- Form mới TRỐNG: không còn ô \"Chi phí vận chuyển nhanh\", không nạp lại G5",
       "- Nếu form nạp lại G5 và lưu ra \"" + MSG_DOI + "\" thì ghi lỗi"]),
    T("026", "Mở form khi chỉ có dòng không hợp lệ", "P2",
      ["G3 đã hạch toán (PKT-T3)"],
      ["1. Trên thanh địa chỉ form Tạo phiếu kế toán đổi danh sách dòng chọn thành G3 (lấy từ đường link ở TC_07.002, "
       "thay mã dòng)", "2. Bấm Lưu nháp"],
      "-",
      ["- Form nạp G3 (như ERP)", "- Lưu: báo \"" + MSG_DOI + "\", không tạo phiếu, G3 vẫn gắn PKT-T3"]),
]

# ================================================================== VIII. PHÂN QUYỀN
S8 = [
    T("001", "Không có quyền nào: vào được màn nhưng không lộ dữ liệu", "P0",
      ["TK-Z không quyền, không chịu phí dòng nào", "Đồng nghiệp gửi đường link màn"],
      ["1. Đăng nhập TK-Z", "2. " + M, "3. Mở đường link được gửi"],
      "-",
      ["- Menu có mục, mở được màn (menu không chặn quyền, giống ERP)",
       "- 0 dòng; không có nút \"Tạo phiếu kế toán\""]),
    T("002", "Không quyền: chỉ thấy dòng mình chịu phí, không tick được", "P0",
      ["NV-A1 không có quyền nào của màn, chịu phí G1, G3, P1"],
      ["1. Đăng nhập NV-A1", "2. " + M, "3. Bấm ô Hạch toán của G1", "4. " + E],
      "-",
      ["- HRM: G1, G3, P1; không có G2, G4, G5, G6",
       "- Ô Hạch toán mọi dòng khoá; không có nút Tạo phiếu kế toán", "- ERP cùng 3 dòng"]),
    T("003", "Quyền Xem theo tổng công ty", "P0",
      ["TK-TCT"],
      ["1. Đăng nhập TK-TCT", "2. " + M, "3. Mở ô Công ty"],
      "-",
      ["- 7 dòng, có G4 (Công ty B)", "- Ô Công ty có mọi công ty"]),
    T("004", "Quyền Xem theo công ty", "P0",
      ["TK-CT (Công ty A, chỉ Xem theo công ty)"],
      ["1. Đăng nhập TK-CT", "2. " + M],
      "-",
      ["- 6 dòng G1, G2, G3, G5, G6, P1; không G4",
       "- Không có nút Tạo phiếu kế toán, ô Hạch toán khoá (thiếu quyền Hạch toán)"]),
    T("005", "Quyền Xem theo phòng ban", "P0",
      ["TK-PB (phòng PB-A1)"],
      ["1. Đăng nhập TK-PB", "2. " + M],
      "-",
      ["- 4 dòng G1, G3, G5, P1 (nhân viên chịu phí thuộc PB-A1)", "- Không có G2, G6 (NV-A2 thuộc PB-A2)"]),
    T("006", "Quyền Xem theo bộ phận", "P0",
      ["TK-BP (bộ phận BP-A1a)"],
      ["1. Đăng nhập TK-BP", "2. " + M],
      "-",
      ["- 3 dòng G1, G3, P1", "- Không có G5 (NV-A3 thuộc BP-A1b)"]),
    T("007", "Nhiều quyền xem: áp quyền rộng nhất", "P1",
      ["TK-PB được gán thêm Xem theo tổng công ty (gỡ sau TC)"],
      ["1. Đăng nhập lại TK-PB", "2. " + M],
      "-",
      ["- 7 dòng (theo tổng công ty), không bị thu hẹp về phòng ban"]),
    T("008", "Quyền Hạch toán chi phí vận chuyển nhanh: hiện nút và tick được", "P0",
      ["TK-KT"],
      ["1. " + M, "2. Tick G5"],
      "-",
      ["- Có nút \"Tạo phiếu kế toán\"", "- Ô Hạch toán dòng Chưa hạch toán tick được; dòng đã hạch toán vẫn khoá"]),
    T("009", "Chỉ có quyền Hạch toán, không có quyền xem", "P1",
      ["NV-A2 được gán Hạch toán chi phí vận chuyển nhanh + Kế toán thanh toán (gỡ sau TC); NV-A2 chịu phí G2, G6"],
      ["1. Đăng nhập NV-A2", "2. " + M, "3. Tick G6, Tạo phiếu kế toán, Lưu nháp"],
      "-",
      ["- Chỉ thấy G2, G6; có nút Tạo phiếu kế toán", "- Lưu được, G6 chuyển Đã hạch toán"]),
    T("010", "Có Hạch toán nhưng thiếu Kế toán thanh toán", "P0",
      ["TK-KTTT0 (Hạch toán + Xem theo công ty, KHÔNG có Kế toán thanh toán); G5 Chưa hạch toán"],
      ["1. Đăng nhập TK-KTTT0", "2. " + M + ", tick G5, " + TAO, "3. Nhập Ngày hạch toán, bấm Lưu nháp"],
      "-",
      ["- Bước 2: nút hiện, form mở và nạp G5",
       "- Bước 3: báo \"" + MSG_KQ_KTTT + "\", không tạo phiếu, G5 vẫn Chưa hạch toán",
       "- Lưu ý: ghi Ghi chú để nghiệp vụ quyết có ẩn nút khi thiếu Kế toán thanh toán (ERP chặn ngay lúc mở form)"]),
    T("011", "Mở đường link form tạo phiếu khi thiếu quyền Hạch toán", "P0",
      ["TK-KT đã sao chép đường link form ở TC_07.002 (G1, P1 Chưa hạch toán)",
       "TK-CT được gán thêm Kế toán thanh toán (gỡ sau TC), KHÔNG có Hạch toán chi phí vận chuyển nhanh"],
      ["1. Đăng nhập TK-CT", "2. Dán đường link form vào thanh địa chỉ, Enter", "3. Nhập Ngày hạch toán, Lưu nháp"],
      "-",
      ["- Form nạp G1, P1 (giống ERP)",
       "- Lưu: báo \"" + MSG_KQ_HT + "\", không tạo phiếu",
       "- Danh sách: G1, P1 vẫn Chưa hạch toán"]),
    T("012", "Bị gỡ quyền Hạch toán khi đang mở form", "P0",
      ["TK-KT đang mở form tạo phiếu cho G5"],
      ["1. Quản trị gỡ quyền Hạch toán chi phí vận chuyển nhanh của TK-KT", "2. TK-KT bấm Lưu nháp",
       "3. TK-KT tải lại danh sách"],
      "-",
      ["- Bước 2: báo \"" + MSG_KQ_HT + "\", không tạo phiếu",
       "- Bước 3: không còn nút Tạo phiếu kế toán, ô Hạch toán khoá"]),
    T("013", "Bị gỡ quyền xem khi đang dùng", "P1",
      ["TK-PB đang xem 4 dòng"],
      ["1. Quản trị gỡ Xem theo phòng ban của TK-PB", "2. TK-PB tải lại màn"],
      "-",
      ["- Chỉ còn dòng TK-PB chịu phí (0 dòng ở bộ mẫu)", "- Xuất Excel cũng theo phạm vi mới"]),
    T("014", "Gán quyền ở ERP có hiệu lực ở HRM", "P1",
      ["TK-Z chưa có quyền"],
      ["1. Trên ERP màn phân quyền gán TK-Z quyền Hạch toán chi phí vận chuyển nhanh - Xem theo công ty",
       "2. TK-Z đăng nhập lại HRM, " + M],
      "-",
      ["- HRM thấy 6 dòng Công ty A (cùng tên quyền dùng chung 2 hệ thống)", "- Gỡ quyền sau TC"]),
    T("015", "Người xem chưa gắn phòng ban mà có quyền theo phòng ban", "P2",
      ["TK-PB0: có Xem theo phòng ban nhưng hồ sơ chưa gắn phòng ban"],
      ["1. Đăng nhập TK-PB0", "2. " + M],
      "-",
      ["- 0 dòng, màn không lỗi (không lộ dòng của người chưa gắn phòng ban khác)"]),
    T("016", "Lọc phòng ban khác khi chỉ có quyền phòng ban", "P1",
      ["TK-PB (PB-A1)"],
      ["1. " + LOC + ", mở ô Phòng ban", "2. Nếu có PB-A2 thì chọn"],
      "Phòng ban: PB-A2",
      ["- Không hiện dòng của PB-A2 (G2, G6) dù chọn được; kết quả 0 dòng",
       "- Lưu ý: ghi vào Ghi chú nếu ô Phòng ban liệt kê phòng ngoài phạm vi"]),
    T("017", "Super Admin", "P1",
      ["TK-SA thuộc nhóm Super Admin, không gán quyền lẻ"],
      ["1. Đăng nhập TK-SA", "2. " + M],
      "-",
      ["- 7 dòng, có nút Tạo phiếu kế toán, tick được dòng Chưa hạch toán"]),
]

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", S1),
    ("II", "TÌM KIẾM & LỌC DANH SÁCH", S2),
    ("III", "SỐ LIỆU BÁO CÁO - DỮ LIỆU NGUỒN VÀ ĐỐI CHIẾU HỆ THỐNG CŨ - HỆ THỐNG MỚI", S3),
    ("IV", "XEM CHI TIẾT CHỨNG TỪ LIÊN KẾT", S4),
    ("V", "TÙY CHỈNH CỘT", S5),
    ("VI", "XUẤT DANH SÁCH EXCEL", S6),
    ("VII", "RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC - HẠCH TOÁN (TẠO PHIẾU KẾ TOÁN) VÀ THAO TÁC ĐỒNG THỜI", S7),
    ("VIII", "PHÂN QUYỀN", S8),
]

DINH_NGHIA = L(
    "Quy ước gọi tên trong tài liệu:",
    "- \"Hệ thống cũ\" = phần mềm ERP đang chạy song song.",
    "- \"Hệ thống mới\" = HRM.",
    "- 2 hệ thống dùng CHUNG dữ liệu.",
)
DESCRIPTION_BLOCK = [(label, (DINH_NGHIA + "\n" + X(body)) if label.startswith("1.") else X(body))
                     for label, body in DESCRIPTION_BLOCK]

if __name__ == "__main__":
    build_chuan(output_file=os.path.join(HERE, "testcase - Danh sach can hach toan chi phi van chuyen nhanh.xlsx"),
                sheet_name="Trang tính1",
                feature_name=TEN + " - Cập nhật ngày " + NGAY,
                module_name=MODULE,
                description_block=DESCRIPTION_BLOCK, sections=SECTIONS, loai="bao_cao")
