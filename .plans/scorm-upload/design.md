# SCORM Upload — Design Summary

**Owner:** @khoipv
**Spec chi tiết:** `docs/superpowers/specs/2026-04-22-scorm-upload-design.md`

## Mục tiêu

Cho phép user upload 1 gói SCORM (.zip) ở form Bài học (type=4). BE giải nén, upload toàn bộ file con lên S3, parse `imsmanifest.xml` để lấy launch URL, trả về FE. FE set `data.content.url` = launch URL + hiển thị info gói (title, version, size). Preview iframe chạy được nội dung SCORM từ S3.

## Scope

- **BE**: 1 endpoint mới `POST /api/v1/training/lessons/upload-scorm` nhận file zip → extract → upload recursively lên S3 folder riêng → parse manifest → trả launch URL tuyệt đối + metadata.
- **FE**: Thêm vùng upload .zip trong block SCORM của `LessonForm.vue`, gọi endpoint mới, set `data.content = { version, url, package_path, package_title, file_size }`. Giữ option nhập URL thủ công như cũ.
- **Không làm trong feature này**: SCORM API runtime shim, tracking CMI, delete old package khi replace (để hook vào luồng xóa lesson sau).

## Quyết định lớn

1. **Folder S3**: `tanphat_hrm/{env}/training/lessons/scorm/{uid}/...` — `uid` = `time()-random(8)` để mỗi lần upload có namespace riêng, tránh đụng path.
2. **Launch URL**: parse `imsmanifest.xml` → `organizations/organization/item[@identifierref]` → resolve sang `resources/resource[@identifier]/@href` (hoặc `file[0]/@href` nếu resource không có href). Nếu không parse được → fallback tìm file `index.html` / `index_lms.html` ở root.
3. **Version SCORM**: tự detect từ manifest (schemaversion) thay vì bắt user chọn; FE vẫn cho override nếu cần.
4. **Giới hạn**: zip ≤ 1GB, số file trong zip ≤ 2000. Vượt → 422.
5. **Cleanup temp**: dùng `storage/app/tmp/scorm/{uid}` → xóa sau khi upload xong (cả success/fail).
6. **ACL public-read**: cần thiết để iframe load trực tiếp từ S3 qua HTTPS.

## Schema data.content sau feature

```json
{
  "version": "scorm_1_2",           // detect từ manifest, có thể override
  "url": "https://s3.../index.html",// launch URL tuyệt đối
  "package_path": "training/lessons/scorm/{uid}",  // để cleanup sau
  "package_title": "Bài 1: An toàn lao động",
  "file_size": 15234567
}
```

## Rủi ro

- CmcS3Helper hiện chỉ support `UploadedFile`, phải thêm method `putLocalFile($localPath, $s3Key, $mime)` — dùng `putObject` với `SourceFile`.
- Một số gói SCORM có `imsmanifest.xml` ở thư mục con → cần scan zip để tìm file manifest thật sự.
- MIME type của `.js/.css/.html` bên trong gói phải set đúng `Content-Type` khi put lên S3 — nếu không iframe có thể fail.
