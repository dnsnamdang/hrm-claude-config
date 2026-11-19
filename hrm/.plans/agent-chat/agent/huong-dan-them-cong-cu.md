# Hướng dẫn: thêm dữ liệu mới cho TPE SMART AGENT

> Viết 11/11/2026. Ví dụ ở mục 5 ĐÃ được làm thật (vai_tro=theo_doi) — xem code `ViecCuaToiTool.php` làm mẫu. Áp dụng cho module `Modules/Agent` (hrm-api) + `components/agent` (hrm-client),
> nhánh `gop_db-tpe-smart-agent`. Ví dụ xuyên suốt: cho Agent trả lời "Danh sách việc tôi đang theo dõi".

---

## 1. Nguyên lý — AI không có "file tri thức"

AI **không biết** DB hay API của mình. Mỗi câu hỏi, AI chỉ nhận:

1. **Luật chung** — `Modules/Agent/Services/AgentPrompt.php`
2. **Menu công cụ** — mỗi công cụ là 1 class trong `Modules/Agent/Tools/`, AI đọc tên + mô tả + tham số
3. **Câu hỏi** của nhân viên (+ ngữ cảnh: người hỏi, hôm nay, tối đa 3 lượt hỏi trước)

```
NV gõ câu hỏi
   │
   ▼
AgentRunner gửi Claude: [luật chung] + [menu công cụ] + câu hỏi
   │
   ▼
Claude đọc mô tả, chọn: gọi viec_cua_toi(overdue=true)
   │
   ▼
Code của mình: kiểm quyền → query DB → trả 2 phần
   ├─ data  → gửi lại Claude để viết câu dẫn ngắn
   └─ block → FE vẽ thẻ (danh sách / bảng / biểu đồ)
   │
   ▼
FE hiện: câu dẫn ≤ 3 câu + thẻ dữ liệu
```

- AI chỉ **chọn công cụ + viết câu dẫn**. Dữ liệu và quyền do **code của mình** quyết định ⇒ AI không lấy
  được gì ngoài thứ công cụ trả về, không lách được quyền.
- Có API HRM sẵn **không có nghĩa** Agent dùng được — phải bọc thành công cụ (hoặc thêm tham số vào công cụ có sẵn).
- Câu hỏi không khớp công cụ nào ⇒ Agent trả lời "chưa hỗ trợ" (luật 8) — đó là đúng thiết kế, không phải lỗi.

---

## 2. Các file liên quan

| # | File | Vai trò | Khi nào sửa |
|---|---|---|---|
| 1 | `hrm-api/Modules/Agent/Tools/<TenCongCu>Tool.php` | **Chính là "tri thức"** — 5 hàm, xem mục 3 | Luôn luôn |
| 2 | `hrm-api/Modules/Agent/Tools/AgentToolRegistry.php` | Danh sách công cụ đưa vào menu | Chỉ khi tạo công cụ MỚI (thêm 1 dòng `XxxTool::class`) |
| 3 | `hrm-client/components/agent/AgentResultBlock.vue` | Vẽ thẻ dữ liệu theo `block.type` | Chỉ khi cần kiểu thẻ mới. Đang có: `tasks`, `meetings`, `meeting`, `bars`, `rank`, `pick`, `rooms`, `bookings`, `timesheet`, `leave`, `requests`… |
| 4 | `hrm-api/Modules/Agent/Services/AgentPrompt.php` | Luật chung | Hiếm — chỉ khi mở phân hệ mới (đầu luật liệt kê "Công việc, Meeting, Chấm công, Lương") |
| 5 | `hrm-api/Modules/Agent/Tests/Feature/Tools/*Test.php` | Test công cụ (client giả, không tốn tiền) | Luôn luôn — có quyền + không quyền |
| 6 | `hrm-api/Modules/Agent/Tests/fixtures/eval/questions.json` | Bộ câu hỏi chấm AI có chọn đúng công cụ không | Luôn luôn — thêm 2–3 câu |

---

## 3. Một công cụ gồm 5 hàm (`AgentTool`)

| Hàm | Ý nghĩa | Lưu ý |
|---|---|---|
| `name()` | Tên công cụ, `snake_case` không dấu, vd `viec_cua_toi` | Không đổi tên công cụ đã chạy (eval + log dùng tên) |
| `definition()` | **Phần AI đọc**: mô tả + `input_schema` | Viết **tiếng Anh, gọn**; kèm 1–2 câu hỏi mẫu tiếng Việt trong ngoặc kép; phải có cụm **"Not for …"** (test kiểm); ≤ 600 ký tự (từ 12/11: mỗi ký tự trả tiền ở MỌI câu hỏi); KHÔNG liệt kê lại giá trị enum đã có trong schema, giá trị mặc định ghi ở mô tả tham số |
| `permissionNeed($input)` | Cần quyền gì; thiếu ⇒ bị chặn TRƯỚC khi chạy query | Trả `null` nếu service bên dưới đã tự lọc phạm vi xem |
| `run($input)` | Query DB (gọi lại service có sẵn), trả `ToolResult::ok($data, $soDong, $block)` | `$data` gửi AI, `$block` cho FE; AI không thấy khoá `link` |
| `matrixRow()` | Dòng ma trận quyền ở màn Thống kê | `['label' => '…', 'need' => null \| tên quyền]` |

**Mẫu mô tả tốt** (copy cấu trúc):

```
<Làm gì, nhấn mạnh CHỦ THỂ> ("câu hỏi mẫu 1", "câu hỏi mẫu 2").
Not for <trường hợp dễ nhầm> (<công cụ đúng>).
<tham số>: <ý nghĩa, định dạng, mặc định>.
Needs <quyền> , else denied.        ← nếu có
Returns <tổng số + tối đa N dòng gồm …>.
```

### Nguyên tắc an toàn (bắt buộc)

1. Công cụ "của tôi" **luôn lấy `auth()->id()`**, KHÔNG nhận id nhân viên từ AI.
2. Tham số có tập giá trị cố định ⇒ khai `enum`; code **tự map** sang bộ lọc thật; giá trị lạ ⇒ bỏ qua / dùng mặc định.
3. Xem dữ liệu người khác / phòng / công ty ⇒ phải có `permissionNeed()` hoặc dùng guard có sẵn
   (`TaskScopeGuard`, `TimesheetGuard`, `MeetingGuard`). Không tìm thấy và không đủ quyền phải trả **giống hệt nhau**
   (chống dò tồn tại).
4. Mỗi dòng trả AI phải có **mã hoặc id** nếu AI có thể cần gọi tiếp công cụ khác (bài học 11/11: `lich_meeting`
   chỉ có `link`, bỏ `link` ⇒ AI mất id để tra biên bản).
5. Lương / dữ liệu nhạy cảm: hỏi trước, không tự mở.

---

## 4. Hai cách mở rộng — chọn cách nào?

| Trường hợp | Cách | Ví dụ |
|---|---|---|
| Cùng loại dữ liệu, chỉ khác góc lọc | **Thêm tham số** vào công cụ có sẵn | Việc tôi theo dõi / tôi giao / tôi duyệt ⇒ `viec_cua_toi` thêm `vai_tro` |
| Loại dữ liệu khác hẳn | **Tạo công cụ mới** | Hợp đồng sắp hết hạn, công nợ khách hàng |

Ưu tiên thêm tham số: ít code, menu không dài thêm, AI ít nhầm giữa các công cụ na ná nhau.

---

## 5. Ví dụ từng bước: "Danh sách việc tôi đang theo dõi"

### Bước 0 — Kiểm dữ liệu + quyền (đọc code, chưa sửa)

- Bộ lọc có sẵn chưa? **Có**: `TaskService::index` nhận `watching_id`
  (`hrm-api/Modules/Assign/Services/TaskService.php` ~dòng 119). Cùng chỗ còn `created_by`, `approver_id`.
- Người theo dõi có được xem việc đó không? **Có**: phạm vi xem trong `TaskService` đã gồm vai trò theo dõi
  (`orWhereHas('watchers' …)` ~dòng 208) ⇒ không cần thêm kiểm quyền.
- Kết luận: cùng là "nhiệm vụ của tôi", khác vai trò ⇒ **thêm tham số `vai_tro` vào `viec_cua_toi`**.

### Bước 1 — `definition()` trong `Modules/Agent/Tools/ViecCuaToiTool.php`

```php
'description' => "List tasks of the ASKER by role: vai_tro=lam (assignee, default - \"việc của tôi\"), "
    . "theo_doi (watcher - \"việc tôi theo dõi\"). Not for other people ... (giữ phần còn lại)",
'input_schema' => [
    'type' => 'object',
    'properties' => [
        'vai_tro' => ['type' => 'string', 'enum' => ['lam', 'theo_doi'], 'description' => 'Asker role, default lam'],
        // overdue, deadline_from, deadline_to, status: giữ nguyên
    ],
],
```

### Bước 2 — `run()`

```php
const ROLE_FILTER = ['lam' => 'assignee_id', 'theo_doi' => 'watching_id'];

public function run(array $input): ToolResult
{
    // Giá trị lạ / không gửi ⇒ 'lam'
    $role = isset(self::ROLE_FILTER[$input['vai_tro'] ?? '']) ? $input['vai_tro'] : 'lam';
    // Người được lọc LUÔN là người hỏi — không nhận id từ AI
    $filters = [self::ROLE_FILTER[$role] => auth()->id()];
    // ... overdue / deadline / status giữ nguyên ...

    [$total, $rows] = TaskQuery::fetch(TaskQuery::visible($filters));
    $name = optional(auth()->user()->info)->fullname;
    $label = $role === 'theo_doi' ? 'việc ' . $name . ' theo dõi' : 'việc của ' . $name;

    return ToolResult::ok(
        ['total' => $total, 'tasks' => $rows],
        count($rows),
        ['type' => 'tasks', 'items' => $rows, 'source' => 'Nhiệm vụ · phạm vi: ' . $label]
    );
}
```

### Bước 3 — Những thứ KHÔNG phải sửa trong ví dụ này

- `AgentToolRegistry.php` — công cụ đã đăng ký.
- FE `AgentResultBlock.vue` — dùng lại thẻ `tasks`.
- `AgentPrompt.php` — vẫn phân hệ Công việc.
- `permissionNeed()` — giữ `null`.

### Bước 4 — Test (client giả, không tốn tiền)

Thêm vào `Modules/Agent/Tests/Feature/Tools/PersonalToolsTest.php` (mẫu: `test_viec_cua_toi_chi_tra_viec_minh_la_nguoi_lam`):

- `test_viec_cua_toi_theo_doi_chi_tra_viec_minh_theo_doi` — tạo 2 việc, NV theo dõi 1 việc ⇒
  `run(['vai_tro' => 'theo_doi'])` ra đúng 1 việc, không lẫn việc mình là người làm.
- `test_viec_cua_toi_vai_tro_la_bi_bo_qua` — `vai_tro = 'abc'` ⇒ kết quả giống `lam`.

```bash
cd wt-tpe-agent/hrm-api
AGENT_FAKE=1 /opt/homebrew/opt/php@8.1/bin/php -d memory_limit=2G vendor/bin/phpunit Modules/Agent/Tests
```

Phải xanh toàn bộ (hiện 129 test).

### Bước 5 — Đo AI có chọn đúng không (API thật, tốn tiền nhỏ)

1. Thêm 2–3 câu vào `Modules/Agent/Tests/fixtures/eval/questions.json`:
   ```json
   {"module": "Công việc", "question": "Danh sách nhiệm vụ tôi là người theo dõi",
    "as_employee_id": 13, "expect_tools": ["viec_cua_toi"], "expect_kind": "ok"}
   ```
2. Hỏi thử 1 câu, xem log có truyền `vai_tro=theo_doi` không (~10 ₫):
   ```bash
   php artisan agent:ask namdangit@gmail.com "Việc tôi đang theo dõi có gì quá hạn không?"
   ```
3. Chạy cả bộ (~800 ₫ với Haiku 5.5). Điểm các câu CŨ **không được tụt**:
   ```bash
   php artisan agent:eval
   ```
   Kết quả in bảng + ghi CSV ở `storage/app/agent-eval-*.csv`.

⚠️ Bộ eval chỉ chấm **tên công cụ** + **loại trả lời** (ok/deny/ask/na), CHƯA chấm tham số ⇒ bước 2 bắt buộc
nhìn tay. ⚠️ Không chạy `agent:eval` trên prod.

### Bước 6 — Kiểm trên giao diện

Mở `/agent`, hỏi "việc tôi đang theo dõi":

- Thẻ ghi "phạm vi: việc … theo dõi".
- Số dòng khớp màn Nhiệm vụ lọc theo người theo dõi.
- Câu dẫn ngắn, không chép lại danh sách.

Khối lượng: 1 file công cụ + 2 test + 2–3 câu eval, ~1–2 giờ.

---

## 6. Chi phí cần biết

- Menu công cụ gửi kèm **mọi** câu hỏi nhưng nằm trong cache: mỗi công cụ thêm ~300 token ≈ +0.05 ₫/câu (Haiku).
- Sửa mô tả công cụ / luật chung ⇒ câu đầu tiên sau đó ghi lại cache 1 lần (~30 ₫ với Haiku).
- Dữ liệu công cụ trả về là phần tốn nhất không đệm được ⇒ chỉ trả trường AI cần; đường dẫn cho FE để trong
  khoá `link` (tự bị bỏ khi gửi AI).
- Giữ tiếng Việt có dấu cho câu hỏi, dữ liệu DB và câu trả lời. Chỉ phần cố định (mô tả công cụ) viết tiếng Anh.
- Đo 11/11/2026 (Haiku 5.5, 88 câu): đúng công cụ 96.6%, đúng loại trả lời 98.9%, **≈ 8 ₫/câu**.

---

## 7. Checklist trước khi báo xong

- [ ] Mô tả tiếng Anh, có câu mẫu tiếng Việt, có "Not for", ≤ 600 ký tự, không lặp enum của schema
- [ ] Công cụ "của tôi" dùng `auth()->id()`, không nhận id từ AI
- [ ] Tham số cố định khai `enum`, giá trị lạ bị bỏ qua
- [ ] Xem dữ liệu người khác có kiểm quyền; không tìm thấy = không đủ quyền (trả giống hệt)
- [ ] Mỗi dòng có mã/id nếu AI cần gọi tiếp
- [ ] Test có quyền + không quyền, chạy xanh toàn bộ `Modules/Agent/Tests`
- [ ] Thêm câu eval, `agent:ask` nhìn tham số, `agent:eval` không tụt điểm câu cũ
- [ ] Kiểm trên `/agent`: thẻ đúng, số khớp màn gốc, câu dẫn ngắn
