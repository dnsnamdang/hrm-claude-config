### Task 6: Đối chiếu baseline + đổi selector e2e

**Files:**
- Modify: `HRM/e2e/tests/assign/potential-customer-care.spec.ts` (106 chỗ `care-drill-*`)

**Interfaces:**
- Consumes: `baseline.json` (Task 1), `/tmp/after.json` (Task 5).

- [ ] **Step 1: So baseline với sau khi chuyển**

```bash
cd HRM && python3 - <<'PY'
import json
a = json.load(open('.plans/base-popup-bao-cao/baseline.json'))
b = json.load(open('/tmp/after.json'))
lech = []
for k in ['cols', 'firstPageRowCount', 'sttFirst', 'sttLast', 'pageTotal', 'sortTextAsc', 'sortDateAsc']:
    if a.get(k) != b.get(k):
        lech.append(f'{k}:\n  trước = {a.get(k)}\n  sau   = {b.get(k)}')
# Toạ độ đo theo pixel: cho sai số 2px, nhưng LUẬT thì phải giữ
if b['tableBottom'] > b['footerTop'] + 1:
    lech.append(f"bảng chạy xuyên hàng nút: đáy bảng {b['tableBottom']} > đỉnh nút {b['footerTop']}")
if not (b['heightFull'] > b['heightNormal']):
    lech.append('nút phóng to không còn tác dụng')
print('KHỚP HẾT' if not lech else 'LỆCH:\n' + '\n'.join(lech))
PY
```

Expected: `KHỚP HẾT`. Lệch chỗ nào thì quay lại Task 5 sửa **đúng chỗ đó**, không sửa baseline.

- [ ] **Step 2: Đổi selector trong spec**

```bash
cd HRM/e2e && python3 - <<'PY'
import io
p = 'tests/assign/potential-customer-care.spec.ts'
s = io.open(p, encoding='utf-8', newline='').read()
truoc = s.count('care-drill')
s = s.replace('care-drill', 'report-drill')
io.open(p, 'w', encoding='utf-8', newline='').write(s)
print('đã đổi', truoc, 'chỗ')
PY
```

Expected: `đã đổi 106 chỗ`.

- [ ] **Step 3: Rà lại các chỗ đổi không phải lớp CSS của Base**

```bash
cd HRM/e2e && grep -n "report-drill" tests/assign/potential-customer-care.spec.ts | grep -vE "report-drill-(table|head|sort|count|filters|dialog|content|paging|sum|customer|meeting|footer|wrap|scroll|back|sub)" | head
```

Expected: không còn dòng nào — nếu còn, đó là lớp riêng của màn bị đổi nhầm, phải trả về `care-drill-*`.

- [ ] **Step 4: Kiểm spec vẫn biên dịch**

```bash
cd HRM/e2e && PATH="$HOME/.nvm/versions/node/v20.20.1/bin:$PATH" \
  npx playwright test tests/assign/potential-customer-care.spec.ts --list --no-deps 2>&1 | tail -3
```

Expected: `Total: 29 tests in 1 file`.

- [ ] **Step 5: Commit**

```bash
git add tests/assign/potential-customer-care.spec.ts
git commit -m "test(cskh): đổi selector popup sang tiền tố report-drill-* của Base"
```

---

