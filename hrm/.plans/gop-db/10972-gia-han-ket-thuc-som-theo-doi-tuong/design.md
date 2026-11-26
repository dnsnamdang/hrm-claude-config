# #10972 Gia hạn / kết thúc sớm phiếu giao công tác theo "Đối tượng"

**Người phụ trách:** @junfoke — 2026-11-26
**Redmine:** http://quanly.dnsmedia.vn/issues/10972 · **Nhánh:** `task_10972` (api + client, tách từ `origin/gop_db`)
**Spec đầy đủ:** `docs/superpowers/specs/gop-db/2026-11-26-10972-gia-han-ket-thuc-som-theo-doi-tuong-design.md`

## Mục tiêu
Trước đây duyệt phiếu gia hạn/kết thúc sớm (GHKTS) của BẤT KỲ nhân viên nào cũng đổi `to_time` của CẢ phiếu công tác.
Nay thêm "Đối tượng": **Tất cả nhân viên** (đổi ngày cả phiếu như cũ) / **Chỉ mình tôi** (chỉ đổi ngày của người tạo phiếu).

## Scope
1. Màn tạo/sửa/xem GHKTS: ô Đối tượng (bắt buộc khi PCT ≥ 2 nhân sự; 1 nhân sự ⇒ khoá "Chỉ mình tôi" nhưng vẫn đổi ngày cả phiếu).
2. Danh sách GHKTS: cột + bộ lọc Loại phiếu, Đối tượng; xuất Excel thêm 2 cột.
3. Chi tiết PCT, tab Nhân sự nhận việc: cột "Ngày gia hạn/kết thúc" (giữa "Có chiều về" và "Ghi chú", chỉ màn xem).
4. Số ngày công tác thực tế theo ngày riêng: chấm công theo PCT, kiểm trùng lịch, số ngày ở hồ sơ/đề nghị thanh toán, hệ số quyết toán.
5. Chặn tạo trùng: theo NGƯỜI TẠO + PCT (1 PCT : n phiếu GHKTS).

## Quyết định đã chốt (user, 26/11/2026)
- Phiếu "Tất cả" duyệt sau khi đã có ngày riêng:
  - gia hạn riêng: nâng theo đoàn nếu ngày đoàn ≥ ngày riêng, không thì giữ;
  - kết thúc sớm riêng: giữ, trừ khi đoàn kết thúc còn sớm hơn ⇒ theo đoàn.
  (User bác "phiếu duyệt sau cùng thắng" vì làm mất ngày riêng.)
- Phạm vi tính theo ngày riêng: chấm công + trùng lịch + thanh toán (+ quyết toán). Báo cáo, lịch, Việc của tôi, AI tool vẫn theo ngày phiếu.
- Cột ngày ở tab Nhân sự nhận việc đặt GIỮA "Có chiều về" và "Ghi chú" đúng như khách yêu cầu.
- Sửa luôn lỗi có sẵn `TimesheetService::isLastDay` (`Carbon::parse(null)` = bây giờ ⇒ ngày cuối thành hôm nay) — đã kiểm là lỗi thật.
- Ô lọc Đối tượng: bỏ trống = tất cả (rule cấm placeholder "Tất cả").
