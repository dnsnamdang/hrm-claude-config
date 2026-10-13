# Task P2-4 — Review Report: BorrowSellPostingService nhánh FirmContract

Reviewer: subagent (code review), 2026-09-07. Base=2d4bbfe, Head=34fd294 (fe9c48f25 + fix 34fd294).

## Kết luận

- **SPEC: PASS** — tất cả yêu cầu brief đáp ứng đủ (shape, 6 const WORK_*, thứ tự 8 cụm, giá vốn 157, resolveContract, test TDD, commit 2 file).
- **QUALITY: APPROVED** — không có finding blocking. 2 finding non-blocking (theo dõi/khuyến nghị, không chặn merge).

## 1. resolveContract / shim Contract — ĐÚNG

Verify độc lập bằng SQL + đọc code (không chỉ tin report):

- `firm_contracts` (SHOW COLUMNS) có đủ **id, code, customer_id, created_by, company_id, department_id, part_id** — đúng tên cột mà `Modules\Assign\Entities\Contract\Contract` cần và trait đọc trực tiếp làm attribute thô (không qua accessor/relation nào khác ngoài `support_accounting`).
- `Contract::$guarded = []` → `new Contract($firm->getAttributes())` mass-assign toàn bộ cột `firm_contracts` an toàn (không bị chặn bởi fillable).
- Điểm mấu chốt: `Contract::support_accounting()` là `morphOne` với `contractable_type` mặc định = FQN `Contract::class`. Nếu để lazy-load, sẽ query sai (`contractable_type = 'Modules\Assign\Entities\Contract\Contract'` thay vì FQN FirmContract) → luôn null → toàn bộ firmBranch lỗi "chưa có HTHT". Code đã **chủ động `setRelation('support_accounting', $sa)`** với `$sa` tra đúng theo `(contractable_id=$firm->id, contractable_type=BorrowSell::CONTRACT_FIRM)` TRƯỚC khi bất kỳ method nào trong `firmBranch` chạm tới `$contract->support_accounting` → đúng, né được bẫy.
- Verify SQL: `firm_support_accounting` group by contractable_type cho ra đúng 2 loại (`FirmContract` 21403 dòng, `Contract` 2 dòng) — khớp báo cáo, không phải suy đoán.
- Meta ghi sổ (`postAccounting`): `contractable_id`/`contractable_type` lấy **thẳng từ `$bs->contractable_id/contractable_type`** (id HĐ hãng thật), KHÔNG dùng id của shim (shim thực ra CŨNG mang đúng id đó vì `getAttributes()` copy nguyên `id` từ `firm_contracts`, nhưng code không phụ thuộc vào điều này — dùng trực tiếp từ `$bs` là an toàn hơn, đúng ERP `BorrowSellsController@update`).
- 6 method cụm của trait chỉ đọc `customer_id/created_by/code/company_id/department_id` trên `$contract` dưới dạng attribute thô — tất cả đều tồn tại nguyên vẹn trên shim. Không phát hiện method/accessor nào trait gọi mà firm_contracts không đáp ứng.

## 2. Đúng đắn cụm hỗ trợ (đối chiếu ERP `FirmContractBorrowSellService`)

So khớp từng dòng với `getDataBorrowSellAccounting`/`prepareData` ERP (dòng 119-210):

| Cụm | ERP | HRM P2-4 | Khớp? |
|---|---|---|---|
| 1. Doanh thu | `revenueAccounting($borrow_sell->sum_amount_after_extra, $borrow_sell->sum_amount_after_extra_vat, $contract, ...)` | dùng thẳng `$bs->sum_amount_after_extra/_vat` (KHÔNG cộng dồn lại từ chi tiết) | Khớp — đúng vì ERP borrow_sell dùng thẳng cột header (khác `ProductExportPostingService::prepareData` phải cộng dồn do lý do khác, task đó không áp dụng ở đây) |
| 2. Giảm trừ | `$sale_invoice/_vat` từ `Σ(price+extra-allocated-rebate)×qty` + `×vat_percent/100` | công thức giống hệt (dòng 190-193) | Khớp |
| 3. Giá vốn | `export_price × qty`, KHÔNG nhân `unit_coefficient` (dòng 203) | đã fix ở 34fd294: `export_price × qty` | Khớp — xem mục 3 |
| 4/5. Thưởng HĐ + TNCN | `percent_export_without_delivery` truyền cho `bonusContractAccounting`/`vatExtraCostAccounting` | `pct_wo_delivery` (cùng công thức `intval($before_vat_not_include_delivery) ? amount/... : 0`) | Khớp |
| 6/7. HH tháng/quý | `percent_export_without_cost` | `pct_wo_cost` (cùng công thức `intval($before_vat) ? amount/... : 0`) | Khớp |
| 8. Quỹ rủi ro | `percent_export_without_cost` | `pct_wo_cost` | Khớp |
| Thứ tự gọi | 1→2→3→4→5→6+7→8 | y hệt | Khớp |
| company_id truyền cho cụm 6/7/8 | ERP gọi trait 4 tham số (không company_id) — nhưng đây là hàm base cũ; trait HRM (Task 3) đã đổi chữ ký thêm `$contractCompanyId` để lọc phòng theo công ty HĐ | P2-4 truyền `$contract->company_id` (từ shim = `firm_contracts.company_id` đúng) | Khớp với chữ ký trait hiện tại (đã chốt ở Task 3, không phải lỗi của P2-4) |

