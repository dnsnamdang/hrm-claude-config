# Brief A — Báo giá: Danh sách · Phân quyền · Trạng thái · Xoá · Duyệt/Từ chối · Chốt

Nguồn: worktree `gop_db-client` (FE) + `gop_db-api` (BE), đọc ngày 13/10/2026.
Viết tắt đường dẫn:
- FE `L` = `pages/assign/quotations/index.vue` · FE `P` = `pages/assign/quotations/pending-approval/index.vue` · FE `D` = `pages/assign/quotations/_id/index.vue` · FE `E` = `pages/assign/quotations/_id/edit.vue`
- BE `C` = `Modules/Assign/Http/Controllers/Api/V1/QuotationController.php` · BE `S` = `Modules/Assign/Services/QuotationService.php` · BE `Q` = `Modules/Assign/Entities/Quotation.php` · BE `R` = `Modules/Assign/Transformers/QuotationResource.php` · BE `RT` = `Modules/Assign/Routes/api.php`

---

## 1. Đường dẫn menu (chữ trên giao diện)

Cả 2 phân hệ nằm trong nhóm phân hệ **"4. KINH DOANH - TÀI CHÍNH"** (`components/subsystems.js:51` hằng `GROUP_BUSINESS`).

### 1.1 Danh sách báo giá (`/assign/quotations`) — 2 lối vào
1. **Phân hệ "CSKH trước bán"** (`subsystems.js:516-527`, label `CSKH trước bán`, mô tả `Khách hàng tiềm năng`, icon `ri-user-search-line`) → mục menu cấp 1 **"Báo giá"** (icon `ri-file-list-3-line`) — `components/subsystem-menu/presale.js:62-68`. Không gate quyền (`isShow: true`).
   - Thứ tự menu phân hệ: Tổng quan · Dự án TKT · Yêu cầu giải pháp · Yêu cầu tính giá bán · **Báo giá** · Nhiệm vụ · Vấn đề · Báo cáo… (presale.js:33-90).
2. **Phân hệ "Bán hàng"** (`subsystems.js:530-541`, label `Bán hàng`, mô tả `Đơn hàng & báo giá`) → nhóm **"Bán hàng"** → mục **"Báo giá"** → màn **"Danh sách báo giá"** — `components/subsystem-menu/sale-hub.js:36-50`. Không gate quyền.
   - Hub (trang Tổng quan `/sale/dashboard`) và sidebar dọc dùng chung 1 nguồn (`sale.js:1-12`, `buildSaleTree`).
   - Cùng mục "Báo giá" có 2 màn xám (chưa xây): "Báo giá vật tư - hàng hóa - thiết bị", "Báo giá dự án" (sale-hub.js:43-44).
   - ⚠️ ĐỪNG nhầm: nhóm **"Bán dịch vụ" → "Báo giá dịch vụ SC-BD-BT" → "Danh sách báo giá"** (`sale-hub.js:98`) là màn KHÁC (`/customer-care/wr-quotations?type=all`, báo giá dịch vụ sửa chữa), không thuộc tài liệu này.
3. (Ngoài menu) tab Báo giá trong màn Dự án TKT cũng dùng chung logic sao chép/chốt (`utils/mixins/Assign/QuotationCopyMixin.js` docblock dòng 3-8).

### 1.2 Báo giá chờ duyệt (`/assign/quotations/pending-approval`) — 1 lối vào
- **Phân hệ "Bán hàng"** → nhóm **"Phê Duyệt"** → mục **"Dự án TKT"** → màn **"Báo giá chờ duyệt"** (`sale-hub.js:273-283`).
- Gate menu: sidebar dọc gắn quyền `['Trưởng phòng duyệt giá Bom giải pháp', 'Ban giám đốc duyệt giá Bom giải pháp']` qua map `SALE_LINK_PERMISSIONS` (`sale.js:42-46`). ⚠️ Thực tế: (a) trên HUB `/sale/dashboard` màn này KHÔNG khai `isShow` inline nên `hub.js:139-155 isScreenVisible` trả `true` → hiện cho mọi người; (b) ở sidebar dọc đây là lá cấp 3 (Phê Duyệt › Dự án TKT › Báo giá chờ duyệt) mà `components/training-components/Sidebar.vue:129` chỉ ẩn lá cấp 3 khi `isShow == false` → mảng quyền không có hiệu lực. Kết luận: menu có thể hiện với người không có quyền; BE chặn bằng middleware (403) — xem mục 2.
- Ngoài ra thông báo "gửi duyệt" có deep-link thẳng tới màn này (S:3916-3918, S:3984-3986).

---

## 2. Phân quyền

### 2.1 Danh sách quyền nhóm "Báo giá" (`Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php:1053-1063`, type=4)
| sort | id | Tên quyền (name) | display_name | Tác dụng THẬT trong code |
|---|---|---|---|---|
| 1 | 1080 | Xây dựng giá bán theo công ty | (như tên) | Không mở màn Báo giá. Dùng khi **lập báo giá từ Yêu cầu tính giá bán (YCBG)** của dự án triển khai liên phòng/khác BY_DEPT (C:268-286, S:4904-4922) và gate nút **Sao chép** báo giá lập từ YCBG (S:284-287, mixin `canCopyQuotation`). Menu "Yêu cầu tính giá bán" (`sale.js:43`). |
| 2 | 1091 | Xây dựng giá bán theo phòng | | Như trên nhưng cho dự án `implementation_type = BY_DEPT`; thêm điều kiện YCBG phải cùng phòng ban của người thao tác (C:274-280, S:4910-4916). |
| 3 | 1081 | Trưởng phòng duyệt giá Bom giải pháp | | Xem màn **Báo giá chờ duyệt** + xuất Excel (RT:607-610); **Duyệt (TP)** (RT:648-649); **Từ chối** khi báo giá đang Chờ TP duyệt (RT:652-653, S:4074-4076); xem chi tiết báo giá trong hàng chờ của mình dù thiếu quyền xem danh sách (C:411-419); được xem tỷ suất LN dòng hàng tạm (S:3756-3757); nhận thông báo gửi duyệt/đã duyệt. |
| 4 | 1082 | Ban giám đốc duyệt giá Bom giải pháp | | Xem **Báo giá chờ duyệt** + xuất Excel; **BGĐ duyệt** (RT:650-651); **Từ chối** khi đang Chờ BGĐ duyệt (S:4077-4079); nhận thông báo "TP đã duyệt & chuyển BGĐ". |
| 5 | 1083 | **Xem tất cả danh sách Báo giá** | Xem danh sách Báo giá theo tổng công ty | Phạm vi xem: TẤT CẢ báo giá (không lọc). |
| 6 | 1084 | Xem danh sách Báo giá theo công ty | | Báo giá có `company_id` = công ty đang chọn của user **hoặc** do chính user tạo. |
| 7 | 1085 | Xem danh sách Báo giá theo phòng ban | | Báo giá thuộc phòng ban user quản lý (`listManageDepartmentIds`) hoặc bộ phận user quản lý (`listManagePartIds`) **hoặc** do chính user tạo. |
| 8 | 1086 | Xem danh sách Báo giá theo bộ phận | | Báo giá thuộc bộ phận user quản lý hoặc do chính user tạo. |
| 9 | 1092 | Xem giá vốn hàng hoá | | Thấy Tổng giá nhập, Tỷ suất LN, cột "Thành tiền nhập" ở bảng tổng hợp (S:3640-3670, `DetailQuotationResource.php:338-343`, D:990); popup Gửi duyệt hiện "Tổng giá nhập" + "Tỷ suất LN" (`components/assign/quotation/QuotationSubmitModal.vue:16-35`); màn Sửa hiện badge "Cấp duyệt" dự kiến (E:1227); popup Sao chép thấy cả thay đổi giá vốn (C:449-453). Dùng chung với nhiều màn khác (BOM, kho...). |
| 10 | 1173 | Cho phép thêm giảm giá trong báo giá | | Không có quyền → ô Loại giảm giá bị khoá ở màn Sửa (E:298, E:1724); BE chặn mọi THAY ĐỔI giảm giá (đổi phương thức GG hoặc số tiền GG) khi tạo/sửa → lỗi 403 `Bạn không có quyền áp dụng giảm giá trong báo giá` (S:4804-4823). Giữ nguyên GG cũ vẫn lưu được. |

Ghi chú: `display_name` của quyền 1083 khác `name` — trên màn phân quyền hiển thị "Xem danh sách Báo giá theo tổng công ty".

### 2.2 Phạm vi dữ liệu màn Danh sách báo giá
- BE: `S:4321-4350 getListForUser` gọi `checkPermissionListWithColumn($query, [1083, 1084, 1085, 1086, true], 'quotations', 'created_by')`. Logic helper `app/Helper/PermissionHelper.php:336-381`: xét lần lượt từ quyền rộng nhất, có quyền nào dừng ở đó.
- **Không có quyền nào trong 4 quyền xem** → phần tử thứ 5 = `true` ⇒ chỉ thấy **báo giá do chính mình tạo** (`created_by = mình`) (PermissionHelper.php:372-377).
- `company_id`/`department_id`/`part_id` của báo giá = theo hồ sơ của NGƯỜI TẠO lúc tạo (tự gán bởi `app/Models/BaseModel.php:118-149`).
- FE truyền 4 cờ quyền vào bộ lọc Công ty/Phòng ban/Bộ phận/Người lập để giới hạn lựa chọn (L:862-868).
- Chi tiết: cùng phạm vi + thêm báo giá đang nằm trong hàng chờ duyệt của chính user (C:392-420 `scopedQuotationQuery` + `findViewableQuotation`). Ngoài phạm vi → 404 `Không tìm thấy báo giá.` (C:228-230). FE hiện "Không tìm thấy báo giá." (D:5).
- Xuất Excel danh sách: KHÔNG gate quyền riêng, dùng đúng phạm vi + bộ lọc của danh sách (C:58-76; comment L:102-104).

### 2.3 Phạm vi màn Báo giá chờ duyệt (`S:4369-4423 applyPendingApprovalScope`)
- Route gắn middleware `checkPermission:Trưởng phòng duyệt giá Bom giải pháp|Ban giám đốc duyệt giá Bom giải pháp` (RT:608-611) → không có 1 trong 2 quyền ⇒ 403.
- Chỉ báo giá thường (`is_summary = false`); báo giá tổng có luồng duyệt riêng.
- Có quyền TP: báo giá **Chờ TP duyệt** thuộc **phòng ban mình quản lý** (`manageDepartmentIdsOf`, gồm cả cờ "quản lý tất cả phòng ban") (S:4924-4945).
- Có quyền BGĐ: báo giá **Chờ BGĐ duyệt** có `company_id` = **công ty trong hồ sơ** của mình (`auth()->user()->info->company_id`).
- Có cả 2: hợp 2 nhóm. Có quyền nhưng không quản lý phòng nào / không có công ty → danh sách rỗng.

### 2.4 Ma trận thao tác (ai được làm gì) — chốt chặn THẬT ở BE
| Thao tác | Điều kiện BE | Điều kiện hiện nút FE |
|---|---|---|
| Tạo báo giá (nút "Tạo báo giá") | Không có quyền riêng. Báo giá gắn dự án tự lập: chỉ **Sale phụ trách dự án** (`project.main_sale_employee_id`) — lỗi `Bạn không phải Sale phụ trách dự án này` (C:286-291). Lập từ YCBG: quyền Xây dựng giá (2.1). Báo giá không gắn dự án: ai vào được màn đều tạo được (C:260-262). | Nút luôn hiện, không gate (L:89-101). |
| Sửa (Sửa / Làm giá) | `ensureEditableByCreator` S:4719-4727: trạng thái **Đang tạo** VÀ **người tạo** = mình. Lỗi: `Báo giá không ở trạng thái Đang tạo, không thể sửa.` / `Chỉ người tạo báo giá mới có thể sửa.` | status = 1 và `creator_id` = NV đang đăng nhập (L:1136, D:1080-1082, E:1715-1720). |
| Xoá | Như Sửa (S:1785). | Như Sửa (L:1270-1272, D:725). |
| Sao chép | Nguồn phải trong phạm vi xem (else 404). Nguồn từ YCBG → quyền Xây dựng giá theo kiểu triển khai (+ cùng phòng nếu theo phòng). Nguồn không dự án → chỉ người lập (`Chỉ người lập báo giá mới được sao chép.`). Nguồn có dự án → chỉ Sale phụ trách dự án hiện tại (`Bạn không phải Sale phụ trách dự án này`) (S:280-302). Sao chép được ở MỌI trạng thái. | Xấp xỉ (mixin `QuotationCopyMixin.js` `canCopyQuotation`): YCBG → có 1 trong 2 quyền Xây dựng giá; còn lại: danh sách so `creator_id` (vì danh sách không có Sale phụ trách), chi tiết so `project.main_sale_employee_id`. Có lệch đã biết (FE hiện nút nhưng BE 403). |
| Gửi duyệt | Chỉ người tạo + trạng thái Đang tạo (qua `assertSubmittable` S:3796-3814). | Nút "Gửi duyệt" ở màn Sửa/Tạo mới, `canEdit` (E:1243-1247). Không có ở màn Danh sách/Chi tiết. |
| Tự duyệt (cấp 1) | Người tạo + Đang tạo + `price_approval_level = 1` (S:3923-3929). | Trong popup Gửi duyệt, nút "Xác nhận duyệt". |
| Duyệt TP | Quyền 1081 (middleware + S:3962) + phòng ban báo giá ∈ phòng mình quản lý (S:4947-4953 `Bạn không quản lý phòng ban của báo giá này.`) + trạng thái Chờ TP duyệt. | `hasTp && status === 2` (D:1092-1094) — FE KHÔNG kiểm phòng ban. |
| Duyệt BGĐ | Quyền 1082 + công ty báo giá = công ty hồ sơ mình (S:4955-4961 `Bạn không thuộc công ty của báo giá này.`) + Chờ BGĐ duyệt. | `hasBgd && status === 3` (D:1095-1097). |
| Từ chối | Chờ TP duyệt → quyền TP + phòng; Chờ BGĐ duyệt → quyền BGĐ + công ty (S:4069-4082). | `(hasTp && status 2) || (hasBgd && status 3)` (D:1098-1100). |
| Chốt (Trúng thầu) / Hủy chốt — báo giá KHÔNG gắn dự án | Chỉ **người lập** (C:1331-1340 `Chỉ người lập báo giá mới được thao tác.`; Q:357-371). Báo giá CÓ dự án: chỉ Sale phụ trách dự án (`Bạn không phải Sale phụ trách dự án này`) — thao tác ở tab Báo giá của Dự án TKT, không ở màn này. | Cờ `can_finalize` / `can_unfinalize` do BE trả (R:108-111). |
| Lập hợp đồng | (luồng hợp đồng) | Trạng thái Trúng thầu + chưa có HĐ + người lập = mình; không cần quyền (L:1207-1209, D:1102-1110). |
| Cập nhật Ghi chú kinh doanh | Trạng thái Đã duyệt; có dự án → NV KD phụ trách dự án; không dự án → người lập (S:4281-4316). | Ô ghi chú ở màn chi tiết (D:643-660). |
| Xem giá vốn | Quyền 1092 (2.1). | |
| Giảm giá | Quyền 1173 (2.1). | |

