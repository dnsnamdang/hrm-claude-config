# Design tóm tắt — Xử lý cung ứng (build thật)

> Phụ trách: @namdangit · Ngày: 2026-07-08 · Loại: **build thật (BE + FE)** — màn thứ 2 phân hệ Cung ứng
> Spec đầy đủ: `docs/superpowers/specs/2026-07-08-xu-ly-cung-ung-design.md`
> Demo tham chiếu luồng: `C:/Users/Legion/Downloads/xu_ly_cung_ung.html`

## Quyết định đã chốt
- Đề xuất → **mô hình phản hồi**: 1 đề xuất nhận nhiều phiếu xử lý + nhiều từ chối; trạng thái xử lý SUY RA (Chờ/Đang xử lý/Đã từ chối).
- Phiếu con (xuất kho/mua/gửi/vay): **lưu phân bổ + tab tổng hợp read-only**, chưa sinh chứng từ thật.
- **Có duyệt** cho phiếu xử lý loại nội bộ (BGĐ, quyền 515); loại KH không cần.
- Số liệu nguồn tạm 0 (như đề xuất); validate vượt đặt đơn + vượt HĐ (bỏ vượt kho).
- Sửa/xóa phiếu xử lý: owner, khi chưa chốt (KH: Đã lập vẫn sửa; nội bộ: chỉ khi Chờ duyệt).
- **3 màn tách riêng**: Phiếu đề xuất (người ĐX, đã có) · Danh sách đề xuất — inbox xử lý · Phiếu xử lý.

## Refactor đề xuất
- Bỏ set status terminal 7/9; reject → tạo `supply_proposal_rejections`; thêm accessor `handle_status`; đổi `is_can_delete`.
- Resource đề xuất thêm `handle_status*` + `responses` (gộp phiếu xử lý + từ chối).

## Bảng mới
`supply_handlings` (PXL) · `supply_handling_products` (9 cột phân bổ + dat_don) · `supply_proposal_rejections`.

## Quyền
Tái dùng 514 (xử lý + từ chối) + thêm **515 Duyệt phiếu xử lý cung ứng**.

## FE
Menu +2 mục · Inbox `supply_proposals/inbox.vue` · List+form `supply_handlings/{index,add}.vue` (bảng phân bổ theo loại + tabs tổng hợp) · bổ sung khối "Phản hồi xử lý" ở chi tiết đề xuất.
