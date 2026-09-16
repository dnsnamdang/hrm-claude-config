# Thiết kế lại Báo cáo theo dõi giữ hàng

> Trạng thái: **ĐANG DUYỆT MOCKUP** — chưa viết plan code.
> Nhánh: `gop_db` (cả `hrm-api` và `hrm-client`).
> Màn thay thế: `/finance/prepick-stocks` (giữ nguyên URL).

## Mockup

`bao-cao-theo-doi-giu-hang.html` (cùng thư mục) — port nguyên khối ngôn ngữ thiết kế của
`.plans/gop-db/bao-cao-ket-qua-du-an-tkt/bao-cao-ket-qua-du-an-tkt.html`.

## Quyết định đã chốt (2026-09-12)

| # | Vấn đề | Chốt |
|---|--------|------|
| 1 | Mốc thời gian | **Tồn giữ HIỆN TẠI**, không có bộ lọc Kỳ — hàng giữ là tồn tại thời điểm |
| 2 | Cấu trúc cấp | Theo nhân viên: **Phòng ban ▸ Nhân viên ▸ Hàng hoá** · Theo hàng hoá: **Hàng hoá ▸ Nhân viên** |
| 3 | Chỉ tiêu | **Số lượng / Trong hạn / Sắp hết hạn / Hết hạn** (đo kép theo cấp) + bộ cột hàng hoá bám màn cũ. BỎ cột Tỷ trọng quá hạn |
| 4 | Phạm vi thay | Giữ URL `/finance/prepick-stocks`; **KHÔNG** đụng `/finance/prepick-expiring` |
| 5 | Đơn vị đo ở cấp tổng | Đếm **SỐ LÔ GIỮ** (cộng được mọi cấp); số lượng + đơn vị chỉ hiện ở dòng hàng hoá |

Lý do #5: `prepick_details.qty` là đơn vị cơ bản của từng mặt hàng (cái/kg/mét/bộ) — cộng
số lượng ở cấp Phòng ban/Nhân viên ra con số vô nghĩa. Màn cũ né được vì tầng 1 luôn là 1 mặt hàng.

## Bổ sung vòng 2 (2026-09-12)

| # | Yêu cầu | Cách làm |
|---|---------|----------|
| 6 | Cấu hình số ngày cảnh báo đến hạn | Ô **"Cảnh báo trước N ngày"** trên thanh lọc, mặc định `configs.warning_day` (đang = 7). Nhóm "Đến hạn" (chỉ đúng hôm nay) đổi thành **"Sắp hết hạn"** = `[hôm nay · hôm nay + N]`. 3 nhóm vẫn chia hết tổng |
| 7 | Khối "Phạm vi đang giữ" | **Giữ** |
| 8 | Cột "Tỷ trọng quá hạn" | **Bỏ** |
| 9 | Cột **Tồn hiện tại** | Tồn kho của mặt hàng theo công ty đang lọc (`accounting_stocks` — đúng `stockSubQuery()` màn cũ đang dùng). Kèm cột **SL đang giữ** để đối chiếu |
| 10 | Cột **Số lần gia hạn** | Bấm số → popup lịch sử từng lần, xếp **CŨ → MỚI** |
| 11 | "Hạn giữ" → **"Hạn giữ hiện tại"** | Đổi ở popup danh sách lô, để hiểu hạn này có thể đã qua nhiều lần gia hạn |

### ⚠️ Gotcha BE của "Số lần gia hạn" — đã kiểm trên DB thật

`PrepickStockService::moveToExpireDate()` **KHÔNG sửa `expire_date` của lô cũ** mà **trừ ở lô cũ,
cộng sang lô MỚI** (`prepick_details` khác). Hệ quả:

- Đếm theo **LÔ đang tồn** → tối đa **3 lần**, trung bình 1,02 → **SAI**.
- Đếm theo **NHÓM GIỮ = bộ 4 (Nhân viên × Khách hàng × Hàng hoá × Công ty)** trên MỌI lô của nhóm
  (kể cả lô đã rút hết `qty = 0`) → tối đa **15 lần**, trung bình 1,81; 339/2.355 nhóm đã gia hạn ≥ 5 lần.
  **Đây là con số đúng.**
- Nguồn đếm: `prepick_logs` với `objectable_type = 'App\Model\Warehouse\PrepickExtendRequestDetail'`
  và `change > 0`. Chi tiết từng lần join `prepick_extend_request_details` (`new_expire_date`,
  `extend_qty`) + `prepick_extend_requests` (`code`, `approved_time`, người duyệt).
- 2.300/2.355 nhóm (97,7%) chỉ còn **đúng 1 lô** đang tồn → hiển thị số lần gia hạn ở dòng lô là chấp
  nhận được; 55 nhóm còn 2–3 lô sẽ thấy cùng một con số ở các dòng đó (tooltip nói rõ đếm theo nhóm).

## Bổ sung vòng 3 (2026-09-12)

### 12 · Cột chính đo KÉP theo cấp

| Cấp dòng | Cột "Số lượng" | 3 cột hạn |
|---|---|---|
| Phòng ban / Nhân viên | **số mã hàng** đang giữ (`14 Mã`) | số mã hàng theo từng nhóm hạn |
| Hàng hoá | **số lượng** theo đơn vị đang chọn (`157 Cái`) | số lượng theo từng nhóm hạn |

⚠️ **Ở dòng tổng, 3 cột hạn ĐẾM CHỒNG LẤN** — một mã hàng có thể vừa có lô trong hạn vừa có lô quá
hạn, nên `Trong hạn + Sắp hết hạn + Hết hạn` **lớn hơn** cột Số lượng (đo thật: 14 Mã vs tổng 25).
Ở dòng hàng hoá thì 3 nhóm **chia hết** tổng. Tooltip cột phải nói rõ để user không cộng tay rồi
tưởng số sai.

### 13 · Bộ cột hàng hoá bám đúng màn đang chạy

Màn ERP `prepickIndex.blade.php` tầng hàng hoá có: *Tên hàng hóa · Đơn vị · Kho · Model · Mã hàng
hóa · Thương hiệu · Tổng SL trong kho · SL giữ*. Bản mới lấy **đủ trừ cột Kho** —
`prepick_details` không có kho, hàng giữ là tồn theo **nhân viên**; cột Kho bên ERP lấy từ bảng tồn
nên một mã nằm nhiều kho sẽ nhân dòng.

Ô **Đơn vị** giữ đúng hành vi màn cũ: chỉ dựng select khi hàng hoá có ≥ 2 ĐVT (890/895 hàng hoá đang
giữ chỉ có 1 đơn vị), đổi đơn vị thì quy đổi cả 4 cột số của dòng đó, **không làm tròn về số nguyên**
(25 Mét ở đơn vị Cuộn ×100 phải ra `0.25`, làm tròn thành 0 là mất hàng trên báo cáo).

5 cột thuộc tính hàng hoá (mã · đơn vị · model · thương hiệu · tồn) **tự ẩn khi bảng chưa render
dòng hàng hoá nào** — giữ lại là mất ~550px cho ô rỗng; bung tay một nhánh tới hàng hoá là hiện lại ngay.

### 14 · Số lần gia hạn — GỠ khỏi bảng theo dõi

