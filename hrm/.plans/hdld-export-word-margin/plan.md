# Plan — Lề file Word + bản in HĐLĐ

Nhánh: `fix_hdld_export_word` (tách từ `tpe`) — worktree `wt-hdld-api` / `wt-hdld-client`.
Người phụ trách: @junfoke

Chuẩn lề chốt với user (14/09/2026): **20mm trên / 15mm phải / 20mm dưới / 25mm trái** — lấy theo
`padding` của `#content` trong `pages/decision/labor-contract/_id/print.vue`. Ba nơi phải giống nhau:
preview web · cửa sổ in thật · file Word.

## Phase 1 — Xuất Word HĐLĐ đúng lề như bản in web

- [x] BE: `exportWord()` đổi lề trang 1cm tứ phía → 20/15/20/25mm
- [x] BE: giữ `text-indent`, map `margin-left` → indentation trái của Word (PhpWord không hiểu `margin-left`)
- [x] BE: giãn dòng 1.4 + bỏ khoảng cách trước/sau đoạn (khớp CSS bản in web)
- [x] BE: chuẩn hoá bề rộng bảng + ô về % để không tràn lề sau khi đổi lề
- [x] Verify: render lại `.docx` bằng PHP 7.4 local với template thật (HĐ id 706, 91KB)

## Phase 2 — Bản in thật (Ctrl+P) khớp với preview

- [x] FE: `print.vue` truyền `pageMargin: '20mm 15mm 20mm 25mm'` cho `$printContent`
- [x] FE: truyền `styles` bù phần scoped CSS không sang được cửa sổ in (font, cỡ chữ, giãn dòng, bảng 100%)
- [x] Verify bằng Playwright: đo bề ngang bảng trong cửa sổ in

## Kết quả đo được

| | Trước | Sau |
| --- | --- | --- |
| `w:pgMar` file Word | 567 twip tứ phía (1cm) | top 1134 · right 850 · bottom 1134 · left 1417 |
| Đoạn có lùi lề trái (`w:ind`) | 0 | 35 |
| Giãn dòng | không khai | `w:line="336" w:lineRule="auto"` (= 1.4) |
| Bề ngang bảng trong Word | `9645 dxa` cố định | `5000 pct` (100%), mọi ô đổi sang % |
| Bề ngang bảng ở cửa sổ in | **697px** (tràn khỏi vùng in 605px → Chrome co trang → tiêu đề xuống dòng) | **643px** = đúng bằng bề ngang preview |
| Nội dung chữ | 7.119 ký tự | 7.119 ký tự (không mất chữ) |

## Phase 3 — Dấu đầu dòng (bullet) và file hỏng khi có dấu "&" (14/09/2026)

QA báo bullet ra ô vuông rỗng. Truy ra 2 lỗi SẴN CÓ của PhpWord (bản export cũ cũng dính,
không phải do Phase 1 gây ra):

- [x] Bullet ra ô vuông: `Html::getListStyle()` ghép ký tự `•` (U+2022) với font **Symbol**,
      `◦` (U+25E6) với **Courier New** — hai font này KHÔNG có ký tự đó nên Word vẽ ô vuông.
      → `fixBulletFont()` đổi font mọi cấp bullet sang Times New Roman.
- [x] Word báo hỏng không mở được file khi nội dung có dấu `&` (vd phòng "P. MKT & TT"):
      PhpWord mặc định ghi text THÔ (`Settings::isOutputEscapingEnabled()` = false) → `document.xml`
      sai cú pháp XML. → gom dựng + ghi file vào `buildTempFile()`, bật escaping quanh lúc ghi
      rồi trả lại giá trị cũ (cờ toàn cục).
- [x] Verify: mẫu VNPTHCM có `<ul><li>` — XML hợp lệ, Word mở được, dấu đầu dòng ra đúng chấm tròn
      U+2022 (kiểm bằng mã ký tự trong PDF, không còn ký tự vùng private-use F000-F0FF).

⚠ Còn 1 điểm chưa xử lý (Word vẫn mở bình thường nên để nguyên): PhpWord ghi vài giá trị twip
dạng số thực (`w:firstLine="186.99999999999997"`, `w:pgSz w:w="11905.511811023622"`) trong khi
OOXML khai kiểu số nguyên.

## Checkpoint

### Checkpoint — 14/09/2026
Vừa hoàn thành: Phase 1 + Phase 2, ĐÃ VERIFY THẬT (mở file Word bằng Word trên máy + in ra PDF, và
in bản web bằng Chrome qua CDP `Page.printToPDF` khổ A4 tỷ lệ 100%).

Hai lỗi CHỈ lộ ra khi verify bằng file thật, đã sửa:
1. `text-indent:.5in` bị PhpWord bỏ im lặng — `Converter::cssToPoint()` đòi `[0-9]+` trước dấu chấm
   nên `.5in` không khớp regex → trả null. Thêm `normalizeCssNumber()` đổi `.5in` → `0.5in`.
2. Dù đã có `w:firstLine`, Word vẫn không thụt đầu dòng vì PhpWord LUÔN ghi kèm `w:hanging="0"`
   (mặc định của `Style\Indentation::$hanging` là 0 chứ không phải null), mà OOXML quy định
   `hanging` đè `firstLine`. Thêm `fixFirstLineIndent()` đặt `hanging = null`.
3. FE: `#content p { margin: 0 }` viết tắt đã xoá luôn `margin-left:48px` của template → bản in mất
   lùi lề khối "Hôm nay, ngày…". Đổi thành `margin-top/margin-bottom` như đúng CSS của preview.

Bước tiếp theo: user commit + đẩy nhánh `fix_hdld_export_word`.
Blocked: (không)

## Kết quả verify cuối (HĐ 4900/2026/HĐLĐ-KSCHCM, template thật lấy từ cổng KSC)

| Vị trí chữ (mm tính từ mép trái giấy) | Bản in web (Chrome, A4) | File Word (Word xuất PDF) |
| --- | --- | --- |
| Dòng "Căn cứ…" | 24.9 | 25.0 |
| Khối "Hôm nay, ngày…" | 37.6 | 37.7 |
| Dòng "Số CCCD" | 37.6 | 37.7 |
| Lề phải | 15.0 | 14.8–15.0 |
| Lề trên | 20 | 19.7 |
| Tiêu đề "CỘNG HÒA XÃ HỘI CHỦ NGHĨA VIỆT NAM" | 1 dòng | 1 dòng |

Trước khi sửa, in A4 với lề mặc định: tiêu đề tách 2 dòng ("…CHỦ NGHĨA VIỆT" / "NAM"), bản in 6 trang.
Sau khi sửa: 1 dòng, 5 trang. File Word cũ: lề 10mm tứ phía, 0 đoạn thụt đầu dòng, 0 khai giãn dòng.
