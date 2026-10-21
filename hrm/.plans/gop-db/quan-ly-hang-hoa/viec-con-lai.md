# Việc còn lại — feature Chuyển đổi hàng hoá

## 🧭 CÒN LẠI sau 15/10/2026 (bản gom — đọc mục này trước)

### A. Code — chưa có quyết định "để sau" (nên xử lý trước prod)
**A1. Bảo mật / sai số liệu**
| # | Việc |
|---|---|
| ~~N144~~ ✅ 16/10 | ERP `print()` thêm gate `canView()` như `show()` (chưa commit). Kiểm tinker DB giacty: NV không quyền ⇒ `not_found`, người lập ⇒ bản in. Test `N126InlandOrderRequestNewScreenTest::test_n144_…` |
| ~~N145~~ ✅ 16/10 | `stockOfProducts` tra phiếu qua `scopedQuery()` (chưa commit) — nháp người khác/phiếu ngoài phạm vi ⇒ ngữ cảnh rơi về người đăng nhập. FE chỉ gửi id ở màn Sửa (nháp của mình) ⇒ luồng thật không đổi. Test mới `StockOfProductsScopeTest` (đỏ trên code cũ); sửa giả định `StockAndUnitTest::test_ctx_…` (dựng nháp của người 999). Thư mục vẫn 24 đỏ sẵn = N159 |
| ~~N146~~ ✅ 17/10 (merge LOCAL, chưa push) | Đã kiểm: KHÔNG sai số liệu — lưu phiếu BE tự tra giá theo công ty phiếu (`ProductExportRequestService::resolveManualLineMeta` + `CompanyHelper::pricingCompanyId($req)`, không tin giá client). Chỉ lệch HIỂN THỊ: `ProductExportRequestForm::onProductsApply` đặt `price = it.quoted_price` của popup (công ty người đăng nhập) cho dòng mới, trong khi đổi ĐVT lấy giá công ty phiếu (N137) ⇒ chỉ xảy ra khi đổi công ty đang làm rồi sửa nháp; tải lại phiếu là đúng. Sửa (FE): `ManualLinesTable` nạp ĐVT xong thì đặt lại giá dòng mới theo ĐVT hiện tại |
| ~~N147~~ ✅ 16/10 | User chốt "Ẩn nháp người khác". ERP `InlandOrderRequestNew` (chưa commit): `searchByFilter` 3 phạm vi tổng cty/cty/phòng ban gắn `notOthersDraft()`; `canView()` chặn status Đang tạo sau nhánh người lập ⇒ show/print theo. Kiểm tinker (model trong bộ nhớ — DB dev 0 nháp): nháp người khác false, chờ duyệt true, nháp mình true; SQL list có `(status <> 3 or created_by = ?)`. ERP PHPUnit 203 OK. Còn sót: nhánh fallback danh sách `approver_id = tôi` vẫn liệt kê nháp có gán người duyệt (canView đã chặn ⇒ bấm vào not_found) |
| ~~N160~~ ✅ 17/10 (merge LOCAL, chưa push) | (ngoài luồng) ERP `InlandOrderRequestNew::canView()` cho `Super Admin` qua thẳng — trái quy tắc super admin không mặc định có quyền |
| ~~N148~~ ✖ 16/10 báo nhầm | 1527–1530 là guard `api` (HRM), 100870–100873 là guard `web` (ERP) — tách guard đúng thiết kế DB gộp; 0 ánh xạ chéo guard (api↔api 11.143, web↔web 8.363) |
| N161 | (ngoài luồng — `permission:sync` tự gộp, giữ 1115/1116) Trùng tên THẬT cùng guard `api`: "Quản lý danh mục tiền tệ" 1115/1117, "Xem danh mục tiền tệ" 1116/1118 — có cả ở `hrm_erp` lẫn `hrm_erp_giacty`; legacy khai 1115/1116. Gate theo tên ⇒ không hỏng chức năng, nhưng màn phân quyền hiện 2 ô. Kiểm prod rồi dọn 1117/1118 (chuyển role_has_permissions sang 1115/1116) |
| ~~N162~~ ✅ 17/10 (merge LOCAL, chưa push) | (ngoài luồng) API YCXH trả 400 kèm NGUYÊN câu SQL lỗi (`{"code":400,"message":"SQLSTATE[23000]… insert into product_export_requests …"}`) — lộ cấu trúc bảng; cùng loại N103 |
| ~~N163~~ ✅ 17/10 (merge LOCAL, chưa push) | (ngoài luồng) `V2BaseSelectInModal` chưa Việt hoá câu lỗi select2 ⇒ hiện "The results could not be loaded." / "Searching…" (vd ô Model popup BOM) |
| ~~N149~~ ✅ 16/10 soát (tài liệu) | Dry-run giacty: thêm 52 (41 giữ id cũ) · sửa 83 (type NULL→1, nhóm Task→Nhiệm vụ) · gộp trùng 2 (tiền tệ = N161, sync tự dọn) · không khai 8. **4 "lương P3"** = migration đổi tên `2026_10_13_000001_rename_luong_p3…` chưa chạy trên giacty ⇒ thứ tự runbook (migrate §6 trước sync §7) đúng; thêm dấu hiệu DỪNG vào `deploy-dev-server.md` §7. **4 "… danh mục hàng hoá"** (1616–1619) = rác sự cố 21/09, code không dùng, chiếm id legacy của "công nợ đầu kỳ" ⇒ sync chèn id mới, không gán nhầm (đã đọc `PermissionSync::upsert/adoptLegacyPivots`). Còn tuỳ chọn: khai 4 quyền rác vào REMOVED để sync gỡ (cần xin phép code) |

**A2. Ổn định / trải nghiệm**
| # | Việc |
|---|---|
| ~~N150~~ ✅ 16/10 | (chưa commit) Cơ chế: store `apiGetMethod`… ném lại lỗi axios, interceptor không nuốt status nào ⇒ Vue errorHandler của Nuxt (`.nuxt/client.js:63`) ⇒ `layouts/error.vue` luôn "KHÔNG TÌM THẤY TRANG"; 400/404/422 không toast. Khảo sát: ~684 file có await API không bắt lỗi (sai số 15–25%). Sửa: plugin mới `plugins/api-error-guard.js` (client, khai `nuxt.config.js`) BỌC handler Nuxt — lỗi API ⇒ toast `apiErrorMessage` (trừ 401/403/428/500/504 interceptor đã báo, trừ `X-Silent-Errors`) + giữ trang; lỗi code vẫn ra trang lỗi. 2 helper `utils/business-catalog.js`/`vehicle-catalog.js` trả [] khi lỗi (11 chỗ master-data). Đo Playwright trước/sau (trước: 404 cả trang, 0 toast). Spec mới `e2e/tests/shared/api-error-guard-ui.spec.ts` 4/4. Hệ quả: màn nào dựa trang 404 khi mở bản ghi không tồn tại nay hiện toast trên khung trống. Ghi chú: helper bắt lỗi 4xx thì ô trống không toast (interceptor không báo 4xx) |
| ~~N107~~ ✅ 16/10 | (chưa commit) `V2BaseSelectRemote` + `BomBuilderEditModal` (ô Model) transport trả `{ abort }`, bỏ kết quả request đã huỷ. Tái hiện trước khi sửa trên `/sale/customer-debt-by-employee` (500 ⇒ kẹt "Đang tìm..." + pageerror `'status' in undefined`; gõ nhanh ⇒ ô "abc" hiện kết quả "ab") và popup BOM (kẹt "Searching…"). Sau: "Không tải được dữ liệu", gõ tiếp tìm lại được, kết quả mới không bị đè. Spec mới `e2e/tests/shared/select-remote-error-ui.spec.ts` 2/2 (đỏ trên code cũ) |
| N105 | `php artisan route:list` hrm-api lỗi sẵn · ✅ 20/10 đã sửa trong worktree (chưa commit) — xem `ngoai-luong/soat-bang-a-2010.md` |
| N151 | 214 gói bảo dưỡng dev không có file đính kèm mà form HRM bắt buộc ⇒ mở Sửa gói cũ 422 (kiểm prod) |
| N152 | Popup danh mục cũ (vd `BankModel.vue`) báo lỗi bằng `.text-small-error`, ô không viền đỏ · 2 helper song song `scrollToFirstError` / `scrollToInputError` nên gộp |
| N153 | Snapshot HĐ 2 truy vấn giá/dòng (chưa gom lô) · màn duyệt TN mới ERP gọi searchData 7 lần/lần mở (có sẵn) · **A (snapshot HĐ) ✅ 20/10 gom lô (chưa commit); B (ERP searchData) còn mở** |
| N154 | Excel "Loại tài liệu" (Assign) dùng nhãn "loại file đính kèm" (khoá dùng chung) · ✅ 20/10 đã sửa trong worktree (chưa commit) — xem `ngoai-luong/soat-bang-a-2010.md` |
| — | 54 minor hoãn của 4.1–4.5/4.3b — ledger `popup-tim-kiem-hang-hoa/progress.md` (gom 1 đợt dọn) |

**A3. Test / công cụ**
| # | Việc |
|---|---|
| ~~N155~~ ✅ 17/10 spec viết (chưa chạy) | Chưa có spec e2e màn Gói bảo dưỡng (N100) — tài khoản e2e thiếu quyền Thêm/Sửa gói ⇒ spec tự tạo role tạm |
| ~~N156~~ ✅ 16/10 | Bắt được đỏ ở lượt 3/3 chạy MasterData: `xe_cha_con_sai_thi_422` nhận 200. Gốc: ca gọi `chain()` rồi `vehiclePayload()` gọi lại `chain()` — `first()` không ORDER BY trên join 3 bảng (1.278 dòng, 41 hãng) có lúc ra dòng khác ⇒ "Loại xe khác hãng" lại khớp hãng của payload. Sửa test: `chain()` orderBy + nhớ trong ca; otherBrand/otherModel orderBy. Ca "nhớ trạng thái" picker: chưa tái hiện lại |
| ~~N157~~ ✅ 16/10 | `ActsAsProductUser` bỏ id cố định 1652–1658 — quyền thiếu thì tạo id tự sinh (tra theo tên trước như cũ) |
| N158 | e2e 404 ở `/finance/currencies`, `/customer-care/levels`; console "Module parse failed" (webpack đọc file nhị phân) |
| ~~N159~~ ✅ 16/10 | 24 ca đỏ = id giả bị FK chặn trên DB gộp: fixture `customer_id=1` (19 ca, gồm 3 TypeError do tạo phiếu 400), `BranchTransferEditTest` thiếu model_id/brand_id (3), `StockAndUnitTest` công ty/KH/lô giả (2), `DownstreamTest` loại 12 `customer_id=1`. Lấy id có thật ⇒ thư mục 120 ca 0 đỏ (1 skip sẵn) |
| N164 | Role e2e "E2E Assign Admin" (118805) provision 13/10 — chép quyền Super admin lúc đó ⇒ thiếu 9 quyền gán cho Super admin sau (8 quyền xe 2c 1720–1727 + "Xuất excel danh sách hàng hoá") ⇒ 6 ca product-catalog-ui/vehicles-ui đỏ 403 khi chạy `--no-deps`. 16/10 đo bằng role tạm 129854 (đã gỡ): 6 ca xanh. Cần chạy lại provision (`api-setup`) hoặc bổ sung bước cấp quyền |
| ~~N165~~ ✅ 17/10 spec sửa (P7 skip khi role chỉ gắn công ty 1 — N206) | 2 spec giả định dữ liệu quyền: `product-price-approvals-ui` A2 cần tài khoản e2e KHÔNG có 1092 (provision chép từ Super admin ⇒ có ⇒ 15 cột thay 13); `product-prices-ui` P7 đổi company_role = 2 nhưng role chỉ gắn công ty 1 ⇒ route guard ra trang 404. Không liên quan code |
| ~~N166~~ ✖ 17/10 không phải lỗi app (gõ phím thật vẫn hỏi; chỉ `fill()` không phát keydown) | (phát hiện khi chụp SRS 16/10, Playwright 3031) Form **Thêm mới hàng hoá** đã gõ Tên rồi bấm **Quay lại** ⇒ thoát luôn, KHÔNG hỏi "Bạn có thông tin chưa lưu" (`create.vue` dùng `unsavedChildFormMixin`). Chưa thử form Sửa. Testcase TC_04.015 |
| ~~N167~~ ✅ 17/10 (merge LOCAL, chưa push) | (16/10) Câu xác nhận Khóa / Mở khóa / Gỡ ghi "tại công ty đang làm việc" thay tên công ty — `currentCompanyName()` đọc `store.company_roles` rỗng với tài khoản e2e_assign (có thể chỉ do dữ liệu tài khoản); kiểm với tài khoản thật. Cùng gốc: tiêu đề số đếm màn Cập nhật giá bán cũng ghi "tại công ty đang làm việc"; popup xác nhận Duyệt giá bán ra "…ghi vào công ty công ty đang làm việc." |
| ~~N168~~ ✅ 17/10 (merge LOCAL, chưa push) | (16/10) FE ↔ BE lệch ở form hàng hoá: Bảo hành FE cho số lẻ / BE `integer`; Hệ số thuế BVMT FE `min=0` / BE `min:1`; nhãn "Loại tài liệu" không có * nhưng BE bắt buộc khi có dòng |
| ~~N169~~ ✅ 17/10 (merge LOCAL, chưa push) | (16/10, hỏi nghiệp vụ) (a) Khoá hàng không chặn/huỷ yêu cầu duyệt giá đang chờ — duyệt vẫn áp giá cho hàng khoá; (b) thêm ĐVT cho hàng Đang KD ⇒ ĐVT mới giá 0 vẫn vào popup chứng từ; (c) hàng 2/5 vẫn sửa được toàn bộ, lệch chốt cũ §26c-bis. Testcase TC_09.016 / TC_09.010 |
| ~~N170~~ ✅ 17/10 (merge LOCAL, chưa push) | (SRS Cập nhật giá bán 16/10) Lần nạp đầu, dòng **TMĐT** hiện giá trị DB chứ không theo công thức T5 (`productPriceModel.js`): TEWI-AQUA TMĐT 0 / Bán lẻ 341.000.000; sửa ô bất kỳ là TMĐT nhảy 443.300.000 và Lưu ghi giá trị đó |
| ~~N171~~ ✅ 17/10 (merge LOCAL, chưa push) | (16/10) Màn Cập nhật giá bán: nhảy tới lỗi ô Giá vốn thì ô bị cột dính "ĐVT · Lưu" che 29px (ô left 576 < cột dính right 605) ⇒ chữ lỗi khuất một phần |
| ~~N172~~ ✅ 17/10 (merge LOCAL, chưa push) | (16/10, hỏi nghiệp vụ, thừa kế ERP) Đề xuất giá bị từ chối vẫn nằm trong ô "Giá mới"; ở công ty không bật duyệt, sửa 1 ô rồi Lưu là áp luôn các giá đã bị từ chối thành giá hiệu lực |
| ~~N173~~ ✅ 17/10 (merge LOCAL, chưa push) | (16/10) FE gán cứng hệ số TMĐT 1,3, BE đọc theo cấu hình từng công ty ⇒ công ty cấu hình khác thì màn hình xem trước và giá lưu lệch nhau |
| ~~N174~~ ✅ 17/10 (merge LOCAL, chưa push) | (SRS Duyệt giá bán 16/10) Không duyệt với lý do > 2000 ký tự: popup đóng, mất lý do đã gõ, toast tiếng Anh "The given data was invalid." |
| ~~N175~~ ✖ giữ như ERP | (16/10, hỏi nghiệp vụ) Người duyệt sửa Bán lẻ ở màn Duyệt thì TMĐT không tính lại và 4 loại giá khác không lan theo — lệch luật TMĐT = Bán lẻ × hệ số mà BE ép ở đường lưu thẳng (Cập nhật giá bán) |
| ~~N176~~ ✅ 17/10 (merge LOCAL, chưa push) | (16/10) Hệ số → giá ở dòng giá hiệu lực: màn Duyệt làm tròn tới trăm, màn Cập nhật giá bán làm tròn tới đồng |
| ~~N177~~ ✅ 17/10 (merge LOCAL, chưa push) | (16/10) Ẩn giá vốn không đồng nhất: bảng + Excel màn Duyệt ẩn khi thiếu 1092, popup Lịch sử giá chỉ ẩn khi thiếu CẢ 1657 và 1092 |
| ~~N178~~ ✅ 17/10 (merge LOCAL, chưa push) | (16/10) Không duyệt hàng loạt không báo số yêu cầu bị bỏ qua (đã có người xử lý), Duyệt hàng loạt có báo |
| ~~N179~~ ✅ 17/10 (merge LOCAL, chưa push) | (16/10, giao diện) Chữ lỗi ô Hệ số ở màn Duyệt xuống dòng từng chữ trong cột rộng 72px |
| ~~N180~~ ✅ 17/10 (merge LOCAL, chưa push) | (SRS YC hỏi giá 16/10, giao diện) Bung dòng nhóm có chữ "Chờ <tên> duyệt" làm cột Hành động giãn 100 → 186px ⇒ bảng 1222px trong khung 1139px, cuộn ngang, cột Hành động bị che một phần (đo DOM 1440px) |
| ~~N181~~ ✅ 17/10 (merge LOCAL, chưa push) | (16/10) Màn Hàng đang kinh doanh: khi đang hiện dải "chưa xếp catalog" thì thanh hàng loạt "Đã chọn N" (Lập YCHG / Bỏ chọn / Xếp catalog) không bao giờ hiện — V2BaseDataTable chỉ render slot toolbar HOẶC left-actions |
| ~~N182~~ ✅ 17/10 (merge LOCAL, chưa push) | (16/10) Form Sửa phiếu YCHG Không duyệt không hiện lý do PTKD từ chối |
| ~~N183~~ ✅ 17/10 (merge LOCAL, chưa push) | (16/10) YCHG: ô lọc "XNK tiếp nhận" lọc theo XNK đã lưu trên nhóm, cột hiển thị XNK đang được phân công ⇒ đổi phân công sau khi gửi là lệch |
| ~~N184~~ ✅ 17/10 (merge LOCAL, chưa push) | (16/10) YCHG: "PTKD duyệt" (cột + ô lọc) gồm cả người đã từ chối phiếu |
| ~~N185~~ ✅ 17/10 (merge LOCAL, chưa push) | (16/10, nhẹ) YCHG: ô lọc Người tạo liệt kê cả người chỉ có phiếu nháp / Không duyệt mà người xem không thấy |
| ~~N186~~ ✅ 17/10 (merge LOCAL, chưa push) | (SRS YC tính giá 16/10, hỏi nghiệp vụ) Lưu nháp YCTG "Không duyệt" đưa phiếu về "Đang tạo": mất lý do từ chối, người khác hết thấy, xoá được — trái T4-Q3 (Không duyệt chỉ sửa rồi gửi lại) |
| ~~N187~~ ✅ 17/10 (merge LOCAL, chưa push) | (16/10) YCTG: thao tác từ chối của KTMH có 4 tên (nút "Từ chối" · trạng thái "Không duyệt" · lịch sử "KTMH không duyệt" · thông báo "Yêu cầu làm lại"); thông báo gửi ghi "Chờ duyệt" trong khi trạng thái "Chờ tính giá" |
| ~~N188~~ ✅ 17/10 (merge LOCAL, chưa push) | (16/10) YCTG: lỗi BE "Nhóm không còn hàng hoá nào có đơn vị tính" không có chỗ hiện trên form ⇒ bấm Lưu như không có gì xảy ra |
| ~~N189~~ ✅ 17/10 (merge LOCAL, chưa push) | (16/10) YCTG: số vượt giới hạn báo khác nhau — FE "Không hợp lệ", BE "Không được lớn hơn 999,999,999,999." |
| ~~N190~~ ✅ 17/10 (merge LOCAL, chưa push) | (16/10) YCTG: cột Chi phí màn chi tiết tính lại theo tỷ lệ, bản in lấy số đã lưu ⇒ phiếu ERP cũ lệch (PYCTG-03162: màn 1,958,654 / in 1,959,031) |
| ~~N191~~ ✅ 17/10 (merge LOCAL, chưa push) | (16/10, nhẹ) YCTG: thông báo không quyền hiện 2 toast trùng; ô lọc Thương hiệu/Hãng/Người tạo gồm cả dữ liệu từ nháp người khác (cùng kiểu N185) |
| N192 | (16/10, VPS test) DB test KHÔNG có dòng giá Cty 2 (HP): lệnh chép giá chạy 15/10 14:01 theo luật cũ (nhóm 1·3·4, `0a598827e`), trước N128 (`06867a1e5` 23:14, HP vào nhóm 1·2·3·4) ⇒ cần chạy lại chép giá cho HP trên test (ghi DB — hỏi riêng). Cùng đợt: ERP test từng hiện 505.730 (= giá Cty 1 × 1,03 không tròn, kiểu code cũ) trong khi HRM 506.000; sau khi giá được lưu lại 2 bên khớp 528.700 ⇒ nghi ERP test lúc đó chưa nạp code mới — deploy xong phải reload php-fpm/opcache |
| ~~N193~~ ✖ giữ tròn đồng | (16/10, hỏi nghiệp vụ) Giá TMĐT = Bán lẻ × 1,3 làm tròn tới ĐỒNG (luật ERP gốc `round($retail * $ecom)`, HRM chép y) ⇒ DB lưu số lẻ (690.170, 687.310). Có muốn đổi sang tròn nghìn không |
| ~~N194~~ ✖ 16/10 user đóng: đúng quy ước | **Không phải dữ liệu lỗi — quy ước nghiệp vụ từ 2022**: dòng giá dự kiến Bán lẻ 1 đ / hệ số 0 ngày 31/12 do người dùng nhập ở PTG (ERP `PriceCalculate.php:499` chép nguyên `expected_prices` của phiếu; không có code/cron nào tự sinh). Năm nào cũng có: 31/12/2022: 225 · 2023: 647 · 2024: 1.692 · 2025: 3.081 (đều đã áp) · 2026: 6.755 (chờ áp; 6.415 của NV 1027 minhnt.da1; ~5.994 dòng tạo 10/10 = bản chép sang công ty nhận khi backfill). Bán lẻ 1 đ = "chưa có giá / phải tính lại": hiện Cty 1 có 32.092/46.487 dòng Bán lẻ ≤ 1 đ. Còn: nghiệp vụ xác nhận quy ước; PTG HRM giữ được thao tác nhập giá dự kiến 31/12 |
| ~~N195~~ ✅ 17/10 (merge LOCAL, chưa push) | (16/10) Màn PTG dùng câu của YCTG: toast thiếu quyền "Bạn không có quyền xem yêu cầu tính giá" (hiện 2 lần); nhóm đóng "…yêu cầu tính giá chỉ còn xem." |
| ~~N196~~ ✅ 17/10 (merge LOCAL, chưa push) | (16/10) PTG đã lưu giá hiệu lực ⇒ TMĐT hiện 2 dòng "giá sẽ áp dụng"; dòng đầu nhập được nhưng BE bỏ qua (thấy ở PTG-02618; mọi PTG HRM có giá hiệu lực Bán lẻ) |
| ~~N197~~ ✅ 17/10 (merge LOCAL, chưa push) | (16/10, giao diện) Popup Chọn YCTG ở 1440px: bảng 841px trong khung 726px, nút Chọn ngoài khung (left 1116 > right 1083) ⇒ phải cuộn ngang |
| ~~N198~~ ✅ 17/10 (merge LOCAL, chưa push) | (16/10) PTG chi tiết + bản in tính lại chi phí theo tỉ lệ ⇒ lệch giá vốn đã áp (PTG-03178: hiện 13,108,667 / lưu 13,108,986) — cùng gốc N190 |
| ~~N199~~ ✖ giữ | (16/10, hỏi nghiệp vụ) PTG: "Giá nhập kho" (sẽ thành giá vốn công ty phiếu) không che theo 1092, bản in cũng in |
| ~~N200~~ ✅ 17/10 (merge LOCAL, chưa push) | (16/10, hỏi nghiệp vụ) PTG: Lưu và duyệt / gửi duyệt ghi đè "Lý do sửa giá" của ĐVT thành "Phiếu tính giá PTG-x" |
| ~~N201~~ ✅ 17/10 (merge LOCAL, chưa push) | (16/10, lệch tài liệu) PTG: xoá phiếu người khác trả "Trạng thái đã bị thay đổi…" (t5-plan ghi: không có quyền); C20 ghi cột Hành động có "Xem", code không có |
| ~~N202~~ ✅ 17/10 (merge LOCAL, chưa push) | (16/10, nhẹ) PTG: ô chọn ngày giá hiệu lực mở ra đè chữ lỗi "Bắt buộc phải chọn" |
| ~~N203~~ ✅ 17/10 (merge LOCAL) — báo giá, BOM, mượn hàng, giữ hàng; ô đang chọn: tên + chấm đỏ + tooltip | (16/10, phát sinh khi làm N169(b)) Ghi chú "(Chưa có giá)" mới có ở popup chọn hàng + ô ĐVT YCXH; các màn chứng từ tự dựng danh sách ĐVT (báo giá `quotations/_id/edit.vue`, BOM, mượn hàng, huỷ giữ hàng…) chưa có — không có helper chung |
| N204 | (16/10, ngoài luồng, cùng kiểu N160) ERP còn bypass `hasRole('Super Admin')`: `InlandOrderSummaryNew.php:893,941`, `InlandOrderNotificationNew.php:299`, `InlandPurchaseInvoice.php:631,656,707`, `InlandBuyContractNewController.php:253`, `InlandOrderNotificationNewController.php:172` |

