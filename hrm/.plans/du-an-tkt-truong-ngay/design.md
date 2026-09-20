# Dự án TKT — Đổi tên trường ngày, khoá Ngày bắt đầu, tooltip Ngày kết thúc

- **Redmine**: [#11310](http://quanly.dnsmedia.vn/issues/11310) — [PL8 - Quản lý dự án TKT]
- **Người phụ trách**: @khoipv
- **Nhánh**: `fix-bug-11092026` (hrm-client) — không phải nhánh `gop_db`
- **Phạm vi**: chỉ FE (`hrm-client`), không đụng BE

## Mục tiêu

Màn **Quản lý dự án TKT → Dự án** (`/assign/prospective-projects`):

1. Đổi nhãn `Ngày bắt đầu dự án` → **`Ngày bắt đầu dự án TKT`**,
   `Ngày kết thúc dự án` → **`Ngày kết thúc dự án TKT`**.
2. `Ngày bắt đầu dự án TKT`:
   - Màn Tạo mới: mặc định = ngày hiện tại, **khoá không cho sửa**.
   - Màn Sửa: giữ nguyên giá trị đã lưu, vẫn **khoá**.
3. `Ngày kết thúc dự án TKT`: thêm icon `(i)` cạnh nhãn, hover hiện tooltip
   *"Ngày dự kiến chốt báo giá cuối cùng để chuyển sang giai đoạn ký hợp đồng"*.

## Quyết định

- **Chỉ sửa 1 component dùng chung**: `pages/assign/prospective-projects/components/ProgressFinanceSection.vue`
  — đã grep toàn FE, 2 nhãn này **chỉ xuất hiện ở đây**. Component được dùng bởi 4 màn:
  `add.vue` (Tạo mới), `_id/edit.vue` (Sửa), `_id/index.vue` (Chi tiết),
  `request-solution/components/TktTab.vue` (tab TKT, `isShow=true`) → sửa 1 chỗ là đồng bộ cả 4.
- **Giá trị mặc định ngày hiện tại đặt ở `add.vue` `data()`**, KHÔNG đặt trong `mounted()` của
  component con. Hai lý do:
  - `unsavedChangesMixin` chốt `unsavedBaseline` ngay trong `mounted()` → gán ở `mounted` sẽ làm
    form bị coi là "đã sửa" và hiện popup "chưa lưu" dù user không đụng gì.
  - Đặt trong component con sẽ ăn sang cả màn Sửa: lúc `mounted` dữ liệu API chưa về nên
    `start_date` còn rỗng → sẽ âm thầm ghi đè thành ngày hôm nay, sai yêu cầu "giữ nguyên giá trị đã lưu".
- **Không dùng `toISOString()`** để lấy ngày hôm nay: hàm đó trả giờ UTC, VN là UTC+7 nên từ
  00:00–07:00 sẽ ra **ngày hôm trước**. Dựng chuỗi `YYYY-MM-DD` từ `getFullYear/getMonth/getDate`
  (khớp `valueType` mặc định của `V2BaseDatePicker`).
- **Icon Info** theo `.claude/skills/info-icon-tooltip/SKILL.md` mục 2: `ri-information-line` 14px
  `#94a3b8` + `b-popover` `custom-class="info-popover"` `triggers="hover focus"` `placement="bottom"`.
- Giữ nguyên `disabled-date="disablePastDates"` và toàn bộ rule validate timeline hiện có —
  trường bị khoá thì rule không còn cơ hội nổ, nhưng không xoá để màn Sửa dữ liệu cũ vẫn an toàn.

## Không làm

- Không sửa BE: nhãn chỉ nằm ở FE, `start_date` vẫn được gửi lên như cũ (ô disabled của
  `vue2-datepicker` vẫn giữ giá trị trong `v-model`).
- Không đổi các câu thông báo lỗi validate (`"Ngày bắt đầu dự án phải …"`) — Redmine chỉ yêu cầu đổi **nhãn trường**.

## Phát sinh khi làm — hai thế kẹt do khoá trường

Mô tả Redmine chỉ nói "khoá ngày bắt đầu", không tính tới các rule đang chặn ngày quá khứ:

1. **Dự án nháp tạo từ hôm trước (đã xử lý)**: `ProspectiveProjectRequest` áp
   `after_or_equal:today` cho `start_date` khi dự án còn nháp; FE cũng có rule tương ứng.
   Khoá trường ⇒ user không dời được ngày ⇒ **không bao giờ lưu lại được**.
   Xử lý: bỏ rule quá khứ cho riêng `start_date` ở cả FE lẫn BE; `end_date` và 2 mốc kỹ thuật
   giữ nguyên. Lỗi cặp bắt đầu/kết thúc chuyển hết sang báo ở `Ngày kết thúc dự án TKT`.
2. **Dự án con có cha bắt đầu ở tương lai (CHƯA xử lý — chờ BA)**:
   `withValidator()` bắt `start_date >= parent.start_date`. Ngày bắt đầu giờ cứng = hôm nay
   ⇒ tạo dự án con cho một dự án cha bắt đầu từ ngày mai trở đi sẽ luôn báo lỗi mà không có
   đường gỡ. Xem T10 trong `plan.md`.
