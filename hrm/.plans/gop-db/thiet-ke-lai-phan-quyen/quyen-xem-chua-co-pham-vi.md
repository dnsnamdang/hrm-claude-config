# 107 quyền "Xem" chưa có phạm vi — phân loại (@cuong61n, 18/11/2026)

Nguồn: bảng `permissions` (kind = view, allowed_scopes rỗng) trên DB local nhánh gop_db. **Phân loại là ĐỀ XUẤT dựa trên tên quyền + Catalog, chưa kiểm từng màn BE** — chờ user duyệt trước khi sửa Catalog.

Tóm tắt: A = 59, B = 18, C = 22, D = 8

**Điều kiện khi thêm phạm vi cho 1 quyền Xem:** (1) BE của màn phải thật sự lọc theo phạm vi (PermissionChecker), nếu không ô chọn phạm vi chỉ là hình thức; (2) vai trò đang giữ quyền (scope NULL) phải backfill 1 mức cố định để không đổi hành vi hiện có; (3) sửa Catalog + `permission:catalog-sync` (không đổi `code`).


## A. KHÔNG nên có phạm vi (danh mục / cấu hình dùng chung) (59)

| Phân hệ | Chức năng | Mã quyền | Tên quyền | Lý do |
|---|---|---|---|---|
| Công việc | Danh mục | `assign.danh_muc_cau_hoi_khao_sat.view` | Xem danh mục câu hỏi khảo sát | Danh mục dùng chung toàn hệ thống |
| Công việc | Danh mục | `assign.danh_muc_linh_vuc_cong_ty_kinh_doanh.view` | Xem danh mục lĩnh vực Công ty kinh doanh | Danh mục dùng chung toàn hệ thống |
| Công việc | Danh mục | `assign.danh_muc_linh_vuc_khach_hang.view` | Xem danh mục lĩnh vực khách hàng | Danh mục dùng chung toàn hệ thống |
| Công việc | Danh mục | `assign.danh_muc_loai_tai_lieu.view` | Xem danh mục loại tài liệu | Danh mục dùng chung toàn hệ thống |
| Công việc | Danh mục | `assign.danh_muc_nhom_linh_vuc_khach_hang.view` | Xem danh mục nhóm lĩnh vực khách hàng | Danh mục dùng chung toàn hệ thống |
| CSKH sau bán | Cấp dịch vụ bảo dưỡng | `customer_care.cap_dich_vu_bao_duong.view` | Xem cấp dịch vụ bảo dưỡng | Danh mục dùng chung toàn hệ thống |
| CSKH sau bán | Dịch vụ sửa chữa và chi phí khác | `customer_care.dich_vu_sua_chua_va_chi_phi_khac.view` | Xem dịch vụ sửa chữa và chi phí khác | Danh mục dùng chung toàn hệ thống |
| CSKH sau bán | Ghi chú kiểm tra bảo dưỡng | `customer_care.ghi_chu_kiem_tra_bao_duong.view` | Xem ghi chú kiểm tra bảo dưỡng | Danh mục dùng chung toàn hệ thống |
| CSKH sau bán | Serial thiết bị làm dịch vụ | `customer_care.danh_muc_serial_thiet_bi_lam_dich_vu.view` | Xem danh mục serial thiết bị làm dịch vụ | Danh mục dùng chung toàn hệ thống |
| CSKH trước bán | Danh mục | `presale.danh_muc_giai_doan_du_an.view` | Xem danh mục giai đoạn dự án | Danh mục dùng chung toàn hệ thống |
| CSKH trước bán | Danh mục | `presale.danh_muc_hang_muc_du_an.view` | Xem danh mục hạng mục dự án | Danh mục dùng chung toàn hệ thống |
| CSKH trước bán | Danh mục | `presale.danh_muc_nguyen_nhan_that_bai_du_an.view` | Xem danh mục nguyên nhân thất bại dự án | Danh mục dùng chung toàn hệ thống |
| CSKH trước bán | Danh mục | `presale.danh_muc_nhom_giai_phap.view` | Xem danh mục nhóm giải pháp | Danh mục dùng chung toàn hệ thống |
| CSKH trước bán | Danh mục | `presale.danh_muc_nhom_nganh.view` | Xem danh mục nhóm ngành | Danh mục dùng chung toàn hệ thống |
| CSKH trước bán | Danh mục | `presale.danh_muc_ung_dung.view` | Xem danh mục ứng dụng | Danh mục dùng chung toàn hệ thống |
| CSKH trước bán | Danh mục | `presale.danh_muc_vai_tro_du_an.view` | Xem danh mục vai trò dự án | Danh mục dùng chung toàn hệ thống |
| Danh mục dùng chung | Biển số xe | `master_data.danh_muc_bien_so_xe.view` | Xem danh mục biển số xe | Danh mục dùng chung toàn hệ thống |
| Danh mục dùng chung | Chính sách kinh doanh | `master_data.danh_muc_chinh_sach_kinh_doanh.view` | Xem danh mục chính sách kinh doanh | Danh mục dùng chung toàn hệ thống |
| Danh mục dùng chung | Chương | `master_data.danh_muc_chuong.view` | Xem danh mục chương | Danh mục dùng chung toàn hệ thống |
| Danh mục dùng chung | Code đặt hàng | `master_data.danh_muc_code_dat_hang.view` | Xem danh mục code đặt hàng | Danh mục dùng chung toàn hệ thống |
| Danh mục dùng chung | Danh mục xe | `master_data.danh_muc_xe.view` | Xem danh mục xe | Danh mục dùng chung toàn hệ thống |
| Danh mục dùng chung | Dòng xe | `master_data.danh_muc_dong_xe.view` | Xem danh mục dòng xe | Danh mục dùng chung toàn hệ thống |
| Danh mục dùng chung | Đặc tính sản phẩm | `master_data.danh_muc_dac_tinh_san_pham.view` | Xem danh mục đặc tính sản phẩm | Danh mục dùng chung toàn hệ thống |
| Danh mục dùng chung | Đời xe | `master_data.danh_muc_doi_xe.view` | Xem danh mục đời xe | Danh mục dùng chung toàn hệ thống |
| Danh mục dùng chung | Đơn vị thuộc tính | `master_data.danh_muc_don_vi_thuoc_tinh.view` | Xem danh mục đơn vị thuộc tính | Danh mục dùng chung toàn hệ thống |
| Danh mục dùng chung | Đơn vị thuộc tính | `master_data.don_vi_thuoc_tinh.view` | Xem đơn vị thuộc tính | Danh mục dùng chung toàn hệ thống |
| Danh mục dùng chung | Đơn vị tính | `master_data.danh_muc_don_vi_tinh.view` | Xem danh mục đơn vị tính | Danh mục dùng chung toàn hệ thống |
| Danh mục dùng chung | File đính kèm | `master_data.danh_muc_file_dinh_kem.view` | Xem danh mục file đính kèm | Danh mục dùng chung toàn hệ thống |
| Danh mục dùng chung | Hãng sản xuất | `master_data.danh_muc_hang_san_xuat.view` | Xem danh mục hãng sản xuất | Danh mục dùng chung toàn hệ thống |
| Danh mục dùng chung | Hãng xe | `master_data.danh_muc_hang_xe.view` | Xem danh mục hãng xe | Danh mục dùng chung toàn hệ thống |
| Danh mục dùng chung | Lái xe ngoài | `master_data.danh_muc_lai_xe_ngoai.view` | Xem danh mục lái xe ngoài | Danh mục dùng chung toàn hệ thống |
| Danh mục dùng chung | Loại sản phẩm | `master_data.danh_muc_loai_san_pham.view` | Xem danh mục loại sản phẩm | Danh mục dùng chung toàn hệ thống |
| Danh mục dùng chung | Loại xe | `master_data.danh_muc_loai_xe.view` | Xem danh mục loại xe | Danh mục dùng chung toàn hệ thống |
| Danh mục dùng chung | Mã màu | `master_data.danh_muc_ma_mau.view` | Xem danh mục mã màu | Danh mục dùng chung toàn hệ thống |
| Danh mục dùng chung | Model | `master_data.danh_muc_model.view` | Xem danh mục model | Danh mục dùng chung toàn hệ thống |
| Danh mục dùng chung | Model xe | `master_data.danh_muc_model_xe.view` | Xem danh mục model xe | Danh mục dùng chung toàn hệ thống |
| Danh mục dùng chung | Mục | `master_data.danh_muc_muc.view` | Xem danh mục mục | Danh mục dùng chung toàn hệ thống |
| Danh mục dùng chung | Nhiên liệu | `master_data.danh_muc_nhien_lieu.view` | Xem danh mục nhiên liệu | Danh mục dùng chung toàn hệ thống |
| Danh mục dùng chung | Nhóm chức năng | `master_data.danh_muc_nhom_chuc_nang.view` | Xem danh mục nhóm chức năng | Danh mục dùng chung toàn hệ thống |
| Danh mục dùng chung | Nhóm khách hàng | `master_data.nhom_khach_hang.view` | Xem nhóm khách hàng | Danh mục dùng chung toàn hệ thống |
| Danh mục dùng chung | Nhóm sản phẩm | `master_data.danh_muc_nhom_san_pham.view` | Xem danh mục nhóm sản phẩm | Danh mục dùng chung toàn hệ thống |
| Danh mục dùng chung | Quản lý lĩnh vực | `master_data.linh_vuc.view` | Xem lĩnh vực | Danh mục dùng chung toàn hệ thống |
| Danh mục dùng chung | Quản lý nhóm hàng hóa | `master_data.nhom_hang_hoa.view` | Xem nhóm | Danh mục dùng chung toàn hệ thống |
| Danh mục dùng chung | Tải trọng xe | `master_data.danh_muc_tai_trong_xe.view` | Xem danh mục tải trọng xe | Danh mục dùng chung toàn hệ thống |
| Danh mục dùng chung | Thuế suất | `master_data.danh_muc_thue_suat.view` | Xem danh mục thuế suất | Danh mục dùng chung toàn hệ thống |
| Danh mục dùng chung | Thuộc tính | `master_data.danh_muc_thuoc_tinh.view` | Xem danh mục thuộc tính | Danh mục dùng chung toàn hệ thống |
| Danh mục dùng chung | Thương hiệu | `master_data.danh_muc_thuong_hieu.view` | Xem danh mục thương hiệu | Danh mục dùng chung toàn hệ thống |
| Danh mục dùng chung | Tiểu mục | `master_data.danh_muc_tieu_muc.view` | Xem danh mục tiểu mục | Danh mục dùng chung toàn hệ thống |
| Danh mục dùng chung | Tính chất hàng hóa | `master_data.danh_muc_tinh_chat_hang_hoa.view` | Xem danh mục tính chất hàng hóa | Danh mục dùng chung toàn hệ thống |
| Danh mục dùng chung | Xuất xứ | `master_data.danh_muc_xuat_xu.view` | Xem danh mục xuất xứ | Danh mục dùng chung toàn hệ thống |
| Meeting | Danh mục | `meeting.danh_muc_loai_meeting.view` | Xem danh mục loại meeting | Danh mục dùng chung toàn hệ thống |
| Meeting | Danh mục | `meeting.danh_muc_ly_do_huy_cuoc_hop.view` | Xem danh mục lý do hủy cuộc họp | Danh mục dùng chung toàn hệ thống |
| Tài chính | Danh mục | `finance.danh_muc_loai_tai_khoan.view` | Xem danh mục loại tài khoản | Danh mục dùng chung toàn hệ thống |
| Tài chính | Danh mục | `finance.danh_muc_tai_khoan.view` | Xem danh mục tài khoản | Danh mục dùng chung toàn hệ thống |
| Tài chính | Danh mục | `finance.danh_muc_tien_te.view` | Xem danh mục tiền tệ | Danh mục dùng chung toàn hệ thống |
| Tính lương | Các thành phần khác | `payroll.cac_thanh_phan_khac.view` | Xem các thành phần khác | Cấu hình tính lương, không gắn cấp tổ chức |
| Tính lương | Cơ cấu định biên nhân sự | `payroll.co_cau_dinh_bien_nhan_su.view` | Xem cơ cấu định biên nhân sự | Cấu hình tính lương, không gắn cấp tổ chức |
| Tính lương | Định mức thưởng P3 (Hoa hồng/lương khoán) | `payroll.dinh_muc_thuong_p3.view` | Xem định mức thưởng P3 (Hoa hồng/lương khoán) | Cấu hình tính lương, không gắn cấp tổ chức |
| Tính lương | Mẫu bảng tính thu nhập | `payroll.mau_bang_luong.view` | Xem mẫu bảng lương | Cấu hình tính lương, không gắn cấp tổ chức |

## B. KHÔNG nên có phạm vi (công tắc, quyền "tất cả", dữ liệu nhạy cảm) (18)

| Phân hệ | Chức năng | Mã quyền | Tên quyền | Lý do |
|---|---|---|---|---|
| Bán hàng | Báo giá - HĐ dự án | `sale.gia_von_du_an.view` | Xem giá vốn dự án | Công tắc/quyền "tất cả" hoặc dữ liệu nhạy cảm — tên đã là cấp, không phải chọn phạm vi |
| Bán hàng | Hỗ trợ hạch toán | `sale.ho_tro_hach_toan_day_du.view` | Xem đầy đủ hỗ trợ hạch toán | Công tắc/quyền "tất cả" hoặc dữ liệu nhạy cảm — tên đã là cấp, không phải chọn phạm vi |
| Bán hàng | Hỗ trợ hạch toán | `sale.ho_tro_hach_toan.view` | Xem danh sách hỗ trợ hạch toán | Công tắc/quyền "tất cả" hoặc dữ liệu nhạy cảm — tên đã là cấp, không phải chọn phạm vi |
| Bán hàng | Hỗ trợ hạch toán ban giám đốc | `sale.ho_tro_hach_toan_ban_giam_doc.view` | Xem hỗ trợ hạch toán, giá vốn, quyết toán dành cho ban giám đốc | Công tắc/quyền "tất cả" hoặc dữ liệu nhạy cảm — tên đã là cấp, không phải chọn phạm vi |
| Bán hàng | Hợp đồng bán hàng | `sale.hop_dong_an_gia.view` | Xem hợp đồng ẩn giá | Công tắc/quyền "tất cả" hoặc dữ liệu nhạy cảm — tên đã là cấp, không phải chọn phạm vi |
| Chấm công | Tổng quan | `timesheet.dashboard_nhan_vien.view` | Dashboard nhân viên | Công tắc/quyền "tất cả" hoặc dữ liệu nhạy cảm — tên đã là cấp, không phải chọn phạm vi |
| Chấm công | Tổng quan | `timesheet.dashboard_quan_ly.view` | Dashboard quản lý | Công tắc/quyền "tất cả" hoặc dữ liệu nhạy cảm — tên đã là cấp, không phải chọn phạm vi |
| Chấm công | Tổng quan | `timesheet.dashboard_truong_phong.view` | Dashboard trưởng phòng | Công tắc/quyền "tất cả" hoặc dữ liệu nhạy cảm — tên đã là cấp, không phải chọn phạm vi |
| Danh mục dùng chung | Hàng hoá, vật tư | `master_data.gia_von_hang_hoa.view` | Xem giá vốn hàng hoá | Công tắc/quyền "tất cả" hoặc dữ liệu nhạy cảm — tên đã là cấp, không phải chọn phạm vi |
| Đào tạo - đánh giá | Danh sách khóa học | `training.thong_tin_tat_ca_khoa_hoc.view` | Xem thông tin của tất cả khóa học | Công tắc/quyền "tất cả" hoặc dữ liệu nhạy cảm — tên đã là cấp, không phải chọn phạm vi |
| Đào tạo - đánh giá | Dashboard đào tạo | `training.dashboard_khoi_quan_ly.view` | Xem khối quản lý ở dashboard đào tạo | Công tắc/quyền "tất cả" hoặc dữ liệu nhạy cảm — tên đã là cấp, không phải chọn phạm vi |
| Đào tạo - đánh giá | Dashboard đào tạo | `training.dashboard_khoi_quan_tri.view` | Xem khối quản trị ở dashboard đào tạo | Công tắc/quyền "tất cả" hoặc dữ liệu nhạy cảm — tên đã là cấp, không phải chọn phạm vi |
| Kho | Danh mục | `warehouse.kho_tat_ca_cong_ty.view` | Xem danh mục kho của tất cả công ty | Công tắc/quyền "tất cả" hoặc dữ liệu nhạy cảm — tên đã là cấp, không phải chọn phạm vi |
| Kho | Kho | `warehouse.phieu_xuat_nhap_kho.view` | Xem phiếu xuất nhập kho | Công tắc/quyền "tất cả" hoặc dữ liệu nhạy cảm — tên đã là cấp, không phải chọn phạm vi |
| Kho | Tồn kho đầu kỳ | `warehouse.ton_kho_dau_ky_tat_ca_cong_ty.view` | Xem tồn kho đầu kỳ của tất cả công ty | Công tắc/quyền "tất cả" hoặc dữ liệu nhạy cảm — tên đã là cấp, không phải chọn phạm vi |
| Quản lý cơm | Thực đơn | `rice.thuc_don.view` | Xem thực đơn | Công tắc/quyền "tất cả" hoặc dữ liệu nhạy cảm — tên đã là cấp, không phải chọn phạm vi |
| Quản trị hệ thống | Hệ thống | `admin.phan_quyen.view` | Phân quyền | Công tắc/quyền "tất cả" hoặc dữ liệu nhạy cảm — tên đã là cấp, không phải chọn phạm vi |
| Tài chính | Giữ hàng | `finance.huy_hang_giu_ke_toan_tat_ca_cong_ty.view` | Xem phiếu huỷ hàng giữ kế toán của tất cả công ty | Công tắc/quyền "tất cả" hoặc dữ liệu nhạy cảm — tên đã là cấp, không phải chọn phạm vi |

## C. NÊN CÓ phạm vi (dữ liệu theo nhân sự / phòng ban / công ty) (22)

| Phân hệ | Chức năng | Mã quyền | Tên quyền | Lý do |
|---|---|---|---|---|
| CSKH trước bán | Báo cáo phân chia thị trường | `presale.bao_cao_phan_chia_thi_truong.view` | Xem báo cáo phân chia thị trường | Báo cáo theo phòng ban |
| Danh mục dùng chung | Danh sách nhân viên | `master_data.ho_so_nhan_vien.view` | Xem hồ sơ | Hồ sơ nhân viên thuộc phòng ban/bộ phận |
| Danh mục dùng chung | Khách hàng | `master_data.khach_hang_da_dang_ky.view` | Xem danh sách khách hàng đã đăng ký | Cùng nhóm Khách hàng |
| Danh mục dùng chung | Khách hàng | `master_data.khach_hang.view` | Xem khách hàng | Quyền cũ có 4 mức (tất cả / công ty / phòng ban / bộ phận), Step 4 gộp thành 1 mã không phạm vi ⇒ ai có quyền cũng thấy mọi khách hàng. Code lọc chưa sửa |
| Danh mục dùng chung | Khách hàng | `master_data.lich_su_khach_hang.view` | Xem lịch sử khách hàng | Cùng nhóm Khách hàng |
| Đào tạo - đánh giá | Bài thi đánh giá năng lực cần chấm điểm | `training.bai_thi_danh_gia_nang_luc_can_cham.view` | Xem danh sách bài thi đánh giá năng lực cần chấm điểm | Báo cáo/kết quả theo nhân viên ⇒ nên lọc theo phòng ban/công ty |
| Đào tạo - đánh giá | Báo cáo hoàn thành khung năng lực | `training.bao_cao_hoan_thanh_khung_nang_luc.view` | Báo cáo hoàn thành khung năng lực | Báo cáo/kết quả theo nhân viên ⇒ nên lọc theo phòng ban/công ty |
| Đào tạo - đánh giá | Tổng hợp đánh giá theo năng lực | `training.tong_hop_danh_gia_theo_nang_luc.view` | Xem tổng hợp đánh giá theo năng lực | Báo cáo/kết quả theo nhân viên ⇒ nên lọc theo phòng ban/công ty |
| Đào tạo - đánh giá | Tổng hợp điểm bài thi kỳ đánh giá | `training.ket_qua_danh_gia_nang_luc.view` | Xem kết quả đánh giá năng lực | Báo cáo/kết quả theo nhân viên ⇒ nên lọc theo phòng ban/công ty |
| Đào tạo - đánh giá | Tổng hợp kết quả khóa học | `training.tong_hop_ket_qua_khoa_hoc.view` | Tổng hợp kết quả khóa học | Báo cáo/kết quả theo nhân viên ⇒ nên lọc theo phòng ban/công ty |
| Đào tạo - đánh giá | Tổng hợp kết quả theo kỳ đánh giá | `training.tong_hop_ket_qua_danh_gia_theo_ky.view` | Tổng hợp kết quả đánh giá theo kỳ | Báo cáo/kết quả theo nhân viên ⇒ nên lọc theo phòng ban/công ty |
| Kho | Báo cáo kho | `warehouse.bao_cao_ton_kho_theo_kho.view` | Xem báo cáo tồn kho theo kho | Theo kho ⇒ gắn công ty |
| Kho | Điều chuyển | `warehouse.dieu_chuyen_vi_tri_theo_kho.view` | Xem điều chuyển vị trí theo kho | Theo kho ⇒ gắn công ty |
| Tài chính | Khách hàng | `finance.khai_bao_han_muc_cong_no_khach_hang.view` | Xem khai báo hạn mức công nợ khách hàng | Dữ liệu theo khách hàng/công ty |
| Thông tin nhân sự | Cập nhật tình hình nhân sự | `human.bao_cao_cap_nhat_tinh_hinh_nhan_su.view` | Xem báo cáo cập nhật tình hình nhân sự | Báo cáo nhân sự theo phòng ban |
| Tính lương | Bảng chấm công tổng hợp | `payroll.bang_cham_cong_tong_hop.view` | Xem bảng chấm công tổng hợp | Dữ liệu lương theo nhân viên ⇒ nên lọc theo phòng ban/công ty (cần kiểm BE hiện lọc thế nào) |
| Tính lương | Bảng chi trả | `payroll.bang_chi_tra_luong.view` | Xem bảng chi trả lương | Dữ liệu lương theo nhân viên ⇒ nên lọc theo phòng ban/công ty (cần kiểm BE hiện lọc thế nào) |
| Tính lương | Khấu trừ khác | `payroll.khau_tru_khac.view` | Xem khấu trừ khác | Dữ liệu lương theo nhân viên ⇒ nên lọc theo phòng ban/công ty (cần kiểm BE hiện lọc thế nào) |
| Tính lương | Phân công lương | `payroll.bang_phan_cong_luong.view` | Xem bảng phân công lương | Dữ liệu lương theo nhân viên ⇒ nên lọc theo phòng ban/công ty (cần kiểm BE hiện lọc thế nào) |
| Tính lương | Tạm ứng | `payroll.tam_ung_luong.view` | Xem tạm ứng lương | Dữ liệu lương theo nhân viên ⇒ nên lọc theo phòng ban/công ty (cần kiểm BE hiện lọc thế nào) |
| Tính lương | Thu nhập khác | `payroll.thu_nhap_khac.view` | Xem thu nhập khác | Dữ liệu lương theo nhân viên ⇒ nên lọc theo phòng ban/công ty (cần kiểm BE hiện lọc thế nào) |
| Tính lương | Tổng hợp lương | `payroll.bang_tong_hop_luong.view` | Xem bảng tổng hợp lương | Dữ liệu lương theo nhân viên ⇒ nên lọc theo phòng ban/công ty (cần kiểm BE hiện lọc thế nào) |

## D. Cần xác nhận nghiệp vụ (8)

| Phân hệ | Chức năng | Mã quyền | Tên quyền | Lý do |
|---|---|---|---|---|
| Danh mục dùng chung | Danh mục công ty | `master_data.cong_ty.view` | Xem công ty | Dữ liệu dùng chung hoặc theo công ty — cần xác nhận với nghiệp vụ |
| Danh mục dùng chung | Dữ liệu hàng hoá công ty | `master_data.du_lieu_hang_hoa_cong_ty.view` | Xem dữ liệu hàng hoá công ty | Dữ liệu dùng chung hoặc theo công ty — cần xác nhận với nghiệp vụ |
| Danh mục dùng chung | Hàng hoá, vật tư | `master_data.hang_hoa.view` | Xem hàng hóa | Dữ liệu dùng chung hoặc theo công ty — cần xác nhận với nghiệp vụ |
| Danh mục dùng chung | Hàng hoá, vật tư | `master_data.lich_su_hang_hoa.view` | Xem lịch sử chỉnh sửa hàng hóa | Dữ liệu dùng chung hoặc theo công ty — cần xác nhận với nghiệp vụ |
| Danh mục dùng chung | Hàng tạm | `master_data.hang_tam.view` | Xem danh sách hàng tạm | Dữ liệu dùng chung hoặc theo công ty — cần xác nhận với nghiệp vụ |
| Danh mục dùng chung | Nhà cung cấp | `master_data.lich_su_nha_cung_cap.view` | Xem lịch sử nhà cung cấp | Dữ liệu dùng chung hoặc theo công ty — cần xác nhận với nghiệp vụ |
| Danh mục dùng chung | Nhà cung cấp | `master_data.nha_cung_cap.view` | Xem nhà cung cấp | Dữ liệu dùng chung hoặc theo công ty — cần xác nhận với nghiệp vụ |
| Danh mục dùng chung | Quản lý danh mục | `master_data.danh_muc.view` | Xem danh mục | Dữ liệu dùng chung hoặc theo công ty — cần xác nhận với nghiệp vụ |
