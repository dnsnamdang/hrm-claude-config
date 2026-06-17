# Design — Đồng bộ thông tin hợp đồng gốc xuống phụ lục

**Người phụ trách:** @khoipv
**Spec chi tiết:** `docs/superpowers/specs/2026-06-08-dong-bo-thong-tin-hop-dong-xuong-phu-luc-design.md`

## Mục tiêu
Sửa 4 trường ở hợp đồng gốc (màn `contract/contract/{id}`, sau duyệt) → mọi phụ lục hiển thị giá trị mới:
`number` (số HĐ), `contract_sign_time` (ngày ký), `contract_end_time` (ngày kết thúc), `time_progress` (thời gian thực hiện — dẫn xuất từ ngày ký/kết thúc).

## Nguyên nhân
Phụ lục đọc thông tin gốc từ snapshot `ContractVersion`, nhưng `updateDataAfterApprove` chỉ update bảng `contracts`, không đụng snapshot → phụ lục thấy giá trị cũ.

## Quyết định lớn
- **Hướng A:** Đồng bộ 4 trường vào snapshot `ContractVersion` (giữ nguyên cách phụ lục đọc snapshot — rủi ro thấp, không sửa Resource).
- **Phạm vi:** Đồng bộ TẤT CẢ bản ghi `ContractVersion` của hợp đồng.
- **time_progress:** FE là nguồn tính, gửi lên trong payload; BE lưu + đồng bộ.

## Phạm vi
- Trong: 4 trường nêu trên.
- Ngoài: không đụng trường khác trong snapshot, không sửa Resource phụ lục, không đụng luồng tạo/duyệt phụ lục.
