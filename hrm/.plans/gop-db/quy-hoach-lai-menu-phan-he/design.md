# Quy hoạch lại menu & phân hệ theo sơ đồ chốt 04/09/2026

**Người phụ trách:** @junfoke — 2026-09-16

## Mục tiêu

Sắp xếp lại **nhóm / phân hệ / menu** của `hrm-client` theo bản quy hoạch mới nhất user cấp:
Google Sheet `1s8fb8lWuP6o4LjUcwk77Wkh5nx0x8tkq9dNeV1P41tg`, **5 sheet = 5 nhóm**
(QUẢN TRỊ LÕI, NHÂN SỰ, VĂN PHÒNG SỐ, SẢN XUẤT - CUNG ỨNG, KINH DOANH - TÀI CHÍNH).

Khác với `bo-sung-menu-phan-he` (làm 2026-08-01 theo sheet `Gộp phân hệ ERP-HRM` cũ): bản này
**đổi cấu trúc** — tách/gộp phân hệ, đổi tên hàng loạt, dời chức năng giữa các phân hệ.

## Quy ước đọc sheet (BẮT BUỘC, CSV không mang được)

| Định dạng ô | Nghĩa |
| --- | --- |
| Gạch ngang (strikethrough) | **Đã bỏ / đã chuyển sang phân hệ khác** — không khai menu |
| Nền vàng tươi `FFFF00` | Chưa xây dựng, **dự kiến làm sau** — vẫn khai menu, chưa có `link` |
| Nền vàng đậm `FFD966` | Mục mới bổ sung 03/09 |
| Nền vàng nhạt `FFF2CC` | Ô ghi chú / link ảnh, không phải trạng thái |

**Gạch thắng vàng**: ô vừa vàng vừa gạch = bỏ. Cột `Ghi chú` chứa "Tên cũ: …" → phần lớn công
việc là ĐỔI TÊN, không phải làm màn mới. Cách đọc lại sheet: xem memory `project_khung_phan_he_fe`.

## Quyết định chính (user chốt 16/09/2026)

1. **Quản lý công việc** thuộc nhóm VĂN PHÒNG SỐ (bản bên KINH DOANH bị gạch toàn bộ).
2. **Meeting** tách khỏi Quản lý công việc thành **phân hệ riêng** (khối Danh mục/Meeting trong
   QLCV bị gạch).
3. **Quản lý CSKH trước khi bán** (tên cũ: dự án TKT) tách khỏi hub Bán hàng thành phân hệ riêng.
4. **Tra cứu - thông báo** đứng riêng đầu nhóm KINH DOANH (bản nằm trong Bán hàng bị gạch).
5. **Hai phân hệ khác nhau, KHÔNG gộp**: `Ban hành văn bản nội bộ (Quyết định - quy định - quy chế)`
   (tên cũ: Vận hành nội bộ → key `operation`) và `Ban hành văn bản nội bộ` (tên cũ: Quyết định →
   key `decision`).
6. **Quản lý an toàn 5S** tách khỏi ISO thành phân hệ riêng — tách khung trước, chức năng bổ sung sau.
7. **Đánh giá KPI** nằm ở nhóm NHÂN SỰ (bản ở VĂN PHÒNG SỐ bị gạch) — đúng như registry hiện tại.
8. Mục chưa có màn: khai menu **không có `link`** → sidebar render xám mờ (cơ chế sẵn có).

## Scope

- Chỉ đụng `hrm-client`: `components/subsystems.js`, `components/subsystem-menu/*.js`,
  `components/menu.js`, `components/menu-sidebar.js`, `components/default-menu/*.js`.
- Thêm 3 phân hệ: `meeting`, `presale` (CSKH trước bán), `safety-5s`.
- Đổi nhãn: `operation`, `decision`, `iso`, `customer-care`, `training`, `insurance`.
- Dời chức năng giữa phân hệ theo cột gạch ngang (bảo hiểm → Bảo hiểm, thông báo nội bộ →
  Ban hành VB nội bộ, ngân hàng câu hỏi khảo sát → Danh mục dùng chung…).

**Không làm:** viết màn mới, phân quyền cho mục mới, dashboard theo cột `Dashboard` của sheet
(khối việc riêng), di chuyển code page sang route mới.

## Rủi ro / bất biến

- **1 link chỉ được nằm trong menu của ĐÚNG 1 phân hệ** — `resolveSubsystem()` dựa vào đó.
  Sau mỗi phase phải chạy script đếm link trùng.
- Màn bị **tách đôi theo sheet** thì không dời được nguyên link (vd `/human/settings` chứa cả
  "Dùng định biên nhân sự" lẫn "Lương cơ bản / thâm niên") → giữ nguyên chỗ cũ, ghi vào mục
  "Chờ user chốt" của plan.md.
- Không xoá mục menu chỉ vì sheet không nhắc tới — sheet không liệt kê hết màn đã có.

Chi tiết từng mục: `docs/superpowers/specs/gop-db/2026-09-16-quy-hoach-lai-menu-phan-he-design.md`
