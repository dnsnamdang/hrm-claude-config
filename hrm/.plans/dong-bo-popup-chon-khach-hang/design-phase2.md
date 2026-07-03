# Design Phase 2 — Phân quyền hiển thị KH theo Ownership (TH1/TH2/TH3)

Nguồn spec: `phan_quyen.xlsx` (= Google Sheet yêu cầu gốc, tab "phan quyen khach hang") — 2026-07-02.

## 4 quyết định user đã chốt (2026-07-02)

1. **TH3-B2C ẩn áp cho CẢ 3 màn** (danh sách chính + popup Meeting + popup TKT).
2. **TH2-B2C search đúng SĐT**: HIỆN dòng KH + thông báo "Đã có người đăng ký nên bạn không được phép chọn" — không cho chọn.
3. **Quyền cấp cao**: THẤY theo quyền ERP (quản lý vẫn thấy KH trong phạm vi), nhưng CHỌN theo ownership — chỉ người đang đăng ký mới chọn được KH đang trong hạn đăng ký; KH đang đăng ký bởi người khác thì kể cả quản lý cũng bị chặn chọn.
4. **Làm cả 2 khối trong 1 đợt**: rule mức KH + rule droplist người liên hệ B2B.

## Dữ liệu nền (đã xác minh)

- ERP `customer_registers`: `customer_id`, `customer_contact_id`, `employee_id` (ERP), `quotation_id`, `firm_quotation_id`, `expired_date` (date), `note`. Hiện có 2.028 bản ghi, 25 còn hạn.
- Đăng ký còn hạn = `expired_date >= hôm nay`.
- Tương tác: báo giá ERP (4 bảng quotations, created_by=ERP emp id) + `meetings` (HRM, customer_id) + `prospective_projects` (HRM, customer_id).
- Map user: HRM `TpEmployee.employee_info_id` ↔ ERP employee (helper `resolveErpEmployeeIdFromHrm` / `ErpPermissionHelper::erpEmployeeId()` có sẵn).

## Phân loại (tính theo user hiện tại, cho KH CÁ NHÂN — customer_type=1)

- **TH1 — của mình/có tương tác**: (a) có đăng ký còn hạn của CHÍNH user; HOẶC (b) KH do user tạo (`customers.created_by`); HOẶC (c) user từng phát sinh báo giá ERP / Meeting / Dự án TKT với KH (creator). *(Giả định: "tương tác" tính theo creator bản ghi — xác nhận thêm nếu cần tính cả thành viên meeting.)*
- **TH2 — của Sales khác**: tồn tại đăng ký CÒN HẠN của người khác trên KH → chặn CHỌN với mọi user (kể cả quản lý/TH1-c), hiện + báo khi search đúng SĐT.
- **TH3 — tự do**: không rơi vào TH1/TH2 (chưa ai đăng ký còn hạn, chưa từng tương tác với user) → mặc định ẨN ở cả 3 màn; chỉ hiện khi search đúng full SĐT (cơ chế `phone_exact_bypass` hiện có); chọn được bình thường.

Hiển thị B2C = (TH1 của user) OR (trong phạm vi quyền cấp ERP — nhánh báo giá scope hiện có, "thấy theo quyền") OR (search đúng full SĐT). KH cá nhân tự do (chưa tương tác với ai) không lọt nhánh nào → tự khắc ẩn, kể cả với "Xem tất cả khách hàng" (chốt 1 áp cho cả 3 màn).

KH DOANH NGHIỆP (type 2-5): hiển thị công ty giữ nguyên theo quyền ERP (tìm MST/tên như hiện tại). Rule áp ở NGƯỜI LIÊN HỆ (customer_contacts + customer_registers.customer_contact_id):
- Contact TH1 (mình đăng ký/thêm/tương tác): hiện sẵn tên + SĐT trong droplist, cho chọn.
- Contact TH2 (người khác đăng ký còn hạn): hiện trong droplist nhưng DISABLE + tooltip/báo "Đã có người đăng ký..."; search đúng SĐT cũng báo tương tự.
- Contact TH3 (tự do): ẩn khỏi droplist mặc định, buộc nhập đúng full SĐT (ô search trong droplist) mới hiện + chọn được.

SĐT hiển thị: TH1 hiện RÕ số thật (thay hardcode '-' trong CustomerListResource bằng check ownership); TH2/TH3/theo-quyền hiện '-'.

## Thay đổi dự kiến

### BE (hrm-api, Modules/Assign)
- Helper mới `CustomerOwnership` (app/Helper hoặc Service): `classify($customerIds)` → map id→{th, register_owner, is_mine} (batch, tránh N+1); `classifyContacts($contactIds)`; cache per-request.
- `CustomerService::index`: thêm lớp lọc B2C theo công thức trên (thay thế vai trò hide_individual cũ); trả kèm cờ `ownership_th`, `can_select`, `register_note` trong CustomerListResource; SĐT rõ khi TH1.
- Validate khi LƯU Meeting + Dự án TKT (FormRequest withValidator): customer_id / contact được chọn rơi vào TH2 → 422 "Đã có người đăng ký...".
- API contacts theo customer (droplist người liên hệ) trả kèm cờ ownership + lọc TH3.

### FE (hrm-client)
- `ChooseErpCustomerModal.vue`: row TH2 → style khóa + click hiện toast/băng rôn "Đã có người đăng ký nên bạn không được phép chọn" (không emit chọn).
- Màn `/assign/customers` (index.vue): danh sách tự áp rule qua BE (không sửa nhiều); hiện SĐT rõ TH1.
- Droplist người liên hệ ở form Meeting (GeneralInfo) + TKT (CustomerBlock): disable contact TH2 + báo; contact TH3 chỉ hiện khi search đúng SĐT.

### Không đụng
- Quyền ERP `applyErpVisibilityScope` giữ nguyên (lớp 1). Không migration (dùng bảng ERP sẵn). Không permission mới. Không git.

## Edge cases
- KH có nhiều đăng ký: lấy đăng ký còn hạn mới nhất; hết hạn → rơi về TH3/TH1-c.
- User vừa là người đăng ký vừa hết hạn → TH1-a mất, còn TH1-c (đã từng tương tác qua báo giá gắn register? báo giá vẫn tính).
- `customers.mobile` nhiều số cách nhau dấu phẩy — cơ chế so khớp exact hiện có đã xử lý (CONCAT/REPLACE).
- Meeting/TKT cũ đã gắn KH TH2 → chỉ chặn khi CHỌN MỚI/đổi KH, không chặn xem/sửa field khác.


## Kết quả triển khai (2026-07-02 — CODE DONE + VERIFIED)

- HRM BE: `hrm-api/app/Helper/CustomerOwnership.php`; `CustomerService::index` + `applyB2cOwnershipVisibility` + `applyErpVisibilityScope` (nhánh của-mình); `CustomerListResource` (register_locked, SĐT rõ TH1); `customerContacts` (locked + nhánh đăng ký/báo giá); `show()` contacts kèm locked; validate 422 ở `ProspectiveProjectRequest` + `MeetingCreateApiRequest` + `MeetingUpdateApiRequest`.
- HRM FE: `ChooseErpCustomerModal` (badge + chặn click); `GeneralInfo` (guard droplist + fix auto-fill bỏ contact khóa); `CustomerBlock` (guard droplist).
- ERP (yêu cầu bổ sung "quy tắc hiển thị ERP = HRM"): `TanPhatDev/app/Services/CustomerOwnership.php` + `Customer::searchByFilter` áp `applyB2cVisibility` — B2C tự do ẩn, ô MST/SĐT khớp đúng full SĐT thì hiện; đọc HRM meetings/TKT qua connection `hrm` (map user 2 hệ bằng employee_info_id, try/catch để HRM lỗi không chặn ERP).
- Verify: tinker 2 hệ + HTTP 422 + Playwright E2E — chi tiết trong plan.md. Tổng B2C hiển thị: HRM 41.209→16.619; ERP 16.971.
- CÒN MỞ: ERP đang hiện SĐT RÕ trên danh sách — có áp che '-' theo TH1 như HRM không (đụng blade ERP + nghiệp vụ ERP hiện tại)?
