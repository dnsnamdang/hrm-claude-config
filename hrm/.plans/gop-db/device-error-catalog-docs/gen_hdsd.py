# -*- coding: utf-8 -*-
"""Sinh HDSD man 'Danh muc cong viec, loi thiet bi'.

Chay:  python .plans/gop-db/device-error-catalog-docs/gen_hdsd.py
"""
import os
import sys

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "..", ".claude", "skills",
                                "hdsd-documenter", "assets"))
sys.path.insert(0, HERE)
from hdsd_engine import HdsdBuilder  # noqa: E402
import de_config as C  # noqa: E402

TEN, DT, QUYEN, S = C.TEN, C.DOI_TUONG, C.QUYEN, C.SHOTS

b = HdsdBuilder(
    output=os.path.join(HERE, 'HDSD_%s.docx' % TEN.replace('/', '-')),
    shots_dir=os.path.join(HERE, 'de_shots'),
    cover_title='(Màn hình: %s)' % TEN,
    doc_title='HDSD - %s' % TEN)

# ==================================================================== TỔNG QUAN
b.h1("TỔNG QUAN")

b.h2("1. Thuật ngữ sử dụng trong tài liệu")
b.table([["Thuật ngữ", "Giải thích"]] + [[t[0], t[1]] for t in C.THUAT_NGU])

b.h2("2. Cập nhật tài liệu")
b.table([
    ["Phiên bản", "Ngày", "Người cập nhật", "Nội dung"],
    ["1.0", "18/08/2026", "Tri Lee", "Lập mới cho màn %s." % TEN],
])

b.h2("3. Giới thiệu chung")
b.para("%s là danh mục nền của nghiệp vụ sửa chữa. Mỗi bản ghi ở đây là một hạng mục công việc "
       "hoặc một tình trạng lỗi của thiết bị, kèm theo định mức công, các hệ số tính giá, danh "
       "sách thiết bị áp dụng, vật tư thay thế và dịch vụ đi kèm." % TEN)
b.para("Dữ liệu của màn này được chọn khi lập báo giá dịch vụ và phiếu sửa chữa, nên mỗi thay đổi "
       "ở đây đều ảnh hưởng tới việc báo giá cho khách hàng.")
b.para("Đường dẫn truy cập:")
b.bullet("Menu: Chăm sóc khách hàng → Danh mục → Công việc, lỗi thiết bị")
b.bullet("Hoặc gõ thẳng đường dẫn %s vào thanh địa chỉ trình duyệt" % C.ROUTE)

b.h2("4. Quyền sử dụng")
b.table([
    ["Tên quyền", "Cho phép làm gì", "Ghi chú"],
    [QUYEN,
     "Mở màn hình và thực hiện đầy đủ: Thêm mới, Chỉnh sửa, Xóa, Khóa / Mở khóa, In danh sách, "
     "In chi tiết, Xuất tệp bảng tính.",
     "Màn hình chỉ có MỘT quyền cho cả xem lẫn thao tác."],
])
b.para("Nếu không có quyền này, mục menu Công việc, lỗi thiết bị sẽ không hiển thị; trường hợp "
       "truy cập trực tiếp bằng đường dẫn, hệ thống báo lỗi không có quyền.")
b.para("Riêng chức năng Xem lịch sử thay đổi không gắn quyền riêng, theo quy ước chung của mọi "
       "màn danh sách trong hệ thống.")

# ==================================================================== PHẦN 1
b.h1("PHẦN 1: TRUY CẬP VÀ BỐ CỤC MÀN HÌNH")

b.h2("1. Truy cập màn hình")
b.para("Đăng nhập hệ thống, vào menu Chăm sóc khách hàng → Danh mục → Công việc, lỗi thiết bị.")
b.image(S['danhsach'], "Màn hình %s khi mới truy cập" % TEN)

b.h2("2. Bố cục màn hình")
b.para("Màn hình chia làm ba khu vực từ trên xuống:")
b.bullet("Khu vực tìm kiếm — ô tìm kiếm nhanh, nút Tìm kiếm nâng cao, nút Tìm kiếm và Làm mới.")
b.bullet("Thanh công cụ — nút Tạo mới, Xuất Excel, In danh sách và biểu tượng cấu hình cột.")
b.bullet("Bảng danh sách — các cột thông tin, cột Hành động ở cuối, phân trang bên dưới.")

b.h2("3. Các cột của bảng danh sách")
b.table([["Cột", "Nội dung"]] + [[c[0], c[1]] for c in C.COT])
b.para("Lưu ý: bảy cột ghi “Mặc định ẩn” sẽ không thấy khi anh/chị mới vào màn. Muốn xem, hãy bật "
       "chúng ở cửa sổ Tuỳ chỉnh cột — xem Phần 2 mục 3.")

b.h2("4. Cột Hành động")
b.para("Mỗi dòng có tối đa năm thao tác: Sửa, Xóa, Khóa (hoặc Mở khóa), In và Lịch sử.")
b.para("Cột này chỉ hiện THẲNG hai thao tác đầu tiên còn dùng được; các thao tác còn lại tự động "
       "dồn vào nút ba chấm bên cạnh.")
b.image(S['menu'], "Nút ba chấm chứa các thao tác còn lại của dòng")
b.para("Vì vậy anh/chị sẽ thấy các dòng khác nhau có tập nút khác nhau — đây là thiết kế, "
       "không phải lỗi hiển thị:")
b.table([
    ["Trạng thái của dòng", "Hai nút hiện thẳng", "Trong nút ba chấm"],
    ["Hoạt động, chưa dùng ở báo giá hay phiếu sửa chữa", "Sửa, Xóa", "Khóa, In, Lịch sử"],
    ["Hoạt động, đã dùng ở báo giá hoặc phiếu sửa chữa", "Sửa, Khóa", "In, Lịch sử"],
    ["Đã Khóa", "Mở khóa, In", "Lịch sử"],
])
b.para("Quy tắc chung: thao tác nào không dùng được thì hệ thống ẩn hẳn nút đi, chứ không hiện "
       "nút mờ. Không thấy nút Xóa nghĩa là hạng mục đó đã được dùng ở đâu đó, hoặc đang bị Khóa.")

b.h2("5. Phân trang và sắp xếp")
b.para("Cuối bảng có ô hiển thị tổng số bản ghi khớp bộ lọc đang áp dụng — không phải tổng toàn "
       "danh mục. Đổi bộ lọc thì con số này đổi theo.")
b.para("Bấm vào tiêu đề cột có mũi tên để sắp xếp, bấm lần thứ hai để đảo chiều. Thứ tự sắp xếp "
       "giữ nguyên khi chuyển trang. Anh/chị đổi được số dòng mỗi trang; sau khi đổi hệ thống tự "
       "quay về trang 1.")

# ==================================================================== PHẦN 2
b.h1("PHẦN 2: TÌM KIẾM, LỌC VÀ TUỲ CHỈNH CỘT")

b.h2("1. Tìm kiếm nhanh")
b.para("Gõ từ khóa vào ô tìm kiếm ở đầu màn hình để tìm theo tên công việc hoặc tình trạng lỗi. "
       "Xóa hết từ khóa thì danh sách quay về đầy đủ.")

b.h2("2. Bộ lọc nâng cao")
b.para("Bấm nút Tìm kiếm nâng cao để mở panel chứa 8 tiêu chí lọc.")
b.image(S['boloc'], "Panel Tìm kiếm nâng cao đang mở")
b.table([["Tiêu chí", "Cách dùng"]] + [[f[0], f[4]] for f in C.LOC[1:]])
b.para("Chọn xong bấm Tìm kiếm. Các tiêu chí kết hợp với nhau theo kiểu VÀ — chỉ hạng mục thỏa "
       "đồng thời tất cả các tiêu chí mới hiện ra.")
b.para("Bấm Làm mới để xóa toàn bộ tiêu chí; danh sách nạp lại đầy đủ ngay lập tức.")
b.para("Lưu ý về ô “Tên hoặc mã hàng hóa”: ô này tìm theo THIẾT BỊ ĐƯỢC ÁP DỤNG, không phải tên "
       "của hạng mục. Nhập mã một thiết bị sẽ ra tất cả hạng mục có áp dụng cho thiết bị đó.")
b.para("Ô “Đơn giá bán: từ – đến” cho phép chỉ nhập một đầu. Nhập mỗi ô “từ” thì hệ thống lấy "
       "tất cả hạng mục có đơn giá từ mức đó trở lên.")

b.h2("3. Tuỳ chỉnh cột hiển thị")
b.para("Bấm biểu tượng cấu hình cột ở góc phải thanh công cụ.")
b.image(S['cot'], "Cửa sổ Tuỳ chỉnh cột hiển thị")
b.bullet("Tích hoặc bỏ tích để hiện / ẩn từng cột.")
b.bullet("Cột STT và cột Tên công việc / Tình trạng lỗi bị khóa, luôn hiển thị.")
b.bullet("Bấm Lưu để ghi nhận. Cấu hình lưu riêng cho tài khoản của anh/chị, không ảnh hưởng "
         "người khác.")
b.para("Bảy cột được ẩn sẵn để bảng gọn hơn: Loại, Áp dụng cho thiết bị, Định mức công, Công kỹ "
       "thuật, Đơn giá bán, Người cập nhật, Ngày cập nhật. Khi cần đối chiếu giá hoặc định mức, "
       "anh/chị bật chúng lên rồi tắt đi sau.")

# ==================================================================== PHẦN 3
b.h1("PHẦN 3: THÊM MỚI CÔNG VIỆC / LỖI THIẾT BỊ")
b.para("Yêu cầu quyền: %s." % QUYEN)

b.h2("1. Mở trang thêm mới")
b.para("Bấm nút Tạo mới trên thanh công cụ. Khác các màn danh mục khác, chức năng này mở một "
       "TRANG RIÊNG chứ không phải cửa sổ, vì form có nhiều bảng con.")
b.image(S['taomoi'], "Trang Thêm công việc / lỗi thiết bị")

b.h2("2. Các trường thông tin chung")
b.table([["Trường", "Kiểu nhập", "Bắt buộc", "Giá trị ban đầu", "Ghi chú"]] +
        [[t[0], t[1], t[3], t[4], t[5]] for t in C.TRUONG[:11]])
b.para("Giá trị điền sẵn khi thêm mới: tất cả các ô đều để trống. Hạng mục mới luôn được tạo với "
       "trạng thái Hoạt động.")

b.h2("3. Bốn ô có thể để trống vì hệ thống tự tính")
b.para("Đây là điểm khác biệt lớn nhất của màn này so với các danh mục khác. Bốn ô sau KHÔNG bắt "
       "buộc, để trống thì hệ thống tự điền:")
b.table([
    ["Ô", "Nếu để trống thì..."],
    ["Công kỹ thuật", "Hệ thống tự tính từ Định mức công anh/chị đã nhập."],
    ["Đơn giá bán", "Hệ thống tự tính theo công thức nội bộ."],
    ["Hệ số giá bán dịch vụ", "Hệ thống lấy theo cấu hình của công ty anh/chị đang làm việc."],
    ["Đơn giá công kỹ thuật", "Hệ thống lấy theo cấu hình của công ty anh/chị đang làm việc."],
])
b.para("Nếu anh/chị tự nhập giá trị vào các ô này thì giá trị nhập tay được ưu tiên, hệ thống "
       "không tính đè lên.")
b.para("Lưu ý: vì hai ô cuối lấy theo cấu hình công ty, hai người ở hai công ty khác nhau khai "
       "cùng một hạng mục có thể ra kết quả tính khác nhau. Đây là đúng thiết kế.")

b.h2("4. Ba bảng con")
b.table([["Bảng", "Bắt buộc", "Cách dùng"],
         ["Áp dụng cho thiết bị", "Có",
          "Bấm nút thêm để mở cửa sổ tìm kiếm hàng hóa, chọn thiết bị mà hạng mục này áp dụng. "
          "BẮT BUỘC có ít nhất một dòng, không thì không lưu được."],
         ["Vật tư thay thế", "Không",
          "Khai các hàng hóa dùng để thay thế khi thực hiện hạng mục. Bỏ trống vẫn lưu được."],
         ["Dịch vụ sửa chữa kèm theo", "Không",
          "Khai các dịch vụ đi kèm. Bỏ trống vẫn lưu được, NHƯNG mỗi dòng đã thêm thì phải nhập "
          "đủ cả Giá vốn và Giá dịch vụ."]])
b.para("Nhắc lại điểm dễ nhầm: bảng Dịch vụ sửa chữa kèm theo không bắt buộc phải có dòng nào. "
       "Nhưng một khi anh/chị đã thêm dòng vào thì hai ô Giá vốn và Giá dịch vụ của dòng đó trở "
       "thành bắt buộc. Nếu không định khai giá, hãy xóa hẳn dòng đó đi.")

