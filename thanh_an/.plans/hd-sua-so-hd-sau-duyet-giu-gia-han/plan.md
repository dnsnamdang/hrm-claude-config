# Plan — HĐ: sửa số HĐ sau duyệt không làm mất gia hạn của phụ lục thời gian

> @khoipv — Bắt đầu 27/10/2026
> Màn: `hrm-thanhan-client/pages/contract/contract/components/GeneralComponent.vue` (lưu sau duyệt) · BE: `ContractService::updateDataAfterApprove`

## Bối cảnh
- Sửa số HĐ / ngày ký / ngày KT sau duyệt → BE ghi vào `contracts` + đồng bộ vào TẤT CẢ `contract_versions` (đã đúng với số HĐ).
- Lỗi: FE luôn gửi đủ 4 trường; ô Ngày KT + Tiến độ hiển thị theo **version 0** (`ContractDetailResource`) → HĐ đã có PL gia hạn được duyệt, chỉ sửa số HĐ cũng ghi đè `contracts.contract_end_time` / `time_progress` + snapshot các version sau về ngày gốc → mất gia hạn.

## Quyết định
- HĐ có phụ lục `extend_time` **đã duyệt** → khoá ô Ngày KT ở màn HĐ (đổi ngày KT qua phụ lục); BE bỏ qua `contract_end_time`, `time_progress`.
- FE chỉ gửi trường thực sự thay đổi (BE đã dùng `has()`).
- Số HĐ, ngày ký vẫn đồng bộ vào mọi version như cũ.

## Phase 1 — BE
- [x] `updateDataAfterApprove`: HĐ có PL gia hạn đã duyệt → bỏ `contract_end_time`, `time_progress` khỏi danh sách trường cập nhật

## Phase 2 — FE
- [x] `callApiSubmitDataAfterApprove`: chỉ gửi trường thay đổi so với `originalData`
- [x] Computed `hasApprovedExtendTimeAnnex` (từ `formSubmit.annexes`) → khoá ô Ngày KT + dòng ghi chú
- [x] Watcher `formSubmit` khởi tạo `originalData` thiếu `time_progress` → bổ sung

## Phase 3 — Cho sửa Tên HĐ sau duyệt (27/10/2026, user yêu cầu "tương tự số HĐ")
- [x] BE `updateDataAfterApprove`: nhận `name` → ghi `contracts` + đồng bộ mọi `contract_versions` (key `name` khớp `ContractDetailResource`)
- [x] BE controller: validate `name` `sometimes|required` (không cho để trống — lúc lập HĐ là bắt buộc)
- [x] FE: mở ô Tên HĐ khi `canEditAfterApprove`; thêm `name` vào `originalData` / theo dõi thay đổi / payload; bắt lỗi 422 hiện dưới ô

### Checkpoint — 27/10/2026
Vừa hoàn thành: Phase 1 + 2 + 3
Đang làm dở:
Bước tiếp theo: user test — HĐ có PL gia hạn đã duyệt: sửa số HĐ → `contracts.contract_end_time` + các version giữ ngày gia hạn; HĐ chưa có PL gia hạn: sửa ngày KT vẫn lưu bình thường
Blocked:
