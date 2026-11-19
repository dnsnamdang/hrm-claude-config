# Kịch bản video "Việc của tôi" + Nhắc việc cá nhân (app) — bản 2, 08/11/2026

Mục đích (user chốt 08/11): (1) giới thiệu mục đích, chức năng, cách dùng màn Việc của tôi; (2) đi FULL chi tiết Nhắc việc
cá nhân + menu Danh bạ cá nhân (tìm liên hệ có sẵn, chọn từ danh bạ máy, tra khách hàng của phần mềm theo số) + Lịch làm việc
lãnh đạo + Cài đặt nhắc việc. Các loại phiếu khác chỉ nhắc tên — mỗi loại có video riêng.
Nguồn: code app `lib/ui/my_todo/**`, `leader_schedule/**` + tài liệu `.plans/my-todo*`, `gop-db/danh-ba-ca-nhan`,
`gop-db/loai-nhac-viec`, `gop-db/lich-cong-tac-lanh-dao`, `gop-db/nhom-da-ket-thuc` (đối chiếu 08/11, đã tự kiểm lại các điểm
chính trong code).

Quy ước: mỗi dòng = 1 bước; [ ] = thao tác chạy lúc bắt đầu bước; bước sau chạy khi lời bước trước đọc xong. Popup/sheet
chỉ đóng ở bước riêng có lời. LƯU THẬT trên DB local. Cảnh GỌI: đoạn iPhone thật `video/goi-that-iphone.mp4` (user quay 08/11, gọi từ THẺ, dữ liệu khác — user chốt dùng
luôn) ghép ở bước 📱 chương 7; máy ảo không bấm Gọi. Cắt đoạn màn chi tiết nhắc việc còn đang tải (1–2s đầu hiện "Không hạn").

## 1. Mở đầu
1. Xin chào. Các bạn đang xem video hướng dẫn sử dụng Phần mềm quản trị ERP TPE.
2. Video này giới thiệu màn Việc của tôi trên ứng dụng di động, và hướng dẫn chi tiết Nhắc việc cá nhân, Danh bạ cá nhân, cùng phần cài đặt nhắc việc.

## 2. Việc của tôi là gì
3. [màn chọn phân hệ] Sau khi đăng nhập, bạn chọn phân hệ Công việc.
4. [bấm Công việc] Màn đầu tiên là Việc của tôi. Đây là nơi gom mọi việc liên quan tới bạn vào một chỗ: nhiệm vụ, vấn đề, meeting, các loại phiếu, và nhắc việc cá nhân.
5. [khung 2 tab] Màn có hai tab: Công việc của tôi, xem dạng danh sách; và Lịch làm việc, xem theo ngày.

## 3. Danh sách công việc
6. [khung các tiêu đề nhóm] Việc được chia nhóm theo hạn: Hôm nay, Ngày mai, Tuần này, Tuần sau, Sau đó, Không hạn, và nhóm Quá hạn ở cuối. Số bên cạnh là số việc trong nhóm.
7. [khung Tuần này] Nhóm Tuần này tính cả việc của hôm nay và ngày mai, để bạn nhìn được cả tuần một lúc.
8. [bấm mở nhóm Quá hạn] Bấm vào tiêu đề nhóm để mở ra hoặc thu gọn. Mặc định chỉ mở nhóm Hôm nay.
9. [khung 1 thẻ nhiệm vụ quá hạn] Mỗi thẻ cho biết loại việc, vai trò của bạn, trạng thái, tên việc và hạn. Việc quá hạn có chữ đỏ, ghi trễ bao nhiêu ngày.
10. [khung thẻ meeting] Với meeting, thẻ ghi giờ họp và địa điểm. Nếu chưa xác nhận, bạn bấm Xác nhận tham gia ngay trên thẻ.
11. [bấm thẻ nhiệm vụ] Bấm vào thẻ để mở chi tiết. Ví dụ đây là chi tiết một nhiệm vụ.
12. [bấm Quay lại] Bấm quay lại để về danh sách. Mỗi loại việc mở đúng màn chi tiết của nó — các loại này có video hướng dẫn riêng.

