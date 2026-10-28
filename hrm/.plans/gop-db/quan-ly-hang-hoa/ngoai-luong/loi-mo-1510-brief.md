# Brief sửa lỗi mở 15/10 (N79 N82 N84 N85 N86 N87 N91 N97 N98 N99)

Khảo sát gốc: `khao-sat-loi-mo-1510.md` (cùng thư mục) — đọc mục của mã mình làm. **User đã nói "Làm" 15/10** cho đúng phạm vi dưới đây.

## Chốt của user (15/10)
- **N79**: sửa đúng logic — đổi gán `$service` chưa khai báo thành `$product_item` (`WrServiceQuotation.php` ~1072, ~1308). So thử vài báo giá dịch vụ trước/sau (đọc, không lưu dữ liệu thật).
- **N82**: mặc định `show_children = 1` khi thiếu (stdClass báo giá trực tiếp trong `QuotationController::exportExcel` + `BomListExport.php:546` `?? 0` → `?? 1`).
- **N84**: migration index ghép `(product_id, life_id)` cho `product_vehicle_model_has_life`, CHẠY vào `hrm_erp_giacty` (chỉ migration này, `--path` đúng file), EXPLAIN trước/sau.
- **N85**: `ProductFormGallery.vue` hiện cả lỗi `galleries.N`.
- **N86**: `itemSearch` thêm tham số `exclude_locked` (bỏ hàng pcc status 4 ở công ty đang làm); CHỈ 2 chỗ chọn hàng kèm theo ở form hàng hoá truyền; ô lọc "Máy" của picker giữ nguyên.
- **N87**: cả 7 chỗ `.text-muted` trong `components/product/form` → class xám chuẩn của repo (đo `getComputedStyle` màu).
- **N91**: `AdminData::source` + `mediaAndGuarantee` bỏ dòng hệ số `status` NULL (đồng bộ luật ERP).
- **N97**: vá `no_set` ở `OrderRequestProduct2` + `InlandOrderRequestProduct2` (áp cả màn `inland_order_request2`); ẩn nút "Tạo" màn TN mới (thiếu create/edit — làm sau, ghi mã mới).
- **N98**: `Customer.blade.php` coi SĐT NULL là rỗng (KH 232387). KH 1000: CHỈ khảo sát bằng trình duyệt (đọc), ghi nguyên nhân; KHÔNG sửa — báo lại.
- **N99**: tái hiện bằng Playwright trình duyệt thật (bấm select2 thật, phát change); chỉ sửa nếu tái hiện được; không tái hiện ⇒ ghi bằng chứng, đóng.

## Quy tắc chung
- Nhánh con từ nhánh chung, xong merge `--no-ff` LOCAL về nhánh chung, soát marker xung đột, KHÔNG push / stash / đổi nhánh worktree khác. Commit cuối message:
  `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>` / `Claude-Session: https://claude.ai/code/session_014JQzu8PhMym1qvYWURxtd3`
- Giữ EOL (kiểm `git diff --numstat`); comment tiếng Việt; không dùng prop `trim`.
- PHP `/opt/homebrew/opt/php@7.4/bin/php`; trước artisan/phpunit: `ls bootstrap/cache/config.php` không tồn tại + `php artisan config:clear`.
- Dữ liệu thử / role tạm trên `hrm_erp_giacty` được phép, ghi id, xoá đúng id, đếm lại mốc. Role tạm HRM: roles + role_has_permissions (company_id=1) + employee_has_roles (company_id, model_type `Modules\Timesheet\Entities\Employee`), `php artisan cache:clear` ở hrm-api.
- Không đụng server 8031/3031 (đang chạy từ worktree). ERP: `php artisan serve --port=8090`, kill đúng PID. Không pkill theo tên. Không dispatch subagent. Không sửa CLAUDE.md/cấu hình.
- Lỗi mới ngoài phạm vi: ghi report, mã từ **N112**, không vá.

## Đợt bổ sung (15/10) — user nói "Làm"
Chốt user: N79 VAT DV bảo hành giữ theo danh mục chi phí (không sửa thêm). N113, N115 để sau.
- **(a) hrm-api** nhánh con `feat/cdhh-loi-mo-2-api` từ `feat/chuyen-doi-hang-hoa`: **N112** — `AdminData::formValues` (tab Quản trị form sửa hàng) bỏ dòng hệ số `status` NULL, rơi về thông tin chung của hàng, đúng luật N91/ERP `adminRowFor`. PHPUnit (form giá trị = màn chi tiết với dòng NULL). Bộ `Modules/MasterData` (mốc 553).
- **(b) hrm-client** nhánh con `feat/cdhh-loi-mo-2-fe`: **N114** — form hàng hoá nhận 422 từ BE ⇒ cuộn + focus ô lỗi đầu tiên (tái hiện trước: lỗi y=1368 khung 900; marker `.v2-error` vs `.invalid-feedback` — xem memory); **N116** — `ChooseErpCustomerModal` bỏ khai trùng `fields` (data vs computed), popup vẫn đủ cột, console sạch. Playwright đo DOM, cập nhật spec (`products-form-loimo-ui.spec.ts` hoặc spec liên quan), chạy riêng `--workers=1`.
- **(c) ERP** nhánh con `feat/cdhh-loi-mo-2-erp` từ `feat/2d1-erp-khong-loi`: **N120** — màn TN mới ẩn nút Sửa/Xoá (danh sách) + Duyệt/Huỷ/Lưu ý kiến (chi tiết) ⇒ màn chỉ xem + in; sửa luôn comment N97 đang ghi "(N112)" thành "(N120)". **N121** — `show_.blade.php` chi tiết KH: vòng `.date-model` không ném lỗi khi `contactToAdd` chưa có (KH loại ≥ 2, vd KH 1000); kiểm form thêm người liên hệ (không lưu) ô ngày sinh vẫn định dạng. PHPUnit ERP cả bộ (mốc 191) + Playwright 8090.
Lỗi mới: mã từ **N122**.
