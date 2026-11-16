# Plan — Duyệt kết quả HĐ dịch vụ báo "Có lỗi xảy ra!" khi phiếu duyệt không giao đủ hàng của HĐ (@junfoke)

Phiếu prod: `TPE.PDKQ.2026020028` (`/admin/customer-care/wr_approve_results/20028/edit`), HĐ dịch vụ 8398, PGV `TPE.PGV.2026020019`.

## Ngày 13/11/2026 (@junfoke)
- [x] 13/11/2026 — Xử lý lỗi bấm Duyệt phiếu duyệt KQ 20028 báo "Có lỗi xảy ra!": log prod chỉ ra `WrApproveResultsController@update` (dòng 1154) → `WrAssignTask::updateContract()`. Hàm duyệt từng dòng hàng bán thêm / vật tư / dịch vụ bảo hành của HĐ rồi đọc thẳng dòng tương ứng trên phiếu duyệt, mã nào lần này không giao ⇒ `Trying to get property 'qty' of non-object`, huỷ cả thao tác. Lộ ra từ 11/11 vì #11512 chặn giao hàng chưa xuất kho (HĐ 8398 local mới xuất 1/5 mã).
- [x] 13/11/2026 — Sửa `app/Model/Customers/WrAssignTask.php` (+5 dòng): dòng nào phiếu duyệt lần này không có thì bỏ qua, không cộng số lượng — như nhánh Sửa chữa đang làm; áp cho hàng bán thêm (chỗ gây lỗi) + vật tư, dịch vụ của thiết bị bảo hành. Dựng lại lỗi trên DB local bằng phiếu 19597 cùng HĐ, giả lập giao 1/5 mã (transaction rollback): code cũ lỗi đúng dòng 2422, code mới qua. Bỏ duyệt không dính.
- [x] 13/11/2026 — Commit `101bda88a6` (gop_db, đã push).

### Checkpoint — 13/11/2026 15:02
Vừa hoàn thành: sửa + lên `origin/gop_db`.
Đang làm dở: —
Bước tiếp theo: deploy xong nhờ người dùng bấm Duyệt lại phiếu 20028; còn lỗi thì lấy dòng thông báo ngay trên `#0` trong log.
Blocked:
