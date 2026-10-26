# Kế thừa giá bán theo hãng — Design

> 24/10/2026 · @namdangit · nhánh `gop_db` (checkout chính hrm-api + hrm-client). Chốt Q1–Q13: `ton.md`.
> ⛔ Không phải lệnh code — code phải xin "làm" riêng kèm phạm vi (có migration + quyền mới ⇒ nêu rõ).

## 1. Nghiệp vụ

### Chốt cũ bị thay
| Chốt cũ | Nay |
|---|---|
| Luồng tính giá Q3/Q4 + D1: "cả luồng trong 1 công ty, không tính giá hộ" | Hàng kế thừa: YCHG tách sang **công ty quản lý** tính giá; giá áp cho công ty quản lý + mọi công ty đang kế thừa |
| Giá theo công ty P1–P14: mỗi công ty tự quản bộ giá | Hàng kế thừa: bộ giá công ty kế thừa là **bản chép** của công ty quản lý, không sửa được |
| Sàn giá 21/10 (`OwnerPriceFloor`) | Vẫn giữ cho hàng tự tính giá; hàng kế thừa luôn bằng giá nguồn ⇒ không phát sinh |
| Chuyển KD không tính giá 23/10 | Chỉ còn cho hàng **không** kế thừa |

### Định nghĩa "hàng kế thừa" (MỘT nguồn luật)
Hàng `p` tại công ty `c` **kế thừa** khi đủ cả 3:
1. `p.company_id ≠ c` (Q2 — hàng công ty mình tạo luôn tự tính giá);
2. `p.manufacture_id` có giá trị (hàng không có hãng ⇒ tự tính giá — *tự chốt T1*);
3. hãng đó là "kế thừa" theo cài đặt của `c` (Q13):
   - chế độ **Chọn hãng kế thừa** (mặc định, kể cả công ty chưa cài): hãng nằm trong danh sách;
   - chế độ **Chọn hãng tự xây dựng**: hãng KHÔNG nằm trong danh sách.

Công ty nguồn = `p.company_id`. Trạng thái kế thừa **suy ra lúc đọc**, không lưu cờ theo từng hàng (Q10 chọn ghi đè ⇒ không
cần cờ riêng).

