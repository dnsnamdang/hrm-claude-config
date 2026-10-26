# SDD ledger — plan: HRM/.plans/gop-db/quan-ly-hang-hoa/sao-chep-hang-hoa/plan.md

Worktree: `websites/wt-sao-chep-hang-hoa/{hrm-api,hrm-client}` nhánh `feat/sao-chep-hang-hoa` từ origin/gop_db
(api 2169b460e · client 0113bddb6). vendor/node_modules copy thật (autoload đã kiểm trỏ worktree). DB test:
`hrm_erp_test_saochep` (dump `hrm_erp_21_10_prod` 24/10). PHPUnit: `DB_DATABASE=hrm_erp_test_saochep DB_DATABASE_SECOND=hrm_erp_test_saochep /opt/homebrew/opt/php@7.4/bin/php vendor/bin/phpunit …`

Pre-flight: T3 dùng T1 `copyToTemporary(string): string|false` + T2 `KitStatusGuard::reasons(array,int): array` — khớp;
T6 dùng khuôn JSON T3 (`copy_source`, `dropped`, `option_ids`) — khớp; T4 chữ ký `store(..., ?int $copyFromId)` — chỉ controller dùng.

Ruling: không commit theo task (memory khong-hoi-commit-user-tu-bao) — task-done ghi theo lệnh test, không theo dải commit — cost if wrong: user phải tự commit 1 lần.

