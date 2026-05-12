# SRS: Quản lý Khoá học (Subject Builder)

| Thông tin | Chi tiết |
|-----------|----------|
| Module | Training (Đào tạo) |
| Phiên bản | 1.0 |
| Ngày tạo | 2026-05-12 |
| Người tạo | @junfoke |
| Trạng thái | Draft |

---

## 1. Giới thiệu

### 1.1. Mục đích

Rebuild màn tạo/sửa Khoá học (subjects) từ form đơn giản lên giao diện builder 4 tab đầy đủ: Thông tin, Cấu hình đánh giá, Cấu hình người học, Chứng chỉ. Đổi label "Môn học" → "Khoá học" trên toàn bộ màn subjects. Chuẩn hoá dữ liệu backend bằng các bảng mới thay cho JSON `evaluation_config` cũ.

### 1.2. Phạm vi

**Trong scope:**
- Màn danh sách khoá học: filter, phân trang, khoá/mở khoá, xoá
- Màn tạo mới / chỉnh sửa khoá học: builder 4 tab (Thông tin, Đánh giá, Người học, Chứng chỉ)
- Lưu tạm (DRAFT) — bỏ qua validation chi tiết, chỉ cần `name`
- Cấu hình chương & bài học: có/không có chương, drag-drop sắp xếp, prerequisite
- Cấu hình đánh giá: completion rule hoặc exam (đề thi + người chấm + thời gian)
- Cấu hình người học: onboarding, đối tượng bắt buộc / khuyến nghị (phòng ban / chức vụ / năng lực)
- Cấu hình chứng chỉ: upload ảnh nền, 4 trường text overlay, canvas preview, tải PDF
- Upload ảnh banner khoá học
- 3 field mô tả chi tiết: `what_includes`, `for_who`, `will_learn` (nhập bằng BulletListEditor)

**Ngoài scope:**
- Export Excel (đã có, không thay đổi)
- Job onboarding auto-assign
- Render PDF chứng chỉ thực (chỉ preview + download cục bộ)
- Màn downstream: training_programs, courses, training_plans, reports — giữ nguyên logic
- Permission phân cấp theo phòng ban/chi nhánh

### 1.3. Thuật ngữ

| Thuật ngữ | Giải thích |
|-----------|-----------|
| Subject | Khoá học (entity chính trong bảng `subjects`) |
| Subject Exam | Bài thi được gắn vào khoá học (bảng `subject_exams`) |
| Subject Assignee | Đối tượng học polymorphic: phòng ban / chức vụ / năng lực (`subject_assignees`) |
| Subject Chapter | Chương của khoá học (`subject_chapters`) |
| Subject Lesson | Bài học trong khoá học (`subject_lessons`, pivot giữa subject ↔ lesson) |
| DRAFT | Trạng thái Nháp (status=3), lưu tạm chưa hoàn thiện |
| Prerequisite | Điều kiện mở khoá: phải hoàn thành bài học X trước mới học bài Y |
| Onboarding | Tự động giao khoá học cho nhân viên mới theo cấu hình ngày |
| evaluation_mode | Phương thức đánh giá: `completion` (tiêu chí hoàn thành) hoặc `exam` (thi đề) |

---

## 2. Actors & Permissions

| Actor | Mô tả | Permissions |
|-------|-------|-------------|
| Admin / HR | Quản trị viên hệ thống | Toàn quyền: tạo, sửa, xoá, khoá/mở khoá |
| Manager Đào tạo | Cán bộ phụ trách đào tạo | Xem + tạo + sửa khoá học, không xoá |
| Nhân viên | Người dùng cuối | Chỉ xem (các màn tự học, không vào subject builder) |

> Permission key: `Quản lý khoá học` (renamed từ `Quản lý môn học`, giữ nguyên permission_id).

---

## 3. Use Cases

### UC-01: Xem danh sách khoá học

| | |
|---|---|
| **Actor** | Admin / Manager Đào tạo |
| **Precondition** | Đã đăng nhập, có quyền `Quản lý khoá học` |
| **Main Flow** | |
| 1 | Truy cập `/training/subjects` |
| 2 | Hệ thống hiển thị bảng danh sách khoá học, hỗ trợ filter theo: tên/mã, loại đào tạo, trạng thái (Hoạt động / Khoá / Nháp), phân trang |
| 3 | Mỗi row hiển thị: mã, tên, loại đào tạo, trạng thái badge (xanh/đỏ/xám), nút sửa, khoá/mở khoá, xoá |
| **Postcondition** | Danh sách hiển thị đúng filter |
| **Alternative Flow** | Không có dữ liệu → hiển thị empty state |
| **Exception** | Token hết hạn → redirect login |