Gia hạn phát sinh trên **từng lần yêu cầu giữ** nên cộng dồn lên dòng Phòng ban / Nhân viên là sai.
Cột này chuyển hẳn vào **popup danh sách lô**, mỗi dòng lô một con số, bấm ra lịch sử của đúng lần
giữ đó. Popup danh sách lô thêm cột **"Yêu cầu giữ gốc"**; cột "Hạn giữ" đổi thành
**"Hạn giữ hiện tại"**.

**Cách đếm đúng** (đo trên DB thật, 2.412 lô đang tồn):

| Cách đếm | Tối đa | Kết luận |
|---|---|---|
| Log trên chính lô đang tồn | 3 lần | Sai — chỉ thấy lần cuối |
| **Chuỗi lần ngược của từng lô** | **10 lần** (TB 1,31 · 206 lô ≥ 5 lần) | **Đúng** |
| Gộp theo bộ 4 NV × KH × hàng hoá | 15 lần | Sai — gộp nhiều lần yêu cầu giữ |

SQL: đệ quy `prepick_details.objectable_id` → `prepick_extend_request_details.prepick_detail_id` →
lô nguồn → lặp. Chứng từ gốc cuối chuỗi: **Phiếu xuất giữ 1.794 · Nhập hàng cho khách 341 ·
Điều chuyển giữ 93 · không xác định 184**.

## Chưa chốt

- Ở cấp Phòng ban, popup lịch sử gia hạn có thể ra hơn 100 bảng con (mỗi nhóm giữ 1 bảng) — có cần
  chặn ngưỡng / phân trang không?

## Link

- Spec chi tiết: `docs/superpowers/specs/gop-db/2026-09-12-bao-cao-theo-doi-giu-hang-design.md`
- Plan: `plan.md` cùng thư mục

## Bổ sung vòng 4 (2026-09-12)

| # | Yêu cầu | Cách làm |
|---|---------|----------|
| 15 | Ô "Hạn giữ hiện tại" tô màu theo hạn | Xanh `#15803d` còn trong hạn · vàng `#b45309` khi số ngày còn lại ≤ ngưỡng cảnh báo · đỏ `#b91c1c` đã quá hạn. Tô cả ngày lẫn dòng "còn N ngày / quá hạn N ngày", dùng chung bảng màu với 3 cột hạn. Đo kiểm: cùng lô "còn 8 ngày" — ngưỡng 7 ra xanh, ngưỡng 10 ra vàng |
| 16 | Bảng có hàng hoá luôn có cột **Đơn vị tính riêng**, số lượng bỏ hậu tố ĐVT | Bảng chính + popup danh sách lô đều có cột ĐVT; 4 cột số bỏ `unit-sub`. Dòng TỔNG vẫn giữ nhãn **"Mã"** vì đó không phải đơn vị tính mà là thứ phân biệt "14 mã hàng" với "14 cái". Popup lịch sử gia hạn đưa ĐVT lên dòng mô tả |
| 17 | Popup luôn hiển thị 2 cột Mã hàng + Tên hàng | Bỏ cơ chế ẩn cột theo chiều đã cố định cho hàng hoá — kể cả khi popup mở từ đúng 1 hàng hoá vẫn giữ 2 cột (ô LỌC hàng hoá thì vẫn ẩn). Cột Nhân viên / Phòng ban giữ nguyên hành vi ẩn |
| 18 | Mã hàng là cột riêng, đứng TRƯỚC tên hàng | Bảng chính: `STT · Mã hàng hoá · Nội dung theo dõi · Đơn vị · Model · Thương hiệu · Tồn hiện tại · Số lượng · 3 cột hạn`. Popup: `STT · Mã hàng · Tên hàng · ĐVT · …` |
| 19 | Tiêu đề popup dùng khuôn **"Mã hàng - Tên hàng"** | `productLabel()` / `nodeLabel()` dùng chung cho tiêu đề popup, dòng breadcrumb, dòng mô tả nhóm gia hạn, tooltip nút drill và ô lọc hàng hoá |

⚠️ **Bẫy đã trả giá ở vòng này:** đổi thứ tự trong `colgroup`/`COLS` mà quên đổi thứ tự render ô
trong `nodeRow` làm **toàn bảng lệch đúng 1 nhịp** — cột "Mã hàng hoá" hiện ra tên hàng, cột tên bị
bóp còn 1 chữ/dòng. Ô Mã phải tách khỏi cụm thuộc tính (`codeTd` riêng, `attrTds` cho 4 ô còn lại)
vì nó nằm ở phía TRƯỚC cột tên còn cụm kia nằm phía SAU.

## Bổ sung vòng 5 (2026-09-12)

| # | Yêu cầu | Cách làm |
|---|---------|----------|
| 20 | "Số lượng" → **"Số lượng giữ"** | Đổi nhãn cột |
| 21 | **Bỏ cột Mã hàng riêng** | Cột riêng rỗng ở dòng Phòng ban / Nhân viên làm vỡ cấu trúc cây. Mã đi liền tên trong CÙNG ô theo khuôn **"Mã hàng - Tên hàng"**, mã có style riêng (`.prd-code`: 11px, xám `#64748b`, nền `#f1f5f9`, giãn chữ) để không bị đọc nhầm thành một phần của tên. Áp cho **toàn bộ báo cáo**: bảng chính, popup danh sách lô, popup gia hạn, tiêu đề popup |
| 22 | Sort cho **Mã - Tên hàng · Nhân viên · Hạn giữ · Ngày bắt đầu giữ** | Bảng chính: nút sort trên cột "Nội dung theo dõi" (A→Z → Z→A → **về mặc định**). Popup: header bấm được ở 4 cột trên, cùng chu kỳ 3 trạng thái |
| 23 | Popup theo nhân viên hiện **"Tên - Phòng ban"** | `empLabelDept()` — dùng ở cột "Nhân viên giữ" và tiêu đề popup: *"…theo Nhân viên: Nguyễn Thị Cần - Phòng Kinh doanh 1"*. Khác khuôn select toàn hệ thống (`Tên - Mã phòng - Mã NV`) vì ở báo cáo này người đọc cần tên PHÒNG, không cần mã |
| 24 | Bảng chi tiết thêm **Số hợp đồng** + **Tổng thanh toán** | Giữ hàng có 2 kiểu, **cả hai đều có khách hàng**: theo hợp đồng (`product_prepick_requests.contractable_type = FirmContract`) và không theo hợp đồng (`NULL`). Dữ liệu thật: **501 / 1.673** phiếu (~23%). Lô không có hợp đồng ghi rõ *"Không theo hợp đồng"*, cột tiền để `—` |
| 25 | Bấm Tổng thanh toán → popup phiếu thu | Nguồn: `bill_income_details` lọc `objectable_type = FirmContract` + `objectable_id = <id hợp đồng>`, cộng `income_money_real` của phiếu **đã duyệt**. Có thật: **6.734 dòng thu / 26.349 tỷ**, 352 hợp đồng đang có hàng giữ. Popup hiện giá trị HĐ · đã thanh toán · số phiếu thu + danh sách phiếu (số phiếu · ngày · người nộp · số tiền · nội dung) |
| 27 | **KHÔNG hiện "Còn phải thu"** | Popup này chỉ gom PHIẾU THU, chưa phải công nợ. Công nợ thật còn phụ thuộc giảm giá, thuế, bù trừ, các khoản khác — lấy `giá trị HĐ − đã thu` rồi gọi là công nợ là ra số sai. Muốn công nợ phải đọc từ nghiệp vụ công nợ, không suy diễn ở màn này |
| 26 | **Thứ tự mặc định toàn báo cáo** | Chứng từ xếp **MỚI → CŨ** (phiếu thu). Riêng hàng giữ xếp **quá hạn nhiều nhất → trong hạn**: bảng chính sắp node theo số lô quá hạn giảm dần, popup danh sách lô sắp theo hạn giữ tăng dần. User tự sort cột thì theo user; bấm hết chu kỳ sort quay về đúng thứ tự mặc định này |

