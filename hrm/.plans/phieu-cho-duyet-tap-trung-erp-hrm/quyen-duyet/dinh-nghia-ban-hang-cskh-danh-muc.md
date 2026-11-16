# Định nghĩa loại phiếu — nhóm Bán hàng · CSKH · Vận chuyển · Danh mục dùng chung — @cuong61n

Ngày 16/11/2026. Kết quả triển khai `ApprovalDefinition` cho nhóm này (đối chiếu code `hrm-api` nhánh `gop_db-main`, DB local `local_hrm_erp`). Báo cáo gốc: `05-ban-hang-cskh-danh-muc.md`. Mọi loại dưới đây đã: Definition + trait `SyncsApprovalInbox` trên model nguồn + `seedTest`/`deleteTest` + test PHPUnit + kiểm thử đột biến + `approval-inbox:verify` 0 chênh lệch + gọi API thật `GET /api/v1/approval-center/inbox?doc_type=…`.

Thư mục: `Modules/ApprovalCenter/Definitions/{CustomerCare,Transport,Sale,MasterData}/` · test `tests/Feature/ApprovalCenter/{CustomerCare,Transport,Sale,MasterData}/` · helper test mới `tests/Feature/ApprovalCenter/Concerns/{VerifiesWithExplicitTesters,GrantsTestRoles}.php`.

## 1. Quy tắc chung đã chốt khi viết

- **Người duyệt gắn với "công ty đang làm"**: quyền (`PermissionLookup::holders($mã, $công_ty)`) tính theo công ty đang làm; còn các phép "cùng công ty / cùng phòng / quản lý phòng" của code gốc lại so theo **công ty GỐC** (`employee_infos.company_id`) hoặc `auth()->user()->info->company_id` — Definition dùng đúng như vậy, không đổi sang công ty đang làm.
- **Loại không xét công ty / quyền** (HĐ SC-BD-BT): người duyệt được gắn với **mọi công ty** trong bảng `companies` (cổng không phụ thuộc công ty đang làm).
- **Màn chi tiết là cửa vào thật**: nút Duyệt nằm ở màn chi tiết; nơi nào `show` chặn bằng quyền xem (THGVC, HĐ vận chuyển) thì Definition = `canView && canApprove` (người chỉ có quyền Duyệt mà không mở được phiếu thì không vào danh sách). Đây là điểm cần chốt ở mục 4.

## 2. Bảng loại đã làm

| doc_type | Màn gốc (route FE) | Cấp | Gate (tóm tắt) | Pending thật local | Verify / test |
|---|---|---|---|---|---|
| `wr_service_contract` | `/customer-care/wr-service-contracts/{id}` (menu Bán hàng › Phê duyệt › HĐ chờ duyệt) | 1: Chờ duyệt | `approver_id` có ⇒ CHỈ người đó; không có ⇒ người có dòng quản lý ĐÚNG phòng HĐ tại công ty gốc (không cờ tổng, không phòng ngồi). Không cần mã quyền, mọi công ty | 2 (+6 seed) | verify 103.920 cặp / 0 chênh; PHPUnit 2.750 cặp, 190 duyệt thật; đột biến 7/7 |
| `wr_import_result` | `/customer-care/wr-import-results/{id}/approve` | 1: Chờ duyệt kết quả · 2: Đang duyệt kết quả | Cấp 1: `customer_care.phieu_nhap_ket_qua.approve` (công ty đang làm) + công ty gốc = công ty phiếu. Cấp 2: chỉ người tạo phiếu duyệt nháp | 197 + 2 | verify 14.760 cặp / 0; PHPUnit 4.000 cặp, 52 duyệt thật; đột biến 5/6 (1 tương đương) |
| `other_delivery_trip` | `/transport/other-delivery-trips/{id}` | 1: Chờ duyệt | qua đủ 3 cổng của endpoint: Thủ kho (`warehouse.thu_kho.manage`) → xem được phiếu (người tạo · cùng công ty gốc + Duyệt · xem tổng công ty · phòng ban) → Duyệt (`warehouse.chuyen_xe_khac.approve`) | 2 (+8 seed) | verify 31.960 cặp / 0; PHPUnit 5.760 cặp, 269 duyệt thật; đột biến 10/10 |
| `delivery_cost_summary` | `/transport/delivery-cost-summaries/{id}` | 1: Chờ duyệt | `warehouse.gia_van_chuyen.approve` + mở được phiếu (`canView`) | 0 (+8 seed) | verify 16.448 cặp / 0; PHPUnit 1.920 cặp, 134 duyệt thật; đột biến 8/8 |
| `delivery_contract` (HĐ + phụ lục) | `/transport/delivery-contracts/{id}` | 1: Chờ duyệt | `warehouse.gia_van_chuyen.approve` + thấy phiếu theo `scoped()` (quyền xem rộng nhất thắng, không cộng dồn; người lập; `approver_id`) | 0 (+8 seed) | verify 16.448 cặp / 0; PHPUnit 1.560 cặp, 98 duyệt thật; đột biến 9/9 |

Các loại Bán hàng › Phê duyệt (Sale) và Danh mục dùng chung (MasterData): xem mục 5.

## 3. Loại KHÔNG đăng ký (đã đọc lại code, không để file Definition)

| Loại | Lý do |
|---|---|
| Biên bản bàn giao sơ bộ (`handover_records`) | BE không kiểm người duyệt (`canApprove` chỉ xét `status = 2`, "ai cũng duyệt được" — user chốt 04/11); `approver_id` chỉ dùng gửi thông báo ⇒ không biểu diễn được bằng logic đáng tin, nếu đăng ký `approver_id` sẽ HẸP hơn thực tế BE cho phép. Cần user chốt giữ y ERP hay siết `approver_id`. |
| Yêu cầu đi kiểm tra sửa chữa - bảo hành (`warranty_repair_requests`) | Hàng đợi tiếp nhận của phòng (thao tác chính là "Tạo phiếu xử lý yêu cầu"), "Từ chối / chuyển phòng" chỉ là phụ; không nằm trong menu Phê duyệt. Gate nếu cần: `…yeu_cau_di_kiem_tra_sua_chua_bao_hanh.confirm` + phòng tiếp nhận = phòng ngồi của người xem + chưa có phiếu xử lý (cần kiểu "phòng của tôi" — Definition riêng). **Cần user quyết có đưa vào không.** |
| Phiếu xử lý yêu cầu "Chờ CCTT" (A4), Phiếu cung cấp thông tin "chờ làm báo giá" (A5, wr-information-requests) | Hàng đợi công việc (làm phiếu / báo giá); "từ chối" chỉ là thao tác phụ — brief nói rõ không phải duyệt. |
| HĐ dịch vụ chờ tiếp nhận (A6), Yêu cầu giao việc khác (A7) | Hàng đợi tiếp nhận công việc của phòng, không có người duyệt xác định. |
| Phụ lục HĐ dịch vụ SC-BD-BT (type 3/4) | Không có route duyệt trên HRM (`contractOrFail` ép `type = 1`), chỉ duyệt được trên ERP. (Phụ lục HĐ **vận chuyển** thì có và nằm trong `delivery_contract`.) |
| Chuyến xe khác "Chờ hạch toán" (status 1) | Nút "Hạch toán" mở màn phiếu hạch toán bên ERP; HRM chỉ có "Không duyệt" của kế toán ⇒ nửa luồng. |

## 4. Điểm cần người điều phối / user quyết

1. **THGVC & HĐ vận chuyển — "thấy" vs "duyệt được"**: endpoint `approve` chỉ cần quyền Duyệt (xuyên công ty, không xét xem), nhưng nút Duyệt nằm ở màn chi tiết mà `show` chặn bằng quyền xem. Mình chọn `canView && canApprove` (giống đúng những gì người dùng làm được trên UI). Nếu muốn "mọi người giữ quyền Duyệt đều thấy" thì phải mở quyền xem hoặc đổi `show` — việc ngoài phạm vi.
2. **Chuyến xe khác**: menu "chờ duyệt" chỉ kiểm "Duyệt chuyến xe khác" nhưng mọi API đòi thêm "Thủ kho" — người thiếu "Thủ kho" thấy menu nhưng 403; Definition theo endpoint (cần cả hai) nên không hiện cho họ.
3. **HĐ SC-BD-BT**: `approver_id` = 0 nghĩa là chưa chọn (không phải NULL). ERP ghi `approver_id` lúc lập HĐ (dữ liệu local: mọi HĐ đều mang cột này); HRM không có ô nhập.
4. **PNKQ cấp 2**: người khác (có quyền duyệt) không tiếp tục được phiếu "Đang duyệt kết quả" mà người A đã mở; dòng bảng gom chỉ hiện cho A (đúng code gốc).

## 5. Bán hàng › Phê duyệt (Sale) và MasterData

| doc_type | Màn gốc (route FE) | Cấp / gate | Pending thật local | Verify / test |
|---|---|---|---|---|
| `business_target_department` | `/finance/business-target-departments/{id}` | status 2 "Chờ duyệt"; mã `sale.chi_tieu_kinh_doanh_phong_ban.approve` (công ty đang làm) VÀ công ty GỐC của người duyệt = công ty phiếu | 0 | verify 5.022 cặp / 0; đột biến 5/5 |
| `business_target_employee` | `/finance/business-target-employees/{id}` | như trên, mã `…chi_tieu_kinh_doanh_nhan_vien.approve` | 0 | verify 5.022 / 0; chung bộ test |
| `division_market_employee` | `/finance/division-market-employees/{id}` | status 3 "Chờ duyệt"; mã `sale.phan_chia_thi_truong_nhan_vien.approve`, cùng luật công ty gốc | 0 | verify 4.986 / 0; đột biến 3/3 |
| `price_asking_request` (YCHG chờ PTKD) | `/sale/price-asking-requests/{id}` | status 2; mã PTKD (`finance.yeu_cau_hoi_gia.approve`), công ty phiếu = công ty đang làm, và phải THẤY phiếu (người lập hoặc phạm vi `sale.yeu_cau_hoi_gia.view`) | 4 | verify 9.040 / 0; đột biến 4/4 (+4/5 trên helper phạm vi xem, 1 tương đương) |
| `price_asking_group` (nhóm hàng chờ XNK) | cùng màn YCHG | nhóm status 5, YCHG đang hỏi giá; người duyệt = XNK phân công hiện hành tra ĐỘNG từ `assign_histories` (thương hiệu × hãng × công ty) + mã `finance.yeu_cau_hoi_gia.update` + thấy phiếu | 0 (bảng nhóm đang rỗng) | verify 5.424 / 0; đột biến 7/7 |
| `product_price_approval` (Duyệt giá bán hàng hoá) | `/finance/product-price-approvals` | mỗi dòng `product_approves` tồn tại = một yêu cầu chờ (không có status, duyệt xong xoá dòng); mã `finance.gia_ban_hang_hoa.approve` + `company_id` = công ty đang làm | 0 | verify 4.920 / 0; đột biến 4/4 |

Model đã gắn trait: `BusinessTargetCompany`, `BusinessTargetForDepartment`, `DivisionMarketDepartmentEmployee` (Finance); `PriceAskingRequest` (kèm `booted()` sync lại các nhóm khi phiếu đổi trạng thái), `PriceAskingRequestGroup`, `ProductApprove` (MasterData).

**Hoãn / bỏ**
- **Kế hoạch bán hàng / phát triển thị trường của nhân viên (`sale-plan-employees`, `market-plan-employees`)**: HOÃN — cột `form_version` chưa có ở DB local (migration `2026_11_14_000001` chưa chạy, không được migrate) nên `canApprove` luôn false, không kiểm chứng được. Gate đã đọc xong để làm sau: cấp "Chờ TP duyệt" = mã duyệt ở công ty đang làm VÀ (dòng quản lý phòng ở bất kỳ công ty, hoặc cùng phòng) VÀ khác người lập, phiếu HRM (`form_version = 2`); cấp "Gửi BGĐ" thêm điều kiện `canView` (endpoint `findOr404`); cấp BGĐ không có màn duyệt trên HRM.
- Phân chia thị trường theo phòng ban: bỏ (chỉ Đang tạo → Đã duyệt, không có trạng thái chờ).
- Hàng tạm trong YCHG: bỏ (duyệt ngay trong form YCHG, cùng cổng PTKD — chi tiết của `price_asking_request`).
- YCTG "Chờ tính giá": bỏ (hàng đợi công việc). Phiếu tính giá "Chờ duyệt giá": bỏ vì trùng với `product_price_approval`.

