# Spec: Action "Lưu và duyệt" / "Giao cho Leader" từ danh sách giải pháp

**Ngày:** 2026-05-07
**Người phụ trách:** @manhcuong
**Module:** Assign — Giải pháp (Solution)

---

## 1. Mục tiêu

Thêm action duyệt nhanh trên row danh sách giải pháp (SolutionsTab trong my-job), cho phép PM vào trang edit với footer đơn giản chỉ có nút duyệt + quay lại. Đồng thời tách biệt hành vi: action "Chỉnh sửa" chỉ cho phép lưu thông tin mà không chuyển trạng thái.

---

## 2. Scope

### Trong scope
- Thêm action mới trên row danh sách SolutionsTab khi status = `STATUS_CHO_PM_DUYET (3)` + `can_edit = true`
- Trang edit nhận query param `mode=approve` để thay đổi footer
- Action "Chỉnh sửa" ở trang edit chỉ hiện "Lưu" (giữ nguyên status) + "Quay lại"

### Ngoài scope
- Không thay đổi logic backend approve
- Không thay đổi flow cho các status khác
- Không thay đổi trang manager

---

## 3. Chi tiết thiết kế

### 3.1 SolutionsTab.vue — Thêm action trên row

Trong method `getRowActions(item)`, khi `item.can_edit === true` và `item.status === STATUS_CHO_PM_DUYET`:

| Điều kiện | Action mới | Icon |
|-----------|-----------|------|
| `has_modules = true` | "Giao cho Leader" | `ri-send-plane-line` |
| `has_modules = false` | "Lưu và duyệt" | `ri-check-double-line` |

Navigate tới: `/assign/solutions/${item.id}/edit?mode=approve&from=my-job&tab=solutions`

**Dữ liệu cần:** `item.has_modules` — cần kiểm tra SolutionResource backend đã trả field `has_modules` chưa.

### 3.2 edit.vue — Footer thay đổi theo mode

Đọc `this.$route.query.mode` để xác định chế độ:

#### Mode `approve` (vào từ action "Giao cho Leader" / "Lưu và duyệt"):
- Ẩn: button "Lưu nháp", button "Lưu hạng mục"
- Hiện: button submit duy nhất (text "Giao cho Leader" hoặc "Lưu và duyệt" tuỳ `has_modules`) + "Quay lại"
- Logic submit: giữ nguyên `submitForm(nextStatus)` hiện tại

#### Mode mặc định (vào từ action "Chỉnh sửa", không có query `mode`):
- Ẩn: button submit chuyển trạng thái ("Giao cho Leader" / "Lưu và duyệt")
- Hiện: button **"Lưu"** (gọi API PUT giữ nguyên status hiện tại) + "Quay lại"
- Logic "Lưu": gọi `submitForm(STATUS_CHO_PM_DUYET)` — PUT update thông tin nhưng status không đổi

#### Bảng tổng hợp footer theo mode + status

| Mode | Status | Buttons |
|------|--------|---------|
| `approve` | `CHO_PM_DUYET` + `has_modules` | "Giao cho Leader" + "Quay lại" |
| `approve` | `CHO_PM_DUYET` + `!has_modules` | "Lưu và duyệt" + "Quay lại" |
| mặc định | `CHO_PM_DUYET` | "Lưu" + "Quay lại" |
| mặc định | Các status khác | Giữ nguyên như hiện tại |

### 3.3 Backend

Không thay đổi. API `PUT /api/v1/assign/solutions/{id}` đã hỗ trợ:
- Chuyển status khi `status` trong payload khác status hiện tại (approve flow)
- Giữ nguyên status khi `status` trong payload = status hiện tại (save flow)

---

## 4. Files cần sửa

| File | Thay đổi |
|------|---------|
| `hrm-client/pages/assign/my-job/components/SolutionsTab.vue` | Thêm action "Giao cho Leader" / "Lưu và duyệt" trong `getRowActions()` + handle navigate trong `handleRowAction()` |
| `hrm-client/pages/assign/solutions/_id/edit.vue` | Đọc `$route.query.mode`, thay đổi footer buttons theo mode |

---

## 5. Kiểm tra trước khi code

- [ ] Confirm `SolutionResource` đã trả `has_modules` trong response list (SolutionsTab dùng API `/my-job/solution-list`)
- [ ] Confirm `submitForm(STATUS_CHO_PM_DUYET)` ở mode mặc định chỉ save mà không chuyển trạng thái

---

## 6. Edge cases

- PM mở trang edit trực tiếp bằng URL (không qua action) → xử lý như mode mặc định (chỉ "Lưu" + "Quay lại")
- Giải pháp đã bị người khác duyệt trong khi PM đang ở trang edit → backend trả lỗi status không hợp lệ, FE hiện toast lỗi
