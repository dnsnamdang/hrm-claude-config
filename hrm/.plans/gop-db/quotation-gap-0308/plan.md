# Plan — Báo giá GAP 0308 (@cuong61n)

## Phase 1 — Các mục sửa được ngay
- [x] BE+FE: Nhu cầu khách hàng (chọn nhiều danh mục ERP customer_demands, bắt buộc khi gửi duyệt, lịch sử, đồng bộ ERP)
- [x] BE+FE: Địa chỉ giao hàng (bắt buộc khi gửi duyệt) + đồng bộ ERP dùng giá trị này
- [x] BE+FE: File đính kèm báo giá (files table=quotations, description 'Tài liệu đính kèm')
- [x] FE: Chuyển khối File đính kèm lên ngay dưới Thông tin chung (màn Sửa/Tạo + Chi tiết)
- [x] BE: Tính lại ngày hiệu lực báo giá lúc phê duyệt cuối (selfApprove/tpApprove cấp 2/bgdApprove) — GAP dòng 16
- [x] FE: cột Ảnh + Thời gian bảo hành trên lưới báo giá (form + chi tiết)
- [x] FE: nhãn "Có tính doanh thu / Không tính doanh thu" ở dịch vụ & chi phí
- [x] BE+FE: cột "Báo giá" ở danh mục Hàng hóa dự án (ẩn mặc định, có xuất Excel)
- [x] FE: ô "Chọn báo giá đã có" ở màn tạo mới (dùng luồng copy-draft)
- [x] Ghi chú kết quả vào file Excel tải về (nay gộp vào `GAP_baogia_qlda_erp_ghichu_2710_v11.xlsx`)
- [ ] User test UI + commit/push gop_db (migration 2026_10_26_000001 + route mới → prod phải route:cache)

## Phase 1b — Chương trình khuyến mại (port ERP)
- [x] BE: migration 2026_10_26_000002 + Entity `quotation_promotions`
- [x] BE: QuotationPromotionService (danh sách CT áp dụng, catalog, tính/validate, lưu, hàng tặng gộp, payload ERP)
- [x] BE: endpoint promotion-categories (list + detail), gắn create/update/submit/destroy/detail/history/sync
- [~] ~~BE: fix đồng bộ ERP (vat_percent null, 200 success=false)~~ + ~~ERP nhận combo_categories/promotions~~ — GỠ 27/10 (không đồng bộ ERP nữa)
- [x] FE: utils/quotationPromotion.js + QuotationPromotionSection / GiftTable / PickerModal, gắn edit.vue + index.vue
- [x] Test: PHPUnit 10 case tính, API 29 case, phạm vi 12 case, gửi duyệt hết hạn, đồng bộ ERP thật, JS 20 case, Playwright UI
- [x] Ghi chú lại dòng 34/46 file Excel

## Phase 2 — Chờ chốt nghiệp vụ (xem cột E file Excel)
- [x] 27/10: tải lại sheet khách sửa (gộp 4 loại BG ERP → 2), đọc code ERP, ghi đánh giá + câu hỏi vào `GAP_baogia_qlda_erp_ghichu_2710_v11.xlsx` (bản cuối, các bản cũ đã xoá 28/10); đọc lại ghi chú khách + câu user đã trả lời → bản `_v6.xlsx` hết câu hỏi (tạo hợp đồng + TSKT chính để sau) (sheet Cau_hoi_cho_khach), 22 mục đã chốt (nhu cầu KH: chọn 1; BOM mẫu làm giống báo giá mẫu ERP – màn riêng, quyền "Quản lý BOM mẫu", dùng chung) (sheet Da_chot)
- [ ] Loại báo giá (1)/(2) · Báo giá mẫu/Dữ liệu mẫu · BOM mẫu · GG theo phòng · Hàng tự khai thác · Hỏi giá · quyền lập HĐ · tồn "Có thể LR/Đang giữ" · tuỳ chọn In · cột Ảnh/Bảo hành lưới BOM

## Phase 3 — Làm hết mục đã chốt (file `_v6.xlsx`, 27/10)
Sao lưu sau mỗi task: `backup/backup.sh` (worktree gop_db dùng chung nhiều phiên).
- [x] 1. BE+FE dòng 13: Nhu cầu KH đổi từ danh mục ERP sang nhu cầu meeting, chọn 1; có dự án → lấy theo dự án, khoá; không dự án → bắt buộc khi gửi duyệt
- [x] 2. FE dòng 28/63: lưới BOM thêm cột Ảnh + Bảo hành; cột "Có/Không tính doanh thu" ở popup dịch vụ + lưới BOM
- [x] 3. FE dòng 57: nút "Hỏi giá" (hàng ERP giá ≤ 1,000đ) ở lưới báo giá + BOM → mở /sale/price-asking-requests/add?product_ids=
- [x] 4. BE+FE dòng 30: tồn "Có thể bán (theo công ty) / Có thể LR / Đang giữ" ở popup chọn hàng + lưới báo giá + lưới BOM (cách tính ERP)
- [x] 5. BE+FE dòng 22/26/60: ô "Báo giá mẫu" (project_quotations is_template) + "Dữ liệu mẫu" (quotation_templates) đọc từ ERP, chọn thì thay hết
- [x] 6. FE dòng 45–49: dòng cộng nhóm + tab Tổng hợp theo VAT (báo lỗi cùng mã khác VAT) + dòng tổng các tab như ERP
- [x] 7. BE(+ERP) dòng 58: loại hàng "Hàng tự khai thác"; hàng tạm vào danh mục mang loại này; popup chọn hàng lọc theo loại + hiện người tạo
- [x] 8. BE+FE dòng 56: tuỳ chọn in như ERP + cột Định mức đàm phán + ẩn/hiện cấp nhóm + ẩn/hiện phần báo giá nguồn
- [x] 9. BE+FE dòng 27/59: màn BOM mẫu + quyền "Quản lý BOM mẫu" + chọn mẫu ở tạo BOM / tạo báo giá
- [x] 10. Ghi kết quả từng mục vào file Excel (`_v7.xlsx`, sheet Ket_qua_27_10 + cột E)

### Checkpoint — 2026-10-28 (nhu cầu cho báo giá có dự án + thanh tải)
Vừa hoàn thành: báo giá CÓ dự án cũng chọn nhu cầu meeting (điền sẵn nhu cầu dự án, đổi được, bắt buộc khi gửi duyệt), nhãn nhu cầu kèm mã meeting + ngày; thanh tải Nuxt ($safeLoading) khi chọn Báo giá mẫu / BOM mẫu / Dữ liệu mẫu / Chọn báo giá đã có / Dự án / BOM tổng hợp / BOM mẫu (màn BOM). Test: API 63/63, UI 58/58, bổ sung 19/19, ERP 1,093/1,093. File `_v10.xlsx`.
Đang làm dở: —
Bước tiếp theo: user test tay → xin phép commit 3 repo.
Blocked: chờ user chốt có lọc nhu cầu theo loại/trạng thái meeting (chỉ "Giới thiệu sản phẩm" đã hoàn thành) không.

### Checkpoint — 2026-10-28 (dữ liệu + hướng dẫn test tay)
Vừa hoàn thành: user chốt (a) xoá BOM mẫu khi chưa khoá, (b) không gắn lại Hàng tự khai thác cho hàng tạm cũ. Bộ dữ liệu test [TEST] (`e2e-p3/seed_test_data.py`), test bổ sung `run_extra.py` 15/15; chạy lại API 58/58, UI 58/58, PHPUnit hàng tạm 17/17. DB local chạy 2 migration team còn thiếu (2026_10_24_000001/2). File `_v9.xlsx`: sheet Huong_dan_test + Du_lieu_test.
Đang làm dở: —
Bước tiếp theo: user test tay theo Huong_dan_test → xin phép commit 3 repo.
Blocked:

### Checkpoint — 2026-10-27 (Phase 3 – bổ sung + e2e)
Vừa hoàn thành: màn Chi tiết báo giá thêm 3 cột tồn + cộng tiền nhóm; BOM mẫu thêm Xuất Excel / Tuỳ chỉnh cột / Lịch sử thay đổi. E2E: API 58/58, Playwright UI 58/58, ERP parity "Có thể LR" 1,093/1,093 (script `e2e-p3/`). File kết quả `_v8.xlsx`.
Đang làm dở: —
Bước tiếp theo: user test tay :3002 → xin phép commit 3 repo.
Blocked: chờ chốt điều kiện xoá BOM mẫu; có gắn "Hàng tự khai thác" cho hàng tạm cũ không.

