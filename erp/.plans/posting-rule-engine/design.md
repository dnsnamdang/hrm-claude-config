# Posting Rule Engine — Cấu hình công thức hạch toán

**Ngày:** 2026-07-24 · **Dự án:** ERP Tân Phát (TanPhatDev) · **Demo tham chiếu:** `~/Documents/demo/posting-rule-engine-v3.html`

## 1. Mục tiêu
Cho phép kế toán **cấu hình công thức hạch toán** (nhóm bút toán + điều kiện + dòng định khoản với công thức) cho các loại phiếu có hạch toán, qua một màn cấu hình. Khi ghi sổ phiếu, một **engine runtime** nạp cấu hình, đánh giá điều kiện + công thức trên dữ liệu thật của phiếu, sinh ra bút toán (`account_details`) — thay cho logic hạch toán hard-code.

**Pilot phase 1:** loại phiếu **`product_export` — Xuất bán HĐ hãng (`XUAT_BAN_HD_HANG`)**, chạy end-to-end (màn cấu hình + engine + ghi sổ thật), theo cơ chế **shadow** (đối chiếu với logic cũ trước khi thay).

## 2. Quyết định chốt (brainstorm 2026-07-24)
| # | Quyết định |
|---|---|
| Phạm vi | Pilot end-to-end 1 loại phiếu: `product_export` / `XUAT_BAN_HD_HANG` |
| Mô hình biến | **VariableProvider bằng CODE** cho mỗi loại phiếu (biến = code, config = data). Không cho config trỏ thẳng cột DB |
| Rollout | **Shadow**: engine tính song song + so sánh + log; vẫn ghi sổ bằng logic cũ tới khi khớp 100% → mới flip sang engine |
| FE | **AngularJS 1.3.9 + Blade** (đúng chuẩn ERP, không dùng Vue như demo) |
| Bộ đánh giá công thức | **symfony/expression-language** (PHP, an toàn, không `eval`) |

## 3. Kiến trúc
```
Màn cấu hình (Blade+Angular)  →  DB posting rules  →  PostingEngine  →  mảng bút toán  →  AccountDetail::saveAccountDetail
   (config = data)                                          ↑ ↑
                        VariableProviderRegistry (code) ─────┘ │  trả map biến từ record phiếu
                        DynamicAccountResolverRegistry (code) ─┘   trả account_id cho TK @động
```
Tách bạch:
- **Config (data, sửa qua UI):** nhóm bút toán, điều kiện, dòng định khoản.
- **Catalog (code, dev khai báo):** biến khả dụng + TK động + đối tượng — theo từng loại phiếu.
- **Engine (runtime):** thuần đọc config + catalog → sinh bút toán.

## 4. Schema (5 bảng mới)
```
posting_doc_types
  id, code (unique, vd 'product_export.xuat_ban_hd_hang'), name, version (int, default 1),
  created_by, updated_by, timestamps

posting_groups
  id, posting_doc_type_id (FK), name, order (int), active (bool),
  has_condition (bool), cond_expr (text nullable),
  loop_source (varchar nullable — key collection để LẶP; null = nhóm thường 1 lần),
  timestamps

posting_lines
  id, posting_group_id (FK), order (int), side (enum 'no'|'co'),
  account (varchar — mã cố định vd '5111' HOẶC '@KEY' cho TK động),
  value_formula (text), obj (varchar nullable — '@phieu' | mã cố định),
  fee_code (varchar nullable), job_code (varchar nullable), timestamps

posting_config_histories
  id, posting_doc_type_id (FK), user_id, version (int),
  summary (text), snapshot (json — toàn bộ groups+lines sau khi lưu), created_at

posting_shadow_logs   -- chỉ dùng ở giai đoạn shadow
  id, invoiceable_type, invoiceable_id, doc_type_code,
  matched (bool), diff (json — chênh lệch engine vs logic cũ), created_at
```
> Convention DB ERP: khóa ngoại `unsignedBigInteger nullable`, `created_by/updated_by` thủ công, không SoftDeletes cho entity chính. Không tạo migration riêng cho quyền (thêm vào seeder chuẩn nếu có quyền).

## 5. Ánh xạ dòng định khoản → `account_details`
| Config | account_details | Ghi chú |
|---|---|---|
| `side` no/co | `type` = 1 (Nợ) / 2 (Có) | `AccountDetail::TYPE_DEPT / TYPE_HAS` |
| `account` (cố định) | `account_id` | lookup `accounts.identify_number = account` |
| `account` `@KEY` | `account_id` | DynamicAccountResolver(KEY, record) → account_id |
| `value_formula` | `money_value` (+ `money_value_exchange` theo tỷ giá phiếu) | tính bằng engine |
| `obj` = `@phieu` | `customer_id` / `supplier_id` / `employee_id` | đối tượng chính của phiếu (KH của product_export) |
| `obj` = mã cố định | tương ứng | (ít dùng ở pilot) |
| `fee_code` | `cost_debt_id` | lookup mã phí |
| `job_code` | `work_id` | lookup vụ việc |
| (bối cảnh phiếu) | `company_id, department_id, part_id, invoiceable_id/type/code, invoiceable_date_accounting, contract_id, contract_type, contract_customer_id, currency_id, exchange_rate` | engine set từ record phiếu, không cấu hình |

## 6. VariableProvider — `ProductExportVariableProvider`
Interface `PostingVariableProvider`:
```php
interface PostingVariableProvider {
    // trả metadata biến để MÀN CẤU HÌNH hiển thị (key, label, kiểu, sample)
    public function catalog(): array;      // [['key'=>'TienHang','label'=>...,'type'=>'number','sample'=>...], ...]
    public function attributes(): array;   // biến phân loại cho điều kiện: [['key'=>'type','options'=>[...]]]
    // trả GIÁ TRỊ biến thật từ record (dùng khi ghi sổ) + object đối tượng
    public function values($record): array;      // ['TienHang'=>..., 'GiaVon'=>..., 'type'=>'xuat_ban_hd_hang', ...]
    public function objectFor($record): array;   // ['customer_id'=>..., 'supplier_id'=>null, 'employee_id'=>null]

    // ── LOOP (nhóm lặp) ──
    // metadata collection để MÀN hiển thị dropdown "Lặp theo" + token {item.*}
    public function collections(): array;  // [['key'=>'nhan_vien_phong','label'=>...,'itemFields'=>[['key'=>'commission_sale_percent','label'=>...], ...]], ...]
    // trả DANH SÁCH item (đã LÀM PHẲNG vòng lặp lồng) cho 1 collection khi ghi sổ.
    // mỗi item = ['vars'=>[field=>value,...], 'object'=>['employee_id'=>..,'employee_department_id'=>..,...]]
    public function collectionValues($record, string $key): array;
}
```
`ProductExportVariableProvider::values($productExport)` **tái dùng logic tính hiện có** (không viết lại): gọi `FirmContractProductExportService`/`prepareData` để lấy `sale_invoice, sale_invoice_vat, sum_amount_after_extra, sum_amount_after_extra_vat, giá vốn, support_accounting.before_vat_*`, `vat_percent`, `type`. Đây là điểm neo để engine ra kết quả trùng logic cũ.

Registry: `PostingVariableProviderRegistry` map `doc_type_code → provider`.

## 6b. Nhóm lặp (loop group) — cấu hình được cụm bút toán per-đối tượng
Nhiều cụm hạch toán (thưởng thực hiện HĐ, thuế TNCN tạm, thưởng NS tháng+quý, quỹ rủi ro phòng) **lặp qua collection** (nhân viên phòng / tổ trưởng / trưởng phòng / các phòng), mỗi item sinh 1 cặp Nợ/Có với giá trị = `amount × item.rate/100 × context.rate/100`, đối tượng = item.employee/department. Để cấu hình được:
- `posting_groups.loop_source` = key collection (null = nhóm thường). Nhóm lặp → **các dòng của nhóm được sinh MỘT LẦN CHO MỖI ITEM** trong collection.
- **Provider (code) làm phẳng vòng lặp lồng** thành 1 danh sách item (`collectionValues`); mỗi item mang `vars` (trường per-item: `commission_sale_percent`, `diff_employee_percent`, `month_amount`, `risk_fund_amount`...) + `object` (employee_id/department của item). Config KHÔNG cần lồng.
- **Dòng trong nhóm lặp**: công thức dùng `{item.<field>}` + biến vô hướng `{amount}`...; đối tượng chọn **`@item`** → engine gán object của item; TK/mã phí/vụ việc như thường.
- **Ánh xạ 4 cụm → nhóm lặp:**
  | Cụm | loop_source (collection) | dòng (Nợ/Có) | công thức value |
  |---|---|---|---|
  | Thưởng thực hiện HĐ | `bonus_recipients` (NV+tổ trưởng+trưởng phòng, đã phẳng) | Nợ 5211 / Có 35241 | `{amount} * {item.rate} / 100` (rate = commission_sale × diff_employee, hoặc diff_part_lead / diff_department_lead — provider tính sẵn vào item.rate) |
  | Thuế TNCN tạm | `tndn_recipients` | Nợ 35241 / Có 3335 | ↑ |
  | Thưởng NS tháng | `commission_recipients` | Nợ 6411 / Có 35241 | `{item.month_amount}` |
  | Thưởng NS quý | `commission_recipients` | Nợ 6411 / Có 35241 | `{item.quarter_amount}` |
  | Quỹ rủi ro phòng | `risk_departments` | Nợ 6411 / Có 35241 | `{item.risk_fund_amount}` |
  > Provider tính sẵn `item.rate`/`item.month_amount`/... (làm phẳng logic per-employee/part-lead/dept-lead) → công thức trong config gọn, engine chỉ lặp.

