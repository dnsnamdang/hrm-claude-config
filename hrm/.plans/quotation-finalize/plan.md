# Chốt / Hủy chốt báo giá — Implementation Plan

> **Phụ trách:** @khoipv
> **Spec:** `.plans/quotation-finalize/design.md`
> **Lưu ý:** KHÔNG commit/push (theo CLAUDE.md). Đánh `[x]` mỗi task khi xong. Verify bằng thao tác thủ công + log `hrm-api/storage/logs/laravel-[ngày].log`.

**Goal:** Thêm thao tác Chốt / Hủy chốt báo giá (trạng thái Trúng thầu) cho tab Báo giá trong màn chi tiết dự án tiền khả thi.

**Architecture:** BE thêm 1 trạng thái `Trúng thầu (7)` + 2 method service `finalize`/`unfinalize` (đổi status + ghi `quotation_histories`), gate isSaleOfProject ở controller. FE thêm 2 icon-button vào row action của tab + modal nhập lý do hủy chốt. Không migration, không permission mới.

**Tech Stack:** Laravel 8 (Modules/Assign), Nuxt 2 (Vue 2 + Bootstrap-Vue).

---

## Phase 1 — Backend

### Task 1: Thêm trạng thái Trúng thầu

**Files:**
- Modify: `hrm-api/Modules/Assign/Entities/Quotation.php`

- [ ] **Step 1: Thêm hằng trạng thái** (sau `const STATUS_DUNG = 6;`, ~dòng 18)

```php
    const STATUS_TRUNG_THAU = 7;
```

- [ ] **Step 2: Thêm vào `getStatusList()`** (sau dòng `STATUS_DUNG`)

```php
            self::STATUS_TRUNG_THAU => ['name' => 'Trúng thầu', 'color' => '#D4AF37'],
```

- [ ] **Step 3: Verify** — không lỗi syntax:

```bash
php -l hrm-api/Modules/Assign/Entities/Quotation.php
```
Expected: `No syntax errors detected`

---

### Task 2: Thêm action lịch sử finalize / unfinalize

**Files:**
- Modify: `hrm-api/Modules/Assign/Entities/QuotationHistory.php`

- [ ] **Step 1: Thêm 2 hằng action** (sau `const ACTION_UPDATE_DISCOUNT = 'update_discount';`)

```php
    const ACTION_FINALIZE = 'finalize';
    const ACTION_UNFINALIZE = 'unfinalize';
```

- [ ] **Step 2: Thêm vào `ACTION_LABELS`** (trước dấu `]` đóng mảng)

```php
        'finalize' => 'Chốt báo giá (Trúng thầu)',
        'unfinalize' => 'Hủy chốt',
```

- [ ] **Step 3: Thêm vào `ACTION_COLORS`** (trước dấu `]` đóng mảng)

```php
        'finalize' => '#D4AF37',
        'unfinalize' => '#EF4444',
```

- [ ] **Step 4: Verify**

```bash
php -l hrm-api/Modules/Assign/Entities/QuotationHistory.php
```
Expected: `No syntax errors detected`

---

### Task 3: FormRequest validate lý do hủy chốt

**Files:**
- Create: `hrm-api/Modules/Assign/Http/Requests/Quotation/QuotationUnfinalizeRequest.php`

- [ ] **Step 1: Tạo file** (mirror `QuotationRejectRequest`)

```php
<?php

namespace Modules\Assign\Http\Requests\Quotation;

use Illuminate\Foundation\Http\FormRequest;

class QuotationUnfinalizeRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            'reason' => 'required|string|max:1000',
        ];
    }

    public function messages(): array
    {
        return [
            'reason.required' => 'Vui lòng nhập lý do hủy chốt.',
        ];
    }
}
```

- [ ] **Step 2: Verify**

```bash
php -l hrm-api/Modules/Assign/Http/Requests/Quotation/QuotationUnfinalizeRequest.php
```
Expected: `No syntax errors detected`

---

### Task 4: Service finalize / unfinalize

**Files:**
- Modify: `hrm-api/Modules/Assign/Services/QuotationService.php` (thêm 2 public method, đặt sau `reject()` ~dòng 1386)

- [ ] **Step 1: Thêm method `finalize()`**

