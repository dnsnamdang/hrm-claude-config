# Fix: Excel "Số phút phạt đi muộn về sớm" sai (60 → 600)

**Người phụ trách:** @khoipv
**Màn:** `timesheet/timesheet_summaries/{id}` (Bảng chấm công tổng hợp) — nút "Xuất excel"
**Ca lỗi gốc:** Bảng công id 81, NV Nguyễn Ngọc Quỳnh (NV.00087): màn hình 60, Excel 600

**Tài liệu:**
- Design tóm tắt: [`design.md`](design.md)
- Spec chi tiết: [`docs/superpowers/specs/2026-09-04-fix-excel-so-phut-phat-di-muon-ve-som-design.md`](../../docs/superpowers/specs/2026-09-04-fix-excel-so-phut-phat-di-muon-ve-som-design.md)

---

## Root cause (đã chứng minh bằng dữ liệu thật trên demo)

`components/export-excel/timesheet_month_summaries.vue:102-103`

```js
this.json_data[i]['so_phut_phat_di_muon_ve_som'] =
    (this.json_data[i]['total_minutes_early'] || 0) + (this.json_data[i]['total_minutes_late'] || 0)
```

API `GET timesheet/timesheet_month_summaries/show` trả về key `data` là **collection Eloquent thô**
(`TimesheetMonthSummaryService::show()` → `'data' => $timesheetMonthSummaryDetails`), nên kiểu dữ liệu
đi thẳng từ cột DB:

| Cột | Kiểu DB | Kiểu trong JSON |
|---|---|---|
| `total_minutes_early` | `int` | **number** |
| `total_minutes_late` | `decimal(8,1)` | **string** (`"0.0"`) |

→ JS thực hiện **nối chuỗi** chứ không cộng: `60 + "0.0"` = `"600.0"` → Excel hiện **600**.

Bằng chứng (bảng công 81, 120 dòng — **7 dòng sai**):

| Nhân viên | early | late | Excel (sai) | Đúng |
|---|---|---|---|---|
| Nguyễn Ngọc Quỳnh | 60 | "0.0" | 600 | 60 |
| Mai Tuấn Anh | 60 | "0.0" | 600 | 60 |
| Nguyễn Huy Tân | 30 | "60.0" | 3060 | 90 |
| Bùi Quang Hưng | 30 | "30.0" | 3030 | 60 |
| Phạm Ngọc Tiển | 30 | "0.0" | 300 | 30 |
| Nguyễn Quốc Đàn | 30 | "0.0" | 300 | 30 |
| Trịnh Phương Thảo | 30 | "0.0" | 300 | 30 |

Các dòng có `early = 0` cho ra `"00.0"` → Excel parse ra 0 nên vô tình vẫn đúng (che giấu lỗi).

Màn hình KHÔNG sai vì hiển thị 2 cột riêng (`total_minutes_late`, `total_minutes_early`), không cộng.

## Phạm vi ảnh hưởng cùng khuôn (cùng file, cùng kiểu nối chuỗi)

- `so_phut_di_muon_ve_som` (dòng 97-101): 4 cột `di_muon_*`/`ve_som_*` hiện đều là `number` → chưa lộ lỗi, nhưng vẫn phải bọc `Number()` để không tái phát khi kiểu cột đổi.
- `num_of_in_out` (dòng 95-96): 2 cột `int` → an toàn.
- Nhóm `_tv` (dòng 104-113): các cột `double` → đều `number`, an toàn.

## Task

- [x] T1 — Điều tra root cause, tái hiện trên demo bằng dữ liệu thật (bảng 81)
- [x] T2 — Sửa `components/export-excel/timesheet_month_summaries.vue`: bọc `Number(...)` cho toàn bộ 6 phép cộng
- [x] T3 — Verify: chạy lại logic export trên dữ liệu API thật của bảng 81 → 7 dòng sai trở về đúng, 113 dòng còn lại không đổi

## Phát hiện phụ — CHƯA sửa (chờ @khoipv chốt)

Cột Excel **"Nghỉ hưởng BHXH"** và **"Nghỉ hưởng BHXH TV"** luôn **rỗng**:
`json_fields` map sang `work_day_huong_bhxh` / `work_day_huong_bhxh_tv`, nhưng key thật trong
mảng `data` là `nghi_huong_bhxh` / `nghi_huong_bhxh_tv` (chỉ mảng `newData` mới đổi tên).
Fix 2 dòng nếu được duyệt.

## Checkpoint — 2026-09-04

Vừa hoàn thành: T1 (điều tra root cause + tái hiện trên demo bằng dữ liệu thật bảng 81), T2 (sửa
`components/export-excel/timesheet_month_summaries.vue` — thêm helper `toNumber()`, ép kiểu 6 phép
cộng), T3 (verify trên dữ liệu API thật: 7/120 dòng sai → đúng, 113 dòng không đổi, 0 regression),
T4 (viết `design.md` + spec chi tiết `docs/superpowers/specs/2026-09-04-...-design.md`).

Đang làm dở: (không có — code đã xong, tài liệu đã đầy đủ)

Bước tiếp theo:
1. Build lại + deploy FE lên demo, hard refresh rồi bấm **Xuất excel** ở bảng công 81 → kiểm 7 nhân
   viên trong bảng bằng chứng, đặc biệt Nguyễn Ngọc Quỳnh phải ra **60** (không phải 600).
2. @khoipv chốt: có sửa luôn 2 cột Excel "Nghỉ hưởng BHXH" / "Nghỉ hưởng BHXH TV" đang **luôn rỗng**
   do `json_fields` map sai tên field (`work_day_huong_bhxh` ↔ `nghi_huong_bhxh`) không — fix 2 dòng.
3. @khoipv tự commit (không tự động commit theo quy ước dự án).

Blocked: (không)
