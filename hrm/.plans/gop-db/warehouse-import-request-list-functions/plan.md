# Plan — Chức năng màn "Danh sách đề nghị nhập kho" (Lỗi #11400)

Nhánh `gop_db` · @namdangit · Redmine Lỗi #11400 · làm song sinh với màn ĐNXK đã xong

## Phase 1 — 5 yêu cầu bảng danh sách + đồng bộ chi tiết

### BE — `hrm-api`
- [x] `Modules/Finance/Transformers/WarehouseImportRequestResource.php`: thêm `updater_name`
      (employee_update.info.fullname), `requester_name`
      (productImportRequest.employee_create.info.fullname), `updated_at` (Carbon d/m/Y H:i)
- [x] `Modules/Finance/Http/Controllers/V1/WarehouseImportRequestController@index`:
      + sortMap type_name→type; product_import_request_code (join product_import_requests);
        supplier_name (join customers theo supplier_id)
      + eager-load `employee_update.info`, `productImportRequest.employee_create.info`
- [x] `Modules/Finance/Services/WarehouseImportRequestService.php`: `use LogsCatalogHistory`
      + catalogTable/catalogColumns/catalogDisplay/detailRows/numText/statusText/logStatusChanged;
      log ở createFromImportRequest (create), updateDraft (update+status), deny (status+note), cancel (status)
- [x] `app/Services/CatalogHistoryService.php` TABLES: đăng ký `warehouse_import_requests`
      (type→Loại nhập, warehouse_id→Kho nhập, note→Ghi chú, details_rows→Bảng chi tiết hàng hóa)

### FE — `hrm-client`
- [x] `pages/finance/warehouse-import-requests/index.vue`:
      + nhãn creator_name "Người lập"→"Người tạo"
      + 4 cột mới: updated_at (center), updater_name, requester_name, approver_name + cell template
      + sortable:true cho type_name, product_import_request_code, supplier_name
      + action `history` (icon ri-history-line, luôn hiện) + goHistory + <CatalogHistoryModal>
      + ô trống `'—'`→`''`
- [x] `pages/finance/warehouse-import-requests/_id/index.vue`: thêm <SystemInfoSection>

### Verify
- [x] Playwright: 15 cột đúng thứ tự + nhãn "Người tạo" + sort 3 cột (Loại/Mã YCNH/Nhà cung cấp);
      getRowActions của page component có "Xem lịch sử" (icon ri-history-line, luôn hiện)
- [x] BE pipeline (tinker): TABLES đăng ký `warehouse_import_requests`; getLogs/filterOptions chạy OK
      (3 nhóm hành động + 783 performers); detailRows/catalogSnapshot/catalogDisplay ra giá trị hiển thị
      (type→"Nhập hàng khác", warehouse→"Liên Ninh"); round-trip logCatalogCreate→getLogs("Tạo mới")→xoá log sạch
- [~] Xem trực tiếp detail SystemInfoSection trên UI: BỊ CHẶN — user test (Trần Văn Đức) không có
      phạm vi dữ liệu ĐNNK nên list rỗng + detail redirect về list; route `finance-warehouse-import-requests-id`
      match + compile sạch; SystemInfoSection copy đúng pattern màn ĐNXK đã nghiệm thu
- [ ] Commit/push — **CHỜ user duyệt**

### Checkpoint — 2026-09-19
Vừa hoàn thành: code trọn 6 file (4 BE + 2 FE) + verify Playwright header/row-menu + verify BE pipeline (tinker, có cleanup).
Đang làm dở: không.
Bước tiếp theo: chờ user duyệt để commit/push (KHÔNG tự commit).
Blocked: xem UI detail bị chặn do phạm vi quyền của user test — đã verify bằng BE pipeline + đối chiếu pattern ĐNXK.
