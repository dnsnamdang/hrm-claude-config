# Meeting theo đối tượng (Dự án TKT / Hợp đồng) — Design

> @namdangit · Module `Assign` · Nhánh `gop_db` (cả 2 repo) · Brainstorm chốt 08/10/2026
> Feature nhỏ (1 phase) → design.md + plan.md. **CHƯA được phép code** — chờ user cho phép riêng kèm phạm vi.

## Mục tiêu

Thay checkbox "Meeting theo dự án" ở form meeting bằng **cấu hình trên loại meeting**: loại meeting
khai "Meeting theo đối tượng" = Dự án TKT / Hợp đồng → meeting thuộc loại đó **bắt buộc** chọn đối
tượng tương ứng.

## Hiện trạng (đọc code 08/10/2026)

- `meeting_types` có `has_customer` (cờ tương tự). Nút Sửa chỉ hiện khi `isCanEdit()` = không phải
  hệ thống + đang hoạt động + **chưa có meeting nào** (`MeetingType.php:41`, FE `meeting_type/index.vue:939`).
  BE `updateOrCreate` chỉ chặn loại hệ thống (`MeetingTypeController.php:54`).
- Checkbox `meetings.has_prospective_project` (`GeneralInfo.vue:256`) điều khiển 3 việc:
  ô chọn NHIỀU Dự án TKT (+ Giải pháp/Module mỗi dự án), giữ khối Khách hàng khi đổi loại meeting
  (`GeneralInfo.vue:1211`), tab "Dự án tiền khả thi" (`MeetingForm.vue:474`).
  Dự án lưu ở bảng nối `prospective_project_meetings`.
- Nguồn dự án: `GET assign/prospective-projects/getForMeeting` — dự án mình tạo / mình làm giải pháp /
  mình là người hỗ trợ. FE lọc `status != 1` + lọc theo `customer_id` đã chọn; chọn dự án → tự điền KH.
- Meeting **chưa có liên kết hợp đồng**. Hợp đồng HRM = `hrm_contracts` (`Modules/Assign/Entities/Contract/Contract.php`).

## Quyết định đã chốt

| # | Câu hỏi | Chốt |
|---|---|---|
| 1 | Dự án TKT nào được chọn | Dự án thường: tiến trình **2 → 10** (bỏ 1 Đang tạo, 11 Đóng/Không thực hiện, 12 Kết thúc & lưu trữ). Dự án cha: **cho chọn**, cùng dải 2–10 → thực tế 2 Đang thực hiện · 7 Trình duyệt HĐ · 8 Thương thảo HĐ · 9 HĐ đủ ĐK thực hiện · 10 Nghiệm thu & Thanh lý. Một điều kiện `status BETWEEN 2 AND 10` cho cả 2 loại. |
| 2 | Hợp đồng nào được chọn | Hợp đồng HRM (`hrm_contracts`, không phải HĐ ERP cũ). Mọi trạng thái **trừ** 3 Đang tạo và 10 Đã thanh lý — lọc bằng LOẠI TRỪ để trạng thái chưa kích hoạt (8/9/11/12) tự vào khi bật. |
| 3 | Chọn 1 hay nhiều | TKT giữ **nhiều** (bảng nối cũ, báo cáo không đổi). Hợp đồng chọn **1** → cột `meetings.contract_id`. |
| 4 | Phạm vi danh sách | TKT: giữ phạm vi `getForMeeting` hiện tại. Hợp đồng: **tất cả** hợp đồng (không lọc quyền). Endpoint chỉ trả `id, code, customer_*, status` — **không trả giá trị/số tiền**. |
| 5 | Hợp đồng ↔ Khách hàng | Giống TKT: đã chọn KH → chỉ hiện HĐ của KH đó; chọn HĐ trước → tự điền KH + người liên hệ từ HĐ. |
| 6 | Bỏ checkbox, meeting cũ | Ô Dự án TKT + tab "Dự án tiền khả thi" hiện khi **loại = TKT HOẶC meeting đã có dự án**; chỉ bắt buộc khi loại = TKT. Cột `has_prospective_project` giữ trong DB, thôi dùng cho hiển thị. Tạo từ trong Dự án TKT (`?project_id=`) giữ nguyên: luôn hiện + khoá ô dự án, bất kể loại. |
| 7 | Loại meeting đang dùng | Loại đã có meeting vẫn mở popup Sửa nhưng **chỉ đổi được "Meeting theo đối tượng"**, các ô khác khoá; BE chặn đổi trường khác. Loại hệ thống vẫn khoá hoàn toàn. Đổi cấu hình chỉ ảnh hưởng tạo/sửa về sau. |
| 8 | Màn danh sách loại meeting | Thêm: cột · bộ lọc (TKT / Hợp đồng / Không) · cột xuất Excel · ghi lịch sử danh mục. **Không** thêm vào nhập Excel (loại nhập vào = Không). |
| 9 | Hiện HĐ ở đâu | Form + chi tiết meeting (mã · tên KH · badge trạng thái; chi tiết bấm mã mở HĐ tab mới) · lịch sử meeting ("Hợp đồng: cũ → mới"). **Không**: cột/lọc ở danh sách meeting, tab Meetings trong HĐ, báo cáo. |

Tự chốt (kỹ thuật): đổi loại khỏi "Hợp đồng" → xoá `contract_id` (TKT thì giữ dự án theo #6).
Meeting cũ có HĐ/dự án đã ra khỏi dải trạng thái → vẫn hiện lựa chọn cũ (kiểu `include_ids`);
BE chỉ kiểm dải trạng thái với giá trị **mới chọn thêm**. Lỗi: "Vui lòng chọn Dự án TKT." /
"Vui lòng chọn Hợp đồng." — hiện đồng thời với lỗi các ô khác khi bấm Lưu.

### Điều chỉnh sau review (08/10/2026)
- `getForMeeting` KHÔNG nhận `include_ids` tự do (lộ ngân sách/KH của dự án bất kỳ) → nhận `meeting_id`, BE tự lấy dự án đang gắn và chỉ khi người gọi `canView()` meeting đó.
- `contracts/for-meeting` KHÔNG trả `customer_contact_phone` (endpoint không lọc quyền, SĐT KH phải qua che số). Chọn HĐ chỉ điền KH + tên người liên hệ; SĐT điền ở bước chi tiết KH nếu có quyền.
- Admin đổi cấu hình loại khỏi "Hợp đồng": meeting cũ giữ nguyên loại thì GIỮ HĐ (ô HĐ vẫn hiện, không bắt buộc) — đối xứng với dự án ở #6. Chỉ khi user tự đổi loại meeting mới bỏ HĐ.

### Sửa 5 lỗi nhỏ sau review (09/10/2026)
- Ô Dự án TKT + tab không tự ẩn khi bỏ dự án cuối (cờ `hadProjects` giữ suốt phiên mở form).
- Chế độ chỉ-đổi-đối-tượng so tên/mô tả sau khi `trim` (dữ liệu cũ dính khoảng trắng không bị 423 oan).
- BE chặn HĐ khác khách hàng của meeting: "Hợp đồng không thuộc khách hàng đã chọn."
- Danh sách loại meeting lấy `meetings_exists` bằng `withExists` (hết 1 truy vấn/dòng — trước đó 49 câu).
- `has_prospective_project` suy từ bảng nối SAU khi sync (`MeetingService::refreshHasProspectiveProject`), không từ payload.

## Thiết kế

### DB (2 migration, `Modules/Assign/Database/Migrations`)
- `meeting_types.target_type` tinyint unsigned NULL — `1` Dự án TKT, `2` Hợp đồng, NULL = không.
  Hằng `MeetingType::TARGET_PROSPECTIVE_PROJECT = 1`, `TARGET_CONTRACT = 2` + `TARGETS` (id/name) là nguồn tên duy nhất.
- `meetings.contract_id` unsignedBigInteger NULL + index. Không FK (theo thói quen bảng meetings; kiểm lại khi viết plan).

### BE
- **MeetingType:** fillable `target_type`; `MeetingTypeRequest` thêm `nullable|in:1,2`.
  `isCanEditTargetOnly()` = không hệ thống + đã có meeting. `updateOrCreate`: nếu đang ở chế độ chỉ-đổi-đối-tượng
  → chỉ nhận `target_type`; trường khác bị đổi → trả 423 "Loại meeting đã có meeting, chỉ được đổi Meeting theo đối tượng." Resource trả `target_type`, `target_type_text`,
  `is_can_edit_target`. Bộ lọc `target_type` (giá trị `0` = NULL). `MeetingTypeExport` + `ExportColumnRegistry`
  thêm cột. `CatalogHistoryService` ghi đổi `target_type`.
- **Meeting create/update request** (cả 2 file):
  - loại có `target_type = 1` → `projects` `required|array|min:1`; dự án **mới** (không có trong liên kết cũ)
    phải có `status` 2–10.
  - loại có `target_type = 2` → `contract_id` `required`; nếu khác giá trị đang lưu thì phải tồn tại trong
    `hrm_contracts` và `status NOT IN (3, 10)`.
  - bỏ dùng `has_prospective_project` trong rule.
- **Controller store/update:** lưu `contract_id` (xoá về NULL khi loại không phải HĐ). Thôi ghi
  `has_prospective_project` từ request (giữ cột).
- **Endpoint chọn HĐ:** `GET assign/contracts/for-meeting?customer_id=&include_id=` — tất cả HĐ ngoài
  (3, 10), cộng `include_id` nếu có; trả `id, code, customer_id, customer_name, customer_code, customer_contact_*, status, status_name, status_color`.
  Không gắn quyền Hợp đồng (chốt #4), chỉ cần đăng nhập.
- **getForMeeting (TKT):** thêm điều kiện `status BETWEEN 2 AND 10` ở BE (thay lọc `!= 1` ở FE), cộng
  `include_ids` để giữ dự án cũ của meeting đang sửa.
- **MeetingTransformer:** trả `contract_id` + `contract` (code, customer_name, status_name, status_color).
  `MeetingHistoryService` ghi "Hợp đồng".

### FE
- `meeting_type/index.vue`: cột + bộ lọc + popup thêm `V2BaseSelect` "Meeting theo đối tượng" (không bắt buộc).
  Nút Sửa hiện thêm khi `is_can_edit_target`; ở chế độ đó khoá các ô khác.
- `GeneralInfo.vue`: bỏ checkbox. `showProjectPicker = targetType === 1 || hasExistingProjects || isFromProject`;
  ô Hợp đồng (`SearchPicker` 1 giá trị) hiện khi `targetType === 2`, lọc theo `customer_id`, chọn → điền KH.
  Dấu `*` theo `targetType`. `keepCustomerFromProject` tính theo đối tượng thay cho checkbox.
- `MeetingForm.vue:474`: tab "Dự án tiền khả thi" theo cùng điều kiện `showProjectPicker`.
- `create.vue`: bỏ `has_prospective_project` khỏi form mặc định.
- Màn chi tiết: hiện HĐ dạng link mở tab mới.

### Ngoài phạm vi
- Thiết kế app mobile (`.plans/app-meeting-mobile`) — cần cập nhật luồng chọn đối tượng sau.
- Danh sách meeting, báo cáo meeting, tab Meetings trong Hợp đồng.

## Kiểm thử
- Quyền: tạo meeting loại HĐ bằng tài khoản **không** có quyền xem Hợp đồng → vẫn chọn được (chốt #4),
  response không chứa trường tiền. Tài khoản không quyền quản lý danh mục → không thấy nút Sửa.
- Playwright (MCP) đo DOM: ô hiện/ẩn theo loại; bấm Lưu thiếu đối tượng → lỗi hiện cùng các ô khác;
  meeting cũ có dự án + loại không TKT → vẫn thấy ô + tab, lưu không bị bắt buộc; danh mục: loại đang dùng
  mở Sửa chỉ đổi được ô đối tượng.
- Cập nhật spec e2e meeting + danh mục loại meeting (chỉ chạy khi user yêu cầu).
