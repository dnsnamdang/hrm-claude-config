# Design — Quyết toán thưởng năm (DSTC): "DSTC phòng thực đạt trong năm" lấy sai nguồn

Redmine **#10651**. Fix **cả 2 bên** (ERP + HRM). Bản HRM: `HRM/.plans/quyet-toan-thuong-nam-dstc-thuc-dat/`.

## Hiện trạng / Triệu chứng

Màn **Quyết toán thưởng năm**, loại quyết toán **Doanh số tiêu chuẩn (DSTC)**: ô
**"DSTC phòng thực đạt trong năm"** (cột `actual_revenue`) đang tính **SAI nguồn** so với spec #10651.

Theo #10651: ô này phải = tổng **DS tiêu chuẩn** của các **HĐ đã quyết toán** có **ngày hạch toán
nằm trong khoảng [từ ngày, đến ngày]** đã chọn — tức lấy từ **"DSTC tính thưởng năng suất quý"**
(BC tổng hợp thu nhập từ bán hàng).

## Gốc rễ (ĐÃ trace tới tận hàm — giống hệt 2 bên, HRM port 1:1 ERP)

- ERP: `App\Services\Accounting\BonusEndYearSettlementService::getActualRevenue()` (dòng 32-69).
- HRM: `Modules\Finance\Services\BonusEndYearSettlement\BonusEndYearSettlementService::getActualRevenue()` (dòng 69-96).

Logic hiện tại (SAI): lấy `Σ(Có type=2) − Σ(Nợ type=1)` cột `money_value_exchange` trên các TK
`511/5211/5212/5213` + TK con (qua `identify_number_parent`), từ bảng `account_details`, lọc theo
`employee_department_id` + `invoiceable_date_accounting ∈ [từ, đến]`.
→ Đây là **phát sinh thô trên TK doanh thu**, KHÔNG phải DS tiêu chuẩn đã quyết toán.

## Nguồn ĐÚNG (đối chiếu với báo cáo chuẩn + dữ liệu thật)

Báo cáo chuẩn nêu trong spec = `App\Services\Reports\CommissionSettlementQuarterReportService`
(subquery `settlement_firm`, dòng 84-116). Cột "DSTC" ở đó = `settlement_contract_employees.commission_sale`,
lấy từ chuỗi bảng quyết toán:

```
settlement_contract_departments (scd)
  └─ firm_settlement_contract_detail (fscd)  [fscd.type = 2 = đã quyết toán thực tế]
      └─ settlement_contracts (sc)           [sc.date_accounting = ngày hạch toán phiếu QT]
```

**Công thức MỚI của `getActualRevenue($departmentId, $dateFrom, $dateTo)`:**

```sql
SELECT SUM(scd.commission_sale)
FROM settlement_contract_departments scd
JOIN firm_settlement_contract_detail fscd ON fscd.id = scd.firm_settlement_contract_detail_id
JOIN settlement_contracts sc              ON sc.id  = fscd.settlement_contract_id
WHERE fscd.type = 2                                   -- đã quyết toán (actual)
  AND scd.contractable_type = 'App\Model\Sale\Firm\Contract\FirmContract'
  AND scd.department_id = :departmentId
  AND sc.date_accounting BETWEEN :from AND :to        -- ngày hạch toán ∈ [từ, đến]
```

- JOIN tới `settlement_contracts` qua `fscd.settlement_contract_id` đã tương đương điều kiện
  "đã quyết toán" (`whereNotNull('settlement_contract_id')`) của báo cáo chuẩn.
- Dùng `scd.commission_sale` (cấp phòng) thay vì `Σ sce.commission_sale` (cấp NV) vì **bằng nhau**
  (verify dưới) và gọn hơn, 1 dòng / (HĐ × phòng).

## Vì sao nguồn mới đã bao gồm đủ các yêu cầu nghiệp vụ

- **Hệ số DSTC**: đã bake vào `standard_price` → `commission_sale` ngay lúc LẬP hợp đồng
  (`FirmContractService.php:726-731`), KHÔNG nhân lại ở tầng báo cáo/quyết toán → dùng
  `commission_sale` là đã gồm hệ số.
- **HĐ phối hợp**: đã chia sẵn ở tầng quyết toán — mỗi phòng tham gia có 1 dòng `scd` với phần
  `commission_sale` được ghi nhận riêng (theo `commission_sale_percent`). Tổng theo `department_id`
  tự gồm đúng phần phối hợp.
- **Nhập trả lại**: nằm trong số liệu quyết toán của HĐ, không cần cộng/trừ thêm.

## Verify bằng dữ liệu thật (DB gộp `erp_hrm_check`, 2026-11-26)

- `scd.contractable_type` thật = `App\Model\Sale\Firm\Contract\FirmContract` (có thư mục `Contract\`);
  WR dùng `App\Model\Customers\WrServiceContract` và có `firm_settlement_contract_detail_id = NULL`
  → **tự loại** khi JOIN qua `firm_settlement_contract_detail`.
- `fscd.type` phân bố 1/2/3 mỗi loại 24,291 dòng. Lọc `type=2` = bản quyết toán thực tế.
- `scd.commission_sale == SUM(sce.commission_sale)` ở **mọi** mẫu kiểm (10/10 khớp).
- 12,061 dòng Firm đã quyết toán, tổng `scd.commission_sale` ≈ 409,388,614,930. Lọc 1 phòng + năm
  2025 (dept=55) ra 9,163,656,207.80 → công thức + lọc ngày chạy đúng.

## Quyết định đã chốt

1. **Phạm vi HĐ = CHỈ HĐ hãng (Firm)** (`contractable_type = App\Model\Sale\Firm\Contract\FirmContract`).
   Lý do: spec #10651 nêu đích danh nguồn là "BC tổng hợp thu nhập từ bán hàng", mà cột DSTC của báo
   cáo đó chỉ tính HĐ Firm. WR (`WrServiceContract`) KHÔNG có `firm_settlement_contract_detail` nên
   không mang DS tiêu chuẩn Firm. Nếu sau QA muốn gộp WR → mở rộng là union thêm nhánh WR (đảo ngược
   được). Bám chuẩn báo cáo nguồn là lựa chọn an toàn nhất hiện tại.
2. **Cột lọc ngày = `settlement_contracts.date_accounting`** (ngày hạch toán phiếu quyết toán),
   `BETWEEN [từ, đến]`. **Lưu ý chủ đích lệch báo cáo chuẩn**: báo cáo quý cố ý BỎ lọc `sc.date_accounting`
   ("Hướng A", comment `CommissionSettlementQuarterReportService.php:111-113`), nhưng spec #10651 dòng 55
   của màn thưởng năm **bắt buộc** lọc theo ngày hạch toán trong khoảng → fix NÀY có lọc ngày.
3. **Các phần KHÁC giữ nguyên (đã đúng):**
   - `getRegisteredRevenue` (DSTC đăng ký đầu năm) = `Σ sales_department_plans.standard_sale` where `status=3`.
   - Quỹ thưởng 1% / 1%×90% (`calculateBonusFundDSTC`). Không đụng.

## Phạm vi ảnh hưởng (an toàn)

`getActualRevenue` chỉ được gọi bởi `calculateDepartmentDetail()` (ERP) cho `TYPE_DSTC`
(và thêm `recomputeDetailForSave()` bên HRM). Chữ ký hàm KHÔNG đổi → không ảnh hưởng nơi gọi khác.
