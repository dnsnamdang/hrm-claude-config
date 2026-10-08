# Design — Tiếp nhận thông tin HĐ đã kết xuất (Cung ứng)

**Người phụ trách:** @khoipv · **Ngày:** 05/10/2026 · **Trạng thái:** đã viết spec, chờ user review

> Spec đầy đủ: [docs/superpowers/specs/2026-10-05-tiep-nhan-hd-ket-xuat-design.md](../../docs/superpowers/specs/2026-10-05-tiep-nhan-hd-ket-xuat-design.md)

## Mục tiêu

Ghi nhận **ai đang tiếp nhận thông tin** từng HĐ đã kết xuất sang Cung ứng, kèm lịch sử tiếp nhận / hủy.
Thao tác được ở màn **Hợp đồng đã kết xuất** và màn **chi tiết HĐ** (chỉ khi đi từ màn kết xuất, `?from=supply_render`).

## Các quyết định lớn

| # | Quyết định |
|---|---|
| 1 | Mỗi HĐ **1 người tiếp nhận**; người đó **tự hủy** được → HĐ mở lại cho người khác |
| 2 | **Ai cũng tiếp nhận được**, không quyền, không phạm vi |
| 3 | Không ràng buộc lập phiếu đề xuất; không ghi chú; không thông báo; không bộ lọc |
| 4 | Lưu: 2 cột `contracts.supply_received_by/_at` + bảng `contract_supply_receive_histories` (action 1/2) |
| 5 | Chống bấm đồng thời bằng update có điều kiện `WHERE supply_received_by IS NULL`, dùng `DB::table` để không đổi `updated_at` HĐ |
| 6 | 3 API trong module Supply: `receive`, `cancel-receive`, `receive-info`; không sửa resource phân hệ Hợp đồng |
| 7 | FE: cột "Người tiếp nhận" + link Lịch sử; nút Tiếp nhận / Hủy trong cột Thao tác (≤ 3 nút); popup lịch sử dùng chung |
