# Gộp loại đề xuất cung ứng còn 2 loại — Kế hoạch triển khai

> Phụ trách: @khoipv · Ngày lập: 25/09/2026
> **Spec:** [docs/superpowers/specs/2026-09-25-de-xuat-cung-ung-gop-2-loai-design.md](../../docs/superpowers/specs/2026-09-25-de-xuat-cung-ung-gop-2-loai-design.md)
> **Tóm tắt:** [design.md](design.md)

**Mục tiêu:** Ô "Loại đề xuất" ở màn lập phiếu đề xuất cung ứng rút từ 6 xuống 2 lựa chọn
(*Cung ứng nội bộ* / *Cung ứng khách hàng*); mã `type` thật (6 loại) do BE tự suy khi lưu, dựa
vào loại hợp đồng của dòng hàng đã chọn.

**Kiến trúc:** Thêm khái niệm **nhóm** (`group`) ở tầng giao diện + tham số API, giữ nguyên cột
`supply_proposals.type` 6 mã ở DB. FE có 1 computed `effectiveType` làm nguồn sự thật duy nhất cho
mọi chỗ trước đây đọc `formSubmit.type`. BE thêm `resolveType()` suy `type` từ `group` + dòng hàng,
và **không tin** `type` FE gửi lên.

**Tech stack:** PHP 7.4 / Laravel 8 (`Modules/Supply`) · Nuxt 2.14 / Vue 2 / Bootstrap-Vue
(`pages/supply/supply_proposals`)

## Ràng buộc chung (áp cho MỌI task)

- **Không migration, không đổi schema.** `supply_proposals.type` giữ nguyên 6 mã 1..6.
- **Không commit / không push git** — người dùng tự commit.
- `GET /supply-proposals/customers` và `/goods-pool` **dùng chung** với màn *Phiếu xử lý*
  (`supply_handlings/add.vue:839`) và màn *Hợp đồng đã kết xuất* (`contract_render/index.vue:321`).
  2 hàm service nhận **thêm** tham số `group` (optional); **không có `group` thì chạy y nguyên nhánh
  `type` cũ**. Cấm đổi chữ ký kiểu thay thế.
- `supply_proposals.contract_id` là **HĐ NGUỒN** (phiếu lập từ màn Kết xuất HĐ). **KHÔNG** suy ngược
  từ dòng hàng — suy vào sẽ bật nhầm `isFromContract` bên FE và khóa oan ô Loại / Khách hàng.
- FE: dropdown dùng `base-select2`, input dùng `b-form-input` — không dùng thẻ native.
- Mọi hằng số FE phải khớp hằng số BE; file `constants.js` đã có comment quy ước này, giữ nguyên nếp.
- Dự án **không có test tự động** cho module này → mỗi task kết thúc bằng bước **kiểm tra thủ công**
  cụ thể thay cho bước chạy test.

## Điểm dễ vỡ cần soi kỹ khi review

1. **Phiếu cũ (đã lưu) mở lại** — `d.type` là 1 trong 6 mã, FE phải suy ngược ra `group` đúng và
   `effectiveType` phải bằng đúng `d.type` khi dòng hàng chưa trả `contract_type` (Task 9, Task 3).
2. **Phiếu lập từ màn Kết xuất HĐ** — `isFromContract` khóa ô Loại; `group` phải được set từ
   `prefillType`, và `contract_id` (HĐ nguồn) không được mất khi lưu (Task 4, Task 9).
3. **Màn Phiếu xử lý + màn Hợp đồng đã kết xuất** — 2 màn này gọi `customers` / `goods-pool` bằng
   `type` cũ, phải trả **y hệt dữ liệu như trước** (Task 2, kiểm tra ở luồng 11/12).
4. **Chỉ chọn hàng ngoài HĐ** → `type = 3` (khách lẻ), `contract_id = null`, gửi đi phải vào
   *Chờ BGĐ duyệt* chứ không vào thẳng inbox (Task 4).
5. **Bộ lọc "Loại" ở 2 màn danh sách** — đổi từ `type` (6 mã) sang `type_group` (2 nhóm); param cũ
   `type` vẫn phải chạy được vì filter đã lưu trong localStorage của user (Task 7, Task 11).

---

## Phase 0 — Khảo sát & thiết kế

- [x] Khảo sát hiện trạng BE `Modules/Supply` + FE `pages/supply/supply_proposals`
- [x] Chốt 4 quyết định lớn với user
- [x] Viết spec đầy đủ tại `docs/superpowers/specs/2026-09-25-...-design.md`
- [x] Viết `.plans/de-xuat-cung-ung-gop-2-loai/design.md` (tóm tắt)
- [x] User duyệt plan này

---

## Phase 1 — Backend (`hrm-thanhan-api/Modules/Supply`)

### Task 1: Hằng số & helper nhóm trong entity

**File:**
- Sửa: `Modules/Supply/Entities/SupplyProposal.php`

**Cung cấp cho task sau:** `SupplyProposal::GROUP_KHACH`, `GROUP_NOI_BO`, `GROUPS`,
`groupOf($type): int`, `groupTypes($group): array`, `groupName($group): string`,
`typeFromSelection($contractType): int`, `allContractTypes(): array`

- [x] **Bước 1.1: Thêm 2 hằng nhóm + mảng `GROUPS`**

Chèn ngay sau `const TYPE_HD_NGUYEN_TAC = 6;` (dòng 32):

```php
    // 25/09/2026 — Ô "Loại đề xuất" ngoài màn lập phiếu gộp còn 2 NHÓM. Cột supply_proposals.type
    // VẪN giữ 6 mã ở trên (BE tự suy lúc lưu theo loại HĐ của dòng hàng đã chọn) nên toàn bộ chỗ
    // hạ nguồn — phiếu xử lý, báo cáo nhu cầu mua, đơn mua, export — không phải đổi gì.
    const GROUP_KHACH  = 1;   // gồm type 1, 3, 4, 5, 6
    const GROUP_NOI_BO = 2;   // chỉ type 2
```

Chèn ngay sau mảng `public const TYPES = [...]` (kết thúc dòng 61):

```php
    public const GROUPS = [
        ['id' => self::GROUP_KHACH,  'name' => 'Cung ứng khách hàng'],
        ['id' => self::GROUP_NOI_BO, 'name' => 'Cung ứng nội bộ'],
    ];
```

- [x] **Bước 1.2: Thêm 4 hàm static**

Chèn ngay sau `typeShowsDealerPrice()` (kết thúc dòng 146), trước `public function products()`:

```php
    /**
     * Nhóm hiển thị của 1 loại đề xuất — dùng cho cột "Loại" và bộ lọc ở 2 màn danh sách.
     */
    public static function groupOf($type): int
    {
        return (int) $type === self::TYPE_NOI_BO ? self::GROUP_NOI_BO : self::GROUP_KHACH;
    }

    /**
     * Các mã type thuộc 1 nhóm — dùng cho whereIn khi lọc danh sách theo nhóm.
     */
    public static function groupTypes($group): array
    {
        return (int) $group === self::GROUP_NOI_BO
            ? [self::TYPE_NOI_BO]
            : [
                self::TYPE_KHACH,
                self::TYPE_KHACH_LE,
                self::TYPE_HD_DAT_MUON,
                self::TYPE_HD_TRAO_TANG,
                self::TYPE_HD_NGUYEN_TAC,
            ];
    }

    public static function groupName($group): string
    {
        $found = collect(self::GROUPS)->firstWhere('id', (int) $group);

        return $found['name'] ?? '';
    }

    /**
     * Suy loại đề xuất từ loại HĐ của dòng hàng đã chọn (nhóm "Cung ứng khách hàng").
     * Không có dòng hàng nào trong HĐ -> khách lẻ (khách chưa có HĐ nào).
     */
    public static function typeFromSelection($contractType): int
    {
        return is_null($contractType) ? self::TYPE_KHACH_LE : self::typeFromContractType($contractType);
    }

    /**
     * Toàn bộ loại hợp đồng bán — pool hàng của nhóm "Cung ứng khách hàng" lấy hết 5 loại,
     * người lập không còn phải tự biết hàng nằm trong HĐ loại nào trước khi chọn loại phiếu.
     */
    public static function allContractTypes(): array
    {
        return [
            Contract::TRONG_THAU,
            Contract::NGOAI_THAU,
            Contract::CHO_TANG,
            Contract::DAT_MUON,
            Contract::NGUYEN_TAC,
        ];
    }
```

- [x] **Bước 1.3: Kiểm tra `Contract` đã được `use`**

`Entities/SupplyProposal.php` đã dùng `Contract::TRONG_THAU` trong `contractTypes()` nên import đã có.
Chạy để chắc chắn file không lỗi cú pháp:

```bash
cd hrm-thanhan-api && php -l Modules/Supply/Entities/SupplyProposal.php
```

Kỳ vọng: `No syntax errors detected`

---

### Task 2: Service — `customers()` và `goodsPool()` nhận thêm `group`

**File:**
- Sửa: `Modules/Supply/Services/SupplyProposalService.php` (`customers()` dòng 57, `goodsPool()` dòng 122)

**Dùng từ task trước:** `SupplyProposal::GROUP_NOI_BO`, `allContractTypes()`
**Cung cấp cho task sau:** `customers($type = null, $group = null)`,
`goodsPool($type, $customerId = null, $group = null)`, `contractGoodsPool(array $contractTypes, $customerId): array`

> ⚠️ **2 hàm này dùng chung với màn Phiếu xử lý và màn Hợp đồng đã kết xuất.** Tham số `group` là
> **thêm vào**, đặt cuối. Không có `group` → rơi xuống đúng code cũ, không đổi 1 dòng hành vi nào.

- [x] **Bước 2.1: `customers()` — thêm nhánh `group` ở đầu hàm**

Đổi chữ ký dòng 57 và chèn nhánh mới ngay dưới:

```php
    public function customers($type = null, $group = null)
    {
        // 25/09/2026 — màn LẬP PHIẾU gửi `group` (2 nhóm mới). Màn "Hợp đồng đã kết xuất" và màn
        // "Phiếu xử lý" vẫn gửi `type` (6 mã cũ) hoặc không gửi gì → rơi xuống nguyên code cũ.
        // Nhóm khách hàng: pool hàng lấy hết 5 loại HĐ + hàng ngoài HĐ nên danh sách khách phải là
        // TOÀN BỘ danh mục (giống loại khách lẻ cũ), không lọc theo HĐ nữa.
        if ($group !== null && $group !== '') {
            return (int) $group === SupplyProposal::GROUP_NOI_BO
                ? $this->customers(SupplyProposal::TYPE_NOI_BO)
                : $this->customers(SupplyProposal::TYPE_KHACH_LE);
        }

        $catalogTypes = [
```

Phần còn lại của hàm (từ `$catalogTypes = [` trở xuống) **giữ nguyên 100%**.

> Nhóm nội bộ vẫn gọi lại nhánh cũ với `TYPE_NOI_BO` vì danh sách này dùng cho ô **"KH sử dụng"**
> của phiếu nội bộ — hành vi hiện tại là "khách có HĐ đã duyệt", giữ nguyên để không đổi ngầm.

- [x] **Bước 2.2: Tách nhánh HĐ của `goodsPool()` thành `contractGoodsPool()`**

Thay toàn bộ thân `goodsPool()` (dòng 122 → hết, kết thúc ở `return array_merge($items, $this->catalogItems());`) bằng:

```php
    public function goodsPool($type, $customerId = null, $group = null)
    {
        // 25/09/2026 — màn LẬP PHIẾU gửi `group`; màn Phiếu xử lý vẫn gửi `type` (6 mã) → nhánh cũ.
        if ($group !== null && $group !== '') {
            // Nội bộ: không bám HĐ → chỉ danh mục.
            if ((int) $group === SupplyProposal::GROUP_NOI_BO) {
                return $this->catalogItems();
            }
            if (empty($customerId)) {
                return [];
            }

            // Nhóm khách hàng: hàng của MỌI loại HĐ còn hiệu lực của khách đó + toàn bộ danh mục.
            // Việc chỉ được bám 1 HĐ do popup khóa (activeContractId), không lọc ở đây.
            return $this->contractGoodsPool(SupplyProposal::allContractTypes(), $customerId);
        }

        $type = (int) $type;

        // Nội bộ / khách lẻ: không bám HĐ → chỉ toàn bộ danh mục hàng hóa.
        if (!SupplyProposal::isContractBased($type)) {
            return $this->catalogItems();
        }

        // Các loại bám HĐ: cần customer_id mới biết lấy HĐ của ai.
        if (empty($customerId)) {
            return [];
        }

        return $this->contractGoodsPool(SupplyProposal::contractTypes($type), $customerId);
    }

    /**
     * Hàng của các HĐ đã duyệt (3) / đã kết xuất (9) và CÒN HIỆU LỰC của 1 khách hàng, giới hạn theo
     * các loại HĐ truyền vào, + toàn bộ danh mục hàng hóa (để FE phân biệt Trong/Ngoài HĐ).
     *
     * Còn hiệu lực = chưa quá contract_end_time — cột này đã bao gồm gia hạn từ phụ lục đã duyệt.
     * HĐ để trống ngày kết thúc: không kết luận được là hết hạn nên vẫn cho hiện.
     */
    private function contractGoodsPool(array $contractTypes, $customerId): array
    {
        $items = [];

        $contracts = Contract::query()
            ->whereIn('status', Contract::approvedStatuses())
            ->where('record_type', Contract::HOP_DONG)
            ->whereIn('type', $contractTypes)
            ->where('customer_id', $customerId)
            ->where(function ($q) {
                $q->whereNull('contract_end_time')
                    ->orWhereDate('contract_end_time', '>=', now()->toDateString());
            })
            ->with(['products' => function ($q) {
                $q->with('unit');
            }, 'main_company'])
            ->get();

        $importTypeByProductId = $this->importTypeFallbackMap($contracts);
        $allProductIds = collect($contracts)->flatMap(fn($c) => collect($c->products)->pluck('product_id'));
        $unitMap = $this->unitConversionMap($allProductIds);
        // Nạp mã hiện hành cho toàn bộ hàng của mọi HĐ trong 1 query (thay vì mỗi HĐ 1 query).
        $this->warmLiveCodes($allProductIds);

        foreach ($contracts as $contract) {
            // Popup chọn hàng: KHÔNG gộp — hiện từng dòng HĐ để người dùng thấy tên riêng của mỗi dòng
            // (VD HD-101/2026 có 3 dòng cùng mã HC-HH-084: mức thấp / trung bình / cao).
            $items = array_merge($items, $this->contractProductRows($contract, $importTypeByProductId, $unitMap, false));
        }

        return array_merge($items, $this->catalogItems());
    }
```

- [x] **Bước 2.3: Kiểm tra cú pháp**

```bash
cd hrm-thanhan-api && php -l Modules/Supply/Services/SupplyProposalService.php
```

Kỳ vọng: `No syntax errors detected`

---

### Task 3: Dòng hàng trả thêm `contract_type` / `contract_type_name`

**File:**
- Sửa: `Modules/Supply/Services/SupplyProposalService.php` (`contractRow()` dòng 784, `contractRefMap()` dòng 854)
- Sửa: `Modules/Supply/Transformers/SupplyProposal/DetailSupplyProposalResource.php` (dòng ~71)

**Cung cấp cho task sau:** mỗi dòng hàng (pool & phiếu đã lưu) có `contract_type` (int|null) và
`contract_type_name` (string) → FE dùng để suy `effectiveType` và hiện nhãn loại HĐ trong popup.

- [x] **Bước 3.1: `contractRow()` — thêm 2 key**

Trong mảng `return [...]` của `contractRow()`, ngay sau dòng `'contract_code' => $contract->code ?? '',`:

```php
            // 25/09/2026 — pool nay trộn hàng của cả 5 loại HĐ nên dòng hàng phải tự khai loại HĐ:
            // FE suy loại đề xuất (bảng hàng hóa + duyệt BGĐ) từ đây.
            'contract_type'      => $contract->type !== null ? (int) $contract->type : null,
            'contract_type_name' => Contract::TYPE_NAME[(int) $contract->type] ?? '',
```

- [x] **Bước 3.2: `contractRefMap()` — thêm 2 key vào `$meta`**

Trong `foreach ($contracts as $c)`, mảng `$meta`, ngay sau `'contract_code' => $c->code ?? '',`:

```php
                'contract_type'      => $c->type !== null ? (int) $c->type : null,
                'contract_type_name' => Contract::TYPE_NAME[(int) $c->type] ?? '',
```

- [x] **Bước 3.3: `DetailSupplyProposalResource` — trả `contract_type` ra FE**

Trong khối `'products' => (function () {...})`, ngay sau dòng
`'contract_code' => $ref['contract_code'] ?? '',`:

```php
                        // Loại HĐ của dòng hàng — FE suy effectiveType khi mở lại phiếu đã lưu.
                        'contract_type'      => $ref['contract_type'] ?? null,
                        'contract_type_name' => $ref['contract_type_name'] ?? '',
```

- [x] **Bước 3.4: Kiểm tra thủ công**

Mở 1 phiếu đề xuất cũ có hàng trong HĐ (màn Chi tiết), mở DevTools → tab Network → response
`GET supply/supply-proposals/{id}`. Kỳ vọng: mỗi dòng `products` có `in_contract: true` đều có
`contract_type` là số 1..5 và `contract_type_name` là tên tiếng Việt tương ứng.

---

### Task 4: Suy `type` khi lưu (`resolveType`) + áp vào `store()` / `update()`

**File:**
- Sửa: `Modules/Supply/Services/SupplyProposalService.php` (`store()` dòng 1355, `update()` dòng 1406)

**Dùng từ task trước:** `SupplyProposal::GROUP_NOI_BO`, `typeFromSelection()`

- [x] **Bước 4.1: Thêm `resolveType()`**

Chèn ngay trước `public function store($request)` (dòng 1355):

```php
    /**
     * Suy mã loại đề xuất (supply_proposals.type, 6 mã) từ NHÓM người dùng chọn + dòng hàng đã tick.
     *
     * 25/09/2026 — màn lập phiếu chỉ còn 2 nhóm. KHÔNG tin `type` / `contract_type` FE gửi lên:
     * đọc lại contracts.type từ DB theo contract_id của dòng hàng trong HĐ ĐẦU TIÊN (1 phiếu chỉ
     * bám 1 HĐ — assertSingleContract() đã chặn ở trên). Chỉ có hàng ngoài HĐ -> khách lẻ (3).
     */
    private function resolveType($group, $products): int
    {
        if ((int) $group === SupplyProposal::GROUP_NOI_BO) {
            return SupplyProposal::TYPE_NOI_BO;
        }

        $contractId = null;
        foreach (is_array($products) ? $products : [] as $p) {
            if (!empty($p['in_contract']) && !empty($p['contract_id'])) {
                $contractId = (int) $p['contract_id'];
                break;
            }
        }

        $contractType = $contractId ? Contract::where('id', $contractId)->value('type') : null;

        return SupplyProposal::typeFromSelection($contractType);
    }
```

- [x] **Bước 4.2: `store()` — lấy `$type` từ `group`**

Thay dòng `$type = (int) $request->input('type');` (trong `store()`) bằng:

```php
        // 25/09/2026 — FE mới gửi `group` (2 nhóm), BE tự suy `type`. API cũ / client cũ không gửi
        // group thì vẫn dùng `type` gửi lên để không vỡ tích hợp sẵn có.
        $group = $request->input('group');
        $type  = ($group !== null && $group !== '')
            ? $this->resolveType($group, $request->input('products', []))
            : (int) $request->input('type');
```

Trong mảng `SupplyProposal::create([...])`, đổi `'type' => $request->input('type'),` thành:

```php
            'type'          => $type,
```

- [x] **Bước 4.3: `update()` — y hệt**

Thay dòng `$type = (int) $request->input('type');` (trong `update()`) bằng khối `$group` / `$type`
giống hệt Bước 4.2, và trong `$model->update([...])` đổi `'type' => $request->input('type'),` thành
`'type' => $type,`.

> `$isInternal`, `$needApprove`, `$contractId` bên dưới đã tính theo biến `$type` → tự động đúng,
> không đụng vào. `contract_id` vẫn chỉ lưu khi `isContractBased($type)` và vẫn lấy từ
> `$request->input('contract_id')` (HĐ NGUỒN), **không** suy từ dòng hàng.

- [x] **Bước 4.4: Kiểm tra cú pháp**

```bash
cd hrm-thanhan-api && php -l Modules/Supply/Services/SupplyProposalService.php
```

---

### Task 5: Validation — chấp nhận `group`

**File:**
- Sửa: `Modules/Supply/Http/Requests/SupplyProposal/StoreSupplyProposalRequest.php` (dòng 15, 18, 43-45)

- [x] **Bước 5.1: Nới rule `type`, thêm rule `group`**

Đổi dòng 15:

```php
            // 25/09/2026 — FE mới gửi `group` và BE tự suy `type`; client cũ vẫn gửi `type`.
            'type'                  => ['required_without:group', 'nullable', 'integer', 'in:' . implode(',', array_column(SupplyProposal::TYPES, 'id'))],
            'group'                 => ['nullable', 'integer', 'in:' . implode(',', array_column(SupplyProposal::GROUPS, 'id'))],
```

- [x] **Bước 5.2: `customer_id` bắt buộc theo `group` khi có `group`**

Đổi rule `customer_id` (dòng 18) thành:

```php
            'customer_id'           => $this->requiresCustomer()
                ? ['required', 'integer']
                : ['nullable', 'integer'],
```

Thêm helper vào cuối class (trước dấu `}` đóng class):

```php
    /**
     * Phiếu có ô Khách hàng không — chỉ nhóm/loại nội bộ là không.
     * Ưu tiên `group` (FE mới), thiếu thì rơi về `type` (client cũ).
     */
    private function requiresCustomer(): bool
    {
        $group = request()->input('group');

        if ($group !== null && $group !== '') {
            return (int) $group !== SupplyProposal::GROUP_NOI_BO;
        }

        return (int) request()->input('type') !== SupplyProposal::TYPE_NOI_BO;
    }
```

- [x] **Bước 5.3: Thêm message cho `group`**

Trong mảng `messages()`, sau `'type.in' => 'Loại phiếu không hợp lệ.',`:

```php
            'group.in'                       => 'Nhóm đề xuất không hợp lệ.',
            'type.required_without'          => 'Vui lòng chọn loại phiếu.',
```

- [x] **Bước 5.4: Kiểm tra cú pháp**

```bash
cd hrm-thanhan-api && php -l Modules/Supply/Http/Requests/SupplyProposal/StoreSupplyProposalRequest.php
```

---

### Task 6: Controller — chuyển `group` xuống service

**File:**
- Sửa: `Modules/Supply/Http/Controllers/Api/V1/SupplyProposalController.php` (dòng 72, 115)

- [x] **Bước 6.1: `customers()`**

Đổi dòng 72:

```php
            return $this->responseJson('success', Response::HTTP_OK, $this->service->customers($request->input('type'), $request->input('group')));
```

- [x] **Bước 6.2: `goodsPool()`**

Đổi dòng 115:

```php
            return $this->responseJson('success', Response::HTTP_OK, $this->service->goodsPool($request->type, $request->customer_id, $request->group));
```

- [x] **Bước 6.3: `productInfo()` — KHÔNG đổi**

`typeShowsDealerPrice($request->input('type'))` giữ nguyên: FE sẽ gửi `effectiveType` (1 trong 6 mã)
vào đúng key `type` này, nên logic 2 cột giá dealer tự khớp. Ghi chú lại để khỏi sửa nhầm:

```php
            // 25/09/2026 — FE gửi `type` ở đây là effectiveType (đã suy từ loại HĐ của hàng đã
            // chọn), vẫn là 1 trong 6 mã cũ → giữ nguyên nhánh này.
```

- [x] **Bước 6.4: Kiểm tra cú pháp**

```bash
cd hrm-thanhan-api && php -l Modules/Supply/Http/Controllers/Api/V1/SupplyProposalController.php
```

---

### Task 7: Danh sách — lọc theo nhóm + trả tên nhóm

**File:**
- Sửa: `Modules/Supply/Services/SupplyProposalService.php` (`index()` dòng 1189, `inbox()` dòng ~1240)
- Sửa: `Modules/Supply/Transformers/SupplyProposal/SupplyProposalResource.php` (dòng 20-21)
- Sửa: `Modules/Supply/Transformers/SupplyProposal/DetailSupplyProposalResource.php` (dòng 15)

- [x] **Bước 7.1: `index()` — thêm bộ lọc `type_group`**

Ngay sau dòng `->when($request->type, fn($q) => $q->where('type', $request->type))` trong `index()`:

```php
            // 25/09/2026 — bộ lọc "Loại" ở màn danh sách gộp còn 2 nhóm. Giữ luôn nhánh `type` ở
            // trên vì filter cũ đang nằm trong localStorage của user.
            ->when($request->type_group, fn($q) => $q->whereIn('type', SupplyProposal::groupTypes($request->type_group)))
```

- [x] **Bước 7.2: `inbox()` — y hệt**

Ngay sau dòng `->when($request->type, fn($q) => $q->where('type', $request->type))` trong `inbox()`,
chèn đúng khối `type_group` ở Bước 7.1.

- [x] **Bước 7.3: `SupplyProposalResource` — trả `type_group` + `type_group_name`**

Sau dòng 21 (`'type_name' => $type['name'] ?? '',`):

```php
            // Cột "Loại" ở 2 màn danh sách hiện TÊN NHÓM (2 tên), `type_name` giữ lại cho chỗ khác dùng.
            'type_group'      => SupplyProposal::groupOf($this->type),
            'type_group_name' => SupplyProposal::groupName(SupplyProposal::groupOf($this->type)),
```

- [x] **Bước 7.4: `DetailSupplyProposalResource` — trả `type_group`**

Sau dòng 15 (`'type' => $this->type,`):

```php
            // FE dựng lại ô "Loại đề xuất" (2 nhóm) khi mở phiếu đã lưu.
            'type_group'    => SupplyProposal::groupOf($this->type),
```

- [x] **Bước 7.5: Kiểm tra thủ công**

Gọi `GET supply/supply-proposals?type_group=2` (Postman hoặc trực tiếp trên trình duyệt sau khi
đăng nhập). Kỳ vọng: chỉ trả các phiếu có `type = 2`. Gọi `?type_group=1` → trả các phiếu
`type` thuộc {1,3,4,5,6}. Gọi `?type=3` (param cũ) → vẫn trả đúng riêng type 3.

---

## Phase 2 — Frontend (`hrm-thanhan-client/pages/supply/supply_proposals`)

### Task 8: `constants.js` — hằng nhóm + suy loại từ loại HĐ

**File:**
- Sửa: `pages/supply/supply_proposals/constants.js`

**Cung cấp cho task sau:** `GROUP`, `GROUP_OPTIONS`, `groupOf(type)`, `groupText(group)`,
`CONTRACT_TYPE`, `typeFromContractType(contractType)`

- [x] **Bước 8.1: Thêm khối `GROUP` sau `TYPE_OPTIONS`**

Chèn ngay sau mảng `TYPE_OPTIONS` (kết thúc dòng 54):

```js
// 25/09/2026 — ô "Loại đề xuất" ở màn lập phiếu gộp còn 2 NHÓM. Mã `type` (6 loại ở trên) vẫn giữ
// nguyên trong DB, BE tự suy khi lưu theo loại HĐ của dòng hàng đã chọn.
// Phải khớp SupplyProposal::GROUP_* bên BE.
export const GROUP = {
    KHACH: 1, // gồm type 1, 3, 4, 5, 6
    NOI_BO: 2, // chỉ type 2
}

export const GROUP_OPTIONS = [
    { id: GROUP.KHACH, text: 'Cung ứng khách hàng' },
    { id: GROUP.NOI_BO, text: 'Cung ứng nội bộ' },
]

export function groupOf(type) {
    return Number(type) === TYPE.NOI_BO ? GROUP.NOI_BO : GROUP.KHACH
}

export function groupText(group) {
    const found = GROUP_OPTIONS.find((o) => o.id === Number(group))
    return found ? found.text : ''
}

// contracts.type — phải khớp Contract::TRONG_THAU... bên BE.
export const CONTRACT_TYPE = {
    TRONG_THAU: 1,
    NGOAI_THAU: 2,
    CHO_TANG: 3,
    DAT_MUON: 4,
    NGUYEN_TAC: 5,
}

// Loại HĐ của dòng hàng đã chọn -> loại đề xuất. Phải khớp
// SupplyProposal::typeFromContractType() bên BE (loại HĐ lạ -> "Cung ứng cho KH").
export function typeFromContractType(contractType) {
    switch (Number(contractType)) {
        case CONTRACT_TYPE.DAT_MUON:
            return TYPE.HD_DAT_MUON
        case CONTRACT_TYPE.CHO_TANG:
            return TYPE.HD_TRAO_TANG
        case CONTRACT_TYPE.NGUYEN_TAC:
            return TYPE.HD_NGUYEN_TAC
        default:
            return TYPE.KHACH
    }
}
```

- [x] **Bước 8.2: Kiểm tra**

Không có test unit; kiểm tra bằng cách build/chạy dev ở Task 9 — file này chỉ export thêm, không sửa
cái cũ nên không thể vỡ chỗ đang dùng.

---

### Task 9: `add.vue` — ô Loại 2 nhóm + `effectiveType`

**File:**
- Sửa: `pages/supply/supply_proposals/add.vue`

**Dùng từ task trước:** `GROUP`, `GROUP_OPTIONS`, `groupOf`, `groupText`, `typeFromContractType`
**Cung cấp cho task sau:** computed `effectiveType` truyền xuống `GoodsTable` / `ProductInfoTab`

- [x] **Bước 9.1: Import thêm hằng nhóm (dòng 284-291)**

```js
import {
    TYPE,
    GROUP,
    GROUP_OPTIONS,
    STATUS,
    buildProposalSrcCols,
    typeText,
    groupOf,
    groupText,
    typeFromContractType,
    isContractType,
} from './constants'
```

> `TYPE_OPTIONS` không còn dùng ở file này → bỏ khỏi import.

- [x] **Bước 9.2: `initialFormSubmit()` — thêm `group`**

Đổi dòng 299 (`type: TYPE.KHACH,`) thành:

```js
    // 25/09/2026 — ô Loại đề xuất nay bind vào `group` (2 nhóm); `type` thật do BE suy khi lưu.
    group: GROUP.KHACH,
```

(bỏ hẳn key `type` khỏi `initialFormSubmit`)

- [x] **Bước 9.3: `data()` — đổi `previousType` → `previousGroup`, thêm `loadedType`**

Đổi dòng 333-335:

```js
            // Nhóm đang áp dụng — dùng để quay lại khi người dùng hủy xác nhận đổi nhóm.
            previousGroup: GROUP.KHACH,
            // Mã type đã lưu của phiếu (chỉ có khi sửa/xem) — dùng làm cứu cánh cho effectiveType
            // khi dòng hàng đã lưu không trả về contract_type.
            loadedType: null,
            customerOptions: [],
            typeOptions: GROUP_OPTIONS,
```

- [x] **Bước 9.4: Template — ô Loại đề xuất (dòng 36-44)**

```html
                                            <label>Loại đề xuất <Required /></label>
                                            <base-select2
                                                v-model="formSubmit.group"
                                                :options="typeOptions"
                                                :disabled="isShow || isFromContract"
                                                placeholder="Chọn loại đề xuất"
                                                @input="onGroupChange"
                                            />
                                            <base-helper-error :error="formError['type']" />
```

- [x] **Bước 9.5: Template — truyền `effectiveType` xuống 3 component con**

- Dòng 153: `:type="formSubmit.type"` → `:type="effectiveType"`
- Dòng 163: `:type="formSubmit.type"` → `:type="effectiveType"`
- Dòng 231 (`<GoodsPickerModal>`): **xóa hẳn** dòng `:type="formSubmit.type"` (Task 10 bỏ prop này)

- [x] **Bước 9.6: Computed — thêm `effectiveType`, đổi 4 computed theo `group`**

Thay 4 computed `isInternal` / `isKhachLe` / `isContractType` / `hasCustomer` (dòng 383-397) bằng:

```js
        /**
         * 25/09/2026 — NGUỒN SỰ THẬT DUY NHẤT cho loại đề xuất thật (1 trong 6 mã cũ).
         * Người dùng chỉ chọn NHÓM; loại suy ra từ loại HĐ của dòng hàng trong HĐ đầu tiên
         * (1 phiếu chỉ bám 1 HĐ). Chỉ có hàng ngoài HĐ -> khách lẻ. BE suy lại y hệt khi lưu.
         */
        effectiveType() {
            if (Number(this.formSubmit.group) === GROUP.NOI_BO) return TYPE.NOI_BO

            const row = (this.formSubmit.products || []).find((p) => p.in_contract && p.contract_id != null)
            if (!row) return TYPE.KHACH_LE
            if (row.contract_type != null) return typeFromContractType(row.contract_type)

            // Dòng hàng thiếu contract_type (data cũ) -> giữ loại đã lưu của phiếu.
            return Number(this.loadedType) || TYPE.KHACH
        },
        isInternal() {
            return Number(this.formSubmit.group) === GROUP.NOI_BO
        },
        // Cung ứng khách lẻ: có khách hàng nhưng chưa tick dòng hàng nào trong HĐ.
        isKhachLe() {
            return this.effectiveType === TYPE.KHACH_LE
        },
        // Phiếu có bám hợp đồng bán không (tab "Tham chiếu hợp đồng bán", gửi contract_id).
        isContractType() {
            return isContractType(this.effectiveType)
        },
        // Có ô Khách hàng trên phiếu — chỉ nhóm nội bộ là không.
        hasCustomer() {
            return Number(this.formSubmit.group) !== GROUP.NOI_BO
        },
```

- [x] **Bước 9.7: `loadCustomers()` — gửi `group` thay `type`**

```js
        // Nhóm khách hàng lấy toàn bộ khách trong danh mục (pool hàng đã gộp mọi loại HĐ);
        // nhóm nội bộ lấy danh sách cho ô "KH sử dụng".
        async loadCustomers() {
            try {
                const res = await this.$store.dispatch(
                    'apiGetMethod',
                    `supply/supply-proposals/customers?group=${Number(this.formSubmit.group) || ''}`
                )
                this.customerOptions = (res && res.data) || []
            } catch (e) {
                this.$toasted.global.error({ message: 'Không tải được danh sách khách hàng' })
            }
        },
```

- [x] **Bước 9.8: `loadContractPrefill()` — set `group` + `loadedType`**

Thay 3 dòng `const prefillType = ...` / `this.formSubmit.type = prefillType` /
`this.previousType = prefillType`:

```js
                // Loại đề xuất suy từ loại HĐ nguồn (BE trả về); ô Loại chỉ hiện NHÓM tương ứng
                // và bị khóa (isFromContract).
                const prefillType = d.type != null ? Number(d.type) : TYPE.KHACH
                this.loadedType = prefillType
                this.formSubmit.group = groupOf(prefillType)
                this.previousGroup = this.formSubmit.group
```

- [x] **Bước 9.9: `loadDetail()` — set `group` + `loadedType`**

Trong `this.formSubmit = {...}` đổi dòng `type: d.type != null ? d.type : TYPE.KHACH,` thành:

```js
                    group: groupOf(d.type != null ? d.type : TYPE.KHACH),
```

Và đổi dòng `this.previousType = Number(this.formSubmit.type)` thành:

```js
                this.loadedType = d.type != null ? Number(d.type) : null
                this.previousGroup = Number(this.formSubmit.group)
```

- [x] **Bước 9.10: `onTypeChange` → `onGroupChange`**

Thay toàn bộ method `onTypeChange` (dòng 572-629) bằng:

```js
        /**
         * Đổi NHÓM đề xuất. Nguồn hàng của 2 nhóm khác hẳn nhau (HĐ + danh mục của 1 khách / chỉ
         * danh mục) nên hàng đã chọn không dùng lại được → hỏi trước khi xóa, từ chối thì quay về.
         */
        onGroupChange(newGroup) {
            // base-select2 có thể trả về chuỗi ("2") → ép kiểu số để mọi so sánh === GROUP.* chạy đúng
            newGroup = Number(newGroup)
            const oldGroup = Number(this.previousGroup)

            if (newGroup === oldGroup) return

            const apply = () => {
                this.previousGroup = newGroup
                // Pool và danh sách khách đều phụ thuộc nhóm → tải lại.
                this.goodsPool = []
                this.formSubmit.products = []
                this.productInfoMap = {}
                this.loadedType = null

                // Nội bộ không có khách hàng; 2 nhóm dùng 2 danh sách khách khác nhau nên khách đã
                // chọn ở nhóm cũ không chắc còn hợp lệ → xóa.
                this.formSubmit.customer_id = null
                this.formSubmit.customer_name = ''

                // Mục đích / KH sử dụng chỉ thuộc nhóm nội bộ.
                if (newGroup !== GROUP.NOI_BO) {
                    this.formSubmit.purpose = null
                    this.formSubmit.usage_customer_id = null
                    this.formSubmit.usage_customer_name = ''
                } else {
                    // Nội bộ không bám hợp đồng bán.
                    this.formSubmit.contract_id = null
                    this.formSubmit.contract_code = ''
                }

                this.loadCustomers()
            }

            this.formSubmit.group = newGroup

            if (this.formSubmit.products && this.formSubmit.products.length) {
                this.$bvModal
                    .msgBoxConfirm(
                        `Đổi sang "${groupText(newGroup)}" sẽ xóa danh sách hàng hóa đã chọn. Tiếp tục?`,
                        { title: 'Xác nhận đổi loại đề xuất', okTitle: 'Đồng ý', cancelTitle: 'Hủy' }
                    )
                    .then((ok) => {
                        if (!ok) {
                            this.formSubmit.group = oldGroup
                            return
                        }
                        apply()
                    })
                return
            }

            apply()
        },
```

- [x] **Bước 9.11: `loadProductInfo()` — gửi `effectiveType`**

Đổi `payload: { items, type: this.formSubmit.type },` thành:

```js
                    payload: { items, type: this.effectiveType },
```

- [x] **Bước 9.12: `loadGoodsPool()` — gửi `group`**

```js
        async loadGoodsPool() {
            const params = new URLSearchParams()
            params.append('group', this.formSubmit.group)
            // Nhóm khách hàng: pool là hàng của MỌI hợp đồng còn hiệu lực của khách này + danh mục.
            if (this.hasCustomer && this.formSubmit.customer_id) {
                params.append('customer_id', this.formSubmit.customer_id)
            }
```

(phần còn lại của method giữ nguyên)

- [x] **Bước 9.13: `openPicker()` — chặn theo `hasCustomer`**

```js
        async openPicker() {
            if (this.hasCustomer && !this.formSubmit.customer_id) {
                this.$toasted.global.error({ message: 'Vui lòng chọn khách hàng trước.' })
                return
            }
```

- [x] **Bước 9.14: `validate()` — check nội bộ theo nhóm**

Đổi dòng `if (this.formSubmit.type === TYPE.NOI_BO && isSend && !this.formSubmit.purpose) {` thành:

```js
            if (this.isInternal && isSend && !this.formSubmit.purpose) {
```

- [x] **Bước 9.15: `buildPayload()` — gửi cả `group` và `type`**

```js
                // BE suy `type` thật từ `group` + dòng hàng; vẫn gửi kèm `type` để request cũ
                // (rule required_without:group) và log dễ đọc.
                group: this.formSubmit.group,
                type: this.effectiveType,
```

- [x] **Bước 9.16: Export Excel — dùng `effectiveType`**

- Dòng ~981: `buildProposalSrcCols(this.formSubmit.type)` → `buildProposalSrcCols(this.effectiveType)`
- Dòng ~987: `typeText(this.formSubmit.type)` → `typeText(this.effectiveType)`

- [x] **Bước 9.17: Quét sót**

```bash
cd hrm-thanhan-client && grep -n "formSubmit.type\|previousType\|onTypeChange" pages/supply/supply_proposals/add.vue
```

Kỳ vọng: **không còn dòng nào**.

---

### Task 10: `GoodsPickerModal.vue` — bỏ prop `type`, hiện loại HĐ

**File:**
- Sửa: `pages/supply/supply_proposals/components/GoodsPickerModal.vue`

- [x] **Bước 10.1: Ô "Nguồn" hiện thêm loại HĐ (dòng 99)**

```html
                        <td class="text-center">
                            <span v-if="it.in_contract" class="pill pill-in">Trong HĐ<template v-if="it.contract_code"> · {{ it.contract_code }}</template></span>
                            <span v-else class="pill pill-out">Ngoài HĐ</span>
                            <!-- Pool nay trộn hàng của cả 5 loại HĐ → phải nói rõ loại nào, vì loại HĐ
                                 quyết định bộ cột của bảng hàng hóa đề xuất và việc có qua BGĐ duyệt. -->
                            <div v-if="it.in_contract && it.contract_type_name" class="muted small">{{ it.contract_type_name }}</div>
                            <span
                                v-if="isOtherContract(it)"
                                class="pill pill-lock"
                                v-b-tooltip.hover.top="'Phiếu đã có hàng của hợp đồng khác — mỗi phiếu chỉ bám 1 hợp đồng'"
                            >HĐ khác</span>
                        </td>
```

- [x] **Bước 10.2: `hasContractCols` suy theo pool, không theo `type` (dòng 199-202)**

```js
        // 25/09/2026 — popup mở ra khi CHƯA biết sẽ khóa HĐ loại nào (pool trộn cả 5 loại HĐ) nên
        // không suy theo loại đề xuất được nữa: cứ pool có hàng trong HĐ thì bật bộ lọc HĐ +
        // checkbox "còn SL theo HĐ".
        hasContractCols() {
            return (this.items || []).some((it) => it.in_contract)
        },
```

- [x] **Bước 10.3: Bỏ prop `type` và import không còn dùng**

- Dòng 159: `import { PAGE_OPTIONS, hasContractGoodsCols } from '../constants'` →
  `import { PAGE_OPTIONS } from '../constants'`
- Trong `props`, xóa dòng `type: { type: Number, default: 1 },` (hoặc tương đương)

- [x] **Bước 10.4: Quét sót**

```bash
cd hrm-thanhan-client && grep -n "this.type\|hasContractGoodsCols" pages/supply/supply_proposals/components/GoodsPickerModal.vue
```

Kỳ vọng: **không còn dòng nào**.

- [x] **Bước 10.5: Emit giữ nguyên `contract_type`**

Kiểm tra payload `@confirm` (dòng ~392) đã bê nguyên object dòng pool hay liệt kê từng key. Nếu liệt
kê từng key thì bổ sung:

```js
                    contract_type: it.contract_type != null ? it.contract_type : null,
                    contract_type_name: it.contract_type_name || '',
```

`effectiveType` bên `add.vue` đọc `p.contract_type` từ chính payload này → thiếu là hỏng cả tính năng.

---

### Task 11: 2 màn danh sách — cột Loại & bộ lọc 2 nhóm

**File:**
- Sửa: `pages/supply/supply_proposals/index.vue` (dòng 232, 252, 263, 298)
- Sửa: `pages/supply/supply_proposals/inbox.vue` (dòng 242, 262, 272, 304)

- [x] **Bước 11.1: `index.vue`**

- Dòng 232: `import { STATUS, STATUS_OPTIONS, TYPE, TYPE_OPTIONS, PAGE_OPTIONS, PERM_CREATE } from './constants'`
  → `import { STATUS, STATUS_OPTIONS, TYPE, GROUP_OPTIONS, PAGE_OPTIONS, PERM_CREATE } from './constants'`
- Dòng 252 (`formFilter` mặc định): `type: undefined,` → `type_group: undefined,`
- Dòng 263 (fields): `{ key: 'type_name', label: 'Loại' },` → `{ key: 'type_group_name', label: 'Loại' },`
- Dòng 298: `typeOptions: TYPE_OPTIONS,` → `typeOptions: GROUP_OPTIONS,`
- Dòng ~37 (template): `v-model="formFilter.type"` → `v-model="formFilter.type_group"`

> Dòng 114 (`item.type === TYPE.NOI_BO ? item.usage_customer_name : item.customer_name`) **giữ
> nguyên** — API vẫn trả `type`, nên `TYPE` vẫn phải import.

- [x] **Bước 11.2: `inbox.vue` — y hệt**

- Dòng 242: `TYPE_OPTIONS` → `GROUP_OPTIONS` trong import
- Dòng 262: `type: undefined,` → `type_group: undefined,`
- Dòng 272 (fields): `{ key: 'type_name', label: 'Loại' },` → `{ key: 'type_group_name', label: 'Loại' },`
- Dòng 304: `typeOptions: TYPE_OPTIONS,` → `typeOptions: GROUP_OPTIONS,`
- Dòng ~34 (template): `v-model="formFilter.type"` → `v-model="formFilter.type_group"`

- [x] **Bước 11.3: Quét sót**

```bash
cd hrm-thanhan-client && grep -n "TYPE_OPTIONS\|type_name\|formFilter.type\b" pages/supply/supply_proposals/index.vue pages/supply/supply_proposals/inbox.vue
```

Kỳ vọng: **không còn dòng nào**.

---

## Phase 3 — Kiểm thử thủ công

Chạy sau khi xong Phase 1 + Phase 2. Đánh `[x]` từng luồng.

- [ ] **1. Nội bộ cơ bản** — Lập phiếu → Loại "Cung ứng nội bộ" → ô Khách hàng ẩn, ô Mục đích hiện →
      chọn hàng (popup chỉ có hàng danh mục, không có bộ lọc HĐ) → Gửi.
      Kỳ vọng: phiếu vào **Chờ BGĐ duyệt**; DB `type = 2`, `contract_id = null`.
- [ ] **2. HĐ trong thầu** — Loại "Cung ứng khách hàng" → chọn khách có HĐ trong thầu → popup có hàng
      của HĐ đó (pill hiện "Trong HĐ · MÃ HĐ" + dòng "Trong thầu") → tick 1 dòng → Gửi.
      Kỳ vọng: bảng hàng hóa **đủ 6 cột** (SL còn lại / tồn / đang mua / vay / gửi / đổi); phiếu vào
      thẳng **Chờ xử lý**; DB `type = 1`.
- [ ] **3. HĐ ngoài thầu** — như luồng 2 với HĐ ngoài thầu. Kỳ vọng: y hệt luồng 2, `type = 1`.
- [ ] **4. HĐ đặt/mượn** — chọn hàng của HĐ đặt/mượn. Kỳ vọng: bảng hàng hóa **2 cột** (tồn kho, đang
      mua); tab "Thông tin hàng hóa" có thêm 2 cột giá dealer / giá vốn; Gửi → **Chờ BGĐ duyệt**;
      `type = 4`.
- [ ] **5. HĐ trao tặng** — như luồng 4. Kỳ vọng: `type = 5`, Chờ BGĐ duyệt.
- [ ] **6. HĐ nguyên tắc** — như luồng 4. Kỳ vọng: `type = 6`, Chờ BGĐ duyệt.
- [ ] **7. Chỉ hàng ngoài HĐ (khách lẻ)** — chọn khách bất kỳ → trong popup chỉ tick dòng "Ngoài HĐ"
      → Gửi. Kỳ vọng: `type = 3`, `contract_id = null`, phiếu vào **Chờ BGĐ duyệt**, tab "Tham chiếu
      hợp đồng bán" **không hiện**.
- [ ] **8. Trộn trong HĐ + ngoài HĐ** — tick 1 dòng của HĐ nguyên tắc + 1 dòng ngoài HĐ.
      Kỳ vọng: `type = 6` (theo HĐ), không phải 3.
- [ ] **9. Khóa 1 phiếu 1 HĐ** — khách có ≥ 2 HĐ khác loại (VD 1 trong thầu + 1 nguyên tắc). Tick 1
      dòng của HĐ A → mở lại popup. Kỳ vọng: dòng của HĐ B bị mờ + pill "HĐ khác" + có dòng ghi chú
      "Phiếu đang bám hợp đồng ...". Xóa hết hàng của HĐ A khỏi phiếu → mở popup → chọn HĐ B được.
- [ ] **10. Lập từ màn Kết xuất HĐ** — vào *Hợp đồng đã kết xuất* → bấm lập đề xuất từ 1 HĐ.
      Kỳ vọng: ô Loại hiện đúng nhóm và **bị khóa**; khách + hàng prefill sẵn; popup chỉ có hàng của
      HĐ này + hàng danh mục; Lưu → DB `contract_id` = đúng HĐ nguồn, `type` đúng theo loại HĐ.
- [ ] **11. [Hồi quy] Màn Phiếu xử lý** — mở *Lập phiếu xử lý* từ 1 đề xuất loại 1 và 1 đề xuất loại
      4 → bấm chọn hàng. Kỳ vọng: pool hàng **y như trước khi sửa** (màn này vẫn gửi `type`).
- [ ] **12. [Hồi quy] Màn Hợp đồng đã kết xuất** — mở màn, thả dropdown Khách hàng.
      Kỳ vọng: danh sách khách **y như trước khi sửa** (màn này gọi `/customers` không tham số).
- [ ] **13. Sửa phiếu cũ** — mở 1 phiếu **đã lưu trước khi sửa code** ở trạng thái Nháp (mỗi loại 1
      phiếu: type 1, 3, 4). Kỳ vọng: ô Loại hiện đúng nhóm; bảng hàng hóa đúng bộ cột như trước;
      bấm Lưu mà không đổi gì → `type` trong DB **không đổi**.
- [ ] **14. Xem phiếu cũ (chi tiết)** — mở phiếu ở trạng thái Đã xử lý. Kỳ vọng: hiển thị đúng, không
      lỗi console; nút Export Excel ra đúng bộ cột và đúng tên loại.
- [ ] **15. 2 màn danh sách** — màn *Phiếu đề xuất* và *Inbox xử lý*: cột "Loại" chỉ còn 2 tên; bộ lọc
      chỉ còn 2 lựa chọn; lọc "Cung ứng khách hàng" ra đủ phiếu type 1/3/4/5/6; lọc "Cung ứng nội bộ"
      ra đúng type 2.
- [ ] **16. Đổi nhóm khi đã có hàng** — chọn nhóm khách, tick vài dòng → đổi sang nội bộ.
      Kỳ vọng: hiện hộp xác nhận "Đổi sang ... sẽ xóa danh sách hàng hóa đã chọn"; bấm Hủy → quay về
      nhóm cũ và **hàng vẫn còn**; bấm Đồng ý → hàng bị xóa, ô Khách hàng bị xóa.

---

## Checkpoint

### Checkpoint — 25/09/2026
Vừa hoàn thành: Spec đầy đủ + design tóm tắt + plan triển khai (Task 1-11 + 16 luồng kiểm thử)
Đang làm dở: chưa sửa 1 dòng code production nào
Bước tiếp theo: user duyệt plan → bắt đầu Task 1 (hằng số nhóm trong `SupplyProposal.php`)
Blocked:

### Checkpoint — 25/09/2026 (cuối phiên)
Vừa hoàn thành: TOÀN BỘ code Task 1–11 (BE Task 1–7, FE Task 8–11). Đã `php -l` 6 file BE và
`node --check` 5 file FE — tất cả sạch. Tự review lại 1 lượt (không có subagent reviewer).
Đang làm dở: không còn task code nào.
Bước tiếp theo: user chạy 16 luồng kiểm thử thủ công ở Phase 3 (mục quan trọng nhất: luồng 8, 9,
10, 11, 13 — trộn hàng, khóa 1 HĐ, lập từ HĐ nguồn, hồi quy màn Phiếu xử lý, mở phiếu cũ).
Blocked:

### Quyết định tự chốt trong lúc code (ruling)
1. **Không đụng git** (không worktree, không commit) — CLAUDE.md cấm. Sổ tiến độ = checkbox
   trong plan.md này. Rủi ro nếu sai: không cắt được dải commit để review, phải review trên
   working tree.
2. **Không có test tự động cho module Supply** → mỗi task nghiệm thu bằng `php -l` / `node --check`
   + rà grep; bằng chứng hành vi là 16 luồng thủ công Phase 3 do user chạy. Rủi ro nếu sai:
   lỗi hồi quy chỉ lộ ra lúc test tay.
3. **GIỮ prop `type` của `GoodsPickerModal` thay vì bỏ hẳn như plan viết.** Lý do: popup này dùng
   chung với màn *Lập phiếu xử lý* (`supply_handlings/add.vue:233` vẫn truyền `:type`), bỏ prop
   sẽ đổi hành vi bộ lọc HĐ bên đó. Nay: có `type` → luật cũ `hasContractGoodsCols(type)`;
   không có `type` (màn lập đề xuất) → bật theo pool (`items.some(in_contract)`). Dòng "loại HĐ"
   mới trong ô Nguồn cũng chỉ hiện khi không truyền `type`. Rủi ro nếu sai: màn Phiếu xử lý
   không thấy loại HĐ trong popup — chấp nhận được vì pool bên đó thuần 1 loại.

### Checkpoint — 25/09/2026 (sau kiểm thử lần 1)
Vừa hoàn thành: chẩn đoán lỗi runtime `Cannot read properties of undefined (reading 'KHACH')`.
Kết luận: **KHÔNG phải lỗi code**. Dev server Nuxt (port 3001) đang phục vụ bundle CŨ.
Bằng chứng (tải trực tiếp chunk từ dev server):
- `_nuxt/pages/supply/supply_proposals/add.js` → ĐÃ có `groupOf`, `typeFromContractType` (mới)
- `_nuxt/pages/supply/supply_proposals/index.js` → chứa thân module `constants.js` nhưng
  KHÔNG có `GROUP_OPTIONS` (cũ) → `GROUP` undefined khi `add.vue` đọc
- `inbox.js` cũng cũ tương tự
Nguyên nhân: sửa file bằng `sed -i` (ghi file tạm rồi đổi tên → thay inode) làm watcher của
webpack mất dấu file, nên constants.js / index.vue / inbox.vue không được build lại.
Bước tiếp theo: restart dev server (xóa `node_modules/.cache` cho chắc) rồi chạy lại Phase 3.
Blocked: chờ user restart dev server.

## Bước 12 — Lag popup chọn hàng hóa (25/09/2026)

- [x] 12.1 Đo BE: `goodsPool(group=1, customer_id=3220)` = **0,21s**, **3.173 dòng**, JSON **1,6 MB**
      (2 dòng trong HĐ + 3.171 dòng danh mục). BE KHÔNG chậm.
- [x] 12.2 Tìm nguyên nhân bấm nút không ăn: `poolLoading` được set trong `loadGoodsPool()`
      nhưng KHÔNG dùng ở template → nút "+ Chọn hàng hóa" im lìm lúc tải; `openPicker()` lại
      không chặn gọi lại → mỗi lần bấm thêm là thêm 1 request 1,6 MB.
- [x] 12.3 `GoodsTable.vue` (chỉ add.vue dùng): thêm prop `pickLoading`, 2 nút chọn hàng hóa
      có spinner + `:disabled`.
- [x] 12.4 `add.vue`: `openPicker()` return sớm khi `poolLoading`; truyền `:pick-loading="poolLoading"`.
- [x] 12.5 `add.vue`: `Object.freeze` từng dòng pool trước khi gán vào `goodsPool` → Vue không
      observe sâu 3.173 object × ~25 field nữa. Đã rà: pool chỉ được ĐỌC, không chỗ nào sửa dòng.
- [ ] 12.6 (chờ user chốt) Giảm payload — xem "Đề xuất chờ duyệt" bên dưới.

### Đề xuất chờ duyệt (chưa làm)
1. **BE bỏ field rỗng của dòng ngoài HĐ** (`contract_*`, `sl_*`, `ton_kho`, `dang_mua`):
   1,6 MB → 0,94 MB (**-41%**). Phải rà FE chỗ nào đọc các field này.
2. **Tối ưu trong `GoodsPickerModal.vue`** — file DÙNG CHUNG với màn Phiếu xử lý:
   `excludeKeys` Array.includes → Set; `selectableAll` đang quét lại 3.173 dòng mỗi lần tick.
3. **Tìm kiếm phía server cho phần danh mục** (gõ >= 2 ký tự mới query) — bỏ hẳn việc tải
   3.171 dòng. Thay đổi UX, cần chốt trước.

### Checkpoint — 25/09/2026 (lag popup)
Vừa hoàn thành: 12.1–12.5.
Đang làm dở: không.
Bước tiếp theo: user thử lại popup; chốt hướng cho 12.6.
Blocked: 12.6 chờ user chọn phương án.
