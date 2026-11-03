# Trả hàng hóa đơn có quà tặng — không trả nốt được phần còn lại (HD1526681) — @cuong61n

- [x] **03/11/2026 — Sửa màn "Khách trả hàng" cho hóa đơn có hàng tặng đã trả một phần**
  - Số Redmine: chưa có (khách NT Hồng Mai / tài khoản anhmy3513, GDP, báo qua chat 02/11).
  - Nghiệp vụ: HD1526681 (bán 26/02/2025, 140 sp gồm 4 dòng quà) đã có phiếu trả HDT204604
    (120 sp, chỉ trả phần quà + 3 dòng bán, còn thiếu 20 hộp Becolitor 10 lô 0100). Khách muốn
    trả thêm 4 hộp nhưng màn trả hàng khoá ô "Số lượng trả" nên không trả được. Quy tắc hiện tại:
    hóa đơn có quà phải trả nguyên đơn; đã trả một phần rồi thì giờ cho nhập số còn lại, tính tiền
    theo giá dòng bán (15.840 đ/hộp + VAT 5%).
  - Kỹ thuật (`sphacy_web/src/pages/sales/partials/SalesReturnModal.jsx`, commit `07f6256`):
    (1) dòng bán và dòng quà trùng thuốc/đơn vị/lô nên số đã trả bị dồn vào dòng đầu tiên → ghép
    theo loại dòng (phiếu trả không lưu `is_gift`, dòng đơn giá 0 coi là quà), ưu tiên dòng còn dư;
    (2) cờ khóa `isGift` chỉ bật khi hóa đơn chưa từng trả.
  - Đã kiểm: Playwright GDP :3007 trên dump local (dựng lại HD1526681 done + phiếu trả thiếu dòng
    20 hộp): bản cũ hiện 5 dòng/ô khóa (test fail), bản mới 1 dòng, ô nhập được, nhập 4 → 66.528;
    bấm "Hoàn thành" thật → phiếu IV3 4 hộp, đơn giá 15.840, VAT 5, tồn lô 0100 +4 (đã hoàn dữ liệu
    thử). Test: `tests/test_return_gift_partial.py` (chưa commit, ngoài repo sphacy_web).
  - Dữ liệu prod: chỉ đọc, không sửa. Lưu ý cửa hàng 2612 có ~34% hóa đơn bán 90 ngày có quà
    (178/524), nên lỗi này sẽ gặp lại nếu chưa vá; không có chương trình khuyến mãi cấu hình
    (bảng `promotion` rỗng), quà do người bán tự thêm dòng `is_gift`.
  - Trạng thái: **đã deploy prod 03/11/2026** — build GDP + GPP (bản đang chạy là `bd95360`, build
    02/11 16:27, mới hơn đúng 1 commit), chép vào `/var/www/html/gdp/build` và
    `/var/www/html/sphacy_gppweb/build` trên cả 42.96.41.13 và 42.96.41.135; bản cũ giữ ở
    `build_truoc_tra_hang_03_11` (rollback: đổi tên lại). Chunk mới `1.a4136a27`, kiểm 12/12 lần
    qua LB ở cả hai cổng đều trả index trỏ chunk mới. Chưa test thao tác trả 4 hộp thật trên prod —
    cần người dùng trả thử HD1526681.
  - Chưa làm: `pages/updateData/partials/SalesReturnModal.jsx` và `WarehousingReturnModal.jsx`
    có logic tương tự, ngoài phạm vi đơn này.
