# Popup chọn hàng HĐ mua — tách bộ lọc + nới rộng — @khoipv

File: `hrm-thanhan-client/pages/supply/purchase_contracts/components/GoodsPickerModal.vue` (chỉ FE)

## Phase 1 — FE
- [x] Tách ô tìm chung thành ô **Mã/Tên hàng** (chỉ khớp tên, mã hàng, mã HH)
- [x] Thêm bộ lọc **Khách hàng** (base-select2, allowClear, option lấy từ goods-pool)
- [x] Thêm bộ lọc **Số HĐ** (HĐ bán — số HĐ, fallback mã HĐ; option thu hẹp theo khách hàng đã chọn)
- [x] Khách hàng + Số HĐ lọc theo **cùng 1 dòng phiếu** (purpose) — hàng danh mục (không phiếu) bị loại khi có lọc
- [x] Giữ bộ lọc Nguồn; reset cả 4 khi mở popup; đổi lọc → về trang 1
- [x] Nới rộng popup: `size="xl"` → `dialog-class="modal-md-width"` (85% màn hình)
- [x] Fix không gõ tìm được trong ô Khách hàng / Số HĐ: b-modal giữ focus (enforce focus) nên ô search của select2 (gắn ở body) không nhận focus → thêm `no-enforce-focus`
- [x] Ô Khách hàng hiện TOÀN BỘ KH danh mục (dùng lại `GET supply/supply-proposals/customers?group=1`, nạp 1 lần) + gộp thêm KH chỉ có trên phiếu
- [x] Ô Nguồn thêm lựa chọn **Theo hợp đồng** (hàng có ít nhất 1 dòng phiếu gắn HĐ bán)
- [x] Ô Mã/Tên đổi sang `base-input-field` + ép chiều cao bằng select2 (modal render ngoài `.default-layout` nên input cao 38px)
- [x] Bộ lọc dùng `col-md-3` (4 ô lọc 1 hàng). Đã thử nút Làm mới rồi bỏ theo yêu cầu user
- [x] **Chọn riêng từng phiếu** (theo màn Đơn mua hàng): mỗi dòng phiếu PĐX/PXL của 1 mã = 1 dòng trong popup (SL đề xuất = SL của phiếu đó); cột "Phiếu đề xuất / xử lý" hiện PĐX + PXL (bấm mở chi tiết); KH 1 dòng; footer đếm "dòng"
- [x] `ProductsTab.mergeLine`: bỏ trùng purpose thêm điều kiện `handling_id` (2 PXL cùng PĐX + KH không bị mất 1 dòng)
- [x] Bảng hàng hóa (`ProductsTab.vue`): dòng **TỔNG CỘNG** chuyển từ đầu xuống cuối bảng (sau các dòng hàng), thêm kẻ đậm phía trên
- [x] Fix: đã chọn mã ở PĐX 1, mở lại popup không chọn tiếp được PĐX 2 (do loại CẢ MÃ đã có trong HĐ)
  - [x] BE `PurchaseContractController::goodsPool`: `exclude_codes` chỉ loại catalog + nhu cầu KHÔNG phiếu; nhu cầu có dòng phiếu giữ lại
  - [x] FE `ProductsTab.pickedLines` (mã + purposes từng dòng HĐ) → `GoodsPickerModal.isPicked` ẩn đúng dòng phiếu đã có (so PĐX + KH + HĐ bán + PXL nếu có); chọn phiếu mới của mã đã có → gộp vào dòng sẵn có (pill "Ghép vào dòng sẵn có")
- [ ] Build client + hard refresh, test UI

## Phase 2 — Lọc theo HĐ hiện cả hàng CHƯA ĐỀ XUẤT (02/10/2026)
Chốt với user: ô Số HĐ = mọi HĐ bán còn hiệu lực (thu hẹp theo KH) · hàng chưa đề xuất SL để trống, nhập tay ·
"chưa đề xuất" = mã chưa có trên phiếu đề xuất còn sống nào của HĐ đó (đã đề xuất rồi mua đủ → không hiện) · chỉ HĐ mua, không đụng Đơn mua.
### BE
- [x] `PurchaseContractService::saleContractOptions()` — HĐ bán duyệt/kết xuất, record_type HĐ, chưa hết hạn (gồm gia hạn) → trả thêm key `contracts` trong `goods-pool`
- [x] `PurchaseContractService::unproposedContractGoods($contract)` — dòng hàng HĐ (gộp theo mã) bỏ mã đã có trong `proposedQtyMap` + enrich quy cách/hãng
- [x] Route `GET purchase-contracts/sale-contracts/{contract}/goods` + controller
### FE — GoodsPickerModal
- [x] Ô Số HĐ gộp danh sách `contracts` (thu hẹp theo KH đang chọn)
- [x] Chọn HĐ → gọi API lấy hàng chưa đề xuất (cache theo HĐ), ứng viên mang purpose không phiếu (KH + HĐ bán), SL đề xuất trống
- [x] Ẩn hàng chưa đề xuất đã có trong HĐ mua (cùng mã + cùng HĐ bán, purpose không phiếu); nguồn "Theo phiếu" loại, "Không theo phiếu"/"Theo hợp đồng" giữ; pill "HĐ · chưa đề xuất"
- [x] Thêm vào HĐ: lấy từ cả pool lẫn cache HĐ (giữ lựa chọn khi đổi HĐ)
### FE — ProductsTab
- [x] Purpose không phiếu nhưng có HĐ bán: hiện chip "Chưa đề xuất" thay mã phiếu; tính như 1 phiếu (ô Mua riêng) để tách giá theo KH; SL đề xuất chỉ cộng phiếu thật; lọc "ngoài phiếu đề xuất" theo phiếu thật
- [x] Fix: lọc theo HĐ chỉ thấy hàng theo phiếu — hàng chưa đề xuất bị nối cuối, HĐ nhiều dòng phiếu đẩy sang trang sau → khi lọc HĐ trộn + xếp theo tên hàng; footer đếm "gồm N hàng HĐ chưa đề xuất"
- [x] Fix: Nguồn = "Theo hợp đồng" (chưa chọn Số HĐ) chỉ ra hàng theo phiếu → nạp hàng chưa đề xuất của MỌI HĐ còn hiệu lực
  - [x] BE `unproposedActiveContractGoods()` + gom `unproposedGoodsOf()` (nhiều HĐ, truy vấn 1 lần); route `GET purchase-contracts/sale-contracts/goods` (trước wildcard)
  - [x] FE `fetchAllContractGoods` khi Nguồn = Theo hợp đồng, chia vào cache theo HĐ; `_idx` cố định `ctr:<HĐ>:<SP>:<ĐVT>`, confirm bỏ trùng
- [x] Test UI bằng MCP browser: lọc Số HĐ (74 dòng / 60 chưa ĐX), Nguồn Theo HĐ (3994 / 3959), thêm vào HĐ hiện chip "Chưa đề xuất"
- [x] Hàng THUỘC HĐ lên đầu ở MỌI chế độ (user chốt): mở popup nạp nền hàng chưa đề xuất của mọi HĐ (`allCtrLoading`, không che bảng, footer báo "Đang tải…", token chống request cũ); sort: hasCtr trước (trộn phiếu có HĐ + chưa ĐX, xếp theo tên), hàng không gắn HĐ sau giữ thứ tự cũ. Test MCP: Tất cả = 7168 dòng, 3994 dòng thuộc HĐ ở đầu
- [x] Sửa thứ tự theo ý user: (0) dòng phiếu đề xuất có gắn HĐ lên đầu → (1) hàng HĐ chưa đề xuất (xếp theo tên) → (2) hàng không gắn HĐ. Nhóm 0/2 giữ thứ tự cũ. Test MCP Nguồn Theo HĐ: 3994 dòng = 35 dòng phiếu ở đầu + 3959 dòng chưa ĐX, không có dòng nào sai thứ tự
- [x] Xóa nhãn "Ghép vào dòng sẵn có" ở popup HĐ mua (user yêu cầu): bỏ template, CSS `.gm-pill-merge`, cờ `inContract` + hàm `inHd`. Chọn hàng trùng mã vẫn tự gộp vào dòng có sẵn (mergeLine), chỉ không báo trước. Đơn mua hàng không đụng
- [x] Bỏ 1 phiếu khỏi dòng hàng gộp nhiều phiếu (ProductsTab HĐ mua): nút × cuối mỗi dòng phiếu (≥2 phiếu, không readonly, không dòng đã đổi) → msgBoxConfirm → splice purpose, tính lại proposed_qty/order_qty (+ base), giá bình quân, ghi chú, CK; phiếu hiện lại ở popup. Test MCP: mã 52861 gộp 3 phiếu (17) → bỏ DXCU-0039 còn 10, popup hiện lại DXCU-0039; còn 1 phiếu thì nút × ẩn
- [x] Bỏ tooltip "Bỏ phiếu này khỏi dòng hàng" trên nút × (user yêu cầu)
- [x] Đơn mua hàng (purchase_orders/ProductsTab) bổ sung nút × bỏ 1 phiếu như HĐ mua (user yêu cầu): tính lại proposed_qty/order_qty (+ base), giá bình quân, ghi chú, Bên mua; không tooltip. Test MCP: 52861 gộp 3 phiếu (17) → bỏ DXCU-0028·PXL-0015 còn 14. LƯU Ý: popup DMH ẩn CẢ mã đã có trong đơn (BE lọc exclude_codes) → phiếu vừa bỏ KHÔNG hiện lại để chọn, chờ user quyết có sửa không
- [ ] User test lưu / mở lại HĐ mua có dòng chưa đề xuất

### Checkpoint — 2026-09-30
Vừa hoàn thành: tách mỗi phiếu 1 dòng trong popup + mergeLine so thêm handling_id
Đang làm dở: —
Bước tiếp theo: user build client + test UI
Blocked:

### Checkpoint — 2026-10-02
Vừa hoàn thành: Phase 2 BE (saleContractOptions, unproposedContractGoods, route sale-contracts/{contract}/goods) + FE GoodsPickerModal (gộp HĐ, nạp lười hàng chưa đề xuất, pill "HĐ · chưa đề xuất") + ProductsTab (purpose không phiếu có HĐ bán = chip "Chưa đề xuất", ô Mua riêng, ĐX chỉ cộng phiếu thật). Đã test BE bằng tinker, biên dịch thử template/script 2 file Vue OK
Đang làm dở: —
Bước tiếp theo: user build client + hard refresh, test UI (lọc Số HĐ → thấy hàng chưa đề xuất, thêm vào HĐ, nhập SL, lưu/mở lại)
Blocked:
