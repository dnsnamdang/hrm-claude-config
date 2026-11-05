# Kết chuyển chi phí phải trả — port ERP → HRM

Nguồn ERP: `ClosingEntryController`, `Model/Accounting/ClosingEntry`, `Jobs/SaveAdClosingEntry`, view `accounting/closing_entries/*`.
Menu ERP: Kế toán → Kết chuyển cuối kỳ → Kết chuyển chi phí phải trả (`closing_entries.index`).
HRM: phân hệ Tài chính (permissionType 8), route FE `/finance/closing-entries`, API `/api/v1/finance/closing-entries`.
Nhánh `feature/ket-chuyen-chi-phi-phai-tra` (worktree `.worktrees/hrm-{api,client}-kccppt`). User: "cứ làm đi" — bỏ hỏi đáp.

## Bảng dữ liệu (dùng chung ERP, KHÔNG migration)
- `closing_entries`: code (unique), year varchar, to_date, date_accounting, note, sum_money_debt, created_by/updated_by NOT NULL, department_id NOT NULL, has_invoice.
- `closing_entry_details`: parent_id, work_id, debt_money.

## Quyền (guard api, tên y ERP, type 8, group "Kết chuyển chi phí phải trả")
- `Tạo kết chuyển chi phí phải trả` — gắn middleware POST store.
- `Xem kết chuyển chi phí phải trả theo tổng công ty` — xem tất cả.
- `Xem kết chuyển chi phí phải trả theo công ty` — phiếu có phòng ban thuộc công ty mình.
- Không có quyền xem → chỉ phiếu mình tạo. Super Admin xem tất cả.

## Danh sách
Cột: STT · Mã phiếu (link) · Đến ngày · Ngày hạch toán · Phòng ban · Số tiền kết chuyển · Người tạo · Ngày tạo · Hành động (Xem, Lịch sử).
Lọc: tìm nhanh mã phiếu; Phòng ban; Người tạo; Vụ việc (phiếu có dòng vụ việc đó); Số tiền từ–đến; Ngày tạo từ–đến.
Sort mặc định created_at desc. Xuất Excel (export-rows), Cấu hình cột. Không sửa/xoá/in (ERP không có).

## Form tạo (1 nút "Lưu và duyệt")
- Năm (bắt buộc, năm hiện tại−1 … +10, mặc định năm hiện tại) · Tính đến ngày (bắt buộc, không tương lai, cùng năm) · Ngày hạch toán (khoá, = Tính đến ngày) · Phòng ban (bắt buộc; quyền "theo công ty"/không quyền tổng → chỉ phòng công ty mình) · Ghi chú. has_invoice luôn 1 (hiện ở chi tiết dạng chỉ đọc "Có hóa đơn").
- Bảng chi tiết: STT · Vụ việc (bắt buộc, không trùng) · TK nợ 3351 · TK có 33481 · Số tiền (chỉ đọc, BE tính) · xoá dòng (dòng đầu không xoá). Đổi năm/ngày/phòng → làm mới số tiền các dòng.
- BE validate: `Ngày đến không được chọn ngày tương lai` · `Ngày đến không trùng với năm được chọn` · `Số tiền kết chuyển phải khác 0` (BE tự tính lại số tiền, không tin FE).
- Lưu thành công → toast `Tạo kết chuyển thành công!` → về danh sách.

## Hạch toán (đồng bộ trong transaction — ERP chạy queue)
Mỗi dòng vụ việc: gom `account_details` TK 117(3351), employee/contract not null, employee_department_id = phòng, năm(invoiceable_date_accounting)=year, ngày ≤ to_date, HĐ FirmContract/WrServiceContract has_invoice=1; amount = Σ(type2 ? +v : −v) theo (HĐ, NV).
- Mỗi nhóm: dòng 3351 Nợ nếu amount>0 ngược lại Có, |amount| làm tròn, mang work/NV/HĐ, employee_department_id=phòng, employee_company_id=cty phòng, contract_id=contractable_id.
- Mỗi (NV, vụ việc): 1 dòng 33481 Có nếu Σ>0 ngược lại Nợ.
- company_id/department_id = của người tạo; created_by NULL (y ERP); currency 1, tỷ giá 1, group 1; bỏ dòng làm tròn = 0.
- refs: dòng 117 → ref 116, dòng khác → ref 117.
- invoiceable_type `App\Model\Accounting\ClosingEntry`.

## Quyết định đã chốt (của mình — user giao)
- Sửa bug ERP: lọc năm/ngày hạch toán ERP lọc sai cột → HRM không port 2 ô lọc đó (ERP UI cũng không có ô); thiếu rollBack → HRM transaction đầy đủ; hạch toán đồng bộ.
- Mã phiếu `{mã cty}.KCCPPT{năm}.NNNNN`.
- "Theo công ty" = phòng ban thuộc `company_id` người đăng nhập.
