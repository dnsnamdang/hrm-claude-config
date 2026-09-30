# Sắp xếp danh sách khách hàng ô chọn — Phiếu đề xuất cung ứng

**Người phụ trách:** @khoipv
**Ngày bắt đầu:** 22/09/2026

## Hiện tượng

Ô chọn Khách hàng ở màn `supply/supply_proposals/add` hiện thứ tự khác nhau giữa 2 loại đề xuất:
- Loại 1 (Cung ứng cho KH): lộn xộn, không theo A→Z
- Loại 3 (Cung ứng khách lẻ): đúng A→Z

## Nguyên nhân

`SupplyProposalService::customers($type)` có 2 nhánh lấy từ 2 bảng khác nhau:

| | Type 1 | Type 3 |
|---|---|---|
| Nguồn | `contracts` (HĐ đã duyệt) | `category_customers` |
| Sắp xếp | **không có `ORDER BY`** → MySQL trả theo thứ tự lưu trữ (xấp xỉ `contracts.id`) | `orderBy('name')` |
| Tên hiển thị | `contracts.customer_name` (bản chụp lúc lập HĐ) | `category_customers.name` |

Verify trên `thanhan_stag_07052026`: type 1 = 120 KH thứ tự lộn xộn, type 3 = 801 KH đúng A→Z.

## Quyết định

**User chốt phương án 1 (22/09/2026), sau đó làm luôn phương án 2 trong cùng ngày:**
1. Thêm sắp xếp A→Z cho nhánh type 1.
2. Đổi nguồn tên hiển thị của nhánh type 1 sang danh mục `category_customers.name` để cùng 1 khách
   không ra 2 tên khác nhau giữa loại 1 và loại 3.

- Màn Kết xuất hợp đồng (`supply/contract_render`) cũng gọi endpoint này (không truyền `type`) → đổi
  cả thứ tự lẫn text hiển thị. Lọc ở màn đó chạy theo `customer_id` (`index.vue:34`) nên không ảnh hưởng.
- `leftJoin` + `COALESCE(NULLIF(TRIM(cc.name), ''), contracts.customer_name)`: KH đã bị xóa khỏi danh
  mục vẫn còn tên từ bản chụp trên HĐ (stag hiện 0 ca, nhưng phòng prod).
- **KHÔNG lọc `status` / `is_customer`** ở nhánh type 1: khách đã có HĐ duyệt phải chọn được kể cả khi
  danh mục đã ngừng hoạt động (stag có 1 ca: id 3169 CÔNG TY CP BỆNH VIỆN MẮT HÀ NỘI - BẮC NINH).
- `orderByRaw` thay vì `orderBy('customer_name')` để tránh nhập nhằng giữa alias và cột gốc `contracts.customer_name`.
- Dùng `orderBy('customer_name')` ở tầng SQL (không `sortBy` ở PHP) vì `contracts.customer_name` và
  `category_customers.name` cùng collation `utf8mb4_unicode_ci` → thứ tự 2 loại khớp nhau, chuẩn
  tiếng Việt có dấu, không phân biệt hoa/thường.

**Đã xử lý (phương án 2):** 4 khách trước đây hiện tên cũ theo bản chụp HĐ nay lấy tên danh mục —
id 2860, 1992, 1594 và 2863 (HĐ ghi "BỆNH VIỆN ĐA KHOA TRUNG ƯƠNG QUẢNG NAM" → danh mục
"Bệnh viện Việt - Hàn Đà Nẵng").

## Task

### BE — `Modules/Supply/Services/SupplyProposalService.php`
- [x] Thêm sắp xếp A→Z vào nhánh HĐ của `customers()` (`orderByRaw`)
- [x] `leftJoin category_customers` + `COALESCE` lấy tên từ danh mục (phương án 2)
- [x] Cập nhật comment docblock ghi rõ 2 nhánh đều sắp xếp A→Z

### Verify
- [x] `php -l` sạch
- [x] Tinker: type 1 ra đúng A→Z (BỆNH VIỆN 19-8 → 199 → A → BÃI CHÁY → BẢO VỆ → C → CHUYÊN KHOA MẮT…), vẫn 120 KH, 0 id trùng
- [x] Regression: gọi `customers(null)` (đường của `contract_render`) vẫn ra 120 KH, chỉ đổi thứ tự
- [ ] @khoipv test UI 2 loại đề xuất

## Không đụng

- Nhánh type 3 (`category_customers`) — đã đúng
- `contracts.customer_name` trong DB (chỉ đổi cách hiển thị ở ô chọn, không sửa dữ liệu HĐ)
- FE `add.vue`, `contract_render/index.vue`
- Các màn khác đọc `contracts.customer_name` (báo cáo, in ấn…) — vẫn dùng bản chụp như cũ

### Checkpoint — 22/09/2026
Vừa hoàn thành: thêm `->orderBy('customer_name')` vào nhánh HĐ của `SupplyProposalService::customers()`
+ bổ sung comment docblock. `php -l` sạch; tinker: type 1 = 120 KH đúng A→Z, 0 id trùng; `customers(null)`
(màn kết xuất HĐ) vẫn 120 KH, chỉ đổi thứ tự, text hiển thị không đổi.
Đang làm dở: không có — code-complete, chỉ sửa BE nên không cần build lại client.
Bước tiếp theo: @khoipv test UI ô chọn Khách hàng ở 2 loại đề xuất + soát nhanh màn `supply/contract_render`.
Blocked: không có.

### Checkpoint — 22/09/2026 (làm tiếp phương án 2)
Vừa hoàn thành: nhánh type 1 của `customers()` chuyển sang `leftJoin category_customers` +
`COALESCE(NULLIF(TRIM(cc.name), ''), contracts.customer_name)`, sắp xếp bằng `orderByRaw` cùng biểu thức.
Verify tinker: type 1 = 120 KH, 0 id trùng, **0 khách lệch tên so với type 3** (trước là 4);
4 khách đổi tên đúng như danh mục; KH id 3169 ngừng hoạt động vẫn còn trong type 1 (đúng ý đồ);
`customers(null)` (màn kết xuất HĐ) vẫn 120 KH, lọc theo `customer_id` nên không ảnh hưởng.
Đang làm dở: không có — code-complete, chỉ sửa BE.
Bước tiếp theo: @khoipv reload và test UI 2 loại đề xuất + màn `supply/contract_render`.
Blocked: không có.
