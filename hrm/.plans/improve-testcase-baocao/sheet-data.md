# Nội dung mô tả 10 sheet báo cáo (end-user friendly)

> Tổng hợp từ 10 Explore agent đọc BE/FE/plan tương ứng từng báo cáo. Dùng làm dữ liệu nguồn cho script `tools/improve_testcase_baocao.py`. Người dùng review file này trước khi chạy script.

---

## Sheet 17 — BC Theo dõi meeting theo dự án

1. **Mục đích báo cáo:** Thống kê các cuộc họp đã hoàn thành theo từng dự án tiềm khả thi (TKT), giúp lãnh đạo nắm được khối lượng meeting (số lượng, thời lượng, loại, hình thức, số người tham gia) của mỗi dự án.
2. **Đối tượng được tính:** Chỉ tính các cuộc họp đã hoàn thành (đã diễn ra) thuộc các dự án TKT đã được khởi động.
3. **Đối tượng bị ẩn:** Dự án ở trạng thái "Đang tạo" (bản nháp); cuộc họp ở trạng thái "Đang tạo / Lên lịch / Đã chốt lịch / Đang diễn ra / Đã huỷ"; dự án không có meeting nào.
4. **Bộ lọc thời gian áp dụng cho:** Ngày họp thực tế (ngày cuộc họp diễn ra), KHÔNG phải ngày tạo lịch họp hay ngày tạo dự án. Có 3 chế độ: Tuỳ chọn (từ-đến), Tháng/Năm, Năm.
5. **Cấu trúc cây phân cấp:** Công ty → Phòng ban → Dự án TKT → Cuộc họp.
6. **Quy tắc cộng dồn cấp cha:** Số meeting + tổng thời lượng (phút) = cộng dồn từ các meeting con. Hình thức (Trực tiếp/Online) + Loại meeting = đếm số meeting theo từng loại/hình thức. Số người tham gia = đếm UNIQUE theo nhân viên (1 nhân viên dự nhiều meeting chỉ tính 1 lần). Dòng cấp meeting thì là tổng số người dự cuộc họp đó (gồm cả khách ngoài).
7. **Phân quyền cấp:**
   - "Xem theo tổng công ty" — toàn bộ dữ liệu, không giới hạn công ty.
   - "Xem theo công ty" — chỉ dự án thuộc công ty hiện tại của user (+ dự án mình tạo).
   - "Xem theo phòng ban" — chỉ dự án thuộc phòng ban của user (+ dự án mình tạo).
   - Không có quyền nào — chỉ dự án mình tạo hoặc mình là nhân viên kinh doanh phụ trách.
8. **Ghi chú đọc bảng:** Phân trang theo cuộc họp (30 meeting/trang), không phải theo dự án. Các thống kê tổng ở cấp cha + dưới bảng tính từ TOÀN BỘ kết quả sau filter, không phụ thuộc trang đang xem. Click chip Loại/Hình thức/Số người tham gia ở cấp cha → mở modal danh sách chi tiết.

### TC cần giải thích nghiệp vụ
- **Lọc thời gian (TC-ROLE-23/24):** Bộ lọc thời gian lọc theo NGÀY HỌP THỰC TẾ, không phải ngày tạo lịch họp. Ví dụ: chọn 01/01–31/03 → chỉ thấy meeting đã họp trong quý 1, kể cả lịch tạo từ tháng trước.
- **Đếm unique người tham gia (TC-ROLE-19, TC-ROLE-21, TC-ROLE-35):** Ở dòng Phòng ban/Công ty, "Số người tham gia" đếm UNIQUE — 1 nhân viên dự 5 meeting chỉ tính 1 người. Ở dòng meeting thì là tổng số người dự cuộc họp đó, gồm cả khách ngoài.
- **Ẩn dự án trạng thái Đang tạo (TC-ROLE-09):** Dự án ở trạng thái "Đang tạo" (bản nháp, NVKD chưa khởi động) không xuất hiện trong báo cáo.
- **Phân quyền phòng ban null (TC-ROLE-04):** User có quyền "Xem theo phòng ban" nhưng phòng ban của user là null sẽ không thấy dữ liệu nào, trừ dự án mình tự tạo.
- **Thống kê tổng dưới bảng (TC-ROLE-08):** Khu vực tổng dưới bảng (Tổng dự án, Tổng cuộc họp, Tổng KH, Tổng thời lượng) là tổng của TOÀN BỘ kết quả sau filter, không bị phân trang ảnh hưởng.

---

## Sheet 18 — Báo cáo thời gian meeting theo nhân viên

1. **Mục đích báo cáo:** Thống kê thời gian họp của từng nhân viên (số cuộc họp, tổng thời lượng, loại, hình thức), phân cấp Công ty → Phòng ban → Nhân viên, giúp đánh giá khối lượng họp hành.
2. **Đối tượng được tính:** Cuộc họp đã hoàn thành có ít nhất 1 nhân viên công ty tham gia.
3. **Đối tượng bị ẩn:** Cuộc họp ở trạng thái khác Đã hoàn thành (Đang tạo / Lên lịch / Đang diễn ra / Đã huỷ); cuộc họp không có nhân viên công ty tham gia (chỉ có khách ngoài); nhân viên không thuộc phạm vi quyền của user.
4. **Bộ lọc thời gian áp dụng cho:** Ngày họp thực tế (ngày cuộc họp diễn ra), không phải ngày tạo lịch. Có 3 chế độ: Tuỳ chỉnh, Tháng/Năm, Năm.
5. **Cấu trúc cây phân cấp:** Công ty → Phòng ban → Nhân viên → Cuộc họp.
6. **Quy tắc cộng dồn cấp cha:** Tổng cuộc họp + tổng thời lượng = cộng dồn từ cấp con. Số người tham gia cấp cha = đếm UNIQUE (1 nhân viên dự 5 meeting chỉ tính 1 lần). Dòng meeting = tổng số người dự cuộc họp (gồm khách ngoài).
7. **Phân quyền cấp:**
   - "Xem theo tổng công ty" — tất cả meeting mọi công ty.
   - "Xem theo công ty" — chỉ meeting của nhân viên cùng công ty mình.
   - "Xem theo phòng ban" — chỉ meeting của nhân viên cùng phòng ban.
   - Không có quyền — chỉ meeting mà chính user tham gia.
8. **Ghi chú đọc bảng:** Thống kê tổng dưới bảng là tổng sau filter, không phụ thuộc trang đang xem. Danh sách meeting sắp xếp theo ngày họp giảm dần.

### TC cần giải thích nghiệp vụ
- **Phân quyền (TC-ROLE-01):** User có quyền "Xem theo tổng công ty" thấy meeting toàn bộ công ty; user không có quyền này chỉ thấy công ty hiện tại.
- **Lọc thời gian:** Lọc theo ngày họp thực tế, không phải ngày tạo lịch. Ví dụ: lịch tạo tháng 12/2025 nhưng họp 05/01/2026 → filter quý 1/2026 sẽ thấy.
- **Đếm unique người tham gia:** Dòng Phòng ban — 1 nhân viên dự 5 meeting = 1 người. Dòng meeting — tổng số người dự (gồm khách).
- **Pagination + thống kê tổng:** Trang 1 hiện 30 meeting đầu; "Tổng" luôn tính toàn bộ kết quả (mọi trang), không chỉ trang hiện tại.

---

## Sheet 23 — BC theo dõi làm giải pháp theo phòng kinh doanh

1. **Mục đích báo cáo:** Thống kê các yêu cầu làm giải pháp (YCGP) theo Công ty → Phòng KD → Nhân viên kinh doanh, theo dõi tiến trình xử lý từ lúc gửi yêu cầu đến khi chốt giải pháp.
2. **Đối tượng được tính:** Tất cả yêu cầu làm giải pháp đã được gửi đi (gồm các trạng thái: Chờ tiếp nhận, Đã tiếp nhận, Đang thực hiện, Đã hoàn thành, Đã chốt giải pháp).
3. **Đối tượng bị ẩn:** YCGP ở trạng thái "Đang tạo" (bản nháp NVKD chưa gửi); YCGP ở trạng thái "Từ chối" hoặc "Đóng" (đã kết thúc, không còn xử lý).
4. **Bộ lọc thời gian áp dụng cho:** Ngày gửi yêu cầu (ngày NVKD bấm gửi YCGP), không phải ngày tạo dự án hay ngày tiếp nhận. Ví dụ: chọn 01/01–31/03 → chỉ thấy YCGP được gửi trong quý 1.
5. **Cấu trúc cây phân cấp:** Công ty → Phòng kinh doanh (phòng tiếp nhận làm giải pháp) → Nhân viên kinh doanh (người tạo YC) → Yêu cầu giải pháp.
6. **Quy tắc cộng dồn cấp cha:** Cấp Công ty = tổng số phòng + nhân viên + YC trong công ty. Cấp Phòng = tổng số nhân viên + YC. Cấp NV = số YC do nhân viên đó tạo. Đếm nhân viên ở cấp phòng = UNIQUE (1 nhân viên có 10 YC vẫn tính 1 người).
7. **Phân quyền cấp:**
   - "Tổng công ty" — toàn bộ YCGP mọi công ty.
   - "Công ty" — chỉ YCGP của nhân viên cùng công ty.
   - "Phòng ban" — chỉ YCGP của nhân viên cùng phòng ban.
   - Không có quyền — chỉ YCGP do chính user tạo.
