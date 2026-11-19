# Phase 32 — Xác nhận bảo lãnh · Ngày mốc thực hiện nhập sau · Xuất hàng khi chưa đủ mốc (HĐ bán HRM)

Nguồn: **yêu cầu khách hàng** 10/11/2026, mục 4a, 5, 6 (`yeu-cau-bo-sung-10-11-gap.md`). Đợt 2/5. Quyết định chốt với user 11/11 (3 câu, đều chọn phương án đề xuất).
Mockup: `mockup-moc-bao-lanh-xuat-hang.html`. Nền: Phase 31 (bỏ mặc định điều kiện hiệu lực / mốc tính thời hạn).

## 1. Mục tiêu

- Ngày bảo lãnh được duyệt và ngày mốc thực hiện là **sự kiện xảy ra SAU khi ký** ⇒ nhập bằng nút riêng trên màn xem HĐ, kèm bằng chứng + lịch sử, không nhập trong form Lập/Sửa.
- HĐ đã có hiệu lực nhưng chưa có ngày mốc (chưa tính được ngày kết thúc thực hiện) vẫn xuất hàng được, đổi lại phiếu phải qua TP → BGĐ.

**Không làm (đợt sau):** Yêu cầu xuất giữ cho HĐ HRM (Yêu cầu xuất giữ HRM chưa gắn được HĐ bán HRM — làm phần gắn HĐ trước); tiến độ thanh toán / kế hoạch giao hàng / cảnh báo (đợt 3).

## 2. Xác nhận bảo lãnh được duyệt (4a) — chốt câu 1

- **Nút** "Xác nhận bảo lãnh được duyệt" (màn xem HĐ, khu nút luồng duyệt): chỉ **người lập**, HĐ **KH đã ký (17)** và `effective_condition = 3`. Ẩn khi đã xác nhận.
- **Popup** khuôn `ContractCustomerSignedModal` (V2BaseModal md): *Ngày bảo lãnh được duyệt* * (không quá hôm nay) + *File bảo lãnh* * (V2BaseFile, PDF/ảnh/Word ≤ 20MB). Dòng nhắc: HĐ chuyển Có hiệu lực khi tới ngày.
- **BE** `POST assign/contracts/{id}/guarantee-approved` ⇒ `ContractService::confirmGuaranteeApproved(contract, date, fileName, filePath)`:
  ghi `guarantee_approved_date` + 2 cột mới `guarantee_file_name`, `guarantee_file_path`, `guarantee_confirmed_at`; lịch sử action `guarantee_approved`
  (không đổi trạng thái — log status cũ = mới); `recomputeEffectiveDates` + `activateIfEffective` (tới ngày ⇒ Có hiệu lực ngay, chưa tới ⇒ lệnh lịch `contracts:activate`).
  Chặn: không phải người lập 403; sai trạng thái / sai điều kiện 422; thiếu ngày / file 422 dưới ô.
- **Form Lập/Sửa:** bỏ ô *Ngày bảo lãnh được duyệt*; BE store/update **không nhận** `guarantee_approved_date` nữa (chỉ đi qua nút).
- **Màn xem HĐ:** hiện ngày + link file bảo lãnh (như file HĐ đã ký).

## 3. Ngày mốc thực hiện nhập sau (5) — chốt câu 2

- **Nút** "Cập nhật ngày mốc thực hiện": chỉ **người lập**, `execution_deadline_base ∈ {2,3,4}`, HĐ ở **KH đã ký (17) / Có hiệu lực (6) / Đang thực hiện (19)**. Đã nhập vẫn hiện (sửa lại).
- **Popup:** *Ngày <tên mốc>* * (vd "Ngày KH bàn giao mặt bằng"; không quá hôm nay) + *Biên bản* (V2BaseFile, KHÔNG bắt buộc). Hiện ngày hiện tại nếu đã có.
- **BE** `POST assign/contracts/{id}/execution-base-date` ⇒ `ContractService::updateExecutionBaseDate(contract, date, ?fileName, ?filePath)`:
  ghi `execution_base_date` + cột mới `execution_base_file_name`, `execution_base_file_path`; `recomputeEffectiveDates` (ra `execution_end_date`);
  lịch sử action `execution_base_date` kèm meta cũ → mới. Chặn như mục 2.
- **Form Lập/Sửa:** bỏ ô *Ngày mốc (bàn giao/chốt TK)*; BE store/update không nhận `execution_base_date`.
- Hệ quả: HĐ mốc 2–4 lúc mới có hiệu lực chưa có ngày kết thúc thực hiện ⇒ rơi vào mục 4.

## 4. Xuất hàng khi chưa đủ mốc (6) — chốt câu 3

- **"Chưa đủ mốc"** = HĐ Có hiệu lực / Đang thực hiện, có `effective_date`, `execution_deadline_days > 0` nhưng **chưa có `execution_end_date`** (thiếu ngày mốc).
  HĐ chưa có hiệu lực ⇒ vẫn chặn như hiện tại.
- `Contract`: `can_export` = có hiệu lực (giữ điều kiện cũ, bỏ vế bắt buộc ngày kết thúc); thêm accessor `is_missing_execution_base`. Câu chặn cũ "chưa có hiệu lực hoặc chưa nhập thời hạn thực hiện" đổi thành "chưa có hiệu lực".
- **YCXH loại 20/21 gắn HĐ HRM** — dùng lại luồng TP → BGĐ sẵn có (vượt hạn mức công nợ, #11900):
  1. Gửi duyệt (status 2) mà HĐ thiếu mốc ⇒ 409 `type = contract_missing_execution_base`, câu: *"Hợp đồng chưa đủ mốc tính thời gian thực hiện (chưa nhập ngày <tên mốc>), cần Trưởng phòng và Ban giám đốc duyệt. Bạn có muốn gửi duyệt không?"*
  2. Đồng ý ⇒ FE gửi lại status 10 ⇒ phiếu **Đợi TP duyệt**, báo TP.
  3. TP "Chuyển BGĐ duyệt" (bắt buộc ghi chú) ⇒ **Đợi BGĐ duyệt**, báo BGĐ. TP / BGĐ "Không duyệt" như hiện có.
  4. BGĐ duyệt ⇒ **Chờ duyệt (2)**, đi tiếp như phiếu thường.
  - Vượt hạn mức công nợ chỉ áp loại 14/17 ⇒ phiếu 20/21 chỉ có thể vào 10/11 vì thiếu mốc — không cần cột cờ lý do, không có trường hợp dính cả 2.
  - Tới lúc duyệt mà HĐ đã nhập đủ mốc ⇒ vẫn cho duyệt bình thường (không hỏi lại).
- **Người duyệt** (khác loại 14/17): TP = có quyền **duyệt HĐ bước TP** (`sale.hop_dong_du_an_tkt.approve`) + phòng HĐ thuộc phòng được giao quản lý (cùng điều kiện duyệt HĐ);
  BGĐ = quyền **BGĐ duyệt HĐ** (`sale.hop_dong_du_an_tkt_ban_giam_doc.approve`) cùng công ty phiếu. `canManagerApprove` / `canBoardOfManagerApprove` / `canReject` rẽ theo loại phiếu;
  `notifyManagers` / `notifyBoard` lấy người nhận theo đúng quyền đó.
- **Hiển thị:** màn chi tiết YCXH ở 10/11 có khối cảnh báo lý do (note-warning); màn xem HĐ khi thiếu mốc có dòng nhắc "Chưa đủ mốc — YCXH cần TP và BGĐ duyệt" cạnh nút Yêu cầu xuất hàng.

## 5. Dữ liệu

Migration `hrm_contracts` (bảng riêng HRM): `guarantee_file_name`, `guarantee_file_path`, `guarantee_confirmed_at`, `execution_base_file_name`, `execution_base_file_path` — nullable. Không sửa dữ liệu.
YCXH: không thêm cột (bảng dùng chung ERP).

## 6. Kiểm

- PHPUnit: 2 endpoint (đúng người / sai người / sai trạng thái / sai điều kiện / thiếu file), tính lại ngày + chuyển Có hiệu lực; can_export; YCXH 20/21 thiếu mốc ⇒ 409 ⇒ 10 ⇒ 11 ⇒ 2,
  quyền TP/BGĐ (có / không quyền, khác phòng), loại 14/17 không đổi hành vi (bộ ProductExportOverLimitApiTest).
- Playwright: 2 popup (lỗi dưới ô, file), màn xem HĐ hiện ngày + file; form Lập/Sửa không còn 2 ô; YCXH gửi duyệt ⇒ hộp xác nhận ⇒ Đợi TP duyệt; TP/BGĐ thấy nút.

## 7. Nhánh

Đụng `edit.vue` / `ContractService` vừa sửa ở Phase 31 (chưa commit) và YCXH loại 20/21 (Phase 29/30 sửa nhiều ở nhánh `gop_db-xuat-hang-cha-con`, chưa merge gop_db).
Đề xuất làm tiếp trên `gop_db-hd-dieu-kien-duyet` (cùng Phase 31) — hỏi lúc xin "làm".
