# Design (tóm tắt) — Fix Excel "Số phút phạt đi muộn về sớm" sai (60 → 600)

**Người phụ trách:** @khoipv · **Ngày:** 2026-09-04 · **Loại:** Bug fix, chỉ FE

> Spec chi tiết: [`docs/superpowers/specs/2026-09-04-fix-excel-so-phut-phat-di-muon-ve-som-design.md`](../../docs/superpowers/specs/2026-09-04-fix-excel-so-phut-phat-di-muon-ve-som-design.md)

## Mục tiêu

Màn `timesheet/timesheet_summaries/{id}` — nút **Xuất excel**: cột "Số phút phạt đi muộn về sớm"
xuất ra sai số (NV Nguyễn Ngọc Quỳnh: màn hình 60, Excel 600). Sửa cho Excel khớp màn hình.

## Root cause

Màn hình và Excel dùng **cùng 1 API** nhưng **2 key khác nhau** trong response của
`TimesheetMonthSummaryService::show()`:

- Màn hình đọc `newData` — mảng PHP map thủ công → hiển thị 2 cột riêng, không cộng ⇒ **đúng**
- Excel đọc `data` — **collection Eloquent thô**, kiểu dữ liệu đi thẳng từ cột DB ⇒ **sai**

Trong `data`, `total_minutes_early` là cột `int` (→ JSON **number**) còn `total_minutes_late` là
cột `decimal(8,1)` (→ JSON **string** `"0.0"`, đúng chuẩn PDO native type của Laravel).
JS gặp `number + string` thì **nối chuỗi**: `60 + "0.0"` = `"600.0"` → Excel hiện **600**.

`|| 0` không cứu được vì `"0.0"` là chuỗi truthy. Các dòng có về sớm = 0 cho ra `"00.0"` → Excel
vẫn parse đúng thành 0, nên lỗi bị che giấu lâu nay.

## Quyết định lớn

1. **Sửa ở FE, không đụng BE** — không thêm `$casts` vào entity (dùng chung với tính lương),
   không đổi kiểu cột DB. Ép kiểu ngay tại điểm cộng, phạm vi đúng 1 file.
2. **Sửa cả 6 phép cộng trong file, không chỉ cột báo lỗi** — cùng một khuôn code, chỉ cần
   một lần đổi kiểu cột là các cột kia tái phát y hệt.
3. **Không sửa cột "Nghỉ hưởng BHXH" bị rỗng** — phát hiện phụ, ngoài phạm vi yêu cầu, chờ chốt.

## Phạm vi thay đổi

| File | Thay đổi |
|---|---|
| `hrm-thanhan-client/components/export-excel/timesheet_month_summaries.vue` | thêm helper `toNumber()`, bọc ép kiểu 6 phép cộng, rút biến `row` |

Không migration · không quyền mới · không phân quyền cấp · không đụng Backend.

## Kết quả verify

Chạy logic mới trên dữ liệu API thật bảng công 81 (120 dòng): **7 dòng sai → đúng 100%**
(600→60, 3060→90, 3030→60, 300→30), 113 dòng còn lại không đổi, giá trị ghi ra Excel là
**number thật** thay vì chuỗi, **0 regression** ở 3 nhóm cột cộng khác.

## Tồn đọng

- Chờ **build + deploy** demo để test lại nút Xuất excel (sửa FE nên phải hard refresh).
- Chờ @khoipv chốt có sửa luôn 2 cột Excel "Nghỉ hưởng BHXH" / "Nghỉ hưởng BHXH TV" đang
  **luôn rỗng** do `json_fields` map sai tên field (`work_day_huong_bhxh` ↔ `nghi_huong_bhxh`).
