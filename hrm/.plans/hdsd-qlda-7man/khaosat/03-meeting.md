# Khảo sát — MEETING (Cuộc họp)

## 1. URL & phạm vi
| Chức năng | URL | File |
|---|---|---|
| Danh sách | `/assign/meeting` | `pages/assign/meeting/index.vue` |
| Tạo mới | `/assign/meeting/create` | `create.vue` |
| Sửa | `/assign/meeting/{id}/edit` | `_id/edit.vue` |
| Xem chi tiết | `/assign/meeting/{id}/show` | `_id/show.vue` |
| In biên bản (tab mới) | `/assign/meeting/{id}/print` | `_id/print.vue` |
| Bản in nhập phiếu khảo sát | `/assign/meeting/{id}/survey-input?projectIndex=N` | `_id/survey-input.vue` |
| Bản in phiếu khảo sát | `/assign/meeting/{id}/survey-print?projectIndex=N` | `_id/survey-print.vue` |
| Danh mục Loại meeting | `/assign/meeting_type` | `meeting_type/index.vue` |

Menu: **Meetings → Lịch Meeting**; **Danh mục → Loại meeting**.

**Meeting gắn dự án: CẢ HAI.** Thực thể độc lập, nhưng có checkbox **"Meeting theo dự án"** (`has_prospective_project`) gắn 1..n Dự án TKT. Tạo từ: nút **Tạo mới** ở `/assign/meeting`; hoặc tab Meetings của `/assign/solutions/{id}/manager`, `/assign/solution-modules/{id}/manager`, `/assign/prospective-projects/{id}/manager`, `/assign/request-solution`, `/assign/my-job` → push `/assign/meeting/create?project_id=...`. Khi có `project_id` trên URL thì Dự án TKT **tự chọn sẵn và bị khoá**.

## 2. Màn danh sách
### 2.1 Cột (cấu hình được qua nút Cấu hình cột)
STT · **Mã / Tên Meeting** (`code - name` + dòng phụ Người tạo, Ngày tạo, Cập nhật + cụm nút thao tác) · **Thời gian** (sortable — ngày họp + `giờ bắt đầu – giờ kết thúc`) · **Thời lượng họp** (`{n} phút`) · **Loại & Hình thức** (chip Loại meeting + chip Trực tiếp/Online) · **Khách hàng** (tên KH + `Người liên hệ: ... • SĐT`) · **Dự án tiền khả thi** · **Thành phần tham dự** (`Phía Công ty: n người` / `Phía KH: n người`) · **Trạng thái** · **Biên bản** (`Chưa lập biên bản` hoặc link `Biên bản cuộc họp_{code}` → popup **"Xem biên bản cuộc họp"**).

### 2.2 Bộ lọc
Lọc nhanh: ô `Tìm theo mã / tên meeting` + **Tìm kiếm** / **Làm mới** / **Tìm kiếm nâng cao**.
Lọc nâng cao (auto-search bằng deep watcher):
| Tiêu chí | Control | Nguồn |
|---|---|---|
| Công ty / Phòng ban / Bộ phận / Nhân viên | select | `V2BaseCompanyDepartmentFilter` — chỉ hiện theo quyền cấp |
| Loại Meeting | select | `apiGetMasterSelect meeting_types` |
| Dự án tiền khả thi | select | `GET assign/meeting/getListMeetingProject` |
| Khách hàng | select | `human/customers?customer_type=2` |
| Hình thức | select | Trực tiếp / Online |
| Trạng thái | select | Lưu nháp / Lên lịch hẹn / Đã chốt lịch / Đã hoàn thành / Huỷ |
| Có biên bản? | select | Đã lập biên bản / Chưa lập biên bản |
| Người cập nhật gần nhất | select | `allEmployeesOptions` |
| Ngày họp từ / đến | date dd/mm/yyyy | ràng buộc chéo từ ≤ đến |

Bộ lọc nhớ 10 phút trong localStorage key `assign_meeting`.

### 2.3 Nút thanh công cụ
**Tạo mới** → `/assign/meeting/create` · **Xuất Excel** → `GET assign/meeting/export` tải `danh_sach_cuoc_hop.xls`, toast **"Xuất Excel thành công"** / **"Lỗi khi xuất Excel"** · icon **Cấu hình cột hiển thị** (`table=meetings`).

