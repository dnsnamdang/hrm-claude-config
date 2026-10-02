# Plan — Danh sách Nhu cầu khách hàng (Redmine #11386)

Nhánh: `task_11386` (tách từ `tpe`) ở cả `hrm-api` và `hrm-client`.

## Phần 1 — Màn danh sách + phân quyền 5 cấp

### BE
- [x] 4 quyền mới id 1184-1187 (`Xem danh sách nhu cầu khách hàng theo tổng công ty / công ty / phòng ban / bộ phận`), đặt CUỐI seeder, id tăng dần
- [x] `CustomerDemandService` — query + phân quyền theo cấp của NGƯỜI CHỦ TRÌ meeting + bộ lọc + phân trang
- [x] `CustomerDemandController@index` + route `GET v1/assign/customer-demands`
- [x] `CustomerDemandListResource` — 13 cột theo spec

### FE
- [x] `pages/assign/customer-demands/index.vue` theo skill `list-page`
- [x] Menu: Meetings → "Nhu cầu khách hàng"

## Phần 2 — Hạn xử lý + cảnh báo trực quan ✅ XONG

> Làm trọn trong **Redmine #11377** (nhánh `task_11377`) vì đó mới là task sở hữu tham số N/M.
> Chi tiết + kết quả verify: `.plans/demand-expiry-config/`.
> Khách đã chốt mốc tính hạn 14/09: **nhu cầu ĐANG MỞ áp mốc mới, nhu cầu ĐÃ ĐÓNG để nguyên**.

- [x] Cột `demand_due_days` trên `internal_business_scopes` + ô nhập ở màn danh mục
- [x] Tham số M ngày cảnh báo vào `general_regulations`
- [x] Cột "Thời gian hết hạn nhu cầu" + highlight khi sắp hết hạn — dùng **CAM**, không dùng đỏ
      (đỏ trong hệ thống chỉ dành cho lỗi validate, CLAUDE.md)
- [x] Sửa cron `assign:close-expired-customer-demands` theo công thức mới + backfill mốc T
      (`meetings.completed_at`, backfill từ `end_date` cho cuộc họp đã Hoàn thành)

## Phần 3 — Đóng nhu cầu thủ công ✅ XONG

Mô tả mới của #11386 (khách sửa 15/09/2026) đã chốt: popup chỉ có **Textarea "Ghi chú chi tiết"
(bắt buộc nhập)**, KHÔNG chọn từ danh mục → bỏ hẳn hướng gắn danh mục, #11465 giữ nguyên trạng dừng.

- [x] ~~Danh mục "Lý do đóng nhu cầu"~~ — khách chốt nhập tay, không làm danh mục
- [x] Cột `closed_by` + `close_note` trên bảng nhu cầu
      (migration `2026_09_15_000001_add_manual_close_to_customer_demands`; `closed_by` rỗng = cron tự đóng)
