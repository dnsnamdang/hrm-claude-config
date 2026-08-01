# Khảo sát — GIAO VIỆC: TASK & ISSUE

## 1. Lối vào & phân biệt
| Lối vào | URL | Nhãn menu |
|---|---|---|
| Danh sách Task | `/assign/tasks` | **Giao việc & Bàn giao › Task** |
| Danh sách Issue | `/assign/issues` | **Giao việc & Bàn giao › Issue** |
| Nhập tiến độ hằng ngày | `/assign/tasks/daily-report` | **Cập nhật tiến độ Task** |
| Công việc của tôi | `/assign/my-job?tab=tasks` \| `?tab=issues` | **Công việc của tôi** |
| Tab trong chi tiết dự án | `/assign/prospective-projects/{id}/manager` | tab **Task** / **Issue** |
| Tab trong chi tiết hạng mục | `/assign/solution-modules/{id}/manager` | tab **Task** |

Tab trong dự án dùng lại component của giải pháp (`solutions/components/manager/TasksTab.vue`, `IssueTab.vue`); chỉ render khi dự án đã có giải pháp, ngược lại báo **"Dự án chưa có giải pháp tương ứng"**.

### Phân biệt nghiệp vụ
| | TASK (công việc) | ISSUE (vấn đề) |
|---|---|---|
| Bản chất | Việc **giao chủ động**, có kế hoạch, có số giờ định mức | Sự cố/vướng mắc **phát sinh ngoài kế hoạch** |
| Mã tự sinh | `{MÃ_CTY}.TASK.NB.{yy}.{0001}` | `ISS-{YYYY}{MM}-{0001}` |
| Trạng thái | 10 trạng thái, kiểu **số** (1–10) | 8 trạng thái, kiểu **chuỗi** (`new`, `assigned`…) |
| Vai trò | Người tạo, Người thực hiện, Người duyệt KQ, Người theo dõi | Người tạo, Người xử lý, Người duyệt đóng, Người theo dõi, **Người phối hợp**, **Người phát hiện** |
| Đặc thù | Task con, checklist, lặp lại (recurring), yêu cầu báo cáo tiến độ, số giờ/hiệu suất, liên kết FS/SS/FF/SF | Nguồn phát hiện, nhóm nguyên nhân, mức ảnh hưởng (tiến độ/chất lượng/khách hàng), SLA, điều kiện đóng |
| Phân cấp | Có cha–con (`parent_id`) | Không |

## 2. Màn danh sách

### 2.1 Task — tiêu đề **"Danh sách task"**, rỗng → **"Không có dữ liệu phù hợp bộ lọc."**
**Cột:** STT | **Mã-Tên task** | **Mã-Tên giải pháp** | **Version GP** | **Dự án** | **Hạng mục/Module** | **Trạng thái** | **Ưu tiên** | **Người làm** | **Người theo dõi** | **Người duyệt** | **Người tạo** | **Bắt đầu** | **Hạn hoàn thành** | **Checklist/Task con**.
Cột *Mã-Tên task* kèm dòng phụ `Cập nhật: … / Bởi: …`, badge **Trong hạn** (xanh) / **Quá hạn** (đỏ) — ẩn khi status ∈ {1, 8, 9} — và chip tag tối đa 4. Ba cột đầu tự động ghim.

**Bộ lọc** — panel **"Bộ lọc danh sách task"**, mặc định thu gọn:
| Tiêu chí | Control | Nguồn |
|---|---|---|
| Ô tìm nhanh — **"Tìm theo Mã/Tên task, Dự án"** | input | – |
| Công ty / Phòng ban / Bộ phận | V2BaseCompanyDepartmentFilter | lọc theo quyền |
| **Giải pháp** | select | `assign/solutions/getAll` |
| **Dự án** | select | rỗng nếu chưa chọn Giải pháp |
| **Hạng mục/Module** | select | modules của giải pháp |
| **Version giải pháp** | select | `assign/solutions/{id}/versions` |
| **Người thực hiện** / **Người tạo** / **Người duyệt kết quả** | select allowClear | `allEmployeesOptions` |
| **Trạng thái** | select | 10 mục |
| **Mức độ ưu tiên** | select | Bình thường / Cao / Khẩn cấp |
| **Ngày cập nhật từ** / **đến** | datepicker | – |
| **Hạn hoàn thành từ** / **đến** | datepicker | – |
| **Tag** | MultiSearchPicker — "Chọn tag để lọc (gõ để tìm kiếm)…" | `assign/tasks/tags/getAll` |

Auto-search: `ignoredFields = ['keyword','quick_scope']` → chọn filter là tìm luôn, từ khóa phải bấm **Tìm kiếm**. Lưu localStorage `assign_tasks`, 10 phút.

**Lọc nhanh** (4 nút icon): **Task tôi làm** / **Task tôi giao** / **Task tôi theo dõi** / **Task tôi duyệt kết quả**. Kèm 2 pill **Tổng: {n}** và **Quá hạn: {n}**.

**Thanh công cụ** — **không nút nào bị chặn bởi `hasPermission`**: **Tạo mới** | **Xuất Excel** | icon **Cấu hình cột hiển thị**. Không có Import Excel.

