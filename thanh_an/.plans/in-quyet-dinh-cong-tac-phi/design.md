# In QUYẾT ĐỊNH cử đi công tác — Tóm tắt thiết kế

**Người phụ trách:** @khoipv
**Ngày:** 2026-06-15

## Mục tiêu
Đổi bản in màn `timesheet/jobassignment/:id/print` từ "GIẤY ĐI ĐƯỜNG" sang "QUYẾT ĐỊNH cử người lao động đi công tác" theo mẫu Word `Mau bieu cong tac phi (1).docx` (chỉ lấy trang 1 — phần QUYẾT ĐỊNH; bỏ phần Giấy đề nghị thanh toán & bảng nội dung công tác phí).

## Scope
- Chỉ sửa 1 file: `hrm-thanhan-client/pages/timesheet/jobassignment/_id/print.vue`.
- Không đụng backend/API/store — dùng dữ liệu API sẵn có.

## Quyết định lớn (đã chốt)
1. **1 bản quyết định** liệt kê tất cả nhân viên (bỏ `v-for` ngoài).
2. Header dạng **2 cột text theo đúng mẫu Word** (không dùng ảnh letterhead).
3. **Điều 1 dạng đoạn văn** — mỗi NV 1 dòng (Ông/Bà … Chức vụ … Thuộc đơn vị …).
4. Ngày tháng **để trống dạng chấm**, điền tay.
5. **Không có số quyết định** → bỏ dòng "Số:".

## Map dữ liệu
- Tên cty: `company_current.name` (fallback dấu chấm).
- Điều 1: `employee.fullname / employee_work_position / department`.
- Đi công tác tại: gộp distinct `place` trong `form`.
- Thời gian: `from_time` → `to_time`.

## Spec chi tiết
`docs/superpowers/specs/2026-06-15-in-quyet-dinh-cong-tac-phi-design.md`

## Plan triển khai
`docs/superpowers/plans/2026-06-15-in-quyet-dinh-cong-tac-phi.md`
