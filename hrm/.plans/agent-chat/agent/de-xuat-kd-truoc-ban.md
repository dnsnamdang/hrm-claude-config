# Đề xuất: Agent phục vụ kinh doanh trước bán — 11/11/2026

User 11/11: tạm dừng việc Agent nội bộ (xem plan.md "⏸ VIỆC CHỜ"), ưu tiên phân hệ **CSKH trước bán + Meeting phục
vụ kinh doanh**: (1) dự án tiền khả thi, (2) meeting theo thị trường, (3) làm giải pháp. CHƯA code.

Rà code hrm-api worktree `gop_db-tpe-smart-agent` (2 agent rà + tự kiểm các điểm chính bằng code/DB local).

## 1. Hiện trạng dữ liệu

### Dự án tiền khả thi — `prospective_projects` (`Modules/Assign/Entities/ProspectiveProject.php`)
- Mã, tên, khách hàng (`customer_id` + bản chụp tên/mã/MST/liên hệ; KH hưởng lợi khi qua trung gian), **NVKD chính**
  (`main_sale_employee_id` + phòng/bộ phận), phòng/NV hỗ trợ (`prospective_project_support_departments` → employees),
  PM giải pháp (`solution_employee_id`).
- **Tiến trình nội bộ** (status, `:112-123`): 1 Đang tạo · 2 Thu thập thông tin · 3 Chờ tiếp nhận làm GP · 4 Đang làm GP ·
  5 Trao đổi GP với KH · 6 Lập dự toán · 7 Thương thảo giá & GP · 8 Thương thảo HĐ · 9 Thực hiện HĐ · 10 Nghiệm thu &
  thanh lý · 11 Đóng/Không thực hiện · 12 Kết thúc & lưu trữ (dự án cha dùng bộ nhãn khác — `resolveStatusName`).
  DB local: 586 dự án (2: 196 · 6: 59 · 7: 158 · 11: 143 …).
- **Giai đoạn dự án KH** (`project_phase_id`), quy mô, loại đầu tư, nguồn vốn, **nhóm ngành** (`scope_id` → hrm_scopes,
  cấp trên = Lĩnh vực công ty KD), nhóm giải pháp (`industry_id`), ứng dụng, lĩnh vực / loại hình KH.
- Tiền: `estimated_budget` (ngân sách dự kiến), `expected_contract_amount`, `expected_profit`. KHÔNG có cột xác suất,
  KHÔNG có ngày dự kiến chốt. Hạn: `customer_need_solution_date`, `internal_solution_close_date`, `auto_close_date`.
- Lịch sử: `prospective_project_status_logs` (đổi tiến trình, `statusAt($date)`), `prospective_project_history` (audit).
- Liên kết: meeting (`prospective_project_meetings`), yêu cầu làm GP (`request_solutions.project_key`), giải pháp
  (`solutions.prospective_project_id`), báo giá (`quotations.project_id`).
- **Quyền xem**: `presale.danh_sach_du_an_tien_kha_thi.view` (1–4). Có sẵn `ProspectiveProject::visibleIdsQuery()` (đã có
  test giữ khớp màn danh sách): GROUP thấy hết; còn lại theo **org người TẠO** (công ty / phòng-bộ phận quản lý / tự tạo)
  HOẶC là NV hỗ trợ có tên. ⚠️ API `show` không kiểm quyền ⇒ công cụ phải tự lọc qua `visibleIdsQuery()`.
- Báo cáo có sẵn: tổng hợp dự án TKT (`presale.bao_cao_tong_hop_du_an_tkt.view`), **kết quả dự án TKT** (theo NVKD chính;
  thắng 9/10/12, thua 11, tỉ lệ thành công, tổng ngân sách — `presale.bao_cao_ket_qua_du_an_tkt.view`), phát triển KH theo
  NVKD, tổng hợp CSKH tiềm năng (nhu cầu từ meeting + dự án đang mở, "lần chăm sóc cuối").

### Meeting theo thị trường
- **"Thị trường" trong code hiện tại = tỉnh/thành của khách hàng.** Meeting chụp `province_id` / `province_name` lúc lưu
  (`MeetingMarketSnapshotService`; local 2,337/3,025 meeting có tỉnh). Thiếu tỉnh ⇒ "Chưa xác định thị trường". Tỉnh có
  `area_id` (Vùng).
- Báo cáo có sẵn: **Kết quả meeting theo thị trường** (cây Tỉnh → KH → meeting; tổng theo trạng thái, theo tỉnh, theo
  phòng chủ trì, KH mới, tỉ lệ hoàn thành — `presale.bao_cao_ket_qua_meeting_theo_thi_truong.view`); **Phát triển thị
  trường – KH** (cây Thị trường › Phòng › Bộ phận › NV; kế hoạch, hoàn thành, huỷ, KH mới, nhu cầu, đầu tư —
  `presale.bao_cao_phat_trien_thi_truong_khach_hang.view`); meeting theo NV, theo dự án.
- Phân chia thị trường (phòng/NV phụ trách tỉnh/phường) có bảng `division_market_*` (nhập ở ERP, HRM chỉ đọc).
- ⚠️ `MeetingByMarketService.php:234` còn tra tỉnh qua DB ERP cũ (`DB_DATABASE_SECOND`) — trái quy tắc gop_db; công cụ
  Agent sẽ dùng cột chụp `meetings.province_id`, không gọi hàm này.

### Làm giải pháp
- **Yêu cầu làm GP** `request_solutions`: 1 Nháp · 2 Chờ tiếp nhận · 9 Yêu cầu bổ sung · 3 Đã tiếp nhận · 4 Từ chối ·
  6 Đang thực hiện · 8 Đã hoàn thành · 5 Đã huỷ · 10 Đóng · 11 Đã chốt GP; hạn phản hồi (trong hạn/quá hạn), ngày KH cần
  GP / báo giá, phòng + người tiếp nhận. Quyền `presale.danh_sach_yeu_cau_lam_giai_phap.view` (local 33 yêu cầu).
- **Giải pháp** `solutions`: 1 Nháp · 3 Chờ PM duyệt · 5 Chờ Leader duyệt · 7 Đang triển khai · 9 Chờ duyệt GP ·
  11 Đã duyệt GP · 13 Đã duyệt giá · 15 Chờ làm giá · 17 Chốt GP · 2 Đóng; PM, % tiến độ, version hiện tại, hạng mục
  (leader, hạn), thành viên. Quyền `assign.danh_sach_lam_giai_phap.view` + nới cho PM / leader / thành viên (local 43 GP).
