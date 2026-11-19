# Design — Chặn khóa hàng hóa khi còn phiếu dở trong luồng mua / nhập / xuất

Feature: `khoa-hang-chan-tien-trinh`
Ngày: 2026-10-29
Nơi làm: **HRM** (hrm-api + hrm-client). DM hàng hóa đã chuyển từ ERP sang HRM.

---

## 1. Mục tiêu & lý do (why)

Ở DM hàng hóa (HRM), "Khóa hàng" = **ngừng kinh doanh mặt hàng, không cho phát sinh giao dịch
mới**. Nếu khóa trong khi mặt hàng vẫn đang nằm trong một chứng từ chưa xong, chứng từ đó sẽ mắc kẹt
(không hoàn tất được giao dịch đang dở). Vì vậy: **không cho khóa khi mặt hàng còn bất kỳ phiếu dở
nào** trong 3 luồng Mua / Nhập / Xuất. Khi bị chặn, hiện **một popup liệt kê đúng những phiếu đang
giữ** để người dùng biết phải xử lý/hủy phiếu nào trước rồi mới khóa được.

## 2. Goals / Non-goals / Anti-goals

**Goals**
- Chặn thao tác **Khóa** một mặt hàng khi mặt hàng đó còn phiếu dở ở luồng Mua, Nhập, hoặc Xuất.
- Popup liệt kê các phiếu đang giữ, **gom nhóm theo luồng** (Mua / Nhập / Xuất), mỗi dòng:
  **mã phiếu (ấn vào mở màn xem phiếu)**, **người tạo**, **ngày tạo**.
- Mã phiếu trỏ **đúng nơi phiếu xem được**: phiếu có màn HRM → mở trong HRM; phiếu chỉ có bên ERP
  → mở sang ERP (tab mới).

**Non-goals**
- KHÔNG đụng thao tác **Xóa** (đã có `ProductUsageGuard` riêng) và **Khôi phục/Mở khóa**.
- KHÔNG đổi ngữ nghĩa khóa (vẫn là set `product_company_coefficients.status = 4` theo công ty).
- KHÔNG làm khóa hàng loạt (hiện khóa vốn chỉ từng mặt hàng — giữ nguyên).

**Anti-goals** (coi là thất bại dù chạy được)
- Chặn nhầm vì tính cả phiếu đã **Hủy** hoặc đã **Hoàn thành/Kết thúc** → người dùng không bao giờ
  khóa được dù thực tế không còn gì dở.
- Chặn theo **sai công ty**: khóa hàng cho công ty A nhưng lại chặn vì phiếu dở của công ty B.

## 3. Quyết định đã chốt (user đã duyệt trong brainstorm)

1. **Định nghĩa "đang trong tiến trình" (dở):** tồn tại ≥1 phiếu có dòng chi tiết chứa `product_id`
   này, mà phiếu đó **CHƯA Hủy và CHƯA Hoàn thành/Kết thúc**. → **Tính luôn cả phiếu "Đang tạo"
   (nháp)**. Chỉ phiếu đã Hủy hoặc đã Hoàn thành mới KHÔNG chặn.
2. **Phạm vi công ty:** vì khóa là **khóa theo công ty** (set status của riêng công ty đang đăng
   nhập), nên **chỉ xét phiếu thuộc công ty đang đăng nhập**. Phiếu dở của công ty khác không chặn.
3. **Chỉ chặn Khóa.** Xóa/Mở khóa/Khôi phục giữ nguyên.
4. **Hiển thị = popup danh sách** (KHÔNG phải toast 1 câu). Gom nhóm theo luồng, có mã phiếu bấm
   được, người tạo, ngày tạo.
5. **Link mã phiếu trỏ về đúng nơi phiếu thực sự xem được** (HRM nếu đã có màn, ngược lại ERP tab mới).
6. **Chỗ cài chốt chặn:** trong `ProductLifecycleService::lock()` (hrm-api), sau các check hiện có
   (quyền → đang KD → chưa khóa), trước khi `setStatus(...STATUS_STOPPED)`.
7. **Đọc bảng phiếu ERP:** HRM & ERP **chung connection `mysql` mặc định** → guard dùng `DB::table(...)`
   trực tiếp, không cần cấu hình connection mới.
