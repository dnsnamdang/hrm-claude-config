# Đổi đơn vị tính ở màn Lập đơn mua hàng — Plan

Người phụ trách: @khoipv · Ngày tạo: 2026-09-14

## Yêu cầu
*"bây giờ màn lập đơn mua hàng tôi muốn cho được thay đổi đơn vị tính nữa, khi thay đổi đơn vị tính thì số lượng, đơn giá, thành tiền,.. tự cập nhật lại theo hệ số tương ứng"*

## Quyết định đã chốt với user (AskUserQuestion)
| Vấn đề | Chốt |
|---|---|
| Đơn giá khi đổi ĐVT | **Quy đổi giá, GIỮ NGUYÊN THÀNH TIỀN** (100 mL × 2.000 = 200.000 → 2 Hộp × 100.000 = 200.000) |
| SL đề xuất mua | **Quy đổi hết**: cả SL đề xuất và SL mua của từng phiếu |
| Số lẻ sau quy đổi | **Làm tròn tới 2 chữ số thập phân** |
| Danh sách ĐVT cho chọn | **Chỉ ĐVT đã khai hệ số của chính hàng đó** (`product_package_informations`) |

## Công thức
`conversion_factor` = hệ số so với ĐƠN VỊ CƠ BẢN (mL cơ bản = 1, Hộp = 50 → 1 Hộp = 50 mL).
Đổi từ ĐVT cũ **A** sang ĐVT mới **B**: `ratio = f(A) / f(B)`
- Số lượng: `qty_B = round2(qty_A × ratio)` — áp cho `order_qty`, `proposed_qty`, `purposes[].qty`, `purposes[].buyQty`
- Đơn giá: `price_B = round0(price_A / ratio)` — áp cho `price` và `purposes[].price` (VNĐ chẵn, DB là bigInteger)
- Thành tiền: KHÔNG lưu riêng ở FE, `amountOf()` tự tính lại từ giá × SL → tự đúng

## Khảo sát trước khi code (đã làm)
- `purchase_order_products` **đã có** `unit_id` + `unit_name`, `PurchaseOrderService::syncProducts()` đã lưu thẳng từ payload → **KHÔNG cần migration, không cần sửa service lưu**.
- Đã có helper dùng chung `SupplyProposalService::unitConversionMap($productIds)` trả `product_id => [main_unit_id, main_unit_name, main_factor, factors[unit_id => hệ số], names[]]`, đã lọc `deleted_at` → **dùng lại, KHÔNG sửa**.
- FE `ProductsTab.vue` giữ số liệu ở: `p.order_qty`, `p.proposed_qty`, `p.price`, và mỗi phần tử `p.purposes[]` có `qty` (SL đề xuất), `buyQty` (SL mua), `price` (đơn giá theo khách) → đổi ĐVT phải quét hết 6 chỗ này.
- ⚠️ Bẫy đã biết (memory `project_unit_factor_soft_deleted_trap`): `product_package_informations` xóa mềm khi sửa hàng hóa → **ĐVT hiện tại của dòng có thể không còn hệ số**. Khi đó: vẫn cho đổi ĐVT nhưng GIỮ NGUYÊN số và cảnh báo rõ trên màn, không âm thầm nhân sai.

## Task

### BE
- [x] `PurchaseOrderController::productUnits(Request)` — nhận `product_ids[]`, gọi `unitConversionMap()`, trả `{ pid: { main_unit_id, units: [{ id, name, factor }] } }` (sắp theo hệ số tăng dần).
- [x] Route `POST supply/purchase-orders/product-units` (đặt trước wildcard `/{purchaseOrder}`).

