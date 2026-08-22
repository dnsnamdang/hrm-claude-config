# Yêu cầu kiểm tra sửa chữa – bảo hành (YCKT SC-BH)

> Port màn ERP `/admin/customer-care/warranty_repair_requests` sang HRM. Nhánh `gop_db`.
> Phụ trách: @namdangit · Bắt đầu: 2026-08-18
> Spec chi tiết: `docs/superpowers/specs/gop-db/2026-08-18-warranty-repair-request-design.md`

## Mục tiêu

Đây là **chứng từ đầu tiên** của dây chuyền 9 chứng từ phân hệ Dịch vụ (Bảo hành – Sửa chữa).
Nó ghi nhận "khách báo hỏng", rồi chuyển cho phòng tiếp nhận để lập *Phiếu xử lý yêu cầu*.

Bản đồ toàn luồng: artifact "Luồng Dịch vụ ERP"
(https://claude.ai/code/artifact/a48710cf-029a-45c5-b1d7-9b39da28c18d).

## Vị trí trong hệ thống — CHỐT 2026-08-19

Màn thuộc **phân hệ CSKH**, KHÔNG phải CSKH (user chốt 2026-08-19):

| | |
| --- | --- |
| Menu | **CSKH → Kiểm tra bảo hành sửa chữa → Yêu cầu kiểm tra sửa chữa - bảo hành** (mục ĐÃ CÓ SẴN trong `components/subsystem-menu/sale-hub.js`, chỉ nối thêm `link`) |
| Route FE | `/customer-care/warranty-repair-requests` |
| Code FE | `pages/customer-care/warranty-repair-requests/` |
| Code BE | `Modules/CustomerCare/` |
| Prefix API | `/api/v1/customer-care/warranty-repair-requests` |
| Quyền | `type = 23` (Bán hàng), group `Yêu cầu sửa chữa - bảo hành` |

⚠️ Bảng dữ liệu (`warranty_repair_requests`) và các danh mục liên quan vẫn là của luồng Dịch vụ,
nhưng **vị trí menu/module đi theo phân hệ CSKH** — đừng suy module từ tên bảng.

## Scope — CHỐT 2026-08-18

| Hạng mục | Quyết định |
| --- | --- |
| Phạm vi | **Full như ERP**: 3 tab + CRUD + Chuyển phòng tiếp nhận + Từ chối + In phiếu + In danh sách + Xuất Excel |
| Trạng thái | **Giữ nguyên 9** (kể cả trạng thái do chứng từ downstream đẩy về) |
| Bảng thiết bị | **Đủ 3 nguồn** `ncck` / `tpc` / `tp` — dùng lại `getListProductOfCustomer`, kèm serial |
| Permission | **Copy nguyên tên quyền ERP** (3 quyền xem theo cấp + "Xử lý yêu cầu sửa chữa") |

## Dữ liệu

2 bảng **đã tồn tại sẵn trên DB gộp**, KHÔNG tạo migration mới:

- `warranty_repair_requests` — header phiếu
- `warranty_repair_request_products` — thiết bị trong phiếu

## 9 trạng thái

| # | Hằng | Nhãn | Ai set |
| --- | --- | --- | --- |
| 1 | STATUS_CREATING | Đang tạo | Màn này (Lưu nháp) |
| 2 | STATUS_WAITING_HANDLE | Chờ xử lý | Màn này (Gửi yêu cầu) |
| 3 | STATUS_HANDLING | Đang xử lý | Phiếu xử lý yêu cầu |
| 9 | STATUS_CREATING_INFORMATION | Đang CCTT | Phiếu CCTT |
| 4 | STATUS_HAS_INFORMATION | Đã CCTT báo giá | Phiếu CCTT |
| 5 | STATUS_HAS_QUOTATION | Đã báo giá | Báo giá dịch vụ |
| 6 | STATUS_HAS_CONTRACT | Đã lập hợp đồng | Hợp đồng dịch vụ |
| 7 | STATUS_HANDLED | Đã xử lý | Downstream |
| 8 | STATUS_PHONE_CONSULTATION | Đã tư vấn điện thoại | Phiếu xử lý yêu cầu |

## Màn danh sách — 1 DANH SÁCH, KHÔNG TAB (sửa 2026-08-19)

ERP có **đúng 1 màn danh sách** (`index.blade.php`, 1 bảng `#table-list`), menu trỏ thẳng vào
`?type=all` (`topmenubar.blade.php:438` / `:1918`). Tham số `type` của `searchByFilter` **không
phải 3 màn**:

| `type` | Vai trò thật bên ERP |
| --- | --- |
| `all` | thứ **menu trỏ tới** — phạm vi chuẩn của màn |
| `index` | giá trị mặc định khi vào route trần (2 mục menu phụ) |
| `waiting_handle` | **không có mục menu nào** — chỉ là link "Quay lại" từ màn form |

→ HRM cũng dùng **1 màn duy nhất, luôn chạy `all`**. Bản đầu tôi dựng 3 tab từ 3 giá trị `type`
là **sai** (user chỉ ra 2026-08-19) — đã gỡ.

Phạm vi `all` đã bao trùm: gate 3 cấp quyền + phiếu do chính mình tạo + phiếu gửi về phòng tiếp
nhận của mình. Muốn xem riêng phiếu của mình → lọc ô **Người yêu cầu** (đã kiểm: cho ra đúng cùng
số phiếu với tab "Phiếu của tôi" cũ).

### Đổi phạm vi bằng query, đúng cơ chế ERP

ERP truyền `d.type = '{{ $type }}'` xuống datatable, `$type = $request->type ?? 'index'`.
HRM giữ nguyên: `/customer-care/warranty-repair-requests?type=index|all|waiting_handle`.
Mặc định `all` (thứ menu trỏ tới). Query **thắng** bộ lọc đã lưu trong localStorage.

### Đối chiếu bộ lọc với ERP

| ERP (`index.blade.php`) | HRM |
| --- | --- |
| `code` (text) | gộp vào **ô tìm nhanh** (BE lọc `code` OR `customer_name`) |
| `status` (select) | ✓ |
| `customer_id` (select-ajax) | ✓ (`V2BaseSelectRemote`) |
| `product_name` (text) | ✓ |
| `created_by` (select-ajax) | ✓ |
| `province_id` (select) | ✓ |
| `search_by_time` | ✓ Ngày yêu cầu từ – đến |
| `search_by_info` (is_big_boss/is_boss/is_manager) | ✓ khối Công ty – Phòng ban, hiện theo `scope` BE trả về |

## Điều kiện hành động (nguồn chân lý = accessor Entity)

| Hành động | Điều kiện |
| --- | --- |
| Sửa / Xoá | `status = Đang tạo` **và** `created_by = tôi` (`canEdit`) |
| Tạo phiếu xử lý yêu cầu · **Chuyển phòng tiếp nhận** · **Từ chối** | **CÙNG một điều kiện** `canHandleRequest()`: `status = Chờ xử lý` + đúng phòng tiếp nhận + quyền "Xử lý yêu cầu sửa chữa" + **chưa có phiếu xử lý** (Super admin — role id 18 — bỏ qua điều kiện phòng) |
| In | luôn hiện |

⚠️ **Đừng tách điều kiện của Chuyển phòng / Từ chối ra riêng.** ERP có sẵn hàm
`canTransferDepartmentReception()` với điều kiện khác, nhưng đó là **CODE CHẾT — 0 nơi gọi**.
Thực tế ERP gate cả nhóm bằng `canHandelRequest()`: cột Hành động danh sách (2 khối `if` giống hệt
nhau), guard endpoint transfer, và footer màn form (3 nút chung 1 `@if`). Bản đầu tôi tách riêng →
Super admin chuyển được phiếu của phòng khác (sửa 19/08).

### Số hành động — 2 màn phải KHỚP

| | Danh sách | Chi tiết |
| --- | --- | --- |
| Phiếu nháp của tôi | Sửa · Xoá · In | Sửa · Xoá · In |
| Phiếu Chờ xử lý gửi về phòng tôi | Tạo phiếu xử lý · Chuyển phòng · Từ chối · In | Tạo phiếu xử lý · Chuyển phòng · Từ chối · In |
| Phiếu trạng thái khác | In | In |

**Khác ERP 1 điểm — user chốt 19/08**: ERP đặt "Không duyệt" ở footer màn form, cột Hành động của
danh sách chỉ có 5 nút. HRM đưa **Từ chối vào cả 2 nơi** để tuân thủ quy tắc "màn chi tiết phải có
đủ hành động như dòng ở danh sách" (`list-page` mục 7.2 + CLAUDE.md). Nghiệp vụ không đổi, chỉ thêm
lối vào nhanh cho người tiếp nhận.

## Quyết định đã chốt

> Nguyên tắc user chốt 2026-08-18: **nghiệp vụ bám ERP 1:1, trình bày theo skill.**

- **Mã phiếu**: `{mã công ty}.YCSCBH.{yy}.{6 số}` — giữ nguyên format ERP.
- **Thông báo**: khi phiếu chuyển sang "Chờ xử lý" → bắn cho **cả phòng tiếp nhận**
  (prefix `[YCSCBH]`, theo skill `notification-convention`). **Bổ sung so với ERP**: báo ngược cho
  người lập khi bị Từ chối — ERP không báo gì, người lập phải tự vào xem mới biết.
- **Không dùng `mysql2`** — đọc/ghi thẳng bảng ERP trên DB gộp.
- **Màu trạng thái do BE trả về** (`status_color` hex), FE chỉ hiển thị qua `V2BaseBadge :color`.
  Dùng đúng 5 trong 9 mã màu chuẩn: `#64748B` Đang tạo · `#D97706` Chờ xử lý ·
  `#2563EB` Đang xử lý / Đang CCTT · `#0EA5E9` Đã CCTT / Đã báo giá / Đã lập hợp đồng ·
  `#16A34A` Đã xử lý / Đã tư vấn điện thoại. Quy tắc này đã được bổ sung vào
  `.claude/skills/list-page/SKILL.md` mục 3c-1 & 3c-2 và `CLAUDE.md` trong session này.
- **Chữ trên nút theo skill, KHÔNG copy ERP**: ERP ghi "Lưu" / "Lưu & Gửi duyệt" / "Không duyệt"
  → HRM dùng **"Lưu nháp" / "Lưu và gửi" / "Từ chối"** (bảng text chuẩn của
  `button-convention`). Nghiệp vụ không đổi: vẫn là `status = 1` và `status = 2`.
- **Validate theo trạng thái, KHÁC ERP có chủ ý**: ERP bắt buộc TOÀN BỘ trường kể cả khi lưu nháp
  (không lưu dở dang được). HRM: `status = 1` chỉ cần Khách hàng; `status = 2` bắt buộc đủ như ERP
  (skill `form-validate`). FE chỉ gắn required cho Khách hàng, phần còn lại BE trả 422.
- **Excel / In danh sách gộp mỗi phiếu 1 dòng**: ERP tách MỖI THIẾT BỊ thành 1 dòng (phiếu 5 thiết
  bị in ra 5 dòng trùng nhau, STT cũng lặp). HRM để thiết bị xuống dòng trong 1 ô → số dòng =
  số phiếu, đếm ra đúng.
- **Dùng lại thay vì viết mới** (bắt buộc rà project trước — CLAUDE.md):
  - Popup chọn khách hàng → `components/modals/ChooseErpCustomerModal.vue` (modal global).
  - Người liên hệ → select từ `customer.contacts` (pattern `pages/assign/prospective-projects`).
  - Trang thiết bị của khách → `GET /v1/assign/customers/{id}/equipment`
    (`CustomerManagerService::equipmentList`, đủ 3 nguồn + serial) — KHÔNG viết API mới.
  - Mẫu in → 2 mẫu ERP sẵn có trong `report_templates`: **277** (1 phiếu) và **278** (danh sách).
- **Ánh xạ loại thiết bị** HRM → giá trị cột `type` mà ERP lưu:
  `tan_phat → tp` · `external_old → tpc` · `external_equipment → ncck`.

## Còn nợ

- Nút **"Tạo phiếu xử lý yêu cầu"** hiện đúng điều kiện nhưng chưa điều hướng được — màn *Phiếu xử
  lý yêu cầu* chưa port, tạm báo toast hướng dẫn xử lý trên ERP. Bỏ nhánh này khi màn đó xong
  (`index.vue::handleRowAction`, nhánh `action === 'handle'`).


## Đổi chữ nút gửi phiếu (2026-08-21)

Nút gửi phiếu đổi từ **"Lưu và gửi duyệt"** sang **"Lưu và gửi"** (user chốt): phiếu được GỬI cho
PHÒNG TIẾP NHẬN để họ xử lý — phòng đó chỉ có Từ chối / Chuyển phòng tiếp nhận / lập Phiếu xử lý,
**không có thao tác "Duyệt" nào**. `V2Footer` có sẵn `send_and_submit_form` kèm đúng câu xác nhận
("Xác nhận lưu và gửi / Bạn đồng ý lưu và gửi?") nên KHÔNG phải sửa component dùng chung.
Cả 3 chứng từ của luồng dịch vụ nay dùng chung chữ này.
`testcase.xlsx` và `Mô tả nghiệp vụ` đã sinh lại theo chữ mới; bản testcase ERP giữ nguyên.
