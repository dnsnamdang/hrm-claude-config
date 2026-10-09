# Fix data — PYCXH-38110 sửa "có lắp đặt" nhưng không hiện ở YC lắp đặt bàn giao

DB: **erp_new (production)** — erp.eteksofts.com:33061

## Hiện tượng
Phiếu yêu cầu xuất hàng **PYCXH-38110** được sửa thành "có lắp đặt", nhưng khi tạo
**Yêu cầu lắp đặt bàn giao** (AssemblyRequest) thì phiếu không hiện ra trong picker chọn phiếu xuất.

## Root cause (đã điều tra, không đoán)
Luồng AssemblyRequest có 2 cổng:
1. `FirmContractController@getDataForFirmContractAssemblyProduct($contract)` — trả danh sách SP
   cần lắp đặt. JS chỉ set `self.firm_contract_id` (mở được picker phiếu) khi danh sách này > 0.
   Query lọc `firm_contract_tab_products` theo `(need_repair = 1 OR created_at < '2025-11-16 23:59:59')`
   rồi `having SUM(warehouse_exported_qty) > 0`.
2. `SearchProductExportRequestService@searchAllProductExportRequest` — picker phiếu xuất.

Kiểm chứng trên erp_new:
- HĐ gốc **21134** (`HĐ_..._0553_VinfastDTBacGiang`, type=1): getData → **135 SP** → mở được picker.
- **PLBS1 22371** (`..._PLBS1`, type=2, parent=21134) — nơi phiếu 38110 thuộc về: getData → **0 SP**.
  Vì cả 10 dòng `firm_contract_tab_products` của 22371 đều `need_repair=0/NULL` và `created_at=2026-06-18`
  (SAU mốc grandfather 2025-11-16) → bị loại hết → danh sách rỗng → JS KHÔNG set firm_contract_id
  → picker không mở → "phiếu chưa hiện ra".
- Picker search (cổng 2) trả phiếu 38110 cho **cả** 2 lựa chọn HĐ (status=5 ∈ [4,8,9,5,1], type=14 ∉ [2,8]).

⇒ Người dùng chọn **PLBS1 22371** (đúng nơi họ sửa "có lắp đặt"), nên vướng cổng 1.
Việc sửa phiếu chỉ set `product_export_requests.need_repair=1`, KHÔNG lan sang
`firm_contract_tab_products.need_repair` mà cổng 1 đọc → đó là gốc lỗi.

## Phạm vi sửa (chính xác)
Phiếu 38110 có 4 dòng `need_export=1` (SP 31798, 29882, 38793, 31723) ↔ tab-product rows:
`253677, 253678, 253679, 253680` (đều fcid=22371, root=21134, whx>0, need_repair=0).
Hai dòng exported khác của PLBS1 (253676 pid 43588, 253681 pid 43788) thuộc phiếu KHÁC
(không đánh "có lắp đặt") → GIỮ NGUYÊN.

## Task
- [x] Điều tra root cause trên erp_new (2 cổng, hierarchy HĐ, mapping tab-product)
- [x] Thêm method `fixAssemblyNeedRepairPycxh38110()` vào `database/seeds/UpdateDB.php`
      (dry-run mặc định, in before-state để hoàn tác được)
- [x] Chạy dry-run qua tinker → xác nhận đúng 4 dòng 253677–253680
- [x] Chạy thật: `UPDATE firm_contract_tab_products SET need_repair=1 WHERE id IN (253677,253678,253679,253680)` → affected=4
- [x] Verify: getDataForFirmContractAssemblyProduct(22371) trả 4 SP ✓

### Kết quả — 2026-08-25
Đã update 4 dòng trên erp_new. getData(22371): 0 → 4 SP. Picker phiếu (cổng 2) đã trả 38110 sẵn.
Hoàn tác nếu cần: `UPDATE firm_contract_tab_products SET need_repair=0 WHERE id IN (253677,253678,253679,253680)`.

---

## Case tiếp theo — HĐ_TPV_MT_KD_26_0687_102 (fcid 26990) — 2026-09-11

Cùng root cause: user tick "Có lắp đặt" sau khi phiếu đã xuất → `product_export_requests.need_repair`
được set nhưng KHÔNG lan sang `firm_contract_tab_products.need_repair` → cổng lắp đặt (getInstallable…)
đọc `need_repair=1` nên bỏ qua → installable = 0 → chặn tạo YCLD lắp đặt.

- Tầng 1: phiếu YCXH `product_export_requests` id **39961** (PYCXH-39961, type=14) — need_repair 0→1.
- Tầng 2: dòng HĐ đã xuất `firm_contract_tab_products` id **344531** (prod 42425), **344532** (prod 4524) — need_repair 0→1.
- Bỏ qua id 344533 (prod 49599, `warehouse_exported_qty=0` → chưa xuất, không đụng).

### Task
- [x] Khảo sát prod erp_new: xác định fcid 26990, PER 39961, FCTP 344531/344532 (skip 344533)
- [x] Thêm method `fixInstallFlagFirmContract26990_20260911($dryRun=true)` vào `database/seeds/UpdateDB.php`
      (transaction + verify installable trong hàm; dry-run tự rollback)
- [x] Dry-run qua tinker → Tầng1=1 [39961], Tầng2=2 [344531,344532], installable 42425/4524 = 1/1
- [x] User duyệt → chạy thật `(false)` → COMMIT; verify độc lập: PER 39961=1, FCTP 344531=1, 344532=1

### Kết quả — 2026-09-11
Đã commit trên erp_new. installable prod 42425 & 4524: 0 → 1 (hết chặn tạo YCLD lắp đặt).
Hoàn tác nếu cần:
`UPDATE product_export_requests SET need_repair=0 WHERE id=39961;`
`UPDATE firm_contract_tab_products SET need_repair=0 WHERE id IN (344531,344532);`

---

## Case tiếp theo — HĐ_TPE_HN_KD2_26_0742_CARPLA (fcid 21001) — 2026-09-17

Cùng root cause: user tick "Có lắp đặt" muộn (sau khi phiếu đã xuất/hạch toán status 5) →
`need_repair` kẹt 0 cả ở PER lẫn dòng HĐ → getInstallableAvailableQty=0 → chặn tạo YCLD lắp đặt.
Scope theo PHIẾU (không cả HĐ). Chỉ 1 SP cần xuất.

- Tầng 1: phiếu YCXH `product_export_requests` id **33135** (PYCXH-33135, type=14, status=5) — need_repair 0→1.
- Tầng 2: dòng HĐ đã xuất `firm_contract_tab_products` id **244588** (prod **34011** 'Máy hàn MIG 250A, 3 pha (Kèm phụ kiện)', đã xuất 1) — need_repair 0→1.

### Task
- [x] Khảo sát prod erp_new: PER 33135 → fcid 21001, SP need_export=1 = [34011], FCTP 244588 (exp=1, nr=0), installable=0
- [x] Thêm method `fixInstallFlagPer33135_20260917($dryRun=true)` vào `database/seeds/UpdateDB.php` (khuôn Ca 39811, transaction + verify)
- [x] Dry-run qua tinker → Tầng1=1 [33135], Tầng2=1 [244588], installable 34011 = 1
- [x] User duyệt → chạy thật `(false)` → COMMIT; verify độc lập: PER 33135=1, FCTP 244588=1, installable=1

### Kết quả — 2026-09-17
Đã commit trên erp_new. installable prod 34011: 0 → 1 (hết chặn tạo YCLD lắp đặt).
Hoàn tác nếu cần:
`UPDATE product_export_requests SET need_repair=0 WHERE id=33135;`
`UPDATE firm_contract_tab_products SET need_repair=0 WHERE id=244588;`

---

## Case tiếp theo — HĐ fcid 21134 (Vinfast ĐT Bắc Giang) — 2026-09-28

> ⚠️ DB đích nay là **hrm_erp_gop (gộp DB production)** — hrm.eteksofts.com:33062 (không còn erp_new).

Cùng root cause: user tick "Có lắp đặt" muộn (phiếu đã xuất/hạch toán status 5) →
`need_repair` kẹt 0 cả ở PER lẫn dòng HĐ → getInstallableAvailableQty=0 → chặn tạo YCLD lắp đặt.
Scope theo PHIẾU (không cả HĐ). 3 SP cần xuất của phiếu.

- Tầng 1: phiếu YCXH `product_export_requests` id **37373** (PYCXH-37373, type=14, status=5) — need_repair 0→1.
- Tầng 2: dòng HĐ đã xuất `firm_contract_tab_products` (SP của phiếu, whx>0, nr=0):
  **241851** (prod 3967 'Thước đo độ sâu hoa lốp TMS-1450', whx 2),
  **241910** (prod 27874 'Máy hàn rút nhôm 220V, model 6100', whx 1),
  **241911** (prod 27869 'Máy hàn rút tôn 220V, model 9900S', whx 1) — need_repair 0→1.
- SP của phiếu (need_export=1) = [3967, 27874, 27869]. Các dòng HĐ khác của fcid 21134 GIỮ NGUYÊN.

### Task
- [x] Khảo sát prod hrm_erp_gop: PER 37373 → fcid 21134, SP need_export=1 = [3967,27874,27869], FCTP 241851/241910/241911 (whx>0, nr=0)
- [x] Thêm method `fixInstallFlagPer37373_20260928($dryRun=true)` vào `database/seeds/UpdateDB.php` (khuôn Ca 39811/33135, transaction + verify)
- [x] Dry-run qua tinker → Tầng1=1 [37373], Tầng2=3 [241851,241910,241911], installable 3967/27874/27869 = 2/1/1
- [x] User duyệt → chạy thật `(false)` → COMMIT; verify độc lập: PER 37373=1, FCTP 241851/241910/241911 = 1/1/1
- [x] Ghi kết quả + câu hoàn tác

### Kết quả — 2026-09-28
Đã commit trên hrm_erp_gop. installable prod 3967/27874/27869: 0 → 2/1/1 (hết chặn tạo YCLD lắp đặt).
Hoàn tác nếu cần:
`UPDATE product_export_requests SET need_repair=0 WHERE id=37373;`
`UPDATE firm_contract_tab_products SET need_repair=0 WHERE id IN (241851,241910,241911);`
