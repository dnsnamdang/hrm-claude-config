# Task P2-8 Report — StoreBorrowSellRequest FormRequest + Test

## Status
**DONE**

## Commit
```
7277390be Task P2-8: Thêm FormRequest + test cho xuất bán hàng mượn
```

## Deliverables

### 1. FormRequest
- **File:** `Modules/Finance/Http/Requests/BorrowSell/StoreBorrowSellRequest.php`
- Validate payload theo đúng shape từ brief:
  - `borrow_sell_request_id`: required|integer|exists
  - `products[*]`: array với min:1
    - `objectable_id`: required|integer
    - `objectable_type`: required|string
    - `details[*]`: array với min:1
      - `product_export_request_detail_id`: required|integer
      - `qty`: required|numeric|min:0
- Messages tiếng Việt đầy đủ per brief
- Authorize: return true (quyền gate ở middleware + service)

### 2. Test
- **File:** `Modules/Finance/Tests/Unit/StoreBorrowSellRequestTest.php`
- 3 test cases:
  1. `test_missing_products_fails()` — validation fails khi thiếu products
  2. `test_missing_product_details_fails()` — validation fails khi thiếu products.0.details
  3. `test_valid_payload_passes()` — payload hợp lệ passes (unset FK rule để không phụ thuộc DB)

## Test Summary
**3/3 tests pass** (OK: 5 assertions, 2.033s)

## Concerns
None. Payload shape và rules match đúng T7 BorrowSellService::store() consume.

## Notes
- Không dùng DB_CONNECTION_SECOND/mysql2 (none)
- Không override failedValidation (giữ mặc định Laravel rethrow)
- Test unset borrow_sell_request_id rule để tránh DB dependency trên unit test (inline comment giải thích)
