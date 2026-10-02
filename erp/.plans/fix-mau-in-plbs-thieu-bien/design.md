# Fix mẫu in "Phụ lục bổ sung hợp đồng bán tổ chức" mất biến

> @junfoke · Repo `TanPhatDev`, nhánh `master` · Báo lỗi: QA, mẫu in id 97 (`PLBSHDBTC`)
> URL gặp lỗi: `https://erp.eteksofts.com/admin/report_templates/97/edit`

## Hiện tượng QA báo

Bản in phụ lục bổ sung (phát sinh tăng giá trị hợp đồng):

1. `{{SO_PHU_LUC}}`, `{{NGAY}}`, `{{THANG}}`, `{{NAM}}`, `{{NGAY_KY_HOP_DONG}}` → in ra **trống**.
2. `{{SO_HOP_DONG}}` → in ra **mã phụ lục** (`..._-PL`), đúng ra phải là mã hợp đồng gốc.

## Nguyên nhân

Phụ lục bổ sung là 1 bản ghi `firm_contracts` (type 2 / 5), in qua
`FirmContractController@print` → `FirmContractPrint::handlePrint()`.

- `handlePrint()` **không set** 5 biến ở mục 1 ⇒ `clearNull()` xoá sạch `{{...}}` ⇒ in trống.
- `handlePrint()` gán `SO_HOP_DONG = $contract->code`, mà `$contract` ở đây chính là bản ghi
  phụ lục (code có hậu tố `-PL`) ⇒ ra số phụ lục.
- Quy ước đúng đã tồn tại sẵn trong cùng file, ở `getPrintProductData()` (dòng 723-724):
  `SO_PHU_LUC` = mã bản ghi, `SO_HOP_DONG` = mã HĐ cha. Chỉ thiếu ở `handlePrint()`.

Tái hiện trên DB local `erp_dev_30_01_26` (firm_contract id 329, type 2):

```
MISSING: SO_PHU_LUC, NGAY, THANG, NAM, NGAY_KY_HOP_DONG, CHI_TIET, SO_BAN_IN...
SO_HOP_DONG => HĐ_TPSG_KV4_25_0002_040820225-PL   ← mã phụ lục
```

## Bẫy: KHÔNG được đổi `SO_HOP_DONG` cho mọi loại phụ lục

| Loại | type | Mẫu in dùng | Ý nghĩa `{{SO_HOP_DONG}}` |
| --- | --- | --- | --- |
| PL bổ sung HĐ hàng hoá | 2 | 97 `PLBSHDBTC` | **mã HĐ gốc** (cần sửa) |
| PL bổ sung HĐ dự án | 5 | 97 | **mã HĐ gốc** (cần sửa) |
| PL giảm (3/6/10) | 3,6,10 | 96 `PLHDBTC` | **mã phụ lục** — mẫu có `{{SO_HOP_DONG_GOC}}` riêng ⇒ GIỮ NGUYÊN |
| PL bổ sung HĐ nguyên tắc | 9 | mẫu riêng, in `(Số: {{SO_HOP_DONG}})` = số của chính nó ⇒ GIỮ NGUYÊN |

Đối chiếu 48 bản ghi phụ lục trên DB local: type 2 & 5 dùng `SO_PHU_LUC`, không dùng
`SO_HOP_DONG_GOC`; type 3/6/10 thì ngược lại — khớp bảng trên.

⇒ Chỉ ghi đè `SO_HOP_DONG` cho **type 2 và 5**.

## Quyết định đã chốt (user, 14/09/2026)

- **Ngày/tháng/năm/ngày ký**: bảng `firm_contracts` không có cột "ngày ký" riêng, không rõ lấy
  nguồn nào cho đúng ⇒ **in dấu chấm để người in tự điền** (giống dòng "Hôm nay, ngày …… tháng ……
  năm ……" vốn có sẵn trong mẫu), KHÔNG lấy `approved_time`.
- **`{{CHI_TIET}}`**: mẫu 97 trên prod chỉ dùng `{{CHI_TIET_HOP_DONG}}` (đã chạy đúng) ⇒
  **không đụng tới**, không thêm alias.
- `SO_PHU_LUC` set cho mọi phụ lục (mẫu 96 không dùng biến này nên vô hại).
