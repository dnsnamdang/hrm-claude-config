# Design (tóm tắt) — Loại meeting "Họp tìm hiểu & Giới thiệu sản phẩm" + Khảo sát nhu cầu đầu tư

- **Người phụ trách**: @dnsnamdang · **Ngày**: 2026-08-21 · **Nhánh**: `tpe` (api + client)
- **Spec đầy đủ**: `docs/superpowers/specs/2026-08-21-meeting-tim-hieu-gioi-thieu-sp-design.md`
- **Plan**: `.plans/meeting-tim-hieu-gioi-thieu-sp/plan.md`

## Mục tiêu

1. Thêm **loại meeting hệ thống** "Họp tìm hiểu & Giới thiệu sản phẩm" — có Khách hàng, không cho Sửa / Xoá / Khoá.
2. Với đúng loại đó, tab **Biên bản** có thêm khối **Khảo sát nhu cầu khách hàng** (3 câu hỏi bắt buộc khi Hoàn thành), hiện cả ở bản In biên bản và file Excel biên bản.

## Bộ câu hỏi

1. Anh/Chị có nhu cầu đầu tư trong thời gian tới? (Có / Không)
2. *(chỉ khi câu 1 = Có)* Anh/Chị đầu tư vào lĩnh vực nào TPE cung cấp? — chọn nhiều; mỗi lĩnh vực đã tích phải nhập **Mức đầu tư dự kiến (VNĐ)** + **Thời gian dự kiến bắt đầu (dd/mm/yyyy, không cho chọn quá khứ)**.
3. Anh/Chị có nhu cầu về dịch vụ sửa chữa bảo dưỡng/bảo trì máy móc thiết bị? (Có / Không)

## Quyết định lớn

| # | Chốt |
|---|------|
| 1 | Loại meeting cố định = **bản ghi mới thứ 7** + cột `meeting_types.code` + whitelist `MeetingType::SYSTEM_CODES` → chặn Sửa/Xoá/**Khoá** bằng **423 ở BE**, ẩn hẳn nút ở FE. Không đổi tên bản ghi cũ `id = 1` |
| 2 | Câu hỏi **hard-code**; **danh sách lĩnh vực đọc động từ ERP `scopes` qua `mysql2`** (13 bản ghi `status = 1`) |
| 3 | Lưu theo **PA1**: 2 cột trên `meetings` (`has_investment_demand`, `has_maintenance_demand`) + bảng mới `meeting_investment_demands` (`scope_id`, `scope_name` snapshot, `expected_amount`, `expected_start_date`, `position`) |
| 4 | Bắt buộc **khi bấm Hoàn thành** (`status = 3`) — đúng khuôn `conclusion => required_if:status,3` sẵn có |
| 5 | Snapshot `scope_name` để ERP đổi tên/xoá lĩnh vực không làm sai biên bản cũ; `scope_id` **không** đặt FK (khác database) |
| 6 | Endpoint mới `GET /assign/meeting/investment-scopes` (lazy-load + cache Vuex, nhận `include_ids` để lĩnh vực đã chọn nay bị khoá vẫn hiện) |
| 7 | **Không** thêm quyền mới |

## Phát hiện quan trọng khi rà project

- `meeting_types.has_customer` **đã có sẵn** → khối Khách hàng tự bật, không phải code thêm (`MeetingForm.vue:361`).
- Cột `meeting_types.type` **rỗng 100%, không code nào dùng** → cột chết, không tái sử dụng, để nguyên.
- ⚠️ **6 lĩnh vực trong yêu cầu gốc** (Gara ô tô / Công nghiệp / Đào tạo / Xử lý môi trường / Năng lượng / Dân sinh) **không tồn tại** ở bất kỳ danh mục nào — quét toàn bộ cột text của `hrm_tpe`, `hrm_erp`, `erp2326` không có "Dân sinh". Đã chốt render **động** theo data ERP thực tế; 2.1–2.6 chỉ là ví dụ.
- ⚠️ **Đừng nhầm 2 bảng cùng tên `scopes`**: ERP `erp2326.scopes` (13 dòng, dùng cho feature này, qua `mysql2`) ≠ HRM `scopes` (22 dòng, danh mục "Nhóm ngành" `/assign/industry-groups`, connection mặc định).
- Blade in biên bản `resources/views/exports/meeting_record.blade.php` **tự đánh số section** bằng `$sectionNumber` → chèn section mới không phải sửa số thủ công.
- Excel biên bản sinh **ở client** bằng ExcelJS trong `MeetingReport.vue`, không qua API.

## Ngoài scope

- "(Cấu hình thời gian)" trong yêu cầu gốc — feature sau.
- Báo cáo tổng hợp nhu cầu đầu tư — schema đã sẵn sàng, làm sau.
- Lỗi tải Excel trên Safari (`blob` + `<a download>`) — lỗi có sẵn của ~151 màn, không sửa lẫn vào đây.
- Chuẩn hoá `:disabled` → ẩn hẳn cho 6 bản ghi loại meeting cũ — không sửa đại trà màn cũ.
