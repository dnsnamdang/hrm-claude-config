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

## Ngày 04/11/2026 (@junfoke) — build FE trên server dev sập hết bộ nhớ (exit 134)
- [x] 04/11/2026 — Xử lý lỗi build hrm-client trên server dev hết RAM: build cùng mã ở máy đo heap đỉnh **6.101 MB**, đúng trần ~6.144 MB của `build_common.sh` trên server (server sập ở 6.110 MB sau 805s) ⇒ không phải rò bộ nhớ, mã lớn dần chạm trần. Server chỉ có ~5,9 GB RAM thật (swap đã dùng 3,2 GB) nên không nâng heap được ⇒ mục tiêu heap đỉnh ≤ ~3,5 GB.
- [x] 04/11/2026 — Thử bọc plugin nén esbuild để không dựng source map: không có tác dụng (heap vẫn vọt 2 → 6 GB ở cuối build), chưa phải thủ phạm.

## Ngày 05/11/2026 (@junfoke)
- [x] 05/11/2026 — Tìm ra nguyên nhân thật: plugin sinh client manifest của Nuxt gọi `getStats().toJson()` không tuỳ chọn ở pha emit ⇒ webpack 4 dựng thống kê đầy đủ (mã nguồn, quan hệ import, module từng chunk) cho ~2.300 chunk, chạy liền ~60s, đẩy heap 2 → 6 GB.
- [x] 05/11/2026 — Thêm `build-utils/lean-manifest-stats-plugin.js` (tắt các phần thống kê manifest không dùng) + sửa `nuxt.config.js`. Đo ở máy: heap đỉnh sau GC 6.101 → **2.227 MB**, build qua với giới hạn **4 GB** (trước cần 8 GB), biên dịch 4,3 → 2,2 phút; so mã nén với bản gốc. Commit `e212d0cfb` (develop, đã lên origin develop + gop_db).
- [x] 05/11/2026 — Server dev build lại thành công: **301s, exit 0** (trước sập sau 805s). Cảnh báo Nuxt "process still running… will be fatal in Nuxt 3" sau khi build xong là vô hại (tiến trình phụ esbuild/webpack chưa đóng, Nuxt chờ 5s rồi tự thoát 0), có từ trước bản sửa.
- [x] 05/11/2026 — Ước lượng độ bền theo lịch sử develop (11/2025 700 trang 19 MB .vue → 11/2026 1.263 trang 45 MB): phần phình nhanh (thống kê theo chunk) đã bỏ hẳn, còn lại tăng tỉ lệ với lượng mã; mức an toàn ~80 MB mã ⇒ khoảng 4 tháng nếu giữ tốc độ 8 MB/tháng như 2 tháng gần đây. Dấu hiệu sớm: thời gian build trên server (hiện 301s) tăng rõ. Hướng dứt điểm: build ở máy khác/CI rồi chép lên, hoặc nâng Nuxt/webpack 5.

### Checkpoint — 2026-11-05
Vừa hoàn thành: giảm RAM build FE, server dev build qua.
Đang làm dở: —
Bước tiếp theo: theo dõi thời gian build trên server; Phase 2 vẫn chờ user quyết.
Blocked:
