# Công nợ đầu kỳ — bổ sung bộ lọc Quá hạn + Ngày BGNT

## Mục tiêu
Màn `/admin/accounting/declare-debt-beginning` (Công nợ đầu kỳ theo KH - hợp đồng) bổ sung 2 bộ lọc:
1. **Quá hạn** — select 2 lựa chọn: Có / Không (map cột `is_overdue`).
2. **Ngày BGNT** (Bàn Giao Nghiệm Thu = `acceptance_handover_date`) — khoảng ngày: Từ ngày → Đến ngày.

## Hiện trạng
- List dùng helper `DATATABLE` (partial `partials/classes/base/Datatable.blade.php`) + mảng `search_columns`.
- Lọc chạy qua `DeclareDebtBeginning::searchByFilter($request)` (danh sách) và `searchByFilterExport($user, $request)` (in + xuất Excel).
- Đã có cột hiển thị `is_overdue` ("Quá hạn") và `acceptance_handover_date` ("Ngày BGNT").
- `search_type: 'date'` render 1 input `.date` (định dạng d/m/Y); `mergeSearch` gửi raw `.val()` → BE parse bằng `Carbon::createFromFormat('d/m/Y', ...)`.

## Quyết định
- Dùng `search_type: 'select'` cho Quá hạn với `column_data: [{id:1,name:'Có'},{id:0,name:'Không'}]`.
  BE phải phân biệt "0" (Không) với rỗng (không lọc) → check `!== ''`/`!== null`, KHÔNG dùng `if ($request->is_overdue)` (0 sẽ bị bỏ qua).
- Dùng 2 `search_type: 'date'` cho khoảng ngày BGNT: `acceptance_handover_from`, `acceptance_handover_to` (mirror pattern `money_from`/`money_to`).
- Áp cả 2 hàm `searchByFilter` + `searchByFilterExport` để danh sách/in/xuất Excel đồng bộ.
- Parse date theo convention repo: `Carbon::createFromFormat('d/m/Y', $val)->format('Y-m-d')` + `whereDate('acceptance_handover_date', '>=' / '<=')`.

## Không đụng
- Không đổi schema, không thêm quyền, không sửa hàm dùng chung (`Datatable.blade.php`).
