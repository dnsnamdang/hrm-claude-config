# #10325 — [App] Thông báo mất kết nối mạng — @cuong61n

TPE_APP `develop`. CHƯA commit. Yêu cầu: mất mạng thì báo "Mất kết nối mạng, hãy kiểm tra và thử lại nhé" thay cho lỗi kỹ thuật.

- [x] Hằng `RemoteException.noInternetMessage`; message mapper + popup lỗi chung dùng câu này
- [x] `RemoteException.toString()` trả câu này khi mất mạng → các màn in thẳng `'$e'` (Chấm công, Giao việc…) cũng hiện câu thân thiện
- [x] Vá: đăng xuất từ menu trái khi mất mạng kẹt vòng quay "Đang đăng xuất" mãi → tắt vòng quay + báo mất mạng (`utils/exts/obj_func_exts.dart`)
- [x] Test iOS (build trỏ host không phân giải được, tái hiện đúng lỗi ảnh task): Tổng quan (popup), Cập nhật tiến độ task (ô lỗi), Chấm công (toast), Đăng xuất (màn chọn phân hệ + menu trái); build có mạng tải dữ liệu bình thường
