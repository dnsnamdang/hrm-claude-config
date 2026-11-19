# Redmine 09/11/2026 — đợt B (lỗi mới + phản hồi)

Worktree: HRM/.wt-hrm-api-0911b, HRM/.wt-hrm-client-0911b (nhánh fix/redmine-0911-b từ origin/develop).
Ảnh vé: scratchpad rm/<id>/*.png. #11952/#11953 KHÔNG sửa: đã sửa lề ở client 889a5ab1b (07/11), chờ tester thử lại.

## A. Yêu cầu hạch toán DV HĐBH (plan gốc: gop-db/yeu-cau-hach-toan-dich-vu-hdbh, phieu-hach-toan-dich-vu-hdbh)
- [x] #12067 Chi tiết: tăng cỡ chữ cho đồng bộ
- [x] #12077 Tùy chỉnh cột: lưu xong thứ tự cột sai
- [x] #12078 Lưu nháp chỉ validate 1 trường bắt buộc
- [x] #12079 Data HRM thiếu/không khớp ERP (YC + Phiếu HĐBH) — KHÔNG sửa code: do quyền
- [x] #12080 Sửa phiếu cho phép sửa kiểu hạch toán, hợp đồng — không sửa — user chốt giữ như ERP (khoá kiểu, không đổi HĐ)
  - [x] A1 (#12067) Ô "Số hợp đồng" có link (chi tiết YC + form phiếu HT) dùng cỡ chữ/padding/nền như ô V2BaseInput sm — `.link-field` 12px/6px 10px/nền #f1f5f9; ServiceAccountingRequestDetail.vue + ServiceAccountingForm.vue
  - [x] A2 (#12077) Tìm gốc lệch thứ tự cột sau khi lưu (cột locked đứng sau cột thường trong allColumns) — mixin ghim cột locked theo số cột thường đứng trước; dời createdAt ra sau code ở service-accounting-requests/index.vue (mô phỏng mixin OK)
  - [x] A3 (#12078) Lưu nháp chỉ bắt Hợp đồng (FE + BE); type rỗng khi nháp → mặc định 1 như ERP — StoreRequest `required_if:status,2`; Service requestType() fallback 1; ServiceAccountingRequestForm.vue chỉ bắt type khi gửi duyệt
  - [x] A4 (#12079) So scope danh sách YC + Phiếu HRM với ERP, kết luận code hay quyền/dữ liệu — ảnh chỉ còn phiếu DNS Admin tự tạo = nhánh không có quyền xem (created_by=mình); cần cấp quyền view cho vai trò ở cty đang làm việc
  - [x] A5 (#12080) ĐÃ HOÀN TÁC theo user: màn Sửa giữ khoá Kiểu + Hợp đồng như ERP; bỏ toàn bộ logic đổi HĐ/kiểu ở Service/Controller/Form (controller về nguyên bản; test rollback: update gửi HĐ/kiểu khác vẫn giữ 5491/type 3)
  - [x] A6 (#12080) Ô "chọn tất cả" bảng chi phí tích khi bảng trống như ERP (`check_all_costs` = số tick === số dòng, 0 === 0) — allTicked bỏ điều kiện `length > 0`; ServiceAccountingRequestForm.vue

## B. DM mẫu báo giá vận chuyển (plan gốc: gop-db/mau-bao-gia-van-chuyen, delivery-quotation-qa-ui)
- [x] #12070 Lưu nháp mất số km + không ghi lịch sử; km vượt trội giữ 2 số thập phân
- [x] #11936 Lưu nháp không bắt số km; ngày hiệu lực từ < hôm nay: sửa thông báo/chặn lịch
- [x] #11935 Popup: nút Áp dụng trước Đóng
- [x] #11934 Làm sáng màu ô (không nhầm ô disabled)
- Việc con B:
  - [x] B1 (#12070a) Lưu nháp chưa đủ xe/trọng tải → tuyến + km bị `sanitizeDetails` bỏ (tuyến chỉ lưu dưới payload) → mất dữ liệu, không lịch sử. Thêm cột `delivery_quotations.draft_roads` (JSON) giữ tuyến khi chưa có xe; Resource + lịch sử `road_rows` đọc dự phòng từ đó — test rollback: nháp không xe giữ tuyến+km, lịch sử create+update có Km; migration CHƯA chạy
  - [x] B2 (#12070b) `km_actual` là INT ở `delivery_quotations` + `price_list_valid_deliveries` → migration DECIMAL(10,2) (KHÔNG chạy); hiển thị lịch sử BGHLVC giữ 2 số lẻ — bảng tạm DECIMAL lưu 12.50, lịch sử "12.5"
  - [x] B3 (#11936a) FE gửi km trống = 0 → BE nháp `min:1` báo lỗi. FE gửi null khi trống; BE `sanitizeDetails` km null → 0 cho cột NOT NULL — Validator nháp km null PASS; Resource trả km 0 → null
  - [x] B4 (#11936b) Ngày hiệu lực từ < hôm nay: câu lỗi nghiệp vụ rõ ràng + khoá ngày quá khứ trên lịch — messages() Store+Update; disabled-date 2 ô ngày
  - [x] B5 (#11935) QuickAddRoadModal: Áp dụng trước Đóng — compile OK
  - [x] B6 (#11934) Ô "Chọn tuyến đường" đổi sang `V2BasePickerInput` (ô trắng + kính lúp, bỏ disabled giả) — thêm nút × xoá tuyến; compile OK
  - [x] B7 (#12070 ERP) Worktree ERP/.wt-erp-km (fix/km-actual-decimal từ origin/gop_db): cast km_actual float ở PriceListValidDelivery + DeliveryQuotation (JS cộng km chuyến không nối chuỗi "12.50"); show bảng giá + biến in KM_VUOT_TROI dùng formatKm (12.5 / 1,200) — php -l OK, chưa commit

## C. QT thưởng NS quý (plan gốc: qt-thuong-ns-quy-moi)
- [x] #12031 Danh sách: icon Duyệt đồng bộ
- [x] #12033 Popup HĐ: chữ "Trưởng phòng", màu tiêu đề bảng + phân trang như buy-service-accounting-requests, 10/20/50/100 mặc định 10
- [x] #12034 Chi tiết: khoảng cách nút đồng bộ; người tạo "Tên - ngày giờ", bỏ mã phòng
- [x] #12035 Excel: giãn 2 cột để tên trên 1 dòng
- Việc con C:
  - [x] C1 index.vue: nút Duyệt hàng dùng icon + kiểu chung như các màn khác — ri-checkbox-circle-line + `to` sang chi tiết như QT thưởng năm/phiếu thu chi; bỏ approveItem
  - [x] C2 ContractDetailModal: tag chức danh viết đủ "Trưởng phòng"; header bảng + phân trang theo SourcePickerModal của buy-service-accounting-requests; 10/20/50/100 mặc định 10 — tag TP/TBP ra chữ đủ; màu misa-grid + chữ 12px; thanh phân trang chép markup V2BaseDataTable
  - [x] C3 _id/index.vue: khoảng cách nút như buy-service-accounting-requests/_id; người tạo "Tên - ngày giờ" bỏ mã phòng — bỏ class mr-2 mb-2 (V2Footer đã gap 5px); BE detail thêm creator_name (chỉ tên)
  - [x] C4 Export danh sách: giãn cột "Tổng thưởng năng suất", "Hoa hồng thưởng thêm"; kiểm bằng openpyxl — exportColumns 20→30 (+ Ngày hạch toán 16→20); file dựng bằng buildXlsxBlob thật, G:H=30

## D. Vận chuyển + HĐ bán đầu kỳ
- [x] #11956 HĐ vận chuyển: ẩn "In bảng kê danh sách"; nút + cách xuất Excel theo chuẩn chung
  - [x] D1. Đối chiếu ERP HĐ vận chuyển: có/không "In bảng kê danh sách" — ERP chỉ có In / In bảng kê / Xuất bảng kê TỪNG HĐ ở dòng, không có bản in cả danh sách
  - [x] D2. Bỏ lựa chọn "In bảng kê danh sách" ở danh sách HĐVC (giữ quyền ẩn nút các mục còn lại) — bỏ nút toolbar; giữ "In bảng kê" từng HĐ ở dòng + chi tiết; user chốt xoá BE in cả danh sách: printListData bắt buộc id (thiếu → 422), bỏ nhánh scoped+lọc + PRINT_LIST_MAX (route/method/mẫu in giữ vì in từng HĐ dùng chung)
  - [x] D3. Nút Xuất Excel theo button-convention + luồng xuất theo export-excel (so màn BGHLVC/mẫu BGVC) — BE export-columns/export-rows (quyền export) + ExportFieldsModal/exportListFile; nút xuất chi tiết thêm ?id= (trước xuất cả danh sách)
- [x] #12053 HĐ bán đầu kỳ tạo mới: placeholder địa chỉ/SĐT; ô khách hàng xuống hàng 2 trước địa chỉ
  - [x] D4. Form tạo/sửa: ô Khách hàng xuống hàng 2 trước Địa chỉ; placeholder Địa chỉ + SĐT — ngắt w-100 sau Ngày ký; placeholder "Tự điền theo khách hàng"

## E. Phiếu xuất bán hàng mượn chi tiết (plan gốc: pxbhm-detail-match-erp)
- [x] #11427 KHÔNG sửa: đã kiểm 06/11 (PXBHM-04312 đủ 2 tab + bảng thanh toán), chỉ còn treo trạng thái

## Kết
- [x] Review diff, kiểm tra (php -l, compile template, script), commit + push develop khi user đồng ý
