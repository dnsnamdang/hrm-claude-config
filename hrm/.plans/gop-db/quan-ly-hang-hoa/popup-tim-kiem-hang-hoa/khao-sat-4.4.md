# Bước 4.4 (ERP) — kiểm kê tuỳ chọn 2 partial chính — khảo sát 14/10/2026 (chỉ đọc)

> ERP `wt-erp-2d1` (`feat/2d1-erp-khong-loi`). Endpoint cũ: `SearchController::searchProduct` (l.441-917) và `::searchProductStockBuyer` (l.921-1306).
> Chưa đụng source.

## 1. Cách 2 popup nhận tuỳ chọn + trả hàng
| | `searchProduct` (99 view) | `searchProductQuotation` (27 view) |
|---|---|---|
| Hàm mở | `searchProduct(options, disabled)` — **mọi khoá `options` chép thẳng vào request** (l.121-123); `disabled` chỉ khoá ô lọc trên UI | `searchProduct(quotation, options)` — đọc `quotation.price_type`, `quotation.is_liquidation`; `options.has_product_id` / `is_service_quotation` / `name` |
| Luôn gửi | `price_type=1`, `saleable_stock=1` | `price_type` của chứng từ |
| Trả về | bấm tên ⇒ `$scope.addProduct(row)`; tick (`has_checkbox_all`) ⇒ `addProduct` / `removeProduct` từng dòng | bấm tên ⇒ `addProduct(row)`; tick + "Chọn" ⇒ `addProduct({id})` hoặc 3 nhánh `type_add_product` (merchandise / extend_product / wr_product) popup tự gọi `getData` |
| Màn đọc gì từ dòng | gần như mọi màn chỉ đọc `id` rồi tự gọi `/admin/products/{id}/getData*`; vài màn đọc thêm `name`, `code_raw`, `brand_id`; `sale/services` đọc cả `group` + HTML tên/mã | `id` (+ `name` ở báo cáo) |

⇒ Adapter ERP chỉ cần trả `{id, code, code_raw, name, brand_id}` cho hàm cũ — khớp plan A1.

## 2. Màn đã bị chặn (đã chuyển sang HRM) — loại khỏi phạm vi
`products/*`, `product_infos/*`, `product_templates/*`, `tmp_products`, `products_approve`, `product2`, `price_asking_requests`,
`manufacture_expect_prices` (tạo) — gồm toàn bộ chỗ dùng `group_ids[]` (chọn "dùng cho máy" theo Nhóm cũ). 16 view include nhưng không mở popup (chết).

## 3. Nhóm màn còn sống theo hành vi
| Nhóm | Màn (số view) | Tuỳ chọn | API mới có sẵn? |
|---|---|---|---|
| **N1 Tìm tự do** | ~40 view `()`: kho (YC xuất/nhập/chuyển, tồn đầu kỳ, gộp/tách YCXK), mua (HĐ mua NK/TN, hồ sơ NK, HĐ nguyên tắc), bán (CT KM, combo, mẫu báo giá, PL bổ sung HĐ DV), CSKH (KH-thiết bị, BHSC) · 7 báo giá bán (`searchProductQuotation` #1-7) | không / `brand_id` (15) / `manufacture_id` (6) khoá ô / `name` (1) | **Có** (`brand_ids`, `manufacture_ids`, `keyword` + `lockedFilters`) |
| **N2 Báo cáo — chọn 1 hàng để lọc** | 4 view `{type:'include_deleted'}` (thẻ kho, thẻ kho KT, BC hàng hold, BC buyer) + 18 báo cáo `searchProductQuotation` (truyền `include_deleted` nhưng **không tới server** ⇒ đang chỉ hàng đang KD + có giá loại 1) + ~4 báo cáo `()` | `include_deleted`: bỏ lọc `status≠0` và "đang KD tại công ty" | **Không** |
| **N3 Giới hạn theo hợp đồng** | PL HĐ mua NK (1), PL HĐ mua TN v2 (2, + popup KM), PL HĐ DV (1), PL HĐ hãng / ZT / nguyên tắc (4) — `contract_annexes` truyền `contract_id` nhưng server **bỏ qua** | `*_contract_id` + `request_type='annex'` (chỉ hàng còn SL > 0) | **Không** |
| **N4 Giới hạn theo kho / tồn / giữ hàng** | kiểm kê (2), kiểm kê KT (2), tự kiểm kê (3), YC tự kiểm kê (3), chuyển vị trí (1), YC giữ hàng (1), chuyển giữ hàng v2 (1) | `has_stock`, `is_self_inventory` + `warehouses[]` (tồn theo KHO), `position_transfers`, `has_prepick` (hàng NV đang giữ, chưa hết hạn) | Chỉ `in_stock` (tồn bán được của công ty) — **thiếu tồn theo kho, hàng đang giữ** |
| **N5 Thanh lý** | PL bổ sung HĐ bán (HĐ loại 4), báo giá thanh lý, báo giá thường loại 2 (3) | `is_liquidation` ⇒ chỉ hàng còn tồn + 2 cột ĐMGG hàng thúc đẩy / % giảm thanh lý | `in_stock` có; **2 cột thanh lý chưa có** |
| **N6 CSKH chế độ máy** | Báo giá DV CSKH, YC thông tin BHSC (`has_product_id` = máy; `is_service_quotation`), Báo giá DV bán (ô "Trang thiết bị") | máy ⇒ phụ tùng `productables` máy/nhóm máy + **mọi dầu nhớt**; `is_service_quotation` ⇒ enum `accessories`/`lubricant` | **Có** — spec §4 quy tắc 4 (`machine_id` + `include_service_shared`) |

Ngoài 2 partial, endpoint cũ còn bị gọi trực tiếp (`sale/services` thêm theo nhóm, YC đặt hàng ×6 theo barcode, lỗi thiết bị ×4,
`CreateDeviceErrorModal`, `searchServiceProductJs`, `searchProductStockBuyerApi` cho HRM) ⇒ **giữ nguyên 2 endpoint cũ**, 4.4 chỉ thay popup.

## 4. Khác biệt phạm vi mặc định ERP ↔ API mới
| | ERP hôm nay | API mới |
|---|---|---|
| Hàng không có giá loại 1 (ĐVT cơ bản, công ty) | **bị ẩn** (join giá thành điều kiện lọc) | hiện, giá `null` |
| Tồn | danh sách tồn bán được theo **từng** công ty | tồn bán được của **công ty chứng từ** (spec §4.7) |
| Hàng tạo ở HRM (`product_type` NULL) | hiện (trừ lọc enum) | hiện |
| Hàng chưa xếp catalog | hiện | mặc định ẩn, bật công tắc (spec §4.2) |

## 5. Tự chốt (kỹ thuật / UI)
- **Token**: ERP + HRM chung `JWT_SECRET`. Proxy dùng `jwt_token` của phiên; **ERP local tắt SSO (`IS_USE_SSO` không khai) ⇒ không có token** ⇒
  khi `!config('app.is_use_sso')` proxy tự ký token cho nhân viên đang đăng nhập (chỉ để chạy local); bật SSO mà thiếu/hết hạn token ⇒ 401 + thông báo spec §5.3.
- **Công ty chứng từ** = công ty đang làm việc của người dùng (như popup cũ và HRM C0#1).
- **Chọn nhiều (`has_checkbox_all`, 4 form)**: popup mới tick ⇒ "Thêm (N)" ⇒ gọi `addProduct({id})` từng hàng. Bỏ tick trong popup KHÔNG xoá dòng đã thêm
  (popup cũ xoá ngay; 2 màn YC xuất kho / YC tự kiểm kê còn lỗi sẵn vì không khai `removeProduct`). Hàng đã có ⇒ nhãn "Đã có".
- Khoá ô lọc (`disabled`) ⇒ `lockedFilters` hiện ô đã chọn + khoá.
- `type_add_product` 3 nhánh (CSKH) giữ nguyên trong adapter.

## 6. Chốt của user 14/10
| # | Câu | Chốt |
|---|---|---|
| Q1 | Hàng chưa có giá bảng giá loại 1 | **Hiện, giá "—"** (thống nhất HRM 4.3). Bỏ điều kiện "phải có giá" của ERP ở mọi màn. |
| Q2 | N2 Báo cáo | **Toàn bộ hàng** — chế độ báo cáo bỏ lọc đang KD / catalog (vẫn ẩn hàng tạm); sửa luôn 18 màn `include_deleted` không tới server. |
| Q3 | N3 Hợp đồng | **Popup mới, khoá theo HĐ** — ERP tính danh sách id bằng logic cũ (phụ lục: còn SL > 0) ⇒ API tham số chung "chỉ trong các id này"; trong danh sách bỏ lọc đang KD / catalog; thanh trên popup ghi HĐ. Sửa luôn PL HĐ bán (`contract_id` hôm nay bị bỏ qua). |
| Q4 | N4 Kho / giữ hàng | **Khoá danh sách + cột tồn theo kho** — ERP tính id (tồn theo kho / tồn bán được / hàng NV đang giữ) và điền cột "Tồn tại kho" hoặc "SL đang giữ". |
| Q5 | N5 Thanh lý | **Ngừng hẳn báo giá thanh lý ở ERP** — việc riêng ⇒ ghi **N93** (`ngoai-luong/soat-bang-c.md`). 4.4 KHÔNG làm chế độ thanh lý: 3 màn (báo giá thanh lý, báo giá loại 2, PL bổ sung HĐ loại 4) dùng popup mới **chế độ thường** (bỏ ràng buộc còn tồn + cột thanh lý) — không giữ được popup cũ vì báo giá thường dùng chung partial. |
