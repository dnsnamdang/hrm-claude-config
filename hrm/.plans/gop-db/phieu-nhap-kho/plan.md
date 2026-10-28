# Plan — Phiếu nhập kho (ERP `warehouse_imports` → HRM)

> @junfoke · nhánh `gop_db` (cả 2 repo — hiện đứng `develop`, checkout từ `gop_db`) · bắt đầu 2026-10-15 · Redmine #11693
> Design: `.plans/gop-db/phieu-nhap-kho/design.md`
> Spec: `docs/superpowers/specs/gop-db/2026-10-15-phieu-nhap-kho-design.md`

**0 bảng mới, 0 migration. 3 quyền mới guard `api` (Q7 chốt).** Nhánh: `feat/finance-warehouse-import` (cả 2 repo, tách từ `develop`).
Ước lượng tổng: **~26,5 công** (0,5 + 2,5 + 6 + 1,5 + 5,5 + 4 in/Excel/lịch sử/barcode + 4 xuất lại/nhập lại + 0,5 + 2).

---

## Phase 0 — Khảo sát (0,5 công) ✅

- [x] Đọc controller ERP 2.505 dòng, model 1.787 dòng, 12 blade, route group `warehouse_imports` (38 route)
- [x] Soi hết cửa vào menu ERP (all / for_approve / discrepancy / excShortage / forAccounting cũ)
- [x] Đo dữ liệu `gop_db` local: 8.887 phiếu, 13 loại có dữ liệu, phân bố status/step, 8 bảng tồn
- [x] Xác định chỗ HRM đang đọc/ghi `warehouse_imports` (ProductImportService, bill payment, chuyến xe, hàng đang về)
- [x] Xác nhận HRM chưa có writer tồn vật lý theo vị trí; chưa có popup vị trí / chuyến xe / tuyến đường
- [x] Viết spec + design + plan
- [x] **User chốt Q1–Q13** (2026-10-15 — xem design.md mục "Đã chốt": Q1 port hết, Q6 port, Q12 OK, còn lại theo đề xuất)

---

## Phase 1 — BE: Entity + API đọc (2,5 công)

- [x] Entity mới `Entities/WarehouseImport/`: `WarehouseImport` (`$table`, STATUSES + màu SRS, STEP, quan hệ), `TmpWarehouseImportLot`,
      `TmpWarehouseImportLotDetail`, `WarehouseImportLot` (ghi được), `WarehouseImportLotDetail`, `WarehouseImportExportArrangeDelivery`,
      `…Executor` — giữ `Entities/Contract/WarehouseImport*` chỉ đọc cho 5 service cũ (Q10)
- [x] `WarehouseImportService::scopedQuery()` port `searchByFilter type=all` (4 nhánh quyền + fallback của mình, ẩn nháp người khác,
      `company_id` null ⇒ `1 = 0`) + preset `for_approve` (status 2, công ty mình)
- [x] Bộ lọc 11 ô + khoảng ngày + tổ chức; sort; cột "Người đề nghị"/"Người yêu cầu" (loại 7, loại 8 nhập ghép) không N+1
- [x] `meta()` (loại, trạng thái, kho, NCC) · `show()` + cờ quyền `is_can_*` (edit / arrange / deny / cancel / create_product_import / view)
- [x] Controller + routes `finance/warehouse-imports` (route tĩnh trước `/{id}`), gate trong Controller (trait 2 guard)
- [x] 3 quyền "Xem phiếu nhập kho theo …" cuối `PermissionsTableSeeder`
- [x] Smoke: index/show/meta, đối chiếu số phiếu theo scope với ERP cho 3-4 nhân viên mẫu

## Phase 2 — BE: Ghi (6 công)

- [x] `PhysicalStockWriter::importLot()` (dùng chung, Q12 OK) — port `updateWarehouse()` 8 bảng, lock, `objectable_type` chuỗi class ERP,
      đọc `App\BaseModel` ERP để ghi đủ cột tự gán (`company_id`, `created_by`…)
- [x] Kiểm kho: port `Product::checkInventory` + `Position::checkInventory` (chặn hàng/vị trí đang kiểm kho)
- [x] `store()` — Request class port rule ERP + rule loại 7; tmp lots/details; bốc xếp + người nhận việc; chuyến xe; tabs;
      `generateCode()`; **duyệt ĐNNK** (ĐNNK → 1, YCNH → 4, thông báo) qua `WarehouseImportRequestService`
- [x] `saveArrange()` (lưu nhóm + người đi xếp) + `printArrangeData()` (không ghi)
- [x] `update()` Lưu / Gửi — lots xoá-ghi lại, file đính kèm (chờ Q8), chuyến xe/tuyến/km, bốc xếp; Gửi: loại 2 cập nhật đơn đặt hàng gốc
      (`root_order_request_*`), `PhysicalStockWriter`, `send()` (ĐNNK → 6, YCNH → 8, YC xuất nội bộ, thông báo KT kho); chuyến chờ duyệt ⇒ về 3
