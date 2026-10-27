# Plan — PXL ma trận Nguồn × Phương án

@khoipv

## Phase 1 — BE
- [x] Migration thêm 11 cột ô `alloc_<nguồn>_<pa>` + backfill từ `alloc_*` cũ
- [x] `SupplyHandling`: const MATRIX theo loại + helper suy ra alloc cũ
- [x] `StoreSupplyHandlingRequest`: validate 11 ô
- [x] `SupplyHandlingService::syncProducts`: lưu ô (ép 0 ô không thuộc loại), suy ra `alloc_*` cũ
- [x] `DetailSupplyHandlingResource`: trả 11 ô
- [x] Xuất Excel bảng hàng theo ma trận (blade)

## Phase 2 — FE
- [x] `constants.js`: ma trận theo loại + helper (cellKey, lineSum, colSum, deriveLegacy)
- [x] `HandlingGoodsTable.vue`: viết lại thành khối dòng nguồn × cột PA (giới hạn nguồn, trả gửi, SL đã xử lý xanh/đỏ, Hợp đồng bán, gợi ý ô mua, khóa dòng không có hàng; giữ đổi hàng / sticky / phím)
- [x] `add.vue`: blankAllocs, mapper, totalAlloc, overContractRows, lỗi nguồn chặn lưu, xuất Excel (ma trận trải phẳng: nhóm cột theo nguồn), suy lại alloc cũ khi đổi loại
- [x] `HandlingSummaryTabs.vue`: đổi tên tab, tách tồn/mua ở đề nghị xuất kho
- [x] Copy demo mới vào `demos/` + cập nhật `demos/README.md`

## Phase 3 — Kiểm tra
- [x] `php -l` các file BE, chạy migration local
- [x] Kiểm tra cú pháp client (vue-template-compiler + babel parser — client không cài eslint)
- [ ] User test tay trên trình duyệt: các loại 1 / 2 / 3 / 4-6, phiếu cũ mở lại, đổi hàng, xuất Excel
- [x] ~~Khi BE trả số thật → bật `SOURCE_LIMITS_ON`~~ — đã bật 24/10/2026 (Phase 4)

## Phase 4 — Đối chiếu tab "Giải thích logic" của demo (24/10/2026)
- [x] `add.vue` overContractRows (banner vượt HĐ): so **Cần cung ứng** với SL còn lại (khối đổi: Σ Thay cho hàng gốc) — khớp ô đỏ trong bảng + demo §4, bỏ cách cộng cột HĐơn
- [x] `HandlingSummaryTabs.vue`: cột "SL tồn kho" ở PĐNXK / Nhu cầu mua = tổng tồn còn lại (trừ dòng trên cùng mã) như demo
- [x] Bỏ `HDDON_PURPOSES` không còn dùng (constants.js)
- [x] Kiểm tra cú pháp 4 file
- [x] Giới hạn nguồn + khóa dòng hết hàng (demo §2, §4): user chốt **bật luôn** `SOURCE_LIMITS_ON = true` dù BE còn trả cứng 0 → dòng tồn kho / KH vay đang luôn khóa, chỉ nhập Chốt mua thêm
- [x] Bỏ tooltip rê chuột ở ô khóa của bảng hàng ("Khách đang vay: không có hàng", "Trừ hàng KH vay chỉ lấy từ…")
- [x] Nguồn hết hàng không khóa ô nữa (user chốt): vẫn hiện ô nhập, nhập > 0 → ô đỏ + "Vượt SL xuất được / KH đang vay", chặn lưu; ô ngoài ma trận của loại phiếu vẫn xám
- [x] Chuyển "KH đang gửi: X" từ cột Tên thương mại xuống ngay dưới ô Xuất trả gửi cho KH (dòng nguồn đầu khối), đỏ khi vượt
- [x] ~~Tạm ẩn nhóm "Số liệu nguồn" của loại Nội bộ~~ — user đổi ý, đã mở lại như cũ (24/10/2026)
- [x] Nội bộ: chỉ comment 2 cột "SL đang mua" + "Số liệu tồn hợp đồng" (giữ "Số lượng đã tặng" khi có KH sử dụng + "Số lượng mượn")
- [ ] Nối số tồn kho / KH vay / KH gửi thật ở BE (chưa có nguồn dữ liệu trong hệ thống)

## Phase 5 — Popup đổi hàng chọn nhiều hàng thay thế (24/10/2026)
- [x] `GoodsPickerModal` (dùng chung, user đồng ý sửa): prop `multiple` (mặc định false) — chế độ swap + multiple dùng checkbox, emit `confirm-swap` là MẢNG; không bật thì giữ chọn 1 như cũ
- [x] PXL `add.vue` onSwapConfirm nhận mảng: 1 hàng → như cũ; ≥ 2 hàng → hàng đầu vào dòng đang đổi, hàng sau chèn cuối khối, TẤT CẢ SL = 0 / Thay cho hàng gốc = 0 / phân bổ trống (user chốt); bỏ qua hàng trùng hàng gốc / trùng hàng thay thế của khối (báo toast)
- [x] Đề xuất `add.vue` onSwapConfirm: như PXL (quantity = 0, swap_quantity = 0)
- [x] Đơn mua / HĐ mua: CHƯA bật — đang đổi 1 dòng → 1 hàng, không có khối nhiều hàng thay thế (báo user)
- [x] Kiểm tra cú pháp

### Checkpoint — 23/10/2026
Vừa hoàn thành: FE ma trận (bảng hàng, add.vue, tab tổng hợp, export), demo vào demos/
Đang làm dở: —
Bước tiếp theo: user test tay; nối số tồn kho / vay / gửi thật ở BE rồi bật SOURCE_LIMITS_ON
Blocked: số nguồn BE đang trả cứng 0 (Detail*Resource, ExposesSwapProduct, SupplyProposalService)
