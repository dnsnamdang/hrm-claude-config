# Final whole-branch review — xuat-ban-hang-muon Phase 2 (phiếu BÁN thực tế, BorrowSell / PXBHM-)

Giao tiếp tiếng Việt. Bạn là REVIEWER cuối cùng của toàn bộ Phase 2. KHÔNG sửa code, KHÔNG spawn subagent, KHÔNG git mạng. Chỉ đọc + báo cáo findings.

## Nhánh & phạm vi
- Repo: hrm-api (`gop_db`) + hrm-client (`gop_db`). DB gộp `erp_hrm_check`.
- 3 gói diff (ĐỌC CẢ 3):
  1. `.plans/gop-db/xuat-ban-hang-muon/sdd/final-review-be-committed.txt` — BE đã commit (10 commit, range c562527e0^..HEAD): 6 entity BorrowSell, ActivityHasDeliveryTrip, tách SupportAccountingTrait (Hướng A), BorrowSellPostingService (nhánh Firm 157 + WrService 1561×coef + chiết khấu 5211 + chuyến xe 6427/3351), BorrowSellService::store (1 transaction), StoreBorrowSellRequest, BorrowSellController + routes + 3 Resource, tests.
  2. `.plans/gop-db/xuat-ban-hang-muon/sdd/final-review-be-uncommitted-objectable.txt` — 1 delta additive (objectable_id/type vào BorrowSellRequestDetailResource).
  3. `.plans/gop-db/xuat-ban-hang-muon/sdd/final-review-fe-worktree.txt` — FE working-tree (uncommitted đúng quy ước Phase 1 FE): menu link, nút "Lập phiếu bán", folder `pages/finance/borrow-sells/**` (api.js, index list, create+BorrowSellForm, _id/index chi tiết 2 tab, _id/print).

## Spec authority
- Plan: `docs/superpowers/plans/2026-09-07-xuat-ban-hang-muon-phase2.md` (đọc để đối chiếu spec).
- Design chi tiết: `docs/superpowers/specs/gop-db/` (nếu cần tra bút toán).

## Global constraints (binding — bất kỳ vi phạm nào = finding)
1. **FULL accounting scope**; port toàn bộ 4 màn FE.
2. **Hướng A đã duyệt**: được sửa SupportAccountingTrait (tách từ ProductExportPostingService). Kiểm: extraction KHÔNG đổi hành vi bút toán xuất-hàng-thường (regression). `vatExtraCostAccounting` = TNCN, tên giữ nguyên.
3. **Tiền tính ở BE, FE gửi qty-only** (Ruling T8-payload): payload `{borrow_sell_request_id, products:[{objectable_id, objectable_type, details:[{product_export_request_detail_id, qty}]}]}`. FE KHÔNG gửi field tiền.
4. **Cờ quyền FE fail-closed** — KHÔNG hardcode `= true` (pattern cấm `can[A-Za-z]*\s*=\s*true`). List gate 4 cấp qua `BorrowSell::searchByFilter`; detail/print gate `is_can_view`; create gate "Kế toán kho" qua `userCanCreate()`. KHÔNG có route edit/delete/approve.
5. **BE rethrow ValidationException** (không catch chung Exception).
6. **Bỏ nhánh KM (HANG_KM)** — chỉ hàng thường. Suy loại HĐ firm/service từ `contractable_type`.
7. **Giá vốn nhánh**: Firm → Có **157**, cost = Σ export_price×qty (KHÔNG nhân unit_coefficient); WrService → Có **1561** ×unit_coefficient + chiết khấu 5211 (work CKHH=20).
8. **KHÔNG đụng bug Phase 1 type_name mislabel** (BorrowSellRequestDetailResource `$typeNames=[1=>'HĐ hãng',2=>'HĐ dịch vụ']`) — ngoài scope, đừng báo.
9. gop_db: KHÔNG dùng DB_CONNECTION_SECOND/mysql2; bảng trùng ưu tiên bản ERP.

## Điểm cần soi kỹ (rủi ro cao)
- Cân bằng Nợ=Có mọi nhánh; đúng TK theo loại HĐ; atomic `returned_by_sell` (increment, KHÔNG `+= rồi save`); parent status=1 sau store; transaction bao trọn.
- SupportAccountingTrait: const `self::WORK_*` — gotcha đã ghi (const không nằm trong trait). Kiểm không vỡ.
- FE: import từ `../api` (KHÔNG nhầm api Phase 1); getter tiền verbatim Phase 1; box tổng đọc field BE.
- SQL injection / N+1 / thiếu index không phải trọng tâm nhưng nếu thấy rõ thì báo.

## Report contract
Ghi report đầy đủ vào `.plans/gop-db/xuat-ban-hang-muon/sdd/final-review-report.md`.
Trả về ngắn gọn: tổng số finding theo severity (Blocker/High/Medium/Low), 3-5 finding nặng nhất (1 dòng mỗi cái + file:line), verdict tổng (SHIP / SHIP-with-nits / BLOCK). Mỗi finding trong report: severity, file:line, mô tả, failure scenario cụ thể, và verdict CONFIRMED/PLAUSIBLE. Nếu sạch → nói rõ "không có finding chặn".