**Thao tác trên dòng:**
| Nút | Điều kiện | Mở ra |
|---|---|---|
| **Xem** | luôn | Modal theo trạng thái |
| **Sửa** | `can_edit` | `CreateTaskModal.edit()` |
| **Nhập kết quả** | `can_import_result` | `ImportResultModal` |
| **Duyệt** | `can_approve` | `ImportResultModal` |
| **Lịch sử chỉnh sửa** | luôn | `TaskHistoryModal` |
| **Xoá** | `can_delete` | Confirm xóa |

**Quy tắc chọn modal:** trạng thái 1, 2, 3, 10 → `CreateTaskModal`; trạng thái 4–9 → `ImportResultModal`.
Confirm xóa: **"Xác nhận xóa"**, **`Bạn có chắc muốn xóa công việc '{tên}'?`**, nút **Hủy** / **Xóa**. Toast **"Xóa công việc thành công"** / **"Lỗi khi xóa công việc"**.
Phân trang mặc định 10 dòng (5/10/20/50). Sắp xếp mặc định `created_at desc`.

### 2.2 Issue — tiêu đề **"Danh sách Issue"**, rỗng → **"Không có issue nào được tìm thấy."**
**Cột:** STT | **Mã-Tên issue** | **Mã-Tên giải pháp** | **Dự án** | **Hạng mục/Module** | **Loại issue** | **Người xử lý** | **Hạn xử lý** | **Ưu tiên** | **Trạng thái** | **Người theo dõi** | **Người phối hợp** | **Người duyệt** | **Người tạo** | **Nguồn phát hiện** | **Người phát hiện** | **Ngày phát hiện**.

**Bộ lọc** — panel **"Bộ lọc Issue"**: ô tìm nhanh **"Tìm theo Mã/Tiêu đề Issue..."**, Công ty/Phòng ban/Bộ phận, **Giải pháp**, **Dự án**, **Hạng mục/Module**, **Version giải pháp**, **Người thực hiện**, **Người tạo**, **Người duyệt**, **Trạng thái** (8 mục), **Mức độ ưu tiên** (4 mục), **Ngày tạo từ/đến**. Auto-search `ignoredFields = ['keyword']`. Không có lọc theo Tag.

**Lọc nhanh**: **Tôi phụ trách xử lý** / **Tôi phát hiện** / **Tôi theo dõi** / **Tôi duyệt đóng**.
**Thanh công cụ**: **Tạo Issue** | **Xuất Excel** | icon **Tùy chỉnh cột**.
**Thao tác dòng**: **Xem** (luôn) | **Sửa** (`can_edit`) | **Lịch sử** (luôn) | **Xoá** (`can_delete`) | **Xử lý** (`can_handle`, cuối).
Confirm xóa: **"Xác nhận xóa Issue"**, **`Bạn có chắc muốn xóa Issue '{tên}'? Hành động này không thể hoàn tác.`**
Phân trang mặc định **20** dòng (khác Task).

Cả hai màn **không có chọn nhiều dòng, không xóa hàng loạt, không import Excel**.

## 3. TẠO MỚI TASK
**Popup** `CreateTaskModal.vue`, tiêu đề **"Thêm mới Task"**, khổ `xl` toàn màn hình.
2 chế độ, nút góc trên phải: **Chế độ nâng cao** / **Chuyển về đơn giản**; badge **Đơn giản** hoặc **Nâng cao**. Mặc định `mode = 1` (Đơn giản) — chỉ có cột trái phần thông tin cơ bản; **Nâng cao** mở thêm Checklist, Task con, Tệp đính kèm, Bình luận và toàn bộ cột phải.

### 3.1 Trường bắt buộc (luôn hiện)
| Nhãn | Control | Bắt buộc | Mặc định | Ẩn/hiện/khóa | Options |
|---|---|---|---|---|---|
| **Tên công việc** * | V2BaseInput, `VD: Thiết kế popup tạo Task` | ✅ BE `required\|max:255` | rỗng | – | – |
| **Giải pháp** * | SearchPicker `Tìm giải pháp theo mã / tên...` | ✅ | rỗng | **Khóa** nếu mở từ dự án/hạng mục | `assign/solutions/getAll`, chỉ GP ở 6 trạng thái cho phép |
| **Dự án/Nhóm** * | SearchPicker | ✅ | **tự điền** theo giải pháp | **Luôn readonly** | suy từ giải pháp |
| **Hạng mục/Module** | SearchPicker | ✅ **chỉ khi** giải pháp `has_modules` | rỗng | Khóa nếu chưa chọn GP / GP không có hạng mục / mở từ hạng mục | hạng mục Đã duyệt hoặc Chờ duyệt hồ sơ |
| **Người thực hiện** * | SearchPicker `Tìm và chọn người thực hiện...` | ✅ `required\|exists:employees` | rỗng | – | `assign/tasks/employees` — **toàn bộ NV đang hoạt động của công ty**, KHÔNG lọc theo giải pháp |
| **Trạng thái** | SearchPicker `Tìm trạng thái...` | BE `required` (FE không đánh *) | **1 – Nháp** | – | Khi tạo mới chỉ 4: **Nháp / Chờ phê duyệt triển khai / Chờ bắt đầu / Đang thực hiện** |
| **Mức độ ưu tiên** | SearchPicker `Chọn mức độ ưu tiên...` | BE `required` | **null** | – | Bình thường / Cao / Khẩn cấp |
| **Hạn hoàn thành** * | V2BaseDatePicker DD/MM/YYYY | BE `nullable` nhưng FE gắn * | **hôm nay** | – | – |
| **Giờ hạn** * | V2BaseDatePicker time HH:mm | BE `nullable`, FE gắn * | **17:00** | – | – |
| **Mô tả** | V2BaseTextarea 3 dòng | ❌ | rỗng | – | – |
| **Số giờ được giao** * | number, step 0.5, `VD: 8.0` | ✅ `required\|numeric\|min:0` | null | – | – |

