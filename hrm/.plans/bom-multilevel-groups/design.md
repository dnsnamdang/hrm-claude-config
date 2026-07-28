# Design (tóm tắt): Nhóm hàng 2 cấp + kéo-thả cho BOM

> Spec đầy đủ: `docs/superpowers/specs/2026-07-17-bom-multilevel-groups-design.md`

- **Phụ trách**: @manhcuong · **Ngày**: 2026-07-17
- **Phạm vi**: CHỈ BOM Giải pháp (`/assign/bom-list`). KHÔNG làm Báo giá (làm sau).
- **Feature liền trước**: `bom-import-export-copy` — feature này **viết đè** một phần import/export/template/validate của nó.

## Mục tiêu
Nhóm hàng từ **phẳng 1 cấp** → **2 cấp** (cha/con), đồng bộ Import/Export/UI + **kéo-thả** sắp xếp nhóm.

## 6 quyết định chốt (brainstorming)
| # | Vấn đề | Chốt |
|---|---|---|
| 1 | Số cấp nhóm | **2 cấp** (Cấp 1 + Cấp 2) — theo file template, dù task text nói "cây" |
| 2 | Template | **14 cột mới** (`Import_bomlist_Task_10790`), thay 12 cột feature trước |
| 3 | Cha-con hàng hoá | Cột **`Mã hàng cha`** (nearest-above cùng nhóm lá), thay STT parsing |
| 4 | Kéo-thả | Đổi thứ tự **trong cùng cấp** (anh em), con theo cha. Không re-parent, không kéo hàng hoá |
| 5 | AC2 in/export | **Chỉ Export Excel** (BOM không có In PDF) |
| 6 | Kiểu export | **Round-trip 14 cột** (2 cột nhóm cha/con), nạp lại được |

## DB
1 migration: `bom_list_groups` + `parent_id` (nullable, không FK, không transaction). `parent_id NULL`=Cấp 1, có=Cấp 2. `sort_order` đổi nghĩa: thứ tự trong cùng cấp cùng cha. Nhóm cũ → tự động Cấp 1 (an toàn, không backfill).

## Phát hiện khảo sát
- **`vuedraggable ^2.24.3` CÓ SẴN** — kéo-thả khả thi, không thêm dependency.
- **BOM không có In PDF** — chỉ Export Excel (2 blade: `bom_list.blade.php` báo cáo La Mã dùng chung Quotation; `bom_list_import_format.blade.php` round-trip BOM-only). Chỉ đụng blade round-trip.
- **Mã hàng KHÔNG duy nhất trong BOM** (verify: `bom3/GC-GC-40PRO-A:06` x2) → nối cha-con bằng **nearest-above cùng nhóm lá**, không dùng "mã == X" đơn thuần.

## Đụng gì feature trước
Viết đè: `validateImportData` (14 cột + luật nhóm/Mã hàng cha), `importProducts` (nhóm 2 cấp), `importTemplate`, export blade, `BomImportModal.vue`, `syncGroups` (2 pass). Thêm: migration, FE tree + drag-drop. Giữ nguyên: 3 nhánh Mã hàng, Master Data, dịch vụ, pending, Copy (chỉnh cho khớp nhóm 2 cấp).

## AC
- AC1: tạo nhóm con dưới nhóm đã có
- AC2: export Excel hiển thị đúng phân cấp (2 cột nhóm cha/con)
- AC3: import Excel cha-con nhóm → thành công + hiển thị đúng
- AC4: kéo nhóm 3→1 → UI đổi ngay; Lưu → reload giữ thứ tự

## Ngoài scope
Báo giá · nhóm 3+ cấp · In PDF BOM · re-parent/kéo hàng hoá · `bom_list.blade.php` (Quotation dùng chung).
