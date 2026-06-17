# Chốt / Hủy chốt báo giá — Design

> Phụ trách: @khoipv
> Phạm vi: Tab "Báo giá" trong màn chi tiết dự án tiền khả thi (`assign/prospective-projects/{id}/manager`).

## Mục tiêu

Bổ sung 2 thao tác **Chốt báo giá** và **Hủy chốt** cho từng báo giá trong tab Báo giá, để đánh dấu báo giá **trúng thầu** của dự án.

## Nghiệp vụ

- Mỗi dự án chỉ có **duy nhất 1** báo giá trúng thầu.
- **Chốt báo giá**: báo giá `Đã duyệt (4)` → trạng thái mới **Trúng thầu (7)**.
- Khi dự án **đã có** báo giá trúng thầu, muốn chốt báo giá khác phải **Hủy chốt** cái cũ trước (BE **chặn + báo lỗi**, không tự thay thế).
- **Hủy chốt**: báo giá `Trúng thầu (7)` → quay lại `Đã duyệt (4)`, **bắt buộc nhập lý do**.

## Điều kiện hiển thị nút

- Nút **Chốt**: `status === 4 (Đã duyệt)` **và** `isSaleOfProject`.
- Nút **Hủy chốt**: `status === 7 (Trúng thầu)` **và** `isSaleOfProject`.
- `isSaleOfProject` = nhân viên hiện tại là Sale chính của dự án (`main_sale_employee_id`), đã có sẵn computed ở FE; BE gate lại bằng pattern `store()`.

## Quyết định chính

| Vấn đề | Quyết định |
| --- | --- |
| Ý nghĩa "chốt" | Chọn báo giá trúng thầu, độc nhất / dự án |
| Khi đã có trúng thầu | Chặn + báo lỗi ở BE, FE hiện toast |
| Xác nhận | Chốt: confirm đơn giản. Hủy chốt: modal nhập **lý do bắt buộc** |
| Phân quyền | Chỉ `isSaleOfProject`, **không** thêm permission → **không** gắn middleware |
| Lưu vết | Chỉ ghi `quotation_histories` (không thêm cột `won_at`/`won_by`, **không migration**) |
| Trạng thái dự án | **Không** đổi (giữ nguyên scope, chỉ đổi trạng thái báo giá) |

## Thay đổi kỹ thuật (tóm tắt)

**Backend** (`Modules/Assign`)
- `Entities/Quotation.php`: thêm `STATUS_TRUNG_THAU = 7` + map `['name' => 'Trúng thầu', 'color' => '#D4AF37']`.
- `Entities/QuotationHistory.php`: thêm action `finalize` ("Chốt báo giá (Trúng thầu)", `#D4AF37`) và `unfinalize` ("Hủy chốt", `#EF4444`).
- `Services/QuotationService.php`: thêm `finalize(Quotation)` và `unfinalize(Quotation, string $reason)`.
- `Http/Controllers/Api/V1/QuotationController.php`: thêm `finalize($id)`, `unfinalize(QuotationUnfinalizeRequest, $id)` — gate isSaleOfProject.
- `Http/Requests/Quotation/QuotationUnfinalizeRequest.php`: validate `reason` required (rethrow `ValidationException`).
- `Routes/api.php`: `POST /assign/quotations/{id}/finalize`, `POST /assign/quotations/{id}/unfinalize` (không middleware).

**Frontend** (`hrm-client`)
- `pages/assign/prospective-projects/components/ProspectiveProjectQuotationsTab.vue`:
  - 2 icon-button trong `#cell-code` actions (Chốt `ri-trophy-line`, Hủy chốt `ri-arrow-go-back-line`).
  - Modal nhập lý do hủy chốt — validate inline (`touched` + `is-invalid` + `invalid-feedback`).
  - Hằng `STATUS_BG_DA_DUYET = 4`, `STATUS_BG_TRUNG_THAU = 7`.

## Edge cases

- Sau trúng thầu (7): nút "Sửa ghi chú KD" (`v-if status===4`) tự ẩn — **giữ nguyên**.
- `canEdit` / `canDelete` dùng `status===1` → không ảnh hưởng.
- Đóng dự án chỉ cascade báo giá status 1/2/3 → báo giá trúng thầu (7) không bị đụng.
- Chốt đồng thời 2 báo giá: chặn bằng `lockForUpdate` khi kiểm tra tồn tại trúng thầu trong cùng dự án.

## Spec chi tiết BE

### `finalize(Quotation $q): Quotation`
```
- if status !== STATUS_DA_DUYET → throw "Chỉ chốt được báo giá đã duyệt."
- DB::transaction:
    - lockForUpdate kiểm tra Quotation::where(project_id, $q->project_id)
        ->where(status, STATUS_TRUNG_THAU)->where(id, '!=', $q->id)->exists()
      → nếu có → throw "Dự án đã có báo giá trúng thầu, vui lòng hủy chốt trước."
    - update status = STATUS_TRUNG_THAU
    - logHistory(FINALIZE, oldStatus, STATUS_TRUNG_THAU)
    - return fresh()
```

### `unfinalize(Quotation $q, string $reason): Quotation`
```
- if status !== STATUS_TRUNG_THAU → throw "Báo giá chưa ở trạng thái trúng thầu."
- if trim(reason) === '' → throw "Vui lòng nhập lý do hủy chốt."
- DB::transaction:
    - update status = STATUS_DA_DUYET
    - logHistory(UNFINALIZE, oldStatus, STATUS_DA_DUYET, ['reason' => $reason], $reason)
    - return fresh()
```

### Controller gate (cả 2 method, tái dùng pattern `store()` dòng 99-106)
```
- $q = Quotation::findOrFail($id);
- $project = ProspectiveProject::findOrFail($q->project_id);
- resolve employeeId từ auth()->user()->employee_info_id
- if !employeeId || project->main_sale_employee_id !== employeeId → abort(403, "Bạn không phải Sale phụ trách dự án này")
- gọi service, trả response (DetailQuotationResource hoặc success message)
```

## API contract

| Method | URL | Body | Response |
| --- | --- | --- | --- |
| POST | `/assign/quotations/{id}/finalize` | — | 200 success / 400 message lỗi / 403 |
| POST | `/assign/quotations/{id}/unfinalize` | `{ reason: string }` | 200 success / 422 validate / 400 / 403 |
