# Báo giá đã duyệt — sửa trường hành chính không phải duyệt lại

**Phụ trách:** @khoipv
**Bắt đầu:** 25/09/2026
**Phạm vi:** chỉ BE (`QuotationService::update()`), màn Báo giá

## Bối cảnh

`Quotation::canEdit()` cho phép người lập sửa báo giá khi đang `3 DA_DUYET`. FE `edit.vue` gửi thẳng
`status` theo nút bấm (**Lưu** → `1 DANG_TAO`, **Lưu và gửi** → `2 CHO_DUYET`) nên báo giá đã duyệt
mà chỉ sửa vài trường hành chính cũng bị rớt trạng thái + bắn thông báo "cần trưởng phòng duyệt".

Yêu cầu: sửa **chỉ** các trường dưới đây thì **giữ nguyên `3 DA_DUYET`**.

| Nhóm | Field |
|---|---|
| Tab Tiến độ thực hiện | `result`, `reason`, bảng `quotation_attachments` |
| Tab Thư mời báo giá | `info`, `receiver_time`, `request_complete_time`, `complete_time`, `khclnt`, `public_hsmt_time`, bảng `quotation_attachment_invitations` |

## Phase 1 — BE

- [x] `QuotationService`: thêm hằng `APPROVAL_INSENSITIVE_FIELDS` (whitelist + cột suy ra + cột hệ thống tự ghi + cột chụp từ danh mục)
- [x] `QuotationService::approvalSignature(Quotation)` — dấu vân tay `quotations` + 5 bảng con, bỏ `id`/khóa cha/timestamps
- [x] `QuotationService::normalizeSignatureValue()` — chuẩn hoá số + `''` → `null`
- [x] `QuotationService::update()` — chụp signature trước, chạy luồng cũ, chụp lại; giống nhau + đang `DA_DUYET` → ép `status = DA_DUYET` + `$request->merge(['status' => DA_DUYET])`
- [x] Chuyển `sendNotificationQuotation()` xuống SAU bước quyết định trạng thái
- [x] `php -l`

## Phase 2 — Test UI

- [ ] Báo giá `3 Đã duyệt` → sửa bảng Tiến độ thực hiện → **Lưu** → vẫn `Đã duyệt`, TP không nhận thông báo
- [ ] Sửa `result` / `reason` → vẫn `Đã duyệt`
- [ ] Sửa 5 trường tab Thư mời + bảng file thư mời → vẫn `Đã duyệt`
- [ ] Bấm **Lưu và gửi** mà chỉ sửa trường trong danh sách → vẫn `Đã duyệt` (user chốt)
- [ ] Sửa số lượng / đơn giá / hàng hóa → rớt trạng thái như cũ (`Lưu` → Đang tạo, `Lưu và gửi` → Chờ duyệt)
- [ ] Đổi khách hàng → rớt trạng thái như cũ
- [ ] Báo giá đang `1 Đang tạo` / `5 Bị từ chối` → hành vi không đổi
- [ ] `total_amount` + `Project.quotation_total_amount` vẫn đúng sau khi sửa (bẫy cache relation)

## Quyết định (user chốt)

- "Tiến độ thực hiện" = **cả tab**: bảng tiến độ + ô `result` (Kết quả) + ô `reason` (Lý do).
- Bảng **File đính kèm của tab Thư mời** (`attachment_invitations`) **CÓ** tính vào danh sách.
- Bấm **Lưu và gửi** mà chỉ sửa trường trong danh sách → **vẫn giữ Đã duyệt** (quy tắc bám theo
  "sửa gì" chứ không bám nút bấm) → không sinh thông báo cần duyệt.

## Ghi chú kỹ thuật

- So dấu vân tay **trước/sau trên cùng DB** (không so payload với DB) để tránh lệch định dạng
  ngày/số/thứ tự key giữa FE và DB.
- Bỏ khỏi signature các cột **chụp sống từ danh mục** (`customer_name/code/phone/address`,
  `customer_area_name`, `customer_group_name`, `customer_province_name`, `customer_last_used_name`,
  `array_product_name`, `product_group_name`): `DetailQuotationResource` trả các cột này lấy từ
  `category_customers` rồi FE gửi lại → danh mục đổi tên sau ngày duyệt sẽ tự cập nhật dù người lập
  không sửa. Đổi khách thật thì `customer_id` / `customer_contact_id` đổi — 2 cột này VẪN trong
  signature nên không lọt.
- Bỏ `expected_time` (BE tự ghi theo `request_complete_time`) và `total_amount` (tính từ products —
  products đã nằm trong signature).
- ⚠️ Signature phải query bằng model query builder, **KHÔNG** chạm relation `$quotation->products`:
  chạm sẽ cache bản trước khi sync, làm `total_amount = $quotation->products->sum('amount')` ở dưới
  tính sai.
- `$request->merge(['status' => DA_DUYET])` là bắt buộc vì `sendNotificationQuotation()` đọc
  `$request->status`, không đọc `$quotation->status`.
- KHÔNG đụng `store()`, `render()`, `canEdit()`, không migration, không sửa FE → không cần build client.

## Ngoài phạm vi

- Màn sửa vẫn hiện đủ 4 nút kể cả khi báo giá đã duyệt (chưa ẩn "Lưu và gửi").
- Không áp dụng cho màn Hợp đồng / Gói thầu.


## Kết quả verify trên DB `thanhan_stag_07052026` (25/09/2026)

Verify bằng tinker, mọi kịch bản chạy trong transaction rồi `rollBack()` — đã đối chiếu lại DB:
0 `notifications` / 0 `jobs` mới trong 15 phút, `BG-335` vẫn `status=3`, không sót dòng test.

**Vòng 1 — dấu vân tay (12/12 PASS)** trên `BG-335`:

| Kịch bản | Kết quả |
|---|---|
| Chụp 2 lần liên tiếp | giống nhau ✅ |
| Sửa `result`/`reason`/`info`/4 cột ngày/`khclnt` | giữ nguyên ✅ |
| Thêm dòng bảng Tiến độ thực hiện | giữ nguyên ✅ |
| Thêm file đính kèm tab Thư mời | giữ nguyên ✅ |
| Sửa cột chụp từ danh mục + `total_amount` + `approved_time` | giữ nguyên ✅ |
| Đổi số lượng / đơn giá / xóa dòng hàng hóa | đổi ✅ |
| Trả lại số lượng cũ | giữ nguyên ✅ |
| Đổi `customer_id` / `budget_code` | đổi ✅ |

**Vòng 2 — end-to-end `update()` với payload thật** (lấy nguyên output `DetailQuotationResource`
làm payload, đúng như FE nạp form rồi gửi lại):

| Kịch bản | Nút | status sau | Đúng? |
|---|---|---|---|
| Không sửa gì | Lưu | 3 | ✅ |
| Không sửa gì | Lưu và gửi | 3 | ✅ |
| Sửa Kết quả + Lý do | Lưu | 3 | ✅ |
| Sửa 6 trường tab Thư mời | Lưu và gửi | 3 | ✅ |
| Thêm dòng Tiến độ (không file) | Lưu | 3 | ✅ |
| Thêm file đính kèm tab Thư mời | Lưu | 3 | ✅ |
| Đổi số lượng hàng hóa | Lưu | 1 | ✅ |
| Đổi số lượng hàng hóa | Lưu và gửi | 2 | ✅ |
| Đổi nguồn kinh phí | Lưu | 1 | ✅ |
| Báo giá đang `1 Đang tạo` | Lưu và gửi | 2 | ✅ (không đổi hành vi) |

Quan trọng: kịch bản "không sửa gì" ra `status=3` chứng minh **round-trip qua
`DetailQuotationResource` không tự sinh thay đổi giả** — đây là rủi ro lớn nhất của cách so sánh này.

**Vòng 3 — thông báo:**

| Kịch bản | status | notifications mới | jobs mới |
|---|---|---|---|
| Chỉ sửa Lý do + Lưu và gửi | 3 | 0 | 0 |
| Không sửa gì + Lưu và gửi | 3 | 0 | 0 |
| Đổi số lượng + Lưu và gửi | 2 | 1 | 2 |

→ Giữ Đã duyệt thì TP **không** nhận thông báo "cần trưởng phòng duyệt"; có thay đổi thật thì vẫn nhận.

`total_amount` và số dòng hàng hóa đúng ở mọi kịch bản → không mắc bẫy cache relation.

### Checkpoint — 25/09/2026
Vừa hoàn thành: Phase 1 BE (1 file `Modules/Category/Services/QuotationService.php`) + verify 3 vòng
trên DB stag, tổng 25 kịch bản đều đúng, DB đã dọn sạch.
Đang làm dở: (không)
Bước tiếp theo: Phase 2 — test UI thật trên màn `plan/quotation/_id/edit` với tài khoản người lập.
Blocked:
