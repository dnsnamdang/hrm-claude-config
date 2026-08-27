---
name: export-excel
description: Use when tạo mới hoặc sửa chức năng XUẤT EXCEL ở BE (class `*Export` + blade `exports/*.blade.php` dùng `maatwebsite/excel`), hoặc khi user báo lỗi file .xlsx tải về — thiếu logo công ty, cột quá hẹp/chữ bị cắt, số tiền bị Excel cảnh báo "The number in this cell is formatted as text", số không có dấu phân cách hàng nghìn, dấu ngăn nghìn ra dấu phẩy thay vì dấu chấm, cộng SUM ra 0.
---

# Skill: Export Excel (BE)

Áp dụng cho mọi export dựng bằng **`FromView`** (blade HTML → PhpSpreadsheet) — kiểu đang dùng ở
`Modules/Finance/Exports/*`, `Modules/Assign/Export/*`, `app/ExcelExport/*`.

> Nền tảng phải nhớ: `FromView` đi qua **HTML reader** của PhpSpreadsheet. Reader này **KHÔNG phải
> trình duyệt**: nó bỏ qua hầu hết CSS, quy đổi `width: ..px` theo cách riêng, và quyết định kiểu ô
> (số/chuỗi) chỉ dựa trên **nội dung text** của thẻ `<td>`.

---

## 1. Số tiền / số lượng — SỐ THÔ + `data-format`, KHÔNG `number_format`

Đây là lỗi hay gặp nhất: file tải về mỗi ô tiền có tam giác xanh, hover ra
*"The number in this cell is formatted as text"*, SUM/lọc/pivot không dùng được.

**Nguyên nhân:** reader dùng `DefaultValueBinder`, chỉ chuỗi **thuần số** (dấu chấm thập phân) mới
thành ô kiểu số. `number_format(2135916)` ra `"2,135,916"` → ô kiểu CHUỖI.

**Cách đúng** — in số thô, và khai định dạng ngay trên thẻ `<td>` bằng thuộc tính `data-format`
(PhpSpreadsheet đọc thuộc tính này: `Reader/Html.php` → `processDomElementDataFormat()`):

```php
// ĐÚNG — service dựng bảng bản Excel
$rows .= '<td style="text-align: right" data-format="#,##0">' . $this->excelNumber($money) . '</td>';

// SAI — ô thành chuỗi, Excel cảnh báo
$rows .= '<td style="text-align: right">' . number_format($money) . '</td>';
```

Trong blade cũng vậy:

```blade
<td colspan="2" data-format="#,##0">{{ $data['SO_TIEN'] }}</td>
```

Helper chuẩn (copy `BillIncomePrintService::excelNumber()` / `BillPaymentPrintService::excelNumber()`):

```php
private function excelNumber($value): string
{
    $number = (float) $value;
    $text = number_format($number, 2, '.', '');

    return strpos($text, '.') === false ? $text : rtrim(rtrim($text, '0'), '.');
}
```

**Mã định dạng hay dùng:** `#,##0` (tiền VND) · `#,##0.##` (có thể có phần lẻ) · `#,##0.00`
(luôn 2 số lẻ) · `0%` · `dd/mm/yyyy`.

**Ngoại lệ — ô CỐ Ý là chuỗi:** giá trị in kèm đơn vị/tiền tệ (`"169,374,000 đồng"`,
`"1,000,000 USD"`). Chuỗi này không thuần số nên Excel không cảnh báo → giữ `number_format`,
**không** gắn `data-format`.

### 1a. Mã định dạng gắn theo TỪNG Ô, không dùng chung 1 mã cho cả cột

Cột tiền thường lẫn cả số nguyên (`56546`) lẫn số lẻ (`111961.08`). Gắn chung `#,##0` thì số lẻ bị
làm tròn mất; gắn chung `#,##0.##` thì **số nguyên hiện thừa dấu thập phân**. Quyết định theo chính
giá trị của ô:

```php
/** '' -> blade bỏ luôn thuộc tính `data-format` (ô `_`, ô gạch ngang, ô chữ). */
private function moneyFormat($value): string
{
    if (!is_string($value) || !preg_match('/^-?\d+(\.\d+)?$/', $value)) {
        return '';
    }

    return strpos($value, '.') === false ? '#,##0' : '#,##0.##';
}
```

Bảng dữ liệu động thì sinh sẵn 1 mảng mã định dạng song song với mảng ô (`row_formats` /
`total_formats`) rồi blade gắn thẳng — khuôn `BillPaymentRequestService::moneyFormats()`:

```blade
<td ... @if (!empty($data['row_formats'][$r][$i])) data-format="{{ $data['row_formats'][$r][$i] }}" @endif>{{ $cell }}</td>
```

**Vẫn canh phải tay** cho cột tiền dù ô số Excel tự canh phải: ô placeholder (`_`, `-`) là chuỗi,
Excel canh trái, để nguyên là nó lệch hẳn khỏi cột số bên trên.

### 1b. "Sao dấu ngăn nghìn ra dấu phẩy?" — TUYỆT ĐỐI không chữa bằng cách ghi ô thành chữ

Mã định dạng của `.xlsx` (`#,##0`) **không chứa ký tự ngăn cách**: Excel vẽ bằng ký tự lấy từ
**Windows Regional Settings của máy đang mở file**. Máy đặt kiểu Anh thì ô số luôn ra `60,000` dù
file ghi hoàn toàn đúng chuẩn. Không có mã nào ép được dấu `.` mà vẫn giữ ô là số — `[$-42A]#,##0`,
`#\.##0` đều đã thử và không dùng được cho tiền.

⚠️ **Đã đi đường vòng này một lần rồi, đừng đi lại** (phiếu đề nghị thanh toán):

| | |
| --- | --- |
| 25/08/2026 | Đổi ô tiền sang **CHUỖI** kiểu Việt (`60.000`) để mọi máy ra dấu chấm |
| 26/08/2026 | User báo *"nó bị lỗi is formatted as text"* → **đảo lại về ô SỐ** + `data-format` |

Đổi sang chuỗi là mua đúng 3 thứ: tam giác xanh ở **mọi** ô tiền, mất SUM/lọc/pivot, và cái bẫy ở
mục 1c. Cách chữa đúng khi user chê dấu ngăn cách là **đổi Regional format của Windows sang
Vietnam** (Settings → Time & language → Language & region → Regional format), không phải sửa code.

Cũng đừng mất công tìm cách tắt tam giác xanh bằng `<ignoredErrors numberStoredAsText="1"/>`:
PhpSpreadsheet của dự án là **1.25.2**, API `setIgnoredErrors()` mãi 1.29 mới có. Muốn dùng phải
vá thẳng vào gói `.xlsx` sau khi ghi, và thẻ đó bắt buộc nằm **trước** `<drawing>` (letterhead) theo
schema — sai thứ tự là Excel báo file hỏng.

### 1c. Chuỗi kiểu Việt còn sót lại — phải chặn bằng `WithCustomValueBinder`

`is_numeric('23.000')` là **true** trong PHP (dấu chấm = dấu thập phân), nên bất kỳ chuỗi định dạng
sẵn kiểu Việt nào lọt vào `<td>` đều bị `DefaultValueBinder` biến thành số: ô **Tỷ giá** `23.000`
ra đúng một chữ `23`. Chuỗi nhiều dấu chấm (`3.720.816`) thoát được vì không còn là số hợp lệ →
**lỗi chỉ lộ ở số hàng nghìn tròn trĩnh**, rất dễ lọt review.

Reader không hỗ trợ thuộc tính `data-type` trên `<td>`, phải chặn ở tầng binder:

```php
class XxxExport extends DefaultValueBinder implements FromView, WithCustomValueBinder
{
    /** Chuỗi số kiểu Việt ĐÃ định dạng sẵn: `62.000` · `5.213.456,6` · `196,66`. */
    const MONEY_TEXT = '/^-?(?:\d{1,3}(?:\.\d{3})+(?:,\d+)?|\d+,\d+)$/';

    public function bindValue(Cell $cell, $value): bool
    {
        if (is_string($value) && preg_match(self::MONEY_TEXT, $value)) {
            $cell->setValueExplicit($value, DataType::TYPE_STRING);

            return true;
        }

        return parent::bindValue($cell, $value);
    }
}
```

Regex cố tình **bắt buộc có dấu ngăn cách** để số thô của mục 1 (`60000`, `1234567.5`) đi lọt và vẫn
vào sheet đúng kiểu số. Khuôn: `BillPaymentRequestExport::bindValue()`.

---

## 2. Bản IN và bản EXCEL là 2 nhánh khác nhau — đừng dùng chung hàm dựng HTML

Bản in là HTML hiển thị thẳng trên trình duyệt → **phải** `formatCurrency()` / `number_format()`.
Bản Excel → số thô. Cùng một service thì tách bằng cờ:

```php
private function detailTable(BillPayment $bill, bool $isPrint): string   // pattern có sẵn
private function excelBillPaymentTable(BillPayment $bill): string        // hoặc tách hẳn hàm
```

Sửa nhánh Excel thì **kiểm lại bản in không đổi** (và ngược lại) — 2 nhánh này rất hay dính nhau.

---

## 3. Bề rộng cột — `WithColumnWidths`, KHÔNG đặt `width: ..px` trong `<td>`

Reader quy đổi px sang "ký tự" theo tỉ lệ riêng: `width: 10px` ra **1.43 ký tự**, `width: 50px` ra
**7.14** → cột bé tí, chữ bị cắt. Đây là nguyên nhân thật của lỗi "cột đang hơi bé".

```php
class BillIncomeExport implements FromView, WithColumnWidths
{
    public function columnWidths(): array
    {
        return ['A' => 6, 'B' => 36, 'C' => 26, 'G' => 18, 'H' => 18];
    }
}
```

- Export có **nhiều bố cục** (theo loại chứng từ / số dòng chi tiết) → trả bộ bề rộng khác nhau theo
  bố cục, xem `BillPaymentExport::columnWidths()`.
- `ShouldAutoSize` chỉ hợp với báo cáo dạng bảng phẳng; chứng từ có ô gộp (`colspan`) thì auto-size
  ra kết quả lệch — dùng bề rộng cứng.
- Ô chữ dài (lý do, ghi chú) → thêm wrap text trong `AfterSheet`:
  `$sheet->getStyle('A4:D10')->getAlignment()->setWrapText(true);`

---

## 4. Logo / letterhead công ty — `WithDrawings` + trait dùng chung

Ảnh letterhead là **URL tuyệt đối** lấy từ `companies.header` (dữ liệu `gop_db` đã chuẩn hoá về
tuyệt đối 2026-08-21; `ERP_URL` chỉ còn là lưới an toàn cho giá trị tương đối sót lại), trong khi
HTML reader chỉ nhận ảnh có sẵn trên đĩa → `<img src="...">` trong blade **không bao giờ vào file**.
Phải tải ảnh về rồi chèn bằng `WithDrawings`.

⚠️ **Cách dựng URL đó nằm ở skill `print-page` mục 4b — đọc trước khi viết `HEADER`.** Tóm tắt: lấy
công ty theo `company_id` GHI TRÊN CHỨNG TỪ (không phải người tạo, càng không phải người đăng nhập),
dùng nguyên giá trị `companies.header`, thiếu `ERP_URL` thì trả nguyên path chứ không trả `''`.

Dùng trait có sẵn `Modules\Finance\Exports\Concerns\EmbedsCompanyLetterhead`:

```php
class BillIncomeExport implements FromView, WithEvents, WithDrawings
{
    use EmbedsCompanyLetterhead;

    public function drawings()
    {
        return $this->letterheadDrawings((string) ($this->data['HEADER'] ?? ''));
    }

    public function registerEvents(): array
    {
        return [AfterSheet::class => function (AfterSheet $event) {
            $this->fitLetterheadRow($event->sheet->getDelegate());   // nới cao dòng 1
        }];
    }
}
```

Bắt buộc:
- **Tải lỗi/timeout → bỏ ảnh, KHÔNG ném lỗi.** Thiếu logo là mất thẩm mỹ, ném lỗi là mất cả file.
- Chỉ nới cao dòng khi ảnh **thật sự** vào được (`getDrawingCollection()`), không thì file ra một
  dòng trống cao lêu nghêu.
- Giữ kênh alpha (`imagesavealpha`) — PNG nền trong suốt không giữ alpha sẽ ra **khối đen**.
- Dòng neo ảnh (thường A1) phải là dòng **để trống** trong blade.

---

## 5. `registerEvents()` — KHÔNG trỏ vùng ô tuyệt đối cho dữ liệu động

```php
// SAI — 'E18:E30' tính theo số dòng ERP, bảng nở/co 1 dòng là trượt hết
$sheet->getStyle('E18:E' . (17 + $count))->getNumberFormat()->setFormatCode('###,###,###');
```

Đo thật trên nhánh `gop_db` (2026-08-20) với code port nguyên vùng ô của ERP: phiếu chi 918 cột
"Số tiền đề nghị chi" **không hề được định dạng** ở 6 dòng đầu; phiếu 290 mất định dạng từ dòng 46
và cột "Tổng cộng" thì **không bao giờ** có. Người dùng chỉ thấy "số này có dấu phẩy, số kia không".

→ Định dạng số **luôn** khai bằng `data-format` trên từng ô (mục 1).
`registerEvents()` chỉ nên giữ những thứ **không phụ thuộc số dòng**: chiều cao dòng, wrap text,
freeze pane, kẻ viền vùng tiêu đề cố định.

