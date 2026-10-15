# Tổng hợp câu hỏi & chỗ code chưa khớp (07/10/2026)

## TC cd · 1. DM dịch vụ sửa chữa và chi p
- [Hỏi] Nhiều case cũ còn bước “Mở bộ lọc nâng cao” và ô lọc “Tên dịch vụ / chi phí”, “Người cập nhật” (TC_01.012, TC_02.003, TC_02.004, TC_02.005, TC_02.009, TC_02.010, TC_02.011) — code hiện tại chỉ còn ô tìm nhanh + Phân loại + Trạng thái hiện sẵn, không có nút Tìm kiếm nâng cao. Có cho viết lại/bỏ các case này không? (ngoài phạm vi 2 loại dòng được sửa)
- [Hỏi] TC_01.012 (đang Passed) ghi bộ lọc được giữ khi chuyển sang màn khác rồi quay lại trong 10 phút; code hiện tại chỉ giữ khi vào trang con dạng /costs/{id} mà màn này không có trang con → rời màn là xóa bộ lọc. Case mới TC_01.015 viết theo code; cần chốt hành vi mong muốn.
- [Hỏi] TC_01.001 bước đi menu ghi “CSKH sau bán → Danh mục- Dịch vụ → Danh mục dịch vụ sửa chữa và chi phí khác”; menu hiện tại là CSKH → Danh mục → “Dịch vụ sửa chữa và chi phí khác”. Chỉ sửa cột I theo phạm vi, cột G chưa sửa.
- [Hỏi] TC_05.008: mở khóa dịch vụ đã bị xóa hiện báo “Item Not Found!” (tiếng Anh, câu chung của hệ thống). Expected đang viết theo hành vi đúng mong đợi (câu tiếng Việt báo không còn tồn tại) — cần chốt câu chữ.
- [Code] Khóa/Mở khóa dịch vụ đã bị người khác xóa: hệ thống báo “Item Not Found!” (tiếng Anh), chưa có câu tiếng Việt và danh sách không tự tải lại.
- [Code] Bộ lọc của màn không được ghi nhớ khi rời màn (không có trang con khớp điều kiện giữ bộ lọc) — khác với TC_01.012 đang ghi.
## TC cd · 2. DM tiền tệ
- [Hỏi] Thứ tự mặc định theo code là bản ghi tạo TRƯỚC nằm trên (tăng dần theo thứ tự tạo), ngược với yêu cầu 'mới nhất → cũ nhất' của tester. Có cần đổi code sang mới nhất lên đầu không? Expected TC_01.001 đang viết theo code.
- [Hỏi] TC_02.012 / TC_02.013 (đã Passed) ghi bộ lọc được nhớ 10 phút khi sang màn khác, và mô tả đầu tab (R10) cũng ghi vậy; nhưng code chỉ lưu bộ lọc khi đi vào trang con /finance/currencies/{id} — màn này không có trang con nên rời màn là xóa. TC_02.020 viết theo code; cần tester kiểm lại TC_02.012/013.
- [Hỏi] TC_02.007 / TC_02.008 có bước 'Bấm mở bộ lọc nâng cao' nhưng màn đang ở chế độ gọn (không có nút này). Không thuộc 2 loại được sửa nên chưa đụng.
- [Hỏi] Cột hiển thị mặc định theo code đã khác các case cũ (TC_01.002, TC_01.003: cột Cập nhật nay ẩn mặc định, có thêm Người tạo/Ngày tạo; ô Tên không còn dòng phụ Tên gọi khác; nút Khóa/Mở khóa nằm ở cột Hành động chứ không ở cột Trạng thái). Expected TC_01.001 đã viết lại theo code; các case khác chưa sửa.
- [Hỏi] Ô tìm nhanh không giới hạn số ký tự; chuỗi cực dài (vài chục nghìn ký tự) có thể làm máy chủ từ chối yêu cầu. Có cần đặt giới hạn (ví dụ 255) không?
- [Code] Mở khóa (và Khóa) một tiền tệ vừa bị người khác xóa: hệ thống hiện thông báo tiếng Anh "Item Not Found!" (thông báo chung khi không tìm thấy bản ghi) thay vì câu tiếng Việt; TC_05.009 viết theo câu đúng mong đợi "Dữ liệu đã thay đổi, vui lòng tải lại" (câu mà cửa sổ Sửa đang dùng khi bản ghi đã bị xóa).
- [Code] Sau khi Mở khóa thất bại vì người khác đã mở khóa trước, danh sách không tự tải lại nên dòng vẫn hiện Khóa cho tới khi bấm Làm mới.
- [Code] Ô tìm nhanh không có giới hạn độ dài.
## TC cd · 3. DM tài khoản
- [Hỏi] Thứ tự mặc định theo code là cây số tài khoản (tăng dần theo Số tài khoản, con nằm dưới mẹ), KHÔNG phải 'tạo mới nhất → cũ nhất'. Expected TC_01.001 viết theo code — xác nhận đúng mong muốn.
- [Hỏi] Tiêu đề khối lọc trong code là 'Bộ lọc danh sách' (Expected cũ TC_01.001 ghi 'Bộ lọc danh mục tài khoản'); cột mặc định đang hiện cũng ít hơn danh sách cột cũ — đã viết lại theo code.
- [Hỏi] TC_02.016 (Expected 'sang màn khác, quay lại trong 10 phút vẫn giữ bộ lọc') trái với code: rời sang màn khác là xoá bộ lọc, chỉ giữ khi vào trang Chi tiết/Sửa rồi quay lại. Case mới TC_02.031 viết theo code; cột I của TC_02.016 không thuộc 2 loại được sửa nên chưa đụng — tester cần cập nhật.
- [Hỏi] Bấm Tạo mới rồi Quay lại thì bộ lọc bị xoá (trang Thêm không nằm trong nhóm trang con được giữ, chỉ trang Chi tiết/Sửa có mã số). Có cần giữ bộ lọc cả khi đi qua trang Thêm không?
- [Hỏi] Bộ lọc nhớ dùng chung giữa các tab của cùng trình duyệt (TC_02.033 viết theo code) — xác nhận chấp nhận được.
- [Hỏi] Ô tìm nhanh không có giới hạn độ dài — có cần đặt giới hạn (vd 255 ký tự) không?
- [Hỏi] Mở khóa bản ghi đã bị xóa ở tab khác: hệ thống báo 'Item Not Found!' (tiếng Anh, không thân thiện) và không tự tải lại danh sách — nên đổi thành câu tiếng Việt kiểu 'Tài khoản không còn tồn tại' và nạp lại danh sách?
- [Hỏi] Mở khóa bản ghi đã được mở khóa ở tab khác: báo 'Bạn không có quyền mở khóa tài khoản này' — câu gây hiểu nhầm (thực chất là trạng thái đã đổi); có nên báo 'Tài khoản đã ở trạng thái Hoạt động' và nạp lại danh sách?
- [Hỏi] TC_05.014 (Lưu và tiếp tục) nằm ở nhóm V. SỬA nhưng nút 'Lưu và tiếp tục' chỉ có ở trang Thêm mới; case mới đặt ở nhóm IV.
- [Code] Mở khóa tài khoản đã bị xóa: thông báo lỗi tiếng Anh 'Item Not Found!' và danh sách không tự nạp lại (pages/finance/accounts/index.vue handleConfirmToggleLock chỉ nạp lại khi thành công).
- [Code] Mở khóa tài khoản đã được người khác mở khóa: thông báo 'Bạn không có quyền mở khóa tài khoản này' sai bản chất, danh sách không tự nạp lại.
## TC cd · 4. DM loại tài khoản
- [Hỏi] TC_02.016 (R48) và mô tả R10 ghi bộ lọc được nhớ 10 phút khi sang màn khác rồi quay lại, nhưng code chỉ nhớ khi đi vào trang con dạng /finance/type-accounts/{id} — màn này không có trang con (Xem/Sửa là cửa sổ) nên rời màn là bộ lọc bị xóa ngay. Case mới TC_02.032 viết theo code (bộ lọc trở về mặc định); cần chốt: sửa expected TC_02.016 hay bổ sung nhớ bộ lọc cho màn này?
- [Hỏi] Ô tìm nhanh không có giới hạn độ dài (TC_02.030 viết theo code). Có cần đặt giới hạn (vd 255 ký tự) không?
- [Hỏi] Expected cũ của TC_01.001 (R24) lệch code develop: tiêu đề khối lọc là "Bộ lọc danh sách" (không phải "Bộ lọc danh mục loại tài khoản"), cột mặc định là STT, Mã, Tên, Người tạo, Ngày tạo, Trạng thái, Hành động (Ghi chú/Cập nhật đang ẩn) — đã viết lại 2 ý này theo code khi sửa cột I. Nhiều case khác của tab (TC_01.004, TC_01.006, TC_04.008, TC_05.001/003…) vẫn mô tả nút Khóa nằm trong cột Trạng thái và nút Sửa bị mờ, trong khi code hiện để Khóa/Mở khóa ở cột Hành động và ẩn hẳn nút không dùng được — ngoài phạm vi 2 loại dòng được sửa nên chưa đụng.
- [Hỏi] TC_05.008: expected viết câu đúng mong đợi "Dữ liệu đã thay đổi, vui lòng tải lại"; code hiện báo "Item Not Found!" (xem code_gaps). Chốt câu nào?
- [Code] Mở khóa loại tài khoản đã bị người khác xóa: hệ thống báo câu tiếng Anh "Item Not Found!" thay vì "Dữ liệu đã thay đổi, vui lòng tải lại" (TC_05.008); danh sách cũng không tự tải lại sau khi báo lỗi.
- [Code] Khóa loại tài khoản đã bị người khác khóa trước: hệ thống báo "Không thể khóa loại tài khoản do còn tài khoản đang hoạt động." — sai lý do (điều kiện khóa gộp cả 'đang Khóa' với 'còn tài khoản dùng').
- [Code] Import Excel chỉ kiểm trùng Mã, KHÔNG kiểm trùng Tên loại tài khoản (form Tạo/Sửa thì chặn trùng tên) → import được loại tài khoản trùng tên đã có; #11588 với trùng tên không áp dụng được.
- [Code] Bộ lọc không được nhớ khi rời màn rồi quay lại trong 10 phút (màn không có trang con khớp điều kiện giữ bộ lọc) — lệch mô tả R10 và TC_02.016.
## TC cd · 6. DM serial thiết bị làm dịch 
- [Hỏi] TC_02.017 (dòng 49) đang ghi rời sang màn khác rồi quay lại trong 10 phút thì bộ lọc vẫn giữ (đã Passed), nhưng code chỉ giữ bộ lọc khi đi vào trang con dạng chi tiết của chính màn — màn serial không có trang con nên rời sang màn khác là xoá bộ lọc. Case mới TC_02.033 viết theo code; cần chốt lại TC_02.017 (sửa expected hay đây là lỗi).
- [Hỏi] TC_01.001 cũ ghi tiêu đề khối lọc "Bộ lọc serial thiết bị làm dịch vụ" và bảng có 8 cột gồm Người cập nhật/Ngày cập nhật, nhưng code: màn không truyền tiêu đề nên khối lọc hiện "Bộ lọc danh sách"; bảng mặc định 7 cột (ẩn Người cập nhật, Ngày cập nhật), có thêm cột Ngày tạo. Đã viết lại expected theo code — cần xác nhận.
- [Hỏi] Dòng tổng dưới bảng in số liền không có dấu phân cách nghìn ("Hiển thị 1–10 / 21600") trong khi quy chuẩn số toàn hệ thống là "21,600". Expected đang chép theo code — có cần sửa code để hiện "21,600" không?
- [Code] Dòng tổng "Hiển thị a–b / N" của bảng dùng chung không định dạng nghìn cho N (quy chuẩn số yêu cầu dấu phẩy ngăn cách nghìn).
- [Code] Bộ lọc màn serial khai giữ trạng thái cho trang con nhưng màn không có trang con nào, nên cơ chế nhớ bộ lọc 10 phút không bao giờ có tác dụng ở màn này.
## TC cd · 7. DM cấp dịch vụ bảo dưỡng
- [Hỏi] Thứ tự mặc định trong code là theo thứ tự tạo TĂNG dần (cấp tạo trước đứng trên, mới nhất ở trang cuối) — tester mong 'mới nhất → cũ nhất'. Đã viết Expected TC_01.001 theo code; có cần đổi code về mới nhất lên đầu không?
- [Hỏi] Mô tả đầu tab (R10) ghi 'Bộ lọc được ghi nhớ trong 10 phút', nhưng màn chỉ lưu bộ lọc khi đi vào trang con mà màn này không có trang con → thực tế bộ lọc KHÔNG được nhớ khi rời màn/F5. Đã viết TC_02.017/018 theo code; có muốn giữ bộ lọc khi rời màn quay lại trong 10 phút không?
- [Hỏi] Expected cũ TC_01.001 lệch code (bảng 4 cột, khối lọc 'Bộ lọc cấp dịch vụ bảo dưỡng', thiếu Import Excel) — đã viết lại theo code hiện tại; các case TC_01.003 ('không có cột Trạng thái / nút Khóa'), TC_03.002, mô tả R4/R10 cũng đã cũ nhưng ngoài phạm vi được sửa.
- [Hỏi] TC_08.013: mở khóa cấp đã bị người khác xóa — Expected viết theo câu xung đột chung 'Trạng thái đã bị thay đổi. Vui lòng load lại trang'; code hiện trả thông báo tiếng Anh 'Item Not Found!'. Xác nhận câu mong đợi?
- [Code] Mở khóa / Khóa cấp dịch vụ đã bị người khác xóa: route bind model nên trả 404 'Item Not Found!' (tiếng Anh) trước khi tới guard GuardsCatalogStatus — chưa ra câu 'Trạng thái đã bị thay đổi. Vui lòng load lại trang' (LevelController::unlock/lock + app/Exceptions/Handler.php:52).
- [Code] Thứ tự mặc định danh sách là id tăng dần (cũ → mới), chưa phải mới nhất lên đầu (LevelService::index orderBy('id','asc')).
- [Code] Nhớ bộ lọc không có tác dụng ở màn này: pathsToKeep ['/customer-care/levels'] nhưng màn không có route con /{id} nên rời màn luôn xoá bộ lọc.
## TC cd · 8. DM ghi chú kiểm tra bảo dưỡn
- [Hỏi] TC_02.006 (R37) và mô tả R10 ghi 'Bộ lọc được nhớ khi quay lại màn trong 10 phút', nhưng code chỉ lưu bộ lọc khi rời sang trang con dạng /customer-care/note-maintenances/{id} — màn này không có trang con nên rời sang màn khác là bộ lọc bị xoá. Case mới TC_02.012 viết theo code (về mặc định) → TC_02.006 đang mâu thuẫn, cần sửa/bỏ (ngoài phạm vi được phép sửa).
- [Hỏi] R24 Expected cũ ghi khối lọc có tiêu đề 'Bộ lọc ghi chú kiểm tra bảo dưỡng' và bảng 6 cột STT, Hạng mục, Ký hiệu, Mô tả, Cập nhật, Hành động; code hiện tại: tiêu đề khối lọc mặc định 'Bộ lọc danh sách', bộ cột mặc định STT, Hạng mục, Người tạo, Ngày tạo, Trạng thái, Hành động → đã viết lại theo code, nhờ xác nhận.
- [Hỏi] Ô tìm nhanh không có giới hạn ký tự; dán chuỗi rất dài (vài nghìn ký tự) có thể vượt giới hạn độ dài đường dẫn của máy chủ — có cần đặt giới hạn (vd 255) không?
- [Hỏi] Mở khóa ghi chú đã bị người khác xóa: code hiện trả câu tiếng Anh 'Item Not Found!' (không qua được bước kiểm tra bản ghi). TC_13.001 viết expected theo hành vi đúng mong đợi (câu chung 'Trạng thái đã bị thay đổi. Vui lòng load lại trang') — xác nhận câu chuẩn.
- [Hỏi] Lưu và tiếp tục khi trùng Hạng mục/Ký hiệu: thông báo nổi là 'Bạn chưa nhập đầy đủ thông tin' (câu dùng chung cho mọi lỗi nhập) dù lỗi là trùng — có muốn đổi câu không?
- [Code] Mở khóa / Khóa ghi chú đã bị xóa: route gắn bản ghi trả 'Item Not Found!' (tiếng Anh) thay cho câu xung đột 'Trạng thái đã bị thay đổi. Vui lòng load lại trang' (Modules/CustomerCare/Routes/api.php:108-111 + app/Exceptions/Handler.php:52-53).
- [Code] Màn không có trang con nên filterStateMixin không bao giờ lưu bộ lọc — mô tả 'nhớ bộ lọc 10 phút' của tab không đúng thực tế.
## TC cd · 9. DM khách hàng
- [Hỏi] TC_01.013 (đã có) kỳ vọng tải lại trang (F5) vẫn giữ bộ lọc, nhưng màn chỉ lưu bộ lọc khi đi vào màn Chi tiết / Sửa / Quản lý của một khách hàng; F5 ngay trên danh sách sẽ mất bộ lọc (hoặc hiện lại bộ lọc cũ của lần vào Chi tiết gần nhất nếu chưa quá 10 phút). Cần chốt hành vi đúng để sửa code hoặc sửa case.
- [Hỏi] Bộ lọc được nhớ chung cho cả trình duyệt, không theo tài khoản: A lọc → vào Chi tiết → đăng xuất, B đăng nhập trong 10 phút sẽ thấy bộ lọc của A. Case mới viết expected theo hành vi đúng (B thấy mặc định) — cần sửa code.
- [Hỏi] Nhớ bộ lọc dùng chung giữa các tab (tab mới mở sau khi tab khác vừa vào Chi tiết sẽ nhận bộ lọc của tab đó) — case đang viết theo hiện trạng; xác nhận có chấp nhận không.
- [Hỏi] Ô tìm nhanh không giới hạn độ dài — case đang viết "nhận hết, không báo lỗi". Có cần đặt giới hạn không?
- [Hỏi] Tab đang gọi nút là "Bộ lọc nâng cao" và mô tả là "cửa sổ", trên màn thực tế nút là "Tìm kiếm nâng cao" và mở ra khối lọc ngay dưới hàng tìm nhanh (không phải cửa sổ). Có cần đồng bộ lại chữ trong các case cũ không?
- [Hỏi] Mở khóa khách hàng đã được người khác mở khóa: máy chủ không báo xung đột như các danh mục địa lý ("Trạng thái đã bị thay đổi. Vui lòng load lại trang") mà báo thành công. Case viết theo hiện trạng — xác nhận có cần báo xung đột không.
- [Code] Import khách hàng chưa có chặn #11588: máy chủ vẫn ghi các dòng còn hợp lệ, trả "Import một phần thành công"; màn đóng cửa sổ Import và báo "Import thành công 2/3 khách hàng. 1 khách hàng thất bại." — không giữ cửa sổ, không tô đỏ dòng lỗi (2 case Import mới sẽ Failed cho tới khi sửa).
- [Code] Bộ lọc màn khách hàng: ô Tỉnh/Thành phố luôn liệt kê toàn bộ tỉnh, không lọc theo Quốc gia đang chọn và đổi Quốc gia không xoá Tỉnh/Thành phố — TC_02.012 (đã có) sẽ Failed.
- [Code] Nhớ bộ lọc không tách theo tài khoản (tài khoản B nhận bộ lọc của A trên cùng trình duyệt).
- [Code] Khóa / Mở khóa khách hàng không kiểm trạng thái hiện tại nên không báo xung đột khi người khác vừa thao tác.
- [Code] Dòng tổng "Hiển thị a–b / N" ghi N liền không có dấu phân cách hàng nghìn (vd 3321), lệch quy chuẩn định dạng số toàn hệ thống (1,234) — thành phần bảng dùng chung, không riêng màn này.
## TC cd · 10. Danh mục ngân hàng
- [Hỏi] TC_02.018 / TC_02.019 và mục 'Ghi chú đọc bảng' ghi bộ lọc được nhớ 10 phút khi rời màn rồi quay lại. Theo code, bộ lọc chỉ được lưu khi rời sang trang con dạng 'Danh mục ngân hàng/{số}', mà màn này không có trang con nào (Xem/Sửa/Chi nhánh đều là cửa sổ) -> thực tế rời sang màn khác là bộ lọc bị xoá, quay lại luôn trống. Cần chốt: sửa expected 2 case đó theo code, hay đây là lỗi cần làm cho màn nhớ bộ lọc?
- [Hỏi] Ô tìm nhanh và ô Tên giao dịch quốc tế không đặt giới hạn số ký tự (TC_02.026 viết theo hiện trạng: không giới hạn, không báo lỗi). Có cần chốt giới hạn tối đa (vd 255 ký tự) không? Chuỗi quá dài (hàng chục nghìn ký tự) có thể bị máy chủ từ chối và báo 'Lỗi khi tải dữ liệu'.
- [Hỏi] TC_05.011 / TC_05.012 viết expected theo hành vi đúng mong đợi (báo 'Trạng thái đã bị thay đổi. Vui lòng load lại trang' — cùng câu đang dùng cho chi nhánh và danh mục địa lý). Hiện tại Mở khóa ngân hàng không kiểm tra nên vẫn báo 'Mở khoá thành công' và ghi thêm mốc lịch sử trùng. Xác nhận dùng câu này cho ngân hàng?
- [Code] Mở khóa NGÂN HÀNG (BankService::unlock + BankController::unlock) không kiểm tra bản ghi còn tồn tại hay đã ở trạng thái Hoạt động: mở khóa ngân hàng đã bị xoá vẫn báo 'Mở khoá thành công'; mở khóa ngân hàng đã được người khác mở khóa vẫn báo thành công và ghi thêm mốc lịch sử 'Mở khóa' Hoạt động → Hoạt động. Chi nhánh đã có chặn (GuardsCatalogStatus) nhưng ngân hàng chưa dùng. Khóa ngân hàng cũng không chặn khóa trùng.
- [Code] Bộ lọc màn Danh mục ngân hàng khai báo nhớ 10 phút nhưng pathsToKeep chỉ khớp đường dẫn '/human/banks/{id}' (không tồn tại) -> bộ lọc thực tế không bao giờ được nhớ khi rời màn.
## TC cd · 11. Danh mục tài khoản ngân hàn
- [Hỏi] TC_02.018 ("Hệ thống ghi nhớ bộ lọc khi rời màn rồi quay lại", đang Passed) và TC_02.019 mâu thuẫn với code hiện tại: màn chỉ lưu bộ lọc khi chuyển sang trang con (trang chi tiết riêng), mà màn này KHÔNG có trang con (Xem/Sửa là cửa sổ trên cùng màn) — nên rời sang màn khác là bộ lọc bị xoá, 10 phút không có tác dụng. Case mới TC_02.025 viết theo code (không giữ). Có cần sửa TC_02.018/019 (ngoài phạm vi được phép sửa) hay đổi code để giữ bộ lọc 10 phút như tài liệu mô tả (mục 9 ghi chú số 8)?
- [Hỏi] Dòng tổng "Hiển thị a–b / N" in số N trần, không có dấu phẩy ngăn hàng nghìn (trái quy tắc định dạng số chung). Thực tế mỗi công ty ít khi > 1.000 tài khoản ngân hàng nên không đưa vào Expected — có cần ghi rõ không?
- [Hỏi] TC_04.001 (Passed) ghi chân cửa sổ chỉ có 2 nút Lưu và Đóng, nhưng code hiện có thêm nút "Lưu và tiếp tục" ở cửa sổ Tạo mới. Case cũ không thuộc 2 loại được phép sửa nên để nguyên — tester cần cập nhật.
- [Hỏi] TC_01.009 (Passed) ghi dòng thống kê khi rỗng là "Hiển thị 0–0 / 0", code hiện hiện "Không có tài khoản nào." — Expected TC_01.001 (đã sửa) và TC_02.024 viết theo code.
- [Code] Mở khóa (và Khóa) không kiểm trạng thái hiện tại: bản ghi đã được người khác Mở khóa trước, bấm Mở khóa lần nữa vẫn báo "Mở khóa thành công" và ghi thêm 1 mốc lịch sử thừa "Hoạt động → Hoạt động" (CompanyAccountController::unlock → CompanyAccountService::setStatus không so trạng thái cũ). TC_05.012 viết theo hành vi đúng mong đợi (không sinh mốc thừa).
## TC cd · 12.Danh mục gói bảo dưỡng
- [Hỏi] TC_02.017 (hàng 59) đang ghi 'Sang màn khác, trong 10 phút quay lại → bộ lọc cũ vẫn còn' nhưng code chỉ giữ bộ lọc khi đi vào màn chi tiết / màn Sửa của 1 gói rồi quay lại; rời sang màn khác (kể cả bấm Tạo mới) là xoá bộ lọc. Case cũ đã Passed — có cần sửa lại TC_02.017 không (ngoài phạm vi 2 loại dòng được sửa)?
- [Hỏi] Bấm Tạo mới rồi Quay lại thì bộ lọc bị xoá (chỉ giữ khi vào chi tiết / Sửa). Đã viết expected theo code ở TC_02.026 — xác nhận đây là hành vi mong muốn?
- [Hỏi] Bộ lọc nhớ theo trình duyệt chứ không theo tài khoản: A lọc → vào chi tiết → đăng xuất, B đăng nhập trong 10 phút sẽ thấy bộ lọc của A. TC_02.027 viết expected là B thấy bộ lọc trống (hành vi đúng mong đợi) → case này sẽ Failed với code hiện tại.
- [Hỏi] Tab mới: nếu tab 1 đã vào màn chi tiết (đã lưu bộ lọc) thì tab mới mở danh sách trong 10 phút sẽ nhận bộ lọc của tab 1 (bộ nhớ dùng chung trình duyệt). TC_02.028 chỉ viết trường hợp tab 1 chưa vào chi tiết — có cần thêm case cho trường hợp này không?
- [Hỏi] Ô tìm nhanh không có giới hạn số ký tự (không maxlength). TC_02.023 viết theo code (nhận hết, lọc ra rỗng) — có cần đặt giới hạn (vd 255) không?
- [Code] Mở khóa gói đã bị người khác xóa: hệ thống trả câu tiếng Anh 'Item Not Found!' (gói không tìm thấy trước khi tới bước kiểm tra xung đột) thay vì 'Trạng thái đã bị thay đổi. Vui lòng load lại trang' — TC_06.023.
- [Code] Import gói bảo dưỡng (#11588) chưa áp dụng: lúc bấm Import, dòng không còn hợp lệ (mã/tên vừa được tạo ở nơi khác) bị bỏ qua âm thầm, các dòng còn lại vẫn được ghi, cửa sổ đóng và báo 'Import thành công N gói bảo dưỡng.' (N không tính dòng bị bỏ); ServiceImportModal không dùng markRejectedImportRows, BE import() dùng pickValidRows thay vì từ chối cả lô — TC_11.024, TC_11.025.
- [Code] Bộ lọc nhớ theo trình duyệt, không theo tài khoản: đổi tài khoản trong 10 phút vẫn thấy bộ lọc của tài khoản trước — TC_02.027.
## TC cd · 13. DM quốc gia
- [Hỏi] Ý 5 (nhớ bộ lọc): màn này mở Xem/Sửa bằng cửa sổ, không có trang con nên bộ lọc KHÔNG được nhớ trong bất kỳ trường hợp nào — rời sang màn khác (kể cả quay lại trước 10 phút) hay F5 đều về mặc định. Expected đang viết theo hiện trạng. Nếu yêu cầu là giữ bộ lọc 10 phút như các màn có trang chi tiết thì phải sửa code và đổi expected các case nhớ bộ lọc.
- [Hỏi] Ô tìm kiếm nhanh không giới hạn độ dài (không chặn ở ô nhập, máy chủ cũng không kiểm) — case độ dài đang viết theo hiện trạng "nhận hết, không báo lỗi". Có cần đặt giới hạn (vd 255 ký tự) không?
- [Code] Dòng tổng "Hiển thị a–b / N" ghi N liền không có dấu phân cách hàng nghìn (vd 3321), lệch quy chuẩn định dạng số toàn hệ thống (1,234) — thành phần bảng dùng chung, không riêng màn này.
## TC cd · 14. DM khu vực
- [Hỏi] Ý 5 (nhớ bộ lọc): màn này mở Xem/Sửa bằng cửa sổ, không có trang con nên bộ lọc KHÔNG được nhớ trong bất kỳ trường hợp nào — rời sang màn khác (kể cả quay lại trước 10 phút) hay F5 đều về mặc định. Expected đang viết theo hiện trạng. Nếu yêu cầu là giữ bộ lọc 10 phút như các màn có trang chi tiết thì phải sửa code và đổi expected các case nhớ bộ lọc.
- [Hỏi] Ô tìm kiếm nhanh không giới hạn độ dài (không chặn ở ô nhập, máy chủ cũng không kiểm) — case độ dài đang viết theo hiện trạng "nhận hết, không báo lỗi". Có cần đặt giới hạn (vd 255 ký tự) không?
- [Hỏi] TC_09.016 (Import thành công) của tab này ghi "Import thành công N đường/phố." — đúng phải là "Import thành công N khu vực." (không thuộc 2 loại dòng được phép sửa nên chưa đổi).
- [Code] Dòng tổng "Hiển thị a–b / N" ghi N liền không có dấu phân cách hàng nghìn (vd 3321), lệch quy chuẩn định dạng số toàn hệ thống (1,234) — thành phần bảng dùng chung, không riêng màn này.
## TC cd · 15. DM phườngxã
- [Hỏi] Ý 5 (nhớ bộ lọc): màn này mở Xem/Sửa bằng cửa sổ, không có trang con nên bộ lọc KHÔNG được nhớ trong bất kỳ trường hợp nào — rời sang màn khác (kể cả quay lại trước 10 phút) hay F5 đều về mặc định. Expected đang viết theo hiện trạng. Nếu yêu cầu là giữ bộ lọc 10 phút như các màn có trang chi tiết thì phải sửa code và đổi expected các case nhớ bộ lọc.
- [Hỏi] Ô tìm kiếm nhanh không giới hạn độ dài (không chặn ở ô nhập, máy chủ cũng không kiểm) — case độ dài đang viết theo hiện trạng "nhận hết, không báo lỗi". Có cần đặt giới hạn (vd 255 ký tự) không?
- [Hỏi] Bộ lọc màn Phường/Xã không có ô Trạng thái dù danh sách hiện cả bản ghi Khóa — có cần bổ sung không?
- [Code] Dòng tổng "Hiển thị a–b / N" ghi N liền không có dấu phân cách hàng nghìn (vd 3321), lệch quy chuẩn định dạng số toàn hệ thống (1,234) — thành phần bảng dùng chung, không riêng màn này.
## TC cd · 16. DM tỉnhTP
- [Hỏi] Ý 5 (nhớ bộ lọc): màn này mở Xem/Sửa bằng cửa sổ, không có trang con nên bộ lọc KHÔNG được nhớ trong bất kỳ trường hợp nào — rời sang màn khác (kể cả quay lại trước 10 phút) hay F5 đều về mặc định. Expected đang viết theo hiện trạng. Nếu yêu cầu là giữ bộ lọc 10 phút như các màn có trang chi tiết thì phải sửa code và đổi expected các case nhớ bộ lọc.
- [Hỏi] Ô tìm kiếm nhanh không giới hạn độ dài (không chặn ở ô nhập, máy chủ cũng không kiểm) — case độ dài đang viết theo hiện trạng "nhận hết, không báo lỗi". Có cần đặt giới hạn (vd 255 ký tự) không?
- [Code] Dòng tổng "Hiển thị a–b / N" ghi N liền không có dấu phân cách hàng nghìn (vd 3321), lệch quy chuẩn định dạng số toàn hệ thống (1,234) — thành phần bảng dùng chung, không riêng màn này.
## TC cd · 17. DM đườngphố
- [Hỏi] Ý 5 (nhớ bộ lọc): màn này mở Xem/Sửa bằng cửa sổ, không có trang con nên bộ lọc KHÔNG được nhớ trong bất kỳ trường hợp nào — rời sang màn khác (kể cả quay lại trước 10 phút) hay F5 đều về mặc định. Expected đang viết theo hiện trạng. Nếu yêu cầu là giữ bộ lọc 10 phút như các màn có trang chi tiết thì phải sửa code và đổi expected các case nhớ bộ lọc.
- [Hỏi] Ô tìm kiếm nhanh không giới hạn độ dài (không chặn ở ô nhập, máy chủ cũng không kiểm) — case độ dài đang viết theo hiện trạng "nhận hết, không báo lỗi". Có cần đặt giới hạn (vd 255 ký tự) không?
- [Hỏi] Cửa sổ Tạo Đường/Phố gắn dấu * cho Quốc gia, Tỉnh/TP, Quận/Huyện/Thị xã nhưng khi bỏ trống chỉ báo "Bắt buộc phải nhập" dưới ô Phường/xã (máy chủ chỉ bắt buộc Phường/xã). Expected case Lưu và tiếp tục viết theo hiện trạng — xác nhận có cần báo lỗi riêng từng ô không.
- [Code] Dòng tổng "Hiển thị a–b / N" ghi N liền không có dấu phân cách hàng nghìn (vd 3321), lệch quy chuẩn định dạng số toàn hệ thống (1,234) — thành phần bảng dùng chung, không riêng màn này.
- [Code] Đường/Phố: ô Quốc gia, Tỉnh/TP, Quận/Huyện/Thị xã có dấu * nhưng bỏ trống không báo lỗi tại ô đó (chỉ báo ở Phường/xã).
## TC cd · 18. DM quận huyện
- [Hỏi] Ý 5 (nhớ bộ lọc): màn này mở Xem/Sửa bằng cửa sổ, không có trang con nên bộ lọc KHÔNG được nhớ trong bất kỳ trường hợp nào — rời sang màn khác (kể cả quay lại trước 10 phút) hay F5 đều về mặc định. Expected đang viết theo hiện trạng. Nếu yêu cầu là giữ bộ lọc 10 phút như các màn có trang chi tiết thì phải sửa code và đổi expected các case nhớ bộ lọc.
- [Hỏi] Ô tìm kiếm nhanh không giới hạn độ dài (không chặn ở ô nhập, máy chủ cũng không kiểm) — case độ dài đang viết theo hiện trạng "nhận hết, không báo lỗi". Có cần đặt giới hạn (vd 255 ký tự) không?
- [Code] Dòng tổng "Hiển thị a–b / N" ghi N liền không có dấu phân cách hàng nghìn (vd 3321), lệch quy chuẩn định dạng số toàn hệ thống (1,234) — thành phần bảng dùng chung, không riêng màn này.
## TC cd · 19. DM vụ việc 
- [Hỏi] Màn mở Xem/Sửa bằng cửa sổ nổi, không có trang con, nên quy tắc "giữ bộ lọc 10 phút khi vào trang con rồi quay lại" không bao giờ áp dụng: rời màn bằng bất kỳ đường nào (kể cả F5) bộ lọc đều về mặc định. Case TC_02.021/022 viết theo hành vi này — xác nhận có đúng mong muốn không, hay cần giữ bộ lọc khi rời màn?
- [Hỏi] Dòng tổng "Hiển thị a–b / N" in N dạng số trơn, không có dấu phẩy ngăn cách hàng nghìn (vd 1234) — khác quy tắc định dạng số toàn hệ thống; có cần sửa không?
- [Hỏi] TC_03.001 (hàng 55) đang ghi cửa sổ Tạo mới "Chỉ có 2 nút: Lưu và Đóng" nhưng code có 3 nút: Lưu, Lưu và tiếp tục, Đóng — case cũ cần sửa nhưng nằm ngoài 2 loại được phép sửa.
## TC cd · 20. DM nguồn vốn
- [Hỏi] Nhớ bộ lọc: màn Nguồn vốn xem chi tiết bằng cửa sổ bật lên, không có trang con, nên cơ chế giữ bộ lọc 10 phút KHÔNG bao giờ áp dụng — rời màn là mất bộ lọc, quay lại trước hay sau 10 phút đều về mặc định. Testcase TC_02.009–02.010 viết theo hành vi này; xác nhận đây là mong muốn hay cần giữ bộ lọc 10 phút khi rời sang màn khác?
- [Hỏi] Mô tả đầu tab (R10) ghi "Cửa sổ nhập liệu chỉ có 2 nút: Lưu và Đóng, KHÔNG có nút Lưu và tiếp tục" nhưng code hiện có nút "Lưu và tiếp tục" ở cửa sổ Tạo mới (TC_03.013 cũng đã dùng nút này). Cần sửa lại phần mô tả đầu tab cho khớp.
## TC cd · 21. DM mã phí
- [Hỏi] Màn Mã phí khai nhớ bộ lọc 10 phút nhưng chỉ lưu khi đi vào trang con dạng /…/{id} — màn này không có trang con nên thực tế KHÔNG bao giờ nhớ bộ lọc. Có cần nhớ bộ lọc khi rời màn quay lại không? Case TC_02.020–022 đang viết theo hành vi hiện tại (không nhớ).
- [Hỏi] Code hiện có nút "Lưu và tiếp tục" ở cửa sổ Tạo mã phí, trong khi TC_03.001 (Expected "Chỉ có 2 nút: Lưu và Đóng") và ghi chú đầu tab (R10) nói màn KHÔNG có nút này — brief không cho sửa các dòng đó, cần tester/QA cập nhật lại TC_03.001 và ghi chú R10.
- [Hỏi] Ô tìm nhanh không giới hạn độ dài; có cần đặt giới hạn (vd 255 ký tự) không?
- [Code] Ô tìm nhanh không có giới hạn độ dài (V2BaseSmartFilterPanel không đặt maxlength).
- [Code] Dòng tổng "Hiển thị a–b / N" in N thô, không có dấu phẩy ngăn hàng nghìn theo chuẩn định dạng số toàn hệ thống (chỉ ảnh hưởng khi > 999 mã phí).
## TC cd · 22. DM công việc, lỗi thiết bị
- [Hỏi] TC_02.035: bộ lọc được lưu trên trình duyệt theo màn, KHÔNG theo tài khoản — A vào trang chi tiết rồi đăng xuất, B đăng nhập trong 10 phút sẽ thấy bộ lọc của A. Expected đang viết theo hành vi đúng mong đợi (B thấy mặc định); xác nhận có cần sửa code không?
- [Hỏi] TC_02.036: tab mới dùng chung bộ lọc đã lưu của tab khác trong 10 phút — chấp nhận như hiện tại hay muốn mỗi tab độc lập?
- [Hỏi] TC_02.031: ô tìm kiếm không giới hạn độ dài — có cần đặt giới hạn (vd 255 ký tự) không?
- [Hỏi] TC_07.010: hạng mục đã bị xóa thì hệ thống hiện câu 'Item Not Found!' (tiếng Anh). Expected viết 'báo lỗi tiếng Việt cho biết hạng mục không còn tồn tại' — cần chốt câu chữ.
- [Hỏi] TC_07.011: Mở khóa bản ghi đang Hoạt động vẫn báo thành công và ghi thêm 1 dòng lịch sử 'Hoạt động → Hoạt động'. Có muốn chặn (báo 'dữ liệu đã thay đổi' như thao tác Khóa) không?
- [Hỏi] TC_01.001: số dòng mặc định của màn là 20 (khác 10 của quy tắc chung) — giữ 20?
- [Code] Mở khóa hạng mục đã bị xóa: thông báo 'Item Not Found!' tiếng Anh, danh sách không tự tải lại (TC_07.010).
- [Code] Mở khóa hạng mục đã Hoạt động: không kiểm trạng thái, vẫn báo thành công và ghi dòng lịch sử thừa (TC_07.011).
- [Code] Bộ lọc nhớ theo trình duyệt chứ không theo tài khoản: tài khoản sau thấy bộ lọc của tài khoản trước nếu tài khoản trước đăng xuất từ trang chi tiết trong 10 phút (TC_02.035).
## TC qlda · 1.DM Ứng dụng
- [Hỏi] Màn Ứng dụng mở Xem/Sửa bằng popup, không có trang con nên bộ lọc KHÔNG được nhớ khi rời màn (kể cả quay lại trong 10 phút) và F5 cũng về mặc định — expected đang viết theo hành vi này; xác nhận đây là hành vi mong muốn hay cần nhớ bộ lọc 10 phút cả khi sang màn khác.
- [Hỏi] Ô tìm nhanh không giới hạn số ký tự (giao diện và máy chủ đều không chặn) — có cần đặt giới hạn (vd 255 ký tự) không?
- [Hỏi] Dòng 34 "Sort mặc định Cập nhật DESC": code sắp theo thứ tự tạo (mới tạo nhất lên đầu), không theo ngày cập nhật — tên case cũ chưa khớp, không thuộc 2 loại được phép sửa nên giữ nguyên.
- [Code] Bộ lọc màn danh sách: đổi Nhóm ngành thì Nhóm giải pháp đã chọn KHÔNG tự xoá dù không thuộc nhóm ngành mới (cặp Loại hình → Lĩnh vực thì có tự xoá) — expected viết theo hành vi đúng (tự xoá).
- [Code] Mở khoá bản ghi đã được người khác mở khoá: máy chủ không chặn (chỉ kiểm nhóm giải pháp cha còn hoạt động) → vẫn báo "Mở khóa thành công" và ghi thêm lịch sử; expected viết hành vi đúng mong đợi "Dữ liệu đã thay đổi, vui lòng tải lại".
- [Code] Import (#11588) chưa áp cho màn này: lúc Import, dòng trùng Mã với bản ghi vừa tạo ở tab khác sẽ GHI ĐÈ bản ghi đó (nhập theo kiểu cập nhật theo mã); dòng trùng Tên thì bị bỏ qua nhưng các dòng khác vẫn được ghi, popup đóng và chỉ báo "Import thành công x/y ứng dụng. n ứng dụng thất bại." — không giữ popup, không tô đỏ dòng lỗi.
## TC qlda · 2.DM Nhóm ngành
- [Hỏi] TC ID tab này là chuỗi cố định, đánh số không theo nhóm (đã trùng số ở nhóm Khóa/Mở khóa) — case mới đánh tiếp từ số lớn nhất của tab (TC-ROLE-111 trở đi) theo thứ tự hàng; cần đánh số khác thì báo.
- [Hỏi] Màn mở Xem/Sửa bằng popup, không có trang con nên bộ lọc KHÔNG được nhớ khi rời màn (kể cả quay lại trong 10 phút), F5 cũng về mặc định — expected viết theo hành vi này; xác nhận có đúng mong muốn không.
- [Hỏi] Ô tìm nhanh không giới hạn số ký tự — có cần đặt giới hạn không?
- [Code] Mở khoá nhóm ngành đã được người khác mở khoá: máy chủ không kiểm trạng thái hiện tại → vẫn báo "Mở khóa thành công" và ghi thêm lịch sử; expected viết hành vi đúng "Dữ liệu đã thay đổi, vui lòng tải lại".
- [Code] Import (#11588) chưa áp cho màn này: lúc Import máy chủ kiểm lại, BỎ QUA dòng trùng và vẫn ghi các dòng còn lại, popup đóng, chỉ báo "Import thành công x/y nhóm ngành. n nhóm ngành thất bại." — không giữ popup, không tô đỏ dòng lỗi.
## TC qlda · 3.DM Nhóm giải pháp
- [Hỏi] TC ID tab này là chuỗi cố định, số không theo nhóm (đã trùng ở nhóm Khóa/Xóa) — case mới đánh tiếp từ số lớn nhất của tab (TC-ROLE-98 trở đi).
- [Hỏi] Màn mở Xem/Sửa bằng popup, không có trang con nên bộ lọc KHÔNG được nhớ khi rời màn (kể cả quay lại trong 10 phút), F5 cũng về mặc định — expected viết theo hành vi này; xác nhận có đúng mong muốn không.
- [Hỏi] Ô tìm nhanh không giới hạn số ký tự — có cần đặt giới hạn không?
- [Code] Mở khoá nhóm giải pháp đã được người khác mở khoá: máy chủ không kiểm trạng thái hiện tại → vẫn báo "Mở khóa thành công" và ghi thêm lịch sử; expected viết hành vi đúng "Dữ liệu đã thay đổi, vui lòng tải lại".
- [Code] Import (#11588) chưa áp cho màn này: lúc Import máy chủ kiểm lại, BỎ QUA dòng trùng và vẫn ghi các dòng còn lại, popup đóng, chỉ báo "Import thành công x/y nhóm giải pháp. n nhóm giải pháp thất bại." — không giữ popup, không tô đỏ dòng lỗi.
## TC qlda · 4.DM Vai trò dự án
- [Hỏi] ⚠️ Tab này lệch cột: I = Test Data (trùng H), Expected nằm ở cột J. Sửa ý 3 đã ghi col "J". Case chèn mới cần dán lệch 1 cột so với mặc định (C..H như thường, I = Test Data (chép lại "data"), J = Expected) — script chèn mặc định ghi C..I sẽ đặt Expected vào cột I.
- [Hỏi] TC ID tab này là chuỗi cố định, số không theo nhóm — case mới đánh tiếp từ số lớn nhất của tab (TC-ROLE-93 trở đi).
- [Hỏi] Màn mở Xem/Sửa bằng popup, không có trang con nên bộ lọc KHÔNG được nhớ khi rời màn (kể cả trong 10 phút), F5 cũng về mặc định — xác nhận đúng mong muốn.
- [Hỏi] Ô tìm nhanh không giới hạn số ký tự — có cần đặt giới hạn không?
- [Code] Mở khoá vai trò đã được người khác mở khoá: máy chủ chỉ kiểm vai trò cha còn khoá không, không kiểm trạng thái hiện tại → vẫn báo "Mở khóa thành công" và ghi thêm lịch sử; expected viết hành vi đúng "Dữ liệu đã thay đổi, vui lòng tải lại".
- [Code] Import (#11588) chưa áp cho màn này: lúc Import máy chủ kiểm lại, BỎ QUA dòng trùng tên và vẫn ghi các dòng còn lại, popup đóng, chỉ báo "Import thành công x/y vai trò dự án. n vai trò dự án thất bại." — không giữ popup, không tô đỏ dòng lỗi.
## TC qlda · 5.DM Giai đoạn dự án
- [Hỏi] TC ID tab này là chuỗi cố định — case mới đánh tiếp từ số lớn nhất của tab (TC-ROLE-85 trở đi).
- [Hỏi] Màn danh sách mở Xem/Sửa bằng popup (có sẵn trang chi tiết riêng trong code nhưng danh sách không dẫn sang), nên bộ lọc KHÔNG được nhớ khi rời màn, F5 cũng về mặc định — expected viết theo hành vi này; xác nhận đúng mong muốn.
- [Hỏi] Ô tìm nhanh không giới hạn số ký tự — có cần đặt giới hạn không?
- [Hỏi] Dòng 101 (thanh top-scroll) có cột Expected đang ghi "Bảng rộng (scroll ngang)" — nghi lệch cột, không thuộc phạm vi sửa nên để nguyên.
- [Code] Mở khoá giai đoạn đã được người khác mở khoá: máy chủ không kiểm trạng thái hiện tại → vẫn báo "Mở khóa thành công" và ghi thêm lịch sử; expected viết hành vi đúng "Dữ liệu đã thay đổi, vui lòng tải lại".
- [Code] Import (#11588) chưa áp cho màn này: lúc Import máy chủ kiểm lại, BỎ QUA dòng trùng và vẫn ghi các dòng còn lại, popup đóng, chỉ báo "Import thành công x/y giai đoạn dự án. n giai đoạn dự án thất bại." — không giữ popup, không tô đỏ dòng lỗi.
## TC qlda · 6.DM Lý do thất bại
- [Hỏi] TC ID tab này là chuỗi cố định — case mới đánh tiếp từ số lớn nhất của tab (TC-ROLE-81 trở đi).
- [Hỏi] Nhóm Import của tab đang ghi Nhóm chức năng = "Export" cho các dòng Import (ô gộp B84:B91) — case Import mới để theo ô gộp đó; có muốn đổi thành "Import" không?
- [Hỏi] Màn mở Xem/Sửa bằng popup, không có trang con nên bộ lọc KHÔNG được nhớ khi rời màn (kể cả trong 10 phút), F5 cũng về mặc định — xác nhận đúng mong muốn.
- [Hỏi] Ô tìm nhanh không giới hạn số ký tự — có cần đặt giới hạn không?
- [Code] Mở khoá nguyên nhân đã được người khác mở khoá: máy chủ không kiểm trạng thái hiện tại → vẫn báo "Mở khóa thành công" và ghi thêm lịch sử; expected viết hành vi đúng "Dữ liệu đã thay đổi, vui lòng tải lại".
- [Code] Import (#11588) chưa áp cho màn này: lúc Import máy chủ kiểm lại, BỎ QUA dòng trùng và vẫn ghi các dòng còn lại, popup đóng, chỉ báo "Import thành công x/y nguyên nhân thất bại. n nguyên nhân thất bại thất bại." — không giữ popup, không tô đỏ dòng lỗi.
## TC qlda · 7.DM Lĩnh vực khách hàng
- [Hỏi] TC ID tab này là chuỗi cố định — case mới đánh tiếp từ số lớn nhất của tab (TC-ROLE-123 trở đi).
- [Hỏi] Tab có 2 khối Import (nhóm KBKT dòng 92–100 và khối "UPDATE NỘI DUNG 4/6/2026" dòng 114–122); case Import mới đặt cuối nhóm KBKT (sau dòng 100). Muốn đặt vào khối cập nhật 4/6 thì đổi after_row = 122.
- [Hỏi] Tiền tố mã thực tế trong code là "LVKDKH." (case cũ còn ghi "LVKH.") — case mới viết theo "LVKDKH.".
- [Hỏi] Màn mở Xem/Sửa bằng popup, không có trang con nên bộ lọc KHÔNG được nhớ khi rời màn (kể cả trong 10 phút), F5 cũng về mặc định — xác nhận đúng mong muốn.
- [Hỏi] Ô tìm nhanh không giới hạn số ký tự — có cần đặt giới hạn không?
- [Code] Mở khoá lĩnh vực đã được người khác mở khoá: máy chủ không kiểm trạng thái hiện tại → vẫn báo "Mở khóa thành công" và ghi thêm lịch sử; expected viết hành vi đúng "Dữ liệu đã thay đổi, vui lòng tải lại".
- [Code] Import (#11588) chưa áp cho màn này: lúc Import máy chủ kiểm lại, BỎ QUA dòng trùng và vẫn ghi các dòng còn lại, popup đóng, chỉ báo "Import thành công x/y lĩnh vực kinh doanh khách hàng. n lĩnh vực thất bại." — không giữ popup, không tô đỏ dòng lỗi.
## TC qlda · 7.1 DM nhóm Lĩnh vực khách hàng
- [Hỏi] Tiêu đề nhóm tab này không có tiền tố "KBKT_" (vd "Tìm kiếm & Lọc", "Khoá / Mở khoá"); TC ID chuỗi cố định — case mới đánh tiếp TC-ROLE-85 trở đi.
- [Hỏi] Màn mở Xem/Sửa bằng popup, không có trang con nên bộ lọc KHÔNG được nhớ khi rời màn (kể cả trong 10 phút), F5 cũng về mặc định — xác nhận đúng mong muốn.
- [Hỏi] Ô tìm nhanh không giới hạn số ký tự — có cần đặt giới hạn không?
- [Code] Mở khoá loại hình đã được người khác mở khoá: máy chủ không kiểm trạng thái hiện tại → vẫn báo "Mở khoá thành công" và ghi thêm lịch sử; expected viết hành vi đúng "Dữ liệu đã thay đổi, vui lòng tải lại".
- [Code] Import (#11588) chưa áp cho màn này: lúc Import máy chủ kiểm lại, BỎ QUA dòng trùng và vẫn ghi các dòng còn lại, popup đóng, chỉ báo "Import thành công x/y loại hình hoạt động khách hàng. n loại hình thất bại." — không giữ popup, không tô đỏ dòng lỗi.
- [Code] File danh sách khai trùng 2 bộ hàm xoá/khoá (dòng ~884-935 và ~1232-1290) — bộ khai sau đang có hiệu lực; không ảnh hưởng câu thông báo nhưng nên dọn.
## TC qlda · 8.DM Hạng mục dự án
- [Hỏi] TC ID tab này là chuỗi cố định — case mới đánh tiếp từ số lớn nhất của tab (TC-ROLE-84 trở đi).
- [Hỏi] Màn mở Xem/Sửa bằng popup, không có trang con nên bộ lọc KHÔNG được nhớ khi rời màn (kể cả trong 10 phút), F5 cũng về mặc định — xác nhận đúng mong muốn.
- [Hỏi] Ô tìm nhanh không giới hạn số ký tự — có cần đặt giới hạn không?
- [Hỏi] Dòng 100 (thanh top-scroll) cột Expected đang ghi "Bảng rộng (scroll ngang)" — nghi lệch cột, không thuộc phạm vi sửa nên để nguyên.
- [Code] Mở khoá hạng mục đã được người khác mở khoá: máy chủ không kiểm trạng thái hiện tại → vẫn báo "Mở khóa thành công" và ghi thêm lịch sử; expected viết hành vi đúng "Dữ liệu đã thay đổi, vui lòng tải lại".
- [Code] Import (#11588) chưa áp cho màn này: lúc Import máy chủ kiểm lại, BỎ QUA dòng trùng tên và vẫn ghi các dòng còn lại, popup đóng, chỉ báo "Import thành công x/y hạng mục dự án. n hạng mục dự án thất bại." — không giữ popup, không tô đỏ dòng lỗi.
## TC qlda · 9.DM Loại meeting
- [Hỏi] Mã TC của tab là số chạy toàn tab (TC-ROLE-01…83), không đánh theo nhóm — case mới đánh tiếp từ TC-ROLE-84 để không trùng mã đang có.
- [Hỏi] Mở khóa một loại meeting đã được người khác mở khóa trước: hệ thống vẫn báo "Mở khóa thành công" (không báo dữ liệu đã thay đổi) và ghi thêm 1 dòng lịch sử. Có cần chặn và báo "Dữ liệu đã thay đổi, vui lòng tải lại" như khi Khóa không?
- [Hỏi] Ô tìm nhanh không giới hạn độ dài — có cần đặt giới hạn (vd 255 ký tự) không?
- [Hỏi] Bộ lọc của màn chỉ được lưu khi vào trang con /assign/meeting_type/{id}, nhưng màn không có trang con nên thực tế không bao giờ nhớ bộ lọc. Xác nhận hành vi mong muốn là luôn về mặc định khi rời màn.
- [Code] Import Loại meeting chưa theo #11588: khi bấm Import mà 1 dòng vừa bị trùng (tạo ở tab khác sau lúc Validate), hệ thống vẫn ghi các dòng còn lại, báo "Import thành công x/y loại meeting. n loại meeting thất bại." và đóng popup; nếu file chỉ có dòng lỗi thì báo "Không có dữ liệu hợp lệ để import" nhưng không tô đỏ dòng. Màn không dùng CatalogImportMixin/markRejectedImportRows.
## TC qlda · 10.Câu hỏi thu thập thông tin
- [Hỏi] TC ID tab này là chữ (TC-ROLE-NN tăng liên tục toàn tab, tới TC-ROLE-131), không phải công thức; case mới đánh tiếp TC-ROLE-132… theo thứ tự hàng nên số không liền mạch trong nhóm. Nếu muốn đánh lại toàn tab thì báo.
- [Hỏi] Nhớ bộ lọc lưu chung trên trình duyệt, không theo tài khoản: A vào màn Chi tiết rồi đăng xuất, B đăng nhập trong 10 phút sẽ thấy bộ lọc của A. Case viết expected theo hành vi đúng (B thấy mặc định) — cần xác nhận/sửa code.
- [Hỏi] Tương tự, mở tab mới trong lúc tab 1 đang ở màn Chi tiết (chưa quá 10 phút) thì tab mới nhận bộ lọc của tab 1. Có chấp nhận không?
- [Hỏi] Bấm 'Tạo mới' (sang màn Tạo mới câu hỏi) rồi quay lại thì bộ lọc bị xoá (chỉ màn Chi tiết/Sửa mới giữ). Có đúng ý không?
- [Hỏi] Mở khoá bản ghi đã bị xoá chỉ báo chung 'Mở khóa thất bại' (không nói rõ dữ liệu đã thay đổi); mở khoá bản ghi đã được mở khoá vẫn báo thành công. Có cần câu báo 'Dữ liệu đã thay đổi, vui lòng tải lại' như màn Loại giảm giá không?
- [Code] Nhớ bộ lọc không tách theo tài khoản: tài khoản B có thể nhận bộ lọc tài khoản A để lại trên cùng trình duyệt (khoá lưu 'assign_questions' dùng chung)
## TC qlda · 13.Mẫu phiếu TTTT
- [Hỏi] Tab lệch cột (Bước ở cột H, Expected ở cột J, TC ID ở cột D, tiêu đề nhóm ở cột A) — edits dùng H/J, cases cần ghi theo col_map.
- [Hỏi] TC ID trong tab đánh trùng/không liền mạch giữa các nhóm (vd TC-ROLE-41..44, 59 lặp lại; khối Import đánh lại từ 01) nên case mới đánh tiếp từ số lớn nhất toàn tab: TC-ROLE-228 → 237.
- [Hỏi] Ý 3 sửa cả R13 (TC-ROLE-05 gốc) và R126 (bản cập nhật 16/06 của chính TC-ROLE-05) cho đồng nhất; nội dung cũ về cột/bộ lọc Nhóm ngành, Nhóm giải pháp đã không còn đúng nên viết lại theo màn hiện tại.
- [Hỏi] Sắp xếp mặc định theo code là Ngày cập nhật mới nhất → cũ nhất (không phải ngày tạo) — đã ghi đúng theo code.
- [Hỏi] Bộ lọc nhớ trên trình duyệt, không tách theo tài khoản: nếu User A đăng xuất ngay ở màn Chi tiết thì User B đăng nhập trong 10 phút sẽ thấy bộ lọc của A. TC-ROLE-233 viết theo hành vi đúng (B thấy mặc định) — xác nhận?
- [Hỏi] Mở tab mới khi tab 1 đang đứng ở màn Chi tiết (vừa rời danh sách) thì tab mới sẽ nhận bộ lọc của tab 1 trong 10 phút — có coi là lỗi không? (TC-ROLE-234 chỉ viết trường hợp tab 1 còn ở màn danh sách)
- [Hỏi] Mở khoá mẫu phiếu đã được người khác mở khoá trước: code vẫn báo "Mở khoá mẫu phiếu thành công" và ghi đè người cập nhật; TC-ROLE-236 viết theo hướng cảnh báo dữ liệu đã thay đổi — cần chốt câu thông báo.
- [Hỏi] Ô Tìm kiếm nhanh không có giới hạn độ dài — có cần chặn không?
- [Code] Mở khoá/Khoá mẫu phiếu không kiểm trạng thái hiện tại: mở khoá mẫu đã Hoạt động vẫn báo thành công, ghi đè Người cập nhật (TC-ROLE-236)
- [Code] Bộ lọc lưu chung trên trình duyệt, không tách theo tài khoản (TC-ROLE-233)
- [Code] Thao tác trên mẫu phiếu đã bị xoá trả về câu tiếng Anh "Item Not Found!" thay vì thông báo tiếng Việt
## TC qlda · 16.DM Loại tài liệu
- [Hỏi] Mã TC của tab là số chạy toàn tab (đang có TC-ROLE-01…76, có mã trùng 18/19), case mới đánh tiếp từ TC-ROLE-77.
- [Hỏi] Mở khóa một loại tài liệu đã được người khác mở khóa trước: hệ thống vẫn báo "Mở khóa thành công" và ghi thêm lịch sử. Có cần báo "Dữ liệu đã thay đổi, vui lòng tải lại" không?
- [Hỏi] Ô tìm nhanh không giới hạn độ dài — có cần đặt giới hạn không?
- [Hỏi] Bộ lọc màn hiện không có ô Trạng thái (chỉ Người tạo, Người cập nhật, Ngày tạo, Ngày cập nhật) nhưng case TC-ROLE-15 (R24) vẫn test 'Lọc theo trạng thái' — cần tester rà lại case cũ này.
- [Hỏi] Bộ lọc chỉ được lưu khi vào trang con /assign/attachment-type/{id} mà màn không có trang con → thực tế không nhớ bộ lọc. Xác nhận hành vi mong muốn.
## TC qlda · 49. DM Khách hàng
- [Hỏi] Bộ lọc Quốc gia và Tỉnh/Thành phố ở màn danh sách hiện KHÔNG liên kết (ô Tỉnh luôn liệt kê tỉnh mọi quốc gia, đổi Quốc gia không xoá Tỉnh). Case TC_02.024 viết theo hành vi mong đợi (liên kết) — có chốt cần liên kết không?
- [Hỏi] Bộ lọc chỉ được nhớ khi vào màn Sửa/Quản lý rồi quay lại; vào 'Tạo mới' rồi Quay lại thì bộ lọc bị xoá. Trang đang xem và số dòng/trang cũng không được nhớ. Có cần nhớ thêm không?
- [Hỏi] Các tab trên cùng trình duyệt dùng chung phần nhớ bộ lọc (TC_02.022 bước 6 tab 2 nhận bộ lọc của tab 1) — chấp nhận hay cần tách theo tab?
- [Hỏi] Mở khoá khách hàng đã được người khác mở khoá: hệ thống vẫn báo 'Mở khóa khách hàng thành công!' (không cảnh báo dữ liệu đã thay đổi) — giữ hay cần báo 'Dữ liệu đã thay đổi, vui lòng tải lại'?
- [Hỏi] Ô tìm nhanh không giới hạn độ dài — có cần đặt giới hạn (vd 255 ký tự) không?
- [Hỏi] Phần MÔ TẢ (R16) và TC_01005/TC_07.x vẫn ghi 'màn không có UI khóa/mở khóa', 'không có Import' — đã lệch code (nay có Khóa/Mở khóa, Import, Lịch sử); không thuộc phạm vi sửa lần này
- [Code] Import khách hàng (#11588): khi bấm Import mà có dòng không còn hợp lệ, hệ thống vẫn ghi các dòng còn lại (import một phần), đóng cửa sổ và báo 'Import thành công x/y khách hàng. n khách hàng thất bại.' — chưa có chặn 'không import dòng nào, giữ popup, tô đỏ dòng lỗi' (pages/assign/customers không dùng CatalogImportMixin; CustomerController::import trả 207)
- [Code] Bộ lọc danh sách: Quốc gia không lọc ô Tỉnh/Thành phố (provinceOptions nạp không theo nation_id) và đổi Quốc gia không xoá Tỉnh đã chọn
- [Code] Dòng tổng dưới bảng in tổng số bản ghi không có dấu phân cách hàng nghìn (vd 43520) — lệch quy tắc định dạng số chuẩn quốc tế
## TC qlda · 50. DM Loại chiết khấu
- [Hỏi] Màn Loại giảm giá không có trang con (Xem/Sửa đều là popup) nên cơ chế giữ bộ lọc 10 phút không bao giờ kích hoạt: rời sang màn khác là mất bộ lọc. Có cần giữ bộ lọc khi rời sang màn khác rồi quay lại không? Hiện viết expected theo code (về mặc định).
- [Hỏi] Mở khoá bản ghi đã được người khác mở khoá trước: hệ thống vẫn báo 'Mở khóa thành công' (không cảnh báo bản ghi đã ở trạng thái Hoạt động). Có cần báo 'Dữ liệu đã thay đổi, vui lòng tải lại' như trường hợp bị xoá không?
- [Hỏi] Case TC_02.007 ghi nút 'Đặt lại' nhưng nút trên màn là 'Làm mới' (không sửa vì ngoài phạm vi 2 loại dòng được sửa).
## TC qlda · 51. DM Danh sách lĩnh vực Công 
- [Hỏi] Màn này dùng cửa sổ (popup) cho Xem/Sửa nên không có trang con: bộ lọc KHÔNG được nhớ khi rời màn (kể cả quay lại trong 10 phút) và mất khi F5 — tester hỏi 'giữ bao nhiêu phút' thì ở màn này là không giữ. Có cần nhớ bộ lọc khi rời màn không?
- [Hỏi] Mở khoá bản ghi đã được người khác mở khoá: hệ thống vẫn báo 'Mở khóa thành công' (không cảnh báo dữ liệu đã thay đổi) — giữ hay cần báo 'Dữ liệu đã thay đổi, vui lòng tải lại'?
- [Hỏi] Ô tìm nhanh không giới hạn độ dài — có cần đặt giới hạn không?
- [Hỏi] Ô tìm nhanh, ô Mã, ô Tên chỉ lọc khi nhấn Enter / bấm Tìm kiếm, trong khi TC_02.001 hiện ghi 'không cần bấm nút tìm, bảng tự lọc' — case cũ đã lệch code (không thuộc phạm vi sửa lần này)
- [Code] Import lĩnh vực Công ty kinh doanh (#11588): bấm Import mà có dòng không còn hợp lệ thì hệ thống vẫn ghi các dòng còn lại (import một phần), đóng cửa sổ và báo 'Import thành công x/y lĩnh vực Công ty kinh doanh. n lĩnh vực thất bại.' — chưa có chặn 'không import dòng nào, giữ popup, tô đỏ dòng lỗi' (pages/assign/internal-business-scopes không dùng CatalogImportMixin; InternalBusinessScopeController::import trả 207)
- [Code] Dòng tổng dưới bảng in tổng số bản ghi không có dấu phân cách hàng nghìn — lệch quy tắc định dạng số (chỉ lộ khi > 999 bản ghi)
## TC qlda · 53. DM lý do hủy cuộc họp
- [Hỏi] Màn không có trang con (Xem/Sửa là cửa sổ) nên mốc 'giữ bộ lọc 10 phút khi vào trang con rồi quay lại' không áp dụng; code đang khai đường giữ bộ lọc trỏ nhầm sang màn 'Lý do dự án thất bại' — xác nhận hành vi đúng là KHÔNG giữ bộ lọc khi rời màn (TC_02.025)?
- [Hỏi] Mở khóa một lý do đã được người khác mở khóa trước: code hiện báo 'Mở khóa thành công' (không kiểm trạng thái), trong khi Khóa lý do đã bị khóa trước lại báo 'Dữ liệu đã thay đổi, vui lòng tải lại'. TC_05.011 viết theo hướng nhất quán với Khóa — xác nhận?
- [Hỏi] Thêm/Lưu và tiếp tục trùng tên: code hiện thông báo chung 'Bạn chưa nhập đầy đủ thông tin' kèm lỗi đỏ dưới ô (câu thông báo không khớp lỗi trùng) — giữ nguyên hay đổi câu?
- [Hỏi] Ô chọn Số dòng/trang theo code có 5 mức 5 · 10 · 20 · 50 · 100 (TC_03.007 đang ghi 4 mức); dòng tổng theo code là 'Hiển thị 1–10 / 12' không kèm chữ 'lý do' (nhiều case cũ ghi '… / 12 lý do') — các case cũ không thuộc phạm vi sửa lần này.
- [Hỏi] Ô tìm nhanh không có giới hạn độ dài (TC_02.024 viết theo hiện trạng) — có cần chặn số ký tự tối đa không?
- [Code] Import (#11588): màn Lý do hủy cuộc họp chưa dùng cơ chế chặn — bấm Import khi có dòng vừa bị tạo trùng thì máy chủ vẫn nhập các dòng còn hợp lệ (báo 'Import thành công x/y … n dòng lỗi.' và đóng cửa sổ), hoặc chỉ báo 'Không có dữ liệu hợp lệ để import' nếu không còn dòng nào; không tô đỏ dòng lỗi (TC_08.022)
- [Code] Mở khóa không kiểm trạng thái hiện tại: mở khóa lý do đã Hoạt động vẫn báo thành công và ghi lịch sử thêm 1 lần (TC_05.011)
- [Code] Đường giữ bộ lọc của màn khai nhầm sang màn 'Lý do dự án thất bại' (pathsToKeep)
## SRS · Danh mục serial thiết bị làm dịch vụ
- [Code] Màn không có chức năng Import: danh mục CHỈ ĐỌC (xem, lọc, tùy chỉnh cột, Xuất Excel); thêm/sửa/xóa serial làm ở màn Quản lý khách hàng – tab Trang thiết bị. Máy chủ chỉ có đường xem danh sách và tùy chọn lọc. SRS hiện tại đã ghi đúng (BR-01 nêu không có Import Excel) — không cần bổ sung.
## SRS · Danh mục tài khoản
- [Hỏi] Import có cần chặn Tài khoản mẹ / Loại tài khoản đang Khóa giống form Thêm mới không? Code hiện cho qua.
- [Hỏi] Có cần bắt buộc Bậc khớp độ dài Số tài khoản (3 số = Bậc 1, 4 số = Bậc 2, 5 số = Bậc 3) khi Import như quy tắc gợi ý ở Thêm mới không? Code hiện không kiểm.
- [Code] Lịch sử Tạo mới của tài khoản (cả Thêm mới lẫn Import) không phải là một bản ghi lịch sử riêng: chức năng Xem lịch sử tự dựng dòng Tạo mới từ người tạo + thời điểm tạo của tài khoản. Hiển thị đúng, nhưng khác cơ chế với các danh mục ghi lịch sử thật (vd Tiền tệ).
- [Code] Import KHÔNG kiểm tra trạng thái: chấp nhận Tài khoản mẹ đang Khóa và Loại tài khoản đang Khóa, trong khi form Thêm mới chỉ cho chọn tài khoản mẹ/loại đang Hoạt động.
- [Code] File mẫu là file tĩnh có sẵn (không sinh theo khuôn chung): không có cột STT, không có hàng mô tả, không có ô chọn cho cột Theo dõi công nợ — lệch quy ước file mẫu import dùng chung.
- [Code] Dòng ví dụ 3 của file mẫu dùng Loại tài khoản “TKTS”/“Tài khoản tài sản” — chỉ hợp lệ nếu danh mục loại tài khoản có mã/tên đó; số tài khoản ví dụ 8888 có 4 chữ số nhưng là Bậc 1 (khác quy tắc tự gợi ý bậc ở Thêm mới).
## SRS · Lĩnh vực kinh doanh khách hàng
- [Hỏi] Bỏ trống ô bắt buộc đang làm hỏng cả lượt Validate với câu chung “Bắt buộc phải nhập”: sửa code để báo theo từng dòng như SRS đang ghi, hay sửa SRS theo hành vi hiện tại?
- [Code] Ô bắt buộc (Mã, Tên, Trạng thái) bỏ trống ở bất kỳ dòng nào: hệ thống từ chối CẢ lượt Validate với câu chung “Bắt buộc phải nhập” (không chỉ ra dòng/cột nào, không tô đỏ dòng); các câu lỗi theo dòng kiểu “… không được để trống / … là bắt buộc” mà SRS ghi hiện KHÔNG bao giờ hiện ra. Ngoài ra danh sách cột bắt buộc khai cho cửa sổ Import không được dùng để kiểm tra trước.
- [Code] Chưa có luồng giữ cửa sổ Import và tô đỏ dòng không còn hợp lệ: màn không dùng khuôn import dùng chung; khi bấm Import mà một số dòng hết hợp lệ (dữ liệu đổi giữa lúc Validate và Import), hệ thống vẫn ghi các dòng còn lại, chỉ báo “Import thành công x/y … z … thất bại.”, đóng cửa sổ, không cho biết dòng nào lỗi; nếu không ghi được dòng nào thì chỉ hiện thông báo lỗi chung, cũng không tô đỏ dòng.
- [Code] Câu lỗi trùng “… (dòng n)”: n = thứ tự dòng dữ liệu + 1 (tính dòng tiêu đề là dòng 1, không tính dòng mô tả), lệch 1 so với số # ở bảng xem trước và lệch 2 so với số dòng thật trong Excel.
- [Code] Độ dài Tên/Mô tả đang đếm theo byte chứ không theo ký tự: chữ tiếng Việt có dấu chiếm 2–3 byte nên tên có dấu chỉ khoảng 85–127 ký tự đã bị báo “vượt quá độ dài cho phép (tối đa 255 ký tự)”.
- [Code] Tiêu đề cột Mã và Tên trong file mẫu không có dấu * dù là cột bắt buộc (chỉ cột Trạng thái có *).
- [Code] Giá trị Trạng thái viết “Khoá” (dấu đặt ở chữ a) không được nhận ra, bị báo “Trạng thái không hợp lệ…”; chỉ nhận đúng chữ “Khóa”.
## SRS · Nhóm giải pháp
- [Hỏi] Bỏ trống ô bắt buộc đang làm hỏng cả lượt Validate với câu chung “Bắt buộc phải nhập”: sửa code để báo theo từng dòng như SRS đang ghi, hay sửa SRS theo hành vi hiện tại?
- [Hỏi] Sheet DM_nhomnganh trong file mẫu: có cần sinh từ danh mục Nhóm ngành thật lúc tải file mẫu không, hay bỏ sheet này?
- [Code] Ô bắt buộc (Mã, Tên, Mã Nhóm ngành, Trạng thái) bỏ trống ở bất kỳ dòng nào: hệ thống từ chối CẢ lượt Validate với câu chung “Bắt buộc phải nhập” (không chỉ ra dòng/cột nào, không tô đỏ dòng); các câu lỗi theo dòng kiểu “… không được để trống / … là bắt buộc” mà SRS ghi hiện KHÔNG bao giờ hiện ra. Ngoài ra danh sách cột bắt buộc khai cho cửa sổ Import không được dùng để kiểm tra trước.
- [Code] Chưa có luồng giữ cửa sổ Import và tô đỏ dòng không còn hợp lệ: màn không dùng khuôn import dùng chung; khi bấm Import mà một số dòng hết hợp lệ (dữ liệu đổi giữa lúc Validate và Import), hệ thống vẫn ghi các dòng còn lại, chỉ báo “Import thành công x/y … z … thất bại.”, đóng cửa sổ, không cho biết dòng nào lỗi; nếu không ghi được dòng nào thì chỉ hiện thông báo lỗi chung, cũng không tô đỏ dòng.
- [Code] Câu lỗi trùng “… (dòng n)”: n = thứ tự dòng dữ liệu + 1 (tính dòng tiêu đề là dòng 1, không tính dòng mô tả), lệch 1 so với số # ở bảng xem trước và lệch 2 so với số dòng thật trong Excel.
- [Code] Độ dài Tên/Mô tả đang đếm theo byte chứ không theo ký tự: chữ tiếng Việt có dấu chiếm 2–3 byte nên tên có dấu chỉ khoảng 85–127 ký tự đã bị báo “vượt quá độ dài cho phép (tối đa 255 ký tự)”.
- [Code] Sheet DM_nhomnganh trong file mẫu là danh sách mã giả cố định (NH.TEST1, NN.DIEN, NN.DIEN 2…), không phải danh mục Nhóm ngành thật đang Hoạt động; người dùng chép mã từ đây sẽ bị báo không tồn tại.
- [Code] Giá trị Trạng thái viết “Khoá” (dấu đặt ở chữ a) không được nhận ra, bị báo “Trạng thái không hợp lệ…”; chỉ nhận đúng chữ “Khóa”.
## SRS · Danh mục Đường/Phố
- [Code] Khi đối chiếu tên danh mục cha, hệ thống KHÔNG loại bản ghi đang Khóa: ô chọn trong file mẫu chỉ liệt kê bản ghi đang Hoạt động, nhưng gõ tay đúng tên một tỉnh/TP hoặc phường/xã đang Khóa vẫn Validate qua và Import thành công — lệch với màn Thêm mới (chỉ cho chọn bản ghi đang Hoạt động).
## SRS · Vai trò dự án
- [Code] Chưa có luồng giữ cửa sổ Import và tô đỏ dòng không còn hợp lệ lúc bấm Import: màn không dùng khuôn import chung; khi bấm Import hệ thống kiểm tra lại, dòng nào không còn hợp lệ (vd vừa có người tạo trùng) bị BỎ QUA im lặng, các dòng còn lại vẫn được ghi và báo “Import thành công N …” rồi đóng cửa sổ (N chỉ đếm dòng ghi được, không báo số dòng bị bỏ). Chỉ khi không còn dòng nào hợp lệ mới báo “Không có dữ liệu hợp lệ để import” và giữ cửa sổ, nhưng không đánh dấu lại dòng lỗi trên bảng xem trước.
- [Code] Vai trò cha nằm trong file được chấp nhận chỉ cần dòng đó có Trạng thái “Hoạt động”, kể cả khi chính dòng cha bị lỗi (vd trùng tên hệ thống) → dòng con qua Validate, nhưng cha không được tạo nên con được ghi mà không có vai trò cha, không báo gì.
- [Code] Không kiểm vòng lặp cha–con trong cùng file (A có cha B, B có cha A) → có thể tạo quan hệ vòng.
- [Code] Câu lỗi “… bị trùng lặp trong file import (dòng N)”: N = vị trí dòng trong bảng xem trước + 1 (dòng đầu tiên là 2), không khớp STT cũng không khớp số dòng Excel (dữ liệu bắt đầu từ dòng 3).
- [Code] File mẫu là file tĩnh, không theo khuôn file mẫu chung; ô chọn Vai trò cha chỉ lấy tên ở dòng 3–10 của file.
## SRS · Loại meeting
- [Hỏi] Có cần đổi câu báo trùng thành “… (dòng N)” theo đúng số dòng Excel không? Hiện N = thứ tự dòng trong bảng xem trước + 1.
- [Code] Dòng ghi chú (dòng 2) của file mẫu có ô “Nhập Có / Không” ở cột Loại khách hàng — không khớp dạng dòng ghi chú mà hệ thống tự bỏ qua, nên khi tải file mẫu về điền tiếp mà không xoá dòng 2 thì dòng này bị đọc thành 1 dòng dữ liệu và báo lỗi (người dùng phải Bỏ dòng lỗi). Cần sửa câu ghi chú trong file mẫu (vd “(Có / Không)”).
- [Code] File mẫu là file tĩnh dựng tay, không sinh theo khuôn chung; tiêu đề cột đen không có * đỏ theo khuôn — nằm ngoài phạm vi SRS nhưng nên ghi nhận.
- [Code] Luồng giữ cửa sổ khi Import gặp dòng không còn hợp lệ CHƯA có: Import có dòng hỏng thì vẫn ghi phần hợp lệ, báo “x/y … thất bại” rồi đóng cửa sổ; nếu tất cả hỏng thì chỉ hiện thông báo lỗi chung “Không có dữ liệu hợp lệ để import”, không tô đỏ lại dòng.
## SRS · Danh mục khu vực
- [Code] Khi đối chiếu tên danh mục cha, hệ thống KHÔNG loại bản ghi đang Khóa: ô chọn trong file mẫu chỉ liệt kê bản ghi đang Hoạt động, nhưng gõ tay đúng tên một quốc gia đang Khóa vẫn Validate qua và Import thành công — lệch với màn Thêm mới (chỉ cho chọn bản ghi đang Hoạt động).
## SRS · Danh mục vụ việc
- [Hỏi] Câu “Mã vụ việc bị trùng với dòng N trong file”: N do hệ thống tính = thứ tự dòng dữ liệu + 1 (dòng dữ liệu đầu tiên là “dòng 2”), không khớp STT trên bảng xem trước (1) và cũng không khớp số hàng thật trong Excel (3, vì hàng 2 là dòng mô tả). SRS ghi nguyên chữ “dòng N” hay cần sửa code cho N khớp STT?
## SRS · Danh mục ghi chú kiểm tra bảo dưỡng
- [Hỏi] Mô tả khi import: chốt 255 (khớp form, sửa code) hay 500 (giữ code, sửa SRS)?
- [Hỏi] Ghi “dòng N” trong câu lỗi trùng theo code hiện tại (lệch 1 so với STT) hay sửa code trước?
- [Code] Mô tả: import cho tối đa 500 ký tự nhưng form Thêm/Sửa giới hạn 255 ký tự — lệch quy tắc giữa 2 đường tạo; nếu cột lưu chỉ 255 ký tự thì dòng 256–500 ký tự qua Validate nhưng ghi thất bại lúc Import.
- [Code] Câu lỗi “… bị trùng với dòng N trong file”: N = STT + 1, không khớp STT bảng xem trước cũng không khớp số dòng Excel.
## SRS · Danh mục tiền tệ
- [Hỏi] Import có phải chặn tỷ giá > 999,999.99 như Thêm mới không? (SRS đang ghi có, code chưa chặn → nếu có thì là lỗi code cần sửa.)
- [Code] Import KHÔNG kiểm tra trần Tỷ giá 999,999.99 (Thêm mới/Chỉnh sửa có chặn “Tối đa 999999.99”) — file nhập tỷ giá lớn hơn vẫn qua Validate.
- [Code] Số dòng trong câu báo trùng (“bị trùng với dòng N trong file”) lệch 1 so với số hàng Excel: file mẫu có dữ liệu từ hàng 3 nhưng hệ thống đếm dòng đầu tiên là dòng 2.
- [Code] Tỷ giá ghi theo kiểu Việt Nam “25.000” bị hiểu là 25 (dấu chấm là thập phân) mà không báo lỗi.
## SRS · Cấp dịch vụ bảo dưỡng
- [Hỏi] Khi viết câu lỗi trùng trong file vào SRS, ghi “dòng N” theo đúng code hiện tại (lệch 1 so với STT) hay sửa code cho khớp STT rồi mới ghi?
- [Code] Câu lỗi “Tên cấp bị trùng với dòng N trong file”: N = STT + 1 (STT 1 báo “dòng 2”), không khớp STT ở bảng xem trước cũng không khớp số dòng Excel (STT + 2). Tester đối chiếu sẽ thấy lệch.
## SRS · Danh mục nguồn vốn
- [Hỏi] Câu “Tên nguồn vốn bị trùng với dòng N trong file”: N = thứ tự dòng dữ liệu + 1, không khớp STT trên bảng xem trước và số hàng thật trong Excel. SRS ghi nguyên “dòng N” hay cần sửa code?
- [Hỏi] Màn Thêm mới có chọn Trạng thái (Hoạt động/Khóa) nhưng file import không có cột Trạng thái (luôn Hoạt động) — giữ nguyên như vậy hay cần bổ sung cột Trạng thái cho đồng bộ với Vụ việc / Mã phí?
## SRS · Khách hàng
- [Hỏi] Nhóm khách hàng đang Khóa có được phép import không (hiện cho phép)?
- [Hỏi] Địa danh đang Khóa: giữ câu “không tồn tại trên hệ thống” hay tách câu “đang bị khoá”?
- [Code] Không có luồng giữ cửa sổ tô đỏ dòng không còn hợp lệ khi Import (Ý 1): khách hàng nào không còn hợp lệ lúc Import thì bị bỏ qua, phần còn lại vẫn ghi, cửa sổ đóng với thông báo “Import thành công x/y khách hàng. z khách hàng thất bại.”; nếu tất cả thất bại thì chỉ hiện thông báo lỗi chung trên cửa sổ, không tô đỏ dòng.
- [Code] Nhóm khách hàng không kiểm tra trạng thái — nhóm đang Khóa vẫn import được; trong khi địa danh/ngân hàng đang Khóa lại báo “không tồn tại trên hệ thống” (câu lỗi gây hiểu nhầm).
- [Code] Các cột Fax, Người đại diện, Chức vụ, Địa chỉ xuất hoá đơn, Người liên hệ, Số nhà đường, Số tài khoản, Chủ tài khoản, Chi nhánh không giới hạn độ dài ở bước Validate — nếu quá dài sẽ chỉ lỗi lúc Import với câu lỗi hệ thống.
- [Code] Đối tượng “Tổ chức” được nhận nhưng không có trong danh sách thả xuống của file mẫu (danh sách chỉ có 5 giá trị).
- [Code] Số dòng tối đa: chặn chung 500 dòng mỗi lần (đúng SRS); riêng chức năng còn giới hạn 1,000 dòng không bao giờ chạm tới.
## SRS · Hạng mục dự án
- [Code] Chưa có luồng giữ cửa sổ Import và tô đỏ dòng không còn hợp lệ lúc bấm Import: màn không dùng khuôn import chung; khi bấm Import hệ thống kiểm tra lại, dòng nào không còn hợp lệ (vd vừa có người tạo trùng) bị BỎ QUA im lặng, các dòng còn lại vẫn được ghi và báo “Import thành công N …” rồi đóng cửa sổ (N chỉ đếm dòng ghi được, không báo số dòng bị bỏ). Chỉ khi không còn dòng nào hợp lệ mới báo “Không có dữ liệu hợp lệ để import” và giữ cửa sổ, nhưng không đánh dấu lại dòng lỗi trên bảng xem trước.
- [Code] Độ dài Tên hạng mục khi import đếm theo byte chứ không theo ký tự: tên tiếng Việt có dấu chưa tới 255 ký tự vẫn có thể bị báo “vượt quá độ dài cho phép (tối đa 255 ký tự)” (Giai đoạn/Vai trò dự án đã đếm đúng theo ký tự).
- [Code] Kiểm tra trùng tên khi import chỉ không phân biệt hoa/thường với chữ không dấu: “Đánh giá” và “đánh giá” không bị báo trùng ở bước Validate, sang bước Import có thể ghi thất bại → rơi vào báo “Import thành công x/y … z thất bại”.
- [Code] Câu lỗi “… bị trùng lặp trong file import (dòng N)”: N = vị trí dòng trong bảng xem trước + 1 (dòng đầu tiên là 2), không khớp STT cũng không khớp số dòng Excel (dữ liệu bắt đầu từ dòng 3).
- [Code] File mẫu là file tĩnh, không theo khuôn file mẫu chung (tiêu đề cột bắt buộc không có dấu *, dòng mô tả cột Mô tả chỉ ghi “Text”).
## SRS · Danh mục loại tài khoản
- [Hỏi] Import có phải chặn trùng Tên loại tài khoản như Thêm mới không? (SRS đang ghi có chặn, code chưa chặn → nếu có thì là lỗi code cần sửa.)
- [Code] Import KHÔNG kiểm tra trùng Tên loại tài khoản (cả trong file lẫn với hệ thống), trong khi Thêm mới/Chỉnh sửa chặn trùng tên (“Tên loại tài khoản đã tồn tại”) — import tạo được 2 loại cùng tên.
- [Code] Lịch sử Tạo mới (cả Thêm mới lẫn Import) không phải bản ghi lịch sử riêng: chức năng Xem lịch sử tự dựng dòng Tạo mới từ người tạo + thời điểm tạo của bản ghi.
- [Code] File mẫu là file tĩnh có sẵn (không sinh theo khuôn chung): không có cột STT, không có hàng mô tả, cột Trạng thái không có ô chọn giá trị — lệch quy ước file mẫu import dùng chung.
## SRS · Danh mục tài khoản ngân hàng
- [Hỏi] Có cần chặn ngân hàng/chi nhánh/tiền tệ đang Khóa ở Import cho khớp Thêm mới không? Nếu có thì câu lỗi đề xuất: “Ngân hàng X đang bị khóa”.
- [Code] Import KHÔNG chặn ngân hàng / chi nhánh / tiền tệ đang Khóa (tra cả bản ghi Khóa), trong khi màn Thêm mới chỉ cho chọn bản ghi đang Hoạt động → import được tài khoản gắn ngân hàng/chi nhánh/tiền tệ đã khóa.
## SRS · Danh mục Tỉnh/TP
- [Code] Khi đối chiếu tên danh mục cha, hệ thống KHÔNG loại bản ghi đang Khóa: ô chọn trong file mẫu chỉ liệt kê bản ghi đang Hoạt động, nhưng gõ tay đúng tên một quốc gia/khu vực đang Khóa vẫn Validate qua và Import thành công — lệch với màn Thêm mới (chỉ cho chọn bản ghi đang Hoạt động).
## SRS · Loại hình hoạt động khách hàng
- [Hỏi] Có sửa code để thiếu Mã/Tên/Trạng thái báo lỗi tại dòng (như SRS) không, hay SRS ghi theo hành vi hiện tại?
- [Hỏi] Có sửa file mẫu (thêm * cho cột Tên, đổi “Mã*” thành “Mã loại hình hoạt động KH *”) để khớp bảng xem trước không?
- [Code] Nếu bất kỳ dòng nào trong tệp để trống Mã, Tên hoặc Trạng thái thì code hiện tại từ chối cả lượt Validate (thông báo chung “Bắt buộc phải nhập” trên đầu cửa sổ, không chỉ ra dòng nào) thay vì báo lỗi riêng ở dòng đó; các câu “… không được để trống” trong code không bao giờ hiện ra.
- [Code] File mẫu: tiêu đề cột Tên là “Loại hình hoạt động khách hàng” KHÔNG có dấu * dù là cột bắt buộc; cột Mã ghi “Mã*” (thiếu khoảng trắng, khác chữ trong bảng xem trước).
- [Code] Các dòng ví dụ của file mẫu (LHHDKH.0001 Ngành dệt may…) nhiều khả năng trùng dữ liệu đã có → báo “đã tồn tại” nếu để nguyên.
- [Code] Độ dài Tên (255) và Mô tả (1,000) đang đếm theo byte nên chữ tiếng Việt có dấu bị chặn sớm hơn số ký tự ghi trên SRS.
- [Code] Câu “… bị trùng lặp trong file import (dòng n)”: n = thứ tự dòng dữ liệu + 1, không khớp số dòng Excel lẫn STT bảng xem trước.
- [Code] Trạng thái viết “Khoá” không được nhận, chỉ nhận đúng “Khóa”.
- [Code] Không có luồng giữ cửa sổ tô đỏ dòng không còn hợp lệ khi Import (Ý 1): Import bỏ qua dòng lỗi, ghi phần còn lại, đóng cửa sổ và báo “Import thành công x/y loại hình hoạt động khách hàng. z loại hình thất bại.”
## SRS · Danh mục dịch vụ sửa chữa và chi phí khác
- [Hỏi] Số dòng N trong câu lỗi “bị trùng với dòng N trong file” nên ghi theo STT bảng xem trước hay theo số hàng Excel? Hiện code ra STT + 1.
- [Hỏi] Chống trùng tên áp trên toàn bộ dịch vụ/chi phí không có loại chi phí (gồm cả nhóm chi phí phải trả/bán hàng chưa chuyển sang nếu chúng không có loại) — SRS có cần nói rõ phạm vi trùng không, hay giữ “trong danh mục”?
- [Code] Câu lỗi trùng trong file “… bị trùng với dòng N trong file” đánh số dòng = vị trí dòng dữ liệu + 1 (dòng dữ liệu đầu tiên là “dòng 2”), không khớp STT trên bảng xem trước (1) cũng không khớp số hàng trong Excel (hàng 3, vì hàng 2 là dòng mô tả).
- [Code] Cột “Có tính doanh thu” không bị kiểm tra: gõ sai (vd “abc”) không báo lỗi mà lặng lẽ thành “Không” (Chi phí khác).
## SRS · Lý do thất bại (Nguyên nhân thất bại dự án)
- [Hỏi] Mô tả khi import: chốt giới hạn 255 ký tự (khớp ô Mô tả ở cửa sổ Tạo mới và nơi lưu) hay nới nơi lưu lên 1,000 ký tự?
- [Hỏi] Có cần bổ sung luồng giữ cửa sổ + tô đỏ dòng lỗi khi Import (như Ý 1) cho màn này không, thay cho cách hiện tại là ghi dòng hợp lệ rồi đóng cửa sổ?
- [Code] Ý 1 (giữ cửa sổ, tô đỏ dòng lỗi khi Import): CHƯA có. Màn không dùng CatalogImportMixin; khi bấm Import mà có dòng không còn hợp lệ, hệ thống vẫn ghi các dòng hợp lệ rồi báo cảnh báo x/y và ĐÓNG cửa sổ; nếu không còn dòng nào hợp lệ thì chỉ báo “Không có dữ liệu hợp lệ để import”, cửa sổ còn mở nhưng không tô đỏ dòng lỗi.
- [Code] Mô tả: bước kiểm tra cho tối đa 1,000 ký tự nhưng nơi lưu chỉ 255 ký tự → dòng có Mô tả 256–1,000 ký tự qua Validate nhưng ghi thất bại lúc Import (bị tính vào số “thất bại”, không có câu báo dễ hiểu).
- [Code] Tiêu đề cột “Nguyên nhân thất bại” trong file mẫu KHÔNG có dấu * dù là cột bắt buộc (cột Trạng thái thì có “Trạng thái *”). File mẫu là file tĩnh, chưa theo khuôn chung (chưa có viền kẻ sẵn tới hàng 17; ô chọn Trạng thái chỉ tới dòng 10).
- [Code] Câu lỗi “… bị trùng lặp trong file import (dòng n)”: n = STT + 1 (đếm từ dòng dữ liệu đầu tiên = 2), không khớp STT bảng xem trước cũng không khớp số dòng Excel (dòng dữ liệu đầu tiên là dòng 3).
## SRS · Loại tài liệu
- [Code] Màn Loại tài liệu không có chức năng Import Excel trong code develop (không có nút Import Excel, không có file mẫu, máy chủ không có chức năng import). SRS hiện tại cũng không có mục Import (chỉ có Xuất Excel) → không cần bổ sung cột file import / lịch sử import.
## SRS · Danh mục công việc, lỗi thiết bị
- [Hỏi] Feedback ý 2 'áp TẤT CẢ danh mục' — danh mục này không có Import, có cần làm thêm chức năng Import không hay bỏ qua?
- [Code] Màn Danh mục công việc, lỗi thiết bị KHÔNG có chức năng Import: thanh công cụ chỉ có Tạo mới / In danh sách / Xuất Excel / Cấu hình cột, máy chủ không có đường import cho danh mục này. SRS hiện tại cũng không có mục Import (2.1–2.11 không có Import) → không cần bổ sung ý 2, ý 5 cho SRS này.
## SRS · Ứng dụng
- [Hỏi] Import ứng dụng đang cập nhật cả mã đã có (kể cả ứng dụng đang Khóa): giữ hành vi cập nhật hay chỉ cho thêm mới như các danh mục khác? Nếu giữ, có chặn ứng dụng đang Khóa không?
- [Hỏi] Bỏ trống ô bắt buộc đang làm hỏng cả lượt Validate với câu chung “Bắt buộc phải nhập”: sửa code để báo theo từng dòng như SRS, hay sửa SRS?
- [Hỏi] Quy tắc mã ứng dụng khi import nên thống nhất với màn Thêm mới không?
- [Code] Ô bắt buộc (Mã, Tên, Nhóm giải pháp, Trạng thái) bỏ trống ở bất kỳ dòng nào: hệ thống từ chối CẢ lượt Validate với câu chung “Bắt buộc phải nhập” (không chỉ ra dòng/cột nào, không tô đỏ dòng); các câu lỗi theo dòng kiểu “… không được để trống / … là bắt buộc” mà SRS ghi hiện KHÔNG bao giờ hiện ra. Ngoài ra danh sách cột bắt buộc khai cho cửa sổ Import không được dùng để kiểm tra trước.
- [Code] Chưa có luồng giữ cửa sổ Import và tô đỏ dòng không còn hợp lệ: màn không dùng khuôn import dùng chung; khi bấm Import mà một số dòng hết hợp lệ (dữ liệu đổi giữa lúc Validate và Import), hệ thống vẫn ghi các dòng còn lại, chỉ báo “Import thành công x/y … z … thất bại.”, đóng cửa sổ, không cho biết dòng nào lỗi; nếu không ghi được dòng nào thì chỉ hiện thông báo lỗi chung, cũng không tô đỏ dòng.
- [Code] Import cập nhật được cả ứng dụng đang Khóa (không kiểm tra trạng thái khoá trước khi ghi đè) — trái quy tắc bản ghi đã khoá không được sửa.
- [Code] Validate không kiểm tra trùng Mã hoặc trùng Tên giữa các dòng trong cùng tệp: hai dòng cùng mã đều qua Validate, lúc Import dòng sau thất bại với “Mã ứng dụng đã tồn tại” và chỉ được đếm vào số thất bại.
- [Code] Quy tắc mã khi import (≤ 7 ký tự, chữ/số/_/.) khác màn Thêm mới (dạng CHỮ.xxx); dòng mô tả trong file mẫu ghi “Hậu tố bắt buộc đủ 4 ký tự” nhưng hệ thống không kiểm tra điều này.
- [Code] Câu lỗi mã “Chỉ cho phép: Chữ cái không dấu(A-Z, a-z), chữ số (0-9) và dấu gạch dưới (_).” không nhắc dấu chấm dù dấu chấm được phép.
- [Code] Sheet HDSD_KHAIBAO ghi DM_nhomgiaiphap “Hệ thống xuất ra danh mục tương ứng đang hoạt động tại thời điểm User bấm tải file mẫu” nhưng file mẫu là tệp cố định với mã giả (NGP.GP01…), không có cặp nhóm ngành.
- [Code] Mô tả không giới hạn độ dài khi import.
- [Code] Độ dài Tên và Mã đang đếm theo byte chứ không theo ký tự: chữ tiếng Việt có dấu chiếm 2–3 byte nên tên có dấu chỉ khoảng 85–127 ký tự đã bị báo “vượt quá độ dài cho phép (tối đa 255 ký tự)”.
## SRS · Danh mục khách hàng (phần chuyển đổi ERP→HRM)
- [Hỏi] Sheet Hướng dẫn trong file mẫu chỉ liệt kê 5 giá trị Đối tượng (không có “Tổ chức”), trong khi hệ thống vẫn nhận “Tổ chức” = Doanh nghiệp tư nhân — SRS có cần nêu giá trị “Tổ chức” không?
- [Code] Chưa có luồng giữ cửa sổ Import tô đỏ dòng lỗi khi Import bị từ chối: màn khách hàng không dùng luồng import chung; bấm Import thì hệ thống kiểm tra lại, khách hàng nào lỗi bị bỏ qua và vẫn ghi phần còn lại (báo “Import thành công a/b khách hàng. c khách hàng thất bại.”), đóng cửa sổ — không trả lại kết quả để tô đỏ.
- [Code] Địa danh (Tỉnh/TP, Quận/Huyện, Phường/Xã, Thôn/Xóm) tra theo TÊN trên toàn hệ thống và chỉ lấy bản ghi đầu tiên trùng tên: tên phổ biến (vd “Phường 1”, “Xã Tân Lập”) có thể bị lấy nhầm của tỉnh khác rồi báo sai “… không thuộc …” dù dữ liệu đúng.
- [Code] Nhóm khách hàng tra không lọc trạng thái — nhóm đang Khóa vẫn import được.
- [Code] SĐT người liên hệ, Số tài khoản không kiểm tra định dạng; Số điện thoại của tổ chức không kiểm tra định dạng.
- [Code] Giới hạn số dòng: cửa sổ chặn 500 dòng nhưng máy chủ cho tới 1,000 dòng (không ảnh hưởng người dùng, chỉ lệch cấu hình).
## SRS · Nhóm ngành
- [Hỏi] Có sửa code để thiếu Mã/Tên/Trạng thái báo lỗi tại dòng (như SRS) không, hay SRS ghi theo hành vi hiện tại?
- [Hỏi] Có cho phép dấu gạch dưới trong Mã nhóm ngành khi import cho khớp form Tạo mới không?
- [Code] Nếu bất kỳ dòng nào trong tệp để trống Mã, Tên hoặc Trạng thái thì code hiện tại từ chối cả lượt Validate (thông báo chung “Bắt buộc phải nhập” trên đầu cửa sổ, không chỉ ra dòng nào) thay vì báo lỗi riêng ở dòng đó; các câu “… không được để trống” trong code không bao giờ hiện ra.
- [Code] Mã nhóm ngành: import chỉ nhận chữ cái và chữ số sau “NN.”, trong khi form Tạo mới cho phép cả dấu gạch dưới (_) — mã có “_” tạo tay được nhưng import báo sai định dạng.
- [Code] Dòng ví dụ đầu tiên của file mẫu dùng mã “NN.TEST1” (5 ký tự sau NN.) — tự báo sai định dạng nếu người dùng để nguyên.
- [Code] Độ dài Tên (255) và Mô tả (1,000) đang đếm theo byte nên chữ tiếng Việt có dấu bị chặn sớm hơn số ký tự ghi trên SRS.
- [Code] Câu “… bị trùng lặp trong file import (dòng n)”: n = thứ tự dòng dữ liệu + 1, không khớp số dòng Excel (dữ liệu bắt đầu dòng 3) cũng không khớp STT bảng xem trước.
- [Code] Trạng thái viết “Khoá” (dấu đặt ở chữ a) không được nhận, chỉ nhận đúng “Khóa”.
- [Code] Không có luồng giữ cửa sổ tô đỏ dòng không còn hợp lệ khi Import (Ý 1): Import bỏ qua dòng lỗi, ghi phần còn lại, đóng cửa sổ và báo “Import thành công x/y nhóm ngành. z nhóm ngành thất bại.”
## SRS · Danh mục mã phí
- [Hỏi] Câu “Mã phí bị trùng với dòng N trong file”: N do hệ thống tính = thứ tự dòng dữ liệu + 1 (dòng dữ liệu đầu tiên là “dòng 2”), không khớp STT trên bảng xem trước (1) và cũng không khớp số hàng thật trong Excel (3, vì hàng 2 là dòng mô tả). SRS ghi nguyên chữ “dòng N” hay cần sửa code cho N khớp STT?
## SRS · Danh mục gói bảo dưỡng
- [Hỏi] Công ty quản lý / Công ty ở sheet 4 đang được so với TẤT CẢ công ty (không lọc công ty đang hoạt động) — có cần chặn công ty ngừng hoạt động không?
- [Hỏi] Bảng mô tả cột có cần thêm cột “Sheet” (file có 5 sheet, cột “Mã gói” lặp ở sheet 2–5) — JSON đã kèm khoá `sheet` cho từng cột.
- [Hỏi] Có làm luồng giữ cửa sổ tô đỏ dòng lỗi (ý 1) cho màn này không, hay SRS ghi đúng hành vi hiện tại (bỏ qua lặng lẽ)?
- [Code] Chưa có luồng giữ cửa sổ Import tô đỏ dòng lỗi (ý 1): màn dùng cửa sổ Import riêng (không dùng khuôn chung của danh mục), lúc Import máy chủ kiểm tra lại rồi tự bỏ qua gói không còn hợp lệ và vẫn ghi phần còn lại, không trả kết quả để tô đỏ.
- [Code] File mẫu KHÔNG theo khuôn chung: không có cột STT, dòng 2 chỉ là gợi ý ví dụ (không phải câu “(Bắt buộc, …)”), không có dòng ví dụ, màu/kiểu khác file mẫu chuẩn.
- [Code] Import gói bảo dưỡng không áp giới hạn 500 dòng/lần như các danh mục khác (cả ở cửa sổ lẫn máy chủ).
- [Code] Câu lỗi sheet 2 dùng tên “Hệ số hưởng lợi”, “Giá cơ sở” trong khi tiêu đề cột là “Hệ số công nghệ”, “Giá bán cơ sở”.
- [Code] Câu lỗi giới hạn số in theo định dạng Việt Nam (“99.999.999,99”), trái chuẩn số quốc tế của hệ thống.
- [Code] Ô số coi dấu phẩy là phần thập phân: nhập “1,234” sẽ hiểu là 1.234 chứ không phải một nghìn hai trăm ba tư — cần ghi rõ cho người nhập (Giá bán cơ sở phải nhập số thuần).
## SRS · Danh mục quốc gia
- [Hỏi] Mã bưu chính chốt quy tắc nào: chỉ chữ số (như câu gợi ý trong file mẫu và bước Import) hay chữ không dấu/số/-/_ (như màn Thêm mới và bước Validate)?
- [Code] Mã bưu chính: bước Validate (và màn Thêm mới) nhận chữ không dấu, số, - và _, nhưng bước Import chỉ nhận toàn chữ số → dòng như “AB-100” báo hợp lệ ở Validate rồi thất bại khi Import.
- [Code] Mã quốc gia: Import cho tối đa 255 ký tự, màn Thêm mới chỉ cho tối đa 50 ký tự → import được mã dài hơn mức Thêm mới cho phép.
## SRS · Giai đoạn dự án
- [Hỏi] Import có phải bắt buộc tiền tố “GD.” cho Mã giai đoạn như cửa sổ Tạo mới không? (code hiện nhận mọi tiền tố chữ cái)
- [Hỏi] Mức độ ưu tiên khi import có phải giới hạn trong cấu hình của công ty người đang import không?
- [Code] Chưa có luồng giữ cửa sổ Import và tô đỏ dòng không còn hợp lệ lúc bấm Import: màn không dùng khuôn import chung; khi bấm Import hệ thống kiểm tra lại, dòng nào không còn hợp lệ (vd vừa có người tạo trùng) bị BỎ QUA im lặng, các dòng còn lại vẫn được ghi và báo “Import thành công N …” rồi đóng cửa sổ (N chỉ đếm dòng ghi được, không báo số dòng bị bỏ). Chỉ khi không còn dòng nào hợp lệ mới báo “Không có dữ liệu hợp lệ để import” và giữ cửa sổ, nhưng không đánh dấu lại dòng lỗi trên bảng xem trước.
- [Code] Mã giai đoạn khi import chỉ kiểm dạng <chữ cái>.<chữ/số/_> đủ 7 ký tự, KHÔNG bắt buộc tiền tố “GD.” (vd “ABC.123”, “X.ABCDE” vẫn hợp lệ), trong khi cửa sổ Tạo mới cố định tiền tố “GD.”.
- [Code] Mức độ ưu tiên được dò theo tên trên toàn bộ các mức của mọi công ty (cấu hình mức độ ưu tiên tách theo công ty, cho phép trùng tên giữa các công ty) → có thể gán nhầm mức của công ty khác; ô chọn trong file mẫu cố định “Bình thường, Khẩn cấp”, không theo cấu hình thật.
- [Code] Câu lỗi “… bị trùng lặp trong file import (dòng N)”: N = vị trí dòng trong bảng xem trước + 1 (dòng đầu tiên là 2), không khớp STT cũng không khớp số dòng Excel (dữ liệu bắt đầu từ dòng 3).
- [Code] File mẫu là file tĩnh, không theo khuôn file mẫu chung.
## SRS · Danh mục Phường/Xã
- [Code] Khi đối chiếu tên danh mục cha, hệ thống KHÔNG loại bản ghi đang Khóa: ô chọn trong file mẫu chỉ liệt kê bản ghi đang Hoạt động, nhưng gõ tay đúng tên một tỉnh/TP đang Khóa vẫn Validate qua và Import thành công — lệch với màn Thêm mới (chỉ cho chọn bản ghi đang Hoạt động).
- [Code] Tỉnh/TP tra theo tên nhưng KHÔNG xử lý trường hợp cùng tên ở nhiều quốc gia (khác Quận/Huyện, Đường/Phố): hệ thống lấy đại 1 tỉnh, nếu ghi Quốc gia khác thì báo nhầm “Tỉnh/TP Y không thuộc quốc gia X” dù tỉnh đúng có tồn tại.
## SRS · Ngân hàng câu hỏi khảo sát
- [Code] Màn Ngân hàng câu hỏi khảo sát không có chức năng Import (không có nút Import Excel, không có đường import riêng); SRS hiện cũng không có mục Import. Câu hỏi chỉ vào ngân hàng gián tiếp khi Lưu mẫu phiếu có câu hỏi import ở màn Phiếu thu thập thông tin (đã nêu ở Phần 4 SRS) — không cần bổ sung mục Import.
- [Code] Màn này không có chức năng lịch sử thay đổi.
## SRS · Phiếu thu thập thông tin
- [Hỏi] Phạm vi câu hỏi bỏ trống/sai: báo lỗi hay mặc định “Theo ứng dụng”?
- [Hỏi] Ý 5 có áp cho màn này không, khi Mẫu phiếu và Ngân hàng câu hỏi chưa có lịch sử thay đổi? Nếu có thì ghi lịch sử ở đâu (ngân hàng câu hỏi hay mẫu phiếu)?
- [Hỏi] Độ dài tối đa Tên Section và Nội dung câu hỏi khi import là bao nhiêu?
- [Code] Ý 5 (ghi lịch sử Tạo mới khi import): màn này không có chức năng lịch sử thay đổi cho Mẫu phiếu lẫn Ngân hàng câu hỏi; câu hỏi tạo mới vào ngân hàng lúc Lưu cũng không ghi lịch sử. Không đáp ứng được nếu không bổ sung tính năng lịch sử.
- [Code] Phạm vi câu hỏi không được kiểm: giá trị trống/sai bị tự hiểu là “Theo ứng dụng”.
- [Code] File mẫu không theo khuôn chung (không có cột STT, không có dòng mô tả cách nhập, tiêu đề không có dấu * cho cột bắt buộc, dòng ví dụ bắt đầu từ dòng 2).
- [Code] Không giới hạn 500 dòng/lần như các màn import khác.
- [Code] Không kiểm độ dài Tên Section / Nội dung câu hỏi khi Validate — quá dài có thể chỉ lỗi lúc Lưu mẫu phiếu.
- [Code] Luồng giữ cửa sổ tô đỏ dòng lỗi: không áp dụng theo nghĩa catalog vì bước Import không ghi dữ liệu (chỉ nạp vào phiếu đang dựng); không có bước kiểm tra lại lúc Import.
## SRS · Danh mục Quận/Huyện
- [Code] Khi đối chiếu tên danh mục cha, hệ thống KHÔNG loại bản ghi đang Khóa: ô chọn trong file mẫu chỉ liệt kê bản ghi đang Hoạt động, nhưng gõ tay đúng tên một tỉnh/TP đang Khóa vẫn Validate qua và Import thành công — lệch với màn Thêm mới (chỉ cho chọn bản ghi đang Hoạt động).
## SRS · Loại chiết khấu (màn Loại giảm giá)
- [Code] Màn Loại chiết khấu (màn Loại giảm giá) không có chức năng Import Excel trong code develop (không có nút Import Excel, không có file mẫu, máy chủ không có chức năng import). SRS hiện tại cũng không có mục Import (chỉ có Xuất Excel) → không cần bổ sung cột file import / lịch sử import.
## SRS · Cập nhật nhanh giá dịch vụ
- [Code] Màn không có chức năng Import: là màn cấu hình 1 bản ghi duy nhất (hệ số + định mức đàm phán cho toàn bộ gói bảo dưỡng), chỉ có Xem và Cập nhật. Máy chủ chỉ có đường xem và cập nhật, màn hình không có nút Import Excel. SRS hiện tại cũng không có mục Import — không cần bổ sung.