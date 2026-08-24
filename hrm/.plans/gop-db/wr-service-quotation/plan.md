# Plan — Phiếu cung cấp thông tin làm báo giá (chứng từ 3)

> @namdangit · nhánh `gop_db` · phạm vi đã chốt ở `design.md` mục 8: **chỉ chứng từ 3**,
> tính tiền ở FE, giữ dữ liệu bảo hành nhưng chưa dựng màn Phiếu bảo hành.

## Phase 0 — Nền tảng
- [x] Rà 12 bảng ERP trên DB gộp, xác nhận không cần migration
- [x] Thêm 3 quyền xem vào `PermissionsTableSeeder` (id 1515–1517); quyền LẬP tái dùng id 1514
- [x] Khai 2 bảng chính + con vào `CatalogHistoryService::TABLES` cho Lịch sử

## Phase 1 — BE Entity
- [x] `WrServiceQuotation` (trạng thái, màu, canEdit/canView/canCreateQuotation/canDelete, generateCode)
- [x] 8 entity con (product, product_item, product_service, 3 bảng device_error, extend_product + service + item, cost)
- [x] Quan hệ + scope theo `type`

## Phase 2 — BE Service
- [x] `WrServiceQuotationService`: filteredQuery + 3 scope (mine / all / waiting_create_quotation)
- [x] `prefillFromHandleRequest()` — dựng dữ liệu từ Phiếu xử lý (tách dòng theo `device_error_old`)
- [x] `deviceErrorDetails()` — định mức công + vật tư + dịch vụ theo từng lỗi thiết bị
- [x] `store/update` + sync 3 cấp bảng con
- [x] `applyStatusSideEffects()` — đóng dấu ngược 2 chứng từ trước
- [x] `delete()` — trả trạng thái 2 chứng từ trước, xoá đủ 7 bảng con
- [x] `reject()` (Từ chối tiếp nhận)

## Phase 3 — BE Controller / Request / Resource
- [x] Request validate theo trạng thái
- [x] Controller: index, prefill, show, store, update, delete, unApprove, optionsData, exportRows, printData, printListData
- [x] 2 Resource (list + detail)
- [x] Notifier `[PCCTT]`

## Phase 4 — FE module tính tiền dùng chung
- [x] `utils/wrServiceQuotationMoney.js` — port công thức ERP
- [x] Đối chiếu số học với dữ liệu ERP thật

## Phase 5 — FE màn danh sách
- [x] `pages/customer-care/wr-information-requests/index.vue` (7 cột mặc định + Khách hàng)
- [x] Bộ lọc, xuất Excel chia trang, in danh sách, Lịch sử
- [x] Gắn menu phân hệ CSKH

## Phase 6 — FE màn form + chi tiết + in
- [x] Form 4 khối A/B/C/D theo ERP, toàn bộ V2Base*
- [x] Popup chọn lỗi thiết bị / vật tư / dịch vụ
- [x] Chi tiết + In phiếu (khung giấy chuẩn)

## Phase 7 — Kiểm thử & tài liệu
- [x] Test luồng BE đối chiếu ERP (API thật trên DB gộp)
- [x] Test giao diện thật trên cổng 3002 (trọn luồng, tìm & sửa 2 lỗi)
- [ ] testcase.xlsx (HRM + ERP) + mô tả nghiệp vụ — **chỉ làm khi user yêu cầu**


### Checkpoint — 2026-08-21
Vừa hoàn thành: trọn bộ chứng từ 3 (BE 8 file + FE 11 file + module tính tiền), đã chạy thử toàn
luồng bằng API thật trên DB gộp: danh sách/lọc/xuất/in · prefill · lưu nháp · gửi đi (kèm thông
báo đúng người) · từ chối tiếp nhận · xoá (trả trạng thái 2 chứng từ trước). Dữ liệu test đã dọn.
Đang làm dở: (không có)
Bước tiếp theo: chờ user chốt 2 việc — (1) có test giao diện không, (2) quyền "Xem giá vốn hàng
hoá" có cấp cho người lập phiếu không. Sau đó mới sinh testcase + mô tả nghiệp vụ.
Blocked:


### Checkpoint — 2026-08-21 (sau khi test giao diện)
Vừa hoàn thành: chạy trọn luồng trên trình duyệt — danh sách · chi tiết · lập mới từ phiếu xử lý ·
sửa số lượng · thêm dịch vụ (giá vốn tự suy từ tỉ lệ) · thêm thiết bị bảo dưỡng + gói bảo dưỡng ·
chuyển thiết bị Sửa chữa ↔ Bảo hành · lưu nháp · sửa · in phiếu · xoá · cảnh báo chưa lưu.
Số tiền trên màn hình = số tiền trên bản in = số lưu trong DB (94.825.599 trên phiếu thử).

**2 lỗi tìm ra khi test giao diện và đã sửa:**
1. Màn LẬP MỚI thiếu cột "Giá vốn" — `prefill` không trả cờ `can_view_cost_price` nên form luôn
   coi như không có quyền, trong khi màn Chi tiết lại hiện. Đã bổ sung cờ vào `prefillFromHandleRequest()`.
2. **Lưu nháp luôn thất bại** — `quotation_term` là cột `int NOT NULL` không default, màn nháp cho
   bỏ trống nên gửi `null` -> MySQL từ chối, người dùng chỉ thấy "Lưu thất bại". Đã thêm
   `fillDefaults()` bù giá trị cho toàn bộ cột NOT NULL không default (kể cả `code` lúc insert đầu).

Đã dọn: 2 phiếu thử + log lịch sử + thông báo; 2 chứng từ trước trả về đúng trạng thái ban đầu.
Bước tiếp theo: sinh testcase (HRM + ERP) + mô tả nghiệp vụ khi user yêu cầu.
Blocked:

### Checkpoint — 2026-08-21 (sửa chữ trên nút)
Đổi nút gửi phiếu từ "Lưu và gửi duyệt" sang **"Lưu và gửi"** (`V2Footer` có sẵn
`send_and_submit_form`, không phải sửa component dùng chung như tôi nhận định lúc đầu).
Chạy lại trọn luồng gửi phiếu: validate chặn đúng 2 ô bắt buộc khi gửi (không chặn lúc Lưu nháp),
popup xác nhận đúng chữ, phiếu sang "Chờ làm báo giá", 2 chứng từ trước đóng dấu đúng, thông báo
bắn đúng người yêu cầu. Dữ liệu thử đã dọn.
Blocked:

### Checkpoint — 2026-08-21 (test kỹ toàn màn)
Chạy **10 bảng kiểm** trên dữ liệu thật (DB gộp `local_hrm_erp`), 3 vai: người lập phiếu CCTT (13,
Super admin) · người lập Phiếu yêu cầu (235) · nhân viên KHÔNG quyền (789).

| Bảng | Nội dung | Kết quả |
| --- | --- | --- |
| 1 | Quyền & bảo mật — 10 phép thử trên phiếu nháp | đúng cả 10 (403/423/400) |
| 2 | Quyền trên phiếu ĐÃ GỬI + từ chối sai người | đúng |
| 3 | Validate — 11 ca (thiếu trường, trạng thái lạ, id không tồn tại, số âm, trùng serial) | đúng cả 11 |
| 4 | Round-trip: lưu rồi đọc lại, đối chiếu TỪNG trường kể cả lồng 3 cấp | khớp hoàn toàn |
| 5 | Tiền: giao diện (JS) vs máy chủ (PHP) trên **244 phiếu thật** | khớp tuyệt đối 5/5 chỉ tiêu |
| 6 | Bản in phiếu: đủ 8 khối, số khớp màn hình, gói SL=0 bị loại, bằng chữ | đúng |
| 7 | Danh sách: 16 bộ lọc · sắp xếp 3 cột · phân trang · trần `limit` 100 · xuất file · in danh sách khổ ngang | đúng |
| 8 | 3 phạm vi `?type=` × 3 vai + ẩn phiếu nháp người khác | đúng |
| 9 | Lịch sử: 3 nhóm hành động cố định, 4 ô lọc, timeline mới→cũ, ghi lý do từ chối | đúng |
| 10 | Giao diện: cấu hình cột · chi phí tự tính · thêm/xoá dòng con · URL trực tiếp | đúng |

**2 lỗi tìm ra và đã sửa trong đợt này:**
1. Ô **Số lượng nhận cả chữ và số âm** — tiền không vỡ (mọi phép tính qua `num()`) nhưng màn hiện
   "-0" và số âm gặp đơn giá > 0 sẽ **TRỪ vào tổng**; máy chủ chỉ chặn lúc bấm Lưu. Thêm
   `cleanQty()` vào module tính tiền, gắn cho cả 4 ô số lượng của 2 bảng (11 ca kiểm đều đúng).
2. Trước đó: thiếu cờ quyền giá vốn ở màn lập mới, và `quotation_term` NOT NULL làm Lưu nháp hỏng.

**Chốt chặn ERP được xác nhận lại**: 1 phiếu xử lý chỉ lập được 1 phiếu CCTT (lần 2 trả 403).

Dữ liệu thử đã dọn sạch; 3 chứng từ trở lại đúng trạng thái ban đầu.
Blocked:

## Popup chọn hàng hoá — chế độ chọn một
- [x] `ProductSearchModal` thêm prop `multiple` (mặc định `true`, giữ nguyên các màn cũ); `false` → ẩn cột checkbox + nút "Thêm N hàng hoá", bấm dòng là chọn xong
- [x] Popup "Thêm mới trang thiết bị" (chứng từ 1) và ô hàng hoá tương đương (chứng từ 2) dùng `:multiple="false"`

## Rà màn CCTT theo quy tắc mới + lỗi phát hiện khi rà (2026-08-22)
- [x] Lịch sử: bỏ track cột `status`, thêm `logStatusChanged()` → đổi trạng thái ra dòng riêng "Thay đổi trạng thái" (entity-history §3a)
- [x] Ô lọc gõ tay chờ Enter/nút Tìm kiếm (`ignoredFields` computed + `textFilterKeys`)
- [x] `:disabled` trên V2BaseButton → `:interactable` (không có tác dụng)
- [x] Thêm `$safeLoadingStart/Finish` cho mọi lệnh ghi (lưu, xoá ở cả list lẫn form, từ chối); đổi `$nuxt.$loading` → helper an toàn
- [x] Nút Xuất Excel / In danh sách không ẩn theo quyền xem
- [x] **Khối "Điều khoản báo giá" làm SAI ERP** — `quotation_term` là ID MẪU điều khoản (bảng `quotation_terms` type=3) chứ không phải số ngày hiệu lực; `footer` là HTML phải dùng CKEditor. Đã sửa: select mẫu ở `#actions` của khối + CKEditor + đổi mẫu đổ `content` (đúng `changeFooter()` của ERP); màn xem render HTML
- [x] **Xuất Excel treo ~57s** — `canCreateQuotation()` bắn 4+ truy vấn/dòng và bị gọi 2 lần/dòng (N+1). Đã nhớ kết quả trong bản ghi + tắt tính cờ `is_can_*` khi xuất file → 2.000 dòng còn **0,41s**
- [x] Điều khoản báo giá dùng `CompactReviewEditor` (CKEditor 4 dùng chung, `remove-buttons=""` → 43 nút / 10 nhóm như màn Báo giá), KHÔNG dùng CKEditor 5 lẻ
- [x] Biến `{{VAT_NOTE}}` được thay bằng câu thật ở CẢ màn xem (computed `footerDisplay`) lẫn bản in (BE thêm biến `VAT_NOTE` cho `fillReport`)
- [x] Popup "Chọn dịch vụ sửa chữa" nới 720px → 1100px
- [x] `V2BasePagination` đồng bộ với phân trang màn danh sách (12px `#6b7280`, en dash) — quy ước ghi ở `list-page` mục 3b-6, 3b-7

## Test trọn luồng 3 chứng từ trên 4 tài khoản (2026-08-22)
Tài khoản dựng riêng: A không quyền · B phòng tiếp nhận (xử lý) · C lập CCTT · D xem tổng công ty.
- [x] A tạo phiếu YCSCBH: danh sách rỗng lúc đầu → tạo được → chỉ mình thấy; B/C/D KHÔNG thấy phiếu nháp
- [x] Gửi thiếu dữ liệu → 422 đúng 6 trường; gửi đủ → Chờ xử lý; lịch sử 2 dòng (thông tin + trạng thái)
- [x] B/C thấy phiếu sau khi gửi (nhánh phòng tiếp nhận), D thấy theo tổng công ty; A không thao tác được
- [x] A thử Từ chối → 403; B từ chối thiếu lý do → 422; có lý do → về Đang tạo, lịch sử ghi kèm lý do
- [x] Chuyển phòng tiếp nhận sang phòng khác → B mất quyền xem luôn (403); D không có quyền xử lý → 403
- [x] B lập Phiếu xử lý: A/C bị chặn prefill; gửi thiếu Nguyên nhân/Hành động → 422; gửi đủ → YCSCBH=Đã xử lý, PXL=Chờ CCTT
- [x] C lập CCTT: A/B bị chặn; tạo → gửi → YCSCBH=Đã CCTT, PXL=5, CCTT=Chờ làm báo giá; lập lần 2 trên cùng PXL → 403
- [x] A (người lập phiếu yêu cầu) Từ chối tiếp nhận CCTT → cả 3 phiếu lùi trạng thái, lịch sử ghi lý do
- [x] Xoá CCTT → chuỗi phiếu quay lại Chờ CCTT, lập lại được; A xoá phiếu người khác → 403; xoá phiếu đã gửi → 400
- [x] Bộ lọc CCTT (từ khoá / trạng thái / khách hàng / khoảng ngày) đúng số liệu; phiếu nháp người khác không lọt
- [x] C không có quyền xem giá vốn → bảng KHÔNG hiện cột giá vốn (fail-closed)
- [x] UI bằng chính tài khoản C: tạo/sửa/gửi/xem/in/xuất Excel/lịch sử — 0 lỗi console; Excel chỉ ra phiếu của mình + có letterhead
- [x] Bản in khớp số tiền trên màn (135.082.747), biến `{{VAT_NOTE}}` đã thay, tiền bằng chữ đúng
Dữ liệu test đã xoá sạch; 4 role test đã gỡ.

## Thanh cuộn ngang trên+dưới — rà 3 luồng (2026-08-22)
- [x] `V2BaseDataTable`: thanh trên có nhưng **bề rộng lạc hậu** (bảng 1320px / thanh 1140px) → thêm `ResizeObserver` (bảng + khung) và hook `updated()`. Áp cho MỌI màn danh sách toàn hệ thống
- [x] Popup "Chọn hàng hóa áp dụng" (`ProductSearchModal`) và "Chọn dịch vụ sửa chữa" (`CostSearchModal`) chưa có thanh trên → bọc `V2BaseTableScroll`
- [x] Đo lại: 3 màn danh sách + 6 bảng màn CCTT + form/chi tiết 2 màn kia + 2 popup — đều đủ 2 thanh, kéo thanh trên bảng chạy theo và ngược lại
- [x] Quy ước bổ sung: `list-page` mục 3b-8 (thanh trên phải đồng bộ bề rộng, không chỉ "có mặt")

## Bản in: popup + letterhead (2026-08-22)
- [x] BE: 3 service in thiếu biến `{{HEADER}}` → bản in trống phần đầu. Thêm trait `PrintsCompanyLetterhead` (lấy theo `company_id` chứng từ; bản in danh sách lấy công ty người đăng nhập), áp cho cả 3 màn × (chi tiết + danh sách)
- [x] FE: `components/print/ReportPrintPreviewModal.vue` + `utils/mixins/reportPrintPreviewMixin.js` — nút In mở POPUP thay vì tab `/print` mới; nút In nằm cạnh tiêu đề popup, in qua cửa sổ riêng, chờ ảnh letterhead tải xong
- [x] Cỡ chữ bám bản in báo giá: văn bản 13px / bảng 10px; ép `font-size` inline của CKEditor (18px) về 13px
- [x] Áp cho 6 đường in: 3 chứng từ + 3 danh sách; đo lại đều có letterhead, đúng 2 cỡ chữ, 0 lỗi console
- [x] Quy ước: `print-page` mục 8 + 8a
- [x] Gộp CSS xem trước + bản in về MỘT nguồn `utils/print/reportPrintStyle.js` (trước đó 2 khối riêng nên xem trước và in lệch nhau). Đo tự động: so `getComputedStyle` 17 thuộc tính từng phần tử giữa popup và trang in → **lệch 0**
- [x] Tiêu đề phiếu 17px (trước bị rule ép cỡ chữ kéo xuống 10px), bảng bố cục 13px / bảng dữ liệu 10px
- [x] Giảm khoảng trống: `line-height 1.25`, ẩn `p:empty`/`div:empty`/`br+br`, `p` margin 2px
- [x] Chỗ ký: `markSignatureSpace()` gắn class cho dòng trống giữa chức danh và tên → cao 56px (trước 15px)
- [x] Ẩn rác do tiện ích trình duyệt chèn (`chrome-extension://…`, `.ddict_btn`)
