# -*- coding: utf-8 -*-
"""Sinh testcase.xlsx cho man 'Danh muc goi bao duong' (/customer-care/services).

Ban nay THAY THE `generate-testcase.py` (form cu 15 cot) — dung engine chung
`.claude/skills/testcase-documenter/assets/tc_engine.py` (form 17 cot, 2 khoi summary DNS/TP).

Nguon doi chieu (doc truc tiep tu code nhanh gop_db, 2026-08-17):
  BE  Modules/CustomerCare/Routes/api.php (prefix /services — 3 quyen Them/Sua/Xoa;
      danh sach/xem/in/xuat Excel KHONG gate; route sua+xoa gan `serviceNotLocked`)
      Modules/CustomerCare/Http/Controllers/V1/ServiceController.php
      Modules/CustomerCare/Services/ServiceService.php (1.242 dong)
      Modules/CustomerCare/Entities/Service/{Service,ServiceLevel,ServiceMaintain,
      ServiceMaintainLevel}.php
      Modules/CustomerCare/Http/Requests/Service/ServiceRequest.php
      Modules/CustomerCare/Transformers/ServiceResource/ServiceListResource.php
      app/ExcelExport/ServiceExport.php · app/Services/CatalogHistoryService.php (bang `services`)
  FE  hrm-client/pages/customer-care/services/{index.vue,create.vue,_id/index.vue,_id/edit.vue,
      _id/print.vue,components/ServiceFormComponent.vue,components/ProductSearchModal.vue,
      components/GroupSearchModal.vue}

Chay:  python .plans/gop-db/customer-care-services-catalog/gen_testcase.py
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..", "..", ".claude", "skills", "testcase-documenter", "assets"))

from tc_engine import build  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "testcase.xlsx")

MODULE = "DM gói bảo dưỡng"

# ============================================================ 9 MUC MO TA
DESCRIPTION_BLOCK = [
    ("1. Mục đích tính năng",
     "Quản lý danh mục gói bảo dưỡng của phân hệ Chăm sóc khách hàng: mỗi gói gồm thông tin "
     "chung, danh mục nội dung kiểm tra bảo dưỡng theo từng cấp, hệ số giá bán theo từng công ty, "
     "danh sách hàng hoá áp dụng và file đính kèm PDF.\n"
     "Gói bảo dưỡng là nguồn dữ liệu cho báo giá dịch vụ và phiếu yêu cầu dịch vụ.\n"
     "Người dùng làm được: xem danh sách, tìm kiếm, lọc, tạo mới, sửa, xem chi tiết, nhân bản, "
     "xóa (hoặc khóa), in phiếu, xuất Excel và xem lịch sử thay đổi."),

    ("2. Đối tượng được tính / hiển thị",
     "Danh sách hiển thị TẤT CẢ gói bảo dưỡng của hệ thống, không giới hạn theo công ty của người "
     "đăng nhập:\n"
     "- Gói trạng thái Hoạt động — nhãn xanh; có nút Sửa, Xóa (nếu chưa được sử dụng), Nhân bản, "
     "In, Lịch sử.\n"
     "- Gói trạng thái Khóa — nhãn đỏ; chỉ còn Mở khóa, Nhân bản, In, Lịch sử.\n"
     "- Gói chưa khai nội dung kiểm tra hoặc chưa gắn hàng hoá vẫn hiển thị bình thường.\n"
     "- Cột Tên gói có biểu tượng chữ i khi gói đã khai cấp bảo dưỡng: rê chuột hiện giá bán theo "
     "từng cấp."),

    ("3. Đối tượng bị ẩn / không tính",
     "- Nút Tạo mới và Nhân bản: ẩn khi tài khoản không có quyền Thêm danh mục gói bảo dưỡng.\n"
     "- Nút Sửa: ẩn khi thiếu quyền Sửa, hoặc khi gói đang ở trạng thái Khóa.\n"
     "- Nút Xóa: ẩn khi thiếu quyền Xóa, khi gói đang Khóa, hoặc khi gói ĐÃ ĐƯỢC SỬ DỤNG (đã gắn "
     "hàng hoá, hoặc đã dùng ở báo giá dịch vụ).\n"
     "- Nút Mở khóa: chỉ hiện với gói đang Khóa và tài khoản có quyền Sửa.\n"
     "- Trong ô chọn của form: đơn vị tính đang ngừng sử dụng không xuất hiện.\n"
     "- Màn hình KHÔNG có chức năng nhập từ Excel."),

    ("4. Bộ lọc thời gian áp dụng cho",
     "Không áp dụng. Màn hình không có bộ lọc theo khoảng thời gian; các cột Ngày tạo và Ngày sửa "
     "chỉ dùng để hiển thị và sắp xếp."),

    ("5. Cấu trúc dữ liệu / cây phân cấp",
     "Một gói bảo dưỡng gồm 5 khối dữ liệu:\n"
     "1. Thông tin chung: tên, mã, định mức đàm phán giá, VAT, công ty quản lý, hệ số giá bán, "
     "ghi chú, trạng thái.\n"
     "2. Danh mục kiểm tra bảo dưỡng định kỳ — dạng MA TRẬN: mỗi DÒNG là một nội dung kiểm tra "
     "(kèm ĐVT, số lượng), mỗi CỘT là một cấp bảo dưỡng; ô giao nhau chọn các ghi chú kiểm tra.\n"
     "3. Dòng thông số của từng cấp (nằm dưới ma trận): Định mức công, Hệ số công nghệ, Giá vốn, "
     "Giá công thức, Giá bán cơ sở, Gợi ý hàng hoá.\n"
     "4. Giá vốn theo công ty: mỗi công ty một dòng, nhập Hệ số giá bán riêng.\n"
     "5. Áp dụng cho hàng hoá và File đính kèm PDF.\n"
     "Danh mục phụ thuộc: Cấp dịch vụ, Ghi chú kiểm tra bảo dưỡng, Đơn vị tính, Công ty, Hàng hoá "
     "và Nhóm hàng hoá."),

    ("6. Quy tắc cộng dồn / deduplicate",
     "- Tên gói và Mã gói đều là DUY NHẤT trên toàn hệ thống; mã luôn được lưu dạng CHỮ IN HOA.\n"
     "- Một cấp bảo dưỡng chỉ được chọn một lần trên toàn ma trận: chọn trùng cấp ở cột khác sẽ bị "
     "chặn kèm cảnh báo.\n"
     "- Ô tìm nhanh quét đồng thời Tên và Mã; một bản ghi khớp cả hai vẫn chỉ hiện một dòng.\n"
     "- Kết quả tìm nhanh được xếp theo ĐỘ KHỚP: trùng khít trước, khớp đầu chuỗi tiếp theo, khớp "
     "giữa chuỗi cuối cùng."),

    ("7. Phân quyền cấp",
     "Màn hình dùng 3 quyền, đều thuộc nhóm quyền Danh mục dịch vụ bảo dưỡng:\n"
     "- \"Thêm danh mục gói bảo dưỡng\" — nút Tạo mới và Nhân bản.\n"
     "- \"Sửa danh mục gói bảo dưỡng\" — nút Sửa và nút Mở khóa.\n"
     "- \"Xóa danh mục gói bảo dưỡng\" — nút Xóa.\n"
     "⚠️ Xem danh sách, xem chi tiết, In phiếu và Xuất Excel KHÔNG đòi quyền nào: mọi tài khoản đã "
     "đăng nhập đều xem và xuất được. Đây là hiện trạng giữ nguyên theo phần mềm cũ, KHÔNG phải lỗi "
     "cấu hình môi trường test.\n"
     "Không có phân quyền theo cấp công ty / phòng ban / bộ phận: mọi người thấy chung một danh "
     "sách."),

    ("8. Cách tính các ô thống kê",
     "- Ô \"Hiển thị a–b / N\": a là dòng đầu trang, b là dòng cuối, N là tổng số gói khớp bộ lọc.\n"
     "- Ô \"Số dòng/trang\": 5 / 10 / 20 / 50 / 100, mặc định 10; đổi số dòng thì về trang 1.\n"
     "- Giá bán hiện ở biểu tượng chữ i cạnh tên gói = đơn giá công của công ty quản lý × định mức "
     "công của cấp × hệ số giá bán gói, LÀM TRÒN XUỐNG.\n"
     "- Trong form: Giá vốn = đơn giá công của công ty quản lý × định mức công × hệ số công nghệ; "
     "Giá công thức = Giá vốn × hệ số giá bán gói; Giá bán cơ sở mặc định bằng Giá công thức và "
     "cho phép sửa tay; Giá bán theo từng công ty = Giá bán cơ sở × hệ số của công ty đó."),

    ("9. Ghi chú đọc bảng",
     "Các bẫy dễ sai nhất của màn này — đọc trước khi chạy test:\n"
     "1. ⚠️ Nút Xóa KHÔNG phải lúc nào cũng xóa: gói đã gắn hàng hoá hoặc đã dùng ở báo giá dịch "
     "vụ sẽ bị ẩn nút Xóa; nếu gọi thẳng chức năng Xóa thì hệ thống chuyển gói sang trạng thái Khóa "
     "và báo \"Gói bảo dưỡng đang được sử dụng nên đã được chuyển sang trạng thái Khóa\".\n"
     "2. ⚠️ Xuất Excel xuất TOÀN BỘ danh mục, KHÔNG áp bộ lọc đang có trên màn hình. Lọc còn 6 dòng "
     "nhưng file vẫn ra đủ 221 dòng — đúng thiết kế, đừng ghi Failed.\n"
     "3. ⚠️ Thứ tự cột trong file Excel chạy theo THỨ TỰ BẠN CHỌN ở cửa sổ Chọn trường xuất file, "
     "không theo thứ tự cột trên bảng.\n"
     "4. ⚠️ Gói đang Khóa không sửa được: nút Sửa bị ẩn; gõ thẳng đường dẫn sửa hoặc gọi thẳng chức "
     "năng Sửa đều bị chặn kèm yêu cầu mở khoá trước.\n"
     "5. ⚠️ Mã gói tự chuyển thành CHỮ IN HOA khi lưu; tên gói thì giữ nguyên như nhập.\n"
     "6. ⚠️ Các ô phần trăm và hệ số nhận DẤU PHẨY là dấu thập phân: nhập 12,5 là 12.5 — không "
     "phải lỗi.\n"
     "7. ⚠️ Bắt buộc đính kèm ít nhất 1 file PDF thì mới lưu được gói; đây là quy định riêng của "
     "HRM, phần mềm cũ không bắt buộc.\n"
     "8. ⚠️ Một cấp bảo dưỡng chỉ chọn được một lần trong ma trận; chọn lại cấp đã dùng ở cột khác "
     "sẽ hiện cảnh báo \"Cấp bảo dưỡng này đã được chọn ở cột khác\".\n"
     "9. Bỏ một cột cấp đã phát sinh báo giá dịch vụ sẽ bị hệ thống chặn khi lưu.\n"
     "10. Số liệu tham chiếu của môi trường test khi viết tài liệu: 221 gói bảo dưỡng; tìm từ khoá "
     "\"GBDT\" ra 6 gói; gói \"BDT001\" đang Hoạt động và có sẵn nội dung kiểm tra + giá theo cấp."),
]

# ============================================================ TC PHAN QUYEN
ROLE_TCS = [
    ("00", "Tài khoản KHÔNG có quyền nào vẫn xem được danh sách", "P0",
     "Tài khoản nhân viên thường, không có 3 quyền của màn; danh mục có 221 gói",
     "1. Đăng nhập bằng tài khoản không có quyền nào của màn\n"
     "2. Vào phân hệ Chăm sóc khách hàng → Danh mục → Danh mục gói bảo dưỡng\n"
     "3. Quan sát danh sách và thanh công cụ",
     "Tài khoản: nhân viên thường",
     "- Vào được màn hình, danh sách hiện đủ 221 gói\n"
     "- KHÔNG có nút Tạo mới\n"
     "- Trên từng dòng chỉ còn In và Lịch sử\n"
     "- ⚠️ Đây là hiện trạng ĐÚNG: xem danh sách không đòi quyền"),

    ("01", "Tài khoản không quyền vẫn xem được chi tiết và in", "P0",
     "Vẫn tài khoản ở TC-ROLE-00; gói BDT001 đang Hoạt động",
     "1. Bấm vào mã BDT001 để mở chi tiết\n2. Bấm nút In ở chân trang chi tiết",
     "Gói: BDT001",
     "- Mở được màn chi tiết, mọi ô ở chế độ chỉ đọc\n"
     "- Mở được màn in phiếu Danh mục kiểm tra bảo dưỡng định kỳ\n"
     "- Chân trang chi tiết KHÔNG có nút Sửa"),

    ("02", "Tài khoản không quyền vẫn xuất được Excel", "P1",
     "Vẫn tài khoản ở TC-ROLE-00",
     "1. Bấm nút Xuất Excel\n2. Chọn trường và bấm Xuất file",
     "—",
     "- Cửa sổ Chọn trường xuất file mở bình thường và tải được file\n"
     "- ⚠️ Xuất Excel không gate quyền — nếu nghiệp vụ muốn siết thì phải báo lại"),

    ("03", "Quyền Thêm danh mục gói bảo dưỡng", "P0",
     "Tài khoản CHỈ có quyền \"Thêm danh mục gói bảo dưỡng\"",
     "1. Đăng nhập bằng tài khoản đó\n2. Vào màn danh sách\n3. Quan sát thanh công cụ và menu ba "
     "chấm của một dòng đang Hoạt động",
     "Quyền: Thêm danh mục gói bảo dưỡng",
     "- Có nút Tạo mới\n- Menu ba chấm có Nhân bản, In, Lịch sử\n"
     "- KHÔNG có nút Sửa, KHÔNG có nút Xóa"),

    ("04", "Quyền Sửa danh mục gói bảo dưỡng", "P0",
     "Tài khoản CHỈ có quyền \"Sửa danh mục gói bảo dưỡng\"; danh sách có gói Hoạt động và gói Khóa",
     "1. Đăng nhập bằng tài khoản đó\n2. Quan sát cột Hành động của dòng Hoạt động và dòng Khóa",
     "Quyền: Sửa danh mục gói bảo dưỡng",
     "- Dòng Hoạt động: có nút Sửa, không có nút Xóa\n"
     "- Dòng Khóa: có nút Mở khóa\n- Không có nút Tạo mới và Nhân bản"),

    ("05", "Quyền Xóa danh mục gói bảo dưỡng", "P0",
     "Tài khoản CHỈ có quyền \"Xóa danh mục gói bảo dưỡng\"; có gói chưa được sử dụng",
     "1. Đăng nhập bằng tài khoản đó\n2. Quan sát cột Hành động của gói chưa được sử dụng",
     "Quyền: Xóa danh mục gói bảo dưỡng",
     "- Có nút Xóa ở gói chưa được sử dụng\n- Không có nút Tạo mới, Sửa, Mở khóa"),

    ("06", "Gọi thẳng chức năng Tạo mới khi không có quyền Thêm", "P0",
     "Tài khoản không có quyền Thêm danh mục gói bảo dưỡng",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Tạo mới gói bảo dưỡng, bỏ qua giao diện\n"
     "2. Đăng nhập lại bằng tài khoản có quyền và tìm gói vừa gửi",
     "Mã gói: QA-BYPASS-01",
     "- Hệ thống từ chối, báo không có quyền\n- Danh sách không phát sinh gói QA-BYPASS-01"),

    ("07", "Gọi thẳng chức năng Sửa khi không có quyền Sửa", "P0",
     "Tài khoản không có quyền Sửa; gói BDT001 đang Hoạt động",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Sửa cho gói BDT001\n"
     "2. Mở lại chi tiết BDT001 và đối chiếu dữ liệu",
     "Gói: BDT001",
     "- Hệ thống từ chối, báo không có quyền\n- Dữ liệu gói BDT001 không đổi"),

    ("08", "Gọi thẳng chức năng Xóa khi không có quyền Xóa", "P0",
     "Tài khoản không có quyền Xóa; có gói chưa được sử dụng",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Xóa cho gói đó\n2. Làm mới danh sách",
     "—",
     "- Hệ thống từ chối, báo không có quyền\n- Gói vẫn còn trong danh sách"),

    ("09", "Chưa đăng nhập thì không vào được màn hình", "P0",
     "Trình duyệt ẩn danh, chưa đăng nhập",
     "1. Gõ thẳng /customer-care/services vào thanh địa chỉ\n2. Nhấn Enter",
     "—",
     "- Hệ thống chuyển sang màn Đăng nhập, không hiển thị dữ liệu nào"),

    ("10", "Xem lịch sử không cần quyền riêng", "P1",
     "Tài khoản không có quyền nào của màn",
     "1. Mở menu ba chấm ở một dòng\n2. Bấm Lịch sử",
     "—",
     "- Cửa sổ Lịch sử thay đổi mở bình thường"),
]

# ============================================================ SECTIONS
S1 = [
    (1, "Vào màn hình từ menu", "P0",
     "Đã đăng nhập; danh mục có 221 gói bảo dưỡng",
     "1. Vào phân hệ Chăm sóc khách hàng\n2. Mở nhóm menu Danh mục\n"
     "3. Bấm Danh mục gói bảo dưỡng",
     "—",
     "- Tiêu đề trang hiển thị \"Danh mục gói bảo dưỡng\"\n"
     "- Khối Bộ lọc danh sách nằm trên, bảng nằm dưới\n"
     "- Dòng thống kê hiện \"Hiển thị 1–10 / 221\""),

    (2, "Bố cục mặc định của bảng", "P0",
     "Tài khoản chưa từng chỉnh Cấu hình cột ở màn này",
     "1. Vào màn hình\n2. Quan sát tiêu đề các cột từ trái sang phải",
     "—",
     "- Hiển thị sẵn: STT, Mã, Tên gói bảo dưỡng, Người tạo, Ngày tạo, Trạng thái, Hành động\n"
     "- Các cột Công ty quản lý gói bảo dưỡng, Người sửa, Ngày sửa mặc định KHÔNG hiển thị\n"
     "- Cột Hành động nằm cuối bảng"),

    (3, "Thanh công cụ trên bảng", "P0",
     "Tài khoản có đủ 3 quyền của màn",
     "1. Quan sát góc phải phía trên bảng",
     "—",
     "- Nút Tạo mới (nền xanh dương, dấu cộng)\n- Nút Xuất Excel (nền xanh lá)\n"
     "- Nút Cấu hình cột hiển thị (biểu tượng cột)\n"
     "- Không có nút Nhập Excel"),

    (4, "Bấm mã gói để vào chi tiết", "P0",
     "Danh sách đang hiển thị gói BDT001",
     "1. Bấm vào mã BDT001",
     "Gói: BDT001",
     "- Chuyển sang màn Chi tiết gói bảo dưỡng, tiêu đề \"Chi tiết gói bảo dưỡng: BDT001\"\n"
     "- Đường dẫn trên trình duyệt đổi sang trang chi tiết (mở được tab mới bằng chuột phải)"),

    (5, "Biểu tượng chữ i hiển thị giá theo cấp", "P0",
     "Gói BDT001 đã khai cấp bảo dưỡng và định mức công",
     "1. Rê chuột vào biểu tượng chữ i cạnh tên gói BDT001",
     "—",
     "- Hiện bảng nhỏ liệt kê từng cấp bảo dưỡng kèm giá bán tương ứng\n"
     "- Số tiền có dấu phân cách hàng nghìn"),

    (6, "Gói chưa khai cấp thì không có biểu tượng chữ i", "P1",
     "Có gói chưa khai nội dung kiểm tra / cấp bảo dưỡng",
     "1. Tìm gói chưa khai cấp\n2. Quan sát cột Tên gói bảo dưỡng",
     "—",
     "- Không hiện biểu tượng chữ i, chỉ hiện tên gói"),

    (7, "Hiển thị nhãn trạng thái", "P0",
     "Danh sách có cả gói Hoạt động và gói Khóa",
     "1. Quan sát cột Trạng thái",
     "—",
     "- Gói đang dùng: nhãn \"Hoạt động\" nền xanh\n- Gói đã khóa: nhãn \"Khóa\" nền đỏ"),

    (8, "Bộ nút hành động của gói Hoạt động chưa được sử dụng", "P0",
     "Gói \"tên gói bảo dưỡng test 001\" đang Hoạt động và chưa gắn hàng hoá, chưa dùng ở báo giá",
     "1. Quan sát cột Hành động của dòng đó\n2. Mở menu ba chấm",
     "—",
     "- 2 nút ngoài: Sửa (bút chì), Xóa (thùng rác đỏ)\n"
     "- Menu ba chấm: Nhân bản, In, Lịch sử"),

    (9, "Bộ nút hành động của gói Hoạt động ĐÃ được sử dụng", "P0",
     "Gói BDT001 đã gắn hàng hoá hoặc đã dùng ở báo giá dịch vụ",
     "1. Quan sát cột Hành động của dòng BDT001",
     "Gói: BDT001",
     "- Có nút Sửa và nút Nhân bản\n- KHÔNG có nút Xóa (ẩn hẳn, không phải làm mờ)"),

    (10, "Bộ nút hành động của gói đang Khóa", "P0",
     "Gói GBDT007 đang ở trạng thái Khóa",
     "1. Quan sát cột Hành động của dòng GBDT007",
     "Gói: GBDT007",
     "- Có nút Mở khóa (ổ khoá mở) và Nhân bản\n- KHÔNG có Sửa, KHÔNG có Xóa\n"
     "- Menu ba chấm vẫn có In và Lịch sử"),

    (11, "Trạng thái danh sách rỗng", "P1",
     "Danh mục có 221 gói",
     "1. Nhập vào ô tìm nhanh chuỗi không tồn tại\n2. Nhấn Enter",
     "Từ khoá: zzz-khong-ton-tai",
     "- Bảng hiện \"Không có dữ liệu phù hợp bộ lọc.\"\n- Dòng thống kê hiện 0 bản ghi"),

    (12, "Hiệu ứng chờ khi tải danh sách", "P2",
     "Đường truyền bình thường",
     "1. Bấm Làm mới\n2. Quan sát vùng bảng",
     "—",
     "- Có hiệu ứng đang tải; tải xong hiệu ứng biến mất, không nhấp nháy bảng trắng"),
]

S2 = [
    (1, "Tìm nhanh theo tên gói", "P0",
     "Danh mục có gói tên \"gói bảo dưỡng test 007\"",
     "1. Nhập từ khoá vào ô \"Tìm theo tên hoặc mã gói bảo dưỡng...\"\n2. Nhấn Enter",
     "Từ khoá: test 007",
     "- Kết quả chỉ gồm gói có tên hoặc mã chứa chuỗi test 007"),

    (2, "Tìm nhanh theo mã gói", "P0",
     "Danh mục có 6 gói mã bắt đầu bằng GBDT",
     "1. Nhập từ khoá\n2. Nhấn Enter",
     "Từ khoá: GBDT",
     "- Kết quả gồm 6 gói có mã chứa GBDT\n- Dòng thống kê hiện \"Hiển thị 1–6 / 6\""),

    (3, "Tìm nhanh tự chạy sau khi ngừng gõ", "P0",
     "Đang ở màn danh sách",
     "1. Gõ từ khoá vào ô tìm nhanh\n2. KHÔNG nhấn Enter, chờ khoảng 1 giây",
     "Từ khoá: GBDT",
     "- Danh sách tự lọc sau khi ngừng gõ khoảng nửa giây\n"
     "- ⚠️ Khác các màn danh mục khác: ô này tự tìm, không bắt buộc bấm Tìm kiếm"),

    (4, "Gõ nhanh nhiều ký tự chỉ gọi một lần", "P1",
     "Đang ở màn danh sách",
     "1. Gõ liên tục 6 ký tự thật nhanh\n2. Quan sát số lần bảng tải lại",
     "Từ khoá: GBDT00",
     "- Bảng chỉ tải lại MỘT lần sau khi ngừng gõ, không tải lại theo từng ký tự"),

    (5, "Thứ tự kết quả theo độ khớp", "P0",
     "Danh mục có gói mã \"01\" và nhiều gói mã chứa \"01\" ở giữa",
     "1. Nhập từ khoá 01\n2. Quan sát thứ tự các dòng kết quả",
     "Từ khoá: 01",
     "- Gói có mã trùng khít \"01\" đứng đầu\n"
     "- Kế đến là gói bắt đầu bằng 01, cuối cùng mới tới gói chỉ chứa 01 ở giữa"),

    (6, "Tìm nhanh không phân biệt chữ hoa chữ thường", "P1",
     "Danh mục có gói mã GBDT005",
     "1. Nhập gbdt005, chờ lọc\n2. Nhập lại GBDT005",
     "Từ khoá: gbdt005 → GBDT005",
     "- Hai lần cho cùng kết quả"),

    (7, "Lọc theo trạng thái Hoạt động", "P0",
     "Danh sách có cả gói Hoạt động và Khóa",
     "1. Chọn ô Trạng thái = Hoạt động",
     "Trạng thái: Hoạt động",
     "- Danh sách tự lọc ngay khi chọn\n- Mọi dòng đều mang nhãn Hoạt động"),

    (8, "Lọc theo trạng thái Khóa", "P0",
     "Có ít nhất 5 gói đang Khóa",
     "1. Chọn ô Trạng thái = Khóa",
     "Trạng thái: Khóa",
     "- Kết quả chỉ gồm gói đang Khóa\n"
     "- ⚠️ Trạng thái Khóa lưu giá trị 0 — kiểm kỹ có bỏ sót dòng nào không"),

    (9, "Lọc theo người tạo", "P0",
     "Danh mục có gói do nhiều người tạo",
     "1. Chọn ô Người tạo = một nhân viên cụ thể",
     "Người tạo: DNS Admin",
     "- Kết quả chỉ gồm gói do người đó tạo\n- Cột Người tạo của mọi dòng đều là người đã chọn"),

    (10, "Kết hợp từ khoá và trạng thái", "P0",
     "Từ khoá GBDT ra 6 gói, trong đó có cả Hoạt động và Khóa",
     "1. Nhập từ khoá GBDT\n2. Chọn Trạng thái = Khóa",
     "Từ khoá: GBDT | Trạng thái: Khóa",
     "- ⚠️ Kiểm TỪNG DÒNG: mỗi dòng phải vừa khớp từ khoá vừa đang Khóa"),

    (11, "Kết hợp trạng thái và người tạo", "P1",
     "Có gói Hoạt động do DNS Admin tạo",
     "1. Chọn Trạng thái = Hoạt động\n2. Chọn Người tạo = DNS Admin",
     "—",
     "- Kết quả thoả mãn đồng thời hai điều kiện"),

    (12, "Nút Tìm kiếm chạy ngay không chờ", "P1",
     "Vừa gõ xong từ khoá",
     "1. Gõ từ khoá\n2. Bấm ngay nút Tìm kiếm",
     "Từ khoá: GBDT",
     "- Danh sách lọc ngay, không phải chờ hết thời gian trễ"),

    (13, "Nút Làm mới xoá toàn bộ điều kiện lọc", "P0",
     "Đang lọc từ khoá + trạng thái + người tạo",
     "1. Bấm nút Làm mới",
     "—",
     "- Cả 3 ô lọc trở về trống\n- Danh sách tải lại đủ 221 gói"),

    (14, "Lọc xong luôn quay về trang 1", "P1",
     "Đang đứng ở trang 3",
     "1. Sang trang 3\n2. Chọn Trạng thái = Khóa",
     "—",
     "- Kết quả hiển thị từ trang 1"),

    (15, "Từ khoá chứa ký tự đặc biệt", "P1",
     "Danh mục có 221 gói",
     "1. Nhập ký tự % vào ô tìm nhanh\n2. Chờ lọc",
     "Từ khoá: %",
     "- Không được trả về toàn bộ 221 gói\n"
     "- Kết quả rỗng hoặc chỉ gồm gói thật sự có ký tự % trong tên/mã"),

    (16, "Từ khoá 1 ký tự", "P2",
     "Danh mục có 221 gói",
     "1. Nhập 1 ký tự vào ô tìm nhanh",
     "Từ khoá: 0",
     "- Vẫn lọc theo chuỗi đó\n"
     "- ⚠️ Với 1 ký tự hệ thống không xếp theo độ khớp, thứ tự về mặc định — không phải lỗi"),

    (17, "Hệ thống ghi nhớ bộ lọc trong 10 phút", "P1",
     "Đang lọc Trạng thái = Khóa",
     "1. Lọc Trạng thái = Khóa\n2. Sang màn khác\n3. Trong 10 phút quay lại màn này",
     "—",
     "- Bộ lọc cũ vẫn còn, danh sách vẫn đang lọc"),

    (18, "Rời màn khi đang chờ lọc", "P2",
     "Vừa gõ từ khoá, chưa lọc xong",
     "1. Gõ từ khoá rồi bấm ngay sang màn khác",
     "—",
     "- Không xuất hiện lỗi trên màn mới, không có yêu cầu tải dữ liệu treo lại"),
]

S3 = [
    (1, "Phân trang mặc định", "P0",
     "Danh mục có 221 gói",
     "1. Vào màn hình\n2. Quan sát vùng dưới bảng",
     "—",
     "- 10 dòng/trang, có 23 trang\n- Dòng thống kê: \"Hiển thị 1–10 / 221\""),

    (2, "Chuyển trang", "P0",
     "Danh sách có nhiều trang",
     "1. Bấm số trang 2",
     "—",
     "- Hiển thị 10 dòng tiếp theo, cột STT bắt đầu từ 11"),

    (3, "Nhảy tới trang cuối", "P1",
     "Danh mục 221 gói, 10 dòng/trang",
     "1. Bấm nút về trang cuối",
     "—",
     "- Trang cuối hiện 1 dòng\n- Dòng thống kê: \"Hiển thị 221–221 / 221\""),

    (4, "Đổi số dòng/trang", "P0",
     "Danh mục 221 gói",
     "1. Chọn Số dòng/trang = 50",
     "Số dòng/trang: 50",
     "- Hiện 50 dòng, quay về trang 1, tổng số trang giảm còn 5"),

    (5, "Danh sách mức số dòng/trang", "P2",
     "Đang ở màn danh sách",
     "1. Mở ô Số dòng/trang",
     "—",
     "- Có đúng 5 lựa chọn: 5, 10, 20, 50, 100"),

    (6, "Phân trang giữ nguyên bộ lọc", "P0",
     "Đang lọc Trạng thái = Hoạt động, kết quả nhiều hơn 1 trang",
     "1. Lọc Trạng thái = Hoạt động\n2. Sang trang 2\n3. Kiểm tra nhãn trạng thái mọi dòng",
     "—",
     "- Trang 2 vẫn chỉ chứa gói Hoạt động"),

    (7, "Không trùng, không sót dữ liệu giữa các trang", "P0",
     "Lọc còn 6 gói, đặt 5 dòng/trang",
     "1. Lọc từ khoá GBDT, chọn 5 dòng/trang\n2. Ghi lại mã ở trang 1 và trang 2",
     "—",
     "- Tổng 6 mã, không mã nào lặp lại giữa 2 trang"),

    (8, "Thứ tự mặc định của danh sách", "P0",
     "Vừa tạo một gói mới hôm nay",
     "1. Tạo gói mới\n2. Quay về danh sách, không bấm sắp xếp",
     "—",
     "- Gói vừa tạo nằm ở dòng đầu tiên (mới nhất trước theo Ngày tạo)"),

    (9, "Sắp xếp theo Mã", "P0",
     "Danh sách có nhiều mã khác nhau",
     "1. Bấm tiêu đề cột Mã\n2. Quan sát thứ tự\n3. Bấm lần nữa",
     "—",
     "- Lần 1 tăng dần, lần 2 giảm dần; dữ liệu thực sự đổi thứ tự"),

    (10, "Sắp xếp theo Tên gói bảo dưỡng", "P0",
     "Danh sách có nhiều tên khác nhau",
     "1. Bấm tiêu đề cột Tên gói bảo dưỡng",
     "—",
     "- Xếp đúng theo bảng chữ cái, bấm lần 2 đảo chiều"),

    (11, "Sắp xếp theo Ngày tạo", "P1",
     "Danh sách có bản ghi tạo nhiều ngày khác nhau",
     "1. Bấm tiêu đề cột Ngày tạo",
     "—",
     "- Xếp đúng theo ngày giờ tạo, bấm lần 2 đảo chiều"),

    (12, "Sắp xếp theo Ngày sửa", "P1",
     "Đã bật cột Ngày sửa ở Cấu hình cột",
     "1. Bật cột Ngày sửa\n2. Bấm tiêu đề cột đó",
     "—",
     "- Xếp đúng theo ngày giờ sửa gần nhất"),

    (13, "Sắp xếp kết hợp với tìm kiếm", "P0",
     "Đang tìm từ khoá GBDT (6 kết quả)",
     "1. Nhập từ khoá GBDT\n2. Bấm sắp xếp theo Mã",
     "—",
     "- Kết quả vẫn đúng 6 gói và đã xếp theo mã\n"
     "- ⚠️ Khi user tự bấm sắp xếp thì thứ tự theo độ khớp bị bỏ qua — đúng thiết kế"),

    (14, "Cột không cho sắp xếp", "P2",
     "Đang ở màn danh sách",
     "1. Bấm tiêu đề cột Trạng thái, Người tạo, Công ty quản lý",
     "—",
     "- Các cột này không có biểu tượng sắp xếp, bấm vào không xảy ra gì"),

    (15, "Mở cửa sổ Cấu hình cột", "P0",
     "Đang ở màn danh sách",
     "1. Bấm nút biểu tượng cột",
     "—",
     "- Cửa sổ \"Tuỳ chỉnh cột\" liệt kê đủ 10 cột\n- Có nút Lưu và Đóng"),

    (16, "Cột bị khoá trong Cấu hình cột", "P0",
     "Cửa sổ Tuỳ chỉnh cột đang mở",
     "1. Thử bỏ tích STT, Mã, Hành động",
     "—",
     "- Ba dòng này có biểu tượng ổ khoá, không bỏ tích được"),

    (17, "Bật thêm cột và lưu", "P0",
     "Cột Công ty quản lý gói bảo dưỡng đang tắt",
     "1. Tích cột Công ty quản lý gói bảo dưỡng\n2. Bấm Lưu\n3. Tải lại trang",
     "—",
     "- Bảng hiện thêm cột đó và giữ nguyên sau khi tải lại trang"),

    (18, "Đóng cửa sổ Cấu hình cột không lưu", "P1",
     "Đã tích thêm cột nhưng chưa Lưu",
     "1. Tích thêm 1 cột\n2. Bấm Đóng",
     "—",
     "- Bảng KHÔNG đổi"),
]

S4 = [
    (1, "Mở màn Thêm gói bảo dưỡng", "P0",
     "Tài khoản có quyền Thêm danh mục gói bảo dưỡng",
     "1. Bấm nút Tạo mới ở màn danh sách",
     "—",
     "- Chuyển sang TRANG RIÊNG (không phải cửa sổ), tiêu đề \"Thêm gói bảo dưỡng\"\n"
     "- Có 5 khối: Thông tin chung · Danh mục kiểm tra bảo dưỡng định kỳ · Giá vốn theo công ty · "
     "Áp dụng cho hàng hóa · File đính kèm (PDF)\n"
     "- Chân trang có nút Lưu và Quay lại"),

    (2, "Giá trị điền sẵn khi tạo mới", "P0",
     "Vừa mở màn Thêm gói bảo dưỡng",
     "1. Quan sát toàn bộ các ô",
     "—",
     "- Tên, Mã, Định mức đàm phán giá, VAT, Ghi chú, Hệ số giá bán: trống\n"
     "- Công ty quản lý gói bảo dưỡng: điền sẵn công ty của người đăng nhập\n"
     "- KHÔNG có ô Trạng thái (gói mới luôn là Hoạt động)\n"
     "- Bảng nội dung kiểm tra trống, hiện dòng \"Không có danh mục kiểm tra bảo dưỡng\"\n"
     "- Khối Giá vốn theo công ty liệt kê sẵn 8 công ty, hệ số mặc định 1"),

    (3, "Thêm dòng nội dung kiểm tra bảo dưỡng", "P0",
     "Đang ở màn Thêm gói bảo dưỡng",
     "1. Bấm \"+ Thêm danh mục kiểm tra bảo dưỡng\"\n2. Nhập Nội dung, chọn ĐVT, nhập SL",
     "Nội dung: Kiểm tra dầu máy | ĐVT: Bộ | SL: 1",
     "- Bảng thêm 1 dòng có STT = 1\n- Ba ô Nội dung, ĐVT, SL đều có dấu sao đỏ"),

    (4, "Thêm cột cấp bảo dưỡng", "P0",
     "Bảng nội dung kiểm tra đã có ít nhất 1 dòng",
     "1. Bấm dấu + ở góc phải tiêu đề bảng\n2. Chọn một cấp bảo dưỡng cho cột vừa thêm",
     "Cấp: Bảo dưỡng máy làm sạch buồng đốt",
     "- Bảng có thêm một cột mang tên cấp vừa chọn\n"
     "- Dưới bảng xuất hiện các dòng Định mức công, Hệ số công nghệ, Giá vốn, Giá công thức, "
     "Giá bán cơ sở, Gợi ý hàng hoá cho cột đó"),

    (5, "Chọn trùng cấp bảo dưỡng ở hai cột", "P0",
     "Đã có cột cấp \"Bảo dưỡng máy làm sạch buồng đốt\"",
     "1. Thêm cột thứ hai\n2. Chọn đúng cấp đã dùng ở cột trước",
     "Cấp: Bảo dưỡng máy làm sạch buồng đốt",
     "- Hệ thống cảnh báo \"Cấp bảo dưỡng này đã được chọn ở cột khác\"\n"
     "- Cột thứ hai KHÔNG nhận cấp trùng"),

    (6, "Chọn ghi chú kiểm tra cho ô giao nhau", "P0",
     "Bảng đã có 1 dòng nội dung và 1 cột cấp",
     "1. Bấm vào ô giao giữa dòng nội dung và cột cấp\n2. Chọn một hoặc nhiều ghi chú kiểm tra",
     "Ghi chú: DK, VS",
     "- Ô hiển thị ký hiệu của các ghi chú đã chọn\n- Chọn được nhiều ghi chú trong cùng một ô"),

    (7, "Xoá dòng nội dung kiểm tra", "P1",
     "Bảng đã có 2 dòng nội dung",
     "1. Bấm biểu tượng xoá ở cuối dòng thứ hai",
     "—",
     "- Dòng đó biến mất, STT các dòng còn lại đánh lại liên tục"),

    (8, "Xoá cột cấp bảo dưỡng", "P1",
     "Bảng đã có 2 cột cấp",
     "1. Bấm biểu tượng xoá cột ở tiêu đề cột thứ hai",
     "—",
     "- Cột và các dòng thông số tương ứng biến mất"),

    (9, "Nhập Định mức công và xem giá tự tính", "P0",
     "Đã có 1 cột cấp; công ty quản lý có đơn giá công 700.000; hệ số giá bán gói = 2",
     "1. Nhập Hệ số giá bán gói bảo dưỡng = 2\n2. Nhập Định mức công = 2\n"
     "3. Nhập Hệ số công nghệ = 2\n4. Quan sát các dòng Giá vốn, Giá công thức, Giá bán cơ sở",
     "Định mức công: 2 | Hệ số công nghệ: 2 | Hệ số giá bán: 2",
     "- Giá vốn = 700.000 × 2 × 2 = 2.800.000\n"
     "- Giá công thức = 2.800.000 × 2 = 5.600.000\n"
     "- Giá bán cơ sở mặc định bằng Giá công thức = 5.600.000 và vẫn sửa tay được"),

    (10, "Sửa tay Giá bán cơ sở", "P0",
     "Đã có giá công thức tự tính",
     "1. Sửa ô Giá bán cơ sở thành một số khác\n2. Quan sát bảng Giá bán theo công ty",
     "Giá bán cơ sở: 9.000.000",
     "- Giá bán theo từng công ty tính lại theo giá cơ sở mới × hệ số công ty đó"),

    (11, "Nhập hệ số giá bán theo công ty", "P0",
     "Khối Giá vốn theo công ty liệt kê 8 công ty",
     "1. Đổi Hệ số giá bán của một công ty thành 1,5\n2. Quan sát giá bán theo công ty đó",
     "Hệ số: 1,5",
     "- Giá bán của công ty đó = giá bán cơ sở × 1,5\n"
     "- ⚠️ Dấu phẩy là dấu thập phân — 1,5 phải hiểu là một phẩy năm"),

    (12, "Chọn hàng hoá áp dụng", "P0",
     "Đang ở màn Thêm gói bảo dưỡng",
     "1. Bấm nút \"Chọn hàng hóa\"\n2. Tìm và tích chọn 2 hàng hoá\n3. Bấm \"Thêm ... hàng hoá\"",
     "—",
     "- Cửa sổ \"Chọn hàng hóa áp dụng\" mở kèm bộ lọc và ô tìm kiếm\n"
     "- Sau khi thêm, bảng Áp dụng cho hàng hóa hiện 2 dòng kèm hình ảnh, tên hàng, mã hàng"),

    (13, "Chọn theo nhóm hàng", "P1",
     "Đang ở màn Thêm gói bảo dưỡng",
     "1. Bấm nút \"Chọn nhóm hàng\"\n2. Chọn một nhóm hàng",
     "—",
     "- Toàn bộ hàng hoá của nhóm được thêm vào bảng Áp dụng cho hàng hóa"),

    (14, "Bỏ hàng hoá đã chọn", "P1",
     "Bảng Áp dụng cho hàng hóa đã có ít nhất 2 dòng",
     "1. Bấm biểu tượng xoá ở một dòng hàng hoá",
     "—",
     "- Dòng đó biến mất khỏi bảng"),

    (15, "Đính kèm file PDF", "P0",
     "Có sẵn file quy_trinh.pdf",
     "1. Bấm ô \"+ Thêm file\" ở khối File đính kèm (PDF)\n2. Chọn file quy_trinh.pdf",
     "File: quy_trinh.pdf",
     "- Tên file hiện trong khối đính kèm kèm nút bỏ file"),

    (16, "Đính kèm file không phải PDF", "P0",
     "Có sẵn file anh.png",
     "1. Bấm Thêm file\n2. Chọn anh.png\n3. Bấm Lưu",
     "File: anh.png",
     "- Hệ thống báo \"Chỉ nhận file PDF\"\n- Không lưu gói"),

    (17, "Lưu gói mà chưa đính kèm file", "P0",
     "Đã nhập đủ thông tin bắt buộc nhưng chưa đính kèm file nào",
     "1. Nhập đủ Tên, Mã, Công ty quản lý, nội dung kiểm tra\n2. Bấm Lưu",
     "—",
     "- Hệ thống báo \"Bắt buộc phải đính kèm ít nhất 1 file PDF\"\n"
     "- Khối File đính kèm viền đỏ, không lưu gói\n"
     "- ⚠️ Đây là quy định riêng của phần mềm mới, phần mềm cũ không bắt buộc"),

    (18, "Tạo mới đầy đủ và lưu thành công", "P0",
     "Danh mục chưa có mã QA001",
     "1. Nhập Tên, Mã, Công ty quản lý\n2. Thêm 1 dòng nội dung kiểm tra + 1 cột cấp + chọn ghi "
     "chú\n3. Nhập Định mức công\n4. Đính kèm 1 file PDF\n5. Bấm Lưu",
     "Tên: Gói kiểm thử QA001 | Mã: qa001 | ĐVT: Bộ | SL: 1 | Định mức công: 2",
     "- Hệ thống báo \"Tạo gói bảo dưỡng thành công\"\n"
     "- Quay về danh sách, gói QA001 nằm ở đầu, trạng thái Hoạt động\n"
     "- ⚠️ Mã hiển thị IN HOA: QA001 dù nhập chữ thường"),

    (19, "Bỏ trống toàn bộ rồi bấm Lưu", "P0",
     "Vừa mở màn Thêm gói bảo dưỡng",
     "1. Bấm ngay nút Lưu",
     "—",
     "- Ô Tên gói bảo dưỡng viền đỏ kèm \"Bắt buộc phải nhập\"\n"
     "- Màn hình không rời trang, không tạo bản ghi"),

    (20, "Trùng tên gói bảo dưỡng", "P0",
     "Danh mục đã có gói tên \"BD test 001\"",
     "1. Nhập Tên trùng, Mã mới và các thông tin bắt buộc\n2. Bấm Lưu",
     "Tên: BD test 001 | Mã: QA002",
     "- Ô Tên hiện lỗi \"Đã tồn tại\"\n- Không tạo bản ghi"),

    (21, "Trùng mã gói bảo dưỡng", "P0",
     "Danh mục đã có mã BDT001",
     "1. Nhập Mã trùng, Tên mới và các thông tin bắt buộc\n2. Bấm Lưu",
     "Mã: BDT001 | Tên: Gói kiểm thử QA003",
     "- Ô Mã hiện lỗi \"Đã tồn tại\"\n- Không tạo bản ghi"),

    (22, "Trùng mã chỉ khác chữ hoa chữ thường", "P0",
     "Danh mục đã có mã BDT001",
     "1. Nhập mã bdt001 (chữ thường) và thông tin bắt buộc\n2. Bấm Lưu",
     "Mã: bdt001",
     "- Vẫn bị báo \"Đã tồn tại\"\n"
     "- ⚠️ Mã được chuyển in hoa trước khi kiểm tra trùng nên bdt001 và BDT001 là một"),

    (23, "Thiếu công ty quản lý", "P1",
     "Đang ở màn Thêm gói bảo dưỡng",
     "1. Xoá trắng ô Công ty quản lý gói bảo dưỡng\n2. Nhập các ô còn lại, bấm Lưu",
     "Công ty quản lý: (để trống)",
     "- Ô Công ty quản lý hiện lỗi \"Bắt buộc phải nhập\""),

    (24, "Thiếu Định mức công của cấp", "P0",
     "Đã thêm dòng nội dung và cột cấp nhưng chưa nhập Định mức công",
     "1. Bỏ trống Định mức công\n2. Nhập các ô khác, bấm Lưu",
     "Định mức công: (để trống)",
     "- Hiện lỗi \"Bắt buộc phải nhập\" tại ô Định mức công"),

    (25, "Thiếu ghi chú kiểm tra ở ô giao nhau", "P0",
     "Đã có dòng nội dung và cột cấp nhưng ô giao nhau để trống",
     "1. Không chọn ghi chú kiểm tra nào\n2. Bấm Lưu",
     "—",
     "- Hiện lỗi \"Bắt buộc phải nhập\" ở ô nội dung kiểm tra của cấp đó"),

    (26, "Thiếu ĐVT hoặc SL của dòng nội dung", "P0",
     "Đã thêm dòng nội dung",
     "1. Bỏ trống ĐVT (hoặc SL)\n2. Bấm Lưu",
     "—",
     "- Ô bỏ trống hiện lỗi \"Bắt buộc phải nhập\""),

    (27, "Bấm Lưu nhiều lần liên tiếp", "P0",
     "Đã nhập đủ dữ liệu hợp lệ",
     "1. Bấm nút Lưu 3 lần thật nhanh\n2. Về danh sách và đếm số gói vừa tạo",
     "Mã: QA004",
     "- Chỉ tạo ra ĐÚNG 1 gói QA004"),

    (28, "Bấm Quay lại khi đang nhập dở", "P1",
     "Đã nhập Tên gói nhưng chưa lưu",
     "1. Nhập Tên gói\n2. Bấm nút Quay lại",
     "—",
     "- Hệ thống hỏi lại \"Thông tin chưa lưu\" trước khi rời trang\n"
     "- Chọn ở lại thì dữ liệu còn nguyên; chọn rời đi thì về danh sách và bỏ dữ liệu"),

    (29, "Gói mới tạo dùng được ngay ở báo giá dịch vụ", "P0",
     "Vừa tạo gói QA001 trạng thái Hoạt động",
     "1. Tạo gói QA001\n2. Vào màn báo giá dịch vụ, mở ô chọn gói bảo dưỡng\n3. Tìm QA001",
     "Gói: QA001",
     "- QA001 có trong danh sách chọn của màn báo giá dịch vụ"),

    (30, "Gói đang Khóa không xuất hiện khi chọn ở màn khác", "P1",
     "Gói QA001 vừa bị khóa",
     "1. Khóa gói QA001\n2. Vào màn báo giá dịch vụ, mở ô chọn gói bảo dưỡng",
     "—",
     "- Ghi nhận kết quả thực tế: gói đã khóa có còn chọn được hay không\n"
     "- ⚠️ Nghiệp vụ mong đợi gói đã khóa không chọn mới được; nếu vẫn chọn được thì báo lại"),
]

S5 = [
    (1, "Mở màn Sửa từ danh sách", "P0",
     "Gói BDT001 đang Hoạt động, tài khoản có quyền Sửa",
     "1. Bấm nút Sửa ở dòng BDT001",
     "Gói: BDT001",
     "- Chuyển sang trang \"Sửa gói bảo dưỡng\"\n"
     "- Toàn bộ 5 khối đã nạp sẵn dữ liệu hiện tại\n- Có thêm ô Trạng thái so với màn Thêm mới"),

    (2, "Ô Trạng thái chỉ có ở màn Sửa", "P0",
     "So sánh màn Thêm mới và màn Sửa",
     "1. Mở màn Thêm mới, quan sát khối Thông tin chung\n2. Mở màn Sửa, quan sát khối Thông tin "
     "chung",
     "—",
     "- Màn Thêm mới KHÔNG có ô Trạng thái\n- Màn Sửa CÓ ô Trạng thái với 2 lựa chọn Hoạt động / "
     "Khóa"),

    (3, "Sửa và lưu thành công", "P0",
     "Gói QA001 vừa tạo",
     "1. Bấm Sửa QA001\n2. Đổi Tên gói và Ghi chú\n3. Bấm Lưu",
     "Tên: Gói kiểm thử QA001 - đã sửa | Ghi chú: cập nhật lần 1",
     "- Hệ thống báo \"Cập nhật gói bảo dưỡng thành công\"\n"
     "- Quay về danh sách, dòng đó hiện tên mới\n- Cột Người sửa và Ngày sửa cập nhật"),

    (4, "Sửa trùng tên với gói khác", "P0",
     "Đang sửa QA001; danh mục đã có gói \"BD test 001\"",
     "1. Đổi Tên thành BD test 001\n2. Bấm Lưu",
     "Tên: BD test 001",
     "- Ô Tên hiện lỗi \"Đã tồn tại\", không lưu"),

    (5, "Sửa giữ nguyên tên và mã của chính nó", "P0",
     "Đang sửa QA001",
     "1. Giữ nguyên Tên và Mã, chỉ đổi VAT\n2. Bấm Lưu",
     "VAT: 8",
     "- Lưu thành công, KHÔNG báo trùng với chính nó"),

    (6, "Thêm cột cấp mới khi sửa", "P1",
     "Gói QA001 đang có 1 cột cấp",
     "1. Bấm Sửa QA001\n2. Thêm 1 cột cấp mới, chọn ghi chú và nhập định mức công\n3. Bấm Lưu",
     "Cấp: Bảo dưỡng định kỳ cấp 2",
     "- Lưu thành công\n- Mở lại chi tiết thấy đủ 2 cột cấp"),

    (7, "Bỏ cột cấp CHƯA phát sinh báo giá", "P1",
     "Gói QA001 có 2 cột cấp, cấp thứ hai chưa dùng ở báo giá dịch vụ nào",
     "1. Bấm Sửa QA001\n2. Xoá cột cấp thứ hai\n3. Bấm Lưu",
     "—",
     "- Lưu thành công, chi tiết chỉ còn 1 cột cấp"),

    (8, "Bỏ cột cấp ĐÃ phát sinh báo giá", "P0",
     "Gói BDT001 có cấp đã được dùng trong báo giá dịch vụ",
     "1. Bấm Sửa BDT001\n2. Xoá cột cấp đã dùng\n3. Bấm Lưu",
     "—",
     "- Hệ thống chặn kèm thông báo không cho bỏ cấp đã phát sinh báo giá\n"
     "- Dữ liệu gói giữ nguyên, không mất nội dung kiểm tra"),

    (9, "Sửa gói đang Khóa từ danh sách", "P0",
     "Gói GBDT007 đang Khóa",
     "1. Quan sát cột Hành động của GBDT007",
     "—",
     "- Không có nút Sửa; muốn sửa phải Mở khóa trước"),

    (10, "Gõ thẳng đường dẫn sửa gói đang Khóa", "P0",
     "Gói GBDT007 đang Khóa",
     "1. Ghi lại đường dẫn trang sửa của gói đó\n2. Gõ thẳng đường dẫn vào thanh địa chỉ",
     "—",
     "- Hệ thống chặn, báo bản ghi đang bị khoá và yêu cầu mở khoá trước khi cập nhật\n"
     "- ⚠️ Chốt chặn nằm ở máy chủ, không chỉ ẩn nút ngoài danh sách"),

    (11, "Đổi trạng thái sang Khóa ngay trong màn Sửa", "P1",
     "Gói QA001 đang Hoạt động",
     "1. Bấm Sửa QA001\n2. Đổi ô Trạng thái sang Khóa\n3. Bấm Lưu",
     "Trạng thái: Khóa",
     "- Lưu thành công, dòng chuyển sang nhãn Khóa và mất nút Sửa"),

    (12, "Mở màn chi tiết", "P0",
     "Gói BDT001 đang hiển thị trên danh sách",
     "1. Bấm vào mã BDT001",
     "—",
     "- Tiêu đề \"Chi tiết gói bảo dưỡng: BDT001\"\n"
     "- Toàn bộ ô ở chế độ chỉ đọc, không gõ sửa được\n"
     "- Chân trang có các nút Sửa, In, Nhân bản, Quay lại"),

    (13, "Chi tiết hiển thị đủ 5 khối dữ liệu", "P0",
     "Gói BDT001 đã khai đủ nội dung",
     "1. Mở chi tiết BDT001\n2. Cuộn hết trang",
     "—",
     "- Hiện đủ: Thông tin chung, Danh mục kiểm tra bảo dưỡng định kỳ (kèm định mức công, hệ số "
     "công nghệ, giá vốn, giá công thức, giá bán cơ sở), Giá bán theo công ty, Áp dụng cho hàng "
     "hóa, File đính kèm"),

    (14, "Mở file đính kèm từ màn chi tiết", "P1",
     "Gói BDT001 có file PDF đính kèm",
     "1. Mở chi tiết BDT001\n2. Bấm vào tên file đính kèm",
     "—",
     "- File PDF mở ở tab mới và xem được nội dung"),

    (15, "Nút Sửa ở màn chi tiết của gói đang Khóa", "P1",
     "Gói GBDT007 đang Khóa",
     "1. Mở chi tiết GBDT007\n2. Quan sát chân trang",
     "—",
     "- Không có nút Sửa; vẫn còn In, Nhân bản, Quay lại"),

    (16, "Nhân bản gói bảo dưỡng", "P0",
     "Gói BDT001 đã khai đủ nội dung; tài khoản có quyền Thêm",
     "1. Mở menu ba chấm dòng BDT001\n2. Bấm Nhân bản",
     "—",
     "- Mở trang \"Sao chép gói bảo dưỡng\"\n"
     "- Toàn bộ dữ liệu của gói nguồn được điền sẵn, kể cả file đính kèm\n"
     "- ⚠️ Tên và Mã vẫn giữ nguyên của gói nguồn nên PHẢI sửa trước khi lưu"),

    (17, "Lưu bản nhân bản mà chưa đổi mã", "P0",
     "Đang ở trang Sao chép gói bảo dưỡng từ BDT001",
     "1. Không sửa gì\n2. Bấm Lưu",
     "—",
     "- Ô Tên và Mã đều báo \"Đã tồn tại\"\n- Không tạo bản ghi"),

    (18, "Lưu bản nhân bản sau khi đổi tên và mã", "P0",
     "Đang ở trang Sao chép từ BDT001",
     "1. Đổi Tên và Mã\n2. Bấm Lưu\n3. Mở chi tiết gói mới",
     "Tên: Gói kiểm thử nhân bản | Mã: QA010",
     "- Tạo gói mới thành công\n"
     "- Gói mới có đủ nội dung kiểm tra, cấp, hệ số công ty, hàng hoá và file đính kèm giống gói "
     "nguồn\n- Gói nguồn BDT001 không bị thay đổi"),

    (19, "Nhân bản từ gói đang Khóa", "P1",
     "Gói GBDT007 đang Khóa",
     "1. Mở menu ba chấm dòng GBDT007\n2. Bấm Nhân bản\n3. Đổi tên, mã rồi Lưu",
     "—",
     "- Vẫn nhân bản được\n- Gói mới ở trạng thái Hoạt động (không kế thừa trạng thái Khóa)"),

    (20, "Mở Sửa hai gói liên tiếp", "P0",
     "Danh sách có gói BDT001 và gói 111",
     "1. Bấm Sửa BDT001, xem dữ liệu, bấm Quay lại\n2. Bấm Sửa gói 111",
     "—",
     "- Trang sửa lần 2 hiển thị đúng dữ liệu gói 111, không sót dữ liệu gói trước"),

    (21, "Chuyển từ chi tiết sang sửa", "P0",
     "Đang ở màn chi tiết BDT001",
     "1. Bấm nút Sửa ở chân trang chi tiết",
     "—",
     "- Chuyển sang trang Sửa của đúng gói đó, các ô mở khoá nhập được"),

    (22, "Rời trang Sửa khi đã thay đổi mà chưa lưu", "P1",
     "Đang sửa QA001 và đã đổi một ô",
     "1. Đổi ô Ghi chú\n2. Bấm Quay lại",
     "—",
     "- Hệ thống hỏi lại \"Thông tin chưa lưu\"; chọn ở lại thì giữ nguyên dữ liệu đang sửa"),
]

S6 = [
    (1, "Mở hộp xác nhận Xóa", "P0",
     "Gói \"tên gói bảo dưỡng test 001\" đang Hoạt động và chưa được sử dụng",
     "1. Bấm nút Xóa ở dòng đó",
     "—",
     "- Hộp thoại \"Xác nhận xóa\"\n"
     "- Nội dung: \"Bạn có chắc chắn muốn xóa gói bảo dưỡng '<tên>'? Hành động này không thể hoàn "
     "tác.\"\n- Hai nút: Xóa và Hủy"),

    (2, "Xóa gói chưa được sử dụng", "P0",
     "Gói QA004 chưa gắn hàng hoá và chưa dùng ở báo giá dịch vụ",
     "1. Bấm Xóa ở dòng QA004\n2. Bấm nút Xóa trong hộp xác nhận",
     "Gói: QA004",
     "- Hệ thống báo \"Xóa gói bảo dưỡng thành công\"\n"
     "- Dòng biến mất khỏi danh sách, tổng số bản ghi giảm 1\n"
     "- Toàn bộ nội dung kiểm tra và cấp của gói cũng bị xoá theo"),

    (3, "Hủy thao tác Xóa", "P0",
     "Gói QA010 đang hiển thị",
     "1. Bấm Xóa ở dòng QA010\n2. Bấm nút Hủy",
     "—",
     "- Hộp thoại đóng, gói vẫn còn nguyên"),

    (4, "Gói đã gắn hàng hoá không có nút Xóa", "P0",
     "Gói BDT001 đã gắn ít nhất 1 hàng hoá",
     "1. Quan sát cột Hành động của dòng BDT001",
     "—",
     "- Không hiển thị nút Xóa"),

    (5, "Gói đã dùng ở báo giá dịch vụ không có nút Xóa", "P0",
     "Có gói đã được chọn trong ít nhất 1 báo giá dịch vụ",
     "1. Tìm gói đó trên danh sách\n2. Quan sát cột Hành động",
     "—",
     "- Không hiển thị nút Xóa"),

    (6, "Gọi thẳng chức năng Xóa với gói đã được sử dụng", "P0",
     "Gói BDT001 đã được sử dụng, nút Xóa đã bị ẩn",
     "1. Ghi lại định danh gói BDT001\n"
     "2. Dùng công cụ kiểm thử API gọi thẳng chức năng Xóa cho gói đó\n"
     "3. Làm mới danh sách và kiểm tra trạng thái",
     "Gói: BDT001",
     "- Hệ thống KHÔNG xoá mà chuyển gói sang trạng thái Khóa\n"
     "- Thông báo: \"Gói bảo dưỡng đang được sử dụng nên đã được chuyển sang trạng thái Khóa\"\n"
     "- ⚠️ Đây là hành vi giữ nguyên từ phần mềm cũ — dữ liệu không bị mất"),

    (7, "Mở khóa gói bảo dưỡng", "P0",
     "Gói GBDT007 đang Khóa; tài khoản có quyền Sửa",
     "1. Bấm nút Mở khóa ở dòng GBDT007\n2. Bấm nút Mở khóa trong hộp xác nhận",
     "Gói: GBDT007",
     "- Hộp thoại tiêu đề \"Xác nhận mở khóa\", nội dung nêu tên gói\n"
     "- Báo \"Mở khóa gói bảo dưỡng thành công\"\n"
     "- Dòng trở lại nhãn Hoạt động và hiện lại nút Sửa"),

    (8, "Hủy thao tác Mở khóa", "P1",
     "Gói GBDT003 đang Khóa",
     "1. Bấm Mở khóa\n2. Bấm nút Hủy",
     "—",
     "- Trạng thái giữ nguyên Khóa"),

    (9, "Gọi thẳng chức năng Mở khóa với gói đang Hoạt động", "P1",
     "Gói BDT001 đang Hoạt động",
     "1. Dùng công cụ kiểm thử API gọi thẳng chức năng Mở khóa cho gói đang Hoạt động",
     "—",
     "- Hệ thống báo \"Gói bảo dưỡng đang hoạt động, không cần mở khóa.\"\n"
     "- Không thay đổi dữ liệu"),

    (10, "Trạng thái sau khi tải lại trang", "P1",
     "Vừa mở khóa gói GBDT007",
     "1. Mở khóa GBDT007\n2. Nhấn F5 tải lại trang",
     "—",
     "- GBDT007 vẫn ở trạng thái Hoạt động (đã ghi thật)"),

    (11, "Lịch sử ghi nhận thao tác Mở khóa", "P0",
     "Vừa mở khóa gói GBDT007",
     "1. Mở cửa sổ Lịch sử của GBDT007",
     "—",
     "- Mốc mới nhất là \"Mở khóa\", chi tiết: Trạng thái: Khóa → Hoạt động"),

    (12, "Lịch sử ghi nhận việc chuyển sang Khóa khi xoá gói đang dùng", "P0",
     "Vừa thực hiện TC_06.006",
     "1. Mở cửa sổ Lịch sử của gói đó",
     "—",
     "- Có mốc \"Khóa\" với chi tiết Trạng thái: Hoạt động → Khóa\n"
     "- ⚠️ Không có mốc \"Xóa\" vì bản ghi không bị xoá"),

    (13, "Xóa gói vừa nhân bản", "P1",
     "Gói QA010 nhân bản từ BDT001, đã mang theo hàng hoá của gói nguồn",
     "1. Quan sát cột Hành động của QA010",
     "—",
     "- Nếu gói nhân bản mang theo hàng hoá thì KHÔNG có nút Xóa\n"
     "- ⚠️ Ghi nhận: nhân bản kéo theo cả điều kiện chặn xoá"),

    (14, "Xóa ở trang cuối chỉ còn 1 dòng", "P2",
     "Trang cuối chỉ còn 1 gói và gói đó xoá được",
     "1. Sang trang cuối\n2. Xóa dòng duy nhất",
     "—",
     "- Danh sách tự lùi về trang trước, không hiện trang trắng"),
]

S7 = [
    (1, "Mở cửa sổ Chọn trường xuất file", "P0",
     "Đang ở màn danh sách",
     "1. Bấm nút Xuất Excel",
     "—",
     "- Cửa sổ \"Chọn trường xuất file\" mở ra\n"
     "- Có 6 trường: Mã, Tên gói bảo dưỡng, Công ty quản lý, Trạng thái, Người tạo, Ngày tạo\n"
     "- Mặc định chọn sẵn cả 6 trường, dòng chữ ghi \"Đang chọn 6/6 trường\""),

    (2, "Xuất file với đủ 6 trường", "P0",
     "Cửa sổ Chọn trường xuất file đang mở",
     "1. Giữ nguyên 6 trường\n2. Bấm Xuất file",
     "—",
     "- Trình duyệt tải về file Danh_sach_goi_bao_duong.xlsx\n"
     "- File mở được bằng Excel, có đủ 6 cột theo đúng thứ tự trên cửa sổ"),

    (3, "Xuất file KHÔNG áp bộ lọc màn hình", "P0",
     "Đang lọc từ khoá GBDT, danh sách còn 6 dòng; danh mục có 221 gói",
     "1. Lọc từ khoá GBDT\n2. Bấm Xuất Excel, xuất file\n3. Mở file và đếm số dòng dữ liệu",
     "Từ khoá: GBDT",
     "- File chứa ĐỦ 221 gói, không phải 6 gói đang lọc\n"
     "- ⚠️ Đây là hành vi giữ nguyên từ phần mềm cũ — KHÔNG ghi Failed, nhưng phải báo lại nếu "
     "nghiệp vụ mong đợi khác"),

    (4, "Bỏ bớt trường xuất", "P0",
     "Cửa sổ Chọn trường xuất file đang mở",
     "1. Bỏ chọn Công ty quản lý và Người tạo\n2. Bấm Xuất file\n3. Mở file",
     "Trường xuất: Mã, Tên gói bảo dưỡng, Trạng thái, Ngày tạo",
     "- File chỉ có 4 cột đã chọn"),

    (5, "Thứ tự cột chạy theo thứ tự chọn", "P0",
     "Cửa sổ Chọn trường xuất file đang mở",
     "1. Bấm Bỏ chọn hết\n2. Chọn lần lượt: Trạng thái, Mã, Tên gói bảo dưỡng\n3. Xuất file",
     "Thứ tự chọn: Trạng thái → Mã → Tên",
     "- Dòng mô tả trong cửa sổ ghi đúng thứ tự vừa chọn\n"
     "- File Excel có cột theo đúng thứ tự Trạng thái, Mã, Tên gói bảo dưỡng"),

    (6, "Nút Chọn tất cả và Bỏ chọn hết", "P1",
     "Cửa sổ Chọn trường xuất file đang mở",
     "1. Bấm Bỏ chọn hết\n2. Bấm Chọn tất cả",
     "—",
     "- Bỏ chọn hết: không còn trường nào, nút Xuất file không dùng được\n"
     "- Chọn tất cả: quay lại đủ 6 trường"),

    (7, "Mã gói toàn số hiển thị đúng trong Excel", "P0",
     "Danh mục có gói mã \"01\" và gói mã \"111\"",
     "1. Xuất file\n2. Mở file và xem ô mã của 2 gói đó",
     "—",
     "- Mã \"01\" giữ nguyên số 0 ở đầu, không bị Excel cắt thành 1\n"
     "- Không hiện cảnh báo góc ô kiểu \"số đang lưu dạng chữ\""),

    (8, "Xuất file khi danh sách rỗng theo bộ lọc", "P2",
     "Đang lọc bằng từ khoá không có kết quả",
     "1. Lọc chuỗi không tồn tại\n2. Bấm Xuất Excel và xuất file",
     "—",
     "- File vẫn ra đủ dữ liệu toàn danh mục (do không áp bộ lọc)"),

    (9, "Mở màn In phiếu từ danh sách", "P0",
     "Gói BDT001 đã khai nội dung kiểm tra",
     "1. Mở menu ba chấm dòng BDT001\n2. Bấm In",
     "Gói: BDT001",
     "- Mở TAB MỚI với màn In danh mục kiểm tra bảo dưỡng\n"
     "- Danh sách ở tab cũ không bị ảnh hưởng"),

    (10, "Nội dung phiếu in", "P0",
     "Đang ở màn In của gói BDT001",
     "1. Quan sát nội dung phiếu",
     "—",
     "- Có logo và thông tin công ty ở đầu phiếu\n"
     "- Tiêu đề \"DANH MỤC KIỂM TRA BẢO DƯỠNG ĐỊNH KỲ\" và dòng \"TÊN DỊCH VỤ: <tên gói in hoa>\"\n"
     "- Bảng gồm STT, Nội dung kiểm tra bảo dưỡng, SL, các cột cấp bảo dưỡng, cột Kiểm tra "
     "(Có/Không) và Ghi chú\n"
     "- Cuối phiếu có phần Ghi chú của gói và bảng giải thích ký hiệu (KTBM, DK, CC, VS…)"),

    (11, "Bấm nút In trên màn in", "P1",
     "Đang ở màn In",
     "1. Bấm nút In ở góc trái phía trên",
     "—",
     "- Mở hộp thoại in của trình duyệt\n- Bản xem trước không có menu bên trái và không có nút In"),

    (12, "In gói chưa khai nội dung kiểm tra", "P1",
     "Có gói chưa khai nội dung kiểm tra nào",
     "1. Bấm In ở gói đó",
     "—",
     "- Phiếu vẫn mở được, bảng nội dung để trống, không báo lỗi"),

    (13, "In từ màn chi tiết", "P1",
     "Đang ở màn chi tiết BDT001",
     "1. Bấm nút In ở chân trang",
     "—",
     "- Mở đúng màn In của gói đang xem"),

    (14, "In khi mẫu in bị thiếu", "P2",
     "Mẫu in Danh mục kiểm tra bảo dưỡng bị xoá khỏi hệ thống",
     "1. Bấm In ở một gói bất kỳ",
     "—",
     "- Hệ thống báo không tìm thấy mẫu in, không treo trang trắng"),
]

S8 = [
    (1, "Nhập VAT vượt trần", "P0",
     "Đang ở màn Thêm gói bảo dưỡng",
     "1. Nhập VAT = 150\n2. Nhập các ô bắt buộc, bấm Lưu",
     "VAT: 150",
     "- Ô VAT hiện lỗi \"Tối đa 100\", không lưu"),

    (2, "Nhập Định mức đàm phán giá vượt trần", "P0",
     "Đang ở màn Thêm gói bảo dưỡng",
     "1. Nhập Định mức đàm phán giá = 120\n2. Bấm Lưu",
     "Định mức đàm phán giá: 120",
     "- Hiện lỗi \"Tối đa 99\", không lưu"),

    (3, "Nhập giá trị âm cho VAT", "P1",
     "Đang ở màn Thêm gói bảo dưỡng",
     "1. Nhập VAT = -5\n2. Bấm Lưu",
     "VAT: -5",
     "- Hiện lỗi \"Không được nhỏ hơn 0\""),

    (4, "Nhập Hệ số giá bán nhỏ hơn 1", "P0",
     "Đang ở màn Thêm gói bảo dưỡng",
     "1. Nhập Hệ số giá bán gói bảo dưỡng = 0,5\n2. Bấm Lưu",
     "Hệ số giá bán: 0,5",
     "- Hiện lỗi \"Không được nhỏ hơn 1\""),

    (5, "Nhập Hệ số giá bán vượt trần", "P1",
     "Đang ở màn Thêm gói bảo dưỡng",
     "1. Nhập Hệ số giá bán = 150\n2. Bấm Lưu",
     "Hệ số giá bán: 150",
     "- Hiện lỗi \"Tối đa 100\""),

    (6, "Dấu phẩy là dấu thập phân", "P0",
     "Đang ở màn Thêm gói bảo dưỡng",
     "1. Nhập VAT = 12,5\n2. Nhập đủ các ô bắt buộc, bấm Lưu\n3. Mở lại màn Sửa",
     "VAT: 12,5",
     "- Lưu thành công, giá trị hiển thị lại đúng 12,5 (mười hai phẩy năm)\n"
     "- ⚠️ Không được hiểu 12,5 thành 125"),

    (7, "Nhập chữ vào ô số", "P1",
     "Đang ở màn Thêm gói bảo dưỡng",
     "1. Nhập VAT = abc\n2. Bấm Lưu",
     "VAT: abc",
     "- Hiện lỗi \"Phải là số\""),

    (8, "Tên gói vượt 255 ký tự", "P1",
     "Đang ở màn Thêm gói bảo dưỡng",
     "1. Nhập Tên gói 300 ký tự\n2. Bấm Lưu",
     "Tên: chuỗi 300 ký tự",
     "- Hiện lỗi \"Tối đa 255 ký tự\", không lưu âm thầm chuỗi bị cắt"),

    (9, "Ghi chú vượt 255 ký tự", "P2",
     "Đang ở màn Thêm gói bảo dưỡng",
     "1. Nhập Ghi chú 300 ký tự\n2. Bấm Lưu",
     "Ghi chú: chuỗi 300 ký tự",
     "- Hiện lỗi \"Tối đa 255 ký tự\""),

    (10, "Hệ số công ty vượt trần", "P1",
     "Khối Giá vốn theo công ty đang hiển thị",
     "1. Nhập hệ số của một công ty = 999999999\n2. Bấm Lưu",
     "Hệ số: 999.999.999",
     "- Hiện lỗi \"Tối đa 99.999.999,99\"\n"
     "- ⚠️ Trước đây giá trị vượt trần bị lưu sai âm thầm — phải kiểm kỹ giá trị sau khi lưu"),

    (11, "Hệ số công ty để trống", "P1",
     "Khối Giá vốn theo công ty đang hiển thị",
     "1. Xoá trắng hệ số của một công ty\n2. Bấm Lưu\n3. Mở lại màn Sửa",
     "Hệ số: (để trống)",
     "- Lưu thành công; hệ số của công ty đó về mặc định 1, KHÔNG phải 0"),

    (12, "Nhập khoảng trắng đầu cuối cho Tên và Mã", "P1",
     "Đang ở màn Thêm gói bảo dưỡng",
     "1. Nhập Tên và Mã có dấu cách ở đầu và cuối\n2. Bấm Lưu\n3. Mở lại màn Sửa",
     "Tên: \"  Gói QA011  \" | Mã: \"  qa011  \"",
     "- Giá trị lưu đã cắt sạch khoảng trắng; Mã hiển thị QA011 in hoa"),

    (13, "Số lượng của dòng nội dung nhập chữ", "P2",
     "Bảng nội dung kiểm tra đã có 1 dòng",
     "1. Nhập SL = abc\n2. Bấm Lưu",
     "SL: abc",
     "- Hiện lỗi \"Phải là số\" tại ô SL"),

    (14, "Đính kèm nhiều file PDF", "P1",
     "Có sẵn 3 file PDF",
     "1. Thêm lần lượt 3 file PDF\n2. Bấm Lưu\n3. Mở chi tiết gói",
     "File: 3 file PDF",
     "- Lưu thành công, chi tiết hiển thị đủ 3 file, mở được từng file"),
]

S9 = [
    (1, "Hai người cùng sửa một gói", "P0",
     "Người A và người B cùng mở màn Sửa của gói QA001",
     "1. Người A đổi Tên rồi Lưu\n2. Người B (đang mở dữ liệu cũ) đổi Ghi chú rồi Lưu\n"
     "3. Cả hai mở lại chi tiết",
     "—",
     "- Ghi nhận kết quả thực tế: bản lưu sau ghi đè bản trước hay hệ thống cảnh báo\n"
     "- ⚠️ Kiểm cửa sổ Lịch sử: phải có đủ 2 mốc thay đổi của 2 người"),

    (2, "Khóa gói trong khi người khác đang sửa", "P0",
     "Người A đang mở màn Sửa gói QA001",
     "1. Người B xoá gói QA001 (gói đang được dùng nên chuyển sang Khóa)\n2. Người A bấm Lưu",
     "—",
     "- Người A bị chặn kèm thông báo yêu cầu mở khoá trước khi cập nhật\n"
     "- Dữ liệu không bị ghi đè, màn hình không treo"),

    (3, "Xóa gói trong khi người khác đang mở màn Sửa", "P0",
     "Người A đang mở màn Sửa gói QA004 (gói xoá được)",
     "1. Người B xoá QA004\n2. Người A bấm Lưu",
     "—",
     "- Người A nhận thông báo lỗi đọc hiểu được, không tạo lại bản ghi đã xoá"),

    (4, "Hai người cùng tạo trùng mã", "P1",
     "Người A và người B cùng nhập mã QA020",
     "1. Cả hai nhập cùng mã\n2. Cùng bấm Lưu gần như đồng thời",
     "Mã: QA020",
     "- Chỉ một người lưu thành công, người còn lại nhận lỗi \"Đã tồn tại\"\n"
     "- Danh sách chỉ có 1 gói QA020"),

    (5, "Danh sách tự làm mới sau thao tác ghi", "P0",
     "Đang ở trang 1 với bộ lọc rỗng",
     "1. Xoá một gói\n2. Không tải lại trang, quan sát danh sách",
     "—",
     "- Danh sách tự cập nhật, dòng đã xoá biến mất, tổng số bản ghi giảm 1"),

    (6, "Lưu gói khi mất kết nối", "P2",
     "Màn Thêm gói đã nhập đủ dữ liệu hợp lệ",
     "1. Ngắt mạng\n2. Bấm Lưu\n3. Nối lại mạng và bấm Lưu",
     "Mã: QA021",
     "- Lần 1: báo lỗi, không rời trang, dữ liệu còn nguyên\n"
     "- Lần 2: lưu thành công, chỉ tạo 1 bản ghi"),

    (7, "Lỗi giữa chừng khi lưu không để lại dữ liệu rác", "P0",
     "Gói QA001 đang có 2 cột cấp, trong đó 1 cấp đã dùng ở báo giá dịch vụ",
     "1. Sửa QA001: đổi nội dung kiểm tra VÀ xoá cột cấp đã dùng\n2. Bấm Lưu (sẽ bị chặn)\n"
     "3. Mở lại chi tiết QA001",
     "—",
     "- Hệ thống chặn không cho lưu\n"
     "- ⚠️ Nội dung kiểm tra của gói phải NGUYÊN VẸN như trước khi sửa, không được mất dòng nào"),

    (8, "Đổi danh mục phụ thuộc trong lúc đang mở form", "P1",
     "Đang mở màn Thêm gói; ở màn khác vừa khoá một đơn vị tính",
     "1. Mở màn Thêm gói\n2. Ở tab khác khoá một đơn vị tính đang dùng\n"
     "3. Quay lại form, mở ô ĐVT",
     "—",
     "- Ghi nhận kết quả thực tế: đơn vị vừa khoá còn xuất hiện trong ô chọn hay không\n"
     "- Tải lại trang thì danh sách chọn phải cập nhật"),
]

S10 = [
    (1, "Mở cửa sổ Lịch sử từ danh sách", "P0",
     "Gói BDT001 đã từng bị đổi trạng thái",
     "1. Mở menu ba chấm dòng BDT001\n2. Bấm Lịch sử",
     "—",
     "- Cửa sổ \"Lịch sử thay đổi\", dòng phụ ghi \"Gói bảo dưỡng: BDT001 - BD test 001\"\n"
     "- Các mốc xếp mới nhất trước\n- Có nút Bộ lọc và nút Đóng"),

    (2, "Nội dung một mốc lịch sử", "P0",
     "Gói BDT001 vừa được mở khóa",
     "1. Mở cửa sổ Lịch sử của BDT001\n2. Đọc mốc trên cùng",
     "—",
     "- Hiện ngày giờ, nhãn hành động (\"Mở khóa\"), tên người thực hiện kèm phòng ban\n"
     "- Dòng chi tiết: Trạng thái: Khóa → Hoạt động"),

    (3, "Lịch sử ghi nhận việc tạo mới", "P0",
     "Vừa tạo gói QA011",
     "1. Tạo QA011\n2. Mở cửa sổ Lịch sử của QA011",
     "—",
     "- Có đúng 1 mốc \"Tạo mới\" với người thực hiện là người vừa tạo"),

    (4, "Lịch sử ghi nhận từng trường thay đổi", "P0",
     "Vừa đổi Tên, VAT và Ghi chú của QA011",
     "1. Sửa 3 ô trên rồi Lưu\n2. Mở cửa sổ Lịch sử",
     "—",
     "- Mốc \"Thay đổi thông tin\" liệt kê cả ba trường với giá trị cũ → giá trị mới\n"
     "- Nhãn trường bằng tiếng Việt: Tên gói bảo dưỡng, VAT, Ghi chú"),

    (5, "Thay đổi nội dung kiểm tra có vào lịch sử không", "P1",
     "Vừa thêm một dòng nội dung kiểm tra cho QA011",
     "1. Sửa QA011: thêm 1 dòng nội dung kiểm tra, Lưu\n2. Mở cửa sổ Lịch sử",
     "—",
     "- Ghi nhận kết quả thực tế\n"
     "- ⚠️ Lịch sử chỉ theo dõi các trường của khối Thông tin chung (mã, tên, định mức đàm phán "
     "giá, VAT, ghi chú, trạng thái); thay đổi ma trận nội dung KHÔNG sinh mốc — không phải lỗi"),

    (6, "Sửa mà không thay đổi gì", "P1",
     "Gói QA011 đã có lịch sử",
     "1. Bấm Sửa QA011, không sửa ô nào, bấm Lưu\n2. Mở cửa sổ Lịch sử",
     "—",
     "- Vẫn báo cập nhật thành công\n- KHÔNG phát sinh thêm mốc \"Thay đổi thông tin\""),

    (7, "Lọc lịch sử theo loại hoạt động", "P1",
     "Bản ghi có đủ 3 loại mốc",
     "1. Mở cửa sổ Lịch sử\n2. Bấm Bộ lọc\n3. Chọn \"Thay đổi trạng thái\"",
     "—",
     "- Chỉ còn các mốc Khóa / Mở khóa\n- Danh sách loại hoạt động có đúng 3 nhóm"),

    (8, "Lịch sử của gói chưa từng thay đổi", "P1",
     "Gói cũ chưa phát sinh thao tác nào từ khi có chức năng lịch sử",
     "1. Mở cửa sổ Lịch sử của gói đó",
     "—",
     "- Hiển thị \"Chưa có lịch sử thao tác nào.\", không báo lỗi"),

    (9, "Luồng đầy đủ: tạo → sửa → nhân bản → khóa → mở khóa → xóa", "P0",
     "Danh mục chưa có mã QA030",
     "1. Tạo gói QA030 đủ thông tin + 1 file PDF\n2. Sửa Ghi chú\n3. Nhân bản thành QA031\n"
     "4. Xoá QA030 (chưa gắn hàng hoá nên xoá thật)\n5. Với QA031: đổi trạng thái sang Khóa rồi "
     "Mở khóa\n6. Mở cửa sổ Lịch sử của QA031",
     "Mã: QA030, QA031",
     "- Mỗi bước có thông báo thành công tương ứng\n"
     "- QA030 biến mất khỏi danh sách sau bước 4\n"
     "- Lịch sử QA031 có đủ các mốc theo thứ tự: Tạo mới, Khóa, Mở khóa"),

    (10, "Dọn dữ liệu sau khi test", "P1",
     "Đã tạo các gói QA001 … QA031 trong quá trình test",
     "1. Lọc theo từ khoá QA\n2. Xoá lần lượt các gói kiểm thử\n3. Bấm Làm mới và đối chiếu tổng số",
     "Từ khoá: QA",
     "- Danh mục trở về đúng 221 gói như trước khi test\n"
     "- ⚠️ Gói nào đã gắn hàng hoá sẽ không xoá được mà chỉ chuyển Khóa — ghi lại danh sách để bộ "
     "phận kỹ thuật dọn"),
]

SECTIONS = [
    ("I", "HIỂN THỊ TRANG & TRUY CẬP", S1),
    ("II", "BỘ LỌC & TÌM KIẾM", S2),
    ("III", "DANH SÁCH, SẮP XẾP & PHÂN TRANG", S3),
    ("IV", "TẠO MỚI GÓI BẢO DƯỠNG", S4),
    ("V", "SỬA / XEM CHI TIẾT / NHÂN BẢN", S5),
    ("VI", "XÓA, KHÓA & MỞ KHÓA", S6),
    ("VII", "XUẤT EXCEL & IN PHIẾU", S7),
    ("VIII", "RÀNG BUỘC NHẬP LIỆU", S8),
    ("IX", "CÔ LẬP DỮ LIỆU & THAO TÁC ĐỒNG THỜI", S9),
    ("X", "LỊCH SỬ THAY ĐỔI & LUỒNG TỔNG THỂ", S10),
]

build(output_file=OUT,
      sheet_name="Trang tính1",
      feature_name="Danh mục gói bảo dưỡng - Cập nhật ngày 17/08/2026",
      module_name=MODULE,
      description_block=DESCRIPTION_BLOCK,
      role_tcs=ROLE_TCS,
      sections=SECTIONS)
