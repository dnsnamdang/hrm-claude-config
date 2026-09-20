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
5. ~~**Hai phân hệ khác nhau, KHÔNG gộp**~~ → **ĐẢO 16/09/2026 (chiều): user chốt GỘP làm 1**,
   tên **"Văn bản nội bộ"**, subtext **"Quyết định, Quy chế công ty"**. `decision` (tên cũ: Quyết
   định) biến mất khỏi registry; `operation` giữ `slugs: ['operation','decision','regulations']`,
   `permissionType: 6`, `isShowKey: 'is_use_decision'`; 36 link dời từ `default-menu/decision.js`
   (đã xoá) vào `operation-hub.js`; 143 page `/decision/*` đổi sang `layout: 'default-sidebar'`.
   Chi tiết ở Phase 11 của plan.md.
   (Ghi chú gốc) Hai phân hệ khác nhau: `Ban hành văn bản nội bộ (Quyết định - quy định - quy chế)`
   (tên cũ: Vận hành nội bộ → key `operation`) và `Ban hành văn bản nội bộ` (tên cũ: Quyết định →
   key `decision`).
6. **Quản lý an toàn 5S** tách khỏi ISO thành phân hệ riêng — tách khung trước, chức năng bổ sung sau.
   (16/09 chiều: đổi tên thành **An toàn - 5S**, xem quyết định #9.)
7. **Đánh giá KPI** nằm ở nhóm NHÂN SỰ (bản ở VĂN PHÒNG SỐ bị gạch) — đúng như registry hiện tại.
8. Mục chưa có màn: khai menu **không có `link`** → sidebar render xám mờ (cơ chế sẵn có).
9. **(16/09 chiều) Rút gọn tên 10 phân hệ + gộp tiếp `legal`** — user chốt, KHÁC tên trong sheet:
   Đánh giá KPI→**KPI** · Quản lý sản xuất→**Sản xuất** · Quản lý tài sản→**Tài sản** ·
   Quản lý an toàn 5S→**An toàn - 5S** · Quản lý công việc→**Công việc** ·
   Quản lý bán hàng→**Bán hàng** · Hoạt động ISO (quản lý quy trình)→**ISO** ·
   Tra cứu - thông báo→**Thông báo** · Quản lý CSKH trước khi bán→**CSKH trước bán** ·
   CRM→**CSKH sau bán**; và **Hoạt động pháp lý + Văn bản nội bộ → "Văn bản - Hồ sơ pháp lý"**
   (subtext "Quyết định, quy chế, hồ sơ pháp lý"). Chi tiết ở Phase 12 của plan.md.
   ⚠️ Từ nay tên phân hệ **không còn bám nguyên văn sheet** — sửa `label` trong `subsystems.js` là
   nguồn duy nhất, `doi-chieu-menu.py` vẫn đối chiếu ở mức CHỨC NĂNG nên không ảnh hưởng.

## Scope

- Chỉ đụng `hrm-client`: `components/subsystems.js`, `components/subsystem-menu/*.js`,
  `components/menu.js`, `components/menu-sidebar.js`, `components/default-menu/*.js`.
- Thêm 3 phân hệ: `meeting`, `presale` (CSKH trước bán), `safety-5s`; **bỏ 2 phân hệ: `decision`
  và `legal` (đều gộp vào `operation`)** → registry còn **28 phân hệ**.
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
