# App desktop HRM (Electron) thay cho cài PWA (#chưa có Redmine) — @cuong61n

## Mục tiêu
Khách dùng Windows muốn số tin chưa đọc trên icon taskbar là **vòng tròn đỏ** như Dock của Mac.
PWA (Badging API) chỉ gửi số, hình do HĐH vẽ (Windows = ô vuông overlay 16×16) ⇒ không làm được bằng web.
Chốt 25/11/2026: **bỏ hẳn cách "Cài HRM thành ứng dụng" (PWA)**, thay bằng app desktop Electron bọc trang HRM.

## Scope
- Repo mới `HRM/hrm-desktop` (Electron 33 + electron-builder): mở URL HRM, khay hệ thống, đóng = thu khay, 1 instance, link ngoài mở trình duyệt, tự cập nhật (electron-updater, provider generic `<HRM_URL>/desktop/`).
- Badge: Mac dùng `app.setBadgeCount` (Dock đỏ hệ thống). Windows vẽ icon app + vòng tròn đỏ góc trên phải bằng canvas trong preload rồi `win.setIcon()` ⇒ nhìn như Mac.
- hrm-client: `utils/appBadge.js` ưu tiên cầu nối `window.hrmDesktop.setBadge(n)`; gỡ `utils/pwaInstall.js`, manifest, nút/mục "Cài HRM thành ứng dụng"; thay bằng mục "Tải ứng dụng HRM" (Windows `.exe` / Mac `.dmg`) trỏ `/desktop/`.
- Mỗi cổng 1 bản build: `configs/<port>.json` (tên, URL, icon). Trước mắt TPE; cổng khác chỉ thêm config.

## Quyết định đã chốt
- Bỏ PWA hoàn toàn (user chốt 25/11/2026), service worker `/sw.js` GIỮ vì thông báo chat dùng nó.
- File cài phát hành tại `<HRM_URL>/desktop/` (nginx static trên server), cùng chỗ cho `latest.yml` tự cập nhật.
- Chưa có chứng chỉ ký Windows ⇒ lần đầu cài SmartScreen cảnh báo, ghi rõ trong HDSD.

## Spec chi tiết
`docs/superpowers/specs/gop-db/2026-11-25-hrm-desktop-app-design.md`
