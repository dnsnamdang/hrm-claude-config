# Plan — Dự án TKT: trường ngày (Redmine #11310)

Người phụ trách: @khoipv · Nhánh: `fix-bug-11092026` (`hrm-client` + `hrm-api`)

## Phase 1 — FE

- [x] T1. Đổi nhãn `Ngày bắt đầu dự án` → `Ngày bắt đầu dự án TKT`
      (`components/ProgressFinanceSection.vue:37`)
- [x] T2. Đổi nhãn `Ngày kết thúc dự án` → `Ngày kết thúc dự án TKT` (cùng file, dòng 51)
- [x] T3. Khoá ô `Ngày bắt đầu dự án TKT` (`:disabled="true"`) — ăn cho cả 4 màn dùng component:
      Tạo mới, Sửa, Chi tiết, tab TKT của Yêu cầu giải pháp
- [x] T4. Màn Tạo mới: `formSubmit.start_date` mặc định = ngày hiện tại
      (`add.vue` — helper `todayISO()`, gán trong `data()`)
- [x] T5. Thêm icon `(i)` + `b-popover` cạnh nhãn `Ngày kết thúc dự án TKT`
      (chuẩn `info-icon-tooltip` mục 2: `ri-information-line` 14px `#94a3b8`,
      `custom-class="info-popover"`, `triggers="hover focus"`, `placement="bottom"`)

## Phase 2 — Gỡ thế kẹt do khoá trường (phát sinh, ngoài mô tả Redmine)

Khoá `Ngày bắt đầu dự án TKT` làm dự án **nháp tạo từ hôm trước** không lưu lại được:
rule "ngày bắt đầu không được ở quá khứ" vẫn nổ mà user không còn cách nào dời ngày.

- [x] T6. FE: bỏ kiểm tra "ngày bắt đầu >= hôm nay" trong `validateTimelineDates()`
- [x] T7. FE: lỗi cặp bắt đầu/kết thúc luôn báo ở `Ngày kết thúc dự án TKT`
      (trường duy nhất còn sửa được)
- [x] T8. BE: bỏ `after_or_equal:today` cho riêng `start_date`
      (`Modules/Assign/Http/Requests/ProspectiveProject/ProspectiveProjectRequest.php:17`);
      `end_date` / `customer_need_solution_date` / `internal_solution_close_date` giữ nguyên
- [x] T9. Kiểm tra biên dịch: `vue-template-compiler` + `@babel/parser` (2 file .vue) và `php -l` (1 file PHP)

## Chờ xác nhận

- [ ] T10. **Dự án con có cha bắt đầu ở tương lai**: `ProspectiveProjectRequest::withValidator()`
      bắt `start_date >= parent.start_date`. Ngày bắt đầu giờ cứng = hôm nay và không sửa được
      → tạo dự án con cho cha bắt đầu ngày mai trở đi sẽ **luôn báo lỗi, không có đường gỡ**.
      Cần BA chốt: (a) bỏ rule này, (b) dự án con lấy mặc định = `parent.start_date` thay vì hôm nay,
      hay (c) giữ nguyên và chấp nhận chặn.

## Nghiệm thu (theo Redmine) — chưa chạy trên trình duyệt

- [ ] AC1. Màn Tạo mới hiện đúng 2 nhãn mới
- [ ] AC2. Màn Tạo mới: `Ngày bắt đầu dự án TKT` = ngày hôm nay, không sửa/không mở lịch được
- [ ] AC3. Màn Sửa: hiện đúng ngày bắt đầu đã lưu, vẫn bị khoá, và **lưu lại được**
      (kể cả dự án nháp tạo từ hôm trước)
- [ ] AC4. Có icon `(i)` cạnh `Ngày kết thúc dự án TKT` ở cả Tạo mới và Sửa
- [ ] AC5. Hover icon `(i)` hiện đúng câu
      "Ngày dự kiến chốt báo giá cuối cùng để chuyển sang giai đoạn ký hợp đồng",
      rê chuột ra thì tooltip tự ẩn

### Checkpoint — 2026-09-11
Vừa hoàn thành: T1–T9 (code FE + BE, đã biên dịch sạch).
Đang làm dở: không.
Bước tiếp theo: user mở trình duyệt chạy AC1–AC5; hỏi BA về T10 (dự án con vs khung thời gian cha).
Blocked: T10 chờ BA.
