# Thiết kế — Phiếu xuất bán hàng mượn (PXBHM): Xuất Excel, Lịch sử, Bộ lọc, UI danh sách & Xem chi tiết

> Tóm tắt tổng thể. Spec đầy đủ (API contract, display fields, business rule, edge case):
> `docs/superpowers/specs/gop-db/2026-10-10-borrow-sells-export-history-design.md`.
> Phụ trách: @namdangit · Nhánh: `gop_db` (cả hrm-api + hrm-client).

## Mục tiêu

Hoàn thiện màn `finance/borrow-sells` (Phiếu xuất bán hàng mượn — PXBHM) cho ngang với màn mẫu ERP
và màn `finance/product-exports`: bổ sung Xuất Excel danh sách, Lịch sử (2 nơi), đủ bộ lọc, chỉnh
UI lưới, và dựng lại màn Xem chi tiết đồng bộ với ERP.

`borrow_sells` là bảng ERP dùng chung (DB gộp `erp_hrm_check`). Controller HRM **chỉ có luồng tạo**
(index / store / show / printData) — không update / status / cancel.

## Phạm vi (5 phase, đã xong hết)

| Phase | Nội dung | Trạng thái |
|---|---|---|
| **1** | Xuất Excel danh sách (8 cột, chia trang, dựng file ở FE) + Lịch sử (popup danh sách + mục màn chi tiết) | ✅ api `c8cb68ff0` |
| **2 (filter)** | 10 bộ lọc màn danh sách, mirror `BorrowSellRequest::searchByFilter` | ✅ api `56b0d833c` |
| **B (list UI)** | Ẩn Tổng tiền; thêm Ngày/Người cập nhật + Phiếu YC + Người YC; Mã HĐ thành link; ẩn nút Xem chi tiết ở lưới | ✅ |
| **2 (type_name)** | Sửa nhãn "Loại phiếu" suy từ `contractable_type` (cột `type` ERP luôn = 1, là loại HÀNG) | ✅ api `1936a0b25` |
| **C (chi tiết)** | Màn Xem chi tiết đồng bộ ERP: +Người/Phòng yêu cầu, tách tab Hàng hoá/Nhóm, bảng Thông tin thanh toán HĐ | ✅ api `9177aa457` · client `12d2c1d44` |

## Các quyết định đã chốt (với user)

1. **Lịch sử**: vẫn làm đủ 2 nơi dù phiếu chỉ có 1 dòng log "Tạo mới" (không có luồng đổi trạng thái).
   Track header (loại HĐ, số HĐ, khách, ghi chú, VAT%, ship, tổng tiền) + bảng hàng; KHÔNG track `status`.
   Không có quyền xem riêng (ai vào màn thì xem được).
2. **Loại hợp đồng** lấy từ morph `contractable_type`, KHÔNG từ cột `type` (= loại hàng, luôn = 1):
   `FirmContract`→"HĐ hãng", `WrServiceContract`→"HĐ dịch vụ", `HrmContract`→"HĐ HRM". Mirror ở cả
   list resource lẫn detail resource qua helper `contractTypeName()`.
3. **Mã HĐ link** (màn danh sách): HRM→`/assign/contracts/{id}`, WR_SERVICE→`/customer-care/wr-service-contracts/{id}`,
   FIRM→`null` (HRM không có màn chi tiết firm_contracts → render text thường).
4. **Màn chi tiết — sync "Chỉ bổ sung field còn thiếu"**: GIỮ layout kv-grid hiện tại, chỉ thêm
   Người yêu cầu + Phòng yêu cầu (mã PYCXH đã có sẵn). KHÔNG dựng lại kiểu ERP.
5. **Bảng "Thông tin thanh toán hợp đồng" + tab Nhóm: CHỈ cho HĐ hãng** (mirror ERP):
   `need_contract_info = contract && type != 3 && !has_rebate_price`, với
   `has_rebate_price = (contractable_type == WrServiceContract)`. → ẩn với HĐ dịch vụ và HĐ type 3.
6. **KHÔNG đụng**: luồng Phase 1 (phiếu YÊU CẦU), `BorrowSellListResource` (ngoài field đã khai),
   `BorrowSellPostingService` / `enrichAccounting` / `EXPORT_COLUMNS` dùng chung, `BorrowSellPrintResource`.

## Bẫy gộp DB đã xử lý

- Quyền "hàng mượn" của user cấp qua vai trò ERP **guard `web`**; store FE chỉ có guard `api` (584 quyền,
  không có quyền "mượn") → cờ scope fail-closed ra rỗng dù BE cho ALL_COMPANY. Fix: FE đọc cờ phạm vi
  (`canViewAllCompany/Company/Department`) từ **meta BE** trả về trong `loadData()`, computed `permissions`
  map sang cụm Công ty–Phòng ban. (Phase 2-filter, mục B-fix.)
- `BorrowSell` extends `Model` thuần (bảng ERP) → `employee_update()` phải khai tay theo `updated_by`.

## Kiểm chứng

Playwright MCP tại `http://127.0.0.1:3000` (SPA nav, KHÔNG hard-navigate — hard-navigate rơi trang 404
tĩnh do SSR không có token, không phải bug). File Excel đọc lại bằng PhpSpreadsheet: cột Tổng tiền là
ô SỐ `#,##0`. 2 ca chi tiết: FIRM 4312 (2 tab + payment HĐ_TPE_HN_KDXM_26_0398_03) / WR_SERVICE 4228
(1 tab, không payment).
