# Khảo sát FE + quyền — luồng Tính giá ERP (10/10/2026)

> Chỉ đọc, không sửa source. Nguồn ERP: worktree `wt-erp-2d1` (nhánh `feat/2d1-erp-khong-loi`, đã có G3 giá theo
> công ty). Đường dẫn ERP dưới đây tính từ gốc `wt-erp-2d1/`. HRM: `wt-chuyen-doi-hang-hoa/hrm-client`
> (nhánh `feat/chuyen-doi-hang-hoa`). Mockup / design: `HRM/.plans/gop-db/quan-ly-hang-hoa/man-danh-muc-hang-hoa/`.
>
> Viết tắt: **YCHG** = Yêu cầu hỏi giá (`PriceAskingRequest`) · **YCTG** = Yêu cầu tính giá
> (`PriceCalculateRequest`) · **PTG** = Phiếu tính giá (`PriceCalculate`) · **KQTG** = Kết quả tính giá
> (`PriceCalculateResult`).

---

## 0. Bức tranh chung

```
YCHG  Đang tạo(3) ─Lưu&Gửi→ Chờ PTKD duyệt(2) ─PTKD duyệt→ Chờ XNK duyệt(5) ─XNK duyệt→ "Chờ XNK hỏi giá"(1, DA_DUYET)
      │ PTKD không duyệt → Không duyệt(8)      │ XNK không duyệt → Không có giá(9)     │ XNK huỷ duyệt → Huỷ duyệt(6)
      └─ (1) ─[Lập YCTG, Lưu&Gửi]→ Chờ tính giá(7) ─[PTG Lưu&Duyệt]→ Đã tính giá(4)
YCTG  Đang tạo(3) ─Lưu&Gửi→ Chờ duyệt(2) ─[KT mua hàng bấm "Tính giá" → lưu PTG lần đầu]→ Đã duyệt(1) ─[PTG duyệt]→ Đã tính giá(4)
                                          └─ Không duyệt → quay về Đang tạo(3)
PTG   Đang tạo(3) ─Lưu&Duyệt→ Đã duyệt(1)  ⇒ ghi giá vào product_unit_prices (hoặc đẩy chờ duyệt giá) + sinh KQTG
KQTG  chỉ đọc, sinh tự động khi PTG duyệt (PriceCalculate.php:783-799)
```

- Chuyển trạng thái: `PriceAskingRequest.php:591-592` (PTKD duyệt→5), `:617-618` (→8), `:631-632` (XNK duyệt→1),
  `:648-649` (→9), `:663-664` (→4), `:674-675` (huỷ duyệt→6); `PriceCalculateRequestController.php:150-158`
  (YCTG gửi ⇒ YCHG→7); `PriceCalculateRequest.php:404-427` (approve→1 · reject→3 · calculated→4).
- ⚠️ `PriceCalculateController.php:134-160`: **lưu PTG lần đầu (kể cả chỉ "Lưu" status 3) đã gọi `$req->approve()`**
  ⇒ YCTG sang *Đã duyệt* ngay khi PTG được tạo, không đợi PTG duyệt. Quan hệ YCTG–PTG là **1–1** (sau khi YCTG
  rời *Chờ duyệt* thì `canApprove()` false, không lập PTG thứ hai được).
- Tất cả màn dùng khuôn cũ: DataTable server-side (`DATATABLE` + `search_columns`) + form AngularJS
  `ng-controller="Order"` + class JS trong `resources/views/partials/classes/order/*`.

---

## 1. Từng màn

### 1.1 Yêu cầu hỏi giá (YCHG)

**Danh sách** — `resources/views/orders/price_asking_requests/index.blade.php`
- Cột (`:43-58`): STT · Số yêu cầu (link show, `PriceAskingRequestController.php:38-40`) · Thương hiệu · Hãng sản xuất
  · Người lập · Ngày lập · Ngày nhận · Người duyệt PTKD · Ngày duyệt PTKD · Người nhận hỏi giá · Người duyệt XNK ·
  Ngày duyệt XNK · Trạng thái · Hành động.
- Bộ lọc (`:59-79`): Số yêu cầu · Tên/mã hàng · Thương hiệu · Hãng SX · Trạng thái (9 trạng thái
  `PriceAskingRequest.php:39-85`) · Người tạo · Người nhận hỏi giá · Người duyệt PTKD · Người duyệt XNK + cụm
  Công ty/Phòng/Bộ phận (`search_by_info`, `search_by_parts` theo quyền generic "Xem tất cả phiếu…" `:81-89`) +
  khoảng thời gian (`search_by_time`).
- Tham số `?type=` (`approve` · `xnk_approve` · `calculate` · mặc định) đổi phạm vi dữ liệu
  (`PriceAskingRequest.php:305-334`). Luôn chỉ thấy *Đang tạo / Không duyệt / Không có giá* của chính mình (`:336-340`).
- Menu ⚙ hành động (`PriceAskingRequestController.php:78-104`): **In** (luôn) · **Sửa** (`canEdit`) · **Xóa**
  (`canDelete`) · **PTKD duyệt yêu cầu** (`canApprove`, mở show) · **XNK duyệt yêu cầu** (`canXNKApprove`) ·
  **Yêu cầu tính giá** (`canCalculate`, sang `PriceCalculateRequest.create?price_asking_request_id=`) · **Huỷ duyệt**
  (`canCancelApprove`).

**Form tạo/sửa** — `form.blade.php` + `formJs.blade.php`
- Thông tin chung (`form:9-68`): Thương hiệu* (select) · Hãng SX (khoá, tự điền từ hàng đầu tiên) · Gửi tới công ty*
  (tự điền = `manufactures.company_id`, `formJs:15-20`) · Người nhận hỏi giá (khoá, lấy từ `getDeputy` =
  `assign_histories` theo hãng×thương hiệu×công ty, `formJs:48-68`) · Ghi chú.
- Bảng Chi tiết (`form:78-128`): STT · Tên hàng · Mã · Model · Thương hiệu · ĐVT (select đơn vị) · SL (cố định 1) ·
  Giá niêm yết (= giá Bán lẻ type 1 của ĐVT, `PriceAskingRequestProduct.blade.php:9-16`) · nút −.
  Nút + ở tiêu đề chỉ hiện khi đã chọn thương hiệu → popup `partials.modals.searchProduct` (`form:89-93`, `:137`).
- Luật thêm hàng (`formJs:7-46`): **mọi hàng phải cùng một hãng SX** (toast "Hàng hóa không cùng hãng sản xuất!"),
  chặn trùng (hàng × ĐVT đầu tiên).
- Footer (`form:139-153`): **Lưu** (status 3) · **Lưu & Gửi** (status 2) · Hủy.

**Xem chi tiết** — `show.blade.php`
- Thông tin chung chỉ đọc (`:23-79`). Bảng Chi tiết khi chưa tính giá (`:88-121`) thêm Trọng lượng(kg) · Kích thước(cm).
- Khi *Đã tính giá* (status 4) bảng đổi thành **kết quả giá** của PTG (`:122-211`): Tên · Mã · ĐVT · Loại giá · Giá mới
  · Định mức đàm phán giá · Ngày hiệu lực (dòng "Đang áp dụng" + các dòng giá hiệu lực).
- Card Ghi chú duyệt (`:214-266`): PTKD duyệt · XNK duyệt · Lý do huỷ duyệt (bắt buộc khi huỷ).
- Card Lịch sử duyệt (`:270-305`): Tài khoản · Nội dung · Hành động · Thời gian.
- Footer (`:307-347`): Duyệt / Không duyệt (PTKD) · Duyệt / Không duyệt (XNK) · Huỷ duyệt · Quay lại.

**Bản in** — `PriceAskingRequestController.php:401-406` → `ReportTemplate::YC_HOI_GIA = 98`
(`PriceAskingRequest.php:689`, dữ liệu `:694-712`: SO_PHIEU, LOGO, CONG_TY, NGAY_LAP, NGUOI_LAP, PHONG_BAN, GHI_CHU,
GHI_CHU_DUYET, GHI_CHU_XNK_DUYET, NGUOI_DUYET(_XNK), THOI_GIAN_DUYET_XNK, CHI_TIET; bảng `:714-760` có cột Giá bán
làm tròn nghìn). **Không có export Excel** (FastExcel chỉ `use`, không dùng).

### 1.2 Yêu cầu tính giá (YCTG)

**Danh sách** — `orders/price_calculate_requests/index.blade.php`
- Cột (`:43-55`): STT · Số yêu cầu · Yêu cầu hỏi giá · Thương hiệu · Hãng SX · Người lập · Ngày lập · Người duyệt ·
  Ngày duyệt · Trạng thái · Hành động.
- Bộ lọc (`:56-79`): Số yêu cầu · Phiếu YCHG · Tên/mã hàng · Thương hiệu · Hãng SX · **Phòng YCHG** · **Người yêu cầu
  hỏi giá** · Trạng thái (4: Đã duyệt/Chờ duyệt/Đang tạo/Đã tính giá, `PriceCalculateRequest.php:30-51`) · Người tạo ·
  Người duyệt + cụm Công ty/Phòng/Bộ phận gate bằng **quyền riêng của màn** (`:80-97`) + thời gian.
- Menu ⚙ (`PriceCalculateRequestController.php:61-80`): In · Sửa (`canEdit`) · Xóa (`canDelete`) · **Tính giá**
  (`canApprove` → `PriceCalculate.create?price_calculate_request_id=`).

**Form tạo/sửa** — `form.blade.php` (+ footer trong `create.blade.php:17-31`, `edit.blade.php:17-31`)
- Thông tin chung (`form:9-85`): **Chọn yêu cầu hỏi giá*** (popup, khoá khi đã có id, `:9-25`) · **Đơn vị tiền tệ***
  (`:26-39`, đổi thì tỉ giá = `currencies.exchange_rate`, `formJs:7-12`) · Tỉ giá (`:40-48`) · Thương hiệu (khoá) ·
  Hãng SX (khoá) · Ghi chú.
- Popup chọn YCHG (`create.blade.php:93-118`): `BaseSearchModal` gọi `PriceAskingRequest.searchData?type=calculate`,
  cột STT · Mã phiếu · Người tạo · Ngày tạo; lọc Mã phiếu · Người tạo. Chọn ⇒ `getDataForPriceCalculate` nạp
  thương hiệu/hãng/ghi chú/hàng (`:80-91`; class `PriceCalculateRequest.blade.php:57-67`). Có lối vào thẳng qua
  `?price_asking_request_id=` (`:120-122`).
- **Tab Hàng hóa** (`form:108-176`): STT · ô tick *Cần tính* (+ tick tất cả) · Tên · Mã · Model · Thương hiệu ·
  HS code · ĐVT · SL(1) · **Giá NCC (ngoại tệ)** (nhập, khoá khi chưa chọn tiền) · Giá NCC (VNĐ) (chỉ khi tỉ giá≠1) ·
  **Thuế NK** (nhập, mặc định `products.import_tax`, `PriceCalculateRequestProduct.blade.php:15`) · Thành tiền sau thuế (VNĐ).
- **Tab Chi phí** (`form:178-243`): chỉ các hàng đã tick; mỗi hàng N dòng: Tên chi phí (select `costs` loại
  `GIA_HANG_HOA=8`, `formJs:6`) · Tỉ lệ (%) · Đơn giá (ngoại tệ) · Đơn giá (VNĐ) · Thành tiền (VNĐ) · link
  "+ Thêm chi phí" / ✕. Dòng chi phí mặc định lấy từ `manufactures.costs` (`PriceCalculateRequestProduct.blade.php:12-14`).
- Footer: **Lưu** (3) · **Lưu & Gửi** (2) · Hủy.

**Xem chi tiết** — `show.blade.php`: dùng lại form ở chế độ chỉ đọc + card Ghi chú duyệt (`:16-32`) + nút
**Tính giá** (`canApprove`, link sang tạo PTG) · **Không duyệt** (`canReject`) · Quay lại (`:34-50`).

**Bản in** — `ReportTemplate::YC_TINH_GIA = 99` (`PriceCalculateRequest.php:433`). Không export.

### 1.3 Phiếu tính giá (PTG)

**Danh sách** — `orders/price_calculates/index.blade.php`
- Cột (`:43-53`): STT · Số yêu cầu (thực ra là số PTG) · Yêu cầu tính giá · Thương hiệu · Hãng SX · Người lập ·
  Ngày lập · Trạng thái · Hành động.
- Bộ lọc (`:54-87`): Số phiếu · Phiếu YCTG · Tên/mã hàng · Thương hiệu · Hãng SX · Phòng YCTG · Phiếu YCHG · Phòng
  YCHG · Trạng thái (**lấy nhầm `PriceCalculateRequest::STATUSES`**, 4 trạng thái, trong khi PTG chỉ có 1 và 3 —
  `:76-77` vs `PriceCalculate.php:37-51`) · Người tạo · Người duyệt. Cụm Công ty/Phòng chỉ khi `?type=all` (`:88-97`).
- `?type=all` ⇒ phạm vi theo quyền "Xem DS tính giá bán theo…", không có type ⇒ chỉ phiếu mình tạo
  (`PriceCalculate.php:145-160`).
- Menu ⚙ (`PriceCalculateController.php:54-65`): chỉ **Sửa** (`canEdit` = Đang tạo + người tạo). In bị comment.

**Form tạo/sửa** — `form.blade.php` (footer `create.blade.php:18-32`, `edit.blade.php:18-32`)
- Thông tin chung (`form:9-85`): Chọn yêu cầu tính giá (popup, link mở YCTG tab mới, `:9-30`) · Đơn vị tiền tệ
  (**khoá**, lấy từ YCTG, `:31-39`) · **Tỉ giá** (sửa được, `:40-48`) · Thương hiệu (khoá) · Hãng SX (khoá) ·
  Người hỏi giá (= người tạo YCHG) · Ghi chú.
- Popup chọn YCTG (`create.blade.php:102-127`): `PriceCalculateRequest.searchData?type=calculate` (chỉ YCTG
  *Chờ duyệt*, cần quyền "Tính giá bán"), cột STT · Mã phiếu · Người tạo · Ngày tạo.
- **Tab Hàng hóa** (`form:112-171`): STT · tick Cần tính · Tên · Mã · Model · **Code đặt hàng** · ĐVT · Giá NCC
  (ngoại tệ, nhập) · Đơn giá VNĐ (khi ngoại tệ) · Thuế NK(%) · Thành tiền sau thuế (VNĐ). (Bỏ Thương hiệu, HS code,
  SL so với YCTG.)
- **Tab Chi phí** (`form:172-235`): y hệt tab Chi phí của YCTG.
- **Tab Tính giá** (`form:236-354`) — bảng rowspan:
  - Cột gộp theo hàng: STT · Tên · **Mã hàng + ô Ghi chú** (textarea, khi duyệt ghi đè `products.note`,
    `PriceCalculate.php:363-370`) · ĐVT · Đơn giá VNĐ (*thực ra hiển thị `amount_exchange_after_tax`*, `:272`) ·
    Tổng chi phí · **Chi phí khác** (nhập) · **Giá nhập kho**.
  - Khối **Giá bán** cho từng loại giá (theo `product_unit_prices` của công ty yêu cầu): Loại · **Hệ số** · Giá công
    thức · **Giá mới** · **Định mức đàm phán giá** · Ngày hiệu lực ("Đang áp dụng"). Link "Thêm giá hiệu lực" khi loại
    giá chưa có dòng hiệu lực (`:285-289`) ⇒ dòng con: Hệ số · Giá công thức · Giá · ĐMGG · Ngày hiệu lực + ✕
    (`:312-343`). BE chỉ cho **tối đa 1 giá hiệu lực / loại**, ngày > hôm nay.
- Footer: **Lưu** (3) · **Lưu & Duyệt** (1) · Hủy. Lỗi "Cần xử lý giá đang chờ duyệt…" bật SweetAlert
  (`create.blade.php:64-75`).

**Xem chi tiết** — `show.blade.php`: chỉ form chỉ đọc + nút Hủy. Không có nút duyệt/in.

**Bản in** — route có (`PriceCalculate.print`) nhưng menu đã comment. Template `TINH_GIA = 100`
(`PriceCalculate.php:801-825`); 🐞 `result_table` không tồn tại (`:824`) ⇒ khối TINH_GIA trống; bảng hàng in
`$product->qty` và cột Đơn giá VNĐ rỗng (`:827-850`).

### 1.4 Kết quả tính giá (KQTG)

- Danh sách `orders/price_calculate_results/index.blade.php:43-66`: STT · YCHG · YCTG · PTG · Người yêu cầu ·
  Người lập · Ngày lập · Hành động (menu ⚙ **rỗng**, In bị comment `PriceCalculateResultController.php:55-63`).
  Lọc: 3 số phiếu · Tên/mã hàng · Người tạo · Người yêu cầu.
- Xem `show.blade.php`: 3 ô số phiếu + bảng Tên · Mã · ĐVT · Loại · Giá mới · ĐMGG · Ngày hiệu lực (`:52-97`).
- 🐞 Bản in gọi `ReportTemplate::KET_QUA_TINH_GIA` (`PriceCalculateResult.php:155`) — **hằng số không tồn tại** trong
  `ReportTemplate.php` ⇒ in sẽ lỗi. `canView()` luôn `return true` (`:147-149`).
