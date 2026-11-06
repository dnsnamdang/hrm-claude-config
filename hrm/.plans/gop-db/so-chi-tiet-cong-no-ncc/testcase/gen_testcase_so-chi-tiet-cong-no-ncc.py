# -*- coding: utf-8 -*-
"""Testcase man "So chi tiet cong no phai tra nha cung cap" (HRM: phan he Tai chinh > Ke toan cong no > Nha cung cap;
port ERP Ke toan > Ke toan Cong no > Nha cung cap). Kieu doi chieu cheo ERP - HRM (2 he thong dung CHUNG du lieu).

Nguon da doc (06/11/2026):
  - Spec: docs/superpowers/specs/gop-db/2026-11-04-so-chi-tiet-cong-no-ncc-design.md;
    .plans/gop-db/so-chi-tiet-cong-no-ncc/{design,plan}.md
  - HRM FE: hrm-client/pages/finance/supplier-debt-details/{index.vue, components/constants.js},
    components/subsystem-menu/finance.js (425-440), components/V2BaseSmartFilterPanel.vue, V2BaseSelectRemote.vue,
    utils/{filterRequiredErrors.js, invoiceable-link.js, contract-link.js, export/listExportFile.js},
    utils/mixins/{filterStateMixin.js, reportPrintPreviewMixin.js}, plugins/axios.js
  - HRM BE: Modules/Finance/Http/Controllers/V1/SupplierDebtDetailController.php,
    Controllers/V1/Concerns/ValidatesAccountDebtFilters.php, Services/SupplierDebt/SupplierDebtDetailService.php,
    Services/AccountDebt/AccountLedgerService.php, Services/AccountDebt/Concerns/AccountDebtCommon.php,
    Routes/api.php (1959-1967), Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php (2038-2041);
    nguon ghi so: DeclareDebt/DeclareDebtPostingService.php, BillPaymentApprovalFlowService.php,
    BillAdjustDeptWriteService.php, BuyServiceAccountingService.php, DomesticPurchaseProductImportAccountingService.php
  - ERP: TanPhatDev app/Http/Controllers/Accounting/AccountDetailController.php (index 30-60, searchData 63-100,
    supplierExport 601-668), app/Model/Accounting/AccountDetail.php (searchByFilter 448-585, getInvoiceableLinkAttribute 2130),
    views accounting/account_details/{index.blade.php, account_detail_table.blade.php},
    layouts/topmenubar.blade.php (1163-1181), routes/web.php 5079-5086
  - Mau: .plans/gop-db/hach-toan-cpvc-nhanh/testcase/gen_testcase_hach-toan-cpvc-nhanh.py,
    .plans/gop-db/finance-declare-debt-beginning/testcase/gen_testcase_cong-no-dau-ky-kh-hd.py
Khuon: build_chuan (tab "13. DM quoc gia", chot 03/11/2026), loai bao_cao.
Chay: PYTHONIOENCODING=utf-8 python3 gen_testcase_so-chi-tiet-cong-no-ncc.py
"""
import os
import re
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", "..", ".claude", "skills", "testcase-documenter", "assets"))
from tc_chuan import build_chuan  # noqa: E402

NGAY = "06/11/2026"
TEN = "Sổ chi tiết công nợ phải trả nhà cung cấp"
MODULE = "Sổ chi tiết công nợ phải trả NCC"


def L(*lines):
    return "\n".join(lines)


def X(s):
    """ERP -> "hệ thống cũ", HRM -> "hệ thống mới"; viết hoa khi đứng đầu ý / đầu câu."""
    s = s.replace("ERP - HRM", "hệ thống cũ - hệ thống mới")
    s = re.sub(r"\bERP\b", "hệ thống cũ", s)
    s = re.sub(r"\bHRM\b", "hệ thống mới", s)
    s = re.sub(r"(^|\n|^- |\n- |\n  |\d\. |[.:;] |\()(hệ thống)", lambda m: m.group(1) + "Hệ thống", s)
    return s


def T(n, func, prio, pre, steps, data, exp):
    def j(x):
        return X(x if isinstance(x, str) else L(*x))
    return (n, X(func), prio, j(pre), j(steps), j(data), j(exp))


# ------------------------------------------------------------------ đường bấm / câu cố định
M = ('HRM: vào phân hệ Tài chính > nhóm "Kế toán công nợ" > "Nhà cung cấp" > bấm "Sổ chi tiết công nợ phải trả nhà '
     'cung cấp"')
E = ('ERP: menu Kế toán > "Kế toán Công nợ" > nhóm "Nhà cung cấp" > bấm "Sổ chi tiết công nợ phải trả nhà cung cấp"')
LOC = "chọn bộ lọc chuẩn F0 rồi bấm Tìm kiếm"
LOC_C = "Chọn bộ lọc chuẩn F0 rồi bấm Tìm kiếm"
LOC_E = "chọn cùng bộ lọc trên ERP (2 ô Từ ngày / Đến ngày) rồi bấm nút Tìm (kính lúp)"
PC_H = 'HRM: phân hệ Tài chính > nhóm "Quản lý tiền" > "Thanh toán tiền mặt" > bấm "Phiếu chi"'
UNC_H = 'HRM: phân hệ Tài chính > nhóm "Quản lý tiền" > "Thanh toán tiền mặt" > bấm "Phiếu ủy nhiệm chi"'
PKT_H = 'HRM: phân hệ Tài chính > nhóm "Sổ tổng hợp" > bấm "Phiếu kế toán"'
PNH_H = 'HRM: phân hệ Tài chính > nhóm "Hàng hoá - Dịch vụ - Vận chuyển" > "Nhập hàng" > bấm "Phiếu nhập hàng"'
HTDV_H = ('HRM: phân hệ Tài chính > nhóm "Hàng hoá - Dịch vụ - Vận chuyển" > "Mua dịch vụ" > bấm "Hạch toán mua dịch '
          'vụ"')
KB_H = 'HRM: phân hệ Tài chính > nhóm "Khai báo đầu kỳ" > bấm "Khai báo đầu kỳ công nợ nhà cung cấp"'
SOTK_E = 'ERP: menu Kế toán > "Sổ tổng hợp" > bấm "Sổ chi tiết các tài khoản"'

MSG_TK = "Vui lòng chọn tài khoản"
MSG_NCC = "Vui lòng chọn nhà cung cấp"
MSG_TG = "Vui lòng chọn thời gian"
MSG_THIEU = "Vui lòng chọn tài khoản, nhà cung cấp và thời gian"
MSG_CHO = "Chọn tài khoản, nhà cung cấp và thời gian để xem sổ chi tiết."
MSG_RONG = "Không có dữ liệu phù hợp bộ lọc."
MSG_KQ = "Bạn không có quyền thực hiện thao tác này"
MSG_XLS_OK = "Xuất Excel thành công"
MSG_XLS_RONG = "Không có dữ liệu để xuất"
TIEU_DE_IN = "SỔ CHI TIẾT CÔNG NỢ PHẢI TRẢ NHÀ CUNG CẤP"
P_ALL = "Xem sổ chi tiết công nợ phải trả nhà cung cấp theo tổng công ty"
P_CT = "Xem sổ chi tiết công nợ phải trả nhà cung cấp theo công ty"

# ------------------------------------------------------------------ số liệu mẫu
# NCC-T01, TK 331, VNĐ, kỳ 01/11-30/11/2026.
# Trước kỳ: KB1 Có 50,000,000 (A, HDM-T01) | PKT-T0 20/10 Nợ 12,000,000 (A, HDM-T01, Có 1121) | PKT-B0 25/10 Nợ 3,000,000 (B)
# Trong kỳ: D1 03/11 Có 22,000,000 (3311, HDM-T02) | D2 05/11 Có 8,800,000 (HDV-T01) | D3 10/11 Nợ 15,000,000 (PC, HDM-T01)
#           D4 12/11 Nợ 25,000,000 (UNC, HDM-T02, 1121) | B1 14/11 Nợ 6,000,000 (B, HDM-B1) | B2 16/11 Nợ 4,000,000 (B, HDM-B2 do TK-CT lập)
#           D5 30/11 Nợ 1,500,000 (PKT, HDM-T02, Có 711)
# TK-KT : đầu Có 38,000,000 | Nợ 41,500,000 | Có 30,800,000 | cuối Có 27,300,000 | 5 bút toán
# TK-CT : đầu Có 38,000,000 | Nợ 45,500,000 | Có 30,800,000 | cuối Có 23,300,000 | 6
# TK-TCT: đầu Có 35,000,000 | Nợ 51,500,000 | Có 30,800,000 | cuối Có 14,300,000 | 7
# TK-CTB: đầu Nợ 3,000,000  | Nợ 10,000,000 | Có trống     | cuối Nợ 13,000,000 | 2

F0 = "Tài khoản 331, Nhà cung cấp NCC-T01, Thời gian 01/11/2026 - 30/11/2026, Loại tiền VNĐ"
KQ_KT = ["- Số dư đầu kỳ: cột Phát sinh có 38,000,000; cột Phát sinh nợ trống",
         "- Tổng phát sinh: Phát sinh nợ 41,500,000; Phát sinh có 30,800,000",
         "- Số dư cuối kỳ: cột Phát sinh có 27,300,000; cột Phát sinh nợ trống"]

DU_LIEU = L(
    "Dữ liệu mẫu dùng xuyên suốt (hệ thống tự sinh mã chứng từ thì ghi mã thật vào cột Ghi chú của TC đầu tiên dùng nó):",
    "- Công ty A (phòng Mua hàng, phòng Xuất nhập khẩu), Công ty B. Ngày tính công nợ đầu kỳ trong cấu hình hệ thống là "
    "một ngày TRƯỚC 01/11/2026.",
    "- Nhà cung cấp (danh mục khách hàng, đánh dấu là nhà cung cấp): NCC-T01 Công ty TNHH Thiết bị Minh An; NCC-T02 "
    "Công ty CP Vật tư Hoàng Long; NCC-T03 Global Parts Co., Ltd (nước ngoài).",
    "- Người lập hợp đồng: NV-MH1 (Công ty A, phòng Mua hàng) lập HĐ mua HDM-T01 và HĐ mua dịch vụ HDV-T01; NV-MH2 "
    "(Công ty A, phòng Xuất nhập khẩu) lập HDM-T02 và HĐ nhập khẩu HDM-NK1; NV-B1 (Công ty B) lập HDM-B1; HDM-B2 của "
    "Công ty B do TK-CT lập.",
    "- Tiền tệ: VNĐ; USD tỷ giá 25,350; EURO tỷ giá 27,850. Tài khoản 331 có tài khoản con trực tiếp 3311.",
    "- Tài khoản đăng nhập (đều KHÔNG phải Super Admin, đăng nhập được cả ERP và HRM):",
    "  TK-TCT: Công ty A, quyền \"" + P_ALL + "\".",
    "  TK-KT: Công ty A, quyền \"" + P_CT + "\", không lập hợp đồng nào.",
    "  TK-CT: Công ty A, quyền \"" + P_CT + "\", là người lập HDM-B2 (Công ty B).",
    "  TK-CTB: Công ty B, quyền \"" + P_CT + "\". TK-2Q: Công ty A, có CẢ 2 quyền.",
    "  TK-Z: không có quyền nào của màn. TK-SA: Super Admin.",
    "- Bút toán TRƯỚC kỳ của NCC-T01 trên TK 331 (VNĐ):",
    "  KB1: Khai báo đầu kỳ công nợ NCC, HĐ HDM-T01, Dư có 50,000,000 (ghi sổ ở ngày tính công nợ đầu kỳ).",
    "  PKT-T0: Phiếu kế toán ngày hạch toán 20/10/2026, Nợ 331 / Có 1121, 12,000,000, HDM-T01, Lưu và duyệt.",
    "  PKT-B0: Phiếu kế toán Công ty B ngày 25/10/2026, Nợ 331 / Có 1121, 3,000,000, HDM-B1.",
    "- Bút toán TRONG kỳ 01/11/2026 - 30/11/2026 (đã ghi sổ):",
    "  D1: Phiếu nhập hàng mua trong nước PNH-T02 theo HDM-T02, 03/11/2026, hàng 20,000,000 + thuế 2,000,000: Có 3311 "
    "22,000,000 (đối ứng 1541, 1331), ghi chú phiếu \"Nhập hàng đợt 1\".",
    "  D2: Hạch toán mua dịch vụ HTDV-T01 theo HDV-T01, 05/11/2026, 8,000,000 + thuế 800,000: Có 331 8,800,000 (đối "
    "ứng tài khoản chi phí trên phiếu và 1331).",
    "  D3: Phiếu chi PC-T01 trả NCC-T01 theo HDM-T01, thủ quỹ duyệt 10/11/2026: Nợ 331 15,000,000 (đối ứng 1111).",
    "  D4: Phiếu ủy nhiệm chi UNC-T01 theo HDM-T02, duyệt 12/11/2026: Nợ 331 25,000,000 (đối ứng 1121), ghi chú phiếu "
    "\"Thanh toán đợt 1 HDM-T02\".",
    "  B1: Phiếu chi PC-B1 Công ty B theo HDM-B1, 14/11/2026: Nợ 331 6,000,000.",
    "  B2: Phiếu kế toán PKT-B2 Công ty B theo HDM-B2, 16/11/2026: Nợ 331 / Có 1121, 4,000,000.",
    "  D5: Phiếu kế toán PKT-T1 theo HDM-T02, 30/11/2026: Nợ 331 / Có 711, 1,500,000 (chiết khấu NCC).",
    "  F0: Phiếu kế toán PKT-F0 NCC-T01 bằng USD, 07/11/2026: Có 331 1,000 USD, tỷ giá 25,350 (25,350,000).",
    "- KHÔNG được lên sổ: N1 phiếu kế toán PKT-N1 Đang tạo (Nợ 331 3,000,000, 15/11); N2 phiếu chi PC-N2 7,000,000 còn "
    "chờ thủ quỹ duyệt; N3 phiếu kế toán PKT-N3 ngày 01/12/2026 Nợ 331 2,000,000 (sau kỳ); N5 phiếu chi PC-N5 9,000,000 "
    "của NCC-T02.",
    "- Ngoại tệ NCC-T03 (Công ty A): KB2 khai báo đầu kỳ HDM-NK1 Dư có 10,000 USD tỷ giá 25,350 (253,500,000); PKT-F1 "
    "06/11 Có 331 2,000 USD tỷ giá 25,350 (50,700,000); PKT-F2 09/11 Có 331 1,000 EURO tỷ giá 27,850 (27,850,000); "
    "UNC-F1 13/11 Nợ 331 5,000 USD tỷ giá 25,450 (127,250,000).",
    "- Kết quả bộ mẫu, bộ lọc F0 = " + F0 + ":",
    "  TK-KT 5 bút toán (D1, D2, D3, D4, D5): đầu kỳ Có 38,000,000; phát sinh Nợ 41,500,000 / Có 30,800,000; cuối kỳ "
    "Có 27,300,000.",
    "  TK-CT 6 (thêm B2): đầu kỳ Có 38,000,000; Nợ 45,500,000 / Có 30,800,000; cuối kỳ Có 23,300,000.",
    "  TK-TCT 7 (thêm B1, B2): đầu kỳ Có 35,000,000; Nợ 51,500,000 / Có 30,800,000; cuối kỳ Có 14,300,000.",
    "  TK-CTB 2 (B1, B2): đầu kỳ Nợ 3,000,000; Nợ 10,000,000; cuối kỳ Nợ 13,000,000.",
    "- Môi trường có sẵn dữ liệu thật của NCC-T01 thì lấy kết quả bộ mẫu cộng thêm phần thật; đối chiếu bằng cùng tài "
    "khoản, cùng bộ lọc trên ERP.",
)

DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng", L(
        "Màn HRM \"" + TEN + "\" (chuyển từ ERP) cho kế toán xem từng bút toán công nợ của MỘT nhà cung cấp trên một tài "
        "khoản theo dõi công nợ (331…) trong một khoảng thời gian: số dư đầu kỳ, từng chứng từ phát sinh Nợ / Có, tổng "
        "phát sinh, số dư cuối kỳ. Màn CHỈ ĐỌC; có In (ERP không có) và Xuất Excel.",
        "ERP và HRM dùng CHUNG sổ kế toán: chứng từ ghi sổ ở hệ thống nào thì sổ ở cả 2 hệ thống đều thấy ngay. Chứng từ "
        "lập được ở cả 2 hệ thống: phiếu chi, phiếu ủy nhiệm chi, phiếu kế toán, phiếu nhập hàng, hạch toán mua dịch vụ, "
        "khai báo đầu kỳ công nợ nhà cung cấp. Hợp đồng mua chỉ lập ở ERP.",
        "Lối vào HRM: 1 mục menu (phân hệ Tài chính > Kế toán công nợ > Nhà cung cấp). ERP: 1 mục (Kế toán > Kế toán "
        "Công nợ > Nhà cung cấp).",
        DU_LIEU,
    )),
    ("2. Đối tượng được tính / hiển thị", L(
        "Một bút toán LÊN sổ khi đủ các điều kiện:",
        "- Đã ghi sổ kế toán: phiếu chi / ủy nhiệm chi đã duyệt chi; phiếu kế toán Đã duyệt (Lưu và duyệt); phiếu nhập "
        "hàng đã hạch toán; hạch toán mua dịch vụ đã duyệt; khai báo đầu kỳ ghi sổ ngay khi Lưu.",
        "- Thuộc tài khoản đã chọn HOẶC tài khoản con TRỰC TIẾP của nó (chọn 331 thì có cả 3311; không lấy cấp cháu).",
        "- Đối tượng là nhà cung cấp đã chọn (ghi ở vế nhà cung cấp HOẶC vế khách hàng của bút toán - giống ERP).",
        "- Ngày hạch toán nằm trong khoảng Thời gian (từ 00:00 ngày đầu đến 23:59:59 ngày cuối). Bút toán TRƯỚC ngày đầu "
        "dồn vào Số dư đầu kỳ.",
        "- Loại tiền: VNĐ chỉ lấy bút toán bằng VNĐ; Ngoại tệ lấy mọi bút toán khác VNĐ.",
        "- Khớp mọi ô lọc khác (mục 4, 9) và trong phạm vi quyền (mục 7).",
    )),
    ("3. Đối tượng bị ẩn / không tính", L(
        "- Chứng từ chưa ghi sổ: phiếu kế toán Đang tạo (N1), phiếu chi chưa duyệt chi (N2), phiếu chưa hạch toán.",
        "- Ngày hạch toán SAU Đến ngày (N3): không lên, cũng KHÔNG vào đầu kỳ.",
        "- Nhà cung cấp khác (N5); tài khoản khác ngoài tài khoản chọn và con trực tiếp; sai loại tiền.",
        "- Ngoài phạm vi quyền: người có quyền theo công ty không thấy bút toán của công ty khác, TRỪ hợp đồng do chính "
        "mình lập. Phạm vi áp cho cả Số dư đầu kỳ.",
        "- Thiếu 1 trong 4 ô bắt buộc (Tài khoản, Nhà cung cấp, Thời gian): không tải gì.",
    )),
    ("4. Bộ lọc thời gian áp dụng cho", L(
        "Ô \"Thời gian\" (1 ô chọn khoảng ngày, BẮT BUỘC) lọc theo NGÀY HẠCH TOÁN ghi trên sổ của từng bút toán, tính "
        "trọn ngày (00:00:00 ngày đầu đến 23:59:59 ngày cuối).",
        "Số dư đầu kỳ = tổng Nợ trừ tổng Có của các bút toán có ngày hạch toán TRƯỚC ngày đầu, cùng mọi ô lọc khác.",
        "Phiếu chi / ủy nhiệm chi: ngày hạch toán = ngày duyệt chi. Khai báo đầu kỳ: ngày tính công nợ đầu kỳ trong cấu "
        "hình. Lập bộ mẫu vào ngày khác thì đổi ngày tương ứng, giữ đúng thứ tự trước kỳ / trong kỳ / sau kỳ.",
    )),
    ("5. Cấu trúc dữ liệu / cây phân cấp", L(
        "Bộ lọc (khung \"Bộ lọc danh sách\", nút \"Tìm kiếm nâng cao\" / \"Ẩn tìm kiếm nâng cao\"): ô tìm nhanh \"Tìm "
        "theo số chứng từ hoặc số hợp đồng\", nút Tìm kiếm, Làm mới; Công ty (chỉ người có quyền theo tổng công ty), Tài "
        "khoản (*), Nhà cung cấp (*), Thời gian (*), Tài khoản đối ứng, Đơn hàng/Hợp đồng, Số chứng từ, Nhân viên, Loại "
        "tiền (VNĐ mặc định / Ngoại tệ), Số tiền từ, Số tiền đến.",
        "Thanh công cụ: In, Xuất Excel. Không có cấu hình cột, không sắp xếp theo cột.",
        "Bảng mẫu VNĐ (11 cột): STT, Đơn hàng/Hợp đồng (link), Ngày hạch toán, Số chứng từ (link), Nhân viên, Phòng ban, "
        "Ghi chú, Phát sinh nợ, Phát sinh có, nhóm \"Tài khoản đối ứng\" gồm Tài khoản và Tên tài khoản.",
        "Bảng mẫu Ngoại tệ (15 cột): 7 cột đầu như trên, Loại tiền, nhóm \"Số phát sinh ngoại tệ\" (Nợ, Có), Tỷ giá, "
        "nhóm \"Số phát sinh VNĐ\" (Nợ, Có), nhóm Tài khoản đối ứng.",
        "Dòng tổng nằm ĐẦU bảng, nền xám, nhãn căn phải gộp 7 cột đầu: Số dư đầu kỳ, Tổng phát sinh, Số dư cuối kỳ "
        "(Ngoại tệ: 3 dòng này cho TỪNG loại tiền).",
        "Nhân viên = người lập hợp đồng của bút toán; Phòng ban = phòng ban người đó. Ghi chú = ghi chú của chứng từ "
        "(chỉ phiếu nhập hàng, phiếu xuất, phiếu thu, phiếu báo có, ủy nhiệm chi có; phiếu chi, phiếu kế toán để trống).",
    )),
    ("6. Quy tắc cộng dồn / deduplicate", L(
        "- 1 dòng = 1 bút toán trên sổ (1 chứng từ ghi nhiều bút toán vào 331 thì ra nhiều dòng).",
        "- Thứ tự: ngày hạch toán tăng dần, cùng ngày thì bút toán ghi trước đứng trước.",
        "- Tài khoản đối ứng: 1 bút toán có nhiều tài khoản đối ứng thì liệt kê cách nhau dấu phẩy, không lặp.",
        "- Số dư đầu kỳ, tổng phát sinh, số dư cuối kỳ tính trên TOÀN BỘ kết quả lọc, không phụ thuộc trang đang xem.",
        "- Số dư cuối kỳ = Số dư đầu kỳ + Tổng phát sinh nợ - Tổng phát sinh có (làm tròn 2 số lẻ).",
    )),
    ("7. Phân quyền cấp", L(
        "Tên quyền nguyên văn (nhóm \"Sổ chi tiết công nợ phải trả nhà cung cấp\"), dùng chung tên với ERP:",
        "- " + P_ALL + ": xem sổ mọi công ty; có thêm ô lọc Công ty.",
        "- " + P_CT + ": xem bút toán của công ty mình HOẶC bút toán thuộc hợp đồng do chính mình lập (kể cả của công "
        "ty khác). Không có ô Công ty.",
        "- Có cả 2 quyền: lấy quyền rộng hơn (tổng công ty). Super Admin có mọi quyền.",
        "- Không có quyền nào: menu ẨN; mở đường link màn thì hệ thống báo \"" + MSG_KQ + "\", không hiện số liệu, "
        "không In / Xuất Excel được.",
        "Lưu ý: menu hiện theo quyền gán qua VAI TRÒ. Quyền tra theo TÊN nên gán ở ERP hay HRM đều có hiệu lực ở cả 2.",
    )),
    ("8. Cách tính các ô thống kê", L(
        "- Dòng bút toán mẫu VNĐ: Phát sinh nợ / Phát sinh có = số tiền VNĐ của bút toán ở đúng phía Nợ hoặc Có.",
        "- Mẫu Ngoại tệ: Số phát sinh ngoại tệ Nợ / Có = số nguyên tệ; Tỷ giá; Số phát sinh VNĐ = số quy đổi.",
        "- Số dư đầu kỳ / cuối kỳ: số dương (dư Nợ) hiện ở cột Nợ, số âm (dư Có) hiện giá trị tuyệt đối ở cột Có; bằng 0 "
        "thì để trống. Tổng phát sinh hiện tổng Nợ và tổng Có riêng (không bù trừ).",
        "- Ngoại tệ: mỗi loại tiền có 3 dòng Số dư đầu kỳ / Tổng phát sinh / Số dư cuối kỳ, có cả nguyên tệ và VNĐ quy "
        "đổi của RIÊNG loại tiền đó (USD 3 dòng, EURO 3 dòng); không có dòng gộp các loại tiền.",
        "- Ví dụ TK-KT bộ lọc F0: đầu kỳ = 12,000,000 - 50,000,000 = -38,000,000 (Có 38,000,000); Nợ = 15,000,000 + "
        "25,000,000 + 1,500,000 = 41,500,000; Có = 22,000,000 + 8,800,000 = 30,800,000; cuối = -38,000,000 + 41,500,000 - "
        "30,800,000 = -27,300,000 (Có 27,300,000).",
        "- Ô \"Hiển thị a–b / N bút toán\" dưới bảng: a, b là STT dòng đầu / cuối trang; N là tổng số bút toán khớp lọc.",
    )),
    ("9. Ghi chú đọc bảng", L(
        "- Số theo chuẩn quốc tế (phẩy ngăn nghìn, chấm thập phân, tối đa 2 số lẻ). Ô rỗng / dòng tổng bằng 0 để TRỐNG.",
        "- Mở màn chưa tải gì, bảng ghi \"" + MSG_CHO + "\". Đủ 3 ô bắt buộc thì chọn ô chọn nào cũng tự tải lại; ô gõ "
        "tay (tìm nhanh, Đơn hàng/Hợp đồng, Số chứng từ, Số tiền) phải bấm Tìm kiếm / Enter.",
        "- Mọi ô lọc (cả ô tìm nhanh, Số tiền, Nhân viên, Hợp đồng) áp CẢ cho Số dư đầu kỳ: đổi lọc thì đầu kỳ đổi theo, "
        "luôn giữ đầu kỳ + phát sinh = cuối kỳ.",
        "- Đơn hàng/Hợp đồng so khớp CHÍNH XÁC cả mã; Số chứng từ và ô tìm nhanh tìm theo một phần mã.",
        "- Số tiền từ / đến so với số VNĐ của TỪNG bút toán (kể cả mẫu Ngoại tệ); để trống hoặc 0 là không lọc.",
        "- Phân trang 10 bút toán / trang (chọn 10, 20, 50, 100); STT liên tục qua trang; dòng tổng giữ nguyên khi đổi trang.",
        "- Chuyển trang, In, Xuất Excel dùng bộ lọc ĐÃ ÁP lần tải gần nhất (ô gõ dở chưa bấm Tìm kiếm không được tính).",
        "- Bộ lọc được nhớ 10 phút; tải lại trang (F5) hoặc chuyển sang màn khác là xoá bộ lọc.",
        "KHÁC BIỆT ĐÃ CHỐT ERP - HRM (gặp thì ghi \"khác biệt đã chốt, không ghi lỗi\"):",
        "- K1. ERP dòng tổng ở CUỐI bảng, 4 dòng (Số dư đầu kỳ, Tổng phát sinh nợ, Tổng phát sinh có, Số dư cuối kỳ); HRM ở "
        "ĐẦU bảng, 3 dòng (Tổng phát sinh có cả Nợ và Có trên 1 dòng). Số liệu phải bằng nhau.",
        "- K2. ERP không phân trang (tải hết, STT 1..N); HRM 10 / trang, tổng tính trên toàn bộ kết quả.",
        "- K3. ERP ô rỗng in \"-\"; HRM để trống. ERP cột Ghi chú trên màn luôn trống; HRM hiện ghi chú chứng từ.",
        "- K4. Ngày hạch toán: ERP lấy ngày trên CHỨNG TỪ (có thể là ngày lập / ngày duyệt, nằm ngoài khoảng lọc); HRM lấy "
        "ngày ghi sổ, luôn nằm trong khoảng lọc.",
        "- K5. Số dư đầu kỳ: HRM dùng ĐÚNG bộ lọc của danh sách (nhà cung cấp ở cả 2 vế, hợp đồng khớp chính xác, mọi ô "
        "lọc) nên luôn đầu kỳ + phát sinh = cuối kỳ. ERP đầu kỳ chỉ lọc vế nhà cung cấp và hợp đồng theo một phần mã nên "
        "có thể lệch (HRM sửa lỗi, user chốt 04/11/2026).",
        "- K6. Ngoại tệ: HRM tách đầu kỳ / phát sinh / cuối kỳ theo TỪNG loại tiền; ERP cộng lẫn nguyên tệ mọi loại tiền vào "
        "1 số đầu kỳ / cuối kỳ (USD cộng EURO), chỉ tổng phát sinh tách theo loại tiền.",
        "- K7. ERP lọc Tài khoản đối ứng báo \"Đã có lỗi xảy ra\" và ô đó chỉ liệt kê tài khoản theo dõi công nợ; HRM lọc "
        "được, liệt kê mọi tài khoản đang dùng.",
        "- K8. Làm mới: ERP xoá trắng cả Loại tiền (tiêu đề chuyển sang mẫu ngoại tệ); HRM về VNĐ.",
        "- K9. HRM thêm: ô tìm nhanh, 1 ô Thời gian thay 2 ô, tự tải khi đổi ô chọn, Nhà cung cấp tìm theo mã / tên (gõ từ 1 "
        "ký tự, tối đa 20 kết quả), nút In. Báo thiếu ô: ERP chữ đỏ \"Bắt buộc chọn\" + \"Chưa chọn đủ điều kiện bắt buộc\"; "
        "HRM chữ đỏ \"" + MSG_TK + "\" / \"" + MSG_NCC + "\" / \"" + MSG_TG + "\".",
        "- K10. Excel: ERP file cong_no_ncc.xlsx, không STT, cột nhân viên ghi NVKD, dòng tổng ở cuối, ngày kèm giờ, chỉ 2 "
        "cột định dạng số, đầu kỳ KHÔNG áp phạm vi công ty, mẫu ngoại tệ lỗi đầu kỳ. HRM file so_chi_tiet_cong_no_ncc.xlsx "
        "sửa hết.",
        "- K11. Không quyền: ERP hiện trang không tìm thấy; HRM ẩn menu, mở đường link thì báo không có quyền.",
        "- K12. Link Số chứng từ / Hợp đồng: chứng từ đã có màn HRM mở màn HRM (tab mới); hợp đồng mua mở ERP.",
        "- Lưu ý: 2 hệ thống dùng chung dữ liệu, chạy TC theo thứ tự trong nhóm; TC lập chứng từ mới thì ghi mã vào Ghi chú "
        "và trừ lại ở TC sau nếu chưa xoá.",
    )),
]

# ================================================================== I. HIỂN THỊ TRANG & TRUY CẬP
S1 = [
    T("001", "Mở màn từ menu: bố cục màn", "P0",
      ["TK-KT (quyền theo công ty)"],
      ["1. Đăng nhập HRM bằng TK-KT", "2. " + M],
      "-",
      ["- Tiêu đề tab trình duyệt và tiêu đề bảng: \"" + TEN + "\"",
       "- Khung \"Bộ lọc danh sách\": ô tìm nhanh gợi ý \"Tìm theo số chứng từ hoặc số hợp đồng\", nút Tìm kiếm, Làm mới; "
       "khối nâng cao đang mở: Tài khoản (*), Nhà cung cấp (*), Thời gian (*), Tài khoản đối ứng, Đơn hàng/Hợp đồng, Số "
       "chứng từ, Nhân viên, Loại tiền, Số tiền từ, Số tiền đến",
       "- KHÔNG có ô Công ty (TK-KT chỉ có quyền theo công ty)",
       "- Thanh công cụ theo thứ tự: \"In\", \"Xuất Excel\""]),
    T("002", "Màn chưa tải dữ liệu khi chưa đủ ô bắt buộc", "P0",
      ["TK-KT", "Bộ lọc chưa chọn gì"],
      ["1. " + M, "2. Quan sát bảng, chưa bấm gì"],
      "-",
      ["- Bảng ghi \"" + MSG_CHO + "\"",
       "- Không có dòng tổng, không có thanh phân trang",
       "- Không có chữ đỏ dưới ô nào (chưa bấm Tìm kiếm)"]),
    T("003", "Tiêu đề cột mẫu VNĐ", "P0",
      ["TK-KT", "Bộ mẫu mục 1"],
      ["1. " + M, "2. " + LOC, "3. Đọc 2 dòng tiêu đề bảng"],
      F0,
      ["- Theo thứ tự: STT, Đơn hàng/Hợp đồng, Ngày hạch toán, Số chứng từ, Nhân viên, Phòng ban, Ghi chú, Phát sinh nợ, "
       "Phát sinh có, nhóm \"Tài khoản đối ứng\" (tầng dưới: Tài khoản, Tên tài khoản)",
       "- Tiêu đề dính trên cùng khi cuộn bảng",
       "- Cùng thứ tự cột như ERP mẫu VNĐ"]),
    T("004", "Tiêu đề cột mẫu Ngoại tệ", "P0",
      ["TK-TCT", "NCC-T03 có bút toán USD, EURO"],
      ["1. " + M, "2. Chọn Tài khoản 331, Nhà cung cấp NCC-T03, Thời gian 01/11/2026 - 30/11/2026, Loại tiền Ngoại tệ"],
      "Loại tiền: Ngoại tệ",
      ["- 7 cột đầu như mẫu VNĐ, sau đó: Loại tiền, nhóm \"Số phát sinh ngoại tệ\" (Nợ, Có), Tỷ giá, nhóm \"Số phát sinh "
       "VNĐ\" (Nợ, Có), nhóm \"Tài khoản đối ứng\" (Tài khoản, Tên tài khoản)",
       "- Đổi lại Loại tiền VNĐ thì bảng tự trở về 11 cột"]),
    T("005", "Đọc sổ sau khi chọn đủ bộ lọc", "P0",
      ["TK-KT", "Bộ mẫu mục 1"],
      ["1. " + M, "2. " + LOC],
      F0,
      ["- 3 dòng tổng ở đầu bảng, nền xám, chữ đậm, nhãn căn phải: \"Số dư đầu kỳ\", \"Tổng phát sinh\", \"Số dư cuối kỳ\""]
      + KQ_KT +
      ["- Dưới dòng tổng: 5 bút toán theo thứ tự D1 (03/11), D2 (05/11), D3 (10/11), D4 (12/11), D5 (30/11)",
       "- Dưới bảng: \"Hiển thị 1–5 / 5 bút toán\""]),
    T("006", "Dòng bút toán: đọc đúng từng cột", "P0",
      ["TK-KT, bộ lọc F0"],
      ["1. " + M + ", " + LOC, "2. Đọc dòng D4 (ủy nhiệm chi UNC-T01) và dòng D3 (phiếu chi PC-T01)"],
      F0,
      ["- D4: Đơn hàng/Hợp đồng HDM-T02; Ngày hạch toán 12/11/2026; Số chứng từ = mã UNC-T01; Nhân viên NV-MH2; Phòng "
       "ban Xuất nhập khẩu; Ghi chú \"Thanh toán đợt 1 HDM-T02\"; Phát sinh nợ 25,000,000; Phát sinh có trống; Tài khoản "
       "1121 kèm tên tài khoản",
       "- D3: HDM-T01; 10/11/2026; mã PC-T01; NV-MH1; Mua hàng; Ghi chú TRỐNG (phiếu chi không có ghi chú trên sổ); Nợ "
       "15,000,000; Tài khoản 1111",
       "- Ngày dạng dd/mm/yyyy, số căn phải"]),
    T("007", "Ô trống để trống, không in dấu gạch", "P1",
      ["TK-KT, bộ lọc F0"],
      ["1. " + M + ", " + LOC, "2. Quan sát ô Phát sinh có của D3, ô Phát sinh nợ của dòng Số dư đầu kỳ",
       "3. " + E + ", " + LOC_E + ", cùng các ô đó"],
      F0,
      ["- HRM: các ô đó TRỐNG",
       "- ERP: in \"-\" (K3 - khác biệt đã chốt, không ghi lỗi)"]),
    T("008", "Định dạng số theo chuẩn quốc tế", "P1",
      ["TK-TCT", "NCC-T03: UNC-F1 5,000 USD tỷ giá 25,450"],
      ["1. " + M, "2. Lọc NCC-T03, Tài khoản 331, Thời gian 01/11/2026 - 30/11/2026, Loại tiền Ngoại tệ",
       "3. Đọc dòng UNC-F1"],
      "Loại tiền: Ngoại tệ",
      ["- Số phát sinh ngoại tệ Nợ \"5,000\"; Tỷ giá \"25,450\"; Số phát sinh VNĐ Nợ \"127,250,000\"",
       "- Phẩy ngăn nghìn, chấm thập phân, không có \".00\" thừa"]),
    T("009", "Bộ lọc không khớp bút toán nào", "P1",
      ["TK-KT", "NCC-T02 chỉ có PC-N5 ngày 11/11/2026"],
      ["1. " + M, "2. Chọn Tài khoản 331, Nhà cung cấp NCC-T02, Thời gian 01/10/2026 - 31/10/2026"],
      "Thời gian: 01/10/2026 - 31/10/2026",
      ["- 3 dòng tổng vẫn hiện, các ô số đều TRỐNG",
       "- Dưới dòng tổng: \"" + MSG_RONG + "\"",
       "- Không có thanh phân trang"]),
    T("010", "Phân trang mặc định 10 bút toán", "P1",
      ["TK-TCT", "NCC-NHIEU: nhà cung cấp thật có từ 25 bút toán trở lên TK 331 trong kỳ chọn (ghi số N vào Ghi chú)"],
      ["1. " + M, "2. Lọc NCC-NHIEU, Tài khoản 331, kỳ có từ 25 bút toán trở lên", "3. Quan sát dưới bảng"],
      "Nhà cung cấp: NCC-NHIEU",
      ["- \"Số dòng/trang:\" mặc định 10, danh sách chọn 10, 20, 50, 100",
       "- \"Hiển thị 1–10 / N bút toán\"; nút trang 1 đang chọn, nút về trang trước mờ",
       "- ERP không phân trang, hiện đủ N dòng (K2 - khác biệt đã chốt, không ghi lỗi); N 2 bên bằng nhau"]),
    T("011", "Chuyển trang: STT liên tục, dòng tổng giữ nguyên", "P0",
      ["Như TC_01.010"],
      ["1. Ghi 3 dòng tổng ở trang 1", "2. Bấm trang 2", "3. Bấm nút trang cuối, rồi nút trang đầu"],
      "-",
      ["- Trang 2: STT 11..20, \"Hiển thị 11–20 / N bút toán\"",
       "- Dòng tổng ở trang 2 và trang cuối GIỐNG HỆT trang 1 (tính trên toàn kỳ, không theo trang)",
       "- Thứ tự bút toán nối tiếp theo ngày hạch toán, không trùng, không mất dòng giữa 2 trang"]),
    T("012", "Đổi số dòng / trang", "P1",
      ["Như TC_01.010, đang ở trang 2"],
      ["1. Chọn Số dòng/trang = 50"],
      "Số dòng/trang: 50",
      ["- Về trang 1, hiện tối đa 50 bút toán, \"Hiển thị 1–50 / N bút toán\" (N < 50 thì 1–N)",
       "- Dòng tổng không đổi"]),
    T("013", "Thứ tự bút toán cùng ngày", "P1",
      ["TK-KT", "Lập thêm 2 phiếu kế toán Nợ 331 NCC-T01 ngày 12/11/2026: PKT-S1 500,000 lập trước, PKT-S2 700,000 lập "
       "sau (Lưu và duyệt). Xoá ở TC_07.006 hoặc trừ khi so tổng"],
      ["1. " + M + ", " + LOC, "2. Quan sát các dòng ngày 12/11/2026", "3. " + E + ", " + LOC_E],
      F0,
      ["- HRM: ngày 12/11 có D4 rồi PKT-S1 rồi PKT-S2 (bút toán ghi sổ trước đứng trước)",
       "- ERP: cùng thứ tự"]),
    T("014", "Biểu tượng chữ i cạnh tiêu đề trang giải thích màn", "P2",
      ["TK-KT"],
      ["1. " + M, "2. Rê chuột / bấm biểu tượng chữ i cạnh tiêu đề trang ở thanh trên cùng"],
      "-",
      ["- Hiện chú thích: \"Sổ chi tiết từng bút toán công nợ của một nhà cung cấp trên một tài khoản theo dõi công nợ: số "
       "dư đầu kỳ, phát sinh Nợ / Có trong kỳ, số dư cuối kỳ. Quyền xem theo tổng công ty hoặc công ty (công ty: sổ của "
       "công ty mình và các hợp đồng do mình tạo).\""]),
    T("015", "Đối chiếu lối vào 2 hệ thống", "P1",
      ["TK-KT"],
      ["1. " + M, "2. " + E, "3. Trên HRM tìm mục cùng tên ở phân hệ khác"],
      "-",
      ["- Mỗi hệ thống đúng 1 mục menu, cùng tên \"" + TEN + "\"",
       "- HRM: mục nằm ở Tài chính > Kế toán công nợ > Nhà cung cấp; mục \"Bảng cân đối phát sinh công nợ nhà cung cấp\" "
       "cùng nhóm chưa có màn (giống ERP, mục đó cũng không mở được gì)"]),
    T("016", "Bảng rộng cuộn ngang, tiêu đề dính khi cuộn dọc", "P2",
      ["TK-TCT, NCC-NHIEU mẫu Ngoại tệ, 50 dòng / trang"],
      ["1. Cuộn bảng xuống cuối", "2. Cuộn ngang sang cột Tài khoản đối ứng"],
      "-",
      ["- Tiêu đề 2 tầng luôn hiện trên cùng khi cuộn dọc",
       "- Cuộn ngang trong khung bảng, trang không vỡ bố cục; cột Ghi chú, Tên tài khoản tự xuống dòng"]),
]

# ================================================================== II. TÌM KIẾM & LỌC DANH SÁCH
S2 = [
    T("001", "Bấm Tìm kiếm khi chưa chọn ô bắt buộc nào", "P0",
      ["TK-KT, bộ lọc trống"],
      ["1. " + M, "2. Bấm Tìm kiếm", "3. " + E + ", bấm nút Tìm khi chưa chọn gì"],
      "-",
      ["- HRM: chữ đỏ dưới 3 ô: \"" + MSG_TK + "\", \"" + MSG_NCC + "\", \"" + MSG_TG + "\"; bảng vẫn \"" + MSG_CHO + "\"",
       "- Khung lọc đang thu gọn thì tự mở ra để thấy chữ đỏ",
       "- ERP: chữ đỏ \"Bắt buộc chọn\" dưới 4 ô + thông báo \"Chưa chọn đủ điều kiện bắt buộc\" (K9 - khác biệt đã chốt)"]),
    T("002", "Thiếu riêng Nhà cung cấp", "P0",
      ["TK-KT"],
      ["1. " + M, "2. Chọn Tài khoản 331, Thời gian 01/11/2026 - 30/11/2026, để trống Nhà cung cấp", "3. Bấm Tìm kiếm"],
      "Nhà cung cấp: (trống)",
      ["- Chỉ ô Nhà cung cấp báo đỏ \"" + MSG_NCC + "\"",
       "- Không tải dữ liệu; Tài khoản và Thời gian vẫn giữ giá trị đã chọn"]),
    T("003", "Thiếu riêng Tài khoản", "P1",
      ["TK-KT"],
      ["1. Chọn Nhà cung cấp NCC-T01, Thời gian 01/11/2026 - 30/11/2026", "2. Bấm Tìm kiếm"],
      "Tài khoản: (trống)",
      ["- Ô Tài khoản báo đỏ \"" + MSG_TK + "\"; không tải dữ liệu"]),
    T("004", "Thiếu riêng Thời gian", "P1",
      ["TK-KT"],
      ["1. Chọn Tài khoản 331, Nhà cung cấp NCC-T01", "2. Bấm Tìm kiếm"],
      "Thời gian: (trống)",
      ["- Ô Thời gian báo đỏ \"" + MSG_TG + "\"; không tải dữ liệu"]),
    T("005", "Chữ đỏ tự tắt khi chọn đủ", "P1",
      ["Đang có chữ đỏ ở 3 ô sau TC_02.001"],
      ["1. Chọn lần lượt Tài khoản 331, Nhà cung cấp NCC-T01, Thời gian 01/11/2026 - 30/11/2026"],
      F0,
      ["- Chọn ô nào thì chữ đỏ dưới ô đó tắt ngay",
       "- Chọn đủ 3 ô là bảng tự tải sổ, không cần bấm Tìm kiếm; số liệu như TC_01.005"]),
    T("006", "Ô Tài khoản chỉ liệt kê tài khoản theo dõi công nợ", "P1",
      ["TK-KT"],
      ["1. Mở ô Tài khoản", "2. Gõ \"331\"", "3. Gõ \"1111\""],
      "Tài khoản: 331, 1111",
      ["- Danh sách dạng \"<số tài khoản> - <tên tài khoản>\", chỉ tài khoản đang dùng có theo dõi công nợ",
       "- Có 331 và 3311; KHÔNG có 1111 (không theo dõi công nợ)",
       "- Cùng danh sách với ô \"Chọn tài khoản\" của ERP"]),
    T("007", "Chọn tài khoản cha lấy cả tài khoản con trực tiếp", "P0",
      ["TK-KT, bộ mẫu: D1 ghi vào 3311, các bút toán khác vào 331"],
      ["1. " + LOC_C, "2. Đổi Tài khoản sang 3311", "3. " + E + ", lặp lại 2 lần lọc"],
      "Tài khoản: 331, sau đó 3311",
      ["- Bước 1 (331): có D1 (3311) cùng 4 bút toán 331, tổng như TC_01.005",
       "- Bước 2 (3311): chỉ D1; đầu kỳ trống; Tổng phát sinh có 22,000,000; Số dư cuối kỳ cột Phát sinh có 22,000,000",
       "- ERP ra cùng số dòng và cùng tổng phát sinh ở cả 2 lần lọc"]),
    T("008", "Ô Nhà cung cấp tìm theo mã / tên", "P1",
      ["TK-KT"],
      ["1. Bấm vào ô Nhà cung cấp, chưa gõ gì", "2. Gõ \"Minh An\"", "3. Gõ \"ncc-t0\"", "4. Gõ \"khongcoNCCnay\""],
      "Từ khoá: Minh An; ncc-t0; khongcoNCCnay",
      ["- Bước 1: nhắc \"Vui lòng nhập thêm 1 ký tự\"",
       "- Bước 2: hiện \"NCC-T01 - Công ty TNHH Thiết bị Minh An\"",
       "- Bước 3: không phân biệt hoa thường, hiện NCC-T01, NCC-T02, NCC-T03 (tối đa 20 kết quả)",
       "- Bước 4: không có kết quả; KHÔNG hiện khách hàng thường (không phải nhà cung cấp)"]),
    T("009", "Chọn Nhà cung cấp khác thì sổ tự tải lại", "P0",
      ["TK-KT đang xem sổ NCC-T01 theo F0"],
      ["1. Đổi Nhà cung cấp sang NCC-T02"],
      "Nhà cung cấp: NCC-T02",
      ["- Bảng tự tải lại, không cần bấm Tìm kiếm",
       "- Chỉ còn PC-N5 (11/11/2026, Phát sinh nợ 9,000,000); không còn bút toán nào của NCC-T01",
       "- Đầu kỳ trống; Tổng phát sinh nợ 9,000,000; Số dư cuối kỳ cột Phát sinh nợ 9,000,000"]),
    T("010", "Xoá giá trị ô Nhà cung cấp", "P1",
      ["TK-KT đang xem sổ NCC-T01"],
      ["1. Bấm nút x trong ô Nhà cung cấp"],
      "-",
      ["- Bảng trở về \"" + MSG_CHO + "\", mất dòng tổng và phân trang"]),
    T("011", "Đổi kỳ: bút toán trước kỳ chuyển vào Số dư đầu kỳ", "P0",
      ["TK-KT, bộ mẫu mục 1"],
      ["1. " + LOC_C, "2. Đổi Thời gian sang 11/11/2026 - 30/11/2026", "3. " + E + ", lọc cùng kỳ mới"],
      "Thời gian: 11/11/2026 - 30/11/2026",
      ["- Còn 2 bút toán D4, D5",
       "- Số dư đầu kỳ cột Phát sinh có 53,800,000 (= 38,000,000 + 22,000,000 + 8,800,000 - 15,000,000)",
       "- Tổng phát sinh nợ 26,500,000; phát sinh có trống",
       "- Số dư cuối kỳ cột Phát sinh có 27,300,000 (KHÔNG đổi so với kỳ 01/11 - 30/11)",
       "- ERP ra cùng số dư đầu kỳ, cùng tổng phát sinh, cùng cuối kỳ"]),
    T("012", "Đến ngày lấy trọn ngày cuối", "P0",
      ["TK-KT", "D5 có ngày hạch toán 30/11/2026"],
      ["1. Lọc Thời gian 30/11/2026 - 30/11/2026", "2. Lọc Thời gian 01/11/2026 - 29/11/2026"],
      ["Lần 1 Thời gian: 30/11/2026 - 30/11/2026", "Lần 2 Thời gian: 01/11/2026 - 29/11/2026"],
      ["- Lần 1: chỉ D5 (Phát sinh nợ 1,500,000); Số dư đầu kỳ cột Phát sinh có 28,800,000; Số dư cuối kỳ cột Phát sinh "
       "có 27,300,000",
       "- Lần 2: KHÔNG có D5; Số dư cuối kỳ cột Phát sinh có 28,800,000",
       "- ERP cùng kết quả 2 lần lọc"]),
    T("013", "Bút toán sau Đến ngày không lên và không vào đầu kỳ", "P0",
      ["TK-KT", "N3 phiếu kế toán PKT-N3 ngày 01/12/2026 Nợ 331 NCC-T01 2,000,000 (đã duyệt)"],
      ["1. " + LOC_C, "2. Đổi Thời gian sang 01/12/2026 - 31/12/2026"],
      "Thời gian: 01/12/2026 - 31/12/2026",
      ["- Bước 1: không có PKT-N3, tổng như TC_01.005",
       "- Bước 2: có PKT-N3 (Nợ 2,000,000); Số dư đầu kỳ cột Phát sinh có 27,300,000 (= cuối kỳ tháng 11); Số dư cuối kỳ "
       "cột Phát sinh có 25,300,000"]),
    T("014", "Lọc Tài khoản đối ứng", "P0",
      ["TK-KT, bộ mẫu: PKT-T0 (trước kỳ) và D4 có đối ứng 1121"],
      ["1. " + LOC_C, "2. Chọn Tài khoản đối ứng 1121", "3. " + E + ", " + LOC_E + ", chọn tài khoản đối ứng"],
      "Tài khoản đối ứng: 1121",
      ["- HRM: tự tải lại, chỉ còn D4; Số dư đầu kỳ cột Phát sinh nợ 12,000,000 (chỉ PKT-T0); Tổng phát sinh nợ 25,000,000; "
       "Số dư cuối kỳ cột Phát sinh nợ 37,000,000",
       "- Ô Tài khoản đối ứng HRM liệt kê mọi tài khoản đang dùng (có 1121)",
       "- ERP: ô chỉ có tài khoản theo dõi công nợ (không chọn được 1121); chọn tài khoản khác thì báo \"Đã có lỗi xảy ra\" "
       "(K7 - hệ thống mới đã sửa, không ghi lỗi)"]),
    T("015", "Lọc Đơn hàng/Hợp đồng khớp chính xác", "P0",
      ["TK-KT, bộ mẫu mục 1"],
      ["1. " + LOC_C, "2. Gõ Đơn hàng/Hợp đồng \"HDM-T02\", bấm Tìm kiếm", "3. Sửa thành \"HDM-T0\", bấm Enter"],
      "Đơn hàng/Hợp đồng: HDM-T02; HDM-T0",
      ["- Lần 1: D1, D4, D5; đầu kỳ trống; Tổng phát sinh nợ 26,500,000, có 22,000,000; Số dư cuối kỳ cột Phát sinh nợ "
       "4,500,000",
       "- Lần 2: \"" + MSG_RONG + "\", 3 dòng tổng trống (khớp chính xác, không tìm một phần mã)",
       "- Gõ xong chưa bấm Tìm kiếm / Enter thì bảng KHÔNG đổi"]),
    T("016", "Lọc Số chứng từ theo một phần mã", "P1",
      ["TK-KT, mã UNC-T01 đã ghi ở TC_01.006"],
      ["1. " + LOC_C, "2. Gõ 6 ký tự cuối mã UNC-T01 vào ô Số chứng từ, Enter"],
      "Số chứng từ: 6 ký tự cuối mã UNC-T01",
      ["- Chỉ còn D4; đầu kỳ trống (không có bút toán trước kỳ khớp mã); Tổng phát sinh nợ 25,000,000; Số dư cuối kỳ cột "
       "Phát sinh nợ 25,000,000",
       "- ERP cùng dòng D4"]),
    T("017", "Lọc Nhân viên = người lập hợp đồng", "P0",
      ["TK-KT", "HDM-T01, HDV-T01 do NV-MH1 lập; HDM-T02 do NV-MH2 lập"],
      ["1. " + LOC_C, "2. Chọn Nhân viên NV-MH1", "3. Đổi sang NV-MH2", "4. " + E + ", lặp lại"],
      "Nhân viên: NV-MH1; NV-MH2",
      ["- NV-MH1: D2, D3; đầu kỳ cột Phát sinh có 38,000,000; Tổng phát sinh nợ 15,000,000, có 8,800,000; cuối kỳ cột "
       "Phát sinh có 31,800,000",
       "- NV-MH2: D1, D4, D5; đầu kỳ trống; nợ 26,500,000, có 22,000,000; cuối kỳ cột Phát sinh nợ 4,500,000",
       "- Danh sách bút toán 2 bên khớp nhau (lọc theo người LẬP HỢP ĐỒNG, không phải người lập chứng từ)"]),
    T("018", "Lọc Loại tiền Ngoại tệ", "P0",
      ["TK-KT, F0 phiếu kế toán USD của NCC-T01 ngày 07/11/2026"],
      ["1. " + LOC_C, "2. Đổi Loại tiền sang Ngoại tệ"],
      "Loại tiền: Ngoại tệ",
      ["- Tự tải lại, bảng chuyển mẫu 15 cột",
       "- Chỉ 1 bút toán PKT-F0: Loại tiền USD, Số phát sinh ngoại tệ Có 1,000, Tỷ giá 25,350, Số phát sinh VNĐ Có "
       "25,350,000",
       "- Dòng tổng USD: Số dư đầu kỳ trống; Tổng phát sinh Có 1,000 / 25,350,000; Số dư cuối kỳ Có 1,000 / 25,350,000",
       "- Mẫu VNĐ (bước 1) KHÔNG có PKT-F0"]),
    T("019", "Lọc Số tiền từ / đến theo từng bút toán", "P0",
      ["TK-KT, bộ mẫu mục 1"],
      ["1. " + LOC_C, "2. Nhập Số tiền từ 10,000,000, Số tiền đến 25,000,000, bấm Tìm kiếm",
       "3. " + E + ", cùng bộ lọc"],
      "Số tiền từ: 10,000,000\nSố tiền đến: 25,000,000",
      ["- Còn D1 (22,000,000), D3 (15,000,000), D4 (25,000,000 - lấy cả mốc bằng)",
       "- Số dư đầu kỳ cột Phát sinh nợ 12,000,000 (chỉ PKT-T0; KB1 50,000,000 bị loại)",
       "- Tổng phát sinh nợ 40,000,000, có 22,000,000; Số dư cuối kỳ cột Phát sinh nợ 30,000,000",
       "- ERP cùng danh sách bút toán"]),
    T("020", "Số tiền để trống hoặc bằng 0 thì không lọc", "P2",
      ["TK-KT"],
      ["1. " + LOC_C, "2. Nhập Số tiền từ 0, bấm Tìm kiếm"],
      "Số tiền từ: 0",
      ["- Kết quả như TC_01.005 (0 coi như không lọc)"]),
    T("021", "Số tiền từ lớn hơn Số tiền đến", "P2",
      ["TK-KT"],
      ["1. " + LOC_C, "2. Nhập Số tiền từ 30,000,000, Số tiền đến 10,000,000, bấm Tìm kiếm"],
      "Số tiền từ: 30,000,000\nSố tiền đến: 10,000,000",
      ["- Không lỗi trang; \"" + MSG_RONG + "\"; dòng tổng trống",
       "- Lưu ý: ghi Ghi chú nếu nghiệp vụ muốn báo đỏ thay vì trả rỗng"]),
    T("022", "Ô tìm nhanh theo số chứng từ hoặc số hợp đồng", "P1",
      ["TK-KT, bộ mẫu mục 1"],
      ["1. " + LOC_C, "2. Gõ \"HDM-T0\" vào ô tìm nhanh, bấm Tìm kiếm", "3. Gõ \"  HDM-T01  \" (có khoảng trắng "
       "đầu cuối), Enter", "4. Gõ \"%_\", Enter"],
      "Tìm nhanh: HDM-T0; HDM-T01 có khoảng trắng; %_",
      ["- Bước 2: đủ 5 bút toán (tìm một phần mã hợp đồng)",
       "- Bước 3: D3 (HDM-T01); đầu kỳ cột Phát sinh có 38,000,000 (KB1, PKT-T0 cùng hợp đồng); cuối kỳ cột Phát sinh có "
       "23,000,000; khoảng trắng đầu cuối được bỏ",
       "- Bước 4: không lỗi, \"" + MSG_RONG + "\" (ký tự đặc biệt tìm như chữ thường)",
       "- Ô tìm nhanh là phần HRM thêm, ERP không có (K9)"]),
    T("023", "Kết hợp nhiều ô lọc", "P1",
      ["TK-KT"],
      ["1. " + LOC_C, "2. Chọn Nhân viên NV-MH2, Tài khoản đối ứng 1121"],
      "Nhân viên: NV-MH2\nTài khoản đối ứng: 1121",
      ["- Chỉ D4; đầu kỳ trống; Tổng phát sinh nợ 25,000,000; Số dư cuối kỳ cột Phát sinh nợ 25,000,000"]),
    T("024", "Ô Công ty chỉ người có quyền tổng công ty mới có", "P0",
      ["TK-TCT; bộ mẫu Công ty B có PKT-B0, B1, B2"],
      ["1. Đăng nhập TK-TCT, " + M + ", " + LOC, "2. Chọn Công ty B", "3. Chọn Công ty A"],
      "Công ty: Công ty B; Công ty A",
      ["- Bước 1: 7 bút toán, đầu kỳ Có 35,000,000, cuối kỳ Có 14,300,000",
       "- Công ty B: B1, B2; đầu kỳ cột Phát sinh nợ 3,000,000; Tổng phát sinh nợ 10,000,000; cuối kỳ cột Phát sinh nợ "
       "13,000,000",
       "- Công ty A: 5 bút toán, số như TK-KT (cuối kỳ Có 27,300,000)",
       "- ERP TK-TCT ô Công ty cho cùng kết quả"]),
    T("025", "Làm mới về mặc định, Loại tiền về VNĐ", "P0",
      ["TK-KT đang lọc F0 + Loại tiền Ngoại tệ + Nhân viên NV-MH1 + tìm nhanh \"HDM\""],
      ["1. Bấm Làm mới", "2. " + E + ", lọc Ngoại tệ rồi bấm nút làm mới"],
      "-",
      ["- HRM: mọi ô về trống, Loại tiền về \"VNĐ\"; bảng \"" + MSG_CHO + "\"; KHÔNG hiện chữ đỏ",
       "- ERP: Loại tiền bị xoá trắng, tiêu đề chuyển sang mẫu ngoại tệ (K8 - khác biệt đã chốt, không ghi lỗi)"]),
    T("026", "Gõ dở chưa bấm Tìm kiếm thì chuyển trang không dùng giá trị gõ dở", "P1",
      ["TK-TCT đang xem NCC-NHIEU trang 1 (N bút toán)"],
      ["1. Gõ \"ZZZ\" vào ô Số chứng từ, KHÔNG bấm Tìm kiếm", "2. Bấm trang 2"],
      "Số chứng từ: ZZZ (chưa áp)",
      ["- Trang 2 vẫn theo bộ lọc cũ: STT 11..20, tổng N không đổi, dòng tổng không đổi"]),
    T("027", "Lưu bộ lọc khi mở tab mới / tải lại trang / chuyển màn", "P2",
      ["TK-KT đang lọc F0 + Nhân viên NV-MH1"],
      ["1. Mở màn ở tab mới trong 10 phút", "2. Ở tab cũ bấm F5", "3. Lọc lại, chuyển sang màn Phiếu chi rồi quay lại"],
      "-",
      ["- Bước 1: tab mới giữ đủ bộ lọc, tải ra đúng sổ",
       "- Bước 2: F5 xoá bộ lọc, bảng \"" + MSG_CHO + "\"",
       "- Bước 3: quay lại màn thì bộ lọc đã xoá (không ghi lỗi)"]),
]

# ================================================================== III. SỐ LIỆU BÁO CÁO
S3 = [
    # --- đối chiếu cùng bộ lọc
    T("001", "Đối chiếu sổ 2 hệ thống: danh sách bút toán", "P0",
      ["TK-KT (đăng nhập được cả 2 hệ thống), bộ mẫu mục 1"],
      ["1. " + M + ", " + LOC, "2. " + E + ", " + LOC_E, "3. So từng dòng: hợp đồng, số chứng từ, nhân viên, phòng ban, "
       "phát sinh nợ, phát sinh có, tài khoản đối ứng"],
      F0,
      ["- 2 bên cùng 5 bút toán, cùng thứ tự D1, D2, D3, D4, D5",
       "- Từng cột khớp nhau (trừ Ngày hạch toán xem TC_03.004, Ghi chú xem TC_03.005)"]),
    T("002", "Đối chiếu sổ 2 hệ thống: dòng tổng", "P0",
      ["Như TC_03.001"],
      ["1. Đọc dòng tổng HRM (đầu bảng)", "2. Đọc dòng tổng ERP (cuối bảng)"],
      F0,
      KQ_KT + ["- ERP: Số dư đầu kỳ Có 38,000,000; Tổng phát sinh nợ 41,500,000 (1 dòng); Tổng phát sinh có 30,800,000 (1 "
               "dòng); Số dư cuối kỳ Có 27,300,000",
               "- Vị trí và số dòng tổng khác nhau là K1 - khác biệt đã chốt, không ghi lỗi; SỐ phải bằng nhau"]),
    T("003", "Công thức đầu kỳ + phát sinh = cuối kỳ", "P0",
      ["TK-TCT, NCC-NHIEU, kỳ 1 tháng có nhiều bút toán"],
      ["1. Lọc NCC-NHIEU, Tài khoản 331, kỳ đã chọn", "2. Tính: đầu kỳ (Nợ dương, Có âm) + Tổng phát sinh nợ - Tổng phát sinh "
       "có", "3. Thêm lần lượt từng ô lọc Nhân viên, Đơn hàng/Hợp đồng, Số tiền từ, tính lại"],
      "-",
      ["- Mọi lần lọc: kết quả tính đúng bằng Số dư cuối kỳ hiển thị (chênh lệch tối đa 0.01 do làm tròn)",
       "- Số dư cuối kỳ của kỳ này = Số dư đầu kỳ khi lọc kỳ kế tiếp"]),
    T("004", "Ngày hạch toán lấy theo ngày ghi sổ", "P1",
      ["TK-KT", "D3 phiếu chi PC-T01 lập ngày 08/11/2026, thủ quỹ duyệt chi ngày 10/11/2026"],
      ["1. " + M + ", " + LOC + ", đọc Ngày hạch toán D3", "2. " + E + ", " + LOC_E + ", đọc cùng dòng"],
      F0,
      ["- HRM: 10/11/2026 (ngày ghi sổ, luôn nằm trong khoảng lọc)",
       "- ERP: lấy ngày trên chứng từ; chứng từ khác ngày ghi sổ thì ERP có thể hiện ngày khác, kể cả ngày ngoài khoảng "
       "lọc (K4 - khác biệt đã chốt, không ghi lỗi)"]),
    T("005", "Cột Ghi chú hiện ghi chú chứng từ", "P1",
      ["TK-KT, bộ mẫu: PNH-T02 ghi chú \"Nhập hàng đợt 1\", UNC-T01 ghi chú \"Thanh toán đợt 1 HDM-T02\""],
      ["1. " + M + ", " + LOC, "2. Đọc cột Ghi chú các dòng", "3. " + E + ", cùng bộ lọc"],
      F0,
      ["- HRM: D1 \"Nhập hàng đợt 1\"; D4 \"Thanh toán đợt 1 HDM-T02\"; D2 (hạch toán mua dịch vụ), D3 (phiếu chi), D5 "
       "(phiếu kế toán) TRỐNG",
       "- ERP: cột Ghi chú trên màn trống hết (K3 - khác biệt đã chốt, không ghi lỗi)"]),
    T("006", "Số dư tách cột theo dấu", "P0",
      ["TK-KT"],
      ["1. Lọc F0 (dư Có)", "2. Lọc thêm Nhân viên NV-MH2 (dư Nợ)"],
      F0,
      ["- Lần 1: Số dư đầu kỳ / cuối kỳ hiện ở cột Phát sinh có, số dương (không có dấu trừ), cột Phát sinh nợ trống",
       "- Lần 2: Số dư cuối kỳ 4,500,000 ở cột Phát sinh nợ, cột Phát sinh có trống; Số dư đầu kỳ bằng 0 nên cả 2 ô trống"]),
    T("007", "Phạm vi theo quyền công ty: đầu kỳ cũng theo phạm vi", "P0",
      ["TK-KT (Công ty A, quyền theo công ty, không lập HĐ nào); PKT-B0, B1, B2 thuộc Công ty B"],
      ["1. Đăng nhập TK-KT, " + M + ", " + LOC],
      F0,
      ["- 5 bút toán, KHÔNG có B1, B2",
       "- Số dư đầu kỳ Có 38,000,000 (KHÔNG trừ PKT-B0 3,000,000 của Công ty B)",
       "- Cuối kỳ Có 27,300,000"]),
    T("008", "Phạm vi quyền công ty: thấy hợp đồng mình lập ở công ty khác", "P0",
      ["TK-CT (Công ty A, quyền theo công ty) là người lập HDM-B2 (Công ty B)"],
      ["1. Đăng nhập HRM bằng TK-CT, " + M + ", " + LOC, "2. Đăng nhập ERP bằng TK-CT, " + LOC_E],
      F0,
      ["- HRM: 6 bút toán (5 của Công ty A + B2); KHÔNG có B1",
       "- Đầu kỳ Có 38,000,000; Tổng phát sinh nợ 45,500,000, có 30,800,000; cuối kỳ Có 23,300,000",
       "- ERP cùng 6 bút toán, cùng số"]),
    T("009", "Phạm vi quyền tổng công ty", "P0",
      ["TK-TCT"],
      ["1. Đăng nhập TK-TCT cả 2 hệ thống, lọc F0 ở cả 2"],
      F0,
      ["- 7 bút toán theo thứ tự D1, D2, D3, D4, B1, B2, D5",
       "- Đầu kỳ Có 35,000,000; Tổng phát sinh nợ 51,500,000, có 30,800,000; cuối kỳ Có 14,300,000",
       "- ERP cùng số"]),
    T("010", "Mẫu Ngoại tệ: tổng theo từng loại tiền", "P0",
      ["TK-TCT, NCC-T03: KB2, PKT-F1, PKT-F2, UNC-F1 như mục 1"],
      ["1. Lọc Tài khoản 331, NCC-T03, Thời gian 01/11/2026 - 30/11/2026, Loại tiền Ngoại tệ", "2. Đọc dòng tổng"],
      "Loại tiền: Ngoại tệ",
      ["- 6 dòng tổng: 3 dòng USD rồi 3 dòng EURO (cột Loại tiền ghi rõ)",
       "- USD: Số dư đầu kỳ Có 10,000 / VNĐ Có 253,500,000; Tổng phát sinh Nợ 5,000 / 127,250,000 và Có 2,000 / 50,700,000; "
       "Số dư cuối kỳ Có 7,000 / VNĐ Có 176,950,000",
       "- EURO: Số dư đầu kỳ trống; Tổng phát sinh Có 1,000 / 27,850,000; Số dư cuối kỳ Có 1,000 / 27,850,000",
       "- Bút toán: PKT-F1 (06/11, USD), PKT-F2 (09/11, EURO), UNC-F1 (13/11, USD)"]),
    T("011", "Mẫu Ngoại tệ: hệ thống cũ cộng lẫn các loại tiền", "P1",
      ["Như TC_03.010"],
      ["1. " + E + ", lọc cùng bộ lọc, Loại tiền Ngoại tệ", "2. Đọc Số dư đầu kỳ, Số dư cuối kỳ nguyên tệ"],
      "Loại tiền: Ngoại tệ",
      ["- ERP: Số dư cuối kỳ nguyên tệ Có 8,000 (cộng lẫn 7,000 USD với 1,000 EURO); VNĐ cuối kỳ Có 204,800,000 (gộp)",
       "- HRM tách USD 7,000 và EURO 1,000 (K6 - hệ thống mới đã sửa, không ghi lỗi)",
       "- Tổng phát sinh từng loại tiền 2 bên phải bằng nhau"]),
    T("012", "Đầu kỳ dùng cùng bộ lọc hợp đồng", "P1",
      ["TK-KT", "Lập thêm khai báo đầu kỳ KB4 cho NCC-T01, HĐ mua có mã bắt đầu bằng HDM-T01 (vd HDM-T01-PL1), TK 331, Dư "
       "có 6,000,000 (xoá ở cuối TC)"],
      ["1. " + LOC_C + ", gõ Đơn hàng/Hợp đồng \"HDM-T01\", Tìm kiếm", "2. " + E + ", cùng bộ lọc",
       "3. Xoá KB4 ở " + KB_H[5:]],
      "Đơn hàng/Hợp đồng: HDM-T01",
      ["- HRM: chỉ D3; Số dư đầu kỳ Có 38,000,000 (KB1 + PKT-T0, KHÔNG có KB4); cuối kỳ Có 23,000,000",
       "- ERP: danh sách cũng chỉ D3 nhưng đầu kỳ có thể cộng cả KB4 (Có 44,000,000) do đầu kỳ tìm theo một phần mã - "
       "hiện tượng hệ thống cũ (K5), hệ thống mới đúng, không ghi lỗi",
       "- Bước 3: xoá xong sổ trở lại như cũ"]),
    T("013", "Tài khoản đối ứng nhiều tài khoản", "P1",
      ["TK-KT, D2 hạch toán mua dịch vụ (đối ứng tài khoản chi phí và 1331); D1 đối ứng 1541, 1331"],
      ["1. " + LOC_C, "2. Đọc cột Tài khoản / Tên tài khoản của D1, D2", "3. So ERP"],
      F0,
      ["- D1: Tài khoản \"1541, 1331\" (cách nhau dấu phẩy, không lặp); Tên tài khoản tương ứng cùng thứ tự",
       "- D2: tài khoản chi phí trên phiếu và 1331",
       "- ERP cùng danh sách tài khoản"]),
    # --- luồng phát sinh
    T("014", "Ghi số nền trước khi lập chứng từ", "P0",
      ["TK-KT, bộ mẫu mục 1"],
      ["1. " + M + ", " + LOC, "2. Ghi 3 dòng tổng và số bút toán vào Ghi chú", "3. " + E + ", ghi số nền ERP"],
      F0,
      ["- Số nền: 5 bút toán; đầu kỳ Có 38,000,000; nợ 41,500,000; có 30,800,000; cuối kỳ Có 27,300,000",
       "- 2 hệ thống cùng số nền; các TC_03.015 - TC_03.024 đều so với số nền MỚI NHẤT"]),
    T("015", "Phiếu chi đã duyệt chi làm tăng Phát sinh nợ", "P0",
      ["Số nền TC_03.014; N2 phiếu chi PC-N2 7,000,000 trả NCC-T01 theo HDM-T01 đang chờ thủ quỹ duyệt"],
      ["1. Lọc lại sổ khi PC-N2 còn chờ duyệt", "2. " + PC_H + ", thủ quỹ duyệt chi PC-N2 (trong kỳ)",
       "3. Lọc lại sổ ở HRM và ERP"],
      "Số tiền: 7,000,000",
      ["- Bước 1: không có PC-N2, số không đổi",
       "- Bước 3: thêm dòng PC-N2, Ngày hạch toán = ngày duyệt chi, Phát sinh nợ 7,000,000, Tài khoản đối ứng 1111",
       "- Tổng phát sinh nợ 48,500,000; Số dư cuối kỳ Có 20,300,000; đầu kỳ không đổi",
       "- ERP thấy ngay dòng mới, cùng số"]),
    T("016", "Phiếu ủy nhiệm chi làm tăng Phát sinh nợ", "P0",
      ["Số nền mới sau TC_03.015"],
      ["1. " + UNC_H + ", lập ủy nhiệm chi trả NCC-T01 theo HDM-T02, 3,500,000, ghi chú \"Thanh toán đợt 2\", duyệt đến khi "
       "ghi sổ", "2. Lọc lại sổ"],
      "Số tiền: 3,500,000",
      ["- Thêm 1 dòng: Phát sinh nợ 3,500,000; Ghi chú \"Thanh toán đợt 2\"; Nhân viên NV-MH2",
       "- Tổng phát sinh nợ tăng 3,500,000; Số dư cuối kỳ Có giảm 3,500,000 (còn 16,800,000)"]),
    T("017", "Phiếu nhập hàng mua trong nước làm tăng Phát sinh có", "P0",
      ["Số nền mới"],
      ["1. " + PNH_H + ", lập phiếu nhập hàng mua trong nước của NCC-T01 theo HDM-T02, hàng 10,000,000, thuế 10%, hoàn thành "
       "và hạch toán trong kỳ", "2. Lọc lại sổ (Tài khoản 331)", "3. Lọc Tài khoản 3311"],
      "Giá trị: 10,000,000 + thuế 1,000,000",
      ["- Thêm 1 dòng Phát sinh có 11,000,000, Tài khoản đối ứng 1541, 1331",
       "- Tổng phát sinh có tăng 11,000,000; Số dư cuối kỳ Có tăng 11,000,000",
       "- Bước 3: dòng mới cũng hiện khi chọn 3311 (ghi vào tài khoản con)"]),
    T("018", "Hạch toán mua dịch vụ làm tăng Phát sinh có", "P1",
      ["Số nền mới; có HĐ mua dịch vụ HDV-T01 của NCC-T01"],
      ["1. " + HTDV_H + ", lập hạch toán mua dịch vụ cho NCC-T01, 5,000,000, thuế 10%, Lưu và duyệt trong kỳ",
       "2. Lọc lại sổ"],
      "Số tiền: 5,000,000 + thuế 500,000",
      ["- Thêm 1 dòng Phát sinh có 5,500,000 (số sau thuế), đối ứng tài khoản chi phí và 1331",
       "- Cuối kỳ Có tăng 5,500,000"]),
    T("019", "Phiếu kế toán: Đang tạo không lên, Lưu và duyệt mới lên", "P0",
      ["Số nền mới; N1 PKT-N1 Đang tạo Nợ 331 NCC-T01 3,000,000 ngày 15/11/2026"],
      ["1. Lọc lại sổ", "2. " + PKT_H + ", mở PKT-N1, bấm Lưu và duyệt", "3. Lọc lại sổ"],
      "Số tiền: 3,000,000",
      ["- Bước 1: không có PKT-N1",
       "- Bước 3: thêm dòng 15/11/2026 Phát sinh nợ 3,000,000; Ghi chú trống; cuối kỳ Có giảm 3,000,000"]),
    T("020", "Khai báo đầu kỳ công nợ NCC làm đổi Số dư đầu kỳ", "P0",
      ["Số nền mới; HĐ mua HDM-T05 của NCC-T01 chưa khai báo đầu kỳ"],
      ["1. " + KB_H + ", thêm khai báo cho NCC-T01, HĐ HDM-T05, Tài khoản 331, Loại dư Dư có, Công nợ 6,000,000, Lưu",
       "2. Lọc lại sổ (kỳ 01/11 - 30/11/2026)", "3. Lọc kỳ chứa ngày tính công nợ đầu kỳ"],
      "Công nợ: 6,000,000\nLoại dư: Dư có",
      ["- Bước 2: KHÔNG thêm dòng; Số dư đầu kỳ Có tăng 6,000,000 (44,000,000); cuối kỳ Có tăng 6,000,000",
       "- Bước 3: dòng khai báo hiện với Số chứng từ = mã khai báo, Phát sinh có 6,000,000",
       "- ERP cùng số dư đầu kỳ mới"]),
    T("021", "Sửa khai báo đầu kỳ thì sổ cập nhật", "P1",
      ["Khai báo HDM-T05 ở TC_03.020 chưa có chứng từ công nợ nào"],
      ["1. Sửa khai báo HDM-T05: Công nợ 6,000,000 thành 6,500,000, Lưu", "2. Lọc lại sổ"],
      "Công nợ: 6,500,000",
      ["- Số dư đầu kỳ Có tăng thêm 500,000 so với TC_03.020; không sinh dòng trùng"]),
    T("022", "Xoá khai báo đầu kỳ thì trả lại số", "P0",
      ["Như TC_03.021"],
      ["1. Xoá khai báo HDM-T05", "2. Lọc lại sổ ở HRM và ERP"],
      "-",
      ["- Số dư đầu kỳ và cuối kỳ trở về đúng như trước TC_03.020",
       "- ERP cùng số"]),
    T("023", "Chứng từ ngày ngoài kỳ không lên, đổi kỳ thì vào đầu kỳ", "P0",
      ["Số nền mới"],
      ["1. " + PKT_H + ", lập phiếu kế toán Nợ 331 NCC-T01 2,500,000, ngày hạch toán 15/10/2026, Lưu và duyệt",
       "2. Lọc lại sổ kỳ 01/11 - 30/11/2026", "3. Lọc kỳ 01/10/2026 - 31/10/2026"],
      "Ngày hạch toán: 15/10/2026\nSố tiền: 2,500,000",
      ["- Bước 2: không thêm dòng; Số dư đầu kỳ Có GIẢM 2,500,000; cuối kỳ Có giảm 2,500,000",
       "- Bước 3: phiếu hiện là dòng ngày 15/10/2026, Phát sinh nợ 2,500,000"]),
    T("024", "Chứng từ lập ở hệ thống cũ cũng lên sổ hệ thống mới", "P0",
      ["Số nền mới"],
      ["1. Trên ERP lập phiếu kế toán Nợ 331 NCC-T01 / Có 1121, 1,800,000, ngày 20/11/2026, duyệt",
       "2. Trên HRM lọc lại sổ (không cần đăng nhập lại)"],
      "Số tiền: 1,800,000",
      ["- HRM có ngay dòng 20/11/2026 Phát sinh nợ 1,800,000, đối ứng 1121; cuối kỳ Có giảm 1,800,000",
       "- Số chứng từ là link mở được phiếu kế toán trên HRM"]),
    T("025", "Bút toán ngoại tệ không lẫn vào mẫu VNĐ", "P1",
      ["Số nền mới mẫu VNĐ và mẫu Ngoại tệ của NCC-T01"],
      ["1. " + PKT_H + ", lập phiếu kế toán Có 331 NCC-T01 500 USD, tỷ giá 25,350, trong kỳ, Lưu và duyệt",
       "2. Lọc mẫu VNĐ", "3. Lọc mẫu Ngoại tệ"],
      "Số tiền: 500 USD (12,675,000)",
      ["- Mẫu VNĐ: KHÔNG đổi",
       "- Mẫu Ngoại tệ: thêm dòng USD Có 500 / 12,675,000; dòng tổng USD phát sinh có 1,500 / 38,025,000; cuối kỳ Có 1,500 "
       "/ 38,025,000"]),
]

