# Tổng hợp khối lượng công việc — Luồng BOM List + Báo giá (phục vụ nghiệm thu)

> Lập ngày **24/09/2026** · Phạm vi: phân hệ **Giao việc / Quản lý dự án TKT** của HRM
> (`Modules/Assign` + `pages/assign`), gồm **luồng chính BOM List → Báo giá** và **toàn bộ feature
> liên quan** đã làm kèm theo.
> Nguồn số liệu: `.plans/` (hồ sơ thiết kế + plan + checkpoint của từng hạng mục), `.plans/STATUS.md`,
> `.plans/gop-db/STATUS.md` và lịch sử git của 2 repo `hrm-api` · `hrm-client`.

---

## 1. Số liệu tổng quan

| Chỉ số | Giá trị |
|---|---|
| Khoảng thời gian thực hiện | **03/2026 → 09/2026** (7 tháng) |
| Luồng chính (BOM List + Báo giá) | **33 phase** |
| Hạng mục feature / điều chỉnh liên quan | **45 hạng mục** (mỗi hạng mục có hồ sơ riêng trong `.plans/`) |
| Hạng mục trên nhánh gộp DB (`gop_db`) | **7 hạng mục** |
| Commit liên quan | **216** (hrm-api **110** · hrm-client **106**) |
| Tài liệu bàn giao | SRS (html + docx, 27 bảng) · 135 test case luồng chính · bộ test case BOM & Báo giá riêng · HDSD màn Báo giá chờ duyệt |

---

## 2. Luồng chính — BOM List + Báo giá (33 phase)

### 2.1. Nền tảng BOM List (Phase 1 → 6)

| Phase | Nội dung |
|---|---|
| 1 | Màn **Danh sách BOM List** + trạng thái + Xoá |
| 1.5 | Bổ sung trường mới + **phân quyền** + bộ lọc |
| 2 | Refactor logic lưu sản phẩm BOM (cấu trúc cha–con) |
| 3 | **Xuất Excel** BOM |
| 4 | **Import Excel** BOM |
| 5 | Trang **chi tiết** BOM (chỉ xem) |
| 6 | Test toàn bộ BOM List |

### 2.2. Theo yêu cầu khách hàng + quy trình duyệt giá (Phase 7 → 9)

| Phase | Nội dung |
|---|---|
| 7 | Cập nhật BOM theo yêu cầu khách hàng (51 đầu việc) |
| 8a | **Quy trình trạng thái** BOM + loại tiền tệ + cấu hình cột + dịch vụ (83 đầu việc) |
| 8b | Xử lý các điểm còn thiếu sau Phase 8a |
| 9 | **Làm giá + Phê duyệt giá BOM** |

### 2.3. Tách Báo giá thành nghiệp vụ riêng (Phase 11 → 16)

| Phase | Nội dung |
|---|---|
| 11 | **Tách BOM và Báo giá** thành 2 nghiệp vụ độc lập |
| 12 | **Quản lý VAT** cho báo giá |
| 13 | Email khách hàng trên Dự án TKT + Báo giá |
| 14 | **Roll-up giá trị từ hàng con lên hàng cha** (14A BOM · 14B Báo giá 6 cột) |
| 15 | **Xoá báo giá** |
| 16 | Hoàn thiện giao diện báo giá + tìm kiếm BOM từ xa (remote search) |

### 2.4. Gắn kết với dự án TKT & giải pháp (Phase 17 → 18, 23, 27, 28)

| Phase | Nội dung |
|---|---|
| 17 | **Cascade trạng thái** Dự án TKT ↔ Giải pháp |
| 18 | **Chốt giải pháp** + cập nhật UI + **lịch sử BOM** |
| 23 | Đổi nguồn dữ liệu màn **Danh sách hàng hoá dự án** |
| 27 | Bổ sung cột trang Hàng hoá dự án |
| 28 | Cải thiện giao diện màn chi tiết Dự án TKT |

### 2.5. Xuất / In / Import báo giá (Phase 19, 20, 22)

| Phase | Nội dung |
|---|---|
| 19 | **Xuất / Import Excel** ngay trên màn sửa Báo giá |
| 20 | Hoàn thiện Excel + hyperlink + import theo nhóm hàng |
| 22 | **In báo giá** |

### 2.6. Nghiệp vụ giá: dịch vụ, cha–con, chiết khấu, làm tròn (Phase 21, 29 → 33)

| Phase | Nội dung |
|---|---|
| 21 | **Dịch vụ bổ sung** + đảo logic cha–con + làm tròn |
| 29 | **Chiết khấu / giảm giá báo giá** |
| 30 | **Báo giá tự xây dựng** (báo giá độc lập, không cần BOM) |
| 31 | **Logic hàng hoá cha–con** cho cả BOM và Báo giá (snapshot bộ ghép từ ERP, khoá dòng con, kiểm giá vốn cha ≥ Σ con) |
| 32 | **Làm tròn số nhất quán** toàn bộ báo giá · **Chọn/đổi ĐVT** ở màn Tạo/Sửa BOM · tối ưu popup "Thêm hàng hoá" |
| 33 | **Validate hiển thị inline tại ô** (bỏ toast) |

### 2.7. Sửa lỗi theo đợt (Phase 24, 25, 26)

Ba đợt sửa lỗi + cải thiện giao diện trong 05/2026, gồm bỏ bắt buộc giá nhập/giá bán khi **Lưu nháp**.

---

## 3. Các hạng mục feature / điều chỉnh liên quan (45 hạng mục)

### 3.1. Nghiệp vụ giá & phê duyệt

| Hạng mục | Nội dung | Trạng thái |
|---|---|---|
| Quyền áp dụng giảm giá (Redmine #10789) | Gắn quyền cho thao tác giảm giá trên báo giá | Code xong, chờ test tay |
| Cảnh báo đơn giá ≤ 1.000đ & tự động duyệt (#10797) | Chặn/cảnh báo giá bất thường, tự duyệt theo ngưỡng | Code xong, chờ test tay |
| Cảnh báo giá bán ≤ 1.000đ ở màn **Tạo mới** | Bổ sung cảnh báo còn thiếu ở luồng tạo | Xong |
| Cảnh báo đơn giá thay đổi khi sửa báo giá (#10791) | Báo cho người lập khi giá ERP đã đổi | Xong phần chính |
| Cảnh báo báo giá có giá = 0 | Chặn gửi duyệt khi còn dòng giá 0 | Xong |
| Tỷ suất lợi nhuận dòng hàng tạm (#10898) | Đưa hàng tạm vào luồng duyệt, hiện giá vốn hàng tạm | Xong phần chính |
| Sắp xếp & đổi nhãn 9 quyền nhóm Báo giá | Chuẩn hoá màn phân quyền | Xong |
| Đổi tên "Loại chiết khấu" → "Loại giảm giá" | Đổi nhãn + quyền + danh mục | Xong |
| Chốt / Huỷ chốt báo giá | Nghiệp vụ chốt báo giá | Xong |
| Gửi duyệt ở màn Tạo mới không sinh bản nháp | Bỏ bản ghi nháp thừa | Xong |
| Chặn lập báo giá thường trên dự án cha | Ràng buộc nghiệp vụ dự án nhiều cấp | Xong |

### 3.2. Tiền tệ, làm tròn, bảng giá

| Hạng mục | Nội dung | Trạng thái |
|---|---|---|
| Cho chọn **Loại tiền tệ** khi lập báo giá | Kế thừa từ dự án + cho chọn lại khi tạo mới | Code xong, chờ nghiệm thu |
| Chuẩn định dạng tiền tệ luồng quản lý dự án | Thống nhất cách hiển thị số | Code xong, chờ nghiệm thu |
| Chuẩn định dạng tiền tệ ERP ở màn Tạo/Sửa báo giá | Đồng bộ với ERP | Xong |
| **Làm tròn báo giá theo tiền tệ** | Quy tắc làm tròn theo VND/ngoại tệ | Code xong, chờ nghiệm thu |
| Trường **Bảng giá** cho báo giá | Chọn bảng giá áp dụng | Xong |
| Trường "Bảng giá áp dụng: Bán lẻ" + tooltip Làm tròn | Bổ sung thông tin trên form | Xong |
| Hiển thị Loại tiền tệ chỉ "Tên" + Ngày/Người lập báo giá | Gọn giao diện | Xong |
| Chi phí vận chuyển + thiết kế lại khối Tổng hợp giá trị | Thêm cấu phần chi phí | Code xong (Phase 1–17), chờ nghiệm thu |

### 3.3. Nhập / xuất / in / sao chép

| Hạng mục | Nội dung | Trạng thái |
|---|---|---|
| **Import báo giá v2** | Nhập báo giá từ Excel, 9 phase | Xong (còn 1 phần E2E) |
| Sao chép / Export / Import **Báo giá** | 3 thao tác trên danh sách báo giá | Xong |
| Import / Export / Sao chép **BOM List** | Tương ứng cho BOM | Xong |
| BOM List — Xuất Excel & In | Theo khuôn màn Báo giá | Xong |
| Cột "Hình ảnh" + "Thời gian bảo hành" khi In/Xuất Excel | Bổ sung cột theo yêu cầu | Xong |
| Hiệu chỉnh mẫu in báo giá | Sửa mẫu in | Xong |
| Popup **cấu hình in báo giá** (mặc định cột) | Ghi nhớ cột hiển thị khi in | Code xong, chờ nghiệm thu |
| Xuất Excel báo giá — bỏ thẻ HTML ở cột Thông số kỹ thuật | Sửa lỗi hiển thị | Xong |
| Miễn kiểm tra giá vốn cha ≥ Σ con cho hàng cha ERP khi import | Nới ràng buộc đúng nghiệp vụ | Xong |

### 3.4. Cấu trúc hàng hoá & nhóm hàng

| Hạng mục | Nội dung | Trạng thái |
|---|---|---|
| **Nhóm hàng 2 cấp + kéo–thả** cho Báo giá | Gom nhóm hàng trong báo giá | Xong |
| **Nhóm hàng 2 cấp + kéo–thả** cho BOM | Tương ứng cho BOM | Xong |
| Đồng bộ popup "Thêm hàng hoá" theo popup ERP | Thống nhất trải nghiệm chọn hàng | Xong |
| Chọn ĐVT khi tạo/sửa báo giá (hàng ERP) | Cho đổi đơn vị tính | Code xong + test người dùng OK |
| Tổng hợp BOM: sắp xếp hàng hoá theo thứ tự tạo | Sửa thứ tự hiển thị | Xong |
| Sửa 2 lỗi UI tên BOM (thụt lề, tràn chip) | Sửa giao diện | Xong |
| Hàng hoá dự án: hàng tạm từ báo giá độc lập không render link BOM | Sửa lỗi liên kết | Xong |
| Màn `/assign/product-project` hiển thị cả hàng ERP + hàng tạm | Mở rộng nguồn dữ liệu | Xong |

### 3.5. Liên kết dự án – giải pháp – hợp đồng

| Hạng mục | Nội dung | Trạng thái |
|---|---|---|
| Giai đoạn dự án cho Báo giá & Yêu cầu giải pháp (#11016) | Thêm trường + đồng bộ ngược về dự án | Xong (BE 35/35 test) |
| Đồng bộ Giai đoạn dự án từ Báo giá / YCGP | Hoàn thiện đồng bộ | Xong |
| Icon Info + tooltip mô tả Giai đoạn dự án (#11058) | Giao diện | Xong |
| Danh mục Loại meeting / Giai đoạn dự án (#11064) | Danh mục dùng chung | Xong phần chính |
| Huỷ yêu cầu làm giải pháp + trả dự án về "Thu thập thông tin" (#10841) | Nghiệp vụ huỷ | Xong |
| Từ chối Yêu cầu làm giải pháp + thông báo (#10845) | Nghiệp vụ từ chối | Xong |
| Link "Dự án" ở màn báo giá trỏ sang Quản lý dự án | Điều hướng | Xong |
| Báo cáo "Dự án TKT theo PB - NV KD" (#10819) | Sửa số liệu nhóm cột Báo giá | Xong |
| Báo cáo vòng đời dự án TKT (#11134) | Báo cáo mới | Xong |
| Lập HĐ ERP từ báo giá HRM | Chuyển báo giá thành hợp đồng ERP | **Đang làm** |
| Lập HĐ hãng từ báo giá HRM theo 2 cấp | Hợp đồng 2 cấp | **Đang làm** |

### 3.6. Hiệu năng & giao diện

| Hạng mục | Nội dung | Trạng thái |
|---|---|---|
| Tối ưu tốc độ load màn Danh sách báo giá | Giảm thời gian mở màn | Xong |
| Chỉnh UI bảng chi tiết màn Tạo báo giá | Giao diện bảng | Xong |
| Cho phép xoá giá trị (dấu ×) ở select màn Báo giá | Trải nghiệm nhập liệu | Xong |
| Thiết kế lại module Báo giá | Đợt redesign lớn | **Đang làm** (xong Task 1–13) |

---

## 4. Chuẩn hoá màn theo bộ quy chuẩn (nhánh gộp DB `gop_db`)

| Hạng mục | Nội dung | Trạng thái |
|---|---|---|
| Chuẩn hoá **Danh sách BOM List** theo skill `list-page` | Bộ lọc, cột, nút, phân trang theo chuẩn | Xong |
| Sửa lỗi API bộ lọc Khách hàng ở màn BOM List | Sửa lỗi | Xong |
| Chuẩn hoá **Danh sách báo giá** | Theo chuẩn `list-page` | Xong |
| Chuẩn hoá **Báo giá chờ duyệt** | Theo chuẩn `list-page` | Xong |
| Chuẩn hoá **Yêu cầu xây dựng giá** | Theo chuẩn `list-page` | Xong |
| **Mockup màn Chi tiết Báo giá** (giao diện Bán hàng) | Thử nghiệm giao diện mới | Xong (mockup) |
| Cụm CCTT + **Báo giá dịch vụ** | Khảo sát đầy đủ | **Khảo sát xong, chưa code** |

---

## 5. Tài liệu bàn giao kèm theo

| Tài liệu | Nội dung |
|---|---|
| `Bomlist-Quotation/srs.html` + `srs.docx` | SRS đầy đủ: sơ đồ use-case, swimlane luồng tạo/duyệt/chốt báo giá, **27 bảng đặc tả** |
| `Bomlist-Quotation/testcase.xlsx` | **135 test case** (P0 40%), 14 nhóm: BOM CRUD, cha–con, import/export, báo giá, VAT, chiết khấu, vận chuyển, làm tròn, duyệt, chốt… |
| `Bomlist-Quotation/Testcase_BOM_List.xlsx` | Test case riêng màn BOM List |
| `testcase-bom-baogia/` | Bộ test case BOM & Báo giá theo form khách (kèm đối chiếu 2 lần rà soát) |
| `bao-gia-cho-duyet-hdsd/` | **HDSD** màn "Phê duyệt → Báo giá chờ duyệt" (file Word) |
| `Bomlist-Quotation/design-phase*.md` · `plan-phase*.md` | Hồ sơ thiết kế + kế hoạch chi tiết từng phase |

---

## 6. Mục CHƯA hoàn thành (không tính vào nghiệm thu đợt này)

| Hạng mục | Tình trạng |
|---|---|
| Thiết kế lại module Báo giá (redesign) | Đang làm — xong Task 1–13, còn các task sau |
| Lập HĐ ERP / HĐ hãng 2 cấp từ báo giá HRM | Đang làm |
| Cụm CCTT + Báo giá dịch vụ | Mới khảo sát, chưa code |
| Giải pháp: Nhóm ngành / Nhóm giải pháp / Ứng dụng + Khách hàng cuối | Mới mở, phần lớn chưa làm |
| Một số hạng mục "code xong, chờ khách test/nghiệm thu" | Ghi rõ ở cột Trạng thái các bảng trên |

---

## 7. Ghi chú cách đọc bảng

- **Xong** = đã code + tự kiểm (test tự động hoặc kiểm trên trình duyệt), có hồ sơ checkpoint trong `.plans/<hạng mục>/plan.md`.
- **Code xong, chờ test/nghiệm thu** = đã hoàn thiện mã nguồn, đang chờ phía khách kiểm tra thực tế.
- **Đang làm** = còn đầu việc chưa khép.
- Mỗi hạng mục đều truy được: hồ sơ thiết kế (`design.md`), kế hoạch + checkpoint (`plan.md`) và commit tương ứng trong 2 repo.

---

## 8. Nhật ký cập nhật

| Ngày | Nội dung |
|---|---|
| 24/09/2026 | Lập bộ tài liệu: `tong-hop.md` + `tong-hop-nghiem-thu-bomlist-baogia.xlsx` (84 hạng mục / 10 nhóm · 36 phase · sheet bằng chứng) |
| 25/09/2026 | Xuất thêm **bảng danh mục hàng hoá** phục vụ nghiệm thu phần Hàng hoá: `.plans/gop-db/quan-ly-hang-hoa/danh-sach-danh-muc-hang-hoa.xlsx` (31 danh mục / 5 nhóm · 13 phase · bằng chứng) |

**Còn để mở:** chưa xuất bản **Word biên bản nghiệm thu có chỗ ký** — chờ anh chốt có cần hay không.
