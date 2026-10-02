# Plan — Gia hạn hàng giữ không hiện hàng

@junfoke · Repo `TanPhatDev` · nhánh `master`

## Phase 1 — Bỏ điều kiện hạn giữ ở màn Tạo phiếu gia hạn

- [x] BE: `PrepickExtendRequest::getDataToCreate()` — bỏ `where('pd.expire_date', '<=', $date)`,
      dọn `$date` + `$config` + import `Config` không còn dùng
- [x] BE: `PrepickExtendRequestController::getDataToCreate()` — dọn `$config` / `$date` chết
- [x] Rà các nơi khác dùng `warning_day` — chỉ dashboard/cron cảnh báo/báo cáo tồn-mượn, giữ nguyên
- [x] BE: vá vòng lặp dựng cột "Hợp đồng" (lỗi lộ ra khi bảng có dữ liệu):
      khởi tạo lại `$contract = null` mỗi vòng + guard null cho 3 nhánh objectable
- [x] Verify trên DB local `erp_dev_30_01_26` (xem checkpoint)
- [ ] QA nghiệm thu trên prod với tài khoản chị Hải (NV 828): công ty SG ra 25 dòng,
      đổi sang công ty HN ra 11 dòng
- [ ] Cập nhật issue Redmine

### Checkpoint — 17/09/2026

Vừa hoàn thành: bỏ lọc hạn giữ + vá vòng lặp hợp đồng, verify bằng tinker trên DB local.

Bằng chứng verify (NV 263, 208 dòng `qty > 0`):
- `getDataToCreate()` trả **207 dòng** (trước khi sửa, lọc hạn `<= 24/09` cũng ra 207 — DB local
  hạn giữ đều cũ nên không tái hiện được cảnh rỗng; cảnh rỗng đã chứng minh bằng số đếm trên prod)
- Đi qua đủ 3 nhánh objectable: `WarehousePrepickRequest` 196, `PrepickExtendRequestDetail` 10,
  `PrepickTransfer2` 1 — không lỗi
- **189/196 dòng trỏ tới `warehouse_prepick_requests` đã bị xoá** ⇒ đúng kịch bản khiến
  `$contract` cũ bị dùng lại cho dòng sau nếu không reset

Đang làm dở: không có.
Bước tiếp theo: QA kiểm trên prod bằng tài khoản 828; sau đó commit + push `master`.
Blocked: chưa commit (chờ xác nhận của chủ dự án).
