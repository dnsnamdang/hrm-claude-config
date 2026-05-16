# Design Phase 13 — Email khách hàng trên Dự án TKT + Báo giá

**Ngày brainstorm:** 2026-04-20
**Người phụ trách:** @dnsnamdang
**Branch:** `tpe-develop-assign` (cả API + Client)

---

## 1. Scope & Nguyên tắc

### 1.1 Mục tiêu

Bổ sung trường **Email khách hàng** (`customer_email`) vào luồng Dự án TKT → Báo giá:

- Màn **Tạo / Sửa** Dự án: nhập + validate (required, đúng format email).
- Màn **Show** Dự án (`manager.vue`): hiển thị readonly sau trường Địa chỉ.
- Các màn **Báo giá** (edit / show): lấy email đã snapshot từ Dự án, hiển thị readonly.
- Auto-fill email từ master Khách hàng khi user chọn KH.

### 1.2 Quyết định đã chốt qua brainstorming

| # | Điểm | Quyết định |
|---|---|---|
| 1 | Required vs Optional | **Required** + validate format email (Laravel `email` rule). Nhất quán với pattern "Người liên hệ" của Batch 10. |
| 2 | Điểm áp validation | Áp cả **"Lưu nháp"** và **"Gửi duyệt"**. Đảm bảo Project TKT luôn có email → snapshot Quotation luôn đầy đủ. |
| 3 | Auto-fill | Khi chọn master KH → auto-fill `customer_email = customer.email`. Logic auto-fill đã có sẵn trong CustomerInfoSection (dòng 179, 205). User vẫn có thể sửa override. |
| 4 | Snapshot sang Quotation | Theo pattern Batch 10: khi `QuotationService::createFromRequest`, copy `prospective_project.customer_email` → `quotations.customer_email`. Snapshot tại thời điểm tạo, không sync về sau. |
| 5 | Phạm vi hiển thị | Dự án (add/edit/manager/show). Báo giá (edit/show). **KHÔNG** thêm cột list báo giá, **KHÔNG** thêm cột Excel export (YAGNI). |
| 6 | Manager view (`_id/manager.vue`) | Màn này render riêng, không dùng CustomerInfoSection. Thêm row display email ngay sau row Địa chỉ. |

### 1.3 Breaking change

- **Schema:** 1 migration thêm cột `quotations.customer_email VARCHAR(255) NULL` sau `customer_address`.
- **Validation behavior:** Các Project TKT đang active **chưa có email** → lần sau mở edit + Lưu nháp/Gửi duyệt sẽ bị block đến khi user nhập email. Cố ý theo lựa chọn (a). Không chạy backfill tự động.
- **Quotation cũ:** Các báo giá tạo trước migration giữ `customer_email = NULL`, UI hiển thị "—". Không backfill từ prospective_project.

### 1.4 Không làm

- KHÔNG chạy backfill script copy email từ prospective_projects → quotations cũ.
- KHÔNG thêm cột `customer_email` vào list báo giá, list dự án, Excel export.
- KHÔNG validate uniqueness email (KH B2B có thể share email).
- KHÔNG sync 2 chiều: sửa email ở Quotation không cập nhật về Project.
- KHÔNG sửa master table `customers` (schema customer master giữ nguyên).

---

## 2. Data model

### 2.1 Tận dụng schema có sẵn

**Bảng `prospective_projects`** (migration `2025_12_28_202501_create_prospective_projects_table.php` dòng 31):
```php
$table->string('customer_email')->nullable()->comment('Email khách hàng');
```
→ **KHÔNG cần migration mới cho project.**

Entity `ProspectiveProject` đã có `customer_email` trong `$fillable` (dòng 36). Transformer `DetailProspectiveProjectResource` đã expose `customer_email` (dòng 43). → **BE Project KHÔNG cần sửa.**

### 2.2 Migration mới cho Quotation

File: `hrm-api/database/migrations/2026_04_20_100001_add_customer_email_to_quotations.php`

```php
<?php
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class AddCustomerEmailToQuotations extends Migration {
    public function up() {
        Schema::table('quotations', function (Blueprint $t) {
            $t->string('customer_email')->nullable()->after('customer_address')
              ->comment('Email khách hàng (snapshot từ prospective_projects tại thời điểm tạo)');
        });
    }
    public function down() {
        Schema::table('quotations', function (Blueprint $t) {
            $t->dropColumn('customer_email');
        });
    }
}
```

### 2.3 Snapshot chain (end-to-end)

```
customers (master)
    └─ customer.email
         │  auto-fill khi CustomerInfoSection.handleSelectCustomer
         ▼
prospective_projects.customer_email   ← user có thể override trước khi save
    │  snapshot khi QuotationService::createFromRequest
    ▼
quotations.customer_email             ← immutable sau khi tạo
    │  display trên Quotation edit/show
```

---

## 3. Backend changes

### 3.1 Không sửa gì cho Project

Đã có sẵn:
- Migration: `customer_email VARCHAR(255) NULL`
- `ProspectiveProject` entity: fillable + casts
- `DetailProspectiveProjectResource`: expose field

### 3.2 Sửa Quotation

**3.2.1 Entity `Quotation.php`** — thêm `'customer_email'` vào `$fillable`:
```php
protected $fillable = [
    // ...
    'customer_tax_code',
    'customer_address',
    'customer_email',   // NEW
    'customer_contact_name',
    'customer_contact_phone',
    // ...
];
```

**3.2.2 Service `QuotationService::createFromRequest`** — thêm dòng snapshot:
```php
$quotation = Quotation::create([
    // ... field hiện tại ...
    'customer_tax_code' => $project->customer_tax_code,
    'customer_address' => $project->customer_address,
    'customer_email' => $project->customer_email,    // NEW
    'customer_contact_name' => $contact?->fullname,
    'customer_contact_phone' => $contact?->mobile,
    // ...
]);
```

**3.2.3 Transformer `DetailQuotationResource`** — expose `customer_email` (nằm cạnh `customer_tax_code`, `customer_address`):
```php
'customer_tax_code' => $this->customer_tax_code,
'customer_address' => $this->customer_address,
'customer_email' => $this->customer_email,          // NEW
'customer_contact_name' => $this->customer_contact_name,
'customer_contact_phone' => $this->customer_contact_phone,
```

### 3.3 Form Request validation (Project)

**3.3.1 `ProspectiveProjectRequest` (hoặc tương đương)** — thêm rule:
```php
public function rules() {
    return [
        // ...
        'customer_email' => 'required|email|max:255',
        // ...
    ];
}

public function messages() {
    return [
        'customer_email.required' => 'Email khách hàng là bắt buộc',
        'customer_email.email' => 'Email khách hàng không đúng định dạng',
    ];
}
```

Rule áp đồng đều cho cả store (add) và update (edit). Không tách rule theo `is_draft` — FE đã chặn submit khi thiếu email (áp cả Lưu nháp và Gửi duyệt).

---

## 4. Frontend changes — Project TKT

### 4.1 `components/CustomerInfoSection.vue`

**4.1.1 Template** — thêm row input Email sau readonly-box hiển thị customer info (giữa dòng 43 và 45):

```html
<div v-if="formSubmit.customer_id" class="readonly-box readonly-customer-info mb-3">
    <!-- ... existing display ... -->
</div>

<!-- NEW: input Email khách hàng -->
<div class="row">
    <div class="col-md-12 mb-2">
        <V2BaseLabel required>Email khách hàng</V2BaseLabel>
        <V2BaseInput
            v-model="formSubmit.customer_email"
            type="email"
            placeholder="Nhập email khách hàng"
            :disabled="isShow"
        />
        <V2BaseError v-if="formError.customer_email" :message="formError.customer_email" />
    </div>
</div>

<div class="row">
    <div class="col-md-12 mb-2">
        <V2BaseLabel required>Người liên hệ</V2BaseLabel>
        <!-- ... existing select ... -->
    </div>
</div>
```

**4.1.2 Auto-fill logic** — KHÔNG sửa. Logic `updated.customer_email = customerDetail.email || customer.email || ''` ở dòng 179, 205 đã đúng.

### 4.2 `pages/assign/prospective-projects/add.vue`

Trong `submitForm()` (áp cả 2 button "Lưu nháp" + "Gửi duyệt"), thêm validation block ở đầu (trước các validate hiện có):