## Phase 4 — Đẩy code + lên dev (30/10/2026) — @cuong61n
- [x] 30/10 Gom file báo giá (Phase 1/1b/3) thành nhánh `feature/quotation-gap-0308` dựng từ `origin/gop_db`, không gồm file của phiên khác đang sửa trong worktree (Rank, phiếu công tác, meeting, quyết định nhân lực) — đã push 3 repo: hrm-api 196b0ccdd, hrm-client ca8b12874, TanPhatDev 51664d41c
- [x] 30/10 Merge vào nhánh dev: hrm-api `develop` 80337359a, hrm-client `develop` 4e2a3e1fc (gỡ conflict nối 2 bên: ProductPickerRequest `product_cate`+`stock_company_ids`, ProductExportService `updater_name`+`note`, product-list-screens cột `updater_name`+`LINKED_COLUMNS`), ERP `develop_02` 9330af057 (không conflict)
- [x] 30/10 ERP dev (dev-erp.dnsmedia.vn) đã git pull develop_02
- [x] 30/10 Dọn worktree gop_db-api/gop_db-client: gỡ file báo giá đã nằm trên nhánh feature (so hash từng file), file của phiên khác đã có trên origin/gop_db ⇒ kéo worktree về khớp origin/gop_db (api a3321d08e, client 56d488304), git status sạch cả 2; ERP TanPhatDev sạch
- [x] 30/10 HRM dev: chạy `~/build_tpe.sh` (migrate 2026_10_26_000001/000002, 2026_10_27_000001 + seeder quyền + route:cache + build FE) — xong
- [x] 30/10 Test lại trên cổng dev: bộ e2e chạy được 2 môi trường (`E2E_ENV=dev`; `seed_dev.py` dựng dữ liệu [TEST] trên hrm_erp_test: KH 232834, dự án [TEST] 491 nhân bản dự án 489 với Sale = namdangit, báo giá 422/423/424/425, nhu cầu 533–536, BOM mẫu 1/2, BOM nháp 31, hàng tự khai thác 52061/52062; cấp quyền "Quản lý BOM mẫu" cho vai trò Super admin công ty 1 trên dev). Kết quả: API 64/64, UI 58/58, bổ sung 22/22, KM dev (CT 506, KH 18002, BG 433) 13/13
- [x] 30/10 Bỏ bắt buộc "Nhu cầu khách hàng": FE bỏ * + bỏ chặn khi Gửi duyệt (edit.vue), BE bỏ chặn trong `QuotationService::assertSubmittable` — commit trên feature/quotation-gap-0308: api e400fa09a, client 89ba441c7 — đã push + merge develop (api 9481bb6a1, client bed7c13bd), build dev lại; e2e sửa ca kiểm tương ứng
- [x] 30/10 Khách chốt lại Nhu cầu KH: báo giá độc lập chọn nhu cầu thu thập từ meeting; báo giá từ dự án TKT KẾ THỪA nhu cầu chọn ở màn tạo dự án, KHÔNG cho đổi. BE: `resolveDemandId` có dự án ⇒ luôn lấy nhu cầu gắn với dự án (bỏ qua giá trị FE gửi), mỗi lần lưu báo giá dự án tự lấy lại; `customer-demand-options` có project_id chỉ trả nhu cầu của dự án; DetailQuotationResource trả nhu cầu dự án (cả bản ghi cũ lưu lệch) + cờ `customer_demand_locked`. FE: ô khoá khi có dự án, placeholder "Dự án chưa gắn nhu cầu khách hàng". Commit api 2b1f28006, client e869b2a25 (chưa push). e2e sửa: gửi nhu cầu khác/KH khác ⇒ vẫn lưu nhu cầu dự án, dự án chưa gắn nhu cầu ⇒ trống không lỗi, UI ô khoá

