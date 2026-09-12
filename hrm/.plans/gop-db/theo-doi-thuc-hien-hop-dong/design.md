# Design — Mockup màn Theo dõi thực hiện hợp đồng

> Nhánh `gop_db` (đang đứng ở `permiss_manager`, checkout từ `gop_db`). Phụ trách: @namdangit.
> Nguồn yêu cầu: `THEO DÕI THỰC HIỆN HỢP ĐỒNG.docx` — họp 25/08/2026
> (Sếp Phong, a Nam, a Tú, c Ngô Hằng, c Thúy, c Lệ, c Huyền).

## Mục tiêu

Dựng **1 file mockup HTML tĩnh** cho màn **Chi tiết theo dõi thực hiện hợp đồng** — màn mới, độc lập
với màn chi tiết hợp đồng hiện có (`/assign/contracts/{id}`). Dùng làm bản duyệt UI trước khi code Vue thật.

## Phạm vi

- **Trong scope:** 1 màn, 6 tab, file `mockup.html` self-contained (không CDN, mở bằng browser là chạy).
- **Ngoài scope (làm sau):**
  - **Nhóm A** — bổ sung trường + luồng 7 trạng thái vào FORM hợp đồng hiện có
  - **Nhóm C** — 3 báo cáo (công nợ quá hạn · theo dõi đặt hàng theo HĐ có hiệu lực · theo dõi tiến độ giao hàng)
  - Màn **danh sách HĐ đang thực hiện** (user chốt: làm sau)
  - Không sửa code Vue thật, không API, không DB.

## Hiện trạng code (khảo sát 02/09/2026)

Module hợp đồng HRM **đã có một phần** — mockup phải bám vào, không vẽ lại từ đầu:

| Đã có | Nơi |
| --- | --- |
| 4 trạng thái: Đang tạo(3) · Chờ duyệt(2) · Có hiệu lực(6) · Đã thanh lý(10) | `pages/assign/contracts/index.vue:192` |
| `sign_date`, `effective_date`, `expiry_date`, `execution_deadline_days`, `execution_end_date` | `Modules/Assign/Entities/Contract/Contract.php` |
| 3 điều kiện hiệu lực `EFFECTIVE_COND_*` + 4 mốc `EXEC_BASE_*` | cùng file |
| Guard `getCanExportAttribute` (chặn xuất hàng khi chưa hiệu lực / chưa có thời hạn) | cùng file |
| `ContractPaymentTermsTable` (điều khoản thanh toán) | `components/ContractPaymentTermsTable.vue` |

**Tài liệu yêu cầu thêm** (chưa có): 3 trạng thái Không duyệt / Chờ KH ký / KH đã ký / Đóng · cảnh báo giao hàng ·
cảnh báo sắp hết hiệu lực · kế hoạch giao hàng · mẫu in duyệt pháp chế · tiến độ thanh toán gắn mốc nghiệm thu
kèm biên bản · toàn bộ màn theo dõi thực hiện · 3 báo cáo.

## Bố cục chung (chốt vòng 2 — 02/09/2026)

- **Sidebar mặc định thu gọn** thành rail icon 62px (mỗi mục có `title` tooltip); bấm burger trên topbar
  để mở về 236px. Thanh hành động dưới đáy bám theo (`left: 62px ↔ 236px`).
- **Bỏ thanh trạng thái (stepper 7 bước)** — màn này **chỉ áp dụng cho hợp đồng Có hiệu lực**,
  nên luồng duyệt không thuộc phạm vi màn. Trạng thái vẫn hiển thị bằng 1 chip cạnh mã HĐ.
- **Nhãn tab bỏ số thứ tự**, rút gọn nhưng giữ nguyên nghĩa:
  Thông tin chung · Hàng hoá ký · Cung ứng · Tài chính · Thiết kế & giám sát · Giao hàng & nghiệm thu · Bảo hành.
- **Khối tổng hợp mỗi tab dùng lại component của mockup Báo cáo CSKH tiềm năng**
  (`.plans/gop-db/ke-hoach-phat-trien-thi-truong/bao-cao-ket-qua-cham-soc-khach-hang-tiem-nang.html`):
  một card `.rsum` gọn có nút **Thu gọn / Mở rộng**, bên trong là các box `.rsum-blk`
  (viền mảnh + nền tint, nhãn UPPERCASE, số tổng lớn bên phải, các ô con nền trắng/tint theo good–warn–bad)
  và hàng `.rsum-kpi` `border-left` màu, số lớn kèm đơn vị mờ, **track 5px** và dòng công thức.
  Thay hoàn toàn `.kpis/.kpi` và `.stats/.st` của vòng 1.

## Tab Thông tin chung (chốt vòng 3 — 02/09/2026)

- **Bỏ toàn bộ khối summary tài chính** (Giá trị & thu tiền, Chi phí & hiệu quả). Tiền bạc chỉ theo dõi ở
  tab **Tài chính** — tab này giữ đúng vai trò *hồ sơ + tiến độ*. Khối tổng hợp đổi tên thành
  **Tiến độ thực hiện**, chỉ còn 3 KPI: tiến độ tổng thể · mã hàng đủ phương án cung ứng · thời gian còn lại.
- **Nguyên tắc gỡ trùng lặp áp dụng mềm** (chốt vòng 5): các trường **định danh** vẫn phải nằm trong nhóm của nó,
  kể cả khi thanh tiêu đề đã hiển thị — *Số hợp đồng* đứng đầu nhóm *Thông tin hợp đồng*;
  *Mã khách hàng · Tên khách hàng · Mã số thuế* đứng đầu nhóm *Thông tin khách hàng*.
  Chỉ gỡ những lặp lại **không mang thêm thông tin** (chip *còn 45 ngày*, dòng phụ đặt cọc, note điều hướng sang tab khác).
- **Gỡ trùng lặp trong tab** — những gì thanh tiêu đề (sticky, dùng chung 7 tab) đã hiển thị thì không lặp lại
  bên trong: bỏ ô *Số hợp đồng*, *Khách hàng*, *Trạng thái* khỏi lưới thông tin; bỏ chip *còn 45 ngày* ở ô
  *Ngày hết hiệu lực*; bỏ dòng phụ *Đặt cọc lần 1 nhận ngày…* (đã có ở *Điều kiện hiệu lực*).
  Timeline bỏ các chip cảnh báo và các dòng *mở khoá thanh toán đợt N* — cảnh báo thuộc về khối callout,
  thanh toán thuộc về tab Tài chính. Ô MST / người liên hệ đổi nhãn thành *Mã số thuế KH* / *Người liên hệ KH*
  để không cần lặp lại tên khách hàng.