# ================================================================== IV. XEM CHI TIẾT CHỨNG TỪ LIÊN KẾT
S4 = [
    T("001", "Bấm Số chứng từ phiếu chi mở phiếu chi trên hệ thống mới", "P0",
      ["TK-KT có quyền xem Phiếu chi; bộ lọc F0"],
      ["1. " + LOC_C, "2. Bấm mã PC-T01 ở dòng D3"],
      "-",
      ["- Mở TAB MỚI màn chi tiết phiếu chi PC-T01 trên HRM, đúng mã, đúng số tiền 15,000,000",
       "- Tab sổ giữ nguyên bộ lọc và trang đang xem"]),
    T("002", "Link ủy nhiệm chi, phiếu kế toán, phiếu nhập hàng", "P1",
      ["TK-KT có quyền xem các màn tương ứng"],
      ["1. Bấm Số chứng từ D4 (ủy nhiệm chi)", "2. Bấm D5 (phiếu kế toán)", "3. Bấm D1 (phiếu nhập hàng)"],
      "-",
      ["- Mỗi link mở tab mới đúng màn chi tiết chứng từ trên HRM, đúng mã"]),
    T("003", "Link khai báo đầu kỳ công nợ NCC", "P2",
      ["TK-KT, lọc kỳ chứa ngày tính công nợ đầu kỳ để thấy dòng KB1"],
      ["1. Bấm Số chứng từ của KB1"],
      "-",
      ["- Mở tab mới màn chi tiết khai báo đầu kỳ công nợ nhà cung cấp trên HRM, đúng HĐ HDM-T01, Dư có 50,000,000"]),
    T("004", "Link chứng từ hạch toán mua dịch vụ", "P1",
      ["TK-KT, D2 hạch toán mua dịch vụ HTDV-T01"],
      ["1. Bấm Số chứng từ D2", "2. " + E + ", bấm cùng mã"],
      "-",
      ["- Mở được chi tiết hạch toán mua dịch vụ HTDV-T01 (hệ thống mới đã có màn này)",
       "- ERP: mã là link mở chi tiết",
       "- Lưu ý: nếu HRM hiện mã dạng chữ thường không bấm được thì ghi Failed (nghi vấn thiếu link)"]),
    T("005", "Bấm Đơn hàng/Hợp đồng mở hợp đồng mua", "P1",
      ["TK-KT, D3 thuộc HDM-T01 (hợp đồng mua)"],
      ["1. Bấm HDM-T01 ở dòng D3"],
      "-",
      ["- Mở tab mới màn xem hợp đồng mua HDM-T01 trên hệ thống cũ (hệ thống mới chưa có màn hợp đồng mua, K12)"]),
    T("006", "Dòng không có hợp đồng / loại chứng từ chưa có màn", "P2",
      ["TK-TCT, NCC-NHIEU có bút toán không gắn hợp đồng"],
      ["1. Lọc NCC-NHIEU, tìm dòng không có hợp đồng"],
      "-",
      ["- Ô Đơn hàng/Hợp đồng TRỐNG (ERP in \"-\")",
       "- Chứng từ loại chưa có màn ở cả 2 hệ thống: hiện mã dạng chữ, không lỗi trang"]),
    T("007", "Mở link khi thiếu quyền màn chứng từ", "P2",
      ["TK-KT KHÔNG có quyền xem Phiếu kế toán"],
      ["1. Bấm Số chứng từ D5"],
      "-",
      ["- Tab mới bị chặn theo quyền của màn Phiếu kế toán (báo không có quyền), tab sổ không bị ảnh hưởng"]),
]

