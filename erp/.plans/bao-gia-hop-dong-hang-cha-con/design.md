# Design — Hàng hoá 2 cấp cha-con cho Báo giá / Hợp đồng hãng

> Trạng thái: **ĐÃ CHỐT brainstorm (v2)** — 2026-06-20. Logic v1 đã bỏ. Sẵn sàng viết plan.

---

## 1. Mục tiêu & phạm vi

Cho phép khai báo **hàng hoá 2 cấp cha-con** (cha A, con B/C…) trên **báo giá hãng** và **hợp đồng hãng**, với ràng buộc tỉ lệ cố định và nghĩa vụ giao liên kết (linked) khi xuất hàng.

**Trong phạm vi (chỉ ERP):**
- Báo giá hãng: `FirmQuotation` / bảng `firm_quotation_tab_products` / form `resources/views/sale/firm/quotations/form.blade.php`.
- Hợp đồng hãng: `FirmContract` / bảng `firm_contract_tab_products` / form `resources/views/sale/firm/contracts/form.blade.php`.
- Yêu cầu xuất hàng từ HĐ hãng (ProductExportRequest) — nơi áp logic quỹ cha-con.

**Ngoài phạm vi (làm sau):**
- ZT Firm Contract (`/zt-firm-contracts`, blade `ztect_contracts/form.blade.php`): dùng chung model `FirmContractTabProduct` nên data-layer tương thích, nhưng KHÔNG làm UI cha-con lần này.
- Báo giá/HĐ dự án, dịch vụ (model + form riêng).
- Đường HRM: HĐ lập từ báo giá HRM tạm thời giao phẳng (không cha-con). Cha-con bên HRM (module Assign) làm sau.

---

## 2. Cấu trúc cha-con

1. **2 cấp** cố định: cha → con. KHÔNG có cấp cháu (con không làm cha của hàng khác).
2. **Cha, con đều là hàng thật** trong danh mục — có mã, tồn kho, giá riêng.
3. **Quan hệ gắn theo DÒNG, không theo mã hàng:**
   - 1 mã hàng có thể vừa đứng độc lập, vừa làm cha ở cụm này, vừa làm con ở cụm khác.
   - 1 mã con có thể thuộc 2 cha khác nhau ở 2 cụm khác nhau trong cùng phiếu.
   - 1 cha có nhiều con (không giới hạn).
4. **Tỉ lệ con/cha** = số nguyên dương (1, 2, 3…). Không cho số lẻ.
5. **SL con = SL cha × tỉ lệ** — auto tính, khoá sửa tay. Sửa SL cha → SL con cập nhật theo.

---

## 3. Tiền & hiển thị

- **Tổng tiền chỉ tính theo hàng CHA** (SL cha × giá cha). Hàng con KHÔNG cộng vào tổng.
- **Trên FORM (màn hình)** của cả báo giá lẫn HĐ: dòng con hiện đầy đủ — đơn giá + thành tiền dòng (SL con × đơn giá con) — nhưng **không cộng vào tổng cuối**. (Chấp nhận: cộng dồn cột thành tiền tất cả dòng ≠ tổng hiển thị.)
- **Hiển thị gom nhóm:** cha trên, con thụt lề ngay dưới cha.
- **BẢN IN** (báo giá in + HĐ in): **CHỈ in dòng cha** — con KHÔNG in ra cho khách.
- **Báo cáo:** không quan tâm cha-con — liệt kê từng dòng như bình thường.

---

## 4. Nhập liệu (UX form)

- Nút **"+ con"** trên mỗi dòng cha → thêm dòng con **thụt lề** ngay dưới cha; chọn mã con + gõ **tỉ lệ**.
- SL con auto = SL cha × tỉ lệ (input SL con khoá).
- Xoá cha → xoá luôn các con của nó.
- Một cụm = 1 dòng cha + N dòng con, nằm trong cùng 1 tab.

---

## 5. Carryover báo giá → hợp đồng

- Lập HĐ hãng từ **báo giá hãng ERP** → **bê NGUYÊN** cụm cha-con + tỉ lệ + SL sang HĐ.
- Trên HĐ **KHOÁ** cấu trúc cha-con: không cho sửa/thêm/bớt cụm (giữ đúng theo báo giá).
- HĐ tạo tay thuần (không từ báo giá) → không có cụm cha-con.

---

## 6. Nghĩa vụ giao LINKED & quỹ xuất

### Mô hình
- Tổng nghĩa vụ giao quy về "suất cha". Mỗi suất giao được bằng 1 cha HOẶC bộ con tương ứng.
- Cha liên kết với từng con; **các con độc lập với nhau** (B không trừ C và ngược lại).
- Xuất con chỉ "khoá" phần cha tương ứng; xuất cha trừ đều tất cả con.

### Công thức "còn được xuất"
Cụm: cha P (SL HĐ = Q), con i có tỉ lệ r_i (SL HĐ con i = Q × r_i). Gọi `a` = đã xuất cha, `delivered_i` = đã xuất con i (lấy theo `exported_qty`):

```
P_remaining        = Q − a − max_i( delivered_i / r_i )
child_i_remaining  = (Q × r_i) − delivered_i − (r_i × a)
```

Bất biến: `a + max_i(delivered_i / r_i) ≤ Q`.

**Ví dụ A=2, B=4, C=4 (r_B = r_C = 2):**
```
A còn = 2 − a − max(b,c)/2
B còn = 4 − b − 2a
C còn = 4 − c − 2a
```

| Đã xuất | A còn | B còn | C còn |
|---|---|---|---|
| (chưa) | 2 | 4 | 4 |
| B=4 | 0 | 0 | 4 |
| B=4, C=4 | 0 | 0 | 0 |
| A=1 | 1 | 2 | 2 |
| B=2 | 1 | 2 | 4 |
| A=2 | 0 | 0 | 0 |

### Nơi áp
- Logic quỹ (tính "còn được xuất" + validate chặn vượt) đặt ở **bước TẠO YÊU CẦU XUẤT HÀNG** (rút SL từ HĐ). FE + BE đều chặn.
- **Phiếu xuất kho** chỉ thực hiện theo yêu cầu — KHÔNG validate cha-con.
- Giao diện màn yêu cầu xuất **giữ nguyên danh sách phẳng** hiện tại — không thêm UI gom nhóm cha-con. Thay đổi chỉ ở backend (cách tính "còn được xuất").
- 1 mã con ở 2 cụm → 2 dòng riêng trên màn yêu cầu xuất, quỹ tính riêng từng cụm (theo id dòng HĐ).

### Tồn kho & bộ đếm
- Tồn kho **độc lập theo từng mã** (xuất A trừ tồn A, xuất B trừ tồn B…). Quy đổi cha-con CHỈ ở tầng nghĩa vụ giao, không đụng tồn kho.
- `exported_qty` = SL đã xuất, cộng khi làm phiếu xuất hàng → **quỹ cha-con trừ theo `exported_qty`**.
- `warehouse_exported_qty` = giữ nguyên logic hiện tại (lưu ở đâu xử lý ở đó), không đụng.
- Sửa HĐ giảm SL cha xuống dưới mức đã xuất quy đổi → **chặn**.

---

## 7. Thay đổi kỹ thuật

### 7.1 Schema (migration)
Thêm cột vào **`firm_quotation_tab_products`** và **`firm_contract_tab_products`**:
- `child_parent_id` — `unsignedBigInteger` nullable; self-ref tới **id dòng cha** trong cùng bảng. (Phân biệt rõ với cột `parent_id` hiện có = id của Tab.)
- `child_ratio` — `int` nullable; tỉ lệ con/cha (chỉ có ở dòng con).

> Dòng độc lập & dòng cha: `child_parent_id = NULL`. Dòng con: `child_parent_id = <id dòng cha>`, `child_ratio = <int>`.

### 7.2 Refactor bắt buộc — attribution `exported_qty`
- Hiện `ProductExport::syncFirmContractTabProducts` (ProductExport.php:1676–1703) + `WarehouseExportRequest.php:947` cộng `exported_qty`/`warehouse_exported_qty` về dòng HĐ bằng khóa tổ hợp `(firm_contract_id, parent_id=tab_id, product_id, unit_id)->first()`.
- Vì cha-con khiến 1 mã xuất hiện nhiều dòng → match `->first()` sẽ dồn sai. **Chuyển attribution sang id dòng `firm_contract_tab_product_id`.**
- Kiểm tra dữ liệu phiếu xuất đã lưu `firm_contract_tab_product_id` (trong `product_export_request_tab_products`) → dùng trực tiếp.

