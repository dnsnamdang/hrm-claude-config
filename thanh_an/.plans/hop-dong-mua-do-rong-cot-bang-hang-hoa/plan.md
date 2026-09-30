# Plan — Chỉnh bề rộng cột bảng hàng hóa màn Lập hợp đồng mua

**Người phụ trách:** @khoipv
**Ngày:** 23/09/2026
**File chính:** `hrm-thanhan-client/pages/supply/purchase_contracts/components/ProductsTab.vue` (chỉ FE)
**Tham chiếu chuẩn:** `hrm-thanhan-client/pages/supply/purchase_orders/components/ProductsTab.vue` (màn Đơn mua hàng)

## Vấn đề (user báo qua ảnh chụp)
1. Bảng nhìn "xấu", bề rộng cột không giống màn Đơn mua hàng.
2. Cột **Mục đích mua (Phiếu đề xuất / KH / HĐ bán)** bị bóp → mỗi mục đích vỡ thành 3-4 dòng.
3. Cột **Tên hàng hóa**, dòng "Đã mua của: ..." bị cắt cụt (`ANOXY INTERNATIONA…`) và layout lệch.

## Nguyên nhân
- HĐ mua **không có** vùng cuộn giới hạn chiều cao + **không đông cứng** 3 cột đầu (Đơn mua hàng có).
- `.pp-line` để `flex-wrap: wrap` (Đơn mua hàng dùng `nowrap`) → mỗi dòng đề xuất tự bẻ.
- `td.cell-purpose` không chốt `min-width` → cột co lại theo bảng.
- `.sup-line` dùng `display:flex` + `text-overflow: ellipsis` → cắt tên NCC. Đơn mua hàng để block, cỡ chữ 11px.
- `.cell-name` min 260 / max 380 nhưng Đơn mua hàng chốt cứng 240px.
- `.cell-code` để monospace 11px (Đơn mua hàng đã bỏ, dùng font bảng).

## Task
- [x] T1. Thêm `.table-responsive` max-height + cuộn dọc như Đơn mua hàng
- [x] T2. Đông cứng 3 cột đầu (STT / Mã hàng / Tên hàng hóa) — thêm class `col-freeze` vào template + CSS sticky
- [x] T3. Chốt bề rộng cột Mục đích mua + đổi `.pp-line` sang `flex-wrap: nowrap`
- [x] T4. Sửa `.sup-line` (bỏ ellipsis, cho xuống dòng) + `.cell-name` về 240px
- [x] T5. Bỏ monospace ở `.cell-code`
- [x] T6. Kiểm tra hàng TỔNG CỘNG (colspan 6) còn khớp sau khi đông cứng cột

## Ket qua

Chi sua 1 file FE: `hrm-thanhan-client/pages/supply/purchase_contracts/components/ProductsTab.vue`
(khong dung BE). Da verify: `vue-template-compiler` parse template OK, `node-sass` bien dich SCSS OK.

### Thay doi cu the
| Muc | Truoc | Sau (khop man Don mua hang) |
|---|---|---|
| Vung cuon | khong co | `.table-responsive` max-height `calc(100vh - 200px)`, min-height 420px, cuon doc |
| 3 cot dau | cuon mat | dong cung sticky (STT 42 / Ma hang 96 / Ten hang 240) |
| Dong TONG CONG | `colspan=6` | tach `3 + 3`, o dau sticky de chu luon nhin thay |
| Cot Ten hang hoa | min 260 / max 380 | chot 240px |
| Dong "Da mua cua" | flex + ellipsis -> cat cut ten NCC | bo flex/ellipsis, cho xuong dong, font 11px |
| Cot Muc dich mua | khong chot width | `min-width: 460px` (ca th lan td) |
| `.pp-line` | `flex-wrap: wrap` -> vo 3-4 dong | `flex-wrap: nowrap` -> moi muc dich 1 hang |
| O nhap SL mua trong muc dich | 52px | 72px |
| Cot Ma hang | monospace 11px | dung font/co chu cua bang |

### Con lai
- [ ] Build lai client + hard refresh de xem tren UI

### Checkpoint - 23/09/2026
Vua hoan thanh: sua xong CSS + template `purchase_contracts/components/ProductsTab.vue`, verify parse/compile sach.
Dang lam do: khong co.
Buoc tiep theo: build lai client, hard refresh, mo man Lap hop dong mua > tab Hang hoa de doi chieu voi man Don mua hang.
Blocked:

### Bo sung - noi chieu cao bang (user yeu cau)
Ban dau de `calc(100vh - 260px)` / min 360px -> user bao xem duoc it dong qua.
Da noi thanh `calc(100vh - 200px)` / min 420px (them ~60px, tuong duong ~2-3 dong).
Van chua het chieu cao man hinh vi con phai chua cho footer nut Huy / Luu nhap / Luu va gui
o `PurchaseContractForm.vue`. Neu muon cao hon nua -> ha tiep so 200px.
