# Plan — Nút "Tạo mới" ĐNNK + picker chọn phiếu YCNH nguồn (parity ERP)

Nguồn yêu cầu (user, 2026-10-07): *"đề nghị nhập kho Chưa có nút tạo mới ở màn danh sách, bên erp
có '…' cạnh nút xuất excel ấy"*. Màn **Đề nghị NHẬP kho (ĐNNK)** =
`pages/finance/warehouse-import-requests`.

## Bối cảnh / đối chiếu ERP

- ERP `warehouse/warehouse_import_requests` **CÓ** nút tạo trực tiếp (`create_link` ở DATATABLE,
  cạnh "Xuất Excel"). Màn Tạo mở `searchProductImportRequest` (BaseSearchModal) để **chọn 1 phiếu
  YCNH nguồn** (product_import_request) → chọn kho nhập → Lưu nháp / Gửi thủ kho.
  Filter ERP của picker: `type='accounting'`, `status=2` (đã duyệt), `is_import_direct=0`.
- HRM hiện tại: `create.vue` **BẮT BUỘC** có `?request_id` ở query, thiếu thì toast lỗi + redirect
  về `/finance/product-import-requests`. Màn list ĐNNK CHƯA có nút "Tạo mới" (đang có comment nói
  "ĐNNK lập từ YCNH nguồn, không tạo trực tiếp" — **sai**, phải gỡ).

## Quyết định đã chốt (user xác nhận qua AskUserQuestion)

1. Màn đích = **Đề nghị NHẬP kho (ĐNNK)** = `warehouse-import-requests` (không phải ĐNXK).
2. Luồng tạo = **giống ERP**: picker chọn phiếu YCNH nguồn ngay trong màn Tạo.

## Task

### FE — `warehouse-import-requests/index.vue` (toolbar)
- [x] Gỡ comment "Màn này KHÔNG có 'Tạo mới'…" (dòng ~50-51).
- [x] Thêm nút **Tạo mới** `V2BaseButton primary size="sm"` icon `ri-add-line`, **đứng ĐẦU** toolbar
      (trước "Xuất Excel") → `goCreate()` → `$router.push('/finance/warehouse-import-requests/create')`
      (không query). (button-convention §5 toolbar: primary trước secondary.)

### FE — `warehouse-import-requests/create.vue` (vào màn không cần ?request_id + picker)
- [x] `mounted()`: thiếu `?request_id` thì **KHÔNG redirect** nữa → `loading=false` + mở picker
      "Chọn phiếu YCNH nguồn" (và set `cameFromYcnh=false`). Có `?request_id` (vào từ YCNH) →
      `cameFromYcnh=true` + giữ nguyên `fetchData()` như cũ.
- [x] Dựng modal "Chọn phiếu YCNH nguồn" = `components/SourceImportRequestSearchModal.vue`.
      **QUYẾT ĐỊNH (2026-10-07): KHÔNG dùng `V2BaseModal` mà copy khuôn `b-modal` của
      `product-import-requests/components/ExportRequestSearchModal.vue`.** Lý do: đây là picker
      chọn phiếu-nguồn của phân hệ Finance — đã có 6 anh em cùng họ (ExportRequestSearchModal…)
      đều dùng `b-modal` + bảng `*-table` + phân trang server. Làm 1 bản `V2BaseModal` lạc loài sẽ
      tạo đúng cái "nhiều kiểu khác nhau cho cùng 1 thứ" mà CLAUDE.md cấm. Giữ §4b (click dòng =
      chọn ngay). Cột: STT / Mã phiếu / Loại / Người tạo / Ngày tạo. Không có select trong modal
      (chỉ 1 ô lọc Mã phiếu) nên không cần `V2BaseSelectInModal`.
- [x] Endpoint list YCNH đã chốt (Explore agent): `GET finance/product-import-requests` params
      `status=2` (CHO_DUYET/đã duyệt), `is_import_direct=0`, `keyword` (LIKE mã phiếu), `page`,
      `per_page`. Envelope `{data, total, lastPage, currentPage, perPage}`. Trùng tập điều kiện
      `assertCanCreate()` của BE (`warehouse-import-data`).
- [x] **FIX hình dạng response (2026-10-07):** popup lúc đầu rỗng dù API 200. Nguyên nhân: picker
      copy khuôn `ExportRequestSearchModal` nên đọc `response.data.data`, NHƯNG `apiGetMethod` trả
      về **THẲNG body** (không phải axios response), và route `index` của `product-import-requests`
      là Resource collection + `->additional()` → **dòng nằm ở `body.data`, phân trang ở TẦNG GỐC**
      (`body.total/lastPage/currentPage/perPage`). Khác `export-requests` (bọc `responseJson` nên
      mới là `body.data.data`). Sửa `loadData()`: đọc `safe.data` + phân trang tầng gốc. Verify:
      `status=2&is_import_direct=0` → đúng 15 YCNH.
- [x] Chọn phiếu → `onChooseSource(item)` set `this.requestId=item.id` + reset `form.warehouse_id` +
      gọi `fetchData()` (modal tự `hide()`).
- [x] Nút ghi dữ liệu (`submit(status)` — Lưu nháp status 3 / Gửi thủ kho status 2): đã thêm
      `$safeLoadingStart()` sau `submitting=true` + `$safeLoadingFinish()` trong `finally`
      (button-convention §6b). (Nút đã có `:interactable="!submitting"` sẵn.)
- [x] Giữ `unsavedChangesMixin` + `markFormSaved()` sau khi lưu; `goBack()` về list đúng nguồn
      (`cameFromYcnh` → `/finance/product-import-requests`, ngược lại → `/finance/warehouse-import-requests`).

### Verify
- [x] Playwright 127.0.0.1:3000 (2026-10-07):
      - (1) ✅ list ĐNNK có nút **Tạo mới** (primary) đứng trước **Xuất Excel** — đúng thứ tự toolbar.
      - (2) ✅ bấm Tạo mới → vào `/create`, picker "Chọn phiếu yêu cầu nhập hàng" tự mở.
      - (3) ✅ sau FIX response-shape: picker hiện **15 YCNH** (PYCNH-12226/12216/12209…, phân trang
        1/2). Chọn PYCNH-12216 → form nạp đủ: Thông tin chung (Mã YCNH, Loại, NCC ETEK GREEN,
        Ngày/Người yêu cầu), **Kho nhập = Liên Ninh**, **Danh sách hàng hoá** 1 dòng
        (ETGN-EG-IE010010002, SL yêu cầu 8, SL nhập kho 8), nút Lưu nháp/Gửi thủ kho/Quay lại.
      - Console chỉ còn lỗi benign (ERR_CONNECTION_REFUSED của socket.io :8891 + warning webpack),
        KHÔNG có 500/404/403 hay lỗi `warehouse-import-data`/`product-import-requests`.
- [ ] (4) Lưu nháp → về list, thấy phiếu mới: **CHƯA chạy** — bước này GHI bản ghi thật vào DB gộp
      prod (ràng buộc chỉ-đọc). Chờ user quyết có chạy write-test hay không.
- [x] KHÔNG commit/push (chờ user).

## Checkpoint
### Checkpoint — bắt đầu (2026-10-07)
Vừa hoàn thành: chốt 2 quyết định với user; đọc create.vue + index.vue; tạo plan.
Đang làm dở: chờ Explore agent trả endpoint list YCNH + filter eligibility để dựng picker.
Bước tiếp theo: điền endpoint vào plan → thêm nút Tạo mới (index.vue) → dựng picker (create.vue) →
  Playwright verify.
Blocked: chờ kết quả Explore agent (endpoint + filter YCNH).

### Checkpoint — code xong + verify đọc (2026-10-07)
Vừa hoàn thành: toàn bộ code (nút Tạo mới index.vue; picker SourceImportRequestSearchModal.vue;
  create.vue mounted/onChooseSource/safeLoading/goBack). FIX hình dạng response của picker
  (`apiGetMethod` trả thẳng body; dòng ở `body.data`, phân trang tầng gốc) → picker hiện đủ 15 YCNH.
  Playwright verify xong bước 1-3 (nút đúng vị trí → picker mở → chọn YCNH nạp đủ kho + hàng), console
  sạch (chỉ lỗi socket.io benign).
Đang làm dở: không.
Bước tiếp theo: chờ user quyết (a) có chạy write-test "Lưu nháp" (ghi bản ghi thật vào DB gộp prod)
  không; (b) commit/push.
Blocked: bước verify (4) + commit/push đều chờ user — không tự ghi prod, không tự commit.
