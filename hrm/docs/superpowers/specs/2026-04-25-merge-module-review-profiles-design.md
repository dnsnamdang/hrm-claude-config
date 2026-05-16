# Gộp hồ sơ trình duyệt hạng mục vào tab Hồ sơ giải pháp

**Ngày:** 2026-04-25
**Module:** Assign (Giao việc)
**Màn hình:** `/assign/solutions/{id}/manager` → tab "Hồ sơ"

---

## 1. Mục tiêu

Hiện tại tab "Hồ sơ" trên trang quản lý giải pháp chỉ hiển thị hồ sơ trình duyệt của giải pháp (`solution_review_profiles`). PM phải vào từng trang manager của hạng mục để xem/duyệt hồ sơ trình duyệt hạng mục.

Yêu cầu: gộp hồ sơ trình duyệt của các hạng mục thuộc giải pháp vào cùng tab Hồ sơ, để PM duyệt tất cả tại một nơi.

---

## 2. Phạm vi

### Làm
- Mở rộng API `GET assign/solutions/{id}/manager/review-profiles` để trả cả hồ sơ hạng mục
- Thêm bộ lọc: Loại, Hạng mục, Version HM
- Thêm cột: Loại, Hạng mục vào bảng
- Tạo `ModuleApprovalViewModal` — modal xem + duyệt hồ sơ hạng mục
- Gọi trực tiếp API decision hiện có của hạng mục khi duyệt

### Không làm
- Không tạo/sửa hồ sơ hạng mục từ trang giải pháp (chỉ xem + duyệt)
- Không thay đổi flow duyệt hiện có
- Không sửa API decision của hạng mục
- Không sửa trang manager riêng của hạng mục

---

## 3. Quyền thao tác

| Vai trò | Hồ sơ giải pháp | Hồ sơ hạng mục |
|---------|-----------------|-----------------|
| PM | Tạo, sửa, gửi duyệt | Xem + duyệt/từ chối |
| Trưởng phòng | Duyệt/từ chối | Chỉ xem |

---

## 4. Backend

### 4.1. Mở rộng `SolutionService::getSolutionReviewProfiles()`

**File:** `Modules/Assign/Services/SolutionService.php`

**Thêm query params:**

| Param | Type | Default | Mô tả |
|-------|------|---------|-------|
| `type` | string | `all` | `all` / `solution` / `module` |
| `solution_module_id` | integer | null | Lọc theo hạng mục cụ thể |
| `module_version_id` | integer | null | Lọc theo version hạng mục |

**Logic xử lý:**

1. **Khi `type=all` hoặc `type=solution`:** Query `SolutionReviewProfile` như hiện tại (giữ nguyên filter keyword, status, solution_version_id, sent_date, review_deadline)

2. **Khi `type=all` hoặc `type=module`:** Query thêm `SolutionModuleReviewProfile`:
   - Lấy tất cả `solution_module_ids` thuộc giải pháp: `SolutionModule::where('solution_id', $solution->id)->pluck('id')`
   - Query `SolutionModuleReviewProfile::whereIn('solution_module_id', $moduleIds)`
   - Áp filter chung: keyword (tìm theo code), status, sent_date range, review_deadline range
   - Áp filter riêng: `solution_module_id`, `module_version_id`
   - Filter `solution_version_id` KHÔNG áp dụng cho hồ sơ hạng mục

3. **Merge + Sort + Paginate:**
   - Transform cả 2 tập dữ liệu sang cùng format (thêm field `type`, `module_id`, `module_name`, `module_version_code`)
   - Merge 2 collection thành 1
   - Sort theo field được yêu cầu (`sort_by`, `sort_desc`)
   - Paginate thủ công: `$merged->forPage($page, $perPage)`
   - Tính toán meta pagination: total, last_page, from, to

**Response format cho mỗi record:**

```php
[
    'id' => $profile->id,
    'code' => $profile->code,
    'content' => $profile->content,
    'status' => $profile->status,
    'status_name' => $statusName,
    'status_color' => $statusColor,
    'sent_date' => $formattedSentDate,
    'review_deadline' => $formattedDeadline,
    'created_at' => $formattedCreatedAt,
    'created_by_name' => $createdByName,

    // Fields mới
    'type' => 'solution' | 'module',
    'module_id' => null | $moduleId,
    'module_name' => null | $moduleName,
    'solution_version_code' => $solutionVersionCode | null,  // chỉ có khi type=solution
    'module_version_code' => null | $moduleVersionCode,       // chỉ có khi type=module
    'version_display' => $solutionVersionCode ?? $moduleVersionCode, // để hiển thị chung 1 cột

    // Giữ nguyên các field hiện có
    'files' => [...],
    'bom_lists' => [...],
    'is_can_edit' => ...,
    'is_can_decide' => ...,
]
```

**Lưu ý `is_can_decide` cho hồ sơ hạng mục:** Chỉ true khi người đăng nhập là PM của giải pháp VÀ status = `pending`.

### 4.2. Thêm API lấy danh sách hạng mục của giải pháp (nếu chưa có)

Kiểm tra xem đã có API trả về danh sách hạng mục (`solution_modules`) theo giải pháp chưa. Nếu chưa, thêm endpoint đơn giản trả `[{ id, name }]` để frontend dùng cho filter.