## 4. Tìm, sắp xếp, lọc
13. [bấm ô tìm, gõ "hop"] Muốn tìm nhanh, gõ tên công việc vào ô tìm kiếm, danh sách lọc ngay khi gõ.
14. [xoá chữ] Xoá chữ để hiện lại đầy đủ.
15. [bấm ⇅] Nút này để sắp xếp. Danh sách vẫn chia nhóm theo hạn, chỉ đổi thứ tự trong từng nhóm.
16. [khung 5 lựa chọn] Có năm cách: Hạn hoàn thành, Cập nhật gần nhất, Tạo gần nhất, Ưu tiên cao trước, và Tên A tới Z.
17. [chọn Ưu tiên cao trước] Ví dụ chọn Ưu tiên cao trước. Lựa chọn được ghi nhớ cho lần sau, và nút sáng màu để bạn biết đang sắp khác mặc định.
18. [bấm ⇅, chọn Hạn hoàn thành] Mình chọn lại Hạn hoàn thành như mặc định.
19. [bấm nút Lọc] Nút Bộ lọc có hai điều kiện: Loại việc và Trạng thái.
20. [mở Loại việc, chọn Nhắc việc cá nhân] Loại việc chọn được nhiều loại cùng lúc. Ví dụ chỉ chọn Nhắc việc cá nhân.
21. [mở Trạng thái] Trạng thái có bốn nhóm: Chưa làm, Đang làm, Hoàn thành, và Dừng hoặc Hủy. Để trống thì ứng dụng chỉ hiện việc chưa xong.
22. [chọn Chưa làm, Đang làm, Hoàn thành → Xem kết quả] Mình chọn thêm Hoàn thành, rồi bấm Xem kết quả.
23. [khung chip] Điều kiện đang lọc hiện thành các nhãn phía trên. Chạm vào nhãn để sửa, bấm dấu x để bỏ.
24. [cuộn xuống, bấm mở nhóm Đã kết thúc] Vì có chọn Hoàn thành, cuối danh sách có thêm nhóm Đã kết thúc trong 30 ngày gần nhất. Thẻ trong nhóm này có màu xám.
25. [bấm Xóa lọc] Bấm Xóa lọc để bỏ hết điều kiện.
26. [kéo xuống] Kéo danh sách xuống để tải lại dữ liệu mới nhất.

## 5. Lịch làm việc
27. [bấm tab Lịch làm việc] Tab Lịch làm việc xếp các việc theo ngày.
28. [khung dải tuần] Dải tuần hiện thứ, ngày dương và ngày âm lịch. Chấm màu dưới mỗi ngày cho biết ngày đó có những loại việc nào.
29. [bấm 1 ngày] Bấm vào một ngày, phía dưới hiện danh sách việc từ ngày đó tới hết tuần.
30. [bấm Tháng] Bấm Tháng để xem cả tháng. Bạn cũng có thể vuốt lịch xuống để mở tháng, vuốt lên để thu về tuần.
31. [bấm ›, rồi Hôm nay] Hai mũi tên để sang kỳ trước hoặc kỳ sau. Bấm Hôm nay để về ngày hiện tại.
32. [bấm Bộ lọc lịch → Đóng] Lịch có Bộ lọc riêng theo loại việc và trạng thái. Nút xoay tròn bên cạnh để bỏ lọc và tải lại.
33. [bấm Tuần, về tab Công việc của tôi] Giờ mình đi vào phần chính: Nhắc việc cá nhân.

## 6. Tạo nhắc việc — tình huống nhắc gọi điện cho khách (liên hệ NHẬP TAY)
34. [bấm Tạo mới] Bấm nút Tạo mới ở giữa thanh dưới.
35. [khung danh sách] Từ đây tạo được mọi loại việc: Nhắc việc cá nhân, Nhiệm vụ, Meeting, các loại phiếu, và Vấn đề.
36. [bấm Nhắc việc cá nhân] Nhắc việc cá nhân là việc riêng của bạn, có thể chia thành nhiều bước. Ví dụ mình cần nhắc gọi điện cho khách hàng.
37. [bấm Lưu khi chưa nhập gì] Tiêu đề là ô bắt buộc. Chưa nhập mà bấm Lưu, ứng dụng báo đỏ ngay dưới ô.
38. [gõ Tiêu đề] Nhập tiêu đề: Gọi điện cho khách xác nhận lịch giao hàng.
39. [bấm Gắn liên hệ] Việc này liên quan tới khách, nên bấm Gắn liên hệ.
40. [khung sheet] Sheet Gắn liên hệ hiện danh bạ cá nhân của bạn, xếp theo chữ cái, có thanh chữ cái bên phải để nhảy nhanh.
41. [khung dải Gần đây] Dải Gần đây giữ những người bạn gắn gần nhất, kèm hai nút: Thêm mới để nhập tay, và Danh bạ máy để chọn từ điện thoại.
42. [bấm Thêm mới] Khách này chưa có trong điện thoại, mình bấm Thêm mới để nhập tay.
43. [gõ Tên] Nhập tên: Anh Minh, Công ty Hoà Phát.
44. [gõ Số điện thoại] Nhập số điện thoại. Tên và số điện thoại là bắt buộc, ứng dụng kiểm tra số có hợp lệ không.
45. [gõ Địa chỉ, Ghi chú] Địa chỉ và Ghi chú thì tuỳ chọn.
46. [khung dòng ghi chú cuối form] Lưu nhắc việc xong, người này tự vào danh bạ cá nhân, lần sau chỉ cần chọn lại. Nếu số đã có trong danh bạ, ứng dụng dùng lại người cũ, không tạo trùng.
47. [bấm Gắn liên hệ] Bấm Gắn liên hệ. Thông tin khách đã vào form, có nút gọi nhanh. Chạm vào thẻ để đổi người, bấm dấu x để gỡ.
48. [gõ Mô tả] Nhập mô tả: hỏi khách giờ nhận hàng và người ký nhận.
49. [gõ bước 1 + Enter] Phần Các bước giúp chia việc thành từng bước. Gõ nội dung rồi nhấn Enter là thêm xong một bước.
50. [gõ bước 2, bước 3] Thêm tiếp: Gọi xác nhận giờ giao, Báo lại kho, Gửi tin nhắn xác nhận. Bấm thùng rác cạnh bước để xoá.
51. [bấm Loại nhắc việc] Loại nhắc việc giúp phân nhóm. Có sẵn Việc cá nhân và Việc công ty.
52. [bấm + Thêm loại nhắc việc, gõ "Khách hàng", Thêm] Bạn tự thêm được loại mới, ví dụ Khách hàng. Bấm Thêm là loại mới được chọn luôn. Muốn sửa tên hoặc xoá loại thì làm trên web.
53. [bấm Ngày hạn, chọn ngày mai] Chọn ngày hạn trên lịch.
54. [bấm Giờ hạn, chọn 9:00] Chọn giờ hạn, ví dụ 9 giờ sáng. Có giờ hạn thì ứng dụng mới nhắc đúng giờ. Không chọn ngày hạn thì việc nằm ở nhóm Không hạn.

## 6a. Báo lịch làm việc lãnh đạo (trong form nhắc việc)
55. [khung khối Báo lịch làm việc lãnh đạo] Người được cấp quyền báo lịch sẽ thấy thêm phần Báo lịch làm việc lãnh đạo: báo cả công ty khi bạn đi vắng. Không có quyền thì phần này không hiện.
56. [bật công tắc] Bật lên, Ngày hạn và Giờ hạn chuyển vào khung này, thêm Ngày bắt đầu và Giờ bắt đầu.
57. [chọn Ngày bắt đầu, Ngày hạn] Chọn đủ ngày bắt đầu và ngày hạn. Ngày hạn phải từ ngày bắt đầu trở đi, sai là báo đỏ.
58. [khung xem trước] Khung này cho xem trước thông báo cả công ty sẽ nhận: ông bà nào vắng mặt, từ ngày nào tới ngày nào.
59. [bỏ tick Gửi kèm tiêu đề, tick lại] Bỏ chọn Gửi kèm tiêu đề nếu chỉ muốn báo thời gian vắng, không lộ nội dung việc. Mô tả, các bước và liên hệ không bao giờ gửi đi.
60. [bấm Lưu → hộp "Thông báo cho toàn Công ty?"] Bấm Lưu, ứng dụng hỏi lại vì nhắc việc này sẽ thông báo cho toàn công ty.
61. [bấm Đồng ý → toast "Đã lưu và thông báo cho toàn công ty"] Bấm Đồng ý. Nhắc việc được lưu, mọi nhân viên của công ty nhận thông báo, trừ chính bạn.
62. [khung toast] Sau khi đã báo, nếu bạn đổi ngày, tắt công tắc, xoá, hay hoàn thành sớm nhắc việc, cả công ty đều nhận thông báo cập nhật.

