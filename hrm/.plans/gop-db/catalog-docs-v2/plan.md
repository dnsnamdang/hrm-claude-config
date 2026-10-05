# Plan — Cập nhật tài liệu 20 danh mục chuyển ERP→HRM theo code hiện tại (25/09/2026)

Nguồn: bảng theo dõi `Checklist HDSD_SRS_TESTCASE` tab "Chuyển đổi ERP->HRM" dòng 3–24 (trừ Gói bảo dưỡng — đã làm, Quốc gia — bản mẫu).
Khuôn đã được duyệt: Gói bảo dưỡng (`customer-care-services-catalog/docs_v2/`), thư viện `_catalog_docs_lib/qg_writer.py`.

Quy tắc (user chốt 25/09):
- HDSD/SRS dựng theo khuôn tài liệu Quốc gia, nội dung theo code gop_db; KHÔNG ghi URL; ghi đè giữ ID (so modtime trước — file có người sửa tay thì đối chiếu).
- Testcase: sửa THẲNG case cũ liên quan (mã / import / xuất Excel), chức năng chưa có thì thêm nhóm; dòng sửa → xoá "DNS check lần 1"; không thay cả tab.

## Tiến độ
- [x] Rà code 20 màn (4 agent song song)
- [x] Bộ công cụ: `_catalog_docs_lib/catalog_v2.py` (HDSD/SRS/UML) · `capture_tpl.js` + `make_capture.py` (chụp ảnh) · `import_tpl.js` · `upload.py` (Drive giữ ID) · `tc_gen.py` + `tc_ops.py` + `_catalog_docs_lib/sheet_tpl.js` (sửa tab testcase)
- [x] Khu vực (mẫu chuẩn): HDSD + SRS đã đẩy Drive giữ ID · tab 14 thêm nhóm VIII Xuất Excel (9 TC) + IX Import (19 TC), sửa B8 — 25/09/2026
- [x] Vụ việc: HDSD+SRS Drive · tab 19 (B7, TC_03.012–015, TC_04.012, nhóm VII Xuất 9 + VIII Import 24) — 26/09
- [x] Mã phí: HDSD+SRS Drive · tab 21 (B7, TC_03.012–015, TC_04.013, nhóm VII+VIII) — 26/09
- [x] Nguồn vốn: HDSD+SRS Drive · tab 20 (nhóm VII Xuất 9 + VIII Import 18) — 26/09
- [x] Loại tài khoản: HDSD+SRS Drive · tab 4 (sửa 27 ô nhóm Xuất/Import + mã, xoá K 14 hàng, TC_09.012–014) — 26/09
- [x] Tiền tệ: HDSD+SRS Drive · tab 2 (B7, 19 ô Xuất/mã, TC_08.019–022, nhóm XI Import 29) — 26/09
- [x] Tài khoản: HDSD+SRS Drive · tab 3 (31 ô, xoá K 17 hàng, TC_09.015–016) — 26/09
- [x] Tỉnh/TP: HDSD+SRS Drive · tab 16 (B8, TC_03.015–017, nhóm VIII Xuất + IX Import 26) — 26/09
- [x] Quận/Huyện: HDSD+SRS Drive · tab 18 (B8, nhóm VII Xuất + VIII Import 20) — 26/09
- [x] Phường/Xã: HDSD+SRS Drive · tab 15 (B8, TC_03.012–016, TC_04.012–014, nhóm VIII Xuất 10 + IX Import 22) — 26/09
- [x] DV sửa chữa & chi phí: HDSD Drive, SRS (file Google Docs, đẩy bằng import-formats) · tab 1 (22 ô Xuất, TC_07.011–014, nhóm X Import 28) — 26/09
- [x] Đường/Phố: HDSD+SRS Drive · tab 17 (B8, nhóm VII Xuất + VIII Import 23) — 26/09
- [x] Đối chiếu lại code (agent) cho geo + levels/note-maintenances/banks/account-banks; đẩy lại Tỉnh/TP, Quận/Huyện, Phường/Xã bản đã sửa — 26/09
- [x] Cấp DV BD: HDSD+SRS Drive · tab 7 (B8, I19–20, 12 ô Xuất, TC_06.007–012, nhóm IX Import 19) — 26/09
- [x] Ghi chú KT BD: HDSD+SRS Drive · tab 8 (B8, I19–20, 12 ô Xuất, TC_06.007–013, TC_07.012–013, nhóm IX Import 24) — 26/09
- [x] Serial: HDSD+SRS Drive · tab 6 (17 ô Xuất, TC_04.013–016) — 26/09
- [x] Ngân hàng: HDSD+SRS Drive · tab 10 (B4, I29/91/163, TC_04.034–035, nhóm XI Xuất 10 + XII Import 25) — 26/09
- [x] TK ngân hàng: HDSD+SRS Drive · tab 11 (B2, B8, I31, nhóm X Xuất 11 + XI Import 27) — 26/09
- [x] Công việc/lỗi TB: HDSD+SRS Drive · tab 22 (13 ô Xuất, TC_08.011–019) — 26/09
- [x] Cập nhật nhanh giá DV: HDSD+SRS Drive (tả đúng lỗi bỏ trống Hệ số); tab 5 không đổi — 26/09
- [x] Phần 4 SRS 5 cột (khuôn Quốc gia) cho 18 danh mục + Gói BD — 26/09
- [ ] Soạn config 19 danh mục còn lại (agent) → chụp ảnh → build → Drive → testcase
- [ ] CSKH: Công việc-lỗi thiết bị · Cấp dịch vụ BD · Ghi chú kiểm tra BD · Dịch vụ sửa chữa & chi phí khác · Cập nhật nhanh giá DV · Serial thiết bị
- [ ] Địa lý: Khu vực · Tỉnh/TP · Quận/Huyện · Phường/Xã · Đường/Phố
- [ ] Tài chính: Tài khoản · Loại tài khoản · Tiền tệ · Ngân hàng · Tài khoản ngân hàng
- [ ] Khác: Khách hàng · Vụ việc · Mã phí · Nguồn vốn

