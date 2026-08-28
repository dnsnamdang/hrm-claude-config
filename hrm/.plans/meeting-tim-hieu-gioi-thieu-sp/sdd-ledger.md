# SDD ledger — plan: .plans/meeting-tim-hieu-gioi-thieu-sp/plan.md

Spec: `docs/superpowers/specs/2026-08-21-meeting-tim-hieu-gioi-thieu-sp-design.md`

## Setup (2026-08-21)

- **Nhánh**: `meeting-by-market` ở **cả 2 repo** (`hrm-api`, `hrm-client`) — user chốt "dùng luôn nhánh này". Working tree sạch lúc bắt đầu.
- **Commit**: được commit **local**, TUYỆT ĐỐI không push (user chốt, đè lên luật cấm commit của `CLAUDE.md`).
- **Không worktree**: `HRM/` không phải git repo, `hrm-api` + `hrm-client` là 2 repo riêng. Ledger quản tay ở file này theo tiền lệ `.plans/meeting-by-market/sdd-ledger.md`.
- **PHP**: `/opt/homebrew/opt/php@7.4/bin/php` (php không có trên PATH).

## Pre-flight conflict scan

### Cặp task dùng chung file / interface

| Task A | Task B | File / interface chung | Kết quả |
|--------|--------|------------------------|---------|
| 1.1 | 1.2 | cột `meeting_types.code` | OK — 1.1 tạo cột, 1.2 dùng. Đúng thứ tự |
| 1.2 | 1.3, 1.4, 1.5 | `CODE_PRODUCT_INTRO`, `SYSTEM_CODES`, `isSystem()` | OK — 1.2 định nghĩa trước, 3 task sau tiêu thụ |
| 1.4 | 1.4 | `MeetingTypeController` + `MeetingTypeService` | OK — cùng 1 task, không tranh chấp |
| 1.5 | 1.6 | field `is_system` | OK — BE trả trước, FE dùng sau |
| 2.1 | 2.2 | `GET assign/meeting/investment-scopes` | OK — endpoint trước, store sau |
| 2.1 | 3.1 | `TpScope` | OK — 2.1 tạo, 3.1 dùng trong `syncInvestmentDemands` |
| 2.1 | 3.3 | **`MeetingController.php`** | OK — 2.1 thêm method `investmentScopes()` + `use TpScope`; 3.3 sửa `$request->only()` / `update()` / `store()` / eager load. Khác vùng code |
| 2.2 | 3.4, 3.5 | `MEETING_TYPE_PRODUCT_INTRO`, `fetchInvestmentScopes`, `getInvestmentScopes` | OK — đúng thứ tự |
| 3.1 | 3.3, 4.1 | `investment_demands()`, `syncInvestmentDemands()` | OK |
| 3.3 | 3.5 | `meeting_type_code` (transformer → computed FE) | OK — 3.3 trước 3.5 |
| 3.4 | 3.5, 4.2, 5.1 | `buildPayload()`, `loadScopes()`, `data-testid` | OK — 3.4 trước cả 3 |
| **3.5** | **4.2** | **`MeetingReport.vue`** | OK — 4.2 cần `needInvestmentSurvey` + `$refs.investmentSurvey` do 3.5 tạo. Thứ tự 3.5 → 4.2 đúng |
| 3.4 | 3.5 | ghi ngược `form` (watcher) vs merge `buildPayload()` vào payload | **Xem C3** |

### Tự mâu thuẫn trong từng task

| Task | Kết quả |
|------|---------|
| 1.1 | OK — `down()` drop unique trước drop column, Bước 6 verify rollback |
| 1.2 | OK — hằng khai trước khi 3 hàm `isCan*` dùng |
| 1.3 | OK — verify idempotent bằng cách chạy lần 2 |
| 1.4 | OK — 5 guard, Bước 8 có ca regression bản ghi thường |
| 1.5 | OK |
| 1.6 | OK — checkbox `v-if` khớp với `is_can_delete=false` nên "chọn tất cả" cũng loại đúng |
| 2.1 | OK — route đặt trước `{id}`, Bước 7 verify đúng điểm đó |
| 2.2 | OK — cảnh báo trùng khoá `scopes` đã ghi rõ |
| 3.1 | OK — cảnh báo tinker không có `auth()` nên `created_by` có thể NULL, verify lại ở 3.3 |
| 3.2 | OK — code Bước 1 khớp cấu trúc file thật (dòng 140-147) |
| 3.3 | **Xem C1** — thiếu `store()` |
| 3.4 | **Xem C2** — `data-testid` trên component Vue |
| 3.5 | OK |
| 4.1 | OK — `$sectionNumber` tự tăng, có ca regression loại meeting khác |
| 4.2 | OK — đã cảnh báo kiểm `this.$dayjs` |
| 5.1 | OK — testid do 3.4 gắn |
| 5.2 | OK — verify thuần |

### Rulings

**C1 — Task 3.3 bỏ sót `MeetingController::store()`.**
`store()` (dòng 158) dùng **đúng cùng pattern** `$request->only([...])` có `conclusion`, rồi gọi `syncReports()`. Tab "Biên bản" **có sẵn ở màn Tạo mới** (`MeetingForm.vue:384-389` — `baseTabs` luôn gồm `reports`, không gate theo `isCreateMode`). Nên user điền khảo sát lúc TẠO MỚI sẽ bị **mất im lặng**.
`Ruling: mở rộng Task 3.3 sang store() — thêm 2 cột has_*_demand vào $request->only() và gọi syncInvestmentDemands() ngay sau syncReports(), y hệt update(). — Vì spec §5.8 nói "mọi đường ghi", và tab Biên bản dùng được lúc tạo mới. — Nếu sai: thêm 2 dòng thừa ở store(), vô hại (create không bao giờ ở status 3 nên validate không đổi).`

**C2 — `data-testid` trên component Vue có thể rơi vào wrapper, không phải `<input>`.**
`b-form-radio`, `V2BaseCheckbox`, `V2BaseInput` là component bọc — attribute không phải prop rơi vào **element gốc của component**, thường là `<div>` wrapper chứ không phải thẻ `<input>` bên trong. E2E Task 5.1 gọi `.check()`, `.fill()`, `.toBeDisabled()` — đều cần đúng `<input>`.
`Ruling: Task 3.4 phải kiểm DOM thật sau khi render và ghi vào report testid rơi vào đâu. Rơi vào wrapper thì GIỮ NGUYÊN tên testid (E2E đã bám) và Task 5.1 đổi selector thành getByTestId('x').locator('input'). Không đổi tên testid. — Vì tên testid là interface đã chốt giữa 3.4 và 5.1, đổi tên thì gãy cả 2. — Nếu sai: Task 5.1 phải sửa selector, tốn 1 vòng fix.`

**C3 — Trùng đường ghi payload giữa Task 3.4 (watcher ghi ngược `form`) và Task 3.5 (merge `buildPayload()`).**
Hai đường cùng đặt 3 field vào request. Không phải lỗi: watcher tồn tại **vì `unsavedChangesMixin`**, merge tồn tại **vì không chắc `MeetingForm` dựng payload bằng spread `form` hay liệt kê key tay**. Giá trị y hệt nhau nên idempotent.
`Ruling: giữ CẢ HAI, bắt buộc ghi comment nêu rõ 2 mục đích khác nhau để reviewer không gắn cờ "duplication". — Vì bỏ watcher thì mất cảnh báo unsaved, bỏ merge thì rủi ro mất field nếu payload liệt kê key tay. — Nếu sai: thừa 3 dòng gán lặp, không ảnh hưởng hành vi.`

**C4 — Tiền lệ `reports.*.expected_deadline` viện dẫn trong spec E-13 đã đổi trên đĩa.**
Spec E-13 nói rule chặn ngày quá khứ của `expected_start_date` bám theo `reports.*.expected_deadline` (`required|after_or_equal:today`). File `MeetingUpdateApiRequest.php` **vừa đổi**: rule đó nay là điều kiện — chỉ chặn quá khứ khi `$currentStatus == 1` (Lên lịch hẹn), họp đã diễn ra thì giữ nguyên hạn cũ.
`Ruling: GIỮ NGUYÊN after_or_equal:today vô điều kiện cho expected_start_date (user chốt rõ ở lượt review spec: "Chặn không cho chọn quá khứ"); chỉ sửa lại câu chữ E-13 trong spec vì tiền lệ viện dẫn không còn đúng. KHÔNG copy pattern điều kiện mới. — Vì 2 field khác bản chất: expected_deadline là hạn xử lý của việc đã phát sinh (quá khứ hợp lệ), expected_start_date là KẾ HOẠCH đầu tư tương lai của khách hàng. Copy pattern điều kiện sẽ vô hiệu hoá rule hoàn toàn (khảo sát bắt buộc ở status 3, lúc đó currentStatus=2 nên nhánh điều kiện không bao giờ chặn). — Nếu sai: mở lại meeting cũ có ngày đã trôi qua rồi Lưu sẽ bị 422, user phải chọn lại ngày.`

**C5 — Gom task 1.2+1.3+1.4+1.5 vào 1 dispatch.**
Bốn task cùng thao tác trên một cụm file nhỏ (`MeetingType.php`, seeder mới, `MeetingTypeController.php`, `MeetingTypeService.php`, `MeetingTypeResource.php`) và phụ thuộc nhau chặt: 1.2 tạo `isSystem()` → 1.3 seed bản ghi → 1.4 dùng `isSystem()` chặn 423 → 1.5 trả cờ ra API. Verify của 1.4 (curl 5 guard) và 1.5 (curl getAll) đều **cần bản ghi do 1.3 tạo**, nên tách ra thì 3 trong 4 task không tự verify được.
`Ruling: gộp 1.2–1.5 thành 1 dispatch, 1 review surface, 1 commit. Giữ 1.1 và 1.6 riêng (1.1 là migration chạy trước, 1.6 là repo khác + FE). — Vì SDD nói gom "small same-shape work" cùng cụm file, và tách ra sẽ khiến 4 subagent cùng đọc lại một file. — Nếu sai: diff review 1 lượt to hơn (~5 file nhỏ), vẫn trong tầm 1 reviewer.`

## Tiến độ

- Task 1.1: dispatched (sonnet), BASE hrm-api = 134cdf6
- Task 1.1: implementer DONE (commit `fcccceb`) — schema verify khớp brief, rollback --step=3 + migrate lại sạch, `dropUnique` đúng tên ngay lần đầu.
  - Concern implementer nêu: `artisan migrate` kéo theo 1 migration pending có sẵn không thuộc scope (`2026_08_18_000001_add_description_to_solutions_table`). Hành vi mặc định Laravel, `git status` xác nhận chỉ 3 file target được commit. Không phải lỗi của task.
  - Task reviewer: dispatched (sonnet), package `task-1.1-review-package.md`
- Task 1.2–1.5 (gộp, xem C5): dispatched (sonnet), BASE hrm-api = `fcccceb`
- Task 1.1: task review → **Spec ✅ · Quality Approved**. Reviewer tự chạy lại `SHOW COLUMNS`/`SHOW CREATE TABLE` và xác nhận output khớp từng ký tự với report (kể cả tên constraint tự sinh) → bằng chứng verify là thật, không suông.
  - **C6 — finding Important (plan-mandated): `after()` có thể rebuild toàn bảng `meetings`.**
    Dữ kiện đo thật: MySQL **8.0.43** (INSTANT ADD COLUMN hỗ trợ vị trí bất kỳ, kể cả `AFTER`, từ 8.0.29 — Laravel không ép `ALGORITHM` nên MySQL tự chọn INSTANT). Bảng `meetings` = **40 dòng** local; đây là bảng 1 dòng/cuộc họp nên production cũng ở mức nghìn, không phải triệu.
    `Ruling: GIỮ NGUYÊN after() — không sửa migration. — Vì trên 8.0.29+ thao tác này là INSTANT, không rebuild; và kể cả rơi về COPY thì bảng cỡ này khoá dưới một giây. Đổi sang append cuối bảng chỉ đổi thứ tự cột cho xấu đi mà không mua được gì. — Nếu sai: production chạy MySQL < 8.0.29 VÀ bảng meetings lớn bất thường thì lần migrate đầu khoá bảng meetings vài giây.`
  - Minor (deferred): câu chữ Bước 6 trong report giải thích vòng vo về cách xác nhận tên unique index; bằng chứng thật (rollback không throw) mạnh hơn nhưng không được nêu thẳng. Không ảnh hưởng code.
  - ⚠️ reviewer nêu (controller tự resolve): lo schema cache của module khác lệch sau migration. **Không phải gap** — Laravel 8 không giữ schema cache bền, `doctrine/dbal` đọc live, repo không có OpenAPI schema dump. Đóng lại, không vào fix loop.
- **Task 1.1: complete (commit `fcccceb`, review clean, 1 finding Important đã ruling giữ nguyên)**
- Task 1.2–1.5: implementer DONE (commit `91bdd89`, 5 file, 103+/5-). Verify: tinker `isSystem`/`isCan*` khớp; seeder tạo id=7 và idempotent (n=1 sau 2 lần chạy); **5 guard đều trả 423** đúng message; regression lock/unlock bản ghi thường id=3 vẫn 200; `updated_by=1170` không NULL; `getAll` trả `code`+`is_system` đúng cho cả 7 bản ghi.
  - **Sửa lỗi brief (áp cho MỌI task sau dùng curl)**: endpoint login thật là `POST /api/v1/users/auth/login` (KHÔNG phải `/api/v1/login`), token nằm ở field **`access_token` top-level** (KHÔNG phải `data.token`). Brief Task 1.4 Bước 7 ghi sai, implementer tự tra ra. Phải truyền thông tin này vào brief Task 2.1 và 3.3.
  - Concern: `database/e2e_provision.php` lỗi khi tạo user thứ 2 (nocost) do rác data local; user admin cần dùng đã tạo xong trước lỗi. Không thuộc scope.
  - **C7 — bản ghi hệ thống id=7 có `created_by`/`updated_by` = 0 (không phải NULL).**
    Seeder chạy qua console nên `BaseModel` không có `Auth::user()`; cột `meeting_types.created_by` là `integer NOT NULL` (migration gốc 2025_11_21) nên **không thể** để NULL. Hệ quả: cột Người tạo/Người cập nhật của riêng bản ghi này rỗng trên UI.
    `Ruling: chấp nhận, không sửa. — Vì bản ghi hệ thống do hệ thống sinh, không có người tạo là đúng ngữ nghĩa; cột NOT NULL nên 0 là giá trị duy nhất khả dĩ; và không ảnh hưởng logic khoá 423. — Nếu sai: QA soi màn danh mục thấy 1 dòng trống cột Người tạo, phải giải thích.`
  - Task reviewer: dispatched (sonnet), package `task-1.2-1.5-review-package.md`
- Task 1.6: dispatched (sonnet), BASE hrm-client = `b2e9c1c`
- Task 1.2–1.5: task review → **Spec ✅ · Quality Approved**. 5/5 guard đủ (kể cả `unlock()` vốn không có guard nào); `isSystem()` dùng đúng whitelist; `updateOrCreate` chỉ chặn nhánh có `id`, không chặn nhầm tạo mới; không scope creep. Reviewer tự grep xác nhận không còn đường nào khác ghi `meeting_types`, và `importMeetingTypes()` chỉ `create()` + check trùng tên nên không lách được.
  - **C8 — finding Important (plan-mandated): guard trong `updateOrCreate` KHÔNG chạy trước validate.**
    `updateOrCreate(MeetingTypeRequest $request)` nhận FormRequest → Laravel validate ngay lúc resolve tham số, trước thân hàm. Payload sửa bản ghi hệ thống mà **thiếu field** sẽ trả **422** thay vì 423. Đúng cái bẫy `CLAUDE.md` đã ghi ("Controller nhận FormRequest thì `if` đầu hàm KHÔNG chạy trước validate → phải đặt guard ở middleware route, khuôn `CheckCustomerNotLocked`"). Plan chỉ định nguyên văn cách đặt guard trong thân hàm nên đây là lỗi kế thừa từ plan, không phải implementer chệch hướng.
    `Ruling: PARK — chấp nhận, không dựng middleware. — Vì không có đường ghi nào lọt: payload HỢP LỆ thì guard chạy và trả đúng 423; payload KHÔNG hợp lệ thì validate chặn trước, dữ liệu vẫn không bị sửa. Sai lệch duy nhất là mã lỗi 422 thay vì 423 cho payload rác gọi thẳng API — không task nào phía sau phụ thuộc vào mã này. Dựng middleware mới cho route POST không có route-param (phải đọc id từ body) là chi phí không tương xứng. — Nếu sai: người gọi thẳng API bằng payload thiếu field nhận message "name required" thay vì "Loại meeting hệ thống, không được phép sửa" — khó hiểu hơn, nhưng không mất mát dữ liệu.`
  - Minor (deferred): `created_by/updated_by = 0` — reviewer đối chiếu `BaseModel.php:28-38` xác nhận đúng nguyên nhân, trùng với ruling C7.
  - ⚠️ reviewer nêu (controller resolve): không tự chạy lại curl nên chỉ kiểm được tính nhất quán nội tại của output. **Chấp nhận** — đúng chỉ dẫn "không chạy lại test implementer đã chạy"; tính nhất quán message/id/mã lỗi đã được đối chiếu với diff.
- **Task 1.2–1.5: complete (commit `91bdd89`, review clean, 1 Important đã park)**
- **C9 — Plan ghi sai phiên bản Node.** Plan viết `nvm use 14` (theo `CLAUDE.md`), nhưng máy này **không có Node 14** (chỉ 12.18.4 / 12.22.12 / 20.20.1) và memory phiên trước ghi rõ client Nuxt chạy bằng **Node 12 + heap 8192**. Task 1.6 vì vậy không build verify được.
  `Ruling: sửa plan sang "nvm use 12 && NODE_OPTIONS=--max-old-space-size=8192" ở cả 4 chỗ. — Vì đó là môi trường thật đang có và đã chạy được ở phiên trước. — Nếu sai: build FE fail, phải cài Node 14 rồi chạy lại.`
- **C10 — Verify FE bằng mắt/browser dồn về 1 lượt.**
  `Ruling: KHÔNG build kiểm từng task FE riêng lẻ; dồn toàn bộ verify giao diện + E2E vào một lượt sau Phase 4, vì Phase 5 dù sao cũng cần app chạy thật. — Vì build Nuxt 2 tốn vài phút mỗi lần và thay đổi của Task 1.6 chỉ là 4 dòng v-if, review code tĩnh đủ bắt lỗi cú pháp. — Nếu sai: lỗi giao diện lộ muộn hơn, phải quay lại sửa ở cuối Phase 4.`
- Task 1.6: task review → **Spec ✅ · Quality Approved**, không finding Critical/Important. Đủ 4 `v-if` (checkbox :151, Khoá :199, Sửa :239, Xoá :262); nút Xem :224 còn nguyên; không đụng `:disabled`/`:title` của bản ghi cũ; file LF thuần (reviewer kiểm độc lập, 0 ký tự CR) → không phá line ending.
  - Reviewer xác nhận thêm: `selectableItems` (:543) lọc theo `is_can_delete`, mà BE đã trả `false` cho bản ghi hệ thống → "chọn tất cả"/xoá hàng loạt vốn đã an toàn trước khi có `v-if`. `is_system` luôn có trong `item` vì `tableData` chỉ gán 1 chỗ từ API. Không có đường lách.
  - ⚠️ ×2 (controller resolve): đều là "chưa xem bằng mắt trên browser" — **đã có ruling C10**, dồn về lượt verify FE sau Phase 4. Không phải gap.
- **Task 1.6: complete (commit `e51d159`, review clean)**
- **=== PHASE 1 HOÀN TẤT === (hrm-api `fcccceb`+`91bdd89`, hrm-client `e51d159`)**
- Task 2.1: dispatched (sonnet), BASE hrm-api = `91bdd89`
- Task 2.2: dispatched (sonnet), BASE hrm-client = `e51d159`
- **C11 — Gom task 3.1+3.2+3.3 vào 1 dispatch.** Cùng repo `hrm-api`, phụ thuộc chặt, và **Task 3.2 tự nó không verify được** (chính brief 3.2 Bước 5 ghi "hoãn sang Task 3.3").
  `Ruling: gộp 3.1–3.3 thành 1 dispatch + 1 commit, kèm bản vá ruling C1 (mở rộng sang store()) dán ngay đầu brief. — Cùng lý do như C5. — Nếu sai: diff review to hơn (~5 file BE).`
- Task 2.2: implementer DONE (commit `2592830`, 2 file, 41+/0-). `store/optionsSelect.js` giữ nguyên **CRLF** (kiểm trước/sau), diff toàn dòng thêm. Bộ `scopes`/`SET_SCOPES`/`fetchScopes`/`getScopes` cũ còn nguyên 4 chỗ; bộ mới `investmentScopes`/... tách bạch (grep xác nhận).
  - Bỏ qua Bước 6-7 (verify qua browser console) theo ruling C10. Endpoint BE chưa tồn tại lúc chạy nên chỉ verify logic tĩnh theo contract.
  - Task reviewer: dispatched (sonnet)
- Task 2.1: implementer DONE_WITH_CONCERNS (commit `ba480fd`, 3 file, 72+/0-). Endpoint trả đúng 13 lĩnh vực; `include_ids` ẩn/hiện đúng lĩnh vực đã khoá kèm `is_locked: true`; route không bị `{id}` nuốt (200); `erp2326.scopes` đã trả về nguyên trạng 13/13 active (chứng minh bằng cả SQL lẫn 1 lần gọi API cuối).
  - Concern 1: `artisan route:list` **hỏng toàn repo** trên nhánh này do lỗi CÓ SẴN (`Modules\Decision\Http\Controllers\DecisionController` thiếu). Implementer xác nhận pre-existing bằng `git stash`, thay bằng dump router qua tinker. → chuyển reviewer xác nhận lại.
  - **C12 — Local DB đang gộp: `mysql` và `mysql2` hiện trả CÙNG 13 dòng `scopes` kiểu ERP.**
    `.env` trỏ `DB_DATABASE=hrm_erp` (DB đã gộp) chứ không phải `hrm_tpe`. Hệ quả nguy hiểm: **nếu code lỡ dùng connection mặc định thay vì `mysql2` thì test local VẪN PASS** mà production đọc nhầm bảng (production HRM có `scopes` = "Nhóm ngành" 22 dòng). Bằng chứng "đếm ra 13 dòng" trong report KHÔNG phân biệt được connection.
    `Ruling: không đổi code (implementer đã hardcode 'mysql2' đúng yêu cầu); thay vào đó CHUYỂN gánh nặng verify sang reviewer — yêu cầu reviewer đọc thẳng code xác nhận $connection = 'mysql2' thay vì tin vào con số 13. — Vì đây là lỗ hổng của BẰNG CHỨNG, không phải của code. — Nếu sai: production đọc nhầm danh mục "Nhóm ngành" thay vì "Lĩnh vực đầu tư", user chọn ra danh sách vô nghĩa.`
  - **C13 (rủi ro tương lai, KHÔNG hành động bây giờ)**: `CLAUDE.md` cấm dùng `mysql2` cho tính năng mới **trên nhánh `gop_db`** ("mysql2 trỏ DB ERP CŨ, id lệch"). Feature này nằm trên nhánh `meeting-by-market` (hậu duệ `tpe`) nên hợp lệ, và chính feature meeting-by-market cũng đang dùng `mysql2` cho provinces.
    `Ruling: giữ mysql2, KHÔNG xử lý bây giờ. — Vì user đã chốt rõ "lấy qua second DB: scopes", và nhánh hiện tại được phép. — Nếu sai: khi merge sang dòng gop_db sau này, TpScope phải đổi sang connection mặc định + map lại id. GHI VÀO BÀN GIAO cho user.`
  - Task reviewer: dispatched (sonnet), có nhấn mạnh C12
- Task 2.2: task review → **Spec ✅ · Quality NEEDS WORK** (1 Critical, 1 Important, 1 Minor).
  - **C14 — Critical (plan-mandated): cache lĩnh vực bị "nhiễm" mục đã khoá, rò rỉ sang bản ghi khác.**
    Action commit TOÀN BỘ response (gồm mục khoá do `include_ids` kéo về) vào state dùng chung. Mở bản ghi A dùng lĩnh vực khoá #99 → cache 14 mục; sang bản ghi B không truyền `includeIds` → `missing=[]` nên trúng cache → dropdown của B hiện #99 không liên quan, treo tới khi F5.
    Reviewer chỉ ra **cùng file `store/optionsSelect.js` đã có `fetchProjectPhases` (dòng ~361-401) từng dính đúng bug này và ĐÃ FIX**, kèm comment mô tả y hệt kịch bản. Code mẫu trong plan của tôi không bám tiền lệ đó → lỗi của plan, không phải implementer.
    `Ruling: SỬA (vào fix loop). — Vì finding đúng, có tiền lệ đã fix ngay cạnh trong cùng file, và LOAD-BEARING: Task 3.4 (chưa dispatch) đang thiết kế đọc qua getter — đúng đường rò rỉ. — Nếu sai: thêm 1 vòng fix, code phức tạp hơn vài dòng.`
  - Important: `catch` trả `[]` thay vì cache cũ → select có thể trống, vi phạm luật "danh mục khoá vẫn phải hiện". `fetchProjectPhases` trả `state.projectPhases`. → sửa.
  - Minor: không lọc `null`/`''` khỏi `includeIds` như `fetchProjectPhases` làm. → sửa luôn cùng vòng.
  - Reviewer xác nhận OK: case (a)-(e) cache/refetch, `Number(id)` an toàn cho `['2']` vs `[2]`, query `include_ids[]=` có encode đúng, không duplicate id.
  - **Sửa lan sang plan Task 3.4** (chưa dispatch nên rẻ): đổi từ `mapGetters(['getInvestmentScopes'])` sang lưu giá trị return vào `data.scopeOptions`; `buildRows()` đọc `scopeOptions`. Đã cập nhật cả khối Interfaces của 2.2 và 3.4.
  - Fix round 1/5: resume implementer 2.2 với 3 finding.
- Task 2.1: task review → **Spec ✅ · Quality Approved**, 0 Critical/Important. Reviewer verify độc lập rất chắc:
  - Đọc `.env` xác nhận `DB_DATABASE=hrm_erp` (mặc định) vs `DB_DATABASE_SECOND=erp2326` (`mysql2`) → 2 DB tách biệt ở tầng config bất kể data local đang trùng. **Giải quyết đúng lo ngại C12** — không dựa vào con số 13.
  - Đọc `Modules/Assign/Entities/Scope/Scope.php` xác nhận model đó KHÔNG khai `$connection`/`$table` → đọc bảng `scopes` trên connection mặc định, tức cảnh báo nhầm bảng trong docblock `TpScope` là chính xác, không phải suy đoán.
  - Đọc `BaseModel.php:28-61` xác nhận lý do không `extends BaseModel` là đúng kỹ thuật.
  - PHP 7: `catch (Exception)` KHÔNG bắt `\Error`/`TypeError` (không kế thừa `Exception`) nhưng CÓ bắt `PDOException`/`QueryException` → catch đúng phạm vi, không che lỗi lập trình mà vẫn trả 503 khi mất kết nối.
  - Xác nhận `/investment-scopes` nằm trong group `auth:api`; không route Meeting nào trong file gắn `checkPermission` → không thêm quyền là nhất quán, không phải ngoại lệ tự chế.
  - **Tự tái hiện concern 1**: chạy `route:list` ra đúng lỗi `Modules\Decision\Http\Controllers\DecisionController does not exist`, truy nguồn `Modules/Decision/Routes/web.php:17` (controller string không namespace) — file khác module, xác nhận **lỗi có sẵn**, không do task 2.1.
  - Minor (deferred): `array_map('intval', $includeIds)` không lọc phần tử mảng lồng (payload dị dạng `include_ids[][]=1`) → E_WARNING "Array to integer conversion", quy về 1/0. Không phải lỗ hổng bảo mật, chỉ log rác.
  - ⚠️ ×3 (controller resolve): hành vi FE khi nhận 503 → thuộc Task 3.4, sẽ kiểm ở đó. Số liệu `scopes` production → không có quyền truy cập, chấp nhận. Không chạy lại curl → đúng chỉ dẫn.
- **Task 2.1: complete (commit `ba480fd`, review clean, 1 Minor deferred)**
- Task 3.1–3.3 (gộp, xem C11): dispatched (sonnet), BASE hrm-api = `ba480fd`
- Task 2.2: fix round 1/5 (3 addressed theo báo cáo implementer — cache chỉ giữ mục active, return trả full list, catch trả cache cũ, lọc includeIds; commits `2592830`..`f975e7d`). Re-review có phạm vi: dispatched (sonnet).
- Task 2.2: re-review có phạm vi → **F1/F2/F3 đều ADDRESSED, không có hỏng hóc mới**.
  - Reviewer phân tích thêm 2 điểm và kết luận không phải bug: (a) sau khi lọc `is_locked` khỏi cache thì mục khoá luôn kích `missing` → luôn gọi lại API; đó là trade-off CỐ Ý, giống hệt tiền lệ `fetchProjectPhases`. (b) shape return khác nhau giữa nhánh cache-hit (chỉ active) và nhánh API (active + khoá) không tạo nghịch lý, vì mục khoá không bao giờ vào cache nên không thể rơi vào nhánh cache-hit.
  - Bộ `scopes` cũ nguyên vẹn (dòng 56/238/248/492); file vẫn CRLF; diff đúng 21+/6-.
- **Task 2.2: complete (commits `2592830`..`f975e7d`, review clean sau 1 vòng fix)**
- **=== PHASE 2 HOÀN TẤT === (hrm-api `ba480fd`, hrm-client `f975e7d`)**
- Task 3.4: dispatched (sonnet), BASE hrm-client = `f975e7d`
- Task 3.4: implementer DONE (commit `82c1bc7`, 1 file mới 335 dòng, LF).
  - **C2 ĐÃ TRẢ LỜI DỨT ĐIỂM** — bảng `data-testid` rơi vào đâu:
    | testid | rơi vào |
    |---|---|
    | `investment-survey`, `scope-row` | `<div>` thuần |
    | `q1-yes/q1-no/q3-yes/q3-no` | **thẳng vào `<input type=radio>`** (bootstrap-vue `formRadioCheckMixin` spread `$attrs` lên input) |
    | `scope-check` | **thẳng vào `<input type=checkbox>`** (cả 2 lớp bọc đều forward attrs) |
    | `scope-amount` | **thẳng vào `<input>`** (`V2BaseCurrencyInput` có `v-bind="$attrs"` trên input root) |
    | `scope-date` | **`<div>` wrapper** — E2E phải dùng `[data-testid="scope-date"] input` |
    → Đã sửa E2E ở plan Task 5.1: `.getByRole('textbox')` → `.locator('input')`.
  - Lệch brief có lý do chính đáng (implementer ghi rõ): dùng `V2BaseCurrencyInput` (helper tiền dùng chung, có sẵn ở nhiều màn `pages/assign`) thay vì tự viết `formatMoney` → **đúng luật CLAUDE.md "rà project trước, không tự phát minh"**. Bỏ nhánh `form.status` trong `disablePastDates` (không liên quan trường này). Thêm `danger: true` vào `$confirm` vì là thao tác xoá dữ liệu.
- **C15 — Dấu phân cách hàng nghìn: project TỰ MÂU THUẪN → hỏi user (không tự quyết).**
  Dữ kiện: `V2BaseCurrencyInput` (10 màn dùng) format bằng **phẩy** `1,500,000,000`; blade in sẵn có chia **12 chỗ phẩy / 10 chỗ chấm**; blade biên bản meeting chưa có `number_format` nào. Plan tôi viết dấu chấm → lệch màn hình.
  `CLAUDE.md` ghi rõ: "Phát hiện project đang có nhiều kiểu khác nhau cho cùng 1 thứ → nêu ra cho user chọn, KHÔNG tự chọn rồi làm tiếp." → đã hỏi.
  **User chốt (2026-08-21): DẤU PHẨY ở cả màn hình, bản In và Excel** — khớp ô nhập user vừa gõ.
  Đã đồng bộ: plan Task 4.1 blade `number_format($x, 0, ',', ',')`, plan Task 5.1 E2E assert `'1,500,000,000'`, plan T-12, spec mục 2 dòng 5 + mục 6.2 + mục 7.
- **C16 — Agent Task 3.1–3.3 chết 2 lần do MÁY SLEEP** (lỗi hạ tầng, không phải lỗi agent). Cả 2 lần code đều còn nguyên trong working tree (6 file, lint sạch) nhưng **chưa commit** và report chưa ghi.
  `Ruling: resume chính agent đó (context còn nguyên) thay vì dispatch agent mới; lần resume thứ 2 ĐỔI THỨ TỰ — bắt commit NGAY TRƯỚC khi làm bất cứ việc gì khác, rồi mới ghi report dần từng phần. — Vì dispatch mới sẽ mất toàn bộ kết quả verify đã chạy, còn commit trước thì lần đứt kế tiếp không mất code. — Nếu sai: commit vào khi report chưa đầy đủ, phải bổ sung bằng vòng fix.`
- Task 3.1–3.3: implementer DONE sau 2 lần resume (commit `e34067d`, 6 file, 159+/4-). Chạy đủ **10/10 ca** verify với output HTTP + SQL thật, không bỏ ca nào: ghi qua `store()` (meeting 43, created_by=1170), ghi qua `update()` (meeting 43, đổi scope 1→5), 4 ca lỗi validate, 2 ca regression 200, câu 1=Không xoá sạch dòng (meeting 44), cascade delete (meeting 45).
  - **C17 — Mã lỗi validate là 400, KHÔNG phải 422.** `app/Http/Requests/ApiBaseRequest::failedValidation()` override toàn app: trả `meta.code=400` + `data = $validator->errors()->toArray()`, HTTP 400. Spec/plan tôi viết 422 khắp nơi → sai.
    Đã truy tiếp để chắc chắn KHÔNG ảnh hưởng code FE: `pages/assign/meeting/_id/edit.vue:113-118` bắt đúng `status === 400` và đọc `error.response.data.data` — mà `data` là **mảng theo field** (`{field: ["msg"]}`), nên `formError[key][0]` trong component Task 3.4 **là đúng**, không phải bug.
    `Ruling: sửa tài liệu chứ không sửa code — thay 422→400 ở 11 chỗ trong plan và 8 chỗ trong spec. — Vì 400 là convention có sẵn toàn app, code đã đúng. — Nếu sai: E2E/test case ghi sai mã kỳ vọng, fail giả.`
  - Concern 3: route xoá meeting là `POST /{id}/delete` chứ không phải `DELETE /{id}` như brief ghi. Implementer dùng đúng route thật. Đã sửa trong plan.
  - Concern 2 (deferred, dọn ở Task 5.2): còn rác test trong DB dev — meeting id 43 (status 3, đã khoá, không xoá được qua API) và id 44 (status 2, còn 1 dòng `investment_demands`).
  - Task reviewer: dispatched (sonnet), có nhấn mạnh kiểm `store()` + thứ tự update-rồi-sync + rule `after_or_equal:today` phải vô điều kiện.
- Task 3.5: dispatched (sonnet), BASE hrm-client = `82c1bc7`. Cảnh báo riêng: `MeetingReport.vue` là **CRLF** còn `MeetingForm.vue` là **LF** — 2 kiểu khác nhau trong cùng 1 task.
- Task 3.1–3.3: task review → **Spec ✅ · Quality Approved**. Reviewer xác nhận điểm khó nhất đã làm đúng (`$request->only()` + `syncInvestmentDemands()` có ở CẢ `store()` :216-217/:242 lẫn `update()` :402-403/:437) và rule `after_or_equal:today` giữ vô điều kiện, KHÔNG copy nhầm pattern điều kiện của `expected_deadline`.
  - Reviewer **bác bỏ được nghi ngờ xoá nhầm** bằng cách đọc `vendor/prettus/l5-repository/BaseRepository.php:695-707`: `update()` làm `fill()`+`save()` rồi mới return → `$entity->has_investment_demand` đã là giá trị MỚI trước khi sync chạy. Cả 2 đường sync đều nằm trong transaction sẵn có.
  - **C18 — Important: `scope_id` không có `exists` → biên bản lưu được tên lĩnh vực bịa.** Client gọi thẳng API gửi `scope_id` không tồn tại + `scope_name` tự chế; service fallback dùng tên client gửi → snapshot vĩnh viễn trong chứng từ, và `scope_id` sau này còn dùng làm báo cáo tổng hợp.
    `Ruling: SỬA — thêm exists:mysql2.scopes,id. — Vì đây là dữ liệu chứng từ + khoá báo cáo, và fix chỉ là 1 rule. — Nếu sai: thêm 1 truy vấn exists mỗi lần lưu (không đáng kể, 13 bản ghi).`
  - **C19 — Important: thiếu `distinct` → gửi trùng lĩnh vực ra 500 kèm SQL thô.** Migration có `unique(meeting_id, scope_id)` nhưng rule không chặn trùng → vỡ ở `create()` lần 2 → `catch (\Exception)` → 500. Không nằm trong 10 ca đã chạy.
    `Ruling: SỬA — thêm distinct. — Vì 500 kèm SQL thô là lỗi lộ nội tại, và fix 1 từ khoá. — Nếu sai: không có rủi ro.`
  - **C20 — Important: `MeetingCreateApiRequest` không có rule khảo sát (và `status` đang bị comment).** Gọi thẳng `store()` với `status:3` sẽ bỏ qua yêu cầu bắt buộc.
    `Ruling: PARK — không sửa. — Vì reviewer đã xác nhận UI không có đường vào (nút "Hoàn thành" chỉ hiện khi status===2 nên luôn đi qua update()); và store() vốn ĐÃ bỏ qua cả guard điểm danh lẫn conclusion required_if — đây là lỗ hổng CÓ SẴN của store(), sửa cho riêng khảo sát là vá chắp vá và lấn sang hành vi cũ ngoài scope. — Nếu sai: API caller ngoài FE tạo được meeting status=3 thiếu đáp án khảo sát. GHI VÀO BÀN GIAO.`
  - Minor: `requiresInvestmentSurvey()` tạo ra nhưng không nơi nào gọi (dead code). `Ruling: giữ helper, cho blade Task 4.1 dùng nó thay vì lặp lại điều kiện — đã sửa plan + spec + brief 4.1.`
  - Minor (deferred): `position` có thể có khoảng hở khi item bị `continue`; vô hại vì `orderBy` giữ đúng thứ tự tương đối.
  - Fix round 1/5: resume implementer với C18 + C19.
- Task 3.1–3.3: fix round 1/5 (2 addressed, 0 open — C18 `exists:mysql2.scopes,id`, C19 `distinct`; commits `e34067d`..`16d2907`, 1 file +3/-1). Verify: scope_id=999999 → 400; 2 item trùng scope_id → 400 (không phải 500); 2 ca regression vẫn 200.
- Task 3.1–3.3: re-review có phạm vi → **F1/F2 ADDRESSED, không hỏng hóc mới**. Reviewer xác nhận rule nằm đúng trong nhánh `if ($needSurvey)`, tiền tố connection `mysql2` khớp `TpScope::$connection`, 2 message đúng key, và 2 rule `expected_deadline`/`expected_start_date` giữ nguyên.
- **Task 3.1–3.3: complete (commits `ba480fd`..`16d2907`, review clean sau 1 vòng fix)**
- Task 3.5: implementer DONE (commit `08cf2dfb`, 2 file, 41+/0-). Line ending giữ đúng cả 2 kiểu: `MeetingReport.vue` 100% CRLF (sửa bằng script byte-level `\r\n`), `MeetingForm.vue` 100% LF. Không lẫn kiểu nào.
  - Kết luận về payload: `MeetingForm::getFormData()` dựng bằng **spread `this.form`** → merge `buildPayload()` là dư về mặt kỹ thuật (watcher Task 3.4 đã ghi ngược 3 field vào `form` rồi), nhưng giữ theo ruling C3 và đã có comment tại chỗ nêu 2 mục đích. Merge đặt tại 1 điểm phễu duy nhất `getFormData()` → phủ mọi đường lưu. Hai chỗ `apiPostMethod` mà brief chỉ đến hoá ra là `change-status` và `delete` — không mang form data nên bỏ qua đúng.
  - **C21 — Concern implementer nêu: `removeNullAndUndefined()` ở `create.vue`/`edit.vue` có thể strip `has_investment_demand` khi `null`.** Controller tự truy `utils/helpers.js:32-39`: hàm chỉ xoá key có giá trị `null`/`undefined`, nông (top-level).
    `Ruling: KHÔNG phải lỗi, không hành động. — Vì (a) giá trị 0 = "trả lời Không" KHÔNG bị xoá (0 !== null) — đây mới là ca kích hoạt xoá dòng chi tiết, vẫn chạy đúng; (b) null = chưa trả lời bị xoá key thì BE thấy field VẮNG MẶT, mà required_if vẫn fail đúng khi status=3; (c) status != 3 thì cột không bị đụng nên giữ giá trị DB cũ, khớp spec E-5. — Nếu sai: một luồng nào đó gửi null có chủ ý sẽ không ghi được null đè lên giá trị cũ.`
  - Task reviewer: sắp dispatch
- Task 4.1: implementer DONE (commit `0307b86`, 1 file blade, +42/0). 3/3 ca verify có trích HTML thật:
  (1) meeting 44 câu 1 = Có → section 4 đủ `.1`/`.2`+bảng/`.3`, tiền `1,500,000,000` đúng dấu phẩy, ngày `15/03/2027`;
  (2) meeting 44 câu 1 = Không → chỉ `.1` và `.3`, không có `.2`;
  (3) meeting 43 loại khác → không render section khảo sát, "Kết luận cuộc họp" **vẫn là Section 4** ngay sau "Thành phần tham dự" (Section 3) → số KHÔNG nhảy cóc.
  - Brief tôi ghi sai 1 chỗ: `print_templates` code `BIEN_BAN_CUOC_HOP` **thực ra ĐÃ tồn tại** (count=1), không phải ca thiếu dữ liệu như tôi phỏng đoán từ memory. Implementer vẫn render qua tinker để verify, hợp lệ.
  - Ghi chú tên: bảng thật là `meeting_investment_demands`; `investment_demands` chỉ là tên relation.
  - **Rác test tăng thêm (dọn ở Task 5.2)**: implementer đã UPDATE/INSERT trực tiếp DB local trên meeting id 43 và 44 để dựng 3 ca. Cộng với rác từ Task 3.1–3.3 → danh sách cần dọn: meeting 43, 44, và mọi dòng `meeting_investment_demands` của chúng.
  - Task reviewer: dispatched (sonnet)
- Task 4.1: task review → **Spec ✅ · Quality Approved**, 0 Critical. Reviewer tự đọc file (không chỉ tin diff): `{{ $d->scope_name }}` auto-escape → an toàn XSS; `requiresInvestmentSurvey()` (`Meeting.php:256-260`) có short-circuit `$this->meeting_type &&` → an toàn khi meeting mồ côi loại; `@php $sectionNumber++ @endphp` (:297) nằm TRONG `@if` (đóng :298) → không nhảy số; `investment_demands` đã eager load ở `print()` → không N+1.
  - Important: rác fixture — meeting 44 đang ở trạng thái **nghịch lý** `has_investment_demand=0` nhưng vẫn còn dòng `meeting_investment_demands` id=9. Nguyên nhân: implementer set cờ bằng SQL UPDATE trực tiếp, **bỏ qua `syncInvestmentDemands()`** (nếu qua service thì dòng đã bị xoá). **Không phải bug code** — blade vẫn ẩn bảng đúng vì check `has_investment_demand`. → gộp vào danh sách dọn ở Task 5.2.
  - **C22 — Minor: `$d->expected_amount ? number_format(...) : ''` dùng truthy check → mức đầu tư = 0 sẽ IN RA RỖNG.** Rule cho phép `min:0` và `withValidator` coi 0 là đã điền (`=== null || === ''`), nên user lưu được 0 → màn hình hiện "0" còn bản in hiện trống.
    `Ruling: SỬA, nhưng KHÔNG mở fix round riêng — gộp vào dispatch Task 4.2 (cùng cặp "In & Excel"), đổi sang so sánh !== null ở blade; đồng thời viết brief 4.2 dùng !== null ngay từ đầu để Excel không lặp lại lỗi. — Vì để lệch nhau giữa In (trống) và Excel (0) còn tệ hơn, mà fix chỉ 1 toán tử. — Nếu sai: 1 dòng blade thay đổi ngoài phạm vi task gốc của nó.`
  - Minor (deferred): comment `<!-- Section ... -->` đặt ngoài `@if` nên luôn in ra kể cả meeting loại khác — vô hại (HTML comment), và đúng y code mẫu trong brief tôi đưa.
  - Minor (deferred, rủi ro CÓ SẴN toàn hệ thống): `fillReport()`/`clearNull()` (`app/Helper/FormatHelper.php:961-974`) chạy `preg_replace("/\{\{.*?\}\}/", "", $template)` trên toàn template → dữ liệu người dùng chứa `{{ }}` sẽ bị nuốt. Áp cho cả `conclusion`, tên file đính kèm… không phải lỗi mới của feature này. **GHI VÀO BÀN GIAO.**
  - ⚠️ reviewer nêu: report khẳng định render qua tinker "tương đương 100%" `/print` là hơi lạc quan vì chưa qua `fillReport()`/`clearNull()`. Controller ghi nhận — sẽ được phủ ở Phase 5 khi verify `/print` thật.
- **Task 4.1: complete (commit `0307b86`, review clean, 1 minor gộp sang 4.2)**
- Task 3.5: task review → **Spec ❌ · Needs work** (1 Critical). Fix round 1/5 đã dispatch.
- Task 3.5: fix round 1/5 (1 addressed, 0 open — C23 `needInvestmentSurvey` đọc field không tồn tại; commits `08cf2dfb`..`eab3431`, +12/-2).
  - **C23 — Critical (plan-mandated): `form.meeting_type_code` KHÔNG NƠI NÀO GÁN.** Reviewer grep toàn app: field chỉ xuất hiện đúng 1 chỗ ĐỌC (`MeetingReport.vue:422`), không có chỗ ghi. Hệ quả: màn Tạo mới `create.vue` không có key này → khối khảo sát **không bao giờ hiện** (đúng kịch bản nghiệm thu Bước 4); màn Sửa stale khi đổi dropdown. Lỗi thiết kế trong plan tôi viết.
    `Ruling: SỬA. — Vì feature không dùng được ở luồng tạo mới, và có sẵn khuôn đúng ngay trong cùng file (hasCustomer tính từ selectedMeetingType.code, bám form.meeting_type_id tức bám dropdown). — Nếu sai: thêm 1 prop truyền qua 2 tầng component.`
    Đã sửa **plan + spec** để không tái diễn.
  - Re-review: **F1 ADDRESSED, không hỏng hóc mới**. Reviewer kiểm đủ 3 mắt xích prop (computed `MeetingForm.vue:369` → truyền `:141` → khai prop `MeetingReport.vue:380-383`), guard `undefined → false`, import đã dọn khỏi `MeetingReport.vue`, line ending giữ đúng (MeetingForm 0 CR, MeetingReport 1118 CR = 100% CRLF), và không dòng nào còn dùng `form.meeting_type_code`.
- **Task 3.5: complete (commits `82c1bc7`..`eab3431`, review clean sau 1 vòng fix)**
- **=== PHASE 3 HOÀN TẤT === (hrm-api `16d2907`, hrm-client `eab3431`)**
- Task 4.2: dispatched (sonnet). BASE hrm-client = `eab3431`, BASE hrm-api = `0307b86` (task này đụng CẢ 2 repo do gộp fix C22).
- Task 4.2: implementer DONE — **2 commit** (hrm-client `9e16d63` +69/0; hrm-api `dc56043` +1/-1). Ca `expected_amount = 0` verify qua tinker: render ra `<td>0</td>` thay vì trống, đồng thời `1500000000` vẫn ra `1,500,000,000`. Dữ liệu test DB đã dọn và verify về nguyên trạng.
  - **Ghi nhận cách làm tốt**: implementer dính đúng bẫy CRLF — tool `Edit` ghi **literal 2 ký tự `\r`** thay vì byte CR thật; tự phát hiện qua `git diff` bất thường, `git checkout` hoàn tác ngay, làm lại bằng Python `newline=''`, rồi verify `od -c` + `grep -c $'\r' == wc -l` (1187 = 1187). Không commit nào chứa bản lỗi.
    → **Bài học cho các task FE còn lại**: với file CRLF, KHÔNG dùng tool Edit cho khối nhiều dòng; dùng script Python `newline=''`.
  - Task reviewer: dispatched (sonnet), package gộp diff cả 2 repo.
- Task 4.2: task review → **Spec ✅ PASS · Quality Approved**, 0 Critical/Important. Reviewer trace trọn `rowCursor` qua mọi nhánh của `exportMeetingExcel()` (dòng 476-790) — không lệch; `sectionNumber++` chỉ trong nhánh `if` nên "KẾT LUẬN" không nhảy số ở cả 2 trường hợp; merge cell không chồng lấn; `safeText` chặn đúng 4 ca `=`/`+`/`-`/`@` và an toàn với null.
  - Reviewer xác nhận độc lập: `this.$dayjs` **không tồn tại** trong project → implementer đã tự phát hiện và sửa đúng sang `import dayjs` (đã có trong `package.json`). Line ending verify độc lập: `wc -l` 1187 == số dòng có `\r` 1187, và grep literal `\r` (2 ký tự) ra rỗng → sự cố Edit tool đã khắc phục triệt để.
  - Minor (deferred): dòng câu 1/câu 3 không `mergeCells` giá trị qua nhiều cột như `infoRows`; `expected_amount` không qua `safeText` (an toàn vì `buildPayload().toNumber()` luôn trả số hoặc null).
  - ⚠️ (deferred sang Phase 5): chưa bấm nút Excel thật để mở file .xlsx kiểm layout / `=SUM()` / ca `=1+1`.
- **Task 4.2: complete (hrm-client `9e16d63`, hrm-api `dc56043`, review clean)**
- **=== PHASE 4 HOÀN TẤT ===**
- **Môi trường Phase 5 (controller tự kiểm)**: FE Nuxt **đã chạy sẵn** ở `127.0.0.1:3000` (200), API Laravel **đã chạy sẵn** ở `127.0.0.1:8000` (`php -S`, login trả `access_token`). `node_modules` cả hrm-client lẫn e2e, `.nuxt` cache, Playwright chromium: đủ. Node 20.20.1 có sẵn cho E2E (Node 14 KHÔNG có).
- Task 5.1: dispatched (sonnet). Dặn tránh meeting id 43/44 (fixture rác), tự tạo meeting sạch và ghi id để dọn sau.
- Task 5.1: agent chạy được E2E nhưng **dừng giữa chừng chưa ghi report** (kết thúc bằng "chờ Monitor"). Đã viết `e2e/tests/assign/meeting-investment-survey.spec.ts`, dựng meeting **46** (loại 7) + **47** (loại 2), ghi vào `e2e/.env`. Kết quả: **1/6 PASS** — chỉ ca 1 (danh mục khoá thao tác, thuần server-rendered list) pass; 5 ca còn lại fail.
- **C24 — 5 ca E2E fail do MÔI TRƯỜNG CŨ, không phải app sai.** Controller tự chẩn đoán:
  - Dev server Nuxt (pid 90421) khởi động **19:21**; `.nuxt` build gần nhất **20:02**; `find .nuxt -newermt "21:00"` → **0 file**.
  - 3 commit FE thực sự dựng khối khảo sát landed **21:47** (`08cf2dfb` nhúng vào tab), **21:58** (`eab3431` fix điều kiện hiện), **22:10** (`9e16d63` Excel).
  → Server đã ngừng rebuild, đang phục vụ code từ TRƯỚC khi `MeetingReport.vue` được nối với component. Ca 2 ("khối chỉ hiện với đúng loại meeting") fail kéo theo mọi ca sau — đúng triệu chứng.
  `Ruling: HỎI USER trước khi kill tiến trình của họ (không tự quyết) — user chốt "để em kill và khởi động lại". Đã kill 90421/90423/59108, xoá .nuxt/components (gotcha stale components manifest đã biết), khởi động lại bằng Node 12 + NODE_OPTIONS=--max-old-space-size=8192. — Vì đây là tiến trình trên máy user, và memory ghi rõ client Nuxt dễ OOM nên restart có rủi ro thật. — Nếu sai: build OOM, user tạm thời không có dev server.`
- Task 5.1 vòng 1: sau restart server, fail giảm **5 → 2** (tức 4/6 PASS). Xác nhận chẩn đoán C24 đúng: 3 trong 5 ca fail lần đầu là do bundle cũ.
  - Còn fail: ca 2 "Khối khảo sát chỉ hiện với đúng loại meeting", ca 3 "Câu 2 hiện/ẩn theo câu 1, đủ 13 lĩnh vực". Đáng chú ý ca 4 (checkbox+format) và ca 6 (lưu rồi mở lại) **đã PASS** — 2 ca này đòi khối phải hiện và có dòng lĩnh vực → khối CÓ render, vấn đề nằm chỗ khác.
- **C25 — Agent Task 5.1 kẹt vòng lặp chờ Monitor 2 lần liên tiếp**, tiêu 217k token / 119 tool call mà không bao giờ trả được kết quả (câu kết cả 2 lần đều là "chờ Monitor").
  `Ruling: KHÔNG resume lần 3 — dispatch agent MỚI, giữ nguyên tier model, nhưng CẤM tuyệt đối tool Monitor / run_in_background / vòng lặp chờ; bắt chạy playwright ở foreground với timeout tool 600s và ghi report dần từng phần. — Vì thất bại không phải do năng lực suy luận mà do pattern dùng tool; resume lại cùng agent chỉ lặp lại pattern đó. — Nếu sai: mất context điều tra của agent cũ (đã giảm thiểu bằng cách trỏ agent mới đọc report cũ, trong đó có đủ phát hiện quan trọng).`
- **C26 — Agent 5.1 phát hiện 1 LỖI APP CÓ SẴN, ngoài phạm vi feature.**
  `MeetingForm.vue::initializeCompanyMembers()` (~dòng 987, code có TRƯỚC feature này) đọc `currentEmployee.info.work_position.name` **không null-guard**. User nào chưa có `employee_work_position_id` → `info.work_position` là null → `TypeError: Cannot read properties of null (reading 'name')` ngay lúc mount → **crash toàn bộ cây component**, Nuxt đá sang trang "Không tìm thấy trang yêu cầu". Không mở được màn Sửa meeting.
  `Ruling: KHÔNG sửa (ngoài phạm vi feature). Agent lách bằng cách set employee_work_position_id=17 cho employee 1170 trong DB — coi như dựng fixture. — Vì sửa hàm này đụng luồng chung của mọi meeting, phải hỏi user trước theo CLAUDE.md. — Nếu sai: user thật nào thiếu work_position sẽ không mở được màn Sửa meeting. **GHI VÀO BÀN GIAO — đây là bug đáng báo cho team.**`
  Rác fixture thêm: `employees.employee_work_position_id` của id 1170 đã bị đổi → ghi vào danh sách dọn/bàn giao.
