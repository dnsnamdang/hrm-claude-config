# Chuyển code màn sang phân hệ mới — Danh mục chung & Bảo hiểm

> Phụ trách: @junfoke · Bắt đầu: 2026-08-04 · Nhánh: `gop_db` · Trạng thái: đã chốt design
> Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-08-04-chuyen-code-phan-he-master-data-insurance-design.md`

## Mục tiêu

Giai đoạn 2 của `tach-phan-he-erp-hrm`: đưa **code** màn về đúng phân hệ, không chỉ menu.
Làm 2 phân hệ nhỏ trước để định hình quy trình chuẩn, sau đó áp cho Bán hàng (30 màn).

## Kết quả khảo sát 2026-08-04

Chỉ 3 phân hệ đang ở trạng thái "menu đã chuyển, code chưa chuyển":

| Phân hệ | Số mục | Route cũ |
|---|---|---|
| Bán hàng (`sale`) | 30 | `/assign/*` — **đợt sau** |
| Danh mục chung (`master-data`) | 10 | `/human/*` (7) + `/assign/*` (3) |
| Bảo hiểm xã hội (`insurance`) | 7 | `/decision/*` (6) + `/regulations/*` (1) |

`finance` + `customer-care` đã có màn thật đúng route. 9 phân hệ còn lại chỉ có mục xám mờ.
BE: `Modules/{Sale,MasterData,Insurance}` vẫn là skeleton rỗng (route 17 dòng, 0 controller).

## Quyết định (user chốt 2026-08-04)

1. **Chuyển cả 3 lớp**: FE route + BE module + dọn quyền.
2. **Danh mục chung làm đủ 10 màn**, gồm cả 3 màn Khách hàng (dù dính quyền ERP + ~10 picker).
3. **URL cũ redirect vĩnh viễn** — khai bảng ánh xạ ở `nuxt.config.js::extendRoutes`.
4. **Giữ nguyên tên đoạn cuối route** cho dễ đối chiếu: `/insurance/insurance`, không đổi tên.
5. **1 feature, 2 giai đoạn**: A = Danh mục chung (A1 địa lý-ngân hàng → A2 đối tác), B = Bảo hiểm.
   Verify sau mỗi bước.
6. **BE chuyển hẳn, không alias** — đã xác minh ngoài `hrm-client` không có consumer nào gọi
   `/api/v1/human/*` hay `/api/v1/decision/*`.

## Quy trình chuẩn 7 bước (tái dùng cho các phân hệ sau)

1. FE pages: `git mv` + đổi `layout: 'subsystem'` + sửa link nội bộ (`$router.push`, `:to`,
   `url-back`, `pathsToKeep`)
2. FE redirect: thêm cặp route cũ → mới ở `extendRoutes` (cụ thể trước, tổng quát sau)
3. FE gọi API: đổi endpoint, **kể cả nơi ngoài màn** (store, component dùng chung, modal)
4. BE move: chuyển file + đổi namespace + khai route mới + xóa route cũ
5. Quyền: migration `UPDATE hrm_permissions SET type/group` giữ nguyên `id` + sửa seeder
6. Menu: sửa `link` trong `subsystem-menu/<slug>.js`
7. Verify: HTTP thật + browser + DB nguyên trạng

## Ranh giới khó nhất — Bảo hiểm ↔ Quyết định

`Modules/Decision` có 4 cụm chứa chữ "Insurance", chỉ 2 cụm chuyển đi:

- **Đi**: `InsuranceType*`, `InsurancePackage*`, `InsuranceRegister/*`, `InsuranceOutCompany/*`,
  `Export/ReportInsuranceRegister`
- **Ở lại**: `Regulation/RegulationInsurance*` (Quy chế chung), `Benefit/BenefitInsurance*`
  (Chế độ phúc lợi) — thuộc phân hệ khác, chỉ *tham chiếu* gói bảo hiểm

→ Decision phụ thuộc Insurance một chiều. Màn "Báo cáo bảo hiểm đã khai báo" tách 2 phương thức ra
controller riêng bên Insurance, không kéo cả `RegulationGeneralController`.

## Quyền — số liệu thật

- Bảo hiểm `type 6 → 11`: id 404-406, 887-891, 897-898, 947-951, 955 (+ phải rà nốt nhóm
  `Bảo hiểm nhân viên` bằng query, menu không gate nên chưa lộ tên)
- Lĩnh vực/nhóm lĩnh vực KH `type 4 → 9`: id 996, 1006, 1093, 1094 — **phải đổi `group` từ
  `Danh mục` sang `Danh mục đối tác`**, vì `Permission.vue` gom nhóm chỉ theo tên `group`
- 7 màn địa lý-ngân hàng **không có permission nào** (ai đăng nhập cũng vào được) — không tự thêm
  trong đợt này, ghi lại để user quyết
- 3 màn Khách hàng dùng quyền ERP → không có gì trong `hrm_permissions` để chuyển
- "Báo cáo BH đã khai báo" gate bằng `Quản lý quyết định` — quyền của phân hệ Quyết định, giữ nguyên

## Rủi ro chính

1. Redirect cụm `/decision/insurance` — vừa là màn vừa là tiền tố của 5 route con, khai sai thứ tự
   là nuốt nhau
2. `pathsToKeep` hardcode route cũ ở 5 chỗ → quên sửa là mất bộ lọc
3. Thông báo cũ trong DB trỏ `/decision/insurance/add` (sinh từ `SelfNotificationForm.vue`)
4. Phụ thuộc chéo module: PHP không báo lỗi tới lúc gọi → `composer dump-autoload` + grep `use`
5. `Tp*` entity trong `Modules/Human` trỏ DB ERP cũ — xác định phạm vi dùng trước khi chuyển kèm
6. Nhánh `gop_db`: code mới không dùng `mysql2`

## Đã làm trước

Bỏ mục "Khách hàng" trùng khỏi `subsystem-menu/sale.js` (bug ghi ở `bo-sung-menu-phan-he/plan.md`,
user chốt giữ ở Danh mục chung).

## Bổ sung 2026-08-06 — Phase 17: CSKH + Tài chính vào chuẩn hub

Chuẩn hub nâng từ 3 lên **5 phân hệ**. Quyết định chính: menu Tài chính có 24 mục cấp 1 (rail
quá dài) nên gom còn **11 nhóm bám thẳng mega-menu `Kế toán` của ERP** — cấu trúc 3 cấp của ERP
trùng khớp cấu trúc hub, mà các màn này vốn chuyển từ đó sang. Cách gom dùng cờ `hubGroup` gắn
trên cây menu sẵn có, **không sinh file hub thứ hai** như `sale-hub.js`. CSKH giữ nguyên 4 nhóm.

Spec đầy đủ: `docs/superpowers/specs/gop-db/2026-08-06-hub-menu-customer-care-finance-design.md`
