# Plan — Dự án TKT: đổi nhãn + Nhóm ngành (Redmine #11142)

> @junfoke — Nhánh `task_11142` (tách từ `tpe`), cả 2 repo.
> Design: `.plans/tkt-project-labels-and-industry/design.md`

## Phase 1 — Đổi nhãn (màn dự án TKT + message BE)

- [x] 1.1 `components/ProgressFinanceSection.vue` — nhãn Giai đoạn dự án KH / Ngày bắt đầu dự án TKT /
      Ngày kết thúc dự án TKT + 4 message validate inline
- [x] 1.2 `prospective-projects/index.vue` — nhãn ô lọc + tiêu đề cột
- [x] 1.3 `components/ProspectiveProjectChildrenTab.vue` — tiêu đề cột (tab Dự án con)
- [x] 1.4 `components/SolutionListModal.vue` — tiêu đề cột
- [x] 1.5 BE `ProspectiveProjectRequest.php` — message `start_date.after_or_equal`,
      `end_date.after_or_equal` + attribute `project_phase_id`
- [x] 1.6 Rà lại toàn bộ chuỗi cũ trong phạm vi dự án TKT, kiểm CRLF, verify trên UI

## Điểm cần chốt trước khi làm tiếp

1. **Nhãn "Giai đoạn dự án KH" lan tới đâu?** Trường `project_phase_id` còn hiện ở Báo giá (bộ lọc +
   form), Yêu cầu làm giải pháp, Công việc của tôi, Meeting. Đổi hết hay chỉ màn dự án TKT? Tên
   **danh mục** "Giai đoạn dự án" (menu Danh mục, `/assign/project_phase`) có đổi không?
2. **Phase 3 (ràng buộc trùng nhóm ngành)**: "đang mở" tính theo trạng thái nào trong 12 trạng thái
   của dự án TKT? Dữ liệu cũ đang vi phạm thì xử lý ra sao?
3. **Phase 4 (kéo meeting cá nhân)**: đối chiếu "tên và SĐT trong danh sách liên hệ" theo quy tắc nào?

## Phase 2 — Trường Nhóm ngành (chưa làm)
## Phase 3 — Ràng buộc 1 KH + 1 nhóm ngành (chưa làm, chờ chốt)
## Phase 4 — Liên kết meeting khi chuyển loại KH (chưa làm, chờ chốt)

### Checkpoint — 2026-09-11
Vừa hoàn thành: tách nhánh `task_11142` ở cả 2 repo, rà phạm vi nhãn
Đang làm dở: Phase 1
Bước tiếp theo: sửa 4 file FE + 1 file BE
Blocked:

## Phase 2 — Trường Nhóm ngành (đã code)

- [x] 2.1 Migration `2026_09_11_000001_create_prospective_project_scopes_table.php` — bảng nhiều-nhiều
      cho dự án CHA (dự án con/độc lập vẫn dùng cột `scope_id` có sẵn). Đã chạy trên DB `hrm_prod_30_3_26`
- [x] 2.2 `ProspectiveProject`: quan hệ `scopes()` + hằng `SCOPE_OCCUPYING_STATUSES`
- [x] 2.3 `ProspectiveProjectService`: bỏ ghi đè `scope_id` theo Ứng dụng (chỉ còn điền hộ khi trống),
      thêm `syncProjectScopes()` gọi ở cả store và update
- [x] 2.4 `ProspectiveProjectRequest`: `scope_id` bắt buộc (con/độc lập), `scope_ids[]` bắt buộc (cha)
- [x] 2.5 `DetailProspectiveProjectResource`: trả `scope_name` + `scopes[]`; controller `show()` eager load
- [x] 2.6 FE `ProjectInfoSection.vue`: ô chọn Nhóm ngành (1 giá trị / nhiều giá trị theo loại dự án)
- [x] 2.7 FE `add.vue` / `_id/edit.vue` / `_id/index.vue`: khởi tạo + map `scope_ids` từ `scopes[]`

## Phase 3 — Ràng buộc 1 KH + 1 nhóm ngành (đã code)

- [x] 3.1 `scopeConflictRule()` trong FormRequest — chặn khi tạo mới / đổi sang nhóm đang bị chiếm
- [x] 3.2 `ScopeService::getAll()` nhận `customer_id` + `current_project_id` — ẩn nhóm ngành bị chiếm,
      GIỮ nhóm ngành của chính dự án đang sửa (kể cả khi dữ liệu cũ đang vi phạm)

### Kiểm BE bằng dữ liệu thật (2026-09-11, DB `hrm_prod_30_3_26`)

| Ca | Kết quả |
| --- | --- |
| Quan hệ `scopes()` sync/đọc pivot | ✔ |
| Tạo mới, chọn nhóm ngành đang bị dự án mở khác chiếm | ✔ bị chặn, message nêu rõ mã dự án đang giữ |
| Tạo mới, chọn nhóm khác | ✔ cho qua |
| Sửa dự án cũ, giữ nguyên nhóm ngành (dữ liệu cũ vi phạm) | ✔ cho qua — đúng "chỉ chặn từ nay" |
| Sửa dự án A đổi sang nhóm của dự án mở B | ✔ bị chặn |
| Options: ẩn nhóm bị chiếm khi tạo mới | ✔ |
| Options: giữ nhóm của chính dự án đang sửa | ✔ (lần đầu SAI, đã vá: trừ nhóm của chính dự án ra khỏi danh sách bị chiếm) |

**CHƯA verify:** FE trên UI thật (ô chọn 1 giá trị / nhiều giá trị, lưu và mở lại).

### Verify FE trên UI thật (2026-09-11, FE :3005 -> API :8002 -> DB hrm_prod_30_3_26)

| Ca | Kết quả |
| --- | --- |
| Nhãn màn Tạo mới dự án TKT | ✔ "Giai đoạn dự án KH *", "Ngày bắt đầu dự án TKT", "Ngày kết thúc dự án TKT" |
| Dự án độc lập: ô Nhóm ngành | ✔ hiện, bắt buộc (*), chọn 1, 22 nhóm ngành |
| Dự án CHA: ô Nhóm ngành | ✔ chuyển sang chọn NHIỀU; Giai đoạn dự án KH ẩn đúng URD; 2 ô ngày thành bắt buộc |
| Chọn nhiều nhóm ngành | ✔ `scope_ids = [2, 6]`, `scope_id = 2` (nhóm đầu làm đại diện, khớp cách BE lưu) |
| Đổi khách hàng -> lọc lại options | ✔ 22 -> 21, nhóm ngành đang bị dự án mở khác của KH 2317 chiếm biến mất |

Lỗi 500 trong console là do tôi gán `customer_id` bằng tay không qua luồng chọn KH thật (API khách
hàng/meeting của ERP cần dữ liệu kèm theo), không liên quan code mới.

**CHƯA verify:** lưu thật rồi mở lại — tài khoản dev không phải Sale phụ trách dự án nào nên BE chặn
tạo/sửa dự án TKT (đúng vấn đề đã gặp ở #10900).

## Phase 4 — Liên kết meeting khi chuyển loại KH (ĐÃ LÀM)

Spec còn hở, cần chốt với khách:
- Đối chiếu "khách hàng cá nhân ban đầu có tên và SĐT trong danh sách liên hệ của doanh nghiệp mới"
  theo quy tắc nào (khớp cả tên lẫn SĐT? chỉ SĐT? chuẩn hoá số thế nào?)
- "Người chủ trì cuộc họp phải là người tạo dự án TKT hiện tại" — áp cho cả meeting doanh nghiệp hay
  chỉ meeting cá nhân?
- Kéo meeting cũ về là gắn thêm vào `prospective_project_meetings` hay đổi chủ sở hữu meeting?

### Checkpoint — 2026-09-11 (lần 2)
Vừa hoàn thành: Phase 1 (nhãn) + Phase 2 (Nhóm ngành) + Phase 3 (ràng buộc trùng) — code xong,
BE kiểm bằng dữ liệu thật, FE kiểm trên UI
Đang làm dở: không
Bước tiếp theo: user chốt spec Phase 4; cân nhắc commit Phase 1-3 trước
Blocked: Phase 4 chờ spec; ca "lưu thật" chờ tài khoản Sale phụ trách dự án

### Phase 4 — cách làm (user chốt "làm xong cả đi", 3 điểm hở tôi tự quyết, ghi rõ để QA soát)

- [x] 4.1 BE `ProspectiveProjectService::getSelectableMeetings($customerId, $projectId)` — trả đúng tập
      meeting chọn được cho ô "Meeting liên quan"
- [x] 4.2 BE endpoint `GET /assign/prospective-projects/meeting-options?customer_id=&project_id=`
- [x] 4.3 FE `RelatedSection.vue` dùng endpoint mới (bỏ cách cũ tải `assign/meeting?per_page=1000`
      rồi tự lọc — vừa nặng vừa không làm được vế meeting cá nhân)

**Giả định đã chọn (cần khách xác nhận):**
1. **Đối chiếu bằng SỐ ĐIỆN THOẠI, không đối chiếu tên.** Tên người ERP viết hoa/có dấu không thống
   nhất nên khớp tên sẽ vừa sót vừa nhầm; SĐT là khoá định danh chắc chắn. SĐT được chuẩn hoá trước
   khi so: bỏ khoảng trắng/dấu chấm/gạch, `+84`/`84` → `0`, số 9 chữ số thêm `0` đầu; 1 người liên hệ
   khai nhiều số (`,` `;` `/` `|`) thì tách ra so từng số.
2. **Điều kiện "người chủ trì = người tạo dự án TKT" áp cho CẢ HAI nhóm** (meeting của khách doanh
   nghiệp lẫn meeting cá nhân) — đúng câu chữ spec. Lưu ý: siết chặt hơn hiện tại, trước đây chọn
   được mọi meeting của khách hàng đó. "Người tạo dự án" = `created_by` của dự án đang sửa; màn Tạo
   mới thì là người đang đăng nhập.
3. **Kéo meeting về = gắn thêm liên kết** (`prospective_project_meetings`), KHÔNG đổi chủ sở hữu
   meeting — meeting vẫn thuộc khách cá nhân cũ, chỉ là dự án của doanh nghiệp mới trỏ tới nó.
4. Meeting đã gắn sẵn vào dự án luôn được trả về kể cả khi không còn khớp điều kiện, tránh mở màn
   Sửa là mất liên kết cũ. Dòng meeting kéo từ khách cá nhân hiện hậu tố "(khách cá nhân)".

### Kiểm Phase 4 (2026-09-11)

| Ca | Kết quả |
| --- | --- |
| Chuẩn hoá SĐT: `0966266709` / `+84 966 266 709` / `84966266709` / `966266709` / `0966.266.709` | ✔ đều ra `0966266709` |
| Tách nhiều số trong 1 người liên hệ | ✔ KH 620 ra 43 số riêng lẻ |
| Tìm KH cá nhân theo SĐT người liên hệ | ✔ `['0966266709']` → KH cá nhân id 3966 (cả khi SĐT gốc viết dạng +84) |
| Lọc theo người chủ trì | ✔ dự án 3 (người tạo 57) + KH 2317 → 0 meeting; đổi sang đúng KH 43556 của meeting do 57 chủ trì → 1 meeting |
| FE gọi endpoint mới | ✔ `meeting-options?customer_id=43556`, KHÔNG còn gọi `assign/meeting?per_page=1000` |
| Đổi khách hàng → nạp lại danh sách | ✔ |

**CHƯA kiểm được end-to-end vế "kéo meeting cá nhân"**: DB snapshot không có sẵn cặp (KH cá nhân có
SĐT trùng người liên hệ của một KH doanh nghiệp) và thao tác ghi DB bị chặn nên không dựng được dữ
liệu giả. Đã kiểm từng mắt xích (chuẩn hoá SĐT → tìm KH cá nhân → truy vấn meeting) bằng dữ liệu thật.

### Checkpoint — 2026-09-11 (lần 3, kết)
Vừa hoàn thành: cả 4 mục của #11142
Đang làm dở: không
Bước tiếp theo: commit 2 repo; khách xác nhận 3 giả định ở Phase 4
Blocked: không
