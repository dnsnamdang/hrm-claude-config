# PXL hiển thị SL đã xử lý của các phiếu trước + chặn vượt đề xuất — Plan

@khoipv — Bắt đầu 01/10/2026 · Design: [design.md](design.md) · Spec: [docs/superpowers/specs/2026-10-01-pxl-hien-thi-da-xu-ly-phieu-truoc-design.md](../../docs/superpowers/specs/2026-10-01-pxl-hien-thi-da-xu-ly-phieu-truoc-design.md)

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development hoặc superpowers:executing-plans. Đánh `[x]` từng step.
> **KHÔNG commit / push** (CLAUDE.md) — user tự commit. Không có bước commit trong plan.

**Goal:** Người lập PXL sau thấy `[còn lại] / SL đề xuất` + popover các PXL khác đã xử lý gì; FE + BE chặn cứng khi gửi chính thức vượt đề xuất / phân bổ vượt đặt đơn.

**Architecture:** BE thêm 1 hàm đọc lịch sử (`handledHistoryByProduct`) expose qua 2 resource chi tiết, và 1 guard (`guardProposalLimit`) gọi trong `store/update` có `lockForUpdate` đề xuất. FE thêm component popover, hiển thị `x / y` trong `HandlingGoodsTable`, `add.vue` tính lỗi L1/L2 một chỗ rồi truyền xuống bảng + chặn `submit`.

**Tech Stack:** Laravel 8 / PHP 7.4 (module `Modules/Supply`), Nuxt 2 / Vue 2 + Bootstrap-Vue (`b-popover`).

## Global Constraints

- Không migration, không đổi schema.
- Nháp (status 1) + Từ chối duyệt (status 7) **không** tính là đã xử lý — dùng `SupplyProposal::inactiveHandlingStatuses()`.
- ε so sánh SL = `SupplyProposalService::QTY_EPSILON` (0.0005) ở BE, `0.0005` ở FE.
- Chỉ kiểm tra khi gửi chính thức; "Lưu nháp" không kiểm tra. Không kiểm tra lại khi duyệt.
- Cảnh báo "vượt SL còn lại theo HĐ" (`overContractRows`) giữ nguyên — chỉ cảnh báo.
- Không đổi `syncHandledStatus`, `handledDetailByProduct`, export Excel.
- PHP 7.4: không dùng `match`, named args, nullsafe `?->`; arrow fn `fn()` được.

## Review Focus

1. **2 người gửi cùng lúc** — người gửi sau phải bị chặn với message "tải lại trang", không được lưu vượt → Task 3 Step 4 (case 5).
2. **Sửa PXL đã gửi** — phần còn lại phải loại chính phiếu đó ra, nếu không sửa phiếu không đổi số cũng bị chặn → Task 3 Step 4 (case 4).
3. **Khối đổi hàng + dòng giữ A cùng `product_id`** — L1 phải cộng chung (dat_don dòng A + swap_origin_quantity dòng đổi) → Task 3 Step 4 (case 3) + Task 7 Step 3.
4. **Dòng đổi hàng L2** — so phân bổ với `swap_quantity` (ĐVT B), không với SL A → Task 3 Step 4 (case 2).
5. **Lưu nháp với số vượt** — phải lưu được, và gửi nháp đi sau đó mới bị chặn → Task 3 Step 4 (case 6).

---

## Phase 1 — BE (`hrm-thanhan-api/Modules/Supply`)

### Task 1: `handledHistoryByProduct()` — lịch sử xử lý theo hàng gốc A

**Files:**
- Modify: `Services/SupplyProposalService.php` — thêm method ngay sau `handledDetailByProduct()` (~dòng 1972)

**Interfaces:**
- Produces: `SupplyProposalService::handledHistoryByProduct($proposalId, $excludeHandlingId = null): array`
  → `[int product_id => [ ['handling_id'=>int,'code'=>string,'status'=>int,'status_name'=>string,'creator_name'=>string,'created_at'=>'d/m/Y','lines'=>[['swap_product_id'=>?int,'swap_product_code'=>?string,'swap_unit_name'=>?string,'unit_name'=>?string,'dat_don'=>float,'swap_origin_quantity'=>?float,'allocs'=>[['key','label','qty'=>float]],'qty_a'=>float]],'qty_a'=>float], ... ]]`

- [x] **Step 1: Thêm method**

```php
    /**
     * Lịch sử xử lý của 1 đề xuất theo hàng gốc A — popover "Phiếu xử lý khác" ở bảng PXL
     * (spec 2026-10-01-pxl-hien-thi-da-xu-ly-phieu-truoc §6.1).
     * Cùng điều kiện lọc với handledDetailByProduct (bỏ Nháp / Từ chối duyệt, loại $excludeHandlingId)
     * và cùng công thức quy về A, nên Σ qty_a ở đây khớp 'qty_a' bên đó. 2 query, không N+1.
     * Dòng không phân bổ gì (không đóng góp "đã xử lý") bị bỏ; phiếu không còn dòng của A thì không hiện.
     */
    public function handledHistoryByProduct($proposalId, $excludeHandlingId = null): array
    {
        if (empty($proposalId)) {
            return [];
        }

        $handlings = \Modules\Supply\Entities\SupplyHandling::query()
            ->with('employee_create.info')
            ->where('supply_proposal_id', $proposalId)
            ->whereNotIn('status', SupplyProposal::inactiveHandlingStatuses())
            ->when($excludeHandlingId, fn($q) => $q->where('id', '!=', $excludeHandlingId))
            ->orderBy('created_at')
            ->orderBy('id')
            ->get();

        if ($handlings->isEmpty()) {
            return [];
        }

        $linesByHandling = \Modules\Supply\Entities\SupplyHandlingProduct::query()
            ->whereIn('supply_handling_id', $handlings->pluck('id')->all())
            ->orderBy('id')
            ->get()
            ->groupBy('supply_handling_id');

        $statusNames = collect(\Modules\Supply\Entities\SupplyHandling::STATUSES)->pluck('name', 'id');

        $out = [];
        foreach ($handlings as $h) {
            $byProduct = [];
            foreach ($linesByHandling->get($h->id, collect()) as $l) {
                $allocs = [];
                $sum = 0.0;
                foreach (\Modules\Supply\Entities\SupplyHandling::ALLOC_TYPES as $a) {
                    $v = (float) $l->{'alloc_' . $a['key']};
                    if (abs($v) > self::QTY_EPSILON) {
                        $allocs[] = ['key' => $a['key'], 'label' => $a['label'], 'qty' => $v];
                        $sum += $v;
                    }
                }
                if ($sum <= self::QTY_EPSILON) {
                    continue;
                }

                $datDon = (float) $l->dat_don;
                $qtyA = $l->swap_product_id
                    ? ($datDon > 0 ? (float) $l->swap_origin_quantity * $sum / $datDon : 0.0)
                    : $sum;

                $byProduct[(int) $l->product_id][] = [
                    'swap_product_id'      => $l->swap_product_id ? (int) $l->swap_product_id : null,
                    'swap_product_code'    => $l->swap_product_code,
                    'swap_unit_name'       => $l->swap_unit_name,
                    'unit_name'            => $l->unit_name,
                    'dat_don'              => $datDon,
                    'swap_origin_quantity' => is_null($l->swap_origin_quantity) ? null : (float) $l->swap_origin_quantity,
                    'allocs'               => $allocs,
                    'qty_a'                => round($qtyA, 3),
                ];
            }

            foreach ($byProduct as $productId => $lines) {
                $out[$productId][] = [
                    'handling_id'  => $h->id,
                    'code'         => $h->code,
                    'status'       => (int) $h->status,
                    'status_name'  => $statusNames[(int) $h->status] ?? '',
                    'creator_name' => optional($h->employee_create)->info ? $h->employee_create_name : '',
                    'created_at'   => \Modules\Human\Helper\Helper::formatDate($h->created_at),
                    'lines'        => $lines,
                    'qty_a'        => round(array_sum(array_column($lines, 'qty_a')), 3),
                ];
            }
        }

        return $out;
    }
```

- [x] **Step 2: Lint** — `php -l Modules/Supply/Services/SupplyProposalService.php` → `No syntax errors detected`.

- [x] **Step 3: Đối chiếu với `handledDetailByProduct`** — script tinker trong scratchpad (chỉ đọc):

```php
// scratchpad/check_history.php — chạy: php artisan tinker < <path>
$s = app(\Modules\Supply\Services\SupplyProposalService::class);
$pid = \Modules\Supply\Entities\SupplyHandling::whereNotIn('status',[1,7])
    ->groupBy('supply_proposal_id')->havingRaw('count(*) >= 2')->value('supply_proposal_id');
$h = $s->handledHistoryByProduct($pid); $d = $s->handledDetailByProduct($pid)['qty_a'];
foreach ($d as $p => $q) { $t = array_sum(array_column($h[$p] ?? [], 'qty_a')); echo "$p: detail=$q history=$t ".(abs($q-$t)<0.001?'OK':'LECH')."\n"; }
echo json_encode(array_slice($h, 0, 1, true), JSON_UNESCAPED_UNICODE|JSON_PRETTY_PRINT);
```
Expected: mọi dòng `OK`; JSON có `code`, `creator_name`, `status_name`, `allocs` đúng nhãn. Không có đề xuất ≥ 2 PXL thì lấy đề xuất có 1 PXL (bỏ `havingRaw`).

### Task 2: Expose `sl_de_xuat_a`, `sl_da_xu_ly_a`, `lich_su_xu_ly` ở 2 resource

**Files:**
- Modify: `Transformers/SupplyProposal/DetailSupplyProposalResource.php` (khối `'products'`, ~dòng 51–95)
- Modify: `Transformers/SupplyHandling/DetailSupplyHandlingResource.php` (khối `'products'`, ~dòng 63–125)

**Interfaces:**
- Consumes: Task 1 `handledHistoryByProduct()`.
- Produces (mỗi phần tử `products[]` của cả 2 API):
  `sl_de_xuat_a: float|null` (null = hàng không thuộc đề xuất), `sl_da_xu_ly_a: float`, `lich_su_xu_ly: array` (entry của Task 1).
  `DetailSupplyProposalResource` đã có `sl_da_xu_ly_a` — giữ nguyên.

- [x] **Step 1: `DetailSupplyProposalResource`** — trong closure `'products'`, sau dòng `$variants = $handled['variants'];` thêm:

```php
                // Popover "Phiếu xử lý khác" + mốc "/ SL đề xuất" ở bảng PXL (spec 2026-10-01 §6.2).
                $history    = $service->handledHistoryByProduct($this->id);
                $proposedA  = $this->products->groupBy('product_id')
                    ->map(fn($g) => (float) $g->sum('quantity'));
```
  thêm `$history, $proposedA` vào `use (...)` của `map(function ($p) use (...))`, và trong mảng trả về, ngay sau `'sl_da_xu_ly_a'`:

```php
                        // SL đề xuất của hàng gốc A (Σ mọi dòng cùng product_id, ĐVT A) — mốc "x / y" ở PXL
                        'sl_de_xuat_a'    => (float) ($proposedA[$p->product_id] ?? 0),
                        // Các PXL đã xử lý hàng gốc A này (bỏ nháp / từ chối duyệt)
                        'lich_su_xu_ly'   => $history[$p->product_id] ?? [],
```

- [x] **Step 2: `DetailSupplyHandlingResource`** — sau dòng `$variants = $handled['variants'];` thêm:

```php
                // Các PXL KHÁC đã xử lý từng hàng gốc A (loại chính phiếu này) — popover ở bảng PXL.
                $history    = $service->handledHistoryByProduct($this->supply_proposal_id, $this->id);
```
  thêm `$history` vào `use (...)`, và ngay sau `'sl_con_de_xuat_a' => ...,` thêm:

```php
                        // SL đề xuất A + SL các PXL khác đã xử lý (quy về A); null = hàng không thuộc đề xuất.
                        'sl_de_xuat_a'     => isset($proposedA[$p->product_id]) ? (float) $proposedA[$p->product_id] : null,
                        'sl_da_xu_ly_a'    => (float) ($handledA[$p->product_id] ?? 0),
                        'lich_su_xu_ly'    => $history[$p->product_id] ?? [],
```

- [x] **Step 3: Lint** 2 file → `No syntax errors detected`.

- [x] **Step 4: Kiểm tra output** — tinker:

```php
$h = \Modules\Supply\Entities\SupplyHandling::whereNotIn('status',[1,7])->latest('id')->first();
$h->load('products','proposal.files','proposal.employee_create.info');
$r = (new \Modules\Supply\Transformers\SupplyHandling\DetailSupplyHandlingResource($h))->toArray(request());
echo json_encode(collect($r['products'])->map(fn($p)=>array_intersect_key($p, array_flip(['product_code','sl_de_xuat_a','sl_da_xu_ly_a','sl_con_de_xuat_a','lich_su_xu_ly'])))->take(2), JSON_UNESCAPED_UNICODE|JSON_PRETTY_PRINT);
$p = $h->proposal;
$r2 = (new \Modules\Supply\Transformers\SupplyProposal\DetailSupplyProposalResource($p))->toArray(request());
echo json_encode(collect($r2['products'])->map(fn($x)=>array_intersect_key($x, array_flip(['product_code','quantity','sl_de_xuat_a','sl_da_xu_ly_a','lich_su_xu_ly'])))->take(2), JSON_UNESCAPED_UNICODE|JSON_PRETTY_PRINT);
```
Expected: resource PXL — `lich_su_xu_ly` **không** chứa `handling_id = $h->id`; `sl_con_de_xuat_a == max(sl_de_xuat_a - sl_da_xu_ly_a, 0)`. Resource đề xuất — `lich_su_xu_ly` có cả `$h->id`.

### Task 3: `guardProposalLimit()` — chặn L1/L2 khi gửi chính thức

**Files:**
- Modify: `Services/SupplyHandlingService.php` — thêm `use Modules\Supply\Entities\SupplyProposalProduct;`, method mới cuối class, gọi trong `store()` + `update()`.

**Interfaces:**
- Consumes: `SupplyProposalService::handledDetailByProduct()` (có sẵn), `SupplyProposalService::QTY_EPSILON`, trait `hasSwap()`.
- Produces: `private function guardProposalLimit(SupplyProposal $proposal, $items, $excludeHandlingId = null): void` — ném `\Exception` (controller → HTTP 400 `message`).

- [x] **Step 1: Thêm method** (cuối class, trước `}` đóng):

```php
    /**
     * Chặn vượt đề xuất khi gửi chính thức (spec 2026-10-01-pxl-hien-thi-da-xu-ly-phieu-truoc §4, §6.3):
     *  L2 — mỗi dòng: Σ phân bổ ≤ SL đặt đơn (dòng đổi so theo swap_quantity — ĐVT của B, như syncProducts ép).
     *  L1 — mỗi hàng gốc A thuộc đề xuất: Σ SL quy về A (giữ A: dat_don; đổi: swap_origin_quantity)
     *       ≤ SL đề xuất A − SL các PXL khác đã xử lý (handledDetailByProduct, loại $excludeHandlingId).
     * Khóa dòng đề xuất (controller đã bọc DB::transaction) → 2 người gửi cùng lúc chạy tuần tự,
     * người sau đọc được phiếu người trước vừa lưu.
     */
    private function guardProposalLimit(SupplyProposal $proposal, $items, $excludeHandlingId = null): void
    {
        SupplyProposal::whereKey($proposal->id)->lockForUpdate()->first();

        $items  = is_array($items) ? $items : [];
        $eps    = SupplyProposalService::QTY_EPSILON;
        $fmt    = fn($n) => rtrim(rtrim(number_format((float) $n, 3, ',', '.'), '0'), ',');
        $label  = fn($it) => ($it['product_code'] ?? '') ?: ($it['product_name'] ?? '');
        $errors = [];

        // L2
        foreach ($items as $it) {
            $datDon = $this->hasSwap($it) ? (float) ($it['swap_quantity'] ?? 0) : (float) ($it['dat_don'] ?? 0);
            $alloc  = 0.0;
            foreach (self::ALLOC_KEYS as $key) {
                $alloc += (float) ($it['alloc_' . $key] ?? 0);
            }
            if ($alloc > $datDon + $eps) {
                $errors[] = sprintf('Hàng %s: phân bổ (%s) vượt SL đặt đơn (%s).', $label($it), $fmt($alloc), $fmt($datDon));
            }
        }

        // L1
        $proposedA = SupplyProposalProduct::query()
            ->where('supply_proposal_id', $proposal->id)
            ->groupBy('product_id')
            ->selectRaw('product_id, sum(quantity) as qty')
            ->pluck('qty', 'product_id');
        $handledA = app(SupplyProposalService::class)
            ->handledDetailByProduct($proposal->id, $excludeHandlingId)['qty_a'];

        $inputA = [];
        $labels = [];
        foreach ($items as $it) {
            $pid = (int) ($it['product_id'] ?? 0);
            if (!isset($proposedA[$pid])) {
                continue; // hàng chọn thêm, không thuộc đề xuất
            }
            $inputA[$pid] = ($inputA[$pid] ?? 0) + ($this->hasSwap($it)
                ? (float) ($it['swap_origin_quantity'] ?? 0)
                : (float) ($it['dat_don'] ?? 0));
            $labels[$pid] = $labels[$pid] ?? $label($it);
        }
        foreach ($inputA as $pid => $qty) {
            $remain = max((float) $proposedA[$pid] - (float) ($handledA[$pid] ?? 0), 0);
            if ($qty > $remain + $eps) {
                $errors[] = sprintf(
                    'Hàng %s: vượt SL còn lại theo đề xuất (còn %s, nhập %s). Có thể phiếu khác vừa được lưu, vui lòng tải lại trang.',
                    $labels[$pid], $fmt($remain), $fmt($qty)
                );
            }
        }

        if (!empty($errors)) {
            throw new \Exception(implode(' ', array_slice($errors, 0, 3)) . (count($errors) > 3 ? ' …' : ''));
        }
    }
```
  Thêm `use Modules\Supply\Entities\SupplyProposalProduct;` vào khối `use` đầu file (kiểm tra entity nằm ở `Modules/Supply/Entities/SupplyProposalProduct.php`).

- [x] **Step 2: Gọi trong `store()`** — ngay sau `$type = $this->resolveType(...)`:

```php
        // Gửi chính thức: chặn vượt đề xuất / phân bổ vượt đặt đơn. Lưu nháp không kiểm tra.
        if (!$this->isDraftRequest($request)) {
            $this->guardProposalLimit($proposal, $request->input('products', []));
        }
```

- [x] **Step 3: Gọi trong `update()`** — ngay sau khối tính `$type` / `$data['type']`, **trước** `if ($wasDraft && !$keepDraft)`:

```php
        // Mọi lần lưu không giữ nháp (gửi nháp đi, sửa phiếu đã gửi, gửi lại phiếu bị từ chối) đều kiểm tra;
        // phần còn lại tính sau khi loại chính phiếu này.
        if (!$keepDraft && $model->proposal) {
            $this->guardProposalLimit($model->proposal, $request->input('products', []), $model->id);
        }
```

- [x] **Step 4: Lint + script kiểm tra (rollback)** — `php -l` → OK. Script tinker trong scratchpad, bọc `DB::beginTransaction()` … `DB::rollBack()`, gọi qua reflection `guardProposalLimit` với đề xuất thật có ≥ 1 PXL đã gửi. In `OK`/`CHAN: <message>` cho từng case:

| # | Input | Expected |
|---|---|---|
| 1 | A `dat_don` = còn lại, alloc_mua = còn lại | OK |
| 2 | Dòng đổi: `swap_quantity` 10, alloc_xkho 12 | CHAN "phân bổ (12) vượt SL đặt đơn (10)" |
| 3 | A giữ: `dat_don` = còn lại; + dòng đổi cùng A: `swap_origin_quantity` 1 | CHAN "vượt SL còn lại theo đề xuất" (cộng chung) |
| 4 | Lấy chính các dòng của 1 PXL đã gửi, `$excludeHandlingId` = id phiếu đó | OK |
| 5 | Tạo PXL tạm (insert trong transaction) xử lý hết còn lại, rồi guard 1 PXL mới `dat_don` 1 | CHAN "còn 0, nhập 1" |
| 6 | Hàng không thuộc đề xuất, `dat_don` 999, alloc 999 | OK (không áp L1) |

- [x] **Step 5: Kiểm tra luồng nháp** — đọc lại `store()`/`update()`: `is_draft=1` khi tạo → không gọi guard; phiếu nháp lưu nháp tiếp (`$keepDraft`) → không gọi guard. (Case 6 Review Focus — test UI ở Phase 3.)

## Phase 2 — FE (`hrm-thanhan-client/pages/supply/supply_handlings`)

### Task 4: Component `HandledHistoryPopover.vue`

**Files:**
- Create: `components/HandledHistoryPopover.vue`

**Interfaces:**
- Consumes: entry `lich_su_xu_ly` (Task 2).
- Produces: `<HandledHistoryPopover :items="Array" :total="Number" :remain="Number" :proposed="Number" :unit-name="String" />`
  — render dòng "Đã xử lý X ⓘ · Còn Y" + `b-popover` hover trên icon.

- [x] **Step 1: Tạo file**

```vue
<template>
    <span class="hh-note">
        Đã xử lý {{ fmt(total) }}
        <i :id="tid" class="mdi mdi-information-outline hh-icon" tabindex="0"></i>
        · Còn {{ fmt(remain) }}
        <b-popover :target="tid" triggers="hover focus" placement="auto" custom-class="hh-popover">
            <div class="hh-title">Phiếu xử lý khác của đề xuất này</div>
            <div v-if="!items.length" class="hh-empty">Không có chi tiết.</div>
            <div v-for="h in items" :key="h.handling_id" class="hh-item">
                <div class="hh-head">
                    <a :href="linkOf(h)" target="_blank" rel="noopener">{{ h.code }}</a>
                    · {{ h.creator_name || '—' }} · {{ h.created_at }} · {{ h.status_name }}
                </div>
                <div v-for="(l, li) in h.lines" :key="li" class="hh-line">{{ lineText(l) }}</div>
            </div>
            <div class="hh-total">Tổng đã xử lý: {{ fmt(total) }} / {{ fmt(proposed) }} {{ unitName }}</div>
        </b-popover>
    </span>
</template>

<script>
// Popover "Phiếu xử lý khác" ở ô Đặt đơn / Thay cho hàng gốc của bảng PXL
// (spec 2026-10-01-pxl-hien-thi-da-xu-ly-phieu-truoc §5.1). items = lich_su_xu_ly từ BE.
export default {
    name: 'HandledHistoryPopover',
    props: {
        items: { type: Array, default: () => [] },
        total: { type: Number, default: 0 },
        remain: { type: Number, default: 0 },
        proposed: { type: Number, default: 0 },
        unitName: { type: String, default: '' },
    },
    computed: {
        tid() {
            return `hh-pop-${this._uid}`
        },
    },
    methods: {
        fmt(v) {
            const n = Number(v || 0)
            return isFinite(n) ? n.toLocaleString('vi-VN') : '0'
        },
        linkOf(h) {
            return this.$router.resolve(`/supply/supply_handlings/add?mode=show&id=${h.handling_id}`).href
        },
        // "Đổi sang 315-613 (hộp): 20 hộp, thay cho 5 thùng · Xuất kho 20" / "Mua hàng 10"
        lineText(l) {
            const allocs = (l.allocs || []).map((a) => `${a.label} ${this.fmt(a.qty)}`).join(' · ')
            if (!l.swap_product_id) return allocs
            const unitB = l.swap_unit_name || ''
            const swap = `Đổi sang ${l.swap_product_code || ''}${unitB ? ` (${unitB})` : ''}: ${this.fmt(l.dat_don)} ${unitB}, thay cho ${this.fmt(l.swap_origin_quantity)} ${l.unit_name || ''}`
            return allocs ? `${swap} · ${allocs}` : swap
        },
    },
}
</script>

<style lang="scss" scoped>
.hh-note {
    font-size: 11px;
    color: #6b7280;
    white-space: nowrap;
}
.hh-icon {
    cursor: pointer;
    color: #2563eb;
}
</style>

<style lang="scss">
// b-popover render ra body → style không scoped
.hh-popover {
    max-width: 420px;
    font-size: 12px;
    .hh-title {
        font-weight: 600;
        margin-bottom: 4px;
    }
    .hh-item + .hh-item {
        margin-top: 6px;
    }
    .hh-line {
        padding-left: 12px;
        color: #374151;
    }
    .hh-total {
        border-top: 1px solid #e5e7eb;
        margin-top: 6px;
        padding-top: 4px;
        font-weight: 600;
    }
}
</style>
```

- [x] **Step 2: Compile check** — script node trong scratchpad dùng `hrm-thanhan-client/node_modules/vue-template-compiler`:
  `parseComponent` file → `compile(template)` → in `errors` (expected `[]`).

### Task 5: `add.vue` — map field mới + tính lỗi L1/L2 + chặn submit

**Files:**
- Modify: `add.vue` — `mapProposalItem` (~934), `mapHandlingItem` (~979), `mapPoolItem` (~1197), computed validate (~444–510), `submit` (~1327), truyền prop vào `<HandlingGoodsTable>` (~172).

**Interfaces:**
- Consumes: field BE Task 2.
- Produces: computed `rowLimitErrors: { [index]: { proposal?: number /* còn lại */, alloc?: true } }` → prop `limit-errors` của `HandlingGoodsTable` (Task 6). Mỗi dòng có thêm `sl_de_xuat_a: number|null`, `sl_da_xu_ly_a: number`, `lich_su_xu_ly: array`.

- [x] **Step 1: Map field** — thêm vào object trả về của:
  - `mapProposalItem(p)`:
    ```js
                // Mốc "x / y" + popover các PXL khác (BE: sl_de_xuat_a, sl_da_xu_ly_a, lich_su_xu_ly)
                sl_de_xuat_a: p.sl_de_xuat_a == null ? null : Number(p.sl_de_xuat_a),
                sl_da_xu_ly_a: daXlA,
                lich_su_xu_ly: p.lich_su_xu_ly || [],
    ```
  - `mapHandlingItem(p)`:
    ```js
                sl_de_xuat_a: p.sl_de_xuat_a == null ? null : Number(p.sl_de_xuat_a),
                sl_da_xu_ly_a: Number(p.sl_da_xu_ly_a || 0),
                lich_su_xu_ly: p.lich_su_xu_ly || [],
    ```
  - `mapPoolItem(it)`: `sl_de_xuat_a: null, sl_da_xu_ly_a: 0, lich_su_xu_ly: [],`
  (Dòng đổi hàng thêm vào khối / bỏ đổi đều `...cur` nên tự mang theo 3 field — kiểm tra lại `clearSwap` ~1154 có spread `cur`.)

- [x] **Step 2: Thay `overProposalRows` bằng L1 + gom lỗi** — xóa computed `overProposalRows`, thêm:

```js
        // L1 (spec §4): mỗi hàng gốc A thuộc đề xuất — Σ SL quy về A (giữ A: dat_don; đổi: "Thay cho A")
        // của mọi dòng cùng product_id ≤ còn lại = SL đề xuất A − SL các PXL khác đã xử lý.
        // Trả { index dòng cuối của nhóm: SL còn lại } — lỗi hiện ở dòng cuối, không lặp mọi dòng.
        overProposalLimit() {
            const groups = {}
            ;(this.formSubmit.products || []).forEach((p, i) => {
                if (p.sl_de_xuat_a == null) return
                const g = (groups[p.product_id] = groups[p.product_id] || {
                    qty: 0,
                    last: i,
                    remain: Math.max(0, Number(p.sl_de_xuat_a || 0) - Number(p.sl_da_xu_ly_a || 0)),
                })
                g.qty += p.swap_product_id ? Number(p[ORIGIN] || 0) : Number(p.dat_don || 0)
                g.last = i
            })
            const out = {}
            Object.values(groups).forEach((g) => {
                if (g.qty > g.remain + 0.0005) out[g.last] = round3(g.remain)
            })
            return out
        },
        // Gom lỗi chặn theo dòng cho bảng: proposal = còn lại (L1), alloc = phân bổ vượt đặt đơn (L2)
        rowLimitErrors() {
            const out = {}
            Object.keys(this.overProposalLimit).forEach((i) => {
                out[i] = { proposal: this.overProposalLimit[i] }
            })
            ;(this.formSubmit.products || []).forEach((p, i) => {
                if (this.totalAlloc(p) > Number(p.dat_don || 0) + 0.0005) out[i] = { ...(out[i] || {}), alloc: true }
            })
            return out
        },
        // Câu báo lỗi chặn (banner + toast khi bấm lưu); null = không vượt
        limitErrorText() {
            const l2 = this.overOrderRows.length
            const l1 = Object.keys(this.overProposalLimit).length
            if (l1) return `Có ${l1} mặt hàng vượt SL còn lại theo đề xuất.`
            if (l2) return `Có ${l2} mặt hàng phân bổ vượt SL đặt đơn.`
            return null
        },
```
  Sửa `overOrderRows` thêm ε: `return this.totalAlloc(p) > Number(p.dat_don || 0) + 0.0005`.

- [x] **Step 3: `validationBanner`** — thay 2 nhánh `overOrderRows` và `overProposalRows` bằng:

```js
            if (this.limitErrorText) {
                return { variant: 'danger', text: `${this.limitErrorText} Không lưu được phiếu.` }
            }
```
  giữ nhánh `overContractRows` (cảnh báo HĐ) + `hasAnyAlloc`. Sửa comment template "Banner validate (cảnh báo, không chặn lưu)" → "Banner validate — đỏ L1/L2 chặn lưu, vượt HĐ chỉ cảnh báo".

- [x] **Step 4: `submit(isDraft)`** — thay comment "Cảnh báo vượt SL … KHÔNG chặn lưu" bằng:

```js
            // Gửi chính thức: vượt đề xuất / phân bổ vượt đặt đơn → chặn (BE cũng kiểm tra lại). Lưu nháp bỏ qua.
            if (!isDraft && this.limitErrorText) {
                this.$toasted.global.error({ message: this.limitErrorText })
                return
            }
```

- [x] **Step 5: Truyền prop** — `<HandlingGoodsTable ... :limit-errors="isShow ? {} : rowLimitErrors" />`.

- [x] **Step 6: Grep** `overProposalRows` trong `pages/supply` → không còn chỗ dùng. Compile check như Task 4 Step 2.

### Task 6: `HandlingGoodsTable.vue` — `x / y`, popover, ô đỏ

**Files:**
- Modify: `components/HandlingGoodsTable.vue` — ô Đặt đơn (~147–165), ô Thay cho hàng gốc (~171–189), `props` (~465), `components`, methods, style.

**Interfaces:**
- Consumes: prop `limitErrors` (Task 5), component Task 4, field dòng `sl_de_xuat_a`, `sl_da_xu_ly_a`, `lich_su_xu_ly`.

- [x] **Step 1: Prop + component + helpers**

```js
        // Lỗi chặn theo index dòng (add.vue tính): { proposal: SL còn lại theo đề xuất, alloc: true }
        limitErrors: { type: Object, default: () => ({}) },
```
  import `HandledHistoryPopover from './HandledHistoryPopover.vue'` + đăng ký `components`. Methods:

```js
        // Dòng thuộc đề xuất → có mốc "/ SL đề xuất" (hàng chọn thêm: null)
        hasProposalRef(p) {
            return p && p.sl_de_xuat_a != null
        },
        // Còn lại theo đề xuất của hàng gốc A = SL đề xuất − SL các PXL khác đã xử lý (quy về A)
        proposalRemain(p) {
            return Math.max(0, Number(p.sl_de_xuat_a || 0) - Number(p.sl_da_xu_ly_a || 0))
        },
        // Ô hiển thị "x / y": dòng giữ A → ô Đặt đơn; khối đổi hàng → ô "Thay cho A" ở dòng cuối khối
        showRefAtDatDon(p) {
            return this.hasProposalRef(p) && !p.swap_product_id
        },
        showRefAtOrigin(p, i) {
            return this.hasProposalRef(p) && !!p.swap_product_id && this.metas[i] && this.metas[i].last
        },
        rowErr(i) {
            return this.limitErrors[i] || {}
        },
```

- [x] **Step 2: Ô Đặt đơn** — bọc input/span + thêm mốc, note, lỗi:

```html
                            <td class="text-right" :class="{ 'cell-invalid': rowErr(i).alloc || (rowErr(i).proposal != null && !p.swap_product_id) }">
                                <div class="datdon-cell">
                                    <base-input-field v-if="editable" ...giữ nguyên các attr hiện tại... />
                                    <span v-else>{{ fmtNum(p.dat_don) }}</span>
                                    <span v-if="showRefAtDatDon(p)" class="of-proposed">/ {{ fmtNum(p.sl_de_xuat_a) }}</span>
                                </div>
                                <div v-if="showRefAtDatDon(p) && Number(p.sl_da_xu_ly_a) > 0">
                                    <HandledHistoryPopover
                                        :items="p.lich_su_xu_ly || []"
                                        :total="Number(p.sl_da_xu_ly_a || 0)"
                                        :remain="proposalRemain(p)"
                                        :proposed="Number(p.sl_de_xuat_a || 0)"
                                        :unit-name="p.unit_name || ''"
                                    />
                                </div>
                                <div v-if="rowErr(i).proposal != null && !p.swap_product_id" class="qty-error">
                                    Vượt SL còn lại theo đề xuất (còn {{ fmtNum(rowErr(i).proposal) }})
                                </div>
                                <div v-if="rowErr(i).alloc" class="qty-error">
                                    Phân bổ vượt SL đặt đơn ({{ fmtNum(p.dat_don) }})
                                </div>
                                <div v-if="isOverContract(p)" class="qty-error">...giữ nguyên...</div>
                            </td>
```

- [x] **Step 3: Ô Thay cho hàng gốc** — trong `<template v-if="p.swap_product_id">`, sau `.origin-cell` và lỗi "Nhập SL hàng gốc tương ứng", thêm:

```html
                                    <div v-if="showRefAtOrigin(p, i)" class="origin-ref">
                                        Khối / {{ fmtNum(p.sl_de_xuat_a) }} {{ p.unit_name }}
                                    </div>
                                    <div v-if="showRefAtOrigin(p, i) && Number(p.sl_da_xu_ly_a) > 0">
                                        <HandledHistoryPopover
                                            :items="p.lich_su_xu_ly || []"
                                            :total="Number(p.sl_da_xu_ly_a || 0)"
                                            :remain="proposalRemain(p)"
                                            :proposed="Number(p.sl_de_xuat_a || 0)"
                                            :unit-name="p.unit_name || ''"
                                        />
                                    </div>
                                    <div v-if="rowErr(i).proposal != null" class="qty-error">
                                        Vượt SL còn lại theo đề xuất (còn {{ fmtNum(rowErr(i).proposal) }})
                                    </div>
```
  và thêm `:class="{ 'cell-invalid': rowErr(i).proposal != null && p.swap_product_id }"` cho `<td v-if="hasSwap">`.

- [x] **Step 4: Style** (scoped):

```scss
.datdon-cell {
    display: flex;
    align-items: center;
    justify-content: flex-end;
    gap: 4px;
}
.of-proposed,
.origin-ref {
    font-size: 11px;
    color: #6b7280;
    white-space: nowrap;
}
.cell-invalid ::v-deep input {
    border-color: #dc3545 !important;
}
```

- [x] **Step 5: Compile check** như Task 4 Step 2. Bề rộng cột Đặt đơn: nếu `/ 1.000` làm vỡ cột sticky → tăng `min-width` cột Đặt đơn trong style hiện có (giữ `syncStickyCols`).

## Phase 3 — Kiểm tra UI (spec §9)

- [ ] Build / chạy client (user tự build nếu cần) — mở `/supply/supply_handlings`.
- [ ] 1. Đề xuất A 20 / B 30 → PXL1 Mua A 10, Mua B 10 → gửi.
- [ ] 2. Tạo PXL2: A `[10] / 20`, "Đã xử lý 10 ⓘ · Còn 10"; B `[20] / 30`; hover ⓘ → PXL1 · người lập · ngày · Đã duyệt · Mua hàng 10; link mở tab mới đúng phiếu.
- [ ] 3. PXL2 A = 15 → ô đỏ "Vượt SL còn lại theo đề xuất (còn 10)", banner đỏ, bấm Lưu → toast, không gọi API. Lưu nháp → lưu được.
- [ ] 4. A = 10, Mua 12 → "Phân bổ vượt SL đặt đơn (10)", chặn.
- [ ] 5. Đổi A → B (ĐVT khác), "Thay cho A" 12 > còn 10 → lỗi ở dòng cuối khối, chặn.
- [ ] 6. 2 tab cùng tạo PXL từ 1 đề xuất: tab 1 gửi A 10 → tab 2 gửi A 10 → toast BE "còn 0, nhập 10 … tải lại trang".
- [ ] 7. Sửa PXL1: popover không có PXL1; `/ 20`, "Đã xử lý" = phần của PXL2; lưu lại không đổi số → OK.
- [ ] 8. Hàng chọn thêm từ popup: không `/ y`, không popover, chỉ L2.
- [ ] 9. PXL nội bộ Chờ duyệt → Duyệt: không bị chặn.
- [ ] 10. Màn xem (mode=show): hiện `10 / 20` text + popover, không có ô đỏ.

### Checkpoint — 01/10/2026 (2)
Vừa hoàn thành: Task 1–6 (BE + FE) — php -l, tinker 8 case guard (rollback), compile vue 3 file đều OK.
Đang làm dở: Final review toàn bộ (reviewer độc lập).
Bước tiếp theo: Xử lý finding Critical/Important (nếu có) → user test UI Phase 3.
Blocked:

Rulings khi thực thi:
- `update()`: guard đặt ngay trước `$model->update` (sau khối kiểm tra đề xuất còn chờ xử lý) — message "đề xuất không còn chờ xử lý" ưu tiên.
- `mapProposalItems`: dòng đổi điền sẵn gán thêm `swap_quantity = remainB` cho khớp `dat_don` (BE ép dat_don = swap_quantity; trước đây PXL thứ 2 lưu dat_don = SL B đầy đủ của đề xuất).
- Viền đỏ ô lỗi đè lên `div[style]` của base-input-field (viền nằm ở div bọc, không ở input).

### Checkpoint — 01/10/2026
Vừa hoàn thành: Brainstorming xong, spec + design + plan đã viết, user duyệt spec.
Đang làm dở: —
Bước tiếp theo: Task 1 — `SupplyProposalService::handledHistoryByProduct()`.
Blocked:

---

## Sửa đổi 1 — 02/10/2026: L1 + mốc "x / y" tính theo PHÂN BỔ (không theo Đặt đơn)

**Bug user báo:** mở PXL-2026-0020 (phiếu đầu của DXCU-2026-0039) thấy Đặt đơn `15 / 15`, trong khi phiếu chỉ phân bổ Mua 7.
**Nguyên nhân:** "đã xử lý" của các PXL khác (`handledDetailByProduct`) = Σ phân bổ, còn L1 + mốc hiển thị lại dùng **Đặt đơn**
→ lệch thước đo. Hệ quả thật: PXL2 phân bổ 8 xong, sửa PXL1 (Đặt đơn 15 > còn 7) bị chặn dù không đổi số.
**User chốt (02/10/2026):** đã xử lý = **Σ phân bổ** (quy về A). Đặt đơn chỉ là SL phiếu nhận, phần chưa phân bổ để phiếu sau.

- [x] BE `SupplyHandlingService::guardProposalLimit()` L1: cộng Σ phân bổ quy về A (dòng đổi: `swap_origin_quantity × Σ phân bổ / swap_quantity`, cùng công thức `handledDetailByProduct`) thay cho Đặt đơn / Thay cho A
- [x] FE `add.vue` `overProposalLimit`: cùng công thức (helper `allocQtyA`)
- [x] FE `HandlingGoodsTable.vue`: ô Đặt đơn bỏ `/ y` cạnh ô nhập → dòng phụ `Phân bổ x / y` (x = Σ phân bổ quy A của cả nhóm hàng gốc); ô "Thay cho hàng gốc" dòng cuối khối tương tự; câu lỗi L1 "Phân bổ vượt SL còn lại theo đề xuất"
- [x] php -l + compile FE
- [ ] User test: mở PXL-2026-0020 → `Phân bổ 7 / 15`; lập PXL2 → còn 8, phân bổ 9 bị chặn; sửa PXL1 sau khi PXL2 phân bổ 8 → lưu được

### Checkpoint — 02/10/2026
Vừa hoàn thành: Sửa đổi 1 — L1 + mốc hiển thị theo Σ phân bổ (BE guardProposalLimit, FE constants.allocQtyA + add.vue overProposalLimit + HandlingGoodsTable "Phân bổ x / y"). php -l OK, compile vue OK; script guard trên DXCU-2026-0039 (rollback): sửa PXL1 không đổi số → OK; PXL2 mua 8 (còn 8) → OK; mua 9 → chặn; đặt 15 mua 5 → OK.
Đang làm dở: —
Bước tiếp theo: user build client + hard refresh, test UI 10 kịch bản Phase 3 + kịch bản Sửa đổi 1 (lưu ý kịch bản 3 nay là "phân bổ vượt còn lại", không phải đặt đơn vượt)
Blocked:

---

## Sửa đổi 2 — 02/10/2026: khóa Đặt đơn dòng thuộc đề xuất + gọn hiển thị (user chốt)

**User báo:** PXL thứ 2 ô Đặt đơn 3 tầng chiếm diện tích; ô Đặt đơn sao lại sửa được.
**Chốt:** (1) dòng giữ hàng gốc A thuộc đề xuất → Đặt đơn KHÓA (chỉ hiển thị), tự điền = còn lại theo đề xuất lúc lập, phiếu cũ giữ số đã lưu; dòng đổi B + hàng chọn thêm ngoài đề xuất vẫn nhập. BE không đổi. (2) bỏ dòng "Phân bổ x / y" (trùng cột Kết quả) + bỏ dòng "Đã xử lý · Còn"; chỉ hiện icon ⓘ cạnh số Đặt đơn khi có PXL khác, popover đầu có "Đề xuất y · Đã xử lý x · Còn z".

- [x] FE `HandlingGoodsTable.vue`: ô Đặt đơn dòng giữ A thuộc đề xuất → text (không input), kiểm tra điều hướng bàn phím không gãy
- [x] FE `HandledHistoryPopover.vue`: chế độ chỉ icon (trigger ⓘ), dòng tóm tắt "Đề xuất · Đã xử lý · Còn" ở đầu popover
- [x] FE ô "Thay cho hàng gốc" dòng cuối khối: bỏ "Phân bổ x / y", chỉ icon ⓘ
- [x] Kiểm tra prefill dat_don khi lập PXL mới = còn lại theo đề xuất
- [x] Compile check
- [ ] User test: PXL2 của DXCU-2026-0039 → ô Đặt đơn hàng HC-ĐG-138 hiện `8 ⓘ` (không nhập được), rê ⓘ → "Đề xuất 15 · Đã xử lý 7 · Còn 8" + PXL-2026-0020; hàng chọn thêm / dòng đổi B vẫn nhập được; mở PXL-2026-0020 → `15`, chưa có PXL khác thì không có ⓘ

### Checkpoint — 02/10/2026 (Sửa đổi 2)
Vừa hoàn thành: khóa Đặt đơn dòng giữ A thuộc đề xuất (`datDonLocked`), bỏ dòng "Phân bổ x / y" + "Đã xử lý · Còn", popover chỉ còn icon ⓘ (tóm tắt Đề xuất · Đã xử lý · Còn ở đầu popover); bỏ CSS `.of-proposed/.origin-ref`, bỏ import `allocQtyA` khỏi bảng (add.vue vẫn dùng). Compile 3 file Vue + constants.js OK. BE không đổi.
Đang làm dở: —
Bước tiếp theo: user build client + hard refresh, test UI (Sửa đổi 1 + 2 + 10 kịch bản Phase 3 — kịch bản 2 nay là `8 ⓘ`, không còn "[10] / 20")
Blocked:

## Sửa đổi 3 — 02/10/2026: popover bỏ trạng thái phiếu
- [x] FE `HandledHistoryPopover.vue`: dòng đầu mỗi phiếu chỉ còn `mã · người lập · ngày` (bỏ `status_name` theo yêu cầu user; BE vẫn trả, không đổi)

## Sửa đổi 4 — 02/10/2026: popover tách "Phiếu này" / "Phiếu khác"
**User báo:** mở PXL-2026-0020 (phiếu 1) thấy "Đề xuất 15 · Đã xử lý 2 · Còn 13" — 2 là của PXL-0021, loại chính phiếu đang xem nên "Còn 13" ≠ còn thật (15 − 7 − 2 = 6).
- [x] FE popover: tóm tắt `Đề xuất y · Phiếu này a · Phiếu khác b · Còn y − a − b` (a = Σ phân bổ quy A của hàng gốc trên form, realtime); bỏ prop `remain`
- [x] FE bảng: truyền `:current` (Σ `allocQtyA` cùng product_id), bỏ `:remain`
- [x] Compile check
- [ ] User test: mở PXL-2026-0020 → ⓘ: "Đề xuất 15 · Phiếu này 7 · Phiếu khác 2 · Còn 6 Hộp"; sửa phân bổ trên form → "Phiếu này"/"Còn" đổi theo

## Fix 5 — 02/10/2026: header cột cố định bị lộ viền / chữ khi cuộn ngang
**User báo:** cuộn ngang bảng hàng PXL → vùng header STT + Định danh lộ vạch cam/xám và chữ "Hàng hóa" của cột trượt qua.
**Nguyên nhân:** `.table-bordered` dùng `border-collapse: collapse` → viền thuộc về bảng chứ không thuộc ô sticky, nên viền (gạch chân nhóm cột) + chữ ô `rowspan` nằm đúng vạch giữa 2 hàng header lộ ra trên khối cố định.
- [x] FE `HandlingGoodsTable.vue`: chuyển bảng sang `border-collapse: separate; border-spacing: 0`, mỗi ô chỉ vẽ viền phải + dưới (viền trái ở `stk-0` / dòng breakdown, viền trên ở hàng nhóm cột) → nền ô sticky phủ luôn viền của nó
- [x] Bỏ bóng đổ + vạch xám ở mép phải khối cố định (`.stk-last` box-shadow) theo yêu cầu user — ranh giới chỉ còn viền phải 1px của ô
- [ ] User build client + hard refresh, cuộn ngang kiểm tra header + dòng đổi hàng + dòng tổng
