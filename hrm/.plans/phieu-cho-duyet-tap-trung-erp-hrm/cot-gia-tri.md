# Cột "Giá trị" — từng loại phiếu (từ code hrm-api / hrm-client đang chạy) — @cuong61n

Ngày 15/11/2026. Khảo sát 3 lượt đọc code (Tài chính · Công việc · còn lại). Ký hiệu: **VND** = số đã quy đổi VND · **NT** = nguyên tệ, phải kèm mã tiền · **SUM** = BE phải cộng từ bảng dòng lúc `sync()` (lưu sẵn vào registry) · **che** = BE phải che theo quyền.

## 1. Quy tắc chung của cột
- Hiện số tiền chính + mã tiền nhỏ (VND/USD), căn phải. Loại không có tiền, hoặc người xem không có quyền xem giá → `—` (hợp đồng bị che hiện `*****` như màn gốc).
- KHÔNG sắp xếp, KHÔNG cộng tổng cột: khác loại, khác tiền tệ, và có loại là điểm công khoán (không phải tiền).
- Cột tuỳ chọn, mặc định ẩn (bật ở Cấu hình cột). Rê vào icon ⓘ ở tiêu đề xem giải thích (info-popover); nhãn riêng từng loại ("Số tiền đề nghị"…) lưu ở `amount_label`.
- BE trả số THÔ, FE định dạng `toLocaleString('en-US')` (BE phiếu chi đang trả chuỗi kiểu VN `number_format(…,',','.')` — màn này KHÔNG dùng chuỗi đó).
- Điểm công khoán (Quyết toán công khoán, Giao việc, Duyệt kết quả giao việc) KHÔNG đưa vào cột này (khác đơn vị) → `—`.

## 2. Loại CÓ giá trị
| Loại phiếu | Lấy số nào (bảng · cột) | Đơn vị | Che theo quyền | Ghi chú |
|---|---|---|---|---|
| Đề nghị thanh toán | SUM `bill_payment_request_details`, cột theo cấp như `BillPaymentRequestListResource::MONEY_COLUMN_BY_STATUS` (status 2 `payment_money_request`; 3 `_manage`; 4–5 `_accountant_debt`; 6–8 `_chief_accountant`) | NT (+ `type_money_id`) | Không | Số = của CẤP TRƯỚC (mirror list hiện tại). ⚠ Bảng ánh xạ list ≠ Service: BGĐ không thấy số KT trưởng vừa chỉnh → CẦN CHỐT |
| Đề nghị thu tiền | SUM `income_money_request_exchange` | VND | Không | 1 cấp KT |
| Yêu cầu hạch toán bổ sung | `addition_accounting_requests.money` | NT (+ `currency_code`) | Không | Loại 2, 6 đã ghi sẵn tổng |
| Yêu cầu điều chỉnh công nợ | `bill_adjust_dept_requests.total_amount` | VND (đã quy đổi) | Không | |
| Phiếu chi | `bill_payments.sum_payment_money_approve_exchange` | VND | Không | Thủ quỹ sửa số duyệt khi duyệt (có trần) |
| Phiếu thu | `bill_incomes.sum_money` | VND | Không | Số thực thu ở dòng chi tiết, không đổi `sum_money` |
| Quyết toán thưởng cuối năm | SUM `bonus_fund` (tổng quỹ thưởng) | VND (chưa xác minh tiền tệ) | Không | `total_approved` = 0 khi chờ BGĐ |
| Báo giá | `quotations.total_after_vat` | NT (+ `currency_code`) | Không che tổng (chỉ che giá vốn/biên lãi) | Chưa nhân tỷ giá; cấp duyệt tính theo số trước VAT × tỷ giá |
| Hợp đồng (TKT) | `hrm_contracts.total_after_vat` (+ `total_extra_amount` là lý do cần BGĐ) | Chưa xác minh (có `currency_id`, FE ghi cứng VND) | **CÓ — `hide_price`** (quyền `sale.hop_dong_an_gia.view` + phạm vi): ngoài phạm vi → `*****`, và không duyệt được | Phải giữ cơ chế này |
| Đề nghị thanh toán công tác phí | SUM 4 khoản (đi đường + công tác phí + lưu trú + khác) | VND | Không | BE CHƯA có tổng (FE cộng) → BE tự cộng; số theo cấp: TP sửa rồi KT; chọn "thực tế/duyệt" |
| Duyệt kết quả công tác | SUM 4 cột `total_cost_*` của `assign_requests` | VND | Không | BE chưa có tổng; chưa rõ bước này dùng số dự trù hay số kết quả |
| HĐ dịch vụ SC-BD-BT | `wr_service_contracts.total_after_vat` | VND | Không (tên quyền gây hiểu nhầm) | |
| Chuyến xe khác | `other_delivery_trips.total_cost_transition` (cước thực tế) | VND | Không | |
| Phiếu đăng ký bảo hiểm | SUM `insurance_register_types.total_fee` | VND | Không | |
| Quyết định khen thưởng | `decision_rewards.total_amount` (đề xuất); có `_reviewed`, `_approved` theo bước | VND | Không | Màn chờ duyệt Quyết định hiện chỉ khi lọc đúng loại → registry phải lưu sẵn |
| Quyết định cử đi đào tạo | `assign_trainings.total_cost_course_training_manager_approve` | VND | Không | |
| Đề xuất đào tạo | đơn giá/người × số học viên theo cấp: `person_cost_course` → `_department_head_approve` → `_training_manager_approve` | VND | Không | Không có cột tổng; BE SUM (`TrainingRequestController.php:527`) |
| Khoá học | SUM `course_cost_payments` theo cấp: `cost` → `cost_department_head_approve` → `cost_director_approve` | VND | Chưa xác minh quyền `training.chi_phi.manage` | |
| Đề xuất khoá học · Kế hoạch đào tạo | SUM bảng dòng chi phí | VND | Chưa xác minh | Chưa có số tổng ở list; giai đoạn 2 |