6 const `WORK_*` khai đủ trong `BorrowSellPostingService` (copy y hệt `ProductExportPostingService`), giá trị đúng bảng brief (15/16/12/13/14/6). Không thiếu → không fatal.

Không phát hiện cụm nào bị bỏ sót, truyền nhầm percent, hay nhầm company_id.

## 3. Giá vốn (đã fix 34fd294) — ĐÚNG, có test chặn tái phát

- `costAccounting` hiện tại: `$total = round((float) $p->export_price * $qty)` — KHÔNG nhân `unit_coefficient`, khớp đúng ERP dòng 203 (`$product->export_price * $product->qty`).
- Test `BorrowSellPostingFirmTest` dùng fixture `unit_coefficient=5`, `export_price=900000`, `qty=10` → assert `cost157 == 9000000` (không phải 45.000.000 nếu nhân nhầm coefficient) — **chặn tái phát hiệu quả**, chạy `phpunit --filter=BorrowSellPostingFirmTest` → `OK (1 test, 6 assertions)` (verify lại độc lập, kết quả khớp report).
- Docblock trong code giải thích rõ lý do lệch khỏi văn bản brief (brief ghi nhân coefficient là lỗi copy từ mẫu `ProductExportPostingService`, đã tự phát hiện + sửa + ghi chú minh bạch, đúng tinh thần "theo ERP khi brief mâu thuẫn nguồn ERP thật").

## 4. Shape — ĐÚNG

- `getDataAccounting(BorrowSell $bs): [bool, array, string]`, không ghi DB (chỉ query đọc `FirmContract::find`, `SupportAccounting::where`) — khớp `getDataProductExportAccounting`.
- `postAccounting(BorrowSell $bs): [bool, string]`, ghi trong `DB::transaction(...)`, bắt `\Throwable` trả lỗi thay vì để exception vỡ ra ngoài — khớp `ProductExportPostingService::postAccounting`.
- Nhánh WrService trả đúng `[false, [], 'Nhánh WrService chưa hỗ trợ (Task 5)']` như brief yêu cầu, không tự làm.

## Non-blocking findings (không chặn merge, ghi để lưu ý Task 5-7 / integration)

1. **`Modules/Finance/Services/BorrowSell/BorrowSellPostingService.php:198-199`** — `gross`/`gross_vat` lấy thẳng từ `$bs->sum_amount_after_extra(_vat)` (đúng ERP), nhưng khác cột này **chưa chắc luôn được điền** ở luồng tạo `BorrowSell` phía HRM (Task 1/2 khác đảm nhiệm) — `ProductExportPostingService` từng phải né vấn đề tương tự bằng cách cộng dồn lại từ chi tiết vì lý do y hệt (comment dòng 36 file đó: "sum_amount_after_extra có thể chưa được điền ở luồng HRM"). Đây KHÔNG phải lỗi của P2-4 (port đúng ERP, đúng brief), nhưng khi Task 6/7 nối luồng tạo/duyệt `BorrowSell` thật, cần xác nhận cột `sum_amount_after_extra/_vat` được tính đúng trước khi gọi `postAccounting` — nếu không, doanh thu cụm 1 sẽ ra 0 dù có hàng xuất thật.
2. **`Modules/Finance/Services/BorrowSell/BorrowSellPostingService.php:83-108`** — `postAccounting` gọi `resolveContract($bs)` LẦN THỨ 2 (lần 1 đã chạy bên trong `getDataAccounting`) chỉ để lấy dữ liệu cho `$meta` — 2 query DB (`FirmContract::find` + `SupportAccounting::where`) dư thừa mỗi lần post. Không sai (kết quả giống hệt, vì cùng input), chỉ là hiệu năng nhỏ (1 phiếu = 2 lần query thay vì 1). Có thể tối ưu sau bằng cách trả `$contract` kèm theo từ `getDataAccounting` nếu muốn, không cấp thiết ở khối lượng hiện tại.

## Verify đã chạy độc lập (không chỉ tin report)

```
mysql -h127.0.0.1 -uroot erp_hrm_check -e "SHOW COLUMNS FROM firm_contracts;"   # đủ id/code/customer_id/created_by/company_id/department_id/part_id
mysql -h127.0.0.1 -uroot erp_hrm_check -e "SHOW COLUMNS FROM borrow_sells;"     # có sum_amount_after_extra(_vat), created_by, contractable_id/type
mysql -h127.0.0.1 -uroot erp_hrm_check -e "SHOW COLUMNS FROM borrow_sell_products;" # đủ export_price/qty/unit_coefficient/price/extra_price/allocated_price/rebate_price/vat_percent
php vendor/bin/phpunit --filter=BorrowSellPostingFirmTest Modules/Finance/Tests/Feature/BorrowSellPostingFirmTest.php
  → OK (1 test, 6 assertions)
git log --oneline -- Modules/Finance/Services/BorrowSell/BorrowSellPostingService.php
  → 34fd29452, fe9c48f25 (khớp report)
```

Đọc thêm để đối chiếu (chỉ đọc): ERP `FirmContractBorrowSellService.php` (toàn văn), HRM `SupportAccountingTrait.php` (toàn văn), `ProductExportPostingService.php` (mẫu, toàn văn), `Contract.php`, `FirmContract.php`, `BorrowSell.php`, `SupportAccounting.php`.

## Verdict cuối

**APPROVED — không cần sửa gì trước khi merge.** 2 điểm non-blocking nêu trên nên chuyển thành lưu ý cho Task 6/7 (luồng tạo/duyệt BorrowSell thật) chứ không phải việc của P2-4.
