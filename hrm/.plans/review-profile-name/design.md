# Tên hồ sơ cho Hồ sơ trình duyệt giải pháp

## Mục tiêu
Bổ sung trường **"Tên hồ sơ"** (bắt buộc) vào hồ sơ trình duyệt, hiển thị trong form Tạo/Sửa và danh sách theo dõi.

## Scope
- Áp dụng **cả 2 cấp**: Giải pháp (`solution_review_profiles`) + Hạng mục (`solution_module_review_profiles`).
- Validate **chỉ ở backend** (FormRequest, trả 422); FE chỉ hiển thị lỗi trả về, không validate phía client.
- Vị trí trên form: đầu khối trái, trên ô "Nội dung trình duyệt".
- Danh sách: thêm **cột riêng "Tên hồ sơ"** ở cả 3 tab dùng chung (solutions, solution-modules, prospective-projects).

## Quyết định chính
- Cột `name` VARCHAR(255) **nullable** (record cũ hiển thị "—"); bắt buộc nhập đảm bảo qua FormRequest cho bản ghi mới.
- Entity `$guarded=[]` → không cần sửa fillable.

## Nghiệm thu
- AC1: form Tạo có nhãn "Tên hồ sơ*".
- AC2: bỏ trống → BE 422 → không lưu + hiện lỗi inline.
- AC3: nhập đủ → lưu thành công.
- AC4: danh sách hiển thị đúng tên.

Spec chi tiết: `docs/superpowers/specs/2026-07-06-review-profile-name-design.md`
