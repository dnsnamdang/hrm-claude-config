# Design — Close Prospective Projects

**Ngày tạo:** 2026-04-19
**Người phụ trách:** @dnsnamdang
**Branch:** `tpe-develop-assign` (cả API + Client)

---

## 1. Scope & Nguyên tắc

### 1.1 Mục tiêu

Cho phép NV KD phụ trách dự án tiền khả thi bấm "Đóng dự án" khi dự án bị huỷ không thực hiện tiếp. Khi đóng:
- Lý do thất bại chọn từ danh mục `reason_project_failures` + ghi chú bổ sung.
- Toàn bộ công việc liên quan **dừng lại**: cascade 5 entity chính sang trạng thái Đóng.
- Thông báo đến các bên đang dính việc.
- **Không hỗ trợ mở lại** (no reopen).

### 1.2 Quyết định đã chốt (brainstorming 2026-04-19)

| # | Điểm | Quyết định |
|---|---|---|
| 1 | Khái niệm "Đóng" | Huỷ dự án không thực hiện tiếp → dừng toàn bộ công việc. |
| 2 | Tác nhân | Chỉ **NV KD phụ trách** (`prospective_projects.main_sale_employee_id === current employee id`). Admin KHÔNG override. |
| 3 | UI trigger | Button "Đóng dự án" trên `/assign/prospective-projects/:id/manager`. |
| 4 | Form nhập | Modal: dropdown "Nguyên nhân thất bại" (từ `reason_project_failures`) + textarea "Ghi chú" + checkbox xác nhận + warning "Không thể khôi phục". |
| 5 | Cascade 5 entity | ProspectiveProject → Solutions → SolutionModules → PricingRequests → Quotations đều chuyển sang "Đóng". Các entity khác (Task/Meeting/Issue/ReviewProfile) chưa quyết, để sau. |
| 6 | Reopen | KHÔNG hỗ trợ. |
| 7 | Notify | Gửi đến: (a) Creator của tất cả Solutions thuộc project, (b) PM các giải pháp, (c) NLG đang làm giá (Quotation status 1/2/3), (d) User có quyền TP đang pending duyệt (Quotation status 2/3), (e) User có quyền BGĐ đang pending duyệt (Quotation status 3). |

### 1.3 Không làm

- Không cascade Task/Meeting/Issue/ReviewProfile (user sẽ quyết sau).
- Không cho reopen.
- Không cho admin override (chỉ creator).
- Không xoá data — chỉ đổi status + snapshot lý do.

---

## 2. Data model

### 2.1 Migration `2026_04_19_100004_add_close_fields_to_prospective_projects`

```php
Schema::table('prospective_projects', function (Blueprint $t) {
    $t->unsignedBigInteger('closed_reason_id')->nullable()->after('status')
      ->comment('FK → reason_project_failures.id — lý do đóng');
    $t->text('closed_note')->nullable()->after('closed_reason_id')
      ->comment('Ghi chú bổ sung khi đóng');
    $t->timestamp('closed_at')->nullable()->after('closed_note');
    $t->unsignedBigInteger('closed_by')->nullable()->after('closed_at')
      ->comment('FK → users.id — người bấm đóng');
});
```

Không dùng `->foreign(...)` để tránh ràng buộc chéo module (convention project hiện có).

### 2.2 Status constants

**ProspectiveProject** (đã có — reuse):
- `STATUS_DONG_DU_AN = 11`

**Solution** (đã có — reuse):
- `STATUS_DONG = 2`

**SolutionModule** (thêm mới — hiện có 1, 2, 6, 8):
- `STATUS_DONG = 10`
- Label: `'Đóng'`

**PricingRequest** (thêm mới — hiện có 1..4):
- `STATUS_DONG = 5`
- Label: `'Đóng'`

**Quotation** (thêm mới — hiện có 1..4):
- `STATUS_DONG = 5`
- Label: `'Đóng'` (color: `#6B7280` xám)

### 2.3 Bảng `reason_project_failures` (đã có sẵn)

