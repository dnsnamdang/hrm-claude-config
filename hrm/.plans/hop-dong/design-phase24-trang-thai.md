# Phase 24 — Bộ trạng thái Hợp đồng bán mới

> Brainstorm 30/10 – 02/11/2026. Khảo sát hiện trạng: `plan.md` mục Phase 24.

## Nguyên tắc (user chốt 02/11)
- MỌI trạng thái do **code tự chuyển** khi một điều kiện / nghiệp vụ hoàn thành. Không có chỗ cho user tự chọn trạng thái.
- Bước 1: **khai báo đủ bộ 16 trạng thái** (mã + tên + màu). Sau đó làm dần từng trạng thái: chốt sự kiện kích hoạt → code.
- Thanh lý **giữ** làm trạng thái thứ 16 (mã 10). Sự kiện kích hoạt: chốt sau. Nút bấm tự do hiện tại trái nguyên tắc, sẽ đổi khi làm tới.

## Bảng mã — ĐÃ CHỐT 02/11
Giữ nguyên mã cho trạng thái trùng nghĩa, vì code ngoài module đang đọc mã cứng (thu tiền 6/10/11/12, QR bản in 6/11/12, picker YCXH 6, hàng bán trả lại 11/12). Trạng thái mới cấp mã 13–22.

| # | Trạng thái | Mã | Nguồn | Sự kiện kích hoạt |
|---|---|---|---|---|
| 1 | Đang tạo | 3 | giữ | tạo HĐ (đã có) |
| 2 | Không duyệt | 13 | mới | người duyệt bấm Không duyệt (hiện đang trả về 3) |
| 3 | Chờ TP duyệt | 2 | đổi tên "Chờ duyệt" | gửi duyệt (đã có) |
| 4 | Chờ pháp chế duyệt | 14 | mới | chốt sau |
| 5 | Chờ BGĐ duyệt | 15 | mới | chốt sau |
| 6 | Chờ KH ký | 16 | mới | duyệt xong (hiện đang nhảy thẳng 6) |
| 7 | KH đã ký | 17 | mới | popup xác nhận: file + ngày ký |
| 8 | Có hiệu lực | 6 | giữ | tới ngày hiệu lực (lệnh lịch) |
| 9 | Đóng | 18 | mới | chốt sau (chỉ từ Chờ KH ký) |
| 10 | Đang thực hiện | 19 | mới | chốt sau |
| 11 | Hết hiệu lực | 20 | mới | quá thời hạn thực hiện (lệnh lịch) |
| 12 | Gia hạn chờ duyệt | 21 | mới | chốt sau |
| 13 | Chờ quyết toán | 22 | mới | chốt sau |
| 14 | Đang quyết toán | 12 | giữ | chốt sau |
| 15 | Đã quyết toán | 11 | giữ | chốt sau |
| 16 | Đã thanh lý | 10 | giữ | chốt sau |

Mã cũ không còn trong bộ mới: 1 Đã duyệt · 7 Chờ hiệu lực · 8 Đang xuất hàng · 9 Đã xuất hàng → bỏ khỏi danh sách hiển thị / bộ lọc, giữ hằng số (đánh dấu ngưng dùng) để không vỡ `BillIncomeRequestService`, `ContractPrintService`. Không có dữ liệu cần chuyển (local chỉ HĐ test; prod chưa có HĐ HRM).

## Phạm vi code bước 1 (khai báo)
- hrm-api `Modules/Assign/Entities/Contract/Contract.php`: hằng số 13–22 + `getStatusList()` đủ 16 (màu theo bảng chuẩn list-page 3c-2).
- hrm-client `pages/assign/contracts/index.vue`: bộ lọc trạng thái đủ 16.
- Không migration (cột `status` là số), không đổi luồng chuyển trạng thái.

## Bước 1 — Mẫu in ⇒ Pháp chế duyệt (brainstorm 02/11)
Hiện trạng: lập HĐ chọn mẫu HĐ (`print_template_id`), nội dung chép vào `hrm_contracts.template`, sửa tự do bằng editor; phụ lục hàng hoá chỉ lưu nội dung `template_print_product` (FE tự điền từ mẫu đầu tiên sub_type `sale_contract_product_annex`, không lưu id mẫu). Chưa có logic so/đánh dấu "đã sửa mẫu".
- [x] Q1 (02/11): **Sửa lời văn mẫu in (khác mẫu gốc) ⇒ bắt buộc qua Chờ pháp chế duyệt; giữ nguyên ⇒ bỏ qua bước pháp chế.**
- [x] Q2 (02/11): chỉ xét **lời văn HĐ** (`template`); phụ lục hàng hoá không tính.
- [x] Q3 (02/11) — cơ chế do user chốt (thay cho "so tự động quyết định"):
  - Chọn mẫu ⇒ tab "Mẫu in" hiện mẫu **chỉ xem**. Có nút **Sửa**.
  - Bấm Sửa ⇒ hộp xác nhận: "Chọn sửa mẫu in thì hợp đồng này cần gửi duyệt qua Pháp chế. Bạn chắc chắn cần sửa?" ⇒ Đồng ý: **lưu cờ cần pháp chế duyệt** + mở editor sửa như hiện tại.
  - **Cờ quyết định bước pháp chế**, không phải kết quả so. So chữ chỉ để **đánh dấu cho Pháp chế thấy chỗ khác mẫu**, duyệt nhanh hơn.
  - Kết quả thử 02/11 (HĐ 94 vs mẫu 65): HTML thô khác (editor định dạng lại, mẫu gốc NFD ↔ HĐ NFC, nbsp); sau chuẩn hoá NFC + nbsp + khoảng trắng ⇒ chữ giống hệt. ⇒ phần đánh dấu khác biệt phải so CHỮ đã chuẩn hoá, không so HTML thô.
