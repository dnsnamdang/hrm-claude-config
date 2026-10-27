# Sao chép hàng hoá — khảo sát (24/10/2026)

Nguồn: đọc code ERP `TanPhatDev` (gop_db) + HRM `hrm-api`/`hrm-client` (gop_db) + hồ sơ `quan-ly-hang-hoa/`.
Chưa đụng source. Đường dẫn: `M` = `hrm-api/Modules/MasterData`, ERP tính từ `ERP/TanPhatDev`.

## 1. ERP cũ làm thế nào

- **Copy = mở form tạo điền sẵn**, không clone ở server. `ProductsController@copy` (:1024-1055) nạp
  `Product::getDataForEdit` (cùng hàm màn Sửa) → view `products/copy.blade.php` (dùng chung `products.form`/`formJs`)
  → bấm Lưu POST `productStore` → `Product::createRecord`. Không lưu nguồn copy (`copied_from` không có).
- **Điền sẵn**: toàn bộ thông tin chung (tên, model, thương hiệu, hãng, xuất xứ, nhóm, VAT, thuế NK, HS, bảo hành,
  định mức, khối lượng, kích thước…), NCC, ĐVT, giá vốn/giá mua/hệ số, thuộc tính (nạp lại theo nhóm), 4 bảng hàng kèm
  (recipe, phụ kiện, phụ kiện lắp đặt, phụ kiện sửa chữa), xe, nhóm dùng, ảnh/video.
- **Bị xoá/ép**: giá bán mọi ĐVT ép = **1 đ** (:1032-1036); tài liệu kỹ thuật **xoá trắng** (copy.blade.php:61).
- **Ảnh**: dùng lại URL cũ (không chép file S3).
- **Mã**: server tự sinh `<mã hãng>-<code đặt hàng|model>`, trùng thêm `:01`…
- **Trùng tên**: rule tên × model × thương hiệu × hãng ⇒ không đổi gì là lỗi trùng.
- **Nút**: menu dòng danh sách (status ∈ {1,2,5}), màn chi tiết (status 1), danh sách hàng gốc. Đã gỡ ở 2-D1 (09/10);
  route copy + `productStore` đang bị `productMovedToHrm` chặn 403 → link HRM `/master-data/products/create`.
- **Copy hàng gốc** (`ProductTemplatesController@copy`): giống hệt, vẫn POST `productStore` ⇒ ra 1 Product, không ra template.
- **Lịch sử**: không ghi gì riêng cho copy.
- **Bug ERP không được chép theo**: video gửi kèm `id` nguồn ⇒ `syncVideos` **chuyển** video khỏi hàng gốc sang hàng mới;
  object JS giữ `id` nguồn ⇒ người không có quyền "Quản lý giá" không thấy phần giá trên form copy.

## 2. HRM hiện có gì

- **Chưa có code sao chép** (BE lẫn FE).
- Hồ sơ cũ: G8 "Sao chép: làm sau" (`2c-ghi/chot.md:22,79`). Đề xuất `2c-ghi/yeu-cau-ghi.md:81-86`: quyền
  "Xây dựng thông tin hàng hoá", bản sao = bản ghi mới, mã mới, trạng thái Đang nhập thông tin tại công ty đang làm,
  FE mở `/products/create?copy_from=<id>`, không endpoint clone. **T9 (chép những gì) chưa chốt** (`yeu-cau-ghi.md:257`).
  `man-danh-muc-hang-hoa/plan.md:577-582` (task C4.3 cũ) lại ghi "nhân bản server-side + toàn bộ bảng con" ⇒ mâu thuẫn, phải chọn 1.
- **Luồng tạo**: `ProductListPage.vue:139` → `pages/master-data/products/create.vue` → `ProductForm mode=create`
  (`emptyForm` + `loadOptions`) → `POST products` (`M/Routes/api.php:545`, quyền "Xây dựng thông tin hàng hoá" +
  `dueConfig:Cập nhật hàng hóa`) → `ProductRequest` → `ProductWriteService::storeWithRetry` (:101-128):
  `products` (status 1, `company_id` = công ty đang làm, mã `ProductCodeGenerator`), ĐVT (giá vốn/mua 0) + bộ giá rỗng
  6 dòng/ĐVT cho công ty tạo, thuộc tính, 4 bảng hàng kèm, tài liệu kỹ thuật, ảnh, video, xe/nhóm máy/máy,
  tab Quản trị (`product_company_coefficients` status 1 + `info_entered_at = now()`, NCC, catalog theo công ty),
  lịch sử `ProductHistoryService::logCreate($id, $note)` (có sẵn tham số ghi chú).

## 3. Ràng buộc bản sao phải theo (luồng mới)

| Điểm | Hiện trạng HRM | Hệ quả cho Sao chép |
|---|---|---|
| Trạng thái | quy trình nằm ở `pcc.status` (1 nhập TT · 2 chờ tính giá · 3 Đang KD · 4 Ngừng · 5 Đang tính · 6-8 hàng tạm) | bản sao luôn pcc 1, không mang trạng thái gốc |
| Đã nhập thông tin | `writeAdmin` đặt `info_entered_at = now()` khi tạo | bản sao lưu xong đủ điều kiện "Chuyển KD không tính giá" ngay |
| Giá | tạo mới luôn bộ giá rỗng 0, `ProductRequest` không nhận giá | không chép giá (khác ERP ép 1 đ) — có giá qua YCHG→tính giá hoặc Chuyển KD không tính giá |
| Kế thừa giá theo hãng | chỉ áp khi `products.company_id ≠` công ty xét | bản sao do công ty mình làm chủ ⇒ không kế thừa ở công ty mình |
| Chủ hàng | `company_id` = công ty đang làm việc | sao chép hàng công ty khác ⇒ bản sao thuộc công ty mình |
| Mã | `ProductCodeGenerator`, chỉ ở đường tạo | giữ hãng/model ⇒ ra mã hậu tố `:NN` |
| Tên | duy nhất theo tên × model × thương hiệu × hãng (`ProductRequest.php:309`) | không đổi gì ⇒ 422 như ERP |
| Barcode (chuỗi) | không kiểm trùng | — |
| ĐVT / tài liệu | gửi `id` cũ ⇒ 422 "không thuộc hàng hoá này" | FE phải bỏ mọi `id` con |
| Tài liệu kỹ thuật | tệp không id **phải là URL tạm** (`ProductRequest.php:294-298`) | dùng lại đường dẫn cũ ⇒ 422 — phải bỏ / chép S3 sang tạm / nới luật |
| Ảnh | chỉ kiểm regex URL, tối đa 10; xoá hàng không xoá S3 | dùng chung URL an toàn; 28.569 hàng ERP chỉ có `avatar` ⇒ đưa avatar vào galleries kẻo mất ảnh |
| Hàng kèm | `checkKitStatus` chặn hàng đã xoá / tạm / đang khoá tại công ty | bản gốc giữ hàng kèm đã khoá ⇒ bản sao 422; FE lọc trước + báo |
| Nguồn điền sẵn | `GET products/{id}/edit` 403 nếu công ty chưa lấy về, 423 Ngừng KD, 422 hàng tạm | sao chép hàng công ty khác / đang khoá cần endpoint đọc riêng |
| Phân loại | `product_type_id` bắt buộc; cột cũ `group_id`/`product_cate` không nhận | hàng gốc chưa gán Loại SP ⇒ bản sao phải chọn |

## 4. Chỗ gắn

- Menu dòng `ProductListPage.vue` `rowActionsOf` (:1095-1136) sau "Sửa", `onRowAction` (:1143); cờ `can_copy`
  ở `ProductListResource.php:75-85` / `ProductDetailResource.php:46-54` theo khuôn `Product::editableAt`.
- Màn chi tiết `pages/master-data/products/_id/index.vue:56-80` `V2Footer #custom-actions`.
- Form: `create.vue` đọc `?copy_from=` → `ProductForm.init()` (:278) nhánh nạp nguồn, xoá id/code/owner/…,
  truyền id đã chọn vào `includeIdsOf` để ô chọn danh mục hiện đúng.

## 5. Câu cần chốt (hỏi lần lượt)

1. Cách làm: form điền sẵn (bám ERP + yeu-cau-ghi) hay nhân bản phía server (C4.3 cũ)?
2. Phạm vi nguồn: được sao chép hàng nào (của mình / công ty khác / đang khoá / Ngừng KD / hàng tạm / đã xoá)?
3. Chép những gì: tab Quản trị (NCC, catalog, hệ số), giá vốn/giá mua, tài liệu kỹ thuật (bỏ hay chép file), ảnh/video.
4. Vị trí nút: màn nào (Nhập thông tin / Đang KD / Dữ liệu công ty), có ở màn chi tiết không.
5. Lịch sử: ghi "Sao chép từ <mã>" ở bản mới? Có lưu cột nguồn (`copied_from_id`) không?
6. ERP: chỉ để chặn như hiện tại (link sang HRM) — hay cần gì thêm?
