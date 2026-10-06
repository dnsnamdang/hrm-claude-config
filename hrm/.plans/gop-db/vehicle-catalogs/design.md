# 5 danh mục Xe (port ERP → HRM)

> Nhánh: `gop_db` (cả 2 repo) · Phụ trách: @namdangit · Bắt đầu 22/09/2026
> Nền tảng đọc trước: `.plans/gop-db/design.md` · Khuôn màn: `.plans/gop-db/product-classification-catalogs/`
> **Spec đầy đủ**: `docs/superpowers/specs/gop-db/2026-09-22-vehicle-catalogs-design.md`

## Mục tiêu

Chuyển 5 danh mục xe từ ERP sang HRM, gom vào **một nhóm menu "Danh mục xe"** của phân hệ
**Danh mục chung** (`/master-data/...`) — đúng chỗ ERP đang đặt (menu `Danh mục → Xe`).

| Màn HRM | Route | Bảng (dùng lại của ERP) | Cấp cha | Dòng |
|---|---|---|---|---|
| Danh mục hãng xe | `/master-data/vehicle-manufacts` | `vehicle_manufacts` | — | 55 |
| Danh mục dòng xe | `/master-data/vehicle-categories` | `vehicle_categories` | — | 11 |
| Danh mục phân loại xe | `/master-data/vehicle-brands` | `vehicle_brands` | Hãng xe | 322 |
| Danh mục model xe | `/master-data/vehicle-models` | `vehicle_models` | Hãng xe + Phân loại xe | 1.281 |
| Danh mục đời xe | `/master-data/vehicle-life` | `vehicle_life` | — | 61 |

## Quyết định đã chốt (user chốt 22/09/2026)

1. **Dùng lại bảng ERP**, không tạo bảng mới — dữ liệu thật đang chạy, ERP vẫn đọc chung.
2. **Thêm cột `code`** vào cả 5 bảng + sinh mã cho dữ liệu cũ (`HX.` / `DX.` / `PLX.` / `MDX.` / `DOX.`
   + 4 ký tự) để bám đúng khuôn `product-natures` (cột Mã là cột link mở popup).
3. **Trạng thái: DB giữ nguyên quy ước ERP (`1` hoạt động / `0` khóa), KHÔNG sửa dữ liệu cũ**
   (user chốt lại 22/09/2026). HRM ánh xạ `0 ⇄ 2` ngay ở `BaseVehicleCatalogModel` nên khuôn
   dùng chung vẫn nói chuẩn HRM 1/2. Bảng `vehicle_life` được **bổ sung cột `status`** (mặc định 1).
   Lý do không đổi 0 → 2: màn Dòng xe của ERP validate `status => in:0,1`, gặp giá trị 2 thì ô
   Trạng thái hiện trống và lần lưu sau ép về 0/1.
4. **Xóa: chặn khi đang được dùng** — còn danh mục con HOẶC còn bản ghi nghiệp vụ tham chiếu
   (`products`, `vehicles`, hợp đồng vận chuyển…) thì ẩn nút Xóa, BE trả
   `Không thể xóa do dữ liệu đang được sử dụng.` Muốn ẩn khỏi danh sách thì dùng **Khóa**.
5. **Đủ Xuất Excel + Import** cho cả 5 màn (ERP chỉ có import ở màn Model xe).
6. Tái sử dụng nguyên bộ `Base*` của `ProductClassification` (Model/Controller/Service/Request/
   Resource) — không viết CRUD mới.
7. **Ghi chú**: 3 bảng có sẵn cột `note` (Hãng xe / Phân loại xe / Model xe) → giữ ô "Ghi chú";
   2 bảng còn lại (Dòng xe, Đời xe) ERP không có ghi chú → **không thêm ô**.
   FE/BE vẫn dùng khóa `description`, Entity ánh xạ `description ⇄ note` bằng accessor/mutator
   để không phải sửa lớp `Base*` dùng chung.
8. **Quyền**: tạo mới 10 quyền (`Xem/Quản lý danh mục <tên>`), group `Danh mục xe`, type 9,
   id 1590–1599. Quyền ERP cũ (`Quản lý dòng xe`) giữ nguyên, không đụng.
9. **Không phân quyền theo cấp** (công ty/phòng ban) — danh mục dùng chung toàn hệ thống,
   giống 6 danh mục hàng hóa.

## Kết luận khảo sát đáng nhớ

- "Danh mục phân loại xe" bên ERP là bảng **`vehicle_brands`** (không phải `vehicle_categories`),
  còn "Danh mục dòng xe" mới là `vehicle_categories`. Đặt nhầm là hỏng cả cây cha–con.
- `products.model_id` trỏ tới **`vehicle_models`** (38.776 hàng hóa) — đây là lý do phải chặn xóa.
- `vehicle_categories` có hook đồng bộ CRM (`CRMVehicleCategoriesService`) ở ERP, chỉ chạy khi
  `services.mate.use_crm` bật. Bên HRM **không port hook này** (ghi thẳng DB gộp).
- 4 bản ghi đang `status = 0` là bản ghi ERP đã "xóa mềm" → sau migration hiện là **Khóa**.
- Một số cột khóa ngoại dùng để kiểm tra "đang sử dụng" chưa có index → migration thêm index.

## Ngoài phạm vi đợt này

Màn "Danh mục xe" (`vehicles`), "Danh mục biển số xe", "Danh mục tải trọng xe", "Danh mục lái xe
ngoài" · gắn danh mục xe vào màn Hàng hóa · đồng bộ CRM.
