# Skill: Entity History (Lịch sử thay đổi)

Chuẩn hoá cách làm tính năng "Lịch sử thay đổi / lịch sử chỉnh sửa" (audit log ai sửa gì, cũ → mới, lúc nào) cho một màn/entity.
Áp dụng khi user yêu cầu: "bổ sung lịch sử chỉnh sửa", "lịch sử thay đổi", "log ai sửa", "audit" cho bất kỳ màn nào.

**Mẫu chuẩn (đọc code trước khi làm):**

| Phần | File mẫu |
| --- | --- |
| Migration | `hrm-api/Modules/Timesheet/Database/Migrations/2026_07_10_000001_create_general_regulation_history_table.php` |
| Entity | `hrm-api/Modules/Timesheet/Entities/GeneralRegulationHistory.php` |
| Ghi log + endpoint | `hrm-api/Modules/Timesheet/Services/GeneralRegulationService.php` (TRACKED_FIELDS, buildTrackedSnapshot, normalizeTrackedValue, logHistoryIfChanged, histories) |
| Controller + route | `GeneralRegulationController::histories()` + `GET /histories` cùng group |
| FE modal | `hrm-client/components/setting/general/GeneralHistoryModal.vue` |
| Biến thể full-snapshot | `employee_history` (`EmployeeService` + `pages/human/employee/components/EmployeeHistoryModal.vue`) |

---

## 0. Câu hỏi PHẢI chốt với user trước khi code

1. **Track trường nào?** Chỉ trường trên màn đó, hay mọi cột? (endpoint save có thể được màn khác dùng chung → trường của màn khác KHÔNG được sinh log)
2. **Ai được xem?** Mặc định: KHÔNG permission riêng (ai vào được màn thì xem được lịch sử). Chỉ thêm permission khi user yêu cầu (sửa `PermissionsTableSeeder`, không migration).
3. **Có cần action ngoài `update` không?** (create/đổi trạng thái/đổi mật khẩu → dùng biến thể full-snapshot như employee)

## 1. Chọn biến thể

- **Subset-diff (MẶC ĐỊNH)**: BE diff sẵn, `old_value`/`new_value` = JSON **chỉ gồm các trường thay đổi**. FE render thẳng, không cần diffJson. Dùng khi chỉ có action `update`, hoặc có trường nội dung dài (HTML editor) — full snapshot sẽ phình bảng.
- **Full-snapshot**: lưu snapshot đầy đủ, FE tự diff (mẫu employee). Chỉ dùng khi cần nhiều loại action (create/change_status/password) hoặc trường dạng list added/removed.

## 2. DB

Bảng `<entity>_history` (số ít, theo mẫu `employee_history`):

- `id`, `<entity>_id` (unsignedBigInteger, index), `company_id` (nullable, index — nếu entity scope theo công ty)
- `action` (string), `old_value`/`new_value` (text nullable, JSON), `changed_by` (nullable), `changed_at` (timestamp `useCurrent`), `timestamps()`
- KHÔNG FK cứng, KHÔNG SoftDeletes. Migration có PHPDoc trên `up()`/`down()`.

## 3. BE (ghi log trong Service — KHÔNG dùng Observer)

- Hằng `TRACKED_FIELDS` (whitelist) + `BOOLEAN_TRACKED_FIELDS` trong Service.
- Trong `save()`/`update()`: chụp snapshot tracked TRƯỚC `fill()` → save → diff → có thay đổi mới insert 1 dòng (`action='update'`, `changed_by=auth()->id()`, `changed_at=Carbon::now()`, JSON `JSON_UNESCAPED_UNICODE`). Không đổi gì → không ghi.
- **Bắt buộc chuẩn hoá kiểu trước khi so sánh** (copy `normalizeTrackedValue`): rỗng/null → null; boolean → 0/1 (`filter_var`) vì FE gửi `true/false` còn DB trả `"1"/0`; numeric → int nếu tròn; còn lại string. Không chuẩn hoá = log rác `"5" → 5`.
- Endpoint `GET <prefix>/histories` cùng group route (mặc định chỉ `auth:api`), method Service `histories()`:
  - `with('user.info')`, scope theo `company_id` hiện tại
  - **Sắp xếp `changed_at` ASC + `id` ASC (cũ → mới)** — convention đã chốt
  - Trả: `id, action, old_value, new_value, changed_by, changed_by_name` (fullname ?? email ?? '—'), `changed_at` (`d/m/Y H:i:s`), `changed_at_raw` (`Y-m-d` cho FE lọc ngày)
