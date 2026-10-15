# Khai báo hạn mức công nợ khách hàng — design (tóm tắt)

> Người phụ trách: @khoipv · Nhánh: `develop` (con của `gop_db`) cả 2 repo
> Spec chi tiết: `docs/superpowers/specs/gop-db/2026-10-14-declare-limit-debts-design.md`

## Mục tiêu
Chuyển màn ERP "Khai báo hạn mức công nợ khách hàng" (`DeclareLimitDebt.index`, menu Kế toán › Kế toán Công nợ ›
Khách hàng › "Khai báo hạn mức công nợ KH") sang HRM: `/finance/declare-limit-debts`, gắn link vào mục menu đã khai sẵn
ở `components/subsystem-menu/finance.js`.

## Phạm vi
- Danh sách MỌI khách hàng (`customers.is_customer = 1`) dạng cây 2 tầng: dòng cha = khách hàng, dòng con = hạn mức
  theo từng công ty (Cách tính lãi · Hạn mức công nợ tính lãi · Hạn mức công nợ xuất hàng).
- Sửa THẲNG trong bảng ô của dòng công ty mình + nút Lưu từng khách (y ERP). Lịch sử (popup ở danh sách). Xuất Excel + Cấu hình cột.
- Không có màn chi tiết / thêm mới (ERP không có, dữ liệu gắn theo khách hàng).

## Quyết định (user chốt 14/10/2026)
1. **Kiểu màn**: sửa thẳng trong bảng + nút Lưu từng khách, y ERP (user đổi lại 14/10/2026 — trước đó chốt popup Sửa).
2. **Quyền**: 2 quyền HRM mới, tên y ERP, `type` 8 (Tài chính):
   - `Xem khai báo hạn mức công nợ khách hàng` → xem mọi công ty;
   - `Quản lý khai báo hạn mức công nợ khách hàng` → xem công ty mình (nếu không có quyền Xem) + sửa dòng công ty mình.
   - Không quyền nào → vẫn thấy menu + vào màn, xem mọi công ty, không sửa được (y ERP — user đổi lại 14/10/2026,
     trước đó chốt ẩn menu + 403).
3. **Giữ y ERP 2 hành vi lưu / hiện dòng** (dù là lỗi ERP):
   - Lưu = xoá TẤT CẢ dòng hạn mức của khách rồi ghi lại các dòng đang hiện → người chỉ có quyền Quản lý bấm Lưu làm
     mất dòng của công ty khác.
   - Khách đã có dòng thì chỉ hiện các dòng đã có; chưa có dòng nào mới hiện đủ các công ty người xem được thấy.
   - HRM KHÔNG tin giá trị FE gửi cho dòng công ty khác: BE dựng lại tập dòng đang hiện từ DB, chỉ thay dòng công ty mình
     bằng giá trị gửi lên (kết quả y ERP khi không ai sửa request).

## Thành phần
- BE: `Modules/Finance/Services/CustomerDebt/DeclareLimitDebtService.php`, `Http/Controllers/V1/DeclareLimitDebtController.php`,
  route `finance/declare-limit-debts` (`/`, `/meta`, `/export-rows`, `/customers/{id}`, `PUT /customers/{id}`).
  Lịch sử: `catalog_histories` khoá ảo `customer_limit_debts`, `table_id` = id khách hàng, cột ảo `company_rows`.
- FE: `pages/finance/declare-limit-debts/index.vue` (1 file).
  Khuôn: `pages/finance/report-limit-debts` (danh sách), `pages/finance/prepick-stocks` (nền dòng con).
- Quyền: `PermissionsTableSeeder` id 1707 / 1708. Không migration.
