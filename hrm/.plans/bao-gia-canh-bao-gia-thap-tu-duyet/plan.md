# Plan — Báo giá: cảnh báo đơn giá ≤ 1.000 & tự động duyệt (#10797)

## Phase 1 — Logic phê duyệt (BE)

- [x] `QuotationService::LOW_PRICE_THRESHOLD = 1000`
- [x] `QuotationService::isAutoApprovable()` — không GG + không hàng/DV tạm + mọi đơn giá bán > 1.000 + báo giá không rỗng
- [x] `calculateLevel()` ép `level = 1` khi thoả TH1, trả thêm cờ `auto_approve` (submit() dùng lại nên tự chạy đúng)

## Phase 2 — Cảnh báo đơn giá thấp (FE)

- [x] Component mới `QuotationLowPriceWarningModal.vue` (bảng Mã/Tên/Đơn giá, 2 nút, footer ghim đáy)
- [x] `edit.vue`: computed `lowPriceItems` + `lowPriceKeySet`, cờ `lowPriceHighlight` / `lowPriceModalShow`
- [x] `edit.vue`: tô nền cam dòng vi phạm (class `.low-price-row`, áp cho cả dòng cha và dòng con)
- [x] `edit.vue`: `openSubmit()` chèn bước cảnh báo; `onLowPriceContinue()` mở popup gửi duyệt
- [x] `QuotationSubmitModal.vue`: hiển thị "Tự động duyệt" + câu giải thích khi `auto_approve`

## Phase 3 — Rà lại theo skill + test thật

- [x] `button-convention`: sửa nút "Tiếp tục gửi duyệt" → `primary status="warning"` + `ri-send-plane-line` (trước đó sai: `primary` teal + `ri-check-line`)
- [x] `button-convention` mục 4.2: đổi chữ nút theo bảng chuẩn — "Tiếp tục trình duyệt" → **Tiếp tục gửi duyệt**, "Quay lại chỉnh sửa" → **Quay lại**
- [x] `modal-popup` mục 0: triệt `margin-top`/`margin-bottom` khối đầu-cuối trong body popup
- [x] Sửa icon khoá ô GG bị ĐỎ: theme `custom-assign.scss` đặt `.text-muted { color: #dc3545 !important }` cho cả phân hệ Giao việc → dùng lớp riêng `.text-soft` (#6b7280), bám pattern `SummaryQuotationForm.vue`
- [x] Bổ sung quy tắc "skill thắng spec về hình thức UI" vào CLAUDE.md

## Kết quả test (2026-08-17, cổng 3000/8000, tài khoản DNS Admin)

**BE — `isAutoApprovable()` (chạy trong transaction rồi rollback, dữ liệu thật không đổi):**

| Ca | Kết quả |
| --- | --- |
| ERP + đơn giá 5.000.000 + không GG | TRUE — tự duyệt ✅ |
| Có 1 dòng đơn giá = 1.000 (biên) | false ✅ |
| Dòng đó = 1.001 | TRUE ✅ |
| Biến 1 dòng thành hàng tạm | false ✅ |
| Bật GG mặt hàng 50.000 | false ✅ |
| Báo giá rỗng / dòng chưa có giá | false ✅ |

**FE — luồng thật trên BG-2026-00240:** `lowPriceItems` bắt đúng 1 dòng 500đ · popup hiện đúng tiêu đề, số lượng, bảng Mã/Tên/Đơn giá · dòng vi phạm nền cam `rgb(255,237,213)` · "Quay lại" đóng popup giữ nguyên màn và giữ nền cam · "Tiếp tục gửi duyệt" sang popup phê duyệt, ra **Cấp 3** (đúng TH2 vì có dòng ≤ 1.000).

## Test lại đầy đủ trên nhánh `tpe-develop-assign` (2026-08-18)

| AC | Kết quả |
| --- | --- |
| AC1 | Báo giá sạch (2 dòng ERP 3tr + 5tr, không GG): **không** popup cảnh báo · popup ghi "Tự động duyệt" · bấm Xác nhận duyệt → status 1 → **4 Đã duyệt**, level=1, approved_by=13, lịch sử `self_approve` 1→4 ✅ |
| AC2 | 1 dòng 500đ → popup đúng nội dung, dòng vi phạm nền cam `rgb(255,237,213)`; nút `primary-warning` + `ri-send-plane-line` ✅ |
| AC3 | "Quay lại" → đóng popup, ở nguyên màn, dòng vẫn nền cam ✅ |
| AC4 | "Tiếp tục gửi duyệt" → sang popup phê duyệt ✅ |
| AC5 | Có GG tổng 200.000 → không tự duyệt, ra Cấp 3, Xác nhận gửi → status 1 → **2 Chờ TP duyệt**, lịch sử `submit` ✅ |

ERP sync sau khi tự duyệt fail mềm ("Khách hàng ERP chưa có địa chỉ giao hàng") → ghi
`erp_sync_status = failed`, không tạo bản ghi bên ERP. Dữ liệu test đã khôi phục nguyên trạng.

### Checkpoint — 2026-08-17
Vừa hoàn thành: BE + FE #10797, rà lại theo `button-convention` / `modal-popup`, test BE 6 ca + FE hết AC2/AC3/AC4.
Đang làm dở: không.
Bước tiếp theo: chưa test AC1 (báo giá sạch → tự duyệt) trên UI vì chưa có báo giá nào đủ điều kiện — cần 1 báo giá toàn hàng ERP có giá > 1.000.
Blocked:
