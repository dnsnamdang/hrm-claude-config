# Fix 500 danh sách Phiếu YC xuất bán hàng mượn — `admin/warehouse/borrow_sell_requests?type=all`

> Nhánh: `develop_02` (hậu duệ `gop_db`) · DB lỗi: `hrm_erp_test`
> Loại: bug fix phát sinh sau gộp DB

## Bối cảnh / Root cause

- `GET admin/warehouse/borrow_sell_requests?type=all` → **500 SQL** `Unknown column 'customer_id' in 'field list'` trên bảng `inland_buy_contract_news`.
- `BorrowSellRequest.contractable` là quan hệ **morphTo** nhiều loại HĐ. Eager-load trong `searchByFilter()` hard-code `->select(['id','code','customer_id','type'])` cho **mọi** loại HĐ.
- HĐ bán (`FirmContract`, `WrServiceContract`) có cột `customer_id`; nhưng **HĐ mua nội địa `InlandBuyContractNew` KHÔNG có `customer_id`** và không có quan hệ `customer()`. Sau gộp DB, luồng YCXBHM/HRM có thể link 1 phiếu YC sang HĐ mua nội địa (dòng `TEST.YCXBHM-PKT.00001`, id 5003 → HĐ mua id 2169) → select cứng `customer_id` gãy SQL, 500 **cả danh sách**.

## Tasks

- [x] Model `app/Model/Warehouse/BorrowSellRequest.php::searchByFilter()` — bỏ `select(['id','code','customer_id','type'])` cứng trên `contractable`; dùng `morphWith([FirmContract, WrServiceContract => ['customer' => select(id,fullname)]])` để chỉ eager-load `customer` theo đúng loại HĐ bán. Thêm `use ...\MorphTo;`.
- [x] Controller `app/Http/Controllers/Warehouse/BorrowSellRequestsController.php::searchData()` — null-guard các closure: `contract` (`$object->contractable ? ...code : ''`), `contract_link` (`...->link : ''`), `customer_name` (`optional(optional($object->contractable)->customer)->fullname`).
- [x] Kiểm controller song sinh CRM `app/Http/Controllers/CRM/Warehouse/BorrowSellRequestsController.php` — chỉ serialize `items()`, không truy cập `contractable->customer->fullname`/`->link`; dùng chung `searchByFilter` đã fix → **KHÔNG cần sửa**.
- [x] Xác minh approve methods (`canApprove/canManagerApprove/canBoardOfManagerApprove`) không đụng `contractable` → an toàn với dòng inland.
- [x] Mô phỏng toàn bộ closure của `searchData` trên `hrm_erp_test` (200 dòng gồm dòng inland 5003): **0 errors**, dòng inland render `customer_name=''` không crash, dòng HĐ bán vẫn ra customer qua morphWith.
- [x] **Quyết định nghiệp vụ (user chốt 2026-10-13):** data có thể sai nhưng **chỉ cần fix cho không lỗi**. → KHÔNG chặn linkage YC↔HĐ mua ở tầng nghiệp vụ; fix code (morphWith + null-guard) là đủ.
- [ ] Xin phép commit (ERP: không commit khi chưa có yêu cầu).

## Kết quả kiểm thử

```
DB = hrm_erp_test
row 5003: type=App\Model\Order\InlandBuyContractNew status=1 created_by=13 company_id=1
searchByFilter OK, loaded 200 rows
  [INLAND OK] id=5003 contract='DHNT-002169' link_set=Y customer_name='' canApprove=0
DONE. rows_run=200 errors=0 inland_seen=Y
```

## Checkpoint — 2026-10-13
Vừa hoàn thành: Fix model + controller, kiểm CRM song sinh (không cần sửa), mô phỏng đủ closure trên hrm_erp_test = 0 lỗi. User chốt chỉ fix cho hết lỗi, không chặn linkage nghiệp vụ.
Đang làm dở: chờ user duyệt commit.
Bước tiếp theo: user xác nhận → commit 2 file đã sửa.
Blocked:
