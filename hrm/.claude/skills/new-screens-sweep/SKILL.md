---
name: new-screens-sweep
description: Use when phải RÀ / SỬA ĐỒNG LOẠT nhiều màn theo 1 quy tắc chung mới (task kiểu "tất cả màn danh sách…", "các màn mới phải…", "check lại các màn mới", "sửa lại cho đúng toàn bộ màn", "áp dụng cho mọi màn"), hoặc khi cần biết màn nào là màn MỚI (dùng V2Base — phần dự án + chuyển đổi ERP→HRM) để không sót. Có script kiểm kê inventory.py ra checklist + lệnh tự verify.
---

# Rà / sửa đồng loạt các màn MỚI — không sót, sửa nhanh

Lý do có skill này: các lần trước sửa theo quy tắc chung **hay bị sót** vì phạm vi bị đoán theo tên phân hệ
hoặc theo trí nhớ. Từ giờ phạm vi **chỉ lấy từ script**, việc kiểm "đã sửa xong chưa" **cũng giao cho script** —
không dùng mắt để đếm.

## 1. Định nghĩa "màn mới" (chốt 2026-10-03)

**Màn MỚI = file `.vue` trong `pages/` hoặc `components/` có dùng `<V2Base*>`.** Phần dự án và các màn chuyển
đổi ERP→HRM đều dựng trên V2Base, màn cũ thì không. KHÔNG suy theo thư mục: `human/banks`, `human/provinces`,
`timesheet/timeworking/shift-history`, `meeting/*`, `lookup/*` là màn mới dù nằm trong phân hệ cũ.

Script phân loại mỗi file (1 file có thể thuộc nhiều loại):

| Loại | Dấu hiệu | Là gì |
|---|---|---|
| `list` | có `<V2BaseDataTable>` | màn danh sách, **tab** danh sách, **popup** chọn có bảng |
| `table` | có V2Base nhưng bảng tự viết `<table>`/`<b-table>` | **VÙNG XÁM**: bảng con trong form, popup chọn phiếu |
| `form` | có ô nhập V2Base | form thêm/sửa, popup nhập liệu |
| `modal` | `<V2BaseModal>` / `<b-modal>` | popup |
| `print` | `print.vue` | màn in |
| `other` | còn lại | chi tiết, dashboard… |

4 chỗ trước đây hay sót, script đã tự bắt:
1. Màn mới nằm trong phân hệ cũ (xem trên).
2. **Tab và popup** có bảng (`TasksTab`, `IssueTab`, `*SearchModal`…), không chỉ `index.vue`.
3. **Component dùng chung trong `components/`** (`components/assign/task/TaskListTab.vue`,
   `components/finance/declare-debt/DeclareDebtList.vue`…). Script in kèm route của các màn đang dùng nó.
4. Trang cha không chứa V2Base nhưng component con thì có → script bắt theo component con.

Script **bỏ qua chính các component nền `components/V2Base*.vue`**. Đó là GỐC: nếu cần sửa thì sửa riêng
(bước 1 dưới đây) và phải hỏi trước, vì đây là hàm dùng chung.

## 2. Script `inventory.py`

```bash
S=.claude/skills/new-screens-sweep/inventory.py     # chạy từ HRM/ hoặc bất kỳ thư mục con nào
python3 $S --kind list                               # toàn bộ màn danh sách mới
python3 $S --kind list --has "REGEX"                 # PHẠM VI: màn mới có dính thứ cần sửa
python3 $S --kind list --has "REGEX" --lacks "REGEX_ĐÚNG"      # VERIFY: còn file nào chưa sửa
python3 $S --kind list --order "REGEX_A;;REGEX_B"    # VERIFY thứ tự: file có B đứng TRƯỚC A
python3 $S --kind list --be                          # kèm Controller BE (dò Routes/*.php)
python3 $S ... --format checklist                    # dạng - [ ] để dán vào plan.md
python3 $S ... --format paths                        # chỉ đường dẫn (giao cho subagent / xargs)
python3 $S --root worktrees/gop_db-client ...        # quét worktree khác (hoặc đặt HRM_CLIENT=...)
```

