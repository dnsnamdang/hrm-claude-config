# Plan — Fix mất ảnh đại diện nhân sự (file S3 biến mất)

Phụ trách: @khoipv

## Bối cảnh / triệu chứng
- Nhân sự (đặc biệt vào từ ~10/2025) mất ảnh đại diện trên FE.
- Đã xác minh (DB snapshot `hrm_production_29052026` + gọi thẳng S3 CMC):
  - Cột `employee_infos.image` **vẫn có URL đúng**.
  - File trên S3 trả **HTTP 403 / NoSuchKey (404)** → **file vật lý đã mất / không truy cập được**.
  - Cùng định dạng URL mới (`tanphat.s3.../tanphat_hrm/`): **trước 10/2025 hỏng ~3%**, **từ 10/2025 hỏng ~59%**.
  - URL cũ (`s3.cloud.../tanphat/...`) hỏng ~77% (vấn đề cũ, diện rộng hơn).
- `CmcS3Helper` không đổi từ 2024 → không phải lỗi code upload. BE create không xóa file S3 (chỉ `Http::get` để đẩy lên máy chấm công).

## Phase 1 — Truy nguyên cơ chế mất file (XONG)
- [x] Quét toàn bộ điểm xóa/ghi đè file S3 trong `tanphat_hrm`
- [x] Soi luồng sync máy chấm công / face-recognition
- [x] Kết luận root cause (đã xác minh bằng dữ liệu)

### ROOT CAUSE (đã xác minh)
1. `EmployeeInfoService::createEmployeeInfo()` dòng **779** (và luồng update): set `face_image_url = $newImageLink` = **chính URL avatar** (`image`) khi nhân sự bật face_recognition (dùng avatar làm ảnh mặt ban đầu đẩy lên máy).
2. Job sync mặt `ConnInfoService::syncFaceForDeviceSsn()` dòng **196-197** (và Rice `RiceConnInfoService` ~146-147): trước khi tải ảnh mặt mới từ máy, gọi `deleteS3ByUrl($employeeInfo->face_image_url)` → **xóa luôn file avatar** (vì face_image_url == image).
3. Sau đó chỉ cập nhật `face_image_url = URL mới`, **KHÔNG đụng `image`** → `image` trỏ tới file đã xóa → HTTP 403/404 → mất avatar.

Bằng chứng dữ liệu (nhân sự từ 10/2025): 47/48 avatar mất nằm đúng nhóm "đã sync mặt & face_image_url≠image"; nhóm chưa sync avatar nguyên vẹn 100%.

## Phase 2 — Fix chặn bug (XONG 2026-06-06)
- [x] Thêm guard trong `ConnInfoService::deleteS3ByUrl()` (Timesheet): bỏ qua xóa nếu URL đang là `employee_infos.image`
- [x] Thêm guard tương tự trong `RiceConnInfoService::deleteS3ByUrl()` (Rice)
- [x] Lint PASS cả 2 file; test logic guard với dữ liệu thật PASS
- Tác dụng: từ giờ sync mặt không xóa file đang là avatar. Bảo vệ cả nhóm còn nguyên (face_image_url==image, ~13+ người + nhân sự mới) khỏi bị mất ở lần sync sau. KHÔNG khôi phục được ảnh đã mất (xem Phase 3).

### Khả năng khôi phục (đã khảo sát)
- S3 versioning: TẮT → không phục hồi bản gốc.
- Nhóm 10/2025: 47/48 có `face_image_url` còn sống (ảnh máy chấm công ~12–25KB, vốn là avatar bị nén) → khôi phục `image = face_image_url`.
- Nhóm cũ (URL path-style, ~77% mất): không có face_image_url → chỉ còn ERP/Odoo (chưa truy cập được) hoặc upload tay.

## Phase 3 — Khôi phục dữ liệu (XONG phần khôi phục được — 2026-06-06)
- [x] Dò danh sách khôi phục được: 56 nhân sự (image hỏng + face_image_url còn sống), lưu `recover-list.csv` (kèm URL cũ làm backup)
- [x] Update `image = face_image_url` qua **query builder** (KHÔNG dùng Eloquent save vì model có event đồng bộ sang ERP `erp_new_11032026` — fail FK department, lỗi dữ liệu ERP có sẵn, không liên quan)
- [x] Verify: 56/56 avatar load HTTP 200
- [ ] (Còn lại) Nhóm cũ URL path-style mất ~77% nhưng KHÔNG có face_image_url → không tự khôi phục được. Cần: xuất danh sách cho HR upload tay, hoặc kiểm tra ảnh trong ERP/Odoo (image_1920). Chờ user.

### Lưu ý
- Ảnh khôi phục là ảnh mặt máy chấm công (~12–25KB, phân giải thấp hơn avatar gốc) nhưng đúng người.
- Recovery local chỉ tác động DB snapshot local, KHÔNG đụng production.

## Phase 4 — Áp dụng lên PRODUCTION
3 file cần deploy:
1. `Modules/Timesheet/Services/ConnInfoService.php` (guard deleteS3ByUrl)
2. `Modules/Rice/Services/Category/ConnInfo/RiceConnInfoService.php` (guard deleteS3ByUrl)
3. `app/Console/Commands/RecoverEmployeeAvatar.php` (command khôi phục, mới)

Quy trình trên production (thứ tự bắt buộc):
- [ ] B1. Deploy 3 file lên server API production (CHẶN tiếp tục mất avatar) — làm TRƯỚC
- [ ] B2. `php artisan human:recover-employee-avatar` (dry-run) → xem số lượng + CSV `storage/app/avatar-recover-*.csv`
- [ ] B3. `php artisan human:recover-employee-avatar --apply` → khôi phục thật (query builder, né sync ERP)
- [ ] B4. Verify avatar hiển thị

Lưu ý: số trên production nhiều khả năng LỚN HƠN 56 (snapshot cũ ~1 tuần + mỗi ngày sync vẫn xóa thêm tới khi B1 xong). Command tự dò trên DB đang chạy nên KHÔNG cần mang CSV local sang.
- [ ] (Còn lại) Nhóm cũ path-style không có face_image_url → upload tay / kiểm tra ERP.

## Phase 3 — Khắc phục dữ liệu đã mất (tuỳ chọn, hỏi user)
- [ ] (điền sau)
