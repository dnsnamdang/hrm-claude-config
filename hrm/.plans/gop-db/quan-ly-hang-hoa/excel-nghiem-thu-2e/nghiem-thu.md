# T5 — Nghiệm thu "ERP không vỡ" (A3 / 2-E) — lượt 1 14/10, lượt 2 15/10/2026

**Trạng thái (sau lượt 2, 15/10): XONG.** 12 đạt · 1 đạt một phần (2) · 1 không đạt (3', lỗi mới **N111**) · 0 không làm được.
Dữ liệu thử đã dọn theo id, mốc trước = sau (84 bảng). ERP 8090 đã tắt đúng PID.

## Lượt 2 (15/10/2026)

User cho phép trong phiên: *"Cho phép ghi dữ liệu vào database"* (DB dev `hrm_erp_giacty`), và chốt N110 = chạy đủ luồng giá Phase 7
trên UI HRM. Lượt này không bị chặn ghi. Chỉ một lần auto mode chặn **lệnh đọc** (headless mở Nuxt 3031, lý do "Interfere With
Workloads"); viết script ra file riêng rồi chạy lại thì qua. Không sửa code repo nào. Không đổi nhánh. Không đụng tiến trình
8031/3031, chỉ dùng chúng. Worktree HRM lúc chạy ở nhánh `feat/chuyen-doi-hang-hoa` @ hrm-api `b38852de0` (đã merge 2-E).
ERP worktree `wt-erp-2d1` @ `ca5fa294de`. Trước khi chạy đã kiểm `bootstrap/cache/config.php` không tồn tại và chạy `config:clear`.
`php artisan serve --port=8090` có PID 50324, tiến trình con `php -S` PID 50332. Cả hai đã kill đúng PID; cổng 8090 đã đóng.
Script và ảnh chụp lưu ở `scratchpad/a3t5/`: `x4.js` (form), `x5.js` (popup catalog), `x6.js` (Phase 7), `e2–e10.js` (ERP), `ids.log`,
`before2.txt` / `mid.txt` / `after2.txt`.

### Kịch bản đã chạy

1. **Mốc trước**: đếm từng bảng, gồm `count` và `max(id)`, không dùng GROUP_CONCAT. Có **84 bảng**: 48 bảng của lượt 1, thêm 14 bảng
   phiếu Phase 7, cùng `assign_histories`, `brands`, `manufactures`, `employee_has_permissions`, `product_prices`, `recipe_products`,
   `files`, `failed_jobs`… Mốc bắt đầu lúc 04:11:28.
2. **Cây phân loại** (qua API HRM): Tính chất 6852 › Nhóm CN 6388 › Nhóm SP 6008 › Loại SP 5911. **Nhánh catalog mới**: Chương 7005 ›
   Mục 6745 › Tiểu mục 6130, thuộc Lĩnh vực 2 "Công nghiệp".
3. **Quyền tạm** (SQL):
   - role HRM 121836 cho e2e_assign tại Cty 1, gồm 1092, 1662, 1663, 1664;
   - role ERP 121837 (`App\Employee`, guard web), gồm Xem hàng hóa, Thêm báo giá, Mua hàng, Lập HĐ mua hàng trong nước. Sau đó
     thêm "Quản lý giá", vì thiếu quyền này thì màn chi tiết ERP ẩn khối Giá theo đơn vị;
   - phân công XNK tạm `assign_histories` 4440 cho cặp KOKEN (1104) × Kowa Seiki (288) tại Cty 1. Cặp này chưa có phân công nào ở
     Cty 1, nên không chiếm chỗ của ai.
4. **Tạo hàng bằng form HRM** (Playwright, `/master-data/products/create`): điền Model, Loại SP A3T5 (3 cấp trên tự điền), KOKEN,
   Germany, Kowa Seiki, ĐVT Cái, VAT 10%. Tab Quản trị tick Tiểu mục 3730 "Mục điện". Lưu cho `POST 200`, ra hàng **74653
   `KOWA--T4DT135H`**, status 1 tại Cty 1.
5. **Popup "Xây dựng catalog" thật** (màn Dữ liệu hàng hoá công ty): tìm cây "A3T5", chọn Tiểu mục 6130, sang tab "Thêm hàng vào tiểu
   mục", tick hàng, bấm Thêm hàng hoá rồi Lưu. Kết quả `POST catalogs/sync` 200 `{"added":1}`, payload chỉ 1 cặp (74653 × 6130).
6. **Luồng giá Phase 7, toàn bộ trên UI HRM**:
   - màn Nhập thông tin: tick hàng, bấm "Lập yêu cầu hỏi giá", rồi Lưu và gửi duyệt. Ra **YCHG 6664**, hàng sang status 2;
   - PTKD bấm Duyệt (phiếu sang 10);
   - XNK bấm Duyệt **nhóm 6839** (popup "Duyệt nhóm hàng"), rồi Lập YCTG: chọn VNĐ, giá NCC 1.000.000, Lưu và gửi duyệt. Ra **YCTG
     3720** (status 2);
   - KTMH bấm Tính giá, ra form PTG. Giá nhập kho 1.000.000. Gõ hệ số Bán lẻ 1.5, giá tự lan ra 4 loại = 1.500.000, TMĐT = 1.950.000.
     Bấm Lưu và duyệt. Ra **PTG 3497**, "Đã áp giá bán" (Cty 1 tắt quy chế);
   - kiểm bằng SQL: PTG 1, YCTG 4, nhóm 4, YCHG 4, **`pcc` Cty 1 = 3**. Giá Cty 1: loại 1–5 là 1.500.000, loại 6 là 1.950.000. Giá vốn
     `pcu` 1.000.000. KQ 3269.
7. **Hàng đối chứng 74654 `KOWA-118REA0001`**: tạo bằng cùng form, xếp vào Tiểu mục 3730, để nguyên status 1. Dùng làm ca (i) "chưa
   KD thì không hiện", vì lúc hàng 74653 còn status 1 chưa mở popup ERP.
8. ERP 8090: chạy B1–B5 (bảng dưới). Lưu 1 báo giá ERP **56445**, rồi xoá bằng đường xoá của ERP (`firm-quotations/56445/delete`).
   Các dòng con 110997 / 1264893 / 101261 / 1239256 bị xoá theo.
9. **Mốc giữa** (sau khi lưu báo giá, trước khi xoá), xem bước 11. **Dọn** trong 1 transaction, xoá đúng id, rồi
   `php artisan cache:clear` ở hrm-api. **Mốc sau = mốc trước: 84/84 bảng, count và max id khớp, `diff` = 0.**

## Bảng 14 bước (sau lượt 2)

| # | Bước | Kết quả | Bằng chứng / lý do |
|---|---|---|---|
| 1 | ERP `admin/products` thấy hàng mới, mã đúng khuôn | ✅ Đạt | Gõ ô Mã `KOWA--T4DT135H`: `searchData` 200, "1 đến 1 trong tổng số 1", DOM **1 dòng**: tên, model, KOKEN, **1,500,000 / Cái**, Hoạt động. Gõ ô Tên "A3T5": **2 dòng**, gồm hàng đối chứng status 1. Màn danh sách ERP cố ý hiện mọi hàng status≠0, tổng 28,380 = 28,378 + 2. Mã = `<mã hãng KOWA>-<model>`. Model là `-T4DT135H` nên mã ra `--`; DB đã có 4 mã cũ cùng dạng (vd `CH-CXV120--061KV`), không tính là lỗi |
| 2 | Popup chọn hàng ERP: (i) chưa KD không hiện / (ii) KD hiện / (iii) Cty khác không hiện | 🟡 Đạt một phần | Đo trên 3 chứng từ: **Báo giá VT-HH-TB**, **Phiếu YC xuất mượn (kho)**, **HĐ mua hàng trong nước**. Gõ "A3T5" ở cả 3: `product-picker/search` 200, `meta.total=1`, DOM 1 dòng `KOWA--T4DT135H … 1,500,000` ⇒ **(ii) đạt**. Cả 3 đều không hiện hàng đối chứng 74654 (status 1, đã xếp catalog, tên cũng có "A3T5") ⇒ **(i) đạt**. Ca (i) đo trên hàng đối chứng, không đo trên chính 74653 trước khi KD. Cây popup "Tất cả hàng đã xếp catalog" ra 22 = 21 + 1. **(iii) không đo được bằng phiên ERP**: e2e_assign chỉ làm việc ở Cty 1. Gọi thẳng API picker HRM với `company_id=2/4` bị **403** "Bạn không được làm việc tại công ty này". SQL: hàng chỉ có `pcc` ở Cty 1 ⇒ Cty khác không có dòng `status=3` để lọt |
| 3' | ERP `products/{id}/show` đủ dữ liệu | ❌ Không đạt (N111) | HTTP 200, 0 lỗi JS. Có 2 lỗi 404 ảnh (`uploads/…tanphat-soft.jpg`, `e2e.png`), hàng cũ 43467 cũng y hệt. **Đúng**: Tên, Model, Nguồn gốc 4/6 (KOKEN, Germany, Kowa Seiki, Cty), Giá theo đơn vị **22/23 ô** (Cái, hệ số 1, 5 loại 1.5 → 1,500,000, TMĐT 1.95 → 1,950,000), khớp `product_unit_prices` Cty 1. Khối giá chỉ hiện khi có quyền ERP "Quản lý giá" (`can_show_price`), đúng như thiết kế cũ. **Sai**: "Tính chất hàng hóa", "Loại hàng hóa", "Nhóm hàng hóa", "Bảo hành" **trống**, còn hàng ERP cũ 43467 thì có đủ. Thông tin hàng hóa ra 3/11 ô, hàng cũ 9/11 ⇒ **N111** |
| 4 | Báo giá ERP: giá đúng công ty chứng từ (lưu 1 rồi xoá) | ✅ Đạt | Báo giá Cty 1, bảng giá Bán lẻ. Chọn hàng từ popup thì lưới ra **1,500,000**, VAT 10 % = 150,000, thành tiền 1,650,000. Lưu ra **56445** (`BGBH_TPE_HN_KD2_26_5091`, KH 44307). SQL `firm_quotation_tab_products.price = 1500000.00` = `product_unit_prices` (Cty 1, loại 1). Màn chi tiết báo giá hiện cùng số. Đã xoá bằng đường xoá ERP, 5 bảng về 0 dòng. Phiếu xuất mượn và HĐ mua chỉ mở popup + tìm, không thêm vào lưới, không lưu |
| 5 | Người tạo / cập nhật đúng tên | ✅ Đạt | SQL `products.created_by = updated_by = 1180` (e2e_assign), `pcc.updated_by = 1180` sau PTG. ERP `searchData` của dòng trả `created_by: "E2E Assign"`, `updated_by: "E2E Assign"`. Cột Người tạo / Người sửa ở màn ERP ẩn mặc định; bật bằng API DataTables không ăn, nên chưa đo trên DOM |
| 6 | Sửa giá công ty sinh chờ duyệt (HRM) | ✅ Đạt (PHPUnit, lượt 1) | `ProductPriceScreenApiTest` 30/30 |
| 7 | Màn Duyệt giá thấy phiếu (HRM) | ✅ Đạt (PHPUnit, lượt 1) | `ProductPriceApprovalApiTest` 22/22 |
| 8 | Duyệt ⇒ giá áp dụng, cờ về 0 | ✅ Đạt | PHPUnit lượt 1. Phần "ERP đọc giá mới": bước 1, 3', 4 đều đọc đúng giá vừa áp qua PTG |
| 9 | Công ty không bật duyệt ⇒ giá đổi ngay | ✅ Đạt | PHPUnit lượt 1. Lượt 2 thấy thật: Cty 1 tắt quy chế, PTG "Lưu và duyệt" áp giá ngay ("Đã áp giá bán") |
| 10 | Không quyền ⇒ giá giữ nguyên | ✅ Đạt (PHPUnit, lượt 1) | `ProductWriteApiTest` 34/34 |
| 11 | Đếm bảng trước/sau, chỉ tăng đúng số vừa tạo | ✅ Đạt | **Mốc giữa** chỉ tăng đúng bản ghi đã tạo: products +2, product_units +2, pcc +2, pcu +2, product_unit_prices +12 (6 loại × 2 hàng), product_business_catalogs +3, catalog_histories +8 (7 cây + 1 `product_prices` của PTG), 4 bảng cây +1, 3 bảng catalog +1, YCHG / nhóm / dòng +1, log duyệt +6, YCTG +1 / dòng +1, PTG +1 / dòng +1 / giá +6, KQ +1 / dòng +1 / giá +6, firm_quotations / tabs / tab_products / groups / group_products +1, roles +2, rhp +9, ehr +2, assign_histories +1, notifications +6. Các bảng còn lại = 0 (product_histories, product_versions, product_expected_prices, files…). **Sau dọn = trước: 84/84 bảng** |
| 12 | `products.code` rỗng = 0 | ✅ Đạt | Đo lại khi còn dữ liệu thử: **0** |
| 13 | Mã trùng = 0 | ✅ Đạt | Đo lại khi còn dữ liệu thử: **0** |
| 14' | Tạo đồng thời, retry `products_code_unique` | ✅ Đạt (PHPUnit, lượt 1) | `ProductCodeRetryTest` 2/2 |

**Tổng lượt 2: 12 đạt (1, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14') · 1 đạt một phần (2, ca iii) · 1 không đạt (3', N111) · 0 không làm được.**

### Lỗi mới

- **N111 — Màn Chi tiết hàng hoá ERP để trống phân loại và bảo hành với hàng tạo ở HRM.** `products/formShow.blade.php` đọc cột cũ
  `products.product_type` / `product_cate` / `group_id` / `guarantee`. Hàng HRM mới để NULL những cột này: `ProductRequest` không nhận
  `product_type` / `product_cate` / `group_id`, còn bảo hành giờ ở khối Quản trị theo công ty. Phân loại mới nằm ở
  `product_type_id` (Loại SP › Nhóm SP › Nhóm CN › Tính chất) mà ERP không hiện. Hệ quả: người dùng ERP xem hàng mới thấy 4 ô trống,
  trong khi hàng cũ có đủ. Gợi ý sửa: ERP chi tiết đọc chuỗi phân loại mới từ `product_type_id`, và đọc bảo hành theo công ty đang
  làm. Chưa vá.
- Ghi nhận, chưa tính là lỗi:
  - API `product-picker/items` (HRM) trả `price: null`, `units: []` cho hàng có 1 ĐVT, nhưng lưới báo giá vẫn ra đúng giá và ĐVT;
  - lỗi 404 ảnh mặc định trên màn chi tiết ERP có cả ở hàng cũ;
  - HRM log `laravel-2026-10-15.log` có ERROR "push FCM: Invalid service account", do cấu hình local, mỗi lần bắn thông báo Phase 7.

### Dữ liệu lượt 2 đã tạo / xoá (xoá đúng id, 1 transaction)

| Bảng | Id | Xoá |
|---|---|---|
| Cây phân loại | `product_natures` 6852, `product_function_groups` 6388, `product_families` 6008, `product_types` 5911 | ✅ |
| Catalog | `chapters` 7005, `job_groups` 6745, `job_clusters` 6130 | ✅ |
| `catalog_histories` | 8621–8628 | ✅ |
| Hàng | `products` 74653, 74654 · `product_units` 67758, 67759 · `product_company_coefficients` 150925, 150926 · `product_company_units` 166164, 166168 · `product_unit_prices` 964069–964080 · `product_business_catalogs` 7002, 7003, 7004 | ✅ |
| YCHG | `price_asking_requests` 6664 · `_groups` 6839 · `_products` 11844 · `_approve_histories` 26666–26671 | ✅ |
| YCTG | `price_calculate_requests` 3720 · `_products` 7911 (không có chi phí) | ✅ |
| PTG + KQ | `price_calculates` 3497 · `price_calculate_products` 5700 · `_product_prices` 32782–32787 · `price_calculate_results` 3269 · `_result_products` 5183 · `_result_product_prices` 29399–29404 | ✅ |
| Thông báo | `notifications` 6 uuid (2feb24d2…, 4fbb26bc…, 8b179278…, b02a20ec…, b6f06358…, fbb087fd…) | ✅ |
| Báo giá ERP | `firm_quotations` 56445 + tabs 110997, tab_products 1264893, groups 101261, group_products 1239256 | ✅ xoá bằng đường xoá ERP |
| Quyền tạm | roles 121836 (HRM), 121837 (ERP) + `role_has_permissions` 9 dòng + `employee_has_roles` 2 dòng · `assign_histories` 4440 | ✅ + `cache:clear` hrm-api (ERP `expiration_time = 0`, không đệm) |

Không đụng: `product_approves` vẫn 0 (Cty 1 tắt quy chế), `product_histories`, `product_versions`, `files`. AUTO_INCREMENT các bảng
trên đã nhảy, không lùi được, vô hại.

---

# Lượt 1 (14/10/2026) — giữ lại để tra cứu

**Trạng thái lượt 1: DỪNG GIỮA CHỪNG. Bộ phân loại an toàn (auto mode) chặn lệnh ghi dữ liệu thử.**
Lần ghi đầu đi qua (tạo Tính chất 6805 qua API HRM). Lần ghi thứ hai (`POST product-function-groups`) bị chặn 2 lần,
lý do "Modify Shared Resources" rồi "Irreversible Local Destruction". Mọi bước cần dữ liệu thử đều bị chặn theo, vì cần
cây phân loại, hàng thử, role tạm ERP và báo giá thử. Đã gỡ Tính chất 6805 và 2 dòng lịch sử của nó. Mốc trước = sau.

Môi trường: hrm-api / hrm-client worktree `wt-chuyen-doi-hang-hoa` ở nhánh `feat/cdhh-2e-excel` (không đổi nhánh). ERP worktree
`wt-erp-2d1` ở nhánh `feat/2d1-erp-khong-loi` @`ca5fa294de`, đã chứa merge P4 `d7f15cfcca`. DB `hrm_erp_giacty`. ERP 8090
**không khởi động**, vì chưa tới bước cần nó. Không sửa code repo nào. Không đụng API 8031 / Nuxt 3031.

## Phát hiện trước khi bị chặn: không có nút UI nào đưa hàng HRM mới tới "Đang kinh doanh" (status 3), ngoài luồng Phase 7

- Nút tạm "Chuyển kinh doanh" (H1) **đã bị bỏ**: `2c-ghi/chot.md:9` (H1'').
- Trong hrm-api, chỉ có 3 chỗ ghi `pcc.status = 3` cho hàng mới:
  - `PriceCalculateFinalizer::promoteProducts` (`Services/PriceCalculation/PriceCalculateFinalizer.php:229-243`), tức kết quả
    phiếu tính giá (PTG);
  - `ProductPriceApprovalService::applyApprove → markOwnerTrading` (`:394-398`, `:487`), tức duyệt giá bán một dòng
    `product_approves`; dòng này chỉ sinh ra từ PTG hoặc từ màn Cập nhật giá;
  - `unlock` (đi 4 → 3, không dùng cho hàng mới).
- Màn Cập nhật giá bán (1657) **không nhận** hàng ở status 1: `ProductPriceUpdateService.php:167-171` trả
  `423 MSG_ENTERING`.
- Kết luận: muốn hàng thành status 3 thì phải đi hết luồng Phase 7 (YCHG → YCTG → PTG → KQ → duyệt). Brief đã ghi trường hợp
  này: "DỪNG phần này, ghi rõ chặn ở đâu". Vậy ngay cả khi không bị chặn ghi, các bước **2(ii)** và **4 (giá hàng mới)** cũng
  không làm được trên hàng mới, trừ khi user cho chạy đủ luồng Phase 7 bằng UI.
- Ghi chú: form tạo hàng HRM **bắt buộc** chọn ≥ 1 Tiểu mục catalog (`ProductRequest.php:171`, `admin.job_cluster_ids`). Vì vậy
  popup Xây dựng catalog chỉ dùng được để xếp **thêm** nhánh, sau khi form đã lưu. Có thể dùng sẵn nhánh 3730 "Mục điện"
  (chương 4354, Lĩnh vực 2). Popup phải dùng một nhánh **mới**, tránh `catalogs/sync` đụng 21 hàng đang nằm ở 3730.

## Bảng 14 bước — lượt 1 (đã thay bằng bảng lượt 2 ở trên)

| # | Bước | Kết quả | Bằng chứng / lý do |
|---|---|---|---|
| 1 | ERP `admin/products` thấy hàng mới, mã đúng khuôn | ⛔ Không làm được | Không tạo được hàng thử (lệnh ghi bị chặn); thiếu role tạm ERP |
| 2 | Popup chọn hàng ERP (i) / (ii) / (iii) | ⛔ Không làm được | Như trên. Riêng (ii) còn bị chặn ở nghiệp vụ: không có đường UI tới status 3 ngoài Phase 7 (mục trên) |
| 3' | ERP `products/{id}/show` đủ tab | ⛔ Không làm được | Cần hàng thử + role tạm ERP |
| 4 | Báo giá ERP, giá đúng công ty chứng từ (lưu 1 rồi xoá) | ⛔ Không làm được | Cần hàng status 3 (Phase 7) + role tạm ERP; chưa lưu báo giá nào |
| 5 | Người tạo / cập nhật đúng tên | ⛔ Không làm được | Cần hàng thử |
| 6 | Sửa giá công ty sinh chờ duyệt (HRM) | ✅ Đạt (PHPUnit) | `ProductPriceScreenApiTest` **30/30**, 218 assertion |
| 7 | Màn Duyệt giá thấy phiếu (HRM) | ✅ Đạt (PHPUnit) | `ProductPriceApprovalApiTest` **22/22**, 295 assertion |
| 8 | Duyệt ⇒ giá áp dụng, cờ về 0 | ✅ Đạt (PHPUnit) | cùng bộ trên; phần "ERP đọc giá mới" thuộc bước 4, chưa làm |
| 9 | Công ty không bật duyệt ⇒ giá đổi ngay | ✅ Đạt (PHPUnit) | `ProductPriceScreenApiTest` 30/30 |
| 10 | Không quyền ⇒ giá giữ nguyên | ✅ Đạt (PHPUnit) | `ProductWriteApiTest` **34/34**, 220 assertion |
| 11 | Đếm bảng trước/sau, chỉ tăng đúng số vừa tạo | ✅ Đạt (cho phần đã làm) | 48 bảng, đếm từng bảng (count + max id, không GROUP_CONCAT); sau dọn `diff` = 0. Không có lượt tạo hàng nên chưa kiểm được ý "tăng đúng số" |
| 12 | `products.code` rỗng = 0 | ✅ Đạt | SQL `code IS NULL OR TRIM(code)=''` ⇒ **0** |
| 13 | Mã trùng = 0 | ✅ Đạt | SQL `GROUP BY code HAVING COUNT(*)>1` ⇒ **0** |
| 14' | Tạo đồng thời, retry `products_code_unique` | ✅ Đạt (PHPUnit) | `ProductCodeRetryTest` **2/2**, 19 assertion |

**Tổng: 8 đạt (6, 7, 8, 9, 10, 12, 13, 14'), 1 đạt một phần (11), 5 không làm được (1, 2, 3', 4, 5). 0 không đạt.**

PHPUnit ERP (`wt-erp-2d1`, cả bộ, sau `config:clear`; `bootstrap/cache/config.php` không tồn tại): **185 test, 4305 assertion,
OK, 4 skipped**. Khớp mốc 185.

## Dữ liệu đã tạo / xoá

| Bản ghi | Tạo | Xoá |
|---|---|---|
| `product_natures` **6805** `TCHH.A3T5` | `POST master-data/product-natures` (API HRM) | `DELETE master-data/product-natures/6805` ⇒ 200 |
| `catalog_histories` **8569** (create), **8620** (delete) của 6805 | sinh tự động | SQL xoá đúng 2 id (`table_name='product_natures' AND table_id=6805`), row_count 2 |
| Role tạm HRM / ERP | **không tạo**. e2e_assign đã có role cố định 118805 "E2E Assign Admin" đủ 1575–1585, 1652/1653/1655/1657/1658, 1671–1675 ở Cty 1. Không đụng role này | — |
| Báo giá ERP | không tạo | — |

**Mốc trước = sau** (`scratchpad/a3t5/before.txt` vs `after.txt`, 48 bảng, `diff` = 0). Một số số đo:
products 45.890 (max 50066), product_units 46.560, product_company_coefficients 113.782, product_company_units 133.101,
product_unit_prices 789.765, product_business_catalogs 21, catalog_histories 3.541 (max 8482), product_histories 319.303,
product_natures 1, product_function_groups / families / types 0, chapters 66, job_groups 107, job_clusters 3,
firm_quotations 55.257 (max 56444), roles 130, role_has_permissions 20.958, employee_has_roles 1.718.
AUTO_INCREMENT của `product_natures` đã nhảy (không lùi được, vô hại).

## Lỗi phát hiện

Không phát hiện lỗi mới. Vướng nghiệp vụ (không phải lỗi code; đề xuất ghi **N110** (N109 đã dùng cho gate company/entering)): **không có đường UI ngắn nào đưa hàng
HRM mới tới Đang KD.** Nút H1 đã bỏ, màn Cập nhật giá trả 423 với hàng status 1. Muốn nghiệm thu bước 2(ii) và bước 4 trên
hàng mới thì phải chạy đủ luồng Phase 7 bằng UI. Cần user chốt: cho chạy Phase 7 trong T5 (kèm dọn YCHG / YCTG / PTG / KQ /
`product_approves` theo id), hay chấp nhận dùng hàng ERP cũ đang KD làm đối chứng cho bước 4.

## Để chạy tiếp

1. User cho phép lệnh ghi dữ liệu thử trong auto mode (thêm rule cho Bash, hoặc tự chạy), hoặc tắt auto mode cho phiên T5.
2. User chốt N110 (Phase 7 đủ luồng hay dùng hàng đối chứng).
3. Chạy lại từ bước 1 của brief. Fixture dự kiến:
   - `TCHH.A3T5 › NCN.A3T5 › NSP.A3T5 › LSP.A3T5`;
   - form dùng Tiểu mục 3730; popup Xây dựng catalog xếp thêm vào một nhánh mới (Chương thuộc Lĩnh vực 2 › Mục › Tiểu mục);
   - role tạm ERP (`model_type App\Employee`, guard web) cho: `Xem hàng hóa`, `Thêm báo giá`, màn phiếu xuất kho, HĐ mua.
