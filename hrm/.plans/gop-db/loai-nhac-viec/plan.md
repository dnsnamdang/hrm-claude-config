# "Loại nhắc việc" thay cho "Danh sách" (web + app) — plan

> Design: `.plans/my-todo/design.md` mục "Chốt 07/11 — Loại nhắc việc". Mockup app MT-05/06/07 (`meeting-mobile.pen`).
> ⛔ Chưa có lệnh code. Không commit.

## Hiện trạng (rà 08/11/2026, DB local db_gop_6_11)
- `personal_todo_lists`: 365 dòng / 349 user; **349 dòng tên `Mac dinh`** (đúng 1/user, không ai có 2); 16 loại tự tạo
  (Phần mềm ×2, Báo giá, …); **0** dòng trùng tên "Việc cá nhân"/"Việc công ty". 187 nhắc việc.
- Loại gắn theo USER (không lọc theo công ty — `getLists` chỉ `where user_id`), cột `company_id` chỉ ghi lại.
- `getOrCreateDefaultList` lấy `first()` / tạo `Mac dinh` (MyTodoService:40), gọi ở `listLists`.
- `storeList`/`updateList` không chặn trùng tên; `destroyList` xoá luôn nhắc việc trong loại.

## Migration (2 file, hrm-api, chạy lẻ --path vào db_gop_6_11 khi được phép)
1. `2026_11_09_000002_add_system_key_to_personal_todo_lists` — thêm `system_key` varchar(20) NULL (personal|company)
   + unique (`user_id`,`system_key`). Không đụng dữ liệu.
2. `2026_11_09_000003_seed_default_personal_todo_lists` — UPDATE 349 dòng `Mac dinh` → name "Việc cá nhân",
   system_key personal; INSERT 349 dòng "Việc công ty" system_key company (copy user_id, company_id từ dòng personal).
   down(): xoá dòng company RỖNG nhắc việc, đổi personal về `Mac dinh`.

## Task
- BE: `ensureDefaultLists($userId)` (đủ 2 loại, thay getOrCreateDefaultList); `getLists` xếp personal → company →
  tự tạo theo sort_order; resource thêm `is_default`; trùng tên (theo user, kể cả 2 loại mặc định) → 422;
  sửa/xoá loại mặc định → 423; reorder bỏ qua loại mặc định. Test feature.
- Web: TodoFormModal nhãn "Loại nhắc việc" + chọn sẵn Việc cá nhân + thêm nhanh; TodoCalendarSidebar "LOẠI NHẮC VIỆC",
  "Tạo loại nhắc việc mới", loại mặc định có nhãn "Mặc định", ẩn Sửa/Xoá, không kéo được; TodoListFormModal tiêu đề.
  Playwright MCP.
- App: form nhãn + sheet chọn MT-06 (2 mặc định đầu, nhãn "Mặc định") + thêm nhanh MT-07 (dòng cuối sheet → ô nhập +
  Thêm, xong tự chọn); chọn sẵn Việc cá nhân. Test + máy ảo.

## Tiến độ — 08/11/2026 (user "Làm"; web thêm nhanh theo skill: nút cạnh nhãn)
- [x] Migration `2026_11_09_000002` + `000003` ĐÃ CHẠY lẻ --path vào db_gop_6_11: 349 "Việc cá nhân" (đổi từ Mac dinh) + 349 "Việc công ty"; 16 loại tự tạo + 187 nhắc việc giữ nguyên; 714 dòng.
- [x] BE: `ensureDefaultLists` (thay getOrCreateDefaultList), getLists xếp personal → company → tự tạo; resource `is_default`/`system_key`; tên trùng theo user → 422 (unique, collation utf8mb4_unicode_ci ⇒ KHÔNG phân biệt hoa thường VÀ dấu: "viec cong ty" trùng "Việc công ty"); sửa loại mặc định 423 chặn ở `prepareForValidation` (trước validate) + service; xoá 423; reorder bỏ qua loại mặc định. Test `Feature/MyTodo/PersonalTodoListTypeTest` 5/5; LeaderSchedule 54/54.
- [x] Web: TodoFormModal (nhãn, chọn sẵn Việc cá nhân, V2BaseQuickAddButton "Thêm nhanh loại nhắc việc" → ô + Thêm/Huỷ 12px, lỗi dưới ô); sidebar "LOẠI NHẮC VIỆC" (2 loại mặc định khoá + "Mặc định", không kéo); TodoListDetail ẩn Sửa/Xóa loại mặc định; TodoListFormModal tiêu đề + lỗi trùng dưới ô. ⚠️ BE trả `errors.name` dạng CHUỖI → `[0]` ra 1 ký tự "Đ" (bắt được khi Playwright, đã sửa). Playwright MCP namdangit 1440 đạt hết. E2E: sửa 3 spec chữ cũ + spec mới `my-todo-loai-nhac-viec.spec.ts` (4 ca) — CHƯA CHẠY (chờ user yêu cầu).
- [x] App (subagent + Claude kiểm máy ảo): `TodoListOption.isDefault/systemKey`, `todo_list_picker_sheet.dart` (mới), form chọn sẵn Việc cá nhân, thêm nhanh cuối sheet. Test my_todo + leader_schedule 119/119, analyze 173. Máy ảo: nhãn "Loại nhắc việc", chọn sẵn Việc cá nhân, sheet 2 loại "Mặc định" + ✓, 422 thật "Đã tồn tại trên hệ thống" dưới ô (gõ lại thì ẩn), thêm mới → tự chọn. Đã xoá loại thử.
- Ghi chú app: ô thêm nhanh không có nút Huỷ riêng (đóng sheet để bỏ) — khác web (có Huỷ).

### Checkpoint — 08/11/2026 (wrap up)
Vừa hoàn thành: code + kiểm (Playwright web, máy ảo app, e2e my-todo) → ĐÃ COMMIT + PUSH 08/11: hrm-api gop_db `cc12bd91d`, hrm-client gop_db `2a4b888ff`, TPE_APP develop `73b82b4` (rebase lên 14 commit develop: gộp thẻ meeting "Đã báo vắng" + `!closed`; giữ TodoListPickerSheet thay showAppPickSheet; sinh lại notification.freezed).
Đang làm dở: —
Bước tiếp theo: deploy — migration 2026_11_08_000001/2 + 2026_11_09_000001/2/3, `~/build_tpe.sh` (catalog-sync đổi tên 2 quyền LCT), thêm key ẩn menu mới ở Cài đặt phân hệ nếu chưa bàn giao; build app mới. Còn treo nhẹ: kiểm máy thật (Gọi / Lưu danh bạ máy / Android) cho Danh bạ.
Blocked:
