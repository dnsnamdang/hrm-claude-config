# Kế hoạch — Port màn "Phiếu yêu cầu điều chuyển hàng giữ"

Tóm tắt: [design.md](design.md) · Spec chi tiết:
[docs/superpowers/specs/gop-db/2026-08-24-finance-prepick-transfer-request-design.md](../../../docs/superpowers/specs/gop-db/2026-08-24-finance-prepick-transfer-request-design.md)
Nhánh: `feat/finance-prepick-transfer-request` (cả 2 repo, tách từ `origin/gop_db`).
Người làm: @junfoke. Thứ tự do user chốt: làm **sau** màn Yêu cầu gia hạn hàng giữ (xong 24/08/2026).

## Phase 0 — Khảo sát + chuẩn bị dữ liệu ✅ (2026-08-24)

- [x] Đọc nguồn ERP: controller, model cha/con, 6 blade, Excel export, 13 route → ghi `design.md`
- [x] Liệt kê 13 lỗi ERP sẽ vá (bảng đối chiếu ở spec mục 5)
- [x] User kéo bảng `prepick_transfer2` từ dev về local: **1.295 phiếu** (1.244 Đã duyệt / 50 Không
      duyệt / 1 Chờ TP duyệt), `prepick_transfer2_details` 3.942 dòng
- [x] Tách nhánh mới ở cả 2 repo (api `8ecfb3287`, client `5b5b56d45`)
- [x] Sao lưu 4 bảng `bak_*_20260824`: prepick_details 53.832 · prepick_logs 110.744 ·
      prepick_transfer2 1.295 · prepick_transfer2_details 3.942
- [x] Kiểm dữ liệu: chỉ **79/1.295** phiếu có `to_customer_id` tồn tại trong `customers` — lỗi dữ
      liệu đã biết của DB gộp, KHÔNG phải lỗi màn

## Phase 1 — Entity + migration bảng lịch sử ✅ (2026-08-24)

- [x] `Entities/PrepickTransfer/PrepickTransferRequest.php` — 5 trạng thái kèm mã màu chuẩn,
      `WRITABLE_STATUSES`, `SORTABLE_COLUMNS`, `searchByFilter` + `applyAllScope` /
      `applyViewScope` / `orWhereApprovable` / `applyFilters` / `applySort`, các cờ `can*`
- [x] Vá lỗi #1 (`canView()` luôn true) + lỗi phạm vi (`where('company_id')` ở cuối `searchByFilter`
      của ERP làm quyền "theo tổng công ty" thành vô nghĩa)
- [x] `PrepickTransferRequestDetail.php` (`prepick_detail()`, `baseQty()`)
- [x] `PrepickTransferRequestHistory.php` — 7 action, có `delete`, KHÔNG có `send_approve`
- [x] Migration `2026_08_24_000001_create_prepick_transfer_request_history_table` + đã migrate

## Phase 2 — Service ✅ (2026-08-24)

- [x] `PrepickStockService::moveToOwner()` — **hàm dùng chung MỚI**, ghi tồn khi KT duyệt
      (vá lỗi #6 `company_id`, #7 `objectable_type`, thêm `lockForUpdate` + kiểm đủ tồn)
- [x] `PrepickStockService::holdingLots()` — **hàm dùng chung MỚI**, popup chọn lô
- [x] `PrepickTransferRequestHistoryService` (theo khuôn màn gia hạn; khoá ghép đổi sang
      `from_prepick_detail_id`, thêm `logDelete()`, bỏ `send_approve`)
- [x] `PrepickTransferRequestService`: `searchByFilter` · `meta` · `findForShow` · `detailData` +
      `approvalRows` (vá #2) · `lotCustomers` · `store`/`update` (vá #4, #5) · `normalizeLines` +
      `buildLine` + `productSnapshots` + `syncProducts` · `approve` 3 cấp · `applyApproverEdits` ·
      `applyTransferToStock` · `reject` · `destroy` (vá #9) · `needBoardApprove` + helper hợp đồng
      (vá #10, #11)
- [x] Test tinker trên phiếu thật `ĐCHG-01307`: `detailData` trả đủ 3 dòng duyệt + 3 dòng hàng

## Phase 3 — Controller + FormRequest + Resource + route ✅ (2026-08-24)

- [x] `PrepickTransferRequestStoreRequest` (không có `status` vì màn không có nháp) +
      `PrepickTransferRequestRejectRequest`
- [x] `PrepickTransferRequestListResource` — trả `status_color`, 3 cờ `is_can_*`, 2 cột cập nhật
- [x] `PrepickTransferRequestController` — 12 action (kể cả `products`, `lots`, `inStock`,
      `uploadFiles`), guard 423 ở `update`/`destroy`
- [x] 12 route trong `Modules/Finance/Routes/api.php` (route tĩnh khai TRƯỚC `/{id}`)
- [x] Gọi thật `GET /prepick-transfer-requests`: **1.245/1.295** phiếu (đúng luật ẩn 50 phiếu
      "Không duyệt" của người khác), badge `#16A34A`, `GET /{id}` trả đủ 3 cấp duyệt

### Checkpoint — 2026-08-24
Vừa hoàn thành: Phase 0-3b — BE đọc + GHI đã chạy thật, DB đã hoàn nguyên (0 chênh lệch so với
4 bảng `bak_*_20260824`).
Đang làm dở: bù tài liệu — user nhắc "tài liệu chưa xử lý xong đã code à?". Đã viết spec chi tiết
+ plan đầy đủ task; từ Phase 3b trở đi bám plan này.
Bước tiếp theo: Phase 5 — FE form lập/sửa (popup chọn hàng + chọn lô).
Blocked: không.

## Phase 3b — Test ghi ở BE ✅ (2026-08-24)

- [x] Lập phiếu: `ĐCHG-01426` · status 5 (Chờ TP) · 2 dòng · lịch sử ghi `create`
- [x] Sửa phiếu bị Không duyệt: 3 cột duyệt về `null`, status về 5, SL ghi lại đúng (vá #5).
      `canEdit` của người lập = yes, của người khác = no
- [x] TP duyệt → `needBoardApprove()` = false (hàng không gắn HĐ, tổng giá < `prepick_other_value`)
      nên đi thẳng Chờ KT (2) — đúng nhánh ERP
- [x] KT duyệt → ghi tồn thật: lô nguồn 53586 **5→4**, 53585 **4→3**; sinh 2 lô đích mới
      (`qty` 1, `expire_date` = đúng hạn lô nguồn 26/08, `company_id` **1 lấy theo lô nguồn** → vá #6);
      4 dòng `prepick_logs` **cùng `objectable_type = PrepickTransfer2Detail`** → vá #7
- [x] Không duyệt ở cấp TP: status 3, `manager_approver_status = 0`, lý do vào
      `manager_approved_comment`, KHÔNG đụng cột của cấp KT
- [x] Xoá phiếu: phiếu + 1 dòng chi tiết biến mất, **lịch sử còn đủ 4 dòng**
      `create → reject → update → delete`

## Phase 4 — FE màn danh sách + menu ✅ (2026-08-24)

- [x] `pages/finance/prepick-transfer-requests/index.vue` — 4 mixin, `V2BaseSmartFilterPanel`,
      10 cột hiện + 5 cột ẩn mặc định, `V2BaseRowActions` (`switch (action)`).
      Ô rỗng để TRỐNG (không dùng `|| '—'` như 3 màn Giữ hàng cũ)
- [x] 11 ô lọc: khối Công ty/Phòng ban · Trạng thái · Người nhận · Khách nhận (select tìm từ xa,
      nguồn `assign/customers` = id ERP) · Người tạo · Người duyệt · Tên hàng · Mã hàng ·
      **Số hợp đồng** (vá #13) · Ngày tạo từ/đến; tìm nhanh theo mã phiếu / người tạo
- [x] Menu: gắn link cho mục sẵn có `Phiếu Yêu cầu điều chuyển hàng giữ` (nhóm Giữ hàng) —
      đã bấm thật trên sidebar, link ra đúng `/finance/prepick-transfer-requests`
- [x] Bật `hrm_path` cho **2** entry `PrepickTransfer2` + `PrepickTransfer2Detail` trong
      `PrepickStockReportService::DOCUMENT_MAP` → link ở Lịch sử giữ hàng trỏ về màn HRM
- [x] Bấm thật trên trình duyệt (chờ 3,5s mỗi lần), **đối chiếu SQL khớp tuyệt đối**:
      không lọc **1.245** · Trạng thái "Chờ TP duyệt" **1** · Mã hàng `NAHU-NHXZ-04:02` **18** ·
      Người nhận 744 **13** · tìm nhanh `ĐCHG-01300` **1**. Badge "Đã duyệt" ra
      `rgba(22,163,74,...)` đúng mã màu BE. 0 lỗi console
- [ ] Nút **In** + **Xuất Excel** trên toolbar — làm ở Phase 7 cùng màn in/export

## Phase 5 — FE form lập / sửa ✅ (2026-08-24)

- [x] `components/PrepickTransferRequestForm.vue` — Người nhận / Khách hàng nhận (select tìm từ xa) /
      Ghi chú / đính kèm; dùng chung cho cả màn Chi tiết (`mode = show`)
- [x] Bảng chi tiết 11 cột + 3 popup: **Tìm kiếm hàng hoá** (tái dùng `PrepickStockSearchModal`,
      user chốt thêm 5 prop `endpoint`/`requireCustomer`/`title`/`subtitle`/`emptyText` thay vì
      chép bản thứ 2) · **Từ xuất giữ** (`PrepickLotSearchModal` MỚI, để ở `components/finance/
      prepick/` cho màn sau dùng lại) · **Đơn hàng/Hợp đồng** (`ContractSearchModal`, port ERP
      `searchAllContract` nhánh `can_prepick_product`)
- [x] Cột "Có thể giữ" gọi `/in-stock` SAU khi bảng đã hiện, kèm icon ⓘ phân biệt với "Đang giữ";
      ô ĐVT khoá cũng có ⓘ giải thích
- [x] Validate: SL > 0, SL ≤ đang giữ, chưa chọn lô, trùng lô, thiếu người/khách nhận — bấm thật:
      gõ 99 (đang giữ 7) ra đỏ *"Chuyển – Không được vượt số đang giữ (7)"*, **giữ nguyên số 99**,
      submit bị chặn, KHÔNG gọi API
- [x] `unsavedChangesMixin` + `markFormSaved()`; lưu xong **về thẳng danh sách** (đã bấm thật)
- [x] BE: `PrepickLotContractService` — **tách hàm suy hợp đồng của lô ra service dùng chung**
      (user chốt), màn Gia hạn chuyển sang gọi service này; **đã test lại màn Gia hạn**: 143 lô,
      126 lô có mã hợp đồng, không đổi
- [x] BE: endpoint `GET /contracts` (port `can_prepick_product`) + vá lỗi `contractable_type`
      mất dấu `\` do nhét chuỗi lớp vào `DB::raw`
- [x] Bấm thật cả luồng lập phiếu: chọn hàng → chọn lô (7 - KH - 14/09/2026) → nhập SL 3 → lưu →
      DB ra `ĐCHG-01428` status 5, 1 dòng chi tiết, lịch sử `create`. Đã dọn sạch dữ liệu test,
      đối chiếu 4 bảng `bak_*_20260824`: **0 chênh lệch**
- [ ] ⚠️ Nút **Từ chối** dùng chữ của skill button-convention (ERP ghi "Không duyệt") — cần user
      xác nhận rồi ghi vào design.md mục "Quyết định đã chốt"

## Phase 6 — FE chi tiết + 3 cấp duyệt ✅ (2026-08-24)

- [x] `_id/index.vue` (dùng lại form ở `mode = show`) + `RejectModal.vue`; nút dựng ở
      `#custom-actions` của `V2Footer` — nhãn nút duyệt đổi theo cấp (TP / BGĐ / KT duyệt)
- [x] Sửa câu xác nhận: giữ NGUYÊN nhãn nút thay vì `toLowerCase()` ("tp duyệt" nhìn như lỗi
      chính tả — màn Gia hạn đang bị, chưa sửa vì là màn đang chạy)
- [x] Khối "Lịch sử duyệt" 4 cột, dòng bị từ chối có nhãn đỏ; **dòng duyệt KHÔNG ghi chú vẫn
      hiện** (vá lỗi ERP #2) — đã kiểm bằng dòng TP duyệt không nhập ghi chú
- [x] Khối Lịch sử thao tác (mặc định ẩn, click mới nạp — `PrepickHistoryPanel` dùng chung)
- [x] Thông báo chuông: lập/sửa → TP **quản lý phòng của người nhận**; TP duyệt → BGĐ hoặc KT;
      BGĐ duyệt → KT; KT duyệt / từ chối → người lập. Nội dung theo template `[TC] {Nhóm}: {Mã}.`
      (ERP ghi nhầm "yêu cầu **xuất giữ**" ở 3 chỗ — vá lỗi #8)
- [x] **Bấm thật cả 3 luồng trên trình duyệt** (`ĐCHG-01429`, `ĐCHG-01430`):
      · TP duyệt → status 2, ghi `manager_approver_*`, **tồn KHÔNG đổi** (đúng: chỉ KT ghi tồn)
      · KT duyệt → status 1; lô nguồn **7 → 4**; sinh lô đích cho NV 744 qty 3, **giữ nguyên hạn
        14/09/2026**, `company_id` 1 theo lô nguồn; 2 log cùng `objectable_type`
      · Từ chối → chặn khi chưa nhập lý do; nhập rồi → status 3 + lý do vào cột của cấp TP,
        cột KT KHÔNG bị đụng; danh sách trả `is_can_edit/delete = true` cho người lập
      Đã dọn sạch dữ liệu test, đối chiếu 4 bảng `bak_*_20260824`: **0 chênh lệch**

## Phase 7 — In + xuất Excel ✅ (2026-08-24)

- [x] `renderPrint()` + blade `prepick-transfer-request.blade.php` — khổ **NGANG**, 9 cột
      (thêm cột "Từ xuất giữ" cho khớp màn hình) + bảng lịch sử duyệt đủ 4 cột và in cả cấp
      KHÔNG ghi chú (vá #3)
- [x] `renderPrintList()` + blade danh sách 9 cột, `exportData()` cho FE dựng Excel
- [x] 3 route `/export`, `/print-list-data`, `/{id}/print-data` (tổng **17 route**)
- [x] `_id/print.vue` + `print-list.vue` + `components/export-excel.js` (popup chọn trường,
      14 trường) + nút In / Xuất Excel trên toolbar + hành động In từng dòng + nút In màn chi tiết
- [x] Bấm thật: bản in 1 phiếu — giấy rộng **1007px** (A4 ngang), nền xám `rgb(238,238,238)`,
      nút In thẳng mép phải giấy (1019 = 1019), 9 cột + bảng duyệt 3 dòng + 4 khối ký;
      in danh sách `?status=5` ra **"Tổng số phiếu: 1"** khớp bộ lọc;
      xuất Excel tải về thật `danh_sach_yeu_cau_dieu_chuyen_hang_giu.xlsx` (**103.907 bytes**),
      đọc `sharedStrings.xml`: tiêu đề + đủ header (có Người nhận / Khách nhận)

## Phase 8 — Đính kèm ✅ (2026-08-24)

- [x] `V2BaseFile` + upload S3 — gọi thật `POST /upload-files`: trả URL
      `.../prepick_transfer2/dkpdf-...pdf` (đúng thư mục ERP), giới hạn 13 MB + bộ đuôi như ERP
- [x] Xem / tải / gỡ file ở màn Thêm-Sửa; màn Chi tiết chỉ xem (nút gỡ ẩn theo `isShow`)

## Phase 9 — Checklist + verify + bàn giao ⏳ (chờ user test tay)

- [x] **6 lệnh grep tự kiểm chạy SẠCH**: `status-pill` / `V2BaseFilterPanel` chỉ khớp trong
      COMMENT giải thích; `interactable:` `action.key ===` `advanced-filters` = 0; 2 trường hợp
      còn lại là cố ý (`Xuất Excel thành công` — bảng QLDA không có mã cho việc xuất file;
      `<button class="close">` — nút × của `b-modal`, y hệt các popup đã port)
- [x] Không còn ô nào in dấu `—` (rule 22/08/2026)
- [~] Checklist A→H: đã soát mục A (danh sách), B (nút), C (hiển thị), D (form), E (chi tiết),
      G (thông báo). **Bổ sung nút Sửa / Xóa ở footer màn Chi tiết** cho khớp cột Hành động
      ngoài danh sách (mục 7.2) — đã bấm thật trên phiếu bị Không duyệt: Sửa · Xóa · In · Quay lại.
      Mục F (Import) không áp dụng — màn này không có import
- [~] Đối chiếu ngược §2 design: đã soát cột danh sách + bộ lọc + điều kiện ẩn/hiện nút.
      Còn phải rà lại bảng chi tiết so với ERP lần cuối khi user test tay
- [x] Bấm thật bằng Playwright: danh sách + 4 ô lọc · form lập phiếu (chọn hàng → chọn lô →
      SL → lưu) · validate vượt SL · chi tiết · TP duyệt · KT duyệt (ghi tồn thật, đã đo DB) ·
      Từ chối · màn Sửa (nạp đủ giá trị, kể cả select khách hàng tìm-từ-xa) · 2 màn in · xuất Excel.
      **Mọi lần test đều hoàn nguyên DB, đối chiếu 4 bảng `bak_*_20260824`: 0 chênh lệch**
- [ ] User bấm tay trên dev bằng tài khoản KHÔNG phải Super admin, đủ 3 cấp duyệt TP → BGĐ → KT
- [ ] Cập nhật `.plans/gop-db/STATUS.md`, xoá 4 bảng `bak_*_20260824` sau khi user nghiệm thu

---

## Phase 9b — Rà lại bằng Playwright (2026-08-25) ✅

Đợt verify riêng theo yêu cầu user, bấm thật từng chức năng của màn mới:

- [x] Danh sách: 10 cột đúng thứ tự · 3 badge ra đúng 3 mã màu chuẩn (`#DC2626` Không duyệt ·
      `#D97706` Chờ TP · `#16A34A` Đã duyệt) · ô rỗng để trống
- [x] Cột Hành động theo trạng thái: phiếu **Không duyệt** → Sửa · Xóa · menu ⋮ (In, Lịch sử);
      phiếu **Chờ TP** → Duyệt · In · Lịch sử; phiếu **Đã duyệt** → In · Lịch sử
- [x] Bộ lọc đối chiếu SQL: Khách nhận 27400 → **16** = SQL 16 · Số hợp đồng `TPE` → **230** =
      SQL 230 · Người tạo 13 → **2** = SQL 2 · Làm mới → 1.247 và xoá sạch điều kiện
- [x] Sắp xếp cột Mã phiếu: tăng dần `ĐCHG-00001…00020`, giảm dần `ĐCHG-01433…01288`
- [x] Phân trang: sang trang 2 ra 10 dòng; đổi 20 dòng/trang thì **nhảy về trang 1**
- [x] Cấu hình cột: bật "Ghi chú" → cột hiện ngay; tắt lại → biến mất (đã trả về mặc định)
- [x] Popup Lịch sử ở dòng: 2 mốc, **mới → cũ**, có diff hàng hoá + người thực hiện `Mã phòng - Tên`
- [x] Nút Sửa: mở đúng màn Sửa, nạp đủ dữ liệu (kể cả select Khách nhận tìm-từ-xa)
- [x] Sửa rồi Gửi duyệt: status về 5, **cả 3 khối duyệt reset NULL** (vá #5), SL ghi lại đúng,
      lịch sử `create → reject → update`
- [x] Nút Xóa ở dòng: popup "Bạn có chắc muốn xóa phiếu ĐCHG-01433?" → toast "Xóa thành công.",
      dòng biến mất, **lịch sử còn đủ 5 mốc** (có `delete`)
- [x] **BUG TÌM RA + ĐÃ SỬA**: form gọi `markFormSaved()` ngay sau khi nạp dữ liệu → cờ
      `unsavedIgnore` bật VĨNH VIỄN nên cảnh báo "chưa lưu" **không bao giờ hiện**. Sửa thành
      `markFormPristine()`. Bấm lại: gõ ghi chú → Quay lại → hiện popup "Thông tin chưa lưu /
      Thoát / Ở lại", chọn **Ở lại** thì vẫn ở màn Sửa
- [x] 0 lỗi console suốt đợt; dọn sạch dữ liệu test, đối chiếu 4 bảng `bak_*_20260824`:
      **0 chênh lệch**
- [x] ⚠️ **Đã vá cùng lỗi `markFormSaved()` cho 2 màn đang chạy** (user duyệt 25/08): màn Gia hạn
      (`loadStock` + `loadDetail`) và màn Phiếu hủy hàng giữ (2 chỗ nạp dữ liệu) -> đổi sang
      `markFormPristine()`. Bấm thật màn Gia hạn: gõ ghi chú -> Quay lại -> hiện popup
      "Thông tin chưa lưu", chọn Ở lại thì vẫn ở màn; F5 cũng bật hộp thoại của trình duyệt
- [x] Vá câu xác nhận duyệt màn Gia hạn: bỏ `toLowerCase()` ("tp duyệt" -> "TP duyệt")
- [x] **Bỏ dấu `—` ở ô rỗng cho 3 màn Giữ hàng cũ** (rule 22/08): 43 chỗ `|| '—'` + 7 chỗ
      `placeholder="—"` trong 6 file. GIỮ LẠI 2 chỗ dấu — nằm giữa câu văn (hạn cảnh báo /
      trần hạn giữ) và dòng "Người lập — Ngày lập" vì đó là dấu ngăn cách, không phải ô rỗng
- [x] **Bấm Lưu là NHẢY TỚI ĐÚNG DÒNG LỖI** (user chốt hướng 25/08: toast cứ để câu chung, việc
      cần là trỏ về dòng — inline đã ghi chi tiết rồi). Thêm util dùng chung
      `utils/scrollToFirstError.js`: tìm ô lỗi -> cuộn cả `<tr>` vào giữa màn hình -> kéo ngang tới
      đúng ô -> nháy nền đỏ 1,5s + focus. Gom 4 khối cuộn viết tay ở 4 form nhóm Giữ hàng về util.
      2 bẫy đo được: `V2BaseError` render `.v2-error` (không phải `.invalid-feedback`), và
      `V2BaseDatePicker` có lỗi mà wrapper KHÔNG có `is-invalid` -> bản đầu tìm không ra ô nào.
      Bấm thật: phiếu **116 dòng** đang ở cuối trang (scrollTop 7337) -> bấm Duyệt nhảy về dòng 1
      (scrollTop 143, dòng giữa khung nhìn, nền nháy `rgba(220,38,38,0.08)`); bảng 3 dòng chỉ
      **dòng 3** thiếu lô -> từ đầu trang tự cuộn xuống đúng dòng 3; màn Yêu cầu hủy vẫn báo đúng
      lỗi inline. Đã ghi vào skill `form-validate` mục 3b
- [x] Bấm thật lại 3 màn cũ sau khi sửa: Gia hạn (list + chi tiết + form), Phiếu hủy hàng giữ
      (list + chi tiết), Yêu cầu hủy hàng giữ (list) — dữ liệu lên đủ, badge đúng màu,
      **không còn dấu `—` trong bảng**, 0 lỗi console

---

## Phase 10 — Vá QA redmine 11279 / 11296 (2026-09-04)

- [x] **11279** — một hàng hoá đang giữ cho **2 khách hàng / 2 hạn khác nhau** phải thêm được 2
      dòng (ERP cho phép). Popup đang loại theo `product_id` nên dùng 1 lô là mất luôn các lô còn
      lại. Chuyển sang loại theo **LÔ**: FE gửi `exclude_lot_ids[]` (`prepick_detail_id` của ô
      "Từ xuất giữ"), BE `PrepickStockService::searchHoldingProducts()` lọc `pd.id NOT IN (...)`
      — hàng chỉ rơi khỏi popup khi **hết sạch lô** chưa dùng, và `held_qty` chỉ còn cộng phần
      lô còn lại. 2 màn Hủy / Gia hạn giữ nguyên cách loại theo hàng hoá (mỗi hàng 1 dòng).
- [x] **11296** — 404 báo "Không tìm thấy dữ liệu" + trả về danh sách.
- [ ] User verify trên dev với hàng có nhiều lô.

### Checkpoint — Phase 10

```text
Vừa hoàn thành: 11279 (FE modal + FE màn + BE service/controller), 11296.
Đang làm dở: không.
Bước tiếp theo: user verify trên dev.
Blocked: không.
Verify: chạy thật `searchHoldingProducts()` trên `gop_db` với NV 1028 / hàng 22325 (4 lô, tổng 9):
loại 1 lô -> hàng VẪN còn, held_qty 9 -> 7; loại hết 4 lô -> hàng biến mất; loại theo product ->
biến mất (giữ nguyên hành vi cũ cho 2 màn kia).
```

---

## Bẫy đã biết — đọc lại trước mỗi phase

| Bẫy | Cách tránh |
|---|---|
| Màn này **không có nháp** | Lập phiếu là `CHO_TP_DUYET`; chỉ phiếu **Không duyệt** mới sửa/xoá được |
| TP duyệt xét phòng ban **người nhận** | Đừng đọc `department_id` trên phiếu — phải join `to_employee.info` |
| `prepick_transfer2_details` không có `unit_coefficient` | `qty` đã là ĐV cơ bản, đừng nhân hệ số |
| Khách nhận rỗng ở phiếu cũ | Lỗi dữ liệu DB gộp (79/1.295), KHÔNG nới join để "chữa" |
| ERP ghi 2 `objectable_type` cho 1 lần chuyển | HRM thống nhất `PrepickTransfer2Detail` |
| `V2Footer` tự chèn popup cho `menu.approve` | Dựng nút ở `#custom-actions` |
| `V2BaseRowActions` emit chuỗi key | `switch (action)`, đừng so `action.key` |
| `V2BaseButton` không có prop `disabled` | Ẩn bằng `v-if` / `visible` |
| Ô khoá nhìn như ô trống | Kèm icon ⓘ + tooltip nói rõ vì sao khoá |
| Test bộ lọc chờ < 3s | API dev ~1.2s baseline → số lệch một nhịp, dễ báo nhầm bug |
