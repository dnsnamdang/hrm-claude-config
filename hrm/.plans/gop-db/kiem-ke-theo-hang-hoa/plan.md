# Kiểm kê theo hàng hóa (Phiếu kiểm kê) — Plan

> @khoipv · nhánh `feat/chuyen-doi-hang-hoa` (từ `gop_db`) · Spec: `docs/superpowers/specs/gop-db/2026-10-20-kiem-ke-theo-hang-hoa-design.md`
> Khuôn: màn anh em **Kiểm kê theo vị trí** (`Modules/Finance/*PositionInventoryResult*`, `pages/warehouse/position-inventory-results`)
> + màn cha **Kế hoạch kiểm kê theo hàng hóa** (`*SelfInventoryRequest*`, `pages/finance/self-inventory-requests`).

## Phase 0 — Khảo sát
- [x] Đọc controller/model/blade/JS class ERP `self_inventories` (danh sách, form, chi tiết, quyền, trạng thái, luồng) + dữ liệu thật
- [x] Chốt với user 20/10 (spec mục 3): điều chuyển → HRM, nhập/xuất → ERP; 3 quyền tên y ERP type 21; popup kế hoạch y ERP; làm hết phần phụ như ERP

## Phase 1 — BE (`Modules/Finance`)
- [x] B1. 3 quyền trong `PermissionsTableSeeder` (type 21, group "Kiểm kê theo hàng hóa") + `permission:sync --dry-run`
- [x] B2. Entities `SelfInventory/*` (phiếu + 9 bảng con): STATUSES màu SRS, quyền, `scopedQuery` (type all / wait-approve), cờ (`canEdit/canUpdateResult/canApprove/canHandle/canTransfer/canInventoryImport/Export`), `needTransfer/needImport/needExport/handleCompleted`, `generateCode` `<cty>.KKK-NNNNN`
- [x] B3. Hàm tồn dùng chung: port `Product::getDataForInventory` (vị trí + lô có tồn, lọc công ty thuê) + `lotStockOfProducts` (Làm mới số liệu) — grep trước, đặt service theo chủ đề tồn vật lý
- [x] B4. `SelfInventoryService` (list/filter/sort/export-rows/print-list/filter-options/detail)
- [x] B5. `SelfInventoryWriteService`: form-options (kho, công ty thuê theo kho, NV + chức vụ), popup kế hoạch (union y ERP), plan-data, product-data, lot-stocks, store/update (validate, phiếu treo → popup, chặn hàng trùng kế hoạch tổng, kế hoạch → Đã lập kiểm kê), destroy, saveResult (+ Hàng thừa khác, file kết quả S3, thông báo Kế toán kho), approve/reject (thông báo), lịch sử
- [x] B6. FormRequest + Controller + routes `/self-inventories` + đăng ký `catalog_histories` (GATED)
- [x] B7. In (mẫu 292 phiếu / 291 danh sách, letterhead công ty phiếu) + Xuất Excel phiếu
- [x] B8. Nối màn khác: Kế hoạch theo hàng hóa nút Lập phiếu → HRM (gỡ `ERP_RESULT_CREATE_PATH`); Phiếu điều chuyển vị trí nhận `self_inventory_id` (source + store + cập nhật trạng thái phiếu KK) — test lại 2 màn đó
- [x] B9. Smoke test HTTP kernel toàn luồng + dọn dữ liệu test theo id

### Checkpoint — 2026-10-20 (Phase 1 BE xong)
Vừa hoàn thành: B1–B9 — 3 quyền seeder (dry-run OK, chưa sync thật); Entities `SelfInventory/*` (+ `SelfInventoryRequestAll` chỉ đọc);
`PhysicalStockReader` (port `getDataForInventory` + `lotStockOfProducts`); `SelfInventoryService` / `WriteService` / `AttachmentService` /
`PrintService` + `SelfInventoryExport` + blade; FormRequest Store / SaveResult; controller + 23 route `/self-inventories`;
`catalog_histories` GATED `self_inventories`; màn Kế hoạch: `erp_result_path` → `result_create_path` (HRM); Phiếu điều chuyển vị trí:
`GET /position-transfers/source-self/{id}` + store/update nhận `self_inventory_id`. Smoke HTTP kernel trong transaction rollback: 84/84 PASS
(Super admin 77 + NV thường 7). API contract thực tế: spec mục 8.
Đang làm dở: —
Bước tiếp theo: Phase 2 FE (F1–F6); FE màn Kế hoạch đổi `erp_result_path` → `result_create_path`, màn Phiếu điều chuyển đọc `?self_inventory_id=`.
Blocked:

## Fix 20/10 — user chốt lại 2 điểm "y ERP" sau Phase 1
- [x] Gỡ chặn phiếu nhập/xuất treo khi Lưu & gửi (ERP `checkPending` không bao giờ chặn) — `SelfInventoryController::blockedResponse`, bỏ `PENDING_MESSAGE` + `SelfInventoryWriteService::pendingVouchers()`
- [x] Thêm hàng trả MỌI lô `qty != 0` trong vị trí (công ty thuê chỉ để chọn vị trí) — `PhysicalStockReader::inventoryProducts`; kiểm tinker: SP 35182 kho 4 lọc TPE vẫn ra lô TPSG

## Phase 2 — FE (`pages/warehouse/self-inventories`)
- [x] F1. Danh sách `index.vue` (+ `?type=wait-approve`), row-actions, export-excel, In danh sách, Lịch sử
- [x] F2. Form dùng chung: thông tin chung + popup chọn kế hoạch, kho + công ty thuê (đổi thì xoá hàng, hỏi xác nhận), bảng hàng rowspan + ĐVT tách dòng, Làm mới số liệu, hội đồng, Hàng thừa khác, file kết quả, popup phiếu treo
- [x] F3. create / _id/edit / _id/index: footer theo cờ (Lưu / Lưu & gửi / Gửi duyệt / Duyệt / Không duyệt / 3 nút Xử lý / In / Xuất), 404
- [x] F4. Menu: Kho › Kiểm kho "Kiểm kê theo hàng hóa" → link; Tài chính › Kiểm kê thêm "Phiếu kiểm kê theo hàng hóa chờ duyệt kết quả"
- [x] F5. Màn Kế hoạch: Lập phiếu → HRM; màn Phiếu điều chuyển vị trí: tạo từ `?self_inventory_id=`
- [x] F6. Checklist skill erp-to-hrm-screen (grep) + compile

### Checkpoint — 2026-10-20 (Phase 2 FE xong, chưa mở trình duyệt)
Vừa hoàn thành: F1–F6 — `pages/warehouse/self-inventories/` (index + create + _id/edit + _id/index, components: SelfInventoryForm,
PlanPickerModal, row-actions, export-excel, product-tree). Dùng lại KHÔNG sửa: `position-inventory-results/components/result-units.js`
(ĐVT tách dòng) + `ApproveNoteModal.vue`, `AttachmentSection` (api-base), `SystemInfoSection`, `CatalogHistoryModal`.
Không dùng `PendingVouchersModal` (BE đã gỡ chặn phiếu treo 20/10). Menu: Kho › Kiểm kho "Kiểm kê theo hàng hóa" có link;
Tài chính › Kiểm kê thêm "Phiếu kiểm kê theo hàng hóa chờ duyệt kết quả" (`?type=wait-approve`, trang có watcher query).
Màn Kế hoạch: Lập phiếu → `result_create_path` (HRM, cùng tab). Phiếu điều chuyển vị trí: `?self_inventory_id=` →
`/source-self/{id}`, gửi `self_inventory_id`; list/chi tiết nguồn `self_inventory` link HRM.
Grep checklist skill sạch; parse vue-template-compiler + @babel/parser 16 file OK; nuxt dev :3000 trả 200, chunk không lỗi build.
Đang làm dở: —
Bước tiếp theo: V1 — user mở trình duyệt kiểm toàn luồng (tạo tay / từ KH theo HH / từ KH tổng, Làm mới số liệu, đổi ĐVT,
Gửi duyệt + Hàng thừa khác + file, Duyệt / Không duyệt, Tạo phiếu điều chuyển).
Blocked:

## Phase 3 — Kiểm chứng
- [x] V1a. Playwright toàn luồng 20/10 (DNS Admin, trình duyệt riêng headless): danh sách/sort/số dòng/lọc nâng cao, validate trống,
  tạo tay (kho → tự điền công ty thuê, chọn hàng, hội đồng → chức vụ tự chọn), sửa + đổi ĐVT Can (tồn lô quy đổi 161),
  Lưu và gửi, nhập Thực kiểm + Hàng thừa khác + file PNG, Gửi duyệt, `?type=wait-approve`, Không duyệt → gửi lại → Duyệt,
  nút xuất kho → ERP tab mới, In, Xuất Excel, Lịch sử; lập từ KH theo HH (KH → Đã lập), Tạo phiếu điều chuyển vị trí (nháp,
  `tmp_position_transfer_details` có `self_inventory_result_id`, phiếu KK → Đang xử lý); nút Lập phiếu ở màn Kế hoạch.
  Dọn theo id: phiếu 874/875, PĐCVT 948, lịch sử 1226–1240, 1 thông báo, KH 6 trả status 1 — DB về đúng mốc.
  Chưa test được: KH tổng kiểm kê (bảng `self_inventory_request_alls` local rỗng), bấm "Điều chuyển" thật (đụng tồn kho), NV thường.
- [x] Fix 20/10 (user): Ghi chú cùng hàng Công ty thuê kho — `SelfInventoryForm.vue` col-md-8 (Thêm) / col-md-4 (Sửa, Chi tiết)
- [x] Fix 20/10 (user): Lịch sử dòng SỬA kết quả kiểm kê chỉ in tên hàng + trường đổi — `SelfInventoryWriteService::loadVirtualRows`
  dòng kết quả `__brief` → `true` (bỏ phụ chú Vị trí / Lô / ĐVT). Log đã ghi trước giữ nguyên hiển thị cũ.
- [ ] V1b. Chờ user chốt: bảng hàng ở bước nhập kết quả rộng ~1.780px > khung 1.336px → cột Thực kiểm / Chênh lệch / Ghi chú khuất phải
- [ ] V1c. Chờ user chốt: phiếu rác id 97 (status 0, không mã) hiện badge "0" ở danh sách

## Rà sau Phase 2 (20/10)
- [x] Nhãn 2 nút Xử lý theo ERP: "Tạo phiếu nhập kho điều chuyển" / "Tạo phiếu xuất kho điều chuyển" (subagent đặt "điều chỉnh")
- [x] Grep checklist + fail-open trên `pages/warehouse/self-inventories`: sạch
- Giữ: "Duyệt kết quả" (đồng bộ màn anh em + popup dùng chung); khối file tiêu đề "File đính kèm" (component chung); cột Kế hoạch KK ở danh sách là chữ (ERP danh sách không có cột này); Hàng thừa khác dùng `position-inventory-results/structure` + `master-data/units/getAll` (route không gate quyền)
