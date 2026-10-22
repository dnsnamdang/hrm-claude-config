# Plan — Báo cáo tổng hợp nhu cầu mua: sửa theo demo (bỏ tab Đã có HĐ mua)

**Người phụ trách:** @khoipv
**Ngày bắt đầu:** 21/10/2026
**Demo gốc:** `demos/demo-bc-tong-hop-nhu-cau-mua.html` (chỉ lấy tab **Cần đi mua**)
**Spec chi tiết:** `docs/superpowers/specs/2026-10-21-bc-nhu-cau-mua-theo-demo-design.md`
**Design tóm tắt:** `.plans/bc-nhu-cau-mua-theo-demo/design.md`

## Chốt với user (21/10/2026)
- **Bỏ tab "Đã có HĐ mua"** → bỏ hẳn thanh tab, chỉ còn nội dung "Cần đi mua" (dòng còn cần mua > 0) + dòng gợi ý trên bảng
- **Đã mua tính cả HĐ mua + đơn mua** (giữ như hiện tại, KHÁC demo) — tránh mua trùng khi Lập đơn mua từ báo cáo
- Bộ lọc / nút **theo demo**: Nhóm hàng · Loại đề xuất · Khách hàng · NCC · Hợp đồng mua (NCC / HĐ lọc theo đúng dòng đã gắn chứng từ đó); bỏ 2 ô tick "Hiện cả dòng đã mua đủ" / "Chỉ mã chưa có HĐ / đơn mua"; bỏ nút giả "Tạo yêu cầu giao hàng"

## Phase 1 — FE `pages/supply/reports/purchase-demand/index.vue`
- [x] 1.1 KPI theo demo: Mã hàng cần đi mua · Phiếu xử lý có Mua thêm · Dòng cần đi mua · Tổng SL còn cần mua (bỏ "Mã hàng theo dõi")
- [x] 1.2 Bộ lọc: bỏ 2 ô tick (field + slot + state `showDone` / `onlyNoDoc`); "Mục đích mua" → "Loại đề xuất"; NCC (HĐ mua) → NCC
- [x] 1.3 Thanh thao tác: bỏ nút + popup "Tạo yêu cầu giao hàng"; Lập HĐ mua / Lập đơn mua hiện số mã đã tick `(n)`
- [x] 1.4 Dòng gợi ý (hint) trên bảng như demo
- [x] 1.5 Bảng theo demo: bỏ cột Tồn kho · HĐ / Đơn mua · SL còn lại HĐ mua · Mục đích; nhóm cột "Nhu cầu mua thêm (từ phiếu xử lý cung ứng)" = Phiếu xử lý · Cần mua thêm · Đã mua · Còn cần mua; nhóm "Thông tin đề xuất" 6 cột; chip "Σ còn cần mua" dưới tên hàng khi mã có ≥ 2 dòng; tooltip cột theo demo
- [x] 1.6 Bỏ popup "HĐ mua với NCC còn hiệu lực" (cột SL còn lại HĐ mua đã bỏ); giữ popup chứng từ mua của dòng (bấm số Đã mua)
- [x] 1.7 Thông báo bảng rỗng theo demo ("Không còn hàng nào cần đi mua" / "Không có dòng nào khớp điều kiện lọc")
- [x] 1.8 Xuất Excel khớp cột mới (bỏ Tồn kho / HĐ-Đơn mua / SL còn lại HĐ mua / Mục đích; Nhu cầu → Cần mua thêm)

## Phase 2 — BE `SupplyReportService::purchaseDemand()` (hàm dùng chung với 2 popup chọn hàng HĐ mua / đơn mua — user đã đồng ý 21/10/2026)
- [x] 2.1 Bỏ tham số `show_done` (luôn ẩn dòng đã mua đủ) — controller bỏ nhận
- [x] 2.2 `purchaseDocMeta()` trả thêm `supplier_id` / `supplier_name` → `purchase_docs` của dòng có NCC
- [x] 2.3 Lọc `ncc` / `hd_mua` theo DÒNG (dòng có chứng từ của NCC / HĐ đó), thay vì theo mã + HĐ đã duyệt
- [x] 2.4 Options NCC / HĐ mua lấy từ chứng từ còn hiệu lực (Nháp / Chờ duyệt / Đã duyệt), NCC gồm cả đơn mua; HĐ chưa duyệt ghi kèm trạng thái
- [x] 2.5 Bỏ dữ liệu không còn dùng: `purchase_contracts` / `purchase_orders` / `remaining_on_po` của row + KPI `so_ma_theo_doi`
- [x] 2.6 Kiểm tra 2 popup chọn hàng (HĐ mua / đơn mua) không đọc các field đã bỏ

## Phase 3 — Kiểm tra
- [x] 3.1 `php -l` + gọi thử service qua tinker (lọc NCC / HĐ, KPI)
- [x] 3.2 Cập nhật `demos/README.md` (ghi chú màn thật đã làm theo demo, bỏ tab 2)

## Phase 4 — Chỉnh sau review (21/10/2026)
- [x] 4.1 Bỏ dòng gợi ý (hint) trên bảng theo yêu cầu user (task 1.4 bỏ)

### Ghi chú khi làm
- Popup chứng từ của dòng (bấm số Đã mua) thêm cột **NCC**; Excel cột "Chứng từ mua" ghi HĐ/ĐM + NCC
- "Σ còn cần mua": các dòng cùng ĐVT → cộng số gốc; lệch ĐVT → dùng `total_remaining_qty` (ĐVT khối); không quy đổi được → ẩn
- Option "Hợp đồng mua" hiện `số HĐ - tên (trạng thái nếu chưa duyệt) · NCC`
- Đã chạy thử service (DB dev): 27 mã / 38 dòng; lọc NCC 2950 → 1 dòng; lọc HĐ 3 → 1 dòng; NCC không tồn tại → 0
- Cấu hình bộ lọc đã lưu có key cũ `show_done` / `only_no_doc` → panel tự bỏ key không còn trong schema

### Checkpoint — 21/10/2026
Vừa hoàn thành: Phase 1–3 (FE + BE + README demos)
Đang làm dở: —
Bước tiếp theo: user test trên trình duyệt màn /supply/reports/purchase-demand + 2 popup chọn hàng ở HĐ mua / đơn mua
Blocked:
