# Design (tóm tắt) — Nhóm nghiệp vụ áp dụng theo nghiệp vụ

> @khoipv — 2026-09-17 — **bản nháp, chờ user chốt**

## Vấn đề

Phạm vi duyệt hiện tại là **hợp của mọi nhóm nghiệp vụ mà một người làm "Người có quyền duyệt"**, và dùng chung cho **mọi loại phiếu**:

```
duyệt được phiếu X của người Y  ⟺  có quyền "Duyệt X"  AND  Y ∈ listManageEmployeeIdsByGroup()
```

- **Quyền** chọn LOẠI phiếu, **nhóm nghiệp vụ** chọn NGƯỜI — hai trục nhân chéo, không cắt chéo được.
- Hệ quả: không cấu hình được "A duyệt hợp đồng của nhóm B nhưng không duyệt đơn xin nghỉ của chính nhóm B đó". Cách duy nhất là gỡ quyền loại phiếu, nhưng như vậy A cũng mất quyền duyệt loại phiếu đó ở **mọi** nhóm khác.

## Giải pháp đề xuất (Hướng C — bản 2: theo **phân hệ**)

> **Chốt với user 17/09/2026:** ô tích lấy đúng **danh sách phân hệ của màn `timesheet/setting/roles`** —
> tức cột **`permissions.type`**. **Chọn phân hệ nào thì áp dụng cho TẤT CẢ quyền trong phân hệ đó.**
> Ưu điểm: không phải bịa danh mục module mới, user đã quen cách chia này ở màn phân quyền chức vụ.

9 phân hệ đang hiển thị ở màn roles (`Permission.vue` hardcode): **1** Chấm công (75 quyền) · **2** Tính lương (13) ·
**3** Hành chính nhân sự (46) · **14** Kinh doanh (7) · **4** Kế hoạch (12) · **5** Quản lý thầu (10) ·
**15** Danh mục (12) · **8** Hợp đồng (22) · **7** Cung ứng (14).
(4 type 6/10/11/12 mỗi type 1 quyền "Cấu hình phân hệ …" không được render — không đưa vào.)

1. Bảng nối `group_permission_types (group_permission_id, permission_type)` — chỉ index, không khóa ngoại.
2. FE màn nhóm nghiệp vụ: multi-select **"Áp dụng cho phân hệ"**, dùng lại danh sách type của màn roles.
3. Helper nhận **tên quyền** (không phải tên module): `listManageEmployeeIdsByGroup($permission = null)` → tra
   `permissions.name → type` (có cache) rồi lọc nhóm theo type. `null` = hành vi cũ → 91 call site không phải sửa ngay.
   Call site chỉ việc lặp lại đúng chuỗi quyền đang check ở dòng bên cạnh (`isCurrentEmployeeHasPermission('Duyệt hợp đồng')`).
4. Chỉ sửa call site của phân hệ cần tách + hàm định tuyến thông báo.
5. Migration dữ liệu: nhóm hiện có bật đủ tất cả phân hệ → deploy xong không ai mất quyền.

### Độ phủ theo từng phân hệ (rà call site thật)

| Phân hệ | type | Số quyền | Call site | Kết luận |
|---|---|---|---|---|
| Chấm công | 1 | 75 | 47 | **MỘT PHẦN** — thiếu `BGD duyệt đơn xin nghỉ` |
| Hợp đồng | 8 | 22 | 8 | **MỘT PHẦN** — thiếu biên bản NT / TL / kết xuất cung ứng |
| Quản lý thầu | 5 | 10 | 8 | **MỘT PHẦN** — thiếu `BGD duyệt kết quả thầu` |
| Kế hoạch (báo giá) | 4 | 12 | 4 | **MỘT PHẦN** — thiếu `BGĐ duyệt báo giá`, `BGĐ duyệt dự toán chuyển HĐ` |
| Kinh doanh (dự toán) | 14 | 7 | 4 | **MỘT PHẦN** — nhóm KPI không có call site |
| Tính lương | 2 | 13 | **0** | **KHÔNG DÙNG** — `SalaryService` dùng `listManageEmployeeInfoIds()` (cây quản lý), khác cơ chế |
| Hành chính nhân sự | 3 | 46 | **0** | **KHÔNG DÙNG** — chỗ duy nhất `EmploymentContractService.php:45` đang comment |
| Cung ứng | 7 | 14 | **0** | **KHÔNG DÙNG** |
| Danh mục | 15 | 12 | **0** | **KHÔNG DÙNG** |
| Đào tạo | — | **0** | 1 | **KHÔNG CÓ PHÂN HỆ** — `Training/BaseService.php:33` có scope nhóm nhưng bảng `permissions` không có quyền nào → không có ô nào đại diện |

### 3 câu cần user chốt

