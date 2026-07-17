# Plan — Hero Carousel trang chủ Elearning

- **Người phụ trách**: @junfoke
- **Design**: `.plans/elearning-hero-carousel/design.md`
- **Spec đầy đủ**: `docs/superpowers/specs/2026-07-15-elearning-hero-carousel-design.md`
- **Plan chi tiết**: `docs/superpowers/plans/2026-07-15-elearning-hero-carousel.md`

## Tasks

### Task 1 — Lớp dữ liệu

- [x] Tạo `elearning/src/constants/heroSlides.js` (hằng số + hàm thuần `buildHeroSlides`)
- [x] Verify `buildHeroSlides` bằng node script tạm (6 case: rỗng→fallback, thứ tự ưu tiên, dedupe giữ badge đầu, cùng id khác type, cap 5, không mutate) → 6/6 PASS → đã xoá script
- [x] Thêm getter `heroSlides` vào `elearning/src/stores/elearning.js`
- [x] Lint sạch

### Task 2 — Component + nối dây

- [x] Tạo `elearning/src/components/home/HeroCarousel.vue`
- [x] Sửa `HeroBanner.vue`: nửa trái → `<HeroCarousel>`, bỏ 2 nút demo + `useToast`, thêm prop `slides` + emit `open-learn`
- [x] Sửa `HomeView.vue`: truyền `store.heroSlides`, nối `@open-learn="openLearn"`
- [x] Lint + build pass
- [x] Verify browser: slide thật hiện, badge đúng, 2 nút demo biến mất, cột "Hoạt động gần đây" nguyên vẹn, CTA điều hướng đúng

### Task 3 — Tự chuyển + accessibility

- [x] `current` → ref, thêm state `userPaused`/`hovering`/`focusing`/`reduceMotion`
- [x] Logic `isPlaying` + interval + `watch(count)` reset + cleanup `onBeforeUnmount`
- [x] Bọc `<Transition>` fade + handler hover/focus/keyboard
- [x] Thanh điều khiển: prev / dots / next / pause
- [x] **FIX phát sinh 1** — ngõ cụt nút Play: click Play làm chính nút đó nhận focus → `focusing=true` → carousel không bao giờ chạy lại. Sửa: hover/focus-pause chỉ áp cho vùng nội dung slide, thanh điều khiển nằm ngoài. Theo APG: "It does not resume unless the user activates the rotation control."
- [x] **FIX phát sinh 2** — điều hướng tay không reset đồng hồ: bấm dot lúc chu kỳ sắp hết → slide nhảy đi ngay sau ~0.8s. Sửa: thêm `userGoTo`/`userNext`/`userPrev` nạp lại đồng hồ; timer nội bộ vẫn dùng `goNext` thuần.
- [x] Lint + build pass
- [x] Verify browser (chi tiết ở Checkpoint)
- [x] Verify trường hợp rỗng → banner tĩnh, không control → đã hoàn nguyên getter
- [x] Cập nhật plan.md + STATUS.md

### Task 4 — Dọn nợ kỹ thuật `LearnCard` (user duyệt 2026-07-15: "dọn đi nếu cần thiết")

- [x] Đối chiếu từng dòng: logic `LearnCard` ≡ `useDeadline`, chỉ khác nhánh `state=null` (`''` vs class nền trắng) — không với tới vì pill chỉ render khi `showDeadline && item.deadline`
- [x] `LearnCard.vue`: xoá `todayISO` + `daysBetween` + 3 computed chép lại → gọi `getDeadlineState`/`getDeadlineLabel`/`getDeadlinePillClass` từ composable (−31 dòng)
- [x] Chứng minh tương đương bằng node script: so bản cũ vs `useDeadline` trên **801 ngày (-400 → +400)** → **0 lệch**; mốc biên đúng (-1 late, 0/7 soon, 8 ok) → đã xoá script
- [x] Verify runtime: chặn API `public/subjects` tiêm deadline -3/+5/+30 → 3 pill render đúng nhãn + đúng class màu **trùng khít bản cũ**
- [x] Lint + build pass

## Checkpoint — 2026-07-15

**Vừa hoàn thành:** Toàn bộ Task 1-3. CODE DONE + VERIFIED browser.

**Đã verify (Playwright, `localhost:3001`, chế độ khách):**

| # | Hạng mục | Kết quả |
|---|---|---|
| 1 | Nhịp autoplay | Đo MutationObserver: **6012ms / 5999ms** — đúng 6s, chỉ một timer (không chạy đôi) |
| 2 | Hover dừng | 8s trên hero → không đổi slide |
| 3 | Nút pause DÍNH | Bấm pause → rời chuột → 13s vẫn đứng yên; nút đổi nhãn + icon play |
| 4 | Bấm Play chạy lại | Chạy lại ngay **dù nút vẫn giữ focus + chuột vẫn trên nút** (kịch bản lỗi cũ) |
| 5 | Dot | Bấm dot 3 → đúng slide 3, `aria-current` đúng index 2 |
| 6 | Reset đồng hồ khi bấm dot | Bấm lúc chu kỳ còn 0.8s → giữ trọn 6s rồi mới nhảy |
| 7 | Bàn phím | ArrowRight 0→1, ArrowLeft 1→0, wrap-around 0→4 |
| 8 | Focus-pause nội dung | Focus nút CTA trong slide → dừng 8s |
| 9 | `prefers-reduced-motion` | autoplay tắt hẳn (9s), nút pause ẩn, dot vẫn bấm được |
| 10 | CTA điều hướng | Slide type `path` → `/lo-trinh/test-lo-trinh-hoc` đúng nhánh |
| 11 | Console | 0 lỗi, 0 cảnh báo |
| 12 | Trường hợp rỗng | Banner tĩnh TPE_BANNER.jpg + badge "Elearning TanPhat Etek", 0 dot / 0 mũi tên / 0 pause / 0 CTA, không tự chuyển |
| 13 | `thumb` rỗng | Dùng gradient trung tính (không ảnh giả) |
| 14 | Cột "Hoạt động gần đây" | Nguyên vẹn, không regression |
| 15 | eslint + build | Sạch, build pass (Node 24.6.0) |

**Verify bổ sung (2026-07-15, sau khi dọn nợ `LearnCard`)** — gỡ được các mục trước đó ghi "chưa verify", bằng cách **chặn response API và tiêm data** (`page.route`) thay vì cần tài khoản learner. Lưu ý shape: rows của `public/subjects` nằm ở `data.items` (lần tiêm đầu trượt vì nhắm `data.data`).

| # | Hạng mục | Kết quả |
|---|---|---|
| 16 | Badge "Bạn cần học" | Hiện đúng — thứ tự ưu tiên need → recommend chạy đúng trên UI thật |
| 17 | Pill "Bắt buộc" | Hiện đúng |
| 18 | Pill hạn trên nền tối | "Hạn: 12/07/2026 • Quá hạn 3 ngày", class `text-white border-red-400/40 bg-red-500/40` — ảnh chụp xác nhận đọc rõ trên ảnh nền |
| 19 | CTA theo `learn_status` | `learning` + `progress=45` → "Học tiếp 45%" |
| 20 | Khử trùng lặp ở runtime | 2 item tiêm vào `need_to_learn` vốn lấy từ pool `popular` → KHÔNG xuất hiện lại ở slide sau. 5 slide, 0 tiêu đề trùng, badge đúng thứ tự `need,need,recommend,recommend,recommend` |
| 21 | `LearnCard` sau refactor | 3 pill hạn (-3/+5/+30) render đúng nhãn + class màu trùng khít bản cũ |

**CHƯA verify được:** không còn mục nào.

**Bước tiếp theo:** User xem lại bằng mắt trên browser (tuỳ chọn). Không có việc gì phải chạy (không migration/lệnh).

**Blocked:** không.
