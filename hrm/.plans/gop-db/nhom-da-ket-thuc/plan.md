# Nhóm "Đã kết thúc" — Việc của tôi (app + web) — plan

> Design: `.plans/my-todo/design.md` "Chốt 07/11 (user "làm"): nhóm Đã kết thúc". ⛔ Chưa có lệnh code. Không commit.

## Chốt 08/11 (user)
- Làm cả app (`my_todo_list_view.dart`) và web (`TodoMainList.vue`) — web đang dính cùng lỗi (lọc "Đã xong"/"Tất cả" → việc xong hạn cũ rơi vào Quá hạn).
- Nhắc việc cá nhân đã xong cũng cắt 30 ngày (theo `completed_at`) cho khớp tiêu đề "30 ngày gần nhất" — DB local: 49/79 việc xong cũ hơn 30 ngày sẽ không còn hiện ở danh sách (vẫn xem được ở màn Loại nhắc việc web).

## Luật
- Việc có `status_group` ∈ {done, stopped} (nhắc việc cá nhân: đã tick xong) → nhóm "Đã kết thúc · 30 ngày gần nhất", đứng CUỐI (sau Quá hạn); không chia theo hạn, không tính trễ, thẻ xám.
- Nhóm chỉ hiện khi bộ lọc trạng thái có chọn Hoàn thành / Dừng-Huỷ (web: "Đã xong" / "Tất cả"); mặc định thu gọn; nếu CHỈ lọc trạng thái kết thúc thì tự mở.
- Trong nhóm vẫn xếp theo ⇅ đang chọn.

## Task
- BE: `getPersonalTodosNormalized` — nhánh done/all từ getAll chỉ lấy việc xong có `completed_at` ≥ 30 ngày (TimesheetWorkItems::PENDING_LOOKBACK_DAYS). Test.
- Web: TodoMainList (nhóm mới + luật mở/thu), TodoGroupHeader (nhãn/icon/màu), TodoItem thẻ xám ở nhóm này. Playwright.
- App: `_group()` + `_groups` + mở mặc định + thẻ xám; test widget; máy ảo.
- Ô tick nhắc việc cá nhân trong nhóm: GIỮ (bỏ tick = mở lại), ẩn mọi nút khác (user chốt 08/11).

## Tiến độ — 08/11/2026 (user "Làm")
- [x] BE: `getPersonalTodosNormalized` — việc xong chỉ lấy `completed_at` ≥ 30 ngày (nhánh done + all). Test `Feature/MyTodo/PersonalDoneLookbackTest` 4/4 (cả đường web status=done/all và app status_groups).
- [x] Web: TodoMainList nhóm `closed` cuối (luật mở/thu suy từ dữ liệu: chỉ toàn việc kết thúc → mở; không cần sửa index.vue), `isClosedItem` (status_group done/stopped hoặc personal Hoàn thành); TodoGroupHeader nhãn + màu xám; TodoItem `closed` (nền #f8fafc, chữ #94a3b8, ẩn item-actions, giữ ô tick, ngày không đỏ). Lỗi tự bắt khi Playwright: prop `closed` gắn nhầm nhánh danh sách phẳng — đã sửa. Playwright MCP đạt. Spec mới `my-todo-closed-group.spec.ts` (3 ca) — chưa chạy.
- ⚠️ NGOÀI PHẠM VI, chưa sửa: web chọn "Tất cả" KHÔNG gửi `status` (index.vue:311 bỏ qua chuỗi rỗng) ⇒ BE hiểu là "Chưa xong" ⇒ "Tất cả" chỉ hiện việc chưa xong (đã đo: URL `assign/my-todo?month=…`). Sửa = gửi `status=all` (index.vue) — cần user cho phép.
- [x] App (subagent + Claude kiểm máy ảo): `my_todo_list_view.dart` nhóm `closed` cuối (hiện khi lọc có Hoàn thành/Dừng-Huỷ; chỉ trạng thái kết thúc → tự mở, đổi lọc áp lại), header nhóm `Flexible` cắt "…"; `work_item_card.dart` tham số `closed` (xám, không trễ/quá hạn, ẩn Xác nhận tham gia, giữ ô tick; tick từng BƯỚC trong nhóm bị tắt — chỉ xem). Test mới `my_todo_closed_group_test.dart` 7 ca; my_todo + leader_schedule 126/126; analyze 173. Máy ảo iPhone 18 Pro: lọc Hoàn thành → Quá hạn 0, nhóm Đã kết thúc 1 (tự mở, cuối), thẻ xám có ✓, "Hạn 03/11" không đỏ. Đã xoá todo thử 719/720.
- [x] (user "Làm" 08/11) Web "Tất cả" gửi `status=all` (index.vue loadData); nút làm mới bộ lọc về "Chưa xong" (trước đặt '' = "Tất cả" nhưng vì lỗi cũ nên thực tế ra Chưa xong — giữ hành vi người dùng đang thấy). BE `status=all` đã đúng cả 3 nguồn (task…/personal ≤30 ngày/TimesheetWorkItems). Playwright: mở màn status=pending; Tất cả → status=all, có nhóm closed thu gọn + việc chưa xong; làm mới → pending. Thêm ca e2e "Tất cả" vào my-todo-closed-group.spec.ts (chưa chạy).
- [x] (08/11) E2E bắt LỖI CỦA ĐỢT NÀY: `isClosedItem` web xét cả `status_text === 'Hoàn thành'` → tick tại chỗ (tickTaiCho đổi status_text, không đổi status_group) làm việc vừa tick nhảy ngay sang nhóm Đã kết thúc (thu gọn), phá luồng "tick xong ở yên rồi mờ dần" (my-todo-toggle-smooth ca :107 đỏ). Sửa: chỉ theo `status_group` server (personal xong cũng là done). Sau sửa toggle-smooth 4/4 + closed-group 4/4. App không dính (app tải lại từ server, không đổi tại chỗ).

### Checkpoint — 08/11/2026 (wrap up)
Vừa hoàn thành: code + kiểm (Playwright web, máy ảo app, e2e my-todo) → ĐÃ COMMIT + PUSH 08/11: hrm-api gop_db `cc12bd91d`, hrm-client gop_db `2a4b888ff`, TPE_APP develop `73b82b4` (rebase lên 14 commit develop: gộp thẻ meeting "Đã báo vắng" + `!closed`; giữ TodoListPickerSheet thay showAppPickSheet; sinh lại notification.freezed).
Đang làm dở: —
Bước tiếp theo: deploy — migration 2026_11_08_000001/2 + 2026_11_09_000001/2/3, `~/build_tpe.sh` (catalog-sync đổi tên 2 quyền LCT), thêm key ẩn menu mới ở Cài đặt phân hệ nếu chưa bàn giao; build app mới. Còn treo nhẹ: kiểm máy thật (Gọi / Lưu danh bạ máy / Android) cho Danh bạ.
Blocked:
