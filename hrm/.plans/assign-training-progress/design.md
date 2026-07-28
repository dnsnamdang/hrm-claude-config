# Design (tóm tắt) — Trường "Tiến trình" cho QĐ cử đi đào tạo

- **Người phụ trách**: @manhcuong
- **Ngày**: 2026-07-15
- **Spec đầy đủ**: `docs/superpowers/specs/2026-07-15-assign-training-progress-design.md`
- **Màn**: `/decision/assign-training` · liên quan: `/decision/category/training-contract`

## Mục tiêu

Thêm trường **Tiến trình** cho QĐ cử đi đào tạo, phản ánh đã lập đủ HĐ đào tạo cho học viên chưa: **Chưa tạo** (0 HĐĐT) → **Chưa hoàn thành** (có nhưng chưa đủ) → **Đã hoàn thành** (đủ tất cả).

## Công thức

```
n = số học viên trong QĐ    (assign_training_students)
c = số HĐĐT đã tạo          (count DISTINCT student_id trong training_contracts)

c == 0             -> Chưa tạo
c < n              -> Chưa hoàn thành
n > 0 && c >= n    -> Đã hoàn thành
n == 0             -> Chưa tạo
```

`DISTINCT student_id`: nếu 1 HV lỡ có 2 HĐĐT thì đếm thường ra c=2/n=2 → báo nhầm "Đã hoàn thành".

## Quyết định lớn

| # | Vấn đề | Chốt |
|---|---|---|
| 1 | Nguồn tính | **Đếm bảng `training_contracts`** (nguồn sự thật), KHÔNG dùng cờ `training_contract_status` — cờ này set rải rác 3 nơi nên có rủi ro lệch |
| 2 | Lưu hay tính | **Tính động** — không migration, không thể lệch, không phải sửa luồng tạo/xoá HĐĐT |
| 3 | Hiển thị | Cột "Tiến trình" (badge) trong danh sách + bộ lọc. Không kèm số (2/3), không thêm màn chi tiết |
| 4 | QĐ 0 học viên | **Chưa tạo** |

## Điểm kỹ thuật

1. **Không đụng mixin dùng chung**: `getStatusClass`/`listStatus` ở `pages/decision/mixins/common.js` dùng chung mọi màn QĐ → khai `listProgress`/`getProgressClass` **local** trong assign-training.
2. **Filter không dùng được alias `withCount`**: MySQL không cho tham chiếu alias subselect trong `WHERE` → phần lọc viết correlated subquery riêng trong `whereRaw`.
3. **Tiện tay sửa N+1 sẵn có**: `count_students` đang query riêng mỗi dòng → gộp vào `withCount` → màn danh sách **bớt** 1 query/dòng dù thêm tính năng mới.

## Phạm vi

**5 file, không migration / permission / git.**

| File | Việc |
|---|---|
| `Modules/Decision/Entities/AssignTraining.php` | + relation `trainingContracts()` + hằng `PROGRESS_*` + `PROGRESS_TEXT` |
| `Services/AssignTraining/AssignTrainingService.php` | + `withCount` 2 count; + filter `training_progress` |
| `Transformers/AssignTraining/AssignTrainingResource.php` | + `training_progress` + `training_progress_name` |
| `pages/decision/assign-training/index.vue` | + cột "Tiến trình" (trước "Trạng thái") + droplist lọc + method local |
| `resources/views/exports/assign_training.blade.php` | + cột "Tiến trình" trước "Trạng thái" + nới `colspan` 12→13 |

## Badge màu

Chưa tạo = `badge-info` (xanh dương) · Chưa hoàn thành = `badge-warning` (vàng) · Đã hoàn thành = `badge-success` (xanh lá).
**Lưu ý**: `badge-secondary` KHÔNG tồn tại trong theme (0 chỗ dùng toàn dự án) → render nền trắng vô hình. Chỉ dùng info/warning/success/danger.

## Downstream

Thêm 2 khoá vào response `index` (thuần bổ sung → FE cũ không vỡ). `export()` đi qua `index()` nên có sẵn data, NHƯNG blade chọn cột thủ công → phải thêm cột vào blade (data có sẵn không tự xuất hiện). Export ra định dạng **`.xls`** (BIFF/OLE2), không phải `.xlsx`. Cờ `training_contract_status` giữ nguyên, không đụng.

## Data test

AT#4 = 0/3 (**Chưa tạo**) · AT#1 = 1/1 và AT#3 = 3/3 (**Đã hoàn thành**). Chưa có ca **Chưa hoàn thành** → tạo bằng `DB::transaction` + `rollBack` (xoá 1 HĐĐT của AT#3 → 2/3).
