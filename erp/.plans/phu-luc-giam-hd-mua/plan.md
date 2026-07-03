# Phụ lục giảm HĐ mua — Implementation Plan

> Scope ĐÃ ĐÍNH CHÍNH (xem design.md): phụ lục giảm phần lớn đã tồn tại. Việc thực = 2 phần.
> Verify = `php -l` + tinker + browser (repo không dùng test tự động). Nhánh: chốt với user (đang ở `master`). KHÔNG commit khi chưa yêu cầu.

---

## PHẦN A — Nhập khẩu: bổ sung BE-validate sàn — XONG (2026-06-29)

`BuyContractAnnex2` đã có sẵn (menu/màn/duyệt/trừ available_qty) nhưng `store()`/`update()` KHÔNG validate sàn → giảm có thể vượt SL đã về (chỉ FE chặn).

- [x] Thêm `validateReduceQty()` vào `BuyContractAnnex2Controller`: mỗi dòng `products[].details[]`, SL giảm ≤ `buy_contract_product_detail2.qty − arrived_qty − annex_qty` (sàn = đã về). Trả `errors[products.X.details.Y.qty]` + message; FE đã có `$scope.errors`+toastr.
- [x] Gọi trong `store()` và `update()` (sau Validator, trước DB::beginTransaction).
- [x] import `BuyContractProductDetail2`. `php -l` sạch (+44 dòng).
- [ ] User test browser: tạo phụ lục giảm vượt SL đã về → bị chặn; hợp lệ → qua. (chưa commit)

---

## PHẦN B — Build phụ lục giảm cho `InlandBuyContractNew` (hãng + tự do) — CHƯA LÀM

`InlandBuyContractNew` (đời mới, `HOP_DONG_TU_DO=1`/`HOP_DONG_HANG=2`) **chưa có** phụ lục giảm. Đời cũ `InlandBuyContract` có `InlandBuyContractAnnex2` → **dùng làm khuôn mẫu mirror, đổi đích sang `InlandBuyContractNew`**.

**Khuôn mẫu chính:** `InlandBuyContractAnnex2Controller` + model `InlandBuyContractAnnex2`/`InlandBuyContractProductAnnex2`/`InlandBuyContractProductDetailAnnex2` + views `orders/inland_buy_contract_annex2/` + routes web.php:2531–2546. Hành vi giảm: approve → `annex_qty += qty; available_qty -= qty` trên dòng HĐ; sàn = đã về.

### Tasks (cần đọc kỹ khuôn mẫu trước khi code từng task)
- [x] **B0 — Khảo sát (XONG):** SP HĐ New = `inland_buy_contract_new_products` (id, product_id, qty, **annex_qty, available_qty, arrived_qty**, arriving_qty) + `inland_buy_contract_new_product_details` (id, product_id, qty, **arrived_qty, annex_qty, available_qty**, is_arrived_notify). **Đã có sẵn annex_qty/available_qty/arrived_qty → KHÔNG migration bảng SP.** "Đã về" = `arrived_qty`. Khuôn mẫu: `InlandBuyContractAnnex2Controller` + 3 bảng `inland_buy_contract_annex2`/`_product_annex2`/`_product_detail_annex2`. Bảng annex mới đề xuất: `inland_buy_contract_new_annex` (+`_product_annex`, `_product_detail_annex`), FK → `inland_buy_contract_news`. Nhánh feature: `phu-luc-giam-hd-mua`.
- [x] **B1 — Migration (XONG, chưa migrate):** `2026_06_29_000001_create_inland_buy_contract_new_annex_tables.php` tạo 3 bảng `inland_buy_contract_new_annex` / `_product_annex` / `_product_detail_annex` mirror annex2 cũ, FK đời mới, Laravel 6 bigIncrements. php -l sạch.
- [x] **B2 — Models (XONG):** `InlandBuyContractNewAnnex` (+ `InlandBuyContractNewProductAnnex`, `InlandBuyContractNewProductDetailAnnex`) mirror annex2 cũ, `contract()→InlandBuyContractNew`, syncDetails/approve/getData…; bỏ promotion (đời mới chưa có). php -l sạch.
- [x] **B3 — Controller (XONG):** `InlandBuyContractNewAnnexController` mirror đầy đủ (index/searchData/forApprover/create/store/show/edit/update/approve/print/printExtraContent/cancel/delete). Delta: `validateReduceQty` (sàn `discount_qty ≤ qty − arrived_qty − annex_qty` trên `inland_buy_contract_new_product_details`) ở store+update; approve trừ `annex_qty += discount_qty`, `available_qty = max(0, …)` trên cả `inland_buy_contract_new_products` + `_details`. Bỏ promotion. php -l sạch. **CHƯA review kỹ.**
- [x] **B4 — Routes + Permission + Menu (XONG):** 13 route group `inland_buy_contract_new_annexs` (name `inlandBuyContractNewAnnex.*`, checkPermission ở create/store/approve); permission id 1038 "Lập phụ lục giảm hợp đồng mua hàng trong nước" + 1039 "Duyệt..." (group Đặt hàng trong nước); menu topmenubar dòng 1719. php -l sạch. (Verify id permission không trùng ở B7.)
- [x] **B5 — Views (XONG):** 10 file `orders/inland_buy_contract_new_annex/` (index/approver_index/create/edit/show/form/formJs + 3 partial JS class) mirror; sàn hiển thị (SL HĐ/đã về/tối đa giảm), cap `discount_qty ≤ available`, inline `errors[products.X.details.Y.discount_qty]`; bỏ promotion. Endpoint HĐ đời mới (`searchData`/`getData`/`getDataProduct`) đã verify TỒN TẠI (route 2816/2828/2834).
- [x] **B6 — Nút (XONG):** "Tạo phụ lục giảm" trên `inland_buy_contract_new/show.blade.php` (hiện khi status=1=DA_DUYET, truyền `?contract_id`).
- [~] **B7 — Verify (code XONG, browser còn lại):**
  - [x] Migrate dev: 3 bảng `inland_buy_contract_new*annex` đã tạo (chỉ migrate file này).
  - [x] Permission id 1038/1039 không trùng (1037 là max cũ).
  - [x] Review controller: validate sàn đúng; approve trừ annex_qty/available_qty cả 2 bảng + guard max(0,...). OK.
  - [x] **FIX 2 bug FE detail (B5)**: (1) getter `available_qty` trùng cột server → constructor crash → thêm `no_set:['available_qty']`; (2) submit `inland_buy_contract_new_product_detail_id` undefined khi tạo mới (getDataForAnnex trả `id`/`inland_buy_contract_new_detail_id`) → sửa fallback `|| inland_buy_contract_new_detail_id || id` (nếu không BE validate sàn bị bỏ qua).
  - [ ] **User**: insert/gán 2 permission 1038/1039 cho role; browser test: tạo phụ lục giảm hãng+tự do / giảm vượt đã về bị chặn / duyệt trừ SL đúng + không âm / nút trên màn HĐ.
  - [ ] Commit khi user duyệt (cả Part A + Part B trên nhánh `phu-luc-giam-hd-mua`).

### Self-review (sẽ chạy sau khi viết đủ task B)
- Coverage: hãng + tự do đều tạo được; sàn = đã về enforce cả BE; approve trừ đúng + chặn âm.

---

### Checkpoint — 2026-06-29
Vừa hoàn thành: **Phần A** (BE-validate sàn nhập khẩu) code xong, php -l sạch, chưa commit. Đính chính scope (phụ lục giảm phần lớn đã có; chỉ thiếu đời InlandBuyContractNew).
Đang làm dở: Phần B chưa bắt đầu (mới có khung task, cần B0 khảo sát trước khi code).
Bước tiếp: User (1) test browser Phần A; (2) chốt có build Phần B ngay không + nhánh. Nếu build → chạy B0 khảo sát rồi subagent-driven theo B1–B7.
Blocked: (trống)
