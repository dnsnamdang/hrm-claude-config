# Nhiệm vụ agent: dò "màn hình tham chiếu dữ liệu danh mục" cho Phần 5 SRS

Bối cảnh: mỗi SRS danh mục được bổ sung "Phần 5. Bảng danh sách các màn hình tham chiếu dữ liệu danh mục"
— bảng 4 cột STT | Nhóm | Màn hình | Đường dẫn, liệt kê các màn KHÁC trong hệ thống có dùng dữ liệu danh mục đó.
Bạn CHỈ dò code và ghi file JSON; KHÔNG sửa code, KHÔNG sửa docx, KHÔNG đẩy Drive.

## Code để dò (nhánh gop_db — CHỈ ĐỌC, không sửa, không git gì cả)
- FE: /Users/manhcuong/Desktop/dns/HRM/worktrees/gop_db-client  (pages/, components/)
- BE: /Users/manhcuong/Desktop/dns/HRM/worktrees/gop_db-api  (Modules/, app/)
- Menu thật: gop_db-client/components/subsystems.js (tên phân hệ) + components/subsystem-menu/*.js (cây menu từng phân hệ) + components/menu-sidebar.js, components/menu.js
- Không đọc vendor/, node_modules/.

## Xác định danh mục
Đọc Phần 1/Phần 3 của file SRS (python-docx, file ở /Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/srs-phan5-tham-chieu/drive2/) để biết đúng danh mục là màn nào, bảng nào, route nào. Rồi trace route → page → API → controller → Entity → getTable() để chốt tên bảng + cột khoá ngoại (vd district_id, bank_id, currency_id…).

## Cách lấy dòng
- Grep cột khoá ngoại / tên model / API danh mục / component select danh mục ở BE + FE, tìm mọi màn mà người dùng CHỌN, LƯU, hoặc LỌC theo danh mục đó.
- Màn chỉ HIỂN THỊ (không chọn, không lọc) → KHÔNG đưa vào.
- Không đưa chính màn danh mục đó vào. Danh mục con dùng danh mục này làm cha (vd Quận/Huyện chọn Tỉnh) → CÓ đưa vào.
- Màn chỉ có route mà không có lối vào menu (code chết, không nằm trong subsystem-menu) → không đưa vào, nhưng ghi vào "excluded".
- Một màn có lối vào ở nhiều phân hệ → mỗi lối vào 1 dòng, cột Nhóm là phân hệ của lối vào đó.
- Popup/form dùng chung nhúng ở nhiều màn (vd popup Thêm khách hàng nhanh) → dòng theo màn chứa nó, ghi rõ trong tên màn.
- Gộp các thao tác của cùng 1 màn vào 1 dòng: "Danh sách/Thêm/Sửa/Chi tiết X" → "X", chỉ ghi rõ khi cần (vd "Hồ sơ nhân sự (địa chỉ thường trú, tạm trú)").

## Quy ước cột
- nhom: tên phân hệ hiển thị trong subsystems.js (vd "Danh mục", "Tài chính", "Bán hàng", "CSKH sau bán", "Thông tin NS", "Kho"…). Đúng chữ trên giao diện.
- man_hinh: tên màn theo nhãn menu (+ tab/popup nếu cần).
- duong_dan: đường bấm menu từ phân hệ tới NHÓM menu chứa màn, nối bằng " -> ", KHÔNG gồm tên màn ở cuối, theo đúng nhãn trong subsystem-menu. Màn nằm ngay cấp 1 thì chỉ ghi tên phân hệ. Ví dụ bảng mẫu (SRS Danh mục quốc gia):
  1 | Danh mục | Khu vực | Danh mục -> Địa lý
  3 | Danh mục | Khách hàng | Danh mục -> Đối tác
  5 | Bảo hiểm | Mua bảo hiểm nguyên tắc (Phiếu yêu cầu, Đơn bảo hiểm, Phiếu báo sau, Phụ lục bổ sung) | Nhân sự -> Bảo hiểm
- TUYỆT ĐỐI KHÔNG ghi URL hay route vào 3 cột này (chỉ được ghi trong evidence).
- Sắp xếp: nhóm theo phân hệ, các phân hệ theo thứ tự trong subsystems.js.

## Output — 1 file / danh mục
/Users/manhcuong/Desktop/dns/HRM/.plans/gop-db/srs-phan5-tham-chieu/refs2/<slug>.json
{
  "catalog": "Danh mục …",
  "srs_file": "SRS - Danh mục ….docx",
  "table": "<tên bảng>", "fk_columns": ["…"],
  "rows": [ {"nhom": "...", "man_hinh": "...", "duong_dan": "...", "evidence": "FE <file:dòng> · BE <file:dòng> · Lối vào: <subsystem-menu file:dòng>"} ],
  "excluded": [ {"man_hinh": "...", "ly_do": "chỉ hiển thị / không có menu / ..."} ],
  "notes": "lỗi đáng chú ý nếu thấy (vd xoá danh mục không kiểm tra đang dùng), ngắn gọn"
}
Rỗng thật thì rows = [] và giải thích trong notes.

Báo cáo cuối (ngắn): mỗi danh mục số dòng + điểm bất thường. Viết tiếng Việt.
