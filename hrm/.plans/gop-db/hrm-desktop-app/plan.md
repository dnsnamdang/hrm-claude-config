# App desktop HRM (Electron) thay cho cài PWA (#chưa có Redmine) — @cuong61n

## Điều tra 25/11/2026
- [x] 25/11 — Badge khác nhau Win/Mac: cùng code `utils/appBadge.js` → `navigator.setAppBadge`; HĐH vẽ (Mac Dock tròn đỏ, Windows overlay 16×16 vuông), Badging API không đổi được. Kết luận: phải bọc app native. User chốt làm Electron, bỏ cách cài PWA.

## ⏸ TẠM DỪNG 25/11/2026 — user bảo dừng sau khi đã chốt hướng Electron. Chưa sửa code hrm-client/hrm-api; thư mục `hrm-desktop` mới `npm install` đã xoá. Muốn làm tiếp: dựng lại theo spec.

## Phase 1 — Vỏ Electron (`HRM/hrm-desktop`)
- [ ] Khởi tạo repo: package.json, electron-builder, `configs/tpe.json` (tên, URL, icon), script build theo cổng
- [ ] `main.js`: cửa sổ chính mở HRM_URL, 1 instance, khay + đóng = thu khay, link ngoài mở trình duyệt, menu tối thiểu
- [ ] Badge: IPC `badge:set` → Mac `app.setBadgeCount`; Windows nhận dataURL icon đã vẽ vòng tròn đỏ → `win.setIcon`
- [ ] `preload.js`: `window.hrmDesktop = { setBadge, platform, version }`, vẽ icon+badge bằng canvas (ảnh icon lấy từ main qua IPC)
- [ ] Tự cập nhật electron-updater provider generic `<HRM_URL>/desktop/`
- [ ] Chạy thử trên Mac: mở HRM local, badge Dock, thông báo chat qua SW, bấm thông báo; dựng ảnh icon Windows ra file để soi

## Phase 2 — hrm-client (nhánh gop_db-main)
- [ ] `utils/appBadge.js`: ưu tiên `window.hrmDesktop.setBadge`, fallback setAppBadge
- [ ] Gỡ PWA: xoá `utils/pwaInstall.js`, bỏ import ở `plugins/chat-sw.js`, bỏ manifest (link head + server-middleware), bỏ `installable` ở `components/chat/ConversationList.vue`
- [ ] Thêm mục "Tải ứng dụng HRM" (Windows/Mac) trong menu thông báo + banner, link `/desktop/HRM-Setup.exe` · `/desktop/HRM.dmg` (ẩn khi đang chạy trong app)

## Phase 3 — Phát hành
- [ ] nginx dev/prod: thư mục `/desktop/` static (hỏi trước khi sửa server)
- [ ] Build Windows (cần máy/CI Windows hoặc build cross trên Mac bằng wine) + Mac, upload `/desktop/`
- [ ] HDSD cài app + gỡ bản PWA cũ