## 7. Dynamic accounts + Objects
- `DynamicAccountResolver` interface: `resolve($key, $record): ?int` (account_id). Registry theo key (vd `@TK_PHAI_THU_KH` → TK phải thu theo nhóm KH của phiếu). Pilot có thể chưa cần TK động nếu logic cũ dùng TK cố định — sẽ xác định khi map bút toán XUAT_BAN_HD_HANG.
- `obj @phieu` → dùng `provider->objectFor($record)`.

## 8. Engine runtime
`PostingEngine::generate($docTypeCode, $record): array` (mảng bút toán dạng `saveAccountDetail` nhận):
1. Nạp `posting_doc_types` + groups(active, order) + lines.
2. `vals = provider->values($record)`.
3. Với mỗi group: nếu `has_condition` → `ExpressionLanguage->evaluate(cond_expr, vals)`; false → bỏ qua.
4. Với group thỏa:
   - **Nhóm thường** (`loop_source` null): mỗi line → tính `value_formula` (expression-language) với `vals` → 1 phần tử bút toán (type, account_id, money_value, customer/supplier/employee, cost_debt_id, work_id, + bối cảnh phiếu).
   - **Nhóm lặp** (`loop_source` != null): `items = provider->collectionValues($record, loop_source)`; **với mỗi item**: ctx = `vals + ('item.'.$k => $v cho $item['vars'])`; mỗi line tính với ctx; `@item` → gán `$item['object']` (employee_id/employee_department_id...). Sinh N cặp bút toán (mỗi item 1 bộ dòng). Đánh `group` tăng dần mỗi item (khớp cột `account_details.group`).
5. Trả mảng. Bút toán rỗng (điều kiện không thỏa / collection rỗng) → mảng rỗng.

**Cú pháp công thức:** biến dạng `{TenBien}` (đồng nhất demo) — engine thay `{X}` bằng giá trị trước khi đưa vào expression-language, HOẶC map sang biến expression-language trực tiếp. Value formula chỉ số học `+ - * / ()`; điều kiện cho so sánh `== != > < >= <= && ||` + chuỗi. Validate parse + kiểm biến ∈ catalog.

## 9. Tích hợp + Shadow (an toàn)
Điểm chèn: `ProductExportsController::store`, nhánh `XUAT_BAN_HD_HANG` (sau khi có `$data` từ `getDataProductExportAccounting`, trước `saveAccountDetail`):
```
$engineData = PostingEngine::generate('product_export.xuat_ban_hd_hang', $object);
$diff = comparePostings($data /*cũ*/, $engineData);
PostingShadowLog::create([... invoiceable, matched=empty($diff), diff=$diff]);
// GIAI ĐOẠN SHADOW: vẫn dùng $data (logic cũ) để saveAccountDetail
// SAU KHI KHỚP 100%: đổi cờ (config posting.use_engine=true) → dùng $engineData
```
Cờ bật/tắt qua config/env (vd `POSTING_ENGINE_DOCS=product_export.xuat_ban_hd_hang`), không hard-code.

`comparePostings`: so khớp tập bút toán (bỏ qua thứ tự) theo (type, account_id, money_value làm tròn, customer/supplier/employee, cost_debt_id, work_id). Lệch → ghi diff.

## 10. Màn cấu hình (Blade + AngularJS 1.3.9)
Route: `admin/accounting/posting-rules` (Common/Accounting). Layout `layouts/app.blade.php` (interpolation `<% %>`).
- Toolbar: chọn loại phiếu (`posting_doc_types`), trạng thái hợp lệ/dirty/version, nút Lưu / Hủy thay đổi / Lịch sử.
- Danh sách nhóm bút toán (card, kéo-thả thứ tự): tên, badge quan hệ (nNợ-nCó), bật/tắt active, xóa.
  - **Lặp theo** (loop_source): dropdown chọn collection từ `provider->collections()` (— Không lặp — / nhan_vien_phong / ...). Khi chọn → dòng của nhóm sinh per-item; popup công thức thêm token `{item.<field>}` (từ `collections()[key].itemFields`) + đối tượng có option `@item`.
  - Điều kiện áp dụng: bật/tắt + nút mở popup công thức ƒx (chế độ cond).
  - Dòng định khoản (bảng kéo-thả): Nợ/Có toggle · TK (select2 tìm kiếm cố định+động) · Giá trị (nút mở popup ƒx value) · Đối tượng (select @phieu/mã) · Mã phí · Mã vụ việc.
- Popup công thức ƒx (2 chế độ cond/value): textarea + token biến/giá trị/toán tử (chèn) + **xem trước** với dữ liệu mẫu (sample từ catalog) — validate realtime.
- Validate (BE + FE): nhóm 1Nợ-nCó hoặc nNợ-1Có (không n-n), đủ Nợ+Có, công thức/điều kiện hợp lệ + biến ∈ catalog. Lưu chỉ khi hợp lệ.
- Kéo-thả: dùng jQuery UI sortable (có sẵn) hoặc HTML5 DnD; select2 dùng biến `select2-in-modal`/`select2-ajax` theo chuẩn ERP.
- Popup công thức: vì Angular 1.3.9 compile toàn body, chú ý `ng-non-bindable`/`ng-model` cho các select trong vùng compile (bài học ERP).

## 11. API
- `GET admin/accounting/posting-rules/config?doc_type=...` → groups+lines + catalog biến/attrs + danh mục (accounts, dynamic accounts, objects, feeCodes=cost_debts, jobCodes=works).
- `POST admin/accounting/posting-rules/save` → validate + lưu groups/lines + version++ + history snapshot. Rethrow ValidationException.
- `GET admin/accounting/posting-rules/history?doc_type=...`.
- (nội bộ) `POST .../validate-formula` (tùy chọn — có thể validate client + server khi lưu).

## 12. Validate rules (đồng nhất demo)
- Nhóm: có ≥1 Nợ và ≥1 Có; không (nhiều Nợ VÀ nhiều Có); mỗi dòng có TK + công thức value hợp lệ; điều kiện (nếu bật) parse được + trả bool.
- Biến trong công thức phải ∈ catalog của loại phiếu (BE kiểm bằng provider->catalog()).
- Doc hợp lệ = mọi nhóm active hợp lệ. Lưu bị chặn nếu có nhóm active lỗi.

## 13. Quyền
- `Cấu hình hạch toán` (xem + sửa màn) — thêm vào seeder quyền chuẩn (nếu ERP có seeder; nếu không, tạo qua tinker firstOrCreate). Route data thao tác gắn `checkPermission:Cấu hình hạch toán`.

## 14. Edge cases
- Loại phiếu chưa cấu hình nhóm nào → engine trả rỗng → shadow log để phát hiện; không tự ghi sổ sai.
- Biến null/0 → công thức trả 0; dòng money_value=0 vẫn sinh hay bỏ? → **chốt: bỏ dòng có money_value=0** (đồng nhất kế toán, tránh bút toán 0đ) — trừ khi cần giữ để cân đối (xác định khi map XUAT_BAN_HD_HANG).
- Tỷ giá: phiếu ngoại tệ → money_value (nguyên tệ) + money_value_exchange (VND). Pilot XUAT_BAN_HD_HANG chủ yếu VND.
- TK không tồn tại (identify_number sai) → validate chặn khi lưu; runtime nếu thiếu → log lỗi, không ghi.
- Điều kiện chạy sai/exception → nhóm bị bỏ qua + log (không làm hỏng cả phiếu).

## 15. Downstream impact
- Không đổi bảng `account_details` (chỉ thêm nguồn sinh bút toán). Báo cáo/sổ (Sổ NKC, bảng kê mã phí, công nợ...) dùng account_details như cũ.
- Giai đoạn shadow: 0 rủi ro (vẫn logic cũ ghi sổ). Chỉ khi flip mới thay nguồn — và chỉ cho đúng loại phiếu bật cờ.
- Không đụng các service hạch toán khác (chỉ nhánh XUAT_BAN_HD_HANG của product_export).

## 16. Ngoài phạm vi phase 1 (YAGNI)
- **Trong phạm vi (đã chốt B):** cả 8 cụm của Xuất bán HĐ hãng — 3 cụm cố định + 4 cụm động (qua nhóm lặp, mục 6b). Shadow (mục 9) đối chiếu toàn bộ.
- Các loại xuất khác (KM/trả NCC/bảo hành/bốc xếp) + loại phiếu khác — nhân rộng sau khi pilot khớp.
- Khôi phục version cũ từ history (chỉ lưu snapshot ở phase 1; khôi phục để sau).
- TK động phức tạp / phân bổ nhiều chiều — chỉ làm khi bút toán pilot cần.