### B. User đã chốt "để sau"
N101 Bảo hành hãng tìm toàn bộ hàng · N90 báo cáo CSKH/Tổng hợp bán hàng đọc bảo hành cột chung · N83 gỡ chip select2 · A4 popup hàng công ty khác · A5 (N34 N36) bỏ hệ số giá · N35 hệ số đóng băng tới Phase 8 · A6 2-bc báo cáo theo công ty · A11 bắt buộc Đặc tính hàng thường · N5 cron giá về 0 · N64-rest / N80 lịch sử & YC xuất hàng lộ tài chính · N113 index đời xe (theo dõi) · N115 thiết bị KTSC 403.

### C. Dữ liệu / nghiệp vụ trước go-live
> **16/10 — B6 + catalog + bỏ Nhóm hàng: xem `catalog-import/README.md`** (tạm dừng; chờ nghiệp vụ sửa file cây theo `can-sua-cay-phan-loai-1610.xlsx`, chờ user trả lời Q1–Q5 đề xuất bỏ Nhóm hàng).

B6 🔴 nhập cây phân loại + quy đổi 45.890 hàng + xếp catalog (dev: Loại SP 0 dòng — gói bảo dưỡng hiện "Chưa phân loại" hết) · B5 🔴 nhập Đặc tính · 🔴 cờ "Hàng hoá làm dịch vụ / Dùng cho báo giá dịch vụ" trên Tính chất · B1 cờ phụ tùng ô tô · B2 Cty 5/6/8 mốc tắt · B4 dọn 30 phiếu hỏi chéo công ty (T-7) · dọn hàng tạm ERP chờ duyệt · gán quyền nghiệp vụ (tra theo TÊN) · A9 nghiệm thu Phase 1/2b/2d/48 màn · A10 dữ liệu thử "lấy về" · N126 kiểm lại 2 màn chờ duyệt TN mới trên dữ liệu thật (dev không có phiếu 2/6).

### D. Deploy
> 16/10 tối: kéo `develop` vào nhánh chung hrm-api (`c85a59031`, chủ ý — code HĐ HRM mới: Điều kiện thanh toán). Đã chạy vào **giacty** 2 migration `2026_10_16_000001/000002` (payment_conditions + 2 cột `hrm_contract_process_payments`) + `PaymentConditionsTableSeeder` (8 dòng). Prod/VPS cần chạy tương tự. PriceReaderWhitelist 2/2 · MasterData 551 · Assign 23 OK.

ERP prod `HRM_API_BASE_URL` + `config:cache`, `IS_USE_SSO=true`, thử staging SSO · runbook `gia-theo-cong-ty/runbook-trien-khai.md` + `deploy-dev-server.md` (quyền = `permission:sync`; backfill luật 1·2·3·4 ⇒ TỔNG ~1,04 triệu, ra ~810 nghìn là code cũ ⇒ DỪNG) · migration `2026_10_15_000001` (gói BD) + 23 migration gop_db chưa chạy giacty + `2026_10_12_000000_change_exchange_rate…` · prod đếm lại `quotations`/`contracts` cũ · công ty 9 chỉ có trên VPS/prod — đối chiếu lại dry-run.

## 📌 Phiên 15/10/2026 tối — nhánh con `feat/cdhh-viec-ton-1510` ĐÃ MERGE nhánh chung + ĐÃ PUSH 15/10: api `46385a8b4`, client `495c4eecf`, ERP `f43a663f5d` (nhánh con đã xoá local)