---

### UC-02: Tạo mới khoá học

| | |
|---|---|
| **Actor** | Admin / Manager Đào tạo |
| **Precondition** | Đã đăng nhập, có quyền `Quản lý khoá học` |
| **Main Flow** | |
| 1 | Click "Tạo mới" → chuyển sang `/training/subjects/add` |
| 2 | Builder mở với 4 tab: Thông tin, Cấu hình đánh giá, Cấu hình người học, Chứng chỉ |
| 3 | Điền thông tin cần thiết (ít nhất `name`), cấu hình các tab |
| 4 | Click "Lưu tạm" → gọi `POST /store-builder` với `status=3` (DRAFT), chỉ validate `name` |
| 4a | Hoặc click "Lưu" → validate đầy đủ theo `evaluation_mode`, `onboarding_enabled`, `certificate_enabled`; gọi `POST /store-builder` |
| 5 | Backend tạo subject + sync chapters/lessons + exams + assignees + certificate_fields trong 1 transaction |
| 6 | Nếu `code` rỗng, BE auto-gen `SUB-YYYY-XXXX` |
| 7 | Redirect về danh sách, toast thành công |
| **Postcondition** | Subject mới được tạo trong DB, trạng thái theo `status` gửi lên |
| **Alternative Flow** | Validation lỗi → FE hiển thị lỗi inline, tự chuyển đúng tab có lỗi |
| **Exception** | Mã khoá học trùng → lỗi 422 `code: Mã khoá học đã tồn tại` |

---

### UC-03: Chỉnh sửa khoá học

| | |
|---|---|
| **Actor** | Admin / Manager Đào tạo |
| **Precondition** | Khoá học tồn tại, status = Hoạt động hoặc Nháp (status=1 hoặc 3) |
| **Main Flow** | |
| 1 | Click icon sửa ở danh sách → chuyển sang `/_id/index` |
| 2 | FE gọi `GET /subjects/{id}/builder` → load toàn bộ dữ liệu 4 tab |
| 3 | Builder hiển thị đầy đủ dữ liệu đã lưu (chapters, exams, assignees, cert fields) |
| 4 | Chỉnh sửa, click "Lưu" → gọi `POST /subjects/{id}/builder` |
| 5 | BE update subject + re-sync tất cả relation trong transaction |
| **Postcondition** | Subject được cập nhật, timestamp `updated_at` + `updated_by` cập nhật |
| **Alternative Flow** | Subject status=Khoá → nút sửa bị disable, chỉ xem |
| **Exception** | Subject không tồn tại → 404 |

---

### UC-04: Lưu tạm (DRAFT)

| | |
|---|---|
| **Actor** | Admin / Manager Đào tạo |
| **Precondition** | Đang ở màn tạo hoặc sửa khoá học |
| **Main Flow** | |
| 1 | Click "Lưu tạm" |
| 2 | FE validate chỉ: `name` không được trống |
| 3 | Gọi API với `status=3`, bỏ qua validation chi tiết các tab |
| 4 | BE chỉ áp dụng rules: `name required`, `code unique`, `status in:1,2,3` |
| 5 | Khoá học được lưu với status=3 (Nháp) |
| **Postcondition** | Subject ở trạng thái DRAFT; không tạo row con (`subject_exams`, `subject_assignees`, ...) nếu dữ liệu tab chưa đủ |
| **Exception** | `name` rỗng → FE báo lỗi inline, không gọi API |

---

### UC-05: Cấu hình chương & bài học (Tab 1)

| | |
|---|---|
| **Actor** | Admin / Manager Đào tạo |
| **Precondition** | Đang trong builder, Tab "Thông tin" |
| **Main Flow** | |
| 1 | Toggle "Có chương" (use_chapters=1): kéo thả chương, mỗi chương thêm bài học từ ngân hàng |
| 1a | Toggle "Không có chương" (use_chapters=2): bài học thẳng vào khoá học |
| 2 | Với mỗi bài học, click icon ⓘ để xem/ghi đè tiêu chí hoàn thành |
| 3 | Toggle "Bật điều kiện mở khoá" → multi-select bài học prerequisite |
| 4 | Kéo thả để sắp xếp thứ tự chương / bài học |
| **Postcondition** | `chapters`, `subject_lessons` được sync đúng |
| **Business Rule** | Đổi use_chapters 1→2: xoá sạch chapters, set `chapter_id=null` cho lessons; Đổi 2→1: xoá lessons cũ, dùng chapters mới |
| **Exception** | Bài học bị xoá khi là prerequisite → `prerequisite_subject_lesson_ids` được clean tự động |

