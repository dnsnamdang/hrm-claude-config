# #12212 YCTG / PTG — tick "Tính giá" theo từng ĐVT

Redmine: http://quanly.dnsmedia.vn/issues/12212 · user duyệt thiết kế 18/11/2026.

## Mục đích
Yêu cầu tính giá đang tính MỌI đơn vị tính của hàng hoá (bắt Giá NCC > 0 cho cả Cái/Hộp/Thùng dù NCC chỉ báo 1 ĐVT).
Sửa: tick chọn từng ĐVT cần tính giá → chỉ ĐVT được tick sang kế toán làm phiếu tính giá; ĐVT bỏ tick nhập lý do và
lý do hiện ở kết quả trả về kinh doanh (màn YCHG).

## Hiện trạng (17/10 — `khao-sat-duyet-tung-ma-erp-1710.md` D1–D5)
- Mỗi ĐVT đã là 1 dòng (`price_calculate_request_products`, `price_calculate_products`) có sẵn `chosen` + `unchosen_reason`.
- Nhưng tick theo MÃ: `ChosenProducts::resolve` lấy ĐVT đầu quyết cho cả mã; FE `priceInputRowsMixin.setChosen/setReason` lan cả mã;
  checkbox + ô lý do chỉ ở dòng đầu (`PriceInputGoodsTable.vue`); PTG 6 chặn bỏ tick mã còn ĐVT đã duyệt (`MSG_UNCHOSEN_LOCKED`).
- Đã sẵn theo DÒNG: PTG `skeletonRows` lọc `chosen=1`; `submit` bỏ dòng `chosen=0`; bản in + lịch sử in theo dòng.

## Quyết định đã chốt (user 18/11)
1. Đổi CẢ YCTG và PTG sang tick theo ĐVT (dùng chung mixin/bảng).
2. Kết quả trả KD ghi theo từng ĐVT: `Không tính giá ĐVT Hộp (XNK) — lý do: …`.
3. Mỗi ĐVT bỏ tick có 1 ô lý do riêng, bắt buộc khi gửi.

## Thiết kế
- **DB**: không đổi, không migration. Phiếu cũ tương thích (mọi ĐVT của 1 mã cùng giá trị).
- **BE `ChosenProducts::resolve`**: trả theo khoá `"product_id:unit_id"`, mỗi dòng tự quyết `chosen` + lý do; lỗi `rows.{i}.unchosen_reason`
  ở đúng dòng. `assertAnyChosen`: còn ≥ 1 ĐVT tick (message đổi thành "Phải chọn ít nhất 1 đơn vị tính để tính giá").
- **YCTG / PTG validate**: Giá NCC (và giá bán ở PTG) chỉ bắt buộc ở ĐVT tick.
- **PTG 6 (từ chối 1 phần)**: chỉ dòng bị từ chối sửa được (như cũ), nay bỏ tick được từng dòng đó dù mã còn ĐVT đã duyệt —
  bỏ khối `MSG_UNCHOSEN_LOCKED` (chống "mã nửa có giá nửa không" của D1 nay là chính yêu cầu).
- **Trạng thái hàng (D2)**: khi nhóm tính giá xong, chỉ mã **bỏ hết mọi ĐVT** (không còn dòng PTG `chosen=1`) mới về 1 Nhập thông tin;
  mã còn ≥ 1 ĐVT tick đi luồng bình thường (lên 3).
- **Thông báo người lập YCHG**: `(N hàng hoá không tính giá)` — N = số mã có ≥ 1 ĐVT không tính giá *(call của Claude)*.
- **Kết quả trả KD** (`not_priced` của dòng YCHG): đổi từ object sang MẢNG `[{unit_name, reason, by}]` (null nếu không có);
  FE liệt kê từng dòng. Tô nền "không đi tiếp" chỉ khi mã không có giá nào (không có `result`) *(call của Claude)*.
- **FE**: checkbox ở mọi dòng ĐVT; bỏ tick ⇒ ô "Lý do không tính giá *" hiện ở dòng đó (cột Tên hàng của dòng ĐVT);
  tick lại xoá lý do; checkbox khoá theo dòng (`readonly || row.editable === false`).
- Bản in / lịch sử: đã theo dòng, giữ nguyên.

## Ngoài phạm vi
ERP (không có màn tương ứng); đổi DB; tick hàng loạt ở tiêu đề cột.
