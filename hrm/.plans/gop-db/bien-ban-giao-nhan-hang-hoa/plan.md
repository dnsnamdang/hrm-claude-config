# Plan — Biên bản giao nhận hàng hóa (ERP → HRM) — @khoipv

Spec: `docs/superpowers/specs/gop-db/2026-11-10-bien-ban-giao-nhan-hang-hoa-design.md`
Khuôn bám: BB bàn giao nghiệm thu (`Modules/CustomerCare/*HandoverAcceptanceRecord*`, `pages/assign/handover-acceptance-records/`).

## Phase 1 — Khảo sát + chốt (10/11)
- [x] Khảo sát ERP (controller, model, blade, JS class, menu, mẫu in, dữ liệu)
- [x] User chốt: nguồn HĐ hãng + BH/SC + HRM (qua YCXH loại 21), quyền y ERP (mã có sẵn), sửa/xoá y ERP, in mẫu BBGNHHVT
- [x] Spec + plan

## Phase 2 — BE (`Modules/Sale`)
- [x] B1 Entity 3 bảng (`HandoverProductRecord`, `…Detail`, `…Serial`) + hằng trạng thái / contract class
- [x] B2 Service dùng chung `ContractDeliveredQtyService` (SL theo HĐ / đã xuất / nhập trả / đã bàn giao / ngày xuất cuối, 3 nguồn HĐ)
- [x] B3 Service nguồn HĐ (popup + điền sẵn + hàng)
- [x] B4 Service danh sách / chi tiết / xoá / phạm vi / lịch sử
- [x] B5 Service lưu (tạo / sửa / duyệt → serials) + FormRequest + validate-serials
- [x] B6 Print service (mẫu BBGNHHVT + in danh sách) + ExportColumnRegistry
- [x] B7 Controller + routes + Catalog `platforms` hrm + đăng ký CatalogHistoryService::TABLES
- [x] B8 Smoke test HTTP kernel (tinker) — chi tiết/in/popup HĐ/điền sẵn/tạo/422 vượt SL + thiếu serial/sửa/duyệt→serials + lịch sử/xoá 409/validate-serials OK, chạy trong transaction rollback. Danh sách/meta/xuất với `type=all` cần DB đã `rbac:convert` (local thiếu `permissions.code`) — chưa kiểm được ở local

## Phase 3 — FE (`pages/sale/handover-product-records/`)
- [x] F1 index.vue (danh sách chuẩn, lọc, cấu hình cột, xuất, in, lịch sử)
- [x] F2 Form + bảng hàng + popup chọn HĐ + popup serial
- [x] F3 create / edit / chi tiết (V2Footer, lịch sử, in popup "In hãng sản xuất")
- [x] F4 Menu `sale-hub.js` 2 mục → link
- [x] F5 Compile check (vue-template-compiler + babel) + grep checklist skill — sạch

## Phase 4 — Hoàn thiện
- [ ] Hỏi user vá ERP đọc biên bản HĐ HRM (`contract()` belongsTo FirmContract)
- [x] Check lỗi 500 "Mã quyền không tồn tại: customer_care.bien_ban_giao_nhan.view" (10/11): code đã theo phân quyền mới;
      DB local chưa nạp catalog → chạy `permission:catalog-sync` (942 mã). Vai trò chưa được gán mã mới (`rbac:convert` chưa chạy)
      → Super admin cũng chỉ thấy phiếu mình tạo (fail-closed, đúng).
- [x] Test Playwright có cửa sổ (user theo dõi), tài khoản 583: danh sách 7 dòng, bộ lọc, tạo mới (chọn HĐ → điền sẵn),
      chặn vượt SL + thiếu serial + thiếu file khi duyệt, nhập seri, Lưu nháp, chi tiết, in kèm hãng SX (letterhead TPSG), sửa,
      xoá (lịch sử create/update/delete). Không phát hiện lỗi màn. Dọn: biên bản id 12 + 3 dòng catalog_histories 1860–1862.
      Chưa test: "Lưu và duyệt" thật (cần upload S3 + ghi bảng serials chung), Xuất Excel, In danh sách.
- [x] Tạo dữ liệu test local cho namdangit (13) — `test-data/seed_bbgn_test.php` (chỉ THÊM dòng, id ghi `test-data/manifest.json`):
      HĐ hãng `HĐ_TEST-BBGN_HANG_01` (24940, 6 hàng xuất đủ) + `_02` (24941, đơn hàng nguyên tắc, 7/16 hàng đã xuất),
      HĐ HRM `HĐ-TEST-BBGN-HRM-01` (44, 7 hàng, 3 hàng xuất 1 phần, máy hàn FUNISI-9900S bắt buộc serial) + báo giá test riêng,
      3 YCXH đã hạch toán (35778–35780), vai trò tạm 100211 công ty 1 cấp `customer_care.bien_ban_giao_nhan.view` mức Tổng công ty.
      Xoá: `test-data/cleanup_bbgn_test.php` (xoá kèm biên bản tạo trên các HĐ test; serial ở bảng `serials` chung chỉ liệt kê).

### Checkpoint — 2026-11-10
Vừa hoàn thành: BE `Modules/Sale` (entity 3 bảng, `ContractDeliveredQtyService` dùng chung, nguồn HĐ, danh sách/chi tiết/xoá/lịch sử,
lưu + FormRequest + validate-serials, in mẫu BBGNHHVT + in danh sách, route `/v1/sale/handover-product-records`, Catalog `platforms` hrm,
export registry, catalog history). FE `pages/sale/handover-product-records/` (index, create, `_id/index`, `_id/edit`, form, bảng hàng,
popup chọn HĐ / nhập seri / tuỳ chọn in), menu `sale-hub.js` 2 mục → link. Bám màn BB bàn giao nghiệm thu ở mọi khối.
Đang làm dở: —
Bước tiếp theo: user mở trình duyệt bấm thật (chưa kiểm UI); lấy dump prod hoặc `rbac:convert` local để thử danh sách `type=all` / meta / xuất
(local thiếu `permissions.code` → 500 như mọi màn dùng mã quyền); user quyết có vá ERP đọc biên bản gắn HĐ HRM không.
Blocked: DB local chưa chuyển phân quyền mới.
