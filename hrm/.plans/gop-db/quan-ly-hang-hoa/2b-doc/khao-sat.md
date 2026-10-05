# Đợt 2-B — Đọc (4 màn danh sách + form chỉ xem): khảo sát

> 04/10/2026 · @namdangit · chưa đụng source.
> Tài liệu nguồn cùng thư mục: `mockup-inventory.md` (kiểm kê mockup chốt) · `tai-su-dung-nhanh-cu.md` (code nhánh cũ `feat/p1-danh-muc-hang-hoa`).

## 1. Phạm vi 2-B (theo sổ chốt §2c)

API + FE **chỉ đọc** cho: Kho dữ liệu hàng hoá (`sc-tong`) · Dữ liệu hàng hoá công ty (`sc-kho`) ·
Hàng hoá nhập thông tin (`sc-l1`) · Hàng đang kinh doanh (`sc-l3`) · form hàng hoá ở chế độ chỉ đọc.
Mọi nút [GHI] (Lấy về, Tạo mới, Sửa, Sao chép, Xoá, Xây dựng catalog, Xếp vào tiểu mục) để 2-C;
Tính giá / Lập yêu cầu tính giá để phase Tính giá; Xuất Excel để 2-E.

## 2. Số đo mockup (chi tiết `mockup-inventory.md`)

| Màn | Cột (hiện sẵn) | Lọc | Ghi chú |
|---|---|---|---|
| Kho dữ liệu | 26 (15) | công tắc "Chỉ hàng công ty chưa dùng" + 10 ô | mọi công ty, không cần quyền |
| Dữ liệu hàng hoá công ty | 27 (15) | 4 ô catalog dây chuyền + công tắc "Chỉ hàng chưa xếp catalog" + 12 ô | quyền 1652 HOẶC 1653 |
| Hàng hoá nhập thông tin | 26 (13) | 11 ô | quyền 1652 |
| Hàng đang kinh doanh | 26 (14) | 4 ô catalog + công tắc + 11 ô; dòng nhắc cam đếm hàng chưa xếp catalog | không cần quyền; không có cột Giá vốn |
| Form | 2 tab cha, 5 tab con: Thông tin chung 19 trường · Thông số KT 5 + 5 bảng · Mua hàng 8 · Quản trị 6 + catalog · Phân loại xe 4 + bảng · Nhóm máy 1 + bảng | — | chỉ đọc: khoá mọi ô, ẩn nút (§35b-3) |

Mockup có 16 điểm mơ hồ (mục 7 file kiểm kê) — điểm thuần UI sẽ tự chốt theo khuôn và ghi lại.

## 3. Tái sử dụng nhánh cũ (chi tiết `tai-su-dung-nhanh-cu.md`)

- Lấy lại (có sửa): Entity `Product` + 13 bảng con (→ `BaseModel`, bỏ `product_type_id`/`product_characteristic_id`,
  bỏ `ProductCompanyCoefficient` trùng `ProductCompany` 2-A, `ProductSupplier` + `company_id`), `ProductService`
  index/show (5 query, không N+1), `ProductOptionService` (form-options 14 danh mục, `include_ids`/`is_locked`).
- Viết lại: 2 Resource list/detail (bỏ tab Giá bán, `rate_liquidation` (F8), `admin_data` đọc cột chung, lọc Công ty quản lý).
- Bỏ: quyền 1616–1619, khối 17 route, migration drop `can_retail`, toàn bộ FE (mockup Vue 21/09 lỗi thời).
- Nhánh cũ **không có test** cho list/detail/form-options/gate giá ⇒ 2-B tự viết, đủ ca có quyền + không quyền.

## 4. Câu chặn cần user chốt

| # | Câu | Vì sao chặn |
|---|---|---|
| Q1 | Hàng cũ chưa có dòng trạng thái (K1) thì 3 màn theo trạng thái hiện gì | không có dòng ⇒ Nhập thông tin / Đang kinh doanh / Dữ liệu công ty **trắng**; cột "Công ty đang kinh doanh" ở Kho dữ liệu cũng trắng |
| Q2 | Quyền gate giá vốn: `Xem giá vốn hàng hoá` (api, id 1092 — HRM đang dùng ở báo giá/BOM) hay đọc chéo `Quản lý giá` (web ERP, nhánh cũ làm) | tài liệu ghi "Quản lý giá" nhưng đó là quyền guard `web` |
| Q3 | 2 cột phân loại `products.product_type_id` / `product_characteristic_id` (spec 21/09) — thêm ở 2-B hay 2-C | nhánh chung chưa có; dữ liệu cũ đều rỗng (chưa quy đổi — sổ chốt §5-1) |
| Q4 | Quyền seed ở 2-B: 1652 *Xây dựng thông tin* + 1653 *Xem dữ liệu* (gate vào màn); 1654/1655 để đợt dùng | id 1652–1656 còn trống cả seeder lẫn DB (đo 04/10) |

## 5. Chốt (04/10/2026)

| # | Chốt |
|---|---|
| Q1 | **Suy ra trạng thái lúc đọc**, không ghi DB: hàng `products.status = 1` chưa có dòng trạng thái ⇒ coi là *Đang kinh doanh* của **công ty tạo** (`products.company_id`). Chỉ công ty tạo — chi nhánh có dòng hệ số cũ KHÔNG được suy ra. Gỡ nhánh suy ra khi phase giá backfill thật. Gom điều kiện vào 1 chỗ (scope Entity) để gỡ 1 lần |
| Q1b | Màn *Hàng hoá nhập thông tin*: **BỎ cả cột Giá vốn và Giá bán lẻ** (kể cả trong Cấu hình cột) — hàng chưa qua tính giá thì chưa có giá; mockup sót vì 4 màn dùng chung bộ 28 cột. Giá vốn chỉ còn ở *Dữ liệu hàng hoá công ty* (tắt sẵn) + form |
| Q2 | 🔄 **Ẩn HOÀN TOÀN giá khỏi các màn hàng hoá** (user 04/10: *"giá sẽ chỉ quản lý ở các màn quản lý giá riêng biệt"*) ⇒ 4 màn danh sách + form KHÔNG có cột/ô Giá vốn, Giá bán lẻ; API list/detail **không trả trường giá** (không cần gate quyền giá vốn ở 2-B). Thay Q1b. Câu hỏi quyền giá vốn chuyển sang Phase 8 (Quản lý giá) |
| Q3 | **Thêm 2 cột phân loại trong 2-B**: `products.product_type_id` + `product_characteristic_id` nullable + index, KHÔNG FK (spec 21/09); dữ liệu cũ NULL tới khi quy đổi (sổ chốt §5-1). DB local đã có 2 cột từ nhánh cũ ⇒ migration guard `hasColumn` |
| Q4 | (theo §35b, không hỏi lại) seed **1652** *Xây dựng thông tin hàng hoá* + **1653** *Xem dữ liệu hàng hoá công ty* ở 2-B vì 2 màn gate theo chúng; 1654/1655 seed ở đợt dùng tới |
