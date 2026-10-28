# Plan — Cấu hình chặn luồng hàng quá hạn (@khoipv)

## Phase 1 — Port màn
### BE (`hrm-api`)
- [x] Quyền 1706 `Cấu hình chặn luồng hàng quá hạn` (type 10) vào `PermissionsTableSeeder` + insert DB local (chưa gán vai trò nào)
- [x] `Modules/Finance/Services/DueConfigService.php` (show: mục theo tab + công ty `status=1` + mục đang tích; update: diff từng công ty, ghi pivot, ghi log)
- [x] `Modules/Finance/Http/Controllers/V1/DueConfigController.php` + route `GET/PUT /v1/finance/due-configs` (checkPermission)
- [x] Đăng ký `CatalogHistoryService::TABLES['company_due_configs']` + nhãn nhóm trong `rowItemLabel()` (thuần thêm)
- [x] Migration dữ liệu `2026_10_13_000001_move_due_config_histories_to_catalog_histories` — đã chạy local: 204 dòng ERP → 212 log, đọc ngược đủ 922 thay đổi
- [x] Smoke test API qua HTTP kernel: không quyền 403 (GET/PUT); có quyền GET 200 (3 nhóm/21 mục, 31 mục, 5 công ty); PUT đổi → 200 + log đúng (+/−); PUT y nguyên → không log; công ty lạ / đã ngừng → 422; payload rỗng → 422; hoàn tác cấu hình công ty 3 về nguyên trạng. Đã xoá 2 log test (id 953, 954) + gỡ quyền tạm.
### FE (`hrm-client`)
- [x] `pages/admin/due-configs/index.vue` — V2BaseFormSection + 2 tầng V2BaseTabNavigation + V2BaseCheckbox + V2Footer (Lưu) + SystemInfoSection theo công ty; unsavedChangesMixin
- [x] Menu `components/subsystem-menu/admin.js` dưới "Hệ số công nghệ theo nhóm hàng hóa", `isShow` theo quyền mới
- [x] Compile FE (vue-template-compiler + babel): OK
- [ ] User gán quyền 1706 cho vai trò rồi mở trình duyệt kiểm (CHƯA bấm thật)

### Checkpoint — 2026-10-13
Vừa hoàn thành: BE + FE + migration lịch sử, smoke test API pass, compile FE pass. Đã push develop (api de0a3a485, client 03d265cd9).
Đang làm dở: không.
Bước tiếp theo: admin gán quyền "Cấu hình chặn luồng hàng quá hạn" → mở `/admin/due-configs` kiểm tích/bỏ tích, Lưu, lịch sử từng công ty, cảnh báo chưa lưu.
Blocked:


## Dời menu sang Bán hàng (15/10)
- [x] Gỡ mục khỏi `components/subsystem-menu/admin.js`, thêm vào `sale-hub.js` › Quy chế - Thiết lập › Thiết lập (route giữ `/admin/...`)
- [ ] User mở trình duyệt kiểm sidebar Bán hàng

## Redmine #11709 (17/10)
- [x] Bug 1: tiêu đề "Chi tiết chặn" thêm `(*)` đỏ như ERP (`edit.blade.php:35`) + bỏ khoảng trống trên khối (padding-top 8px của trang)
- [x] Bug 2 (user chốt "làm như ERP"): màn YC nhập hàng HRM trước đây KHÔNG có chặn hàng quá hạn nào. Port ERP `checkDueConfigs` trên productImportRequest.create/store/update:
  - BE `DueConfigBlockService::importRequestBlockedReason()` (hàm mới) + middleware mới `CheckProductImportRequestDueConfig` gắn vào POST/PUT + `GET /product-import-requests/create-check` (:create)
  - Đúng ERP: mở màn tạo chỉ chặn nhóm hàng giữ + nhập thẳng; lưu loại 3 (mượn trả lại) được miễn nhóm hàng mượn; bỏ tích thì không chặn
  - FE `ProductImportRequestForm` màn tạo gọi create-check, 423 -> toast cảnh báo + về danh sách; lưu bị 423 dùng toast có sẵn
- [x] Smoke test HTTP: emp 27 (hàng giữ QH, cty 1) create-check/lưu -> 423 "Có hàng giữ quá hạn!"; emp 590 (hàng mượn QH) create-check 200, lưu loại 1 -> 423, loại 3 -> lọt qua tới validate 422 (không ghi gì)
- [x] Khớp ERP nhóm hàng nhập thẳng khi công ty chưa khai `overdue_date_export_direct` (user duyệt sửa hàm chung 17/10): `hasOverdue(..., $self)` — tab 1 (chặn chính người lập, ERP middleware `CheckDueConfigs`) coi mọi dòng còn tồn là quá hạn; tab 2 (chặn TP duyệt, ERP `isManagerBlocked` có `> 0`) giữ không tính. Hiện cty 5/6/7 (null) chưa tích cấu hình + không có dòng tồn nên chưa ảnh hưởng thực tế
- [ ] User mở trình duyệt kiểm (chưa bấm thật)

### Checkpoint — 2026-10-17
Vừa hoàn thành: #11709 bug 1 (tiêu đề (*) + bỏ khoảng trống trên khối) + bug 2 (chặn hàng quá hạn ở YC nhập hàng như ERP).
Đang làm dở: không.
Bước tiếp theo: user kiểm trên trình duyệt `/admin/due-configs` và `/finance/product-import-requests/create`.
Blocked:

## Redmine #11722 (17/10) — "chưa chặn luồng bên HRM"
- [x] YC nhập hàng: đã chặn lập ở #11709 (ảnh tester chụp trước khi sửa). Local không tái hiện được (NV 787 không còn hàng quá hạn trên DB local)
- [x] Rà toàn bộ: 11 thao tác đã port mà chưa chặn (xem báo cáo chat 17/10) + lỗi tên `Duyệt kết quả công tác trên HRM)` dư `)` ở Assign/Routes/api.php:1220
- [x] Chờ user chốt phạm vi sửa → 20/10 user chốt: sửa CẢ tab 1 + tab 2 như ERP, code ngay trên nhánh hiện tại `feat/chuyen-doi-hang-hoa`

## Redmine #11722 phản hồi (20/10) — gắn chặn cho mọi thao tác ERP có `checkDueConfigs(Manager)`
Tester 20/10: tích "Hàng giữ quá hạn › Lập YC nhập hàng", tạo YC nhập hàng vẫn lọt + "check luôn các phần khác".
Local: NV 265 (Lại Văn Hiệp, cty 4, 63 dòng giữ quá hạn) create-check/lưu → 423 đúng. Phần còn lại chưa gắn chặn.
### BE
- [x] Service: tab 1 xét nhóm theo thứ tự cố định ERP (giữ → mượn → nhập thẳng); nhóm hàng mượn tab 1 join `warehouse_export_requests` + `warehouses` như ERP `CheckDueConfigs`
- [x] Service: `exportRequestBlockedReason()` — ngoại lệ ERP của YC xuất hàng (mọi hàng trong phiếu đều là hàng mình đang giữ quá hạn, hoặc xuất thẳng → cho qua)
- [x] Service: `createBlockedReason()` cho màn TẠO (YC nhập hàng giữ ngoại lệ cũ; YC xuất hàng ERP không chặn mở màn)
- [x] Endpoint chung `GET /v1/finance/due-configs/create-check?action=...` (không gate quyền)
- [x] Gắn tab 1: báo giá (store/update/create-and-submit/create-from-bom), báo giá DV BH-SC (wr-quotations store/update), hợp đồng (store/update), HĐ DV BH-SC (store/update), YC xuất hàng (store/update + từ HĐ), hàng hoá (store/take/update/admin-data/destroy), duyệt hàng tạm (tempSave/approve/reject), gia hạn + điều chuyển hàng giữ (store/update)
- [x] Gắn tab 2: duyệt YC nhập hàng (3 cấp), gia hạn/điều chuyển hàng giữ approve, hợp đồng bán approve, đề nghị thanh toán (store/update/approve như ERP), xuất bán hàng mượn manager-approve
- [x] Sửa tên `Duyệt kết quả công tác trên HRM)` dư `)` ở Assign/Routes/api.php (assign_business update)
- [x] Smoke test HTTP kernel: NV 265 bị 423 ở từng nhóm route; NV không quá hạn lọt qua
### FE
- [x] Helper/mixin gọi create-check khi mở màn tạo (+ màn sửa hàng hoá / hàng tạm như ERP) → 423 toast + quay về danh sách
- [x] Gắn vào: báo giá, báo giá DV, hợp đồng, HĐ DV, hàng hoá (tạo/sửa), hàng tạm, gia hạn + điều chuyển hàng giữ
- [x] Kiểm form lưu / nút duyệt có hiện message 423 của BE (đều đọc `response.data.message`)
- [x] Compile FE
- [ ] User mở trình duyệt kiểm (CHƯA bấm thật) + đẩy lên dev cho tester

Ghi chú khác ERP / chưa port (không gắn được vì HRM chưa có màn): YC xuất hàng TP duyệt + switchBoardOfManager, YCNH switchBoardManager,
phụ lục HĐ / HĐ nguyên tắc, HĐ mua, YC đặt hàng, lắp đặt bàn giao, giá VC quốc tế, product.copy/restore/deleted.
Super Admin: HRM bỏ qua theo role 18 (`Super admin`, guard api); ERP bỏ qua role `Super Admin` (guard web, id 100002 trên DB gộp) — chưa đổi.

### Checkpoint — 2026-10-20
Vừa hoàn thành: #11722 phản hồi — gắn chặn hàng quá hạn cho toàn bộ route ERP có `checkDueConfigs(Manager)` đã port sang HRM (tab 1 + tab 2) + chặn mở màn tạo ở FE. Smoke HTTP: NV 265 → 423 ở báo giá (4 lối), HĐ, báo giá DV, HĐ DV, YC xuất hàng, create-check; xuất thẳng / xuất đúng hàng đang giữ → lọt; NV 222 (không quá hạn) → 200; TP 233 duyệt gia hạn hàng giữ → 423. Compile FE 10 file OK.
Đang làm dở: không. Đã commit + push nhánh `feat/chuyen-doi-hang-hoa` (api afb74a09d, client bb913e1c8) — chưa vào develop/gop_db.
Bước tiếp theo: user kiểm trình duyệt bằng tài khoản người còn hàng giữ quá hạn (vd Lại Văn Hiệp) → commit/đẩy dev → trả lời tester.
Blocked:
