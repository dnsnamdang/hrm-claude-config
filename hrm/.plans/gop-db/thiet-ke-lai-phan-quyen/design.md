# Thiết kế lại màn Quản lý phân quyền HRM

> Tóm tắt. Spec chi tiết: `docs/superpowers/specs/gop-db/2026-08-14-thiet-ke-lai-phan-quyen-design.md`
> Nhánh: `gop_db` (cả hrm-api + hrm-client).

## Mục tiêu

Thiết kế lại màn quản lý phân quyền, đưa về phân hệ **"Quản trị hệ thống"** (`admin`, type 10 — đã khai sẵn ở `subsystems.js` nhưng menu còn placeholder). Giải quyết 4 pain hiện tại:
- Quá nhiều quyền (617 permission, phần lớn là "xem theo cấp" nở ra nhiều dòng).
- Giao diện xấu (cây checkbox 3 tầng, không rõ ràng).
- Không có tìm kiếm quyền.
- Không có nhóm/gom quyền tốt.

## Phân rã theo phase

- **Phase 1 (đang làm) — UI, KHÔNG đụng DB/BE cốt lõi.** Thiết kế lại 2 màn (danh sách chức vụ + form phân quyền), đưa vào menu Quản trị hệ thống. Giữ nguyên schema (`role_has_permissions.company_id`, spatie, seeder). FE chỉ gửi `permission_ids` cho **1 công ty** (của người đăng nhập) thay vì mảng nhiều công ty.
- **Phase 2 (sau) — BE.** Chuẩn hóa 617 permission thành (tài nguyên × hành động), tách module `Administration` riêng, thêm bảng danh mục nhóm quyền. Cần migration → tính riêng, chưa làm.

## Hiện trạng (2026-08-14)

**Đã xong: MOCKUP tương tác hoàn chỉnh** trong bộ demo kế toán (không phải code hrm-client thật), verify bằng Playwright:
- `.plans/demo-man-hinh-ke-toan/demo/phan-quyen.html`
- `.plans/demo-man-hinh-ke-toan/demo/assets/permissions.js` (toàn bộ logic 2 màn)
- `assets/app.js` (thêm menu "Quản trị hệ thống → Phân quyền"), `index.html` (thêm card)

Chưa port vào `hrm-client` thật — đó là việc của phần "IMPLEMENT" trong plan.

## Các quyết định thiết kế chốt qua brainstorming

1. **Phân quyền theo ngữ cảnh 1 công ty.** Bỏ cơ chế 1 form hiển thị tab nhiều công ty. Mỗi chức vụ vẫn có thể có quyền ở nhiều công ty, nhưng người quản trị **chỉ phân cho công ty của mình** (cố định theo user, không cho chọn).
2. **Mô hình quyền = Loại × Phạm vi:**
   - **Xem** và **Duyệt** → có **Phạm vi** = chọn 1 cấp trong `Tổng công ty → Công ty → Phòng ban → Bộ phận` (thứ tự trái→phải), **cấp cao bao hàm cấp thấp**. Duyệt **mặc định Công ty**. Mỗi chức năng chỉ hiện các cấp nó hỗ trợ.
   - **Thao tác** (Thêm mới, Sửa, Xóa, Quản lý…) → chỉ **bật/tắt**, không phạm vi.
   - Trong 1 nhóm, xếp theo loại: **Xem → Thao tác → Duyệt**.
3. **Layout form phân quyền:** phân hệ = **card (accordion)** → các chức năng bên trong = **bảng** (`Loại | Tên quyền | Phạm vi`). Phạm vi dùng **select** (gọn); Thao tác dùng **checkbox** — đều canh phải cột Phạm vi.
4. **Bộ lọc phân tầng 1 hàng:** Nhóm phân hệ → Phân hệ → Chức năng (đổ dây) + **Loại quyền** (Xem/Thao tác/Duyệt) + tìm nhanh.
5. **Panel "Quyền đã phân" (tỷ lệ 8:4, bên phải):** header chỉ "N quyền đã phân"; **chip tổng hợp số quyền theo phân hệ**; danh sách gom theo Phân hệ → Nhóm với badge cấp/loại. Nút **Lưu phân quyền** đặt ở **cuối form** (footer).
6. **Màn danh sách chức vụ:** bảng chuẩn, cột **"Quyền đang có"** là nút bấm → **popup** liệt kê quyền đang có (có bộ lọc Phân hệ/Chức năng/Loại + chip tổng hợp theo phân hệ). Giữ: Phân quyền hàng loạt, Lịch sử thay đổi, Xuất Excel.

## Ảnh hưởng BE (Phase 1)

- Giữ nguyên: bảng `roles`, `permissions` (cột `type` + `group`), pivot `role_has_permissions(company_id)`, `company_roles`, `RoleController`, `PermissionController`, `Role::syncPermissionsByCompany`.
- Điều chỉnh nhỏ: `store` chỉ nhận/ghi `permissions` cho **1 company_id** (của user), thay vì mảng nhiều công ty. Cần xác nhận cách xác định "công ty của user" (từ `DEFAULT_USER`/token).
- Gate dữ liệu nhạy cảm giữ nguyên nguyên tắc fail-closed (không hard-code cờ quyền `= true`).

## Rủi ro / cần làm rõ trước khi implement thật

- Cách map `display_name` → loại (Xem/Thao tác/Duyệt) và các cấp phạm vi trên **dữ liệu thật 617 permission** (mockup đang mô hình hóa sạch cho phân hệ Chấm công). Dữ liệu thật có nhiều bản "bare"/"theo công ty" trùng lặp → cần metadata hoặc quy ước parse tên. Đây là ranh giới dễ trượt sang Phase 2.
- "Công ty của user" khi phân quyền: 1 hay nhiều? Nếu user thuộc nhiều công ty thì UX chọn thế nào (hiện mockup cố định 1).
- Quyền "Phân ca theo cấp" (action có hậu tố cấp) — theo quy ước "chỉ Xem/Duyệt có phạm vi" thì các action-theo-cấp này cần được xử lý/gộp ở Phase 2.

## Quyết định đã chốt — Mở rộng sang CẢ HAI HỆ (2026-09-02)

User chốt: màn này quản lý quyền cho **cả HRM lẫn ERP** — DB đã gộp nên dùng chung một màn. Kèm
bối cảnh: một số chức năng ERP đã chuyển dần sang HRM, quyền cũng chuyển theo nhưng mang
`guard = api` (code HRM là API/client, không còn Blade). Giai đoạn đầu **chấp nhận một chức năng
có source ở hai bên và hai bản ghi quyền khác guard**.

### Số đo trên DB gộp `hrm_erp` (sau khi chạy lại `PermissionsTableSeeder` ngày 2026-09-02)

| | HRM (`guard = api`) | ERP (`guard = web`) |
|---|---|---|
| Quyền | **722** | **965** |
| Phân hệ | cột `type` (78 dòng `NULL` = Chấm công) | `type` NULL toàn bộ → dùng `group_category` (7 giá trị) |
| Nhóm (`group`) | 151 | 137 |
| Chức vụ (`roles`) | 45 | 75 |

Hai tập chức vụ **tách biệt**: tên khác hẳn nhau (chỉ trùng đúng `Super admin`), và trong
`role_has_permissions` không có một dòng nào gán chéo guard. Nhân viên nhận role từ cùng bảng
`employee_has_roles` (425 dòng trỏ role HRM + 1.252 dòng trỏ role ERP) — một người đeo song song
chức vụ của cả hai hệ.

### 4 quyết định

1. **Danh sách chức vụ gộp, form theo đúng hệ.** Màn danh sách bày cả 120 chức vụ, thêm cột `Hệ`
   (HRM/ERP) + bộ lọc. Mở chức vụ HRM thì ma trận nạp 722 quyền HRM, mở chức vụ ERP thì nạp 965
   quyền ERP. **Không** cho một chức vụ giữ quyền của cả hai hệ: HRM kiểm quyền bằng
   `isCurrentEmployeeHasPermission()` join thẳng `role_has_permissions` (KHÔNG lọc guard) còn ERP
   dùng `can()` của spatie (CÓ lọc guard) ⇒ quyền `web` gán vào role `api` sẽ ăn bên HRM nhưng
   **câm bên ERP**, người phân quyền tưởng đã cấp mà thực tế không. BE chặn lại bằng validate,
   trả lỗi thay vì im lặng.

