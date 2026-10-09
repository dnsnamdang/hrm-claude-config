# Fix: thị trường HĐ tính theo TỈNH KHÁCH HÀNG (không phải nơi giao hàng)

## Bối cảnh
Báo cáo `plan-department-by-employee`. Khách báo NV178 (Nguyễn Thị Phương Thùy) có HĐ T7 ngoài KH không hiện.
- HĐ khách BHT: khách ở Ninh Bình(41) NGOÀI KH T7[2,24], nhưng giao tới Hà Nội(2) TRONG KH.
- Root: commit 06d160ea (19/05/2026) đổi tỉnh thị trường từ `c.province_id` → `COALESCE(dp.province_id, c.province_id)` (ưu tiên NƠI GIAO). Mục đích lần đó chỉ để GẮN TÊN TỈNH cho dòng ngoài KH đang trống (NV99 T4, dòng 1.3.7) — nhưng sửa lố sang đổi cả phân loại in/out.

## Quyết định (user chốt)
Thị trường = TỈNH KHÁCH HÀNG là chính, nơi giao hàng chỉ FALLBACK khi tỉnh KH null.
→ Đảo thứ tự COALESCE: `COALESCE(c.province_id, dp.province_id)` + name `COALESCE(provinces.name, dp_prov.name)`.
→ Thoả cả 2: BHT tính theo khách=Ninh Bình→ngoài KH; dòng tỉnh KH null vẫn fallback nơi giao để hiện tên.

## Tasks
- [x] Swap 9 chỗ province_id + 2 chỗ province_name sang customer-first. php -l sạch. Backup: scratchpad/PlanImplement.bak.php
- [x] Verify NV178 T7: prov_out=1, dòng Ninh Bình(41) in_plan=false + tên 'Tỉnh Ninh Bình'. ✓
- [x] Verify NV99 T4: Hưng Yên(24) out vẫn hiện có tên; 5 tỉnh in-plan đều có tên. Không phá. ✓
- [ ] User reload xác nhận.

## Lưu ý
- Chưa commit (master). Đây là file report dùng chung — gộp cùng fix Nghệ An (fix-plan-department-market-out-ke-hoach-phong) chờ commit.
- Dòng trống 1.3.7 (HĐ dịch vụ WR không có tỉnh cả 2 phía) là vấn đề RIÊNG, swap không phá thêm.
