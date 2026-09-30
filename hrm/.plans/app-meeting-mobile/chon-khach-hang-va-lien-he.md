# Chọn khách hàng & người liên hệ trên app mobile — thiết kế v10

**Ngày:** 15/09/2026
**File thiết kế:** `~/Documents/demo giao dien/pencil_design/meeting-mobile.pen` (50 artboard)
**Bản giao:** CHƯA xuất lại sau vòng sửa 15/09 (bản v10 cũ trong `exports/` đã lạc hậu — chỉ xuất khi user yêu cầu)
**Trạng thái:** thiết kế đã chốt, CHƯA code

---

## 1. Ba yêu cầu đã xử lý

| # | Yêu cầu của user | Đã làm |
|---|---|---|
| 1 | Select chọn khách hàng cần có UI/UX rõ khi chọn | Thêm màn **41 · Chọn khách hàng** (đẩy toàn màn) + **41b · Không tìm thấy** |
| 2 | Bổ sung nút thêm nhanh khách hàng → người liên hệ | Thêm màn **42 · Thêm nhanh khách hàng** và sheet **44 · Thêm nhanh người liên hệ**; chip `Thêm nhanh` gắn cạnh nhãn Người liên hệ ở W03/W05/W28 |
| 3 | Bỏ toàn bộ field trạng thái meeting | Xoá `f-trangthai` ở **W05 / W25 / W28**, xoá dòng `Trạng thái` ở **W33**. Trạng thái CHỈ còn badge cạnh mã meeting trên Hero của Hub — **không** thêm dải trạng thái ở màn con (user chốt 15/09) |

## 2. Quyết định đã chốt

- **Thêm nhanh khách hàng trên app = bản RÚT GỌN**, chỉ trường bắt buộc: Tên KH, Loại hình tổ chức, Tên đơn vị, SĐT, Quốc gia / Tỉnh-TP / Quận-Huyện / Phường-Xã, Địa chỉ xuất hoá đơn (mặc định tick "Giống địa chỉ ở trên"), + 1 người liên hệ (Họ tên, Chức vụ, SĐT). Các trường còn lại bổ sung sau trên web. Web hiện nhúng **nguyên** `CustomerForm.vue` vào modal — app KHÔNG bê nguyên.
- **Chọn người liên hệ = bottom sheet**, không đẩy màn riêng (danh sách thường 3–8 người). Chọn khách hàng thì ngược lại: **đẩy toàn màn** vì phải lọc + đọc nhiều dòng.
- Chưa chọn khách hàng thì ô **Người liên hệ khoá** (nền `#F1F3F5`) + dòng ghi chú xám; chip `Thêm nhanh` liên hệ cũng ẩn.
- Khối **tóm tắt KH đã chọn** (Mã KH · MST · SĐT · Địa chỉ) hiện ngay dưới ô Khách hàng — bám `readonly-customer-info` của web.
- Nút `Lịch sử meeting` chỉ hiện **khi đã chọn khách hàng** (giống web: `hasCustomer && form.customer_id`), nên W25 (chưa chọn KH) chỉ còn chip `Thêm nhanh KH`.
- **KHÔNG đưa logic "đã có người đăng ký" vào thiết kế app** (user chốt 15/09). Bản web có cờ `register_locked` / `locked` nhưng chưa có yêu cầu nghiệp vụ cho app — không suy diễn, khi nào khách yêu cầu thì bổ sung.

## 3. API cần cho nhóm màn này

| Màn | Endpoint web đang dùng | Ghi chú cho app |
|---|---|---|
| 41 · Chọn khách hàng | `GET assign/customers?page&per_page&filter&tax_code&mobile` | App cần **phân trang cuộn**, trả kèm `customer_type_text`, `province_name`, `address` dựng sẵn |
| 41 · quyền tạo KH | `GET assign/customers/my-permissions` → `create` | Ẩn nút `Thêm nhanh KH` khi `create = false` (**fail-closed**, không mặc định `true`) |
| 42 · Thêm nhanh KH | `POST assign/customers` (form đầy đủ) | BE phải chấp nhận payload rút gọn, hoặc bổ sung `?mode=quick`. Lưu xong app tự tìm lại theo `code` rồi đổ vào form meeting (đúng luồng `handleCustomerCreated`) |
| 43 · Chọn liên hệ | `GET assign/customers/{id}/contacts[?phone=]` | Chỉ cần danh sách liên hệ; app KHÔNG dùng `locked` / `locked_message` |
| 44 · Thêm nhanh liên hệ | (web toggle inline, gửi kèm form meeting) | App nên có endpoint riêng tạo contact rồi trả về id — nếu không thì giữ trong state tới lúc lưu meeting |

