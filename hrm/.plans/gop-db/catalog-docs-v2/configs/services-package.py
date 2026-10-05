# -*- coding: utf-8 -*-
# Danh mục gói bảo dưỡng — CHỈ dùng cho tc_ops.py (sửa tab testcase online).
# HDSD / SRS của màn này KHÔNG dựng bằng catalog_v2: bộ sinh riêng ở
#   .plans/gop-db/customer-care-services-catalog/docs_v2/ (gen_hdsd.py, gen_srs.py, gen_uml.py)
# nên `upload.py services-package` KHÔNG dùng được (file out/ nằm ở thư mục docs_v2).
# Nguồn: code gop_db 28/09/2026 — BE Modules/CustomerCare (Service, ServiceService, ServiceController,
# ServiceRequest, ServiceImportService, Routes/api.php), FE pages/customer-care/services/.
# Dump tab: customer-care-services-catalog/docs_v2/ref/testcase_tab.txt (tải 28/09, số R = hàng thật).

_DUNG = ('báo giá dịch vụ, hợp đồng dịch vụ, phụ lục hợp đồng dịch vụ, đề nghị xuất dịch vụ, '
         'đề nghị hạch toán dịch vụ, hạch toán dịch vụ; báo giá, hợp đồng, phiếu giao việc, '
         'phiếu nhập kết quả của dịch vụ bảo hành – sửa chữa')
_KHOA = 'Gói bảo dưỡng đang bị khoá, vui lòng mở khoá trước khi cập nhật.'
_DADUNG = 'Gói bảo dưỡng đang được sử dụng, không thể xóa.'
_XUNGDOT = 'Trạng thái đã bị thay đổi. Vui lòng load lại trang'

CFG = {
    'slug': 'services-package',
    'ten': 'Danh mục gói bảo dưỡng',
    'file_hdsd': 'HDSD_Danh muc goi bao duong.docx',
    'file_srs': 'SRS - Danh mục gói bảo dưỡng.docx',
}

