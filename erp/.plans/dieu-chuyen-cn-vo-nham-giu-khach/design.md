# Điều chuyển kho chi nhánh: 2 phiếu over-commit cùng một pool hàng giữ

> ⚠️ Bản design này ĐÃ ĐẢO HƯỚNG so với draft đầu. Draft đầu ("Model A: điều chuyển không được
> dùng giữ") **SAI vì hiểu sai nghiệp vụ**. Xem mục "Hiểu đúng nghiệp vụ".

## Hiểu đúng nghiệp vụ (user chốt 2026-09-16)

- **Hàng giữ gắn khách = giữ cho KINH DOANH**, định danh bằng `prepick_details.employee_id`.
  `customer_id` chỉ cho biết hàng này thuộc đơn nào — bản chất là giữ cho người kinh doanh đó.
  Người kinh doanh **sở hữu toàn bộ phần giữ của mình**, bất kể của khách nào.
- **Xuất điều chuyển kho chi nhánh (type 7)** = chuyển hàng từ kho **cty nguồn** → kho **cty đích**
  (khác công ty). Người ở cty đích yêu cầu điều chuyển. **Nếu người đó CÓ hàng giữ ở cty nguồn →
  xuất trên chính phần giữ đó; không có giữ → xuất từ tồn.**
- Hàng thường được đặt mua ở luồng mua về cty nguồn rồi gán giữ cho người ở cty đích → gần như chắc
  chắn hàng điều chuyển sẽ nằm trong phần giữ của người đó ở nguồn.
- ⟹ Điều chuyển chi nhánh **xuất từ giữ là ĐÚNG thiết kế**; **không lọc customer cũng ĐÚNG** (giữ
  là của người kinh doanh, không phải của một khách). Bước trừ giữ customer-blind trong
  `ProductExport::updateWarehouse` **giữ nguyên**.

## Ca thật (erp_new prod, 2026-09) — KHÔNG phải mất hàng của khách

- **pd 60504**: giữ 3 cái product 4524 cho kinh doanh **emp 263 Bùi Sỹ Phú** (đơn khách 17590 ĐỖ
  ANH SÀI GÒN), tại **cty nguồn = 1**.
- Ông 263 ở **cty đích = 4**, tạo 2 phiếu YC điều chuyển kéo hàng của mình từ cty 1:
  - **PXK-34214** (TR 7810): đòi 3 → xuất thực 3 từ giữ (pd 60504: 3→0) lúc 09-12 16:11.
  - **PXK-34072** (TR 7797): đòi 1 → ban đầu gợi ý 1 từ giữ.
- Giữ chỉ có 3, hai phiếu đòi 3+1 = **4 > 3**. Việc 34214 vét 3 là **hợp lệ** (hàng theo ông 263 về
  cty 4 để giao khách). Trạng thái cuối (giữ=0, 34072 xuất 1 từ tồn) là **phân bổ ĐÚNG**.

## Lỗi thật: cơ chế pending không quy đúng "người giữ" cho điều chuyển chi nhánh

Nguyên tắc đúng (user nêu): nếu cho nhiều phiếu cùng xuất từ giữ thì **tổng xuất-từ-giữ ≤ lượng
giữ**, phần dư rớt sang tồn. Hệ thống phải trừ chỗ (pending) để phiếu sau thấy phần phiếu trước đã
nhận. Nhưng với điều chuyển chi nhánh nó hụt:

`Product::getAccountingStockDetail()` — nhánh `pending_prepicks` (`app/Product.php:2470-2481`):
```php
->join('product_export_requests as pr', 'r.product_export_request_id', '=', 'pr.id')
->where('pr.created_by', $employee_id)   // $employee_id = người giữ = 263 (transfer requester)
```
Nhưng với điều chuyển chi nhánh, **`pr.created_by` = người LẬP phiếu ở nguồn (1119), không phải
người giữ**. Người giữ thật = `product_transfer_requests.created_by = 263` (đã verify: PER 39922 &
40081 đều created_by=1119, TR 7797 & 7810 đều created_by=263, company_id=4).

⟹ `1119 ≠ 263` → phiếu này **không thấy pending của phiếu kia** → cả hai cùng nhận "xuất từ giữ"
vượt lượng giữ (4 > 3).

**Hệ quả thực tế:** phiếu chốt sau (34072) khi xuất thực gặp giữ đã cạn (`ProductExport` ~1413):
`export_from_prepick(1) > total_prepick(0)` → **ném lỗi "Xuất nhiều hơn lượng prepick hiện có"** →
người dùng phải sửa tay sang xuất-từ-tồn. Nếu pending đúng, hệ thống tự chia (34072 → 1 từ tồn),
không kẹt.

## Hướng sửa: quy đúng "người giữ" trong pending cho type 7

Trong `getAccountingStockDetail()`, chỗ trừ pending phải xác định người giữ của **các phiếu khác**
giống hệt cách bước trừ giữ và bước đề nghị xác định: điều chuyển chi nhánh → `product_transfer_
requests.created_by`; loại khác → `pr.created_by`.

### Thay đổi code (ứng viên — chốt chi tiết ở Phase 1)
| # | Vị trí | Sửa |
|---|---|---|
| B1 | `Product.php` `pending_prepicks` ~2470-2481 | LEFT JOIN `product_transfer_requests as ptr` on `ptr.product_export_request_id = pr.id`; đổi `where('pr.created_by',$employee_id)` → khớp người giữ = `COALESCE(ptr.created_by, pr.created_by) = $employee_id` (chỉ áp cho pr.type=7 mới lấy ptr; loại khác COALESCE rơi về pr.created_by → **không đổi hành vi xuất thường**). Xử lý khả năng 1 PER có nhiều TR (lấy TR đầu / distinct). |
| B2 | `Product.php` block `total_pending_products` ~2512-2569 nếu cũng trừ theo người giữ | Rà xem có phụ thuộc `pr.created_by` không; nếu có, áp cùng logic COALESCE. |
| — | `ProductExport::updateWarehouse` (trừ giữ customer-blind, holder=TR.created_by), `WarehouseExportRequest::updateWarehouse` (đề nghị), sum tồn-giữ theo employee_id | **GIỮ NGUYÊN — đều đúng.** |

### Không đổi
- Không đụng logic customer-blind (đúng thiết kế).
- **Không vá dữ liệu prod** — trạng thái hiện tại đã đúng (giữ 60504=0 do 34214 hợp lệ, 34072 từ tồn).

## Kiểm thử then chốt
- 2 phiếu điều chuyển chi nhánh của cùng 1 người giữ, cùng product, tổng đòi > giữ → phiếu tính sau
  phải **tự trừ pending của phiếu trước**, chỉ gợi xuất-từ-giữ tới hết giữ, phần dư sang tồn; **không
  còn kẹt "xuất nhiều hơn prepick"**.
- Xuất thường (bán HĐ, xuất gửi…) của người có phiếu điều chuyển đang treo: pending vẫn khớp đúng,
  không đổi so với trước với các loại không phải type 7.
