# Fix: Quyết toán HĐ dịch vụ báo "chưa hoàn thành giao việc" khi HĐ có cả PGV đời cũ lẫn đời mới

QA báo HĐ `HDDV_TPE_HN_KDTM_25_0006_003` (id 395) · @junfoke · ERP `TanPhatDev` nhánh `gop_db`

## Ngày 05/11/2026 (@junfoke)
- [x] 05/11/2026 — Xử lý lỗi: HĐ 11 dòng, PLG002 giảm 5 dòng, 6 dòng còn lại đã giao + duyệt KQ 100% (PGV 520 → PDKQ 1358: 5 dòng; PGV 1240 → PDKQ 1838: 1 dòng) mà Quyết toán báo chưa hoàn thành giao việc. Nguyên nhân: bảng tiến độ `assign_task_progress` chỉ ghi với PGV lập từ ~16/09/2025; PGV 520 (22/08/2025) không có bản ghi, PGV 1240 lại ghi tiến độ cho cả 11 dòng (10 dòng SL 0) ⇒ code cũ "có bản ghi tiến độ thì chỉ cộng tiến độ" bỏ qua kết quả PGV 520.
- [x] 05/11/2026 — Sửa "chọn một trong hai" → **cộng cả hai**: đã giao = tiến độ + SL hoàn thành trên **phiếu kết quả** của PGV đời cũ (hàm mới `WrAssignTask::legacyTaskIdsOfContract`); sửa `WrServiceContractProduct::getAssigningProcessQty` (công sửa chữa) và `WrServiceContractProductService::getAssigningServiceQty` (dịch vụ, lọc đúng tên dịch vụ). HĐ không có PGV cũ thì như trước.
- [x] 05/11/2026 — Verify DB local bắt lỗi bản đầu (đếm cả PGV gốc 520 — dòng dịch vụ mặc định cờ hoàn thành lúc lập ⇒ đếm trùng) → chỉ đếm phiếu kết quả. `canCreateSettlementContract` HĐ 395 qua bước giao việc, dừng ở "Hợp đồng vẫn còn công nợ" (điều kiện nghiệp vụ). Giao diện local: code cũ "Hợp đồng chưa hoàn thành giao việc!", code mới hết; màn tạo PGV không cho giao lại 5 dòng (câu "Không có quyền!" là câu chung khi `canAssignTask()` false).
- [x] 05/11/2026 — Commit `9323072f2b` ("fix lỗi", gop_db, đã push).
