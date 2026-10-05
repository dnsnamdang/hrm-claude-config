# Thiết kế — Phiếu yêu cầu gia hạn hàng mượn (ERP → HRM)

> Khảo sát 24/09/2026. Nguồn ERP: repo `TanPhatDev`, nhánh `master`.
> Màn ERP: `borrowExtendRequest` (`app/Http/Controllers/Warehouse/BorrowExtendRequestController.php`).

## 1. Màn ERP nào được port — đã soi HẾT các cửa vào

Bài học rút từ màn "Hàng sắp hết hạn mượn" (port nhầm biến thể, xem
`.plans/gop-db/finance-borrow-stock-list/design.md` mục 11): grep ra bao nhiêu dòng menu thì phải
mở bấy nhiêu route để đối chiếu, KHÔNG suy đoán. Lần này đã làm và kết quả khác lần trước.

| Dòng menu ERP | Route | Tham số gửi lên | Kết luận |
| --- | --- | --- | --- |
| Kho → Mượn hàng (`topmenubar.blade.php:326`) | `borrowExtendRequest.index` | `?type=all` | Màn chính |
| Kế toán kho → Mượn hàng (`:1064`) | `borrowExtendRequest.index` | `?type=all` | **Trùng y hệt dòng trên** — cùng route, cùng tham số |
| Hub "chờ duyệt" (`:2297`, bọc `@can('Kế toán kho')`) | `borrowExtendRequest.index` | `?type=for-approve` | Cùng màn, khác preset |
| — | `borrowExtendRequest.forAccounting` | `type='accounting'` | **Route CHẾT**: không dòng menu nào trỏ tới; view kiểu DataTable cũ chưa nâng cấp |

⇒ **1 màn danh sách HRM, 2 preset** (`all` / `for-approve`). Không port `forAccounting`.

Khác với cặp `expiringBorrow` / `accountingExpiringBorrow`: ở đó là HAI controller action khác
nhau nên phải chọn; ở đây là MỘT action, chỉ khác tham số, nên không có rủi ro chọn nhầm.

## 2. Dữ liệu

Bảng ERP `borrow_extend_requests` — **KHÔNG bảng chi tiết riêng**. Chi tiết mặt hàng đọc thẳng từ
phiếu cha `product_export_requests` (+ `product_export_request_details` với `need_export = 1`).
Đây là khác biệt lớn nhất so với màn sinh đôi bên hàng giữ (`prepick_extend_request_details`).

Đo trên `gop_db` ngày 24/09/2026: **2.607 phiếu** (status 1: 2.539 · 3: 65 · 4: 3), dữ liệu từ
08/08/2025 → 28/07/2026. Không có phiếu nào đang ở status 2 hoặc 5.

Cột đáng lưu ý: `return_date` (ngày hẹn trả CŨ, chụp lại lúc tạo), `new_return_date`,
`attachments` (chuỗi URL nối bằng `", "`), 3 cặp cột người duyệt / thời điểm / ghi chú cho 3 cấp
(`approver_*` = kế toán, `manager_approver_*` = trưởng phòng, `board_of_manager_approver_*` = BGĐ).

## 3. BẪY NẶNG NHẤT — mã trạng thái KHÁC màn sinh đôi

`prepick_extend_requests` và `borrow_extend_requests` dùng CÙNG dải số 1-5 nhưng **nghĩa khác nhau**:

| status | Gia hạn hàng GIỮ (HRM đã có) | Gia hạn hàng MƯỢN (màn này) |
| --- | --- | --- |
| 1 | Đã duyệt | Đã duyệt |
| 2 | Chờ KT duyệt | Chờ KT duyệt |
| 3 | **Đang tạo** (nháp) | **Không duyệt** |
| 4 | **Chờ BGĐ duyệt** | **Chờ TP duyệt** |
| 5 | **Chờ TP duyệt** | **Chờ BGĐ duyệt** |

Chép `PrepickExtendRequestService` sang mà không đổi hằng số là sai toàn bộ trạng thái, và sai
theo kiểu vẫn chạy được — phiếu "Không duyệt" sẽ hiện thành "Đang tạo".

Hệ quả thứ hai: hàng mượn **KHÔNG có trạng thái nháp**. Phiếu sinh ra thẳng ở status 4, nên màn
này **không có sửa, không có xoá** (ERP cũng không khai route `update`/`destroy`).

## 4. Luồng duyệt

```
Tạo (status 4 — Chờ TP duyệt)
  └─ TP duyệt ──┬─ tổng giá trị còn nợ > companies.borrow_limit_value → status 5 (Chờ BGĐ)
                │                                        └─ BGĐ duyệt → status 2 (Chờ KT)
                └─ không vượt                                         → status 2 (Chờ KT)
                                                  KT duyệt → status 1 (Đã duyệt)
Bất kỳ cấp nào Không duyệt → status 3
```

- Ngưỡng vượt cấp tính trong `checkSwitchApprove()`: tổng của `(exported_qty − returned_qty) × price`
  trên các dòng thuộc phiếu cha, so với `companies.borrow_limit_value` của công ty NGƯỜI ĐANG DUYỆT
  (`auth()->user()->info->company->borrow_limit_value`) — không phải công ty của phiếu. Giữ nguyên
  hành vi này, chỉ ghi chú lại.
- **Chỉ khi KT duyệt (status → 1)** mới ghi `product_export_requests.return_date = new_return_date`.
  Đây là toàn bộ tác động nghiệp vụ của màn: không đụng tồn kho, không hạch toán.
- Kế toán duyệt **được sửa `new_return_date`** ngay trên màn chi tiết trước khi bấm Duyệt
  (`show.blade.php` mở khoá ô này khi `canApprove()`), TP và BGĐ thì không.

## 5. Quyền — KHÔNG tạo quyền mới

Đã kiểm trên `gop_db` 24/09/2026, cả 6 quyền đều có sẵn:

| Quyền | guard | id | Dùng để |
| --- | --- | --- | --- |
| `Kế toán kho` | web / api | 100080 / 1136 | Duyệt cấp cuối, xem toàn công ty |
| `Trưởng phòng duyệt hàng mượn` | web | 100842 | Duyệt cấp 1 (bó theo phòng quản lý) |
| `Ban giám đốc duyệt hàng mượn` | web | 100952 | Duyệt cấp vượt ngưỡng |
| `Xem phiếu hàng mượn theo tổng công ty` | web | 100890 | Phạm vi xem |
| `Xem phiếu hàng mượn theo công ty` | web | 100891 | Phạm vi xem |
| `Xem phiếu hàng mượn theo phòng ban` | web | 100892 | Phạm vi xem |

3 quyền phạm vi chính là bộ đang dùng ở màn Danh sách hàng mượn. Vài quyền chỉ có guard `web`
nhưng `ChecksEmployeePermission` khớp **theo TÊN qua mọi guard** nên không cần seeder `api`
(đã kiểm chứng ở đợt `finance-borrow-stock-list`).

## 6. Phạm vi xem của danh sách

`BorrowExtendRequest::searchByFilter()` — 4 nhánh theo quyền, áp dụng khi `type = all`:

| Quyền cao nhất | Điều kiện |
| --- | --- |
| Xem theo tổng công ty | không bó thêm |
| Xem theo công ty | `company_id` = công ty mình **HOẶC** `created_by` = mình |
| Xem theo phòng ban | `department_id` thuộc phòng mình quản lý **HOẶC** `created_by` = mình |
| Không có quyền nào | `created_by` = mình |

Cộng thêm 2 điều kiện luôn đúng với `type = all`:
- Phiếu **status 3 (Không duyệt)** chỉ người lập ra nó mới thấy.
- Dòng cuối hàm: `->where('company_id', công ty mình)` — **đè lên cả nhánh "tổng công ty"**, nên
  trên thực tế ngay cả người có quyền tổng công ty cũng chỉ thấy phiếu công ty mình. Giữ nguyên
  hành vi (ghi rõ ở đây để sau này không ai tưởng là thiếu dữ liệu như vụ `accountingExpiringBorrow`).

Với `type = for-approve`: gom các phiếu ĐẾN LƯỢT MÌNH duyệt — status 2 nếu là Kế toán kho, status 4
nếu là TP (bó theo phòng quản lý), status 5 nếu là BGĐ; ai không có quyền nào thì chỉ thấy phiếu
mình lập. Lưu ý ERP viết bằng `orWhere` nối tiếp — port sang phải bọc thành một nhóm `where(fn)`
để không rò rỉ phiếu khi kết hợp với các bộ lọc khác.

