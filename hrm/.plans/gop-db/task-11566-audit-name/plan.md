# Plan — #11566 Người tạo/cập nhật + thứ tự cột + mã max 50

Lệnh phạm vi (skill new-screens-sweep, `S=.claude/skills/new-screens-sweep/inventory.py`, `R=worktrees/gop_db-client`):
- YC1: `python3 $S --root $R --kind list --has "Người tạo|Người cập nhật|Người sửa" --be` (139 file) + popup chọn phiếu trong `--kind table`
- YC2: `python3 $S --root $R --kind list --has "Người tạo|Người cập nhật" --lacks "columnCustomizationMixin|column-customizations"` (10 file, kiểm tay)
- YC3: `python3 $S --root $R --kind form --has 'v-model="[\w.]*\.code"' --lacks "max:\s*\d+|maxlength"` (25 file)

## Phase 1 — Gốc BE
- [x] BE: helper `employeeAuditLabel()` (FormatHelper) — "Tên - Mã phòng"
- [x] BE: BaseModel `cachedEmployeeName` + 4 accessor dùng helper; entity tự override accessor cũng đổi theo (Assign 4 + BaseCatalogModel; Decision = màn cũ, giữ nguyên)
- [x] FE: util `employeeAuditText()` trong utils/employeeOptionText.js
- [x] Màn mẫu: BillIncomeListResource + BillIncomeService (eager-load .info.department)

## Phase 2 — Từng màn
- [x] BE+FE YC1 (145 file = 139 list + 6 popup chọn phiếu, 8 lô song song) — ~190 file BE, FE chỉ DeclareDebtContractPicker: Resource/Service của màn mới tự ghép fullname người tạo/cập nhật → helper (chia lô theo phân hệ)
- [x] FE YC2: rà 10 danh sách không tuỳ chỉnh cột — KHÔNG file nào có cột người cập nhật → không có cặp sai thứ tự, 0 thay đổi
- [x] FE+BE YC3 (31 file rà, 10 FE + 13 BE sửa; mọi ô mã user nhập = 50): ô mã user nhập thêm max 50 + rule FormRequest

- [x] YC1 bổ sung: 7 màn nhãn khác (Người lập/đề xuất/yêu cầu) + ChildQuotationResource + PricingRequest "Người yêu cầu" — sót do lệnh phạm vi chỉ lọc nhãn

## Phase 3 — Verify
- [x] php -l 202 file BE sạch · 13 file FE parse sạch (vue-template-compiler + babel) · diff toàn file đúng chủ đề, không nhiễu EOL
- [x] Rà ngược BE: List Resource còn tự ghép fullname chỉ còn Detail/Print (ngoài phạm vi) + Payroll (màn cũ)
- [x] Remote gop_db +20/+14 commit: không trùng file; màn mới (sale/prepick-tracking) không có cột người tạo
- [ ] Test tay / Playwright — chờ user yêu cầu
- [x] User chốt 03/10: Mã vụ việc/Mã phí/Mã ngân hàng về 50 — FormRequest + popup FE + import BE + ô thêm nhanh Phiếu xuất (DB hiện max 8/9/11 ký tự, không chặn bản ghi cũ)

### Checkpoint — 2026-10-03
Vừa hoàn thành: YC1 (154 màn: 145 + 7 nhãn khác + 2 bảng con dự án/giá), YC2 (0 thay đổi), YC3 (mã max 50).
Đang làm dở: chưa commit — 202 file BE + 13 file FE trong worktrees/gop_db-api|client.
Bước tiếp theo: user review → test → commit/push khi được phép.
Blocked: 
