# Redmine Quyết toán công 09/11/2026 (ERP phần)

Worktree: ERP/.wt-erp-qtc, nhánh fix/redmine-qtc-0911 từ origin/develop.

- [x] #11490a PLBS HĐ dịch vụ SC-BH (đang tạo): không hiện Phòng QTC / NV QTC; chỉ hiện khi QTC của HĐDV đã duyệt
- [x] #11490b Đơn hàng nguyên tắc: hiện NV QTC + phòng QTC khi QTC của ĐHNT/HĐ được duyệt
- [x] Verify (rollback-sim SettlementQtcHelper: QTC chờ duyệt → rỗng; đã duyệt → NV 13 / phòng 5)

### Checkpoint — 2026-11-09
Vừa hoàn thành: SettlementQtcHelper + gắn vào PLBS HĐDV (tạo/sửa/xem) và ĐHNT (tạo/sửa/xem, thêm 2 ô chỉ đọc Phòng QTC / NV QTC).
Đang làm dở: không
Bước tiếp theo: user duyệt → commit + push develop
Blocked:

- [x] Sửa nhánh: ERP dev là develop_02 (lỡ push 01b4c56851 lên origin/develop cũ) → cherry-pick lên gop_db 4015b16d7a + develop_02 ca45786c5b; kiểm cột/bảng gop_db + test helper rollback OK

### Checkpoint — 2026-11-09
Vừa hoàn thành: #11490 đã lên gop_db + develop_02
Đang làm dở: —
Bước tiếp theo: xong — user chọn để nguyên origin/develop cũ
Blocked:
