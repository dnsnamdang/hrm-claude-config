# Plan — Elearning cleanup (@junfoke)

Xuất phát từ đợt quét toàn bộ elearning (24/06/2026). Danh sách bug/cải thiện đã được verify.

## Phase 1 — Thống nhất API client (refresh token)

Vấn đề: có 2 API client. `src/utils/api.js` (axios) có interceptor auto-refresh 401;
`src/services/api.js` (fetch) KHÔNG có → các store dùng fetch client (learningPathDetail,
subjectDetail, elearning, search, myLearning, filterOptions, useDiscussion, useListPage...)
khi token hết hạn không tự refresh → user lỗi/đăng xuất thay vì gia hạn ngầm.

Giải pháp: cho `services/api.js` dùng lại axios + interceptor của `utils/api.js`, giữ nguyên
hợp đồng cũ (full path, trả JSON body trực tiếp, throw Error có `.status`) → không phải sửa call-site.

- [x] Tách `attachAuthInterceptors(instance)` trong `utils/api.js` (request token + response refresh), export ra
- [x] Viết lại `services/api.js` dùng axios instance (baseURL = VITE_API_URL root), gắn `attachAuthInterceptors`, giữ contract `{ get, post, put, del }` trả JSON + `err.status`
- [x] Verify build (`npm run build`) không lỗi import — build OK trong container (Node 24), 44.58s

### Checkpoint — 2026-06-24
Vừa hoàn thành: Phase 1 — thống nhất API client, services/api giờ có auto-refresh token qua axios interceptor dùng chung
Đang làm dở: (không)
Bước tiếp theo: Backlog phase sau (useHeartbeat retry, mock data, tách component...) khi được yêu cầu
Blocked:

### Backlog (các phase sau — chưa làm)
- useHeartbeat double-retry, elearning.js trộn mock, useGoogleAuth currentCallback reset,
  setTimeout cleanup, tách component lớn, dọn dead code useAuthGuard.js
