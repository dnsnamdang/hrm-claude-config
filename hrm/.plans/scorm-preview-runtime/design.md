# SCORM Preview Runtime (hrm-client) — Design (tóm tắt)

**Owner:** @junfoke
**Date:** 2026-06-01
**Trạng thái:** Đang làm

## Vấn đề

Màn quản lý bài học `pages/training/lessons/_id/edit.vue` → panel preview SCORM
(`LessonForm.vue`, type=4) hiện chỉ nhúng iframe "trần" trỏ thẳng URL launch trên S3:

```html
<iframe :src="data.content.url"></iframe>
```

Gói SCORM khi chạy duyệt cây `window` để tìm LMS API (`window.API` / `window.API_1484_11`).
Vì (1) không có runtime API nào được cung cấp và (2) iframe khác origin (localhost ↔ S3),
gói không gọi được runtime → các gói có advanced runtime calls (vd Rustici "Run-time
Advanced Calls") bung alert lỗi như `ERROR - could not find objective: obj_playing`.

## Giải pháp

Port lại cơ chế của feature [[scorm-lms-runtime]] (đã DONE cho phía elearning) sang admin
hrm-client, nhưng **rút gọn ở mức PREVIEW** — chỉ để gói chạy đúng, KHÔNG tracking:

1. **Same-origin proxy** `/scorm-proxy` (Nuxt 2 `serverMiddleware`) reverse-proxy S3 về cùng
   origin hrm-client + inject `window.confirm=()=>true` + `Cache-Control: no-store` cho HTML
   (tái dùng nguyên logic vite proxy của elearning, viết lại bằng Node `https`).
2. **scorm-again** dựng LMS API runtime đầy đủ (1.2 + 2004) gắn lên `window` → gói tìm thấy
   API, các call objectives/cmi hoạt động → hết lỗi.
3. Component nhỏ `ScormPreview.vue` thay block iframe trần trong panel preview.

## Khác biệt với scorm-lms-runtime (elearning)

| | elearning (học viên) | hrm-client (preview admin) |
|---|---|---|
| Proxy | Vite dev + nginx prod | Nuxt `serverMiddleware` (1 cơ chế cho cả dev+prod) |
| Runtime | scorm-again | scorm-again (giống) |
| Tracking | Có (commit BE, resume, completion) | **KHÔNG** — runtime in-memory, `lmsCommitUrl:false` |
| Resume popup | Có | KHÔNG |
| BE | migration + endpoint scorm-commit | **KHÔNG đụng BE** |

## Scope

- CHỈ FE hrm-client. Không đụng BE, không migration, không permission.
- Mục tiêu: admin upload gói SCORM → preview chạy không lỗi runtime, kiểm tra hiển thị.

## Spec chi tiết

`docs/superpowers/specs/2026-06-01-scorm-preview-runtime-design.md`
