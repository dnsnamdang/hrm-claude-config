# Plan — Điều chuyển chi nhánh over-commit pool hàng giữ

Xem `design.md`. **Hướng đã đảo:** điều chuyển chi nhánh xuất-từ-giữ là ĐÚNG; lỗi thật = cơ chế
pending không quy đúng "người giữ" (dùng `pr.created_by` nguồn thay vì `product_transfer_requests.
created_by`) nên 2 phiếu cùng người giữ over-commit pool giữ. Không vá dữ liệu.

## Phase 0 — Điều tra & hiểu đúng nghiệp vụ
- [x] Xác nhận cả PXK-34072 & PXK-34214 là type 7 (điều chuyển chi nhánh)
- [x] Xác nhận người giữ = `product_transfer_requests.created_by = 263` (cty đích 4), khác
      `pr.created_by = 1119` (cty nguồn 1)
- [x] Hiểu đúng: giữ gắn khách = giữ cho kinh doanh; điều chuyển kéo giữ của chính người YC là đúng
- [x] Chốt: KHÔNG vá dữ liệu (trạng thái hiện tại là phân bổ đúng); Model A bị loại
- [x] Viết lại design.md theo hướng đúng
- [ ] **User duyệt hướng B (sửa pending)** ← ĐANG CHỜ

## Phase 1 — Sửa cơ chế pending (ĐÃ DUYỆT & CODE)
- [x] Đọc kỹ `getAccountingStockDetail` 2 block pending: `pending_prepicks` (~2470) và
      `total_pending_products` (~2512-2569) — xác định chỗ nào phụ thuộc `pr.created_by`
- [x] B1: `pending_prepicks` (`app/Product.php:2470`) — thay `where('pr.created_by',$employee_id)`
      bằng type-split khớp người giữ: `(type!=7 AND pr.created_by=$emp) OR (type=7 AND pr.id IN
      (SELECT product_export_request_id FROM product_transfer_requests WHERE created_by=$emp))`.
      Dùng **subquery-in-WHERE** (KHÔNG LEFT JOIN pt) để không nhân dòng khi 1 PER nhiều TR.
      Bám đúng khuôn có sẵn `import_direct_pending_1/2` (2579-2607).
- [x] B2: rà `total_pending_products` (2512+) — **KHÔNG cần sửa**: nó trừ pending toàn công ty khỏi
      tổng công ty (in_stock free-stock), độc lập người giữ → không dính bug.
- [x] Phần dư (đòi > giữ) tự rớt sang tồn ở `WarehouseExportRequest::updateWarehouse` — GIỮ NGUYÊN,
      cơ chế đã đúng, chỉ cần pending trả `prepick_qty` đúng.
- [x] `php -l` sạch; `ExportModel` đã import (:94)
- [x] Verify SQL (toSql read-only): WHERE đúng type-split, bindings `[7,263,7,263,...]`
- [x] Verify prod read-only: subquery(holder 263) bắt đúng cả PER 39922+40081 (code cũ bắt trượt vì
      pr.created_by=1119) → xác nhận đúng nguồn bug
- [ ] (khi có màn test) bấm thật 2 phiếu điều chuyển cùng người giữ tổng > giữ → phiếu sau tự trừ
      pending, không kẹt "xuất nhiều hơn prepick"; hồi quy xuất thường không đổi

## Không làm
- KHÔNG đụng logic customer-blind (sum tồn giữ theo employee_id, trừ giữ trong ProductExport) — đúng
- KHÔNG vá dữ liệu prod PXK-34072/34214 — đã đúng
- KHÔNG đổi default `getAccountingStockDetail` cho caller khác (fix chỉ cộng thêm, an toàn)

## Phase 2 — Hủy giữ kế toán không thấy pending điều chuyển (cùng họ, path khác)
Phát hiện khi user hỏi: màn hủy giữ kế toán (`AccountingPrepickCancelController@store` →
`AccountingPrepickCancel::validateProducts` → `Product::getAccountingStockDetail`) KHÔNG có hard-block;
chỉ chặn gián tiếp qua `prepick_qty` khả dụng (ignore_pending mặc định false → có trừ pending).
- [x] Xác định lỗ: `validateProducts` truyền `customer_id` cụ thể → nhánh `pending_prepicks` lọc
      `pr.customer_id = $customer_id`. Nhưng PER type 7 LUÔN `customer_id = NULL` (verify prod:
      2168/2168) → pending điều chuyển bị loại sạch → kế toán hủy nhầm phần giữ điều chuyển đã đặt
      trước → phiếu điều chuyển chốt xuất kẹt "Xuất nhiều hơn lượng prepick".
- [x] Bản chất khác Phase 1: Phase 1 = holder attribution (path customer_id=NULL); Phase 2 = filter
      customer loại type 7 (path customer_id cụ thể). Fix Phase 1 KHÔNG đóng lỗ này.
- [x] Fix (hướng 1, user chốt): nới filter customer trong `pending_prepicks` (`Product.php:2498`)
      thành `(pr.customer_id = $customer_id OR pr.type = 7)` — điều chuyển customer-blind nên pending
      của holder phải trừ bất kể khách.
- [x] `php -l` sạch; verify SQL: customer clause `(pr.customer_id = ? or pr.type = ?)` bindings `[...,17590,7]`
- [x] Đối chiếu regression: path tạo phiếu xuất/điều chuyển (customer_id=NULL) KHÔNG đụng block
      `if(!empty($customer_id))` → không đổi. Path xuất thường có customer: nay cũng trừ pending
      điều chuyển customer-blind của cùng holder → ĐÚNG (pool giữ bị điều chuyển tranh chấp), không
      phải regression mà là mở rộng đúng.
- [ ] (khi có luồng test) tạo pending phiếu điều chuyển giữ pool → thử hủy giữ kế toán cùng holder
      → phải bị chặn phần đã đặt trước

### Checkpoint — 2026-09-16 (3)
Vừa hoàn thành: Phase 1 (holder attribution, `Product.php:2481`) + Phase 2 (nới filter customer cho
type 7, `Product.php:2498`) — cùng block `pending_prepicks`. 2 edit, `php -l` sạch, verify SQL cả 2
path (customer_id=NULL và customer cụ thể), verify prod read-only holder mapping + customer NULL 2168/2168.
Đang làm dở: — (chỉ còn test bấm thật; chưa vá dữ liệu, đúng chủ trương)
Bước tiếp theo: user review diff; theo dõi ca điều chuyển đôi + ca hủy giữ khi có phiếu điều chuyển treo
Blocked: (trống)