8. **Ghi chú đọc bảng:** Click chip "Cơ cấu" ở cột "Tiến trình YC" để mở popup biểu đồ phân tích trạng thái. Click mũi tên expand/collapse từng cấp. Mỗi YC có thể xem chi tiết: KH, dự án, người tiếp nhận, PM.

### TC cần giải thích nghiệp vụ
- **Phân quyền các cấp (TC-ROLE-01/02/03):** Tổng công ty = thấy tất cả; Công ty = cùng công ty (mọi phòng); Phòng ban = cùng phòng (không thấy phòng khác kể cả cùng công ty).
- **Lọc thời gian (TC-FILTER-TIME):** Lọc theo NGÀY GỬI yêu cầu, không phải ngày chuyển trạng thái. YC tạo 01/01 nhưng tiếp nhận 15/01 vẫn xuất hiện ở filter từ 01/01.
- **Đếm unique nhân viên (TC-COUNT):** Dòng phòng "số người tham gia" = số nhân viên DISTINCT có tạo YC (1 NV có 10 YC = 1 người). Dòng YC thì hiện số lượng YC của NV đó.

---

## Sheet 24 — BC tổng hợp Dự án TKT theo Phòng ban / Nhân viên

1. **Mục đích báo cáo:** Theo dõi khối lượng và trạng thái dự án tiềm khả thi (TKT) mỗi nhân viên kinh doanh đang quản lý, đánh giá hiệu suất phát triển cơ hội theo phòng ban và cá nhân.
2. **Đối tượng được tính:** Dự án TKT đã được khởi động (trạng thái từ "Thu thập thông tin dự án" đến "Kết thúc và lưu trữ"). NVKD phụ trách = người được gán là nhân viên kinh doanh chính của dự án, hoặc người tạo nếu chưa gán.
3. **Đối tượng bị ẩn:** Dự án ở trạng thái "Đang tạo" (bản nháp); dự án không thuộc phạm vi quyền của user.
4. **Bộ lọc thời gian áp dụng cho:** Ngày tạo dự án TKT. Hỗ trợ: Năm / Quý / Tháng / khoảng ngày tuỳ chọn.
5. **Cấu trúc cây phân cấp:** Công ty → Phòng ban → Nhân viên kinh doanh. Mỗi NVKD trên 1 dòng.
6. **Quy tắc cộng dồn cấp cha:** Phòng ban = tổng dự án + giải pháp + chốt giải pháp của các NV trong phòng. Công ty = tổng các phòng. Số nhân viên cấp phòng/công ty = UNIQUE NVKD. Tỷ lệ chốt giải pháp = (số GP chốt) / (số GP đã làm) × 100 ở từng cấp — tính theo TỔNG, không phải trung bình tỷ lệ cá nhân.
7. **Phân quyền cấp:**
   - "Tổng công ty" — tất cả dự án.
   - "Công ty" — dự án thuộc công ty được chọn.
   - "Phòng ban" — dự án cùng phòng.
   - Không có quyền — chỉ dự án mình tạo hoặc mình là NVKD.
8. **Ghi chú đọc bảng:** Bảng có 9 nhóm cột song song: Số lượng dự án + Cơ cấu trạng thái, Cấu trúc ngành/giải pháp/ứng dụng, Giải pháp đã làm + chốt + tỷ lệ, Báo giá, Hợp đồng. Click số bất kỳ → modal danh sách dự án chi tiết kèm status + giải pháp gần nhất.

### TC cần giải thích nghiệp vụ
- **Phân quyền phòng ban (TC-ROLE-01):** User có quyền phòng ban chỉ thấy cây Công ty → Phòng ban của mình + NVKD trong phòng; không thấy phòng khác kể cả cùng công ty.
- **Lọc theo năm (TC-TIME-01):** Chọn "Năm 2025" → chỉ tính dự án TẠO trong 01/01/2025–31/12/2025, kể cả đã hoàn thành/đóng. Dự án tạo năm 2024 không xuất hiện.
- **Tỷ lệ chốt giải pháp cấp phòng (TC-MERGE-01):** Tỷ lệ chốt = (số GP chốt được) / (số GP đã làm) × 100. Dòng phòng lấy TỔNG GP của tất cả NVKD chia tổng đã làm, KHÔNG lấy trung bình tỷ lệ cá nhân.

---

## Sheet 30 — BC hiệu suất nhân viên theo dự án

1. **Mục đích báo cáo:** Đánh giá hiệu suất làm việc của nhân viên trong các dự án theo: số task hoàn thành đúng/trễ hạn, tỷ lệ hoàn thành, hiệu suất giờ (giờ thực tế so với giờ được giao).
2. **Đối tượng được tính:** Tất cả task đã được gán cho nhân viên ở trạng thái "Đã hoàn thành" (DONE) hoặc "Chờ duyệt" (REVIEW), kể cả task phòng ban / dự án / hạng mục giải pháp.
3. **Đối tượng bị ẩn:** Task chưa hoàn thành (trừ task quá hạn); task chưa có người gán; nhân viên không có task trong kỳ; dự án không thuộc phòng ban được lọc.
4. **Bộ lọc thời gian áp dụng cho:** Ngày bắt đầu dự án, không phải ngày hoàn thành task. Có 3 chế độ: Tuỳ chỉnh, Tháng cố định, Năm cố định.
5. **Cấu trúc cây phân cấp:** Phòng ban → Nhân viên → Dự án → Task chi tiết.
6. **Quy tắc cộng dồn cấp cha:** Tổng task + giờ giao + giờ thực tế = cộng dồn từ cấp con. Tỷ lệ hoàn thành = (số task done đúng hạn + done trễ hạn) / tổng task × 100. Hiệu suất = giờ thực tế / giờ giao × 100 (null nếu giờ giao = 0).
7. **Phân quyền cấp:**
   - "Tổng công ty" — toàn bộ dữ liệu.
   - "Công ty" — chỉ nhân viên cùng công ty.
   - "Phòng ban" — chỉ nhân viên cùng phòng ban.
   - Không có quyền — chỉ task chính mình.
8. **Ghi chú đọc bảng:** "Hiệu suất (%)" = giờ thực tế / giờ giao × 100. Trên 100% = làm chậm hơn dự kiến. "Hoàn thành đúng hạn" = task kết thúc ≤ hạn chót. Giờ thực tế lấy từ log tiến độ ghi nhận khi báo cáo công việc, không phải giờ ước tính ban đầu.

### TC cần giải thích nghiệp vụ
- **Cấu trúc cây khi NV làm nhiều dự án:** Nếu 1 nhân viên trong 2 dự án cùng hạng mục, kiểm tra cây gộp theo dự án hay theo hạng mục.
- **Cách tính giờ thực tế:** Giờ thực tế là TỔNG giờ ghi nhận trong log tiến độ khi NV báo cáo công việc, không phải giờ ước tính (estimated) cũng không phải duration task.
- **Phân quyền phòng ban:** User phòng A không thấy data phòng B kể cả khi cùng công ty.
- **Task quá hạn chưa hoàn thành:** Task chưa ở trạng thái Done/Review nhưng quá hạn — vẫn được gộp vào "Không hoàn thành".

---

## Sheet 31 — BC hiệu suất làm việc theo giải pháp

1. **Mục đích báo cáo:** Thống kê hiệu suất làm giải pháp theo phòng ban làm GP, so sánh giữa giờ dự toán (kế hoạch) và giờ thực tế (thực hiện).
2. **Đối tượng được tính:** Giải pháp đã được phê duyệt trở lên (đã qua "Nháp"), thuộc dự án TKT đã được khởi động, có hạng mục được phân công nhân lực.
3. **Đối tượng bị ẩn:** GP ở trạng thái "Nháp" (chưa phê duyệt) hoặc "Đóng"; hạng mục không có nhân lực được giao; GP không có dự án TKT hoặc dự án ở trạng thái nháp.
4. **Bộ lọc thời gian áp dụng cho:** Ngày bắt đầu dự án TKT mà giải pháp thuộc về. Ví dụ chọn 01/01–31/03 → chỉ thấy GP thuộc dự án TKT có ngày bắt đầu trong quý 1, bất kể công việc được ghi nhận lúc nào.
5. **Cấu trúc cây phân cấp:** Phòng ban (phòng làm GP) → Giải pháp → Hạng mục (xem trong modal chi tiết).
6. **Quy tắc cộng dồn cấp cha (Phòng ban):** Số hạng mục = tổng hạng mục của các GP trong phòng. Tổng nhân sự = đếm UNIQUE (1 nhân viên tham gia nhiều GP chỉ tính 1). Giờ dự toán + giờ thực tế = cộng đơn giản các GP. Hiệu suất phòng = TRUNG BÌNH CỘNG hiệu suất các GP, KHÔNG tính lại từ tổng giờ.
7. **Phân quyền cấp:**
   - "Tổng công ty" — toàn bộ phòng ban làm GP.
   - "Công ty" — phòng ban làm GP của công ty hiện tại.
   - "Phòng ban" — chỉ phòng của user.
   - "Bộ phận" — chỉ bộ phận của user.
   - Không có quyền — chỉ dữ liệu mình tạo/làm.
8. **Ghi chú đọc bảng:** Dòng phòng ban hiển thị "Hiệu suất trung bình" (TB cộng các GP), không phải tổng. Dòng GP hiển thị "Đã chốt" (xanh) / "Chưa chốt" (đỏ) dựa trên trạng thái dự án TKT — Đã chốt = dự án từ "Thực hiện hợp đồng" trở lên. Click số hạng mục / giờ dự toán / giờ thực tế / hiệu suất ở dòng GP → modal chi tiết hạng mục. Phân trang theo số phòng ban.

### TC cần giải thích nghiệp vụ
- **Hiệu suất % (TC-ROLE-09):** Hiệu suất GP = (Giờ dự toán / Giờ thực tế) × 100. Ví dụ: dự toán 100h, thực tế 80h → 125% (làm nhanh hơn). Dự toán 80h, thực tế 100h → 80% (làm chậm hơn). Nếu giờ thực tế = 0 → 0%.
- **Hiệu suất phòng = TB cộng:** Dòng phòng KHÔNG tính lại từ tổng giờ — mà là TB của các hiệu suất GP. (GP1=125%, GP2=80% → phòng = 102,5%).
- **Chốt HĐ:** "Đã chốt" xanh khi dự án TKT của GP ở trạng thái "Thực hiện hợp đồng" / "Nghiệm thử và thanh lý" / "Đóng dự án".
- **Phân quyền (TC-ROLE-01/02/03/04):** Tổng công ty thấy tất cả; Công ty chỉ thấy công ty mình; Phòng ban chỉ thấy phòng mình.

---

## Sheet 35 — BC theo dõi chỉ số hoàn thành giải pháp theo version

1. **Mục đích báo cáo:** Theo dõi quá trình hoàn thiện kỹ thuật của mỗi giải pháp qua các phiên bản (version) — đánh giá hiệu suất thực hiện, so sánh giờ dự toán với giờ thực tế của từng version.
2. **Đối tượng được tính:** Giải pháp đã phê duyệt (không phải nháp) và các version đã phê duyệt của nó. Task, giờ dự toán, giờ thực tế, nhân sự lấy từ các version này.
3. **Đối tượng bị ẩn:** GP và version ở trạng thái "Tạo nhập" (nháp); task không có giờ giao; nhân sự không có log giờ thực tế.
4. **Bộ lọc thời gian áp dụng cho:** Ngày bắt đầu làm của version. Có 3 chế độ: Tháng (mặc định tháng hiện tại), Năm, Tuỳ chỉnh.
5. **Cấu trúc cây phân cấp:** Công ty → Phòng ban → Giải pháp → Version. ("Version" = mỗi lần GP cần thay đổi lớn, người quản lý tạo phiên bản mới với lịch + nhân sự + task riêng — coi như một "giai đoạn hoàn thiện" của GP.)
6. **Quy tắc cộng dồn cấp cha:** Số task + giờ dự toán + giờ thực tế + số nhân sự + số version = cộng dồn từ con. Hiệu suất (%) + Task/giờ TÍNH LẠI dựa trên tổng số đã dồn, KHÔNG cộng từng phần.
7. **Phân quyền cấp:**
   - "Tổng công ty" — toàn bộ.
   - "Công ty" — chỉ GP cùng công ty.
   - "Phòng ban" — chỉ GP cùng phòng ban.
   - Không có quyền — chỉ GP mà user là PM.
8. **Ghi chú đọc bảng:**
   - Hiệu suất (%) = (Giờ dự toán / Giờ thực tế) × 100. > 100% = làm nhanh hơn dự toán (tốt); < 100% = làm chậm hơn (cần cải thiện); 0% = chưa có giờ thực tế.
   - Task/giờ = số task / giờ thực tế (năng suất).
   - Số ngày thực hiện = Ngày chốt − Ngày bắt đầu.
   - Ngày chốt = ngày phê duyệt version.
   - Mặc định mở dạng thu gọn (chỉ cấp Công ty), bấm "Xem chi tiết" để mở tất cả cấp. Phân trang 15 GP/trang.

### TC cần giải thích nghiệp vụ
- **Filter giải pháp (TC-VERSION-001):** Chọn 1 GP → chỉ thấy các version của GP đó. Cấp phòng vẫn tính tổng các version đã chọn.
- **Công thức hiệu suất (TC-EFFICIENCY-002):** Dự toán 80h, thực tế 100h → 80% (chậm). Dự toán 100h, thực tế 80h → 125% (nhanh).
- **Số ngày thực hiện (TC-TIMELINE-003):** Bắt đầu 01/05, chốt 15/05 → 14 ngày. Nếu chưa chốt thì = 0.
- **Đếm nhân sự (TC-MEMBER-HOUR-004):** Có 3 nhân sự tham gia version nhưng chỉ 2 người log giờ — số nhân sự tham gia = 3, giờ thực tế chỉ từ 2 người.

---

## Sheet 36 — BC tổng hợp giải pháp theo Phòng ban

1. **Mục đích báo cáo:** Theo dõi số lượng, trạng thái, hiệu suất và cơ cấu giải pháp do từng phòng ban + nhân viên kỹ thuật thực hiện; khảo sát tỷ lệ chuyển đổi từ GP sang báo giá → hợp đồng.
2. **Đối tượng được tính:** Giải pháp đã vượt qua trạng thái "Đang tạo" (bản nháp) — kể cả Chốt / Duyệt / Hủy. Mỗi GP gắn 1 kỹ sư chính: leader của hạng mục đầu tiên, hoặc người tạo GP nếu chưa có hạng mục.
3. **Đối tượng bị ẩn:** GP ở trạng thái "Đang tạo" (nháp chưa lưu); GP không có yêu cầu giải pháp hoặc không có nhân viên phụ trách.
4. **Bộ lọc thời gian áp dụng cho:** Ngày tạo GP, không phải ngày phê duyệt hay hoàn thành. Có 3 chế độ: Năm / Tháng–Năm / Tuỳ chọn ngày.
5. **Cấu trúc cây phân cấp:** Công ty → Phòng ban làm GP → Nhân sự kỹ thuật. Có dòng "Tổng toàn bộ giải pháp" ở đầu bảng.
6. **Quy tắc cộng dồn cấp cha:** Dòng phòng/công ty = tổng GP của các lá (nhân viên). Tỷ lệ chốt = (GP chốt) / (GP không nháp). Tỷ lệ chuyển báo giá = (GP có báo giá) / (GP chốt). Tỷ lệ chuyển hợp đồng = (GP ký HĐ) / (GP có báo giá). Cấp cha tính tổng số lượng, KHÔNG tính trung bình %.
7. **Phân quyền cấp:**
   - "Tổng công ty" — tất cả dữ liệu.
   - "Công ty" — chỉ công ty hiện tại.
   - "Phòng ban" — chỉ phòng ban user thuộc.
   - "Bộ phận" — chỉ bộ phận user thuộc.
