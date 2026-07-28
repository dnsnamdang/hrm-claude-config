# Cấu hình trang chủ Elearning — Tóm tắt

- **Owner**: @junfoke | **Ngày**: 2026-07-23 | **Trạng thái**: Design
- **Spec đầy đủ**: [docs/superpowers/specs/2026-07-23-cau-hinh-trang-chu-elearning-design.md](../../docs/superpowers/specs/2026-07-23-cau-hinh-trang-chu-elearning-design.md)

## Mục tiêu
Cho admin cấu hình 2 phần đang fix cứng trên trang chủ portal elearning:
1. **Hero slide**: bật/tắt + sắp thứ tự ưu tiên 4 nhóm nguồn (`need / recommend / popular / newest`) + số slide tối đa. **Giữ cá nhân hoá** (data theo user), chỉ điều khiển "luật" trộn.
2. **Footer**: Thông tin liên hệ (email/sđt/địa chỉ) + Khối giới thiệu (text + bật/tắt). Bỏ chữ "(Demo)".

## Quyết định lớn
- **Mô hình Hero**: cấu hình nguồn động (không phải chọn tay từng khóa).
- **Tổ chức**: gộp 1 màn "Cấu hình trang chủ Elearning" (2 tab), 1 quyền `Quản lý cấu hình trang chủ elearning`.
- **Lưu trữ**: 1 bảng singleton `elearning_home_settings` (hero_sources dạng JSON) — idiom `HallOfFameSetting::current()`.
- **Kiến trúc**: admin UI hrm-client `/training/home_config` → BE ghi `Modules/Training` → learner đọc `Modules/Elearning` `public/site-config` → FE elearning store.

## Ngoài phạm vi
Quick links / bản quyền / version footer giữ cứng; không bật/tắt cả khối hero; không chọn tay khóa; không cấu hình autoplay.

## Bước tiếp
User review spec → writing-plans lập plan.md → code.