```php
    public function finalize(Quotation $quotation): Quotation
    {
        if ($quotation->status !== Quotation::STATUS_DA_DUYET) {
            throw new \Exception('Chỉ chốt được báo giá đã duyệt.');
        }

        return DB::transaction(function () use ($quotation) {
            $exists = Quotation::where('project_id', $quotation->project_id)
                ->where('status', Quotation::STATUS_TRUNG_THAU)
                ->where('id', '!=', $quotation->id)
                ->lockForUpdate()
                ->exists();
            if ($exists) {
                throw new \Exception('Dự án đã có báo giá trúng thầu, vui lòng hủy chốt trước.');
            }

            $oldStatus = $quotation->status;
            $quotation->update(['status' => Quotation::STATUS_TRUNG_THAU]);

            $this->logHistory(
                $quotation->id,
                QuotationHistory::ACTION_FINALIZE,
                $oldStatus,
                Quotation::STATUS_TRUNG_THAU
            );

            return $quotation->fresh();
        });
    }
```

- [ ] **Step 2: Thêm method `unfinalize()`**

```php
    public function unfinalize(Quotation $quotation, string $reason): Quotation
    {
        if ($quotation->status !== Quotation::STATUS_TRUNG_THAU) {
            throw new \Exception('Báo giá chưa ở trạng thái trúng thầu.');
        }
        if (trim($reason) === '') {
            throw new \Exception('Vui lòng nhập lý do hủy chốt.');
        }

        return DB::transaction(function () use ($quotation, $reason) {
            $oldStatus = $quotation->status;
            $quotation->update(['status' => Quotation::STATUS_DA_DUYET]);

            $this->logHistory(
                $quotation->id,
                QuotationHistory::ACTION_UNFINALIZE,
                $oldStatus,
                Quotation::STATUS_DA_DUYET,
                ['reason' => $reason],
                $reason
            );

            return $quotation->fresh();
        });
    }
```

- [ ] **Step 3: Verify** — `Quotation`, `QuotationHistory`, `DB` đã được import sẵn ở đầu file (đã dùng trong `reject`/`bgdApprove`). Chạy:

```bash
php -l hrm-api/Modules/Assign/Services/QuotationService.php
```
Expected: `No syntax errors detected`

---

### Task 5: Controller finalize / unfinalize (gate isSaleOfProject)

**Files:**
- Modify: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/QuotationController.php`

- [ ] **Step 1: Import FormRequest mới** — thêm vào khối `use` cùng chỗ với `QuotationRejectRequest`

```php
use Modules\Assign\Http\Requests\Quotation\QuotationUnfinalizeRequest;
```

- [ ] **Step 2: Thêm 2 method** (đặt sau `reject()` ~dòng 240)

```php
    public function finalize($id)
    {
        try {
            $item = Quotation::findOrFail($id);
            $this->ensureSaleOfProject($item->project_id);
            $updated = $this->service->finalize($item);
            return $this->responseJson('Đã chốt báo giá (Trúng thầu)', Response::HTTP_OK, ['id' => $updated->id]);
        } catch (Exception $e) {
            Log::error($e);
            return $this->responseJson($e->getMessage(), Response::HTTP_UNPROCESSABLE_ENTITY);
        }
    }

    public function unfinalize(QuotationUnfinalizeRequest $request, $id)
    {
        try {
            $item = Quotation::findOrFail($id);
            $this->ensureSaleOfProject($item->project_id);
            $updated = $this->service->unfinalize($item, $request->validated()['reason']);
            return $this->responseJson('Đã hủy chốt báo giá', Response::HTTP_OK, ['id' => $updated->id]);
        } catch (Exception $e) {
            Log::error($e);
            return $this->responseJson($e->getMessage(), Response::HTTP_UNPROCESSABLE_ENTITY);
        }
    }

    /**
     * Chỉ Sale phụ trách dự án (main_sale_employee_id) mới được thao tác.
     * (Tái dùng pattern gate ở store()).
     */
    private function ensureSaleOfProject($projectId): void
    {
        $project = \Modules\Assign\Entities\ProspectiveProject::findOrFail($projectId);
        $user = auth()->user();
        $emp = \Modules\Human\Entities\Employee::where('employee_info_id', $user->employee_info_id)->first();
        $employeeId = $emp ? (int) $emp->id : null;
        if (!$employeeId || (int) $project->main_sale_employee_id !== $employeeId) {
            abort(403, 'Bạn không phải Sale phụ trách dự án này');
        }
    }
