# ERP → HRM Migration (Umbrella Roadmap)

> **Trạng thái:** BRAINSTORMING — đang tư vấn phương án. Chưa chốt.
> Đây là feature "ô" (umbrella) tổng hợp chiến lược chuyển 4 mảng ERP TanPhatDev sang HRM:
> Báo giá · Hợp đồng bán hàng (firm) · Hợp đồng dịch vụ · Kế toán.

## Mục tiêu 3 tiêu chí (user yêu cầu)
- **Nhanh** — sớm có giá trị sử dụng, không big-bang kéo dài.
- **An toàn** — không phá vỡ nghiệp vụ đang chạy, rollback được.
- **Bảo toàn dữ liệu tối đa** — dữ liệu lịch sử báo giá/HĐ/kế toán không mất, không sai lệch.

## Quy mô nguồn (ERP TanPhatDev) — áng chừng
| Mảng | Controller | Bảng DB | View Blade |
|------|-----------|---------|-----------|
| Báo giá | ~7 | ~30 | ~66 |
| HĐ bán / Firm | ~18 | ~60 | ~90 |
| HĐ dịch vụ | ~12 | ~30 | ~30 |
| Kế toán | ~30 | ~45 | ~99 |
| **Tổng** | **~65** | **~165** | **~285** |

## Hiện trạng HRM (đích) — đã làm tới đâu
- **Báo giá:** ĐANG CHẠY MẠNH trong `Modules/Assign` — nhiều feature đã CODE DONE
  (Quotation ĐVT, BOM, print config, prospective-projects, dự án cha-con...). Entity `Quotation*`, `Tp*` đã có.
- **HĐ bán / HĐ dịch vụ:** đã có entity nền (`TpFirmContract`, `TpWrServiceContract`, `SettlementContract*`) — độ phủ nghiệp vụ CHƯA rõ, cần khảo sát sâu.
- **Kế toán:** MỚI Ở KHUNG — chỉ có báo cáo Sổ NKC (đọc) + demo HTML tĩnh 14 nhóm màn (`demo-man-hinh-ke-toan`). Chưa có bảng/bút toán/chứng từ. Có merge conflict chưa resolve ở `Modules/Accounting/Routes/api.php`.
- **Dữ liệu:** HRM đã bridge sang dữ liệu ERP (endpoint `erp-product-units`, entity `Tp*`) — pattern bảo toàn dữ liệu đang dùng = đọc/mirror dữ liệu ERP, không ETL cứng.

## Bối cảnh tầng dữ liệu (đã xác minh 2026-07-27)
- HRM nối ERP qua nhiều connection phụ: `mysql2` (=DB_*_SECOND, DB ERP chính), `mysql_tpe`, `mysql_etek_green/power/etek`.
- Model `Tp*` trỏ ERP: `TpFirmContract→mysql2.firm_contracts`, `TpWrServiceContract→mysql2.wr_service_contracts`, `TpProduct→mysql2.products`; 28 model dùng `mysql_tpe`.
- HRM có bảng native CÙNG TÊN: `customers`, `quotations` (connection mặc định) → trùng tên với ERP.

## Quyết định đã chốt
- **[CHỐT 2026-07-27] Chỉ gộp DB của 1 pháp nhân**: HRM (`mysql`) ⊕ ERP (`mysql2`) → 1 database.
  Các connection theo pháp nhân (`mysql_etek_green/power/etek`, và `mysql_tpe`?) dùng cho mục đích riêng → KHÔNG gộp, sẽ **bỏ các kết nối đó**. ⇒ loại bỏ rủi ro trùng khoá chính giữa các pháp nhân.

## Quyết định đã chốt (tiếp)
- **[CHỐT 2026-07-27] ERP repoint sang DB HRM** — mục tiêu cuối: ERP + HRM dùng chung 1 database.
- **[CHỐT 2026-07-27] Đích = 🅑 MỘT SCHEMA DUY NHẤT** (không chọn "2 schema/1 server"). Phải gộp thật, gồm cả 50 bảng trùng tên.

## Dữ liệu va chạm (đối chiếu migration offline, 2026-07-27)
- ERP: **1.225 bảng** · HRM: **635 bảng** · **trùng tên: 50 bảng** (xem `collisions-50-tables.txt`).
- 3 nhóm va chạm: (a) Khung/Auth Laravel (`users`, `jobs`, `failed_jobs`, `password_resets`) — 2 hệ auth khác nhau, chỉ tồn tại trong giai đoạn coexist, ERP retire là drop; (b) Master/tổ chức (`companies`, `departments`, `customers`…) — nhiều khả năng CÙNG thực thể nhân đôi → cần merge/dedupe; (c) Nghiệp vụ (`quotations`, `settlement_contracts`…).

## Đường đi an toàn tới 🅑 (2 phase — chờ xác nhận + khảo sát Phase 2)
- **Phase 1 — Colocate + prefix legacy:** đưa toàn bộ bảng ERP vào schema HRM; 50 bảng trùng của ERP đổi tiền tố `tp_` (HRM giữ tên canonical), repoint app ERP dùng bảng `tp_*` + gỡ connection phân tán. ⇒ ĐÃ đạt "1 database chung", dữ liệu nguyên vẹn 100%, rủi ro thấp.
- **Phase 2 — Hợp nhất thực thể dần theo domain:** khử trùng lặp `tp_customers`→`customers`… gắn với việc viết lại UI + retire ERP từng mảng. Phần rủi ro, chia nhỏ, reversible.

## Kết quả phân loại 50 bảng (script offline, 2026-07-27 — xem `phase2-risk-map.md`)
- 44 cùng thực thể / 3 trùng một phần / 3 va chạm giả → **HRM là bản fork/re-model một phần của ERP**.
- Xếp theo VAI TRÒ: T0 Khung/Auth (không merge) · T1 va chạm giả (rename) · T2 danh mục (dedupe) · T3 lõi tổ chức (rủi ro cao) · T4 nghiệp vụ KH/HĐ.
- `quotations` = va chạm GIẢ (HRM đã re-model, 11/55 cột chung) → chỉ rename ERP, không merge.
- **~Phần lớn 165 bảng của 4 mảng KHÔNG trùng tên** → bê sang giữ nguyên tên, không va chạm.

## Quyết định đã chốt (tiếp)
- **[CHỐT 2026-07-27] T3 (lõi tổ chức) đã ĐỒNG BỘ sẵn giữa ERP↔HRM** — cùng thực thể thật, đã đối soát. ⇒ merge T3 = "retire bản copy ERP", dùng tương ứng sync sẵn có để remap id. Gộp 1 DB → **gỡ bỏ toàn bộ sync (chính là hệ phân tán cần xoá)**.
- **[CHỐT 2026-07-27] Prefix legacy phía ERP (`tp_`)** — HRM là hệ sống tiếp, giữ tên bảng chuẩn.

## Kiến trúc đích + lộ trình (chờ user duyệt)
- **End-state:** 1 schema HRM duy nhất; HRM = canonical; ERP retire dần; hết connection phân tán; hết sync.
- **Phase 1 — Hợp nhất hạ tầng (nhanh, an toàn, ĐẠT "1 DB chung"):** colocate toàn bộ bảng ERP vào schema HRM; 50 bảng trùng → `tp_` + reconfigure app ERP; gỡ connection phân tán; giữ sync T3 tạm (nội bộ 1 DB) tới khi domain retire. Dữ liệu nguyên vẹn 100%.
- **Phase 2 — Hợp nhất + viết lại UI theo domain (master → báo giá → HĐ → kế toán):** mỗi domain: viết lại UI HRM đọc bảng ERP đã bê sang → remap FK T3 (company/employee) ERP→HRM qua tương ứng sync → retire màn ERP → dedupe/drop `tp_` dup. T2 danh mục dedupe sớm; T0 framework drop khi ERP retire hẳn.

## Quyết định còn treo
- [ ] Sync T3 có giữ NGUYÊN id 2 bên hay map qua natural key? (quyết remap có cần bảng ánh xạ) — xác minh ở Phase 1 spec.
- [ ] (Tầng UI) Biến thể nào còn dùng (thường/firm/zt-ztec/project/inland)? Thứ tự ưu tiên trong 4 mảng.

## Link chi tiết
- Spec đầy đủ: `docs/superpowers/specs/2026-07-27-erp-to-hrm-migration-design.md` (sẽ fill sau brainstorming)
- Các feature con đã/đang làm: xem `.plans/STATUS.md` (Bomlist-Quotation, du-an-cha-con, demo-man-hinh-ke-toan, quotation-*...).
