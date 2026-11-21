# Phản hồi note Tân Phát trên bảng "Danh mục quyền theo chức năng" (db_gop_3_11) — @cuong61n

Nhánh code: `gop_db-phan-quyen-tan-phat-note` (tách từ `gop_db`, chưa push). hrm-api commit `70cffc095`; ERP (TanPhatDev) commit `7fd95c41e7`.

## Phase 1 — Phản hồi cột "DNS phản hồi" (19/11/2026)
- [x] 19/11 Đọc 95 dòng có "Tân Phát note" (sheet Danh sách quyền), đối chiếu Catalog `app/Support/Permissions/Catalog` + code gop_db + menu FE (cổng 3002)
- [x] 19/11 Soạn 95 phản hồi nháp; đã thử điền lên Google Sheet rồi GỠ lại theo yêu cầu (chưa cho người khác đọc). Bản nháp lưu local, chờ Cường duyệt trước khi đưa lên sheet
- [x] 19/11 Phát hiện: dòng 290 đổi tên sẽ TRÙNG tên mã HRM `sale.yeu_cau_hach_toan_mua_dich_vu.view` → phải gộp 2 mã, không đổi tên (xem Phase 3)

## Phase 2 — Sửa Catalog (chỉ đổi nhãn/nhóm hiển thị, KHÔNG đổi `code`) — chờ test
- [x] 19/11 Đổi tên quyền: báo cáo Công việc (562-566), danh sách vấn đề/nhiệm vụ, duyệt triển khai nhiệm vụ, Quản lý vai trò và phân quyền, Trưởng phòng duyệt hợp đồng, Duyệt YC hạch toán mua dịch vụ, Xem phiếu hạch toán mua dịch vụ, loại hình/lĩnh vực kinh doanh KH, báo cáo meeting NV/phòng ban/công ty
- [x] 19/11 Đổi chức năng (feature): 5 báo cáo công nợ, Hợp đồng dự án (giá vốn, phân tích DA)
- [x] 19/11 Chuyển nhóm: danh mục câu hỏi KS/loại tài liệu/loại giảm giá → CSKH trước bán > Danh mục; lĩnh vực + loại hình KH → Danh mục dùng chung; Nhu cầu KH + 2 báo cáo meeting → Meeting; Duyệt YC làm dịch vụ → CSKH sau bán; Hạch toán mua dịch vụ → Tài chính
- [x] 19/11 Kiểm: `php -l` sạch; test Catalog còn 3 lỗi CÓ SẴN (tpe_agent_thong_ke, payroll.bang_luong, báo cáo giữ hàng) — không liên quan
- [x] 19/11 Kiểm dữ liệu prod (chỉ đọc, ssh hrm-prod): `phieu_tinh_lai.view` 20 vai trò đều mức 3/4 → thu hẹp còn [3,4] KHÔNG ảnh hưởng ai; đã sửa `scopes` + bỏ 2 legacy min_scope 1,2
- [x] 19/11 Đổi tên `presale.bao_cao_ket_qua_du_an_tkt.view` → "Xem báo cáo kết quả thực hiện dự án TKT", `presale.bao_cao_theo_doi_giai_phap_theo_phong_kd.view` → "Xem báo cáo theo dõi YCLGP theo phòng KD" (khớp tên menu)
- [x] 19/11 Bỏ `admin.phan_quyen.view`: ERP HomeController (cảnh báo "Tài khoản chưa phân quyền") chuyển sang `admin.phan_quyen.manage`; gỡ mã khỏi Catalog; sửa AdminCodesTest (ERP, chưa chạy test); prod: 10 vai trò giữ mã, chỉ TPE_Chủ tịch HĐQT (2 nv) chưa có manage
- [x] 19/11 `catalog-sync --dry-run` (DB local): validate OK, `phan_quyen.view` + `sale.bao_cao_giu_hang.view` vào "ngừng dùng"
- [ ] Chờ: `permission:catalog-sync` chạy thật (ghi DB — hỏi trước); deploy dev/prod qua `~/build_tpe.sh`

## Phase 3 — Chưa làm, cần quyết định
- [x] 19/11 Kiểm "công ty nào xem công ty đó" cho 8 danh mục (dòng 362-369): Công ty, Khối, Phòng ban, Bộ phận, Chức vụ, Chức danh, Ngạch lương ĐÃ lọc theo công ty đang chọn (Khối/Phòng ban/Bộ phận: `company_role` hoặc `company_id` của người dùng) → giữ nguyên, không sửa code. (Kết luận sớm "Khối/Phòng ban/Bộ phận thấy mọi công ty" là SAI — bỏ sót nhánh else, đã đính chính). Danh sách Năng lực KHÔNG lọc công ty
- [x] 19/11 Lọc danh sách Năng lực theo công ty (dòng 369): `CompetencyService::index` + `getAll` lọc theo công ty của NHÓM năng lực (prod `competencies.company_id` lệch nhóm 35/396 dòng); chỉ khi `use_common_catalog=false`. Kiểm DB local: 7 công ty, index/getAll khớp số kỳ vọng. Chưa commit/deploy
- [ ] `accounting.bao_cao_ban_hang_theo_mat_hang.view`: prod có 15 vai trò (~55 nv) ở mức Phòng ban/Bộ phận → chờ Tân Phát chọn nâng lên Công ty / bỏ quyền / giữ Phòng ban (chưa sửa)
- [ ] Bỏ `sale.ho_tro_hach_toan_day_du.view` (11 file ERP → mã danh sách): prod 5 vai trò Giám đốc chưa có `ho_tro_hach_toan.view` cần cấp bù; 6 vai trò kế toán sẽ thấy đủ thông tin → chờ xác nhận
- [ ] Bổ sung phạm vi cho `sale.ho_tro_hach_toan.view` (ERP): prod 18 vai trò scope NULL, màn ERP không lọc theo phạm vi → chờ Tân Phát chọn mức từng vai trò rồi sửa Catalog + lọc ERP
- [ ] Gộp 2 mã cùng nghĩa YC hạch toán mua dịch vụ (HRM `...mua_dich_vu.view` ↔ ERP `...dich_vu_can_mua.view`)
- [ ] Thêm mã mới (chờ Tân Phát xác nhận): Quản lý nhiệm vụ phòng ban, Quản lý định biên theo quy mô, Quản lý phân công nhiệm vụ, Thêm HĐ bán đầu kỳ, quyền riêng BC vòng đời TKT / tổng hợp giải pháp theo phòng ban
- [ ] Tách HĐ nguyên tắc thành 2 bước duyệt (cần chốt với ERP)
