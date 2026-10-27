# Chuyển kinh doanh không tính giá — Design

> 23/10/2026 · @namdangit · nhánh `gop_db` (checkout chính hrm-api + hrm-client). Chốt Q1–Q8: `ton.md`.
> ⛔ Không phải lệnh code — code phải xin "làm" riêng kèm phạm vi.

## 1. Nghiệp vụ

Bỏ tính BẮT BUỘC của K1 / §29a-1 / Phase 7 Q1a ("mọi hàng phải qua YCHG → YCTG → PTG → KQ"). Ở màn
*Hàng hoá nhập thông tin*, người có quyền **Xây dựng thông tin hàng hoá** chọn **"Chuyển kinh doanh không tính giá"**
cho 1 hoặc nhiều hàng ⇒ hàng sang **Đang kinh doanh** tại công ty đang làm việc với bộ giá 0. Áp cho MỌI hàng
(tự tạo + lấy về — Q8). Luồng 4 chứng từ giữ nguyên, vẫn là đường chính để có giá.

### Điều kiện từng mã (BE xét, mã không đạt bỏ qua + báo lý do — khuôn `restore()`)
| # | Điều kiện | Câu báo khi bỏ qua |
|---|---|---|
| 1 | Hàng tồn tại, `products.status = 1` (không xoá ERP) | Hàng hoá không tồn tại / đã bị xoá ở ERP |
| 2 | `pcc.status = 1` tại công ty đang làm việc (Q6: 2/5 đang trong YCHG đã gửi ⇒ không) | Chỉ chuyển được hàng đang ở trạng thái Đang nhập thông tin. (2/5: "Hàng đang trong yêu cầu hỏi giá") |
| 3 | `pcc.info_entered_at` NOT NULL — "Đã nhập thông tin" (Q1) | Hàng chưa nhập thông tin, vui lòng Lưu thông tin hàng hoá trước |

Tối đa **100 mã / lượt** (Q5). Hàng chỉ nằm trong YCHG **nháp** (vẫn status 1) thì chuyển được; gửi YCHG sau đó vẫn hợp lệ
vì YCHG nhận hàng Đang KD (Q15 Phase 7).

### Kết quả mỗi mã đạt
1. `ProductPriceSetWriter::ensureProductSet(productId, companyId)` — bù dòng còn thiếu của bộ giá (6 loại × mọi ĐVT + `pcu`)
   giá 0. **Dòng đã có giữ nguyên giá trị** (bình thường đã 0 từ lúc tạo/lấy về — xem §4 điểm 1).
2. `pcc.status` 1 ⇒ 3, `updated_by/at`; giữ `coefficient`, `info_entered_at`.
3. Lịch sử hàng hoá: `ProductHistoryService::logStatus(id, company, 1, 3, 'change_status', 'Không bắt buộc tính giá')` (Q7).
   Không ghi lịch sử giá.
4. Không thông báo, không đổi gì của công ty khác, không migration, không quyền mới (Q2, Q4).

### Hệ quả sau chuyển (đã chấp nhận)
- Hàng hiện "Chưa có giá" (giá ≤ 1 đ) ở popup chọn hàng; Báo giá hỏi lại khi chọn (đợt gia-0).
- Muốn có giá: YCHG (nhận hàng Đang KD) hoặc màn Cập nhật giá bán (G4 sửa được hàng status 3).
- Chứng từ cần giá vốn công ty (hạch toán hỗ trợ, hiệu quả HĐ) bị chặn duyệt tới khi có giá vốn (P8, Q3).
- Công ty khác lấy về được hàng chủ đang KD giá 0 (L3 chỉ xét trạng thái); sàn giá B ≥ A bỏ qua khi giá A = 0.

## 2. BE (hrm-api)

| File | Thay đổi |
|---|---|
| `Modules/MasterData/Entities/Product/Product.php` | + `tradableWithoutPriceAt(?int $companyStatus, $infoEnteredAt): bool` — cờ NHẸ cho danh sách (status 1 + đã nhập thông tin + `products.status = 1`) |
| `Modules/MasterData/Services/Product/ProductLifecycleService.php` | + `tradeWithoutPrice(array $ids)`: kiểm rỗng / ≤ 100 (422), `DB::transaction` + `lockForUpdate` `products` + `pcc` như `restore()`; trả `{trading: [{id, code}], skipped: [{id, code, message}]}` (200 kể cả bỏ qua hết) |
| `Http/Controllers/V1/Product/ProductLifecycleController.php` | + `tradeWithoutPrice(Request)` |
| `Routes/api.php` | `POST products/trade-without-price` — `checkPermission:Xây dựng thông tin hàng hoá` + `dueConfig:Cập nhật hàng hóa` (như take/restore) |
| `Transformers/Product/ProductListResource.php` | + `can_trade_without_price` = `$canBuild && tradableWithoutPriceAt(...)` |
| `Tests/Feature/ProductTradeWithoutPriceApiTest.php` (mới) | xem §5 |

## 2b. Đổi luật khôi phục (Đ2, 23/10) — `hang-hoa-dang-khoa` K2/K3

`ProductRestoreRule` là MỘT nguồn luật cho cột "Khôi phục về", ô lọc, xuất Excel và `restore()` ⇒ sửa tại đó:
- `readySql()` = `(hàng khoá theo công ty) OR (luật cũ)`; "khoá theo công ty" = `products.status = 1` AND tồn tại dòng
  `pcc` công ty đang làm việc `status = 4`. Biểu thức cần bind company id 2 lần ⇒ thêm `readyBindings(int $companyId)`
  và đổi 3 chỗ gọi (`ProductService:100`, `:297`, `ProductLifecycleService:345`).
