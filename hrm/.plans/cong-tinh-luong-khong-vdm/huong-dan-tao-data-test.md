# Hướng dẫn tạo data test — cột "Công tính lương (13)" (Redmine #11457)

## 0. Hiểu trước: 2 màn lấy dữ liệu từ 2 NƠI KHÁC NHAU

| Màn | Nguồn dữ liệu | Tính lúc nào |
|---|---|---|
| **Bảng công chi tiết** `/timesheet/timesheet_details` | Bảng `timesheet_summaries` (1 dòng = 1 ngày công của 1 NV) + `overtime_details` (VĐM) | **LIVE** — sửa dữ liệu ngày là màn đổi ngay, không cần chốt gì |
| **Bảng công tổng hợp** `/timesheet/timesheet_summaries/{id}` | Bảng `timesheet_month_summary_details` — sinh ra lúc **bấm Thêm mới bảng công**, tổng hợp từ `timesheet_summaries` | **CHỐT MỘT LẦN** — sửa dữ liệu ngày sau đó thì bảng cũ KHÔNG tự cập nhật |

⚠️ Nên tạo data ngày **TRƯỚC**, rồi mới tạo bảng công tổng hợp. Làm ngược lại thì bảng tổng hợp ra toàn số 0.

⚠️ **Cột (11) Công cộng giảm trừ được tính từ 2 nguồn khác nhau ở 2 màn**:
màn chi tiết lấy `(phút đi muộn + phút về sớm) / 480`, màn tổng hợp lấy thẳng cột `punishment_rule`.
Tạo data phải set **cả hai cho khớp**, nếu không 2 màn ra số lệch nhau và tưởng là bug.

---

## 1. Cách nhanh nhất — chạy script có sẵn

```bash
cd hrm-api
php artisan tinker --execute="\$MA_NV='10610024'; \$THANG='2026-08'; require '/Users/manhcuong/Desktop/dns/HRM/.plans/cong-tinh-luong-khong-vdm/seed-test-data.php';"
```

Đổi `$MA_NV` (mã nhân viên) và `$THANG` (`YYYY-MM`) theo ý. Script:

- chỉ đụng **đúng 1 nhân viên + đúng 1 tháng** đó (xoá sạch rồi tạo lại) — nhân viên khác, tháng khác không ảnh hưởng
- chạy lại nhiều lần được, không sinh dữ liệu trùng
- in ra luôn **bảng giá trị kỳ vọng** để đối chiếu với màn hình

Bộ ca nó tạo (tháng 08/2026, mã 10610024 — đã chạy và đối chiếu khớp 22/09/2026):

| Ca | Tạo gì | Rơi vào cột |
|---|---|---|
| 1 | 13 ngày công thường | (1) Công hành chính |
| 2 | 2 ngày nghỉ phép | (5) → (8) |
| 3 | 1 ngày lễ hưởng lương | (6) → (8) |
| 4 | 1 ngày nghỉ chế độ hưởng nguyên lương | (7) → (8) |
| 5 | 1 ngày đi muộn 30' + 1 ngày về sớm 24' | (9)(10) → (11) |
| 6 | 2 ngày làm thêm (x1.5 = 4h, x2 = 3h) | VĐM → (3), **KHÔNG được vào (13)** |

Kết quả kỳ vọng:

```
(1)  Công hành chính     = 17
(3)  Tổng VĐM quy đổi    = 1.5
(8)  Cộng NHL            = 4      (phép 2 + lễ 1 + chế độ 1)
(11) Công cộng giảm trừ  = 0.11   (54 phút / 480)
(13) CÔNG TÍNH LƯƠNG     = 20.89  <-- (1)+(8)-(11)
(14) Tổng công tính lương= 22.39  <-- (13) + VĐM 1.5
```

**Ca số 6 chính là ca quan trọng nhất**: cột (13) và (14) phải LỆCH NHAU đúng bằng phần VĐM.
Nếu hai cột bằng nhau ở nhân viên có làm thêm → sai.

Xem kết quả: mở `/timesheet/timesheet_details`, chọn tháng 08/2026, gõ mã NV vào ô "Nhân viên".

---

## 2. Tạo tiếp data cho màn Bảng công tổng hợp

1. Vào `/timesheet/timesheet_summaries` → **Thêm mới**
2. Điền: **Tên bảng chấm công** (vd `TEST 11457 tháng 8/2026`) · **Từ ngày** `01/08/2026` · **Đến ngày** `31/08/2026` · **Loại** = `Bảng công thường`
3. Lưu → hệ thống tổng hợp từ dữ liệu ngày vừa tạo
4. Mở bảng vừa tạo, kiểm cột **Công tính lương (13) = (1)+(8)-(11)**, thử cả **2 kiểu xem** (`Tổng hợp` / `Chi tiết`) ở ô chọn góc trái

### Hai cột chỉ test được ở màn tổng hợp

| Cột | Vì sao | Cách tạo |
|---|---|---|
| **(2) Công đi đường** | Màn chi tiết lấy live từ đề nghị thanh toán đã được kế toán duyệt — dựng tay rất dài | Ở bảng tổng hợp, gõ thẳng vào ô **Công đi đường(2)** rồi Lưu |
| **(12) Bù trừ sau quyết toán** | Màn chi tiết **luôn trả 0** (hard-code trong `TimesheetSummaryService`) | Ở bảng tổng hợp, gõ vào ô **Bù trừ công hành chính…(12)** rồi Lưu |

Cả 2 cột này **không được cộng vào (13)** — đây là ca test bắt buộc phải kiểm.
Ô ở bảng tổng hợp sửa tay được nên cột (13) nhảy **ngay khi gõ**, chưa cần bấm Lưu.

---

## 3. Test thành phần lương `CONG_TINH_LUONG`

1. `/payroll/salarycomposition/system-category` → phải thấy `CONG_TINH_LUONG` / "Công tính lương"
2. Đưa TPL đó vào một công thức lương, chạy tính lương cho kỳ có bảng công vừa tạo
3. Giá trị TPL phải bằng đúng cột (13) trên bảng công

Kiểm nhanh không cần chạy tính lương:

```bash
cd hrm-api
php artisan tinker --execute="
\$svc = app(\Modules\Payroll\Services\SalaryService::class);
echo \$svc->calcData('CONG_TINH_LUONG', <employee_info_id>, <salary_id>);
"
```

---

## 4. Xoá data test

Chạy lại script ở mục 1 là nó tự xoá rồi tạo lại. Muốn xoá hẳn:

```bash
cd hrm-api
php artisan tinker --execute="
use Modules\Timesheet\Entities\{TimesheetSummary, OvertimeDetail, EmployeeInfo};
\$id = EmployeeInfo::where('code','10610024')->value('id');
\$ids = TimesheetSummary::where('employee_info_id',\$id)->whereBetween('day',['2026-08-01','2026-08-31'])->pluck('id');
OvertimeDetail::whereIn('timesheet_summary_id',\$ids)->delete();
TimesheetSummary::whereIn('id',\$ids)->delete();
echo 'đã xoá '.\$ids->count().' ngày công';
"
```

Bảng công tổng hợp test thì xoá bằng nút **Xoá** ngoài danh sách `/timesheet/timesheet_summaries`.

---

## 5. Bẫy đã dính khi viết script này

- **`type_day` và `ca_dem` KHÔNG nằm trong `$fillable` của model `TimesheetSummary`** → `create()` bỏ qua **im lặng**, không báo lỗi gì. Ngày lễ tạo ra vẫn thành ngày thường, cột (6) ra 0. Phải ghi lại bằng query builder sau khi create (script đã xử lý).
- Ngày nghỉ phép vẫn phải để `labour_day = 1` **và** `work_day_phep = 1`: công hành chính (1) được tính bằng `tổng labour_day − phép − chế độ − lễ`. Để `labour_day = 0` là hụt công.
- Tháng ít ngày thường (T2–T6) hơn số ca cần tạo thì script báo và dừng — đừng chọn tháng có quá nhiều lễ.
