# Auto Progress 100% khi chuyển trạng thái Hoàn thành

**Ngày**: 2026-05-06
**Module**: Giao việc (Assign)
**File ảnh hưởng**: `hrm-client/pages/assign/tasks/components/ImportResultModal.vue`

---

## Mục tiêu

Khi nhập kết quả task mà task **không yêu cầu báo cáo tiến độ** (`progress_report.is_active = false`), nếu user đổi trạng thái sang **Hoàn thành - Chờ duyệt (6)** hoặc **Hoàn thành (8)** thì tiến độ tự động nhảy sang 100%. Khi đổi trạng thái về giá trị khác thì tiến độ quay về giá trị cũ.

## Điều kiện áp dụng

- Chỉ áp dụng khi `task.progress_report.is_active = false` (ô input tiến độ đơn giản)
- Không áp dụng khi `is_active = true` (tiến độ tính từ bảng log `latestLogProgressPct`)

## Trạng thái target

| Status ID | Tên | Auto 100% |
|-----------|-----|-----------|
| 6 | Hoàn thành - Chờ duyệt | Co |
| 8 | Hoàn thành | Co |
| Khac | * | Khong |

## Thiết kế kỹ thuật

### 1. Thêm biến data

- `_savedProgressPercent: null` — lưu giá trị tiến độ trước khi auto set 100%

### 2. Thêm watcher trên `result.status`

```javascript
watch: {
    'result.status'(newVal, oldVal) {
        if (this.task.progress_report.is_active) return

        const completionStatuses = [6, 8]
        const isNew = completionStatuses.includes(newVal)
        const isOld = completionStatuses.includes(oldVal)

        if (isNew && !isOld) {
            this._savedProgressPercent = this.result.progress_percent
            this.result.progress_percent = 100
        } else if (!isNew && isOld && this._savedProgressPercent !== null) {
            this.result.progress_percent = this._savedProgressPercent
            this._savedProgressPercent = null
        }
    }
}
```

### 3. Thêm computed `isCompletionStatus`

```javascript
isCompletionStatus() {
    return [6, 8].includes(this.result.status)
}
```

### 4. Disable ô input tiến độ khi completion status

Thay `:disabled="isReadOnly"` thành `:disabled="isReadOnly || isCompletionStatus"` trên ô input `result.progress_percent`.

## Edge cases

- User đổi status 6 → 8 (cả hai đều completion): không thay đổi gì, giữ nguyên 100%
- User đổi status 6 → 4 → 6: lưu lại giá trị mới mỗi lần, khôi phục đúng
- `fetchTaskDetail` set status ban đầu = 6 hoặc 8: watcher sẽ fire nhưng `_savedProgressPercent` sẽ lưu giá trị từ API response (đã có sẵn progress_percent)

## Không thay đổi

- Logic save (`handleSave`) và payload gửi API
- Trường hợp `progress_report.is_active = true`
- Backend
