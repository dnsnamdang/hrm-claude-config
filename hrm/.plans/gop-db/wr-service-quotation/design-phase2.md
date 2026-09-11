# Chứng từ 4 — BÁO GIÁ DỊCH VỤ (`wr_service_quotations · type = 1`)

> @namdangit · nhánh `gop_db` · **khảo sát 2026-08-24, CHƯA CODE**
> Đọc kèm `design.md` (khảo sát cả cụm) — file này chỉ nói phần RIÊNG của chứng từ 4.
> Nguồn: đọc thẳng ERP `TanPhatDev/` + đếm dữ liệu thật trên DB gộp `local_hrm_erp`.

---

## 1. Màn ERP tương ứng

| | |
| --- | --- |
| Đường dẫn | `/admin/customer-care/warranty_repair_service_quotations` |
| Controller | `WarrantyRepairServiceQuotationsController` — **883 dòng**, 13 method |
| View | `resources/views/customercare/service_quotations/` — form **1.399 dòng** + formJS 466 |
| Model | `WrServiceQuotation` (**dùng chung với chứng từ 3**) |
| Lối vào menu | **ĐÚNG 1**: Bán hàng → Báo giá dịch vụ SC-BD-BT → **"Danh sách báo giá"** (`?permission=all`) |

⚠️ **Không có mục menu nào trỏ tới `?type=warranty`** ("Danh sách báo giá chờ tạo phiếu bảo hành").
Code màn đó vẫn còn nhưng không có đường vào — xem mục 7.

---

## 2. Số liệu thật trên DB gộp (2026-08-24)

| Chỉ tiêu | Số thật | Ý nghĩa khi port |
| --- | --- | --- |
| Bản ghi `type = 1` | **5.170** | (chứng từ 3 là 4.980) |
| **Lập ĐỘC LẬP** (`parent_id` rỗng) | **3.966 — 77%** | ⚠️ Đường dùng CHÍNH không phải từ phiếu CCTT |
| Lập từ phiếu CCTT | 1.204 — 23% | |
| Có dòng khối "Loại hàng hoá" | 812 phiếu / 1.535 dòng | khối C thật sự có dùng |
| **`has_warranty = 1`** | **1 / 5.170** | ⚠️ nhánh bảo hành ở báo giá gần như CHẾT |
| Trạng thái | Đang tạo 952 · Duyệt 121 · Đã tạo hợp đồng 2.503 · **Hết hiệu lực 1.594** | |

Kết luận rút ra: **màn này không phải "bước tiếp theo của CCTT" mà là một màn lập báo giá đứng riêng**,
CCTT chỉ là một trong hai nguồn dữ liệu đầu vào. Thiết kế HRM phải lấy nhánh lập độc lập làm mặc định.

---

## 3. Khác gì chứng từ 3 (bảng đối chiếu)

| Hạng mục | Chứng từ 3 — CCTT | **Chứng từ 4 — Báo giá** |
| --- | --- | --- |
| Cách lập | CHỈ từ Phiếu xử lý yêu cầu | **3 đường**: từ phiếu CCTT · **lập mới độc lập** (nút Tạo mới trên danh sách) · **Sao chép** từ báo giá khác |
| Khách hàng | khoá, lấy theo phiếu xử lý | **tự chọn** (popup tìm khách) + tự chọn Người liên hệ, Địa chỉ sửa chữa |
| Dòng thiết bị sửa chữa | bê từ phiếu xử lý | tự thêm từ **danh mục thiết bị của khách**, có cả **tạo lỗi thiết bị mới ngay trong form** (`CreateDeviceErrorModal`) và **chọn thiết bị tương đương** |
| Khối riêng | — | **C - LOẠI HÀNG HOÁ** (bảng `wr_service_quotation_merchandises`) |
| VAT | không có | **có**: `vat_percent` + `vat_cost` + `total_before_vat` + `total_after_vat` lưu trên phiếu; khối hàng hoá có VAT theo từng dòng |
| Hiệu lực báo giá | — | ô **"Hiệu lực báo giá"** = `date_of_entering`, đơn vị **SỐ NGÀY** kể từ ngày lập |
| Tệp đính kèm | — | **có** (pdf/ảnh/doc/xls, ≤ 13MB/tệp, đẩy S3), có nút **Cập nhật File** ở màn xem |
| 2 nút lưu | Lưu (Đang tạo) · Lưu & Gửi duyệt (Chờ làm báo giá) | Lưu (Đang tạo) · **Lưu & Duyệt** (Duyệt — **tự duyệt, không có người duyệt riêng**) |
| Thao tác riêng | Không duyệt (từ chối tiếp nhận) | **Sao chép** · **Lập hợp đồng dịch vụ SC - BH** |
| In | 1 mẫu | **3 mẫu** (Báo giá mẫu 1 / mẫu 2 / mẫu 3) + tuỳ chọn **In kèm checklist bảo dưỡng** — chọn trong popup |
| Bảng con | 11 | **12** (thêm `wr_service_quotation_merchandises`) |
| Chặn ngoài | — | **middleware `checkDueConfigs`** — xem mục 6 |

**Điểm rất có lợi:** giao diện ERP của 2 màn **dùng CHUNG class JS `WRInformation`** (màn báo giá
`@include` thẳng file của màn CCTT). Nghĩa là module tính tiền HRM `utils/wrServiceQuotationMoney.js`
dùng lại được nguyên, chỉ bổ sung phần **hàng hoá + VAT**.

---

## 4. Trạng thái & luồng đẩy ngược

Bộ trạng thái riêng (`STATUSES_QUOTATIONS`), **KHÔNG dùng chung với chứng từ 3**:

| Mã | Tên | Sinh ra khi |
| --- | --- | --- |
| 1 | Đang tạo | bấm **Lưu** |
| 2 | Duyệt | bấm **Lưu & Duyệt** (tự đóng dấu người duyệt = chính mình, thời điểm = lúc bấm) |
| 3 | Đã tạo hợp đồng | Hợp đồng dịch vụ / phụ lục lập từ báo giá này (chứng từ 5 set) |
| 4 | Hết hiệu lực | **lệnh chạy nền `update:quotations-expried`, 00:30 hằng ngày**: phiếu đang ở *Duyệt* mà `ngày lập + số ngày hiệu lực < hôm nay` |

Đẩy ngược lên chứng từ trước (chỉ khi báo giá lập TỪ phiếu CCTT):

- Lưu nháp (Đang tạo) → phiếu CCTT chuyển **Đang báo giá** (8)
- Lưu & Duyệt → phiếu CCTT chuyển **Báo giá đã duyệt** (4) · Phiếu yêu cầu gốc chuyển **Đã có báo giá**
- Xoá báo giá đang ở Đang tạo → phiếu CCTT trả về **Chờ làm báo giá** (2)

Sửa / Xoá: `canEditQuotation()` = `type = 1` **và** người lập **và** trạng thái **Đang tạo**
(Super admin được thêm ngoại lệ ở ERP — HRM đã chốt bỏ ngoại lệ này từ chứng từ 2).
Sao chép: `canCopy()` ở ERP **luôn trả true** → ai xem được là sao chép được.

---

## 5. Quyền

| Quyền | ERP | Đề xuất HRM |
| --- | --- | --- |
| Xem báo giá dịch vụ SC - BH theo tổng công ty | id 402 | thêm mới |
| Xem báo giá dịch vụ SC - BH theo công ty | id 403 | thêm mới |
| Xem báo giá dịch vụ SC - BH theo phòng ban | id 404 | thêm mới |
| **Tạo báo giá dịch vụ SC - BH** | **id 414 — BỊ COMMENT trong seeder** | ⚠️ ERP hiện **không gate** quyền tạo. HRM nên tạo quyền thật (fail-closed) — cần user chốt |

Phạm vi xem chạy đúng như chứng từ 3 (`searchByFilter` nhánh `'quotation'`), gồm cả quy tắc
**phiếu Đang tạo của người khác thì không ai thấy**.

---

## 6. Ràng buộc cắm sang phân hệ khác

1. **`checkDueConfigs`** gắn trên `create` / `store` / `update` — chặn lập & sửa báo giá khi người
   dùng đang có **hàng giữ quá hạn / hàng mượn quá hạn / hàng nhập thẳng quá hạn**, bật tắt theo
   cấu hình từng công ty (`company_due_configs` × `due_configs`, nhóm "Lập báo giá"). Super admin
   được bỏ qua. → HRM có port ràng buộc này không? **Cần chốt** (mục 9).
2. **Phân chia thị trường** — kiểm ở bước lập hợp đồng (`getForServiceContract`), báo cáo lỗi
   *"Báo giá đã chọn không thuộc phân công của phân chia thị trường của nhân viên"*. Việc của
   chứng từ 5, ghi lại để không quên.
3. **Xem tồn kho** — ô "Xem tồn" theo kho ở khối A / B / C, gọi sang Kho lấy *Tồn dự kiến* và
   *Đang giữ*. Chứng từ 3 đã port phần này, dùng lại.

---

## 7. Nhánh bảo hành — bằng chứng cho thấy đã chết

- Nút **"Lập phiếu bảo hành"** trong menu hành động **bị comment**
  (`WarrantyRepairServiceQuotationsController.php:132–134`) và đó là link duy nhất tới
  `WrWarrantys.create` trong toàn repo ERP.
- Màn danh sách `?type=warranty` **không có mục menu nào trỏ tới**.
- Dữ liệu: **1 / 5.170** bản ghi có `has_warranty = 1`.
- Ngược lại, `store()` / `update()` vẫn ghi `has_warranty = 1`, `status_warranty = 1` khi phiếu có
  dòng bảo hành → dữ liệu vẫn sinh ra, chỉ là không ai dùng tiếp.

→ **Đề xuất**: HRM vẫn **ghi đủ 2 cột** (như đã làm ở chứng từ 3), nhưng **không dựng** màn
`?type=warranty` và **không** làm nút Lập phiếu bảo hành. Cần user xác nhận với nghiệp vụ.

---

## 8. Hiện trạng HRM — dùng lại được bao nhiêu

Đã có sẵn (từ chứng từ 3):

- **11 entity con** `Modules/CustomerCare/Entities/WrServiceQuotation/` — thiếu đúng **1**: `WrServiceQuotationMerchandise`
- `WrServiceQuotationService` (1.262 dòng) · `WrServiceQuotationPrintService` · `WrServiceQuotationNotifier` · Resource
- FE: 11 file `pages/customer-care/wr-information-requests/` + **`utils/wrServiceQuotationMoney.js`**
  (đã đối chiếu số học khớp tuyệt đối 39 phiếu thật)
- 12 bảng ERP đã nằm sẵn trên DB gộp, kể cả `wr_service_quotation_merchandises` → **không cần migration**

Phải sửa ở tầng chung (design.md hứa "không hard-code `type = 0`" nhưng thực tế còn 3 chỗ):

| File | Dòng | Việc |
| --- | --- | --- |
| `WrServiceQuotationService.php` | 120 | `->where('type', TYPE_INFORMATION)` trong truy vấn danh sách |
| `WrServiceQuotationService.php` | 779, 807 | gán cứng `type = TYPE_INFORMATION` khi tạo / cập nhật |
| `WrServiceQuotation.php` | 89–97 | hằng `PERM_*` đang là quyền của CCTT |

→ Cách làm đề xuất: tách phần dùng chung thành **service cơ sở + 2 lớp con theo `type`**, hoặc
đưa `type` + bộ quyền thành thuộc tính của lớp con. Quyết trước khi viết dòng code đầu tiên.

⚠️ Nợ đang treo: nút **"Tạo báo giá dịch vụ"** ở màn CCTT hiện chỉ bắn toast — làm xong chứng từ 4
thì nối vào.

---

## 9. Cần chốt trước khi lên plan

| # | Câu hỏi | Đề xuất của mình |
| --- | --- | --- |
| 1 | Có làm **nhánh bảo hành** (màn `?type=warranty` + nút Lập phiếu bảo hành) không? | **Không** — giữ dữ liệu, bỏ màn. Bằng chứng ở mục 7 |
| 2 | Có port **`checkDueConfigs`** (chặn lập báo giá khi có hàng giữ / mượn / nhập thẳng quá hạn) không? | Làm, nhưng **phase sau**: HRM mới có màn hàng giữ, chưa có hàng mượn và hàng nhập thẳng |
| 3 | **Quyền tạo báo giá** — ERP để trống, HRM có gate không? | **Có**, thêm quyền *Tạo báo giá dịch vụ SC - BH* (fail-closed theo CLAUDE.md) |
| 4 | **Sao chép báo giá** — ERP cho mọi người sao chép mọi phiếu xem được | Giữ nguyên, nhưng gate thêm quyền tạo ở câu 3 |
| 5 | **3 mẫu in** — làm đủ cả 3 + checklist, hay chỉ mẫu đang dùng thật? | Đếm dữ liệu thật không biết được (ERP không lưu mẫu đã in) → **hỏi nghiệp vụ mẫu nào còn dùng** |
| 6 | Nút thứ hai đặt chữ gì? ERP ghi **"Lưu & Duyệt"** nhưng thực chất là tự duyệt | Theo `button-convention` + 3 chứng từ trước: **"Lưu và gửi"**? hay giữ **"Lưu và duyệt"** vì đây là hành vi duyệt thật? — cần chốt |
| 7 | **Lưu nháp** có nới lỏng validate như 3 chứng từ trước không? | Có — chỉ bắt Khách hàng, phần còn lại để trạng thái Duyệt mới bắt |

---

## 10. Khối lượng ước tính (sau khi chốt mục 9)

| Lớp | Việc |
| --- | --- |
| DB | **0 migration** (12 bảng đã có trên DB gộp) |
| BE | 1 entity mới + tách service theo `type` + service/controller/request/resource cho `type = 1` + 3–4 quyền + ~14 route + lệnh chạy nền "hết hiệu lực" |
| FE | ~12 file `pages/customer-care/wr-service-quotations/` — dựng lại từ khuôn CCTT, thêm khối Loại hàng hoá, VAT, đính kèm, chọn khách hàng, sao chép, popup chọn mẫu in |
| Tính tiền | mở rộng `utils/wrServiceQuotationMoney.js`: hàng hoá + VAT; **bắt buộc đối chiếu số học với dữ liệu ERP thật** như chứng từ 3 |

---

## 11. Quyết định đã chốt (user chốt 2026-08-24)

| # | Vấn đề | Chốt |
| --- | --- | --- |
| 1 | Nhánh bảo hành | **Làm ngay trong đợt này** (user chốt lại sau khi có dữ kiện mục 12): nối `createWrWarranty()` vào chứng từ 3 + dựng màn Phiếu bảo hành. Phạm vi thực tế rất nhẹ — xem mục 13 |
| 2 | `checkDueConfigs` | **Phase sau** — HRM mới có màn hàng giữ, chưa có hàng mượn / hàng nhập thẳng |
| 3 | Quyền tạo báo giá | **KHÔNG gate**, giữ đúng ERP: ai vào được màn (có quyền xem) là lập được. Không thêm quyền mới, route store/update/delete không gắn `checkPermission` |
| 4 | Sao chép báo giá | Giữ hành vi ERP (ai xem được thì sao chép được), thuộc Phase B |
| 5 | Mẫu in | **Làm đủ 3 mẫu + In kèm checklist**. Nguồn: mẫu 1 `ReportTemplate::BAO_GIA_DICH_VU_BH_SC`, mẫu 2 `...MAU_2`, mẫu 3 `PrintTemplate` mã `BGDV-02A`, checklist `ReportTemplate::DANH_MUC_KIEM_TRA_BAO_DUONG` |
| 6 | Chữ nút thứ hai | **"Lưu và duyệt"** — đây là hành vi duyệt thật (đóng dấu người duyệt + ngày duyệt), khác 3 chứng từ trước nên KHÔNG dùng "Lưu và gửi" |
| 7 | Validate lưu nháp | Nới như 3 chứng từ trước: nháp chỉ bắt Khách hàng, phần còn lại chỉ bắt khi bấm Lưu và duyệt |

---

## 12. ⚠️ Dữ kiện mới về nhánh bảo hành (đào thêm 2026-08-24, SAU khi chốt câu 1)

Mục 7 kết luận "nhánh bảo hành đã chết" là **SAI một nửa**. Đếm lại bảng `wr_service_contracts`:

| Chỉ tiêu | Số thật |
| --- | --- |
| Phiếu bảo hành (`type = 2`) | **3.631** — nhiều hơn cả Hợp đồng dịch vụ (2.321) |
| Sinh từ **phiếu CCTT** (`wr_information_id`) | **3.631 — 100%** |
| Sinh từ **báo giá** (`wr_service_quotation_id`) | **0** |
| Bản ghi mới nhất | 28/07/2026 — vẫn đang chạy |

Nguyên nhân: `WrServiceQuotation::createWrWarranty()` được gọi trong `store()` / `update()` của
**chứng từ 3** khi người lập bấm gửi đi mà phiếu có dòng bảo hành → phiếu bảo hành sinh TỰ ĐỘNG,
không ai bấm nút. Nút "Lập phiếu bảo hành" ở màn Báo giá bị comment vì **đã chuyển sang cơ chế tự
động ở chứng từ 3**, không phải vì nghiệp vụ bỏ nhánh này.

Hệ quả:

- "Làm đầy đủ như ERP" ở **màn Báo giá** = **không làm gì cả** (ERP đang tắt nút, 0 bản ghi đi đường này).
- Chỗ HRM đang thiếu thật so với ERP nằm ở **chứng từ 3 đã port**: hiện chỉ ghi `has_warranty` /
  `status_warranty`, **chưa gọi `createWrWarranty()`** → phiếu bảo hành không được sinh ra.
- Làm phần đó phải port bảng **`wr_service_contracts`** — bảng dùng chung cho **3 màn** (Hợp đồng
  dịch vụ · Phụ lục hợp đồng · Phiếu bảo hành), model ERP **3.327 dòng**, 3 bộ hằng trạng thái đọc
  trên cùng cột `status`. HRM **chưa đụng gì** tới bảng này.

→ Cần user chốt lại: sinh phiếu bảo hành tự động thuộc phạm vi đợt nào.

---

## 13. Phạm vi mở rộng — PHIẾU BẢO HÀNH (user chốt 2026-08-24: làm ngay đợt này)

### 13.1 Phiếu bảo hành sinh ra thế nào

`WrServiceQuotation::createWrWarranty()` chạy trong `store()` / `update()` của **chứng từ 3** khi
người lập bấm gửi đi mà phiếu có dòng ở khối A. Nó:

1. Tạo bản ghi `wr_service_contracts` với `type = 2`, mã **`<MÃ CTY>.PBH.<năm>.<số thứ tự>`**
2. Chép sang: thông tin khách hàng (kèm mã số thuế, tài khoản ngân hàng, người đại diện lấy tại
   thời điểm lập), phòng tiếp nhận = phòng của người lập, ghi chú, điều khoản, khối tiền `warranty`
3. Đặt **`status = 2` (Đã duyệt)** ngay — không qua bước duyệt nào
4. `syncProduct(product_warrantys)` + `syncCosts(costs)`
5. Bắn thông báo *"Bạn có phiếu bảo hành: <mã>"* cho **chính người lập**

Rồi quay lại đóng dấu lên phiếu CCTT: `has_warranty = 1`, `status_warranty = 2` (Đã tạo phiếu bảo hành).

### 13.2 Vì sao phạm vi nhẹ hơn tưởng — số liệu thật

| Chỉ tiêu | Số thật |
| --- | --- |
| Phiếu bảo hành (`type = 2`) | 3.631 |
| **Trạng thái Đã duyệt (2)** | **3.631 — 100%** |
| Đang tạo / Đang thực hiện / Đã hoàn thành | **0** |
| Có dòng hàng | 3.631 — 100% |

Hệ quả trực tiếp:

- `canEdit()` của phiếu bảo hành đòi trạng thái **Đang tạo** → **không phiếu nào sửa hoặc xoá được**
  → màn HRM **ẩn hẳn** Sửa và Xoá (đúng quy ước "không dùng được thì ẩn" của CLAUDE.md)
- Nút **Tạo phiếu giao việc** thuộc chứng từ 6 (chưa port) → ẩn trong đợt này
- Thao tác **Từ chối** (`reject`) đòi `canApprove()` của nhánh hợp đồng → không áp cho `type = 2`

→ **Màn Phiếu bảo hành đợt này = danh sách + xem chi tiết.** Không form, không thao tác đổi dữ liệu.

### 13.3 Bảng phải port (chỉ nhánh `type = 2`)

| Bảng | Dòng (cả 4 type) | Cần cho phiếu bảo hành |
| --- | --- | --- |
| `wr_service_contracts` | 5.195 | có — **dùng chung 4 `type`**: 1 Hợp đồng · 2 Bảo hành · 3 PL bổ sung · 4 PL giảm |
| `wr_service_contract_products` | 7.979 | có |
| `wr_service_contract_product_items` | 3.005 | có |
| `wr_service_contract_product_services` | 1.841 | có |
| `wr_service_contract_costs` | 33.548 | có |
| 3 bảng `*_device_errors` | 0 | khai entity cho đủ, chưa có dữ liệu |
| `*_extend_products` / `*_merchandises` / `*_payments` / `*_items` | 1.575 / 769 / 3.256 / 3.810 | **KHÔNG** — của Hợp đồng, đợt sau |

⚠️ `wr_service_contracts` có **3 bộ hằng trạng thái đọc trên cùng cột `status`**
(`STATUSES` hợp đồng · `STATUSES_WARRANTY` bảo hành · `STATUSES_ANNEX` phụ lục). Entity HRM phải
tách nhánh theo `type` NGAY TỪ ĐẦU, y như bài học `wr_service_quotations` ở chứng từ 3.

Trạng thái phiếu bảo hành: Đang tạo → **Đã duyệt** → Đang thực hiện → Đã hoàn thành
(3 bước sau do chứng từ 6/7 đẩy, chưa port).

### 13.4 Quyền (ERP có sẵn, HRM thêm mới)

- `Xem phiếu bảo hành theo tổng công ty` (405) · `theo công ty` (406) · `theo phòng ban` (407)
- `Tạo phiếu bảo hành` (416) — ERP dùng cho `canCreateWarranty()`; ở HRM phiếu sinh tự động nên
  quyền này **không dùng tới**, chỉ khai cho đủ nếu sau này bật lại đường tạo tay

### 13.5 Lối vào menu ERP

CSKH → Kiểm tra bảo hành sửa chữa → **Phiếu bảo hành** (`?type=all`) — đúng 1 mục.