- `--module "finance|assign"`: lọc theo regex trên đường dẫn. `--include-old`: tính cả màn cũ (chỉ dùng khi task yêu cầu rõ).
- Mỗi dòng in ra: loại · route để mở bằng Playwright · màn cha đang dùng (với tab/modal/component) · API · Controller BE nếu có `--be`.
- `--be` chỉ là **gợi ý** (dò tĩnh theo `prefix` của group route). Đừng dùng `php artisan route:list`: chỉ cần 1 controller bị thiếu là cả lệnh sập (nhánh `develop` đang dính `DecisionController`).
- Chạy hết toàn bộ repo mất dưới 1 giây, nên cứ chạy lại thoải mái.

## 3. Quy trình (theo đúng thứ tự)

### Bước 1. Tách yêu cầu: sửa ở GỐC được không?
Với từng gạch đầu dòng của task, hỏi trước: có 1 chỗ sửa mà mọi màn tự đúng theo không?

| Loại yêu cầu | Gốc để sửa |
|---|---|
| Định dạng tên người (người tạo/cập nhật, select nhân viên) | BE helper `app/Helper/FormatHelper.php` + accessor/Resource trả `*_name`; FE `utils/employeeOptionText.js` |
| Chữ/màu badge, câu lỗi validate | BE Resource `status_text/status_color`; lang file `resources/lang/vi/validation.php`, `locales/vi.json` |
| Hành vi chung của bảng/ô nhập/nút | component `components/V2Base*.vue` |
| Độ dài tối đa, rule validate | FormRequest (BE) + `v-validate` trên V2Base (FE) |

- Sửa được ở gốc thì **sửa gốc trước**. Đụng hàm/component dùng chung thì **phải hỏi trước** (CLAUDE.md).
- Phần còn lại mới là việc phải sửa **từng màn**: đi tiếp bước 2.

### Bước 2. Lập phạm vi bằng script, ghi vào plan.md
- Với mỗi yêu cầu phải sửa từng màn, chọn `--kind` + `--has` cho đúng. **Ghi nguyên văn lệnh đã chạy vào plan.md**, kèm checklist `--format checklist`.
- Có file loại `table` (vùng xám) và chưa có quyết định ở mục 5: **hỏi user 1 lần** (liệt kê vài file mẫu), chốt xong thì ghi vào mục 5 của skill này.
- Kiểm kê từ nhánh/worktree đang sửa, không từ thư mục khác (dùng `--root`).

### Bước 3. Viết regex "ĐÃ ĐÚNG" cho từng yêu cầu, TRƯỚC khi sửa
- Mỗi yêu cầu cần 1 lệnh verify: `--lacks "<dấu hiệu đúng>"` hoặc `--order "A;;B"`. Chạy ngay để biết **còn bao nhiêu file sai**. Con số này là mốc để báo cáo.
- Regex phải bám đúng ngữ cảnh: vd `created_by_name` có thể chỉ xuất hiện ở bộ lọc chứ không ở khai báo cột → khớp theo `key: 'created_by_name'` / `title: 'Người tạo'`.
- Yêu cầu nào không viết được regex thì ghi rõ "kiểm tay" trong plan.md, kèm danh sách file.

### Bước 4. Sửa: 1 màn mẫu trước, rồi chia lô
1. Sửa **1 màn mẫu** thật chuẩn và lấy diff của nó làm khuôn.
2. Trên ~15 file thì chia theo phân hệ cho **subagent chạy song song** (mặc định ≤ 10 agent, mỗi agent ~10–20 file). Prompt cho mỗi agent phải có: quy tắc · diff màn mẫu · danh sách file (`--format paths`) · lệnh verify. Agent **không được sửa file ngoài danh sách**, và gặp trường hợp lạ thì ghi lại chứ không tự đoán.
3. Có phần BE thì chạy `--be` để ra danh sách Controller, từ đó lần sang Resource/Service. Gom các Resource dùng chung để sửa 1 lần.

### Bước 5. Verify bằng script, không bằng mắt
- Chạy lại mọi lệnh `--lacks`/`--order` của bước 3: **phải RỖNG**. Còn file nào thì sửa tiếp hoặc ghi lý do bỏ qua.
- Chạy lại lệnh phạm vi ở bước 2 để bắt **màn mới phát sinh** trong lúc sửa (nhánh khác vừa merge vào).
- `php -l` các file PHP vừa sửa. FE thì xem lại diff (`git diff --stat`) xem có file ngoài phạm vi bị đụng không.
- Kiểm bằng Playwright: chỉ chạy khi user yêu cầu (memory). Route để mở đã có sẵn trong output của script.

### Bước 6. Báo cáo
- `Đã sửa X/Y file (phạm vi: <lệnh>)`. Lệnh verify đã rỗng. Danh sách file bỏ qua kèm lý do. Các quyết định vùng xám đã chốt.
- Đánh `[x]` trong plan.md.

## 4. Mẫu: task #11566 (người tạo/cập nhật + thứ tự cột + mã tối đa 50)

```bash
# a) định dạng "Tên NV_Mã phòng": sửa GỐC ở BE (helper + accessor *_name), không sửa từng màn FE
#    Lọc theo CẢ nhãn lẫn tên field — cột người tạo còn mang nhãn "Người lập/đề xuất/yêu cầu/gửi duyệt"
python3 $S --kind list --be --has "(title|label):\s*'Người (tạo|cập nhật|sửa|lập|gửi|đề xuất|yêu cầu)|key:\s*'(creator_name|created_by_name|createdByName|creator|updater_name|updated_by_name|updatedByName|creatorName|updaterName|createdName|editor_name)'"
# b) thứ tự cột: chỉ áp cho màn KHÔNG có tuỳ chỉnh cột
python3 $S --kind list --lacks "column-customizations" \
  --order "title:\s*'Người tạo';;title:\s*'(Người cập nhật|Người sửa)'"
# c) mã tối đa 50: form mới có ô nhập mã (v-model *.code) nhưng chưa khai max ở FE
python3 $S --kind form --has 'v-model="[\w.]*\.code"' --lacks "max:\s*\d+|maxlength"
#    BE: rule 'max:50' cho 'code' ở FormRequest — grep Modules/*/Http/Requests theo Controller ra từ --be
```

⚠️ Bài học #11566 (lần chạy thật): lệnh phạm vi ban đầu chỉ lọc chữ "Người tạo|Người cập nhật" → **sót 7 màn**
có cột người tạo mang nhãn "Người lập" / "Người đề xuất" / "Người yêu cầu" (vd `finance/product-exports`).
**Luôn lọc theo cả TÊN FIELD, không chỉ nhãn hiển thị.** Quy tắc đã chốt: cột hiển thị created_by/updated_by của
chính bản ghi thì áp quy tắc, bất kể nhãn.

⚠️ Bài học khi viết regex: lần đầu (c) dùng `label="Mã…"` và ra **0 file**. Kết quả rỗng đó là do regex sai,
không phải code đã đúng hết, vì ô mã khai bằng `<V2BaseLabel>` + `v-model`. **Lệnh `--has` ra 0 file thì luôn nghi
regex trước**: mở 1 màn chắc chắn có thứ đó ra, đối chiếu lại rồi mới kết luận.

## 5. Quyết định phạm vi đã chốt
<!-- Ghi lại mỗi lần user chốt, để lần sau không hỏi lại. Định dạng: ngày · task · quyết định -->
- 2026-10-03 · Định nghĩa màn mới = có `<V2Base*>` (mục 1). Màn cũ không sửa, trừ khi task ghi rõ.
- 2026-10-03 · #11566 · Vùng xám `table`: **popup chọn phiếu có bảng = CÓ** sửa (cũng là danh sách); **bảng con trong form chi tiết = KHÔNG**.
- 2026-10-03 · #11566 · Tên người tạo/cập nhật hiển thị `Tên NV - Mã phòng` (ngăn cách ` - `, KHÔNG dùng `_` dù task ghi `Tên NV_Mã phòng`). Sửa thẳng accessor `BaseModel::employee_create_name/employee_update_name` (ảnh hưởng cả màn cũ — user đồng ý), helper `employeeAuditLabel()` trong `FormatHelper.php`.
- 2026-10-03 · #11566 · Mã tối đa 50: chỉ ô mã USER TỰ NHẬP (bỏ ô khoá/tự sinh), thêm cả FE (`max:50`) lẫn BE (`max:50` ở FormRequest), chỉ nơi chưa có giới hạn.
