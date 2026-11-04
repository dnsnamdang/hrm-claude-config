# YCHG — Tùy chọn duyệt dòng "Duyệt không cần tính giá" (PTKD)

**Ngày:** 2026-11-03
**Màn:** Bán hàng › Yêu cầu › Hàng hóa › YC hỏi giá → Chi tiết phiếu YCHG ở trạng thái "Chờ PTKD duyệt" (bước PTKD duyệt).
**Repo:** hrm-api (`Modules/MasterData`), hrm-client (`components/sale/price-asking` + `components/product/form`).

---

## 1. Mục đích & lý do (intent / why)

Hiện tại khi PTKD duyệt phiếu YCHG, mọi dòng hàng được "Đồng ý" đều bị đẩy qua đủ luồng: XNK lập YCTG → Kế toán lập Phiếu tính giá → áp giá → hàng mới lên "Đang kinh doanh". Có hai nhóm hàng **đã biết trước giá**, đi qua luồng này là thừa và làm chậm việc lập hợp đồng / đồng bộ ERP:

- **TH1 — Vật tư/phụ kiện giá 0:** hàng vốn không có giá trị tiền (giá nhập = 0, giá bán = 0), không cần hỏi giá.
- **TH2 — Hàng tạm kế thừa báo giá trúng thầu:** giá nhập + giá bán đã chốt sẵn trên báo giá đã trúng thầu, chỉ cần ghi nhận.

Tính năng bổ sung **tùy chọn duyệt thứ 3** cho từng dòng hàng: **"Duyệt không cần tính giá"**. Dòng chọn tùy chọn này sẽ bỏ qua YCTG (XNK) và Phiếu tính giá (Kế toán), tự ghi giá vào danh mục chuẩn và chuyển thẳng hàng sang **"Đang kinh doanh"** ngay khi PTKD bấm **Duyệt cả phiếu**.

**Thành công trông thế nào:** PTKD mở phiếu "Chờ PTKD duyệt", với mỗi dòng (cả hàng tạm Cha lẫn từng Con) chọn 1 trong 3 trạng thái; nút Duyệt phiếu chỉ sáng khi 100% dòng đã có trạng thái; sau khi bấm Duyệt phiếu, hàng option-3 lập tức sẵn sàng kinh doanh với giá đúng, các dòng thường vẫn đi luồng cũ.

---

## 2. Bối cảnh kỹ thuật đã khảo sát (để builder khỏi dò lại)

Toàn bộ luồng YCHG nằm ở `Modules/MasterData` (không phải `Modules/Assign`). Mọi path tính từ `/Users/nguyentrancu/DEV/code/ERP-HRM/HRM/hrm-api/Modules/`.

### 2.1 Trạng thái duyệt từng dòng = `product_company_coefficients.status`
Model `MasterData/Entities/Product/ProductCompany.php:23-36`. Cặp (hàng × công ty):
- `1` Đang nhập thông tin, `2` Chờ tính giá, `3` **Đang kinh doanh (STATUS_TRADING)**, `4` Ngừng KD, `5` Đang tính giá.
- `6` **Hàng tạm (chờ duyệt)**, `7` **Hàng tạm đã duyệt (đồng ý)**, `8` **Hàng tạm không duyệt (từ chối)**.
- `TEMP_STATUSES = [6,7,8]` (dòng 33), `PRICING_FLOW_STATUSES = [2,5]` (dòng 36).
- **Không có cột duyệt riêng** trên `price_asking_request_products`; trạng thái duyệt dòng chính là cột `status` này. Lý do từ chối lưu ở `price_asking_request_approve_histories` (`type='temp_reject'`, note = "`<mã hàng>: <lý do>`"), đọc lại qua `PriceAskingRequestService::tempRejectReasons` → trường `temp_reject_reason` ở `lineRow`.

### 2.2 Trạng thái phiếu `price_asking_requests.status`
Model `MasterData/Entities/PriceCalculation/PriceAskingRequest.php:19-29`: `3` Đang tạo, `2` Chờ PTKD duyệt, `8` PTKD không duyệt, `10` Đang hỏi giá, `4` **Đã tính giá**, `9` Không có giá, `11` Đã chuyển cty. Luồng chuẩn `3→2→10→(4|9)`.

### 2.3 Cha–Con
Con ghép bộ ở `recipe_products` (`base_product_id` = cha, `product_id` = con, `is_main`). Dòng phiếu chỉ lưu hàng Cha; Con có `status` 6/7/8 riêng, PTKD duyệt độc lập. `lineRow` trả `recipe_children[]` kèm `can_temp_approve` riêng (`PriceAskingRequestService.php:494`).

### 2.4 PTKD duyệt phiếu — `PriceAskingRequestWriter::ptkdApprove` (591-665)
Trong transaction: khoá phiếu (`lockForPtkd`, phiếu phải ở `2`) → nếu còn dòng ở `6` thì chặn ("Còn N hàng tạm chưa duyệt", 613-616) → nhóm toàn bộ dòng `8` thì đóng `STATUS_CANCELLED` (6) → nhóm còn lại: resolve XNK (thiếu XNK báo lỗi), nhóm → `STATUS_WAITING_XNK`(5), phiếu → `STATUS_ASKING`(10) + `approver_id/approved_time/comment` → `moveProducts` chuyển hàng `7→2` (813, dòng 650) → có nhóm đóng thì `refreshHead` (654). **YCTG và Phiếu tính giá KHÔNG tự sinh ở đây** — là bước thủ công kế tiếp của XNK (`xnkApprove`→lập YCTG) rồi Kế toán (lập Phiếu tính giá). Không tồn tại bước "áp giá chung của phiếu".

Duyệt/từ chối dòng: `tempApprove`(529) set 7, `tempReject`(556) set 8 (lý do ≤255, `TEMP_REASON_MAX`), `setTempStatus`(579) cập nhật `product_company_coefficients.status` + ghi lịch sử. Gate chung `assertTempGate`(498): quyền PTKD + dòng thuộc phiếu + phiếu ở `2` + dòng ở 6/7/8.

### 2.5 Lên "Đang kinh doanh"
`PriceCalculateFinalizer::promoteProducts` (`PriceCalculateFinalizer.php:256-275`): khi mọi ĐVT của hàng trong Phiếu tính giá xong, cập nhật hàng đang ở `2/5` → `3` (269) + `trackStatus` ("Duyệt phiếu tính giá <mã>") + `ProductPriceSetWriter::ensureProductSet`. `ProductHistoryService::trackStatus` bọc mọi lần đổi trạng thái để ghi lịch sử — tái sử dụng được.

### 2.6 Ghi giá danh mục chuẩn — `MasterData/Services/ProductPrice/ProductPriceWriter.php`
`apply($productId,$productUnitId,$companyId,array $resolved,float $cost,?string $reason,int $by)` (31), gọi trong transaction của caller:
1. `ProductPriceSetWriter::ensureUnitSet` sinh 6 dòng giá rỗng + `product_company_units`.
2. `writePrices`(133) ghi 6 loại giá vào **`product_unit_prices`** (`price_type_id` 1-6) + giá hiệu lực.
3. `writeCompanyUnit`(208) ghi **giá nhập** vào **`product_company_units.cost_price`** (+ `reason_edit_price`).
4. `dropPendingApprovals`, `InheritedPriceSync::propagate`.

`resolvePrices($prices,$companyId)` (66): cần đủ 6 loại, loại `1` (Bán lẻ) bắt buộc; **loại `6` (TMĐT) BE tự tính = Bán lẻ × `configs.coefficient_ecommerce_price` (mặc định 1.3)**.
⚠️ **Giá nhập KHÔNG nằm ở `product_unit_prices`** — nằm ở `product_company_units.cost_price`.

### 2.7 Hàng tạm ↔ Báo giá trúng thầu
Không có bảng `product_projects`. Nối qua `quotation_product_prices.erp_product_id = products.id`, join `quotations.status = Quotation::STATUS_TRUNG_THAU (=7)` (`Assign/Entities/Quotation.php:19`). Trên dòng báo giá: `estimated_price` = **giá nhập**, `quoted_price` = **giá bán**, `decimal(15,2)`, **theo tiền tệ báo giá** (`quotations.currency_id`, `exchange_rate`). Một hàng có thể gắn nhiều dòng báo giá. Tỷ giá hiện tại: `QuotationService::resolveCurrentExchangeRate` (`Assign/Services/QuotationService.php:1428`) trả `1.0` nếu VND/không có currency, ngược lại lấy `currencies.exchange_rate` hiện tại (KHÔNG dùng `quotations.exchange_rate` đóng băng). Reuse-price gate hiện có: `ProductProjectController::canSeeReusePrice`(737).

### 2.8 Front-end
- Phiếu: `components/sale/price-asking/PriceAskingRequestForm.vue` (dùng cho add/edit/show). Mỗi dòng ở bước duyệt **không có radio inline** — chỉ 1 nút điều hướng `openTempApprove(row)` → `router.push('/sale/price-asking-requests/{id}/temp/{product_id}')`. Nhãn nút: "Duyệt" khi `company_status===6`, "Sửa" khi 7/8. Con render thành `<tr class="recipe-child-row">` ngay dưới Cha, có nút duyệt riêng.
- Trang quyết định từng SP: `pages/sale/price-asking-requests/_id/temp/_productId.vue` → `components/product/form/ProductForm.vue` mode `temp-approve`. Footer (72-105): **Lưu / Đồng ý / Không duyệt / Hủy**, hiện theo cờ BE `tempMeta.can_save|can_approve|can_reject`. Không giữ lựa chọn ở FE — BE persist ngay, trả lại `company_status` + `temp_reject_reason`.
- Nút **Duyệt phiếu**: `<V2BaseButton :interactable="!tempPendingCount">`; `tempPendingCount = Number(detail.temp_pending_count)` (BE đếm, chỉ đếm dòng ở `6`).
- API: base `master-data/price-asking-requests`. Duyệt dòng: `POST {API}/{id}/temp-products/{pid}/approve`; từ chối: `.../reject {reason}`. Duyệt phiếu: `POST {API}/{id}/approve {comment}`.

---

## 3. Quyết định thiết kế (đã chốt với người đặt hàng)

### 3.1 UX — ba lựa chọn, một nút mới
- Giữ nguyên mô hình hiện tại: mỗi dòng (Cha + từng Con) điều hướng sang trang quyết định từng sản phẩm. **Thêm nút footer thứ 3 "Duyệt không cần tính giá"** trên `ProductForm.vue` mode `temp-approve`, cạnh **Đồng ý** / **Không duyệt**.
- **Một nút chung** — hệ thống tự phân loại TH1 hay TH2 (không hiện 2 mục riêng cho PTKD).
- Nút **luôn bấm được** (không khóa theo điều kiện trên trang quyết định). Việc kiểm tra dòng có thực sự đủ điều kiện dồn về lúc **Duyệt cả phiếu**.
- **Đổi ý:** dòng đang ở trạng thái `9` vẫn bấm "Sửa" để đổi lại sang 7/8/9 bất kỳ lúc nào trước khi Duyệt phiếu (gate `assertTempGate`/`setTempStatus` phải nhận `9` là trạng thái hiện tại hợp lệ).

### 3.1b Bộ Cha–Con — cho phép lệch luồng *(đã chốt)*
Mỗi dòng (Cha hoặc từng Con) được định tuyến **theo trạng thái của chính nó**, không ràng buộc nhau. Cha chọn `9` → promote Cha ngay; Con chọn Đồng ý (1/7) → Con vẫn đi XNK/tính giá như thường; và ngược lại. Một bộ có thể nửa "Đang kinh doanh" nửa "đang tính giá". Nút Duyệt phiếu chỉ cần 100% dòng (Cha + mọi Con) đã rời khỏi trạng thái `6`.

### 3.2 Đánh dấu trạng thái dòng *(QUYẾT ĐỊNH CỦA NGƯỜI THIẾT KẾ — xác nhận khi review)*
Thêm **một giá trị trạng thái mới** vào `product_company_coefficients.status`: **`9` = Hàng tạm duyệt không cần tính giá** (hằng đề xuất `STATUS_TEMP_APPROVED_NO_PRICE`). Lý do: cột `status` đang là nơi mang trạng thái duyệt dòng (6/7/8); thêm giá trị song song sạch hơn thêm cột cờ. Dòng `9`:
- Được tính là **"đã quyết"** → không kẹt nút Duyệt phiếu (`temp_pending_count` chỉ đếm `6`, nên `9` tự động bị loại — không cần sửa đếm).
- Lúc Duyệt phiếu được định tuyến **promote thẳng → 3** thay vì `7→2`.

### 3.3 Điều kiện hợp lệ (kiểm tại bước Duyệt phiếu)
Với mỗi dòng (Cha/Con) mang trạng thái `9`, tại `ptkdApprove` xác định loại và validate:
- **TH2 (ưu tiên trước):** tồn tại `quotation_product_prices` với `erp_product_id = product_id`, join `quotations.status = 7`, và dòng đó có **cả** `estimated_price` **và** `quoted_price` (NOT NULL). Nhiều dòng → lấy **báo giá trúng thầu mới nhất** (`quotations.id` lớn nhất). → dùng giá của dòng đó.
- **TH1:** không thuộc TH2, và dòng có **giá nhập = 0 VÀ giá bán = 0 nhập tường minh** *(QUYẾT ĐỊNH CỦA NGƯỜI THIẾT KẾ: thuần theo giá trị; không ràng buộc phải là nhóm vật tư/phụ kiện)*. → ghi giá 0. **Giá còn trống/null (hàng tạm chưa từng nhập giá) KHÔNG đủ điều kiện** — phải là giá trị 0 có thật, để tránh hàng tạm mới lọt thẳng vào kinh doanh.
- **Không thuộc TH1 lẫn TH2** → **chặn Duyệt phiếu**, báo lỗi liệt kê các dòng vi phạm (gợi ý khóa lỗi `temp_products`, thông điệp nêu mã hàng + lý do: "chưa đủ điều kiện duyệt không cần tính giá").
- **Không thêm gate người/công ty cho TH2** *(đã chốt)*: chỉ cần hàng tạm gắn báo giá trúng thầu (status 7) có đủ 2 giá là được áp — PTKD duyệt phiếu đã là đủ thẩm quyền. Gate hiển thị M1 (own + quyền giá vốn) **chỉ áp cho việc XEM giá ở picker**, không áp cho hành vi ghi giá khi duyệt.

### 3.4 Ghi giá & promote (ngay trong transaction `ptkdApprove`)
Với mỗi dòng `9` hợp lệ, trước khi/khi chuyển trạng thái:
- **TH2:** đọc giá từ dòng báo giá trúng thầu mới nhất. Quy đổi VND: nếu tiền tệ báo giá ≠ VND thì **nhân tỷ giá hiện tại** (`resolveCurrentExchangeRate`). `cost = estimated_price × rate` → `product_company_units.cost_price`. Giá bán = `quoted_price × rate`, **đồng giá — gán cho cả 6 loại giá bán** (ghi đè cả TMĐT loại 6 = đúng `quoted_price × rate`, KHÔNG dùng hệ số 1.3). Ghi qua `ProductPriceWriter::apply` cho từng ĐVT của hàng.
- **TH1:** `cost = 0`, cả 6 loại giá bán = `0`.
- **Đơn vị tính** *(QUYẾT ĐỊNH CỦA NGƯỜI THIẾT KẾ)*: giá (sau quy đổi VND) áp cho **ĐVT của dòng báo giá** (TH2) hoặc ĐVT gốc (TH1); các ĐVT khác của hàng **quy đổi theo hệ số** như luồng chuẩn khi `ensureProductSet` dựng bộ giá, không áp phẳng cùng một con số cho mọi ĐVT. Builder pin cơ chế quy đổi đúng theo bộ giá chuẩn.
- Sau khi ghi giá: set `product_company_coefficients.status 9 → 3` (Đang kinh doanh) + `trackStatus` ghi chú "Duyệt không cần tính giá — YCHG <mã phiếu>" + `ensureProductSet`.
- Ghi lịch sử phiếu: thêm loại log mới (gợi ý `type='temp_approve_no_price'`) ở `price_asking_request_approve_histories`.

### 3.5 Trạng thái phiếu sau Duyệt phiếu
- Hàng `9` promote **ngay** lúc bấm Duyệt phiếu.
- Sau khi xử lý dòng `8` (từ chối) + dòng `9` (option-3), **nếu không còn nhóm nào cần giao XNK** (mọi dòng trong phiếu đều `8` hoặc đã promote `3`) → **đóng phiếu = `STATUS_PRICED` (4)**. Nhóm toàn dòng option-3 cũng đóng tương ứng (gợi ý nhóm → `STATUS_PRICED` 4 vì đã có giá; builder chốt và reuse `refreshHead` nếu khớp).
- Nếu vẫn còn dòng thường (option-1) → phiếu sang **`STATUS_ASKING` (10)** như hiện tại; dòng option-3 trong phiếu vẫn promote ngay.

### 3.6 Quyền
**Dùng chung** quyền "PTKD duyệt yêu cầu hỏi giá" + middleware `dueConfig:Duyệt hàng tạm` sẵn có. **Không thêm quyền mới**, không seed gì.

### 3.7 Front-end cụ thể
- `ProductForm.vue` (temp-approve): nút footer "Duyệt không cần tính giá" (luôn hiện khi dòng còn ở bước duyệt/`can_approve`-tương đương), gọi endpoint mới `POST {API}/{id}/temp-products/{pid}/approve-no-price` → BE set `9`. Có confirm nhẹ như "Đồng ý".
- `PriceAskingRequestForm.vue`: nhận diện `company_status===9` — nhãn nút "Sửa" (giống 7/8) + badge/nhãn dòng "Duyệt — không tính giá" (phân biệt với Đồng ý/Từ chối). Không cần sửa `tempPendingCount` (BE chỉ đếm `6`).
- Con hiển thị y hệt Cha cho trạng thái `9`.

---

## 4. Goals / Non-goals / Anti-goals

**Goals**
- Thêm tùy chọn duyệt dòng thứ 3 cho cả hàng Cha và từng hàng Con.
- TH1 & TH2 tự phân loại; TH2 lấy giá từ báo giá trúng thầu mới nhất, quy đổi VND theo quy tắc hiện hành.
- Hàng option-3 lên "Đang kinh doanh" + ghi giá danh mục chuẩn ngay khi Duyệt phiếu, bỏ qua YCTG + Phiếu tính giá.
- Nút Duyệt phiếu chỉ sáng khi 100% dòng (Cha + mọi Con) đã có trạng thái; chặn + báo lỗi nếu có dòng option-3 không đủ điều kiện.

**Non-goals**
- Không đổi luồng của dòng Đồng ý (option-1) / Từ chối (option-2).
- Không thêm quyền mới, không seed.
- Không làm radio inline trên phiếu (giữ mô hình trang quyết định từng SP).
- Không đụng màn XNK/Kế toán.

**Anti-goals (coi là thất bại dù chạy được)**
- Lộ giá/giá vốn cho người không đủ quyền, hoặc ghi giá sai do quên quy đổi tiền tệ.
- Dòng option-3 không đủ điều kiện mà vẫn lọt lên "Đang kinh doanh".
- Giá trị trạng thái mới `9` làm vỡ các màn/đọc khác của `product_company_coefficients.status` (list, báo cáo, cột "Trạng thái HH công ty quản lý").
- Promote một phần rồi transaction lỗi để lại dữ liệu nửa vời (phải nằm trọn trong transaction `ptkdApprove`).

---

## 5. Ràng buộc (constraints)
- hrm-api = Laravel 8 / PHP 7.4; hrm-client = Nuxt 2.14 / Vue 2 / Bootstrap-Vue.
- Dữ liệu nhạy cảm (giá vốn/giá nhập) phải gate server-side, không chỉ ẩn FE (quy tắc CLAUDE.md).
- Mọi thay đổi trạng thái/giá của một lần Duyệt phiếu phải atomic trong transaction sẵn có của `ptkdApprove`.
- Số hiển thị en-US; badge màu + text do BE quyết (nhất quán các task YCHG trước).
- Giữ 1:1 ngữ nghĩa với ERP ở những chỗ port (nếu có).

---

## 6. Phần để lại cho builder quyết (open questions — không đổi "cái gì được xây", chỉ là chi tiết hiện thực)

