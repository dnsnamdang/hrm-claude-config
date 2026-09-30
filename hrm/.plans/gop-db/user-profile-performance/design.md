# Tối ưu API `user-profile` — giảm tải CPU cho server

**Người phụ trách:** @namdangit · **Nhánh:** `gop_db` · **Bắt đầu:** 22/09/2026

## Mục tiêu

Giảm thời gian và CPU của `GET /api/v1/users/auth/user-profile` — API nặng nhất hệ thống, chạy ở
MỌI lần tải trang. Đích: payload 1,45 MB → dưới 300 KB, thời gian 0,65 s → dưới 0,25 s.

## Hiện trạng (đo 22/09/2026 trên hrm_crm)

Một request tiêu **0,5–0,7 s CPU**, trả **1.483.587 B** JSON, chạy **37 query**. Máy dev chỉ 4 CPU
cho 9 instance → trần ~6 req/s, nên "lúc nhanh lúc chậm" (xem [[reference_devhrm_server_perf]]).

Phân rã 1,45 MB payload và thời gian từng khối:

| Khối | Kích thước | Thời gian | Ghi chú |
|---|---|---|---|
| `departments` (67 dòng) | 442 KB | 60 ms / 13 query | **86% là 2 quan hệ lồng** `department_lead` (3,9 KB/dòng) + `parent_department` (1,8 KB/dòng) |
| `employees` (562 dòng) | 258 KB | 68 ms / 2 query | trả nguyên model, không lọc cột |
| `employee` → `permissions` | 199 KB | — | **TRÙNG HOÀN TOÀN** với `permissions` top-level, FE không đọc |
| `list_employee_infos` (562) | 186 KB | 21 ms / 1 query | đã select 13 cột, giữ nguyên |
| `permissions` (628) | 199 KB | 25 ms | bản FE thật sự dùng |
| còn lại | ~60 KB | ~60 ms | companies, parts, groups, notifications |
| `json_encode` toàn bộ | — | 93 ms | tỉ lệ thuận kích thước |

## Quyết định đã chốt

1. **KHÔNG tách endpoint theo kiểu lazy-load từng danh mục.** `state.departments` đang được đọc ở
   **119 file**, `companies` 84, `employees` 43 — đổi hợp đồng store là phải nghiệm thu lại toàn hệ
   thống. Giữ nguyên tên và hình dạng state; chỉ làm dữ liệu nhẹ đi và nạp thông minh hơn.
2. **Cắt tại nguồn trước, cache sau.** Việc rẻ và an toàn nhất (bỏ trùng lặp, select cột) làm trước
   và đo lại; cache chỉ để giải quyết phần còn lại.
3. **Chỉ làm trên `gop_db`.** Bản `tpe-develop-assign` (hrm.eteksofts.com) nặng tương đương — port
   sang sau khi bản này chạy ổn, không làm song song.

## Rủi ro đã biết

- `employee.permissions` bỏ đi: FE không dùng, nhưng **app di động `TPE_APP` chưa được kiểm** — phải
  grep trước khi xoá (Phase 1).
- `department_lead` / `parent_department`: có 3 file FE đọc tới (màn Quyết định điều chuyển / thành
  lập phòng ban) — giữ quan hệ nhưng chỉ select cột cần, không bỏ hẳn.
- Cache theo công ty phải xoá khi sửa danh mục phòng ban / nhân sự, nếu không user thấy dữ liệu cũ.

Spec chi tiết: `docs/superpowers/specs/gop-db/2026-09-22-user-profile-performance-design.md`

## Kết quả Phase 1 (22/09/2026)

Đo trên dữ liệu thật của `hrm_crm`, dựng **cả hai phiên bản hàm từ chính source** rồi so từng khoá
(script `/tmp/verify2.php`, sinh tự động bằng `scratchpad/gen.py` để không chép sai):

| | Cũ | Mới |
|---|---|---|
| Payload | 1.336.257 B | **867.993 B (−35%)** |
| Thời gian (CLI, không opcache) | 353 ms | 305 ms |
| Số query | 38 | 34 |

16/16 khoá cấp 1 còn nguyên, **14/16 khối giống hệt từng byte**. Hai khối đổi đúng như thiết kế:
`employee` 205.765 → 3.634 B (bỏ permissions trùng) và `departments` 421.228 → 155.095 B.

### Phát hiện ngoài dự kiến — lộ dữ liệu cá nhân

`departments[].department_lead` trỏ sang `EmployeeInfo` và được eager load **trần**, nên mỗi request
trả về **124 cột hồ sơ** của trưởng phòng cho **mọi user đăng nhập**, bất kể quyền: số CCCD/CMND
(47/67 phòng có giá trị thật), mã số thuế, ngày sinh, số tài khoản ngân hàng, địa chỉ thường trú,
đường dẫn file giấy tờ (`identity_card_file`, `birth_certificate_file`...), và 3 cột `salary_p1/p2/p3`
(rỗng ở DB này nhưng có cột). Thu gọn xuống `id,code,fullname` gỡ luôn 121 cột này.

