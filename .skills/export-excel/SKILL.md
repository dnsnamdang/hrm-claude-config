# Skill: Export Excel — Header / Footer chuẩn HRM

## Mục đích
Đảm bảo MỌI báo cáo / danh sách xuất Excel trong project có **header và footer giống nhau** (logo, tiêu đề, phần ký tên), tránh mỗi màn một kiểu.

**Phạm vi bắt buộc**: chỉ HEADER và FOOTER. Phần thân bảng (thead/tbody) tự do tuỳ màn.

Khi user yêu cầu:
- "Thêm xuất Excel"
- "Bổ sung export Excel cho màn ..."
- "Tham khảo màn X xuất Excel cho màn Y"

→ Đọc skill này TRƯỚC khi viết code.

---

## Chọn cách triển khai

Tuỳ độ phức tạp, chọn 1 trong 2 cách. **Cả hai đều hợp lệ** miễn là header/footer khớp đặc tả ở phần dưới.

| Cách | Khi nào dùng | Library |
|---|---|---|
| **A. BE Blade view** | Báo cáo có dữ liệu lớn, query phức tạp, cần phân cấp/aggregate ở DB; muốn tập trung logic ở BE; cần dùng lại data từ API report | `maatwebsite/excel` (BE) → FE gọi API `arraybuffer` |
| **B. FE ExcelJS** | Bảng nhỏ vừa; data đã có sẵn ở FE state; không muốn tạo endpoint riêng; cần style/freeze/merge phức tạp khó làm trong blade | `exceljs` + `file-saver` (đã cài sẵn ở `hrm-client/package.json`) |

**Nguyên tắc chọn**: Hỏi user nếu không chắc. Mặc định **ưu tiên cách A (BE blade)** cho các báo cáo, vì:
- Không phụ thuộc state FE (tránh xuất lệch khi user chưa load hết)
- Tận dụng được filter/permission BE
- Một file blade dễ review hơn 200 dòng JS gen excel

Cách B phù hợp khi data đơn giản, đã có đủ ở FE và không cần backend tính lại.

---

## Nguyên tắc bất biến

Bất kể chọn cách A hay B:
1. Header phải có **ảnh header của công ty hiện tại** (lấy từ `companies.header`) + **tiêu đề HOA, font 20, bold, center**
2. Footer phải có **3 dòng "Ngày..." / "Người lập" / "(Ký, họ tên)"** căn giữa vùng 5 cột bên phải
3. Có khoảng trống 60px ở cuối để chừa chỗ ký tay
4. FE luôn dùng `this.$nuxt.$loading.start() / finish()` bao quanh thao tác xuất

### Lấy header công ty (quan trọng)

Mỗi công ty trong hệ thống có ảnh header riêng — KHÔNG hardcode `info-tpe.jpg`.

- Field: `companies.header` (string, có thể là URL S3 đầy đủ hoặc đường dẫn relative)
- Công ty hiện tại của user: `auth()->user()->current_company_role`
- **Fallback** khi công ty chưa cấu hình header: dùng `public_path('images/info-tpe.jpg')`

**Cách A (BE Blade)** — load company trong service rồi truyền xuống blade:

```php
// Trong Service::getExportData()
use Modules\Human\Entities\Company;

private function getCurrentCompanyForExport(): array
{
    $companyId = auth()->user()->current_company_role ?? null;
    if (!$companyId) {
        return ['name' => '', 'header' => null];
    }
    $company = Company::query()->find($companyId);
    if (!$company) {
        return ['name' => '', 'header' => null];
    }
    return [
        'name' => $company->name ?? '',
        'header' => $company->header ?: null,
    ];
}

// return [..., 'company' => $this->getCurrentCompanyForExport()];
```

