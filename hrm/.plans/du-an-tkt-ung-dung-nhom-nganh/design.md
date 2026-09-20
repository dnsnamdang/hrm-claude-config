# Design — Ràng buộc Ứng dụng ↔ Nhóm ngành ở dự án TKT

Phụ trách: @cuong61n · Ngày mở: 2026-09-16 · Liên quan: Redmine #11142 (Tri Lee thêm trường Nhóm ngành)

## Vấn đề
Từ #11142, Nhóm ngành do user tự chọn (trước đó server suy từ Ứng dụng). Hai trường đang lọc theo
2 nguồn khác nhau và KHÔNG ràng buộc nhau:
- Ứng dụng: lọc theo Loại hình + Lĩnh vực của khách hàng cuối (`application_customer_scopes`).
- Nhóm ngành: lọc theo `customer_id` (ẩn nhóm ngành đang thuộc dự án còn mở khác của cùng KH).

⇒ Lưu được cặp mâu thuẫn: nhóm ngành không thuộc ứng dụng đã chọn.

Quan hệ dữ liệu đã có sẵn: pivot `application_scopes` (`Applications::scopes()`).
Dữ liệu dev đủ để áp ràng buộc ngay: 146/146 ứng dụng hoạt động đã khai nhóm ngành, 234 dòng pivot,
22/23 nhóm ngành có gắn ứng dụng.

## Quyết định đã chốt (2026-09-16, user chốt)
1. **Ràng buộc HAI CHIỀU**: chọn bên nào trước cũng được; mỗi trường lọc trường còn lại theo giá trị
   đang có. Đổi một bên làm bên kia không còn hợp lệ → hiện xác nhận "Giá trị đang chọn không còn
   phù hợp, sẽ bị xoá", đồng ý thì xoá giá trị bên kia (dùng `base-confirm-modal` qua `$confirm`).
2. **Dự án cha tự do, dự án con phải nằm trong cha**: cha (ẩn Ứng dụng) chọn nhiều nhóm ngành tuỳ ý;
   dự án con chỉ được chọn nhóm ngành vừa thuộc Ứng dụng của con VỪA nằm trong danh sách nhóm ngành
   của dự án cha.
3. Ràng buộc phải chặn ở **BE lúc lưu**, FE chỉ là lớp trải nghiệm.