⚠️ **Bẫy lặp lại lần 2:** `.drill-table { min-width: 1740px }` — vòng trước đã override cho `#ext-modal`,
vòng này thêm popup phiếu thu lại quên, nên bảng bị ép 1740px và **cắt mất 2 cột cuối** (Số tiền, Nội
dung). Selector nay liệt kê cả hai popup; **thêm popup mới thì phải thêm selector**.

## Bổ sung vòng 6 (2026-09-12) — sửa 2 chỗ định nghĩa sai

### 28 · Cột "Tồn hiện tại" chỉ có ở tiêu chí HÀNG HOÁ

Bỏ khỏi **popup chi tiết** và khỏi bảng khi xem theo tiêu chí **Nhân viên**. Lý do: tồn kho là con
số của **cả công ty**, đặt cạnh số lượng giữ của từng lô / từng nhân viên là mời người đọc so hai
đại lượng không so được. Chỉ khi bổ dọc theo hàng hoá thì "tồn 907 · đang giữ 684" mới có nghĩa.

### 29 · Bộ lọc **Hình thức giữ**: Tất cả / Giữ theo hợp đồng / Không theo hợp đồng

Lọc theo `product_prepick_requests.contractable_type` (NULL = không theo hợp đồng). Cả hai kiểu đều
bắt buộc có khách hàng.

### 30 · Đo bằng SỐ MÃ hay SỐ LƯỢNG — quyết định theo DÒNG, không theo cấp

**Định nghĩa cũ sai:** "dòng Phòng ban/Nhân viên = số mã, dòng Hàng hoá = số lượng". Ở tiêu chí
**Hàng hoá** thì dòng Nhân viên nằm DƯỚI một mã hàng nên số mã luôn bằng 1 — vô nghĩa.

**Định nghĩa đúng:** dòng gom **đúng 1 mã hàng** → đo bằng **số lượng** (theo đơn vị đang chọn);
dòng gom **nhiều mã** → đo bằng **số mã**. Mục đích đếm mã chỉ là để không cộng thẳng số lượng của
các đơn vị tính khác nhau — hết lý do đó thì phải quay về số lượng.

| Dòng | Tiêu chí Nhân viên | Tiêu chí Hàng hoá |
|---|---|---|
| TỔNG | số mã | số mã |
| Phòng ban | số mã | — |
| Nhân viên | số mã | **số lượng** (nằm dưới 1 mã) |
| Hàng hoá | số lượng | số lượng |

Quy tắc này cũng tự đúng khi bộ lọc thu về đúng 1 mã hàng: lúc đó cả dòng TỔNG cũng hiện số lượng.
Cài bằng `metrics().onlyProductId` (mã duy nhất của dòng, `null` nếu nhiều mã) — 3 cột hạn dùng
chung cờ đó nên không bao giờ lệch đơn vị với cột "Số lượng giữ".

## Bổ sung vòng 7 (2026-09-12)

| # | Yêu cầu | Cách làm |
|---|---------|----------|
| 31 | **Bỏ chế độ đổi đơn vị trên báo cáo** | Luôn quy về **đơn vị cơ bản** (`prepick_details.qty` vốn đã là ĐVT cơ bản). Cột "Đơn vị" chỉ để ĐỌC. Lý do: cho đổi ĐVT ngay trên báo cáo thì mỗi người xem một kiểu, số trên màn không khớp số xuất Excel, và dòng tổng cộng lẫn lộn nhiều hệ số |
| 32 | Khối tổng hợp 1 đổi thành **"Tình trạng theo yêu cầu giữ"** | 3 ô: **Tổng yêu cầu đang giữ hàng · Yêu cầu sắp hết hạn · Yêu cầu đã hết hạn**. Đếm theo **chứng từ gốc** (Phiếu xuất giữ · Nhập hàng cho khách · Điều chuyển giữ), không đếm lô |
| 33 | Khối "Phạm vi đang giữ" | Giữ nguyên |
| 34 | Sort thêm trong popup: **Phòng ban · Số lượng đang giữ · Khách hàng** | Popup nay sort được 7 cột: Mã-Tên hàng · SL đang giữ · Khách hàng · Nhân viên giữ · Phòng ban · Ngày bắt đầu giữ · Hạn giữ hiện tại |

⚠️ **Hai nhóm "sắp hết hạn" / "đã hết hạn" của khối yêu cầu CHỒNG LẤN nhau** — một yêu cầu giữ đẻ
nhiều lô hạn khác nhau, nên nó được tính vào nhóm nào có ÍT NHẤT một lô rơi vào. Không cộng 2 số này
lại thành tổng. Bấm vào số mở danh sách **toàn bộ lô của các yêu cầu trúng nhóm** (nhiều hơn số lô
thuần ở trạng thái đó) — tooltip đã ghi rõ.

⚠️ **Bẫy đã trả giá:** xoá rule `.unit-select` bằng cách cắt đoạn giữa 2 mốc comment đã **cắt nhầm cả
khối CSS phía sau** — mất `.rsum-tb` min-width, màu 3 cột hạn, `.unit-sub`, `.prd-code`, `.sort-btn`,
`.code-sub`, `.na-cell`… Triệu chứng lộ ra trên màn: nhãn ra **"22MÃ"** (dính số + viết hoa theo dòng
TỔNG) và nút sort mang **viền outset 2px + nền #efefef** mặc định của trình duyệt. Cắt CSS theo mốc
comment phải kiểm lại danh sách selector còn sống, đừng tin vào việc file vẫn hợp lệ.
Ghi chú thêm: `.sort-btn` phải dùng `all: unset` chứ `border: 0` không đủ để gỡ khuôn button mặc định.

## Bổ sung vòng 8 (2026-09-12)

| # | Yêu cầu | Cách làm |
|---|---------|----------|
| 35 | Tiêu đề cột có sort **không đổi màu nền khi hover** | Header bảng popup là nền SÁNG (gradient `#f3fdfe → #e2f6f9`) chữ teal `#0a7c88`; tô nền teal đậm khi hover là chữ teal trên nền teal — mất chữ. Phải **ghi đè cả rule hover có sẵn trong khối style gốc** (`background: linear-gradient(#eafcfe,#d3f1f6)`), không thì nền vẫn đổi. Báo hiệu bấm được bằng gạch chân + mũi tên đậm lên |
| 36 | Khối hạn giữ thêm **"NV có hàng giữ quá hạn"** | Đếm distinct nhân viên có ít nhất 1 lô đã quá hạn, kèm mẫu số "trên N người đang giữ". Khác "Yêu cầu đã hết hạn" — một người có thể ôm nhiều yêu cầu quá hạn. Bấm vào số mở danh sách lô quá hạn. Khối 1 nay có **4 ô** và vẫn nằm gọn trong 1 hàng (đo: không tràn, dải tổng hợp không sinh cuộn ngang) |

ℹ️ Dữ liệu demo hiện cho ra "10 trên 10 người" vì bộ lô mẫu có 66% quá hạn — dữ liệu thật ở local
còn cực đoan hơn (**2.412/2.412 lô đang quá hạn**). Trên production con số này sẽ tách ra.

## Bổ sung vòng 9 (2026-09-12) — bỏ thuật ngữ "lô" + sửa mô hình dữ liệu demo

### 37 · Không dùng chữ "lô" trên giao diện

Chữ "lô" tôi dùng ở các bản trước trỏ tới **1 dòng `prepick_details`** = tổ hợp duy nhất của
**(nhân viên × khách hàng × hàng hoá × công ty × hạn giữ)**. Đã kiểm: 2.412 dòng đang có hàng,
**0 nhóm trùng** bộ 5 đó. Gia hạn thì trừ dòng cũ và **đẻ dòng mới** với hạn mới.

**Vì sao phải bỏ:** hệ thống ĐÃ CÓ lô hàng thật ở `warehouse_import_lots` — **36.613 bản ghi**,
`lot_number` UNIQUE, có `remain_qty`. Hàng giữ không gắn lô nhập, không gắn kho, không có số lô.
Mượn lại chữ "lô" là khiến người đọc tưởng đang theo dõi lô hàng vật lý.

**Chốt:** giao diện chỉ đếm theo **YÊU CẦU GIỮ** (chứng từ gốc) và **MÃ HÀNG**. Mọi nhãn / tooltip /
tiêu đề popup / dòng đếm đã đổi; số dòng đang xem đọc ở cột STT của bảng. Quét lại toàn bộ text +
tooltip + 3 popup: chỉ còn 2 câu chứa chữ đó, và cả hai là câu **cảnh báo "KHÔNG phải lô kho"**.

### 38 · Sửa mô hình dữ liệu demo: 1 yêu cầu giữ → nhiều dòng

**Sai ở bản trước:** mỗi dòng hàng giữ được gán một mã chứng từ gốc **ngẫu nhiên riêng**, nên "số
yêu cầu giữ" gần bằng số dòng; con số 199/214 chỉ là kết quả **trùng mã tình cờ**, không có nghĩa
nghiệp vụ.

**Số liệu thật:** 2.311 dòng còn hàng / **1.441 chứng từ gốc** ≈ **1,6 dòng mỗi yêu cầu**;
1.365/1.441 yêu cầu chỉ còn 1 dòng, phần còn lại 2–11 dòng. (Phiếu xuất giữ lúc lập trung bình
5,19 dòng hàng, tối đa 134 — nhưng phần lớn đã xuất/huỷ hết nên tới lúc xem chỉ còn 1 dòng.)

**Đã sửa:** sinh dữ liệu theo chứng từ — mỗi yêu cầu giữ lập cho **đúng 1 khách hàng + 1 nhân
viên**, gồm nhiều mặt hàng khác nhau; hợp đồng gắn trên **phiếu** nên mọi dòng cùng yêu cầu có
cùng hợp đồng. Kiểm lại: 180 dòng / 139 yêu cầu, 26 yêu cầu nhiều dòng, **0 vi phạm** quy tắc
"cùng yêu cầu ⇒ cùng khách + cùng nhân viên".

### 39 · Đổi vị trí 2 khối tổng hợp

Thứ tự mới: **"Phạm vi đang giữ"** (trái) → **"Tình trạng theo yêu cầu giữ"** (phải).
Đọc từ quy mô trước rồi mới tới mức độ cấp bách.

### 40 · Cột "Nhân viên giữ" trong popup chỉ hiện TÊN

Popup đã có cột **Phòng ban** riêng ngay bên cạnh; ghép thêm tên phòng vào cột nhân viên là lặp
đúng một thông tin ở hai cột liền nhau. Khi cột Phòng ban bị ẩn (popup mở từ chính một phòng ban
hoặc một nhân viên) thì phòng đã nằm ở **tiêu đề popup** nên không mất thông tin:

| Popup mở từ | Cột Nhân viên | Cột Phòng ban | Tiêu đề |
|---|---|---|---|
| Toàn báo cáo | `Bùi Thị Ngọc` | `Phòng Dự án` | — |
| Một phòng ban | `Lê Minh Đức` | *(ẩn)* | …theo Phòng ban: **Phòng Kinh doanh 1** |
| Một nhân viên | *(ẩn)* | *(ẩn)* | …theo Nhân viên: **Nguyễn Thị Cần - Phòng Kinh doanh 1** |

Khuôn "Tên - Phòng ban" vẫn giữ ở **tiêu đề popup** (chốt ở vòng 5).

### 41 · Lối tắt "Hàng giữ của tôi"

Nút bật/tắt đặt **đầu thanh lọc** (không nằm trong dãy select, vì nó đổi một lúc 5 thứ chứ không
phải một ô lọc). Bật lên thì nền teal đặc để user biết báo cáo đang ở chế độ lọc riêng.

**Bật** → ép: tiêu chí `Theo nhân viên` · công ty của tôi · phòng ban của tôi · nhân viên = tôi ·
cấp bung = `Tất cả cấp (đến Hàng hoá)`.
⚠️ Phải set **cả công ty và phòng ban** của chính người đó — bộ lọc là cascade, đang đứng ở công ty
khác mà chỉ set `employee_id` thì ra bảng rỗng và không nói vì sao.
⚠️ Đã bó về đúng 1 người thì dừng ở cấp Phòng ban / Nhân viên là vô nghĩa → bung thẳng tới Hàng hoá.

**Tắt bằng chính nút đó** → khôi phục **đúng bộ lọc trước khi bật** (ảnh chụp 5 giá trị), không đưa
về mặc định.

**Đổi tay** ô Nhân viên / Công ty / Phòng ban / Tiêu chí khi đang bật → **tắt cờ nhưng GIỮ lựa chọn
user vừa chọn**, không khôi phục ảnh chụp: user đang chủ động đi hướng khác, kéo bộ lọc về chỗ cũ là
cướp thao tác của họ. Nút "Xoá lọc" cũng tắt cờ.

**BE**: id người đăng nhập lấy `auth()->id()` (= `employees.id`), **không** dùng
`auth()->user()->info->id` (đó là id bảng `employee_infos`).

ℹ️ Khi chỉ còn 1 nhân viên, dòng Phòng ban và dòng Nhân viên hiện cùng một con số — có thể cân nhắc
ẩn 2 cấp trên ở chế độ này, nhưng chưa làm vì user chưa yêu cầu.

### 42 · ĐỊNH NGHĨA CHỐT — "Số yêu cầu giữ" (13/09/2026)

> **1 yêu cầu giữ = PHIẾU yêu cầu giữ + MÃ HÀNG + NHÂN VIÊN**
> Một phiếu của nhân viên A xin giữ 5 mã hàng ⇒ đếm là **5 yêu cầu giữ**.

Thay cho định nghĩa cũ ("1 yêu cầu = 1 chứng từ gốc"). Hệ quả phải biết — đo trên DB thật:

| Đơn vị | Số lượng |
|---|---|
| Dòng hàng giữ (`prepick_details` còn hàng) | **2.412** |
| **Yêu cầu giữ** (định nghĩa mới) | **2.410** |
| Phiếu / chứng từ gốc | **593** |

⇒ Đây là **đơn vị đếm chi tiết**, gần như *mỗi dòng hàng giữ là một yêu cầu*, KHÔNG phải đếm chứng
từ (593). Một yêu cầu chỉ còn nhiều dòng khi gia hạn tách một phần số lượng sang hạn mới — thực tế
đúng **2 trường hợp** trên 2.412 dòng.

**Cài đặt:** khoá đếm `source|product_id|employee_id`, dùng CHUNG ở `metrics()` và ở bộ lọc drill
của popup — lọc nhầm theo mỗi mã phiếu sẽ kéo theo các mã hàng khác của cùng phiếu và con số popup
không khớp khối tổng hợp. Đã đối chiếu: khối tổng hợp 180 ↔ popup 180 ↔ đếm lại từ DOM 180.

**Đổi nhãn cho khỏi lẫn:** cột trong popup từ *"Yêu cầu giữ gốc"* → **"Phiếu giữ gốc"**, vì nó hiện
mã CHỨNG TỪ, còn "yêu cầu giữ" nay là đơn vị đếm.

### 43 · ⚠️ RÀNG BUỘC BE — phải LẦN NGƯỢC về chứng từ gốc trước khi đếm

Gia hạn tạo **bản ghi `prepick_details` MỚI** (trừ bản ghi cũ, cộng sang bản ghi hạn mới), nên nếu BE
lấy thẳng `prepick_details.objectable_id` làm khoá đếm thì hỏng. Đã đo trên DB thật:

| Cách làm | Số yêu cầu | Ghi chú |
|---|---|---|
| Đếm THÔ theo `objectable` của chính bản ghi | 2.411 | — |
| Đếm ĐÚNG, lần ngược về chứng từ gốc | **2.410** | — |

**Đếm chồng thực tế chỉ 1 trường hợp** — vì gia hạn thường rút HẾT bản ghi cũ (`qty = 0`) nên nó rơi
khỏi báo cáo, chỉ khi **gia hạn một phần số lượng** mới còn 2 bản ghi sống cùng một yêu cầu.

**Nhưng thiệt hại lớn hơn nằm ở chỗ khác:** có **1.111 / 2.412 bản ghi đang còn hàng (46%)** mang
`objectable_type = PrepickExtendRequestDetail`. Đếm thô thì cột **"Phiếu giữ gốc"** của 46% số dòng
sẽ hiện **mã phiếu GIA HẠN** thay vì phiếu xuất giữ gốc — sai chứng từ, không lần ra được nguồn.

**Chốt cho lúc code:**
- Khoá đếm và cột "Phiếu giữ gốc" đều phải lấy từ **gốc chuỗi**: đệ quy `objectable_id` →
  `prepick_extend_request_details.prepick_detail_id` → bản ghi nguồn → lặp (MySQL 8 có recursive CTE).
- Nếu recursive CTE quá nặng cho báo cáo chạy thường xuyên → cân nhắc **denormalize**: thêm cột
  `root_objectable_id` / `root_objectable_type` vào `prepick_details`, ghi ngay trong
  `moveToExpireDate()` khi tạo bản ghi mới (copy gốc từ bản ghi nguồn). ⚠️ Đây là bảng **dùng chung
  với ERP** nên phải hỏi trước khi thêm cột.

**Mockup đã mô phỏng đúng ca này:** thêm ~8% dòng "gia hạn một phần" (cùng phiếu + mã hàng + nhân
viên, khác hạn). Kết quả kiểm: **185 dòng → 175 yêu cầu**, 10 yêu cầu có 2 dòng, và con số khớp giữa
khối tổng hợp ↔ popup ↔ đếm lại từ DOM.

## PHÂN QUYỀN — chốt 13/09/2026 (note cho implement)

### Quy tắc

Báo cáo dùng **ĐÚNG MỘT quyền**: **`Xem báo cáo giữ hàng theo tổng công ty`**

| | CÓ quyền | KHÔNG có quyền |
|---|---|---|
| Ô chọn Công ty | **Hiện**, có thêm mục **"Tất cả công ty"** | **Ẩn hẳn** |
| Phạm vi dữ liệu | Công ty tự chọn, hoặc toàn bộ công ty | Khoá theo **công ty trong hồ sơ nhân sự** |

Không dùng bộ 3 quyền phạm vi (`… theo tổng công ty / theo công ty / theo phòng ban`) mà
`PrepickStockReportService` đang áp cho màn cũ — màn báo cáo mới chỉ 1 quyền.

### ⚠️ Quyền này CHƯA TỒN TẠI — phải thêm

Đã tra bảng `permissions`: chỉ có 9 quyền liên quan hàng giữ, **không có** quyền này. Gần nhất là
`Xem phiếu hàng giữ theo tổng công ty` (id 100839) — của màn PHIẾU, tên khác, đừng dùng nhầm.

Phải thêm vào `Modules/Timesheet/Database/Seeders/PermissionsTableSeeder.php` (không tạo migration
riêng cho permission). ⚠️ Seeder này **truncate cả bảng**, và `role_has_permissions` cần
`company_id = 1` — xem ghi chú ở feature `hrm-them-permission-moi`.

### Ràng buộc khi code

- **Cờ quyền FE fail-closed**: khởi tạo `false`, chỉ bật từ `$store.state.permissions`. TUYỆT ĐỐI
  không gán literal `true`.
- **BE là chốt chặn thật**: không có quyền thì BE tự ép `company_id` = công ty trong hồ sơ, **không
  đọc `company_id` do FE gửi lên**. Ẩn ô lọc ở FE chỉ là lớp trải nghiệm.
- **Nút "Xoá lọc" KHÔNG được reset `company`** — với người không có quyền đó là phạm vi bị khoá,
  xoá đi là mở rộng quyền xem bằng một cú bấm. Đã xử lý trong mockup.
- **Lối tắt "Hàng giữ của tôi"** không đụng tới `company` khi user không có quyền.
- Khoá phạm vi **ngay lúc khởi tạo**, trước lần render đầu tiên, để không có khoảnh khắc nào dữ
  liệu công ty khác lọt ra màn.
- Người không có quyền vẫn phải **thấy mình đang xem công ty nào**: thay ô chọn bằng nhãn tĩnh
  (`.company-fixed`), không ẩn im lặng — ẩn trơn thì user tưởng báo cáo thiếu dữ liệu.
- Xem **"Tất cả công ty"** thì cột **Tồn hiện tại** phải **cộng tồn của mọi công ty**; lấy tồn một
  công ty đặt cạnh số đang giữ của toàn bộ là hai vế khác phạm vi. Đã kiểm: tất cả `1,058` vs một
  công ty `602`.

### Đã chốt nốt (13/09/2026)

1. **KHÔNG gate vào màn.** Màn báo cáo mới **không dùng** quyền `Quản lý giữ hàng` (id 100427) mà màn
   cũ `/finance/prepick-stocks` đang gate. Mọi user đăng nhập đều vào được báo cáo.
2. **Không giới hạn theo phòng ban.** Người không có quyền xem tổng công ty vẫn xem **toàn bộ hàng
   giữ của công ty mình** — không bó về phòng ban, không bó về "chỉ của tôi".

⇒ Tổng kết quyền của màn: **đúng 1 quyền duy nhất**, và nó chỉ quyết định **phạm vi công ty**
(một công ty tự chọn / tất cả công ty), không quyết định việc được vào màn hay không.

⚠️ Hệ quả để biết khi bàn giao: hàng giữ của **toàn công ty** hiển thị cho mọi nhân viên đăng nhập.
Nếu sau này cần siết, chỗ siết là thêm gate vào màn — không phải sửa quy tắc phạm vi.

### Xem thử 2 trạng thái trên mockup

Mặc định là **có quyền**. Thêm `?noPerm=1` vào URL để xem trạng thái **không có quyền**
(ô chọn công ty biến mất, còn nhãn tĩnh; dữ liệu chỉ còn 4 phòng của 1 công ty).

## PHÂN TRANG — chốt 13/09/2026 (đã làm vào mockup)

### Bảng chính — phân trang theo NODE CẤP 1

Mỗi trang = **N node cấp 1 + toàn bộ cấp con của chúng**. KHÔNG phân trang theo dòng render: bảng là
cây, bung/thu một nhánh sẽ đẩy nội dung chạy sang trang khác và số trang nhảy liên tục.

- Cỡ trang mặc định **25**, cho chọn 10/25/50/100.
- Đơn vị đếm ghi đúng thứ đang phân trang: *"Hiển thị 11–20 / 21 **hàng hoá**"* (tiêu chí Hàng hoá)
  hoặc *phòng ban* (tiêu chí Nhân viên) — không ghi "dòng", vì mỗi trang còn kéo theo cấp con.
- **STT chạy tiếp theo toàn bộ danh sách**, trang 2 bắt đầu từ 11 chứ không đánh lại từ 1.
- Quy mô thật: cấp 1 của tiêu chí Hàng hoá là **895 mã** → bắt buộc phân trang; tiêu chí Nhân viên
  chỉ 17 phòng → thực tế gọn 1 trang nhưng vẫn dùng chung cơ chế.

### ⚠️ Dòng TỔNG và dải tổng hợp KHÔNG theo trang

Luôn tính trên **toàn bộ dữ liệu đã lọc**. Đã kiểm bằng số: chuyển từ trang 1 sang trang 2, dòng
TỔNG giữ nguyên `21 Mã | 15 | 4 | 20`. Khi làm BE thì đây là **2 truy vấn tách bạch** — một cho tổng
hợp, một cho trang.

### Popup — phân trang theo dòng

- Cỡ trang mặc định **20**, cho chọn 10/25/50/100; giữ cỡ trang user đã chọn khi mở popup khác.
- STT cũng chạy tiếp: trang 2 bắt đầu từ 21, trang 4 từ 61.
- Dòng đếm (`21 mã hàng · 175 yêu cầu giữ · 5 đơn vị tính`) tính trên **toàn bộ kết quả lọc**, không
  phải trang đang xem.
- Popup **lịch sử gia hạn** (tối đa 10 lần) và **phiếu thu** (thường < 10 phiếu) **không phân trang**.

### Về trang 1 khi nào

Đổi bộ lọc · đổi tiêu chí · đổi ngưỡng cảnh báo · Xoá lọc · bật/tắt "Hàng giữ của tôi" · **đổi sắp
xếp**. Sort chạy trên toàn bộ rồi mới cắt trang — ở lại trang cũ sau khi sort là nhìn vào lát cắt vô
nghĩa. Đổi **cấp bung** thì KHÔNG đổi trang (số node cấp 1 không đổi).

### Khi làm BE (phân trang)

- **Sort ở server, trên toàn bộ, rồi mới cắt trang.** Nút sort cột "Nội dung theo dõi" và 7 cột sort
  của popup đều phải đẩy lên server.
- **Cấp sâu nhất lazy load**: 1 nhân viên có tới 151 mã hàng (TB 30,4) → trả sẵn cấp 1 + cấp 2, cấp 3
  gọi riêng khi bung.
- **In / Xuất Excel lấy toàn bộ theo bộ lọc**, không theo trang.
- Dùng lại `components/V2BasePagination.vue` + khuôn server-side của
  `pages/assign/report/prospective-projects` (`current_page` / `per_page`, BE `paginate()`).

## Bổ sung vòng 10 (2026-09-14) — lọc Bộ phận · đổi thứ tự cột popup · ghim cột · In/Excel

### 44 · Bộ lọc **Bộ phận** (cấp con của Phòng ban) — chỉ là Ô LỌC, không phải cấp của cây

Cascade `Công ty ▸ Phòng ban ▸ Bộ phận ▸ Nhân viên`. `parts.department_id` là cấp cha, nhân viên gắn
qua `employee_infos.part_id`. `prepick_details` KHÔNG có `part_id` (cũng không có `department_id`) →
phạm vi bộ phận phải quy về **danh sách `employee_id`**, y như cách màn đang làm với phòng ban.

**⚠️ ĐO TRÊN DB THẬT `hrm_erp` — dữ liệu bộ phận gần như TRỐNG:**

| Chỉ tiêu | Số |
|---|---|
| Bộ phận / phòng ban toàn hệ thống | 25 bộ phận · chỉ **8/84 phòng** có chia |
| Nhân viên có `part_id` | 275 / 1.109 (24,8%) |
| **Nhân viên ĐANG GIỮ HÀNG có bộ phận** | **5 / 74** |
| **Dòng hàng giữ có bộ phận** | **63 / 2.412 (2,6%)** |
| **Phòng đang giữ hàng có bộ phận** | **1 / 17** (PHÒNG KINH DOANH THƯƠNG MẠI, 6 bộ phận) |

⇒ Đây là lý do **KHÔNG thêm Bộ phận thành một cấp của cây**: 16/17 nhánh sẽ đẻ ra "Chưa phân bộ phận"
ôm gần hết dữ liệu, cây dài thêm một tầng mà không chia được gì.

**3 trạng thái bắt buộc của ô lọc** — không bao giờ để rỗng im lặng (trạng thái "khoá" mới là ca
thường gặp, bỏ mặc ô rỗng thì user tưởng báo cáo hỏng):

| Tình huống | Ô Bộ phận |
|---|---|
| Chưa chọn phòng ban | Khoá, ghi *"Chọn phòng ban trước"* |
| Phòng chưa chia bộ phận | Khoá, ghi *"Phòng này chưa chia bộ phận"* |
| Phòng có bộ phận | Liệt kê + mục **"Chưa phân bộ phận"** (`value = none`) |

- Mục **"Chưa phân bộ phận"** chỉ hiện khi phòng thực sự còn nhân viên chưa gán. **Bỏ mục này là lọc
  bộ phận nuốt mất nhóm đó** — cộng các bộ phận lại không ra tổng của phòng mà không ai biết vì sao.
  Đo kiểm trên mockup: `21 + 17 + 29 = 67` = đúng tổng của phòng, không mất dòng nào.
- Chỉ liệt kê bộ phận **thực sự đang giữ hàng** (cùng quy tắc với ô Nhân viên).
- Đổi Phòng ban → **reset Bộ phận**; giữ lại id bộ phận của phòng cũ là lọc theo bộ phận không thuộc
  phòng đang chọn → bảng rỗng vô lý.
- Chọn Bộ phận → nạp lại ô **Nhân viên** cho khớp, nếu không user chọn được người ngoài bộ phận đang lọc.
- *Xoá lọc* reset bộ phận (vẫn **không** reset công ty). *Hàng giữ của tôi* nay ép **6 giá trị**
  (thêm bộ phận của chính mình); người chưa gán bộ phận thì để "Tất cả", **không** ép `none` — `none`
  là nhóm lọc thật (cả phòng chưa phân bộ phận) chứ không phải "của tôi".

**BE**: lọc bộ phận = thêm điều kiện vào tập `employee_id`; `part = none` ⇒ `part_id IS NULL`.

### 45 · Popup chi tiết — 3 cột vòng đời hàng giữ chuyển lên NGAY SAU "SL đang giữ"

```
STT · Mã hàng - Tên hàng · ĐVT · SL đang giữ · Ngày bắt đầu giữ · Hạn giữ hiện tại ·
Số lần gia hạn · Thương hiệu/Model · Khách hàng · Số hợp đồng · Tổng thanh toán ·
Nhân viên giữ · Phòng ban · Trạng thái · Phiếu giữ gốc
```

Trước đây 3 cột này ở vị trí 11–13: muốn xem hạn giữ là phải cuộn hết bảng 15 cột. Nay nằm sát khối
cột được ghim nên đọc được cùng lúc với mã hàng.

### 46 · Ghim 3 cột đầu popup khi cuộn ngang (STT · Mã hàng - Tên hàng · ĐVT)

Bảng rộng 2.088px trong khung ~1.300px — cuộn sang phải là mất luôn mã hàng, không còn biết dòng
đang đọc là mặt hàng nào. Chỉ áp cho **popup danh sách chi tiết**; popup *lịch sử gia hạn* và
*phiếu thu* đã đặt `min-width: 0` nên không hề tràn ngang.

**⚠️ 3 bẫy đã trả giá, mất 3 lần đo mới ra nguyên nhân thật:**

1. **`left` không hard-code được.** Bảng `table-layout: fixed` + `min-width: 1740px`: khi tổng bề
   rộng khai trong `<colgroup>` khác bề rộng thật của bảng, trình duyệt **co giãn mọi cột theo tỉ lệ**.
2. **`getBoundingClientRect` trả toạ độ SAU transform.** Popup mở kèm `transform: scale(.96)` nên mọi
   khoảng cách bị nhân 0,96 — đo ra `301.44px` thay vì `314px` (đúng bằng 314 × 0,96), ghim lệch 13px,
   3 cột ghim đè lên nhau. Màn hình **không báo lỗi gì**, chỉ trông "hơi lệch".
   → Dùng **`offsetLeft`** (số đo layout, miễn nhiễm transform). `ResizeObserver` KHÔNG cứu được ca
   này vì transform không làm đổi kích thước layout nên observer không hề kêu.
3. **`border-collapse: collapse` làm ô ghim mất viền** khi trượt qua (viền thuộc về bảng, không thuộc
   ô) và **nền trong suốt** để nội dung cột sau chạy xuyên qua. → vẽ lại viền bằng `box-shadow inset`,
   nền ô ghim phải ĐẶC và đổi đúng theo trạng thái hover.

Đo sau khi sửa: cuộn ngang 900px, 3 cột ghim lệch **1px** (viền container), khít nhau, cột 4 cuộn đi.
Phải đo lại offset mỗi khi bảng đổi bề rộng (phóng to popup, đổi cỡ cửa sổ).

### 47 · In / Xuất Excel — 4 đường, đều lấy TOÀN BỘ theo bộ lọc

| Nút | Nội dung |
|---|---|
| **In báo cáo** (thanh tiêu đề) | Popup chọn chế độ: *In bảng theo dõi* / *In danh sách chi tiết* |
| **Xuất Excel** (thanh tiêu đề) | Bảng theo dõi, đủ mọi cấp |
| **In danh sách** (popup chi tiết) | Danh sách chi tiết theo bộ lọc của popup |
| **Xuất Excel danh sách** (popup chi tiết) | Như trên |

- Bản in **A4 ngang**, có dòng tóm tắt bộ lọc đang áp (thiếu dòng này thì 2 bản in của 2 bộ lọc khác
  nhau nhìn y hệt).
- **KHÔNG theo trang, KHÔNG phụ thuộc cấp đang bung**: dựng lại cây đủ mọi cấp thay vì đọc `TREE` của
  lần render gần nhất. Đo kiểm: trang 1 và trang 2 in ra **cùng 73 dòng**; `level = 0` (chưa bung) vẫn
  có dòng hàng hoá; popup hiện 20 dòng/trang nhưng xuất ra **185 dòng**.
- Bản chữ của ô đo dùng **chung quy tắc** với `measureTd()` — nếu không bản in ghi "14" còn màn hình
  ghi "14 Mã" và không ai biết bên nào đúng.
- Bảng chi tiết 15 cột **vừa đúng khổ**: đo `scrollWidth` 1.046px / khung giấy 1.047px, không tràn.
- ⚠️ **Bẫy khi đổ HTML ra text phẳng**: các mẩu trong `<span>` dính liền nhau —
  `"VT.00611-Ống thủy lực"`, `"Công ty CP Đóng tàu Hạ Long21TPHP-176"`. Phải chèn khoảng trắng
  **2 phía** mỗi span (1 phía vẫn dính đầu bên kia), mã phụ `.code-sub` tách bằng `" · "`.
- ⚠️ **Thụt lề cây phải dùng khoảng trắng CỨNG (` `)**: HTML gộp mọi khoảng trắng liền nhau
  thành 1, Excel cũng cắt khoảng trắng đầu ô → thụt lề bằng dấu cách thường là mất sạch cấu trúc cây.
- Lấy tiêu đề popup **trước** khi đóng popup: `closeDrill()` xoá `state.drillKey`.
- **BE**: bản thật xuất Excel từ server theo `.claude/skills/export-excel/SKILL.md` — ô số phải là
  **SỐ THẬT + `numFmt` `#,##0`**, không đổ chuỗi đã format sẵn. Danh sách chi tiết 2.412 dòng × 15 cột
  nên bám mục 14c của `list-page` (chia trang `export-rows` rồi dựng file ở FE) nếu quá 2s.

### 48 · 2 nút **Gia hạn** / **Huỷ giữ** nằm TRONG ô "Hạn giữ hiện tại"

Nút **icon + chữ**, đặt ngay **trong ô "Hạn giữ hiện tại"** (dưới dòng *"còn N ngày / quá hạn N
ngày"*) — **KHÔNG tách thành cột Hành động riêng**. Chốt 2026-09-14 sau 1 vòng thử cột riêng.

Lý do: bảng đã 15 cột, thêm cột nữa là tốn chỗ ngang; và hạn giữ với việc phải làm về cái hạn đó
nên đọc **cùng một chỗ**. Đo: ô rộng 196px, 2 nút 70/71 × 22px nằm gọn 1 hàng, dòng cao đều 76px,
bảng vẫn 15 cột ở cả 2 chế độ.

Chỉ hiện khi bật lối tắt **"Hàng giữ của tôi"** — ngoài chế độ đó danh sách là hàng của NGƯỜI KHÁC,
không ai lập phiếu gia hạn / hủy giữ hộ được. (Đo: chế độ thường 0 nút, chế độ của tôi 20/20 dòng.)

| Nút | Màn đích | Icon | Màu |
|---|---|---|---|
| **Gia hạn** | `/finance/prepick-extend-requests/create?prepick_detail_id=<id>` | `ri-calendar-check-line` | teal |
| **Huỷ giữ** | `/finance/prepick-cancel-requests/create?prepick_detail_id=<id>` | `ri-close-circle-line` | đỏ (nhóm phá huỷ) |

- Bản thật: `V2BaseButton size="sm"` + icon qua slot `#prefix` (đúng `button-convention` mục 1).
- **Dạng VIỀN, không phải nút đặc**: 20 dòng × 2 nút teal/đỏ đặc thì cả bảng thành một mảng màu,
  không còn đọc được số liệu. Màu vẫn đúng nhóm hành động.
- **Icon + CHỮ chứ không icon-only** (khác cột hành động của màn danh sách): 2 hành động này khác
  hẳn nhau về hệ quả — kéo dài hạn vs trả hàng về tồn — đoán bằng icon là đoán sai.
- Nút giữ đúng màu ở cả 3 trạng thái hạn, **không bị màu chữ của ô đè** (ô tô xanh/vàng/đỏ theo hạn).
- Cả 2 là **ĐIỀU HƯỚNG**, chưa ghi gì → theo `button-convention` mục 6c **KHÔNG hỏi xác nhận**;
  popup xác nhận nằm ở nút Lưu / Gửi duyệt của chính màn lập phiếu.

⚠️ **Bẫy của việc nhét nút vào ô dữ liệu:** bản in / Excel lấy chữ từ chính ô HTML, nên ô hạn giữ
đổ ra thành `"03/08/2026 quá hạn 40 ngày Gia hạn Huỷ giữ"` — in chữ nút lên giấy là rác. Phải **gỡ
hẳn `.row-acts`** trước khi lấy text. Đo sau khi sửa: ô bản in = `"18/06/2026 quá hạn 86 ngày"`,
bản chi tiết vẫn đúng 15 cột.

#### 2 điểm lệch quy ước — user đã chốt 14/09/2026

| # | Quy ước | User chốt | Ghi chú |
|---|---|---|---|
| a | `button-convention`: dấu kiểu mới **"Hủy"** | **"Huỷ giữ"** | Giữ đúng chính tả user gõ; lệch với các nút "Hủy" khác trong hệ thống |
| b | CLAUDE.md: nút không dùng được thì **ẩn hẳn** | **Nút Gia hạn hiện ở MỌI dòng**, kể cả dòng Trong hạn | Xem cảnh báo ngay dưới |

#### ⚠️ RỦI RO ĐÃ NÊU VÀ USER VẪN CHỌN — phải xử lúc code BE

Màn lập phiếu gia hạn lấy nguồn dòng bằng `getDataToCreate($employee_id)`:
`prepick_details` của chính nhân viên đó, `qty > 0`, cùng công ty, **và
`expire_date <= hôm nay + configs.warning_day`** (local = 7 ngày).

⇒ Lô đang **Trong hạn KHÔNG hề xuất hiện** ở màn đó. Nút Gia hạn ở dòng Trong hạn là **nút chết**:
bấm sang màn kia sẽ không thấy dòng của mình.

**Bắt buộc khi triển khai — chọn 1 trong 2, không được để im lặng:**
1. Màn lập phiếu gia hạn nhận `prepick_detail_id` và khi dòng đó chưa tới ngưỡng cảnh báo thì **báo
   rõ lý do** ("Hàng này còn N ngày mới tới hạn, chưa lập được yêu cầu gia hạn"); **hoặc**
2. Hỏi khách để **nới điều kiện** `getDataToCreate()` cho phép gia hạn cả lô còn xa hạn — đây là đổi
   nghiệp vụ của màn khác nên phải được duyệt riêng.

#### ⚠️ Huỷ giữ trừ tồn theo FIFO, KHÔNG theo dòng được bấm

`PrepickCancel::updateWarehouse()` trừ tồn theo bộ 4 `(product_id, employee_id, customer_id,
company_id)` với `orderBy('expire_date', 'ASC')` — tức trừ từ lô **hạn sớm nhất** trở đi. Bấm "Huỷ
giữ" ở một dòng **không đảm bảo huỷ đúng dòng đó** nếu bộ 4 còn nhiều dòng khác hạn.

Thực tế nhẹ hơn vẻ ngoài: đo trên DB thật **2.300/2.355 nhóm (97,7%) chỉ còn đúng 1 dòng đang tồn**,
nên đa số trường hợp trùng khớp. Nhưng màn lập phiếu hủy vẫn phải cho **sửa số lượng + thấy rõ mình
đang hủy lô nào**, đừng hứa với user là "hủy đúng dòng vừa bấm".

### 49 · Rà toàn bộ nút theo `button-convention` (14/09/2026) — 5 lỗi đã sửa

Rà lại MỌI nút trong mockup, không chỉ 2 nút mới. 5 lỗi dưới đây đều ở các nút làm từ vòng trước,
không phải do quyết định nào của user:

| # | Nút | Sai gì | Đã sửa thành |
|---|---|---|---|
| 1 | "In báo cáo" (thanh tiêu đề) | Chữ này nằm thẳng trong cột **"KHÔNG dùng"** của bảng text chuẩn (hàng *In cả danh sách*) | **"In danh sách"** |
| 2 | "Xuất Excel danh sách" (popup) | 4 từ, vượt giới hạn **tối đa 3 từ** | **"Xuất Excel"** |
| 3 | Thứ tự footer popup | `Đóng · In · Xuất Excel` — mục 5 bắt **Thoát/Huỷ LUÔN CUỐI CÙNG**. Sai ở cả popup chi tiết lẫn popup chọn chế độ in | `In danh sách · Xuất Excel · Đóng` và `In · Hủy` |
| 4 | 4 nút Đóng / Huỷ | Thiếu icon — mục 1: *mọi button PHẢI có icon* | Thêm icon mũi tên trái (`fas fa-arrow-left` ở bản thật) |
| 5 | "Xuất Excel" trong popup tô **teal** | Nhóm Xuất file phải `secondary status="success"` (**xanh lá**). Nút Xuất Excel ở thanh tiêu đề đã xanh lá → 2 nút CÙNG làm một việc mà 2 màu, đọc thành 2 mức quan trọng khác nhau | `.modal-btn--excel` = `#16a34a` |

Kèm theo: **"Huỷ"** ở popup chọn chế độ in đổi thành **"Hủy"** (dấu kiểu mới). Chỉ nhãn **"Huỷ giữ"**
trong bảng là giữ nguyên chính tả user gõ — đó là điểm đã chốt riêng ở mục 48.

ℹ️ Nút "Xuất Excel" ở thanh tiêu đề dùng `rgba(34,133,90,.55)` còn trong popup dùng `#16a34a`: khác
sắc là **cố ý** — thanh tiêu đề nền navy nên nút phải bán trong suốt để hoà, popup nền trắng thì
dùng màu đặc. Cùng một họ xanh lá, đúng tinh thần "cả nhóm Xuất cùng màu".

ℹ️ Nút **In** trong popup chọn chế độ in để `primary` (teal) vì nó là **action chính của popup đó**
(mục 2 xếp In vào nhóm primary), còn nút **In danh sách** ở footer popup chi tiết để `secondary` —
ở đó nó chỉ là hành động bổ trợ.