### FE (`hrm-thanhan-client/pages/supply/purchase_orders/components/ProductsTab.vue`)
- [x] `data.unitOptionsMap = {}` — key `product_id`.
- [x] `loadProductUnits()` gom `product_id` distinct → gọi API 1 lần → merge; gọi ở `created()` và trong `onAddLines()` (cùng chỗ với `loadProductRefs`).
- [x] Cột ĐVT: `readonly` → text như cũ; cho sửa → `base-select2` (đúng quy tắc dự án: không dùng select native). Hàng không có/1 ĐVT khai hệ số → vẫn hiện text, không cho chọn.
- [x] `onUnitChange(p, unitId)`: tính `ratio`, quy đổi 4 trường SL (round 2 chữ số) + 2 trường giá (round số nguyên), gán `unit_id`/`unit_name`, gọi `syncRowPrice(p)`.
- [x] Thiếu hệ số ĐVT cũ → chỉ đổi nhãn, giữ nguyên số, hiện cảnh báo.
- [x] Số cột giữ nguyên (19/20) — không đụng dòng TỔNG CỘNG.

### Verify
- [x] SSR render thật: cột ĐVT ra select khi sửa / ra text khi xem chi tiết; số cột không đổi.
- [x] Test hàm quy đổi: giữ nguyên thành tiền, nhiều khách nhiều phiếu, làm tròn 2 chữ số, thiếu hệ số.

## Checkpoint — 2026-09-14
Vừa hoàn thành: toàn bộ task BE + FE + Verify của feature đổi ĐVT.
- BE: `PurchaseOrderController::productUnits()` + route `POST supply/purchase-orders/product-units`, đã test bằng tinker trên dữ liệu thật (trả đúng map ĐVT + hệ số).
- FE: `ProductsTab.vue` — `unitOptionsMap`, `loadProductUnits()` (gọi ở `created()` và `onAddLines()`), ô ĐVT thành `base-select2` khi lập/sửa đơn và hàng có ≥2 ĐVT khai hệ số, 7 method `loadProductUnits/unitOptions/unitFactor/unitNameOf/cvtQty/cvtPrice/onUnitChange`.
- Verify: `scratchpad/render_unit.js` — **37/37 PASS** (giữ nguyên thành tiền 2 chiều, nhiều khách nhiều phiếu, làm tròn 2 chữ số, null giữ null, thiếu hệ số chỉ đổi nhãn + cảnh báo, select/text theo readonly, số cột 20/19 không đổi). Chạy lại 2 bộ cũ `render_tab.js` 45/45 và `render_del.js` 14/14 — không hồi quy.
Đang làm dở: (không)
Bước tiếp theo: user build lại client + hard refresh, BE chạy lại, test trên trình duyệt.
Blocked:

## Yêu cầu bổ sung 1 — nới rộng 2 ô nhập SL
*"cột sl mua bạn cho rộng ra giúp tôi 1 chút nữa, form input SL trong cột Mục đích mua (Phiếu đề xuất / KH / HĐ bán) nữa"*

Lý do: sau khi cho đổi ĐVT, SL có thể ra số lẻ tới 2 chữ số thập phân (VD `0.14`) — cộng thêm nút tăng/giảm của `input[type=number]` thì ô cũ cắt mất số.

- [x] `input.inp-oq` (cột **SL mua**): `min-width` 72px → **96px**
- [x] `input.pp-buy` (ô "Mua" trong cột **Mục đích mua**): `width` 52px → **72px**
- [x] Chỉ CSS, không đụng template/logic. `node-sass` compile sạch; 3 bộ verify chạy lại 37/37 + 45/45 + 14/14, không hồi quy.

## Yêu cầu bổ sung 2 — mất viền giữa 2 cột đông cứng khi cuộn ngang
*"hiện tại tôi thấy cột mã hàng, tên hàng hóa khi tôi kéo scroll ngang sang thì nó đang bị mất border giữa 2 cột"*

Nguyên nhân: bảng dùng `border-collapse` → viền phải của một ô thực chất là viền trái của ô bên cạnh. Khi cuộn ngang, ô bên cạnh trôi xuống DƯỚI cột sticky nên vạch ngăn biến mất. Cột thứ 3 (`.col-freeze-last`) đã xử lý từ trước bằng inset shadow, 2 cột đầu thì chưa.

- [x] Thêm `box-shadow: inset -1px 0 0 0 ...` cho `.col-stt` và `.col-code` (th dùng `#d9e2e0`, td dùng `#e3e8ee` — đúng màu border sẵn có của bảng).
- [x] Chỉ CSS. `node-sass` compile sạch, 3 bộ verify 45/45 + 37/37 + 14/14 không hồi quy.

