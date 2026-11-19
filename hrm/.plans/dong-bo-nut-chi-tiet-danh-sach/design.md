# Thiết kế: Đồng bộ nút màn Xem chi tiết ↔ Danh sách (10 màn luồng kho)

Ngày: 2026-11-02 · Dự án: HRM · Nhánh đích: `develop`

## 1. Ý định & lý do (why)

Hiện các màn **Xem chi tiết (`_id/index.vue`)** của luồng xuất/nhập kho **không hiển thị đầy đủ** các nút hành động mà màn **Danh sách (`index.vue`)** cho phép trên cùng bản ghi (sửa, in, xuất excel, duyệt, tạo chứng từ…). Người dùng vào chi tiết để xem kỹ rồi phải quay ra danh sách mới thao tác được → thừa thao tác, dễ nhầm.

Yêu cầu: **màn chi tiết phải có đủ từng ấy nút như danh sách cho đúng bản ghi đó**, và nút **"Quay lại" luôn nằm cuối cùng**.

## 2. Mục tiêu / Không mục tiêu / Chống mục tiêu

**Mục tiêu**
- Mỗi màn chi tiết hiển thị **đúng tập nút** mà danh sách hiển thị cho cùng bản ghi (cả tập nút lẫn điều kiện ẩn/hiện khớp nhau).
- "Quay lại" luôn ở cuối cụm nút.
- Toàn bộ footer màn chi tiết/form dùng component chuẩn `V2Footer` (bỏ `.export-actionbar` tự dựng).
- Parity 2 chiều: nút chỉ có ở chi tiết mà danh sách thiếu → bổ sung vào danh sách.
- Mọi lệch điều kiện ẩn/hiện giữa 2 màn → đồng bộ.

**Không mục tiêu**
- Không đổi nghiệp vụ/validation của bất kỳ hành động nào (chỉ đồng bộ hiển thị + nơi đặt nút).
- Không đụng các màn phụ (`pick`, `re-export`, `arrange`, `barcode`, `print`…) ngoài phần footer nếu chúng cũng tự dựng — *trừ khi* cần (xem phần "Để lại cho builder").
- Không commit/push (theo quy ước phiên làm việc).

**Chống mục tiêu (coi là thất bại dù chạy được)**
- Nút không dùng được mà **hiện ra disable** thay vì **ẩn** (vi phạm chuẩn HRM — phải ẩn bằng `v-if`/`visible`).
- Hard-code cờ quyền `=true` (phải fail-closed, lấy từ bản ghi/`can_*`).
- "Quay lại" không ở cuối.
- Thêm nút vào danh sách nhưng không nối đúng handler/popup → bấm không ra gì.

## 3. Quyết định đã chốt với người dùng (3 điều)

1. **Footer** → *Chuyển hẳn sang `V2Footer`*. Di cư toàn bộ 7 footer tự dựng (`.export-actionbar`) sang `V2Footer`; nút không có key sẵn (Xuất Excel, Tạo HĐ, các biến thể In) đặt vào slot `#custom-actions` (render trước "Quay lại").
2. **Chiều ngược** → *Bổ sung hết vào danh sách*. Nút chỉ có ở chi tiết mà danh sách thiếu → thêm vào cột hành động của danh sách.
3. **Điều kiện** → *Sửa luôn cho đồng bộ*. Mọi lệch điều kiện ẩn/hiện → chỉnh để 2 màn khớp.

### Quyết định bổ sung (chốt sau builder-check, 2026-11-02)