```blade
@php
    $companyHeader = $data['company']['header'] ?? null;
    if (!empty($companyHeader)) {
        $headerSrc = preg_match('#^https?://#i', $companyHeader)
            ? $companyHeader
            : public_path($companyHeader);
    } else {
        $headerSrc = public_path('images/info-tpe.jpg');
    }
@endphp
...
<tr>
    <td colspan="N" style="width: 100%;">
        {{-- Width ~ N * 80px để bằng độ rộng bảng; height auto giữ tỉ lệ --}}
        <img src="{{ $headerSrc }}" style="width: 1400px; height: auto;" width="1400">
    </td>
</tr>
```

> **Quy ước kích thước**: ảnh header để `width` cố định bằng pixel ≈ tổng độ rộng bảng (rule of thumb: `số_cột × 80px`), `height: auto` để giữ tỉ lệ. KHÔNG dùng `width="100%"` vì PhpSpreadsheet không render đúng. Ví dụ: bảng 12 cột → `width="960"`, bảng 18 cột → `width="1400"`.

**Cách B (FE ExcelJS)** — lấy URL header từ store/profile user, fetch về buffer rồi `addImage`:

```javascript
// Pseudo: this.$store.state.currentCompany.header là URL ảnh header công ty
const headerUrl = this.$store.state.currentCompany?.header
    || '/images/info-tpe.jpg' // fallback

const imgResponse = await this.$axios.get(headerUrl, { responseType: 'arraybuffer' })
const imgId = workbook.addImage({
    buffer: imgResponse.data,
    extension: headerUrl.toLowerCase().endsWith('.png') ? 'png' : 'jpeg',
})
worksheet.addImage(imgId, `A1:${lastColLetter}1`)
```

---

---

# Cách A — BE Blade view

## Bố cục blade view chuẩn

Mọi file `resources/views/exports/*.blade.php` phải tuân theo cấu trúc 4 phần sau:

```
┌──────────────────────────────────┐
│ 1. HTML wrapper + CSS            │
│ 2. HEADER (logo + tiêu đề)       │
│ 3. THEAD + TBODY (dữ liệu)       │
│ 4. FOOTER (ngày + chữ ký)        │
└──────────────────────────────────┘
```

### Template skeleton bắt buộc

```blade
@php
    // Helper format có thể tái sử dụng
    function fmtNumber($value) {
        return number_format((float)($value ?? 0), 0, ',', '.');
    }
    function fmtPercent($value) {
        return number_format((float)($value ?? 0), 1, ',', '.') . '%';
    }

    // Header công ty hiện tại — fallback về logo mặc định
    $companyHeader = $data['company']['header'] ?? null;
    if (!empty($companyHeader)) {
        $headerSrc = preg_match('#^https?://#i', $companyHeader)
            ? $companyHeader
            : public_path($companyHeader);
    } else {
        $headerSrc = public_path('images/info-tpe.jpg');
    }
@endphp
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="{{ public_path('css/pdf.css') }}" rel="stylesheet" type="text/css" />
</head>
<body>
<table style="width:100%">

    {{-- ===== HEADER ===== --}}
    <tr>
        <td colspan="{{ $totalCols }}" style="width: 100%;">
            <img src="{{ $headerSrc }}" style="width: {{ $totalCols * 80 }}px; height: auto;" width="{{ $totalCols * 80 }}">
        </td>
    </tr>
    <tr class="no-border">
        <td colspan="{{ $totalCols }}" style="font-size: 20px; font-weight: bold; text-align: center;">
            {{ $reportTitle }}
        </td>
    </tr>
    <tr><td colspan="{{ $totalCols }}"></td></tr>

    {{-- ===== THEAD ===== --}}
    <thead>
        <tr>
            {{-- ... các <td> header in đậm, background #D9E1F2, border #8EA9DB --}}
        </tr>
    </thead>

    {{-- ===== TBODY ===== --}}
    <tbody>
        @foreach($data as $k => $item)
            <tr>
                {{-- ... cells dữ liệu --}}
            </tr>
        @endforeach
    </tbody>

    {{-- ===== FOOTER ===== --}}
    <tr>
        <td colspan="{{ $totalCols }}" style="height: 20px;"></td>
    </tr>
    <tr>
        <td colspan="{{ $totalCols - 5 }}"></td>
        <td colspan="5" style="text-align: center; font-style: italic;">
            Ngày ..., tháng ..., năm ...
        </td>
    </tr>
    <tr>
        <td colspan="{{ $totalCols - 5 }}"></td>
        <td colspan="5" style="text-align: center; font-weight: bold; font-size: 14px;">
            Người lập
        </td>
    </tr>
    <tr>
        <td colspan="{{ $totalCols - 5 }}"></td>
        <td colspan="5" style="text-align: center; font-style: italic;">
            (Ký, họ tên)
        </td>
    </tr>
    <tr>
        <td colspan="{{ $totalCols }}" style="height: 60px;"></td>
    </tr>

</table>
</body>
</html>
```