### Điều chỉnh so với dự kiến ban đầu

- Dự kiến cắt cột `employees` (258 KB) → **BỎ**. Rà 43 file thấy `CreateTaskModal.vue:1710` và
  `SalesTeamSection.vue:96-113` đang đọc `department_name`, `part_name`, `email`,
  `personal_telephone`, `working_position_name` từ `state.employees` — bỏ đi là picker chọn người ở
  màn Giao việc mất email/điện thoại/bộ phận mà không có lỗi nào báo ra. Chỉ tối ưu phần nạp ngầm
  (`load('info:...')`): JSON không đổi 1 byte, 59 ms → 40 ms.
- Đích ban đầu "payload < 700 KB, 0,45 s" **không đạt bằng riêng Phase 1**: còn 868 KB vì 4 khối
  lớn còn lại (`permissions` 202 KB, `employees` 252 KB, `list_employee_infos` 180 KB,
  `departments` 155 KB) đều đang có client đọc thật. Muốn xuống nữa phải sang Phase 2 (cache) và
  Phase 3 (ETag/304), hoặc đổi hợp đồng store — việc đã cân nhắc và loại ở mục "Quyết định đã chốt".

## Kết quả cuối Phase 1 (sau khi rà thêm theo yêu cầu "check thật kỹ")

Rà tiếp **bên trong** từng khối, tìm được 2 nguồn lãng phí nữa:

- **`permissions`**: trả 10 cột nhưng FE chỉ đọc `.name` (+1 chỗ `.id`), app TPE_APP chỉ khai `name`.
  Riêng `created_at` + `updated_at` là 58 B/dòng × 628 dòng. → `select('id','name')`, giảm 159 KB.
  Màn cấu hình vai trò (`components/setting/Permission.vue`) nhận `permissions` qua **prop từ API
  riêng** (`pages/human/roles/add/_id.vue:182`), không lấy từ khối này.
- **`departments`**: 22/68 cột (cấu hình lương thưởng, `conditions_quarter_bonus`,
  `working_position_order`, ảnh nền…) **không xuất hiện ở bất kỳ file nào** của hrm-client lẫn
  TPE_APP → `makeHidden`, giảm 74 KB. Dùng blacklist thay whitelist để không sót cột FE đang đọc.

| | Server (hrm_crm) | Local (:8003) |
|---|---|---|
| Trước | 1.336.257 B | 1.579.984 B |
| Sau | **633.250 B (−53%)** | **748.196 B (−53%)** |

Kiểm chứng: 13/16 khối giống hệt từng byte · departments 67 dòng **0 giá trị lệch** · permissions
**628 quyền, tập id giống hệt, 0 tên lệch** · trên trình duyệt local **menu 40 = 40 mục, quyền
698 = 698** khi so bản gốc với bản mới trên cùng máy.

## Kiểm tác động lên app TPE_APP (đối chiếu từng JsonKey)

App gọi `user-profile` ở 4 chỗ (`user_api_service_profile_ext.dart`). Đối chiếu mọi `@JsonKey` mà
app khai với response mới thật (bản local), kết quả: **không ảnh hưởng**.

| Chỗ gọi | App đọc gì | Sau thay đổi |
|---|---|---|
| `getProfile()` | `json['employee']`: id, department_id, department_name, company_id, code, fullname, ssn, image, telephone, employee_work_position_id | còn đủ |
| `getUserId()` | `json['employee_data']['id']` | còn |
| `getDsNhanVien()` | `employees[]`: id, name, department_code, part_id, department_id, company_id, employee_info_id | còn đủ |
| `getUserProfile()` | companies, list_employee_infos, employees, departments, parts, permissions | còn đủ |

Hai khoá app có khai mà nay không còn, đều đã kiểm là vô hại:

1. **`employee.permissions`** — `getProfile()` ghi đè bằng `json['permissions']` top-level ngay sau khi
   parse (`if (permissionsRaw is List && permissionsRaw.isNotEmpty)`), nên khối lồng không được dùng.
   Trường hợp duy nhất còn lại là tài khoản **0 quyền**: mapper kết thúc bằng `.toList() ?? []`
   (`remote_employee_info_data_mapper.dart:33`) nên null → `[]`, đúng y như trước.
2. **`permissions[].guard_name / created_at / updated_at / display_name / group`** — mapper gán từng
   field bằng `e.<field> ?? ''` nên thiếu key chỉ ra chuỗi rỗng, không crash. Toàn bộ 12 chỗ app đọc
   permissions đều theo dạng `permissions.map((e) => e.name)` — chỉ dùng `name`.

`status_options` và `list_leave_type` app khai nhưng API **vốn chưa bao giờ trả** (trước và sau đều
không có) → app vẫn nhận `[]` như cũ.

⚠️ Phạm vi kiểm: source `TPE_APP` trong workspace (commit `632c24a`, 26/08/2026). Bản app đã phát
hành cho nhân viên nếu cũ hơn thì cần đối chiếu lại đúng bản đó.
