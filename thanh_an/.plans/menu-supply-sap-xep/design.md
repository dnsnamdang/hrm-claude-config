# Design (tóm tắt) — Sắp xếp lại menu phân hệ Cung ứng

**Spec đầy đủ:** `docs/superpowers/specs/2026-08-10-menu-supply-sap-xep-design.md`

## Mục tiêu

Menu Cung ứng đang là 7 mục phẳng, lệch convention với các phân hệ khác (đều dùng `subItems`) và thứ tự không theo luồng nghiệp vụ. Gom lại thành 5 mục topbar, nhóm theo luồng.

## Cấu trúc chốt

```
Tổng quan
Phiếu đề xuất cung ứng          (link phẳng — quyền bên đề xuất)
Xử lý cung ứng ▾                (quyền "Xử lý cung ứng hàng hóa")
   ├ Danh sách đề xuất cung ứng
   └ Phiếu xử lý cung ứng
Mua hàng ▾
   ├ Hợp đồng mua
   └ Đơn mua hàng
Báo cáo ▾
   └ Báo cáo tổng hợp nhu cầu mua hàng
```

## Quyết định lớn

1. **Gom theo quyền, không gom theo đối tượng dữ liệu** — inbox đề xuất nằm ở nhóm "Xử lý cung ứng" (cùng quyền `Xử lý cung ứng hàng hóa` với phiếu xử lý), không nằm cạnh "Phiếu đề xuất cung ứng" (quyền khác). Mỗi dropdown vì thế đồng nhất quyền: hiện ra là có đủ mục con.
2. **Menu cha có `isShow`** — khác `MenuContract.js` (comment `isShow` ở cha) vốn để lọt dropdown rỗng khi user thiếu quyền.
3. **"Báo cáo" giữ dropdown dù 1 mục** — đồng bộ convention, thêm báo cáo sau không phải đổi cấu trúc.

## Phạm vi

Chỉ 1 file: `hrm-thanhan-client/utils/MenuSupply.js`. Không đụng route/page/component/BE, không migration.