Task 0: complete (worktree + DB test)
Task 1: complete (tests: phpunit Modules/MasterData/Tests/Unit/CmcS3HelperCopyToTemporaryTest.php → 4/4 OK; RED trước: 4 lỗi undefined method)
Ruling: Task 6–7 (FE) viết trước khi Task 2–5 xanh, vì DB test đang nạp — hrm-client không có bộ unit test, FE kiểm bằng Playwright ở Task 8 — cost if wrong: sửa FE nếu khuôn JSON BE đổi.
S10 (user chốt 24/10): chữ "Nhân bản" theo button-convention thay "Sao chép" — đã đổi design/plan/FE/test.
Ruling: nút Nhân bản ở footer chi tiết = `secondary`, đứng CUỐI slot (sau các nút primary) — button-convention mục 5 (chính → phụ) — cost if wrong: đổi 1 dòng.
Task 2: complete (tests: KitStatusGuardTest 2/2 + ProductWriteHardeningTest 11/11 + ProductWriteApiTest 34/34; RED trước: class không tồn tại)
Ruling: menu dòng — 'Nhân bản' đặt SAU Xóa/Khóa (trước Lịch sử), không ngay sau Sửa như plan — V2BaseRowActions đưa 3 mục đầu ra ngoài, quy ước Sửa → Xoá/Khoá → ⋮ — cost if wrong: đổi vị trí 1 dòng.
Task 3: complete (ProductCopyApiTest copy-data 13 ca; RED trước: 404 route) — fixture: payload([]) không đè mảng mặc định ⇒ xoá thẳng ảnh/video trong ca.
Task 4: complete (ProductCopyApiTest +6 ca; RED trước: note null, copy_from_id không 422) + ProductWriteApiTest 34, TempProductApiTest 16, PriceAskingTempProductTest 16, ProductHistoryApiTest 6, ProductCodeRetryTest 2 xanh.
Task 5: complete (can_copy 1 ca, RED trước: null). Cả thư mục Modules/MasterData/Tests: 734 ca, 3 đỏ — ĐỀU ĐỎ SẴN trên gop_db 2169b460e cùng DB test: ExpectedPriceApplyTest::chot_chan_tach…, TempProductVisibilityTest::catalog_tab_them…, PriceReaderWhitelistTest (file Finance/InventoryAuditReportService.php). Ghi chú: memory_limit 2G hết bộ nhớ ở ~580/734 ⇒ chạy -d memory_limit=-1.
Task 6–7: complete — kiểm Playwright MCP (API :8011 + Nuxt :3011 worktree, DB hrm_erp_test_saochep; NV 408 có quyền Cty 3, NV 663 role tạm TMP-NHANBAN-XEM 108733 chỉ "Xem dữ liệu hàng hoá công ty" — chỉ trong DB test):
  · menu dòng trading/company: [edit, lock, file-copy] × 5 dòng; entering [edit, file-copy]; warehouse 0 nút; temp/locked Cty 3 không có dòng
  · footer chi tiết 26684: Sửa(#1abc9c) · Khóa(#d97706) · Nhân bản(trắng) · Quay lại, gap 5px đều (gap của V2Footer)
  · form /create?copy_from=26684: title "Nhân bản hàng hoá", dải nguồn đúng chữ, điền Tên/Model/Loại SP/Thương hiệu/Xuất xứ/Hãng/3 ĐVT
  · Lưu không đổi ⇒ 1 POST 422 ô Tên, payload copy_from_id 26684; đổi tên ⇒ 200 id 62995 mã PINA-PTZ7A:01, badge Đang nhập thông tin, DB: note "Nhân bản từ PINA-PTZ7A", pcc 3 status 1 info_entered, 3 ĐVT, giá 0, ảnh = avatar gốc
  · dropped giả lập (page.route) ⇒ 5 dòng; LỖI tái hiện: icon căn giữa khối (iconTop 123 vs box 70) ⇒ sửa align-items flex-start ⇒ tâm icon 88 = tâm dòng đầu 88; dải không đè thanh tab (bottom 196 < 208)
  · Quay lại form chưa sửa ⇒ về trading, 0 modal
  · NV 663: company 20 dòng 0 icon copy; chi tiết chỉ "Quay lại"; /create?copy_from ⇒ /pages/extras/404; API copy-data 403
  · Sự cố khi đo: lượt bấm nút cuối dòng mở popup "Xác nhận khóa" ENEO-230-45912 ⇒ bấm Hủy, DB vẫn status 3 (không khoá).
Task 8: e2e — spec mới HRM/e2e/tests/master-data/products-copy-ui.spec.ts (NB1–NB6, có quyền + không quyền); sửa ca so khít nút ở products-lifecycle-ui (D1, expectedActions, D9), products-form-ui (E4 — vốn đã lệch từ 23/10 vì thiếu Chuyển KD), products-read-ui (expectedFooter). `--list` biên dịch 47 ca/4 file; CHƯA chạy (memory khong-tu-chay-e2e-moi-task).
Final review (opus, code-reviewer): 0 Critical, 2 Important, 7 Minor. Chấm lại: Minor 1 (2 toast trùng khi 403) nâng lên Important — người dùng thấy trực tiếp.
Final: fixed nhóm máy còn sót khi lọc hết máy ⇒ 422 — may_bi_loc_het_thi_bo_ca_nhom_may_de_luu_duoc RED→GREEN
Final: fixed vehicle_lives lọc theo vehicle_model_ids (trái R20, mất đời xe cũ im lặng) — doi_xe_cu_khong_thuoc_model_dang_chon_van_giu RED→GREEN (+ model_xe_khoa_thi_bo_doi_xe_cua_model_do_va_bao giữ xanh)
Final: fixed 2 toast trùng khi copy-data 403 — tái hiện Playwright 2 toast ⇒ sau sửa 1; 404 "Item Not Found!" ⇒ "Không tìm thấy hàng hoá để nhân bản." (thêm ca e2e NB7). Suite: ProductCopyApiTest 23/23, KitStatusGuard 2/2, CmcS3Helper 4/4, ProductWriteApi 34/34, Hardening 11/11, TempProductApi 16/16.
Final: minor (deferred): hàng kèm/máy trỏ id products không còn (mồ côi) không bị lọc ⇒ Lưu 422 `exists` (hiếm, hardDelete đã chặn chiều ngược)
Final: minor (deferred): lỗi S3 khác 404 (AccessDenied/timeout) làm copy-data 500 cả form; chép tệp tuần tự trong 1 GET
Final: minor (deferred): hàng cũ có dữ liệu xe mà Tính chất không phải phụ tùng ô tô ⇒ bản sao ẩn tab xe, BE bỏ dữ liệu xe khi Lưu mà dải cảnh báo không nhắc
Final: minor (deferred): closedErrors gọi từng tiểu mục; copy-data dựng cả formOptions + vehicleOptions (~1,7k dòng) chỉ để đọc is_locked, FE lại gọi form-options lần nữa
Final: minor (deferred): form nhân bản vừa nạp coi là chưa sửa ⇒ thoát không hỏi (đã chủ ý, đo NB5)
Final: minor (deferred): dữ liệu cũ lỗi (recipe thiếu ĐVT cơ bản, guarantee_type lạ, thuộc tính rỗng) vẫn 422 khi Lưu — giống đường Sửa
E2E 24/10 (user yêu cầu): `products-copy-ui` 7/7 passed (--retries=0) trên :8011/:3011 + API_REPO worktree, DB hrm_erp_test_saochep; dọn sạch (0 hàng E2EC1S, 0 role tạm). Sửa spec trong lúc chạy: NB4 đo nhầm khối bọc (`div > div`) ⇒ `:scope > div > div` + tâm hàng chữ đầu; NB6 role rỗng thì chi tiết 403 ⇒ role tạm chỉ quyền xem + company_roles; `roles` DB gộp không có company_id; tài khoản mới bị bắt đổi mật khẩu (password_changed_at NULL ⇒ mọi API 403 require_change_password).
Môi trường đã đổi (dọn sau): worktree hrm-api/.env DB ⇒ hrm_erp_test_saochep (bản cũ scratchpad wt-api.env.bak); HRM/e2e/.auth/user.json thêm origin http://127.0.0.1:3011 (bản cũ scratchpad user.json.bak); DB test có NV 15758 e2e_cmd_noperm@test.local, role tạm 108733 (NV 663), hàng 62995.
3 spec cũ đã sửa (lifecycle D1/D9/expectedActions, form-ui E4, read-ui expectedFooter) CHƯA chạy.
Minor 25/10 (user: "làm theo đề xuất" — sửa #1 #2 #3, giữ #4 #6, #5 chờ user chọn):
Final: fixed minor #1 thu hẹp — 4 bảng hàng kèm (recipe_products, product_has_*accessories) CÓ khoá ngoại tới products ⇒ không mồ côi được; chỉ máy (productables) mồ côi ⇒ bỏ + báo "Hàng hoá không còn tồn tại." (tên "ID x") — may_khong_con_ton_tai_bo_va_bao RED→GREEN
Final: fixed minor #2 — copyToTemporary ném lỗi khác 404 ⇒ service bắt Throwable, report(), bỏ 1 tệp vào dropped.files; câu FE đổi "không còn trên máy chủ" ⇒ "không chép được" — loi_s3_khac_404_bo_tep_va_bao_khong_hong_ca_form RED→GREEN
Final: fixed minor #3 — Tính chất Loại SP của hàng gốc không phải phụ tùng ⇒ bỏ hết xe + đời xe ở bản sao, dropped.vehicles=true, FE thêm dòng "Bỏ dữ liệu xe … không phải phụ tùng ô tô" — hang_khong_phai_phu_tung_co_xe_bo_xe_va_bao + hang_phu_tung_co_xe_giu_xe_khong_bao RED→GREEN; 2 ca xe cũ chuyển sang Loại SP phụ tùng
Suite: ProductCopyApiTest 27/27, KitStatusGuard 2/2, ProductWriteApi 34/34. Playwright MCP hàng 62995 (gắn tạm model xe + máy id 63995, đã gỡ): 2 dòng đúng, iconMid 88 = firstMid 88, bottom 142 < tabs 154, 0 toast. Spec NB4 cập nhật 6 dòng (CHƯA chạy).
Final: fixed minor #5 (user 25/10: "bật form cảnh báo theo mẫu chung") — ProductForm override `isFormDirty`: copySource && ready && !unsavedIgnore ⇒ true, còn lại gọi mixin. Không sửa mixin dùng chung. Tái hiện trước: Quay lại ⇒ /trading, 0 popup. Sau sửa (Playwright MCP, hàng 62995): popup "Thông tin chưa lưu" 1, Ở lại giữ URL + giá trị ô, Thoát ⇒ /trading; tạo mới thường không sửa vẫn thoát thẳng (0 popup). Lưu thành công: markFormSaved trước emit saved (NB3 kiểm chuyển sang chi tiết). Spec NB5 viết lại theo hành vi mới (CHƯA chạy).
Final: fixed minor #4 (user 25/10 "làm luôn") — `ProductOptionService::optionsForIds($ids)` đi qua CHÍNH các builder form-options/vehicle-options ở chế độ chỉ-id (thêm cờ `$onlyIncluded`/`$onlyIds` + `whereScope`) ⇒ `is_locked` 1 định nghĩa; `CatalogBranchGuard::closedIds()` 1 truy vấn (closedErrors tách `rows()`/`isOpen()` dùng chung, hành vi giữ). ProductCopyService::lockableOptions gom id từ option_ids + xe + đời xe. Test: ProductOptionsForIdsTest (so khớp từng danh mục với form-options/vehicle-options, có dòng đã khoá; rỗng ⇒ rỗng; closedIds 1 query) + copy_data_chi_tra_danh_muc_theo_id_hang_goc — RED→GREEN. Đo hàng 62995 (ấm): copy-data 512 ⇒ ~390 ms, ngang edit ~400 ms. FE gọi form-options 1 lần (lần trùng ở BE đã hết).
Merge 25/10 (user yêu cầu): commit api ddd04398a / client c0062eabf trên feat/sao-chep-hang-hoa ⇒ fast-forward gop_db (bản chính HRM/hrm-api, hrm-client sạch) ⇒ push origin cả gop_db + feat/sao-chep-hang-hoa, đã xác nhận remote = local. e2e (HRM/e2e, ngoài git) chưa chạy lại NB4/NB5 + 3 spec cũ.
E2E 25/10 (user yêu cầu, sau merge): products-copy-ui lượt 1 NB5 đỏ = LỖI THẬT — isFormDirty đòi `ready`, mà dải nguồn hiện trước khi form-options về ⇒ bấm Quay lại sớm thoát không hỏi (tái hiện MCP ready=false popup 0). Sửa bỏ điều kiện ready (ProductForm.vue, CHƯA commit — ngoài commit c0062eabf đã push) ⇒ MCP popup 1 ⇒ copy-ui 7/7 passed. 3 spec cũ: read-ui 13 passed; lifecycle 8 passed + 1 skip + N1 đỏ (spec INSERT roles.company_id — DB gộp không có cột, giống NB6 đã sửa); form-ui E1 đỏ (spec cũ: nút Tạo mới hiện ở Đang KD từ 21/10) + E10 đỏ (spec cũ: commit 9156d687f 21/10 bỏ bắt buộc Tiểu mục catalog) ⇒ chạy bỏ E1/E10: 15 passed + 1 skip (E4 đã sửa xanh). N1/E1/E10 là spec lỗi thời ngoài luồng — chưa sửa.
Dọn 25/10: DROP hrm_erp_test_saochep; dừng :8011 (PID 5603) :3011 (PID 95399); khôi phục worktree hrm-api/.env + e2e/.auth/user.json từ bản lưu; không tệp S3 nào được ghi (spec không có tài liệu kỹ thuật, PHPUnit mock S3). Worktree giữ lại vì còn bản sửa NB5 chưa commit.
Fix NB5 25/10 (user chọn commit + push): hrm-client 5fb61efc0 trên feat ⇒ fast-forward gop_db ⇒ push cả 2 nhánh (remote = local). Đã xoá worktree websites/wt-sao-chep-hang-hoa + nhánh feat local (nhánh remote giữ).