Entity `Modules\Assign\Entities\ReasonProjectFailure`. Không sửa schema, chỉ dùng cho dropdown + FK.

---

## 3. Business rules

### 3.1 Precondition để đóng

- User hiện tại là NV KD phụ trách: `auth.user.employee_id === project.main_sale_employee_id` (match qua `Employee` entity).
- Project chưa đóng: `status !== STATUS_DONG_DU_AN` (11).
- `closed_reason_id` phải tồn tại trong `reason_project_failures`.
- `closed_note` optional, max 500 chars.

### 3.2 Flow đóng

```
1. User click "Đóng dự án" trên manager.vue.
2. FE load dropdown reason_project_failures → show CloseProjectModal.
3. User chọn reason + nhập note + tick checkbox xác nhận.
4. FE gọi POST /api/v1/assign/prospective-projects/:id/close.
5. BE validate → DB transaction:
   a. Update project: status=11, closed_reason_id, closed_note, closed_at=now(), closed_by=user.
   b. Cascade Solutions: status=2 (Đóng), updated_by=user. Chỉ update solution chưa ở status Đóng/Chốt.
   c. Cascade SolutionModules: status=10.
   d. Cascade PricingRequests: status=5. Chỉ update request status 1/2/3 (không update 4 "Đã có báo giá").
   e. Cascade Quotations: status=5. Chỉ update quotation status 1/2/3 (không update 4 "Đã duyệt").
   f. Log vào `quotation_histories` cho các quotation bị cascade: action='closed_by_project', meta={project_id, reason_id, note}.
   g. Collect notification targets → gửi notification sau transaction commit.
6. FE nhận response → toast success → reload manager page (hiện banner đỏ + ẩn buttons).
```

### 3.3 Notify targets (Q3-B)

Sau transaction commit, gửi notification type `project_closed`:

| Target | Điều kiện |
|---|---|
| Creator của Solutions | Tất cả `solutions.created_by` của project |
| PM giải pháp | `solutions.pm_id` hoặc field PM tương ứng (xác định qua entity Solution) |
| NLG đang làm giá | `quotations.created_by` của quotation status 1/2/3 trước khi cascade |
| User có quyền TP | Tất cả user có permission "Trưởng phòng duyệt giá Bom giải pháp" — nếu có quotation status 2 trước khi cascade |
| User có quyền BGĐ | Tất cả user có permission "Ban giám đốc duyệt giá Bom giải pháp" — nếu có quotation status 3 trước khi cascade |

Message: `Dự án "[project_name]" đã được đóng bởi [NV KD]. Lý do: [reason_name]. Các giải pháp/hạng mục/báo giá liên quan đã tự động chuyển sang trạng thái Đóng.`

Link: `/assign/prospective-projects/:id/manager`

Dùng helper `EmployeeInfoService::sendToAllNotification` (pattern Phase 11).

### 3.4 Post-close readonly

Project sau đóng: tất cả action button ẩn, tab edit readonly, banner đỏ hiển thị lý do + ghi chú + ngày + người đóng.

Các entity cascade: màn edit của Solution/Module/Quotation/PricingRequest phải check status trước khi render form — nếu đóng → readonly + hiển thị warning "Thuộc dự án đã đóng, không thể chỉnh sửa".

---

## 4. API endpoints

### 4.1 Endpoint mới

```
POST /api/v1/assign/prospective-projects/{id}/close
Body: { "closed_reason_id": 3, "closed_note": "Khách từ chối báo giá" }
Response 200: {
    "data": {
        "id": 167,
        "status": 11,
        "closed_at": "2026-04-19 21:00:00",
        "closed_by_name": "Nguyễn Văn A",
        "closed_reason": { "id": 3, "name": "Khách từ chối giá" },
        "cascade": {
            "solutions": 2,
            "solution_modules": 5,
            "pricing_requests": 1,
            "quotations": 3
        }
    }
}
Response 422: creator validate fail / reason_id missing / already closed
Response 403: user không phải creator
```

### 4.2 Endpoint đã có dùng lại