8. **Xét "dở" theo DÒNG của chính mặt hàng** (không phải theo cả phiếu). Chặn chỉ khi **dòng của đúng
   mặt hàng đang khóa** còn dở, dùng tín hiệu "còn dở" theo dòng sẵn có từng luồng (YCXH `need_export`,
   YCNH `need_import`, HĐ `qty − arrived_qty − arriving_qty > 0`…). Nơi nào không có tín hiệu theo
   dòng → fallback xét theo phiếu cho dòng đó. (Tránh chặn oan vì mặt hàng KHÁC trên cùng phiếu.)
9. **CÓ tính mặt hàng xuất hiện GIÁN TIẾP** (thành phần công thức/combo/phụ kiện/"đặt mã lẻ" của một
   dòng khác). Builder **dùng lại bản đồ vị trí của `ProductUsageGuard`** (nơi liệt kê các bảng
   combo/recipe/phụ kiện) rồi áp thêm bộ lọc "phiếu còn mở" + theo dòng — không phát minh lại.
10. **Chặn cả nháp của NGƯỜI KHÁC** (giữ nguyên "chặn hết"). Dead-end được popup giải quyết: popup
    hiện người tạo + ngày tạo để người dùng biết liên hệ ai nhờ hủy. Không lọc theo người tạo.

## 4. Kiến trúc & luồng

```
FE DM hàng hóa  --(PUT products/{id}/lock)-->  ProductLifecycleController@lock
                                                   -> ProductLifecycleService::lock()
                                                        [guard mới: ProductInProgressGuard]
                                                        - đếm/liệt kê phiếu dở theo product_id + company_id
                                                        - có phiếu dở => throw 422 { message, blocking_documents }
                                                        - không => setStatus(STATUS_STOPPED) như cũ
FE: bắt 422 có 'blocking_documents' => mở modal danh sách (thay vì toast)
```

### 4.1 Backend (hrm-api)

- **Guard mới** (gợi ý: `Modules/MasterData/Services/Product/ProductInProgressGuard.php`), được
  `ProductLifecycleService::lock()` gọi. Trả về cấu trúc:
  ```php
  // rỗng => cho khóa; có phần tử => chặn
  [
    'purchase' => [ ['code'=>'DH-123', 'created_by_name'=>'Nguyễn A', 'created_at'=>'2026-10-20',
                     'url'=>'https://erp.eteksofts.com/admin/.../123', 'target'=>'erp'], ... ],
    'import'   => [ ... 'target'=>'hrm', 'url'=>'/master-data/.../456' ... ],
    'export'   => [ ... ],
  ]
  ```
- **Chặn & response:** nếu có phần tử → `throw new HttpResponseException(response()->json([
  'message' => 'Không thể khóa: hàng hóa đang trong tiến trình.',
  'blocking_documents' => $groups ], 422))`. (Cùng pattern `fail()` hiện có, chỉ thêm khóa
  `blocking_documents`.)
- **Mỗi luồng = một tập bảng.** Với mỗi bảng: JOIN cha↔chi tiết theo `parent_id`, lọc
  `detail.product_id = ?`, `header.company_id = ?` (công ty đang đăng nhập), và **loại trừ các
  trạng thái kết thúc** (Hủy + Hoàn thành). Lấy `code`, người tạo (join `created_by` → tên), `created_at`.
- **Người tạo:** nhiều bảng ERP chỉ lưu `created_by` (id). Join sang bảng nhân viên/`users` để ra
  tên hiển thị (theo cách các service HRM hiện có đang làm — builder dùng lại helper sẵn có).

### 4.2 Frontend (hrm-client)

- Hook ở `utils/productLifecycle.js` (nơi tập trung lock/delete/restore). Trong nhánh `catch` của
  lock (hiện 422/423 chỉ toast `message`): **nếu response 422 có `blocking_documents`** → KHÔNG toast,
  mà mở **modal mới** `ProductInProgressModal.vue` truyền `blocking_documents`.
- **Modal** (bám chuẩn modal/list-page của dự án — xem skill `modal-popup`, `list-page`,
  `button-convention`): tiêu đề "Hàng hóa đang trong tiến trình — chưa thể khóa"; 3 khối nhóm
  **Luồng mua / Luồng nhập / Luồng xuất**, nhóm nào rỗng thì ẩn. Mỗi khối là bảng: Mã phiếu |
  Người tạo | Ngày tạo. Mã phiếu là link: `target='hrm'` → `<nuxt-link>`/router nội bộ; `target='erp'`
  → `<a :href target="_blank">`.
- Chỗ gọi khóa: nút trong `ProductListPage.vue` (dòng danh sách) và footer `_id/index.vue` (màn chi
  tiết) đều đi qua `productLifecycle.js` nên chỉ sửa một chỗ tập trung + thêm modal.

## 5. Bản đồ luồng → bảng → trạng thái loại trừ (builder PHẢI xác minh lại từ Model)

> ⚠️ Các hằng trạng thái dưới đây lấy từ rà soát nhanh (recon) các Model ERP. Trước khi code,
> builder **mở từng Model đọc lại hằng `const STATUS_*` / cột cờ hoàn thành** để chốt chính xác —
> KHÔNG hardcode theo trí nhớ. Quy tắc chung: **block = (không thuộc tập Hủy) AND (không thuộc tập
> Hoàn thành/không bật cờ hoàn thành)**; nháp/Đang tạo coi là dở (block).

### Luồng MUA → "Hàng đang trong tiến trình mua"
| Phiếu | Bảng cha | Chi tiết (có product_id) | Loại trừ (Hủy + Hoàn thành) — cần xác minh |
|---|---|---|---|
| YC đặt hàng gốc | `root_order_requests` | chi tiết theo parent_id | done=4, cancel=5 → trừ {4,5} |
| Đơn đặt hàng | `order_requests` / `order_request2` | details | done={1,4}, cancel=0 → trừ {0,1,4} |
| Hóa đơn mua (ngoài/trong) | `purchase_invoices` / `inland_purchase_invoices` | details | done=1, cancel=4 → trừ {1,4} |
| HĐ mua (ngoài/trong) | `buy_contract2` / `inland_buy_contract_new` | details | cancel=0; "Hoàn thành" = đã giao đủ (xem ghi chú HĐ) |
| Hóa đơn | `invoice2` | details | done={1,5}, cancel=7 → trừ {1,5,7} |

> **Ghi chú HĐ mua:** với hợp đồng, `status=1` thường là **đang hiệu lực/đã duyệt**, KHÔNG phải
> "đã xong" — HĐ còn dòng chưa giao đủ (`qty - arrived_qty - arriving_qty > 0`) vẫn là **dở → block**.
> Builder xác minh ERP đánh dấu HĐ "hoàn thành" bằng gì (trạng thái riêng, hay suy ra từ đã giao đủ),
> và chỉ loại trừ khi thật sự đã xong/đã hủy.

### Luồng NHẬP → "Hàng đang trong tiến trình nhập"
| Phiếu | Bảng cha | Chi tiết | Loại trừ — cần xác minh |
|---|---|---|---|
| YC nhập kho (YCNH) | `product_import_requests` | `product_import_request_details` (parent_id) | cờ `is_complete`; done={5,8}, cancel={6,0}. block = `is_complete=0` AND status ∉ {5,8,6,0} |
| Đề nghị nhập kho (ĐNNK) | `warehouse_import_requests` | details | in-progress {3,2}; cancel 0; done = có `change_stock_time` |
| Phiếu nhập kho (PNK) | `product_imports` | details (parent_id) | 3=nháp, 1=done → block {3, các trạng thái ∉ done/cancel} |
| Order import | `order_import_requests` | details | in-progress {3,2}, done=1, cancel=6 → trừ {1,6} |

### Luồng XUẤT → "Hàng đang trong tiến trình xuất"
| Phiếu | Bảng cha | Chi tiết | Loại trừ — cần xác minh |
|---|---|---|---|
| YC xuất hàng (YCXH) | `product_export_requests` | `product_export_request_details` | cờ `is_completed`; cancel=6, done=5. block = `is_completed=0` AND status ∉ {5,6} |
| Đề nghị xuất kho (ĐNXK) | `warehouse_export_requests` | details | cờ `is_complete` (khác tên!); 3=nháp; 5=done/cancel. block = `is_complete=0` AND status ∉ {3→vẫn block, 5} |
| Phiếu xuất kho (PXK) | `product_exports` | `product_export_details` (parent_id) | 3=nháp; không có cờ hoàn thành rõ — builder xác định điều kiện "đã xong" (trạng thái thanh toán/quyết toán) |
| YC xuất bán/mượn | `borrow_sell_requests` | `borrow_sell_request_products` (parent_id) | in-progress {2,3,10,11}; một số suy ra qua `ProductImportRequest.is_complete=false` liên quan |

> **Cảnh báo tên cột:** YCXH dùng `is_completed`, ĐNXK dùng `is_complete` — KHÁC NHAU. Giá trị
> "Hủy" cũng khác nhau giữa các model (0/4/5/6). Phải đọc đúng từng Model.

## 6. Bản đồ "loại phiếu → URL xem phiếu" (builder lập đầy đủ)

Mỗi phần tử trong `blocking_documents` kèm `target` ('hrm' | 'erp') và `url`:
- **Phiếu đã có màn HRM** (vd YCXH, ĐNXK, YCNH, ĐNNK, PNK, PXK đã port…): `target='hrm'`, url là
  route nội bộ HRM tương ứng. Builder kiểm màn nào đã có trong hrm-client trước khi gán HRM.
- **Phiếu chỉ có bên ERP** (HĐ mua, đơn đặt hàng, hóa đơn mua, invoice2…): `target='erp'`, url =
  `{ERP_BASE_URL}/admin/.../{id}` mở tab mới. Lấy base URL ERP từ config/env đang dùng (không
  hardcode domain). Builder lập bảng ánh xạ rõ ràng từng loại phiếu.

## 7. Ràng buộc & lưu ý

- ERP là Laravel 6; nhưng guard nằm ở **hrm-api (Laravel 8)** truy vấn bảng ERP qua `mysql` → dùng
  query builder thuần, không phụ thuộc model ERP.
- Hiệu năng: khóa là thao tác đơn lẻ từng mặt hàng → ~1 truy vấn/bảng là chấp nhận được. Nên dùng
  `EXISTS` để quyết định chặn, rồi chỉ `SELECT` chi tiết các bảng thực sự có phiếu dở (để dựng popup).
- Giới hạn danh sách: nếu một nhóm quá nhiều phiếu, cân nhắc cap (vd 50/nhóm) + dòng "và N phiếu
  khác" — builder tự quyết con số hợp lý, ghi vào plan.
- Quyền xem phiếu đích: link có thể dẫn tới phiếu người dùng không có quyền (nhất là sang ERP) →
  chấp nhận (ERP tự chặn), không xử lý thêm ở feature này.
- Bám chuẩn dự án: skill `modal-popup`, `list-page`, `button-convention`, `notification-convention`.
- **Cột "công ty của phiếu" KHÁC nhau giữa các bảng** (reviewer xác nhận `header.company_id` KHÔNG
  phổ quát): nhiều bảng ERP không có `company_id`, `product_export_requests` dùng `export_company_id`,
  `product_exports` suy từ người tạo → `info.company_id`, nhiều luồng lấy từ `auth()->user()->info->company_id`.
  → Builder **xác định biểu thức "công ty của phiếu" cho TỪNG bảng**, và bảo đảm nó **cùng hệ id** với
  công ty hiện tại mà lock dùng (`ProductLifecycleService::companyId` = `current_company_role`). Đây là
  điểm dễ sai dẫn tới Anti-goal #2 (chặn sai công ty) — phải kiểm từng bảng, không dùng chung một cột.
- **Xóa mềm:** guard dùng `DB::table()` thuần → KHÔNG tự áp global scope `deleted_at`. Builder phải
  `whereNull('deleted_at')` cho mọi bảng có soft delete, nếu không phiếu đã xóa mềm vẫn bị đếm → chặn nhầm.

## 8. Phần để builder tự quyết / xác minh (tổng hợp)
- Xác minh lại **toàn bộ hằng trạng thái & cờ hoàn thành** từng Model ERP ở mục 5.
- Chốt **điều kiện "đã xong"** cho HĐ mua và PXK (chưa có cờ rõ).
- Lập đầy đủ **bản đồ loại phiếu → (target, url)** ở mục 6; kiểm màn HRM nào đã tồn tại.
- Con số cap danh sách mỗi nhóm (mục 7).
- Tên/đường dẫn file cụ thể của guard và modal (gợi ý ở mục 4).

## 9. Câu hỏi còn mở cho user — ĐÃ CHỐT (2026-10-29)

Cả 3 câu builder-check đã được user duyệt, nay nằm ở mục 3 (quyết định 8, 9, 10):
1. Xét "dở" **theo DÒNG** của chính mặt hàng (→ quyết định 8).
2. **CÓ** tính mặt hàng gián tiếp (combo/công thức/phụ kiện), dùng lại bản đồ `ProductUsageGuard`
   (→ quyết định 9).
3. **Chặn cả nháp người khác**, popup hiện người tạo để biết liên hệ (→ quyết định 10).

Thiết kế đã đủ để lập plan.
