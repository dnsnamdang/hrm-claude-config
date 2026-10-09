# Task P2-5 Report — BorrowSellPostingService: nhánh WrServiceContract (HĐ dịch vụ)

## Status: DONE

## Commit
- `4ddb4cd1a` — `feat(finance): bổ sung nhánh hạch toán HĐ dịch vụ (WrServiceContract) cho BorrowSellPostingService`

## Files đổi
**Sửa:**
- `Modules/Finance/Services/BorrowSell/BorrowSellPostingService.php`
  - Thêm import `WrServiceContract`, `WrSupportAccounting`
  - Thêm const `WORK_CHIET_KHAU = 20`
  - `getDataAccounting()`: thay nhánh trả lỗi tạm bằng resolve HĐ dịch vụ + gọi `wrServiceBranch`
  - `resolveContract()`: rẽ nhánh theo `contractable_type` (Firm giữ nguyên logic cũ, thêm nhánh WrService)
  - `postAccounting()`: bỏ điều kiện chỉ resolve cho FIRM → resolve cả 2 loại để lấy meta HĐ
  - Thêm `wrServiceBranch()` — port 5 block (doanh thu, chiết khấu, giảm trừ doanh thu, giá vốn, cụm hỗ trợ)
  - Thêm `costAccountingWrService()` — giá vốn 1561, CÓ nhân `unit_coefficient`
  - Cập nhật docblock class (bỏ ghi chú "Task 5 chưa hỗ trợ")
- `Modules/Assign/Services/Accounting/SupportAccountingTrait.php`
  - `monthlyAndQuarterlyCommissionAccounting` + `riskFundAccounting`: thêm điều kiện `$contractCompanyId !== null &&` trước so sánh company — khi `null` thì không lọc company (dùng cho nhánh WrService)

**Tạo mới (4 entity mirror)** trong `Modules/Finance/Entities/Contract/`:
- `WrSupportAccounting.php` (bảng `wr_support_accounting`, 2 accessor alias `bonus_contract_before_vat` ← `contract_performance_bonus_before_vat`, `tndn_vat` ← `personal_income_tax`)
- `WrSupportAccountingDepartment.php` (bảng `wr_support_accounting_departments`)
- `WrSupportAccountingEmployee.php` (bảng `wr_support_accounting_employees`)
- `WrSupportAccountingDepartmentDetail.php` (bảng `wr_support_accounting_department_details`)

**Test:**
- `Modules/Finance/Tests/Feature/BorrowSellPostingWrServiceTest.php` (mới)

Toàn bộ đúng nguyên văn theo brief — không có điểm lệch.

## Cách chọn contract fixture

Query trên `erp_hrm_check`:
```sql
SELECT wsa.contractable_id AS wr_id, wsa.id AS sa_id, wsad.department_id, d.department_lead_id, wsad.is_main
FROM wr_support_accounting wsa
JOIN wr_support_accounting_departments wsad ON wsad.wr_support_accounting_id = wsa.id AND wsad.is_main = 1
JOIN departments d ON d.id = wsad.department_id
WHERE wsa.contractable_type='App\\Model\\Customers\\WrServiceContract'
  AND d.department_lead_id IS NOT NULL
ORDER BY wsa.contractable_id LIMIT 10;
```

Chọn **`wr_service_contracts.id = 4`** (mã `HDDV_TPE_HN_KDTM_25_0001_NAT- NGUYỄN XIỂN`):
- `wr_support_accounting.id = 1`: `before_vat_total=969300`, `before_vat_other_cost=0`, `before_vat_delivery_cost=0`, `before_vat_product=0`, `before_vat_repair=969300`, `contract_performance_bonus_before_vat=9000`, `personal_income_tax=0`
- Phòng chính (`is_main=1`): `department_id=47`, `department_lead_id=96`
- Nhân viên: `employee_id=808`, `part_id=NULL`, `commission_sale_percent=100`

Chọn id=4 (không dùng gợi ý id=139 trong brief) vì đơn giản, đủ điều kiện trưởng phòng và có `bonus > 0` để test được cụm thưởng HĐ (assert #7 khuyến khích trong brief).

Gợi ý id=139 trong brief KHÔNG dùng vì id=4 đã thoả đủ điều kiện ngay từ query đầu tiên, không cần dò tiếp.

## Giá trị bút toán thực tế (từ test)

Fixture: 1 SP `price=1000000, extra_price=0, allocated_price=0, rebate_price=100000, qty=10, unit_coefficient=5, export_price=900000, vat_percent=10`; header `sum_amount_after_extra=10000000, sum_amount_after_extra_vat=1000000`.

- **Giá vốn**: Có 1561 = Nợ 632 = `900000 × 10 × 5 = 45.000.000` (đúng CÓ nhân coefficient, ngược nhánh Firm)
- **Chiết khấu**: Nợ 5211 (work CKHH=20) = `100000 × 10 = 1.000.000`
- **Cân Nợ/Có**: tổng type=1 (Nợ) = tổng type=2 (Có), delta < 1.0
- **Thưởng HĐ**: có phát sinh bút toán 5211 work TTHHD=12 (accessor alias `bonus_contract_before_vat` từ `contract_performance_bonus_before_vat=9000` hoạt động đúng — không throw lỗi thiếu HTHT/trưởng phòng)

Test: `php vendor/bin/phpunit --filter=BorrowSellPostingWrServiceTest Modules/Finance/Tests/Feature/BorrowSellPostingWrServiceTest.php`
→ **OK (1 test, 8 assertions)**

Regression check (không sửa logic nhưng đụng file dùng chung):
- `BorrowSellPostingFirmTest` (Task 4, nhánh Firm) → OK (1 test, 6 assertions), không đổi hành vi
- `ProductExportPostingRegressionTest` (Assign module, cũng dùng `SupportAccountingTrait` qua `ProductExportPostingService`, luôn truyền company_id thật nên nhánh `null` mới thêm không kích hoạt) → OK (1 test, 2 assertions), snapshot sumDept=sumHas=80543085 không đổi

## Điểm lệch so với brief
Không có. Mọi tên cột, hằng số, method signature, giá trị test dùng nguyên văn theo brief. Chỉ khác 1 chi tiết không ảnh hưởng kết quả: dùng `wr_service_contracts.id=4` thay vì gợi ý `id=139` (vì id=4 đã thoả điều kiện ngay từ query đầu, không cần dò thêm).

## Concerns
Không có.