## 6b. Nhắc việc thứ hai — CHỌN TỪ DANH BẠ MÁY
64. [Tạo mới → Nhắc việc cá nhân, gõ "Gửi báo giá cho chị Kate"] Tạo thêm một nhắc việc: Gửi báo giá cho chị Kate.
65. [bấm Gắn liên hệ → Danh bạ máy] Người này đã có trong điện thoại, bấm Danh bạ máy.
66. [chọn Kate Bell] Danh bạ điện thoại mở ra, chọn đúng người. Tên và số được điền sẵn. Ứng dụng chỉ đọc đúng người bạn chọn, không đọc cả danh bạ.
67. [khung thẻ liên hệ] Nếu người được chọn chưa có số, ứng dụng mở form Liên hệ mới để bạn nhập số.
68. [chọn Ngày hạn hôm nay, Lưu] Chọn hạn hôm nay rồi bấm Lưu.

## 6c. Nhắc việc thứ ba — TÌM LIÊN HỆ CÓ SẴN và TRA KHÁCH HÀNG CỦA PHẦN MỀM
69. [Tạo mới → Nhắc việc cá nhân, gõ "Hẹn gặp anh Toàn trao đổi thiết bị"] Nhắc việc thứ ba: Hẹn gặp anh Toàn trao đổi thiết bị.
70. [Gắn liên hệ, gõ "Minh"] Muốn tìm người đã có, gõ tên vào ô tìm. Anh Minh vừa nhập tay ở trên đã có trong danh bạ.
71. [xoá chữ, gõ 0908396342] Còn nếu gõ đủ số điện thoại, ứng dụng tra luôn trong danh mục khách hàng của công ty.
72. [khung nhóm KHÁCH HÀNG CÔNG TY · KHỚP SỐ ĐIỆN THOẠI] Số này khớp người liên hệ Bùi Thanh Toàn của Trường Cao đẳng Dầu khí, có nhãn KH công ty. Phải gõ đủ số mới tra được, không tìm khách theo tên.
73. [khung dòng Chọn từ danh bạ điện thoại / Tạo liên hệ mới với số] Bên dưới còn hai lối khác: Chọn từ danh bạ điện thoại, hoặc Tạo liên hệ mới với đúng số vừa gõ.
74. [chọn Bùi Thanh Toàn] Chọn khách hàng. Thông tin được chép sang danh bạ của bạn.
75. [chọn Ngày hạn tuần sau, Lưu] Chọn hạn rồi Lưu.

## 6d. Thoát form khi chưa lưu
76. [Tạo mới → Nhắc việc cá nhân, gõ vài chữ, bấm quay lại] Nếu đang nhập dở mà bấm quay lại, ứng dụng hỏi lại để bạn không mất dữ liệu.
77. [khung 3 lựa chọn] Bạn chọn Lưu và quay lại, Quay lại không lưu, hoặc Ở lại màn này.
78. [bấm Quay lại, không lưu] Ở đây mình bỏ, bấm Quay lại không lưu.

## 7. Dùng nhắc việc ngay trên danh sách
79. [khung thẻ "Gọi điện cho khách…"] Nhắc việc mới nằm ở nhóm Ngày mai và cả nhóm Tuần này. Thẻ có ô vuông để đánh dấu xong, tên khách kèm nút gọi, và số bước đã xong.
80. [bấm Xem bước] Bấm Xem bước để mở các bước ngay trên thẻ, bấm Thu gọn để đóng lại.
81. [tick bước 1 → xác nhận] Tick một bước, ứng dụng hỏi lại cho chắc, bấm đồng ý là xong bước đó.
82. [bấm tên khách] Bấm vào tên khách để xem thông tin người đó.
83. [quay lại] Quay lại danh sách.
83a. 📱 [đoạn quay iPhone thật `goi-that-iphone.mp4`, 9s: bấm nút xanh trên thẻ → máy hỏi "Gọi 098…" → Đang gọi → Kết thúc] Đây là cảnh trên điện thoại thật: tới giờ gọi khách, bấm nút xanh trên thẻ, điện thoại hỏi lại số rồi gọi luôn, không phải tìm lại số.
83b. [quay lại máy ảo] Gọi xong quay lại ứng dụng để đánh dấu các bước đã làm.

