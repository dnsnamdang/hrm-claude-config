# Danh sách người dùng / vai trò cần xem xét cấp lại quyền sau chuyển đổi

> Lập 03/11/2026 từ báo cáo **lần chạy thật diễn tập 26/10** (`../bao-cao-dien-tap/chay-that/`) + DB `hrm_erp_rbac_rehearsal`
> (GĐ2c, GĐ3b). Chỉ tính **NV đang làm** (`employee_infos.status = 1`).
>
> **Bản gửi quản trị viên: `danh-sach-cap-lai-quyen.xlsx`** (8 sheet: Hướng dẫn · 1 · 1b chi tiết 20,750 quyền · 2 · 3 · 4 · 5 · 6, tiêu đề
> cột tiếng Việt, cột vàng để ghi quyết định xử lý). Sinh lại bằng `build_xlsx.py` (cùng thư mục; cần `emp.tsv`, `cty.tsv`, `gd2c.tsv` xuất từ DB — xem đầu script). CSV giữ để tra nhanh.
>
> ⚠️ **Đây là danh sách diễn tập.** Runbook bước 4 / go-live A5: lúc go-live phải phát lại danh sách từ **chính lần chạy go-live**
> (dữ liệu prod sẽ khác). Dùng file này để quản trị viên làm quen và chuẩn bị trước.

## Người dùng

| # | File | Nội dung | Quy mô | Việc quản trị viên làm |
|---|---|---|---|---|
| 1 | `1-nv-mat-quyen-do-bit-ro.csv` | Quyền NV có được **chỉ nhờ cách tính cũ không xét công ty** (vai trò/dòng cấp quyền ở công ty khác vẫn có hiệu lực). Sau chuyển đổi bị đóng — `mat-do-bit-ro` = (thực tế đang chạy) − (đúng công ty) | **384 NV · 439 cặp NV×công ty** (379 cặp ngay công ty hồ sơ). Mất 1 quyền: 18 · 2–5: 191 · 6–20: 85 · 21–100: 102 · >100: 43 | Xét từng người: quyền nào thật sự cần ở công ty đó thì gán Vai trò của **chính công ty đó** (màn Vai trò nhân viên), hoặc thêm quyền vào Vai trò của công ty. Ưu tiên 43 cặp mất > 100 quyền |
| 2 | `2-nv-mat-truy-cap-cong-ty.csv` | NV **mất hẳn quyền vào một công ty** — trước có nhờ danh sách công ty của vai trò (`company_roles`), nay vai trò không có bản ở công ty đó | **14 NV · 55 dòng** — vai trò cũ: `Super admin (DNS DÙNG)` (18), `Admin_TPE` (19), `Kế toán_TPE` (10), `Xem báo cáo hàng giữ` (100138) | Gán Vai trò tương ứng của từng công ty cho người cần làm việc ở đó (cột "dùng được trên giao diện" cho biết mất bao nhiêu quyền thật sự dùng) |
| 3 | `5-gd2c-ha-pham-vi-tong-cong-ty.csv` | **GĐ2c (chủ ý, user chốt 01/11):** 6 công ty ≠ TPE tắt phạm vi Tổng công ty ⇒ quyền phạm vi 4 tính như phạm vi Công ty | **119 NV · 140 cặp · 87 vai trò · 2,725 dòng quyền**, ở 5 công ty có dữ liệu | Không cấp lại — chỉ báo người dùng biết; muốn mở lại cho công ty nào thì NV 13 bật ở màn Cấu hình phạm vi Tổng công ty |
| 4 | (không file) | **GĐ3b Q4:** duyệt vượt hạn mức HĐ dự án TKT + phạm vi xoá liên hệ KH ở hrm-api chỉ tính mã ở công ty đang làm | **1 NV: 197 Trần Thị Hương** (Giám đốc ở DTTDETEK, đang làm TPE) | Nếu bà Hương cần duyệt ở TPE: gán Vai trò TPE_Giám đốc ở TPE (hoặc cấp mã `sale.hop_dong_vuot_han_muc.approve` + `sale.khach_hang_pham_vi.view` vào vai trò của bà ở TPE) |

## Vai trò

| # | File | Nội dung | Quy mô | Việc quản trị viên làm |
|---|---|---|---|---|
| 5 | `3-vai-tro-thieu-quyen-xem.csv` | Vai trò có quyền thao tác (duyệt/sửa…) nhưng **thiếu quyền Xem** đi kèm ⇒ có nút mà không mở được màn | **54 vai trò · 106 dòng** — nhiều nhất: TPE_Giám đốc phòng PTKD (6), TPE_Trưởng phòng XNK (6), TPE_Trưởng phòng CSKH (4), TPE_Giám đốc (4), EG_Giám đốc (4), TPHP_Giám đốc chi nhánh (4) | Thêm mã Xem còn thiếu (cột `ma_xem_con_thieu`) vào vai trò, hoặc bỏ mã thao tác nếu không dùng |
| 6 | `4-du-lieu-tro-vai-tro-can-chon-lai.csv` | Cấu hình nghiệp vụ trỏ vào **id vai trò không chuyển được** sang vai trò mới (không xác định được công ty / công ty không có bản vai trò) | **18 dòng**: `companies.deputy_role` (4), `self_inventory_members` (6), `inland_buy_contract_annexes`/`inland_buy_contracts`/`rule_inland_buy_contracts`/`inland_buy_contract_news` người duyệt/ký (7), `position_inventory_members` (1) | Mở cấu hình tương ứng, chọn lại vai trò của đúng công ty (vd Phó giám đốc của công ty, thành viên kiểm kê, người duyệt/ký HĐ mua) |

Không cần làm gì (để biết): `vai-tro-khong-chuyen` 0 · `trung-ten-vai-tro` 0 · `vai-tro-ngung-van-cap-quyen` 0 · 45 dòng
`role_permission_history` trỏ id vai trò cũ (lịch sử, chỉ hiển thị) · `quyen-bo-theo-danh-muc` 98 tên quyền bị bỏ vì không còn code
nào kiểm (không đổi hành vi) · `du-lieu-mo-coi-nhan-vien` 13 dòng gán vai trò cho NV không tồn tại (B.4b dọn).
