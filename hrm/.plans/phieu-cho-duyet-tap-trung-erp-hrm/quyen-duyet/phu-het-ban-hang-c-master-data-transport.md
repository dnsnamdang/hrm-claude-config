# Phủ hết màn duyệt — nhóm C: MasterData + Transport — @cuong61n

Ngày 17/11/2026. Fork C của nhóm Bán hàng/CSKH/Vận chuyển/Danh mục. Phạm vi: `Modules/MasterData`, `Modules/Transport` (FE `pages/master-data`, `pages/sale/price-*`, `pages/transport`). Manifest dữ liệu thử: `wave2-sale-c.json` (đã `clean-test`, không còn dòng thử). Không chạy migration.

## 1. Kết quả đăng ký

| doc_type | Cấp | Màn (chi tiết) | Gate (BE chốt — không "điều kiện giao diện") |
|---|---|---|---|
| `other_delivery_trip` (SỬA, version 1→2) | 1 Chờ duyệt (status 5) · **2 Chờ hạch toán (status 1, mới)** | `/transport/other-delivery-trips/{id}` | Cấp 2 = đường `deny` (OtherDeliveryTripController.php:280 → withViewable → `canDeny` OtherDeliveryTrip.php:248 = status 1 + quyền "Hạch toán chuyến xe khác" `warehouse.hach_toan_chuyen_xe_khac.create`) + Thủ kho + `canView` (cùng luật cấp 1). Kết thúc cấp 2: ERP tạo phiếu hạch toán (7/3) ⇒ ĐÃ DUYỆT; Không duyệt (6) ⇒ TỪ CHỐI |
| `delivery_trip` (MỚI) | 1 Chờ hạch toán (status 1) | `/transport/delivery-trips/{id}` | DeliveryTripController.php:271 `deny` → `run` (Thủ kho) → `withViewable` (status 1 ai cũng xem) → `canDeny` = `canAccounting` DeliveryTrip.php:297 (status 1 + `warehouse.hach_toan_chuyen_xe_cho_hang.create` + công ty GỐC = công ty phiếu) |
| `price_calculate_request` (MỚI) | 1 Chờ tính giá (status 2) | `/sale/price-calculate-requests/{id}` | PriceCalculateRequestController::reject → Writer::reject:138 → `assertWritable` (thấy phiếu: người lập hoặc `sale.yeu_cau_tinh_gia_ban.view`, cấp phòng ban = phòng NGỒI) + `canReject` PriceCalculateRequestAccess.php:147 (status 2 + công ty phiếu = công ty đang làm + `finance.phieu_tinh_gia.create` + nhóm chưa đóng; nhóm đóng ⇒ `approvable=false`) |

Đã đọc lại, KHÔNG sửa: `price_asking_request`, `price_asking_group`, `product_price_approval` (đợt 1) — đối chiếu code thấy đủ cấp: YCHG chỉ có 1 cấp chờ (status 2; status 1/5/7 là hiển thị "Đang hỏi giá"); nhóm có 1 cấp chờ XNK (status 5, gồm Duyệt + "Báo không có giá"); status 1 của nhóm ("Chờ lập YCTG") chỉ có Huỷ duyệt của chính XNK + Lập YCTG (hàng đợi công việc, `PriceAskingAccess::groupActions` :158). `product_price_approval` verify 0 chênh lệch. Delivery_contract / delivery_cost_summary đợt 1 giữ nguyên.

## 2. Luồng KHÔNG đăng ký riêng (kèm bằng chứng)