CFG['tc'] = {
    'tab': '12.Danh mục gói bảo dưỡng',
    'hdr_row': 135,            # "VI. XÓA, KHÓA & MỞ KHÓA"
    'edits': [
        # --- Khối mô tả đầu tab ---
        ('B3', 'Danh sách hiển thị TẤT CẢ gói bảo dưỡng của hệ thống, không giới hạn theo công ty của người đăng nhập:\n'
               '- Gói trạng thái Hoạt động — nhãn xanh; có nút Sửa, Xóa (nếu chưa được sử dụng ở chứng từ nào), Khóa, Nhân bản, In, Lịch sử.\n'
               '- Gói trạng thái Khóa — nhãn đỏ; chỉ còn Mở khóa, Nhân bản, In, Lịch sử.\n'
               '- Gói chưa khai nội dung kiểm tra hoặc chưa gắn hàng hoá vẫn hiển thị bình thường.\n'
               '- Cột Tên gói có biểu tượng chữ i khi gói đã khai cấp bảo dưỡng: rê chuột hiện giá bán theo từng cấp.'),
        ('B4', '- Nút Tạo mới, Import Excel và Nhân bản: ẩn khi tài khoản không có quyền Thêm danh mục gói bảo dưỡng.\n'
               '- Nút Sửa và nút Khóa: ẩn khi thiếu quyền Sửa, hoặc khi gói đang ở trạng thái Khóa.\n'
               '- Nút Xóa: ẩn khi thiếu quyền Xóa, khi gói đang Khóa, hoặc khi gói ĐÃ ĐƯỢC SỬ DỤNG ở chứng từ (' + _DUNG + '). Gói chỉ gắn hàng hoá áp dụng vẫn có nút Xóa.\n'
               '- Nút Mở khóa: chỉ hiện với gói đang Khóa và tài khoản có quyền Sửa.\n'
               '- Trong ô chọn của form: đơn vị tính, cấp bảo dưỡng, ghi chú kiểm tra đang bị khóa không xuất hiện (gói cũ đang dùng giá trị đã khóa vẫn hiện đúng tên kèm 🔒).'),
        ('B8', 'Màn hình dùng 3 quyền, đều thuộc nhóm quyền Danh mục dịch vụ bảo dưỡng:\n'
               '- "Thêm danh mục gói bảo dưỡng" — nút Tạo mới, Import Excel và Nhân bản.\n'
               '- "Sửa danh mục gói bảo dưỡng" — nút Sửa, nút Khóa và nút Mở khóa.\n'
               '- "Xóa danh mục gói bảo dưỡng" — nút Xóa.\n'
               '• Xem danh sách, xem chi tiết, In phiếu và Xuất Excel KHÔNG đòi quyền nào: mọi tài khoản đã đăng nhập đều xem và xuất được. Đây là hiện trạng giữ nguyên theo phần mềm cũ, KHÔNG phải lỗi cấu hình môi trường test.\n'
               '• Không có phân quyền theo cấp công ty / phòng ban / bộ phận: mọi người thấy chung một danh sách.'),
        ('B10', 'Các bẫy dễ sai nhất của màn này — đọc trước khi chạy test:\n'
                '1. Xóa là xóa HẲN và chỉ làm được với gói CHƯA được sử dụng ở chứng từ nào (' + _DUNG + '). Gói đã được sử dụng bị ẩn nút Xóa; gọi thẳng chức năng Xóa thì hệ thống chặn và báo "' + _DADUNG + '" — KHÔNG còn tự chuyển sang Khóa. Gói chỉ gắn hàng hoá áp dụng vẫn xóa được (hàng hoá gắn kèm và hệ số giá bán theo công ty bị xóa theo).\n'
                '2. Xuất Excel xuất TOÀN BỘ danh mục, KHÔNG áp bộ lọc đang có trên màn hình. Lọc còn 6 dòng nhưng file vẫn ra đủ 221 dòng — đúng thiết kế, đừng ghi Failed.\n'
                '3. Cửa sổ Chọn trường xuất file tích sẵn đúng các cột đang hiển thị trên bảng; thứ tự cột trong file chạy theo thứ tự các trường trên cửa sổ, đổi thứ tự bằng cách kéo biểu tượng ☰.\n'
                '4. Gói đang Khóa không sửa, không xóa được: nút Sửa, Xóa bị ẩn; mở trang Sửa từ liên kết đã lưu hoặc gọi thẳng chức năng Sửa / Xóa đều bị chặn kèm yêu cầu mở khoá trước. Khóa được CẢ gói đang được sử dụng — bằng nút Khóa ở danh sách, ở chân trang màn Chi tiết (khóa xong ở lại màn Chi tiết), hoặc đổi Trạng thái trong trang Sửa.\n'
                '5. Mã gói tự chuyển thành CHỮ IN HOA ngay khi gõ và chỉ nhận chữ không dấu, số, dấu - và _ (có dấu tiếng Việt, khoảng trắng giữa mã hoặc ký tự đặc biệt sẽ báo lỗi ngay dưới ô); tên gói thì giữ nguyên như nhập.\n'
                '6. Các ô phần trăm và hệ số nhận DẤU PHẨY là dấu thập phân: nhập 12,5 là 12.5 — không phải lỗi.\n'
                '7. Bắt buộc đính kèm ít nhất 1 file PDF thì mới lưu được gói; đây là quy định riêng của HRM, phần mềm cũ không bắt buộc.\n'
                '8. Một cấp bảo dưỡng chỉ chọn được một lần trong ma trận; chọn lại cấp đã dùng ở cột khác sẽ hiện cảnh báo "Cấp bảo dưỡng này đã được chọn ở cột khác". Cấp bảo dưỡng và ghi chú kiểm tra đã khóa không chọn được.\n'
                '9. Bỏ một cột cấp đã phát sinh báo giá dịch vụ sẽ bị hệ thống chặn khi lưu.\n'
                '10. Số liệu tham chiếu của môi trường test khi viết tài liệu: 221 gói bảo dưỡng; tìm từ khoá "GBDT" ra 6 gói; gói "BDT001" đang Hoạt động và có sẵn nội dung kiểm tra + giá theo cấp.\n'
                '11. Gói tạo bằng Import Excel chưa có file PDF (file mẫu không nhập được PDF) → muốn Sửa gói đó phải đính kèm PDF trước.'),
        # --- Phân quyền: nút Khóa ---
        ('I23', '- Dòng Hoạt động: có nút Sửa và nút Khóa, không có nút Xóa\n- Dòng Khóa: có nút Mở khóa\n- Không có nút Tạo mới và Nhân bản'),
        ('I24', '- Có nút Xóa ở gói chưa được sử dụng\n- Không có nút Tạo mới, Sửa, Khóa, Mở khóa'),
        # --- I. Hiển thị: bộ nút theo trạng thái ---
        ('F38', 'Gói "tên gói bảo dưỡng test 001" đang Hoạt động và chưa được chọn ở chứng từ nào'),
        ('I38', '- 2 nút ngoài: Sửa (bút chì), Xóa (thùng rác đỏ)\n- Menu ba chấm: Khóa, Nhân bản, In, Lịch sử'),
        ('F39', 'Gói BDT001 đang Hoạt động và đã được chọn ở ít nhất 1 chứng từ (vd báo giá dịch vụ)'),
        ('G39', '1. Quan sát cột Hành động của dòng BDT001\n2. Mở menu ba chấm'),
        ('I39', '- 2 nút ngoài: Sửa và Khóa\n- Menu ba chấm: Nhân bản, In, Lịch sử\n- KHÔNG có nút Xóa (ẩn hẳn, không phải làm mờ)'),
        ('I40', '- Có nút Mở khóa (ổ khoá mở) và Nhân bản\n- KHÔNG có Sửa, Xóa, Khóa\n- Menu ba chấm vẫn có In và Lịch sử'),
        # --- IV. Tạo mới: gói khóa không chọn được ở màn khác ---
        ('G111', '1. Khóa gói QA001\n2. Vào màn báo giá dịch vụ, mở ô chọn gói bảo dưỡng\n3. Mở một báo giá dịch vụ cũ đã chọn QA001'),
        ('I111', '- Ô chọn gói KHÔNG còn QA001\n- Báo giá cũ đã chọn QA001 vẫn hiện đúng gói QA001'),
        # --- V. Sửa / Chi tiết: ô Trạng thái, chân trang ---
        ('D114', 'Ô Trạng thái ở màn Thêm mới và màn Sửa'),
        ('I114', '- Màn Thêm mới CÓ ô Trạng thái, mặc định Hoạt động\n- Màn Sửa CÓ ô Trạng thái với 2 lựa chọn Hoạt động / Khóa'),
        ('I123', '- Lưu thành công, dòng chuyển sang nhãn Khóa\n- Mất nút Sửa, Xóa, Khóa; còn Mở khóa, Nhân bản, In, Lịch sử'),
        ('D127', 'Chân trang màn chi tiết của gói đang Khóa'),
        ('I127', '- Không có nút Sửa, Xóa, Khóa\n- Có Mở khóa (nếu có quyền Sửa), In, Nhân bản, Quay lại'),
        # --- VI. Xóa / Khóa / Mở khóa ---
        ('F137', 'Gói QA004 đang Hoạt động, chưa được chọn ở chứng từ nào'),
        ('I137', '- Hệ thống báo "Xóa gói bảo dưỡng thành công"\n- Dòng biến mất khỏi danh sách ở cả trạng thái Hoạt động lẫn Khóa, tổng số bản ghi giảm 1 (xóa hẳn, không chuyển sang Khóa)\n- Toàn bộ nội dung kiểm tra, cấp, hàng hoá áp dụng và hệ số giá bán theo công ty của gói cũng bị xoá theo'),
        ('D139', 'Gói chỉ gắn hàng hoá (chưa dùng ở chứng từ) vẫn xóa được'),
        ('F139', 'Gói QA005 đang Hoạt động, đã gắn ít nhất 1 hàng hoá áp dụng, chưa được chọn ở chứng từ nào'),
        ('G139', '1. Quan sát cột Hành động của dòng QA005\n2. Bấm Xóa, bấm Xóa trong hộp xác nhận'),
        ('H139', 'Gói: QA005'),
        ('I139', '- CÓ nút Xóa\n- Báo "Xóa gói bảo dưỡng thành công", QA005 biến mất khỏi danh sách\n- Hàng hoá áp dụng của QA005 bị xoá theo, danh mục hàng hoá không bị ảnh hưởng'),
        ('D140', 'Gói đã dùng ở chứng từ dịch vụ không có nút Xóa'),
        ('F140', 'Chuẩn bị các gói đang Hoạt động, mỗi gói được chọn ở đúng một loại chứng từ như Test data'),
        ('G140', '1. Tìm lần lượt từng gói trên danh sách\n2. Quan sát cột Hành động'),
        ('H140', '1. Báo giá dịch vụ\n2. Hợp đồng dịch vụ\n3. Phụ lục hợp đồng dịch vụ\n4. Đề nghị xuất dịch vụ\n5. Đề nghị hạch toán dịch vụ\n6. Hạch toán dịch vụ\n7. Báo giá / hợp đồng / phiếu giao việc / phiếu nhập kết quả dịch vụ bảo hành – sửa chữa'),
        ('I140', '- Mọi gói đều KHÔNG hiển thị nút Xóa\n- Vẫn có nút Sửa, Khóa'),
        ('I141', '- Hệ thống từ chối, báo "' + _DADUNG + '"\n- BDT001 vẫn còn, trạng thái vẫn Hoạt động (KHÔNG tự chuyển sang Khóa)'),
        ('I144', '- Hệ thống báo "' + _XUNGDOT + '"\n- Không thay đổi dữ liệu, không phát sinh mốc lịch sử mới'),
        ('D147', 'Gọi thẳng Xóa gói đã dùng không phát sinh lịch sử'),
        ('I147', '- Không có mốc "Khóa" hay "Xóa" mới\n- Trạng thái gói vẫn Hoạt động'),
        ('F148', 'Gói QA010 nhân bản từ BDT001, đã mang theo hàng hoá của gói nguồn, chưa được chọn ở chứng từ nào'),
        ('G148', '1. Quan sát cột Hành động của QA010\n2. Bấm Xóa, xác nhận\n3. Tìm lại BDT001'),
        ('I148', '- QA010 CÓ nút Xóa (chỉ mang theo hàng hoá chưa tính là đã sử dụng)\n- Xóa thành công\n- BDT001 không bị ảnh hưởng'),
        # --- IX. Đồng thời ---
        ('G187', '1. Người B bấm Khóa gói QA001 ở danh sách và xác nhận\n2. Người A bấm Lưu'),
        ('I187', '- Người A bị chặn kèm thông báo "' + _KHOA + '"\n- Dữ liệu không bị ghi đè, màn hình không treo'),
        # --- X. Luồng đầy đủ ---
        ('G203', '1. Tạo gói QA030 đủ thông tin + 1 file PDF\n2. Sửa Ghi chú\n3. Nhân bản thành QA031\n4. Xoá QA030 (chưa được chọn ở chứng từ nào nên xoá thật)\n5. Với QA031: bấm Khóa rồi Mở khóa\n6. Mở cửa sổ Lịch sử của QA031'),
        # --- XI. Import: cấp / ghi chú đã khóa ---
        ('D216', 'Validate – công ty / cấp / ĐVT / ghi chú kiểm tra không có trong danh mục hoặc đã bị khóa'),
        ('F216', 'File ghi sai tên: công ty ở sheet 1, cấp ở sheet 2, ghi chú kiểm tra ở sheet 3; thêm 1 dòng dùng cấp đang bị Khóa'),
        ('H216', 'Công ty: Công ty không tồn tại / Cấp: Cấp 9 không có / Ghi chú: Ghi chú không có / Cấp đang Khóa'),
        ('I216', '- Công ty, ĐVT sai báo "… “X” không có trong danh mục"\n- Cấp sai hoặc đang Khóa báo "Cấp bảo dưỡng “X” không có trong danh mục hoặc đã bị khóa"\n- Ghi chú sai hoặc đang Khóa báo "Ghi chú kiểm tra “X” không có trong danh mục hoặc đã bị khóa"\n- Gói ở sheet 1 báo thêm "Sheet “…” dòng N có lỗi"'),
    ],
    'clear_k': [3, 4, 8, 10, 23, 24, 38, 39, 40, 111, 114, 123, 127, 137, 139, 140, 141, 144, 147, 148, 187, 203, 216],
    'blocks': [
        # IV. TẠO MỚI — cuối nhóm (TC_04.030 ở R111)
        {'after': 111, 'merge_from': 82, 'cases': [
            ('TC_04.031', 'Cấp bảo dưỡng đã khóa không có trong ô chọn', 'P0', 'Danh mục Cấp dịch vụ bảo dưỡng có cấp C1 đang Khóa.',
             '1. Mở màn Thêm gói\n2. Thêm 1 cột cấp, mở ô chọn Cấp bảo dưỡng', 'Cấp: C1 (Khóa)',
             '- Ô chọn chỉ có cấp đang Hoạt động, KHÔNG có C1'),
            ('TC_04.032', 'Ghi chú kiểm tra đã khóa không có trong ô chọn', 'P0', 'Danh mục Ghi chú kiểm tra bảo dưỡng có ghi chú G1 đang Khóa.',
             '1. Mở màn Thêm gói, thêm 1 dòng và 1 cột cấp\n2. Mở ô chọn Ghi chú kiểm tra ở ô giao', 'Ghi chú: G1 (Khóa)',
             '- Ô chọn chỉ có ghi chú đang Hoạt động, KHÔNG có G1'),
            ('TC_04.033', 'Cấp bị khóa trong lúc đang nhập', 'P1', 'Đang mở màn Thêm gói, đã chọn cấp C2 cho một cột và nhập đủ thông tin.',
             '1. Ở tab khác, khóa cấp C2 trong danh mục Cấp dịch vụ bảo dưỡng\n2. Quay lại, bấm Lưu', 'Cấp: C2',
             '- Không lưu được, báo lỗi "Cấp bảo dưỡng đã bị khóa hoặc không tồn tại"\n- Dữ liệu đã nhập vẫn còn'),
            ('TC_04.034', 'Ghi chú kiểm tra bị khóa trong lúc đang nhập', 'P1', 'Đang mở màn Thêm gói, đã chọn ghi chú G2 ở một ô giao và nhập đủ thông tin.',
             '1. Ở tab khác, khóa ghi chú G2 trong danh mục Ghi chú kiểm tra bảo dưỡng\n2. Quay lại, bấm Lưu', 'Ghi chú: G2',
             '- Không lưu được, báo lỗi "Nội dung kiểm tra đã bị khóa hoặc không tồn tại"\n- Dữ liệu đã nhập vẫn còn'),
        ]},
        # V. SỬA / XEM CHI TIẾT — cuối nhóm (TC_05.022 ở R134)
        {'after': 134, 'merge_from': 113, 'cases': [
            ('TC_05.023', 'Gói cũ dùng cấp / ghi chú đã khóa vẫn hiện đúng', 'P0', 'Gói QA020 đang Hoạt động, dùng cấp C3 và ghi chú G3; sau đó C3 và G3 bị Khóa ở danh mục.',
             '1. Mở chi tiết QA020\n2. Bấm Sửa QA020, quan sát cột cấp C3 và các ô ghi chú G3\n3. Bấm Lưu (không đổi gì)', 'Gói: QA020',
             '- Chi tiết và trang Sửa vẫn hiện đúng tên C3, G3 kèm biểu tượng 🔒, ô chọn không bị trống\n- Lưu thành công, C3 và G3 vẫn giữ nguyên'),
            ('TC_05.024', 'Đổi sang cấp khác thì cấp đã khóa biến mất khỏi ô chọn', 'P2', 'Đang Sửa gói QA020 (cột cấp C3 đang Khóa).',
             '1. Đổi cột C3 sang một cấp khác đang Hoạt động\n2. Mở lại ô chọn cấp của cột đó', '',
             '- Ô chọn KHÔNG còn C3\n- Muốn quay lại C3 thì phải Mở khóa C3 ở danh mục'),
        ]},
        # VI. XÓA, KHÓA & MỞ KHÓA — cuối nhóm (TC_06.014 ở R149)
        {'after': 149, 'merge_from': 136, 'cases': [
            ('TC_06.015', 'Khóa gói chưa được sử dụng từ danh sách', 'P0', 'Gói QA006 đang Hoạt động, chưa được chọn ở chứng từ nào; tài khoản có quyền Sửa.',
             '1. Mở menu ba chấm dòng QA006, chọn Khóa\n2. Quan sát hộp thoại\n3. Bấm Khóa', 'Gói: QA006',
             '- Hộp thoại tiêu đề "Xác nhận khóa", nội dung "Bạn có chắc chắn muốn khóa gói bảo dưỡng \'<tên>\'?", 2 nút Khóa và Hủy\n- Báo "Khóa gói bảo dưỡng thành công", nhãn đổi thành Khóa\n- Cột Hành động còn Mở khóa, Nhân bản, In, Lịch sử'),
            ('TC_06.016', 'Khóa gói đã được sử dụng', 'P0', 'Gói BDT001 đang Hoạt động, đã được chọn ở báo giá dịch vụ.',
             '1. Bấm nút Khóa (hiện thẳng trên dòng BDT001)\n2. Bấm Khóa trong hộp xác nhận', 'Gói: BDT001',
             '- Khóa thành công, không bị chặn vì đang được sử dụng\n- Báo giá dịch vụ cũ vẫn hiện đúng gói BDT001\n- Sau test: Mở khóa lại BDT001'),
            ('TC_06.017', 'Hủy thao tác Khóa', 'P1', 'Gói QA006 đang Hoạt động.',
             '1. Chọn Khóa ở dòng QA006\n2. Bấm Hủy', '', '- Hộp thoại đóng, trạng thái giữ nguyên Hoạt động'),
            ('TC_06.018', 'Khóa ở màn chi tiết', 'P0', 'Gói QA007 đang Hoạt động; tài khoản có quyền Sửa.',
             '1. Mở chi tiết QA007, quan sát chân trang\n2. Bấm Khóa, xác nhận', 'Gói: QA007',
             '- Chân trang có nút Khóa (màu cam)\n- Báo "Khóa gói bảo dưỡng thành công", VẪN Ở LẠI màn chi tiết\n- Chân trang đổi ngay: còn Mở khóa, Nhân bản, In, Quay lại; không còn Sửa, Xóa, Khóa'),
            ('TC_06.019', 'Mở khóa ở màn chi tiết', 'P1', 'Gói QA007 đang Khóa, chưa được chọn ở chứng từ nào.',
             '1. Mở chi tiết QA007\n2. Bấm Mở khóa, xác nhận', 'Gói: QA007',
             '- Báo "Mở khóa gói bảo dưỡng thành công", VẪN Ở LẠI màn chi tiết\n- Chân trang hiện lại Sửa, Khóa và Xóa (gói chưa được sử dụng) — giống cột Hành động của dòng QA007 ở danh sách'),
            ('TC_06.020', 'Lịch sử ghi nhận thao tác Khóa', 'P1', 'Vừa khóa gói QA006 bằng nút Khóa.',
             '1. Mở cửa sổ Lịch sử của QA006', '', '- Mốc mới nhất là "Khóa", chi tiết: Trạng thái: Hoạt động → Khóa, kèm người thực hiện'),
            ('TC_06.021', 'Hai người cùng khóa một gói', 'P2', 'Hai tài khoản A, B cùng mở danh sách; gói QA008 đang Hoạt động.',
             '1. A khóa QA008 thành công\n2. B (chưa tải lại trang) chọn Khóa ở QA008 và xác nhận', '',
             '- B nhận thông báo "' + _XUNGDOT + '"\n- Lịch sử QA008 chỉ có 1 mốc Khóa'),
            ('TC_06.022', 'Gói được sử dụng trong lúc đang mở hộp xác nhận Xóa', 'P1', 'Gói QA009 đang Hoạt động, chưa được sử dụng, đang hiện nút Xóa.',
             '1. Bấm Xóa ở dòng QA009, để hộp xác nhận mở\n2. Ở tab khác, chọn QA009 trong một báo giá dịch vụ rồi lưu\n3. Quay lại, bấm Xóa', '',
             '- Báo "' + _DADUNG + '"\n- QA009 vẫn còn, trạng thái Hoạt động\n- Tải lại trang: dòng QA009 không còn nút Xóa'),
            ('TC_06.023', 'Gói bị khóa trong lúc đang mở hộp xác nhận Xóa', 'P1', 'Hai tài khoản A, B. Gói QA009 đang Hoạt động, chưa được sử dụng.',
             '1. A bấm Xóa ở dòng QA009, để hộp xác nhận mở\n2. B khóa QA009\n3. A bấm Xóa', '',
             '- A nhận thông báo "' + _KHOA + '"\n- QA009 vẫn còn, ở trạng thái Khóa sau khi tải lại'),
            ('TC_06.024', 'Không có quyền Sửa thì không Khóa được', 'P0', 'Tài khoản KHÔNG có quyền "Sửa danh mục gói bảo dưỡng"; gói QA006 đang Hoạt động.',
             '1. Quan sát cột Hành động của QA006 và chân trang màn chi tiết QA006\n2. Dùng công cụ kiểm thử API gọi thẳng chức năng Khóa cho QA006', '',
             '- Không có nút Khóa ở cả danh sách và chi tiết\n- Gọi thẳng bị từ chối, báo không có quyền; trạng thái không đổi'),
            ('TC_06.025', 'Xóa từ màn chi tiết', 'P1', 'Gói QA011 đang Hoạt động, chưa được sử dụng.',
             '1. Mở chi tiết QA011\n2. Bấm Xóa ở chân trang, xác nhận', 'Gói: QA011',
             '- Báo "Xóa gói bảo dưỡng thành công"\n- Quay về màn danh sách, QA011 không còn'),
        ]},
    ],
}

CFG['tc_ngoai_pham_vi'] = [
    'TC_09.008 (R193): case chỉ nói ĐVT bị khoá trong lúc mở form; cấp / ghi chú kiểm tra đã có case riêng TC_04.033, TC_04.034 — chưa sửa R193.',
]