- Card đổi tên **Thông tin chung**, chia **4 nhóm chủ đề**, mỗi nhóm một dải tiêu đề `.sub-t` + lưới `.info` riêng
  (riêng nhóm *File đính kèm* là bảng). Card timeline đổi tên **Tiến độ thực hiện theo các mốc thời gian**:

  | Nhóm | Số ô | Nội dung |
  | --- | --- | --- |
  | Thông tin hợp đồng | 10 | **Số hợp đồng** · Trạng thái · Mã báo giá · Loại hợp đồng · Loại tiền tệ · NV kinh doanh · Phòng thực hiện · Người phụ trách HĐ · Bảo lãnh thực hiện · Thời gian bảo hành *(ô cuối tràn hết hàng)* |
  | Thông tin khách hàng | 9 | **Mã khách hàng · Tên khách hàng · Mã số thuế** · Người đại diện · Chức vụ đại diện · Người liên hệ · SĐT liên hệ · Email liên hệ · Địa chỉ |
  | Hiệu lực & thời hạn | 6 | Ngày ký · Điều kiện hiệu lực · Ngày có hiệu lực · Mốc tính thời hạn *(kèm ngày bàn giao mặt bằng)* · Thời hạn thực hiện · Ngày hết hiệu lực |
  | File đính kèm | 4 file | Bảng file: tên · loại tài liệu · ngày tải · người tải · dung lượng · nút tải về (HĐ bản ký · mẫu in duyệt pháp chế · bảo lãnh · biên bản bàn giao mặt bằng) |

  Số ô mỗi nhóm là **bội số của 3** (lưới 3 cột) nên không nhóm nào có ô nằm lẻ một dòng.
  File bản ký tách khỏi ô *Ngày ký* để dồn về nhóm *File đính kèm* — không còn file nằm rải rác trong lưới.
- **Bỏ các note điều hướng sang tab khác** (kiểu *“số liệu tài chính theo dõi ở tab Tài chính”*):
  gỡ `.rsum-sub` ở tab 1, cắt vế trỏ tab ở hint tab *Hàng hoá ký* và tab *Thiết kế & giám sát*.
  Đo trên toàn trang: chuỗi *“ở tab”* và *“tab Tài chính”* còn **0 lần**.

## Tab Giao hàng & nghiệm thu (chốt vòng 15 — 03/09/2026)

- **Chuyển lên vị trí thứ 3**, ngay sau *Cung ứng & dịch vụ* — luồng đọc thành
  hồ sơ → cung ứng → giao hàng → tiền → thiết kế → bảo hành.
- Cột **Nội dung giao** rút gọn thành `N mã · M đơn vị`, **bấm ra popup** liệt kê từng mã trong đợt
  kèm SL giao, phiếu xuất kho, biên bản, tình trạng. Tổng 5 đợt = **9 mã · 1.767 đơn vị** = đúng tổng SL ký.
- **Một đợt giao có thể có nhiều phiếu xuất kho**: đợt 2 giao làm 2 chuyến —
  `PXK-2026-1326` (cầu trục + ống thép) và `PXK-2026-1331` (6 van). Cột PXK hiện cả 2 mã,
  popup chi tiết chỉ rõ mã hàng nào đi theo phiếu nào.
- Bảng khối lượng theo từng mã: **bấm số ở cột *Đã giao* mở popup serial** —
  serial · ngày giao · phiếu xuất kho · biên bản · vị trí lắp đặt · trạng thái.
  Mặt hàng vật tư (ống thép, cáp điện) không quản lý serial thì popup nói rõ điều đó thay vì để trống.

## Tab Tài chính chia 4 tab con (chốt vòng 14 — 03/09/2026)

Tab Tài chính vốn dồn 4 nghiệp vụ khác nhau vào 1 trang dài; nay tách thành **4 tab con** dạng pill,
**mỗi tab con có khối thống kê + cảnh báo riêng** (không còn khối tổng hợp dùng chung ở trên):

| Tab con | Thống kê | Cảnh báo | Bảng |
| --- | --- | --- | --- |
| **Giá trị & thanh toán** | Giá trị HĐ 5.038.000.000 (trước VAT · VAT · gốc · PL) · cơ cấu hàng hoá/dịch vụ · 5 đợt | — | Giá trị HĐ & thuế (gốc / PL01 / tổng) · Điều khoản thanh toán 2 bên · Điều khoản khác |
| **Công nợ NCC** | Phải trả 3.008.000.000 (đã trả · còn lại · quá hạn) · tỷ lệ đã trả 70,2% · 1 NCC quá hạn | Việt Tiến quá hạn 5 ngày | Công nợ theo NCC · **Phiếu chi cho NCC** (7 dòng) |
| **Công nợ KH** | Phải thu 5.038.000.000 (đã thu · còn lại · quá hạn) · tỷ lệ đã thu 75,0% · quá hạn 12 ngày | Đợt 3 quá hạn 12 ngày | Công nợ theo đợt · **Phiếu thu từ KH** (6 dòng) · Hoá đơn–nghiệm thu–quyết toán |
| **Dự toán** | Chi phí 3.606.000.000 (dự toán · thực tế · vượt) · chênh lệch +2,44% · lãi gộp 21,3% | 1 khoản vượt chưa có lý do | Dự toán vs Thực tế (7 khoản mục) |

Bảng *Công nợ phải thu* cũ vốn trộn **điều khoản** với **tình hình thu**; nay tách đôi:
điều khoản (tỷ lệ · thời hạn · chứng từ bắt buộc) về tab *Giá trị & thanh toán*,
tình hình thu (đã thu · còn lại · quá hạn) về tab *Công nợ KH*.

## Trường nhập tay vs trường tự tính (chốt vòng 7)

Bám đúng cột *Diễn giải* của tài liệu: chỗ nào ghi **“bắt buộc nhập / chọn ngày / nhập số ngày /
phải nhập ngày và có biên bản đính kèm / bắt buộc lý do”** thì mockup dựng **ô nhập thật**;
chỗ nào ghi **“tự tính”** thì khoá lại.

| Tab | Ô nhập tay | Căn cứ trong tài liệu |
| --- | --- | --- |
| Thông tin chung | Ngày ký * · Điều kiện hiệu lực * (select 3 lựa chọn) · Ngày có hiệu lực * · Mốc tính thời hạn * (select 4 lựa chọn) · Ngày đạt mốc * · Thời hạn thực hiện * (số ngày) | mục 1, 2, 3 |
| Thông tin chung | **Ngày hết hiệu lực — khoá, `TỰ TÍNH`** kèm công thức `Ngày đạt mốc + số ngày` | mục 4 “Tự tính” |
| Tài chính | Lý do vượt dự toán (3 dòng vượt; dòng chưa nhập để **viền đỏ + placeholder bắt buộc**) | “Khi duyệt giá nếu có chênh lệch vượt dự toán thì bắt buộc lý do” |
| Tài chính | Ngày đạt mốc của đợt thanh toán chưa tới + nút **Đính kèm biên bản** | mục 9 “Phải nhập ngày và có biên bản đính kèm” |
| Thiết kế & giám sát | Ngày duyệt + nút **Tải hồ sơ** cho 2 hạng mục chưa duyệt | theo dõi tiến độ thiết kế |
| Giao hàng & nghiệm thu | Ngày dự kiến + ngày thực tế + nút **Đính kèm** cho 3 đợt chưa giao | mục 10 “Từng lần giao hàng gì, dự kiến giao khi nào” |

