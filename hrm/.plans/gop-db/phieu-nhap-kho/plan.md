# Plan — Phiếu nhập kho (ERP `warehouse_imports` → HRM)

> @junfoke · nhánh `gop_db` (cả 2 repo — hiện đứng `develop`, checkout từ `gop_db`) · bắt đầu 2026-10-15 · Redmine #11693
> Design: `.plans/gop-db/phieu-nhap-kho/design.md`
> Spec: `docs/superpowers/specs/gop-db/2026-10-15-phieu-nhap-kho-design.md`

**0 bảng mới, 0 migration. 3 quyền mới guard `api` (chờ chốt Q7).**
Ước lượng tổng đợt 1: **~21 công** (0,5 + 2,5 + 6 + 1,5 + 5,5 + 2,5 + 0,5 + 2; chưa gồm barcode / xuất lại / nhập lại).

---

## Phase 0 — Khảo sát (0,5 công) ✅

- [x] Đọc controller ERP 2.505 dòng, model 1.787 dòng, 12 blade, route group `warehouse_imports` (38 route)
- [x] Soi hết cửa vào menu ERP (all / for_approve / discrepancy / excShortage / forAccounting cũ)
- [x] Đo dữ liệu `gop_db` local: 8.887 phiếu, 13 loại có dữ liệu, phân bố status/step, 8 bảng tồn
- [x] Xác định chỗ HRM đang đọc/ghi `warehouse_imports` (ProductImportService, bill payment, chuyến xe, hàng đang về)
- [x] Xác nhận HRM chưa có writer tồn vật lý theo vị trí; chưa có popup vị trí / chuyến xe / tuyến đường
- [x] Viết spec + design + plan
- [ ] **User chốt Q1–Q13** (spec mục 10)

---

## Phase 1 — BE: Entity + API đọc (2,5 công)

- [ ] Entity mới `Entities/WarehouseImport/`: `WarehouseImport` (`$table`, STATUSES + màu SRS, STEP, quan hệ), `TmpWarehouseImportLot`,
      `TmpWarehouseImportLotDetail`, `WarehouseImportLot` (ghi được), `WarehouseImportLotDetail`, `WarehouseImportExportArrangeDelivery`,
      `…Executor` — giữ `Entities/Contract/WarehouseImport*` chỉ đọc cho 5 service cũ (Q10)
- [ ] `WarehouseImportService::scopedQuery()` port `searchByFilter type=all` (4 nhánh quyền + fallback của mình, ẩn nháp người khác,
      `company_id` null ⇒ `1 = 0`) + preset `for_approve` (status 2, công ty mình)
- [ ] Bộ lọc 11 ô + khoảng ngày + tổ chức; sort; cột "Người đề nghị"/"Người yêu cầu" (loại 7, loại 8 nhập ghép) không N+1
- [ ] `meta()` (loại, trạng thái, kho, NCC) · `show()` + cờ quyền `is_can_*` (edit / arrange / deny / cancel / create_product_import / view)
- [ ] Controller + routes `finance/warehouse-imports` (route tĩnh trước `/{id}`), gate trong Controller (trait 2 guard)
- [ ] 3 quyền "Xem phiếu nhập kho theo …" cuối `PermissionsTableSeeder`
- [ ] Smoke: index/show/meta, đối chiếu số phiếu theo scope với ERP cho 3-4 nhân viên mẫu

## Phase 2 — BE: Ghi (6 công)

- [ ] `PhysicalStockWriter::importLot()` (dùng chung, chờ Q12) — port `updateWarehouse()` 8 bảng, lock, `objectable_type` chuỗi class ERP,
      đọc `App\BaseModel` ERP để ghi đủ cột tự gán (`company_id`, `created_by`…)
- [ ] Kiểm kho: port `Product::checkInventory` + `Position::checkInventory` (chặn hàng/vị trí đang kiểm kho)
- [ ] `store()` — Request class port rule ERP + rule loại 7; tmp lots/details; bốc xếp + người nhận việc; chuyến xe; tabs;
      `generateCode()`; **duyệt ĐNNK** (ĐNNK → 1, YCNH → 4, thông báo) qua `WarehouseImportRequestService`
- [ ] `saveArrange()` (lưu nhóm + người đi xếp) + `printArrangeData()` (không ghi)
- [ ] `update()` Lưu / Gửi — lots xoá-ghi lại, file đính kèm (chờ Q8), chuyến xe/tuyến/km, bốc xếp; Gửi: loại 2 cập nhật đơn đặt hàng gốc
      (`root_order_request_*`), `PhysicalStockWriter`, `send()` (ĐNNK → 6, YCNH → 8, YC xuất nội bộ, thông báo KT kho); chuyến chờ duyệt ⇒ về 3
- [ ] `deny()` (lý do bắt buộc) · `cancel()` (gọi hủy ĐNNK có sẵn)
- [ ] Soát `ProductImportService::markParentUsed` có đủ bước `product_transfer_requests → 10` cho loại 7 như ERP `approve()` chưa
- [ ] **Đối chiếu song song**: 1 phiếu ERP ↔ 1 phiếu HRM cùng dữ liệu trên DB local → so từng dòng 8 bảng tồn + chứng từ cha, rollback/dọn

## Phase 3 — FE: Danh sách (1,5 công)

- [ ] `pages/finance/warehouse-imports/index.vue` theo skill `list-page` + `erp-to-hrm-screen` checklist A–C: 14 cột, cấu hình cột,
      ghi nhớ bộ lọc, badge `V2BaseBadge`, cột Tiến trình, link mã ĐNNK / phiếu cha "Nhập lại cho phiếu …"
- [ ] Menu hành động theo cờ BE: Xếp hàng / Nhập kho (Sửa) / Tạo phiếu nhập hàng / Hủy / In / Lịch sử (+ deep-link ERP Q4/Q5)

## Phase 4 — FE: Thêm / Xếp hàng / Nhập kho / Chi tiết (5,5 công)

- [ ] `create.vue` — popup chọn ĐNNK (status 2, thủ kho), nhận `?warehouse_import_request_id=`, bảng dòng hàng + nhiều vị trí/dòng,
      tab Vận chuyển + Bốc xếp (Q6), `unsavedChangesMixin`, `form-validate`
- [ ] Popup dùng chung mới: chọn vị trí kho (theo kho + hàng), chọn chuyến xe, chọn tuyến đường, chọn người nhận việc bốc xếp
- [ ] `_id/arrange.vue` — nhóm phiếu xếp hàng (kéo-thả), chọn người đi xếp, Lưu, In nhóm
- [ ] `_id/edit.vue` — Nhập kho: SL/vị trí thực, file (bắt buộc), Lưu / Gửi, xem trước bản in
- [ ] `_id/index.vue` — chi tiết + actionbar (Không duyệt + modal lý do, Tạo phiếu nhập hàng, Sửa, Hủy, In, Quay lại) + lịch sử

## Phase 5 — In · Excel · Lịch sử (2,5 công)

- [ ] In phiếu nhập kho mẫu ERP id 46 (`print-page`, letterhead theo `company_id` phiếu, path logo ghép `ERP_URL`)
- [ ] In phiếu đi xếp hàng mẫu ERP id 30
- [ ] Xuất Excel danh sách (`export-excel`, `ExportFieldsModal`), bộ lọc giống danh sách
- [ ] Lịch sử: đăng ký `warehouse_imports` vào `CatalogHistoryService::TABLES` + nhãn action (create / update / send / deny / cancel)
- [ ] (Đợt 2, nếu Q4 chốt port) In barcode 3 mẫu theo `barcode_template_type` (+1,5 công)

## Phase 6 — Nối luồng + menu (0,5 công)

- [ ] `finance.js:153` đổi `erpPath` → `link: '/finance/warehouse-imports'` (giữ thứ tự theo sheet quy hoạch)
- [ ] ĐNNK `index.vue:639` + `_id/index.vue:376`: `openErp(...)` → `$router.push('/finance/warehouse-imports/create?warehouse_import_request_id=')`;
      bỏ import `openErp` nếu không còn dùng; sửa docblock Controller ĐNNK :656-662
- [ ] Nút "Tạo phiếu nhập hàng" ở PNK → `/finance/product-imports/create?warehouse_import_id=` (HRM có sẵn)
- [ ] (Q11) Đổi link phía ERP sang HRM / chặn tạo-sửa PNK phía ERP — cần team ERP

## Phase 7 — Kiểm chứng + QA (2 công)

- [ ] Playwright MCP đi hết luồng: YCNH → ĐNNK → PNK (tạo → xếp → nhập kho → Gửi) → KT kho: Không duyệt / Tạo phiếu nhập hàng → duyệt → PNK "Đã hạch toán"
- [ ] Kiểm tồn sau Gửi trên màn tồn kho HRM/ERP; phiếu tạo ở HRM mở được ở ERP (show/edit/arrange)
- [ ] Phạm vi danh sách ↔ `canView` khớp trên nhóm nhân viên mẫu; đóng browser
- [ ] Trả lời Redmine #11693

---

### Checkpoint — 2026-10-15
Vừa hoàn thành: khảo sát ERP + HRM, viết spec (`docs/superpowers/specs/gop-db/2026-10-15-phieu-nhap-kho-design.md`), design, plan; thêm entry STATUS.
Đang làm dở: chưa code (chưa đụng hrm-api / hrm-client).
Bước tiếp theo: user chốt Q1–Q13 (spec mục 10) → bắt đầu Phase 1 (entity + scopedQuery + routes).
Blocked: chờ user chốt — Q1 phạm vi đợt 1, Q6 vận chuyển + bốc xếp, Q8 nơi lưu file đính kèm, Q12 tạo `PhysicalStockWriter` dùng chung.