**Chỗ ghi bằng query builder đã gọi `scheduleSync`** (nhóm này): `PriceAskingRequestWriter` (nhóm chuyển sang công ty quản lý), `PriceAskingStaleCloser`, `PriceAskingGroupBackfill`; và 8 chỗ xoá/sửa `product_approves`: `ProductPriceApprovalService` (duyệt + từ chối), `ProductPriceApprovalSubmitter` (xoá + update), `ManufacturePriceModeService`, `ProductLifecycleService`, `InheritedPriceSync`, `ProductPriceSetWriter`, `ProductPriceWriter`. Dòng `product_approves` bị xoá ghi là "Đóng" (không phân biệt Duyệt / Không duyệt vì dòng bị xoá cứng).

**Lỗi / lệch của code gốc**: YCHG — người chỉ có mã PTKD / XNK mà không thấy phiếu thì endpoint trả 404 (`assertWritable`) nhưng nút vẫn hiện ở nhiều nơi. Phân chia thị trường theo nhân viên — `assertWithinLimit` có thể chặn lúc bấm Duyệt (khu vực khoá, vượt hạn mức), chỉ ghi ở `gate_blocker`. Chỉ tiêu và phân chia thị trường so công ty GỐC của người duyệt, không phải công ty đang làm.

**Bẫy cho Definition sau này**: `watchedTables()` KHÔNG được chứa chính bảng nguồn — refresher chạy giữa lúc insert và đọc `lastInsertId` ngoài giao dịch làm `$model->id = 0`. Cả hai nhóm đã bỏ bảng nguồn khỏi `watchedTables`.

## 6. Chỗ ghi bằng query builder đã xử lý

- `DeliveryContractService::closeContract()` cập nhật hàng loạt `delivery_contracts.status = 4` (đóng HĐ cùng NCC + kho khi duyệt HĐ khác) — kể cả HĐ đang "Chờ duyệt" ⇒ đã thêm `ApprovalInboxService::scheduleSync('delivery_contract', $id)` cho từng id bị đóng; outcome của HĐ đóng khi còn chờ = `STATE_CLOSED` (không phải "đã duyệt"). Đã kiểm thật ngoài giao dịch bằng script (tự dọn).
- Các loại còn lại: mọi chỗ ghi trạng thái đều qua Eloquent (`save()`), trait tự đồng bộ.

## 7. Lỗi / điều cần biết của code gốc (không sửa)

- HĐ SC-BD-BT: `managedDepartmentIds` ép `(int) NULL = 0` nên dòng quản lý không có phòng khớp HĐ không có phòng; không tính cờ `all_department`; docblock còn ghi "Super Admin" nhưng code không có.
- `ChecksEmployeePermission::currentCompanyId()` (dùng ở Chuyến xe khác) lấy **công ty gốc** làm "công ty hiện tại" trong khi quyền tính theo công ty đang làm ⇒ người kiêm nhiệm lệch giữa hai nơi.
- PNKQ: quyền xét ở công ty đang làm nhưng so công ty phiếu bằng công ty gốc (cùng kiểu lệch).
- Biên bản bàn giao sơ bộ: ai cũng duyệt được (đã chốt giữ y ERP, xem mục 3).

## 8. Hiệu năng

- `WrImportResultDefinition` KHÔNG theo dõi bảng `wr_assign_tasks` (đã gỡ): mỗi lần ghi bảng đó sẽ quét lại ~200 phiếu PNKQ (~1,7 giây, ~4.600 query); phiếu duyệt nháp luôn được ghi cùng lúc với trạng thái PNKQ qua Eloquent nên trait đã đồng bộ.
- `WrServiceContractDefinition` gắn người duyệt với mọi công ty ⇒ tối đa (số quản lý × 10) dòng người duyệt mỗi phiếu; phiếu chờ rất ít nên không đáng kể.
