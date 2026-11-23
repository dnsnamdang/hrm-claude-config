# Favicon tab trình duyệt dùng icon app (logo ETEK SOFTS) — @cuong61n

## Phase 1
### FE (hrm-client, nhánh gop_db)
- [x] 2026-11-23 Tab trình duyệt (vd "Tổng quan") không hiện icon app: thêm `<link rel="icon" png 192>` + `apple-touch-icon` trỏ `/icons/app-192.png` vào `nuxt.config.js` head.link, giữ `favicon.ico` làm dự phòng. Chưa kiểm trên trình duyệt (cần restart nuxt dev; trình duyệt cache favicon nên Ctrl+Shift+R). Trạng thái: chờ test, chưa commit.
- [x] 2026-11-23 Tab vẫn hiện logo cũ (trình duyệt chọn favicon.ico): bỏ khai `.ico` khỏi head.link, thêm `?v=2` chống cache, và thay `static/favicon.ico` bằng icon app (PIL, 16/32/48). Kiểm: cổng 3002 trả thẻ icon PNG mới, file ico đúng định dạng. Chờ user xác nhận trên tab; chưa commit.
