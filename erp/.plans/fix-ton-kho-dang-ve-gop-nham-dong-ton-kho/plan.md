# Fix: lấy tồn kho đang về từ hợp đồng — SL nhảy hết vào dòng tồn kho khi hủy đặt lại

**Người phụ trách:** @junfoke
**Repo:** `TanPhatDev` · **Nhánh:** `task_ton-kho-dang-ve` (rẽ từ `master`)
**Nguồn:** chị QA/XNK báo qua chat 16/09/2026, HĐ mua trong nước `1336` (`/admin/orders/inland_buy_contract_new/1336/show`), PI `0168_2026/SEVL_TANPHAT`

## Hiện tượng

XNK hủy đặt lại toàn bộ PI. Sau đó ở màn Tổng hợp đặt hàng trong nước theo NCC, 2 bộ đặt cho khách
LEXUS PHÚ MỸ HƯNG (phiếu `PDHTN-04703`, KD Nguyễn Văn Thu) **biến mất và bị gộp vào dòng tồn kho
đang về** của `PDHTN-02251` (Trần Anh Tuấn - XNK): dòng tồn kho hiện 8 thay vì 6.

## Root cause (đã xác minh trên DB prod `erp_new`)

Chi tiết HĐ `6241` (khách Phú Mỹ Hưng, 2 bộ, tạo 25/08/2026) có
`inland_purchase_invoice_customer_id = 10857` — **đúng bằng dòng PI của tồn kho** (`type = 2`,
`PDHTN-02251`, `qty = 8`). Hai chi tiết HĐ khác nhau dùng chung một dòng PI.

Do `InlandOrderRequestNew::addCustomerStockEntry()` có 2 nhánh xử lý lệch nhau:

| | Nhánh `stock_entry_flowable_type = InlandPurchaseInvoice` | Nhánh `= InlandBuyContractNew` |
|---|---|---|
| Tạo dòng PI riêng cho khách | Có (`type = 1`) | **Không** |
| Trừ qty dòng PI tồn kho | Có | **Không** |
| Trừ qty phía hợp đồng | — | Có |

Nhánh hợp đồng copy thẳng `inland_purchase_invoice_customer_id` của dòng tồn kho sang chi tiết mới.
Khi `reOrder()` hủy đặt lại, `contracted_qty` được trả về "dòng PI đang link" → cả 6 lẫn 2 đổ chung
vào dòng tồn kho 10857.

## 2 lỗi độc lập phát hiện thêm

1. **`reOrder()` không chặn chạy lại trên dòng đã hủy** → bấm 2 lần trừ 2 lượt. Dòng PI `10856`
   đang `contracted_qty = -2`, sổ cái `order_stock_progress` id `35091` đang `qty = -2`.
   Dấu vết: chi tiết `4263` `updated_at` 18:03:22 còn dòng PI `updated_at` 18:04:34 — lần 2 Eloquent
   không dirty `status` nên không đụng `updated_at` của chi tiết, nhưng phép trừ vẫn chạy.
2. **Typo `objectable_id` lặp 2 lần** (phải là `objectable_type`) ở `InlandBuyContractNewController`
   trong `reOrder()` → `$stock_pi` luôn null, sổ cái hàng đang về **ở bước PI không được cộng trả
   lại** khi hủy đặt lại (3 dòng `35086/35087/35088` đang `qty = 0`). Kèm truy cập
   `->inland_purchase_invoice_customer->...` ngoài vùng null-check → 500 nếu link chết.

Quét toàn hệ thống: chỉ 2 HĐ khác có dòng link chết (`1812/ECO-TANPHAT`, `MK-111125`, mỗi cái 1 dòng).

## Tasks

### Phase A — Nắn dữ liệu HĐ 1336 (chờ user chốt hướng nghiệp vụ, KHÔNG làm trước)

- [x] Khách chốt **A1** (16/09/2026): giữ 2 bộ cho Lexus Phú Mỹ Hưng, tồn kho `PDHTN-02251` còn 6, để KD tạo lại bước HĐ
- [x] Bước 1 đã chạy trên prod `erp_new` 16/09/2026, 2 query kiểm đều khớp
- [x] Sổ cái bước PI đã bù (35086=2, 35087=6, 35088=2, thêm 54075=2)
- [x] Bước 2: **KHÔNG phải làm gì** — kiểm lại thấy số đã đúng sẵn (xem checkpoint cuối)

### Phase B — Vá code (độc lập Phase A, làm trước)

- [x] B1. `InlandOrderRequestNew::addCustomerStockEntry()` nhánh hợp đồng: tách dòng PI riêng cho
      khách (`type = 1`), chia cả `qty` lẫn `contracted_qty` từ dòng tồn kho, trỏ chi tiết HĐ mới
      sang dòng PI mới
- [x] B2. `InlandBuyContractNewController::reOrder()`: chặn khi chi tiết đã ở trạng thái HUY
- [x] B3. `InlandBuyContractNewController::reOrder()`: sửa 2 chỗ `objectable_id` → `objectable_type`
      và bỏ truy cập thuộc tính trên object có thể null
- [x] B4. `php -l` sạch, kiểm CRLF nguyên vẹn, `git diff --stat` không phình
- [x] B5. Commit `00ff575208` trên nhánh `task_ton-kho-dang-ve`
- [x] B6. Chạy luồng thật trên DB `erp_prod_09_26`, có đối chứng code cũ/code mới

## Checkpoint — 16/09/2026

Vừa hoàn thành: Phase B (B1-B5). Nhánh `task_ton-kho-dang-ve` rẽ từ `master`,
commit **`00ff575208`** — 2 file, +61/−6, `php -l` sạch, CRLF nguyên vẹn, không còn
chỗ nào viết `objectable_id', InlandPurchaseInvoice::class`.

Đang làm dở: không có.

Bước tiếp theo: (1) chạy thử luồng thật trên local hoặc staging — tạo phiếu đặt hàng
lấy tồn kho đang về **của hợp đồng**, kiểm PI đẻ ra dòng khách riêng, rồi hủy đặt lại xem
SL về đúng dòng; (2) chờ user chốt A1/A2 để chạy Phase A nắn dữ liệu HĐ 1336.

Blocked: Phase A chờ user chốt hướng nghiệp vụ.

**CHƯA test runtime** — DB local `erp_dev_30_01_26` là snapshot 30/01/2026, không có HĐ
mua trong nước nào còn dòng tồn kho hợp lệ để chạy đúng luồng này.

## Checkpoint — 16/09/2026 (Phase A bước 1)

Vừa hoàn thành: nắn dữ liệu HĐ 1336 / PI 2124 theo hướng A1, chạy trực tiếp trên prod `erp_new`.

Kết quả sau khi chạy — PI product row 10487 có 4 dòng:

| id | type | khách / phiếu | qty | contracted_qty |
|---|---|---|---|---|
| 10856 | 1 | 50TPHNCU-1 — PDHTN-01994 | 2 | 0 |
| 10857 | 2 | tồn kho — PDHTN-02251 | 6 | 0 |
| 10858 | 1 | 29TPHPTU-53 — PDHTN-02253 | 2 | 0 |
| **17159** | 1 | **50TPHPTA-1166 — PDHTN-04703** | 2 | 0 |

`order_stock_progress` (product 43297): 4 dòng bước PI cộng = 12 (35086=2, 35087=6,
35088=2, **54075**=2 mới tạo cho detail 5422), 4 dòng bước HĐ đều = 0 (35091 đã hết -2).
Chi tiết HĐ `6241` đã trỏ sang dòng PI `17159`.

Sao lưu trước khi chạy: `bk_20260916_pi_customers`, `bk_20260916_stock_progress`,
`bk_20260916_contract_details` (xoá sau khi nghiệm thu xong).

⚠️ KHÔNG được sửa PI này qua màn Sửa rồi bấm Lưu — `syncProducts()` xoá sạch và tạo lại
toàn bộ dòng phân bổ khách với id mới, sẽ đứt hết liên kết vừa nắn.

Bước tiếp theo: (1) KD lập lại hợp đồng cho dòng Lexus Phú Mỹ Hưng từ màn Tổng hợp đặt hàng
theo NCC; (2) Bước 2 — cột "Hàng đang về" trên phiếu đặt hàng, chờ kết quả query
`inland_order_request_new_products` id 3282 / 6479.

Blocked: không có.

## Checkpoint — 16/09/2026 (Phase A bước 2 — không cần làm)

Kiểm xong lớp "hàng đang về", kết luận **không phải nắn gì thêm**:

- `inland_order_request_new_product_details.arriving_qty` của 2402 / 2657 / 5422 đều = **2**,
  khớp đúng SL trên PI. Root detail cũng = 2.
- `PDHTN-02251` (product 3282 / root 11596): `arriving_qty = 6`, `stock_incoming_pi = 6`,
  `stock_incoming_contract = 0` — đúng sau khi tách.
- `PDHTN-04703` (product 6479 / root 21528): tất cả = 0 — **đúng theo thiết kế**, không phải bug.
  Hệ thống ghi "hàng đang về" ở 2 cấp khác nhau: dòng **tồn kho** ghi ở cấp SẢN PHẨM
  (`inland_order_request_new_products.arriving_qty` + `root.stock_incoming_pi`), dòng **đặt cho
  khách** ghi ở cấp DÒNG CHI TIẾT (`inland_order_request_new_product_details.arriving_qty`).
  Xem `InlandPurchaseInvoice::syncProducts()` — nhánh có `inland_order_request_new_detail_id`
  chỉ cộng vào detail, nhánh `type == 2` mới cộng vào product.
  ⚠️ Đừng lặp lại nhầm lẫn này: đã đoán sai một lần rằng `6479.arriving_qty` phải lên 2.

## Quyết định đã chốt

**`root_status` không hoàn tác khi hủy đặt lại — ĐỂ NGUYÊN, không sửa** (user chốt 16/09/2026).

Hiện trạng: `reOrder()` không lùi `root_order_request_product_details.status` và không xoá
`send_contract_date`. Sau khi hủy sạch HĐ 1336, 3 dòng gốc vẫn đứng ở `6 = Đang sản xuất`
(2402, 2657 — do `InlandBuyContractNewController.php:769` lúc duyệt HĐ) và `5 = Đã lập hợp đồng`
(5422 — sinh sau lúc duyệt nên dừng ở 5). Đáng lẽ phải lùi về `4 = Đàm phán đơn hàng`.

Lý do chấp nhận: màn theo dõi tiến độ chỉ sai trong khoảng chờ; KD lập lại hợp đồng là trạng thái
tự ghi đè đúng. Không vá code, không nắn dữ liệu cho phần này.

Nếu sau này quyết định làm: vá ở `reOrder()` nhánh `$type == 2`, lùi status về
`RootOrderRequestProductDetail::DAM_PHAN_DON_HANG` và `send_contract_date = null`
(luồng "không duyệt hợp đồng" đã có tiền lệ xoá `send_contract_date`).

## Checkpoint — 16/09/2026 (Phase B đã test luồng thật)

Test trên DB local **`erp_prod_09_26`** (bản prod mới), chạy bằng tinker trong transaction rồi
`DB::rollBack()` — **DB không đổi**. Script: `scratchpad/test_b.php` (chạy
`DB_DATABASE=erp_prod_09_26 php artisan tinker --execute="require '<path>';"`).

Kịch bản: HĐ `2046` (`DHNT-002046`) có chi tiết tồn kho `6539`, sản phẩm `28744`, qty 24,
dòng PI `16422` (type 2, qty 24, contracted 24). Tạo phiếu đặt hàng mới lấy **10** bộ tồn kho
đang về **của hợp đồng** → hủy đặt lại → bấm hủy đặt lại lần 2.

| Bước | Code CŨ (master) | Code MỚI (task_ton-kho-dang-ve) |
|---|---|---|
| Sau khi lấy 10 tồn kho | PI vẫn 1 dòng `16422` qty **24**; chi tiết HĐ mới link **trùng 16422** | PI tách 2 dòng: `16422` type 2 qty **14**/contracted 14 + dòng mới type 1 qty **10**/contracted 10; chi tiết HĐ mới link sang **dòng mới** |
| Sau hủy đặt lại | contracted dòng tồn kho 24 → **14** (10 của khách dồn vào tồn kho) | dòng khách contracted → **0**; dòng tồn kho **giữ nguyên 14/14** |
| Bấm hủy đặt lại lần 2 | **không bị chặn**, contracted 14 → **4** (trừ 2 lượt) | trả lỗi "Dòng hàng này đã được hủy trước đó.", số **không đổi** |

Code cũ tái hiện đúng cả 2 lỗi đã gặp ở HĐ 1336 (gộp vào dòng tồn kho + trừ 2 lượt thành số âm),
code mới sạch cả 2. Sau khi test, working tree trả về đúng nhánh, `git status` rỗng.

**ĐÃ LÊN `master` VÀ PUSH 16/09/2026** (`00ff575208`), nhánh task đã xoá.