```js
if (!this.formSubmit.customer_email || !this.formSubmit.customer_email.trim()) {
    this.formError.customer_email = 'Email khách hàng là bắt buộc'
    this.$toast.error('Vui lòng nhập email khách hàng')
    return
}
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
if (!emailRegex.test(this.formSubmit.customer_email.trim())) {
    this.formError.customer_email = 'Email khách hàng không đúng định dạng'
    this.$toast.error('Email khách hàng không đúng định dạng')
    return
}
```

Đặt block này ngay **sau** block validate "Người liên hệ" (đã có từ Batch 10) để giữ thứ tự tương tự field hiển thị.

### 4.3 `pages/assign/prospective-projects/_id/edit.vue`

Cùng logic validate như `add.vue`. Copy-paste block validate trong `submitForm()`.

### 4.4 `pages/assign/prospective-projects/_id/manager.vue` (màn show)

Màn này render riêng, không dùng `CustomerInfoSection.vue`. Tìm row hiển thị "Địa chỉ" → thêm row "Email khách hàng" ngay sau:

```html
<tr>
    <th>Địa chỉ</th>
    <td colspan="3">{{ form.customer_address || '—' }}</td>
</tr>
<!-- NEW -->
<tr>
    <th>Email khách hàng</th>
    <td colspan="3">{{ form.customer_email || '—' }}</td>
</tr>
```

(Layout chính xác — colspan, th/td cấu trúc — tuân theo pattern row "Địa chỉ" hiện có trong file, không ép 2-cột nếu file đang dùng 1-cột full-width.)

### 4.5 `pages/assign/prospective-projects/_id/index.vue` (view show khác)

File này là 1 view show khác của Project (render riêng, không dùng CustomerInfoSection).

**Chốt:** Thêm row display "Email khách hàng" ngay sau row "Địa chỉ" — pattern giống `manager.vue`:

```html
<tr>
    <th>Địa chỉ</th>
    <td colspan="...">{{ form.customer_address || '—' }}</td>
</tr>
<!-- NEW -->
<tr>
    <th>Email khách hàng</th>
    <td colspan="...">{{ form.customer_email || '—' }}</td>
</tr>
```

(colspan và cấu trúc th/td adjust theo layout hiện có của file, không ép nếu file đang dùng layout khác.)

---

## 5. Frontend changes — Báo giá

### 5.1 `pages/assign/quotations/_id/edit.vue`

**Update 2026-04-20:** user yêu cầu "Email cùng row với Địa chỉ" thay vì row riêng. Restructure layout:

```html
<tr>
    <th>MST</th>
    <td colspan="3">{{ item.customer_tax_code || '—' }}</td>
</tr>
<tr>
    <th>Địa chỉ</th>
    <td>{{ item.customer_address || '—' }}</td>
    <th>Email khách hàng</th>
    <td>{{ item.customer_email || '—' }}</td>
</tr>
<tr>
    <th>Người liên hệ</th>
    <td>{{ item.customer_contact_name || '—' }}</td>
    <th>SĐT liên hệ</th>
    <td>{{ item.customer_contact_phone || '—' }}</td>
</tr>
```

Thay đổi:
- MST chuyển sang row riêng, colspan=3.
- Địa chỉ + Email đứng chung 1 row (2 cặp th/td, giữ layout 4 cột).

Chỉ **display readonly**. Người dùng không sửa được email trên báo giá (giống MST/Địa chỉ đã là readonly sau Batch 10).

### 5.2 `pages/assign/quotations/_id/index.vue` (show báo giá)

**Update 2026-04-20:** cũng gộp row.

```html
<tr>
    <th>Địa chỉ</th>
    <td>{{ item.customer_address || '—' }}</td>
    <th>Email khách hàng</th>
    <td>{{ item.customer_email || '—' }}</td>
</tr>
```

Đổi colspan của cell Địa chỉ từ 3 xuống 1; thêm cặp Email bên phải trong cùng row.

---

## 6. Edge cases & Downstream impact

### 6.1 Project TKT đang active chưa có email

- Mở edit → user thấy email rỗng → submit (Lưu nháp hoặc Gửi duyệt) bị block.
- **Cách xử lý:** user nhập email thủ công hoặc chọn lại master KH để auto-fill (nếu KH đã có email).
- **Không chạy backfill tự động** — giữ nguyên hành vi "force user fill khi next edit".

### 6.2 Master KH chưa có email

- Dropdown chọn KH hoạt động bình thường, nhưng auto-fill `customer_email = ''`.
- User phải nhập thủ công trên form Project, HOẶC cập nhật master KH trước.
- Không có logic bắt buộc master KH phải có email (scope này không đụng master).

### 6.3 Quotation tạo trước migration

- `customer_email = NULL` → UI hiển thị "—". Không block việc xem / approve báo giá cũ.
- Không backfill từ `prospective_project.customer_email` vì báo giá cũ có thể đã "frozen" với dữ liệu snapshot khác — giữ immutability.

### 6.4 Email chứa ký tự đặc biệt / Unicode

- Laravel `email` rule default validate RFC 5322 nhẹ. Chấp nhận email chuẩn.
- Không cần validation Unicode đặc biệt (email business Việt Nam thường ASCII).

### 6.5 Multi-email (user nhập nhiều email cách dấu phẩy)

- KHÔNG hỗ trợ. Cột cho 1 email duy nhất. Nếu KH có nhiều email → user chọn 1 chính.

### 6.6 Pattern regex FE vs BE

- FE regex `/^[^\s@]+@[^\s@]+\.[^\s@]+$/` là sanity check nhanh, KHÔNG thay thế BE.
- BE `email` rule của Laravel là source of truth — FE fail thì toast, BE fail thì 422 response.

---

## 7. Test plan

### 7.1 Unit / Integration (BE)

1. Migration chạy clean — `quotations.customer_email` tồn tại, nullable.
2. `QuotationService::createFromRequest` snapshot đúng email từ `prospective_project`.
3. `ProspectiveProjectRequest` validate `customer_email` required + email format.

### 7.2 Manual (FE Project)

- [ ] Tạo Project mới: KH có email → auto-fill, save OK.
- [ ] Tạo Project mới: KH không có email → input rỗng, submit Lưu nháp → toast "Email khách hàng là bắt buộc".
- [ ] Tạo Project mới: nhập `abc@` → submit → toast "không đúng định dạng".
- [ ] Tạo Project mới: nhập `valid@company.com` → submit Lưu nháp OK.
- [ ] Tạo Project mới: nhập email → submit Gửi duyệt OK.
- [ ] Sửa Project cũ chưa có email: mở edit → email rỗng → không Lưu được đến khi nhập.
- [ ] Show manager.vue: hiện row "Email khách hàng" sau Địa chỉ, giá trị đúng, không có input.

### 7.3 Manual (FE Quotation)

- [ ] Tạo YCBG từ Project (đã có email) → Quotation mới → mở edit → thấy row "Email khách hàng" đúng giá trị snapshot.
- [ ] Show báo giá cũ (trước migration) → row "Email khách hàng" hiện "—".
- [ ] Edit báo giá: không có input sửa email — chỉ readonly display.
- [ ] Đổi email trên Project (sau khi đã tạo Quotation) → Quotation cũ **không đổi**, Quotation mới tạo sau mới lấy email mới.

---

## 8. Rollout & Rollback

**Rollout:**
1. Deploy code BE + FE.
2. Chạy migration: `php artisan migrate`.
3. Không backfill data.
4. Thông báo team: các Project TKT đang active nếu thiếu email sẽ bị block khi edit lần kế tiếp — cần nhập email.

**Rollback:**
1. `php artisan migrate:rollback` (drop `quotations.customer_email`).
2. Revert code FE + BE.
3. Dữ liệu `prospective_projects.customer_email` giữ nguyên (cột có sẵn từ đầu project).

---

## 9. Reference

- Pattern Batch 10 (plan-phase12 Task 54-57): MST + Người liên hệ + SĐT liên hệ snapshot. Follow y hệt kiến trúc.
- Migration `2025_12_28_202501_create_prospective_projects_table.php` dòng 31: `customer_email` có sẵn.
- `CustomerInfoSection.vue` dòng 151, 179, 205: data + auto-fill logic sẵn sàng.
