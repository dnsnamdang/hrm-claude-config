# Phân trang popup chọn hàng hóa — Phiếu đề xuất cung ứng

**Người phụ trách:** @khoipv
**Ngày bắt đầu:** 22/09/2026

## Mục tiêu

Popup "Chọn hàng hóa từ danh mục" (`pages/supply/supply_proposals/components/GoodsPickerModal.vue`)
đang cắt cứng 200 dòng (`displayLimit`) rồi báo "gõ từ khóa để lọc thu hẹp" → thay bằng phân trang FE
giống popup chọn hàng của màn Hợp đồng mua (`supply/purchase_contracts/components/GoodsPickerModal.vue`).

**Lưu ý:** API `goods-pool` trả toàn bộ pool 1 lần → lọc + phân trang đều ở FE, KHÔNG sửa BE.

## Quyết định

| Điểm | Chốt |
|---|---|
| Nguồn dữ liệu | Giữ nguyên prop `items` (goods-pool trả 1 lần) — không đụng BE |
| Số dòng/trang | Mặc định **25** (user chốt 22/09), options `PAGE_OPTIONS` ([10, 25, 50, 100]) |
| STT | Chạy liên tục theo trang: `(currentPage - 1) * perPage + i + 1` |
| Checkbox đầu bảng | Thao tác trên **trang hiện tại** (giống popup HĐ mua) |
| Nút "Chọn tất cả" ở footer | Thao tác trên **toàn bộ dòng đã lọc** (mọi trang) — đúng nghĩa tên nút |
| Giữ lựa chọn khi đổi trang | Có — `selected` là Set theo `_idx` của pool gốc, không phụ thuộc trang |
| Về trang 1 | Khi đổi từ khóa / HĐ / phân loại / "chỉ hàng còn SL" / số dòng mỗi trang / mở lại popup |

## Task

### FE — `pages/supply/supply_proposals/components/GoodsPickerModal.vue`
- [x] Import `PAGE_OPTIONS` từ `../constants`
- [x] `data()`: bỏ `displayLimit`, thêm `currentPage: 1`, `perPage: 25`, `pageOptions: PAGE_OPTIONS`
- [x] `computed.displayed`: `slice((currentPage-1)*perPage, ...+perPage)` thay cho `slice(0, displayLimit)`
- [x] Thêm `computed.selectableAll` — toàn bộ dòng đã lọc & chưa bị khóa (`isExcluded`), cho nút footer
- [x] Template: STT tính theo trang
- [x] Template: bỏ dòng "Hiển thị 200/N — gõ từ khóa để lọc thu hẹp", giữ dòng "Không tìm thấy..."
- [x] Template: thêm khối `.paging` (tổng bản ghi + `b-form-select` + `b-pagination`) ngay dưới bảng, NGOÀI vùng cuộn `.goods-list`
- [x] `watch`: keyword / contractFilter / importTypeFilter / onlyRemaining / perPage → `currentPage = 1`
- [x] `watch.visible`: reset thêm `currentPage = 1`
- [x] Footer: nút "Chọn tất cả" / "Bỏ chọn tất cả" dùng `selectableAll`; text đếm ghi rõ "(tính cả các trang)"
- [x] CSS: thêm block `.paging` (khai báo lại vì modal render ngoài `.default-layout`)

### Verify
- [x] Compile SFC sạch — `vue-template-compiler` 0 lỗi template, script parse OK
- [x] Smoke test logic bằng Node (47 dòng, 5 dòng khóa): trang 5 ra 7 dòng STT bắt đầu 41; `selectableAll` = 42; "Chọn tất cả" tick 42 dòng mọi trang; đổi trang giữ tick; lọc từ khóa ra 9 dòng gọn 1 trang
- [ ] @khoipv test UI: đổi trang giữ tick, lọc về trang 1, STT liên tục, "Chọn tất cả" bắt mọi trang,
      dòng "đã thêm" vẫn bị khóa, tick nhiều dòng cùng mã trong 1 HĐ vẫn cộng dồn đúng

## Không đụng

- BE `SupplyProposalService::goodsPool()` và API `goods-pool`
- Logic gộp dòng `onPickConfirm()` ở `add.vue` (chỉ nhận mảng đã chọn, không quan tâm trang)
- 3 popup chọn hàng của màn khác (`purchase_orders`, `purchase_contracts`, `acceptance_report`)

### Checkpoint — 22/09/2026
Vừa hoàn thành: Phân trang FE cho popup chọn hàng hóa màn đề xuất cung ứng — bỏ `displayLimit: 200`,
thêm `currentPage`/`perPage`/`pageOptions`, khối `.paging` dưới bảng, STT liên tục theo trang,
reset trang khi đổi bộ lọc, nút "Chọn tất cả" ở footer bắt mọi trang (checkbox đầu bảng vẫn theo trang).
Verify: compile SFC sạch + smoke test logic bằng Node đạt.
Đang làm dở: không có — code-complete.
Bước tiếp theo: build lại client, @khoipv hard refresh và test UI màn `supply/supply_proposals/add` → nút Chọn hàng hóa.
Blocked: không có.

### Checkpoint — 22/09/2026 (đổi mặc định 25 dòng/trang)
User chốt mặc định 25 thay vì 10 → sửa `perPage: 25` trong `data()` của `GoodsPickerModal.vue`
(`pages/supply/supply_proposals/components`, dòng 163). Options dropdown giữ nguyên 10/25/50/100.
Bước tiếp theo: build lại client, hard refresh, test UI.
