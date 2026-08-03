# Design (tóm tắt): KH cá nhân không cần người liên hệ

**Module:** Assign | **Người phụ trách:** @manhcuong | **Ngày:** 2026-06-29

## Mục tiêu
KH là cá nhân (`customer_type === 1`) → ẩn hẳn block người liên hệ + không bắt buộc contact. KH doanh nghiệp (type 2–5) → giữ bắt buộc người liên hệ.

## Phạm vi
2 màn module Giao việc, cả thêm + sửa (dùng chung component nên tự phủ):
- Dự án tiền khả thi: add + edit
- Meeting: create + edit

## Quyết định lớn
1. Cá nhân ⇔ `customer_type === 1`; null/khác coi như doanh nghiệp.
2. UI: **ẩn hẳn** block người liên hệ khi cá nhân.
3. Đổi KH sang cá nhân → **xoá sạch** dữ liệu contact, không gửi BE.
4. BE đồng bộ: doanh nghiệp bắt buộc tên + SĐT liên hệ; cá nhân nullable.

## Điểm chạm code
- FE Prospective: `CustomerBlock.vue` (2 block direct/benefit) — ẩn + reset theo `val('type')`.
- FE Meeting: `GeneralInfo.vue` (ẩn + reset) + `MeetingForm.vue` `validate()` (contact required khi type ≠ 1).
- BE: `MeetingCreateApiRequest` + request update Meeting; `ProspectiveProjectRequest` (chỉ block direct).

## Không làm
Không permission, không migration, không git, không đụng masking.

→ Spec chi tiết: `docs/superpowers/specs/2026-06-29-customer-individual-no-contact-design.md`