### Checkpoint — 2026-10-27 (Phase 3)
Vừa hoàn thành: 9 việc Phase 3 (nhu cầu meeting, cột Ảnh/Bảo hành/tồn BOM, Hỏi giá, tồn 3 cột, Báo giá mẫu + Dữ liệu mẫu, Tổng hợp VAT + cộng nhóm, Hàng tự khai thác (sửa cả ERP 7 file), tuỳ chọn in, màn BOM mẫu + chọn mẫu ở BOM/báo giá). Test API + Playwright :3002.
Đang làm dở: —
Bước tiếp theo: user test tay :3002 → xin phép commit 3 repo (hrm-api, hrm-client, TanPhatDev). Deploy: migrate (2026_10_26_000001 đổi cột customer_demand_id, 2026_10_27_000001 bom_templates), seeder quyền "Quản lý BOM mẫu", route:cache.
Blocked: chờ user chốt: điều kiện xoá BOM mẫu; có gắn "Hàng tự khai thác" cho hàng tạm cũ không.

### Checkpoint — 2026-10-26 (KM)
Vừa hoàn thành: Phase 1b Chương trình khuyến mại (BE+FE+ERP) + test.
Đang làm dở: không.
Bước tiếp theo: user test UI :3002 (CT 482 đang gia hạn tạm tới 31/12/2026 ở DB local, BG test BG-2026-00123 id 214) → commit/push 2 repo (hrm-api, hrm-client) khi được duyệt; deploy chạy migration 2026_10_26_000002 + route:cache.
Blocked:

### Checkpoint — 2026-10-26
Vừa hoàn thành: Phase 1 (BE+FE) + test API (validate, chặn gửi duyệt đúng thứ tự, lịch sử, files) + PHPUnit Quotation 11/11.
Đang làm dở: không.
Bước tiếp theo: user test UI tại :3002 → commit/push.
Blocked: các mục Phase 2 chờ user chốt.

### Checkpoint — 2026-10-26 (e2e KM + đối chiếu ERP)
Vừa hoàn thành: test e2e luồng KM, script lưu ở `e2e-km/` — FE vs JS ERP 750/750 bộ số ngẫu nhiên; BE vs ERP 750/750 (285 ca nhập vượt BE chặn đúng lúc ERP tự kéo về); phạm vi CT 510 tổ hợp (NV × KH × bộ lọc + chi tiết) khớp ERP; UI HRM 42/42; đồng bộ ERP (BG 50435) — DB + màn Xem/Sửa ERP khớp HRM 7/7. File giải thích luồng: `Luong_CTKM_ERP_va_HRM.xlsx`.
Đang làm dở: —
Bước tiếp theo: user test tay; xin phép commit 3 repo; trả hạn CT 482 về 2026-09-30 sau khi test tay.
Blocked: nút "Đồng bộ lại" (retry-sync) team đang tạm tắt (fa9e461dc) — đồng bộ chỉ chạy tự động sau duyệt cuối.

### Checkpoint — 2026-10-27 (đánh giá file GAP bản khách sửa)
Vừa hoàn thành: đánh giá lại toàn bộ sheet bao_gia_QLDA_0308 theo code ERP; file `GAP_baogia_qlda_erp_ghichu_2710_v11.xlsx` (bản cuối, các bản cũ đã xoá 28/10).
Đang làm dở: —
Bước tiếp theo: không còn câu hỏi khách (`_v6.xlsx`), bắt đầu làm; các mục tự làm được không cần hỏi: cột Ảnh/Bảo hành lưới BOM, cột có/không tính doanh thu ở popup dịch vụ + lưới BOM, nút Hỏi giá (≤ 1,000đ), cột tồn kho 3 cột, dòng tổng hợp + tuỳ chọn in như ERP, mẫu báo giá đọc từ ERP, loại "Hàng tự khai thác".
Blocked: Nhu cầu KH (dòng 13) khách muốn bỏ danh mục ERP đã làm 26/10 — chờ trả lời H7–H9.
Định hướng 27/10: báo giá dùng hẳn trên HRM, KHÔNG đồng bộ sang ERP (sau này bỏ ERP) → user chốt: đồng bộ cũ đang lỗi thì kệ (không sửa, không tắt); đã gỡ toàn bộ sửa đổi đồng bộ 26/10 (HRM QuotationErpSyncService về bản gốc, xoá erpPayload; TanPhatDev sạch). Đợt commit chỉ còn hrm-api + hrm-client.
