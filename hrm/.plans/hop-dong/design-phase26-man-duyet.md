# Phase 26 — Màn Duyệt hợp đồng bán (HRM)

> Ngày: 06/11/2026 · Nhánh: `gop_db-hop-dong-ban` (worktree `wt-hop-dong-ban`, hrm-api + hrm-client)
> Trạng thái: thiết kế đã chốt, plan ở `plan.md` mục Phase 26, GĐ 1–5 đã code (chưa commit GĐ 5), xem Checkpoint trong plan.md.
> Mockup: `mockup-man-duyet-hd.html` (số liệu HĐ 734, 4 vai). Mockup là chuẩn về bố cục. Tài liệu này là chuẩn về logic.

## 1. Mục đích

Hiện người duyệt HĐ HRM không có một nơi để xem đủ thông tin rồi quyết định:
- Bước TP phải sang màn Hỗ trợ hạch toán (HTHT). Bước Pháp chế và BGĐ bấm Duyệt thẳng ở chi tiết, không qua màn xem nào.
- Pháp chế không có cách đánh dấu đoạn cần sửa trên bản in. Chỉ có một ô lý do.
- Bấm Duyệt không ghi được ý kiến, nên bước sau không biết bước trước nghĩ gì.
- Khi soạn và khi duyệt đều không biết bản in ra mấy trang, ngắt ở đâu (hạn chế lớn so với Word).

User cần màn này để thuyết trình phương án với KH, nên mockup phải đẹp và sản phẩm thật phải giống mockup.

## 2. Mục tiêu / Không làm / Thất bại nếu

**Mục tiêu**
- Mọi bước duyệt đều đi qua một màn Duyệt. Không còn đường duyệt thẳng từ danh sách hay chi tiết.
- Màn Duyệt có 3 tab: Hỗ trợ hạch toán, Bản in hợp đồng (chia tờ A4), Phân tích lãi lỗ.
- Pháp chế chỉ xem bản in và đánh dấu nội dung cần sửa. Người lập sửa theo ý kiến, HĐ đi lại đủ các bước từ TP.
- Ở mỗi bước, người xem đọc được ý kiến duyệt / không duyệt của các bước khác, có lịch sử theo từng lần gửi duyệt.
- Những gì ERP cho sửa khi duyệt thì HRM giữ nguyên logic (user chốt 06/11).

**Không làm**
- Không làm trang soạn kiểu Word trên tab Mẫu in (đã tư vấn mức 2, user chưa chốt, là việc riêng).
- Không đổi 3 điều kiện chuyển BGĐ đã làm ở Phase 24. Chỉ thêm 1 điều kiện mới theo D11.
- Không làm cờ HĐ ngoài thị trường (`is_market`), tách việc riêng.
- Không sửa báo cáo Phân tích lãi lỗ của ERP. Không dựng báo cáo tổng nhiều HĐ trong HRM.
- Không đụng màn `paymentManage` kiểu ERP. Đó là màn sau duyệt (Thanh toán / Bàn giao / Hạch toán / Tính lãi), chỉ tham khảo bố cục tab.

**Thất bại nếu (dù chạy được)**
- Còn đường nào duyệt được mà không qua màn Duyệt, hoặc API duyệt không kiểm đúng bước và đúng người.
- BGĐ sửa HTHT nhưng số thưởng / hoa hồng đã lưu không khớp số đang xem lúc bấm Duyệt.
- Ý kiến Pháp chế biến mất hoặc gắn sai đoạn sau khi người lập sửa bản in.
- Bản in trên màn Duyệt lệch nội dung với bản in thật, hoặc mất / lặp chữ khi chia tờ.
- Người không có quyền xem giá vốn thấy giá vốn hoặc lãi lỗ qua tab mới.

## 3. Quyết định đã chốt

