# Test Cases: Quản lý Khoá học (Subject Builder)

| Thông tin | Chi tiết |
|-----------|----------|
| Module | Training — Subjects |
| Phiên bản | 1.0 |
| Ngày tạo | 2026-05-12 |
| Liên quan | [SRS](course-subject-builder.md) |
| Trạng thái | Draft |

---

## Ký hiệu

| Ký hiệu | Nghĩa |
|---------|-------|
| ✅ Pass | Kết quả đúng kỳ vọng |
| ❌ Fail | Kết quả sai |
| — | Chưa test |
| P | Priority: High / Medium / Low |

---

## TC-01: Danh sách khoá học

### TC-01-01: Hiển thị danh sách
| | |
|---|---|
| **Priority** | High |
| **Precondition** | Có ít nhất 3 khoá học trong DB (status: 1, 2, 3) |
| **Steps** | 1. Đăng nhập, vào `/training/subjects` |
| **Expected** | - Bảng hiển thị đúng dữ liệu (mã, tên, loại, trạng thái)<br>- Badge màu đúng: Hoạt động=xanh, Khoá=đỏ, Nháp=xám<br>- Sidebar menu hiển thị "Khoá học" (không phải "Môn học") |
| **Result** | — |

### TC-01-02: Filter theo trạng thái
| | |
|---|---|
| **Priority** | Medium |
| **Steps** | 1. Chọn filter Trạng thái = "Nháp" → 2. Submit |
| **Expected** | Chỉ hiển thị khoá học status=3; các status khác ẩn đi |
| **Result** | — |

### TC-01-03: Filter theo tên/mã
| | |
|---|---|
| **Priority** | Medium |
| **Steps** | 1. Nhập từ khoá vào ô tìm kiếm → 2. Submit |
| **Expected** | Chỉ hiển thị khoá học khớp tên hoặc mã |
| **Result** | — |

### TC-01-04: Nút sửa — chỉ hiện với status Hoạt động và Nháp
| | |
|---|---|
| **Priority** | High |
| **Steps** | Quan sát cột actions với 3 khoá học có status khác nhau |
| **Expected** | - Status=1 (Hoạt động): nút ✏ sửa hiện<br>- Status=3 (Nháp): nút ✏ sửa hiện<br>- Status=2 (Khoá): nút ✏ sửa ẩn hoặc disabled |
| **Result** | — |

---

## TC-02: Tạo mới khoá học — Lưu tạm (DRAFT)

### TC-02-01: Lưu tạm chỉ với tên
| | |
|---|---|
| **Priority** | High |
| **Steps** | 1. Click "+ Tạo mới"<br>2. Chỉ nhập "Tên khoá học test"<br>3. Click "Lưu tạm" |
| **Expected** | - API `POST /store-builder` gọi với `status=3`<br>- Khoá học được tạo với status=Nháp<br>- Mã được auto-gen dạng `SUB-YYYY-XXXX`<br>- Toast thành công<br>- Redirect về danh sách |
| **Result** | — |

### TC-02-02: Lưu tạm khi tên rỗng
| | |
|---|---|
| **Priority** | High |
| **Steps** | 1. Vào tạo mới<br>2. Để trống tên<br>3. Click "Lưu tạm" |
| **Expected** | - FE validate: hiện lỗi inline dưới field tên<br>- Không gọi API<br>- Tab chuyển về Tab 1 (Thông tin) |
| **Result** | — |

### TC-02-03: Lưu tạm với mã trùng
| | |
|---|---|
| **Priority** | Medium |
| **Steps** | 1. Nhập tên + mã đã tồn tại<br>2. Click "Lưu tạm" |
| **Expected** | - API trả về 422<br>- Lỗi inline "Mã khoá học đã tồn tại" hiển thị dưới field mã<br>- Tab chuyển đúng về Tab 1 |
| **Result** | — |

---

## TC-03: Tạo mới khoá học — Lưu đầy đủ (status=1)

### TC-03-01: Lưu đầy đủ — evaluation_mode = completion
| | |
|---|---|
| **Priority** | High |
| **Steps** | 1. Tab 1: nhập tên, chọn loại đào tạo, thêm ≥1 bài học<br>2. Tab 2: chọn "Hoàn thành bài học", rule = "Tất cả bắt buộc"<br>3. Click "Lưu" (status=1) |
| **Expected** | - API gọi thành công<br>- Khoá học được tạo status=1<br>- `evaluation_config.rule = "all_required"` lưu đúng<br>- `evaluation_mode = "completion"`<br>- Không tạo row trong `subject_exams` |
| **Result** | — |

### TC-03-02: Lưu đầy đủ — evaluation_mode = exam
| | |
|---|---|
| **Priority** | High |
| **Steps** | 1. Tab 1: nhập tên, thêm ≥1 bài học<br>2. Tab 2: chọn "Thi đề", chọn 1 đề thi, nhập time_limit=60, pass_score=70, attempt_limit=3, score_rule=highest<br>3. Click "Lưu" |
| **Expected** | - `evaluation_mode = "exam"`<br>- `subject_exams` có 1 row với đúng exam_id, time_limit_min=60, pass_score_percent=70<br>- `exam_attempt_limit=3`, `exam_score_rule="highest"` lưu trên subjects |
| **Result** | — |

### TC-03-03: Validation — exam mode thiếu đề thi
| | |
|---|---|
| **Priority** | High |
| **Steps** | 1. Tab 2: chọn "Thi đề", không chọn đề nào<br>2. Click "Lưu" |
| **Expected** | - Lỗi validation hiển thị: "Phải cấu hình ít nhất một bài thi"<br>- Tab tự chuyển về Tab 2 |
| **Result** | — |

### TC-03-04: Validation — đề thi có tự luận + không có người chấm
| | |
|---|---|
| **Priority** | High |
| **Steps** | 1. Tab 2: chọn đề thi có câu tự luận (essay_count > 0)<br>2. Không chọn người chấm<br>3. Click "Lưu" |
| **Expected** | - FE validate: lỗi "Phải chọn ít nhất 1 người chấm" dưới grader_ids của đề đó<br>- Tab chuyển về Tab 2 |
| **Result** | — |

### TC-03-05: Lưu với ảnh banner
| | |
|---|---|
| **Priority** | Medium |
| **Steps** | 1. Tab 1: click vùng BannerUploader, chọn file ảnh<br>2. Quan sát: local preview xuất hiện ngay, spinner khi đang upload<br>3. Sau upload: ảnh hiển thị URL server<br>4. Click "Lưu" |
| **Expected** | - `banner_url` lưu đúng URL S3<br>- Khi load lại: ảnh vẫn hiển thị |
| **Result** | — |

### TC-03-06: Lưu với chứng chỉ
| | |
|---|---|
| **Priority** | Medium |
| **Steps** | 1. Tab 4: bật chứng chỉ, upload ảnh nền<br>2. Điền cả 4 trường (course_name, employee_name, issued_date, signer)<br>3. Click "Lưu" |
| **Expected** | - `certificate_enabled=1` lưu đúng<br>- `certificate_template_url` có giá trị URL<br>- 4 row trong `subject_certificate_fields` với đúng field_key và tọa độ |
| **Result** | — |

### TC-03-07: Validation — chứng chỉ bật nhưng thiếu ảnh nền
| | |
|---|---|
| **Priority** | Medium |
| **Steps** | 1. Tab 4: bật chứng chỉ, KHÔNG upload ảnh nền<br>2. Click "Lưu" |
| **Expected** | - Lỗi "Chưa chọn ảnh mẫu chứng chỉ"<br>- Tab chuyển về Tab 4 |
| **Result** | — |

---

## TC-04: Cấu hình chương & bài học (Tab 1)

### TC-04-01: Thêm chương và bài học
| | |
|---|---|
| **Priority** | High |
| **Steps** | 1. Toggle "Có chương"<br>2. Click "Thêm chương", nhập tên<br>3. Trong chương, click thêm bài học, chọn bài từ ngân hàng<br>4. Lưu |
| **Expected** | - Chương tạo trong `subject_chapters`<br>- Bài học trong `subject_lessons` với đúng `chapter_id` + `sort_order` |
| **Result** | — |

### TC-04-02: Sửa tên chương (bug fix Phase 16)
| | |
|---|---|
| **Priority** | High |
| **Steps** | 1. Đang có ≥2 chương (chưa lưu DB)<br>2. Click icon sửa chương đầu tiên<br>3. Nhập tên mới<br>4. Lưu modal |
| **Expected** | - Chương đầu tiên được **cập nhật** tên mới (không tạo thêm chương mới)<br>- Chương thứ 2 giữ nguyên |
| **Result** | — |

### TC-04-03: Đổi use_chapters 1→2
| | |
|---|---|
| **Priority** | High |
| **Steps** | 1. Khoá học đang có use_chapters=1 với 2 chương + bài học<br>2. Toggle sang "Không có chương"<br>3. Lưu |
| **Expected** | - `subject_chapters` bị xoá<br>- `subject_lessons.chapter_id = null` cho các bài còn lại |
| **Result** | — |

### TC-04-04: Prerequisite — chọn bài trước
| | |
|---|---|
| **Priority** | Medium |
| **Steps** | 1. Có 2 bài học trở lên<br>2. Bật "Bật điều kiện mở khoá" cho bài thứ 2<br>3. Chọn bài thứ 1 làm prerequisite<br>4. Lưu |
| **Expected** | - `prerequisite_enabled=1` lưu đúng<br>- `prerequisite_subject_lesson_ids` chứa id bài thứ 1 |
| **Result** | — |

### TC-04-05: Xoá bài học đang là prerequisite
| | |
|---|---|
| **Priority** | Medium |
| **Steps** | 1. Bài A là prerequisite của bài B<br>2. Xoá bài A<br>3. Lưu |
| **Expected** | - `prerequisite_subject_lesson_ids` của bài B không còn id bài A |
| **Result** | — |

### TC-04-06: Prerequisite persist sau khi đóng/mở modal
| | |
|---|---|
| **Priority** | Medium |
| **Steps** | 1. Cấu hình prerequisite cho bài học<br>2. Đóng modal → mở lại modal bài học đó |
| **Expected** | - Danh sách prerequisite vẫn hiển thị đúng (không bị reset) |
| **Result** | — |

### TC-04-07: Drag-drop sắp xếp chương
| | |
|---|---|
| **Priority** | Medium |
| **Steps** | 1. Có ≥2 chương<br>2. Kéo thả đổi thứ tự<br>3. Lưu |
| **Expected** | - `sort_order` được cập nhật theo thứ tự kéo thả<br>- Khi load lại: thứ tự vẫn đúng |
| **Result** | — |

---

## TC-05: Cấu hình đánh giá (Tab 2)

### TC-05-01: Chuyển mode exam → completion → xoá subject_exams
| | |
|---|---|
| **Priority** | High |
| **Steps** | 1. Tạo khoá học với eval_mode=exam, 1 đề thi → Lưu<br>2. Vào sửa, chuyển sang eval_mode=completion → Lưu |
| **Expected** | - `subject_exams` của khoá học bị xoá sạch<br>- `subject_exam_graders` cũng bị xoá<br>- `evaluation_mode = "completion"` lưu đúng |
| **Result** | — |

### TC-05-02: exam_participation_required bật
| | |
|---|---|
| **Priority** | Medium |
| **Steps** | 1. Eval mode = exam<br>2. Bật "Yêu cầu hoàn thành bài học trước khi thi"<br>3. Nhập % = 80<br>4. Lưu |
| **Expected** | - `exam_participation_required=1`<br>- `exam_min_required_percent=80` lưu đúng |
| **Result** | — |

### TC-05-03: Validation exam_participation khi bật nhưng không nhập %
| | |
|---|---|
| **Priority** | Medium |
| **Steps** | 1. Eval mode = exam, bật participation<br>2. Không nhập `exam_min_required_percent`<br>3. Click "Lưu" |
| **Expected** | - Lỗi "Chưa nhập % bài học tối thiểu" hiện dưới field |
| **Result** | — |