### Vòng đời hàng kế thừa ở công ty kế thừa
1. Lấy về ⇒ *Đang nhập thông tin* (như cũ). Nhập thông tin quản trị theo công ty ⇒ Lưu thông tin (`info_entered_at`).
2. Thao tác **"Chuyển kinh doanh (kế thừa giá)"** (Q4) ở màn Nhập thông tin + Dữ liệu hàng hoá công ty + footer chi tiết, theo
   dòng + hàng loạt (≤ 100), popup xác nhận. Điều kiện mỗi mã: hàng kế thừa · `pcc.status = 1` · đã Lưu thông tin · có ≥ 1 ĐVT ·
   `products.status = 1` · công ty nguồn có dòng `pcc` không phải 4 (*tự chốt T2*: nguồn khoá ⇒ bỏ qua, báo "Công ty quản lý đã
   ngừng kinh doanh hàng này"). Giá nguồn 0 vẫn cho (Q5).
   Kết quả: chép bộ giá (§3) ⇒ `pcc.status` 1 → 3 ⇒ lịch sử hàng hoá ghi chú "Kế thừa giá từ <mã công ty nguồn>".
3. Hàng kế thừa trạng thái 1: ẩn *Chuyển KD không tính giá* + *Lập YCHG* (Q4); BE từ chối nếu gọi thẳng.
4. Đang KD: giá tự đổi theo nguồn (§3). Khoá / khôi phục ở công ty kế thừa như cũ (Đ2 — về Đang KD). Nguồn khoá ⇒ giữ giá cuối,
   vẫn bán (Q9).

## 2. Cài đặt — màn "Giá bán theo hãng sx"

- **Menu**: Tài chính › Quản lý giá - CTKM › Giá bán › *Giá bán theo hãng sx* (`/finance/manufacture-price-modes`), gate quyền mới.
- **Quyền mới** (Q12): "Cài đặt giá bán theo hãng" — type 8 Tài chính, id mới (kiểm `uniq -d` seeder + DB trước khi chọn),
  khai 1 dòng `$this->perm([...])` trong `PermissionsTableSeeder` (đồng bộ theo tên — CLAUDE.md 14/10, không seeder riêng).
  Xem + sửa cùng 1 quyền, xét theo công ty đang làm.
- **Màn** (1 trang, công ty đang làm):
  - Radio chế độ: *Chọn hãng tự xây dựng giá bán* / *Chọn hãng kế thừa giá theo công ty quản lý*. Nhãn danh sách đổi theo chế độ.
  - Bảng hãng đã chọn: Mã hãng · Tên hãng · Số mã hàng đang KD bị ảnh hưởng · Xoá dòng. Nút **Chọn hãng** mở popup chọn nhiều
    (khuôn popup Chọn hãng của Chính sách giá bán nội bộ — mọi hãng, tick giữ khi đổi từ khoá). Ô tìm trong bảng.
  - **Lưu**: BE tính chênh lệch trước/sau ⇒ trả *bản xem trước*: số hàng chuyển sang kế thừa (sẽ ghi đè giá — Q10), số hàng thôi kế
    thừa (giữ giá cuối — Q11), danh sách YCHG đang chạy chặn đổi (Q10). Popup xác nhận ⇒ lưu thật trong 1 transaction.
  - Nút **Lịch sử** (skill `entity-history`): đổi chế độ · thêm / bỏ hãng · người · lúc; mỗi lần lưu ghi kèm số hàng bị đổi giá.
  - unsaved-changes khi rời trang.
- **CSDL** (migration mới):
  - `manufacture_price_modes`: `company_id` UNIQUE · `mode` (1 Chọn hãng kế thừa · 2 Chọn hãng tự xây dựng) · audit.
  - `manufacture_price_mode_items`: `company_id` · `manufacture_id` · UNIQUE(company_id, manufacture_id) · audit.
  - Lịch sử: `catalog_histories` (table_name `manufacture_price_modes`, table_id = dòng công ty).

### Đổi cài đặt (Q10, Q11)
- Hàng **chuyển sang kế thừa**, đang KD (`pcc.status = 3`): ghi đè ngay bằng giá nguồn (§3), lịch sử giá từng dòng "Kế thừa từ <công
  ty> (đổi cài đặt)". Yêu cầu Duyệt giá đang chờ của các dòng đó ⇒ huỷ (*tự chốt T3*, ghi lịch sử).
- Hàng chuyển sang kế thừa nằm trong YCHG đã gửi của công ty mình (`pcc.status` 2/5) ⇒ **chặn lưu**, 422 liệt kê số phiếu.
- Hàng trạng thái 1 / 4: không ghi giá; trạng thái 4 khi khôi phục mới chép (*tự chốt T4*: khôi phục hàng kế thừa ⇒ chép giá nguồn
  trước rồi về Đang KD).
- Hàng **thôi kế thừa**: không đụng giá (giữ giá cuối thành giá riêng); từ đó sửa được ở Cập nhật giá + hỏi giá trong công ty.
- Khối lượng: một lần lưu có thể chạm hàng chục nghìn dòng (123.060 dòng lấy về đang KD trên local) ⇒ chép bằng câu SQL theo lô
  (INSERT … SELECT / UPDATE JOIN theo `product_unit_id`), không lặp từng hàng qua PHP; lịch sử giá ghi gộp theo lô. Đo thời gian
  trên DB local trước khi chốt plan; nếu > 30 s ⇒ chuyển sang job nền + màn báo "đang áp" (*hỏi lại user lúc plan*).

## 3. Chép + đồng bộ giá

**Lớp mới** `ProductPrice/InheritedPriceSync` (1 nguồn cho mọi đường):
- `copy(productIds, targetCompanyId)` — dùng cho nút Chuyển KD, đổi cài đặt, khôi phục.
- `propagate(productUnitIds, sourceCompanyId)` — gọi SAU khi công ty nguồn ghi giá; tìm mọi công ty đang kế thừa các hàng đó
  (theo luật §1, `pcc.status = 3`) rồi chép.
- Giá trị chép (Q3), theo `product_unit_id`: 6 dòng `product_unit_prices` (`price`, `coefficient`, `sale_max_percent`, cờ sửa tay
  TMĐT) · dòng giá hiệu lực `product_expected_prices` của từng loại giá (thay toàn bộ: xoá dòng cũ của công ty kế thừa rồi chép) ·
  `ensureUnitSet` trước khi chép. **Không** chép `pcu.cost_price` / `buy_price` (Q7) và các cột chờ duyệt.
- Lịch sử: `ProductPriceHistoryService::snapshot` trước/sau + `logAction('inherit', …, 'Kế thừa từ <mã công ty>')` ở công ty kế thừa.
- Cùng transaction với lần ghi của nguồn ⇒ hai bên không lệch.

**Điểm gọi `propagate`** (giá nguồn THẬT SỰ áp — Q6):
| Đường ghi giá công ty nguồn | File |
|---|---|
| Cập nhật giá bán, nhánh không duyệt | `ProductPriceUpdateService` → `ProductPriceWriter` |
| Duyệt giá bán — dòng được duyệt | `ProductPriceApprovalService` |
| PTG áp giá (không duyệt / duyệt xong) | `PriceCalculateWriter` / `PriceCalculateFinalizer` |
| Cron áp giá hiệu lực + màn Nhật ký áp giá | `ExpectedPriceApplier` |
| Thêm / sửa / xoá giá hiệu lực ở nguồn | `ProductPriceWriter` (khối `product_expected_prices`) |
| Chuyển KD không tính giá ở nguồn (bộ giá 0) | `ProductLifecycleService::tradeWithoutPrice` |
Gửi duyệt (`ProductPriceApprovalSubmitter`) chỉ đặt cờ chờ ⇒ **không** đồng bộ. Cron áp giá hiệu lực chạy theo từng công ty:
dòng giá hiệu lực của công ty kế thừa là bản chép ⇒ phải **bỏ qua** công ty kế thừa khi áp, chỉ áp ở nguồn rồi `propagate`
(tránh áp 2 lần — *tự chốt T5*).

**Chặn ghi thẳng** ở công ty kế thừa: mọi đường trên gọi với công ty kế thừa + hàng kế thừa ⇒ 423 "Hàng kế thừa giá từ <công ty>,
không sửa giá ở công ty này" (G4 lưu, G5 duyệt, gửi duyệt, PTG). Kiểm test `PriceReaderWhitelistTest` / danh sách writer nếu có.

## 4. Hỏi giá hàng kế thừa — tách phiếu (Q8)

- YCHG vẫn lập ở công ty mình, chọn được hàng kế thừa **đang KD** (trạng thái 1 kế thừa không vào YCHG — dùng nút Chuyển KD).
- **Gửi**: `PriceAskingRequestWriter` tách dòng hàng kế thừa theo công ty nguồn ⇒ mỗi công ty nguồn 1 YCHG mới
  (`company_id` = công ty nguồn, `created_by` = người gửi, cột mới `origin_request_id` → phiếu gốc, `origin_company_id`). Phiếu gốc
  chỉ còn hàng tự tính giá; phiếu gốc toàn hàng kế thừa ⇒ phiếu gốc đóng với trạng thái "Đã chuyển công ty quản lý" (*tự chốt T6*),
  hiện link các phiếu tách. Gửi trong 1 transaction; một phiếu tách lỗi (nhóm chưa phân công XNK ở công ty nguồn — Q3 cũ) ⇒ không
  gửi gì, 422 nêu hãng + công ty.
- Phiếu tách chạy đúng luồng hiện có trong **công ty nguồn**: PTKD (1662) · XNK phân công của công ty nguồn (1663) · KTMH (1664) ·
  quy chế duyệt giá công ty nguồn. Hàng ở công ty nguồn đang KD ⇒ giữ trạng thái (Q15 cũ); nguồn khoá ⇒ chặn lúc Gửi (Q9).
- Giá áp ở công ty nguồn ⇒ `propagate` (§3) ⇒ mọi công ty kế thừa, kể cả công ty người hỏi.
- Người lập phiếu (khác công ty): **xem** phiếu tách + kết quả nhóm, **nhận** thông báo "giá đã áp" / "từ chối" (link về phiếu tách).
  Không thao tác duyệt. Đây là ngoại lệ duy nhất của "chỉ thấy công ty mình" — `PriceAskingAccess` cho phép theo `created_by`.
- Thông báo PTKD / XNK / KTMH: người của công ty nguồn (lọc theo công ty phiếu — đúng Q16 cũ vì phiếu tách thuộc công ty nguồn).

## 5. Màn hiện có

| Màn | Thay đổi |
|---|---|
| Cập nhật giá bán (G4) | Hàng kế thừa vẫn hiện; nhãn "Kế thừa · <mã công ty>" ở dòng; mọi ô khoá (kể cả giá vốn — Q7 ngoài phạm vi), không chọn được để Lưu; ô lọc "Nguồn giá: Tự xây dựng / Kế thừa" (*tự chốt T7*) |
| Duyệt giá bán (G5) | Không phát sinh yêu cầu cho hàng kế thừa ở công ty kế thừa |
| Hàng hoá nhập thông tin / Dữ liệu công ty / chi tiết | Nút "Chuyển kinh doanh (kế thừa giá)"; ẩn nút không tính giá + YCHG với hàng kế thừa trạng thái 1; cờ BE `can_trade_inherited` |
| YCHG | Cột/nhãn "Gửi công ty quản lý" ở dòng hàng kế thừa trước khi gửi; phiếu tách hiện ở danh sách của người lập (lọc "Phiếu tôi lập") |
| Popup chọn hàng / báo giá | Không đổi (đọc giá công ty đang làm — đã là bản chép) |
| ERP | Không đổi: ERP đọc giá theo công ty (G3) ⇒ đọc bản chép |

## 6. Điểm tự chốt — user soát

- **T1** Hàng không có hãng ⇒ luôn tự tính giá.
- **T2** Nút Chuyển KD kế thừa bỏ qua mã mà công ty nguồn đã khoá.
- **T3** Đổi sang kế thừa ⇒ huỷ yêu cầu Duyệt giá đang chờ của dòng bị ghi đè.
- **T4** Khôi phục hàng kế thừa đang khoá ⇒ chép giá nguồn trước khi về Đang KD.
- **T5** Cron giá hiệu lực bỏ qua công ty kế thừa, chỉ áp ở nguồn rồi đồng bộ.
- **T6** Phiếu gốc toàn hàng kế thừa ⇒ đóng "Đã chuyển công ty quản lý" + link phiếu tách.
- **T7** Màn Cập nhật giá khoá cả giá vốn của hàng kế thừa (giá vốn chờ luồng riêng — Q7) + thêm ô lọc nguồn giá.
- Không gửi thông báo cho công ty kế thừa khi giá đổi theo nguồn (chỉ ghi lịch sử).

## 7. Đợt con dự kiến

| Đợt | Nội dung |
|---|---|
| K0 | Mockup màn Giá bán theo hãng sx + popup xác nhận đổi cài đặt + nhãn kế thừa ở G4 / YCHG — ✅ dựng 24/10 `mockup-ke-thua-gia.html` (DOM + CSS thật, ảnh `anh-mockup/m1…m8`, điểm UI tự chốt U1–U11 ở đầu file) — chờ user duyệt |
| K1 | CSDL (2 bảng + 2 cột YCHG) + quyền + màn cài đặt + lịch sử + luật "hàng kế thừa" |
| K2 | `InheritedPriceSync` + gắn 6 điểm gọi + chặn ghi ở công ty kế thừa + cron + đổi cài đặt (đo khối lượng) |
| K3 | Nút Chuyển KD kế thừa + ẩn nút cũ + khôi phục (T4) |
| K4 | Tách YCHG khi Gửi + quyền xem / thông báo người lập khác công ty |
| K5 | Màn G4 khoá dòng + lọc; nghiệm thu PHPUnit giá + e2e giá / hàng hoá / tính giá |

## 8. Kiểm

- PHPUnit: luật kế thừa (2 chế độ × trong/ngoài danh sách × hàng tự tạo × không hãng) · copy đủ 6 giá + ĐMGG + giá hiệu lực, giữ
  giá vốn · propagate ở 6 điểm gọi, không ở gửi duyệt · chặn 423 ở công ty kế thừa · đổi cài đặt (ghi đè / giữ / chặn 2-5) · cron
  không áp 2 lần · tách YCHG (lẫn hàng, nhiều nguồn, toàn kế thừa, nguồn chưa phân công XNK, nguồn khoá) · quyền mới có / không.
- Playwright MCP đo DOM: màn cài đặt (2 chế độ, popup chọn hãng, xác nhận, lịch sử), G4 khoá dòng, nút Chuyển KD kế thừa, YCHG tách.
- e2e: spec mới màn cài đặt + luồng kế thừa (có / không quyền); chạy khi user yêu cầu.