---

### UC-06: Cấu hình đánh giá (Tab 2)

| | |
|---|---|
| **Actor** | Admin / Manager Đào tạo |
| **Precondition** | Đang trong builder, Tab "Cấu hình đánh giá" |
| **Main Flow — Completion mode** | |
| 1 | Chọn `evaluation_mode=completion` |
| 2 | Chọn `rule`: all_required / percent / weighted |
| 3 | Nếu rule=percent: nhập `percent` (1-100) + `percent_mode` |
| **Main Flow — Exam mode** | |
| 1 | Chọn `evaluation_mode=exam` |
| 2 | Chọn ≥1 đề thi từ danh sách |
| 3 | Mỗi đề thi: nhập time_limit_min, pass_score_percent; chọn người chấm (nếu đề có tự luận) |
| 4 | Nhập `exam_attempt_limit` (số lần thi tối đa) |
| 5 | Chọn `exam_score_rule` (highest / last / average) |
| 6 | Toggle `exam_participation_required`: nếu ON → nhập `exam_min_required_percent` |
| **Postcondition** | `subject_exams`, `subject_exam_graders` được sync; chuyển mode → xoá dữ liệu mode cũ |
| **Business Rule** | Đề thi có câu tự luận (essay_count > 0) → FE bắt buộc chọn grader_ids |

---

### UC-07: Cấu hình người học (Tab 3)

| | |
|---|---|
| **Actor** | Admin / Manager Đào tạo |
| **Precondition** | Đang trong builder, Tab "Cấu hình người học" |
| **Main Flow** | |
| 1 | Toggle Onboarding: ON → nhập `onboarding_new_employee_days` và `onboarding_must_finish_days` |
| 2 | Chọn loại đối tượng bắt buộc (Phòng ban / Chức vụ / Năng lực) → multi-select → chip list |
| 3 | Tương tự cho đối tượng khuyến nghị |
| **Postcondition** | `subject_assignees` được sync đúng với `is_mandatory=1/0` |
| **Business Rule** | `onboarding_new_employee_days=0` = luôn coi là nhân viên mới; `onboarding_must_finish_days=0` = không deadline |

---

### UC-08: Cấu hình chứng chỉ (Tab 4)

| | |
|---|---|
| **Actor** | Admin / Manager Đào tạo |
| **Precondition** | Đang trong builder, Tab "Chứng chỉ" |
| **Main Flow** | |
| 1 | Toggle `certificate_enabled=1` |
| 2 | Upload ảnh nền → URL được lưu vào `certificate_template_url` |
| 3 | Cấu hình 4 trường: `course_name`, `employee_name`, `issued_date`, `signer` (text, X, Y, font_size, font_weight) |
| 4 | Canvas preview (1600×900) render real-time |
| 5 | Button "Download PDF" → jsPDF tạo file từ canvas |
| **Postcondition** | `certificate_enabled`, `certificate_template_url`, 4 `certificate_fields` được lưu |
| **Business Rule** | Nếu `certificate_enabled=1` → `certificate_template_url` required + `certificate_fields` phải đủ 4 trường |

---

### UC-09: Khoá / Mở khoá khoá học

| | |
|---|---|
| **Actor** | Admin / Manager Đào tạo |
| **Precondition** | Khoá học tồn tại |
| **Main Flow** | |
| 1 | Click icon khoá/mở khoá ở danh sách |
| 2 | Hiển thị dialog xác nhận (BaseConfirmModal) với title/message động theo trạng thái hiện tại |
| 3 | Xác nhận → gọi `GET /subjects/{id}/lock` hoặc `/unlock` |
| 4 | Danh sách refresh, badge trạng thái cập nhật |
| **Postcondition** | `status` chuyển từ 1→2 (khoá) hoặc 2→1 (mở) |

---

### UC-10: Xoá khoá học

| | |
|---|---|
| **Actor** | Admin |
| **Precondition** | Khoá học `is_can_delete=true` |
| **Main Flow** | |
| 1 | Click icon xoá → confirm dialog |
| 2 | Gọi `DELETE /subjects/{id}/builder` |
| **Postcondition** | Subject bị xoá, các relation con bị xoá cascade |
| **Business Rule** | DRAFT luôn xoá được; status≠DRAFT không xoá được nếu có reference trong: `course_requests`, `training_requests`, `training_planning_subjects`, `training_program_subject`, `courses` |

---

## 4. Business Rules

| ID | Rule | Mô tả | Áp dụng tại |
|----|------|-------|-------------|
| BR-01 | DRAFT skip validation | status=3 chỉ validate `name` + `code unique` | UC-04, SubjectBuilderRequest |
| BR-02 | Auto-gen code | Sau khi tạo, nếu `code` rỗng → BE sinh `SUB-YYYY-XXXX` | UC-02, SubjectService::storeWithStructure |
| BR-03 | Code unique per company | `code` phải unique trong bảng `subjects` (bỏ qua chính nó khi update) | UC-02, UC-03 |
| BR-04 | use_chapters đổi 1→2 | Xoá tất cả chapters; lesson chapter_id=null | UC-05, SubjectService::syncChaptersAndLessons |
| BR-05 | evaluation_mode đổi | Khi save, xoá toàn bộ `subject_exams` + `subject_exam_graders` cũ rồi insert mới | UC-06, SubjectService::syncExams |
| BR-06 | is_can_delete DRAFT | DRAFT luôn trả `is_can_delete=true` bỏ qua check reference | UC-10, Subject::getIsCanDeleteAttribute |
| BR-07 | is_can_delete non-DRAFT | Không xoá được nếu tồn tại reference trong 5 bảng downstream | UC-10, Subject::getIsCanDeleteAttribute |
| BR-08 | Cert fields 4 trường | `certificate_enabled=1` → phải có đủ 4 trường (size:4) | UC-08, SubjectBuilderRequest |
| BR-09 | Grader khi có essay | FE validate: exam có `essay_count > 0` → bắt buộc `grader_ids` (BE validate tạm comment out) | UC-06, SubjectBuilderForm::validate() |
| BR-10 | Sync atomic | storeWithStructure / updateWithStructure bọc DB::transaction | UC-02, UC-03 |
| BR-11 | exam_participation_required | Nếu `exam_participation_required=1` → `exam_min_required_percent` required (1-100) | UC-06, SubjectBuilderRequest |
| BR-12 | Onboarding days | Nếu `onboarding_enabled=1` → `onboarding_new_employee_days` + `onboarding_must_finish_days` required | UC-07, SubjectBuilderRequest |

---

## 5. Data Model

### 5.1. Entity Relationship

```
Subject 1──N SubjectChapter 1──N SubjectLesson N──1 Lesson
Subject 1──N SubjectLesson (chapter_id=null khi use_chapters=false)
Subject 1──N SubjectExam 1──N SubjectExamGrader N──1 Employee
Subject 1──N SubjectAssignee
Subject 1──N SubjectCertificateField
Subject N──1 TrainingType
Subject N──1 ExamKit (legacy, có thể null)
```

### 5.2. Bảng dữ liệu

#### Bảng: `subjects` (các cột liên quan đến feature)

| Cột | Type | Nullable | Default | Mô tả |
|-----|------|----------|---------|-------|
| id | bigint PK | No | auto | |
| code | varchar(50) | Yes | null | Auto-gen `SUB-YYYY-XXXX` nếu rỗng |
| name | varchar(255) | No | — | Tên khoá học |
| banner_url | varchar(500) | Yes | null | URL ảnh banner (Phase 16) |
| status | tinyint | Yes | 1 | 1=Hoạt động, 2=Khoá, 3=Nháp |
| training_type_id | bigint FK | Yes | null | |
| description | text | Yes | null | Mô tả ngắn |
| what_includes | text | Yes | null | Khoá học này có gì? (HTML) |
| for_who | text | Yes | null | Dành cho ai? (HTML) |
| will_learn | text | Yes | null | Bạn sẽ học được gì? (HTML) |
| use_chapters | tinyint(1) | Yes | 1 | 1=có chương, 0=không chương |
| linear_required | tinyint(1) | Yes | 0 | 1=bắt buộc học tuần tự |
| evaluation_mode | varchar | Yes | 'completion' | 'completion' / 'exam' |
| evaluation_config | json | Yes | null | Legacy config + completion rule |
| exam_score_rule | enum | Yes | null | 'highest' / 'last' / 'average' |
| exam_attempt_limit | int | Yes | null | Số lần thi tối đa |
| exam_participation_required | tinyint | Yes | 0 | 1=bắt buộc hoàn thành bài học trước khi thi |
| exam_min_required_percent | int | Yes | null | % bài học tối thiểu phải hoàn thành trước thi |
| onboarding_enabled | tinyint | Yes | 0 | 1=bật tự động giao khi onboarding |
| onboarding_new_employee_days | int | Yes | null | Trong bao nhiêu ngày được coi là mới |
| onboarding_must_finish_days | int | Yes | null | Phải hoàn thành trong bao nhiêu ngày |
| mandatory_assignee_type | varchar | Yes | null | 'department' / 'position' / 'capability' |
| recommended_assignee_type | varchar | Yes | null | 'department' / 'position' / 'capability' |
| certificate_enabled | tinyint | Yes | 0 | 1=cấp chứng chỉ |
| certificate_template_url | varchar(500) | Yes | null | URL ảnh nền chứng chỉ |
| company_id | bigint | Yes | null | |
| created_by | bigint | Yes | null | |
| updated_by | bigint | Yes | null | |
| created_at | timestamp | Yes | null | |
| updated_at | timestamp | Yes | null | |

#### Bảng: `subject_exams`

| Cột | Type | Nullable | Default | Mô tả |
|-----|------|----------|---------|-------|
| id | bigint PK | No | auto | |
| subject_id | bigint FK | No | — | |
| exam_id | bigint FK | No | — | ID đề thi (exam_kits) |
| time_limit_min | int | No | 0 | Thời gian làm bài (phút); 0=không giới hạn |
| pass_score_percent | int | No | 60 | Điểm đạt (%) |
| sort_order | int | No | 0 | |

#### Bảng: `subject_exam_graders`

| Cột | Type | Nullable | Default | Mô tả |
|-----|------|----------|---------|-------|
| id | bigint PK | No | auto | |
| subject_exam_id | bigint FK | No | — | |
| employee_id | bigint FK | No | — | |

#### Bảng: `subject_assignees`

| Cột | Type | Nullable | Default | Mô tả |
|-----|------|----------|---------|-------|
| id | bigint PK | No | auto | |
| subject_id | bigint FK | No | — | |
| assignee_type | enum | No | — | 'department' / 'position' / 'capability' |
| assignee_id | bigint | No | — | ID của phòng ban / chức vụ / năng lực |
| is_mandatory | tinyint | No | 0 | 1=bắt buộc, 0=khuyến nghị |

#### Bảng: `subject_certificate_fields`

| Cột | Type | Nullable | Default | Mô tả |
|-----|------|----------|---------|-------|
| id | bigint PK | No | auto | |
| subject_id | bigint FK | No | — | |
| field_key | enum | No | — | 'course_name' / 'employee_name' / 'issued_date' / 'signer' |
| text | varchar(255) | Yes | null | Text hiển thị (null = auto cho employee_name, issued_date) |
| x | int | No | 800 | Tọa độ X trên canvas 1600×900 |
| y | int | No | 450 | Tọa độ Y |
| font_size | int | No | 32 | |
| font_weight | int | No | 500 | 400/500/600/700/800 |

### 5.3. Enum Values

| Entity | Constant | Value | Meaning |
|--------|----------|-------|---------|
| Subject | HOAT_DONG | 1 | Hoạt động |
| Subject | KHOA | 2 | Khoá |
| Subject | STATUS_DRAFT | 3 | Nháp |
| Subject | evaluation_mode | 'completion' | Đánh giá theo tiêu chí hoàn thành |
| Subject | evaluation_mode | 'exam' | Đánh giá theo thi đề |
| Subject | exam_score_rule | 'highest' | Lấy điểm cao nhất |
| Subject | exam_score_rule | 'last' | Lấy điểm lần cuối |
| Subject | exam_score_rule | 'average' | Lấy điểm trung bình |
| SubjectAssignee | assignee_type | 'department' | Phòng ban |
| SubjectAssignee | assignee_type | 'position' | Chức vụ (working_position) |
| SubjectAssignee | assignee_type | 'capability' | Năng lực |
| SubjectCertificateField | field_key | 'course_name' | Tên khoá học |
| SubjectCertificateField | field_key | 'employee_name' | Tên học viên |
| SubjectCertificateField | field_key | 'issued_date' | Ngày cấp |
| SubjectCertificateField | field_key | 'signer' | Người ký |

---

## 6. API Specification

> Prefix: `/api/v1/training`  
> Auth: `Bearer Token (JWT)`  
> Permission middleware: `Quản lý khoá học`

### 6.1. Danh sách khoá học

```
GET /subjects
```

**Query params:**

| Field | Type | Mô tả |
|-------|------|-------|
| search | string | Tìm theo tên/mã |
| training_type_id | int | Lọc loại đào tạo |
| status | int | Lọc trạng thái (1/2/3) |
| page | int | Trang hiện tại |
| limit | int | Số item/trang |

---

### 6.2. Tạo khoá học (Builder)

```
POST /subjects/store-builder
Content-Type: application/json
```

**Request body:**

| Field | Type | Required | Validate | Mô tả |
|-------|------|----------|----------|-------|
| name | string | Yes | max:255 | Tên khoá học |
| status | int | Yes | in:1,2,3 | 1/2/3 |
| code | string | No | max:50, unique | Bỏ trống để auto-gen |
| description | string | No | — | |
| banner_url | string | No | max:500 | URL ảnh banner |
| what_includes | string | No | — | HTML |
| for_who | string | No | — | HTML |
| will_learn | string | No | — | HTML |
| training_type_id | int | No | exists:training_types,id | |
| use_chapters | int | No | in:1,2 | 1=có, 2=không |
| linear_required | int | No | in:1,2 | |
| evaluation_mode | string | No | in:completion,exam | |
| evaluation_config | object | No | — | `{rule, percent, percent_mode}` khi completion |
| chapters | array | Cond | required_if:use_chapters,1 | |
| chapters.*.code | string | Yes (khi có chapters) | max:50 | |
| chapters.*.name | string | Yes (khi có chapters) | max:255 | |
| chapters.*.subject_lessons | array | Cond | required_if:use_chapters,1 | |
| chapters.*.subject_lessons.*.lesson_id | int | Yes | exists:lessons,id | |
| subject_lessons | array | Cond | required_if:use_chapters,2 | |
| subject_exams | array | Cond | required khi exam mode | |
| subject_exams.*.exam_id | int | Yes | — | |
| subject_exams.*.time_limit_min | int | Yes | min:0 | |
| subject_exams.*.pass_score_percent | int | Yes | min:0,max:100 | |
| subject_exams.*.grader_ids | array | No | — | |
| exam_attempt_limit | int | Cond | required khi exam, min:1 | |
| exam_score_rule | string | Cond | required khi exam, in:highest,last,average | |
| exam_participation_required | int | No | in:0,1 | |
| exam_min_required_percent | int | Cond | required nếu participation=1, min:1,max:100 | |
| onboarding_enabled | int | No | in:0,1 | |
| onboarding_new_employee_days | int | Cond | required khi onboarding=1, min:0 | |
| onboarding_must_finish_days | int | Cond | required khi onboarding=1, min:0 | |
| mandatory_assignee_type | string | No | in:department,position,capability | |
| recommended_assignee_type | string | No | in:department,position,capability | |
| subject_assignees | array | No | — | |
| subject_assignees.*.assignee_type | string | Yes | in:department,position,capability | |
| subject_assignees.*.assignee_id | int | Yes | — | |
| subject_assignees.*.is_mandatory | int | Yes | in:0,1 | |
| certificate_enabled | int | No | in:0,1 | |
| certificate_template_url | string | Cond | required khi cert=1, max:500 | |
| certificate_fields | array | Cond | required khi cert=1, size:4 | |
| certificate_fields.*.field_key | string | Yes | in:course_name,...,signer | |
| certificate_fields.*.x | int | Yes | — | |
| certificate_fields.*.y | int | Yes | — | |
| certificate_fields.*.font_size | int | Yes | min:10 | |
| certificate_fields.*.font_weight | int | Yes | in:400,500,600,700,800 | |

> **Lưu ý DRAFT:** Khi `status=3`, chỉ validate `name` + `code`. Các field khác được bỏ qua.

**Response (200):**
```json
{
  "message": "success",
  "status": 200,
  "data": { /* SubjectDetailResource */ }
}
```

**Error cases:**

| HTTP Code | Condition | Message |
|-----------|-----------|---------|
| 422 | name rỗng | `Tên khoá học là bắt buộc` |
| 422 | code trùng | `Mã khoá học đã tồn tại` |
| 422 | exam mode, không có đề thi | `Phải cấu hình ít nhất một bài thi` |
| 422 | cert=1, thiếu ảnh | `Chưa chọn ảnh mẫu chứng chỉ` |
| 422 | cert=1, thiếu trường | `Phải cấu hình đủ 4 trường` |

---

### 6.3. Lấy chi tiết khoá học để edit

```
GET /subjects/{id}/builder
```