| # | Việc | Trạng thái |
|---|---|---|
| N137 🔴 | 3 file đọc giá theo công ty chứng từ (ContractService, YCXH picker + service) + FE `ManualLinesTable` gửi `product_export_request_id` | ✅ code + PHPUnit (MasterData 547/547) + Playwright |
| N139 | Gỡ khoá trùng `attachment_types` (giữ bản đang hiệu lực) | ✅ |
| N138 | Runbook → `permission:sync` ✅; gỡ 4 seeder quyền id cố định + 4 test, thay `ProductPermissionsDeclaredTest` + trait `EnsuresDeclaredPermissions` | ✅ |
| N130 | Popup chọn hàng: lỗi search hiện khối lỗi + Thử lại | ✅ Playwright; spec +2 ca |
| N94-rest | ERP gỡ @json danh mục trong `searchProductJs` (~15 truy vấn/trang), gỡ include thừa 7 view, `availableGroup` ở sync_products | ✅ PHPUnit + Playwright 9 trang 0 lỗi JS (self_inventory show chưa kiểm — bảng rỗng) |
| N100 🔴 | Gói bảo dưỡng: Loại SP lấy TỪ HÀNG (không mapping), `group_id` nullable (migration `2026_10_15_000001…` ĐÃ CHẠY giacty, batch 439), Excel bỏ cột Nhóm hàng, ERP màn gói chạy tiếp (nhóm null ⇒ "Chưa xác định") | ✅ PHPUnit HRM 5/5 · ERP 197; Playwright HRM + ERP. Thiếu spec e2e màn gói |
| N128 | Đo: 668 chứng từ HP dở ⇒ user chốt HP VÀO nhóm chia sẻ 1·2·3·4 (`config/price.php`) | ✅ test 13/13, compare 113.484 cặp 0 lệch; giacty khớp — hết việc "dọn giacty" phần HP |
| N133 | Công ty 9 tự quản: `self_managed_company_ids` = [7, 9] | ✅ |
| N95 | Cột tồn lắp ráp popup ERP | ❌ user: không đưa lại |
| N104 | Quyền xe 2b lệch id | ✅ hết tác động — seeder đồng bộ theo TÊN, code gate theo tên |
| N88 · N92 · N142 | e2e: `api.setup.ts` đọc `API_REPO`/`PHP_BIN` env · nocost spec đọc FX · Mẫu in tem chờ request product-natures | ✅ sửa spec (chưa chạy) |
| N126 · N127 | ERP TN mới: `type` giữ nghĩa loại đặt hàng (menu gửi ?type=1/2 vốn đúng), tên màn sang tham số `screen`; Chờ duyệt = status 2 + approver_id = tôi, Chờ TP duyệt = status 6 + department_approver_id = tôi (bám canApprove/canDepartmentApprove + InlandOrderRequest2 — user xác nhận 15/10); nút In chi tiết | ✅ PHPUnit ERP 201; Playwright: Danh sách 4.990 = SQL, type 1/2 = 3.489/1.501; 2 màn chờ duyệt 0 = 0 (giacty không có phiếu 2/6) |
| N122 · N123 | `fieldsBagName: 'veeFields'` (grep: 0 chỗ đọc túi cờ vee qua `fields`) · `scrollToInputError`: bỏ lỗi ẩn, bỏ dấu `*`, nhận `.v2-error`/`.invalid-feedback` hiện/`.is-invalid` (+ `.text-small-error`/`.field-error`/`.cell-invalid` — user giữ 15/10), ưu tiên popup trên cùng (user giữ), focus ô 1 lần cuộn | ✅ Playwright: cảnh báo 1–2 ⇒ 0; số ô lỗi trước = sau; spec mới `tests/shared/scroll-to-error-ui.spec.ts` 9 ca (chưa chạy). Rủi ro: 89 nơi gọi helper |
| N140 · N130b | Popup chọn hàng: bấm ảnh mở FilePreviewModal z 5100 (bám gop_db f4b44b9d9, 1 ảnh `avatar`) · số đếm cây lỗi ⇒ dòng "Không tải được số lượng — Thử lại" · "Chọn tất cả" gom đủ trang rồi mới áp, lỗi giữ lựa chọn cũ + khối báo (trước đây lỗi làm SẬP cả trang thành 404, mất form đang nhập) | ✅ Playwright; spec +3 ca (chưa chạy) |
| N103 · N143 | Hãng xe trùng tên bản ghi khoá ⇒ 422 (chỉ `vehicle_manufacts` có UNIQUE trong 2b) · `product-units?product_export_request_id` tra phiếu qua `scopedQuery()` như `show`, không thấy ⇒ 404 | ✅ test 3+3; MasterData 551 (1 đỏ chập chờn `VehicleCatalog2cTest::xe_cha_con_sai_thi_422` — `chain()` dùng `first()` không ORDER BY) · Assign 23 OK |
| N141 | Role tạm 126621 (8 quyền 1720–1727) cho NV e2e 1180 khi chạy e2e, xong ĐÃ GỠ (roles 130 · rhp 20.967 · ehr 1.718 = mốc trước) | ✅ |
| e2e 15/10 tối | worktree 3031/8031, --workers=1: product-picker-filters-ui **12/12** (sửa spec N140 chờ focus vào preview trước Escape; 1 lượt ca "nhớ trạng thái" đỏ không tái hiện) · scroll-to-error-ui **9/9** · product-catalog-ui **31/31** (lượt 1 có 4 ca timeout 30s do biên dịch/API chậm, lượt 2 xanh — gồm 5 ca N141 + N142) · quotation-unit-select + nocost **2/2** | ✅ |

Ghi mới (ngoài luồng, chưa sửa): popup danh mục cũ (vd `BankModel.vue`) báo lỗi bằng `.text-small-error`, ô không viền đỏ · 2 helper song song `scrollToFirstError` / `scrollToInputError` nên gộp · e2e 404 ở `/finance/currencies`, `/customer-care/levels` · mẫu "async handler không try/catch ⇒ Nuxt thay cả trang bằng 404 khi API lỗi" cần rà toàn app · console "Module parse failed" (webpack đọc file nhị phân) · ERP `InlandOrderRequestNewController::print` không kiểm canView · màn duyệt TN mới gọi searchData 7 lần/lần mở (có sẵn) · Danh sách TN mới phạm vi tổng công ty hiện phiếu Đang tạo của người khác · `stockOfProducts` YCXH tra phiếu bằng `find()` không gate quyền xem · tên quyền "Xem yêu cầu xuất hàng theo …" trùng (id 1527–1530 và 100870–100873) · `VehicleCatalog2cTest::chain()` chập chờn · 214 gói bảo dưỡng dev không có file đính kèm mà form HRM bắt buộc ⇒ mở Sửa gói cũ 422 · `QuotationProductSearchModal` thêm hàng vào YCXH lấy `quoted_price` theo picker báo giá (có thể lệch công ty phiếu) · Snapshot HĐ 2 truy vấn/dòng · Excel Loại tài liệu (Assign) dùng nhãn "loại file đính kèm" · `ActsAsProductUser` còn chèn quyền theo id cố định 1652–1658 · dry-run `permission:sync` báo 8 quyền DB không khai + 41 quyền tạo theo id legacy (soát trước prod).

## 📌 Bản tổng hợp 14/10/2026 (thay cho số đếm cũ bên dưới)
Đã xong & ĐÃ PUSH tới 14/10: Phase 1, 2-A…2-D, 2d cây catalog, Phase 6 hàng tạm, Phase 7 (T1–T7), giá theo công ty G0–G6, bảng C đợt C-a…C-f (N1 N13 N14 N26 N27 N32 N33 N39 N41–N46 N49–N51 N54 N58–N63 N65 N67 N68 N73–N78 N81 N89 + A8), A7 Phase 3 (đóng — đã hấp thụ), Phase 4 (4.1–4.5 + 4.3b), Phase 5.

### 1. Còn phải làm (code) — trước lên prod
| # | Việc | Ghi chú |
|---|---|---|
| A7-2c | ✅ Phase 2c — Biển số · Lái xe ngoài · Danh mục xe · Nhiên liệu + ERP chặn ghi 10 danh mục xe | XONG + ĐÃ PUSH 14/10 (api `8f5990cca`, client `cf5efd2ea`, ERP `ca5fa294de`); checklist deploy gán quyền trong `plan-2c.md` |
| N100 🔴 | Gói bảo dưỡng: `service_has_products.group_id` → id Loại SP theo mapping user cung cấp (migration + chuyển dữ liệu + ERP đọc) | task riêng; CHẶN GO-LIVE |
| A3 | 2-E Excel hàng hoá (Catalog chỉ ghi Tiểu mục) + nghiệm thu "ERP không vỡ" 14 bước | Excel XONG (merge 15/10 api `b38852de0`, client `0469c32a3`, ĐÃ PUSH); nghiệm thu lượt 2: 12 đạt · B2 đạt một phần (iii chỉ đo bằng SQL/API 403) · B3' không đạt ⇒ N111 đã sửa 15/10 (ERP `bfbd794503`, ĐÃ PUSH 15/10) — `excel-nghiem-thu-2e/nghiem-thu.md` |
| ~~N79~~ | ERP `WrServiceQuotation.php:1072,1308` `$service` chưa khai báo | lỗi cũ  ✅ sửa 15/10 (ĐÃ PUSH) |
| ~~N82~~ | Xuất Excel báo giá KHÔNG theo BOM 400 `$show_children` | lỗi cũ  ✅ sửa 15/10 (ĐÃ PUSH) |
| ~~N84~~ | Bảng `product_vehicle_model_has_life` thiếu index `product_id` (80k dòng) | cần migration  ✅ sửa 15/10 (ĐÃ PUSH) |
| ~~N85~~ | Lỗi BE `galleries.N` không có chỗ hiện ở FE | nhỏ  ✅ sửa 15/10 (ĐÃ PUSH) |
| ~~N86~~ | Ô chọn hàng kèm theo chưa lọc hàng đang khoá ở công ty | nhỏ  ✅ sửa 15/10 (ĐÃ PUSH) |
| ~~N87~~ | `ProductFormVehicles` "Đang tải…" dùng `.text-muted` (= đỏ) | nhỏ  ✅ sửa 15/10 (ĐÃ PUSH) |
| N88 | e2e `api.setup.ts` ghim `API_REPO` checkout chính | công cụ test |
| ~~N91~~ | HRM `AdminData::source` đọc cả dòng hệ số status NULL (lệch ERP 23 dòng) | nhỏ  ✅ sửa 15/10 (ĐÃ PUSH) |
| N92 | Spec e2e `quotation-unit-select-nocost` gõ cứng giá cũ | spec |
| N94-rest | Catalog `@json` trong `searchProductJs` còn ~70 trang đọc; `sync_products` gọi `availableGroup` không có | dọn sau 4.5 |
| ~~N97~~ | ERP YC đặt hàng NK 2 / TN mới thêm hàng tay lỗi `unit_coefficient` (+ TN mới thiếu create/edit) | lỗi cũ từ 01/2024  ✅ sửa 15/10 (ĐÃ PUSH) |
| ~~N98~~ | ERP Chi tiết KH (2 KH) lỗi JS khi mở | lỗi cũ, chưa khảo sát  ✅ sửa 15/10 (ĐÃ PUSH) |
| ~~N99~~ | HRM `ChooseEquipmentTypeModal` không nhận chọn loại | cần kiểm tay  ✅ sửa 15/10 (ĐÃ PUSH) |
| ~~N129~~ | Popup chọn hàng HRM: lọc Thương hiệu/Hãng SX/Xuất xứ ra 0 hàng + bố cục ô tag + công tắc lệch + đổi nhãn "Gồm hàng ngoài catalog" | ✅ sửa 15/10 (client merge `995dfb554`, ĐÃ PUSH 15/10 (client `41085f380`, ERP `4462d1178b`)) |
| N130 | Popup HRM nuốt lỗi 422 thành "0 hàng" — xem `soat-bang-c.md` (N131 nhãn ERP ✅ 15/10 `0441a83b9d`) | ngoài luồng |
| N137 🔴 | 3 file gop_db đọc giá không theo công ty (Doanh số tiêu chuẩn HĐ, giá bán lẻ YCXH) — sau merge gop_db 15/10 | CHẶN GO-LIVE, user: làm sau |
| N141 | Tài khoản e2e thiếu 4 quyền Phase 2c (1720–1727) ⇒ 5 ca product-catalog-ui đỏ — xem `soat-bang-c.md` | ngoài luồng (e2e) |
| N142 | Spec "Mẫu in tem" bấm Tạo mới quá sớm, popup chưa mở — có sẵn | ngoài luồng (e2e) |
| N138 · N139 · N140 | ~~Runbook đổi sang `permission:sync`~~ ✅ 15/10 (`deploy-dev-server.md` §7 + cảnh báo `runbook-trien-khai.md`; còn phần code: gỡ 4 seeder quyền riêng + test) · khoá trùng `attachment_types` · port "xem trước ảnh" vào popup chọn hàng | chờ |
| ~~N132 N134 N135 N136~~ | Popup chọn hàng: panel 280px · cấu hình cột bấm sớm + STT · bảng theo mẫu MISA (1 dòng + tooltip đen, mặc định 20) — HRM + ERP | ✅ ĐÃ PUSH 15/10 (client `41085f380`, ERP `4462d1178b`) |
| N122, N123, N126, N127, N128 + dọn giacty luật giá cũ | Lỗi mới 15/10 (N112 N114 N116 N120 N121 đã sửa; N113 N115 để sau) — xem `soat-bang-c.md` | chờ chốt |
| — | Minor hoãn của 4.4 / 4.5 / 4.3b (ledger `popup-tim-kiem-hang-hoa/progress.md`) | gom 1 đợt dọn |

### 2. Chờ user chốt / để sau (⏸)
| # | Việc |
|---|---|
| N95 | Cột "tồn lắp ráp" trong popup chọn hàng báo giá ERP — có đưa lại không |
| N103 | Gỡ UNIQUE DB `name` (biển số, nhiên liệu, hãng xe) để tạo lại tên đã khoá — Hãng xe 2b trùng tên lộ lỗi SQL — user 14/10: làm sau |
| N101 | Bảo hành hãng ERP (`firm_warranty_*`) có tìm toàn bộ hàng không — user: xử lý sau |
| N104 | Quyền xe 2b lệch id DB (1620–1631) vs seeder (1640–1651) — soát trước deploy |
| N105–N107 | `route:list` hrm-api lỗi sẵn · e2e mẫu in tem Loại SP đỏ · `V2BaseSelectRemote` TypeError khi request lỗi |
| N90 | Báo cáo CSKH + Tổng hợp bán hàng đọc bảo hành cột chung — user tính sau |
| N83 | Gỡ chip select2 nhiều lựa chọn — cần kiểm tay |
| A4 | Popup "Xem hàng hoá Công ty khác" (L6) |
| A5 (N34 N36) | Bỏ hẳn hệ số giá: 2 cron + 3 màn xem giá ERP, Cập nhật giá theo hãng — "chuyển sau" |
| N35 | Hệ số giá đóng băng — chấp nhận tới Phase 8 |
| A6 | 2-bc Báo cáo hàng hoá theo công ty |
| A11 | Bắt buộc Đặc tính ở form hàng thường — chờ dữ liệu cũ |
| N5 | Cron giá về 0 khi hết tồn bỏ sót hàng HRM |
| N64-rest · N80 | Route lịch sử chung chưa gate (chứng từ tài chính) · YC xuất hàng lộ tài chính HĐ — ngoài feature, việc riêng |

### 3. Trước go-live — dữ liệu / nghiệp vụ (không phải code)
| # | Việc |
|---|---|
| B6 🔴 | Nhập cây phân loại (Tính chất › Nhóm CN › Nhóm SP › Loại SP) + quy đổi 45.890 hàng + xếp catalog — dev gần rỗng; popup mới mặc định chỉ hiện hàng đã xếp catalog |
| B5 🔴 | Nhập danh mục Đặc tính (0 dòng) — hàng tạm bắt buộc |
| — 🔴 | Khai cờ "Hàng hoá làm dịch vụ" / "Dùng cho báo giá dịch vụ" trên Tính chất (vật tư theo máy / gói BD / vật tư thay thế đang ra 0 hàng) |
| B1 | Tick cờ phụ tùng ô tô (`is_auto_parts`) cho Tính chất thật |
| B2 | Cty 5/6/8 loại bỏ: mốc tắt tài khoản / chứng từ dở |
| B4 | Dọn 30 phiếu hỏi chéo công ty còn dở ở ERP (T-7 ngày) |
| A9 | Nghiệm thu Phase 1 · 2b · 2d · 48 màn `bang-man-hinh-menu.md` |
| A10 | Dựng dữ liệu thử "lấy về" khi nghiệm thu |
| Deploy | ERP prod khai `HRM_API_BASE_URL` + `config:cache`, giữ `IS_USE_SSO=true`, thử staging có SSO (đường cookie `jwt_token`); chạy runbook `gia-theo-cong-ty/runbook-trien-khai.md`; migration gop_db `2026_10_12_000000_change_exchange_rate…` chưa chạy giacty/hrm_erp; prod đếm lại `quotations`/`contracts` cũ |

---

## (Bản soát 12/10/2026 — giữ để tra)

> Gom từ `SO-CHOT-VA-TON.md` §2 + `2c-ghi/chot.md` (Việc ngoài luồng N1–N53) + `gia-theo-cong-ty/design.md` (N54–N70)
> + `gia-theo-cong-ty/g2-plan.md` (N71–N75) + plan T1–T7 Phase 7.
> Trạng thái mỗi mục = đã đối chiếu plan/kết quả kiểm của đợt xử lý (cột Căn cứ). Chưa đối chiếu được ⇒ ghi "⬜ còn".
> Ký hiệu: ✅ đã xử lý · ⬜ còn phải làm · ⏸ user chốt để sau · ❌ user bỏ · ❓ cần user chốt có thuộc lần lên prod này không.
> 🔴 Nguyên tắc: feature lên prod MỘT lần; việc ngoài luồng phải xong hết trước khi merge prod (tiền đề 9).

## Thứ tự đề xuất (user đồng ý 12/10)

1. **T7** chặn ERP luồng tính giá + nghiệm thu Phase 7 — plan `luong-tinh-gia/t7-plan.md`, chờ "làm" (phạm vi §5)
2. **Phase 6** Danh mục hàng tạm — chưa mở (user 10/10: chuyển hết sang HRM trong lần này)
3. **Xử lý mục ⬜ ở bảng C** (việc ngoài luồng)
4. **2-E** Excel hàng hoá + nghiệm thu "ERP không vỡ" 14 bước (`hop-dong-tuong-thich-erp.md`)
5. **Popup "Xem hàng hoá Công ty khác"** (L6 hoãn ở 2-C2)

## A. Phase / đợt chức năng

| # | Việc | Trạng thái | Căn cứ |
|---|---|---|---|
| A1 | Phase 7 T7 — chặn 40 route tính giá ERP, 5 link menu, 3 thẻ dashboard, chạy thử runbook | ✅ 12/10 (ERP `443c812553`, đã lên remote) | `luong-tinh-gia/t7-plan.md` §7–9 |
| A2 | Phase 6 Hàng tạm (phương án mới) | ✅ 13/10 đã push (api 657fa731f, client dc793189e, ERP 396f42dd7c); e2e xanh | `danh-muc-hang-tam/p6-plan.md` |
| A3 | 2-E Excel hàng hoá (Catalog chỉ ghi Tiểu mục) + nghiệm thu ERP 14 bước | 🟡 Excel xong (ĐÃ PUSH 15/10); nghiệm thu 12/14 đạt, N111 đã sửa (ERP `bfbd794503`, ĐÃ PUSH 15/10) | SO-CHOT §2c |
| A4 | Popup "Xem hàng hoá Công ty khác" | ⏸ hoãn (L6) — hiện thay bằng nút "Kho dữ liệu" | `2c-ghi/chot.md` L6 |
| A5 | Bỏ hẳn hệ số giá (tiền đề 8) — N34 cron + 3 màn xem giá ERP, N36 Cập nhật giá theo hãng | ⏸ user 09/10 "chuyển sau" | QC-7, QC-10 |
| A6 | 2-bc Báo cáo hàng hoá theo công ty | ⏸ để sau (04/10) | §27 |
| A7 | Phase 2c (3 danh mục xe còn lại) · 3 (phân quyền theo công ty) · 4 (popup tìm hàng dùng chung) · 5 (gỡ 5 danh mục) | ⬜ **THUỘC lần lên prod này** (user chốt 13/10) — **làm SAU bảng C** (user 13/10), chưa mở cả 4 | SO-CHOT §2 |
| A8 | 5 ca e2e "không quyền" đỏ sẵn (spec chèn `roles.company_id`) | ⬜ | G6 |
| A9 | Nghiệm thu: Phase 1 · 2b · 2d · 48 màn `bang-man-hinh-menu.md` | ⬜ chờ user | — |
| A11 | Bắt buộc **Đặc tính** (`product_characteristic_id`) ở form hàng hoá THƯỜNG — tạm bỏ vì dữ liệu cũ chưa có; cần bổ sung Đặc tính cho hàng cũ rồi mới bật bắt buộc (hàng tạm Phase 6 đã bắt buộc ngay) | ⏸ chờ dữ liệu cũ | user 12/10 |
| A10 | Dữ liệu thử "lấy về": DB giacty 0 mã lấy về được (backfill gán cả 4 công ty status 3) | ⬜ cần dựng dữ liệu khi nghiệm thu luồng lấy về | đo 12/10 |

## B. Trước go-live (thao tác dữ liệu, không phải code)

| # | Việc | Trạng thái |
|---|---|---|
| B1 | N10 tick cờ `product_natures.is_auto_parts` cho các Tính chất phụ tùng ô tô thật | ⬜ |
| B2 | N69/N70 Cty 5/6/8 sẽ loại bỏ: tắt cờ duyệt hàng mới Cty 8, mốc tắt tài khoản / chứng từ dở | ⬜ cần user/khách chốt mốc |
| B3 | Runbook triển khai `gia-theo-cong-ty/runbook-trien-khai.md` + bổ sung bước Phase 7 (T7) | ✅ 12/10 Phần 2 (chạy thử đạt) |
| B6 | **Cây phân loại hàng hoá gần như RỖNG** (giacty + hrm_erp, đo 12/10): Tính chất 1 · Nhóm chức năng 0 · Nhóm SP 0 · Loại SP 0 · Đặc tính 0; 0 hàng có `product_type_id` ⇒ HRM KHÔNG tạo được hàng hoá mới nào (thường lẫn tạm) tới khi nghiệp vụ nhập cây (Phase 0 màn đã có). e2e / kiểm tay phải tự dựng cây thử rồi dọn | ⬜ nghiệp vụ — chặn go-live |
| B5 | Danh mục **Đặc tính sản phẩm** (`product_characteristics`) đang **0 dòng** (giacty + hrm_erp, đo 12/10) — hàng tạm Phase 6 BẮT BUỘC Đặc tính ⇒ phải nhập danh mục trước go-live, nếu không không tạo được hàng tạm | ⬜ nghiệp vụ |
| B4 | D1: dọn 30 phiếu hỏi chéo công ty còn dở ở ERP (production phải = 0 trước deploy) | ⬜ nghiệp vụ, T-7 ngày |

## C. Việc ngoài luồng

> 🔎 **Soát lại 13/10** (chỉ đọc) ⇒ `ngoai-luong/soat-bang-c.md`: đóng N31 · N66 · N64 (phần feature); 16 câu chờ user chốt (Q-N61 trước); đề xuất 5 đợt C-a…C-e.

| # | Việc (tóm tắt) | Trạng thái | Căn cứ |
|---|---|---|---|
| N1 | ERP đọc `min_stock_qty`/`guarantee` chung ⇒ đọc theo công ty chứng từ | ⬜ (2-D ton: "để sau, trước merge prod") | `2d/ton.md:29` |
| N2 | Hãng SX ERP ghi đè `company_id` + xoá dòng hàng × công ty | ✅ 2-D1 (bỏ khối ghi) | `d1-plan` |
| N3 | Thương hiệu ERP ghi đè `company_id` | ✅ 2-D1 (gỡ 2 lời gọi) | `2d/ton.md:10` |
| N4 | Chặn `products/*` ERP chừa danh sách trắng | ✅ 2-D1 | `khao-sat-a` |
| N5 | Cron giá về 0 khi hết tồn bỏ sót hàng HRM | ⏸ để sau các chức năng hàng hoá | chot |
| N6 | `sync:crm` không đẩy hàng HRM | ❌ user bỏ | chot |
| N7 | `->group->` null (popup 338 màn) | ✅ 2-D1 M1–M7 | `d1-kiem-p3` |
| N8 | Popup ERP chọn được hàng công ty đã khoá | ✅ 2-D1 | `d1-kiem-p3` K2 |
| N9 | Popup ERP lọc mất hàng HRM (`product_type` NULL) | ✅ 2-D1 | `d1-kiem-p3` |
| N10 | Cờ phụ tùng ô tô | ⬜ → B1 | |
| N11 | `can_retail` | ✅ 2-D1 P1 gỡ | `d1-plan` |
| N12 | Thiếu tài khoản e2e "chỉ xem hàng hoá" | ⬜ | |
| N13 | Form sửa hàng nhiều đời xe chậm | ⬜ | |
| N14 | Tồn nhỏ 2-C1 (định dạng URL, exists không lọc status, S3 mồ côi, composer.lock) | ⬜ | |
| N26 | 59.710 `product_histories` mồ côi / AUTO_INCREMENT | ⬜ | |
| N27 | Lấy về / sửa đồng thời với khoá không `lockForUpdate` | ⬜ | |
| N28 | `products/change` + 3 route `view-import*` không gate | ✅ 2-D1 gỡ route | `d1-plan` |
| N29 | 4 route `approve*Submit` không kiểm quyền | ✅ G6 chặn (sang HRM) | `g6-plan:35` |
| N30 | `manualUpdatePrices` GET ghi giá | ✅ G6 chặn | `g6-plan:35` |
| N31 | Route `productDelete` khai trùng | ✅ hết tác động (soát 13/10: 2 route đều chặn) ~~⬜~~ (2-D1 chỉ trỏ đích, không đổi tên) | `d1-plan:34` |
| N32 | HRM Thuế suất không lan xuống `products`/`groups` | ✅ C-b 13/10 (ERP `42bbe92ae2` + HRM `5d109a505`, ĐÃ PUSH) ~~⬜~~ | |
| N33 | Hàng HRM không có hàng gốc / hàng gốc lỗi thời | ✅ C-b 13/10 (ERP `42bbe92ae2`, ĐÃ PUSH) ~~⬜~~ | |
| N34 | 2 cron giá + 3 màn xem giá ERP | ⏸ → A5 | |
| N35 | Hệ số giá đóng băng | ⏸ user chấp nhận tới Phase 8 | QC-3 |
| N36 | Cập nhật giá theo hãng | ⏸ → A5 | |
| N37 | `getWareHouseImportLot` 500 hàng không nhóm | ✅ 2-D1 M4b | `d1-plan` |
| N38 | Mẫu tem 1–6 | ✅ 2-D1 (tem theo Loại SP) | `d1-kiem-p3` K6 |
| N39 | ERP CLAUDE.md ghi sai Laravel 8 | ⬜ (tài liệu) | |
| N40 | `brands/list` gọi `importExcelAttribute` | ✅ 2-D1 chặn | `d1-plan` |
| N41 | In tem `twoCode=false` in cả mẫu 2 | ⬜ lỗi cũ | |
| N42 | `product_infos/list` còn nút "Thêm mới" | ✅ C-b 13/10 (ERP `42bbe92ae2`, ĐÃ PUSH) ~~⬜~~ | |
| N43 | `BaseProduct.php:76` `->group->` | ⬜ | |
| N44 | `Product::exportExcel` không null-safe | ⬜ | |
| N45 | ERP `ExampleTest` đỏ sẵn | ⬜ | |
| N46 | In tem phiếu nhập chết Angular | ⬜ lỗi cũ gop_db | |
| N47 | Excel Doanh thu theo hàng hoá 500 | ❌ user bỏ qua 13/10 ~~⬜~~ lỗi cũ | |
| N48 | PDF Doanh thu theo hàng hoá 500 | ❌ user bỏ qua 13/10 ~~⬜~~ lỗi cũ | |
| N49 | Báo giá dịch vụ `reading 'cost'` | ⬜ lỗi cũ | |
| N50 | Báo giá mẫu `infdig` | ⬜ lỗi cũ | |
| N51 | Chi tiết hàng ERP `$parse:syntax` | ⬜ lỗi cũ | |
| N52 | `<title>` trang ngừng sử dụng | ✅ ERP `b2f1761789` | chot |
| N53 | Hàng đang nhập thông tin chọn được ở popup ERP | ✅ ERP `b2f1761789` | chot |
| N54 | 3 luật làm tròn giá × hệ số ERP | ✅ C-a 13/10 (ERP `e7e2ea24c5`, merge + PUSH nhánh chung `3432ca97ac` 13/10) ~~⬜ (hết khi bỏ hệ số — A5)~~ | |
| N55 | Ô lọc Tồn kho màn giá ERP chết | ✅ màn bị chặn ở G6 | |
| N56 | Duyệt hàng loạt ERP sai `price/prices`, `dd($e)` | ✅ màn bị chặn ở G6 | |
| N57 | `manualUpdatePrices` không lọc `flag` | ✅ chặn ở G6 | |
| N58 | Cron 01:00 làm mồ côi cờ chờ duyệt | ✅ C-a 13/10 (ERP `5408c052aa`, merge + PUSH nhánh chung `3432ca97ac` 13/10) ~~⬜~~ | |
| N59 | `getProductsAndPrices` cột sắp xếp tự do | ✅ C-a 13/10 (ERP `b373f1f1cc`, merge + PUSH nhánh chung `3432ca97ac` 13/10) ~~⬜~~ | |
| N60 | `ProductExportsController:766` truyền nhầm `unit_coefficient` | ✅ C-a 13/10 (ERP `0fd8894a5d`, merge + PUSH nhánh chung `3432ca97ac` 13/10) ~~⬜~~ | |
| N61 | `getData` lộ giá vốn cho người không quyền | ✅ C-a 13/10 (ERP `3fcbf36a5c`, merge + PUSH nhánh chung `3432ca97ac` 13/10) ~~⬜ 🔴 bảo mật giá vốn~~ | |
| N62 | `WrServiceQuotation` lấy giá theo thứ tự | ✅ C-a 13/10 (ERP `e42f297894`, merge + PUSH nhánh chung `3432ca97ac` 13/10) ~~⬜~~ | |
| N63 | 2 Job giá không dispatch (code chết) | ✅ C-a 13/10 (ERP `164fb432ff`, merge + PUSH nhánh chung `3432ca97ac` 13/10) ~~⬜~~ | |
| N64 | HRM `catalog-histories/{table}/{id}` không gate | ✅ phần hàng hoá/giá (soát 13/10); phần chứng từ tài chính ⇒ Q-N64 ~~⬜~~ | |
| N65 | 13.662 giá hiệu lực quá ngày + cờ mồ côi | ⬜ | |
| N66 | 3 bảng chứng từ không `company_id` gần rỗng | ✅ G3 `DocumentCompany` phủ (soát 13/10) ~~⬜~~ | |
| N67 | 2 nơi ghi cờ duyệt giá công ty | ✅ C-a 13/10 (ERP `51918163e3`, merge + PUSH nhánh chung `3432ca97ac` 13/10) ~~⬜~~ | |
| N68 | `firstOrFail` chỗ gọi chưa bắt exception | ✅ C-a 13/10 (ERP `27204dab75`, merge + PUSH nhánh chung `3432ca97ac` 13/10) ~~⬜~~ | |
| N76 | 8 danh mục Phase 1 còn lại + bản `pi-*` vẫn ghi được ở ERP ⇒ user 13/10: chặn hết ở ERP, HRM duy nhất (đảo QĐ8 Phase 1) | ✅ C-b 13/10 (ERP `42bbe92ae2`, ĐÃ PUSH) ~~⬜~~ | `ngoai-luong/soat-bang-c.md` |
| N77 🔴 | trang sửa/xem/sao chép chứng từ ERP nhúng `units` đủ 13 cột pcu (giá vốn…) vào JSON trang — **XÁC NHẬN 13/10** (YC đặt hàng tổng #7692 `cost_price` 240.000 trong `@json($object)`); ~25 hàm; sửa tập trung `unitsInfoFor` | ✅ C-a2 13/10 (ERP `8b23629e97` + `60719788f8` `$hidden` ProductUnit; merge + PUSH `3f017e66dd` 13/10) | `ngoai-luong/n77-khao-sat.md` |
| N77-b | màn Chi tiết hàng hoá ERP (`productShow`, quyền Xem hàng hóa) hiện ô Giá vốn + Giá mua | ✅ C-a2 13/10 ẩn 2 ô (`8b23629e97`); đo bố cục sau khi sửa N51 | n77-khao-sat |
| N80 | trang xem YC xuất hàng nhúng tổng giá vốn HỢP ĐỒNG (`cost_price` khối hiệu quả HĐ) | ⏸ user 13/10: ghi riêng STATUS gop-db, làm sau (ngoài hàng hoá) | n77-khao-sat |
| N78 | thẻ "Hàng reset giá" ghi ở cả ERP Quy chế lẫn HRM tab Hàng hóa — cùng loại N67 | ✅ C-b 13/10 (ERP `42bbe92ae2`, ĐÃ PUSH) ~~⬜ user 13/10: HRM duy nhất — đợt C-b~~ | `ngoai-luong/cb-khao-sat.md` |
| N79 | `WrServiceQuotation.php:1072,1308` `$service` chưa khai báo (lỗi cũ, cảnh báo) | ⬜ lỗi cũ | ca-plan §6 |
| N81 | Route ghi `pi-groups` / `pi-brands` / `pi-manufactures` ở ERP còn mở (menu đã ẩn; ghi bảng pi_*, phục vụ form Hàng hoá có sẵn đã chặn) | ✅ 13/10 user "chặn luôn": 21 route (pi-groups đích `stopped-generic`), ERP `42bbe92ae2` ĐÃ PUSH | `ngoai-luong/cb-plan.md` |
| N69–N70 | Cty 5/6/8 loại bỏ | ⬜ → B2 | |
| N71 | Comparator lệch cặp HRM | ✅ G2b | |
| N72 | Backfill 4 ô quản trị NULL | ✅ G2b | |
| N73 | Seeder test nối giá không kẹp công ty | ⬜ | |
| N74 | 4 helper Human đọc `mysql2` (erp2326) | ⬜ (cờ đã gỡ ở G2b — cần kiểm còn đường đọc này không) | |
| N75 | `e2e_provision.php` mã hàng id erp2326 | ⬜ | |

**Đếm (bảng C, 63 dòng):** ✅ 20 · ⬜ 38 (khoảng 15 là lỗi cũ ERP có sẵn trên gop_db) · ⏸ 4 · ❌ 1.
✅ **User chốt 12/10: SỬA HẾT trước khi update prod** — kể cả lỗi cũ ERP có sẵn trên gop_db (N41, N45–N51, N59–N63, N65…).

## 📝 Chốt nghiệp vụ 16/10/2026 (tối)
| # | Chốt |
|---|---|
| N194 | ✖ Đóng — đúng quy ước (giá dự kiến 1 đ ngày 31/12 hằng năm) |
| N169(a) | **Chặn duyệt hàng đang khoá**: yêu cầu vẫn hiện, gắn nhãn "Hàng đang khoá"; Duyệt (lẻ + hàng loạt) ⇒ báo lỗi, chỉ được Không duyệt; mở khoá thì duyệt lại được, không mất đề xuất |
| N169(b) | **Hiện nhưng cảnh báo**: ĐVT chưa có giá vẫn chọn được; popup ghi "Chưa có giá"; cảnh báo giá 0 sẵn có của báo giá báo khi lưu |
| N169(c) | **Khoá trường định danh khi đang tính giá** (status 2 Chờ tính giá bán · 5 Đang tính giá): khoá Hãng SX, Thương hiệu, Model, Code đặt hàng, Xuất xứ, ĐVT ở FE + BE; mô tả/ảnh/tài liệu/quản trị vẫn sửa; muốn đổi phải huỷ yêu cầu trước |
| N172 | **Từ chối ⇒ trả ô về giá hiện hành**: Không duyệt xoá giá chờ duyệt; ô "Giá mới" hiện giá đang áp + dòng "Đề xuất X bị từ chối: <lý do>"; đề xuất lại phải gõ lại (khác ERP) |
| N175 | ✖ **Giữ như ERP** (màn Duyệt sửa Bán lẻ không tính lại TMĐT / không lan 4 loại giá) — đóng |
| N186 | **Bỏ nút Lưu nháp với YCTG Không duyệt (5)**: chỉ còn Gửi lại; BE cũng chặn lưu nháp phiếu status 5 (giữ T4-Q3) |
| N193 | ✖ **Giữ tròn đồng như ERP** — đóng. (N176 vẫn là lỗi code: màn Duyệt hệ số→giá tròn trăm, cần thống nhất) |
| N199 | ✖ **Giữ** — quyền PTG 1663/1664 bao gồm xem Giá nhập kho; ghi rõ trong SRS PTG — đóng |
| N200 | **Ghép "PTG-x: <lý do gõ>"**; ô trống thì "Phiếu tính giá PTG-x" |

## 📌 17/10/2026 — đợt lỗi SRS 16/10 ĐÃ MERGE LOCAL nhánh chung (chưa push): api `6acb9dbcd`, client `cc5763107`, ERP `8d677d7906`. Chi tiết `ngoai-luong/loi-srs-1610-plan.md` (Kết quả Lượt 1–3). Trước deploy: gán quyền "Xem phiếu yêu cầu đặt hàng trong nước theo tổng công ty" (N160). Còn mở: N203, N204, N155, N164, N165, N192.

### Chốt 17/10/2026
| # | Chốt |
|---|---|
| N185 | Giữ phần mở rộng (5 ô lọc YCHG theo phiếu thấy được) |
| N187 | Đã bổ sung `Không duyệt` · `Chờ tính giá` vào skill notification-convention (16 giá trị) |
| N179 | Nới cột Hệ số lên ~125px (2 màn giá) — đợt kế |
| N172 | Giữ dòng "Đề xuất … bị từ chối" ở ô Tên |
| N204 | Để riêng NGOÀI feature — không sửa trên nhánh Chuyển đổi hàng hoá |
| N203 | Làm bằng helper chung cho các màn chứng từ BÁN chọn ĐVT (kiểm kê màn trước) |

| N205 | ✅ 17/10 Giữ hàng (api `784814717` · client `de26eb522`); Mượn hàng chỉ có màn Tạo ⇒ không cần sửa — xem "Kết quả N205" trong `ngoai-luong/loi-srs-1610-plan.md`. (17/10, phát sinh khi làm N203) Giá ĐVT ở **Mượn hàng** (`BorrowExportRequestService::unitsOfProducts`) và **Giữ hàng** (`ProductPrepickRequestController`) vẫn lấy theo công ty NGƯỜI ĐĂNG NHẬP, không theo công ty chứng từ (cùng loại N137). Báo giá + BOM đã sửa trong N203 (gửi `quotation_id` / `bom_list_id`) |
| N206 | (17/10, e2e) Ca N2 `product-price-approvals-ui` đổi `company_role=2` — cùng giả định dữ liệu quyền như P7; P7 sẽ skip trên DB hiện tại vì role chỉ gắn công ty 1 (spec tự gắn tạm vai trò cho công ty khác cần user cho phép ghi DB) |
| N207 | ✅ 17/10 nhánh `feat/cdhh-n207-gia-giu-hang` (api `cf4b83e67` · client `01ef566f7`, chưa merge nhánh chung, chưa push) — BE tự tra giá + nhãn khi lưu (HĐ: dòng HĐ; 99: giá lẻ công ty phiếu; không giá ⇒ 0); màn Sửa loại 99 hiện giá hiện hành. Xem "Kết quả N207" trong `ngoai-luong/loi-srs-1610-plan.md`. (17/10, phát sinh N205, hỏi nghiệp vụ) **Giữ hàng tin giá client khi lưu**: `ProductPrepickRequestService::normalizeLines` lấy `price`/`total_amount` từ payload mọi loại phiếu (YCXH/Mượn hàng thì BE tự tính lại). Sửa = lưu lại nháp cũ sẽ chốt theo bảng giá hiện hành; loại gắn HĐ cần chốt nguồn giá |
| N208 | (17/10, hệ thống) Công ty phiếu MỚI lệch 2 nguồn: giá đọc `company_role ?: company_id` (công ty đang làm), `store()` Mượn hàng/Giữ hàng/YCXH ghi `company_id = employee_infos.company_id` (công ty gốc) — 3/1119 NV local lệch; Mượn hàng tính lại lúc lưu ⇒ giá màn ≠ giá lưu |
| N210 | ✅ 17/10 ERP nhánh `feat/2d1-gia-cu-chon-lai` commit `f8c8f3e60a` (chưa merge nhánh chung, chưa push). **Lỗi:** BG HĐ nguyên tắc — chọn hàng (chưa lưu), đổi giá nơi khác, xoá dòng, mở popup (thấy giá mới), chọn lại ⇒ dòng vẫn giá CŨ. **Nguyên nhân:** `$scope.addProduct` tìm trong `$scope.products` (cache phản hồi `/admin/products/{id}/getData` theo trang) và dùng lại, không gọi lại máy chủ. **Sửa:** bỏ nhánh dùng cache, mỗi lần chọn đều gọi getData (giữ tham số cũ), cache thay bản ghi thay vì push trùng — 11 chỗ/10 file: sale/firm/quotations (2: phẳng + chọn SP con), firm/orders, firm/ztect_orders, project_quotations, service_quotations (cả `quotation_products`), liquidation_quotations, liquidation_contracts, sale_orders, quotations, partials/contracts/js/createEditJs. 3 chỗ grep khớp nhưng KHÔNG phải cache (manufacture_expect_prices, quotation_templates, classes/sale/Service — chặn chọn trùng) ⇒ giữ. **Kiểm:** Playwright (e2e_assign không có quyền Thêm báo giá ⇒ render view thật qua tinker rồi route.fulfill, API thật, chặn POST/PUT, giá giả bằng route.fulfill lần getData thứ 2): BG HĐNT trước sửa lần chọn 2 = 0 request, dòng 100,000 (cũ); sau sửa = 1 request, dòng 200,000 (mới), cache 1 bản. BG thúc đẩy bán: lần 2 = 1 request, giữ `query_stock/check_promo/warehouse_group_id`. ĐH bán hàng `addPromotion`: 1 request/lần. PHPUnit 207 OK (4 skip). **Tồn:** `sale_orders.addPromotion` là code chết sẵn (`form.addPromotion is not a function`, không nút nào gọi) — không sửa. |
| N211 | ✅ 20/10 hrm-api nhánh chung `fcdf728e8` (đã push). **Lỗi** (đến từ merge gop_db 19/10): `PriceReaderWhitelistTest` ĐỎ — `ProductExportRequestService::getWrServiceContractDataForExport` (commit gop_db `9ab7f5184`, YCXH loại 17 Xuất bán SC-BĐ) đọc `product_unit_prices.sale_max_percent` (loại 1) bằng `first()` KHÔNG kẹp công ty ⇒ sau M3 lấy ĐMGG của công ty bất kỳ. **Sửa:** đọc qua `ProductPriceReader::pricesByUnit` theo `CompanyHelper::pricingCompanyId($contract)` (công ty HĐ SC-BH, lùi công ty người dùng — khớp ERP `DocumentCompany::ofOrUser`); thiếu dòng giá của công ty ⇒ vẫn ném như ERP firstOrFail. **Kiểm:** PHPUnit `PriceReadPointsTest::a12` (HĐ B 5% · HĐ C 10% · chủ A không bộ giá ⇒ ném) — ĐỎ trên code cũ (5 ≠ 10), xanh sau sửa; Whitelist 2/2 · PriceReadPoints 10/10 · 2 bộ YCXH xanh; API thật HĐ 7725/7712 trả 200, ĐMGG khớp bộ giá công ty 1. |

### Chốt 17/10/2026 (tiếp)
| # | Chốt |
|---|---|
| N207 | **Máy chủ tự tra giá khi lưu Giữ hàng** theo công ty phiếu, bỏ giá client; loại gắn HĐ lấy giá dòng HĐ (khảo sát trước khi code) |
| N208 | ~~Phiếu mới thuộc công ty ĐANG LÀM~~ ⇒ sau khảo sát (quyền duyệt/thông báo/kiểm tồn/letterhead của YCXH·Mượn·Giữ hàng đều theo công ty GỐC qua trait `ChecksEmployeePermission`; BaseModel gán company gốc cho 282 bảng) user chốt **ĐỂ RIÊNG NGOÀI FEATURE** |
| N209 | ✅ 20/10 BE `detailData` trả giá dòng HĐ cho phiếu Đang tạo + khoá `lineKey` (chưa commit). (17/10, phát sinh N207, nhẹ) Màn Sửa Giữ hàng loại 1–5 vẫn hiện giá đã lưu, không nạp lại giá dòng HĐ — chỉ lệch với nháp cũ từng lưu giá client khác HĐ (lưu lại thì máy chủ chốt đúng giá HĐ) |

## 📌 17/10/2026 — đã merge nhánh chung + ĐÃ PUSH: api `dbd9ebbb2` (+17), client `862ea0ef6` (+25), ERP `8d677d7906` (+2); kiểm không nằm trong gop_db. Gồm đợt lỗi SRS (3 lượt) · N203/N179 · N205 · N207.

## ⏰ NHẮC LÀM SAU go-live 20/10 — phần CODE bỏ Nhóm hàng hoá (user chốt 20/10: để đợt code sau)
Dữ liệu B2–B6 đã có gói `catalog-import/golive-2010/`. Còn CODE (chưa viết, mỗi mục xin "làm" riêng):
1. **Nhóm máy → Loại** (1.592 liên kết nhóm 1–1): chuyển dữ liệu + ERP picker phụ tùng lọc Loại OR Nhóm (6 chỗ `Common/SearchController`: 694, 911, 1132, 1353, 1575, 1964) + HRM form hàng ô "Dùng cho Loại máy" cạnh `machine_group_ids`. KHÔNG chuyển dữ liệu trước khi có code (picker ERP mất phụ tùng).
2. ERP báo cáo Tồn lâu đọc `product_types.long_stock_days` theo Loại của hàng, thiếu ⇒ 180 (`Product.php:6798/6830`, `ProductInfo.php:3466/3499`, `ProductTemplate.php:6357`).
3. ERP ~30 báo cáo INNER JOIN `groups` → LEFT JOIN (kiểm kê `catalog-import/phu-luc-kiem-ke-nhom-hang.md`).
4. ERP bỏ dự phòng VAT nhóm (`Common/SearchController.php:856,1703,2065`) — sau khi B4 đã chép VAT.
5. Đợt sau nữa: cấu hình theo nhóm (B), cột chụp nhóm trên chứng từ (Q4), catalog (E), xoá bảng/cột/màn + 3 thuộc tính Q3 (đo prod), lọc báo cáo theo cây (Q5); nghiệp vụ gán Loại dần cho ~16.552 hàng + thuộc tính/Nhóm máy của nhóm nhiều Loại.

## 20/10/2026 — ĐÃ LÊN PRODUCTION (đêm 20/10, ~21:30–23:40) — theo dõi sau go-live
- Chạy trọn `HUONG-DAN-VPS-PROD-2010.md`, mọi điểm dừng đạt, số khớp bản chạy tập `hrm_erp_20_10`. Sao lưu: VPS HRM `~/backup_hrm_erp_gop_2026-10-20_2157.sql.gz`.
- **Cron áp giá HRM lần đầu 21/10 01:00** — user chốt (phương án 1) để áp cả 8 dòng 1 đ ngày 21/10 của 2 mã Sài Gòn `SG-MN-SG-DCT-20K` (Đe thuyền 20kg, 2.800.000) ·
  `SG-MN-SG-VSBD` (Máy vệ sinh buồng đốt, 14.000.000) — 2 dòng gốc Cty 4 (pep 100159/100160, NV 433 lên lịch 21/09) + 6 dòng backfill chép sang Cty 1·2·3 (pep 107329–107334).
  Sáng 21/10: kiểm Nhật ký áp giá có 8 dòng này; nghiệp vụ xác nhận đúng ý.
- **Tra sau (không gấp):** cron ERP cũ `product:update_price` báo email 30/06 "không có thay đổi giá" dù DB gộp có 839 dòng `status 2`, `effect_date 2026-06-30`, flag NULL/0, tạo + sửa trước 30/06
  (sao lưu cleanup xác nhận) ⇒ nghi cron đêm đó đọc DB khác (ERP prod trước gộp DB 09/10) hoặc email từ môi trường khác (VPS test). Cron cũ CÓ áp giá 1 đ (không lọc) — giá 1 đ treo không phải vì 1 đ.
  2.105 dòng 2026 quá hạn đã đóng bằng `price:cleanup-stale` (sao lưu ERP `storage/app/price-cleanup/20261020-225503`); 22 giá thật cần nghiệp vụ soát: `golive-2010/gia-qua-han-2026-can-soat.xlsx`.
- ERP thôi gửi email kết quả cron giá (gỡ lịch + PRICE_EMAIL_*) — kết quả xem HRM › Nhật ký áp giá. Nếu nghiệp vụ cần email ⇒ làm thêm phía HRM.
- **N214 (21/10) ✅ ĐÃ SỬA phương án 1+2 — hrm-api `bde261902`, ĐÃ PUSH feat + gop_db 21/10 (chưa pull lên prod): `expectedFailed()` báo `[GIA] Lỗi` + `emailOutputOnFailure(ADMIN_EMAIL)`; test `cron_loi_mot_cong_ty_…` (ExpectedPriceApplyTest 4/4, đã kiểm ngược). Lên prod: merge gop_db → pull /var/www/tpe/hrm-api (không migration). Còn hở: scheduler chết hẳn thì vẫn im lặng (phương án 3 chưa làm). Mô tả gốc:** cron `product-price:apply-expected` LỖI thì không ai biết. Đã báo: áp được (`Cập nhật`), bị chốt chặn (`Quá hạn`). CHƯA báo: (1) lỗi 1 công ty — `catch` chỉ `report()` vào laravel.log + in bảng ra console (không ai đọc), giao dịch rollback ⇒ giá vẫn chờ, đêm sau thử lại, quá 30 ngày mới thành `Quá hạn`; (2) cron không chạy / chết trước vòng lặp (scheduler dừng, lỗi DB, mutex `withoutOverlapping` kẹt) ⇒ im lặng giống đêm không có giá. Đề xuất: thông báo `[GIA] Lỗi` cho người có "Cập nhật giá bán hàng hoá" của công ty + `emailOutputOnFailure(ADMIN_EMAIL)` (khuôn `finance:update-exchange-rate`, Kernel.php:127); tuỳ chọn thêm email tóm tắt mỗi đêm để biết cron còn sống.
- Việc còn: gán 30 quyền mới (xe 2c cho 8 người, PTKD "Xây dựng thông tin hàng hoá"…) ⇒ `php artisan cache:clear` (HRM tpe cache file); nhập Đặc tính sản phẩm; phân công XNK Cty 2/5/6/7/8;
  gửi `ds-gui-nghiep-vu-prod-2010.xlsx`; DROP bảng `zz_golive2010_*` sau nghiệm thu; `rm ~/.golive.cnf` nếu đã tạo; phần CODE bỏ Nhóm hàng (mục "⏰ NHẮC LÀM SAU").
- **Rà menu 21/10** (`catalog-import/golive-2010/tong-hop-menu-dot-golive-2010.xlsx` — HRM 63 menu · ERP 73 menu/màn, 271 route chặn ghi). Lệch còn mở (chỉ ghi nhận):
  (a) ERP Kế toán › Quản lý giá - CTKM › Giá bán › Nhật ký cập nhật giá còn link ERP (qua trang trung gian) · (b) ERP Danh mục chương / nhóm công việc / cụm công việc
  KHÔNG chặn ghi ⇒ 2 bên cùng ghi · (c) HRM Bán hàng › Danh mục › Danh mục chung › Danh mục hàng hóa còn mở `/admin/products` ERP · (d) HRM "YC duyệt hàng tạm" là mục xám ·
  (e) runbook bước 12 ghi "bỏ 3 thẻ", code bỏ 4 (thêm "Hàng tạm cần duyệt") · (f) SelfInventory/SelfInventoryRequest cho Super admin xem toàn tổng công ty KHÔNG cần quyền — trái quy tắc
  "Super admin không mặc định có quyền" (feature kho của đồng đội, báo lại) · (g) `bang-man-hinh-menu.md` (12/10) đã cũ — dùng file Excel 21/10.
- **21/10 — popup chọn hàng ERP đồng bộ HRM + chữ đè cây catalog ✅ ĐÃ MERGE gop_db + PUSH** (chưa pull lên prod): ERP `8318ac7185` → gop_db `b9081f5c61`
  (`partials/modals/productPicker.blade.php`: vạch dọc phân cấp, số Tiểu mục xanh đậm, mũi tên cuối dòng, bỏ dòng "Công ty … · Bảng giá …" mọi màn;
  Lĩnh vực đang chọn dính đầu nền đặc) · hrm-client `8f2f5dc28` → gop_db `e45688424` (`ProductCatalogTree.vue` cùng lỗi nền trong suốt).
  E2E: +1 ca `product-picker-filters-ui.spec.ts` (chưa chạy bộ). Còn: `pp.scopeTip` (`js/productPickerJs.blade.php`) không còn chỗ gọi.
