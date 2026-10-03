# Phiếu yêu cầu gia hạn hàng mượn — plan

Thiết kế: [`./design.md`](./design.md) · Nhánh dự kiến: `feat/finance-borrow-extend-request`

Khuôn mẫu bám theo: màn sinh đôi `prepick-extend-requests` (Yêu cầu gia hạn hàng giữ).
**Đọc mục 3 của design.md trước khi chép bất cứ dòng nào** — mã trạng thái 3/4/5 của hai màn
mang nghĩa khác nhau.

---

## Phase 0 — Khảo sát & chốt hướng ✅ (2026-09-24)

- [x] Tìm màn ERP: `borrowExtendRequest` — controller + model + 6 blade
- [x] Soi HẾT 4 dòng menu ERP trỏ tới màn này → chỉ 1 controller action, 2 preset; `forAccounting`
      là route chết (áp bài học port nhầm biến thể của `finance-borrow-stock-list`)
- [x] Đọc `searchByFilter()` — 4 nhánh phạm vi xem + nhánh `for-approve`
- [x] Đọc luồng duyệt 3 cấp `approve()` / `deny()` / `checkSwitchApprove()`
- [x] Xác nhận tác động nghiệp vụ duy nhất: KT duyệt mới ghi `product_export_requests.return_date`
- [x] Đo dữ liệu `gop_db`: 2.607 phiếu (status 1: 2.539 · 3: 65 · 4: 3)
- [x] Xác nhận **không cần tạo quyền mới** — 6 quyền đã có (design.md mục 5)
- [x] Xác nhận `due_configs` id=25 "Duyệt gia hạn hàng mượn" đã có sẵn, HRM có middleware `dueConfig`
- [x] Phát hiện 5 lỗi ERP (design.md mục 9)
- [x] Chốt với user: làm đủ như ERP **+ bản in** · **+ bảng lịch sử** · **sửa hết 5 lỗi bên HRM**

## Phase 1 — Migration bảng lịch sử ✅ (2026-09-24)

Nhánh `feat/finance-borrow-extend-request` tách từ `origin/gop_db` (đã chứa bản merge
`feat/finance-borrow-stock-list`). Chỉ tạo nhánh Ở REPO `hrm-api` — `hrm-client` đợi Phase 6.

- [x] Đọc skill `entity-history` trước khi viết (§2 quy định cấu trúc bảng)
- [x] Migration `2026_09_24_000001_create_borrow_extend_request_history_table.php`, bám khuôn
      `2026_08_22_000001_create_prepick_extend_request_history_table.php`
- [x] Tên bảng SỞ ÍT `borrow_extend_request_history` (đúng tiền lệ, không phải `_histories`)
- [x] Tên index đặt TAY: `ber_history_request_id_index` / `ber_history_company_id_index`
- [x] Có cột `note` riêng — lý do không duyệt / ghi chú duyệt của từng cấp phải hiện được
      trên lịch sử (skill §4.1), KHÔNG nhồi vào `new_value`
- [x] Không khoá ngoại cứng, không SoftDeletes, PHPDoc trên `up()`/`down()`
- [x] `php -l` sạch
- [x] Chạy migrate trên `gop_db` local → 11 cột + 2 index đúng tên như thiết kế
- [x] Thử `migrate:rollback` → bảng biến mất sạch, rồi migrate lại → OK (`down()` dùng được thật)
- [x] **KHÔNG cần khoá dạng BẢNG** (skill §3): màn này không có bảng chi tiết riêng,
      mặt hàng đọc từ phiếu cha và người dùng không sửa được

### User đã chốt 24/09 (skill `entity-history` §0) — áp vào Phase 3-4

- [x] Trường theo dõi: **Ngày hẹn trả mới · Ghi chú · File đính kèm** (3 ô người dùng nhập
      được). `return_date` chụp từ phiếu cha nên không theo dõi.
- [x] Quyền xem lịch sử: **không thêm quyền riêng** (vào được màn là xem được) — mặc định của skill
- [x] Action: `create` · `change_status` cho TP/BGĐ/KT duyệt và từ chối (mỗi cấp 1 dòng riêng,
      kèm ghi chú của cấp đó). Không có `update` vì màn không cho sửa — **trừ** ô Ngày hẹn trả mới
      mà Kế toán sửa được lúc duyệt ⇒ ghi thêm 1 dòng `update` cho riêng ô đó

## Phase 2 — BE entity & truy vấn ✅ (2026-09-24)

- [x] `Entities/BorrowExtend/BorrowExtendRequest.php` — hằng số trạng thái **của riêng màn mượn**
      (3 = Không duyệt, 4 = Chờ TP, 5 = Chờ BGĐ), có bảng đối chiếu với màn sinh đôi ngay trong
      docblock để người sửa sau không chép nhầm
- [x] Quan hệ tới phiếu cha (`ProductExportRequest` — model CHỈ ĐỌC dùng chung, chỉ đọc, không
      thêm hàm ghi) + 3 người duyệt + công ty + phòng ban
- [x] `Entities/BorrowExtend/BorrowExtendRequestHistory.php` — 6 action, không có `send_approve`
      (màn không có nháp); `update` chỉ dành cho ô Ngày hẹn trả mới Kế toán sửa lúc duyệt
- [x] `searchByFilter()` — 4 nhánh phạm vi + luật status 3 chỉ người lập thấy + điều kiện
      `company_id` cuối hàm (giữ nguyên ERP, chặn thêm `companyId` null để không thành `IS NULL`)
- [x] Nhánh `for-approve` bọc thành MỘT nhóm `where(fn)` thay vì chuỗi `orWhere` phẳng của ERP
- [x] `applyFilters()` — 11 ô lọc + ô tìm nhanh; 3 chỗ `pluck+whereIn` của ERP đổi sang `whereHas`
- [x] `applySort()` — 5 cột sắp được, chốt `id DESC` cuối để lật trang không lặp
- [x] `Services/BorrowExtendRequestService` — `searchByFilter` / `meta` / `findOrFail`
- [x] `meta()` trả trạng thái **đủ 5 giá trị** (lỗi ERP #5) + 4 cờ quyền cấp màn
- [x] `Transformers/BorrowExtendResource/BorrowExtendRequestListResource` — 11 cột ERP + 3 cột ẩn
      sẵn; KHÔNG có cột Người/Ngày cập nhật vì màn không cho sửa
- [x] ~~Nạp mặt hàng của phiếu cha cho cả trang~~ — **KHÔNG CẦN Ở DANH SÁCH**: 11 cột ERP không có
      cột mặt hàng nào, bộ lọc Tên hàng/Model đi bằng `whereHas`. Chuyển việc nạp mặt hàng sang
      Phase 7 (màn chi tiết) — sửa lại ước lượng ban đầu của plan
- [x] `php -l` sạch cả 4 file

### Đo thật trên `gop_db` — 5 hạng quyền, đối chiếu SQL thuần dựng độc lập

| NV | Quyền | preset `all` | SQL thuần | khớp | `for-approve` |
| --- | --- | --- | --- | --- | --- |
| #13 DNS Admin | Super Admin | 1.176 | 1.176 | ✅ | 3 |
| #34 Đào Thị Thúy | Super Admin | 1.176 | 1.176 | ✅ | 3 |
| #24 Nguyễn Đức Tuân | xem theo phòng ban + TP duyệt | 193 | 193 | ✅ | 0 |
| #35 Trần Ngọc Duy | xem theo phòng ban + TP duyệt | 146 | 146 | ✅ | 0 |
| #101 Nguyễn Văn Thắng | không quyền nào | 18 | 18 | ✅ | 18 |

Con số tự nhất quán: công ty 1 có 1.210 phiếu, trong đó 34 phiếu "Không duyệt" ⇒ Super Admin
thấy 1.210 − 34 = **1.176** (phiếu bị từ chối của người khác bị ẩn đúng luật). Người không
quyền chỉ thấy 18 phiếu của mình, `for-approve` cũng 18 (không quyền duyệt thì về phiếu của mình).

### Lỗi ERP #6 — LỖ PHÂN QUYỀN, phát hiện khi viết Phase 2

`BorrowExtendRequestController::index()` mặc định `$type = 'index'` khi URL không có tham số, nhưng
`searchByFilter()` **không có nhánh nào cho `index`** ⇒ chỉ còn điều kiện công ty ở cuối hàm ⇒
người **không có quyền xem nào** mà gõ thảng URL không tham số sẽ thấy **TOÀN BỘ 1.210 phiếu**
của công ty thay vì 18 phiếu của mình. Các dòng menu đều truyền `?type=` nên lỗi chỉ lộ khi vào
bằng URL trần.

→ HRM coi **mọi giá trị `type` lạ (và không truyền gì) là `all`**, tức luôn đi qua `applyViewScope()`.
Script đo đã kiểm điều này: không truyền `type` ra kết quả **giống hệt** preset `all` ở cả 5 hạng.

### 2 lỗi phân quyền khác đã vá trong entity (lỗi ERP #7, #8)

- #7 `canView()` của ERP cho `Kế toán kho` và `Ban giám đốc duyệt hàng mượn` xem phiếu của **mọi
  công ty** (2 nhánh đầu không so `company_id`), và **không xét 3 quyền xem theo cấp** nên người
  có quyền xem bấm vào phiếu lại ra `not_found`. HRM siết cùng công ty + bổ sung 3 nhánh.
- #8 `canTPApprove()` của ERP không so công ty ⇒ TP công ty A duyệt được phiếu công ty B khi trùng
  `department_id`. HRM siết thêm cùng công ty (khớp 2 cấp còn lại).

## Phase 3 — BE tạo phiếu ✅ (2026-09-24)

- [x] `Http/Requests/BorrowExtend/BorrowExtendRequestStoreRequest` — chuẩn hoá `new_return_date` về
      `Y-m-d` ở `prepareForValidation`, nhận cả `dd/mm/yyyy` (lỗi ERP #3); lọc rỗng mảng đính kèm
- [x] `after:today` + chặn vượt `configs.max_borrow_date` so bằng Carbon thật (lỗi ERP #4), giữ câu
      ERP "Không thể mượn quá dd/mm/yyyy". Đọc `configs` thẳng trong service, KHÔNG thêm hàm vào
      `PrepickConfigService` dùng chung (phải hỏi user trước)
- [x] `eligibleParentsQuery()` — NGUỒN DUY NHẤT cho cả popup chọn phiếu lẫn chốt chặn lúc lưu:
      `type=3, status=5, borrow_status=2, created_by=mình`, không có yêu cầu gia hạn chưa chốt (lỗi ERP #1)
- [x] Vá thêm **lỗi ERP #10**: `can_borrow_extend` viết `A || B && C` thiếu ngoặc → cho gia hạn cả
      phiếu ĐÃ TRẢ HẾT hàng. HRM đòi đủ `status=5` VÀ `borrow_status=DA_MUON`
- [x] `lockForUpdate` phiếu cha trong transaction — bấm Gửi 2 lần không đẻ 2 yêu cầu mở
- [x] Đính kèm lưu chuỗi nối `", "` đã lọc rỗng (lỗi ERP #2) — vẫn đúng định dạng cột ERP đọc
- [x] Mã `PGHHM-` + `generateCode(5, id)` giữ đúng ERP → 2 cổng cùng dãy số
- [x] Ghi lịch sử `create`; thông báo cho TP **đang quản lý đúng phòng ban** của phiếu (nhánh
      `$is_same_department` của ERP `NotificationHelper`)

## Phase 4 — BE duyệt / từ chối ✅ (2026-09-24)

- [x] 1 endpoint `approve` cho 3 cấp, tự nhận cấp theo trạng thái, `lockForUpdate`, kiểm quyền ĐÚNG cấp
- [x] Kế toán gửi kèm `new_return_date` sửa lại → dòng lịch sử `update` RIÊNG trước dòng duyệt;
      TP/BGĐ gửi lên thì BE bỏ qua
- [x] `needBoardApprove()` giữ công thức ERP `Σ (exported_qty − returned_qty) × price` trên MỌI dòng;
      KHÔNG dùng `PrepickApprovalRouteService` (công thức nhóm hàng giữ tính theo hợp đồng, khác hẳn)
- [x] KT duyệt → ghi `product_export_requests.return_date` bằng query builder (model phiếu cha chỉ đọc)
- [x] `reject` ghi lý do vào đúng cặp cột của cấp đang duyệt, status 3
- [x] `BorrowExtendRequestNotifyService` — 5 sự kiện đúng người nhận ERP, khuôn
      `[PGHHM] {Hành động}: <b>{mã}</b>. {Ghi chú}`; gửi NGOÀI transaction, lỗi gửi không rollback phiếu
- [x] Vá **lỗi ERP #11**: khối "Lịch sử ghi chú duyệt" ERP chỉ đọc cấp TP + KT và chỉ khi có ghi chú
      → mất hẳn cấp BGĐ. HRM liệt kê đủ cấp đã đóng dấu, đánh dấu cấp đã từ chối

## Phase 5 — BE controller, route, phân quyền ✅ (2026-09-24)

- [x] `V1/BorrowExtendRequestController` — 12 route, KHÔNG `update`/`destroy`
- [x] `dueConfig:Duyệt gia hạn hàng mượn,manager` trên route duyệt (đã kiểm gắn đúng qua router)
- [x] Route tĩnh khai trước `/{id}`
- [x] `php artisan route:list` vỡ do 1 controller KHÁC (lỗi có sẵn, không liên quan) — kiểm route bằng
      script đọc router
- [x] Sửa luôn comment lạc hậu của nhóm route `borrow-expiring` (sau bản fix 24/09)

### Chạy thử E2E tầng service — **48/48 đạt**, rollback sạch

Script bọc 1 transaction rồi rollback; fake Notification + Bus, mock `Redis::publish` để GHI LẠI người
nhận mà không bắn thật; hạ tạm `borrow_limit_value` để chạy được nhánh BGĐ (mọi phiếu thật đều < 20tr).
Phủ: popup chọn phiếu (NV#101 thấy 7, NV#13 không thấy phiếu người khác) · 5 ca validate · tạo 2
phiếu · chặn phiếu thứ 2 · TP thật (NV#96) → BGĐ → KT sửa ngày → `return_date` phiếu cha đổi
`2026-04-24 → 2026-09-29` · nhánh dưới ngưỡng bỏ qua BGĐ · từ chối không đụng phiếu cha · phạm vi
xem sau thao tác · 5 dòng lịch sử MỚI→CŨ · detail / in / in danh sách / export 12 khoá · preset
`for-approve` + bộ lọc không rò. Sau rollback: 0 phiếu rác, ngưỡng công ty về 20.000.000.

## Phase 6 — FE màn danh sách ✅ (2026-09-24)

- [x] `pages/finance/borrow-extend-requests/index.vue` — 11 cột ERP + 3 cột ẩn, 9 ô lọc (7 ERP + tổ chức + ngày)
- [x] Preset `?type=all` / `?type=for-approve` đọc từ URL; watcher `listType` tự nạp lại khi bấm menu khác preset
- [x] 4 mixin chuẩn + watcher so bản sao sâu; `localStorageKey` / `columnScreenKey` riêng
- [x] Hành động dòng: Duyệt (link chi tiết) · Từ chối · In · Lịch sử — không Sửa/Xoá
- [x] Cột "Phiếu mượn" link `/finance/product-export-requests/{id}` (cùng đích các màn anh em)
- [x] `components/export-excel.js` — 9 cột ERP + 3 cột ẩn, tên file giữ đúng ERP
- [x] `RejectModal` dựng trên `V2BaseModal` (skill modal-popup §0) — KHÔNG chép bản `b-modal` tự dựng
      của màn sinh đôi
- [x] Menu: `finance.js` (Kho/Kế toán kho → Mượn hàng) · `sale-hub.js` · nhóm hub MỚI "Hàng mượn chờ
      duyệt" (ERP `topmenubar :2294`, gate `Kế toán kho`) — chỉ khai mục của màn này

## Phase 7 — FE màn tạo & màn chi tiết ✅ (2026-09-24)

- [x] `BorrowExtendRequestForm.vue` dùng chung Tạo + Chi tiết — `V2BaseFormSection` + `V2BaseAttachmentSection`
      (khuôn đã sửa ở màn YCMDV), KHÔNG chép `form-card` tự dựng của màn sinh đôi
- [x] `BorrowPickerModal.vue` (trên `V2BaseModal`) — chọn 1 phiếu, nói rõ vì sao rỗng
- [x] Mọi ô khoá có ⓘ giải thích; date picker chặn ngoài khoảng [ngày mai, trần] khớp 2 rule BE
- [x] Nút: Gửi duyệt (cam) · TP/BGĐ/KT duyệt (teal, có `$confirm` nói rõ hậu quả bước KT) · Từ chối · In
- [x] Mọi thao tác xong về danh sách (quy ước Redmine 11107)
- [x] Khối "Lịch sử duyệt" + "Lịch sử thay đổi" (thu gọn sẵn, badge số mốc, ghi chú phiếu xử lý bên ERP
      không có trong lịch sử)
- [x] `vue-template-compiler` + babel biên dịch sạch 6 file `.vue` + 3 file JS

## Phase 8 — Bản in ✅ (2026-09-24)

- [x] `finance::prints.borrow-extend-request` + `borrow-extend-request-list` (khuôn `prepick-extend-request`)
- [x] KHÔNG dùng `report_templates` của ERP; khổ ngang; số chuẩn quốc tế
- [x] FE qua `reportPrintPreviewMixin` — popup xem trước, không mở tab riêng

## Phase 9 — Nghiệm thu ✅ (2026-09-24) — CHƯA commit, chờ user chốt

Tự chạy 2 server local (nhánh mới), Playwright `playwright-a`, tài khoản DNS Admin (NV#13), **xem ảnh**
từng màn. Đã đóng browser + tắt 2 server sau khi xong.

- [x] Danh sách: **1.176 phiếu** = đúng số đo ở Phase 2 · badge vàng/xanh đúng nhóm · console 0 lỗi
- [x] Lọc Trạng thái "Chờ TP duyệt" → 3 (tự nạp khi chọn) · ô gõ tay Phiếu mượn + Enter → 1 · Làm mới → về 1.176
- [x] Dropdown Trạng thái đủ **5 giá trị** theo thứ tự vòng đời (lỗi ERP #5)
- [x] Preset `?type=for-approve` → tiêu đề "…chờ duyệt", 3 phiếu (= số đo)
- [x] Tạo: bấm Gửi khi trống → 2 lỗi inline đúng dạng `Tên trường – Nội dung` · popup chọn phiếu chỉ ra
      **6 phiếu của chính mình** · lịch chỉ cho chọn 25/09 → 01/10 (ngày mai → hôm nay + 7) · gửi → về
      danh sách, DB đúng (status 4, `return_date` chụp từ phiếu cha, lịch sử `create`)
- [x] Thông báo lúc tạo: 0 người nhận — đúng nghiệp vụ (người duy nhất quản lý phòng 111 là NV#224,
      không có quyền TP duyệt), giống ERP
- [x] Chi tiết: tiêu đề kèm mã · ô khoá có ⓘ · link phiếu mượn · nút đúng cấp (TP duyệt / Từ chối / In)
- [x] TP duyệt (popup xác nhận nút xanh) → status 2 (dưới ngưỡng, bỏ qua BGĐ) · về danh sách
- [x] KT: ô Ngày hẹn trả mới **mở khoá** · sửa 30/09 → 01/10 · popup nói rõ hậu quả · duyệt → status 1,
      **`product_export_requests.return_date` 23/09 → 01/10** · lịch sử `create → tp_approve → update → kt_approve`
- [x] Phiếu mượn đã chốt quay lại popup chọn phiếu, hiện hạn mới 01/10
- [x] Từ chối từ menu dòng ở danh sách: lỗi bắt buộc lý do · xác nhận → Không duyệt, danh sách tự nạp,
      dòng chỉ còn In/Lịch sử
- [x] Popup Lịch sử ở danh sách: dòng Không duyệt kèm lý do trong khối ghi chú vàng — y hệt khối ở màn chi tiết
- [x] In phiếu (header công ty, bảng hàng, bảng 2 cấp duyệt, 4 ô ký) · In danh sách theo bộ lọc
- [x] Popup Xuất Excel tick sẵn đúng 9/12 cột đang hiện
- [x] File Excel — Playwright MCP sập lúc bắt sự kiện download nên kiểm bằng cách khác: chạy NGUYÊN VĂN
      `export-excel.js` trong Node (stub `Blob` + `file-saver`) với dữ liệu thật từ `exportData()`, rồi mở
      lại file đọc từng ô. Đúng: tên file ERP, tên sheet, tiêu đề, dòng khoảng ngày, **thứ tự cột = thứ tự
      tick** (tick lộn 5 cột ra đúng thứ tự đó), 3 dòng dữ liệu = 3 dòng API, khối ký cuối file; không tick
      gì thì xuất đủ 12 cột + STT

### Lỗi bắt được khi bấm thật — đã sửa

| Lỗi | Nguyên nhân | Sửa |
| --- | --- | --- |
| Vue warn `visibleExportFields is not defined` | Dùng `:default-selected="visibleExportFields"` mà không nạp `exportFieldsMixin` — **màn sinh đôi gia hạn hàng giữ cũng dính y lỗi này** (chưa sửa bên đó: màn người khác đã chạy) | Nạp `exportFieldsMixin` |
| Chữ nút "Chọn phiếu" gãy 2 dòng | Nút nằm cạnh ô giãn hết cỡ nên bị ép | `white-space: nowrap; flex-shrink: 0` |
| Viền đỏ ô ngày không tắt khi đã chọn ngày | Lỗi chỉ xoá khi bấm lưu lại | watcher xoá lỗi khi ô có giá trị (skill form-validate) |
| Bảng 2 dòng chiếm **491px** trắng | `assets/scss/default.scss:88` ép `.table-responsive { min-height: 50vh }` cho MỌI màn | Dùng wrapper riêng `.ber-scroll`; rule dùng chung KHÔNG sửa |
| Bản in danh sách ghi "Người lập / Ngày lập" | Chép chữ ERP | "Người tạo / Ngày tạo" cho khớp màn + Excel |

### Dọn dữ liệu test (user cho phép sửa DB local) — đã về đúng trạng thái trước

Xoá 2 phiếu test (#2614, #2615) + 6 dòng lịch sử + 88 job hàng đợi (44 push Firebase + 44 broadcast — không
có worker chạy nên chưa bắn đi đâu) + 44 thông báo chuông; trả `return_date` PYCXH-35542 về 23/09.
Kiểm lại: 2.607 phiếu, 0 job/thông báo/lịch sử thừa. ⚠️ `AUTO_INCREMENT` đã nhảy (id 2608-2615 bị bỏ
qua do rollback + xoá) — chỉ ở DB local, không ảnh hưởng dev.

### Còn cho user quyết

- Commit / đẩy dev (em không commit).
- 2 thứ em để nguyên vì đụng chung: bỏ `.table-responsive { min-height: 50vh }` toàn cục; nạp
  `exportFieldsMixin` cho màn gia hạn hàng giữ.
- Bộ lịch sử dùng `PrepickHistoryPanel` của nhóm hàng giữ (suy ô lọc từ log, lệch skill §0a) để đồng bộ
  6 màn anh em; BE đã trả sẵn `action_group` + `actor_id` nếu muốn chuyển sang `SystemInfoSection`.
- Thêm `maxBorrowDate()` vào `PrepickConfigService` dùng chung (hiện đọc `configs` thẳng trong service).
