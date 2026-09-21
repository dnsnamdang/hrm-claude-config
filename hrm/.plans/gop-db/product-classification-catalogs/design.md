# 6 danh mục quy hoạch lại hàng hóa (Redmine #11421)

> Nhánh: `feat/11421-danh-muc-quy-hoach-hang-hoa` (từ `gop_db`, cả 2 repo) · Phụ trách: @junfoke
> Bắt đầu 18/09/2026 · Nền tảng đọc trước: `.plans/gop-db/design.md`
> **Spec đầy đủ**: `docs/superpowers/specs/gop-db/2026-09-18-product-classification-catalogs-design.md`

## Mục tiêu

Dựng 6 danh mục mới trong phân hệ **Danh mục chung** (`master-data`) phục vụ việc quy hoạch lại
hàng hóa. Đợt này **chỉ làm danh mục**, chưa gắn hàng hóa vào cây mới.

| Danh mục | Bảng mới | Cấp cha |
|---|---|---|
| Tính chất hàng hóa | `product_natures` | — |
| Nhóm chức năng | `product_function_groups` | Tính chất hàng hóa |
| Nhóm sản phẩm | `product_families` | Nhóm chức năng |
| Loại sản phẩm | `product_types` (+ `product_type_attributes`) | Nhóm sản phẩm |
| Chính sách kinh doanh | `business_policies` | — |
| Đặc tính sản phẩm | `product_characteristics` | — |

## Quyết định lớn (user chốt 18/09/2026)

1. **Không đụng cây cũ** `scopes → chapters → job_groups → job_clusters` và bảng `groups` — ERP
   vẫn đang dùng. 6 bảng mới hoàn toàn độc lập.
2. Danh mục **để trống**, nghiệp vụ tự nhập; không seed 16 giá trị `products.product_type` fix cứng.
3. **Dùng chung toàn hệ thống**, không có `company_id`.
4. Giao diện **danh sách + modal thêm/sửa**, khuôn bắt buộc `pages/assign/customer-scopes/`.
5. Mẫu in barcode **giữ 6 mẫu fix cứng** của ERP, không tạo danh mục thứ 7.
6. Làm theo quy tắc chung chuyển ERP → HRM (`.claude/skills/erp-to-hrm-screen/SKILL.md`).

## Kết luận khảo sát đáng nhớ

- "Tính chất hàng hóa" bên ERP **chưa từng là danh mục** — là enum fix cứng ở cột
  `products.product_type` (16 giá trị đang dùng trên 44.288 hàng hóa).
- 3 trường **Thành phần / Cảnh báo an toàn / HDSD** của nhóm hàng hóa cũ đang được dùng để
  **in tem barcode** (`TanPhatDev/resources/views/barcode.blade.php:34,70,74`) → vẫn cần, bê sang
  Loại sản phẩm. Đây là câu chị Thúy hỏi trong tài liệu.
- Thuộc tính dùng lại bảng `attributes` (446 dòng), %VAT dùng lại `tax_rates` (40 dòng) — đều đã có
  sẵn trên `gop_db`.
- Trạng thái theo chuẩn HRM **1 = Hoạt động, 2 = Khóa** (ERP dùng 0/1 — không bê sang).

## Ngoài phạm vi đợt này

Gắn hàng hóa vào cây mới · TASK 2 popup lọc hàng hóa · TASK 3 màn Danh mục hàng hóa 6 tab ·
chuyển màn Nhóm hàng hóa cũ của ERP · lịch sử thay đổi (khuôn danh mục hiện tại không có).