- [x] Q4 (02/11): gỡ cờ bằng nút **"Khôi phục mẫu gốc"** (nội dung về đúng mẫu gốc, khoá lại chỉ xem, gỡ cờ); chọn mẫu khác cũng gỡ cờ. Chỉ khi HĐ Đang tạo / Không duyệt.
- [x] Q5 (02/11): "mẫu gốc" = **bản chụp nội dung mẫu lúc chọn**, lưu kèm HĐ (cột mới, migration). Khôi phục + so khác biệt đều dùng bản chụp này.
- [x] Q6 (02/11): nút **"Xem thay đổi"** ở tab Mẫu in, chỉ hiện khi cờ pháp chế bật; chữ thêm tô xanh, chữ xoá đỏ gạch ngang + số chỗ thay đổi; ai xem được HĐ đều xem được.

### Thiết kế bước 1 — ĐÃ CODE 02/11 (plan.md 24.2)
Tự chốt (theo khuôn, không cần hỏi): nút Sửa / Khôi phục chỉ có khi HĐ sửa được (Đang tạo, sau này cả Không duyệt); phụ lục hàng hoá giữ như hiện tại (sửa tự do, không tính); HĐ cũ: cờ = 0, không có bản chụp ⇒ ẩn "Xem thay đổi".

**DB** — migration `hrm_contracts`: `need_legal_approval` tinyint default 0 · `template_original` longText null (bản chụp mẫu lúc chọn).

**BE**
- Store/Update nhận `need_legal_approval`, `template_original`. BE là nguồn quyết định: cờ = 0 ⇒ ghi `template = template_original` (bỏ qua nội dung FE gửi) ⇒ không lách được bằng gọi API. Đổi `print_template_id` ⇒ chụp lại `template_original` từ `hrm_print_templates` (đọc ở BE, không tin FE) + cờ về 0 trừ khi FE gửi cờ 1 kèm nội dung.
- Lịch sử: ghi "Sửa mẫu in (cần pháp chế duyệt)" / "Khôi phục mẫu gốc".
- `POST assign/contracts/template-diff` body {original, current} (chỉ cần đăng nhập, không đọc DB ⇒ dùng được cả lúc chưa lưu): so CHỮ đã chuẩn hoá (strip thẻ, NFC, nbsp, gộp khoảng trắng) theo TỪ — cắt phần đầu/cuối trùng rồi LCS phần giữa; trả các đoạn {same|add|del} + số chỗ thay đổi. Tự viết (repo chưa có thư viện diff).
- Resource trả `need_legal_approval`.

**FE `_id/edit.vue` tab Mẫu in (con "Mẫu in hợp đồng")**
- Chọn mẫu ⇒ nạp nội dung + bản chụp; hiện **chỉ xem** (v-html).
- Nút **Sửa** ⇒ `$confirm` "Chọn sửa mẫu in thì hợp đồng này cần gửi duyệt qua Pháp chế. Bạn chắc chắn cần sửa?" ⇒ Đồng ý: cờ = 1, mở `CompactReviewEditor`.
- Khi cờ = 1: nhãn "Cần pháp chế duyệt" + nút **Khôi phục mẫu gốc** (confirm ⇒ nội dung = bản chụp, cờ = 0, chỉ xem) + nút **Xem thay đổi** (popup tô xanh/đỏ gạch, số chỗ thay đổi; gửi nội dung đang sửa + bản chụp lên endpoint POST ⇒ xem được cả khi chưa lưu).
- Màn Chi tiết: nhãn cờ + nút Xem thay đổi.
- Đổi mẫu khi cờ = 1 ⇒ confirm như hiện tại, cờ về 0.

**Chưa thuộc bước 1**: dùng cờ để rẽ sang "Chờ pháp chế duyệt" — làm ở bước 2 (luồng duyệt).

## Bước 2 — Duyệt từng bước tới Có hiệu lực (brainstorm 03/11, theo rbac sau merge 24.3)
Hiện trạng (đọc code 03/11): `sale.hop_dong_du_an_tkt.approve` "Duyệt hợp đồng dự án TKT" `scopes => []`; Catalog CHƯA có quyền duyệt nào có phạm vi. Phạm vi rbac: 1 Bộ phận < 2 Phòng < 3 Công ty < 4 Tổng công ty (số lớn bao số nhỏ); phạm vi Phòng ở màn danh sách = `department_id ∈ listManageDepartmentIds()` (phòng được giao QUẢN LÝ — `employee_manage_departments`, cờ quản lý tất cả ⇒ mọi phòng công ty).
- [x] Q1 (03/11): bước **Chờ TP duyệt** do người có quyền **"Duyệt hợp đồng bán hàng"** phạm vi **Phòng** duyệt.
- [x] Q2 (03/11): phạm vi Phòng = HĐ có `department_id` ∈ phòng người duyệt **được giao quản lý** (`listManageDepartmentIds`, khớp màn danh sách).
- [x] Q3 (03/11): quyền "Duyệt hợp đồng bán hàng" có 2 phạm vi: **Phòng** (bước Chờ TP duyệt) và **Công ty** (dùng cho bước **Chờ BGĐ duyệt** — làm sau). Không có Bộ phận / Tổng công ty.
  Lưu ý khi làm bước BGĐ: đang có `sale.hop_dong_vuot_han_muc.approve` "Duyệt hợp đồng vượt hạn mức" (BGĐ duyệt khi doanh số vượt trội quá hạn mức) — chồng ý với phạm vi Công ty, phải chốt gộp hay giữ.
- [x] Q4 (03/11): **mỗi bước đúng mức** — Chờ TP duyệt CHỈ người có phạm vi **đúng bằng** Phòng (quản lý phòng của HĐ); Chờ BGĐ duyệt CHỈ phạm vi Công ty. Phạm vi Công ty KHÔNG duyệt thay bước TP (khác luật chung rbac "lớn bao nhỏ" ⇒ code kiểm `scope === DEPARTMENT`, không `>=`). Phòng thiếu người quản lý ⇒ HĐ kẹt ở bước TP (chấp nhận).
- [x] Q5 (03/11): người có phạm vi Công ty (kể cả khi kiêm quản lý phòng của HĐ) **chỉ duyệt bước BGĐ**, không duyệt bước TP.
  **Nguyên tắc user chốt 03/11: "cấp cao bao gồm cấp con chỉ áp dụng cho quyền Xem"** ⇒ quyền duyệt có phạm vi kiểm ĐÚNG BẰNG.
  ⚠️ rbac lấy `MAX(rhp.scope)` giữa các vai trò (`PermissionChecker.php:266`) và `has($code, $minScope)` so `>=` ⇒ với quyền duyệt phải viết kiểm riêng `CurrentPermission::scope($code) === PermissionScope::DEPARTMENT`; người có 2 vai trò Phòng + Công ty sẽ bị tính là Công ty. Catalog hiện CHƯA có quyền duyệt nào có phạm vi (HĐ bán là quyền đầu tiên) — nên báo nhóm rbac để có hàm kiểm chung.
- [x] Q6 (03/11): thứ tự **TP → Pháp chế (nếu cờ sửa mẫu in) → BGĐ (nếu đủ điều kiện) → Chờ KH ký**; bước không đủ điều kiện tự bỏ qua.
- [x] Q7 (03/11): bước Chờ pháp chế duyệt — **quyền MỚI "Pháp chế duyệt hợp đồng bán hàng", phạm vi Công ty** (duyệt HĐ của công ty mình), gán qua Vai trò.
- [x] **Q8 (03/11) — THAY Q1/Q3/Q4/Q5/Q7:** user: "Bỏ logic Phạm vi cho các quyền loại Duyệt ⇒ tách rõ các quyền ra". Quyền Duyệt KHÔNG có phạm vi, mỗi bước 1 quyền (khuôn ERP `sale.hop_dong.approve` + `sale.hop_dong_ban_giam_doc.approve`, R6):
  | Bước | Mã | Tên |
  |---|---|---|
  | Chờ TP duyệt | `sale.hop_dong_du_an_tkt.approve` (giữ mã, đổi tên; alias api "Duyệt hợp đồng" giữ) | Trưởng phòng duyệt hợp đồng bán hàng |
  | Chờ pháp chế duyệt | `sale.hop_dong_du_an_tkt_phap_che.approve` (MỚI) | Pháp chế duyệt hợp đồng bán hàng |
  | Chờ BGĐ duyệt | `sale.hop_dong_du_an_tkt_ban_giam_doc.approve` (MỚI) | Ban giám đốc duyệt hợp đồng bán hàng |
  Tất cả kind approve, scopes [], platforms [hrm]; giới hạn công ty = quyền gắn trên Vai trò theo công ty. Q2 (phòng được giao quản lý), Q6 (thứ tự) còn hiệu lực — Q2 cần xác nhận lại là điều kiện dữ liệu kèm quyền TP.
- [x] Q9 (03/11): "Trưởng phòng duyệt hợp đồng bán hàng" duyệt HĐ có `department_id` ∈ phòng người duyệt **được giao quản lý** (`listManageDepartmentIds`) — điều kiện dữ liệu kèm quyền, không phải phạm vi. Pháp chế / BGĐ: mọi HĐ của công ty đang làm việc.
- **Khảo sát 03/11 — code cũ chuyển BGĐ khi nào** (đọc code ERP `TanPhatDev` nhánh gop_db + hrm-api worktree):
  - ① **Vượt hạn mức DS vượt trội** — `departments.max_extra_price_percent` (phòng người lập). ERP `ContractService::overMaxExtraPricePercent` (HĐ cũ) / `FirmContractService::overMaxExtraPricePercent` (HĐ firm): % = vượt trội / tổng trước VAT > hạn mức ⇒ chặn "Vui lòng chuyển duyệt BGD", trừ người có `sale.hop_dong_vuot_han_muc.approve`. HRM đã port y hệt: `ContractService::assertExtraWithinLimitOrBgd` (chặn lúc duyệt, KHÔNG tự đổi trạng thái). Hạn mức trống/0 ⇒ không giới hạn.
  - ② **Quy chế phòng có cờ "Chuyển duyệt BGĐ"** (`regulations.change_approver`, khai ở màn Phòng ban ERP) — chỉ HĐ firm, ở màn Hạch toán hỗ trợ: quy chế khớp theo % chiết khấu so giá net (`getMatchRegulation`); quy chế khớp có cờ ⇒ ẩn nút Duyệt, BE chặn (`requiresBgdEscalation`) trừ Giám đốc/Ban Giám đốc THẬT (`approverIsRealBigBoss`, theo vai trò).
  - ③ **Bán dưới giá net có chi phí thị trường** (`switch_approve` FE: `total_market_costs != 0 && discount_rate_before_vat < 0`) — cùng chốt chặn ②.
  - Cách "chuyển": KHÔNG có trạng thái riêng; TP bấm **Chuyển duyệt** chọn người (`approver_id`), HĐ vẫn Chờ duyệt.
  - ~~HRM chưa có HTHT / quy chế~~ — **SAI, đính chính 03/11** (grep sót vì lọc nhầm): HRM ĐÃ port
    - HTHT: `ContractSupportAccountingService` (port FirmSupportAccountingService; `getRegulations`/`getMatchRegulation` đọc chung bảng `regulations` ERP; `discount_rate_before_vat` tính sẵn; `total_market_costs` = Thưởng NVKD `sales_bonus`), màn `pages/assign/contracts/_id/support-accounting.vue` — nút Duyệt ở đây gọi `approve` (ghi HTHT + CHO_DUYET→CO_HIEU_LUC).
    - Quy chế: màn Khai Quy chế – Cấu hình (`RegulationConfigScreen.vue`, tab Hoa hồng) có ô "Chuyển duyệt Ban giám đốc" ghi `regulations.change_approver`.
    - Hiện HRM **chưa dùng** `change_approver` / điều kiện ③ ở luồng duyệt — chỉ có ①.
    - Dữ liệu (tinker, DB local hrm_erp_21_10_prod): regulations Department 472 bản (194 bật cờ), Part 25 (12 bật cờ); phòng có `max_extra_price_percent` > 0: 1.
  - ⇒ Cả ①②③ làm được ngay ở HRM.
- [x] Q11 (03/11): người BGĐ (danh sách chọn khi Chuyển duyệt + người được duyệt) cho cả ①②③ xét **quyền "Ban giám đốc duyệt hợp đồng bán hàng"** (`sale.hop_dong_du_an_tkt_ban_giam_doc.approve`); `sale.hop_dong_vuot_han_muc.approve` nhập vào quyền này (người đang giữ phải được gán quyền mới). KHÔNG xét theo tên vai trò như ERP ②③.
- [x] Q12 (03/11): TP bấm Chuyển duyệt + chọn 1 người (có quyền BGĐ) ⇒ HĐ sang **Chờ BGĐ duyệt (15)**; **chỉ người được chọn** duyệt (lưu như `approver_id` ERP; người đó mất quyền thì không duyệt được).
- [x] Q13 (03/11): HĐ vừa cần Pháp chế vừa dính điều kiện BGĐ ⇒ **TP duyệt bình thường → Chờ pháp chế duyệt → Pháp chế bị chặn, bấm Chuyển duyệt chọn BGĐ → Chờ BGĐ duyệt**. Tức người bị chặn + phải Chuyển duyệt là **bước duyệt cuối trước BGĐ**: có Pháp chế ⇒ Pháp chế; không ⇒ TP. Không dính điều kiện BGĐ ⇒ bước cuối duyệt xong sang Chờ KH ký.
- [x] Q14 (03/11): "Không duyệt" ở bước bất kỳ (TP / Pháp chế / BGĐ, bắt buộc lý do) ⇒ HĐ sang **Không duyệt (13)**; người lập sửa được như Đang tạo, Gửi duyệt lại ⇒ chạy lại từ Chờ TP duyệt; Pháp chế / BGĐ xét lại theo điều kiện mới (người BGĐ đã chọn bị xoá).
- [x] Q15 (03/11): KH đã ký (17) → **Có hiệu lực (6) khi đủ điều kiện hiệu lực + tới ngày** — dựa `recomputeEffectiveDates` có sẵn (`effective_condition`: 1 ngày ký · 2 ngày đặt cọc lần đầu `firstDepositDate` · 3 `guarantee_approved_date`). Kiểm ở 3 chỗ: lúc xác nhận KH đã ký, lúc ghi cọc/duyệt bảo lãnh, và lệnh lịch hằng ngày (ngày hiệu lực ≤ hôm nay). Chưa đủ ⇒ đứng ở KH đã ký.
- [x] Q16 (03/11): "Xác nhận KH đã ký" (popup file HĐ đã ký + ngày ký, HĐ đang Chờ KH ký) — **chỉ người lập HĐ** (`created_by`), không thêm quyền mới.
- [x] Q17 (03/11): Gửi duyệt (từ Đang tạo / Không duyệt) — **chỉ người lập HĐ**, chặn ở API (hiện API không kiểm).
- [x] Q10 (03/11): điều kiện qua BGĐ — **giữ đúng logic cũ ERP** (①②③ như khảo sát trên). Cơ chế chuyển: **như ERP** — dính điều kiện thì chặn nút Duyệt của TP, báo "Vui lòng chuyển duyệt BGD"; TP bấm **Chuyển duyệt** chọn người duyệt. Còn hỏi: ②③ phụ thuộc Hạch toán hỗ trợ chưa có ở HRM; ai được chọn khi chuyển; trạng thái sau khi chuyển.

### Chốt bước 2 — luồng duyệt tới Có hiệu lực (tổng hợp Q1–Q17, 03/11)

```
Đang tạo(3) / Không duyệt(13) ──Gửi duyệt [người lập]──▶ Chờ TP duyệt(2)
Chờ TP duyệt ──TP duyệt──▶ (cờ need_legal_approval) Chờ pháp chế duyệt(14)
                         └▶ (không cờ) [nếu dính ĐK BGĐ: CHẶN Duyệt, TP bấm Chuyển duyệt chọn người BGĐ ▶ Chờ BGĐ duyệt(15)]
                                       [không dính] ▶ Chờ KH ký(16)
Chờ pháp chế ──Pháp chế duyệt──▶ [dính ĐK BGĐ: CHẶN, Pháp chế Chuyển duyệt ▶ Chờ BGĐ(15)] / [không] ▶ Chờ KH ký(16)
Chờ BGĐ ──người BGĐ ĐƯỢC CHỌN duyệt──▶ Chờ KH ký(16)
Mọi bước chờ duyệt ──Không duyệt (lý do)──▶ Không duyệt(13) (xoá người BGĐ đã chọn)
Chờ KH ký ──Xác nhận KH đã ký [người lập; file + ngày ký]──▶ KH đã ký(17)
KH đã ký ──đủ điều kiện hiệu lực & effective_date ≤ hôm nay──▶ Có hiệu lực(6)
   (kiểm lúc xác nhận ký · lúc ghi cọc / duyệt bảo lãnh · lệnh lịch hằng ngày)
```

| Bước | Quyền | Điều kiện dữ liệu |
|---|---|---|
| Gửi duyệt / Xác nhận KH đã ký | — | chỉ `created_by` |
| TP duyệt | `sale.hop_dong_du_an_tkt.approve` (đổi tên "Trưởng phòng duyệt hợp đồng bán hàng") | `department_id` ∈ phòng được giao quản lý |
| Pháp chế duyệt | `sale.hop_dong_du_an_tkt_phap_che.approve` (MỚI) | HĐ công ty đang làm |
| BGĐ duyệt + danh sách chọn khi Chuyển duyệt | `sale.hop_dong_du_an_tkt_ban_giam_doc.approve` (MỚI) | chỉ người được chọn; còn giữ quyền |

**ĐK BGĐ (y ERP):** ① DS vượt trội / tổng trước VAT > `departments.max_extra_price_percent` · ② quy chế khớp của phòng chính (HTHT) có `change_approver` · ③ `total_market_costs != 0 && discount_rate_before_vat < 0`. HRM thôi dùng `sale.hop_dong_vuot_han_muc.approve` (mã giữ cho ERP ⇒ platforms còn `['erp']`).

**Còn ngoài bước 2:** Hết hiệu lực (lệnh lịch, quá `execution_end_date`), Đóng, Đang thực hiện, Gia hạn, quyết toán, thanh lý — chốt sau.
**Lưu ý:** HTHT hiện nhập + ghi ngay lúc TP duyệt (`approve` gọi `calculate`) — ĐK ②③ tính từ HTHT tại bước TP; ở bước Pháp chế dùng HTHT đã lưu.

**Ghi chú khi code (03/11, 24.4):**
- Người duyệt bước cuối trước BGĐ mà CÓ quyền BGĐ ⇒ được Duyệt thẳng sang Chờ KH ký (y ERP: có `sale.hop_dong_vuot_han_muc.approve` / là Giám đốc thì không bị chặn).
- Chuyển duyệt BGĐ không bắt buộc đang dính ĐK (ERP cho chuyển tự do); dính ĐK thì là đường duy nhất. Bước TP chuyển ở màn HTHT (ghi HTHT như Duyệt), bước Pháp chế chuyển ở màn Chi tiết.
- ĐK ②③ ở bước TP lấy theo HTHT đang xem (API preview trả `bgd_reasons`), lúc Duyệt BE xét lại trên HTHT vừa ghi trong cùng transaction; bước Pháp chế xét theo HTHT đã lưu.
- Gửi duyệt lại sau Không duyệt xoá dấu duyệt vòng trước (TP / Pháp chế / BGĐ đã chọn).
- Chưa làm: thông báo người duyệt bước kế; nút "Hủy duyệt" ở Chờ KH ký (khảo sát 30/10 có nêu, chưa chốt); hộp "chờ tôi duyệt" cho Pháp chế / BGĐ không có quyền xem danh sách.

## Bước 3 — Luồng xuất hàng (brainstorm 03/11)

**Khảo sát code (worktree, đọc code — chưa chạy dữ liệu):** luồng YCXH 21 (hàng cha) / 20 (hàng con) → ĐNXK → PXK → PXH đã dựng (Phase 22/23 + hồ sơ `gop-db/hop-dong-xuat-hang`), chưa chạy dữ liệu thật trên prod. Chỗ gắn cứng trạng thái HĐ cần sửa theo bộ 16 trạng thái:
- `Contract::getCanExportAttribute` — chỉ `Có hiệu lực (6)` + ngày hiệu lực + thời hạn thực hiện ⇒ nút YCXH ở Danh sách / Chi tiết, `storeExportRequest`.
- `ProductExportRequestPickerService` (picker HĐ ở màn Tạo YCXH) — `c.status = 6`.
- `DeliveryRequestService::HRM_CONTRACT_ACTIVE = 6` (Yêu cầu giao hàng chọn HĐ).
- `BillIncomeRequestService::HRM_CONTRACT_SELECTABLE_STATUSES` = {6, 8, 9, 10, 11, 12} (thu tiền) — có 8/9 đã ngưng dùng, thiếu 19 Đang thực hiện / 17 KH đã ký…
- `ContractPrintService::QR_STATUSES` = {6, 8, 12, 11} (in QR).
- Chưa nơi nào chuyển HĐ sang **Đang thực hiện (19)**; còn tồn từ 29/10: điều kiện "hàng hoá chưa xuất hết" (SL trên YCXH chưa huỷ hay SL đã xuất thật).
- [x] B3-Q1 (03/11): HĐ Có hiệu lực → **Đang thực hiện (19)** khi **Phiếu xuất kho đầu tiên** của HĐ hoàn tất (hàng thật rời kho).
- [x] B3-Q2 (03/11): bước 3 CHỈ mốc xuất hàng; thu tiền / hạch toán DV / chi phí gắn sau qua 1 hàm chung (`markInProgress`).
- [x] B3-Q3 (03/11): được lập YCXH khi HĐ **Có hiệu lực (6) hoặc Đang thực hiện (19)** (+ giữ: có ngày hiệu lực, thời hạn thực hiện, người lập). Hết hiệu lực / Gia hạn chờ duyệt / quyết toán / thanh lý ⇒ chặn. Không chặn thêm theo ngày kết thúc thực hiện.
- [x] B3-Q4 (03/11): "còn hàng chưa xuất" = SL HĐ − SL trên **YCXH chưa huỷ** (giữ cách picker đang tính); nút YCXH ẩn khi mọi dòng đã được yêu cầu đủ.
- [x] B3-Q5 (03/11): thu tiền chọn được HĐ **từ KH đã ký trở đi** (17, 6, 19, 20, 21, 22, 12, 11, 10) — để thu cọc khi điều kiện hiệu lực = ngày đặt cọc; bỏ mã 8/9 ngưng dùng.

### Chốt bước 3 — đề xuất code (03/11)
- **Có hiệu lực → Đang thực hiện:** `ContractService::markInProgress(Contract)` (6 → 19, lịch sử `in_progress`, idempotent; hàm chung để sau gắn thu tiền / hạch toán DV / CP).
  - Gọi tại `WarehouseExportService::send()` (PXK "Gửi" = hàng rời kho) khi YCXH có `emplement_contract_type = Contract::class`.
  - PXK có thể làm trên **ERP** (máy trạng thái xen kẽ ERP↔HRM, ERP `WarehouseExport::send()` không gọi HRM) ⇒ lệnh lịch hằng ngày quét bù: HĐ 6 có YCXH 20/21 ở trạng thái đã xuất kho trở đi ⇒ 19. Gộp vào `assign:activate-signed-contracts` (đổi tên mô tả) hoặc lệnh riêng.
- **Được lập YCXH:** `can_export` = status ∈ {6, 19} + có ngày hiệu lực + thời hạn thực hiện; `is_can_create_export_request` thêm "còn dòng chưa được yêu cầu đủ" (SL HĐ − SL YCXH chưa huỷ, cùng công thức picker). Picker `hrm-contracts` ∈ {6, 19}.
- **Giao hàng** (`DeliveryRequestService`, chọn HĐ HRM): {6, 19} — cùng điều kiện xuất.
- **Thu tiền** (`BillIncomeRequestService::HRM_CONTRACT_SELECTABLE_STATUSES`): {17, 6, 19, 20, 21, 22, 12, 11, 10}.
- **In QR** (`ContractPrintService::QR_STATUSES`, ERP: Có hiệu lực · Đang xuất hàng · Đang/Đã quyết toán): {6, 19, 22, 12, 11}.

## Hết hiệu lực (20) — CHỐT 05/11/2026
- [x] HHL-Q1: nguồn = **Có hiệu lực (6) VÀ Đang thực hiện (19)**. HĐ đang xuất dở quá hạn cũng chuyển ⇒ không lập YCXH mới được (chờ feature Gia hạn).
- [x] HHL-Q2: mốc = **quá** `execution_end_date` — ngày kết thúc vẫn còn hiệu lực trọn ngày; lệnh 00:20 hôm SAU mới chuyển (`execution_end_date < hôm nay`; cron lỡ ngày vẫn bắt bù).
- [x] HHL-Q3: **báo người lập** lúc chuyển (khuôn `[HDB]`, nhóm "Cập nhật", như Có hiệu lực). Không nhắc trước hạn (chưa có Gia hạn để thao tác) ⇒ không migration.
- [x] HHL-Q4: YCXH đã lập trước khi hết hiệu lực **giữ như hiện tại** — chỉ chặn lưu Chờ duyệt (`assertContractCanExport`, đã có vì 20 ∉ EXPORTABLE_STATUSES); YCXH đã Chờ duyệt / đã duyệt / có ĐNXK đi tiếp tới PXK. PXK gửi sau khi hết hiệu lực không đổi trạng thái HĐ (`markInProgress` chỉ từ 6).
- HĐ không có `execution_end_date` (không nhập số ngày thực hiện) ⇒ không bao giờ tự hết hiệu lực.

**Cách làm:**
- `ContractService::expireIfOverdue(Contract)`: idempotent, chỉ khi status ∈ {6, 19} + `execution_end_date` < hôm nay ⇒ `transition(…, STATUS_HET_HIEU_LUC, [], 'expire', 'Quá thời hạn thực hiện (dd/mm/yyyy)')` + `notify('expired')`.
- `ContractNotificationService::expired()` → người lập, nhóm "Cập nhật"; lệnh lịch dùng nhánh `$command = true` sẵn có.
- `DetailContractResource` nhãn lịch sử `expire` ⇒ "Hết hiệu lực".
- Lệnh `assign:activate-signed-contracts` thêm bước 3 SAU bước quét bù Đang thực hiện: quét HĐ {6, 19} có `execution_end_date < today` ⇒ `expireIfOverdue`; `--dry-run` chỉ liệt kê. Cập nhật mô tả lệnh.
- FE: không sửa (badge/bộ lọc đã có mã 20; nút YCXH đọc cờ BE).
- Ngoài phạm vi: Thanh lý từ Hết hiệu lực (`liquidate()` vẫn chỉ từ 6), Gia hạn (21).

## Hủy duyệt + Đóng (18) ở Chờ KH ký — CHỐT 05/11/2026
Tham khảo ERP `FirmContractController::cancelApprove` (Có hiệu lực → Từ chối, chỉ `approver_id`, xoá HTHT) và `::close` / `FirmContract::canClose` (người lập · quản lý phòng · người duyệt; chặn khi đã có chứng từ).
- [x] HD-Q1: Hủy duyệt ⇒ **Không duyệt (13)**, lý do BẮT BUỘC (ghi `rejected_reason`, xoá người BGĐ đã chọn như reject). Người lập sửa + gửi lại từ bước TP.
- [x] HD-Q2: chỉ **người duyệt bước cuối** = `bgd_approved_at ? bgd_approver_id : (legal_approved_at ? legal_approver_id : approver_id)` (khớp ERP chỉ approver).
- [x] HD-Q3: Đóng (18) chỉ từ Chờ KH ký; ai: **người lập · người quản lý phòng của HĐ (`manageDepartmentIdsOf`) · người duyệt bước cuối**; lý do BẮT BUỘC (thêm so với ERP). Đóng là điểm cuối (không sửa / xoá / mở lại). Không cần kiểm chứng từ (thu tiền từ 17, YCXH từ 6 ⇒ ở 16 chưa thể có).
- [x] HD-Q4: thông báo **người lập + mọi người đã duyệt trong lượt** (approver_id, legal_approver_id nếu legal_approved_at, bgd_approver_id nếu bgd_approved_at), bỏ người thao tác. Hủy duyệt: `[HDB] Không duyệt: <b>{mã}</b>. Hủy duyệt. Người hủy: … Lý do: …` · Đóng: `[HDB] Cập nhật: <b>{mã}</b>. Đã đóng hợp đồng. Lý do: …` (16 nhóm của skill không có "Hủy duyệt"/"Đóng"; không dùng "Hủy" để khỏi hiểu là huỷ HĐ).
- [x] HD-Q5: Hủy duyệt **giữ HTHT** (lệch ERP có chủ đích) — TP duyệt lượt sau xoá + ghi lại (`ContractSupportAccountingService:468`), cùng cách Không duyệt ở bước Pháp chế / BGĐ.
- [x] HD-Q6 (skill thắng spec): nút **"Hủy duyệt"** `primary status="danger"` `ri-close-circle-line`; nút **"Đóng hợp đồng"** `primary status="danger"` `ri-forbid-line` (skill dành chữ "Đóng" cho nút thoát). Trạng thái/badge vẫn "Đóng". Cả 2 chỉ ở màn Chi tiết (thao tác phủ quyết không đặt ở danh sách), mở popup lý do bắt buộc (dùng lại popup Không duyệt).

**Cách làm:**
- BE `ContractService`: `lastApproverId()`, `canCancelApprove()`, `canClose()`, `cancelApprove($reason)` (16 → 13, history `cancel_approve`), `close($reason)` (16 → 18, history `close`); controller `POST {id}/cancel-approve`, `POST {id}/close` (validate `reason` required|string|max:255, 403 khi không đủ quyền).
- `DetailContractResource`: `is_can_cancel_approve`, `is_can_close`, `closed_reason` (ghi chú lịch sử `close` mới nhất), `rejected_by_cancel` (lần vào 13 gần nhất là `cancel_approve`) + nhãn lịch sử "Hủy duyệt" / "Đóng hợp đồng".
- `ContractNotificationService`: `approvalCancelled()`, `closed()`.
- FE `_id/index.vue`: 2 nút; popup lý do dùng chung 3 chế độ (Không duyệt / Hủy duyệt / Đóng hợp đồng); dải "Hủy duyệt: <lý do>" (13) và "Đã đóng: <lý do>" xám (18). Playwright đo nút + popup + payload; e2e thêm ca.
- Không migration.

## Đang thực hiện từ thu tiền / mượn bán — CHỐT 05/11/2026
Khảo sát: HRM có thu tiền (phiếu thu / báo có / điều chỉnh công nợ) + mượn bán ghi `account_details` gắn HĐ HRM (`contractable_type = Modules\Assign\Entities\Contract\Contract`); **hạch toán DV / CP cho HĐ HRM CHƯA CÓ** (ERP chỉ có cho HĐ hãng: `service_export_requests` / `service_accounting_requests`) ⇒ gắn sau khi có feature đó. Phiếu chi gắn HĐ chỉ là "chi trả lại KH" (hoàn tiền).
- [x] DTH-Q1: kích hoạt thêm = **thu tiền + mượn bán ĐÃ HẠCH TOÁN** (invoiceable_type `App\Model\IncomeExpenditure\BillIncome` · `BillIncomeReport` · `BillAdjustDept` · `App\Model\Warehouse\BorrowSell`). Không tính phiếu chi / uỷ nhiệm chi. DV/CP: khi có feature.
- [x] DTH-Q2: chỉ tính chứng từ ghi sổ **SAU lúc HĐ có hiệu lực** (`account_details.created_at` > lịch sử chuyển vào 6 mới nhất; HĐ không có dòng lịch sử đó ⇒ `invoiceable_date_accounting` > `effective_date`). Tiền cọc thu ở KH đã ký KHÔNG đẩy sang Đang thực hiện.
- [x] DTH-Q3: **chỉ quét bù trong lệnh `assign:activate-signed-contracts` (00:20)**, không móc vào service Finance (Đang thực hiện không đổi quyền thao tác nào ⇒ trễ ≤ 1 ngày chỉ là hiển thị). Ghi lịch sử `in_progress` kèm mã chứng từ đầu tiên.
- Ghi nhận ngoài luồng (chưa sửa): ô chọn HĐ ở Yêu cầu mượn bán không lọc trạng thái HĐ (`BorrowSellRequestService:754`) — HĐ Đang tạo cũng chọn được.
