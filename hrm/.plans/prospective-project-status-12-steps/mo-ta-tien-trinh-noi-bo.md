# Tiến trình nội bộ dự án TKT — mô tả dễ hiểu

Nguồn: Redmine #11426 + bảng "Tiến trình dự án con / dự án độc lập nội bộ - QTTT - 10/09".
Áp dụng cho **dự án con** và **dự án độc lập**. Dự án cha giữ nguyên như hiện tại.

---

## 1. Tiến trình nội bộ là gì?

Là **1 con số từ 1 đến 12** gắn trên mỗi dự án (cột `status` bảng `prospective_projects`), hiện thành badge "Tiến trình nội bộ" ở danh sách và chi tiết dự án.

- User **không chọn tay** bước này.
- Hệ thống **tự nhảy bước** khi user làm một thao tác nghiệp vụ (gửi yêu cầu làm giải pháp, tạo báo giá, chốt báo giá...).
- Mỗi lần nhảy bước đều ghi lịch sử (`prospective_project_status_logs`).

---

## 2. Chỉ có 2 luồng

Quyết định bằng checkbox **"Có giải pháp"** khi tạo dự án (`has_solution`):

| Luồng | Nghĩa | Đường đi |
|---|---|---|
| **Không có giải pháp** (TH1) | Sale bán hàng hóa thẳng, không cần phòng kỹ thuật làm giải pháp | 1 → 2 → **6** → 7 → 8 → 9 → 10 → 12 (bỏ qua 3, 4, 5) |
| **Có giải pháp** (TH2, đã gộp TH3 vào) | Có bước gửi yêu cầu làm giải pháp cho phòng kỹ thuật, hoặc phòng kinh doanh tự làm | 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8 → 9 → 10 → 12 |

Bước **11 (Đóng)** có thể rẽ vào từ bất kỳ bước nào.

---

## 3. Bảng 12 bước: thao tác nào đưa dự án vào bước đó

| Bước | Tên (theo spec mới) | Vào bước này khi… | Ai thao tác | Code tpe |
|---|---|---|---|---|
| 1 | Đang tạo | Bấm **Lưu nháp** khi tạo dự án | Sale | ✅ |
| 2 | Thu thập thông tin dự án | Bấm **Lưu** chính thức (sinh mã dự án). Hoặc tạo meeting cho dự án nháp | Sale | ✅ |
| 3 | Chờ tiếp nhận làm giải pháp | Bấm **Gửi yêu cầu làm giải pháp** | Sale | ✅ |
| 4 | Đang làm giải pháp | Phòng giải pháp **Tiếp nhận** yêu cầu và bắt đầu làm | Phòng giải pháp / Sale tự làm | ✅ |
| 5 | Trao đổi giải pháp với khách hàng *(tên cũ: Đã duyệt giải pháp)* | Hồ sơ giải pháp được **Duyệt** nội bộ | Trưởng phòng giải pháp | ✅ logic, ❌ tên |
| 6 | Lập dự toán *(tên cũ: Dự toán)* | Một trong 3 việc: bấm **Chốt giải pháp** (phải đính kèm file) · tạo **Yêu cầu xây dựng giá** · tạo **Báo giá** | Sale | ✅ logic, ❌ tên, ❌ bắt buộc file |
| 7 | Thương thảo giá và giải pháp *(tên cũ: Thương thảo giá)* | Báo giá được **Duyệt** nội bộ | Người duyệt báo giá | ✅ logic, ❌ tên |
| 8 | Thương thảo hợp đồng | Bấm **Chốt báo giá cuối cùng** (Trúng thầu) + đính kèm file xác nhận của khách | Sale | ✅ logic, ❌ bắt buộc file |
| 9 | Thực hiện hợp đồng | Hợp đồng chuyển sang **Có hiệu lực** | Hệ thống (theo hợp đồng) | ❌ chưa có |
| 10 | Nghiệm thu và thanh lý hợp đồng | Hợp đồng bước vào nghiệm thu / thanh lý | Hệ thống (theo hợp đồng) | ❌ chưa có |
| 11 | Đóng / Không thực hiện dự án | (a) Sale bấm **Đóng dự án**, chọn nguyên nhân + ghi chú. (b) Hợp đồng bị **Hủy / Đóng** → hệ thống tự đóng dự án | Sale / Hệ thống | ✅ (a), ❌ (b) |
| 12 | Kết thúc và lưu trữ | Dự án hoàn tất, chỉ để tra cứu | *Spec chưa nói ai bấm* | ❌ chưa có |

