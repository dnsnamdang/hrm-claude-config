# Từ chối lập gói thầu — Design tóm tắt

> Người phụ trách: @khoipv
> Trạng thái: Đã chốt design, chờ viết plan chi tiết

## Mục tiêu
Bổ sung chức năng "Từ chối lập gói thầu" trên màn `bid_package/quotation` (Danh sách báo giá đã gửi thầu, status=7 DA_GUI_THAU). Người có quyền "Lập gói thầu" được từ chối, **bắt buộc nhập lý do**.

## Quyết định lớn
- **Không migration** — tái dùng cột `reason_deny` sẵn có; chỉ thêm const trạng thái trong code.
- Trạng thái mới: Quotation `TU_CHOI_LAP_GOI_THAU = 20`, Project `TU_CHOI_LAP_GOI_THAU = 19` (cùng nhãn "Từ chối lập gói thầu").
- Khi từ chối: báo giá → 20, dự toán → 19 (trạng thái cuối, không khôi phục).
- Endpoint mới `PUT /category/quotations/{quotation}/reject-bid`, quyền dùng chung "Lập gói thầu".
- Ghi `HistoryApprovedQuotation` + gửi notification cho người lập báo giá.
- Nút **chỉ** ở màn danh sách `bid_package/quotation/index.vue` (không làm trang chi tiết).

## Link spec chi tiết
`docs/superpowers/specs/2026-06-23-bid-package-quotation-reject-design.md`
