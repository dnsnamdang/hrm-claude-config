# Plan — Đồng bộ popup HĐ chi phí theo popup HĐ hãng

Nguồn: user — "popup chọn hợp đồng chi phí đang khác popup chọn hợp đồng ở loại xuất bán...";
chốt 2026-10-14: CHƯA sửa logic lấy HĐ, chỉ **đồng bộ khuôn tìm kiếm + cột**.

## Tasks

### BE (hrm-api)
- [x] Task 1: `ProductExportRequestPickerService::costContracts()` — thêm filter `code` (c.code like),
      `customer` (nameExpr like) tách riêng (giữ `search` combined back-compat); thêm `sort_by`/`sort_desc`
      whitelist (`code`, `customer_name`), mặc định id desc; select thêm `customer_address`
      (`c.customer_address` các bảng có cột; `opening_contracts` → `cu.address_text`). KHÔNG đụng `costContractScope()`.
- [x] Task 2: `ProductExportRequestController::costContracts()` — validate thêm `code`/`customer`/`sort_by`/`sort_desc`,
      truyền qua `$request->only(...)`.
- [x] Task 3: `php -l` 2 file BE — không lỗi cú pháp.

### FE (hrm-client)
- [x] Task 4: Dựng lại `ContractCostModal.vue` theo khuôn `FirmContractSearchModal.vue`:
      V2BaseDataTable + hàng lọc (Loại HĐ giữ + Số HĐ + Khách hàng + Tìm kiếm + Làm mới) + cột
      STT/Mã hợp đồng/Khách hàng/Địa chỉ + server-sort + phân trang nhúng + click-dòng-chọn.
      Giữ prop `sources`/`customerId`, method `show(currentKey)`, emit `select({id,code,key})`.
- [x] Task 5: Kiểm FE thô: `grep` không còn `<table`/`<input` thô ngoài V2Base trong file (được dùng
      V2BaseDataTable nên không cần table tay).

### Verify
- [x] Task 6: Playwright MCP — mở `http://127.0.0.1:3000/finance/product-export-requests/create`,
      chọn loại "Xuất khác", mở popup HĐ chi phí: thấy đủ Loại HĐ + Số HĐ + Khách hàng + Tìm kiếm +
      Làm mới + cột Địa chỉ; thử tìm + đổi loại; đối chiếu khuôn với popup HĐ hãng (loại Xuất bán hàng). **ĐẠT** (chi tiết Checkpoint).

### FE bổ sung (user phản ánh 14/10 — ô trigger)
- [x] Task 7: Ô "Hợp đồng chi phí" (trigger mở popup) ở `ProductExportRequestForm.vue` đang là
      `V2BaseInput disabled` bọc `.cost-pick` tự chế → nền xám (trông bị disable) + lệch so với select
      cạnh bên. Ô "Hợp đồng hãng" (loại Xuất bán) dùng `SourcePicker` (V2BaseInput **readonly** +
      `.picker-input`: nền trắng, con trỏ tay, `:disabled="!canChangeSource"`). → Cho ô HĐ chi phí
      DÙNG LẠI `SourcePicker` để render giống hệt; thêm prop `dataTest` (mặc định `ycxh-source-picker`)
      vào SourcePicker để giữ hook `ycxh-cost-contract`; giữ nút xóa chọn (clear) bên cạnh.
      Bỏ `pointer-events:none` + `cursor` ở `.cost-pick__input` (SourcePicker tự xử lý, pointer-events:none
      sẽ chặn click mở popup). File chạm thêm: `SourcePicker.vue` (prop `dataTest`) + `ProductExportRequestForm.vue`.
- [x] Task 8: Verify Playwright — ô HĐ chi phí nền TRẮNG + canh thẳng hàng với "Xuất khác"/"Kho xuất"/"Vận chuyển"
      (hết xám disabled + hết lệch); click mở popup OK; chọn HĐ HRM → điền mã `HĐ_TPE_HN_KDTM_26_0001_HTHT-TEST`
      + đóng popup; nút × xóa chọn → về placeholder. `data-test="ycxh-cost-contract"` vẫn trỏ đúng.
      Ảnh: `cost-field-sourcepicker.png` (rỗng, trắng, thẳng hàng) + `cost-field-filled.png` (đã điền).

### FE bổ sung (user phản ánh 14/10 lần 2 — "vẫn lệch dòng")
- [x] Task 9: Dù ô HĐ chi phí đã dùng SourcePicker (nền trắng), ô vẫn **lệch dòng** (nhích lên 4px) so với
      các select bắt buộc cùng hàng. Root cause (đo bằng Playwright): `V2BaseLabel` có dấu `*` cao **18px**,
      nhãn KHÔNG bắt buộc ("Hợp đồng chi phí") chỉ cao **14px** → control bị đẩy lên 4px (box_top 12 vs 16).
      FIX: thêm rule scoped `.fld ::v-deep .v2-label { min-height: 18px; }` trong `ProductExportRequestForm.vue`
      — giữ chiều cao nhãn tối thiểu bằng nhãn có `*`, mọi ô cùng hàng canh thẳng. KHÔNG đụng `V2BaseLabel` dùng chung.
- [x] Task 10: Verify Playwright — đo lại 4 ô (Loại yêu cầu / Hợp đồng chi phí / Kho xuất / Vận chuyển):
      label_height = 18 đồng loạt, box_top = 152 đồng loạt (trước fix: HĐ chi phí box_top 12 vs 16). Ảnh
      `cost-field-aligned.png` (4 ô thẳng hàng). Click ô HĐ chi phí → popup "Chọn hợp đồng chi phí" vẫn mở OK.

## Checkpoint — 2026-10-14 (cập nhật)
Vừa hoàn thành: Fix "vẫn lệch dòng" ô HĐ chi phí — nhãn không bắt buộc thấp hơn nhãn có `*` 4px.
`.fld ::v-deep .v2-label { min-height: 18px }` → 4 ô cùng hàng canh thẳng (box_top 152 đồng loạt, verify Playwright).
File chạm tổng: 5 (2 BE + 3 FE: ContractCostModal.vue, SourcePicker.vue, ProductExportRequestForm.vue). CHƯA commit.
Bước tiếp theo: chờ user yêu cầu commit/push.

## Checkpoint — 2026-10-14
Vừa hoàn thành: Verify Playwright toàn bộ popup HĐ chi phí đồng bộ khuôn HĐ hãng.
Kết quả verify (DB local `erp_hrm_check`, công ty 1):
- Popup render đúng khuôn: hàng lọc [Loại hợp đồng + Số hợp đồng + Khách hàng + Tìm kiếm + Làm mới];
  bảng V2BaseDataTable cột STT / Mã hợp đồng / Khách hàng / Địa chỉ; phân trang nhúng.
- Loại "Hợp đồng" (type 1): "Không có hợp đồng." (đúng — scope cty 1 có 0 dòng type 1).
- Loại "Hợp đồng đầu kỳ": 1586 dòng; lọc Số HĐ "VF-IP" → 24 dòng (param `code` chạy end-to-end).
- Loại "Hợp đồng HRM": 2 dòng, cột Địa chỉ CÓ dữ liệu (address_text customers).
- Sort cột Mã hợp đồng: asc (`sort_by=code&sort_desc=0`) + desc (`sort_desc=1`) đều 200 OK.
- Chọn dòng: click cả dòng → điền mã HĐ vào ô "Hợp đồng chi phí" + đóng popup (req #51→chọn HĐ HRM).
- Nút xóa chọn (clear) ô field hoạt động; nút "Làm mới" reset lọc.
- Console/network: mọi `cost-contracts` 200 OK; chỉ 1 lỗi `menu-settings 400` pre-existing, KHÔNG từ component mới.
Bước tiếp theo: chờ user yêu cầu commit/push (CHƯA commit). File chạm: 3 (2 BE + 1 FE).

## Ghi chú
- DB local `erp_hrm_check`; API :8000, client :3000 chạy sẵn.
- KHÔNG commit/push khi chưa được yêu cầu.
