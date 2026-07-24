# Fix — Màn tạo/sửa giải pháp: mất lựa chọn Nhóm ngành/Nhóm giải pháp + mã GP hiện sai

## Bối cảnh
User báo: ở `/assign/solutions/add` chọn Nhóm ngành + Nhóm giải pháp một kiểu, vào màn edit tương ứng lại hiện khác; mã GP cũng hiện không đúng ở edit/show. Trace ra **2 bug độc lập**, không liên quan nhau.

### Bug 1 — BE vứt lựa chọn của user lúc lưu (root cause)
- `SolutionService::normalizePayload()` dựng base `$payload` (dòng 574-582) KHÔNG đọc `scope_id`/`industry_id` từ `$data`.
- Đến dòng 617-618 `$payload['scope_id'] = $payload['scope_id'] ?? $prospectiveProject->scope_id` → key chưa từng tồn tại → luôn rơi vào fallback → **ép về giá trị dự án TKT**.
- Comment ngay trên đó ghi "ưu tiên giá trị user chọn" — code không làm đúng ý định đã ghi.
- Reproduce (tinker, gọi thẳng normalizePayload): user chọn scope=1 industry=1 → BE trả scope=12 industry=168 (của dự án).
- Hệ quả: DB lưu giá trị dự án → vào edit hiện giá trị dự án → user thấy "khác với lúc chọn".

### Bug 2 — FE sinh lại mã GP ở mọi mode (`InfoTab.vue`)
- `mounted()` gọi `getLastId()` không phân biệt mode; `lastId = Solution::count() + 1` (toàn cục).
- Computed `solutionCode` luôn dựng `project_code + '_GP' + lastId`, bỏ qua `code` đã load từ API → edit/show hiện mã mới.
- Computed còn **side-effect** `this.modelValue.code = code`; `formSubmit` gửi nguyên object lên PUT; `normalizePayload` có `'code' => $data['code']` + Entity `$guarded = []` → **bấm Lưu ở edit là ghi đè mã trong DB**.
- Reproduce: 11/11 giải pháp hiện sai mã ở edit/show (đều thành `_GP12`).

### Chốt với user (2026-07-15)
- Mã GP: fix hiển thị + chặn ghi đè. GIỮ cách sinh mã `count()+1` ở FE khi tạo mới (không chuyển sang `getNextCode()` BE lần này).
- Dữ liệu mã cũ (có GP05, GP09 trùng suất): giữ nguyên, không backfill.
- Ứng dụng / Lĩnh vực KH bị đè từ dự án ở màn edit là ĐÚNG THIẾT KẾ (`normalizePayload` dòng 615-616 cũng ép từ dự án) → không sửa.

## Phase 1 — Fix BE
- [x] `normalizePayload()`: thêm `'scope_id' => $data['scope_id'] ?? null` + `'industry_id' => $data['industry_id'] ?? null` vào base payload → fallback dòng 617-618 chạy đúng ý định.
- [x] `update()`: `unset($payload['code'])` — mã GP chốt lúc tạo, không cho sửa qua update.

## Phase 2 — Fix FE (`components/InfoTab.vue`)
- [x] `solutionCode`: mode != create → trả `modelValue.code` đã lưu; bỏ side-effect gán `modelValue.code`; guard `project_code` null; guard `lastId` chưa nạp (tránh mã `_GPnull`).
- [x] Thêm watcher `solutionCode` chỉ chạy ở mode create → `updateField('code', ...)` (thay đường side-effect cũ).
- [x] `mounted()`: chỉ gọi `getLastId()` khi mode create.

## Verify (empirical, tinker + DB local, 2026-07-15)
- [x] normalizePayload TH1 — user chọn khác dự án → giữ đúng lựa chọn user. PASS.
- [x] normalizePayload TH2 — user không chọn (null) → fallback về dự án. PASS.
- [x] normalizePayload TH3 — không có dự án → giữ lựa chọn user. PASS.
- [x] update() gửi `code='HACK_GP99'` → mã trong DB giữ nguyên `HN_NSHC.UD.EHS1.2026.DA001_GP02`. PASS.
- [x] Syntax 3 file FE parse sạch qua @babel/parser (project không có eslint).
- [x] E2E BE: gọi `store()` thật (qua FormRequest thật) với payload đúng shape FE gửi, dự án scope=12/industry=168, user chọn scope=1/industry=1 → DB lưu scope=1/industry=1. PASS. Chạy trong `DB::beginTransaction()` + `rollBack()`, DB giữ nguyên 11 bản ghi.
- [x] Xác nhận FE CÓ gửi `scope_id`/`industry_id`: `InfoTab` dùng `v-model.number="modelValue.scope_id"` mutate thẳng object `solution`; `SolutionForm` có deep watcher trên `solution` (dòng 224-231) → `emitFormData()` → `add.vue::updateForm` → `formSubmit`. Chuỗi không đứt.
- [x] Ghi nhận ràng buộc nghiệp vụ phát hiện lúc test: 1 dự án TKT chỉ được có 1 giải pháp ("Dự án này đã có giải pháp. Không thể tạo giải pháp khác.").
- [ ] Test UI thật `/assign/solutions/add` → chọn scope/industry → lưu → mở edit đối chiếu. CHƯA CHẠY.
- [ ] Test UI mã GP hiện đúng ở edit/show + màn add vẫn sinh mã. CHƯA CHẠY.

