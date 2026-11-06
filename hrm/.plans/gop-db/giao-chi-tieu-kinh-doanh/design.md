# Giao chỉ tiêu kinh doanh (ERP → HRM) — #11643 theo phòng ban + #11651 theo nhân viên

**Người phụ trách:** @junfoke — 2026-11-06
**Spec đầy đủ:** `docs/superpowers/specs/gop-db/2026-11-06-giao-chi-tieu-kinh-doanh-design.md`
**Plan:** `plan.md` (viết sau khi duyệt thiết kế)

## Mục tiêu
Port 2 màn phiếu giao chỉ tiêu KD sang HRM (phân hệ Bán hàng), giao diện mới theo bản mẫu HTML QA đính kèm issue.
Làm chung 1 đợt, **phòng ban trước** (phiếu nhân viên nạp chỉ tiêu từ phiếu phòng ban Đã duyệt).

## Thay đổi so với ERP
- Bỏ popup chi tiết khách hàng + "Khách hàng mới": 8 ô số nhập thẳng trên dòng.
- Bỏ "Nhân viên mới": chỉ chọn nhân viên danh mục, ô chọn có tìm, không trùng trong 1 tỉnh.
- Phòng ban thêm cấp **Bộ phận** tuỳ chọn (danh mục `parts` có sẵn) → bảng mới `business_target_department_parts`
  lưu số theo bộ phận; dòng phòng = tổng bộ phận (nơi khác đọc dòng phòng không đổi).
- Chỉ sửa khi Đang tạo; bỏ xoá → **Hủy** (status 5); 1 phiếu hiệu lực / (công ty, năm) hoặc (công ty, phòng, năm).
- Duyệt phiếu nhân viên bằng quyền "…theo nhân viên" (ERP dùng nhầm quyền phòng ban).
- Giao vượt chỉ tiêu phòng: tô cam, không chặn (ERP chặn khi tổng giao < chỉ tiêu).
- Quyền mới guard `api`, type 23 (8 quyền).

## Quyết định đã chốt (user, 06/11/2026)
| # | Quyết định |
|---|---|
| 1 | Sửa 2 báo cáo giao chỉ tiêu ERP: đếm số khách hãng = SUM cột SL khách đã nhập, không đếm bảng chi tiết KH |
| 2 | Bộ phận lấy từ danh mục `parts` có sẵn; bảng mới chỉ để lưu số theo bộ phận trong phiếu |
| 3 | Ẩn menu tạo/sửa/chờ duyệt 2 màn bên ERP sau khi HRM chạy (route giữ cho báo cáo/kế hoạch) |
| 4 | Làm trên nhánh mới tách từ `gop_db` (hrm-api, hrm-client, TanPhatDev) |
| 5 | Sửa phiếu đã duyệt: **Hủy duyệt** → Đang tạo (như các phiếu khác), không có "Thu hồi". Phiếu phòng ban bị chặn Hủy duyệt khi đã có phiếu nhân viên Chờ duyệt/Đã duyệt dùng chỉ tiêu của nó |
| 6 | Phiếu nhân viên chọn phòng theo ERP: phòng mình quản lý; có quyền xem công ty/tổng công ty → mọi phòng; BE kiểm cùng luật |
| 7 | Số theo bộ phận đợt này chỉ lưu + xem/in/xuất (nhân viên/kế hoạch/báo cáo vẫn đọc tổng phòng) |

## Dùng lại / bám
- Bảng ERP `business_target_*` (DB gộp); dữ liệu cũ (9 + 43 phiếu Đã duyệt) giữ nguyên.
- Khuôn: Phiếu phân chia thị trường #11694/#11695 (`Modules/Finance` DivisionMarket*, `pages/finance/division-market-*`).
- FE dùng chung cho 2 màn: `TargetTreeTable.vue` (bảng cây 12 cột), mixin hành động, helper tính tổng.

## Ngoài phạm vi
Port 2 màn báo cáo, Giao chỉ tiêu phát triển sản phẩm, hộp duyệt tập trung, thu hồi phiếu chờ duyệt.