"Người tạo" = `quotations.created_by` (= `employees.id`, `auth()->id()`). "Sale phụ trách dự án" = `prospective_projects.main_sale_employee_id`.

---

## 3. Trạng thái báo giá

### 3.1 Hằng số (Q:11-20, tên + màu Q:62-80, trả ra FE qua `status_name`/`status_color` R:79-81)
| Mã | Hằng | Tên hiển thị | Màu badge |
|---|---|---|---|
| 1 | STATUS_DANG_TAO | **Đang tạo** | #64748B (xám — nháp) |
| 2 | STATUS_CHO_TP_DUYET | **Chờ TP duyệt** | #D97706 (cam — chờ duyệt) |
| 3 | STATUS_CHO_BGD_DUYET | **Chờ BGĐ duyệt** | #D97706 |
| 4 | STATUS_DA_DUYET | **Đã duyệt** | #16A34A (xanh lá) |
| 5 | STATUS_DONG | **Đóng** | #6B7280 (xám đã đóng) |
| 6 | STATUS_DUNG | **Dừng** | #DC2626 (đỏ) |
| 7 | STATUS_TRUNG_THAU | **Trúng thầu** | #7C3AED (tím — chốt) |

- KHÔNG có trạng thái "Từ chối" riêng: từ chối ⇒ quay về **Đang tạo** + lưu lý do (`rejected_reason`), màn chi tiết hiện dải đỏ "**Đã bị từ chối:** {lý do}" (D:8-10).
- Báo giá TỔNG (`is_summary = true`, mã `BGT-YYYY-NNNNN`) dùng bộ trạng thái riêng (Q:117-152): 1 Đang tạo · 2 **Chờ duyệt** · 4 Đã duyệt · 7 Trúng thầu · 9 Đã tạo hợp đồng (#0EA5E9) · 8 Hết hiệu lực (#6B7280) · 5 Đóng. Danh sách báo giá có hiển thị lẫn báo giá tổng (badge "Báo giá tổng", link sang `/assign/summary-quotations/{id}`, L:150-152, L:917-919).
- Loại báo giá (badge phân loại, Q:88-94): 1 **Từ BOM** (#64748B) · 2 **Tự nhập** (#7C3AED).
- Cấp duyệt (`price_approval_level`, R:89-92, màu Q:101-105): 1 → "Tự duyệt" (#64748B) · 2 → "TP" (#2563EB) · 3 → "TP & BGĐ" (#7C3AED).
- Mã báo giá thường: `BG-YYYY-NNNNN` (NNNNN = id lớn nhất + 1) (Q:327-331).

### 3.2 Luồng chuyển trạng thái
```
Đang tạo (1)
  └─ Gửi duyệt → tính cấp duyệt
       ├─ Cấp 1 → (popup "Xác nhận duyệt") Tự duyệt → Đã duyệt (4)
       ├─ Cấp 2 → Chờ TP duyệt (2) → TP Duyệt → Đã duyệt (4)
       └─ Cấp 3 → Chờ TP duyệt (2) → TP "Duyệt & chuyển BGĐ" → Chờ BGĐ duyệt (3) → BGĐ duyệt → Đã duyệt (4)
  Chờ TP duyệt / Chờ BGĐ duyệt ── Từ chối (bắt buộc lý do) ──→ Đang tạo (1)
Đã duyệt (4) ── Chốt (Trúng thầu, bắt buộc file xác nhận KH) ──→ Trúng thầu (7)
Trúng thầu (7) ── Hủy chốt (bắt buộc lý do) ──→ Đã duyệt (4)
Bất kỳ ≠ Đóng ── Dự án TKT bị đóng ──→ Đóng (5)
Đang tạo/Chờ TP/Chờ BGĐ ── có Yêu cầu điều chỉnh giải pháp làm Dừng YCBG đang XD giá ──→ Dừng (6) (không mở lại được)
```
- Cấp 3 cũng đi qua Chờ TP duyệt trước (S:3909-3915).
- Đóng: `ProspectiveProjectService.php:2100-2125` cascade MỌI báo giá của dự án có status ≠ 5 (kể cả Đã duyệt/Trúng thầu — comment Q:15 ghi "status 1/2/3" là cũ, code thực tế lấy tất cả trừ 5) sang Đóng, ghi lịch sử "Đóng theo dự án" kèm lý do đóng dự án.
- Dừng: `SolutionAdjustmentRequestService.php:85-104` — YCBG đang ở "Đang XD giá" bị dừng thì báo giá của YCBG đó (nếu đang 1/2/3) sang Dừng + thông báo cho người tạo.

### 3.3 Cách tính cấp duyệt (S:3524-3546 `calculateLevel`, `BomPriceApprovalConfigService.php:60-98`)
- **Cấp duyệt = MAX(L_V, L_M, L_T)** (Redmine #10898):
  - L_V theo **giá trị đơn hàng trước VAT sau giảm giá, quy đổi VND** (`total_sale_vnd = total_sale_after_discount × tỷ giá`, S:3664).
  - L_M theo **tỷ suất lợi nhuận tổng** M = (Tổng bán sau GG − Tổng giá nhập) / Tổng giá nhập × 100, làm tròn 2 số (S:3631). Tổng giá nhập = Σ giá nhập × SL của hàng hoá (hàng cha có con thì cộng giá nhập các con) + Σ giá nhập dịch vụ × SL + giá nhập chi phí vận chuyển (S:3587-3621). Tổng giá nhập = 0 ⇒ M = 0.
  - L_T theo **tỷ suất LN thấp nhất trong các dòng hàng tạm** (hàng không gắn mã ERP). Không có hàng tạm ⇒ bỏ qua L_T. Giá nhập dòng hàng tạm = 0 ⇒ tỷ suất 0% (S:3672-3684, S:3643-3645).
  - Giá trị không rơi vào khoảng nào ⇒ mặc định cấp 3 (BomPriceApprovalConfigService.php:97). Khoảng: `min ≤ x < max`.
- **Ngưỡng là CẤU HÌNH** (bảng `bom_price_approval_configs`, sửa được ở màn `/assign/settings/price-approval` "Cấu hình…", quyền `Cấu hình phân hệ giao việc/ công tác` — sale.js:55). Giá trị hiện tại trong DB local (`local_hrm_erp`, đọc 13/10/2026):

| Loại | Cấp 1 — Người làm giá tự duyệt | Cấp 2 — Trưởng phòng | Cấp 3 — Ban giám đốc |
|---|---|---|---|
| Giá trị đơn hàng V (order_value) | 0 ≤ V < 1 tỷ | 1 tỷ ≤ V < 20 tỷ | V ≥ 20 tỷ |
| Tỷ suất LN tổng M (profit_margin) | M ≥ 35% | 20% ≤ M < 35% | 0 ≤ M < 20% (M âm → không khớp → cấp 3) |
| Tỷ suất LN dòng hàng tạm (temp_product_margin) | ≥ 35% | 20% ≤ x < 35% | < 20% |
  - Seed gốc migration `database/migrations/2026_04_12_200000_create_bom_price_approval_configs_table.php:24-32` (M: 20/10%) — DB hiện tại đã cấu hình lại thành 35/20%. Hàng tạm seed tại `Modules/Assign/Database/Migrations/2026_08_27_000001_add_temp_product_margin_to_approval_configs.php`. ⇒ Tài liệu nên ghi "theo cấu hình hạn mức phê duyệt", có thể nêu giá trị mặc định hiện hành.
- **Tự động duyệt (đè cấp duyệt về 1)** — `isAutoApprovable` S:3558-3583 (#10797 TH1), khi ĐỦ cả:
  - Không chọn phương thức giảm giá, tổng giảm giá = 0, không có dòng giảm giá theo tổng;
  - Không có hàng tạm (mọi hàng hoá đều có mã ERP) và không có dịch vụ tạm (mọi dịch vụ có `cost_id`);
  - Mọi đơn giá bán hàng hoá/dịch vụ **> 1.000** (S:3549 `LOW_PRICE_THRESHOLD = 1000`);
  - Báo giá không rỗng.
  - Popup hiện: "Báo giá chỉ gồm hàng hoá/dịch vụ đã khai báo trên ERP, đơn giá bán > 1.000 đ và không có giảm giá — hệ thống tự động duyệt." và "Cấp duyệt dự kiến: Tự động duyệt" (QuotationSubmitModal.vue:105-108, 124-126).
- Tự duyệt cấp 1 vẫn do người tạo bấm "Xác nhận duyệt" trong popup (không tự chạy ngầm).

---

## 4. Màn Danh sách báo giá (FE L)

- Tiêu đề trang: **"Danh sách báo giá"** (L:494-496); tiêu đề bảng "Danh sách báo giá" (L:82).
- Phân trang mặc định 20 dòng/trang (L:435); thông báo rỗng: **"Không có dữ liệu phù hợp bộ lọc."** (L:85); lỗi tải: toast **"Lỗi tải dữ liệu"** (L:1092).
- Sắp xếp mặc định: Ngày tạo giảm dần (L:388-389, S:4530-4546). Cột sắp xếp được: Mã báo giá, Tổng giá trị sau VAT, Ngày duyệt, Ngày tạo, Ngày cập nhật (`sortable: true` trong `allColumns`).
- Bộ lọc nhớ trạng thái 10 phút khi đi lại trong `/assign/quotations*` (L:489-492, filterStateMixin). Chọn ô lọc là tìm ngay (deep watcher L:841-858), riêng ô tìm nhanh phải bấm Tìm/Enter.

### 4.1 Cột (L:636-818) — mặc định HIỆN HẾT, user ẩn/hiện/kéo thứ tự ở nút "Cấu hình cột hiển thị" (icon `ri-layout-column-line`); cột khoá (không bỏ tích được): STT, Mã báo giá, Hành động. STT + Mã báo giá ghim trái.
1. STT
2. **Mã báo giá** — link sang chi tiết (báo giá tổng → màn báo giá tổng)
3. **Loại báo giá** — badge "Từ BOM"/"Tự nhập"/"Báo giá tổng"
4. **BOM list** — "Mã BOM - Tên BOM"
5. **Mã YCBG** (tooltip tiêu đề "Mã yêu cầu xây dựng giá")
6. **Dự án TKT** — "Mã - Tên dự án"
7. **Khách hàng**
8. **Giai đoạn dự án**
9. **Tiền tệ**
10. **Tổng giá trị sau VAT** (căn phải, định dạng `1,234,567`, làm tròn số nguyên — L:913-916)
11. **Cấp duyệt** — badge Tự duyệt / TP / TP & BGĐ
12. **Người duyệt** (người duyệt cuối `approved_by`)
13. **Ngày duyệt** (dd/mm/yyyy HH:mm)
14. **Đồng bộ ERP** — badge "Đã đồng bộ" (xanh) / "Thất bại" (đỏ, tooltip lỗi) / trống
15. **Người tạo** — "Tên NV - Mã phòng" (R:113)
16. **Ngày tạo**
17. **Người cập nhật**
18. **Ngày cập nhật**
19. **Trạng thái** — badge màu BE
20. **Hành động**

### 4.2 Ô tìm nhanh
- Placeholder: **"Tìm theo mã báo giá, tên khách hàng"** (L:14). BE lọc `code LIKE %kw%` OR `customer_name LIKE %kw%` (S:4474-4480).

### 4.3 Bộ lọc nâng cao ("Bộ lọc danh sách", nhãn floating, user bật/tắt + sắp xếp ở "Cài đặt bộ lọc") — L:517-575
| Ô | Kiểu | Ghi chú |
|---|---|---|
| Công ty / Phòng ban / Bộ phận / Người lập | 4 ô (component `V2BaseCompanyDepartmentFilter`) | Người lập lọc `created_by` (S:4467-4469); lựa chọn công ty/phòng giới hạn theo quyền xem |
| Dự án TKT | select tìm từ máy chủ (gõ tìm, 20 kết quả) | Đổi dự án → xoá Giải pháp + Version |
| Giải pháp | select tìm từ máy chủ | **Khoá khi chưa chọn Dự án TKT** (L:46) |
| Version giải pháp | select | Chỉ có lựa chọn khi đã chọn Giải pháp |
| Khách hàng | select tìm từ máy chủ | |
| Trạng thái | select | 7 giá trị: Đang tạo, Chờ TP duyệt, Chờ BGĐ duyệt, Đã duyệt, Đóng, Dừng, Trúng thầu (L:468-476) |
| Loại báo giá | select | Báo giá thường / Báo giá tổng (L:440-443; BE S:4453-4459) |
| Cấp duyệt | select | Cấp 1 — Tự duyệt / Cấp 2 — TP duyệt / Cấp 3 — BGĐ duyệt (L:477-481) |
| Người duyệt | select nhân viên | lọc `approved_by` (S:4471-4473) |
| Giai đoạn dự án | select kèm icon ⓘ mô tả giai đoạn | giai đoạn đã khoá vẫn hiện khi đang lọc |
| Ngày tạo | khoảng ngày (1 ô) | `created_from` / `created_to` so theo ngày (S:4482-4487) |
- Nút "Làm mới" xoá hết điều kiện lọc rồi tải lại (L:1308-1320).

### 4.4 Thanh công cụ (L:88-125)
- **Tạo báo giá** (xanh dương primary, icon +) → màn Tạo mới `/assign/quotations/create`. Không gate quyền.
- **Xuất Excel** (xanh lá, icon excel) → mở popup "Chọn trường xuất file", tick sẵn các cột đang hiện.
- Nút icon **Cấu hình cột hiển thị**.

### 4.5 Cột Hành động (L:1135-1205; component `V2BaseRowActions` — tối đa 3 nút hiện thẳng, nếu >3 thì 2 nút đầu hiện thẳng + nút "…" chứa phần còn lại; `components/V2BaseRowActions.vue:86-110`). Nút không đủ điều kiện → ẨN.
| Thứ tự | Nút (tooltip) | Icon | Điều kiện hiện |
|---|---|---|---|
| 1 | **Sửa / Làm giá** → màn sửa | ri-edit-line | Đang tạo + mình là người tạo |
| 2 | **Xóa** (màu đỏ) | ri-delete-bin-line | Đang tạo + mình là người tạo |
| 3 | **Sao chép báo giá** | ri-file-copy-line | `canCopyQuotation` (mục 2.4) — mọi trạng thái |
| 4 | **Chốt báo giá (Trúng thầu)** | ri-checkbox-circle-line | `can_finalize`: báo giá KHÔNG gắn dự án, không phải báo giá tổng, Đã duyệt, mình là người lập (Q:357-362) |
| 5 | **Hủy chốt** | ri-arrow-go-back-line | `can_unfinalize`: không gắn dự án, Trúng thầu, CHƯA có hợp đồng, mình là người lập (Q:365-371) |
| 6 | **Lập hợp đồng** → `/assign/contracts/create?quotation_id=` | ri-file-add-line | Trúng thầu + chưa có HĐ + mình là người lập |
| 7 | **Xem hợp đồng** | ri-eye-line | Đã có hợp đồng |
| 8 | **In báo giá** → popup cấu hình in → xem trước | ri-printer-line | Luôn hiện |
| 9 | **Lịch sử** → popup lịch sử báo giá | ri-history-line | Luôn hiện |
- KHÔNG có nút "Xem" — bấm Mã báo giá để xem.
- Ví dụ báo giá Đang tạo của mình: hiện Sửa, Xóa + "…" (Sao chép, In báo giá, Lịch sử). Báo giá của người khác: Sao chép (nếu đủ điều kiện), In báo giá, Lịch sử.
- In lỗi tải chi tiết: toast "Không tải được chi tiết báo giá" (L:957).

### 4.6 Xuất Excel danh sách
- FE gọi `GET assign/quotations/export-list?<bộ lọc>&fields=a,b,c` → file **`danh_sach_bao_gia.xlsx`**, tiêu đề sheet "Danh sách báo giá" (C:58-76, L:1240-1268).
- Lấy TẤT CẢ dòng theo bộ lọc + phạm vi quyền, KHÔNG giới hạn số dòng, KHÔNG phân trang (C:61 `->get()`).
- Popup chọn cột gồm 20 trường (L:586-609): Mã báo giá · Tên báo giá · Loại báo giá · Mã YCBG · Dự án TKT · Mã BOM · Khách hàng · Version giải pháp · Giai đoạn dự án · Tiền tệ · Tổng giá trị sau VAT · Cấp duyệt · Người duyệt · Ngày duyệt · Trạng thái · Trạng thái đồng bộ ERP · Người tạo · Ngày tạo · Người cập nhật · Ngày cập nhật. (BE còn có "Ngày gửi duyệt" — `app/ExcelExport/ExportColumnRegistry.php:999-1021`.) Không chọn cột nào hợp lệ → xuất đủ mọi cột.
- Thành công: toast **"Xuất Excel thành công"**; lỗi: **"Lỗi khi xuất Excel"** (không hiện khi 403) (L:1259-1263).
- ⚠️ Cột "Trạng thái đồng bộ ERP" xuất giá trị thô `success`/`failed`.

---

## 5. Xoá báo giá

- **Điều kiện** (BE `S:1783-1802` → `ensureEditableByCreator` S:4719-4727): trạng thái **Đang tạo** VÀ người thao tác là **người tạo**. Không cần quyền riêng, route không gắn middleware (RT:640). Không có accessor `is_can_delete`.
  - Lỗi trả về: `Báo giá không ở trạng thái Đang tạo, không thể sửa.` / `Chỉ người tạo báo giá mới có thể sửa.` (chữ "sửa" dùng chung cho xoá).
- **Nơi có nút**: cột Hành động màn danh sách (nút "Xóa") + footer màn chi tiết (nút đỏ "**Xoá**", D:725-728). Cùng điều kiện ở 2 nơi.
- **Hộp xác nhận** (dùng `$bvModal.msgBoxConfirm`, L:1273-1280 và D:1353-1360):
  - Tiêu đề: **Xác nhận xoá**
  - Nội dung: **Bạn có chắc muốn xoá báo giá '{Mã báo giá}'?** (mã nằm trong nháy đơn)
  - Nút: **Xoá** (đỏ) · **Huỷ**
- **Kết quả**:
  - Thành công: BE message `Đã xoá báo giá` (C:633); FE toast **"Đã xoá báo giá"**. Ở danh sách: tải lại danh sách; ở chi tiết: về `/assign/quotations`.
  - Lỗi: toast = message BE, mặc định **"Xoá thất bại"**.
- **Xoá cứng** (không xoá mềm). Trong transaction (S:1787-1801):
  - Xoá các dòng giá hàng hoá `quotation_product_prices` của báo giá;
  - Xoá TOÀN BỘ lịch sử `quotation_histories` của báo giá (⇒ KHÔNG còn vết lịch sử, không ghi log việc xoá);
  - Xoá bản ghi báo giá;
  - Nếu báo giá lập từ YCBG và YCBG đó không còn báo giá nào khác → YCBG trả về trạng thái **"Chờ XD giá"** (`PricingRequest::STATUS_CHO_XD_GIA`).
  - ⚠️ Code KHÔNG xoá dịch vụ (`quotation_service_items`), dòng giảm giá (`quotation_discounts`), nhóm hàng (`quotation_groups`) và DB không có khoá ngoại cascade → các dòng này còn lại mồ côi (kiểm `information_schema` local: chỉ `hrm_contracts.quotation_id` tham chiếu `quotations`, NO ACTION). Không ảnh hưởng người dùng.

---

## 6. Duyệt / Từ chối / Gửi duyệt

### 6.1 Màn Báo giá chờ duyệt (FE P)
- Tiêu đề trang + bảng: **"Báo giá chờ duyệt"** (P:47, P:331-333). Bên trái bảng có nhãn đếm **"Tổng: {n}"** (P:85-89).
- Rỗng: **"Không có báo giá nào chờ duyệt."** (P:53). Lỗi: "Lỗi tải dữ liệu".
- 20 dòng/trang. Sắp xếp mặc định **Ngày gửi duyệt giảm dần** (P:267-268).
- **Ô tìm nhanh**: "Tìm theo mã báo giá, tên khách hàng" (mã báo giá / tên KH).
- **Bộ lọc** (P:342-376): Công ty / Phòng ban / Bộ phận / Người lập · **Dự án TKT** (select nạp toàn bộ dự án) · **Giai đoạn dự án** · **Cấp duyệt** (chỉ 2 giá trị: "Cấp 2 — TP duyệt", "Cấp 3 — TP & BGĐ duyệt", P:307-310) · **Ngày tạo** (khoảng). KHÔNG có ô Trạng thái (máy chủ đã lọc theo hàng chờ).
- **Cột** (P:433-610, mặc định hiện hết, có Cấu hình cột): STT · Mã báo giá (link → chi tiết kèm `?from=pending-approval`) · Loại báo giá · BOM list · Dự án TKT · Khách hàng · Giai đoạn dự án · Tiền tệ · Tổng giá trị sau VAT · Cấp duyệt · **Người gửi duyệt** (thực chất là người tạo — chỉ người tạo mới gửi duyệt được) · **Ngày gửi duyệt** · Ngày tạo · Người cập nhật · Ngày cập nhật · Trạng thái · Hành động. Sắp xếp được: Mã, Khách hàng, Tổng giá trị, Cấp duyệt, Ngày gửi duyệt, Ngày tạo, Ngày cập nhật, Trạng thái.
- **Thanh công cụ**: Xuất Excel (file `danh_sach_bao_gia_cho_duyet.xlsx`, sheet "Danh sách báo giá chờ duyệt", C:94-112; popup chọn 15 trường P:391-409) + Cấu hình cột. Không có nút Tạo.
- **Hành động dòng** (P:772-790): **Duyệt** (icon `ri-check-double-line`) = điều hướng sang màn chi tiết để duyệt (không duyệt ngay tại dòng) · **Lịch sử**.

### 6.2 Nút trên footer màn Chi tiết (D:671-773), thứ tự trái → phải
Quay lại · Xuất Excel · In · Sao chép* · Sửa / Làm giá* · Xoá* · **Duyệt** hoặc **Duyệt & chuyển BGĐ*** · **BGĐ duyệt*** · **Từ chối*** · Chốt báo giá (Trúng thầu)* · Hủy chốt* · Lập hợp đồng* / Xem hợp đồng* (* = có điều kiện).
- Nhãn nút TP: cấp 3 → **"Duyệt & chuyển BGĐ"**, cấp 2 → **"Duyệt"** (D:730-733).
- Tiêu đề trang chi tiết: `Chi tiết báo giá: {Mã} ({Trạng thái}) {Cấp 1 — Tự duyệt | Cấp 2 — TP duyệt | Cấp 3 — TP & BGĐ duyệt}` (D:909-930).

### 6.3 Duyệt TP
- Xác nhận (D:1549-1555, `$bvModal.msgBoxConfirm`): tiêu đề **"Xác nhận duyệt"**; nội dung **"Duyệt & chuyển BGĐ?"** (cấp 3) hoặc **"Duyệt báo giá?"** (cấp 2); nút **Duyệt** / **Huỷ**.
- BE (S:3960-4009): kiểm quyền → phòng ban → trạng thái (`Báo giá không ở trạng thái Chờ TP duyệt.`). Tính lại tổng tiền.
  - Cấp 3: → **Chờ BGĐ duyệt**, lưu người/ngày TP duyệt; lịch sử "TP duyệt & chuyển BGĐ"; thông báo cho BGĐ.
  - Cấp 2: → **Đã duyệt**, lưu người/ngày duyệt; YCBG (nếu có) → "Đã có báo giá"; dự án TKT → tiến trình **"Thương thảo giá"**, tính lại mốc tự đóng dự án; giải pháp → "Đã duyệt giá" (S:4057-4067); lịch sử "TP duyệt"; thông báo đã duyệt; đồng bộ ERP.
- Thông báo kết quả: BE `Đã duyệt báo giá` (C:679); FE toast **"Đã duyệt báo giá"**; lỗi mặc định **"Lỗi duyệt"**. Xong → quay về hàng chờ (nếu vào từ đó) hoặc trang trước (D:1321-1328).

### 6.4 Duyệt BGĐ
- Xác nhận: tiêu đề **"Xác nhận duyệt"**, nội dung **"BGĐ duyệt báo giá?"**, nút **Duyệt** / **Huỷ** (D:1569-1575).
- BE (S:4011-4043): quyền → công ty → trạng thái (`Báo giá không ở trạng thái Chờ BGĐ duyệt.`) → **Đã duyệt** + các tác động như duyệt cấp 2; lịch sử "BGĐ duyệt"; thông báo; đồng bộ ERP.
- FE toast **"BGĐ đã duyệt báo giá"** (D:1582); lỗi "Lỗi duyệt".

### 6.5 Từ chối
- Popup `components/assign/quotation/QuotationRejectModal.vue` (b-modal):
  - Tiêu đề: **"Từ chối báo giá"**
  - Trường **"Lý do từ chối"** (bắt buộc, dấu *), textarea 4 dòng, placeholder **"Nhập lý do từ chối..."**
  - Bỏ trống bấm xác nhận → chữ đỏ **"Vui lòng nhập lý do từ chối"** (FE, không có dấu chấm).
  - Nút: **Huỷ** · **Xác nhận từ chối** (đỏ; khi đang gửi: "Đang gửi...").
- BE `QuotationRejectRequest.php`: `reason` = bắt buộc, chuỗi, **tối đa 1000 ký tự**; message thiếu: `Vui lòng nhập lý do từ chối.`; vượt 1000 → BE trả lỗi validate 422 (câu chuẩn lang file `Vui lòng nhập tối đa 1000 ký tự.` nằm trong `errors.reason`; toast FE hiện `message` của response — chưa kiểm thực tế câu hiển thị). FE không chặn độ dài trước. Service còn chặn chuỗi toàn khoảng trắng (S:4080-4082).
- Điều kiện trạng thái: `Báo giá không ở trạng thái chờ duyệt.` (S:4071-4073); thiếu quyền: `Bạn không có quyền "Trưởng phòng duyệt giá Bom giải pháp".` / `...Ban giám đốc...` (S:4787-4792).
- Kết quả (S:4084-4104): trạng thái → **Đang tạo**; lưu lý do; XOÁ ngày gửi duyệt, người/ngày TP duyệt, người/ngày duyệt, **cấp duyệt** (phải gửi duyệt lại từ đầu, cấp duyệt tính lại). Lịch sử "Từ chối" kèm lý do. Thông báo.
- FE toast **"Đã từ chối báo giá"**; lỗi mặc định **"Không thể từ chối"**; xong → quay về hàng chờ/trang trước.
- Người tạo mở lại báo giá thấy dải đỏ **"Đã bị từ chối: {lý do}"** (D:8-10); lý do bị xoá khi gửi duyệt lại (S:3911).

### 6.6 Gửi duyệt (thực hiện ở màn Tạo mới/Sửa — tóm tắt phần liên quan duyệt)
- Nút **"Gửi duyệt"** (icon máy bay giấy) ở footer màn Tạo/Sửa, cạnh "Lưu nháp" (E:1239-1247), chỉ khi `canEdit`.
- Trước popup, FE kiểm: lệch Báo giá Mỏ neo → popup **"Không thể trình duyệt — vi phạm quy tắc đồng bộ"** (E:1280); có mặt hàng đơn giá bán ≤ 1.000 → tô cam + popup cảnh báo, user chọn "Tiếp tục gửi duyệt" (không chặn) (E:4028-4044).
- Popup **"Gửi duyệt báo giá"** (QuotationSubmitModal.vue): Tổng giá nhập (cần quyền giá vốn) · Tổng giá bán · Tổng giảm giá + Tổng bán sau GG (khi có GG) · Tỷ suất LN (cần quyền giá vốn; màu xanh ≥20%, cam ≥10%, đỏ <10%) · **Cấp duyệt dự kiến** ("Cấp N" / "Tự động duyệt"). Câu thông báo:
  - Cấp 1: "Theo quy chế, bạn có thể tự duyệt báo giá này."
  - Cấp 2: "Theo quy chế, báo giá cần gửi tới Trưởng phòng duyệt."
  - Cấp 3: "Theo quy chế, báo giá cần gửi qua 2 cấp duyệt:" + 2 bước "1 Trưởng phòng duyệt & chuyển BGĐ → 2 Ban giám đốc duyệt".
  - Nút: **Xác nhận duyệt** (cấp 1) / **Xác nhận gửi** (cấp 2-3) · **Huỷ**. Đang tính: "Đang tính cấp duyệt..."; không tính được: "Không tính được cấp duyệt. Vui lòng kiểm tra giá sản phẩm."
- Màn Tạo mới: chưa có bản ghi → BE xem trước bằng `preview-submit` (không ghi DB), xác nhận mới `create-and-submit` tạo + gửi duyệt (+ tự duyệt nếu cấp 1) trong 1 lượt (C:324-360, S:3824-3881). Bị chặn → popup hiện nguyên văn lý do BE (E:4084-4088), mặc định "Không thể gửi duyệt báo giá".
- **Điều kiện chặn gửi duyệt** (S:3796-3814, nguyên văn):
  1. Không phải người tạo / không ở Đang tạo (như Sửa).
  2. `Vui lòng nhập điều khoản thanh toán trước khi gửi duyệt.`
  3. Báo giá gắn dự án mà chưa chọn giai đoạn: `Vui lòng chọn giai đoạn dự án trước khi gửi duyệt.`
  4. `Có {n} sản phẩm/dịch vụ chưa hợp lệ (giá bán > 0, số lượng > 0, giảm giá ≤ đơn giá bán).` (S:4729-4785: hàng không phải con phải có giá bán > 0; hàng tự nhập (không ERP, không phải cha) phải có giá nhập > 0; GG theo mặt hàng ≤ đơn giá; dịch vụ phải có tên, SL > 0, giá bán > 0, GG ≤ đơn giá.)
  5. `Giá bán hàng cha "{tên}" phải ≥ tổng giá bán hàng con.`
  6. `Giá vốn hàng cha "{tên}" đang nhỏ hơn tổng giá vốn hàng con.`
  7. Lệch Báo giá Mỏ neo của dự án cha: `KHÔNG THỂ TRÌNH DUYỆT — báo giá không khớp với Báo giá Mỏ neo {mã}, không đủ điều kiện tổng hợp hợp đồng.` + danh sách "• lỗi" (S:3767-3789).
  8. (create-and-submit) `Cấp duyệt của báo giá vừa thay đổi thành cấp 1 (tự duyệt). Vui lòng bấm Gửi duyệt lại để xác nhận.` (S:3866)
  9. Tự duyệt sai cấp: `Báo giá này không thuộc cấp tự duyệt.` (S:3927)
- Khi gửi duyệt (S:3883-3921): đồng bộ giai đoạn dự án về Dự án TKT; tính lại tổng; tính **ngày hiệu lực báo giá** = MIN(hôm nay + số ngày cấu hình ERP `quotation_valid_days` (mặc định 30), ngày điều chỉnh giá ERP gần nhất của hàng hoá) (S:5141-5185); tính cấp. Cấp 1 → chỉ lưu cấp, chờ người tạo bấm tự duyệt. Cấp 2/3 → **Chờ TP duyệt**, lưu ngày gửi, lịch sử "Gửi duyệt" (kèm cấp), thông báo TP.
- Toast: **"Đã tự duyệt báo giá"** / **"Đã gửi duyệt báo giá"**; lỗi mặc định **"Không thể gửi duyệt"**. Xong → về `/assign/quotations` (E:4094-4096).
- Tự duyệt (S:3923-3958): → **Đã duyệt** + tác động như duyệt (YCBG, dự án, giải pháp), lịch sử "Tự duyệt", thông báo đã duyệt, đồng bộ ERP.

### 6.7 Thông báo (chuông) — `S:5054-5139`
| Sự kiện | Người nhận | Nội dung (title) | Link |
|---|---|---|---|
| Gửi duyệt cấp 2/3 | NV có quyền "Trưởng phòng duyệt giá Bom giải pháp" thuộc/quản lý **đúng phòng ban + công ty của báo giá** (`EmployeeInfoService::listEmployeeInfoByPermissionAndDepartment`) | `**{Tên người gửi}** gửi duyệt báo giá (cấp TP) **{Mã}**` hoặc `(cấp TP + BGĐ)` | `/assign/quotations/pending-approval` |
| TP duyệt & chuyển BGĐ | NV có quyền "Ban giám đốc duyệt giá Bom giải pháp" trong role của **đúng công ty báo giá** và hồ sơ thuộc công ty đó (S:5026-5052) | `**{Tên TP}** TP đã duyệt & chuyển BGĐ **{Mã}**` | `/assign/quotations/pending-approval` |
| Đã duyệt (tự duyệt / TP cấp 2 / BGĐ) | Người lập báo giá + NV KD phụ trách dự án + các TP duyệt giá của phòng ban báo giá (gộp, không trùng) | `**{Tên người duyệt}** đã duyệt báo giá **{Mã}**` | `/assign/quotations/{id}` |
| Từ chối | Người lập; nếu từ chối ở bước BGĐ thì thêm TP đã duyệt trước đó | `**{Tên}** từ chối báo giá **{Mã}**. Lý do: {lý do}` | `/assign/quotations/{id}` |
| Dừng do điều chỉnh giải pháp | Người tạo báo giá | (SolutionAdjustmentRequestService::notifyQuotationCreatorStopped) | |
- Tên người gửi = họ + tên NV (S:4971-4983). Lỗi gửi thông báo không làm hỏng thao tác (try/catch, chỉ ghi log).
- Chốt / Hủy chốt: KHÔNG gửi thông báo.

### 6.8 Đồng bộ ERP
- Chạy ngay sau khi báo giá **chuyển sang Đã duyệt** (tự duyệt, TP duyệt cấp 2, BGĐ duyệt) — `syncToErpAfterApproval` S:4045-4055 → `QuotationErpSyncService::sync` (`Modules/Assign/Services/QuotationErpSyncService.php:19-70`). TP "duyệt & chuyển BGĐ" không đồng bộ.
- Đẩy sang ERP `POST /api/v1/firm-quotations/sync-from-hrm` (báo giá chính thức), tạo hàng tạm / chi phí trên ERP nếu cần. Thành công: lưu `erp_firm_quotation_id`, `erp_sync_status = success` → cột "Đồng bộ ERP" = **"Đã đồng bộ"**.
- Thất bại (không chặn duyệt): `erp_sync_status = failed`, lưu lỗi → badge **"Thất bại"** (tooltip lỗi). Lỗi điển hình: `Không tìm thấy khách hàng ERP: code=..., tax=...`; `Khách hàng ERP (ID=...) chưa có địa chỉ giao hàng`.
- Nút đồng bộ lại (`retry-sync`) hiện **TẠM TẮT**: BE luôn trả 422 `Tính năng đồng bộ báo giá đang tạm tắt.` (C:1889-1894); FE không có nút gọi (hàm `retrySync` L:1335 không được dùng trên giao diện).

---

## 7. Chốt / Hủy chốt (Trúng thầu) — chỉ báo giá KHÔNG gắn Dự án TKT trên màn này

(Báo giá có dự án chốt/hủy chốt ở tab Báo giá của màn Dự án TKT — chỉ Sale phụ trách dự án.)

### 7.1 Chốt báo giá (Trúng thầu)
- Nút: danh sách (hành động "Chốt báo giá (Trúng thầu)") + footer chi tiết (nút xanh "**Chốt báo giá (Trúng thầu)**", D:744-747). Điều kiện: cờ `can_finalize` (Đã duyệt + không dự án + không phải BG tổng + mình là người lập).
- Popup `components/assign/prospective-project/FinalizeQuotationModal.vue` (khuôn V2BaseModal, size lg):
  - Tiêu đề **"Xác nhận chốt báo giá"**, dòng phụ "Báo giá: {Mã}", icon tích tròn.
  - Nội dung: **"Chốt báo giá {Mã} thành Trúng thầu?"** (báo giá có dự án thêm: "Mỗi dự án chỉ có 1 báo giá trúng thầu.").
  - Bảng đính kèm **"File xác nhận của khách hàng"** (bắt buộc). Thiếu: **"Vui lòng đính kèm file xác nhận của khách hàng"**.
  - Nút: **Chốt** (đang chạy "Đang chốt...") · **Huỷ**.
- BE `QuotationFinalizeRequest.php`: `files` bắt buộc ≥1 (`Vui lòng đính kèm file xác nhận của khách hàng`), mỗi file phải có `file_path` (`File chưa tải lên xong, vui lòng thử lại`), tên file ≤255.
- Service S:4107-4159: chỉ Đã duyệt (`Chỉ chốt được báo giá đã duyệt.`); báo giá có dự án mà dự án đã có báo giá trúng thầu khác → `Dự án đã có báo giá trúng thầu, vui lòng hủy chốt trước.`. → **Trúng thầu**; lưu file vào bảng files (mô tả "Xác nhận chốt báo giá"); dự án (nếu có) tiến lên "Thương thảo hợp đồng"; lịch sử "Chốt".
- Toast **"Đã chốt báo giá (Trúng thầu)"**; lỗi mặc định **"Lỗi chốt báo giá"**. Danh sách tải lại.

### 7.2 Hủy chốt
- Nút "**Hủy chốt**" (danh sách + footer chi tiết D:748-751). Điều kiện `can_unfinalize` (Trúng thầu + chưa lập hợp đồng + không dự án + mình là người lập).
- Popup `components/assign/quotation/UnfinalizeQuotationModal.vue`: tiêu đề **"Hủy chốt báo giá"**; nội dung **"Hủy chốt báo giá {Mã} — báo giá sẽ quay lại trạng thái "Đã duyệt"."**; trường **"Lý do hủy chốt"** (bắt buộc, textarea 4 dòng) — thiếu: **"Bắt buộc phải nhập"**; nút **Hủy chốt** (đỏ, "Đang lưu...") · **Huỷ**.
- BE `QuotationUnfinalizeRequest.php`: `reason` bắt buộc, ≤1000 ký tự (`Vui lòng nhập lý do hủy chốt.`). Service S:4161-4210: phải đang Trúng thầu (`Báo giá chưa ở trạng thái trúng thầu.`); không dự án mà đã có HĐ → `Báo giá đã lập hợp đồng, không thể hủy chốt.`. → **Đã duyệt**; XOÁ file xác nhận của lần chốt; dự án lùi về "Thương thảo giá" nếu đang đúng ở "Thương thảo hợp đồng"; lịch sử "Hủy chốt" kèm lý do.
- Toast **"Đã hủy chốt báo giá"**; lỗi mặc định **"Lỗi hủy chốt"**.
- Thao tác chốt/hủy chốt của người không phải người lập → `Chỉ người lập báo giá mới được thao tác.` (C:1337-1339).

---

## 8. Tổng hợp thông báo nguyên văn

### Thành công (toast FE / message BE)
| Thao tác | FE toast | BE message |
|---|---|---|
| Xoá | Đã xoá báo giá | Đã xoá báo giá |
| Gửi duyệt cấp 2/3 | Đã gửi duyệt báo giá | Đã gửi duyệt báo giá |
| Tự duyệt | Đã tự duyệt báo giá | Đã tự duyệt báo giá |
| TP duyệt (cả "Duyệt & chuyển BGĐ") | Đã duyệt báo giá | Đã duyệt báo giá |
| BGĐ duyệt | BGĐ đã duyệt báo giá | Đã duyệt báo giá |
| Từ chối | Đã từ chối báo giá | Đã từ chối báo giá |
| Chốt | Đã chốt báo giá (Trúng thầu) | Đã chốt báo giá (Trúng thầu) |
| Hủy chốt | Đã hủy chốt báo giá | Đã hủy chốt báo giá |
| Xuất Excel | Xuất Excel thành công | — |
| Lưu ghi chú KD | Đã lưu ghi chú | Đã cập nhật ghi chú |

### Lỗi
- Danh sách: `Lỗi tải dữ liệu` · Xuất: `Lỗi khi xuất Excel` · In: `Không tải được chi tiết báo giá` · Xoá: `Xoá thất bại` · Duyệt: `Lỗi duyệt` · Từ chối: `Không thể từ chối` · Gửi duyệt: `Không thể gửi duyệt` / `Không thể gửi duyệt báo giá` / `Không tính được cấp duyệt` / `Không tính được cấp duyệt. Vui lòng kiểm tra giá sản phẩm.` · Chốt: `Lỗi chốt báo giá` · Hủy chốt: `Lỗi hủy chốt` · Sao chép: `Không kiểm tra được thay đổi từ ERP`.
- BE nghiệp vụ (nguyên văn):
  - `Không tìm thấy báo giá.`
  - `Báo giá không ở trạng thái Đang tạo, không thể sửa.`
  - `Chỉ người tạo báo giá mới có thể sửa.`
  - `Bạn không phải Sale phụ trách dự án này`
  - `Bạn không có quyền xây dựng giá bán theo phòng.` / `Bạn không có quyền xây dựng giá bán theo công ty.` / `Yêu cầu xây dựng giá này không thuộc phòng ban của bạn.`
  - `Chỉ người lập báo giá mới được sao chép.` · `Chỉ người lập báo giá mới được thao tác.`
  - `Bạn không có quyền áp dụng giảm giá trong báo giá`
  - `Vui lòng nhập điều khoản thanh toán trước khi gửi duyệt.` · `Vui lòng chọn giai đoạn dự án trước khi gửi duyệt.`
  - `Có {n} sản phẩm/dịch vụ chưa hợp lệ (giá bán > 0, số lượng > 0, giảm giá ≤ đơn giá bán).`
  - `Giá bán hàng cha "{tên}" phải ≥ tổng giá bán hàng con.` · `Giá vốn hàng cha "{tên}" đang nhỏ hơn tổng giá vốn hàng con.`
  - `KHÔNG THỂ TRÌNH DUYỆT — báo giá không khớp với Báo giá Mỏ neo {mã}, không đủ điều kiện tổng hợp hợp đồng.`
  - `Báo giá này không thuộc cấp tự duyệt.` · `Cấp duyệt của báo giá vừa thay đổi thành cấp 1 (tự duyệt). Vui lòng bấm Gửi duyệt lại để xác nhận.`
  - `Bạn không có quyền "Trưởng phòng duyệt giá Bom giải pháp".` · `Bạn không có quyền "Ban giám đốc duyệt giá Bom giải pháp".`
  - `Bạn không quản lý phòng ban của báo giá này.` · `Bạn không thuộc công ty của báo giá này.`
  - `Báo giá không ở trạng thái Chờ TP duyệt.` · `Báo giá không ở trạng thái Chờ BGĐ duyệt.` · `Báo giá không ở trạng thái chờ duyệt.`
  - `Vui lòng nhập lý do từ chối.` (FE: `Vui lòng nhập lý do từ chối`)
  - `Chỉ chốt được báo giá đã duyệt.` · `Dự án đã có báo giá trúng thầu, vui lòng hủy chốt trước.` · `Vui lòng đính kèm file xác nhận của khách hàng` · `File chưa tải lên xong, vui lòng thử lại`
  - `Báo giá chưa ở trạng thái trúng thầu.` · `Vui lòng nhập lý do hủy chốt.` · `Báo giá đã lập hợp đồng, không thể hủy chốt.`
  - `Chỉ có thể sửa ghi chú khi báo giá đã duyệt.` · `Chỉ người lập báo giá mới có thể cập nhật ghi chú.` · `Chỉ NV Kinh doanh phụ trách dự án mới có thể cập nhật ghi chú.`
  - `Tính năng đồng bộ báo giá đang tạm tắt.`

---

## 9. Lịch sử (ghi khi nào) — `Modules/Assign/Entities/QuotationHistory.php:19-61`
Nhãn hành động: Tạo mới · Thay đổi thông tin · Gửi duyệt · Tự duyệt · TP duyệt · TP duyệt & chuyển BGĐ · BGĐ duyệt · Từ chối · Cập nhật ghi chú KD · Áp dụng VAT đồng loạt · Import giá · Đóng theo dự án · Cập nhật giảm giá · Chốt · Hủy chốt · Hết hiệu lực. Xem ở nút "Lịch sử" (danh sách, hàng chờ) và mục "Thông tin hệ thống"/Lịch sử cuối màn chi tiết (D:820). Xoá báo giá thì lịch sử bị xoá theo (không có nhãn "Xoá").

## 10. Điểm lệch/cần lưu ý khi viết SRS (để QA không bất ngờ)
1. Menu "Báo giá chờ duyệt" có thể hiện với người không có quyền (mục 1.2) — vào sẽ bị máy chủ từ chối (403).
2. Nút "Tạo báo giá" không gate quyền; quyền thật nằm ở việc chọn dự án (Sale phụ trách) / YCBG.
3. Nút Duyệt/Từ chối ở chi tiết chỉ xét quyền + trạng thái; TP khác phòng / BGĐ khác công ty vẫn thấy nút nhưng bấm sẽ báo lỗi phòng ban/công ty.
4. Hộp xác nhận Xoá/Duyệt dùng hộp thoại mặc định Bootstrap (`msgBoxConfirm`), không phải popup xác nhận chuẩn của hệ thống.
5. Ngưỡng cấp duyệt lấy từ cấu hình (DB hiện tại: V 1 tỷ/20 tỷ; M và M hàng tạm 35%/20%), seed gốc M = 20%/10%.
6. Trạng thái "Đóng" cascade cả báo giá Đã duyệt/Trúng thầu khi đóng dự án (khác comment Entity).
7. Xuất Excel danh sách không giới hạn số dòng.
