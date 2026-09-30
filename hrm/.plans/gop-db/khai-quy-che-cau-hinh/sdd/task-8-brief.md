# Task 8 brief

## Task 8: FE — nối tab Công nợ với API (thay mock)

**Files:**
- Modify: `pages/master-data/regulation-config/index.vue`
- Modify: `pages/master-data/regulation-config/data.js` (chỉ đánh dấu congno "nạp từ API", giữ tab khác)

**Interfaces:**
- Consumes: API Task 6 (`master-data/regulation-config/congno`, `.../versions`).
- Produces: tab `congno` hiển thị dữ liệu thật; `saveVer()` gọi POST/PUT; nút Huỷ gọi DELETE; sau mỗi thao tác reload config.

Toàn bộ code FE dưới đây là chỉ dẫn — implementer đọc `index.vue` hiện tại để chèn đúng chỗ (methods bắt đầu ~dòng 831). Chỉ đụng đường đi dữ liệu của tab `congno` (`groupIdx` trỏ group id `'congno'`), KHÔNG refactor các tab khác. Giữ nguyên CRLF/LF của file.

- [ ] **Step 1: Thêm state + company hiện tại**

Trong `data()` thêm:
```js
congnoLoading: false,
congnoApi: null,   // { fields, applied_version, pending } từ BE; null = chưa nạp
```
Xác định `companyId` hiện tại: dùng biến company của user đăng nhập (grep trong dự án cách lấy `company_id` hiện hành — vd `this.$store.state.auth.user.company_id` hoặc getter tương tự; nếu màn có chọn công ty thì lấy từ selector). Ghi cách lấy vào design.md.

- [ ] **Step 2: Hàm nạp config congno từ API**

```js
async fetchCongno() {
    if (!this.companyId) return
    this.congnoLoading = true
    try {
        const res = await this.$store.dispatch(
            'apiGetMethod',
            `master-data/regulation-config/congno?company_id=${this.companyId}`
        )
        this.congnoApi = res.data          // {fields, applied_version, pending}
        this.applyCongnoToModel()          // đổ vào this.model.company.groups[congno]
    } catch (e) {
        this.$toasted?.global?.error?.({ message: 'Lỗi khi tải cấu hình Công nợ' })
    } finally {
        this.congnoLoading = false
    }
}
```

`applyCongnoToModel()` map `congnoApi` → group `congno` trong `this.model.company.groups`:
- `group.eff` = `applied_version?.effective_date` (nếu null → giữ nhãn "Bản gốc": set cờ `group.isOriginal = !applied_version`).
- `group.pending` = `congnoApi.pending.map(p => ({ id:p.id, date:p.effective_date, who:p.created_by_name, note:p.note, changes:p.diff_snapshot.map(d=>({label:d.label, old:d.old, new:d.new, unit:d.unit})) }))`.
- `group.fields` số (7 field) = set `val` từ `congnoApi.fields` theo `key`. Giữ field mock `Ngày khai báo công nợ đầu kỳ` (fixed) + `Thuế vận tải` như hiện tại (ngoài scope).

- [ ] **Step 3: Gọi `fetchCongno()` khi mở tab congno**

Trong `mounted()` (hoặc watch `groupIdx`/`scope`): nếu `curGroup.id === 'congno'` và `scope==='company'` và chưa nạp → `this.fetchCongno()`.

- [ ] **Step 4: Wire `saveVer()` (POST tạo / PUT sửa)**

Thay thân `saveVer()` (đang chỉ `close()`):
```js
async saveVer() {
    if (this.verGroup?.id !== 'congno') { this.$refs.verModal.close(); return } // tab khác giữ mock
    const values = this.collectCongnoValues()      // {7 key: number} từ verForm.values
    const payload = {
        company_id: this.companyId,
        effective_date: this.verForm.date,          // 'YYYY-MM-DD'
        note: this.verForm.note || null,
        values,
    }
    try {
        if (this.verEditing && this.verForm.id) {
            await this.$store.dispatch('apiPutMethod', {
                url: `master-data/regulation-config/congno/versions/${this.verForm.id}`,
                payload,
            })
        } else {
            await this.$store.dispatch('apiPostMethod', {
                url: 'master-data/regulation-config/congno/versions',
                payload,
            })
        }
        this.$toasted?.global?.success?.({ message: 'Đã lưu phiên bản' })
        this.$refs.verModal.close()
        await this.fetchCongno()
    } catch (e) {
        const msg = e?.response?.data?.meta?.message || 'Lỗi khi lưu phiên bản'
        this.$toasted?.global?.error?.({ message: msg })
    }
}
```
`collectCongnoValues()` map từ `verForm.values` (label → value) về 7 key BE, dùng metadata key. Khi mở modal sửa (`openVer(group, pIdx)`) nạp `verForm.id = group.pending[pIdx].id`.

- [ ] **Step 5: Wire nút Huỷ lịch hẹn (DELETE)**

Gắn handler cho nút `.iconbtn.danger` trong `.vq-act` (hiện chưa có `@click`):
```js
async cancelPending(pending) {
    if (this.curGroup?.id !== 'congno') return
    if (!confirm('Huỷ lịch hẹn phiên bản này?')) return
    try {
        await this.$store.dispatch('apiDelete', `master-data/regulation-config/congno/versions/${pending.id}`)
        this.$toasted?.global?.success?.({ message: 'Đã huỷ lịch hẹn' })
        await this.fetchCongno()
    } catch (e) {
        this.$toasted?.global?.error?.({ message: 'Lỗi khi huỷ lịch hẹn' })
    }
}
```
Template: `@click="cancelPending(p)"` (với `p` là item trong `v-for` pending).

- [ ] **Step 6: Kiểm thủ công trên trình duyệt**

Chạy FE (hoặc môi trường dev có sẵn), mở `/master-data/regulation-config`, tab "Công nợ & tài chính":
- Nạp đúng 7 field từ BE; nhãn "đang áp dụng" hoặc "Bản gốc".
- Hẹn phiên bản mới ngày tương lai → xuất hiện trong "chờ áp dụng" với diff đúng.
- Hẹn ngày = hôm nay → áp ngay, field cập nhật, biến mất khỏi hàng đợi.
- Sửa/Huỷ phiên bản pending hoạt động, hàng đợi cập nhật.
Expected: khớp; số tiền format `,` nghìn (V2BaseCurrencyInput), ngày `DD/MM/YYYY`.

- [ ] **Step 7: Commit**

```bash
git add pages/master-data/regulation-config/index.vue pages/master-data/regulation-config/data.js
git commit -m "feat(regulation-config): wire congno tab to real versioning API"
```

---

