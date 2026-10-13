> ## ⚠️ NƠI LÀM VIỆC — WORKTREE (chốt 17/09/2026, user yêu cầu)
>
> Nhánh `gop_db` đang được một phiên làm việc khác dùng → mọi thay đổi code của plan này làm trong
> **worktree riêng**, nhánh `feat/quan-ly-phong-hop`:
>
> | Thứ | Đường dẫn |
> |---|---|
> | Repo BE | `/Users/dnsnamdang/Documents/DNSMEDIA/websites/hrm-worktrees/phong-hop-api` |
> | Repo FE | `/Users/dnsnamdang/Documents/DNSMEDIA/websites/hrm-worktrees/phong-hop-client` |
> | Bộ e2e | `/Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/e2e` (DÙNG CHUNG, không có worktree) |
> | Tài liệu (plan, ledger) | `/Users/dnsnamdang/Documents/DNSMEDIA/websites/ERP-HRM/HRM/.plans/gop-db/quan-ly-phong-hop/` |
>
> - API của worktree chạy ở **`http://127.0.0.1:8001`**, Nuxt của worktree ở **`http://127.0.0.1:3001`**.
>   Cổng 8000/3000 là server của phiên khác — **KHÔNG đụng, KHÔNG tắt, KHÔNG `pkill`**.
> - Chạy e2e phải truyền cả 2 biến: `BASE_URL=http://127.0.0.1:3001 API_BASE=http://127.0.0.1:8001`.
> - Phiên đăng nhập của Playwright gắn theo ORIGIN. `.auth/user.json` chỉ dùng được cho `:3000` → đã tạo sẵn
>   **`.auth/user-wt.json`** (admin) và **`.auth/user-nocost-wt.json`** (tài khoản thiếu quyền) với origin
>   đổi sang `:3001`. Spec UI phải khai `test.use({ storageState: '.auth/user-wt.json' })`, KHÔNG dùng
>   `user.json` (dùng nhầm là bị đẩy về `/login`, rất dễ tưởng lỗi đăng nhập).
> - TUYỆT ĐỐI KHÔNG `git commit` / `push` / `stash` / `checkout` file.
> - Worktree KHÔNG có `.plans`, `.claude`, `docs`, `CLAUDE.md` (là symlink ngoài repo) — tài liệu ghi về
>   đường dẫn tài liệu ở bảng trên.
> - Đường dẫn trong phần dưới ghi `hrm-api/...` hay `hrm-client/...` thì hiểu là **thư mục tương ứng trong
>   worktree**, không phải checkout gốc.

## ⚠️ 5 cái bẫy của phase này — đọc trước khi code

1. **KHÔNG có FullCalendar resource-timeline.** Repo chỉ có `@fullcalendar` v5 bản **miễn phí**
   (core/timegrid/list/interaction). Dạng "resource × thời gian" là bản **Premium trả phí** ⇒ lưới Phòng × Giờ
   **phải tự dựng bằng CSS grid**, đừng mất thời gian tìm cách ép FullCalendar làm.
2. **Đo layout trong `watcher` + `$nextTick` ra DOM CŨ** (bẫy đã ghi của dự án): tính toạ độ/độ rộng khối phải
   kèm `requestAnimationFrame`, nếu không lệch đúng 1 nhịp mà **không báo lỗi gì**.
3. **Phiếu QUA ĐÊM** (đã chốt cho phép ở Phase 1): phải hiện ở **mọi ngày nó chạm**, cắt ở mép ngày kèm dấu
   tiếp diễn. Khung giờ lưới phải **tự nới** để ôm trọn phiếu nằm ngoài giờ mở cửa — nếu không, phòng đang bị
   giữ mà lưới trông như trống.
4. **CẤM `networkidle` trong e2e** — màn này có **tự refresh 60 giây**, chờ networkidle là hết giờ test.
   Và `setInterval` phải `clearInterval` khi rời màn, nếu không polling chạy ngầm mãi.
5. **1 request cho cả lưới.** `GET /meeting/rooms/board?date=` trả **cả phòng lẫn phiếu trong ngày**;
   TUYỆT ĐỐI không gọi mỗi phòng một request (spec 6.3, quy tắc hiệu năng của CLAUDE.md).

## Task 22: Tab "Theo tuần (1 phòng)" + tab "Thẻ trạng thái"

- [ ] **Theo tuần**: dùng `@fullcalendar` timeGrid có sẵn (v5 bản free), chọn phòng ở đầu tab, gọi endpoint `week`.
- [ ] **Thẻ trạng thái**: mỗi phòng 1 thẻ — *Đang trống* / *Đang họp đến HH:mm* / *Sắp họp lúc HH:mm*, kèm tên
  cuộc họp + chủ trì. **Tự refresh 60 giây bằng `setInterval`, `clearInterval` ở `beforeDestroy`**.
- [ ] 3 tab giữ được lựa chọn khi chuyển qua lại (không mất ngày/phòng đang chọn).