---

## 4. Các trường hợp LÙI bước

| Đang ở | Lùi về | Khi nào | Code tpe |
|---|---|---|---|
| 3 | 2 | Yêu cầu làm giải pháp bị **Từ chối** hoặc **Hủy** | ✅ |
| 3 | 2 | Yêu cầu làm giải pháp bị **Yêu cầu bổ sung thông tin** | ❌ chưa có |
| 8 | 7 | **Hủy chốt** báo giá | ✅ |

---

## 5. Sơ đồ

```
 [1 Đang tạo] --Lưu chính thức--> [2 Thu thập TT]
                                       |
                 +---------------------+----------------------+
                 | KHÔNG có giải pháp                          | CÓ giải pháp
                 |                                             v
                 |                              --Gửi YC làm GP--> [3 Chờ tiếp nhận]
                 |                                   ^                |  (từ chối / hủy / YC bổ sung → về 2)
                 |                                   |     --Tiếp nhận--> [4 Đang làm GP]
                 |                                   |                      --Duyệt hồ sơ GP--> [5 Trao đổi GP với KH]
                 |                                                                                   |
                 +----------- Tạo báo giá / YC xây dựng giá / Chốt giải pháp (+file) ---------------+
                                                     |
                                                     v
                                            [6 Lập dự toán]
                                   --Duyệt báo giá--> [7 Thương thảo giá & GP]
                    --Chốt báo giá cuối cùng (+file)--> [8 Thương thảo HĐ]   (hủy chốt → về 7)
                            --HĐ có hiệu lực--> [9 Thực hiện HĐ]
                          --Nghiệm thu/thanh lý--> [10 Nghiệm thu & thanh lý]
                                                     --> [12 Kết thúc & lưu trữ]

   Bất kỳ bước nào --Đóng dự án (chọn nguyên nhân) / HĐ bị hủy--> [11 Đóng]
```

---

## 6. Phạm vi đã chốt cho task #11426 (chốt 2026-09-11)

1. **Đổi tên 3 bước** 5, 6, 7 và **gom tên bước về BE**: Resource trả `status_name` + `status_color`, FE bỏ 6 chỗ hard-code (constants.js, `progressOptions` ×4, manager.vue, ChildrenTab, blade export). Sửa luôn lỗi dự án cha hiện sai tên ở filter / export.
2. **"Yêu cầu bổ sung thông tin"** trên yêu cầu làm giải pháp → dự án lùi về bước 2 (gửi lại thì tự lên 3 như cũ).
3. **Bắt buộc file đính kèm** khi bấm **Chốt giải pháp** và **Chốt báo giá cuối cùng**: popup thêm ô `V2BaseFile` bắt buộc (cho nhiều file), BE validate 422 nếu thiếu, lưu bảng `files` chung. Sau khi chốt, file hiện lại ở màn chi tiết dự án (khối Giải pháp cho file chốt GP, tab Báo giá cho file chốt BG), có nút tải xuống.

4. **Lịch sử tiến trình**: dùng lại bảng `prospective_project_status_logs` (đã có `status_from`, `status_to`, `changed_at`, `changed_by`), thêm 2 cột `status_from_text`, `status_to_text` lưu tên bước lúc đổi. Backfill dữ liệu cũ.

## 7. Ngoài phạm vi (đã chốt với user)

- Luồng TH1/TH2 xác định bằng checkbox "Có giải pháp" lúc tạo dự án, **không thêm ô chọn trường hợp** ở yêu cầu làm giải pháp.
- Bước 9, 10, 12 và nhánh "hợp đồng bị Hủy/Đóng tự đóng dự án" (11b): **chưa làm**, phụ thuộc trạng thái hợp đồng, để task sau.
- Bước 11 (Sale bấm Đóng dự án) giữ nguyên như hiện có.