Cần style theo vùng động thì tính từ chính sheet (`$sheet->getHighestRow()`), đừng tính tay theo
số dòng dữ liệu.

---

## 6. Vặt nhưng hay dính

| Triệu chứng | Nguyên nhân | Cách xử lý |
| --- | --- | --- |
| File tải về là JSON lỗi / 401 | `$axios` không tự đính token | FE gọi qua helper `utils/download-excel.js` |
| Ô hiện `&amp;` | escape 2 lần | Blade `{{ }}` đã escape — service bản Excel **không** `e()` nữa (xem `excelText()`) |
| Bảng vỡ ở ký tự `&` | HTML reader vỡ ở `&` trần | escape bằng `e()` khi nối chuỗi HTML trong service |
| `<br>` không xuống dòng | reader chỉ hiểu đúng `<br>` | chuẩn hoá `preg_replace('/<\/?br\s*>/', '<br>', $html)` |
| CSS ngoài không ăn | reader không đọc `<link>` | style **inline** hết |
| Export báo giá lớn chết timeout | tải ảnh tuần tự | tải song song `curl_multi` (xem `QuotationExcelExport::prefetchImages()`) |

---

## 7. Kiểm chứng TRƯỚC khi báo xong

Không đoán bằng mắt — dựng file thật rồi **đọc lại bằng PhpSpreadsheet**. Script mẫu (chạy trong
thư mục `hrm-api`, để ở scratchpad, không commit):

```php
$sheet = \PhpOffice\PhpSpreadsheet\IOFactory::load($file)->getActiveSheet();
foreach ($sheet->getRowIterator(1, 30) as $row) {
    foreach ($row->getCellIterator() as $cell) {
        if ($cell->getValue() === null || $cell->getValue() === '') continue;
        echo $cell->getCoordinate()
            . ' [' . $cell->getDataType() . ']'                                  // n = số, s = chuỗi
            . ' fmt=' . $cell->getStyle()->getNumberFormat()->getFormatCode()
            . ' shown=' . $cell->getFormattedValue() . "\n";
    }
}
echo 'drawings=' . count($sheet->getDrawingCollection()) . "\n";
foreach (range('A','J') as $c) echo $c . '=' . $sheet->getColumnDimension($c)->getWidth() . ' ';
```

Mẹo tìm nhanh ô sai: quét ô kiểu `s` mà nội dung khớp `/^-?[\d.,]+$/` → đó chính là ô Excel sẽ
cảnh báo "formatted as text".

Ảnh letterhead trên máy local: sau khi `companies.header` đã chuẩn hoá về URL tuyệt đối
(`https://erp.eteksofts.com/uploads/...`) thì **tải được ngay ở local** — kiểm bằng
`$export->drawings()` phải trả 1 drawing `letterhead ...x72 @A1`, trả 0 là URL hỏng. Nếu môi trường
chặn mạng ra ngoài, thử nhánh có ảnh bằng một file PNG tạm qua `file:///` và **nói rõ với user**
phần logo chưa kiểm chứng trên môi trường thật.

---

## 8. Checklist khi tạo/sửa export

- [ ] Mọi ô số/tiền: in **số thô** (`excelNumber()`), có `data-format` đúng mã
- [ ] Mã định dạng quyết định theo **từng ô** (`#,##0` số nguyên · `#,##0.##` số lẻ), không dùng
      chung 1 mã cho cả cột (mục 1a)
- [ ] Ô cố ý là chuỗi (kèm "đồng"/tên tiền tệ) thì **không** gắn `data-format`
- [ ] User chê dấu ngăn cách ra dấu phẩy → hướng dẫn đổi Windows Regional Settings, **KHÔNG** đổi ô
      tiền sang chuỗi (mục 1b)
- [ ] Còn chuỗi số kiểu Việt nào trong view (tỷ giá, ghi chú có số…) → đã có `WithCustomValueBinder`
      chặn `is_numeric('23.000')` (mục 1c)
- [ ] Không còn `width: ..px` trong `<td>` của nhánh Excel; bề rộng đặt bằng `WithColumnWidths`
- [ ] Có letterhead nếu chứng từ bản in có (dùng trait `EmbedsCompanyLetterhead`)
- [ ] Ảnh tải lỗi vẫn xuất được file
- [ ] `registerEvents()` không trỏ vùng ô tuyệt đối theo số dòng dữ liệu
- [ ] Sửa nhánh Excel xong đã kiểm lại **bản in** không đổi
- [ ] Đã dựng file thật + đọc lại kiểm kiểu ô / bề rộng / drawing (mục 7)
- [ ] Tên file tải về có mã chứng từ, đã lọc ký tự lạ (`preg_replace('/[^A-Za-z0-9._-]/', '_', $code)`)

---

## 9. File tham chiếu trong repo

| Cần xem gì | File |
| --- | --- |
| Export chứng từ đủ 3 quy tắc (số, bề rộng, logo) | `Modules/Finance/Exports/BillIncomeExport.php` |
| Export nhiều bố cục | `Modules/Finance/Exports/BillPaymentExport.php` |
| Mã định dạng theo từng ô + binder chặn chuỗi Việt | `Modules/Finance/Exports/BillPaymentRequestExport.php` · `Modules/Finance/Services/BillPaymentRequestService.php` (`excelNumber()` · `moneyFormat()` · `moneyFormats()`) |
| Trait nhúng letterhead | `Modules/Finance/Exports/Concerns/EmbedsCompanyLetterhead.php` |
| Service tách nhánh in/Excel + `excelNumber()` | `Modules/Finance/Services/BillIncomePrintService.php` |
| Nhúng ảnh theo dòng + tải song song | `Modules/Assign/Export/QuotationExcelExport.php` |
| Helper tải file phía FE | `hrm-client/utils/download-excel.js` |

## 4b. Letterhead ở file dựng bằng ExcelJS (FE) — TRẢI HẾT BỀ RỘNG BẢNG

Áp cho `utils/export/listExportFile.js` (màn danh sách tự dựng file ở trình duyệt).

Ảnh đầu file là **LETTERHEAD** — dải tiêu đề thư của công ty (tên, địa chỉ, điện thoại, website),
KHÔNG phải cái logo vuông. Vì vậy nó phải **kéo ngang đúng bằng bề rộng của bảng**, y như bản in
giấy. Chèn ảnh cỡ cố định kiểu `260 × 72` thì trên file 15 cột nó chỉ bé bằng 1/10 bảng, nhìn như
ảnh bị lạc vào (Redmine #11170).

```js
const tableWidthPx = headings.reduce(
    (total, _h, i) => total + charWidthToPx(widths[i] || DEFAULT_COLUMN_WIDTH), 0)
const ratio = pngAspectRatio(logo) || DEFAULT_LETTERHEAD_RATIO   // đọc từ 32 byte đầu của PNG
const imageHeightPx = Math.round(tableWidthPx / ratio)

sheet.addImage(imageId, { tl: { col: 0, row: 0 }, ext: { width: tableWidthPx, height: imageHeightPx } })
sheet.getRow(1).height = Math.round(imageHeightPx * 0.75)   // Excel tính dòng bằng POINT
```

Bắt buộc:
- **Bề rộng suy từ chính bảng**, không hằng số: `px = số_ký_tự × 7 + 5` cho MỖI cột (7px/ký tự,
  5px padding) rồi cộng lại. Chỉ cộng số cột có trong `headings` — BE có thể trả dư `widths`.
- **Chiều cao suy từ tỉ lệ ảnh thật**, không đặt cứng: đọc `width`/`height` ở byte 16-23 của PNG
  (khối IHDR) từ chính chuỗi base64, không cần nạp ảnh ra DOM. Đặt cứng chiều cao là ảnh bị bóp
  méo, chữ trong letterhead nhoè.
- **Dòng 1 phải cao bằng ảnh** (`height × 0.75` vì Excel tính bằng point), nếu không ảnh đè lên
  dòng tiêu đề.
- Ảnh hỏng / API letterhead lỗi → bỏ qua ảnh, **vẫn xuất file**.

### Kiểm chứng (đừng tin mắt, cũng đừng tin openpyxl)

`openpyxl` **không đọc được** ảnh do ExcelJS ghi (neo kiểu `oneCellAnchor`) — nó báo `0 ảnh` dù
file có ảnh thật, và cộng thiếu bề rộng ở những dải cột gộp (`<col min="2" max="3">` chỉ tính 1
lần). Đã suýt báo nhầm "mất logo" vì tin nó. Kiểm bằng cách đọc thẳng gói xlsx:

```bash
unzip -l file.xlsx | grep -E 'media|drawing'      # phải có xl/media/image1.png
unzip -p file.xlsx xl/drawings/drawing1.xml | grep -o '<xdr:ext[^/]*/>'   # cx, cy (EMU, 1px = 9525)
unzip -p file.xlsx xl/worksheets/sheet1.xml | grep -o '<col [^>]*>'       # bề rộng từng cột
```

`cx / 9525` phải **bằng** tổng `width × 7 + 5` của các cột.