### 7.3 Service tính quỹ
- Thêm hàm tính `remaining` theo công thức mục 6 cho từng dòng cụm, dùng trong `FirmContractProductExportService::getDataForWarehouseExport` (trả "còn được xuất") + validate khi store yêu cầu xuất.
- Với dòng không cha-con: `remaining = Q − exported_qty` (giữ logic cũ).

### 7.4 Backend store/update báo giá & HĐ
- `FirmQuotationController` + `FirmContractController`: nhận `child_parent_id` + `child_ratio` theo dòng; map id tạm (FE) → id thật khi lưu (vì cha-con tham chiếu nội bộ).
- Validate: tỉ lệ nguyên dương; SL con = SL cha × tỉ lệ; cấu trúc 2 cấp.
- HĐ: chặn sửa cấu trúc cha-con (khoá theo báo giá nguồn).

### 7.5 Frontend (AngularJS 1.3.9)
- Form báo giá + HĐ: thêm nút "+ con", auto-tính SL con, gom nhóm hiển thị (cha trên, con thụt lề), loại con khỏi tổng tiền.
- Carryover: prefill cha-con khi lập HĐ từ báo giá; khoá sửa trên HĐ.
- Validate inline (viền đỏ `is-invalid` + `invalid-feedback`) cho tỉ lệ.

### 7.6 Bản in
- Template in báo giá + HĐ: lọc bỏ dòng con (chỉ render cha).

---

## 8. Edge cases cần xử lý
- Mã con trùng mã ở cụm khác / đứng độc lập → tách theo id dòng, không gộp.
- Xoá cha còn con → cascade xoá con (FE + BE).
- Sửa SL cha sau khi đã xuất một phần → SL con auto đổi, nhưng chặn nếu giảm dưới mức đã xuất quy đổi.
- Báo giá đã có cha-con nhưng HĐ tạo tay (không từ báo giá) → HĐ phẳng, không lỗi.
- Xuất con lệch (B nhiều C ít) → quỹ tính đúng theo `max(delivered_i/r_i)`.

---

## 9. Hiện trạng kỹ thuật (khảo sát)
- **Lưu hàng báo giá:** `firm_quotation_tabs` → `firm_quotation_tab_products` (`parent_id` = tab). Combo 4 cấp (combo_campaign) là cơ chế riêng, KHÔNG dùng cho cha-con này.
- **Lưu hàng HĐ:** `firm_contract_tabs` → `firm_contract_tab_products` (`parent_id` = tab; có `exported_qty`, `warehouse_exported_qty`, các cột giá đàm phán).
- **Xuất kho:** route `firmContract.getDataForWarehouseExport` → `FirmContractProductExportService::getDataForWarehouseExport($contract,$tab_ids,$type,$vat_percent)`; lưu `product_export_request_tabs` / `product_export_request_tab_products` (có `firm_contract_tab_product_id`, `firm_contract_tab_combo_product_id`).
- **Controller:** `app/Http/Controllers/Sale/Firm/FirmQuotationController.php`, `FirmContractController.php`. Model `app/Model/Sale/Firm/Quotation/FirmQuotationTabProduct.php`, `app/Model/Sale/Firm/Contract/FirmContractTabProduct.php`.

---

## 10. Rủi ro lớn
- **Attribution `exported_qty` theo `->first()`** dồn sai khi cha-con → bắt buộc refactor sang id dòng trước khi làm quỹ (mục 7.2). Đây là phần rủi ro nhất, cần test kỹ với HĐ có mã trùng.
- Map id tạm cha-con (FE chưa lưu) → id thật khi store: cần xử lý đúng thứ tự (lưu cha trước, gán `child_parent_id` cho con sau).

---

## 11. Lịch sử — v1 đã BỎ
- v1: cha/con SL độc lập, không ràng buộc tỉ lệ, không linked. Đã bỏ vì v2 ràng buộc tỉ lệ + nghĩa vụ giao linked.
