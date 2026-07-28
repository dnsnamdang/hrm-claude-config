# Phân tích: xử lý BÀI HỌC / KHÓA HỌC bị "Khóa" (status) khi đã có người học

> Đây là loại "khóa" do **admin đặt trạng thái** (khác với "khóa" prerequisite/tuần tự đã xử lý ở fix trước).
> - `Subject.status`: `HOAT_DONG=1`, **`KHOA=2`**, `STATUS_DRAFT=3`
> - `Lesson.status` (ngân hàng): `STATUS_ACTIVE=1`, **`STATUS_LOCKED=2`**

## 1. Hiện trạng — nơi nào đã lọc status, nơi nào CHƯA

### Cấp KHÓA HỌC (`subject.status = KHOA`)
| Điểm chạm | Hiện trạng | File |
|---|---|---|
| Catalog / search / home / "Học theo loại/kỹ năng" | ✅ Đã lọc `HOAT_DONG` → khóa bị khóa **ẩn** khỏi danh mục | `PublicBrowseController`, `HomeCategoryService`, `HomeActivityService` |
| Ghi danh mới (enroll) | ✅ Chặn: *"Khoá học chưa được kích hoạt"* (422) | `SubjectDetailController@enroll:249` |
| **Trang chi tiết khóa (show)** | ❌ KHÔNG chặn status → mở được nếu có slug | `SubjectDetailController@show:20-40` |
| **"Tôi đang học" (Góc học tập)** | ❌ Vẫn liệt kê (lọc theo *enrollment* status, không theo subject.status) | `MyLearningService@getInProgress:56` |
| **Màn học (learn / heartbeat / scorm-commit)** | ❌ KHÔNG chặn → học viên đã enroll vẫn học tiếp | `LearningSessionService@getSessionData/processHeartbeat/processScormCommit` |

→ **Lỗ hổng cấp khóa học:** người đã enroll TRƯỚC khi khóa bị khóa vẫn vào học bình thường (đúng như bạn báo).

### Cấp BÀI HỌC (`lesson.status = STATUS_LOCKED`)
| Điểm chạm | Hiện trạng |
|---|---|
| Transformer màn học (`locked`) | ❌ `locked` chỉ tính từ prerequisite/tuần tự (`LessonLockResolver`), **bỏ qua `lesson.status`** |
| `LessonLockResolver` (nguồn chân lý chung) | ❌ Không xét `lesson.status` |
| `isLessonLocked` (chặn ghi tiến độ ở heartbeat) | ❌ Không xét `lesson.status` |
| Danh sách bài ở trang chi tiết | ❌ Không xét |

→ **Lỗ hổng cấp bài học:** `lesson.status` LOCKED **không được kiểm ở bất kỳ đâu** trong luồng học → bài bị khóa vẫn học bình thường.

## 2. Các tình huống "đã có người học" cần quyết định (downstream)

### Khi KHÓA 1 BÀI trong khóa đang có người học
1. **Tiến độ khóa (%)**: `recalculateCourseProgress` đếm **mọi** `subject_lesson` bất kể `lesson.status`. Nếu bài bị khóa là bài *bắt buộc* → học viên **không bao giờ đạt 100%** → kẹt hoàn thành + không ra chứng chỉ. → cần quyết: **loại bài khóa khỏi mẫu số** hay giữ (khóa kẹt tới khi admin mở lại)?
2. **Học tuần tự (linear)**: nếu đánh `locked=true` cho bài khóa → mọi bài SAU nó bị chặn (không hoàn thành được bài khóa để mở tiếp). → nên **bỏ qua** bài khóa trong chuỗi tuần tự.
3. **Prerequisite trỏ tới bài bị khóa**: bài phụ thuộc sẽ **kẹt khóa vĩnh viễn** (điều kiện không bao giờ đạt).
4. **Bài đã học xong rồi bị khóa**: giữ nguyên bản ghi `done` hay ẩn? (đề xuất: giữ progress, chỉ ẩn/khóa hiển thị).

### Khi KHÓA 1 KHÓA HỌC đang có người học
5. **Học viên đang học dở**: chặn hẳn hay cho xem read-only?
6. **Học viên đã hoàn thành + có chứng chỉ**: còn được xem lại / tải chứng chỉ không? (route `certificate` riêng — đề xuất **vẫn cho tải cert**).
7. **Lộ trình chứa khóa bị khóa**: lộ trình **không bao giờ hoàn thành** (`syncLearningPathCompletion` cần mọi khóa done). LP detail có ẩn khóa con bị khóa không?

## 3. Đề xuất phương án (chờ bạn chốt)

### A. BÀI HỌC bị khóa → xử lý như "ẩn khỏi khóa" (KHÔNG khóa tại chỗ)
Lý do: khóa tại chỗ làm kẹt tiến độ/tuần tự/prerequisite cho tất cả mọi người. Coi bài khóa như "tạm gỡ khỏi khóa học":
- **Transformer**: bỏ qua bài có `lesson.status = LOCKED` khi build danh sách (không trả về FE).
- **`recalculateCourseProgress`**: loại `lesson.status = LOCKED` khỏi mẫu số → khóa vẫn hoàn thành được với các bài còn active.
- **`LessonLockResolver` / linear / prerequisite**: bỏ qua bài khóa.
- **Giữ nguyên** bản ghi `enrollment_lesson_progress` cũ (không xóa) → mở lại là có ngay.
- **Live (đang xem đúng bài bị khóa)**: `processHeartbeat` trả **422** (như "đã gỡ") → **tái dùng nguyên luồng fix trước**: toast + tự chuyển sang bài hợp lệ. Reload: bài không có trong list → cũng rơi vào nhánh "đã xóa" đã làm.
- Ưu điểm: **gần như không phải thêm code FE mới**, tận dụng fix vừa xong.

> Nếu bạn muốn ĐÚNG NGHĨA "khóa" (bài vẫn hiện + overlay "Bài đã bị khóa", chặn học) thay vì ẩn → cần thêm cờ khóa riêng ở transformer + sửa mẫu số/tuần tự để bài khóa không chặn bài khác. Nói mình biết nếu chọn hướng này.

### B. KHÓA HỌC bị khóa → chặn toàn màn học + thông báo
- **`getSessionData` / `processHeartbeat` / `processScormCommit`**: nếu `subject.status = KHOA` → trả lỗi code riêng (đề xuất **423** + message *"Khóa học đã bị khóa"*).
- **FE**: 
  - `fetchCourseData` bắt lỗi này → set cờ `courseLocked` → hiện màn chặn *"Khóa học đã bị khóa"* + nút Về trang chủ (thay vì "Không tìm thấy khoá học" chung chung).
  - Live (đang xem): heartbeat trả 423 course-level → hiện overlay/chuyển về trang chủ.
- **Chi tiết khóa (show)**: thêm chặn tương tự (hiện "Khóa học đã bị khóa", ẩn nút Tiếp tục học).
- **"Tôi đang học"**: ẩn khóa bị khóa khỏi `getInProgress` (hoặc gắn nhãn "Đã khóa" + không cho vào học). → cần chốt: **ẩn hẳn** hay **hiện nhãn khóa**?
- **Chứng chỉ**: giữ cho tải (không chặn route certificate).

## 4. Phạm vi sửa dự kiến (sau khi chốt phương án)
- BE: `LearningSessionService` (getSessionData, processHeartbeat, processScormCommit, recalculateCourseProgress), `LearningSessionResource`, `LessonLockResolver`, `SubjectDetailController@show`, `MyLearningService@getInProgress`.
- FE: `learningSession` store (cờ courseLocked), `SubjectLearnView` (màn chặn + live 423 course), tận dụng handler bài-không-khả-dụng đã có.

## Quyết định đã chốt (2026-07-20) + trạng thái triển khai
1. **Bài học khóa → ẩn khỏi khóa** (tái dùng luồng "bài đã xóa"). ✅ Đã làm.
2. **Khóa học khóa → chặn khi RELOAD/vào lại** (getSessionData trả 423, KHÔNG đụng heartbeat live). ✅ Đã làm.
3. **"Tôi đang học" → hiện nhãn "Đã khóa"** + chặn nút Tiếp tục. ✅ Đã làm.
4. **Tiến độ %: loại bài khóa khỏi mẫu số.** ✅ Đã làm.

### Đã sửa
- BE: `LearningSessionResource` (ẩn bài LOCKED), `LearningSessionService` (recalculateCourseProgress loại LOCKED; getSessionData 423 cho subject KHOA; heartbeat/scormCommit trả 422 cho bài LOCKED; isLessonLocked load `.lesson`), `LessonLockResolver` (bỏ bài LOCKED khỏi linear/prereq), `MyLearningService` (cờ `locked` + nhãn "Đã khóa").
- FE: `learningSession` store (cờ `courseLocked` từ 423), `SubjectLearnView` (màn chặn "Khóa học đã bị khóa"), `StudyCard` + `MyLearningView` (badge "Đã khóa" + chặn Tiếp tục).

### Verify
- BE `php -l` sạch 4 file; FE `vite build` (Node 24) sạch.
- Playwright: (a) mock GET /learn → 423 → FE hiện màn "Khóa học đã bị khóa" ✅; (b) bật cờ locked trên khóa in_progress → thẻ hiện badge "Đã khóa" + nút Tiếp tục bị khóa ✅ (có screenshot).
- CHƯA E2E được nhánh BE cần dữ liệu thật (subject.status=2 / lesson.status=2) vì không được đổi DB — verify bằng lint + review + mock. Đề nghị user tự khóa 1 khóa/bài test để xác nhận end-to-end thật.
