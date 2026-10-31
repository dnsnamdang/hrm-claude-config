# Yêu cầu hạch toán dịch vụ HDDV — Design (tóm tắt)

> @dangquang · nhánh `develop` (con của `gop_db`) · tạo 2026-10-30
> Spec chi tiết: `docs/superpowers/specs/gop-db/2026-10-30-wr-accounting-service-request-design.md`

## Mục tiêu
Port màn ERP "Yêu cầu hạch toán dịch vụ - HDDV" (`wr_accounting_service_requests`, phía **BÁN** dịch
vụ — chuỗi Bán Dịch vụ) sang HRM `/finance/wr-accounting-service-requests`. Bám ERP 1:1 về nghiệp
vụ, UI theo chuẩn HRM. Bản song sinh phía MUA đã port: `.plans/gop-db/buy-service-accounting-request`.

## Quyết định lớn (call của tôi 30/10/2026 — user "làm đi", đã opt-out hỏi)
- **1 loại** (HDDV = hợp đồng dịch vụ). Chi phí tính **sẵn từ hợp đồng** (trừ phụ lục PL_GIAM),
  màn chỉ-đọc chi phí; không có logic SL còn lại / giữ chéo.
- **Phân quyền 3 cấp** như ERP (tổng công ty / công ty / phòng ban) + quyền **Hạch toán dịch vụ
  HDDV** cho hành động Không duyệt. 4 quyền mới guard `api`, `type 23` (Bán hàng),
  group `Yêu cầu hạch toán dịch vụ HDDV`. KHÔNG dùng lại 'Kế toán kho' (guard web) của ERP.
- **Phân hệ chính Bán hàng** (`?type=all`, registry sale-hub có sẵn "YC hạch toán dịch vụ - HDDV");
  lối phụ Tài chính › Bán Dịch vụ (placeholder `finance.js:308` → gán link).
- **Status**: Đã duyệt(1), Chờ duyệt(2), Đang tạo(3→**xám**). Luồng trong màn: tạo → 2; Không
  duyệt → 3; sửa ở 3 rồi gửi lại → 2. Lên 1 là do phiếu Hạch toán (#2) — CHƯA port.
- **Sửa/Xóa**: status Đang tạo(3) + là người tạo; xóa cứng (xoá costs + phiếu).
- **Link màn CHƯA PORT để TRỐNG** (user chốt): "Số hợp đồng" (HĐ DV) + nút "Hạch toán chi phí"
  (phiếu #2) = placeholder vô hiệu, nối luồng khi port sau. (Bản MUA mở ERP — khác; chờ user chỉnh.)
- **Tạo chỉ từ HĐ DV** (ERP `create_link` comment out): create.vue nhận `?wr_service_contract_id=`;
  KHÔNG thêm nút tạo đứng-một-mình / picker HĐ. Entry từ màn HĐ DV = placeholder.
- **Không migration** (bảng ERP dùng chung); lịch sử qua `catalog_histories`.
- **Không bản in** (ERP voucher không có); có **Xuất Excel danh sách**.
- Khuôn: màn `buy-service-accounting-requests` (BE `Modules/Finance`, FE `pages/finance`).

## Hiện trạng dữ liệu / HRM
- Bảng `wr_accounting_service_requests` + `wr_accounting_service_request_costs`: ERP sở hữu, CHƯA có
  model/migration HRM (chỉ tham chiếu đọc ở `WrServiceContract.php:523`, `Cost.php:125`).
- `wr_service_contracts` đã có model HRM (Finance + CustomerCare) → đọc để lấy data tạo phiếu.
- Menu placeholder 4 mục "Bán Dịch vụ" sẵn ở `finance.js:302-313`.

## Lỗi ERP sửa khi port
Kiểm quyền server (ERP route approve chết, canView rộng); "Đang tạo" đỏ→xám; `delete()` ERP có
`dd($e)` rác; không ghi `''`/null sai cột; 409 khi status đổi; nhãn "Người tạo/Ngày tạo".
