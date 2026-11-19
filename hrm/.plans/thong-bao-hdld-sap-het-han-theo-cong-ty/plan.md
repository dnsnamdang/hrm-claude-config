# Thông báo HĐLĐ sắp hết hạn chỉ gửi theo công ty của hợp đồng (chưa có số Redmine) — @cuong61n

Branch: `gop_db` (hrm-api, worktree `worktrees/gop_db-api`) — đã chuyển từ `gop_db-main` 19/11/2026. Trạng thái: đã push `gop_db` (commit fcc961f39, 19/11/2026), đã chạy ~/build_tpe.sh trên prod 19/11/2026 (chưa test chạy lệnh thật).

## Nghiệp vụ
Thông báo "[HDLD] Sắp đến hạn" (còn 15/10/5 ngày) đang gửi cho mọi người có quyền `decision.hop_dong_lao_dong.create`
ở BẤT KỲ công ty nào. Prod (hrm_erp_gop): TK cuong61n@gmail.com (employees.id 1349) giữ quyền ở công ty 10/3/4 nhưng
vẫn nhận HĐ 612, 727 của công ty 1. Yêu cầu: chỉ người có quyền trong công ty của hợp đồng mới nhận.

## Tasks
- [x] 2026-11-19 Điều tra prod: xác nhận nguyên nhân (quyền lấy không lọc công ty, danh sách dùng chung mọi hợp đồng)
- [x] 2026-11-19 BE `DecisionLaborContractService::notifyExpiringContracts()`: người nhận = người có quyền tạo HĐLĐ tại
  công ty của hợp đồng (`labor_contract_company_id`, thiếu thì lấy công ty NV), cache theo công ty; NV có HĐ vẫn nhận như cũ.
  Kiểm: `php -l` OK.
- [ ] Test: chạy `contracts:notify-expiring` trên dev với HĐ còn 5 ngày, kiểm người nhận đúng công ty
- [ ] Chốt với user: NV có hợp đồng có nhận không (hiện giữ nguyên là có)

## Rà soát toàn bộ thông báo gửi sang công ty khác (19/11/2026)
- [x] 2026-11-19 Quét 148 file có gửi thông báo ở hrm-api (gop_db): 309 thông báo → 4 LỖI chắc chắn, 62 NGHI LỖI, 243 OK. Kết quả: `ra-soat-thong-bao-theo-cong-ty.xlsx` (cùng thư mục). Chỉ đọc code, chưa kiểm DB.
- LỖI: Yêu cầu nhập hàng (2: BKS→BGĐ duyệt giá, phiếu trả lại đã quyết toán→BKS), Thông báo khóa học (mở đăng ký, gửi mọi nhân viên), Thông báo nội bộ (Duyệt, gửi mọi nhân viên).
- [ ] Chờ user chốt: sửa nhóm nào, 2 dòng gửi "tất cả" có phải chủ ý không, 62 dòng NGHI có cho thao tác chéo công ty không.