| Luồng | Quyết định | Bằng chứng |
|---|---|---|
| M2 Hàng tạm trong YCHG (PTKD Đồng ý / Không duyệt từng hàng tạm; màn `/sale/price-asking-requests/{id}/temp/{productId}`) | GỘP vào `price_asking_request`, không tạo loại riêng | `assertTempGate` PriceAskingRequestWriter.php:521 = `assertWritable` + `hasPtkd` + phiếu `STATUS_WAITING_PTKD` ≡ đúng `truth()` của YCHG (cùng tập người). Hàng tạm chỉ quyết được khi YCHG đang Chờ PTKD, và `ptkdApprove` chặn Duyệt phiếu nếu còn hàng tạm (:704-708) ⇒ mọi lúc có hàng tạm chờ thì đã có 1 item YCHG đúng người. Tách riêng sẽ sinh item trùng người trùng phiếu. **Điểm user quyết nếu muốn 1 dòng/ hàng tạm** (cần trait trên `product_company_coefficients` + hook ở `setTempStatus`/`moveProducts`/TempProductService, ~6 chỗ query builder) |
| PL01 `line-decisions` (duyệt từng dòng hàng "Đang nhập thông tin") | Không đăng ký | `lineDecide` Writer.php:612: chỉ LƯU quyết định (bảng quyết định, không đổi trạng thái hàng) — "trạng thái hàng đổi lúc PTKD Duyệt phiếu". Là checklist trong phiếu YCHG, cùng gate PTKD. Đăng ký sẽ sinh N item/phiếu |
| Menu "YC duyệt hàng tạm" | Chỉ là chuỗi trần, không có link | `sale-hub.js:165` — chưa có màn HRM riêng; duyệt hàng tạm đi qua YCHG |
| PTG (`price_calculates`, "Chờ duyệt giá" 5) và YCTG status 6 | Không đăng ký riêng | PTG không có nút duyệt: `PriceCalculateAccess` chỉ có canEdit/canDelete/canCalculate (:111-123); "Chờ duyệt giá" do `PriceCalculateFinalizer::settle` :117-133 đặt khi còn dòng `approval_status` chờ — người duyệt xử lý ở màn Duyệt giá bán hàng hoá ⇒ đã phủ bằng `product_price_approval` |
| `ProductExpectedPrice` status 2 (giá hiệu lực chờ tới ngày) / `regulation_scheduled_versions` pending | Không phải duyệt | Chờ đến `effect_date` rồi cron áp (`RegulationConfigService::applyDueGridRows` :1454, `applyVersion` :990); "Huỷ phiên bản" :1176 là người cấu hình tự huỷ, không phải người khác từ chối |
| Mục khác `pages/master-data/*` (đơn vị, thuế, thương hiệu, sản phẩm, xe…) | Không có bước duyệt | grep FE `Duyệt|Từ chối|Không duyệt` trong `pages/master-data` chỉ ra hộp xác nhận xoá; route BE MasterData có approve/reject chỉ ở price-asking / price-calculate-requests / product-price-approvals |
| Transport còn lại (`delivery-quotations`, `valid-delivery-prices`, `arrange-reports`, báo cáo) | Không có | `Modules/Transport/Routes/api.php`: chỉ có approve/deny ở :67 (delivery-trips), :100-102 (other), :139 (cost summaries), :179 (contracts); `DeliveryContract::send` :178 là người lập gửi duyệt |

## 3. Kiểm chứng

| doc_type | verify (cặp / chênh) | PHPUnit (cặp so / duyệt thật) | Đột biến |
|---|---|---|---|
| other_delivery_trip | 11.324 / 0 | cấp 1: 5.940 / 269 · cấp 2: 680 / 45 | 4/4 bị bắt (đổi quyền cấp 2 → Duyệt, bỏ "cùng công ty gốc", bỏ Thủ kho, truth cấp 2 luôn true) |
| delivery_trip | 59.600 / 0 | 1.650 / 42 | 4/4 (bỏ công ty gốc, bỏ Thủ kho, quyền hạch toán chuyến xe khác, `||` công ty làm việc) |
| price_calculate_request | 3.042 / 0 | 2.100 / 58 | 4/6 — 2 sống sót là đột biến TƯƠNG ĐƯƠNG (so `company_id` cấp công ty luôn đúng vì người duyệt chỉ tính ở đúng công ty phiếu; bỏ nhánh `approvable` vì ApprovalInboxService:278 đã bỏ assignee khi `approvable=false`) |

Verify lại 5 loại đợt 1 trong phạm vi (price_asking_request, price_asking_group, product_price_approval, delivery_contract, delivery_cost_summary): 0 chênh lệch cả 5.
API thật `GET /api/v1/approval-center/inbox?doc_type=…` (JWT người duyệt): other_delivery_trip 19 dòng (10 cấp 1 + 9 cấp 2 sau seed), delivery_trip 95, price_calculate_request 1 — `handler_path` trỏ về `pages/transport/other-delivery-trips/_id`, `delivery-trips/_id`, `sale/price-calculate-requests/_id` (đều tồn tại). `inbox/counts` có đủ 3 doc_type.
Pending thật DB local: other_delivery_trip status 1 = 7, status 5 = 6 (+4 phiếu thử cũ `TEST-APPROVAL-CENTER-CXK` của đợt trước, id 568-571); delivery_trips status 1 = 94; price_calculate_requests status 2 = **0** (chỉ phiếu thử).

## 4. File đã tạo / sửa

Tạo: `Definitions/Transport/DeliveryTripDefinition.php`, `Definitions/MasterData/PriceCalculateRequestDefinition.php`, `Definitions/MasterData/Support/PriceCalculateRequestVisibility.php`, test `Transport/DeliveryTripDefinitionTest.php`, `MasterData/PriceCalculateRequestDefinitionTest.php`.
Sửa: `Definitions/Transport/OtherDeliveryTripDefinition.php` (version 2, cấp 2) + test `Transport/OtherDeliveryTripDefinitionTest.php`; model `Transport/Entities/DeliveryTrip/DeliveryTrip.php` (trait), `MasterData/Entities/PriceCalculation/PriceCalculateRequest.php` (trait), `PriceAskingRequestGroup.php` (hook `booted()`: nhóm đổi trạng thái ⇒ sync lại YCTG status 2 của nhóm).

## 5. Chỗ ghi bằng query builder đã chạm

- `PriceAskingGroupBackfill.php` (~:165-170): `DB::table('price_calculate_requests')->update(status = REJECTED)` ⇒ thêm `scheduleSync('price_calculate_request', id)` (lệnh backfill một lần).
- Chưa xử lý (ngoài file của nhóm, nêu để người điều phối): `Modules/Finance/Services/Delivery/StockVoucherTripService.php:89` `DB::table('delivery_trips')->update(['status' => 2])` — chuyến status 1 có thể bị lùi về 2 khi `!guardLocked`; `approval-inbox:backfill` vớt, không có sync tức thì.
- Đường ERP ghi thẳng DB (phiếu hạch toán sinh status 7/3 cho cả 2 loại chuyến xe) không phát sự kiện model ⇒ chờ backfill vớt (như mọi loại ERP-ghi).

## 6. Lỗi / lưu ý code gốc (không sửa)

- `ChecksEmployeePermission::currentCompanyId()` lấy công ty GỐC làm "công ty hiện tại" trong khi quyền tính theo công ty đang làm ⇒ người kiêm nhiệm lệch (Definition theo đúng như vậy).
- `OtherDeliveryTrip::canSeeWaitingAccounting` cho cả người chỉ có "Hạch toán vận chuyển" XEM phiếu chờ hạch toán nhưng nút Không duyệt cần "Hạch toán chuyến xe khác" ⇒ người đó không có trong danh sách duyệt.
- `delivery_trips.is_hidden` chỉ lọc ở danh sách, không chặn deny — Definition không lọc.
- Màn Finance `/finance/delivery-requests` (Phiếu YC vận chuyển, bốc xếp — approve/reject `Finance/Routes/api.php:1888-1889`, F18) chưa có Definition — thuộc nhóm Finance, báo để nhóm đó kiểm.

## 7. "BE không chốt quyền" thuộc nhóm này

Không có — cả 3 loại mới/sửa đều có cổng BE rõ (`canDeny` / `canReject`).
