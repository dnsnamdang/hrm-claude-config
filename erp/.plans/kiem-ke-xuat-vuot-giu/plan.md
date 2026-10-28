# Plan — Kiểm kê xuất vượt lớp hàng giữ

Nhánh: `gop_db`. DB: `hrm_erp_gop` (remote). Xem `design.md` cho bối cảnh + quyết định B/C/E.

## Phase B — Fix data: giải phóng 2 phiếu giữ (lập phiếu hủy giữ chuẩn)

- [x] **B1.** Baseline: ghi lại số trước fix — `prepick_details` SP 34686 (pd64272=1, pd69600=1), "tồn có
  thể bán" = −2.
- [x] **B2.** Viết `\Database\Seeds\UpdateDB::releaseHeldStockProduct34686_20261016()`:
  - Với MỖI hold (A: emp298/kh34023; B: emp744/kh39155):
    - Tạo `PrepickCancelRequest` (PYCHHG): `company_id=4`, `department_id`/`part_id` theo emp tạo giữ,
      `customer_id`, `created_by` = employee của hold, `status=1`, `approver_id`+`approved_time` (thủ công),
      `note` ghi rõ "Giải phóng giữ treo trên tồn 0 — sự cố SP 34686 (kiểm kê PXHĐCKK-00066)". `generateCode()`.
    - `syncProducts([['product_id'=>34686,'unit_id'=>41,'qty'=>1,'need_cancel'=>'true']])` → tạo
      `PrepickCancelRequestDetail` (need_cancel=1).
    - Tạo `PrepickCancel` (PHHG): `prepick_cancel_request_id`, `customer_id`, `status=1`, `company_id=4`,
      `created_by`, `note`. `generateCode()`.
    - `validateProducts($products)` → phải `true` (prepick_qty≥1).
    - `syncProducts($products)` → `PrepickCancelDetail` cancel_qty=1.
    - `updateWarehouse()` → trừ `prepick_details` về 0 + ghi `prepick_logs` (objectable=PrepickCancel).
  - Có cờ `$dryRun` in ra dự kiến (không ghi) để kiểm trước.
  - ⚠️ Fix tinker: `validateProducts` không truyền `company_id`, dựa `Auth::user()->info->company_id` → thêm
    `\Auth::login(Employee::find($hold.employee_id))` trong seeder (đúng nghiệp vụ: NV tự hủy giữ của mình).
- [x] **B3.** Chạy **dry-run** qua tinker — OK: 2 PYCHHG + 2 PHHG, pd64272/pd69600 → 0, validateProducts qua.
- [x] **B4.** Chạy **thật** (2026-10-16). Verify ĐÃ ĐẠT:
  - `prepick_details` pd64272=0, pd69600=0; không còn hold SP 34686 qty>0 (cnt=0).
  - `prepick_logs` 2 dòng change=−1 objectable_type=PrepickCancel (pd 64272 + 69600).
  - Chứng từ: PYCHHG-04592/04593 + PHHG-04524/04525, status=1. Tồn có thể bán = 0−0−0−0 = **0** (hết −2).

## Phase C — Fix code: guard cộng tổng theo sản phẩm (chặn cứng, 2 controller)

- [x] **C1.** `InventoryExportsController::validateAccountingWarehouse` (dòng 331): gom tổng qty các dòng
  cùng `(product_id, accounting_warehouse_id, unit_id, customer_id)` rồi so 1 lần với `in_stock`. (Thêm
  customer_id vào khóa — ruling: in_stock phụ thuộc prepick/hold theo khách, cần tính nhất quán mỗi nhóm.)
  Vượt → `[false, 'Kho ...: Số lượng xuất không được vượt quá số lượng được xuất!']`.
- [x] **C2.** `WarehouseInventoryExportsController::validateAccountingStock` (dòng 370): gom tổng qty theo
  `(product_id, company_id, unit_id)` rồi so 1 lần với `in_stock`. Giữ nguyên thông báo cũ.
- [x] **C3.** Verify mô phỏng (tinker, SP 8077 in_stock=10): C1 & C2 — 2 dòng ×6 = 12 > 10 → `false` (giữ
  thông báo); dòng đơn 8 ≤ 10 → `true`. (Trước fix per-row: mỗi dòng 6<10 lọt → tổng lọt.)

## Phase E — Fix code: chặn tại bước duyệt kiểm kê

- [x] **E1.** `WarehouseInventoryExportsController::approve` (dòng 286): sau `$object->save()`, khi
  `status==1` → dựng lại `$details` từ `$object->details` (map `product_id/unit_id/import_lot_id/qty`),
  gọi `validateAccountingStock($details, $object->warehouse_id)`; fail → `DB::rollBack()` +
  `$json->success=false; $json->message=$stockMessage` + **không** `updateWarehouse()`. Lint sạch.
- [x] **E2.** Verify tinker (login emp298, cty4):
  - Phiếu thật PXKĐCKK-00082 (1 chi tiết): map `$object->details` ra đúng format guard tiêu thụ được
    (đường mapping chạy thật, không lỗi).
  - SP 8077 (in_stock=10, lô 2417 cty4): 1 dòng ×8 ≤ 10 → TRUE (duyệt được); 2 dòng ×6 = 12 > 10
    (lỗ hổng per-row cũ) → FALSE, chặn tại bước duyệt với thông báo tồn không đủ.

## Final review
- [x] Review toàn bộ thay đổi code (fresh context reviewer) — **không có Critical/Important**. Xác nhận:
  C1/C2 gom nhóm đúng (không chặn oan, không lọt), E1 rollback + return sạch (không rò rỉ xuống
  updateWarehouse/Notification), đơn vị gom theo unit_id đúng, seeder B idempotent (`qty<=0 → continue`),
  không regression luồng xuất bình thường. 2 Minor (seeder: `catch` nuốt exception dòng 270 + `Auth::login`
  lưu session tinker dòng 218) → defer, đều là chủ ý của script chạy tay, không sửa.
- [x] Ghi memory root-cause (guard per-row không cộng tổng + kiểm kê không reconcile lớp giữ).
- [ ] KHÔNG commit/push khi chưa được yêu cầu. ← chờ user yêu cầu
