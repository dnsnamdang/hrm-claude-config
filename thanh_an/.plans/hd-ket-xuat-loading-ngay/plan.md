# Plan — HĐ đã kết xuất (Cung ứng): hiện loading ngay khi vào màn

> @khoipv — Bắt đầu 05/10/2026
> Màn: `hrm-thanhan-client/pages/supply/contract_render/index.vue`

## Vấn đề
Vào màn, bảng trống một lúc rồi mới hiện loading. Lý do: `isLoading` khởi tạo `false`, còn `mounted` lại `await loadCustomers()` (API khách hàng cho bộ lọc) rồi mới gọi `getData()` để bật loading.

## Phase 1 — FE
- [x] `isLoading` khởi tạo `true` → spinner hiện ngay lúc vào màn
- [x] `mounted`: gọi `loadCustomers()` song song, không await → không chặn việc tải bảng

### Checkpoint — 05/10/2026
Vừa hoàn thành: 2 task Phase 1
Đang làm dở:
Bước tiếp theo: user kiểm tra trên trình duyệt
Blocked:
