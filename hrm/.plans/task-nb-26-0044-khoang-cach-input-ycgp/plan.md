# Khoảng cách giữa các input màn Chi tiết yêu cầu giải pháp (TPE.TASK.NB.26.0044) — @cuong61n

Nguồn: task nội bộ TPE.TASK.NB.26.0044 trên HRM `/assign/tasks` (giao 14/11/2026, hạn 15/11 17:30).
Nội dung: "Khoảng cách giữa các input đang không đúng với chuẩn chung của phần mềm" — ảnh chụp tab "Thông tin yêu cầu" của YCGP EG.YCP.TC.26.0003.

- [x] 16/11/2026 — Điều tra: tab `pages/assign/request-solution/components/RequestTab.vue` để mọi cột ô `col-md-* mb-3`; chuẩn toàn hệ thống giữa các DÒNG ô là `mb-2` (skill erp-to-hrm-screen, user chốt 14/10/2026; ~150 chỗ trong project dùng `mb-2`), `mb-3` chỉ dùng giữa các card.
- [x] 16/11/2026 — Sửa: đổi 17 cột `col-md-* mb-3` → `mb-2` trong RequestTab.vue (giữ `mb-3` của khối `tp-card` KD panel vì là khoảng giữa card). Chưa đo trình duyệt.
- [x] 16/11/2026 — Khoảng trống đầu card quá rộng (user báo thêm ảnh): khối "Mã yêu cầu/Trạng thái" ở chế độ xem render rỗng (cao 6px + mb-2) đẩy nhãn đầu tiên xuống 46px so với đỉnh card (lề trái 24px). Sửa `v-else` → `v-else-if="request.code || request.status_text"`. Đo Playwright màn /assign/request-solution/37: nhãn đầu cách đỉnh card 28px, lề trái 25px → cân đối.
- [x] 16/11/2026 — Viền kép (user báo ảnh 2): `RequestSolutionForm.vue` lồng 3 lớp viền (tp-card ngoài → `.tp-tab-shell` viền+padding 14px → tp-card trong tab). Bỏ viền `.tp-tab-shell`, padding 14px → `8px 12px 12px`. Đo Playwright /assign/request-solution/37: shell border 0; còn 2 lớp (card ngoài + card trong) cách 12px.
- [x] 16/11/2026 — Góc dưới card ngoài bị mờ: `.tp-tab-shell` nền trắng góc vuông đè lên góc bo → đổi `background: transparent` + bo dưới 0.75rem (đo: bg trong suốt, radius 12px).
- [ ] Chờ test (đo `getBoundingClientRect` giữa 2 dòng ô, so với màn mẫu) + kiểm TktTab.vue (còn `class="mb-3"` ở các section, chưa đụng vì ngoài ảnh task).

Trạng thái: đã sửa code ở working tree hrm-client (nhánh gop_db-main), chưa commit/push.