- [x] `deny()` (lý do bắt buộc) · `cancel()` (gọi hủy ĐNNK có sẵn)
- [ ] Soát `ProductImportService::markParentUsed` có đủ bước `product_transfer_requests → 10` cho loại 7 như ERP `approve()` chưa
- [x] **Đối chiếu song song**: 1 phiếu ERP ↔ 1 phiếu HRM cùng dữ liệu trên DB local → so từng dòng 8 bảng tồn + chứng từ cha, rollback/dọn

## Phase 3 — FE: Danh sách (1,5 công)

- [x] `pages/finance/warehouse-imports/index.vue` theo skill `list-page` + `erp-to-hrm-screen` checklist A–C: 14 cột, cấu hình cột,
      ghi nhớ bộ lọc, badge `V2BaseBadge`, cột Tiến trình, link mã ĐNNK / phiếu cha "Nhập lại cho phiếu …"
- [x] Menu hành động theo cờ BE: Xếp hàng / Nhập kho (Sửa) / Tạo phiếu nhập hàng / Hủy / In / Lịch sử (+ deep-link ERP Q4/Q5)

## Phase 4 — FE: Thêm / Xếp hàng / Nhập kho / Chi tiết (5,5 công)

- [x] `create.vue` — popup chọn ĐNNK (status 2, thủ kho), nhận `?warehouse_import_request_id=`, bảng dòng hàng + nhiều vị trí/dòng,
      tab Vận chuyển + Bốc xếp (Q6), `unsavedChangesMixin`, `form-validate`
- [x] Popup dùng chung mới: chọn vị trí kho (theo kho + hàng), chọn chuyến xe, chọn tuyến đường, chọn người nhận việc bốc xếp
- [x] `_id/arrange.vue` — nhóm phiếu xếp hàng (kéo-thả), chọn người đi xếp, Lưu, In nhóm
- [x] `_id/edit.vue` — Nhập kho: SL/vị trí thực, file (bắt buộc), Lưu / Gửi, xem trước bản in
- [x] `_id/index.vue` — chi tiết + actionbar (Không duyệt + modal lý do, Tạo phiếu nhập hàng, Sửa, Hủy, In, Quay lại) + lịch sử

## Phase 5 — In · Excel · Lịch sử (2,5 công)

- [x] In phiếu nhập kho mẫu ERP id 46 (`print-page`, letterhead theo `company_id` phiếu, path logo ghép `ERP_URL`)
- [x] In phiếu đi xếp hàng mẫu ERP id 30
- [x] Xuất Excel danh sách (`export-excel`, `ExportFieldsModal`), bộ lọc giống danh sách
- [x] Lịch sử: đăng ký `warehouse_imports` vào `CatalogHistoryService::TABLES` + nhãn action (create / update / send / deny / cancel)
- [x] In barcode 3 mẫu theo `barcode_template_type`, nhập NSX/HSD (F11, Q1 chốt port — +1,5 công)

## Phase 5b — Xuất lại / Nhập lại (F12/F13, Q1 chốt port — ~4 công, ước lượng sơ bộ)

- [x] Khảo sát kỹ ERP `WarehouseReExportsController` (màn `warehouse_reexports`, 12 phiếu) + `reImport`/`reImportStore` — chưa soi chi tiết ở Phase 0
- [x] Xuất lại: PNK "Không duyệt" (4) → phiếu xuất lại → PNK 5; **trừ tồn vật lý** ⇒ `PhysicalStockWriter` cần chiều xuất (thiết kế sẵn từ Phase 2)
- [x] Nhập lại: PNK "Đã xuất lại" (5) → PNK mới (cha → 6) + ghi tồn như Gửi
- [x] FE: nút Tạo phiếu xuất lại / nhập lại ở danh sách + chi tiết PNK; màn phiếu xuất lại (tối thiểu tạo + xem) — menu riêng hay không thì hỏi lại khi khảo sát xong

## Phase 6 — Nối luồng + menu (0,5 công)

- [x] `finance.js:153` đổi `erpPath` → `link: '/finance/warehouse-imports'` (giữ thứ tự theo sheet quy hoạch)
- [x] ĐNNK `index.vue:639` + `_id/index.vue:376`: `openErp(...)` → `$router.push('/finance/warehouse-imports/create?warehouse_import_request_id=')`;
      bỏ import `openErp` nếu không còn dùng; sửa docblock Controller ĐNNK :656-662
- [x] Nút "Tạo phiếu nhập hàng" ở PNK → `/finance/product-imports/create?warehouse_import_id=` (HRM có sẵn)
- [ ] (Q11) Đổi link phía ERP sang HRM / chặn tạo-sửa PNK phía ERP — cần team ERP

## Phase 7 — Kiểm chứng + QA (2 công)

- [x] Playwright MCP đi hết luồng: YCNH → ĐNNK → PNK (tạo → xếp → nhập kho → Gửi) → KT kho: Không duyệt / Tạo phiếu nhập hàng → duyệt → PNK "Đã hạch toán"
- [x] Kiểm tồn sau Gửi trên màn tồn kho HRM/ERP; phiếu tạo ở HRM mở được ở ERP (show/edit/arrange)
- [x] Phạm vi danh sách ↔ `canView` khớp trên nhóm nhân viên mẫu; đóng browser
- [ ] Trả lời Redmine #11693

---

### Checkpoint — 2026-10-15 (cuối ngày)
Vừa hoàn thành: Phase 1–4, 5 (in 46/30, Excel, lịch sử, barcode), 6 (menu + nút ĐNNK). Nhánh `feat/finance-warehouse-import`, CHƯA commit.
Kiểm chứng: đối chiếu ghi tồn HRM↔ERP 6 phiếu (2-10 lô, 2 công ty, 4 kho) 0 lệch; luồng đủ tạo→xếp→nhập kho→Gửi→Không duyệt / Hủy
chạy thật trong transaction rollback; UI chụp ảnh danh sách / chi tiết / tạo / xếp hàng / nhập kho / barcode.
Đang làm dở: Phase 5b Xuất lại / Nhập lại (2 nút đang deep-link ERP).
Bước tiếp theo: khảo sát ERP WarehouseReExportsController + reImport/reImportStore → port; Phase 7 QA.
Blocked: không.

### Checkpoint — 2026-10-15 (Phase 5b xong)
Vừa hoàn thành: Xuất lại (`WarehouseReExportService`, `PhysicalStockWriter::exportShortage/exportLot`) + Nhập lại
(`WarehouseImportWriteService::reImport`, thân `update()` tách thành `applyUpdate()` dùng chung). FE: `_id/re-export.vue`,
`_id/re-import.vue` (form Nhập kho chế độ `re-import`), `warehouse-reexports/_id`; row-actions bỏ hết deep-link ERP; chi tiết PNK có link phiếu xuất lại.
Không làm màn danh sách phiếu xuất lại (cả hệ thống 12 phiếu) — xem qua link ở PNK.
Khác ERP: phiếu nhập lại KHÔNG trừ "hàng đang về" lần 2 khi Gửi; xem phiếu xuất lại nới cho ai xem được PNK gốc.
Kiểm chứng: luồng 4→Xuất lại(5, tồn về 0)→Nhập lại Gửi(6, tồn khớp ban đầu) rollback; test cũ Nhập kho không hồi quy; UI chụp 3 màn.
Đang làm dở: không.
Bước tiếp theo: Phase 7 QA.
Blocked: không.

### Checkpoint — 2026-10-16 (Phase 7 QA)
Vừa hoàn thành: QA BE rollback — PNK tạo ở HRM so cột với 30 phiếu ERP cùng loại: lô/chi tiết/lô tạm đủ cột, phiếu chỉ thiếu
approver/approved/handled_time (do Phiếu nhập hàng ghi sau — HRM `ProductImport::updateWarehouse` đã ghi status 1 + handled_time);
Kế toán kho thấy PNK HRM trong nguồn lập Phiếu nhập hàng (8 lô). Phạm vi: 9 nhân viên mẫu × 400 phiếu, danh sách ⊂ canView,
chênh duy nhất 12 phiếu "đang đi xếp hàng" (ERP cho ai cũng xem — giữ). Danh sách chụp lại sau khi đổi row-actions OK.
Đang làm dở: không.
Bước tiếp theo: user commit + deploy dev → trả lời Redmine #11693 (bản nháp đưa user duyệt); Q11 phía ERP cần team ERP.
Blocked: không.

### Checkpoint — 2026-10-16 (chạy thật trên giao diện, user cho phép ghi DB local)
Vừa hoàn thành: bấm thật bằng DNS Admin (13) từ PDNNK-08533: tạo PNK-08924 → xếp hàng 2 phiếu (kéo thả) → in phiếu xếp →
Lưu → Gửi (tồn +32/+1 đủ 4 tầng, ĐNNK 6, YCNH 8) → in phiếu → Không duyệt → Xuất lại PXL-00014 (tồn về đúng số cũ) →
Nhập lại PNK-08925 (tồn cộng lại, cũ → 6, PXL → 1). Form Phiếu nhập hàng nhận PNK-08925 (không bấm Duyệt — ghi sổ kế toán).
ERP local mở PNK-08925 hiển thị đúng. Riêng upload S3 bị chặn (trả URL giả) — không đẩy file lên S3 thật.
Sửa trong đợt: lỗi BE không tự xoá khi đã sửa ô (người giao, vị trí/SL, file, người đi xếp); bản in mẫu 46 điền thêm
NGUOI_YEU_CAU + THU_KHO (ERP cũng để trống); nút Tạo phiếu xuất lại/nhập lại thành nút chính.
Dữ liệu test để lại trên DB local: PNK-08924 (Đã nhập lại), PNK-08925 (Chờ duyệt), PXL-00014, PDNNK-08533 (Đã nhập kho).
Đang làm dở: không.
Bước tiếp theo: user commit + deploy → trả lời Redmine #11693.
Blocked: không.
