# Plan — Điều kiện quyết toán công: yêu cầu đã quyết toán HĐ

## Phase 1 — Sửa điều kiện trong CheckContractIsDoneController

File: `ERP/TanPhatDev/app/Http/Controllers/Common/CheckContractIsDoneController.php`

- [x] Nhánh `firm`: thay logic "giao việc xong" bằng check `FirmContract.status == DA_QUYET_TOAN(10)`
- [x] Nhánh `wr`: thêm rẽ nhánh theo `WrServiceContract.type`
  - [x] `type != BAO_HANH(2)` (HĐDV + phụ lục) → check `status == DA_QUYET_TOAN(5)`
  - [x] `type == BAO_HANH(2)` (PBH) → giữ nguyên logic "giao việc xong" hiện có
- [x] Message khi chưa đủ: "Hợp đồng chưa quyết toán, không thể quyết toán công"
- [x] `php -l` pass

## Kiểm thử (thủ công)
- [ ] HĐ bán chưa quyết toán HĐ → quyết toán công bị chặn, báo message
- [ ] HĐ bán đã quyết toán HĐ (status=10) → cho quyết toán công
- [ ] HĐDV chưa/đã quyết toán HĐ (status=5) → chặn / cho
- [ ] PBH (wr type=2) → vẫn theo "giao việc xong" như cũ
- [ ] ĐHNT (firm type=8) → hành xử như HĐ bán

### Checkpoint — 2026-06-09
Vừa hoàn thành: khảo sát luồng + chốt thiết kế (Phương án A), tạo design.md + plan.md
Đang làm dở: chuẩn bị sửa CheckContractIsDoneController
Bước tiếp theo: edit nhánh firm + wr trong checkContractIsDone
Blocked:
