# Chặn lập HĐ khi hàng hoá chưa đủ điều kiện tính DSTC — Design

**Ngày:** 2026-10-21 · **Nhánh:** `gop_db` (worktree `feat/chan-lap-hd-chua-he-so-dstc` cả 2 repo)
**Spec gốc (tiền đề):** `docs/superpowers/specs/gop-db/2026-10-19-he-so-dstc-theo-tinh-chat-nature-design.md`

## Goal

Chặn **lập hợp đồng** (và phụ lục) trên CẢ ERP và HRM nếu có dòng hàng hoá mà:
- (a) **chưa gắn tính chất hàng hoá** (không leo ra được `product_nature_id`), HOẶC
- (b) tính chất đã có nhưng **công ty chưa khai dòng** trong `company_product_natures`, HOẶC
- (c) tính chất đã khai nhưng **hệ số quy đổi DSTC = 0**.

HĐ **dịch vụ**: dòng "Dịch vụ" (nature_id = 0) của công ty phải có hệ số **> 0**.

Mục tiêu: không để lọt HĐ mà khi tính "doanh số tiêu chuẩn" (standard_price) nhân hệ số DSTC
bị **mất trắng** (hệ số fallback 1 che mất việc chưa khai) hoặc **= 0** (nhân 0).

## Nguyên tắc nền

Kế thừa toàn bộ từ spec gốc: DB chung, 1 bảng `company_product_natures`, leo cây
`products.product_type_id → … → product_nature_id` **y hệt** 2 app (xem spec gốc §"Đường leo cây").
Helper `ProductNatureDstcCoefficient` đã tồn tại ở cả 2 repo và **đang** trả `1.0` cho cả
"không ra nature" lẫn "chưa khai" — nên **không dùng lại được** cho việc chặn (không phân biệt
3 trường hợp). Phải THÊM method validate mới, **giữ nguyên** các method `forProduct/forService/
forNature` hiện có (đang được dùng ở điểm tính giá — spec gốc §"Điểm đọc hệ số").

## Quyết định đã chốt (các window trước)

| # | Hạng mục | Quyết định |
|---|---|---|
| 1 | Hệ số = 0 | **CŨNG chặn** (nhân 0 = mất doanh số) |
| 2 | Phạm vi loại HĐ | **CẢ** HĐ hàng hoá **VÀ** HĐ dịch vụ (dịch vụ: nature 0 phải > 0) |
| 3 | FE/BE | **Hướng A — BE-only**: BE chặn (ERP 422/responseErrors, HRM 422 ValidationException), FE chỉ hiển thị message trả về. **KHÔNG** precheck chủ động ở FE |
| 4 | Hàng tạm HRM (`erp_product_id` NULL) | **CŨNG chặn** — coi như `no_nature` |
| 5 | **Phạm vi phiếu (HƯỚNG 2 — chốt 2026-10-21)** | Chặn **CẢ HĐ tạo MỚI VÀ phụ lục** (phụ lục bổ sung + phụ lục thường). ERP guard phải phủ cả đường phụ lục; KHÔNG cần cổng `if($generateCode)` để bỏ qua phụ lục |

## Kiến trúc chặn

### Vì sao KHÔNG throw exception trong chokepoint (ERP)

Controller HĐ ERP bọc `$service->store(...)` trong:
```php
DB::beginTransaction();
try { ... $service->store($storeValues, $quotation); ... DB::commit(); }
catch (\Exception $e) {
    DB::rollBack();
    if ($e->getCode() == 23000) { ... }          // chỉ bắt lỗi trùng key
    return $this->responseErrors("Không thể tạo hợp đồng, vui lòng thử lại sau.");
}
```
→ `catch` **nuốt** message cụ thể của exception. Nếu throw từ trong `store()`, user chỉ thấy
câu chung "Không thể tạo hợp đồng". Vậy guard phải chạy **TRƯỚC** transaction, ở **tầng
controller**, theo đúng idiom ERP `[bool $isInvalid, string $message]` → `responseErrors`.

### ERP — guard pre-transaction `[bool, message]`

Thêm method **`validateProductNatureDstc(Request $request): array`** trên `FirmContractService`
(các lớp con `ZT*`, `Principle*` kế thừa), **soi khuôn `validateDifferencePrice`**:
- Duyệt `product_id` ở `$request->tabs[*]['products'][*]['product_id']` **và**
  `$request->groups[*]['products'][*]['product_id']` (y hệt `validateDifferencePrice`).
- `company_id = auth()->user()->info->company_id`.
- Gọi helper `ProductNatureDstcCoefficient::validateProducts($companyId, $erpProductIds)` (batch)
  → trả danh sách dòng lỗi kèm reason code.
- Trả `[true, $message]` nếu có lỗi, `[false, null]` nếu OK.

HĐ dịch vụ (ERP `WrServiceContract`): guard riêng gọi `validateService($companyId)` (nature 0).

Gọi tại **mọi** action method create/update/annex (trước `DB::beginTransaction()`):
```php
list($isInvalid, $message) = $service->validateProductNatureDstc($request);
if ($isInvalid) return $this->responseErrors($message);
```

### HRM — guard pre-transaction `ValidationException::withMessages`

HRM `catch (\Exception)` chung KHÔNG bắt `ValidationException` (nó là `HttpException`-family,
Laravel tự render 422). Guard chạy **đầu** `createFromQuotation` (trước `DB::transaction`):
- `ContractService::createFromQuotation` (HĐ hàng hoá): lấy `erp_product_id` từ
  `quotation->productPrices` (hàng tạm `erp_product_id` NULL → `no_nature`).
- `WrServiceContractService::createFromQuotation` (HĐ dịch vụ): validate nature 0.
- Nếu có lỗi → `throw ValidationException::withMessages(['products' => [$message]])` → 422.

### Helper — method validate MỚI (cả 2 repo, giữ nguyên method cũ)

| Method | Trả về |
|---|---|
| `validateProducts(?int $companyId, array $erpProductIds): array` | `[['erp_product_id'=>.., 'reason'=>'no_nature'\|'no_config'\|'zero_coef'], …]` — rỗng nếu tất cả OK |
| `validateService(?int $companyId): ?string` | reason code hoặc `null` nếu OK |

- `no_nature`: `erp_product_id` NULL/0, HOẶC leo cây không ra `product_nature_id`.
- `no_config`: ra nature nhưng công ty không có dòng `company_product_natures`.
- `zero_coef`: có dòng nhưng `coefficient <= 0`.
- ERP: dùng lại cache `$maps` qua **private `cachedMap()`** rút ra từ `forNature` — `forNature`
  giữ **byte-identical** (không đổi hành vi điểm tính giá). `cachedMap()` phải lấy `coefficient`
  qua `array_key_exists` để **phân biệt** "không có dòng" (no_config) với "có dòng, coef 0" (zero_coef).

### Message (đã duyệt)

Header: `Không thể lập hợp đồng. Các hàng hoá sau chưa đủ điều kiện tính doanh số tiêu chuẩn:`
Mỗi dòng (theo reason):
- `no_nature` → `• <mã> - <tên>: chưa gắn tính chất hàng hoá`
- `no_config` → `• <mã> - <tên>: tính chất "<tên nature>" chưa cài hệ số quy đổi DSTC`
- `zero_coef` → `• <mã> - <tên>: hệ số quy đổi DSTC phải lớn hơn 0`

HĐ dịch vụ: `Không thể lập hợp đồng dịch vụ: dòng "Dịch vụ" chưa cài hệ số quy đổi DSTC` /
`… hệ số quy đổi DSTC phải lớn hơn 0`.

## Điểm gắn guard

### ERP (HƯỚNG 2 — new + annexes)

Service method `validateProductNatureDstc` trên `FirmContractService` (kế thừa xuống `ZT*`,
`Principle*`). Gọi ở **mọi** action create/update/annex của các controller tham chiếu
`FirmContractService`/`ZTFirmContractService`/`PrincipleOrderService`/`ZTPrincipleOrderService`/
`FirmContractAnnexService` — xem plan.md để liệt kê chính xác controller + method (đọc trước khi sửa).
HĐ dịch vụ: guard ở controller WrServiceContract (create + annex).

### HRM

- `Modules/Assign/Services/ContractService.php::createFromQuotation` (hàng hoá).
- `Modules/CustomerCare/Services/WrServiceContractService.php::createFromQuotation` (dịch vụ).
- Đường phụ lục HRM (nếu có tạo phụ lục qua service riêng) — đọc xác nhận trong plan.

## Testing

- **Helper (cả 2):** validateProducts với 4 ca (đã phân loại + khai > 0 = OK; chưa phân loại =
  no_nature; ra nature nhưng công ty chưa khai = no_config; khai coef 0 = zero_coef). validateService
  2 ca (khai > 0 OK; khai 0 / chưa khai = chặn).
- **ERP:** tinker bọc `DB::beginTransaction()/rollBack()` — dựng request giả tabs/groups, assert
  `validateProductNatureDstc` trả `[true, …]` đúng message; 1 ca OK trả `[false, null]`.
- **HRM:** feature test createFromQuotation ném 422 khi có dòng thiếu điều kiện; pass khi đủ.

## Review Focus (dễ sót)

- **Hàng tạm HRM** `erp_product_id` NULL phải rơi vào `no_nature` (không bị bỏ qua).
- **Hệ số 0 vs chưa khai**: `cachedMap()`/query phải phân biệt `array_key_exists` (no_config) với
  giá trị 0 (zero_coef) — không dùng truthiness.
- **Không đổi hành vi `forNature/forProduct/forService`** cũ (điểm tính giá vẫn fallback 1).
- **Phủ đủ đường phụ lục** (HƯỚNG 2) — bỏ sót 1 controller annex = lọt lưới.
- **Lớp con ERP** (`ZT*`, `Principle*`) kế thừa đúng method; action method của chúng cũng phải gọi guard.
- **Company_id nguồn**: ERP `auth()->user()->info->company_id`; HRM `optional(optional(auth()->user())->info)->company_id`.

## Rủi ro / điểm mở

- Số lượng controller ERP lớn (~24 tham chiếu). Phải đọc từng action method trước khi chèn guard;
  KHÔNG chèn máy móc. Plan liệt kê danh sách; khi sửa đọc lại file xác nhận vị trí trước transaction.
- Guard thêm 1-2 query/HĐ (batch) — chấp nhận được, không N+1.

---

*Chưa commit (ràng buộc: không commit/push khi chưa yêu cầu).*
