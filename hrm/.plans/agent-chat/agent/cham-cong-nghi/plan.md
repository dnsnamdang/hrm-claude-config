# Agent — thống kê người xin nghỉ (`thong_ke_nghi`)

Spec: `docs/superpowers/specs/agent-chat/2026-11-18-agent-thong-ke-nghi-design.md` · repo hrm-api (không FE, không migration)
· nhánh `gop_db-agent-thong-ke-nghi` (từ origin/gop_db b2b2b7add, worktree wt-tpe-agent) — CHƯA commit.

- [x] `Modules/Agent/Tools/ThongKeNghiTool.php` — đếm người khác nhau / đơn / ngày (đơn đã duyệt, giao kỳ theo ngày nghỉ),
      nhom_theo loai·phong·nhan_vien·thang, danh sách nhân sự nhóm phòng (market_tree, A→Z theo tên), 1 NV ⇒ requests,
      vắng không lý do (quyền bảng công), khớp loai_nghi (cụm tên → từ khoá nhóm), loại trùng tên gộp 1 dòng
- [x] Đăng ký AgentToolRegistry · luật 18 AgentPrompt · mô tả don_cua_phong tách ranh giới
- [x] `Tests/Feature/Tools/ThongKeNghiTest.php` 11 ca xanh · 6 câu eval questions.json
- [x] Đối chiếu dữ liệu thật local tháng 10/2026 (NV 13): 253 đơn · 171 người = đếm thẳng DB; phòng dẫn đầu 48 người khớp; cả năm 1,5s
- [ ] Thẻ danh sách: dòng phụ (loại nghỉ + ngày nghỉ) BE đã gửi `sub` nhưng AgentMarketTree chưa vẽ — cần 1 sửa nhỏ hrm-client (chờ user)
- [ ] Hỏi thật qua Agent (script hoi_*.php) · commit · merge gop_db · deploy TPE (chờ user)

## Đi muộn / về sớm — mở rộng `thong_ke_cham_cong` (18/11, user chọn hướng 1)

Vấn đề trước khi sửa (đo dữ liệu thật 10/2026): tool chỉ đếm LẦN; "bao nhiêu người" phải suy từ số dòng; danh sách cắt 20
không báo; nhóm phòng có `employees` = TỔNG NV phòng (Dự án trọng điểm 61) ⇒ model dễ nói "61 người đi muộn"; mặc định chỉ
phòng của người hỏi.

- [x] `pham_vi` thêm `duoc_xem` = mặc định khi không nêu phòng/người: scope ≥ 3 cả công ty; scope 2 phòng + bộ phận quản lý; scope 1 bộ phận quản lý (khớp TimesheetGuard::checkAccess)
- [x] `tra_loi` {chi_so, so_nguoi (người có chỉ số > 0), tong, don_vi, so_phut cho đi muộn/về sớm}
- [x] nhóm phòng/tháng: `employees` ⇒ `employees_total` + `employees_with_metric`; `xep_theo=so_nguoi`; `dan_dau` (đồng hạng); ghi_chu "Còn N dòng chưa hiện"
- [x] `hien_thi=danh_sach`: thẻ market_tree theo phòng (nhiều người trước), tên A → Z (ThongKeNghiTool::nameKey), cột Người · Lần · Phút, `so_luong` ≤ 100, link Bảng chấm công chi tiết
- [x] AgentPrompt quy tắc 19 · eval +5 câu · `ThongKeChamCongDiMuonTest` 6 ca · cả bộ Agent 412/412 xanh
- [x] Dữ liệu thật 10/2026: NV 13 ⇒ 62 người · 149 lần · 2.097 phút; phòng nhiều người nhất Dự án trọng điểm (9/61 NV); NV 157 ⇒ 5 người phòng 52
- [x] Hỏi thật qua Agent 18/11 (8 câu + 3 câu danh sách, haiku): đúng tool + đúng số; câu danh sách chấm công từng chép tên người ⇒ bỏ tên khỏi data.danh_sach (chỉ còn trong thẻ) + note "trả lời 1 câu"; quy tắc 18/19 siết "CHỈ 1 câu, không kể tên phòng / người"
- [x] hrm-client nhánh `gop_db-agent-thong-ke-nghi` (tách tại 883eaed3c): AgentMarketTree hiện `sub` BE gửi + tooltip, dòng phụ tối đa 2 dòng; BE thống kê nghỉ đưa ngày nghỉ lên đầu dòng phụ, cả danh sách 1 loại thì bỏ tên loại. Kiểm Playwright :3070 (đo DOM: không dòng nào bị cắt, chặn 2 dòng 33px, không cuộn ngang)
- [x] 18/11 ĐÃ merge + push gop_db (api 9600a92f0 · client b86b18b95), commit tính năng api 73ac0da2a · client 01420aae6
- [ ] deploy TPE — chờ user