Quy ước hiển thị: ô nhập nền trắng viền mảnh (focus viền teal), nhãn có dấu `*` đỏ khi bắt buộc,
ô thiếu dữ liệu bắt buộc để `.inp.err` (viền đỏ + nền hồng nhạt), ô hệ thống tự tính dùng `.ro`
(nền xám, **viền đứt**, nhãn `TỰ TÍNH`) để phân biệt rõ với ô nhập được.

**Không** cho nhập tay ở tab *Cung ứng*: theo tài liệu, số lượng Giữ hàng / Đang đi mua sinh ra từ
phiếu giữ và đơn đặt hàng (nút *Giữ hàng* / *Đặt hàng* mở form), không phải gõ tay.

## Thanh tiêu đề màn (chốt vòng 6)

`Mã HĐ · chip trạng thái · Khách hàng · **KD phụ trách** | chip Giá trị · chip Số ngày còn lại · chip Cảnh báo`.
Hai đoạn *Khách hàng* / *KD phụ trách* dùng chung class `.cust` (ngăn nhau bằng vạch dọc mảnh).
Card *Thông tin chung* **bỏ dòng meta Người lập / Tạo lúc**.

## Màu nhận diện tab (chốt vòng 5)

Mỗi tab một màu riêng, đặt bằng 2 biến inline `--tc` (màu chính) và `--tcl` (nền tint):
icon luôn tô màu tab (mờ 68% khi không chọn), hover đổi nền sang tint,
tab đang chọn = nền tint + chữ màu tab + viền trên 2px màu tab.

| Tab | `--tc` | `--tcl` |
| --- | --- | --- |
| Thông tin chung | `#2E71C3` xanh dương | `#eaf2fb` |
| Hàng hoá ký | `#0a99a7` teal | `#e4f6f8` |
| Cung ứng | `#e07b2f` cam | `#fdf0e5` |
| Tài chính | `#0f9d63` xanh lá | `#e6f7ef` |
| Thiết kế & giám sát | `#7a5bd6` tím | `#f1ecfd` |
| Giao hàng & nghiệm thu | `#c9518c` hồng | `#fceef5` |
| Bảo hành | `#b5820e` hổ phách | `#fdf5e2` |

Tab đang chọn có `border-top: 2px` nên `padding-top` giảm 1px để **chiều cao 7 tab luôn bằng nhau (35px)**.

## Cấu trúc màn — 6 tab

| # | Tab | Nội dung chính |
| --- | --- | --- |
| 1 | Thông tin chung | Khối *Tiến độ thực hiện* (3 KPI, **không có số liệu tài chính**) · 5 cảnh báo đang mở · thông tin HĐ **chia 4 nhóm chủ đề** · bảng phụ lục · timeline 8 mốc thực hiện |
| 2 | Cung ứng | **2 bảng**: (a) *Phương án cung ứng theo từng mã hàng* — 9 mã, **Giữ hàng / Đang đi mua**, cột *Đã phân bổ* & *Còn thiếu*, dòng thiếu tô đỏ, mở rộng xem nguồn (phiếu giữ / PO + tình trạng sản xuất–đi đường–về kho); (b) *Dịch vụ đã ký* — 4 gói: đơn vị thực hiện · hạn hoàn thành · **% tiến độ** · trạng thái đã/chưa hạch toán |
| 3 | Giao hàng & nghiệm thu | 5 đợt giao dự kiến vs thực tế (PXK, BBGN) · khối lượng giao–lắp–nghiệm thu theo từng mã |
| 4 | Tài chính | **4 tab con**: *Giá trị & thanh toán* (giá trị + thuế + điều khoản thanh toán 2 bên) · *Công nợ NCC* (thống kê, cảnh báo, công nợ theo NCC, **phiếu chi**) · *Công nợ KH* (thống kê, cảnh báo, công nợ theo đợt, **phiếu thu**, hoá đơn–nghiệm thu–quyết toán) · *Dự toán* (dự toán vs thực tế, chênh lệch, cảnh báo) |
| 4 | Thiết kế & giám sát | 6 hạng mục thiết kế (người phụ trách, hạn, ngày duyệt, file) · nhật ký giám sát công trường |
| 6 | Bảo hành | Thời gian BH · quỹ trích dự phòng · chi phí đã dùng · quỹ còn lại · bảo hành theo thiết bị ↔ bảo hành từ NCC |

## Logic Hiệu lực & thời hạn (chốt vòng 10 — 03/09/2026)

Mockup chạy logic thật, không còn là ô tĩnh:

| Điều kiện hiệu lực | Trường hiện thêm | Ngày có hiệu lực lấy từ |
| --- | --- | --- |
| Kể từ ngày ký | — | **= Ngày ký** (đổi ngày ký thì chạy theo ngay) |
| Theo ngày đặt cọc lần đầu *(mặc định)* | — | **Ngày phiếu thu đặt cọc đầu tiên** — nguồn ở tab Tài chính, sẽ nối sau |
| Theo ngày bảo lãnh được duyệt | **Số bảo lãnh** * + **Ngày bảo lãnh duyệt** * | **= Ngày bảo lãnh duyệt**, dòng nguồn ghi kèm số bảo lãnh |

- **Ngày có hiệu lực chuyển thành ô `TỰ TÍNH`** (không nhập tay nữa) — vì cả 3 nhánh đều suy ra từ dữ liệu khác.
  Dưới ô luôn có dòng nhỏ ghi rõ **đang lấy theo nguồn nào**.
- 2 trường bảo lãnh **chỉ hiện khi chọn nhánh bảo lãnh**, ẩn ở 2 nhánh còn lại
  (`.irow[hidden]{display:none}` — cần khai riêng vì `.irow` là `display:flex`, thuộc tính `hidden` mặc định không thắng được).
- **Ngày hết hiệu lực cũng tính lại trực tiếp** = `Ngày đạt mốc + Thời hạn thực hiện`; thiếu dữ liệu thì hiện `—`
  kèm câu nhắc. Công thức dưới ô cập nhật theo số thực nhập.
- Lưới vẫn kín: ô *Ngày có hiệu lực* bỏ `full` để hàng lấp đủ 3 cột — mặc định `3 + 3`,
  nhánh bảo lãnh `3 + 3 + 2`, riêng *Ngày hết hiệu lực* cố ý trải hết hàng.

## Bảng cung ứng — mô hình tính lại theo SL còn lại (chốt vòng 11 — 03/09/2026)

Thêm 2 cột **SL đã xuất** và **SL còn lại** ngay sau *SL ký*; **mọi cột sau đều tính theo SL còn lại**:

```
SL còn lại = SL ký − SL đã xuất
Đã phân bổ = Giữ hàng + Đang đi mua        (chỉ tính nguồn CHƯA xuất giao)
Còn thiếu  = SL còn lại − Đã phân bổ
```

Hệ quả: mã đã giao đủ (máy tiện · cầu trục · cáp điện) về `còn lại = 0`, không còn chiếm chỗ trong
phần cần cung ứng và mang trạng thái mới **Đã xuất đủ**. Ba con số *Còn thiếu* (80 · 6 · 6) giữ nguyên.

Dòng tổng: ký **1.767** · đã xuất **1.458** · còn lại **309** · giữ **1** · đang mua **216** ·
đã phân bổ **217** · còn thiếu **92** — cân đúng `217 + 92 = 309`.

### Chốt thêm vòng 13

- **Nút *Giữ hàng* chỉ hiện khi `Tồn kho khả dụng > 0`.** Hết tồn thì chỉ còn *Đặt hàng* —
  bấm *Giữ hàng* khi không còn tồn là thao tác chết. VT-VALVE-D100 (tồn 0) nay chỉ còn 1 nút.

### Chốt thêm vòng 12

- **Dòng *Giữ hàng* chỉ còn 2 tình trạng: `Còn hạn` / `Quá hạn`** — suy trực tiếp từ *Hạn giữ* so với hôm nay
  (03/09/2026): 0331 hết 28/07 và 0330 hết 26/08 → *Quá hạn*; 0333 · 0352 · 0348 còn hạn.
  Dòng *Đang đi mua* vẫn giữ tình trạng vận hành riêng (Đang sản xuất / Đi đường / Đã về kho).
- **Bỏ toàn bộ dòng ghi chú quy tắc** — 7 dòng `.hint` ở các tab + dòng *Quy tắc* trong khối tổng hợp
  tab Cung ứng. Toàn trang không còn chữ “Quy tắc”.
- Khối *Hàng hoá cần cung ứng*: ô **Đã phân bổ → Số lượng đã giao** = `1.458` (82,5% của 1.767 đã ký).
  Sửa luôn số liệu cũ đã lỗi thời (1.675) sau khi bảng đổi sang mô hình tính theo SL còn lại.

### Khối tổng hợp: “Tình hình cung ứng” → **“Tình hình đặt mua”**

Hai block *Hàng hoá cần cung ứng* / *Dịch vụ đã ký* giữ nguyên. Hàng KPI thay hoàn toàn:

| KPI | Giá trị | Bấm vào |
| --- | --- | --- |
| Tổng đặt mua | **4 đơn mua** (6 YCĐH · 4 NCC · 217 đơn vị) | — |
| Số lượng đã về kho | **121 đơn vị** | mở popup 2 mã: YCĐH · đơn mua · NCC · SL đặt · đã về · ngày về |
| Số lượng đang mua | **96 đơn vị** | mở popup 5 mã: thêm dự kiến về · tình trạng (đang sản xuất / đi đường) |

`121 + 96 = 217` = tổng lượng đã đặt mua. Lưu ý **217 (theo đơn mua) ≠ 216 (cột *Đang đi mua* trong bảng)**:
chênh 1 là cầu trục — đã đặt mua, đã về kho và **đã xuất giao KH** nên không còn nằm trong phần cần cung ứng.
Dòng công thức của KPI ghi rõ cách cộng để không hiểu nhầm.

Popup dựng theo **khung `.minutes-modal` của mockup Báo cáo CSKH tiềm năng** (chốt vòng 13):
**popup căn giữa màn hình**, rộng 1.240px / max 94vw, cao tối đa 86vh, mở bằng
`translate(-50%,-50%) scale(.96) → scale(1)` kèm fade; backdrop `rgba(0,0,0,.4)` có transition.
Header **dùng chung một gradient xanh** `linear-gradient(135deg, #0a1c3d, #0e7490)` (navy → teal đậm) —
lấy đúng `.minutes-modal__header` của mockup mẫu, **không đổi màu theo ngữ cảnh** (chốt vòng 16).
Icon tròn + tiêu đề 15px kèm dòng phụ mờ vẫn thay đổi theo nội dung.
Bảng trong popup dùng `.mm-wrap` — **`max-height:56vh`, tự cuộn, tiêu đề cột dính** (như `.drill-wrap` của mẫu).
Đóng bằng nút ×, bấm nền hoặc phím **Esc**.

> Vòng 12 từng dựng theo `.ticket-drawer` (panel trượt từ phải) — user phản hồi trông như popover lệch
> bên phải, nên vòng 13 đổi sang `.minutes-modal` căn giữa cho đúng chuẩn popup của mockup mẫu.
Dòng tổng của drawer **chỉ cộng cột có nghĩa** (đã về / chưa về) — cột *SL đặt* để trống vì mã ống thép
xuất hiện ở cả hai drawer (200 đặt = 120 về + 80 chưa về), cộng lại sẽ trùng.

## Bảng cung ứng — chi tiết chốt vòng 9 (03/09/2026)

- **Header bảng có viền đầy đủ** như thân bảng: `thead th` thêm `border:1px solid #bfe3e8`
  (viền `#edf0f4` của thân bảng chìm hẳn trên nền teal của header nên phải dùng tông teal đậm hơn),
  giữ `border-bottom:2px solid #0a99a7`.
- **Cột *Đã về kho* → *Tồn kho khả dụng***: đổi luôn nội dung cho khớp nghĩa — bỏ thanh tiến độ
  `đã về / SL ký`, thay bằng **số tồn còn dùng được** của mã đó. Cột này đứng cạnh *Còn thiếu* để
  người phụ trách quyết được ngay: còn tồn thì **Giữ hàng**, hết tồn thì bắt buộc **Đặt hàng**.
- **Dòng đã phân bổ đủ thì ô *Hành động* để trống** — bỏ nút *Sửa phương án* (6 dòng).
  Chỉ 3 dòng còn thiếu mới có nút *Giữ hàng* / *Đặt hàng*.
- **Bảng chi tiết nguồn cung ứng** (dòng mở rộng) nâng lên **8 cột có tiêu đề**:
  Phương án · Chứng từ · Kho / Nhà cung cấp · Số lượng · Mốc thời gian · **Hạn giữ** · Tình trạng · Ghi chú.
  - Dòng *Đang đi mua* hiện **số Yêu cầu đặt hàng (YCĐH)** làm chứng từ chính, số **Đơn mua (PO)** ở dòng phụ.
  - Dòng *Giữ hàng* bổ sung **Hạn giữ**; hàng còn trong kho mà sắp hết hạn giữ được gắn chip cảnh báo
    (PGH-2026-0333 hạn 10/09/2026 — *còn 7 ngày*, đang chờ xuất giao đợt 3 ngày 08/09).

### ⚠️ Bất nhất dữ liệu tự phát hiện & sửa (vòng 9)

Cùng một số PO nhưng hai tab ghi hai nhà cung cấp khác nhau:
`PO-2026-0438` (tab Cung ứng ghi *Đại Nam*, tab Tài chính ghi *Hoà Phát Nam*) và
`PO-2026-0470` (tab Cung ứng dùng cho cả *Hoà Phát Nam* lẫn *Thang máy Sài Gòn*).
Lấy **tab Tài chính làm chuẩn** (bảng công nợ NCC) rồi gán lại:

| Đơn mua | Nhà cung cấp | Đầu mục |
| --- | --- | --- |
| PO-2026-0412 | Cty TNHH Thiết bị Đại Nam | Máy phay VF-3 ×2 · Máy nén 75kW ×1 |
| PO-2026-0438 | Cty CP Vật tư Hoà Phát Nam | Ống thép D219 200m · Van D100 ×12 |
| PO-2026-0455 | Cty TNHH Cơ điện Việt Tiến | Cầu trục 5T ×1 |
| PO-2026-0470 | Cty TNHH Thang máy Sài Gòn | Tủ điện MCC ×1 |

