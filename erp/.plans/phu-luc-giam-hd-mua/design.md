# Phụ lục giảm cho HĐ mua (giảm số lượng)

> **⚠️ ĐÍNH CHÍNH (2026-06-29) — phụ lục giảm HĐ mua PHẦN LỚN ĐÃ TỒN TẠI.** Khảo sát ban đầu (Explore agent "chưa có") SAI. Scope thực tế:
> - **Nhập khẩu** (`BuyContract2`) → ĐÃ CÓ `BuyContractAnnex2` (menu, màn, duyệt, trừ `available_qty`). **Logic cần verify**: `store()` KHÔNG validate sàn/SL giảm (chỉ status/code/contract), `approve()` trừ available_qty không chặn âm → sàn "đã về" chỉ dựa FE, BE không chặn.
> - **Trong nước ĐỜI CŨ** (`InlandBuyContract`) → ĐÃ CÓ `InlandBuyContractAnnex2`.
> - **Trong nước ĐỜI MỚI** (`InlandBuyContractNew`, hãng + tự do) → **CHƯA CÓ** (đây là phần thật sự cần build).
>
> → Việc thực: (A) Verify + có thể bổ sung BE-validate sàn cho **nhập khẩu**; (B) **Build** phụ lục giảm cho `InlandBuyContractNew` (hãng+tự do). Design "build cả 2 họ" bên dưới chỉ áp cho phần B; nhập khẩu KHÔNG build lại. **Chờ user chốt hướng.**

## Mục tiêu
Thêm luồng **phụ lục GIẢM số lượng** cho HĐ mua (hiện chỉ có phụ lục bổ sung), mirror hành vi `FirmContract::PL_GIAM` bên bán. Phủ 3 loại: nhập khẩu, trong nước theo hãng, trong nước tự do.

## Quyết định đã chốt (Q&A brainstorm)
- **Q1 — giảm cái gì:** A = **giảm số lượng** hàng hoá (không phải giảm giá).
- **Q2 — sàn (SL sau giảm không nhỏ hơn):** B = **SL đã về / đã thông báo về hàng**.
- **Q3 — phạm vi:** A = làm **cả 2 họ** (nhập khẩu + trong nước hãng/tự do) trong feature này, 1 spec, 2 phase.
- **Q4 — tác động khi duyệt:** A = **chỉ hạ SL hiệu lực HĐ**; "SL còn phải về/nhập" tự tính lại. Không đụng công nợ/order summary. **"Tương tự HĐ hãng"** (mirror PL_GIAM bên bán).

## Khuôn mẫu tham chiếu — `FirmContract::PL_GIAM` (bên bán)
- PL_GIAM=3 là 1 loại bản ghi phụ lục (FirmContractAnnexesController + FirmContractAnnexService).
- "SL được phép giảm" mỗi mã = `GREATEST(qty − (exported_qty + returned_qty) − reserved, 0)` (sàn = đã xuất). Buy: sàn = đã về.
- Khi duyệt → trừ thẳng `quantity` mã trên HĐ gốc (FirmContractAnnexService ~dòng 544–556), floor 0.
- Có duyệt: status 3→2→1.

## Design (đã trình, chờ duyệt)

### 1. Mô hình chung
- Phụ lục giảm = bản ghi phụ lục loại "giảm", chứa mã + **SL giảm** mỗi mã.
- Duyệt: `3 Đang tạo → 2 Chờ duyệt → 1 Đã duyệt`.
- **SL được phép giảm mỗi mã** = `qty_HĐ_hiện_tại − SL_đã_về`. Validate: SL giảm ≤ phần này; giảm ≤ 0 invalid.
- **Khi DUYỆT** → `qty_mới = qty − SL_giảm` (sàn = đã về). SL còn phải về/nhập tự tính lại. Không cập nhật gì khác (phương án A).

### 2. Cấu trúc theo họ (2 phase)
- **Phase 1 — Nhập khẩu** (`BuyContract2`): phụ lục dùng entity `BuyContractAnnex2` (bảng `buy_contract_annex2`, link `buy_contract_id`, status 1/2/3, products + `total_decrease`). **CHỐT A: thêm cột `type` vào `buy_contract_annex2`** (vd `BO_SUNG=1`, `GIAM=2`; mặc định BO_SUNG cho data cũ) — dùng chung entity/controller/màn, rẽ nhánh theo `type`. Sàn = SL đã thông báo về hàng (`ProductArrivedNotify2`/`OrderNotification`).
- **Phase 2 — Trong nước hãng + tự do** (`InlandBuyContractNew`): thêm 2 loại `PHU_LUC_HANG_GIAM`, `PHU_LUC_TU_DO_GIAM` (mirror `PHU_LUC_HANG=4`/`PHU_LUC_TU_DO=5`), `parent_id` trỏ HĐ. Sàn = SL đã về (`InlandProductArrivedNew`). 1 lần làm phủ cả hãng & tự do.

### 3. FE / quyền
- Mỗi họ: nút "Tạo phụ lục giảm" trên màn HĐ + form chọn mã & nhập SL giảm (hiện SL HĐ, đã về, tối đa giảm được), inline validate. Route/permission theo pattern phụ lục bổ sung.

### 4. Edge cases
- Giảm vượt `(qty − đã về)` → chặn (FE + BE rethrow ValidationException).
- HĐ đã huỷ/đóng → không cho tạo phụ lục giảm.
- Nhiều phụ lục giảm cùng mã → cộng dồn không vượt; mỗi lần duyệt trừ tiếp trên qty hiện tại.
- Phụ lục giảm chờ duyệt → chưa trừ qty (chỉ trừ khi duyệt).

## Quyết định đã chốt (điểm mở cũ)
- **Cấu trúc Phase 1 (nhập khẩu): CHỐT A** — thêm cột `type` (BO_SUNG/GIAM) vào `buy_contract_annex2`, dùng chung entity/controller/màn, rẽ nhánh theo `type`. Migration thêm cột nullable/default BO_SUNG để data cũ an toàn.

## Bối cảnh code đã khảo sát (để tiếp nhanh)
- Nhập khẩu: `BuyContract2` (const `HOP_DONG=1`, `PL_BO_SUNG=2`), entity phụ lục `BuyContractAnnex2` (`buy_contract_annex2`), controller `Order/BuyContractAnnex(2)Controller`, route prefix `buy_contract_annexs` (web.php:2396). SP HĐ: `buy_contract_product_detail2.qty`.
- Trong nước: `InlandBuyContractNew` (`HOP_DONG_TU_DO=1`, `HOP_DONG_HANG=2`, `DON_HANG=3`, `PHU_LUC_HANG=4`, `PHU_LUC_TU_DO=5`), controller `Order/InlandBuyContractNewController` (store dòng ~138, nhánh phụ lục ~219/245), route prefix `inland_buy_contract_annexs` (web.php:2509).
- Bên bán mẫu: `FirmContractAnnexesController` + `FirmContractAnnexService` (PL_GIAM logic, "SL giảm được" dòng ~97, trừ qty ~544–556).
- "Đã về": nhập khẩu `OrderNotification`/`ProductArrivedNotify2` (có qty); trong nước `InlandProductArrivedNew*`.