- Task 5.1 vòng 2: dispatched agent MỚI (sonnet), cấm Monitor.
- Task 5.1 vòng 2 (agent mới): giải quyết được **cả 2 ca fail còn lại**, nhưng agent chết vì máy sleep trước khi chạy gộp chốt 6/6.
  - **Ca 2 — nguyên nhân là LỖI DỮ LIỆU FIXTURE, không phải app sai.** Agent đọc thẳng Vue instance trong browser: API trả đúng `meeting_type_id: 7` nhưng `form.meeting_type_id` trong Vue là **chuỗi rỗng**. Truy ra `GeneralInfo.vue:~891` có watcher `meetingScope` tự xoá `form.meeting_type_id = ''` khi `is_customer_meeting` của bản ghi lệch với `has_customer` của loại meeting. Meeting 46 do script seed dựng bị lệch 2 field này. Sửa fixture (`is_customer_meeting=1`) → **PASS**. Không đụng app, không đụng file test.
  - **Ca 3 — PASS** sau khi sửa fixture ca 2 (cùng nguyên nhân gốc). `toHaveCount(13)` đúng.
  - **⚠️ Đính chính của controller**: report ghi "13 bản ghi trên connection mặc định `hrm_erp`" là **quy kết sai**. Danh mục lĩnh vực đọc qua `TpScope` connection **`mysql2` → `erp2326`**, không phụ thuộc `DB_DATABASE`. Trên `hrm_erp` cả 2 bảng đều 13 dòng nên test không phân biệt được. **Sau khi user đổi sang `hrm_tpe` (scopes = 22 dòng HRM), ca `toHaveCount(13)` trở thành phép thử PHÂN BIỆT thật sự cho ruling C12** — vẫn ra 13 nghĩa là code đọc đúng `erp2326`, ra 22 nghĩa là đọc nhầm connection mặc định. **Phải chạy lại ca này sau khi đổi DB.**
  - **[Bàn giao] Phát hiện thêm về app**: watcher `meetingScope` xoá `meeting_type_id` **hoàn toàn im lặng** (không log, không toast). Bản ghi production nào lệch `is_customer_meeting` vs `has_customer` (do migrate/import cũ) sẽ tự mất "Loại meeting" khi mở màn Sửa mà không cảnh báo gì.
- **C27 — MÔI TRƯỜNG SAI DB SUỐT QUÁ TRÌNH.** User báo lỗi `Unknown column 'scopes.code'` ở màn Tạo meeting. Controller chẩn đoán:
  - `.env` trỏ `DB_DATABASE=hrm_erp` = **DB đã gộp, dành cho nhánh `gop_db`**; trong đó `scopes` là bảng của ERP (không có `code`), bản HRM đã đổi tên thành `hrm_scopes`. Đúng gotcha `CLAUDE.md` mục gộp DB.
  - Nhánh đang đứng là `meeting-by-market` (hậu duệ `tpe`) → DB đúng là **`hrm_tpe`**, ở đó `scopes` CÓ `code`.
  - Code gây lỗi sửa lần cuối **2026-06-25**, trước feature 2 tháng → **KHÔNG do feature này**.
  - Hệ quả: 3 migration + seeder chỉ chạy trên `hrm_erp` (hrm_tpe = 0); **toàn bộ verify BE + E2E đều chạy trên DB không khớp nhánh**.
  `Ruling: KHÔNG tự đổi .env, KHÔNG tự chạy migration — hỏi user. User tự sửa .env sang hrm_tpe. Sau đó phát hiện hrm_tpe thiếu 19 migration (16 của feature khác) → hỏi tiếp, user chốt "anh tự chạy, em không đụng DB". — Vì đổi DB/chạy 16 migration của người khác là tác động lớn lên môi trường user. — Nếu sai: chậm tiến độ, đổi lại là mọi verify phải chạy lại.`
  - Ghi chú: `config:cache` **không dùng được** cho project này (`config/ckfinder.php` chứa Closure) — chỉ dùng `config:clear`. Lệnh fail tự xoá `bootstrap/cache/config.php` nên kết cục vẫn đúng.
- Final whole-branch review: dispatched (**opus**), package gộp diff cả 2 repo (hrm-api 17 file/+460, hrm-client 6 file/+515), kèm 7 mục hoãn để triage.

## Final whole-branch review (opus) — 2026-08-22

Verdict: **Cần sửa trước khi merge** (3 Important). Bảo mật + hiệu năng sạch (XSS, formula injection, SQL injection, fail-open quyền, N+1, route order đều đã kiểm).

- **C28 — Important: FormData không phân biệt "mảng rỗng" vs "không gửi field" → bỏ tích hết lĩnh vực mà giữ câu 1 = Có thì dữ liệu cũ SỐNG LẠI.** `Object.keys([])` = `[]` nên FE không append key nào; `syncInvestmentDemands` rơi vào `!is_array` → return → dòng cũ còn nguyên, toast báo thành công. **Sai im lặng trên chứng từ.** Comment trong code của tôi mô tả một ngữ nghĩa mà transport không cung cấp.
  `Ruling: SỬA — coi non-array là mảng rỗng, đặt SAU guard has_investment_demand !== 1. — Vì đây là mất dữ liệu im lặng trên chứng từ, và fix 3 dòng. — Nếu sai: luồng nào cố tình không gửi field để giữ dữ liệu cũ sẽ bị xoá; đã rà không có luồng nào như vậy (changeStatus không gọi sync).`
- **C29 — Important: lỗi `investment_demands.*.scope_id` không render được ở FE → ngõ cụt.** ERP xoá lĩnh vực đang chọn → BE trả 400 key `scope_id` → FE không hiện gì, user chỉ thấy toast chung, không biết bỏ tích dòng nào. Mâu thuẫn thiết kế do tôi tạo: `scope_name` snapshot sinh ra để biên bản cũ vẫn đúng, nhưng rule `exists` lại chặn chính bản ghi đó lưu lại.
  `Ruling: SỬA phía FE (render errorFor(i,'scope_id')), KHÔNG nới rule exists. — Vì giữ toàn vẹn dữ liệu quan trọng hơn, và spec E-2 vốn nói "cho bỏ tích nhưng không cho tích lại" — chỉ cần user THẤY được lỗi là đủ. — Nếu sai: user phải bỏ tích thủ công thay vì hệ thống tự bỏ.`
- **C30 — Important: tiền đề spec §6.8 SAI — màn meeting KHÔNG dùng `unsavedChangesMixin`.** `create.vue`/`edit.vue` chỉ có `PageTitleMixin`; `MeetingForm` không khai mixin nào. Watcher ghi ngược `form` mà tôi bắt làm ở Task 3.4 **không có ai tiêu thụ**; T-20 không bao giờ đạt.
  `Ruling: sửa COMMENT cho đúng sự thật + chuyển T-20 ra ngoài scope; GIỮ watcher (làm form thành nguồn duy nhất, sẵn sàng nếu sau này gắn mixin); KHÔNG gắn mixin. — Vì gắn mixin đổi hành vi toàn bộ form meeting, ngoài phạm vi, và CLAUDE.md bắt hỏi trước khi đụng luồng dùng chung. — Nếu sai: màn meeting tiếp tục không cảnh báo thoát-chưa-lưu. GHI VÀO BÀN GIAO.`
- **C31 — Reviewer BÁC lý do park C20 của tôi.** Tôi park `MeetingCreateApiRequest` với lập luận "`store()` vốn đã bỏ qua `conclusion`" — **sai**, file đó CÓ `conclusion => required_if:status,3` (dòng 57). Nguy hại thật: `store()` gọi `syncInvestmentDemands()` với mảng **không validate gì** → trùng `scope_id` vi phạm unique → **500 kèm SQL thô lộ ra client**.
  `Ruling: SỬA — copy 4 rule investment_demands.* sang Create request. Vế required_if cho has_*_demand vẫn hoãn (tạo mới không đi qua nút Hoàn thành). — Vì 500 lộ SQL là lỗi thật, fix 4 dòng. — Nếu sai: thừa validate ở luồng tạo mới, vô hại.`
- Triage 7 mục hoãn: **6 CHẤP NHẬN, 1 PHẢI SỬA** (mục 2 = C31). Reviewer bác thêm tiền đề mục 4 của tôi: PHP 7.4 cast array→int **không** phát E_WARNING (chỉ array→string mới có) → hậu quả tối đa là trả thừa 1 lĩnh vực id=1, và code giống hệt `MeetingTypeController::getAll()` đang chạy production.
- Minor mới ghi nhận (deferred): cast `date` làm `expected_start_date` serialize ra ISO trong khi `expected_deadline` ra `YYYY-MM-DD` (đã verify không hỏng); `scopeLoadFailed` báo nhầm khi ERP có 0 lĩnh vực active; `getInvestmentScopes` getter không ai đọc; nhánh fallback `scope_name` là dead code sau khi có `exists`.
- **Minor CÓ SẴN, không do nhánh này — GHI BÀN GIAO**: `MeetingController::changeStatus()` nhận `status` tuỳ ý **không validate gì** → POST `status=3` hoàn thành meeting bỏ qua cả `conclusion` lẫn khảo sát (BR-4 không phải chốt chặn tuyệt đối ở tầng API). `MeetingController::print()` **không có `canView()`** trong khi `show()` có — mà bản in nay mang thêm **mức đầu tư dự kiến của khách hàng**, dữ liệu thương mại nhạy cảm.

## Đợt fix cuối + re-review — 2026-08-22