```

> Lưu ý: `QuotationUnfinalizeRequest` validate `reason` rỗng → tự ném `ValidationException` (422) trước khi vào try/catch, FE nhận lỗi inline. Block "đã có trúng thầu" và sai trạng thái → ném từ service, trả 422 với message.

- [ ] **Step 3: Verify**

```bash
php -l hrm-api/Modules/Assign/Http/Controllers/Api/V1/QuotationController.php
```
Expected: `No syntax errors detected`

---

### Task 6: Routes

**Files:**
- Modify: `hrm-api/Modules/Assign/Routes/api.php` (nhóm `/assign/quotations`, sau dòng `reject` ~dòng 398)

- [ ] **Step 1: Thêm 2 route** (không middleware — không có permission tương ứng)

```php
        Route::post('/{id}/finalize', [QuotationController::class, 'finalize']);
        Route::post('/{id}/unfinalize', [QuotationController::class, 'unfinalize']);
```

- [ ] **Step 2: Verify** — route đã đăng ký:

```bash
cd hrm-api && php artisan route:list --path=assign/quotations | grep -i "finalize"
```
Expected: thấy 2 dòng `finalize` và `unfinalize` (POST)

---

## Phase 2 — Frontend

### Task 7: Thêm nút Chốt / Hủy chốt + hằng trạng thái

**Files:**
- Modify: `hrm-client/pages/assign/prospective-projects/components/ProspectiveProjectQuotationsTab.vue`

- [ ] **Step 1: Thêm 2 hằng trạng thái** trong `data()` (hoặc dùng trực tiếp số — ở đây thêm vào `data` để rõ nghĩa). Thêm vào object trả về của `data()`:

```js
            STATUS_BG_DA_DUYET: 4,
            STATUS_BG_TRUNG_THAU: 7,
            unfinalizeModal: { show: false, id: null, code: '', reason: '', touched: false, saving: false },
```

- [ ] **Step 2: Thêm 2 icon-button** trong `<template #actions>` của `V2BaseTitleSubInfo` (trong `#cell-code`), đặt sau nút "Sửa ghi chú kinh doanh" (~dòng 73), trước nút "Xuất Excel":

```html
                        <button
                            v-if="item.status === STATUS_BG_DA_DUYET && isSaleOfProject"
                            class="btn btn-light border btn-sm mr-1 text-warning"
                            v-b-tooltip.hover.top="'Chốt báo giá (Trúng thầu)'"
                            @click="handleFinalize(item)"
                        >
                            <i class="ri-trophy-line"></i>
                        </button>
                        <button
                            v-if="item.status === STATUS_BG_TRUNG_THAU && isSaleOfProject"
                            class="btn btn-light border btn-sm mr-1 text-warning"
                            v-b-tooltip.hover.top="'Hủy chốt'"
                            @click="openUnfinalizeModal(item)"
                        >
                            <i class="ri-arrow-go-back-line"></i>
                        </button>
```

- [ ] **Step 3: Verify** — `npm run dev` không lỗi compile; mở tab Báo giá của dự án mình là sale chính: báo giá Đã duyệt thấy nút 🏆, báo giá khác không thấy.

---

### Task 8: Logic Chốt (confirm) + modal Hủy chốt (lý do bắt buộc)

**Files:**
- Modify: `hrm-client/pages/assign/prospective-projects/components/ProspectiveProjectQuotationsTab.vue`

- [ ] **Step 1: Thêm các method** vào object `methods` (sau `handleDelete`):

```js
        async handleFinalize(item) {
            const ok = await this.$bvModal.msgBoxConfirm(
                `Chốt báo giá "${item.code}" thành Trúng thầu? Mỗi dự án chỉ có 1 báo giá trúng thầu.`,
                { title: 'Xác nhận chốt báo giá', okVariant: 'warning', okTitle: 'Chốt', cancelTitle: 'Huỷ', centered: true },
            )
            if (!ok) return
            try {
                await this.$store.dispatch('apiPostMethod', {
                    url: `assign/quotations/${item.id}/finalize`,
                    payload: {},
                })
                this.$toasted?.global?.success?.({ message: 'Đã chốt báo giá (Trúng thầu)' })
                this.loadData()
            } catch (e) {
                this.$toasted?.global?.error?.({ message: e?.response?.data?.message || 'Lỗi chốt báo giá' })
            }
        },
        openUnfinalizeModal(item) {
            this.unfinalizeModal = { show: true, id: item.id, code: item.code, reason: '', touched: false, saving: false }
        },
        async submitUnfinalize() {
            this.unfinalizeModal.touched = true
            if (!this.unfinalizeModal.reason.trim()) return
            this.unfinalizeModal.saving = true
            try {
                await this.$store.dispatch('apiPostMethod', {
                    url: `assign/quotations/${this.unfinalizeModal.id}/unfinalize`,
                    payload: { reason: this.unfinalizeModal.reason },
                })
                this.$toasted?.global?.success?.({ message: 'Đã hủy chốt báo giá' })
                this.unfinalizeModal.show = false
                this.loadData()
            } catch (e) {
                this.$toasted?.global?.error?.({ message: e?.response?.data?.message || 'Lỗi hủy chốt' })
            } finally {
                this.unfinalizeModal.saving = false
            }
        },
```

