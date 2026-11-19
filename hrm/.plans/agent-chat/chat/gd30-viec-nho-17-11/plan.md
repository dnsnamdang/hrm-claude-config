# GĐ30 — Việc nhỏ 17/11/2026: Agent so_luong · bộ đếm 5,000 ký tự · 5 minor GĐ28

User 17/11: "làm 4 7 + 5 minor" (mục 5 gán vai trò Agent, mục 6 YC hỗ trợ, e2e K1: KHÔNG xử lý nữa).
Nhánh: api `gop_db-chat-agent-viec-nho` (từ origin/gop_db a33a6963e) · client `gop_db-fix-toast-lap` (gồm GĐ29 toast lặp). CHƯA commit. Không migration.

## Mục 4 — Agent hiểu số lượng ("1 dự án mới nhất", "top 5")
- [x] `Modules/Agent/Support/ListLimit` (schema + of: 1..trần, mặc định trần / riêng).
- [x] 18 công cụ có `so_luong`: du_an_tkt, giai_phap, van_de, phieu_giao_viec, phieu_cong_tac, lich_meeting, meeting_cua_phong (MeetingListRows::build $limit),
      don_cua_toi, don_cua_phong, don_cho_toi_duyet, gia_han_du_an_tkt, phieu_dat_phong_cua_toi, phieu_dat_phong_cho_toi_duyet,
      4 công cụ việc (TaskQuery::fetch $limit), xep_hang_hoan_thanh (mặc định 5, trần 20). Vẫn báo tổng.
- [x] Luật prompt 14 (AgentPrompt).
- [x] PHPUnit ListLimitToolsTest 3/3; Agent 282/285 (3 lỗi phòng họp có sẵn — DB local thiếu migration sort_order).
- [x] Haiku thật (wt-nhom-trao-doi :8080): 4 câu có số ⇒ so_luong đúng (1·3·3·5), câu không số ⇒ không truyền; ~250₫.
- Chưa làm: bao_gia, ket_qua_du_an_tkt (danh sách gom nhóm) — chưa gắn so_luong.

## Mục 7 — Bộ đếm ký tự ô soạn chat
- [x] `ChatComposer`: >4,500 ký tự hiện "4,600 / 5,000" (xám, dòng gợi ý, canh phải); >5,000 đỏ + khoá Gửi. Đếm theo code point (emoji = 1, như mb_strlen BE).
- [x] Playwright đo: 4,400 ẩn · 4,600 xám · 5,001 đỏ + khoá · 5,000 gửi được.

## 5 minor GĐ28 (review)
- [x] add() + syncSpaceMembers ghi theo lô 500 (tự điền created_by/updated_by): tạo nhóm 650 người 0.57s ⇒ 0.15s (đo trong transaction rollback).
- [x] Khoá các dòng Quản lý trước khi đếm (runBulk + assertNotLastManager chuyển vào transaction ở changeRole/remove).
- [x] 2 action lô có try/catch (ValidationException ⇒ 422, lỗi khác ⇒ 400 + log).
- [x] Lọc phòng ban tab Thành viên theo id (`p:<part_id>` / `d:<department_id>`, API thành viên trả thêm department_id/part_id; tên công ty khác ghi kèm).
- [x] Menu "Đổi vai trò ▾" đóng khi bấm ra ngoài.
- [x] Workspace PHPUnit 259/259.

## E2E
- workspace-role-groups 6/6 (G3 lọc theo khoá id) · chat-core 8/8 (ca "Lấy từ phòng ban" sửa theo giao diện GĐ28 — trước đó ĐỎ, sót khi kiểm GĐ28) · chat-giao-dien 5 · chat-bo-sung 6 · chat-drawer 10 (N7 có 1 lần đỏ chập chờn, chạy lại xanh).

## Deploy
- [x] 17/11 commit api `e1af12bd7` (Agent so_luong) + `53c72b441` (minor GĐ28) · client `9ed6c1557` (GĐ29) + `ab3fbfab8` (bộ đếm) + `848e8d4eb` (minor GĐ28) ⇒ origin/gop_db (ff) ⇒ ĐÃ DEPLOY TPE: build_tpe EXIT 0, Nothing to migrate, prod api 53c72b441 · client 848e8d4eb, site 200.
