# Báo cáo luân chuyển kho — cột "Hàng đang về" hiện phantom 144 (SP 5384, cty 1)

**Nhánh:** `gop_db` (ERP TanPhatDev) — DB gộp `hrm_erp_gop`
**Màn:** `admin/stock-transfer/report` (searchData + popup `getStockTranfer`)
**File liên quan (CHƯA sửa):**
- `app/Services/OrderReports/StockTransferReportService.php` (query getData ~1287–1355, display_stock_order ~1978, bản sao query ~3243–3340, popup getStockTranfer ~4445–4674)
- `app/Model/Warehouse/ProductImport.php` (khối decrement nhập khẩu mới ~1302–1393)
- `app/Model/Order/OrderStockProgress.php` (subtractQty/addQty/capToQty)

## Triệu chứng (user báo 2026-10-06)

SP `product_id=5384`, `company_id=1`: hàng đã về hết nhưng cột **Hàng đang về** vẫn hiện **144**.
Popup chi tiết tách 144 thành: 51 (PI 6001-443), 3 (HĐ mua JONNESWAY), 90 (PI 6001-451).

## Đã xác minh (Phase 1 — root cause investigation)

**1. 144 = SUM `order_request_product2.arriving_qty`** (phiếu PDHNK đã duyệt, cty 1, sau 2024-07-01).
Chỉ **2 dòng** ôm toàn bộ 144:

| orp2 | phiếu | type | arriving_qty | arrived_qty | OrderStockProgress (keyed OrderRequestProduct2) |
|---|---|---|---|---|---|
| #6789 | OR#3152 PDHNK-03152 | 1 (NK) | 54 | **2** | PI#1072 qty=51 + BuyContract2#889 qty=3 (Invoice2/CustomDeclaration/PIR#13698 đã về 0) |
| #8397 | OR#3736 PDHNK-03736 | 1 (NK) | 90 | **0** | PI#1262 qty=90 (KHÔNG có bước sau) |

- Cả 2 dòng **KHÔNG có** `order_request_product_detail2` nào (đơn đặt cho TỒN KHO, không phân bổ khách).
- `order_summary_product2` tương ứng (#13897 qty60, #17057 qty90) `arriving=0/arrived=0` và **không có** progress row → cấp summary KHÔNG phải nơi theo dõi; tracker thật là `order_request_product2` + OrderStockProgress keyed `OrderRequestProduct2`.

**2. Hàng CÓ về thật (ít nhất cho chuỗi 6001-443):**
- PI#1072 (6001-443, PO_JONN_0726.01, summary2 #1175) → đã có nhập **PNH-13030 = 60** (type 11, 2026-08-17) cho SP 5384. Nhưng `arrived_qty` của orp2#6789 chỉ = **2** → 60 đơn vị về được book sang đích KHÁC, không trừ về dòng đặt hàng #6789.
- Chuỗi orp2#6789 còn có PNH-13841 (6 đơn vị, 2026-09-09, qua PIR#13698).

**3. Cơ chế OrderStockProgress:** mỗi dòng đặt hàng có 1 "sổ cái" nhiều bước (PI → BuyContract → Invoice → CustomDeclaration → PIR). Khi hàng tiến bước: `addQty(bước sau)` + `subtractQty(bước trước)`. Khi NHẬP KHO (`ProductImport`) chỉ trừ **trực tiếp** dòng progress có objectable = ProductImportRequest (ProductImport.php:1343–1348/1357–1362), KHÔNG trừ bước PI/BuyContract.
→ Với orp2#6789: bước PI#1072 (51) và BuyContract2#889 (3) **không bao giờ bị trừ** khi hàng tiến xuống Invoice/Declaration/nhập → treo lại vĩnh viễn = phantom "đang về".
→ `ProductImport.php` khối `MUA_HANG_NUOC_NGOAI_MOI` trừ `order_request_product2.arriving_qty` chỉ ở nhánh `customer->type==2` và chỉ khi khớp `order_request2_id` của customer. Với 2 dòng này việc trừ không chạy (arrived≈0).

**4. Phạm vi KHÔNG chỉ 1 SP:** cty 1 có **315 dòng** `order_request_product2` arriving>0 (290 SP, tổng 57,522), 130 dòng > 60 ngày tuổi, chỉ 13 dòng arrived>0. (Chưa khẳng định tất cả đều phantom — phần lớn có thể là hàng đang về THẬT.)

## KẾT LUẬN ĐÚNG/SAI (đối chiếu vật lý — Phase 1b, 2026-10-06)

Đối chiếu **đặt (PO) vs về thật (PNH type 11)** cho SP 5384, cty 1, theo HĐ mua JONNESWAY:

| HĐ mua | Đặt (order_summary_product2) | Về thật (PNH type 11) | Chênh |
|---|---|---|---|
| 0825 | 156 | 102 (PNH-01854) | thiếu 54 |
| 1125 | 60 | 30 (PNH-05227) | thiếu 30 |
| 1225 | (không có PO khớp) | 24 (PNH-06090) | dư 24 |
| 0326 | 60 | 60 (PNH-08515) | 0 ✓ |
| **0726** | **60** | **66 (PNH-13030 60 + PNH-13841 6)** | **DƯ 6 — đã về đủ/vượt** |
| **0926** | **90** | **0** | **thiếu 90** |
| Tổng | 426 | 282 | 144 |

→ Báo cáo cộng `arriving_qty` = 144 = 54 (orp2#6789, gán cho PO 0726) + 90 (orp2#8397, gán cho PO 0926).
Nhưng đối chiếu vật lý tách bạch rõ:

**(1) 54 của orp2#6789 (PO_JONN_0726.01) = PHANTOM — SAI, phải bằng 0.**
- PO 0726 đặt 60, đã về **66** (PNH-13030=60 ngày 2026-08-17 + PNH-13841=6 ngày 2026-09-09) → về vượt.
- Sổ progress của #6789 chứng minh pipeline đã chạy hết: Invoice2#722/#742/#748 = 0, CustomDeclaration#772 = 0, **ProductImportRequest#13698 = 0** (đúng PIR của PNH-13841) — mọi bước dưới đã trừ về 0.
- CHỈ 2 bước đầu kẹt lại: **PurchaseInvoice#1072 = 51 + BuyContract2#889 = 3 = 54**. Khi hàng tiến từ PI/HĐ xuống bước sau, code KHÔNG `subtractQty` 2 bước đầu → treo phantom. Đúng cơ chế đã mô tả ở mục 3.

**(2) 90 của orp2#8397 (PO_JONN_0926.02) = THEO HỆ THỐNG LÀ CHƯA VỀ — báo cáo ĐÚNG.**
- PO 0926: **0** phiếu nhập type 11.
- Sổ progress của #8397 **chỉ có đúng 1 dòng**: PurchaseInvoice#1262 = 90. KHÔNG có BuyContract, Invoice2, CustomDeclaration, PIR nào → pipeline đứng nguyên ở bước PI.
- PI 6001-451 mới lập **2026-09-21**, chưa qua hải quan, chưa nhập. ⇒ 90 cái này ĐÚNG là đang về (hoặc chưa về), KHÔNG phải phantom.
- Không có phiếu nhập ~90 cái nào (mọi type) cho SP 5384 cty 1 sau 2026-09 → hàng chưa thực sự vào kho trong hệ thống.

**Tóm lại:** con số đúng phải là **90** (không phải 144). 54 là phantom cần gỡ; 90 là thật theo dữ liệu.

## Việc duy nhất cần user xác nhận (1 sự thật vật lý)

PO **PO_JONN_0926.02** (90 cái, PI 6001-451 lập 21/09/2026) — hàng đã **thực sự vào kho** chưa?
- Nếu CHƯA → báo cáo hiện 90 là ĐÚNG, chỉ cần gỡ 54 phantom của #6789.
- Nếu RỒI (về mà quên nhập phiếu) → đó là lỗ hổng nhập liệu riêng (pipeline chưa chạy past PI), xử lý khác.

## Chưa kết luận được (phần mở rộng)

Có 2 khả năng, FIX khác hẳn nhau:

- **(A) Stale/phantom do code không trừ ngược về `order_request_product2`** khi nhập kho cho đơn đặt-tồn-kho (customer không map lại đúng dòng đặt). → cần fix `ProductImport.php` + **backfill** data 2 dòng (và rà 130 dòng cũ). ĐỘNG vào hàm/luồng dùng chung → **phải hỏi user trước** (CLAUDE.md).
- **(B) Dữ liệu mồ côi / hàng về qua đơn khác**: 2 dòng đặt này bị bỏ, hàng thực nhập theo đơn khác. → chỉ **dọn data** 2 dòng, không sửa code.

Riêng orp2#8397 (90 @ PI#1262 tạo **2026-09-21**, chưa có nhập nào sau đó cho 90 đơn vị) → có thể là **hàng đang về THẬT**, chưa chắc phantom. Cần user xác nhận PO **6001-451** đã về kho chưa.

## Việc cần user quyết (hỏi trước khi làm)

1. PO **6001-443** (orp2#6789, 54) và **6001-451** (orp2#8397, 90) hàng đã về kho thực tế chưa?
2. Nếu đã về: muốn **sửa code** luồng trừ `order_request_product2` khi nhập (systemic, cần hỏi vì là hàm dùng chung) hay chỉ **dọn data** 2 dòng này?
3. Có backfill cho 130 dòng cũ nghi phantom không, hay chỉ xử lý SP 5384?

## XỬ LÝ 54 (quyết định 2026-10-06) — DỌN DATA 1 dòng, KHÔNG sửa code chung

User chốt "xử lý cái 54 trước, cái 90 để lại". Vì PO_0726 đã về đủ/vượt vật lý (66≥60),
54 là phantom thuần → **chỉ dọn data cho đúng orp2#6789**, gác việc sửa luồng advance
dùng chung (BuyContract2Controller) lại cùng với 90 (systemic, cần hỏi trước).

**Bằng chứng drift ở `root_order_request_products#17070`:** `stock_incoming_pi=54`,
`stock_incoming_invoice=-3` (ÂM → cascade trừ lỗi), `arriving_qty=54` trong khi
`order_company_qty=60` đã về đủ. 3 tầng tracker đều treo 54.

**Chỉ gỡ "đang về", KHÔNG đụng `arrived_qty`** (60 về thật đã book sang chuỗi khác, cộng vào
đây sẽ double-count). Script: `scratchpad/fix54.php` (transaction, DRY-RUN mặc định, APPLY=1 ghi thật).

| Bảng | Dòng | Trước | Sau |
|---|---|---|---|
| order_request_product2 | #6789 | arriving_qty=54 | 0 (arrived=2 giữ nguyên) |
| root_order_request_products | #17070 | arriving=54, inc_pi=54, inc_invoice=-3, inc_notify=3 | tất cả =0 (arrived=2 giữ) |
| order_stock_progress | PROG#41798 (PI#1072) | 51 | 0 |
| order_stock_progress | PROG#47954 (BuyContract2#889) | 3 | 0 |

## Tasks

- [x] Phase 1: trace 144 → 2 dòng orp2, xác minh tracker, cơ chế OrderStockProgress, hàng đã về thật
- [x] Phase 1b: đối chiếu vật lý → 54 phantom (PO_0726 về đủ), 90 theo hệ thống là thật
- [x] Soạn script dọn data fix54.php + DRY-RUN xác nhận đọc/ghi đúng dòng
- [x] **ĐÃ GHI THẬT** (APPLY=1, 2026-10-07) → DB gộp prod. Verify: orp2#6789 arriving=0, root#17070 incoming=0, PROG#41798/47954=0. TỔNG arriving SP5384 cty1 = **90** (còn đúng orp2#8397)
- [x] (user chốt 2026-10-07: FIX LUÔN) Điều tra + vá lỗi "không trừ ngược" — xem mục FIX CODE bên dưới
- [ ] Verify trình duyệt lại báo cáo sau khi ghi (đang về còn 90)
- [ ] (gác) Rà 130 dòng cũ nghi phantom cty 1

## FIX CODE "không trừ ngược" (2026-10-07) — kết quả điều tra Phase 2/3

### Bug (D) ĐÃ VÁ — typo trong luồng "Hủy đặt lại" (BuyContract2Controller.php:1485)

`cancelContractDetail` nhánh `type==2` (hủy đặt lại), dòng đặt-tồn-kho (OrderRequestProduct2):
- Dòng 1480: Sổ B `stock_incoming_pi += qty` (hoàn về bước PI) — CHẠY
- Dòng 1484-1485: tìm progress Sổ A bước PI để `qty += qty` — nhưng viết sai
  `->where('objectable_id', PurchaseInvoice::class)` (lẽ ra `objectable_type`) → query không match → `$stock_pi=null` → **Sổ A KHÔNG được hoàn**, Sổ B thì có → 2 sổ lệch.
- 2 nhánh anh em (OrderSummaryProduct2 dòng 1506, OrderRequestProductDetail2 dòng 1534) viết ĐÚNG `objectable_type`.
- **FIX: đổi `objectable_id` → `objectable_type` ở dòng 1485.** Rà toàn repo (`grep objectable_id...::class` trong app/): **chỉ 1 ca duy nhất này**, mọi chỗ khác đã đúng.

### SỰ THẬT TRUNG THỰC: Bug (D) KHÔNG phải cơ chế gây phantom #6789

Đã kiểm chứng luồng **tiến** (duyệt HĐ mua `store`, dòng 896-901 cho OrderRequestProductDetail2 + 937-942 cho OrderRequestProduct2):
```
$order_stock_pi->qty -= $detail->qty;   // Sổ A: trừ bước PI  ✓
$root_order_request_product->stock_incoming_pi -= $detail->qty;      // Sổ B ✓
$root_order_request_product->stock_incoming_contract += $detail->qty; // Sổ B ✓
```
→ Luồng tiến **CÓ** trừ ngược bước PI đúng. Không thiếu subtract ở happy-path.

**Vậy tại sao PI#1072 của #6789 kẹt 51?** Vì trên dòng đặt #6789 **chỉ có 9 đơn vị** từng được lập HĐ mua (BuyContract2#889=3 + 6 đã nhập qua PIR#13698). 60−9=51 chưa bao giờ "tiến" trên sổ #6789 → PI giữ 51. 51 đó về thật qua **PI 6001-427 — chuỗi KHÁC, gắn dòng đặt khác** — nên sổ #6789 không có sự kiện nào để trừ.

⇒ Root-cause #6789 = **finding (B): hàng về qua chuỗi song song không liên kết lại dòng đặt gốc.**
KHÔNG có dòng code nào bị thiếu `subtractQty` ở luồng chuẩn; đây là desync **cấu trúc/quy trình**,
không phải 1 bug vá 1 dòng. Dọn data (đã làm) là cách xử lý đúng cho ca này.

### Tồn đọng cần user QUYẾT (chưa làm — rủi ro cao, hàm/quy trình dùng chung)

Để NGĂN TÁI DIỄN ca #6789 chỉ có 2 hướng, đều cần user chốt:
- **(H1) Chốt chặn reconcile khi nhập/định kỳ:** khi nhập kho (ProductImport type 11) hoặc 1 job rà,
  phát hiện bước PI/HĐ còn treo cho SP+cty mà nhu cầu đã thỏa vật lý → zero bước treo. An toàn hơn
  (không đụng luồng tiến đang chạy đúng) nhưng cần định nghĩa "đã thỏa" chặt để không xóa nhầm hàng về thật.
- **(H2) Kỷ luật quy trình:** buộc PI nhập liên kết đúng dòng đặt gốc → luồng tiến tự trừ. Đụng quy
  trình mua hàng, không chỉ code.

## Đặt 60 về 66 — giải thích (2026-10-07)

Không phải 1 đơn dư 6. Là **2 lần nhập riêng cùng dán nhãn HĐ mua "JONNESWAY 0726 HP"**:
- PNH-13030 = **60**, PI 6001-427(+427A), THCPNK-00670, 17/08/2026 (= đúng SL đặt PO_JONN_0726.01)
- PNH-13841 = **6**, PI 6001-443(+443A), THCPNK-00708, 09/09/2026 (đợt bổ sung, PI/PYCNH khác)

PO gốc chỉ đặt 60. 6 cái (09/09) KHÔNG khớp đơn đặt nào — bản chất (bù thiếu/hỏng hay nhập thừa) hệ
thống không ghi lý do, cần hỏi bộ phận mua nếu muốn truy. KHÔNG ảnh hưởng kết luận 54 phantom
(PO về ≥60 = đủ → không còn gì đang về).

## Reconcile 54 (sau khi có dữ liệu 2 PI): 51(PI#1072) + 3(BuyContract#889) + 6(đã nhập) = 60 = SL đặt

→ 51 đơn vị KẸT ở bước PurchaseInvoice của sổ #6789 (trỏ PI 6001-443 vốn chỉ nhập 6). 60 cái thật về
qua PI 6001-427 — chuỗi KHÁC — nên sổ của #6789 không được trừ ngược. `root#17070.stock_incoming_invoice
= -3` (ÂM) = bằng chứng cascade trừ sai. Root-cause code đang điều tra: bước advance add bước sau mà
không subtract bước trước, HOẶC nhập kho chỉ trừ stage PIR/notify không trừ PI/BuyContract.