> Kiểm tra tên action store: `apiPostMethod` nhận `{ url, payload }` (giống `apiPutMethod` đang dùng ở `saveSalesNote`). Nếu store dùng tên khác cho POST, chỉnh lại cho khớp `store/index.js`.

- [ ] **Step 2: Thêm modal Hủy chốt** trong `<template>`, sau modal "Sales note" (sau `</b-modal>` ~dòng 137):

```html
        <!-- Unfinalize reason modal -->
        <b-modal
            :visible="unfinalizeModal.show"
            title="Hủy chốt báo giá"
            centered
            :hide-footer="true"
            @hidden="unfinalizeModal.show = false"
        >
            <p class="mb-2">Hủy chốt báo giá <b>{{ unfinalizeModal.code }}</b> — báo giá sẽ quay lại trạng thái "Đã duyệt".</p>
            <V2BaseLabel>Lý do hủy chốt <span class="text-danger">*</span></V2BaseLabel>
            <V2BaseTextarea
                v-model="unfinalizeModal.reason"
                rows="4"
                placeholder="Nhập lý do hủy chốt..."
                :class="{ 'is-invalid': unfinalizeModal.touched && !unfinalizeModal.reason.trim() }"
            />
            <div v-if="unfinalizeModal.touched && !unfinalizeModal.reason.trim()" class="invalid-feedback d-block">
                Vui lòng nhập lý do hủy chốt.
            </div>
            <div class="d-flex justify-content-end mt-3">
                <button class="btn btn-secondary mr-2" :disabled="unfinalizeModal.saving" @click="unfinalizeModal.show = false">Huỷ</button>
                <button class="btn btn-warning" :disabled="unfinalizeModal.saving" @click="submitUnfinalize">
                    {{ unfinalizeModal.saving ? 'Đang lưu...' : 'Xác nhận hủy chốt' }}
                </button>
            </div>
        </b-modal>
```

- [ ] **Step 3: Verify thủ công** (đăng nhập bằng tài khoản sale chính của dự án):
  - Báo giá Đã duyệt → bấm 🏆 → confirm → status đổi "Trúng thầu", badge vàng.
  - Bấm 🏆 trên báo giá Đã duyệt khác cùng dự án → toast lỗi "Dự án đã có báo giá trúng thầu...".
  - Báo giá Trúng thầu → bấm ↩️ → modal; để trống lý do bấm Xác nhận → viền đỏ + text lỗi; nhập lý do → status quay lại "Đã duyệt".
  - Tài khoản KHÔNG phải sale chính → không thấy 2 nút.

---

### Task 9: Map trạng thái mới trong modal Lịch sử thay đổi (fix)

**Files:**
- Modify: `hrm-client/components/assign/quotation/QuotationHistoryModal.vue`

Lý do: modal lịch sử map `from_status`/`to_status` → tên qua `STATUS_LABELS` cục bộ (thiếu 6, 7) và icon qua `ICON_MAP` (thiếu finalize/unfinalize) → khi chốt hiện "Đã duyệt → —".

- [x] **Step 1: Bổ sung `STATUS_LABELS`** — thêm `6: 'Dừng'`, `7: 'Trúng thầu'`.
- [x] **Step 2: Bổ sung `ICON_MAP`** — `finalize: 'ri-trophy-line'`, `unfinalize: 'ri-arrow-go-back-line'`.
- [x] **Step 3: Verify** — lịch sử hiển thị "Đã duyệt → Trúng thầu" (chốt) / "Trúng thầu → Đã duyệt" (hủy chốt); lý do hủy chốt hiện qua `h.meta.reason` (đã có sẵn ở template).

### Task 10: Ẩn nút Chốt khi dự án đã có báo giá trúng thầu

**Files:**
- Modify: `hrm-api/Modules/Assign/Http/Controllers/Api/V1/QuotationController.php` (`byProject`)
- Modify: `hrm-client/pages/assign/prospective-projects/components/ProspectiveProjectQuotationsTab.vue`

Yêu cầu: khi dự án đã có 1 báo giá Trúng thầu thì ẩn hết nút Chốt của các báo giá khác (phải Hủy chốt trước). Dùng cờ BE để đúng cả khi báo giá trúng thầu nằm ở trang khác (phân trang).

- [x] **Step 1 (BE):** `byProject` thêm `$hasWonQuotation = Quotation::where('project_id',...)->where('status', STATUS_TRUNG_THAU)->exists();` và trả qua `apiGetList($data, ['has_won_quotation' => $hasWonQuotation])` (merge vào top-level response). `php -l` PASS.
- [x] **Step 2 (FE):** thêm state `hasWonQuotation: false`; trong `loadData` gán `this.hasWonQuotation = res?.has_won_quotation || false`.
- [x] **Step 3 (FE):** nút Chốt thêm điều kiện `&& !hasWonQuotation`. Nút Hủy chốt giữ nguyên (chỉ hiện trên báo giá status 7).
- [x] **Step 4: Verify** — sau khi chốt 1 báo giá: các báo giá Đã duyệt khác mất nút 🏆; chỉ báo giá Trúng thầu có ↩️. Hủy chốt xong → nút 🏆 xuất hiện lại.

### Task 11: Thêm nút "Lịch sử phê duyệt" vào tab Báo giá

**Files:**
- Modify: `hrm-client/pages/assign/prospective-projects/components/ProspectiveProjectQuotationsTab.vue`

Yêu cầu: bê nút xem lịch sử phê duyệt giống màn danh sách báo giá (`pages/assign/quotations/index.vue`) vào tab. Tái dùng component `QuotationHistoryModal` (props `:show` + `:quotationId`, emit `@close`).

- [x] Import + đăng ký `QuotationHistoryModal` (`@/components/assign/quotation/QuotationHistoryModal.vue`).
- [x] State: `historyModalShow: false`, `historyQuotationId: null`.
- [x] Nút icon `ri-history-line` tooltip "Lịch sử phê duyệt" trong row action (sau Hủy chốt, trước Xuất Excel) → `openHistoryModal(item.id)`. Hiện cho mọi báo giá.
- [x] Method `openHistoryModal(id)` set `historyQuotationId` + mở modal.
- [x] Đặt `<QuotationHistoryModal>` trong template (sau modal Hủy chốt).
- [x] Verify: lịch sử hiển thị đầy đủ các action gồm finalize/unfinalize (đã map ở Task 9).

### Task 12: Thêm trạng thái "Trúng thầu" vào bộ lọc màn danh sách báo giá

**Files:**
- Modify: `hrm-client/pages/assign/quotations/index.vue`

- [x] Thêm `{ value: 7, label: 'Trúng thầu' }` vào `statusOptions`.
- [x] Verify BE: `applyListFilters` lọc `where('status', value)` không whitelist → giá trị 7 hoạt động, không cần sửa BE. Badge cột trạng thái tự hiển thị qua `getStatusList()` (Task 1).

---

## Checkpoint

### Checkpoint — 2026-06-04
Vừa hoàn thành: **CODE DONE toàn bộ 8 task** (Phase 1 BE: tasks 1-6; Phase 2 FE: tasks 7-8). Tất cả `php -l` PASS, code khớp spec 100% (đã review compliance từng phase).
Đang làm dở: —
Bước tiếp theo: User chạy `hrm-api` + `hrm-client` (`npm run dev`) và verify browser theo Task 8 Step 3:
- Tài khoản sale chính: báo giá Đã duyệt → 🏆 confirm → Trúng thầu (badge vàng). Bấm 🏆 báo giá khác cùng dự án → toast "Dự án đã có báo giá trúng thầu...". Báo giá Trúng thầu → ↩️ → để trống lý do = viền đỏ + text lỗi; nhập lý do → quay lại Đã duyệt.
- Tài khoản KHÔNG phải sale chính → không thấy 2 nút.
Blocked: `php artisan route:list` không chạy được do module Decision lỗi sẵn (không liên quan feature) — đã verify route bằng mắt.
