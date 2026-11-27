# Phiếu YC nhập trả lại hàng mượn: thêm cột "SL duyệt trả" — plan

Báo 27/11/2026: PYCNH-16898 (YCXH 47434) cột "SL trả" = 1 nhưng BC hàng mượn vẫn còn mượn MARA-P0190. Tra hrm_erp_gop:
"SL trả" = `qty` (SL yêu cầu); kho chỉ nhập thật `imported_qty` = 0 (PNK-12995 thực nhập 0) → BC đúng. User chốt thêm cột
"SL duyệt trả" = số đã nhập kho thật để khỏi nhầm.

## Tasks
- [x] `show.blade.php` bảng loại 3 (nhập hàng mượn trả lại): thêm cột "SL duyệt trả" = `imported_qty` sau cột "SL trả"
- [ ] Kiểm màn thật
- [x] Commit/push develop_02 `1fdb613c36` + gop_db `1eb0070bc3` (27/11/2026)

### Checkpoint — 2026-11-27 17:18 (wrap up cuối ngày)
Vừa hoàn thành: Thêm cột SL duyệt trả (`show.blade.php`, type 3, `imported_qty`) ✓push develop_02 `1fdb613c36` + gop_db `1eb0070bc3`. Tra dữ liệu PYCNH-16898 / PNK-12995: MARA-P0190 thực nhận 0 → báo cáo đúng, không phải bug.
Đang làm dở: Kiểm màn thật.
Bước tiếp theo: QA kiểm trên dev-erp.
Blocked: Không
