# Danh mục gói bảo dưỡng (ERP → HRM) — design tóm tắt

> Phụ trách: @khoipv · Bắt đầu: 2026-08-04 · Nhánh: `gop_db` (cả 2 repo)
> Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-08-04-customer-care-services-catalog-design.md`

## Mục tiêu

Port màn ERP "Quản lý gói bảo dưỡng" (`admin/sale/services`, `Sale\ServiceController`, bảng
`services` 207 dòng + 5 bảng con ~9.500 dòng) sang HRM phân hệ **CSKH**, slot menu xám có sẵn
"Danh mục gói bảo dưỡng". 2 cổng chạy song song trên cùng bảng, KHÔNG đổi schema. Đây là màn
**lớn nhất** của phân hệ CSKH tới nay: ma trận nội dung bảo dưỡng × cấp dịch vụ, hệ số giá theo
công ty, hàng hoá liên quan, in phiếu, sao chép, export Excel, đính kèm S3.

## Quyết định đã chốt (user 2026-08-04)

1. **Port ĐẦY ĐỦ tính năng**: CRUD + In phiếu (template 191 `report_templates` chung) + Sao chép +
   Export Excel + File đính kèm S3 (giữ hành vi add-only như ERP).
2. **Quyền: 3 quyền HRM mới trong seeder** — ~~dùng lại 3 quyền ERP 101023–101025 + update tay
   type=24~~ (design cũ, user ĐỔI 2026-08-06 theo pattern màn `bank-account-catalog`):
   seeder thêm id **1126/1127/1128** `Thêm/Sửa/Xóa danh mục gói bảo dưỡng` (guard `api`,
   group `Danh mục dịch vụ bảo dưỡng`, type 24); DB local insert tay (KHÔNG chạy seeder —
   truncate) + copy grant role từ quyền ERP cùng tên; quyền ERP cũ revert `type = NULL`
   (ẩn khỏi màn Phân quyền HRM, role ERP cũ vẫn qua vì `CheckPermission` so theo TÊN).
   Danh sách/xem/in/export KHÔNG gate (như ERP). Chi tiết SQL: plan.md Task 5.8.
3. **Form tạo/sửa = trang riêng** (`create.vue` + `_id/edit.vue`), không nhét modal.
4. **Điều kiện xóa GIỮ NGUYÊN ERP**: chưa gắn hàng hoá + chưa có `service_quotation_items` → xóa
   thật; ngược lại chuyển Khóa. ⚠️ Rủi ro đã báo và user chốt bỏ qua: 6 bảng `wr_*` đang dùng
   `service_id` không được kiểm.
5. **Phương án A**: port bám sát ERP, chia 4 phase (BE → FE list → FE form → In/Export).

## Điểm kỹ thuật chính

- BE `Modules/CustomerCare` theo khuôn 4 màn CSKH có sẵn; routes `/v1/customer-care/services`;
  KHÔNG mysql2; `auth()->user()->id` là id nhân viên duy nhất (employees đã gộp).
- Logic giá (port nguyên): Giá vốn = đơn giá công (companies.work_price của công ty quản lý) ×
  định mức công × hệ số công nghệ → Giá công thức = giá vốn × hệ số giá bán gói → Giá bán cơ sở
  (nhập, default = giá công thức) → Giá bán theo công ty = giá cơ sở × hệ số công ty (pivot
  `company_service_coefficients`, công ty quản lý = 1).
- `saveServiceMaintain` port nguyên: delete-all-recreate maintains + maintainLevels; sync
  `service_levels` theo cột cấp của form; chặn bỏ cấp đã dùng ở báo giá dịch vụ.
- Lỗi ERP chủ động sửa: `vat_percent` thiếu numeric; catch Exception sai namespace; validate
  coefficient khi store; không port route debug `checkk`. Lỗi canDelete thiếu bảng `wr_*` GIỮ NGUYÊN
  theo quyết định user.
- FE đọc skill `button-convention`, `modal-popup`, `print-page` trước khi code; validate inline
  chuẩn CLAUDE.md; áp 4 bài học phân trang finance-account-catalog.
