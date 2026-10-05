# Phase 2 — Màn danh mục hàng hoá (danh sách + tạo/sửa) — PLAN

> Nhánh: `gop_db` · Phụ trách: @namdangit · Mở 21/09/2026
> Đọc kèm: `design.md` (9 quyết định + mockup) · `khao-sat.md` · `khao-sat-don-vi-tinh-gia-ban.md`
> · `yeu-cau-khach.md`

## Đợt 0 — Khảo sát & chốt thiết kế (ĐANG LÀM)

- [x] **T0.1** Khảo sát màn hàng hoá ERP → `khao-sat.md`
      (59 cột · 171 bảng FK · controller 4.623 dòng · model 8.122 dòng · form 95KB × 2 ·
      17 khối form · 29 cột danh sách)
- [x] **T0.2** Nhận tài liệu 6 tab của khách → `yeu-cau-khach.md`
- [x] **T0.3** Chốt 8 quyết định về trường & phân loại → `design.md` §1-§8
- [x] **T0.4** Khảo sát Đơn vị tính ↔ Giá bán → `khao-sat-don-vi-tinh-gia-ban.md`
- [x] **T0.5** Chốt quyết định giá: giữ nguyên logic, chỉ bỏ đồng bộ CRM → `design.md` §9
- [x] **T0.6** Dựng mockup 2 màn (trang Nuxt thật, dữ liệu tĩnh)
- [x] **T0.7** Rà soát trường thiếu + bổ sung thao tác đầy đủ (vòng 3)
- [x] **T0.8** Sửa mockup theo góp ý vòng 2-5
- [x] **T0.9** Icon cho tiêu đề card (vòng 5) · "Đặc điểm" đổi sang CKEditor 5 (vòng 6)
- [x] **T0.10** Xuất **bản HTML độc lập** gửi khách + script xuất lại
- [x] **T0.11** Commit mockup lên nhánh `feat/p1-danh-muc-hang-hoa` (`3863a9bc7`)
- [ ] **T0.12** ⏳ **User / khách duyệt mockup** ← ĐANG CHỜ
- [x] **T0.13** Viết spec đầy đủ →
      `docs/superpowers/specs/gop-db/2026-09-21-man-danh-muc-hang-hoa-design.md`
      (schema · API contract · validate · quyền · hiệu năng · việc treo · cách kiểm).
      Viết TRƯỚC khi khách duyệt: phần bố cục có thể đổi, phần DB/API bám 9 quyết định đã chốt
      nên ổn định. Đã tự soát: 9/9 số liệu và 5/5 đường dẫn file trích trong spec đều khớp thực tế.
- [ ] **T0.14** Sau khi khách duyệt mockup: rà lại spec rồi lên plan các đợt code

## Đợt 1+ — Code (CHƯA MỞ, chờ chốt mockup)

Sẽ chia đợt sau khi có spec. Các việc đã biết chắc phải nằm trong đó:

- [ ] Thêm `products.product_type_id` (+ `product_characteristic_id`) và nạp cây phân loại vào form
- [ ] **Nâng bảng nối thuộc tính lên cấp Nhóm sản phẩm**: `product_type_attributes` →
      `product_family_attributes`; chuyển ô "Thuộc tính" từ màn Loại sản phẩm sang màn Nhóm sản phẩm
      (⚠️ làm SỚM — 3 bảng đang 0 dòng nên chưa phải di trú dữ liệu)
- [ ] Gỡ ô `can_retail` khỏi màn Loại sản phẩm (Phase 0)
- [ ] Bỏ 2 điều kiện lọc theo enum cũ trong `SearchController` (4 hàm) — **cần khách xác nhận trước**
      vì nới lỏng hành vi đang chạy
- [ ] Bỏ đồng bộ CRM **nhánh hàng hoá** (13+ model) — ⚠️ giữ nguyên nhánh nhân sự
- [ ] BE + FE màn danh sách · BE + FE màn tạo/sửa 5 tab
- [ ] Quyền + menu + Import/Export + lịch sử thay đổi

---

### Checkpoint — 21/09/2026 (mở Phase 2, khảo sát + mockup xong)

**Vừa hoàn thành:** đợt 0 từ T0.1 đến T0.8.

**Mockup đang chạy** (trang Nuxt thật, dữ liệu tĩnh, KHÔNG gọi API):
- `/master-data/mockup-hang-hoa` — danh sách
- `/master-data/mockup-hang-hoa/form` — tạo/sửa 5 tab
- File: `hrm-client/pages/master-data/mockup-hang-hoa/{index,form}.vue` — **xoá sau khi chốt**

**5 vòng sửa mockup theo góp ý user:**
1. Dựng lần đầu (6 tab theo tài liệu) → chốt gộp còn **5 tab**, cột danh sách theo cây mới
2. Thêm card **Đơn vị tính** ở tab 1 (trên card file đính kèm); tab **Giá bán** đổi thành tab lồng
   **Công ty → Đơn vị tính** theo khuôn ERP
3. Tab **Dữ liệu quản trị** cũng đổi sang tab theo công ty
4. Rà soát trường thiếu + bổ sung **thao tác đầy đủ** (cột Hành động 6 thao tác, xoá hàng loạt,
   footer Sao chép/In tem/Lịch sử, thao tác tệp-ảnh, nút xoá dòng ở mọi bảng)
5. **Bảo hành + Hệ số công nghệ** chuyển sang Dữ liệu quản trị theo công ty; thêm lại cột
   **Giá công thức** (chỉ đọc)

**4 lỗi của chính mockup, tự bắt được khi đo:**
1. 🔴 Slot `V2BaseDataTable` viết sai khuôn (`#cell(key)="{ row }"` thay vì `#cell-<key>="{ item }"`)
   → 4 ô hiện giá trị thô, mất ảnh/link/badge/dòng phụ mà **Vue không báo lỗi**. Đã lưu memory.
2. `sticky: 'right'` không tồn tại — component hiểu thành ghim TRÁI.
3. Ô **"Serial number"** thêm nhầm: ERP form không bind, `products.serial_number` **0/45.890 dòng**.
4. Đo trang có **tab lồng**: `querySelector('.tab-pane.active')` trả về pane con của tab khác →
   báo nhầm "tab Giá bán có Bảo hành". Phải lấy con trực tiếp của `.tab-content` cấp 1.

**Đang làm dở:** (không)

**Bước tiếp theo:** user duyệt mockup (T0.9). Duyệt xong → viết spec (T0.10) → lên plan code.

**Blocked:**
- Chờ user duyệt mockup.
- Cần khách xác nhận **cách tính "Giá công thức"** — đường dữ liệu đã đứt từ 2020, không nơi nào
  trong ERP tính ra nó.
- Cần khách xác nhận việc **bỏ 2 điều kiện lọc** trong `SearchController` (nới lỏng hành vi thật:
  30 hàng dịch vụ lọt vào popup của 338 màn; báo giá dịch vụ chọn được 45.890 thay vì 12.426).
- Phase 1 vẫn chờ user cherry-pick `221cda7b2` về `gop_db`.

---

### Checkpoint — 21/09/2026 (mockup hoàn chỉnh + bản gửi khách + đã commit)

**Vừa hoàn thành** (tiếp sau checkpoint trước, thêm 3 việc):

**1. Vòng 5 — icon cho tiêu đề card.** Dùng slot `#title` có sẵn của `V2BaseFormSection`, **không
sửa component dùng chung** (file đó 35 màn đang dùng). Chỉ chọn icon **đã xuất hiện thật** trong
hrm-client (đếm được 324 icon `ri-*` đang dùng) để né bẫy 2 bản Remix Icon lệch codepoint.
Đo: 15/15 card đang hiển thị có icon, 0 icon rộng 0px.

**2. Vòng 6 — "Đặc điểm" đổi sang ô nhập CÓ ĐỊNH DẠNG.** Khớp ERP (`ck-editor`). hrm-client có 2
cơ chế song song — chọn **CKEditor 5** (`<ckeditor>`, 25 màn dùng) thay vì `$loadCKEditor`
(CKEditor 4, dành cho mẫu in). Toolbar rút gọn 7 nút. Đo: editor 608×285px, nội dung giữ
`<strong>` + `<ul><li>`.
📌 Còn **"Phụ kiện tiêu chuẩn"** cũng là `ck-editor` bên ERP (`form.blade.php:864`) — chưa đổi,
chờ user xác nhận.

**3. Bản HTML độc lập gửi khách** — `man-danh-muc-hang-hoa/mockup-hang-hoa.html` (**3,1 MB**), mở
bằng nháy đúp, không cần server/internet. Script xuất lại: `e2e/xuat-mockup.js`.

**4. Đã commit** (user chốt: chỉ commit ở nhánh hiện tại, **không merge**):
`3863a9bc7` — mockup 2 màn, commit message ghi rõ "xoá thư mục này sau khi chốt".

**3 bẫy khi xuất HTML độc lập** (ghi để lần sau khỏi vấp — chi tiết ở `design.md`):
1. Chromium mới **không có phiên đăng nhập** → trang đẩy về `/login`. Phải nạp `storageState` từ
   `e2e/.auth/user.json`.
2. 🔴 `remixicon.css` có **HAI khối `src:`** — thay mỗi khối đầu thì khối sau đè lên, icon thành ô
   vuông rỗng. Phải dựng lại cả khối `@font-face`.
3. 5 font cục bộ nạp từ `/_nuxt/assets/fonts/*` — không tồn tại khi mở `file://`, phải nhúng base64.

⚠️ **Đo bề rộng icon > 0 KHÔNG đủ** để kết luận icon đúng — ô vuông rỗng cũng có bề rộng. Phải so
bề rộng giữa font icon và font thường (đo được **64px vs 46px**) hoặc dùng `document.fonts.check`.

**Đang làm dở:** (không)

**Bước tiếp theo:** gửi `mockup-hang-hoa.html` cho khách → khách duyệt → viết spec (T0.13).

**Blocked:**
- Chờ duyệt mockup.
- Chờ khách chốt **cách tính "Giá công thức"** (đường dữ liệu đứt từ 2020).
- Chờ khách xác nhận **bỏ 2 điều kiện lọc** trong `SearchController`.
- Chờ user chốt **"Phụ kiện tiêu chuẩn"** có đổi sang CKEditor không.

---

# PLAN THỰC THI — Phase 2: chuyển màn danh mục hàng hoá sang HRM

> **Spec:** `docs/superpowers/specs/gop-db/2026-09-21-man-danh-muc-hang-hoa-design.md`
> **Quyết định:** `design.md` mục 1–13 · **Hợp đồng ERP:** `hop-dong-tuong-thich-erp.md`
> **Việc sửa ERP:** `sua-erp-de-khong-loi.md` · **Mockup:** `hrm-client/pages/master-data/mockup-hang-hoa/`
>
> **Mục tiêu:** đưa màn danh sách + tạo/sửa hàng hoá sang HRM, **ERP vẫn chạy ổn định**.
> **Kiến trúc:** HRM ghi thẳng bảng `products` của ERP (không di trú dữ liệu). Thêm 2 cột FK trỏ cây
> phân loại Phase 0. ERP bị chặn route tạo/sửa và được vá null-safe để đọc được hàng hoá thiếu cột cũ.
> **Tech:** Laravel 8 + `nwidart/laravel-modules` (`Modules/MasterData`) · Nuxt 2 / Vue 2 + V2Base*.

## Ràng buộc xuyên suốt (mọi task đều phải theo)

- **KHÔNG** dùng `DB_CONNECTION_SECOND` / `mysql2` — DB đã gộp, join thẳng.
- **KHÔNG** khai FK ràng buộc trên `products` (171 bảng tham chiếu) — chỉ index + `exists:` ở validate.
- **KHÔNG** đổi ngữ nghĩa cột cũ nào; chỉ THÊM cột.
- Model mới `extends BaseModel`; `Product` của ERP **không** extends BaseModel ⇒ HRM **tự gán**
  `created_by`/`updated_by` ở mọi đường ghi **kể cả khoá/mở khoá**. Dùng `auth()->id()`.
- FormRequest **chỉ khai `rules()`**, không khai `messages()`.
- Mọi element form dùng `V2Base*`, không HTML thô. Mỗi `.form-row` đủ **12 cột**.
- Cờ quyền FE khởi tạo `false`, chỉ set từ `$store.state.permissions`. Cấm gán literal `true`.
- Nút không dùng được thì **ẩn** (`visible`/`v-if`), không disable.
- Slot của `V2BaseDataTable` là **`#cell-<key>="{ item }"`**, cột hành động `key: 'actions'`.
- Số: `,` ngăn nghìn + `.` thập phân (`toLocaleString('en-US')` / `number_format()` mặc định).
- Chạy e2e **chỉ khi user yêu cầu**; nhưng **mọi task đụng UI phải kiểm bằng Playwright**, đo số từ DOM.

---

## Đợt A — Nền tảng & CSDL

### Task A0: Nhánh làm việc

**Quyết định cần user chốt trước khi bắt đầu** (2 repo đang đứng ở `gop_db`):

| Cách | Việc |
|---|---|
| (a) **Merge Phase 1 về `gop_db` trước**, rồi mở `feat/p2-man-hang-hoa` từ `gop_db` | Sạch nhất. Cần user duyệt Phase 1 |
| (b) Mở `feat/p2-man-hang-hoa` **từ `feat/p1-danh-muc-hang-hoa`** | Làm được ngay, nhưng Phase 2 thừa kế commit Phase 1 chưa duyệt |

⚠️ Phase 2 **phụ thuộc Phase 1**: form hàng hoá dùng 11 danh mục (ĐVT, thương hiệu, hãng SX, xuất xứ,
code đặt hàng, thuộc tính, đơn vị thuộc tính, thuế suất…). Không có Phase 1 thì `GET /form-options`
không có nguồn.

- [x] **A0.1** ✅ User chốt 21/09: **(c) làm tiếp ngay trên `feat/p1-danh-muc-hang-hoa`** — không mở nhánh mới
- [x] **A0.2** `git fetch origin && git checkout -b feat/p2-man-hang-hoa <gốc đã chốt>` ở **cả 2 repo**
- [x] **A0.3** Xác minh: `git branch --show-current` ra `feat/p2-man-hang-hoa` ở cả 2 repo; `git status` sạch

### Task A1: Migration — 2 cột phân loại trên `products`

**Files:**
- Create: `hrm-api/Modules/MasterData/Database/Migrations/2026_09_22_000001_add_classification_to_products_table.php`

- [x] **A1.1** Chụp số dòng trước khi làm gì

```bash
cd hrm-api && php artisan tinker --execute='printf("products=%s\n", DB::table("products")->count());'
```
Ghi lại con số (mong đợi **45.890**).

- [x] **A1.2** Viết migration

```php
<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

/**
 * Nối hàng hoá vào CÂY PHÂN LOẠI mới của Phase 0.
 *
 * `nullable` vì 45.890 hàng hoá cũ chưa có phân loại, và trong giai đoạn chuyển tiếp ERP vẫn tạo
 * hàng hoá qua đường hàng tạm. Bắt buộc CHỈ áp ở tầng validate của HRM.
 *
 * KHÔNG khai foreign key: `products` đang được 171 bảng tham chiếu và ERP vẫn ghi vào — thêm ràng
 * buộc cứng làm tăng rủi ro chặn ghi ở đường ERP. Dùng index + rule `exists:` ở FormRequest.
 *
 * KHÔNG lưu 3 cấp cha (nature / function_group / family): cây có FK NOT NULL từng cấp nên truy
 * ngược từ `product_type_id` là đủ và không bao giờ lệch.
 */
return new class extends Migration
{
    public function up(): void
    {
        Schema::table('products', function (Blueprint $table) {
            $table->unsignedBigInteger('product_type_id')->nullable()->after('group_id');
            $table->unsignedBigInteger('product_characteristic_id')->nullable()->after('product_type_id');
            $table->index('product_type_id');
            $table->index('product_characteristic_id');
        });
    }

    public function down(): void
    {
        Schema::table('products', function (Blueprint $table) {
            $table->dropIndex(['product_type_id']);
            $table->dropIndex(['product_characteristic_id']);
            $table->dropColumn(['product_type_id', 'product_characteristic_id']);
        });
    }
};
```

- [x] **A1.3** Chạy thử KHÔNG ghi

```bash
cd hrm-api && php artisan migrate --path=Modules/MasterData/Database/Migrations --pretend
```
Kết quả mong đợi: in ra 2 câu `alter table` + 2 `create index`, **không** có câu nào đụng bảng khác.

- [x] **A1.4** Chạy thật rồi kiểm

```bash
php artisan migrate --path=Modules/MasterData/Database/Migrations --force
php artisan tinker --execute='
$c = collect(DB::select("SHOW COLUMNS FROM products"))->pluck("Field");
printf("product_type_id: %s | product_characteristic_id: %s | số dòng: %s\n",
  $c->contains("product_type_id") ? "OK" : "THIẾU",
  $c->contains("product_characteristic_id") ? "OK" : "THIẾU",
  number_format(DB::table("products")->count()));'
```
Đạt khi: cả 2 cột **OK** và số dòng **vẫn 45.890** (migration không được làm mất dòng nào).

- [x] **A1.5** Commit

```bash
git add Modules/MasterData/Database/Migrations/2026_09_22_000001_add_classification_to_products_table.php
git commit -m "[gop_db] Hàng hoá P2: thêm product_type_id + product_characteristic_id vào products"
```

### Task A2: Gỡ `can_retail` khỏi Loại sản phẩm

> ✅ **Sửa lại 21/09 (user đính chính):** *"Thuộc tính sản phẩm sẽ nối lên **Loại sản phẩm** chứ
> không phải Nhóm sản phẩm."* ⇒ **GIỮ NGUYÊN `product_type_attributes` của Phase 0**, KHÔNG tạo
> `product_family_attributes`, KHÔNG chuyển ô "Thuộc tính" sang màn Nhóm sản phẩm.
> Task này vì thế chỉ còn việc gỡ `can_retail` (quyết định 4).

**Files:**
- Create: `hrm-api/Modules/MasterData/Database/Migrations/2026_09_22_000002_drop_can_retail_from_product_types_table.php`
- Modify: `hrm-api/Modules/MasterData/Entities/ProductClassification/ProductType.php`
- Modify: `hrm-client/pages/master-data/product-types/AddProductTypeModal.vue`
- Modify: `hrm-client/pages/master-data/product-types/index.vue`

- [x] **A2.1** Xác minh `product_types` đang trống (nếu KHÁC 0 thì dừng, báo user)

```bash
php artisan tinker --execute='printf("product_types=%s
", DB::table("product_types")->count());'
```

- [x] **A2.2** Migration gỡ cột

```php
public function up(): void
{
    Schema::table('product_types', fn (Blueprint $t) => $t->dropColumn('can_retail'));
}

public function down(): void
{
    Schema::table('product_types', fn (Blueprint $t) => $t->boolean('can_retail')->default(false));
}
```

- [x] **A2.3** `ProductType.php`: gỡ `'can_retail'` khỏi `$fillable` **và** khỏi `$casts`.
- [x] **A2.4** FE: gỡ ô `can_retail` khỏi `AddProductTypeModal.vue` + cột tương ứng ở `index.vue`.
      Gỡ khỏi `ExportColumnRegistry` / `CatalogHistoryService::TABLES` nếu có khai.
- [x] **A2.5** Bố cục: gỡ 1 ô làm hàng đó thiếu cột ⇒ **xếp lại cho mỗi `.form-row` đủ 12 cột**.
- [x] **A2.6** Kiểm Playwright: mở `/master-data/product-types`, popup Tạo mới ⇒ **không còn** chữ
      "bán lẻ"; mọi `.form-row` đủ 12 cột, các ô cùng hàng cùng `top`.
- [x] **A2.7** Commit

```bash
git commit -am "[gop_db] Hàng hoá P2: gỡ can_retail khỏi Loại sản phẩm"
```

### Task A3: Quyền + route rỗng

**Files:**
- Modify: `hrm-api/Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php`
- Modify: `hrm-api/Modules/MasterData/Routes/api.php`

- [x] **A3.1** Kiểm id lớn nhất đang dùng (mong đợi **1611**)

```bash
grep -oE "'id' => [0-9]+" Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php \
  | grep -oE "[0-9]+" | sort -n | tail -1
```

- [x] **A3.2** ⚠️ **Dùng 1616–1619**, KHÔNG phải 1612-1615 (id đó đã bị nhánh khác chiếm — xem checkpoint). Thêm 4 quyền, `group = 'Danh mục hàng hóa'`, `type = 9`:
      `Xem hàng hoá` · `Quản lý hàng hoá` · `Xoá hàng hoá` · `Xuất dữ liệu hàng hoá`

⚠️ **KHÔNG chạy `PermissionsTableSeeder`** trên DB đã có dữ liệu — nó **truncate cả bảng**.
Cấp quyền bằng SQL thủ công, và **xoá cache spatie** sau đó:

```bash
php artisan cache:forget spatie.permission.cache || php artisan cache:clear
```

- [x] **A3.3** Kiểm không trùng id

```bash
grep -oE "'id' => [0-9]+" Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php \
  | grep -oE "[0-9]+" | sort -n | uniq -d
```
Đạt khi: **rỗng**.

- [x] **A3.4** Khai nhóm route `products` với đủ 13 endpoint của spec §3 (ô `attributes-by-family`
      đổi thành **`attributes-by-type`**), gắn `checkPermission`.
      ⚠️ `/export`, `/export-rows`, `/form-options`, `/bulk-delete` phải đứng **TRƯỚC** `/{id}`,
      nếu không bị route động nuốt.

- [x] **A3.5** Commit

---

## Đợt B — BE đọc

### Task B1: Entity `Product` + quan hệ

**Files:**
- Create: `hrm-api/Modules/MasterData/Entities/Product/Product.php`

**Produces:** `Modules\MasterData\Entities\Product\Product` với quan hệ
`productType()` · `characteristic()` · `units()` · `attributes()` · `suppliers()` ·
`techAttachments()` · `galleries()` · `videos()` · `companyCoefficients()` ·
`recipeProducts()` · `accessories()` · `installAccessories()` · `repairAccessories()`

- [x] **B1.1** Viết Entity. **Không** `extends BaseModel` — bảng của ERP có `created_by` NOT NULL và
      quy ước riêng; gán tay trong Service.

```php
protected $table = 'products';
protected $fillable = [ /* … 59 cột hợp lệ + product_type_id + product_characteristic_id … */ ];

public function productType()   { return $this->belongsTo(ProductType::class, 'product_type_id'); }
public function characteristic(){ return $this->belongsTo(ProductCharacteristic::class, 'product_characteristic_id'); }
public function units()         { return $this->hasMany(ProductUnit::class, 'product_id'); }
```

⚠️ **Không đặt quan hệ tên `product_type()`** — trùng cột chuỗi cũ `products.product_type`.

- [x] **B1.2** Test: đọc 1 hàng hoá thật, khẳng định quan hệ chạy

```bash
php artisan tinker --execute='
$p = Modules\MasterData\Entities\Product\Product::with("units")->first();
printf("id=%s code=%s units=%s\n", $p->id, $p->code, $p->units->count());'
```
Đạt khi: in ra mã dạng `CH-RRI32` và số ĐVT ≥ 1.

- [x] **B1.3** Commit

### Task B2: `GET /form-options`

**Files:**
- Create: `hrm-api/Modules/MasterData/Http/Controllers/V1/Product/ProductOptionController.php`
- Create: `hrm-api/Modules/MasterData/Services/Product/ProductOptionService.php`

**Produces:** JSON đúng cấu trúc spec §3.1 — `product_types` kèm `path` 3 cấp cha và `family_id`.

- [x] **B2.1** Service gom 13 danh mục trong **một** lần gọi, mỗi danh mục chỉ `select` cột cần.
- [x] **B2.2** `product_types` trả kèm đường dẫn cha bằng **một** query join 3 bảng (không N+1).
- [x] **B2.3** Áp quy tắc **danh mục bị khoá vẫn hiện nếu bản ghi đang dùng**: nhận `include_ids`.
- [x] **B2.4** Kiểm bằng curl: đếm số key trả về = 13, và `product_types[0].path` có đủ 3 cấp.
- [x] **B2.5** Kiểm quyền: token **không** có `Xem hàng hoá` ⇒ **403**.
- [x] **B2.6** Commit

### Task B3: `GET /` (danh sách) + `GET /{id}` (chi tiết)

**Files:**
- Create: `hrm-api/Modules/MasterData/Http/Controllers/V1/Product/ProductController.php`
- Create: `hrm-api/Modules/MasterData/Services/Product/ProductService.php`
- Create: `hrm-api/Modules/MasterData/Transformers/Product/ProductListResource.php`
- Create: `hrm-api/Modules/MasterData/Transformers/Product/ProductDetailResource.php`

- [x] **B3.1** `index()`: phân trang, lọc theo 10 ô của mockup, `with()` eager load, **không** `SELECT *`.
- [x] **B3.2** Lọc theo cây: `product_type_id` trực tiếp; lọc theo 3 cấp cha thì join lên.
- [x] **B3.3** `show()`: trả đúng cấu trúc spec §3.2 (mọi tab).
- [x] **B3.4** 🔴 **Gate giá vốn**: `cost_price` / `buy_price` trả `null` khi **không** có quyền
      `Quản lý giá` — kiểm ở **BE**, không dựa FE ẩn.

```php
$canPrice = isCurrentEmployeeHasPermission('Quản lý giá');
'cost_price' => $canPrice ? $unit->cost_price : null,
```

- [x] **B3.5** Trả cả giá **đang chờ duyệt**: `wait_approve` + cờ, theo `khao-sat-don-vi-tinh-gia-ban.md` §4.
- [x] **B3.6** Kiểm: gọi `/{id}` bằng 2 token (có / không quyền `Quản lý giá`) → so `cost_price`.
- [x] **B3.7** Commit

---

## Đợt C — BE ghi (phần rủi ro nhất)

### Task C1: Sinh mã hàng hoá

**Files:**
- Create: `hrm-api/Modules/MasterData/Services/Product/ProductCodeGenerator.php`

**Produces:** `ProductCodeGenerator::generate(Product $product): string`

- [x] **C1.1** Port **nguyên văn** `Product::generateCode()` của ERP (`app/Product.php:2207`):
      `slug(mã hãng SX) . '-' . slug(tên barcode ?: tên model)`, cắt **32 ký tự**, chống trùng bằng
      hậu tố `:01`, `:02` (cắt prefix để tổng ≤ 32).

- [x] **C1.2** Test: sinh mã cho hàng hoá có hãng `CH` + model `RRI32` ⇒ ra `CH-RRI32`.
- [x] **C1.3** Test va chạm: tạo sẵn `CH-RRI32`, sinh lại ⇒ phải ra `CH-RRI32:01`.
- [ ] **C1.4** *(dời sang Task C2 — xem nhật ký)*  ~~ Bắt `QueryException` mã **23000** ở tầng Service, sinh lại mã, **thử tối đa 5 lần**.~~
- [x] **C1.5** Commit

### Task C2: `POST /` — tạo hàng hoá

**Files:**
- Create: `hrm-api/Modules/MasterData/Http/Requests/Product/ProductRequest.php`
- Modify: `hrm-api/Modules/MasterData/Services/Product/ProductService.php`

- [ ] **C2.1** FormRequest theo spec §4. **Chỉ `rules()`**, không `messages()`.
      Bắt buộc: `name` · `product_type_id` · `units` ≥ 1 có **đúng một** `is_base`.
- [ ] **C2.2** Ghi trong **một** transaction: `products` → `product_units` → `product_unit_prices`
      (6 loại giá) → `attribute_products` → `product_suppliers` → tài liệu/ảnh/video → 4 bảng kèm →
      `product_company_coefficients`.
- [ ] **C2.3** Tự gán `created_by` = `updated_by` = `auth()->id()`.
- [ ] **C2.4** 🔴 **BB-2**: toàn bộ khối giá chỉ chạy khi có quyền `Quản lý giá` — không có thì
      **không đụng** gì tới giá.
- [ ] **C2.5** Test qua API: tạo 1 hàng hoá, rồi đối chiếu DB đủ 6 bảng con, `code` đúng khuôn.
- [ ] **C2.6** Xoá bản ghi thử, kiểm số dòng 12 bảng về đúng ban đầu.
- [ ] **C2.7** Commit

### Task C3: `PUT /{id}` — sửa, và 🔴 luồng duyệt giá

**Files:** Modify `ProductService.php`

- [ ] **C3.1** 🔴 **BB-1** — port **nguyên văn** điều kiện của ERP (`ProductsController:1374-1388`):

```php
$company = Company::find($product->company_id ?? auth()->user()->info->company_id);
$isApprove = $company->is_new_company
    && ($company->is_new_brand
        || in_array($request->manufacture_id, explode(',', $company->new_brand_ids ?: '')));
```

- [ ] **C3.2** Nhánh `isApprove = true`: **KHÔNG** ghi `cost_price`/`price` mà ghi
      `*_wait_approve` + `flag_* = 1`, rồi dựng bản ghi phiếu duyệt giá (như `$approves[]` của ERP).
- [ ] **C3.3** Nhánh `false`: ghi thẳng như cũ.
- [ ] **C3.4** Test **cả 2 nhánh** trên dữ liệu thật:
      - Sửa giá hàng hoá thuộc công ty **#8** (`is_new_company = true`) ⇒ `cost_price` **KHÔNG đổi**,
        `flag_price_wait_approve = 1`.
      - Sửa giá hàng hoá công ty khác ⇒ giá đổi ngay.
      - Token **không** có `Quản lý giá` ⇒ giá **giữ nguyên** ở cả 2 ca.
- [ ] **C3.5** Mở màn **Duyệt giá hàng hoá** của ERP ⇒ thấy phiếu vừa tạo.
- [ ] **C3.6** Commit

### Task C3c: Tab "Phân loại xe" — luồng GHI  🔴

**Files:** Modify `ProductService.php` · `ProductRequest.php`

**Consumes:** `Productable` (đã có) · `Product::vehicleManufactLinks/…` (đã có)

- [ ] **C3c.1** Validate: `vehicle_manufact_ids` / `vehicle_brand_ids` / `vehicle_model_ids` đều
      `nullable|array`, phần tử `exists:` bảng tương ứng. **KHÔNG `required_if`** — user chốt bỏ
      bắt buộc (khác ERP).

- [ ] **C3c.2** 🔴 Ghi bằng cách **xoá + chèn theo TỪNG `productable_type`**, KHÔNG `sync()`:

```php
foreach ([
    Productable::TYPE_VEHICLE_MANUFACT => $request->input('vehicle_manufact_ids', []),
    Productable::TYPE_VEHICLE_BRAND    => $request->input('vehicle_brand_ids', []),
    Productable::TYPE_VEHICLE_MODEL    => $request->input('vehicle_model_ids', []),
] as $type => $ids) {
    Productable::where('product_id', $product->id)
        ->where('productable_type', $type)   // ⚠️ THIẾU DÒNG NÀY LÀ XOÁ SẠCH 5 LOẠI
        ->delete();
    // rồi chèn lại $ids
}
```

- [ ] **C3c.3** 🔴 **Test bất biến**: trước khi lưu, đếm `productables` của hàng hoá đó theo
      `productable_type` cho 2 loại HRM KHÔNG quản (`App\Model\Product\Group`, `App\Product`);
      lưu xong đếm lại — **phải bằng đúng số cũ**. Đây là ca chặn lỗi xoá nhầm 32.366 dòng mà popup
      tìm phụ kiện của ERP đang đọc.
- [ ] **C3c.4** Test: hàng hoá #7599 (47 hãng xe) — bỏ chọn còn 2, lưu, đọc lại ra đúng 2; 0 dòng
      của 2 loại kia bị đụng.
- [ ] **C3c.5** Test đường TẠO MỚI riêng (memory `laravel-getchanges-rong-o-duong-insert`).
- [ ] **C3c.6** Commit

### Task C3b: 2 endpoint còn thiếu — `attributes-by-family` + `bulk-delete`

**Files:** Modify `ProductController.php` · `ProductService.php` · `ProductOptionService.php`

**Consumes:** bảng `product_type_attributes` (có sẵn từ Phase 0) · Entity `Product` (Task B1)
**Produces:** `GET /attributes-by-type/{productTypeId}` (dùng bởi D2.3) · `POST /bulk-delete` (dùng bởi D1)

- [ ] **C3b.1** `GET /attributes-by-type/{productTypeId}` — trả thuộc tính của **Loại sản phẩm**
      (bảng nối `product_type_attributes` có sẵn từ Phase 0):

```php
public function attributesByType(int $productTypeId)
{
    $type = ProductType::with('attributes:id,name')->findOrFail($productTypeId);

    return response()->json([
        'data' => $type->attributes->map(fn ($a) => [
            'attribute_id' => $a->id,
            'name'         => $a->name,
            'value'        => '',
            'unittech_id'  => null,
            'require'      => false,
            'need_print'   => false,
        ]),
    ]);
}
```

- [ ] **C3b.2** Test: gọi với `productTypeId` có 3 thuộc tính ⇒ trả đúng 3 phần tử, đủ 6 khoá mỗi phần tử.
- [ ] **C3b.3** `POST /bulk-delete` — nhận `ids[]`, **bỏ qua** (không xoá) bản ghi đang khoá, trả về
      số đã xoá và danh sách id bị bỏ qua kèm lý do:

```php
'deleted' => 3, 'skipped' => [['id' => 12, 'reason' => 'Bản ghi đang khoá']]
```

- [ ] **C3b.4** Test: gửi 3 id trong đó 1 id đang khoá ⇒ `deleted = 2`, `skipped` có 1 phần tử.
- [ ] **C3b.5** ⏸️ Ghi lịch sử — **tách sang việc xử lý sau** (xem Task C4).
- [ ] **C3b.6** Commit

### Task C4: Khoá / mở khoá / xoá / sao chép

> ⏸️ **LỊCH SỬ HÀNG HOÁ TÁCH RA, XỬ LÝ SAU** (user chốt 21/09/2026):
> *"Lịch sử hàng hoá bị thay đổi ở nhiều luồng chứ không đơn giản như các danh mục HRM."*
>
> Đúng vậy — đo được **319.303 dòng** `product_histories` do **8 file** ghi (26 chỗ `ProductHistory::`),
> và nó bị đổi từ nhiều luồng ngoài màn hàng hoá: duyệt giá · **luồng Tính giá** · duyệt hàng tạm.
> Khác hẳn danh mục HRM (một màn, một đường ghi). ⇒ Phase 2 **KHÔNG làm lịch sử**; brainstorm riêng.
>
> **Hệ quả phải chấp nhận trong lúc chờ:** sửa hàng hoá từ HRM **không để lại vết** ở đâu cả —
> không ghi `product_histories`, cũng chưa ghi `catalog_histories`. Cần user biết rõ điều này.

**Files:** Modify `ProductService.php` · `ProductController.php`

- [ ] **C4.1** `lock` / `unlock`: đổi `status`, **tự gán `updated_by` = `auth()->id()`**
      — đây là chỗ hay quên nhất vì `Product` của ERP không `extends BaseModel`.
- [ ] **C4.2** `delete`: bản ghi **đang khoá thì chặn** → trả **423 LOCKED**.
      ⚠️ Guard đặt ở **middleware route**, KHÔNG đặt trong thân hàm — controller nhận `FormRequest`
      nên Laravel validate trước, guard trong thân hàm sẽ không bao giờ tới lượt.
- [ ] **C4.3** `copy`: nhân bản hàng hoá + toàn bộ bảng con, **sinh mã mới** qua
      `ProductCodeGenerator` (Task C1).
- [ ] **C4.4** Test trên dữ liệu thật:
      - khoá 1 hàng hoá → `status` đổi **và** `updated_by` = id người thao tác
      - xoá bản ghi đang khoá → **423**
      - sao chép → bản mới có mã khác, đủ số dòng bảng con như bản gốc
- [ ] **C4.5** Dọn bản ghi thử, kiểm số dòng 12 bảng về đúng ban đầu.
- [ ] **C4.6** Commit

---

## Đợt D — FE

> Mockup `hrm-client/pages/master-data/mockup-hang-hoa/` **chính là bản thiết kế đã duyệt** — 2 file
> Vue chạy được bằng component thật. Các task dưới là **chuyển mockup thành màn thật + nối API**,
> không vẽ lại từ đầu.

### Task D1: Màn danh sách

**Files:**
- Create: `hrm-client/pages/master-data/products/index.vue` (từ `mockup-hang-hoa/index.vue`)

- [ ] **D1.1** Copy mockup, đổi `layout: 'default-sidebar'`, thêm mixin
      `PageTitleMixin` · `filterStateMixin` · `columnCustomizationMixin` · `exportFieldsMixin` · `CatalogImportMixin`.
- [ ] **D1.2** Nối API `GET /master-data/products` + `/form-options` cho ô lọc.
- [ ] **D1.3** 🐞 **Sửa mã mẫu**: mockup đang vẽ `TP.0012345`, mã thật dạng `CH-RRI32`.
- [ ] **D1.4** Gắn quyền: `canManage = hasAPermission('Quản lý hàng hoá')` — khởi tạo `false`.
      ⚠️ Chuỗi quyền phải **khớp seeder từng ký tự** (Phase 1 từng lệch 1 chữ ⇒ mất sạch nút).
- [ ] **D1.5** Thêm mục menu vào `components/subsystem-menu/master-data.js`, nhóm `Danh mục hàng hóa`.
- [ ] **D1.6** Kiểm Playwright: 12 cột đúng tên · **nội dung ô đã render** (`.thumb`, `.v2-cell-link`,
      `.sub-line`, badge) · ô Hành động có nút · dòng đang khoá **không có** nút Xoá.
- [ ] **D1.7** Commit

### Task D2: Form — tab 1 (Thông tin chung)

**Files:**
- Create: `hrm-client/pages/master-data/products/add.vue` · `_id/edit.vue` (chung một component form)

- [ ] **D2.1** Copy tab 1 từ mockup: Phân loại · Thông tin hàng hoá · Nguồn gốc · Thông số cơ bản ·
      **Đơn vị tính** · Tài liệu/Ảnh/Video.
- [ ] **D2.2** Cây đi **ngược**: chọn *Loại sản phẩm* → điền 3 ô khoá từ `classification_path`.
- [ ] **D2.3** Đổi *Loại sản phẩm* → gọi `GET /attributes-by-type/{id}` đổ khối **Thông số cơ bản**.
- [ ] **D2.4** ⚠️ **Ảnh đại diện là bắt buộc** (`avatar`, 97 % hàng hoá đang có; ERP khai `required`).
- [ ] **D2.5** Dùng `unsavedChangesMixin`, gọi `markFormSaved()` sau khi lưu.
- [ ] **D2.6** Kiểm Playwright: mọi `.form-row` đủ 12 cột; đổi Loại sản phẩm thì 3 ô cha đổi theo.
- [ ] **D2.7** Commit

### Task D3: Form — tab 2 (Thông số kỹ thuật) + tab 3 (Mua hàng)

- [ ] **D3.1** Copy 2 tab từ mockup, giữ nguyên **cột khác nhau của 4 bảng hàng hoá kèm**
      (*Vật tư sửa chữa* **không có** ĐVT/Số lượng).
- [ ] **D3.2** "Đặc điểm" giữ **CKEditor 5**; "Phụ kiện tiêu chuẩn" theo chốt của user (câu treo).
- [ ] **D3.3** Popup chọn hàng hoá dùng lại component có sẵn của hrm-client (rà trước khi tự viết).
- [ ] **D3.4** Kiểm Playwright + commit

### Task D5: FE tab 6 "Phân loại xe"

**Files:** Modify `hrm-client/pages/master-data/products/_id/edit.vue` (+ `add.vue`)

- [ ] **D5.1** Tab thứ 6, **không `v-if` theo Tính chất hàng hoá** — hiện với mọi loại.
- [ ] **D5.2** 3 `V2BaseSelect` + `:extraSettings="{ multiple: true }"`, lưới `col-md-4` × 3
      (đủ 12 cột — đã đo trên mockup: 3 × 412px = 1.236px so với hàng 1.235px).
- [ ] **D5.3** Gọi `GET /products/vehicle-options` **khi mở tab**, không gọi ở `mounted`
      (gộp vào form-options là +147 KB mỗi lần mở form).
- [ ] **D5.4** Lọc dây chuyền tại chỗ: đổi Hãng xe ⇒ Loại xe / Model xe lọc theo
      `vehicle_manufact_id`; đổi Loại xe ⇒ Model xe lọc theo `vehicle_brand_id`. Không bắn request.
- [ ] **D5.5** Bỏ id đã chọn khi nó không còn thuộc cấp cha mới — nhưng **giữ** nếu bản ghi đang
      dùng (quy tắc danh mục khoá vẫn hiện).
- [ ] **D5.6** Kiểm Playwright, đo từ DOM: 6 tab · 3 select2 · **0 phần tử bắt buộc** · chip chọn
      nhiều hiển thị · tổng bề rộng 3 ô = bề rộng hàng · footer không đè.
- [ ] **D5.7** Commit

### Task D4: Form — tab 4 (Dữ liệu quản trị) + tab 5 (Giá bán)

- [ ] **D4.1** Copy 2 tab, giữ **tab lồng theo Công ty**; tab Giá bán lồng thêm tầng **Đơn vị tính**.
- [ ] **D4.2** 🔴 Ô giá **ẩn hoàn toàn** khi không có quyền `Quản lý giá` (ẩn, không disable).
- [ ] **D4.3** Hiển thị **giá đang chờ duyệt** khi cờ bật, kèm nhãn cho người dùng biết.
- [ ] **D4.4** Loại giá **#6 (online)** khoá không cho sửa (giống ERP).
- [ ] **D4.5** Kiểm Playwright — ⚠️ trang có **tab lồng**: lấy con trực tiếp của `.tab-content` cấp 1,
      **không** dùng `querySelector('.tab-pane.active')`.
- [ ] **D4.6** Commit

---

## Đợt E — Làm ERP không lỗi (BẮT BUỘC trước khi bật màn HRM)

> Chi tiết + 8 bước kiểm: `sua-erp-de-khong-loi.md`

### Task E1: `SearchController` — popup của 338 màn

**Files:** Modify `ERP/TanPhatDev/app/Http/Controllers/Common/SearchController.php`

- [ ] **E1.1** 11 chỗ `->group->` → khuôn null-safe của chính ERP:
      `$p->group_id ? $p->group->name : 'Chưa xác định'` (copy từ `Product2Controller@searchData`).
- [ ] **E1.2** Cột **số** phải có mặc định: `floatval(optional($p->group)->vat_percent ?? 0)`.
- [ ] **E1.3** ⏳ Bỏ 4 điều kiện `where('product_type','!=','service_product')` +
      3 chỗ `whereIn(['accessories','lubricant'])` — **chỉ làm sau khi khách xác nhận** (nới lỏng
      hành vi: 30 hàng dịch vụ lọt vào popup; báo giá dịch vụ chọn được 45.890 thay vì 12.426).
- [ ] **E1.4** Kiểm: tạo 1 hàng hoá `group_id = NULL`, mở popup ở 1 màn bất kỳ ⇒ **không nổ**,
      tìm thấy, cột Nhóm hiện "Chưa xác định".
- [ ] **E1.5** Commit

### Task E2: `Product.php` + 9 file còn lại

- [ ] **E2.1** `Product.php`: thêm `product_type_id`, `product_characteristic_id` vào `$fillable`;
      thêm quan hệ `product_type_ref()` · `product_characteristic()`
      (⚠️ **không** đặt tên `product_type()`).
- [ ] **E2.2** `Product.php`: 3 accessor gom null-safe — `getGroupNameAttribute`,
      `getGroupVatPercentAttribute`, `getRateLiquidationValueAttribute`.
- [ ] **E2.3** Sửa 7 chỗ trong `Product.php` sang dùng accessor.
- [ ] **E2.4** `optional()` cho: `DeviceErrorController` (8) · `TmpProductsController` (3) ·
      `LiquidationQuotation` (2) · `CostFixingQuotation` (2) · `ProductSettingMailJob` (1) ·
      `MyTmpProductsController` (1) · `ExportLargeProductList` (1) · `BaseProduct` (1).
- [ ] **E2.5** Rà `ProductsController` (14 chỗ): hàm **chỉ đọc** nào còn được gọi từ ngoài
      (`searchData`, `getData`, `getDataForPriceAsking`, `barcode`…) thì cũng null-safe.
- [ ] **E2.6** Tự kiểm — lệnh này phải **rỗng** trên các file đã sửa:

```bash
grep -rn '\->group->' app/Product.php app/Http/Controllers/Common/SearchController.php \
  app/Http/Controllers/Sale/DeviceErrorController.php | grep -v optional
```

- [ ] **E2.7** Chạy 6 kịch bản còn lại ở `sua-erp-de-khong-loi.md` §5 (lỗi thiết bị · báo giá thanh
      lý · job nền · lệnh xuất · duyệt hàng tạm).
- [ ] **E2.8** Commit

---

## Đợt F — Nhập/Xuất Excel + nghiệm thu

### Task F1: Import + Export

- [ ] **F1.1** `ExportColumnRegistry`: thêm mục `products` với bộ cột của màn danh sách.
- [ ] **F1.2** Xuất Excel: nếu > 2s thì dùng `GET /export-rows` theo trang (2.000 dòng/lượt,
      trần 5.000) + dựng file ở FE bằng `utils/export/listExportFile.js`.
- [ ] **F1.3** Ô số trong Excel phải là **SỐ THẬT** + `numFmt`, không đổ chuỗi đã format.
- [ ] **F1.4** Import: validate trước khi ghi, báo lỗi theo dòng.
- [ ] **F1.5** Commit

### Task F2: Nghiệm thu "ERP không vỡ" — 14 bước

- [ ] **F2.1** Chạy đủ 14 bước ở `hop-dong-tuong-thich-erp.md` §3, ghi kết quả từng bước.
- [ ] **F2.2** Chụp số dòng 12 bảng trước/sau, khẳng định chỉ tăng đúng số bản ghi vừa tạo.
- [ ] **F2.3** `SELECT COUNT(*) FROM products WHERE code IS NULL OR code = ''` ⇒ **0**.
- [ ] **F2.4** `GROUP BY code HAVING COUNT(*) > 1` ⇒ **0**.
- [ ] **F2.5** Cập nhật `design.md` + `STATUS.md`, báo user nghiệm thu.

---

## Việc KHÔNG nằm trong plan này

Đã note ở `design.md` §7 và `phan-tich-song-song-erp-hrm.md` — brainstorm riêng sau khi xong Phase 2:

1. Quy đổi **45.890 hàng hoá** sang cây phân loại mới
2. Thay các chỗ lọc ERP sang danh mục mới (10 chỗ cơ học + 12 nhánh cứng + 176 view)
3. **3 cờ nghiệp vụ** thay `product_type` (hàng hoá làm dịch vụ · báo giá dịch vụ · thiết bị của KH)
4. Xoá hẳn `product_cate` · gỡ `group_id` (~116 chỗ đọc thuộc tính nghiệp vụ của nhóm)
5. Bỏ đồng bộ CRM nhánh hàng hoá (13+ model) — ⚠️ giữ nhánh nhân sự
6. **Phase 7** — luồng Tính giá · Phase 3 — dữ liệu theo công ty · Phase 6 — hàng tạm
7. 🆕 **LỊCH SỬ HÀNG HOÁ — cả cơ chế** (user chốt 21/09): tách khỏi Phase 2 vì lịch sử bị đổi ở
   **nhiều luồng** (màn hàng hoá · duyệt giá · luồng Tính giá · duyệt hàng tạm), không như danh mục
   HRM chỉ một đường ghi. Số liệu nền: `product_histories` **319.303 dòng**, ERP ghi ở **8 file /
   26 chỗ**; `product_versions` **113.768 dòng** (đã chốt bỏ). Kèm câu: màn "Lịch sử chỉnh sửa hàng
   hóa" bên ERP xử lý thế nào, và cách log **bảng con** (ĐVT · giá × 6 loại · thuộc tính · 4 bảng
   hàng hoá kèm)
8. `Product2Controller` (bỏ qua giai đoạn này)

### Checkpoint — 21/09/2026 (xong Đợt A phần CSDL: A0 · A1 · A2)

**Nhánh:** `feat/p1-danh-muc-hang-hoa` (user chốt làm tiếp trên nhánh này, không mở nhánh mới).

| Commit | Repo | Nội dung |
|---|---|---|
| `c59fc9036` | api | thêm `product_type_id` + `product_characteristic_id` vào `products` |
| `259ad55cb` | api | gỡ `can_retail` khỏi Loại sản phẩm — 11 chỗ + migration drop cột |
| `ca4b89f35` | client | gỡ `can_retail` khỏi màn Loại sản phẩm — 10 chỗ |

**Đo sau A1:** 2 cột `bigint unsigned NULL`, 2 index tạo đúng, **45.890 dòng nguyên vẹn**,
**không** có FK nào bị khai nhầm (`--pretend` trước khi chạy: đúng 3 câu, chỉ đụng bảng `products`).

**Đo sau A2 (Playwright):** popup Loại sản phẩm không còn chữ "bán lẻ" · **6/6 hàng đủ 12 cột** và
các ô cùng hàng cùng `top` · bảng danh sách 17 cột, không còn cột "Có thể bán lẻ" · bộ lọc sạch ·
ô **Thuộc tính GIỮ NGUYÊN** ở màn này.

**2 chỗ vấp khi làm, ghi để lần sau nhanh hơn:**
1. Repo dùng **migration có tên class** (`class XxxTable extends Migration`), không phải anonymous
   class kiểu Laravel 8 — bám theo Phase 0.
2. Script sửa file vấp 2 lần vì đoán sai markup: nhãn là `<V2BaseLabel> Serial <Required…` (có
   khoảng trắng), không phải `<V2BaseLabel>Serial`. **Luôn `grep` lấy chuỗi thật trước khi thay.**

**Đang làm dở:** (không)
**Bước tiếp theo:** Task A3 — 4 quyền id 1612-1615 + khai route `products`.
**Blocked:** (không)

### Checkpoint — 21/09/2026 (xong ĐỢT A: A0 · A1 · A2 · A3)

| Commit | Repo | Nội dung |
|---|---|---|
| `c59fc9036` | api | 2 cột phân loại vào `products` |
| `259ad55cb` | api | gỡ `can_retail` (BE) |
| `ca4b89f35` | client | gỡ `can_retail` (FE) |
| `6d5fa8663` | api | 4 quyền **1616-1619** + 15 route `products` |

**🔴 Hai cái bẫy bắt được ở Task A3 — cả hai đều thuộc loại hỏng im lặng:**

**1. Tên quyền đụng ERP vì DB BỎ DẤU.** Định đặt `Xem hàng hoá` / `Xoá hàng hoá`. Cột
`permissions.name` dùng collation `utf8mb4_unicode_ci`, đã đo:
`SELECT ("hàng hoá" = "hàng hóa")` → **1**. ERP có sẵn `Xem hàng hóa` (#100033) và `Xóa hàng hóa`
(#100036) ở guard `web`. Về kỹ thuật spatie vẫn phân biệt nhờ `guard_name` và PHP so chuỗi có phân
biệt dấu — nhưng màn phân quyền sẽ hiện 2 dòng chỉ khác dấu, và query nào quên lọc guard sẽ vớ nhầm
bản ERP. ⇒ user chốt thêm chữ **"danh mục"**, cũng khớp khuôn 11 danh mục Phase 1.

**2. Id 1612-1614 đã bị nhánh khác chiếm.** Seeder trên nhánh này dừng ở 1611 nên 1612-1615 trông
như còn trống. Nhưng DB dùng chung **đã có** 1612-1614 cho nhóm *"Báo cáo kế hoạch & kết quả làm
việc"* (tạo **21/09/2026**), trong khi seeder trên `gop_db` mới tới **1589** — tức nhánh thứ ba.
File seeder là file **phẳng** nên git không báo xung đột. ⇒ dời sang **1616-1619**, xoá bản ghi
#1615 đã lỡ insert (đã kiểm `role_has_permissions` không trỏ tới nó).

📌 **Bài học đo:** `grep "'id' =>"` trên seeder ra 17 id "trùng" — nhưng tất cả đều ở **dòng đã
comment**. Phải lọc `grep -E "^\s*Permission::create"` trước. Và **id lớn nhất trong seeder KHÔNG
bằng id lớn nhất trong DB** — luôn kiểm cả hai.

⚠️ Còn một vấn đề CÓ SẴN, không do Phase 2: **113 quyền trùng TÊN trong DB**, và bảng `permissions`
**không có unique index trên `name`** (chỉ PRIMARY). Đây đúng kiểu gate chết im lặng đã gặp ở
Phase 1 — role gán bản ghi này, code hỏi bản ghi kia. Nên báo cho team.

**Kiểm route:** gọi `/products` và `/products/form-options` đều trả **500 "Target class not found"**
(không phải 404) ⇒ route khớp đúng, `/form-options` không bị `/{product}` nuốt.

**Đang làm dở:** (không)
**Bước tiếp theo:** Đợt B — Task B1 (Entity `Product` + quan hệ).
**Blocked:** (không)

---

### Checkpoint — 21/09/2026, cuối ngày

**Vừa hoàn thành:** Đợt A (32 bước) + **trọn Đợt B** (B1·B2·B3) + tab "Phân loại xe" BE & mockup.
**48/122 bước.** 7 commit:

| Commit | Repo | Nội dung |
|---|---|---|
| `c59fc9036` | api | 2 cột phân loại trên `products` |
| `259ad55cb` | api | gỡ `can_retail` (BE) |
| `ca4b89f35` | client | gỡ `can_retail` (FE) |
| `6d5fa8663` | api | 4 quyền 1616–1619 + 15 route |
| `799b117bb` | api | **B1** — Entity `Product` + 13 model bảng con |
| `4f9184743` | api | **B2** — `GET /form-options`, 14 danh mục / 1 lần gọi |
| `cbcb359a8` | api | **B3** — danh sách + chi tiết, gate giá vốn |
| `cf5c489a9` | api | tab "Phân loại xe" — BE (route thứ 17) |
| `3b1f98798` | client | tab "Phân loại xe" — mockup |

**Số đo chốt lại (để lần sau không phải đo lại):**
- Danh sách: 5 query cho cả 20 lẫn 100 dòng · chi tiết 22–27 query bất kể số dòng con.
- `/form-options`: 13 query / 163 ms / 179,2 KB cho 14 danh mục.
- `/vehicle-options`: 151,3 KB, tách riêng vì gộp vào sẽ đẩy form lên 326,8 KB.
- Index `products_updated_at_id_index`: sắp xếp mặc định 119 ms → 0 ms (rows 42.391 → 20).

**4 bẫy đã ghi vào docblock, đừng "sửa cho đẹp":**
1. KHÔNG `SoftDeletes` cho `products` — 175 hàng hoá `status=1` vẫn còn `deleted_at`.
2. Gate giá phải đọc CHÉO GUARD — `Quản lý giá` chỉ có ở guard `web`.
3. KHÔNG `morphedByMany()` cho `productables` — cột lưu nguyên văn class ERP.
4. `tax_rates` không lọc theo `is_sales_tax` / `is_purchases_tax` — 0/40 dòng bật cờ.

**Đang làm dở:** không có việc nào dở giữa chừng; mọi thứ đã commit.

**Bước tiếp theo:** trả lời 3 câu ở `design.md` §15d, rồi:
- nếu chốt xong → làm **Task C1** (`ProductCodeGenerator`) và chèn các task danh mục xe / Nhóm máy
  vào Đợt C–D;
- Task **C3c** (ghi `productables`) và **D5** (FE tab 6) đã viết sẵn trong plan này.

**Blocked:** 3 câu ở §15d — (1) "Nhóm máy" đụng quyết định bỏ `groups`; (2) phạm vi danh mục xe;
(3) cách hiển thị "Đời xe". Thêm 1 câu cần xác nhận: 2 checkbox trên Tính chất hàng hoá đảo lại
quyết định "tab hiện với mọi Tính chất" — cần user xác nhận cách hiểu.

**Đính chính đã sửa vào tài liệu:** trước đó tôi ghi *"Đời xe bỏ hẳn vì bảng `vehicle_lifes` không
tồn tại"* — SAI, tra nhầm tên số nhiều. Bảng thật là `vehicle_life` (61 dòng) và bảng nối
`product_vehicle_model_has_life` có **48.736 dòng / 91 hàng hoá**. Đã sửa `design.md` §15 và ghi chú
trong mockup.

---

## Nhật ký — 22/09/2026, Task C1 (sinh mã hàng hoá)

`Modules/MasterData/Services/Product/ProductCodeGenerator.php` + 7 ca PHPUnit
(`ProductCodeGeneratorTest`), **7/7 xanh**.

**Kiểm bằng cách dựng lại mã của toàn bộ hàng hoá đang có** rồi so với mã thật đang lưu:

| | |
|---|---:|
| Đối chiếu | **45.890** hàng hoá |
| Khớp | **45.659 (99,50%)** |
| Lệch | 231 |
| ↳ mã sinh TRƯỚC khi hàng hoá được gắn code đặt hàng | 57 |
| ↳ model / code đặt hàng bị **đổi tên sau** khi mã đã chốt | 174 |

231 chỗ lệch **không phải lỗi port**. Chứng minh: hàng hoá #4319 mang mã `COGI-0-1110950116`,
mà `barcodes` id 11 tên `0-11109501/16` → slug ra **đúng** chuỗi đó; hàng hoá này sau đó đổi sang
code đặt hàng khác. ERP không sinh lại mã khi sửa, nên mã đông cứng ở trạng thái lúc tạo.

### 🐞 Bẫy lớn nhất: `iconv //TRANSLIT` cho kết quả KHÁC NHAU theo máy chạy

Bản ERP bỏ dấu bằng `iconv('UTF-8', 'ASCII//TRANSLIT//IGNORE')`. Hàm này phụ thuộc thư viện C và
locale của **máy chạy**, nên cùng một tên cho ra hai mã khác nhau:

| Model `THANH ĐỒNG` | Kết quả |
|---|---|
| ERP production (Linux/glibc) | `THANHDONG` — mã đang lưu trong DB là `CH-THANHDONG:02` |
| Máy dev macOS này | `THANHDNG` — **nuốt luôn chữ `Ồ`** |

Mã hàng hoá là thứ người dùng đọc hằng ngày và **không bao giờ sinh lại khi sửa** — lệch một lần là
lệch vĩnh viễn, không có gì báo ra. Nên bản HRM thay `iconv` bằng **bảng bỏ dấu cố định**
(`BANG_BO_DAU`), cho ra đúng kết quả ERP đang chạy mà không phụ thuộc máy. Ký tự ngoài tiếng Việt
vẫn nhờ `iconv` như cũ.

Đây là chỗ **cố ý lệch khỏi "port nguyên văn"**: giữ nguyên ĐẦU RA của ERP, bỏ sự phụ thuộc môi
trường. Sau khi đổi, số lệch giảm 232 → 231 (đúng dòng `THANH ĐỒNG`).

### 2 điểm khác nữa so với bản ERP, đều cố ý

1. **Không tự `save()`** — ERP gán `$this->code` rồi lưu ngay trong hàm sinh mã nên không gọi được
   ở bước dựng dữ liệu. Bản HRM trả về chuỗi, để `POST /products` ghi trong một transaction.
2. **Có trần vòng lặp** (`MAX_SUFFIX = 99`) — ERP dùng `while` không trần, gặp sự cố là treo tới
   hết timeout. Thực tế đã thấy hậu tố tới `:18`.
3. Thiếu hãng SX + model + code đặt hàng thì **ném lỗi rõ ràng** thay vì ghi mã rác kiểu `-`
   (ERP fatal "property of non-object").

### C1.4 dời sang Task C2

Bắt `QueryException` mã 23000 rồi sinh lại mã là việc của **tầng Service lúc GHI**, mà `store()`
chưa có (Task C2). Để ở C1 thì không có đường nào gọi tới. Đã ghi vào C2.

### Bẫy nhỏ khi viết test

`products` có **10 khoá ngoại**; `brand_id` / `group_id` / `origin_id` / `company_id` mặc định `0`
mà `0` không tồn tại ở bảng cha → insert trần nổ 1452. Test mượn giá trị của một hàng hoá đang có
thay vì hằng số hoá id. Thứ tự dọn rác cũng phải đi từ con lên cha
(`barcodes.manufacture_id` → `manufactures`).

**Dữ liệu sau khi chạy:** `products` 45.890 · `manufactures` 1.071 · `product_models` 39.796 ·
`barcodes` 8.664 — y hệt trước, **0 bản ghi rác**.

## 22/09/2026 — Thực thi §18 (tách giá) + §18b (2 cờ khai báo)

**Gỡ tab "Giá bán" khỏi mockup** — form còn **5 tab**, đo từ DOM: Thông tin chung · Thông số kỹ
thuật · Mua hàng · Dữ liệu quản trị · Phân loại xe. Gỡ luôn dữ liệu mẫu chết (`loaiGia`, 2 cột
`giaVon`/`giaMuaNgoai` trên card ĐVT). Kiểm: trang không còn chuỗi "Giá bán" / "Giá vốn" /
"Giá mua ngoài" nào, 0 lỗi trang.

**`ProductRequest` gỡ khối giá** — 4 rule ERP để `required` (`cost_price` ·
`sale_max_percent_coefficient` · `prices` · `prices.*.coefficient`) đã bỏ khỏi form hàng hoá.
⇒ **hết mâu thuẫn BB-2**, không phải chọn 3 phương án đã nêu lượt trước.

**2 cờ khai báo trên Loại sản phẩm** (§18b):

- migration `2026_09_24_000001` thêm `declare_vehicle` + `declare_machine_group` vào
  `product_types` (bảng MỚI của Phase 0, 0 dòng — không đụng bảng ERP).
- Nối đủ 6 điểm: Entity (`$fillable` + `$casts`) · Service (`fillableFrom` + `catalogColumns` +
  `catalogDisplay`) · Request · Resource (2 cờ + 2 chuỗi `*_text`) · `CatalogHistoryService::TABLES`
  · `ExportColumnRegistry`.
- FE: 2 ô tick ở modal (1 hàng đủ 12 cột) + 2 cột ở bảng + 2 trường xuất Excel + ánh xạ khoá cột.

**Kiểm chứng vòng đời thật qua API** (dựng tạm chuỗi cây Nhóm chức năng → Nhóm sản phẩm → Loại sản
phẩm rồi xoá sạch):

| Bước | Kết quả |
|---|---|
| Tạo với `declare_vehicle=1`, `declare_machine_group=0` | `true` / `false`, text `'Có'` / `''` |
| Sửa đảo ngược 2 cờ | `false` / `true`, text `''` / `'Có'` |
| Lịch sử | ghi đúng nhãn tiếng Việt: `{"Khai báo Phân loại xe":"Có"}` → `{...:null,"Khai báo Nhóm máy":"Có"}` |
| Dọn | `product_types` / `product_families` / `product_function_groups` về **0 / 0 / 0** |

FE đo từ DOM: bảng hiện đủ 2 cột mới; popup Tạo mới có đúng 2 ô tick, bấm nhãn tick được cả hai.

**🐞 Sót từ đợt trước, sửa luôn:** `can_retail` đã gỡ khỏi bảng ở migration `2026_09_22_000002`
nhưng vẫn còn nằm trong `ExportColumnRegistry` (popup "Chọn trường xuất file" vẫn mời tick rồi ra
cột rỗng) và trong `CatalogHistoryService::TABLES`. Đã gỡ cả hai; kiểm `catalog_histories` không có
dòng log nào từng ghi trường này nên không cần `HIDDEN_FIELDS`.

**Test:** `ProductClassificationCatalogTest` **11/11**, `ProductCodeGeneratorTest` **9/9**.

---

### Checkpoint — 22/09/2026 cuối ngày

**Vừa hoàn thành:** Task C1 (sinh mã hàng hoá) + hàng rào "mã sinh một lần" · 2 danh mục Xe bổ
sung (Dòng xe, Tải trọng xe) · mockup dọn lại theo 4 yêu cầu mới của khách · spec §17→§25.

**Đang làm dở:** không có file nào dang dở. Hai repo sạch, nhánh `feat/p1-danh-muc-hang-hoa`
(api +29 commit, client +28 commit chưa merge về `gop_db`).

**Bước tiếp theo:** chốt 1 câu ở §25d rồi viết migration gộp §19 + §24.

**Blocked:** 3 câu — xem mục "Đang chờ user chốt" dưới.

#### Đã làm hôm nay

| Việc | Kết quả |
|---|---|
| **Task C1** sinh mã hàng hoá | `ProductCodeGenerator` + 9 ca PHPUnit. Dựng lại mã cho cả **45.890** hàng hoá: khớp **45.659 (99,50%)**; 231 chỗ lệch chứng minh được là dữ liệu đổi sau khi mã chốt |
| Hàng rào **mã sinh một lần** | hook `updating` ở model `Product` ném lỗi nếu `code` bị đổi (user chốt §16) |
| **2 danh mục Xe** bổ sung | Dòng xe 11 · Tải trọng xe 31. Nhóm menu "Xe" 4 → 6 mục. e2e chung lên **119 ca (17 màn × 7)** |
| **Mockup** | gỡ tab Giá bán · gỡ card xe TRÙNG · thêm tab Nhóm máy 2 tầng · bỏ tab lồng theo Công ty ở Dữ liệu quản trị · sửa 9 nút icon rỗng |
| **2 cờ khai báo** trên Loại sản phẩm | migration + 6 điểm đăng ký + FE. Kiểm vòng đời thật qua API, dọn sạch |

#### 🐞 Lỗi bắt được hôm nay

1. **`iconv //TRANSLIT` cho kết quả khác nhau theo MÁY CHẠY** — model `THANH ĐỒNG` ra `THANHDONG`
   trên Linux (đúng mã đang lưu) nhưng `THANHDNG` trên macOS. Mã hàng hoá không sinh lại khi sửa
   nên lệch một lần là lệch vĩnh viễn. Đã thay bằng bảng bỏ dấu cố định.
2. **9 nút icon của mockup render ra ô vuông TRỐNG** — `V2BaseIconButton` không có prop `icon` lẫn
   `variant`; icon phải qua slot, tông đỏ dùng `danger`. Vue 2 im lặng với prop lạ.
3. **Card "Phụ tùng ô tô" trùng ở 2 tab** — di tích chưa dọn khi tách tab Phân loại xe.
4. **`can_retail` còn sót** ở `ExportColumnRegistry` + `CatalogHistoryService` sau khi cột đã gỡ —
   popup chọn trường xuất vẫn mời tick rồi ra cột rỗng.
5. **Ô ĐVT dòng 2 trống** ở mockup vì `dvtOptions` chỉ khai "Cái".

#### ⚠️ 3 lần tôi kết luận sai, đã đính chính

| Kết luận sai | Thực tế |
|---|---|
| "Ảnh Playwright nằm ngoài phạm vi truy cập" | Ảnh nằm ngay trong workspace; lệnh `find -newermt "-10 minutes"` của tôi sai cú pháp nên trả rỗng |
| "Mockup đã đạt chuẩn, không còn gì sửa" | Do không mở ảnh ra xem. Mở ra là thấy ngay 9 nút rỗng |
| Số file ERP bị ảnh hưởng: 42 / 86 / 44 | Grep thô đếm cả bảng khác trùng tên cột. Số thật: **29** (`min_stock_qty`) · **42** (`guarantee_type`) · **34** (chuỗi giá) |

#### Quyết định mới của khách hôm nay (§17 → §25)

| § | Nội dung |
|---|---|
| 17 | **Bám ERP đang chạy, không bám mockup**; lệch thì báo user quyết |
| 18a | **Giá tách khỏi form hàng hoá** → màn riêng, mở **Phase 8** |
| 18b | 2 cờ khai báo đặt ở **Loại sản phẩm** (cấp lá), không phải Tính chất hàng hoá |
| 19 | **Mỗi công ty một bảng giá độc lập** |
| 20 | Phase 2 thu hẹp còn phần THÔNG TIN hàng hoá |
| 21 | **Giữ bảng `groups`** với vai trò Nhóm máy — Phase 5 chỉ gỡ MÀN |
| 22 | **Chốt spec + mockup TRƯỚC, không động source dự án** |
| 23 | Tab Dữ liệu quản trị **bỏ tab lồng theo Công ty** |
| 24 | Update CSDL: chuyển sang bảng theo công ty, **xoá cột chung**; `company_id` NOT NULL, không chặn trùng |
| 25 | Phân tích lại §19 |

#### 🔴 Đang chờ user chốt

1. **§25d — câu quyết định của cả đợt migration:** *"bảng giá độc lập theo công ty"* có gồm
   **giá vốn / giá mua ngoài** không, hay chỉ 6 loại giá bán?
   → Có = tách tầng giá khỏi `product_units` (thêm bảng `product_company_units`, sửa 34 file ERP).
   → Không = chỉ thêm `company_id` vào `product_unit_prices`.
2. **§24f — hai hướng đang ngược nhau:** §19 (giá) đang theo hướng A *(nullable, giữ giá trị
   chung, ERP 0 file phải sửa)*, §24 (dữ liệu quản trị) đã chốt hướng B *(NOT NULL, xoá cột chung,
   71 file phải rà)*. Cần một hướng duy nhất.
3. **§23a câu 1–2 đã có đáp án** (chỉ thấy công ty mình · cấm tuyệt đối sửa chéo) — nhưng chưa làm
   được chừng nào chưa chốt 2 câu trên.

#### 📌 Việc đã lỡ làm vào source thật trước khi có §22

Đã báo user, **chờ quyết định giữ hay gỡ**: 2 cờ trên màn Loại sản phẩm · 2 màn Dòng xe/Tải trọng
xe · 6 màn danh mục Xe · Task C1. Tất cả đều đã chạy thật và e2e xanh.

---

## ĐỢT MOCKUP LOGIC XÂY DỰNG HÀNG HOÁ (§26 — mở 23/09/2026)

User đưa "Logic xây dựng hàng hoá" 3 bước + chia sẻ hàng hoá giữa công ty (nguyên văn ở
`yeu-cau-khach.md`, phân tích ở `design.md` §26). Chốt cách làm: **dựng mockup HTML nhẹ trước**,
chưa khảo sát 8 tồn ở §26g, xong mockup mới quay lại giải quyết từng cái.

- [x] M0 — Lưu nguyên văn yêu cầu vào `yeu-cau-khach.md`
- [x] M0b — Viết `design.md` §26 (bộ trạng thái · 3 màn · chia sẻ công ty · phạm vi CSDL · 8 tồn)
- [x] M0c — Cập nhật `SO-CHOT-VA-TON.md` (§3.1 có đáp án · 8 tồn mới · bảng phase)
- [x] M1 — Mockup HTML màn **Hàng hoá đang nhập thông tin**
- [x] M2 — Mockup HTML popup **Xem hàng hoá Công ty khác**
- [x] M3 — Mockup HTML màn **Hàng hoá chờ tính giá**
- [x] M4 — Mockup HTML màn **Danh mục hàng hoá kinh doanh**
- [x] M4b — Mockup màn **Sơ đồ luồng** + màn **Tạo/sửa hàng hoá 6 tab** + màn **Tính giá bán**
       (user chốt 23/09: demo đủ các bước như khi vận hành thật)
- [x] M5 — Kiểm bằng Playwright (đo DOM) — xem kết quả đo dưới
- [x] M6 — Viết lại mockup theo token ĐO THẬT từ app (vòng 2)
- [x] M7 — Vòng 3: rail thu gọn + rà style theo `sale-theme` + bộ lọc đầy đủ
- [x] M8 — Vòng 4-11: tab Giá bán (6 loại giá, tab con theo ĐVT) · 3 mức quyền sửa · 2 tab
       Xe/Nhóm máy theo ERP · bộ cột + cấu hình cột · select có ô tìm · dọn menu trái
- [x] M9 — **User duyệt mockup** ← đang chờ
- [x] M10 — **CỔNG CHẶN:** trả lời **đủ 14 câu tồn** (6 câu ở `SO-CHOT-VA-TON.md` mục 3 +
       8 câu ở `design.md` §26g) — user chốt 23/09: *"trước khi code hãy yêu cầu tôi trả lời đủ
       hết các vướng mắc còn tồn"*. Chưa trả lời hết thì **không mở code**
- [x] M11 — Ghi đáp án vào `design.md` + sổ chốt, rồi mới viết migration / BE / FE

### Checkpoint — 23/09/2026 (mockup xong, chờ duyệt)

**Vừa hoàn thành:** `mockup-luong-xay-dung-hang-hoa.html` — **1 file, 76 KB, 0 tài nguyên ngoài**
(nháy đúp là chạy, không cần server/mạng). 6 màn trong 1 file: Sơ đồ luồng · Đang nhập thông tin ·
popup Xem hàng hoá Công ty khác · Form 6 tab · Chờ tính giá · Tính giá bán · Danh mục kinh doanh.
Bấm được hết luồng: Lưu nháp / Lưu → Lưu tạm / Lưu & duyệt giá → hàng hoá chạy qua 4 trạng thái.
Ảnh chụp: `anh-mockup/`.

**Đang làm dở:** không có.
**Bước tiếp theo:** user xem mockup, duyệt hoặc nêu sửa; sau đó quay lại 8 tồn ở `design.md` §26g.
**Blocked:** không.

#### 📐 Số đo lấy từ DOM (Playwright, không phải nhìn ảnh)

| Phép đo | Kết quả |
|---|---|
| Trạng thái theo công ty | TPE **2/2/3** · Power **1/2/2** · Sài Gòn **0/2/3** — đổi ô Công ty là 3 màn đổi theo |
| Badge sidebar khớp số dòng bảng | 2 = 2 ✓ |
| Popup "Công ty khác" | 5 mã, **100%** là hàng công ty khác tạo **và** công ty mình chưa dùng |
| Chạy hết luồng 1 mã | chọn về → `nhap` → Lưu → `cho` → Lưu tạm → `dang` → Duyệt → `kd`; badge 3 màn cộng lại luôn khớp |
| Màu 4 trạng thái | đúng 4 mã chuẩn `#64748B` · `#D97706` · `#2563EB` · `#16A34A` |
| Khoảng cách nút cùng cụm | **12px** (toolbar + footer) |
| Icon rỗng trên màn đang hiện | **0/21** |
| Cuộn ngang thừa | không có (body lẫn khung nội dung) |
| Form | 6 tab / 6 pane, luôn chỉ **1** pane hiện |

#### 🐞 3 lỗi bố cục tự bắt được (test kiểu "đọc code thấy ổn" không thấy)

1. **Nút toolbar cách nhau 24px** thay vì 12px — `gap` của `.page-head` cộng dồn với `margin-right`
   của nút. Chỉ lộ khi đo `getBoundingClientRect()`.
2. **Cụm 3 nút Hành động xuống 2 dòng** làm dòng bảng cao 70px thay vì 49px — phải mở ảnh ra xem
   mới thấy, số liệu bảng vẫn đúng.
3. **Thanh nút form treo lơ lửng cách đáy 40px** — `padding-bottom` của khung cuộn đẩy phần tử
   `position: sticky; bottom: 0` lên. Đo `main.bottom - footer.bottom` = 40 → sửa còn **0**.

### Checkpoint — 23/09/2026 (mở đợt mockup §26)

**Vừa hoàn thành:** lưu nguyên văn yêu cầu mới + phân tích §26 + cập nhật sổ chốt.
**Đang làm dở:** chưa dựng mockup nào.
**Bước tiếp theo:** chốt phạm vi mockup với user rồi dựng file HTML.
**Blocked:** không (8 tồn §26g đã được user cho phép gác lại).


### Checkpoint — 23/09/2026 (vòng 2: sửa style theo app thật)

**Vì sao có vòng 2:** user phản hồi *"còn nhiều lỗi và sai style"*. Bản vòng 1 em bám khung navy của
`theo-doi-thuc-hien-hop-dong/mockup.html` rồi TỰ VIẾT CSS — lệch hẳn app thật.

**Cách sửa:** mở đúng 2 màn Nuxt đang chạy (`/master-data/mockup-hang-hoa` và `.../form`) bằng
Playwright, **bóc `getComputedStyle` của từng thành phần**, rồi viết lại toàn bộ HTML theo số đo đó.
Bảng token nằm ngay đầu file mockup.

#### 5 chỗ sai style đã sửa

| Chỗ | Vòng 1 (sai) | App thật |
|---|---|---|
| Nút chính | xanh dương `#2E71C3` | **teal `#1abc9c`** |
| Cột Hành động | 3 icon rời trên một dòng | **menu ⋮** (`V2BaseRowActions`) |
| Badge trạng thái | nền tự chế | **`rgba(màu,.1)` + viền `rgba(màu,.2)`**, bo 999px |
| Đầu bảng | nền xám, chữ tối | **chữ `#0a7c88`, gạch dưới 2px `#20d9ea`**, viền lưới `#e5e7eb` |
| Khung màn | tự chế card/topbar | **`.tp-card`** + topbar 60px + sidebar 220px đúng gradient |

Kèm: font `Roboto` 12.8px (không phải system font), ô nhập 32px viền `#e2e8f0` bo 5px, tab form
`#2b5098`, tiêu đề card `#0a99a7`, phân trang bootstrap, dòng bảng 2 tầng (mã + barcode,
loại sản phẩm + đường dẫn cây).

#### 📐 Đối chiếu token sau khi sửa — khớp 100%

`body` font/size/nền · sidebar 220px · topbar 60px · `.tp-card` (nền/viền/bo/padding/bóng) ·
tiêu đề lọc `#0a99a7` 12px 900 · tiêu đề danh sách `#0a99a7` 15px 500 · nút primary
`rgb(26,188,156)` cao 32 bo 8 · secondary `#333`/viền `#cbd5e1` · tertiary `#1f2937`/viền `#e2e8f0` ·
ô tìm nhanh 36px viền `#d1d5db` · `th` `#0a7c88` + `2px #20d9ea` · `td` 12px padding 6px 8px ·
link ô `#28539d` 400 · badge bo 999px 11px 600 · trang hiện tại nền `#1abc9c` · tab mở `#2b5098` ·
card-header `12px 10px` + tiêu đề 14px 700 · label 12px 600 `#0f172a` · input 32px bo 5px ·
ô khoá nền `#f1f5f9`.

#### 🐞 2 lỗi bố cục vòng 2 (ảnh mới thấy, số liệu vẫn "đủ")

1. **Menu ⋮ bị `.tbl-wrap` cắt mất mục cuối** — đếm `.ra-item` vẫn ra 3, nhưng "Xoá" không hiện.
   Sửa: menu chuyển `position: fixed`, JS tự đặt toạ độ theo nút và lật lên khi thiếu chỗ.
2. **Ô tìm nhanh lệch ~10px so với ô có nhãn** trong cùng hàng lọc (popup + màn Chờ tính giá) —
   `align-items:center` kéo ô không nhãn lên. Sửa bằng `.tp-head.align-end`; đo lại 3 phần tử
   cùng đáy: 166/166/166 và 216/216/216.

**Bước tiếp theo:** user xem lại mockup; xong thì quay về 8 tồn ở `design.md` §26g.


### Checkpoint — 23/09/2026 (vòng 3: rail thu gọn · sale-theme · bộ lọc)

User yêu cầu 3 việc: sidebar mặc định thu gọn (hover mở), rà lại style (bảng trong popup / nền tiêu
đề cột sai), bổ sung bộ lọc cho màn danh sách + popup — bám cái **đang dùng**.

#### 🔍 Phát hiện quan trọng: có `assets/scss/sale-theme.scss` — style CHỐT cho 14 phân hệ hub

Vòng 2 em đo `getComputedStyle` nhưng **không biết bộ token này tồn tại**, nên lấy nhầm nền trắng cho
đầu cột. Bảng chuẩn (mục 3 + 4 của file đó):

| Thành phần | Giá trị chuẩn |
|---|---|
| `thead th` | nền **`linear-gradient(180deg,#eafcfe,#d2f4f9)`** · chữ `#0a7c88` · 700 · dưới `2px #20d9ea` · trên `1px #e5e7eb` · bóng `0 2px 4px rgba(15,23,42,.08)` · sticky |
| dòng hover | **`#eefafb`** (`--sale-row-hover`) |
| tiêu đề khối | có **gạch teal `::before` 6×15px bo 3px `#0a99a7`** |
| bảng | `border-collapse: separate` (collapse làm mất viền dưới khi `th` sticky) |

⚠️ Bộ này áp cho **cả bảng trong popup** — popup dùng chung `.data-table`, không có style riêng.

#### 🧭 Sidebar rail

Mặc định **58px** (= `$leftbar-width-condensed`), hover mở **220px** (= `$leftbar-width`), chỉ hiện
icon khi thu gọn. Mở kiểu **đè lên nội dung**: đã chừa sẵn `.side-slot` 58px nên
`main` giữ nguyên trái 58 / rộng 1454 ở cả 2 trạng thái — không xô layout.
Ô tên phân hệ trên topbar co giãn theo rail (class `body.rail-mo` do JS gắn).

#### 🔎 Bộ lọc — bám màn + popup ĐANG DÙNG

| Nơi | Nguồn khảo sát | Số ô |
|---|---|---|
| 3 màn danh sách | `mockup-hang-hoa/index.vue` (10 ô) | **12** — bỏ ô *Trạng thái* ở màn chỉ có 1 trạng thái, thêm ô riêng của màn (Công ty tạo / Người nhập / Model / % VAT / Có giá bán) |
| Popup | `QuotationProductSearchModal.vue` (19 ô) | **16** — bỏ 5 ô thuộc nhóm danh mục Phase 5 đã chốt gỡ (Lĩnh vực · Chương · Nhóm công việc · Cụm công việc · Nhóm hàng hoá) + bỏ *Loại hàng hoá* (`product_cate` đóng băng, §3), thêm *Công ty quản lý hàng hoá* (§26d) |

Khuôn: panel **mặc định thu gọn**, nút đổi chữ *Tìm kiếm nâng cao* ↔ *Ẩn tìm kiếm nâng cao*;
lưới **4 ô/hàng** (`col-md-3`), ô cao **36px** bo 6px viền `#dcdfe6`, **nhãn nằm trong ô** (floating)
nên không khai placeholder trùng nhãn và **không dùng "Tất cả"** — đúng quy ước CLAUDE.md
*(popup thật đang dùng "Tất cả", đây là chỗ mockup cố ý làm khác spec cũ)*.

#### 📐 Đo lại sau khi sửa

rail 58 → hover 220 → rời chuột về 58 · `main` không dịch (58/1454 ở cả 2 trạng thái) ·
`th` đúng gradient + `#0a7c88` + `2px #20d9ea` + bóng · gạch tiêu đề 6×15 bo 3 `#0a99a7` ·
số ô lọc 12/12/12/16 · 4 ô mỗi hàng · ô lọc 36px bo 6px viền `#dcdfe6` ·
nhãn trong ô đổi từ xám `#8b95a5` sang `#0f172a` khi chọn · lọc thật chạy (chọn Power → còn 2 mã POW) ·
luồng 4 trạng thái vẫn đúng · **0 lỗi console**.

#### 🐞 3 lỗi bắt trong vòng này

1. **Rail mở làm nội dung trôi sang trái 58px** — do rail đang trong luồng flex rồi chuyển
   `position:absolute` lúc mở. Sửa bằng `.side-slot` chừa chỗ sẵn.
2. **Khai 2 thuộc tính `onchange` trên cùng thẻ `<select>`** — trình duyệt lấy cái đầu, cái sau mất
   im lặng (ô lọc của popup mất hàm đổi màu nhãn).
3. **`:hover` không kiểm được bằng sự kiện giả lập** — phải điều khiển bằng class `body.rail-mo`
   do JS gắn thì vừa chạy thật vừa đo được.

**Bước tiếp theo:** user duyệt mockup; xong quay về 8 tồn ở `design.md` §26g.

### Checkpoint — 23/09/2026 (vòng 4: thiết kế lại màn của người TÍNH GIÁ)

User: *"Hiện đủ các tab thông tin hàng hoá + thêm tab Giá bán. Mỗi đơn vị tính cần hiển thị đủ danh
sách bảng giá để tính chứ không để chế độ select từng loại giá."*

#### Cách làm: MỘT màn form dùng cho 2 vai, không dựng 2 màn song song

| | Vai **nhập thông tin** | Vai **tính giá bán** |
|---|---|---|
| Tab | 6 tab thông tin | 6 tab thông tin + **tab 7 "Giá bán"** (mở sẵn) |
| Ô nhập 6 tab đầu | sửa được | **khoá hết** (39/39 ô) + ẩn nút thao tác trong tab |
| Footer | Lưu nháp · Lưu · Quay lại | Lưu tạm · Lưu & duyệt giá bán · Quay lại |
| Menu trái sáng | Hàng hoá đang nhập thông tin | Hàng hoá chờ tính giá |

⚠️ **Điểm tự quyết cần user duyệt:** khoá 6 tab thông tin ở vai tính giá — vì quyền
"Tính giá bán hàng hoá" khác quyền "Nhập thông tin hàng hoá" (§26b/§26c). Nếu khách muốn người
tính giá sửa được thông tin thì bỏ khoá.

#### Tab "Giá bán" — bám khuôn ERP `products/form.blade.php:969-1160`

**Mỗi ĐƠN VỊ TÍNH một khối**, trong khối hiện **đủ 6 loại giá** (không select từng loại):

- Đầu khối: Giá vốn* · Giá mua ngoài · Hệ số tính định mức hàng thúc đẩy bán · Định mức đàm phán giá
  hàng thúc đẩy bán (%) · ô tick "Tính theo giá niêm yết".
- Bảng 6 dòng = **`price_types` thật của ERP** (`PriceTypeSeeder`), xếp theo cột `order`:
  **Bán lẻ · Giá bán theo lô · Đại lý cấp 1 · Đại lý cấp 2 · Đại lý cấp 3 ·
  Giá bán thương mại điện tử (online)**.
- Cột: Loại giá · Hệ số · Giá công thức · Giá bán · Định mức đàm phán giá (%) · Ngày hiệu lực ·
  nút **+ Giá hiệu lực** (chèn dòng giá áp dụng trong tương lai ngay dưới dòng đang áp dụng —
  đúng cơ chế `expected_prices` của ERP).
- Dòng **online (id 6) KHOÁ** — giữ đúng ERP (`ng-disabled="price_type_id == 6"`).
- Cuối tab: bảng **Hệ số giá theo công ty** (công ty khác tự khai hệ số của mình).

#### 📐 Đo sau khi sửa

vai tt: 6 tab · ô mở · footer Lưu nháp/Lưu — vai gia: **7 tab**, tab đang mở = "Giá bán",
**0/39 ô thông tin còn mở khoá**, nút trong tab đã ẩn, menu sáng đúng "Chờ tính giá" ·
**2 khối ĐVT** (Cái cơ bản + Bộ hệ số 2) · bảng đúng **6 cột** và **6 dòng loại giá** ·
dòng online khoá toàn bộ ô · giá công thức = giá vốn × hệ số (58.000.000 × 1,25 = **72.500.000** ✓) ·
bấm "+ Giá hiệu lực" chèn đúng 1 dòng (6 → 7) · Lưu tạm → *Đang tính giá*, Lưu & duyệt →
*Đang kinh doanh* + về màn danh mục kinh doanh · quay lại vai nhập thông tin thì tab Giá bán ẩn,
ô mở khoá lại · **0 lỗi console**.

**Bước tiếp theo:** user duyệt mockup; xong quay về 8 tồn ở `design.md` §26g.

### Checkpoint — 23/09/2026 (vòng 5: 3 mức quyền sửa)

User chốt thêm: *"Khi tính giá không được sửa thông tin hàng hoá. Công ty A lấy hàng hoá Công ty B
về ⇒ chỉ được nhập thông tin quản trị theo công ty ⇒ tính giá, không được sửa thông tin khác."*
→ ghi thành **design.md §26c-bis** + thêm dòng vào bảng "đã chốt" của `SO-CHOT-VA-TON.md`.

| Trường hợp | Sửa được | Mockup đo được |
|---|---|---|
| Công ty **tạo ra** hàng hoá | cả 6 tab | tab 1 **36/36** ô mở · tab Dữ liệu quản trị **6/6** · không có dải báo |
| Công ty **lấy hàng công ty khác về** | **chỉ tab Dữ liệu quản trị** | tab 1 **0/36** · tab Thông số **0/1** · tab Phân loại xe **0/4** · tab Dữ liệu quản trị **6/6** · form mở thẳng vào tab đó · nhãn 5 tab kia làm mờ · có dải báo |
| Vai **tính giá bán** | chỉ tab Giá bán | tab 1 **0/36** · tab Dữ liệu quản trị **0/6** · có dải báo |

Dải báo dùng chữ **xám** trên nền `#f5f8fc` (không tô đỏ — đỏ chỉ dành cho lỗi validate).

📌 Việc này trả lời **một nửa tồn 26g-6**: công ty đi mượn không sửa được lớp thông tin chung nên
không có chuyện "đổi bên này hỏng bên kia". Nửa còn lại (A sửa thì B có thấy đổi không) vẫn chờ
chốt cùng tồn 26g-5 (chép hay tham chiếu).

🔒 Nhắc khi code thật: đây mới là khoá ở FE. BE phải so `products.company_id` với công ty người
đăng nhập và **chỉ nhận phần dữ liệu quản trị + giá của công ty đó**, đúng tinh thần §23c.

### Checkpoint — 23/09/2026 (vòng 6: multiselect + rà 2 tab theo ERP)

#### 1. Ô chọn nhiều — trước đây dùng `<select multiple>` thô, sai hẳn khuôn

Đo select2 thật của app (`.select2-selection--multiple` + `__choice`) rồi dựng widget chip:

| | Giá trị chuẩn (đo thật) |
|---|---|
| ô | min-height **32px** · viền `#cbd5e1` · bo 5px · nền trắng |
| chip | nền **`#eff6ff`** · chữ **`#1e40af`** · viền **`#bfdbfe`** · bo 5px · **11px** · cao **22px** |

Áp cho **6 chỗ**: Nhà cung cấp · Hãng xe · Loại xe · Model xe · Đời xe (từng dòng bảng) · Nhóm máy.
Đo lại: `select[multiple]` thô còn sót = **0**.

#### 2. Tab "Phân loại xe" — thiếu hẳn bảng bộ ba, đã dựng lại theo ERP

ERP (`products/form.blade.php:424-596`) **không có ô Đời xe phẳng** (đã comment). Bổ sung:
3 ô chọn nhiều kèm **ô tick "Chọn tất cả"** cho từng ô · ô tick **"Áp dụng tất cả đời xe cho model"** ·
**bảng bộ ba** Hãng xe (gộp dòng) | Loại xe | Model xe | Đời xe (chọn nhiều riêng từng model + "Chọn tất cả").
→ Chốt luôn **tồn §3.3** (xem `design.md` §26d-bis).

Đo: chọn Toyota+Honda → Loại xe còn **3** lựa chọn đúng theo hãng · chọn "Xe con 5 chỗ" → Model còn
**Vios, Camry** · bảng đúng **4 cột**, gộp dòng **Toyota:2** · **mọi dòng đều có ô Đời xe riêng** ·
tick "Áp dụng tất cả đời xe" → mỗi model nhận đủ **3** đời.

#### 3. Tab "Nhóm máy" — thiếu luật ẩn/hiện, đã dựng lại theo ERP

ERP (`form.blade.php:353-421`): bảng **Máy** *chỉ hiện khi đã chọn ít nhất 1 nhóm máy*, nhãn **bắt
buộc**, rỗng thì hiện **"Không có máy"**, có nút thêm/xoá từng dòng.

Đo: chưa chọn nhóm → khối Máy **rỗng hoàn toàn** · chọn nhóm → hiện bảng, nhãn có dấu `*`, trạng thái
rỗng đúng chữ "Không có máy" · thêm 2 máy → 2 dòng, cột STT/Mã máy/Tên máy · bỏ nhóm → bảng ẩn và
máy thuộc nhóm đó bị loại.

#### 4. Khớp với 3 mức quyền của vòng 5

Ô chọn nhiều nằm ngoài luồng `disabled` thường nên có hàm đồng bộ riêng. Đo: vai tính giá → ô chọn
nhiều **khoá**, ô tick **khoá**; hàng đi mượn → tab Dữ liệu quản trị mở, **Nhà cung cấp dùng được**,
tab Phân loại xe **khoá**. Luồng 4 trạng thái vẫn chạy. **0 lỗi console.**

⚠️ **Điểm cần user duyệt:** bên ERP 2 khối này hiện theo `products.product_type`; ở HRM §18b đã
chuyển cờ sang **Loại sản phẩm (cấp lá)**. Mockup đang để **cả 2 tab luôn hiện** cho dễ duyệt —
bản thật phải gate theo cờ.

### Checkpoint — 23/09/2026 (vòng 7: tab Giá bán — mỗi ĐVT một tab)

User: *"Demo 2 đơn vị tính, mỗi đơn vị tính 1 tab."*

Đổi tab Giá bán từ **xếp chồng card theo ĐVT** sang **tab con theo ĐVT**, đúng khuôn ERP
(`products/form.blade.php:972` — `ul.nav-tabs.nav-quotation` lặp theo `product.units`):

- Thanh tab con: tên ĐVT, **đơn vị cơ bản in đậm**, ĐVT phụ có dấu **×** để xoá, cuối thanh có **+**
  để thêm đơn vị tính.
- Mỗi tab = thông số riêng của ĐVT đó (ĐVT · hệ số quy đổi · giá vốn · giá mua ngoài · hệ số định mức
  · định mức đàm phán · ô tick "Tính theo giá niêm yết") **+ bảng đủ 6 loại giá của riêng ĐVT đó**.
- `dvtCuaHang()` nay luôn trả **2 đơn vị tính** để demo thấy rõ (Cái ×1 + Bộ ×2; hàng tính bằng Bộ
  thì thêm Thùng ×3).

#### 🐞 Lỗi bắt được: tab cấp 1 nuốt trạng thái tab con

`doiTab()` quét `#sc-form .nav-link` — trúng **cả tab con** trong tab Giá bán, nên vừa mở màn tính giá
là tab ĐVT mất `.active`, không pane nào hiện. Sửa: đặt id `#tab-chinh` cho thanh tab cấp 1 và
thu hẹp mọi truy vấn về đó (cả chỗ làm mờ nhãn tab của `datVaiForm`).

#### 📐 Đo sau khi sửa

3 mục trên thanh tab con (`Cái` · `Bộ ×` · `+`) · ĐVT cơ bản có thẻ `<b>` · ĐVT phụ có nút `×` ·
**2 pane, luôn chỉ 1 pane hiện** · mỗi pane **6 dòng loại giá** riêng · giá vốn theo hệ số quy đổi
(58.000.000 và **116.000.000**) · giá công thức của ĐVT 2 = 116.000.000 × 1,25 = **145.000.000** ✓ ·
đổi tab con → đúng pane thứ 2, tab cấp 1 vẫn là "Giá bán" · rời sang tab khác rồi quay lại thì tab con
**giữ nguyên** tab đang mở · tab Phân loại xe / Nhóm máy / luồng 4 trạng thái vẫn chạy ·
**0 lỗi console**.

### Checkpoint — 23/09/2026 (vòng 8: bộ cột danh sách · màn ghi chú · gọn tab Giá bán)

4 yêu cầu của user trong một lượt:

| # | Yêu cầu | Đã làm |
|---|---|---|
| 1 | Tab Giá bán bỏ nút thêm/xoá ĐVT | thanh tab con còn đúng 2 mục `Cái` · `Bộ`, **0 nút ×, 0 nút +** — ĐVT kế thừa từ tab Thông tin chung |
| 2 | Tách note logic thành màn riêng | menu đổi thành **"Ghi chú & sơ đồ luồng"**, gom 5 khối: quy trình 3 bước · ma trận trạng thái theo công ty · chia sẻ giữa công ty · **bảng "Ai được sửa gì"** · **"Những chỗ mockup làm khác bản thật"**. Dải MOCKUP vàng chỉ còn ở màn này; các màn vận hành sạch |
| 3 | Màn danh mục đủ trường hơn | **14 cột mặc định** — đủ 11 trường khách chốt (kiểm bằng danh sách đối chiếu: **thiếu 0**) |
| 4 | Trường còn lại vào tuỳ chọn cột | popup **Cấu hình cột hiển thị**: **27 cột**, 14 tick sẵn, 2 cột khoá (STT · Hành động), có nút **Mặc định** |

Kèm yêu cầu nhắn giữa chừng: **Ảnh – Mã – Tên lên đầu** → thứ tự đã đúng (ngay sau STT), và làm
thêm cho 4 cột đó **dính trái khi cuộn ngang**.

#### 📐 Đo sau khi sửa

Cột mặc định: `STT · Ảnh · Mã hàng · Tên hàng hoá · Model · Tính chất hàng hoá · Nhóm chức năng ·
Nhóm sản phẩm · Loại sản phẩm · Thương hiệu · Hãng sản xuất · Trạng thái đồng bộ · Trạng thái ·
Hành động` · Trạng thái đồng bộ ra đúng 2 giá trị *Đã đồng bộ* / *Chưa đồng bộ* ·
bật thêm 2 cột → 16 cột, số ô mỗi dòng cũng 16 · bấm **Mặc định** → về 14 ·
bật hết 27 cột thì bảng tràn ngang, cuộn 500px: 4 cột dính **đứng yên** (71/111/158/274), cột thường
trôi theo · **0 cặp cột chồng lấn** · tab Giá bán không còn nút thêm/xoá · luồng 4 trạng thái vẫn
chạy · **0 lỗi console**.

#### 🐞 Lỗi bắt được: toạ độ cột dính tính theo bề rộng KHAI BÁO

Đặt `left` theo `width` khai trong đăng ký cột (44/96/246) trong khi bảng co giãn theo nội dung
(thật là 42/93/219) ⇒ cột "Tên hàng hoá" bị ghim lệch **27px** sang phải, **che mất cột Model**.
Ảnh chụp mới thấy, số liệu bảng vẫn đúng. Sửa: đo `getBoundingClientRect().width` **sau khi** dựng
bảng rồi mới gán `left`; kèm kéo `scrollLeft` về 0 mỗi lần vẽ lại.

#### ❓ Chờ user xác nhận (ghi ở `design.md` §26f)

1. *"nhóm hàng hóa"* / *"loại hàng hóa"* — mockup hiểu là **Nhóm sản phẩm** / **Loại sản phẩm**
   (2 cấp của cây Phase 0), vì `product_cate` đã đóng băng (§3) và `groups` đã thành Nhóm máy (§21).
2. **Trạng thái đồng bộ** là trường **MỚI**, chưa có trong 59 cột `products` — cần chốt đồng bộ với
   cái gì, lưu ở đâu, ai đặt cờ.
3. *"Ảnh chỉ hiển thị ở danh sách hàng hoá"* — hiện để ở cả 3 màn danh sách, không có trong popup
   chọn hàng hoá.

### Checkpoint — 23/09/2026 (vòng 9: chốt 3 câu bộ cột)

User trả lời 3 câu treo ở §26f:

| Câu | Chốt | Đã làm |
|---|---|---|
| *"nhóm hàng hóa" / "loại hàng hóa"* | đúng là **Nhóm sản phẩm** / **Loại sản phẩm** — user nhầm sang tên danh mục cũ | giữ nguyên, không đổi |
| **Trạng thái đồng bộ** | **BỎ HẲN** | gỡ khỏi đăng ký cột, khỏi dữ liệu demo, khỏi popup cấu hình |
| **Ảnh** | cho vào **cả popup chọn hàng hoá** | popup thêm cột Ảnh |

📐 Đo lại: cột mặc định còn **13** (`STT · Ảnh · Mã hàng · Tên hàng hoá · Model · Tính chất hàng hoá ·
Nhóm chức năng · Nhóm sản phẩm · Loại sản phẩm · Thương hiệu · Hãng sản xuất · Trạng thái · Hành động`),
**không còn cột đồng bộ** · popup cấu hình còn **26 cột / 13 tick sẵn**, không còn mục "Trạng thái
đồng bộ" · popup chọn hàng hoá lên **8 cột**, **mọi dòng đều có ô ảnh** · luồng 4 trạng thái vẫn chạy ·
**0 lỗi console** · toàn file `dongBo` = 0 tham chiếu.

### Checkpoint — 23/09/2026 (vòng 10: select có ô tìm · popup rộng · giá ở màn kinh doanh)

| # | Yêu cầu | Đã làm |
|---|---|---|
| 1 | Select danh mục **luôn có ô tìm** | widget `.ss` nâng cấp **tại chỗ** mọi `<select>` đơn: ô hiển thị giống `.v2-input`, bảng chọn có ô *"Gõ để tìm…"*, lọc theo chữ gõ, không khớp thì hiện *"Không tìm thấy"*. Giữ nguyên thẻ `<select>` làm nơi chứa giá trị nên mọi chỗ đang đọc `.value` / `disabled` không phải sửa |
| 2 | Popup: thêm cột như bảng danh sách · rộng hơn · **phóng to toàn màn hình** | popup dùng **chung đăng ký cột** với màn danh sách (12 cột), rộng **1.480px**, thêm nút **Cấu hình cột** và nút **Phóng to** (bấm lần nữa để thu nhỏ) |
| 3 | Màn kinh doanh: **bỏ giá vốn**, "Giá bán" → **"Giá bán lẻ"** | thêm cờ `khong:['l3','pp']` cho cột Giá vốn; đổi nhãn cột `ban` thành *Giá bán lẻ* (= loại giá "Bán lẻ" của bảng giá) |
| — | *(nhắn giữa chừng)* bỏ gạch đậm ở tiêu đề | **bỏ hẳn** ở cả `.tp-section-title::before` và `.tp-list-title::before` — tiêu đề chỉ còn icon + chữ. Đây là chỗ mockup **cố ý khác** `sale-theme`, đừng thấy lệch rồi thêm lại |

#### 📐 Đo sau khi sửa

**Select tìm kiếm:** form có **14 ô** đã nâng cấp, **0 select thô còn sót**; gõ *"cầu"* → còn đúng
1 lựa chọn, chọn xong nhãn + `select.value` khớp và bảng chọn tự đóng; gõ *"zzz"* → *"Không tìm thấy"*;
panel bộ lọc nâng cao dùng ô cao **36px** đúng khuôn; vai tính giá → **mọi ô đều khoá** (xám).

**Popup:** 12 cột giống màn danh sách (Ảnh · Mã hàng · Tên · Model · 4 cấp phân loại · Thương hiệu ·
Hãng SX · Công ty quản lý) · rộng **1.480 → 1.512px** khi phóng to (**= đúng bề rộng màn hình**,
cao 900px), bấm lại về **1.480px** · chọn hàng vẫn chạy.

**Màn kinh doanh:** popup cấu hình **không còn mục "Giá vốn"** (25 mục), cột giá hiện đúng tên
**"Giá bán lẻ"**; màn *Chờ tính giá* **vẫn có** Giá vốn.

**Gạch tiêu đề:** cả `.tp-section-title::before` lẫn `.tp-list-title::before` = `none` — kiểm ở màn danh sách, màn ghi chú và trong popup.

Luồng 4 trạng thái vẫn chạy · **0 lỗi console**.

⚠️ Ô "thêm" bên trong widget **chọn nhiều** (chip) chưa gắn ô tìm — nó vốn là danh sách ngắn đã lọc
sẵn theo cấp trên. Nếu khách muốn cả chỗ này cũng tìm được thì báo.

### Checkpoint — 23/09/2026 (vòng 11: dọn menu trái)

User: *"Sidebar menu bỏ hết các menu khác, giữ các menu demo."*
Menu trái còn đúng **4 mục**: `Ghi chú & sơ đồ luồng` · `Đang nhập thông tin` · `Chờ tính giá` ·
`Hàng hoá kinh doanh` (bỏ 9 mục của phân hệ: Yêu thích · Gần đây · Tổng quan · Khai Quy chế ·
Địa lý · Ngân hàng · Phân loại hàng hoá · Xe · Đối tác). Giữ ô "Tìm chức năng" vì nó là khung
của sidebar thật, không phải mục menu.

#### 🐞 Lỗi tự gây rồi tự bắt: thừa một thẻ đóng làm vỡ khung

Cắt khối sidebar theo mốc `</div>` đầu tiên sau chữ "Đối tác" → dính nhầm thẻ đóng của mục menu,
để lại **một `</div>` thừa** đóng sớm `.body`. Hậu quả: `.main` rơi ra ngoài khung flex, nội dung
**tụt xuống dưới** rail thay vì nằm cạnh. Số liệu menu vẫn đúng 4 mục — chỉ lộ khi mở ảnh ra xem.

#### 📐 Đo sau khi sửa

4 mục, **cả 4 đều có id và bấm ra đúng màn** (`nav-flow→sc-flow`, `nav-l1→sc-l1`, `nav-l2→sc-l2`,
`nav-l3→sc-l3`) · badge đếm vẫn chạy (2/2/3) · rail cao **bằng đúng khung** (840px) · `main` nằm
cạnh rail (trái 58, rộng 1454) · hover: rail **58 → 220 → 58**, `main` **không dịch** ·
**0 lỗi console**.

⚠️ Đo bề rộng rail ngay sau khi bắn sự kiện hover sẽ ra 58 vì có `transition .16s` — phải chờ
~300ms rồi mới đo, nếu không tưởng nhầm là hỏng.


---

## Checkpoint — 23/09/2026 (WRAP UP cuối ngày)

**Vừa hoàn thành:** mockup HTML `mockup-luong-xay-dung-hang-hoa.html` qua **11 vòng sửa theo góp ý
của user**, đã kiểm bằng Playwright ở từng vòng (đo DOM, không chỉ nhìn ảnh).

**Đang làm dở:** không có file nào dang dở. **Hai repo sạch**, nhánh `feat/p1-danh-muc-hang-hoa`,
**không đụng một dòng source nào** của dự án ở đợt này — đúng §22 (chốt spec + mockup trước).

**Bước tiếp theo:** user duyệt mockup. Duyệt xong thì quay lại **8 tồn `design.md` §26g** (nặng nhất
là tồn 5 *lấy hàng công ty khác = chép hay tham chiếu* và tồn 2 *trạng thái theo công ty lưu bảng
nào*) rồi mới mở phần code.

**Blocked:** không — 8 tồn đang được user cho phép gác lại tới sau khi duyệt mockup.

### Mockup chốt lại gồm gì

| Màn | Nội dung |
|---|---|
| Ghi chú & sơ đồ luồng | quy trình 3 bước · ma trận trạng thái theo công ty · chia sẻ giữa công ty · bảng "Ai được sửa gì" · "chỗ mockup khác bản thật" |
| Hàng hoá đang nhập thông tin | 13 cột + cấu hình cột 26 cột · lọc nâng cao 12 ô · nút Xem hàng hoá Công ty khác |
| Popup Xem hàng hoá Công ty khác | 12 cột như màn danh sách · 16 ô lọc · rộng 1.480px · **phóng to toàn màn hình** |
| Form hàng hoá | 6 tab thông tin (+ tab 7 Giá bán ở vai tính giá) · 3 mức quyền sửa |
| Tính giá bán | tab con **theo từng ĐVT**, mỗi ĐVT một **bảng đủ 6 loại giá** |
| Hàng hoá chờ tính giá / kinh doanh | cùng bộ cột; màn kinh doanh **bỏ giá vốn**, cột giá là **"Giá bán lẻ"** |

### Quyết định đã chốt trong đợt (đã ghi `design.md`)

§26 quy trình 3 bước theo công ty · §26c-bis 3 mức quyền sửa · §26d-bis bảng bộ ba xe
(chốt luôn tồn §3.3) · §26d-ter tab Nhóm máy · §26f bộ cột danh sách (bỏ *Trạng thái đồng bộ*,
ảnh có ở cả popup).

### 11 lỗi tự bắt được bằng Playwright trong đợt (test xanh / đọc code đều không thấy)

1. nút toolbar cách 24px thay vì 12px · 2. cụm nút Hành động xuống 2 dòng · 3. thanh nút form treo
lơ lửng cách đáy 40px · 4. menu ⋮ bị khung cuộn bảng cắt mất mục cuối · 5. ô tìm nhanh lệch 10px so
với ô có nhãn · 6. rail mở làm nội dung trôi 58px · 7. khai 2 `onchange` trên cùng thẻ select ·
8. `:hover` không kiểm được bằng sự kiện giả lập · 9. tab cấp 1 nuốt trạng thái tab con ·
10. toạ độ cột dính tính theo bề rộng khai báo → che mất cột Model · 11. thừa một `</div>` làm
nội dung tụt xuống dưới rail.

---

## ĐỢT MOCKUP — BÁO CÁO HÀNG HOÁ THEO CÔNG TY (mở 23/09/2026)

**Yêu cầu user:** xem đầy đủ thông tin hàng hoá · biết mỗi công ty đang dùng mã nào + trạng thái ·
mỗi mã đang có bao nhiêu công ty kinh doanh/sử dụng. Tham khảo mockup báo cáo mới nhất.

**4 quyết định đã chốt trước khi dựng (user trả lời 23/09):**

| # | Câu | Chốt |
|---|---|---|
| 1 | Bố cục | **Ma trận Hàng hoá × Công ty** — 8 công ty là 8 cột, ô = badge trạng thái |
| 2 | "Đang sử dụng" | **Có bản ghi trạng thái** ở công ty đó; đếm tách 2 số: *Đang khai thác* và *Đang kinh doanh* |
| 3 | Bộ cột | **Dùng lại bộ cột màn danh sách** (§26f) + popup Cấu hình cột |
| 4 | Kỳ thời gian | **Không có kỳ** — ảnh chụp hiện trạng |

⚠️ **Giả định phải ghi rõ trong mockup:** báo cáo chỉ đứng được nếu tồn **26g-5** chốt là **tham chiếu**
(một `products.id` dùng chung, công ty đắp thêm dòng trạng thái). Chốt là **chép mã mới** thì ma trận
sụp — mỗi công ty một mã riêng, không còn ô giao nhau.

### Task

- [x] M1 — Port khối token + component từ `bao-cao-ke-hoach-lam-viec-nhan-vien.html` (navy + teal):
      `.topbar*` · `.topbar-btn` · `.page-body` · `.calendar-filter-*` · `.ms*` · `.rsum-blk*` ·
      `.market-table*` · `.minutes-modal*` · `.mtg-badge--*`. KHÔNG tự chế token mới.
- [x] M2 — Dữ liệu demo: giữ nguyên bộ mã/tên của `mockup-luong-xay-dung-hang-hoa.html`, mở rộng
      **12 mã × 3 công ty → 29 mã × 8 công ty thật** (TPE · TPHP · TPV · TPSG · TPA · UPS · EGR · DTT).
      Rải đủ ca: mã 1 công ty · mã 6–7 công ty · mã tắc ở bước tính giá.
- [x] M3 — Thanh tiêu đề navy + ⓘ mục đích báo cáo + 2 nút *In báo cáo · Xuất Excel* dồn phải.
- [x] M4 — Dải tổng hợp 2 khối cùng hàng: *Quy mô danh mục* (Tổng mã · Tổng lượt dùng · Bình quân
      CT/mã · Mã ≥2 công ty) + *Lượt dùng theo trạng thái* (4 ô **cộng đúng bằng Tổng lượt dùng**).
- [x] M5 — Toolbar lọc 1 hàng: tìm nhanh · Công ty (chọn nhiều, **bỏ tick là ẩn cột**) · Trạng thái ·
      cây phân loại · Thương hiệu · Hãng SX · **Số công ty dùng** · Công ty quản lý · Xoá lọc · ⚙ cột.
- [x] M6 — Bảng ma trận: 4 cột định danh **dính trái**, kế đến **khối 8 cột công ty + 2 cột đếm**
      (đặt ngay sau tên để nhìn thấy ma trận không cần cuộn), rồi mới tới các cột thông tin.
- [x] M7 — Popup 1: bấm ô ma trận → *"<Mã> tại <Công ty>"* (trạng thái · ngày chuyển · người nhập ·
      dữ liệu quản trị riêng · bảng giá 6 loại).
- [x] M8 — Popup 2: bấm số ở cột đếm → danh sách công ty của mã đó.
- [x] M9 — Popup 3: Cấu hình cột (26 cột), 4 cột định danh + khối công ty khoá không cho tắt.
- [x] M10 — Sắp xếp: Mã hàng · Tên · 2 cột đếm.
- [x] M11 — Tự kiểm bằng **Playwright đo DOM**: toạ độ 4 cột dính khi cuộn ngang · 2 nút cách 12px ·
      số dải tổng hợp = số đếm thật từ bảng · 4 ô trạng thái cộng đúng tổng · footer không đè ·
      ma trận không tràn ở 1600×900 và 1366×768.
- [x] M13 — Lọc nhanh bằng chú giải trạng thái trên tiêu đề bảng + bỏ dải ghi chú giả định.
- [x] M12 — Ghi quyết định vào `design.md` (§27) + cập nhật `SO-CHOT-VA-TON.md`.

### Checkpoint — 23/09/2026 (mockup Báo cáo hàng hoá — dựng xong, tự kiểm xong)

**Vừa hoàn thành:** `mockup-bao-cao-hang-hoa.html` — 1 file 68 KB, 0 tài nguyên ngoài, nháy đúp là chạy.
Hai repo vẫn sạch, **không đụng dòng source nào** (đúng §22).

**Đang làm dở:** không có. **Bước tiếp theo:** user duyệt mockup báo cáo.

**Blocked:** không, nhưng xem cảnh báo phụ thuộc tồn 26g-5 ngay dưới.

#### Sản phẩm

| Phần | Chốt lại |
|---|---|
| Bảng | Ma trận 29 mã × 8 công ty · 4 cột định danh dính trái · khối 8 cột công ty + 2 cột đếm đặt ngay sau tên |
| Bộ cột | 24 cột trong Cấu hình cột (bộ §26f **trừ** *Trạng thái* — nay là 8 cột công ty — và *Hành động* — báo cáo chỉ để xem) |
| Dải tổng hợp | 2 khối: *Quy mô danh mục* (29 mã · 80 lượt dùng · 2.8 CT/mã · 20 mã ≥2 CT) + *Lượt dùng theo trạng thái* (15 · 14 · 7 · 44 = **đúng 80**) |
| Bộ lọc | 1 hàng gọn (tìm nhanh · Công ty · Trạng thái · Số công ty dùng) + **Bộ lọc nâng cao** 6 ô ẩn sẵn, có chip đếm |
| Popup | ô ma trận → chi tiết mã × công ty (5 khối, bảng 6 loại giá thật của `price_types`) · số ở cột đếm → danh sách công ty · Cấu hình cột |

#### 6 lỗi giao diện TỰ BẮT bằng Playwright (đọc code / nhìn ảnh đều không thấy)

1. **`table-layout:fixed` không khai tổng bề rộng ⇒ trình duyệt co cột**: khai 44/52/150/250px nhưng
   đo thật ra **41/51/132/114px**, làm `left` của 4 cột dính trái lệch hẳn và ô công ty chui xuống
   dưới khối dính. Vá: tính `tongW` rồi ghim `table.style.width`.
2. **Thanh lọc 155px / 2 hàng** trong khi khuôn mẫu 68px / 1 hàng — ăn mất 87px chiều cao bảng.
   Vá: gom 6 ô ít dùng vào *Bộ lọc nâng cao*, còn **79px / 1 hàng**.
3. **Trang cao 975px trong khung 900px ⇒ 2 thanh cuộn lồng nhau.** `max-height: calc(100vh - 340px)`
   ghim cứng là sai vì con số đó đổi theo việc mở/đóng bộ lọc nâng cao. Vá bằng `capNhatChieuCao()`
   đo tại chỗ + nghe `resize` (484px thu gọn → 428px khi mở bộ lọc).
4. **Nhãn nhóm "Thông tin hàng hoá" căn giữa ô colspan rộng 950px ⇒ chữ rơi ra ngoài khung nhìn**,
   hàng tiêu đề trông như trống. Vá: căn trái.
5. **Tiêu đề 2 cột đếm bị cắt** — "Đang khai thác" cần 123px trong ô 111px, nới 92→112px vẫn cắt.
   Vá: rút nhãn còn *Khai thác* / *Kinh doanh* (hàng nhóm ngay trên đã ghi "SỐ CÔNG TY").
6. **Placeholder ô tìm nhanh bị cắt** ("… moc") — chữ cần 278px, ô cho 202px. Nới ô lên 330px chứ
   không cắt chữ, vì placeholder phải nói đúng các trường được lọc.

#### Số đã đối chiếu (1600×900 và 1366×768, cả 2 đều xanh)

- Bề rộng thật 4 cột dính = **44/52/150/250px** đúng bằng bề rộng khai báo.
- Nhãn nhóm khớp mép khối cột bên dưới: trái **521 = 521**, phải **985 = 985**.
- **0 cột** của khối ma trận bị tràn khỏi khung khi chưa cuộn ngang, ở **cả 2 độ phân giải**.
- 4 phép cộng khớp nhau: **80 chấm trên ma trận = 80 "Tổng lượt dùng" = 80 tổng cột *Khai thác* =
  15+14+7+44 của 4 ô trạng thái**. Lọc bỏ 3 công ty + 1 trạng thái → cả 4 số cùng về **44**.
- Tiêu đề dính đúng 2 nấc khi cuộn dọc (`top` 0 và 26px), không đè nhau.
- **0 lỗi console**, trang không sinh cuộn dọc toàn cục.

#### ⚠️ Phụ thuộc phải chốt trước khi code

Báo cáo này chỉ đứng được nếu **tồn 26g-5** chốt là **THAM CHIẾU**. Chốt là *chép thành mã mới cho
từng công ty* thì ma trận sụp — không còn ô giao nhau. Cảnh báo đã in ngay đầu mockup.
Kéo theo **tồn 26g-2** (trạng thái theo công ty lưu bảng nào) là nguồn dữ liệu trực tiếp của màn này.

### Checkpoint — 23/09/2026 (báo cáo: lọc nhanh trên tiêu đề bảng + bỏ dải ghi chú)

**Vừa hoàn thành — 2 yêu cầu của user:**

1. **4 mục trạng thái ở chú giải đầu bảng bấm được để lọc nhanh**, kèm số lượt dùng từng trạng thái.
   Dùng **chung `stChon`** với ô lọc "Trạng thái" nên hai chỗ đồng bộ hai chiều, không sinh ra hai
   nguồn sự thật. Tắt hết 4 trạng thái → bảng báo đúng nguyên nhân thay vì "không có dữ liệu".
2. **Bỏ dải ghi chú giả định khỏi giao diện** (*"khách hàng không cần đọc"*). Nội dung giữ ở
   `design.md` §27f + khối chú thích trong nguồn mockup. Vùng bảng nhờ đó cao thêm **484 → 548px**.

**Vá kèm (tự thấy khi làm):** số đếm trong panel 2 ô chọn nhiều **đang rỗng** từ lượt trước — khai
`<span class="ms__opt__n">` nhưng chưa bao giờ đổ dữ liệu. Nay cả panel lẫn chú giải dùng chung
`demTheoTrangThai()` / `demTheoCongTy()`, theo luật **"số của một ô lọc thì bỏ qua chính ô đó"**.

**Đã đo (1600×900):**

| Phép kiểm | Kết quả |
|---|---|
| Bấm chip *Đang nhập thông tin* (15) | 80 → **65** chấm, nhãn ô lọc đổi thành "Đã chọn 3 trạng thái" |
| Bấm thêm *Chờ tính giá bán* (14) | 65 → **51**, nhãn đổi thành "Đang tính giá, Đang kinh doanh" |
| Bấm lại chip đầu | **66** — bật lại đúng phần đã trừ |
| Gõ tìm "Fusheng" | 4 số trạng thái → **3/3/0/7 = 13** = số chấm trên ma trận |
| Tắt công ty TPE | 4 số trạng thái → **9/11/6/35 = 61**; 8 số của ô Công ty **giữ nguyên** (đúng luật bỏ qua chính ô) |
| Tắt hết 4 trạng thái | bảng báo *"Chưa bật trạng thái nào…"*, ô lọc viền đỏ |
| Tổng 3 nguồn | Σ số theo công ty = Σ số theo trạng thái = số chấm ma trận = **80** |
| Bố cục | không sinh cuộn dọc toàn cục; đáy thẻ bảng 868px trong khung 900px |

### Checkpoint — 23/09/2026 (WRAP UP — mockup Báo cáo hàng hoá chốt lại)

**Vừa hoàn thành:** `mockup-bao-cao-hang-hoa.html` qua **3 vòng sửa theo góp ý user** sau bản dựng đầu:
lọc nhanh trên tiêu đề bảng · bỏ dải ghi chú giả định · đổi nhãn `CHỦ` → `QUẢN LÝ`.

**Đang làm dở:** không có file nào dang dở. **Hai repo sạch** (0 file thay đổi ở cả `hrm-api` lẫn
`hrm-client`), nhánh `feat/p1-danh-muc-hang-hoa`, **không đụng một dòng source nào** — đúng §22.

**Bước tiếp theo:** user duyệt mockup báo cáo. Duyệt xong thì vào **vòng chốt 14 tồn**
(6 câu `SO-CHOT-VA-TON.md` mục 3 + 8 câu `design.md` §26g) rồi mới mở code — cổng chặn §2b.

**Blocked:** không. Nhưng báo cáo này **phụ thuộc tồn 26g-5** (chép hay tham chiếu) và
**26g-2** (trạng thái theo công ty lưu bảng nào) — xem §27f.

#### Vòng sửa cuối (3 yêu cầu)

| # | Yêu cầu | Đã làm |
|---|---|---|
| 1 | *"cho phép click vào các trạng thái trên tiêu đề bảng để lọc nhanh"* | 4 mục chú giải thành nút bật/tắt kèm số lượt dùng, **dùng chung `stChon`** với ô lọc "Trạng thái" nên đồng bộ hai chiều |
| 2 | *"bỏ note phía trên báo cáo, khách hàng không cần đọc"* | Gỡ dải ghi chú giả định; nội dung chuyển vào §27f + khối chú thích trong nguồn. Vùng bảng cao thêm **484 → 548px** |
| 3 | *"thay Chủ → Quản lý"* | Đổi 3 chỗ: nhãn trong ma trận · dòng chú giải · cột *Vai trò* trong popup (chỗ thứ 3 là tự quyết cho đồng bộ, user có thể yêu cầu đổi về *Tạo ra mã*) |

**Vá kèm tự thấy:** số đếm trong panel 2 ô chọn nhiều **đang rỗng** từ vòng trước — khai
`<span class="ms__opt__n">` mà chưa bao giờ đổ dữ liệu. Nay panel + chú giải dùng chung
`demTheoTrangThai()` / `demTheoCongTy()`, theo luật **"số của một ô lọc thì bỏ qua chính ô đó"**.

#### Tổng kết tự kiểm bằng Playwright — 7 lỗi giao diện tự bắt được cả đợt

1. `table-layout:fixed` không khai tổng bề rộng ⇒ cột co (khai 150px ra thật 132px), toạ độ cột
   dính trái lệch, ô công ty chui xuống dưới khối dính.
2. Thanh lọc 155px / 2 hàng thay vì 68px / 1 hàng của khuôn mẫu.
3. Trang 975px trong khung 900px ⇒ 2 thanh cuộn lồng nhau; `max-height` ghim cứng là sai.
4. Nhãn nhóm căn giữa ô `colspan` rộng 950px ⇒ chữ rơi ra ngoài khung nhìn.
5. Tiêu đề 2 cột đếm bị cắt ("Đang khai …").
6. Placeholder ô tìm nhanh bị cắt ("… moc").
7. Số đếm trong panel ô chọn nhiều rỗng (khai thẻ nhưng không đổ dữ liệu).

#### Số chốt lại (1600×900 và 1366×768 đều xanh, 0 lỗi console)

- **80 chấm ma trận = 80 "Tổng lượt dùng" = 80 tổng cột *Khai thác* = 15+14+7+44 của 4 ô trạng thái
  = Σ 8 số của ô lọc Công ty.** Năm nguồn cùng một số.
- Lọc bỏ 3 công ty + 1 trạng thái → cả 4 số cùng về **44**; gõ "Fusheng" → **13**; tắt TPE → **61**.
- Bề rộng thật 4 cột dính = **44/52/150/250px** đúng bề rộng khai báo; nhãn nhóm khớp mép khối cột
  (trái 521=521, phải 985=985); **0 cột ma trận bị tràn** ở cả 2 độ phân giải.
- Nhãn `QUẢN LÝ` rộng 40px trong ô 57px, không tràn ở cả 29 dòng.

#### Xem mockup

Cổng cố định **8899** đang chạy (`python3 -m http.server`, PID ghi ở log `/tmp/mockup-hang-hoa-8899.log`):
`http://127.0.0.1:8899/mockup-bao-cao-hang-hoa.html` · `…/mockup-luong-xay-dung-hang-hoa.html`.
Sửa file xong phải **Cmd+Shift+R** vì cổng cố định có cache. Tắt bằng `kill <PID>`.

---

## ĐỢT MOCKUP — CẤU HÌNH GIÁ BÁN NỘI BỘ KHI CHIA SẺ HÀNG HOÁ (§28 — mở 24/09/2026)

**Yêu cầu user:** cấu hình cách tính giá bán cho các công ty chia sẻ — theo **hãng sản xuất** ⇒
**từng công ty mua**, % tách theo **hàng nhập khẩu** / **hàng tồn kho**.
8 đáp án chốt + công thức + cấu trúc bản ghi: `design.md` §28.

**Chốt cách dựng:** thêm **màn mới vào `mockup-luong-xay-dung-hang-hoa.html`** (không tạo file rời)
vì màn này chỉ có nghĩa khi đứng cạnh ô *"Đang làm việc tại"* — đổi công ty là thấy ngay
"công ty nào cũng có thể là chủ", đúng đáp án 5.

### Task

- [x] C1 — Thêm công ty **GREEN (Etek Green)** vào `CTY` để khớp ví dụ khách (TPE · POWER · TPSG · GREEN);
      không đụng `HH.st` — mã nào GREEN chưa dùng thì vẫn nằm ở popup "Công ty khác".
- [x] C2 — Dữ liệu demo `CH` (8 cấu hình / 3 công ty bán) + **nhúng 1.071 hãng THẬT** từ bảng
      `manufactures` (mã + tên + cờ khoá), trong đó Fusheng đang khoá để demo 🔒.
- [x] C3 — Mục menu trái **Cấu hình giá bán nội bộ** (nhóm Cấu hình, dưới divider) + màn `sc-cf`
      đăng ký vào `moMan()` / `veTatCa()`.
- [x] C4 — Card lọc: tìm nhanh (*mã hãng, tên hãng, công ty mua*) + Tìm kiếm / Làm mới, nâng cao
      3 ô: Hãng sản xuất · Công ty mua · Cách tính (chỉ liệt kê giá trị công ty hiện tại đang dùng).
- [x] C5 — Bảng danh sách 9 cột + menu ⋮ (Sửa · Lịch sử · Xoá) + phân trang, **chỉ hiện cấu hình
      của công ty đang làm việc**.
- [x] C6 — Popup khai: **ô Hãng = chip + popup chọn nhiều (1.071 hãng)** · Công ty mua (bỏ công ty
      mình, chặn trùng cặp ở cả popup chọn hãng lẫn lúc Lưu) · Cách tính · 2 ô % ·
      **khối Xem trước bằng số thật** (giá vốn ×(1+%) / 6 loại giá ×(1−%)).
- [x] C7 — Popup Lịch sử theo khuôn lịch sử danh mục + popup Xác nhận xoá theo `base-confirm-modal`.
- [x] C8 — Tự kiểm bằng **Playwright đo DOM** (bảng bên dưới).
- [x] C9 — Ghi quyết định vào `design.md` (§28 + §28d-bis) + task vào `plan.md`.

### Checkpoint — 24/09/2026 (mockup Cấu hình giá bán nội bộ — dựng xong, tự kiểm xong)

**Vừa hoàn thành:** màn **Cấu hình giá bán nội bộ** thêm vào `mockup-luong-xay-dung-hang-hoa.html`
(file 133 KB → **222 KB** vì nhúng 1.071 hãng thật). Hai repo **không đụng dòng source nào** — đúng §22.

**Đang làm dở:** không có. **Bước tiếp theo:** user duyệt mockup này; duyệt xong thì mockup tiếp
*nơi hiện số gợi ý* (§28e) rồi mới vào vòng chốt 14 tồn.

**Blocked:** không.

#### Đã đo bằng Playwright (1600×900 và 1366×768, console 0 lỗi)

| Phép kiểm | Kết quả |
|---|---|
| Đổi ô "Đang làm việc tại" | TPE **5** cấu hình · POWER **2** · GREEN **0** (hiện dòng trống đúng câu) — mỗi công ty một bộ |
| Hãng khoá | Fusheng hiện **🔒 Fusheng** ở cả bảng lẫn popup chọn hãng |
| Popup chọn hãng | **1.071 hãng**, mỗi lượt vẽ 80 dòng + dòng đếm "Đang hiện 80 / 1,071" |
| Chặn trùng tại popup | MULLER × POWER hiện badge *Đã có cấu hình*, ô tick **disabled** |
| Chặn trùng lúc Lưu | chọn hãng trước rồi mới chọn công ty mua đã có ⇒ lỗi đỏ *"Đã có cấu hình với Tân Phát Power cho: MULLER AUTOMOTIVE SÂS"*, **không lưu** |
| Validate | bấm Lưu khi trống ⇒ **hiện cùng lúc 4 lỗi**, 3 ô viền đỏ `rgb(220,53,69)`, popup không đóng, `CH` giữ nguyên 8 dòng |
| Xem trước — theo giá vốn | 42,500,000 → **42,925,000** (+1%) · **43,350,000** (+2%) |
| Xem trước — theo giá bán | đủ **6 loại giá**; Bán lẻ 53,500,000 → **52,965,000** (−1%) / **52,430,000** (−2%); ĐL1 50,825,000 → 50,316,800 (làm tròn trăm) |
| Định dạng số | `,` ngăn nghìn — đúng chuẩn quốc tế của CLAUDE.md |
| Tạo nhiều hãng một lượt | chọn 4 hãng ⇒ footer *"Lưu sẽ tạo 4 dòng cấu hình"* ⇒ lưu ra **5 → 9 dòng**, badge menu trái theo kịp |
| Sửa | ô hãng **khoá** + câu giải thích; sửa % 2 → 2.8 lên bảng ngay, ngày cập nhật 24/09/2026 |
| Lịch sử | 3 dòng, giá trị cũ gạch đỏ → giá trị mới đậm |
| Xoá | popup xác nhận; bấm Đóng **không xoá** (9 dòng), xác nhận mới xoá (8 dòng) |
| Bộ lọc | lọc *Cách tính = Theo giá bán* còn 2 dòng; **đổi công ty thì bộ lọc dựng lại** (POWER chỉ còn 2 hãng / 2 công ty mua) |
| Bố cục | 1366×768: **0 cuộn ngang** ở cả bảng lẫn trang; modal 495px và popup hãng 569px **nằm trọn** trong khung, footer luôn thấy |
| Nút cùng cụm | cách **12px** |
| Menu ⋮ | đủ 3 mục, không bị khung cuộn cắt |
| Hồi quy màn cũ | 3 màn danh sách + form 7 tab vẫn chạy; popup "Công ty khác" của GREEN ra **12/12 mã** (chưa dùng mã nào), của TPE ra 5 mã |

#### 1 lỗi tự bắt được bằng Playwright (đọc code không thấy)

**Tick hãng xong, gõ từ khoá khác là mất tick.** Bảng vẽ lại theo `cfHangChon`, mà biến đó chỉ được
ghi lúc bấm "Chọn" ⇒ tick 3 hãng Bosch rồi gõ "launch" thì đếm về **1 hãng**, không báo gì.
Sửa: giữ lựa chọn trong `cfHangTam`, cập nhật NGAY mỗi lần tick. Đo lại: 3 → *"3 hãng không nằm
trong danh sách đang hiện"* → tick thêm LAU ra **4**, quay lại "bosch" thấy 3 tick còn nguyên.

#### Xem mockup

`http://127.0.0.1:8899/mockup-luong-xay-dung-hang-hoa.html` (cổng cố định vẫn đang chạy) — vào menu
trái mục **Cấu hình giá bán nội bộ**. Sửa file xong phải **Cmd+Shift+R** vì cổng cố định có cache.

### Vòng 2 — 24/09/2026: DỰNG LẠI THÀNH MỘT LƯỚI NHẬP TẠI CHỖ (user góp ý)

**Góp ý:** *"Tôi muốn một màn hình vừa là form khai báo vừa thể hiện được từng công ty có chính sách
như thế nào luôn. Popup chọn hãng chỉ là check chọn nhiều hãng ⇒ đưa ra màn hình để nhập editable
trên màn hình và lưu luôn."*

**Đã làm:** bỏ hẳn cặp *màn danh sách + popup form*; thay bằng **một lưới**: dòng = hãng ·
cột Cách tính ở cấp hãng · **nhóm cột theo từng công ty mua** (2 ô % mỗi công ty) · gõ thẳng vào ô ·
thanh ghim đáy **Huỷ thay đổi / Lưu**. Popup chọn hãng nay chỉ kéo hãng vào lưới. Menu ⋮ mỗi dòng:
**Xem trước giá** · Lịch sử · Bỏ hãng khỏi lưới. Chi tiết: `design.md` §28d · §28d-ter · §28d-bis.

#### Đã đo lại bằng Playwright (1600×900 và 1366×768, console 0 lỗi)

| Phép kiểm | Kết quả |
|---|---|
| Khung lưới | tiêu đề 2 tầng: tầng 1 *STT · Hãng sản xuất · Cách tính · 3 công ty mua (mỗi công ty colspan 2) · Hành động*; tầng 2 *Nhập khẩu / Tồn kho* × 3 |
| Đổi công ty đang làm việc | TPE **4 hãng** (nhóm cột POWER · TPSG · GREEN) · POWER **2 hãng** (nhóm cột Tân Phát · TPSG · GREEN) · GREEN **0 hãng** + dòng mời bấm *Chọn hãng* |
| Nhập tại chỗ | gõ 2.6 vào ô Tồn kho ⇒ ô nền vàng `rgb(255,251,235)`, chân màn hiện *"1 thay đổi chưa lưu"* |
| Lưu | hết ô vàng, chân màn về *"4 hãng đã có chính sách · 3 công ty mua đang được áp"*, toast xác nhận |
| Huỷ thay đổi | ô đổi 2 → 9 rồi Huỷ ⇒ giá trị về **2**, 0 ô vàng |
| Validate | 1 ô nhập **150** + 1 công ty khai thiếu ô Tồn kho ⇒ **tô đỏ đúng 2 ô**, toast liệt kê, **không lưu gì**, thay đổi vẫn còn để sửa tiếp |
| Popup chọn hãng | 1.071 hãng, vẽ 80 dòng/lượt; hãng đã trên lưới hiện *Đã có trên lưới* + **khoá tick**; chọn 3 hãng Bosch ⇒ chỉ thêm **2 dòng mới** (BOCH đã có) |
| Giữ tick qua các lượt tìm | tick 3 hãng Bosch → gõ "muller" → quay lại vẫn còn 3 tick |
| Xem trước — theo giá vốn | 42,500,000 → **42,925,000 (+1%)** · **43,350,000 (+2%)** · Green 43,137,500 (+1.5%) |
| Xem trước — theo giá bán | 6 loại giá × 2 công ty; Bán lẻ 53,500,000 → **51,360,000 (−4%)** / **50,290,000 (−6%)** |
| Bố cục 1366×768 | 0 cuộn ngang với 3 công ty mua; **ca thật 8 công ty (17 cột)** cuộn ngang **421px**, 2 cột định danh **vẫn dính trái** |
| Popup | popup chọn hãng và popup xem trước đều **nằm trọn** trong khung, footer luôn thấy |
| Hồi quy | 3 màn danh sách cũ + form hàng hoá vẫn chạy |

#### 2 lỗi tự bắt được trong vòng này

1. **Tiêu đề 2 tầng đè lên dòng dữ liệu đầu tiên** — `<th rowspan="2">` + `position:sticky` làm hàng
   tiêu đề tầng 2 tụt xuống che mất toàn bộ ô nhập của dòng 1 (nhìn ảnh mới thấy, đếm DOM vẫn đủ ô).
   Sửa: bỏ sticky cho `<th>` của bảng này, chỉ giữ dính trái 2 cột định danh. Đo lại: đáy tiêu đề
   **252px** = đỉnh dòng dữ liệu **252px**.
2. **Tick hãng mất khi đổi từ khoá tìm** (đã ghi ở vòng 1) — giữ trong mảng tạm, cập nhật ngay mỗi
   lần tick.

### Vòng 3 — 24/09/2026: lưu theo từng hãng · màu theo công ty · cảnh báo chưa lưu

**5 yêu cầu của user:** đổi nhãn *"Nhập khẩu nguyên lô"* → **"Nhập khẩu"** · **lưu theo từng hãng**,
chỉ gửi hãng có thay đổi (gửi cả lưới thì payload quá lớn) · **mỗi công ty một màu nền cột** ·
**cảnh báo khi còn thay đổi chưa lưu** · demo với 6 công ty mua: *Tân Phát Power · Tân Phát Green ·
Tân Phát Sài Gòn · Chi nhánh Hải Phòng · Chi nhánh Vinh · ETEK*.

#### Đã làm

- Nhãn cột đổi thành **Nhập khẩu / Tồn kho** (đổi cả trong popup xem trước và câu báo lỗi).
- **Nút Lưu mọc ngay trên dòng** có thay đổi; bấm là gửi **1 bản ghi của đúng hãng đó**
  (toast ghi rõ *"gửi 1 bản ghi, N công ty mua"*). Nút chân màn đổi thành **"Lưu N hãng đã đổi"**,
  cũng chỉ gửi N hãng đó. Cả 2 nút **ẩn hẳn** khi không có gì để lưu.
- **6 tông màu nền** xoay vòng theo công ty mua (tiêu đề đậm hơn, ô dữ liệu nhạt), giữ màu khi rê
  chuột; tránh vàng (đã dùng cho ô chưa lưu) và đỏ (dành cho lỗi).
- **Cảnh báo chưa lưu ở cả 3 lối rời**: đổi màn menu trái · đổi ô *"Đang làm việc tại"* · đóng/tải
  lại tab (`beforeunload`). Popup *Ở lại để lưu / Rời đi, bỏ thay đổi*.
- Dữ liệu demo dựng lại theo 6 công ty mua, có hãng khai đủ 4 công ty, có hãng mới khai 1.

#### Đã đo lại bằng Playwright (1600×900 + 1366×768, console 0 lỗi)

| Phép kiểm | Kết quả |
|---|---|
| Khung lưới | 16 cột: STT · Hãng · Cách tính · **6 nhóm công ty × (Nhập khẩu / Tồn kho)** · Hành động |
| Màu theo công ty | 6 nền khác nhau, đo `getComputedStyle`: `#dbeafe · #dcfce7 · #cffafe · #ede9fe · #fae8ff · #e2e8f0` |
| Sửa 2 hãng | nút **Lưu mọc đúng 2 dòng** (MLER, LAU), 3 dòng còn lại không có; chân màn *"2 hãng chưa lưu"*, nút *"Lưu 2 hãng đã đổi"* |
| Lưu riêng 1 hãng | toast *"Đã lưu MULLER AUTOMOTIVE SÂS — gửi 1 bản ghi, 4 công ty mua"*; còn đúng **1 hãng chưa lưu**, nút Lưu chỉ còn ở dòng LAUNCH |
| Cảnh báo — đổi công ty | popup *"Còn 1 hãng chưa lưu"*, **ô "Đang làm việc tại" tự trả về Tân Phát**, `CUR` không đổi |
| Cảnh báo — đổi màn | bấm menu *Đang nhập thông tin* ⇒ popup chặn, màn vẫn là `sc-cf` |
| Ở lại để lưu | popup đóng, vẫn ở màn cũ, thay đổi còn nguyên |
| Rời đi, bỏ thay đổi | chuyển đúng sang `sc-l1`; quay lại lưới thì ô về giá trị cũ (4.5 → 4) |
| Cảnh báo — đóng/tải lại tab | `beforeunload` chặn thật (Playwright phải xử lý hộp thoại mới nạp lại được trang) |
| Nút Lưu / Huỷ khi không có thay đổi | **ẩn hẳn** (`hidden`), không hiện nút xám |
| Bố cục | 0 cuộn ngang ở cả 1600×900 lẫn 1366×768; cột định danh vẫn dính trái khi cuộn |

#### 2 lỗi tự bắt được trong vòng này

1. **"Rời đi, bỏ thay đổi" mà màn đứng im** — `coThayDoi()` đếm từ các ô đang có trên DOM, khôi phục
   dữ liệu xong mà chưa vẽ lại thì việc đang chờ (đổi màn) bị chính popup đó chặn tiếp, **không báo
   gì**. Sửa: vẽ lại lưới TRƯỚC khi chạy việc đang chờ.
2. **Chữ trong ô chọn Cách tính bị cắt** (*"Theo giá vốr"*) — đổi nhãn trong ô thành **Giá vốn /
   Giá bán** (tiêu đề cột đã nói "Cách tính"), đo lại: chữ 41px trong ô 99px.

### Vòng 4 — 24/09/2026: ĐỔI TRỤC — công ty thành DÒNG, giá trị cấu hình thành CỘT

**User:** *"Không ổn ⇒ đổi phương án cho công ty thành row, các giá trị cấu hình là col. Gộp hãng,
mỗi công ty là 1 row nhưng phần chọn cách tính theo Giá bán/giá vốn là theo hãng chứ không cần theo
từng công ty."*

**Đã làm:** bỏ kiểu "mỗi công ty một nhóm 2 cột" (bảng phình ngang theo số công ty). Nay:
**ô Hãng + ô Cách tính gộp dòng (`rowspan`)**, **mỗi công ty mua là một dòng**, cột là các giá trị
cấu hình: *Công ty mua · Nhập khẩu (%) · Tồn kho (%) · Cập nhật gần nhất · Hành động*. Nút
**"Lưu hãng này"** + menu ⋮ nằm trong ô gộp của hãng. Màu riêng theo công ty chuyển thành **nền + vạch
màu ở ô tên công ty**. Thêm nút **Xoá** tỷ lệ của riêng một công ty và tick **"Chỉ hiện công ty đã khai"**.

#### Đã đo bằng Playwright (1600×900 + 1366×768, console 0 lỗi)

| Phép kiểm | Kết quả |
|---|---|
| Khung bảng | 8 cột: STT · Hãng sản xuất · Cách tính · Công ty mua · Nhập khẩu (%) · Tồn kho (%) · Cập nhật gần nhất · Hành động |
| Gộp dòng | ô Hãng / Cách tính có `rowspan=6` đúng bằng số công ty mua; **5 hãng → 30 dòng công ty** |
| Cách tính | mỗi hãng **một** ô chọn (kèm chú *"áp cho cả hãng"*), không lặp theo công ty |
| Cuộn ngang | **0** ở cả 1600×900 lẫn 1366×768 (đây là lý do đổi trục) |
| Màu theo công ty | 6 tông nền + vạch màu trái ở ô tên công ty |
| Nhập tại chỗ | gõ 2 ô của MULLER ⇒ **nút "Lưu hãng này" chỉ mọc ở ô gộp của MULLER**, 4 hãng còn lại không có; chân màn *"1 hãng chưa lưu"*, nút *"Lưu 1 hãng đã đổi"* |
| Lưu riêng hãng | toast *"Đã lưu MULLER AUTOMOTIVE SÂS — gửi 1 bản ghi, 5 công ty mua"*; dòng Hải Phòng đổi từ *Chưa khai* → **24/09/2026 Nguyễn Văn An** |
| Xoá tỷ lệ 1 công ty | ô về trống, dòng về *Chưa khai*, hãng đó lại có thay đổi chưa lưu |
| Lọc "Chỉ hiện công ty đã khai" | 30 → **14 dòng**, vẫn đủ 5 hãng |
| Cảnh báo chưa lưu | đổi màn khi còn 1 hãng chưa lưu ⇒ popup *"Còn 1 hãng chưa lưu"*, màn vẫn `sc-cf`; *Rời đi* ⇒ sang `sc-l1` và dữ liệu về như cũ |
| Footer ghim đáy | cuộn hết bảng: đáy dòng cuối **804px** < đỉnh footer **852px** ⇒ **không che** |

**Ghi chú kiểm:** một lượt đo tưởng là "cảnh báo không chạy" — thực ra kịch bản đo sai (đang đứng ở
màn khác, bảng `#tb-cf` vẫn nằm trong DOM ẩn nên vẫn set được giá trị). Chạy lại đúng khi đứng ở màn
chính sách thì popup chặn đúng. Giữ lại đây để lần sau khỏi "sửa" một lỗi không tồn tại.

### Vòng 5 — 24/09/2026: nút hành động · khoá xoá hãng đã khai · màu · giờ phút giây · popup lịch sử chuẩn

**6 yêu cầu của user:** cột Hành động để **button Lưu / Xem trước giá** · **bỏ thao tác xoá theo công
ty** · **hãng đã khai báo thì không được xoá**, chỉ hãng vừa chọn vào mà chưa lưu mới bỏ được ·
**chỉnh lại màu công ty** · **Cập nhật gần nhất hiện cả giờ phút giây** · **popup Lịch sử dựng đúng
chuẩn skill**.

#### Đã làm

- Cột **Hành động** thành ô gộp theo hãng, chứa **button**: `Lưu` (chỉ khi hãng có thay đổi) ·
  `Xem trước giá` · `Lịch sử` · `Bỏ khỏi lưới` (chỉ hãng chưa lưu lần nào). **Bỏ menu ⋮** và
  **bỏ nút Xoá ở dòng công ty** — muốn bỏ chính sách một công ty thì xoá trắng 2 ô rồi Lưu.
- **Màu công ty** đổi công thức: vạch trái 4px màu đậm + nền `rgba(màu,.07)` + tên công ty in chính
  màu đó (đậm) — `#2563EB · #0891B2 · #16A34A · #7C3AED · #C026D3 · #475569`.
- **Cập nhật gần nhất** lưu **theo từng công ty** (`ty[cty].luc` / `.nguoi`), định dạng
  `dd/mm/yyyy HH:mm:ss`; khi lưu chỉ công ty **có thay đổi** mới đóng lại mốc mới.
- **Popup Lịch sử** dựng lại theo `.claude/skills/entity-history/ui-base.md` (đọc cả `SKILL.md` §0a):
  3 nhóm hành động cố định · ô Người thực hiện lấy từ danh sách nhân sự `MÃ PHÒNG - Tên` ·
  timeline mới → cũ · cũ đỏ → mới xanh · ghi chú nền vàng · footer chỉ nút Đóng.
  Mỗi lần **Lưu** sinh mục log thật; bỏ chính sách của một công ty ghi vào nhóm *Thay đổi trạng thái*.

#### Đã đo bằng Playwright (1600×900 + 1366×768, console 0 lỗi ngoài favicon)

| Phép kiểm | Kết quả |
|---|---|
| Cột Hành động | hãng đã lưu: `Xem trước giá · Lịch sử`; có thay đổi thì thêm `Lưu` đứng đầu |
| Hãng vừa chọn vào (3M) | đủ 4 nút, **có `Bỏ khỏi lưới`**; bấm ⇒ popup xác nhận ⇒ biến khỏi lưới (6 → 5 hãng) |
| Hãng đã khai (MULLER) | **không có** nút Bỏ khỏi lưới |
| Xoá theo công ty | **0 nút** `.xoa-o` trên toàn bảng |
| Cập nhật gần nhất | `23/09/2026 14:05:32` · sau khi lưu ra `24/09/2026 16:09:49` — đủ giờ phút giây, chỉ dòng công ty vừa đổi mới nhảy mốc |
| Màu công ty | 6 màu định danh, tên công ty in đúng màu, vạch trái 4px |
| Popup lịch sử | tiêu đề *"Lịch sử chính sách giá bán nội bộ"*, phụ đề `Hãng sản xuất: Fusheng · công ty bán: Tân Phát`, 3 mục **mới → cũ** (`22/09 09:15:03` → `22/09 09:14:27` → `15/09 10:40:18`) |
| Một mục log | thời gian → hành động (màu nhóm `rgb(217,119,6)`) → `Người thực hiện: Trần Thị Bình — Phòng Kinh doanh 1` → thay đổi `Nhập khẩu 3% · Tồn kho 4.5%` (đỏ `rgb(220,38,38)`) → `(trống)` (xanh `rgb(22,163,74)`) → ghi chú nền vàng |
| Bộ lọc lịch sử | Loại hành động đúng **3 nhóm**; Người thực hiện **5 nhân sự** dạng `HN_KD1 - Nguyễn Văn An`; lọc *Thay đổi trạng thái* còn 1 mục; lọc không ra ⇒ *"Không có lịch sử phù hợp bộ lọc."*; Làm mới về 3 mục |
| Bố cục | 0 cuộn ngang ở cả 2 độ phân giải; nút trong cột Hành động rộng 144px, không tràn chữ; popup lịch sử nằm trọn trong khung |

### Vòng 6 — 24/09/2026: tên công ty · lọc Công ty mua · Hệ số chung

**4 yêu cầu của user:** đổi tên công ty thành **ETEK POWER · ETEK GREEN · ETEK · TÂN PHÁT SG ·
CN HẢI PHÒNG · CN VINH** · bộ lọc thêm **Công ty mua** · thêm tuỳ chọn toàn cục **Chọn cách khai báo:
Hệ số theo công ty / Hệ số chung** · chọn *Hệ số chung* thì **chỉ khai ở công ty đầu tiên**, các công
ty còn lại kế thừa giống nhau.

#### Đã đo bằng Playwright (1600×900 + 1366×768, console 0 lỗi)

| Phép kiểm | Kết quả |
|---|---|
| Tên + thứ tự công ty | đúng 6 dòng `ETEK POWER · ETEK GREEN · ETEK · TÂN PHÁT SG · CN HẢI PHÒNG · CN VINH`; ô lọc cũng đúng thứ tự đó |
| Lọc **Công ty mua** = TÂN PHÁT SG | 30 → **5 dòng** (mỗi hãng 1 dòng), chỉ còn công ty đã chọn |
| Dải chọn cách khai báo | 2 lựa chọn + dòng chú giải đổi theo chế độ, cao 25px, thanh lọc tổng 107px |
| Bật **Hệ số chung** | **10 ô nhập được** (2 ô × 5 hãng, chỉ ở ETEK POWER) · **50 ô khoá** kèm nhãn *"kế thừa từ ETEK POWER"* |
| Gõ ở công ty đầu | nhập 2.7 ⇒ **cả 5 công ty còn lại nhận 2.7 ngay**, ô vẫn khoá |
| Giữ dữ liệu khi bật hệ số chung | hãng BOCH (chưa khai ở ETEK POWER) vẫn giữ nguyên **5 hãng có chính sách**, lấy dòng TÂN PHÁT SG làm gốc lan cho cả 6 công ty |
| Bố cục | 0 cuộn ngang ở cả 2 độ phân giải |

#### 1 lỗi tự bắt được (mất dữ liệu im lặng)

Bản lan toả đầu lấy **đúng** công ty đầu làm gốc: hãng nào chưa khai ở công ty đó thì **xoá sạch**
chính sách của các công ty khác ⇒ bật *Hệ số chung* là **5 hãng còn 3**, không báo gì. Sửa: công ty
đầu trống thì lấy **dòng đã khai đầu tiên** làm gốc; hãng chưa khai ở đâu cả mới để trống. Đo lại:
5 hãng giữ nguyên.

### Vòng 7 — 24/09/2026: đổi khái niệm · toggle · dời Cách khai báo lên thanh tiêu đề

**3 yêu cầu của user:** đổi khái niệm **Công ty chủ → Công ty bán**, **Công ty nhận → Công ty mua** ·
bộ lọc đổi checkbox *"Chỉ hiện công ty đã khai"* sang **toggle**, căn cân đối với các ô lọc khác ·
đưa **Cách khai báo** xuống **card header cùng nút Chọn hãng**, chú thích từng lựa chọn gom vào
**icon ⓘ**.

#### Đã đo bằng Playwright (1600×900 + 1366×768, console 0 lỗi)

| Phép kiểm | Kết quả |
|---|---|
| Khái niệm | tiêu đề bảng: *"TÂN PHÁT là công ty bán, khai cho 6 công ty mua"*; cột *Công ty mua*; ô lọc *Công ty mua*; đổi cả trong tài liệu (`design.md`, `plan.md`, `SO-CHOT-VA-TON.md`, khối §28 của `STATUS.md`) |
| Toggle | track **28×16px**, tắt `#cbd5e1` → bật `#1abc9c`, knob dịch **12px** (đúng `custom-switch` Bootstrap của app); có nhãn *Hiển thị* phía trên nên **thẳng hàng với ô Công ty mua** |
| Toggle chạy thật | bật ⇒ 30 → **14 dòng**, tắt ⇒ về 30 |
| Cách khai báo | nằm trong **thanh tiêu đề bảng** (`.tp-card.p0 .tp-head`), **không còn** ở thanh lọc; header cao **55px**, không xuống dòng ở 1366 |
| Icon ⓘ | 14px, viền `#0a99a7` khi hover; tooltip **hiện thật khi hover** (`visibility: visible`), rộng 300px, nội dung nêu đích danh *ETEK POWER* |
| Thanh lọc | còn **77px** một hàng (trước là 107px vì có thêm dải cách khai báo) |
| Bố cục | 0 cuộn ngang ở cả 2 độ phân giải |

#### 1 lỗi tự bắt được

**Tooltip tràn khỏi khung nhìn.** Icon ⓘ nằm sát mép phải, tooltip 300px căn giữa
(`translateX(-50%)`) ⇒ mép phải **1475 > 1464** (đo ở 1600×900), chữ bị cắt. Sửa: neo tooltip theo
**mép phải** của icon. Đo lại: 1600 → `1161…1461`; 1366 → `927…1227`, không tràn.

### Vòng 8 — 24/09/2026: 4 chỉnh nhỏ theo góp ý

| # | Yêu cầu | Đã làm · đo được |
|---|---|---|
| 1 | Bỏ chữ *"kế thừa từ xxx"* ở chế độ hệ số chung (làm lệch dòng) | Gỡ hẳn dòng chữ, giải thích chuyển vào `title` của ô khoá (*"Kế thừa từ ETEK POWER"*). Đo: **0** nhãn `.ke-thua`, 50 ô vẫn khoá |
| 2 | Cột *Cập nhật gần nhất* không có viền phía giáp cột Hành động | Nguyên nhân: cột Hành động là **ô gộp** nên ô cuối của phần lớn dòng là *Cập nhật gần nhất*, dính rule chung `td:last-child{border-right:0}`. Khai lại viền cho bảng này; đo: viền phải **1px `#e5e7eb`** |
| 3 | Hãng mới thêm phải hiện **ở đầu bảng** | Đổi `push` → `unshift`. Đo: thêm hãng 3M ⇒ thứ tự `3M · MLER · FUSE · BOCH · LAU · BRAG` |
| 4 | Bỏ chú *"áp cho cả hãng"*, thay bằng ghi chú **dấu của công thức** | Dưới ô chọn nay là `+ % trên giá vốn` (xanh) / `− % trên giá bán` (cam), đổi **ngay** khi chọn lại |

**Vá kèm (tự thấy khi đo):** dòng công ty cao so le 37/39/41px (dòng *Chưa khai* vs dòng có
*ngày + người* vs dòng đầu nhóm) ⇒ ghim `td{height:38px}`; đo lại còn 38/39 (41 là dòng đầu nhóm,
chênh đúng 2px đường kẻ phân nhóm). Ô nhập thẳng hàng tên công ty (lệch tâm 0–1px).

### Vòng 9 — 24/09/2026: cảnh báo chưa lưu theo chuẩn phần mềm

**User:** *"Cảnh báo lưu thay đổi trước khi thoát làm theo quy chuẩn phần mềm, không dùng popup
trình duyệt."*

**Đã làm:** gỡ hẳn `window.addEventListener('beforeunload')`; popup dựng lại theo đúng chữ của
`.claude/skills/unsaved-changes` mục 1.

| Phép kiểm | Kết quả |
|---|---|
| Tiêu đề | **Thông tin chưa lưu** (dòng phụ *"Còn 1 hãng chưa lưu"*) |
| Câu hỏi | **Bạn có thông tin chưa lưu. Có chắc chắn muốn thoát?** |
| Nút | **Thoát** (`btn-xoa` — nhóm nguy hiểm) · **Ở lại** (tertiary) |
| Bấm *Ở lại* | vẫn ở màn chính sách, thay đổi còn nguyên (1 hãng chưa lưu) |
| Bấm *Thoát* | sang màn đích, dữ liệu trả về bản đã lưu (0 thay đổi) |
| Hộp thoại trình duyệt | **hết** — nguồn không còn `beforeunload`; tải lại trang khi đang có thay đổi đi thẳng, không bị chặn (trước đó Playwright bị treo 60s vì hộp thoại này) |

⚠️ Ghi để khỏi tranh cãi sau: skill `unsaved-changes` có nêu dùng `beforeunload` cho ca đóng tab/F5,
nhưng **yêu cầu của user thắng skill** — màn này bỏ hẳn.

### Vòng 10 — 24/09/2026: 2 nút Excel + icon ⓘ cho 2 cột tỷ lệ

**User:** *"Thêm 2 button: Xuất excel, import excel"* · *"Thêm info icon cho 2 tiêu đề cột —
Nhập khẩu: Giá tính cho trường hợp bán nguyên lô nhập khẩu về thẳng kho Công ty mua; Tồn kho: Giá
tính cho trường hợp xuất bán cho công ty mua từ kho."*

**Đã làm:** 2 nút đặt ở thanh tiêu đề bảng theo `button-convention` — **Import Excel** tông **cam**
(`secondary status="warning"`, ghi dữ liệu vào hệ thống), **Xuất Excel** tông **xanh lá**
(`secondary status="success"`, nhóm chỉ đọc). Popup import dựng theo `V2BaseImportModal` +
`V2BaseImportToolbar`. Icon ⓘ gắn vào 2 tiêu đề cột tỷ lệ.

#### Đã đo bằng Playwright (console 0 lỗi)

| Phép kiểm | Kết quả |
|---|---|
| Màu nút | Import Excel viền `rgb(245,158,11)` chữ `rgb(180,83,9)`; Xuất Excel viền `rgb(22,163,74)` chữ `rgb(21,128,61)`; Chọn hãng vẫn primary |
| Icon ⓘ 2 cột | tooltip đúng nguyên văn 2 câu của user; hover thật thì `visibility: visible`, hộp 300px nằm trong khung (`695…995` / 1366) |
| Xuất Excel | toast *"Đang xuất 14 dòng chính sách của TÂN PHÁT…"* → tên tệp có mã công ty + ngày |
| Popup import | 3 nhóm **File · Hành động · Hiển thị**, đủ 5 nút đúng chữ của app: *Chọn file Excel · Tải file mẫu · Load lên bảng · Validate · Import* |
| Chặn thao tác sai thứ tự | chưa chọn file mà bấm *Load lên bảng* ⇒ *"Chưa chọn file Excel"*; chưa Validate mà bấm *Import* ⇒ *"Bấm Validate trước khi Import"* |
| Validate | 5 dòng ⇒ **3 hợp lệ / 2 lỗi**; lỗi ghi **ngay dưới ô sai** (*"Mã hãng không có trong danh mục"*, *"Nhập khẩu: phải trong khoảng 0 – 100"*) |
| Toggle *Chỉ dòng lỗi* | 5 → **2 dòng** |
| Import | nạp **3 dòng hợp lệ** vào lưới, popup đóng, chân màn hiện *"3 hãng chưa lưu"* — đúng luật: nạp xong vẫn phải bấm Lưu |

**Kèm theo:** bỏ dòng phụ *"— TÂN PHÁT là công ty bán, khai cho 6 công ty mua"* cạnh tiêu đề bảng
(user chốt là thừa); đổi công ty vẫn chạy bình thường, 0 lỗi console.

#### 1 lỗi tự bắt được

**Dòng lỗi trong bảng import không ăn nền hồng** — `table.tbl td{background:#fff}` có độ ưu tiên cao
hơn `.dong-loi td`, đếm class vẫn ra đủ 2 dòng nên chỉ nhìn ảnh mới lộ. Neo lại theo id bảng; đo:
dòng lỗi `rgb(255,245,245)`, dòng thường `rgb(255,255,255)`.

### Checkpoint — 24/09/2026 (WRAP UP — mockup Chính sách giá bán nội bộ §28)

**Vừa hoàn thành:** màn **Chính sách giá bán nội bộ** trong `mockup-luong-xay-dung-hang-hoa.html`
(133 KB → **269 KB**), qua **10 vòng sửa theo góp ý user** trong ngày. Hình thức chốt cuối:

- Lưới **hãng gộp dòng (`rowspan`) · mỗi CÔNG TY MUA là một dòng · giá trị cấu hình là cột**;
  cột *Cách tính* ở cấp hãng kèm ghi chú dấu (`+ % trên giá vốn` / `− % trên giá bán`).
- **Lưu theo từng hãng** (nút *Lưu* mọc ở cột Hành động của hãng có thay đổi; nút chân màn
  *"Lưu N hãng đã đổi"* cũng chỉ gửi hãng đã đổi) · **Huỷ thay đổi** · cảnh báo **chưa lưu** bằng
  popup của phần mềm (bỏ `beforeunload`).
- Cột Hành động: **Lưu · Xem trước giá · Lịch sử** (+ *Bỏ khỏi lưới* chỉ với hãng chưa lưu lần nào);
  **không có thao tác xoá theo công ty**.
- Bộ lọc 1 hàng: tìm hãng · **Công ty mua** · **toggle** *Chỉ công ty đã khai* · Làm mới.
- Thanh tiêu đề: **Cách khai báo** (Hệ số theo công ty / Hệ số chung, chú thích trong icon ⓘ) ·
  **Chọn hãng** · **Import Excel** (cam) · **Xuất Excel** (xanh lá).
- Popup: **Chọn hãng** (1.071 hãng thật, tick nhiều) · **Xem trước giá** · **Lịch sử** (đúng khuôn
  `entity-history/ui-base.md`) · **Import Excel** (khuôn `V2BaseImportModal`) · **Bỏ khỏi lưới** ·
  **Thông tin chưa lưu**.
- Dữ liệu demo: công ty bán **TÂN PHÁT**, 6 công ty mua **ETEK POWER · ETEK GREEN · ETEK ·
  TÂN PHÁT SG · CN HẢI PHÒNG · CN VINH**; 5 hãng có chính sách; mốc cập nhật có **giờ phút giây**
  riêng theo từng công ty mua.

**Đang làm dở:** không có file nào dang dở. **Hai repo code sạch phần này** — không đụng một dòng
source nào (`hrm-api`/`hrm-client` chỉ còn thay đổi của Phase 8 Phòng họp từ session trước).

**Bước tiếp theo:** user duyệt mockup §28 → mockup **nơi hiện số gợi ý** (popup *Xem hàng hoá Công ty
khác* / màn Tính giá — §28e) → rồi vào **vòng chốt 14 tồn** (6 câu `SO-CHOT-VA-TON.md` mục 3 + 8 câu
`design.md` §26g) + **4 tồn riêng của màn** (§28f) trước khi mở code.

**Blocked:** không.

#### 10 vòng sửa trong ngày (tóm tắt)

| Vòng | Nội dung |
|---|---|
| 1 | Dựng lần đầu: danh sách + popup khai, popup chọn hãng 1.071 hãng |
| 2 | Đổi thành **một lưới nhập tại chỗ** (bỏ cặp danh sách + form) |
| 3 | Lưu theo từng hãng · màu theo công ty · cảnh báo chưa lưu · 6 công ty demo |
| 4 | **Đổi trục**: công ty thành DÒNG, giá trị cấu hình thành CỘT, hãng gộp dòng |
| 5 | Cột Hành động là button · khoá xoá hãng đã khai · giờ phút giây · popup Lịch sử chuẩn skill |
| 6 | Tên công ty ETEK* · lọc **Công ty mua** · tuỳ chọn **Hệ số chung** |
| 7 | Đổi khái niệm **Công ty bán / Công ty mua** · toggle · dời Cách khai báo lên thanh tiêu đề |
| 8 | Bỏ chữ "kế thừa từ…" · vá viền cột · hãng mới lên đầu bảng · ghi chú dấu công thức |
| 9 | Cảnh báo chưa lưu theo chuẩn phần mềm, **gỡ `beforeunload`** |
| 10 | **Import / Xuất Excel** · icon ⓘ 2 cột tỷ lệ · bỏ dòng phụ tiêu đề |

#### 9 lỗi tự bắt được bằng Playwright cả đợt (test xanh / đọc code đều không thấy)

1. Tick hãng xong gõ từ khoá khác ⇒ **mất tick im lặng** (3 → 1).
2. `th rowspan=2` + `sticky` ⇒ hàng tiêu đề tầng 2 **đè lên dòng dữ liệu đầu tiên**.
3. Bật *Hệ số chung* ⇒ hãng chưa khai ở công ty đầu bị **xoá sạch chính sách** (5 hãng còn 3).
4. Bấm *"Rời đi, bỏ thay đổi"* mà **màn đứng im** (đếm thay đổi từ DOM cũ).
5. Chữ trong ô chọn *Cách tính* bị cắt (*"Theo giá vốr"*).
6. Tooltip ⓘ căn giữa **tràn khỏi khung nhìn** (phải 1475 > 1464).
7. Cột *Cập nhật gần nhất* **mất viền phải** vì cột Hành động là ô gộp.
8. Dòng công ty cao **so le 37/39/41px**.
9. Dòng lỗi bảng import **không ăn nền hồng** (`table.tbl td` đè `.dong-loi td`).

#### Xem mockup

`http://127.0.0.1:8899/mockup-luong-xay-dung-hang-hoa.html` → menu trái **Cấu hình giá bán nội bộ**.
Cổng cố định 8899 vẫn chạy; sửa file xong phải **Cmd+Shift+R** vì cổng này có cache.

---

## §29 · MOCKUP PHIẾU TÍNH GIÁ cho hàng lấy từ công ty khác (yêu cầu 26/09/2026)

**Yêu cầu user:** *"Thiết kế Mockup màn hình phiếu tính giá cho Case lấy hàng hoá công ty khác về
để kinh doanh: User dùng chức năng xem hàng hoá công ty khác ⇒ chọn ⇒ lấy về danh sách hàng đang
nhập thông tin ⇒ bổ sung đủ thông tin ⇒ Lập Yêu cầu tính giá. Với phiếu tính giá loại này ngoài
form hiện có của phiếu tính giá thì cần hiển thị thêm các thông tin về giá mua từ công ty quản lý
hàng hoá theo cấu hình của màn Chính sách giá bán nội bộ."*

### Đáp án user chốt (26/09/2026)

| # | Câu | Chốt |
|---|---|---|
| 1 | Hàng tự tạo và hàng lấy về tính giá theo đường nào | **MỌI hàng đều qua chứng từ tính giá** (Yêu cầu tính giá → Phiếu tính giá), không tính giá trong form hàng hoá nữa |
| 2 | Ô giá đầu vào của phiếu | **Để trống, người tính giá tự nhập** — khối phương án chỉ để đọc |
| 3 | 2 tỷ lệ Nhập khẩu / Tồn kho | **Hiện cả 2 số song song**, không phải chọn nguồn |
| 4 | Khối tham khảo hiện gì | Cách tính + % chính sách · **giá vốn của công ty quản lý CHỈ khi cách tính theo giá vốn** · **giá bán LUÔN hiện** · giá mua suy ra từ tỷ lệ |
| 5 | Ô của ERP cho hàng nhập khẩu | **Giữ nguyên hết** (đơn vị tiền tệ · tỉ giá · thuế NK · tab Chi phí) — một khuôn phiếu dùng cho cả 2 case |

### Task

- [x] T1 · Khảo sát phiếu tính giá ERP (form, công thức, luồng duyệt, số thật)
- [x] T2 · Dữ liệu demo: map thương hiệu → mã hãng sản xuất, bổ sung hàng "lấy từ công ty khác"
- [x] T3 · Màn **Yêu cầu tính giá**: nút lập ở màn *Đang nhập thông tin* + danh sách + form
- [x] T4 · Màn **Phiếu tính giá** (danh sách) + popup chọn yêu cầu tính giá
- [x] T5 · **Form phiếu tính giá**: Thông tin chung + 3 tab (Hàng hoá · Chi phí · Tính giá) như ERP
- [x] T6 · **Chính sách giá nội bộ theo từng hàng hoá + nút "Tạm tính"** (popup chi tiết)
- [x] T7 · Kiểm bằng Playwright, đo số từ DOM; ghi §29 vào design.md + STATUS.md

### Checkpoint — 26/09/2026 (mockup §29 xong, chờ user duyệt)

**Vừa hoàn thành:** mockup **Yêu cầu tính giá + Phiếu tính giá** cho hàng lấy từ công ty khác, dựng
vào `mockup-luong-xay-dung-hang-hoa.html` (269 KB → **309 KB**). 4 màn mới (2 danh sách + 2 form),
2 popup (*Tạm tính giá mua* · *Chọn yêu cầu tính giá*), 2 mục menu trái. Hai repo **không đụng dòng
source nào** (đúng §22).

**Bằng chứng đo được:** dựng lại đúng phiếu thật **PTG-03178** trên mockup ⇒ Giá nhập kho
**13,108,986** khớp từng đồng với DB; tạm tính *theo giá vốn* 13,108,986 ⇒ 13,213,900 / 13,318,700;
*theo giá bán* 12,500,000 ⇒ 12,125,000 / 11,875,000. Console 0 lỗi.

**5 lỗi tự bắt được:** mất giá khi đổi tiền tệ · tỉ giá không đổi theo tiền tệ · số chứng từ nhảy số ·
bảng bị bóp (ô nhập còn 36px) · dòng giá cao 73px do badge + nút rơi 2 dòng.

**Ảnh chụp thật:** `anh-mockup/29-*.png` (5 ảnh).

**Bước tiếp theo:** user duyệt mockup §29 → chốt **5 việc treo ở design.md §29f** (gỡ tab Giá bán khỏi
form hàng hoá · gate giá vốn liên công ty · ai lập/ai duyệt · phiếu gom nhiều công ty quản lý · lưu vết
số tham khảo) → nhập chung vào **vòng chốt 14 tồn** trước khi mở code.

**Blocked:** không.

### §29g · Gỡ tab "Giá bán" khỏi form hàng hoá (user chốt 27/09/2026)

- [x] T8 · Gỡ tab 7 + pane + footer vai tính giá + 7 hàm/biến liên quan; bỏ vai `'gia'` khỏi 3 mức quyền
- [x] T9 · Nối lại lối vào: nút *Tính giá* ở màn Chờ tính giá → mở phiếu tính giá (`moTinhGia`); bỏ mục *Sửa giá* ở menu màn kinh doanh; sửa mô tả bước 2 của sơ đồ luồng
- [x] T10 · Bổ sung chứng từ demo cho 2 mã đang ở *Chờ tính giá* / *Đang tính giá* (YCTG-00309, YCTG-00310, PTG-03178)
- [x] T11 · Kiểm lại bằng Playwright: form còn 6 tab, khoá theo công ty vẫn đúng, 2/2 hàng truy được về chứng từ, chạy lại trọn luồng, console 0 lỗi

### Checkpoint — 27/09/2026 (gỡ tab Giá bán)

**Vừa hoàn thành:** form hàng hoá còn **đúng 6 tab thông tin**; toàn bộ việc tính giá chuyển sang
cặp chứng từ *Yêu cầu tính giá → Phiếu tính giá*. Không còn nút/menu nào trỏ vào hàm đã gỡ —
đã grep sạch (`moGia`, `pane-gia`, `tab-gia`, `ft-gia`, `veTabGia`, `luuTamGia`, `luuVaDuyetGia`,
`dangTinhGia`). Mockup 309 KB → **300 KB**. Hai repo vẫn **không đụng dòng source nào**.

**Đang làm dở:** không có.

**Bước tiếp theo:** chốt 4 việc treo còn lại ở `design.md` §29f (gate giá vốn liên công ty · yêu cầu
tính giá có cần bước duyệt · phiếu có được gom nhiều công ty quản lý · lưu vết chính sách lúc tính
giá), gộp vào vòng chốt 14 tồn trước khi mở code.

**Blocked:** không.

### §30 · Sửa spec cây 4 cấp Lĩnh vực (user chốt 27/09/2026)

- [x] T12 · Khảo sát 4 bảng cây + chỗ dùng thật (`product_group_classifies` 1.019 · `product_classifies` 0 · `Product::searchByFilter` 4 chỗ)
- [x] T13 · Xác định danh mục thay thế: `internal_business_scopes` (HRM, 8 dòng, màn đã có, quyền 1177/1178)
- [x] T14 · Đếm tham chiếu `scopes` ngoài nhánh hàng hoá (1.058 dòng / 5 bảng) → chốt **giữ bảng, chỉ gỡ màn**
- [x] T15 · Sửa spec: `quan-ly-hang-hoa/design.md` mục B + bảng Phase (thêm **Phase 2d**, sửa Phase 5); `man-danh-muc-hang-hoa/design.md` **§30**; STATUS.md
- [x] T16 · Chốt **bỏ hết dữ liệu catalog cũ, làm mới hoàn toàn** (§30d) — đã soát không phân hệ nào khác dùng
- [x] T17 · Chốt 2 tồn cuối (§30f): **riêng theo từng công ty** · **tối thiểu 3 cấp** tới Nhóm công việc
- [x] T18 · Chốt **xoá sạch data** `scopes` + 3 danh mục + bảng nối; đo lại bằng model và **đính chính** con số "1.058 tham chiếu" (sai do trùng id với `hrm_scopes`)
- [x] T19 · Note **11 vấn đề phát sinh do bỏ data** vào §30e + sổ chốt mục 5
- [ ] T20 · Dựng mockup 4 ô lọc dây chuyền trong tab Dữ liệu quản trị theo công ty

### Checkpoint — 27/09/2026 (§30 hết tồn)

**Vừa hoàn thành:** spec cây 4 cấp lĩnh vực đã chốt đủ — bỏ sạch data cũ, khai mới dưới gốc *Lĩnh
vực Công ty kinh doanh*, 4 cấp nằm trong tab *Dữ liệu quản trị* **riêng theo từng công ty**, **tối
thiểu 3 cấp**. 11 vấn đề do bỏ data đã note.

**Đính chính:** nhận định *"`scopes` còn 1.058 tham chiếu sống"* (ghi ở lượt trước) là **sai** —
đếm bằng id trong khi `scopes` trùng dải id với `hrm_scopes`. Đo lại bằng model: không bảng nào
ngoài nhánh hàng hoá dùng `scopes`.

**Bước tiếp theo:** dựng mockup 4 ô lọc dây chuyền trong tab Dữ liệu quản trị (T20).

**Blocked:** không.

### §30g · Form hàng hoá chia 2 tầng tab (user chốt 28/09/2026)

- [x] T20 · Chia 2 tab cha (Thông tin hàng hoá / Quản trị hàng hoá) + 5 tab con; CSS thanh tab cha
- [x] T21 · Chuyển pane *Dữ liệu quản trị* sang tab cha thứ 2, thêm khối **Phân loại theo lĩnh vực kinh doanh** (4 ô lọc dây chuyền)
- [x] T22 · Lưu **riêng theo từng công ty** + validate **tối thiểu 3 cấp**; sửa cách khoá tab cho 3 mức quyền §26c-bis
- [x] T23 · Kiểm bằng Playwright: cấu trúc tab, lọc dây chuyền, 🔒 lĩnh vực khoá, riêng theo công ty, validate, hàng công ty khác — console 0 lỗi

### Checkpoint — 28/09/2026 (form 2 tầng tab + catalog 4 cấp)

**Vừa hoàn thành:** form hàng hoá chia **2 tab cha**; tab *Quản trị hàng hoá* gồm khối Dữ liệu quản
trị cũ + khối **Phân loại theo lĩnh vực kinh doanh** 4 cấp, khai **riêng theo từng công ty**, bắt
buộc **tối thiểu 3 cấp**. Mockup 300 KB → **310 KB**. Hai repo vẫn không đụng dòng source nào.

**Bước tiếp theo:** user duyệt §30g. Sau đó còn 4 tồn của §29f (gate giá vốn liên công ty · yêu cầu
tính giá có bước duyệt không · phiếu gom nhiều công ty quản lý · lưu vết chính sách lúc tính giá).

**Blocked:** không.

- [x] T24 · Thiết kế lại 2 tầng tab: **tab cha segmented + icon**, **tab con dạng stepper** (vòng tròn số · đường nối · dấu ✓), chấm đỏ báo tab còn thiếu
- [x] T25 · Sửa 2 lỗi trùng tên class (`.step` → `.fstep*`, `.loi` → `.o-loi`) — cả hai chỉ lộ khi chụp ảnh nhìn, số liệu DOM vẫn "đúng"
- [x] T26 · Tab cha đổi sang **segmented control kiểu iOS**: thumb trắng trượt bằng `transform` + easing `cubic-bezier(.32,.72,0,1)`, bóng 3 lớp, nhấn lún `scale(.96)`, vạch phân cách mảnh; đo lại thumb khi form hiện + khi resize
- [x] T27 · Hover tab cha giống lúc active (viên trắng nhạt + chữ/icon teal)
- [x] T28 · **Rà soát form ERP** (42 ô + 19 khối, kèm kiểu điều khiển): sửa **9 lỗi** — Model/Code đặt hàng/3 ô thuế thành SELECT + nút [+], BVMT thành checkbox + khoá hệ số, đơn vị bảo hành đúng 3 giá trị, Phụ kiện tiêu chuẩn thành CKEditor, sửa chữ tiêu đề khối
- [x] T29 · Gỡ 2 khối tôi thêm trùng (Đơn vị tính · Thông số cơ bản đã có sẵn dạng bảng) — ghi bài học vào §31b
- [x] T30 · Nhóm **Phân loại**: xếp lại cha → con (Tính chất → Nhóm chức năng → Nhóm sản phẩm → Loại sản phẩm), **cascade thật**, Đặc tính sản phẩm xuống cuối
- [x] T31 · Tab **Mua hàng**: tách 3 khối *Khai báo hải quan · Thuế · Đặt hàng*; % VAT bổ sung nút [+] + dấu `*`
- [x] T32 · Sửa lỗi `datVaiForm` xoá mất trạng thái khoá riêng (cascade + hệ số BVMT)
- [x] T33 · Ô tick / ô chọn vẽ lại theo phong cách Apple (24 ô), animation cùng nhịp easing với segmented control; kiểm không phá công tắc `.sw` có sẵn
- [x] T34 · Đổi lại nhóm Phân loại: **chọn Loại sản phẩm (cấp con), 3 cấp cha tự điền chỉ đọc**; sửa dữ liệu demo cho mỗi loại thuộc đúng 1 nhánh (3/7 loại đang nằm 2 nhánh)
- [x] T35 · Giữ **thứ tự hiển thị cha → con** (3 ô cha tự điền ở hàng 1, Loại sản phẩm + Đặc tính ở hàng 2) trong khi cách nhập vẫn là chọn cấp con

### Checkpoint — 28/09/2026 (WRAP UP cuối session)

**Vừa hoàn thành — 7 đợt việc, tất cả nằm trong mockup + tài liệu, KHÔNG đụng source:**

1. **§29 · Phiếu tính giá cho hàng lấy từ công ty khác** — 4 màn (Yêu cầu tính giá + form · Phiếu
   tính giá + form 3 tab) + 2 popup (*Tạm tính giá mua* · *Chọn yêu cầu tính giá*). Dựng lại đúng
   phiếu thật **PTG-03178** ⇒ Giá nhập kho **13,108,986** khớp từng đồng với DB.
2. **§29g · Gỡ tab "Giá bán"** khỏi form hàng hoá (mọi hàng tính giá bằng chứng từ), nối lại 3 lối
   vào cũ để không có nút chết.
3. **§30 · Sửa spec cây 4 cấp lĩnh vực** — không bỏ nữa: bỏ màn *Lĩnh vực*, thay gốc bằng **Lĩnh vực
   Công ty kinh doanh** (HRM, có sẵn), 3 danh mục còn lại sang HRM (**Phase 2d** mới). Bỏ sạch data
   cũ + **11 vấn đề phát sinh** ghi vào §30e và sổ chốt.
4. **§30f/g · 4 cấp catalog vào tab Quản trị hàng hoá** (riêng theo từng công ty, tối thiểu 3 cấp)
   + **form chia 2 tầng tab**.
5. **Giao diện kiểu Apple**: tab cha = **segmented control iOS** (thumb trượt, easing
   `cubic-bezier(.32,.72,0,1)`), tab con = **stepper**, **24 ô tick/ô chọn** vẽ lại theo Apple.
6. **§31 · Rà soát form ERP** (42 ô + 19 khối) — sửa **9 lỗi** sai kiểu/sai chữ.
7. **§32 · Xếp lại nhóm Phân loại + tab Mua hàng** — chốt cuối: **hiển thị cha → con, nhập từ cấp
   con**; tab Mua hàng tách 3 khối đúng việc.

**Đang làm dở:** không có. Mockup `mockup-luong-xay-dung-hang-hoa.html` 269 KB → **325 KB**,
console 0 lỗi. Hai repo `hrm-api` / `hrm-client` **không có thay đổi nào của đợt này** (phần đang
sửa dở là Phòng họp Phase 8 từ session trước).

**Bước tiếp theo:**
1. User duyệt mockup §29 → §32 (xem ở cổng 8899, nhớ **Cmd+Shift+R**).
2. Chốt **4 tồn còn lại của §29f**: gate giá vốn liên công ty · yêu cầu tính giá có cần bước duyệt ·
   phiếu có được gom nhiều công ty quản lý · lưu vết chính sách lúc tính giá.
3. Sau đó gộp với **14 tồn** ở sổ chốt (mục 3 + §26g) thành **một vòng chốt duy nhất** trước khi mở code.

**Blocked:** không.

**Bẫy đã trả giá trong session (đều không sinh lỗi JS, chỉ lộ khi nhìn ảnh):**
`.step` trùng class của Sơ đồ luồng ⇒ mỗi bước bị bọc khung card · `.loi` trùng `.loi{display:none}`
của popup Import ⇒ **3 ô select biến mất** · rà form chỉ quét `v2-label` ⇒ kết luận nhầm "thiếu khối
Đơn vị tính / Thông số cơ bản" rồi thêm trùng · `datVaiForm` quét toàn pane ⇒ **xoá trạng thái khoá
riêng** (cascade + hệ số BVMT) · đo màu **ngay sau khi tick** ra màu cũ vì `transition .18s` chưa xong.

## Đợt §33 — Xây dựng catalog kinh doanh (29/09/2026)

- [x] T36 · Hỏi trọn bộ tồn trước khi dựng (4 câu cấu trúc dữ liệu + 6 câu nhỏ), ghi 7 đáp án chốt vào design §33a
- [x] T37 · Đổi mô hình dữ liệu catalog: `cat[<công ty>]` từ **1 nhánh** thành **danh sách nhánh**, mỗi nhánh đủ 4 cấp
- [x] T38 · Bổ sung **Cụm công việc cho toàn bộ 17 nhóm** của cây demo (nhóm không có cụm là nhánh chết)
- [x] T39 · Form hàng hoá: khối *Phân loại theo lĩnh vực kinh doanh* → **bảng danh sách nhánh** + hàng "Thêm nhánh"; validate ≥1 nhánh · đủ 4 cấp · chặn trùng · báo lỗi đồng thời
- [x] T40 · Màn MỚI **Kho dữ liệu hàng hoá Công ty** (`sc-kho`): mọi trạng thái, 4 ô lọc catalog + ô tick "chưa xếp", cột *Catalog kinh doanh*, nút *Xây dựng catalog*, thanh thao tác hàng loạt
- [x] T41 · Popup **Xây dựng catalog kinh doanh**: cây 4 cấp có số đếm · 2 tab Thêm/Gỡ · chọn tất cả kết quả lọc · dán danh sách mã · giỏ chờ + Hoàn tác + Lưu một lần · cảnh báo khi đóng lúc chưa lưu
- [x] T42 · Màn *Hàng hoá đang kinh doanh*: điều kiện vào màn (đang kinh doanh **và** đã xếp catalog) · 4 ô lọc catalog lên đầu · dòng nhắc số hàng chưa xếp · **bỏ** nút Xây dựng catalog
- [x] T43 · Sửa 4 lỗi tự bắt được (ô tick làm hỏng cột dính · `nangCapSelect` nuốt bề rộng · `catTam` rò sang hàng hoá khác · ô lọc khoá mất tên trường)
- [x] T44 · Đo bằng Playwright trên trình duyệt thật + chụp 3 ảnh; console 0 lỗi
- [x] T45 · Ghi §33 vào design.md (7 đáp án · 2 điểm đảo §30f/§30g · spec 3 màn · bảng số đo · 4 lỗi · **8 tồn mới**)

### Checkpoint — 29/09/2026 (§33 mockup xong)

**Vừa hoàn thành:** mockup §33 — **1 màn mới** (Kho dữ liệu hàng hoá Công ty) + **1 popup mới**
(Xây dựng catalog kinh doanh) + sửa **2 màn cũ** (Hàng hoá đang kinh doanh · form hàng hoá).
Mockup 325 KB → **388 KB**. Hai repo `hrm-api` / `hrm-client` **không đụng dòng nào** (đúng §22).

**Đang làm dở:** không có.

**Bước tiếp theo:**
1. User duyệt §33 (cổng `http://127.0.0.1:8913`, nhớ Cmd+Shift+R).
2. Gộp **8 tồn mới của §33** (design §33i) với **4 tồn §29f** + **14 tồn** ở sổ chốt ⇒ **26 câu**
   cho một vòng chốt duy nhất trước khi mở code.

**Blocked:** không.

### Vòng 2 §33 — góp ý sau khi user xem mockup (29/09/2026)

- [x] T46 · Bộ lọc màn Kho theo format chuẩn: mặc định **tìm nhanh + 4 cấp catalog**, phần còn lại (Trạng thái + 12 ô) vào *Tìm kiếm nâng cao*
- [x] T47 · Menu + tiêu đề lưới bỏ chữ "Công ty" → **Kho dữ liệu hàng hoá**
- [x] T48 · Cột Catalog chỉ hiện **tên Cụm**, hover bung đủ 4 cấp
- [x] T49 · Mọi ô của 4 lưới danh sách **không xuống dòng** (`nowrap`) + đồng bộ thanh cuộn trên theo `scrollWidth` thật
- [x] T50 · Bỏ dòng barcode dưới Mã hàng
- [x] T51 · Công tắc *Chỉ hàng chưa xếp catalog* lên cùng hàng ô tìm nhanh
- [x] T52 · Bỏ icon menu (hamburger) trên topbar
- [x] T53 · Popup: thêm 4 cột thông tin hàng hoá (Loại sản phẩm · Thương hiệu · ĐVT · Công ty quản lý)
- [x] T54 · Popup: **trần 100 mã/lượt** — chặn ngay lúc tick, *Chọn tất cả N* dừng ở 100, dán mã cũng dừng
- [x] T55 · Popup: phân trang + số dòng/trang (20/50/100) theo khuôn `V2BasePagination`
- [x] T56 · Popup: click ô **Mã hàng / Tên hàng** là tick cả dòng, dòng đang chọn tô nền
- [x] T57 · Popup: đổi thứ tự 2 tab (*Hàng trong cụm* lên trước) + dải **"Đang xem cụm: …"**
- [x] T58 · Popup: khối *Tìm kiếm nâng cao* 10 ô + nút Làm mới
- [x] T59 · Sinh **140 mã demo** + **phân trang thật cho 4 lưới danh sách** (không có thì 3 yêu cầu trên không kiểm được)
- [x] T60 · Đo lại toàn bộ bằng Playwright, chụp 2 ảnh vòng 2; sửa lỗi thanh cuộn trên = 0px khi màn còn ẩn

### Checkpoint — 29/09/2026 (§33 vòng 2)

**Vừa hoàn thành:** 13 góp ý của user + 2 việc kèm (dữ liệu demo, phân trang 4 lưới).
Mockup 388 KB → **403 KB**, console 0 lỗi, vẫn **không đụng dòng source nào**.

**Đang làm dở:** không có.

**Bước tiếp theo:** user duyệt vòng 2 → chốt **26 câu tồn** (14 cũ + 4 của §29f + 8 của §33i) rồi mở code.

**Blocked:** không.

### Vòng 3 §33 (29/09/2026)

- [x] T61 · Popup: mỗi lần mở đều **thu gọn** khối *Tìm kiếm nâng cao* (trạng thái mở của lần trước còn nguyên trên DOM)
- [x] T62 · Popup: nút **mở toàn màn hình** / thu nhỏ (cây + bảng cao theo khổ mới, footer vẫn ghim đáy)
- [x] T63 · Ô lọc toàn hệ thống nhỏ lại **36px → 32px** cho gọn (ô tìm nhanh · `.fsel` · `.adv .ss-box`)

### Checkpoint — 29/09/2026 (§33 vòng 3)

**Vừa hoàn thành:** 3 góp ý vòng 3. Mockup **404 KB**, console 0 lỗi, không đụng source.
**Bước tiếp theo:** user duyệt → chốt 26 câu tồn rồi mở code.
**Blocked:** không.

### Vòng 4 §33 — xếp lại menu (29/09/2026)

- [x] T64 · Xếp lại menu 8 mục theo đúng thứ tự + tên user đưa; đổi luôn tiêu đề trong màn cho khớp
- [x] T65 · **Bỏ hẳn màn "Chờ tính giá"** (nav · section · `veBang2` · `BO_LOC.l2` · `cotHien.l2` · nút *Tính giá* · nhánh giá vốn); nút **Lưu** ở form nay về *Kho hàng hoá Công ty*
- [x] T66 · Dựng **màn mới "Kho dữ liệu hàng hoá"** (toàn bộ hàng hoá mọi công ty): cột *Công ty quản lý* + trạng thái **"Chưa sử dụng"**, nút **Lấy về** từng dòng + lấy hàng loạt, lọc *Chỉ hàng công ty chưa dùng*, phân trang
- [x] T67 · Đổi tên màn kho cũ thành **Kho hàng hoá Công ty**; `nowrap` + thanh cuộn trên cho màn mới
- [x] T68 · Đo lại toàn bộ bằng Playwright, chụp 2 ảnh vòng 4

### Checkpoint — 29/09/2026 (§33 vòng 4)

**Vừa hoàn thành:** menu 8 mục theo đúng danh sách user; bỏ màn *Chờ tính giá*; thêm màn *Kho dữ
liệu hàng hoá* (toàn hệ thống). Mockup **412 KB**, console 0 lỗi, không đụng source.

**Bước tiếp theo:** user duyệt → chốt **28 câu tồn** (26 cũ + 2 mới của vòng 4) rồi mở code.

**Blocked:** không.

- [x] T69 · Giữ cả popup *Xem hàng hoá Công ty khác* lẫn màn *Kho dữ liệu hàng hoá* (user chốt)
- [x] T70 · Chuyển nút **Tính giá** sang màn *Kho hàng hoá Công ty*, chỉ hiện ở trạng thái *Chờ tính giá bán* / *Đang tính giá*; nới cột Hành động 110 → 170px cho màn này

### Vòng 5 §33 (29/09/2026)

- [x] T71 · Bỏ badge số trên menu (7 ô); `veDem()` chuyển sang `datDem()` guard null
- [x] T72 · Menu + tiêu đề: *Kho hàng hoá Công ty* → **Dữ liệu hàng hoá công ty**
- [x] T73 · Thêm **bảng mục lục màn hình** (là gì · dùng để làm gì · dữ liệu lấy vào) vào đầu màn *Ghi chú*: 8 mục menu + 5 màn/popup phụ
- [x] T74 · Bỏ ô lọc **Đơn vị tính** ở mọi màn và 2 popup (cột ĐVT trong bảng vẫn giữ)

### Checkpoint — 29/09/2026 (§33 vòng 5)

**Vừa hoàn thành:** 4 việc vòng 5. Mockup **416 KB**, console 0 lỗi, không đụng source.
**Bước tiếp theo:** user duyệt → chốt 26 câu tồn rồi mở code.
**Blocked:** không.

### Vòng 6 §33 — Yêu cầu tính giá (29/09/2026)

- [x] T75 · Bỏ 2 ô *Thương hiệu* / *Hãng sản xuất* ở khối Thông tin chung của form Phiếu tính giá
- [x] T76 · Bảng hàng hoá của form Yêu cầu tính giá **tự gom nhóm cha–con** theo Thương hiệu – Hãng sản xuất
- [x] T77 · Dòng cha hiện **người tiếp nhận** theo khuôn `Tên - Mã phòng - Mã nhân viên` (bảng phân công `PHU_TRACH`)
- [x] T78 · Tick cha ↔ con + dòng tổng kết theo số nhóm; đo lại bằng Playwright

### Checkpoint — 29/09/2026 (§33 vòng 6)

**Vừa hoàn thành:** yêu cầu tính giá gom nhóm theo thương hiệu, dòng cha hiện người tiếp nhận.
Mockup **421 KB**, console 0 lỗi, không đụng source.
**Bước tiếp theo:** chốt tồn mới — *một yêu cầu nhiều nhóm thì tách nhiều phiếu tính giá hay một
phiếu chung?* ⇒ vòng chốt nay **27 câu**.
**Blocked:** không.

### Vòng 7 §33 — Yêu cầu 1 – n Phiếu tính giá (29/09/2026)

- [x] T79 · Màn danh sách Yêu cầu: cột **Nhóm / Phiếu tính giá** + bung nhóm, mỗi nhóm một dòng (người phụ trách · số phiếu · trạng thái riêng)
- [x] T80 · Nút **Lập phiếu tính giá** chuyển xuống **từng nhóm**; bỏ nút ở cấp yêu cầu
- [x] T81 · Phiếu tính giá mang `brand`: chỉ nạp hàng của nhóm, người lập = người phụ trách, màn danh sách phiếu thêm cột *Thương hiệu – Hãng sản xuất*
- [x] T82 · Yêu cầu chỉ chuyển *Đã tính giá* khi **mọi nhóm** đã duyệt giá
- [x] T83 · Sửa lỗi 3 class nhóm bị lồng trong `tr.nhom-cha` làm mất style ở màn danh sách

### Checkpoint — 29/09/2026 (§33 vòng 7)

**Vừa hoàn thành:** quan hệ Yêu cầu – Phiếu tính giá thành **1 – n** theo nhóm Thương hiệu – Hãng SX.
Mockup **425 KB**, console 0 lỗi, không đụng source.
**Bước tiếp theo:** chốt 3 việc kéo theo (ai được lập phiếu của nhóm · bảng phân công thương hiệu →
người phụ trách lưu ở đâu · đổi người phụ trách thì phiếu cũ xử lý sao) ⇒ vòng chốt **29 câu**.
**Blocked:** không.

### Vòng 8 §33 — Phân công phụ trách hãng SX (29/09/2026)

- [x] T84 · Thay map cứng `PHU_TRACH` bằng bảng phân công `PHAN_CONG` (mô phỏng `assign_employee_manufactures`)
- [x] T85 · **Màn mới "Phân công phụ trách hãng SX"**: Thương hiệu · Hãng SX · Mã hãng · Người phụ trách (select) · Số mã hàng + nút Lưu
- [x] T86 · **Gate nút Lập phiếu tính giá** theo phân công — không phải người phụ trách thì ẩn hẳn nút, hiện chữ "Chờ <tên> lập phiếu"
- [x] T87 · Người lập phiếu lấy theo phân công; đo lại bằng Playwright (giao/thu quyền thấy nút hiện/mất ngay)

### Checkpoint — 29/09/2026 (§33 vòng 8)

**Vừa hoàn thành:** chức năng phân công + gate lập phiếu theo người phụ trách.
Mockup **432 KB**, console 0 lỗi, không đụng source.
**Bước tiếp theo:** user duyệt → chốt **26 câu tồn** rồi mở code (3 việc kéo theo của vòng 7 đã có đáp án).
**Blocked:** không.

### Vòng 9 §33 — cấu trúc phiếu Yêu cầu tính giá (29/09/2026)

- [x] T88 · Thêm cột **STT**; dòng cha đánh **La Mã I–IV**, dòng con đánh **1-2-3** lại từ đầu mỗi nhóm
- [x] T89 · Sửa hàm sinh dữ liệu: trạng thái **lệch pha** với thương hiệu ⇒ 4 nhóm **9 · 8 · 5 · 11** (trước là 2 nhóm ôm hết)
- [x] T90 · Người tiếp nhận + người đang đăng nhập chuyển về **Phòng Xuất nhập khẩu** (`HN_XNK`)
- [x] T91 · **Bỏ màn + menu Phân công phụ trách hãng SX** (HRM đã có sẵn), giữ dữ liệu phân công để gate nút Lập phiếu

### Checkpoint — 29/09/2026 (§33 vòng 9)

**Vừa hoàn thành:** cấu trúc phiếu yêu cầu tính giá theo đúng 5 góp ý + bỏ màn phân công.
Mockup **429 KB**, console 0 lỗi, không đụng source.
**Bước tiếp theo:** user duyệt → chốt **26 câu tồn** rồi mở code.
**Blocked:** không.

### Vòng 10 §33 — popup chọn hàng hoá (29/09/2026)

- [x] T92 · Dữ liệu demo: rót đúng **2 mã "Đang nhập thông tin" cho mỗi thương hiệu** ⇒ 4 nhóm **4·3·3·3**
- [x] T93 · Form Yêu cầu: bảng chỉ chứa hàng **đã chọn**, mỗi dòng có nút **xoá**; thêm nút **Chọn hàng hoá**
- [x] T94 · **Popup chọn hàng hoá** (lọc thương hiệu / công ty · tick · chọn tất cả kết quả lọc · phân trang 20/50/100 · loại trừ mã đã có trong yêu cầu)
- [x] T95 · Đo lại toàn luồng bằng Playwright, chụp 2 ảnh

### Checkpoint — 29/09/2026 (§33 vòng 10)

**Vừa hoàn thành:** popup chọn hàng hoá vào yêu cầu tính giá + cân lại dữ liệu demo.
Mockup **437 KB**, console 0 lỗi, không đụng source.
**Bước tiếp theo:** user duyệt → chốt **26 câu tồn** rồi mở code.
**Blocked:** không.

- [x] T96 · Màn *Kho dữ liệu hàng hoá*: thêm cột **Công ty đang kinh doanh** (chip xanh, 2 công ty đầu + `+N`, ô rỗng để trống)
- [x] T97 · Rót thêm dữ liệu demo nhiều công ty cùng kinh doanh một mã (58 mã 1 cty · 21 mã 2 cty · 7 mã 4 cty)

- [x] T98 · Panel cây 4 cấp: phân cấp bằng **kiểu chữ + đường nối 1px**, cấp 1 chữ HOA dính đầu, badge đếm chỉ ở cấp 4
- [x] T99 · Thêm **số thứ tự phân cấp** `I. · 1. · 1.1 · 1.1.1`, đánh lại theo từng nhánh

### Vòng 13 §33 — chọn catalog bằng 4 cột kiểu ERP (30/09/2026)

- [x] T100 · Khảo sát form nhóm hàng hoá ERP (`catalogs/groups/form.blade.php` + `GroupsController@update`) — kết luận **áp dụng được**, mô hình lưu trùng §33
- [x] T101 · Thay 4 ô select bằng **4 cột checkbox** + ô tìm từng cột + số đang chọn + bảng nhánh đã gắn
- [x] T102 · Bỏ tick cấp trên thì **gỡ nhánh thuộc nó** kèm toast; mở hàng có sẵn nhánh thì tick sẵn 3 cấp trên
- [x] T103 · Validate: tô viền đỏ **cột Cụm** thay cho tô ô select; đo lại toàn bộ bằng Playwright

### Checkpoint — 30/09/2026 (§33 vòng 13)

**Vừa hoàn thành:** phần chọn catalog trong tab *Quản trị hàng hoá* chuyển sang **4 cột kiểu ERP**.
Mockup **443 KB**, console 0 lỗi, không đụng source.
**Bước tiếp theo:** user duyệt → cổng chặn **24 câu tồn** (đã gom sẵn, chờ anh chốt) rồi mở code.
**Blocked:** không.

- [x] T104 · Đổi tên 2 cấp catalog trên toàn giao diện: **Nhóm công việc → Mục**, **Cụm công việc → Tiểu mục** (tên bảng CSDL giữ nguyên); dữ liệu demo bỏ tiền tố "Cụm "

### ✅ CHỐT MOCKUP — 30/09/2026

- [x] T105 · Rà nhất quán 3 file mockup sau đợt đổi tên 2 cấp — **0** chỗ còn chữ cũ
- [x] T106 · Nghiệm thu bản chốt: 8 mục menu + 11 màn + 13 popup, 5 popup chính mở/đóng được, console **0 lỗi** ở cả 2 mockup
- [x] T107 · Ghi §34 "CHỐT MOCKUP" vào design.md (danh mục màn · bảng nghiệm thu · việc còn lại)

### Checkpoint — 30/09/2026 (CHỐT MOCKUP)

**Vừa hoàn thành:** đóng giai đoạn mockup Phase 2. Mockup chính **448 KB** (11 màn + 13 popup),
mockup báo cáo 69 KB. Từ đây không sửa giao diện nữa; muốn đổi thì mở vòng mới.

**Bước tiếp theo:** chốt **24 câu tồn** (5 nhóm A–E, đã gom kèm đề xuất) → viết migration + BE.
Kèm 1 câu phụ: `mockup-hang-hoa.html` (3,2 MB, bản 21/09 đã lỗi thời) xoá hay giữ.

**Blocked:** cổng chặn 2b — chưa chốt tồn thì chưa mở code.

### Checkpoint — 30/09/2026 (WRAP UP cuối session)

**Vừa hoàn thành — §33 chạy trọn 13 vòng góp ý rồi CHỐT MOCKUP (§34):**

1. **§33 vòng 1–8** (29/09): màn *Kho hàng hoá công ty* + popup **Xây dựng catalog** (cây 4 cấp,
   2 tab, trần 100 mã/lượt, dán danh sách mã, giỏ chờ + Lưu một lần) · form hàng hoá đổi sang
   **danh sách nhánh** · màn *Kho dữ liệu hàng hoá* (toàn hệ thống, nút **Lấy về**) · xếp lại menu
   8 mục, **bỏ màn Chờ tính giá** · Yêu cầu tính giá **gom nhóm Thương hiệu – Hãng SX** · quan hệ
   Yêu cầu ↔ Phiếu thành **1 – n** · gate lập phiếu theo **phân công người phụ trách**.
2. **§33 vòng 9–13** (29–30/09): cột STT + số La Mã cho phiếu yêu cầu · **popup chọn hàng hoá** vào
   yêu cầu · cột **Công ty đang kinh doanh** ở màn Kho dữ liệu · panel cây 4 cấp vẽ lại
   (**kiểu chữ + đường nối + số `I. · 1. · 1.1 · 1.1.1`**) · phần chọn catalog trong tab *Quản trị
   hàng hoá* chuyển sang **4 cột kiểu ERP** (bám `catalogs/groups/form.blade.php`).
3. **Đổi tên 2 cấp** toàn giao diện: *Nhóm công việc → **Mục***, *Cụm công việc → **Tiểu mục***
   (tên bảng CSDL giữ nguyên).
4. **CHỐT MOCKUP (§34)**: 11 màn + 13 popup, console **0 lỗi**, 0 chỗ còn tên cấp cũ.
5. Bổ sung spec kỹ thuật vào `docs/superpowers/specs/gop-db/2026-09-21-man-danh-muc-hang-hoa-design.md`
   (CSDL · API · quyền · 4 ràng buộc nghiệp vụ).

**Đang làm dở:** không có. Cả 2 repo `hrm-api` / `hrm-client` **không có thay đổi nào** của đợt này
(đúng §22 — chốt spec + mockup trước, chưa động source).

**Bước tiếp theo:**
1. Chốt **24 câu tồn** (5 nhóm A–E, đã gom kèm đề xuất từng câu).
2. Quyết `mockup-hang-hoa.html` (3,2 MB, bản 21/09 đã lỗi thời) — **xoá hay giữ**.
3. Chốt xong mới mở code: migration → BE → FE.

**Blocked:** cổng chặn 2b — chưa chốt tồn thì chưa viết migration.

**Bẫy đã trả giá trong session (ghi để không lặp):**
`cumKey`/`duongNhanh` nằm cùng khối với 4 ô select cũ ⇒ thay khối là **nuốt mất hàm dùng chung**,
cả trang trắng · kiểm demo mà **dùng lại cổng cũ** thì trình duyệt trả bản cache, tưởng code hỏng ·
sinh dữ liệu demo bằng **nhiều phép `%` cùng chu kỳ** tạo tương quan giả (2 nhóm ôm hết hàng) ·
3 class khai lồng trong `tr.nhom-cha` ⇒ màn danh sách mất sạch style mà số liệu DOM vẫn đúng ·
`veDem()` gán `textContent` vào ô đếm đã gỡ ⇒ `TypeError` chết cả lượt vẽ màn.

### Checkpoint — 30/09/2026 (dựng lại danh sách tồn)

Vừa hoàn thành: dựng lại danh sách tồn trước khi code (bản gom 24 câu phiên trước chỉ nằm trong chat) → lưu `ton-chot-truoc-code.md`: 22 câu A–E kèm đề xuất + hệ quả, 6 câu đã có đáp án suy ra (26g-4, 26g-6, 33i-6, 33i-8, 29f-2, 29f-4), 2 câu phụ.
Đang làm dở: không.
Bước tiếp theo: user trả lời → ghi đáp án vào design.md (mục mới §35) + sổ chốt → migration.
Blocked: cổng chặn 2b.

### Chốt tồn trước code (30/09 – 01/10/2026)

- [x] T108 · Dựng lại danh sách tồn (bản gom phiên trước chỉ nằm trong chat) → `ton-chot-truoc-code.md`
- [x] T109 · Xuất cùng nội dung ra `ton-chot-truoc-code.xlsx` (30 dòng, cột CHỐT nền vàng, lọc theo nhóm)
- [x] T110 · Nhóm A (8 câu CSDL): user đồng ý toàn bộ đề xuất → ghi §35a + cột CHỐT md/xlsx
- [ ] T111 · Nhóm B (3 câu quyền) — đang ở B1; kèm xử lý 4 quyền 1616–1619 của nhánh
- [ ] T112 · Nhóm C (7) · D (2) · E (2) · câu phụ (2) + 6 câu xác nhận
- [ ] T113 · Chốt xong hết → cập nhật spec kỹ thuật → mở code (migration → BE → FE)

### Checkpoint — 01/10/2026 (WRAP UP)

Vừa hoàn thành: danh sách tồn lưu thành file md + xlsx; **nhóm A chốt hết theo đề xuất** (§35a).
Đang làm dở: **B1** — đã phân tích lại (tách quyền theo người dùng, §35b), user muốn làm rõ thêm, chưa nêu điểm nào.
Bước tiếp theo: hỏi user điểm cần làm rõ ở B1 → chốt B1 → B2, B3 (kèm số phận quyền 1616–1619) → C → D → E → câu phụ. Chốt từng câu một, có phân tích.
Blocked: cổng chặn 2b — chưa chốt hết tồn thì chưa mở code.

### Vòng sửa mockup sau chốt — §36 (01/10/2026)

- [x] T114 · Form hàng hoá: card *Thông tin hàng hoá* lên trước card *Phân loại* (tab Thông tin chung)
- [x] T115 · Chuyển *Trọng lượng* + *Kích thước* + card *Thông số cơ bản* sang đầu tab *Thông số kỹ thuật*; giãn hàng còn lại 6 + 6 cột
- [x] T116 · Đo lại bằng Playwright (thứ tự card, vị trí ô, bề rộng hàng, console) + ghi §36a design.md

### Checkpoint — 01/10/2026 (§36a)
Vừa hoàn thành: T114–T118 — xếp lại 2 tab đầu của form hàng hoá (bỏ Mã + Trạng thái, Công ty lên hàng 1, Định mức sang tab Thông số kỹ thuật) + T119–T120 tab Mua hàng + T121 popup Xây dựng catalog + T122 ⓘ nhóm Phân loại + T123–T127 tab Nhóm máy + T128 ⓘ tab Quản trị + T129 ⓘ 2 tab chính.
Đang làm dở: không.
Bước tiếp theo: chờ user góp ý tiếp cho vòng §36; xong vòng thì quay lại chốt tồn (B1 → B2, B3 → C → D → E → câu phụ).
Blocked:

- [x] T117 · Tab Thông tin chung: bỏ ô *Mã hàng hoá* + *Trạng thái*, xếp lại hàng (Tên + Model 6/6, 3 ô tên phụ 4/4/4), gỡ 3 chỗ JS tham chiếu; đo lại bằng Playwright + ghi §36b
- [x] T118 · Công ty quản lý lên hàng 1 (Tên · Model · Công ty 4/4/4); Định mức công lắp đặt sang hàng đầu card Thông số cơ bản (4/4/4); đo lại + ghi §36c
- [x] T119 · Tab Mua hàng: bỏ % giảm giá thanh lý + card Đặt hàng; SL tối thiểu nhập mua lên sau HS Code (4/4/4); đo lại + ghi §36d
- [x] T120 · Tab Mua hàng: bỏ checkbox Tính thuế BVMT, ô Hệ số luôn hiện + không bắt buộc; xếp lại card Thuế (4/4/4 + 6/6); gỡ doiBVMT; đo lại + ghi §36e
- [x] T121 · Popup Xây dựng catalog: bỏ lọc + cột Công ty quản lý; nút mở/thu toàn bộ cây + nút mở/thu từng lĩnh vực; thêm cột STT, Ảnh, Thông số cơ bản (⋯ xem thêm); bảng 1 dòng + cuộn ngang; đo lại + ghi §36f
- [x] T122 · Nhóm Phân loại: icon ⓘ + định nghĩa (nguyên văn CATALOG_TOOLTIPS) cho 5 ô; neo tooltip mép trái tránh bị khung cắt; đo lại + ghi §36g
- [x] T123 · Tab Nhóm máy: bỏ logic cũ (nhóm máy + bảng Máy); chọn 1 mã thiết bị (Tính chất = Thiết bị) ⇒ 4 ô phân loại chỉ đọc + ⓘ; đo lại qua UI thật + ghi §36h
- [x] T124 · Tab Nhóm máy: khối giải thích "Phụ kiện [Tên hàng hoá] sẽ được sử dụng cho toàn bộ…" (tên lấy từ ô Tên, cập nhật khi gõ; nối đường dẫn 4 cấp khi đã chọn thiết bị); đo lại + ghi §36i
- [x] T125 · Tab Nhóm máy: hàng Tên phụ kiện + Model (chỉ đọc, theo ô Tên/Model của form) trên ô Mã thiết bị; sửa 2 lỗi (vòng phân quyền mở khoá ô tự điền · change không bubble); đo lại + ghi §36j
- [x] T126 · Tab Nhóm máy: bỏ 2 ô Tên/Model (§36j) → 1 dòng chữ "Đang khai báo thiết bị sử dụng cho Phụ tùng/phụ kiện: Tên hàng: … - Model: …"; đo lại + ghi §36k
- [x] T127 · Tab Nhóm máy: đổi câu đầu card → "Đang khai báo thiết bị có sử dụng Phụ tùng/phụ kiện: [Tên hàng]" (bỏ Model); đo lại + ghi §36l
- [x] T128 · Tab Quản trị hàng hoá: ⓘ cho 6 trường Dữ liệu quản trị + 4 cột catalog (9 câu đề xuất chờ duyệt, 1 câu nguyên văn CATALOG_TOOLTIPS); mở overflow khung cột để tooltip không bị cắt; đo lại + ghi §36m
- [x] T129 · ⓘ cho 2 tab chính (Thông tin hàng hoá · Quản trị hàng hoá), mở overflow track để tooltip không bị cắt; đo lại + ghi §36n

### Checkpoint — 02/10/2026 (WRAP UP — vòng sửa mockup sau chốt §36)
Vừa hoàn thành: **§36a–§36n, T114–T129** — mở lại mockup sau chốt 30/09, 14 lượt góp ý trên form hàng
hoá + popup Xây dựng catalog: xếp lại tab Thông tin chung / Thông số kỹ thuật / Mua hàng · bỏ Mã +
Trạng thái + % giảm giá thanh lý + checkbox BVMT · popup catalog bỏ lọc Công ty, thêm nút mở/thu cây +
từng lĩnh vực, cột STT · Ảnh · Thông số cơ bản (⋯) · tab Nhóm máy làm lại (chọn 1 mã thiết bị ⇒ 4 cấp
phân loại + câu giải thích) · ⓘ cho nhóm Phân loại, tab Quản trị, 2 tab chính.
Mockup 448 KB → **459 KB**, console 0 lỗi (chỉ 404 favicon của server tạm). Hai repo **không đụng**.
Đang làm dở: không.
Bước tiếp theo: user trả lời **nhóm F** (tồn phát sinh từ §36, đã thêm vào `ton-chot-truoc-code.md`)
+ duyệt **11 câu tooltip đề xuất** (§36m, §36n) → quay lại chốt tồn **B1 → B2, B3 → C → D → E → câu phụ**.
Blocked: cổng chặn 2b — chưa chốt hết tồn thì chưa mở code.
Bẫy ghi lại: 3 khung `overflow:hidden` (`.main`, `.qt-cot`, `.tab-cha2`) cắt tooltip ⓘ im lặng — phải đo
toạ độ `::after` + tìm tổ tiên có overflow, không chỉ nhìn icon có hiện · vòng phân quyền `datVaiForm`
mở khoá cả ô tự điền (đánh dấu `data-chi-doc`) · `nangCapSelect` bắn `change` không bubble ⇒ nghe ở
pha capture · thay chuỗi trùng 2 chỗ (`if (cty && …)`) ⇒ script assert dừng, luôn kèm ngữ cảnh.
