# Tính Thuế TNCN trong bảng lương

**Ngày:** 2026-05-13
**Owner:** @khoipv
**Spec chi tiết:** `docs/superpowers/specs/2026-05-13-personal-income-tax-design.md`

## Mục tiêu

Hoàn thiện logic tính Thuế TNCN trong flow tính bảng lương theo luật VN — áp biểu lũy tiến 7 bậc, tự động trừ vào tổng khấu trừ.

## Scope MVP

- Chỉ tính cho `employee_taxs.tax_type = 1` (Lũy tiến). Các loại khác trả 0.
- Trừ trước thuế: BHXH NLĐ + Công đoàn 1% + giảm trừ bản thân + giảm trừ NPT.
- `THUE_TNCN` (feature=2) tự cộng vào `total_deduction` — không sửa công thức `thuc_linh`.

## Các quyết định lớn

1. **Config thuế:** 2 bảng mới `tncn_tax_configs` + `tncn_tax_brackets`, theo ngày hiệu lực, cấp company.
2. **Người phụ thuộc:** Mở rộng `employee_relationships` với 3 cột `is_dependent`, `dependent_start_date`, `dependent_end_date`.
3. **BHXH NLĐ:** Tính trực tiếp từ `insurance_configs` × `insurance_salary` — không phụ thuộc thứ tự composition khác trong template.
4. **Công đoàn:** Thêm cột `union_fee_rate` (%) vào `tncn_tax_configs` (default 1%). Tính `insurance_salary × rate / 100` nếu `has_union=true`.
5. **UI config:** Section mới trong `pages/human/settings/index.vue`, pattern giống bảng BHXH (inline edit + ngày hiệu lực). Brackets ở modal riêng.
6. **UI người PT:** Bổ sung 3 trường trong tab Quan hệ thân nhân của màn nhân viên.

## Component chính

- BE: 4 migration + Entity/Service/Controller/Request CRUD `tncn_tax_config` + Helper `TaxCalculator` + inject vào `SalaryService::systemData()`.
- FE: Section "Cấu hình thuế TNCN" trong settings + bổ sung 3 trường người PT.

---

## Ví dụ minh họa — tính thuế cho NV "Nguyễn Thị Hải" (bảng lương #108, tháng 04/2026)

**Bối cảnh:**
- `apply_date = 2026-04-01`, `company_id = 4`
- NV không có row `employee_taxs` → mặc định Lũy tiến

### Dữ liệu đầu vào

**`employee_salary_histories` #70 (đang áp dụng từ 2024-01-01):**

| Phần lương | Số tiền | Cờ `*_tax` |
|---|---:|:---:|
| base_salary | 6.031.250 | p1_tax = 1 |
| p2_salary | 0 | p2_tax = 0 |
| p3_salary | 0 | p3_tax = 0 |
| seniority_salary | 0 | seniority_tax = 0 |
| moving_expenses | 5.000.000 | moving_expenses_tax = 1 |
| telephone_expenses | 4.468.750 | telephone_expenses_tax = 1 |
| other_allowances | 500.000 | other_allowances_tax = 1 |
| **has_insurance** | 1 | `insurance_salary = 6.031.250` |
| **has_union** | 1 | — |

**`insurance_configs` (company 4, date=2024-07-01):** tổng NLĐ = `worker_retire 8% + worker_sick 0% + worker_accident 0% + worker_unemployment 1% + worker_health 1.5%` = **10.5%**

**`tncn_tax_configs` (company 4):** `self_deduction = 11.000.000`, `dependent_deduction = 4.400.000`, `union_fee_rate = 1%`, brackets 7 bậc chuẩn luật VN.

**`employee_relationships`:** 1 NPT active cho 04/2026 (NGUYỄN MẠNH TUYẾN, `is_dependent=1`, `start=2026-03-01`, `end=2026-05-31`).

### Các bước tính

| Bước | Công thức | Kết quả |
|---|---|---:|
| B1 — Loại thuế | Không có `EmployeeTax` → mặc định Lũy tiến | tính tiếp |
| B2 — Thu nhập chịu thuế (Cách A) | 6.031.250 + 5.000.000 + 4.468.750 + 500.000 | **16.000.000** |
| B3 — Giảm trừ BHXH NLĐ | 6.031.250 × 10.5% | **633.281** |
| B4 — Pick TNCN config | company_id=4, date ≤ 2026-04-01 | OK |
| B5 — Giảm trừ công đoàn | 6.031.250 × 1% | **60.313** |
| B6 — Số NPT active | 1 (NGUYỄN MẠNH TUYẾN) | **1** |
| B7 — Thu nhập tính thuế | 16.000.000 − 633.281 − 60.313 − 11.000.000 − 4.400.000 × 1 | **−93.594** |
| B8 — Áp lũy tiến | ≤ 0 → return 0 | **0** |

### Kết quả: **Thuế TNCN = 0 VND**

NV này thu nhập gần đủ ngưỡng chịu thuế, chỉ cần thêm 1 NPT là đủ giảm trừ → không phải đóng thuế.

### Tác động đến các số liên quan trên bảng lương

Engine có sẵn của hệ thống tự cộng dồn — `TaxCalculator` không sửa công thức nào:

```
total_income     = 17.058.333   (Σ composition feature=1)
total_deduction  = 130.000      (QUY_CONG_DOAN 130.000 + 0 + 0 + THUE_TNCN 0)
advance          = 0
thuc_linh        = 16.928.333   = total_income − total_deduction − advance
```

### Bài học rút ra trong quá trình test

- **Self_deduction nhập sai** sẽ gây lệch lớn: ví dụ nhập 1.000.000 thay vì 11.000.000 → thuế nhảy lên 740.641 VND (cao gấp nhiều lần). UI hiển thị format số nhưng vẫn cần check kỹ khi sửa.
- **Insurance_configs phải có row cho company** — nếu thiếu thì BHXH = 0 (không trừ trước thuế), khiến thuế tính ra cao hơn thực tế.
- **Người phụ thuộc theo `dependent_start_date / dependent_end_date`** — phải nằm trong khoảng `apply_date` của kỳ lương. NPT đăng ký từ tháng sau sẽ không được tính cho kỳ trước.
