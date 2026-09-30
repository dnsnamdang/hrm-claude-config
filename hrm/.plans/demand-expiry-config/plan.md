# Plan — Cảnh báo & tự động đóng nhu cầu theo Lĩnh vực (Redmine #11377)

> ⚠️ **FILE NÀY ĐÃ BỊ MẤT NỘI DUNG GỐC ngày 30/09/2026** do lỗi thao tác của Claude: lệnh ghi file
> mở ở chế độ `wb` (cắt file về 0 byte trước), rồi encode nội dung mới thì lỗi — file thành rỗng.
> Thư mục này chưa commit vào `hrm-claude-config` nên **không có bản git để khôi phục**.
>
> Phần dưới đây là **dựng lại từ lịch sử phiên làm việc**, đầy đủ từ đợt QA 17/09 trở đi.
> **ĐÃ MẤT**: phần plan gốc trước 17/09 (danh sách task BE/FE theo Phase của feature, checkpoint
> 14/09 bản đầy đủ). Thiết kế gốc vẫn còn nguyên ở `design.md` cùng thư mục.

---

## Phase QA — Sửa 7 bug QA phản hồi (17/09/2026)

- [x] **BUG 1** — Lưu Cấu hình chung xong ô "Cảnh báo trước khi đóng nhu cầu" bị rỗng, phải F5.
      `MyJobService::saveDeadlineConfig()` trả về thiếu `demand_warning_days`.
- [x] **BUG 2** — Nhập số âm báo tiếng Anh. Rule `min_value` không có bản dịch trong `locales/vi.json`.
- [x] **BUG 3** — Chọn Trạng thái = Khoá là không đổi lại được: `isLocked` đọc giá trị ĐANG CHỌN
      thay vì trạng thái ĐÃ LƯU → thêm `savedStatus`.
- [x] **BUG 4** — Sửa N = 30, báo lưu thành công nhưng danh sách vẫn "Không thời hạn":
      `InternalBusinessScopeService::update()` và `updateOrCreate()` **không đưa `demand_due_days`**
      vào payload — gốc rễ nặng nhất đợt đó.
- [x] **BUG 5** — Bộ lọc Lĩnh vực ở màn Nhu cầu khách hàng rỗng: FE đọc `res.data.fields` / `.scopes`
      trong khi API trả **mảng** lĩnh vực ôm `industry_groups`.
- [x] **BUG 6** — Gõ `1e3333` không bị chặn: `<input type="number">` coi `e` / `+` là hợp lệ nhưng
      trả `value = ''` về Vue → chặn ở `V2BaseInput` (keydown + paste).
- [x] **BUG 7** — Dropdown Lĩnh vực ở form Meeting thiếu lĩnh vực mới: **không phải lỗi**,
      `MeetingController::investmentScopes()` cố ý loại lĩnh vực chưa có Nhóm ngành con.

`hrm-api` ace1f47ec · `hrm-client` 9b4129445 — sau đó merge vào `tpe-develop-assign`
(`hrm-api` 51ca5d7d5 · `hrm-client` ad0182600).

## BUG 8 — giao diện báo "sắp hết hạn" cho nhu cầu không bao giờ được cảnh báo (22/09/2026)

Phát hiện khi QA chạy tay cron: 2 nhu cầu hiện "(còn 2 ngày)" màu cam nhưng cron báo **0 cảnh báo**.
Nguyên nhân: màn danh sách tính `is_due_soon` thiếu điều kiện `N > M` mà cron đang áp.
→ thêm `N > M` vào `attachDueDate` — `hrm-api` **e2f61d6eb**.

> ⚠️ Quyết định này **đã bị đảo ngược ngày 30/09** — xem mục BUG 7 cuối file.

### Cách chạy tay cron để kiểm tra thông báo cảnh báo

```
php artisan assign:close-expired-customer-demands --dry-run   # CHỈ liệt kê, KHÔNG gửi
php artisan assign:close-expired-customer-demands             # chạy thật, có gửi
```

Lịch cron: `dailyAt('01:20')` giờ VN (`app/Console/Kernel.php`). Một nhu cầu vào diện cảnh báo khi:
trạng thái Đang theo dõi · chưa gắn Dự án TKT · cuộc họp đã Hoàn thành (`meetings.completed_at` = T) ·
**N > 0** · `today` trong `[T+N-M, T+N)` · `expiry_warned_at` còn NULL.

⚠️ `expiry_warned_at` là cờ chặn báo trùng — chạy thật 1 lần là nó được ghi, muốn test lại phải đặt
về NULL. Người nhận thông báo là **chủ trì cuộc họp** (`meetings.host_employee_id`), không có thì
người tạo meeting.

## ĐỢT QA 3 — 4 bug phản hồi ngày 24/09/2026

`hrm-api` **4edf957c4** · `hrm-client` **ccb432cc7**.

- [x] **BUG 1** — bấm Lưu form trống chỉ mỗi ô N báo đỏ. Commit `d4437fa3f` (18/09) đã cố ý gỡ
      `v-validate` của Mã / Tên để BE chốt rule, nhưng `submitForm` vẫn `return` sớm → API không
      được gọi → BE mất cơ hội trả 422. → bỏ `return` sớm.
- [x] **BUG 2** — N = 0 đổi chữ thành "Không giới hạn thời gian hiệu lực" (cột danh mục, chú thích
      popup, file Excel).
- [x] **BUG 3** — ô M nhận số âm: chỉ có `min="0"` của HTML, BE `max(0, ...)` lặng lẽ kéo về 0
      (tự sửa giá trị user). → thêm validate + chặn lưu.
- [x] **BUG 4** — lịch sử "Đóng dự án tự động" xếp mới → cũ. Giữ `orderByDesc('id')->limit(500)` để
      lấy đúng 500 bản ghi MỚI NHẤT rồi `->reverse()`.

## ĐỢT QA 4 — 7 bug phản hồi 28/09/2026 (nhánh `develop`)

⚠️ **5/7 bug ĐÃ CÓ CODE SỬA từ trước** — QA test trên bản dev chưa deploy lại.
**Trước khi sửa tiếp, luôn kiểm code trên nhánh đang deploy đã có fix chưa.**

| Bug QA nêu | Thực tế |
| --- | --- |
| 1. Chỉ ô N báo lỗi | ĐÃ sửa từ 24/09 |
| 2. Chặn số âm ở ô M | ĐÃ sửa; **bổ sung 28/09**: chặn luôn phím `-` khi ô khai `min >= 0` |
| 3. Lịch sử cấu hình cũ → mới | ĐÃ sửa từ 24/09 |
| 4. Bản ghi cũ không cập nhật hạn khi đổi N | **ĐẢO THIẾT KẾ** — xem mục riêng bên dưới |
| 5. Message "Bắt buộc nhập, kiểu số nguyên dương >= 0" | **SỬA 28/09** |
| 6, 7. N = M không hiện cảnh báo | **SỬA 30/09** — xem mục BUG 7 |

### BUG 5 — cái bẫy của vee-validate 2

vee-validate 2 **BỎ QUA mọi rule khi ô để TRỐNG** — chỉ `required` mới chạy. Rule tự viết
`non_negative_integer` không tự lo được phần bắt buộc; cờ `computesRequired` đã thử, **không ăn**.
→ giữ `required` trong chuỗi rule, rồi đặt **riêng câu báo lỗi của `required` cho đúng 2 field**
(`demand_due_days`, `demand_warning_days`) qua `Validator.localize` với khoá `custom`.
`hrm-client` **59288bd47**.

### BUG 4 — ĐẢO THIẾT KẾ: hạn nay theo N CHỤP LÚC TẠO (28/09/2026)

Testcase **TC 004** của QA: đổi N của lĩnh vực 30 → 60 thì **nhu cầu đã có phải GIỮ hạn cũ**, chỉ
nhu cầu tạo SAU mới theo N = 60. Code trước đó làm **ngược lại, và là cố ý** (tính tại chỗ).
User chốt đi theo QA → đảo lại.

- [x] Thêm cột `meeting_investment_demands.due_days_snapshot` + **backfill** trong migration
      `2026_09_28_100000_add_due_days_snapshot_to_meeting_investment_demands.php`
- [x] `MeetingInvestmentDemand::effectiveDueDays()` — một cửa duy nhất lấy N của nhu cầu.
      `NULL` = bản ghi cũ chưa backfill → rơi về N hiện tại (tương thích ngược).
      **Phân biệt với snapshot = 0** (cố ý không đặt thời hạn) — lý do cột phải nullable.
- [x] Ghi snapshot **CHỈ ở nhánh TẠO MỚI**, không đưa vào mảng giá trị dùng chung với nhánh cập nhật.
- [x] Màn danh sách **và** cron cùng đọc `effectiveDueDays()`.

Kiểm trên local, cùng cuộc họp (T = 03/04): nhu cầu cũ snapshot 30 → hạn **03/05**; nhu cầu mới
snapshot 60 → hạn **02/06**. `hrm-api` **677021ec7**.

⚠️ **Deploy phải chạy `php artisan migrate`** — migration có backfill.
⚠️ **Đánh đổi**: từ nay sửa N ở danh mục **không còn gia hạn được** cho nhu cầu đang chạy.

### BUG 7 — ĐẢO QUYẾT ĐỊNH: bỏ điều kiện `N > M` (30/09/2026)

Lần thứ **3** QA báo cùng chuyện (18/09 · 28/09 · 30/09). Hai lần đầu chốt giữ spec, lần này chốt
**làm theo QA**.

Lý do spec không sống được: **M mặc định = 3 mà rất nhiều lĩnh vực cũng đặt N = 3** → cấu hình mặc
định **không bao giờ sinh cảnh báo**. Ai test cũng vấp.

- [x] Bỏ so sánh `N > M` ở `CustomerDemandService::attachDueDate()`
- [x] Bỏ ở `CloseExpiredCustomerDemandsCommand::warningDays()` — nay chỉ còn điều kiện `N > 0`

⚠️ **PHẢI sửa ĐỒNG THỜI 2 nơi** — sửa một bên là giao diện báo một đàng, thông báo gửi một nẻo
(đúng lỗi BUG 8 hồi 22/09).

| Tình huống (M = 3) | Luật cũ | Luật mới |
| --- | --- | --- |
| N = 3 = M, còn 2 ngày | ẩn | **HIỆN** |
| N = 3 = M, hết hạn hôm nay | ẩn | **HIỆN** |
| N = 30 > M, còn 2 ngày | hiện | hiện |
| N = 0 | ẩn | ẩn |

⚠️ **Trái spec #11377** — cần báo lại người viết yêu cầu. `hrm-api` **784982bd9**.

### Cụm chữ "Không giới hạn thời gian hiệu lực" bị cắt (30/09/2026)

QA hỏi "sao mất chữ lực" — ô chỉ hiện tới "thời gian hiệu". **Hệ quả của chính lần đổi chữ** từ
"Không thời hạn" (14 ký tự) sang cụm 31 ký tự hồi 24/09 mà không nới cột.

Đo bằng font của bảng (12px Roboto): cụm rộng **174px**, cộng padding cần **190px**. Cột đang để
160px (màn Lĩnh vực) và 150px (màn Nhu cầu KH), lại thêm `white-space: nowrap` ở ô bảng → cắt kèm
ellipsis.

- [x] Nới cả 2 cột lên **200px** + cho ô xuống dòng (`white-space: normal`). `hrm-client` **0cc4e9f74**.

**Bài học**: đổi nhãn hiển thị dài hơn đáng kể thì phải kiểm lại độ rộng cột — bảng này `nowrap` nên
dài quá là MẤT CHỮ, không phải xuống dòng.

### Checkpoint — 2026-09-30

Vừa hoàn thành: bỏ điều kiện `N > M` ở cả màn danh sách lẫn cron (`hrm-api` **784982bd9**); nới 2
cột hạn nhu cầu lên 200px + cho xuống dòng (`hrm-client` **0cc4e9f74**). Cả 2 commit đang ở nhánh
`develop`, **chưa push**.

Đang làm dở: khôi phục lại chính file `plan.md` này sau sự cố ghi file — phần trước 17/09 không
dựng lại được.

Bước tiếp theo: deploy dev (nhớ `php artisan migrate` cho `due_days_snapshot`), báo QA retest 7 bug
đợt 28/09, và báo người viết spec #11377 việc bỏ điều kiện `N > M`.

Blocked: không có.