Sửa kèm câu nhắc ở tab *Giao hàng & nghiệm thu* (đợt 3 nhắc `PO-2026-0438` → `PO-2026-0412`).

## Quyết định phạm vi: bỏ hẳn giá trị từng đầu mục (chốt 03/09/2026)

Khi bỏ tab *Hàng hoá ký*, các cột **Đơn giá · Thành tiền · VAT · Sau VAT của từng đầu mục** cũng bỏ hẳn
theo quyết định của user — **không** đưa lại vào tab Cung ứng hay Tài chính.

Hệ quả: màn theo dõi thực hiện chỉ còn **số lượng** ở cấp đầu mục, còn **tiền chỉ ở cấp tổng**
(giá trị HĐ sau VAT ở thanh tiêu đề + tab Tài chính; doanh thu trước VAT ở bảng dự toán vs thực tế).
Muốn xem giá từng dòng thì mở màn hợp đồng / báo giá gốc.

Đã kiểm bằng grep trên file mockup: 0 cột *Đơn giá / Thành tiền / VAT / Sau VAT*,
8/8 đơn giá của 9 mã hàng đều **0 lần**; các số tổng 5.038.000.000 và 4.580.000.000 vẫn còn đúng chỗ.

## Quy tắc nghiệp vụ mockup thể hiện rõ

- **Cung ứng (tab 3):** `Giữ hàng + Đang đi mua ≥ SL ký` cho **từng mã**. Chưa đủ → tô đỏ, ghi *Còn thiếu*,
  và hệ thống **chặn tạo yêu cầu xuất hàng** cho mã đó. Nút *Giữ hàng* mở form YC xuất giữ, nút *Đặt hàng*
  mở form YC đặt hàng — đều lấy sẵn phần còn thiếu.
- **Tài chính (tab 4):** khoản mục vượt dự toán **bắt buộc nhập lý do** mới cho duyệt giá/duyệt chi.
- **Thanh toán:** đợt trung gian chỉ mở khoá khi có **ngày đạt mốc + biên bản có chữ ký KH**.
- **Phụ lục:** PL gia hạn chưa duyệt thì **chưa đẩy ngày hết hiệu lực**; duyệt xong mới tính lại toàn bộ mốc cảnh báo.
- **Bảo hành:** đối chiếu BH cam kết với KH ↔ BH nhận từ NCC; NCC ngắn hơn → phần chênh công ty tự chịu (tô đỏ).

## Dữ liệu mẫu

Một hợp đồng xuyên suốt cả 7 tab — **HD-2026-00147**, KH *Công ty CP Cơ khí Thăng Long*,
trước VAT 4.580.000.000 ₫ (gốc 4.400.000.000 + PL01 180.000.000), sau VAT **5.038.000.000 ₫**.
Ký 05/05/2026 · hiệu lực 12/05/2026 (đặt cọc lần đầu) · 150 ngày kể từ ngày bàn giao mặt bằng 20/05/2026
→ hết hiệu lực 17/10/2026. Mốc "hôm nay" của mockup: **02/09/2026**.

Số liệu cài sẵn **5 cảnh báo** để thấy rõ cách hiển thị trạng thái xấu:
công nợ đợt 3 quá hạn 12 ngày · 3 mã thiếu phương án cung ứng · phải trả NCC quá hạn 5 ngày ·
đợt giao số 3 còn 6 ngày (ngưỡng 7) · 1 khoản vượt dự toán chưa nhập lý do.

## Quyết định thiết kế

- **Self-contained**, không CDN — kế thừa shell (topbar + sidebar navy, SVG ribbon) và palette từ
  `.plans/gop-db/mockup-chi-tiet-bao-gia/chi-tiet-bao-gia-mockup.html` để đồng bộ bộ mockup Bán hàng:
  navy `#2E71C3`, accent teal `#0a99a7`, header bảng teal nhạt.
- **Header màn sticky** (mã HĐ + stepper 7 trạng thái + tab bar) — luôn thấy khi cuộn nội dung.
- **Bảng cuộn trong khung riêng** (`.tblwrap{overflow:auto;max-height:calc(100vh - 250px)}`) thay vì để
  trang cuộn ngang — nhờ đó `thead` sticky mới có scroll-container để bám.
- **Cột Hành động ghim mép phải** (`.stick-r`) ở tab 3: nút *Giữ hàng / Đặt hàng* là thao tác chính của
  màn, không được rơi ra ngoài vùng cuộn ngang.

## Kiểm chứng (Playwright, viewport 1440×900)

Đo bằng số từ DOM, không chỉ nhìn ảnh:

- 7 tab / 7 pane — luôn đúng **1 pane** hiển thị.
- **0 phần tử bị thanh hành động đè lên** ở cả 7 tab khi cuộn hết xuống (khoảng hở 42–43px).
- `thead` **dính đúng mép trên** khung bảng ở mọi bảng có cuộn dọc.
- **Trang không cuộn ngang** (`documentElement.scrollWidth == clientWidth == 1440`); bảng rộng tự cuộn
  trong khung riêng.
- Cột ghim phải nằm trong vùng nhìn thấy ở **cả `scrollLeft = 0` và `scrollLeft = max`**;
  `elementFromPoint` tại tâm nút *Giữ hàng* trả về đúng nút đó → không bị lớp nào che.
- Mở rộng dòng cung ứng: 9/9 nút hoạt động, hiện đúng 9 dòng chi tiết.
- Console: 0 lỗi (ngoài 404 `favicon.ico`).

### Vòng 17 — đổi nhãn tab (03/09/2026)

Tab **“Cung ứng & dịch vụ” → “Cung ứng”**. Nhãn 6 tab đo được:
*Thông tin chung · Cung ứng · Giao hàng & nghiệm thu · Tài chính · Thiết kế & giám sát · Bảo hành*.
Tab bar dư **452px**, chiều cao 6 tab vẫn đồng đều 35px, bấm vào vẫn mở đúng pane
(2 card *Phương án cung ứng theo từng mã hàng* + *Dịch vụ đã ký* giữ nguyên).

### Vòng 16 — đồng nhất màu header popup (03/09/2026)

Bấm thử **cả 12 popup** và đọc `getComputedStyle` của header:
**chỉ còn 1 gradient duy nhất** `linear-gradient(135deg, rgb(10,28,61), rgb(14,116,144))`
= `#0a1c3d → #0e7490`, khớp chính xác `.minutes-modal__header` của mockup Báo cáo CSKH.
Không còn biến inline `--mm-a/--mm-b` trên phần tử nào (0/12).
Quét bất biến 9 khung nhìn: **0 lỗi** · trang không cuộn ngang · console sạch.

### Vòng 15 — đo lại tab Giao hàng & popup mới (03/09/2026)

- Thứ tự tab đo được: *Thông tin chung · Cung ứng · **Giao hàng & nghiệm thu** · Tài chính ·
  Thiết kế & giám sát · Bảo hành* — đúng yêu cầu.
