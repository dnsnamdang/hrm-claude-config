# Design — PXL hiển thị SL đã xử lý của các phiếu trước + chặn vượt đề xuất

@khoipv — Bắt đầu 01/10/2026 · Spec đầy đủ: [docs/superpowers/specs/2026-10-01-pxl-hien-thi-da-xu-ly-phieu-truoc-design.md](../../docs/superpowers/specs/2026-10-01-pxl-hien-thi-da-xu-ly-phieu-truoc-design.md)

- **Vấn đề:** 1 đề xuất lập nhiều PXL. Người lập sau chỉ thấy SL đặt đơn = phần còn lại (VD 10), không biết SL đề xuất gốc (20),
  không biết phiếu trước xử lý thế nào; nhập vượt vẫn lưu được (cả FE lẫn BE không chặn).
- **Hiển thị (chốt 02/10/2026 — thay bản 01/10):** ô Đặt đơn dòng giữ A thuộc đề xuất KHÓA (= còn lại theo đề xuất lúc lập; dòng đổi B + hàng chọn thêm vẫn nhập), chỉ 1 icon ⓘ khi có PXL khác, popover đầu ghi "Đề xuất · Đã xử lý · Còn". ~~Bản 01/10:~~ ô Đặt đơn `[10] / 20` + "Đã xử lý 10 ⓘ · Còn 10"; rê chuột ⓘ → popover liệt kê PXL khác
  (mã · người lập · ngày · trạng thái · cách phân bổ + SL, đổi hàng ghi rõ B thay cho bao nhiêu A). Khối đổi hàng đặt ở ô "Thay cho hàng gốc".
- **Chặn cứng khi gửi chính thức** (Lưu nháp không kiểm tra), FE + BE:
  - L1: mỗi hàng gốc A thuộc đề xuất — Σ **phân bổ** quy về A (dòng đổi: Thay cho A × phân bổ / Đặt đơn B) ≤ còn lại theo đề xuất. (Sửa đổi 02/10/2026 — trước đây so Đặt đơn; ô hiển thị "Phân bổ x / y".)
  - L2: mỗi dòng — Σ phân bổ ≤ Đặt đơn.
  - Đổi hàng cũng chặn (bỏ banner vàng "vẫn lưu được"); cảnh báo vượt HĐ giữ nguyên chỉ cảnh báo.
- **BE:** `SupplyProposalService::handledHistoryByProduct()` (mới) → expose `sl_de_xuat_a`, `sl_da_xu_ly_a`, `lich_su_xu_ly`
  ở `DetailSupplyProposalResource` + `DetailSupplyHandlingResource`; `SupplyHandlingService::guardProposalLimit()` (mới) gọi trong
  store/update, `lockForUpdate` đề xuất để 2 người lưu cùng lúc chạy tuần tự. Không migration.
- **FE:** `HandlingGoodsTable.vue` (x / y, popover, ô đỏ) + component mới `HandledHistoryPopover.vue`; `add.vue` (map field mới,
  computed L1 thay `overProposalRows`, `submit` chặn khi có lỗi).
- **Giữ nguyên:** Nháp / Từ chối duyệt không tính; `syncHandledStatus`, duyệt PXL nội bộ, export Excel.
