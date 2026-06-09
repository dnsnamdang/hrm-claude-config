# Design (tóm tắt) — Khách hàng thụ hưởng cuối cho Dự án TKT

- **Feature:** `prospective-project-end-customer` · @manhcuong · 2026-06-25
- **Spec đầy đủ:** `docs/superpowers/specs/2026-06-25-prospective-project-end-customer-design.md`

## Mục tiêu
Bổ sung **Khách hàng thụ hưởng cuối** bên cạnh Khách hàng trực tiếp trên dự án TKT. Khi KH trực tiếp là trung gian thương mại dịch vụ, Sale khai thêm KH cuối — sẵn sàng kế thừa cho Phiếu yêu cầu làm GP.

## Phạm vi Phase 1 (đợt này — KHÔNG đụng Ứng dụng)
1. Đổi thứ tự: Thông tin khách hàng **lên trước** Thông tin dự án.
2. Checkbox **"KH thương mại dịch vụ"** (`is_intermediary_customer`, default FALSE).
3. Phân vùng **KH thụ hưởng cuối** đầy đủ (chọn/thêm KH, Loại hình, Lĩnh vực, email, liên hệ) — hiện khi checkbox TRUE.
4. **Masking** SĐT KH cuối ở màn chi tiết.
5. **Icon (i) tooltip** cạnh Loại hình / Lĩnh vực (cả trực tiếp + cuối).
6. **Nguồn scope dự án**: theo KH cuối nếu có (fallback KH trực tiếp), copy snapshot KH trực tiếp vào cột benefit khi bỏ trống.

## Hoãn — Phase 2 (nhóm Ứng dụng)
Xóa Nhóm ngành/Nhóm giải pháp/Ứng dụng khỏi Thông tin dự án; trường Ứng dụng + lọc + cảnh báo rỗng trong phân vùng KH; phiếu thu thập theo ứng dụng; dời nút "Xem danh sách giải pháp" + đổi cột popup (Loại hình + cột "Khách hàng cuối").

## Quyết định chốt (2026-06-25)
- DB: thêm bộ cột `customer_benefit_*` + `is_intermediary_customer` (tận dụng 3 cột benefit cũ).
- FE: tách sub-component dùng chung `CustomerBlock.vue` (variant direct|benefit).
- Edge KH cuối chưa có scope → fallback KH trực tiếp.
- KHÔNG thêm permission mới, KHÔNG đụng git.
