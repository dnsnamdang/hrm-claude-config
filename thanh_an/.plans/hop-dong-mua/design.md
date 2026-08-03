# Hợp đồng mua (build thật) — Design tóm tắt

> Placeholder — sẽ fill sau khi user duyệt thiết kế. Nguồn: demo `demos/demo-lap-hop-dong-mua.html` + spec `docs/superpowers/specs/2026-07-13-lap-hop-dong-mua-design.md`.

@namdangit — 2026-07-20

## Mục tiêu
Dựng thật màn "Hợp đồng mua" (mua hàng của NCC) trong module Supply: danh sách + thêm/sửa + xem + duyệt. Nguồn hàng lấy từ Báo cáo nhu cầu mua hàng.

## Quyết định lớn (đã chốt với user)
- Full-stack (BE + FE), đặt trong module **Supply** (FE `pages/supply/purchase_contracts`).
- 4 màn: danh sách, thêm mới, xem/sửa, duyệt.
- Luồng duyệt **giống HĐ bán** (nháp=1 / chờ duyệt=2 / đã duyệt=3 / từ chối=4 / hủy=5; 1 endpoint store, status trong payload; sendNotification).
- Phân quyền **không phân cấp** (chỉ gate theo tên quyền).
- **Trừ nhu cầu bên báo cáo: để sau** — chừa sẵn con trỏ nguồn trên dòng hàng, chưa ghi ngược.

Chi tiết: xem spec.