- **Không có mục menu** nào trỏ tới KQTG — chỉ vào qua thông báo khi PTG duyệt.

---

## 2. Công thức FE (để port)

Nguồn: `partials/classes/order/PriceCalculateRequestProduct(Cost).blade.php` (YCTG),
`PriceCalculateProduct(Cost).blade.php` (PTG), `partials/classes/sale/ProductPrice.blade.php`,
`ProductExpectedPrice.blade.php`. YCTG và PTG dùng **cùng công thức** phần đầu vào.

### 2.1 Tỉ giá
- Chọn tiền tệ ⇒ tỉ giá = `currencies.exchange_rate` (`price_calculate_requests/formJs:7-12`); ô hiển thị dạng
  `1,234` (`PriceCalculateRequest.blade.php:49-55`); gửi `exchange_rate ?? 1`.
- Cột "(VNĐ)" chỉ hiện khi `currency && exchange_rate != 1` (`is_foreign`, `PriceCalculate.blade.php:66-68`).
- PTG: tiền tệ khoá, tỉ giá sửa được. 🐞 BE `is_foreign` so `currency != 'VNĐ'` (`PriceCalculate.php:904-907`) trong
  khi `currency` lưu **id** ⇒ luôn "ngoại tệ", luôn lấy tỉ giá từ request.