## 3. Loại KHÔNG có giá trị (hiện —)
- Điểm công khoán, không phải tiền: Quyết toán công khoán theo HĐ, Giao việc, Duyệt kết quả giao việc.
- Không thành 1 con số: Duyệt giá bán hàng hoá (giá theo hàng × loại giá + giá vốn bị che) — link sang màn riêng; Chỉ tiêu kinh doanh (chỉ tiêu mục tiêu, không phải tiền chi/thu).
- Có lương nhưng chỉ ở màn chi tiết, nhạy cảm: các quyết định tiếp nhận, ký HĐLĐ, bổ nhiệm, điều chuyển, điều chỉnh lương → `—` (đề xuất, chưa có quy định trong code).
- Phiếu nhập kết quả CSKH (không có số tổng đáng tin) và mọi phiếu chấm công / nhân sự / quyết định không có tiền.
- Giao công tác: có 4 cột dự trù chi phí nhưng list không hiện → giai đoạn 2 (tài liệu đánh giá cũ ghi "không có tiền" là chưa đúng).

## 4. Phát hiện ảnh hưởng phạm vi màn
- **Quyết toán thưởng năng suất quý: HRM không có bước "Chờ duyệt"** (`FORM_STATUSES = [1,3]`, người tạo tự duyệt phiếu Đang tạo) → bỏ khỏi màn tổng hợp. Chưa kiểm dữ liệu DB còn phiếu status 2 không.
- Phiếu chi: BE trả `*_text` kiểu VN (trái quy ước số) — dùng số thô.

## 5. Quyết định cần user chốt
1. Đề nghị thanh toán: hiện số của CẤP TRƯỚC (như list hiện tại) hay số cấp vừa chỉnh?
2. Hợp đồng TKT: tiền tệ thật (có HĐ ngoại tệ không)?
3. Giai đoạn 1 làm các loại nào: đề xuất Tài chính + Báo giá + Hợp đồng TKT (số rõ nhất); nhóm đào tạo/quyết định để giai đoạn 2.
