# Spec: Tự động tính Tiến độ hoàn thành từ nhật ký tiến độ gần nhất

**Ngày:** 2026-05-04  
**Module:** Giao việc — `pages/assign/tasks`  
**File:** `hrm-client/pages/assign/tasks/components/ImportResultModal.vue`

---

## Mục tiêu

Khi task được cấu hình **yêu cầu báo cáo tiến độ** (`progress_report.is_active = true`, Mode B), field "Tiến độ hoàn thành (%)" không cho nhập tay nữa mà **tự động lấy giá trị từ dòng nhật ký có `report_date` lớn nhất và đã có giá trị `progress_pct`**.

---

## Scope

Chỉ thay đổi FE, không thay đổi BE. Backend vẫn nhận `progress_percent` như cũ — chỉ thay đổi nguồn giá trị.

---

## Business Rule

- **Mode A** (`!is_active`): `progress_percent` nhập tay như cũ — không thay đổi.
- **Mode B** (`is_active = true`):
  - Field disabled, không cho nhập.
  - Giá trị hiển thị = `progress_pct` của dòng `progress_logs` có `report_date` lớn nhất **và** `progress_pct` không rỗng/null.
  - Nếu chưa có dòng nào có giá trị → hiển thị rỗng, gửi `null` lên backend.
  - Hiển thị hint text: *"Tự động lấy từ nhật ký gần nhất có giá trị"*

---

## Thay đổi kỹ thuật

### 1. Computed property mới

```js
latestLogProgressPct() {
    const logs = (this.result.progress_logs || [])
        .filter(r => r.progress_pct !== '' && r.progress_pct !== null && r.progress_pct !== undefined)
        .sort((a, b) => b.report_date.localeCompare(a.report_date))
    return logs.length ? logs[0].progress_pct : null
}
```

### 2. Template — field "Tiến độ hoàn thành (%)" ở Mode B (lines ~376-390)

- Đổi `v-model="result.progress_percent"` → `:value="task.progress_report.is_active ? latestLogProgressPct : result.progress_percent"`
- Thêm `:disabled="isReadOnly || task.progress_report.is_active"`
- Thêm hint text bên dưới khi Mode B

### 3. handleSave payload

```js
progress_percent: this.task.progress_report.is_active
    ? this.latestLogProgressPct
    : this.result.progress_percent,
```

---

## Edge cases

- Người dùng xóa hết `progress_pct` trong tất cả các dòng → `latestLogProgressPct` = `null` → gửi `null` lên BE.
- `report_date` cùng ngày nhưng nhiều dòng → sort theo string, lấy dòng đầu tiên sau sort desc (thực tế không xảy ra do schedule không tạo 2 dòng cùng ngày).
- Mode A → Mode B: vì `progress_report.is_active` là readonly (từ server), không có transition này trong UI.

---

## Files cần thay đổi

| File | Thay đổi |
|------|----------|
| `hrm-client/pages/assign/tasks/components/ImportResultModal.vue` | Thêm computed, sửa template, sửa handleSave |
