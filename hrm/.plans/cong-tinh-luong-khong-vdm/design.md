# Công tính lương (không VĐM, không đi đường) — Tóm tắt

**Redmine:** [#11457](http://quanly.dnsmedia.vn/issues/11457) — Tính năng mới · Khẩn cấp · Nguyễn Huyền tạo 11/09/2026 · giao @Manh Cuong
**Trạng thái task:** Chờ Duyệt giá
**Nhánh:** `tpe-develop-assign` (cả `hrm-api` + `hrm-client`)

## Mục tiêu

Thêm MỘT chỉ số công mới — **Công tính lương** — song song với cột `Tổng công tính lương` đang có,
khác ở chỗ **loại bỏ công vượt định mức (VĐM) và công đi đường**.

```
Công tính lương = Công hành chính (1) + Công nghỉ hưởng lương (8) − Công cộng giảm trừ (11)
```

So với cột cũ `Tổng công tính lương = (4)+(8)-(11)+(12)`:
- dùng **(1) Công hành chính** thay **(4) Tổng công đi làm** → bỏ VĐM (3) và công đi đường (2)
- **không cộng (12)** Bù trừ công hành chính sau quyết toán công tác

⚠️ Task ghi rõ: *"Công tính lương KHÁC với tổng công tính lương hiện tại"* → **không được sửa cột cũ**.

## Phạm vi

1. **Bảng công chi tiết** `/timesheet/timesheet_details` — thêm cột, có tooltip công thức
2. **Bảng công tổng hợp** `/timesheet/timesheet_summaries/{id}` — thêm cột ở **cả 2 kiểu xem** (Tổng hợp / Chi tiết)
3. **Thành phần lương hệ thống** `/payroll/salarycomposition/system-category` — thêm TPL `CONG_TINH_LUONG`
4. Xuất Excel của (1) và (2) phải khớp màn hình

## Quyết định đã chốt

| # | Vấn đề | Chốt |
|---|--------|------|
| 1 | TPL mới là bản ghi mới hay map vào TPL có sẵn? | **Bản ghi MỚI**, mã `CONG_TINH_LUONG` (user chốt 22/09/2026) |
| 2 | Có chặn trần bằng Công định mức không? | **KHÔNG cap** — lấy số thô (user chốt 22/09/2026). Lý do: công thức khách ghi là cộng trừ thuần; cột đã bỏ VĐM/đi đường nên phần vượt trần chỉ còn do nghỉ phép/lễ hưởng lương, cắt đi = ăn bớt công của NV; cột (13) cũ ở màn chi tiết cũng đang không cap |
| 3 | "Sửa ở cả 2 dạng xem" nghĩa là gì? | Ô **"Kiểu xem"** đầu màn Bảng công tổng hợp: `Tổng hợp` (1) / `Chi tiết` (2) — `_id/index.vue:641` |
| 4 | Đánh số cột | Cột mới lấy số **(13)**, chèn TRƯỚC cột tổng cũ; (13) cũ → **(14)**, dồn tiếp tới (18)→(19). Công thức các cột cũ GIỮ NGUYÊN, chỉ đổi số hiệu |

## Điểm cần lưu ý khi làm

- Giá trị cột ở **Bảng công chi tiết do FE tự cộng** (`timesheet_details/index.vue` `getData()`), BE chỉ trả field thô → không cần sửa API.
- `openDetail()` dùng offset cứng `+2` (công đi đường) và `+22` (công truy thu). Cột mới nằm ở offset **23** nên KHÔNG vỡ popup — nhưng phải giữ đúng vị trí chèn.
- TPL mới **không cần migration**: tính on-the-fly từ `timesheet_month_summary_details` trong switch-case, giống các TPL chấm công khác.
- Switch-case chấm công bị **nhân bản ở 2 file** (`CreateEmployeePayroll.php` + `SalaryService.php`) → phải sửa cả hai, nếu không lương tính qua job và qua service ra số khác nhau.

**Spec chi tiết:** `docs/superpowers/specs/2026-09-22-cong-tinh-luong-khong-vdm-design.md`
