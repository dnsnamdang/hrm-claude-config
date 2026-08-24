# Plan — Phiếu xử lý yêu cầu (chứng từ 2 dây chuyền dịch vụ)

Người phụ trách: @namdangit · Nhánh `gop_db`
Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-08-20-warranty-repair-handle-request-design.md`

## Phase 0 — Khảo sát ERP
- [x] Đọc controller / model / model con / validate / blade / route / mẫu in / quyền
- [x] Đối chiếu 3 bảng trên DB gộp (`warranty_repair_handle_requests` 5.259 dòng)
- [x] Chốt phạm vi với user (full parity · toast cho nút CCTT · DB local tạo thoải mái)
- [x] Viết design.md + spec chi tiết

## Phase 1 — BE nền ✅
- [x] Entity `WarrantyRepairHandleRequest` (6 trạng thái + màu chuẩn + 2 hành động xử lý + 4 tên
      quyền + `canEdit` / `isCanDelete` / `canCreateRepairInformation` / `canReject` / `canView`)
- [x] Entity `WarrantyRepairHandleRequestProduct` + `...ProductManageDeviceError`
- [x] `WarrantyRepairHandleRequestService`: list/filter/scope 3 cấp quyền (nhánh phòng ban CỘNG
      phòng đang công tác), prefill từ phiếu yêu cầu, store/update/syncProducts (nhiều lỗi thiết bị
      + tự khai thiết bị ngoài khi `type = new`), reject, delete (trả phiếu yêu cầu gốc về "Chờ xử
      lý"), exportRows
- [x] `WarrantyRepairHandleRequestNotifier` — prefix `[PXL]`, báo theo QUYỀN "Tạo phiếu cung cấp
      thông tin" + cùng công ty; bổ sung báo người lập khi bị từ chối (ERP không có)
- [x] `WarrantyRepairHandleRequestPrintService` — mẫu in 273 / 276, đủ 16 + 3 biến
- [x] FormRequest: bắt buộc theo `status`, "Tư vấn điện thoại" bắt nhập nội dung, thiết bị nhập tay
      phải chọn hàng hóa tương đương, chặn trùng (thiết bị + serial + loại + giao nhau lỗi)
- [x] Controller + 12 route `/v1/customer-care/warranty-repair-handle-requests`
- [x] 4 quyền id 1511–1514 vào `PermissionsTableSeeder`; đồng thời sửa `type` của 4 quyền chứng từ 1
      (1507–1510) từ 23 Bán hàng → **24 CSKH** cho khớp phân hệ mới
- [x] Đăng ký 14 cột xuất Excel vào `ExportColumnRegistry`

### Kiểm chứng BE (HTTP thật trên :8003, DB gộp)
| Kịch bản | Kết quả |
| --- | --- |
| Danh sách | 200 · **5.255 phiếu** · badge màu chuẩn · 4 cờ `is_can_*` |
| Chi tiết | 200 · dòng thiết bị trả `action_id` + `action_name` + mảng lỗi + tên lỗi |
| Danh mục lỗi thiết bị | 200 · 171 mục khớp từ khoá · có cờ `is_locked` |
| Lấy dữ liệu điền sẵn từ phiếu yêu cầu | 200 · chép đủ người/phòng/ngày nhận + thiết bị |
| Gửi đi thiếu Nguyên nhân + Hành động | 422 đúng 2 ô |
| "Tư vấn điện thoại" thiếu nội dung xử lý | 422 tại đúng dòng |
| Lưu nháp thiếu hết | 201 (đúng chốt, khác ERP) |
| Gửi đi (CCTT làm báo giá) | phiếu **Chờ CCTT** · đóng dấu giờ gửi · phiếu yêu cầu gốc → **Đã xử lý** + người/ngày xử lý |
| Thông báo | **7 người** có quyền "Tạo phiếu cung cấp thông tin" cùng công ty nhận `[PXL] Chờ duyệt: <b>mã</b>. Khách hàng: …` |
| Mọi dòng = "Tư vấn điện thoại" | phiếu tự thành **Đã tư vấn điện thoại**, phiếu yêu cầu gốc cũng vậy |
| Sửa phiếu đã gửi | **423** |
| Xoá phiếu đã gửi | chặn |
| Xoá phiếu nháp | phiếu yêu cầu gốc **trở lại "Chờ xử lý"**, xoá người/ngày xử lý |
| Không duyệt thiếu lý do / có lý do | 422 · về "Đang tạo" + lưu lý do |
| In 1 phiếu / In danh sách | 0,3s · **0 placeholder sót** · có đủ mã phiếu, phiếu yêu cầu, nguyên nhân, hành động |
| Xuất dữ liệu theo trang | 0,3s · 15 cột (kèm STT) |
| Ghi dữ liệu | bảng nối lưu đúng lỗi; `device_error_id` trên bảng dòng = NULL đúng như ERP |

## Phase 2 — FE ✅
- [x] Màn danh sách `pages/customer-care/warranty-repair-handle-requests/index.vue` — 10 cột ERP
      (Số phiếu xử lý · Số phiếu yêu cầu · Khách hàng · Người yêu cầu · Ngày nhận yêu cầu · Người
      xử lý · Ngày xử lý · Trạng thái · Hành động), badge màu do BE trả, bộ lọc bám ERP
      (trạng thái · số phiếu yêu cầu · khách hàng · tên thiết bị · model · khoảng ngày · công ty –
      phòng ban), tìm nhanh 3 trường, phân trang, tùy chỉnh cột, xuất Excel chia trang, in danh sách.
      **KHÔNG có nút "Tạo mới"** — đúng ERP (`create_link` bị comment): phiếu chỉ sinh từ chứng từ 1.
- [x] Form dùng chung `WarrantyRepairHandleRequestForm.vue` (lập / sửa / xem): khối "Thông tin yêu
      cầu" chỉ đọc + bảng thiết bị có cột **Nguyên nhân** (select2 nhiều lỗi, tự gắn 🔒 cho lỗi đã
      khoá) và **Hành động** (2 lựa chọn; "Tư vấn điện thoại" hiện thêm ô Nội dung xử lý bắt buộc)
- [x] `create.vue` (lập từ `?warranty_repair_request_id=`) · `_id/index.vue` (xem) · `_id/edit.vue`
      (sửa, vào bằng URL khi phiếu đã gửi thì đá về màn xem) · `print.vue` + `_id/print.vue`
- [x] `RejectHandleRequestModal.vue` — popup "Không duyệt", bắt buộc lý do
- [x] Menu CSKH → Kiểm tra bảo hành sửa chữa → **Phiếu xử lý yêu cầu** đã gắn link
- [x] Nối nút "Tạo phiếu xử lý yêu cầu" của chứng từ 1 (cả màn danh sách lẫn màn chi tiết) sang
      màn lập phiếu — bỏ toast tạm

### Lỗi tự phát hiện khi test FE
- [x] **Màn chi tiết trắng trơn, không gọi API**: `loadDetail()` gọi `$nuxt.$loading.start()` trong
      khi watcher `id` chạy `immediate: true` — lúc đó Nuxt chưa gắn xong thanh loading nên ném
      `finish is not a function`, nhảy thẳng vào `catch`, request chi tiết KHÔNG BAO GIỜ được gửi và
      **không có lỗi nào hiện trên giao diện**. Bỏ `$loading` khỏi `loadDetail`/`loadPrefill` (chứng
      từ 1 vốn cũng không dùng), ghi chú cảnh báo ngay tại chỗ.
- [x] Màn chỉ đọc mà dòng không có tệp thì hiện `—` thay vì nút "Chọn tệp" xám (nút không dùng được
      thì ẩn hẳn — CLAUDE.md).

### Kiểm chứng FE (trình duyệt :3002)
| Kịch bản | Kết quả |
| --- | --- |
| Danh sách | 5.256 phiếu · 10 cột đúng ERP · badge màu chuẩn |
| `?type=waiting_information` | 24 phiếu Chờ CCTT · mỗi dòng đủ Tạo phiếu CCTT · Không duyệt · In |
| Từ chứng từ 1 bấm "Tạo phiếu xử lý yêu cầu" | mở đúng màn lập kèm `?warranty_repair_request_id=`, chép sẵn 8 ô chỉ đọc + thiết bị |
| Gửi khi thiếu Nguyên nhân/Hành động | lỗi inline tại đúng ô |
| Chọn "Tư vấn điện thoại" | hiện ô Nội dung xử lý; bỏ trống → lỗi inline |
| Lưu và gửi (mọi dòng tư vấn ĐT) | phiếu **Đã tư vấn điện thoại**, phiếu yêu cầu gốc cũng vậy |
| Màn chi tiết | tiêu đề kèm mã · nguyên nhân + hành động + nội dung xử lý hiển thị đúng · link ngược sang phiếu yêu cầu |
| In 1 phiếu | khung giấy 794px · 0 placeholder sót · có nguyên nhân + hành động |

## Phase 3 — Test & tài liệu
- [ ] Test BE qua HTTP thật (:8003) + FE qua trình duyệt (:3002)
- [ ] Đối chiếu từng luồng với ERP
- [ ] testcase.xlsx + mô tả nghiệp vụ (khi user yêu cầu)

## Phase 3 — Rà soát đối chiếu ERP + soát lại theo skill (2026-08-20)

### Lệch ERP tự phát hiện khi rà — đã sửa
- [x] **Danh mục "Nguyên nhân" đang đổ CẢ danh mục lỗi (2.754 bản ghi)**. ERP chỉ cho chọn trong
      những lỗi **đã gắn với chính hàng hóa đó** (`device_error_products`, xem
      `WarrantyRepairHandleRequestProduct::getDeviceErrorsAttribute()`). Sửa: BE trả
      `device_error_options` **theo từng dòng thiết bị**; endpoint `device-errors` nhận thêm
      `product_id`. Đo thật: hàng hóa 33439 → đúng **1 lỗi**; dòng của phiếu 5285 → **21 lỗi**.
- [x] **Mất lỗi đã chọn khi lỗi bị khoá**: ERP `edit()` merge thêm lỗi `STATUS_BLOCK` đang được
      chọn vào danh sách. Sửa: `deviceErrorOptionsForProduct()` gộp sẵn `selectedIds` kể cả đã khoá,
      trả kèm `is_locked` để FE tự gắn 🔒.
- [x] **Thiếu hiển thị "Thiết bị tương đương"**: ERP hiện `product_no_sale_name || product_name`,
      tên hàng hóa trong danh mục thành dòng phụ. Đã bám đúng — kiểm trên phiếu 5275.
- [x] **Thiếu chọn HÀNG HÓA TƯƠNG ĐƯƠNG cho thiết bị `type = new`** (151 dòng thật trong DB): ERP
      có nút bút chì mở popup chọn hàng hóa, và validate bắt buộc trường này. Đã thêm nút dùng lại
      popup `ProductSearchModal` của màn Gói bảo dưỡng; đổi hàng hóa thì nạp lại danh mục nguyên
      nhân của dòng.

### Soát lại theo skill `list-page` — đã sửa (user nhắc 2026-08-20)
- [x] **Bộ cột mặc định sai mục 6**: đang hiện 10 cột. Sửa còn **7 cột** đúng chuẩn
      (STT · Số phiếu xử lý · Khách hàng · Người xử lý · Ngày tạo · Trạng thái · Hành động — Khách
      hàng là ngoại lệ được phép). 7 cột nghiệp vụ còn lại chuyển `isVisible: false`.
- [x] **Sort sai mục "Cột nào được sort"**: đang cho sort cột Khách hàng (chữ) và Trạng thái (badge).
      Bỏ, chỉ còn Số phiếu + các cột ngày. Sửa cả whitelist `SORT_FIELDS` của BE cho khớp.
      **Sửa cùng lỗi này ở chứng từ 1.**
- [x] **Ô tìm nhanh thiếu "Người tạo"** (mặc định của skill là Mã + Tên + Người tạo): bổ sung tìm
      theo người xử lý bằng `EXISTS` (không join, tránh phình câu COUNT), cập nhật placeholder.

### Kiểm chứng lại sau khi sửa
| Kịch bản | Kết quả |
| --- | --- |
| Cột mặc định | đúng 7 cột; chỉ Số phiếu + Ngày tạo có sort |
| Tìm nhanh "DNS Admin" | 2 phiếu, đều đúng người xử lý |
| Lọc trạng thái "Chờ CCTT" | 24 phiếu, cột trạng thái đồng nhất |
| Xuất Excel | tải về `danh_sach_phieu_xu_ly_yeu_cau.xlsx` |
| Không duyệt qua UI | popup đúng chữ ERP; thiếu lý do → lỗi inline; có lý do → phiếu rời khỏi danh sách Chờ CCTT (24 → 23) |
| Nguyên nhân theo dòng | 21 lựa chọn của đúng hàng hóa, giữ nguyên lỗi đã chọn |

### CÒN THIẾU — cần user quyết
- [ ] **Hành động "Lịch sử"** (skill list-page mục 1, chốt 2026-08-15: *mọi màn danh sách BẮT BUỘC
      có*). Hiện **cả 2 chứng từ đều chưa có** — ERP cũng không có. Làm thì cần: bảng log mới +
      ghi log ở Service + popup ở danh sách + khối "Lịch sử" ở màn chi tiết (skill `entity-history`).
- [ ] **Nút "Thêm nhanh" nguyên nhân** ngay trong form (ERP có popup tạo lỗi thiết bị kèm định mức
      công, giá, chi phí, vật tư). HRM đã có màn danh mục "Công việc, lỗi thiết bị" riêng.

## Phase 4 — Lịch sử + Thêm nhanh nguyên nhân (user chốt 2026-08-20)

### A. Lịch sử thay đổi — làm cho CẢ 2 chứng từ
Dùng **bộ dùng chung `catalog_histories`** (skill entity-history §5.1) — không tạo bảng
`<entity>_history` riêng, không viết popup riêng: các trường theo dõi đều là cột phẳng trên bảng
chính nên đúng phạm vi bộ dùng chung, và 2 màn ăn theo đúng UI base của màn Khách hàng.

- [x] Khai 2 bảng + nhãn cột tiếng Việt vào `CatalogHistoryService::TABLES`
- [x] `use LogsCatalogHistory` trong 2 service, khai `catalogTable()` / `catalogColumns()` /
      `catalogDisplay()` — snapshot lưu **giá trị hiển thị** (tên phòng tiếp nhận, tên trạng thái)
- [x] Ghi log ở đủ nhánh: **Tạo mới · Thay đổi thông tin · Từ chối / Không duyệt (kèm LÝ DO) ·
      Chuyển phòng tiếp nhận · Xóa**
- [x] Bổ sung nhãn + màu cho action `rejected` vào `CatalogHistoryService` (thiếu thì timeline in ra
      nguyên chuỗi kỹ thuật `rejected`)
- [x] FE — **đủ 2 nơi**: mục "Lịch sử" trong menu ⋮ của mỗi dòng (popup `CatalogHistoryModal`) +
      khối "Lịch sử" trong THÂN màn chi tiết (`SystemInfoSection`, không phải nút ở footer)

⚠️ **Dòng thiết bị của phiếu KHÔNG track**: mỗi lần lưu là xoá hết ghi lại nên log sẽ nhiễu kiểu
"xoá 3 thêm 3" dù người dùng chỉ sửa 1 ô. Muốn theo dõi thì phải đổi cách lưu bảng con trước
(upsert theo id) — ghi lại đây để lần sau không tưởng là bỏ sót.

**Kiểm chứng thật:** Không duyệt phiếu TPE.PXL.2026004699 → 1 dòng log `rejected`, `changes` chỉ có
"Trạng thái: Chờ CCTT → Đang tạo", `note` = đúng lý do đã nhập; DTO trả đủ `action_group=status`,
`actor_*`, `department_name`, `created_at_raw`; bộ lọc trả **3 nhóm cố định** + **783 người thực
hiện**. Lập phiếu mới → sinh log `create` cho cả chứng từ 1 và 2. Trên trình duyệt: khối Lịch sử ở
màn chi tiết hiện "20/08/2026 14:53 · Từ chối · Người thực hiện: CTV_NV - DNS Admin — PHÒNG CỘNG
TÁC VIÊN_NV · Trạng thái: Chờ CCTT → Đang tạo · <lý do>"; popup ở màn danh sách mở đúng phiếu.

### B. "Thêm nhanh" nguyên nhân (ERP có nút này)
- [x] BE `POST /customer-care/warranty-repair-handle-requests/device-errors` — tạo công việc / lỗi
      thiết bị và **gắn luôn vào hàng hóa của dòng** (`device_error_products`); thiếu bước gắn thì
      lỗi mới KHÔNG xuất hiện trong ô Nguyên nhân của dòng đó. Gắn quyền
      `checkPermission:Quản lý danh mục công việc - lỗi thiết bị`.
- [x] FE `QuickDeviceErrorModal.vue` — port các trường chính của popup ERP (Loại · Tên · Định mức
      công · ĐM đàm phán giá · VAT · Đơn giá bán · Hệ số công nghệ · Ghi chú). 2 bảng con của ERP
      (Thiết bị áp dụng, Dịch vụ sửa chữa) để ở màn danh mục — có ghi chú hướng dẫn ngay trong popup.
- [x] Lưu xong: tự thêm vào danh mục của đúng dòng + tự tích chọn (như ERP).

**Kiểm chứng thật:** tạo lỗi "Loi test them nhanh" → `device_errors` id 2808 (status 1, created_by
13) + `device_error_products` gắn đúng hàng hóa 8739; ô Nguyên nhân của dòng tăng 64 → 65 lựa chọn
và tự tích lỗi mới. Thiếu Loại/Tên → 2 lỗi inline trong popup.

### Lỗi tự phát hiện
- [x] **Popup không đóng sau khi lưu**: gọi `this.$refs.modal.hide()` trong khi `V2BaseModal` chỉ
      expose `close()` — sai tên hàm nên popup đứng im mà **không có lỗi nào báo ra**. Đã sửa + ghi
      chú cảnh báo tại chỗ.

## Phase 5 — Test kỹ toàn màn, đối chiếu ERP (2026-08-20)

Chạy **43 kịch bản** qua HTTP thật trên :8003 + trình duyệt :3002, mỗi con số đều đối chiếu SQL
theo đúng công thức ERP. **Không phát hiện lỗi ứng dụng mới.**

### A. Phạm vi dữ liệu — khớp SQL công thức ERP từng con số
| type | API | SQL theo công thức ERP |
| --- | --- | --- |
| `all` | 5.256 | 5.256 |
| `index` (của tôi) | 3 | 3 |
| `waiting_information` (Chờ CCTT) | 22 | 22 |
| type lạ | 3 (fail-closed về phiếu của mình) | — |

### B. Bộ lọc — 17 kịch bản đều đúng
tìm nhanh (số phiếu xử lý · số phiếu yêu cầu · tên KH · người xử lý) · trạng thái · số phiếu yêu cầu
· khách hàng · tên thiết bị · model · khoảng ngày · công ty · phòng ban · sort cột hợp lệ · sort cột
KHÔNG cho phép (bị bỏ qua, không đổi kết quả — đúng thiết kế whitelist).

### C. Chặn lập phiếu (mirror `create()` của ERP)
thiếu phiếu yêu cầu → 400 · phiếu đã có phiếu xử lý → **403** · phiếu đang "Đang tạo" → **403** ·
phiếu "Chờ xử lý" hợp lệ → 200 kèm dữ liệu chép sẵn.

### D. Validate khi gửi đi — 7 kịch bản, tất cả 422 đúng ô
thiếu Nguyên nhân + Hành động · "Tư vấn điện thoại" thiếu nội dung xử lý · Nguyên nhân rỗng · không
có thiết bị · **trùng (thiết bị + serial + giao nhau nguyên nhân)** · **thiết bị `type = new` chưa
chọn hàng hóa tương đương** · `status` ngoài {1,2}.

### E–I. Luồng ghi
lưu nháp thiếu hết → 201 (khác ERP có chủ đích) · sửa nháp rồi gửi → "Chờ CCTT" + đóng dấu giờ gửi
+ **phiếu yêu cầu gốc → "Đã xử lý" + người/ngày xử lý** · sửa phiếu đã gửi → **423** · xoá phiếu đã
gửi → chặn · Không duyệt: thiếu lý do 422 / có lý do → "Đang tạo" / từ chối lần 2 → chặn ·
**xoá phiếu nháp → phiếu yêu cầu gốc trở lại "Chờ xử lý", xoá người/ngày xử lý, dọn sạch 2 bảng con**.

⚠️ Đối chiếu ERP: **"Không duyệt" KHÔNG trả phiếu yêu cầu gốc về "Chờ xử lý"** (vẫn giữ "Đã xử lý")
— chỉ XOÁ phiếu xử lý mới trả về. Đã kiểm đúng cả 2 nhánh.

### J. Nhánh đặc thù ERP
Bấm **"Lưu nháp"** nhưng mọi dòng đều chọn "Tư vấn điện thoại" → phiếu vẫn thành **"Đã tư vấn điện
thoại"** và phiếu yêu cầu gốc cũng vậy — đúng ERP (`checkActions()`), không phụ thuộc nút bấm.

### K. Phân quyền (test bằng tài khoản THƯỜNG, không phải Super admin)
| Trường hợp | Kết quả |
| --- | --- |
| Không có quyền xem nào | danh sách 0 phiếu · xem phiếu người khác (nháp lẫn đã gửi) → **403** · Không duyệt → 403 · Thêm nhanh → 403 |
| Cấp quyền "xem theo công ty" | danh sách **5.167** = đúng SQL `company_id = 1 AND (status<>1 OR created_by = mình)` · xem phiếu cùng công ty → 200 · **xem phiếu NHÁP của người khác vẫn 403** |
| Super admin | xem được cả phiếu nháp của người khác — **đúng ERP** (`canView()` cho Super Admin đi trước mọi điều kiện), nhưng phiếu nháp người khác vẫn KHÔNG hiện ở danh sách |

### L–M. Thêm nhanh · In · Xuất
thiếu Tên/Loại → 422 · tạo đủ → lỗi mới nằm trong danh mục của **đúng hàng hóa** · in 1 phiếu 0
placeholder sót + có "Tư vấn điện thoại" · in danh sách 0 placeholder sót · xuất 15 cột.

### N–O. Thông báo · Lịch sử
Gửi đi và gửi lại đều bắn `[PXL] Chờ duyệt`, Không duyệt bắn `[PXL] Từ chối` kèm lý do.
Popup Lịch sử ở màn danh sách chạy đúng cho **cả 2 chứng từ**
(`Tạo mới · Người thực hiện: CTV_NV - DNS Admin — PHÒNG CỘNG TÁC VIÊN_NV`).

### 2 điều TƯỞNG lỗi nhưng đúng ERP (ghi lại để lần sau khỏi "sửa nhầm")
1. Super admin xem được phiếu nháp của người khác qua link trực tiếp — ERP `canView()` cũng vậy.
2. Tài khoản có quyền xem theo công ty vẫn KHÔNG xem được phiếu nháp người khác — nhánh quyền của
   ERP chỉ chạy khi `status != Đang tạo`.

### Ghi chú môi trường test
Có cấp tạm quyền "xem theo công ty" cho role `TEST_YCSCBH` để thử phân quyền, **đã gỡ lại ngay sau
khi test** và xoá cache quyền.

## Phase 6 — Chặn xem phiếu NHÁP của người khác (user chốt 2026-08-20)

**Yêu cầu:** HRM không cho ai xem phiếu nháp của người khác, **kể cả Super admin** — khác ERP.

### Vì sao đây là chỗ đáng sửa
ERP tự mâu thuẫn: danh sách ẩn phiếu nháp của người khác, nhưng mở link chi tiết thì đọc được —
`canView()` đặt nhánh `hasRole('Super Admin')` lên trước mọi điều kiện, còn **chứng từ 1 thì ERP
KHÔNG kiểm gì cả** (`show()` render thẳng, ai có link cũng đọc được). HRM chốt theo phía chặt.

- [x] **Chứng từ 2**: đảo thứ tự trong `canView()` — kiểm "phiếu nháp của người khác" TRƯỚC nhánh
      Super admin. Các nhánh quyền còn lại giữ nguyên như ERP.
- [x] **Chứng từ 1**: **viết mới `canView()`** (ERP không có) theo đúng phạm vi `searchByFilter`:
      người tạo · 3 cấp quyền xem · người của phòng tiếp nhận; phiếu nháp người khác chặn trước tiên.
- [x] Gate ở `show()` của cả 2 màn — chốt chặn THẬT ở BE, không dựa vào việc FE ẩn link.
- [x] **Gate luôn đường IN** (`print-data`) của cả 2 màn: không chặn thì người không được xem vẫn
      đọc trọn nội dung phiếu qua bản in.
- [x] FE: gặp 403 thì báo "Bạn không có quyền xem phiếu này" rồi **đưa về màn danh sách** — trước đó
      đứng lại ở màn trống trơn, user không hiểu chuyện gì.

### Kiểm chứng
| Trường hợp | Trước | Sau |
| --- | --- | --- |
| ct1 · phiếu nháp người khác · Super admin | 200 | **403** |
| ct1 · phiếu nháp người khác · tài khoản thường | 200 | **403** |
| ct1 · IN phiếu nháp người khác | 200 | **403** |
| ct2 · phiếu nháp người khác · Super admin | 200 | **403** |
| ct2 · IN phiếu nháp người khác | 200 | **403** |
| phiếu nháp CỦA MÌNH | 200 | 200 |
| phiếu đã gửi, đủ quyền | 200 | 200 |
| Trên trình duyệt | màn trống | báo lỗi + về danh sách |

### Dọn lệch dữ liệu phân quyền (phát hiện khi test)
DB local giữ 4 quyền của chứng từ 1 ở **id 1177–1180** trong khi `PermissionsTableSeeder` khai
**1507–1510** → chạy seeder ở môi trường khác sẽ đẻ ra 4 quyền TRÙNG TÊN, màn phân quyền hiện 2 dòng
giống hệt nhau. Đã đồng bộ DB local về đúng id của seeder (tạo 1507–1510, chuyển toàn bộ liên kết
role/nhân viên, xoá bộ cũ) và đổi `type` 23 → **24 (CSKH)** cho khớp phân hệ mới.

## Phase 7 — Tài liệu bàn giao (2026-08-21)

- [x] **`testcase.xlsx` (HRM)** — **87 test case**, P0 chiếm 61%, 12 nhóm: Phân quyền & truy cập
      (12 TC) + 11 nhóm La Mã, có riêng nhóm **LỊCH SỬ THAY ĐỔI**. Bộ kiểm tra thuật ngữ in "sạch",
      không trùng mã TC, không freeze panes.
- [x] **`testcase.xlsx` (ERP)** — **57 test case** ở `erp/.plans/warranty-repair-handle-request-erp/`,
      bám hành vi thật của cổng ERP: 2 lối vào menu · nút "Lưu" cũng bắt nhập đủ · "Không duyệt"
      chỉ có ở màn xem chi tiết · từ chối KHÔNG gửi thông báo · quản trị đọc được phiếu nháp của
      người khác (ghi nhận hiện trạng để đối chiếu).
- [x] **`Mô tả nghiệp vụ - Phiếu xử lý yêu cầu.docx`** — 11 chương, 9 bảng, 9 trang: dùng để làm gì
      · ai tham gia · 6 trạng thái và ai làm phiếu chuyển trạng thái · luồng 4 bước · **bảng thông
      báo (ai nhận · nội dung · bấm vào đi đâu · sự kiện KHÔNG gửi thông báo)** · phân quyền · quy
      tắc bắt buộc · tra cứu/in/xuất · liên thông ERP kèm **4 điểm cố ý làm khác** · giới hạn hiện tại.

### Sửa tài sản chung khi làm tài liệu
- [x] `tc_engine.py` chỉ khai số La Mã tới **X** → màn có 11 nhóm bị lỗi khi dựng file. Mở rộng
      danh sách tới **XV** kèm ghi chú (thuần thêm, không đổi hành vi màn nào).

### Checkpoint — 2026-08-21 (đổi chữ nút gửi phiếu)
Đổi nút gửi phiếu từ **"Lưu và gửi duyệt"** sang **"Lưu và gửi"** (user chốt 2026-08-21): phiếu
được GỬI sang bước cung cấp thông tin làm báo giá, không có ai duyệt nó. `V2Footer` có sẵn
`send_and_submit_form` kèm đúng câu xác nhận ("Xác nhận lưu và gửi / Bạn đồng ý lưu và gửi?") —
KHÔNG phải sửa component dùng chung.
Đã sinh lại `testcase.xlsx` (87 TC, 12 ô nhắc tên nút) và `Mô tả nghiệp vụ - Phiếu xử lý yêu cầu.docx`
(5 chỗ) theo chữ mới. Bản testcase ERP giữ nguyên vì ERP không đổi.
Đã kiểm trên giao diện: nút và popup ra đúng chữ; bấm Hủy nên không đổi trạng thái phiếu thật.
Blocked:
- [x] Sửa focus ô tìm của select CHỌN NHIỀU (cột Nguyên nhân): trước đây focus rơi vào ô inline trong khung tag thay vì ô tìm trong dropdown — sửa ở `utils/select2-focus-search.js` (ưu tiên ô trong dropdown), quy ước ghi ở skill `select-and-input-state`
