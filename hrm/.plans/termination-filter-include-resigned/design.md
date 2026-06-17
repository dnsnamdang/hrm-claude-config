# Filter nhân viên màn Chấm dứt HĐLĐ — hiển thị cả người đã nghỉ việc

**Người phụ trách:** @khoipv
**Ngày:** 2026-06-02
**Phạm vi:** 1 màn (`decision/termination-labor-contract/index.vue`) + 1 endpoint mới (Module Decision)

---

## 1. Mục tiêu

Dropdown filter **"Nhân viên"** trên màn danh sách Quyết định chấm dứt HĐLĐ hiện chỉ
hiển thị nhân viên đang làm việc (`status = 1`), nên **không lọc được những người đã
nghỉ việc** — vốn lại chính là đối tượng của màn này. Cần cho phép màn này lọc theo
**toàn bộ nhân viên, bất kể trạng thái** (gồm cả đã nghỉ việc).

## 2. Hiện trạng (nguyên nhân)

- FE bind Select2 "Nhân viên" vào `employeeInfoOptions` = `this.$store.state.employeeInfoOptions`.
- State global này nạp **1 lần** lúc app init từ `/api/v1/users/auth/user-profile`
  (`AuthNewController`), build từ `res.data.list_employee_infos`.
- Query backend lọc cứng: `EmployeeInfo ... ->where('employee_infos.status', 1)` →
  loại hết người nghỉ việc.
- State này **dùng chung mọi màn** → KHÔNG sửa global (sẽ ảnh hưởng toàn hệ thống).
- Endpoint dùng chung `Human/listEmployeeInfo` cũng hardcode `where('status',1)` và đang
  được nhiều nơi dùng (shift_details, reward, trouble_shooting_reports) → KHÔNG sửa
  (vi phạm quy tắc "không tự sửa hàm dùng chung").

## 3. Quyết định thiết kế (đã chốt với user)

| Câu hỏi | Quyết định |
| --- | --- |
| Phạm vi danh sách | **Toàn bộ nhân viên** (đang làm + đã nghỉ), không giới hạn theo QĐ chấm dứt |
| Định nghĩa "đã nghỉ" | Bỏ điều kiện `status = 1` → lấy **tất cả** employee_infos bất kể status |
| Hướng triển khai | **Hướng A** — endpoint riêng cho màn này, cô lập hoàn toàn |

## 4. Thiết kế chi tiết

### 4.1 Backend — `Modules/Decision`

**Route mới** (thêm vào group `termination-labor-contract` trong
`Modules/Decision/Routes/api.php`, ngay cạnh `index`/`export`):

```php
Route::get('/employee-options', [TerminationLaborContractController::class, 'employeeOptions']);
```

- Đặt trước route `/{terminationLaborContract}` để không bị route param "nuốt".
- **Không gắn** `checkPermission` (chỉ là nguồn options cho filter, đồng nhất với
  route `index`/`export` hiện không gắn permission).

**Controller method** `employeeOptions()`:

```php
public function employeeOptions()
{
    $data = EmployeeInfo::select('id', 'code', 'fullname')
        ->orderBy('id', 'desc')
        ->get();

    return response()->json(['data' => $data]);
}
```

- KHÔNG có `where('status', 1)` → trả toàn bộ nhân viên.
- KHÔNG lọc công ty (đồng nhất với hành vi `employeeInfoOptions` global hiện tại vốn
  trả mọi công ty).
- Trả tối thiểu 3 field (id, code, fullname) cho nhẹ payload.

### 4.2 Frontend — `pages/decision/termination-labor-contract/index.vue`

1. Thêm data local:
   ```js
   employeeFilterOptions: [],
   ```

2. Thêm method nạp options + gọi trong `mounted()`:
   ```js
   async fetchEmployeeFilterOptions() {
       const { data } = await this.$store.dispatch(
           'apiGetMethod',
           'decision/termination-labor-contract/employee-options'
       )
       this.employeeFilterOptions = data.map((e) => ({
           text: e.code + ' - ' + e.fullname,
           id: e.id,
       }))
   }
   ```
   ```js
   mounted() {
       this.$store.dispatch('optionsSelect/fetchWorkingPositions')
       this.fetchEmployeeFilterOptions()
   }
   ```

3. Đổi computed `employeeInfoOptions()`:
   ```js
   employeeInfoOptions() {
       return this.employeeFilterOptions
   }
   ```
   (Template `:options="employeeInfoOptions"` giữ nguyên, không phải sửa.)

4. Các phần khác (`exportExcel`, `computedPrintUrl`, filter value `employee_info_id`,
   query gửi lên BE) **giữ nguyên** — chỉ là filter theo id, không phụ thuộc nguồn options.

## 5. Phạm vi ảnh hưởng

- **Chỉ** màn `decision/termination-labor-contract/index.vue`.
- State global `employeeInfoOptions` và các màn decision khác **không đổi** (vẫn chỉ active).
- Backend: thêm 1 route + 1 method, không sửa code dùng chung.

## 6. Edge case / lưu ý

- Đặt route `/employee-options` **trước** `/{terminationLaborContract}` để tránh bị
  bắt nhầm thành show theo id.
- Danh sách dài hơn (gồm cả người nghỉ) → Select2 vẫn search client-side bình thường,
  không cần phân trang.
- Nếu sau này cần lọc theo công ty/phòng ban cho dropdown này thì mở rộng `employeeOptions()`
  với `when($request->company_id, ...)` — hiện chưa cần.

## 7. Kiểm thử

1. Mở màn `Chấm dứt HĐLĐ` → bộ lọc → dropdown "Nhân viên" hiện cả người đã nghỉ việc.
2. Chọn 1 người đã nghỉ → Search → ra đúng các QĐ chấm dứt của người đó.
3. Mở màn decision khác (vd `accept-personnel`) → dropdown nhân viên vẫn chỉ active (không bị ảnh hưởng).
4. Export Excel / In với filter nhân viên đã nghỉ → ra đúng dữ liệu.