1. **Giá trị `9`**: xác nhận `9` chưa bị dùng cho `product_company_coefficients.status` ở nơi khác; **audit mọi reader** của cột này (list sản phẩm, báo cáo, cột "Trạng thái HH công ty quản lý", filter) để `9` không rơi vào nhánh "không xác định". Nếu `9` đụng, chọn giá trị trống kế tiếp.
2. **Đọc "giá nhập = 0 và giá bán = 0" của TH1 ở đâu**: xác định nguồn giá hiện tại của dòng (product record / tab Quản trị / `product_company_units.cost_price` + `product_unit_prices`) để test **= 0 tường minh** (null/thiếu giá = KHÔNG đủ điều kiện, xem 3.3). Builder pin điểm đọc chính xác.
3. **Ghi đè TMĐT (loại 6)**: `resolvePrices` tự tính loại 6 = Bán lẻ × hệ số. Để "đồng giá cả 6 loại = quoted_price", builder chọn đường ghi không bị auto-override loại 6 (truyền đủ 6 giá và chặn auto-compute, hoặc ghi trực tiếp `writePrices`). Giữ đúng ý "đồng giá".
4. **Trạng thái nhóm cho nhóm toàn option-3**: chốt giá trị đóng nhóm (đề xuất `STATUS_PRICED` 4) và tái sử dụng `refreshHead` nếu khớp để phiếu ra `4`.
5. **Điều kiện hiện nút footer** trên `ProductForm.vue` (dùng cờ `can_approve` sẵn có hay thêm `can_approve_no_price` từ BE) — thuần hiện thực.
6. **Thông điệp lỗi** khi chặn Duyệt phiếu do dòng option-3 không hợp lệ: gom nhiều dòng, nêu mã hàng.
7. **Audit hạ nguồn giả định "phải có Phiếu tính giá"**: kiểm tra đồng bộ ERP, lập hợp đồng, và các list/join dựa trên bản ghi `price_calculate*` xem có coi phiếu status `4` / hàng status `3` là bắt buộc kèm một Phiếu tính giá không. Nếu có, bổ sung guard hoặc chọn trạng thái kết thúc khác thay vì chỉ reuse `refreshHead`. (Ý định nghiệp vụ: hàng option-3 lên `3` để phục vụ ERP/lập HĐ — khoá quan trọng là trạng thái hàng `3`, không phải sự tồn tại của Phiếu tính giá.)
8. **Cơ chế quy đổi ĐVT** (xem 3.4): dùng đúng cách bộ giá chuẩn/`ensureProductSet` dẫn giá các ĐVT phụ từ ĐVT gốc theo hệ số.

---

## 7. Phạm vi file dự kiến (định hướng, không phải plan)

**hrm-api (`Modules/MasterData`)**
- `Entities/Product/ProductCompany.php` — hằng `STATUS_TEMP_APPROVED_NO_PRICE = 9` (+ cập nhật nhóm hằng liên quan nếu cần).
- `Services/PriceCalculation/PriceAskingRequestWriter.php` — thêm `tempApproveNoPrice()`; sửa `ptkdApprove()` (validate + ghi giá + promote + đóng phiếu); helper phân loại TH1/TH2 + lấy giá báo giá trúng thầu mới nhất + quy đổi VND.
- `Services/PriceCalculation/PriceAskingRequestService.php` — `lineRow`/`tempMeta` lộ cờ nút mới + nhận diện trạng thái `9` (text/badge).
- `Http/Controllers/V1/PriceCalculation/PriceAskingRequestController.php` + `Routes/api.php` — route `temp-products/{product}/approve-no-price`.
- Tái sử dụng `ProductPrice/ProductPriceWriter::apply`, `ProductHistoryService::trackStatus`, `ProductPriceSetWriter::ensureProductSet`, `QuotationService::resolveCurrentExchangeRate`.

**hrm-client (`components/`)**
- `product/form/ProductForm.vue` — nút footer "Duyệt không cần tính giá" + gọi endpoint mới.
- `sale/price-asking/PriceAskingRequestForm.vue` — nhận diện/nhãn/badge trạng thái `9` cho Cha & Con.

---

## 8. Kiểm thử (định hướng cho plan)
- BE: TH1 (giá 0) promote + ghi 0; TH2 VND; TH2 ngoại tệ (quy đổi × rate, đồng giá 6 loại); nhiều báo giá → lấy mới nhất; dòng `9` không đủ điều kiện → chặn Duyệt phiếu; Cha/Con độc lập; phiếu toàn option-3 → đóng `4`; phiếu lẫn option-1 → `10`; không lộ giá cho người không đủ quyền.
- FE/Playwright (`http://127.0.0.1:3000`): 3 nút trên trang quyết định; nút Duyệt phiếu sáng khi 100% dòng có trạng thái; nhãn trạng thái `9`.
