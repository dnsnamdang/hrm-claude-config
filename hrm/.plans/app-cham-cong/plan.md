# Thiết kế lại màn Chấm công trên app (TPE_APP) — @cuong61n

Người phụ trách: @cuong61n · Nhánh: app `tpe` · hrm-api `develop`
Màn: nút giữa "Chấm công" phân hệ Chấm công → `ui/check_in_out/` + `ui/check_in_out_success/`
API: `GET v1/timekeeper/listTimesheetTypes?only_app=true` · `POST v1/timekeeper/checkTimesheet` · `POST v1/timekeeper`

## Phase 1 — Đọc logic + thiết kế (pen.dev)

- [x] 06/11/2026 Đọc logic app + BE. BE (`TimekeeperController`, `TimesheetService::listTimesheetTypesOf`): danh sách hôm nay gồm tối đa 1 ca (`workshift`) + phiếu giao việc (`jobassignment`, chỉ phiếu có toạ độ) + phiếu công tác (`business_trip`, ERP) + phiếu công tác kỹ thuật / khác (`new_business_trip`) + làm thêm (`overtime`, chỉ có nơi + cho app). `store` KHÔNG phân biệt vào / ra (mỗi lần = 1 lượt), ảnh + ghi chú không bắt buộc, `is_finish` (Kết thúc công việc) bị bỏ qua; phiếu công tác kỹ thuật bắt buộc `job_assign_id` (thiếu → "Chấm công thất bại"); vị trí sai → 422 "Vị trí chấm công không hợp lệ"; API chưa trả toạ độ nơi được chấm. App hiện: bảng chọn ca kiểu cũ, chưa chọn thì không lấy vị trí, không có ca → toast rồi tự đóng màn
- [x] 06/11/2026 Yêu cầu user: chỉ có 1 ca / 1 phiếu hôm nay → tự chọn luôn, không bắt bấm chọn (áp cả phiếu giao việc của phiếu kỹ thuật)
- [x] 06/11/2026 Vẽ board "CC · Chấm công — thiết kế lại" trong `meeting-mobile_v2.pen`: CC-01 1 ca tự chọn · CC-02 nhiều ca / phiếu chọn ngay trên màn · CC-03 phiếu kỹ thuật + chọn phiếu giao việc · CC-04 vị trí không hợp lệ (lỗi dưới khối Vị trí) · CC-05 hôm nay không có ca (ở lại màn, nêu lý do BE) · CC-06 thành công
- [x] 06/11/2026 User chốt: nhiều ca / phiếu → gợi ý sẵn mục đang trong giờ · KHÔNG nhãn Vào / Ra · sửa BE trả toạ độ nơi chấm để hiện khoảng cách · bỏ chip "Duy nhất hôm nay" · trong phạm vi chỉ ghi "Trong phạm vi chấm công" (không số), ngoài phạm vi ghi khoảng cách + mức cho phép (bỏ câu "vẫn bấm được…") · bỏ dòng "Đã chấm hôm nay" → link Xem lịch sử chấm công · màn không có ca chỉ link Lịch sử (bỏ Đề nghị tra soát). Bản vẽ CC đã đồng bộ

## Phase 2 — Code

### BE (hrm-api, develop — chưa commit)
- [x] 06/11/2026 `TimesheetService::listTimesheetTypesOf(..., $withCheckPlaces)`: mỗi ca / phiếu kèm `check_places` [{place, lat, lng, max_distance (m)}] lấy từ `placeToCheckInOut` (CÙNG nguồn với `checkCheckin` lúc chấm) — phiếu công tác kỹ thuật trả theo từng `job_assign[].check_places`; [] = không giới hạn; lỗi dữ liệu → null. Tách `maxCheckinDistance()` (cache GeneralRegulation theo công ty) dùng chung cho `checkCheckin`. Controller bật khi `only_app` (màn đề nghị tra soát không tốn thêm query). Kiểm tinker: ca 1.1.VP_PTT → 189 Phan Trọng Tuệ, 200 m

### App (TPE_APP, tpe — chưa commit)
- [x] 06/11/2026 Model `CheckPlaceData` + `check_places` ở `TimesheetTypeData` / `ApiJobAssignData`
- [x] 06/11/2026 Viết lại bloc: checkTimesheet lỗi → ở lại màn nêu lý do (trước toast + tự đóng); tự chọn khi chỉ 1 ca / phiếu, nhiều thì gợi ý mục đang trong giờ; phiếu kỹ thuật 1 phiếu giao việc tự chọn; lấy vị trí ngay khi có mục chọn, nút Lấy lại; lỗi 422 vị trí hiện dưới khối Vị trí; bỏ is_finish / ngày giờ / chọn ca bằng bảng cũ
- [x] 06/11/2026 Màn mới theo CC-01…05: đồng hồ chạy, thẻ ca (loại · tên · giờ · trạng thái giờ · nơi chấm), nhiều mục chọn ngay trên màn, phiếu giao việc dòng phẳng `AppPickTile`, khối Vị trí (khoảng cách Haversine giống BE), ảnh (không bắt buộc, tối đa 3), ghi chú; chưa đủ điều kiện → ẩn nút + lý do trên thanh đáy (app-ui-convention 1d). Màn thành công CC-06 viết lại
- [x] 06/11/2026 `make gen` + analyze: 0 lỗi / 0 cảnh báo / 171 info

### Đã test simulator iOS (tpeLocal, TK namdangit, dữ liệu thử ca hôm nay — đã xoá)
- 1 ca → tự chọn, lấy vị trí, "Trong phạm vi chấm công" → Chấm công → DB `timesheets` đúng job_type workshift / job_id 1 / place → màn thành công → Về tổng quan
- GPS Hoàn Kiếm → "Ngoài phạm vi chấm công · cách … 9.2 km · cho phép trong 200 m" → bấm → BE 422 hiện đúng khối Vị trí + toast → đổi GPS + Lấy lại → hết lỗi
- Link Xem lịch sử chấm công mở đúng màn · không có ca → CC-05 ở lại màn + Quay lại
- CHƯA thử: nhiều ca / phiếu (CC-02, gợi ý mục đang trong giờ), phiếu công tác kỹ thuật + phiếu giao việc (CC-03), chụp ảnh, Android, cổng có Goong (tên địa điểm)

