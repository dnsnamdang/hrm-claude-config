# Design — Yêu cầu mua dịch vụ (ERP `buy_service_requests` → HRM)

> Phụ trách: @junfoke · Nhánh: `feat/finance-buy-service-request` (từ `gop_db`) · 2026-09-22
> **Spec đầy đủ (schema, API, luồng, edge case): `docs/superpowers/specs/gop-db/2026-09-22-buy-service-request-design.md`**
> Plan + kiểm chứng: `plan.md`

## Mục tiêu

Port màn **Yêu cầu mua dịch vụ** (YCMDV) từ cổng ERP sang HRM. Nhân viên lập phiếu đề nghị mua
dịch vụ thuê ngoài (vận chuyển, lắp đặt, thuê nhân công, kiểm định…), Trưởng phòng duyệt nội dung
rồi **Ban kiểm soát duyệt giá**; phiếu duyệt xong là đầu vào để kế toán lập *Hợp đồng mua dịch vụ*.

Hai bảng ERP có sẵn trên DB gộp — **KHÔNG đổi schema, KHÔNG migration**. Lịch sử thay đổi dùng
bảng CHUNG `catalog_histories` nên màn này không thêm bảng nào (xem quyết định 8).

## Bối cảnh: đây là màn ĐẦU của chuỗi 4 màn

```
Yêu cầu mua dịch vụ  →  Hợp đồng mua dịch vụ  →  YC hạch toán mua dịch vụ  →  Hạch toán mua dịch vụ
      (port lần này)         (giữ ở ERP)               (giữ ở ERP)                  (giữ ở ERP)
```

Chọn màn này port trước vì nó **tự đủ**: toàn bộ nghiệp vụ (lập · 2 nấc duyệt · duyệt lại giá ·
hủy · in · xuất Excel) nằm trọn trong màn. Ba màn sau đều phụ thuộc ngược lên *Hợp đồng mua dịch
vụ* nên không port riêng lẻ được.

## Phạm vi (user chốt 2026-09-22)

| Chốt | Nội dung |
| --- | --- |
| Phạm vi | **Đầy đủ như ERP**: danh sách (3 cửa vào) · chi tiết · tạo · sửa · xóa · TP duyệt · KS duyệt giá · yêu cầu duyệt lại giá · hủy · từ chối · in phiếu · in danh sách · xuất Excel |
| Nút "Lập hợp đồng mua dịch vụ" | **Giữ nút, trỏ sang cổng ERP** qua `env('ERP_URL')` — màn HĐMDV chưa port |
| Module BE | **`Modules/Finance`** (user chốt) — dù màn thuộc phân hệ Bán hàng trên FE |
| Đường dẫn FE | **`/finance/buy-service-requests`** — user chốt "đúng chỗ code" |
| Menu | Phân hệ **Bán hàng**, nhóm `Yêu cầu → Mua dịch vụ` (`sale-hub.js:153`). Bỏ 2 mục trùng ở nhóm `Yêu cầu → Dịch vụ` |
| Phân quyền | Tạo 5 quyền HRM **trùng TÊN quyền ERP**, guard `api`, **id 1586-1590** trong bảng `permissions` (KHÔNG phải `hrm_permissions`), `type = 23` (phân hệ Bán hàng), `group = 'Yêu cầu mua dịch vụ'` |

## Quyết định lớn

1. **BE ở `Modules/Finance`, FE thuộc phân hệ Bán hàng — phân hệ ≠ vị trí code module.**
   Đặt ở Finance để dùng lại nguyên bộ đã chạy ổn: `Finance/Entities/Supplier`,
   `CustomerCare/Entities/Cost/Cost`, `Finance/Http/Middleware/CheckDueConfig`, trait
   `ChecksEmployeePermission`, pattern đính kèm + phạm vi xem của họ màn `prepick-*`.

2. **Điểm cắt duy nhất là nút "Lập hợp đồng".** Bên ERP nút này chỉ là link
   `/admin/orders/buy-service-contract/create?buy_service_request_id=<id>`, **không xử lý gì phía
   YCMDV**, nên chỉ cần trỏ sang ERP. Đúng tiền lệ màn *Yêu cầu hạch toán bổ sung*.

3. **Trạng thái 6 (Đang lập hợp đồng) / 7 (Đã lập hợp đồng) và cột `contracted_qty` là CHỈ ĐỌC
   với HRM** — do `BuyServiceContract::updateBuyServiceRequests()` bên ERP ghi. Dùng chung DB gộp
   nên phiếu tự nhảy trạng thái đúng, HRM không làm gì thêm. **Tuyệt đối không ghi 2 cột này.**

4. **Mã phí lọc `kind_of = 2`** (Dịch vụ sửa chữa & chi phí khác) — đúng `Cost::getForSelect()` của
   ERP, và đã verify 98/98 dòng chi tiết thật đều thuộc loại này. Danh mục này **đã port** sang HRM.

5. **Nhà cung cấp đọc từ `customers` có `is_supplier`**, KHÔNG dùng bảng `suppliers` (bảng đó tồn
   tại trên DB gộp nhưng **0 dòng** — dùng nhầm thì popup NCC rỗng). Đã có sẵn
   `Finance/Entities/Supplier` với global scope.

6. **Đính kèm ghi vào cột `attachments`** (chuỗi nối bằng `, `), KHÔNG dùng bảng `files` chung —
   cổng ERP đọc thẳng cột đó, ghi chỗ khác là bên ERP mở phiếu ra mất sạch đính kèm.

7. **In dùng `report_templates` id 417 (phiếu) / 416 (danh sách)** — mẫu in lưu trong DB, HRM đọc
   qua `Finance/Entities/ErpReportTemplate`. Không dựng lại mẫu.

8. **CÓ làm khối Lịch sử thay đổi, đủ 2 nơi** (user chốt 2026-09-22) — popup mở từ menu ⋮ ở màn
   danh sách **và** khối trong màn chi tiết.

   ⚠️ **ĐỔI HƯỚNG giữa chừng (22/09):** ban đầu bám `PrepickExtendRequestHistory` (bảng history
   riêng cho từng màn) — sai khuôn hiện hành. Mọi màn phiếu Tài chính đã dùng bảng **CHUNG**
   `catalog_histories` qua trait `App\Services\Concerns\LogsCatalogHistory` và endpoint
   `catalog-histories/{bảng}/{id}`. Đã gỡ bảng riêng, đăng ký `buy_service_requests` vào
   `CatalogHistoryService::TABLES` ⇒ **màn này không còn migration nào**.

   Cổng ERP vẫn sửa được phiếu mà không sinh log — log thiếu ở những thao tác làm bên ERP là
   **hạn chế đã biết**, không phải lỗi.

## Các chỗ SỬA so với ERP (có chủ ý)

| Chỗ | ERP | HRM | Lý do |
| --- | --- | --- | --- |
| Màu trạng thái "Đang tạo" | `type: 'danger'` (đỏ) | xám `draft` | SRS: đỏ chỉ dành cho Từ chối / Khóa. Lỗi này đã phải sửa ở 2 màn Tài chính trước |
| Nút không dùng được | disable | **ẩn hẳn** | rule HRM: nút không dùng được thì ẩn |
| Bộ lọc | thanh lọc phẳng | `V2BaseSmartFilterPanel` + popup "Cài đặt bộ lọc" | 8 ô lọc, vượt ngưỡng phải có popup |
| Xuất Excel | tải file luôn | `ExportFieldsModal` chọn cột trước | convention xuất Excel phía FE |
| `canDepartmentApprove()` | ERP **comment tắt** đoạn kiểm `department_id` — ai có quyền TP là duyệt được phiếu của MỌI phòng | giữ nguyên như ERP | không tự ý siết; ghi lại đây để QA biết đó là chủ ý |
| Phạm vi quyền **"theo phòng ban"** | chỉ phòng mình **QUẢN LÝ** (`employee_manage_departments`) | phòng mình quản lý **+ phòng mình đang ngồi** | Quy ước chung của cả phân hệ Tài chính (xem mục dưới) — **user chốt 23/09/2026 giữ nguyên** |
| Mặc định khi URL thiếu `?type=` | `index` — "của tôi" | `all` — danh sách tổng hợp | Menu ERP **không có mục nào trỏ tới `index`** (`topmenubar.blade.php:1766` chỉ còn `?type=all`, 2 mục kia đã comment) ⇒ `index` là mặc định chết. Gõ trần URL mà ra "của tôi" thì tưởng màn mất dữ liệu (user báo 23/09). Đúng bằng màn YC xuất hàng mượn |

Màn chỉ có **một** cửa vào trên menu (`?type=all`). **User chốt 23/09/2026: giữ nguyên**, KHÔNG thêm tab chuyển cửa vào trên màn, cũng không mở lại 2 mục menu `index` / `for-approve` mà ERP đã comment. `?type=index` và `?type=for-approve` vẫn chạy nếu gõ thẳng URL (các màn khác điều hướng sang được), chỉ là không có lối vào từ menu.

### Khác biệt phạm vi "theo phòng ban" — user chốt GIỮ NGUYÊN (23/09/2026)

ERP hiểu quyền *"Xem yêu cầu mua dịch vụ - theo phòng ban"* là **phòng mình QUẢN LÝ**; HRM
(`ChecksEmployeePermission::manageableDepartmentIds()`) cộng thêm **phòng mình đang ngồi**.

Ví dụ đo thật: NV **#105 Bùi Duy Trước** quản lý phòng 85 (**0 phiếu**) nhưng ngồi phòng 95 —
PHÒNG DỰ ÁN TRỌNG ĐIỂM (**51 phiếu**) ⇒ ERP thấy **0**, HRM thấy **51**.

| | Số liệu |
| --- | --- |
| Người có quyền cấp "phòng ban" ở màn này | 57 |
| Trong đó rơi đúng tình huống trên | **5** (hiện mới 1 người lộ ra, 4 người kia phòng chưa có phiếu) |

**Vì sao giữ nguyên:** đây không phải thứ màn này tự thêm mà là **quy ước chung của phân hệ Tài
chính** — 8 entity + 1 service gọi `manageableDepartmentIds()`, và 3 màn hàng giữ
(`PrepickExtendRequest` · `PrepickCancelRequest` · `PrepickTransferRequest`) còn giữ bản chép riêng
cũng cộng phòng mình y hệt. Sửa cho khớp ERP là đổi hành vi **9 màn đang chạy thật** → phải tách
thành việc riêng có QA đàng hoàng, không nhét vào đợt port màn này.

⇒ **QA đối chiếu HRM vs ERP thấy lệch ở đúng nhóm này thì KHÔNG phải bug.**

## Cập nhật theo tài liệu pull ngày 22/09/2026

Rà lại `hrm-claude-config` sau khi user pull (commit `a961c2c`, 22/09 12:06). 5 điểm ảnh hưởng
trực tiếp tới màn này:

| Thay đổi | Ở đâu | Đã xử lý |
| --- | --- | --- |
| **FormRequest mới KHÔNG khai `messages()`** cho rule phổ biến — câu chuẩn đã có ở `hrm-api/resources/lang/vi/validation.php`; chỉ khai `attributes()` để câu lỗi có tên trường | `CLAUDE.md` | ✅ đã bỏ `messages()` khỏi 2 FormRequest + 2 chỗ `validate()` inline; giữ đúng 1 câu nghiệp vụ (`status.in`) |
| **`V2BaseFilterPanel` ĐÃ BỊ XOÁ khỏi repo (21/09)**; panel duy nhất là `V2BaseSmartFilterPanel` và **luôn bật `floating`** | skill `list-page` | plan Phase 5 đã dùng panel mới → bổ sung `floating` + khuôn tham chiếu mới |
| **Khuôn tham chiếu panel lọc đổi sang `pages/master-data/product-natures/index.vue`** | skill `list-page` | Phase 5 đổi khuôn. Khuôn 4 màn tổng thể vẫn là `pages/assign/customers/` |
| **Xuất Excel có 4 mắt xích bắt buộc** (`ExportColumnRegistry` + `DynamicExport` + route `/export` trước `/{id}` + `exportRows()` dùng lại query danh sách) | skill `list-page` mục 14b | Phase 4 viết lại theo khuôn này thay vì `exportData()` tự chế |
| **Toolbar bắt buộc đủ "Xuất Excel" + "Tuỳ chỉnh cột", KHÔNG gate quyền**; thứ tự Tạo mới → Import → Xuất → Tuỳ chỉnh cột | skill `list-page` | Phase 5 ghi rõ |

Ba điểm nhỏ hơn đã ghi vào `plan.md`: select chọn 1 **mặc định có dấu ×** (không khai
`allowClear`), slot `#field-*` **không tự vẽ `V2BaseLabel`**, khối Lịch sử trong popup theo
`modal-popup` mục 3c.

**Line ending** — 2 repo code đã chuẩn hoá **LF** từ 18/09 và có `.gitattributes`, không phải giữ
CRLF nữa. Đã kiểm bằng `file`: mọi file BE của màn này đang là LF. Riêng `hrm-claude-config`
**không có `.gitattributes`** và máy đặt `core.autocrlf = true` nên tài liệu vẫn là CRLF — sửa
`STATUS.md` phải giữ CRLF như cũ.

## Rủi ro đã biết

- **`cost_id` khai `varchar(255)`** trong khi `costs.id` là số — ép kiểu cẩn thận khi join.
- **`supplier_name` trong `buy_service_request_details` toàn NULL** trên dữ liệu thật (chỉ
  `supplier_code` có giá trị) → màn chi tiết phải lấy tên qua quan hệ `supplier`, đừng tin cột lưu sẵn.
- **DB local khác prod**: 81 phiếu ở local, 71/81 đã ở trạng thái *Đã lập hợp đồng* — ít mẫu ở các
  trạng thái đầu. Test 2 nấc duyệt phải tự tạo phiếu mới.
- Màn này **không có trong sheet quy hoạch tách phân hệ** (sheet chỉ quét menu *Kế toán*, còn YCMDV
  chỉ nằm ở menu *Khởi tạo* và *Mua hàng*). User đã xác nhận miệng thuộc phân hệ **Bán hàng**.