- Fix wave: hrm-api `fa723d0`, hrm-client `38f7e60`. Làm FIX 1/2/3/4/6; **bỏ FIX 5** (eager load `show()`) vì `getDataForShow()` vốn không `->load()` quan hệ nào — reviewer tự kiểm và **xác nhận lý do đúng**.
- Re-review có phạm vi: **5/5 ADDRESSED, 0 hỏng hóc mới**. Đã kiểm riêng điểm rủi ro nhất (implementer đổi cách gán `$meetingType` trong `MeetingCreateApiRequest` — file chạy cho MỌI lần tạo meeting): `$hasCustomer` giữ đúng default `true`, không có undefined variable. Line ending: 2 file LF không lẫn CR; 2 file CRLF không bị đụng.
- **VÒNG REVIEW ĐÃ ĐÓNG. Code sẵn sàng merge.**

## Còn lại (chặn bởi môi trường, không phải code)

1. USER chạy seeder trên `hrm_tpe` (DB mới có 6 loại meeting, thiếu bản ghi hệ thống)
2. Chạy lại E2E trên DB đúng — ưu tiên ca "đủ 13 lĩnh vực" (phép thử phân biệt C12)
3. Chạy 19 test case nghiệm thu (T-20 đã ngoài scope)
4. Dọn fixture rác: meeting **43, 44, 46, 47** + dòng `meeting_investment_demands` của chúng (ở `hrm_erp`); `employees.employee_work_position_id` của id **1170** đã bị đổi thành 17

## Bổ sung UI tab Biên bản — 2026-08-22 (yêu cầu mới của user)

Yêu cầu: bố cục I/II/III · bảng có border · tiêu đề cột bỏ IN HOA · giảm khoảng cách thanh trạng thái ↔ thanh tab.

3 điểm user chốt khi brainstorm: (1) **chỉ đánh số khi có cả hai** — loại meeting thường giữ nguyên, không số, không tiêu đề bao; (2) **Kết luận tách ra III/**, II/ gồm bảng nội dung + tài liệu; (3) border cho **cả 3 bảng**; (4) khoảng cách `mb-1` (user sửa từ đề xuất `mb-2`).

- **C32 — Phát hiện khi rà: `MeetingInvestmentSurvey.vue` KHÔNG có khối `<style>` nào.** Nó dùng `.header-row`/`.sec-title` định nghĩa trong `MeetingReport.vue` mà style đó là **`scoped`** — scoped CSS **không áp xuống component con** → bảng khảo sát từ lúc ship tới giờ **không có style gì cả**. Đây là defect thẩm mỹ có thật của phần chúng tôi vừa làm, chỉ lộ ra khi user yêu cầu chỉnh giao diện.
  `Ruling: thêm <style scoped> riêng cho MeetingInvestmentSurvey, CHÉP định nghĩa 3 class từ MeetingReport (kèm comment nêu lý do lặp). — Vì scoped CSS không chia sẻ được, và tách ra file CSS chung là refactor ngoài phạm vi. — Nếu sai: 2 chỗ định nghĩa CSS phải sửa song song khi đổi style sau này.`
- **C33 — Làm border bằng CSS thay vì chuyển DOM sang `<table>`.**
  `Ruling: giữ nguyên lưới div.row/div.col-*, chỉ thêm class .tbl-bordered. — Vì 3 bảng này chứa input/datepicker/nút; chuyển sang <table> thật là refactor lớn, dễ vỡ căn cột và responsive, trong khi kết quả nhìn giống nhau. — Nếu sai: về sau muốn dùng tính năng của <table> (colspan động, sticky header) sẽ phải làm lại.`
- Commit hrm-client `d596f8e` (3 file, 361+/250-). Review: **Spec ✅ 5/5 · Approved**, 0 Critical/Important.
  Reviewer kiểm đúng 3 rủi ro của việc di chuyển khối: `ref="investmentSurvey"` còn nguyên (Excel vẫn gọi được `buildPayload()`); số `<hr>` = 3 (có khảo sát) / 2 (không) khớp bản gốc; computed prefix trả `''` không phải `undefined`; thẻ div cân bằng 58/58 và 24/24; line ending `MeetingReport.vue` CRLF 1240/1240, 2 file kia LF thuần.
  Minor (deferred): thứ tự khai báo class trong 2 khối `<style>` khác nhau — không ảnh hưởng.
- ⚠️ **Chưa xem bằng mắt trên trình duyệt** (máy không chạy được `npm run dev` từ agent). Đây là thay đổi thuần CSS/bố cục nên **bắt buộc user build FE và nhìn thật** — không có cách verify tự động thay thế.

## Tái cấu trúc bố cục I–V — 2026-08-22 (yêu cầu mới, THAY THẾ bố cục I/II/III của commit d596f8e)

- User chốt: 3 mục cũ chưa được nhắc (Dự án · Giai đoạn dự án · Mục tiêu cuộc họp) **đưa hết vào I/ Thông tin cuộc họp**; màn hình hiện tiêu đề mục + dòng xám "Phần mềm thêm tự động khi in" cho I/II/III.
- Commit: hrm-api `bd7ffc9` (blade, 183+/179-) · hrm-client `3abfe29` (MeetingReport, 59+/18-). Trước đó: `fc9719e` căn nhãn 175px, `d3c4ce0` cỡ chữ tiêu đề bản in.
- **Controller tự verify (không chỉ tin report)**: render tinker cả 2 ca → meeting 40 (không khảo sát) ra `I II III IV V` + IV có `1/ Các nội dung khác`, `2/ Tài liệu đính kèm`; meeting 43 (có khảo sát) ra `I II III IV` + `1/ Khảo sát`. So `$var->prop` trước/sau: **không mất biến nào**, chỉ thêm `$meeting->name`. Ba nhãn tiếng Anh (`Meeting place:` `Project:` `Project type:`) không mất mà được gộp vào nhãn tiếng Việt trong ngoặc.
- **C34 — `$meeting->name` chưa từng được in ra trong bản in biên bản** (grep = 0 lần trước khi sửa). Phát hiện khi rà để dựng mục I.
- **C35 — Nguyên nhân "lệch bảng Thời gian" đo được bằng trình duyệt, không đoán**: nhãn "Hình thức họp (Meeting type):" rộng **169.6px** vượt `min-width: 120px` → giá trị thụt ra **49.6px** so với dòng trên trong cùng cột; cột Thời gian cả 2 nhãn đều vừa 120px nên thẳng, làm càng lộ lệch. Nâng cả 6 nhãn lên 175px → offset đồng nhất 179.1/179.1 và 198.3/198.3 (chênh 19.2px giữa 2 cột là `padding-left:20px` tạo khoảng thở, không phải lệch).
- **C36 — Cỡ chữ tiêu đề bản in**: cả 2 `<h3>` đều 18.72px bold (mặc định trình duyệt) trong khi body 13px. Sửa bằng **CSS ở `print.vue`** chứ không sửa bản ghi `print_templates`.
  `Ruling: sửa bằng CSS (code) thay vì sửa template (data). — Vì template là dữ liệu, sửa phải làm lại ở mọi môi trường và dễ bị ghi đè; CSS đi theo deploy. — Nếu sai: nếu team sau này sửa template qua màn quản lý mẫu in, CSS này vẫn đè lên cỡ chữ họ đặt.`
- ⚠️ Agent tự thêm **icon Remix trang trí** cho tiêu đề I/II/III/IV — **không nằm trong yêu cầu**. Đã ghi nhận để user quyết giữ hay bỏ.
- ⚠️ **Chưa xem màn hình bằng mắt** — cần build FE. Bản in đã verify bằng render thật.

## Tinh chỉnh cuối — 2026-08-22

- Commit: hrm-api `59e0990` (giảm khoảng cách bản in) · hrm-client `edbf20f` (gộp ghi chú vào tiêu đề + giảm khoảng cách).
- **C37 — User hủy yêu cầu "bỏ III trong mục V" giữa chừng.** Tôi đã chẩn đoán ra `"III. KẾT LUẬN CHUNG CỦA CUỘC HỌP"` là **dữ liệu người dùng tự gõ** (3/16 bản ghi), và đề xuất lọc ở tầng render blade với điều kiện hẹp. User quyết: *"nếu là data tự gõ thì ko liên quan cấu trúc → bỏ qua"*.
  `Ruling: HỦY, gỡ sạch phần lọc nếu đã viết. Verify NGƯỢC LẠI — phải chứng minh conclusion render NGUYÊN VĂN. — Vì user là chủ dữ liệu và quyết định đúng: cắt chữ ở tầng render là "phép thuật" khó đoán cho người đọc code sau, và có nguy cơ xoá nhầm nội dung thật. — Nếu sai: bản in của 3 bản ghi cũ có dòng tiêu đề thừa; sửa được bằng cách sửa dữ liệu.`
- ⚠️ **Việc làm CHƯA trọn** (agent tự nêu): trên màn hình mới giảm `mb-3`→`mb-2` cho 3 header I/II/III, **các mục IV/V và mục con vẫn giữ `mb-3`**. Bản in mới đổi 2 giá trị (`20px→10px`, `10px→4px`), còn `15px` (khung bảng) và `8px` (khối khảo sát) giữ nguyên. Nếu user muốn "giảm tối đa" đồng loạt thì cần một lượt nữa.
- ⚠️ **Chưa xem màn hình sau lần chỉnh này** — ảnh chụp Playwright là của bản TRƯỚC khi giảm khoảng cách.