### Checkpoint — 25/09/2026 17:40
Vừa hoàn thành: Khu vực (HDSD+SRS Drive, tab 14 testcase xong) · Vụ việc: chụp ảnh + import thử + HDSD/SRS đã đẩy Drive giữ ID.
Config đã có (agent soạn): works, cost-debts, source-capitals, costs, serials, service-price-config. Đang chờ agent: levels/note-maintenances/device-errors · provinces/districts/wards/hamlets · accounts/type-accounts/currencies · customers/banks/account-banks (xong sẽ có configs/<slug>.py).
Đang làm dở: tab testcase "19. DM vụ việc" — CHƯA chạy `.playwright-mcp/sh_works.js` (đã sinh bằng tc_ops.py; chèn sau R84 nhóm VII/VIII, sau R64 TC_04.012, sau R52 TC_03.012–015, sửa B7). Chạy trước phải chụp soát lại R52/R64/R84 trên sheet còn khớp dump không.
Bước tiếp theo: chạy sh_works.js → mỗi slug còn lại: `pipeline.py <slug> cap` → chạy cap_<slug>.js → `imp` → chạy imp_<slug>.js → `copy` → `build` → soát preview → `up` → `tc_ops.py <slug>` → chạy sh_<slug>.js.
Lưu ý: service-price-config phải chụp tay (không có bảng); costs import_ok_msg = "Validate thành công"; source-capitals cần tạo thêm dữ liệu mẫu trước khi chụp. Cuối cùng báo user danh sách loi_code + tc_ngoai_pham_vi (vd Vụ việc/Mã phí: code chặn Khoá khi đã hạch toán, ngược tài liệu cũ).
Cập nhật 17:55: 4 agent còn lại bị treo (watchdog 600s) nhưng đã kịp ghi config: levels, note-maintenances, provinces, districts, wards, hamlets, type-accounts, currencies, banks, account-banks (đều load được, có tc + capture — phải soát kỹ vì agent chưa tự kiểm xong, nhất là banks và nhóm địa lý). CHƯA có config: device-errors, accounts, customers → giao agent lại (mỗi agent 1 màn).

## Sửa code Quận/Huyện (user yêu cầu 26/09/2026)
Quyết định đã chốt (user trả lời 26/09):
- Popup Tạo/Sửa có ô Trạng thái (Hoạt động/Khóa) như các danh mục địa lý khác; danh sách hiện cả bản ghi Khóa, có Khóa / Mở khóa.
- "Đã dùng" = có tham chiếu ở Phường/Xã, hồ sơ nhân sự (thường trú/tạm trú), Khách hàng, Công ty, Nhà cung cấp, Địa điểm giao hàng (KHÔNG tính yêu cầu cập nhật hồ sơ).
- Xóa = xóa hẳn khi chưa dùng; đã dùng → ẩn nút Xóa + máy chủ chặn.
- [x] BE: entity isCanDelete + service lock/unlock/delete cứng + request status + chặn sửa khi Khóa (423) + resource cờ
- [x] FE: DistrictModel thêm Trạng thái, index hành động Khóa/Mở khóa/Xóa theo cờ, bộ lọc Trạng thái
- [x] Kiểm trên trình duyệt; cập nhật config districts → dựng lại HDSD/SRS; sửa tab testcase 18 (28/09)

