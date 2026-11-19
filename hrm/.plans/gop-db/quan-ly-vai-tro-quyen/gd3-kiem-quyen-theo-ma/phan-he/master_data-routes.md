# master_data — đường đọc chụp mốc (GĐ3 Task 8.17)

Đầu vào máy đọc: `master_data-routes.json` (`routes` = ScopeSnapshot; `routes_body` = `bodysnap.py` băm NỘI DUNG — cờ / cột giá vốn / khối blade / tập link menu, vì master_data đổi chủ yếu kiểm có/không).
Catalog master_data 135 mã, chỉ 1 mã có phạm vi (`master_data.yeu_cau_duyet_hang_tam.view` 2/3/4); mọi tên cũ khác min_scope null (kể cả 4 tên "Xem tất cả khách hàng …" — user chốt không phạm vi).

## Tài khoản (rehearsal, chỉ SELECT)

| key | employee | ghi chú |
|---|---|---|
| pv4 | 13 | namdangit — 135/135 mã master_data, yeu_cau_duyet_hang_tam 4, cty 1 |
| pv2 | 211 | phuongbt.ptgd — 89 mã, yeu_cau_duyet_hang_tam 2 (quản lý phòng 95), cty 1 |
| mid | 207 | hantt.kthn — 20 mã (KH, hàng hoá, duyệt hàng tạm; không giá vốn), cty 1 |
| dm | 144 | huyentt.nshn — 63 mã (52 danh mục HRM, xây dựng TT hàng hoá; không hàng hoá ERP), cty 1 |
| it | 24 | tuannd.kd1 — 8 mã, cty 1 |
| cty4 | 901 | sonll.tpsg — 20 mã, cty 4 |
| khong_ma | 630 | triln.datd — 0 mã master_data, cty 1 |

Ca thiếu: không ai giữ `yeu_cau_duyet_hang_tam.view` mức 3 ở công ty đang làm (1 vai trò mức 3 không ai gán) và 0 dòng scope NULL cho mã này ⇒ mức 3 + "có mã không phạm vi" phủ bằng PHPUnit (MasterDataScopeConversionTest). Khác công ty: cty4 (901).

## Route (ScopeSnapshot)

