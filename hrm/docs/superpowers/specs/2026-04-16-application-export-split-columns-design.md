# Spec — Tách cột Excel xuất danh sách Ứng dụng

**Ngày:** 2026-04-16
**Người phụ trách:** @manhcuong
**Module:** Assign
**Màn liên quan:** `/assign/application` (Danh sách ứng dụng)

---

## 1. Bối cảnh

Hiện tại file Excel xuất từ màn danh sách Ứng dụng có **7 cột**, trong đó 2 cột gộp nhiều thông tin vào 1 ô:

- **Cột 2** gộp: `Mã ứng dụng - Tên ứng dụng` + người tạo + ngày tạo
- **Cột 6** gộp: `Ngày cập nhật` + người cập nhật

Gộp nhiều trường vào 1 ô gây khó khăn khi người dùng cần lọc, sắp xếp, hoặc copy từng trường riêng trong Excel. Yêu cầu: **tách mỗi trường thành 1 cột riêng** để Excel đúng dạng bảng dữ liệu chuẩn.

## 2. Mục tiêu

- Mỗi field là 1 cột riêng → tổng 12 cột
- Không thay đổi API, DB, filter, Service query
- Không ảnh hưởng màn danh sách / form detail

## 3. Ngoài phạm vi (out of scope)

- Không đổi định dạng file (giữ `.xls`)
- Không đổi tên file (giữ `danh_sach_ung_dung.xls`)
- Không bổ sung filter mới
- Không bổ sung header style phức tạp (màu nền, border đậm...)
- Không thêm dòng tổng, footer, hay metadata (tên người xuất, ngày xuất...)

## 4. Cấu trúc 12 cột mới

**Lưu ý data flow thực tế:** Controller `export()` gọi `index()` → data đã qua `ApplicationsResource` → blade nhận **array** (không phải Eloquent object). Các field đã có sẵn trong array từ Resource, blade dùng **array access**.

| # | Tên cột | Nguồn data (array key) | Ghi chú format |
|---|---|---|---|
| 1 | STT | `$k + 1` (loop index) | Số nguyên, tăng dần từ 1 |
| 2 | Mã ứng dụng | `$item['code']` | Text |
| 3 | Tên ứng dụng | `$item['name']` | Text |
| 4 | Mô tả | `$item['description']` | Text (có thể dài, wrap trong cell) |
| 5 | Nhóm ngành | `$item['scope_names']` | Đã nối sẵn bằng `, ` từ Resource |
| 6 | Nhóm giải pháp | `$item['industry_names']` | Đã nối sẵn bằng `, ` từ Resource |
| 7 | Lĩnh vực khách hàng | `$item['customer_scope_names']` | Đã nối sẵn bằng `, ` từ Resource |
| 8 | Trạng thái | Map `$item['status']` → text | `1 → Hoạt động`, `2 → Khóa` |
| 9 | Người tạo | `$item['created_by_name']` | Đã map sẵn từ Resource |
| 10 | Ngày tạo | `$item['created_at']` → lấy phần ngày | Resource trả `d/m/Y H:i:s` → dùng `explode(' ', ...)[0]` để lấy `d/m/Y` |
| 11 | Người cập nhật | `$item['updated_by_name']` | Đã map sẵn từ Resource |
| 12 | Ngày cập nhật | `$item['updated_at']` → lấy phần ngày | Resource trả `d/m/Y H:i:s` → dùng `explode(' ', ...)[0]` để lấy `d/m/Y` |

## 5. File cần sửa

**Chỉ sửa 1 file duy nhất** — `applications.blade.php`. Không đụng Controller, Export class, Service, Resource. Zero risk regression cho luồng list / form khác.

### 5.1. `hrm-api/resources/views/exports/applications.blade.php`

Viết lại `<thead>` và `<tbody>` thành 12 cột, dùng **array access** (data đã qua Resource):

```blade
<thead>
    <tr>
        <td style="text-align: center; font-weight: bold; border: 1px solid black">STT</td>
        <td style="text-align: center; font-weight: bold; border: 1px solid black">Mã ứng dụng</td>
        <td style="text-align: center; font-weight: bold; border: 1px solid black">Tên ứng dụng</td>
        <td style="text-align: center; font-weight: bold; border: 1px solid black">Mô tả</td>
        <td style="text-align: center; font-weight: bold; border: 1px solid black">Nhóm ngành</td>
        <td style="text-align: center; font-weight: bold; border: 1px solid black">Nhóm giải pháp</td>
        <td style="text-align: center; font-weight: bold; border: 1px solid black">Lĩnh vực khách hàng</td>
        <td style="text-align: center; font-weight: bold; border: 1px solid black">Trạng thái</td>
        <td style="text-align: center; font-weight: bold; border: 1px solid black">Người tạo</td>
        <td style="text-align: center; font-weight: bold; border: 1px solid black">Ngày tạo</td>
        <td style="text-align: center; font-weight: bold; border: 1px solid black">Người cập nhật</td>
        <td style="text-align: center; font-weight: bold; border: 1px solid black">Ngày cập nhật</td>
    </tr>
</thead>
<tbody>
    @foreach ($data as $k => $item)
    <tr>
        <td style="text-align: center; border: 1px solid black;">{{ $k + 1 }}</td>
        <td style="border: 1px solid black;">{{ $item['code'] ?? '' }}</td>
        <td style="border: 1px solid black;">{{ $item['name'] ?? '' }}</td>
        <td style="border: 1px solid black;">{{ $item['description'] ?? '' }}</td>
        <td style="border: 1px solid black;">{{ $item['industry_names'] ?? '' }}</td>
        <td style="border: 1px solid black;">{{ $item['scope_names'] ?? '' }}</td>
        <td style="border: 1px solid black;">{{ $item['customer_scope_names'] ?? '' }}</td>
        <td style="border: 1px solid black;">{{ ($item['status'] ?? null) == 1 ? 'Hoạt động' : 'Khóa' }}</td>
        <td style="border: 1px solid black;">{{ $item['created_by_name'] ?? '' }}</td>
        <td style="border: 1px solid black;">{{ !empty($item['created_at']) ? explode(' ', $item['created_at'])[0] : '' }}</td>
        <td style="border: 1px solid black;">{{ $item['updated_by_name'] ?? '' }}</td>
        <td style="border: 1px solid black;">{{ !empty($item['updated_at']) ? explode(' ', $item['updated_at'])[0] : '' }}</td>
    </tr>
    @endforeach
</tbody>
```

**Lưu ý mapping cột "Nhóm ngành" / "Nhóm giải pháp":** Blade cũ đã map "Nhóm ngành" ↔ `industry_names` và "Nhóm giải pháp" ↔ `scope_names`. Giữ nguyên mapping này khi tách cột.

**Cập nhật `colspan`**: Các dòng `<tr>` ngoài tbody (logo, tiêu đề, dòng ký tên) đang dùng `colspan="7"` → đổi sang `colspan="12"` cho khớp số cột mới. Cụ thể:
- Dòng 12: `<td colspan="7">` → `<td colspan="12">` (logo)
- Dòng 17: `<td colspan="7">` → `<td colspan="12">` (tiêu đề "Danh sách ứng dụng")
- Dòng 51: `<td colspan="7">` → `<td colspan="12">` (dòng trống)
- Dòng 55: `<td colspan="7">` → `<td colspan="12">` (dòng "Ngày..., tháng..., năm...")
- Dòng 60: `<td colspan="6">` → `<td colspan="11">` + `colspan="1"` giữ nguyên (cặp "Người lập")
- Dòng 66: `<td colspan="6">` → `<td colspan="11">` + `colspan="1"` giữ nguyên (cặp "Ký, họ tên")

(Số dòng tham chiếu file gốc, có thể shift sau khi viết lại.)

## 6. Giữ nguyên

| Phần | Giữ nguyên |
|---|---|
| Route | `GET /api/v1/assign/applications/export` |
| Tên file xuất | `danh_sach_ung_dung.xls` |
| Định dạng | `.xls` |
| Filter hỗ trợ | keyword, scope_id, industry_id, customer_scope_id, status, created_by, updated_by, updated_from, updated_to |
| FE | Nút "Xuất Excel" + hàm `exportExcel()` trong `hrm-client/pages/assign/application/index.vue` |
| Permission | Giữ permission hiện tại (nếu có) |

## 7. Business rules & edge cases

- **Ứng dụng không có relationship** (chưa gán scope/industry/customerScope): cell để trống (hành vi tự nhiên của `implode`)
- **Mô tả dài**: Excel tự wrap text trong cell, không cần cắt/xử lý
- **Người tạo/cập nhật đã nghỉ hoặc bị xóa**: accessor `employee_create_name` / `employee_update_name` trả về `null` → cell trống (giữ behavior hiện tại)
- **`created_at` / `updated_at` null** (trường hợp hiếm với bản ghi lỗi): cell trống, không crash
- **Status có giá trị khác 1 và 2**: theo Model hiện tại chỉ có 2 giá trị, không cần xử lý case khác

## 8. Downstream impact

- **Người dùng đã quen với file cũ**: file mới có số cột và thứ tự cột khác → cần thông báo team khi release. Không có hệ thống hạ nguồn nào tự động parse file này nên không ảnh hưởng kỹ thuật
- **Macro Excel / script ngoài nếu có**: user cần tự cập nhật nếu đang dùng

## 9. Test plan (manual)

1. Vào màn `/assign/application`, click **Xuất Excel** không áp filter → file có đủ 12 cột, data đúng từng cột
2. Áp filter keyword + scope → file chỉ có bản ghi khớp filter, 12 cột đúng
3. Test ứng dụng có nhiều scope/industry/customerScope → giá trị nối bằng `, ` trong 1 cell
4. Test ứng dụng không có relationship → các cell scope/industry/customerScope rỗng
5. Test ứng dụng có description dài → hiển thị đầy đủ trong cell (wrap)
6. Test ngày tạo/cập nhật → định dạng `DD/MM/YYYY`
7. Test trạng thái → hiển thị text `Hoạt động` / `Khóa`
8. Test người tạo/cập nhật đã nghỉ việc → cell trống, không lỗi

## 10. Rủi ro

| Rủi ro | Mức độ | Mitigation |
|---|---|---|
| Blade truy cập relationship chưa eager-load → N+1 query khi export số lượng lớn | Trung bình | Check Service `index()` đã có `with(...)` chưa, bổ sung nếu thiếu |
| Export class đang nhận data đã qua Resource (mất relationship/accessor) | Thấp | Check code, điều chỉnh nếu cần |
| User bất ngờ vì cấu trúc file đổi | Thấp | Thông báo trong release notes |

## 11. Ước lượng effort

- BE: 30 phút (sửa blade + check export class + service)
- Test: 30 phút (manual test 8 case)
- **Tổng: ~1 giờ**
