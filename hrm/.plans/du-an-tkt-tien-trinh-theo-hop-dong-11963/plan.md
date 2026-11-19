# #11963 — Tiến trình nội bộ Dự án TKT đồng bộ theo sự kiện Hợp đồng

## Yêu cầu (Redmine #11963)
1. Sự kiện 1: KD tạo HĐ gắn Dự án TKT ⇒ tiến trình nội bộ dự án = **Thương thảo hợp đồng** (status 8).
2. Sự kiện 2: KD upload thành công file HĐ khách hàng đã ký ⇒ **Thực hiện hợp đồng** (status 9).
3. Lưu vết: thời điểm + người tác động làm đổi bước.

## Hiện trạng
- Bước 8 trước đây chỉ do **chốt báo giá** (`QuotationService::finalize`) đặt. HĐ chỉ lập được từ báo giá trúng thầu
  nên phần lớn dự án đã ở 8, nhưng dữ liệu cũ có dự án vẫn ở 7 (vd dự án 144 / BG-2026-00074).
- Bước 9 chưa có đường nào đặt.
- Lưu vết có sẵn: `ProspectiveProject::changeStatusById()` đi qua model ⇒ hook `booted()->updating` ghi
  `prospective_project_status_logs` (status_from, status_to, changed_at, changed_by = auth). Lịch sử dự án
  (`SystemLogService::prospectiveProjectLogs`) hiện dòng "Thay đổi trạng thái" từ bảng này ⇒ không cần thêm cột/bảng.

## Thay đổi (BE, `Modules/Assign/Services/ContractService.php`)
- [x] `createFromQuotation` (cuối transaction): `changeStatusById(project_id, 8, onlyIfBelow 8)`.
- [x] `confirmCustomerSigned` (sau transition CHO_KH_KY → KH_DA_KY, tức sau khi upload file thành công):
      `changeStatusById(project_id, 9, onlyIfBelow 9)`.
- Chỉ TIẾN: dự án đã ở bước cao hơn (Nghiệm thu, Đóng, Kết thúc…) giữ nguyên, không ghi log.
- HĐ không gắn dự án (`project_id` null) ⇒ bỏ qua.
- Danh sách / chi tiết Dự án TKT và các báo cáo đọc `prospective_projects.status` ⇒ tự ăn theo, FE không đổi.

## Test
`Modules/Assign/Tests/Feature/ContractProjectProgressSyncTest.php` — 4 ca (tạo HĐ → 8 + log người tạo;
KH ký → 9 + log; dự án đã ở 10 không lùi; HĐ không dự án vẫn chạy).
DB dev `erp_hrm_check` đang thiếu migration HĐ ⇒ test dựng TEMPORARY TABLE `hrm_contracts` + áp migration HĐ lên
bảng tạm, rollback cuối test; DB thật không đổi. Đã kiểm ngược: bỏ code ⇒ 2 ca chính đỏ.

## Đợt 2 (18/11, user duyệt đề xuất) — CHƯA commit
- [x] Xoá HĐ Đang tạo ⇒ trả dự án về bước trước khi lập HĐ (`rollbackProjectProgressOnDelete`), chỉ khi: dự án
      vẫn ở 8, không còn HĐ khác gắn dự án, và có log →8 sinh lúc tạo HĐ (≤ 1 phút trước created_at HĐ).
      Dự án đã ở 8 từ chốt báo giá ⇒ giữ nguyên. Lần lùi có log (người xoá + thời điểm).
- [x] HĐ lập từ BÁO GIÁ TỔNG ⇒ dự án cha: tạo HĐ → 8 "Thương thảo/đã hợp đồng", KH ký → 9 "HĐ đủ điều kiện
      thực hiện" (chỉ tiến). HĐ dự án con lẻ không đẩy dự án cha. Xoá HĐ báo giá tổng cũng lùi dự án cha (cùng điều kiện).
- Test thêm 4 ca (tổng 8/8); kiểm ngược tắt code ⇒ 2 ca chính đỏ.

## Không làm
- Luồng ERP `erpMarkContract` (API public, không có người tác động; local 0 báo giá đi luồng này từ 01/10).
- HĐ huỷ / thanh lý sau khi ký: không tự lùi, KD đổi tay.