- PHP 7.4: không `?->`.

## 4. FE

- Nút mở modal đặt trên màn: `V2BaseButton` **`light`** + icon `ri-history-line` + `size="sm"` (nút "Xem log/Lịch sử" cấp page thuộc nhóm light — theo skill `button-convention`).
- Modal copy `GeneralHistoryModal.vue`, tuân thủ skill `modal-popup` (hide-footer, header icon tròn + X, footer chỉ nút Đóng tertiary). Gọi API bằng `apiGetMethod`, KHÔNG thêm Vuex action riêng.
- Hiển thị mỗi dòng: thời gian + người thực hiện + danh sách `Nhãn trường: cũ → mới` với **cũ màu ĐỎ (`.change-old` #dc2626), mới màu XANH (`.change-new` #16a34a)** — không dùng gạch ngang/xám.
- `FIELD_LABELS` tiếng Việt khớp 100% danh sách `TRACKED_FIELDS` BE; map giá trị: boolean → Bật/Tắt (hoặc Có/Không theo màn), enum/radio → nhãn đúng text option trên màn, rỗng → `(trống)`; trường HTML dài → strip HTML + cắt ~100 ký tự + tooltip full.
- Bộ lọc client-side: Trường / Người thực hiện (gom từ data, value = changed_by) / Từ ngày / Đến ngày (so `changed_at_raw`), nút Tìm kiếm + Làm mới. Load hết không phân trang (data ít); có empty state.
- **CẢNH BÁO màn auto-save** (watcher deep trên model tự POST): nút + modal tuyệt đối không đụng `model`/watcher — modal tự chứa state.

## 5. Bẫy thường gặp

- Endpoint save dùng chung với màn khác → trường ngoài whitelist đổi thì KHÔNG được sinh log (verify case này).
- Record tự tạo lần đầu GET → không log action `create`.
- Đổi N trường trong 1 lần lưu → 1 dòng log N key (không tách dòng).
- Key order JSON theo thứ tự `TRACKED_FIELDS`, không theo thứ tự request.

## 6. Verify bắt buộc trước khi báo xong

1. `php -l` + tinker: đổi 1 trường → 1 log đúng subset; không đổi → không log; trường ngoài whitelist → không log; boolean `true` vs `"1"` → không log rác; đổi 2 trường → 1 dòng 2 key; `histories()` đúng format + thứ tự cũ→mới.
2. Playwright: đổi giá trị trên màn → modal hiện dòng mới đúng đỏ/xanh + người + giờ; bộ lọc 4 loại; mở/đóng modal không tự bắn POST.
3. Dọn log test bằng tinker (`where('id','>',$maxTrướcTest)->delete()`), khôi phục giá trị đã đổi. KHÔNG xoá log thật của user.

---

## Checklist khi tạo/review

- [ ] Đã chốt với user: trường track / quyền xem / loại action
- [ ] Bảng `<entity>_history` đúng cột mẫu, migration có PHPDoc
- [ ] Diff trong Service với `normalizeTrackedValue`, whitelist TRACKED_FIELDS
- [ ] Endpoint histories sort ASC (cũ→mới), trả `changed_by_name` + `changed_at_raw`
- [ ] FE: nút light + ri-history-line; modal theo skill `modal-popup`; cũ ĐỎ → mới XANH
- [ ] FIELD_LABELS khớp 100% TRACKED_FIELDS; map boolean/enum/HTML dài
- [ ] Verify đủ mục 6 (tinker + Playwright + dọn data)
