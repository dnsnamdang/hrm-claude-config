# Kế hoạch bán hàng + KH phát triển thị trường của nhân viên (ERP → HRM) — #11884 + #11885

**Người phụ trách:** @junfoke — 2026-11-14
**Spec đầy đủ:** `docs/superpowers/specs/gop-db/2026-11-14-11884-11885-ke-hoach-nhan-vien-design.md`
**Plan:** `plan.md` (viết sau khi duyệt thiết kế)
**Bản chốt của khách:** 2 file demo đính kèm issue (`ke-hoach-ban-hang-cua-nhan-vien (1).html`, `ke-hoach-phat-trien-thi-truong-theo-nhan-vien (1).html`)

## Mục tiêu
Port 2 màn phiếu kế hoạch của nhân viên sang HRM (phân hệ Bán hàng ▸ Kế hoạch), giao diện + luật theo demo khách gửi.
Bỏ tầng Khách hàng: nhập số thẳng trên dòng Tỉnh/TP. Làm chung 1 đợt, **KH phát triển thị trường trước** (ít cột hơn),
rồi KH bán hàng (thêm Doanh số xuất hàng). Hai màn dùng chung khung bảng / luồng duyệt / nút lấy dữ liệu chéo.

## Thay đổi so với ERP
- Bỏ Khách hàng / Người liên hệ / Phân loại khách. Dòng Tỉnh/TP có ô **SL khách** (bắt buộc) — ERP đếm khách, nay nhập tay.
- KH bán hàng thêm cột **Doanh số xuất hàng** (tuỳ chọn).
- Tỉnh/TP chỉ chọn trong **chỉ tiêu được giao** (phiếu giao chỉ tiêu NV Đã duyệt, cùng năm). Chưa có chỉ tiêu từ năm nay trở đi ⇒ chặn Tạo mới.
  ERP: KH bán hàng chặn lưu khi chưa đạt chỉ tiêu; nay **chỉ hiển thị so sánh, không chặn**. KH PTTT ERP không đọc chỉ tiêu.
- **Nhiều phiếu / NV / năm** (ERP chặn 1). Phiếu luôn của chính tài khoản lập.
- Trưởng bộ phận thấy thêm phiếu nhân viên trong bộ phận (chỉ xem). Phiếu trưởng phòng lập ⇒ gửi thẳng Chờ BGĐ duyệt.
- Nút **Gửi BGĐ** trên phiếu TP đã duyệt (ERP: lên BGĐ qua KH phòng ban). Từ chối ⇒ về Đang tạo.
- Nút **Lấy dữ liệu từ kế hoạch kia** theo hệ số chuyển đổi (báo giá ÷ hệ số = hợp đồng; ngược lại nhân).
- 3 tab Chi tiết theo tháng / Theo thị trường (so chỉ tiêu) / Theo tháng; In 3 kiểu A4 ngang; Xuất Excel.
- Bỏ xoá phiếu ⇒ **Hủy** (người lập, khi Đang tạo / Chờ TP duyệt).

## Quyết định đã chốt (user, 14/11/2026)
| # | Quyết định |
|---|---|
| 1 | Demo đính kèm issue là bản chốt của khách — làm theo demo ở mọi điểm khác ERP |
| 2 | ~16 báo cáo ERP + KH phòng ban / công ty đang đọc dòng khách hàng: **sửa sau**, đợt này chỉ làm phần lập kế hoạch |
| 3 | Phiếu ERP cũ (có dòng khách hàng) chỉ giữ để **xem**, không sửa / chuyển đổi |
| 4 | Màn BGĐ duyệt làm sau (menu Chờ duyệt tập trung). Đợt này chỉ tới **Chờ BGĐ duyệt** |
| 5 | Phạm vi xem = ERP (mã `.view` mức Phòng ban / Công ty / Tổng công ty) **cộng** vai trò demo: phiếu mình lập, TP thấy phiếu phòng mình quản lý, TBP thấy phiếu bộ phận mình quản lý, phiếu mình đã duyệt |
| 6 | Ẩn menu lập / danh sách / chờ duyệt 2 màn nhân viên bên ERP, giữ route cho báo cáo + KH phòng ban |

## Quyết định tự chốt theo ERP / màn cùng loại (ghi để QA khỏi hỏi)
- Phiếu mới đánh dấu `form_version = 2`; phiếu cũ (`= 1`) chỉ Xem / In / Xuất Excel.
- Từ chối cấp TP bắt buộc lý do (ERP bắt comment; khớp Giao chỉ tiêu HRM). Không làm Hủy duyệt (demo không có).
- Người duyệt cấp TP theo luật ERP `canDepartmentApprove` (quản lý phòng của người lập, hoặc có mã approve cùng phòng).
- Quy đổi lấy dữ liệu chéo tính ở BE, không lưu phiếu nguồn / hệ số.

## Dùng lại / bám
- Bảng ERP `sales_employee_plan_*`, `market_employee_plan_*` (DB gộp) + thêm cột ở tầng tỉnh / tháng / phiếu.
- Chỉ tiêu: `business_target_for_departments` (status 3) → `_provinces` → `_employees`.
- Khuôn code: Giao chỉ tiêu theo nhân viên (`Modules/Finance` BusinessTarget*, `pages/finance/business-target-employees`).

## Ngoài phạm vi
Màn BGĐ duyệt / hộp duyệt tập trung, sửa các báo cáo ERP + KH phòng ban / công ty, chuyển đổi phiếu cũ.
