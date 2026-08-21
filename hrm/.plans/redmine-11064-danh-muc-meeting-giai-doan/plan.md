# Plan — Redmine #11064 [PL8 - Danh mục] Loại meeting, Giai đoạn dự án

Nguồn: sheet `12_8` (danh_sach_loai_meeting.xlsx) + sheet `11_8` (danh_sach_giai_doan_du_an_anh_chinh.xlsx)
Phạm vi: CHỈ update bản ghi đã có (theo tên cũ / ghi chú cột G), chỉ tạo mới dòng có ghi chú "Thêm mới giai đoạn", không xoá/khoá.

## BE
- [x] Seeder `UpdateMeetingTypesSeeder` — update 3 loại meeting có điền cột C (tên cột D, mô tả cột F)
- [x] Seeder `UpdateProjectPhasesSeeder` — update 4 giai đoạn ghi chú "Cập nhật tên và mô tả" (tên C, mô tả F), match theo mã GD.000x
- [x] Thêm mới giai đoạn "6. CĐT thẩm định giá, phê duyệt dự toán gói thầu" — mã GD.0009
- [ ] Chạy seeder trên DB local kiểm tra
- [ ] Chạy seeder trên cổng chính hrm.eteksofts.com

## Ghi chú
- Mức độ ưu tiên (cột D sheet 11_8) chưa cập nhật cho bản ghi cũ — ghi chú sheet chỉ ghi "Cập nhật tên và mô tả"
- GD.0009 cần mức "Rất cao" nhưng bảng priority_levels chưa có mức này → tạo với mức ưu tiên trống + cảnh báo, cần chốt với TPE Lệ