> Lưu ý: `{{ $totalCols }}` chỉ là biến giả minh hoạ — thay bằng số nguyên cụ thể (ví dụ `12`, `18`).

---

## Quy ước HEADER (đầu file Excel)

| Phần | Quy tắc |
|---|---|
| Logo | `public_path('images/info-tpe.jpg')` — luôn dùng ảnh này, không thay |
| Vị trí logo | Dòng đầu tiên, `colspan` = tổng số cột bảng |
| Tiêu đề | Dòng thứ 2, `font-size: 20px`, `font-weight: bold`, `text-align: center` |
| Class tiêu đề | `class="no-border"` |
| Khoảng cách | 1 dòng `<tr><td colspan="N"></td></tr>` trống ngăn cách trước thead |
| Tiêu đề viết HOA toàn bộ | Ví dụ: `BÁO CÁO TỔNG HỢP DỰ ÁN TKT THEO PHÒNG BAN - NHÂN VIÊN KD` |

---

## Quy ước FOOTER (cuối file Excel)

| Phần | Quy tắc |
|---|---|
| Khoảng cách trước | `<tr><td colspan="N" style="height: 20px;"></td></tr>` |
| Vùng chữ ký | Chiếm **5 cột bên phải** (`colspan = N - 5` trống + `colspan="5"` cho text) |
| Dòng "Ngày ..., tháng ..., năm ..." | `text-align: center; font-style: italic` |
| Dòng "Người lập" | `text-align: center; font-weight: bold; font-size: 14px` |
| Dòng "(Ký, họ tên)" | `text-align: center; font-style: italic` |
| Khoảng trống cuối | `<tr><td colspan="N" style="height: 60px;"></td></tr>` chừa chỗ ký |

> Nếu bảng có **ít hơn 8 cột**, dùng `colspan = N - 3` thay vì `N - 5` để vùng chữ ký vẫn cân đối.

---

## Quy ước THEAD

| Phần | Quy tắc |
|---|---|
| Background | `#D9E1F2` |
| Border | `1px solid #8EA9DB` |
| Font | `font-weight: bold; text-align: center; vertical-align: middle` |
| Multi-row header | Dùng `rowspan` / `colspan` thay vì wrap text |

## Quy ước TBODY (báo cáo phân cấp)

Dùng background khác nhau cho từng cấp để dễ đọc:

| Cấp | Background | Font |
|---|---|---|
| Tổng (Σ) | `#D1FAE5` | `font-weight: bold` |
| Công ty | `#DBEAFE` | `font-weight: bold` |
| Phòng ban | `#F1F5F9` | `font-weight: bold` |
| Nhân viên / chi tiết | (mặc định trắng) | thường |

Số liệu: `text-align: right`. Tên: `text-align: left` với indent (`    `, `        `) cho cấp con.

---

## BE: Pattern Class Export

File: `hrm-api/app/ExcelExport/{Tên}Export.php`

```php
<?php

namespace App\ExcelExport;

use Illuminate\Contracts\View\View;
use Maatwebsite\Excel\Concerns\FromView;
use Maatwebsite\Excel\Concerns\Exportable;

class TenReportExport implements FromView
{
    use Exportable;

    private $data;

    public function forData($data)
    {
        $this->data = $data;
        return $this;
    }

    public function view(): View
    {
        $data = $this->data;
        return view('exports.ten_report', compact('data'));
    }
}
```

## BE: Pattern Controller

```php
use App\ExcelExport\TenReportExport;
use Maatwebsite\Excel\Facades\Excel;

public function export(Request $request)
{
    try {
        $result = $this->reportService->getExportData($request);

        return Excel::download(
            (new TenReportExport())->forData($result),
            'ten_bao_cao.xls'
        );
    } catch (Exception $e) {
        Log::error('Error exporting: ' . $e->getMessage());
        return $this->responseErrors(
            Response::HTTP_BAD_REQUEST,
            $e->getMessage() ?: 'Lỗi khi xuất Excel'
        );
    }
}
```

## BE: Service method

Phải có `getExportData($request)` riêng — **không phân trang**, lấy toàn bộ data theo filter:

```php
public function getExportData(Request $request): array
{
    $query = $this->buildQuery($request);
    $items = $query->get();
    // ... xử lý gom nhóm nếu cần
    return [...];
}
```

## BE: Route

Thêm vào file routes của module:

```php
Route::get('/export', [Controller::class, 'export']);
```

> Đặt `/export` **trước** route wildcard `/{id}` để tránh bị match sai.

---

## FE: Pattern gọi API export

```javascript
async exportExcel() {
    try {
        this.$nuxt.$loading.start()
        const token = localStorage.getItem('access_token')

        const params = { ...this.buildApiFilters() }
        Object.keys(params).forEach((key) => {
            if (params[key] === '' || params[key] === null || params[key] === undefined) {
                delete params[key]
            }
        })
        delete params.current_page
        delete params.per_page

        const query = buildQueryString(params)
        const response = await this.$axios.get(
            `/api/v1/[module]/[feature]/export${query}`,
            {
                responseType: 'arraybuffer',
                headers: { Authorization: `Bearer ${token}` },
            },
        )

        this.$nuxt.$loading.finish()

        const fileURL = window.URL.createObjectURL(new Blob([response.data]))
        const fileLink = document.createElement('a')
        fileLink.href = fileURL
        fileLink.setAttribute('download', 'ten_file.xls')
        document.body.appendChild(fileLink)
        fileLink.click()

        this.$toasted?.global?.success?.({ message: 'Xuất Excel thành công' })
    } catch (error) {
        this.$nuxt.$loading.finish()
        this.$toasted?.global?.error?.({ message: 'Lỗi khi xuất Excel' })
    }
}
```

> Bỏ `current_page` / `per_page` để export toàn bộ dữ liệu, không bị giới hạn trang.

---

# Cách B — FE ExcelJS

Dùng khi data đã có ở FE state và không cần endpoint BE riêng.

## Imports

```javascript
import ExcelJS from 'exceljs'
import { saveAs } from 'file-saver'
```

## Skeleton hàm exportExcel (FE)

```javascript
async exportExcel() {
    if (!this.rows || !this.rows.length) {
        this.$bvModal.msgBoxOk('Không có dữ liệu để xuất.', { title: 'Thông báo', centered: true })
        return
    }

    try {
        this.$nuxt.$loading.start()

        const totalCols = 12 // ⚠️ Thay bằng tổng số cột thực của bảng
        const lastColLetter = String.fromCharCode(64 + totalCols) // 'L' cho 12 cột
        const workbook = new ExcelJS.Workbook()
        const worksheet = workbook.addWorksheet('Báo cáo')

        // ===== HEADER: Logo =====
        // Logo cần được fetch từ server hoặc base64 sẵn (xem note bên dưới)
        worksheet.mergeCells(`A1:${lastColLetter}1`)
        worksheet.getRow(1).height = 60
        // Nếu có ảnh: worksheet.addImage(imageId, 'A1:[lastColLetter]1')

        // ===== HEADER: Tiêu đề =====
        worksheet.mergeCells(`A2:${lastColLetter}2`)
        const titleCell = worksheet.getCell('A2')
        titleCell.value = 'TÊN BÁO CÁO VIẾT HOA'
        titleCell.font = { bold: true, size: 20, name: 'Times New Roman' }
        titleCell.alignment = { vertical: 'middle', horizontal: 'center' }
        worksheet.getRow(2).height = 28

        // Dòng trống ngăn cách
        worksheet.addRow([])

        // ===== THEAD =====
        const headerRow = worksheet.addRow([/* tên các cột */])
        headerRow.eachCell((cell) => {
            cell.fill = { type: 'pattern', pattern: 'solid', fgColor: { argb: 'FFD9E1F2' } }
            cell.font = { bold: true }
            cell.alignment = { vertical: 'middle', horizontal: 'center', wrapText: true }
            cell.border = {
                top: { style: 'thin', color: { argb: 'FF8EA9DB' } },
                left: { style: 'thin', color: { argb: 'FF8EA9DB' } },
                bottom: { style: 'thin', color: { argb: 'FF8EA9DB' } },
                right: { style: 'thin', color: { argb: 'FF8EA9DB' } },
            }
        })

        // ===== TBODY =====
        this.rows.forEach((item) => {
            worksheet.addRow([/* các giá trị */])
        })

        // ===== FOOTER =====
        const lastDataRowIdx = worksheet.lastRow.number
        // Khoảng trống 20px
        worksheet.getRow(lastDataRowIdx + 1).height = 20

        // Vùng chữ ký 5 cột bên phải
        const signStartCol = totalCols - 4 // cột bắt đầu vùng chữ ký
        const signStartLetter = String.fromCharCode(64 + signStartCol)

        const dateRowIdx = lastDataRowIdx + 2
        worksheet.mergeCells(`${signStartLetter}${dateRowIdx}:${lastColLetter}${dateRowIdx}`)
        const dateCell = worksheet.getCell(`${signStartLetter}${dateRowIdx}`)
        dateCell.value = 'Ngày ..., tháng ..., năm ...'
        dateCell.font = { italic: true }
        dateCell.alignment = { horizontal: 'center' }

        const signerRowIdx = dateRowIdx + 1
        worksheet.mergeCells(`${signStartLetter}${signerRowIdx}:${lastColLetter}${signerRowIdx}`)
        const signerCell = worksheet.getCell(`${signStartLetter}${signerRowIdx}`)
        signerCell.value = 'Người lập'
        signerCell.font = { bold: true, size: 14 }
        signerCell.alignment = { horizontal: 'center' }

        const subRowIdx = dateRowIdx + 2
        worksheet.mergeCells(`${signStartLetter}${subRowIdx}:${lastColLetter}${subRowIdx}`)
        const subCell = worksheet.getCell(`${signStartLetter}${subRowIdx}`)
        subCell.value = '(Ký, họ tên)'
        subCell.font = { italic: true }
        subCell.alignment = { horizontal: 'center' }

        // Khoảng trống cuối 60px chừa chỗ ký
        worksheet.getRow(subRowIdx + 1).height = 60

        // ===== Xuất file =====
        const buffer = await workbook.xlsx.writeBuffer()
        const blob = new Blob([buffer], {
            type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        })
        saveAs(blob, 'ten_bao_cao.xlsx')

        this.$toasted?.global?.success?.({ message: 'Xuất Excel thành công' })
    } catch (error) {
        console.error('Error exporting excel:', error)
        this.$toasted?.global?.error?.({ message: 'Lỗi khi xuất Excel' })
    } finally {
        this.$nuxt.$loading.finish()
    }
}
```

## Lưu ý cách B