2. **Phân hệ của quyền ERP = `group_category` map về registry.**
   `Danh mục`→9 · `Kinh doanh`→23 (Bán hàng) · `Kho`→21 · `Kế toán`→25 · `Mua hàng`→20 ·
   `CSKH`→24 · `Cấu hình hệ thống`→10. Nhờ vậy hai hệ dùng chung một bộ dải phân hệ và một bộ màu.
   Giá trị lạ → `type = 0`, FE dựng dải "Chưa phân loại phân hệ" thay vì xếp bừa.

3. **`approve_scope` khoá theo permission ID.** Thêm `hrm-api/config/permission_scopes.php`, chép
   17 quyền đã khai trong `ERP/TanPhatDev/config/approval_inbox.php` — tra ra **20 bản ghi** trong
   DB gộp, vì 3 chức năng đã chuyển sang HRM nên tồn tại hai bản khác guard:
   `Duyệt hợp đồng` (web 100041 / api 1141) · `Trưởng phòng duyệt đề nghị thanh toán`
   (web 100203 / api 1154) · `Trưởng phòng duyệt yêu cầu nhập hàng` (web 100984 / api 1166).
   Khoá theo ID xoá hẳn rủi ro "đổi tên quyền ⇒ âm thầm nới thành cấp công ty". 122 quyền duyệt
   còn lại chưa ai khai → hiện nhãn `Toàn công ty` + viền đứt + ⚠, để nhìn ra chỗ còn nợ.

4. **`type = NULL` của guard `api` quy về 1 (Chấm công) ở tầng BE.** Seeder không khai `type` cho
   nhóm này nên 78 quyền Chấm công **không hiện trên màn phân quyền cũ** (FE khớp `type` với
   `permissionType: 1`). Sửa tận gốc ở seeder thuộc Phase 2.

## Quyết định đã chốt — MỘT DÒNG = MỘT `group` (2026-09-02)

Mockup gom tay được "1 dòng = 1 màn", nhưng dữ liệu thật không có cột nào nói quyền thuộc màn nào
(đó chính là việc của cột `code` ở Phase 2). Đã đo 3 cách gom trên **toàn bộ 1.687 quyền**:

| Cách gom | Số dòng | Dòng chỉ có 1 quyền |
|---|---|---|
| Suy đối tượng từ tên quyền | 848 | 476 |
| Suy đối tượng + gộp tên lồng nhau | 721 | 358 |
| **1 dòng = 1 `group`** ← chọn | **288** | **39** |

Hai cách đầu phải khớp chuỗi tên để đoán, đoán sai thì quyền nằm nhầm dòng mà không ai biết; chúng
còn đẻ ra những dòng vô nghĩa (`danh sách phiếu giao công tác` ôm quyền duyệt). Cách thứ ba bám vào
`group` — dữ liệu có thật — nên không đoán gì cả, và 288 sát con số ~279 mà khảo sát Phase 0 ước tính.

**Không đánh đổi độ mịn:** ô nào gói nhiều quyền gốc thì thành nút `n/N` mở popup, mỗi quyền vẫn
cấp/gỡ riêng được. Toàn hệ: **285 ô checkbox thẳng + 200 ô popup**.

Ví dụ nhóm `Quản lý phiếu giao công tác` (13 quyền) thành **1 dòng**:
`Quản lý` popup 3 · `Xem` checkbox + 4 cấp phạm vi · `Duyệt` popup 3 (TP duyệt phiếu / TP duyệt kết
quả / Duyệt hồ sơ thanh toán) · `Quyền khác` popup 2 (Nhập kết quả công tác / Gia hạn, kết thúc sớm).

**Bất biến bắt buộc:** mọi quyền đều phải có chỗ trên ma trận. `PermissionMatrixService::selfCheck()`
kiểm điều này và controller ghi log lỗi nếu sai — màn giấu quyền thì người phân quyền không cấp được
mà cũng không biết là mình đang thiếu. Đo thực tế: **1.687/1.687, không rơi quyền nào.**

## Quyết định đã chốt — Phạm vi quyền DUYỆT (2026-08-28)

**Scope gắn theo QUYỀN, không theo cặp (chức vụ × quyền).**

- `"Trưởng phòng duyệt X"` tự thân đã mang nghĩa cấp phòng. Cho chức vụ A cấp phòng còn chức vụ B
  cấp công ty trên **cùng một quyền** là mâu thuẫn với chính tên gọi.
- Cần phạm vi khác → **tạo QUYỀN RIÊNG** (vd `"BGĐ duyệt X"`), KHÔNG nới scope. Đây cũng đúng cách
  hệ thống đang làm sẵn.
- Trên màn phân quyền: phạm vi duyệt là **nhãn CHỈ ĐỌC**, người phân quyền không chỉnh được.

### Nguồn dữ liệu scope

Hiện tại: `ERP/TanPhatDev/config/approval_inbox.php` → `permission_scopes`
(`department` = `department_id` ∈ phòng user quản lý · `part` = `part_id` ∈ bộ phận quản lý ·
không khai → `company`). 17 quyền khai `department`, 0 quyền dùng `part`.

**3 vấn đề phải xử khi làm thật:**

1. **KHOÁ THEO ID, KHÔNG THEO TÊN.** Map hiện khoá theo tên quyền + mặc định `company`
   ⇒ đổi tên một quyền cấp phòng là nó rơi khỏi map và **âm thầm nới thành cấp công ty**
   (người duyệt thấy/duyệt được phiếu phòng khác, không lỗi nào báo ra). Đổi tên quyền là việc
   ĐÃ xảy ra trong dự án (vụ "chiết khấu" → "giảm giá", giữ id đổi name).
2. **Không suy scope từ tên quyền** — chỉ đúng 12/17 (71%); 5 quyền cấp phòng không mang chữ
   "Trưởng phòng" (`Duyệt hợp đồng`, `Duyệt kế hoạch bán hàng phòng`,
   `Duyệt kế hoạch phát triển thị trường phòng`, `Duyệt chỉ tiêu kinh doanh theo phòng ban`,
   `Duyệt yêu cầu đặt hàng ngoài`).
3. **Mặc định phải fail-closed.** Quyền duyệt bắt buộc khai scope; thiếu khai thì coi là hẹp nhất
   hoặc chặn seeder — không lấy `company` (rộng nhất) làm mặc định như hiện nay.

**Đích kiến trúc:** thêm cột `permissions.approve_scope` (`company`/`department`/`part`), gate trong
controller đọc từ đó thay vì hardcode → một nguồn sự thật, đổi tên quyền vô hại, mọi màn
(phân quyền · hộp duyệt · báo cáo phê duyệt) dùng chung.
**Bước đi ngay (rẻ):** đổi `permission_scopes` từ khoá-theo-tên sang khoá-theo-ID — sửa 1 file,
xoá hẳn rủi ro (1), chưa phải đụng 47 luồng duyệt.

**UI đã hiện thực trong mockup:** nhãn chỉ đọc 2 mức `Phòng ban quản lý` (cam) / `Toàn công ty` (xám);
quyền **chưa khai scope** thì viền đứt + icon cảnh báo + tooltip, để phân biệt "đã xác nhận cấp công ty"
với "chưa ai khai, đang ăn mặc định". Chỉ vẽ mức nào thực dùng — không bê 4 cấp của cột Xem sang.

## Quyết định đã chốt — Ô "Tất cả" (2026-08-28)

Giữ nguyên hành vi hiện tại (user xác nhận). Cụ thể:
- Là **công tắc chọn nhanh cho cả dòng**, KHÔNG phải một permission — không sinh bản ghi nào trong CSDL.
- Tích → bật mọi hành động đối tượng đó *thực sự có* (Quản lý · Xem · **tất cả** loại Duyệt · tất cả
  mục Quyền khác); ô `–` bỏ qua. Bỏ tích → tắt hết + xoá phạm vi xem đã chọn.
- Trạng thái **suy ra**, chỉ tự tích khi mọi hành động của dòng đều đang bật.
- Khác biệt có chủ ý với ô `Duyệt` (ô Duyệt bật **1 loại đầu**, ô Tất cả bật **mọi loại**) — chấp nhận.
- Khi bật, phạm vi xem tự gán **cấp hẹp nhất** và KHÔNG mở popup (tránh popup nhảy ra giữa lúc tích
  hàng loạt); muốn rộng hơn thì bấm nhãn sửa.

## Quyết định đã chốt — Triển khai `code` (2026-09-05)

User chốt **làm chuẩn theo `code`, chấp nhận sửa lớn, đổi cách kiểm quyền toàn phần mềm**.
Bốn lựa chọn kèm theo:

| # | Chốt | Vì sao |
|---|---|---|
| 1 | **HRM trước, ERP đợt sau** | ERP đang ở nhánh `develop_01` (CLAUDE.md cấm trộn với `gop_db`) và local còn chạy DB riêng `erp2326` — sửa gate ERP bây giờ là sửa mà không test được trên dữ liệu sẽ chạy thật. Cột `code` vẫn backfill cho CẢ 1.687 quyền ngay từ đầu nên ERP chuyển sau không phải làm lại hạ tầng. |
| 2 | **Hằng số trên Entity** | `isCurrentEmployeeHasPermission(AssignJob::PERM_TP_APPROVE)`. Gõ sai thành lỗi ngay thay vì âm thầm trả `false` như 89 quyền ma hiện nay. PHP 7.4 nên không dùng được `enum`. |
| 3 | **Giữ nguyên tên 6 hàm kiểm quyền, chỉ đổi tham số** | Mỗi call site sửa đúng 1 tham số → diff nhỏ, rà soát được, quay đầu được. Gom API để việc riêng. |
| 4 | **Slug TIẾNG VIỆT không dấu** | Máy sinh 100%, không phải dịch tay 332 đối tượng, quyền mới về sau cũng máy sinh. Giá trị của `code` là BẤT BIẾN + máy kiểm được, không phải đẹp. |

⚠️ **Điều chỉnh so với bản chốt 2026-08-28**: mục "Quy ước `code`" bên dưới nêu ví dụ tiếng Anh
(`timesheet.leave_request.approve.tp`). Nay đổi sang tiếng Việt không dấu —
`timesheet.don_xin_nghi.approve.duyet`. Phần cấu trúc 4 đoạn và bộ hành động giữ nguyên.

### Khối lượng đã đo (2026-09-05)

| Nơi | Cơ chế | Số chỗ gọi |
|---|---|---|
| `hrm-api` | `isCurrentEmployeeHasPermission` 784 · middleware `checkPermission:` 418 · `checkPermissionList` 108 · `listEmployeeInfoHasPermission` 35 · khác 10 | **~1.355** |
| `hrm-client` | `hasAPermission` 390 · `hasPermission()` 15 | **~405** |
| ERP `TanPhatDev` (đợt sau) | `Auth::user()->can` 1.082 · `hasPermissionTo` 119 · `@can` 6 — 842 tên khác nhau | ~1.207 |

Hiện **931 chỗ dùng chuỗi literal, 0 chỗ dùng hằng số**.

### Bộ sinh `code` — đã chạy thử trên dữ liệu thật

Quy tắc: phân hệ lấy từ `type` (NULL → 1) · đối tượng = tên quyền đã bỏ động từ và bỏ hậu tố phạm vi,
slug hoá bỏ dấu · hành động `manage|view|approve|create|edit|delete|other` · biến thể = cấp phạm vi
(`all_company|company|department|part`) với `view`/`manage`, vai trò duyệt (`tp|kt|bgd|nshc|…`) với
`approve`, phần còn lại của tên với `other`.

Kết quả trên 722 quyền `guard = api`: **720 code duy nhất**, code dài nhất 84 ký tự, trung bình 45.
Chỉ **2 nhóm trùng**, và cả hai đúng là cặp quyền trùng tên có sẵn trong dữ liệu
(`finance.danh_muc_tien_te.manage` id 1115+1117 · `.view` id 1116+1118) — lỗi dữ liệu phải gộp,
không phải lỗi bộ sinh.

🐞 Bộ sinh bản đầu có lỗi tự bắt được: quyền `other` **vẫn có thể mang phạm vi**
("Phân ca theo công ty", "Xây dựng giá bán theo phòng") mà nhánh `other` lại bỏ mất cấp → 3 quyền
khác nhau dồn về một code. Sửa xong: 716 → 720 code duy nhất.

Phân bố hành động: `view` 495 · `manage` 83 · `approve` 48 · `other` 43 · `create` 27 · `edit` 13 ·
`delete` 13. Tổng 332 đối tượng khác nhau.

## Quyết định đã chốt — Định danh quyền bằng `code` bất biến (2026-08-28)

**Chốt: thêm cột `permissions.code` bất biến, gate đổi sang dùng `code`; `name` tụt xuống chỉ còn để hiển thị.**

### Vì sao không dừng ở "seeder + upsert"

Seeder + upsert theo id là giải pháp **tình thế**, và tự nó sinh một lỗi mới: `create(['id'=>X])` gặp
trùng id thì **nổ ngay**, còn `updateOrCreate(['id'=>X])` thì quyền sau **âm thầm ghi đè** quyền trước
— đổi một lỗi ồn ào lấy một lỗi im lặng. Ngoài ra nó không chạm tới 3 vấn đề gốc: id thủ công gây
tranh chấp giữa các nhánh · 1 file khổng lồ ai cũng sửa cuối file · không ai kiểm tên quyền ở gate
có khớp seeder không.

**Bằng chứng thực tế của cả 3:**
- Cặp trùng `Quản lý danh mục tiền tệ` (id 1115 **và** 1117) + `Xem danh mục tiền tệ` (1116 **và** 1118)
  nằm ở 4 dòng LIỀN NHAU — dấu vết hai nhánh cùng thêm rồi **merge sạch không xung đột**.
  Bảng có `unique(name, guard_name)` ⇒ **seeder hiện sẽ nổ trên DB sạch**.
- **89 quyền "ma"**: gate trỏ vào tên quyền không tồn tại trong seeder ⇒ **vĩnh viễn trả `false`**
  (HRM 28 / 44 chỗ · ERP 61 / 120 chỗ). Gồm cả sai chính tả (`Duyệt kế hoạch bán hàng phòng **ban**` trong khi seeder là
  `Duyệt kế hoạch bán hàng phòng`) và **thừa dấu cách** (`Xem␣␣phiếu báo hàng…`).
  Danh sách đầy đủ: `.plans/gop-db/thiet-ke-lai-phan-quyen/gate-quyen-ma.md`
- Quy mô: HRM 596 quyền / 332 tên dùng ở gate / **774 lời gọi** · ERP 979 quyền / 843 tên /
  **3.561 lời gọi**.

### Quy ước `code`

```
<phân hệ>.<đối tượng>.<hành động>[.<biến thể>]
```
chữ thường, `snake_case` trong từng đoạn, ngăn bằng dấu chấm.

| Ví dụ | Nghĩa |
|---|---|
| `timesheet.leave_request.view.department` | Xem đơn nghỉ phép theo phòng ban |
| `timesheet.leave_request.approve.tp` | Trưởng phòng duyệt đơn nghỉ phép |
| `payroll.salary_template.manage` | Quản lý mẫu bảng lương |
| `assign.business_trip.other.enter_result` | Nhập kết quả công tác |

- **Hành động** khớp đúng bộ cột của ma trận: `manage` · `view` · `approve` · `other`.
- **Biến thể** mang cấp phạm vi (`company`/`department`/…) với `view`, mang vai trò duyệt
  (`tp`/`kt`/`bgd`/`nshc`) với `approve`.
- **`code` phát hành rồi thì KHÔNG bao giờ đổi.** Đổi tên hiển thị thì sửa `name`, không đụng `code`.

### Lộ trình cuốn chiếu

1. Migration thêm `permissions.code` (nullable, `unique`).
2. Backfill `code` cho **1.606 quyền** hiện có (sinh máy từ `type`+`group`+`name`, rà tay ca đặc biệt).
3. Gate chấp nhận **cả `name` lẫn `code`** (resolve code→name) để tương thích ngược.
4. Chuyển call site **theo từng module, mỗi module 1 PR**.
5. `permission_scopes` (ERP) khoá theo `code` thay vì tên.
6. Bỏ nhánh tương thích khi không còn call site dùng `name`.

### Chốt chặn CI — làm được NGAY, không cần chờ `code`

1. **Mọi tên/`code` quyền dùng ở gate phải tồn tại trong seeder** → bắt đúng 92 ca hiện tại.
2. Không trùng `(name, guard_name)` → bắt cặp 1115/1117.
3. Không trùng `id`; `id` đã phát hành không tái dùng cho quyền khác nghĩa.
4. `action=approve` **bắt buộc** khai `approve_scope` (fail-closed, không mặc định `company`).
5. Mọi quyền phải khai đủ `object` + `action`.

Chốt số 1 nên làm trước tiên: rẻ, và đang có 89 quyền bị gate gọi mà không tồn tại (164 chỗ).
