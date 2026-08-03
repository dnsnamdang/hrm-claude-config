# Khảo sát — YÊU CẦU LÀM GIẢI PHÁP

## Sơ đồ luồng
```
Dự án TKT → A. Tạo YÊU CẦU LÀM GIẢI PHÁP → Tiếp nhận (Trưởng phòng GP)
  /assign/prospective-projects   /assign/request-solution/add   /assign/request-solution/pending
       ↓                                                              ↓
  B. Tạo & sửa GIẢI PHÁP → Phân hạng mục cho Leader → C. HỒ SƠ TRÌNH DUYỆT giải pháp
     /assign/solutions/add                              /assign/solutions/{id}/manager
       ↓                                                              ↓
  BOM tổng hợp → Báo giá → Trúng thầu → D. LẬP HỢP ĐỒNG ERP → Chốt giải pháp
```

## A. TẠO MỚI YÊU CẦU LÀM GIẢI PHÁP

### A.1 Điểm vào
| Mục | Giá trị |
|---|---|
| Menu | Quản lý dự án TKT → **Yêu cầu giải pháp** |
| Danh sách | `/assign/request-solution` |
| Nút tạo | **Tạo mới** (icon `ri-add-line`, primary) |
| URL form | `/assign/request-solution/add` |
| Tiêu đề | `Tạo yêu cầu làm giải pháp` |

> Màn riêng, không phải popup trong dự án. Bắt buộc chọn 1 dự án TKT đã có.

### A.2 Các tab trong form
| Tab | Nhãn | Điều kiện hiện |
|---|---|---|
| req | **Thông tin yêu cầu** | Luôn (mặc định active) |
| tkt | **Dự án tiền khả thi** | Luôn — chỉ xem, kế thừa từ dự án |
| meeting | **Meetings** | Luôn — danh sách meeting của dự án |
| add-form | **Phiếu thu thập thông tin** | Chỉ khi `canReceive = true` (người tiếp nhận, ở màn chi tiết) |

### A.3 Tab "Thông tin yêu cầu" — từng trường
| # | Nhãn | Control | Bắt buộc + message | Mặc định | Ẩn/hiện/readonly | Cascading | Options |
|---|---|---|---|---|---|---|---|
| 1 | **Dự án tiền khả thi** * | V2BaseSelect, `-- Chọn dự án --` | `required` → **`Bắt buộc phải nhập`**; `exists` → **`Dự án tiền khả thi không tồn tại.`**; `unique` → **`Dự án tiền khả thi này đã tồn tại yêu cầu làm giải pháp.`** | trống | mode xem → thay bằng **Mã yêu cầu** + **Trạng thái** (pill màu) | **Chọn dự án → nạp tab TKT, panel KD, tự điền 2 ngày, nạp Meetings, nạp Phiếu thu thập** | `assign/prospective-projects/getAll?forRequestSolution=true` (mode create — chỉ dự án chưa có YC). **Lọc bỏ dự án có `is_form_complete === false`** |
| 2 | **Tên yêu cầu** * | V2BaseInput, `VD: Yêu cầu làm giải pháp dây chuyền gara...` | `required`; `max:255` → **`Tiêu đề không được vượt quá 255 ký tự.`**; `unique` → **`Tiêu đề đã tồn tại.`** | trống | – | – | – |
| 3 | **Phòng tiếp nhận yêu cầu** * | V2BaseSelect, `-- Chọn phòng tiếp nhận --` | `required` | Dự án **Triển khai theo Phòng** (type=2): tự điền = phòng KD phụ trách chính | **Khoá khi dự án type=2** | watch implementation_type | `$store.state.departments` |
| 4 | **Ứng dụng** * | V2BaseInput `—` | chỉ đánh sao UI, BE không validate | Kế thừa từ dự án | **readonly luôn** | quyết định options #5, #6 | `optionsSelect/getApplications` |
| 5 | **Nhóm ngành** | V2BaseSelect `Chọn nhóm ngành` | nullable; sai app → **`Nhóm ngành không thuộc Ứng dụng của dự án.`**; chưa có app → **`Dự án chưa có Ứng dụng nên không thể chọn Nhóm ngành.`** | trống | – | Lọc theo `application.scope_ids` | `optionsSelect/getScopes` |
| 6 | **Nhóm giải pháp** | V2BaseSelect `Chọn nhóm giải pháp` | nullable; sai app → **`Nhóm giải pháp không thuộc Ứng dụng của dự án.`** | trống | – | Lọc theo `application.industry_ids` | `optionsSelect/getIndustries` |
| 7 | **Ngày KH cần giải pháp** * | V2BaseDatePicker | `required\|date` | Tự điền `customer_need_solution_date` của dự án | – | – | – |
| 8 | **Ngày KH cần báo giá** * | V2BaseDatePicker | `required\|date` | trống | – | – | – |
| 9 | **Ngày cần nhận GP nội bộ** | V2BaseDatePicker | `nullable\|date` | Tự điền `internal_solution_close_date` của dự án | – | – | – |
| 10 | **Hạn hoàn thành tiếp nhận** | V2BaseInput | – | BE tính `sent_date + response_days + response_hours` theo Mức độ ưu tiên | **disabled**, chỉ hiện khi có giá trị. Format `DD/MM/YYYY HH:mm` | – | – |
| 11 | **Mô tả / ghi chú yêu cầu** | V2BaseTextarea 3 dòng, `Mô tả ngắn nội dung yêu cầu, phạm vi, tài liệu đầu vào...` | `nullable\|max:1000` → **`Ghi chú không được vượt quá 1000 ký tự.`** | trống | – | – | – |
| 12 | **File gửi kèm** | FileAttachmentTable | `files.*.name`, `files.*.file_path` required | 0 dòng | – | – | – |

**Bảng "File gửi kèm"**: nút **Thêm file**; cột **STT**, **Tên tài liệu**, **File đính kèm** (nút `Chọn file`), **Dung lượng**, **Thao tác**. Empty: `Chưa có tài liệu đính kèm. Bấm Thêm file để bắt đầu.`

**Panel "Phụ trách KD nội bộ"** — chỉ xem, tự đổ theo dự án: `Phòng KD phụ trách chính` (Phòng / KD phụ trách chính: Họ tên, SĐT, Email) và `Phòng KD hỗ trợ & KD hỗ trợ`.

> **Hạn tiếp nhận (`need_receive_date`)** BE tính từ `sent_date + response_days/response_hours` của Mức độ ưu tiên trong Giai đoạn dự án, **trừ ngày nghỉ lễ và theo phân ca của trưởng phòng tiếp nhận** — không phải cộng thẳng.

### A.4 Nút lưu
| Nút | Nhãn | status | Trạng thái tạo ra |
|---|---|---|---|
| Trái | **Lưu nháp** | 1 | 1 – Nháp |
| Phải | **Lưu và gửi** | 2 | 2 – Chờ tiếp nhận |
| Cuối | **Quay lại** | – | về `/assign/request-solution` |

- **Lưu và gửi** → modal xác nhận: tiêu đề **`Xác nhận lưu và gửi`**, nội dung **`Bạn đồng ý lưu và gửi ?`**
- API `POST assign/request-solutions`. Toast: **`Đã lưu thành công!`** → về `/assign/request-solution`.
- 422 → **`Vui lòng kiểm tra lại thông tin`** + lỗi inline. 423 → **`Phiếu thu thập thông tin chưa đủ các trường yêu cầu`**. Khác → **`Đã xảy ra lỗi. Vui lòng thử lại.`**

**Sinh mã**: `{Mã công ty}.YCP.{CN|TC}.{yy}.{4 số}` — CN = KH cá nhân, TC = tổ chức.
**Chặn nghiệp vụ**: dự án **Tự triển khai** (type=1) → 422 **`Dự án tự triển khai không cần tạo yêu cầu làm giải pháp.`**
**Thông báo khi gửi**: cho tất cả nhân viên thuộc phòng tiếp nhận / quản lý phòng đó / quản lý toàn công ty VÀ có quyền `Tiếp nhận yêu cầu làm giải pháp`. Tiêu đề `Thông báo yêu cầu làm giải pháp mới`, nội dung `Bạn có yêu cầu làm giải pháp mới cần tiếp nhận: {code} - {title}`.

### A.5 Màn danh sách
Lọc: quick search `Tìm theo Mã yêu cầu, Tên yêu cầu`; nâng cao: Công ty/Phòng ban (theo quyền), **Nhân viên gửi yêu cầu**, **Tiến trình YC**, **Phòng tiếp nhận YC**, **Người tiếp nhận YC**, **Thời gian tạo từ / Đến**.
Cột: STT, **Mã • Tên yêu cầu**, **Mã • Tên dự án TKT**, **Mã • Tên KH**, **Giai đoạn dự án**, **Mức độ ưu tiên**, **Tiến trình YC**, **Ngày gửi YC**, **Ngày cần tiếp nhận YC**, **Ngày chốt GP**, **Ngày KH cần GP**.
| Nút dòng | Điều kiện | Đích |
|---|---|---|
| **Xem chi tiết** | luôn | `/assign/request-solution/{id}` |
| **Sửa** | `status ∈ {1 Nháp, 9 Yêu cầu bổ sung}` | `/assign/request-solution/{id}/edit` |
| **Xóa** | `status ∈ {1, 9}`; BE chỉ cho status=1 | modal `Xác nhận xóa` |
| **Làm giải pháp** | `receive_id == mình && status == 3` | `/assign/solutions/add?request_solution_id={id}` |
Nút khác: **Xuất Excel**, **Cấu hình cột hiển thị**.

### A.6 Sửa yêu cầu
Tiêu đề `Chỉnh sửa yêu cầu làm giải pháp`. Nút **Lưu nháp** (chỉ khi status=1) + **Lưu và gửi**. `PUT assign/request-solutions/{id}`. Toast **`Đã cập nhật thành công!`**
BE chỉ cho sửa khi `status ∈ {1, 9}`, sai → 403 **`Không có quyền!`**; đã Đóng → 422 **`Yêu cầu làm giải pháp đã đóng theo dự án, không thể sửa.`**

### A.7 TIẾP NHẬN yêu cầu
- Menu **Phê duyệt → Yêu cầu giải pháp** → `/assign/request-solution/pending` (chỉ khi có quyền `Tiếp nhận yêu cầu làm giải pháp`).
- Lọc: `status = 2` + phòng tiếp nhận thuộc phạm vi quản lý (type=3) hoặc chính phòng mình (type=2).

| Nút dòng | Nhãn | Hành động |
|---|---|---|
| `ri-eye-line` | **Xem chi tiết** | `/assign/request-solution/{id}` |
| `ri-file-add-line` | **Yêu cầu bổ sung thông tin** | `/assign/request-solution/{id}?tab=add-form` |
| `ri-inbox-archive-line` | **Tiếp nhận** | mở modal tiếp nhận |

**Modal "Tiếp nhận yêu cầu làm GP: {mã} - {tên}"**:
- Khối chỉ xem **Thông tin tóm tắt yêu cầu**: KD gửi yêu cầu, Ngày gửi yêu cầu, Mã - Tên dự án, Mã - Tên khách hàng, Giai đoạn dự án, Mức độ ưu tiên, Ngày cần nhận GP nội bộ, Phòng tiếp nhận, Ngày cần tiếp nhận YC.
- Khối nhập **Thông tin người tiếp nhận cần nhập**:

| Nhãn | Control | Bắt buộc / message | Mặc định | Ghi chú |
|---|---|---|---|---|
| **Ngày dự kiến xong GP (v1)** * | V2BaseDatePicker `DD/MM/YYYY` | `required\|date`; sai định dạng → **`Ngày dự kiến xong GP không hợp lệ`** | trống | **Chặn chọn ngày sau "Ngày KH cần giải pháp"** |
| **PM làm GP** * | V2BaseSelectInModal `-- Chọn PM --` | `required`; **`PM không hợp lệ`** / **`PM không tồn tại`** | trống | Toàn bộ nhân viên |
| **SĐT PM** | V2BaseInput | **`Số điện thoại PM không hợp lệ`** | Tự điền theo PM | **disabled** |
| **Ghi chú** | V2BaseTextarea 3 dòng | max 1000 → **`Ghi chú PM không được vượt quá 1000 ký tự`** | trống | – |

- Nút **Xác nhận tiếp nhận** / **Đóng**. `PUT assign/request-solutions/{id}/receive`.
- Toast **`Thao tác thành công`**; 422 → `Lỗi khi tiếp nhận yêu cầu`; **409 → `Phiếu đã được tiếp nhận, vui lòng tải lại dữ liệu`**.
- Kết quả: status → **3 – Đã tiếp nhận**, ghi `receive_id`, `responded_date`, đánh giá `Trong hạn`/`Quá hạn`.
- Màn chi tiết cũng có nút **Tiếp nhận** ở footer khi `is_can_receive`.

**Yêu cầu bổ sung thông tin**: tab **Phiếu thu thập thông tin** → nút **Thêm câu hỏi** (nhập `Nội dung câu hỏi:`, placeholder `Nhập nội dung câu hỏi...`, nút `Thêm`/`Hủy`) → nút **Yêu cầu bổ sung**. Toast **`Đã lưu yêu cầu bổ sung câu hỏi thành công!`**. YC chuyển **9 – Yêu cầu bổ sung**, KD sửa và gửi lại (deadline tính lại).

### A.8 Trạng thái Yêu cầu làm giải pháp
| Giá trị | Nhãn | Sinh ra khi |
|---|---|---|
| 1 | **Nháp** | Lưu nháp (mặc định) |
| 2 | **Chờ tiếp nhận** | Lưu và gửi |
| 9 | **Yêu cầu bổ sung** | Người tiếp nhận bấm "Yêu cầu bổ sung" |
| 3 | **Đã tiếp nhận** | Xác nhận tiếp nhận |
| 4 | **Từ chối** | (luồng đã comment trên FE) |
| 6 | **Đang thực hiện** | Khi tạo Giải pháp từ YC |
| 8 | **Đã hoàn thành** | Khi "Chốt giải pháp" ở dự án |
| 10 | **Đóng** | Cascade khi đóng dự án TKT |
| 11 | **Đã chốt giải pháp** | (hằng số khai báo) |

## B. CHỈNH SỬA GIẢI PHÁP

### B.1 Màn
| Mục | URL |
|---|---|
| Tạo mới | `/assign/solutions/add` — `Tạo quản lý làm giải pháp` |
| **Sửa** | `/assign/solutions/{id}/edit` — **`Cập nhật quản lý làm giải pháp`** |
| Sửa ở chế độ duyệt | `/assign/solutions/{id}/edit?mode=approve` |
| Xem | `/assign/solutions/{id}` |
| Quản lý | `/assign/solutions/{id}/manager` |

### B.2 Khác tạo mới
| Điểm | Tạo mới | Sửa |
|---|---|---|
| Nguồn dữ liệu | từ `?request_solution_id=` hoặc `?prospective_project_id=` | `GET assign/solutions/{id}` |
| Chọn YC làm GP | có select khi vào từ danh sách GP | không hiển thị |
| Mã GP | sinh mới `{mã dự án}_GP{lastId}` | hiển thị mã đã lưu |
| Nút | **Lưu nháp** + **Lưu và gửi** | đổi theo trạng thái (B.6) |
| Quyền | không chặn | `can_edit === false` → toast **`Bạn không có quyền!`** + redirect |
| Chống ghi đè | – | gửi kèm `current_status`; lệch → 409 **`Dữ liệu đã được cập nhật bởi người khác hoặc tab khác. Vui lòng tải lại trang!`**, tự reload sau 2s |
| Khoá khối Thông tin GP | – | `status >= 3 && status != 2` → khoá |

### B.3 Các tab form GP
| Tab | Nhãn | Điều kiện |
|---|---|---|
| info | **Thông tin** | Luôn |
| modules | **Quản lý hạng mục** | `has_modules === true` |
| orgchart | **Sơ đồ nhân sự** | Luôn (chỉ xem) |
Có lỗi 422 → tự nhảy sang tab chứa lỗi.

### B.4 Tab "Thông tin"
**Card 1 – Thông tin dự án** (chỉ xem): Khách hàng (link), Khách hàng cuối, Dự án (link + `KD phụ trách:`, `Giai đoạn:`, `Ngày hoàn thành dự án:`), Yêu cầu làm GP (link + `Ngày KH cần GP:`, `Ưu tiên:` — **ẩn với dự án Tự triển khai**).