## Áp nguyên tắc danh mục cho toàn bộ màn (user chốt 26/09/2026)
Nguyên tắc: không xoá mềm; Xoá = xoá hẳn khi chưa dùng (đã dùng → ẩn nút + BE chặn); có Khoá/Mở khoá; popup/form có ô Trạng thái; bản ghi Khoá bị BE chặn sửa/xoá 423 (middleware recordNotLocked). Khuôn: Quận/Huyện.
Quyết định:
- Phạm vi: TẤT CẢ màn lệch, làm dần — nặng trước (Nguồn vốn, Đường/Phố, Cấp DV BD, Ghi chú KT BD, Chi nhánh NH, Vụ việc, Mã phí, Chi phí, Gói BD), sau đó bổ sung kiểm "đã dùng" ở BE cho các màn còn lại (Khu vực, Tỉnh/TP, Phường/Xã, Ngân hàng, Tiền tệ, Loại TK, TK ngân hàng, Lỗi TB, Serial, Tài khoản).
- Khách hàng: giữ "Xoá = Khoá" như ERP, CHỈ thêm ô Trạng thái vào form.
- "Đã dùng" = có dòng ở mọi bảng có cột id trỏ tới (không tính cột lưu tên bằng chữ).
- Cho Khoá cả khi bản ghi đang được dùng (bỏ luật cấm khoá ở Phường/Xã, Loại TK, Vụ việc/Mã phí đã hạch toán).
- Mỗi màn sửa code xong → cập nhật config + chụp lại ảnh + dựng lại HDSD/SRS + sửa tab testcase.
- [x] Code Đường/Phố (hamlets): BaseModel + USAGE_REFERENCES (customers/delivery_places/companies/suppliers.hamlet_id), list 2 trạng thái + lọc, ô Trạng thái, Khoá/Mở khoá, xoá cứng (400 đã dùng / 423 khoá), export Trạng thái — 28/09
- [x] Code Chi nhánh NH (bank_branches): migration status+created_by+updated_by, BankBranchService (lịch sử bank_branches), PUT/DELETE/lock/unlock + recordNotLocked, popup Chi nhánh có Trạng thái/badge/lọc/Khoá/Lịch sử; màn khác (hồ sơ NS, TK NH, KH) ẩn chi nhánh khoá + 🔒 — 28/09
- [ ] Chi nhánh NH + Đường/Phố: kiểm trên trình duyệt; cập nhật config → dựng lại HDSD/SRS; sửa tab testcase
- [x] Code Cấp DV BD (levels) + Ghi chú KT BD (note_maintenances): migration status (2026_09_28_000001/000002), BaseModel, USAGE_REFERENCES + usedIds, list 2 trạng thái + lọc + badge, ô Trạng thái popup, PUT lock/unlock, xoá cứng (400/423), export Trạng thái; select ở form Gói BD + import gói + báo giá chỉ lấy bản ghi Hoạt động, gói cũ nhận `locked_levels`/`locked_note_maintenances` hiện 🔒 — 28/09
- [x] Code Chi phí (costs): bỏ "Xoá thành Khoá", USAGE_REFERENCES 61 cột (kể cả wr_accounting_service_items/wr_import_result_services.service_id trỏ costs), lock/unlock GET→PUT, bỏ /usage, sửa export thiếu status_text/revenue_calculation_text — 28/09
- [x] Code Gói BD (services): bỏ "Xoá thành Khoá", thêm PUT /lock + nút Khóa (danh sách + chi tiết), USAGE_REFERENCES 10 bảng (4 wr_*_extend_product_services + 6 service_*_items), xoá cứng dọn cả service_has_products/company_service_coefficients — 28/09
- [ ] Levels/Ghi chú/Chi phí/Gói BD: user xác nhận 2 điểm (service_has_products không tính "đã dùng"; 2 bảng wr_* trỏ costs), kiểm trình duyệt; cập nhật config → dựng lại HDSD/SRS; sửa tab testcase
- [x] Tài liệu Vụ việc / Mã phí / Nguồn vốn / Đường-Phố / Ngân hàng (+ chi nhánh): config cập nhật, chụp lại, dựng + đẩy HDSD/SRS (giữ ID); tab testcase 19, 20, 21 đã sửa — 28/09
- [x] Tài liệu Cấp DV / Ghi chú KT / Chi phí / Gói BD: config + chụp lại (Gói: ảnh 54–58 + 3 icon), dựng; đẩy SRS 4 màn + HDSD Chi phí (giữ ID) — 28/09
- [ ] HDSD Cấp DV / Ghi chú KT / Gói BD CHƯA đẩy: file trên Drive bị người khác đổi tên (có dấu) + đang sửa 28/09 → chờ user cho ghi đè (đã xoá 3 bản trùng rclone lỡ tạo)
- [x] Tab testcase 17 (Đường/Phố), 10 (Ngân hàng), 12 (Gói BD) đã sửa — 28/09
- [ ] Tab 7 (Cấp DV), 8 (Ghi chú KT), 1 (Chi phí): tester đang sửa tay cùng lúc (xoá case gọi thẳng API, đổi "nạp lại"→"tải lại") → đã rebase số hàng, chờ user chốt giờ chạy + có bỏ case gọi thẳng API không

