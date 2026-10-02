# Thêm cột Cước vận chuyển thực tế — màn DS Chuyến xe chở hàng & Chuyến xe khác (Redmine #11355)

@junfoke — Repo `TanPhatDev`, nhánh `task_11355` (checkout từ `master`).

## Yêu cầu (Redmine #11355)
- Màn **Chuyến xe chở hàng**: `/admin/warehouse/delivery_trips/all`
- Màn **Chuyến xe khác**: `/admin/other_delivery_trips/all`
- Thêm cột **Cước vận chuyển thực tế**, lấy đúng trường "Cước vận chuyển thực tế" ở màn chi tiết.
- Cột phải **sắp xếp được** (nhỏ → lớn và ngược lại).
- **Bộ lọc**: ô "từ" – "đến", lọc `từ <= cước vận chuyển thực tế <= đến`.
- Ảnh QA: cột đặt **trước cột Trạng thái** (sau cột Phiếu ở màn chuyến xe chở hàng).

## Hiện trạng code
| | Chuyến xe chở hàng | Chuyến xe khác |
|---|---|---|
| View | `resources/views/warehouse/delivery_trips/all.blade.php` | `resources/views/common/other_delivery_trips/all.blade.php` |
| Controller | `Warehouse\DeliveryTripController@searchData` | `Common\OtherDeliveryTripController@searchData` |
| Model filter | `App\Model\Warehouse\DeliveryTrip::searchByFilter` | `App\Model\Common\OtherDeliveryTrip::searchByFilter` |

- Trường dữ liệu = cột DB **`total_cost_transition`** (`decimal(16,2)`), có ở **cả 2 bảng** `delivery_trips` và `other_delivery_trips` (migration `2021_01_13_110637`, `2021_03_17_155233`). Màn chi tiết bind `form.total_cost_transition`.
- Không cần migration.

## Quyết định
1. **Không thêm search_type mới.** Dùng đúng pattern sẵn có của team: 2 ô `search_type: "currency"` (`*_from` / `*_to`) — giống `accounting/bill_commission_settlement_months/index.blade.php:71-72`, `customercare/warranty_payments/index.blade.php:79-80`.
   - Tham số gửi lên: `total_cost_transition_from`, `total_cost_transition_to`.
   - BE `str_replace(',', '', ...)` trước khi so sánh (ô currency tự chèn dấu phẩy hàng nghìn) — copy pattern `BillCommissionSettlementMonth.php:190-201`.
2. **Sắp xếp**: `total_cost_transition` là cột thật trong bảng nên để `orderable` mặc định (true) là Yajra tự `ORDER BY` đúng — không cần `orderColumn` tuỳ biến.
3. **Hiển thị**: `number_format(...)` trong `editColumn` (dữ liệu tiền các màn khác cùng kiểu). Null → chuỗi rỗng.
4. **Phạm vi**: chỉ màn danh sách. KHÔNG đụng In / Xuất Excel danh sách (issue không yêu cầu).
