# Plan — Bổ sung cột "Phương án xử lý" cho biên bản cuộc họp

> **Người phụ trách:** @khoipv · **Module:** Assign · **Ngày:** 2026-06-05
> Spec: `.plans/meeting-bien-ban-phuong-an-xu-ly/design.md`
> KHÔNG commit/push (theo CLAUDE.md). Đánh `[x]` mỗi task khi xong.

**Goal:** Thêm trường text `solution` (Phương án xử lý, nullable) vào mỗi dòng biên bản cuộc họp, hiển thị sau cột "Nội dung", đồng bộ màn nhập + Excel export + màn in.

**Kiến trúc:** Thêm 1 cột DB → khai báo `fillable` (mass-assign tự lưu qua `syncReports`, Resource trả nguyên `reports` nên không sửa) → thêm rule validation nullable → sửa FE (UI grid + Excel) → fill ô blade in (header đã có sẵn).

---

## Phase 1 — Backend (hrm-api)

### Task 1: Migration thêm cột `solution`

**Files:**
- Create: `hrm-api/Modules/Assign/Database/Migrations/2026_06_05_000001_add_solution_to_meeting_reports_table.php`

- [ ] **Step 1: Tạo file migration** (PHPDoc trên `up()/down()` theo convention project)

```php
<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class AddSolutionToMeetingReportsTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::table('meeting_reports', function (Blueprint $table) {
            $table->text('solution')->nullable()->after('content')
                ->comment('Phương án xử lý');
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::table('meeting_reports', function (Blueprint $table) {
            $table->dropColumn('solution');
        });
    }
}
```

- [ ] **Step 2: Chạy migration**

Run: `cd hrm-api && php artisan migrate`
Expected: `Migrated: ... add_solution_to_meeting_reports_table`. Kiểm tra cột `solution` đã có trong bảng `meeting_reports` (sau cột `content`).

### Task 2: Khai báo `fillable` trong model

**Files:**
- Modify: `hrm-api/Modules/Assign/Entities/Meeting/MeetingReport.php:25-35`

- [ ] **Step 1: Thêm `'solution'` vào `$fillable`** (sau `'content'`)

```php
protected $fillable = [
    'meeting_id',
    'content',
    'solution',
    'proposer_id',
    'proposer_name',
    'proposer_type',
    'executor_id',
    'executor_name',
    'executor_type',
    'expected_deadline'
];
```

> Không sửa `MeetingService::syncReports()` (mass-assign theo fillable) và `MeetingResource` (trả nguyên `$this->reports`).

### Task 3: Thêm rule validation `solution` (nullable) cho 2 request

**Files:**
- Modify: `hrm-api/Modules/Assign/Http/Requests/Meeting/MeetingCreateApiRequest.php:42`
- Modify: `hrm-api/Modules/Assign/Http/Requests/Meeting/MeetingUpdateApiRequest.php:67`

- [ ] **Step 1: MeetingCreateApiRequest — thêm dòng sau `reports.*.content`**

```php
'reports.*.content' => 'required|max:1000',
'reports.*.solution' => 'nullable|string|max:2000',
```

- [ ] **Step 2: MeetingUpdateApiRequest — thêm dòng sau `reports.*.content`**

```php
'reports.*.content' => 'required|max:1000',
'reports.*.solution' => 'nullable|string|max:2000',
```

### Task 4: Fill ô "Phương án xử lý" trong blade màn in

**Files:**
- Modify: `hrm-api/resources/views/exports/meeting_record.blade.php:204`

- [ ] **Step 1: Thay ô `<td>` trống (dòng 204) bằng nội dung `solution`**

Tìm dòng (ngay sau `<td>...content...</td>`):

```blade
<td style="border: 1px solid #000; padding: 8px; font-family: 'Times New Roman', serif; font-size: 13px;"></td>
```

Thay thành:

```blade
<td style="border: 1px solid #000; padding: 8px; font-family: 'Times New Roman', serif; font-size: 13px;">{!! nl2br(e($report->solution ?? '')) !!}</td>
```

> Header cột "Phương án xử lý (Solution plan)" (dòng 193) đã có sẵn, không sửa.

---

## Phase 2 — Frontend (hrm-client)

### Task 5: Thêm cột "Phương án xử lý" vào UI bảng biên bản

**Files:**
- Modify: `hrm-client/pages/assign/meeting/components/MeetingReport.vue` (header ~dòng 41-47, rows ~dòng 50-66, `addReport()` ~dòng 362-373)

- [ ] **Step 1: Header — đổi col Nội dung 5→3, chèn col Phương án 2**

Thay block header (dòng 41-47):

```html
<!-- Header -->
<div class="row header-row px-1">
    <div class="col-1">STT</div>
    <div class="col-3">Nội dung / Vấn đề trao đổi <Required /></div>
    <div class="col-2">Phương án xử lý</div>
    <div class="col-2">Người đề xuất</div>
    <div class="col-2">Người thực hiện <Required /></div>
    <div class="col-2">Hạn dự kiến <Required /></div>
</div>
```

- [ ] **Step 2: Row — đổi col Nội dung 5→3, chèn ô textarea Phương án col-2**

Thay block cột Nội dung (dòng 55-66) bằng cột Nội dung (col-3) + cột Phương án (col-2) ngay sau:

```html
<div class="col-3">
    <V2BaseTextarea
        v-model="r.content"
        rows="2"
        placeholder="Nội dung trao đổi..."
        :disabled="isShow"
    />
    <V2BaseError
        v-if="formError['reports.' + i + '.content']"
        :message="formError['reports.' + i + '.content'][0]"
    />
</div>

<!-- Phương án xử lý -->
<div class="col-2">
    <V2BaseTextarea
        v-model="r.solution"
        rows="2"
        placeholder="Phương án xử lý..."
        :disabled="isShow"
    />
</div>
```

- [ ] **Step 3: `addReport()` — thêm `solution: ''` vào object mặc định**

```javascript
addReport() {
    this.form.reports.push({
        content: '',
        solution: '',
        proposer_id: '',
        proposer_name: '',
        proposer_type: null,
        executor_id: '',
        executor_name: '',
        executor_type: null,
        expected_time: '',
    })
},
```

- [ ] **Step 4: Verify UI** — chạy FE, vào `assign/meeting/create` tab Biên bản → bấm "Thêm dòng": bảng hiện 6 cột đúng thứ tự (STT · Nội dung · Phương án xử lý · Người đề xuất · Người thực hiện · Hạn dự kiến), ô Phương án nhập text được, không có viền đỏ bắt buộc.

### Task 6: Đồng bộ cột "Phương án xử lý" vào Excel export

**Files:**
- Modify: `hrm-client/pages/assign/meeting/components/MeetingReport.vue` — hàm `exportMeetingExcel()` (dòng 381-624)

> Bảng report đổi 5→6 cột (A–F). Các vùng merge trải hết bảng đổi `:E` → `:F`. Rà từng dòng tránh lệch cột.

- [ ] **Step 1: `worksheet.columns` — thêm 1 width cho cột Phương án** (dòng 396-402)

```javascript
worksheet.columns = [
    { width: 15 },
    { width: 50 },
    { width: 40 },
    { width: 24 },
    { width: 24 },
    { width: 18 },
]
```

- [ ] **Step 2: Tiêu đề + các block info/section — đổi `:E` → `:F`**

Đổi tất cả `mergeCells` trải hết chiều ngang bảng từ cột E sang F:
- `worksheet.mergeCells('A1:E1')` → `'A1:F1'` (tiêu đề BIÊN BẢN CUỘC HỌP)
- Trong `infoRows.forEach`: `worksheet.mergeCells(\`B${rowCursor}:E${rowCursor}\`)` → `:F${rowCursor}`
- Block DỰ ÁN: `mergeCells(\`A${rowCursor}:E${rowCursor}\`)` (tiêu đề section) → `:F` ; dòng "Tên dự án": `\`B${rowCursor}:E${rowCursor}\`` → `:F`
- Block BIÊN BẢN CUỘC HỌP section title: `mergeCells(\`A${rowCursor}:E${rowCursor}\`)` → `:F`
- Block KẾT LUẬN: tiêu đề `\`A${rowCursor}:E${rowCursor}\`` → `:F` ; vùng nội dung `\`A${rowCursor}:E${rowCursor + 2}\`` → `:F` ; vòng `for ... c <= 5` → `c <= 6`

> Lưu ý: phần "THÀNH PHẦN THAM DỰ" và "TÀI LIỆU ĐÍNH KÈM" có bảng riêng (3 và 4 cột) — KHÔNG đổi, giữ nguyên `:C` / `A:D`.

- [ ] **Step 3: Header bảng report — 5→6 cột** (dòng 515-524)

```javascript
// 6 cột: A=STT, B=Nội dung, C=Phương án, D=Người đề xuất, E=Người thực hiện, F=Hạn dự kiến
const reportCols = ['A', 'B', 'C', 'D', 'E', 'F']
const reportHeaderTexts = ['STT', 'Nội dung / Vấn đề trao đổi', 'Phương án xử lý', 'Người đề xuất', 'Người thực hiện', 'Hạn dự kiến']
reportCols.forEach((col, i) => {
    const cell = worksheet.getCell(`${col}${rowCursor}`)
    cell.value = reportHeaderTexts[i]
    cell.font = { bold: true }
    cell.alignment = { horizontal: 'center', vertical: 'middle', wrapText: true }
    cell.border = borderThin
    cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFF3F4F6' } }
})
rowCursor += 1
```

- [ ] **Step 4: Dòng dữ liệu report — dịch index cột + thêm `solution`** (dòng 534-549)

```javascript
reports.forEach((item, idx) => {
    worksheet.getCell(`A${rowCursor}`).value = idx + 1
    worksheet.getCell(`A${rowCursor}`).alignment = { horizontal: 'center', vertical: 'top' }
    worksheet.getCell(`B${rowCursor}`).value = this.toPlainText(item.content)
    worksheet.getCell(`B${rowCursor}`).alignment = { vertical: 'top', wrapText: true }
    worksheet.getCell(`C${rowCursor}`).value = this.toPlainText(item.solution)
    worksheet.getCell(`C${rowCursor}`).alignment = { vertical: 'top', wrapText: true }
    worksheet.getCell(`D${rowCursor}`).value = item.proposer_name || ''
    worksheet.getCell(`D${rowCursor}`).alignment = { vertical: 'top', wrapText: true }
    worksheet.getCell(`E${rowCursor}`).value = item.executor_name || ''
    worksheet.getCell(`E${rowCursor}`).alignment = { vertical: 'top', wrapText: true }
    worksheet.getCell(`F${rowCursor}`).value = item.expected_deadline || ''
    worksheet.getCell(`F${rowCursor}`).alignment = { horizontal: 'center', vertical: 'top' }
    reportCols.forEach((col) => {
        worksheet.getCell(`${col}${rowCursor}`).border = borderThin
    })
    rowCursor += 1
})
```

- [ ] **Step 5: Nhánh "Không có biên bản"** (dòng 527-532) — dùng `reportCols` mới (6 cột) nên border tự trải đủ; giữ nguyên `worksheet.getCell(\`B${rowCursor}\`).value = 'Không có biên bản'`. Kiểm tra lại đoạn này không hardcode cột E.

- [ ] **Step 6: Verify Excel** — tạo/mở 1 meeting có ≥1 dòng biên bản (có nhập Phương án xử lý), bấm nút "Excel": file tải về, mở lên thấy cột "Phương án xử lý" nằm giữa "Nội dung" và "Người đề xuất", dữ liệu đúng dòng, không lệch cột, các tiêu đề section merge full chiều ngang (A:F).

---

## Verify tổng (sau khi xong 2 phase)

- [ ] Tạo mới meeting + nhập biên bản có Phương án xử lý → lưu → mở lại (edit): dữ liệu Phương án còn nguyên.
- [ ] Bấm "In" → màn in hiển thị cột "Phương án xử lý" với đúng nội dung đã nhập.
- [ ] Bấm "Excel" → cột Phương án đúng vị trí, đúng dữ liệu.
- [ ] Dòng biên bản để trống Phương án → lưu OK (không bị validate), in/Excel hiển thị ô trống.

## Checkpoint

### Checkpoint — 2026-06-05 (khởi tạo)
Vừa hoàn thành: Brainstorm + design + plan.
Đang làm dở: chưa code.
Bước tiếp theo: Task 1 — tạo migration.
Blocked:

### Checkpoint — 2026-06-05 (CODE DONE)
Vừa hoàn thành: Toàn bộ Task 1-6.
- BE: migration `2026_06_05_000001_add_solution_to_meeting_reports_table` (đã `php artisan migrate` PASS), fillable `solution` (MeetingReport), rule `reports.*.solution => nullable|string|max:2000` (2 request), fill ô `<td>` solution màn in (blade dòng 204). PHP lint 4 file PASS.
- FE: UI bảng (Nội dung col-5→3 + cột Phương án col-2 + addReport thêm `solution:''`), Excel export 5→6 cột (toàn bộ merge full-bảng `:E`→`:F`, `c<=5`→`c<=6`, dữ liệu dịch cột + thêm `toPlainText(item.solution)` ở cột C). Đã grep xác nhận không còn `:E` sót.
Đang làm dở: Không.
Bước tiếp theo: User chạy app verify 4 điểm — (1) nhập+lưu+mở lại còn dữ liệu, (2) In hiện cột Phương án, (3) Excel cột đúng vị trí, (4) để trống Phương án vẫn lưu OK.
Blocked:
