# Plan: Lọc trong popup Chi tiết báo giá — màn detail-report

**@khoipv · 2026-07-09**

> Thêm 3 ô lọc **dạng nhập text** (contains, client-side) ngay trong popup
> "Chi tiết báo giá" để lọc danh sách hàng hóa (`modalItems`) đã load sẵn.
> Không gọi API — lọc trực tiếp trên dữ liệu popup.

## Phase 1 — Frontend (`pages/plan/detail-report/index.vue`)
- [x] `modalFilter` (product_code, producer_country, bid_contract_code) trong data
- [x] Computed `filteredModalItems` — lọc `modalItems` theo Mã hàng / Hãng-nước SX / Mã Gói thầu-HĐ
- [x] Hàng ô lọc (3 `b-form-input` trong `search-filter`, style filter chuẩn) bọc trong `b-collapse#modal-filters` + nút toggle "Bộ lọc"
- [x] Bảng render `filteredModalItems`; STT + footer đếm theo list đã lọc
- [x] Reset `modalFilter` khi mở/đóng popup

## Phase 2 — Verify
- [ ] Chạy thử lọc trên UI (chờ user verify)

---
### Checkpoint — 2026-07-09
Vừa hoàn thành: FE lọc popup (3 ô text, computed filteredModalItems)
Đang làm dở: không
Bước tiếp theo: user verify trên UI
Blocked:
