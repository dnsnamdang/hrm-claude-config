# Plan tổng — Phân hệ Công việc (Không gian làm việc + Nhóm chat)

> **For agentic workers:** mỗi giai đoạn có plan chi tiết riêng (TDD, bite-sized) trong folder con `gdN-<ten>/plan.md`, viết khi BẮT ĐẦU giai đoạn đó (memory feature-lon-folder-chua-folder-con). Khi chạy plan chi tiết: REQUIRED SUB-SKILL superpowers:subagent-driven-development hoặc superpowers:executing-plans.

**Goal:** Nhân viên chọn 1 không gian (Nhóm trao đổi / Dự án khách hàng) để giao việc bằng Nhiệm vụ / Vấn đề và trao đổi bằng nhóm chat, trên web + app; không gian TKT và Giải pháp thay 2 màn manager cũ.

**Architecture:** 1 bảng không gian (phẳng — 09/11) + bảng thành viên (Nhóm trao đổi thêm tay / lấy 1 lần từ phòng ban; Dự án KH đọc nguồn gốc; TKT–GP ghi về bảng gốc qua adapter theo loại) + 1 hàm kiểm quyền chung. Nhiệm vụ / Vấn đề thêm cột không gian (nullable). Màn không gian = tab chung + tab riêng do loại khai báo. Chat = bảng tin nhắn kiểu tin + đối tượng gắn kèm, đẩy realtime qua `hrm-api/server_node/server.js` (sửa tách sự kiện chat), app qua FCM; tin hệ thống qua Laravel event + listener.

**Tech Stack:** Laravel 8 / PHP 7.4 (`Modules/Assign`), Nuxt 2 / Vue 2 (`pages/assign`, V2Base*), Node socket.io + Redis, Flutter (TPE_APP), MySQL.

**Spec:** `docs/superpowers/specs/gop-db/2026-11-02-phan-he-cong-viec-design.md` · tóm tắt `design.md` cùng folder.

## Global Constraints
- Nhánh `gop_db` (hrm-api, hrm-client); TPE_APP hỏi nhánh trước khi sửa. Không dùng `mysql2`.
- **Mọi bước code / migration / chạy migrate / seeder / commit phải xin phép riêng** kèm phạm vi (CLAUDE.md gốc). Plan được duyệt ≠ lệnh code.
- Model mới `extends BaseModel`; `company_id/department_id/part_id` nullable; file dùng bảng `files` chung.
- Quyền mới (nếu cần) khai ở Catalog `app/Support/Permissions/Catalog/` (skill permission-seeder) — seeder đã gỡ 06/11.
- FE màn mới: chỉ `V2Base*`, popup `V2BaseModal`, xác nhận `base-confirm-modal`, badge màu do BE trả, nút ẩn chứ không disable, `mr-2 mb-2` (HRM/CLAUDE.md).
- Thông báo theo `.claude/skills/notification-convention/SKILL.md`.
- Lên prod: tính năng đang dev ẩn qua Cài đặt phân hệ (key menu mới) — không feature flag riêng.
- Sửa FE phải kiểm bằng Playwright MCP + đo DOM trước khi báo xong; không tự chạy e2e mỗi task (chỉ khi user yêu cầu).

## Review Focus (áp cho mọi giai đoạn)
1. Người ngoài Nhóm trao đổi mở thẳng URL / gọi API chat, file của nhóm → phải 403; nhiệm vụ của nhóm chỉ mở cho người có vai trò trên việc / quyền xem theo tổ chức (test BE ở GĐ1, GĐ3).
2. Kinh doanh mở không gian Giải pháp (và ngược lại) khi không là thành viên → 403; nhưng vẫn thấy vấn đề GP mình dính vai trò ở tab Vấn đề TKT (test GĐ2).
3. (09/11) Lấy thành viên từ phòng ban: chép 1 lần, bỏ trùng, không đổi vai trò người đã có; nhân viên chuyển phòng ban sau đó KHÔNG tự ra khỏi nhóm (test GĐ1).
4. Thành viên GP bị khoá (INACTIVE) → không vào không gian GP, không nhận push chat (test GĐ1/GĐ3).
5. Tin chat đẩy qua socket KHÔNG bật chuông/toast thông báo (test socket GĐ3).

---

## GĐ0 — Mockup (tài liệu, không phải source)
Folder: `gd0-mockup/` · đầu ra HTML self-contained dựng trên DOM + CSS thật của app (memory hrm-demo-html-dung-style-v2, cách "Lần 4").
- [x] M1. Đo khuôn từ app đang chạy (`/assign/solutions/{id}/manager`, `/assign/prospective-projects/{id}/manager`, `/assign/tasks`): CSS + markup có `data-v-*`; ghi bảng token đầu file.
- [x] M2. Màn vào phân hệ: danh sách không gian của tôi (Phòng / Dự án / Lưu trữ).
- [x] M3b. (03/11, góp ý user) Thanh tab: 5 tab cố định Tổng quan · Nhiệm vụ · Vấn đề · Meeting · File + nút "Thêm ▾" (menu các tab còn lại, TKT/GP chia nhóm) + nút Trao đổi ở mép phải; tab Meeting chung (màn 15), menu Thêm mở (màn 14). Đo 1440 + 1366: không tràn ngang.
- [x] M3. (03/11 xong: + Vấn đề 19 · File 20 · Cấu hình 21; mọi tab danh sách đổi sang thanh công cụ gọn) · Meeting ✔ màn 15 Màn không gian Phòng: Tổng quan · Nhiệm vụ · Vấn đề · Trao đổi · File · Thành viên · Nhóm · Cấu hình.
- [x] M4. (03/11 đổi theo chốt bỏ Nhóm) Dự án nội bộ thuộc phòng (Mở/Kín, màn 06–08) + popup Tạo không gian 3 ca: Phòng làm việc theo phòng ban / tự chọn / Dự án nội bộ (có Thuộc phòng + Mở/Kín) — màn 11–13.
- [x] M3c. (03/11) Thanh công cụ gọn cho tab danh sách (màn 16–18) — **user duyệt 03/11**; đánh giá ảnh hưởng ở spec §5.4; duyệt thì áp cho mọi tab danh sách (Nhiệm vụ, Vấn đề, Meeting, File, Thành viên, Dự án nội bộ).
- [x] M5. (03/11 xong: + Tổng quan GP 22 · Hạng mục 23) Không gian Dự án KH · Giải pháp (tab chung + tab riêng theo §3.9; Hạng mục là tab riêng; Thành viên có trường GP).
- [x] M6. Không gian TKT (§3.10; tab Vấn đề / File gộp có cột Nguồn).
- [x] M7. Chat: tin thường, trả lời, @, file, thẻ `#` nhiệm vụ, tin hệ thống, "Tạo nhiệm vụ từ tin nhắn".
- [x] M7b. (04/11, user) Chat demo chạy thật màn 04 + 08 (U25, `_build/chatx.js` + `chatx.css`): @, #, đính kèm/kéo thả/dán ảnh, trả lời, cảm xúc, ghim, sửa, thu hồi, tìm, tạo nhanh nhiệm vụ/vấn đề (từ tin + từ ô soạn), nút trên thẻ theo vai trò → tin hệ thống tự báo theo cấu hình 9 sự kiện, mô phỏng sự kiện người khác, thẻ khoá dự án Kín. Đo 1440 + 1366: không tràn ngang, 0 lỗi JS.
- [x] M8. App (Pencil, `meeting-mobile.pen` khu Công việc): danh sách không gian, chat, tạo nhanh từ tin — **dựng 05/11**, hàng mới y 5040–6570, x 16073–19777 (backup `meeting-mobile.backup-20261105-truoc-khong-gian-chat.pen`). 8 màn: KG-01 danh sách (tab 2) · KG-02 Trao đổi · KG-03 nhấn giữ tin → sheet · KG-04 Tạo nhiệm vụ từ tin (form NV-10 điền sẵn, L3) · KG-05 gõ # chèn việc · KG-06 tab Nhiệm vụ của không gian · KG-07 Thông tin không gian · KG-08 rỗng. Đã đổi thanh dưới 8 màn cũ (NV-01/02/16, CV-00b, CV-PD1/PD2, VD-01/02) theo U26. **Chờ user Cmd+S + duyệt.**
  - C-M1 (Claude chốt, thuần UI): KG-01 xếp Đã ghim → Gần đây theo tin mới nhất (kiểu app chat), không chia khối theo loại như panel web; lọc loại bằng chip.
  - C-M2 (Claude chốt, spec §4.5 [B]): thông báo theo không gian 3 mức Tất cả / Chỉ khi được @ / Tắt, lưu theo người dùng ở BE (KG-07).
  - **(05/11 tối) U35 — user chốt:** app có thêm **Tổng quan + Meeting**; thanh tab app (cuộn ngang): Trao đổi · Tổng quan · Nhiệm vụ · Vấn đề · Meeting · File (Trao đổi đứng đầu vì dùng nhiều nhất trên app). Thành viên / Dự án nội bộ của phòng / Hạng mục GP: **chỉ xem** ở màn Thông tin. Tạo không gian, quản lý thành viên, Cấu hình sự kiện: giữ chỉ web (§5.2). Thay dòng dưới (4 tab) — đã lỗi thời.
  - **(05/11 tối) KG-01 thiết kế lại theo góp ý:** bỏ tin mới nhất + cảnh báo quá hạn; dòng = icon loại + tên 1 dòng + chip chưa đọc ('@' khi bị nhắc, xám + 🔕 khi tắt thông báo); chỉ Dự án KH có dòng phụ loại · khách hàng; gom Đã ghim · Phòng (dự án nội bộ thụt dưới phòng) · Dự án nội bộ · Dự án KH · Lưu trữ. Thay C-M1.
  - **(05/11 tối) Rà soát với mockup web — bổ sung KG-09…KG-20:** KG-09 nhấn giữ không gian (Ghim ≤5 · Đánh dấu đã đọc · Thông báo Tất cả/Chỉ @/Tắt) · KG-10 Lưu trữ · KG-11 Tổng quan (5 ô, chạm mở tab đã lọc) · KG-12 Meeting · KG-13 File · KG-14 Thông tin Giải pháp (Hạng mục, liên kết TKT) · KG-15 chat đủ trạng thái (tin ghim, nút theo vai trò trên thẻ, thẻ khoá, thu hồi, đã sửa, đã xem, ↓ tin mới) · KG-16 nhấn giữ tin của mình (Sửa, Thu hồi, Ghim) · KG-17 danh sách tin ghim (≤20) · KG-18 tìm trong trao đổi · KG-19 nút + ô soạn (Nhiệm vụ mới, Vấn đề mới, Chèn việc, Ảnh, Chụp, Tệp) · KG-20 vai trò Xem chỉ đọc. Sửa kèm: KG-07 thêm Dự án nội bộ của phòng; KG-03 thêm Ghim; tab mới cho KG-02/03/05/06; nút + thay 📎.
  - **(05/11 tối) Góp ý KG-06 (thanh tab + chip + Gom/Sắp rối, tốn chỗ):** dựng 2 phương án cạnh nhau (x 25530): **KG-06A** 1 hàng công cụ 44px — nút lọc thả xuống 'Tất cả · 8 ▾' + '1 quá hạn' + 🔍 + ⚙ Cách xem (đề xuất) · **KG-06B** ô tìm có nút Lọc bên trong + dòng tóm tắt. **KG-06C** sheet Cách xem = Gom theo · Sắp xếp · **Trường hiển thị** (như Cấu hình cột chế độ Danh sách của web: luôn hiện tên/trạng thái/hạn/nút/💬; tuỳ chọn bật mặc định Người làm · Tiến độ · Người giao & cập nhật; tắt mặc định Mã · Thẻ · Dự án/Hạng mục · Người duyệt · Số file; lưu dùng chung web). **KG-06D** menu lọc mở + dòng bật thêm Mã/Thẻ/Dự án. **05/11 user chọn A** → đã áp cho KG-06, NV2-01/03, tab Vấn đề.
  - **Đã áp A (05/11):** KG-06 cũ + KG-06B xoá, KG-06A thay vào chỗ KG-06 (x 18438); KG-06C/D dời x 25530/26003. NV2-01/02/03: thanh 146px → 1 hàng 44px `Tất cả · 22 ▾` + `3 quá hạn` · 🔍 · ☰ Bộ lọc nâng cao · ⚙ Cách xem (NV2-03 gom Hạn ⇒ chấm xanh); sheet NV2-02 thay bằng đúng sheet KG-06C (có Trường hiển thị). VD-01/02: `Tôi phụ trách xử lý · 4 ▾` + `1 quá hạn` · 🔍 · ☰ (không ⚙ vì Vấn đề không gom nhóm), bỏ dòng "Tổng · Quá hạn". Màn cũ NV-01/02/16 (đã bị NV2 thay) không sửa. **Chờ user Cmd+S + duyệt.**
  - **[B] còn treo:** ~~ai được ghim tin~~ → **chốt 05/11: Quản lý + Thành viên ghim/bỏ ghim, vai trò Xem không; tin ghim ghi "X đã ghim"** · ~~vai trò Xem có gửi tin ở dự án Mở không~~ → **chốt 05/11: chỉ đọc + nút Xin tham gia gửi Quản lý duyệt (luồng mới, cần bảng yêu cầu) — bổ sung KG-20 + mockup web** · ~~sửa / thu hồi~~ → **chốt 05/11: trong 24h kể từ lúc gửi, BE kiểm**. Hết [B] treo của chat.
  - **(05/11) Đóng / mở lại không gian — user chốt 4 điểm** (spec §3.11): việc dở tự huỷ (nhiệm vụ → Huỷ 9, vấn đề → Đã đóng; mở lại không khôi phục) · ai đóng = Quản lý dự án + Quản lý Phòng cha; Phòng tự chọn = Quản lý phòng · Phòng theo phòng ban tự lưu trữ theo phòng ban, Phòng tự chọn đóng tay, chặn đóng khi còn dự án con đang chạy · popup chọn Kết quả Hoàn thành / Dừng + lý do. **Đã vẽ 05/11:** web màn 06 menu ⋮ → popup Đóng dự án (Kết quả Hoàn thành / Dừng + lý do bắt buộc khi Dừng, khối vàng liệt kê việc dở sẽ Huỷ / Đã đóng, nút đỏ) + Mở lại (`_build/close.js`, `close.css` nhúng vào màn 06); màn 08 Mô phỏng → "Quản lý đóng dự án": chat chỉ đọc, tin hệ thống, việc trong cột Việc chuyển Huỷ / Đã đóng, nút Mở lại — kiểm Playwright 0 lỗi JS. App: KG-22 sheet Đóng dự án, KG-23 trao đổi dự án đã đóng + Mở lại (Claude tự chốt: app cũng Đóng / Mở lại được). **Ca Phòng:** web màn 21 mục Lưu trữ — Phòng theo phòng ban không còn nút (ghi "tự lưu trữ theo phòng ban", nhãn Đang hoạt động) + dòng Mockup "Ca Phòng tự chọn" → popup "Chưa đóng được" liệt kê 2 dự án con, lối sang đóng từng dự án (`_build/arch21.js/.css` nhúng màn 21, kiểm Playwright 0 lỗi JS). App KG-24 sheet tương ứng. C7 app đã sửa (đường vào Huỷ = đóng dự án).
  - **(05/11) Sắp lại khu Công việc trong `meeting-mobile.pen` để thuyết trình:** mục lục (y −1580) + 14 nhóm xếp dọc từ y −1430, mỗi nhóm 1 khung tiêu đề nền tối (tên · mô tả · luồng bấm) + 1 hàng màn trái → phải; caption màn có số bước ①.1, ①.2…: ① Vào phân hệ · ② Trong không gian · ③ Trao đổi · ④ Chỉ xem & xin tham gia · ⑤ NV danh sách · ⑥ NV tạo & giao · ⑦ NV duyệt triển khai · ⑧ NV người làm · ⑨ NV người giao & duyệt KQ · ⑩ NV tiện ích · ⑪ VĐ báo & giao · ⑫ VĐ xử lý & duyệt đóng · ⑬ Phê duyệt · ⑭ Đóng / mở lại. 20 màn cũ (NV-01/03/05–14, VD-01/03–08) dồn xuống khu "Bản cũ" (y 21946). Toạ độ cũ ghi ở các mục trên không còn đúng — tìm theo tên màn.
  - **(05/11) Vấn đề v2 trên app:** user chốt U36 (trạng thái khi tạo tự suy theo người nhận) + U37 (Báo đã xử lý có Cách xử lý * + Nhóm nguyên nhân *). Dựng VD2-01…VD2-16 (`app-cong-viec-nhiem-vu-van-de/design.md` Đợt 3). **(05/11) Đã sửa mockup web GĐ0** (`_build/td.js`, `chatx.js/.css`, `mockup.css` → nhúng lại vào màn 03, 19, 04, 08, 29; kiểm Playwright 1440, 0 lỗi JS): bỏ Trọng số KPI (Thiết lập n/3) · công tắc Cần duyệt triển khai + Bắt đầu ngay · form Vấn đề theo U36 (Loại / Mức độ ảnh hưởng / Nguồn phát hiện / Người phụ trách hoặc Phòng ban + dòng báo trước trạng thái, Người duyệt đóng, Mô tả bắt buộc, nút Gửi vấn đề) · chat: người chỉ xem (Mô phỏng sự kiện ở màn 08 → "Xem như người chỉ xem") + Xin tham gia, sửa / thu hồi trong 24 giờ, chữ luật ghim · sửa lỗi lưới ô c4/c6 bị kéo full dòng. Chưa vẽ phía Quản lý duyệt yêu cầu tham gia trên web (app có KG-21). **(05/11) Thiết kế lại form Tạo / Sửa nhiệm vụ web theo khuôn app** (user chốt: web GIỮ Lặp lại, GIỮ nút "Giao & tạo tiếp" riêng): Không gian làm việc + Dự án / Nhóm · Loại · Tên · Người thực hiện + Số giờ · công tắc Cần duyệt triển khai · Ngày bắt đầu / Hạn / Giờ (mặc định 17:30, U33) + chọn nhanh · Mức độ ưu tiên chip tô màu (U32) + Meeting · Mô tả · hàng "+ Checklist · + Nhiệm vụ con · + Tệp" (U27) · Thiết lập trong form "n/5 đang dùng": Người duyệt kết quả · Người theo dõi · Thẻ · Báo cáo tiến độ + giờ nhắc · Lặp lại (U34). Form vấn đề dùng chung chip ưu tiên, 17:30, ô Không gian. Kiểm Playwright 1440: tạo → mở Sửa giữ đủ dữ liệu, báo lỗi đồng thời, không tràn ngang, 0 lỗi JS. **Sửa theo góp ý (Checklist + Nhiệm vụ con chưa đúng):** bỏ ô nhập nhiều dòng, làm lại bám `CreateTaskModal.vue:418-700` — Checklist: ô "Nhập mục checklist và Enter" + [+], "n/m hoàn thành", Thêm nhanh n dòng trống, mỗi dòng ⠿ · tick · sửa · xoá; Nhiệm vụ con: hàng tiêu đề Tên · Người làm · Hạn (ngày) · Giờ hạn (17:30), dòng thêm + [+]/Enter, Thêm nhanh, mỗi dòng sửa / xoá, bắt buộc tên + người làm + hạn (báo dưới từng dòng). Đo Playwright: cột 3 hàng thẳng nhau, Sửa lại giữ đủ. **U39 (05/11) Ngày bắt đầu không bắt buộc:** web màn 03 ẩn sau "+ Ngày bắt đầu" (để trống → ngày giao việc; vẫn chặn Hạn < Ngày bắt đầu), app thêm link dưới Hạn ở NV2-10/11/13/32–37, KG-04. **Việc cho GĐ2 code:** BE tự điền `start_date` = ngày giao khi trống; FE bỏ `*` + `seedDates()`. **Việc cho GĐ2 web:** bỏ ô Trạng thái ở form tạo vấn đề (tự suy), API đổi trạng thái nhận `resolution` + `root_cause_group` (cột `resolution` đang varchar 255 → cân nhắc text).
  - **(05/11) Xin tham gia — app:** KG-20 dải "👁 Bạn chỉ có quyền xem" + nút Xin tham gia; **KG-21** (x 26476) Thông tin dự án nội bộ Mở phía Quản lý: khối YÊU CẦU THAM GIA trên phần Thành viên, mỗi dòng ✓ Đồng ý / ✕ Từ chối; mở từ thông báo. Duyệt làm được trên app, thêm/bớt thành viên khác vẫn trên web. **Còn: bổ sung mockup web GĐ0 (màn dự án Mở + tab Thành viên) khi làm plan GĐ2.**
  - Không gian trên app chỉ 4 tab Trao đổi · Nhiệm vụ · Vấn đề · File; Thông tin chỉ xem; thêm/bớt thành viên, cấu hình sự kiện, tạo không gian chỉ trên web (spec §5.2).
  - **U26 (user 05/11):** thanh dưới app phân hệ Công việc đổi U3 → **Việc của tôi · Không gian · [+ Tạo mới] · Nhiệm vụ · Phê duyệt**; ô Không gian có chấm đỏ khi có tin chưa đọc (khuôn badge C/BottomNav); **Vấn đề chuyển vào drawer**, vẫn tạo được từ [+].
- [x] M9. Đo lại mockup bằng Playwright (1440 + 1366 ✔), ghi quyết định tự chốt vào comment đầu file ✔; **user CHỐT mockup 05/11/2026** — 30 màn + màn thuyết minh logic `gd0-mockup/thuyet-minh.html`.
- [x] M10. (05/11) Màn thuyết minh logic: 12 mục (không gian, thành viên, quyền xem, quyền tạo, màn không gian, Phòng ↔ GP, vòng đời Nhiệm vụ / Vấn đề, gom theo Hạn, Trao đổi + 9 sự kiện, sidebar, điểm cần chốt L2–L4, lộ trình); link từ index.html + present.html.

## GĐ1 — Nền không gian + quyền (BE trước, FE tối thiểu)
> **(11/11) Đợt CORE CHAT (Nhóm trao đổi + chat 1–1) — plan riêng `.plans/agent-chat/chat/gd1-core-chat/plan.md`** (thay các dòng dưới cho phần nhóm + chat; các dòng còn lại theo mô hình cũ, đọc với N4). Chờ user duyệt + trả lời Q1–Q4, chưa có lệnh code.
- [ ] BE: bảng không gian (họ, loại, kiểu, cha = Phòng làm việc cho Dự án nội bộ, chế độ Mở/Kín, thời hạn, trạng thái, company_id, liên kết nguồn) + bảng thành viên (vai trò, nguồn) + migration.
- [ ] BE: adapter nguồn thành viên theo loại (phòng ban/bộ phận, tay, TKT, Giải pháp/hạng mục); đồng bộ Phòng theo phòng ban (K4).
- [ ] BE: hàm kiểm quyền chung §3.4 + K2 + K7; bịt `TaskController::show` / `TaskService::update` (+ Issue).
- [ ] BE: API không gian (danh sách của tôi, chi tiết, tạo/sửa/đóng, thành viên, nhóm); quyền "Quản lý phòng làm việc".
- [ ] BE: không gian tự sinh cho TKT / Giải pháp (+ backfill 484 TKT, 40 GP).
- [ ] FE: màn danh sách không gian (lọc 2 họ) + khung màn không gian (5 tab + Thêm + Trao đổi) + Thành viên + Dự án nội bộ của phòng + Cấu hình.

## GĐ2 — Nhiệm vụ / Vấn đề theo không gian + thay 2 màn manager
- [ ] BE: cột không gian trên `tasks` / `issues` (nullable, K1) + backfill 19 nhiệm vụ → không gian GP; lọc danh sách theo không gian.
- [ ] FE: `V2BaseSmartFilterPanel` thêm `variant="toolbar"` (mặc định giữ `card`) + popover kéo giãn + xử lý select2/lịch trong popover + tìm khi gõ; BE: số đếm chip (Của tôi / Chờ tôi duyệt) dùng chung scope quyền — spec §5.4.
- [ ] FE: thanh tab 5 cố định + menu Thêm + nút Trao đổi (spec §5.1); tab Meeting chung + bảng nối meeting ↔ không gian (Phòng/Dự án/Nhóm; TKT/GP giữ nguồn cũ).
- [ ] FE: sidebar truy cập nhanh (spec §5.1, U14) — trong `SaleHubSidebar.vue`: mục rail "Không gian làm việc" mở panel chuyển nhanh (ô tìm, Ctrl K, nhóm Ghim & gần đây · Phòng làm việc + Dự án nội bộ con · Dự án nội bộ · Dự án KH · Lưu trữ) + tối đa 5 không gian ghim trên rail; BE: API danh sách không gian của tôi gọn (id, tên, loại, cha, số chưa đọc, số quá hạn) + bảng ghim theo người dùng + ghi "mở gần đây"; màn không gian chuyển sang layout hub (có rail).
- [ ] FE: tab Nhiệm vụ / Vấn đề 2 cách xem Danh sách nhóm (mặc định, gom theo Trạng thái / Người làm / Hạn / Dự án) · Bảng (spec §5.1, U19); BE: đếm theo nhóm + tải theo nhóm. Kanban để sau.
- [ ] FE+BE: panel chi tiết Nhiệm vụ / Vấn đề thay CreateTaskModal + ImportResultModal (spec §5.1 "Đề xuất thay popup Nhiệm vụ", U20–U21): sửa từng trường (API PATCH 1 trường + lịch sử), Thiết lập, Nhật ký tiến độ, bấm vào hạn, **Đề nghị gia hạn (bảng mới)**, Thêm nhanh → Nháp.
- [ ] FE: 1 tab Nhiệm vụ chung thay 4 bản copy; `CreateTaskModal` / `CreateIssueModal` nhận không gian.
- [ ] FE+BE: không gian Giải pháp chứa đủ tab §3.9 (tab riêng tái dùng component hiện có).
- [ ] FE+BE: không gian TKT chứa đủ tab §3.10; tab Vấn đề / File gộp có Nguồn.
- [ ] Chuyển mọi đường dẫn manager cũ (danh sách, thông báo, meeting, báo cáo) sang không gian; bỏ 2 màn cũ.

## GĐ3 — Chat đợt 1 (web)
- [ ] BE: bảng tin nhắn + đã đọc; API gửi/sửa/xoá/lấy theo con trỏ; @nhắc tên; file; thẻ đối tượng (Nhiệm vụ/Vấn đề) kiểm quyền khi render.
- [ ] Socket: sửa `server_node/server.js` tách sự kiện chat khỏi `notification`; publish theo lô qua job.
- [ ] FE: tab Trao đổi; đếm chưa đọc; tạo nhiệm vụ/vấn đề từ tin nhắn (lưu tin gốc, nhảy về tin).

## GĐ3-AI — Trợ lý AI thử nghiệm (chạy cùng đợt Nhóm trao đổi GĐ1–GĐ3) [U 11/11]
User 11/11: *"làm thử nghiệm cho phân hệ Công việc cùng đợt với làm Nhóm trao đổi"* — chốt PHẠM VI + THỜI ĐIỂM, **chưa phải lệnh code**. Ý tưởng + định hướng chọn công cụ: `.plans/agent-chat/agent/y-tuong.md`.
- [ ] AI0. Tài liệu: danh sách 5–10 công cụ đợt 1 (tên, mô tả 4 ý, tham số, service có sẵn bọc bên trong — đọc kỹ service trước khi ghi) + bộ ~50 câu hỏi mẫu có đáp án công cụ đúng.
- [x] AI1. (11/11) Mockup **màn 33 Trợ lý ERP** (`screens/33-tro-ly-erp.html` = bản 31 + `_build/ai.js`/`ai.css`) — user 11/11: *"mục đích để giới thiệu giải pháp cho khách hàng nên cần ấn tượng, mượt, phản hồi chính xác · thể hiện được việc phân quyền rõ ràng ai được hỏi gì, bị chặn khi quá quyền hạn"*. Hội thoại "Trợ lý ERP" ghim đầu danh sách; nút demo **Xem như** Nhân viên / Trưởng phòng / Giám đốc; mỗi câu trả lời có dòng **các bước** (Người hỏi → Kiểm quyền → Tra dữ liệu, bấm mở) + nguồn + giờ dữ liệu; chữ hiện dần, thẻ việc / lịch họp / biểu đồ / xếp hạng; quá quyền ⇒ thẻ vàng 🔒 nêu quyền cần + "chưa đọc dữ liệu nào" + nút hỏi trong phạm vi của mình; trùng tên ⇒ hỏi lại chọn người; lương / giá vốn / công nợ loại trừ mọi vai trò; cột phải: quyền đang có, bảng **Ai được hỏi gì**, **Nhật ký lượt hỏi**. 7 câu kịch bản. Kiểm Playwright 1366 + 1440: đầu 64px, không tràn, 7 kịch bản đúng loại kết quả theo vai, chuyển sang chat 1–1 rồi quay lại giữ hội thoại, 0 lỗi JS (chỉ 404 favicon của http.server).
- [x] AI1c. (11/11, user: "có tính được token của từng user không?" → "làm 1 và 2") Màn 33: dưới mỗi câu trả lời dòng token (tổng · đọc từ cache · số lần gọi · giây · ≈ ₫), nhật ký có token + ₫, cột phải "Hôm nay đã hỏi n / hạn mức" + chi phí hôm nay + link sang 34. **Màn 34 Thống kê sử dụng Trợ lý** (`screens/34-thong-ke-tro-ly.html` = khung màn 01 + `_build/aiu.js/.css`): 4 ô số (lượt hỏi · token + % cache · chi phí so ngân sách tháng có vạch dự kiến · bị chặn do quyền), biểu đồ cột chồng lượt hỏi theo ngày (Trả lời / Bị chặn / Không hỗ trợ — màu đã chạy validate_palette PASS, rê chuột xem số), khối "Bị chặn nhiều nhất theo quyền", bảng Theo nhân viên (Tên - Mã phòng - Mã NV, hôm nay / hạn mức, Gần chạm) / Theo phòng ban, ngăn kéo Nhật ký lượt hỏi, popup Cài hạn mức (ngân sách tháng, cảnh báo %, khi hết ngân sách, câu/ngày theo vai trò). Giá giả định Sonnet 5.5 + 26,000 ₫/USD. Kiểm Playwright 1366 + 1440: không tràn, tooltip nằm trong khung biểu đồ, 2 bảng 10/8 dòng, nhật ký 5 dòng, popup lưu đóng, 0 lỗi JS.
- [x] AI1d. (11/11) User: (1) "thêm màn 33 vào danh sách chọn" → thanh trình chiếu (STORY nhúng 30 màn) + `present.html` thêm nhóm **TPE SMART AGENT (AI)** gồm 33, 34 (đánh số lại 19–30), ghi chú trình chiếu ở `present-notes.js`; (2) **hạn mức theo Chức vụ trong hồ sơ nhân viên**: popup Cài hạn mức = mức theo **nhóm chức vụ** (Lãnh đạo · Quản lý · Chuyên viên · Nhân viên · Nhân viên phổ thông — lấy từ `working_position_groups` DB local, công ty 1 có 170 chức vụ) + dòng "Chưa khai chức vụ" + **cài riêng từng chức vụ** (`working_positions`, ưu tiên hơn nhóm); bảng 34 cột Vai trò → Chức vụ; 33 cột phải ghi "Hạn mức theo chức vụ … (nhóm …)"; (3) tên **TPE SMART AGENT** + linh vật robot (kính mặt elip xanh #2B59A7 từ logo Tân Phát ETEK `hrm-client/assets/images/logo-etek.jpg`, đèn ăng-ten, tay cầm cờ lê, ngực "TPE", chớp mắt / vẫy tay / bồng bềnh, tắt khi reduced-motion) + khẩu hiệu "Hội tụ tinh hoa - Tiên phong giải pháp". Facebook tanphatetek bị chặn đăng nhập nên lấy nhận diện từ logo trong source. Kiểm Playwright 1366 + 1440: đầu 64px, không tràn, popup footer luôn thấy (thân cuộn), 0 lỗi JS.
- [ ] AI1b. Còn: `@TPE SMART AGENT` trong chat nhóm (04) — chờ user duyệt màn 33, 34.
- (11/11) **Đã tách thành feature riêng `.plans/agent-chat/agent/` (TPE SMART AGENT): spec + plan 15 task** — theo dõi ở đó; các mục AI2–AI5 dưới đây chuyển sang plan đó.
- [ ] AI2. Chốt trước khi code (hỏi user): model + trần chi phí/tháng · loại dữ liệu KHÔNG đưa vào công cụ · ZDR / khu vực xử lý · nhóm user thử · nơi giữ API key.
- [ ] AI3. BE (song song GĐ1–GĐ2, không phụ thuộc bảng chat): lớp công cụ chỉ đọc bọc service Assign hiện có, chạy với danh tính + công ty của người hỏi; job gọi Claude API (SDK PHP, tool runner); log mỗi lượt. Kiểm bằng lệnh artisan / API thử, chưa có giao diện.
- [ ] AI4. Gắn vào chat khi GĐ3 có bảng tin nhắn + socket: người dùng hệ thống "Trợ lý", hội thoại 1–1 + `@Trợ lý` trong nhóm; công cụ "việc của nhóm" dùng cột không gian của GĐ2.
- [ ] AI5. Chạy bộ 50 câu (chấm chọn đúng công cụ + trả lời đúng), mở cho nhóm user thử ~2 tuần, sửa mô tả theo log.
- Ghi sau thử nghiệm (ngoài đợt này): thao tác GHI qua thẻ đề xuất + nút Xác nhận; mở rộng phân hệ khác.

## GĐ4 — App (TPE_APP)
- [ ] Danh sách không gian của tôi → chat (đọc, gửi, file, @) + push FCM; cập nhật nhiệm vụ/vấn đề được giao; tạo nhanh từ tin nhắn. Giữ U1–U13 của `.plans/app-cong-viec-nhiem-vu-van-de/`.

## GĐ5 — Tin hệ thống + Hợp đồng
- [ ] BE: event nghiệp vụ Task/Issue + listener ghi tin `system`; cấu hình sự kiện theo không gian.
- [ ] Chứng từ GP ↔ TKT báo vào đúng chat (YCP, YCĐC → GP; hồ sơ duyệt, phiên bản → TKT).
- [ ] Không gian tự sinh cho Hợp đồng (khảo sát `Modules/Assign/Entities/Contract/*`, K6).

## GĐ6 — Mở rộng
- [ ] Thẻ đối tượng khác (meeting, phiếu duyệt…), ghim tin, tìm trong chat; Kanban/Gantt nếu cần.

## Trước khi lên prod
- [ ] Xử lý danh sách §10 spec (vấn đề ngoài luồng).
- [ ] Kiểm tiến trình socket trên VPS HRM (`pm2 ls`, `ss -ltnp | grep 889`, `SOCKET_URL` prod).

## Sổ quyết định logic (hỏi user sau — user 04/11: "các quyết định logic lưu lại hỏi tôi sau", không chặn việc mockup)
- [x] L1. Đề nghị gia hạn (người làm gửi ngày mới + lý do → người giao Đồng ý / Từ chối) — **CHỐT 04/11: làm ở GĐ2** (bảng mới + API + thông báo + lịch sử).
- [x] L2. **CHỐT 05/11: (a) tính theo lúc nộp** — nộp kết quả TRƯỚC hạn (`submitted_at` ≤ hạn) thì không tính quá hạn dù chờ duyệt lâu; nộp SAU hạn vẫn tính. Sửa BE `deadline_state_text` + chip/báo cáo quá hạn dùng chung 1 điều kiện (GĐ2). Câu hỏi gốc: "Hoàn thành - Chờ duyệt" đã qua hạn có tính Quá hạn không? BE `deadline_state_text` hiện TÍNH; mockup KHÔNG tính. Phương án: (a) không tính nếu `submitted_at` ≤ hạn (đề xuất) · (b) đã nộp là không tính · (c) giữ BE. User muốn làm rõ trước khi chọn.
- [x] L3. **CHỐT 05/11, SỬA 05/11 tối:** kiểm code thì "cần duyệt triển khai" là do NGƯỜI GIAO chọn (không có luật tự quyết) → form có công tắc "Cần duyệt triển khai" (U31b, `.plans/app-cong-viec-nhiem-vu-van-de/design.md`). Nội dung chốt ban đầu: **theo luồng giao việc hiện có** — tạo từ chat đi đúng luật tạo nhiệm vụ như popup tạo hiện tại (cần duyệt triển khai thì vào Chờ phê duyệt triển khai, không thì Chờ bắt đầu); tin "giao việc" báo khi việc thật sự được giao. Builder kiểm lại trong code điều kiện cần duyệt triển khai ở GĐ2 (mockup đang minh hoạ ca Chờ bắt đầu). Câu hỏi gốc: Tạo nhiệm vụ từ chat (bấm "Tạo nhiệm vụ", không phải Lưu nháp) thì nhiệm vụ vào trạng thái nào: **Chờ bắt đầu** (mockup đang làm) hay **Chờ phê duyệt triển khai** như luồng giao việc hiện có (cần quyền `assign.trien_khai_task.approve` + quản lý phòng ban người làm duyệt)? Ảnh hưởng: tin hệ thống "giao việc" có báo ngay hay đợi duyệt.
- [x] L4. **CHỐT 05/11: Quản lý không gian bật/tắt** (tab Cấu hình); **mặc định giữ như mockup** — bật 7, tắt "Bắt đầu thực hiện" + "Đổi hạn · đề nghị gia hạn". Câu hỏi gốc: Ai bật/tắt được "Tự báo vào nhóm" (mockup ghi: Quản lý phòng / Quản lý dự án) và mặc định 9 sự kiện bật/tắt thế nào (mockup: tắt "Bắt đầu thực hiện" + "Đổi hạn · đề nghị gia hạn", còn lại bật).
- Thêm các câu logic mới phát sinh khi làm mockup vào đây (L3…), hỏi lần lượt bằng AskUserQuestion trước khi viết plan GĐ1.

- [x] (05/11) **Tuỳ chọn tab** (spec §3.12, user chốt: cố định Trao đổi + Nhiệm vụ; tuỳ chọn Tổng quan · Vấn đề · Meeting · File; tắt = chỉ ẩn + không tạo mới; mỗi không gian tự cấu hình, dự án con điền sẵn theo phòng; mở không gian vào Trao đổi; Dự án KH không áp dụng) — vẽ mockup web màn 21 + app. **Đã vẽ:** web màn 21 mục mới "Tab sử dụng" (mục lục trái + 2 dòng Luôn bật + 4 công tắc, số bản ghi đang mở, popup "Tắt tab …?" giải thích chỉ ẩn; tắt là thanh tab trên ẩn ngay — `_build/tabs21.js/.css`, kiểm Playwright 0 lỗi JS); app KG-25 (②.9) không gian chỉ còn Trao đổi · Nhiệm vụ · File. Việc GĐ2 code: cột `enabled_tabs` + lọc ô Không gian ở form tạo + chặn tạo mới ở BE khi tab tắt.

## ▶ 09/11/2026 — ĐỔI LOGIC LỚN: Nhóm trao đổi (đọc trước mục việc chờ bên dưới)
User 09/11 chốt: chỉ còn **Nhóm trao đổi** + **Dự án khách hàng**. Nhóm trao đổi: phẳng, thời hạn tuỳ chọn, bỏ Mở/Kín, mọi nhân viên tạo được, thành viên thêm tay hoặc lấy toàn bộ 1+ phòng ban / bộ phận **1 lần lúc chọn** (không đồng bộ), người lấy vào là Thành viên. Spec đã sửa §3.0–3.5, §3.11, §3.12, §4.1, §5, §7, K2, K4.
- [x] N0. Sửa spec + design.md + plan.md (09/11).
- [x] N1. Builder check (09/11): sửa ~15 câu sót; user chốt nhóm chỉ 1 công ty, Quản lý cuối cùng nghỉ việc ⇒ tự nâng người vào sớm nhất; Claude chốt người xem theo quyền tổ chức không mở màn nhóm, K7 không vào chat (trả về bản gốc).
- [x] N2. (10/11) Sửa mockup web GĐ0 — 28 màn (bỏ 06, 07 → `gd0-mockup/_bo-09-11/`). Popup 11 (không hạn) · 12 (lấy từ phòng ban, soát tick, bỏ trùng) · 13 (có hạn); panel Ctrl K còn Ghim · Nhóm trao đổi · Dự án KH · Lưu trữ; 01 cột "Khách hàng / Thời hạn"; 02/24 ô 5 = Meeting sắp tới + bảng Nhiệm vụ sắp đến hạn; 03/19/20/15 bỏ cột Dự án + bỏ Gom theo Dự án; 05 nút Thêm thành viên + cột Cách thêm; 21 Cấu hình (Tên sửa được, Thời hạn, Công ty chỉ đọc, bỏ dòng dự án con) + mục Đóng nhóm có popup thật (`close21.js`); chat 04/08/29 bỏ Kín; index, present, present-notes, thuyet-minh viết lại. Kiểm Playwright 1440: 28 màn 0 lỗi JS, không tràn ngang; footer popup 12px; luồng radio → 13, Lấy từ phòng ban → 12 → Thêm 16 người → 11; Đóng nhóm Dừng thiếu lý do báo lỗi, đóng → Mở lại. Script dựng lại: scratchpad phiên e33ee83d `g1.py`/`g2.py`/`g3.py` chạy trên bản sao lưu `gd0-backup/` (scratchpad tạm — mất khi phiên hết).
- [x] N2b. (10/11, user chốt phương án 1 — áp cả Dự án KH) Thanh tab mọi không gian: Trao đổi · Nhiệm vụ · Meeting · Vấn đề · Báo cáo (tên cũ Tổng quan) · File · Thêm; bỏ nút Trao đổi riêng bên phải. Mockup 22 màn không gian đã đổi + kịch bản trình chiếu theo thứ tự mới + Tab sử dụng (21); spec §5.1, §3.12. Kiểm Playwright 1366: thứ tự đúng, viên chọn khớp tab, vừa 1 hàng, 0 lỗi JS. Thanh trình chiếu mặc định thu gọn.
- [x] N2c. (10/11, user chọn phương án 1) Chat cá nhân 1–1 — spec §4.6 (Hội thoại: space / direct / group sau; danh sách người trong tab Trao đổi + mục Tin nhắn trên rail; nhắn được mọi NV cùng công ty). Mockup: cột Hội thoại trong tab Trao đổi (04, 08, 29 — `_build/dm.js/.css`), màn 32 (mở sẵn chat 1–1), màn 31 Tin nhắn (mọi hội thoại); mục Tin nhắn trên rail thêm trong `sb2.js` (mọi màn, `?v=3`). Kiểm Playwright 1366: 30 màn có mục Tin nhắn, 0 lỗi JS; mở 1–1, gửi Enter, tìm người ngoài nhóm, quay về nhóm, màn 31 ẩn thanh tab không gian.
- [x] N2d. (10/11) Nhóm trao đổi chỉ cố định tab Trao đổi; Nhiệm vụ · Meeting · Vấn đề · Báo cáo · File bật mới hiện, nhóm mới mặc định tắt (spec §3.12; Dự án KH chưa áp — user sửa sau). Mockup: popup 11/13 thêm "Tab sử dụng", màn 21 Nhiệm vụ thành tuỳ chọn, nhóm có hạn (08/16/17/18) chỉ có Trao đổi · Nhiệm vụ · Meeting. Kiểm Playwright 1366: 0 lỗi JS, viên chọn khớp tab, tắt Nhiệm vụ ở 21 thì tab ẩn.
- [x] N2e. (10/11, user chọn phương án 1) Nhắn riêng với MỌI nhân viên đang làm việc của TẤT CẢ công ty, không cần chung nhóm (spec §4.6). Mockup: nút "Tin nhắn mới" → popup Danh bạ (tìm, lọc Công ty, nhóm theo phòng ban) ở 04/08/29/31/32; ô tìm chia Thành viên nhóm · Cùng công ty · Công ty khác; nhãn công ty cho người khác công ty; màn 05 nút "Nhắn tin" từng thành viên → 31?to=. Kiểm Playwright 1366: 0 lỗi JS.
- [x] N2f. (10/11, user: "tham khảo zalo để làm cho chuẩn") Viết lại chat 1–1 + danh sách hội thoại theo khuôn Zalo PC (spec §4.6 "Khuôn giao diện"): chip lọc, ghim / tắt thông báo / chưa đọc qua ⋯, avatar ghép nhóm, gom tin theo người, trả lời trích dẫn, cảm xúc, ⋯ tin (ghim / sao chép / tạo nhiệm vụ / thu hồi), dải tin ghim, Đã xem, đang soạn tin, cột Thông tin hội thoại. `_build/dm.js/.css`. Kiểm Playwright 1440 + 1366: không tràn ngang, 0 lỗi JS. Chat nhóm (04) chưa đổi khuôn — chờ user.
- [x] N2g. (10/11, user chọn phương án 1) Tab nằm TRONG hội thoại — khung kiểu Teams cho mọi màn không gian (24 màn) + Tin nhắn (31, 32): cột Hội thoại chung bên trái (thu gọn 68px), đầu không gian + tab trong khung phải, topbar chỉ còn tiêu đề. `dm.js` chế độ `__DM_LISTONLY`. Kiểm Playwright 1366 + 1440: 30 màn 0 lỗi JS, không tràn (thanh công cụ xuống dòng, popover Lọc tự thu, tên KPI 2 dòng).
- [x] N2h. (10/11) Tab là con của hội thoại ⇒ 1 hàng gọn 48px (tên · tab gạch chân · thành viên · Phóng to) + chế độ **Phóng to** (ẩn cột hội thoại, tên nhóm lên topbar, nhớ trạng thái). Spec §5.1. Kiểm Playwright 1366: 24 màn hàng cao 48, tab vừa 1 hàng, nội dung bắt đầu y=108; phóng to / thu nhỏ / chip thành viên → tab Thành viên chạy; 0 lỗi JS.
- [x] N2i. (10/11, user chọn hướng A) Bỏ tab Trao đổi — bấm tên nhóm về chat; đầu không gian = khối tên (avatar · tên + chưa đọc · loại / thành viên / liên kết) + nút công cụ icon + chữ + số đếm (Nhiệm vụ · Meeting · Vấn đề · Báo cáo · File · ⋮ · Phóng to). Spec §5.1. Kiểm Playwright 1366 + 1440: 24 màn vừa 1 hàng, đúng mục sáng, tên → chat, ⋮ → Thành viên / Cấu hình, Phóng to (chip topbar bấm về chat); 0 lỗi JS.
- [x] N2j. (10/11 tối) Bỏ Báo cáo (nút, Tab sử dụng 21, popup 11/13; màn 02, 22 → `_bo-09-11/`, mọi link trỏ về Trao đổi) + nút công cụ theo khuôn `V2BaseSegmented` (rãnh xám, viên trắng, icon màu theo loại). Kiểm Playwright 1366 + 1440: 22 màn vừa 1 hàng, 0 lỗi JS.
- [x] N2k. (10/11) Gọn chat (spec §4.4b): cột phải ẩn mặc định, chỉ Ghim · Thành viên; rê tin không đổi nền — nút ⋯ nhỏ, bấm mới hiện thanh thao tác (cả chat 1–1); bớt chữ, giãn khoảng cách. Vá thẳng chatx nhúng ở 04/08/29 + khối `/*cx-tidy 10/11*/`; `dm.js/.css`. Kiểm Playwright 1366: 3 màn chat nhóm + 31 — ẩn cột, ⋯ mở / đóng thanh, thẻ việc mở cột, 0 lỗi JS. 
- [x] N2l. (10/11) Gộp hàng icon khung chat lên đầu không gian (spec §4.4b): chatx nghe click ở `document` + nhận nút trong `.ws-chat-acts`; `dm.js` chuyển `.cx-hd-r` lên, ẩn `.cx-hd`. Kiểm Playwright 1366 + 1440 (04, 08, 29): vừa 1 hàng, cột phải / tìm / thông báo / mô phỏng mở đúng chỗ, ⋯ tin + thẻ việc vẫn chạy, 0 lỗi JS.
- [x] N2m. (10/11) Cột Hội thoại tự thu gọn (68px) khi mở Nhiệm vụ / Meeting / Vấn đề / File / mục ⋮ (spec §5.1); về chat trả lại lựa chọn đã nhớ; mở rộng tạm ở mục công cụ không ghi nhớ. Kiểm Playwright 1366 (03, 04, 08, 10, 15, 19, 20, 21, 27, 29): đúng trạng thái, khung phải 1020 → 1240px, không tràn ngang, 0 lỗi JS.
- [x] N2n. (10/11) Chip lọc nhanh → ô chọn có số + màu (spec §5 "Khung tab danh sách gọn"): `_build/qsel.js` + `qsel.css` chèn vào 20 màn có `.mk-tb-chips`; giữ chip gốc ẩn để bộ lọc cũ vẫn đếm + lọc, ô chọn đọc nhãn/số và bấm hộ chip. Kiểm Playwright 1366 (01, 03, 05, 15, 19, 20, 23, 25): nút 124–130px cao 32, thanh công cụ không tràn, menu đủ mục + màu đúng, chọn mục lọc đúng (03 Quá hạn còn 3 việc), về Tất cả trả lại, 0 lỗi JS.
- [x] N2o. (10/11 khuya) Bỏ ghim lên thanh bên + icon Tin nhắn trên topbar (spec §4.6): `sb2.js` (v=6) gỡ khối Đã ghim ở rail, nút ghim + khối Đã ghim ở panel Không gian, "Ghim & gần đây" → "Gần đây"; chèn icon `fe-message-square` + badge giữa Phóng to và chọn phân hệ (cả 2 bản topbar trong trang). Kiểm Playwright 1366 (01, 03, 04, 21, 29, 31): thứ tự icon đúng, cùng hàng với chuông, bấm → 31, ở 31 có vạch xanh, chế độ Phóng to chip không đè icon, 0 lỗi JS.
- [x] N2q. (10/11 khuya) Danh sách hội thoại thoáng hơn (dòng 66px) + khối "Đã ghim" tách riêng (nền xám nhạt, tiêu đề + số, vạch ngăn; phần dưới "Tất cả hội thoại" / tên bộ lọc) — `dm.js` + `dm.css`, chép lại 24 màn. Kiểm Playwright 1366 (31, 04, 03 thu gọn; lọc Chưa đọc / Nhóm / Cá nhân): đúng tiêu đề + số, không tràn, 0 lỗi JS.
- [x] N2r. (10/11 khuya) Đồng bộ chat 1–1 với chat nhóm (spec §4.6): tiêu đề "Tin nhắn", khung phẳng màn 31/32, thanh ghim vàng + "Người gửi: nội dung", khung soạn tin ô nhập trên / công cụ dưới; nút trình chiếu thu gọn chuyển xuống góc trái (trên thanh bên) để không che nút Gửi (`sb2.js` v=7). Kiểm Playwright 1366 + 1440 (31, 31 có cột Thông tin, 32): khung sát nhau, không tràn / không cuộn trang, gửi tin + bỏ ghim chạy, 0 lỗi JS.
- [x] N2s. (10/11 khuya) Đầu chat 1–1 = đầu nhóm 64px; mở chat nhóm ⇒ xoá số chưa đọc của nhóm đó (đầu nhóm + danh sách + tổng Chưa đọc). Kiểm Playwright 1366 + 1440 (03, 04, 08, 15, 21, 29, 31, 32): cao 64, đầu nhóm 1 hàng không tràn, số đúng, 0 lỗi JS.
- [x] N2t. (10/11 khuya) Nút công cụ nhóm kiểu Apple trong + sáng bóng (spec §5.1): rãnh kính mờ trắng, icon màu trong ô tròn, mục đang mở viên trắng bóng + bóng màu loại. Kiểm Playwright 1366 + 1440 (03, 04, 15, 29): đầu nhóm vẫn 64px 1 hàng, cụm nút 488×40, không tràn, 0 lỗi JS.
- [x] N2u. (10/11 khuya) MINITAB: chuyển động lò xo như V2Base cho cụm nút nhóm (`miniTab()` trong `dm.js`, `.mtab*` trong `dm.css`) — giãn 160ms + lò xo 400ms, hover nở 2px, vào trang trượt tiếp từ mục cũ. Kiểm Playwright 1366: viên chọn khớp mục (lệch < 0.5px), giữa chuyển động phủ Nhiệm vụ → Vấn đề, hover nở ~2px, chữ không transform, đầu nhóm 64px, 0 lỗi JS.
- [ ] N2v. Khi code (cần "làm" riêng): tạo `V2BaseMiniTab` (hrm-client/components) theo spec §5.1 mục MINITAB + bổ sung skill `segmented-control`.
- [x] N2w. (10/11 khuya) Bỏ icon trạng thái đầu dòng (phương án A user chọn): nút ⇄ Đổi trạng thái ở cột thao tác + menu có dòng trạng thái hiện tại ✓; gom theo Người làm / Hạn hiện nhãn trạng thái bấm được. Vá 4 màn danh sách 03, 19, 25, 26 (rowHtml + khối style `/*st-act*/`). Kiểm Playwright 1366 + 1440: không còn nút đầu dòng, cột thao tác không tràn, menu đúng trạng thái được phép, gom Người làm ra nhãn (22/5/6/5 dòng), chọn Tạm dừng mở popup lý do, 0 lỗi JS.
- [ ] N2p. **LÀM SAU** [U 10/11]: Dự án KH (TKT / GP / HĐ) giữ giao diện màn cũ + thêm tab nhóm chat tích hợp — thiết kế riêng; mockup GP/TKT theo khuôn Nhóm trao đổi (09, 10, 14, 23, 25–30) là bản cũ.
- [ ] N3. Sửa app `meeting-mobile.pen` nhóm KG (danh sách không gian, header, tạo nhóm nếu có, đóng/mở lại) theo Nhóm trao đổi.
- [ ] N4. Việc chờ cũ bị ảnh hưởng: B1 (điền sẵn tab theo phòng cha) **BỎ**; A2 điểm "Phòng theo phòng ban tự lưu trữ…" **BỎ**; C1 plan GĐ1 viết theo mô hình mới.

### Checkpoint — 11/11/2026 (wrap up)
- Xong trong phiên 10–11/11: N2m → N2w (thu gọn cột hội thoại, lọc nhanh dạng ô chọn, bỏ ghim lên thanh bên + icon Tin nhắn topbar, khối Đã ghim, đồng bộ chat 1–1, nút công cụ kiểu Apple + MINITAB lò xo, đổi trạng thái bằng nút ⇄) → **CHỐT mockup web Nhóm trao đổi**.
- Chờ user chọn: N3 app Pen · C1 plan GĐ1 · N2p Dự án KH · N2v code `V2BaseMiniTab` (cần "làm").
- Trợ lý AI: 11/11 user chốt thử nghiệm cho phân hệ Công việc, cùng đợt Nhóm trao đổi → mục **GĐ3-AI** (AI0–AI5). Chưa có lệnh code.
- Không đụng source trong phiên.

### ✅ CHỐT 10/11/2026 — mockup web Nhóm trao đổi
User: *"Chốt mockup ở đây cho phần nhóm trao đổi ⇒ Dự án KH sẽ làm sau"*. Bản chốt: màn 01, 03, 04, 05, 08, 11–13, 15–21, 31, 32 + `_build/dm.js`, `dm.css`, `qsel.*`, `sb2.js` (v=7). Dự án KH (09, 10, 14, 23, 25–30) ngoài bản chốt → N2p. Chốt mockup KHÔNG phải lệnh code. Việc kế tiếp (chờ user chọn): N3 cập nhật app Pen theo bản chốt · C1 viết plan GĐ1 · N2p thiết kế Dự án KH.

### Checkpoint — 10/11/2026 (mockup web theo Nhóm trao đổi)
Vừa hoàn thành: N0–N2 — spec + design + plan theo Nhóm trao đổi; builder check (user chốt 1 công ty, Quản lý cuối nghỉ việc tự nâng người vào sớm nhất); mockup web 28 màn sửa xong, kiểm Playwright.
Đang làm dở: —
Bước tiếp theo: (1) user xem mockup web (`gd0-mockup/index.html`, mở qua http.server, màn 11–13, 05, 21, 24); (2) N3 sửa app `meeting-mobile.pen` nhóm KG; (3) C1 plan GĐ1 theo mô hình mới.
Blocked: chưa có lệnh code

## ▶ VIỆC CHỜ LÀM TIẾP (lưu 05/11/2026 — đọc mục này đầu phiên sau)

**A. Chờ user duyệt** (mở `~/Documents/demo giao dien/pencil_design/meeting-mobile.pen`, khu Công việc — mục lục y −1580, 14 nhóm ①…⑭; nhắc user Cmd+S nếu chưa lưu)
- [ ] A1. Duyệt bộ app theo 14 nhóm (KG-01…25, NV2-01…37, VD2-01…16).
- [ ] A2. Duyệt các điểm Claude tự chốt:
  - Tuỳ chọn tab (§3.12): Tổng quan ẩn ô của tab tắt · bật/tắt có tin hệ thống · chỉ cấu hình trên web.
  - Đóng / mở lại (§3.11): sau khi đóng chỉ đọc + Lưu trữ + dải "đã đóng" · Phòng theo phòng ban tự lưu trữ thì dự án con vẫn chạy, Quản lý phòng cũ mất quyền "luôn xem" · dự án quá hạn 7 ngày nhắc hằng tuần · app cũng Đóng / Mở lại được.
  - Xin tham gia: người chỉ xem không thả cảm xúc · 1 yêu cầu chờ / người / dự án · Quản lý duyệt được trên app (KG-21).
  - Nhiệm vụ / Vấn đề app: thêm nút ☰ Bộ lọc nâng cao trên thanh công cụ (tab Nhiệm vụ trong không gian thì không).

**B. Thiết kế còn lại**
- [ ] B1. (tuỳ chọn) Web: popup tạo Dự án nội bộ — phần "Tab sử dụng" điền sẵn theo phòng cha.
- [ ] B2. Web: màn phía Quản lý duyệt "Xin tham gia" (app đã có KG-21).
- [ ] B3. (nếu user cần) Xuất PNG từng nhóm ①…⑭ để đưa vào slide thuyết trình.
- [ ] B4. Sau khi user duyệt: xoá hẳn hoặc giữ khu "Bản cũ" (20 màn NV-/VD- cũ, y 21946).

**C. Tài liệu**
- [ ] C1. Plan chi tiết **GĐ1 — nền không gian** (`.plans/gop-db/phan-he-cong-viec/gd1-nen-khong-gian/plan.md`; folder con chỉ tạo khi bắt đầu).
- [ ] C2. Gom vào plan GĐ2 các việc code đã ghi rải rác:
  - Nhiệm vụ: công tắc Cần duyệt triển khai (BE chỉ nhận Nháp / 2 / 3 / 4) · `start_date` trống thì BE điền ngày giao, FE bỏ `*` + `seedDates()` · bỏ Trọng số KPI ở mockup / spec (đã sửa mockup).
  - Vấn đề: form tạo bỏ ô Trạng thái (tự suy theo người nhận) · API đổi trạng thái nhận `resolution` + `root_cause_group` (`resolution` đang varchar 255 → cân nhắc text).
  - Chat: ghim (Quản lý + Thành viên, ≤ 20, lưu người ghim) · sửa / thu hồi trong 24h kiểm ở BE · người chỉ xem chặn ghi ở BE · bảng yêu cầu tham gia + thông báo.
  - Không gian: cột trạng thái đóng (`status`, `close_result`, `close_reason`, `closed_at`, `closed_by`) + middleware 423 + tự Huỷ / Đã đóng việc dở · `enabled_tabs` + lọc ô Không gian ở form tạo + chặn tạo mới khi tab tắt.

**D. Code — CHỈ khi user nói rõ "làm" (hỏi riêng phạm vi: repo · nhánh · file · migration)**
- [ ] D1. TPE_APP: cập nhật app theo NV2 / VD2 / KG (sau khi A1 duyệt).
- [ ] D2. hrm-api / hrm-client theo plan GĐ1 → GĐ2.

### Checkpoint — 05/11/2026 (wrap up — tuỳ chọn tab)
Vừa hoàn thành: tuỳ chọn tab của không gian (spec §3.12) — cố định Trao đổi + Nhiệm vụ; tuỳ chọn Tổng quan · Vấn đề · Meeting · File; tắt = chỉ ẩn + không tạo mới; mỗi không gian tự cấu hình, dự án con điền sẵn theo phòng; mở không gian vào Trao đổi; Dự án KH không áp dụng. Mockup web màn 21 mục "Tab sử dụng" (`_build/tabs21.js/.css`, kiểm Playwright 0 lỗi JS) + app KG-25 (②.9).
Đang làm dở: — (Pen: user Cmd+S).
Bước tiếp theo: (1) user duyệt app 14 nhóm + tuỳ chọn tab; (2) tuỳ chọn: vẽ phần điền sẵn tab ở popup tạo dự án nội bộ (web); (3) plan chi tiết GĐ1 — nền không gian; (4) hỏi riêng phạm vi rồi mới code.
Blocked: chưa có lệnh code

### Checkpoint — 05/11/2026 (wrap up tối — app + chỉnh mockup web)
Vừa hoàn thành:
- App (`meeting-mobile.pen`): KG-06 chốt phương án A (1 hàng công cụ + Cách xem/Trường hiển thị) áp NV2-01/02/03, VD-01/02; Vấn đề v2 VD2-01…16 (U36 trạng thái tự suy theo người nhận, U37 Báo đã xử lý có Cách xử lý + Nhóm nguyên nhân, U38 cùng khuôn Nhiệm vụ); KG-21 duyệt Xin tham gia; KG-22/23/24 đóng / mở lại; U39 "+ Ngày bắt đầu"; **sắp lại cả khu Công việc thành 14 nhóm thuyết trình** (mục lục y −1580, số bước ①.1…, 20 màn cũ dồn khu "Bản cũ").
- Chốt logic: ghim (Quản lý + Thành viên), người chỉ xem chỉ đọc + Xin tham gia, sửa/thu hồi 24h, đóng/mở lại không gian (spec §3.11: việc dở tự Huỷ / Đã đóng, ai đóng, Phòng theo phòng ban tự lưu trữ, Phòng tự chọn chặn khi còn dự án con, kết quả Hoàn thành / Dừng + lý do), Ngày bắt đầu không bắt buộc (U39).
- Mockup web GĐ0 (`gd0-mockup/_build/td.js`, `chatx.js/.css`, `close.js/.css`, `arch21.js/.css`, `mockup.css` → nhúng lại vào màn 03, 04, 06, 08, 19, 21, 29): bỏ Trọng số KPI; form Nhiệm vụ thiết kế lại theo khuôn app (Không gian, chip ưu tiên, 17:30, + Checklist / Nhiệm vụ con / Tệp bám CreateTaskModal, Thiết lập n/5 giữ Lặp lại, nút Giao & tạo tiếp riêng, công tắc Cần duyệt triển khai, + Ngày bắt đầu); form Vấn đề U36; chat chỉ xem + Xin tham gia + 24h + dự án đã đóng; popup Đóng dự án (màn 06) + Phòng chưa đóng được (màn 21). Kiểm Playwright 1440 từng phần, 0 lỗi JS.
Đang làm dở: — (Pen chưa chắc đã lưu: user Cmd+S).
Bước tiếp theo: (1) user duyệt bộ app theo 14 nhóm (có thể xuất PNG từng nhóm cho slide); (2) plan chi tiết GĐ1 — nền không gian (`gd1-nen-khong-gian/plan.md`, chỉ tài liệu); (3) hỏi riêng phạm vi trước khi code. Việc code đã ghi cho GĐ2: BE tự điền start_date, bỏ `*`/seedDates; form tạo vấn đề bỏ ô Trạng thái; API đổi trạng thái vấn đề nhận resolution + root_cause_group (resolution varchar 255); bảng yêu cầu tham gia; cột trạng thái đóng của không gian + middleware 423; màn web phía Quản lý duyệt Xin tham gia.
Blocked: chưa có lệnh code

### Checkpoint — 05/11/2026 (Nhiệm vụ app v2)
Vừa hoàn thành: thiết kế lại màn Nhiệm vụ trên app theo logic mockup web — U27–U31 (`.plans/app-cong-viec-nhiem-vu-van-de/design.md` mục "Đợt 2"); 13 màn NV2-01…NV2-12 + cập nhật KG-04, KG-06 trong `meeting-mobile.pen`.
Đang làm dở: — (Pen chưa lưu: user Cmd+S).
Góp ý 05/11 đã áp: Bình luận thành màn riêng (3 tab), màu ưu tiên theo BE, hạn mặc định 17:30, NV2-13 Thiết lập (bỏ Trọng số KPI — form thật không có; mockup web + spec §5.1 mục 3 ghi "Trọng số KPI · n/4" cần sửa lại cho khớp).
05/11 tối: bổ sung 24 màn NV2-14…37 (xem theo trạng thái, sheet thao tác/duyệt, báo kết quả, tạo/sửa).
Bước tiếp theo: (1) user duyệt NV2; (2) áp khuôn cho Vấn đề; (3) user chốt rồi mới cập nhật code TPE_APP (hỏi phạm vi); (4) plan GĐ1.
Blocked: chờ user duyệt

### Checkpoint — 05/11/2026 (M8 app)
Vừa hoàn thành: U26 (thanh dưới app: Việc của tôi · Không gian · [+] · Nhiệm vụ · Phê duyệt; Vấn đề vào drawer); M8 dựng 8 màn KG-01…KG-08 trong `meeting-mobile.pen` + cập nhật thanh dưới 8 màn Công việc cũ; C-M1, C-M2 ghi ở mục M8.
Đang làm dở: — (Pen KHÔNG tự lưu — user phải Cmd+S; kiểm `stat -f "%Sm" meeting-mobile.pen`).
Bước tiếp theo: (1) user Cmd+S + duyệt 8 màn app; (2) viết plan chi tiết GĐ1 `gd1-nen-khong-gian/plan.md` → hỏi riêng xin phép code (repo · nhánh · file · migration).
Blocked: chờ user duyệt M8

### Checkpoint — 05/11/2026 (wrap up)
Vừa hoàn thành: chốt mockup GĐ0 (30 màn) + màn thuyết minh logic `gd0-mockup/thuyet-minh.html`; chốt sổ quyết định L2 (quá hạn tính theo lúc nộp), L3 (tạo việc từ chat theo luồng giao việc hiện có), L4 (Quản lý không gian bật/tắt, mặc định như mockup) — ghi vào spec §4.3, §5.1 và thuyết minh mục 12.
Đang làm dở: —
Bước tiếp theo: (1) M8 mockup app trên Pencil (danh sách không gian, chat, tạo nhanh từ tin); (2) viết plan chi tiết GĐ1 `gd1-nen-khong-gian/plan.md` → hỏi riêng xin phép code (repo · nhánh · file · migration).
Ghi chú: spec §5.1 mục 7 "Thêm nhanh đầu danh sách" đã bỏ trên mockup (05/11) — sửa spec khi viết plan GĐ2. Mockup L2/L3 chưa minh hoạ ca nộp sau hạn / ca chờ duyệt triển khai. Server xem mockup: `python3 -m http.server 8770` trong `gd0-mockup/`.
Blocked: —

### Checkpoint — 05/11/2026 (chốt mockup GĐ0)
Vừa hoàn thành: user chốt mockup GĐ0 (30 màn). Đợt 04–05/11: sidebar mới (4 khối, Thiết lập ghim đáy, rail + popover nền navy, topbar bỏ hiệu ứng sáng — `sb2.css`/`sb2.js`, design.md 9d); 6 màn thao tác GP40 (25–30, dựng tự động bằng `_build/build_gp.py`) + GP40 Thành viên đủ 7 người; chat: nền khung tin "nằm sâu", header gọn, ô nhập ghim đáy; header card Tổng quan theo chuẩn section-header; hiệu ứng rê chuột thanh tab (`tabsnav.js`, theo V2BaseTabNavigation); bỏ ô thêm nhanh trên bảng (spec §5.1 mục 7 — cập nhật khi viết plan GĐ2); gom theo Hạn: Hôm nay đầu, Quá hạn cuối; Phòng có 22 nhiệm vụ demo; màn thuyết minh logic.
Đang làm dở: —
Bước tiếp theo: ~~(1) hỏi L2–L4~~ — đã chốt 05/11; (2) M8 mockup app; (3) plan chi tiết GĐ1 → xin phép code.
Blocked: —

### Checkpoint — 04/11/2026 (chat demo)
Vừa hoàn thành: M7b — mockup chat chạy thật ở màn 04 (Phòng) + 08 (Dự án Kín): toàn bộ thao tác user yêu cầu (tag tên, chèn nhiệm vụ/vấn đề, đính kèm, ghim, tạo nhanh, tự báo vào nhóm khi hoàn thành) + trả lời, cảm xúc, sửa, thu hồi, tìm, mô phỏng sự kiện. Quyết định U25 ghi ở index.html. Đã kiểm bằng Playwright (1440 + 1366): @/# chọn bằng phím, validate báo đồng thời, Báo kết quả → tin "báo hoàn thành" → mô phỏng duyệt → "hoàn thành", sự kiện tắt thì không sinh tin, file chọn/gửi, ghim, tìm, thu hồi, nút "tin mới" — 0 lỗi JS.
Đang làm dở: —
Bước tiếp theo: (1) user xem chat demo, góp ý; (2) hỏi lần lượt sổ quyết định L2–L4 (user muốn hỏi sau); (3) áp U19–U24 cho màn 16–18, 10, Giải pháp; (4) M8 app; (5) plan chi tiết GĐ1 → xin phép code.
Ghi chú kỹ thuật: nguồn dựng nay ở scratchpad session 43cb6d96 `mk/` + `cap/` (đã copy từ session cũ, assemble.py trỏ đường mới); bản sao `gd0-mockup/_build/` (có chatx.js, chatx.css). Dựng lại `NOCSS=1 python3 assemble.py`.
Blocked: chờ user

### Checkpoint — 03/11/2026 (khuya, wrap up)
Vừa hoàn thành (mockup GĐ0, quyết định U14–U24b ghi ở index.html + spec §5.1):
- U14 sidebar chuyển nhanh (màn 24, Ctrl K, ghim) · U15–U16 tên + chip không gian trên topbar; Phòng theo phòng ban tên = tên phòng ban (title-case)
- U17 dải 5 ô số liệu Tổng quan · U18 thanh cuộn ngang 2 đầu · bản trình bày khách hàng `present.html` + `present-notes.js` (thuyết minh để trống, user tự viết)
- U19–U19e Nhiệm vụ / Vấn đề: Danh sách nhóm (mặc định) · Bảng; gom theo, ⓘ giải thích nhóm, trường hiển thị cấu hình được
- U20–U21 panel chi tiết thay CreateTaskModal + ImportResultModal (khảo sát: `khao-sat-nhiem-vu.md`): sửa tại chỗ, Thiết lập, nhật ký tiến độ, bấm vào hạn / đề nghị gia hạn, thêm nhanh → Nháp, quyền bám canEdit / canDelete / canImportResult
- U22b thẻ trắng chứa toolbar + nội dung (GIỮ style tab dùng chung, đệm 1 lớp) · U23 Sắp xếp theo từng màn · U24–U24b bộ lọc chạy thật (Tìm kiếm / Làm mới)
- Chỉ màn 3 (Nhiệm vụ) + 19 (Vấn đề) có bộ chức năng U19–U24.
Đang làm dở: chưa áp U19–U24 cho màn 16–18 (Dự án nội bộ), 10 (TKT), Giải pháp; thuyết minh trình bày chờ user.
Bước tiếp theo: (1) áp bộ chức năng cho các màn còn lại; (2) user chốt 2 câu: đề nghị gia hạn có vào phạm vi không · "Hoàn thành - Chờ duyệt" có tính quá hạn không (BE hiện tính); (3) M8 mockup app; (4) plan chi tiết GĐ1 → xin phép code.
Ghi chú kỹ thuật: nguồn dựng ở scratchpad `mk/` (assemble.py, sb.py, lv.js, td.js, flt.js, present.js, mk.css) + bản sao `gd0-mockup/_build/`; dựng lại `NOCSS=1 python3 assemble.py` trong `mk/` rồi copy sang `_build/`.
Blocked: chờ user

### Checkpoint — 03/11/2026 (sidebar)
Vừa hoàn thành: U14 sidebar truy cập nhanh — mockup màn 24 + rail có ở cả 24 màn (mục "Không gian làm việc" mở panel, 4 không gian ghim trên rail, Ctrl K). Kèm sửa khuôn khi nội dung hẹp đi 58px: header không gian 1 hàng (tên dài cắt …), 5 thẻ Tổng quan 1 hàng. Đo 1440/1366: 1 rail, không tràn ngang, thanh công cụ 46px, tiêu đề bảng 189, panel không đè rail.
Bước tiếp theo: user duyệt sidebar → M8 mockup app (Pencil) → plan chi tiết GĐ1 → xin phép code.
Blocked: chờ user

### Checkpoint — 03/11/2026 (tối)
Vừa hoàn thành: user duyệt thanh công cụ gọn, chỉ áp cho feature này; đã áp cho mọi màn danh sách (01, 03, 05, 06, 09, 10, 15) + dựng 19 Phòng·Vấn đề, 20 Phòng·File, 21 Phòng·Cấu hình, 22 GP·Tổng quan, 23 GP·Hạng mục; đổi chữ UI "không gian" → "không gian làm việc". Mockup 23 màn, đo 1440 + 1366 không tràn, thanh công cụ 1 hàng; Lọc/Áp dụng/Xoá lọc chạy. Spec §3.0 (quy ước chữ), §5.1, §5.4.
Bước tiếp theo: user xem mockup → M8 mockup app (Pencil) → plan chi tiết GĐ1 → xin phép code.
Blocked: chờ user

### Checkpoint — 03/11/2026 (chiều)
Vừa hoàn thành: user chốt đặt tên 2 họ (Nhóm làm việc: Phòng làm việc, Dự án nội bộ · Dự án khách hàng: Tiền khả thi, Giải pháp, Hợp đồng) + BỎ Nhóm, gộp vào Dự án nội bộ thuộc phòng. Spec §3.0–3.5, §3.8–3.9, §4, §5.1 + design.md cập nhật; mockup 15 màn đổi tên/dựng lại (06 tab Dự án nội bộ, 07 popup tạo dự án trong phòng, 08 dự án Kín, 13 popup có Thuộc phòng + Mở/Kín, header Dự án KH có khách hàng). Đo 1440 + 1366 không tràn.
Bước tiếp theo: user xem lại → màn còn thiếu → M8 app → plan chi tiết GĐ1.
Blocked: chờ user

### Checkpoint — 03/11/2026 (sáng)
Vừa hoàn thành: đổi thanh tab mọi màn không gian theo góp ý (5 tab cố định + Thêm ▾ + Trao đổi bên phải), thêm màn 14 (menu Thêm TKT) và 15 (Phòng · Meeting); spec §5.1, §3.9, §3.10 cập nhật. Script dựng: _build/retab.py + assemble.py (NOCSS=1 dựng lại không cần Nuxt).
Đang làm dở: M3 còn Vấn đề / File / Cấu hình của Phòng; M5 còn Tổng quan GP, Hạng mục; M8 app.
Bước tiếp theo: user xem lại thanh tab mới → dựng tiếp màn còn thiếu hoặc M8.
Blocked: chờ user

### Checkpoint — 02/11/2026 (cũ)
Vừa hoàn thành: GĐ0 mockup web 10 màn — `gd0-mockup/index.html` (mục lục + iframe), `gd0-mockup/screens/*.html`, `gd0-mockup/mockup.css` (CSS thật của app + font nhúng), script dựng lại ở `gd0-mockup/_build/`. Đo DOM: màn danh sách khớp /assign/tasks (thẻ lọc 68,70 · thẻ danh sách top 184), màn không gian khớp manager GP (header 65, tab top 71, thẻ 12,132,119).
Đang làm dở: M3 còn thiếu tab Vấn đề / File / Cấu hình của Phòng (cùng khuôn tab Nhiệm vụ) — chưa dựng; M5 chỉ dựng tab Thành viên GP; M8 app chưa làm.
Bước tiếp theo: user duyệt mockup → sửa theo góp ý → M8 mockup app (Pencil) → viết plan chi tiết GĐ1.
Blocked: chờ user
