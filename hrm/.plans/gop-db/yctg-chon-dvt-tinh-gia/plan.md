# #12212 YCTG / PTG tick theo ĐVT — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Cho XNK (YCTG) và Kế toán mua hàng (PTG) tick "Tính giá" theo từng đơn vị tính; ĐVT bỏ tick bắt lý do, không bắt giá, và hiện từng ĐVT ở kết quả trả KD.

**Architecture:** DB đã lưu `chosen`/`unchosen_reason` theo dòng (mã × ĐVT) — chỉ đổi lớp quyết định từ "theo mã" sang "theo dòng": `ChosenProducts` khoá `pid:uid`, 2 writer tra theo khoá, finalizer chỉ trả về 1 mã bỏ HẾT ĐVT, `unpricedOf` trả mảng theo ĐVT; FE mixin/bảng bỏ lan cả mã.

**Tech Stack:** Laravel 8 (hrm-api, PHPUnit feature test), Nuxt 2 (hrm-client), Playwright (e2e/).

**Spec:** `HRM/.plans/gop-db/yctg-chon-dvt-tinh-gia/design.md`

## Global Constraints
- Làm trong worktree nhánh `feature/yctg-chon-dvt-tinh-gia` tách từ `develop` (cả hrm-api lẫn hrm-client). KHÔNG đụng working tree chính hrm-api (đang có WIP Import của session khác).
- Không migration, không đổi DB.
- Message: `ChosenProducts::MSG_NONE_CHOSEN = 'Phải chọn ít nhất 1 đơn vị tính để tính giá'`; `MSG_REASON_REQUIRED` giữ `'Vui lòng nhập lý do không tính giá'`; `REASON_MAX = 255`.
- Lỗi theo dòng: `rows.{i}.unchosen_reason`, tổng: `rows`.
- `not_priced` của dòng YCHG: `null` hoặc mảng `[{unit_name: string, reason: ?string, by: 'XNK'|'Kế toán mua hàng'}]`, thứ tự: YCTG trước, PTG sau, trong mỗi nguồn theo id dòng.
- Trạng thái hàng khi nhóm tính giá xong: chỉ mã KHÔNG còn dòng PTG `chosen=1` (hoặc bị bỏ hết ở YCTG) mới về 1 Nhập thông tin.
- Thông báo `(N hàng hoá không tính giá)`: N = số MÃ có ≥ 1 ĐVT bỏ tick (YCTG hoặc PTG).
- FE: chữ lỗi đỏ chỉ cho validate; ghi chú "Không tính giá" dùng xám `#6b7280`. Chạy test e2e bằng Node 20.
- Commit trailer: `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. Không push/merge khi chưa được user duyệt.

## Review Focus
1. Phiếu CŨ (mọi ĐVT 1 mã cùng `chosen`) mở Sửa/Chi tiết vẫn hiện đúng — mỗi dòng đọc `chosen` riêng của nó.
2. PTG 6: dòng KHÔNG editable gửi `chosen=false` từ client phải bị bỏ qua (giữ giá trị DB), không được lén bỏ tick ĐVT đã duyệt.
3. Bỏ tick ĐVT cơ sở nhưng tick ĐVT khác: gợi ý Giá NCC từ ĐVT cơ sở (mixin) không được làm vỡ — ĐVT tick vẫn nhập giá tay được.
4. Mã có 1 ĐVT tick + 1 ĐVT bỏ: mã lên 3 (đang KD), KQ chỉ chứa ĐVT tick, `not_priced` liệt kê ĐVT bỏ, nền dòng YCHG KHÔNG tô "không đi tiếp".
5. Nháp: bỏ tick không bắt lý do, gửi mới bắt; tick lại xoá lý do cũ ở đúng dòng đó (không xoá dòng khác cùng mã).

---

### Task 1: `ChosenProducts` theo ĐVT + YCTG validate

**Files:**
- Modify: `hrm-api/Modules/MasterData/Services/PriceCalculation/ChosenProducts.php`
- Modify: `hrm-api/Modules/MasterData/Services/PriceCalculation/PriceCalculateRequestWriter.php` (~222-275, `validate()`)
- Test: `hrm-api/Modules/MasterData/Tests/Feature/PriceCalculateRequestApiTest.php`

**Interfaces:**
- Produces: `ChosenProducts::resolve(array $skeleton, array $given, bool $send, array &$errors, ?array $only = null): array` — trả `["pid:uid" => ['chosen' => bool, 'reason' => ?string]]` cho MỌI dòng skeleton; `$only` (mảng `"pid:uid"`) giới hạn dòng được đọc từ `$given`, dòng ngoài `$only` KHÔNG có trong kết quả. `ChosenProducts::key(int $pid, int $uid): string` = `"$pid:$uid"`.

- [ ] **Step 1: Sửa test cũ + thêm test**
  - `bo_tick_ma_khong_bat_gia_ncc_bat_ly_do_va_con_it_nhat_1_ma` → đổi kỳ vọng theo dòng (message mới cho `rows`).
  - Thêm `bo_tick_rieng_dvt_u2_cua_n1_chi_dong_do_bo_tick`: gửi `rows[1]` (n1,u2) `chosen=false, unchosen_reason='NCC chỉ báo Cái', supplier_price=null`, các dòng khác đủ giá, `send=true` → 200; DB `price_calculate_request_products` n1: u1 `chosen=1, reason=null`, u2 `chosen=0, reason='NCC chỉ báo Cái'`.
  - Thêm `bo_tick_dvt_thieu_ly_do_bao_dung_dong`: `rows[1]` chosen=false không lý do, send → 422 có `rows.1.unchosen_reason`, KHÔNG có `rows.0.unchosen_reason`; `rows[0]` (n1,u1) để `supplier_price=null` vẫn bị bắt giá (`rows.0.supplier_price`).
  - Thêm `nhap_bo_tick_dvt_khong_bat_ly_do`: send=false, `rows[1]` chosen=false không lý do → 200.
- [ ] **Step 2:** `cd <worktree-api> && php artisan test --filter=PriceCalculateRequestApiTest` → FAIL ở 3 test mới (u1 bị kéo theo u2 / lỗi ở rows.0).
- [ ] **Step 3:** `resolve` bỏ `if (isset($out[$pid])) continue;`, khoá theo `key()`; đổi `MSG_NONE_CHOSEN`. Writer: `$choice[ChosenProducts::key($pid, $uid)]`.
- [ ] **Step 4:** chạy lại filter → PASS toàn file.
- [ ] **Step 5:** commit `feat(#12212): YCTG tick tính giá theo từng ĐVT`.

### Task 2: PTG validate theo ĐVT + finalizer trả hàng theo mã bỏ hết

**Files:**
- Modify: `.../PriceCalculation/PriceCalculateWriter.php` — `validate()` ~565-590, 742, 754; bỏ khối `MSG_UNCHOSEN_LOCKED` (~568-575) và const (line 55).
- Modify: `.../PriceCalculation/PriceCalculateFinalizer.php` — `releaseUnchosen()` ~217-235.
- Test: `hrm-api/Modules/MasterData/Tests/Feature/PriceCalculateApiTest.php`

**Interfaces:**
- Consumes: `ChosenProducts::resolve` / `key` (Task 1). PTG 6 truyền `$editable` làm `$only`; dòng không editable tra `$choice[$key] ?? null` → giữ giá trị DB (đọc từ dòng hiện có), không lấy từ client.
- Produces: `releaseUnchosen()` vẫn trả `int` = số MÃ có ≥ 1 dòng `chosen=0` (YCTG ∪ PTG); nhưng chỉ đổi status/`releaseWaiting` cho tập mã = (mã có dòng `chosen=0`) − (mã có dòng PTG `chosen=1`).

- [ ] **Step 1: Sửa/ thêm test**
  - `bo_tick_ma_o_ptg_khong_ap_gia_khong_vao_kq_va_ve_nhap_thong_tin`: giữ kịch bản bỏ tick CẢ 2 dòng n1 (gửi `rows[1]` cũng `chosen=false` + lý do) — kỳ vọng cũ giữ, trừ `not_priced` (Task 3 sửa).
  - Thêm `ptg_bo_tick_rieng_u2_n1_ap_gia_u1_ma_len_3`: submit, `rows[1]` (n1,u2) `chosen=false, reason='Không bán thùng'` → 200; `upp('n1','u1',1)` có giá, `upp('n1','u2',1)` null; `pccStatus('n1') === 3`; KQ chứa n1; title thông báo chứa `(1 hàng hoá không tính giá)`.
  - `ptg_6_khong_bo_tick_duoc_ma_con_dvt_da_duyet_...` → đổi tên `ptg_6_bo_tick_duoc_dvt_bi_tu_choi_du_ma_con_dvt_da_duyet`: bỏ tick `rows[1]` (n1,u2 bị từ chối) + lý do → 200, dòng u2 `chosen=0`, `approval_status=null`; dòng u1 vẫn `chosen=1` đã duyệt; gửi kèm `rows[0]` (u1 không editable) `chosen=false` → bị bỏ qua, DB vẫn `chosen=1`. Kết thúc: PTG status 1 khi n2 duyệt lại xong, `pccStatus('n1') === 3`.
  - `bo_tick_ptg_bat_ly_do_khi_gui_va_con_it_nhat_1_ma`: đổi `MSG_NONE_CHOSEN` mới; vòng bỏ tick phải bỏ CẢ 3 dòng (0,1,2) mới ra lỗi `rows`.
- [ ] **Step 2:** `php artisan test --filter=PriceCalculateApiTest` → FAIL ở test mới/đổi.
- [ ] **Step 3:** sửa writer (tra theo key, bỏ khối locked, `assertAnyChosen` dùng `$otherChosen || contains true`) và finalizer (tập mã release như Interfaces).
- [ ] **Step 4:** chạy lại → PASS (trừ 2 assert `not_priced` dòng ~337, ~436 nếu chưa làm Task 3 — tạm thời Task 2 không đổi chúng; chúng vẫn PASS vì shape chưa đổi).
- [ ] **Step 5:** commit `feat(#12212): PTG tick tính giá theo ĐVT, mã còn ĐVT tick đi luồng thường`.

### Task 3: `not_priced` theo ĐVT

**Files:**
- Modify: `.../PriceCalculation/PriceAskingRequestService.php` — `unpricedOf()` 286-310 (join `units` lấy `name as unit_name`), docblock kiểu trả về.
- Test: `PriceCalculateApiTest.php` (~337, ~436), `PriceAskingRequestApiTest.php` nếu có assert `not_priced`.

**Interfaces:**
- Produces: `unpricedOf(array $calcRequestIds): array<int YCTG id, array<int product_id, list<array{unit_name: string, reason: ?string, by: string}>>>`; chỗ dùng ~430 giữ `?? null`.

- [ ] **Step 1:** đổi assert:
  - ~337: `[['unit_name' => <tên u1>, 'reason' => 'Hãng ngừng sản xuất', 'by' => 'Kế toán mua hàng'], ['unit_name' => <tên u2>, ...cùng lý do]]` (tên lấy `DB::table('units')->where('id',$this->fx['u1'])->value('name')`).
  - ~436: 1 phần tử u1 `'NCC không báo giá'`, `by` XNK.
  - Trong test mới Task 2 `ptg_bo_tick_rieng_u2_n1_...`: `not_priced` n1 = đúng 1 phần tử u2 `'Không bán thùng'`.
- [ ] **Step 2:** chạy `--filter=PriceCalculateApiTest` → FAIL ở 3 assert.
- [ ] **Step 3:** sửa `unpricedOf` (append, không bỏ trùng; 1 dòng = 1 phần tử).
- [ ] **Step 4:** chạy `--filter='PriceCalculateApiTest|PriceCalculateRequestApiTest|PriceAskingRequestApiTest'` → PASS.
- [ ] **Step 5:** commit `feat(#12212): kết quả trả KD liệt kê ĐVT không tính giá`.

### Task 4: FE — tick + lý do theo dòng

**Files:**
- Modify: `hrm-client/utils/mixins/priceInputRowsMixin.js` (~67-85 `setChosen`, `setReason`)
- Modify: `hrm-client/components/sale/price-calculate/PriceInputGoodsTable.vue` (checkbox + ô lý do + `checkLocked`)
- Modify: `hrm-client/components/sale/price-calculate/PriceCalculateRequestForm.vue`, `hrm-client/components/finance/price-calculate/PriceCalculateForm.vue` chỉ khi có chỗ dựng/đọc `chosen` theo `_first` (grep `_first` + `chosen`).

**Interfaces:**
- Consumes: payload `rows[i].chosen/unchosen_reason` đã gửi theo dòng (không đổi).

- [ ] **Step 1:** `setChosen(i, v)`: chỉ `rows[i]`; tick lại → `unchosen_reason = null`; xoá lỗi `rows.${i}.*` và `rows`. `setReason(i, v)`: chỉ `rows[i]`, xoá `rows.${i}.unchosen_reason`.
- [ ] **Step 2:** bảng: checkbox "Tính giá" ở MỌI dòng (bỏ `v-if="row._first"` cho checkbox); ô `V2BaseInput` "Lý do không tính giá *" (đỏ `is-invalid` theo `err['rows.'+i+'.unchosen_reason']`) hiện ở cột Tên hàng của dòng có `row.chosen === false` — cả dòng "↳ cùng mã"; `checkLocked(row)` = `readonly || row.editable === false`.
- [ ] **Step 3:** `cd hrm-client && npx eslint <các file đã sửa>` → 0 lỗi.
- [ ] **Step 4:** commit `feat(#12212): FE tick tính giá + lý do theo từng ĐVT`.

### Task 5: FE — YCHG hiện `not_priced` theo ĐVT

**Files:**
- Modify: `hrm-client/components/sale/price-asking/PriceAskingRequestForm.vue` (~198-226)

- [ ] **Step 1:** class `row-temp-rejected` = `isTempRejected(row) || (row.not_priced && row.not_priced.length && !(row.result || []).length)` (kiểm tên trường kết quả giá thật trong file trước khi dùng; nếu khác `result` thì dùng đúng trường hiển thị giá).
- [ ] **Step 2:** ghi chú: `v-for` mỗi phần tử 1 dòng xám `#6b7280`: `Không tính giá ĐVT {{ n.unit_name }} ({{ n.by }})` + ` — lý do: {{ n.reason }}` khi có.
- [ ] **Step 3:** eslint file → 0 lỗi; commit `feat(#12212): YCHG liệt kê ĐVT không tính giá`.

### Task 6: Kiểm Playwright

**Files:**
- Create: `e2e/tests/yctg-chon-dvt-tinh-gia.spec.ts` (bám spec YCTG có sẵn trong `e2e/tests` — grep `price-calculate-requests`)

- [ ] **Step 1:** kịch bản: mở form YCTG có hàng ≥ 2 ĐVT → bỏ tick dòng ĐVT thứ 2 → thấy ô lý do ở đúng dòng đó, dòng 1 vẫn tick và ô Giá NCC bật; bấm gửi khi trống lý do → đỏ đúng dòng; tick lại → ô lý do biến mất.
- [ ] **Step 2:** `cd e2e && PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" npx playwright test yctg-chon-dvt-tinh-gia` → PASS (API/client của worktree, không chạm server :3000/:8000 của session khác — dùng port riêng nếu cần).
- [ ] **Step 3:** chụp ảnh màn hình form + màn YCHG kết quả, lưu `HRM/.plans/gop-db/yctg-chon-dvt-tinh-gia/`; commit spec.
