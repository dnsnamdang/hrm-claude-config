# Spec — Khảo sát nhu cầu KH: đổi nguồn sang Lĩnh vực kinh doanh nội bộ + nhập theo Nhóm ngành

- **Feature**: `meeting-tim-hieu-gioi-thieu-sp` (đợt cập nhật 2)
- **Ngày**: 2026-08-23
- **Người phụ trách**: @dnsnamdang
- **Nhánh**: `tpe` — nhánh này đã chứa **cả hai** phần phụ thuộc: feature khảo sát (merge từ `meeting-by-market`, hrm-api `5ae177a2` / hrm-client `0a9734b6`) và 2 danh mục mới (commit `linhvucnoibo + sua nhom ngành`, hrm-api `4bb78bc5` / hrm-client `4361be0e`). Không phải chờ merge thêm nhánh nào.
- **Module**: `Modules/Assign` (BE) · `pages/assign/meeting` (FE)
- **Spec gốc của feature**: `docs/superpowers/specs/2026-08-21-meeting-tim-hieu-gioi-thieu-sp-design.md` — spec này **thay thế** mục 3 (nguồn lĩnh vực) và mục 9 (mức đầu tư/thời gian) của bảng quyết định trong spec gốc.

---

## 1. Mục tiêu

Khối **Khảo sát nhu cầu khách hàng** ở tab Biên bản (chỉ hiện với loại meeting "Họp tìm hiểu & Giới thiệu sản phẩm") đổi 2 điểm:

1. Danh mục **Lĩnh vực** không đọc bảng `scopes` bên ERP (`mysql2`) nữa, mà đọc **`internal_business_scopes`** (Danh mục *Lĩnh vực kinh doanh nội bộ*, DB HRM).
2. Bổ sung cấp **Nhóm ngành** (`scopes` HRM — danh mục con của Lĩnh vực kinh doanh nội bộ). Khách chọn **nhóm ngành**, và **Mức đầu tư dự kiến + Thời gian dự kiến bắt đầu nhập ở cấp Nhóm ngành**, không còn ở cấp Lĩnh vực.

Hệ quả: khối khảo sát **bỏ hoàn toàn phụ thuộc connection `mysql2`**.

## 2. Quyết định đã chốt (brainstorming 2026-08-23)

| # | Vấn đề | Chốt |
|---|--------|------|
| 1 | Nguồn danh mục Lĩnh vực | `internal_business_scopes` (HRM, connection mặc định). Bỏ `TpScope` / `mysql2` |
| 2 | Vị trí câu hỏi Nhóm ngành | **Không** thêm câu hỏi thứ 4. Nhóm ngành là **cột trong bảng của câu 2**, mỗi dòng chỉ thuộc đúng lĩnh vực cha của nó |
| 3 | Cấp nhập Mức đầu tư + Thời gian | **Cấp Nhóm ngành** (đổi so với spec gốc — trước ở cấp Lĩnh vực) |
| 4 | Bố cục bảng | **1 bảng phẳng**, mỗi dòng = 1 nhóm ngành; Lĩnh vực gom dòng kiểu rowspan (chỉ hiện tên ở dòng đầu của nhóm) |
| 5 | Cấp tích chọn | Tích ở **cấp Nhóm ngành**. Lĩnh vực chỉ là nhãn gom nhóm, coi như "được quan tâm" khi có ≥1 nhóm ngành con được tích |
| 6 | Nhóm ngành bắt buộc khi Hoàn thành? | **Có** — cùng mức bắt buộc với Mức đầu tư / Thời gian (`status = 3`) |
| 7 | Xử lý dữ liệu khảo sát cũ | **Xoá sạch** — `scope_id` cũ trỏ bảng ERP, không map sang danh mục nội bộ được. Feature chưa lên production |
| 8 | Cách đổi schema | **Migration mới** (`2026_08_23_000001`), KHÔNG sửa lại 3 migration `2026_08_21_*` đã chạy trên `hrm_tpe` / `hrm_erp` |
| 9 | Lĩnh vực chưa có nhóm ngành con Hoạt động | **Không hiện dòng nào** trong bảng (coi như chưa dùng được) |
| 10 | Bảng rỗng (cả danh mục không có nhóm ngành nào) | **Bỏ qua ràng buộc "chọn ít nhất 1"** để không kẹt màn Hoàn thành |
| 11 | Số thứ tự câu hỏi | Giữ nguyên **1 – 2 – 3** ở cả màn hình lẫn bản in |
| 12 | Xuất Excel | **File Excel biên bản** (sinh ở FE bằng ExcelJS trong `MeetingReport.vue`) **phải thêm cột Nhóm ngành** giống bản in. `MeetingController::export()` (Excel *danh sách cuộc họp*, `MeetingExport`) **không đụng** — file đó không chứa khảo sát |

## 3. Hiện trạng đã rà thực tế

### 3.1 Danh mục nguồn

| Bảng | Vai trò | Cột dùng đến |
|------|---------|--------------|
| `internal_business_scopes` | Lĩnh vực kinh doanh nội bộ | `id, code, name, status` (1 = Hoạt động, 2 = Khoá) |
| `scopes` | Nhóm ngành | `id, code, name, status, internal_business_scope_id` |

- `scopes.internal_business_scope_id`: nullable ở tầng schema, **bắt buộc do BE validate**; migration `2026_08_22_000002` đã backfill toàn bộ bản ghi cũ về `LVKDNB.KHAC` ("Khác") → thực tế mọi nhóm ngành đều có lĩnh vực cha.
- Quan hệ đã có sẵn: `InternalBusinessScope::scopes()` (hasMany) và `Scope::internalBusinessScope()` (belongsTo).
- 2 endpoint `getAll` của cả hai danh mục **không gắn `checkPermission`** → không phải nới quyền cho người dùng meeting.

### 3.2 Toàn bộ điểm chạm hiện tại của khối khảo sát

Rà bằng `grep -rn "investment_demands\|TpScope"` — danh sách đóng, không sót:

**hrm-api**
| File | Vai trò hiện tại |
|------|------------------|
| `Modules/Assign/Database/Migrations/2026_08_21_000003_create_meeting_investment_demands_table.php` | Tạo bảng chi tiết (giữ nguyên, không sửa) |
| `Modules/Assign/Entities/Meeting/MeetingInvestmentDemand.php` | Model, `$fillable`, cast `expected_start_date` |
| `Modules/Assign/Entities/Meeting/Meeting.php:249` | Relation `investment_demands()` order theo `position`; `requiresInvestmentSurvey()` |
| `Modules/Assign/Entities/TpScope.php` | Model ERP `scopes` qua `mysql2` — **chỉ feature này dùng** |
| `Modules/Assign/Http/Controllers/Api/V1/MeetingController.php:528` | `investmentScopes()` — endpoint danh mục |
| `Modules/Assign/Services/MeetingService.php:126` | `syncInvestmentDemands()` — xoá hết rồi ghi lại, snapshot tên |
| `Modules/Assign/Http/Requests/Meeting/MeetingCreateApiRequest.php:73` | Rule khi loại meeting cần khảo sát |
| `Modules/Assign/Http/Requests/Meeting/MeetingUpdateApiRequest.php:148` | Rule + `after()` closure bắt buộc khi `status = 3` |
| `Modules/Assign/Transformers/MeetingResource/MeetingTransformer.php:92` | Trả thẳng collection `investment_demands` |
| `resources/views/exports/meeting_record.blade.php:185-230` | Mục `IV/ 1. Khảo sát`, bảng "1.2 Lĩnh vực đầu tư" |

**hrm-client**
| File | Vai trò hiện tại |
|------|------------------|
| `pages/assign/meeting/components/MeetingInvestmentSurvey.vue` | Toàn bộ khối 3 câu hỏi (394 dòng) |
| `pages/assign/meeting/components/MeetingReport.vue` | Nhúng component, truyền `sectionPrefix`, gọi `loadScopes()` khi mở tab; **và sinh file Excel biên bản** |
| `pages/assign/meeting/components/MeetingForm.vue` | Gom payload lưu |
| `pages/assign/meeting/components/MeetingReport.vue:744-810` | Sinh **file Excel biên bản** bằng ExcelJS — có sẵn bảng "2. Lĩnh vực đầu tư" 4 cột |
| `store/optionsSelect.js:445` | Action `fetchInvestmentScopes` + cache `investmentScopes` |

**e2e**: `e2e/tests/assign/meeting-investment-survey.spec.ts`

### 3.3 Hành vi hiện có cần giữ nguyên

- **Cache getter vs giá trị return**: getter `getInvestmentScopes` chỉ chứa mục đang hoạt động; mục đã khoá mà bản ghi đang dùng chỉ có trong **giá trị trả về** của action. Component phải dùng giá trị return, không đọc getter (đã có comment cảnh báo trong code, giữ nguyên nguyên tắc này cho cả 2 cấp).
- **Dòng ảo cho bản ghi đã bị xoá**: mục đã lưu mà danh mục xoá mất thì vẫn dựng dòng từ snapshot, cho **bỏ tích** nhưng **không cho tích lại**.
- **Câu 1 = Không** → xoá sạch chi tiết (BE `syncInvestmentDemands` + FE hỏi xác nhận trước khi xoá).
- **FormData không phân biệt mảng rỗng với không gửi field** → BE luôn `delete()` trước khi ghi lại.

## 4. Thiết kế

### 4.1 Endpoint danh mục — `GET assign/meeting/investment-scopes`

Giữ nguyên đường dẫn và tên method `MeetingController::investmentScopes()`, đổi ruột: đọc `internal_business_scopes` + eager-load `scopes` (nhóm ngành) trên **connection mặc định**, trả **cây 2 tầng trong 1 lần gọi**.

```json
[
  {
    "id": 3,
    "name": "Tự động hoá",
    "is_locked": false,
    "industry_groups": [
      { "id": 12, "name": "Dệt may", "is_locked": false },
      { "id": 15, "name": "Ô tô",   "is_locked": true  }
    ]
  }
]
```

Quy tắc dựng:

- Lĩnh vực: `status = STATUS_ACTIVE`, **hoặc** `id ∈ include_ids`.
- Nhóm ngành: `scopes.status = STATUS_ACTIVE`, **hoặc** `id ∈ include_group_ids`; lọc theo `internal_business_scope_id` của lĩnh vực cha.
- **Lĩnh vực không còn nhóm ngành con nào sau khi lọc → loại khỏi kết quả** (quyết định #9).
- `is_locked` = `status !== STATUS_ACTIVE`, tính riêng cho từng cấp.
- Sắp xếp: lĩnh vực theo `id`, nhóm ngành theo `id` (giữ đúng kiểu sắp xếp cũ, ổn định giữa các lần gọi).
- Bỏ `try/catch` trả `503 "Không kết nối được danh mục lĩnh vực bên ERP"` — không còn gọi ERP. Giữ `catch` chung ghi log và trả lỗi chuẩn của repo.

**Tham số**

| Tham số | Ý nghĩa |
|---------|---------|
| `include_ids[]` | id **lĩnh vực** meeting đang dùng — kể cả đã khoá, để màn Sửa không mất giá trị |
| `include_group_ids[]` | id **nhóm ngành** meeting đang dùng — cùng mục đích |

Cả hai chấp nhận mảng hoặc chuỗi phân cách bởi dấu phẩy (giữ nguyên cách chuẩn hoá `include_ids` hiện có).

### 4.2 Schema

`meeting_investment_demands` giữ vai trò "1 dòng = 1 nhóm ngành được chọn":

| Cột | Trước | Sau |
|-----|-------|-----|
| `scope_id` | id ERP `scopes` | **đổi nghĩa** → id nhóm ngành (`scopes` HRM) |
| `scope_name` | snapshot tên lĩnh vực ERP | snapshot tên **nhóm ngành** |
| `internal_business_scope_id` | — | **mới** — id lĩnh vực cha |
| `internal_business_scope_name` | — | **mới** — snapshot tên lĩnh vực cha |
| `expected_amount`, `expected_start_date` | theo lĩnh vực | **theo nhóm ngành** (cột không đổi) |
| `position` | thứ tự lĩnh vực | thứ tự dòng nhóm ngành |
| unique | `(meeting_id, scope_id)` | `(meeting_id, scope_id)` — vẫn đúng vì nhóm ngành là duy nhất toàn hệ thống |

**Migration mới** `hrm-api/Modules/Assign/Database/Migrations/2026_08_23_000001_switch_meeting_investment_demands_to_internal_scopes.php`:

1. `DB::table('meeting_investment_demands')->delete()` — xoá dữ liệu cũ trước khi đổi cột (id trỏ sai bảng).
2. Bỏ unique cũ `(meeting_id, scope_id)` và index `scope_id`.
3. `renameColumn('scope_id', 'internal_business_scope_id')` và `renameColumn('scope_name', 'internal_business_scope_name')` — `doctrine/dbal ^3.2` đã có trong `composer.json`, repo đã dùng `renameColumn` ở migration khác.
4. Thêm lại `scope_id` (unsignedBigInteger, sau `internal_business_scope_name`, comment "Nhom nganh - bang scopes HRM") + `scope_name` (string 255).
5. Dựng lại `unique(['meeting_id', 'scope_id'])` + `index('internal_business_scope_id')` + `index('scope_id')`.
6. `down()` làm ngược lại, cũng xoá sạch dữ liệu trước khi đổi.

**Không đặt FK cứng** cho `scope_id` / `internal_business_scope_id` — giữ đúng kiểu snapshot đang dùng, để xoá danh mục không làm chết biên bản cũ. FK `meeting_id` giữ nguyên `onDelete('cascade')`.

**Không bọc `addColumn`/`renameColumn` trong `DB::transaction`** — MySQL implicit-commit sẽ báo "no active transaction" (đã vấp ở migration `2026_08_22_000002`).

`MeetingInvestmentDemand::$fillable` bổ sung `internal_business_scope_id`, `internal_business_scope_name`; cập nhật docblock (không còn liên quan ERP).

### 4.3 Lưu dữ liệu — `MeetingService::syncInvestmentDemands()`

Giữ khuôn cũ (xoá hết → ghi lại, snapshot 1 lần cho cả mảng, không query trong vòng lặp), đổi phần tra tên:

```php
$scopeIds = array_values(array_filter(array_column($demands, 'scope_id')));
$scopes = empty($scopeIds)
    ? collect()
    : Scope::whereIn('id', $scopeIds)->get(['id', 'name', 'internal_business_scope_id'])->keyBy('id');
$internalById = $scopes->pluck('internal_business_scope_id')->filter()->unique()->values();
$internalNames = InternalBusinessScope::whereIn('id', $internalById)->pluck('name', 'id');
```

Với mỗi dòng:

- `scope_id` lấy từ payload; bỏ qua dòng không có `scope_id`.
- `scope_name` = tên hiện tại trong DB, thiếu thì lấy `scope_name` FE gửi lên (giữ đúng thứ tự ưu tiên cũ).
- **`internal_business_scope_id` BE tự tra từ `scopes.internal_business_scope_id`, ghi đè giá trị FE gửi** — không tin payload, khỏi phải viết rule kiểm chéo cha–con. Nhóm ngành mồ côi (`internal_business_scope_id` NULL) thì ghi NULL + `internal_business_scope_name` lấy từ payload.
- `internal_business_scope_name` = tên hiện tại của lĩnh vực cha, thiếu thì lấy từ payload.
- `position` = chỉ số dòng.

`use Modules\Assign\Entities\TpScope;` được thay bằng `Scope` + `InternalBusinessScope`.

### 4.4 Validate

Sửa cùng lúc ở `MeetingCreateApiRequest` và `MeetingUpdateApiRequest` (2 file đang lặp rule):

```php
$rules['investment_demands']                                = 'nullable|array';
$rules['investment_demands.*.scope_id']                     = 'required|integer|min:1|distinct|exists:scopes,id';
$rules['investment_demands.*.internal_business_scope_id']   = 'nullable|integer';  // BE tự ghi đè
$rules['investment_demands.*.expected_amount']              = 'nullable|numeric|min:0|max:999999999999999999';
$rules['investment_demands.*.expected_start_date']          = 'nullable|date|after_or_equal:today';
```

Bỏ tiền tố `mysql2.` trong rule `exists`.

Thông báo lỗi (`messages()`):

| Key | Nội dung |
|-----|----------|
| `investment_demands.*.scope_id.exists` | Nhóm ngành không tồn tại hoặc đã bị xoá. |
| `investment_demands.*.scope_id.distinct` | Mỗi nhóm ngành chỉ được chọn một lần. |
| `investment_demands.*.expected_start_date.after_or_equal` | Phải lớn hơn hoặc bằng ngày hiện tại. (giữ nguyên) |

Closure `after()` của `MeetingUpdateApiRequest` (chỉ chạy khi `status = 3`):

- `has_investment_demand !== 1` → không kiểm gì thêm (giữ nguyên).
- Không có dòng nào → lỗi `investment_demands`: **"Vui lòng chọn ít nhất một nhóm ngành."**
  **Ngoại lệ (quyết định #10)**: nếu toàn bộ danh mục không có nhóm ngành nào đang Hoạt động (`Scope::where('status', ACTIVE)->doesntExist()`) thì bỏ qua ràng buộc này để không kẹt màn.
- Từng dòng: thiếu `expected_amount` → "Vui lòng nhập mức đầu tư dự kiến."; thiếu `expected_start_date` → "Vui lòng chọn thời gian dự kiến bắt đầu." (giữ nguyên câu chữ, chỉ đổi ngữ cảnh sang cấp nhóm ngành).

### 4.5 Transformer

`MeetingTransformer:92` giữ `'investment_demands' => $meeting->investment_demands` — model đã có sẵn 2 cột mới nên payload tự có. Không cần Resource riêng.

### 4.6 Giao diện — `MeetingInvestmentSurvey.vue`

**Bảng câu 2**, chia 12 cột:

| Cột | Bề rộng | Ghi chú |
|-----|---------|---------|
| Lĩnh vực | `col-3` | Chỉ hiện tên ở **dòng đầu** của mỗi nhóm; các dòng sau để trống |
| Chọn | `col-1` | Checkbox ở **cấp nhóm ngành** |
| Nhóm ngành | `col-3` | Chỉ đọc (tên) |
| Mức đầu tư dự kiến (VNĐ) | `col-3` | `V2BaseCurrencyInput`, disabled khi dòng chưa tích |
| Thời gian dự kiến bắt đầu | `col-2` | `V2BaseDatePicker`, `disablePastDates`, disabled khi dòng chưa tích |

Bảng đang dựng bằng `div.row / col-*` (không phải `<table>`) nên **không có rowspan thật**. Cách làm: mỗi nhóm lĩnh vực thêm class `group-start` cho dòng đầu → `border-top` đậm hơn ngăn giữa 2 nhóm; ô lĩnh vực ở các dòng sau render rỗng. Nhìn ra đúng hiệu ứng rowspan mà không phải đập lại DOM và bộ style `.tbl-bordered` (đang chép chung với `MeetingReport.vue`).

**Cấu trúc `rows` phẳng** (mỗi phần tử = 1 nhóm ngành):

```js
{
  internal_business_scope_id, internal_business_scope_name,
  scope_id, scope_name,
  is_group_start,          // true ở dòng đầu của mỗi lĩnh vực
  is_locked,               // nhóm ngành đã khoá
  missing,                 // dựng từ snapshot vì danh mục đã xoá
  checked, expected_amount, expected_start_date
}
```

- `loadScopes()` gọi action với **cả 2 danh sách id**: `includeIds` (lĩnh vực đã lưu) và `includeGroupIds` (nhóm ngành đã lưu), lấy từ `form.investment_demands`.
- `buildRows()`: duyệt cây trả về → phẳng hoá theo thứ tự lĩnh vực → nhóm ngành; ghép đáp án đã lưu theo `scope_id`. Bản ghi đã lưu mà không có trong cây → **dòng ảo** đặt cuối, gom theo `internal_business_scope_name` snapshot, `missing = true`, checkbox bị khoá không cho tích lại.
- Checkbox disabled khi `isShow || ((missing || is_locked) && !checked)` — giữ nguyên công thức cũ.
- Bỏ tích → xoá luôn `expected_amount` + `expected_start_date` (giữ nguyên `onToggleRow`).
- Câu 1 đổi sang "Không" khi đang có dòng tích → vẫn hỏi xác nhận rồi bỏ tích hết (giữ nguyên `onChangeAnswer1`, chỉ đổi câu chữ hộp thoại sang "nhóm ngành").
- `buildPayload()` trả thêm `internal_business_scope_id` + `internal_business_scope_name` cho mỗi dòng (BE vẫn ghi đè id).
- `errorFor()` / `payloadIndexOf()` giữ nguyên cơ chế map index dòng đã tích → key lỗi BE.

**`store/optionsSelect.js`** — `fetchInvestmentScopes({ includeIds, includeGroupIds })`:

- Ghép query `include_ids[]` + `include_group_ids[]`.
- Map giữ nguyên `id / name / is_locked`, **thêm** `industry_groups`.
- Điều kiện dùng cache phải tính cả nhóm ngành: chỉ dùng cache khi mọi `includeIds` **và** mọi `includeGroupIds` đều đã có trong cache — nếu không sẽ tái lập đúng lỗi "mục đã khoá biến mất khỏi dropdown cho tới khi F5" mà comment trong file đang cảnh báo.
- `SET_INVESTMENT_SCOPES` vẫn chỉ commit mục không khoá (cả 2 cấp), action vẫn **trả về danh sách đầy đủ**.

### 4.7 Bản in — `resources/views/exports/meeting_record.blade.php`

Bảng mục `{{$ivIndex}}.2 Lĩnh vực đầu tư:` thêm cột **Nhóm ngành**, dùng `rowspan` **thật** (blade vốn là `<table>`):

| Cột | Bề rộng |
|-----|---------|
| STT | 6% |
| Lĩnh vực (`rowspan` = số nhóm ngành của lĩnh vực đó) | 27% |
| Nhóm ngành | 27% |
| Mức đầu tư dự kiến (VNĐ) | 22% |
| Thời gian dự kiến bắt đầu | 18% |

- STT đánh theo **dòng nhóm ngành** (1, 2, 3…).
- Gom nhóm trong blade bằng `$meeting->investment_demands->groupBy('internal_business_scope_id')`; nhãn lấy `internal_business_scope_name` (snapshot), rỗng thì để trống.
- Giữ nguyên `number_format($d->expected_amount, 0, ',', ',')` (dấu **phẩy** phân cách nghìn — quyết định #5 của spec gốc) và `format('d/m/Y')`.
- Giữ nguyên đánh số `IV/ 1. Khảo sát` và 3 mục con `1.1 / 1.2 / 1.3`.

### 4.8 File Excel biên bản — `MeetingReport.vue`

Khối `if (this.needInvestmentSurvey)` dựng sheet bằng ExcelJS. Bảng "2. Lĩnh vực đầu tư" đổi từ 4 cột sang **5 cột**:

| Cột | Nội dung |
|-----|----------|
| A | STT (đánh theo dòng nhóm ngành) |
| B | Lĩnh vực |
| C | Nhóm ngành |
| D | Mức đầu tư dự kiến (VNĐ) |
| E | Thời gian dự kiến bắt đầu |

- `surveyCols` đổi từ `['A','B','C','D']` sang `['A','B','C','D','E']`.
- ExcelJS **không gộp ô kiểu rowspan tự động** ở đây → cột B ghi tên lĩnh vực **ở mọi dòng** (không để trống như trên màn hình). Lý do: file Excel để lọc/pivot, ô trống làm hỏng thao tác lọc.
- Giữ nguyên `safeText()` chống formula injection — áp cho **cả** `internal_business_scope_name` và `scope_name`.
- Giữ nguyên cách ghi mức đầu tư: ghi **số** (không phải chuỗi) + `numFmt = '#,##0'`, và điều kiện `!== null && !== undefined` để giá trị 0 vẫn hiện ra "0".
- Nguồn dữ liệu vẫn là `this.$refs.investmentSurvey.buildPayload()` → tự có 2 field mới sau khi sửa `buildPayload()` ở mục 4.6.

## 5. Dọn dẹp kèm theo

- **Xoá** `hrm-api/Modules/Assign/Entities/TpScope.php` — sau thay đổi này không còn chỗ nào dùng (đã kiểm bằng `grep -rn "TpScope"`: chỉ `MeetingController` và `MeetingService`).
- Bỏ 2 dòng `use Modules\Assign\Entities\TpScope;`.
- Không đụng các chỗ khác đang dùng `mysql2` (danh sách khách hàng, tỉnh/thành…) — ngoài phạm vi.

## 6. Kiểm thử

### 6.1 E2E — `e2e/tests/assign/meeting-investment-survey.spec.ts`

Phải sửa: ca cũ khẳng định **"đủ 13 lĩnh vực"** (đếm bản ghi ERP `scopes`) không còn đúng. Thay bằng:

1. Bảng dựng đúng số dòng = tổng số **nhóm ngành đang Hoạt động** có lĩnh vực cha đang Hoạt động (đếm từ DB, không viết cứng).
2. Lĩnh vực chỉ hiện tên ở dòng đầu của nhóm.
3. Tích 1 nhóm ngành → 2 ô Mức đầu tư / Thời gian bật lên; bỏ tích → xoá trắng.
4. `status = 3` mà không tích dòng nào → lỗi "Vui lòng chọn ít nhất một nhóm ngành.".
5. Tích nhưng bỏ trống mức đầu tư / thời gian → lỗi đúng ô.
6. Lưu → mở lại màn Sửa: đúng nhóm ngành, đúng số tiền, đúng ngày, đúng lĩnh vực cha.
7. Nhóm ngành bị khoá sau khi meeting đã lưu → vẫn hiện, cho bỏ tích, **không** cho tích lại.
8. **Ca phân quyền**: người dùng không có quyền meeting → không vào được màn (fail-closed). Người có quyền meeting nhưng **không** có quyền danh mục nhóm ngành → vẫn dựng được bảng (2 endpoint `getAll` ungated, endpoint khảo sát không gắn `checkPermission`).

### 6.2 Kiểm bằng mắt

- Tab Biên bản: bảng 5 cột, hiệu ứng gom nhóm, không dòng nào lẻ cột.
- Bản in: `rowspan` đúng, không vỡ bảng khi 1 lĩnh vực có nhiều nhóm ngành.
- File Excel biên bản: 5 cột, tên lĩnh vực lặp đủ mọi dòng, mức đầu tư vẫn là số (SUM được).
- Cả 3 nơi hiển thị đúng với meeting cũ (dữ liệu khảo sát đã bị xoá → khối rỗng, không lỗi).

## 7. Việc phải làm khi lên môi trường khác

1. Chạy `php artisan migrate` — migration mới **xoá sạch** `meeting_investment_demands`. Môi trường nào đã nhập khảo sát thử thì mất dữ liệu đó (chấp nhận, quyết định #7).
2. Danh mục `internal_business_scopes` + cột `scopes.internal_business_scope_id` phải đã migrate trước (migration `2026_08_22_000001/000002`).
3. Loại meeting hệ thống `SystemMeetingTypesSeeder` vẫn là việc còn treo từ đợt trước — không thuộc spec này nhưng chặn việc test.

## 8. Ngoài phạm vi

- Không đổi 3 câu hỏi, không thêm câu thứ 4.
- Không đụng `MeetingExport` / `MeetingController::export()` (Excel **danh sách cuộc họp**). File **Excel biên bản** thì có sửa — xem mục 4.8.
- Không sửa 6 bug có sẵn đã ghi nhận ở STATUS (crash khi thiếu `work_position`, watcher xoá `meeting_type_id`, `changeStatus` không validate, `print()` thiếu `canView`, `route:list` hỏng, thiếu cảnh báo thoát chưa lưu).
- Không thêm quyền mới.

## 9. Rủi ro

| Rủi ro | Cách chặn |
|--------|-----------|
| `renameColumn` cần `doctrine/dbal` | Đã có `^3.2` trong `composer.json`; repo đã dùng `renameColumn` ở 2 migration khác |
| Cache `optionsSelect` giữ cây cũ → nhóm ngành mới không hiện | Điều kiện dùng cache tính cả `includeGroupIds`; action luôn trả danh sách đầy đủ, component dùng giá trị return chứ không đọc getter |
| Nhóm ngành mồ côi (`internal_business_scope_id` NULL) | Migration `2026_08_22_000002` đã backfill; BE vẫn ghi NULL an toàn thay vì chết |
| Bảng rỗng làm kẹt màn Hoàn thành | Quyết định #10 — bỏ qua ràng buộc khi không có nhóm ngành nào Hoạt động |
| Sửa `div.row/col` làm vỡ style dùng chung | `.tbl-bordered` / `.sec-title` / `.header-row` đang **chép** giữa `MeetingInvestmentSurvey.vue` và `MeetingReport.vue` — sửa bên nào phải soát bên kia |

---

# ĐỢT CẬP NHẬT 2026-08-23 — chọn cặp Lĩnh vực » Nhóm ngành

> **THAY THẾ** mục 4.6 (bảng phẳng 5 cột), 4.7 (bản in `rowspan`) và 4.8 (Excel 5 cột) ở trên. Các mục 4.1–4.5 (endpoint, schema nhóm ngành, service, validate cơ bản, transformer) **giữ nguyên hiệu lực**.
>
> **Nguồn chân lý về hành vi + giao diện**: `.plans/meeting-tim-hieu-gioi-thieu-sp/demo/khao-sat-nhom-nganh.html` — mockup đã được user duyệt 2026-08-23. Mọi chi tiết tương tác không ghi trong spec này thì lấy theo mockup.

## 10. Lý do đổi

Bảng phẳng liệt kê **toàn bộ** nhóm ngành của danh mục (thực tế 22 dòng, sẽ còn tăng) khiến user phải cuộn tìm giữa hàng chục dòng trống chỉ để nhập 2–3 dòng. Đổi sang: **chọn trước bằng select có tìm kiếm, bảng chỉ chứa dòng đã chọn**.

## 11. Quyết định đã chốt (brainstorming 2026-08-23, vòng 2)

| # | Vấn đề | Chốt |
|---|--------|------|
| 1 | Cách chọn | Tái dùng component chung **`components/assign-components/CascadePairSelect.vue`** (đang chạy ở `pages/assign/customers`, `prospective-projects`) — 2 ô: cha = Lĩnh vực kinh doanh nội bộ, con = Nhóm ngành |
| 2 | Bố cục 2 ô | **Xếp dọc** (cha trên, con dưới) |
| 3 | Cascade | Ô con chỉ hiện nhóm ngành thuộc lĩnh vực đã tick ở ô cha; chưa tick cha thì hiện tất cả |
| 4 | Tick con khi chưa tick cha | **Tự thêm lĩnh vực cha** vào ô cha |
| 5 | Lĩnh vực chọn mà chưa có nhóm ngành nào | **Phải nhớ được** khi lưu → cần chỗ lưu riêng (xem mục 12) |
| 6 | Bỏ tick 1 lĩnh vực ở ô cha | Hỏi xác nhận rồi xoá luôn nhóm ngành thuộc lĩnh vực đó (kèm tiền/ngày đã nhập) |
| 7 | Panel ô con | Gom theo lĩnh vực, mỗi lĩnh vực **đóng/mở được**, icon chevron SVG xoay theo trạng thái |
| 8 | Dòng tiêu đề lĩnh vực trong panel con | Icon đóng/mở · checkbox tick cả nhóm · tên · **badge `N/M`** = số nhóm ngành đang chọn / tổng (ẩn khi N = 0) |
| 9 | Nút "Chọn tất cả" ở ô con | Áp cho **cả nhóm đang thu gọn** |
| 10 | Đang gõ tìm kiếm | Nhóm có kết quả khớp **tự bung ra** |
| 11 | Số câu hỏi | **4 câu** (tách riêng câu về mức đầu tư — xem mục 13) |
| 12 | Nút `×` xoá từng dòng trong bảng | **BỎ** — chỉ bỏ chọn qua chip ở ô con hoặc bỏ tick trong panel |
| 13 | Trên bảng | 1 dòng tóm tắt `Đang chọn: N lĩnh vực · M nhóm ngành`, cập nhật realtime |
| 14 | Tiêu đề bảng | Theo chuẩn phân hệ = `components/V2BaseDataTable.vue`: nền `#f8fafc`, viền `1px solid #e5e7eb`, chữ **12px**, padding `6px 8px`, **KHÔNG in hoa**. KHÔNG áp zebra `nth-child(even)` (đánh nhau với dòng nhóm) |

## 12. Schema bổ sung

Bảng mới `meeting_investment_scopes` — **danh sách lĩnh vực user đã chọn**, kể cả lĩnh vực chưa tích nhóm ngành nào:

```
meeting_investment_scopes
  id
  meeting_id                      -- FK meetings.id, onDelete cascade
  internal_business_scope_id      -- KHÔNG FK cứng (giữ kiểu snapshot như bảng demands)
  internal_business_scope_name    -- snapshot tên lúc lưu
  position
  created_by, updated_by, timestamps
  unique(meeting_id, internal_business_scope_id)
  index(internal_business_scope_id)
```

`meeting_investment_demands` **giữ nguyên** cấu trúc sau Phase 6: mỗi dòng = 1 nhóm ngành đã chọn kèm `expected_amount` + `expected_start_date` và snapshot lĩnh vực cha.

Quan hệ mới trên `Meeting`: `investment_scopes()` hasMany, `orderBy('position')`.

Sync theo đúng khuôn `syncInvestmentDemands()`: câu 1 ≠ Có → xoá sạch cả 2 bảng; ngược lại xoá hết rồi ghi lại, snapshot tên tra 1 lần cho cả mảng, không query trong vòng lặp.

## 13. Bố cục 4 câu hỏi

| # | Nội dung | Điều kiện hiện |
|---|----------|----------------|
| 1 | Anh/Chị có nhu cầu đầu tư trong thời gian tới? (Có / Không) | luôn |
| 2 | **Anh/Chị quan tâm tới lĩnh vực và nhóm ngành nào?** + ghi chú `(chọn nhiều — chọn nhóm ngành sẽ tự thêm lĩnh vực tương ứng)` | câu 1 = Có |
| 3 | **Mức đầu tư và thời gian dự kiến triển khai?** → bảng bên dưới là phần trả lời | đã chọn ≥1 nhóm ngành |
| 4 | Anh/Chị có nhu cầu về dịch vụ sửa chữa bảo dưỡng/bảo trì máy móc thiết bị? (Có / Không) | **luôn hiện** — câu độc lập, KHÔNG phụ thuộc câu 1 |

> **Đính chính 2026-08-24**: bản đầu của mục 13 ghi nhầm câu 4 là "câu 1 = Có". Sai. Câu 4 độc lập — BE validate `has_maintenance_demand` bằng `required_if:status,3`, không ràng buộc theo câu 1; ẩn câu 4 khi câu 1 = Không sẽ làm user **kẹt vĩnh viễn** không Hoàn thành được meeting (câu hỏi bị ẩn nhưng vẫn bắt buộc). Spec gốc 2026-08-21 mục 6.2 cũng đặt câu này ngoài khối phụ thuộc câu 1.

Câu 1 chuyển Có → Không khi đang có dữ liệu: hỏi xác nhận rồi xoá sạch (giữ hành vi cũ, dùng `await this.$confirm({...})` — mockup dùng `window.confirm()` chỉ để demo, **bản thật phải dùng `$confirm`**).

## 14. Bảng của câu 3

| Cột | Nội dung |
|-----|----------|
| STT | lĩnh vực = **số La Mã** (I, II…); nhóm ngành = đếm **lại từ 1** trong mỗi lĩnh vực |
| Lĩnh vực / Nhóm ngành | 1 cột chung; tên nhóm ngành **thụt lề** |
| Mức đầu tư dự kiến (VNĐ) | dòng Tổng + dòng lĩnh vực: **chỉ đọc, tự cộng**; dòng nhóm ngành: ô nhập `V2BaseCurrencyInput`, phân cách nghìn bằng **dấu PHẨY** (giữ đúng quyết định #5 của spec gốc và cách `number_format(...,',',',')` của bản in/Excel; mockup hiển thị dấu chấm chỉ vì dùng `toLocaleString('vi-VN')` — mockup không phải nguồn chân lý về format số) |
| Thời gian dự kiến bắt đầu | chỉ ở dòng nhóm ngành, `dd/mm/yyyy`, chặn ngày quá khứ |

Dòng đầu bảng là **`Tổng:`** (đậm) = tổng toàn bộ. Lĩnh vực đã chọn mà chưa có nhóm ngành nào thì **không xuất hiện** trong bảng (vẫn còn chip ở câu 2).

## 15. Validate khi `status = 3`

- Chưa chọn lĩnh vực nào → `Vui lòng chọn ít nhất một lĩnh vực.`
- Chưa chọn nhóm ngành nào → `Vui lòng chọn ít nhất một nhóm ngành.` (giữ ngoại lệ mục 4.4: bỏ qua khi cả danh mục không còn nhóm ngành nào Hoạt động **và** lĩnh vực cha Hoạt động)
- Mỗi dòng đã chọn: bắt buộc Mức đầu tư + Thời gian (giữ nguyên câu chữ cũ)
- **KHÔNG** bắt mỗi lĩnh vực phải có nhóm ngành
- Bấm 1 lần phải hiện **hết** lỗi của mọi ô cùng lúc

## 16. Bản in + Excel

Áp đúng bố cục mục 14: dòng `Tổng:`, dòng lĩnh vực số La Mã, nhóm ngành đếm lại từ 1, cột tiền của lĩnh vực là tổng cộng dồn. Thay hoàn toàn bảng `rowspan` (mục 4.7) và bảng 5 cột (mục 4.8). Excel giữ nguyên nguyên tắc: ghi **số** (không phải chuỗi) + `numFmt '#,##0'`, `safeText()` chống formula injection cho mọi cột tên.

## 17. Vá kèm 1 bug có sẵn (chặn cả E2E lẫn user thật)

`hrm-client/pages/assign/meeting/components/MeetingForm.vue:997` và `:1018` đọc `currentEmployee.info.work_position.name` **không null-guard** → user thiếu chức danh **không mở được màn Sửa meeting** (TypeError làm chết cây component, FE đá sang trang 404). Đã tái hiện thật bằng trình duyệt 2026-08-23 với tài khoản E2E.

Vá tối thiểu: `optional chaining` / kiểm null, fallback chuỗi rỗng. Không đụng gì khác trong hàm.

## 18. Ngoài phạm vi

Không đổi 4 câu hỏi thành cấu hình động; không đụng `MeetingExport` (Excel danh sách cuộc họp); không thêm quyền mới; không sửa 5 bug có sẵn còn lại đã ghi ở STATUS.

---

# ĐỢT TINH CHỈNH UI 2026-08-24 (Phase 8) — thay mục 16

> Thay thế mục 16 (Bản in + Excel) ở trên về **cách trình bày và luồng thao tác**. Bố cục bảng ở mục 14 vẫn giữ nguyên hiệu lực.

## 19. Luồng In — bám chuẩn In của Báo giá

Chuẩn tham chiếu: `components/assign/quotation/QuotationPrintConfigModal.vue` → `QuotationPrintPreview.vue` (xem `pages/assign/quotations/_id/index.vue` cách nối 2 modal).

**2 bước:**

1. **Popup cấu hình** — `components/assign/meeting/MeetingPartsConfigModal.vue` (dùng chung cho cả In lẫn Excel, phân biệt bằng prop `title` / `confirmLabel` / `confirmIcon`). Cho tick chọn **phần nào được in**: Thông tin chung · Dự án (chỉ hiện khi có) · Thành phần tham dự · Biên bản cuộc họp · Tài liệu đính kèm · Khảo sát nhu cầu (chỉ với loại meeting có khảo sát) · Kết luận. Mặc định tick hết, có "Chọn tất cả", nút chính **"Xem trước"**.
2. **Modal xem trước** — `components/assign/meeting/MeetingPrintPreview.vue`: `size="xl"` `centered` `scrollable` `hide-footer` `modal-class="print-preview-modal"`, **nút In nằm trong slot `#modal-title` ngay cạnh tiêu đề**, nội dung render **bằng Vue** trong `<div class="print-content" ref="printContent">`, `printContent()` mở cửa sổ mới rồi `document.write` HTML + CSS `@page`.

**Đánh số**: số La Mã của các mục cấp 1 và số của các mục con trong IV đều phải **đánh lại liên tục** khi bỏ bớt phần — không được thủng số.

## 20. Luồng Xuất Excel

Dùng lại `MeetingPartsConfigModal` với tiêu đề "Cấu hình xuất Excel biên bản" và nút chính **"Xuất Excel"** — bấm là **tải thẳng file**, KHÔNG xem trước. `sectionNumber` trong `exportMeetingExcel()` đánh lại liên tục theo phần được chọn.

## 21. Vị trí nút

Nút **In** và **Xuất Excel** đặt ở **đầu tab Biên bản** (không nằm trong khối "Các nội dung khác" như trước). **Ẩn hẳn** ở màn tạo meeting (`v-if="form.id"`) vì bản in/Excel cần bản ghi đã tồn tại.

## 22. Quy ước trình bày trong form meeting

- Header **mọi** bảng trong form meeting (tất cả các tab): chữ **thường** (không in hoa) + `font-weight: bold`, theo chuẩn `components/V2BaseDataTable.vue`.
- Cột STT: **text thuần, căn giữa** — không dùng ô nhập readonly.
- Câu hỏi và cụm radio Có/Không nằm **cùng một hàng**, căn giữa theo chiều dọc.
- Các câu hỏi con thụt lề so với tiêu đề mục cha.
- Panel "Nhóm ngành": dòng nhóm ngành con thụt lề so với dòng tiêu đề lĩnh vực.
- 2 ô chọn Lĩnh vực / Nhóm ngành nằm **cùng hàng, chia đôi** — dùng `flex: 1 1 0`, KHÔNG đặt cứng `0 0 50%` (`.cps-wrap` có `gap: 12px`, đặt cứng sẽ tràn khung đúng 12px).
- Icon tiêu đề mục trong component con phải khai lại `.text-brand` — `.text-brand` của `MeetingReport.vue` nằm trong `<style scoped>` nên KHÔNG áp xuống component con.

## 23. NỢ KỸ THUẬT — bản in có 2 nguồn

User đã chọn phương án render nội dung xem trước bằng Vue (thay vì nhúng iframe trang in server) để giống chuẩn Báo giá 100%. Hệ quả: bố cục bản in tồn tại ở **2 nơi**:

- `hrm-api/resources/views/exports/meeting_record.blade.php` — bản in THẬT (mở tab in, in từ màn danh sách meeting)
- `hrm-client/components/assign/meeting/MeetingPrintPreview.vue` — bản XEM TRƯỚC

**Sửa bố cục bản in phải sửa cả 2 nơi.** Đã ghi chú chéo ở đầu cả 2 file. Feature này đã từng dính đúng lỗi lệch giữa các bề mặt (màn hình / bản in / Excel), nên đây là rủi ro có thật chứ không phải lo xa.

Ngoài ra: header "Số biên bản / Ngày lập biên bản" ở bản in server lấy từ `print_templates` trong DB (admin cấu hình được), còn bản Vue dựng tĩnh tương đương → đổi print template thì bản xem trước KHÔNG đổi theo.
