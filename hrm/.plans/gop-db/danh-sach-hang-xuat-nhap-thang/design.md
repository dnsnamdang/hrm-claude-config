# Danh sách hàng xuất nhập thẳng (ERP → HRM) — design

> Phụ trách: @khoipv · Bắt đầu: 2026-11-11 · Nhánh: `develop` (cả 2 repo, checkout ra từ `gop_db`)
> Spec chi tiết: `docs/superpowers/specs/gop-db/2026-11-11-danh-sach-hang-xuat-nhap-thang-design.md`

## Mục tiêu
Port màn ERP `warehouseInfo.productImportDirectDetails` ("Báo cáo tồn hàng nhập xuất thẳng theo nhân viên") sang
HRM `/finance/import-direct-stocks`. Màn CHỈ ĐỌC: tồn hàng nhập thẳng (`product_import_direct_details`, hàng về
thẳng tay nhân viên, không qua kho) gom Phòng ban → Nhân viên → Hàng.

## Menu (2 chỗ, giữ nhãn có sẵn)
- Tài chính › Báo cáo hàng tồn kho › "Báo cáo tồn hàng nhập xuất thẳng" (`finance.js`)
- Tra cứu › Thông báo › "Hàng xuất nhập thẳng" (`lookup.js`)
ERP: Thông báo › "Danh sách hàng xuất nhập thẳng" + Kế toán › Báo cáo hàng tồn kho — không tham số trên link.

## Quyết định (user chốt 2026-11-11)
1. Phân quyền theo cấp **y ERP**, mã `accounting.bao_cao_ton_hang_nhap_xuat_thang_theo_nhan_vien.view` (4 mức),
   thêm platform `hrm`. Không có quyền vẫn vào màn, thấy hàng của chính mình → route không gắn checkPermission, menu không `codes`.
2. Phân trang **theo phòng ban** (ERP theo dòng hàng → phòng bị cắt 2 trang, tổng phòng sai). Không sửa ERP.
3. Bảng **cây 3 tầng** + dòng TỔNG CỘNG, mặc định mở hết, thu/mở từng phòng / nhân viên.

## Khác ERP có chủ đích
- Nhân viên chưa gán phòng ban hiện ở nhóm "Chưa gán phòng ban" (ERP bỏ khỏi cây nhưng vẫn cộng vào tổng).
- Ô tìm nhanh `keyword` (mã/tên hàng) thay 2 ô Mã hàng / Tên hàng; ô Công ty chỉ hiện + chỉ được BE đọc với người xem mọi công ty.
- Cấp Phòng ban = phòng quản lý + phòng mình (ERP chỉ phòng quản lý) — như các màn HRM khác.
- Bản in có tiêu đề riêng (ERP mượn nhầm mẫu "Báo cáo thực hiện kế hoạch bán hàng"). Xuất Excel qua popup chọn trường.
