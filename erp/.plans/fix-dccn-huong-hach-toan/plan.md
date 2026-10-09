# Fix chiều hạch toán "Điều chỉnh công nợ HĐ A → HĐ B" (KH & NCC)

**Goal:** Bút toán chuyển công nợ phải theo dấu số dư thực tế của HĐ "điều chỉnh từ" (A) lấy từ sổ (`account_details`), thay vì luôn cố định Nợ A / Có B.

## Bug

`BillAdjustDeptRequest` (customer + supplier builder) hard-code chiều: A(old)→Nợ, B(new)→Có. Chỉ đúng khi A **dư Có**. Khi A **dư Nợ** → ghi thêm Nợ cho A → **double dư Nợ của A** (và Có B sai chiều).

Đúng phải là:
- A dư Nợ → **Có A / Nợ B**
- A dư Có → **Nợ A / Có B**

## Bằng chứng (DB dev `dev_128`)

- PKT 347 (KH, request 278): HĐ A dư Nợ → phiếu vẫn ghi Nợ A → double.
- PKT 346 (NCC, request 279): PULI (supplier 11600, 3311) dư Nợ 515.569.507 → phiếu ghi Nợ A → thành 516.569.507 (double). `balance_old` NCC lưu ngược dấu so với sổ nên không tin được, phải tính từ `account_details`.

## Scope

- `app/Model/IncomeExpenditure/BillAdjustDeptRequest.php`
  - Thêm helper `adjustFromIsDebit()` — tính dấu số dư A từ `AccountDetail::getDeptAccount`.
  - `getDataForBillAdjustDeptCustomer` (1311) — đảo chiều theo dấu.
  - `getDataForBillAdjustDeptSupplier` nhánh **không báo cáo (else)** (3311) — đảo chiều theo dấu.
- **Ngoài scope lần này:** nhánh NCC có báo cáo (with-report) — chưa reproduce, chờ user xác nhận có dùng không.

## Sau khi fix code

- Hỏi user (Q3): có sửa lại 2 phiếu đã tạo sai trên dev (PKT 347, PKT 346) không. KHÔNG tự đụng data đã hạch toán.
- KHÔNG commit/push khi chưa được yêu cầu.

## Trạng thái
- [x] Xác định root cause + bằng chứng DB
- [x] Sửa code (helper `adjustFromIsDebit` + KH builder + NCC else builder)
- [x] `php -l` — no syntax errors
- [x] Verify downstream an toàn (type dùng truthiness, validateDetails cân, money_adjusted/total_amount không đổi)
- [x] Hỏi user về data 2 phiếu dev đã sai (PKT 347, 346) — user chuyển sang xử lý phiếu prod
- [x] **Prod**: sửa PKT 13766 (req 7336) — NCC 34, HĐ A=BuyDebtContractBeginning 87, HĐ B=InlandBuyContractNew 1133, 77.22M
  - Trước: Nợ A/Có B → A dư Nợ 154.44M (double). Sau: Có A/Nợ B → A=0, B=-180.18M. total_amount giữ 77.22M
  - account_details 1078375 (type 1→2), 1078376 (type 2→1); bill_adjust_dept_details 36339/36340 đảo dept↔has