- `reasons()` trả `[]` cho hàng khoá theo công ty (cột không hiện lý do thiếu giá / phân loại).
- Hàng ERP đã xoá (kể cả có `pcc` 4): luật cũ — đủ 6 giá > 0 + Loại SP.
- Test: `ProductRestoreRuleTest` + `ProductRestoreApiTest` thêm ca (khoá theo công ty giá 0 ⇒ Đang KD; thiếu Loại SP ⇒ Đang KD;
  ERP xoá giá 0 ⇒ Đã nhập thông tin) + sửa ca cũ nào đang khẳng định "khoá theo công ty thiếu giá ⇒ Đã nhập thông tin".
- Ghi lại K2/K3 trong `hang-hoa-dang-khoa/design.md`.

## 3. FE (hrm-client)

| File | Thay đổi |
|---|---|
| `utils/product-list-screens.js` | màn `entering`: + cờ `tradeWithoutPrice: true` (+ dòng chú thích đầu file) |
| `components/product/ProductListPage.vue` | `canTradeWithoutPrice` = `screen.tradeWithoutPrice && canBuildProduct` (fail-closed) · menu dòng: mục **"Chuyển kinh doanh không tính giá"** (icon `ri-store-2-line`, theo `can_trade_without_price`) sau Sửa · thanh hàng loạt: nút cùng tên (primary sm, cạnh "Lập yêu cầu hỏi giá") · trước khi hỏi: lọc dòng tick có `can_trade_without_price`; 0 dòng ⇒ toast; > 100 ⇒ toast trần · `$confirm` → POST → toast kết quả + mã bỏ qua → bỏ tick → tải lại |
| `utils/productLifecycle.js` | + `tradeWithoutPrice(vm, rows, companyName)` cùng khuôn `restoreProducts` (câu hỏi + toast) |

Câu xác nhận: "Chuyển N hàng hoá sang Đang kinh doanh tại <công ty> mà không tính giá? Toàn bộ giá bán, giá vốn của
công ty sẽ là 0 (Chưa có giá)." Nút: **Chuyển** / **Huỷ**. Toast: "Đã chuyển N hàng hoá sang Đang kinh doanh" + danh sách
mã bỏ qua kèm lý do (như Lấy về).

Ô tick màn Nhập thông tin giữ luật hiện tại (`isRowSelectable` cho YCHG: status 1/3) — không đổi; nút hàng loạt chỉ gửi
dòng có cờ.

## 4. Điểm tự quyết — user soát

1. **Dòng giá đã có ≠ 0 giữ nguyên** (không ép về 0). Ca hiếm: hàng ERP cũ khôi phục về "Đã nhập thông tin" còn sót
   vài loại giá. Ép về 0 = xoá giá thật im lặng; giữ = đúng tinh thần "chỉ bù cái thiếu".
2. ~~Khoá rồi khôi phục về Đã nhập thông tin~~ ⇒ 🔄 **user đổi 23/10 (Đ2): hàng KHOÁ THEO CÔNG TY khôi phục LUÔN về
   Đang kinh doanh**, bỏ cả điều kiện giá (K2) lẫn Loại SP (K3) — về đúng trạng thái trước khoá (khoá chỉ từ 3). Hàng ERP
   đã xoá (`products.status = 0`, 17.596 mã local, 11.774 mã bộ giá toàn 0) GIỮ luật cũ. Xem §2b.
3. ~~Không thêm nút ở footer chi tiết~~ ⇒ 🔄 **user chốt 23/10 (lúc code): THÊM vào footer chi tiết** (CLAUDE.md: hành động chi tiết
   phải khớp danh sách) — cờ `can_trade_without_price` ở `ProductDetailResource`. Hệ quả: màn *Dữ liệu hàng hoá công ty* (cũng
   hiện hàng trạng thái 1) bật cùng action dòng + hàng loạt, để chi tiết mở từ màn nào cũng khớp dòng.
4. Thêm điều kiện **có ≥ 1 ĐVT** (bỏ qua "Hàng hoá chưa có đơn vị tính.") — hàng không ĐVT thì không có bộ giá.

## 5. Kiểm

- PHPUnit `ProductTradeWithoutPriceApiTest`: đạt (1 ⇒ 3, đủ 6 dòng giá 0 mỗi ĐVT, lịch sử 1 dòng đúng ghi chú) · chưa nhập
  thông tin ⇒ bỏ qua · status 2/5/3/4 ⇒ bỏ qua · hàng lấy về + hàng tự tạo · hàng ERP xoá ⇒ bỏ qua · > 100 ⇒ 422 ·
  không quyền "Xây dựng thông tin hàng hoá" ⇒ 403 · dòng giá có sẵn ≠ 0 giữ nguyên · công ty khác không đổi.
  Chạy lại `ProductLifecycleApiTest`, `ProductRestoreApiTest`, `ProductTakeApiTest`.
- Playwright MCP (đo DOM): menu dòng hiện đúng theo cờ · tick 2 hàng (1 đạt, 1 chưa nhập thông tin) ⇒ toast + mã bỏ qua ·
  hàng biến khỏi màn Nhập thông tin, hiện ở Đang kinh doanh · popup chọn hàng Báo giá hiện "Chưa có giá" · tài khoản
  không 1652 không thấy nút.
- e2e: thêm spec `HRM/e2e/tests/master-data/products-trade-without-price-ui.spec.ts` (có / không quyền) — chạy khi user yêu cầu.
