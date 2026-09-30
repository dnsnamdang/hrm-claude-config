# Plan — Sửa thanh tab khi có nhiều tab (V2BaseTabNavigation)

Nhánh: `tpe` (worktree `HRM/worktrees/tpe-client` :3005) · @cuong61n

## Phase 1 — FE
- [x] Lỗi: `.tabs-root` inline-flex không `nowrap`/`flex-shrink:0` → 11 tab ở `/assign/prospective-projects/{id}/manager` bị bóp, chữ gãy 2-3 dòng, tab cuối tràn khỏi card (cả `solutions/_id/manager` 10 tab, `solution-modules/_id/manager` 9 tab)
- [x] `components/V2BaseTabNavigation.vue`: tab 1 hàng (`white-space: nowrap` + `flex: 0 0 auto`), thanh cuộn ngang ẩn scrollbar, 2 nút mũi tên ‹ › chỉ hiện khi tràn (disable ở đầu/cuối), tự cuộn tab đang chọn vào tầm nhìn, đo lại bằng ResizeObserver
- [x] Kiểm UI :3005 — màn TKT 272 (11 tab, có mũi tên) + `/assign/my-job` (7 tab, không mũi tên, giữ nguyên hình thức cũ)

- [x] Thu gọn + làm phẳng thanh tab: cao 36px (trước ~52px), chữ 13px / icon 15px, bo 10px, nền track `#f1f5f9`, tab active xanh brand `#16a34a` phẳng (bỏ bóng xanh đổ), hover xám `#e2e8f0`; mũi tên đổi từ nút tròn viền sang chevron mảnh 20px; thêm vệt mờ ở mép đang bị cắt
- [x] Kiểm lại UI: TKT 272 hiện 10/11 tab trong 1 hàng (trước 8), my-job 7 tab gọn không mũi tên

- [x] Canh lề trái: mũi tên chuyển sang nằm ĐÈ lên mép track (absolute, không chiếm chỗ) + `manager.vue` đổi `ml-3` (24px) → `.tab-nav-align` 15px ⇒ thanh tab thẳng hàng với nội dung trong tab (đo: track 246px = content 246px)
- [x] Màu tab chưa chọn hết bị trông như disabled: chữ `#64748b` → `#334155`, icon `#64748b` (bỏ opacity 0.85), hover đổi từ nền xám sang **viên trắng + chữ/icon xanh `#15803d`** + bóng nhẹ; mũi tên bỏ trạng thái disabled, chỉ hiện đúng phía còn tab bị khuất

- [x] Nền thanh tab xám `#f1f5f9` làm tab chưa chọn trông như disabled → đổi track sang **trắng `#ffffff`** (viền `#e2e8f0` giữ nguyên để thấy vùng cuộn), hover đổi sang xanh rất nhạt `#f0fdf4` + chữ `#15803d`, vệt mờ mép cuộn đổi theo nền trắng

- [x] Trạng thái tab có lỗi validate (`hasError`): tab KHÔNG active → **chữ + icon chức năng + icon cảnh báo đều đỏ `#dc3545`** (trước đó icon bị `.tab-icon` ép xám nên không đỏ theo chữ), hover nền `#fef2f2` chữ `#b91c1c`; tab ĐANG mở mà còn lỗi → **nền đỏ đặc `#dc3545` chữ/icon trắng** thay cho nền xanh + viền đỏ (2 màu cũ chồng nhau rối)
- [x] Kiểm trên `/assign/meeting/create`: bấm "Lưu và Chốt lịch" → tab Thông tin đỏ đặc khi đang mở, chuyển sang tab Điểm danh thì Thông tin chuyển chữ+icon đỏ trên nền trắng

### Checkpoint — 2026-09-16
Vừa hoàn thành: fix component chung V2BaseTabNavigation + kiểm UI 2 màn.
Đang làm dở: (không)
Bước tiếp theo: user rà thêm `solutions/_id/manager`, `solution-modules/_id/manager`; chưa commit git.
Blocked: (không)
