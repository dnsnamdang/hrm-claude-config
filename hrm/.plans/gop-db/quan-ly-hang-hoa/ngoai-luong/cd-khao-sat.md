# Khảo sát đợt C-d — hàng hoá HRM (13/10/2026, chỉ đọc)

> Mục: N27 · N14 · N13 · N74 · N73 · N75 · N12/A8. HRM worktree `wt-chuyen-doi-hang-hoa` @api `5d109a505`.

| Mục | Hiện trạng chính | Hướng sửa | Cỡ |
|---|---|---|---|
| N27 | `ProductWriteService`: `assertOwner`/`assertCanEditAdmin` đọc model cũ + pcc không khoá, gọi TRƯỚC transaction (`updateAdmin` :258, `writeUpdate` :282); `take` (:181-188) đọc products/pcc không khoá; controller không bọc transaction | Trong transaction: `Product::lockForUpdate()->findOrFail` ⇒ khoá mọi pcc của hàng (thứ tự products → pcc như `ProductLifecycleService:317,321`, `TempProductService:69-72`) ⇒ kiểm lại; `take`: khoá theo id tăng dần, tự suy owner_status; mã lỗi giữ 404/403/423 | S |
| N14 | `ProductRequest:99-111` (+ `machine_ids.*` :136) `exists:products,id` không lọc; URL :79-84 chỉ string; `promoteTemporary` :472 để lại bản copy S3 khi rollback | `checkKitStatus` trong `withValidator`: xoá (`products.status<>1`) chặn mọi dòng; khoá (pcc=4) chặn dòng MỚI theo từng bảng (tập cũ pluck theo base_product_id); gom N+1 `checkKits`. Ảnh: regex `http(s)` hoặc `/uploads/` (1548/1548 ảnh cũ dạng `/uploads/...`); video `url`; `file_path` mới phải là URL tạm. S3: try/catch xoá bản promote khi lỗi (khuôn `MeetingService::deleteAttachmentFilesAfterCommit`) | S-M |
| N13 | Hàng 7338: 7.582 dòng đời xe / 125 model (14 hàng > 1000 dòng); BE ~7,7k query exists + 7.582 insert lẻ; FE 125 select2 × 61 option, `find`/mảng mới mỗi render, watch deep + JSON.stringify form | BE: rule bỏ exists từng phần tử ⇒ `checkVehicleLives` 2 query whereIn, lỗi đúng khoá; insert lô 1000. FE: Map tra dòng (giữ tham chiếu value); hiển thị (chờ chốt Q4); Playwright đo mở tab / lưu (ngưỡng < 1,5s) 7338 + 7578 | M |
| N74 | `TpProductUnitPrice::getBaseUnitIds` (mysql2 product_units); 3 chỗ báo giá đọc `mysql2.products` (avatar, guarantee): `QuotationController:1359`, `DetailQuotationResource:177`, `QuotationExcelExport:783`; `ProductProjectController:307` đã đọc DB mặc định (chỉ sai chú thích). Thêm 2 chỗ: `QuotationController:808` (price_types), `e2e_provision.php:145` (currencies) | DB mặc định; `AdminData::mediaAndGuarantee(ids, CompanyHelper::pricingCompanyId($quotation))` — pcc.guarantee của công ty báo giá, thiếu dòng lùi cột chung (luật `AdminData::source`) | S |
| N73 | `BorrowExportRequestTestDataSeeder:178-217` join pup không kẹp công ty | `ProductPriceSql::joinPrices(..., $this->info->company_id)`; sửa `price-readers.txt` | XS |
| N75 | `e2e_provision.php:60,145` mysql2; mã 3920 status 0 không pcc; spec `quotation-unit-select` gõ cứng Hộp/90,000/50,849 | DB mặc định; chọn hàng động (status 1, pcc cty 1 = 3, ĐVT phụ có giá); đưa vào `E2E_JSON`; spec đọc FX | S |
| N12/A8 | 5 spec chèn `roles.company_id` (catalog-popup-ui :356, take.api :201, lifecycle-ui :419, take-ui :447, lifecycle.api :381) | `utils/tempRoleFixture.ts` `createTempRole/dropTempRole` (khuôn `products-temp-ui.spec.ts:354-365`) | S |

## Tự chốt
- Q3 ảnh: chấp nhận `http(s)://` HOẶC `/uploads/...` (giữ dữ liệu ERP cũ lưu lại được).
- Q5: gom luôn 2 chỗ mysql2 ngoài danh sách (`price_types`, `currencies`) — đúng tinh thần "bỏ mysql2" (gop_db cấm mysql2).
- N14 áp cả `machine_ids.*` (Nhóm máy) + chặn hàng tạm của công ty khác như picker (cùng luật hàng kèm theo).

## Chốt (hỏi lần lượt)
| # | Câu | Đáp án (user 13/10) |
|---|---|---|
| C-d-1 | Khoá (pcc=4) xét ở công ty nào | ✅ **công ty đang làm việc** (= công ty tạo hàng chính trên đường ghi chung) |
| C-d-2 | Hàng kèm theo ĐÃ XOÁ nằm sẵn trong dòng cũ | ✅ **dòng cũ đã xoá thì GIỮ** — xoá cũng như khoá: chỉ chặn gắn MỚI (đổi chốt N14 trước "chặn mọi trường hợp") |
| C-d-3 | Bảng Đời xe theo model | ✅ **tóm tắt, bấm Sửa dòng mới mở ô chọn** — làm mockup duyệt trước |