**Card 2 – Thông tin GP**:
| # | Nhãn | Control | Bắt buộc | Mặc định | Readonly |
|---|---|---|---|---|---|
| 1 | **Phòng làm GP** | Input | – | Phòng tiếp nhận của YC, fallback phòng user, fallback `Phòng Giải pháp` | **readonly luôn** |
| 2 | **Mã GP** | Input mono | `nullable\|max:255` | `{project_code}_GP{lastId}` | **readonly luôn** |
| 3 | **PM làm giải pháp** * | Select `-- Chọn PM --` | `required` | Từ YC làm GP; Tự triển khai → user hiện tại | `disableGpInfo` hoặc Tự triển khai |
| 4 | **Tên GP** * | Input, `VD: GP dây chuyền sơn xưởng ô tô tiêu chuẩn` | `required\|max:255\|unique` | – | `disableGpInfo` |
| 5 | **Ngày cần xong GP** (kèm ` (V{n})`) * | DatePicker | `required\|date\|after_or_equal:today` → **`Phải lớn hơn hoặc bằng ngày hiện tại`** | Từ YC làm GP | `disableGpInfo` |
| 6 | **Ứng dụng** | Input `—` | UI đánh sao | Kế thừa từ dự án | **readonly luôn** |
| 7 | **Nhóm ngành** * (hint *Nếu không tìm thấy Nhóm ngành tương ứng hãy liên hệ với bộ phận Master Data để thêm mới*) | Select `Chọn nhóm ngành` | `required\|integer` | Từ YC làm GP | `disableGpInfo` |
| 8 | **Nhóm giải pháp** * | Select `Chọn nhóm giải pháp` | `required\|integer` | Từ YC làm GP | `disableGpInfo` |
| 9 | **Dự án có hạng mục** | Checkbox | `required\|boolean` | **`true`** | `status > 3 && status != 2`; ẩn với Tự triển khai |

**Card 3 – Bảng phân công nhân sự** (chỉ khi KHÔNG có hạng mục): nút **Thêm nhân sự**; cột **STT**, **Phòng ban** (`-- Chọn phòng ban --`), **Nhân sự** * (`-- Chọn nhân sự --`), **Vai trò dự án** * (`-- Chọn vai trò --`), **Mô tả công việc** (`VD: thiết kế layout, cấu hình hệ thống...`), **Ngày bắt đầu** * (mặc định hôm nay), **Thao tác** (`Xoá nhân sự`). Empty: `Chưa có nhân sự nào. Bấm Thêm nhân sự để phân công.`

### B.5 Tab "Quản lý hạng mục"
Header **Quản lý tạo hạng mục** + nút **Thêm hạng mục**. Empty: **Chưa có hạng mục nào** / `Bấm "Thêm hạng mục" để bắt đầu.`
| Trường | Control | Bắt buộc | Mặc định | Disabled |
|---|---|---|---|---|
| **Mã hạng mục** | Input mono | – | `{mã GP}_HM01, _HM02…` | readonly luôn |
| **Tên hạng mục** * | Select `-- Chọn tên hạng mục từ danh mục --` + nút **Tạo nhanh** (modal **Thêm hạng mục dự án**) | `required` | – | Leader không đổi được |
| **Leader hạng mục** * | Select `-- Chọn Leader --` | `required` | – | Leader không đổi được |
| **Ngày cần hoàn thành** * | DatePicker | `required\|date\|after_or_equal:today` → **`Phải lớn hơn hoặc bằng ngày hiện tại`** | – | theo `isModuleDisabled` |
| **Ghi chú** | Textarea `Ghi chú nội bộ cho hạng mục...` | nullable | – | theo `isModuleDisabled` |
| **Bảng phân công nhân sự** trong hạng mục | như Card 3 | member_id / project_role_id / start_date required | – | Loại Leader và người đã chọn |

### B.6 Versioning — CÓ, ở 2 cấp
```
Solution ──1..n──> SolutionVersion (current_version_id / current_version_code)
   └──1..n──> SolutionModule ──1..n──> SolutionModuleVersion (gắn solution_version_id)
```
| Thời điểm | Hành vi |
|---|---|
| Tạo giải pháp | Tự sinh version `code=1`, `start_date = hôm nay`, `end_date = internal_need_gp_date` |
| Tạo hạng mục | Tự sinh module version `code=1` |
| Sửa "Ngày cần xong GP" | Đồng bộ `end_date` xuống version hiện tại (**không** sinh version mới) |
| **Bấm "Tạo version"** | Sinh version mới `code = cũ + 1` |

**Nút "Tạo version"** (icon `ri-git-branch-line`) — topbar `/assign/solutions/{id}/manager`, hiện khi `status ∈ {11 Đã duyệt giải pháp, 13 Đã duyệt giá, 15 Chờ làm giá}`.
Modal **Tạo phiên bản mới**: **Mã phiên bản** (auto `V{current+1}`, disabled), **Mô tả** (`Mô tả phiên bản (tuỳ chọn)`), **Ngày kết thúc** (`required|date|after_or_equal:today` → **`Ngày kết thúc phải lớn hơn hoặc bằng ngày hiện tại`**). Nút **Tạo mới** / **Đóng**. `POST assign/solutions/{id}/create-new-version`. Toast **`Tạo phiên bản mới thành công`**; 423 → **`Bạn không có quyền tạo phiên bản mới cho giải pháp này!`**

Tạo version mới: snapshot nhân sự + tiến độ version cũ → reset `progress_percent=0` → **mọi hồ sơ trình duyệt `Đã duyệt` chuyển sang `Hết hiệu lực`** → tạo version mới → **đặt lại trạng thái GP về `7 – Đang triển khai`**.

### B.7 Điều kiện được sửa theo trạng thái
| Trạng thái GP | Ai được sửa |
|---|---|
| 1 – Nháp | Chỉ **người tạo** |
| 3 – Chờ PM duyệt | Chỉ **PM** |
| 5 – Chờ Leader duyệt | **PM** (thêm hạng mục) hoặc **Leader của hạng mục chưa duyệt** |
| 7 – Đang triển khai | Chỉ **PM** |
| 9 / 11 | Người thuộc phòng tiếp nhận YC **và** có quyền `Tiếp nhận yêu cầu làm giải pháp` |
| 2 Đóng / 13 / 15 / 17 | **Không ai** |

