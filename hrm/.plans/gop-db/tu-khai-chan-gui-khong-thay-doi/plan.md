# Hồ sơ tự khai: chặn gửi duyệt khi không có thay đổi (chưa có số Redmine) — @junfoke

Nguồn: người dùng báo màn Duyệt cập nhật hồ sơ nhân sự "không còn báo đỏ chỗ mọi người sửa". Làm trên `develop` trước.

## Ngày 18/11/2026 (@junfoke)
- [x] 18/11/2026 — Khảo sát: phần tô đỏ vẫn chạy (dựng thử yêu cầu 393 đổi SĐT cá nhân → ô hiện "Có sự thay đổi" + nút xem giá trị cũ; đã trả nguyên trạng; code develop = gop_db). Nguyên nhân thật: NV không sửa gì vẫn gửi duyệt được (đoạn kiểm cũ bị comment), vd NV 49 gửi 391 và 393 cách 7 phút.
- [x] 18/11/2026 — BE: lúc gửi, so bản khai với hồ sơ hiện tại (`getEmployeeInfoDetail`, gồm ngân hàng, học vấn, người thân, quá trình công tác, kiêm nhiệm); không khác → không tạo yêu cầu, trả 422 "Bạn chưa thay đổi thông tin nào so với hồ sơ hiện tại nên không thể gửi duyệt". Bỏ qua 3 trường suy ra luôn lệch giả: chuỗi địa chỉ đầy đủ (thường trú, nơi ở) và chức vụ người quản lý trực tiếp. Chặn đặt sau validate, phủ cả 3 màn gửi tự khai.
- [x] 18/11/2026 — FE: 3 màn gửi hiện đúng câu BE trả (trước là câu lỗi cố định).
- [x] 18/11/2026 — Kiểm local: 4 hồ sơ thật (6, 22, 49, 594) gửi không sửa → đều chặn; 9 kiểu sửa thật (SĐT, ngày sinh, tỉnh, sửa/xoá học vấn, thêm người thân, thêm TK ngân hàng, ảnh CCCD, đổi quan hệ) → gửi được; giao diện: không sửa hiện toast đỏ, sửa Email gửi thành công. Đã dọn yêu cầu thử.
- [x] 18/11/2026 — Commit develop api `2ef1957a0`, client `d35213964`.
- [x] 19/11/2026 — Đã push develop cùng #12215 (rebase nên đổi mã: api `55585ddb1`, client `57eb9a078`).
- [ ] Lỗi có sẵn chưa sửa: form tự khai luôn gửi chức vụ người quản lý trực tiếp rỗng → duyệt xong có thể xoá chức vụ này trên hồ sơ (lịch sử 384, 380, 379) — làm riêng nếu user muốn.
