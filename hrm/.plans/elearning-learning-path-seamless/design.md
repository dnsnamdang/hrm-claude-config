# Elearning — Học liền mạch lộ trình (tóm tắt)

> Owner: @junfoke · Spec đầy đủ: `docs/superpowers/specs/2026-06-03-elearning-learning-path-seamless-design.md`

## Mục tiêu
Học một lộ trình nhiều khoá liền mạch: vào học từ trang lộ trình, đi hết khoá này sang khoá khác,
chứng chỉ cấp lộ trình khi hoàn thành. **Không** tạo màn học gộp — vẫn học per-khoá bằng
`SubjectLearnView`, lộ trình là lớp điều hướng + context bọc ngoài.

## Quyết định lớn
- Context `?lp=<slug>` truyền vào màn học → quyết định nút Quay lại (về lộ trình), khoá tiếp theo.
- "Tiếp tục học" resume đúng bài đang dở (xuyên khoá).
- `linear_required=true` → khoá khoá sau cho tới khi xong khoá trước (lock cấp khoá, BE tính cờ `locked`).
- Modal hoàn thành 3 biến thể: học khoá tiếp theo / hoàn thành lộ trình (+chứng chỉ) / khoá lẻ (cũ).
- Chứng chỉ lộ trình: mirror chứng chỉ khoá (LP đã có sẵn cột cert), endpoint riêng, tính done on-demand.
- **Không migration** (cột cert + linear_required đã có). Không sửa `CertificateService` khoá (tạo service LP riêng).

## Trạng thái
Brainstorm DONE, spec DONE (2026-06-03). Chờ user review spec → lập plan.