8. **Ghi chú đọc bảng:** Click số liệu ở hàng cấp cha → modal danh sách GP chi tiết với lọc theo Nhóm ngành / Nhóm GP / Ứng dụng / Trạng thái GP + tìm kiếm. Dòng tổng cuối modal là tổng của tất cả kết quả lọc, không chỉ trang hiện tại. Modal hỗ trợ export + phân trang.

### TC cần giải thích nghiệp vụ
- **Phân quyền tổng công ty (TC-ROLE-01):** Thấy tất cả công ty / phòng / nhân viên; không có quyền thì chỉ thấy của mình.
- **Filter theo phòng (TC-ROLE-02):** Chọn phòng → chỉ hiện nhánh có phòng đó, cấu trúc cây giữ nguyên.
- **Filter theo nhân viên (TC-ROLE-03):** Chọn 1 nhân viên → thấy GP mà nhân viên là kỹ sư chính. Cấp cha vẫn tính tổng dữ liệu con (không phải chỉ riêng nhân viên lọc).

---

## Sheet 38 — BC phân bổ nguồn lực (GANTT) theo nhân viên

1. **Mục đích báo cáo:** Hiển thị phân bổ task + công suất của từng nhân viên trên trục thời gian dạng biểu đồ Gantt. Giúp quản lý theo dõi mức độ sử dụng nguồn lực (dưới tải / bình thường / vượt tải) và lên kế hoạch phân công.
2. **Đối tượng được tính:** Nhân viên có task trong khoảng lọc (hoặc tất cả nếu bỏ tick "Chỉ NV có task"). Task có thời gian giao đè lên khoảng filter, trạng thái khác Nháp & Huỷ. Giờ làm định mức = tổng giờ phân ca thực tế trong kỳ. Nếu chọn 1 dự án thì chỉ tính task dự án đó.
3. **Đối tượng bị ẩn:** Task ở trạng thái Nháp hoặc Huỷ; nhân viên không có task (nếu bật "Chỉ NV có task"); phòng ban không có nhân viên thoả filter "% sử dụng".
4. **Bộ lọc thời gian áp dụng cho:**
   - Công suất nhân viên: giờ làm tính từ phân ca trong khoảng [từ ngày, đến ngày].
   - Task: tính task có thời gian giao đè lên khoảng filter (không yêu cầu nằm trọn).
   - Gantt: hiển thị từng ngày của khoảng filter.
5. **Cấu trúc cây phân cấp:** Tổng báo cáo → Phòng ban (tổng NV + task + giờ + %) → Nhân viên (chi tiết + thanh Gantt).
6. **Quy tắc cộng dồn cấp cha (Phòng ban):** Tổng task + tổng giờ làm + tổng giờ task = cộng dồn từ NV con. % sử dụng phòng = tổng giờ task / tổng giờ làm × 100. Cấp NV: số task = đếm task; giờ làm = tổng phân ca; giờ task = tổng giờ giao; % sử dụng = giờ task / giờ làm × 100. Giờ rảnh = max(0, giờ làm − giờ task). Giờ vượt tải = max(0, giờ task − giờ làm).
7. **Phân quyền cấp:**
   - "Tổng công ty" — tất cả nhân viên mọi công ty.
   - "Công ty" — chỉ nhân viên cùng công ty hiện tại.
   - "Phòng ban" — chỉ nhân viên cùng phòng.
   - "Bộ phận" — chỉ nhân viên cùng bộ phận.
   - Không có quyền — chỉ chính mình.
8. **Ghi chú đọc bảng:**
   - Mỗi thanh ngang Gantt là 1 task, kéo từ ngày bắt đầu task đến ngày hạn.
   - Màu: xanh (chưa quá hạn) / cam (đến hạn hôm nay) / đỏ (quá hạn, chưa hoàn thành).
   - Click thanh → mở modal chi tiết task.
   - Task vượt ra ngoài khoảng filter bị cắt (clamp) — phần ngoài không hiển thị nhưng vẫn tính giờ.
   - Task chồng nhau được xếp theo nhiều hàng để tránh đè.
   - Cột ngày hôm nay được tô nền xanh nhạt.
   - Nút "Ẩn/Hiện Gantt" để chỉ xem 7 cột data.
   - 7 cột đầu (STT…Trạng thái) sticky khi scroll ngang; cột Gantt scroll tự do.

### TC cần giải thích nghiệp vụ
- **Phân quyền (TC-ROLE-01..04):** Tổng công ty thấy tất cả; Công ty cùng công ty; Phòng ban cùng phòng; Không quyền chỉ chính mình.
- **Filter % sử dụng + có task (TC-COMPLEX-01):** NV1 50% / NV2 80% / NV3 120% (không có task) — filter 60–100% + chỉ NV có task → chỉ thấy NV2.
- **Task vượt ngoài khoảng filter (TC-COMPLEX-02):** Task A từ 01/04–25/04, filter 07/04–15/04 → thanh Gantt bị cắt trong khoảng đó, nhưng vẫn tính đủ giờ task vào NV.
- **NV chưa phân ca (TC-COMPLEX-03):** NV4 chưa phân ca + có 8h task → giờ làm = 0, % sử dụng = 0% (không chia cho 0). NV4 vẫn hiển thị nếu không tick "Chỉ NV có task".

---

## Sheet 39 — BC phát triển khách hàng theo nhân viên kinh doanh

1. **Mục đích báo cáo:** Theo dõi hiệu quả phát triển khách hàng của từng NVKD theo 2 góc nhìn: khách hàng mới được phát triển trong kỳ + kết quả chăm sóc các khách hàng (qua dự án tư vấn) tạo trong kỳ.
2. **Đối tượng được tính:**
   - Nhóm A (Phát triển KH mới): Khách hàng tổ chức tạo trong kỳ, có dự án tư vấn hoặc chưa có dự án nào. NVKD = NVKD chính của dự án, hoặc người tạo KH nếu chưa có dự án.
   - Nhóm B (Kết quả chăm sóc): Dự án tư vấn tạo trong kỳ, gắn với NVKD chính của dự án.
3. **Đối tượng bị ẩn:** Khách hàng loại "Cá nhân" (chỉ tính loại tổ chức); dự án ở trạng thái "Đang tạo" / "Đóng dự án" / "Kết thúc và lưu trữ".
4. **Bộ lọc thời gian áp dụng cho:**
   - Nhóm A: Ngày tạo khách hàng nằm trong kỳ.
   - Nhóm B: Ngày tạo dự án tư vấn nằm trong kỳ.
   - Trạng thái chốt tại ngày cuối kỳ — lấy từ log lịch sử trạng thái dự án.
5. **Cấu trúc cây phân cấp:** Công ty → Phòng ban → Nhân viên kinh doanh.
6. **Quy tắc cộng dồn cấp cha:** Cấp NV = tổng KH/dự án ở mỗi trạng thái (Chưa tiềm năng / Đang trao đổi / Đang làm GP / Đang thương thảo / Đang thực hiện HĐ). Cấp Phòng = cộng các NV. Cấp Công ty = cộng các phòng.
7. **Phân quyền cấp:**
   - "Tổng công ty" — toàn bộ.
   - "Công ty" — chỉ công ty mình.
   - "Phòng ban" — chỉ phòng ban mình.
   - Cá nhân — chỉ chính mình.
8. **Ghi chú đọc bảng:** 2 nhóm cột song song (Phát triển KH mới | Kết quả chăm sóc), mỗi nhóm 6 cột: Tổng số / Chưa tiềm năng / Đang trao đổi / Đang làm GP / Đang thương thảo / Đang thực hiện HĐ. Click số → chi tiết danh sách KH/dự án theo trạng thái.

### TC cần giải thích nghiệp vụ
- **KH chưa có dự án (TC-DEV-CHUA):** KH tổ chức tạo trong kỳ, không có dự án tư vấn → tính vào Nhóm A trạng thái "Chưa tiềm năng", NVKD = người tạo KH.
- **KH có nhiều dự án từ nhiều NVKD (TC-MULTI-STAGE):** KH tạo tháng 5, NVKD A tạo dự án (trạng thái 2) tháng 5, NVKD B tạo dự án (trạng thái 4) tháng 5 → mỗi NVKD 1 dòng Nhóm B, trạng thái = trạng thái cao nhất tại cuối kỳ. Nhóm A tính theo người tạo KH ban đầu.
- **Phân quyền phòng ban (TC-PERM-DEPT):** NVKD có quyền "Xem theo phòng ban" chỉ thấy dữ liệu của NV trong phòng ban mình; click phòng ban → modal chi tiết phòng đó.