b.h2("5. Quy tắc trùng tên — đọc kỹ")
b.para("Tên hạng mục không được trùng TRONG CÙNG MỘT LOẠI công việc / lỗi. Hai loại khác nhau thì "
       "ĐƯỢC PHÉP trùng tên.")
b.para("Ví dụ: anh/chị hoàn toàn có thể có hạng mục “Kiểm tra cầu nâng” ở loại Lỗi đã xác định, "
       "đồng thời có một hạng mục cũng tên “Kiểm tra cầu nâng” ở loại Tư vấn, khảo sát. Hai bản "
       "ghi này độc lập hoàn toàn, sửa cái này không ảnh hưởng cái kia.")
b.para("Hệ quả cần nhớ: khi anh/chị SỬA một hạng mục và đổi ô Loại, hệ thống sẽ kiểm tra lại "
       "trùng tên trong loại mới. Nếu loại mới đã có hạng mục cùng tên thì thao tác bị chặn.")

b.h2("6. Lưu và các lỗi thường gặp")
b.para("Nhập xong bấm Lưu ở cuối trang. Nếu dữ liệu hợp lệ, hệ thống báo thành công và quay về "
       "danh sách.")
b.para("Nếu còn thiếu sót, hệ thống báo lỗi đỏ ngay dưới ô tương ứng. Trang KHÔNG chuyển và dữ "
       "liệu đã nhập vẫn còn nguyên — anh/chị chỉ cần sửa chỗ báo đỏ rồi bấm Lưu lại.")
b.image(S['validate'], "Trang thêm mới báo lỗi đỏ ngay dưới ô còn thiếu")
b.table([
    ["Thông báo", "Nguyên nhân và cách xử lý"],
    ["Bắt buộc phải nhập",
     "Chưa nhập một trong các ô bắt buộc: Loại công việc / lỗi, Tên công việc / tình trạng lỗi, "
     "Định mức công, Định mức giảm giá, VAT, Hệ số công nghệ."],
    ["Nhập hệ số lớn hơn 0",
     "Ô Hệ số công nghệ đang là 0. Hệ số này bắt buộc lớn hơn 0."],
    ["Tối đa 100", "Ô VAT vượt quá 100."],
    ["Phải là số", "Ô số đang chứa chữ cái hoặc ký tự không hợp lệ."],
    ["Không được nhỏ hơn 0", "Ô số đang là số âm."],
    ["(thông báo tên đã tồn tại)",
     "Đã có hạng mục cùng tên TRONG CÙNG LOẠI. Đổi tên, hoặc đổi sang loại khác."],
    ["(thông báo phải chọn thiết bị)",
     "Bảng Áp dụng cho thiết bị chưa có dòng nào. Thêm ít nhất một thiết bị."],
    ["Bắt buộc phải nhập (trong bảng Dịch vụ sửa chữa)",
     "Một dòng dịch vụ đang thiếu Giá vốn hoặc Giá dịch vụ. Nhập đủ hai ô, hoặc xóa dòng đó."],
])
b.para("Nếu anh/chị bấm Quay lại khi đã nhập dở, hệ thống hỏi xác nhận rời khỏi trang. Chọn ở lại "
       "thì dữ liệu còn nguyên; chọn rời đi thì mọi thứ vừa nhập sẽ mất.")

# ==================================================================== PHẦN 4
b.h1("PHẦN 4: CHỈNH SỬA VÀ XÓA")
b.para("Yêu cầu quyền: %s." % QUYEN)

b.h2("1. Chỉnh sửa")
b.para("Bấm biểu tượng bút chì ở dòng cần sửa. Hệ thống mở trang chỉnh sửa giống hệt trang thêm "
       "mới, nhưng mọi ô và cả ba bảng con đã điền sẵn dữ liệu hiện tại.")
b.para("Các quy tắc bắt buộc và thông báo lỗi giống hệt phần thêm mới. Có hai điểm khác:")
b.bullet("Giữ nguyên tên cũ của chính hạng mục đó thì hệ thống KHÔNG báo trùng.")
b.bullet("Đổi ô Loại sẽ khiến hệ thống kiểm tra lại trùng tên trong loại mới — xem Phần 3 mục 5.")
b.para("Lưu ý: hạng mục đang ở trạng thái Khóa sẽ KHÔNG có nút bút chì. Muốn sửa, anh/chị phải "
       "Mở khóa trước.")
b.para("Sửa xong bấm Lưu. Mọi thay đổi đều được ghi vào Lịch sử kèm tên anh/chị và thời điểm.")

b.h2("2. Xóa")
b.para("Bấm biểu tượng thùng rác ở dòng cần xóa, rồi xác nhận ở hộp thoại hiện ra. Hộp thoại nêu "
       "rõ tên hạng mục — hãy đọc kỹ để chắc chắn không bấm nhầm dòng.")
b.para("Nút thùng rác CHỈ hiện khi hạng mục thỏa CẢ HAI điều kiện:")
b.bullet("Đang ở trạng thái Hoạt động.")
b.bullet("Chưa được dùng trong bất kỳ báo giá hay phiếu sửa chữa nào.")
b.para("Không thấy nút thùng rác nghĩa là hạng mục đó thiếu một trong hai điều kiện trên. Khi đó "
       "anh/chị dùng thao tác Khóa thay cho Xóa — xem Phần 5.")

# ==================================================================== PHẦN 5
b.h1("PHẦN 5: KHÓA VÀ MỞ KHÓA")
b.para("Yêu cầu quyền: %s." % QUYEN)

b.h2("1. Khóa nghĩa là gì")
b.para("Khi một hạng mục không còn dùng nữa nhưng đã phát sinh báo giá hoặc phiếu sửa chữa (nên "
       "không xóa được), anh/chị dùng thao tác Khóa. Sau khi khóa:")
b.bullet("Hạng mục VẪN nằm trong danh mục, cột Trạng thái hiện chữ Khóa.")
b.bullet("Các báo giá và phiếu sửa chữa cũ giữ nguyên đầy đủ thông tin, không bị ảnh hưởng.")
b.bullet("Hạng mục không còn xuất hiện khi lập báo giá hoặc phiếu sửa chữa MỚI.")
b.bullet("Hai nút Sửa và Xóa của dòng đó biến mất; chỉ còn Mở khóa, In và Lịch sử.")

b.h2("2. Các bước khóa")
b.para("Bấm nút ba chấm ở dòng cần khóa, chọn Khóa. Hệ thống hiện hộp xác nhận nêu rõ tên hạng mục.")
b.image(S['khoa'], "Hộp xác nhận khóa hạng mục")
b.bullet("Bấm Khóa để xác nhận. Cột Trạng thái đổi ngay thành Khóa.")
b.bullet("Bấm Hủy nếu bấm nhầm. Không có gì thay đổi.")

b.h2("3. Mở khóa")
b.para("Với hạng mục đang Khóa, bấm nút ba chấm rồi chọn Mở khóa và xác nhận. Hạng mục trở về "
       "trạng thái Hoạt động, nút Sửa hiện trở lại, và hạng mục lại chọn được khi lập báo giá mới.")
b.para("Nếu hạng mục vừa bị người khác thao tác trước đó, hệ thống báo dữ liệu đã thay đổi. "
       "Anh/chị chỉ cần tải lại danh sách rồi thử lại.")

# ==================================================================== PHẦN 6
b.h1("PHẦN 6: IN VÀ XUẤT TỆP BẢNG TÍNH")
b.para("Yêu cầu quyền: %s." % QUYEN)

b.h2("1. Xuất tệp bảng tính")
b.para("Lọc danh sách theo nhu cầu rồi bấm nút Xuất Excel trên thanh công cụ. Hệ thống sinh tệp "
       "theo ĐÚNG bộ lọc đang áp dụng.")
b.para("Lưu ý: tệp chứa TOÀN BỘ kết quả lọc, không phải chỉ những dòng của trang đang xem. Nếu bộ "
       "lọc cho ra 60 hạng mục và anh/chị đang ở trang 2, tệp vẫn có đủ 60 dòng.")
b.para("Tệp có kèm cột thuế suất để anh/chị đối chiếu khi lập báo giá.")

b.h2("2. In danh sách")
b.para("Bấm nút In danh sách trên thanh công cụ để mở bản in toàn bộ danh sách đang lọc. Bản in "
       "có sẵn tiêu đề đầu trang của công ty.")

b.h2("3. In chi tiết một hạng mục")
b.para("Bấm nút ba chấm ở dòng cần in rồi chọn In. Hệ thống mở bản in chi tiết của riêng hạng mục "
       "đó, gồm đầy đủ thông tin chung và ba bảng con.")
b.para("Thao tác In dùng được với cả hạng mục đã Khóa.")

# ==================================================================== PHẦN 7
b.h1("PHẦN 7: XEM LỊCH SỬ THAY ĐỔI")
b.para("Bấm nút ba chấm ở dòng cần xem rồi chọn Lịch sử.")
b.image(S['lichsu'], "Cửa sổ Lịch sử thay đổi của một hạng mục")
b.para("Cửa sổ liệt kê mọi lần thay đổi của hạng mục đó, MỚI NHẤT Ở TRÊN CÙNG. Mỗi dòng cho biết:")
b.bullet("Thời điểm thay đổi.")
b.bullet("Loại thay đổi — sửa thông tin hoặc đổi trạng thái.")
b.bullet("Người thực hiện, kèm mã nhân viên và phòng ban.")
b.bullet("Trường nào đã đổi, giá trị cũ và giá trị mới.")
b.para("Hạng mục vừa được tạo, chưa sửa lần nào thì cửa sổ hiện “Chưa có lịch sử thao tác nào.” — "
       "đây là bình thường, không phải lỗi.")

# ==================================================================== PHẦN 8
b.h1("PHẦN 8: CÂU HỎI THƯỜNG GẶP")
b.table([
    ["Tình huống", "Giải thích"],
    ["Tôi không thấy mục menu của màn này",
     "Anh/chị chưa được gán quyền “%s”. Liên hệ quản trị hệ thống." % QUYEN],
    ["Dòng này không có nút Xóa",
     "Hạng mục đó đã được dùng trong báo giá hoặc phiếu sửa chữa, hoặc đang ở trạng thái Khóa. "
     "Hãy dùng thao tác Khóa thay cho Xóa."],
    ["Dòng này không có nút Sửa",
     "Hạng mục đang ở trạng thái Khóa. Hãy Mở khóa trước rồi sửa."],
    ["Sao mỗi dòng lại có tập nút khác nhau?",
     "Cột Hành động chỉ hiện thẳng hai thao tác đầu còn dùng được, phần còn lại dồn vào nút ba "
     "chấm. Xem bảng ở Phần 1 mục 4."],
    ["Hệ thống báo trùng tên nhưng tôi tìm không thấy hạng mục nào cùng tên",
     "Trùng tên xét trong CÙNG MỘT LOẠI. Hãy lọc theo đúng loại đang chọn rồi tìm lại, và nhớ "
     "rằng hạng mục đã Khóa vẫn tính là trùng."],
    ["Tôi muốn tạo hai hạng mục cùng tên ở hai loại khác nhau",
     "Hoàn toàn được. Hệ thống chỉ chặn trùng tên trong cùng một loại."],
    ["Tôi để trống Công kỹ thuật và Đơn giá bán, có sao không?",
     "Không sao. Hệ thống tự tính hai ô này. Chỉ nhập tay khi anh/chị muốn ghi đè giá trị."],
    ["Đồng nghiệp khai cùng hạng mục nhưng ra giá khác tôi",
     "Hai ô Hệ số giá bán dịch vụ và Đơn giá công kỹ thuật lấy theo cấu hình của từng công ty. "
     "Khác công ty thì kết quả tính khác nhau."],
    ["Tôi thêm dòng dịch vụ nhưng không lưu được",
     "Mỗi dòng dịch vụ đã thêm phải nhập đủ cả Giá vốn và Giá dịch vụ. Nếu không định khai giá, "
     "hãy xóa hẳn dòng đó."],
    ["Tôi không lưu được vì báo phải chọn thiết bị",
     "Bảng Áp dụng cho thiết bị bắt buộc có ít nhất một dòng. Bấm nút thêm để chọn thiết bị."],
    ["Bảng thiếu cột tôi cần xem",
     "Bảy cột được ẩn sẵn cho gọn. Bấm biểu tượng cấu hình cột ở góc phải thanh công cụ để bật lên."],
    ["Tôi xóa nhầm một hạng mục",
     "Liên hệ quản trị hệ thống. Lịch sử thay đổi ghi lại người thực hiện và thời điểm nên tra "
     "cứu được."],
])

b.finish()