- **12 popup** (2 đặt mua + 5 đợt giao + 5 serial) — bấm thử **toàn bộ**: mở đúng, có nội dung, đóng được; **0 lỗi**.
- Popup đợt 2 hiện đúng **2 phiếu xuất kho khác nhau** trên 3 dòng hàng.
- ⚠️ **Lỗi tự bắt được**: link serial ban đầu gắn nhầm vào cột *SL ký* ở 3 dòng
  (TB-LATHE-ST20, TB-CRANE-5T, VT-CABLE-4x35) vì `replace` bắt trúng ô đầu tiên có cùng con số.
  Sửa bằng cách đếm chỉ số ô (`<td>` thứ 6) thay vì so khớp chuỗi. Đo lại: 5/5 mã có link ở đúng cột
  *Đã giao*, **0 ô *SL ký* còn link**.
- ⚠️ **Lỗi số liệu tự bắt được**: đợt 3 giao 08/09 so với hôm nay 03/09 là **5 ngày**, nhưng 4 chỗ
  (khối tổng hợp, callout, chip trạng thái, danh sách cảnh báo tab 1) vẫn ghi 6 ngày — đã đồng bộ về 5.
- Quét bất biến trên **9 khung nhìn**: **0 lỗi** · trang không cuộn ngang · console 0 lỗi 0 cảnh báo.

### Vòng 14 — đo lại tab con Tài chính (03/09/2026)

- 4 tab con / 4 pane con; bấm lần lượt đều mở **đúng pane tương ứng**, luôn chỉ 1 pane con hiển thị.
  Mỗi tab con có **1 khối `.rsum`**; 3/4 tab có callout cảnh báo riêng (tab *Giá trị & thanh toán* không cần).
- Kiểm cân bằng số học các bảng mới:
  - **NCC**: `đã trả + còn lại = giá trị` (2.112.000.000 + 896.000.000 = 3.008.000.000) ✓;
    tổng **phiếu chi đã chi = 2.112.000.000** khớp đúng cột *Đã trả* ✓
  - **KH**: `đã thu + còn lại = số tiền` (3.778.800.000 + 1.259.200.000 = 5.038.000.000) ✓;
    tổng **phiếu thu đã thu = 3.778.800.000** khớp đúng cột *Đã thu* ✓
  - **Giá trị**: `gốc 4.840.000.000 + PL01 198.000.000 = 5.038.000.000` ✓;
    **tổng 5 đợt điều khoản thanh toán = đúng giá trị hợp đồng** ✓
- Quét bất biến trên **9 khung nhìn** (6 tab, riêng Tài chính tách 4 tab con): **0 lỗi** —
  0 phần tử bị thanh hành động đè · `thead` dính · cột ghim phải luôn thấy · không bảng nào cuộn ngang ·
  trang không cuộn ngang · console sạch.

### Vòng 13 — đo lại popup căn giữa & sticky header (03/09/2026)

- Popup **căn giữa cả 2 chiều** (lệch tâm ≤ 2px so với tâm màn), rộng 1.240px, nằm trọn trong màn,
  đóng được bằng ×, nền và Esc. Không còn phần tử `#dw` (drawer cũ) trong DOM.
- **Sticky header chứng minh bằng cách ép khung xuống 120px cho bảng buộc phải cuộn**: cuộn hết xuống,
  tiêu đề cột vẫn nằm cách mép trên khung **1px**, và `elementFromPoint` ngay tại tiêu đề trả về
  chính `TH` (không bị dòng dữ liệu đè lên).
- Nút hành động theo tồn kho: *VT-PIPE-D219* (tồn 120) → **Giữ hàng + Đặt hàng** ·
  *VT-VALVE-D100* (tồn 0) → **chỉ Đặt hàng** · *VT-FILTER-A* (tồn 2) → **Giữ hàng + Đặt hàng**.
- 0 ô bị cắt trong popup ở cả 2 nội dung.
- Bất biến ở cả 6 tab: 0 phần tử bị thanh hành động đè · `thead` dính · cột ghim phải luôn thấy ·
  không bảng nào cuộn ngang · console sạch.

### Vòng 12 — đo lại sau khi đổi drawer & dọn ghi chú (03/09/2026)

- Dòng *Giữ hàng*: tập tình trạng đo được đúng **{Còn hạn, Quá hạn}** — không còn giá trị nào khác.
- `.hint` còn **0** phần tử; chuỗi “Quy tắc” trong toàn trang: **0 lần**.
- Khối *Hàng hoá cần cung ứng* đọc ra: *Đã đủ phương án 6 · Thiếu phương án 3 · **Số lượng đã giao 1.458** (82,5% của 1.767 đã ký)*.
- Drawer: mở/đóng bằng **nút ×, bấm nền, phím Esc** — cả 3 đều chạy; header đúng gradient theo màu nhấn
  (`#0f9d63→#0b7d4e` và `#e0921c→#b8760f`), chữ trắng, 3 chip meta; drawer luôn nằm trọn trong màn.
- ⚠️ Sửa 2 lần mới hết cắt cột: drawer 940 → 1.080px vẫn cắt 7 ô ở bảng *đang mua* (nhiều cột hơn) →
  cho cột *Nhà cung cấp* xuống dòng (`td.wrap`) và hạ `min-width` bảng. Kết quả cuối: **0 ô bị cắt** ở cả 2 drawer.
- Bất biến ở cả 6 tab: 0 phần tử bị thanh hành động đè · `thead` dính · cột ghim phải luôn thấy ·
  không bảng nào cuộn ngang · **console 0 lỗi 0 cảnh báo**.

### Vòng 11 — đo lại bảng cung ứng & popup đặt mua (03/09/2026)

- Kiểm **cân bằng số học từng dòng** (9/9 mã) — **0 lỗi**:
  `ký − xuất = còn lại` · `giữ + mua = đã phân bổ` · `phân bổ + thiếu = còn lại`.
- Dòng tổng khớp 100% với tổng cộng từ DOM: `1.767 · 1.458 · 309 · 1 · 216 · 217 · 92`.
- Popup *đã về kho*: 2 dòng, tổng **121**. Popup *đang mua*: 5 dòng, tổng **96**,
  cộng lại từ từng dòng cũng ra **96**. Đóng được bằng cả nút × lẫn phím Esc.
- Popup nới lên 1.200px: **0 ô bị cắt**, bảng trong popup không phải cuộn ngang, popup nằm trọn trong màn.
- Mở rộng dòng chi tiết vẫn chạy **9/9** sau khi dựng lại bảng.
- Bất biến ở cả 6 tab: 0 phần tử bị thanh hành động đè · `thead` dính · cột ghim phải luôn thấy ·
  không bảng nào cuộn ngang · **console 0 lỗi 0 cảnh báo**.

### Vòng 10 — chạy thử logic hiệu lực (03/09/2026)

Bấm/gõ thật qua Playwright, đo giá trị sau mỗi thao tác:

| Thao tác | Kết quả đo |
| --- | --- |
| Mặc định *Theo đặt cọc lần đầu* | Ngày hiệu lực **12/05/2026**, nguồn *“phiếu thu đặt cọc lần đầu — lấy từ tab Tài chính”*, 2 ô bảo lãnh **ẩn** |
| Chọn *Kể từ ngày ký* | Ngày hiệu lực → **05/05/2026** (bằng ngày ký) |
| Đổi ngày ký thành 11/06/2026 | Ngày hiệu lực **tự chạy theo → 11/06/2026** |
| Chọn *Theo bảo lãnh được duyệt* | 2 ô bảo lãnh **hiện ra**, ngày hiệu lực = ngày bảo lãnh |
| Đổi ngày + số bảo lãnh | Ngày hiệu lực → **25/07/2026**, nguồn ghi **BL-2026-0999/VCB** |
| Quay lại *đặt cọc* | 2 ô bảo lãnh **ẩn lại**, ngày hiệu lực về 12/05/2026 |
| Đổi Ngày đạt mốc 01/06 + 90 ngày | Ngày hết hiệu lực **tự tính 30/08/2026**, công thức cập nhật đúng |
| Bỏ trống số ngày | Hiện **—** + câu nhắc *“Cần nhập đủ Ngày đạt mốc và Thời hạn thực hiện”* |

Lưới sau khi bỏ `full` ở ô *Ngày có hiệu lực*: mặc định **3 + 3**, nhánh bảo lãnh **3 + 3 + 2** — không còn ô trống lẻ.
Bất biến giữ nguyên ở cả 6 tab: 0 phần tử bị thanh hành động đè · `thead` dính · cột ghim phải luôn thấy ·
không bảng nào cuộn ngang · **console 0 lỗi 0 cảnh báo**.

### Vòng 9 — đo lại sau khi chỉnh bảng cung ứng (03/09/2026)

- `thead th` của bảng cung ứng: viền trái/phải/trên **1px `#bfe3e8`**, dưới **2px teal**; **13/13** ô header có viền trái.
- Cột *Tồn kho khả dụng* hiển thị số + đơn vị; đối chiếu khớp ghi chú trong dòng chi tiết:
  ống D219 **120 Mét** (giữ được ngay) · van D100 **0 Cái** (hết tồn → buộc đặt hàng) · bộ lọc **2 Bộ**.
- 6 dòng đủ phương án có ô *Hành động* **trống**; 3 dòng thiếu vẫn còn nút *Giữ hàng* / *Đặt hàng*.
- Bảng chi tiết: **9/9 bảng có tiêu đề**, số cột tiêu đề **khớp số cột thân** ở mọi bảng; 14 dòng chi tiết, đều 8 cột.
- Đối chiếu lại PO → NCC giữa tab Cung ứng và tab Tài chính: **khớp 100%** sau khi sửa.
- Bất biến giữ nguyên: 0 phần tử bị thanh hành động đè · `thead` dính · cột ghim phải luôn thấy ·
  không bảng nào cuộn ngang · trang không cuộn ngang · console sạch.

### Vòng 8 — đo lại sau khi gộp dịch vụ & bỏ tab Hàng hoá ký (03/09/2026)

- Còn **6 tab / 6 pane**, `#p2` đã biến mất khỏi DOM; bấm lần lượt 6 tab đều mở **đúng pane tương ứng**.
- Tab chứa **2 card**: *Phương án cung ứng theo từng mã hàng* (9 dòng hàng hoá)
  và *Dịch vụ đã ký* (4 dòng: DV-INSTALL · DV-DESIGN · DV-TRAIN · DV-EXTRA).
  Khối tổng hợp đổi thành 2 block *Hàng hoá cần cung ứng* (9 mã) / *Dịch vụ đã ký* (4 gói, tiến độ TB 30,3%).
- Timeline: mốc **Ký hợp đồng không còn chip trạng thái**; các mốc *sau khi ký* vẫn giữ đánh giá đúng hạn
  (Hiệu lực *Đúng hạn* · Mặt bằng *Chậm 5 ngày* · Thiết kế *Chậm 6 ngày* · Giao hàng *Đang thực hiện*).
- ⚠️ Lỗi tự bắt được khi verify: card *Dịch vụ đã ký* ban đầu chèn **rơi ra ngoài `pane#p3`** nên hiện ở mọi tab;
  phát hiện bằng cách liệt kê con trực tiếp của `.mainpad` (có phần tử lạ ngoài 6 pane) — đã chuyển vào trong pane.
- Tab bar còn **dư 392px** sau khi bớt 1 tab; không bảng nào cuộn ngang; 0 phần tử bị thanh hành động đè;
  `thead` dính; cột ghim phải luôn thấy; **console 0 lỗi 0 cảnh báo**.

### Vòng 7 — đo lại sau khi mở ô nhập tay (03/09/2026)

Số ô nhập đếm được theo tab: Thông tin chung **6** (2 select + 4 input, 7 dấu `*`, **1 ô `TỰ TÍNH`**) ·
Tài chính **5** (1 ô lỗi bắt buộc) · Thiết kế **2** · Giao hàng **6** (1 ô lỗi) ·
Hàng hoá ký / Cung ứng / Bảo hành **0** (đúng chủ ý).

- Gõ thật bằng Playwright vào ô *lý do vượt dự toán*: nhận đủ **52 ký tự**.
- **0 ô nhập nào tràn ra ngoài ô bảng** ở cả 7 tab.
- Bất biến giữ nguyên: 0 phần tử bị thanh hành động đè · `thead` dính · cột ghim phải luôn thấy ·
  không bảng nào cuộn ngang · trang không cuộn ngang · console sạch.

### Vòng 6 — đo lại sau khi rút gọn trường & bổ sung KD phụ trách (03/09/2026)

- Bỏ khỏi tab: *Mẫu in · Người nhận cảnh báo · Cảnh báo giao hàng · Cảnh báo hết hiệu lực · Người lập · Tạo lúc*
  — đếm trong `#p1.innerText` đều **0 lần**. Riêng chuỗi *“Mẫu in”* còn 1 lần nhưng là **tên loại tài liệu**
  (`Mẫu in đã duyệt pháp chế`) trong bảng *File đính kèm*, không phải trường đã bỏ — đã truy ngược đúng phần tử.
- Card *Thông tin chung* **không còn `.meta`**; 2 card còn lại vẫn giữ meta của mình.
- Số ô mỗi nhóm: **10 · 9 · 6**. Nhóm *Thông tin hợp đồng* lẻ 1 ô ở hàng cuối nên ô *Thời gian bảo hành*
  cho **tràn hết hàng** (`.irow.full`) — không để ô đứng lẻ trong lưới 3 cột.
  Nhóm *Hiệu lực & thời hạn* gộp *Ngày bàn giao mặt bằng* vào ô *Mốc tính thời hạn* để về đúng 6 ô (3×2).
- Thanh tiêu đề thêm *KD phụ trách*, **không tràn ngang** (`scrollWidth = clientWidth = 1334`).
- Bất biến giữ nguyên: 0 phần tử bị thanh hành động đè · `thead` dính · cột ghim phải luôn thấy ·
  1 pane hiển thị · 7 tab vừa khung · không bảng nào cuộn ngang · trang không cuộn ngang · console sạch.

### Vòng 5 — đo lại sau khi bổ sung trường định danh & tô màu tab (02/09/2026)

