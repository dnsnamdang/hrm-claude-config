# PLAN — Đồng bộ header màn chi tiết phân hệ Quản lý dự án TKT

Chốt với user (2026-08-18):
- Khuôn tiêu đề topbar theo skill `list-page` mục 7.1: `Chi tiết <đối tượng>: <MÃ> (<Trạng thái>)`
  — mã in đậm, trạng thái tô màu `status_color` BE trả về; chưa có dữ liệu thì để tiêu đề trần.
- Thay khuôn cũ `MÃ — Chi tiết X` (đặt ở #10814) trên toàn nhóm menu "Quản lý dự án TKT" + Meetings.
- Nhánh: `hrm-client` / `hrm-api` đều đứng trên `tpe-develop-assign_fix` (checkout từ `tpe`).

## FE (hrm-client)
- [x] Thêm helper dùng chung `utils/detailPageTitle.js` (`buildDetailPageTitle` + `escapeHtml`)
- [x] Chi tiết báo giá — `quotations/_id/index.vue`: bổ sung chữ "Chi tiết" (giữ chip cấp duyệt)
- [x] Chi tiết dự án tiền khả thi / dự án cha — `prospective-projects/_id/index.vue` (+ status_name)
- [x] Chi tiết yêu cầu giải pháp — `request-solution/_id/index.vue` (+ status_text/color)
- [x] Chi tiết giải pháp — `solutions/_id/index.vue` (+ status_text/color)
- [x] Quản lý giải pháp — `solutions/_id/manager.vue` (+ mã, status_text/color)
- [x] Quản lý hạng mục — `solution-modules/_id/manager.vue` (+ mã, status_text/color)
- [x] Chi tiết BOM List — `bom-list/_id/index.vue` (+ status_name/color, bỏ commit pageTitle thủ công)
- [x] Chi tiết yêu cầu XD giá — `pricing-requests/_id/index.vue` (+ mã/trạng thái; gộp 2 khối `computed`
      trùng nhau làm `pageTitle` cũ không bao giờ chạy)
- [x] Chi tiết báo giá tổng — `summary-quotations/_id/index.vue` (+ khuôn chuẩn, trước là `Báo giá tổng <mã>`)

## BE (hrm-api)
- [x] `DetailBomListResource`: trả thêm `status_name` / `status_color` (cùng nguồn `BomList::getStatusList()`
      với màn danh sách) để header BOM có trạng thái

## Footer che nội dung (port từ nhánh gop_db)
- [x] `components/V2Footer.vue`: lấy nguyên bản gop_db (commit `5ccf37fee`) — bọc thanh nút `position: fixed`
      trong khối tĩnh `.v2-footer-spacer` cao 66px để mọi màn tự có chỗ trống ở đáy
- [x] Bỏ hack chừa chỗ ở từng màn (đã thừa): `meeting/_id/show.vue` (margin-bottom 64px),
      `summary-quotations/_id/index.vue` + `_id/edit.vue` + `add.vue` (padding-bottom 70px),
      `components/assign-components/customer/CustomerForm.vue` (inline 70px),
      `bom-list/_id/index.vue` (inline 64px)
- Không port phần còn lại của commit gop_db (màn danh mục Finance/Customer-care… khác nhánh nhiều)

## Còn treo
- Meeting: header mới chỉ `Chi tiết meeting: <mã>` — BE `Meeting::STATUS` đặt tên khác FE danh sách
  ("Đang tạo/Lên lịch/Chốt lịch" vs "Lưu nháp/Lên lịch hẹn/Đã chốt lịch") nên chưa gắn trạng thái vào
  tiêu đề, tránh 2 nơi hiện 2 chữ khác nhau. Cần chốt bộ chữ chuẩn rồi mới bổ sung.
- Skill `.claude/skills/list-page/SKILL.md` nên ghi thêm helper `utils/detailPageTitle.js` + quy ước
  chip trạng thái trong tiêu đề (tài sản chung → sửa qua PR).

### Checkpoint — 2026-08-18
Vừa hoàn thành: 10 màn FE + 1 resource BE, chưa test UI.
Bước tiếp theo: user build FE xem lại 10 màn (hoặc bảo tôi chạy Playwright).
