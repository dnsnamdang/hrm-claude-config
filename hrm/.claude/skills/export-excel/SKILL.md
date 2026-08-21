---
name: export-excel
description: Use when tạo mới hoặc sửa chức năng XUẤT EXCEL ở BE (class `*Export` + blade `exports/*.blade.php` dùng `maatwebsite/excel`), hoặc khi user báo lỗi file .xlsx tải về — thiếu logo công ty, cột quá hẹp/chữ bị cắt, số tiền bị Excel cảnh báo "The number in this cell is formatted as text", số không có dấu phân cách hàng nghìn, cộng SUM ra 0.
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

**Mã định dạng hay dùng:** `#,##0` (tiền VND) · `#,##0.00` (2 số lẻ) · `0%` · `dd/mm/yyyy`.

**Ngoại lệ — ô CỐ Ý là chuỗi:** giá trị in kèm đơn vị/tiền tệ (`"169,374,000 đồng"`,
`"1,000,000 USD"`). Chuỗi này không thuần số nên Excel không cảnh báo → giữ `number_format`,
**không** gắn `data-format`.

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
- [ ] Ô cố ý là chuỗi (kèm "đồng"/tên tiền tệ) thì **không** gắn `data-format`
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
| Trait nhúng letterhead | `Modules/Finance/Exports/Concerns/EmbedsCompanyLetterhead.php` |
| Service tách nhánh in/Excel + `excelNumber()` | `Modules/Finance/Services/BillIncomePrintService.php` |
| Nhúng ảnh theo dòng + tải song song | `Modules/Assign/Export/QuotationExcelExport.php` |
| Helper tải file phía FE | `hrm-client/utils/download-excel.js` |
