# Task 20 — RoomTimelineGrid.vue — Báo cáo

## Status: HOÀN THÀNH

## File tạo

1. `hrm-worktrees/phong-hop-client/components/meeting-room/RoomTimelineGrid.vue` — component dùng chung, 1 CSS grid duy nhất (không lồng grid con) cho toàn bộ bảng: góc, header giờ, nhãn phòng, ô trống, khối phiếu, vạch "bây giờ".
2. `hrm-claude-config/hrm/.claude/skills/room-timeline-grid/SKILL.md` — khi nào dùng, bảng props/emit, cách tính cột từ phút (giải thích lý do dùng 1 grid duy nhất), 5 bẫy.
3. `hrm-worktrees/phong-hop-client/pages/meeting/_gridpreview.vue` — page tạm để đo (Task 21 xoá sau khi nối màn thật).
4. `HRM/e2e/tests/meeting/_grid-preview.smoke.spec.ts` — spec tạm đo 3 phép đo bắt buộc.

## ⚠️ Lệch tên file so với brief — có lý do kỹ thuật

Brief yêu cầu `pages/meeting/_grid-preview.vue` (có gạch ngang). Đã thử đúng tên này trước, nhưng
Nuxt 2 sinh route dynamic từ tên file bắt đầu `_` bằng path-to-regexp — path-to-regexp coi `-` là
ký tự **kết thúc tên param**, nên `_grid-preview.vue` bị Nuxt hiểu thành route
`"/meeting/:grid-preview?"` = param `:grid` + literal `-preview`, KHÔNG khớp URL
`/meeting/_grid-preview` (Nuxt trả `route.name = null`, ra thẳng trang lỗi "Không tìm thấy trang
yêu cầu" — đã tái hiện bằng script Playwright độc lập, xem `[console] log {name: null, ...}`).
Đã đổi tên file thành **`_gridpreview.vue`** (bỏ gạch ngang, giữ nguyên dấu `_` đầu theo đúng tinh
thần "page tạm") → route sinh ra `"/meeting/:gridpreview?"`, khớp bình thường. Đã ghi rõ trong
comment đầu spec để Task 21 (người sẽ xoá 2 file tạm này) không bối rối. Đây CHỈ ảnh hưởng page tạm
(dùng dấu `_`) — page thật của Task 21 dùng tên thường sẽ không dính bẫy này.

## Dòng tổng kết Playwright (chạy sạch, không retry)

```
Running 3 tests using 1 worker

[đo thật] cột 14:00: x=1755.00 width=48.00 | khối 14:00-15:30: x=1755.00 width=144.00 (kỳ vọng 144.00)
  ✓  1 … khối 14:00-15:30 bắt đầu đúng mép cột 14:00 và rộng đúng 3 ô (5.0s)
[đo thật] khối qua đêm: x=411.00 | ô đầu lưới Phòng B: x=411.00
  ✓  2 … phiếu qua đêm có dấu tiếp diễn và bắt đầu từ mép trái lưới (7.4s)
[đo thật] tổng số cột giờ hiện tại: 40 (mặc định 07:00-20:00 = 26)
  ✓  3 … khung giờ đã tự nới để chứa phiếu 22:00-02:00 (nhiều cột hơn mặc định 07:00-20:00) (6.9s)

3 passed (19.9s)
```

## 3 số đo DOM thật

1. **Khối 14:00-15:30 vs cột 14:00**: cột `x=1755.00 width=48.00`; khối `x=1755.00 width=144.00`
   (kỳ vọng `48 × 3 = 144.00`) → **khớp tuyệt đối, lệch 0px**, rộng đúng 3 ô.
2. **Phiếu qua đêm**: khối `x=411.00` = ô đầu tiên của lưới Phòng B `x=411.00` → **khớp tuyệt đối,
   lệch 0px** (cắt đúng mép trái lưới); có `←` (`.rtg-continue--start`), KHÔNG có `→` (kết thúc
   trong ngày `date`, không cắt ở cuối).
3. **Khung giờ tự nới**: 40 cột (00:00→20:00, bước 30') so với 26 cột mặc định (07:00→20:00) →
   **nới thêm 14 cột (7 tiếng)** để ôm trọn phần 22:00 hôm trước → 02:00 hôm nay rơi vào ngày xem.

Ghi chú kỹ thuật quan trọng nhất trong quá trình làm: lúc đầu khối phiếu có `margin: 6px 2px`
(lề ngang 2px cho đẹp) làm phép đo #1 lệch đúng 2px — đã tái hiện, sửa thành `margin: 6px 0`
(chỉ lề dọc, không lề ngang) để khối bắt đầu **đúng mép cột theo pixel**, đúng yêu cầu "phép đo
quan trọng nhất" của task. Test đỏ trước khi sửa, xanh sau khi sửa — đã tái hiện đúng quy trình.

## Concerns

- File preview tạm/spec tạm còn nằm trong worktree — Task 21 phải xoá cả 2 (`pages/meeting/_gridpreview.vue` và `e2e/tests/meeting/_grid-preview.smoke.spec.ts`) sau khi nối `RoomTimelineGrid` vào màn thật + có spec e2e chính thức.
- Component chưa test `slot-click` tự thân qua e2e (chỉ đo layout theo yêu cầu task) — hành vi emit được review bằng code, Task 21 khi nối `BookingFormModal` sẽ là bài kiểm thực tế đầu tiên cho `slot-click`.
- Vạch đỏ "bây giờ" dùng `setInterval` 60s + `clearInterval` ở `beforeDestroy` (đúng bẫy #4 của phase) nhưng chưa có ca e2e riêng kiểm tra nó ẩn/hiện đúng theo `date` — không nằm trong 3 phép đo bắt buộc của task này.