### Phase 3 — Test kỹ (iOS + Android) + sửa lỗi phát hiện — 06/11/2026
- [x] Dữ liệu thử (DB local, đã trả lại): ca hôm nay + PCT-TEST-KT (kỹ thuật, 2 phiếu giao việc) + PCT-TEST-KC (khác) dời sang 06–07/11 + gán namdangit (`assign_request_employees.employee_id` = employees.id 13) + phiếu làm thêm chép từ 5532 (18:00–21:00)
- [x] iOS: 4 mục → gợi ý sẵn ca đang trong giờ · chọn phiếu kỹ thuật → bắt chọn phiếu giao việc (nút ẩn + lý do) · ngoài phạm vi 20.2 km → bấm → BE 422 khớp app · GPS tới Thạch Thất + Lấy lại → trong phạm vi → chấm OK (DB job_id 13328, job_assign_id 17929) · KC lượt đầu đúng nơi OK, lượt sau "không giới hạn nơi chấm" (đúng quy tắc ngày đầu BE) · ghi chú lưu DB + hiện màn thành công · ‹ ở màn thành công về Tổng quan · làm thêm chưa tới giờ hiện "Còn 5g38p"
- [x] Android (Pixel 4 API 29, adb reverse 8000): từ chối quyền vị trí → câu lỗi tiếng Việt trong khối Vị trí · Lấy lại → cho phép → trong phạm vi · chụp ảnh camera giả lập → ảnh + ✕ → chấm kèm ảnh, DB lưu `images` + `device_id` → màn thành công có ảnh
- [x] Sửa: viên trạng thái dưới đồng hồ báo "Trong / Ngoài phạm vi chấm công" (nhiều mục thì khối Vị trí bị đẩy xuống, trước chỉ báo "Đã lấy vị trí")
- [x] Sửa: nút "Chấm" từng dòng ở Tổng quan → mở màn chọn sẵn đúng ca / phiếu đó (`CheckInOutRoute(preferType, preferId)`; trước luôn gợi ý ca đang trong giờ)
- [x] Sửa: ca / phiếu không giới hạn vị trí → dòng xanh "Ca / phiếu này không giới hạn nơi chấm công"
- [x] Sửa: phần chọn phiếu giao việc mất viền 2 bên (nền dòng đè viền) → làm lại cùng kiểu ô chọn ca / phiếu (ô bo góc + nút tròn ✓, mã đậm / khách hàng / địa điểm)
- [x] Sửa: từ chối quyền vị trí hiện toast "rootError: Location permissions are denied" → câu tiếng Việt theo nguyên nhân (GPS tắt / chưa cho phép / từ chối hẳn) trong khối Vị trí
- [x] User chốt thêm: ngoài phạm vi chỉ ghi khoảng cách (bỏ "cho phép trong …"); đồng hồ HH:mm (thử HH:mm:ss, user bỏ), cập nhật mỗi giây
- [x] Analyze 0 lỗi / 0 cảnh báo / 171 info; log 2 máy không có lỗi Flutter mới (chỉ còn lỗi cuộn menu trái có từ trước)
- Ghi chú: 2 lần "nhảy về màn Chấm công cũ" khi bấm Chụp ảnh chỉ xảy ra ngay sau hot reload / hot restart giữa chừng; mở sạch thì không tái hiện (iOS simulator không có camera → hộp "Camera not available" của hệ thống) → kiểm lại trên bản build thật
- CHƯA thử: iPhone thật (camera thật), cổng dev / prod, tài khoản không có mã chấm công / thiết bị chưa đăng ký

### Checkpoint — 06/11/2026 12:32
Vừa hoàn thành: test kỹ iOS + Android đủ loại ca / phiếu, sửa 5 lỗi phát hiện
Đang làm dở: —
Bước tiếp theo: user xem; thử iPhone thật; user cho commit (hrm-api + TPE_APP)
Blocked:

## Phase 4 — Màn Lịch sử chấm công thiết kế lại — 06/11/2026 — @cuong61n
- [x] 06/11/2026 Vẽ board "LS · Lịch sử chấm công — thiết kế lại" (`meeting-mobile_v2.pen`): LS-01 gom theo ngày (giờ to · ca / phiếu + mã · nguồn App / Máy chấm công · nơi chấm · ảnh thu nhỏ · ghi chú · 🗑 khi canDelete) · LS-02 xem ảnh toàn màn vuốt qua lại · LS-03 lọc ra rỗng. User duyệt
- [x] 06/11/2026 User duyệt sửa BE 4 mục (phát hiện khi đọc dữ liệu): ảnh nhiều tấm hỏng (lưu nối `|`, API tách `,`) · lượt Làm thêm hiện "Ca hành chính" · API không trả ghi chú · API trả cả lịch sử 1 lần (có NV 7,754 lượt) + N+1 query phiếu
### BE (hrm-api)
- [x] 06/11/2026 `TimekeeperEmployeeResource`: thêm `image_urls` (mảng URL đầy đủ, tách cả `|` lẫn `,`; `images` giữ chuỗi thô vì web tự tách `|`), `image` lấy đúng ảnh đầu, thêm `note`, job_type `overtime` → "Làm thêm" (trước rơi về "Ca hành chính"), nạp trước conn_info / phiếu công tác / phiếu giao việc (hết N+1). Kiểm tinker: lượt 2 ảnh ra 2 URL, phiếu kỹ thuật đúng mã PCT + PGV, làm thêm đúng nhãn
- [x] 06/11/2026 `TimekeeperController::employeeIndex`: có `page` → paginate(`limit`, mặc định 30, trần 100) + `total` / `currentPage` / `lastPage`; không có `page` → trả cả danh sách như cũ (app bản cũ). Web màn Lịch sử chấm công (gửi page + limit) nay nhận đúng `total`. Kiểm curl: 22 lượt → 5 trang × 5, lọc máy chấm công 3
### App (TPE_APP)
- [x] 06/11/2026 Model `image_urls` + entity `note`, mapper (fallback `image` cho BE cũ); repository / use case trả `PagedList<CheckIn>` theo trang; bloc `LoadMore` (cuộn còn ~600px), state page / isLastPage / loadingMore / total
- [x] 06/11/2026 Màn viết lại theo LS-01 / LS-03: gom theo ngày (Hôm nay / Hôm qua / Thứ, dd/MM, năm khác ghi năm), mỗi lượt giờ HH:mm · ca / phiếu + chip App / Máy chấm công · mã phiếu · nơi chấm (máy không có tên → "Máy chấm công") · ảnh thu nhỏ 48 · ghi chú · 🗑 khi canDelete (showAppConfirm, toast "Xóa thành công"); tiêu đề "Lịch sử điểm danh" → "Lịch sử chấm công"; dòng tổng dùng `total` BE; bộ đếm "Xem N lượt" hỏi page=1&limit=1 (trước tải cả lịch sử để đếm); đổi lọc / tìm → cuộn về đầu
- [x] 06/11/2026 Widget chung MỚI `custom_view/app_photo_viewer.dart` → `showAppPhotoViewer(urls, initialIndex, caption, subCaption)` (LS-02: toàn màn nền tối, vuốt qua lại, chụm phóng to, 1 / N, chấm trang, chú thích) — thay hộp thoại ảnh 300×300; ghi vào skill app-components
- [x] 06/11/2026 Test iOS: 5 lượt thử (2 ảnh + ghi chú, phiếu kỹ thuật, làm thêm, 2 lượt máy) hiện đúng; bấm ảnh 2 → mở 2/2, vuốt → 1/2, ✕ đóng; tạm cỡ trang 10 → cuộn nạp trang 2, 3 mỗi trang 1 lần rồi dừng (27 lượt); lọc App 22 / Máy 5 khớp tổng 27; Xóa lọc về đầu danh sách; xóa lượt 12:01 → hỏi xác nhận → DB mất dòng, còn 26. Sửa khi test: giờ xuống dòng "17:3/2" (cột 54 → 58, không xuống dòng), mục cuối bị nút giữa che (đệm đáy 48), đổi lọc giữ vị trí cuộn cũ làm khuất tiêu đề ngày
- [x] 06/11/2026 Test Android: danh sách + trình xem ảnh + nút Back hệ thống đóng trình xem
- [x] 06/11/2026 User hỏi "ảnh không hiển thị được à" → ảnh vẫn hiện, do ảnh thử tự vẽ (ô màu + khung) trông như ô giữ chỗ → thay bằng ảnh thật. Sửa thêm: ảnh thu nhỏ đang tải để trống trơn → ô xám giữ chỗ; giải mã ảnh ở cỡ ô (`cacheWidth` 144) cho nhẹ
- Dữ liệu thử còn để trên DB local cho user xem: timesheets 7401797–7401799, 7401801 (NV 11910245) + ảnh `hrm-api/public/uploads/test_ls/` — xoá khi user xem xong
- Analyze: 0 lỗi / 0 cảnh báo / 171 info

### Phase 5 — Đẩy code + deploy dev + build app dev — 06/11/2026 (user yêu cầu)
- [x] hrm-api `develop`: commit `5d4731e38` (chấm công check_places, lịch sử phân trang / ảnh / ghi chú, badge icon app + câu nhắc push nhạy cảm của phiên khác, eager load đơn nghỉ) → merge origin/develop (14 commit, không conflict) → smoke API local 200 → push `d13a547fb`
- [x] Server dev (`~/build_tpe.sh`, log `~/build_tpe_20261106_app.log`): BE pull `d13a547fb`, migrate "Nothing to migrate"; FE build đang chạy (xem kết quả bên dưới)
- [x] TPE_APP: commit `10653bb` trên `tpe` (toàn bộ thay đổi app hôm nay + icon thông báo Android tpeProd + màn đăng nhập về tông chung) → merge sang `develop` (không conflict) → bump tpeDev 2.2.6 (162) `af37972` → push `develop` + `tpe`
- [x] hrm-client `develop` (sót lúc đầu, user nhắc): 2 màn Đơn xin nghỉ / Duyệt đơn badge trạng thái `V2BaseBadge` màu BE `status_color` → commit + merge origin (15 commit) → push `522ddea6f`; xếp lượt `build_tpe.sh` thứ 2 chạy sau lượt đầu (log `~/build_tpe_20261106_app2.log`)
- [x] Build IPA tpeDev 2.2.6 (162) + upload TestFlight (Tân Phát ERP-HRM) — "No errors uploading archive"
- [x] User yêu cầu merge lên prod: `develop` → `gop_db` hrm-api (`fff12a936`) + hrm-client (`bf0986007`) trong worktree tạm `worktrees/merge-*-1106` (không conflict, 68 file BE, không thêm mysql2, php -l sạch); `develop` → `tpe` app (fast-forward)
- [x] Bump HRM TPE (tpeProd) 2.3.8 (103) iOS + Android (TestFlight đã có build 102 bản gia hạn) → push `tpe` `db976cc`, đồng bộ ngược `develop`
- [x] Server prod: lượt 1 (`~/build_tpe_20261106_1650.log`) dừng ở migrate vì `APP_ENV=production` (từ 04/11) bắt xác nhận → kiểm cột `assign_other_requests` (bigint có dấu, không FK) → chạy lại `yes yes | ~/build_tpe.sh` (`~/build_tpe_20261106_1655.log`): 2 migration OK, route:cache OK, seeder quyền, FE `bf0986007`. Web 200, API lịch sử 401 khi chưa đăng nhập (route có). ⚠️ Script prod giờ cần trả lời yes cho migrate / db:seed — chạy nền phải `yes yes |`
- [x] Server dev lượt 2 nhận hrm-client `522ddea6f`
- [x] HRM TPE 2.3.8 (103) iOS: IPA upload → gán nhóm external "Tân Phát" (public link) + ghi chú + gửi Beta App Review bằng ASC API key (script `asc.py` ở scratchpad) → WAITING_FOR_REVIEW 06/11 16:50
- [x] HRM TPE 2.3.8 (103) Android: AAB (ký SHA-1 65:1B…F8) → Play Console Phát hành công khai 100%, ghi chú `<vi>` → Lưu → Tổng quan xuất bản → Gửi 1 thay đổi xét duyệt (06/11 16:52, chế độ xuất bản có quản lý tắt → duyệt xong tự phát hành)
- [x] Cập nhật state gia hạn TestFlight: tpeProd.env 2.3.8 (103) `db976cc`, tpeDev.env 2.2.6 (162) `af37972`; dọn worktree tạm

- [x] 06/11/2026 User muốn Android tự động như iOS: bật Google Play Android Developer API (project `tanphat-soft`), tạo service account `play-publisher@tanphat-soft.iam.gserviceaccount.com` + khoá JSON `~/.play_api/play-publisher.json`. Chưa mời được vào Play Console (cuong61n không có quyền quản lý người dùng) → user chốt tạm thời Android vẫn phát hành qua Playwright

### Checkpoint — 06/11/2026 16:55
Vừa hoàn thành: đẩy code 3 repo, deploy dev + prod, app dev 162 TestFlight, HRM TPE 2.3.8 (103) gửi duyệt iOS external + CH Play
Đang làm dở: —
Bước tiếp theo: chờ Apple / Google duyệt; user cân nhắc tạm tắt số đỏ icon cho app cũ
Blocked: + upload TestFlight (Tân Phát ERP-HRM)

### Checkpoint — 06/11/2026 15:48
Vừa hoàn thành: màn Lịch sử chấm công theo LS-01..03 + BE 4 mục, test iOS + Android
Đang làm dở: —
Bước tiếp theo: user xem; xoá dữ liệu thử; user cho commit (hrm-api + TPE_APP)
Blocked:
