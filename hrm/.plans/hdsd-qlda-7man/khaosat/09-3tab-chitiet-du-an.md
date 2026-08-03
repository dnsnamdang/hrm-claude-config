# Khảo sát — 3 tab trong màn Chi tiết dự án tiền khả thi
`/assign/prospective-projects/{id}/manager` — file gốc `pages/assign/prospective-projects/_id/manager.vue`

## 0. Hàng tab và điều kiện hiển thị
Thứ tự 10 tab: Dự án (dự án cha đổi nhãn thành **Thông tin chung**) · **Yêu cầu** · **Giải pháp** · Task · Issue ·
Meetings · Files · Hồ sơ · **Báo giá** · Thu thập thông tin. Tab mặc định khi mở màn là **Dự án**.

Quy tắc ẩn/hiện:
- **Dự án cha**: chỉ 3 tab Thông tin chung / Dự án con / Meetings → **ẩn cả Yêu cầu, Giải pháp, Báo giá**.
- Dự án **Tự triển khai** mà **không làm giải pháp** → ẩn Yêu cầu, Giải pháp, Task, Issue, Files, Hồ sơ.
  **Tab Báo giá VẪN HIỆN** (push vô điều kiện).
- Dự án đã đóng (status 11): banner đỏ phía trên hàng tab, tiêu đề **"Dự án đã đóng"** + Lý do / Ghi chú /
  "Đóng ngày … bởi …".

---

## 1. Tab YÊU CẦU
Render `pages/assign/request-solution/components/RequestTab.vue` với `:disabled="true"` — **toàn bộ read-only**.

**Empty state:** icon + chữ **"Dự án chưa có yêu cầu giải pháp tương ứng"** (khi `request_solution_id` rỗng).
Nạp bằng `GET assign/request-solutions/{request_solution_id}`; lỗi → toast **"Không thể tải dữ liệu yêu cầu"**.

**KHÔNG có bảng danh sách, KHÔNG có banner, KHÔNG CÓ NÚT NÀO.** Gồm 2 thẻ:

### Card 1 — Thông tin yêu cầu (mọi trường disabled)
| # | Nhãn | Ghi chú |
|---|---|---|
| 1 | **Mã yêu cầu** + **Trạng thái** | pill màu, chỉ hiện ở chế độ xem |
| 2 | **Tên yêu cầu** * | |
| 3 | **Phòng tiếp nhận yêu cầu** * | dự án Triển khai theo phòng bị khoá = phòng KD phụ trách |
| 4 | **Ứng dụng** * | kế thừa từ dự án |
| 5 | **Nhóm ngành** | lọc theo Ứng dụng |
| 6 | **Nhóm giải pháp** | lọc theo Ứng dụng |
| 7 | **Ngày KH cần giải pháp** * | |
| 8 | **Ngày KH cần báo giá** * | |
| 9 | **Ngày cần nhận GP nội bộ** | |
| 10 | **Hạn hoàn thành tiếp nhận** | chỉ hiện khi có giá trị, format DD/MM/YYYY HH:mm |
| 11 | **Mô tả / ghi chú yêu cầu** | |
| 12 | **File gửi kèm** | cột STT / Tên tài liệu / File đính kèm / Dung lượng (cột Thao tác bị ẩn vì disabled) |

### Card 2 — Phụ trách KD nội bộ
Cột trái **Phòng KD phụ trách chính**: Phòng, rồi khối **KD phụ trách chính** (Họ tên `Tên (Mã)`, SĐT, Email).
Cột phải **Phòng KD hỗ trợ & KD hỗ trợ** — chỉ hiện khi có; mỗi phòng là hộp **"Phòng hỗ trợ #N: <tên phòng>"**
+ danh sách `Tên (Mã) — SĐT — Email`.

---

## 2. Tab GIẢI PHÁP
Có **2 tab con**, tab con 1 active mặc định.

### 2.1 Tab con "Thông tin giải pháp"
**Empty state:** **"Dự án chưa có giải pháp tương ứng"**.
Bố cục (không bảng danh sách, không banner):
- **Khối "Thông tin giải pháp"** — 6 ô: Mã giải pháp, Tên giải pháp, Trạng thái (badge màu),
  Version hiện tại, PM làm giải pháp, Phòng tiếp nhận. Rỗng hiển thị `—`.
- **Khối "Quản lý nhân sự"** — nhúng `HumanResourceTab` với `readonly=true`:
  - Bảng: **STT / THÀNH VIÊN (avatar + tên + email) / HẠNG MỤC / VAI TRÒ (badge) / NGÀY BẮT ĐẦU /
    NGÀY KẾT THÚC / TASK ĐANG PHỤ TRÁCH (số) / TRẠNG THÁI (badge)**.
    Rỗng → **"Chưa có nhân sự nào trong dự án"**.
  - Khối **"Sơ đồ cấu trúc nhân sự"** + badge **PM: …**, **Hạng mục: …**, **Nhân sự: …**.
    Rỗng → **"Chưa có dữ liệu nhân sự. Hãy thêm nhân sự trong các hạng mục."** hoặc
    **"Chưa có dữ liệu sơ đồ. Hãy chọn Leader và phân công nhân sự."**
  - Vì `readonly=true` nên **toàn bộ thanh nút (Phân công / Xem lịch sử phân công / Thêm nhân sự) BỊ ẨN**
    → tab con này **KHÔNG CÓ NÚT NÀO**.

### 2.2 Tab con "Yêu cầu điều chỉnh GP"
Chưa có giải pháp → **"Dự án chưa có giải pháp tương ứng"**.
Bảng tiêu đề **"Yêu cầu điều chỉnh giải pháp"**, empty **"Chưa có yêu cầu điều chỉnh giải pháp nào."**
API `GET assign/prospective-projects/{id}/solution-adjustment-requests`; lỗi → **"Không thể tải danh sách yêu cầu điều chỉnh"**.

| # | Cột | Nội dung |
|---|---|---|
| 1 | STT | theo trang |
| 2 | **Mã yêu cầu** | VD `YCDCGP.00001`, bấm mở popup chi tiết |
| 3 | **Version** | `solution_version_code` |
| 4 | **Người yêu cầu** | |
| 5 | **Ngày gửi** | dd/mm/yyyy |
| 6 | **Trạng thái** | **Đã gửi** (xanh dương) / **Tiếp nhận** (xanh lá) / **Từ chối** (đỏ) |
| 7 | **Hành động** | **chỉ hiện khi người xem KHÔNG phải NV KD phụ trách dự án** |

| Nút | Điều kiện hiện | Hành vi |
|---|---|---|
| **Tạo yêu cầu** (góc phải bảng) | là **NV KD phụ trách dự án** VÀ trạng thái GP ∈ {Đã duyệt giải pháp, Đã duyệt giá, Chờ làm giá, Chốt giải pháp} | Mở modal Tạo yêu cầu điều chỉnh giải pháp |
| Xem chi tiết (mắt) | khi cột Hành động hiện | mở modal chi tiết |
| Tiếp nhận (✓ xanh) | `is_can_accept`: trạng thái **Đã gửi** và người xem là **PM của giải pháp** hoặc **TP phòng tiếp nhận** | confirm **"Phê duyệt yêu cầu điều chỉnh" / "Bạn có chắc muốn tiếp nhận yêu cầu điều chỉnh này?"** |
| Từ chối (✕ đỏ) | `is_can_reject` (cùng luật) | mở modal Từ chối |

**Popup Tạo yêu cầu điều chỉnh giải pháp** (lg): **Giải pháp** (disabled, điền sẵn `MãGP - TênGP (VVersion)`),
**Nội dung điều chỉnh** (textarea 5 dòng, BẮT BUỘC, placeholder "Nhập nội dung cần điều chỉnh..."),
**File đính kèm**. Nút **Gửi** / **Đóng**. Rỗng → **"Nội dung điều chỉnh không được để trống"**.
`POST .../solution-adjustment-requests` → **"Gửi yêu cầu điều chỉnh thành công"**.
BE sinh mã `YCDCGP.NNNNN`, trạng thái **Đã gửi**, gửi thông báo cho PM + TP phòng tiếp nhận.

**Popup Chi tiết**: bảng 2 cột — Mã yêu cầu / Giải pháp / Người yêu cầu / Ngày gửi / Trạng thái /
Nội dung điều chỉnh; thêm **Người tiếp nhận** (status 2) hoặc **Người từ chối** + **Lý do từ chối** (status 3);
khối File đính kèm. Footer: **Tiếp nhận** / **Từ chối** / **Đóng**.

**Popup Từ chối** (md): **Lý do từ chối** (textarea 4 dòng, bắt buộc). Nút **Gửi** / **Đóng**.
`PUT .../{id}/reject` → **"Đã từ chối yêu cầu điều chỉnh"**.

**Tiếp nhận** → `PUT .../{id}/accept` → **"Đã tiếp nhận yêu cầu điều chỉnh"**.
⚠️ **HỆ QUẢ DÂY CHUYỀN**: mọi YCXD giá của dự án đang Chờ/Đang XD giá chuyển sang **Dừng**;
báo giá liên quan đang Đang tạo / Chờ TP duyệt / Chờ BGĐ duyệt chuyển sang **Dừng**,
người lập báo giá nhận thông báo "Báo giá tạm dừng".

### 2.3 Nút "Chốt giải pháp" — KHÔNG nằm trong tab
Nằm ở **thanh footer của cả màn**. Điều kiện: dự án chưa đóng + người xem là **NV KD phụ trách** +
có hồ sơ chốt được (`GET .../finalizable-profiles` trả ≥1 bản ghi).
Popup **Chốt giải pháp**: rỗng → **"Không có hồ sơ nào ở trạng thái Đã duyệt / Hết hiệu lực."**;
**Chọn hồ sơ giải pháp** * (bảng radio: Mã hồ sơ / Version GP / Trạng thái / Ngày duyệt);
**Ghi chú chốt giải pháp** (textarea 3 dòng, ≤1000 ký tự, không bắt buộc).
Nút **"Lưu & gửi thông báo"** (disable tới khi chọn hồ sơ) → `POST .../finalize-solution` →
**"Đã chốt giải pháp thành công"**. Lỗi → **"Chốt giải pháp thất bại. Vui lòng thử lại."**

---

## 3. Tab BÁO GIÁ
`ProspectiveProjectQuotationsTab.vue`. Hiện với **mọi dự án không phải dự án cha**, kể cả Tự triển khai
không làm GP. API `GET assign/prospective-projects/{projectId}/quotations` → trả thêm `has_won_quotation`,
`tmp_sync`, `contract`.

Điều kiện chung của hầu hết nút: **`isSaleOfProject`** = người đăng nhập === `main_sale_employee_id`.
BE gate lại → 403 **"Bạn không phải Sale phụ trách dự án này"**.

### 3.1 Banner 1 — Đồng bộ hàng tạm sang ERP
Hiện khi dự án **có báo giá Trúng thầu** và báo giá đó **có ≥1 dòng hàng tạm**.
Tiêu đề: "Báo giá trúng thầu **<mã>** — Đồng bộ hàng tạm sang ERP".

| Badge | Khi nào | Dòng tiến độ |
|---|---|---|
| **Chưa đồng bộ** (xám) | chưa có trạng thái | "*N* hàng tạm chờ gửi" |
| **Đang đồng bộ sang ERP** (vàng) | `syncing` | "*x/y* hàng tạm đã duyệt" |
| **Đã đồng bộ** (xanh) | `synced` | "*y/y* hàng tạm đã tạo trên ERP" |

Có dòng **"Mã phiếu: <mã>"** link mở phiếu hàng tạm bên ERP khi đã gửi.

| Nút | Điều kiện hiện | Hành vi |
|---|---|---|
| **Gửi duyệt hàng tạm** | `isSaleOfProject` + chưa có trạng thái đồng bộ + còn ≥1 hàng tạm chưa gửi | Confirm **"Gửi duyệt hàng tạm của báo giá trúng thầu sang ERP?"** (nút Gửi duyệt / Huỷ) → `POST .../send-tmp-approval` → **"Đã gửi duyệt hàng tạm sang ERP"** |
| **Cập nhật kết quả duyệt** | `isSaleOfProject` + trạng thái `syncing` | `POST .../pull-tmp-approval` → có hàng bị từ chối: toast đỏ **"Có N hàng tạm bị từ chối"**; ngược lại **"Đã cập nhật kết quả duyệt"** |

Tự động: mở tab mà trạng thái đang `syncing` thì FE tự gọi `pull-tmp-approval` một lần.

### 3.2 Banner 2 — Lập hợp đồng ERP
Hiện khi dự án **có báo giá Trúng thầu**. Tiêu đề "Lập hợp đồng ERP từ báo giá **<mã>**".
Badge theo thứ tự ưu tiên:
1. **Đã lập hợp đồng ERP** (xanh) — đã có mã HĐ
2. **Báo giá ngoại tệ — chưa hỗ trợ** (xám)
3. **Báo giá có cấp con — chưa hỗ trợ lập HĐ** (xám)
4. **Chờ đồng bộ hết hàng sang ERP** (vàng)
5. **Sẵn sàng lập hợp đồng** (xanh dương) — đủ điều kiện và người xem là người tạo báo giá
6. **Đã đồng bộ — chỉ người lập báo giá mới lập được HĐ** (xanh)

Dòng meta: **Mã hợp đồng ERP** (link mở ERP, else `—`), **Trạng thái đồng bộ**
(badge *Đã đồng bộ* / *Đồng bộ lỗi* / *Chưa đồng bộ*), **Thời gian đồng bộ**.

Nút **Lập hợp đồng ERP** — điều kiện `can_create_contract`: đã map hết hàng ERP + VND + chưa có HĐ ERP +
người xem là **người tạo báo giá** + báo giá không có dòng cấp con.
Link mở **tab mới** sang ERP `.../admin/sale/firm-contracts/create?hrm_quotation_id=<id>&contract_type=4`.
Không gọi API HRM, không toast.

### 3.3 Bảng danh sách
Tiêu đề **"Danh sách báo giá"**, empty **"Dự án chưa có báo giá nào."** Mặc định 10 dòng/trang.

| # | Cột | Nội dung |
|---|---|---|
| 1 | STT | theo trang |
| 2 | **Mã BG** | `Mã BG - Tên BOM`; dòng phụ **"YCBG: <mã>"** nếu lập từ YCBG. Cụm nút thao tác nằm trong ô này |
| 3 | **Loại** | **Từ BOM** / **Tự nhập** |
| 4 | **Version GP** | badge, không có → `—` |
| 5 | **BOM** | mã BOM, link sang `/assign/bom-list/{id}`; không có → `—` |
| 6 | **Khách hàng** | |
| 7 | **Loại tiền tệ** | |
| 8 | **Tổng giá trị báo giá** | `total_after_vat` + mã tiền tệ |
| 9 | **Người lập** | |
| 10 | **Trạng thái** | Đang tạo / Chờ TP duyệt / Chờ BGĐ duyệt / Đã duyệt / Đóng / Dừng / **Trúng thầu** |
| 11 | **Ngày duyệt** | dd/mm/yyyy HH:mm, không có → `—` |

### 3.4 Nút trên tab Báo giá
| Nút | Vị trí | Điều kiện hiện | Kết quả |
|---|---|---|---|
| **Tạo báo giá** | toolbar | `isSaleOfProject` | Điều hướng `/assign/quotations/create?project_id={id}` |
| **Xem chi tiết** (mắt) | dòng | luôn hiện | `/assign/quotations/{id}` |
| **Sửa / Làm giá** (bút) | dòng | status = Đang tạo VÀ là **người lập** báo giá | `/assign/quotations/{id}/edit` |
| **Sao chép báo giá** | dòng | BG từ YCBG → cần quyền **Xây dựng giá bán theo phòng** (dự án type 2) hoặc **theo công ty** (type 1/3); BG tự lập → phải là Sale phụ trách. Hiện ở **MỌI trạng thái** | `copy-preview` → không thay đổi thì copy luôn; có thay đổi thì mở popup so sánh. Toast **"Đã sao chép sang báo giá <mã mới>"** rồi sang màn sửa bản mới |
| **Sửa ghi chú kinh doanh** | dòng | status = Đã duyệt VÀ `isSaleOfProject` | `PUT .../sales-note` → **"Đã lưu ghi chú"** |
| **Chốt báo giá (Trúng thầu)** | dòng | status = Đã duyệt VÀ `isSaleOfProject` VÀ dự án **chưa có** báo giá trúng thầu | `POST .../finalize` → **"Đã chốt báo giá (Trúng thầu)"**, 2 banner xuất hiện |
| **Hủy chốt** | dòng | status = Trúng thầu VÀ `isSaleOfProject` | `POST .../unfinalize` → **"Đã hủy chốt báo giá"**, về Đã duyệt |
| **Lịch sử phê duyệt** (đồng hồ) | dòng | luôn hiện | Popup **Lịch sử báo giá** — timeline |
| **Xuất Excel** | dòng | luôn hiện | Tải `BaoGia_<mã>.xlsx` |
| **Xoá** (thùng rác) | dòng | status = Đang tạo VÀ là **người lập** | Confirm → `DELETE` → **"Đã xoá báo giá"** |

**Popup Ghi chú kinh doanh**: 1 trường **Ghi chú** (textarea 4 dòng, không bắt buộc).
Nút **Lưu** / **Đóng**.
⚠️ **LỖI PHÁT HIỆN**: `QuotationResource` **không trả trường `sales_note`** → popup mở từ tab này
**LUÔN TRỐNG**, người dùng sửa là **ghi đè mất ghi chú cũ**. Cần báo dev.

**Popup Hủy chốt báo giá**: mô tả *"Hủy chốt báo giá <mã> — báo giá sẽ quay lại trạng thái "Đã duyệt"."*;
**Lý do hủy chốt** * (textarea 4 dòng, bắt buộc, ≤1000 ký tự). Bỏ trống → **"Vui lòng nhập lý do hủy chốt."**
Nút **Xác nhận hủy chốt** / **Huỷ**.

**Popup Xác nhận chốt báo giá**: không có trường nhập, chỉ câu hỏi
*"Chốt báo giá <mã> thành Trúng thầu? Mỗi dự án chỉ có 1 báo giá trúng thầu."* Nút **Chốt** / **Huỷ**.

---

## 4. Phân quyền
- **Không có `hasPermission` trực tiếp** trên cả 3 tab, trừ một chỗ: nút **Sao chép báo giá** dùng
  `Xây dựng giá bán theo phòng` / `Xây dựng giá bán theo công ty`.
- **Không route nào của 3 tab gắn `checkPermission`**. Gate nằm trong controller/service bằng
  **vai trò dữ liệu** (Sale phụ trách / người lập / PM / TP phòng tiếp nhận) + **trạng thái**.
- Route `byProject` của tab Báo giá **KHÔNG áp scope 4 quyền "Xem danh sách Báo giá"** —
  tab liệt kê toàn bộ báo giá của dự án.
- Quyền `Xem giá vốn hàng hoá` ảnh hưởng nội dung file Excel xuất ra.
