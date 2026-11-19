# Agent — chỉ số Dự án TKT & Giải pháp (17/11/2026, đang brainstorm, CHƯA code)

## Yêu cầu user (17/11)
- Dự án: mỗi phòng KD có bao nhiêu dự án — tổng, theo thời gian, theo NV, theo trạng thái, theo lĩnh vực KD, nhóm ngành, nhóm giải pháp, ứng dụng.
- Giải pháp: phòng nào làm GP, tiến trình GP, mỗi NV đang tham gia bao nhiêu GP.
- Kèm thống kê xếp hạng: phòng nào nhiều nhất, NV nào nhiều nhất…

## Hiện trạng (rà 17/11, subagent + tự kiểm)
- `thong_ke_du_an_tkt`: nhom_theo tien_trinh/phong/nvkd/linh_vuc/nhom_nganh/giai_doan/ly_do_dong; query riêng, quyền DANH SÁCH TKT (`presale.danh_sach_du_an_tien_kha_thi.view`). THIẾU: theo tháng, nhóm giải pháp (industry_id), ứng dụng (application_id), lĩnh vực KD KHÁCH HÀNG, phòng × chiều khác.
- `linh_vuc` của tool = lĩnh vực CÔNG TY kinh doanh (scope_id→hrm_scopes→internal_business_scopes). Báo cáo "Vòng đời dự án TKT" (`ProspectiveProjectsReportService`, quyền `presale.bao_cao_tong_hop_du_an_tkt.view`) từ #10818 dùng Loại hình hoạt động (customer_scope_group_id) / Lĩnh vực KD KHÁCH HÀNG (customer_scope_id) / Ứng dụng — đã kiểm code dòng 710-715.
- `thong_ke_giai_phap`: giai_phap nhom_theo phong/pm/thanh_vien/trang_thai/nhom_nganh/nhom_giai_phap/thang/giai_phap; query riêng. thanh_vien = solution_members ACTIVE. DB local: 43 GP có PM, chỉ 4 PM nằm trong solution_members ⇒ đếm "NV tham gia" đang bỏ sót PM (và leader hạng mục).
- Báo cáo GP: Tổng hợp GP theo phòng ban (`presale.bao_cao_tong_hop_gp.view`, gán 1 kỹ sư chính), Hiệu suất theo GP, Version GP, Yêu cầu GP theo phòng KD. Không báo cáo nào có "NV → số GP".

## Đã chốt
1. (17/11) Lĩnh vực KD: giữ CẢ 2 nghĩa — lĩnh vực KD khách hàng (+ Loại hình hoạt động, như báo cáo Vòng đời TKT) và lĩnh vực công ty KD (cha nhóm ngành); Agent chọn theo cách hỏi, câu trả lời ghi rõ nghĩa nào.

## Báo cáo "Kết quả thực hiện dự án TKT" (/assign/report/prospective-project-results) — đọc 17/11
- Service `ProspectiveProjectResultReportService` (quyền `presale.bao_cao_ket_qua_du_an_tkt.view`, phạm vi 2/3/4; không quyền ⇒ dự án mình phụ trách/tạo).
- Tập dự án của kỳ: lập trong kỳ (TH2) + lập trước kỳ mà đầu kỳ chưa đóng (TH1); bỏ nháp theo trạng thái CUỐI KỲ (đọc log, không đọc cột status); bỏ dự án cha.
- Kỳ: tháng này/trước, quý này/trước, năm nay/trước, tuỳ chọn.
- Tiêu chí theo dõi (cây): dept = Phòng ▸ Bộ phận ▸ NV chủ trì ▸ Thị trường; market = Thị trường ▸ Phòng ▸ Bộ phận ▸ NV; scope = Lĩnh vực Công ty KD ▸ Nhóm ngành ▸ Phòng.
- Cột: Tổng · Đang triển khai · Đóng trong kỳ · Thành công · Thất bại · Tỷ lệ thành công (won/(won+lost)) · Giá trị HĐ (luôn trống, chưa có nguồn) · Giá trị đầu tư dự kiến (estimated_budget).
- Dải tổng hợp: Dự án trong kỳ (tổng / lập trước kỳ / lập trong kỳ) + Kết quả (thành công / thất bại / vẫn triển khai), mỗi ô kèm tiền; meta số KH distinct.
- Lọc: phòng, bộ phận, NV chủ trì, thị trường, KH, tiến trình, kết quả, lĩnh vực, nhóm ngành. Popup drill danh sách dự án theo ô.
- Agent hiện: `ket_qua_du_an_tkt` dùng đúng service này nhưng PHẲNG (toi/nguoi/phong/cong_ty, kỳ) — thiếu tiêu chí/cây, lọc, drill.
2. (17/11) Dự án TKT bám báo cáo "Kết quả thực hiện dự án TKT"; phương án 1: nâng cấp `ket_qua_du_an_tkt` (tiêu chí/cây/lọc/chi tiết) + thêm chiều cho `thong_ke_du_an_tkt` (thang, nhom_giai_phap, ung_dung, linh_vuc_kh, loai_hinh). Spec: `docs/superpowers/specs/agent-chat/2026-11-17-agent-ket-qua-du-an-tkt-design.md` (CHỜ DUYỆT).

## Giải pháp — rà 18/11 (subagent + tự kiểm lại code/DB local)
- Chốt 3 (18/11): "NV tham gia GP" = PM (`solutions.pm_id`) + thành viên GP (`solution_members` ACTIVE, dùng khi has_modules=0) + leader hạng mục (`solution_modules.leader_id`) + thành viên hạng mục (`solution_module_members`); đếm distinct theo GP, chia theo vai trò. DB local: chỉ thành viên = 38 người, cả 4 vai trò = 65 (đã tự đếm lại).
- Tiến trình GP = `solutions.status`: 1 Nháp · 3 Chờ PM duyệt · 5 Chờ Leader duyệt · 7 Đang triển khai · 9 Chờ duyệt GP · 11 Đã duyệt GP · 13 Đã duyệt giá · 15 Chờ làm giá · 17 Chốt GP · 2 Đóng.
- "Phòng làm GP" có 2 cách gán:
  - `solutions.department_id` = phòng người tạo GP (= `request_solutions.receive_dept`) — `thong_ke_giai_phap`, báo cáo Version GP dùng.
  - Báo cáo "Tổng hợp GP theo phòng ban" (`SolutionsWorkSummaryByDepartmentReportService`, quyền `presale.bao_cao_tong_hop_gp.view`): 1 "kỹ sư chính"/GP = leader hạng mục đầu tiên, không có thì người tạo; phòng = phòng HIỆN TẠI của người đó (`resolvePrimaryEngineer`, đã đọc code). Kỳ theo `solutions.created_at`, bỏ Nháp. Cây Công ty ▸ Phòng làm GP ▸ Nhân sự kỹ thuật. Cột: YCGP nhận/tiếp nhận, Tổng GP đã làm (status ≥11), đúng/trễ hạn, cơ cấu tiến trình, GP chốt, tỷ lệ chốt, ngành/nhóm GP/ứng dụng, báo giá. Local lệch với department_id 1/43 GP.
- Báo cáo "Hiệu suất theo GP" có staff_count nhưng chỉ leader + thành viên hạng mục (bỏ PM, bỏ solution_members) ⇒ không dùng để đếm tham gia.
- "Yêu cầu GP theo phòng KD" = phía phòng KD gửi yêu cầu (request_solutions), không phải phòng làm.
- Chốt 4 (18/11): "phòng làm GP" + "tiến trình GP" bám báo cáo "Tổng hợp GP theo phòng ban" (phương án 1) ⇒ công cụ mới `tong_hop_giai_phap`; NV tham gia làm ở `thong_ke_giai_phap`. Spec: `docs/superpowers/specs/agent-chat/2026-11-18-agent-tong-hop-giai-phap-design.md` (CHỜ DUYỆT).
