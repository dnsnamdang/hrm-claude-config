# Đưa dòng TỔNG CỘNG xuống cuối bảng Hàng hóa — Đơn mua hàng

**Người phụ trách:** @khoipv
**Màn:** `supply/purchase_orders` — tab "Hàng hóa" (`ProductsTab.vue`, dùng chung Lập mới / Sửa / Xem)
**Phạm vi:** chỉ FE, 1 file. Không BE / API / migration / quyền.

## Yêu cầu

Dòng TỔNG CỘNG đang nằm **đầu** `<tbody>` → chuyển xuống **cuối bảng**.
Chốt với user: **nằm cuối bảng, cuộn dọc thì trôi theo** (KHÔNG dính đáy vùng cuộn).

## Task

### Phase 1 — FE
- [x] 1. Cắt khối `<tr class="total-row">…</tr>` (dòng 76–104) ở đầu `<tbody>` của `ProductsTab.vue`
- [x] 2. Dán xuống cuối `<tbody>`, sau `v-for="row in visibleRows"` và sau dòng "Không có hàng hóa phù hợp bộ lọc"
- [x] 3. Giữ nguyên CSS (`tr.total-row td`, `tr.total-row td.col-freeze`, `.col-freeze-total`) — selector không phụ thuộc vị trí

### Phase 2 — Verify
- [x] 4. Đếm ô dòng tổng = 20 cột (khớp header)
- [x] 5. Compile sạch bằng `vue-template-compiler`
- [ ] 6. User xem mắt trên trình duyệt (cần build lại client + hard refresh)

## Ghi chú kỹ thuật

- Không có logic kéo-thả bám vị trí dòng; `drag-handle` chỉ là class CSS thừa
- Sticky-left 3 cột đầu (0 / 42 / 138) và nền đục `#eef4f3` của dòng tổng giữ nguyên
- Liên quan: `.plans/don-mua-co-dinh-cot-bang-hang-hoa/plan.md` (cố định 3 cột đầu cùng bảng này)

### Checkpoint — 2026-09-10
Vừa hoàn thành: chuyển dòng TỔNG CỘNG từ đầu `<tbody>` xuống cuối (ProductsTab.vue dòng 291–320 sau khi chuyển). CSS giữ nguyên. Compile `vue-template-compiler` sạch; dòng tổng = 20 cột, khớp 20 `<th>` header. Lưu ý: file dùng CRLF — sed đã đổi sang LF, đã convert lại CRLF nên diff chỉ còn đúng khối di chuyển.
Đang làm dở: (không)
Bước tiếp theo: @khoipv build lại client + hard refresh, xem mắt trên trình duyệt
Blocked:

## Task bổ sung — Tiền tố 4 cột tham chiếu hiện Mã HĐ thay vì Số HĐ (2026-09-10)

Bối cảnh: user hỏi 4 cột "Đơn giá báo giá / Ghi chú báo giá / Ghi chú thầu / Ghi chú hợp đồng"
lấy dữ liệu gì (thấy tiền tố `kl;lk;`, `fbdfb`). Truy ra: tiền tố là **Số HĐ bán**
(`contracts.number`, do `SupplyReportService` dòng 139 ưu tiên `number` rồi mới `code`),
người dùng gõ tay nên hay rác. Trong khi cột "Mục đích mua" cùng bảng đã hiện **Mã HĐ**
(`contracts.code`) qua `saleContractCode()` → đang không đồng nhất.

**User chốt: đổi tiền tố 4 cột sang Mã HĐ.**

- [x] 7. `contractsOf(p)` lấy `contract_code` ưu tiên từ `productRefMap` (= `contracts.code` do
      `PurchaseOrderController::productInfo` trả về), fallback `purposes[].contract_code` cũ
- [x] 8. Compile `vue-template-compiler` sạch
- [x] 9. Đối chiếu DB: HĐ 220 phải hiện `HD-192/2026` (thay `kl;lk;`), HĐ 221 `HD-193/2026` (thay `fbdfb`)

Chỉ FE, 1 file, KHÔNG đụng BE (`SupplyReportService` dùng chung với báo cáo nhu cầu mua).

## CHƯA LÀM — chờ @khoipv chốt

**Bug: `keyBy('product_id')` làm mất đơn giá báo giá khi 1 HĐ bán có nhiều dòng cùng mã hàng.**
`SupplyHandlingService::productInfoMap()` dòng ~50 `->keyBy('product_id')` chỉ giữ **dòng cuối**.
Ví dụ thật: HĐ 220 (`HD-192/2026`) liệt kê mã 3322 "Chất hiệu chuẩn HDL/LDL" trên 3 dòng —
cp.id 6211 (status 1, `price_quotation` 200.000), 6214 + 6215 (status 2, NULL) → hiện `—`
thay vì 200.000. DB hiện có **13 cặp (HĐ, mã hàng) trùng dòng**, 1 cặp đang thực sự mất dữ liệu.
Đề xuất: lấy giá trị khác rỗng ĐẦU TIÊN theo từng trường, thay vì khóa cứng 1 dòng.
⚠️ `productInfoMap()` là **hàm dùng chung** (Phiếu đề xuất cung ứng + Xử lý cung ứng + HĐ mua)
→ theo CLAUDE.md phải được xác nhận trước khi sửa.

### Checkpoint — 2026-09-10 (task bổ sung)
Vừa hoàn thành: `contractsOf()` trong `ProductsTab.vue` lấy `contract_code` ưu tiên từ `productRefMap` (mã HĐ thật `contracts.code`), fallback `purposes[].contract_code`. Template + script compile sạch. Verify bằng `php artisan tinker` gọi thẳng `SupplyHandlingService::productInfoMap()`: HĐ 220 → `HD-192/2026`, HĐ 221 → `HD-193/2026`; đồng thời TÁI HIỆN được bug keyBy (cid 220 trả `price_quotation=NULL` dù dòng cp.id 6211 có 200.000).
Đang làm dở: (không)
Bước tiếp theo: @khoipv chốt hướng sửa bug `keyBy('product_id')` ở `productInfoMap()` (hàm dùng chung)
Blocked: chờ xác nhận để sửa hàm dùng chung

## Task 10-11 — Luôn in mã HĐ ở 4 cột tham chiếu

- [x] 10. Bỏ `v-if="contractsOf(row.p).length > 1"` trên span `.ref-hd` ở cả 4 cột (Đơn giá báo giá / Ghi chú báo giá / Ghi chú thầu / Ghi chú hợp đồng) — `ProductsTab.vue` dòng 192, 205, 219, 232
- [x] 11. Verify: `vue-template-compiler` → 0 error / 0 tip; file giữ CRLF; diff đúng 4 dòng

**Lý do:** trước đây hàng chỉ thuộc 1 HĐ bán thì in giá trị trần, người dùng không biết dữ liệu của HĐ nào.
VD hàng "Cóng đựng mẫu bệnh phẩm" (product_id=1) chỉ nằm trong HĐ 2 (HD-002/2025) → 4 cột hiện `—` / `—` / `STT1. Phần mềm…` / `STT1. Phần mềm…` mà không có nhãn.
Sau khi sửa: luôn hiện `HD-002/2025: …`. Nhất quán với cột "Mục đích mua" (vốn luôn in mã HĐ).

**Dữ liệu tham khảo:** `supply_handling_products` có 26 dòng, 9 dòng `contract_id = NULL` (mua ngoài HĐ bán).
Dòng không gắn HĐ không có `contract_products` để tham chiếu → 4 cột hiện `—`, không đổi.

### Checkpoint — 2026-09-10
Vừa hoàn thành: task 10-11 (luôn in mã HĐ ở 4 cột tham chiếu)
Đang làm dở: (không)
Bước tiếp theo: user build lại client + hard refresh
Blocked: bug `keyBy('product_id')` trong `SupplyHandlingService::productInfoMap()` — chờ @khoipv chốt vì là hàm dùng chung
