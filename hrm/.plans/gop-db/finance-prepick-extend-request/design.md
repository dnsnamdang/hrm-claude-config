# Thiết kế — Port màn "Yêu cầu gia hạn hàng giữ" ERP → HRM

Feature: `finance-prepick-extend-request` · Nhánh: `feat/finance-prepick-extend-request` · @junfoke
Ngày khảo sát: 2026-08-22. Nguồn nghiệp vụ: `TanPhatDev` (ERP). Nguồn giao diện: HRM (skill
`erp-to-hrm-screen` — ERP là nguồn NGHIỆP VỤ, HRM là nguồn GIAO DIỆN).

Đây là màn thứ 4 của nhóm **Giữ hàng** được port, sau `Danh sách hàng giữ`,
`Yêu cầu hủy hàng giữ`, `Phiếu hủy hàng giữ` (xem `../finance-prepick-cancel-request/`).

---

## 1. Chốt phạm vi (user duyệt 2026-08-22)

| Điểm | Chốt |
|---|---|
| Thứ tự | Gia hạn **trước**, Điều chuyển sau (gia hạn không đổi chủ lô) |
| Nhánh | **2 nhánh riêng**, 2 thư mục `.plans` — 2 màn độc lập, nghiệm thu từng màn |
| Quyền xem | **Giữ đúng ERP**: 3 cấp `Xem phiếu hàng giữ theo tổng công ty / công ty / phòng ban`. KHÔNG thêm cấp bộ phận |
| 2 lối vào ERP (`index` + `forAccounting`) | **Gộp về 1 màn**, nút duyệt hiện theo quyền — đúng rule đã áp cho các màn trước |

- Phân hệ: **Tài chính**, nhóm menu **Giữ hàng** (`components/subsystem-menu/finance.js:174`,
  mục "Yêu cầu gia hạn hàng giữ" hiện đang **không có link**).
- Route HRM: `/finance/prepick-extend-requests`
- Bảng: `prepick_extend_requests` (**1.421 phiếu**) + `prepick_extend_request_details` (**31.437 dòng**),
  0 dòng mồ côi trên dev. Mã phiếu `PGHHG-xxxxx`.

## 2. Bảng nghiệp vụ (bước 1 của skill — chỉ lấy nghiệp vụ ERP)

### 2.1 Màn danh sách

| Cột ERP | Ghi chú port |
|---|---|
| STT · Mã phiếu · Người lập · Ngày lập · Trạng thái · Người duyệt · Ngày duyệt · Hành động | Giữ nguyên. Mã phiếu là `<nuxt-link>` sang chi tiết |

Bộ lọc ERP: `code` (text) · `created_by` (select NV) · `status` (select 5 giá trị) ·
`approver` (select NV) · `productName` (text) · `productCode` (text) · **`search_by_time`**
(khoảng ngày) · `search_by_info` (khối công ty/phòng ban).

⚠️ 6 ô lọc > 3 → bắt buộc `V2BaseSmartFilterPanel` + schema `filterFields`.

### 2.2 Hành động mỗi dòng + ĐIỀU KIỆN (ghi cả điều kiện — bẫy số 1 khi port)

| Hành động | Điều kiện ERP |
|---|---|
| Sửa · Xóa | `canEdit()` = `status == 3` **và** `created_by == user` |
| Duyệt | `canApprove() \|\| canBKSApprove() \|\| canTPApprove()` (xem §3) |
| In · Xuất Excel | `canView()` |

`canView()` = (có 1 trong 3 quyền duyệt **và** `status != 3` **và** cùng công ty) **hoặc** là người lập.

### 2.3 Màn form (Thêm / Sửa) — bảng chi tiết

STT · ☑ Cần gia hạn · Tên hàng hóa · Khách hàng · **Hợp đồng** · ĐVT · Có thể giữ ·
Đang giữ · **Cần gia hạn (SL)** · Ngày bắt đầu giữ · Hạn giữ hiện tại · **Hạn giữ mới (\*)** · Lịch sử.

- Nguồn dòng hàng: `getDataToCreate($employee_id)` — lấy `prepick_details` của **chính nhân viên đó**,
  `qty > 0`, cùng công ty, và **`expire_date <= hôm nay + configs.warning_day`** (local = **7 ngày**).
  Tức là **chỉ hiện lô SẮP hết hạn**, không phải mọi lô đang giữ.
