# Design (tóm tắt) — Điều kiện thanh toán cho Tiến độ thanh toán HĐ

**Phụ trách:** @dangquang.tom
**Nhánh:** `develop` (gop_db) — cả hrm-api + hrm-client
**Spec chi tiết:** `docs/superpowers/specs/gop-db/2026-10-16-dieu-kien-thanh-toan-design.md`

## Mục tiêu
Nền tảng dữ liệu cho Tiến độ thanh toán HĐ (module Assign): dựng danh mục điều kiện thanh toán cố
định + cho mỗi đợt thanh toán chọn 1 điều kiện và nhập số ngày bắt đầu tính thanh toán, lưu vào HĐ.
Chưa làm cảnh báo thu tiền/công nợ, chưa làm nhập ngày thực tế + biên bản.

## Quyết định đã chốt
- Hướng 1: bảng danh mục riêng `payment_conditions` seed cố định 8 giá trị (global) + 2 cột mới
  (`payment_condition_id`, `offset_days`) trên `hrm_contract_process_payments`.
- Danh mục cố định (A), global, chưa có màn admin.
- Làm cả 2 cột (điều kiện + số ngày) trong 1 đợt.
- KHÔNG bắt buộc nhập đợt này (nullable, không rule required); siết required khi làm cảnh báo.
- Áp cho cả màn Tạo mới + Sửa (component dùng chung, create.vue extends edit.vue).

## Scope
- TRONG: danh mục + 2 cột + FE/BE lưu-đọc.
- NGOÀI: cảnh báo quá hạn, ngày thực tế + biên bản/chữ ký, màn quản trị danh mục.

## 8 điều kiện (seed)
Kể từ ngày ký · Kể từ ngày HĐ có hiệu lực · Phê duyệt thiết kế · Giao hàng lần 1 có chữ ký KH ·
Giao hàng lần 2 có chữ ký KH · Lắp đặt có chữ ký KH · Chạy thử Có chữ ký KH · Bàn giao nghiệm thu.
