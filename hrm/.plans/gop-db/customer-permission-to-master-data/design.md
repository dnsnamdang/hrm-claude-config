# Chuyển quyền Quản lý khách hàng sang phân hệ Danh mục chung

> Phụ trách: @khoipv — nhánh `gop_db` (hrm-api)
> Spec chi tiết: `docs/superpowers/specs/gop-db/2026-08-20-customer-permission-to-master-data-design.md`

## Mục tiêu

1. Bỏ quyền khách hàng đang nằm ở phân hệ **Hành chính nhân sự** (type 3) bên HRM.
2. Đưa **11 quyền quản lý khách hàng của ERP** sang phân hệ **Danh mục chung** (type 9).
3. Màn Danh sách khách hàng bên HRM dùng đúng bộ quyền đó. ✅ **Xong 2026-08-21** —
   30 route đổi `erpPermission` → `checkPermission`, thêm `App\Helpers\CustomerPermissionHelper`,
   `my-permissions` trả đủ 11 cờ. Chi tiết ở mục "Bổ sung 2026-08-21 (2)" trong spec.
   ⚠️ Phải cấp lại quyền cho role trên màn Phân quyền, xem cảnh báo cuối file.

## Hiện trạng (khảo sát 2026-08-20)

- **Nhóm quyền cũ bên HRM**: id 166-169, `guard=api`, `type=3`, group `Danh mục khách hàng`.
- **Màn KH bên HRM đã chạy bằng quyền ERP rồi**: 30 route trong `Modules/Assign/Routes/api.php` gắn
  `erpPermission:Xem|Thêm|Sửa|Xóa|Xuất dữ liệu khách hàng`; thêm `ErpPermissionHelper::customerPermissions()`
  (API `assign/customers/my-permissions`) và FE middleware `middleware/checkCustomerPermission.js`.
- **11 quyền ERP** trên DB gộp: id `100057…100228`, `guard=web`, group `Quản lý khách hàng`.
  (Bẫy: trên DB gộp quyền ERP mang id `+100000`. Query bằng id ERP gốc 57/58/… sẽ trúng nhầm quyền
  HRM `guard=api` trùng số.)
- Màn Phân quyền HRM (`components/setting/Permission.vue` + `PermissionService::getLists()`) lọc theo
  cột **`type`**, **không lọc `guard`**.

### ⚠️ Đính chính giữa chừng: 166-169 không chết hết

Khảo sát đầu tiên kết luận cả 4 quyền đều chết vì grep không thấy tên nào được tham chiếu. **Sai với
id 167.** `ErpPermissionHelper::userCan()` tra quyền bằng `whereIn('name', ...)` và **không lọc guard**,
mà 167 tên là `Xem tất cả khách hàng` — trùng nguyên văn tên quyền ERP 100170. Nên 14 dòng gán của 167
vẫn đang thực sự cấp quyền xem khách hàng toàn tổng công ty.

166 (`Quản lý khách hàng` — ERP không có quyền nào tên vậy, đó là tên *nhóm*), 168 (`…theo công ty` vs
ERP `…của công ty`) và 169 (`…theo phòng ban` vs ERP `…của phòng ban`) thì đúng là chết.

## Quyết định

Khai **11 quyền bản `guard=api`, `type=9`, group `Quản lý khách hàng`**, tên giữ **nguyên văn của ERP**.

Đây là tiền lệ đã có sẵn trong chính file seeder (id 1515-1516, Phiếu ủy nhiệm chi): quyền ERP có ở
`guard=web` nhưng app chạy `guard=api` nên khai bản `api` riêng, giữ nguyên tên để 2 cổng không lệch.

Vì các helper so theo `name` chứ không theo id/guard, cách này được cả hai đầu:

| Tên quyền | id khớp | số role đang gán |
| --- | --- | --- |
| Xem khách hàng | 1517 (api) + 100057 (web) | 64 |
| Sửa khách hàng | 1519 (api) + 100059 (web) | 14 |
| Xem tất cả khách hàng | 167 (api) + 100170 (web) | 32 |

→ Gán cũ bên ERP **vẫn hiệu lực**, đồng thời tick mới trên màn Phân quyền HRM cũng ăn ngay.

**Id 167 được giữ lại** cho quyền `Xem tất cả khách hàng` (chỉ đổi `group` + `type`), để 14 dòng gán
đang có không mất. 166/168/169 bỏ hẳn.

## Cách triển khai: TẤT CẢ trong `PermissionsTableSeeder`, KHÔNG dùng migration

User chốt 2026-08-20: không viết migration riêng cho permission, đúng luật CLAUDE.md, và khai quyền
theo đúng kiểu `Permission::create` như mọi quyền khác trong file. Seeder gánh 3 việc:

1. Bỏ 4 dòng `Permission::create` id 166-169 ở nhóm `Danh mục khách hàng`.
2. Khai 11 dòng `Permission::create` mới ở cuối `run()` — id 1517-1526 + 167, `type => 9`,
   `sort_order => 1..11`.

Hết. Không đụng `GROUP_ORDER` (type 9 chỉ có đúng 1 nhóm nên khai thứ tự nhóm không đổi gì; thứ tự
hiển thị trong nhóm do `sort_order` quyết định, độc lập với `GROUP_ORDER`) và không thêm bất kỳ xử lý
nào khác vào `run()` — làm y như các phân hệ khác trong file, chỉ khai quyền.

### Đánh đổi đã chấp nhận

- Thay đổi chỉ có hiệu lực **khi chạy seeder**. Không có migration nghĩa là không có bước tự động lúc
  deploy — mỗi môi trường phải chủ động chạy `PermissionsTableSeeder`.
- 166/168/169 biến mất khỏi seeder nhưng phần gán cũ của chúng trong `role_has_permissions` vẫn nằm lại
  (seeder không dọn pivot cho bất kỳ quyền nào — giữ đúng nếp của file). Vô hại vì join sẽ rớt, chỉ lưu ý
  nếu sau này có ai cấp lại 3 id đó cho quyền khác.
- ⚠️ **Chặn triển khai**: seeder đang có sẵn lỗi trùng `name`+`guard` (id 1117≡1115, 1118≡1116 —
  "Quản lý/Xem danh mục tiền tệ", dòng ~1130-1131). Chạy seeder thật sẽ ném `PermissionAlreadyExists`
  tại 1117 và mọi dòng sau đó KHÔNG chạy, kể cả 11 quyền mới ở cuối file. Phải bỏ 1 cặp trước khi seed.
  Lỗi có từ trước, đã ghi trong `.plans/gop-db/STATUS.md`.

## Phạm vi 11 quyền

Chốt với user: **chỉ nhóm `Quản lý khách hàng`**. KHÔNG gồm nhóm `Quản lý Nhóm khách hàng`
(ERP id 61, 1026-1028) và KHÔNG gồm quyền `danh mục lĩnh vực khách hàng` của HRM (996, 1006, 1093,
1094 — giữ nguyên type 4).

| id mới | name (nguyên văn ERP) | display_name | sort |
| --- | --- | --- | --- |
| 1517 | Xem khách hàng | Xem | 1 |
| 1518 | Thêm khách hàng | Thêm | 2 |
| 1519 | Sửa khách hàng | Sửa | 3 |
| 1520 | Xóa khách hàng | Xóa | 4 |
| 1521 | Xem lịch sử khách hàng | Xem lịch sử | 5 |
| 1522 | Xuất dữ liệu khách hàng | Xuất dữ liệu | 6 |
| **167** | Xem tất cả khách hàng | Xem khách hàng theo tổng công ty | 7 |
| 1523 | Xem tất cả khách hàng của công ty | Xem khách hàng theo công ty | 8 |
| 1524 | Xem tất cả khách hàng của phòng ban | Xem khách hàng theo phòng ban | 9 |
| 1525 | Xem tất cả khách hàng của bộ phận | Xem khách hàng theo bộ phận | 10 |
| 1526 | Xem danh sách khách hàng đã đăng ký | Xem danh sách khách hàng đã đăng ký | 11 |

