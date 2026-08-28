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

## Testcase màn ERP (2026-08-24)
- [x] Viết testcase màn ERP "Phiếu cung cấp thông tin làm báo giá" (`warranty_repair_information_requests`): `gen_testcase_erp.py` → `testcase - Phiếu cung cấp thông tin làm báo giá (ERP).xlsx` — 124 TC, P0 67%, đủ 9 mục mô tả + 9 TC phân quyền + 11 section

## Chứng từ 4 — Báo giá dịch vụ (2026-08-24)
- [x] Khảo sát màn ERP `warranty_repair_service_quotations` (controller 883 dòng, form 1.399 dòng, model dùng chung) → `design-phase2.md`
- [x] Đếm dữ liệu thật DB gộp: 5.170 phiếu · 77% lập độc lập · 812 phiếu có hàng hoá · has_warranty chỉ 1 bản ghi
- [x] Xác định 3 chỗ tầng chung còn hard-code `TYPE_INFORMATION` (service dòng 120/779/807) + hằng `PERM_*`
- [ ] Chốt 7 câu ở `design-phase2.md` mục 9 (nhánh bảo hành · checkDueConfigs · quyền tạo · sao chép · 3 mẫu in · chữ trên nút · validate lưu nháp)
- [ ] Lên plan chi tiết BE/FE sau khi chốt

### Đã chốt 2026-08-24
- [x] 7 câu ở design-phase2.md mục 11: bảo hành làm ngay đợt này · checkDueConfigs phase sau · KHÔNG gate quyền tạo báo giá · sao chép giữ như ERP · làm đủ 3 mẫu in + checklist · nút "Lưu và duyệt" · lưu nháp nới validate
- [x] Khảo sát bổ sung Phiếu bảo hành → design-phase2.md mục 12-13 (100% sinh từ CCTT, 100% ở trạng thái Đã duyệt → màn chỉ cần danh sách + xem)

### Thứ tự làm (user duyệt 2026-08-24)

#### Bước 0 — tách tầng chung theo `type` (BE, không đổi hành vi chứng từ 3)
- [x] `WrServiceQuotationService`: đưa `TYPE_INFORMATION` ở 3 chỗ (truy vấn danh sách · store · update) về 1 method `documentType()` cho lớp con ghi đè
- [x] `WrServiceQuotationService`: bộ 3 quyền xem đọc qua method `viewPermissions()` thay vì hằng `PERM_*` cứng của CCTT
- [x] Chạy lại luồng chứng từ 3 (danh sách 4.980 phiếu type=0, cờ quyền nguyên vẹn, lưu nháp + gửi đi chạy đúng)

#### Bước 1 — Phiếu bảo hành (BE + FE)
BE
- [x] 5 entity `Modules/CustomerCare/Entities/WrServiceContract/`: `WrServiceContract` (tách nhánh theo `type` NGAY, 3 bộ trạng thái riêng) + `Product` + `ProductItem` + `ProductService` + `Cost` + 3 bảng `*DeviceError`
- [x] `WrWarrantyService`: danh sách (gate 3 cấp quyền + phiếu của mình) · chi tiết · bộ lọc · cờ `is_can_*` fail-closed
- [x] `WrWarrantyController` + 2 Resource (list + detail) + route `/customer-care/wr-warranties`
- [x] 3 quyền xem (id 1542–1544) vào `PermissionsTableSeeder` (KHÔNG migration)
- [x] Nối `createWrWarranty()` vào chứng từ 3: khi gửi đi mà có dòng khối A → sinh phiếu bảo hành (mã `<CTY>.PBH.<năm>.<số>`, trạng thái Đã duyệt, chép dòng hàng + chi phí), đóng dấu `has_warranty` / `status_warranty` lên phiếu CCTT, bắn thông báo cho người lập
BE — verify
- [x] `php -l` sạch; **đối chiếu 30 phiếu thật: 0 lệch** (13 chỉ tiêu/phiếu: tiền, số dòng, khách hàng, 7 nhóm khối `warranty`)
- [x] Lập thử 1 phiếu CCTT có dòng bảo hành trên DB gộp → phiếu bảo hành sinh đúng, dọn dữ liệu test sau khi xong
FE
- [x] `pages/customer-care/wr-warranties/index.vue` — danh sách theo khuôn màn CCTT (V2BaseDataTable, badge màu do BE trả, thanh cuộn trên+dưới)
- [x] `pages/customer-care/wr-warranties/_id/index.vue` — màn xem chi tiết (V2BaseFormSection, V2Footer chỉ có Quay lại)
- [x] Ẩn hẳn Sửa / Xoá / Tạo phiếu giao việc (bỏ luôn cột Hành động) (không phiếu nào đủ điều kiện — xem design-phase2 mục 13.2)
- [x] 1 mục menu CSKH "Phiếu bảo hành"
- [x] Compile `.vue` sạch (template compiler)

#### Bước 2 — Báo giá Phase A (lập từ CCTT)
- [x] Entity `WrServiceQuotationMerchandise` + sync khối C
- [x] Service/Controller/Request/Resource cho `type = 1` kế thừa tầng chung ở Bước 0
- [x] VAT + hiệu lực báo giá (số ngày) · tệp đính kèm mới ĐỌC được, chưa đính thêm được
- [x] 3 quyền xem báo giá vào seeder; KHÔNG gate quyền tạo (đã chốt)
- [x] Mở rộng `utils/wrServiceQuotationMoney.js`: hàng hoá + VAT, đối chiếu số học với dữ liệu ERP thật
- [x] FE màn danh sách + form + xem
- [x] Popup chọn mẫu in (3 mẫu + In kèm checklist)
- [x] Nối nút "Tạo báo giá dịch vụ" ở màn CCTT (đang bắn toast)

#### Bước 3 — Báo giá Phase B (lập độc lập)
- [ ] Chọn khách hàng / người liên hệ / địa chỉ sửa chữa
- [ ] Thêm thiết bị thủ công từ danh mục thiết bị của khách · thiết bị tương đương · tạo lỗi thiết bị ngay trong form
- [x] Sao chép báo giá

#### Bước 4 — lệnh chạy nền hết hiệu lực báo giá (00:30 hằng ngày)
- [x] Command + lịch chạy + kiểm trên dữ liệu thật (chưa chạy thật — chờ user duyệt, xem cuối file)

### Checkpoint — 2026-08-24
Vừa hoàn thành: **Bước 0 + Bước 1 (Phiếu bảo hành) — BE và FE, chưa chạy thử trên trình duyệt**
Đang làm dở: không có
Bước tiếp theo: user xem thử màn `/customer-care/wr-warranties` trên cổng dev → OK thì sang Bước 2 (Báo giá Phase A)
Blocked: 

Khác biệt CÓ CHỦ Ý so với ERP ghi thêm ở bước này:
- **Chặn sinh trùng phiếu bảo hành**: ERP gọi `createWrWarranty()` ở cả `store()` lẫn `update()` không kiểm gì → phiếu bị Không duyệt rồi gửi lại sẽ đẻ thêm phiếu bảo hành thứ 2. HRM chỉ sinh ĐÚNG 1 phiếu cho mỗi phiếu CCTT (đã test: gửi lại lần 2 vẫn 1 phiếu).
- **Khối tiền `warranty` tính ở máy chủ**, không nhận từ giao diện như ERP (dùng `WrServiceQuotationPrintService`).
- **Không tính `net_price` / `standard_price`** cho dòng thiết bị: đo 4.364 dòng thật của ERP thì cả 2 cột đều bằng 0.
- Bỏ 3 entity `*DeviceError` của hợp đồng: 3 bảng rỗng 0 dòng và luồng sinh phiếu bảo hành không đụng tới.

Lưu ý khi bàn giao: 3 quyền mới đã được cấp cho vai trò Super admin **trên DB local** để test; môi trường khác phải chạy lại seeder.

## Redmine #11210 — Bộ lọc + nhãn cột (2026-08-24)
- [x] Đổi "Người lập phiếu / Ngày lập phiếu" → "Người tạo / Ngày tạo" ở ĐỦ 5 nơi: cột bảng danh sách · ô lọc (gồm "Ngày tạo từ/đến") · placeholder ô tìm nhanh · popup chọn trường xuất file · nhãn cột file Excel (`app/ExcelExport/ExportColumnRegistry`) · tiêu đề cột bản in danh sách (`WrServiceQuotationPrintService`)
- [x] Hiện MẶC ĐỊNH cột "Trạng thái bảo hành" (ERP `index.blade.php` để 2 cột Trạng thái + Trạng thái bảo hành cạnh nhau) — thiếu nó thì không thấy phiếu nào ở "Chờ tạo phiếu bảo hành". Đổi `key` `status_warranty` → `warranty_status` (kèm slot `#cell-warranty_status`) để cấu hình cột ĐÃ LƯU của user coi đây là cột MỚI mà hiện lại — khuôn ở skill `list-page` mục 6
- [x] Bỏ ô lọc "Dịch vụ"
- [ ] **Mục 4 (bộ lọc Công ty–Phòng ban không hiện) — CHƯA sửa, cần tài khoản của người test.** Khối này render qua slot `#field-org` → `V2BaseCompanyDepartmentFilter`, mà component đó có `v-if` riêng theo cờ quyền: ô "Công ty" chỉ hiện khi `is_all_company`, ô "Phòng ban" hiện khi có 1 trong 3 cờ. Cờ lấy từ `wr-information-requests/options` → `WrServiceQuotationService::scopeFlags()` → `WarrantyRepairPermission::has()`. Vì field khai `hideLabel: true` nên quyền thiếu là mất trắng, không còn nhãn nào để nhận ra.
  - Phát hiện đáng ngờ trên DB gộp: quyền **trùng tên ở 2 guard** — `Xem phiếu cung cấp thông tin theo tổng công ty` có id **1515 (guard api, 1 vai trò)** và **100429 (guard web, 7 vai trò)**. Nếu màn phân quyền ghi vào bản `web` thì `getAllPermissions()` (guard api) không thấy → cờ false → mất bộ lọc. Cần biết tài khoản/vai trò người test dùng để xác nhận rồi mới sửa (đụng vào tầng phân quyền, không đoán)

## Redmine #11204 — Check trùng serial ở Phiếu YCSCBH (2026-08-24)
Trước đó chỉ chặn trùng `serial_id` (chọn từ danh mục); đường "Nhập serial tạm" (gõ tay) không kiểm gì.
ERP cũng KHÔNG có check này — đây là yêu cầu mới, bê 2 điều kiện của màn Danh mục khách hàng
(`CustomerManagerService::addSerial`) sang.
- [x] `WarrantyRepairRequestRequest::withValidator()`: (1) serial gõ tay trùng nhau giữa các dòng trong cùng phiếu; (2) serial gõ tay đã có trong danh mục `serials` → báo "vui lòng chọn từ danh sách". So sánh bỏ qua hoa/thường + khoảng trắng thừa; 1 truy vấn `whereIn` cho cả bảng, không hỏi từng dòng
- [x] Lỗi bắn vào key `products.{i}.serial` — FE đã có sẵn `serialError(index)` hiện inline, không phải sửa gì
- [x] Kiểm chứng bằng dữ liệu thật: 4 dòng (2 trùng nhau khác hoa/thường · 1 trùng danh mục `GL4300` · 1 hợp lệ) → ra đúng 3 lỗi vào đúng dòng, dòng hợp lệ không bị chặn

## Fix lệch cột "Loại công việc" (2026-08-24)
- [x] `WrDeviceLinesTable.vue` — dòng tiêu đề thiết bị thiếu 1 `<td>` (10/11 cột khi không có quyền giá vốn, 11/12 khi có) nên select Sửa chữa/Bảo hành tụt sang cột "Thành tiền sau chiết khấu". Thêm ô trống thứ 2 cho cặp cột tiền. Xác nhận trên phiếu xử lý 5287 (server hrm-crm): select đang ở cột 8, đúng phải cột 9
- [x] Bug đổi "Loại công việc" làm dòng KHÁC cũng đổi theo: `v-for` của `WrDeviceLinesTable` khoá theo CHỈ SỐ, mà `moveRow()` splice/push nên Vue tái dùng nguyên node của dòng đã chuyển đi cho dòng kế tiếp; select2 là DOM jQuery, prop `value` không đổi ('repair' vẫn 'repair') nên không vẽ lại → dòng còn lại hiện nhầm "Bảo hành". Gắn `_rowKey` cho từng dòng ở `normalizeProducts()` (không gửi lên BE, `buildProductPayload` liệt kê field tường minh) và dùng làm khoá. Verify 2 chiều trên dev local :3002 với phiếu xử lý 65 (3 dòng)

## Test Phiếu bảo hành trên trình duyệt (2026-08-25)
Phiên đăng nhập lấy bằng cách sinh mã phiên từ máy chủ cho chính tài khoản của @namdangit rồi bơm vào trình duyệt — không cần mật khẩu, không đổi dữ liệu nào.

**Tìm ra 3 lỗi, đã sửa hết:**
- [x] **Bộ lọc + phân trang + sắp xếp KHÔNG chạy** (nặng nhất, 64 lỗi console): lược mixin khi dựng màn nên thiếu hẳn 8 hàm `toggleFilterPanel` / `handleQuickSearchChange` / `handleFilterChange` / `handleSearch` / `handleReset` / `handleSort` / `handlePageChange` / `handlePageSizeChange`. Chúng KHÔNG nằm trong mixin nào — màn CCTT tự khai trong `methods`. Đã bê sang.
- [x] **Sắp xếp im lặng không chạy**: service đọc `sort_by` / `sort_dir` trong khi `V2BaseDataTable` gửi `sort_field` / `sort_type` (khuôn của `WrServiceQuotationService`). Bấm tiêu đề cột vẫn đổi mũi tên nhưng thứ tự dòng không đổi — không có lỗi nào báo ra.
- [x] **Mở phiếu không tồn tại ra trang trống**: nay báo rõ ("Không tìm thấy…" / "Bạn không có quyền…") rồi đưa về danh sách.
- [x] Đồng bộ nhãn với Redmine #11210: "Người lập phiếu / Ngày lập phiếu" → **Người tạo / Ngày tạo** (cột bảng, ô lọc, ô lọc ngày)

**Đã kiểm và đạt:**
- Máy chủ 15 nhóm: phân trang · chỉ lấy đúng loại chứng từ · 4 trạng thái · lọc theo số phiếu CCTT / khách hàng / serial / khoảng ngày · sắp xếp 3 cột · phạm vi "phiếu của tôi" · giá trị lọc lạ · id không tồn tại (404) · id của hợp đồng dịch vụ (404) · người không quyền (danh sách 0 phiếu, mở thẳng phiếu bị chặn) · chưa đăng nhập (401)
- Giao diện: danh sách 3.631 phiếu, 7 cột, không nút Tạo mới, không cột Hành động · sang trang 2 · đổi 25 dòng/trang · sắp xếp mã và tiền · tìm nhanh · lọc trạng thái · Làm mới · popup Tuỳ chỉnh cột · menu CSKH có mục Phiếu bảo hành đi đúng đường dẫn
- Màn chi tiết: 3 khối, 3 bảng đúng cột, chỉ có nút Quay lại, link tra ngược sang phiếu CCTT đúng, **khối Tổng hợp khớp từng đồng với dữ liệu máy chủ**
- Console: **0 lỗi** ở cả màn danh sách lẫn màn chi tiết (trước khi sửa là 64)

## Bỏ ô lọc "Trạng thái bảo hành" ở màn CCTT (user chốt 2026-08-25)
Lý do: trên màn này cột đó chỉ nhận ĐÚNG MỘT giá trị. Phiếu bảo hành sinh ngay lúc bấm "Lưu và gửi"
nên không tồn tại quãng "Chờ tạo phiếu bảo hành". Đếm dữ liệu thật: **3.631 "Đã tạo phiếu bảo hành"
/ 1.349 để trống / 0 "Chờ tạo"**. Giá trị "Chờ tạo" là của màn Báo giá dịch vụ (1 bản ghi duy nhất,
dấu vết cách làm cũ). ERP cũng KHÔNG có ô lọc này — đây là ô HRM tự thêm.
- [x] FE `wr-information-requests/index.vue`: bỏ field khỏi `filterFields`, bỏ `status_warranty` khỏi bộ lọc lưu, bỏ `statusWarrantyOptions` + dòng gán trong `loadOptions`
- [x] BE `WrServiceQuotationService::filteredQuery()`: bỏ nhánh lọc `status_warranty` (thay bằng chú thích nêu lý do + số liệu)
- [x] BE `WrServiceQuotationController::optionsData()`: bỏ khoá `statuses_warranty` khỏi phản hồi
- [x] **GIỮ NGUYÊN**: cột trên bảng (Redmine #11210 yêu cầu hiện mặc định), cột trong file xuất, và `STATUSES_WARRANTY` trên Entity (dùng để đổ chữ + màu cho cột)
- [x] Verify: bộ lọc còn 9 ô, không còn khoá `status_warranty` trong bộ lọc lưu · cột vẫn hiện "Đã tạo phiếu bảo hành" · lọc Trạng thái + Làm mới vẫn chạy (3.759 / 4.980) · gọi API kèm `status_warranty=2` nay trả đủ 4.980 (không còn lọc) · 0 lỗi console

## Thống nhất ô lọc "Phòng ban" của cả 3 màn (user chốt 2026-08-25)
Trước: cùng một khối lọc "Công ty – Phòng ban" nhưng BA màn hiểu theo BA nghĩa khác nhau —
chứng từ 1 và 2 lọc theo phòng người lập chính phiếu đó, riêng CCTT lọc ngược về phòng của
NGƯỜI YÊU CẦU (đúng ERP). Người dùng đứng ở màn không có cách nào biết mình đang lọc theo gì.
- [x] **KHÁC ERP CÓ CHỦ Ý**: `WrServiceQuotationService::filteredQuery()` đổi từ `EXISTS(phòng người yêu cầu)` sang `wr_service_quotations.department_id` (phòng người lập phiếu CCTT, đóng dấu lúc tạo bằng `stampOrganization()`)
- [x] Đổi nhãn **mẫu in 275**: "Phòng yêu cầu" → **"Phòng cung cấp thông tin"**; đã sao lưu `storage/app/backup_report_template_275.html`
- [x] Dữ liệu đủ để lọc: 4.980/4.980 phiếu CCTT đều có `department_id`, không bản ghi nào trống
- [x] Verify đối chiếu với số đếm trên DB: phòng CSKH 4.530 · Kỹ thuật CN 364 · CSKH SG 44 — **khớp tuyệt đối**; bản in ra "Phòng cung cấp thông tin = Tất cả / = PHÒNG CHĂM SÓC KHÁCH HÀNG"
- [x] Phòng của người yêu cầu vẫn tra được ở **cột "Phòng yêu cầu"** trên lưới và trong file xuất — không mất thông tin

Sau thay đổi, cả 3 màn cùng một nghĩa: **lọc theo phòng của người lập chính phiếu đó**.
| Màn | Nhãn trên bản in danh sách |
| --- | --- |
| Yêu cầu kiểm tra SC–BH | Phòng yêu cầu |
| Phiếu xử lý yêu cầu | Phòng xử lý yêu cầu |
| Phiếu cung cấp thông tin | Phòng cung cấp thông tin |

## Bước 2 — Báo giá dịch vụ Phase A (bắt đầu 2026-08-25)
BE — nền tảng
- [x] Entity `WrServiceQuotationMerchandise` (khối C Loại hàng hoá, 1.535 dòng thật) — không khai quan hệ sang hàng hoá, mọi thứ hiển thị đã chụp sẵn vào dòng
- [x] Entity `WrServiceQuotation`: thêm bộ trạng thái RIÊNG của báo giá (`STATUSES_QUOTATION`: Đang tạo · Duyệt · Đã tạo hợp đồng · Hết hiệu lực) + 3 hằng quyền xem
- [x] **`statusTable()` rẽ theo `type`** — bẫy lớn nhất của bảng dùng chung: cùng số 2 nhưng "Chờ làm báo giá" ở CCTT và "Duyệt" ở báo giá. Verify trên dữ liệu thật: 4 trạng thái mỗi loại đều ra đúng nhãn + màu
- [x] `WrQuotationService extends WrServiceQuotationService`: ghi đè `documentType()` · `viewPermissions()` · `createPermission()` trả `null` (KHÔNG gate quyền tạo, đúng ERP) · `syncChildren()` thêm khối hàng hoá · `applyStatusSideEffects()` riêng (Duyệt = tự duyệt, đẩy trạng thái về phiếu CCTT + phiếu yêu cầu, KHÔNG bắn thông báo)
- [x] Mở tầm vực 3 hàm của lớp cha cho lớp con ghi đè: `syncChildren` · `applyStatusSideEffects` · `fillDefaults`
- [x] 3 quyền xem vào seeder — **id 1548–1550** (dải 1545–1547 đã bị nhóm Phiếu bảo hành chiếm sau merge)
- [x] Verify: service đọc đúng 3.586 báo giá trong phạm vi quyền của tài khoản test, nhãn trạng thái đúng, `can_create = true`

BE — tiếp (2026-08-25)
- [x] `prefillFromInformation()`: chép nội dung phiếu CCTT sang form báo giá + **nạp VAT từ DANH MỤC** — công lấy `device_errors.vat_percent`, vật tư `products`, dịch vụ `costs`, gói bảo dưỡng `services`. Phiếu CCTT không có cột VAT nào nên đây là việc cốt lõi của bước lập báo giá
  - KHÁC ERP về CÁCH LẤY, không khác kết quả: ERP gọi `Product::findOrFail()` ngay trong vòng lặp từng dòng (N+1); ở đây gom id tra 1 lượt mỗi danh mục
  - Verify: **10 phiếu thật, 108 dòng, LỆCH 0** so với danh mục
- [x] `canEdit()` rẽ theo `type`: báo giá chỉ sửa được khi "Đang tạo" và là người lập (ERP `canEditQuotation()`), bỏ ngoại lệ quản trị viên như đã chốt từ chứng từ 2
- [x] `canView()` rẽ **bộ 3 quyền xem** theo `type` — 2 màn dùng chung bảng nhưng khác bộ quyền
- [x] Verify: 7 tổ hợp type × trạng thái ra đúng cờ sửa và đúng nhãn; báo giá nháp của người khác `canView = false`

BE — hoàn tất phần ghi/đọc (2026-08-25)
- [x] `WrQuotationRequest extends WrServiceQuotationRequest`: bộ trạng thái riêng · khối hàng hoá · `date_of_entering` (số NGÀY, min 1) · tệp đính kèm · phiếu CCTT gốc để TUỲ CHỌN cho Phase B
  - Mở tầm vực `isSending()` ở lớp cha thành `protected` và ghi đè hẳn — KHÔNG dựa vào việc 2 bộ trạng thái tình cờ trùng con số 2
- [x] `WrQuotationListResource` + `WrQuotationResource`: cột theo ERP, thêm `expired_at` tính sẵn (ngày lập + số ngày), khối hàng hoá, tách chuỗi tệp đính kèm
- [x] Entity: 2 quan hệ `merchandises()` / `informationRequest()` + `attachments` vào `fillable`
- [x] `WrQuotationController` + 7 route `/customer-care/wr-quotations` — **KHÔNG gắn `checkPermission` cho store/update/delete** (đúng ERP, user chốt)
- [x] Ghi đè `delete()`: trả phiếu CCTT gốc về "Chờ làm báo giá" (lớp cha trả nhầm sang trạng thái của luồng chứng từ 3). KHÁC ERP: dọn sạch dòng con thay vì để mồ côi

**2 lỗi tìm được khi chạy thử luồng, đã sửa:**
- [x] Prefill trả cả trường CHỈ ĐỂ HIỂN THỊ (`approved_time` dạng `28/07/2026 08:32`) mà cột đó lại nằm trong `fillable` → `fill()` ném lỗi Carbon. Lọc bỏ 15 khoá hiển thị trước khi trả về
- [x] **Giá vốn null làm lưu vỡ** — lỗi nặng nhất: người lập báo giá chính là người lập Phiếu yêu cầu (kinh doanh), họ thường KHÔNG có quyền "Xem giá vốn hàng hoá"; Resource che giá vốn thành `null`, cột `engineering_work` là NOT NULL → vỡ ngay dòng đầu. Không thể bắt giao diện gửi số nó không có → **máy chủ tự chép giá vốn từ phiếu CCTT gốc** (ghép dòng theo lỗi thiết bị + hàng hoá + serial). Giá vốn không đi qua giao diện: vừa lưu đúng vừa không lộ

Verify luồng thật (tạo → duyệt → xoá, rollback sạch):
| Bước | Kết quả |
| --- | --- |
| Lưu nháp | sinh `TPE.BGDV.2026010355`, trạng thái Đang tạo, khối hàng hoá lưu đúng |
| → phiếu CCTT gốc | Đang báo giá |
| Lưu và duyệt | Duyệt, đóng dấu người + ngày duyệt, khoá không sửa được nữa |
| → phiếu CCTT / phiếu yêu cầu | Báo giá đã duyệt / Đã báo giá |
| Xoá báo giá nháp | phiếu CCTT trả về Chờ làm báo giá, 0 dòng con mồ côi |

Verify API: danh sách 3.586 phiếu · options 4 trạng thái · chi tiết · id sai loại chứng từ → 404 · prefill thiếu tham số → 400, phiếu không đủ điều kiện → 403 · người không quyền chỉ thấy phiếu của mình, mở thẳng → 403 · chưa đăng nhập → 401 · sửa/xoá báo giá đã khoá → 423

BE — còn lại
- [x] Thêm ô lọc **Người duyệt** (`approved_id`) — chỉ màn báo giá mới có, ERP có ô này
- [x] Bản in 3 mẫu + tuỳ chọn In kèm checklist bảo dưỡng (xem mục riêng cuối file)
- [x] Nhận tệp đính kèm khi lưu (tải lên S3)

FE (2026-08-25)
- [x] Mở rộng `utils/wrServiceQuotationMoney.js`: `merchandiseTotals()` (hàng hoá — không chiết khấu, VAT theo từng dòng) + `quotationGrandTotal()` (tổng của báo giá, **không cộng phần bảo hành**)
  - **Đối chiếu 101 báo giá ERP thật, trong đó 40 phiếu có khối hàng hoá: tính lại từ dòng chi tiết ra đúng cả 3 cột tiền đã lưu, LỆCH 0**
  - Khối bảo hành: dữ liệu không phân định được (mọi phiếu đều 0 đồng) → theo mã ERP, dòng "Bảo hành" bị comment khỏi bảng tổng
- [x] Màn danh sách `/customer-care/wr-quotations` — cột + bộ lọc bám ERP (`service_quotations/index.blade.php`), hành động Sửa · Xoá · Lịch sử
- [x] `WrMerchandiseTable.vue` — khối "C - Loại hàng hóa", đổi ĐVT là đổi luôn đơn giá theo bảng giá (đúng `changeUnit()` của ERP)
- [x] `WrQuotationForm.vue` — **kế thừa form Phiếu cung cấp thông tin** (`extends`) nên dùng lại nguyên bộ xử lý dòng, chỉ ghi đè phần khác: khối hàng hoá · hiệu lực báo giá · bảng tổng không cộng bảo hành · 2 nút "Lưu nháp" / "Lưu và duyệt"
- [x] 3 trang: lập mới · sửa · xem chi tiết (vào màn Sửa khi đã duyệt thì chuyển về Chi tiết)
- [x] Thêm mục menu "Báo giá dịch vụ" vào phân hệ CSKH
- [x] Nối nút "Tạo báo giá dịch vụ" ở màn CCTT (danh sách + màn chi tiết) — trước đây chỉ bắn toast
- [x] Popup chọn mẫu in
- [x] Đính THÊM tệp mới
- [x] 2 cột "Tồn dự kiến" / "Đang giữ" của bảng hàng hoá

Verify FE (2026-08-25) — chạy thật qua API bằng đúng dữ liệu form dựng ra:
| Bước | Kết quả |
| --- | --- |
| Prefill từ phiếu `TPE.PCCTT.2026010301` | 1 dòng sửa chữa + 5 dòng chi phí, VAT 8% nạp đúng, mã để trống |
| Lưu nháp kèm 1 hàng hoá (2 × 341.000.000) | `TPE.BGDV.2026010357`, tiền lưu **683.023.500 / 54.641.880 / 737.665.380** — khớp từng đồng với công thức giao diện |
| Hiệu lực 15 ngày | ngày hết hiệu lực 09/09/2026 (ngày lập + 15) |
| Sửa số lượng 2 → 3 rồi "Lưu và duyệt" | trạng thái Duyệt, đóng dấu người + ngày duyệt, khoá sửa; tiền cập nhật đúng |
| → phiếu CCTT gốc / phiếu yêu cầu | Báo giá đã duyệt / Đã báo giá |
| Xoá | phiếu CCTT về Chờ làm báo giá, 0 dòng con mồ côi, dữ liệu thử đã trả về nguyên trạng |

### Checkpoint — 2026-08-25
Vừa hoàn thành: toàn bộ FE màn Báo giá dịch vụ (danh sách + form + chi tiết) và module tính tiền, đã đối chiếu số học với 101 báo giá ERP thật.
Đang làm dở: chưa có.
Bước tiếp theo: bản in 3 mẫu + In kèm checklist (máy chủ), rồi popup chọn mẫu in ở giao diện; sau đó là phần tệp đính kèm.
Blocked: chưa chạy thử trên trình duyệt (chờ user xác nhận có test không).

### Rà lịch sử cho cả luồng (2026-08-25)
- [x] Rà 4 màn chứng từ: tất cả đều dùng chung `SystemInfoSection` (màn chi tiết) và `CatalogHistoryModal` (popup ở danh sách — ruột chính là `SystemInfoSection`), nên bản sửa hiển thị tệp đính kèm áp cho **cả luồng chỉ bằng một chỗ sửa**, không phải lặp lại từng màn
- [x] **Lỗi thật tìm thêm — nhãn trạng thái của báo giá bị ghi theo bộ của phiếu cung cấp thông tin**: `logStatusChanged()` map qua hằng `STATUSES` cứng, mà số `2` = "Chờ làm báo giá" của chứng từ 3 nhưng = "Duyệt" của báo giá → log ghi "Đang tạo → Chờ làm báo giá" trên phiếu đang hiện badge "Duyệt". Sửa: lấy nhãn từ `statusTable()` của chính bản ghi (rẽ theo `type`)
- [x] **Lỗi thật thứ hai — nhãn cột viết theo một loại chứng từ**: `'code' => 'Số phiếu cung cấp thông tin'` bị đóng dấu vào log báo giá. Đổi sang nhãn trung tính "Số phiếu" + khai thêm `date_of_entering` = "Hiệu lực báo giá (ngày)"
- [x] `WrQuotationService::catalogColumns()` thêm `date_of_entering` — trước đó sửa hiệu lực báo giá thì lịch sử không ghi nhận gì
- [x] Verify luồng thật: tạo → duyệt → sửa, log ra đúng **Tạo mới · Trạng thái "Đang tạo → Duyệt" · "Hiệu lực báo giá (ngày): 15 → 30"**; đã xoá bản ghi thử lẫn log của nó, phiếu gốc trả về nguyên trạng
- [x] Cập nhật `.claude/skills/entity-history/SKILL.md` §3c "Bảng chứa NHIỀU LOẠI chứng từ" + 1 dòng checklist

**Còn thiếu, chưa làm (cần user chốt):** màn **Phiếu bảo hành** hiện KHÔNG có lịch sử ở cả hai lớp — `WrWarrantyService` không dùng `LogsCatalogHistory`, bảng `wr_service_contracts` chưa nằm trong whitelist, giao diện chưa có popup lẫn khối lịch sử.

### Test trên trình duyệt — màn Báo giá dịch vụ (2026-08-25, Playwright)

Chạy thật với 2 tài khoản (người có 773 báo giá để soi danh sách, người lập phiếu yêu cầu để lập mới). **0 lỗi console** ở mọi màn.

| Hạng mục | Kết quả |
| --- | --- |
| Danh sách 773 phiếu | cột + badge trạng thái đúng; hành động ẩn/hiện khớp trạng thái (phiếu "Đang tạo" có Sửa+Xoá, phiếu đã duyệt chỉ còn Lịch sử) |
| Tìm nhanh theo số báo giá | 1/1 đúng phiếu |
| Lọc Trạng thái = Duyệt | 20 phiếu — **khớp tuyệt đối** với đếm trực tiếp trên dữ liệu; chọn xong tự tìm luôn, không phải bấm Tìm kiếm |
| Sắp xếp Số báo giá | đổi chiều 2 lần đều đúng; sang trang 2 vẫn giữ bộ lọc |
| Chi tiết phiếu có hàng hoá | 6 khối đúng thứ tự; tổng hợp **6.256.764** khớp từng đồng với số ERP đã lưu |
| Nút "Tạo báo giá dịch vụ" ở phiếu cung cấp thông tin | dẫn thẳng sang form lập, dữ liệu điền sẵn đủ |
| Thêm hàng hoá qua popup dùng chung | thêm đúng dòng, tiền cập nhật tức thì |
| Đổi số lượng 1 → 3 | dòng và bảng tổng tính lại đúng ngay (11.149.380) |
| "Lưu và duyệt" khi thiếu hiệu lực báo giá | máy chủ chặn, lỗi đỏ "Bắt buộc phải nhập" hiện ngay dưới ô, không rời trang |
| Lưu nháp → sửa → Lưu và duyệt | tiền lưu khớp số trên màn; đóng dấu người + ngày duyệt; phiếu cung cấp thông tin → "Báo giá đã duyệt" |
| Vào URL màn Sửa khi đã duyệt | tự chuyển về màn Chi tiết, chỉ còn nút Quay lại |
| Popup Lịch sử ở danh sách | ghi đúng "Đang tạo → Duyệt" (nhãn theo loại chứng từ, bản sửa hôm nay) |
| Xoá báo giá nháp từ giao diện | popup xác nhận đúng chuẩn; xoá xong phiếu gốc về "Chờ làm báo giá", 0 dòng con mồ côi |
| Cảnh báo "chưa lưu" khi Quay lại | hiện đúng popup "Bạn có thông tin chưa lưu…" |

Dữ liệu thử đã dọn sạch: tổng báo giá trở lại **5.170** như trước khi test, log thử đã xoá, trạng thái phiếu gốc trả nguyên trạng.

**4 lỗi tìm được khi test, đã sửa ngay:**
- [x] **Tiền lẻ không làm tròn** trên lưới — hiện "3.045.027,6" trong khi ERP in số nguyên. `formatMoney` gọi thẳng `toLocaleString`. Sửa: dùng `money()` dùng chung ở **cả 3 màn** (báo giá + danh sách và chi tiết phiếu bảo hành cũng dính)
- [x] **Cột "Mã hàng" và "ĐVT" trống** ở khối hàng hoá — bảng dòng chỉ lưu `product_id`/`unit_id`. Thêm `attachMerchandiseInfo()` bồi mã hàng + tên đơn vị + danh sách đơn vị kèm giá (2 truy vấn cho cả phiếu, không N+1)
- [x] **Cột "Model" trống khi mở lại phiếu** — lúc lưu không ghi `model_name` (ERP trông chờ giao diện gửi kèm). Sửa: **máy chủ tự tra** model / hãng / xuất xứ từ danh mục hàng hoá lúc lưu, form chỉ cần gửi hàng hoá + số lượng + đơn giá
- [x] Bồi thêm ô lọc **Người duyệt** (`approved_id`) cho khớp ERP

**Không phải lỗi** (đã kiểm lại): popup chọn hàng hoá cố ý không tự đóng sau khi thêm — đúng khuôn dùng chung của màn báo giá.

### Sửa lỗi: in xong thì ô lọc select2 không bấm được (chỉ trên Windows) — 2026-08-25
- [x] Nguyên nhân: popup xem trước in bằng `window.open('', '_blank')` + `win.print(); win.close()`. Cửa sổ in con đóng lại nhưng cửa sổ HRM chưa lấy lại focus của hệ điều hành; select2 mở dropdown theo focus và tự đóng khi mất focus → mọi cú bấm vào ô lọc đều không ăn. **Mac không tái hiện được** (đã dựng lại đúng luồng trên Chromium/Mac: bình thường) nên phải sửa theo nguyên nhân, không theo triệu chứng
- [x] Chuyển `components/print/ReportPrintPreviewModal.vue` sang in bằng **iframe ẩn** (khuôn có sẵn ở bản in phân hệ Tài chính) — không tạo cửa sổ nào nên trang chính không bao giờ mất focus, và hết luôn cảnh báo "trình duyệt chặn pop-up"
- [x] Giữ nguyên phần chờ ảnh letterhead; thêm guard `frame.parentNode && frame.contentWindow` (bấm In lần nữa / đóng popup lúc ảnh chưa tải xong làm hẹn giờ cũ chạy trên iframe đã gỡ → lỗi null); dọn iframe khi đóng popup và khi component bị huỷ
- [x] Áp cho **cả 3 màn** đang dùng popup này: phiếu yêu cầu · phiếu xử lý yêu cầu · phiếu cung cấp thông tin (mỗi màn 2 nơi: danh sách + chi tiết)
- [x] Verify: bấm In → **không mở tab mới**, iframe dựng đúng nội dung (956 ký tự + 2 ảnh letterhead), hộp thoại in được gọi; đóng popup xong mở lại ô lọc vẫn focus đúng ô tìm; 0 lỗi ứng dụng trên bảng điều khiển
- [x] Ghi `.claude/skills/print-page/SKILL.md` §4a — kèm cảnh báo lỗi chỉ hiện trên Windows

**Chưa sửa (cần user chốt):** `components/assign/quotation/QuotationPrintPreview.vue` (màn Báo giá phân hệ Giao việc) dùng `window.open` y hệt nên dính đúng lỗi này — nằm ngoài luồng dịch vụ đang làm.

### Xuất Excel: tick sẵn đúng cột đang hiện trên màn (2026-08-25)
- [x] Trước đây popup "Chọn trường xuất file" mở ra là tick TẤT CẢ cột → người dùng cấu hình màn còn 5 cột mà file vẫn ra 13 cột, phải bỏ tick 8 lần mỗi lần xuất
- [x] `exportFieldsMixin` thêm computed `visibleExportFields`: lấy `tableColumns` (cột đang hiện, đúng thứ tự trên màn) giao với `exportFields`; tự map `status` → `status_text`; bỏ `index`/`actions`; màn nào lệch nhiều thì khai `exportFieldKeyMap`
- [x] `export-fields-modal.vue` thêm prop `default-selected`; mở popup thì tick sẵn theo đó (gán `orderedKeys` TRƯỚC `selected`, nếu không thứ tự cột rơi về thứ tự option gốc). Không truyền / truyền rỗng → giữ hành vi cũ là tick tất cả
- [x] Nối `:default-selected="visibleExportFields"` cho **9 màn CSKH** đang dùng popup này
- [x] Verify trên trình duyệt: màn hiện 5 cột dữ liệu → popup tick sẵn **5/13** đúng thứ tự; bật thêm cột "Địa chỉ sửa chữa" ở Cấu hình cột → mở lại popup thành **6/13** có cột mới đúng vị trí; bấm "Chọn tất cả" vẫn lên 13/13 (thêm/bớt tự do). Đã trả cấu hình cột của tài khoản test về như cũ
- [x] Ghi `.claude/skills/list-page/SKILL.md` §14b, kèm cảnh báo dễ chèn nhầm `:default-selected` vào `V2BaseDataTable` (đã dính khi sửa hàng loạt)

**Chưa nối (ngoài phạm vi luồng dịch vụ, cần user chốt):** 11 màn còn lại dùng chung popup này — `/assign/customers` và 10 màn phân hệ Tài chính.

#### Bổ sung: khoá cột bảng lệch khoá cột file xuất (2026-08-25)
- [x] Phát hiện khi kiểm màn Phiếu cung cấp thông tin bằng tài khoản của user: cột **Trạng thái bảo hành** đang hiện trên màn nhưng KHÔNG được tick sẵn. Lý do: bảng đặt khoá `warranty_status`, file xuất đặt `status_warranty_text` — **đảo thứ tự từ** nên quy tắc tự suy `<khoá>_text` không bắt được
- [x] Rà tự động cả 9 màn (đối chiếu `allColumns` với `exportFields`) → còn 3 chỗ nữa: `costStatus` / `serviceStatus` → `status_text`, `serviceCode` → `code`. Khai `exportFieldKeyMap` cho 3 màn: dịch vụ/chi phí · gói bảo dưỡng · phiếu cung cấp thông tin
- [x] Các cột lệch còn lại (Người/Ngày cập nhật ở màn danh mục, Áp dụng cho thiết bị / Công kỹ thuật ở màn công việc–lỗi thiết bị) là do **file xuất vốn không có cột đó** — không phải lỗi ánh xạ
- [x] Verify bằng file THẬT: xuất từ màn Phiếu cung cấp thông tin ra đúng 7 cột khớp màn hình, có `Số phiếu xử lý` (TPE.PXL.2026005291) và `Trạng thái bảo hành` (Đã tạo phiếu bảo hành)
- [x] Bổ sung cách rà tự động vào `.claude/skills/list-page/SKILL.md` §14b

#### Lịch sử: bỏ mã phòng trước tên người thực hiện (2026-08-25)
- [x] Dòng log đổi từ `CTV_NV - DNS Admin — PHÒNG CỘNG TÁC VIÊN_NV` thành `DNS Admin — PHÒNG CỘNG TÁC VIÊN_NV` — phòng ban đã in ngay bên cạnh nên ghép thêm mã phòng là lặp lại chính thông tin đó
- [x] Sửa ở CẢ HAI nơi hiển thị cho khỏi lệch: `SystemInfoSection.vue` (khối ở màn chi tiết + ruột popup lịch sử danh mục) và `CustomerHistoryModal.vue` (popup lịch sử màn Khách hàng)
- [x] **Ô lọc "Người thực hiện" giữ nguyên `MÃ PHÒNG - Tên`**: ở dropdown không có cột phòng ban nào khác, bỏ mã đi là hai người trùng tên không phân biệt được. Nhánh dựng tạm danh sách từ log cũng giữ mã phòng cho khớp danh sách chuẩn của máy chủ
- [x] Bộ lọc so khớp theo `actor_id` nên đổi chuỗi hiển thị KHÔNG ảnh hưởng lọc (đã kiểm code)
- [x] Verify trên màn thật: popup ở danh sách và khối ở màn chi tiết đều ra `Người thực hiện: DNS Admin — PHÒNG CỘNG TÁC VIÊN_NV`; dropdown lọc vẫn 783 người dạng `BDH - Bùi Thị Phương`
- [x] Ghi `.claude/skills/entity-history/ui-base.md` §7

### Bản in Báo giá dịch vụ — 3 mẫu + checklist (2026-08-25, phần máy chủ)

Cả 4 mẫu đều có sẵn trên dữ liệu gộp, đã trích biến từ mẫu THẬT chứ không suy từ tên trường (skill print-page mục 4c):

| Mẫu | Nguồn | Cách dựng |
| --- | --- | --- |
| Mẫu 1 — "Báo giá dịch vụ bảo hành sửa chữa" | `report_templates` id **272** | in theo từng thiết bị; bảng tổng hợp nằm ở biến riêng `TONG_HOP_BAO_GIA` |
| Mẫu 2 — "…mẫu 2" | `report_templates` id **361** | y hệt mẫu 1 nhưng tổng hợp nằm trong `CHI_TIET` như khối cuối |
| Mẫu 3 — "Báo giá dịch vụ sữa chữa bảo dưỡng" | `print_templates` mã **BGDV-02A** | KHÁC HẲN: gom phẳng thành 4 bảng I Dịch vụ · II Vật tư hàng hóa · III Chi phí khác · IV Tổng thanh toán |
| Checklist | `report_templates` id **191** | in kèm khi bật, mỗi dịch vụ bảo dưỡng một trang |

- [x] `WrQuotationPrintService extends WrServiceQuotationPrintService` cho mẫu 1 + 2. **Kế thừa không phải cho tiện**: trong ERP hai chứng từ gọi CHUNG hàm `getTable()`, nhánh `contract_2` và nhánh `2` (phiếu cung cấp thông tin) nằm cùng một chỗ trong mã — nên 4 khối Bảo hành / Dịch vụ / Chi phí / Tổng dựng y hệt nhau
- [x] Bồi phần riêng của báo giá: khối **HÀNG HÓA** (10 cột, VAT theo từng dòng, ảnh hàng hoá lấy 1 truy vấn cho cả phiếu) + `SO_BAO_GIA` · `GHI_CHU` · `HIEU_LUC_BAO_GIA`
- [x] **Lỗi tìm được khi chạy thử**: bảng "Tổng hợp báo giá" ban đầu dùng nguyên bảng của chứng từ 3 nên **bỏ sót toàn bộ khối hàng hoá** — in ra 347.004 đ trong khi tổng thật là 6.256.764 đ. Sửa: ghi đè `grandTotal()` + `totalTable()`, thêm dòng "Hàng hóa bán" đúng `totalQuotation()` của ERP
- [x] `WrQuotationCompactPrintService` cho mẫu 3 — quy tắc gộp dòng của ERP: cùng tên + đơn giá + %VAT + %chiết khấu (+ ĐVT với vật tư) thì cộng dồn số lượng, ghi chú nối bằng "; "; cùng dịch vụ khác giá thì vẫn tách dòng. Số La Mã tự lùi khi bảng nào rỗng
- [x] `checklistPages()` + mẫu 191: chỉ in dịch vụ có số lượng khác 0 (gói bảo dưỡng khai sẵn nhiều cấp, in cả cấp bỏ trống là ra hàng chục trang thừa); chú giải ký hiệu lấy từ danh mục, không hard-code
- [x] Endpoint `GET /customer-care/wr-quotations/{id}/print-data?template=mau_1|mau_2|mau_3&check_list=1`, gate `canView()` — không chặn ở đường in thì người không được xem vẫn đọc trọn nội dung
- [x] Mở tầm vực 10 hàm dựng bảng ở lớp cha thành `protected` (chỉ đổi tầm vực, không đổi hành vi màn chứng từ 3)

**Verify bằng dữ liệu thật:**
| Phép kiểm | Kết quả |
| --- | --- |
| Tổng bản in (mẫu 1/2) vs số đã lưu — 300 báo giá ngẫu nhiên | **2026: 159/159 khớp tuyệt đối**; 2025: 5/141 lệch — dữ liệu cũ, không phải lỗi công thức |
| Tổng mẫu 3 (gom phẳng, tính khác hẳn) vs số đã lưu — 120 báo giá 2026 | **120/120 khớp** |
| Bản in mẫu 1 phiếu TPE.BGDV.2026008582 | đủ 6.256.764 / 5.472.000 / 321.300 / 463.464, có dòng "Hàng hóa bán", bằng chữ đúng |
| Mẫu 2 | tổng hợp nằm trong phần chi tiết, không còn biến chưa fill |
| In kèm checklist | 1 → 6 trang, có bảng "Nội dung kiểm tra bảo dưỡng", ký hiệu cấp bảo dưỡng, chú giải 16 ký hiệu, chỗ ký |
| Mọi mẫu | 0 biến `{{...}}` sót lại |

**Còn lại của Phase A:** popup chọn mẫu in ở giao diện (3 mẫu + ô "In kèm danh mục kiểm tra bảo dưỡng") · nhận tệp đính kèm khi lưu · 2 cột tồn kho của bảng hàng hoá.

### Sửa file xuất Excel màn danh sách (2026-08-25)
- [x] Bỏ đóng băng hàng tiêu đề trong `utils/export/listExportFile.js` (áp cho cả 3 màn dùng chung: Phiếu CCTT · Yêu cầu SC-BH · Phiếu xử lý SC-BH — user chốt)
- [x] `WrServiceQuotationService::exportRows()` trả `total_before_vat` / `total_after_vat` kiểu số (bỏ ép `(string)`); FE gắn `numFmt = '#,##0'` + canh phải cho ô kiểu number → hết cảnh báo "The number in this cell is formatted as text"

### Fix lỗi validate bám sai dòng khi xoá/thêm dòng trong bảng (2026-08-25)
- [x] Thêm `utils/rowFieldErrors.js` (`removeRowErrors` / `dropRowErrorsFrom` / `clearRowErrors`) — dọn khoá lỗi 422 gắn chỉ số dòng (`products.2.serial`) mỗi khi mảng dòng đổi
- [x] Áp vào chỗ xoá / thêm / chuyển dòng của form màn này; đổi khách hàng (xoá cả bảng) thì xoá hết lỗi của bảng

### Rà "một màn vào từ nhiều link" cho cả luồng (2026-08-26)
- [x] Rà ERP: mỗi màn có nhiều mục menu trỏ cùng đường dẫn, khác query — `?type=all` · `?type=waiting_handle` · `?type=waiting_information` · `?type=waiting_create_quotation`; riêng màn Báo giá ERP đặt tên tham số là **`permission`** (`?permission=all`)
- [x] Kiểm HRM: **4/5 màn đã xử lý sẵn** bằng `applyQueryType()` — whitelist giá trị máy chủ hiểu, áp SAU khi nạp bộ lọc đã lưu (link thắng bộ lọc cũ), "Làm mới" giữ nguyên phạm vi
- [x] **Màn Báo giá dịch vụ còn thiếu** (lúc port chốt "ERP chỉ có 1 mục menu") → bổ sung `applyQueryType()` nhận `?type=` và cả `?permission=` làm bí danh + `handleReset` giữ phạm vi
- [x] Verify trên trình duyệt: `?type=waiting_handle` → phạm vi đổi đúng · `?type=all` → đổi lại đúng · `?permission=index` ở màn báo giá → nhận đúng · `?type=xoa-het-du-lieu` → **bỏ qua, giữ `all`** (không đẩy giá trị lạ xuống máy chủ)
- [x] Ghi `.claude/skills/list-page/SKILL.md` §3d kèm 4 điểm dễ sai

### Đối chiếu LỐI VÀO của HRM với ERP bằng số liệu thật (2026-08-26)

ERP local và HRM chạy trên **cùng một cơ sở dữ liệu** (`local_hrm_erp`) nên đếm được cả hai bên với
cùng một người dùng rồi so từng lối vào — không phải đọc code rồi đoán.

| Màn | Lối vào | ERP | HRM | Kết luận |
| --- | --- | --- | --- | --- |
| Phiếu yêu cầu | (trống) / `?type=all` / `?type=waiting_handle` | 6 / 5.371 / 0 | 6 / 5.371 / 0 | **khớp tuyệt đối** |
| Phiếu xử lý | (trống) / `all` / `waiting_information` | 5 / 5.258 / 22 | 5 / 5.258 / 22 | **khớp tuyệt đối** |
| Phiếu cung cấp thông tin | (trống) / `all` / `waiting_create_quotation` | 1 / 4.980 / 0 | 1 / 4.980 / 0 | **khớp tuyệt đối** |
| Phiếu bảo hành | (trống) / `all` | 0 / 3.631 | 0 / 3.631 | **khớp tuyệt đối** |
| Báo giá dịch vụ | (trống) / `all` | 0 / 4.218 | 0 / 3.586 | **lệch — do QUYỀN, không do logic** |

(số của tài khoản id 13; đã chạy lại với id 34 và 224 cho cùng kết luận)

**Truy nguyên 2 nguyên nhân gây lệch — cả hai đều KHÔNG phải lỗi xử lý lối vào:**
1. **3 quyền của màn Báo giá chưa được seed vào dữ liệu**: `Xem báo giá dịch vụ SC - BH theo tổng công ty/công ty/phòng ban` đã khai trong `PermissionsTableSeeder` (id 1548–1550) nhưng chưa chạy seeder trên cơ sở dữ liệu này — bên ERP quyền cùng tên có sẵn ở guard `web`. Hệ quả: mọi người mở màn Báo giá đều rơi về "chỉ phiếu của mình". (Phiếu bảo hành không dính vì quyền của nó đã có sẵn ở guard `api`.)
2. **Cùng một người, hai guard hai bộ quyền**: vd tài khoản 235 có `Xử lý yêu cầu sửa chữa` ở guard `web` (ERP) nhưng không có ở `api` (HRM) → ERP thấy 4.867 phiếu, HRM chỉ thấy 686. Đây đúng là vấn đề **phân quyền vận hành** đang treo chờ user quyết.

**Logic thì đã khớp từng nhánh**, kể cả nhánh dễ sót nhất: người có quyền `Xử lý yêu cầu sửa chữa` luôn nhìn thấy thêm phiếu gửi về phòng mình dù không đủ quyền xem theo cấp (`applyScope()` của HRM có đúng nhánh `orWhere(department_reception_id = phòng tôi)` như ERP).

**Việc cần user quyết:** chạy `PermissionsTableSeeder` để cấp 6 quyền của 2 màn mới (Phiếu bảo hành 1545–1547 · Báo giá 1548–1550) — tôi KHÔNG tự chạy vì seeder này đụng toàn bộ bảng quyền.

- [x] Bổ sung chương **9. CÁC LỐI VÀO MÀN HÌNH** vào 3 tài liệu mô tả nghiệp vụ (bảng 3 cột: Vào bằng · Danh sách hiện ra · Dùng khi nào + 3 câu lưu ý), đã sinh lại 4 file .docx
- [x] `.claude/skills/business-flow-documenter/SKILL.md`: cấu trúc chuẩn nay **12 chương**, thêm mục hướng dẫn viết chương 9 + checklist
- [x] `.claude/skills/testcase-documenter/SKILL.md`: thêm mục "test ĐỦ CÁC LỐI VÀO" (5 loại TC bắt buộc mỗi lối vào) + checklist

### Popup chọn mẫu in — phần giao diện (2026-08-26)
- [x] `SelectPrintTemplateModal.vue` dựng trên `V2BaseModal` (khuôn popup dùng chung): ô chọn mẫu bằng `V2BaseSelectInModal` + ô tích "In kèm danh mục kiểm tra bảo dưỡng" + nút In / Đóng. Bám đúng ERP (`service_quotations/index.blade.php`), mặc định chọn sẵn mẫu 1 để mở popup là bấm In được ngay
- [x] Popup chỉ CHỌN rồi báo ra ngoài, màn dùng lo gọi máy chủ → dùng lại được ở **cả màn danh sách lẫn màn chi tiết** mà không lặp code
- [x] Ô tích chỉ hiện khi báo giá CÓ dịch vụ bảo dưỡng — không có thì tích vào cũng không ra trang nào, để ô trống chỉ làm người dùng tưởng hệ thống lỗi
- [x] Máy chủ trả thêm cờ `has_maintenance` cho từng dòng danh sách bằng `withCount('extendProducts')` — **một truy vấn con cho cả trang**, không hỏi từng dòng
- [x] Nối vào hành động "In" ở màn danh sách và nút "In" ở footer màn chi tiết; màn chi tiết suy cờ bảo dưỡng ngay từ dữ liệu form
- [x] ⚠️ Template component con ghi đè TRỌN template cha nên popup xem trước phải khai lại ở `WrQuotationForm` dù lớp cha đã có — không khai là bấm In xong không thấy gì

**Verify trên trình duyệt (0 lỗi console):**
| Phép thử | Kết quả |
| --- | --- |
| Màn danh sách → In (phiếu CÓ bảo dưỡng) | popup mở đúng, tiêu đề kèm mã phiếu, đủ 3 mẫu + ô tích |
| Chọn mẫu 3 + tích checklist → In | bản xem trước dựng đúng: có bảng Dịch vụ (mẫu gọn) và có các trang danh mục kiểm tra bảo dưỡng |
| Màn chi tiết → nút In ở footer | popup mở đúng, footer đủ Sửa · Xóa · In · Quay lại |
| Phiếu KHÔNG có bảo dưỡng | ô tích **ẩn hẳn**, popup chỉ còn ô chọn mẫu |
| Mở phiếu của người khác | 404 — gate quyền xem vẫn chặn đúng ở cả đường in |

**Phase A của Báo giá dịch vụ tới đây là DÙNG ĐƯỢC trọn vẹn.** Còn 2 hạng mục phụ: nhận tệp đính kèm khi lưu (tải lên S3) và 2 cột tồn kho của bảng hàng hoá.

### 2 hạng mục phụ cuối của Phase A (2026-08-26)

**1. Tệp đính kèm**
- [x] Máy chủ: endpoint `POST /wr-quotations/upload-attachment` tải 1 tệp lên kho tệp, trả đường dẫn — cùng khuôn màn Phiếu yêu cầu. Thư mục giữ nguyên tên ERP dùng (`wr_service_quotations`) để hai hệ đọc chung một chỗ
- [x] Form gửi lên **danh sách đường dẫn** (tệp đã tải trước), giữ toàn bộ form là JSON thuần — ERP gửi multipart trong lúc lưu phiếu. Service gói lại thành một chuỗi nối bằng ", " đúng cách ERP lưu
- [x] Không gửi khoá `attachments` thì **giữ nguyên tệp cũ** — tránh việc màn nào quên gửi là xoá sạch tệp
- [x] Giao diện: dùng `V2BaseFile` (component chọn tệp dùng chung), mỗi tệp một dòng + nút Thêm tệp / Xoá tệp; màn XEM mà chưa có tệp thì bỏ hẳn khối, không để nút xám nằm trơ
- [x] Verify: tải PDF thật lên → nhận URL trên kho tệp; lưu phiếu → cột dữ liệu có URL, đọc lại ra đúng mảng; gửi mảng rỗng → xoá sạch. **Tệp giả đuôi .pdf bị chặn** ("Chỉ nhận file PDF, ảnh, Word hoặc Excel") — chặn ở máy chủ chứ không dựa vào `accept` của trình duyệt

**2. Hai cột tồn kho**
- [x] **Không viết lại công thức tồn kho**: dùng lại `Modules\Assign\Services\StockService` (đã port đúng `getAccountingStockDetail` của ERP)
- [x] Endpoint `GET /wr-quotations/warehouses` (mirror `Warehouse::getByGroup()`: nhóm kho của công ty + kho trong nhóm thụt đầu dòng + kho lẻ, khoá giữ khuôn ERP `warehouse_group_id-5` / `warehouse_id-123`) và `POST /wr-quotations/stock-of-products`
- [x] Chọn cả NHÓM kho thì cộng tồn từng kho trong nhóm — các kho hạch toán độc lập nên cộng lại đúng bằng cách ERP gộp danh sách kho rồi tính một lượt
- [x] Giao diện: ô "Xem tồn" cạnh tiêu đề khối C (đúng chỗ ERP đặt) + 2 cột "Tồn dự kiến" / "Đang giữ"; chưa chọn kho thì để **trống** chứ không in "0" (số 0 dễ bị hiểu là hết hàng); thêm hàng hoá mới thì tự nạp lại; bỏ chọn kho thì xoá sạch số
- [x] **Verify đối chiếu ERP: 25 sản phẩm trên cùng một kho, LỆCH 0** (`in_stock` / `prepick_qty` / `in_warehouse` khớp từng số). Trên màn: chọn kho → 2 cột có số; hàng có tồn ra đúng 1; bỏ chọn kho → về trống

**PHASE A HOÀN TẤT.** Việc còn lại của luồng: Phase B (lập báo giá độc lập + sao chép) và lệnh chạy nền chuyển "Hết hiệu lực".

### Phase B — bước 1: LẬP BÁO GIÁ ĐỘC LẬP (2026-08-26)

Nhánh chính trên dữ liệu thật: **3.966/5.170 báo giá (77%) lập độc lập**, không sinh từ phiếu cung cấp thông tin nào.

**Máy chủ**
- [x] **Lỗi chặn đường: giá vốn công `NOT NULL`.** Lập từ phiếu gốc thì chép sang được, lập độc lập thì không có gì để chép → lưu vỡ ngay dòng thiết bị đầu tiên (`Column 'engineering_work' cannot be null`)
- [x] Tìm được công thức thật của ERP (`getRepairProduct()`): **giá vốn công = `companies.work_price × device_errors.recipe_work_norm`**. HRM đã port công thức này ở màn Danh mục lỗi thiết bị nên chỉ việc dùng lại
- [x] `fillWorkCost()` bồi giá vốn theo thứ tự: giữ giá trị form gửi (người có quyền xem giá vốn nhập tay) → chép từ phiếu gốc → **tính từ danh mục lỗi thiết bị** → 0. Gom 2 truy vấn cho cả phiếu
- [x] Verify: tạo báo giá độc lập qua API → giá vốn lưu **350.000** = đúng `700.000 × 0,5` của công thức ERP

**Giao diện**
- [x] Nút **Tạo mới** ở màn danh sách → `/customer-care/wr-quotations/create` (không kèm phiếu gốc)
- [x] Form tự nhận biết 2 đường vào: có `?wr_information_id=` thì khoá khách hàng theo phiếu gốc (đúng ERP), không có thì cho **tự chọn khách hàng · người liên hệ · địa chỉ sửa chữa**
- [x] Dùng lại popup chọn khách hàng dùng chung `ChooseErpCustomerModal` — không dựng popup riêng
- [x] Đổi khách hàng thì **xoá sạch** người liên hệ / địa chỉ của khách cũ, tránh lưu nhầm dữ liệu khách trước
- [x] Người liên hệ + địa chỉ nạp qua endpoint của màn Phiếu yêu cầu (**không** dùng `assign/customers/{id}` vì endpoint đó gate bằng quyền ERP "Xem khách hàng" → người chỉ có quyền luồng dịch vụ sẽ nhận 403 và 2 ô trống trơn)
- [x] Lập độc lập thì dựng sẵn 5 dòng chi phí từ danh mục (lập từ phiếu gốc thì đi kèm dữ liệu điền sẵn)
- [x] Ô "Số phiếu cung cấp thông tin" **ẩn hẳn** khi lập độc lập, không để ô trống vô nghĩa

**Verify trên trình duyệt:** bấm Tạo mới → form lập độc lập; chọn khách "CÔNG TY TNHH HUAZHI MATERIALS VIỆT NAM" → nạp đúng người liên hệ và địa chỉ; nhập hiệu lực 15 ngày → Lưu nháp → sinh `TPSG.BGDV.2026010362`, trạng thái Đang tạo, **không gắn phiếu gốc**, 5 dòng chi phí. Đã xoá phiếu thử, tổng báo giá trở lại 5.170.

**Lỗi tự gây khi sửa, đã sửa:** `createItem` chèn hụt vào `methods` nên nút Tạo mới báo "not defined" (bảng điều khiển đỏ 14 dòng) — đã chèn lại đúng chỗ và kiểm lại.

**Ghi nhận (không phải lỗi mới):** `ChooseErpCustomerModal` có sẵn cảnh báo `The computed property "fields" is already defined in data` — do vee-validate chiếm tên `fields`, màn Phiếu yêu cầu dùng cùng component cũng dính. Là component dùng chung nên chưa tự sửa.

**Còn lại của Phase B:** thêm thiết bị thủ công từ danh mục thiết bị của khách · thiết bị tương đương · tạo lỗi thiết bị ngay trong form · Sao chép báo giá.

### Sửa vị trí mục menu — tôi đặt sai (2026-08-26)
- [x] **Lỗi**: tôi đặt "Báo giá dịch vụ" vào CSKH → Kiểm tra bảo hành sửa chữa theo suy đoán, KHÔNG tra menu ERP. Menu ERP đặt nó ở **Kinh doanh → Báo giá → "Báo giá dịch vụ sửa chữa - bảo dưỡng - bảo trì" → "Danh sách báo giá"** (`topmenubar.blade.php:497`)
- [x] Quét lại toàn bộ 5 màn của luồng trong menu ERP:

| Màn | Vị trí trong menu ERP |
| --- | --- |
| Phiếu yêu cầu | Hàng hóa → Lắp đặt-BH-SC · Lắp đặt-BH-SC (`?type=all`) · CSKH → Kiểm tra bảo hành sửa chữa (`?type=all`) · **Kinh doanh → Báo giá → BG dịch vụ SC-BD-BT** |
| Phiếu xử lý | CSKH → Kiểm tra bảo hành sửa chữa (`?type=all`) |
| Phiếu cung cấp thông tin | CSKH → Kiểm tra bảo hành sửa chữa (`?permission=all`) · **Kinh doanh → Báo giá** (`?permission=waiting_create_quotation`) |
| **Báo giá dịch vụ** | **CHỈ** Kinh doanh → Báo giá → BG dịch vụ SC-BD-BT (`?permission=all`) |
| Phiếu bảo hành | CSKH → Kiểm tra bảo hành sửa chữa (`?type=all`) |

- [x] Bỏ mục đặt nhầm khỏi `customer-care.js`, ghi chú lý do ngay tại chỗ để không ai thêm lại
- [x] HRM **đã khai sẵn** nhóm "Bán dịch vụ → Báo giá dịch vụ SC-BD-BT" trong `sale-hub.js` nhưng chưa nối link → nối 3 màn, **giữ nguyên tham số** trên link vì mỗi lối vào là một phạm vi dữ liệu (`?type=waiting_create_quotation`, `?type=all`)
- [x] Verify: hub Bán hàng → Bán dịch vụ → nhóm hiện đúng 3 mục, bấm "Danh sách báo giá" ra `/customer-care/wr-quotations?type=all`; menu CSKH còn đúng 4 mục như ERP
- [x] Ghi `.claude/skills/erp-to-hrm-screen/SKILL.md` bước 2: **tra menu ERP trước, đừng suy từ tên màn**, kèm lệnh quét và 3 điều rút ra (một màn nằm nhiều nhóm · giữ nguyên tham số link · không khai trùng)

### Sửa lỗi hiệu năng: lối vào "chờ làm báo giá" mất 15 giây (2026-08-26)

**Đo trước, không đoán:**
| Lối vào | Trước | Sau |
| --- | --- | --- |
| `?type=waiting_create_quotation` | **14,7s** | **0,24s** |
| `?type=all` | 0,60s | 0,27s |
| `?type=index` | — | 0,26s |

**Truy nguyên:** tách từng phần thì thấy chậm nằm ở CHÍNH truy vấn danh sách (11s), không phải Resource (0,01s). Lối vào này lọc bằng 2 truy vấn con `EXISTS` trên `wr_service_quotation_products` (13.716 dòng) và `wr_service_quotation_extend_products` (3.488 dòng) — mà cột nối `wr_service_quotation_id` **không có index**, nên mỗi dòng cha phải quét trọn bảng con.

**Rà đủ thì thiếu 12 index** trên 5 bảng của nhóm này (kể cả `customer_id`, `department_id`, `approved_by`, `parent_id` — toàn cột dùng ở bộ lọc).

- [x] Migration `2026_08_26_000001_add_indexes_to_wr_service_quotation_tables`: 12 index đơn + 2 index ghép `(type, status)` và `(type, created_by)` — một mình `type` lọc rất kém vì chỉ có 2 giá trị
- [x] **Tên index phải tự đặt, rút gọn**: tên mặc định của Laravel (`wr_service_quotation_extend_products_wr_service_quotation_id_index`) dài 66 ký tự, vượt trần 64 của MySQL → lệnh tạo index ném "Identifier name is too long"
- [x] Không bọc DDL trong transaction (MySQL implicit-commit)
- [x] Migration idempotent: cột đã là cột đầu của index nào đó thì bỏ qua, chạy lại không lỗi
- [x] Verify: cả **5 màn của luồng** đều về ~0,27s

Bảng dùng chung với ERP nên thêm index cũng làm ERP nhanh lên theo; không đổi dữ liệu, không đổi cấu trúc logic.

### Sửa 3 điểm lệch ERP ở form lập báo giá (2026-08-26, user chỉ ra)

- [x] **Ô "Số phiếu cung cấp thông tin" phải có ở form lập độc lập.** Tôi ẩn hẳn vì nghĩ lập độc lập thì không có phiếu gốc — sai. ERP (`service_quotations/form.blade.php:14`) để ô này kèm nút tìm ngay cả ở màn tạo mới: chọn phiếu xong thì **nạp toàn bộ nội dung phiếu vào form** (`addCopyInfo`). Đã dựng `InformationRequestSearchModal` (khuôn `V2BaseModal`, bám popup chọn chứng từ của phân hệ Tài chính), lọc đúng lối vào ERP dùng (`?type=waiting_create_quotation` — chỉ phiếu chờ CHÍNH TÔI làm báo giá) và **dùng lại chính endpoint `prefill`** nên hai đường vào ra cùng một kết quả
- [x] **Ô chọn tệp hiện 2 icon xoá.** `V2BaseFile` có sẵn nút xoá riêng, cộng nút xoá dòng của bảng thành 2 icon cạnh nhau — người dùng không biết cái nào xoá tệp, cái nào xoá dòng. Thêm prop `hide-remove` cho `V2BaseFile` (mặc định `false` → mọi màn đang dùng giữ nguyên hành vi), form báo giá bật lên; xoá = xoá cả dòng
- [x] **Ô chọn khách hàng gộp thành 1 input** như màn Phiếu yêu cầu: bấm thẳng vào ô để mở popup, bỏ nút "Chọn" riêng bên cạnh. Dùng khuôn `.picker-input` (`readonly` + `@click.native`, KHÔNG `disabled` vì `disabled` nuốt sự kiện click)

**Verify trên trình duyệt:** ô phiếu và ô khách hàng đều là 1 input với chữ nhắc "Nhấn vào đây để chọn…", **0 nút phụ**; bấm ô phiếu → popup liệt kê đúng phiếu chờ tôi làm báo giá → chọn `TPE.PCCTT.2026010301` → nạp đủ khách hàng + 1 dòng sửa chữa + 5 dòng chi phí; dòng tệp chỉ còn **1 icon xoá**.

### BỘ KIỂM ĐẦY ĐỦ luồng dịch vụ — nhiều case, nhiều tài khoản (2026-08-26)

**Bộ tài khoản đại diện** (chọn theo quyền THẬT, không chọn bừa):

| TK | Quyền |
| --- | --- |
| 13 | đủ quyền ở CẢ guard HRM và ERP (tổng công ty) |
| 36 | đủ quyền ở cả 2 guard |
| 224 | HRM: tổng công ty · ERP: CHỈ phòng ban (lệch guard) |
| 235 | HRM: KHÔNG có · ERP: phòng ban + xử lý |
| 214 | KHÔNG có quyền nào |
| 242 / 461 | chỉ quyền ERP |

**Nhóm A — phạm vi dữ liệu: 65 phép so ERP ↔ HRM** (5 màn × mọi lối vào × 5 tài khoản) → **53 khớp**.
12 chỗ lệch, truy nguyên tất cả về **một nguyên nhân duy nhất: bộ quyền khác nhau giữa 2 guard**, không có lệch logic nào. Chứng minh chứ không suy luận: tạm cấp 3 quyền báo giá cho tài khoản 13 trong một giao dịch rồi đếm lại → HRM ra **đúng 4.218 = ERP**, sau đó rollback sạch.

**Nhóm B — quyền trên từng bản ghi: 76 phép so** (19 báo giá đủ 4 trạng thái × 4 tài khoản) → **72 khớp**. 4 chỗ lệch đều là **phiếu nháp của người khác**: ERP cho quản trị xem/sửa, HRM chặn — đúng khác biệt có chủ ý đã chốt từ chứng từ 2 và đã ghi trong mã.

**Nhóm C — chốt chặn & validate qua API: 36/36 đạt.** Xác thực (401 ×2) · xem chi tiết (chính chủ 200 / người khác 403 / id lạ 404 / id khác loại chứng từ 404) · sửa–xoá phiếu đã duyệt **423 cho cả chính chủ, người khác lẫn quản trị** · validate tạo mới (payload rỗng, thiếu khách hàng, trạng thái lạ, hiệu lực = 0 → 422) · in 3 mẫu + checklist + mẫu lạ · prefill (thiếu tham số 400 · đúng người 200 · người khác 403 · phiếu không đủ điều kiện 403 · id lạ 404) · kho và tồn kho · tải tệp.

**Nhóm D — luồng end-to-end: 12/12 đạt.** Lập từ phiếu gốc → phiếu gốc chuyển "Đang báo giá" → người khác không xem/sửa được → chính chủ sửa được → Lưu và duyệt → khoá sửa, phiếu gốc chuyển "Báo giá đã duyệt" → sửa/xoá sau duyệt đều 423 → lập tiếp từ phiếu đã dùng bị chặn 403.

**LỖI THẬT bắt được nhờ bộ kiểm — đã vá:**
- [x] **4 cột tiền tổng phụ thuộc hoàn toàn vào giao diện.** Lưu phiếu mà không gửi kèm thì phiếu lưu **0 đồng** trong khi bản in tính ra 1.105.380 — cột "Tổng thanh toán" trên lưới và mọi báo cáo đọc thẳng 4 cột này. Trên dữ liệu ERP thật chỉ 4/5.171 phiếu dính (giao diện gần như luôn gửi đủ), nhưng đây là chỗ hỏng chờ xảy ra
- [x] Vá: máy chủ **tự chốt lại 4 cột tổng** khi lưu bằng đúng công thức của bản in (`grandTotal`, đã đối chiếu hơn 200 báo giá ERP thật, lệch 0) → số trên lưới, trên bản in và trong báo cáo luôn là một
- [x] Verify bản vá: lưu lại phiếu không kèm cột tổng → ra đúng 1.023.500 / 81.880 / 1.105.380

**Ghi chú về chính bộ kiểm** (2 lần đầu chạy có FAIL giả, đều do script chứ không phải ứng dụng):
- Thiếu `Accept: application/json` → Laravel trả **302 redirect** thay vì JSON. Test API luôn phải gửi header này.
- Muốn kiểm chốt chặn **423** thì payload phải HỢP LỆ: `FormRequest` validate chạy TRƯỚC guard nên payload sai chỉ ra 422, guard không bao giờ tới lượt (đúng cái bẫy CLAUDE.md đã ghi).
- JSON lồng dấu nháy trong hàm bash bị hỏng escape → dùng file payload (`--data-binary @file`).

Dữ liệu thử đã dọn sạch: tổng báo giá trở lại **5.170**, phiếu gốc về "Chờ làm báo giá", 0 dòng con mồ côi.

### Bộ kiểm GIAO DIỆN bằng Playwright — nhiều tài khoản (2026-08-26)

Bộ kiểm hôm trước chạy ở tầng API/truy vấn; phần giao diện mới chỉ chạy rải rác. Nay chạy có hệ thống, **đăng nhập thật bằng mật khẩu** (không nhét token) để đi qua cả lớp xác thực.

| Tài khoản | Vai | Kết quả |
| --- | --- | --- |
| 214 (`duyendh.datd`) | KHÔNG có quyền nào | 5/6 — phạm vi 0 phiếu, có nút Tạo mới, **không hiện ô lọc Công ty** (đúng fail-closed), dòng báo trống |
| 235 (`khangcx.cshn`) | 773 báo giá | 9/9 — nút Sửa/Xoá ẩn-hiện đúng trạng thái ở **cả 10 dòng**, badge đủ, tiền làm tròn, tìm nhanh 1/1, Làm mới về 773, sắp xếp đổi chiều, phân trang, đổi số dòng/trang |
| 428 (`Luyentq.kd1`) | người lập phiếu CÓ gốc | 4/4 — khách hàng và số phiếu gốc đều **khoá**, hiện đúng `TPE.PCCTT.2025000142` |

**Màn chi tiết** (phiếu Đã tạo hợp đồng): đủ 8 khối (Thông tin khách hàng · A→E · Điều khoản · Lịch sử), footer **chỉ còn In + Quay lại** (không Sửa/Xoá), số tiền khớp dữ liệu 6.256.764.

**Màn sửa:** 2 nút Lưu · popup xác nhận trước khi duyệt · bỏ trống hiệu lực rồi duyệt → **lỗi đỏ inline "Bắt buộc phải nhập", không rời trang** · gõ rồi bấm Quay lại → **cảnh báo "Bạn có thông tin chưa lưu"**.

**Chốt chặn qua URL trực tiếp:** mở `/wr-quotations/10285/edit` bằng tài khoản KHÔNG phải người lập → tự chuyển **trang 404**.

**3 "FAIL" đầu tiên đều là kỳ vọng sai của tôi, không phải lỗi màn:**
- đếm 15 cột — thực tế 11 là số cột HIỆN mặc định (15 là tổng khai)
- dùng selector `h5` để đếm khối — khối dùng thẻ khác, đếm lại đủ 8
- tưởng phiếu `10285` sinh từ phiếu gốc nên phải khoá khách hàng — tra dữ liệu thì nó **lập độc lập**, cho đổi khách là đúng. Kiểm lại bằng phiếu `144` (có gốc thật) → khoá đúng

**Sự cố khi test — đã xử lý ngay:** tôi lỡ đổi mật khẩu `namdangit@gmail.com` (chính là id 13) trong lúc đặt mật khẩu hàng loạt cho tài khoản test. Đã khôi phục ngay về `2025Dns@2` và xác nhận lại bằng `Hash::check`. Các tài khoản test khác (235, 214, 461, 428) dùng `Test@2026`.

#### Playwright — 2 mảng còn lại (2026-08-26)

**A. Luồng lập báo giá ĐỘC LẬP trọn vẹn từ giao diện** (tài khoản 428, người lập thật):
mở form → chọn khách qua popup → chọn người liên hệ → chọn địa chỉ sửa chữa → nhập hiệu lực 12 ngày
→ thêm hàng hoá qua popup dùng chung → chọn kho xem tồn → **Lưu nháp** → mở lại (dữ liệu còn nguyên)
→ **Lưu và duyệt** → phiếu khoá sửa/xoá, dòng chỉ còn In + Lịch sử.
Số tiền: màn hiện **53.350.000**, phiếu lưu **53.350.000**, bản in ra **53.350.000** — ba nơi bằng nhau.

**B. Popup chọn mẫu in:** mở từ dòng danh sách → đủ 3 mẫu, mặc định mẫu 1, **ô tích checklist ẩn đúng**
(phiếu không có dịch vụ bảo dưỡng) → bấm In → bản xem trước có tên hàng hoá, tiền và dòng "Bằng chữ".

**LỖI THẬT bắt được — đã vá:**
- [x] **Tên người liên hệ lưu RỖNG.** Máy chủ trả `fullname` nhưng tôi map `contact.name` → chọn xong ô hiện trống, tên không vào phiếu, và **không có lỗi nào báo ra**. Mẫu in dùng tên này ở dòng "Kính gửi" nên bản in sẽ thiếu. Sửa map + bổ sung nhánh **khách CÁ NHÂN** (không có danh sách người liên hệ thì lấy luôn tên khách), giống hệt màn Phiếu yêu cầu
- [x] Verify sau vá: chọn người liên hệ → `"Ms. Nhung" | SĐT 0376284889`; mở lại phiếu vẫn còn

**3 "FAIL" khác đều do script test, không phải lỗi màn:** tìm kho "Kho Sài Gòn" trong khi tài khoản thuộc công ty TPE (danh sách kho đúng theo công ty người dùng) · bấm nút In qua menu "Hành động khác" trong khi nút In nằm thẳng trên dòng.

Dữ liệu thử đã dọn: tổng báo giá trở lại **5.170**, 0 dòng con mồ côi.

---

## Bổ sung: In danh sách + Xuất Excel cho 2 màn cuối luồng (2026-08-26)

**Vì sao có mục này:** user hỏi sao màn Báo giá dịch vụ và Phiếu bảo hành không có 2 nút này. Tra ERP
(blade `index`, route, controller) — **ERP vốn KHÔNG có** ở 2 màn này, chỉ 3 màn đầu của luồng mới có
(mẫu in 275/276/278). User chốt **bổ sung cho đồng bộ**, chấp nhận khác ERP.

### BE
- [x] `ExportColumnRegistry`: thêm bộ cột `wr_quotations` (15 cột) và `wr_warranties` (11 cột)
- [x] `WrServiceQuotationService::exportRows` — đổi `self::LIST_RELATIONS` → `static::`, thêm điểm móc
      `listResourceClass()`. **Lỗi bắt được:** hàm cha hard-code Resource của phiếu cung cấp thông tin
      nên màn Báo giá xuất ra rỗng ở đúng các cột riêng (số phiếu CCTT, số điện thoại, người duyệt)
      mà không có lỗi nào báo ra
- [x] `WrQuotationService`: khai `LIST_RELATIONS` riêng (thêm `approver.info`, `informationRequest`)
      — trước đó 2 cột này rơi vào lazy load, mỗi dòng thêm 2 truy vấn
- [x] `WrQuotationListResource`: bổ sung `wr_information_code` (cột đã có trên bảng nhưng luôn trống)
- [x] `WrWarrantyService::exportRows` (mới)
- [x] `WrQuotationPrintService::listVariables` + `WrWarrantyPrintService` (mới) — cùng bộ biến với
      mẫu 275 để 4 bản in của luồng đọc lên giống nhau
- [x] Migration `2026_08_26_000002_...`: chèn 2 mẫu in `DANH_SACH_BAO_GIA_DICH_VU`,
      `DANH_SACH_PHIEU_BAO_HANH`. **Tra theo `code`, không theo id** — mẫu do HRM sinh nên id mỗi
      môi trường một khác (ERP có sẵn mới dùng được id cứng)
- [x] Controller + route `export-rows` / `print-list-data` cho cả 2 màn (đặt TRƯỚC `/{id}`)

### FE
- [x] 2 màn thêm nút **Xuất Excel** + **In danh sách**, `exportFieldsMixin` + `ExportFieldsModal`
      (tick sẵn cột đang hiện), `reportPrintPreviewMixin` + `ReportPrintPreviewModal` cho màn bảo hành

### Kiểm chứng
- Gọi thật qua HTTP: `export-rows` trả đúng nhãn + số dòng (3.586 báo giá / 3.631 phiếu bảo hành);
  lọc cột `fields=` cắt đúng; số tiền trả về **số thật** (không phải chuỗi)
- `print-list-data`: không còn biến `{{...}}` chưa thay, letterhead ra URL thật, nhãn phòng ban đúng
  tên phòng khi có lọc / "Tất cả" khi không lọc, trần 2.000 dòng hoạt động
- **Phân quyền — 6 tài khoản khác mức quyền** (13, 428, 24, 25, 27, 28): số dòng *trên màn* = số dòng
  *file xuất* = số dòng *bản in* ở cả 2 màn, không lệch trường hợp nào (13: 3.586/3.631 · 428: 99/0 ·
  28: 256 · 27: 60 · 25: 3 · 24: 1)

**Chưa làm:** chưa kiểm trên giao diện thật bằng Playwright (chờ user xác nhận có cần không).

### Playwright — kiểm trên giao diện thật (2026-08-26)

Chạy trên **2 tài khoản khác mức quyền**: `Luyentq.kd1@tanphat.com` (phạm vi hẹp) và
`namdangit@gmail.com` (toàn quyền).

| # | Trường hợp | Kết quả |
| --- | --- | --- |
| 1 | 2 nút hiện đủ ở cả 2 màn, cả khi vào bằng link `?type=all` | Đạt |
| 2 | Phạm vi dữ liệu theo quyền: báo giá 99 dòng (hẹp) / 3.586 (toàn quyền); bảo hành 0 / 3.631 | Đạt |
| 3 | Popup chọn cột **tick sẵn đúng cột đang hiện**, đúng thứ tự (9/15 và 6/11) | Đạt |
| 4 | Xuất Excel màn báo giá → file 99 dòng, tiền là ô SỐ (`#,##0`) | Đạt |
| 5 | Xuất Excel màn bảo hành 3.631 dòng (2 lượt tải) → đủ 3.631 dòng, 12 cột, **0 ô tiền bị lưu dạng chữ** | Đạt |
| 6 | Bỏ tick hết cột → nút "Xuất file" bị khoá | Đạt |
| 7 | Xuất khi danh sách rỗng → không sinh file rỗng | Đạt |
| 8 | Lọc còn 2 dòng → bản in 2 dòng, file xuất 2 dòng, khớp màn | Đạt |
| 9 | In vượt trần (3.586 / 3.631 dòng) → cắt đúng 2.000 dòng + hiện dòng nhắc thu hẹp bộ lọc | Đạt (sau 2 lần vá) |
| 10 | Bản in: đủ 10 cột đúng thứ tự, có letterhead, tiền có dấu phân cách, không còn biến chưa thay | Đạt |

**2 LỖI THẬT bắt được nhờ test giao diện — đã vá:**

- [x] **Thiếu prop `notice`** ở 2 màn mới → danh sách vượt trần bị cắt bớt mà người dùng không được
      báo gì, in ra thiếu dòng mà không biết.
- [x] **`ReportPrintPreviewModal` dựng `v-else` sai** (lỗi có sẵn, ảnh hưởng CẢ 3 màn làm trước):
      khối nội dung bản in là `v-else` của khối ghi chú → **hễ có dòng nhắc là mất trắng bản in**,
      nút In cũng vô tác dụng. Chỉ hỏng khi danh sách vượt 2.000 dòng nên 3 màn trước lọt qua.
      Sửa `v-else` → `v-if="!loading && !error"`; kiểm lại màn Phiếu cung cấp thông tin (4.980 dòng)
      đã hiện đủ 2.000 dòng + dòng nhắc. Bài học đã ghi vào `.claude/skills/print-page/SKILL.md` §4d.

**Không kiểm được trong môi trường tự động:** bấm nút "In" mở hộp thoại in thật của trình duyệt nên
treo ở chế độ không giao diện — đã kiểm gián tiếp qua bản xem trước (nội dung + nút In bật đúng).

### Chốt lại cách xử lý khi IN DANH SÁCH vượt trần (2026-08-26, sau khi user xem thực tế)

User hỏi: *"sao hiện dòng nhắc rồi mà vẫn hiện danh sách"* → chốt **CHẶN HẲN, không in phần đầu**.
Quy ước cũ (in 2.000 dòng đầu kèm lời nhắc, chốt 2026-08-24) **BỎ**. Lý do: bản in danh sách hay
được ký / lưu hồ sơ — thà không in còn hơn in ra bản thiếu dòng mà người cầm không để ý.

Sửa ở **3 lớp, áp cho cả 5 màn** dùng chung khuôn:

- [x] `LimitsPrintListRows::limitedPrintRows()` — vượt trần thì trả sớm bộ rỗng; `printListPayload()`
      ép `template` về rỗng. Khỏi tải mấy nghìn dòng kèm quan hệ rồi ghép ~1,6 MB HTML để vứt đi
- [x] `ReportPrintPreviewModal` — ẩn bản xem trước (`!notice`) và **ẩn hẳn nút In** (không để nút xám)
- [x] `reportPrintPreviewMixin` — đổi câu nhắc cho khớp thứ người dùng nhìn thấy: *"…vượt mức in tối
      đa 2.000 dòng nên chưa in được. Vui lòng thu hẹp bộ lọc rồi in lại…"* (bản cũ ghi "chỉ lấy
      2.000 dòng đầu" trong khi màn không hiện dòng nào — đọc lên mâu thuẫn)
- [x] **Lỗi bắt được khi kiểm lại:** nhánh `!html → "Không có dữ liệu để in"` chạy TRƯỚC nhánh
      `truncated`, nên vượt trần lại báo *"Không có dữ liệu để in"* trong khi có 4.980 dòng — người
      dùng tưởng mất dữ liệu. Đã đảo thứ tự

**Kiểm lại trên giao diện (màn Phiếu cung cấp thông tin, 4.980 dòng):** vượt trần → chỉ dòng nhắc,
không bảng, không nút In · lọc còn 2 dòng → bản in hiện đủ, nút In có. Skill `print-page` §4d đã
viết lại theo quy ước mới.

### Fix: thanh bên nhảy sang Bán hàng khi mở màn từ CSKH (2026-08-26)

User báo: vào **CSKH → Kiểm tra bảo hành sửa chữa → Yêu cầu kiểm tra sửa chữa – bảo hành** thì thanh
bên nhảy sang phân hệ **Bán hàng**.

**Nguyên nhân (do chính việc nối menu ở phiên này gây ra):** 2 màn được khai ở CẢ menu CSKH lẫn menu
Bán hàng (đúng ERP). `findSubsystemByLink()` chọn phân hệ có link khớp **dài nhất**; hai bên khai
cùng một link nên độ dài **bằng nhau**, code dùng `length > winnerLength` → giữ phân hệ **đứng trước
trong mảng `SUBSYSTEMS`**, tình cờ là Bán hàng (dòng 436) trước CSKH (dòng 450). Quét toàn bộ menu:
đúng **2 link** bị trùng phân hệ, cả hai đều là link tôi thêm vào `sale-hub.js`.

**Hướng xử lý — user chốt: giữ menu đang dùng.** Sửa 1 chỗ trong `components/subsystems.js`:
hoà thì ưu tiên (1) phân hệ đang làm việc nhớ trong `sessionStorage`, (2) phân hệ khớp slug đầu
đường dẫn, (3) thứ tự khai báo. Chỉ ghi nhớ khi đường dẫn thuộc **duy nhất** một phân hệ — để màn
dùng chung tự ghi nhớ là mở nó một lần rồi mọi màn dùng chung sau đó bị kéo theo.

**Kiểm trên giao diện — 3 nhánh:** vào từ CSKH → thanh bên CSKH · vào từ Bán hàng → thanh bên BÁN
HÀNG · xoá ngữ cảnh rồi mở thẳng đường dẫn → CSKH (theo slug). Bài học ghi vào
`.claude/skills/list-page/SKILL.md` §3d-1.

## Bước 3b — SAO CHÉP BÁO GIÁ + Bước 4 — lệnh hết hiệu lực (2026-08-26)

### 3b. Sao chép báo giá

Port từ ERP `getDataCopy()` + `WrServiceQuotation::getForCopy()`; lối vào ERP là
`create?copy=<id>` — HRM dùng **đúng tên tham số** đó.

- [x] `WrQuotationService::prefillFromQuotation()` — tách 3 helper dùng chung với nhánh lập từ
      phiếu cung cấp thông tin (`refreshCatalogValues`, `stripDisplayOnlyFields`, `toPlainArray`)
- [x] `GET wr-quotations/{id}/copy-source` — **gate `canView()`**. ERP để `canCopy()` trả cứng
      `true` vì phạm vi đã chặn từ danh sách, nhưng endpoint gọi thẳng bằng id thì phải tự kiểm,
      nếu không người ngoài phạm vi đọc trọn nội dung báo giá qua đường sao chép
- [x] Bản sao **cắt sạch liên kết** (`parent_id`, phiếu yêu cầu, phiếu xử lý) → là báo giá lập
      độc lập, không phải báo giá thứ hai của phiếu cung cấp thông tin cũ
- [x] **Không chép tệp đính kèm** (tệp thuộc chứng từ đã lập)
- [x] **Làm mới địa chỉ + thuế suất theo danh mục hiện tại** — ERP chú thích rõ: giữ địa chỉ cũ
      thì bản in ra địa chỉ lỗi thời
- [x] FE: hành động **Sao chép** trên từng dòng (hiện với mọi báo giá, đúng ERP) + nhánh `?copy=`
      trong `loadPrefill()`

**Địa chỉ khách hàng — một cái bẫy:** `customers` KHÔNG có cột `address`, ERP ghép bằng accessor
`getAddressAttribute()`. Port công thức sang HRM, đối chiếu **200 báo giá thật**: khớp 184/200.
16 chỗ lệch đều **đúng chủ ý**: khách đã đổi địa chỉ trong danh mục (KH 12739 đổi phường 04/2026,
báo giá lập 08/2025), hoặc dữ liệu cũ bị escape HTML (`B&#039;Lao`) mà bản ghép ra ký tự thật.
⚠️ Số nhà nối bằng **dấu cách**, các cấp hành chính mới nối bằng dấu phẩy — dùng dấu phẩy cho cả
số nhà thì 17/40 địa chỉ lệch.

**Verify trên trình duyệt:** sao chép báo giá `TPSG.BGDV.2025000098` → form điền sẵn khách, SĐT,
hiệu lực 30 ngày, 2 dòng hàng hoá, 5 dòng chi phí; lưu ra `TPE.BGDV.2026010365` với `parent_id`,
phiếu yêu cầu, phiếu xử lý đều rỗng. Đã xoá bản thử, tổng báo giá về 5.170.

**Ghi nhận (không phải lỗi mới):** đối chiếu 60 báo giá CÓ hàng hoá thì 57 khớp tổng, 3 lệch —
truy ra là **ERP không tính lại tổng khi sửa dòng con sau lúc lập** (phiếu lập 04/08, dòng hàng
hoá sửa 18/08, tổng vẫn giữ số cũ). HRM đã chặn điểm này bằng `syncTotals()`.
Ngoài ra DB còn **7 dòng hàng hoá mồ côi** của ERP (phiếu gốc đã xoá, 11/2025–07/2026) — không
đụng vào vì là dữ liệu thật.

### 4. Lệnh chạy nền: báo giá hết hiệu lực

- [x] `customer-care:expire-quotations` (có `--dry-run`) + lịch **00:30 hằng ngày**, đúng khung
      giờ ERP (`update:quotations-expried`) để hai hệ thống không chuyển lệch nhau
- [x] `WrQuotationService::expire()` — đổi trạng thái Duyệt → Hết hiệu lực
- [x] Chạy thử: liệt kê đúng **116** báo giá quá hạn; thử `expire()` 1 phiếu → trạng thái đổi,
      lịch sử ghi "Duyệt → Hết hiệu lực" kèm ghi chú, `updated_by` **giữ nguyên**; đã hoàn nguyên

**2 điểm KHÁC ERP có chủ ý:**
- ERP đổi hàng loạt bằng một câu `update()` → không ghi lịch sử, người dùng thấy trạng thái tự
  nhảy mà không có dòng nào giải thích. HRM đi từng phiếu để **ghi lịch sử** (quy ước bắt buộc,
  skill `entity-history`), kèm ghi chú "Hệ thống tự chuyển khi báo giá quá hạn hiệu lực". Người
  thực hiện để trống → giao diện hiển thị **"Hệ thống"** (đã có sẵn, không phải sửa).
- Bỏ qua phiếu **không đặt số ngày hiệu lực** (null / 0) — ERP không loại nên phiếu để trống bị
  coi là hết hạn ngay ngày lập. Trên dữ liệu thật hiện **không có phiếu nào** như vậy nên kết quả
  hai bên vẫn bằng nhau; đây chỉ là lưới an toàn.
- Không đụng `updated_by`: hệ thống chuyển theo hạn, không phải ai đó sửa phiếu — ghi đè vào đây
  là xoá mất dấu người sửa cuối.

**⚠️ CHỜ USER QUYẾT 2 việc:**
1. **Chạy thật lần đầu sẽ đổi 116/121 báo giá** đang ở trạng thái Duyệt (tồn đọng vì HRM chưa từng
   chạy lệnh này). Chưa chạy.
2. **Trên môi trường thật, ERP đang chạy `update:quotations-expried` trên CÙNG cơ sở dữ liệu.**
   Bật cả hai thì bên nào chạy trước sẽ đổi trạng thái, và nếu ERP chạy trước thì HRM **không ghi
   được lịch sử** (phiếu đã rời trạng thái Duyệt). Nên tắt lệnh bên ERP khi bật bên HRM.

### BỘ KIỂM Sao chép báo giá + Lệnh hết hiệu lực (2026-08-26)

**91/91 trường hợp đạt.** Chạy trên **4 tài khoản khác mức quyền**: 13 (toàn quyền), 428 (phạm vi
hẹp), 62 (người lập phiếu yêu cầu), 242. Mật khẩu `namdangit@gmail.com` giữ nguyên `2025Dns@2`.

| Nhóm | Nội dung | Kết quả |
| --- | --- | --- |
| A (13) | Chốt chặn API `copy-source`: ngoài phạm vi 403 · id lạ / id phiếu cung cấp thông tin / id phiếu bảo hành 404 · chưa đăng nhập 401 · **phiếu nháp của người khác 403** | 13/13 |
| B (42) | Dữ liệu bản sao trên 3 loại báo giá (có thiết bị SC · có bảo hành · lập từ phiếu gốc): cắt liên kết, không mang id/mã, không chép tệp, chép đủ mọi khối con, bỏ hết trường chỉ để hiển thị | 42/42 |
| C (13) | Lệnh hết hiệu lực: tập phiếu **trùng khít câu SQL của ERP** (116=116) · chỉ đổi trạng thái Duyệt · Đang tạo / Đã tạo hợp đồng / Hết hiệu lực đều không đổi và **không ghi log** · chạy lại an toàn · giữ nguyên người cập nhật | 13/13 |
| D (3) | `--dry-run` không ghi gì (đếm trước/sau bằng nhau) · liệt kê 116 dòng · `schedule:list` xác nhận `30 0 * * *`, lần chạy kế 27/08 00:30 | 3/3 |
| E (9) | Hồi quy: lập báo giá từ phiếu cung cấp thông tin vẫn chạy sau khi tách helper · màn phiếu cung cấp thông tin không đổi (4.980) · **nhãn trạng thái không lẫn giữa 2 loại chứng từ** (số 2 = "Duyệt" ở báo giá, "Chờ làm báo giá" ở phiếu) | 9/9 |
| F (11) | Hồi quy API: xuất Excel + in danh sách của cả 3 màn, chi tiết, in 1 báo giá, gate quyền | 11/11 |

**Giao diện (Playwright):** nút Sao chép hiện ở **10/10 dòng** (đúng ERP, không gate) · bấm nút →
form nạp đúng khách + mọi khối con, **không lộ mã báo giá cũ** · bản sao **đổi được khách hàng**
(popup mở bình thường — khác nhánh lập từ phiếu gốc bị khoá) · lưu ra bản ghi mới cắt sạch liên
kết · **tài khoản quyền hẹp gõ thẳng URL sang báo giá ngoài phạm vi → bị chặn, báo "Bạn không có
quyền xem báo giá này", chuyển về danh sách** · cảnh báo "chưa lưu" hoạt động.

**4 lần "KHÔNG ĐẠT" đều là kỳ vọng sai của tôi, không phải lỗi màn — đã truy đến cùng:**
- báo giá `80` bị 403 với cả tài khoản toàn quyền → hoá ra là **phiếu nháp của người khác**, đúng
  ra phải chặn. Giữ lại thành case A9
- `prefill` trả 403 với tài khoản toàn quyền → điều kiện ERP là **phải là người lập phiếu yêu cầu**,
  không phải quyền xem. Đổi sang tài khoản 62 thì 200; thêm case nghịch F1b
- đếm số phiếu màn cung cấp thông tin: công thức kỳ vọng tôi tự viết lại sai, số thật 4.980 đúng
- "thoát không cảnh báo chưa lưu": mixin chỉ tính bẩn khi có **phím/chuột thật**, mà `fill()` của
  Playwright đặt giá trị bằng JS nên không phát `keydown`. Gõ từng ký tự thì popup hiện đúng

**Một khác biệt cần biết khi dùng:** bản sao có thể ra **tiền khác bản gốc** nếu danh mục đã đổi
thuế suất — đo thật trên báo giá `TPE.BGDV.2026007040`: bản gốc lưu VAT 0% cho 2 dòng sửa chữa,
danh mục lỗi thiết bị nay là 8% nên bản sao ra 2.067.120 thay vì 2.010.000. **Đây là chủ ý** (ERP
`getForCopy()` cũng gán lại VAT từ danh mục): báo giá mới phải dùng thuế suất hiện hành.

**Dữ liệu sau kiểm thử:** tổng báo giá 5.170 · Duyệt 121 · Hết hiệu lực 1.594 — đúng bằng số trước
khi test; đã xoá 3 bản ghi thử và 6 dòng lịch sử của chúng. 7 dòng hàng hoá mồ côi vẫn là dữ liệu
cũ của ERP, không đụng.

## Bước 3a — THÊM THIẾT BỊ THỦ CÔNG vào báo giá (bắt đầu 2026-08-27)

### Khảo sát ERP (đọc code, không suy đoán)

Khối "I - Dịch vụ kiểm tra, sửa chữa" của form báo giá ERP có nút **"Thêm mới"** →
`addCustomerProduct()` → mở popup `customerProductModal` = **DANH SÁCH THIẾT BỊ CỦA KHÁCH**,
chứ KHÔNG phải chọn tự do trong danh mục hàng hoá.

Thiết bị của khách gom từ **3 nguồn** (`CustomerManagerController::getListProductOfCustomer`):

| Nguồn | Bảng | Ý nghĩa |
| --- | --- | --- |
| Tân Phát | `product_export_requests` | thiết bị đã xuất kho / bán cho khách |
| Thiết bị cũ | `equipments_old` | khách tự khai, hàng Tân Phát nhưng không có chứng từ xuất |
| NCC khác | `external_equipments` | hàng của nhà cung cấp khác — chọn kèm **thiết bị tương đương** trong danh mục để tra lỗi/giá |

Popup `#oldEquipment` của ERP có **2 nhánh**: `form2` → `add-old-equipment-customer`, và `form3` →
`add-external-equipment-customer` (nhánh này mới là chỗ dùng `searchProductEquivalent`).
Chọn xong, máy chủ trả kèm **lỗi thiết bị mặc định của hàng hoá đó** (`DeviceErrorProduct`) để form
tự đổ dòng công việc.

### Hiện trạng HRM — phần lớn đã có sẵn

- [x] Máy chủ: `GET assign/customers/{id}/equipment` (gom đủ 3 nguồn) · `POST .../equipment/old` ·
      `POST .../equipment/external` · `add-quantity` · `equipment/{type}/{eqId}`
- [x] Giao diện: màn **Phiếu yêu cầu kiểm tra SC-BH** đã có 4 popup dùng được lại —
      `ChooseEquipmentTypeModal` · `AddOldEquipmentModal` · `AddExternalEquipmentModal` ·
      `AddEquipmentQuantityModal`
- ⚠️ **Lệch cần sửa:** form Báo giá đang dùng `ProductSearchModal` (chọn tự do trong danh mục hàng
      hoá) — không đúng ERP, và cho phép báo giá thiết bị khách không hề có

### Việc phải làm
- [ ] Đổi nút thêm dòng ở khối A/B của form báo giá sang chọn từ **thiết bị của khách**, dùng lại
      popup của màn Phiếu yêu cầu (tách dùng chung, KHÔNG copy sang thư mục mới)
- [ ] Nối 2 popup khai báo thiết bị mới (Tân Phát / NCC khác + thiết bị tương đương)
- [ ] Đổ dòng kèm **lỗi thiết bị mặc định** của hàng hoá
- [ ] Tạo lỗi thiết bị nhanh ngay trong form (ERP: `CreateDeviceErrorModal`)
- [ ] Kiểm thử nhiều tài khoản + dọn dữ liệu thử

### Bộ kiểm bước 3a (2026-08-27)

**Máy chủ — 12/12 đạt** (2 tài khoản): chọn 1 lỗi → 1 dòng · 3 lỗi → 3 dòng · không chọn → 1 dòng
trống · hàng hoá không tồn tại / id lỗi lạ / id trùng đều không vỡ · chưa đăng nhập 401 · tài khoản
quyền hẹp dùng được · lấy lỗi cho 2 hàng hoá trong **1 request** · **lỗi đã khoá không lọt vào ô
chọn**. Số liệu: giá vốn công `350.000 = 700.000 × 0,5` đúng công thức ERP, giá bán = giá của lỗi,
giữ nguyên serial / nguồn / NCC / model / số biên bản.

**Hồi quy — 7/7 đạt**: 4 màn của luồng + danh mục loại lỗi + nhân bản báo giá + danh sách thiết bị
của khách vẫn chạy sau khi **di chuyển 5 popup** sang thư mục dùng chung.

**Giao diện**: màn Phiếu yêu cầu mở popup khai báo thiết bị bình thường sau khi popup đổi chỗ ·
nút "Thêm thiết bị" hiện đủ ở **cả 2 khối** của báo giá · popup chọn thiết bị mở đúng 11 cột, có ô
Nguyên nhân lỗi (51 lỗi của hàng hoá) + nút Thêm nhanh · **chưa chọn nguyên nhân mà bấm Chọn thì bị
chặn** · chọn xong thì thêm dòng đúng, mang đủ định mức công, dịch vụ và vật tư.

**3 LỖI THẬT bắt được nhờ chạy giao diện — đã vá:**
- [x] **Gửi sai khoá tham số**: `apiPostMethod` đọc `options.payload`, tôi viết `data` → request đi
      với **thân rỗng**, máy chủ trả `[]` mà không có lỗi nào báo ra. Ô Nguyên nhân trống trơn.
- [x] **Chọn nhiều không bật**: `V2BaseSelectInModal` đọc cấu hình từ `extraSettings`, khai thuộc
      tính `multiple` trần thì ô vẫn ở chế độ chọn MỘT, im lặng.
- [x] **Nguồn thiết bị lưu sai mã**: gửi thẳng `external_old` (tên của giao diện) thay vì `tpc` như
      ERP → dòng mang mã lạ, khác 4.364 dòng dữ liệu thật. Đã map qua `EQUIPMENT_TYPE_MAP`.

**Chọn NHIỀU lỗi — đã chạy đúng ERP.** Hai nguyên nhân, mất khá lâu mới tách bạch được:

- **Nguyên nhân thật:** `V2BaseSelectInModal` mặc định lọc option đã khoá dựa trên **chính giá trị
  đang chọn** (`filterUnusedLockedOptions(options, currentValue)`). Với ô chọn-nhiều thì mỗi lần
  tích thêm một lỗi là danh sách options được tính lại thành **mảng mới**, select2 dựng lại và mất
  sạch lựa chọn. Component có sẵn prop **`keepLockedOptions`** để bỏ bước lọc đó — danh mục ở đây
  máy chủ đã lọc `status = 1` nên không có lỗi khoá nào cần giấu.
- **Một nửa là lỗi của cách tôi test:** select2 chọn-nhiều vẫn liệt kê option ĐÃ CHỌN, click lại
  chính nó là **bỏ chọn**. Kịch bản của tôi click `nth=0` hai lần nên lần hai bỏ đúng lỗi vừa
  chọn → tưởng là mất dữ liệu. Chọn theo TÊN lỗi khác nhau thì giữ đủ.

**Kết quả cuối:** chọn 2 lỗi → giữ cả 2 chip → bấm Chọn ra **2 dòng công việc**, mỗi dòng mang giá
vốn / giá bán / VAT riêng của lỗi đó, nguồn thiết bị đúng mã ERP (`tpc`).

---

## Phase — Sửa lỗi QA đợt 26/08 (Redmine #11207, #11230, #11240, #11241, #11242)

### #11207 — Bản in
- [x] BE: `NGUOI_YEU_CAU` / `PHONG_YEU_CAU` tra ngược phiếu yêu cầu gốc khi cột trên phiếu trống
- [x] BE: Resource chi tiết + danh sách cũng tra ngược `department_requester` (màn hình khớp bản in)
- [x] FE: CSS xem trước/in ép `font-weight: 400 !important` cho mọi ô bảng → mất chữ đậm inline của mẫu ERP
- [x] BE: in danh sách — ô "Thời gian" trống thì ghi "Tất cả"
- [x] BE: in danh sách — "Ngày nhận yêu cầu" lấy `send_request_time` của phiếu xử lý (quan hệ cũ không select `created_at` nên cột luôn rỗng)
- [x] BE: in danh sách — "Ngày tạo" hiện cả giờ
- [x] BE: bảng Tổng hợp báo giá của bản in thêm hạng mục "Bảo hành" + đổi điều kiện ẩn dòng (phiếu chỉ có bảo hành trước đây ra bảng trống, không dòng nào có STT)
- [x] Quy tắc dấu `.`/`,`: GIỮ kiểu Anh `357,000` — user chốt 2026-08-27, đúng commit "sửa quy tắc số" 26/08

### #11230 — Xuất Excel
- [x] Letterhead chặn trần 900px (trước kéo bằng cả bề rộng bảng = 1.590×142px)
- [x] Cột "Tên thiết bị liên quan" hiện MẶC ĐỊNH ở màn Yêu cầu sửa chữa – bảo hành
- [x] **Vòng 2 (28/08) — logo vẫn đè tiêu đề trên MỘT SỐ MÁY.** Gốc rễ: ảnh neo `oneCellAnchor`
      + `ext` = kích thước TUYỆT ĐỐI, không dính gì tới chiều cao dòng 1; máy nào Excel không áp
      đúng `row height` là ảnh tràn xuống dòng 2-3. Đổi sang **neo 2 ô** (`tl` + `br`, `br.row = 1`)
      → biên dưới ảnh CHÍNH LÀ biên dưới dòng 1, không máy nào tràn được nữa.
- [x] Gộp cả dòng 1 (`mergeCells`) để nó là dòng THẬT — dòng rỗng thì có bản Excel bỏ qua chiều cao
- [x] Letterhead **căn giữa** bảng thay vì kéo dài hết bảng (user chốt 28/08), thẳng trục với dòng
      tiêu đề ngay dưới. Neo bằng `nativeColOff` (EMU) chứ KHÔNG dùng `col` số thực: ExcelJS quy đổi
      phần lẻ của `col` bằng `width × 10000`, không phải pixel thật → đo ra lề 56/127 thay vì cân.
      Sau khi sửa: rộng đúng 900px, lề trái 107 / lề phải 106.

### #11240 — Form phiếu
- [x] Ô tìm trong popup "Chọn dịch vụ sửa chữa" có nút xoá (x)
- [x] Popup "Chọn dịch vụ sửa chữa" cuộn dọc được (lớp div của `V2BaseTableScroll` chặn `flex` của vùng cuộn)
- [x] Lỗi 500 `engineering_work cannot be null` — BE zero-fill cột số NOT NULL của 3 bảng dòng, `engineering_work_qty` mặc định 1
- [x] Popup "Chọn hàng hoá áp dụng": bật `add-on-row-click`
- [x] Khoá ô chọn MẪU điều khoản ở màn Sửa (user chốt; ERP thực đo KHÔNG khoá — đã báo lại)
- [x] Ô "Thời gian có vật tư (ngày)" chỉ nhận chữ số
- [x] **Vòng 3 (28/08) — chốt cách làm chuẩn.** Bỏ hết chặn ký tự tự chế, chuyển sang rule CHUNG
      `positive_integer` + `V2BaseError` (báo "Giá trị phải là số nguyên dương."), và thêm rule
      tương ứng ở `WrServiceQuotationRequest` — chặn cả khi Lưu nháp. Đã đo: gửi thẳng API với
      `time_to_has = 'abc'` ở trạng thái NHÁP → BE trả 422 đúng khoá dòng.
      Phát hiện `validateAll()` bỏ qua mọi ô nằm trong component con (lọc theo `vmId`) → phải gọi
      `validateAll(null, { vmId: null })`; đã ghi vào `form-validate` mục 3c.
      ⚠️ Trước khi có rule BE, chuỗi `xyzabc` ĐÃ lọt vào `wr_service_quotation_product_services`
      của phiếu 10321 trên DB local — đã dọn tay.
- [x] **Vòng 2 (28/08) — vẫn nhập được chữ.** Lọc ở `@input` mới sạch DỮ LIỆU, còn MÀN HÌNH vẫn hiện
      chữ: `V2BaseInput` render `:value`, chuỗi lọc ra trùng giá trị cũ (gõ `1` rồi `a` → vẫn `"1"`)
      nên prop không đổi, Vue không render lại. Đã chặn thêm ở `@keypress` + xử lý riêng `@paste`
      (ép lại thẳng thẻ input). Kiểm bằng gõ TUẦN TỰ: `1abc2xyz3` → `123`, dán `12abc` vào ô đang
      `12` → `12`. Ghi bẫy này vào skill `select-and-input-state` mục 4b.
- [x] Đổi nhãn "Người lập" → "Người tạo" (3 màn cùng luồng CSKH)
- [x] Trường "Phiếu xử lý yêu cầu" ở màn chi tiết có khung ô như các trường khác

### #11241 — Công thức bảng chi phí
- [x] "Chi phí cho SC - BD" = Giá trị − Cho bảo hành, KHÔNG cho nhập tay (cả bảng I và II)
- [x] "Trả phí" = Cho bảo hành − Miễn phí; "Khách hàng phải trả" = Trả phí + SC-BD
- [x] Chặn "Cho bảo hành" > "Giá trị" và "Miễn phí" > "Cho bảo hành" (đúng ERP)
- [x] **Đối chiếu ERP thật (28/08, cổng 8001, phiếu 10311/10321)** — chạy song song cùng bộ số:
      `1.000.000 / 400.000 / 100.000` → ERP và HRM cùng ra `300.000 / 600.000 / 900.000`;
      "Miễn phí" vượt "Cho bảo hành" → cả hai đưa về 0; 2 cột SC-BD và Khách phải trả ở ERP cũng là
      ô TÍNH, không nhập.
- [x] **Lệch phát hiện thêm: 3 cột "Cho bảo hành / Miễn phí / Trả phí" chỉ hiện khi phiếu CÓ thiết
      bị bảo hành** (`ng-if="form.product_warrantys.length"`). HRM đang hiện cho mọi phiếu → phiếu
      thuần sửa chữa bày thừa 3 ô, điền vào là sai tiền. Đã thêm prop `showWarranty`; đo lại:
      phiếu 10321 (không bảo hành) ra 6 cột / 2 ô nhập — **đúng y ERP**; phiếu 10081 (có bảo hành)
      vẫn đủ 9 cột.
- [ ] ⚠️ **CÒN 1 ĐIỂM CỐ Ý LỆCH ERP — chờ user chốt.** Nhập "Cho bảo hành" VƯỢT "Giá trị" trong khi
      "Miễn phí" đang có số: ERP đưa "Cho bảo hành" về 0 nhưng GIỮ "Miễn phí" → Trả phí ra **ÂM**
      (đo thật: −100.000). HRM đang dọn "Miễn phí" về 0 nên Trả phí = 0. Giữ cách của HRM hay bám
      đúng ERP kể cả khi ra số âm?

### #11242 — Màn sửa thiếu bảng
- [x] Khối D dựng đủ 3 bảng như ERP: I - Bảo hành · II - Sửa chữa - Bảo dưỡng · III - Tổng hợp báo giá
- [x] Bảng III bám ERP: 2 hạng mục Bảo hành / Sửa chữa bảo dưỡng, luôn hiện kể cả bằng 0

### Checkpoint — 2026-08-27
Vừa hoàn thành: toàn bộ 5 task Redmine ở trên. Đối chiếu trực tiếp với ERP local (cổng 8001) trên
cùng phiếu 10081 — bảng I và II của khối D khớp từng con số với ERP.
Đang làm dở: không có.
Bước tiếp theo: tester chạy lại 5 task trên bản HRM.
Blocked: không có.

## Fix: 2 lối vào cùng một màn cho ra CÙNG kết quả — sai ERP (user phát hiện 2026-08-27)

**Hiện tượng user báo:** vào màn Yêu cầu kiểm tra sửa chữa – bảo hành từ **Bán hàng** và từ **CSKH**
ở HRM ra giống hệt nhau, trong khi ERP hai lối cho hai danh sách khác nhau.

**Nguyên nhân — lỗi của tôi ở bản port đầu.** ERP có **4 mục menu** trỏ vào màn này, tôi chỉ đọc 2:

| Lối vào ERP | Tham số | Phạm vi |
| --- | --- | --- |
| CSKH → Kiểm tra bảo hành sửa chữa (dòng 1918) | `?type=all` | gate 3 cấp quyền |
| Bán hàng → Lắp đặt-BH-SC (371) | **route trần** | `index` = chỉ phiếu của mình |
| Bán hàng → Báo giá dịch vụ (495) | **route trần** | `index` = chỉ phiếu của mình |
| Bán hàng → trang tổng quan (438) | `?type=all` | gate 3 cấp quyền |

Chú thích tôi viết trong `WarrantyRepairRequestService` khẳng định *"menu luôn trỏ `?type=all`"* —
đọc sót 2 mục vào route trần. Hậu quả lan sang **cả 4 màn** của luồng: đều để mặc định `SCOPE_ALL`.

**Sửa đủ BA nơi** (thiếu một là không đổi gì — giao diện vẫn gửi `type=all` lên):
- [x] Máy chủ: `get('type', self::SCOPE_MINE)` cho cả 4 service
- [x] Giao diện: `initialStateForm.type` đổi `'all'` → `'index'` ở cả 4 màn
- [x] Menu CSKH: thêm `?type=all` (và `?permission=all` cho phiếu cung cấp thông tin — ERP dùng tên
      tham số khác ở màn này); menu Bán hàng giữ route trần
- [x] `applyQueryType()` của 4 màn nhận **cả `type` lẫn `permission`**

**Đo lại sau khi sửa** (tài khoản quản trị): route trần → **6 / 5 / 1 / 0** phiếu · `?type=all` →
**5.371 / 5.258 / 4.980 / 3.631**. Đối chiếu nhánh mặc định với công thức ERP
(`COUNT(*) WHERE created_by = 13`): **khớp cả 4 màn**.

Bài học ghi vào `.claude/skills/list-page/SKILL.md` §3d-2, kèm cách tra menu ERP cho đủ và cách tự
kiểm bằng số.

### Tài liệu — bổ sung 28/08
- [x] `Mô tả nghiệp vụ - Phiếu cung cấp thông tin làm báo giá.docx`: thêm mục **8.5 Cách tính tiền
      trên phiếu** (5 mục con theo 4 khối A/B-I/B-II/C + khối D tổng hợp), viết bằng ngôn ngữ
      nghiệp vụ, nêu rõ ô nào NHẬP ô nào TỰ TÍNH và 3 cột bảo hành chỉ hiện khi phiếu có thiết bị
      bảo hành. Bộ kiểm thuật ngữ kỹ thuật: sạch.