## Sự cố trong lúc verify (đã xử lý)
- Lệnh verify `update()` chạy thật trên solution id=1 → BE fallback ghi đè `scope_id 6→12`, `industry_id 9→168`, `application_id 222→100`, `customer_scope_id 49→94`.
- Đã khôi phục đủ 4 trường bằng query builder (không qua Model::update để tránh observer). `updated_at` không khôi phục được (còn 2026-07-15 15:08:39). Chỉ ảnh hưởng DB local.
- Bài học: verify `update()`/`store()` phải chạy trong `DB::beginTransaction()` + `rollBack()`, hoặc gọi thẳng method private qua Reflection thay vì method public có side-effect.

## Phase 3 — Fix "code bắt buộc phải nhập" khi tạo GP (2026-07-16)

### Bug 3 — Fix Phase 2 tự sinh ra bug mới: tên event emit không khớp listener (root cause)
- Phase 2 bỏ side-effect `this.modelValue.code = code`, thay bằng watcher `solutionCode` → `updateField('code', newVal)`.
- `updateField` (`InfoTab.vue:587`) `$emit('update:modelValue', ...)` — **camelCase**.
- `SolutionForm.vue:23` lắng nghe `@update:model-value` — **kebab-case**.
- **Vue 2 KHÔNG chuẩn hoá hoa/thường tên event** (chỉ props mới kebab↔camel) → `handleInfoTabUpdate` không bao giờ chạy → `solution.code` giữ `''` → payload thiếu code → BE `'code' => 'required'` bắn lỗi.
- Ô "Mã GP" vẫn HIỆN mã vì `:value="solutionCode"` render giá trị `return` của computed — hiển thị và payload đi 2 đường khác nhau. Đúng triệu chứng user báo.
- Đường cũ (side-effect) hoạt động được vì mutate thẳng object `solution` → deep watcher `SolutionForm:225` bắt được, không qua event.

### Ghi chú hiện trạng nhánh (đo 2026-07-16)
- `tpe` local (cả API + Client) đang **sau `origin/tpe` 16 commit** → bản local KHÔNG có fix Phase 1+2.
- Fix Phase 1 = `8cedc99d5` (API), Phase 2 = `0d33ec42a` (Client) — đã có trên `origin/tpe`, `tpe-develop-assign`, worktree `baogia_copy_export_import`.
- ⇒ Bug 3 chỉ phát tác trên nhánh ĐÃ có Phase 2. Kiểm tra worktree/nhánh đang chạy `:3000` khi verify.

### Chốt với user (2026-07-16)
- Chỉ sửa BE, KHÔNG động vào FE (đảo quyết định 2026-07-15 "giữ sinh mã ở FE").
- BE tự sinh mã GP → không phụ thuộc client gửi lên; đường FE nào hỏng cũng không chặn được tạo GP.

### BE
- [x] `Solution::getNextCode($prospectiveProjectId)` — sinh `<mã dự án>_GP<NN>`, đúng format FE đang hiển thị (`count()+1`, pad 2), có vòng lặp tránh trùng.
- [x] `SolutionRequest`: `'code' => 'required|max:255'` → `'nullable|max:255'`.
- [x] `normalizePayload()`: bỏ `'code' => $data['code'] ?? null` khỏi base payload, chỉ gán khi `!empty($data['code'])` → update không gửi code thì KHÔNG ghi đè mã cũ thành null (bug tiềm ẩn trước đây bị rule `required` che).
- [x] `store()`: `empty($payload['code'])` → `Solution::getNextCode(...)`.

### Verify (empirical, tinker + DB local, 2026-07-16)
- [x] `php -l` sạch 3 file BE.
- [x] `getNextCode(25)` → `HN_DA.UD.0134.2026.DA003_GP12`; `getNextCode(null)` → `_GP12`. Khớp format FE.
- [x] Validate payload KHÔNG có `code` (qua `SolutionRequest::rules()` thật) → PASS, không còn lỗi `code`.
- [x] E2E `store()` thật, payload không gửi code → tạo OK, code sinh `HN_KD2.UD.0100.2026.DA001_GP12`. Chạy trong `beginTransaction()` + `rollBack()`, DB giữ nguyên 11 bản ghi.
- [x] E2E `update()` không gửi code → mã giữ nguyên `HN_NSHC.UD.EHS1.2026.DA001_GP02`, không bị null.
- [ ] Test UI thật `/assign/solutions/add` → Lưu nháp / Lưu và gửi. CHƯA CHẠY (cần xác nhận nhánh đang chạy `:3000`).

### Còn treo
- Bug 3 (emit sai tên) VẪN CÒN trên FE — BE đã miễn nhiễm, nhưng `updateField()` là hàm dùng chung của InfoTab: mọi field đi qua nó đều mất (hiện chỉ `code` + `request_solution_id` dùng). Cần quyết định sửa FE hay không ở phiên sau.
- Sửa BE đang nằm trên `tpe` local (sau origin/tpe 16 commit) → khi pull/merge `origin/tpe` sẽ đụng `normalizePayload` (commit `8cedc99d5` sửa cùng hàm). Cần rebase thủ công.

## Liên quan
- `.plans/fix-solution-list-master-data-source/plan.md` — fix cột list đọc theo `solutions.*_id`. Là tiền đề: chỉ sau khi cả 2 fix xong thì lựa chọn của user mới hiển thị đúng xuyên suốt list → edit → show.
