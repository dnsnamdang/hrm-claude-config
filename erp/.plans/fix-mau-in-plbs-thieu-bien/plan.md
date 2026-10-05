# Plan — Fix mẫu in Phụ lục bổ sung HĐ bán tổ chức mất biến

@junfoke · Repo `TanPhatDev`, nhánh `master`

## Phase 1 — BE

- [x] Tái hiện lỗi trên DB local, xác định luồng in (`FirmContractController@print` → `FirmContractPrint::handlePrint`)
- [x] Xác định phạm vi an toàn: chỉ type 2 (PL bổ sung) và 5 (PL bổ sung HĐ dự án)
- [x] Bổ sung `SO_PHU_LUC` cho mọi phụ lục trong `handlePrint()`
- [x] Ghi đè `SO_HOP_DONG` = mã HĐ gốc cho type 2/5 (+ `SO_HOP_DONG_GOC` cho đồng bộ)
- [x] `NGAY` / `THANG` / `NAM` / `NGAY_KY_HOP_DONG` = dòng chấm để người in tự điền
- [x] `php -l` sạch, kiểm CRLF không đổi
- [x] Verify lại bằng script: không còn biến thiếu, `SO_HOP_DONG` ra mã HĐ gốc
- [ ] User test trên browser (in 1 phụ lục bổ sung thật)

## Không làm (đã chốt)

- KHÔNG thêm alias `{{CHI_TIET}}` — mẫu prod dùng `{{CHI_TIET_HOP_DONG}}`
- KHÔNG đổi `SO_HOP_DONG` cho PL giảm (type 3/6/10) và PL bổ sung HĐ nguyên tắc (type 9)

### Checkpoint — 14/09/2026
Vừa hoàn thành: sửa `app/Services/PrintTemplate/FirmContractPrint.php` (+15 dòng), verify bằng script tinker trên bản ghi type 2 id 329.
Đang làm dở: chưa commit, chờ user test browser.
Bước tiếp theo: user in thử 1 phụ lục bổ sung trên bản B local / prod staging → OK thì commit.
Blocked:
