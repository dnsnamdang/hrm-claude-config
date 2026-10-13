# Plan đợt C-d — hàng hoá HRM (việc ngoài luồng) — 13/10/2026

> Nguồn: `cd-khao-sat.md` (khảo sát + chốt C-d-1…3). Mockup N13: `mockup-doi-xe.html`.
> ✅ User duyệt mockup + "làm" 13/10 (e2e: chưa trả lời ⇒ không tự chạy, chỉ sửa spec + Playwright MCP).
> HRM worktree `wt-chuyen-doi-hang-hoa` — api + client nhánh con `feat/cd-hang-hoa-hrm` từ `feat/chuyen-doi-hang-hoa`. DB `hrm_erp_giacty`.

## Task BE (hrm-api)
- [x] B1 N27 `ProductWriteService`: `writeUpdate` / `updateAdmin` — trong transaction khoá `products` (lockForUpdate, findOrFail) ⇒ khoá mọi pcc của hàng ⇒ `assertOwner` / `assertCanEditAdmin` trên dữ liệu mới; `$oldTypeId` đọc trong transaction. `take`: khoá products theo id tăng dần ⇒ pcc (product_id, company_id) ⇒ tự suy owner_status. Giữ mã 404/403/423.
- [x] B2 N14 `ProductRequest::withValidator` + `checkKitStatus`: 4 bảng hàng kèm theo + `machine_ids` — hàng ĐÃ XOÁ (`products.status<>1`) hoặc KHOÁ (pcc=4 tại công ty đang làm việc) hoặc hàng tạm công ty khác ⇒ chặn khi gắn MỚI; dòng đã gắn trước (tập cũ theo từng bảng) GIỮ (C-d-2). Gom N+1 `checkKits`. Ảnh: `http(s)://` hoặc `/uploads/`; video `url`; `file_path` dòng mới phải là URL tạm. S3: lỗi trong `store`/`writeUpdate` ⇒ xoá bản promote đã copy (khuôn `MeetingService::deleteAttachmentFilesAfterCommit`).
- [x] B3 N13 BE: rule `vehicle_lives.*` bỏ `exists` từng phần tử ⇒ `checkVehicleLives` 2 query whereIn, lỗi đúng khoá `vehicle_lives.i.life_ids.j`; `writeVehicleLives` insert lô 1000 (lọc trùng).
- [x] B4 N74: `TpProductUnitPrice::getBaseUnitIds` DB mặc định; `AdminData::mediaAndGuarantee(ids, companyId)` (pcc.guarantee của công ty báo giá, thiếu dòng lùi cột chung) dùng ở `QuotationController` exportExcel, `DetailQuotationResource`, `QuotationExcelExport`; `QuotationController:808` price_types DB mặc định; sửa chú thích `ProductProjectController:307,345`; `price-readers.txt` sửa lý do.
- [x] B5 N73 seeder BorrowExport kẹp công ty (`ProductPriceSql::joinPrices`).
- [x] B6 N75 `database/e2e_provision.php`: bỏ mysql2 (products, currencies); chọn hàng động (status 1, pcc cty 1 = 3, ĐVT phụ có giá) đưa vào E2E_JSON.
- [x] B7 PHPUnit: N27 (model cũ ⇒ 403/423; take pcc chủ 4 ⇒ skipped), N14 (mới/cũ × xoá/khoá × 4 bảng + Nhóm máy; ảnh `/uploads/` 200; video sai 422; file_path không tạm 422), N13 (id đời xe sai ⇒ 422 đúng khoá; 125×61 ⇒ 200, < 50 query), N74 (bảo hành theo công ty báo giá, lùi cột chung; getBaseUnitIds).

## Task FE (hrm-client)
- [x] F1 N13 `components/product/form/ProductFormVehicles.vue` theo mockup: cột Đời xe tóm tắt (chip "Tất cả N đời xe" / ≤ 6 chip + "+N" / "Chưa chọn đời xe"), cột Hành động `Sửa` + `Chọn tất cả` (dòng cũ: `Sửa` + `Xoá dòng`), 1 dòng sửa tại 1 lúc (mount `V2BaseSelect` chỉ dòng đó, nút `Xong`); ẩn nút khi "Áp dụng tất cả"; lỗi đỏ dưới tóm tắt; Map tra dòng (giữ tham chiếu `:value`).
- [x] F2 e2e: `e2e/tests/master-data/products-form-vehicles-ui.spec.ts` (mới) — hàng 7338: mở bước Xe < 1,5s, 125 dòng tóm tắt, Sửa 1 dòng → đổi → Xong → Lưu 1 PUT 200, DB 7.582 dòng; khoảng cách nút 12px; console sạch. Sửa spec `assign/quotation-unit-select.spec.ts` đọc FX (N75).
- [x] F3 N12/A8: `e2e/utils/tempRoleFixture.ts` `createTempRole/dropTempRole` + sửa 5 spec (catalog-popup-ui, take.api, lifecycle-ui, take-ui, lifecycle.api).

## Kiểm
- PHPUnit HRM MasterData + Assign liên quan cả bộ.
- Playwright MCP (3031/8031): form 7338 + 7578 đo trước/sau (mốc hiện tại: mở bước 2,2s sau tải, dòng 115px); popup chọn hàng kèm theo; bản in / xuất Excel báo giá có ảnh + bảo hành.
- e2e: chạy 5 spec A8 + spec đời xe mới + quotation-unit-select (`--workers=1`, `--no-deps`, BASE_URL 3031 / API_BASE 8031) — CHỈ khi user bảo (memory "không tự chạy e2e mỗi task") ⇒ xin cùng lần "làm".
- Checksum bảng hàng hoá liên quan trước/sau.

## Phạm vi xin "làm"
| | |
|---|---|
| Repo / nhánh | HRM worktree `wt-chuyen-doi-hang-hoa`: hrm-api + hrm-client nhánh `feat/cd-hang-hoa-hrm` từ `feat/chuyen-doi-hang-hoa`; merge LOCAL, push khi user báo. e2e (ngoài git) sửa trong `wt-chuyen-doi-hang-hoa/e2e` |
| File api | ProductWriteService, ProductRequest (+ Temp/PriceAskingTemp kế thừa), AdminData, TpProductUnitPrice, QuotationController, DetailQuotationResource, QuotationExcelExport, ProductProjectController (chú thích), BorrowExportRequestTestDataSeeder, database/e2e_provision.php, tests/fixtures/price-readers.txt, test mới |
| File client | components/product/form/ProductFormVehicles.vue (có thể thêm 1 component con tóm tắt) |
| DB | `hrm_erp_giacty`: chỉ đọc + dữ liệu thử trong transaction/tự dọn; không migration/seeder/quyền mới |

### Checkpoint — 2026-10-13 (wrap up 6)
Vừa hoàn thành: khảo sát, chốt C-d-1…3, mockup đời xe (đo style app thật; nút cách 12px, dòng 67px, không tràn 1440/390), plan.
Đang làm dở: không.
Bước tiếp theo: user duyệt mockup + "làm" (hỏi chạy e2e) ⇒ B1…B7, F1…F3.
Blocked: chờ user.