### 2.2 Đầu vào → Giá nhập kho (`PriceCalculateProduct.blade.php`)
```
supplier_price_exchange (Đơn giá VNĐ)  = supplier_price × exchange_rate                 (:49-51)
import_tax                              kẹp 0..100                                       (:39-43)
amount_exchange_after_tax               = Đơn giá VNĐ × (1 + import_tax/100)             (:53-55)
Chi phí — nhập Tỉ lệ %:   value = rate × supplier_price / 100   (trên giá NCC NGOẠI TỆ, CHƯA thuế)  Cost:18-23
Chi phí — nhập Đơn giá:   value kẹp ≤ supplier_price; rate = round2(value / supplier_price × 100)    Cost:29-37
value_exchange (Thành tiền VNĐ)         = exchange_rate × value                          Cost:14-16
sum_cost (Tổng chi phí)                 = Σ value_exchange                               (:57-61)
cost_price (Giá nhập kho)               = amount_exchange_after_tax + sum_cost + other_cost   (:77-79)
```
- ✅ Nhánh `wt-erp-2d1` **đã cộng từ sau thuế** (comment #11334, `:75-76`) — khớp "dữ liệu thật" mà mockup §29b đo.
  Ghi chú 🐞 trong design §29b ("develop_01 cộng từ chưa thuế") **đã lỗi thời** với nhánh này.
- Chi phí: ô Tỉ lệ và Đơn giá **ràng nhau 2 chiều**, đơn giá không được vượt giá NCC (tức chi phí ≤ 100%).
- Ô nhập khoá khi chưa chọn tiền tệ (`ng-disabled="!form.currency || show"`).

### 2.3 Giá bán (`ProductPrice.blade.php`, chạy trong ngữ cảnh `is_price_calculate_context`)
```
Sửa Hệ số loại X:     price_X = round(coef × cost_price / 100) × 100      (tròn TRĂM)        :197-204
Sửa Giá loại X:       price_X = số nhập                                                      :174-182
Sửa ĐMGG:             kẹp 0..100                                                             :217-226
Nếu X = Bán lẻ(1):    ghi đè cùng trường (price / coef / ĐMGG) cho MỌI loại ≠ TMĐT          :179-181,203,225
                      (PriceCalculateProduct.updatePrices :97-113) rồi tính lại TMĐT
TMĐT(6):              price = round(price_bán_lẻ × k) · coef = coef_bán_lẻ × k · ĐMGG = 0   :95-104
                      k = CONFIG.coefficient_ecommerce_price (configs, = 1,3); setter bị chặn (can_edit=false)
                      ⇒ thực chất chỉ đọc, dù input không disabled (form:292,299)
Giá công thức:        cost_price × coef   (KHÔNG làm tròn; TMĐT tròn NGHÌN)                   :228-248
Mở màn tạo mới:       recalcAllPrices — giá Bán lẻ = round(coef_hiện_hành × cost/100)×100,
                      rồi lan sang các loại khác (chỉ khi chưa lưu)                         PriceCalculateProduct:18,30-37
Phiếu đã lưu:         hiển thị nguyên giá DB, không tính lại (is_saved_record)               :21-28; ProductPrice:109
```
Giá hiệu lực (`ProductExpectedPrice.blade.php`):
```
Sửa Hệ số:   price = coef × cost_price        (KHÔNG tròn trăm — lệch với dòng hiện hành)   :87-94
TMĐT:        = giá hiệu lực Bán lẻ cùng ngày × k (không có thì lấy giá Bán lẻ hiện hành) ; khoá  :19-36,54-72
Ngày:        dd/mm/yyyy ⇄ Y-m-d                                                              :143-151
```
Validate BE (`PriceCalculateController.php:100-127`): giá NCC, chi phí khác bắt buộc ≥0; hệ số 0..<100; giá hiệu lực
≤1/loại, hệ số ≤99, ngày > hôm nay; ĐMGG 0..100.

Khi duyệt PTG (`PriceCalculate.php:333-375`, `updatePriceWithApproval :377+`): chặn nếu hàng có `product_approves`
chưa duyệt; ghi `products.note`; ghi giá vào `product_unit_prices` + giá vốn `product_company_units` của
**`products.company_id` (công ty quản lý hàng)**; nếu công ty bật `is_company_price` (+ `is_all_brand`/`brand_ids`) thì
ghi vào cột `*_wait_approve` + cờ ⇒ sang màn **Duyệt giá bán** (G5 HRM đã có).
⚠️ Lệch nội bộ ERP: **nạp** giá theo công ty YCTG (`PriceCalculateRequest.php:135-151`, G3) nhưng **ghi** theo công ty
quản lý hàng (`PriceCalculate.php:385-389`, @TODO-PHASE7). Đã có ở HRM `productPriceModel.js` (xem mục 5).

---

## 3. Quyền (ERP `database/seeds/PermissionsTableSeeder.php`)

| id | Tên | Nhóm | Dùng ở đâu |
|---:|---|---|---|
| 144 | Kế toán mua hàng | Kế toán | **YCTG**: nút *Tính giá* + *Không duyệt* (`PriceCalculateRequest.php:375-387`), mở `getDataForPriceCalculate` + `store` PTG (`PriceCalculateController.php:134`); xem YCTG ≠ Đang tạo (`:369`); xem mọi PTG (`PriceCalculate.php:297`); nhận thông báo YCTG mới (`:401`) |
| 1003 | PTKD duyệt yêu cầu hỏi giá | Yêu cầu hỏi giá | YCHG `canApprove/canReject` (+ trong phạm vi quyền xem) `PriceAskingRequest.php:486-500`; danh sách `?type=approve` |
| 1004 | XNK duyệt yêu cầu hỏi giá | " | YCHG `canXNKApprove/Reject` + `canCancelApprove`, **chỉ người mua được phân công** (`assign_histories`) `:503-558` |
| 1005 | Lập yêu cầu tính giá | " | route `create/edit` YCTG (middleware `routes/web.php:2266-2267`), `store` (`PriceCalculateRequestController.php:133`), `canEdit/canDelete` YCTG (`PriceCalculateRequest.php:389-397`), menu *Yêu cầu tính giá* trên YCHG (`canCalculate` `PriceAskingRequest.php:560-567`) |
| 1006 | Tính giá bán | " | chỉ lọc danh sách `?type=calculate` — tức **popup chọn YCHG** ở form YCTG (`PriceAskingRequest.php:323-330`) và **popup chọn YCTG** ở form PTG (`PriceCalculateRequest.php:180-198`) |
| 1007 / 1008 / 1009 / 1036 | Xem danh sách YCHG theo tổng công ty / DS … theo công ty / phòng ban / bộ phận | " | phạm vi YCHG (`VIEW_SCOPE_PERMISSIONS` `:88-93`) |
| 1010 / 1011 / 1012 / 1035 | Xem DS tính giá bán theo tổng công ty / công ty / phòng ban / bộ phận | " | phạm vi PTG (`PriceCalculate.php:145-160`, `canView :290-320`) + popup YCHG type=calculate (`CALCULATE_SCOPE_PERMISSIONS`) |
| 1013 / 1014 / 1015 / 1034 | Xem DS yêu cầu tính giá bán theo tổng công ty / công ty / phòng ban / bộ phận | " | phạm vi YCTG (`PriceCalculateRequest.php:155-215`, `canView :338-372`); cụm lọc công ty ở list (`index:80-97`) |
| 71 | Tổng hợp đặt hàng | Mua hàng | chỉ gate **menu** YCHG (`topmenubar.blade.php:1533-1535`, `:2382-2384`) |

Gate theo nút (tóm tắt):
- YCHG: Sửa/Xóa = người tạo + trạng thái 3/6/8/9 (không cần quyền) · PTKD duyệt = 1003 · XNK duyệt/Không duyệt/Huỷ
  duyệt = 1004 + người mua phân công · Lập YCTG = 1005 + trạng thái 1 + chưa có YCTG.
- YCTG: Sửa/Xóa = người tạo + Đang tạo + 1005 · Tính giá / Không duyệt = 144 + Chờ duyệt.
- PTG: tạo = 144 (qua `canApprove` của YCTG) — **route `create` không có middleware**; popup chỉ ra dữ liệu nếu có 1006;
  Sửa = người tạo + Đang tạo (không cần quyền) · Xóa = tắt (`canDelete` return false).
- KQTG: không gate.

Menu (`resources/views/layouts/topmenubar.blade.php`):
- *Khởi tạo › Hàng hóa*: "Phiếu Yêu cầu hỏi giá" (`:327`, không gate).
- *Kế toán › Quản lý giá - CTKM*: "Phiếu tính giá hàng hóa" `?type=all` (`:931`, không gate) — kế bên đã có link
  "Cập nhật giá bán (HRM)" (`:932`).
- *Mua hàng › Hàng tạm - Hỏi giá*: "Phiếu yêu cầu hỏi giá" (gate 71, `:1534`) · "Phiếu yêu cầu tính giá" (`:1536`, không gate).
- *Chờ duyệt › Mua hàng*: "Phiếu yêu cầu hỏi giá chờ duyệt" `?type=approve` (gate 71, `:2383`).
- KQTG: không có menu.

HRM hiện **chưa có quyền nào** của luồng này. ⚠️ Các id ERP **trùng id HRM**: 1003 (HRM = "Xem danh mục vai trò dự án"),
1006 (HRM = "Xem danh mục lĩnh vực khách hàng"), 144 (HRM có dòng comment) — phải cấp id mới (HRM đang dùng tới 1675).

---

## 4. So với mockup HRM đã chốt (§29, §33o–§33s)

Mockup: `mockup-luong-xay-dung-hang-hoa.html` (màn `sc-yc`/`sc-ycf`/`sc-pt`/`sc-ptf`, JS `:5490-6365`, popup
`mask-tt` `:2147-2160`, `mask-cyc`, `mask-chh`); design `design.md:2024-2190` (§29), `:2845-2983` (§33o–§33s).

### 4.1 Luồng
| # | ERP | Mockup HRM | Ghi chú |
|---|---|---|---|
| L1 | Chuỗi 4 chứng từ **YCHG → YCTG → PTG → KQTG** | Chỉ **YCTG → PTG**; nguồn YCTG là hàng *Đang nhập thông tin* (popup chọn hàng) | **Bỏ YCHG + KQTG**? (chưa có dòng chốt) |
| L2 | YCTG phải được **duyệt** (KT mua hàng bấm *Tính giá* / *Không duyệt*) | Gửi xong là *Chờ tính giá*, không có bước duyệt/không duyệt | §29f-3 còn treo |
| L3 | YCTG – PTG **1–1**, mỗi YCTG một thương hiệu/hãng | YCTG **nhiều thương hiệu–hãng**, tự gom nhóm cha–con; YCTG – PTG **1–n** (mỗi nhóm một phiếu); YCTG *Đã tính giá* khi đủ nhóm | §33o, §33p |
| L4 | Ai lập PTG: người có quyền 144 (+1006 để thấy popup) | **Đúng người phụ trách hãng** (`assign_employee_manufactures`), không phải thì ẩn nút | §33q |
| L5 | YCTG sang *Đã duyệt* ngay khi PTG lưu lần đầu | Hàng sang *Đang tính giá* khi PTG lưu; PTG duyệt ⇒ hàng *Đang kinh doanh* | trạng thái nhóm: Chờ lập phiếu → Đang tạo → Đã duyệt |
| L6 | Duyệt PTG ghi giá công ty quản lý hàng (G3 tạm) | Phiếu "của công ty đang đăng nhập", giá riêng công ty | luật chính thức P9/Phase 7 |
| L7 | Lối vào PTG: menu + nút trên YCTG | + nút **Tính giá** ở màn *Dữ liệu hàng hoá công ty* (mở phiếu dở / phiếu mới từ YCTG đang chờ) | §29g |

### 4.2 Danh sách YCTG
- ERP: Số yêu cầu · YCHG · Thương hiệu · Hãng SX · Người lập · Ngày lập · Người duyệt · Ngày duyệt · Trạng thái · ⚙.
- Mockup (`:5656`): Số phiếu (+ ghi chú) · **Số mã hàng** · **Nhóm / Phiếu tính giá** (`x/n nhóm đã duyệt giá`, bung
  dòng nhóm) · **Công ty quản lý hàng hoá** · **Đơn vị tiền tệ (+ tỉ giá)** · Người lập · Ngày lập · Trạng thái · Hành động.
- Mockup **bỏ**: YCHG, Thương hiệu, Hãng SX (chuyển xuống dòng nhóm), Người duyệt, Ngày duyệt. Bộ lọc mockup chỉ có ô
  tìm nhanh (ERP 10 ô + cụm công ty/phòng).
- Dòng nhóm (mockup): Thương hiệu — Hãng · số mã · Người phụ trách · số PTG · trạng thái nhóm · nút Lập phiếu /
  Tính giá tiếp / Xem phiếu. ERP không có.

### 4.3 Form YCTG
| | ERP | Mockup |
|---|---|---|
| Thông tin chung | Chọn YCHG* · Tiền tệ* · Tỉ giá · Thương hiệu · Hãng · Ghi chú | **Công ty đề nghị** · Tiền tệ* · Tỉ giá · **Người lập** · Ghi chú (không YCHG, không thương hiệu/hãng) |
| Nguồn hàng | nạp nguyên từ YCHG | popup **Chọn hàng hoá** (hàng *Đang nhập thông tin* chưa có trong yêu cầu; lọc Thương hiệu · Công ty quản lý; tick trang / "Chọn tất cả N kết quả lọc"; 20/50/100) |
| Bảng hàng | tab **Hàng hóa** (tick cần tính · HS code · ĐVT · SL · **Giá NCC · Thuế NK · Thành tiền sau thuế**) + tab **Chi phí** | **một bảng**, không tab: STT (La Mã cha / 1-2-3 con) · Mã · Tên · Model · **Công ty quản lý** · **Chính sách giá nội bộ** (+ Tạm tính) · nút xoá |
| Nhập giá | **Có** — giá NCC, thuế NK, chi phí nhập ngay ở YCTG rồi PTG kế thừa | **Không** — mọi số nhập ở PTG |
| Footer | Lưu · Lưu & Gửi · Hủy | Lưu nháp · Lưu & gửi tính giá · Quay lại |

### 4.4 Danh sách PTG
- ERP: Số · YCTG · Thương hiệu · Hãng · Người lập · Ngày lập · Trạng thái · ⚙(Sửa).
- Mockup (`:5935`): Số phiếu · YCTG · **Thương hiệu – Hãng SX** (gộp 1 cột) · **Số mã hàng** · **Công ty quản lý** ·
  Người lập · Ngày lập · Trạng thái · Hành động (Sửa khi Đang tạo / Xem khi Đã duyệt) + bộ lọc nâng cao 6 ô.
  Nút **Tạo phiếu tính giá** mở popup chọn YCTG (STT · Số phiếu · Số mã hàng · Công ty quản lý · Người lập · Ngày lập ·
  Chọn) — nhưng §33p nói lập phiếu nay **luôn đi từ một nhóm** ⇒ nút này + popup có còn không?

### 4.5 Form PTG
| | ERP | Mockup |
|---|---|---|
| Thông tin chung | YCTG · Tiền tệ (**khoá**) · Tỉ giá · Thương hiệu · Hãng · Người hỏi giá · Ghi chú | YCTG* (+nút chọn) · **Công ty quản lý hàng hoá** · Tiền tệ* (**sửa được**) · Tỉ giá* · **Người đề nghị · Ngày đề nghị** · Ghi chú. **Bỏ** Thương hiệu/Hãng (§33o-1) và Người hỏi giá. Thêm badge trạng thái + "Hàng lấy từ công ty khác" |
| Tab Hàng hoá | tick · Tên · Mã · Model · Code đặt hàng · ĐVT · Giá NCC · Đơn giá VNĐ (khi ngoại tệ) · Thuế NK · Thành tiền sau thuế | thêm **Mã vạch** dưới mã, **Chính sách giá nội bộ (+ Tạm tính)**; đổi tên "Giá NCC" → **Giá mua**; Đơn giá VNĐ hiện luôn; ô giá mua **để trống** (ERP kế thừa từ YCTG) |
| Tab Chi phí | như YCTG, mặc định chi phí của hãng | như ERP, mặc định 1 dòng "Cước vận tải quốc tế", chọn dòng mới tự lấy chi phí chưa dùng, không cho xoá dòng cuối |
| Tab Tính giá | Đơn giá VNĐ (thực là sau thuế) · Tổng CP · CP khác · Giá nhập kho · Loại · Hệ số · Giá công thức · Giá mới · ĐMGG · Ngày hiệu lực | thêm cột **Thành tiền sau thuế** (tách khỏi Đơn giá VNĐ); khối chính sách bản gọn trong ô Mã; "Giá mới" → **Giá bán**; nút **Giá hiệu lực** mỗi dòng (ERP: link chỉ khi chưa có) |
| Hệ số | sửa Bán lẻ **lan sang 4 loại** khác (+ TMĐT tính lại) | **hệ số riêng từng loại** (comment mockup `:5986-5988`), mặc định 1.25/1.18/1.15/1.12/1.10 |
| TMĐT | = Bán lẻ × 1,3, chỉ đọc | giống, ghi chú "= Bán lẻ × 1.3" |
| Giá công thức | không tròn | mockup `soVND` tròn đồng |
| Ghi chú dòng | textarea, duyệt ⇒ ghi `products.note` | ô input "Ghi chú" (chưa nói ghi đi đâu) |
| ĐVT | theo ĐVT của YCHG (1 ĐVT/dòng) | đơn vị cơ bản; mockup ghi rõ bản thật phải đủ ĐVT (`:1011`) |
| Validate | BE: giá NCC, CP khác bắt buộc… | FE: chặn nếu chưa nhập giá mua |
| Footer | Lưu · Lưu & Duyệt · Hủy | Lưu · Lưu & duyệt giá · Quay lại |

### 4.6 Phần chỉ có ở mockup
- Cột **Chính sách giá nội bộ** + popup **Tạm tính giá mua từ Công ty quản lý** (`:5579-5650`): cách tính (giá vốn
  +% / giá bán −%) · 2 tỷ lệ Nhập khẩu nguyên lô / Tồn kho · giá vốn công ty quản lý (chỉ khi theo giá vốn) · 6 giá bán ·
  giá mua suy ra, làm tròn trăm, **chỉ tham khảo**. Hãng chưa cấu hình ⇒ badge cam, vẫn lập phiếu.
- Gom nhóm Thương hiệu–Hãng, người phụ trách, STT La Mã.
- ERP có mà mockup chưa vẽ: card **Ghi chú duyệt / Không duyệt** của YCTG, **lịch sử duyệt**, **bản in**, cảnh báo
  "giá đang chờ duyệt" khi duyệt PTG, **KQTG**.

---

## 5. Tái dùng được trong hrm-client

| Thứ | Ở đâu | Dùng cho |
|---|---|---|
| **`utils/productPriceModel.js`** — `Calc` (T1–T11), `PRICE_TYPES` (thứ tự 1·5·2·3·4·6), `ECOM=1.3`, `blockRows`, `validateUnit`, `buildPayload`, `fmt/toNum/fmtCoef`, `roundK` | `:1-366` | Tab Tính giá: **đúng** các phép ERP ở mục 2.3 (setCoef tròn trăm `:163-169`, spread Bán lẻ `:148-153`, TMĐT `:140-146`, recipe tròn nghìn TMĐT `:181-184`, hiệu lực không tròn `:186-193`, TMĐT hiệu lực chỉ đọc `:200-206`). Chỉ cần thêm phần đầu vào (giá mua × tỉ giá, thuế NK, chi phí ⇒ `u.cost`). Nếu chốt "hệ số riêng từng loại" thì **không** gọi `spread` |
| `components/product/price/ProductPriceTable.vue` (839 dòng) | bảng nhập giá khối hàng × ĐVT nhiều `<tr>` rowspan, `V2BaseTableScroll`, cột dính trái, badge cờ duyệt, giá hiệu lực | khuôn bảng tab Tính giá (6 loại giá + dòng hiệu lực) |
| `components/product/price/ProductPriceApprovalTable.vue` + `pages/finance/product-price-approvals/index.vue` (G5, quyền 1658) | màn Duyệt giá bán | đích của PTG khi công ty bật `is_company_price` — không phải làm lại |
| `pages/finance/product-prices/index.vue` (G4, quyền 1657) | khuôn list-page: `V2BaseSmartFilterPanel` floating + `V2BasePagination` + gate fail-closed `canView` + `unsavedChangesMixin` | khuôn danh sách YCTG / PTG và form có dữ liệu chưa lưu |
| `components/product/ProductListPage.vue` + `utils/product-list-screens.js` (màn `entering` `:109`) | 4 màn hàng hoá dùng chung (`extends`) | màn *Đang nhập thông tin* — chỗ đặt nút **Lập yêu cầu tính giá**; trạng thái "Chờ tính giá bán" (`:200`) đã có |
| `components/product/form/ProductItemPickerModal.vue` | popup chọn nhiều hàng (`V2BaseModal` + `V2BaseDataTable` + checkbox), API `master-data/products/item-search` | nền cho popup **Chọn hàng hoá** của YCTG; còn thiếu lọc Thương hiệu / Công ty quản lý, phân trang, "chọn tất cả kết quả lọc", lọc theo trạng thái *Đang nhập thông tin* |
| `pages/customer-care/services/components/ProductSearchModal.vue` (852 dòng) | popup tìm hàng có bộ lọc + phân trang | tham khảo nếu cần bộ lọc đầy đủ |
| `components/subsystem-menu/finance.js:434-451` | nhóm rail *Quản lý giá - CTKM › Giá bán* đã có mục **"Phiếu tính giá"** (chưa link) | gắn link + `isShow` khi có màn |
| `components/product/price/ProductPriceHistoryModal.vue`, `ProductRecipeModal.vue` | lịch sử giá, công thức giá | xem thêm từ tab Tính giá (tuỳ chọn) |

⚠️ Đụng tên: `components/subsystem-menu/presale.js:56` đã có mục **"Yêu cầu tính giá bán"** → `/assign/pricing-requests`
(chứng từ bán hàng/báo giá, KHÔNG phải YCTG hàng hoá). Đặt tên màn mới phải tránh nhầm (vd. "Yêu cầu tính giá hàng hoá").

Chưa có ở HRM: bảng/route/quyền cho YCTG–PTG, danh mục `costs` loại GIA_HANG_HOA và `currencies` (cần API đọc từ DB
gộp), bảng phân công `assign_employee_manufactures` (design §33q nói "nằm sẵn trên HRM" — cần kiểm lại).

---

## 6. Câu hỏi nghiệp vụ cần chốt (trước khi code)

1. **YCHG và KQTG**: bỏ hẳn ở HRM (YCTG lập thẳng từ hàng *Đang nhập thông tin*), hay vẫn giữ chuỗi YCHG → YCTG cho
   hàng **nhập khẩu hỏi giá NCC** (luồng ERP đang chạy 4.029 phiếu)? Nếu bỏ: dữ liệu YCHG/KQTG cũ xem ở đâu?
2. **Giá NCC / thuế NK / chi phí nhập ở YCTG hay PTG?** ERP nhập ở YCTG (người yêu cầu biết giá NCC), mockup dời hết sang
   PTG. Với hàng nhập khẩu, người lập PTG (XNK phụ trách hãng) có giá NCC không?
3. **Bước duyệt YCTG** (KT mua hàng *Tính giá / Không duyệt*, quyền 144): giữ hay bỏ? (§29f-3 còn treo) Nếu bỏ thì
   "Không duyệt / trả lại" yêu cầu làm thế nào?
4. **Hệ số giá**: riêng từng loại (mockup) hay sửa Bán lẻ **lan** sang 4 loại (ERP + G4 HRM `Calc.spread`)? Hai màn
   Cập nhật giá bán và Phiếu tính giá có nên cùng một luật không?
5. **Tiền tệ ở PTG** sửa được (mockup) hay khoá theo YCTG (ERP)? Một YCTG nhiều nhóm thì tiền tệ/tỉ giá ở cấp YCTG
   hay cấp từng phiếu?
6. **Nút "Tạo phiếu tính giá" + popup chọn YCTG** ở danh sách PTG còn giữ không, khi §33p đã chốt lập phiếu luôn từ
   dòng nhóm của YCTG?
7. **Công ty ghi giá khi duyệt PTG**: công ty lập phiếu (mockup/D9) hay công ty quản lý hàng (ERP G3 tạm, @TODO-PHASE7)?
8. **Quyền HRM**: dùng bộ tên ERP (Lập yêu cầu tính giá · Tính giá bán · Kế toán mua hàng · 12 quyền phạm vi xem) với id
   mới, hay gom lại (vd. 1 quyền lập YCTG + 1 quyền tính giá + gate người phụ trách hãng)? Phạm vi xem 4 cấp (tổng
   công ty/công ty/phòng/bộ phận) có giữ?
9. **Ghi chú dòng ở tab Tính giá**: vẫn ghi đè `products.note` khi duyệt như ERP?
10. **Gate giá vốn liên công ty** trong popup Tạm tính (§29f-2): quyền nào được thấy (Quản lý giá / 1657)?
11. **Bản in** YCTG / PTG: cần không (ERP: in PTG đã tắt và hỏng `result_table`, in KQTG lỗi hằng số)?
12. **ĐVT**: PTG tính cho 1 ĐVT (ERP, theo YCHG) hay đủ mọi ĐVT đã khai (mockup `:1011`)?

## 7. Lỗi ERP thấy khi đọc (ghi lại, không vá)
- `price_calculates/index.blade.php:76-77` lọc trạng thái PTG bằng `PriceCalculateRequest::STATUSES`.
- `PriceCalculate.php:904-907` `is_foreign` so `currency` (id) với `'VNĐ'` ⇒ luôn true.
- `PriceCalculate.php:824` gọi `result_table` không tồn tại; `:827-850` in `qty` và cột Đơn giá VNĐ rỗng.
- `PriceCalculateResult.php:155` `ReportTemplate::KET_QUA_TINH_GIA` không tồn tại.
- `price_calculates/form.blade.php:272` cột "Đơn giá VNĐ" ở tab Tính giá hiển thị **thành tiền sau thuế**.
- `PriceCalculateController::store` gọi `$req->approve()` ngay cả khi PTG chỉ "Lưu".
- `PriceCalculateRequest.php:182` popup chọn YCTG cần quyền "Tính giá bán" (1006) nhưng tạo PTG lại cần "Kế toán mua
  hàng" (144) ⇒ người chỉ có một trong hai quyền bị kẹt im lặng.
- `PriceAskingRequest.php:323-330` tương tự: lập YCTG cần 1005 nhưng popup chọn YCHG cần 1006.
- `price_calculates/form.blade.php:285` hai `ng-if` trên một thẻ (link "Thêm giá hiệu lực" vẫn hiện khi xem).
