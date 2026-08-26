# Design — Danh mục Nhóm ngành: bổ sung Lĩnh vực kinh doanh nội bộ

**Ngày**: 2026-08-22 · **Nhánh**: `linh-vuc-noi-bo` (cả `hrm-api` + `hrm-client`)
**Màn**: Danh mục › Nhóm ngành (`/assign/industry-groups`, bảng `scopes`, `Modules/Assign` — Entity `Scope`)

> Folder này là nơi gom MỌI thay đổi về sau của màn **Danh mục Nhóm ngành**.
> Danh mục nguồn (Lĩnh vực kinh doanh nội bộ) dựng ở `.plans/linh-vuc-kinh-doanh-noi-bo/`.

## Mục tiêu

Nhóm ngành phải gắn với **1 Lĩnh vực kinh doanh nội bộ** (LVKDNB):

1. Form Thêm mới / Sửa: thêm dropdown **Lĩnh vực kinh doanh nội bộ (*)**, chọn tối đa 1, nguồn dữ
   liệu là LVKDNB **đang Hoạt động**, bắt buộc nhập.
2. Màn danh sách: thêm **cột** Lĩnh vực kinh doanh nội bộ + **bộ lọc** theo LVKDNB.

## Quyết định (chốt với user 2026-08-22)

| # | Quyết định |
| --- | --- |
| 1 | Tài liệu đặt ở folder mới `.plans/danh-muc-nhom-nganh/` (đặt tên theo MÀN, gom thay đổi về sau) |
| 2 | 22 bản ghi Nhóm ngành cũ: **backfill 1 giá trị mặc định** `LVKDNB.KHAC` — "Khác" (migration tự tạo nếu chưa có) |
| 3 | Ràng buộc chiều ngược: áp **đúng logic đã có** của cặp cha-con trong module (xem dưới) |
| 4 | Import **và** Export đều bổ sung trường LVKDNB; cập nhật luôn file mẫu |

## Ràng buộc Xoá / Khoá — copy pattern có sẵn, không tự chế

Cặp `Scope → Industries` (`Scope::isCanDelete/isCanLockUpdate`) và
`CustomerScopeGroup → CustomerScope` đang làm giống hệt nhau; áp y nguyên cho
`InternalBusinessScope → Scope`:

- `isCanDelete()` = đang Hoạt động **và** không còn Nhóm ngành nào tham chiếu.
- `isCanLockUpdate()` = không còn Nhóm ngành **đang Hoạt động** nào tham chiếu.
- Controller `delete` / `lock` guard → **400** `Dữ liệu đang được sử dụng, vui lòng tải lại`.
- FE **ẩn hẳn** nút theo cờ BE (`is_can_delete` / `is_can_lock_update`), không disable.
- LVKDNB bị khoá vẫn hiển thị đúng tên ở Nhóm ngành đang gán, trong dropdown có 🔒 (quy tắc chung
  CLAUDE.md — `getAll` nhận `include_ids`).

## Bố cục form Thêm/Sửa (chốt 2026-08-23)

Thêm 1 trường vào form 4 ô cũ làm select Lĩnh vực nằm trơ 1 dòng → bố trí lại **2 hàng cân đối**,
mỗi hàng lấp đầy 12 cột:

| Hàng | Bố cục |
| --- | --- |
| 1 | `Mã nhóm ngành (col-md-4)` + `Tên nhóm ngành (col-md-8)` |
| 2 | `Lĩnh vực kinh doanh nội bộ (col-md-8)` + `Trạng thái (col-md-4)` |
| 3 | `Mô tả (col-md-12)` |

Hai trường quan trọng nhất (Tên, Lĩnh vực) cùng độ rộng 8/12; không ô nào bị cụt.
Ảnh: `screenshots/nhomnganh-modal-bocuc-moi.png`.

## Phạm vi kỹ thuật

- **DB**: `scopes.internal_business_scope_id` (unsignedBigInteger nullable + index) + backfill.
  Cột để nullable, **bắt buộc do BE validate** — không khoá cứng schema.
- **BE**: `Scope` (fillable + quan hệ), `InternalBusinessScope` (quan hệ + 2 hàm chặn),
  `ScopeRequest` (required + phải đang hoạt động, trừ khi giữ nguyên giá trị cũ đã khoá),
  `ScopeService` (lọc + eager load + lưu + import), 2 Resource, `ScopeController` (guard lock),
  `InternalBusinessScopeController` (guard delete/lock + `include_ids` cho getAll),
  blade export `scopes`.
- **FE**: `pages/assign/industry-groups/{index.vue, AddScopeModal.vue}` +
  `static/Mau_import_NhomNganh.xlsx`.
- **E2E**: bổ sung ca vào `e2e/tests/assign/` (form bắt buộc, cột, bộ lọc, chặn xoá LVKDNB đang dùng).

## Tài liệu kèm theo

- `testcase.xlsx` — 56 test case cho QA (sinh bằng `gen_testcase.py`, engine chuẩn của team):
  6 ca phân quyền + 10 nhóm nghiệp vụ (hiển thị/bố cục form · bộ lọc · danh sách · tạo-sửa-xem ·
  trạng thái & danh mục bị khoá · xoá · xuất/nhập Excel · ràng buộc nhập liệu · thao tác đồng thời ·
  luồng tổng thể). P0 chiếm 55%.
- `screenshots/` — ảnh chụp thật màn hình.

**Spec chi tiết** của danh mục nguồn: `docs/superpowers/specs/2026-08-22-linh-vuc-kinh-doanh-noi-bo-design.md`