## 8. Chi tiết nhắc việc
84. [bấm thẻ] Bấm vào thẻ để mở chi tiết nhắc việc.
85. [khung đầu] Đầu màn là tiêu đề, loại nhắc việc và hạn. Bên dưới là Liên hệ, Mô tả và các bước con.
86. [khung nút Gọi ở khối Liên hệ — KHÔNG bấm] Ở màn chi tiết cũng có nút Gọi ngay khối Liên hệ, bấm là gọi luôn như trên thẻ. Bấm vào tên liên hệ để mở thông tin người đó.
88. [tick bước 2] Tick vòng tròn để hoàn thành bước.
89. [bấm tên bước 3 → sheet Sửa bước, sửa chữ, Lưu] Bấm vào tên bước để sửa nội dung rồi Lưu. Sheet này cũng có nút Xóa bước.
90. [bấm Thêm bước, gõ, Lưu] Bấm Thêm bước để thêm bước mới ngay tại đây.
91. [bấm Sửa] Nút Sửa mở lại form để đổi bất kỳ thông tin nào.
92. [đổi Giờ hạn 10:00, Lưu] Ví dụ đổi giờ hạn thành 10 giờ rồi bấm Lưu. Lưu xong ứng dụng về lại danh sách.
93. [mở lại thẻ → Đánh dấu hoàn thành → khung hộp xác nhận] Làm xong việc, bấm Đánh dấu hoàn thành. Còn bước chưa xong thì ứng dụng nhắc là các bước đó cũng sẽ được tick.
94. [bấm Hoàn thành] Xác nhận. Tiêu đề có gạch ngang. Tick hết từng bước con cũng tự hoàn thành cả nhắc việc.
95. [bấm Mở lại] Nút đổi thành Mở lại nếu bạn cần làm tiếp. Mở lại thì các bước cũng được bỏ tick.
96. [quay lại, mở "Mua văn phòng phẩm", bấm Xóa] Muốn xoá nhắc việc không cần nữa, mở chi tiết và bấm Xóa.
97. [khung hộp xác nhận → bấm Xóa] Ứng dụng hỏi lại vì dữ liệu đã xoá không khôi phục được. Bấm Xóa để xác nhận.

## 9. Danh bạ cá nhân
98. [menu trái → Danh bạ cá nhân] Mọi liên hệ bạn gắn vào nhắc việc được gom ở Danh bạ cá nhân, trong menu bên trái.
99. [khung dòng "Hẹn…"] Liên hệ còn việc chờ có dòng Hẹn kèm ngày giờ và tên việc, quá hạn thì chữ đỏ. Nút xanh bên phải để gọi nhanh.
100. [gõ "Minh" vào ô tìm, rồi xoá] Ô tìm tìm theo tên hoặc số điện thoại.
101. [bấm 👤+] Nút thêm người ở góc trên để thêm liên hệ thẳng vào danh bạ.
102. [bấm Chọn từ danh bạ điện thoại → chọn David Taylor] Bạn chọn từ danh bạ điện thoại, hoặc nhập tay như lúc nãy.
103. [bấm Lưu] Bấm Lưu. David Taylor đã vào danh bạ cá nhân.
104. [bấm 👤+, nhập lại số của Kate Bell, Lưu → thông báo] Nếu số đã có, ứng dụng báo: Số này đã có trong danh bạ, kèm tên người đó.
105. [Đóng] Bấm Đóng.
106. [bấm Anh Minh] Bấm vào một người để xem chi tiết.
107. [khung 3 nút] Ba nút: Gọi, Nhắn tin, và Tạo nhắc việc.
108. [bấm Nhắn tin → ứng dụng Tin nhắn mở, số điền sẵn → quay lại] Nhắn tin mở ứng dụng tin nhắn với số đã điền sẵn.
109. [khung Nhắc việc với Anh Minh] Phần dưới là các nhắc việc với người này, chia Sắp tới và Đã xong, kèm loại nhắc việc và hạn còn bao nhiêu ngày.
110. [bấm Tạo nhắc việc → form điền sẵn liên hệ → bấm Hủy] Tạo nhắc việc từ đây sẽ điền sẵn người này vào form.
111. [bấm ⋮] Menu ba chấm có Sửa liên hệ, Lưu vào danh bạ điện thoại, và Xoá liên hệ.
112. [Sửa liên hệ → đổi Ghi chú → Lưu] Sửa liên hệ để cập nhật thông tin, ví dụ thêm ghi chú.
113. [⋮ → Lưu vào danh bạ điện thoại → màn thêm liên hệ của máy → Huỷ] Lưu vào danh bạ điện thoại mở màn thêm liên hệ của máy, thông tin đã điền sẵn.
114. [quay lại, mở David Taylor → ⋮ → Xoá liên hệ] Xoá liên hệ không cần nữa.
115. [khung hộp xác nhận → Xoá liên hệ] Các nhắc việc đang gắn với người này vẫn giữ nguyên, chỉ bỏ phần liên hệ. Danh bạ trên điện thoại không bị ảnh hưởng.