## 7. Cột bảng và bộ lọc (giữ đúng ERP)

Cột: STT · Mã phiếu · Phiếu mượn · Người lập · Ngày lập · Ngày hẹn trả cũ · Ngày hẹn trả mới ·
Trạng thái · Người duyệt · Ngày duyệt · Hành động.

Bộ lọc: Mã phiếu · Tên hàng · Tên model · Phiếu mượn · Trạng thái · Người duyệt · Người lập ·
khoảng ngày lập · khối Công ty – Phòng ban (hiện theo quyền phạm vi).

Ô lọc "Trạng thái" của ERP chỉ liệt kê 3 giá trị (Đã duyệt / Chờ duyệt / Không duyệt) trong khi dữ
liệu có 5 → chọn "Chờ duyệt" chỉ ra đúng status 2, bỏ sót phiếu chờ TP và chờ BGĐ. **HRM liệt kê
đủ 5 trạng thái** (xem mục 9, lỗi ERP #5).

## 8. Phần MỚI so với ERP (user chốt 24/09/2026)

1. **Bản in** — ERP màn này chỉ có xuất Excel, không có bản in. HRM bổ sung bản in phiếu và in
   danh sách theo đúng cách màn `prepick-extend-requests` đang làm: blade riêng trong
   `Modules/Finance/Resources/views/prints/`, KHÔNG dùng `report_templates` của ERP.
2. **Bảng lịch sử thay đổi** — ERP không có. Thêm bảng MỚI `borrow_extend_request_history` theo
   đúng khuôn `prepick_extend_request_history` (migration `2026_08_22_000001`) và skill
   `.claude/skills/entity-history` mục 2 (subset-diff, lưu sẵn giá trị hiển thị, không khoá ngoại
   cứng, không SoftDeletes, tên index đặt tay tránh lỗi 1059).
   **Bảng nghiệp vụ `borrow_extend_requests` giữ nguyên schema — không đụng.**
   Hệ quả phải ghi lên màn: phiếu được duyệt bên cổng ERP sẽ KHÔNG có mặt trong lịch sử HRM.
3. **Chặn quá hạn khi TP duyệt** — ERP gắn middleware `checkDueConfigsManager:Duyệt gia hạn hàng
   mượn` lên route duyệt. Bản ghi `due_configs` id=25, tab=2 **đã có sẵn** trong `gop_db`, và HRM
   đã có middleware tương đương `dueConfig:<tên>,manager` (đang dùng ở 2 màn khác). Chỉ cần gắn.

## 9. Lỗi ERP phát hiện khi đọc mã — HRM SỬA, ERP để nguyên

> Cập nhật 24/09: thêm #6-#9 phát hiện lúc viết Phase 2. #6 là **lỗ phân quyền thật**, đã đo được.

User chốt 24/09/2026: sửa hết bên HRM, ghi rõ phần lệch để quyết sau có vá ERP không.

| # | Lỗi ERP | Vị trí | HRM làm gì |
| --- | --- | --- | --- |
| 1 | Modal "Tạo mới" chọn phiếu mượn chỉ lọc `status=5, borrow_status=2, export_type=3`, **không lọc `created_by` = mình**, trong khi `can_borrow_extend` lại bắt buộc → chọn xong bấm Gửi mới báo "Không thể gia hạn yêu cầu này!" | `create.blade.php` (modal) vs `ProductExportRequest::getCanBorrowExtendAttribute()` | Endpoint chọn phiếu lọc luôn theo người lập + loại trừ phiếu đang có yêu cầu gia hạn chưa chốt, để danh sách hiện ra là danh sách chọn được |
| 2 | Lưu đính kèm: `$results[] = $object->attachments;` với object MỚI (null) → chuỗi lưu bị **thừa dấu phân cách cuối** | `BorrowExtendRequestController::store()` dòng ~203 | Dùng `V2BaseAttachmentSection` + lưu mảng đã lọc rỗng |
| 3 | `new_return_date` lưu thô `Y-m-d` ở `store()` nhưng `approve()` lại `createFromFormat('d/m/Y', …)` → hai định dạng cùng một cột | `store()` ~194 vs `approve()` ~303 | Chuẩn hoá một định dạng ở tầng Request, service chỉ nhận `Y-m-d` |
| 4 | Chặn vượt `configs.max_borrow_date` so sánh **chuỗi với đối tượng Carbon** (`$request->new_return_date > $max_borrow`) — chạy đúng chỉ nhờ may mắn về thứ tự chữ của `Y-m-d` | `store()` ~173 | So sánh bằng Carbon thật, thông báo giữ nguyên câu chữ |
| 5 | Ô lọc Trạng thái thiếu 2 giá trị (chờ TP, chờ BGĐ) — xem mục 7 | `index.blade.php` `search_columns` | Liệt kê đủ 5 |
| 6 | **LỖ PHÂN QUYỀN**: `index()` mặc định `type = 'index'`, mà `searchByFilter()` không có nhánh cho `index` ⇒ vào bằng URL trần thì người không có quyền xem nào vẫn thấy TOÀN BỘ phiếu của công ty (đo trên `gop_db`: **1.210 thay vì 18**) | `BorrowExtendRequestController::index()` + `searchByFilter()` :62-112 | Mọi `type` lạ (và không truyền) đều coi là `all` ⇒ luôn qua `applyViewScope()` |
| 7 | `canView()` cho `Kế toán kho` và `Ban giám đốc duyệt hàng mượn` xem phiếu **mọi công ty**; và **không xét 3 quyền xem theo cấp** nên người có quyền xem bấm vào phiếu ra `not_found` | `BorrowExtendRequest::canView()` :173-185 | Siết cùng công ty + bổ sung 3 nhánh quyền cấp, khớp 1-1 `applyViewScope()` |
| 8 | `canTPApprove()` không so công ty ⇒ TP công ty A duyệt được phiếu công ty B khi trùng `department_id` | `BorrowExtendRequest::canTPApprove()` :195-200 | Siết thêm cùng công ty (khớp 2 cấp còn lại) |
| 9 | Bộ lọc Tên hàng / Model dò trên MỌI dòng chi tiết, kể cả dòng `need_export = 0` ⇒ lọc ra được phiếu mà bảng chi tiết trên màn không hề hiện mặt hàng vừa tìm | `searchByFilter()` :130-144 | Lọc đúng tập dòng đang hiển thị (`need_export = 1`) |

Lỗi #1 ở ERP còn kéo theo luật: `can_borrow_extend` chặn tạo phiếu thứ hai khi phiếu cũ chưa chốt
(`whereNotIn('status', [1,3])`) — giữ nguyên luật này, chỉ đổi chỗ kiểm tra cho sớm hơn.

## 10. Khuôn mẫu để bám — màn sinh đôi đã port

`prepick-extend-requests` (Yêu cầu gia hạn hàng giữ) là bản tham chiếu gần nhất:

| Lớp | File HRM đã có | Ghi chú khi bám theo |
| --- | --- | --- |
| Service | `Services/PrepickExtendRequestService.php` (1.103 dòng) | Bám khung `searchByFilter/meta/store/approve/reject/renderPrint/exportData`; **bỏ** phần nháp, sửa, xoá, `stock`, `inStock` |
| Lịch sử | `Services/PrepickExtendRequestHistoryService.php` (417 dòng) | Bám gần như nguyên vẹn |
| Controller | `Http/Controllers/V1/PrepickExtendRequestController.php` | Bỏ `update`, `destroy`, `stock`, `inStock` |
| FE danh sách | `pages/finance/prepick-extend-requests/index.vue` (831 dòng) | |
| FE form | `components/PrepickExtendRequestForm.vue` (1.397 dòng) | Màn mượn ĐƠN GIẢN HƠN NHIỀU: không nhập theo dòng, chỉ 1 ô ngày hẹn trả mới cho cả phiếu |

Ước lượng: màn mượn nhẹ hơn hẳn vì không có chi tiết nhập tay, không nháp/sửa/xoá.

## 11. KHÔNG đụng vào

- Schema 2 bảng ERP `borrow_extend_requests`, `product_export_requests`.
- Model dùng chung `ProductExportRequest` phía HRM — nếu cần thêm quan hệ phải **hỏi user trước**.
- Cổng ERP: 5 lỗi ở mục 9 chỉ ghi lại, không tự vá.
