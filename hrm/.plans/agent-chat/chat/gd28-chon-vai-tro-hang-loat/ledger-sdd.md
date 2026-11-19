# SDD ledger — plan: HRM/.plans/agent-chat/chat/gd28-chon-vai-tro-hang-loat/plan.md
Nhánh: api + client `gop_db-chat-vai-tro-hang-loat` (wt-nhom-trao-doi). BASE api ef1b44f1c · client 067de626b (+ GĐ27 chưa commit mang theo).
Ruling: ledger để trong thư mục plan (như GĐ7/11/12) thay cho .superpowers/sdd — plan nằm ngoài repo (symlink .plans) — chỉ khác chỗ lưu.
Pre-flight: T1→T4/T5 hợp đồng `role_groups` khớp (T4 payload()); T2 whole_company → T4 link "Cả công ty"; T3 routes roles / bulk-remove → T6. Không xung đột.
Ruling: không commit theo từng task — CLAUDE.md HRM "không commit khi chưa có yêu cầu" + memory user tự báo commit — chi phí: review cả nhánh bằng diff working tree.
Task 1: Ruling: "Cả công ty" lấy theo `employee_infos.company_id` (hồ sơ) — khớp cách lọc phòng ban theo công ty + popup Tin nhắn mới GĐ8 — sai thì NV làm nhiều công ty (company_employees) không vào.
Task 1: Ruling: `companyEmployeeIds` dùng DB::table thẳng — `pluck` trên `EmployeeProfiles::baseQuery()` (có select alias) trả null (tái hiện bằng test 200≠400).
Task 1: complete (tests: phpunit WorkspaceRoleGroupTest → OK 9/42; Workspace/ → OK 250/2596)
Task 2: complete (gộp chung file test Task 1: test_preview_whole_company_returns_ids_and_names PASS)
Task 3: Ruling: giữ Quản lý — nếu người thao tác không trong lô thì giữ Quản lý vào sớm nhất trong lô (thực tế không xảy ra vì người thao tác là Quản lý ngoài lô) — vô hại.
Task 3: Ruling: đếm việc dở cả lô bằng 1 truy vấn groupBy thay vì openTasksOf từng người — cùng điều kiện status; message giữ đúng câu cũ.
Task 3: complete (tests: phpunit WorkspaceMemberBulkTest → OK 8/61; Workspace/ → xem dòng dưới)
Task 4: Ruling: link "Phòng ban · Cả công ty" dùng V2BaseButton quaternary xs (nút chung) thay link teal tự vẽ ở mockup — CLAUDE.md cấm button thô + không đổi style chung — chi phí: chữ đậm xám thay teal.
Task 4: Ruling: chưa gom chip người thành "+n người" — select2 không hỗ trợ, tự viết = đụng component chung — chi phí: dòng Quản lý 20 người cao ~4 hàng chip.
Task 4: Ruling: chip người tạo vẫn có × của select2; bấm × thì watcher gắn lại ngay — tránh sửa V2BaseSelectInModal dùng chung.
Task 4: Ruling: tooltip vai trò dùng cùng cấu hình v-b-tooltip của V2BaseFieldHint (customClass v2-field-hint-tooltip) — khớp ⓘ chuẩn của V2BaseLabel.
Task 4: Ruling: "Cả công ty" mà 0 người mới ⇒ toast info, không thêm thẻ rỗng (phát hiện khi kiểm Playwright popup Thêm thành viên).
Task 6: Ruling: menu "Đổi vai trò ▾" dựng lại bằng class toàn cục `v2-row-actions__menu/__item` (không có dropdown nút chữ dùng chung) — cùng kiểu menu ⋮ của bảng.
Task 4–6: kiểm Playwright :3080 (đo DOM): 3 dòng cùng x ô chọn, viền kép 1px⇒0 (rule chung `div.v2-select…:not()` !important ⇒ tăng đặc hiệu), không tràn ngang, footer/thanh hàng loạt cách nút 12px, nhóm thật 408 người ⇒ DB 1/26/381 + 1 tin "đã thêm 407 người"; đổi 6 người ⇒ 6/6; tự hạ khi là Quản lý duy nhất ⇒ khối lỗi "Nhóm phải còn ít nhất 1 Quản lý". Push local tắt (CHAT_PUSH_ENABLED=false), notifications 0.
Task 4: complete · Task 5: complete · Task 6: complete (kiểm bằng Playwright như dòng trên)
Task 7: e2e workspace-role-groups.spec.ts G1–G5 → 5 passed (47.2s).
Task 7: complete (workspace-role-groups 5/5 → sau sửa review 6/6; workspace-tasks 12 · chat-members-paging 3 · chat-drawer 10 · chat-task-status 3 xanh)
Task 7: Ruling: workspace-kh-project K1 đỏ (tải lại màn manager ⇒ API :8080 4 worker kẹt bởi 4 request vừa huỷ, trang đứng khung tải) — chạy lại với client GỐC (gỡ tạm patch GĐ27+28) vẫn đỏ đúng chỗ ⇒ không do GĐ28; ghi ngoài luồng — chi phí: K2–K7 "did not run", chưa kiểm lại nhóm KH bằng e2e (đã kiểm tay: tạo nhóm KH qua nút + tải lại OK).
Final review: subagent (opus) — 0 Critical.
Final: fixed Important "giữ nhầm người thao tác không phải Quản lý ⇒ nhóm 0 Quản lý" — test_keeps_a_losing_manager_when_actor_is_not_a_manager RED→GREEN, Workspace 259/259.
Final: fixed Important "Cả công ty lấy công ty đang chọn thay vì công ty của dự án KH (mở từ màn manager)" — kh-group trả company_id khi can_create (WorkspaceKhSourceTest three_states RED→GREEN), preset + CreateWorkspaceModal.companyId dùng nó.
Final: fixed (re-grade Minor→Important: mất người im lặng) "picker bỏ người đang ở dòng cao hơn khỏi thẻ phòng" — e2e G6 GREEN; RED chỉ chứng minh bằng đọc code cũ (existing=true ⇒ không vào employee_ids), không chạy RED trên UI.
Final: fixed (kèm) docblock openTasksOf đặt lệch.
Final: minor (deferred): add()/syncSpaceMembers vẫn insert từng dòng (3.000 người ≈ 6.000 INSERT/transaction) — chưa đo.
Final: minor (deferred): đếm Quản lý còn lại không khoá — 2 Quản lý hạ chéo cùng lúc (lỗi có sẵn ở assertNotLastManager).
Final: minor (deferred): 2 action lô không try/catch như update/destroy ⇒ lỗi lạ ra 500 thô.
Final: minor (deferred): lọc phòng ban ở tab Thành viên gộp theo TÊN (2 công ty trùng tên phòng gộp 1).
Final: minor (deferred): menu "Đổi vai trò ▾" không tự đóng khi bấm ra ngoài.
Final: Ruling: route /preview-departments (không gắn nhóm) cho mọi user truyền company_id bất kỳ, whole_company ra toàn bộ NV công ty — luồng phòng ban cũ đã mở như vậy — chi phí: lộ danh sách tên NV công ty khác (cùng mức hiện tại).
Final: Ruling: trần member_ids API lô 3.000 (spec §5.2 ghi 2.000, §8 nâng 3.000) — giữ 3.000 cho khớp trần thêm theo vai trò.