> Trường **Ngày bắt đầu** đã bị comment out khỏi giao diện — hệ thống tự set = hôm nay ở hậu trường.

### 3.2 Chế độ Nâng cao
**Cột trái:**
| Khối | Nội dung |
|---|---|
| **Checklist** | Ô "Nhập mục checklist và Enter" + nút thêm; nút **Thêm nhanh** mở hộp thoại **"Nhập số lượng"** (1–50, mặc định 3). Mỗi dòng: checkbox + nội dung + nút xóa. Hiển thị `{x}/{y} hoàn thành` |
| **Task con** | Bảng: **Tên task con** (bắt buộc), **Người làm** (bắt buộc), **Hạn (ngày)**, **Giờ hạn**. Hạn/giờ hạn **tự đồng bộ theo task cha**. Có nút **Thêm nhanh** |
| **Tệp đính kèm** | Nút **Thêm tài liệu**; STT, **Tên tài liệu** (bắt buộc), **Loại tài liệu** (bắt buộc, `assign/attachment-types/getAll`), **Upload / File** (**Chọn tệp**), **Dung lượng**, nút xóa. jpg, jpeg, png, doc, docx, xls, xlsx, pdf, ppt, pptx; tối đa 20MB |
| **Bình luận** | Chỉ khi sửa/xem, không có khi tạo mới |

**Cột phải — tab "Thiết lập":**
| Nhãn | Control | Mặc định |
|---|---|---|
| **Người duyệt kết quả** | SearchPicker `Tìm người duyệt...` | **= người đang đăng nhập** |
| **Người theo dõi** | MultiSearchPicker | **= người đang đăng nhập**; thêm **Người thực hiện** tự động khi chọn |
| **Thẻ (Tags)** | Input "Nhập thẻ và Enter" + nút **Xóa** | rỗng |
| **Lặp lại** | Checkbox; bật ra: **Kiểu lặp** (Hàng ngày/tuần/tháng/Tùy chỉnh), **Khoảng lặp**, **Chọn thứ** (T2…CN), **Ngày trong tháng**, **Biểu thức Cron**, **Kết thúc** (Không bao giờ / Đến ngày / Sau {n} lần) + **Xem trước** | tắt; Hàng ngày, khoảng 1, Không bao giờ, max 10 lần |
| **Yêu cầu báo cáo tiến độ?** | Checkbox; bật ra: **Theo chu kỳ** (Hàng ngày/tuần/tháng), **Giờ gửi**, **Chọn thứ báo cáo**, **Ngày trong tháng** + **Xem trước** | tắt; Hàng ngày, giờ gửi **17:00:00** |

**Cột phải — tab "Liên kết & KPI"**: **Liên kết task** — chọn kiểu FS/SS/FF/SF/RL + ô tìm task, kèm dòng gợi ý (VD: *"FS — Task B chỉ bắt đầu khi Task A kết thúc."*).

### 3.3 Cascading và prefill
- Chọn **Giải pháp** → **tự điền Dự án**, **reset Hạng mục**, **reset Người duyệt kết quả** nếu người đó không thuộc nhân sự giải pháp mới.
- Chọn Giải pháp/Hạng mục **KHÔNG** lọc lại Người thực hiện — vẫn là toàn bộ nhân viên công ty.
- **Người duyệt kết quả** CÓ lọc: chỉ PM giải pháp + nhân sự giải pháp + leader/nhân sự các hạng mục.
- Tạo từ tab Task của **dự án/giải pháp**: prefill `solution_id`, `project_id` và **khóa** 2 trường.
- Tạo từ tab Task của **hạng mục**: prefill thêm `solution_module_id`, khóa cả 3.

### 3.4 Lưu
Nút footer: **Lưu**, **Lưu & Tiếp tục** (chỉ khi tạo mới), **Đóng**; góc trên **Xóa trắng** (confirm **"Bạn có chắc muốn xóa trắng toàn bộ nội dung đã nhập?"**).
- `POST assign/tasks`. Toast **"Đã lưu task thành công"**; lỗi **"Lỗi khi lưu task"**; 422 đổ vào từng ô.
- **Lưu & Tiếp tục**: giữ giải pháp/hạng mục/dự án đã khóa, xóa các trường còn lại; **Lưu** thường thì đóng modal và tải lại danh sách.

BE tự sinh khi lưu: mã task, `created_by`, phiên bản giải pháp/hạng mục; ghi lịch sử `create`; trạng thái khác Nháp thì gửi thông báo; trạng thái khác Nháp/Chờ phê duyệt thì "task con" được tạo thành task thật.

**Message lỗi BE:**
| Trường | Message |
|---|---|
| Hạn hoàn thành | **"Không được là ngày trong quá khứ."** |
| Giờ hạn | **"Phải lớn hơn hoặc bằng thời điểm hiện tại."** |
| Hạn của task con | **"Hạn hoàn thành của task con không được sau hạn hoàn thành của task cha"** |
Các trường `required` còn lại dùng message mặc định Laravel.

## 4. CHỈNH SỬA TASK
**Mở**: nút **Sửa** trên dòng (chỉ khi `can_edit`) → tiêu đề **"Chỉnh sửa Task"**. Task ở trạng thái 4–9 mà bấm **Xem**/**Nhập kết quả**/**Duyệt** thì mở `ImportResultModal`.

| Khía cạnh | Tạo mới | Chỉnh sửa |
|---|---|---|
| Trạng thái chọn được | 4 mục cố định | **Chỉ các bước chuyển hợp lệ** — `allowed_next_statuses` do BE trả theo vai trò |
| Người duyệt / theo dõi | tự điền = người đăng nhập | giữ nguyên dữ liệu cũ |
| Nút **Lưu & Tiếp tục** | có | **không có** |
| Nút **Xóa trắng** | có | chỉ khi **chính mình là người tạo** |
| Task con | nhập bảng tay | nếu đã có task con thật thì bảng **chỉ đọc**, bấm vào mở task con |
| Bình luận | không | có (chế độ Nâng cao) |
| API | `POST assign/tasks` | `PUT assign/tasks/{id}` |
| Toast | "Đã lưu task thành công" | **"Đã cập nhật task thành công"** |

**Trường bị khóa khi sửa**: `can_edit = false` → **toàn bộ trường thông tin bị khóa**, chỉ đổi được **Trạng thái**. Trường **Dự án/Nhóm** luôn readonly.
**Điều kiện được sửa**: `can_edit = true` khi **task không có task con** VÀ **người đăng nhập là người tạo**. Nút Lưu vẫn hiện nếu có `can_edit` **hoặc** `can_import_result` **hoặc** `can_approve`.

## 5. TẠO MỚI & CHỈNH SỬA ISSUE
**Popup** `CreateIssueModal.vue`. Tiêu đề: **"Thêm mới Issue"** / **"Chỉnh sửa Issue"** / **"Chi tiết Issue"**. Không có chế độ đơn giản/nâng cao — luôn đủ 2 cột.

### 5.1 Cột trái — "Thông tin Issue"
| Nhãn | Control | Bắt buộc | Mặc định | Options |
|---|---|---|---|---|
| **Tiêu đề Issue** * | Input, `VD: Popup tạo task bị mất dữ liệu khi chuyển tab` | ✅ | rỗng | – |
| **Giải pháp** * | SearchPicker | ✅ | rỗng (khóa nếu mở từ dự án/hạng mục) | GP ở 6 trạng thái cho phép |
| **Dự án/Nhóm** * | SearchPicker | ✅ | **tự điền theo giải pháp**; khóa khi mở từ dự án | – |
| **Hạng mục / Module** | SearchPicker | ✅ **chỉ khi** GP có hạng mục | rỗng | hạng mục Đã duyệt / Chờ duyệt hồ sơ |
| **Loại Issue** * | SearchPicker | ✅ | **"Lỗi phần mềm"** (`bug`) | 9 mục: Lỗi phần mềm, Vướng nghiệp vụ, Yêu cầu thay đổi, Thiếu dữ liệu, Rủi ro, Hạ tầng / tích hợp, Thiếu thông tin đầu vào, Yêu cầu thay đổi từ phía khách hàng, Khác |
| **Nhóm nguyên nhân** | SearchPicker | ❌ | rỗng | Thiếu validate, Sai đặc tả, Thiếu dữ liệu, Lỗi tích hợp, Lỗi logic, Danh mục sản phẩm, Bản vẽ sản phẩm, Thông số kỹ thuật sản phẩm, Thay đổi về công nghệ |
| **Mức độ ưu tiên** * | SearchPicker | ✅ | **"Trung bình"** (`medium`) | Thấp / Trung bình / Cao / Khẩn cấp |
| **Mức độ ảnh hưởng** * | SearchPicker | ✅ | **"Cá nhân"** (`personal`) | Cá nhân, Nhóm nhỏ, Toàn module, Toàn dự án, Khách hàng, Ít, Nhiều, Trung bình |
| **Mô tả Issue** * | Textarea 5 dòng | ✅ | rỗng | – |

### 5.2 "Ghi nhận phát sinh"
| Nhãn | Control | Bắt buộc | Mặc định |
|---|---|---|---|
| **Nguồn phát hiện** * | SearchPicker | ✅ | **"Tự phát hiện"** (`self`) — options: Tự phát hiện, PM phát hiện, Leader phát hiện, Tester phát hiện, Khách hàng phản ánh, Từ meeting, Nhân viên phát hiện |
| **Người phát hiện** | SearchPicker | ❌ | rỗng |
| **Ngày giờ phát hiện** | DatePicker datetime | ❌ | **thời điểm hiện tại** |
| **Task chính liên kết** | SearchPicker | ❌ | rỗng — `assign/tasks/getAll` |
| **Hạn xử lý** | DatePicker | ❌ | rỗng |
| **Giờ hạn** | input time | ❌ | **17:00** |
| **Người duyệt đóng** | SearchPicker | ❌ | rỗng |

### 5.3 "Đánh giá ảnh hưởng"
**Ảnh hưởng tiến độ** / **chất lượng** / **khách hàng** — không bắt buộc, mặc định **"Không đáng kể"** (`no`); options: Không đáng kể / Ảnh hưởng nhẹ / Ảnh hưởng lớn. Kèm **Ghi chú ảnh hưởng** (textarea).

### 5.4 "Tệp đính kèm / chứng cứ"
Nút **Thêm tài liệu**; cột STT | **Tên tài liệu** | **Loại tài liệu** | **Upload / File** (**Chọn tệp**) | **Dung lượng** | nút xóa. Rỗng → **"Chưa có tệp đính kèm"**. Lỗi: **"Định dạng không hợp lệ. Chỉ chấp nhận: …"**, **"File quá lớn. Không được tải lên file lớn hơn 20MB."**

### 5.5 Cột phải
**Thông tin xử lý:**
| Nhãn | Control | Bắt buộc | Mặc định |
|---|---|---|---|
| **Trạng thái issue** | SearchPicker | ✅ (validate FE) | **"Mới ghi nhận"** (`new`). Khi tạo mới chỉ 2: **Mới ghi nhận** / **Đã phân công** |
| **Lý do từ chối** * | Textarea | ✅ chỉ khi trạng thái = Từ chối và đang ở chế độ Xử lý | rỗng |
| **Người phụ trách xử lý** | SearchPicker | **Bắt buộc khi trạng thái = "Đã phân công"** | rỗng |
| **Người theo dõi** | MultiSearchPicker | ❌ | rỗng |
| **Người phối hợp** | MultiSearchPicker | ❌ | rỗng |
| **SLA xử lý** | SearchPicker | ❌ | **"1 ngày"** (`1d`) — options: 4 giờ / 8 giờ / 1 ngày / 2 ngày / Theo deadline riêng |

**Liên kết & phân loại**: **Tags**. **Kế hoạch xử lý**: **Kế hoạch xử lý** (textarea) và **Điều kiện đóng issue** (textarea).
Khác Task: Issue **KHÔNG tự điền người duyệt/người theo dõi = người đăng nhập**.

### 5.6 Lưu
Footer: **Lưu thông tin** và **Đóng**; góc trên **Làm mới** (xóa trắng form).
`POST assign/issues` / `PUT assign/issues/{id}`. Toast **"Lưu Issue thành công"**; lỗi trường: **"Vui lòng kiểm tra lại thông tin."** + inline.

**Message validate FE nguyên văn:**
| Trường | Message |
|---|---|
| Tiêu đề Issue | **"Tiêu đề không được để trống"** |
| Giải pháp | **"Giải pháp không được để trống"** |
| Dự án | **"Dự án không được để trống"** |
| Hạng mục/Module | **"Module không được để trống"** |
| Loại Issue | **"Loại Issue không được để trống"** |
| Mức độ ưu tiên | **"Mức độ ưu tiên không được để trống"** |
| Mức độ ảnh hưởng | **"Mức độ ảnh hưởng không được để trống"** |
| Mô tả | **"Mô tả không được để trống"** |
| Nguồn phát hiện | **"Nguồn phát hiện không được để trống"** |
| Trạng thái | **"Trạng thái không được để trống"** |
| Người phụ trách xử lý | **"Người phụ trách xử lý không được để trống khi trạng thái là "Đã phân công""** |
| Lý do từ chối | **"Vui lòng nhập lý do từ chối"** |

### 5.7 Chỉnh sửa Issue
**Ba chế độ mở:**
| Nút | Hành vi |
|---|---|
| **Sửa** | Sửa toàn bộ trường (khi `can_edit`) |
| **Xem** | Chỉ đọc hoàn toàn, không có nút Lưu |
| **Xử lý** | **Chỉ đọc phần thông tin**, nhưng **mở khóa** Trạng thái, Lý do từ chối và tệp đính kèm — dành cho người xử lý (`can_handle`) |

**Trạng thái** khi sửa chỉ hiện các bước chuyển hợp lệ. Có thêm khối **Bình luận trao đổi**. Hiện box cảnh báo **"Lý do từ chối: …"** khi trạng thái Từ chối, box **"Hoàn thành lúc: …"** khi đã Hoàn thành.

**Điều kiện được sửa/xóa (BE):**
| Cờ | Điều kiện |
|---|---|
| `can_edit` | trạng thái **không phải** Đã đóng/Hoàn thành **VÀ** là người tạo |
| `can_delete` | là người tạo **VÀ** trạng thái = **Mới ghi nhận** |
| `can_handle` | là người xử lý & trạng thái ∈ {Đã phân công, Đang xử lý, Từ chối, Mở lại}; **hoặc** là người duyệt & trạng thái = Đã xử lý xong; **hoặc** là người tạo/người xử lý & trạng thái = Hoàn thành (để mở lại) |

Nếu chỉ có `can_handle` mà không có `can_edit`, BE **chỉ chấp nhận cập nhật `status` và `assignee_id`**. Lỗi: **"Bạn không có quyền chỉnh sửa Issue này hoặc Issue đã đóng."**; xóa: **"Bạn không có quyền xóa Issue này hoặc Issue không còn ở trạng thái Mới."**

## 6. Thao tác liên quan

