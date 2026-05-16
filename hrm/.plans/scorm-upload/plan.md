# SCORM Upload — Plan

**Feature:** scorm-upload
**Spec:** docs/superpowers/specs/2026-04-22-scorm-upload-design.md
**Owner:** @khoipv

## Phase 1 — Backend

- [x] 1.1 Thêm method `putLocalFile($localPath, $s3Key, $mime)` vào `CmcS3Helper`
- [x] 1.2 Tạo `UploadScormRequest` (FormRequest) — validate file zip, size ≤ 1GB
- [x] 1.3 Thêm service method `LessonService::handleScormUpload(UploadedFile $zip)`
  - [x] 1.3.1 Copy zip vào temp dir `storage/app/tmp/scorm/{uid}`
  - [x] 1.3.2 Mở bằng `ZipArchive`, validate số file ≤ 2000
  - [x] 1.3.3 Extract + scan đệ quy tìm `imsmanifest.xml`
  - [x] 1.3.4 Parse manifest bằng `SimpleXMLElement` → launch path / title / version
  - [x] 1.3.5 Fallback: index.html / index_lms.html / story.html
  - [x] 1.3.6 Upload từng file lên S3 với MIME đúng (map + `mime_content_type` fallback)
  - [x] 1.3.7 Build launch URL tuyệt đối
  - [x] 1.3.8 Cleanup temp dir trong `finally`
  - [x] 1.3.9 Trả về `{url, version, package_path, package_title, file_size}`
- [x] 1.4 Controller `LessonController::uploadScorm`
- [x] 1.5 Route `POST /training/lessons/upload-scorm`

## Phase 2 — Frontend

- [x] 2.1 Dùng action chung `apiPostMethod` (không cần store action mới)
- [x] 2.2 Trong `LessonForm.vue` — block SCORM:
  - [x] 2.2.1 Thêm `V2BaseFile` (.zip) bên cạnh dropdown version
  - [x] 2.2.2 Handler `onUploadScormZip(file)` + spinner loading
  - [x] 2.2.3 Info card: tên gói / size / version + nút "Gỡ gói" (`clearScormPackage`)
  - [x] 2.2.4 Ô URL launch vẫn hiện full-row, auto-fill sau upload, cho phép chỉnh tay
- [x] 2.3 Submit: bổ sung `package_path / package_title / file_size / file_name` vào payload khi type=4
- [x] 2.4 Preview iframe dùng `data.content.url` — không đổi, chạy được URL S3

## Phase 3 — Test & Wrap (user thực hiện)

- [ ] 3.1 Test với gói SCORM 1.2 mẫu (ADL Golf Example)
- [ ] 3.2 Test với gói SCORM 2004
- [ ] 3.3 Test edge case: zip không có manifest → 422 báo lỗi rõ
- [ ] 3.4 Test edge case: zip > 1GB → 422
- [ ] 3.5 Tạo lesson type=SCORM → save → show lại → preview iframe load đúng từ S3

## File đã đụng

**BE (5 file):**
- `hrm-api/app/Helper/CmcS3Helper.php` — thêm `putLocalFile()`
- `hrm-api/Modules/Training/Http/Requests/Lesson/UploadScormRequest.php` — mới
- `hrm-api/Modules/Training/Services/Lesson/LessonService.php` — thêm `handleScormUpload` + 3 helper private
- `hrm-api/Modules/Training/Http/Controllers/V1/LessonController.php` — thêm `uploadScorm()`
- `hrm-api/Modules/Training/Routes/api.php` — route `POST /lessons/upload-scorm`

**FE (1 file):**
- `hrm-client/pages/training/lessons/components/LessonForm.vue` — UI block SCORM (upload zip + card info + URL), state `scormUploading`, handler `onUploadScormZip` + `clearScormPackage`, submit bổ sung fields

## Checkpoint — 2026-04-22

Vừa hoàn thành: Phase 1 (BE) + Phase 2 (FE) — 14/14 task code xong.
Đang làm dở: không.
Bước tiếp theo: user test thực tế theo Phase 3 (upload gói SCORM 1.2 + 2004 + edge case). Nếu có lỗi S3 Content-Type / CORS khi iframe load → xử lý sau.
Blocked: chưa test run — cần user upload thử 1 gói SCORM thực tế.
