# SDD ledger — plan: ERP/.plans/tach-quyen-truong-phong-ke-toan/plan.md

Executor: inline (executing-plans). Không commit/push (chưa được phép).
Pre-flight: tất cả task 2-4 consume `TruongPhongKeToanSplitMap` (Task 1). Không xung đột — Task 1 trước.

Task 1: complete — Map `TruongPhongKeToanSplitMap` + 2 entry Catalog accounting.php (sau mã cũ). Test `TruongPhongKeToanSplitMapTest` 4/4 xanh. Không commit.
Task 2: complete — màn ① Phiếu xuất giữ: re-point 6 chỗ (WarehousePrepickRequest:248,270 + HomeController:2140,2143 + topmenubar_old.blade:1439,1454) → `..._phieu_xuat_giu.approve`; fixture MAP +2 dòng. Test `TruongPhongKeToanSplitPhieuXuatGiu` (2) + `...RbacFixture` (1) xanh. Giữ nguyên toán hạng OR (BKS/phiếu hàng giữ/is_warehouse_accountant).
Task 2: Ruling — assert OR cho HomeController chỉ còn `finance.giu_hang_ban_kiem_soat.approve` (file không có `finance.phieu_hang_giu.view`, khác WarehousePrepickRequest) — chỉ sửa test cho khớp thực tế, hành vi code không đổi.
Task 3: complete — màn ② ĐNXK: re-point WarehouseExportRequest:1033 (canView) → `..._de_nghi_xuat_kho.view` (chỉ đổi mã, không đổi hành vi). Test `TruongPhongKeToanSplitDeNghiXuatKho` 1/1 xanh.
Task 4: complete — lệnh `rbac:grant-truong-phong-ke-toan-split` (RbacGrantTruongPhongKeToanSplitCommand, mirror KeToanMuaHang 1→2 mã, CSV cap-ma/doi-chieu-truong-phong-ke-toan). Test `TruongPhongKeToanSplitGrantWiring` 1/1 xanh.
Task 4: Ruling — needle phủ định trong wiring test đổi từ `KeToanSplitMap::` sang dòng `use App\Support\Permissions\KeToanSplitMap;`: tên lớp hợp lệ `TruongPhongKeToanSplitMap` CHỨA chuỗi con `KeToanSplitMap`, needle cũ bắt nhầm chính Map của đợt này. Sửa test, code không đổi. Cost nếu sai: ~0 (chỉ là guard chống tham chiếu nhầm Map đợt khác, dòng `use` phân biệt đủ).
Suite đầy đủ `--filter TruongPhongKeToanSplit`: 9/9 xanh (26 assertions). php -l 7 file PHP đụng tới: sạch. Chưa commit/push.

Final review: reviewer độc lập (opus, fresh context), đọc package + mở file nguồn ERP tới gốc + git grep HEAD + so khuôn KeToanMuaHang + php -l. Kết quả: Critical 0 · Important 0 · Minor 4 (chỉ ghi chú, KHÔNG cần sửa). 6 hằng số nghiệp vụ đều ĐẠT; R1+R2 đều xác nhận ĐÚNG. git grep HEAD = đúng 7 usage mã cũ, khớp 6+1 chỗ re-point; sau sửa grep mã cũ trong code ERP = rỗng.
Final: minor (deferred): ánh xạ mã↔màn đúng ngữ nghĩa (canView→de_nghi_xuat_kho.view; 6 điểm luồng phiếu xuất giữ→phieu_xuat_giu.approve).
Final: minor (deferred): holder mã cũ nhận CẢ 2 mã mới — đúng mục tiêu "không ai mất quyền" (1 cờ gộp cũ bật cả 2 màn).
Final: minor (deferred): history company NV cấp thẳng dùng company_employees.min(company_id) — kế thừa y nguyên KeToanMuaHang đã rollout.
Final: minor (deferred): catalog-sync là tiền đề; lệnh grant đã tiền kiểm chặn chạy sớm — chỉ nhắc rollout đúng thứ tự sync → grant → (deprecate sau).
Không fix pass (không Critical/Important). KHÔNG commit/push (user cấm). Ledger giữ lại (quy ước .plans của project), KHÔNG xoá workspace.
