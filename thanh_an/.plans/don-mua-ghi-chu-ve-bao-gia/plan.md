# Plan — Ghi chú ở Đơn mua hàng đẩy ngược về Báo giá gốc

Phụ trách: @khoipv
Màn: `supply/purchase_orders` (nhập ghi chú) → `plan/quotation` (hiển thị cột mới, chỉ đọc)

## Bối cảnh / Yêu cầu
- Ở Đơn mua hàng (tab Hàng hóa) mỗi dòng hàng có ô **Ghi chú** tách theo từng HĐ bán (`purchase_order_products.purposes[].note`).
- Yêu cầu: ghi chú đó **update trực tiếp về báo giá gốc** của hàng hóa; màn Báo giá thêm cột **"Ghi chú cung ứng"** — **chỉ hiển thị, không sửa**.

## Quyết định đã chốt với user
1. **Tìm báo giá**: chỉ đi qua HĐ bán — `purposes[].contract_id` → `contracts.quotation_id`. (User bác phương án dò thêm qua gói thầu.)
2. **Thời điểm đẩy**: khi **lưu đơn mua** (store + update), trong cùng transaction.
3. **Trùng ghi chú**: **ghi đè** giá trị cũ.
4. **Hàng trùng nhiều dòng trong 1 báo giá**: **ghi vào tất cả** dòng có cùng `(quotation_id, product_id)`.
5. **Xóa trắng ghi chú ở đơn mua** → **xóa luôn** bên báo giá (rỗng cũng là một lần ghi đè).
6. **Vị trí cột** ở bảng hàng hóa Báo giá: **sau "Ghi chú đặc biệt"**.
7. **Chống mất dữ liệu khi lưu báo giá**: sửa `QuotationService::syncGroups()` giữ lại giá trị ở BE (**hàm dùng chung — user đã đồng ý riêng điểm này**), KHÔNG bắt FE round-trip.

## BE
- [x] Migration `add_note_supply_to_quotation_tab_products` — `text('note_supply')->nullable()->after('special_note')` + index `(quotation_id, product_id)` (không FK)
- [x] `QuotationTabProduct::$fillable` thêm `note_supply`
- [x] `PurchaseOrderService::syncNoteToQuotation($items)` — gom `(contract_id, product_id, note)` từ `purposes[]`, map `contracts.quotation_id`, update `quotation_tab_products` theo `(quotation_id, product_id)`; gọi sau `syncProducts()` ở cả `store()` và `update()`
- [x] `QuotationService::syncGroups()` — snapshot `product_id => note_supply` trước khi xóa, gán lại sau khi insert
- [x] `php -l` các file sửa

## FE
- [x] `pages/plan/quotation/components/ProductComponent.vue`:
  - [x] Thêm field `note_supply` (label "Ghi chú cung ứng", isVisible) sau `special_note` trong `columns`
  - [x] Template body **read-only** (không textarea/input)
  - [x] Class độ rộng `note_supply: td-width-200`
  - [x] Header + giá trị xuất Excel
  - Không map vào payload submit — BE đã tự bảo toàn

## Verify
- [x] Nhập ghi chú ở 1 dòng DMH có HĐ bán gắn báo giá → lưu → `quotation_tab_products.note_supply` đúng giá trị
- [x] Mở màn Báo giá → cột "Ghi chú cung ứng" hiện đúng, không sửa được
- [x] Bấm Lưu ở Báo giá → ghi chú **không** bị mất
- [x] Xóa trắng ghi chú ở DMH → lưu → báo giá về rỗng
- [x] Hàng trùng nhiều dòng trong cùng báo giá → cả các dòng đều nhận ghi chú

### Checkpoint — 2026-09-14
Vừa hoàn thành: Toàn bộ BE + FE. Migration đã chạy trên DB (cột `note_supply` text/nullable + index `qtp_quotation_product_idx`). `php -l` 3 file BE sạch, template + script ProductComponent.vue compile sạch.
Verify tự động trên dữ liệu thật (bọc transaction, đã rollback): **10/10 PASS** — ghi mới · ghi đè · xóa trắng → null · purposes thiếu contract_id giữ nguyên · dòng mua ngoài giữ nguyên · payload rỗng giữ nguyên · HĐ không có báo giá bỏ qua · ghi vào tất cả dòng trùng mã (dựng 2 dòng) · lưu báo giá KHÔNG mất ghi chú. (Bỏ qua 1 case: DB hiện không có 2 HĐ bán cùng trỏ 1 báo giá.)
Đang làm dở: (không)
Bước tiếp theo: User test trên trình duyệt — ⚠️ sửa cả BE lẫn FE nên phải **build lại client + hard refresh**.
Blocked:

## Bug phát hiện khi user test — ghi chú lây sang HĐ khác (ĐÃ SỬA)
Triệu chứng user báo: "gộp ghi chú ở đơn mua hàng, nhập ở dòng đầu tiên nó lại ăn cả các dòng dưới, và chữ đầu tiên không xóa đi được hết".

**Root cause (FE `pages/supply/purchase_orders/components/ProductsTab.vue`) — 2 lỗi chồng nhau:**
1. `onGroupNote()` gọi `fillPurposeField(p, 'note', p.note)` ở **MỌI lần gõ**. Gõ "abc": lần gõ thứ 2 có `p.note = 'a'`, các HĐ khác chưa có ghi chú nên bị copy `'a'` vào **dữ liệu thật** của chúng.
2. `noteOfGroup()` fallback `p.note` **vô điều kiện** khi HĐ chưa có ghi chú riêng. `p.note` là chuỗi ghép của cả dòng (`syncRowNote` nối ` | `) → ô của HĐ chưa nhập hiện ghi chú của HĐ khác, và ô vừa xóa trắng nhảy về giá trị cũ.

Kết hợp: xóa hết ô HĐ1 thì ký tự `'a'` đã lây sang HĐ2 quay lại qua fallback ⇒ đúng triệu chứng "chữ đầu tiên không xóa được hết".

**Fix:**
- [x] `noteOfGroup()`: chỉ fallback `p.note` khi **toàn dòng chưa HĐ nào có ghi chú riêng** (đơn cũ lưu trước khi tách ghi chú theo HĐ); dòng không có purposes vẫn dùng thẳng `p.note`.
- [x] `onGroupNote()`: chỉ `fillPurposeField` **một lần duy nhất** — trước lần sửa đầu tiên của đơn cũ có `p.note`, để các HĐ khác giữ ghi chú đang hiển thị; sau đó không lây nữa.
- [x] KHÔNG đụng `onGroupBuyer`/`buyerOfGroup` (cột Cty thực hiện mua) — cùng khuôn nhưng ngoài phạm vi yêu cầu.
- [x] Verify bằng script mô phỏng đúng logic 2 hàm: bản cũ tái hiện đủ 3 triệu chứng (ô HĐ2 ăn theo, dữ liệu HĐ2 bị lây `'a'`, xóa trắng còn sót `'a'`); **bản mới 13/13 PASS** (gõ/xóa 1 HĐ · 2 HĐ ghi chú riêng · xóa 1 HĐ không ảnh hưởng HĐ kia · đơn cũ giữ ghi chú khi sửa 1 HĐ · dòng mua ngoài). Template + script compile sạch.

⚠️ **Dữ liệu đã lưu trước fix**: đơn mua nào đã nhập ghi chú theo kiểu này có thể đang mang ghi chú lây ở các HĐ khác (và nay bị đẩy sang `quotation_tab_products.note_supply`). DB local đang sạch (`note_purposes` toàn null) — cần user kiểm tra trên môi trường đang dùng, sửa lại ghi chú rồi lưu đơn là giá trị đúng sẽ ghi đè.

### Checkpoint — 2026-09-14 (bổ sung)
Vừa hoàn thành: Fix bug ghi chú lây giữa các HĐ bán ở tab Hàng hóa của Đơn mua hàng.
Đang làm dở: (không)
Bước tiếp theo: User build lại client + hard refresh, test lại nhập/xóa ghi chú trên dòng gộp nhiều HĐ.
Blocked:

## Yêu cầu bổ sung — tách cột "Cty thực hiện bán" theo từng HĐ bán (ĐÃ XONG)
Yêu cầu user: *"cột công ty thực hiện bán cũng thêm phân tách dòng ra cho tôi là của hđ nào nữa nhé"*.

