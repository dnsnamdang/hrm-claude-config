# Danh sách hàng xuất nhập thẳng (ERP → HRM) — plan

> Phụ trách: @khoipv · Nhánh: `develop` (cả 2 repo, checkout ra từ `gop_db`) — code CHƯA commit

## Chốt với user (2026-11-11)
- Phân quyền theo cấp **y ERP**: dùng lại mã `accounting.bao_cao_ton_hang_nhap_xuat_thang_theo_nhan_vien.view`
  (4 mức), thêm platform `hrm`. Không có quyền → chỉ thấy hàng của chính mình (route KHÔNG gắn checkPermission, y ERP).
- Phân trang **theo phòng ban** (ERP phân trang theo dòng hàng → phòng bị cắt 2 trang, tổng phòng sai) — không sửa ERP.
- Bảng **cây 3 tầng** Phòng ban → Nhân viên → Hàng, có dòng TỔNG CỘNG (khuôn cây `pages/finance/prepick-stocks`).

## Phase 1 — BE (`Modules/Finance`)
- [x] T1. Catalog `accounting.php`: thêm `hrm` vào `platforms` của mã trên
- [x] T2. `Services/ImportDirectStockReportService.php` — phạm vi y ERP, bộ lọc, cây phân trang theo phòng ban, meta, export, print
- [x] T3. `Http/Controllers/V1/ImportDirectStockController.php` (index / meta / export / print)
- [x] T4. Route `/v1/finance/import-direct-stocks` (CHỈ ĐỌC)
- [x] T5. Blade in `prints/import-direct-stock-list.blade.php` (A4 ngang, cây 3 tầng + Tổng cộng)
- [x] T6. Smoke test qua HTTP kernel (tinker) — đối chiếu tổng SL với query ERP

## Phase 2 — FE (`pages/finance/import-direct-stocks`)
- [x] T7. `index.vue` — SmartFilterPanel floating + V2BaseCompanyDepartmentFilter + cây 3 tầng + In / Xuất / Cấu hình cột
- [x] T8. `components/export-excel.js` — file cây như ERP, letterhead + khối ký + dòng Tổng cộng
- [x] T9. Menu: Tài chính › Báo cáo hàng tồn kho "Báo cáo tồn hàng nhập xuất thẳng" + Tra cứu › Thông báo "Hàng xuất nhập thẳng" → link HRM (giữ nhãn)
- [x] T10. Compile FE (vue-template-compiler + babel) + checklist grep skill erp-to-hrm-screen

### Checkpoint — 2026-11-11
Vừa hoàn thành: T1–T10. Smoke test BE (tinker, HTTP kernel + vai trò tạm trong transaction đã rollback):
không quyền → chỉ hàng của mình (NV 215: 416 = SUM DB); Tổng công ty → 542 = toàn bộ; Công ty → 502 = công ty 1,
lọc company_id bị bỏ qua đúng; Phòng ban → 497; tổng từng phòng = tổng dòng con. Compile FE + grep checklist sạch.
Đang làm dở: không
Bước tiếp theo: user mở trình duyệt `/finance/import-direct-stocks` bấm thử (lọc, thu/mở cây, phân trang, In, Xuất Excel);
deploy chạy `permission:catalog-sync` (đã thêm platform hrm — không đổi quyền ai).
Blocked:

## Phase 3 — Test Playwright (user yêu cầu 11/11, dừng giữa chừng theo yêu cầu user)
- [x] T11. Không quyền: bảng "Không có dữ liệu phù hợp", 1 request danh sách + 1 meta, nâng cao chỉ Thương hiệu / Hãng SX — PASS
- [x] T12. Quyền Tổng công ty (vai trò tạm id 100215, ĐÃ XOÁ theo id): 27/27 bước PASS — Tổng cộng 542, 10 phòng, STT 1/1.1/1.1.1,
      tổng phòng = tổng cộng, thu/mở phòng + nhân viên, 5 dòng/trang → trang 2 STT 6..10 (đúng 2 request), tìm nhanh chỉ gọi API khi Enter,
      không khớp → "Không có dữ liệu phù hợp", Làm mới về 542, đủ 6 ô lọc nâng cao, lọc Công ty CN Vinh → 12 (tự lọc, 1 request)
- [ ] T13. Chưa chạy (user dừng): rời màn rồi quay lại giữ bộ lọc, lọc Thương hiệu, Cấu hình cột, In, Xuất Excel
- Ghi chú: Chromium 1228 (Playwright) sập tab khi bấm Back của trình duyệt sau khi rời màn — chưa khoanh xong là do trình duyệt hay do màn
  (bộ nhớ đứng ~130MB). Ngoài phạm vi: màn Danh sách hàng giữ (`prepick-stocks/index.vue`) dùng `visibleExportFields` mà không khai
  `exportFieldsMixin` → [Vue warn] + popup Xuất không tick sẵn cột đang hiện. CHƯA sửa.

## Dữ liệu test (user yêu cầu 11/11)
- [x] T14. Thêm 13 dòng `product_import_direct_details` id **15872–15884** (`objectable_type = 'TEST_PW_IMPORT_DIRECT'`):
      NV 13 (DNS Admin, phòng 111) 5 mã hiện, tổng 15.5 (gồm mã SL lẻ 2.5, mã cộng 2 dòng = 3, 2 mã nhập rồi xuất về 0 / âm → ẩn);
      NV 236 (cùng phòng 111) 3 mã, tổng 9 — chỉ thấy khi có quyền Phòng ban trở lên. Đã gọi API bằng NV 13 → 15.5, đúng 5 mã.
      Dọn: `DELETE FROM product_import_direct_details WHERE id BETWEEN 15872 AND 15884 AND objectable_type='TEST_PW_IMPORT_DIRECT';`
- [x] T15. (user yêu cầu, chỉ dữ liệu local, không sửa code) Vai trò tạm **id 100216 "Quản trị (local)"** công ty 1, cấp
      `admin.phan_quyen.manage` (permission 5439), gán NV 13 → user-profile đã trả mã này, hiện menu Vai trò / Vai trò nhân viên.
      Nguyên nhân mất menu: vai trò Super admin 18 / 100002 / Giám đốc 100010 có `roles.company_id` NULL → PermissionChecker bỏ qua.
      Dọn: `DELETE FROM employee_has_roles WHERE role_id=100216; DELETE FROM role_has_permissions WHERE role_id=100216; DELETE FROM roles WHERE id=100216;`

### Checkpoint — 2026-11-11 (đóng)
Vừa hoàn thành: user tự test trình duyệt xong; commit + push develop (hrm-api `0b472de60`, hrm-client `56d08069e`) — chỉ file của màn này.
Đang làm dở: không
Bước tiếp theo: deploy chạy `permission:catalog-sync`; dọn dữ liệu test local (T14/T15) khi user báo.
Blocked:

## Phase 4 — Redmine #12137 (12/11/2026, @khoipv)
- [x] T16. Dropdown Thương hiệu / Hãng SX đổ CẢ danh mục `status = 1` như ERP (bỏ lọc "chỉ giá trị có hàng tồn") — BE `filterMeta`
- [x] T17. Nút Cấu hình cột theo chuẩn list-page: `V2BaseButton secondary size="sm"` (đang là `V2BaseIconButton size="lg"`)
- [x] T18. Đổi tên màn → "Báo cáo tồn hàng nhập xuất thẳng theo nhân viên" (tiêu đề màn + popup xem trước + tên sheet Excel)
- [x] T19. Ô chọn cấp bung trong tiêu đề cột Tên hàng: Đến phòng ban / Đến nhân viên / Đến hàng hóa (mặc định Đến hàng hóa)
- [x] T20. Thu hẹp cột để vừa màn nhỏ, không cuộn ngang
- [x] T21. Bản in: dòng ngày in nghiêng căn giữa dưới tiêu đề (bỏ bảng "Ngày in"); in đậm Tổng cộng / phòng / nhân viên (`!important` — CSS trang in đè `font-weight`)
- [x] T22. Excel: tên phòng + nhân viên căn trái (ô gộp ExcelJS dùng chung object style → vòng kẻ viền ghi đè căn giữa của cột ĐVT lên ô chủ)

### Checkpoint — 2026-11-12
Vừa hoàn thành: #12137 đủ 7 mục — BE `ImportDirectStockReportService::filterMeta` (danh mục status=1, local 1120 TH / 981 HSX),
bản in `import-direct-stock-list.blade.php` (dòng "Tính đến: …" nghiêng giữa + đậm !important), FE `index.vue` (tên màn, nút cấu hình
cột, ô chọn cấp, cột tổng 940px), `export-excel.js` (bỏ qua ô phụ vùng gộp — đã chạy thử: phòng/NV căn trái, TỔNG CỘNG giữa).
Đang làm dở: không
Bước tiếp theo: user mở trình duyệt kiểm ô chọn cấp + độ rộng cột ở màn 1366; chưa commit.
Blocked:

## Phase 5 — #12137 bổ sung mục 8, 9 (12/11/2026, @khoipv)
- [x] T23. (mục 8) ⓘ "MỤC ĐÍCH BÁO CÁO" ở `#title-suffix` bộ lọc — `ReportInfoTip` (khuôn Thẻ kho)
- [x] T24. (mục 9, chỉ điều tra trên dev) PXH-43223 = xuất thẳng loại 14, người lập phiếu Thu Trang (209, kế toán) nhưng YCXH-44387
      do Trần Văn Thắng (87, NVKD) lập. ERP `ProductExport::updateWarehouse` trừ tồn nhập thẳng của NGƯỜI LẬP YCXH; báo cáo chỉ
      hiện tồn > 0 (ERP `having qty > 0`, HRM giống). Dev: NV 209 và 87 đều 0 dòng, mã XM-XM-DDBUONGDOT 0 dòng → không phải lỗi báo cáo.
- [ ] T25. Lỗ hổng phát hiện thêm (CHƯA sửa, chờ user): HRM `Assign\ProductExportService` tạo PXH xuất thẳng KHÔNG trừ
      `product_import_direct_details` như ERP (:1256-1310) → tồn nhập thẳng trên báo cáo bị thừa sau khi xuất thẳng ở HRM.