- **Logo `info-tpe.jpg`**: ExcelJS yêu cầu image dạng base64/buffer. Hai lựa chọn:
  - Bỏ qua logo (chỉ giữ tiêu đề chữ) — chấp nhận được nếu đã quá phức tạp
  - Fetch ảnh từ public asset rồi `workbook.addImage({ buffer, extension: 'jpeg' })`
- **Quy ước font/màu**: phải khớp BE blade — bold size 20 cho tiêu đề, `#D9E1F2` cho header bg, `#8EA9DB` cho border, italic cho "Ngày..." và "(Ký, họ tên)"
- **Không freeze pane** ở phần header tiêu đề — chỉ freeze ở dòng thead nếu cần
- **Tên file**: luôn `.xlsx` (ExcelJS), khác với cách A là `.xls` (maatwebsite/excel default)

---

## Checklist khi tạo export Excel mới

**Bước 0 — Quyết định cách triển khai**
- [ ] Chọn cách A (BE Blade) hoặc cách B (FE ExcelJS) — xem mục "Chọn cách triển khai" ở đầu skill

**Nếu chọn Cách A (BE Blade):**
1. [ ] Tạo `getExportData()` trong Service (không phân trang)
2. [ ] Tạo method `export()` trong Controller dùng `Maatwebsite\Excel`
3. [ ] Thêm route `GET /export` (đặt trước wildcard)
4. [ ] Tạo class `{Tên}Export.php` trong `app/ExcelExport/`
5. [ ] Tạo blade view trong `resources/views/exports/{ten_file}.blade.php` theo skeleton
6. [ ] FE: hàm `exportExcel()` gọi API kèm `responseType: 'arraybuffer'`

**Nếu chọn Cách B (FE ExcelJS):**
1. [ ] Import `ExcelJS` và `file-saver` ở `<script>`
2. [ ] Viết hàm `exportExcel()` theo skeleton ExcelJS

**Bắt buộc cho cả hai cách:**
- [ ] **Header ảnh**: lấy từ `companies.header` của công ty hiện tại (`auth()->user()->current_company_role`), fallback `images/info-tpe.jpg` — KHÔNG hardcode
- [ ] **Header tiêu đề**: HOA 20px bold center
- [ ] **Footer**: 3 dòng "Ngày..." / "Người lập" / "(Ký, họ tên)" căn giữa vùng 5 cột bên phải + khoảng trống 60px
- [ ] **Thead**: background `#D9E1F2`, border `#8EA9DB`
- [ ] **Tbody**: phân cấp màu nếu là báo cáo nhóm (Tổng `#D1FAE5` / Công ty `#DBEAFE` / Phòng `#F1F5F9`)
- [ ] FE: bao quanh thao tác xuất bằng `this.$nuxt.$loading.start() / finish()`

---

## File tham chiếu (đang dùng đúng pattern)

| File | Vai trò |
|---|---|
| `hrm-api/resources/views/exports/prospective_projects_report.blade.php` | Báo cáo phân cấp 4 cấp, header/footer đầy đủ |
| `hrm-api/resources/views/exports/accept_personnel.blade.php` | Danh sách phẳng, header/footer đầy đủ |
| `hrm-api/app/ExcelExport/AcceptPersonnelExport.php` | Class Export tham khảo |
| `hrm-api/app/ExcelExport/ProspectiveProjectsReportExport.php` | Class Export báo cáo |
| `hrm-client/pages/decision/accept-personnel/index.vue` | FE gọi API export |
| `hrm-client/pages/assign/report/prospective-projects/index.vue` | FE gọi API export báo cáo |

---

## Cách gọi skill

Khi user yêu cầu thêm xuất Excel cho màn nào:

```
@.skills/export-excel/SKILL.md

Thêm xuất Excel cho màn [đường dẫn].
Cấu trúc cột:
- [danh sách cột]
Phân cấp (nếu có): [Tổng → Công ty → Phòng ban → ...]
```

→ Phải tuân thủ skeleton trong skill này, **không tự sáng tạo header/footer khác**.