### 6.1 Nhập kết quả Task — `ImportResultModal.vue`
Mở từ **Nhập kết quả** / **Duyệt** / **Xem** (khi trạng thái 4–9). Tiêu đề **"Nhập kết quả Task"** / **"Xem kết quả Task"**.
Phần trên: thông tin task **chỉ đọc** (Tên công việc, Mức độ ưu tiên, Dự án/Nhóm, Hạng mục/Module, Người thực hiện, Hạn hoàn thành, Giờ hạn, Mô tả).

**Chế độ A — task KHÔNG yêu cầu báo cáo tiến độ:**
| Nhãn | Control | Bắt buộc | Ghi chú |
|---|---|---|---|
| **Trạng thái** | SearchPicker `Chọn trạng thái...` | – | các bước chuyển hợp lệ; chọn *Hoàn thành - Chờ duyệt* hoặc *Hoàn thành* → **tự set Tiến độ = 100%** |
| **Số giờ được giao** | input | – | chỉ đọc |
| **Số giờ làm thực tế** * | number step 0.5 | ✅ | – |
| **Tiến độ (%)** * | number 0–100 | ✅ | khóa khi trạng thái là hoàn thành |
| **Hiệu suất** | input | – | chỉ đọc, = giờ giao / giờ thực tế × 100 |
| **Kết quả thực hiện** * | Textarea | ✅ | – |

**Chế độ B — task CÓ yêu cầu báo cáo tiến độ**: bảng **nhật ký** sinh sẵn theo chu kỳ: **Ngày báo cáo** (chỉ đọc) | **Số giờ làm** | **Tiến độ (%)** | **Ghi chú**. Chỉ nhập được dòng đã tới ngày; dòng tương lai hiện **"Chưa đến ngày báo cáo"**. Kèm **Tiến độ hoàn thành (%)** (chỉ đọc) và **Kết quả thực hiện (tổng hợp)**.

Ngoài ra: **Checklist** (tick + ghi chú kết quả), **Task con** (chỉ đọc), 2 tab tệp — **File đính kèm giao task** (chỉ đọc, tải xuống) và **File kết quả thực hiện** (nút **Thêm dòng**, upload), **Bình luận**.

Lưu: `PUT assign/tasks/{id}` với `is_import_result: true`. Toast **"Đã lưu kết quả thành công"** / **"Lỗi khi lưu kết quả"**. Lỗi BE: **"Tiến độ hoàn thành phải đạt 100% mới được chuyển sang trạng thái hoàn thành."** và **"Tiến độ không được nhỏ hơn kỳ trước ({n}%)"**.

### 6.2 Cập nhật tiến độ hằng ngày — `/assign/tasks/daily-report`
Tiêu đề **"Nhập kết quả báo cáo tiến độ"**. Chỉ liệt kê task **mình là người thực hiện**, đang **Đang thực hiện**, có bật báo cáo tiến độ và **đến hạn báo cáo hôm nay**.
3 thẻ tổng hợp: **Tổng task** / **Chờ báo cáo** / **Đã hoàn thành**. Mỗi task là khối gập, bảng: **NGÀY BÁO CÁO** | **SỐ GIỜ LÀM** (0–24) | **TIẾN ĐỘ (%)** (0–100) | **GHI CHÚ**. Chân trang cố định: *Tổng giờ hôm nay: {x}h / 8h*, *Tiến độ trung bình*, cảnh báo *{n} task chưa nhập báo cáo*; nút **Lưu tất cả** và **Đóng**.
Toast: **"Lưu tiến độ thành công"**; vượt trần: **"Có task vượt 100% tiến độ, vui lòng kiểm tra lại"**; rỗng: **"Không có dữ liệu để lưu"**.

### 6.3 Bình luận
Component chung `CommentThread.vue` cho cả Task và Issue. Trả lời lồng tối đa 3 cấp, đính kèm tệp (≤50MB), thả cảm xúc, nhắc tên (@). Task còn có chấm điểm 1–5 và **duyệt** bình luận.
Toast BE: **"Thêm comment thành công"**, **"Cập nhật comment thành công"**, **"Xoá comment thành công"**; sửa/xóa comment người khác → **"Bạn không có quyền sửa comment này"** / **"Bạn không có quyền xoá comment này"**.
Thông báo tự động: *"{Tên} đã bình luận về task {tiêu đề}"*, *"… đã trả lời bình luận của bạn trong task …"*, *"… đã nhắc đến bạn trong một bình luận ở task …"*, *"… đã thả {emoji} vào bình luận của bạn trong task …"*.

### 6.4 Đính kèm file
Bảng `files` chung với `table = 'tasks'` / `'issues'`. Định dạng: jpg, jpeg, png, doc, docx, xls, xlsx, pdf, ppt, pptx; tối đa 20MB. Upload qua `POST files/upload`.

### 6.5 Chuyển người thực hiện
Không có chức năng riêng — đổi trực tiếp trường **Người thực hiện** (Task) hoặc **Người phụ trách xử lý** (Issue) trong modal Chỉnh sửa. Người có `can_handle` (Issue) cũng đổi được `assignee_id`.

### 6.6 Lịch sử chỉnh sửa
`TaskHistoryModal.vue` / `IssueHistoryModal.vue`, mở từ **Lịch sử chỉnh sửa** (Task) / **Lịch sử** (Issue). Timeline: thời điểm, hành động, người thực hiện. Nhãn: **Tạo mới task** / **Tạo mới issue** (xanh lá), **Cập nhật thông tin** (hổ phách), **Thay đổi trạng thái** (xanh dương). Với *Cập nhật* thì hiện diff từng trường (rỗng ghi **"(trống)"**). Rỗng → **"Chưa có lịch sử thao tác nào."**

### 6.7 Xuất Excel
Task: `danh_sach_task.xls`; Issue: `danh_sach_issue.xls`. Áp dụng bộ lọc đang chọn. Toast **"Xuất Excel thành công"** / **"Lỗi khi xuất Excel"**.

## 7. Trạng thái

### 7.1 Task
| Mã | Nhãn | Màu |
|---|---|---|
| 1 | **Nháp** | #94a3b8 |
| 2 | **Chờ phê duyệt triển khai** | #0ea5e9 |
| 3 | **Chờ bắt đầu** | #64748b |
| 4 | **Đang thực hiện** | #2563eb |
| 5 | **Tạm dừng** | #f59e0b |
| 6 | **Hoàn thành - Chờ duyệt** | #7c3aed |
| 7 | **Từ chối kết quả** | #ef4444 |
| 8 | **Hoàn thành** | #16a34a |
| 9 | **Huỷ** | #0f172a |
| 10 | **Từ chối triển khai** | #f43f5e |

**Mặc định khi tạo mới: 1 – Nháp.** Khi tạo mới chỉ chọn được 1, 2, 3 hoặc 4.

**Ma trận chuyển trạng thái:**
| Từ | Ai được chuyển | Sang |
|---|---|---|
| Nháp | Người tạo | Chờ bắt đầu, Chờ phê duyệt triển khai, Đang thực hiện |
| Chờ phê duyệt triển khai | Người có quyền *Duyệt triển khai task* trong phòng ban của người thực hiện | Chờ bắt đầu, Từ chối triển khai |
| Từ chối triển khai | Người tạo | Chờ phê duyệt triển khai, Chờ bắt đầu, Đang thực hiện |
| Chờ bắt đầu | Người thực hiện | Đang thực hiện (+ Từ chối triển khai nếu chưa có kết quả); Người thực hiện/Người tạo: Tạm dừng |
| Đang thực hiện | Người thực hiện | Hoàn thành (nếu không có người duyệt) hoặc Hoàn thành - Chờ duyệt; + Tạm dừng |
| Tạm dừng | Người thực hiện hoặc Người tạo | Đang thực hiện, Chờ bắt đầu |
| Hoàn thành - Chờ duyệt | **Người duyệt kết quả** | Hoàn thành, Từ chối kết quả |
| Từ chối kết quả | Người thực hiện | Đang thực hiện, Tạm dừng (+ Hoàn thành nếu không có người duyệt) |
| Hoàn thành | Người tạo | Từ chối kết quả (thu hồi) |

**Thao tác đổi trạng thái**: sửa task (dropdown Trạng thái), Nhập kết quả (dropdown Trạng thái), Duyệt. Không có nút đổi trạng thái nhanh trên danh sách.
Chặn: không cho *Từ chối triển khai* nếu task đã có kết quả — **"Không thể từ chối triển khai vì task đã có kết quả."**; sai bước → **"Không thể chuyển từ trạng thái hiện tại sang trạng thái mới này."**
Timestamp tự sinh: vào *Hoàn thành - Chờ duyệt* → ghi thời điểm gửi duyệt; vào *Hoàn thành* → ghi người duyệt + thời điểm; tính **Hiệu suất %**.

### 7.2 Issue
| Mã | Nhãn | Màu |
|---|---|---|
| `new` | **Mới ghi nhận** | #64748b |
| `assigned` | **Đã phân công** | #0ea5e9 |
| `in_progress` | **Đang xử lý** | #2563eb |
| `resolved` | **Đã xử lý xong** | #16a34a |
| `completed` | **Hoàn thành** | #22c55e |
| `rejected` | **Từ chối** | #f97316 |
| `closed` | **Đã đóng** | #94a3b8 |
| `reopened` | **Mở lại** | #ef4444 |

**Mặc định khi tạo mới: Mới ghi nhận.** Khi tạo mới chỉ chọn *Mới ghi nhận* hoặc *Đã phân công*.

**Ma trận chuyển:**
| Từ | Ai | Sang |
|---|---|---|
| Mới ghi nhận | Người tạo | Đã phân công |
| | Người xử lý | Đang xử lý |
| Đã phân công | Người xử lý | Đang xử lý |
| Đang xử lý | Người xử lý | Đã xử lý xong (nếu có người duyệt đóng) hoặc Hoàn thành |
| Đã xử lý xong | **Người duyệt đóng** | Hoàn thành, Từ chối |
| | Người xử lý/Người tạo (khi không có người duyệt) | Đang xử lý |
| Từ chối | Người xử lý | Đang xử lý |
| Hoàn thành | Người tạo hoặc Người xử lý | Mở lại |
| Mở lại | Người tạo → Đã phân công; Người xử lý → Đang xử lý | |
| **Đã đóng** | – | **trạng thái cuối** |
Hầu hết trạng thái cho phép **Người tạo hoặc Người xử lý** chuyển thẳng sang **Đã đóng**.
Bắt buộc lý do khi *Từ chối*: **"Vui lòng nhập lý do từ chối."**; sai bước → **"Chuyển trạng thái không hợp lệ."**

## 8. Phân quyền
| id | Tên quyền nguyên văn |
|---|---|
| 1020 | **Duyệt triển khai task** |
| 1103–1106 | **Xem danh sách task theo tổng công ty / công ty / phòng ban / bộ phận** |
| 1099–1102 | **Xem danh sách issue theo tổng công ty / công ty / phòng ban / bộ phận** |

> Các quyền *"Nhập kết quả công việc"*, *"Trưởng phòng duyệt kết quả công việc"* thuộc **phân hệ giao việc cũ**, **không** áp dụng cho màn Task/Issue này.

**`checkPermission` trên route: KHÔNG có bất kỳ middleware nào** trên `/assign/tasks` và `/assign/issues`. Toàn bộ kiểm soát ở tầng Service (lọc phạm vi) và Entity (`canEdit`/`canDelete`/`canHandle`/ma trận trạng thái).

**FE không ẩn/hiện nút nào theo tên quyền.** Nút Tạo mới / Sửa / Xóa / Nhập kết quả / Duyệt / Xử lý dựa vào cờ `can_edit`, `can_delete`, `can_import_result`, `can_approve`, `can_handle` do BE trả. Quyền chỉ dùng để cấu hình bộ lọc Công ty/Phòng ban/Bộ phận.

| Thao tác | Điều kiện |
|---|---|
| Xem danh sách | Luôn vào được, **dữ liệu giới hạn theo phạm vi** |
| Tạo mới Task/Issue | Không cần quyền |
| Sửa Task | Không có task con **và** mình là người tạo |
| Xóa Task | Không có task con, là người tạo, **và** trạng thái = Nháp |
| Nhập kết quả Task | Là người thực hiện **và** trạng thái ∈ {Chờ bắt đầu, Đang thực hiện, Từ chối kết quả} |
| Duyệt triển khai Task | Có quyền **"Duyệt triển khai task"**, trạng thái = Chờ phê duyệt triển khai, người thực hiện thuộc phòng ban mình quản lý |
| Duyệt kết quả Task | Là **Người duyệt kết quả** và trạng thái = Hoàn thành - Chờ duyệt |
| Sửa Issue | Là người tạo và issue chưa Đóng/Hoàn thành |
| Xóa Issue | Là người tạo và trạng thái = Mới ghi nhận |
| Xử lý Issue | Là người xử lý / người duyệt đóng / người tạo, tuỳ trạng thái |

### Phân quyền theo cấp — mô hình **3 tầng OR**
Có quyền **"Xem danh sách task/issue theo tổng công ty"** → thấy **toàn bộ**. Ngược lại hợp (OR) 3 tầng:
- **Tầng 1 — vai trò cá nhân**: người tạo, người thực hiện, người duyệt, người theo dõi (Issue thêm: người phối hợp, người phát hiện). Task còn **kế thừa cha–con** (thấy cha thì thấy con và ngược lại). Người có quyền *Duyệt triển khai task* còn thấy task của nhân viên trong phòng ban mình quản lý.
- **Tầng 2 — thành viên dự án/giải pháp**: thành viên giải pháp, thành viên hạng mục, phòng ban hỗ trợ dự án.
- **Tầng 3 — theo đơn vị tổ chức**: dùng bảng snapshot `task_org_units` / `issue_org_units`. Quyền *theo công ty* → toàn công ty hiện tại; *theo phòng ban* → phòng ban mình quản lý; *theo bộ phận* → bộ phận mình quản lý.

**Không có quyền nào ở nhóm "Xem danh sách…" → chỉ thấy việc của chính mình** (Tầng 1 + Tầng 2) — khác hẳn các màn khác (chỉ thấy bản ghi mình tạo).
Task ở trạng thái **Nháp** luôn chỉ người tạo nhìn thấy.

## 9. Không nhất quán phát hiện được
1. **Danh sách trạng thái Task khác nhau giữa các màn**: `/assign/tasks` và tab dự án có đủ 10 mục, nhưng tab *Công việc của tôi* và tab hạng mục chỉ có 5 mục cũ ("Đang tạo / Chờ duyệt / Đang làm / Hoàn thành / Tồn đọng") → lọc sai.
2. `IssueHistoryModal.vue` thiếu nhãn cho `completed` và `rejected` → lịch sử in key thô.
3. Nhãn trạng thái Issue lệch: danh sách *"Đã xử lý xong"* nhưng modal lịch sử *"Đã xử lý"*.
4. Xóa task ở tab Công việc của tôi dùng endpoint khác (`POST assign/tasks/{id}/delete`) so với các màn còn lại (`DELETE assign/tasks/{id}`).
5. `TaskController::deleteByIds` bỏ qua âm thầm task không đủ điều kiện (chưa có UI dùng).
6. Sắp xếp theo header không hoạt động: không cột nào khai báo `sortable: true`.
7. `TaskService::update` không kiểm tra `canEdit()` — chỉ chặn qua ma trận trạng thái.
8. `Issue::employee_create()` trỏ nhầm cột `created_by` trong khi lúc tạo chỉ set `creator_id` → cột *Người tạo* có thể trống.