| id | app | url | mã | chuỗi phạm vi | lọc / ghi chú |
|---|---|---|---|---|---|
| erp.categories | erp | admin/categories | master_data.danh_muc.view |  | middleware + cờ blade |
| erp.categories.create | erp | admin/categories/create | master_data.danh_muc.create |  | middleware + cờ blade |
| erp.categories.getChildren | erp | admin/categories/getChildren | master_data.danh_muc.view |  | middleware |
| erp.categories.search | erp | admin/categories/search | master_data.danh_muc.view |  | middleware |
| erp.categories.searchData | erp | admin/categories/searchData | master_data.danh_muc.view |  | middleware |
| erp.categories.edit | erp | admin/categories/{id}/edit | master_data.danh_muc.update |  | middleware (mở được / chặn) |
| erp.common.transport_types | erp | admin/common/transport_types | master_data.phuong_tien.manage |  | middleware + cờ blade |
| erp.common.transport_types.searchData | erp | admin/common/transport_types/searchData | master_data.phuong_tien.manage |  | middleware |
| erp.companies | erp | admin/companies | master_data.cong_ty.view |  | middleware + cờ blade |
| erp.companies.create | erp | admin/companies/create | master_data.cong_ty.create |  | middleware + cờ blade |
| erp.companies.searchData | erp | admin/companies/searchData | master_data.cong_ty.view |  | middleware |
| erp.companies.edit | erp | admin/companies/{id}/edit | master_data.cong_ty.update |  | middleware (mở được / chặn) |
| erp.customer_groups | erp | admin/customer_groups | master_data.nhom_khach_hang.view |  | middleware + cờ blade |
| erp.customer_groups.searchData | erp | admin/customer_groups/searchData | master_data.nhom_khach_hang.view |  | middleware |
| erp.customers | erp | admin/customers | master_data.khach_hang.view |  | middleware + cờ blade |
| erp.customers.create | erp | admin/customers/create | master_data.khach_hang.create |  | middleware + cờ blade |
| erp.customers.edit | erp | admin/customers/{id}/edit | master_data.khach_hang.update |  | middleware (mở được / chặn) |
| erp.customers.history | erp | admin/customers/{id}/history | master_data.lich_su_khach_hang.view |  | middleware (mở được / chặn) |
| erp.customers.manager | erp | admin/customers/{id}/manager | master_data.khach_hang.view |  | middleware (mở được / chặn) |
| erp.customers.show | erp | admin/customers/{id}/show | master_data.khach_hang.view |  | middleware (mở được / chặn) |
| erp.departments | erp | admin/departments | master_data.phong_ban.manage |  | middleware + cờ blade |
| erp.departments.searchData | erp | admin/departments/searchData | master_data.phong_ban.manage |  | middleware |
| erp.departments.searchDepartmentByKeyword | erp | admin/departments/searchDepartmentByKeyword | master_data.phong_ban.manage |  | middleware |
| erp.employee_infos | erp | admin/employee_infos | master_data.ho_so_nhan_vien.view |  | middleware + cờ blade |
| erp.employee_infos.create | erp | admin/employee_infos/create | master_data.ho_so_nhan_vien.create |  | middleware + cờ blade |
| erp.employee_infos.searchData | erp | admin/employee_infos/searchData | master_data.ho_so_nhan_vien.view |  | middleware |
| erp.employee_infos.edit | erp | admin/employee_infos/{id}/edit | master_data.ho_so_nhan_vien.update |  | middleware (mở được / chặn) |
| erp.employee_infos.histories | erp | admin/employee_infos/{id}/histories | master_data.ho_so_nhan_vien.view |  | middleware (mở được / chặn) |
| erp.groups | erp | admin/groups | master_data.nhom_hang_hoa.view |  | middleware + cờ blade |
| erp.groups.create | erp | admin/groups/create | master_data.nhom_hang_hoa.create |  | middleware + cờ blade |
| erp.groups.searchData | erp | admin/groups/searchData | master_data.nhom_hang_hoa.view |  | middleware |
| erp.orders.delivery_specifications | erp | admin/orders/delivery_specifications | master_data.quy_cach_van_chuyen.manage |  | middleware + cờ blade |
| erp.orders.delivery_specifications.searchData | erp | admin/orders/delivery_specifications/searchData | master_data.quy_cach_van_chuyen.manage |  | middleware |
| erp.orders.ports | erp | admin/orders/ports | master_data.cang.manage |  | middleware + cờ blade |
| erp.orders.ports.searchData | erp | admin/orders/ports/searchData | master_data.cang.manage |  | middleware |
| erp.orders.revenue_collection_agency | erp | admin/orders/revenue_collection_agency | master_data.don_vi_thu_ngan_sach.manage |  | middleware + cờ blade |
| erp.orders.revenue_collection_agency.searchData | erp | admin/orders/revenue_collection_agency/searchData | master_data.don_vi_thu_ngan_sach.manage |  | middleware |
| erp.orders.revenue_collection_categories | erp | admin/orders/revenue_collection_categories | master_data.thu_nop_ngan_sach.manage |  | middleware + cờ blade |
| erp.orders.revenue_collection_categories.searchData | erp | admin/orders/revenue_collection_categories/searchData | master_data.thu_nop_ngan_sach.manage |  | middleware |
| erp.orders.shipping_conditions | erp | admin/orders/shipping_conditions | master_data.dieu_kien_giao_hang.manage |  | middleware + cờ blade |
| erp.orders.shipping_conditions.searchData | erp | admin/orders/shipping_conditions/searchData | master_data.dieu_kien_giao_hang.manage |  | middleware |
| erp.parts | erp | admin/parts | master_data.bo_phan.manage |  | middleware + cờ blade |
| erp.parts.searchData | erp | admin/parts/searchData | master_data.bo_phan.manage |  | middleware |
| erp.pi-groups | erp | admin/pi-groups | master_data.nhom_hang_hoa.view |  | middleware + cờ blade |
| erp.pi-groups.create | erp | admin/pi-groups/create | master_data.nhom_hang_hoa.create |  | middleware + cờ blade |
| erp.pi-groups.searchData | erp | admin/pi-groups/searchData | master_data.nhom_hang_hoa.view |  | middleware |
| erp.pi-uniteches | erp | admin/pi-uniteches | master_data.don_vi_thuoc_tinh.view |  | middleware + cờ blade |
| erp.pi-uniteches.create | erp | admin/pi-uniteches/create | master_data.don_vi_thuoc_tinh.create |  | middleware + cờ blade |
| erp.pi-uniteches.searchData | erp | admin/pi-uniteches/searchData | master_data.don_vi_thuoc_tinh.view |  | middleware |
| erp.pick_up_address | erp | admin/pick_up_address | master_data.dia_chi_lay_hang.update |  | middleware + cờ blade |
| erp.pick_up_address.searchData | erp | admin/pick_up_address/searchData | master_data.dia_chi_lay_hang.update |  | middleware |
| erp.product-infos | erp | admin/product-infos | master_data.hang_hoa.view |  | middleware + cờ blade |
| erp.product-infos.create | erp | admin/product-infos/create | master_data.hang_hoa.create |  | middleware + cờ blade |
| erp.product-infos.searchData | erp | admin/product-infos/searchData | master_data.hang_hoa.view |  | middleware |
| erp.product-infos.searchData2 | erp | admin/product-infos/searchData2 | master_data.hang_hoa.view |  | middleware |
| erp.product-infos.show | erp | admin/product-infos/{id}/show | master_data.hang_hoa.view |  | middleware (mở được / chặn) |
| erp.product2 | erp | admin/product2 | master_data.hang_hoa.view |  | middleware + cờ blade |
| erp.product2.create | erp | admin/product2/create | master_data.hang_hoa.create |  | middleware + cờ blade |
| erp.product2.searchData | erp | admin/product2/searchData | master_data.hang_hoa.view |  | middleware |
| erp.product2.edit | erp | admin/product2/{id}/edit | master_data.hang_hoa.update |  | middleware (mở được / chặn) |
| erp.product2.show | erp | admin/product2/{id}/show | master_data.hang_hoa.update |  | middleware (mở được / chặn) |
| erp.product_templates | erp | admin/product_templates | master_data.hang_hoa.view |  | middleware + cờ blade |
| erp.product_templates.create | erp | admin/product_templates/create | master_data.hang_hoa.create |  | middleware + cờ blade |
| erp.product_templates.searchData | erp | admin/product_templates/searchData | master_data.hang_hoa.view |  | middleware |
| erp.product_templates.show | erp | admin/product_templates/{id}/show | master_data.hang_hoa.view |  | middleware (mở được / chặn) |
| erp.products | erp | admin/products | master_data.hang_hoa.view |  | middleware + cờ blade |
| erp.products.approvePrices | erp | admin/products/approvePrices | master_data.gia_hang_hoa.approve |  | middleware + cờ blade |
| erp.products.create | erp | admin/products/create | master_data.hang_hoa.create |  | middleware + cờ blade |
| erp.products.editPrices | erp | admin/products/editPrices | master_data.gia_hang_hoa.update |  | middleware + cờ blade |
| erp.products.expectedPrices | erp | admin/products/expectedPrices | master_data.gia_hang_hoa.manage |  | middleware + cờ blade |
| erp.products.manualUpdatePrices | erp | admin/products/manualUpdatePrices | master_data.gia_hang_hoa.manage |  | middleware + cờ blade |
| erp.products.searchData | erp | admin/products/searchData | master_data.hang_hoa.view |  | middleware |
| erp.products.copy | erp | admin/products/{id}/copy | master_data.hang_hoa.create |  | middleware (mở được / chặn) |
| erp.products.edit | erp | admin/products/{id}/edit | master_data.hang_hoa.update |  | middleware (mở được / chặn) |
| erp.products.history | erp | admin/products/{id}/history | master_data.lich_su_hang_hoa.view |  | middleware (mở được / chặn) |
| erp.products.show | erp | admin/products/{id}/show | master_data.hang_hoa.view |  | middleware (mở được / chặn) |
| erp.sale.device-errors.create | erp | admin/sale/device-errors/create | master_data.cong_viec_loi_thiet_bi.create |  | middleware + cờ blade |
| erp.sale.device-errors.edit | erp | admin/sale/device-errors/{id}/edit | master_data.cong_viec_loi_thiet_bi.update |  | middleware (mở được / chặn) |
| erp.sale.manufacture_expect_prices | erp | admin/sale/manufacture_expect_prices | master_data.gia_hang_hoa.update |  | middleware + cờ blade |
| erp.sale.manufacture_expect_prices.create | erp | admin/sale/manufacture_expect_prices/create | master_data.gia_hang_hoa.update |  | middleware + cờ blade |
| erp.sale.manufacture_expect_prices.searchData | erp | admin/sale/manufacture_expect_prices/searchData | master_data.gia_hang_hoa.update |  | middleware |
| erp.sale.manufacture_expect_prices.show | erp | admin/sale/manufacture_expect_prices/{id}/show | master_data.gia_hang_hoa.update |  | middleware (mở được / chặn) |
| erp.sale.scopes | erp | admin/sale/scopes | master_data.linh_vuc.view |  | middleware + cờ blade |
| erp.sale.scopes.searchData | erp | admin/sale/scopes/searchData | master_data.linh_vuc.view |  | middleware |
| erp.suppliers | erp | admin/suppliers | master_data.nha_cung_cap.view |  | middleware + cờ blade |
| erp.suppliers.create | erp | admin/suppliers/create | master_data.nha_cung_cap.create |  | middleware + cờ blade |
| erp.uniteches | erp | admin/uniteches | master_data.don_vi_thuoc_tinh.view |  | middleware + cờ blade |
| erp.uniteches.create | erp | admin/uniteches/create | master_data.don_vi_thuoc_tinh.create |  | middleware + cờ blade |
| erp.uniteches.searchData | erp | admin/uniteches/searchData | master_data.don_vi_thuoc_tinh.view |  | middleware |
| erp.tmp_product_requests.index | erp | admin/sale/tmp_product_requests | master_data.yeu_cau_duyet_hang_tam.view | có | cờ is_big_boss/is_boss/is_manager |
| erp.tmp_product_requests.searchData.all | erp | admin/sale/tmp_product_requests/searchData | master_data.yeu_cau_duyet_hang_tam.view | có | company_id / department_id ∈ quản lý / created_by |
| erp.tmp_product_requests.searchData.approve | erp | admin/sale/tmp_product_requests/searchData | master_data.hang_tam.approve |  | company_id |
| erp.tmp_product_requests.searchData | erp | admin/sale/tmp_product_requests/searchData | - |  | created_by |
| erp.tmp_product_requests.show | erp | admin/sale/tmp_product_requests/{id}/show | master_data.hang_tam.approve |  | canView |
| erp.tmp_products.index | erp | admin/tmp_products | master_data.hang_tam.view |  |  |
| erp.tmp_products.searchData | erp | admin/tmp_products/searchData | master_data.hang_tam.view,master_data.hang_tam.approve |  | visibleTo (công ty người tạo / phân công TH-HSX) |
| erp.tmp_products.show | erp | admin/tmp_products/{id}/show | master_data.hang_tam.view |  | canView |
| erp.customers.searchData | erp | admin/customers/searchData | master_data.khach_hang.view | có | Customer::searchByFilter chuỗi 4 tên (cùng mã, không phạm vi) |
| erp.customer_registers.index | erp | admin/customer_registers | master_data.khach_hang_da_dang_ky.view |  | can trong controller |
| erp.device_errors.index | erp | admin/sale/device-errors | master_data.cong_viec_loi_thiet_bi.create |  | nút Thêm (blade) |
| erp.device_errors.searchData | erp | admin/sale/device-errors/searchData | master_data.cong_viec_loi_thiet_bi.update,delete |  | cờ dòng |
| erp.home.approveList | erp | admin/approveList | master_data.gia_hang_hoa.approve,thong_tin_quan_ly_ban_hang.update |  | đếm việc chờ |
| api.md.product-natures | api | master-data/product-natures | master_data.danh_muc_tinh_chat_hang_hoa.manage|master_data.danh_muc_tinh_chat_hang_hoa.view |  | middleware |
| api.md.product-function-groups | api | master-data/product-function-groups | master_data.danh_muc_nhom_chuc_nang.manage|master_data.danh_muc_nhom_chuc_nang.view |  | middleware |
| api.md.product-families | api | master-data/product-families | master_data.danh_muc_nhom_san_pham.manage|master_data.danh_muc_nhom_san_pham.view |  | middleware |
| api.md.product-types | api | master-data/product-types | master_data.danh_muc_loai_san_pham.manage|master_data.danh_muc_loai_san_pham.view |  | middleware |
| api.md.business-policies | api | master-data/business-policies | master_data.danh_muc_chinh_sach_kinh_doanh.manage|master_data.danh_muc_chinh_sach_kinh_doanh.view |  | middleware |
| api.md.product-characteristics | api | master-data/product-characteristics | master_data.danh_muc_dac_tinh_san_pham.manage|master_data.danh_muc_dac_tinh_san_pham.view |  | middleware |
| api.md.origins | api | master-data/origins | master_data.danh_muc_xuat_xu.manage|master_data.danh_muc_xuat_xu.view |  | middleware |
| api.md.attribute-units | api | master-data/attribute-units | master_data.danh_muc_don_vi_thuoc_tinh.manage|master_data.danh_muc_don_vi_thuoc_tinh.view |  | middleware |
| api.md.product-models | api | master-data/product-models | master_data.danh_muc_model.manage|master_data.danh_muc_model.view |  | middleware |
| api.md.units | api | master-data/units | master_data.danh_muc_don_vi_tinh.manage|master_data.danh_muc_don_vi_tinh.view |  | middleware |
| api.md.attributes | api | master-data/attributes | master_data.danh_muc_thuoc_tinh.manage|master_data.danh_muc_thuoc_tinh.view |  | middleware |
| api.md.brands | api | master-data/brands | master_data.danh_muc_thuong_hieu.manage|master_data.danh_muc_thuong_hieu.view |  | middleware |
| api.md.manufacturers | api | master-data/manufacturers | master_data.danh_muc_hang_san_xuat.manage|master_data.danh_muc_hang_san_xuat.view |  | middleware |
| api.md.order-codes | api | master-data/order-codes | master_data.danh_muc_code_dat_hang.manage|master_data.danh_muc_code_dat_hang.view |  | middleware |
| api.md.attachment-types | api | master-data/attachment-types | master_data.danh_muc_file_dinh_kem.manage|master_data.danh_muc_file_dinh_kem.view |  | middleware |
| api.md.color-codes | api | master-data/color-codes | master_data.danh_muc_ma_mau.manage|master_data.danh_muc_ma_mau.view |  | middleware |
| api.md.vehicle-manufacts | api | master-data/vehicle-manufacts | master_data.danh_muc_hang_xe.manage|master_data.danh_muc_hang_xe.view |  | middleware |
| api.md.vehicle-brands | api | master-data/vehicle-brands | master_data.danh_muc_loai_xe.manage|master_data.danh_muc_loai_xe.view |  | middleware |
| api.md.vehicle-models | api | master-data/vehicle-models | master_data.danh_muc_model_xe.manage|master_data.danh_muc_model_xe.view |  | middleware |
| api.md.vehicle-life | api | master-data/vehicle-life | master_data.danh_muc_doi_xe.manage|master_data.danh_muc_doi_xe.view |  | middleware |
| api.md.vehicle-categories | api | master-data/vehicle-categories | master_data.danh_muc_dong_xe.manage|master_data.danh_muc_dong_xe.view |  | middleware |
| api.md.vehicle-payloads | api | master-data/vehicle-payloads | master_data.danh_muc_tai_trong_xe.manage|master_data.danh_muc_tai_trong_xe.view |  | middleware |
| api.md.license-plates | api | master-data/license-plates | master_data.danh_muc_bien_so_xe.manage|master_data.danh_muc_bien_so_xe.view |  | middleware |
| api.md.external-drivers | api | master-data/external-drivers | master_data.danh_muc_lai_xe_ngoai.manage|master_data.danh_muc_lai_xe_ngoai.view |  | middleware |
| api.md.fuels | api | master-data/fuels | master_data.danh_muc_nhien_lieu.manage|master_data.danh_muc_nhien_lieu.view |  | middleware |
| api.md.vehicles | api | master-data/vehicles | master_data.danh_muc_xe.manage|master_data.danh_muc_xe.view |  | middleware |
| api.md.chapters | api | master-data/chapters | master_data.danh_muc_chuong.manage|master_data.danh_muc_chuong.view |  | middleware |
| api.md.job-groups | api | master-data/job-groups | master_data.danh_muc_muc.manage|master_data.danh_muc_muc.view |  | middleware |
| api.md.job-clusters | api | master-data/job-clusters | master_data.danh_muc_tieu_muc.manage|master_data.danh_muc_tieu_muc.view |  | middleware |
| api.md.tax-rates | api | master-data/tax-rates | master_data.danh_muc_thue_suat.manage|master_data.danh_muc_thue_suat.view |  | middleware |
| api.md.vehicles.options.employees | api | master-data/vehicles/options/employees | master_data.danh_muc_xe.manage|view |  | middleware |
| api.products.warehouse | api | master-data/products/warehouse | - (cờ can_build từng dòng: master_data.thong_tin_hang_hoa.manage) |  | middleware + cờ dòng |
| api.products.warehouse.export_rows | api | master-data/products/warehouse/export-rows | master_data.danh_sach_hang_hoa.export |  | middleware + controller |
| api.products.trading | api | master-data/products/trading | - (cờ can_build từng dòng: master_data.thong_tin_hang_hoa.manage) |  | middleware + cờ dòng |
| api.products.trading.export_rows | api | master-data/products/trading/export-rows | master_data.danh_sach_hang_hoa.export |  | middleware + controller |
| api.products.temp | api | master-data/products/temp | - (cờ can_build từng dòng: master_data.thong_tin_hang_hoa.manage) |  | middleware + cờ dòng |
| api.products.temp.export_rows | api | master-data/products/temp/export-rows | master_data.danh_sach_hang_hoa.export |  | middleware + controller |
| api.products.locked | api | master-data/products/locked | - (cờ can_build từng dòng: master_data.thong_tin_hang_hoa.manage) |  | middleware + cờ dòng |
| api.products.locked.export_rows | api | master-data/products/locked/export-rows | master_data.danh_sach_hang_hoa.export |  | middleware + controller |
| api.products.company | api | master-data/products/company | master_data.thong_tin_hang_hoa.manage|master_data.du_lieu_hang_hoa_cong_ty.view (cờ can_build từng dòng: master_data.thong_tin_hang_hoa.manage) |  | middleware + cờ dòng |
| api.products.company.export_rows | api | master-data/products/company/export-rows | master_data.danh_sach_hang_hoa.export |  | middleware + controller |
| api.products.entering | api | master-data/products/entering | master_data.thong_tin_hang_hoa.manage (cờ can_build từng dòng: master_data.thong_tin_hang_hoa.manage) |  | middleware + cờ dòng |
| api.products.entering.export_rows | api | master-data/products/entering/export-rows | master_data.danh_sach_hang_hoa.export |  | middleware + controller |
| api.products.catalogs.counts | api | master-data/products/catalogs/counts | master_data.catalog_kinh_doanh.manage |  | middleware |
| api.products.catalogs.products | api | master-data/products/catalogs/products | master_data.catalog_kinh_doanh.manage |  | middleware |
| api.products.histories | api | master-data/products/histories/{id} | master_data.lich_su_hang_hoa.view |  | controller |
| api.products.edit | api | master-data/products/{id}/edit | master_data.thong_tin_hang_hoa.manage |  | middleware |
| api.customers.index | api | assign/customers | master_data.khach_hang.view | có | CustomerService chuỗi 4 tên (cùng mã) |
| api.customers.my_permissions | api | assign/customers/my-permissions | master_data.khach_hang.* |  | cờ |
| api.customers.show | api | assign/customers/{id} | master_data.khach_hang.view |  | isVisible |
| api.customers.documents | api | assign/customers/{id}/documents | master_data.khach_hang.view |  | erpPermission |
| api.customers.export_rows | api | assign/customers/export-rows | master_data.khach_hang.export |  | erpPermission |
| api.customer_registers.index | api | assign/report/customer-registers | master_data.khach_hang_da_dang_ky.view |  | middleware |
| api.price_calculate_requests.index | api | master-data/price-calculate-requests | master_data.gia_von_hang_hoa.view (isActor) + sale.* | có | PriceCalculateRequestAccess |
| api.price_calculates.index | api | master-data/price-calculates | master_data.gia_von_hang_hoa.view (isActor) + finance.* | có | PriceCalculateAccess |
| api.product_price_approvals.index | api | master-data/product-price-approvals | finance.gia_ban_hang_hoa.approve + master_data.gia_von_hang_hoa.view (cột giá vốn) |  | cột giá vốn |
| api.product_picker.search | api | master-data/products/product-picker/search | master_data.gia_von_hang_hoa.view (công ty chứng từ) |  | cột giá vốn |

## Route băm nội dung (bodysnap)

| id | app | url | mã | đo gì |
|---|---|---|---|---|
| x.api.customers.my_permissions | api | assign/customers/my-permissions | master_data.khach_hang.* | cờ quyền KH (CustomerPermissionHelper) |
| x.api.products.show | api | master-data/products/{id} | master_data.thong_tin_hang_hoa.manage | can_build (ProductDetailResource) |
| x.api.products.warehouse | api | master-data/products/warehouse | master_data.thong_tin_hang_hoa.manage | can_build từng dòng |
| x.api.quotations.show | api | assign/quotations/{id} | master_data.gia_von_hang_hoa.view | giá vốn báo giá |
| x.api.bom_lists.show | api | assign/bom-lists/{id} | master_data.gia_von_hang_hoa.view | can_view_cost_price |
| x.api.product_imports.index | api | finance/product-imports | master_data.gia_von_hang_hoa.view | cột giá vốn danh sách |
| x.api.borrow_exports.show | api | finance/borrow-exports/{id} | master_data.gia_von_hang_hoa.view | giá vốn |
| x.api.price_calculate_requests.show | api | master-data/price-calculate-requests/{id} | master_data.gia_von_hang_hoa.view | can_view_cost / isActor |
| x.api.price_calculates.show | api | master-data/price-calculates/{id} | master_data.gia_von_hang_hoa.view | giá vốn PTG |
| x.api.product_picker.items | api | master-data/products/product-picker/items | master_data.gia_von_hang_hoa.view | giá vốn popup chọn hàng |
| x.erp.menu.tmp_product_requests | erp | admin/sale/tmp_product_requests | topmenubar | tập link menu |
| x.erp.menu.home | erp | admin/customer_registers | topmenubar | tập link menu (trang khác) |
| x.erp.tmp_product_requests.index | erp | admin/sale/tmp_product_requests | master_data.yeu_cau_duyet_hang_tam.view | trang (cờ is_*) |
| x.erp.product2.edit | erp | admin/product2/{id}/edit | master_data.thong_tin_*.update + gia_hang_hoa.manage | can_step1..4, khối Quản lý giá |
| x.erp.product2.create | erp | admin/product2/create | master_data.thong_tin_*.update | can_step1..4 |
| x.erp.products.show | erp | admin/products/{id}/show | master_data.gia_hang_hoa.manage + lich_su_hang_hoa.view | khối Quản lý giá, link lịch sử |
| x.erp.products.edit | erp | admin/products/{id}/edit | master_data.gia_hang_hoa.manage | khối Quản lý giá |
| x.erp.product_templates.show | erp | admin/product_templates/{id}/show | master_data.gia_hang_hoa.manage | khối Quản lý giá |
| x.erp.tmp_products.show | erp | admin/tmp_products/{id}/show | master_data.gia_hang_hoa.manage | khối Quản lý giá |
| x.erp.products.getProductsAndPrices | erp_json | admin/products/getProductsAndPrices | master_data.gia_hang_hoa.update | cột giá vốn |
| x.erp.products.searchData | erp_json | admin/products/searchData | master_data.lich_su_hang_hoa.view | link lịch sử trong cột thao tác |
| x.erp.customer_groups.index | erp | admin/customer_groups | master_data.nhom_khach_hang.create | nút Thêm |
| x.erp.customer_groups.searchData | erp_json | admin/customer_groups/searchData | master_data.nhom_khach_hang.update/delete | nút dòng |
| x.erp.groups.index | erp | admin/groups | master_data.nhom_hang_hoa.create | @can Thêm nhóm |
| x.erp.device_errors.index | erp | admin/sale/device-errors | master_data.cong_viec_loi_thiet_bi.create | nút Thêm |
| x.erp.device_errors.searchData | erp_json | admin/sale/device-errors/searchData | master_data.cong_viec_loi_thiet_bi.* | cờ dòng |
| x.erp.delivery_specifications.index | erp | admin/orders/delivery_specifications | master_data.quy_cach_van_chuyen.manage | canCreate |
| x.erp.import_export_types.searchData | erp_json | admin/orders/import_export_types/searchData | master_data.loai_hinh_xnk.manage | nút dòng |
| x.erp.customers.manager | erp | admin/customers/{id}/manager | master_data.trang_thai_serial.update | canChangeSerialStatus |

## Không chụp
- GET ghi (delete / lock / unlock / restore / cancel / add-group / delete-*-equipment), export/print (file), `update-products`.
- Trang `{id}` không có id mẫu ổn định (suppliers rỗng trên rehearsal…).
- hrm-api `Modules/Human/Routes/api.php` 152–164: route employee-infos tên "Xem/Thêm/Sửa/Xóa hồ sơ" nằm trong khối comment `/* … */` — không chạy, không đổi.