## Bổ sung SRS: Mô tả chi tiết giao diện + Danh sách event (tester báo 28/09/2026)
- Hiện trạng: config chỉ có 2 bảng ở FR Xem danh sách / Tìm kiếm / Thêm mới; thiếu ở Sửa, Xóa, Khóa, Lịch sử, Import, Xuất, Xem chi tiết/In, Tùy chỉnh cột (mọi danh mục trừ QG). Gói BD thiếu ở Chi tiết, Tùy chỉnh cột, Nhân bản, In.
- Brief: SRS_UI_EVENTS_BRIEF.md (khuôn QG; Chi tiết + Tùy chỉnh cột QG để trống → tự viết theo code)
- [x] 4 agent bổ sung config (địa lý 5 · kế toán 5 · tài chính+NH 6 · CSKH 4 + Gói) — mọi FR đủ 2 bảng
- [x] Dựng lại 21 SRS; đẩy 17 file (giữ ID) — 28/09
- [x] 4 SRS Khu vực, Phường/Xã, Loại TK, Lỗi thiết bị: gộp phần tester sửa tay (CFG['srs_tester'] + apply_tester_edits) rồi đẩy — 28/09
- [x] Kiểm trên Drive: 21/21 SRS đủ bảng giao diện + event ở mọi chức năng
- [x] Ghi bài học vào skill (28/09): srs-documenter (2 bảng bắt buộc mọi FR + tự kiểm + đẩy Drive), hdsd-documenter (đẩy Drive), testcase-documenter (sửa tab online: dump lại ngay trước khi chạy, theo giọng tester, cấm emoji kể cả 🔒/☰), erp-to-hrm-screen H2 (danh mục xoá cứng/Khoá/Trạng thái, thứ tự middleware, "Item Not Found!")
- [x] catalog_v2.build_srs + gen_srs.py Gói: thiếu ui/events thì ném lỗi
- [x] Gỡ emoji ☰/🔒 khỏi 43 ô ở 17 tab danh mục + tc_gen.py + config levels/notes

## HDSD Danh mục khách hàng bản 1.3 — viết chi tiết theo khuôn HDSD Quốc gia (user báo 28/09/2026)
- [x] Sửa thẳng trên bản Drive (đã có người sửa tay 14:51 + 15:07) bằng `customers/patch_hdsd_v13.py` + `build_hdsd_v13.sh` — KHÔNG build lại từ configs/customers.py (config chưa có phần này, build lại sẽ mất)
- [x] Cột Hành động, Khóa/Mở khóa, Lịch sử (theo bước), Chi tiết: ảnh nút inline cắt từ UI (customers/icons, 30+ nút mới)
- [x] PHẦN 4 Chỉnh sửa: điểm khác Thêm mới, NV phụ trách đại lý/Cấp đại lý, khối Địa chỉ giao hàng (thêm/bỏ/quy tắc lưu/dùng ở đâu), quy tắc giữ/xoá người liên hệ
- [x] PHẦN 8 Quản lý KH: 6 thẻ, 2 nút Lưu, thiết bị (thêm cũ/NCC, sửa, tăng SL, xoá, serial thêm/sửa/thay đổi/xoá, in/xuất), báo giá/hợp đồng (lọc, cột, phạm vi quyền, in/xuất), Thông tin khác
- [x] Đẩy Drive giữ ID, tải lại đối chiếu khớp — 28/09
- [ ] Đồng bộ nội dung 1.3 ngược về configs/customers.py (nếu sau này build lại cả bộ)

## 29/09/2026 — HDSD bản GỌN (khuôn tester, skill hdsd-documenter mới)
- [x] Rút gọn HDSD 21 màn danh mục theo khuôn HDSD_MAU_GON (mỗi chức năng 1 phần, chỉ các bước, 1 ảnh/chức năng, ảnh nút cắt sát) — gen: `<slug>/gen_hdsd_gon.py` + `_catalog_docs_lib/hdsd_gon.py`, đẩy theo ID bằng `push_hdsd_by_id.py`
- [ ] Tester (hangtechqa) tự xoá 7 file trùng tên bản 21/08 (mình không có quyền xoá) — danh sách: `dup_ids_to_trash.json`