- Cột Hợp đồng suy ra từ `prepick_details.objectable_type`, 3 nhánh:
  `WarehousePrepickRequest` → lần ngược `ProductPrepickRequest.contractable`;
  `PrepickExtendRequestDetail` → `contractable` của chính dòng đó;
  `PrepickTransfer2` → dò `prepick_transfer2_details` theo `parent_id` + `product_id`.
- Trần hạn giữ mới: `configs.max_prepick_date` (local = **30 ngày** kể từ hôm nay).
- Đính kèm: nhiều file, `pdf,png,jpg,jpeg,doc,docx,xls,xlsx`, **≤ 13 MB/file**, lưu qua `CmcS3Helper`.
- Lưu có 2 nút: **Lưu nháp** (`status = 3`) và **Gửi duyệt** (`status = 5`).

## 3. Luồng trạng thái & duyệt 3 cấp

```
3 Đang tạo ──Gửi duyệt──> 5 Chờ TP duyệt ──┬─ checkSwitchApprove() = true ──> 4 Chờ BGĐ duyệt ──> 2 Chờ KT duyệt
                                            └─ false ─────────────────────────────────────────> 2 Chờ KT duyệt
2 Chờ KT duyệt ──Duyệt──> 1 Đã duyệt  (CHÍNH LÚC NÀY mới ghi tồn giữ)
bất kỳ cấp nào ──Từ chối (bắt buộc nhập lý do)──> 3 Đang tạo
```

⚠️ **Trạng thái đánh số không theo thứ tự tự nhiên** — giữ nguyên số của ERP vì 2 cổng dùng chung bảng.
Màu theo SRS: 1 = xanh · 2/4/5 = vàng (chờ duyệt) · **3 "Đang tạo" = XÁM** (ERP đang tô `bg-danger` ĐỎ — sai, phải sửa).

**`checkSwitchApprove()`** quyết định có phải qua BGĐ hay không, xét từng dòng `need_extend`:
- Dòng **có hợp đồng**: tỉ lệ tiền đã thu (`account_details` `account_id = 22`, `type = 2`,
  `invoiceable_type` ∈ {BillIncome, BillAdjustDept, BillIncomeReport}) trên `total_after_vat`
  **< ngưỡng %** cấu hình ở `companies.prepick_contract_types` theo loại HĐ
  (`ban_hang` / `du_an` / `nguyen_tac` / `dich_vu`) → phải qua BGĐ.
- Dòng **không có hợp đồng**: cộng dồn `base_price × extend_qty`, vượt `companies.prepick_other_value`
  (Tân Phát = 20.000.000, chi nhánh = 5.000.000, có công ty = 0) → phải qua BGĐ.

Quyền duyệt: `Trưởng phòng duyệt hàng giữ` (status 5, **và** phòng ban của phiếu phải nằm trong
`employee_manage_departments` của người duyệt, trừ Super Admin) · `Ban giám đốc duyệt hàng giữ`
(status 4) · `Kế toán duyệt hàng giữ` (status 2). Tất cả đều buộc **cùng công ty với phiếu**.

Thông báo: gửi theo QUYỀN (`sendNotifyWithPermission`) cho cấp kế tiếp; từ chối thì báo người lập.

## 4. Ghi tồn giữ khi KT duyệt — `updateWarehouse()`

Gia hạn **KHÔNG phải update `expire_date` tại chỗ**, mà là **chuyển lô**:

1. Bỏ qua dòng `!need_extend`, `!extend_qty`, hoặc `new_expire_date == expire_date` hiện tại.
2. `qty = extend_qty × unit_coefficient` (vì `prepick_details` không có `unit_id`).
3. **Trừ** `qty` ở dòng `prepick_details` cũ + ghi 1 `prepick_logs` (`change = -qty`).
4. Tìm dòng `prepick_details` cùng (`employee_id`, `customer_id`, `product_id`, `expire_date = mới`);
   **không có thì tạo mới** → **cộng** `qty` + ghi 1 `prepick_logs` (`change = +qty`).

`prepick_logs.objectable_type` phải ghi đúng chuỗi lớp ERP `App\Model\Warehouse\PrepickExtendRequestDetail`
thì modal "Lịch sử giữ hàng" bên ERP mới đọc được.

## 5. Lỗi ERP phát hiện — vá khi port

| # | Lỗi | Hậu quả |
|---:|---|---|
| 1 | Dòng `prepick_details` MỚI tạo trong `updateWarehouse()` không set `company_id`; hook `PrepickDetail::created` lấp bằng **công ty của NGƯỜI ĐANG DUYỆT** | Kế toán khác công ty chủ lô duyệt → lô nhảy sang công ty khác, biến mất khỏi Danh sách hàng giữ của chủ lô |
| 2 | `validateProducts()` dùng `$detail->stock->product->name`, `validateApproveProducts()` dùng `$detail->product->name` | 1 trong 2 nhánh nguy cơ 500 khi báo lỗi thiếu hàng |
| 3 | `show()` dựng `approver_comments` với điều kiện `*_approver_id && *_comment` | Duyệt không nhập ghi chú → **mất dòng lịch sử duyệt** (đúng bug đã fix ở màn ĐCHG) |
| 4 | `show()` nhánh KT lấy `$data->comment` nhưng deny/approve ghi vào `approver_comment` | Ghi chú của KT hiển thị sai/rỗng |
| 5 | `store()`/`update()` so `$p['new_expire_date'] > $max_prepick` — so **chuỗi với object Carbon** | Chặn trần hạn giữ không đáng tin |
| 6 | `catch (Exception $e)` thiếu `\` ở `store`/`update`/`approve`/`delete` | Không bắt được lỗi trong namespace |
| 7 | `update()` gõ nhầm `$json->mesage` | Không có quyền sửa → FE không hiện câu báo |
| 8 | Trạng thái "Đang tạo" tô `bg-danger` (ĐỎ) | Nhìn như phiếu bị từ chối — SRS quy định nháp là XÁM |
| 9 | `approve()` nhánh status 5 kiểm `if ($object->status == 4)` **sau khi** vừa gán `= 4` | Điều kiện luôn đúng — vô nghĩa, dễ hiểu nhầm khi đọc |
| 10 | `delete()` xóa cứng cả bảng con | Phiếu đã duyệt không xóa được (đúng), nhưng nên chặn rõ ràng ở BE bằng 423 LOCKED |

## 6. Dùng lại của đợt trước (KHÔNG viết mới)

- `Modules/Finance/Services/PrepickStockService.php` — `availableQtyOfProducts`, `unitCoefficient`,
  `baseUnits`, `holdingCustomers`. **Cần bổ sung** 1 hàm chuyển lô (`moveToExpireDate`) đặt cạnh
  `deductFifo`, vì đây là chỗ DUY NHẤT được chạm `prepick_details` / `prepick_logs`.
- FE: `components/finance/prepick/PrepickStockSearchModal.vue`, `PrepickHistoryPanel.vue`,
  `PrepickHistoryModal.vue`, `PrepickStockLogModal.vue`.
- Bộ 4 quyền có sẵn, **không tạo permission mới**; đọc qua trait `ChecksEmployeePermission`.
- Khuôn 4 màn + checklist UI: skill `erp-to-hrm-screen`.

## 7. Khác ERP có chủ ý

| # | Khác biệt | Lý do |
|---:|---|---|
| 1 | Gộp `index` + `forAccounting` về **1 màn** | User chốt 2026-08-22; nút duyệt hiện theo quyền |
| 2 | Ô ĐVT **khóa**, chỉ hiện chữ | `prepick_details` không có `unit_id`, ERP cũng đã disable sẵn |
| 3 | Lô tồn tra theo **công ty của người lập phiếu**, không phải người duyệt | Vá lỗi #1 |
| 4 | Mẫu in dựng trong `Modules/Finance/Resources/views/prints/`, **không** ghi `report_templates` | Bảng dùng chung với ERP (dù template 423/424 đang có nội dung thật) |
| 5 | Trạng thái "Đang tạo" **xám** | Vá lỗi #8, theo bảng màu SRS |
| 6 | Thêm **Lịch sử thay đổi** (bảng riêng) | ERP không có; đồng bộ với 2 màn hủy đã port |

## 8. Câu hỏi còn mở

1. ~~Đính kèm dùng helper nào?~~ **Đã rõ**: HRM đã có `CmcS3Helper` — mẫu dùng ở
   `Modules/Finance/Services/BillPaymentAttachmentService.php` (`putFiles($files, S3_FOLDER)`,
   mỗi file tên ngẫu nhiên riêng). Bám theo file đó, thư mục S3 `prepick_extend_request`.
2. ~~3 bảng cho `checkSwitchApprove()` có đủ trên DB gộp?~~ **Đã rõ**: `account_details` 971.914 dòng ·
   `firm_contracts` 23.277 · `wr_service_contracts` 6.676 — đủ.
3. ⏳ Bản in ERP dùng khổ **ngang** (`print_landscape`) — **chờ user xác nhận giữ khổ ngang**.