### Kết quả thực hiện — 2026-10-13
- Nhánh `feat/cd-hang-hoa-hrm` (api `71bf13e25`, client `3cdd83f9c`) — merge LOCAL nhánh chung `feat/chuyen-doi-hang-hoa`: api `72f350cd8`, client `baad69b58`. CHƯA push.
- Thêm ngoài plan (cùng tinh thần): `vehicle_model_ids.*` cũng bỏ `exists` từng phần tử (125 query) — gom vào `checkVehicleLives`; `writeLinks` chèn `productables` theo lô.
- Tự chốt: hàng tạm làm hàng kèm theo chặn theo ĐÚNG luật ô chọn `itemSearch` (pcc công ty chủ 6/7/8, mọi công ty) — plan ghi "công ty khác".
- PHPUnit: `ProductWriteHardeningTest` 11/11; MasterData cả bộ 470 (1 đỏ = danh sách trắng giá — đã gỡ dòng seeder, chạy lại xanh); Assign 18 (1 skip có sẵn). Sửa 2 fixture `ProductWriteApiTest` sang URL tạm (luật N14).
- Đo BE hàng 7338 (transaction, rollback): PUT nguyên form 200, 815ms, 100 query, 7.582 dòng (trước ~3,3s, ~15k query). Validate 409ms / 58 query.
- Playwright MCP 3031 hàng 7338: mở bước 2,3s → 0,8s; select2 125 → 0; chip 7.582 → 131; dòng 114px → 80px; nút cách 12px cùng hàng; Sửa ⇒ 1 select2, Xong ⇒ 0; Lưu (chặn PUT) 1 request mang 7.581 đời xe, lỗi BE hiện dưới tóm tắt đúng dòng; "Áp dụng tất cả" ẩn nút dòng thường, dòng cũ giữ Sửa/Xoá dòng; 390px không tràn trang. Console: chỉ 404 ảnh e2e (có sẵn).
- Báo giá: chi tiết BG-2026-00135 384 dòng ảnh / 336 bảo hành; xuất Excel BG theo BOM (#235) 200 có ảnh + bảo hành; `price-types` 200.
- e2e: (xem mục "e2e 13/10" bên dưới). Đã viết `tests/master-data/products-form-vehicles-ui.spec.ts` (V1–V5; V4 ghi thật, chọn hàng có Loại SP + catalog — DB dev hiện không có ⇒ skip), sửa `quotation-unit-select` đọc FX, `utils/tempRoleFixture.ts` + 5 spec; `--list` biên dịch đạt. Dry-run phần chọn hàng của provision: 3921 Cái/Hộp 60,000 / 31,482.

### Vấn đề ngoài luồng phát hiện (note, chưa sửa)
- N82 Xuất Excel báo giá KHÔNG theo BOM (VD BG-2026-00111) 400 `Undefined property $show_children` ở `exports/bom_list.blade.php` — có sẵn (trả controller về gốc vẫn lỗi y hệt).
- N83 Bấm × gỡ chip select2 nhiều lựa chọn không ăn trong Playwright (cả ô Hãng xe không sửa code) — cần kiểm tay xem user thật có gỡ được không.
- N84 `product_vehicle_model_has_life` không có index `product_id` (80k dòng) — DELETE khi lưu quét cả bảng, khoá rộng khi ghi song song.
- N85 Lỗi BE `galleries.N` (URL ảnh sai) không có chỗ hiện ở FE (chỉ `galleries`) — ảnh chỉ đến từ upload nên hiếm gặp.
- N86 Ô chọn hàng kèm theo (`item-search`) chưa lọc hàng đang khoá ở công ty đang làm việc — BE đã chặn 422, nhưng chọn xong mới báo.
- N87 `ProductFormVehicles` dòng "Đang tải danh mục xe..." dùng `.text-muted` (= đỏ trong hrm-client).
- Dữ liệu: hàng 7338 thiếu Loại SP + Tiểu mục catalog ⇒ Lưu form 422 (không do C-d).

### Checkpoint — 2026-10-13 (C-d xong)
Vừa hoàn thành: B1–B7, F1–F3 + kiểm (PHPUnit, Playwright MCP, đo BE 7338) — merge LOCAL nhánh chung.
Đang làm dở: không. Server 8031 / 3031 đang chạy.
Bước tiếp theo: (ĐÃ PUSH 13/10 api `bbc4cf8b2`, client `baad69b58`) · rồi C-c · C-e · C-f · A7; xem N82–N88.
Blocked: —

### e2e 13/10 (user: "chạy e2e trước")
- Worktree: `api.setup.ts` ghim `API_REPO` về checkout chính ⇒ provision chạy tay ở hrm-api worktree (DB giacty), tự ghi `.auth/{api,user,user-nocost}.json` cho 3031/8031, chạy `--no-deps --workers=1`.
- Lượt 1: 39 qua · 3 đỏ · 2 bỏ qua. 3 ca đỏ đều do GIẢ ĐỊNH CŨ của spec/fixture, không do code C-d:
  1. `quotation-unit-select` — giá vốn "—": role Super admin (18) KHÔNG có "Xem giá vốn hàng hoá" (cả hrm_erp lẫn giacty), provision ghim `$COST_PERM_ID = 1045` (nay là quyền khác; giá vốn = 1092) ⇒ sửa provision: tra theo tên, admin dùng role riêng "E2E Assign Admin" = quyền role 18 + giá vốn (api `bbc4cf8b2`).
  2. catalog-popup "màn Hàng đang kinh doanh không có ô tick" — ô tick là của T3 (Lập YCHG) ⇒ sửa ca: tick 1 dòng vẫn không có nút/popup catalog.
  3. catalog-popup "KHÔNG quyền" — role "E2E No Cost" chép quyền Super admin nay có 1653/1655 ⇒ đổi sang tài khoản NO_1652 + role tạm chỉ 1653.
- Lượt 2 (trọn 7 spec): 41 qua · 2 bỏ qua (V4 đời xe — DB dev không có hàng đủ Loại SP + catalog; 1 ca có sẵn) · 1 flaky: V1 đo 1.580ms > 1.500 lúc máy nguội vì gồm API lười `vehicle-options` ⇒ tách: vẽ bảng < 800ms + cả bước < 3s; lặp 3 lần không retry: 6/6 qua.
- Chưa xử lý: `api.setup.ts` ghim `API_REPO` checkout chính (chạy e2e cho worktree phải provision tay) — ghi ngoài luồng N88.
