# Chuyển menu Nhóm giải pháp + Ứng dụng sang Danh mục dùng chung — Tóm tắt

> @khoipv · 2026-08-12 · nhánh `gop_db`
> Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-08-12-chuyen-menu-nhom-giai-phap-design.md`
> Task: `plan.md` cùng thư mục

## Mục tiêu

Đưa 2 mục menu **Nhóm giải pháp** (`/assign/solution-groups`) và **Ứng dụng** (`/assign/application`)
từ phân hệ **Bán hàng** (Danh mục → Dự án - Giải pháp) sang phân hệ **Danh mục dùng chung**,
thành 2 mục cấp 1 phẳng đứng sau `Nhóm ngành`.

## Quyết định chốt với user

| Câu hỏi | Chốt |
|---|---|
| Chuyển mục nào | **Nhóm giải pháp + Ứng dụng**. 4 mục còn lại của nhóm (Hạng mục / Giai đoạn / Vai trò dự án / Lý do thất bại) ở lại Bán hàng |
| Cấu trúc menu đích | **2 mục cấp 1 phẳng** sau Nhóm ngành (không gom thành nhóm `Giải pháp` có subItems) |
| Phạm vi lớp | **CHỈ menu** — giữ nguyên route, code FE/BE, quyền/seeder/DB |

## Thay đổi (3 file, chỉ `hrm-client`)

1. `components/subsystem-menu/sale-hub.js` — xoá 2 dòng khỏi mục `Dự án - Giải pháp` (còn 4 mục)
2. `components/subsystem-menu/sale.js` — xoá 2 entry `SALE_LINK_PERMISSIONS` đã thành code chết
3. `components/subsystem-menu/master-data.js` — thêm 2 mục cấp 1, giữ nguyên link + tên quyền cũ,
   icon `ri-lightbulb-line` / `ri-apps-2-line` (đã đối chiếu có trong `_remixicon.scss`)

Không phải sửa gì thêm: `resolveSubsystem()` map route → phân hệ theo link khai trong menu,
`default-sidebar.vue` chọn sidebar hub theo `HUB_SUBSYSTEMS` (master-data đã có),
`deriveHubNavLinks()` tự biến mục cấp 1 phẳng thành nút rail.

## Điểm cộng ngoài yêu cầu

3 link chéo giữa các màn (`industry-groups → solution-groups`, `industry-groups → application`,
`solution-groups → application`) sau đợt này nằm **cùng một phân hệ** → hết cảnh đang ở Danh mục
dùng chung bấm sang lại nhảy về sidebar Bán hàng.

## Nợ kỹ thuật giữ nguyên (giống đợt Nhóm ngành)

4 quyền của 2 màn vẫn `group = 'Danh mục'` → màn **Phân quyền** vẫn xếp chúng ở tab
*Giao việc › Danh mục*. Đổi mỗi `type` là vô ích hoặc kéo nhầm cả nhóm quyền Giao việc sang tab
khác (`Permission.vue` gom khối chỉ theo tên `group`) — xem mục 2.1 của spec.