---

## 5. Frontend

### 5.1. Mở rộng `ReviewProfilesTab.vue`

**File:** `pages/assign/solutions/components/manager/ReviewProfilesTab.vue`

**Bộ lọc thêm:**

| Filter | Component | Options | Điều kiện hiện |
|--------|-----------|---------|---------------|
| Loại | V2BaseSelect | `[{ id: 'all', name: 'Tất cả' }, { id: 'solution', name: 'Giải pháp' }, { id: 'module', name: 'Hạng mục' }]` | Luôn hiện |
| Hạng mục | V2BaseSelect | Load từ API modules của solution | Khi type = `all` hoặc `module` |
| Version HM | V2BaseSelect | Load versions của hạng mục đã chọn | Khi đã chọn hạng mục cụ thể |

**Khi đổi filter Loại:**
- Nếu chọn `solution` → ẩn filter Hạng mục + Version HM, reset giá trị về null
- Nếu chọn `module` hoặc `all` → hiện filter Hạng mục
- Khi đổi Hạng mục → reset Version HM, load lại versions

**Cột bảng mới (thứ tự):**

| # | Cột | Field | Ghi chú |
|---|-----|-------|---------|
| 1 | STT | index | |
| 2 | Mã / Nội dung | code, content | Giữ nguyên V2BaseTitleSubInfo |
| 3 | Loại | type | V2BaseBadge — "Giải pháp" (xanh dương) / "Hạng mục" (tím) |
| 4 | Hạng mục | module_name | Trống nếu type=solution |
| 5 | Version | version_display | Hiển thị version GP hoặc version HM tuỳ type |
| 6 | Trạng thái | status_name, status_color | V2BaseBadge |
| 7 | Ngày gửi | sent_date | |
| 8 | Hạn duyệt | review_deadline | |

**Hành động khi click row:**
- `type=solution` → mở `SolutionApprovalModal` (giữ nguyên logic hiện tại)
- `type=module` → mở `ModuleApprovalViewModal` mới

### 5.2. Component mới: `ModuleApprovalViewModal`

**File:** `pages/assign/solutions/components/manager/ModuleApprovalViewModal.vue`

**Props:**
- `solutionId` — ID giải pháp (để xác định quyền PM)
- `currentEmployeeId` — ID nhân viên hiện tại

**Method `open(profileData)`:** Nhận data row từ bảng, gọi API detail hiện có `assign/solution-modules/{moduleId}/manager/review-profiles` để lấy chi tiết đầy đủ (hoặc dùng data đã có nếu đủ).

**Layout cột trái:**
- Nội dung trình duyệt — render HTML readonly (dùng `v-html`)
- File đính kèm — `FileAttachmentTable` ở chế độ readonly (chỉ xem + download)
- BOM tổng hợp — hiển thị readonly
- Bình luận — comment thread (`solution_module_review_profile` type)

**Layout cột phải:**
- Dự án / Giải pháp / Hạng mục
- PM hạng mục
- Ngày triển khai, hạn duyệt, ngày gửi
- Người duyệt

**Footer buttons:**
- Khi `isPM && status === 'pending'`:
  - Nút "Từ chối" (secondary, đỏ) → confirm dialog nhập lý do → gọi `POST assign/solution-modules/{moduleId}/manager/review-profiles/{id}/decision` với `{ action: 'reject', reason_deny: '...' }`
  - Nút "Duyệt" (primary, xanh) → confirm → gọi API decision với `{ action: 'approve' }`
- Còn lại: chỉ nút "Đóng"

**Sau khi duyệt/từ chối:** Emit event để `ReviewProfilesTab` reload lại danh sách.

**Xác định `isPM`:** So sánh `currentEmployeeId` với PM của giải pháp (truyền từ props hoặc lấy từ solution data).

---

## 6. Luồng hoạt động

```
PM mở tab Hồ sơ
  → FE gọi GET .../review-profiles?type=all
  → BE query solution_review_profiles + solution_module_review_profiles
  → BE merge, sort, paginate → trả response
  → FE render bảng gộp

PM click hồ sơ hạng mục (status=pending)
  → FE mở ModuleApprovalViewModal
  → PM xem nội dung, file, BOM
  → PM click "Duyệt"
  → FE gọi POST .../solution-modules/{moduleId}/manager/review-profiles/{id}/decision
  → BE xử lý duyệt (logic hiện có, không sửa)
  → FE đóng modal, reload bảng
```

---

## 7. Edge cases

- **Giải pháp không có hạng mục nào:** Bảng chỉ hiển thị hồ sơ giải pháp, filter Hạng mục dropdown rỗng
- **Hạng mục chưa có hồ sơ trình duyệt:** Không có record type=module, bảng chỉ hiện hồ sơ giải pháp
- **PM duyệt xong hồ sơ hạng mục:** Status cập nhật trong bảng, nút duyệt ẩn khi mở lại
- **Trưởng phòng mở modal hồ sơ hạng mục:** Chỉ thấy nội dung readonly, không có nút duyệt/từ chối
- **Sort xuyên 2 loại:** Sort theo sent_date hoặc review_deadline hoạt động đúng trên toàn bộ merged data
- **Filter kết hợp:** `type=module` + `solution_module_id` + `module_version_id` + `status` — tất cả AND logic
