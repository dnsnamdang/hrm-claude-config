# Tối ưu thời gian build FE (hrm-client) — nhánh gop_db

Mục tiêu: giảm thời gian `yarn run build` mỗi lần deploy lên `hrm-crm.eteksofts.com`.

## Phase 1 — Bật cache webpack

### FE

- [x] Bật `build.cache: true` + `build.parallel: true` trong `nuxt.config.js` (trước đó cả 2 đang bị comment)
- [x] Đo thực tế trên bản clone của `gop_db-client` (Node 14.21.3, 10 core): baseline 223s → dựng cache 195s → sửa 2 file 134s → sửa 1 file 96s
- [x] Kiểm chứng cache không trả bundle cũ: chèn chuỗi marker vào template, build lại, xác nhận marker có trong `.nuxt/dist/client`
- [ ] User test trên server CRM và xác nhận số liệu thực tế

### Deploy script (server, ngoài repo)

- [ ] Cập nhật `~/build_hrm_crm.sh`: bỏ qua build khi không có file FE đổi; chỉ `yarn install --frozen-lockfile` khi `package.json`/`yarn.lock` đổi; bỏ `npm install` (trộn npm với yarn làm xoá `node_modules/.cache`)

## Phase 2 — Chưa làm, chờ user quyết

- [ ] Gỡ thư viện 0 import: `c3`, `chartist`, `vue-chartist`, `vue-c3`, `vue-slide-bar`, `vue-form-wizard`, `vue-tour`, `vue-knob-control`, `vue-draggable`, `node-zklib`, nhóm `highcharts`
- [ ] Gộp 4 bộ chart đang nuôi song song về `apexcharts` (`chart.js`/`vue-chartjs` chỉ còn 5-6 file dùng)
- [ ] Đổi `node-sass@4` → `sass` (dart-sass); `sass-loader@10` đang dùng đã hỗ trợ sẵn

### Checkpoint — 2026-08-17
Vừa hoàn thành: bật cache+parallel trong `nuxt.config.js` của worktree `gop_db-client`, đo 4 lần build và kiểm chứng tính đúng đắn.
Đang làm dở: chưa có.
Bước tiếp theo: user copy `build_hrm_crm.sh` đã vá lên server, commit `nuxt.config.js`, chạy thử 2 lần build liên tiếp trên server để xác nhận.
Blocked:
