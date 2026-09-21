# Luồng duyệt Báo giá → Hợp đồng

> Cập nhật: 21/09/2026 — dựng lại từ code thực tế (`Modules/Category` + `hrm-thanhan-client`), không phải từ tài liệu nghiệp vụ.
> Phạm vi: 2 nhánh chính
> 1. Báo giá → Hợp đồng **Trong thầu / Ngoài thầu**
> 2. Báo giá → Hợp đồng **Cho/Tặng, Đặt/Mượn, Nguyên tắc**

---

## 0. Bảng mã tra cứu

### Loại dự toán / báo giá (`project_type`)

| Mã | Tên | Đi nhánh nào |
|---|---|---|
| 1 | Trong thầu | §2 — qua Gói thầu |
| 2 | Ngoài thầu | §3 — thẳng sang Hợp đồng |
| 4 | Hợp đồng Cho/Tặng | §4 |
| 5 | Hợp đồng Đặt/Mượn | §4 |
| 6 | Hợp đồng Nguyên tắc | §4 (code xử lý chung với 4, 5) |

### Trạng thái Báo giá (`Quotation`, `Modules/Category/Entities/Quotation/Quotation.php:90`)

| Mã | Tên |
|---|---|
| 1 | Đang tạo |
| 2 | Chờ duyệt |
| 3 | Đã duyệt |
| 4 | Đã lập hợp đồng |
| 5 | Bị từ chối |
| 6 | Không duyệt |
| 7 | Đã gửi thầu |
| 8 | Đã lập gói thầu |
| 9 | Chuyển hợp đồng |
| 10 | Đang lập hợp đồng |
| 11 | Đang lập gói thầu |
| 12 | Hủy |
| 13 | Chờ BGĐ duyệt |
| 14 | BGĐ duyệt (trung gian, service tự đổi về 3) |
| 15 | TP không duyệt (Dừng dự toán) |
| 16 | BGĐ không duyệt (Dừng dự toán) |
| 17 | Gói thầu đã bị hủy |
| 18 | Gói thầu đã kết xuất |
| 19 | Hủy hợp đồng |
| 20 | Từ chối lập gói thầu |

### Trạng thái Hợp đồng (`Contract`, `Modules/Category/Entities/Contract/Contract.php:125`)

| Mã | Tên |
|---|---|
| 1 | Đang tạo |
| 2 | Chờ duyệt |
| 3 | Đã duyệt |
| 4 | Không duyệt |
| 5 | Hủy hợp đồng |
| 9 | Đã kết xuất cung ứng |
| 10 | Chờ duyệt kết xuất |
| 11 | Không duyệt kết xuất |

- `record_type`: 1 = BB thương thảo, 2 = Hợp đồng, 3 = Phụ lục giảm giá
- `type` (loại HĐ): 1 = Trong thầu, 2 = Ngoài thầu, 3 = Cho/Tặng, 4 = Đặt/Mượn, 5 = Nguyên tắc

### Trạng thái Gói thầu (`BidPackage`, `Modules/Category/Entities/BidPackage/BidPackage.php:93`)

| Mã | Tên |
|---|---|
| 1 | Đang tạo |
| 2 | Đã giao nhân viên |
| 3 | Chờ duyệt kết quả |
| 4 | Kết xuất thầu |
| 8 / 9 | Đang / Đã lập hợp đồng |
| 10 | Đã duyệt kết quả |
| 11 | Không duyệt kết quả |
| 12 | Hủy gói thầu |
| 13 | Chờ BGĐ duyệt |
| 14 | BGĐ duyệt kết quả (trung gian → 10) |
| 15 / 16 | TP / BGĐ không duyệt kết quả |
| 17 | Hủy hợp đồng |

---

## 1. Phần chung: lập và duyệt báo giá (mọi loại)

```
Đang tạo (1) ──gửi duyệt──► Chờ duyệt (2)
                               │
       ┌───────────────────────┼────────────────────────┐
  TP không duyệt          TP duyệt                  Từ chối (5)
  → 15 Dừng dự toán            │
    + dự toán:                 ├─ project_type ∈ {4,5,6}  ─┐
      BAO_GIA_DA_BI_HUY        ├─ hoặc có SP giá ngoài     ├─► Chờ BGĐ duyệt (13)
                               │   khoảng min–max          │      │
                               │                           │  BGĐ duyệt (14) → service set về (3)
                               └─ còn lại ─────────────────┴─► Đã duyệt (3)
                                                                BGĐ không duyệt → 16
```

- Code: `QuotationService::approve()` — `Modules/Category/Services/QuotationService.php:428`
- Route: `PUT /category/quotations/{quotation}/approve`
- Quyền duyệt TP: `Quotation::canApprove()` = status 2 + quyền **TP duyệt báo giá** + người lập nằm trong nhóm mình quản lý (`listManageEmployeeIdsByGroup()`) hoặc là chính mình
- Quyền duyệt BGĐ: `Quotation::canBGDApprove()` = status 13 + quyền **BGĐ duyệt báo giá**
- Điều kiện tự đẩy lên BGĐ (`QuotationService.php:469`):
  - `project_type ∈ {4, 5, 6}` → **luôn luôn** phải qua BGĐ
  - các loại còn lại → chỉ khi có sản phẩm `price` nằm ngoài `price_min`–`price_max` (xét theo `import_type_id` 1 hoặc 2)
- Khi duyệt: ghi `approver_id`, `approved_time`, tạo `HistoryApprovedQuotation`, bắn notification cho người lập
- Nếu ở bước duyệt mà `result = 2` (Không chấp nhận) → báo giá **Hủy (12)**, dự toán về `BAO_GIA_DA_BI_HUY`

### Kết xuất báo giá (render) — điểm rẽ nhánh

- Code: `QuotationService::render()` — `QuotationService.php:651`
- Route: `PUT /category/quotations/{quotation}/render`; màn FE: `pages/plan/quotation/_id/render.vue`
- Quyền: `Quotation::canRender()` = status **3 (Đã duyệt)** + **chính người lập** + quyền **Lập báo giá**
- Nhập ở tab "Tiến độ thực hiện": **Kết quả** (1 = Chấp nhận thực hiện, 2 = Không chấp nhận), lý do, mốc thời gian, file kèm
- Kết quả rẽ nhánh:

| Điều kiện | Báo giá | Dự toán |
|---|---|---|
| `result = 2` | Hủy (12) | `BAO_GIA_DA_BI_HUY` |
| `project_type = 1` | Đã gửi thầu (7), `group_process = 'Thầu'` | `BAO_GIA_DA_GUI_THAU` |
| `project_type ∈ {2, 4, 5, 6}` | Chuyển hợp đồng (9), `group_process = 'Hợp đồng'` | `DA_CHUYEN_HOP_DONG` |

`rendered_at` được ghi tại thời điểm kết xuất.

---

## 2. Nhánh TRONG THẦU (`project_type = 1`) — qua Gói thầu

```
Báo giá: Đã duyệt (3) ──kết xuất──► Đã gửi thầu (7)
                                      │ lập gói thầu (quyền: Lập gói thầu)
                                      ▼
Gói thầu: Đang tạo (1) → Đã giao nhân viên (2)     [BG → Đã lập gói thầu (8)]
            │ nhân viên xử lý + tick SP trúng
            ▼
      Chờ duyệt kết quả (3)
            ├─ TP không duyệt ─────────────────────► 15
            ├─ giá ngoài min–max → Chờ BGĐ duyệt (13) ─BGĐ duyệt (14)─► 10
            │                       └─ BGĐ không duyệt ──────────────► 16
            └─ TP duyệt kết quả ───────────────────────────────────────► Đã duyệt kết quả (10)
                                                                             │ kết xuất thầu
                                                                             ▼
                                                                      Kết xuất thầu (4)
                                                  [BG → Gói thầu đã kết xuất (18), group_process = 'Hợp đồng']
                                                                             │
                                        ┌────────────────────────────────────┼──────────────────────┐
                                Phân công lập HĐ                  Đẩy trả về phòng trước     (Lập BB thương thảo —
                                        │                                                     nút đang bị comment)
                                        ▼
                                 Lập hợp đồng  →  §5 Duyệt hợp đồng
```

- Từ chối lập gói thầu: `QuotationService::rejectBid()` (`:805`) — báo giá **20 (Từ chối lập gói thầu)**, dự toán `TU_CHOI_LAP_GOI_THAU`. Quyền: status 7 + **Lập gói thầu**
- Duyệt kết quả thầu: `BidPackageService::update()` (`:495`)
  - `canApproveResult()` = status 3 + quyền **TP duyệt kết quả thầu** + người xử lý thuộc nhóm mình quản lý
  - `canBGDApprove()` = status 13 + quyền **BGD duyệt kết quả thầu**
  - Điều kiện đẩy BGĐ: có SP `price_bid_package` ngoài khoảng `price_min`–`price_max`
  - Không duyệt: từ 3 → **15 (TP không duyệt)**, từ 13 → **16 (BGĐ không duyệt)**; người xử lý (`canHandle()`) sửa rồi gửi lại
- Kết xuất thầu: `BidPackageController::render()` (`:156`)
  - `canRender()` = status 10 + **chính nhân viên xử lý** (`employee_id`) + có ít nhất 1 SP `status = 1` (tick trúng)
  - Cập nhật **tất cả** báo giá nguồn qua bảng nối `bid_package_quotations` (gói thầu gộp nhiều báo giá) → mỗi báo giá về **18**, dự toán `DA_CHUYEN_HOP_DONG`
- Màn phân công / lập HĐ: `pages/contract/bid_package_render/index.vue`
  - `canAssignCreateContract()` = status 4 + quyền **Phân công hợp đồng** → `PUT /bid_packages/{id}/assign-employee-create-contract`; set `contract_manager_id` cho gói thầu **và tất cả báo giá nguồn**, ghi log `ContractAssignEmployee`
  - `canCreateContract()` = (status 4 + `contract_manager_id` = mình + quyền **Lập hợp đồng**) **hoặc** (status 8/9 + còn SP `qty_contracted < qty`) → cho phép **tách nhiều HĐ từ 1 gói thầu**
  - `canReturnRender()` = status 4 + quyền **Phân công hợp đồng** hoặc **Lập hợp đồng**
- Lập HĐ: link `/contract/contract/add?bid_package_id={id}`; FE (`pages/contract/contract/add.vue:97`) ép `type = 1` (Trong thầu), chỉ lấy SP `status === 1`, giá lấy từ `price_bid_package` / `amount_bid_package`
- BB thương thảo (`record_type = 1`): duyệt ở `NegotiationMinutesController::approve()`; sau khi **Đã duyệt (3)** thì `Contract::canCreateContract()` cho phép đẻ HĐ chính từ BB. Hiện nút "Lập biên bản thương thảo" ở màn gói thầu đã kết xuất **đang bị comment** trong FE

---

## 3. Nhánh NGOÀI THẦU (`project_type = 2`) — thẳng sang hợp đồng

```
Báo giá: Đã duyệt (3)
   │ kết xuất (result = 1)
   ▼
Chuyển hợp đồng (9) — group_process = 'Hợp đồng', dự toán DA_CHUYEN_HOP_DONG
   │
   ├─ đã có contract_manager_id → notify thẳng người đó
   └─ chưa có → notify nhóm quyền "Phân công hợp đồng"
   │
   ├────────────► Đẩy trả về phòng trước → Đang tạo (1)
   │
   ▼ Phân công NV lập HĐ (nếu chưa có)
Lập hợp đồng (/contract/contract/add?quotation_id=…)
   ├─ Lưu nháp   → HĐ Đang tạo (1)  → BG: Đang lập hợp đồng (10)
   └─ Gửi duyệt  → HĐ Chờ duyệt (2) → BG: Đã lập hợp đồng (4)
   │
   ▼
§5 Duyệt hợp đồng
```

- Màn trung gian: **`pages/contract/quotation_render/index.vue`** — lọc cứng `status = 9` (Chuyển hợp đồng), 3 nút thao tác:

| Nút | Cờ | Điều kiện (`Quotation.php`) |
|---|---|---|
| Phân công làm hợp đồng | `can_assign_create_contract` | status 9 + quyền **Phân công hợp đồng** (`:255`) |
| Lập hợp đồng | `can_create_contract` | status 9 + `contract_manager_id` = user hiện tại + quyền **Lập hợp đồng** (`:239`) |
| Đẩy trả về phòng trước | `can_return_render` | status 9 + quyền **Phân công hợp đồng** hoặc **Lập hợp đồng** (`:262`) |

- Phân công: `QuotationService::assignEmployeeCreateContract()` (`:911`) — ghi `ContractAssignEmployee` (status 2 = duyệt sẵn), set `contract_manager_id`, `contract_received_time`, `contract_received_group_id` (nhóm của NV nhận), `process_time`
- Đẩy trả: `QuotationService::returnRender()` (`:844`) — báo giá về **Đang tạo (1)**, xóa `group_process`, dự toán về `DANG_LAP_BAO_GIA`, lưu `return_reason` / `returned_by` / `returned_at` (banner ở màn chi tiết; gửi duyệt lại tự xóa cờ — `updateStatus()` `:887`)
- FE map dữ liệu báo giá → HĐ: `pages/contract/contract/add.vue:140` — mặc định `type = 2` (Ngoài thầu), copy `quotation_id` / `quotation_code`, `main_company_id = main_company_contractor`, gắn `objectable_*` để truy vết nguồn
- Đẩy ngược trạng thái: `ContractService::updateStatus()` (`:807`)
  - HĐ **Đang tạo (1)** → BG **10**, dự toán `DA_LAP_BAO_GIA`, gói thầu `DANG_LAP_HOP_DONG`
  - HĐ **Chờ duyệt (2)** → BG **4**, dự toán `DA_LAP_HOP_DONG`, gói thầu `DA_LAP_HOP_DONG`

---

## 4. Nhánh CHO/TẶNG (4), ĐẶT/MƯỢN (5), NGUYÊN TẮC (6)

Khung luồng **giống hệt Ngoài thầu**, khác 4 điểm:

```
Chờ duyệt (2)
   │ TP duyệt
   ▼
Chờ BGĐ duyệt (13)   ◄── BẮT BUỘC, không phụ thuộc giá min–max
   │ BGĐ duyệt
   ▼
Đã duyệt (3) ──kết xuất──► Chuyển hợp đồng (9)
   │
   ▼
Lập hợp đồng — loại HĐ ÉP theo project_type:
        project_type 4 → contract.type = 3 (Cho/Tặng)
        project_type 5 → contract.type = 4 (Đặt/Mượn)
        project_type 6 → contract.type = 5 (Nguyên tắc)
   │
   ▼
§5 Duyệt hợp đồng
```

**1. Luôn phải qua BGĐ** — `QuotationService.php:470`:

```php
if (in_array($quotation->project_type, [4, 5, 6])) {
    $quotation->status = Quotation::CHO_BGĐ_DUYET;
}
```

Không xét khoảng giá min–max như loại 1/2.

**2. FE map loại HĐ theo bảng cứng** — `pages/contract/contract/add.vue:151`:

```js
const contractTypeMap = { 4: 3, 5: 4, 6: 5 }   // project_type → contract.type
```

Đi qua đúng flow chọn báo giá của màn tạo HĐ thủ công (`getQuotationsForContract()` → `onQuotationChange()`), **không** ép `type = 2` như nhánh Ngoài thầu.

**3. BE validate lại báo giá khi lưu HĐ** — `ContractService::store()` (`:232`):

```php
if (in_array($contract->type, [CHO_TANG, DAT_MUON, NGUYEN_TAC])) {
    $quotation = Quotation::find($request->quotation_id);
    if (!$quotation || $quotation->status != Quotation::CHUYEN_HOP_DONG
        || !in_array($quotation->project_type, [4, 5, 6])) {
        throw new \Exception('Báo giá không hợp lệ hoặc chưa được duyệt');
    }
}
```

→ Bắt buộc báo giá phải đúng **status 9** và đúng loại 4/5/6. Đây là chốt chặn chỉ có ở nhánh này.

**4. Cập nhật trạng thái dự toán riêng:**

- `ContractService::updateStatus()` (`:846`): HĐ loại 3/4/5 + dự toán loại 4/5/6, HĐ ở trạng thái 1 hoặc 2 → dự toán `DANG_LAP_HOP_DONG`
- `ContractController::approve()` (`:572`): duyệt HĐ loại 3/4/5 → dự toán `DA_LAP_HOP_DONG`

---

## 5. Duyệt hợp đồng (chung cho mọi nhánh)

- Route: `PUT /category/contracts/{contract}/approve` và `/reject` — `ContractController::approve()` (`:536`), `reject()` (`:608`)
- Quyền: `Contract::canApprove()` = status **2 (Chờ duyệt)** + quyền **Duyệt hợp đồng** + người lập thuộc nhóm mình quản lý (hoặc là chính mình). Riêng `record_type = 1` (BB thương thảo) xét quyền **Duyệt biên bản thương thảo**

| Hành động | Kết quả |
|---|---|
| **Duyệt** (`result ≠ 2`) | HĐ **Đã duyệt (3)**, ghi `approver_id` + `approved_time`, `current_version = 0`, snapshot `root_qty`/`root_price` vào `contract_products`, tạo `ContractVersion` **v0** (bản gốc để đối chiếu phụ lục sau này) |
| **Duyệt** khi `result = 2` (Không thực hiện) | HĐ **Hủy (5)** + `cancelDownstream()` (`ContractService.php:791`): báo giá → **19 Hủy hợp đồng**, dự toán → `HUY_HOP_DONG`, gói thầu → `HUY_HOP_DONG`. Ghi lịch sử "Hủy hợp đồng" kèm lý do vào cột `note` |
| **Không duyệt** | HĐ **4**, lưu `reason_deny`, gọi `updateStatus()` → báo giá quay về **10 (Đang lập hợp đồng)**. Người lập sửa (`canEdit()` mở cho status 1 và 4) rồi gửi duyệt lại |

Mọi lượt đều ghi `HistoryApprovedContract` qua `ContractService::createHistoryApprove()` và bắn notification cho người lập.

---

## 6. Sau khi duyệt hợp đồng — kết xuất sang Cung ứng

```
Đã duyệt (3) ──người lập gửi──► Chờ duyệt kết xuất (10)
                                   ├─ duyệt    → Đã kết xuất (9) → lập phiếu đề xuất cung ứng
                                   ├─ từ chối  → Không duyệt kết xuất (11) → sửa, gửi lại
                                   └─ người lập tự rút → về Đã duyệt (3)
```

- `canRenderSupply()` = status 3 hoặc 11 + `record_type = 2` + `supply_rendered_at` NULL + **chính người lập**
- `canApproveRenderSupply()` / `canRejectRenderSupply()` = status 10 + quyền **Duyệt hợp đồng kết xuất cung ứng** (không xét phạm vi nhóm — chốt với user 16/09/2026)
- `Contract::approvedStatuses()` = `[3, 9, 10, 11]` — cả 4 trạng thái này đều được coi là "HĐ đã duyệt" cho nghiệm thu / thanh lý / phụ lục / đơn mua hàng

---

## 7. Bảng quyền theo bước

| Bước | Quyền (permission name) |
|---|---|
| Lập / sửa / kết xuất báo giá | Lập báo giá |
| Duyệt báo giá cấp TP | TP duyệt báo giá |
| Duyệt báo giá cấp BGĐ | BGĐ duyệt báo giá |
| Lập / từ chối gói thầu | Lập gói thầu |
| Duyệt kết quả thầu cấp TP | TP duyệt kết quả thầu |
| Duyệt kết quả thầu cấp BGĐ | BGD duyệt kết quả thầu |
| Phân công NV lập HĐ, đẩy trả | Phân công hợp đồng |
| Lập hợp đồng, đẩy trả | Lập hợp đồng |
| Duyệt / không duyệt hợp đồng | Duyệt hợp đồng |
| Lập / duyệt BB thương thảo | Lập biên bản thương thảo / Duyệt biên bản thương thảo |
| Duyệt kết xuất sang cung ứng | Duyệt hợp đồng kết xuất cung ứng |

---

## 8. Điểm cần lưu ý / bẫy

