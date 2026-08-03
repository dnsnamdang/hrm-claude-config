# Lập HĐ hãng từ báo giá HRM theo 2 cấp (cha-con)

> Cross-system (ERP + HRM). Repo chính: **ERP**. Cặp HRM: `HRM/.plans/lap-hd-hang-tu-bao-gia-hrm-2-cap/`.
> Nhánh ERP: làm trên nhánh đã merge `sync_quotation` (= HRM-quotation→contract + cha-con).

## 1. Mục tiêu
Khi lập HĐ hãng ERP **từ báo giá HRM**, giữ nguyên cấu trúc hàng hoá **2 cấp (cha-con)** thay vì import phẳng như hiện tại. Sau import, HĐ ERP có cha-con hoạt động y hệt HĐ cha-con lập tay (xuất hàng, quỹ, VAT, quyết toán tái dùng toàn bộ logic feature `bao-gia-hop-dong-hang-cha-con`).

## 2. Nguyên tắc
- Mirror đúng luồng "báo giá → HĐ" ERP hiện có; **quy tắc sửa/khoá field y nguyên** (không đặt luật mới).
- **DB KHÔNG đổi** — cột cha-con đã có sẵn cả 2 phía.
- Tách bạch: `child_ratio` là khái niệm của ERP → **ERP tự tính**, HRM chỉ lộ `parent_id`.

## 3. Hiện trạng (nguồn gốc vấn đề)
- HRM `quotation_product_prices` có sẵn: `id`, `parent_id` (cha-con), `product_type`, `qty_needed`, `quoted_price`, `vat_percent`, `erp_product_id`, `quotation_group_id`... **Không có cột `ratio`.**
- Tổng tiền báo giá HRM (`QuotationController` ~dòng 855–860) **đã loại hàng con** (`if parent_id continue`), chỉ tính `cha: qty × quoted_price`. → Khớp convention ERP (con thành tiền=0).
- Endpoint ERP gọi (`QuotationController::erpContractData`, ~dòng 557–564) **đang strip cha-con** — select không có `parent_id`/`product_type` → ERP nhận phẳng.
- ERP `HrmQuotationContractController::getDataForContract` map phẳng, gom tab theo `quotation_group_id`.
- ERP form cha-con (đã merge): mỗi dòng có `tmp_row_id`, `is_child`, `child_parent_tmp_id` (trỏ `tmp_row_id` cha), `child_ratio`; FE ép mọi cột tiền của con = 0; store map `tmp_row_id`→id thật để set `child_parent_id` (`FirmContractService` ~dòng 877–883, 1173–1181).

## 4. Thay đổi phía HRM (hrm-api) — TỐI THIỂU
`Modules/Assign/Http/Controllers/Api/V1/QuotationController.php` → `erpContractData()`: thêm **`parent_id`, `product_type`** vào `QuotationProductPrice::...->get([...])` (đã có sẵn `id`). Không đổi gì khác (tổng tiền HRM vốn đã loại con).

## 5. Thay đổi phía ERP (chính)
- `app/Services/Hrm/HrmApiService.php`: **KHÔNG đổi** (passthrough raw `products` → `parent_id` tự chảy qua).
- `app/Http/Controllers/Sale/Firm/HrmQuotationContractController.php` → `getDataForContract()`: bổ sung dựng cha-con khi map mỗi dòng:

| Field form | Giá trị |
|------------|---------|
| `tmp_row_id` | `(string) hrm.id` (ổn định, unique trong báo giá) |
| `is_child` | `!empty(hrm.parent_id)` |
| `child_parent_tmp_id` | nếu con: `(string) hrm.parent_id` (khớp `tmp_row_id` của cha) |
| `child_ratio` | nếu con: `con.quantity / cha.quantity` (cha = dòng có `id == hrm.parent_id`) |
| `total_cost` | cha: `quantity × price` (giữ nguyên); **con: 0** |

  - **Tab grouping:** con luôn gom vào **tab của cha** (nếu `quotation_group_id` của con lệch cha → ép theo cha).
  - `grandTotal` tự đúng (con total=0 → chỉ tính cha).
- Lưu HĐ + render form + xuất hàng/quỹ cha-con: **KHÔNG đổi** (tái dùng logic đã merge).

## 6. Luồng dữ liệu
HRM `erpContractData` (kèm `parent_id`/`product_type`) → ERP `HrmApiService::contractData` (passthrough) → `getDataForContract` (dựng cha-con + prefill KH/SP) → form cha-con (hiện ⌊ con + tỉ lệ, tiền con=0, sửa theo luật cũ) → `store` → `firm_contract_tab_products` có `child_parent_id`+`child_ratio` → `markContractCreated` ghi ngược HRM (`erp_firm_contract_id`).

## 7. Edge cases
- **Con không map được product ERP / `parent_id` trỏ dòng không có trong set (mồ côi):** coi như dòng thường (`is_child=false`). Gate eligibility ("chưa đồng bộ hết hàng") chặn trước.
- **Con khác nhóm cha:** ép con vào tab cha.
- **Tỉ lệ lẻ** (SL không chia hết): `child_ratio` để thập phân (cột float) — chấp nhận.
- **Báo giá direct (không qua BOM):** vẫn chạy — dựng cha-con từ `parent_id` của báo giá, không phụ thuộc BOM.
- **Cha SL = 0:** không chia (tránh /0) → `child_ratio = 0` + log; thực tế cha luôn > 0 vì eligibility.

## 8. Downstream impact
- Xuất hàng / quỹ / VAT / quyết toán cha-con: **không phát sinh mới** — HĐ import ra giống HĐ cha-con lập tay nên dùng chung mọi luồng đã test (gồm cả fix ycldbg quỹ nếu nhánh có).
- Không đụng luồng import phẳng cũ (báo giá HRM không cha-con vẫn chạy y như trước).

## 9. Test
- (a) Báo giá HRM **phẳng** → import như cũ (không regression).
- (b) Báo giá **cha-con** → HĐ ra đúng cấu trúc: con indent, `child_ratio` đúng = con.qty/cha.qty, tiền con=0, tổng HĐ = Σ cha.
- (c) Cha-con + **nhóm lệch** → con vẫn vào tab cha.
- (d) Báo giá **direct** (không BOM) cha-con → chạy.
- (e) Lưu HĐ xong: DB `firm_contract_tab_products` có `child_parent_id`/`child_ratio` khớp; mở lại HĐ form hiện đúng cha-con; thử **xuất hàng** 1 cụm cha-con → quỹ trừ đúng.

## 10. Out of scope
- Không thêm cột ratio bên HRM (suy ra ở ERP).
- Không sửa cách HRM tính tổng/giảm giá/VAT.
- Không đổi DB 2 phía.