- `GET /api/v1/assign/reason-project-failures/getAll` (nếu đã có) — load dropdown reason.
- `GET /api/v1/assign/prospective-projects/{id}` — detail trả thêm closed_* fields.

---

## 5. UI

### 5.1 Manager page — `/assign/prospective-projects/:id/manager`

**Pre-close state:**
- Button "Đóng dự án" (danger, icon `ri-close-circle-line`) ở action bar trên cùng, cạnh button edit/delete.
  - Hiện khi: `project.status !== 11` AND `current_employee.id === project.main_sale_employee_id`.
- Click → mở `CloseProjectModal`.

**Post-close state:**
- Banner đỏ đầu trang:
  ```
  [⚠] Dự án đã đóng
  Lý do: [closed_reason.name]
  Ghi chú: [closed_note || '—']
  Đóng ngày: [closed_at format] bởi [closed_by_name]
  ```
- Tất cả action button (Sửa, Tạo YCBG, Yêu cầu XD giá, v.v.) ẩn.
- Các tab show data readonly (tận dụng `:disabled="true"` pattern đã có trên manager.vue).

### 5.2 Component mới — `CloseProjectModal.vue`

**Props:** `projectId`, `projectName`, `show`.

**Template:**
```
[Modal title] Đóng dự án "[projectName]"

[Warning alert đỏ] ⚠ Đóng dự án sẽ huỷ toàn bộ công việc đang thực hiện:
  - Các giải pháp chuyển sang Đóng.
  - Các hạng mục giải pháp chuyển sang Đóng.
  - Các yêu cầu xây dựng giá chuyển sang Đóng.
  - Các báo giá đang soạn/chờ duyệt chuyển sang Đóng.
  Hành động này KHÔNG THỂ khôi phục.

[Required] Nguyên nhân thất bại:  [V2BaseSelect dropdown từ reason_project_failures]
[Optional] Ghi chú bổ sung:       [V2BaseTextarea max 500 chars]

[Checkbox] Tôi xác nhận muốn đóng dự án này.

[Button Light]  Huỷ
[Button Danger] Xác nhận đóng (disabled đến khi chọn reason + tick checkbox)
```

**Events:**
- `@closed(data)` — parent reload.
- `@cancel` — close modal.

### 5.3 Các entity cascade — UI readonly

**Solution edit page:** check `solution.status === Solution::STATUS_DONG` → hiển thị banner + readonly tất cả field.

**Quotation edit/show:** check `quotation.status === 5 (Đóng)` → banner đỏ "Báo giá đã đóng (dự án đã đóng)" + disable mọi action.

**Pricing request edit:** tương tự.

Pattern: status `Đóng` ở bất kỳ entity nào → full readonly. Màn show vẫn cho xem data lịch sử.

---

## 6. Risks

1. **Cascade transaction lớn:** nếu project có nhiều solution/module/báo giá (>100 record), transaction có thể lâu.  
   → Mitigation: dùng `update()` batch (không load model), index đầy đủ trên foreign keys.

2. **Race: user khác đang edit quotation của project bị đóng cùng lúc.**  
   → Mitigation: entity edit check status mỗi lần save. Nếu status đã đổi sang Đóng → trả 422 "Không thể lưu, báo giá đã đóng".

3. **Notification volume:** nếu project có nhiều báo giá, email/notification nhiều.  
   → Mitigation: notify theo user id (dedup), 1 notification per user tối đa.

4. **Test coverage thấp:** feature ảnh hưởng 5 entity, dễ miss corner case.  
   → Mitigation: test checklist chi tiết trong plan (8 scenario end-to-end).

5. **`reason_project_failures` endpoint có thể chưa có `getAll` theo convention.**  
   → Mitigation: verify endpoint trước, nếu chưa có thì tạo mới (BE task).

---

## 7. Future enhancements (không làm phase này)

- Reopen project (tạo request + 2 bước duyệt).
- Cascade Task/Meeting/Issue/ReviewProfile.
- Report "Dự án thất bại" theo nguyên nhân — dashboard thống kê reason_project_failure.
- Khả năng undo trong vòng X giờ.
