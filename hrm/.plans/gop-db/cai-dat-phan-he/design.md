# Cài đặt phân hệ — ẩn/hiện phân hệ và từng mục menu

**Người phụ trách:** @namdangit — 2026-09-14 · **Nhánh:** `gop_db` (hrm-api + hrm-client)
**Spec chi tiết:** `docs/superpowers/specs/gop-db/2026-09-14-cai-dat-phan-he-design.md`

## Mục tiêu

Một màn cấu hình duy nhất liệt kê **đầy đủ 24 phân hệ + ~600 mục menu**, tick để chọn hiển thị:
tick cả phân hệ hoặc từng mục lẻ ở mọi cấp. Mặc định có tick (hiện). Cấu hình lưu DB, áp dụng
runtime — không phải build lại FE.

Thay cho cách cũ: 4 checkbox rời ("Sử dụng ERP / quyết định / cơm / CRM") trong màn Cài đặt,
lưu key-value ở `master_settings`, không mở rộng được.

## Scope

- Bảng mới `menu_settings` (chỉ lưu mục **bị tắt**) + API `GET`/`PUT /api/v1/menu-settings`.
- Màn mới `/timesheet/setting/subsystems`, vào từ mục **"Cài đặt phân hệ"** trong sidebar Cài đặt.
- Lớp lọc dùng chung `utils/menuVisibility.js`, cắm vào **6 bề mặt hiển thị menu đã có sẵn**
  (topbar, sidebar cây, sidebar hub, lưới Tổng quan hub, màn chọn phân hệ, dropdown chuyển phân hệ).
- Middleware FE `menu-visibility.js` chặn gõ thẳng URL của mục đã ẩn → `/feature-unavailable`.
- Gỡ 3 checkbox ERP / Quyết định / Cơm khỏi màn Cài đặt; khi lưu vẫn ghi bản sao key cũ cho logic nghiệp vụ BE.

**Không làm:** gate ở BE · cấu hình theo vai trò/công ty · lịch sử thay đổi · ẩn cột/nút/tab trong màn.

## Quyết định đã chốt

| # | Điểm | Chốt |
| --- | --- | --- |
| 1 | Phạm vi | Toàn hệ thống, 1 bộ cấu hình |
| 2 | Checkbox cũ | ERP/Quyết định/Cơm **chuyển hẳn sang `menu_settings`** — đây là nguồn đọc DUY NHẤT. Key cũ `master_settings` chỉ còn được GHI bản sao (49 chỗ/22 file BE đọc nó cho nghiệp vụ). Dữ liệu cũ không migrate, cấu hình lại từ đầu |
| 3 | Mức chặn | Ẩn menu + chặn URL ở FE (BE không gate) |
| 4 | Vị trí | Mục riêng trong sidebar Cài đặt, `/timesheet/setting/subsystems` |
| 5 | Quyền | Dùng chung `Quản lý phân quyền` (không thêm quyền mới) |
| 6 | Cha–con | Tắt cha = ẩn hết, **giữ nguyên** tick con trong DB |
| 7 | Lịch sử | Không ghi |
| 8 | Placeholder | Liệt kê tất, tick được |
| 9 | `use_crm` | **Ở lại màn Cài đặt** — là cờ đồng bộ CRM Mate, không phải phân hệ |
| 10 | Menu mới thêm sau | **Tự động có mặt** ở màn cấu hình (màn đọc thẳng registry, DB chỉ giữ key bị ẩn) |

## Hai điểm phải nhớ

- **Key định danh sinh từ đường dẫn nhãn** (`finance::Thu chi::Phiếu thu`) vì ~345 mục placeholder
  không có link. Đổi nhãn menu ⇒ mục đó về mặc định hiện. Util viết sẵn nhánh `item.menuKey ?? nhãn`
  để sau này nâng cấp không phải sửa logic.
- **Trùng mục đích với feature `prod-cutover` (Phần B, spec xong chưa code)**: bên đó là allowlist
  fail-closed cho PROD, bên này là denylist mặc định hiện. Khi cut-over PROD phải **seed sẵn danh sách
  ẩn**, không dựa vào admin nhớ tick. Xem mục 6 của spec.