- [x] Endpoint `POST assign/customer-demands/{id}/close` + popup ghi chú BẮT BUỘC
      (`base-confirm-modal` với `required-input` — prop thêm từ #11369, không dựng popup riêng)
- [x] Quyền 1191 `Đóng nhu cầu khách hàng` — người đang phụ trách tự đóng được mà không cần quyền này
- [x] Ghi 1 dòng `customer_demand_histories` action `close` → hiện ở popup Lịch sử
- [x] Ẩn nút [+ Tạo Dự án TKT] sau khi đóng (`can_create_project` đã gate theo trạng thái)

## Phần 4 — Bàn giao nhu cầu (đơn lẻ + hàng loạt)

- [x] Cột `owner_employee_id` trên bảng nhu cầu + backfill từ `meetings.host_employee_id`
- [x] Rà MỌI chỗ đang đọc "kinh doanh chủ trì" từ `host_employee_id` (Báo cáo CSKH tiềm năng) cho khớp
- [x] Bảng lịch sử nhu cầu (skill `entity-history`) + hành động "Lịch sử" ở cột Hành động
- [x] Endpoint bàn giao đơn lẻ + hàng loạt, kèm quyền thực hiện
- [x] Popup bàn giao dùng `PopupStaff` có sẵn
- [x] Thông báo cho người nhận (skill `notification-convention`)

## Verify

- [ ] Môi trường: FE :3005 → API :8002 → DB `hrm_prod_30_3_26` (đã chạy migration + `assign:seed-care-demo`, 47 nhu cầu mẫu)

## Checkpoint — 2026-09-14

Vừa hoàn thành: **PHẦN 1 XONG, ĐÃ VERIFY, ĐÃ COMMIT** — `hrm-api` 4bbdfa45e, `hrm-client` 183ceeca4.
- Admin (quyền tổng công ty) → 59 nhu cầu; nhân viên 24 (không quyền) → đúng 8 nhu cầu mình chủ trì
- 13 cột đủ dữ liệu, đúng thứ tự spec; phân trang 3 trang; badge màu do BE trả

Bẫy gặp phải (ghi lại để lần sau khỏi mất công):
- `V2BaseDataTable` lấy giá trị ô bằng `getNestedValue(item, column.key)` — prop `field` BỊ BỎ QUA.
  `key` của cột phải trùng tên trường dữ liệu, sai thì ô rỗng mà không lỗi nào báo.
- Skill `list-page` nhắc `V2BaseRowActions` + `columnCustomizationMixin` nhưng nhánh `tpe` CHƯA CÓ
  2 thứ đó — skill đang đi trước code.

Bước tiếp theo: Phần 3 (Đóng nhu cầu thủ công) — Phần 2 vẫn chờ khách chốt mốc tính hạn.
Blocked: Phần 2 — công thức tính hạn nhu cầu.

## Checkpoint — 2026-09-14 (Phần 4)

**PHẦN 4 XONG, đã verify trên trình duyệt.** `hrm-api` 4488a82b1 · `hrm-client` 5c9af4cc3.

- Bàn giao hàng loạt qua UI: 2 nhu cầu đổi chủ, 2 dòng lịch sử ghi đúng từ ai → sang ai + lý do
- Phân quyền: thiếu quyền + không phải người phụ trách → 403 đúng câu; nhu cầu sai trạng thái → 422
- Mốc thời gian giữ nguyên sau bàn giao (không reset bộ đếm hạn)
- Phạm vi xem dịch chuyển: lọc theo người nhận ra nhu cầu đó, lọc theo chủ trì gốc KHÔNG còn thấy
- Thông báo: `[NCKH] Cập nhật: <b>...</b>. Bàn giao từ X.` — 50 ký tự, url kèm ID

User chốt 14/09: prefix thông báo `[NCKH]`; **Báo cáo CSKH tiềm năng GIỮ người chủ trì gốc**,
không đổi theo bàn giao, để không làm đổi số liệu kỳ đã chốt.

2 bẫy gặp phải:
- `assign/meeting/getListEmployee` trả PHÂN TRANG (`data.data`) — đọc `res.data` ra object, select rỗng mà không lỗi.
- `text-muted` trong b-modal bị theme render thành ĐỎ — phải đặt màu xám tường minh.

Còn lại của #11386: **Phần 3 (đóng nhu cầu thủ công)** — chờ chốt lý do đóng nhập tay hay danh mục (#11465 đang tạm dừng).
Blocked: cách nhập lý do đóng.

## Phần 5 — Tab "Nhu cầu của khách hàng" ở Công việc của tôi (#11390) ✅ XONG

Cùng nhánh với #11386 / #11377 vì dùng chung nguyên màn danh sách.

- [x] Tách `components/assign/CustomerDemandList.vue` dùng chung — trang `/assign/customer-demands`
      và tab đều render component này, KHÔNG có bản copy thứ hai
- [x] Trang danh sách rút còn vỏ mỏng: chỉ giữ tiêu đề trang + `filterStateMixin`
      (mixin bám `beforeRouteLeave`, hook chỉ chạy ở component TRANG nên không chuyển xuống con được;
      component nhận `initial-state` lúc tạo và bắn `state-change` khi user đổi bộ lọc)
- [x] BE nhận `only_mine=1` — ép `COALESCE(owner_employee_id, host_employee_id) = mình`, bỏ qua
      5 cấp phân quyền (hẹp hơn mọi cấp quyền nên không cần kiểm quyền thêm)
- [x] `pages/assign/my-job/components/CustomerDemandsTab.vue` + đăng ký tab thứ 7 ở `my-job/index.vue`
      (`?tab=customer-demands` khôi phục đúng tab)

### Checkpoint — 2026-09-15 (rà mô tả mới + Phần 3)

Vừa hoàn thành:
- Đọc lại mô tả MỚI của #11386 và đối chiếu toàn bộ code đã làm. Phần 1/2/4 **không phải sửa nghiệp vụ**.
  3 điểm lệch đã chốt với user (giữ `Đóng`, giữ `Đã lập dự án TKT`, thông báo theo skill) — ghi ở
  `design.md` mục "Quyết định đã chốt — đối chiếu MÔ TẢ MỚI".
- Sửa 2 vi phạm quy tắc mới của CLAUDE.md: `toLocaleString('en-US')` ở màn danh sách, và nhãn select
  nhân viên trong popup bàn giao dùng `utils/employeeOptionText.js`.
- **Phần 3 xong đủ BE + FE**, đã verify tay trên FE :3005 / API :8002 / DB `hrm_prod_30_3_26`:
  bỏ trống ghi chú → viền đỏ + lỗi inline, popup KHÔNG đóng; nhập ghi chú → toast "Đã đóng nhu cầu",
  dòng chuyển badge `Đóng` xám, nút [+ Tạo Dự án TKT] biến mất, popup Lịch sử hiện đủ 2 dòng
  (Bàn giao 14/09 · Đóng nhu cầu 15/09).

Đang làm dở: không có.

Bước tiếp theo: gộp nhánh theo thứ tự `tpe` → `task_11386` → `task_11377`; chạy migration
`2026_09_15_000001` + seed quyền ở mọi môi trường; dọn dữ liệu test trên DB local (nhu cầu #54 vừa
bị đóng bằng tay, dòng lịch sử `close` id 4, và bản ghi `role_has_permissions` quyền 1191 gán tay
cho role 18 lúc verify).

Blocked: không có — Phần 2 hết treo vì mô tả mới xác nhận đúng công thức `T + N` đã code.

### Checkpoint — 2026-09-15 (#11390 — tab Nhu cầu của khách hàng)

Vừa hoàn thành: refactor tách `CustomerDemandList.vue` dùng chung + tab mới ở Công việc của tôi.
Đã verify tay: trang `/assign/customer-demands` chạy nguyên vẹn sau refactor (59 nhu cầu, đủ 13 cột,
bộ lọc/phân trang/cấu hình cột bình thường); tab `?tab=customer-demands` chỉ trả 1 nhu cầu của
chính người đăng nhập — đúng `only_mine`.

Commit: hrm-api `<điền khi commit>`, hrm-client `<điền khi commit>`.

Bước tiếp theo: gộp nhánh + chạy migration/seed ở các môi trường; dọn dữ liệu test DB local.

Blocked: không có.

## Phần 6 — Testcase QA (2026-09-17)

- [x] `testcase.xlsx` — **109 ca / 10 nhóm + nhóm phân quyền**, P0 71%, form chuẩn team (17 cột,
      9 mục mô tả, 2 khối summary DNS/TP). Script sinh: `gen_testcase.py`.
- [x] Phủ đủ 4 phần của #11386 + tab "Nhu cầu của khách hàng" (#11390): 5 cấp phân quyền xem ·
      13 cột đúng thứ tự khách chốt · cấu hình cột · bộ lọc (tìm nhanh, cây Công ty→Bộ phận→Nhân
      viên, Lĩnh vực, Nhóm ngành, Trạng thái) · sắp xếp + phân trang · đóng thủ công (ghi chú bắt
      buộc, ≤1000 ký tự, chặn ở máy chủ) · bàn giao đơn lẻ + hàng loạt (chặn cả lô khi lẫn nhu cầu
      không hợp lệ) · lịch sử cập nhật · thông báo cho người nhận · dịch phạm vi xem sang phòng mới.
- [x] Viết riêng TC cho **6 lỗi QA báo ở ghi chú #7 (16/09/2026)** để retest: tạo Dự án TKT xong
      phải về màn danh sách (IV.9) · Cấu hình cột hiển thị lưu được (I.3, I.4) · bảng không vỡ khi
      bật nhiều cột (I.6) · thông báo thiếu trường khi tạo Dự án TKT phải chỉ đúng ô (IV.10) · popup
      Tìm kiếm nâng cao chọn được người nhận (VI.4) · cột hạn không phải lúc nào cũng "Không thời
      hạn" (IV.13, IV.15 — nêu rõ 4 điều kiện khiến hạn rỗng).

### Checkpoint — 2026-09-17

Vừa hoàn thành: Phần 6 — testcase QA cho toàn bộ #11386.

Đang làm dở: không.

Bước tiếp theo:
- QA chạy bộ testcase; nhóm V/VI/VII cần ít nhất 2 tài khoản khác phòng ban để kiểm phần dịch phạm
  vi xem.
- **6 lỗi QA ở ghi chú #7 (16/09) chưa được xử lý trong đợt này** — task đang ở trạng thái "Phản
  hồi" trên Redmine, cần fix rồi mới khép.

Blocked: không.

## Phase QA — Sửa 6 bug QA phản hồi trên Redmine #11386 (17/09/2026)

Nguồn: comment của Lê Huyền Trang ngày 16/09/2026, trạng thái issue đổi sang **Phản hồi**.
Làm trên `tpe-develop-assign` (toàn bộ code #11386 + #11377 đã merge vào đó, user đang chuẩn bị đẩy dev).

- [x] **BUG 1** — Tạo Dự án TKT xong ra màn chi tiết thay vì danh sách.
      `add.vue` bám URD: Lưu chính thức → `/manager`, Lưu nháp → `/edit`. User chốt cả hai về
      **danh sách, đúng nơi đi vào**: có `?demand_id=` → `/assign/customer-demands`, không thì
      → `/assign/prospective-projects`. Thêm computed `listUrl`, dùng cho cả `url-back` của V2Footer.
- [x] **BUG 2** — Tùy chỉnh cột báo "Thao tác thất bại".
      `ColumnCustomizationService::updateOrCreate()` ghi `[$request->table => $request->columns]`
      — **mỗi màn là MỘT CỘT** trong bảng `column_customizations`. Cột `assign_customer_demands`
      chưa tồn tại → SQL lỗi. → migration thêm cột json nullable. **Đã chạy migrate trên LOCAL;
      dev/prod phải chạy `php artisan migrate` khi deploy.**
- [x] **BUG 3** — "Bảng đang vỡ" / "cuộn lên bị lọt".
      `V2BaseDataTable` đặt `max-height: 640px`; màn này 20 dòng/trang → bảng cao 873px → sinh
      **thanh cuộn dọc riêng lồng trong thanh cuộn trang**. Cuộn thì header sticky che nửa trên
      dòng đang trôi qua, lòi đuôi chữ (ảnh QA: "DUNG BANG" lơ lửng dưới header).
      User chốt **chỉ bỏ trần chiều cao ở riêng màn này** (`::v-deep .table-wrapper { max-height: none }`),
      KHÔNG sửa component chung vì **79 màn** đang dùng. ⚠️ Mọi màn 20 dòng/trang khác vẫn còn lỗi này.
- [x] **BUG 4** — Toast "Chưa nhập đầy đủ thông tin" mà không ô nào đỏ.
      BE bắt buộc người liên hệ qua `customer_contact_name` / `customer_contact_phone`, FE chỉ
      render lỗi của `customer_contact_id` → 422 không có chỗ hiện. → computed `contactError`
      đọc cả 3 key. Vế 2: bấm Lưu khi khối "Thêm nhanh liên hệ" còn gõ dở → chặn và báo ngay
      tại khối đó (`hasPendingQuickContact()` + `blockedByPendingContact()`), KHÔNG tự động lưu thay user.
- [x] **BUG 5** — Popup chọn người nhận bàn giao: click dòng không thấy đã chọn.
      `PopupStaff` chế độ chọn đơn **không tự đóng**, màn cha phải gọi `$bvModal.hide()`
      (xem `PopupStaff.onRowClick`). `CustomerDemandHandoverModal.onStaffPicked` thiếu dòng đó.
- [x] **BUG 6** — Cột "Thời gian hết hạn nhu cầu" chỉ hiện "Không thời hạn".
      **Không phải lỗi của màn này** — hệ quả của #11377 BUG 4 (BE không lưu `demand_due_days`
      nên mọi lĩnh vực đều N = 0). Đã fix ở `hrm-api` ace1f47ec. Verify lại: đặt N = 60 → cột ra 11/10/2026.

### Checkpoint — 2026-09-17

Vừa hoàn thành: 6/6 bug QA của #11386, đã verify từng cái bằng Playwright trên local.
Nhánh `tpe-develop-assign`: `hrm-api` **c1accb67d** · `hrm-client` **1b89b8c47**. Đã commit, CHƯA push.

File đã sửa:
- `hrm-api`: `database/migrations/2026_09_17_100000_add_assign_customer_demands_to_column_customizations.php` (mới)
- `hrm-client`: `pages/assign/prospective-projects/add.vue`,
  `pages/assign/prospective-projects/components/CustomerBlock.vue`,
  `components/assign/CustomerDemandList.vue`, `components/assign/CustomerDemandHandoverModal.vue`

⚠️ **Khi deploy phải chạy `php artisan migrate`** — thiếu cột là BUG 2 tái phát nguyên vẹn.

Bước tiếp theo: push lên dev, báo QA retest.
Blocked: 

## ĐỢT QA 2 — 4 bug phản hồi ngày 18-19/09, sửa 22/09/2026

Làm trên `tpe-develop-assign`. `hrm-api` **851a6a4c3** · `hrm-client` **1b12c2e09** (chưa push).

- [x] **BUG 1 + BUG 2 (BE) — CÙNG MỘT GỐC**: `ColumnCustomization::$casts` thiếu
      `'assign_customer_demands' => 'array'`. Cột là JSON, không cast thì:
      (a) lưu cấu hình cột hỏng → "Thao tác thất bại" (lộ rõ với tài khoản chưa từng lưu vì phải INSERT),
      (b) đọc ra nguyên **chuỗi JSON** thay vì mảng.
      ⚠️ Đợt trước đã thêm CỘT DB bằng migration nhưng **quên cast** — hai việc khác nhau, thiếu
      cái nào cũng hỏng. Thêm cột mới vào `column_customizations` lần sau phải làm ĐỦ CẢ HAI.
- [x] **BUG 2 (FE) — vạch lỗi ở cột đầu sau khi cuộn ngang.** Hit-test cho thấy layout ĐÚNG
      (`elementFromPoint` luôn trả ô dính) — chỉ phần VẼ ra sai: lỗi repaint của Chrome khi
      `position: sticky` nằm trong bảng `border-collapse: collapse`.
      → riêng bảng này dùng `border-collapse: separate` + `border-spacing: 0`, bù viền chỉ ở
      **phải + dưới** (để nguyên `border: 1px` 4 cạnh thì 2 ô cạnh nhau thành đường 2px).
      Đã thử và loại: `backface-visibility: hidden` (không ăn) · `separate` không bù viền (viền đôi).
      ⚠️ Đây là lỗi của `V2BaseDataTable`, **mọi màn có cột dính + cuộn ngang đều dính**. Mới vá 1 màn.
- [x] **BUG 3 — sắp xếp sai.** Mặc định xếp theo `meetings.start_date` (ngày DIỄN RA cuộc họp),
      không phải ngày thu thập nhu cầu → nhu cầu vừa nhập cho cuộc họp cũ bị đẩy xuống dưới.
      → đổi sang `meeting_investment_demands.created_at` DESC, vẫn chốt bằng id.
- [x] **BUG 4 — tích kẹt ở bản ghi bị người khác đóng.** Khi nạp lại chỉ loại dòng KHÔNG CÒN
      trên trang, mà dòng bị đóng vẫn nằm đó; checkbox đã `disabled` theo `can_handover` nên
      bấm không ra. → loại luôn dòng không còn bàn giao được, và `toggleOne` chỉ chặn TÍCH MỚI
      chứ không chặn BỈ TÍCH.

### Checkpoint — 2026-09-22

4/4 bug đã sửa và verify từng cái bằng Playwright trên local. Dữ liệu thử (cấu hình cột, `created_at`
của nhu cầu 57, trạng thái nhu cầu 56) đã khôi phục nguyên trạng.

Bước tiếp theo: push lên dev, báo QA retest.
Blocked: 

## Phần 7 — Testcase #11390 ghi thẳng vào Google Sheet của QA (2026-09-22)

Yêu cầu: QA xin testcase cho tab "Nhu cầu của khách hàng" (#11390) và muốn **thêm vào cuối** tab
`25.CV của tôi` của file Google Sheet "Testcase _Quản lý dự án", KHÔNG sửa/xoá testcase đã có.

- [x] **B1.** Đọc mô tả #11390 + code: `pages/assign/my-job/components/CustomerDemandsTab.vue` (vỏ mỏng
      gọi `CustomerDemandList` với `only-mine`), đăng ký tab thứ 7 ở `my-job/index.vue`, và nhánh
      `only_mine` ở `CustomerDemandService` (bỏ qua 5 cấp quyền, ép về người đăng nhập).
- [x] **B2.** Soạn **24 testcase** `TC-ROLE-45 → TC-ROLE-68` + 1 dòng tên nhóm "Tab Nhu cầu của khách
      hàng (#11390)", đúng 19 cột của tab đó (Module … Ghi chú TPE), ô không chứa xuống dòng để dán
      không vỡ cấu trúc. Script: `.plans/customer-demand-list/` → bản CSV lưu repo
      `testcase-11390-tab-cv-cua-toi.csv`.
- [x] **B3.** Dán vào Google Sheet: tải tab về dạng CSV để biết cấu trúc + dòng cuối (75), nạp khối
      dòng vào clipboard, chọn ô A76 bằng hộp tên rồi dán. Kết quả: vùng A76:R100.
- [x] **B4.** Đối chiếu sau khi dán: tab từ 75 → 100 dòng; các dòng 1-75 (kể cả TC-ROLE-01…44,
      dòng nhóm "Tab Chờ duyệt", "Đang tiển khai") giữ nguyên; 25 dòng mới đúng cột.
      Ảnh: `screenshots/sheet-11390-da-them.png`.

### Checkpoint — 2026-09-22

Vừa hoàn thành: Phần 7 — 24 TC cho #11390 đã nằm trong Google Sheet của QA.

Đang làm dở: không.

⚠️ Lưu ý: trình duyệt dùng để dán **không đăng nhập Google** (file cho phép ai có link đều sửa được),
nên lịch sử phiên bản của Sheet ghi nhận là "người dùng ẩn danh". Muốn có dấu vết tên người sửa thì
lần sau phải đăng nhập tài khoản Google trước khi dán.

Bước tiếp theo: QA chạy 24 TC mới; #11390 đang ở trạng thái "DNS đang test" trên Redmine.

Blocked: không.

## Phần 8 — Hết hạn rồi nhưng hiện "Không thời hạn" (phản hồi #11386, 2026-09-23)

Hiện tượng: nhu cầu hôm nay hiện `24/09/2026 (còn 1 ngày)`, sang ngày hết hạn thì cột "Thời gian hết
hạn nhu cầu" chuyển thành **"Không thời hạn"** — lẫn với nhu cầu mà lĩnh vực để N = 0.

Nguyên nhân: cột hạn dùng chung `MeetingInvestmentDemand::dueDate()`, hàm này trả `null` ngay khi
`status != DANG_THEO_DOI` hoặc đã gắn dự án TKT. Cron `assign:close-expired-customer-demands` chạy
01:20 và đóng nhu cầu **ngay trong ngày hết hạn** (`$today->gte($dueDate)`), nên từ 01:20 hôm đó trở
đi dòng mất luôn ngày hạn. Nhu cầu đã lập dự án TKT cũng dính cùng một `return null`.

- [x] **B1. BE — tách hạn HIỂN THỊ khỏi hạn NGHIỆP VỤ.** Thêm `deadlineDate(?int $dueDays)` ở
      `Modules/Assign/Entities/Meeting/MeetingInvestmentDemand.php`: chỉ tính `meeting.completed_at + N`,
      không xét trạng thái. `dueDate()` giữ nguyên ý nghĩa cũ (còn tự đóng/cảnh báo không) và gọi lại
      hàm mới sau khi qua guard trạng thái.
- [x] **B2. BE — `CustomerDemandService::attachDueDate()`**: `due_date_value` lấy từ `deadlineDate()`,
      còn `due_days_left` + `is_due_soon` vẫn theo `dueDate()` để nhu cầu đã đóng không đếm ngược và
      không bị tô cam. Truyền sẵn `$dueDays` cho cả 2 hàm (khỏi đọc lại danh mục từng dòng).
- [x] **B3. FE — `components/assign/CustomerDemandList.vue`**: dữ liệu đã đúng nên chỉ sửa chú thích
      cho khớp ngữ nghĩa mới; "Không thời hạn" nay chỉ còn cho N = 0 hoặc cuộc họp chưa Hoàn thành.
- [x] **B4. Verify (in-memory, KHÔNG ghi DB).** `php artisan tinker` giả lập N = 5 trên 3 nhu cầu có
      sẵn: Đang theo dõi → hiển thị 18/09/2026 + nghiệp vụ 18/09/2026; Đã đóng và Đã lập dự án →
      hiển thị 18/09/2026, nghiệp vụ NULL; N = 0 → NULL cả hai.

### Checkpoint — 2026-09-23

Vừa hoàn thành: Phần 8 B1-B4 — sửa BE + chú thích FE, verify logic bằng tinker.

Đang làm dở: chưa verify trên giao diện bằng Playwright vì DB local đang để `demand_due_days = 0` ở
mọi lĩnh vực (không có dòng nào có hạn để chụp). Cần user cho phép tạm đặt N > 0 cho 1 lĩnh vực rồi
trả lại nguyên trạng.

Bước tiếp theo: verify UI sau khi được phép sửa dữ liệu thử, rồi push lên dev cho QA.

Blocked: chờ user duyệt việc sửa tạm dữ liệu thử.

- [x] **B5. FE — cột Khách hàng thành hyperlink** (yêu cầu 2026-09-23): `#cell-customer_name` đổi
      thành `nuxt-link` tới `/assign/customers/{customer_id}`, class `v2-cell-link field-line` —
      cùng khuôn với cột Meeting / Dự án TKT trong chính component này. Không có `customer_id`
      (nhu cầu nhập tay tên khách) thì giữ text thường, không tạo link chết.

### Checkpoint — 2026-09-23 (bổ sung)

Vừa hoàn thành: B5 — hyperlink cột Khách hàng.

⚠️ **Không verify được bằng Playwright trên máy này**: API cổng 8000 đang chạy từ
`D:\CompanyProject\hrm\hrm-api` (bản repo KHÁC), nên code sửa ở `hrm-cursor` không có hiệu lực;
API đó còn trả 400 `Unknown column meeting_investment_demands.owner_employee_id` (DB của nó chưa
chạy migration `2026_09_14_000005_add_handover_to_customer_demands`). Thêm nữa DB local để
`demand_due_days = 0` ở mọi lĩnh vực nên không có dòng nào có hạn để chụp.

Bước tiếp theo: dựng API/client chạy từ `hrm-cursor` (hoặc verify trên dev sau khi push) rồi chụp
lại 2 thứ: cột Khách hàng bấm sang được chi tiết, và nhu cầu hết hạn hiện ngày thay vì
"Không thời hạn".

Blocked: chờ user chốt cách verify.

- [x] **B6. FE+BE — link khách hàng chỉ hiện khi mở được, và "Quay lại" về đúng nơi đi vào.**
      - `CustomerController::show` chặn theo phạm vi xem KH của ERP (403 rồi FE đá về danh sách KH,
        trông như lỗi) → thêm `CustomerService::visibleIds()` (bản hàng loạt của `isVisible()`, đúng
        1 query cho cả trang), `CustomerDemandService::attachCustomer()` gắn cờ, Resource trả
        `can_view_customer`; FE chỉ bọc `nuxt-link` khi cờ này bật, còn lại để text thường.
      - Link kèm query theo quy ước module Assign: `?from=customer-demands`, hoặc
        `?from=my-job&tab=customer-demands` khi mở từ tab "Công việc của tôi" (computed
        `customerBackQuery`, dựa trên prop `only-mine`).
      - `CustomerForm.vue`: `backUrl` từ hằng `/assign/customers` đổi thành computed đọc
        `from`/`tab`; 2 chỗ `V2Footer` đổi `url-back` → `:url-back="backUrl"`.

### Checkpoint — 2026-09-23 (verify trên giao diện)

Đã dựng riêng stack của repo này để verify (API `php artisan serve :8002` từ `hrm-cursor/hrm-api`,
client `npm run dev` :3005 theo `.env` sẵn có) — trước đó cổng 8000/3000 là của repo
`D:\CompanyProject\hrm`, nên code sửa ở đây không có tác dụng.

Đã verify:
- Cột Khách hàng render `a.v2-cell-link` href `/assign/customers/26?from=customer-demands`
  (ảnh `screenshots/verify-11386-link-kh.png`).
- Bấm Quay lại ở `/assign/customers/620?from=customer-demands` → về `/assign/customer-demands`;
  với `?from=my-job&tab=customer-demands` → về `/assign/my-job?tab=customer-demands`, đúng tab.
- Dòng KH ngoài phạm vi xem (`can_view_customer=false`) để chữ thường, không tạo link chết.
- Cột hạn: dòng trạng thái **Đóng** có ngày hạn thì hiện `24/09/2026` thay vì "Không thời hạn".

⚠️ Cách verify cột hạn: DB local để `demand_due_days = 0` ở mọi lĩnh vực nên không có dòng nào có
hạn thật; đã bơm giá trị vào **bộ nhớ trình duyệt** (`$set` trên row của `tableData`) để xem nhánh
render — **không ghi DB**. Nghiệp vụ tính hạn đã verify riêng bằng tinker (Phần 8 B4).

Bước tiếp theo: push lên dev, QA retest bằng dữ liệu có `demand_due_days > 0`.

Blocked: không.

## ĐỢT QA — 5 bug #11390 phản hồi ngày 23/09, sửa 24/09/2026

`hrm-api` **0f98ea8ec** · `hrm-client` **07aa4fc66** trên `tpe-develop-assign` (chưa push).

- [x] **BUG 1 — nhu cầu không có lịch sử từ lúc tạo.** Bảng lịch sử trước đây chỉ ghi **Bàn giao**
      và **Đóng**, nên nhu cầu vừa thu thập mở popup Lịch sử ra là trống.
      → thêm 2 hành động **Tạo mới** / **Cập nhật**, ghi trong `MeetingService::syncInvestmentDemands()`.
      ⚠️ **2 cái bẫy đã trả giá ngay lúc verify:**
      1. Phải chụp thay đổi **TRƯỚC `save()`** — sau save `isDirty()` rỗng, không còn gì để ghi.
      2. `isDirty()` **vẫn báo true khi chỉ đổi KIỂU chứ không đổi GIÁ TRỊ**: cột decimal đọc từ DB
         ra chuỗi `'3000000000.00'` còn payload là số nguyên `3000000000`. Lần chạy thử đầu tiên đã
         đẻ ra dòng rác `4,500,000,000 -> 4,500,000,000`. → so sánh theo giá trị **đã chuẩn hoá**.
- [x] **BUG 2 — màn tạo Dự án TKT không kế thừa gì.** Nút chỉ gửi `demand_id` + `meeting_id`, mà
      `add.vue::applyCustomerFromQuery()` **thoát ngay khi thiếu `customer_id`** → không chạy gì cả.
      → gửi thêm `customer_id` (+ tên/mã làm dữ liệu dự phòng khi API chi tiết KH trả 403),
      và kế thừa luôn **Ngân sách dự kiến** ← `expected_amount`, **Nhóm ngành** ← `sector_id`.
      Người liên hệ tự điền theo luồng chọn KH sẵn có (KH nào chưa có liên hệ thì để trống — đúng).
- [x] **BUG 3 — bộ lọc reset khi chuyển tab.** Màn Công việc của tôi render tab bằng `v-if` nên
      chuyển tab là component bị **HUỶ** (đã đo: sau khi chuyển, tìm lại component trả `false`).
      Trang `/assign/customer-demands` không dính vì có `filterStateMixin`, nhưng mixin đó bám
      `beforeRouteLeave` — hook **chỉ chạy ở component TRANG**, tab là component con nên vô dụng.
      → `CustomerDemandsTab` tự giữ bộ lọc vào localStorage, **khoá RIÊNG** (dùng chung khoá với màn
      danh sách là bộ lọc bên này nhảy sang bên kia — 2 nơi phạm vi dữ liệu khác nhau), hạn 10 phút.
- [x] **BUG 4** — còn 0 ngày: `(hết hạn hôm nay)` → `(hết hạn)`.
- [x] **BUG 5** — cột "Thời gian hết hạn nhu cầu" khi không có hạn: `Không thời hạn` →
      `Không giới hạn thời gian hiệu lực`, đồng bộ với màn Lĩnh vực Công ty kinh doanh (#11377).

### Checkpoint — 2026-09-24

5/5 bug đã sửa và verify từng cái bằng Playwright + tinker trên local.
Dữ liệu thử (nhu cầu #60, giá trị + ngày của #59, các dòng lịch sử) đã khôi phục nguyên trạng.

Bước tiếp theo: push lên dev, báo QA retest.
Blocked: 