## 10. Lịch làm việc lãnh đạo
116. [menu trái → Lịch làm việc lãnh đạo] Lịch vắng mà lãnh đạo báo từ nhắc việc hiện ở menu Lịch làm việc lãnh đạo. Mọi nhân viên đều xem được.
117. [khung Bảng tuần] Bảng tuần: mỗi ô chia buổi sáng và buổi chiều. Xanh là có mặt, vàng là vắng mặt, xám là ngoài ca hoặc nghỉ.
118. [bấm ô vàng → sheet chi tiết → Đóng] Chạm vào ô vàng để xem thời gian và nội dung lịch vắng.
119. [bấm Theo ngày] Chế độ Theo ngày cho biết hôm đó bao nhiêu người vắng, bao nhiêu người có mặt.
120. [bấm Dòng thời gian] Dòng thời gian chia Đang vắng, Sắp tới, và Đã qua trong 30 ngày, tìm được theo tên lãnh đạo.

## 10b. Thông báo nhắc việc
120a. [chạy assign:send-work-reminders khi nhắc việc tới giờ nhắc → banner iOS (simctl push, đúng nội dung DB)] Tới giờ nhắc, điện thoại hiện thông báo nhắc việc, kể cả khi đang dùng ứng dụng khác.
120b. [bấm banner] Bấm vào thông báo là mở thẳng màn Việc của tôi.
120c. [bấm chuông góc trên] Mọi thông báo cũng lưu trong chuông ở góc trên, xem lại được bất cứ lúc nào.
120d. [chạy assign:send-work-digest → banner Bản tin sáng → mở chuông] Mỗi sáng có việc, bạn nhận Bản tin sáng tóm tắt việc trong ngày.

## 11. Cài đặt nhắc việc
121. [menu trái → Cài đặt → Nhắc việc] Cuối cùng, trong Cài đặt, nhóm Thông báo, có mục Nhắc việc.
122. [khung danh sách loại] Mỗi loại việc có công tắc nhắc trước hạn. Tắt thì việc chỉ hiện trong chuông thông báo, không nhắc riêng.
123. [bấm Nhắc việc cá nhân → sheet] Bấm vào loại để chọn nhắc trước bao lâu: đúng giờ hạn, 15 phút, 30 phút, 1 giờ, 2 giờ, 4 giờ, hoặc 1 ngày. Mặc định là đúng giờ hạn.
124. [Đóng] Thay đổi được lưu ngay, không cần bấm Lưu.
125. [khung Bản tin sáng + chú thích] Bản tin sáng gửi lúc 7 giờ 30 mỗi ngày có việc. Nhắc việc chỉ có ngày mà không có giờ thì không nhắc riêng, chỉ nằm trong bản tin sáng. Việc quá hạn luôn được báo.

## Kết
126. Đó là các chức năng chính của màn Việc của tôi, Nhắc việc cá nhân và Danh bạ cá nhân.
127. Cảm ơn các bạn đã xem video!

## Dữ liệu dựng ngay trước khi quay (theo ngày quay 09/11)
- Nhắc việc "Mua văn phòng phẩm" (xoá ở bước 96).
- 1 liên hệ có nhắc việc QUÁ HẠN chưa xong (dòng Hẹn chữ đỏ) + 1 nhắc việc đã xong trong 30 ngày (nhóm Đã kết thúc).
- Anh Minh sẽ có cả việc Sắp tới (tạo ở ch.6) — dựng thêm 1 nhắc việc ĐÃ XONG gắn Anh Minh SAU ch.6 là không được trong 1 lần
  quay ⇒ chấp nhận chỉ có "Sắp tới", hoặc dùng liên hệ dựng sẵn có cả 2.
- Lịch lãnh đạo: dựng sẵn 1 lịch vắng trong tuần 09/11 + 1 lịch sắp tới (qua API, trên local — ghi thông báo vào chuông của
  NV local, không có push vì FIREBASE_CREDENTIALS local cố ý hỏng). Có lịch ở tuần quay mới có ô vàng.
- Danh bạ máy ảo: Kate Bell, David Taylor có số (mặc định simulator).
- Số tra KH: 0908396342 (Bùi Thanh Toàn — Trường CĐ Dầu khí), chưa có trong danh bạ cá nhân.
- Kiểm nhóm KH: số 0977113386 (Công ty Giang Hiền) dự phòng.

## Không quay (tài liệu có nhưng app chưa làm)
- Tạo nhắc việc từ ngày trống trên tab Lịch; chip ✕ ở tab Lịch; sửa/xoá Loại nhắc việc; "Tự động" cho nhắc việc cá nhân.