## 4. Cần hỏi lại khách trước khi code

- Quy tắc `Địa chỉ xuất hoá đơn` bắt buộc: bản rút gọn đang mặc định copy địa chỉ chính. Xác nhận nghiệp vụ chấp nhận.
- Người liên hệ tạo từ app có tự thêm vào **Thành phần tham dự phía khách hàng** như web không (thiết kế đang ghi là CÓ).

## 5. Vòng sửa 15/09 (sau nghiệm thu lần 1)

1. **Bỏ logic "KH / liên hệ đã có người đăng ký"** khỏi màn 41 và sheet 43 — gỡ luôn node `ccLock` trong component `C/CustomerCard`.
2. **Thành phần meeting đổi nhãn `Nội bộ` → `Công ty`** cho đồng nhất trên MỌI màn: tab màn 07/35, nút `Thêm thành viên công ty`, màn 17, chip lọc + badge của 08/30/31/32, dòng tóm tắt Hub (`8 công ty · 4 khách hàng`), dòng `Công ty: 8 người (có mặt 7…)` ở bản in 15.
   ⚠️ **Giữ nguyên `Họp nội bộ`** ở trường *Phân loại họp* (`is_customer_meeting`) và ở màn 31 — đó là loại cuộc họp, không phải nhóm thành phần.
3. **Thêm màn 45 · Cảnh báo chưa lưu khi Quay lại** — 3 nút: `Lưu và quay lại` (primary) / `Quay lại, không lưu` / `Ở lại màn này`. Áp cho MỌI màn form khi còn thay đổi chưa lưu; không có thay đổi thì thoát thẳng, không hỏi. Tương đương `unsavedChangesMixin` của web nhưng bổ sung lối "lưu luôn".
4. **Xếp lại bản đồ**: tối đa **4 màn/hàng**, xuống dòng trong từng bước. Khung từ 5685 × 10477 còn **2825 × 22871** — ảnh toàn cảnh mở vừa cửa sổ vẫn đọc được chữ. 5 màn 41–44 trước đó nằm NGOÀI khung, nay đã đưa vào.

## 6. Hub — đánh dấu khối bắt buộc (15/09, vòng 3)

User phản hồi *"chưa thấy thiết kế bắt buộc cho cái hub"*. Rà lại thì Hub thiếu 2 thứ:
khối `Mức độ hoàn thiện hồ sơ` **chỉ tồn tại trong bản Hub nền của popup 16**, 6 màn Hub chính
(04a/04b/04c/24/26/27) và bản nền của popup 22/23 đều KHÔNG có; và 8/9 dòng không có dấu hiệu bắt buộc nào.

### Khối nào bắt buộc — tra từ code, KHÔNG suy diễn

| Khối | Bắt buộc | Căn cứ |
|---|---|---|
| Thông tin chung | luôn luôn | `MeetingUpdateApiRequest`: `name`, `meeting_type_id`, `start_date`, `end_date`, `host_employee_id` = `required`; `location` = `required_if:mode_id,1` |
| Thành phần tham dự | luôn luôn | `'company_members' => 'required|array'` |
| Điểm danh | khi Hoàn thành | `MeetingForm.vue` guard `isAllAttended()` |
| Biên bản cuộc họp | khi Hoàn thành | guard `hasMeetingReport()` |
| Kết luận cuộc họp | khi Hoàn thành | `'conclusion' => 'required_if:status,3'` |
| Khảo sát nhu cầu KH | khi Hoàn thành, **chỉ** loại `CODE_PRODUCT_INTRO` | `has_investment_demand` / `has_maintenance_demand` = `required_if:status,3` trong nhánh `$needSurvey` |
| Dự án tiền khả thi · Tài liệu chuẩn bị · Tài liệu biên bản | không | `nullable` |

### Đã làm

- Dấu `*` đỏ sau nhãn của **5 khối bắt buộc** trên **cả 9 Hub** (6 màn chính + 3 bản nền popup) — 45 dòng.
  Ví dụ đang vẽ là loại *Đấu thầu* nên Khảo sát KHÔNG bắt buộc → mẫu số là **/5**; loại có Khảo sát thì **/6**.
- Khối `Mức độ hoàn thiện hồ sơ` bổ sung vào 6 Hub chính + 2 bản nền còn thiếu, **đếm theo khối bắt buộc** (user chốt),
  kèm dòng chú thích `* Khối bắt buộc để Hoàn thành meeting…`. Giá trị: 04a 1/5 · 04b 2/5 · 04c 5/5 · 24 0/5 (đỏ) · 26 2/5 (xám, đã huỷ) · 27 2/5.
- Dòng phụ `Bắt buộc khi hoàn thành` của khối Kết luận đổi thành `Chưa nhập kết luận` (không còn trùng thông tin với dấu `*`).
- **Màn mới 46 · Hub — chặn Hoàn thành**: banner đỏ liệt kê đúng khối còn thiếu, 3 khối đó tô nền đỏ nhạt + cột phải `Thiếu` đỏ, thanh tiến độ đỏ. Web hiện chỉ bắn toast rồi nhảy tab.

### CHƯA làm — khoảng trống đã biết

Khối **“Phiếu tổng hợp kết quả meeting”** (Redmine #11130, guard `missingRequiredResultAnswers` chặn Hoàn thành
khi thiếu câu bắt buộc, chỉ áp cho Loại meeting có gán phiếu) **chưa có trong thiết kế app** — cả ở Hub lẫn màn nhập.
User chốt 15/09 để lại, làm sau khi chốt với khách.

## 7. Thêm nhanh dự án TKT (15/09, vòng 4)

Khảo sát web: ô *Dự án TKT* ở Thông tin chung có chú thích **"Chọn dự án từ danh sách hoặc tạo mới tại mục
Dự án tiền khả thi."** — tức web có **2 đường**. Bản app mới vẽ đường "chọn" (màn 06), thiếu đường "tạo mới".
Trên web, `MeetingProject.vue` nút `Thêm dự án` dựng inline 2 khối dùng chung với form Dự án TKT thật:
`CustomerInfoSection` + `ProjectInfoSection`.

### Trường của dự án gắn vào meeting — `MeetingUpdateApiRequest`, mảng `projects.*`

| Trường | Key | BE | FE |
|---|---|---|---|
| Tên dự án TKT | `name` | `required\|max:255` | `*` |
| Ứng dụng | `application_id` | `required` | `*` |
| Quy mô dự án | `project_scale_id` | `required` | `*` |
| Phân loại đầu tư | `investment_type_id` | `required` | `*` |
| Loại hình hoạt động KH | `customer_scope_group_id` | `required_unless:…is_intermediary_customer,1` | `*` |
| Lĩnh vực kinh doanh KH | `customer_scope_id` | `required_unless:…` | `*` |
| Nhóm ngành | `scope_id` | **nullable** | `*` |
| Cách triển khai dự án | `implementation_type` | **không có rule** | `*` |
| Địa điểm triển khai | `project_address` | **không có rule** | `*` |
| Mô tả chi tiết | `project_description` | — | không |
| Email KH · Ứng dụng KH · Giai đoạn | `customer_email` · `customer_application_id` · `project_phase_id` | nullable | không |

Tick **KH thương mại dịch vụ** (`is_intermediary_customer`) đẩy 2 ô Loại hình/Lĩnh vực sang khối
*KH thụ hưởng cuối* (`customer_benefit_scope_group_id` / `customer_benefit_scope_id` thành `required_if`).

### Đã làm

- **Màn mới 47 · Thêm nhanh dự án TKT** — đủ 9 ô `*` (giữ dấu `*` theo FE web, user chốt 15/09), 1 ô Mô tả không bắt buộc,
  ô **Khách hàng KHOÁ** hiển thị KH của meeting (web truyền `lock-direct-customer="true"` trong ngữ cảnh meeting),
  checkbox *KH thương mại dịch vụ* kèm ghi chú, ghi chú *Phiếu thu thập thông tin chỉ nhập được sau khi lưu dự án*.
  Nút đáy `Huỷ` / `Lưu & gắn vào meeting`.
- **Màn 06** thêm nút `Thêm nhanh dự án TKT` + dòng *"Chọn dự án có sẵn của khách hàng này, hoặc tạo nhanh dự án mới."*
- Xếp lại Bước 3 để 06 → 47 → 07 nằm liền nhau; bản đồ 50 artboard, khung **2825 × 23105**.

### ⚠️ Việc BE cần làm

`projects.*.scope_id` (Nhóm ngành), `implementation_type` (Cách triển khai), `project_address` (Địa điểm triển khai)
đang **nullable / không có rule** trong khi FE bắt buộc → lưu thiếu mà không báo lỗi. Cùng loại lỗi Redmine #10874
đã vá cho `name` / `application_id`. Cần bổ sung rule trước khi app dùng chung endpoint này.

## 8. Mã công ty trên dòng nhân sự (15/09, vòng 5)

Nhân sự trong hệ thống trải nhiều pháp nhân (`companies.code`: **TPE · ETEK · ETEK POWER · ETEK GREEN · TSLC** —
theo `AddDataInRiceCompaniesSeeder`), nhưng dòng nhân sự trên app chỉ hiện *Tên + Chức vụ* nên không biết người đó
thuộc công ty nào.

**Đã thêm chip mã công ty** (nền `#EEF2F6`, chữ 10px/700 `#64748B`) đứng trước chức vụ ở 4 màn phía công ty:

| Màn | Số dòng |
|---|---|
| 07 · Thành phần tham dự — tab Công ty | 5 |
| 14 · Chọn nhân sự | 7 |
| 17 · Thêm thành viên công ty | 7 |
| 35 · Thành phần tham dự — xem | 5 |

⚠️ **Nhãn chuẩn của select nhân viên KHÔNG đổi.** `utils/employeeOptionText.js` vẫn là
`Tên nhân viên - Mã phòng - Mã nhân viên` (chốt 2026-09-11) — chip mã công ty chỉ là cách trình bày của
**dòng danh sách trên app**, không phải nhãn option select. Đừng nhầm hai thứ.

⚠️ **BE cần trả thêm `company_code`** cho API danh sách nhân viên mà app dùng (hiện `Employee::getAll` /
`user-profile` chỉ có `department_code`, `employee_code`). Các báo cáo đã lấy sẵn bằng `c.code as company_code` —
dùng lại đúng cách đó.

**Chưa áp cho**: 4 màn Điểm danh (08 · 30 · 31 · 32) và bản in Biên bản (15) — cũng liệt kê người phía công ty.
Chờ user quyết có mở rộng không.

## 9. Màn 18 — bỏ nút Thêm ở khối người liên hệ (15/09, vòng 6)

Khối vàng đầu màn 18 trước đây có nút **Thêm** để đẩy người liên hệ vào danh sách — **sai**, vì người liên hệ
**đã luôn nằm sẵn** trong `customer_members` (web: `onContactChange` "Thay thế hoặc thêm người liên hệ vào danh sách
thành viên khách hàng"), và việc thêm/đổi người liên hệ thuộc về màn **Thông tin chung** (sheet 43/44), không phải màn này.

Đã sửa:
- Xoá nút `Thêm` khỏi khối vàng.
- Khối vàng đổi thành thuần thông tin: nhãn `Người liên hệ của khách hàng` + dòng nhắc
  *"Đã nằm sẵn ở NGƯỜI 1 bên dưới. Đổi hoặc thêm người liên hệ làm ở màn Thông tin chung, không làm ở đây."*
- Gắn badge cam **Người liên hệ** vào dòng `NGƯỜI 1` để thấy ngay đó là người liên hệ mặc định.
- Nút `Thêm người` ở cuối danh sách **giữ nguyên** — đó là thêm thành phần khách hàng nhập tay
  (`customer_members` với Họ tên · Chức vụ · SĐT), khác việc thêm người liên hệ.

**Còn để ngỏ:** dòng NGƯỜI 1 vẫn có icon thùng rác như các dòng khác (đúng như web — `customer_members.splice`).
Nếu nghiệp vụ muốn khoá không cho xoá người liên hệ ở màn này thì cần chốt rồi sửa cả web lẫn app.

## 10. Gỡ chú thích logic khỏi màn (15/09, vòng 7)

User: *"Bỏ thông tin note logic đi"*. Đã xoá **19 dòng chú thích** nằm BÊN TRONG khung điện thoại —
chúng là ghi chú của người thiết kế, không phải microcopy thật của app:

- 9× dòng chú giải dấu `*` dưới thanh Mức độ hoàn thiện hồ sơ (9 Hub)
- "Chọn khách hàng trước rồi mới chọn được người liên hệ." (03, 25)
- "Chọn dự án có sẵn của khách hàng này, hoặc tạo nhanh dự án mới." (06)
- "Đã nằm sẵn ở NGƯỜI 1 bên dưới…" (18)
- "Các thông tin còn lại… bổ sung sau trên bản web." (42)
- "Liên hệ mới thuộc khách hàng…" (44)
- 3 dòng ở 47 (khách hàng khoá · tick KH thương mại dịch vụ · phiếu thu thập thông tin)

Nội dung cần giữ đã dồn lên **caption của từng artboard** (03, 04a, 42, 47) — caption nằm ngoài khung máy,
đúng chỗ cho phần giải thích nghiệp vụ.

Giữ lại `Đi công tác Đà Nẵng` ở màn 32 — đó là **dữ liệu thật** (lý do vắng mặt), không phải chú thích.

**Quy tắc từ nay:** không viết giải thích luồng/điều kiện vào bên trong màn. Trạng thái khoá tự nói bằng
ô xám + icon khoá; điều kiện nghiệp vụ nằm ở caption artboard và tài liệu này.

## 11. Nút Xem trên danh sách file (15/09, vòng 8)

Thêm nút **Xem** (icon `eye`) vào **10 dòng file** ở 4 màn tài liệu:

| Màn | Số dòng | Hành động trên dòng |
|---|---|---|
| 11 · Tài liệu đính kèm (biên bản) | 3 | Xem · Tải xuống · Xoá |
| 19 · Tài liệu chuẩn bị | 2 | Xem · Tải xuống · Xoá |
| 36 · Tài liệu chuẩn bị — xem | 2 | Xem · Tải xuống |
| 38 · Tài liệu biên bản — xem | 3 | Xem · Tải xuống |

Dùng **icon-only** cho đồng bộ với 2 hành động sẵn có trên dòng (`download`, `trash-2`) — dòng file rộng 361px,
sau khi thêm icon thứ 3 phần tên file còn 203px, vừa khít mép phải (đo DOM: icon cuối kết thúc ở 347 = mép trong 347).
Đặt chữ "Xem" thì phải xuống dòng, hỏng khuôn.

⚠️ **Web chưa có chức năng này.** Khuôn `V2BaseFile` của hrm-client hiện chỉ có `Tải xuống / Thay đổi / Xóa`
(xem CLAUDE.md mục file đính kèm). Muốn app xem trước file thì cần:
- BE trả URL xem trực tiếp (hoặc endpoint stream) cho file — hiện luồng tải dùng `?token=` + `Content-Disposition`
  (xem [[hrm-export-download-safari-bug]]), tức luôn ép tải về chứ không xem inline.
- Chốt loại file nào xem được trong app (PDF/ảnh xem được; Office thì phải mở app ngoài hoặc convert).

## 12. Quy ước THÔNG BÁO — đồng nhất (15/09, vòng 9)

User phát hiện có màn đẩy nội dung xuống, có màn đè popup lên. Rà ra **2 tầng lệch**:

1. Cùng việc "chặn Hoàn thành" mà 2 kiểu: W24 / W46 dùng **dải trong luồng**, còn W29 / W30 dùng **Toast đỏ đè**
   (`layoutPosition: absolute`, x16 y122).
2. Cùng loại dải mà **4 bảng màu**: đỏ `#FEE2E2` · xám `#F1F5F9` · **xanh lá** `#E8F5E9` (9 màn khoá) ·
   xanh dương `#E3F2FD` · vàng `#FFF8E1`.

### Quy ước đã chốt (user chọn cả 2 phương án khuyến nghị)

**Không dùng toast nổi.** Mọi thông báo là dải/thẻ nằm trong luồng, đúng 3 loại:

| Loại | Nền | Viền | Icon | Chữ | Vị trí | Dùng ở |
|---|---|---|---|---|---|---|
| Lỗi / chặn / đã huỷ | `#FEE2E2` | `#DC262633` | `triangle-alert` `#DC2626` | `#991B1B` | dải full-width dưới Header | 24 · 25 · 26 · 29 · 30 · 46 |
| Đã khoá / chỉ xem | `#F1F5F9` | `#64748B33` | `lock` `#64748B` | `#475569` | dải full-width dưới Header | 27 · 32–40 |
| Thông tin / hướng dẫn | `#E3F2FD` | `#2563EB40` | `info` `#2563EB` | `#1E40AF` | thẻ bo góc 10 trong Body | 13 · 18 · 19 · 31 |

**Lý do bỏ toast**: lỗi chặn Hoàn thành là lỗi **cần hành động** — toast tự tắt sau vài giây, người dùng
đọc không kịp và mất luôn dấu vết phải sửa gì.

**Lý do bỏ xanh lá ở 9 màn khoá**: trong bảng màu trạng thái của hệ thống, xanh lá = hoàn thành/đủ.
Dùng nó cho dải "đã khoá, không sửa được" là ngược nghĩa.

### KHÔNG đụng tới — hộp thoại vẫn là popup

W16 (huỷ meeting) · W22 (menu ⋮) · W23 (đổi giờ) · W43 / W44 (chọn & thêm liên hệ) · W45 (chưa lưu).
Đây là **hộp thoại bắt ra quyết định**, không phải thông báo — popup là đúng.

Quy ước này đã ghi thành 1 dòng legend ngay trên trang **00 · Tổng quan luồng**.

## 13. Màn 21 — dựng lại theo timeline (15/09, vòng 10)

Bản cũ là 4 thẻ phẳng chỉ có: mã · badge trạng thái · tên · ngày. Thiếu người chủ trì, thiếu giờ, không thấy được
trục thời gian. Dựng lại theo yêu cầu user:

**Timeline mới → cũ.** Thời gian là **mốc trên trục**, không nằm trong thẻ (user chốt 15/09):

```
● Thứ 2, 14/09/2026 · 08:30 - 10:00      ← node: chấm + NGÀY · GIỜ
│   ┌──────────────────────────────┐
│   │ MTG.26.0245      [Đã chốt]   │
│   │ Tên meeting                  │
│   │ 👤 Chủ trì: Nguyễn Hữu Học   │
│   │ Chưa lập biên bản            │
│   └──────────────────────────────┘
│
● Thứ 5, 28/08/2026 · 14:00 - 15:30
```

- **Node**: chấm tròn rỗng 14px viền 3px theo **màu trạng thái**, kế bên là `Ngày` (đậm, `#1A2332`) · `Giờ`
  (đậm, accent `#E8972C`). Đường nối 2px `#C9D0D8` chạy từ node xuống node kế.
- **Thẻ**: mã meeting + badge trạng thái · tên · `Chủ trì: …` · `Xem biên bản` / `Chưa lập biên bản` / `Lý do huỷ: …`
- Màu trạng thái lấy từ 9 mã chuẩn: `#2563EB` chốt lịch · `#16A34A` hoàn thành · `#DC2626` huỷ.

**Đối chiếu web** (`CustomerMeetingHistoryModal.vue`, 7 cột: STT · Thời gian · Mã - Tên meeting · Loại meeting ·
Dự án · Biên bản / Lý do hủy · Trạng thái):
- Web **KHÔNG có cột Người chủ trì** → đây là **bổ sung mới của app**, BE phải trả thêm `host_employee_id` /
  `host_name` cho endpoint `GET assign/meeting/customer-history` (cột `meetings.host_employee_id` đã có sẵn từ
  Phase 1 của feature bao-cao-cskh-tiem-nang).
- Web cột Thời gian chỉ in `item.start_date` một cục → app tách **ngày** và **khung giờ**, cần BE trả cả
  `start_date` lẫn `end_date` (đã có trong bảng).
- Hai cột web có mà app **chưa vẽ**: `Loại meeting` và `Dự án`. Chưa thấy cần trên điện thoại, chờ user quyết.
- Web có **6 bộ lọc** trong popup; app chưa có. Danh sách lịch sử của 1 khách hàng thường ngắn nên tạm bỏ.

**Lưu ý kỹ thuật khi dựng**:
- icon `clock` KHÔNG có trong bộ lucide của Pencil (`calendar-clock` thì có) → dùng dấu `·` ngăn ngày và giờ.
- pen.dev không có `alignItems: stretch` → đường nối phải đo chiều cao thẻ rồi set tay:
  `line.height = card.height + padding trên 8 + padding dưới 18`. Thẻ phải bọc thêm 1 frame `cardWrap` giữ
  padding trên, nếu để padding ở hàng `body` thì đường nối bị đứt một đoạn ngay dưới chấm.

## 14. ⚠️ Phạm vi dữ liệu màn 21 — LỆCH GIỮA YÊU CẦU VÀ CODE (15/09)

**Luật user chốt:** màn Lịch sử meeting chỉ hiện meeting mà **user đang đăng nhập** có trong thành phần họp.

**Code hiện tại KHÔNG làm thế.** `MeetingController::customerMeetingHistory()`
(`Modules/Assign/Http/Controllers/Api/V1/MeetingController.php:978`) lọc bằng:

```php
->whereExists(function ($q) {
    $q->select(DB::raw(1))
        ->from('meeting_employees as me')
        ->whereColumn('me.meeting_id', 'm.id')
        ->where('me.type', 1)
        ->whereColumn('me.employee_id', 'm.created_by');   // ← NGƯỜI TẠO, không phải user đang xem
});
```

Điều kiện này so `me.employee_id` với **`m.created_by`** — tức "người tạo meeting có nằm trong thành phần
của chính meeting đó không". Đây là **thuộc tính của bản ghi**, không liên quan gì tới người đang mở popup:
mọi user mở cùng 1 khách hàng đều thấy **danh sách y hệt nhau**. Route `/customer-history` cũng **không gắn
`checkPermission`** và trong hàm không có `auth()` nào.

**Cần sửa BE** — dùng lại nguyên khuôn đã có ở `PotentialCustomerCareService::applyPermissionFilter()`
(`Modules/Assign/Services/Report/PotentialCustomerCareService.php:143`):

```php
$userId = auth()->id();
$query->where(function ($q) use ($userId) {
    $q->where('m.host_employee_id', $userId)
      ->orWhereExists(function ($sub) use ($userId) {
          $sub->selectRaw(1)->from('meeting_employees as me')
              ->whereColumn('me.meeting_id', 'm.id')
              ->where('me.employee_id', $userId);
      });
});
```

Lưu ý khi sửa: giữ hay bỏ điều kiện `created_by` cũ phải hỏi lại — nếu giữ cả hai thì danh sách hẹp hơn nữa.
Đề xuất **thay** chứ không cộng thêm.

**Trên thiết kế app đã phản ánh luật**: dòng khách hàng đầu màn 21 ghi
`CT CP Sản xuất & KD VinFast · 4 cuộc họp bạn tham gia`, caption artboard ghi rõ điều kiện chủ trì HOẶC thành viên.

**Chưa có**: trạng thái rỗng "Bạn chưa tham gia cuộc họp nào với khách hàng này" — luật này làm danh sách rỗng
trở thành tình huống thật, nên cần 1 artboard. Chờ user duyệt.

## 15. Màn 06 — khối Giải pháp đổi sang cây CHA – CON (16/09)

Trước: danh sách phẳng 3 giải pháp, mỗi dòng có checkbox + dòng phụ ghi "GP.012 · 4 hạng mục" nhưng
**không liệt kê hạng mục nào**. User yêu cầu hiển thị cha – con.

**Đã dựng:**
- **Cha = Giải pháp**: checkbox 20px + tên + `GP.012 · 2/4 hạng mục` + chevron mở/đóng.
  Checkbox cha hiện **dấu gạch ngang** khi mới chọn một phần hạng mục, dấu tick khi chọn hết, rỗng khi chưa chọn.
- **Con = Hạng mục/Module**: thụt lề 48px, nền `#FAFBFC`, checkbox 18px + tên + mã hạng mục căn phải.
- Giải pháp chưa chọn gì thì mặc định **đóng** (GP.044), chỉ hiện chevron `chevron-right`.

### ⚠️ Khác bản web — đã note thẳng lên artboard

`GeneralInfo.vue`: mỗi phần tử `form.projects` có **đúng 1 ô Giải pháp và 1 ô Hạng mục/Module**, cả hai là
`SearchPicker` **ĐƠN** (không phải `MultiSearchPicker`); ô Hạng mục `disabled` khi chưa chọn Giải pháp.
Options lấy từ `getSolutionOptionsForProject()` và `getModuleOptionsForSolution(project.solution_id)`.

App đang vẽ **chọn nhiều** giải pháp và nhiều hạng mục → phải chốt trước khi code:
- (a) đổi web sang chọn nhiều — cần **bảng nối mới**, vì hiện chỉ có 2 cột đơn (`solution_id`,
  `solution_module_id`) nằm trên dòng project; hoặc
- (b) app cũng chỉ 1 giải pháp + 1 hạng mục, cây cha-con chỉ là **cách trình bày** cho dễ chọn.

**Khác về vị trí**: trên web khối này nằm TRONG màn Thông tin chung, ngay dưới ô Dự án TKT, và thuộc về
**từng dự án** đã gắn. App tách thành màn 06 riêng → nếu meeting gắn **nhiều dự án** thì màn 06 phải cho
chọn dự án trước rồi mới tới cây giải pháp. Chưa xử lý trường hợp này.

## 16. Màn 01 + 02 — phạm vi "của tôi" (16/09)

**Màn 01 · Lịch meeting**
- Tab cấp 1 đổi từ `Hôm nay / Sắp tới / Tất cả` → **`Tôi chủ trì` / `Tôi tham gia`**.
- Dải thẻ số liệu đổi thành **3 chip vừa là số liệu vừa là lọc nhanh**:
  `Đã hoàn thành` (chấm xanh lá) · `Sắp diễn ra` (chấm xanh dương) · `Chờ biên bản` (chấm cam).
  Bấm để lọc, bấm lại bỏ lọc; số đếm tính trong phạm vi tab đang chọn. Bản vẽ ở trạng thái chưa bấm chip nào.

**Màn 02 · Bộ lọc** — bỏ 2 ô `Công ty` và `Phòng ban`, còn **8 tiêu chí**; nút đổi thành `Áp dụng (2)`.

### BE — đã có sẵn criteria đúng, chỉ cần dùng đúng chỗ

| Criteria | Phạm vi | Dùng cho |
|---|---|---|
| `MeetingCriteria` | quyền tổng công ty / công ty / phòng ban / bộ phận | màn danh sách WEB |
| `MeetingCalendarCriteria` | **user có tên trong Thành phần — Phía Công ty (`meeting_employees.type = 1`)** | tab Lịch của `/assign/my-todo` → **app dùng cái này** |

Không tái dùng `MeetingCriteria`: criteria AND với nhau, khối phạm vi theo quyền nằm cứng bên trong nên AND thêm
điều kiện "liên quan tới tôi" vẫn không cứu được người chủ trì nằm ngoài phạm vi quyền (`false AND true = false`).
Comment trong chính file ghi rõ kèm số đo: **49 meeting lên lịch thì 37 cái không liên quan người xem**.

`MeetingCalendarCriteria` cố ý **không xét `host_employee_id`** — vì `MeetingService::ensureHostIsCompanyMember()`
đã tự đưa người chủ trì vào Thành phần ở MỌI lượt lưu; và **không xét `created_by`** — thư ký nhập hộ không phải người dự.

### ✅ ĐÃ CHỐT (16/09): 2 tab lấy ĐÚNG VAI TRÒ, rời nhau

- `Tôi chủ trì` = `host_employee_id = auth()->id()`
- `Tôi tham gia` = có trong `meeting_employees type=1` **VÀ** `host_employee_id <> auth()->id()`

Phải loại trừ vì chủ trì LUÔN nằm trong thành phần (`ensureHostIsCompanyMember()` tự thêm ở mọi lượt lưu) —
lấy nguyên `meeting_employees` thì meeting mình chủ trì đếm ở cả 2 tab. Tách theo vai trò thì
**tổng 2 tab = tổng meeting của tôi**, không trùng.

Meeting trạng thái **Đang tạo (nháp) chỉ người tạo thấy** — giữ nguyên luật, nhớ áp cả vào số đếm 3 chip.

Toàn bộ nội dung trên đã note thẳng lên artboard 01 (khối vàng dưới khung máy).

## 17. Dấu * trên Hub — theo TRẠNG THÁI của màn (16/09)

Trước: gắn `*` cứng cho 5 khối ở cả 10 Hub. Sai — ở Lưu nháp / Đã chốt lịch thì Biên bản, Kết luận,
Điểm danh **chưa bắt buộc**.

**Luật chốt:** `*` = khối bắt buộc **để lưu được ở trạng thái hiện tại của màn**, KHÔNG phải bộ khối cần cho Hoàn thành.

### Ma trận validate — tra từ source web

| Khối | Bắt buộc từ khi nào | Căn cứ |
|---|---|---|
| Thông tin chung | **Mọi lượt lưu, kể cả Lưu nháp** | `name`, `meeting_type_id`, `start_date`, `end_date`, `host_employee_id` = `required`; `location` = `required_if:mode_id,1` |
| Thành phần tham dự | **Mọi lượt lưu, kể cả Lưu nháp** | `company_members` = `required\|array` |
| Kết luận | chỉ khi Hoàn thành | `conclusion` = `required_if:status,3` |
| Biên bản | chỉ khi Hoàn thành | guard FE `hasMeetingReport()` |
| Điểm danh | chỉ khi Hoàn thành | guard FE `isAllAttended()` |
| Khảo sát nhu cầu KH | chỉ khi Hoàn thành **và** loại meeting `CODE_PRODUCT_INTRO` | `has_investment_demand` / `has_maintenance_demand` = `required_if:status,3` trong nhánh `$needSurvey` |
| Dự án TKT · Tài liệu chuẩn bị · Tài liệu biên bản | không bao giờ | `nullable` |

⚠️ **BE KHÔNG nới rule khi `status = 0`** — Lưu nháp vẫn phải có đủ Thông tin chung + Thành phần.
⚠️ Dòng biên bản đã nhập có required **cấp dòng** ở mọi trạng thái: `reports.*.content`,
`reports.*.executor_name`, `reports.*.expected_deadline`.

### Đã áp lên 10 Hub

| Hub | Dấu * |
|---|---|
| 04a Lưu nháp · 04b Đã chốt lịch · 24 Hub có lỗi · 16/22/23 (nền popup) | **chỉ** Thông tin chung + Thành phần |
| 04c Đã hoàn thành · 46 Hub chặn Hoàn thành | đủ **5** khối |
| 26 Đã huỷ · 27 Chỉ xem | **không có** dấu * (không sửa được nữa) |

Tổng 50 dấu `*` (10 Hub × 5 dòng) → tắt 28, giữ 22.

**Thanh Mức độ hoàn thiện hồ sơ giữ nguyên x/5** (6 nếu loại meeting có Khảo sát) — cố ý **khác** dấu `*`,
vì nó trả lời câu "còn bao xa tới Hoàn thành". Đã ghi rõ chỗ khác biệt này trong DEV NOTE trên artboard 04a.

## 18. Liên quan

- Đề xuất API lưu từng phần: `api-luu-tung-phan.md` (cùng thư mục)
- Nguồn đối chiếu web: `hrm-client/pages/assign/meeting/components/GeneralInfo.vue`, `components/modals/ChooseErpCustomerModal.vue`, `components/modals/QuickAddCustomerModal.vue`
