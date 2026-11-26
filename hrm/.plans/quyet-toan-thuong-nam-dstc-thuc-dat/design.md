# Design — Quyết toán thưởng năm (DSTC): "DSTC phòng thực đạt trong năm" lấy sai nguồn (HRM)

Redmine **#10651**. Fix **cả 2 bên**. Bản ERP (gốc trace + verify dữ liệu): `ERP/.plans/quyet-toan-thuong-nam-dstc-thuc-dat/design.md` — đọc kèm.

HRM **port 1:1 ERP**, cùng gốc rễ, cùng công thức. Tài liệu này chỉ ghi phần KHÁC bên HRM.

## Gốc rễ (HRM)

`Modules\Finance\Services\BonusEndYearSettlement\BonusEndYearSettlementService::getActualRevenue()`
(dòng 69-96) — port 1:1 logic SAI của ERP: `Σ(Có) − Σ(Nợ)` `money_value_exchange` trên TK
`511/5211/5212/5213` (+ con) từ `AccountDetail`, lọc `employee_department_id` + `invoiceable_date_accounting`.

Dùng helper HRM: `Account::selfAndChildIds()`, `AccountDetail::TYPE_HAS`/`TYPE_DEBT`,
`normalizeToIso()` (nhận cả d/m/Y và Y-m-d), `toNumber()`. Const `REVENUE_ACCOUNT_NUMBERS`.

## Công thức MỚI (giống ERP)

```
SUM(settlement_contract_departments.commission_sale)
  JOIN firm_settlement_contract_detail fscd  ON fscd.id = scd.firm_settlement_contract_detail_id
  JOIN settlement_contracts sc               ON sc.id  = fscd.settlement_contract_id
WHERE fscd.type = 2
  AND scd.contractable_type = 'App\Model\Sale\Firm\Contract\FirmContract'
  AND scd.department_id = :departmentId
  AND sc.date_accounting BETWEEN :from AND :to
```

## Lưu ý riêng HRM

1. **`contractable_type` LUÔN là chuỗi lớp ERP** kể cả bản ghi do HRM tạo: `FinanceServiceProvider::registerMorphMap()`
   map KEY = `'App\Model\Sale\Firm\Contract\FirmContract'` → `FinanceContract\FirmContract::class`.
   morphMap lưu KEY vào cột → query bằng **chuỗi literal** `'App\Model\Sale\Firm\Contract\FirmContract'`
   là đúng cho mọi bản ghi. KHÔNG dùng `FirmContract::class` của HRM (ra chuỗi khác → 0 dòng).
2. **Giữ `normalizeToIso()`** cho tham số ngày (FE HRM gửi d/m/Y). Dùng query builder
   `DB::table(...)` hoặc Eloquent — chọn cách khớp phong cách file.
3. **2 nơi gọi** `getActualRevenue`: `calculateDepartmentDetail` (dòng 142) + `recomputeDetailForSave`
   (dòng 201). Cả 2 chỉ cần con số → sửa 1 hàm, cả 2 hưởng.
4. **Const `REVENUE_ACCOUNT_NUMBERS`** thành code chết sau khi sửa → xóa luôn (kèm import `Account`,
   `AccountDetail` nếu không nơi khác trong file dùng).
5. "Theo công ty": hàm này lọc theo `department_id` (phòng), KHÔNG cần `CurrentCompany::id()` —
   nguồn quyết toán đã gắn phòng; giữ nguyên chữ ký, không thêm lọc công ty (bám ERP).

## Verify

- Đọc code + `php -l`. Chạy local (skill `run-hrm`), đối chiếu ô "DSTC phòng thực đạt trong năm"
  trên màn Quyết toán thưởng năm (loại DSTC) với số ERP đã tính (dept=55, 2025 = 9,163,656,207.80)
  qua tinker/endpoint.
- Quỹ thưởng 1%/0.9 (`BonusEndYearSettlementCalculator::bonusFundDstc`) + DSTC đăng ký đầu năm
  KHÔNG đụng.