| # | Nội dung | Chốt (user) |
|---|---|---|
| D1 | Bấm Duyệt | Luôn vào màn xem rồi mới duyệt |
| D2 | Tab | Hỗ trợ hạch toán / Bản in hợp đồng / Phân tích lãi lỗ. Tab thứ 3 là báo cáo `report.analysisProfitContract`, KHÔNG phải tab Tính lãi của `paymentManage` |
| D3 | Pháp chế | Chỉ xem bản in, chỉ duyệt thông tin, có cơ chế đánh dấu nội dung cần sửa |
| D4 | Sau khi người lập sửa | Đi lại đúng các bước từ TP vì HĐ đã đổi |
| D5 | Bố cục | Phương án C: thông tin HĐ + tuyến duyệt ở cột phải 262px, thu gọn được còn 46px, trong layout sidebar + topbar |
| D6 | Tab | Dùng mẫu tab chung của phần mềm (`V2BaseTabNavigation`), đủ hover / active |
| D7 | Thời gian gửi duyệt | Hiện trên panel, kèm thời gian đã chờ |
| D8 | Bản in | Xem theo tờ A4 bằng Paged.js, bảng hàng hoá có viền, có zoom |
| D9 | Lịch sử | Mỗi bước đọc được ý kiến các bước khác, có lịch sử |
| D10 | Logic ERP | Phần ERP cho sửa khi duyệt thì HRM giữ nguyên (L1) |
| D11 | TP đổi tỷ lệ / 14.1 khi HĐ có bước Pháp chế | Vẫn qua Pháp chế duyệt nội dung trước (06/11). TP Duyệt, tới Pháp chế chỉ còn Chuyển duyệt BGĐ |
| D12 | `is_market` | Không làm ở Phase 26, ghi việc riêng (06/11). Tạm thời HĐ ngoài thị trường duyệt như HĐ thường |
| D13 | Quyền tab Phân tích lãi lỗ | Luôn cần Xem giá vốn hàng hoá. Người đang duyệt bước đó (TP, BGĐ) không cần thêm quyền báo cáo. Người khác cần quyền báo cáo, mở quyền này cho HRM (06/11) |
| D14 | Phạm vi Paged.js | Màn Duyệt và nút In hợp đồng ở chi tiết, để bản duyệt và bản in giống nhau (06/11). Các bản in khác giữ nguyên. Gồm cả In hợp đồng ở dòng danh sách (user ok 06/11) |
| D15 | Phụ lục hàng hoá | Tab Bản in chỉ hiện hợp đồng chính (06/11). Phụ lục vẫn in ở chi tiết như hiện tại |
| D16 | Dòng Đề xuất sau khi BGĐ duyệt | Giữ lại, lệch ERP có chủ đích, để xem được TP đề xuất gì và BGĐ duyệt gì (06/11) |
| D17 | Sửa số liệu HTHT giữa TP và BGĐ | Tuân thủ nguyên tắc ERP, theo mục 5.3a. D16 là ngoại lệ duy nhất, user chấp nhận (06/11) |
| D18 | Nhãn nút từ chối ở luồng duyệt HĐ | Giữ "Không duyệt", không theo chữ "Từ chối" của `button-convention` (user chốt 06/11) |

## 4. Kết quả khảo sát ERP và đối chiếu HRM

Đọc code ERP `gop_db` (`8e3f46c42c`) và HRM `gop_db-hop-dong-ban` (`50ca18435`), 06/11. Chưa chạy thử trên ERP.

ERP chỉ có 1 trạng thái Chờ duyệt. Chuyển duyệt chỉ đổi `approver_id`, HĐ vẫn ở Chờ duyệt. Vì vậy `isPreview = status != CHO_DUYET` nên **người nhận chuyển duyệt (BGĐ) dùng đúng màn HTHT, sửa được như TP**, và bấm Duyệt là tính lại HTHT (`FirmSupportAccountingService::calculate`). Bước Pháp chế không có ở ERP, là phần riêng của HRM.

