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

## Phase 5 — Redmine #12119 (11/11/2026): thêm cột Ngày cập nhật, Người cập nhật vào danh sách
- [x] B1 Migration thêm `updated_by` (nullable, sau `created_by`) bảng ERP `handover_acceptance_product_records` + backfill dòng cũ = `created_by`
- [x] B2 Entity hook `saving` ghi `updated_by` = người đăng nhập; sửa phiếu luôn chạm `updated_at` (kể cả chỉ đổi dòng hàng)
- [x] B3 Service: `updater_name` / `updated_at` trong danh sách + chi tiết, sort `updated_at`, export registry
- [x] F1 index.vue: 2 cột mới (sau Ngày tạo) + exportFields
- [x] V1 Verify: migrate, gọi API danh sách, compile FE
      Local: migrate 2 file OK, 0 dòng còn NULL; presentRows trả đúng `updater_name`/`updated_at`; php -l + compile FE sạch.
      Backfill = `created_by` vì cả ERP (`canEdit`) lẫn HRM chỉ cho người tạo sửa. Bản in danh sách giữ nguyên cột (không nằm trong yêu cầu).
      Chưa kiểm trên trình duyệt. Deploy dev cần chạy `php artisan migrate`.

## Phase 6 — Redmine #12121 (11/11/2026): góp ý màn Tạo mới
- [x] 1. Ô lọc "Loại hợp đồng" ở popup chọn HĐ: tên trùng cột bảng — HĐ hãng tách 4 loại (`firm_contract:<type>`:
      bán hàng hóa - vật tư / dự án / nguyên tắc / ĐH nguyên tắc) + HĐ BH-SC + HĐ HRM. BE `contracts()` nhận khoá `firm_contract:<type>`
- [x] 2. SL bàn giao > SL có thể bàn giao: báo đỏ NGAY khi gõ (`qtyExceedError()` + `field-error`), câu rút gọn
      "Không vượt quá số lượng đã xuất (N)" ở cả FE lẫn BE (`HandoverProductRecordStoreService`)
- [x] 3. Popup Nhập seri thu nhỏ: `size="md"`, thân cao tối đa 60vh
- [x] 4. Ẩn dòng chú thích "Seri: …" dưới ô SL bàn giao ở form (màn chi tiết vẫn hiện — chỗ duy nhất xem seri khi chỉ đọc)
- [x] 5. Check "tạo → xoá → chọn lại HĐ báo không có hàng hóa": KHÔNG tái hiện ở local — tinker HTTP kernel (rollback) với HĐ test
      24940 / 24941 / HRM 44: trước 6/7/7 hàng → tạo xong 0 → xoá → 6/7/7 hàng. Xoá đã xoá tường minh serial + dòng hàng.
      Cần dữ liệu dev (mã HĐ `HĐ_TPE_CTV_NV_26_0002_0987656789`): còn biên bản nào khác của HĐ trong
      `handover_acceptance_product_records` (kể cả tạo từ ERP / bấm "Lưu và tiếp tục") không
- [x] V. php -l + tinker: lọc `firm_contract:1` → 1 HĐ đúng loại, `:8` → 1, `:99` → bỏ qua lọc loại; 422 trả câu mới.
      Compile FE (vue-template-compiler + babel) 5 file sạch. Chưa bấm trên trình duyệt.
- [x] Check mục 5 trên dev (API, DNS Admin): HĐ 29962 còn biên bản TPE.BBGN.00011 (id 11, Đang tạo, giữ SL 1/1) → 0 hàng là ĐÚNG.
      id 9 xoá 10:02 có log; id 10 tạo 10:03 rồi mất KHÔNG có log xoá (nghi xoá từ ERP / lưu lỗi giữa chừng) — chưa rõ, cần log dev.
- [x] Push develop: hrm-api `99928bf99`, hrm-client `c4be15627`

### Checkpoint — 2026-11-10
Vừa hoàn thành: BE `Modules/Sale` (entity 3 bảng, `ContractDeliveredQtyService` dùng chung, nguồn HĐ, danh sách/chi tiết/xoá/lịch sử,
lưu + FormRequest + validate-serials, in mẫu BBGNHHVT + in danh sách, route `/v1/sale/handover-product-records`, Catalog `platforms` hrm,
export registry, catalog history). FE `pages/sale/handover-product-records/` (index, create, `_id/index`, `_id/edit`, form, bảng hàng,
popup chọn HĐ / nhập seri / tuỳ chọn in), menu `sale-hub.js` 2 mục → link. Bám màn BB bàn giao nghiệm thu ở mọi khối.
Đang làm dở: —
Bước tiếp theo: user mở trình duyệt bấm thật (chưa kiểm UI); lấy dump prod hoặc `rbac:convert` local để thử danh sách `type=all` / meta / xuất
(local thiếu `permissions.code` → 500 như mọi màn dùng mã quyền); user quyết có vá ERP đọc biên bản gắn HĐ HRM không.
Blocked: DB local chưa chuyển phân quyền mới.