1. **`contract_manager_id` là chốt chặn duy nhất** của nút "Lập hợp đồng". Chưa phân công thì người có quyền *Lập hợp đồng* vẫn không lập được (`canCreateContract()` so sánh `contract_manager_id == auth()->user()->id`)
2. **Báo giá status 3 vẫn cho sửa** (`Quotation::canEdit()` mở cho 1, 5, 3) — dễ lệch dữ liệu so với HĐ đã lập từ báo giá đó
3. **Gói thầu gộp nhiều báo giá**: mọi thao tác kết xuất / phân công đều lặp qua bảng nối `bid_package_quotations` (`sourceQuotations()`); nhánh cột đơn `bid_package.quotation_id` chỉ còn dùng cho gói "nhảy thầu" không sinh từ báo giá
4. **Một gói thầu đẻ được nhiều hợp đồng** khi còn SP `qty_contracted < qty` (`BidPackage::canCreateContract()` nhánh thứ 2). Báo giá thì **không** — chỉ 1 HĐ
5. **Loại 4/5/6 luôn phải qua BGĐ**, không có đường tắt kể cả khi giá nằm trong khoảng cho phép
6. **`result = 2` mang 2 nghĩa khác nhau** tùy vị trí: ở báo giá (kết xuất) → hủy báo giá; ở hợp đồng (duyệt) → hủy hợp đồng + hủy ngược cả chuỗi nguồn
7. `ContractVersion` v0 chỉ sinh **một lần** lúc duyệt HĐ; dữ liệu đông cứng trong đó có thể lệch với thực tế sau khi có phụ lục (giá trị HĐ, ngày kết thúc)
8. Nút "Lập biên bản thương thảo" ở màn gói thầu đã kết xuất đang bị comment trong FE (`pages/contract/bid_package_render/index.vue:200`) — BB thương thảo hiện tạo từ màn riêng `pages/contract/negotiation_minutes/add.vue`

---

## 9. File liên quan

**Backend** (`hrm-thanhan-api/Modules/Category/`)

| File | Vai trò |
|---|---|
| `Entities/Quotation/Quotation.php` | Hằng trạng thái + accessor `canApprove` / `canRender` / `canCreateContract` / `canAssignCreateContract` / `canReturnRender` |
| `Services/QuotationService.php` | `approve()` `:428`, `render()` `:651`, `rejectBid()` `:805`, `returnRender()` `:844`, `assignEmployeeCreateContract()` `:911` |
| `Entities/BidPackage/BidPackage.php` | Hằng trạng thái + accessor `canApproveResult` / `canRender` / `canCreateContract` |
| `Services/BidPackageService.php` | `update()` `:495` (duyệt kết quả), `updateStatus()` `:864`, `assignEmployeeCreateContract()` `:907` |
| `Http/Controllers/Api/V1/BidPackageController.php` | `render()` `:156` (kết xuất thầu) |
| `Entities/Contract/Contract.php` | Hằng trạng thái / loại + `canEdit` / `canApprove` / `canRenderSupply` / `approvedStatuses` |
| `Services/ContractService.php` | `store()` `:205`, `updateStatus()` `:807`, `cancelDownstream()` `:791` |
| `Http/Controllers/Api/V1/ContractController.php` | `approve()` `:536`, `reject()` `:608` |
| `Routes/api.php` | `:265` quotations, `:305` bid_packages, `:374` contracts |

**Frontend** (`hrm-thanhan-client/pages/`)

| File | Vai trò |
|---|---|
| `plan/quotation/index.vue`, `_id/approve.vue`, `_id/render.vue` | Danh sách / duyệt / kết xuất báo giá |
| `contract/quotation_render/index.vue` | Báo giá đã chuyển HĐ (status 9) — phân công, lập HĐ, đẩy trả |
| `contract/bid_package_render/index.vue` | Gói thầu đã kết xuất — phân công, lập HĐ, đẩy trả |
| `contract/contract/add.vue` | Tạo HĐ từ `?quotation_id=` / `?bid_package_id=` / `?project_id=` |
| `contract/contract/approve.vue` | Duyệt hợp đồng |
| `contract/contract/approve-render-supply.vue` | Duyệt kết xuất sang cung ứng |