### TC-05-04: Nhiều đề thi — mỗi đề có cấu hình riêng
| | |
|---|---|
| **Priority** | Medium |
| **Steps** | 1. Chọn 2 đề thi<br>2. Đề 1: time=60, pass=70; Đề 2: time=90, pass=80<br>3. Lưu |
| **Expected** | - `subject_exams` có 2 row với cấu hình riêng biệt |
| **Result** | — |

---

## TC-06: Cấu hình người học (Tab 3)

### TC-06-01: Onboarding — bật và điền ngày
| | |
|---|---|
| **Priority** | Medium |
| **Steps** | 1. Tab 3, bật Onboarding<br>2. `onboarding_new_employee_days = 30`, `onboarding_must_finish_days = 60`<br>3. Lưu |
| **Expected** | - `onboarding_enabled=1`<br>- `onboarding_new_employee_days=30`, `onboarding_must_finish_days=60` lưu đúng |
| **Result** | — |

### TC-06-02: Onboarding bật nhưng không nhập ngày
| | |
|---|---|
| **Priority** | Medium |
| **Steps** | 1. Bật onboarding, không nhập ngày → Lưu |
| **Expected** | - Lỗi validation: "Chưa nhập số ngày được coi là nhân viên mới" |
| **Result** | — |

### TC-06-03: Đối tượng bắt buộc — phòng ban
| | |
|---|---|
| **Priority** | Medium |
| **Steps** | 1. Chọn pill "Phòng ban" ở khối bắt buộc<br>2. Chọn 2 phòng ban<br>3. Lưu |
| **Expected** | - `mandatory_assignee_type = "department"`<br>- `subject_assignees` có 2 row với `assignee_type="department"`, `is_mandatory=1` |
| **Result** | — |

### TC-06-04: Pill selector giữ data khi chuyển type
| | |
|---|---|
| **Priority** | Medium |
| **Steps** | 1. Chọn 2 phòng ban → switch sang "Chức vụ" → chọn 1 chức vụ → switch lại "Phòng ban" |
| **Expected** | - Dữ liệu phòng ban đã chọn vẫn còn |
| **Result** | — |

### TC-06-05: Load lại đúng pill đã chọn khi edit
| | |
|---|---|
| **Priority** | Medium |
| **Steps** | 1. Khoá học đã lưu với mandatory_assignee_type="position"<br>2. Vào sửa, Tab 3 |
| **Expected** | - Pill "Chức vụ" đã được chọn sẵn<br>- Danh sách chức vụ đã chọn hiển thị đúng |
| **Result** | — |

---

## TC-07: Cấu hình chứng chỉ (Tab 4)

### TC-07-01: Canvas preview real-time
| | |
|---|---|
| **Priority** | Medium |
| **Steps** | 1. Upload ảnh nền<br>2. Nhập text cho course_name, signer<br>3. Thay đổi X, Y, font_size |
| **Expected** | - Canvas preview cập nhật real-time theo mỗi thay đổi<br>- Text overlay hiển thị đúng vị trí và kích thước |
| **Result** | — |

### TC-07-02: Download PDF
| | |
|---|---|
| **Priority** | Low |
| **Steps** | 1. Cấu hình cert đầy đủ<br>2. Click "Download PDF" |
| **Expected** | - File PDF được tải về<br>- PDF chứa ảnh nền + text overlay (không phải ảnh trắng) |
| **Result** | — |

### TC-07-03: Tắt chứng chỉ — xoá certificate_fields
| | |
|---|---|
| **Priority** | Medium |
| **Steps** | 1. Khoá học đang có `certificate_enabled=1` + 4 fields<br>2. Vào sửa, tắt chứng chỉ → Lưu |
| **Expected** | - `certificate_enabled=0`<br>- `subject_certificate_fields` bị xoá sạch |
| **Result** | — |

---

## TC-08: Upload ảnh banner

### TC-08-01: Upload và preview ngay
| | |
|---|---|
| **Priority** | High |
| **Steps** | 1. Trong Tab 1, click vùng BannerUploader<br>2. Chọn file ảnh JPEG |
| **Expected** | - Preview ảnh hiển thị ngay (local FileReader, trước khi upload xong)<br>- Spinner loading trong khi upload<br>- Sau upload: ảnh hiển thị URL server |
| **Result** | — |

### TC-08-02: Đổi ảnh
| | |
|---|---|
| **Priority** | Medium |
| **Steps** | 1. Đã có ảnh → hover vào vùng ảnh<br>2. Click "Đổi ảnh" |
| **Expected** | - File picker mở ra<br>- Chọn ảnh mới → ảnh cũ bị thay thế |
| **Result** | — |

### TC-08-03: Xoá ảnh
| | |
|---|---|
| **Priority** | Medium |
| **Steps** | 1. Đang có ảnh → hover → click nút xóa (đỏ) |
| **Expected** | - Ảnh biến mất, quay về trạng thái rỗng<br>- `banner_url = null` khi lưu |
| **Result** | — |

### TC-08-04: Disabled state
| | |
|---|---|
| **Priority** | Low |
| **Steps** | 1. Mở màn xem (isShow=true) |
| **Expected** | - BannerUploader ở trạng thái disabled (opacity 0.6, không click được) |
| **Result** | — |

---

## TC-09: Khoá / Mở khoá

### TC-09-01: Khoá khoá học đang hoạt động
| | |
|---|---|
| **Priority** | Medium |
| **Steps** | 1. Khoá học status=1 → click icon khoá<br>2. Confirm dialog xuất hiện với đúng nội dung<br>3. Click xác nhận |
| **Expected** | - Status chuyển 1→2<br>- Badge đổi sang đỏ "Khoá"<br>- Nút sửa biến mất |
| **Result** | — |

### TC-09-02: Mở khoá
| | |
|---|---|
| **Priority** | Medium |
| **Steps** | 1. Khoá học status=2 → click icon mở khoá → xác nhận |
| **Expected** | - Status chuyển 2→1<br>- Badge đổi sang xanh |
| **Result** | — |

---

## TC-10: Xoá khoá học

### TC-10-01: Xoá DRAFT — luôn được
| | |
|---|---|
| **Priority** | High |
| **Steps** | 1. Khoá học status=3 (DRAFT)<br>2. Click xoá, xác nhận |
| **Expected** | - Khoá học bị xoá<br>- `is_can_delete=true` được trả về từ API |
| **Result** | — |

### TC-10-02: Xoá khoá học có reference downstream
| | |
|---|---|
| **Priority** | High |
| **Steps** | 1. Khoá học status=1 đã được dùng trong 1 course_request<br>2. Quan sát nút xoá |
| **Expected** | - `is_can_delete=false`<br>- Nút xoá bị disable hoặc ẩn |
| **Result** | — |

### TC-10-03: Xoá khoá học không có reference
| | |
|---|---|
| **Priority** | Medium |
| **Steps** | 1. Khoá học status=1 chưa được dùng ở đâu<br>2. Click xoá, xác nhận |
| **Expected** | - `is_can_delete=true`<br>- Khoá học bị xoá thành công |
| **Result** | — |

---

## TC-11: Chỉnh sửa — load lại đúng dữ liệu

### TC-11-01: Load lại subject cũ đã migrate (backfill)
| | |
|---|---|
| **Priority** | High |
| **Steps** | 1. Khoá học cũ (từ trước khi rebuild, data backfill từ evaluation_config JSON)<br>2. Vào sửa |
| **Expected** | - Tab 2 hiển thị đúng evaluation_mode + config<br>- Tab 3 hiển thị đúng assignees (từ backfill working_position/capability) |
| **Result** | — |

### TC-11-02: Load đầy đủ 4 tab
| | |
|---|---|
| **Priority** | High |
| **Steps** | 1. Khoá học đã lưu đầy đủ 4 tab (chapters, exams, assignees, cert)<br>2. Vào sửa |
| **Expected** | - Tab 1: chapters + subject_lessons đúng thứ tự<br>- Tab 2: eval config đúng<br>- Tab 3: onboarding + assignees đúng<br>- Tab 4: cert template + 4 fields đúng |
| **Result** | — |

### TC-11-03: Ghi đè tiêu chí hoàn thành (override_completion)
| | |
|---|---|
| **Priority** | Medium |
| **Steps** | 1. Khoá học đã lưu với 1 bài có `override_completion=2` (ghi đè)<br>2. Vào sửa, load lại |
| **Expected** | - Modal info bài học hiển thị "Đang ghi đè" (màu xanh)<br>- Tiêu chí hiển thị theo override, không phải mặc định |
| **Result** | — |

---

## TC-12: Permission

### TC-12-01: User không có quyền không truy cập được
| | |
|---|---|
| **Priority** | High |
| **Steps** | 1. Đăng nhập với tài khoản không có quyền `Quản lý khoá học`<br>2. Truy cập `/training/subjects` |
| **Expected** | - Bị từ chối truy cập (403 hoặc redirect) |
| **Result** | — |

### TC-12-02: Permission rename không ảnh hưởng user cũ
| | |
|---|---|
| **Priority** | High |
| **Steps** | 1. User đã được phân quyền `Quản lý môn học` (tên cũ) trước khi rename<br>2. Sau khi chạy migration rename permission<br>3. User đăng nhập truy cập `/training/subjects` |
| **Expected** | - User vẫn truy cập được (permission_id không đổi, role_has_permissions giữ nguyên) |
| **Result** | — |

---

## TC-13: BulletListEditor (display info fields)

### TC-13-01: Nhập nội dung dạng bullet
| | |
|---|---|
| **Priority** | Medium |
| **Steps** | 1. Tab 1, section "Khoá học này có gì?"<br>2. Click vào editor, nhập text, format bullet list<br>3. Lưu |
| **Expected** | - `what_includes` lưu dạng HTML `<ul><li>...</li></ul>`<br>- Khi load lại: nội dung render đúng trong editor |
| **Result** | — |

### TC-13-02: 3 editors độc lập nhau
| | |
|---|---|
| **Priority** | Low |
| **Steps** | 1. Nhập nội dung khác nhau vào 3 editor (what_includes, for_who, will_learn) |
| **Expected** | - 3 field lưu độc lập, không ảnh hưởng nhau |
| **Result** | — |

---

## TC-14: Regression — downstream không bị ảnh hưởng

### TC-14-01: Màn training_programs vẫn load đúng
| | |
|---|---|
| **Priority** | High |
| **Steps** | 1. Vào màn Chương trình đào tạo, xem danh sách khoá học trong chương trình |
| **Expected** | - Khoá học hiển thị đúng tên, mã<br>- Không lỗi JS, không lỗi API |
| **Result** | — |

### TC-14-02: Màn courses cũ vẫn load đúng
| | |
|---|---|
| **Priority** | High |
| **Steps** | 1. Vào màn Lớp học (courses), xem chi tiết lớp có khoá học đã migrate |
| **Expected** | - Thông tin khoá học hiển thị đúng<br>- Không lỗi |
| **Result** | — |

---

## Checklist tổng hợp (dùng khi smoke test)

| # | Mục | Status |
|---|-----|--------|
| 1 | Sidebar menu hiển thị "Khoá học" | — |
| 2 | Tạo mới + Lưu tạm với chỉ tên | — |
| 3 | Tạo đầy đủ 4 tab + Lưu | — |
| 4 | Sửa tên chương (không tạo chương mới) | — |
| 5 | Upload ảnh banner → preview + lưu | — |
| 6 | Đổi eval_mode exam → completion → xoá subject_exams | — |
| 7 | Xoá DRAFT thành công | — |
| 8 | Xoá có reference → disabled | — |
| 9 | Khoá/Mở khoá → badge cập nhật | — |
| 10 | Chứng chỉ: upload + canvas preview | — |
| 11 | Permission rename: user cũ vẫn truy cập | — |
| 12 | Downstream (training_programs, courses) không bị ảnh hưởng | — |