- Dashboard quản lý GP có sẵn: hạng mục trễ, người trễ việc, thống kê trạng thái việc, việc/vấn đề/meeting sắp tới.
- ⚠️ `SolutionService::getAll` và `show` + các endpoint manager không kiểm quyền xem (ghi vào lỗ hổng #15).

## 2. Công cụ đề xuất (nháp — chốt sau khi trả lời câu hỏi mục 3)

| # | Công cụ | Trả lời được | Nguồn |
|---|---|---|---|
| 1 | `tim_khach_hang` (tra cứu) | "dự án của KH ABC", "meeting với Hoà Phát" | customers + quyền xem KH (cần chốt) |
| 2 | `du_an_tkt` | "Dự án tôi đang theo?", "Dự án đang thương thảo giá của phòng", "Dự án nhóm ngành thép", "Dự án sắp tới hạn giải pháp" | `ProspectiveProjectService::index` lọc qua `visibleIdsQuery()` |
| 3 | `chi_tiet_du_an_tkt` | "Dự án X đang ở bước nào, ai phụ trách, GP tới đâu, họp KH lần cuối khi nào?" | entity + status_logs + GP + meeting gần nhất |
| 4 | `thong_ke_du_an_tkt` | "Phòng tôi đang có bao nhiêu dự án, tổng ngân sách theo từng bước?", "Tỉ lệ thắng quý này của NVKD" | logic báo cáo tổng hợp / kết quả dự án TKT |
| 5 | `meeting_theo_thi_truong` | "Tháng này họp bao nhiêu KH ở Hà Nội?", "Tỉnh nào nhiều meeting nhất?", "Thị trường nào chưa có meeting?" | `meetings.province_id` + phạm vi quyền báo cáo |
| 6 | `lich_su_cham_soc_khach_hang` | "Lần cuối chăm sóc KH ABC là khi nào, nội dung gì, nhu cầu gì?" | meeting hoàn thành + nhu cầu đầu tư + dự án của KH |
| 7 | `giai_phap` (+ yêu cầu làm GP) | "Yêu cầu GP nào đang chờ tiếp nhận?", "GP của dự án X tới đâu?", "GP nào trễ hạn KH cần?" | `RequestSolutionService::index`, `SolutionService::index` |

## 3. Câu hỏi cần chốt (hỏi lần lượt)

1. "Thị trường" = tỉnh/thành của KH (như báo cáo đang có) hay Vùng hay nhóm ngành? → **CHỐT 11/11: tỉnh/thành của KH** (cột chụp `meetings.province_id`).
2. "Dự án của phòng tôi" tính theo org người TẠO (màn danh sách) hay theo NVKD chính (báo cáo kết quả)? → **CHỐT 11/11: user xác nhận NVKD chính và người tạo thực tế luôn là 1 người** (local 586/586 trùng). Dùng quyền xem qua `visibleIdsQuery()` (org người tạo); "dự án của tôi" = `main_sale_employee_id` = tôi; "của phòng" = org dự án (`department_id`/`part_id`).
3. Có cho Agent nêu số tiền (ngân sách dự kiến, giá trị HĐ dự kiến) không — với ai? → **CHỐT 11/11: CÓ, cho mọi người xem được dự án** (giống màn danh sách; số tiền gửi model — tài khoản chưa ZDR, user chấp nhận).
4. Tra cứu khách hàng: ai được tra KH nào (quyền xem danh sách KH)? → **CHỐT 11/11: giống màn Danh sách KH** (`CustomerService::applyVisibilityScope` — có `master_data.khach_hang.view` thấy tất cả, không có ⇒ KH gắn với mình). Hàm đang private ⇒ tách dùng chung = sửa service dùng chung → PHẢI hỏi lại riêng trước khi code.
5. Người dùng chính: NVKD (của tôi) hay trưởng phòng / BGĐ (thống kê)? — quyết định làm công cụ nào trước. → **CHỐT 11/11: trưởng phòng / BGĐ trước.**

## 4. Lỗ hổng phát hiện thêm
- #15 `SolutionService::getAll` / `show` / endpoint `/{solution}/manager/*` không kiểm quyền xem; `getAll` truyền
  `sort_field` thẳng vào `orderBy`.
- #16 `ProspectiveProjectController::show` không kiểm quyền xem (chỉ route-model binding).
- Ngoài luồng: `MeetingByMarketService` dùng DB ERP cũ.

## 5. ĐỢT 1 (chốt sau 5 câu hỏi) — cho trưởng phòng / BGĐ

Không cần `tim_khach_hang` ở đợt này ⇒ KHÔNG đụng `CustomerService` dùng chung. Chỉ thêm công cụ trong `Modules/Agent`,
dùng lại thẻ FE có sẵn (`bars`, `tasks`), không migration.

### 5.1 `thong_ke_du_an_tkt`
- Tập dự án: `ProspectiveProject::visibleIdsQuery()` (quyền `presale.danh_sach_du_an_tien_kha_thi.view`, = màn danh sách),
  bỏ dự án nháp (status 1), mặc định chỉ dự án gốc + độc lập (không đếm trùng dự án con) — kiểm lại với service list.
- Tham số: `pham_vi` toi (NVKD chính = tôi) / phong (`department_id`; mặc định phòng của tôi; `phong_ban_id` cho phòng khác
  ⇒ tim_phong_ban) / cong_ty · `nhom_theo` tien_trinh (mặc định) | nvkd | nhom_nganh | giai_doan · `tinh_trang`
  dang_theo_duoi (2–8) | thang (9, 10, 12) | dong (11) | tat_ca · `tu_ngay/den_ngay` (ngày tạo).
- Trả: mỗi nhóm số dự án + tổng `estimated_budget`; tổng chung; tỉ lệ thắng = thắng / (thắng + đóng). Thẻ `bars`.
- Câu: "Phòng tôi đang theo đuổi bao nhiêu dự án, tổng ngân sách từng bước?", "NVKD nào nhiều dự án nhất?",
  "Tỉ lệ thắng năm nay?", "Dự án theo nhóm ngành".

### 5.2 `meeting_theo_thi_truong`
- Tập meeting: có `customer_id`, trạng thái 1–4, theo cột chụp `meetings.province_id/province_name` (null ⇒ "Chưa xác định").
- Quyền: `presale.bao_cao_ket_qua_meeting_theo_thi_truong.view` theo đúng logic phạm vi của báo cáo
  (`MeetingByMarketService.php:177-214`: tổng công ty / công ty / phòng-bộ phận quản lý / meeting mình tạo hoặc tham gia).
  KHÔNG gọi phần tra tỉnh qua DB ERP cũ.
- Tham số: `tinh` (tên tỉnh, khớp không dấu ⇒ province_id; "chưa xác định") · `nhom_theo` tinh (mặc định) | trang_thai |
  phong (phòng chủ trì) | nhan_vien (chủ trì) · `tu_ngay/den_ngay` (mặc định tháng này) · `phong_ban_id`.
- Trả: mỗi nhóm số meeting, hoàn thành, huỷ, số KH khác nhau, tỉ lệ hoàn thành. Thẻ `bars`.
- Câu: "Tháng này tỉnh nào nhiều meeting nhất?", "Hà Nội tháng này họp bao nhiêu KH, xong bao nhiêu?",
  "Meeting ở Hải Phòng theo phòng".

### 5.3 `giai_phap`
- `loai` = yeu_cau (request_solutions, quyền `presale.danh_sach_yeu_cau_lam_giai_phap.view` qua `RequestSolutionService::index`)
  | giai_phap (solutions, quyền `assign.danh_sach_lam_giai_phap.view` + nới PM/leader/thành viên qua `SolutionService::index`).
- Tham số: `trang_thai` (nhóm: cho_tiep_nhan, dang_lam, xong, dong/huy) · `qua_han` (yêu cầu: quá hạn phản hồi; giải pháp:
  quá `internal_need_gp_date` / `customer_need_gp_date` mà chưa chốt) · `phong_ban_id` (phòng tiếp nhận) · `tu_khoa` (mã / tên /
  KH / dự án).
- Trả: mã, tên, dự án + KH, PM / người tiếp nhận, hạn KH cần, trạng thái, % tiến độ, version. Thẻ `tasks`.
- Câu: "Yêu cầu giải pháp nào đang chờ tiếp nhận?", "Giải pháp nào trễ hạn KH cần?", "Giải pháp của dự án X tới đâu?".

### Kiểm
Test có quyền / không quyền / phòng khác / khác công ty (giống hệt không tồn tại) cho cả 3; thêm ~9 câu eval; `agent:eval`
(~1,000 ₫/lần) không tụt câu cũ; hỏi thử thật bằng tài khoản trưởng phòng.