Sai → 403 **`Bạn không có quyền chỉnh sửa giải pháp này!`**. Xóa: chỉ status 1 + người tạo.
**Trường bị khóa**: `disableGpInfo` (`status >= 3 && status != 2`) khóa PM/Tên GP/Ngày cần xong GP/Nhóm ngành/Nhóm giải pháp. `status > 3` khóa checkbox hạng mục + bảng nhân sự. Ở `status = 5`, Leader không đổi được Tên hạng mục và Leader hạng mục.
**Validate nghiệp vụ**: chuyển 3 → 5 mà `has_modules=true` chưa có hạng mục → **`Vui lòng thêm ít nhất 1 hạng mục trước khi giao cho Leader`**. Một dự án chỉ 1 GP → **`Dự án này đã có giải pháp. Không thể tạo giải pháp khác.`**

## C. TẠO PHIẾU (HỒ SƠ) TRÌNH DUYỆT GIẢI PHÁP

### C.1 Nút ở đâu
| Mục | Giá trị |
|---|---|
| Màn | `/assign/solutions/{id}/manager` (**Quản lý giải pháp**) |
| Vị trí | Topbar phải, màu success, icon `ri-file-paper-2-line` |
| **Nhãn** | **`Tạo hồ sơ trình duyệt giải pháp`** — đổi thành **`Sửa hồ sơ trình duyệt giải pháp`** nếu hồ sơ mới nhất đang `draft` |
| Điều kiện hiện | `status === 7 (Đang triển khai)` **VÀ** người đăng nhập là **PM** của giải pháp |
| Xem lại hồ sơ | Tab **Hồ sơ** (`review-profiles`); nút dòng **Xem** / **Sửa** |
| Deep-link | `?open_review_profile=1` tự mở modal |

### C.2 Popup "Tạo hồ sơ trình duyệt"
Tiêu đề động: **`Tạo hồ sơ trình duyệt`** / **`Sửa hồ sơ trình duyệt`** / **`Xem hồ sơ trình duyệt`** / **`Duyệt hồ sơ trình duyệt`** + mã hồ sơ.

**Cột trái — "Hồ sơ và tài liệu đính kèm"**
| Nhãn | Control | Bắt buộc | Mặc định | Readonly |
|---|---|---|---|---|
| (Box đỏ) **Lý do từ chối** | text | – | khi hồ sơ `rejected` | chỉ xem |
| **Tên hồ sơ** * | V2BaseInput `Nhập tên hồ sơ` | `required\|string\|max:255` → **`Vui lòng nhập tên hồ sơ.`** | trống | mode xem/duyệt |
| **Nội dung trình duyệt** * | CompactReviewEditor (rich text, cao 180) | `required\|string` | trống | mode xem/duyệt |
| **Danh sách các file** * | FileAttachmentTable (**STT**, **Tên tài liệu** *, **Loại tài liệu** *, **Người thực hiện** *, **File đính kèm** *, **Dung lượng**, **Thao tác**) | mỗi dòng đều required | 1 dòng trống | mode xem/duyệt |
| **BOM tổng hợp gắn vào hồ sơ** | Hiển thị tự động | Không có BOM → cảnh báo đỏ **`Chưa có BOM tổng hợp ở trạng thái Hoàn thành cho version giải pháp này. Vui lòng lập BOM tổng hợp trước khi gửi hồ sơ.`** | Tự tìm BOM Tổng hợp `Hoàn thành` theo `solution_version_id` | chỉ xem, link mở tab mới |
| Bình luận | CommentThread | – | Chỉ khi hồ sơ đã lưu | – |

**Cột phải — "Thông tin tham chiếu"** (chỉ xem, trừ Hạn duyệt):
- **Thông tin giải pháp trình duyệt**: `Dự án`, `Giải pháp`, `Hạng mục`
- **Người phụ trách**: `PM phụ trách`
- **Thông tin thời gian**: `Ngày trình duyệt`, `Thời gian thực hiện`, **`Hạn duyệt`** * — V2BaseDatePicker `Chọn hạn duyệt`, `required|date|after_or_equal:today` → **`Hạn duyệt phải lớn hơn hoặc bằng ngày hôm nay.`** (dự án Tự triển khai: `nullable`, cả khối bị ẩn)
- **Người phê duyệt**: `Trưởng phòng duyệt` (ẩn với Tự triển khai)

**Nút footer**:
| Nhãn | Điều kiện | Hành động |
|---|---|---|
| **Lưu & Trình duyệt** (Tự triển khai: **Lưu & Duyệt**) | mode PM, chưa readonly | `status = pending` |
| **Lưu** | mode PM | `status = draft` |
| **Duyệt** | mode `dept_head` + hồ sơ `pending` | `action=approve` |
| **Từ chối** | như trên | modal `Xác nhận từ chối hồ sơ {mã}?` với ô **Lý do từ chối** (`Nhập lý do từ chối`) |
| **Đóng** | luôn | đóng modal |

API: `POST assign/solutions/{id}/manager/review-profiles`; quyết định: `.../review-profiles/{profileId}/decision`.
Toast: `Đã lưu và gửi trình duyệt hồ sơ giải pháp.` / `Đã lưu hồ sơ trình duyệt giải pháp.` / `Đã duyệt hồ sơ trình duyệt.` / `Đã không duyệt hồ sơ trình duyệt.`; 422 → `Vui lòng kiểm tra lại giữ liệu nhập`.
**Mã hồ sơ**: `HS.TD.{mã GP}.{số thứ tự}`.

### C.3 Ai duyệt
Không có bảng cấu hình cấp duyệt; người duyệt suy ra từ vai trò:
| Loại hồ sơ | Người tạo | Người duyệt |
|---|---|---|
| **Hồ sơ trình duyệt HẠNG MỤC** | Leader của hạng mục | **PM của giải pháp** |
| **Hồ sơ trình duyệt GIẢI PHÁP** | **PM của giải pháp** | **`solution.created_by`** — Trưởng phòng Giải pháp đã tiếp nhận/tạo giải pháp |
| **Dự án Tự triển khai** | KD tự làm | **Không có bước duyệt** — "Lưu & Duyệt" là auto-approve |
Không đúng người → 422 **`Bạn không có quyền duyệt hồ sơ trình duyệt này.`**

### C.4 Luồng duyệt / từ chối
| Hành động | Trạng thái hồ sơ | Trạng thái GP | BOM tổng hợp |
|---|---|---|---|
| Lưu nháp | `draft` – **Nháp** | giữ 7 | – |
| Lưu & Trình duyệt | `pending` – **Chờ duyệt** | 7 → **9 Chờ duyệt giải pháp** | → `pending` |
| Lưu & Duyệt (Tự triển khai) | `approved` – **Đã duyệt** | 7 → **11 Đã duyệt giải pháp** | → `approved` |
| **Duyệt** | `approved` (ghi `approved_at`) | 9 → **11** | → `approved` |
| **Từ chối** | `rejected` (ghi `reason_deny`) | 9 → **7 Đang triển khai** | → `rejected` |
| Tạo version mới | `approved` → `expired` – **Hết hiệu lực** | → 7 | – |
| Chốt giải pháp | → `finalized` – **Đã chốt** | → **17 Chốt giải pháp** | – |

**Chặn**: chỉ thao tác hồ sơ khi GP **Đang triển khai** → **`Chỉ được thao tác hồ sơ trình duyệt khi giải pháp đang ở trạng thái Đang triển khai.`**; chỉ duyệt hồ sơ `pending` → **`Chỉ được duyệt hồ sơ đang ở trạng thái chờ duyệt.`**; Tự triển khai gọi decision → **`Dự án tự triển khai không có bước duyệt hồ sơ riêng.`**

### C.5 Thông báo
| Thời điểm | Người nhận | Nội dung |
|---|---|---|
| PM gửi trình duyệt | `solution.created_by` (bỏ qua nếu Tự triển khai) | `Bạn có 1 hồ sơ trình duyệt giải pháp cần duyệt` / `Hồ sơ trình duyệt {mã HS} của giải pháp {mã GP} - {tên GP} đã được gửi trình duyệt` |
| Trưởng phòng duyệt | KD chính của dự án | `Có 1 hồ sơ trình duyệt giải pháp được duyệt` |
| Từ chối | Không gửi notify | – |

### C.6 Chốt giải pháp
Màn `/assign/prospective-projects/{id}/manager` → footer nút **`Chốt giải pháp`**, hiện khi: dự án chưa đóng + có hồ sơ `Đã duyệt`/`Hết hiệu lực` + user là **KD chính**.
Modal **`Chốt giải pháp`**: bảng chọn hồ sơ (**Mã hồ sơ**, **Version GP**, **Trạng thái**, **Ngày duyệt**, radio) — nhãn **`Chọn hồ sơ giải pháp`** *; ô **`Ghi chú chốt giải pháp`** (`Nhập ghi chú (tối đa 1000 ký tự)`). Nút **`Lưu & gửi thông báo`** / **`Đóng`**. Empty: `Không có hồ sơ nào ở trạng thái Đã duyệt / Hết hiệu lực.`
Kết quả: hồ sơ → **Đã chốt**, GP → **17 Chốt giải pháp**, YC làm GP → **8 Đã hoàn thành**, dự án → **Thương thảo dự án/hợp đồng**.

## D. LẬP HỢP ĐỒNG ERP TỪ BÁO GIÁ TRÚNG THẦU

> Nút trong HRM **không mở popup** — là **link mở tab mới sang ERP**. Form nhập liệu nằm bên ERP. ERP gọi ngược HRM bằng **HTTP API (Guzzle)**.

### D.1 Nút nằm ở đâu
| Mục | Giá trị |
|---|---|
| Màn | Chi tiết **Dự án tiềm năng** → tab **Báo giá** |
| Banner | `Lập hợp đồng ERP từ báo giá {mã báo giá}` |
| **Nhãn nút** | **`Lập hợp đồng ERP`** (icon `ri-external-link-line`), thẻ `<a target="_blank">` |
| Điều kiện | `contract.can_create_contract === true` |

**Điều kiện `can_create_contract`** — phải thỏa **cả 6**:
1. Dự án có báo giá **Trúng thầu** (status=7)
2. Mọi dòng hàng đã có `erp_product_id` (đã đồng bộ hết hàng tạm)
3. Báo giá tiền **VND**
4. Chưa lập hợp đồng lần nào
5. Người đăng nhập là **người LẬP báo giá**
6. Báo giá không có dòng hàng cấp cha-con

**Badge trạng thái banner**: `Đã lập hợp đồng ERP` / `Báo giá ngoại tệ — chưa hỗ trợ` / `Báo giá có cấp con — chưa hỗ trợ lập HĐ` / `Chờ đồng bộ hết hàng sang ERP` / `Sẵn sàng lập hợp đồng` / `Đã đồng bộ — chỉ người lập báo giá mới lập được HĐ`.

**Bước tiền đề** (banner phía trên): `Báo giá trúng thầu {mã} — Đồng bộ hàng tạm sang ERP` với nút **`Gửi duyệt hàng tạm`** và **`Cập nhật kết quả duyệt`**; badge `Chưa đồng bộ` / `Đang đồng bộ sang ERP` / `Đã đồng bộ`; text `X hàng tạm chờ gửi` | `X/Y hàng tạm đã duyệt` | `Y/Y hàng tạm đã tạo trên ERP`.

### D.2 Bấm vào mở ra gì
Tab mới: `{ERP_URL}/admin/sale/firm-contracts/create?hrm_quotation_id={id}&contract_type=4` → màn ERP **`Lập Hợp đồng Dự án`**. Form tự nạp báo giá HRM → toast `Thêm báo giá HRM thành công`, prefill KH + hàng hoá (mỗi **Nhóm báo giá HRM → 1 tab hợp đồng ERP**).

**Trường phải nhập thêm trên ERP**:
| Nhãn | Control | Bắt buộc / message | Mặc định |
|---|---|---|---|
| **Báo giá** | Hiển thị `[HRM] {mã báo giá}` | – | Prefill |
| **Khách hàng** | Text | `customer_id` required | Resolve theo `customer_code` → fallback `tax_code` |
| **Số hợp đồng** * | Input | `Bắt buộc phải nhập.` / `Số hợp đồng chỉ được chứa chữ cái, số, dấu gạch ngang và dấu gạch dưới (không được chứa tiếng Việt có dấu).` / `Số hợp đồng đã tồn tại.` | **trống — user tự nhập** |
| **Diễn giải** | Textarea | – | trống |
| **Địa chỉ / Điện thoại / Fax** | Input | – | Từ KH ERP |
| **Bảng giá** | Select | – | **1 = Bán lẻ** |
| **CMND/MST** * | Input | `required\|regex` (≥9 chữ số) | KH DN → `tax_code`; cá nhân → CMND |
| **Ngày cấp / Nơi cấp** | Datepicker / Input | nullable | Từ KH |
| **Người đại diện** * / **Chức vụ** * | Select | required | Người đại diện đầu tiên |
| **Thời gian bảo hành** | Input | – | trống |
| **Cần lắp đặt** * / **Xuất hóa đơn** * | Radio Có/Không | `required\|in:0,1` | – |
| **Địa chỉ giao hàng** | Input | nullable | = địa chỉ KH |
| **Hãng** | Select | `Chỉ được chọn 1 hãng cho 1 hợp đồng` | Hãng đầu của KH |
| **Phòng QTC / Nhân viên QTC** | Select | Tổng % hưởng = 100 → `Tổng % hưởng phải đủ 100%` | Phòng chính + hỗ trợ |
| **File đính kèm:** | Upload | `Bắt buộc phải đính kèm.` / `File đính kèm phải là file PDF, PNG, JPG, DOCX, DOC, XLS, XLSX, JPEG.` / `File đính kèm không được quá 13 MB.` | nút `Chọn file` |
| Tab **Mẫu in**: `Loại hợp đồng` *, `Mẫu in` * | Select | required | – |
| Tab **Thanh toán** | Bảng | `Tổng số tiền thanh toán phải bằng tổng số tiền.` / `Khi thanh toán đủ 100% thì bắt buộc phải có ít nhất một lần thanh toán có loại là "Thanh toán".` | – |
| **Tài khoản (*)** công ty | Select | required | – |
| **Ký duyệt** * / **Chức vụ** * | Select nhân viên | required | – |

Tab hàng hoá: `Danh sách hàng hóa`, `Khuyến mãi`, `Tổng hợp theo VAT`, `Dịch vụ đi kèm`, `Chi phí khác`, `Thanh toán`, `Mẫu in`, `Nhân sự triển khai`, `Xuất hàng`, `Phụ lục`.
Nút cuối: **`Lưu`** (nháp) / **`Lưu & gửi duyệt`** / **`Hủy`**.

### D.3 Cách đẩy sang ERP
```
HRM: nút <a> → ERP form
ERP → HRM (Guzzle, timeout 15s):
   GET  /api/v1/assign/quotations/erp-contract/{id}?employee_info_id=...
   POST /api/v1/assign/quotations/erp-contract/{id}/mark
ERP ghi DB ERP: firm_contracts (+ cột hrm_quotation_id)
HRM ghi: quotations.erp_firm_contract_id, erp_firm_contract_code
```
Nhóm route `erp-contract` **nằm ngoài `auth:api`** — không auth, không checkPermission (có TODO trong code).

### D.4 Kết quả & kiểm tra
- Lưu thành công trên ERP → toast **`Thao tác thành công`** → về danh sách Hợp đồng Dự án ERP. Nếu `Lưu & gửi duyệt` → notify `Bạn có một Hợp đồng Dự án cần duyệt từ {tên người lập}`.
- Mã HĐ: `HĐDA_{mã công ty}_{mã phòng}_{yy}_{4 số}_{Số hợp đồng nhập tay}`.
- **Quay lại HRM và F5 tab Báo giá** → badge **`Đã lập hợp đồng ERP`**, hiện **`Mã hợp đồng ERP:`** (link mở HĐ bên ERP), **`Trạng thái đồng bộ:`**, **`Thời gian đồng bộ:`**; nút `Lập hợp đồng ERP` biến mất.
- ⚠️ Nếu bước ghi ngược `mark` lỗi thì HRM chỉ ghi log — HĐ bên ERP vẫn tồn tại nhưng HRM không hiện mã và nút vẫn còn. **Cảnh báo người dùng không bấm lập lần 2.**
- ⚠️ Route ERP `firm-contracts/create` có middleware **`checkDueConfigs`** — user còn hàng mượn/pre-pick **quá hạn** sẽ không vào được màn Lập hợp đồng.

### D.5 Lỗi chặn
| Tình huống | Message |
|---|---|
| Báo giá không đủ điều kiện | `Báo giá không đủ điều kiện lập hợp đồng: phải là báo giá của bạn, trúng thầu, chưa lập HĐ, đã đồng bộ hết hàng sang ERP, tiền VND và không có hàng hóa cấp cha-con.` |
| ERP nạp báo giá thất bại | `Báo giá HRM không đủ điều kiện lập hợp đồng (...)` |
| Không tìm được KH ERP | `Không tìm thấy khách hàng ERP tương ứng (mã KH: {code}, MST: {tax_code}).` |
| Gửi duyệt hàng tạm khi chưa trúng thầu | `Chỉ gửi duyệt hàng tạm cho báo giá Trúng thầu.` |
| Gửi duyệt hàng tạm 2 lần | `Báo giá đã gửi duyệt hàng tạm rồi.` |
| Không phải Sale phụ trách (403) | `Bạn không phải Sale phụ trách dự án này` |

## E. TRẠNG THÁI GIẢI PHÁP
| # | Nhãn | Chuyển bởi |
|---|---|---|
| **1** | **Nháp** | **Mặc định khi tạo** — `Lưu nháp` |
| 3 | **Chờ PM duyệt** | `Lưu và gửi` |
| 5 | **Chờ Leader duyệt** | PM bấm `Giao cho Leader` (khi có hạng mục) |
| 7 | **Đang triển khai** | Tất cả Leader bấm `Lưu và duyệt`; hoặc PM `Lưu và duyệt` khi không có hạng mục; hoặc hồ sơ bị **Từ chối**; hoặc **Tạo version** mới |
| 9 | **Chờ duyệt giải pháp** | PM bấm `Lưu & Trình duyệt` |
| 11 | **Đã duyệt giải pháp** | Trưởng phòng GP bấm `Duyệt`; hoặc Tự triển khai `Lưu & Duyệt` |
| 15 | **Chờ làm giá** | Tạo/duyệt yêu cầu xây dựng giá |
| 13 | **Đã duyệt giá** | Duyệt giá báo giá |
| 17 | **Chốt giải pháp** | Nút `Chốt giải pháp` ở màn dự án |
| **2** | **Đóng** | `PUT /assign/solutions/{id}/close` (quyền `Quản lý giải pháp`) — **chưa thấy nút gọi API này trên FE** |

**Trạng thái hồ sơ trình duyệt**: `draft` Nháp / `pending` Chờ duyệt / `approved` Đã duyệt / `rejected` Không duyệt / `expired` Hết hiệu lực / `finalized` Đã chốt.
**Trạng thái hạng mục**: 1 Chưa duyệt / 2 Đang triển khai / 6 Chờ duyệt hồ sơ trình duyệt / 8 Đã duyệt hồ sơ trình duyệt / 10 Đóng.

## F. QUYỀN
| ID | Tên quyền nguyên văn |
|---|---|
| 1007–1010 | **Xem danh sách yêu cầu làm giải pháp theo tổng công ty / công ty / phòng ban / bộ phận** |
| **1012** | **Tiếp nhận yêu cầu làm giải pháp** |
| 1016–1019 | **Xem danh sách làm giải pháp theo tổng công ty / công ty / phòng ban / bộ phận** |
| **1044** | **Quản lý giải pháp** |
| 984 / 999 | **Quản lý / Xem danh mục nhóm giải pháp** |
| 986 / 1001 | **Quản lý / Xem danh mục hạng mục dự án** |

**checkPermission trên route:**
| Route | Middleware |
|---|---|
| `PUT /assign/request-solutions/{id}/receive` | `checkPermission:Tiếp nhận yêu cầu làm giải pháp` |
| `PUT /assign/solutions/{solution}/close` | `checkPermission:Quản lý giải pháp` |
| `assign/industries/*` | `checkPermission:Quản lý danh mục nhóm giải pháp` (+ `\|Xem…` cho GET) |
| `assign/project-items/*` | `checkPermission:Quản lý danh mục hạng mục dự án` (+ `\|Xem…`) |

**Các route CRUD `request-solutions` và `solutions` KHÔNG có checkPermission** — phân quyền bằng logic nghiệp vụ trong Entity (`canEdit()`, `canDelete()`, `isCanReceive()`, so khớp `pm_id`/`created_by`/`leader_id`).

**Phân quyền theo cấp:**
- **YCGP**: `checkPermissionListWithColumn(..., 'receive_id')` — "của mình" = **người tiếp nhận**, KHÔNG phải người tạo → người tạo YCGP mà không có quyền cấp nào sẽ **không thấy chính YC mình tạo**.
- **Giải pháp**: `checkPermissionList` trên `solutions` rồi **mở rộng OR**: vẫn thấy GP nếu mình là `pm_id`, leader hạng mục, thành viên GP, hoặc thành viên hạng mục — kể cả ở phòng khác.
- **Màn "YC chờ tiếp nhận"**: không có quyền `Tiếp nhận yêu cầu làm giải pháp` → trả mảng rỗng. Có quyền thì lọc theo `implementation_type`: type=2 lấy `receive_dept` = phòng của user; type=3 lấy `receive_dept ∈ departmentsManager()`.

## G. Ghi chú bổ sung
- **3 nhánh `implementation_type`** chi phối toàn bộ luồng: `1 Tự triển khai` (không tạo YC làm GP, GP auto-duyệt, không có bước TP duyệt), `2 Theo phòng` (khoá Phòng tiếp nhận), `3 Liên phòng ban` (luồng đầy đủ).
- **`/assign/solution-groups` thực chất là danh mục `industries`** — tiêu đề `Quản lý nhóm giải pháp`; cột STT, Mã–Tên nhóm giải pháp, Nhóm ngành, Số ứng dụng, Mô tả, Cập nhật, Trạng thái.
- **`/assign/solution-modules`** là danh sách tất cả hạng mục (góc nhìn Leader): STT, Hạng mục, Dự án, Leader, Hạn hoàn thành, Phiên bản, Trạng thái, Ngày tạo; nút **Chỉnh sửa** / **Lưu và duyệt** (khi `is_can_approve`) và **Quản lý**.
