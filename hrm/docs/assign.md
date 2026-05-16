# Module Giao Việc (Assign)

## Mục đích
- Quản lý dự án tiền khả thi (TKT): từ meeting → giải pháp → triển khai → quyết toán
- Giao việc, quản lý công tác, thanh toán công tác phí
- Quản lý task, issue, BOM List trong dự án

## Cấu trúc thư mục
- BE: `/hrm-api/Modules/Assign`
- FE: `/hrm-client/pages/assign` (45 feature area, ~289 file Vue)
- Shared components: `/hrm-client/components/assign-components/`

## Module kết nối
- **Human**: công ty, phòng ban, nhân viên, khách hàng, danh mục sản phẩm (TpBrand, TpUnit, TpSupplier...)
- **Timesheet**: phân quyền, ca làm việc, chấm công, quy định lao động, giờ tăng ca

---

## Luồng chính: Quản lý dự án TKT

```
Meeting → Dự án TKT → Yêu cầu làm giải pháp → Giải pháp → Hạng mục → Task/Issue                                     
```

### 1. Meeting
- Trạng thái: DRAFT → SCHEDULED → CONFIRMED → COMPLETED/CANCELLED
- Phân loại thành viên: type=1 (công ty), type=2 (khách hàng)
- Có thể tạo dự án TKT nhanh từ meeting, 1 dự án có nhiều meeting

### 2. Dự án tiền khả thi (ProspectiveProject)
- Mã: `[PHÒNG].[ỨNG_DỤNG].[YYYY].DA[NNN]`
- Trạng thái: TẠO → THU_THẬP_TT → CHỜ_GIẢI_PHÁP → TRIỂN_KHAI → DUYỆT_GP → LÀM_GIÁ → HỢP_ĐỒNG → NGHIỆM_THU → ĐÓNG → LƯU_TRỮ
- Phân loại theo hệ thống phân cấp: Ngành (Scope) → Nhóm giải pháp (Industries) → Ứng dụng (Applications)
- Có thể tạo độc lập hoặc từ meeting

### 3. Yêu cầu làm giải pháp (RequestSolution)
- Trạng thái: DRAFT → CHỜ_TIẾP_NHẬN → [YÊU_CẦU_BỔ_SUNG] → ĐÃ_TIẾP_NHẬN → TRIỂN_KHAI → HOÀN_THÀNH
- Phòng giải pháp có thể yêu cầu bổ sung thông tin hoặc tiếp nhận luôn

### 4. Giải pháp (Solution) - Luồng duyệt đa cấp
- Trạng thái: TẠO_NHÁP → CHỜ_PM_DUYỆT → CHỜ_LEADER_DUYỆT → TRIỂN_KHAI → CHỜ_DUYỆT_GP → ĐÃ_DUYỆT → ĐIỀU_CHỈNH → CHỜ_LÀM_GIÁ → CHỐT_GP → HOÀN_THÀNH
- **Quy tắc**: Giải pháp chỉ tiến sang CHỜ_LEADER khi PM đã duyệt; chỉ TRIỂN_KHAI khi tất cả hạng mục được leader duyệt
- Quản lý version cho cả giải pháp và hạng mục
- Tài nguyên trong giải pháp: Tasks, Issues, Files, Meetings, Hồ sơ trình duyệt, Nhân sự

### 4a. Hồ sơ trình duyệt giải pháp (SolutionReviewProfile)
- Trạng thái: DRAFT → PENDING → APPROVED/REJECTED
- Thuộc về Solution (cấp giải pháp, không phải hạng mục)
- Có files đính kèm, comments (với react), start_date, sent_date, review_deadline
- Quy trình: PM tạo hồ sơ trình duyệt → Gửi Trưởng phòng duyệt

### 5. Hạng mục (SolutionModule)
- Trạng thái: CHƯA_DUYỆT → ĐÃ_DUYỆT → CHỜ_DUYỆT_HỒ_SƠ → ĐÃ_DUYỆT_HỒ_SƠ
- Mỗi hạng mục có leader_id riêng chịu trách nhiệm duyệt
- Hồ sơ trình duyệt hạng mục (SolutionModuleReviewProfile): DRAFT → PENDING → APPROVED/REJECTED
- Quy trình: Leader tạo hồ sơ → Gửi PM → Gửi Trưởng phòng

### 6. Task & Issue
- Task mã: `[CTY].TASK.[KH|NB].[YY].[NNNN]`
- Task trạng thái: DRAFT → CHỜ_DUYỆT → TODO → ĐANG_LÀM → [TẠM_DỪNG] → REVIEW → DONE/REJECTED/CANCELLED
- **Quy tắc duyệt 2 bước**: nhân viên submit kết quả → người duyệt review
- Issue trạng thái: NEW → ASSIGNED → IN_PROGRESS → RESOLVED → CLOSED/REOPENED
- Issue có: Priority, Severity, Impact Level, Root Cause Group, SLA

---

## Luồng phụ: Giao việc & Công tác

### Phiếu đề xuất/công tác (AssignRequest)
- Loại: PHIẾU_ĐỀ_XUẤT (1) | PHIẾU_CÔNG_TÁC (2)
- Trạng thái: DRAFT → CHỜ_DUYỆT → ĐÃ_DUYỆT → TẠO_PHIẾU_CT → NHẬP_KQ → DUYỆT_KQ

### Thanh toán công tác (PaymentBusinessRequest)
- Chi phí chia theo: đi lại, công tác, lưu trú, khác
- Phân biệt chi phí thực tế vs chi phí duyệt
- Duyệt bởi: approver_id + kt_approver_id

### Quyết toán hợp đồng (SettlementContract)
- Trạng thái: TẠO → CHỜ_TP_DUYỆT → CHỜ_KẾ_TOÁN_DUYỆT → ĐÃ_DUYỆT/KHÔNG_DUYỆT
- Liên kết: nhân viên + sản phẩm + task giao việc

### Bàn giao công việc (Handover)
- Mã: `BG.[YYYY].[NNNN]`
- Trạng thái: DRAFT → PENDING → APPROVED → COMPLETED
- Lý do: NGHỈ_VIỆC, CHUYỂN_CÔNG_TÁC, THAI_SẢN, DÀI_HẠN, KHÁC

---

## Danh mục cấu hình
- **Phân cấp ngành**: Ngành (NN.XXXX) → Nhóm GP (NGP.XXXX) → Ứng dụng → hỗ trợ lock/unlock
- **Lĩnh vực KH**: LVKH.XXXX
- **Giai đoạn dự án** (ProjectPhases): GD.XXXX, hỗ trợ lock/unlock
- **Form template động**: theo loại ứng dụng, có versioning bằng snapshot
- **BOM List**: mã BOM-[YYYY]-[NNNNN], hỗ trợ component (1) và aggregate (2), quan hệ cha-con
- Mức ưu tiên, loại cuộc họp, vai trò dự án, phương tiện đi lại, định mức công tác

---

## Phân quyền
- Phân cấp nhân sự: **Trưởng phòng → PM → Leader → Nhân viên**
- Permission route-level qua middleware `checkPermission`
- Permission entity-level: canEdit(), canDelete(), canCreatePaymentProfile()
- Phạm vi quản lý theo departmentsManager()

## Quy tắc sinh mã
| Entity | Format | Ghi chú |
|--------|--------|---------|
| Meeting | [CTY].MET.[KH/NB].[YY].[NNNN] | KH=khách hàng, NB=nội bộ |
| Dự án TKT | [PHÒNG].[APP].[YYYY].DA[NNN] | Theo phòng ban + năm |
| Task | [CTY].TASK.[KH/NB].[YY].[NNNN] | Tự tăng theo năm |
| BOM List | BOM-[YYYY]-[NNNNN] | 5 số tự tăng |
| Bàn giao | BG.[YYYY].[NNNN] | 4 số tự tăng |

## FE: Cấu trúc trang chính
- **Dashboard**: 3 metric card + biểu đồ phân bổ trạng thái
- **My Job**: workspace cá nhân (17+ component)
- **Solutions**: tab-based (Info, Modules, OrgChart) + manager sub-interface
- **BOM Builder**: visual editor với import/export, sub-assembly, 10 modal chuyên biệt
- **Form Templates**: drag-drop builder với preview
- **Settlement Contract**: form 5 bước (ThôngTin → SảnPhẩm → Task → ChiTiết → NhânViên)
- **Report**: 8 sub-view (task theo tỉnh/KH, hiệu suất, dự án TKT, meeting, yêu cầu GP theo phòng)

## Store (Vuex)
- Root actions: init user profile, employees, departments, companies; lọc cooperation_type=2
- optionsSelect: 18 danh mục dropdown cache
- Feature flags: `use_decision`, `use_rice`, `use_erp`
- Riêng: settlementContract, paymentProfile, rice, decision

---

## Lưu ý
- **TODO**: `SolutionRequestsByDepartmentReportService.php:170` - cần uncomment khi bảng solutions sẵn sàng
- **TODO**: `SolutionRequestsByDepartmentReportController.php:105` - chưa tạo class Excel export
- **TODO**: FE `request-solution/index.vue` ~dòng 500 - chưa gọi API delete
- **Pattern lạ**: AttachmentType hỗ trợ cả format cũ (LTL-XXX) và mới (LTL.XXX)
- **File lớn cần refactor**: AssignBusinessForm (187KB), BomBuilderEditor (102KB), AssignRequestForm (107KB)
- **Dual classification**: vừa dùng Scope/Industry/Application vừa dùng ProjectPhase/ProjectPhaseItems
- **Task watchers**: relationship bị comment out trong entity Task