4. **Nút Duyệt phức tạp ở danh sách → ĐIỀU HƯỚNG sang chi tiết.** Các nút duyệt theo hạn mức công nợ (YCXH: Chuyển BGĐ duyệt / BGĐ duyệt) và duyệt cần nhập giá từng dòng (YCNH: BKS/BGĐ duyệt) **không duyệt tại chỗ ở danh sách** — danh sách hiện nút Duyệt, bấm vào `$router.push` sang màn chi tiết để duyệt (đúng ngoại lệ "nút Duyệt là lối sang màn tiếp theo"). **Kéo theo BE**: API danh sách YCXH/YCNH phải trả thêm cờ `is_can_*_approve` tương ứng để danh sách ẩn/hiện nút đúng (fail-closed). ⇒ Feature **không còn thuần FE** — có phần BE ở 2 Resource danh sách (eager-load tránh N+1).
5. **In PXBHM → luôn hiện cả 2 màn.** Bỏ gate `is_can_view` ở nút In màn chi tiết PXBHM (danh sách vốn đã luôn hiện, có chủ ý "in = chỉ đọc"). In là thao tác chỉ đọc nên không gate quyền riêng.
6. **Dọn nút disabled-hiện trên 10 màn danh sách.** Mọi nút đang `interactable + disabledTitle` (hiện nhưng xám) → đổi sang `v-if`/`visible` ẩn hẳn, khớp chuẩn và khớp màn chi tiết (áp cho toàn bộ cột hành động của 10 danh sách, không chỉ các nút liệt kê ở §7).

## 4. Chuẩn áp dụng (từ HRM/CLAUDE.md)

- Nút chi tiết/form **phải** nằm trong `V2Footer`; "Quay lại" tự render cuối.
- Chi tiết chỉ được phép **thiếu** so với danh sách: "Xem" (vì đang ở chi tiết) và "Lịch sử" nếu đã nhúng qua `SystemInfoSection`.
- Nút không khả dụng → **ẩn** (`v-if`/`visible`), **không** hiện disable.
- Dùng `V2Base*` component, không HTML thô.
- Cờ quyền **fail-closed**, lấy từ bản ghi (`can_edit`, `is_can_view`, `can_approve`…), không hard-code.
- Số định dạng quốc tế (`,` nghìn, `.` thập phân) — không liên quan trực tiếp nhưng giữ nguyên tắc.

## 5. Phạm vi: 10 màn

| # | Màn | Route | List | Detail |
|---|-----|-------|------|--------|
| 1 | YCXH – Yêu cầu xuất hàng | /finance/product-export-requests | index.vue | _id/index.vue (dùng `ProductExportRequestForm.vue` readonly) |
| 2 | ĐNXK – Đề nghị xuất kho | /finance/warehouse-export-requests | index.vue | _id/index.vue |
| 3 | PXK – Phiếu xuất kho | /finance/warehouse-exports | index.vue | _id/index.vue (+ pick, re-export) |
| 4 | PXH – Phiếu xuất hàng | /finance/product-exports | index.vue | _id/index.vue |
| 5 | YCNH – Yêu cầu nhập hàng | /finance/product-import-requests | index.vue | _id/index.vue |
| 6 | ĐNNK – Đề nghị nhập kho | /warehouse/import-requests | index.vue | _id/index.vue |
| 7 | PNK – Phiếu nhập kho | /finance/warehouse-imports | index.vue | _id/index.vue (+ arrange, barcode, re-export, re-import) |
| 8 | PNH – Phiếu nhập hàng | /finance/product-imports | index.vue | _id/index.vue |
| 9 | YCXBHM – Yêu cầu xuất bán hàng mượn | /finance/borrow-sell-requests | index.vue | _id/index.vue (+ print) |
| 10 | PXBHM – Phiếu xuất bán hàng mượn | /finance/borrow-sells | index.vue | _id/index.vue |

## 6. Phát hiện hệ thống (từ audit)

**① Footer tự dựng (`.export-actionbar`) ở 7/10 màn chi tiết** — cần di cư sang `V2Footer`:
- Đặt "Quay lại" ở **đầu** cụm (sai thứ tự): ĐNXK, PXK, PXH, YCXBHM, PXBHM.
- "Quay lại" ở cuối nhưng vẫn tự dựng: ĐNNK, PNK.
- Đã dùng `V2Footer` đúng (giữ nguyên, chỉ bổ sung nút thiếu nếu có): YCXH, YCNH, PNH.

**② Nút In / Xuất Excel có ở danh sách nhưng thiếu ở chi tiết**: YCXH (thiếu 3 nút In/Xuất), ĐNXK (thiếu 2 nút In).

## 7. Thay đổi theo từng màn

> Ký hiệu: **[D←L]** = thêm vào chi tiết cho khớp danh sách · **[L←D]** = thêm vào danh sách cho khớp chi tiết · **[FOOTER]** = di cư sang V2Footer · **[COND]** = sửa điều kiện ẩn/hiện.

### 1. YCXH – product-export-requests
- **[D←L]** Thêm vào chi tiết 3 nút: In (các biến thể) + Xuất Excel (danh sách có, chi tiết thiếu) → vào `#custom-actions` của V2Footer đang dùng trong `ProductExportRequestForm.vue`.
- **[L←D]** Thêm vào danh sách: "Lập phiếu xuất hàng" + các nút duyệt (Chuyển BGĐ duyệt / BGĐ duyệt / Không duyệt). Nút duyệt ở danh sách **điều hướng sang chi tiết** (quyết định §3.4), không duyệt tại chỗ.
- **[BE]** Resource danh sách YCXH trả thêm `is_can_manager_approve`, `is_can_board_approve` (đang có ở detail `ProductExportRequestForm.vue:1631-1667`) để danh sách ẩn/hiện nút duyệt đúng. Eager-load/`selectRaw` tránh N+1.
- **[COND]** Nút "Lập ĐNXK": bổ sung điều kiện `is_export_direct ≠ 1` cho khớp.

### 2. ĐNXK – warehouse-export-requests
- **[FOOTER]** Di cư `.export-actionbar` (_id ~231-255) → V2Footer; "Quay lại" về cuối.
- **[D←L]** Thêm 2 nút In còn thiếu ở chi tiết.
- **[L←D]** Thêm "Hủy" vào danh sách nếu chi tiết có mà list thiếu.

### 3. PXK – warehouse-exports
- **[FOOTER]** Di cư `.export-actionbar` (_id ~85-124) → V2Footer; "Quay lại" về cuối. Giữ các nút điều hướng sang pick/re-export trong `#custom-actions`.

### 4. PXH – product-exports
- **[FOOTER]** Di cư `.export-actionbar` (_id ~376-388) → V2Footer; "Quay lại" về cuối.

### 5. YCNH – product-import-requests
- **[L←D]** Thêm vào danh sách 5 nút duyệt/không duyệt (BKS duyệt, Chuyển BGĐ, BGĐ duyệt, Không duyệt…) hiện chỉ có ở chi tiết. Duyệt BKS/BGĐ **cần lưới nhập giá mua từng dòng** (`approvedPrices`, `_id/index.vue:150-168`) → **KHÔNG** duyệt tại chỗ ở danh sách; nút ở danh sách **điều hướng sang chi tiết** để duyệt (quyết định §3.4). Bỏ ý "tái dùng popup" (không tồn tại popup rời — giá nhập inline trong lưới).
- **[BE]** Resource danh sách YCNH trả thêm `is_can_approve_by_manager`, `is_can_control_board_approve`, `is_can_board_of_manager_approve` (đang có ở detail `_id/index.vue:415-434`) để danh sách ẩn/hiện nút duyệt đúng. Eager-load tránh N+1.
- **[~~COND~~]** ĐÍNH CHÍNH: nút "Sửa" ở chi tiết YCNH **đã ẩn đúng** qua `footerMenu = { edit: is_can_edit }` (`_id/index.vue:752`) — **không cần sửa**. (Audit cũ nhầm là disable.)

### 6. ĐNNK – warehouse/import-requests
- **[FOOTER]** Di cư `.export-actionbar` (_id ~180-210, SCSS ~493-524) → V2Footer.

### 7. PNK – warehouse-imports
- **[FOOTER]** Di cư `.export-actionbar` (_id ~174-194, computed `barActions` ~296-301) → V2Footer. List & detail cùng dùng `components/row-actions.js`→`warehouseImportRowActions(item)` nên tập nút đã đồng bộ sẵn; chủ yếu đổi vỏ footer + thứ tự "Quay lại".

### 8. PNH – product-imports
- **[L←D]** Thêm "Phân bổ hàng" vào danh sách (chi tiết có, list thiếu). Chi tiết đã dùng V2Footer + `#custom-actions` (574-590) — giữ nguyên.

### 9. YCXBHM – borrow-sell-requests
- **[FOOTER]** Di cư `.export-actionbar` (_id ~212-248) → V2Footer; "Quay lại" về cuối.
- **[D←L]** Thêm "Sửa" vào chi tiết (list có, detail thiếu).

### 10. PXBHM – borrow-sells
- **[FOOTER]** Di cư `.export-actionbar` (_id ~390-402) → V2Footer; "Quay lại" về cuối.
- **[COND]** Nút "In": **bỏ gate `is_can_view`** ở chi tiết (`_id/index.vue:397`) → In luôn hiện cả 2 màn, khớp chủ ý danh sách "in = chỉ đọc" (quyết định §3.5). (Audit cũ ghi ngược chiều.)

### Xuyên suốt 10 màn danh sách — dọn nút disabled-hiện
- **[COND]** Rà cột hành động 10 `index.vue`, mọi nút dùng `interactable + disabledTitle` (hiện xám) → chuyển điều kiện vào `v-if`/`visible` để **ẩn hẳn** (quyết định §3.6). Ví dụ đã thấy: nút "Sửa" list YCNH (`product-import-requests/index.vue:682-683`). Khớp chuẩn HRM/CLAUDE.md và khớp màn chi tiết.

## 8. Cách làm chung cho mỗi màn chi tiết (khuôn V2Footer)

1. Xác định tập nút của danh sách cho bản ghi (đọc `getRowActions(item)`/`rowActions`/`row-actions.js`).
2. Map mỗi nút sang: (a) key dựng sẵn của V2Footer (`edit/print/approve/delete/cancel/...`) nếu có; (b) còn lại (Xuất Excel, Tạo HĐ, biến thể In nhiều loại, "Lập phiếu…") → `#custom-actions` bằng `V2BaseButton`.
3. Chuyển mỗi điều kiện `visible/v-if` từ danh sách sang đúng nút footer (cùng biểu thức, fail-closed).
4. Nối `@click`/emit về đúng handler đã có ở chi tiết (hoặc gọi API/popup giống danh sách).
5. Bỏ `<div class="export-actionbar">` + SCSS liên quan; "Quay lại" do V2Footer tự render cuối (không tự thêm).

## 9. Kiểm thử (bắt buộc trước khi báo xong)

- Chạy HRM local (skill `run-hrm`): MySQL erp_hrm_check → API:8000 → Nuxt `http://127.0.0.1:3000`.
- Với mỗi màn: mở 1 bản ghi ở **danh sách**, chụp tập nút hiện; mở **chi tiết** cùng bản ghi, xác nhận **đúng tập nút** + **"Quay lại" cuối** + mỗi nút bấm ra đúng hành động/popup.
- Thử ≥1 bản ghi ở trạng thái khác (đã duyệt/đã hủy) để xác nhận điều kiện ẩn/hiện khớp 2 màn.
- Playwright MCP dùng `http://127.0.0.1:3000`, không `pkill -f mcp-chrome`.

## 10. Để lại cho builder (quyết trong lúc làm, ghi lại là quyết định của tôi)

- Tên key/handler chính xác cho từng nút trong V2Footer lấy theo code hiện có từng màn.
- Nếu một màn phụ (pick/re-export/arrange/barcode) cũng tự dựng footer → **chỉ** đổi khi nằm trong cùng flow nút đang đồng bộ; ngoài ra ghi nhận, không mở rộng phạm vi.
- (Đã chốt — không còn để builder) Duyệt BKS/BGĐ ở danh sách = điều hướng sang chi tiết, xem §3.4.
- Tên chính xác cờ BE cần thêm vào Resource danh sách (YCXH/YCNH) lấy theo accessor đang dùng ở detail; cách tính phải tái dùng accessor/logic sẵn có của Entity, eager-load tránh N+1 (không thêm query mỗi dòng).

## 11. Ràng buộc phiên làm việc

- **Không commit/không push** trừ khi người dùng yêu cầu.
- Mọi tài liệu ghi ở `HRM/.plans/dong-bo-nut-chi-tiet-danh-sach/` (qua symlink), không ghi trong `hrm-client`/`hrm-api`.
- Làm trên nhánh `develop` (hiện đang ở `feat/ychtdv-hdbh-p2`; sẽ chuyển nhánh khi được duyệt kế hoạch — kiểm tra sạch working tree trước).