### 2.4 Thao tác trên dòng
| Nút | Điều kiện | Hành động |
|---|---|---|
| **Xem** (mắt) | luôn | `/assign/meeting/{id}/show` |
| **Sửa** | `status ∉ {3 Hoàn thành, 4 Huỷ}` | `/assign/meeting/{id}/edit` |
| **In biên bản** | luôn | tab mới `/assign/meeting/{id}/print` |
| **Tạo phiếu công tác khác** | `status ∉ {3,4}` | tab mới `/assign/assign_business/add?meeting_id={id}` |
| **Xoá** | `status === 0` (Lưu nháp) | popup **"Xác nhận xóa"** — *"Bạn có chắc muốn xóa meeting '{tên}'?"*, nút Hủy/Xóa → `POST assign/meeting/{id}/delete`; toast **"Xóa thành công"** / **"Xoá thất bại"** / 404 → **"Dữ liệu đã thay đổi, vui lòng tải lại"** |

## 3. FORM TẠO MỚI
Form chung `components/MeetingForm.vue`. Đầu form là **thanh trạng thái** 4 bước: Lên lịch → Đã chốt → Hoàn thành → Huỷ; nhãn trạng thái hiện tại ở góc trái ("Trạng thái meeting: Lưu nháp").

### 3.1 Tab **Thông tin** — cột trái
| # | Nhãn | Control | Bắt buộc / message | Mặc định | Ẩn/hiện, readonly | Cascading / options |
|---|---|---|---|---|---|---|
| 1 | **Tên meeting** * | Input, placeholder `VD: Kickoff dự án ERP` | ✅ FE: **"Nhập Tên meeting."**; BE `required\|max:255` | trống | – | – |
| 2 | **Loại meeting** * | Select | ✅ BE `required` | trống | – | `GET assign/meeting_types/getAll` (chỉ loại đang hoạt động). **Chi phối cả form** qua `has_customer` |
| 3 | **Hình thức** | Select | không | trống | – | 1 Trực tiếp / 2 Trực tuyến (Online) |
| 4 | **Link họp (nếu Online)** | Input `https://...` | không, BE `nullable\|url` | trống | **chỉ khi Hình thức = Online** | – |
| 5 | **Địa điểm meeting** * (dấu * khi Trực tiếp) | Radio **Nhập** / **Chọn từ bản đồ** + Input | ✅ khi `mode_id=1` (BE `required_if:mode_id,1`) | radio = **Nhập**; ô trống | chế độ bản đồ → ô readonly, mở popup Google Map/OpenStreetMap | ghi chú cam: *"Nếu chọn nhập thủ công, thì khi làm phiếu giao đi công tác phải chọn lại địa điểm đến."* |
| 6 | **Bắt đầu** * | DatePicker datetime `DD/MM/YYYY HH:mm` | ✅ FE: **"Chọn thời gian bắt đầu/kết thúc."**; BE: **"Ngày giờ bắt đầu phải lớn hơn hoặc bằng thời điểm hiện tại."** | trống | chặn ngày quá khứ | – |
| 7 | **Kết thúc** * | DatePicker datetime | ✅ FE: **"Thời gian kết thúc phải sau thời gian bắt đầu."**; BE: **"Ngày giờ kết thúc phải lớn hơn hoặc bằng thời điểm hiện tại."**, **"Ngày giờ kết thúc phải lớn hơn ngày giờ bắt đầu."** | trống | chặn quá khứ | – |
| 8 | **Meeting theo dự án** | Checkbox | không | **bỏ tích** (auto tích nếu vào từ dự án) | – | tích → hiện Dự án TKT + tab "Dự án tiền khả thi" |
| 9 | **Dự án TKT** * | MultiSearchPicker (chọn nhiều, tìm theo mã/tên) | hiện khi (8) tích. BE: **"Vui lòng chọn ít nhất hoặc tạo mới một dự án TKT."** | trống, hoặc **điền sẵn + khoá** khi mở từ dự án | khoá khi vào từ dự án | `GET assign/prospective-projects/getForMeeting`; **lọc theo Khách hàng đã chọn**; chọn dự án đầu tiên → **tự điền Khách hàng** |
| 9b | Mỗi dự án → thẻ mở rộng: **Giải pháp**, **Hạng mục/Module** | SearchPicker | không | trống | Hạng mục disable đến khi chọn Giải pháp | Giải pháp lọc theo dự án; Module lọc theo Giải pháp |

**Khối "Khách hàng & Người liên hệ"** (badge **Bắt buộc**) — chỉ hiện khi Loại meeting có `has_customer`, hoặc đã tích Meeting theo dự án, hoặc đã có KH:
| Nhãn | Control | Bắt buộc | Mặc định | Ghi chú |
|---|---|---|---|---|
| **Khách hàng** * | ô readonly → popup **Chọn khách hàng ERP** + nút **Thêm nhanh khách hàng** | ✅ BE `customer_name required`. FE: **"Meeting với KH cần chọn Khách hàng."** | trống | Nút Thêm nhanh chỉ khi có quyền tạo KH. Có nút (x) xoá KH |
| (khối xám readonly) Mã khách hàng, MST, SĐT, Họ và tên, Địa chỉ, Liên hệ | text | – | tự điền từ ERP | SĐT có thể hiển thị `-` nếu không đủ quyền |
| **Người liên hệ** | Select remote + nút **Thêm nhanh** | KH doanh nghiệp: bắt buộc. FE: **"Meeting với KH cần: Khách hàng và Người liên hệ (Tên + SĐT)."** | tự chọn liên hệ đầu tiên chưa bị khoá | **Ẩn toàn bộ khối khi KH cá nhân** (`customer_type=1`). Gõ **đầy đủ SĐT** để tìm liên hệ khác. Liên hệ đang bị Sales khác đăng ký → **"Đã có người đăng ký nên bạn không được phép chọn"** |
| (Thêm nhanh liên hệ) **Họ tên** *, **Chức vụ** *, **SĐT** * | Input | cả 3 ✅ | trống | nút **Hủy** / **Lưu & chọn** → `POST assign/meeting/addContact`, toast **"Thao tác thành công!"** |
| Tên người liên hệ / Chức vụ / SĐT | Input | – | tự điền | **luôn readonly** |
| **Mục tiêu / Nội dung** | Textarea 3 dòng | không (BE max 1000) | trống | – |

### 3.2 Cột phải — thành phần tham dự
**Thành phần — Phía Công ty** (bảng STT / Họ tên / Chức vụ / SĐT / nút xoá):
- Mặc định khi tạo mới: **tự thêm chính người đang tạo** (họ tên, chức vụ, SĐT từ hồ sơ nhân viên).
- Nút **Thêm nhân viên** → popup **"Chọn nhân viên phía công ty"**: lọc Công ty/Phòng ban/Bộ phận + ô **Nhân viên**, nút **Tìm kiếm**/**Làm mới**, bảng Họ tên / Phòng ban / Email / SĐT có checkbox chọn nhiều, phân trang; footer **Thêm {n} nhân viên** / **Đóng**.
- BE: `company_members` **required|array**, mỗi dòng `name` bắt buộc, `phone` dạng `0xxxxxxxxx` (9–11 số).

**Thành phần — Phía Khách hàng** (chỉ khi loại meeting có KH): dòng nhập tay **Họ tên / Chức vụ / SĐT**, nút **+** thêm dòng, thùng rác xoá. Người liên hệ đã chọn tự được đưa vào. Ghi chú: *"* Mặc định có thể thêm người liên hệ đã chọn ở trên."*

### 3.3 Tab **Điểm danh**
Bảng: STT / Họ và tên / Chức vụ – Phòng ban / **Thành phần** (chip Nội bộ / Khách hàng) / **Trạng thái điểm danh** / **Ghi chú / Lý do**.
Chip trạng thái: **Có mặt** (1) / **Vắng có lý do** (2) / **Vắng không lý do** (3); chưa chọn hiển thị *Dự kiến tham gia* (0).
Nút **Điểm danh nhanh: Tất cả có mặt**.
**Chỉ sửa được khi meeting ở trạng thái Đã chốt lịch (2) và đang ở màn Sửa**; trạng thái khác chỉ xem.

### 3.4 Tab **Biên bản** — 3 phần
**a) Biên bản cuộc họp** — nút **Thêm dòng**, **Xoá hết**, **In**, **Excel**. Bảng:
| Cột | Control | Bắt buộc |
|---|---|---|
| STT | readonly | – |
| **Nội dung / Vấn đề trao đổi** * | Textarea | BE `required\|max:1000` |
| Phương án xử lý | Textarea | không (max 2000) |
| Người đề xuất | ô readonly + nút chọn → popup **"Chọn người đề xuất"** | không |
| **Người thực hiện** * | ô readonly + nút chọn → popup **"Chọn người thực hiện"** | BE `executor_name required` |
| **Hạn dự kiến** * | DatePicker `DD/MM/YYYY`, chặn quá khứ | BE `required`, **"Phải lớn hơn hoặc bằng ngày hiện tại."** |

Popup chọn người có 2 tab **Nhân sự Công ty** / **Nhân sự Khách hàng** (tab KH chỉ khi loại meeting có KH).
Nút **Excel** xuất `Bien_ban_cuoc_hop_{mã}.xlsx` dựng tại trình duyệt; nút **In** mở `/assign/meeting/{id}/print`.

**b) Import tài liệu kèm biên bản** — nút **Thêm tài liệu**; mỗi dòng: STT / **Tên tài liệu** * (BE `required|max:255`) / **Upload / File** * (nút **Chọn tệp**, chấp nhận `.jpg .jpeg .png .doc .docx .xls .xlsx .pdf`, **tối đa 20MB**, upload ngay) / Dung lượng / nút xoá. File đã có: icon + tên + **Xem trước** / **Tải xuống** / **Thay đổi**. Lỗi: *"Định dạng file không hợp lệ. Chỉ chấp nhận: ..."*, *"File {tên} quá lớn. Kích thước tối đa là 20MB."*, *"Tải lên thất bại: {tên}"*.

**c) Kết luận cuộc họp** * — Textarea 5 dòng, ghi chú cam: *"Bắt buộc nhập kết luận cuộc họp khi hoàn thành"*. BE `conclusion` `required_if:status,3|max:4000`.

### 3.5 Tab **Dự án tiền khả thi** (chỉ khi tích "Meeting theo dự án")
- Nút **Thêm dự án** (chỉ khi đã chọn KH và không vào từ dự án); mỗi dự án là sub-tab **Dự án 1, Dự án 2...** kèm nút (x).
- 2 tab con:
  - **Thông tin chung**: tái sử dụng `CustomerInfoSection` + `ProjectInfoSection` của màn Dự án TKT. BE bắt buộc: `projects.*.address`, `projects.*.project_scale_id`, `projects.*.investment_type_id`.
  - **Phiếu thu thập thông tin**: nút **Lưu phiếu** (`POST assign/meeting/{id}/project/{index}/save-form-answers`, toast **"Lưu phiếu thu thập thông tin thành công"**), **Xem bản in nhập**, **Xem bản in**. Chưa chọn Ứng dụng: *"Vui lòng chọn Ứng dụng (ở phân vùng Khách hàng) và lưu lại để tải phiếu thu thập thông tin."*; không tìm thấy mẫu: *"Không tìm thấy phiếu thu thập thông tin phù hợp."*

> Tab nào có lỗi validate sẽ được tô đỏ + tự nhảy tới field lỗi đầu tiên.

## 4. Nút lưu & điều hướng
Khi **tạo mới**: **Lưu nháp**, **Lưu và Lên lịch**, **Lưu và Chốt lịch**, **Quay lại**.
| Nút | Status | API | Toast | Sau lưu |
|---|---|---|---|---|
| **Lưu nháp** | 0 | `POST assign/meeting` | **"Thêm mới thành công"** | về `/assign/meeting` |
| **Lưu và Lên lịch** | 1 + `send_notification=1` | như trên | như trên | **gửi thông báo lịch họp** cho thành viên phía Công ty |
| **Lưu và Chốt lịch** | 2 | như trên | như trên | **gửi thông báo chốt lịch** |
| **Quay lại** | – | – | – | về trang nguồn hoặc `/assign/meeting` |

Lỗi khi lưu: 400 → **"Bạn chưa nhập đầy đủ thông tin"** + lỗi inline; 403 → **"Bạn không có quyền thực hiện chức năng này"**; 423 → message BE (*"Thao tác không thành công. Dữ liệu đã được thay đổi hoặc chuyển trạng thái bởi người dùng khác. Vui lòng tải lại trang..."*); còn lại → **"Có lỗi xảy ra"**.

**Mã meeting** tự sinh: `{Mã công ty}.MET.{KH|NB}.{2 số cuối năm}.{STT 4 chữ số}` (VD `TPE.MET.KH.26.0001`) — `KH` khi loại meeting có khách hàng, `NB` khi nội bộ. Công ty/Phòng ban/Bộ phận lấy theo hồ sơ người tạo.

## 5. CHỈNH SỬA
| Khía cạnh | Chi tiết |
|---|---|
| Nạp dữ liệu | `GET assign/meeting/{id}`; lỗi → **"Có lỗi xảy ra khi tải dữ liệu"** |
| API lưu | `POST assign/meeting/{id}`; toast **"Cập nhật thành công"** |
| Trường khoá | Dự án TKT khoá nếu mở từ dự án; Tên/Chức vụ/SĐT người liên hệ luôn readonly; **Điểm danh chỉ mở khi status = 2** |
| Ràng buộc ngày | status=1: `start_date` ≥ hiện tại (**"Phải sau hoặc bằng thời gian hiện tại"**); status khác: ≥ ngày tạo meeting (**"Phải sau hoặc bằng thời gian tạo meeting"**); `end_date` **"Phải sau hoặc bằng thời gian bắt đầu"** |
| Điều kiện được sửa | BE: không có quyền xem → 403 **"Bạn không có quyền sửa meeting này!"**; status = 3 hoặc 4 → 423. FE ẩn nút Sửa khi status ∈ {3,4} |
| SĐT bị che | Người không đủ quyền thấy SĐT KH là `-`; khi lưu BE tự khôi phục số thật |

**Bộ nút theo trạng thái:**
| Trạng thái | Nút |
|---|---|
| Tạo mới / 0 Lưu nháp | Lưu nháp • Lưu và Lên lịch • Lưu và Chốt lịch • Quay lại |
| 1 Lên lịch hẹn | **Lưu** (giữ status 1, không báo lại) • Lưu và Lên lịch (gửi lại thông báo) • Lưu và Chốt lịch • Hủy • Quay lại |
| 2 Đã chốt lịch | Lưu • **Hoàn thành** • Hủy • Quay lại |
| 3 Đã hoàn thành | chỉ Quay lại |
| Màn Xem chi tiết | Sửa (status ∉ {3,4}) • Xóa (chỉ status 0) • Hủy (status 1,2) • Tạo phiếu công tác khác • Quay lại |

## 6. Các thao tác khác
| Thao tác | Mở ra gì / nhập gì | Kết quả |
|---|---|---|
| **Xóa** | Popup **"Xác nhận xóa"** — *"Bạn có chắc chắn muốn xóa meeting này?"* | `POST /{id}/delete`. Chỉ khi status=0. Toast **"Xóa thành công"** / **"Xóa thất bại"** |
| **Hủy meeting** | Popup **"Xác nhận huỷ meeting"** — *"Bạn có chắc chắn muốn huỷ meeting này không?"* + ô **"Lý do huỷ (không bắt buộc)"** (placeholder *"Nhập lý do huỷ (nếu có)"*) | `POST /{id}/change-status` status=4 + `cancel_reason`. Toast **"Cập nhật thành công"**; **gửi thông báo huỷ**: *"{Tên meeting} đã bị {người huỷ} huỷ. Lý do: ..."*. Không huỷ được meeting đã Hoàn thành |
| **Hoàn thành** | Kiểm tra trước: chưa có biên bản → **"Vui lòng thêm biên bản cuộc họp trước khi hoàn thành!"** + nhảy tab Biên bản; chưa điểm danh đủ → **"Vui lòng hoàn thành điểm danh cho tất cả thành viên trước khi chốt biên bản và hoàn thành cuộc họp."** + nhảy tab Điểm danh | Lưu status=3. BE bắt buộc **Kết luận cuộc họp** |
| **Đổi thời gian khi đã chốt lịch** | Popup **"Xác nhận thay đổi thời gian"** — *"Thời gian cuộc họp đã thay đổi so với lịch đã chốt trước đó. Việc lưu sẽ gửi lịch họp mới đến tất cả thành viên tham dự. Bạn có xác nhận gửi lịch họp mới không?"*, nút Hủy / **Xác nhận gửi lịch** | Lưu status 2 và gửi lại lịch |
| **In biên bản** | Tab mới `/assign/meeting/{id}/print`, hoặc popup **"Xem biên bản cuộc họp"** từ danh sách | mẫu in mã `BIEN_BAN_CUOC_HOP`. Lỗi: **"Không thể tải biên bản"** / **"Không thể in biên bản cuộc họp"** |
| **Tạo phiếu công tác khác** | Tab mới `/assign/assign_business/add?meeting_id=...` kèm địa điểm meeting | tạo phiếu đi công tác |
| **Thông báo cho người tham dự** | Tự động, không có nút riêng | Thông báo nội bộ (không email) cho **thành viên phía Công ty** khi Lên lịch (1) / Chốt lịch (2) / Huỷ (4). Bấm **Lưu** ở trạng thái Lên lịch thì **không** gửi |

## 7. Trạng thái
| Mã | Nhãn | Đổi bằng |
|---|---|---|
| 0 | **Lưu nháp** (BE: "Đang tạo") | nút **Lưu nháp**. Meeting nháp **chỉ người tạo nhìn thấy** |
| 1 | **Lên lịch hẹn** | **Lưu và Lên lịch** |
| 2 | **Đã chốt lịch** | **Lưu và Chốt lịch** |
| 3 | **Đã hoàn thành** | **Hoàn thành** (cần biên bản + điểm danh đủ + kết luận) |
| 4 | **Huỷ** | **Hủy** |

**Mặc định khi tạo mới: chưa có trạng thái** — quyết định bởi nút bấm khi lưu.

## 8. Phân quyền
| ID | Tên quyền nguyên văn |
|---|---|
| 1095 | **Xem danh sách meeting theo tổng công ty** |
| 1096 | **Xem danh sách meeting theo công ty** |
| 1097 | **Xem danh sách meeting theo phòng ban** |
| 1098 | **Xem danh sách meeting theo bộ phận** |
| 989 | **Quản lý danh mục loại meeting** |
| 1004 | **Xem danh mục loại meeting** |

| Thao tác | Quyền |
|---|---|
| Vào danh sách, tạo, sửa, xoá, huỷ, hoàn thành | **Không có quyền riêng** — route `Routes/Meeting/api.php` không gắn `checkPermission`, chỉ cần đăng nhập |
| Phạm vi dữ liệu | Luôn thấy meeting **mình tạo** + meeting mình có tên trong **Thành phần phía Công ty**; 4 quyền "Xem danh sách meeting theo …" mở rộng theo cấp |
| Xem/sửa qua URL trực tiếp | BE chặn bằng `canView()` → 403 *"Bạn không có quyền xem meeting này!"* / *"...sửa meeting này!"* |
| Nhìn SĐT khách hàng đầy đủ | 4 quyền trên; không đủ → hiển thị `-` |
| Hiện ô lọc Công ty/Phòng ban/Bộ phận/Nhân viên | 4 quyền trên |
| Nút "Thêm nhanh khách hàng" | quyền tạo KH |
| Danh mục Loại meeting: xem | `Quản lý danh mục loại meeting` hoặc `Xem danh mục loại meeting` |
| Danh mục Loại meeting: thêm/sửa/xoá/khoá/import/export | `Quản lý danh mục loại meeting` (có middleware) |

**Phân quyền theo cấp (2 lớp):**
1. Meeting trạng thái **Đang tạo (nháp)** chỉ **người tạo** thấy.
2. Tập id theo `checkPermissionList` chuẩn trên bảng `meetings`.
3. **Mở rộng (OR)**: dù không có quyền cấp nào, vẫn thấy meeting **mình tạo** HOẶC **mình có tên trong "Thành phần — Phía Công ty"**.

## 9. Danh mục Loại meeting
Modal **Thêm / Sửa / Xem loại meeting**: **Loại meeting** * (unique), **Trạng thái** (mặc định Đang hoạt động), **Mô tả**, checkbox **Có khách hàng** (mặc định tích). `has_customer` là công tắc điều khiển toàn bộ khối Khách hàng/Người liên hệ/Thành phần KH/Dự án TKT ở form meeting và quyết định mã meeting là `KH` hay `NB`. Loại meeting đã dùng thì không sửa/xoá được (tooltip: *"Không thể xóa bản ghi, bản ghi hiện tại đã có dữ liệu liên kết đang tồn tại trên hệ thống"*).

## 10. Lưu ý nghiệp vụ
1. Meeting **Lưu nháp** chỉ người tạo thấy.
2. Chọn **Loại meeting** trước tiên — quyết định có phần Khách hàng hay không.
3. Người tạo **tự động** nằm trong Thành phần phía Công ty; đây cũng là danh sách nhận thông báo.
4. **Điểm danh** chỉ mở khi *Đã chốt lịch*; phải điểm danh hết mới Hoàn thành được.
5. **Hoàn thành** bắt buộc: ≥1 dòng biên bản + điểm danh đủ + Kết luận cuộc họp.
6. Meeting **Đã hoàn thành / Đã huỷ** không sửa, không xoá; chỉ **Lưu nháp** mới xoá được.
7. Người đề xuất/thực hiện là **nhân sự Khách hàng** thì tên phải trùng đúng một thành viên trong Thành phần phía KH.
8. KH **cá nhân** không cần Người liên hệ (ẩn khối); KH **doanh nghiệp** bắt buộc Tên + SĐT liên hệ.