- Nhóm *Thông tin hợp đồng* **12 ô**, 3 ô đầu = *Số hợp đồng · Trạng thái · Mã báo giá*.
- Nhóm *Thông tin khách hàng* **9 ô**, 3 ô đầu = *Mã khách hàng · Tên khách hàng · Mã số thuế*.
- Nhóm *Hiệu lực & thời hạn* **9 ô**. Cả 3 nhóm vẫn là bội số của 3 → không ô nào lẻ dòng.
- 7 tab mỗi tab một `--tc` riêng, `getComputedStyle` của icon trả đúng màu đã khai;
  tab đang chọn có màu chữ **khớp đúng `--tc`** ở cả 7 lượt bấm, luôn chỉ **1 tab active**.
- Chiều cao 7 tab **đồng đều 35px** (viền trên 2px được bù bằng `padding-top`), tab bar **không tràn** (0px).
- Bất biến giữ nguyên: 0 phần tử bị thanh hành động đè · `thead` dính · cột ghim phải luôn thấy ·
  1 pane hiển thị · không bảng nào cuộn ngang · trang không cuộn ngang · console sạch.

### Vòng 4 — đo lại sau khi gom nhóm & bỏ note điều hướng (02/09/2026)

- 4 nhóm đúng tên yêu cầu: *Thông tin hợp đồng · Thông tin khách hàng · Hiệu lực & thời hạn · File đính kèm*;
  số ô **9 · 6 · 9** (nhóm File là bảng 4 dòng) — đều bội số của 3, không nhóm nào lẻ ô.
- Tiêu đề card: **Thông tin chung** · Phụ lục hợp đồng · **Tiến độ thực hiện theo các mốc thời gian**.
- Note điều hướng: *“ở tab”* / *“tab Tài chính”* / *“Số liệu tài chính theo dõi”* đều **0 lần** trên toàn trang.
- Trùng lặp với thanh tiêu đề: *Công ty CP Cơ khí Thăng Long* và *Có hiệu lực* vẫn **0 lần** trong tab;
  *HD-2026-00147* còn 1 lần — là tên file `HD-2026-00147_ban_ky.pdf`, không phải lặp thông tin.
- **Không còn bảng nào phải cuộn ngang** ở cả 7 tab (đo `scrollWidth − clientWidth = 0` cho mọi `.tblwrap`).
- Bất biến giữ nguyên: 0 phần tử bị thanh hành động đè · `thead` dính · cột ghim phải luôn thấy ·
  1 pane hiển thị · trang không cuộn ngang · console sạch.

### Vòng 3 — đo lại sau khi dọn tab Thông tin chung (02/09/2026)

- Tab 1 còn **1 khối `.rsum`**, **0 `.rsum-blk`** (đã bỏ hết block tài chính), **3 KPI** tiến độ.
- **4 nhóm** thông tin, số ô lần lượt **6 · 6 · 3 · 3** — không nhóm nào lẻ ô.
- Đếm chuỗi trong `#p1.innerText` so với thanh tiêu đề: *Công ty CP Cơ khí Thăng Long*, *Có hiệu lực*,
  *5.038.000.000*, *45 ngày* đều **0 lần trong tab** (chỉ còn ở header); *3.778.800.000* / *3.606.000.000* /
  *974.000.000* **0 lần** — số liệu tài chính đã rời hẳn sang tab Tài chính.
- Thu gọn khối tổng hợp: **175 → 49px** (khối nhẹ hơn hẳn vòng 2 vì bỏ 2 block tiền).
- Giữ nguyên bất biến: 0 phần tử bị thanh hành động đè ở cả 7 tab · `thead` dính · cột ghim phải luôn thấy ·
  1 pane hiển thị · trang không cuộn ngang · console sạch.

### Vòng 2 — đo lại sau khi đổi bố cục (02/09/2026)

- Sidebar: 62px mặc định ↔ 236px khi bấm burger; thanh hành động bám đúng (`left` 62 ↔ 236); nhãn ẩn/hiện đúng;
  13/13 mục có tooltip. Bấm thật bằng Playwright (không chỉ dispatch) — hoạt động.
- Stepper đã gỡ khỏi DOM (`document.querySelector('.stepper') === null`).
- 7 tab **vừa khít** khung, không tràn (`clientWidth − scrollWidth = 0`, tab cuối nằm trong biên).
- Mỗi tab đúng **1 khối `.rsum`**, **0** khối `.kpis/.stats` cũ còn sót; 3/3 KPI mỗi tab đều có track;
  các ô KPI trong cùng tab **cùng chiều cao** (set chiều cao chỉ có 1 giá trị) — các box cũng vậy.
- Thu gọn khối tổng hợp: cao **286 → 49px**, nút tự đổi nhãn thành *Mở rộng*.
- Giữ nguyên các bất biến vòng 1: 0 phần tử bị thanh hành động đè · `thead` dính · cột ghim phải luôn thấy ·
  trang không cuộn ngang · 9/9 dòng cung ứng mở rộng được · **0 lỗi & 0 cảnh báo console**.

### Lỗi số liệu tự phát hiện ở vòng 2

**Tổng cột "Đang đi mua" sai** — dòng tổng ghi 218 nhưng cộng từng dòng chỉ ra 217
(2+1+1+200+12+1), kéo theo *Đã phân bổ* 1.676 sai. Đã sửa thành **217 / 1.675**, nay cân đúng:
`1.458 + 217 = 1.675` và `1.675 + 92 = 1.767 = tổng SL ký`. Kiểm lại bằng cách cộng DOM từng dòng.
Tab Hàng hoá ký cũng được kiểm tương tự: 13 dòng cộng đúng 4.580.000.000 trước VAT,
VAT 10% = 458.000.000, sau VAT 5.038.000.000; nhóm A 3.969.000.000 + B 611.000.000 khớp tổng.

### 3 lỗi tự phát hiện & sửa trong lúc verify (vòng 1)

1. **`thead` sticky không bao giờ dính** — `.tblwrap{overflow-x:auto}` là scroll-container nhưng không cuộn
   dọc nên `top:0` không có gì để bám; đo được `theadTop: -124` (header trôi khỏi màn). Sửa: thêm
   `max-height` + `overflow:auto` cho `.tblwrap`. *(Lỗi này có sẵn trong mockup báo giá — cần sửa kèm khi port.)*
2. **Tab 7 tràn khỏi màn** ở 1440px (`tabsScrollW 1208 > clientW 1160`). Sửa: rút gọn nhãn tab 2 & 6, giảm padding tab.
3. **Cột Hành động rơi ngoài vùng cuộn** (bảng `min-width:1320`) → ghim `.stick-r`; sau đó cột ghim lại che
   đuôi cột *Đã về kho* → thu gọn độ rộng cột, hạ `min-width` về 1160, `td.name` min 200→170px.

## Cách làm việc tiếp

User xem `mockup.html`, ghi chú yêu cầu chỉnh → sửa thẳng trên mockup, mỗi yêu cầu 1 task ở `plan.md`.
Chốt UI xong mới sang bước design chi tiết (DB/BE/FE) cho màn thật.
