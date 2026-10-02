# Đồng bộ tên thành phần lương với Bảng công chi tiết — Redmine #11328

**Người phụ trách:** @junfoke
**Nhánh:** `tpe-develop-assign` (hrm-api + hrm-client)
**Nguồn yêu cầu:** Redmine [#11328](http://quanly.dnsmedia.vn/issues/11328) — Nguyễn Huyền, 07/09/2026
**Trạng thái duyệt:** khách đã duyệt bảng đối chiếu ngày 08/09/2026 (file `Phản hồi_ Xác nhận tên thành phần lương.xlsx`)

## Mục tiêu

Tên thành phần lương ở màn *Tính lương › Danh mục thành phần lương của hệ thống* đang khác chữ với
tiêu đề cột ở màn *Chấm công › Bảng công chi tiết trong tháng*, khiến người làm lương không đối chiếu
được hai màn với nhau. Sửa tên (và mô tả cách tính) cho khớp, đồng thời bổ sung các thành phần lương
còn thiếu so với bảng công.

## Hiện trạng kỹ thuật (đã rà code)

Tên thành phần lương đi qua **3 lớp copy độc lập**:

| Lớp | Bảng / cột | Sinh ra khi |
| --- | --- | --- |
| Danh mục hệ thống | `system_salary_compositions.name` | `SystemSalaryCompositionSeeder` |
| Danh mục của công ty | `salary_compositions.name` | bấm "đưa vào danh sách sử dụng" (`SalaryCompositionController::addFromSystemSalary`) |
| Mẫu bảng lương → bảng lương | `salary_template_compositions.display_name` → `salary_employee_data.display_name` | snapshot lúc tạo mẫu / tạo bảng lương |

Hệ quả (khớp đúng mô tả của khách): đổi `name` thì **mẫu và bảng lương đã tạo giữ tên cũ**, chỉ mẫu và
bảng lương **tạo mới** mới lấy tên mới.

**Đổi tên không phá công thức lương** — công thức thay biến theo `code`, không theo `name`
(`CreateEmployeePayroll::replaceSystemData` dùng `preg_quote($code)`).

**Tiền lệ trong repo:** `2026_08_04_000001_rename_tong_vdm_quy_doi_salary_composition.php` — migration
data-only, đổi theo `code`, và chỉ đổi bản copy của công ty khi người dùng **chưa tự sửa tên**
(`where('name', $oldName)`). Đợt này bám đúng khuôn đó.

## Quyết định chốt

1. **Chỉ đổi `name` và `description`. Không đổi `code`, không đổi công thức, không đổi số liệu lương.**
2. Migration data-only theo khuôn 08-04, **không lọc `status`** khi update `system_salary_compositions`
   (thành phần đã được công ty lấy về bị set `status = InActive`, lọc `status = 1` sẽ sót).
3. `salary_compositions` chỉ update khi giá trị hiện tại còn đúng bản gốc → không đè lên tên/mô tả
   người dùng đã tự sửa.
4. **Chặn trùng tên trước khi update** — `SalaryCompositionRequest` validate tên là duy nhất trên toàn
   hệ thống, nên bản ghi nào bị trùng thì bỏ qua + ghi log, không update đè.
5. Cập nhật `SystemSalaryCompositionSeeder` để DB dựng mới cũng đúng. **Không chạy lại seeder** trên DB
   đã có dữ liệu (seeder có `truncate()`).
6. **Thành phần mới KHÔNG dùng `formula`.** `CreateEmployeePayroll::systemData` kiểm tra: nếu `code` có
   trong `system_salary_compositions` thì gọi thẳng `calcData()` và **bỏ qua `formula`**. Nên 3 thành
   phần mới phải thêm `case` vào `calcData()`.
7. **Phải sửa `calcData()` ở CẢ HAI nơi**: `CreateEmployeePayroll` (tạo bảng lương) và `SalaryService`
   (tính lại bảng lương qua `GET /payroll/salary/{id}/updateSalaryEmployee`). Sửa một chỗ thì tạo mới ra
   số nhưng tính lại về 0.
8. Không thêm cột Mô tả vào màn danh mục hệ thống (khách chốt 08/09/2026: chỉ cần ghi vào ô Mô tả).

## Phạm vi

**Làm trong đợt này**

- Đổi `name` 9 thành phần (Nhóm 1 khách duyệt) + sửa thiếu dấu cách 1 thành phần → **10 tên**.
- Viết lại `description` nêu rõ cách tính cho **5 thành phần** khách chỉ đích danh.
- Bổ sung **3 thành phần lương mới**: Nghỉ thai sản, Tổng công đi làm, Cộng nghỉ hưởng lương.

**Chưa làm — chờ khách trả lời**

- Mô tả cho `CONG_DI_DUONG` — xem "Vướng mắc" bên dưới.
- Tách thành phần VĐM theo từng hệ số (mục #24 trong bảng đối chiếu).

## Vướng mắc đang chờ khách

**1. `CONG_DI_DUONG` lệch nguồn dữ liệu (lệch SỐ, không phải lệch tên).**

| | Nguồn |
| --- | --- |
| Cột "Công đi đường (2)" trên bảng công | live từ đề nghị thanh toán **kế toán đã duyệt** (`TimesheetSummaryService` ~dòng 1536) |
| Thành phần lương `CONG_DI_DUONG` | `work_day_timekeeper_to_go` chốt trong bảng tổng hợp công (`CreateEmployeePayroll` ~dòng 946) |

Khách ghi mô tả mong muốn là "lấy tổng công đi đường KT duyệt trong đề nghị thanh toán" — tức theo nguồn
của **bảng công**. Ghi mô tả đó vào mà không sửa nguồn thì mô tả sai code; sửa nguồn thì **đổi số liệu
lương**, vượt phạm vi "sửa tên". → Hoãn, tách issue riêng.

Kéo theo: `TONG_CONG_DI_LAM` (4) = (1) + (2) + (3) có chứa Công đi đường. Đợt này lấy đúng nguồn mà
`CONG_DI_DUONG` đang dùng để bảng lương nhất quán nội bộ; chốt lại nguồn thì thành phần này tự khớp theo.

**2. Mục #24 — VĐM tách theo từng hệ số: không tạo cố định được.**

Hệ số VĐM khai ở *Chấm công › Cài đặt › Quy định làm thêm › tab "Khung giờ làm thêm"*
(`/timesheet/setting/overtime`, bảng `overtime_hours`, 3 cột hệ số ngày thường / ngày nghỉ / ngày lễ).
`OvertimeHour::getAllRatio()` gom cả 3 cột của mọi khung giờ → lọc trùng → sắp xếp, nên **số cột VĐM
thay đổi theo cấu hình người dùng**, còn thành phần lương là bản ghi cố định. Cần khách chốt danh sách
hệ số nếu muốn tạo cứng.

## Lỗi có sẵn phát hiện khi rà (KHÔNG sửa trong đợt này)

Đều là lỗi tồn tại từ trước, không do đợt này gây ra. Ghi lại để báo cáo, chờ quyết định riêng vì đụng
vào là **đổi số liệu lương** / đụng hàm dùng chung.

1. **3 thành phần lương luôn trả về 0** trong `CreateEmployeePayroll::calcData`:
   - `BU_TRU_CONG_HANH_CHINH_SAU_QUYET_TOAN` — có `case` nhưng **thiếu trong mảng `$cham_congs`** nên
     `in_array` không lọt vào, `case` thành code chết.
   - `NGHI_KHONG_LY_DO`, `NGHI_HUONG_BHXH` — `case` viết sai hoa thường (`NGHi_KHONG_LY_DO`,
     `NGHi_HUONG_BHXH`) nên không bao giờ khớp.
2. **`SalaryService::calcData` thiếu 9 mã** so với `CreateEmployeePayroll::calcData` (thiếu
   `TONG_VDM_QUY_DOI`, `NGHI_PHEP`, `NGHI_CHE_DO`, `CONG_DI_DUONG`, `CONG_CONG_GIAM_TRU`,
   `NGHI_KHONG_LY_DO`, `NGHI_HUONG_BHXH`, `TONG_NGHI_KL`, `CONG_CA_DEM`; lại thừa `SO_GIO_LAM_THEM`).
   → Bấm "tính lại bảng lương" thì các thành phần đó về 0.
3. **`TONG_VDM_QUY_DOI` có thể lệch cột (3) do làm tròn**: bảng công cộng `round(giờ/8, 2)` **từng dòng**
   (`vdm_total`), thành phần lương làm tròn **một lần trên tổng** (`round(total_overtime_minutes_after / 8, 2)`).
4. **`OvertimeHour::getAllRatio()`**: không loại hệ số rỗng → sinh cột rác `VĐM 1(x-)` trên bảng công;
   và không lọc `company_id` (trong khi màn cài đặt có lọc) → công ty này thấy hệ số công ty khác khai.
5. `TimesheetMonthSummaryService::calc_employee_new` dòng ~547 có lỗi cú pháp
   `$punishment_rule_late + $$punishment_rule_early` (biến-của-biến) làm mất phần "về sớm". Hàm này
   **đang là code chết** (chỗ gọi duy nhất đã bị comment), bản chạy thật là
   `CreateTimesheetSummary::calc_employee_new`.

## Cách tự kiểm sau khi chạy

1. Mở màn Danh mục thành phần lương của hệ thống → đối chiếu 10 tên + 3 thành phần mới có xuất hiện.
2. Mở một bảng lương cũ → tên cũ còn nguyên, số liệu không đổi.
3. Tạo một mẫu bảng lương mới → hiện tên mới.
4. Chạy thử một bảng lương → giá trị các thành phần cũ không đổi; 3 thành phần mới ra số khớp với các
   cột (17), (4), (8) trên Bảng công chi tiết của cùng nhân viên, cùng kỳ.