## Yêu cầu bổ sung 3 — đồng bộ font chữ trong bảng
*"tôi thấy font chữ của cột mã hàng đang khác thì phải, cả tên thương mại dưới tên hàng hóa nữa"*

- [x] `.cell-code` (cột **Mã hàng**): bỏ `font-family: monospace` và `font-size: 11px` → dùng đúng font/cỡ chữ của bảng (12px). Giữ `white-space: nowrap`.
- [x] `.cell-name .sub` (**tên thương mại** dưới tên hàng hóa): bỏ `font-size: 10.5px` → cùng cỡ với tên hàng hóa, chỉ giữ **màu xám** `#8a97a3` để phân biệt phụ/chính.
- [x] Chỉ CSS. `node-sass` compile sạch (không còn `monospace`), 3 bộ verify 45/45 + 37/37 + 14/14 không hồi quy.

## Yêu cầu bổ sung 4 — làm tròn SL 2 chữ số + cuộn dọc trong bảng, cố định tiêu đề
*"hiện tại các cột SL bạn làm tròn đến chữ số thập phân thứ 2 sau dấu phẩy cho tôi thôi, và thêm scoll trong bảng cho tôi nữa, cố định tiêu đề bảng lại ấy"*

### 4a. Làm tròn 2 chữ số ở mọi cột SL
Cột DB là `decimal(15,3)` nên đơn cũ có thể mang sẵn 3 chữ số. Chuẩn hóa **DỮ LIỆU** chứ không chỉ hiển thị, để con số nhìn thấy luôn đúng bằng con số sẽ lưu (nếu chỉ làm tròn lúc hiển thị thì màn hiện `0,33` mà vẫn gửi `0.333` lên BE).

- [x] Thêm `round2(v)` và `fmtQty(v)` — tách riêng khỏi `fmtN` vì `fmtN` còn dùng cho **TIỀN** (VNĐ chẵn, không được hiện phần thập phân) và cột tham chiếu.
- [x] Đổi 4 chỗ hiển thị SL sang `fmtQty`: badge "ĐX" trong cột Mục đích mua, ô SL đề xuất mua (cột gộp), 2 ô dòng TỔNG CỘNG.
- [x] `:value` của 2 input (`inp-oq`, `pp-buy`) bọc `round2()`.
- [x] 2 handler `onOrderQtyInput` / `onBuyQtyInput` cắt về 2 chữ số ngay khi gõ.
- [x] `normalizeQty()` quét `order_qty`, `proposed_qty`, `purposes[].qty`, `purposes[].buyQty` — **null/rỗng giữ nguyên**, không biến thành 0.
- [x] Gọi qua `watch.products { immediate: true }` chứ không chỉ `created()`: `PurchaseOrderForm` fetch chi tiết xong mới **gán lại** mảng `products` (sau khi tab đã mount).

### 4b. Cuộn trong bảng + cố định tiêu đề
- [x] `.table-responsive`: `max-height: calc(100vh - 320px)`, `min-height: 240px`, `overflow-y: auto` → cuộn dọc ngay trong bảng, `thead` sticky bám đầu vùng cuộn. Dropdown `base-select2` render vào `.products-tab` (ngoài khối cuộn) và popup lịch `vue2-datepicker` render vào body → không bị `overflow` cắt.
- [x] `thead.thead-sticky th`: thêm `box-shadow: inset 0 -1px 0 0 #d9e2e0` — cuộn dọc thì viền dưới hàng tiêu đề cũng mất (cùng bẫy `border-collapse` với yêu cầu bổ sung 2), vẽ lại bằng inset shadow.
- [x] `thead.thead-sticky th.col-freeze-last`: giữ đủ 3 lớp bóng (vạch phải + viền dưới thead + bóng đổ sang phần cuộn).

