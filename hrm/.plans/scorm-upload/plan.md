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

## Phase 4 — Fix bug parse manifest (2026-06-02, @junfoke)

- [x] 4.1 `parseScormManifest`: dò `identifierref` đệ quy qua các `<item>` lồng nhau (gói SCORM.com Randomized Testing dùng cụm/aggregation không có identifierref ở cấp ngoài) — helper `findFirstItemRef`
- [x] 4.2 Xử lý `xml:base` trên `<resources>` và `<resource>` khi ghép launch href
- [x] 4.3 Fallback mạnh hơn: lấy `<resource>` đầu tiên có `href`; quét đệ quy index.html/story.html toàn gói thay vì chỉ thư mục gốc — helper `findFallbackLaunchFile` + chuẩn hóa path
- [x] 4.5 Bỏ default `scorm_min_score = 60` → `null` (gói nội dung không chấm điểm sẽ không bao giờ đạt nếu mặc định set điểm; điểm là điều kiện AND cho mọi rule ở `LearningSessionService`). Thêm hint "Để trống nếu gói chỉ là nội dung". BE giữ nguyên (rule `nullable|numeric`, Laravel convert '' → null).
- [x] 4.6 Prune `tracking_completion` khi submit: chỉ giữ key đúng loại bài (1=video_, 2=text_, 3=file_, 4=scorm_) qua helper `pruneTrackingForType` trong `emitFormData`. Bài SCORM chỉ còn `scorm_completion` + `scorm_min_score`. BE không đổi (`getEffectiveTracking` merge defaults fill key thiếu).
- [x] 4.4 Fix preview 403 AccessDenied: build launch URL dạng **virtual-hosted** (`https://tanphat.s3.cloud.cmctelecom.vn/<key>`) thay vì `ObjectURL` path-style (`s3.cloud.../tanphat/<key>`). Proxy `/scorm-proxy` (target virtual-hosted) ghép pathname path-style → trùng segment `tanphat/` trong key → S3 403. (lesson đã upload trước fix phải gỡ gói + tải lại)

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

## Checkpoint — 2026-06-02 (@junfoke)

Vừa hoàn thành: Phase 4 — 4 bug fix sau khi user test thực tế với gói SCORM.com:
- 4.1-4.3: parser manifest robust hơn (item lồng nhau + xml:base + fallback đệ quy) → hết 422 "không tìm thấy launch file" với gói "Randomized Testing".
- 4.4: launch URL đổi sang virtual-hosted → hết 403 AccessDenied khi preview qua /scorm-proxy.
- 4.5: bỏ default scorm_min_score=60 → null (gói nội dung không chấm điểm vẫn hoàn thành được) + hint UI.
- 4.6: prune tracking_completion khi submit, chỉ giữ key đúng loại bài.
File đụng thêm: LessonService.php (parser + launch URL), LessonForm.vue (default điểm + hint + pruneTrackingForType).
Đang làm dở: không.
Bước tiếp theo: user verify lại trên browser. Lesson SCORM tạo trước fix cần gỡ gói + tải lại (URL cũ path-style) và mở ra lưu lại (prune + bỏ điểm 60 cũ).
Blocked: không.