1. 5 phân hệ **KHÔNG DÙNG** → ẩn hẳn hay hiện dạng mờ (disabled) kèm giải thích?
2. Để đúng nghĩa "áp dụng cho tất cả quyền trong phân hệ" thì phải **thêm scope nhóm** vào các quyền cấp BGĐ +
   biên bản nghiệm thu / thanh lý / kết xuất cung ứng → **đổi luật nghiệp vụ**, không phải đổi cấu hình. Có làm không?
3. Phân hệ Đào tạo — có seed quyền + thêm phân hệ mới để cấu hình được không?

### Lưu ý đã có sẵn cơ chế tương tự cho phần XEM

Bảng `permissions` đã có **10 quyền "… theo nhóm nghiệp vụ"** (type 4, 5, 8, 14) dùng cho **xem danh sách / báo cáo**
(3 cấp: tổng công ty / công ty / nhóm nghiệp vụ). Sau khi thêm ô tích phân hệ cho phần **DUYỆT**, phải rà để
hai cơ chế khớp nhau, tránh cảnh **duyệt được nhưng không nhìn thấy phiếu** (hoặc ngược lại).

## Độ phủ: ô tích nghiệp vụ KHÔNG bao quát hết quyền của phân hệ

Rà theo **call site thật** của 2 helper (`listManageEmployeeIdsByGroup` / `listManageEmployeeInfoIdsByGroup`): **91 chỗ / 37 file**. Ba dạng lệch:

1. **Phân hệ không hề dùng nhóm nghiệp vụ** — `Modules/Supply` (13 quyền Cung ứng) và `Modules/Assign`: **0 call site**. Phân quyền theo `created_by` / người được giao / công ty. Tích hay bỏ tích đều vô tác dụng.
2. **Phân hệ có dùng nhưng dễ bỏ sót** — `Modules/Training` lọc qua `Training/Services/BaseService.php:33`, **1 dòng chi phối ~40 service con**. "Phiếu giao việc" nằm trong **Timesheet** (`JobAssignmentNote`), không phải `Modules/Assign`.
3. **Trong phân hệ có dùng thì cũng chỉ MỘT PHẦN quyền bị chi phối** — các hàm dưới chỉ xét quyền, **bỏ qua** nhóm nghiệp vụ → duyệt được **toàn hệ thống**:
   `Quotation::canBGDApprove()` · `BidPackage::canBGDApprove()` · `Attendance::canBGDApprove()` · `AcceptanceReport.php:119` (Duyệt biên bản nghiệm thu) · `ContractLiquidation.php:108` (Duyệt biên bản thanh lý) · `Contract.php:370` (Duyệt hợp đồng kết xuất cung ứng).

→ Hệ quả thiết kế: đặt tên ô theo **nhóm phiếu có scope**, không theo tên phân hệ; mỗi ô phải gắn nhãn **ĐỦ / MỘT PHẦN**; muốn ô phủ trọn phân hệ thì phải **thêm scope** vào các hàm trên — đó là **đổi luật nghiệp vụ**, không phải đổi cấu hình.

Danh sách chốt lại **8 ô sống**: Hợp đồng (8 site, một phần) · Báo giá (4, một phần) · Gói thầu (8, một phần) · Dự án (4, một phần) · Chấm công–Nhân sự (21, một phần) · Phiếu công tác (7, đủ) · Phiếu giao việc (2, đủ) · Đào tạo (1, đủ). Cung ứng để **disabled** kèm giải thích.

## Rủi ro chính

- **Phiếu kẹt**: Đơn xin nghỉ không có nhánh tự duyệt (khác Báo giá / Hợp đồng). Bỏ tích nghiệp vụ Chấm công–Nhân sự mà không nhóm nào khác phủ → đơn nghỉ không ai duyệt được. Cần validate cảnh báo khi lưu.
- **Lệch nút duyệt vs thông báo** nếu chỉ sửa `canApprove()` mà quên `listEmployeeInfoHasPermission()`.
- Sửa **hàm dùng chung**, 91 call site → bắt buộc xin phê duyệt trước.
- **Hiểu nhầm độ phủ**: user bỏ tích một nghiệp vụ và tưởng đã chặn hết, trong khi người giữ quyền cấp BGĐ vẫn duyệt được toàn hệ thống.
- 36/91 call site nằm ở 2 dashboard (`CategoryDashboardService` 26 + `Timesheet/DashboadService` 10) **trộn nhiều loại phiếu trong cùng một hàm** → phải chú thích nghiệp vụ theo từng dòng.

## Demo

`demos/demo-nhom-nghiep-vu-theo-nghiep-vu.html` — 4 tab: màn cấu hình (**ô tích = 9 phân hệ của màn roles**) · mô phỏng ma trận phạm vi duyệt (so sánh trước/sau) · **độ phủ quyền — rà theo call site** · ghi chú kỹ thuật.

## Spec chi tiết

Chưa viết — sẽ tạo `docs/superpowers/specs/YYYY-MM-DD-nhom-nghiep-vu-theo-nghiep-vu-design.md` sau khi user chốt Phase 2.
