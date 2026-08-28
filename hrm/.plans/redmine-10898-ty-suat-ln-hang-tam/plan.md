# Redmine #10898 — Tỷ suất LN dòng hàng tạm vào luồng duyệt báo giá + hiển thị giá vốn hàng tạm

Nhánh: `tpe-develop-assign_fix` (cả API và Client)
Tài liệu mô phỏng: Google Sheets `1_Vt4pzVauKH1st5_GdsrWFLrobOLez31` (đã đọc)

## Quyết định đã chốt (user 2026-08-27)
- **Dòng hàng tạm giá nhập = 0** → tỷ suất = 0% → rơi cấp duyệt cao nhất (nhất quán với nhánh tổng hiện có: `total_import = 0` → `margin = 0` → cấp 3).
- **"Người phê duyệt báo giá"** = ai có quyền `Trưởng phòng duyệt giá Bom giải pháp` hoặc `Ban giám đốc duyệt giá Bom giải pháp` (xem được kể cả trước khi tới lượt duyệt).

## Hiện trạng đã rà
- Cấu hình: bảng `bom_price_approval_configs`, `type` enum(`order_value`,`profit_margin`), mỗi type 3 level.
- Cấp duyệt: `BomPriceApprovalConfigService::calculateApprovalLevel($totalSale, $margin)` = `max(L1, L2)`.
- Tỷ suất hiện chỉ tính TỔNG (`QuotationService::calculateTotals`), không xét từng dòng.
- Hàng tạm = dòng có `erp_product_id` null (FE: `isErpProduct`).
- `DetailQuotationResource` đã cho creator xem giá nhập dòng hàng tạm (`$canViewCostPrice || (!$isErp && $isCreator)`) — **thiếu approver**.

## Phase 1 — BE
- [ ] Migration: thêm `temp_product_margin` vào enum `type` + seed 3 level (≥35% cấp 1 · 20–35% cấp 2 · <20% cấp 3)
- [ ] `calculateTotals()`: tính tỷ suất LN từng dòng hàng tạm, lấy **thấp nhất**; cha-có-con lấy tổng giá nhập của con
- [ ] `calculateApprovalLevel($totalSale, $margin, $tempMargin)` → `max(L1, L2, L3)`; không có hàng tạm thì bỏ qua L3
- [ ] `DetailQuotationResource`: mở quyền xem giá nhập/tỷ suất dòng hàng tạm cho **approver**; trả thêm tỷ suất LN từng dòng hàng tạm

## Phase 2 — FE
- [ ] Màn cấu hình `pages/assign/settings/price-approval/index.vue`: thêm khối "Tỷ suất LN dòng hàng tạm (%)"
- [ ] Màn báo giá (tạo/sửa/chi tiết/duyệt): hiện giá nhập + giá bán + tỷ suất LN dòng hàng tạm cho creator/approver

## Kết quả

### BE (`hrm-api`)
- [x] Migration `2026_08_27_000001`: enum `type` thêm `temp_product_margin` + seed 3 cấp (≥35% · 20–35% · <20%, cấp 3 để `min_value = NULL` nên bắt cả tỷ suất ÂM)
- [x] `QuotationService::calculateTempProductMargins()` — tỷ suất từng dòng hàng tạm; cha-có-con lấy tổng giá nhập của con; giá nhập 0 → 0%
- [x] `QuotationService::isCreatorOrApprover()` — creator, người đã duyệt, hoặc người có quyền TP/BGĐ duyệt giá
- [x] `calculateTotals()` trả `temp_product_margin_percent` / `temp_product_margins` / `has_temp_product`
- [x] `BomPriceApprovalConfigService::calculateApprovalLevel($v, $m, $tempMargin = null)` = `max(L1, L2, L3)`; không có hàng tạm → bỏ qua L3 (không rơi mặc định cấp 3); tham số thứ 3 có default nên gọi 2 tham số như cũ vẫn chạy
- [x] `DetailQuotationResource`: mở quyền xem giá nhập dòng hàng tạm cho **approver** (trước chỉ creator), trả thêm `temp_margin_percent` mỗi dòng + cờ `can_view_temp_product_price`
- [x] `submit()` dùng `calculateLevel()` nên tự động áp L3, không phải sửa thêm

### FE (`hrm-client`)
- [x] `pages/assign/settings/price-approval/index.vue`: thêm khối **"Theo tỷ suất LN dòng hàng tạm (%)"** theo đúng khuôn 2 khối cũ (popover giải thích công thức + quy tắc lấy dòng thấp nhất + dòng chưa có giá vốn = 0%); tổng quát hoá `configListByType` / `setConfigError` / `configTypeLabel` thay vì copy logic
- [x] `pages/assign/quotations/_id/index.vue`: cột **Tỷ suất LN (%)** của dòng hàng tạm lấy `temp_margin_percent` do BE trả (khớp đúng số dùng xét L3); hàng ERP giữ nguyên cách tính cũ

### Kiểm thử — 46 case, 0 FAIL
- [x] BE 22 case: cấu hình L3 · `max(L1,L2,L3)` (L3 kéo cấp lên, không kéo xuống; L1/L2 vẫn có hiệu lực; không có hàng tạm thì bỏ qua; gọi 2 tham số vẫn chạy) · tỷ suất từng dòng (50% / 10%, lấy min, chỉ quét hàng tạm) · giá nhập 0 → 0% → cấp 3
- [x] BE 13 case phân quyền (`Auth::setUser` đúng 3 vai): creator thấy · approver không quyền giá vốn vẫn thấy và **không** bị mở `can_view_cost_price` · user khác không thấy giá nhập/tỷ suất nhưng vẫn thấy giá bán
- [x] UI 9 case màn Cấu hình duyệt giá: có đủ 3 khối, khối mới 3 cấp, nút Lưu riêng, không lỗi JS
- [x] UI 2 case màn chi tiết báo giá (AC2a): creator thấy giá nhập 100 và tỷ suất 50%
- [x] Dọn dữ liệu thử: trả giá dòng 2668 về gốc, trả mật khẩu 2 tài khoản test

### Giới hạn đã biết
- **AC2b/AC3 chỉ kiểm được ở tầng API/Resource, chưa kiểm trên UI**: 2 tài khoản test (approver `dainq.kdtm`, user thường `cannt.kd1`) không thấy báo giá nào có hàng tạm vì phạm vi dữ liệu theo phòng ban — toàn bộ báo giá có hàng tạm đang thuộc phòng 43 của DNS Admin. Muốn kiểm trên UI phải dựng báo giá có hàng tạm trong phòng của họ.
- **Tỷ suất LN dòng HÀNG ERP** trên màn chi tiết vẫn tính theo cách cũ (không trừ chiết khấu, cha-có-con không cộng giá nhập con) nên có thể lệch số so với BE. Ngoài phạm vi task #10898 — chưa sửa.

## Hồi quy các luồng liên quan (2026-08-27) — 88 case, 0 FAIL

Chạy sau khi hoàn thành #10898 + #10886, phủ cả #11044 và #11209.

**BE 36 case**
- Tính lại cấp duyệt của **toàn bộ 64 báo giá** bằng logic cũ (`max L1,L2`) và mới (`max L1,L2,L3`): 61 giữ nguyên · 3 tăng cấp · **0 giảm cấp** · báo giá KHÔNG có hàng tạm giữ nguyên 100%
- `calculateTotals` còn đủ 12 key cũ; `calculateLevel` không rò key nội bộ `_profit_margin_raw` / `_temp_product_margin_raw`
- `DetailQuotationResource` còn đủ key cũ (cả cấp header lẫn từng dòng hàng) + 2 key mới
- User CÓ quyền giá vốn không bị siết nhầm: `can_view_cost_price = true`, vẫn xem được giá nhập hàng ERP
- 16 query cho 1 lần dựng Resource (Resource chỉ dùng cho 1 bản ghi ở show/store/update, không dùng cho danh sách → không N+1)

**API smoke 35 case** — meeting (danh sách, chi tiết, lịch, chọn nhân sự + lọc Chức vụ + `get_all`, chọn KH, `customer-history`, khảo sát), báo giá (danh sách, chi tiết, `calculate-level` POST, `preview-submit`), cấu hình duyệt giá + lịch sử, dự án TKT + giải pháp. Kiểm route `/assign/meeting/{id}` **không bị `/customer-history` nuốt**.

**UI smoke 38 case** — 14 màn của cả 4 task đều render, có nội dung mong đợi, **không lỗi JS**.

**Hồi quy thao tác GHI 15 case** — nút "Thêm nhanh khách hàng" và ô chọn khách hàng vẫn mở popup sau khi sửa template; 2 nút căn giữa cùng hàng (tâm dọc trùng nhau); **lưu meeting HTTP 200**, giữ nguyên khách hàng / trạng thái / số dòng biên bản; lưu cả khối cấu hình cũ lẫn khối mới đều 200.

### Phát hiện đáng lưu ý (không phải lỗi)
1. **3 báo giá sẽ đổi cấp duyệt từ Cấp 1 → Cấp 3** khi gửi duyệt lại: `BG-2026-00002`, `BG-2026-00003`, `BG-2026-00144` — do có dòng hàng tạm **chưa nhập giá vốn** nên tỷ suất tính là 0%, đúng theo quyết định đã chốt. Không báo giá nào bị hạ cấp.
2. Meeting dùng loại meeting **đã khoá** (`meeting_types` id 1, `status = 2`) bị BE chặn `423` khi lưu — chốt chặn nghiệp vụ có sẵn, không liên quan thay đổi của 2 task này.
