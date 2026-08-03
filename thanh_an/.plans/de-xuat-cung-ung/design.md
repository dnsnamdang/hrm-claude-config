# Design tóm tắt — Phiếu đề xuất cung ứng (build thật)

> Phụ trách: @namdangit · Ngày: 2026-07-08 · Loại: **build thật (BE + FE)** — màn đầu tiên phân hệ Cung ứng
> Spec đầy đủ: `docs/superpowers/specs/2026-07-08-de-xuat-cung-ung-design.md`
> Demo tham chiếu luồng (không copy UI): `C:/Users/Legion/Downloads/de_xuat_cung_ung.html`

## Mục tiêu
Xây màn **Phiếu đề xuất cung ứng** — màn đầu tiên phân hệ Cung ứng. Người đề xuất lập & gửi phiếu
(mô tả nhu cầu + file đính kèm + tùy chọn danh mục hàng hóa) → nhóm quyền "Xử lý cung ứng hàng hóa"
nhận thông báo → Từ chối / (màn sau) Tạo phiếu xử lý cung ứng.

## Quyết định đã chốt
- Phạm vi: **trọn phía đề xuất** (list + tạo + chi tiết/sửa + gửi + từ chối). "Tạo phiếu xử lý" để màn sau.
- Backend: **module mới `Modules/Supply`**, API prefix `/api/v1/supply/supply-proposals`.
- Bảng hàng hóa: **đầy đủ cột số liệu nguồn** như demo; cột chưa có nguồn (tồn kho/đang mua/vay/gửi/đổi) tạm `0`, wire sau.
- Không phân quyền cấp (1 quyền xem, thấy tất cả). Xóa được **Nháp + Từ chối** (của mình).
- Trạng thái: **1 Nháp → 3 Đã gửi → 7 Từ chối / 9 Đã xử lý**.
- Thông báo: tái dùng `self_notifications`.
- UI theo convention PM (Bootstrap-Vue + Base components), tên đường dẫn **tiếng Anh** (`supply/supply_proposals`).

## 3 bảng
`supply_proposals` (phiếu) · `supply_proposal_products` (hàng hóa, tùy chọn) · `supply_proposal_files` (đính kèm).

## 3 quyền mới (id nối tiếp 511, group "Cung ứng")
512 Xem · 513 Lập · 514 Xử lý cung ứng hàng hóa.

## FE
Wire phân hệ (MenuSupply.js + layouts/default.vue + dashboard + tile link) · `supply_proposals/index.vue` (list)
· `supply_proposals/add.vue` (create/edit/show, 3 khối + popup chọn hàng + tab tham chiếu HĐ).
