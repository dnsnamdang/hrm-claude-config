# Design — Báo cáo phân chia thị trường

> Phụ trách: @junfoke · Tạo 2026-10-05 · nhánh `develop`
> Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-10-05-presale-division-market-report-design.md`

## Mục tiêu

Port báo cáo ERP *Kinh doanh › Báo cáo thị trường › Báo cáo phân chia thị trường* sang phân hệ
**CSKH trước bán**: tỉnh/xã nào do phòng ban, nhân viên nào phụ trách. Chỉ đọc.

## Quyết định chính (user 2026-10-05)

| Vấn đề | Chốt |
|---|---|
| Menu | `presale.js` nhóm "Báo cáo thị trường" (theo sheet KINH DOANH - TÀI CHÍNH) |
| Quyền | Thêm quyền xem id 1679 (ERP không có quyền) |
| Cột Hãng xe | Giữ như ERP |
| Lỗi lọc ERP | Sửa (Phụ trách hãng, Khu vực, GROUP BY) |

## Code

- BE: `Modules/Assign/Services/Report/DivisionMarketReportService.php` + `Http/Controllers/Api/V1/DivisionMarketReportController.php`
- FE: `pages/assign/report/division-market/`
- Quyền: `PermissionsTableSeeder` id 1679 + SQL chạy server