# ================================================================== V. XUẤT DANH SÁCH EXCEL
S5 = [
    T("001", "Xuất Excel mẫu VNĐ: tên file, tiêu đề, cột", "P0",
      ["TK-KT, bộ lọc F0"],
      ["1. " + LOC_C, "2. Bấm Xuất Excel", "3. Mở file"],
      F0,
      ["- Báo \"" + MSG_XLS_OK + "\", tải ngay file so_chi_tiet_cong_no_ncc.xlsx (không có cửa sổ chọn cột)",
       "- Sheet \"So chi tiet cong no NCC\"; dòng tiêu đề \"SỔ CHI TIẾT CÔNG NỢ PHẢI TRẢ NHÀ CUNG CẤP (TỪ NGÀY 01/11/2026 "
       "ĐẾN NGÀY 30/11/2026)\"",
       "- Tiêu đề cột 1 tầng: STT, Đơn hàng/Hợp đồng, Ngày hạch toán, Số chứng từ, Nhân viên, Phòng ban, Ghi chú, Phát sinh "
       "nợ, Phát sinh có, Tài khoản đối ứng, Tên tài khoản đối ứng",
       "- Cuối file: khối ký \"Ngày ..., tháng ..., năm ...\", \"Người lập\", \"(Ký, họ tên)\""]),
    T("002", "Excel: dòng tổng ở đầu, số khớp màn", "P0",
      ["File từ TC_05.001"],
      ["1. Đọc 3 dòng ngay dưới tiêu đề cột", "2. Đọc các dòng bút toán"],
      "-",
      ["- 3 dòng đầu: nhãn \"Số dư đầu kỳ\", \"Tổng phát sinh\", \"Số dư cuối kỳ\" ở cột Ghi chú; số: đầu kỳ Phát sinh có "
       "38,000,000; tổng nợ 41,500,000, có 30,800,000; cuối kỳ Phát sinh có 27,300,000",
       "- Tiếp theo 5 dòng D1..D5, STT 1..5, đủ cột như màn (cả Ghi chú)",
       "- Ô số là SỐ (cộng được bằng hàm Excel), ngày dạng dd/mm/yyyy không kèm giờ"]),
    T("003", "Excel đúng bộ lọc đã áp", "P0",
      ["TK-KT"],
      ["1. " + LOC_C + ", chọn Nhân viên NV-MH2", "2. Gõ \"ZZZ\" vào Số chứng từ nhưng KHÔNG bấm Tìm kiếm",
       "3. Bấm Xuất Excel"],
      "Nhân viên: NV-MH2",
      ["- File có D1, D4, D5 và dòng tổng như màn (cuối kỳ Phát sinh nợ 4,500,000)",
       "- Giá trị \"ZZZ\" gõ dở KHÔNG áp vào file"]),
    T("004", "Excel xuất đủ mọi trang", "P1",
      ["TK-TCT, NCC-NHIEU N bút toán, đang ở trang 2"],
      ["1. Bấm Xuất Excel"],
      "-",
      ["- Trong lúc xuất hiện tiến độ \"Đã tải x/y dòng…\" rồi \"Đang dựng file … dòng…\"; nút Xuất Excel mờ, bấm lại không "
       "tải 2 lần",
       "- File có đủ N bút toán (không chỉ trang đang xem) + 3 dòng tổng, STT 1..N"]),
    T("005", "Excel mẫu Ngoại tệ", "P0",
      ["TK-TCT, NCC-T03, Loại tiền Ngoại tệ (TC_03.010)"],
      ["1. Bấm Xuất Excel", "2. Mở file"],
      "Loại tiền: Ngoại tệ",
      ["- Cột: 7 cột đầu, Loại tiền, \"Số phát sinh ngoại tệ - Nợ\", \"Số phát sinh ngoại tệ - Có\", Tỷ giá, \"Số phát sinh "
       "VNĐ - Nợ\", \"Số phát sinh VNĐ - Có\", Tài khoản đối ứng, Tên tài khoản đối ứng",
       "- 6 dòng tổng (USD 3 dòng, EURO 3 dòng) đúng số TC_03.010, rồi 3 bút toán"]),
    T("006", "Excel khi thiếu ô bắt buộc", "P1",
      ["TK-KT, chưa chọn Nhà cung cấp"],
      ["1. Bấm Xuất Excel"],
      "-",
      ["- Báo \"" + MSG_THIEU + "\"; chữ đỏ dưới ô thiếu; không tải file"]),
    T("007", "Excel khi bộ lọc không có bút toán", "P2",
      ["TK-KT, lọc như TC_01.009 (0 bút toán)"],
      ["1. Bấm Xuất Excel"],
      "-",
      ["- Mẫu VNĐ: file chỉ có 3 dòng tổng trống, không có dòng bút toán (ghi Ghi chú nếu nghiệp vụ muốn báo \"" + MSG_XLS_RONG
       + "\")",
       "- Mẫu Ngoại tệ không có loại tiền nào: báo \"" + MSG_XLS_RONG + "\", không tải file"]),
    T("008", "Đối chiếu Excel 2 hệ thống", "P1",
      ["TK-KT, bộ lọc F0"],
      ["1. Xuất Excel ở HRM", "2. " + E + ", " + LOC_E + ", bấm \"Xuất excel\"", "3. So 2 file"],
      F0,
      ["- Cùng 5 bút toán, cùng số tiền, cùng tổng phát sinh",
       "- ERP: file cong_no_ncc.xlsx, không STT, cột nhân viên ghi NVKD, dòng tổng ở cuối, ngày kèm giờ (K10 - khác biệt đã "
       "chốt, không ghi lỗi)"]),
    T("009", "Excel áp phạm vi cho cả Số dư đầu kỳ", "P0",
      ["TK-KT (quyền công ty); PKT-B0 Công ty B trước kỳ 3,000,000"],
      ["1. Xuất Excel F0 ở HRM", "2. Xuất Excel F0 ở ERP"],
      F0,
      ["- HRM: Số dư đầu kỳ Phát sinh có 38,000,000 (đúng như màn)",
       "- ERP: dòng \"Công nợ đầu kì\" có thể ra 35,000,000 vì cộng cả PKT-B0 ngoài phạm vi - hiện tượng hệ thống cũ (K10), "
       "hệ thống mới đúng, không ghi lỗi"]),
]

# ================================================================== VI. IN BÁO CÁO
S6 = [
    T("001", "In: mở bản xem trước", "P0",
      ["TK-KT, bộ lọc F0"],
      ["1. " + LOC_C, "2. Bấm In"],
      F0,
      ["- Mở cửa sổ \"Xem trước sổ chi tiết công nợ phải trả nhà cung cấp\", khổ ngang",
       "- Đầu trang: tiêu đề công ty của người in, tiêu đề \"" + TIEU_DE_IN + "\"",
       "- Dòng thông tin: Công ty: Tất cả; Nhà cung cấp: NCC-T01 - Công ty TNHH Thiết bị Minh An; Tài khoản: 331 - <tên>; "
       "Loại tiền: VNĐ; Từ ngày: 01/11/2026; Đến ngày: 30/11/2026"]),
    T("002", "In: bảng và dòng tổng khớp màn", "P0",
      ["Bản xem trước TC_06.001"],
      ["1. Đọc bảng trên bản in"],
      "-",
      ["- Tiêu đề 2 tầng như màn; 3 dòng tổng ĐẦU bảng in đậm, số như TC_01.005",
       "- 5 bút toán đủ cột, STT 1..5, số chuẩn quốc tế, ô 0 để trống",
       "- Cuối: \"Ngày dd tháng mm năm yyyy\" (ngày in), \"Người lập\", \"Kế toán trưởng\" kèm \"(Ký, họ tên)\""]),
    T("003", "In đủ mọi trang, đúng bộ lọc đã áp", "P1",
      ["TK-TCT, NCC-NHIEU N bút toán (N không quá 2,000), đang ở trang 2, ô Số chứng từ gõ dở \"ZZZ\""],
      ["1. Bấm In"],
      "-",
      ["- Bản in có đủ N bút toán (không chỉ trang đang xem), bỏ qua \"ZZZ\" chưa áp"]),
    T("004", "In mẫu Ngoại tệ", "P1",
      ["TK-TCT, NCC-T03 Ngoại tệ"],
      ["1. Bấm In"],
      "Loại tiền: Ngoại tệ",
      ["- Dòng thông tin Loại tiền: Ngoại tệ; bảng 15 cột; 6 dòng tổng theo USD / EURO như TC_03.010"]),
    T("005", "In: thông tin Công ty theo quyền", "P2",
      ["TK-TCT chọn ô Công ty = Công ty B"],
      ["1. Bấm In"],
      "Công ty: Công ty B",
      ["- Dòng \"Công ty: Công ty B\"; chỉ bút toán Công ty B",
       "- Người quyền theo công ty (TK-KT) in thì dòng Công ty ghi \"Tất cả\" (dữ liệu vẫn theo phạm vi; ghi Ghi chú nếu "
       "nghiệp vụ muốn ghi tên công ty)"]),
    T("006", "In khi thiếu ô bắt buộc", "P1",
      ["TK-KT, chưa chọn Thời gian"],
      ["1. Bấm In"],
      "-",
      ["- Báo \"" + MSG_THIEU + "\"; chữ đỏ dưới ô Thời gian; không mở bản xem trước"]),
    T("007", "In vượt 2,000 bút toán", "P2",
      ["TK-TCT, Tài khoản 331, NCC có hơn 2,000 bút toán trong kỳ dài (vd cả năm)"],
      ["1. Bấm In"],
      "-",
      ["- Bản xem trước không có nội dung, hiện \"Danh sách có <N> dòng, vượt mức in tối đa 2,000 dòng nên chưa in được. Vui "
       "lòng thu hẹp bộ lọc (khoảng thời gian, trạng thái…) rồi in lại, hoặc dùng Xuất Excel cho danh sách dài.\""]),
    T("008", "Hệ thống cũ không có In", "P2",
      ["TK-KT"],
      ["1. " + E + ", tìm nút In"],
      "-",
      ["- ERP chỉ có nút Xuất excel, không có In (In là phần hệ thống mới thêm, user chốt 04/11/2026)"]),
]

# ================================================================== VII. RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC
S7 = [
    T("001", "Khớp số với Khai báo đầu kỳ công nợ nhà cung cấp", "P1",
      ["TK-KT; KB1 HDM-T01 Dư có 50,000,000"],
      ["1. " + KB_H + ", tìm khai báo của NCC-T01", "2. Trên sổ lọc kỳ chứa ngày tính công nợ đầu kỳ, Đơn hàng/Hợp đồng "
       "HDM-T01"],
      "-",
      ["- Dòng KB1 trên sổ: Phát sinh có 50,000,000 bằng Công nợ trên màn khai báo, cùng mã khai báo, cùng tài khoản 331"]),
    T("002", "Khớp số với phiếu chi / ủy nhiệm chi", "P1",
      ["TK-KT"],
      ["1. Mở chi tiết PC-T01 và UNC-T01", "2. So với dòng D3, D4 trên sổ"],
      "-",
      ["- Số tiền phần trả NCC-T01, ngày duyệt chi, hợp đồng trên phiếu bằng Phát sinh nợ, Ngày hạch toán, Đơn hàng/Hợp "
       "đồng trên sổ"]),
    T("003", "Khớp với Sổ chi tiết các tài khoản của hệ thống cũ", "P1",
      ["TK-TCT"],
      ["1. " + SOTK_E + ", tài khoản 331, kỳ 01/11 - 30/11/2026, lọc đối tượng NCC-T01", "2. So với sổ HRM bộ lọc F0 "
       "(TK-TCT)"],
      F0,
      ["- Tổng phát sinh nợ / có của NCC-T01 trên Sổ chi tiết các tài khoản bằng sổ công nợ NCC (51,500,000 / 30,800,000)"]),
    T("004", "Số dư cuối kỳ khớp số còn phải trả theo hợp đồng", "P2",
      ["TK-KT"],
      ["1. Lọc F0 + Đơn hàng/Hợp đồng HDM-T02", "2. Đối chiếu với giá trị nhập hàng và số đã trả trên hồ sơ HDM-T02"],
      "Đơn hàng/Hợp đồng: HDM-T02",
      ["- Cuối kỳ dư Nợ 4,500,000 = đã trả (25,000,000 + chiết khấu 1,500,000) vượt giá trị nhập (22,000,000); kế toán "
       "xác nhận đúng nghiệp vụ"]),
    T("005", "Ngoài kỳ khoá sổ: chứng từ sửa ngày hạch toán", "P2",
      ["Phiếu kế toán PKT-T1 (D5) ngày 30/11/2026 còn sửa được ở ERP / HRM theo quy định"],
      ["1. Nếu nghiệp vụ cho phép sửa ngày hạch toán phiếu Đã duyệt, đổi sang 01/12/2026", "2. Lọc lại sổ kỳ tháng 11"],
      "-",
      ["- D5 rời kỳ tháng 11, cuối kỳ Có tăng 1,500,000; không cho sửa thì ghi \"không áp dụng\""]),
    T("006", "Dọn dữ liệu đã lập trong lúc test", "P2",
      ["Đã chạy xong nhóm III"],
      ["1. Liệt kê mã chứng từ đã lập ở TC_01.013, TC_03.015 - TC_03.025 (Ghi chú)", "2. Xoá / huỷ theo đúng quy trình "
       "từng màn nếu được phép"],
      "-",
      ["- Chứng từ xoá được thì sổ trả lại đúng số; chứng từ đã ghi sổ không xoá được thì ghi lại số chênh để các vòng test "
       "sau tính số nền mới"]),
    T("007", "Hai người xem cùng lúc khi có chứng từ mới", "P2",
      ["TK-KT và TK-TCT cùng mở sổ NCC-T01"],
      ["1. TK-TCT lập và duyệt phiếu kế toán mới cho NCC-T01", "2. TK-KT bấm Tìm kiếm lại"],
      "-",
      ["- TK-KT thấy ngay bút toán mới (nếu thuộc Công ty A), số tổng cập nhật; không cần đăng nhập lại"]),
]

# ================================================================== VIII. PHÂN QUYỀN
S8 = [
    T("001", "Quyền theo tổng công ty", "P0",
      ["TK-TCT chỉ có quyền \"" + P_ALL + "\""],
      ["1. Đăng nhập TK-TCT", "2. " + M, "3. Lọc F0"],
      F0,
      ["- Thấy mục menu; có ô Công ty liệt kê mọi công ty",
       "- 7 bút toán, cuối kỳ Có 14,300,000; In / Xuất Excel dùng được"]),
    T("002", "Quyền theo công ty", "P0",
      ["TK-KT chỉ có quyền \"" + P_CT + "\""],
      ["1. Đăng nhập TK-KT", "2. " + M, "3. Lọc F0"],
      F0,
      ["- Thấy mục menu; KHÔNG có ô Công ty",
       "- 5 bút toán của Công ty A, cuối kỳ Có 27,300,000"]),
    T("003", "Quyền theo công ty ở công ty khác", "P0",
      ["TK-CTB (Công ty B, quyền theo công ty)"],
      ["1. Đăng nhập TK-CTB, " + M + ", lọc F0"],
      F0,
      ["- Chỉ B1, B2; đầu kỳ Phát sinh nợ 3,000,000; tổng nợ 10,000,000; cuối kỳ Phát sinh nợ 13,000,000",
       "- KHÔNG thấy bút toán Công ty A"]),
    T("004", "Có cả 2 quyền thì lấy quyền rộng hơn", "P1",
      ["TK-2Q có cả 2 quyền"],
      ["1. Đăng nhập TK-2Q, " + M + ", lọc F0"],
      F0,
      ["- Có ô Công ty; 7 bút toán như TK-TCT"]),
    T("005", "Không có quyền nào: ẩn menu", "P0",
      ["TK-Z không có quyền nào của màn"],
      ["1. Đăng nhập HRM bằng TK-Z", "2. Mở phân hệ Tài chính > Kế toán công nợ > Nhà cung cấp", "3. " + E],
      "-",
      ["- HRM: KHÔNG có mục \"" + TEN + "\" trong nhóm Nhà cung cấp",
       "- ERP: bấm mục menu thì hiện trang không tìm thấy (K11)"]),
    T("006", "Không quyền mở đường link màn", "P0",
      ["TK-Z; đường link màn sao chép từ tài khoản TK-KT"],
      ["1. Đăng nhập TK-Z", "2. Dán đường link màn vào thanh địa chỉ, Enter", "3. Mở ô Nhà cung cấp gõ \"NCC\"",
       "4. Bấm In, bấm Xuất Excel"],
      "-",
      ["- Báo \"" + MSG_KQ + "\"; ô Tài khoản không có lựa chọn nào; bảng \"" + MSG_CHO + "\"",
       "- Ô Nhà cung cấp không ra kết quả, báo không có quyền",
       "- In / Xuất Excel không ra dữ liệu nào (báo thiếu ô bắt buộc hoặc không có quyền)",
       "- KHÔNG lộ bất kỳ số liệu công nợ nào"]),
    T("007", "Bị gỡ quyền khi đang mở màn", "P0",
      ["TK-KT đang xem sổ F0"],
      ["1. Quản trị gỡ quyền \"" + P_CT + "\" của TK-KT", "2. TK-KT bấm Tìm kiếm / chuyển trang / Xuất Excel"],
      "-",
      ["- Báo \"" + MSG_KQ + "\", không tải thêm số liệu, không tải file",
       "- Đăng nhập lại: không còn mục menu"]),
    T("008", "Đổi quyền công ty sang tổng công ty", "P1",
      ["TK-KT đang có quyền theo công ty"],
      ["1. Quản trị gán thêm \"" + P_ALL + "\" cho vai trò của TK-KT", "2. TK-KT đăng nhập lại, lọc F0"],
      F0,
      ["- Có ô Công ty; 7 bút toán như TK-TCT", "- Gỡ quyền sau TC"]),
    T("009", "Gán quyền ở hệ thống cũ có hiệu lực ở hệ thống mới", "P1",
      ["TK-Z chưa có quyền; vai trò của TK-Z dùng chung 2 hệ thống"],
      ["1. Trên ERP gán vai trò của TK-Z quyền \"" + P_CT + "\"", "2. TK-Z đăng nhập lại HRM, " + M + ", lọc F0"],
      F0,
      ["- HRM hiện menu, ra 5 bút toán Công ty A như TK-KT", "- Gỡ quyền sau TC"]),
    T("010", "Quyền gán thẳng nhân viên, không qua vai trò", "P2",
      ["TK-Y không có vai trò nào có quyền màn; quản trị gán thẳng \"" + P_CT + "\" cho riêng TK-Y"],
      ["1. Đăng nhập TK-Y", "2. Tìm mục menu", "3. Dán đường link màn, lọc F0"],
      F0,
      ["- Bước 2: menu KHÔNG hiện (menu xét quyền theo vai trò)",
       "- Bước 3: xem được sổ theo phạm vi công ty",
       "- Lưu ý: ghi Ghi chú để nghiệp vụ quyết có cần hiện menu cho quyền gán thẳng"]),
    T("011", "Quyền theo công ty nhưng chưa gắn công ty", "P2",
      ["TK-NC có quyền \"" + P_CT + "\", hồ sơ chưa gắn công ty, là người lập HDM-B2"],
      ["1. Đăng nhập TK-NC, " + M + ", lọc F0"],
      F0,
      ["- Chỉ thấy B2 (hợp đồng mình lập); không lỗi trang; không lộ bút toán của công ty khác"]),
    T("012", "Super Admin", "P1",
      ["TK-SA thuộc nhóm Super Admin, vai trò đã gắn 2 quyền màn"],
      ["1. Đăng nhập TK-SA, " + M + ", lọc F0"],
      F0,
      ["- Có ô Công ty, 7 bút toán như TK-TCT, In / Xuất Excel dùng được"]),
]

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", S1),
    ("II", "TÌM KIẾM & LỌC DANH SÁCH", S2),
    ("III", "SỐ LIỆU BÁO CÁO - CÁCH ĐỌC SỔ, ĐỐI CHIẾU HỆ THỐNG CŨ - HỆ THỐNG MỚI VÀ KIỂM SỐ THEO LUỒNG PHÁT SINH", S3),
    ("IV", "XEM CHI TIẾT CHỨNG TỪ LIÊN KẾT", S4),
    ("V", "XUẤT DANH SÁCH EXCEL", S5),
    ("VI", "IN BÁO CÁO", S6),
    ("VII", "RÀNG BUỘC VỚI CÁC CHỨC NĂNG KHÁC", S7),
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
    ids = [(sec, tc[0]) for sec, _, tcs in SECTIONS for tc in tcs]
    assert len(ids) == len(set(ids)), "Trùng mã TC"
    build_chuan(output_file=os.path.join(HERE, "testcase - So chi tiet cong no phai tra nha cung cap.xlsx"),
                sheet_name="Trang tính1",
                feature_name=TEN + " - Cập nhật ngày " + NGAY,
                module_name=MODULE,
                description_block=DESCRIPTION_BLOCK, sections=SECTIONS, loai="bao_cao")