## Phạm vi thay đổi

- `hrm-api` — **2 file**:
  - `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` — khai 11 quyền.
  - `Modules/Timesheet/Services/PermissionService.php` — `getLists()` lọc `guard_name = 'api'`
    (xem "Bẫy phát hiện 2026-08-21" bên dưới).
- `hrm-client` — **không sửa gì**.

## ⚠️ Bẫy phát hiện 2026-08-21 — khai quyền đúng vẫn không thấy trên màn Phân quyền

Khai xong 11 quyền, DB có đủ, `getLists()` trả về đủ — nhưng khối "Danh mục chung"
vẫn trống. Nguyên nhân ở FE: `components/setting/Permission.vue:138` gộp quyền thành khối
**chỉ theo tên `group`, bỏ qua `type`**, và lấy `type` của phần tử đầu tiên gặp:

```js
if (this.permissions[i].group == this.list_permissions[j].group) exist = j   // không so type
```

`getLists()` khi đó không lọc guard, mà 11 quyền ERP `guard=web` cùng tên group
`Quản lý khách hàng` có `type=NULL` — sắp xếp theo `type` thì `NULL < 9` nên chúng đứng
trước → khối được tạo với `type=NULL`, 11 quyền `type=9` bị nhét chung vào đó →
`filterPermission(9)` rỗng, mà `type=NULL` không phân hệ nào khai `permissionType` nên
cả khối biến mất khỏi màn.

Quét toàn bảng: đúng **2 nhóm** dính lỗi này — `Quản lý khách hàng` (type 9) và
`Quản lý quyết toán hợp đồng` (type 4). Trong riêng guard `api` không có nhóm nào mang 2 `type`.

**Quyết định (user chốt 2026-08-21): dùng bộ quyền mới bên HRM** — `getLists()` lọc
`guard_name = 'api'`, bỏ 965 quyền ERP `web` khỏi payload màn Phân quyền. Sửa BE thay vì sửa
`Permission.vue` vì `Permission.vue` là component dùng chung, mà trong guard `api` không có
xung đột `group`+`type` nào — lọc guard là đủ và đúng bản chất (app HRM chạy guard `api`).

**Không mất gán quyền ERP cũ**: `RoleDetailResource` vẫn trả đủ `permission_ids` của role
(kể cả id `guard=web`) nên chúng nằm trong v-model của màn; `Role::syncPermissionsByCompany()`
chỉ xóa id **có trong danh sách cũ nhưng không có trong danh sách gửi lên**, nên 8007 dòng
`role_has_permissions` trỏ tới quyền `web` vẫn được giữ nguyên khi lưu.

**Còn tồn đọng (chưa xử lý)**: 78 quyền `guard=api` đang có `type = NULL` — không thuộc
phân hệ nào nên cũng không hiển thị được trên màn Phân quyền.

---

## ⚠️ Sau khi đổi cơ chế (2026-08-21): PHẢI cấp lại quyền

Màn Khách hàng nay chỉ tính quyền HRM `guard = api`. Bộ quyền này gần như chưa gán cho role nào
(Xem/Thêm/Sửa/Xóa/Xuất/Lịch sử đều **0 role**; toàn bộ gán thật đang nằm ở bản ERP `guard = web`:
64/49/14/4/24/19 role). Riêng `Xem tất cả khách hàng` (id 167) có 14 role.

→ Không cấp lại thì **mọi tài khoản** mất nút Thêm/Sửa/Xuất/Khóa/Lịch sử và không mở được chi
tiết KH. Cấp ở Thiết lập → Phân quyền → "Danh mục chung" → nhóm "Quản lý khách hàng".

Phương án thay thế (chưa làm, chờ quyết): copy `role_has_permissions` từ id `web` sang id `api`.