**Response (200):** `SubjectDetailResource` gồm:
```json
{
  "id": 1,
  "code": "SUB-2026-0001",
  "name": "Tên khoá học",
  "status": 1,
  "banner_url": "https://s3.../banner.jpg",
  "use_chapters": 1,
  "linear_required": 2,
  "evaluation_mode": "completion",
  "evaluation_config": { "rule": "all_required" },
  "what_includes": "<ul>...</ul>",
  "for_who": "<ul>...</ul>",
  "will_learn": "<ul>...</ul>",
  "chapters": [
    {
      "id": 1, "code": "CH01", "name": "Chương 1", "sort_order": 0,
      "subject_lessons": [
        {
          "id": 1, "lesson_id": 10, "required": 1,
          "override_completion": 1,
          "prerequisite_enabled": 2,
          "prerequisite_subject_lesson_ids": [],
          "lesson": { "id": 10, "code": "LS01", "name": "Bài 1", "type": 1, "type_text": "Video" }
        }
      ]
    }
  ],
  "subject_lessons": [],
  "subject_exams": [...],
  "subject_assignees": [...],
  "certificate_fields": [...],
  "exam_score_rule": null,
  "exam_attempt_limit": null,
  "onboarding_enabled": 0,
  "mandatory_assignee_type": null,
  "certificate_enabled": 0,
  "is_can_delete": true,
  "created_at": "2026-05-12 10:00:00",
  "updated_at": "2026-05-12 10:00:00"
}
```

---

### 6.4. Cập nhật khoá học

```
POST /subjects/{id}/builder
```

Request body giống UC-02 (6.2), thêm `id` là route param.

---

### 6.5. Xoá khoá học

```
DELETE /subjects/{id}/builder
```

**Error cases:**

| HTTP Code | Condition | Message |
|-----------|-----------|---------|
| 403 | `is_can_delete=false` | Không thể xoá vì có dữ liệu liên quan |
| 404 | Subject không tồn tại | — |

---

### 6.6. Khoá / Mở khoá

```
GET /subjects/{id}/lock
GET /subjects/{id}/unlock
```

---

## 7. UI Specification

### 7.1. Màn danh sách khoá học
- **Route**: `/training/subjects`
- **Layout**: bảng danh sách + filter panel

```
┌─────────────────────────────────────────────────┐
│  Khoá học          [Xuất Excel]  [+ Tạo mới]    │
├─────────────────────────────────────────────────┤
│  Tìm: [__________] Loại: [___] Trạng thái: [__] │
├─────────────────────────────────────────────────┤
│  Mã    │ Tên           │ Loại │ Trạng thái │ ... │
│  ──────┼───────────────┼──────┼────────────┼─── │
│  SUB.. │ Tên khoá học  │  ... │ ● Hoạt động│ ✏🔒🗑│
│        │               │      │ ● Nháp     │     │
│        │               │      │ ● Khoá     │     │
└─────────────────────────────────────────────────┘
```

**Trạng thái badge:**
- Hoạt động → badge xanh lá (`#16A34A`)
- Khoá → badge đỏ (`#DC2626`)
- Nháp → badge xám (`#64748B`)

---

### 7.2. Màn builder (tạo/sửa)
- **Route**: `/training/subjects/add` (tạo), `/training/subjects/_id/index` (sửa)

```
┌────────────────────────────────────────────────────────┐
│  Tạo khoá học                                          │
├────────────────────────────────────────────────────────┤
│  [Thông tin] [Cấu hình đánh giá] [Người học] [Chứng chỉ]│
├────────────────────────────────────────────────────────┤
│  ... nội dung tab ...                                   │
├────────────────────────────────────────────────────────┤
│  [Quay về]                  [Lưu tạm]  [Lưu]          │
└────────────────────────────────────────────────────────┘
```

**Tab 1 — Thông tin:**
- LEFT (col-5): Ảnh banner (BannerUploader), Loại đào tạo, Mã khoá học (disabled + button tạo ngẫu nhiên), Tên khoá học, Mô tả, What includes / For who / Will learn (BulletListEditor)
- RIGHT (col-7): Toggle Có/Không có chương, Toggle Học tuần tự, Builder chương-bài (drag-drop)

**Tab 2 — Cấu hình đánh giá:**
- Radio: Hoàn thành bài học / Thi đề
- Completion: rule, percent, percent_mode
- Exam: chọn đề thi, time_limit, pass_score, graders, attempt_limit, score_rule, participation_required

**Tab 3 — Cấu hình người học:**
- Toggle Onboarding + inputs ngày
- Pill selector (Phòng ban / Chức vụ / Năng lực) cho bắt buộc + khuyến nghị
- Chip list hiển thị các đối tượng đã chọn

**Tab 4 — Chứng chỉ:**
- Toggle bật chứng chỉ
- LEFT: upload template, 4 cert-field config (text, X, Y, font_size, font_weight)
- RIGHT: canvas preview 1600×900
- Buttons: Render lại, Download PDF

---

### 7.3. Component `BannerUploader`

- **File**: `hrm-client/components/shared/BannerUploader.vue`
- **Props**: `value` (String URL), `uploading` (Boolean), `disabled` (Boolean)
- **Emit**: `change(File)`, `remove()`
- **Behavior**: Khi chưa có ảnh → vùng click hình dashed. Khi có ảnh → hiển thị toàn chiều rộng + hover overlay "Đổi ảnh" + nút xóa. FileReader preview local, sau khi upload thành công switch sang URL server.

### 7.4. Component `BulletListEditor`

- **File**: `hrm-client/components/shared/BulletListEditor.vue`
- **Props**: `value` (String HTML), `disabled`, `height`
- **Toolbar**: B / I / U / BulletedList / Undo / Redo (CKEditor 5 minimal)
- **Output**: HTML string

---

## 8. Non-functional Requirements

- **Performance**: List API trả về trong 500ms với dataset thông thường (<10.000 subjects)
- **Security**: JWT auth bắt buộc; permission `Quản lý khoá học` được check tại middleware
- **Transaction**: storeWithStructure / updateWithStructure bọc `DB::transaction` để đảm bảo atomicity
- **Compatibility**: PHP 7.4, Laravel 8, Nuxt 2.14, Vue 2, Bootstrap-Vue 2.15
- **Browser**: Chrome, Firefox, Edge, Safari (canvas API, FileReader API)
- **Upload**: Ảnh banner + cert template dùng endpoint chung `/files/upload`, lưu AWS S3

---

## 9. Phụ lục

### 9.1. File references

| Layer | File path |
|-------|-----------|
| Migration (new cols) | `hrm-api/database/migrations/2026_04_22_*_add_course_config_columns_to_subjects_table.php` |
| Migration (banner) | `hrm-api/database/migrations/2026_05_12_000002_add_banner_url_to_subjects_table.php` |
| Migration (display info) | `hrm-api/database/migrations/2026_05_12_000001_add_detail_info_columns_to_subjects_table.php` |
| Entity | `hrm-api/Modules/Training/Entities/Subject.php` |
| Entity (SubjectExam) | `hrm-api/Modules/Training/Entities/SubjectExam.php` |
| Entity (SubjectAssignee) | `hrm-api/Modules/Training/Entities/SubjectAssignee.php` |
| Entity (SubjectCertField) | `hrm-api/Modules/Training/Entities/SubjectCertificateField.php` |
| Service | `hrm-api/Modules/Training/Services/Subject/SubjectService.php` |
| Request | `hrm-api/Modules/Training/Http/Requests/Subject/SubjectBuilderRequest.php` |
| Transformer | `hrm-api/Modules/Training/Transformers/SubjectResource/SubjectDetailResource.php` |
| Routes | `hrm-api/Modules/Training/Routes/api.php` (line 119-138) |
| FE Builder (shell) | `hrm-client/pages/training/subjects/components/SubjectBuilderForm.vue` |
| FE Tab 1 | `hrm-client/pages/training/subjects/components/tabs/TabInfo.vue` |
| FE Tab 2 | `hrm-client/pages/training/subjects/components/tabs/TabEvaluation.vue` |
| FE Tab 3 | `hrm-client/pages/training/subjects/components/tabs/TabLearners.vue` |
| FE Tab 4 | `hrm-client/pages/training/subjects/components/tabs/TabCertificate.vue` |
| FE List | `hrm-client/pages/training/subjects/index.vue` |
| Component Banner | `hrm-client/components/shared/BannerUploader.vue` |
| Component BulletList | `hrm-client/components/shared/BulletListEditor.vue` |
| SCSS | `hrm-client/pages/training/subjects/scss/_index.scss` |

### 9.2. Known Limitations / TODOs

| Item | Mô tả | Priority |
|------|-------|----------|
| BE grader validate | `withValidator` grader-essay tạm comment out — cần confirm schema `exam_questions.type` | Medium |
| jsPDF | Phải `npm i jspdf` trước khi tính năng Download PDF hoạt động | High |
| CORS S3 | Canvas `crossOrigin='anonymous'` có fallback nhưng cần cấu hình CORS trên S3 bucket | Medium |
| `evaluation_config` legacy | Giữ nguyên cột JSON cũ cho backward-compat, dữ liệu mới dùng các bảng `subject_exams` | Low |
