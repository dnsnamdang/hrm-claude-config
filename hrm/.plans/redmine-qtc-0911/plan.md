# Redmine Quyết toán công 09/11/2026 (HRM phần)

Worktree: HRM/.wt-hrm-api-qtc + HRM/.wt-hrm-client-qtc, nhánh fix/redmine-qtc-0911 từ origin/develop.
Phần ERP (#11490) ở ERP/.plans/redmine-qtc-0911/plan.md.

- [x] #11491 Danh sách phiếu công tác: lọc theo số HĐ (HDDV_TPE_HN_KD2_26_0003_CHECKQTC1) không ra kết quả
- [x] #11493 Tạo PCT mới của HĐ đã có PCT: cho thêm NV QTC mới; 2 PGV cùng HĐ trong 1 PCT thì NV QTC đồng bộ
- [x] #11494 Tạo QTC: HĐ đã giao công tác hết vẫn báo "PGV ... chưa được giao đi công tác"
- [x] #10992 Tạo QTC: Công khoán đề xuất/TP duyệt/KT duyệt + CK phụ đề xuất/TP/KT ≤ ĐM công tương ứng trong phiếu duyệt KQ
- [x] #11492 Dashboard dự án & giao việc: thống kê QTC chờ TP duyệt / chờ KT duyệt (link danh sách QTC lọc trạng thái, phân quyền)
- [x] Verify + test (script PHP + compile-check template; CHƯA bấm thử trên trình duyệt vì client đang chạy là cây chính, không phải worktree)

### Checkpoint — 2026-11-09
Vừa hoàn thành: code xong 5 vé HRM, chưa commit.
- #11491: lọc theo mã HĐ hiện tại (wr_service_contracts/firm_contracts.code) ngoài mã snapshot; đổi điều kiện lọc thì về trang 1. Rollback-test: đổi tên HĐ 2996 → lọc mới ra [10752], cũ ra [].
- #11493: PCT mới kế thừa toàn bộ NV QTC của PCT gần nhất cùng HĐ (employee_info_qtc_list), khoá không cho xoá NV kế thừa, cho thêm; 2 PGV cùng HĐ đồng bộ.
- #11494: tìm PCT đã duyệt theo AssignRequest::PCT_APPROVED_STATUSES thay vì chỉ DA_DUYET.
- #10992: FE validateWithinNorm (viền đỏ + câu lỗi dưới ô) + BE SettlementContractService::normErrors ở store/update/approve/ktApprove (400 kèm lỗi theo key FE). Sai số <0.001 bỏ qua.
- #11492: 2 thẻ "Quyết toán công chờ TP/KT duyệt" ở khối Chờ duyệt dashboard, quyền assign.quyet_toan_hop_dong_{truong_phong|ke_toan}.approve, đếm bằng SettlementContractCriteria (khớp danh sách); index.vue đọc ?status=. Rollback-test: TP=2 KT=1 = số dòng list.
Đang làm dở: không
Bước tiếp theo: user duyệt → commit + push develop (api + client)
Blocked: 
