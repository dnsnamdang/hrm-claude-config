# Đồng bộ hàng tạm trong báo giá HRM → ERP — Tóm tắt

> Spec đầy đủ: `docs/superpowers/specs/2026-06-06-sync-hang-tam-design.md`

## Mục tiêu
Tại tab Báo giá (màn chi tiết dự án tiền khả thi), với báo giá **Trúng thầu** (`status=7`) có **hàng hóa nhập tay** (hàng tạm), bấm **"Gửi duyệt hàng tạm"** để:
1. **Chặng 1:** tạo phiếu `tmp_product_requests` + `tmp_products` trên ERP, notify người duyệt.
2. **Chặng 3:** ERP duyệt → sinh `products` thật → HRM kéo `product_id` về ghi lên dòng báo giá.

Là một phần của luồng đồng bộ báo giá lớn (firm sync **tạm tắt** ở phase này).

## Quyết định lớn
- Chỉ **hàng hóa** (`quotation_product_prices`, `erp_product_id IS NULL`); bỏ qua `service_items`.
- Id tham chiếu (model/brand/origin/unit) trên dòng báo giá **là id ERP** → map thẳng.
- Tạo phiếu ERP **qua API mới**, tái dùng model/logic ERP (mã `PYCDHT-`, status tính động, notification). KHÔNG insert mysql2.
- Chặng 3: **HRM kéo qua API ERP**; trigger = **tự kéo khi mở tab + nút thủ công**.
- Giá: chỉ đẩy **giá vốn + giá bán lẻ (price_type=1)** trên 1 đơn vị cơ bản; còn lại người duyệt ERP bổ sung.
- Hàng bị từ chối: chỉ **cảnh báo** FE.
- Người bấm = **sale của dự án**.

## Thay đổi chính
- **ERP:** migration thêm 4 cột `hrm_*` trên `tmp_product_requests`; 2 endpoint mới (`sync-from-hrm`, `approved-status`) + controller + service.
- **HRM:** migration thêm `erp_tmp_product_id` (dòng) + `tmp_sync_status`/`tmp_synced_at` (báo giá); service `TmpProductSyncService`; 2 endpoint (`send-tmp-approval`, `pull-tmp-approval`); FE nút + trạng thái ở tab báo giá; tắt nút firm sync.

## Trạng thái đồng bộ báo giá (HRM)
`null` (chưa gửi) → `syncing` ("Đang đồng bộ sang ERP") → `synced` ("Đã đồng bộ", khi mọi dòng có `erp_product_id`).

## Bổ sung khi triển khai (2026-06-06) — xem spec §13
- **Bugfix:** ERP `tmp_products` NOT NULL (brand/manufacture/origin → migration nullable + `product_cate='[]'`); `approved-status` chỉ trả `product_id` khi đã duyệt; guard map rỗng để gửi lỗi không kẹt `syncing`.
- **Mở rộng:** 2 nút header cấp dự án (`sendTmpApprovalForProject`/`pullTmpApprovalForProject` + cờ `tmp_can_send`/`tmp_can_pull`) + cột "Trạng thái đồng bộ" trong bảng; giữ nút per-row.
- **Quyết định:** 1 dự án = 1 báo giá trúng thầu (giữ rule `finalize`).