| Việc | ERP | HRM hiện tại | Phase 26 |
|---|---|---|---|
| Sửa HTHT khi TP duyệt | Có | Có | Giữ |
| Sửa HTHT khi BGĐ duyệt | **Có**, Duyệt tính lại HTHT | Không: FE chỉ mở ở status Chờ duyệt, BE chỉ `calculate` khi bước `tp` | **Thêm** (mục 5.3) |
| Nguồn vốn, 14.1 thưởng, 16 dự phòng, chi phí thực hiện | Sửa được (nguồn vốn + chi phí chỉ HĐ dự án, type 4) | Sửa được | Giữ. HĐ HRM tương ứng HĐ dự án (quyền `sale.hop_dong_du_an_tkt.*`) |
| % phân chia phòng chính, phòng hỗ trợ | **Sửa được** (%DS, tháng / quý, tỷ lệ NV / TBP / TP) | **Không có ô nhập**. BE nhận `department_main`, `departments_support` nhưng FE không gửi | **Thêm ô nhập** |
| Tổng %DS các phòng = 100, tổng % phân chia = 100 | Chặn ở FE | Chưa thấy | **Thêm**, chặn cả BE |
| Đổi tỷ lệ so với quy chế (`keyChanged`) | Không phải BGĐ thì phải Chuyển duyệt | Chưa thấy | **Thêm** |
| Đổi 14.1 | Không phải BGĐ thì phải Chuyển duyệt. Mục 15 khác 0 thì chặn | Chưa thấy | **Thêm** |
| Thưởng 14.1 vượt quy chế | BGĐ phải xác nhận | Chưa thấy | **Thêm** |
| HĐ ngoài thị trường được phân (`is_market`) | Cờ tính lúc lập HĐ từ báo giá rồi lưu. TBP không duyệt thẳng được (`canApprove`), khi duyệt có câu hỏi xác nhận | Không có cột, không có code | Tách việc riêng (D12) |
| Thiếu giá vốn công ty HĐ | Chặn duyệt, báo rõ mã (`missingCostError`) | Chưa thấy | **Thêm** |
| Ý kiến khi Duyệt | Ô `approve_comment`, không bắt buộc, ghi lịch sử | `approve()` không nhận ghi chú | **Thêm** |
| Ý kiến khi Chuyển duyệt | **Bắt buộc** | Không bắt buộc | **Đổi thành bắt buộc** |
| Lý do Không duyệt | Bắt buộc | Bắt buộc | Giữ |
| Lịch sử duyệt | Bảng Tài khoản / Nội dung / Hành động / Thời gian trên màn HTHT | Có `hrm_contract_histories` (`note` kiểu text, `meta` json), hiện ở tab Lịch sử chi tiết | Hiện trên màn Duyệt, chia theo lần gửi |
| Không duyệt | **Xoá hẳn HTHT đã lưu** (4 bảng) | Không xoá (HD-Q5 Phase 24: Hủy duyệt giữ HTHT, lệch ERP có chủ đích) | Giữ HD-Q5, lượt sau TP tính lại (mục 5.3) |
| Mở màn HTHT | Nạp HTHT đã lưu | **Luôn tính lại từ quy chế**, không đọc số đã lưu | **Đổi** (mục 5.3) |
| Lưu `over_date`, `interest_rate` khi duyệt | Có | Chưa dùng ở HĐ HRM | Để phase sau, khi làm Tính lãi |
| Quyền xem báo cáo lãi lỗ | Phạm vi công ty trở lên, không có thì ẩn link | Catalog quyền ghi `platforms: ['erp']`, phạm vi 3 và 4, HRM chưa dùng (DB rehearsal có 1 dòng guard api cùng tên). Chưa có báo cáo | Theo D13 |
| HĐ ẩn giá | `shouldHidePrice()` | Tắt `is_can_approve`, chặn HTHT và in hợp đồng | Giữ. Người chỉ thấy HĐ dạng ẩn giá không vào được màn Duyệt. **L3 không cần chốt thêm** |

"Chưa thấy" nghĩa là tôi tìm theo tên ERP và theo từ khoá trong `ContractService`, `ContractSupportAccountingService`, `ContractController`, `support-accounting.vue` nhưng không ra. Khi code phải xác nhận lại trước khi thêm.

**Lỗi ERP cần tránh khi port báo cáo:** `AnalysisProfitContractService::render` đọc `$collection->discount_value`, nhưng câu query đặt alias là `value_discount` (dòng 97, 249). Kết quả là giảm giá dòng dịch vụ không được trừ (đã kiểm thêm model không có accessor nào bù). HRM phải tính đúng. Theo quy tắc port, lỗi này cũng cần sửa ở ERP, nhưng để task riêng.

## 5. Thiết kế

### 5.1 Lối vào

- URL giữ `/assign/contracts/:id/support-accounting`, trang đổi thành màn Duyệt. Không đổi URL để không gãy liên kết cũ.
- Danh sách: action Duyệt đi thẳng tới màn Duyệt.
- Chi tiết: một nút **Duyệt** duy nhất (khi `is_can_approve`) chuyển sang màn Duyệt. Bỏ Duyệt thẳng, Chuyển duyệt BGĐ và Không duyệt khỏi chi tiết.
- Thông báo chờ duyệt (`ContractNotificationService`, hiện trỏ về chi tiết): đổi `url` sang màn Duyệt với các sự kiện chờ duyệt.
- Giữ nút xem HTHT ở chi tiết. Người không duyệt mở màn ở chế độ chỉ xem.
- Người lập mở màn này khi HĐ Không duyệt có ý kiến Pháp chế: chi tiết có nút **Xem ý kiến cần sửa**.

### 5.2 Bố cục và tab theo vai

Theo mockup: tiêu đề `Duyệt hợp đồng: <mã> (<trạng thái>)`, tab bên trái, panel phải, thanh nút cố định dưới.

| Vai | Tab mở đầu | Tab được xem | Nút |
|---|---|---|---|
| TP | HTHT (sửa được) | HTHT, Bản in, Lãi lỗ | Duyệt, Chuyển duyệt BGĐ, Không duyệt |
| Pháp chế | Bản in | Chỉ Bản in | Còn ý kiến chưa đạt: Trả lại sửa (n). Hết: Duyệt, Chuyển duyệt BGĐ, Không duyệt |
| BGĐ | HTHT (sửa được) | HTHT, Bản in, Lãi lỗ | Duyệt, Không duyệt |
| Người lập (Không duyệt) | Bản in | Chỉ Bản in | Sửa hợp đồng, Gửi duyệt lại |
| Người xem khác | HTHT | Như quyền hiện có, không có nút | Quay lại |

- Cổng `is_bgd_required` giữ nguyên: dính ĐK BGĐ thì ẩn Duyệt, chỉ còn Chuyển duyệt.
- Tab Lãi lỗ theo D13, luôn cần quyền **Xem giá vốn hàng hoá**. Dải tóm tắt hiệu quả + cơ cấu giá trị trên tab HTHT cũng ẩn khi `can_view_full = false`.
- Panel: khách hàng, Chi tiết (mở thêm), giá trị sau thuế, gửi duyệt (`submitted_at`) + đã chờ, người lập, tuyến duyệt. Trạng thái thu gọn nhớ theo trình duyệt (localStorage `duyet-hd-panel`).
- Tuyến duyệt không hiện bước Pháp chế khi `need_legal_approval = 0` ("Không cần"), bước BGĐ theo điều kiện.

### 5.3 BE luồng duyệt

- `POST /{id}/approve`: thêm `note` (nullable, tối đa 255). `ContractService::approve` truyền `note` vào `transition`.
- HTHT: `calculate` chạy ở bước `tp` **và** bước `bgd`, cùng transaction với duyệt như hiện tại. Bước `legal` không ghi HTHT.
- **Nguồn số của màn HTHT** (bắt buộc làm cùng việc trên, nếu không BGĐ bấm Duyệt sẽ ghi đè số TP bằng số mặc định):
  - Bước `tp`: tính lại từ quy chế như hiện tại. Lượt gửi lại cũng vậy, vì HĐ có thể đã đổi. Tương đương việc ERP xoá HTHT khi Không duyệt mà không đụng HD-Q5.
  - Bước `bgd`: nạp số TP đã lưu làm giá trị đầu form, tính xem trước trên đó.
  - Chỉ xem (đã duyệt, Pháp chế, người khác): hiện số đã lưu, không tính lại. Chưa có HTHT lưu thì hiện số tính từ quy chế.
  - `computePreview` và cách FE nạp form phải đổi. Số đã lưu cũng là mốc so sánh cho `keyChanged`.
- `POST /{id}/transfer-bgd`: `note` thành bắt buộc, FE và BE cùng chặn.
- `POST /{id}/submit`: thêm `note` (nullable, tối đa 255), dùng cho Gửi duyệt và Gửi duyệt lại.
- Thêm lý do `regulation_changed` ("Đổi tỷ lệ / thưởng so với quy chế") vào `composeBgdReasons`, so HTHT với quy chế. Không có bước Pháp chế: TP chỉ còn Chuyển duyệt BGĐ. Có bước Pháp chế: TP vẫn Duyệt, lý do xét ở bước Pháp chế từ HTHT đã lưu, Pháp chế chỉ còn Chuyển duyệt BGĐ. Người có quyền BGĐ được Duyệt thẳng như cũ.
- Bổ sung các chặn và xác nhận ở mục 4. Quy tắc chặn phải có ở BE. Câu hỏi xác nhận (thưởng vượt quy chế, ngoài thị trường) ở FE, BE nhận cờ đã xác nhận.
- FE `isPreview` đổi thành: không có `is_can_approve`, hoặc `approval_step` khác `tp` và `bgd`.

### 5.3a Sửa số liệu HTHT giữa TP và BGĐ (khảo sát 06/11 bằng đọc code ERP, user chốt tuân thủ ERP)

Theo ERP:
- TP và BGĐ sửa cùng một bộ ô. Khác nhau ở ràng buộc và cách hiện.
- Ô số (nguồn vốn, 14.1, 16, chi phí thực hiện): một ô, BGĐ thấy số TP và sửa đè.
- Ô % của phòng: TP có cột Quy chế / Đề xuất. Sau khi chuyển, BGĐ có Quy chế / Đề xuất (số TP, chỉ đọc) / Duyệt (sửa được).
- TP không có quyền BGĐ: đổi 1 trong 5 tỷ lệ của phòng chính (20.1, 20.2, 21.2.1.1 đến 21.2.1.3) hoặc đổi 14.1 thì không Duyệt được, phải chuyển duyệt. %DS (19) và phân chia thưởng HĐ (21.1.x) đổi vẫn Duyệt được.
- BGĐ không bị chặn vì đổi tỷ lệ. Thưởng 14.1 vượt % công ty thì phải xác nhận.
- Áp cho cả hai: phải có quy chế cho mọi phòng, tổng %DS = 100, tổng phân chia = 100, đổi 14.1 thì mục 15 phải bằng 0, 14.1 không vượt trần. 20.1 hoặc 20.2 bằng 0 chỉ tô đỏ ô, KHÔNG chặn (đính chính 06/11: bản trước ghi nhầm là chặn).
- Chuyển duyệt lưu HTHT dạng Đề xuất (`status` 1, detail type 2). Duyệt cuối lưu dạng Đã duyệt (`status` 2, detail type 3) và xoá dòng Đề xuất.
- HRM giữ dòng Đề xuất khi duyệt cuối (D16), `calculate` không xoá type 2 của lần đó.

HRM phải đổi:
- `transferBgd` đang gọi `calculate(..., true)` nên số TP lưu thành Đã duyệt, BGĐ không có cột Đề xuất. Đổi thành lưu Đề xuất.
- D11: TP Duyệt sang Pháp chế cũng lưu Đề xuất, vì chưa phải duyệt cuối. Pháp chế duyệt cuối (không qua BGĐ) phải chuyển HTHT thành Đã duyệt từ số đã lưu. TP Duyệt cuối (không Pháp chế) lưu Đã duyệt như hiện tại.
- Thêm cột Quy chế / Đề xuất / Duyệt cho ô % trên màn HTHT, theo `department-main.blade.php`.
- Ô 14.1: ERP tự kéo về trần. HRM báo lỗi dưới ô, giữ số user nhập (quy tắc form). BE vẫn chặn.
- Nơi đọc HTHT (grep 06/11): `ProductExportPostingService`, `ProductImportAccountingService`, `FirmContractServiceAccountingPostingService`, `BorrowSellPostingService` không lọc theo `status` hay detail type, chỉ đọc cột trên HTHT và `departments.employees`. Bảng detail chỉ đọc qua relation `details`, chưa thấy nơi dùng. Còn `ProductImportRequestService`, `BorrowSellRequestService` chưa rà, phải kiểm ở GĐ 1.

### 5.4 Lịch sử duyệt

Không thêm bảng. Thêm vào `DetailContractResource` trường `approval_history` từ `hrm_contract_histories`:
- Chỉ lấy action: `submit, approve, legal_approve, bgd_approve, reject, transfer_bgd, cancel_approve`.
- Sắp theo `id` (nhiều dòng trùng giây, không dùng `created_at`).
- Số lần gửi = đếm dòng `submit` tính tới dòng đó. Không thêm cột.
- Mỗi dòng: `round, step (creator|tp|legal|bgd), action, action_label, actor_name, created_at, note, opinions`.
- `reject` có `step` lấy từ `from_status`.
- `opinions`: danh sách ý kiến Pháp chế chụp vào `meta` lúc trả lại, nên về sau đọc đúng nội dung lúc đó dù ý kiến đã đổi trạng thái. `transition` cần nhận thêm `meta`.

FE theo mockup:
- Dưới mỗi bước trên tuyến hiện ý kiến mới nhất của bước đó (trừ bước đang chờ và bước Lập), tối đa 3 dòng. Ý kiến của lần cũ ghi "Lần 1, không duyệt:". Không duyệt nền đỏ.
- Nút **Lịch sử duyệt (n)** hoặc bấm vào ý kiến: mở ngăn kéo phải 384px. Chia theo lần, mới nhất ở trên, có dòng đang chờ. Không che thanh nút. Esc đóng, trả focus về nút.
- Panel thu gọn: còn icon + số lượt.

Ai xem được màn Duyệt thì đọc được toàn bộ lịch sử, gồm Người lập. Ý kiến có thể chứa số tiền nên lịch sử phải theo cùng cổng ẩn giá: `hide_price` thì không trả `note` (tab Lịch sử chi tiết hiện đang trả, sửa luôn).

### 5.5 Ý kiến Pháp chế trên bản in

**Bảng mới `hrm_contract_legal_notes`** (migration duy nhất của phase):
`id, contract_id, round, quote (text, null = ý kiến chung), quote_before (varchar 80), quote_after (varchar 80), note (text), status (1 Cần sửa, 2 Đã sửa, 3 Đạt), reply (text), created_by, fixed_by, fixed_at, closed_by, closed_at, timestamps`. Index `contract_id`.

**Vòng đời**
1. Pháp chế bôi đen đoạn trên bản in hoặc thêm Ý kiến chung, ghi nội dung. Xoá được khi còn Cần sửa.
2. Còn ý kiến khác Đạt thì Pháp chế không Duyệt được, chỉ Trả lại sửa (gọi `reject`, chụp ý kiến vào `meta`).
3. Người lập sửa, bấm **Đã sửa** ở từng ý kiến (phản hồi không bắt buộc). Còn Cần sửa thì không Gửi duyệt lại được (chặn ở BE).
4. HĐ đi lại từ TP. Tới Pháp chế: ý kiến Đã sửa bấm **Đạt** hoặc **Chưa đạt** (về Cần sửa). Có thể thêm ý kiến mới.
5. Hết ý kiến chưa Đạt thì Duyệt / Chuyển duyệt BGĐ.

**Gắn lại vị trí:** ý kiến lưu theo chữ chứ không theo toạ độ, vì nội dung và ngắt trang đều đổi. Sau khi chia tờ, tìm `quote`, nếu nhiều chỗ khớp thì so `quote_before` / `quote_after`. Đoạn nằm vắt qua 2 tờ phải vẫn tìm được. Không tìm thấy (người lập đã sửa đoạn đó): ý kiến vẫn ở danh sách, ghi "Đoạn đã thay đổi", kèm chữ gốc. Ghim ý kiến dùng `position:absolute`, không được làm đổi layout.

**Người lập sửa ở đâu:** ở form Sửa hợp đồng, tab Mẫu in như hiện tại (HĐ Không duyệt đã sửa được). Mockup hiện chỉ minh hoạ, không phải sửa trực tiếp trên tờ.

**So với mẫu gốc:** Pháp chế bật xem phần khác mẫu gốc, dùng lại `POST assign/contracts/template-diff` (`ContractTemplateDiffService`).

### 5.6 Bản in theo tờ

- Dữ liệu từ `GET /{id}/print-data`, mode `contract`, bản Tổng hợp (không gửi `group`), không đổi BE. Ý kiến Pháp chế gắn trên bản này. Không gồm phụ lục (D15).
- Thư viện Paged.js 0.4.3 (MIT), đặt tệp ở `static/pagedjs/` và nạp khi mở tab, giống cách `static/ckeditor`. Tránh qua webpack của Nuxt 2 / node 12.
- Component mới `components/print/ContractPagedView.vue`: chia tờ, pager Trang x/y, zoom − % + (50–200%, bấm % về vừa khung, giữ trang đang xem), In.
- In dùng chính các tờ này (`@page A4 12mm 10mm`). Mức zoom không ảnh hưởng bản in.
- Nút In hợp đồng ở chi tiết dùng cùng cách chia tờ (D14): sửa `contractPrintMixin` / `ReportPrintPreviewModal` chỉ cho mode hợp đồng, giữ QR và `markSignatureSpace`. Kiểm lại các chế độ in của hợp đồng. `ReportPrintPreviewModal` dùng chung, nên phải hỏi trước khi sửa và các màn khác không được đổi.
- Người lập có ô ngắt trang trước Điều: trong mockup chỉ để minh hoạ, phase này **không làm** (cần cột lưu và đụng mẫu in, thuộc việc soạn kiểu Word).

Các bẫy đã gặp ở bản thử (chi tiết trong `plan.md`), phải giữ khi code: gốc CSS in là `.pagedjs_page_content`; `break-after: avoid` không tác dụng nên tự dò tiêu đề cuối trang; lặp thead bằng Handler `renderNode` (`afterPageLayout` đẩy cuối tờ vào cột ẩn); chia lại phải `removeListeners`; override `text-align-last`.

### 5.7 Tab Phân tích lãi lỗ

`GET /{id}/profit-analysis`, service mới `ContractProfitAnalysisService`, trả các dòng hàng + dịch vụ của 1 HĐ và dòng tổng. 15 cột như ERP: STT, Mã, Tên, ĐVT, SL, Đơn giá HĐ, Đơn giá bán sau giảm, Đơn giá net, Đơn giá vốn, Thành tiền HĐ, bán, net, vốn, Chênh lệch (Bán − Net), Lãi lỗ (Bán − Vốn).

Công thức theo ERP, mỗi dòng:
- `sau_vượt = giá + vượt trội`; `giảm_trên_giá = giá / sau_vượt × giảm`; `bán = giá − giảm_trên_giá`.
- `net = giá − giá × sale_max_percent / 100`.
- Vốn hàng: giá nhập gần nhất của hàng ở công ty × hệ số ĐVT, không có thì giá vốn công ty. Vốn dịch vụ: `giá × rate_value_capital / 100`.
- Thành tiền = đơn giá × SL. Chênh lệch `(bán − net) × SL`. Lãi lỗ `(bán − vốn) × SL`.

Nguồn HRM: `ContractProductPrice` dòng cha và `ContractServiceItem`. Ánh xạ cột do builder đối chiếu, số liệu phải khớp cách ERP cho cùng dữ liệu, trừ lỗi đã nêu ở mục 4. Báo cáo chạy theo dữ liệu HĐ hiện tại, không lưu lại.

Điểm lệch ERP (07/11, user đã chốt từng điểm):
- Không có dòng Chi phí vận chuyển. ERP chỉ có dòng này sau khi HĐ Có hiệu lực và mở yêu cầu hạch toán vận chuyển, nên ở bước TP / BGĐ hai bên khớp, về sau mới lệch. **User chốt 07/11: giữ không có dòng (hướng A), không thêm dòng ghi chú.** Lý do: dòng ERP lấy từ `firm_contract_costs` (cost id 72) chỉ được tạo khi người lập mở form yêu cầu hạch toán vận chuyển (GET `getDataForServiceExport` có ghi DB), vốn = 0 vì cost 72 không có `rate_value_capital`, giảm giá không trừ ⇒ cả phí thành lãi; rehearsal 1.320/1.964 HĐ có phí có dòng. Hệ quả chấp nhận: tổng cột Giá HĐ thấp hơn tổng HĐ đúng bằng phí vận chuyển.
- Giá nhập gần nhất và % chiết khấu dịch vụ lấy theo công ty của HĐ. **User chốt 07/11: giữ (hướng A).** Khớp ERP khi mở báo cáo từ màn duyệt/HTHT (link gắn `company_id` = công ty HĐ) với người có quyền Tổng công ty; lệch khi ERP mở từ menu không lọc công ty (rehearsal 46.634/117.729 dòng hàng) hoặc người xem cấp Công ty đang ở công ty khác. % chiết khấu dịch vụ: ERP theo công ty gốc người lập, rehearsal 115 HĐ khác công ty nhưng 0 HĐ ra số khác.
- Chỉ lấy dòng cha. **User chốt 07/11 (hướng B, đã code 07/11): vốn dịch vụ = `estimated_price × qty` của dòng HĐ, thống nhất Phase 25 D7, thay cho `rate_value_capital` của ERP.** Lý do: HĐ 734 theo % danh mục vốn DV 4.000.000, theo đơn giá dự toán 7.000.000 ⇒ tab báo lãi DV 3.000.000 trong khi số ghi sổ 632 là lãi 0. Hệ quả chấp nhận: lệch báo cáo ERP; dòng chưa nhập đơn giá dự toán ra vốn 0.
- Dòng dịch vụ có `estimated_price` ≤ 0 ⇒ `cost_missing` = true ("Chưa có vốn"), vốn tính 0. **User chốt 07/11 (hướng A, đã code 07/11)**: cột NOT NULL mặc định 0, không phân biệt chưa nhập với vốn 0 thật; chấp nhận cảnh báo nhầm cho dịch vụ vốn 0 thật. Thay quy tắc cũ (chỉ thiếu khi `rate_value_capital` null).
- HĐ Đang tạo (status 3): `canView` trả false ⇒ ẩn tab, API 403. **User chốt 07/11 (hướng B, đã code 07/11)**, khớp ERP `fc.status != DANG_TAO`. Trước đó UI không có đường vào, chỉ lọt qua URL/API với người có quyền báo cáo.

Khi deploy phải chạy `permission:catalog-sync` (mã báo cáo `on_hrm` 0 → 1). `permission:sync` đã gỡ. `catalog-sync --dry-run` chạy lệnh ghi rồi rollback.

Cổng: BE `/profit-analysis` kiểm D13 và trả 403 nếu không đạt, không chỉ ẩn tab ở FE. Mở quyền báo cáo cho HRM: sửa catalog quyền theo skill `permission-seeder` (thêm `hrm` vào `platforms`), làm ở GĐ 5. Kiểm cả ca có quyền và không quyền.

### 5.8 Quy ước phải theo khi code

- Thanh nút dùng `V2Footer` + slot `#custom-actions`. Popup dùng `V2BaseModal`, xác nhận dùng `$confirm`. Ô nhập mới dùng `V2Base*`, ô tiền `V2BaseCurrencyInput`.
- Duyệt / Chuyển duyệt / Không duyệt / Gửi duyệt lại xong thì về màn danh sách (`support-accounting.vue` hiện đẩy về chi tiết, phải đổi). Quay lại trỏ về nơi user đi vào.
- Nút chưa dùng được thì ẩn hẳn, không disable. Hành động ở danh sách và chi tiết phải khớp nhau.
- Chữ đỏ chỉ dành cho lỗi validate. Không duyệt trong lịch sử chỉ dùng icon + viền + nền nhạt, chữ giữ màu thường.
- Ý kiến trên bản in là bảng mới: model `extends BaseModel`, có `created_by`, `updated_by`. Nhãn nút "Gửi duyệt" theo `button-convention` (chi tiết hiện ghi "Trình duyệt", cấm dùng, đổi luôn).
- Thông báo mới (trả lại sửa, đã sửa) theo `notification-convention`.
- Tài liệu giữ ở `.plans/hop-dong/` cùng các phase trước, dù nhánh là con của `gop_db`.

## 6. Quyết định của Claude (user kiểm khi đọc)

- C1 Giữ URL `support-accounting`, không tạo route mới.
- C2 Ghi chú Duyệt / Gửi duyệt tối đa 255 ký tự, cùng mức Không duyệt và Chuyển BGĐ.
- C3 Số lần gửi tính từ dòng `submit`, không thêm cột.
- C4 Tệp Paged.js đặt ở `static/`, không thêm vào `package.json`.
- C5 Có ý kiến chưa Đạt thì `need_legal_approval` không được tắt, kể cả khi người lập khôi phục mẫu gốc. Tránh việc né bước kiểm lại.
- C6 Không làm ô ngắt trang tay ở phase này.
- C7 Bước Không duyệt của TP / BGĐ không bắt buộc có ý kiến trên bản in, chỉ cần lý do.
- C8 Kịch bản mockup đổi thành một hồ sơ liền mạch (Pháp chế lần 1 → Người lập → TP lần 2 → BGĐ), tên Pháp chế và ý kiến là dữ liệu mẫu.

## 7. Câu hỏi chờ user

Đã chốt hết (D11–D18, 06/11). Builder check nêu 6 điểm, đã tự kiểm lại trong code: nguồn số HTHT và Không duyệt giải quyết ở mục 5.3, các điểm còn lại user chốt.

## 8. Chia giai đoạn

| GĐ | Nội dung | Repo | DB |
|---|---|---|---|
| 1 | BE luồng: ghi chú, BGĐ ghi HTHT, chặn theo ERP, `approval_history` | hrm-api | Không |
| 2 | FE khung màn Duyệt: lối vào, panel, tab, thanh nút, lịch sử, ô % phòng | hrm-client | Không |
| 3 | Bản in theo tờ + zoom | hrm-client | Không |
| 4 | Ý kiến Pháp chế | cả 2 | 1 migration `hrm_contract_legal_notes` |
| 5 | Tab Phân tích lãi lỗ | cả 2 | Không |

## 9. Kiểm thử

- BE: mỗi bước đúng người / sai người / không quyền. BGĐ sửa HTHT rồi duyệt: số đã lưu bằng số xem trước. Chuyển duyệt thiếu ghi chú bị chặn. Còn ý kiến chưa Đạt: Pháp chế không Duyệt được, người lập không gửi lại được. `approval_history` đúng số lần qua 2 vòng. `hide_price` không trả ý kiến.
- Báo cáo: HĐ 734 đối chiếu tay với công thức, có dòng dịch vụ giảm giá.
- FE: Playwright đo DOM ở 1440 và 1366; so số tờ giữa xem trước và PDF; so toàn văn không mất / lặp chữ; có quyền và không quyền cho từng tab; 2 vòng trả lại với đoạn đã bị sửa.
- Chưa kiểm ở bản thử: Windows / font khác, Safari / Firefox, Nuxt 2 thật, ô bảng dài hơn 1 trang. Phải kiểm ở GĐ 3.
- Dữ liệu thử: DB `hrm_erp_rbac_rehearsal`, HĐ 734, tài khoản namdangit. Role tạm `ZZDEV-BGD-duyet-HD` gỡ khi xong.
