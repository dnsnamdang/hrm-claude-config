# Design (tóm tắt) — Check Xóa/Khóa danh mục chuyển ERP → HRM theo màn đang sử dụng

**Người phụ trách:** @junfoke — 2026-10-03 · **Nhánh:** `feat/catalog-usage-check` (từ `develop`, cả `hrm-api` + `hrm-client`,
worktree `.worktrees/catalog-usage`)

Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-10-03-catalog-usage-check-design.md`

## Mục tiêu
ERP cũ gần như không kiểm "danh mục đã được dùng chưa" trước khi Xóa/Khóa. Sau khi gộp DB, các màn danh
mục đã chuyển sang HRM phải chặn đúng theo **mọi màn (HRM + ERP) đang lưu tham chiếu** tới danh mục.

Nguồn khảo sát (gửi QA): `d:\CompanyProject\hrm\Ra soat danh muc ERP-HRM dang duoc su dung.xlsx` (chi tiết, có
bảng.cột) và `Danh muc ERP-HRM - man dang su dung (ban gon).xlsx` (4 cột, để gửi).

## Quyết định chính (chốt với user 03/10/2026)
1. **Xóa**: chặn khi đã được tham chiếu ở bất kỳ màn nào. Chặn ở BE; FE ẩn nút theo `is_can_delete`.
2. **Khóa**: CHỈ chặn khi còn **danh mục con đang Hoạt động** (Quốc gia → Khu vực/Tỉnh; Khu vực → Tỉnh;
   Tỉnh → Quận/Phường; Quận → Phường; Phường → Đường/phố; TK cha → TK con; Loại TK → TK; Ngân hàng → Chi nhánh).
   Chứng từ cũ KHÔNG chặn khóa (khóa chỉ ẩn khỏi dropdown). Chặn cả nút Khóa lẫn đổi trạng thái qua form Sửa.
3. **Bỏ qua Danh mục khách hàng**: cả HRM lẫn ERP không có Xóa; Khóa không có danh mục con.
4. Làm cả danh mục của @khoipv (Ngân hàng, TK ngân hàng, nhóm CSKH) — user đồng ý.
5. Helper dùng chung mới `app/Support/CatalogUsage.php` (`usedValues/isUsed`, tự bỏ qua bảng/cột không có ở
   DB). Entity giữ hằng `USAGE_REFERENCES`; cơ chế riêng đang chạy tốt (Province UNION, Currency USED_BY,
   Cost) chỉ bổ sung cột thiếu, không viết lại.

## Phạm vi thay đổi
| Danh mục | Xóa | Khóa |
|---|---|---|
| Quốc gia, Khu vực, Phường/xã | BE chưa chặn → thêm đủ tham chiếu + chặn BE | chặn khi còn con Hoạt động |
| Tỉnh/TP | thêm `delivery_contracts.identity_card_place` | chặn khi còn Quận/Phường Hoạt động |
| Quận/huyện | giữ | chặn khi còn Phường Hoạt động |
| Tài khoản | thêm ~20 cột chứng từ (theo id + theo SỐ TK) | chặn khi còn TK con Hoạt động |
| Loại tài khoản | giữ | nới: chỉ chặn khi còn TK **Hoạt động** |
| Tiền tệ | thêm `type_money_id` (7 bảng), `price_calculate*.currency`, `summary_shipping_prices` theo mã | giữ |
| Ngân hàng | thêm KH, nhân sự (mọi trạng thái), phiếu báo có/UNC/phiếu KT + chặn khi chi nhánh đã dùng | chặn khi còn chi nhánh Hoạt động |
| Vụ việc | thêm `bill_bonus_business.month_work_id/quarterly_work_id` | giữ |
| Nguồn vốn | danh sách đang rỗng → thêm 6 cột `source_of_capital` | giữ |
| Lỗi thiết bị | thêm `device_error_id` của 5 bảng dòng thiết bị | giữ |
| Serial (xóa ở Quản lý KH) | thêm `wr_import_result_extend_products`, serial thay thế `parent_id` | — |
| Đường/phố, Mã phí, TK ngân hàng, Gói/Cấp/Ghi chú bảo dưỡng, Chi phí | không đổi (đã đủ / không có Xóa) | — |