### Verify
- [x] `scratchpad/render_round2.js` — **23/23 PASS**: round2/fmtQty (fmtN cho tiền không đổi), normalizeQty cắt 3 chữ số từ BE, null giữ null, gõ tay bị cắt còn 2 chữ số, SSR render thật mọi ô SL ≤ 2 chữ số thập phân.
- [x] `node-sass` compile sạch, có đủ `max-height/min-height/overflow-y` + inset shadow thead.
- [x] Chạy lại 3 bộ cũ: `render_tab.js` 45/45, `render_unit.js` 37/37, `render_del.js` 14/14 — không hồi quy.

### 4c. Nới thêm chiều cao vùng cuộn
*"cho bảng thêm height nữa ra cho tôi"*

- [x] `.table-responsive`: `max-height` `calc(100vh - 320px)` → **`calc(100vh - 210px)`**, `min-height` 240px → **360px**. Chỉ CSS, `node-sass` compile sạch.

---

## Bug 1 — Đổi ĐVT ngược không trả lại đúng SL gốc (16/09/2026)

*"chọn hàng Thuốc thử xét nghiệm α-Amylase 557-048 số lượng nó lại ra lẻ 5.56 và 1.11 … tôi đổi về mL thì nó ra 1000.8 mà trong phiếu xử lý là 1000 mL"*

### Nguyên nhân gốc (đã kiểm chứng bằng DB)
Hàng `HC-SH-047 / 557-048`: ĐVT chính = **Hộp**, `product_package_informations` (id 27167–27169) khai **mL = 1, Hộp = 180, Test = 0.25**.

**Tầng 1 — vì sao ra số lẻ (ĐÚNG THEO THIẾT KẾ, user xác nhận giữ nguyên):**
`SupplyReportService::buildUnitPlans()` — 1 mã được đề xuất ở ≥2 ĐVT giữa các PXL → báo cáo quy hết về ĐVT chính. PXL ghi mL nên `1000 / 180 = 5,5555…` → 5,56 Hộp; `200 / 180 = 1,1111…` → 1,11 Hộp. Popup chọn hàng của DMH nạp `lines[].quantity` (số ĐÃ quy đổi) + ĐVT của khối.

**Tầng 2 — LỖI THẬT:** `ProductsTab.round2()` cắt 5,5555 → **5,56 rồi lưu luôn vào dữ liệu** (`normalizeQty`, yêu cầu bổ sung 4a). Khi đổi ĐVT, `cvtQty` nhân từ số **đã bị làm tròn**: `5,56 × 180 = 1000,8`. Làm tròn 2 lần → sai số tích lũy. Sau khi lưu còn tệ hơn: DB `decimal(15,3)` giữ 5,556 → `× 180 = 1000,08`.

### Chốt với user
| Vấn đề | Chốt |
|---|---|
| Quy đổi về ĐVT chính (5,56 Hộp) | **Giữ nguyên** — "5.56 hộp thì là đúng rồi" |
| Đổi ngược về mL | **Phải ra đúng 1000 mL** |
| Số chính thức hiển thị/lưu | **Vẫn round2** (không đổi luật cũ) |
| Phạm vi | Chỉ màn DMH — **KHÔNG đụng** `buildUnitPlans()` (hàm dùng chung) |

### Cách sửa — neo mốc gốc `*_base` (SL quy về ĐVT CƠ BẢN)
Mỗi chỗ giữ SL mang thêm 1 mốc gốc tính theo ĐVT cơ bản, **không bao giờ làm tròn**. Đổi ĐVT = `round2(base / f(ĐVT mới))` tính từ mốc, KHÔNG nhân chuỗi từ giá trị đang hiện → không tích lũy sai số, đổi qua lại bao nhiêu lần cũng trả đúng số gốc.
- Mốc chuẩn nhất lấy từ **`raw_quantity` + `raw_unit_id`** của từng dòng PXL (BE `goods-pool` đã trả sẵn, FE chưa map) → `base = raw_quantity × f(raw_unit)`; với 1000 mL thì `base = 1000`, đổi về mL ra **đúng 1000**.
- User gõ tay SL → neo lại mốc theo số vừa gõ: `base = qty × f(ĐVT hiện tại)`.
- Thiếu hệ số (`product_package_informations` xóa mềm) → `base = null`, giữ nguyên hành vi cũ (chỉ đổi nhãn + cảnh báo).
- Phải lưu xuống DB, nếu không thì mở đơn đã lưu rồi đổi ĐVT vẫn lệch (1000,08).

### Task

#### BE
- [x] Migration `add_qty_base_to_purchase_order_products_table`: thêm `order_qty_base`, `proposed_qty_base` `decimal(20,6)` nullable (không FK, không index — chỉ để đọc kèm dòng).
- [x] `PurchaseOrderService::syncProducts()` — lưu 2 cột mới từ payload (null nếu không có).
- [x] `DetailPurchaseOrderResource` — trả `order_qty_base` / `proposed_qty_base` về FE.
- [x] `purposes` JSON thêm `qtyBase` / `buyQtyBase`: không cần sửa BE (`$request->input('products')` là input thô, `json_encode` nguyên object).

#### FE
- [x] `GoodsPickerModal.buildCandidates()` — map `rawQty` (`l.raw_quantity`) + `rawUnitId` (`l.raw_unit_id`) vào mỗi phần tử `purposes[]`.
- [x] `ProductsTab` helper: `baseOf(p, unitId, val)` (val × hệ số), `fromBase(p, unitId, base)` (round2(base / hệ số)), `ensureBases(p)` (tính mốc từ rawQty/rawUnitId, fallback từ giá trị hiện tại).
- [x] `onUnitChange()` — quy đổi 4 trường SL **từ mốc** thay vì nhân `ratio`; mốc giữ nguyên. Giá vẫn theo `cvtPrice` cũ.
- [x] `onOrderQtyInput` / `onBuyQtyInput` — neo lại mốc theo số user gõ.
- [x] `mergeLine()` — cộng dồn mốc cùng lúc với `proposed_qty` / `order_qty`.
- [x] `normalizeQty()` — chỉ làm tròn số hiển thị, **không đụng** `*_base`.

#### Verify
- [x] Bộ test round-trip: 1000 mL → 5,56 Hộp → mL = **1000** (không phải 1000,8); qua Test (0.25) rồi về mL vẫn đúng; đổi 3 lần liên tiếp không trôi số.
- [x] Gõ tay SL rồi đổi ĐVT → quy đổi theo số vừa gõ.
- [x] Thiếu hệ số → giữ nguyên số + cảnh báo (không hồi quy).
- [x] Chạy lại 4 bộ cũ: `render_tab.js` 45/45, `render_unit.js` 37/37, `render_del.js` 14/14, `render_round2.js` 23/23.

### Checkpoint — 2026-09-16
Vừa hoàn thành: toàn bộ task BE + FE + Verify của Bug 1 (đổi ĐVT ngược ra sai số).
- BE: migration `2026_09_16_000001_add_qty_base_to_purchase_order_products_table` (đã chạy trên `thanhan_stag_07052026`), `PurchaseOrderService::syncProducts()` + helper `nullableFloat()`, `DetailPurchaseOrderResource` trả 2 cột mốc.
- FE: `GoodsPickerModal.buildCandidates()` map `rawQty`/`rawUnitId`; `ProductsTab` thêm `toBase/fromBase/sumBase/ensureBases/reanchor`, `onUnitChange` quy đổi từ mốc, `onOrderQtyInput`/`onBuyQtyInput` neo lại mốc, `mergeLine` cộng mốc, `loadProductUnits()` chốt mốc ngay khi hệ số về (bịt kẽ hở "thêm hàng rồi lưu luôn").
- Verify: `scratchpad/verify_qty_base.js` **35/35 PASS** (trích thẳng khối `methods` của file .vue, không chép lại logic) + `scratchpad/verify_be_base.php` **10/10 PASS** (tinker, transaction rollback). `vue-template-compiler` parse sạch 2 file.
Đang làm dở: (không)
Bước tiếp theo: user build lại client + hard refresh, test trên dev với hàng `557-048` (1000 mL → 5,56 Hộp → đổi về mL phải ra đúng 1000).
Blocked:

## Bug 1b — Đơn giá cũng sai khi đổi ĐVT qua lại (16/09/2026)

User: *"có chứ, sửa cả giá đi"* → xử lý nốt đơn giá theo đúng cách đã neo mốc cho SL.

**Nguyên nhân:** `price` lưu VNĐ chẵn (DB `bigInteger`), `cvtPrice` lại `Math.round` sau mỗi lần đổi ĐVT. ĐVT nhỏ thì phần lẻ mất hẳn: 100đ/Hộp → 0,55đ/mL → làm tròn **1đ** → đổi về Hộp ra **180đ** (sai 80%).

**Cách sửa:** thêm mốc `price_base` = tiền trên **1 ĐVT cơ bản**, không làm tròn. Ngược chiều SL: quy về mốc thì **chia** hệ số, đổi ra ĐVT thì **nhân** rồi mới làm tròn → thành tiền không đổi, đổi qua lại bao nhiêu lần vẫn trả đúng số gốc.

### BE
- [x] Migration `2026_09_16_000002_add_price_base_to_purchase_order_products_table` — cột `price_base` decimal(20,6) nullable (đã chạy trên `thanhan_stag_07052026`).
- [x] `PurchaseOrderService::syncProducts()` — lưu `price_base` qua `nullableFloat()`.
- [x] `DetailPurchaseOrderResource` — trả `price_base` (null giữ null).
- [x] Mốc trong `purposes[]` (`priceBase`) đi theo JSON, không cần cột riêng.

### FE — `ProductsTab.vue`
- [x] `toBasePrice()` / `fromBasePrice()` — chia/nhân hệ số (ngược chiều `toBase`/`fromBase`).
- [x] `reanchorPrice()` — neo lại mốc khi người dùng gõ giá; key `price_base` ở cấp dòng, `priceBase` trong `purposes[]`.
- [x] `onUnitChange()` — thêm `priceFor()`, tính giá lại từ mốc; chưa có mốc thì rơi về `cvtPrice` cũ.
- [x] `ensureBases()` — vật chất hóa cả mốc giá (dòng + từng phiếu).
- [x] `onPriceInput` / `onCustomerPriceInput` — neo lại mốc theo số vừa gõ.
- [x] `fillPurposePrices` — điền `priceBase`, ưu tiên mốc cấp dòng (chưa làm tròn) hơn số hiển thị.
- [x] `syncRowPrice` — mốc giá cấp dòng = bình quân gia quyền **theo mốc**, không suy ngược từ `p.price` đã làm tròn.

### Verify
- [x] `scratchpad/verify_qty_base.js` — thêm 8 nhóm ca giá (12–19) → **52/52 PASS** toàn bộ.
  - 100đ/Hộp → mL → Hộp ra đúng **100đ** (code cũ ra 180đ — có ca hồi quy chứng minh).
  - 7đ/Hộp qua Test → mL → Hộp vẫn 7đ (đổi vòng nhiều ĐVT không trôi).
  - Giá theo từng khách (nhiều phiếu) về đúng 100đ / 250đ.
  - Gõ tay 3đ/mL → về Hộp ra 540đ (theo số vừa gõ, không phải mốc cũ).
  - Thiếu hệ số → giữ nguyên giá + cảnh báo.
  - Đơn cũ không có mốc → hành vi cũ, không vỡ.
  - Đơn đã lưu đọc `price_base` từ DB → quay lại đúng 100đ.
- [x] `scratchpad/verify_be_base.php` — thêm 4 ca `price_base` → **14/14 PASS** (tinker, transaction rollback).
- [x] `vue-template-compiler` parse sạch `ProductsTab.vue`.

### Checkpoint — 2026-09-16 (lần 2)
Vừa hoàn thành: Bug 1b — neo mốc đơn giá (`price_base`), BE + FE + verify.
Đang làm dở: (không)
Bước tiếp theo: trên dev chạy **`php artisan migrate`** (2 migration `2026_09_16_000001` và `2026_09_16_000002`), build lại client + hard refresh; test hàng `557-048`: 1000 mL → 5,56 Hộp, đổi về mL phải ra đúng 1000 và giá phải quay đúng số cũ.
Blocked:

