# SCORM Preview Runtime (hrm-client) — Plan

Owner: @junfoke — Date: 2026-06-01

## Phase 1 — Proxy same-origin (Nuxt serverMiddleware)

- [x] Tạo `hrm-client/server-middleware/scorm-proxy.js` — reverse-proxy `/scorm-proxy/*` → S3
      bằng Node `https`. Logic port từ vite proxy elearning:
      - strip `accept-encoding` request (ép S3 trả body không nén)
      - với `.html`: bỏ `if-none-match`/`if-modified-since` request; buffer body + inject
        `<script>window.confirm=function(){return true};</script>` vào `<head>`;
        xoá `etag`/`last-modified`/`content-length`; set `cache-control: no-store`
      - file khác: stream nguyên trạng
      - lỗi mạng/TLS → trả 502 sạch
      - host target lấy từ `process.env.SCORM_S3_BASE`, default `https://tanphat.s3.cloud.cmctelecom.vn`
- [x] Đăng ký `serverMiddleware` trong `nuxt.config.js`
- [x] Test standalone: handler kết nối S3 OK (403 XML root, stream non-html đúng)

## Phase 2 — Runtime + component preview

- [x] Thêm `scorm-again@^3.0.5` vào `hrm-client/package.json` + `build.transpile: ['scorm-again']`
- [x] `npm install` trong hrm-client (host) — đã cài, engine warn Node≥20 nhưng dist ship sẵn ES5/ie11
- [x] Tạo helper `hrm-client/utils/scorm.js` — `toScormProxyUrl(url)` (strip origin → `/scorm-proxy`),
      `isScorm2004(version)`
- [x] Tạo `hrm-client/pages/training/lessons/components/ScormPreview.vue` (Vue 2 options API):
      init Scorm12API/Scorm2004API theo version, gắn `window.API`/`window.API_1484_11`,
      settings `{autocommit:false, logLevel:'ERROR', lmsCommitUrl:false}`, iframe src =
      `toScormProxyUrl(content.url)`; cleanup window API ở `beforeDestroy`
- [x] Sửa block SCORM preview trong `LessonForm.vue`: thay `<iframe>` trần bằng
      `<ScormPreview :content="data.content" :key="data.content.url" />`

## Phase 2b — Seed objectives từ manifest (phát sinh khi test)

Sau khi proxy+runtime chạy, gói "Advanced Calls" vẫn lỗi `could not find objective: obj_playing`
và `cmi.objectives.undefined.*` (401) vì LMS chưa nạp sẵn objective khai báo trong manifest.

- [x] `utils/scorm.js`: thêm `toScormManifestProxyUrl(content)` (suy ra URL manifest từ
      launch url + package_path) + `extractObjectiveIds(xml)` (regex `objectiveID=`)
- [x] `ScormPreview.vue`: trước khi load iframe (SCORM 2004), fetch imsmanifest.xml qua proxy →
      parse objective ids → `api.loadFromJSON({ objectives: ids.map(id=>({id})) })` (best-effort)

## Phase 2c — Port fix sang elearning (cùng lỗi)

Gói "Advanced Calls" load ở cả màn học viên elearning (`ScormPlayer.vue`) cũng lỗi obj_playing.

- [x] `elearning/src/utils/scorm.js`: thêm `toScormManifestProxyUrl` + `extractObjectiveIds`
- [x] `elearning/src/components/learning/viewers/ScormPlayer.vue`: seed objectives (2004) trước
      khi load iframe (trước cả resume & finalizeReady)
- [x] VERIFY elearning: reload → KHÔNG còn lỗi obj_playing (user xác nhận 2026-06-01)

## Phase 3 — Verify

- [x] Restart dev server (user đã làm) — proxy + runtime hoạt động (alert đổi từ "tanphat.s3"
      sang "localhost:3000" = đã cùng origin)
- [x] elearning: gói "Advanced Calls" chạy KHÔNG còn alert objective (user xác nhận)
- [x] hrm-client preview: user xác nhận đã hết lỗi obj_playing

## Phase 4 — Seed passing score từ manifest (user yêu cầu)

- [x] `utils/scorm.js` (cả 2 app): thêm `extractScormThresholds(xml)` — đọc `minNormalizedMeasure`
      (→ cmi.scaled_passing_score) + `completionThreshold`/`minProgressMeasure` (→ cmi.completion_threshold)
- [x] Đổi `seedObjectivesFromManifest` → `seedFromManifest` ở cả ScormPreview.vue + ScormPlayer.vue:
      seed thêm scaled_passing_score / completion_threshold (loadFromJSON, trước Initialize)
- [ ] VERIFY: reload elearning + hrm-client → gói advanced chạy OK, pass/fail theo manifest

> Lưu ý 2 tầng điểm đạt (không trùng nhau):
> - cmi.scaled_passing_score (manifest) → gói TỰ set cmi.success_status passed/failed
> - scorm_min_score (cấu hình bài học) → BE elearning checkScormCompletion mới quyết định "done"
>   (đã có sẵn ở feature scorm-lms-runtime, KHÔNG đổi). Preview hrm-client không có tầng BE này.
- [ ] Test cả gói SCORM 1.2 và 2004
- [ ] Đổi gói (upload gói khác) → preview reload runtime sạch (nhờ `:key`)
- [ ] Note OPS: prod cần proxy `/scorm-proxy` qua Node server hrm-client (serverMiddleware đã cover
      cả `nuxt start`; nếu sau reverse-proxy/CDN thì giữ path `/scorm-proxy` về Node)
