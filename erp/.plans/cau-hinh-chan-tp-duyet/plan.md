# Testcase — Cấu hình chặn luồng quá hạn: Chặn trưởng phòng (Tab 2)

## Phạm vi
Testcase cho **màn cấu hình** `admin/due_configs/edit` › Tab 2 "Chặn trưởng phòng duyệt" (bật/tắt chặn TP duyệt từng phiếu theo từng công ty). KHÁC với feature `chan-tp-duyet-qua-han` (đó là testcase enforcement middleware, không gồm màn cấu hình).

## Nguồn tham chiếu (code)
- Controller: `app/Http/Controllers/Common/DueConfigsController.php` (edit/update — diff pivot + ghi history)
- View: `resources/views/common/due_configs/edit.blade.php` (Tab 2: sub-tab công ty × lưới 31 checkbox)
- Bảng: `due_configs` (tab=2, id 22–52), `company_due_configs` (pivot), `due_config_histories`
- Route: `due_configs.edit` / `due_configs.update` (KHÔNG checkPermission — vào qua menu)
- Enforcement liên quan (E2E): `DueConfigBlockService::isManagerBlocked` + middleware `checkDueConfigsManager`

## Output
- `generate-testcase.py` — generator theo skill testcase-documenter
- `testcase.xlsx` — **31 TC**, P0 42%, 5 section (I/V/VI/VII/VIII), đủ 9 mục mô tả + Test Summary + 3 cột check dropdown

## Cấu trúc 5 section
- I. Hiển thị trang & truy cập — 8 TC
- V. Chức năng chính (tick/lưu cấu hình) — 8 TC
- VI. Edge cases & validation — 7 TC
- VII. Cô lập dữ liệu & bảo mật — 4 TC
- VIII. E2E — cấu hình tác động tới chặn duyệt — 6 TC

(Không có section TC-ROLE: màn không có permission code riêng.)

## Tasks
- [x] Khảo sát màn cấu hình + 31 mục tab=2 + luồng lưu (diff pivot + history)
- [x] Viết generator + sinh testcase.xlsx (31 TC)
- [ ] User review nội dung, chỉnh số liệu mẫu/tên công ty thực tế nếu cần

### Checkpoint — 2026-06-29
Đã sinh `testcase.xlsx` (31 TC) cho màn cấu hình "Chặn trưởng phòng" Tab 2. Chờ user review.