Bối cảnh: tab Hàng hóa của Đơn mua hàng cắt 1 dòng hàng thành **2 tầng dòng con** — `rowGroupsOf(p)` cắt theo KHÁCH HÀNG (`g`), rồi `withContractSubs()` cắt tiếp theo HỢP ĐỒNG BÁN (`sg` trong `g.subs`). Cột "Cty thực hiện bán" trước đây gộp ở tầng khách hàng (`v-if="si === 0"` + `rowspan`), trong khi 1 khách có thể có nhiều HĐ và **mỗi HĐ do một công ty khác nhau thực hiện bán**.

**Sửa (`hrm-thanhan-client/pages/supply/purchase_orders/components/ProductsTab.vue`, dòng ~298):**
- [x] Bỏ `v-if="si === 0"` và `:rowspan="g.subs.length"` trên `<td class="cell-sale-company">`.
- [x] Đổi nguồn dữ liệu `saleCompanyOfPurposes(g.purposes)` → `saleCompanyOfPurposes(sg.purposes)` (nhóm theo HĐ bán thay vì theo khách hàng).
- [x] Không đổi JS/logic nào khác, không đụng cột "Cty thực hiện mua".

**Verify — SSR render thật** (`vue` + `vue-server-renderer` 2.6.14 có sẵn trong node_modules; stub các component con), **20/20 PASS** trên 4 kịch bản:
| Kịch bản | Kết quả |
|---|---|
| 1 khách – 2 HĐ, 2 cty bán khác nhau | 2 ô riêng `["Cty Thành An","Cty Miền Bắc"]`, không còn rowspan |
| 2 khách – mỗi khách 1 HĐ | `["Cty Thành An","Cty Miền Nam"]` |
| 2 khách – khách đầu có 2 HĐ | `["Cty Thành An","Cty Miền Bắc","Cty Miền Nam"]` |
| Dòng mua ngoài (không có phiếu đề xuất) | hiển thị `—`, không vỡ bảng |

Mỗi kịch bản còn kiểm tra: ghi chú vẫn tách đúng theo từng HĐ, và **tổng ô mỗi dòng con + ô rowspan mang xuống = đúng 20 cột header** (đảm bảo bảng không lệch cột).

### Checkpoint — 2026-09-14 (bổ sung 2)
Vừa hoàn thành: Tách cột "Cty thực hiện bán" theo từng hợp đồng bán ở tab Hàng hóa của Đơn mua hàng + verify SSR 20/20 PASS.
Đang làm dở: (không)
Bước tiếp theo: User build lại client + hard refresh, test 3 phần: (1) ghi chú đẩy về Báo giá, (2) ghi chú không còn lây giữa các HĐ, (3) cột Cty thực hiện bán tách dòng theo HĐ.
Blocked:

## Yêu cầu bổ sung 2 — bảng hàng hóa khó đọc, không biết giá/cty/ghi chú của dòng nào (ĐÃ XONG)
Yêu cầu user: *"xem có cách nào sửa lại cho bảng nó dễ nhìn hơn không chứ hiện tại tôi thấy giá bán, cty thực hiện, ghi chú các thứ đang hơi khó biết nó của dòng nào?"*

**Root cause (trực quan):** bảng gộp ô ở **3 tầng khác nhau** trên cùng một hàng ngang —
1. cả dòng hàng (`rowspan="row.subCount"`): STT/mã/tên/quy cách/ĐVT/hãng/SL/thành tiền/ngày cần/xóa **+ 4 cột tham chiếu**;
2. theo khách hàng (`rowspan="g.subs.length"`): Đơn giá có VAT, Cty thực hiện mua;
3. theo HĐ bán (không gộp): Mục đích mua, Cty thực hiện bán, Ghi chú.

Thủ phạm chính là **4 cột tham chiếu** (Đơn giá báo giá, Ghi chú báo giá/thầu/HĐ): gộp cả dòng hàng rồi *bên trong ô* tự liệt kê `HĐ-01: …` / `HĐ-02: …`, mà ô lại căn giữa theo chiều dọc → các dòng bên trong **không thẳng hàng** với dòng HĐ thật bên phải, mắt phải tự dò theo mã HĐ.

**Quyết định đã chốt với user:**
- Làm **cách 1**: hạ 4 cột tham chiếu xuống từng dòng HĐ + tô rõ ranh giới dòng. (Bác phương án gộp 3 cột ghi chú tham chiếu làm 1.)
- Cột **Đơn giá có VAT** và **Cty thực hiện mua**: **giữ y nguyên** (vẫn gộp theo khách hàng, không thêm nhãn tên khách).

**Task (`hrm-thanhan-client/pages/supply/purchase_orders/components/ProductsTab.vue`):**
- [x] Thêm helper `subCid(sg)` — lấy `contract_id` của dòng con (mọi purposes trong `sg` cùng 1 HĐ do `withContractSubs` cắt theo `contractKey`).
- [x] 4 ô tham chiếu: bỏ `v-if="gi===0 && si===0"` + `:rowspan="row.subCount"`, mỗi dòng con chỉ hiện giá trị của HĐ của chính nó; bỏ tiền tố `HĐ-xx:` (thừa vì cột Mục đích mua cùng hàng đã ghi mã HĐ); không có HĐ → `—`.
- [x] Cột Đơn giá báo giá căn phải (số), 3 cột ghi chú căn trái.
- [x] CSS: kẻ **2px** ngăn giữa các hàng hóa (`tr.row-first`), kẻ **nét đứt** giữa các dòng con (`tr.grp-sub`), **hover sáng cả hàng ngang**, ô gộp nhiều dòng căn `vertical-align: top` cho thẳng dòng con đầu.
- [x] Dọn CSS không còn dùng (`.ref-wrap`, `.ref-line`, `.ref-hd`); giữ `.ref-val` (pre-line cho newline thật trong ghi chú) và `.ref-none`.
- [x] Số cột giữ nguyên 20 → dòng TỔNG CỘNG không phải sửa.
- [x] Verify bằng SSR render thật: số ô mỗi dòng con khớp header, giá trị tham chiếu khớp đúng HĐ của từng dòng.

**Verify — SSR render thật, 45/45 PASS** trên 4 kịch bản (1 khách 2 HĐ · 2 khách khách đầu có 2 HĐ · dòng mua ngoài không có HĐ · 2 hàng hóa). Mỗi kịch bản kiểm 11 điểm: số ô tham chiếu = 4 × số dòng con · ô tham chiếu không còn `rowspan` · không còn tiền tố `HĐ-xx:` · Đơn giá báo giá và 3 ghi chú tham chiếu khớp ĐÚNG HĐ của từng dòng (kể cả ô rỗng ra `—`) · Cty thực hiện bán + Ghi chú vẫn tách đúng · mỗi hàng hóa đúng 1 `tr.row-first`, các dòng còn lại là `grp-sub` · tổng ô mỗi dòng + rowspan mang xuống = đúng 20 cột header.
SCSS compile sạch bằng node-sass; đã kiểm specificity: rule hover (0,4,3) thắng `td.cell-ref` / `tr.grp-sub` / `td.col-freeze`, `td[rowspan]:not([rowspan='1'])` (0,3,1) thắng `td { vertical-align: middle }`.

### Checkpoint — 2026-09-14 (bổ sung 3)
Vừa hoàn thành: Tách 4 cột tham chiếu theo từng HĐ + kẻ đậm/nét đứt/hover/căn top cho bảng hàng hóa Đơn mua hàng.
Đang làm dở: (không)
Bước tiếp theo: User build lại client + hard refresh, xem bảng đã dễ đọc chưa.
Blocked:

## Yêu cầu bổ sung 3 — hover cũ không dùng được, sáng cả khối hàng hóa bằng JS (ĐÃ XONG)
Yêu cầu user: *"không được, tôi thấy hover như vậy không được"* → chốt phương án **"Sáng cả khối hàng hóa bằng JS"**: trỏ vào bất kỳ dòng con nào thì TẤT CẢ dòng của hàng hóa đó sáng (kể cả các ô gộp: tên hàng, SL mua, đơn giá có VAT), riêng dòng đang trỏ đậm hơn.

**Root cause của hover cũ:** rule `tbody tr:hover > td` là CSS thuần, mà **ô có `rowspan` chỉ thuộc `<tr>` ĐẦU khối**. Khi chuột ở dòng con thứ 2 trở đi, các ô gộp nằm ở dòng khác nên không nhận `:hover` → chỉ sáng được nửa hàng, càng rối hơn không hover. CSS không có selector "cha của dòng đang hover" ⇒ bắt buộc dùng state JS.

**Task (`hrm-thanhan-client/pages/supply/purchase_orders/components/ProductsTab.vue`):**
- [x] `data`: thêm `hoverRow` (index dòng hàng) + `hoverSub` (khoá `g.key + '#' + sg.key` của dòng con).
- [x] `methods`: `setHover(idx, g, sg)` và `clearHover()`.
- [x] Template: `<tbody @mouseleave="clearHover">`, mỗi `<tr>` thêm `@mouseenter="setHover(row.idx, g, sg)"` và 2 class `hl-row` (cùng hàng hóa) / `hl-sub` (đúng dòng đang trỏ).
- [x] CSS: bỏ rule `:hover` thuần; thêm `tr.hl-row > td` (nhạt) và `tr.hl-sub > td` (đậm hơn, đặt SAU vì cùng độ ưu tiên). Dòng cảnh báo SL lệch giữ tông đỏ qua `tr.warning-row.hl-row` / `.hl-sub` để không bị màu xanh nuốt mất tín hiệu.

**Verify — SSR render thật, 13/13 PASS** trên 5 kịch bản (gọi thẳng `vm.setHover(...)` rồi đọc class từng `<tr>`):
| Kịch bản | Kết quả |
|---|---|
| Không hover | không dòng nào có `hl-row`/`hl-sub` |
| Hover dòng con thứ 2 (khách A / HĐ-02) | cả 3 dòng của hàng hóa 1 có `hl-row`, **kể cả dòng đầu chứa các ô rowspan**; hàng hóa 2 không bị ảnh hưởng; đúng 1 dòng có `hl-sub` và ở đúng dòng con thứ 2 |
| Hover dòng con thứ 3 (khách B) | cả 3 dòng `hl-row`, `hl-sub` đúng dòng thứ 3 |
| Hover hàng hóa 2 | hàng hóa 1 sạch, dòng hàng hóa 2 có cả `hl-row` + `hl-sub` |
| Hover dòng cảnh báo SL lệch | vẫn giữ `warning-row`, cả 2 dòng có `hl-row` |

Ghi chú harness: `renderToString` gọi callback **đồng bộ** nên chạy 5 case lồng nhau làm tràn stack từ case thứ 4 — tách bằng `setImmediate(done)`, không liên quan component.

### Checkpoint — 2026-09-14 (bổ sung 4)
Vừa hoàn thành: Thay hover CSS thuần bằng highlight cả khối hàng hóa điều khiển bằng JS (`hoverRow`/`hoverSub`) + verify SSR 13/13 PASS.
Đang làm dở: (không)
Bước tiếp theo: User build lại client + hard refresh, rê chuột kiểm tra cả khối sáng đúng.
Blocked:

## Yêu cầu bổ sung 4 — BỎ HẲN tô nền khi rê chuột (ĐÃ XONG)
Yêu cầu user: *"thôi bạn bỏ cái background khi hover vào giúp tôi đi"* → bỏ luôn highlight hover, không thay bằng hiệu ứng khác.

**Task (`hrm-thanhan-client/pages/supply/purchase_orders/components/ProductsTab.vue`):**
- [x] Template: `<tbody @mouseleave="clearHover">` → `<tbody>`; bỏ `@mouseenter="setHover(...)"` và 2 class `hl-row` / `hl-sub` trên `<tr>`.
- [x] `data`: bỏ `hoverRow`, `hoverSub`. `methods`: bỏ `setHover`, `clearHover`.
- [x] CSS: bỏ 4 rule `tbody tr.hl-row/.hl-sub/.warning-row.hl-row/.warning-row.hl-sub > td`.
- [x] **GIỮ NGUYÊN** phần phân tách dòng đã làm ở bổ sung 2/3: kẻ 2px giữa các hàng hóa (`tr.row-first`), nét đứt giữa dòng con (`tr.grp-sub` + nền `#fbfcfe`), ô gộp `vertical-align: top`, nền tím nhạt 4 cột tham chiếu, tông đỏ `warning-row`. Các rule `&:hover` còn lại chỉ đổi **màu chữ** của 3 link mở popup (đề xuất / xử lý / hợp đồng), không phải nền bảng.

**Verify:** SSR render thật lại toàn bộ bảng — **45/45 PASS** (4 kịch bản, số ô mỗi dòng + rowspan mang xuống = đúng 20 cột header, giá trị tham chiếu vẫn khớp đúng HĐ từng dòng). SCSS compile sạch bằng node-sass.

### Checkpoint — 2026-09-14 (bổ sung 5)
Vừa hoàn thành: Gỡ toàn bộ cơ chế tô nền khi rê chuột (template + data + methods + CSS), giữ nguyên phần kẻ phân tách dòng.
Đang làm dở: (không)
Bước tiếp theo: User build lại client + hard refresh, xác nhận bảng không còn đổi nền khi rê chuột.
Blocked:

## Yêu cầu bổ sung 5 — căn giữa theo chiều cao 4 cột Đơn giá / Thành tiền / Cty thực hiện mua / Ngày cần (ĐÃ XONG)
Yêu cầu user: *"các cột đơn giá, thành tiền, cty thực hiện mua, ngày cần để căn giữa theo chiều cao cho tôi"*.

Bối cảnh: ở bổ sung 2 đã đặt `td[rowspan]:not([rowspan='1']) { vertical-align: top }` để ô gộp thẳng hàng với dòng con đầu. Nhưng 4 cột này nội dung chỉ là **1 ô nhập / 1 con số duy nhất** nên căn lên trên nhìn bị lệch.

**Sửa (`hrm-thanhan-client/pages/supply/purchase_orders/components/ProductsTab.vue`, khối `<style>`):**
- [x] Thêm rule đè sau rule `vertical-align: top`: `td.cell-price[rowspan], td.cell-amount[rowspan], td.cell-buyer[rowspan], td.cell-need[rowspan] { vertical-align: middle; }`.
- [x] Kèm `[rowspan]` để đủ độ ưu tiên: `td[rowspan]:not([rowspan='1'])` = (0,2,1) — nếu chỉ viết `td.cell-price` (0,1,1) sẽ bị đè. Rule mới cũng (0,2,1) nhưng **đứng sau** nên thắng.
- [x] Không đụng template, không đổi số cột.

**Verify:** SCSS compile sạch bằng node-sass (đã xem CSS sinh ra, 4 selector đúng thứ tự sau rule `top`); SSR render lại toàn bảng **45/45 PASS**.

**Bổ sung tiếp (cùng yêu cầu):** *"cột SL đề xuất mua, SL mua nữa"* →
- [x] Ô "SL mua" trước đó chỉ có `class="num"`, không có class riêng → đặt thêm `cell-oq` để CSS bám vào được.
- [x] Thêm `td.cell-propsum[rowspan]` (SL đề xuất mua) và `td.cell-oq[rowspan]` vào cùng rule `vertical-align: middle`.
- [x] Verify lại: SCSS compile sạch, SSR 45/45 PASS. → **6 cột căn giữa**: SL đề xuất mua · SL mua · Đơn giá có VAT · Thành tiền · Cty thực hiện mua · Ngày cần.

### Checkpoint — 2026-09-14 (bổ sung 6)
Vừa hoàn thành: Căn giữa theo chiều cao cho 6 cột SL đề xuất mua / SL mua / Đơn giá có VAT / Thành tiền / Cty thực hiện mua / Ngày cần.
Đang làm dở: (không)
Bước tiếp theo: User build lại client + hard refresh, xem 4 cột đã căn giữa ô gộp chưa.
Blocked:

## Yêu cầu bổ sung 6 — nền bảng loang lổ "chỗ có màu chỗ không" (ĐÃ XONG)
Yêu cầu user: *"sao tôi thấy background nó cứ lung tung hết lên vậy, chỗ có màu chỗ không vậy"*.

**Root cause:** `tr.grp-sub > td { background: #fbfcfe }` tô nền cho dòng con thứ 2 trở đi, **nhưng ô gộp (`rowspan`) chỉ tồn tại ở `<tr>` ĐẦU khối** (`row-first`, không mang class `grp-sub`). Hậu quả trong CÙNG một khối hàng hóa: nửa trái (STT/mã/tên/SL/đơn giá/thành tiền/ngày cần) trắng, nửa phải (mục đích mua, 4 cột tham chiếu, cty bán, ghi chú) xám → nhìn răng cưa.
Làm nặng thêm: `tr.grp-sub > td` (0,1,2) **đè** `td.cell-ref` (0,1,1) → 4 cột tham chiếu ở dòng đầu là tím nhạt nhưng ở dòng con lại thành xám, tức **cùng 1 cột mà 2 màu**. Cộng thêm `td.cell-propsum` tô riêng 1 cột xám → tổng cộng 3 lớp nền chồng nhau không đồng bộ.

**Sửa (`hrm-thanhan-client/pages/supply/purchase_orders/components/ProductsTab.vue`, khối `<style>`) — làm phẳng nền thân bảng:**
- [x] Bỏ `background: #fbfcfe` ở `tr.grp-sub > td`, **giữ nguyên** `border-top: 1px dashed` (vẫn phân tách dòng con bằng đường kẻ — đường kẻ không bị lỗi rowspan như màu nền).
- [x] Bỏ `background: #f7faf9` ở `td.cell-propsum` (giữ `color`).
- [x] Bỏ `background: #faf9fe` ở `td.cell-ref`; **giữ** nền tím `th.cell-ref-h` ở HEADER để vẫn nhận ra nhóm 4 cột chỉ-xem (header chỉ 1 hàng nên không bị lệch).

**Nền còn lại (đều là nền CHỨC NĂNG, áp cho cả dòng nên không loang lổ):** header `#eef4f3` · dòng cảnh báo SL lệch `.warning-row td` `#fcefec` · dòng TỔNG CỘNG `#eef4f3` · `td.col-freeze` `#fff` (bắt buộc để 3 cột đông cứng không bị nội dung cuộn lộ xuyên qua, có biến thể theo `warning-row` / `total-row`) · các badge/input nhỏ (`.pp-qty`, `input.pp-buy`, `inp-oq.oq-over`, `inp-oq.oq-under`).

**Verify:** SCSS compile sạch bằng node-sass; SSR render lại toàn bảng **45/45 PASS**.

### Checkpoint — 2026-09-14 (bổ sung 7)
Vừa hoàn thành: Làm phẳng nền thân bảng hàng hóa (bỏ 3 lớp nền trang trí gây răng cưa do rowspan), giữ nét kẻ phân tách dòng.
Đang làm dở: (không)
Bước tiếp theo: User build lại client + hard refresh, xem nền bảng đã đều chưa.
Blocked:

## Yêu cầu bổ sung 7 — màn XEM CHI TIẾT bỏ cột "Xóa" (ĐÃ XONG)
Yêu cầu user: *"mà xem chi tiết thì bỏ cột xóa đi cho tôi"*.

Trước đây màn chi tiết vẫn giữ cột "Xóa" nhưng ô rỗng (nút xóa đã có `v-if="!readonly"`) → thừa 1 cột trắng.
`ProductsTab` nhận `:readonly="isShow"` từ `PurchaseOrderForm.vue` (dòng 29), `isShow` = chế độ xem chi tiết.

**Sửa (`hrm-thanhan-client/pages/supply/purchase_orders/components/ProductsTab.vue`):**
- [x] `<th style="width: 64px">Xóa</th>` → thêm `v-if="!readonly"`.
- [x] Ô Xóa trong thân bảng: `v-if="gi === 0 && si === 0"` → `v-if="!readonly && gi === 0 && si === 0"`.
- [x] Dòng TỔNG CỘNG: ô cuối (ứng với cột Xóa) thêm `v-if="!readonly"` — nếu quên, dòng tổng thừa 1 ô và lệch toàn bộ bảng.
- [x] `computed colspan`: `20` → `this.readonly ? 19 : 20` (dùng cho dòng "Không có hàng hóa phù hợp bộ lọc").

**Verify — SSR render thật, 14/14 PASS** trên 2 chế độ:
| Chế độ | Số cột header | Kiểm |
|---|---|---|
| `readonly = true` (xem chi tiết) | **19** | header không còn `Xóa`; mỗi dòng con (ô + rowspan mang xuống) = 19; dòng TỔNG CỘNG tổng colspan = 19; `colspan` dòng rỗng = 19 |
| `readonly = false` (thêm/sửa) | **20** | header vẫn có `Xóa`; các số tương ứng = 20 (không đổi hành vi cũ) |

### Checkpoint — 2026-09-14 (bổ sung 8)
Vừa hoàn thành: Ẩn hẳn cột "Xóa" ở màn xem chi tiết đơn mua hàng (header + thân + dòng tổng + computed colspan).
Đang làm dở: (không)
Bước tiếp theo: User build lại client + hard refresh, mở chi tiết 1 đơn mua xem cột Xóa đã biến mất và bảng không lệch cột.
Blocked:
