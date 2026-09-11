/* ============================================================
   Phân quyền dạng MA TRẬN (đối tượng × hành động) — PHƯƠNG ÁN CHỐT
   6 cột: Đối tượng · Tất cả · Quản lý · Xem · Duyệt · Quyền khác
   - Phiếu CÁ NHÂN      : Xem · Duyệt · Quyền khác            (ô Quản lý = –)
   - Phiếu CHUNG/danh mục: Quản lý · Xem · Duyệt · Quyền khác
   Quyền Tạo/Sửa/Xóa rời trong CSDL được GOM vào ô Quản lý (1 ô = n quyền).
   Phạm vi xem nằm trong ô Xem (popup), KHÔNG có cột riêng.
   Dữ liệu là THẬT, trích từ PermissionsTableSeeder (nhánh gop_db).
   Tên phân hệ lấy đúng `label` trong hrm-client/components/subsystems.js — KHÔNG tự thêm tiền tố.
     Chấm công  78 quyền → 24 đối tượng
     Tính lương 57 quyền → 18 đối tượng
   ============================================================ */

var PM_LEVELS = ['Tổng công ty', 'Công ty', 'Phòng ban', 'Bộ phận'];
var PM_MY_COMPANY = 'Cty Tân Phát Hà Nội';
var PM_ROLE = 'Nhân viên chấm công';

/* Mỗi phân hệ một màu riêng — đủ 12 tông phân biệt được cho ERP.
   Mỗi tông gồm: nền nhạt (bg) · chữ đậm (fg) · vạch nhấn bên trái (ac). */
var PM_HUES = [
    { bg: '#e6f4ec', fg: '#14532d', ac: '#16a34a' },   /* xanh lá   */
    { bg: '#eaedfe', fg: '#312e81', ac: '#4f46e5' },   /* chàm      */
    { bg: '#fdf3e3', fg: '#92400e', ac: '#d97706' },   /* hổ phách  */
    { bg: '#e4f4fd', fg: '#075985', ac: '#0ea5e9' },   /* xanh trời */
    { bg: '#f2eafe', fg: '#5b21b6', ac: '#7c3aed' },   /* tím       */
    { bg: '#fdeaef', fg: '#9f1239', ac: '#e11d48' },   /* hồng đậm  */
    { bg: '#e2f6fa', fg: '#155e75', ac: '#0891b2' },   /* xanh ngọc */
    { bg: '#f1f7e2', fg: '#3f6212', ac: '#65a30d' }, /* xanh olive */
    { bg: '#fdeee4', fg: '#9a3412', ac: '#ea580c' },   /* cam       */
    { bg: '#fbeafc', fg: '#86198f', ac: '#c026d3' },   /* đỏ tía    */
    { bg: '#e7effd', fg: '#1e40af', ac: '#2563eb' },   /* xanh dương*/
    { bg: '#eef1f5', fg: '#334155', ac: '#64748b' }    /* xám xanh  */
];
function pmHue(si) { return PM_HUES[si % PM_HUES.length]; }

/* ── PHẠM VI QUYỀN DUYỆT ──────────────────────────────────────────────────────
   CHỐT: scope gắn theo QUYỀN (không theo cặp chức vụ × quyền). Cần phạm vi khác
   thì tạo QUYỀN RIÊNG (vd "BGĐ duyệt X"), không nới scope.
   Nguồn thật: `permission_scopes` (ERP config/approval_inbox.php) — bản thật phải khoá
   theo PERMISSION ID, không theo tên: đổi tên quyền là nó rơi khỏi map và âm thầm
   nới thành 'company' (fail-open, không có lỗi nào báo ra).
   Ở mockup mô phỏng bằng map tên → scope. */
var PM_AP_SCOPE = {
    department: { t: 'Phòng ban quản lý', d: 'Chỉ duyệt phiếu có department_id thuộc phòng user quản lý (employee_manage_departments)' },
    part: { t: 'Bộ phận quản lý', d: 'Chỉ duyệt phiếu có part_id thuộc bộ phận user quản lý' },
    company: { t: 'Toàn công ty', d: 'Duyệt mọi phiếu trong công ty của user' }
};

/* Đã KHAI BÁO tường minh — mô phỏng permission_scopes */
var PM_SCOPE_MAP = {
    'Trưởng phòng': 'department',
    'TP duyệt phiếu giao công việc': 'department',
    'TP duyệt kết quả công việc': 'department',
    'TP duyệt phiếu giao công tác': 'department',
    'TP duyệt kết quả công tác': 'department',
    'TP duyệt phiếu đề xuất công việc': 'department',
    'TP Duyệt đề nghị thanh toán': 'department',
    'TP duyệt quyết toán hợp đồng': 'department',
    'NSHC': 'company',
    'KT Duyệt đề nghị thanh toán': 'company',
    'KT duyệt quyết toán hợp đồng': 'company',
    'Ban giám đốc': 'company'
    /* Các quyền KHÔNG có ở đây → rơi vào mặc định 'company' và bị đánh dấu cảnh báo */
};
function pmApScope(st) { return PM_AP_SCOPE[st.scope] || PM_AP_SCOPE.company; }

/* Nhãn phạm vi duyệt (chỉ đọc). Chưa khai → viền đứt + dấu cảnh báo, để phân biệt
   "đã xác nhận là cấp công ty" với "chưa ai khai, đang ăn mặc định". */
function pmApScopeTag(st, extraCls) {
    var sc = pmApScope(st);
    var undecl = !st.scopeDeclared;
    return '<span class="pm-apscope pm-apscope--' + st.scope + (undecl ? ' pm-apscope--undecl' : '')
        + (extraCls || '') + '" title="' + sc.d
        + (undecl ? ' — ⚠ CHƯA khai trong permission_scopes, đang dùng mặc định' : '') + '">'
        + (undecl ? '<i class="ri-error-warning-line"></i> ' : '') + sc.t + '</span>';
}

var L4 = PM_LEVELS;
var L3 = ['Công ty', 'Phòng ban', 'Bộ phận'];
var L2 = ['Tổng công ty', 'Công ty'];

/* ---------- DỮ LIỆU THẬT ----------
   raw = số permission gốc trong seeder gộp vào dòng này
   view/manage/create/edit/del/approve = null ⇒ KHÔNG có quyền tương ứng ⇒ ô hiện "–" */
var PM_DATA = [
    {
        sub: 'Chấm công', open: true, groups: [
            {
                g: 'Chấm công', objs: [
                    { n: 'Bảng chấm công chi tiết', raw: 4, view: { lv: L4, def: 'Công ty' } },
                    { n: 'Bảng chấm công tổng hợp', raw: 2, view: { lv: ['Công ty'], def: '' } },
                    { n: 'Bảng chấm công tổng hợp trong tháng', raw: 3, view: { lv: L3, def: '' } },
                    { n: 'Dữ liệu chấm công', raw: 4, view: { lv: L4, def: 'Bộ phận' } }
                ]
            },
            {
                g: 'Ca làm việc', objs: [
                    { n: 'Ca làm việc', raw: 1, manage: { on: true } },
                    { n: 'Danh mục ca làm việc', raw: 2, view: { lv: L2, def: '' } },
                    /* "Phân ca theo công ty/phòng ban/bộ phận" — THAO TÁC có phạm vi (ca ngoại lệ) */
                    { n: 'Phân ca', raw: 3, manage: { on: true, lv: L3, def: 'Công ty' }, note: 'Thao tác có phạm vi' }
                ]
            },
            {
                g: 'Quản lý đơn', objs: [
                    { n: 'Đơn nghỉ phép', raw: 6, view: { lv: L4, def: 'Phòng ban' }, approve: { steps: [{ n: 'Trưởng phòng', on: true }, { n: 'NSHC', on: false }] } },
                    { n: 'Đơn đi muộn về sớm', raw: 5, view: { lv: L4, def: '' }, approve: { steps: [{ n: 'Trưởng phòng', on: false }] } },
                    { n: 'Đăng ký làm thêm', raw: 5, view: { lv: L4, def: '' }, approve: { steps: [{ n: 'Trưởng phòng', on: false }] } },
                    { n: 'Phân công làm thêm', raw: 5, view: { lv: L4, def: '' }, manage: { on: false } },
                    { n: 'Phiếu yêu cầu làm thêm', raw: 6, view: { lv: L4, def: '' }, manage: { on: false }, approve: { steps: [{ n: 'Trưởng phòng', on: false }] } },
                    { n: 'Đề nghị tra soát công', raw: 6, view: { lv: L4, def: '' }, approve: { steps: [{ n: 'Duyệt', on: false }, { n: 'Xác nhận', on: false }] } }
                ]
            },
            {
                g: 'Thiết lập', objs: [
                    { n: 'Thông số chấm công', raw: 1, manage: { on: false } },
                    { n: 'Thiết bị chấm công', raw: 1, approve: { steps: [{ n: 'Duyệt', on: false }] } }
                ]
            },
            {
                g: 'Dashboard', objs: [
                    { n: 'Dashboard nhân viên', raw: 1, view: { lv: [], def: '', on: true } },
                    { n: 'Dashboard quản lý', raw: 1, view: { lv: [], def: '' } },
                    { n: 'Dashboard trưởng phòng', raw: 1, view: { lv: [], def: '' } }
                ]
            },
            {
                g: 'Xem báo cáo', objs: [
                    { n: 'Báo cáo tổng hợp chấm công', raw: 4, view: { lv: L4, def: 'Phòng ban' } },
                    { n: 'Báo cáo tổng hợp đi giao việc/công tác', raw: 4, view: { lv: L4, def: '' } },
                    { n: 'Báo cáo làm thêm giờ', raw: 4, view: { lv: L4, def: '' } },
                    { n: 'Báo cáo làm thêm giờ chi tiết', raw: 4, view: { lv: L4, def: '' } },
                    { n: 'Báo cáo phép', raw: 4, view: { lv: L4, def: '' } }
                ]
            },
            {
                g: 'Phân quyền', objs: [
                    { n: 'Phân quyền', raw: 1, manage: { on: false } }
                ]
            }
        ]
    },
    {
        sub: 'Tính lương', open: true, groups: [
            {
                g: 'Thành phần lương', objs: [
                    { n: 'Mẫu bảng lương', raw: 4, view: { lv: [], def: '' }, create: false, edit: false, del: false },
                    { n: 'Lương P3 (Hoa hồng/lương khoán)', raw: 4, view: { lv: [], def: '' }, create: false, edit: false, del: false },
                    { n: 'Thu nhập khác', raw: 4, view: { lv: [], def: '' }, create: false, edit: false, del: false },
                    { n: 'Khấu trừ khác', raw: 4, view: { lv: [], def: '' }, create: false, edit: false, del: false },
                    { n: 'Các thành phần khác', raw: 4, view: { lv: [], def: '' }, create: false, edit: false, del: false },
                    { n: 'Thành phần lương', raw: 1, manage: { on: false } }
                ]
            },
            {
                g: 'Bảng lương', objs: [
                    { n: 'Bảng lương', raw: 3, view: { lv: L2, def: 'Công ty' }, manage: { on: false } },
                    { n: 'Bảng tổng hợp lương', raw: 4, view: { lv: [], def: '' }, create: false, edit: false, del: false },
                    { n: 'Bảng phân công lương', raw: 4, view: { lv: [], def: '' }, create: false, edit: false, del: false },
                    { n: 'Bảng chi trả lương', raw: 4, view: { lv: [], def: '' }, create: false, edit: false, del: false },
                    { n: 'Tạm ứng lương', raw: 4, view: { lv: [], def: '' }, create: false, edit: false, del: false },
                    { n: 'Bảng chấm công tổng hợp', raw: 1, view: { lv: [], def: '' } }
                ]
            },
            {
                g: 'Định biên', objs: [
                    { n: 'Cơ cấu định biên nhân sự', raw: 4, view: { lv: [], def: '' }, create: false, edit: false, del: false },
                    { n: 'Bảng nhân sự theo định biên', raw: 1, view: { lv: [], def: '' } },
                    { n: 'Bảng nhân sự và quỹ lương công ty', raw: 1, view: { lv: [], def: '' } }
                ]
            },
            {
                g: 'Chia thưởng & báo cáo', objs: [
                    { n: 'Bảng chia thưởng', raw: 5, view: { lv: ['Tổng công ty', 'Công ty', 'Phòng ban'], def: '' }, create: false, approve: { steps: [{ n: 'Ban giám đốc', on: false }] } },
                    { n: 'Báo cáo bảng chi trả', raw: 4, view: { lv: L4, def: '' } },
                    { n: 'Thông số lương', raw: 1, manage: { on: false } }
                ]
            }
        ]
    },
    {
        sub: 'Dự án & giao việc', open: true, groups: [
            {
                g: 'Quản lý phiếu giao việc', objs: [
                    {
                        n: 'Phiếu giao việc', raw: 9,
                        view: { lv: L4, def: 'Phòng ban' }, manage: { on: false },
                        approve: { steps: [{ n: 'TP duyệt phiếu giao công việc', on: false }, { n: 'TP duyệt kết quả công việc', on: false }] },
                        other: [{ n: 'Nhập kết quả công việc', on: true }]
                    },
                    {
                        n: 'Phiếu đề xuất công việc', raw: 6,
                        view: { lv: L4, def: '' },
                        approve: { steps: [{ n: 'TP duyệt phiếu đề xuất công việc', on: false }] },
                        other: [{ n: 'Trưởng phòng giao đi công tác', on: false }]
                    }
                ]
            },
            {
                g: 'Quản lý phiếu giao công tác', objs: [
                    {
                        n: 'Phiếu giao công tác', raw: 13,
                        view: { lv: L4, def: '' }, manage: { on: false },
                        approve: { steps: [{ n: 'TP duyệt phiếu giao công tác', on: false }, { n: 'TP duyệt kết quả công tác', on: false }, { n: 'Duyệt hồ sơ thanh toán', on: false }] },
                        other: [{ n: 'Nhập kết quả công tác', on: true }, { n: 'Gia hạn, kết thúc sớm phiếu công tác', on: false }, { n: 'Tạo hồ sơ thanh toán', on: false }]
                    }
                ]
            },
            {
                g: 'Thanh toán & quyết toán', objs: [
                    {
                        n: 'Đề nghị thanh toán', raw: 7,
                        view: { lv: L4, def: '' },
                        approve: { steps: [{ n: 'TP Duyệt đề nghị thanh toán', on: false }, { n: 'KT Duyệt đề nghị thanh toán', on: false }], parallel: true },
                        other: [{ n: 'Tạo đề nghị thanh toán phiếu công tác', on: false }]
                    },
                    {
                        n: 'Quyết toán hợp đồng', raw: 6,
                        view: { lv: L4, def: '' },
                        approve: { steps: [{ n: 'TP duyệt quyết toán hợp đồng', on: false }, { n: 'KT duyệt quyết toán hợp đồng', on: false }], parallel: true }
                    }
                ]
            }
        ]
    }
];

/* DEMO: đưa phân hệ / đối tượng CÓ "Quyền khác" lên đầu để nhìn thấy ngay, khỏi cuộn tìm.
   (chỉ là thứ tự trình bày của mockup; sort ổn định nên trong cùng hạng giữ nguyên thứ tự gốc) */
/* Chuẩn hoá: mọi trạng thái đã cấp đều nằm TRONG PM_DATA (nguồn sự thật duy nhất).
   Trước đây trạng thái nằm ở DOM → đổi bản / mở lại popup là mất. */
PM_DATA.forEach(function (sub) {
    sub.groups.forEach(function (g) {
        g.objs.forEach(function (o) {
            if (o.view && o.view.on === undefined) o.view.on = !!o.view.def;
            if (o.manage && o.manage.on === undefined) o.manage.on = false;
            /* Phạm vi của quyền DUYỆT là THUỘC TÍNH CỐ HỮU của chính quyền đó, KHÔNG cho admin chọn.
               Nguồn thật: ERP `config/approval_inbox.php` → `permission_scopes`
                 'department' → phiếu.department_id ∈ phòng user QUẢN LÝ (employee_manage_departments)
                 'part'       → phiếu.part_id ∈ bộ phận user quản lý
                 mặc định     → 'company'
               Map này phản chiếu gate hardcode trong controller ⇒ đổi ở đây mà không đổi gate là SAI. */
            if (o.approve) o.approve.steps.forEach(function (st) {
                st.scopeDeclared = Object.prototype.hasOwnProperty.call(PM_SCOPE_MAP, st.n);
                st.scope = st.scopeDeclared ? PM_SCOPE_MAP[st.n] : 'company';
            });
        });
    });
});

function pmOtherOf(o) { return (o.other || []).length; }
function pmSubOtherCount(sub) {
    return sub.groups.reduce(function (a, g) {
        return a + g.objs.reduce(function (b, o) { return b + (pmOtherOf(o) ? 1 : 0); }, 0);
    }, 0);
}
PM_DATA.forEach(function (sub) {
    sub.groups.forEach(function (g) {
        g.objs.sort(function (x, y) { return (pmOtherOf(y) ? 1 : 0) - (pmOtherOf(x) ? 1 : 0); });
    });
    sub.groups.sort(function (a, b) {
        var ca = a.objs.filter(pmOtherOf).length, cb = b.objs.filter(pmOtherOf).length;
        return (cb ? 1 : 0) - (ca ? 1 : 0);
    });
});
PM_DATA.sort(function (a, b) { return (pmSubOtherCount(b) ? 1 : 0) - (pmSubOtherCount(a) ? 1 : 0); });

/* ======================= STYLE ======================= */
function pmInjectStyle() {
    if (document.getElementById('pm-style')) return;
    var css = ''
        /* banner + công tắc bản A/C */
        + '.pm-banner{display:flex;align-items:center;gap:7px;padding-bottom:10px;margin-bottom:10px;border-bottom:1px solid #eef2f6;font-size:12.5px;color:#475569}'
        + '.pm-banner i{color:#16a34a;font-size:15px}'
        + '.pm-banner b{color:#0f172a}'
        /* bộ lọc 1 hàng */
        + '.pm-filter{display:flex;gap:10px;align-items:flex-end;flex-wrap:wrap}'
        + '.pm-ff{display:flex;flex-direction:column;gap:3px;flex:1;min-width:150px}'
        + '.pm-ff .tp-label{margin-bottom:0}.pm-ff .quick-search{margin-bottom:0}'
        + '.pm-bulkact{display:flex;gap:4px}'
        /* card phân hệ */
        + '.pm-chev{color:var(--c-ac);font-size:16px;transition:transform .18s}'
        + '.pm-sub__sp{flex:1}'
        + '.pm-scroll{overflow:visible}'
        + '@media(max-width:1199px){.pm-scroll{overflow-x:auto}}'
        /* bảng ma trận */
        + '.pm-tb{width:100%;border-collapse:separate;border-spacing:0;min-width:980px}'
        + '.pm-tb thead th{background:#eef2f6;color:#475569;font-size:10.5px;font-weight:800;text-transform:uppercase;letter-spacing:.03em;padding:8px 8px;border-bottom:1px solid #d8e0e8;border-right:1px solid #e5e7eb;text-align:center;position:sticky;top:var(--topbar-h);z-index:6;white-space:nowrap;box-shadow:0 1px 0 #d8e0e8}'
        + '.pm-tb thead th.l{text-align:left}'
        + '.pm-tb thead th.grpA{background:#e8f1ea}'
        + '.pm-tb thead th.grpB{background:#eef2f6}'
        + '.pm-tb thead th.grpC{background:#fdf3e7}'
        + '.pm-tb td{border-bottom:1px solid #eef2f6;border-right:1px solid #f1f5f9;padding:5px 8px;font-size:12.5px;color:#334155;text-align:center;vertical-align:middle}'
        + '.pm-tb td.l{text-align:left}'
        + '.pm-tb tbody tr.pm-obj:hover td{background:#f6fdf9}'
        /* cột đối tượng ghim trái */
        + '.pm-tb .c-obj{position:sticky;left:0;background:#fff;z-index:2;min-width:320px}'
        + '.pm-tb thead .c-obj{z-index:7}'
        + '.pm-tb tbody tr.pm-obj:hover .c-obj{background:#f6fdf9}'
        + '.pm-obj-nm{color:#334155;cursor:help}'
        /* dải nhóm */
        + '.pm-hidden{display:none}'
        + '.pm-filtered-out{display:none}'
        /* dải PHÂN HỆ — nền xanh, ghim ngay dưới hàng tiêu đề cột */
        + '.pm-srow td{background:var(--c-bg);border-top:1px solid rgba(0,0,0,.06);border-bottom:1px solid rgba(0,0,0,.06);border-left:4px solid var(--c-ac);padding:0;cursor:pointer;position:sticky;top:calc(var(--topbar-h) + var(--pm-thead-h, 33px));z-index:4}'
        + '.pm-srow td:hover{filter:brightness(.97)}'
        + '.pm-srow .in{display:flex;align-items:center;gap:9px;padding:9px 12px}'
        + '.pm-srow .nm{font-weight:800;color:var(--c-fg);font-size:13px}'
        + '.pm-srow .sp{flex:1}'
        + '.pm-secn{display:inline-flex;align-items:center;background:var(--c-ac);color:#fff;border-radius:999px;padding:2px 9px;font-size:10.5px;font-weight:700}'
        + '.pm-srow .ct{font-size:11px;color:var(--c-fg);opacity:.75;font-weight:600}'
        + '.pm-sec.collapsed .pm-chev{transform:rotate(-90deg)}'
        + '.pm-gsel{display:inline-flex;align-items:center;gap:6px;font-size:11px;color:#475569;font-weight:600;margin:0;cursor:pointer}'
        + '.pm-grow td{background:#dfe6ef;padding:0;border-right:0}'
        + '.pm-grow .in{display:flex;align-items:center;gap:8px;padding:7px 11px}'
        + '.pm-grow .nm{font-size:11.5px;font-weight:800;color:#334155;display:inline-flex;align-items:center;gap:6px}'
        + '.pm-grow .nm i{font-size:14px;color:#3f7f5f}'
        + '.pm-grow .sp{flex:1}'
        + '.pm-grow .ct{font-size:10.5px;color:#64748b;font-weight:600}'
        /* ô */
        + '.pm-na{color:#cbd5e1;font-size:13px;user-select:none}'
        + '.pm-ck{width:17px;height:17px;accent-color:#16a34a;cursor:pointer;vertical-align:middle}'
        + '.pm-ck--all{accent-color:#0ea5e9}'
        + '.pm-ck--bundle{accent-color:#7c3aed}'
        + '.pm-advbtn{border:1px dashed #d5dde5;background:#fff;border-radius:7px;font-size:11px;color:#94a3b8;padding:4px 9px;cursor:pointer;font-family:inherit;white-space:nowrap}'
        + '.pm-advbtn:hover{border-color:#94a3b8;color:#475569}'
        + '.pm-advbtn.on{border-style:solid;border-color:#86c9a4;background:#effaf3;color:#166534;font-weight:700}'
        + '.pm-note{display:inline-block;font-size:10px;color:#b45309;background:#fef3c7;border-radius:4px;padding:1px 5px;margin-left:6px}'
        /* thanh tổng hợp ghim đáy */
        + '.pm-pills{display:flex;gap:5px;flex-wrap:wrap}'
        + '.pm-pill{display:inline-flex;align-items:center;gap:5px;border:1px solid #cfe0d6;background:#f3faf6;color:#166534;border-radius:999px;padding:2px 9px;font-size:10.5px;font-weight:600}'
        + '.pm-pill b{font-weight:800}'
        /* popup quyền nâng cao */
        + '.pm-advgrp{border:1px solid #e5e7eb;border-radius:9px;margin-bottom:10px;overflow:hidden}'
        + '.pm-advgrp__hd{display:flex;align-items:center;gap:8px;background:#f1f5f9;padding:7px 11px;border-bottom:1px solid #e5e7eb}'
        + '.pm-advgrp__hd .nm{font-size:11.5px;font-weight:800;color:#334155}'
        + '.pm-advgrp__hd .sp{flex:1}'
        + '.pm-advrow{display:flex;align-items:center;gap:9px;padding:7px 11px;font-size:12.5px;color:#334155;border-top:1px solid #f6f8fa}'
        + '.pm-advrow:first-child{border-top:0}'
        + '.pm-empty{padding:14px;text-align:center;font-size:12.5px;color:#6b7280;background:#f8fafc;border:1px dashed #e2e8f0;border-radius:9px}'
        + '.pm-footer{display:flex;justify-content:flex-end;gap:10px;padding:14px 2px 2px;margin-top:12px;border-top:1px solid #e5e7eb}'
        + '.pm-footer .v2-btn{height:40px;padding:0 22px;font-size:13px}'
        + '.pm-grid{display:grid;grid-template-columns:minmax(0,1fr) 320px;gap:12px;align-items:start}'
        + '@media(max-width:1360px){.pm-grid{grid-template-columns:1fr}}'
        + '.pm-panel{position:sticky;top:calc(var(--topbar-h) + 12px);max-height:calc(100vh - var(--topbar-h) - 24px);min-height:0;display:flex;flex-direction:column}'
        + '.pm-panel__hd{display:flex;align-items:center;gap:7px;padding-bottom:9px;border-bottom:1px solid #eef2f6}'
        + '.pm-panel__hd .n{font-size:22px;font-weight:800;color:#16a34a;line-height:1}'
        + '.pm-panel__hd .lb{font-size:11.5px;color:#6b7280}'
        + '.pm-panel .pm-pills{padding:9px 0 4px}'
        + '.pm-panel__bd{overflow-y:auto;flex:1;margin:0 -4px;padding:0 4px}'
        + '.pm-panel__empty{padding:22px 0;text-align:center;font-size:12px;color:#94a3b8}'
        + '.pm-panel__f{display:flex;flex-direction:column;gap:7px;padding:9px 0;border-bottom:1px solid #eef2f6}'
        + '.pm-panel__f .quick-search{margin:0}'
        + '.pm-kinds{display:flex;gap:5px;flex-wrap:wrap}'
        + '.pm-kind{border:1px solid #e2e8f0;background:#fff;border-radius:999px;padding:2px 9px;font-size:10.5px;font-weight:700;font-family:inherit;color:#64748b;cursor:pointer;display:inline-flex;align-items:center;gap:4px}'
        + '.pm-kind b{font-weight:800}'
        + '.pm-kind:hover{border-color:#cbd5e1;color:#334155}'
        + '.pm-kind--empty{opacity:.45}'
        + '.pm-kind--mg.on{background:#f3f0ff;border-color:#c4b5fd;color:#5b21b6}'
        + '.pm-kind--vw.on{background:#effaf3;border-color:#86c9a4;color:#166534}'
        + '.pm-kind--ap.on{background:#fdf6ec;border-color:#f0c98a;color:#92400e}'
        + '.pm-kind--ot.on{background:#eff6ff;border-color:#93c5fd;color:#1d4ed8}'
        + '.pm-pg{margin-bottom:9px}'
        + '.pm-pg__chev{font-size:14px;transition:transform .18s}'
        + '.pm-pg.collapsed .pm-pg__chev{transform:rotate(-90deg)}'
        + '.pm-pg.collapsed .pm-pg__bd{display:none}'
        + '.pm-pg__n{margin-left:auto;background:var(--c-ac);color:#fff;border-radius:999px;padding:0 7px;font-size:10px;font-weight:800}'
        + '.pm-pg__hd{display:flex;align-items:center;gap:5px;font-size:10.5px;font-weight:800;text-transform:uppercase;letter-spacing:.04em;color:var(--c-fg);background:var(--c-bg);border-left:3px solid var(--c-ac);border-radius:4px;padding:5px 8px;margin-bottom:6px;cursor:pointer;user-select:none}'
        + '.pm-po{padding:1px 0 3px 9px;border-left:2px solid var(--c-ac);margin-bottom:7px}'
        + '.pm-po__n{font-size:12px;font-weight:700;color:#0f172a;margin-bottom:2px}'
        + '.pm-pi{display:flex;align-items:center;gap:7px;padding:1px 0 1px 14px;font-size:11px;font-weight:400;color:#64748b;background:none;border:0}'
        + '.pm-pi::before{content:"";width:5px;height:5px;border-radius:50%;background:var(--dot,#cbd5e1);flex:none}'
        + '.pm-pi__t{flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}'
        + '.pm-pi--vw{--dot:#16a34a}'
        + '.pm-pi--mg{--dot:#7c3aed}'
        + '.pm-pi--ap{--dot:#d97706}'
        + '.pm-pi--ot{--dot:#2563eb}'
        + '.pm-pi__b{flex:none;font-size:10px;color:#94a3b8;font-style:italic}'
        + '.pm-viewcell{display:inline-flex;align-items:center;gap:7px}'
        + '.pm-scopebtn{display:inline-flex;align-items:center;gap:4px;border:1px solid #cfe0d6;background:#effaf3;color:#166534;border-radius:999px;padding:2px 9px;font-size:10.5px;font-weight:700;font-family:inherit;cursor:pointer;white-space:nowrap}'
        + '.pm-scopebtn:hover{background:#dcfce7;border-color:#86c9a4}'
        + '.pm-arn{flex:1}'
        + '.pm-apscope{display:inline-flex;align-items:center;gap:4px;border-radius:999px;padding:2px 9px;font-size:10.5px;font-weight:700;white-space:nowrap;cursor:help}'
        + '.pm-apscope--department{background:#fdf6ec;color:#92400e;border:1px solid #f0c98a}'
        + '.pm-apscope--part{background:#fdeee4;color:#9a3412;border:1px solid #f5c09a}'
        + '.pm-apscope--company{background:#eef1f5;color:#334155;border:1px solid #d5dde5}'
        + '.pm-apscope--undecl{border-style:dashed;border-color:#f59e0b;background:#fffbeb;color:#b45309}'
        + '.pm-scopebtn i{font-size:12px}'
        + '.pm-rank{margin-left:auto;font-size:10px;color:#94a3b8;font-weight:600}'
        + '.pm-gatehide{visibility:hidden}'
        + '.pm-hint{font-size:11.5px;color:#475569;background:#f1f5f9;border:1px solid #e2e8f0;border-radius:8px;padding:8px 11px;line-height:1.5}';
    var s = document.createElement('style');
    s.id = 'pm-style'; s.textContent = css;
    document.head.appendChild(s);
}

/* ======================= HELPER ======================= */
function pmNA() { return '<span class="pm-na" title="Không có quyền tương ứng trong hệ thống">–</span>'; }
var PM_CRUD_LABEL = { create: 'Tạo', edit: 'Sửa', del: 'Xóa' };
/* Các quyền CRUD rời mà đối tượng thực sự có trong CSDL */
function pmCrudParts(o) {
    return ['create', 'edit', 'del'].filter(function (k) { return o[k] !== undefined; });
}
function pmCrudOn(o) {
    var b = pmCrudParts(o);
    return b.length > 0 && b.every(function (k) { return o[k]; });
}

function pmDataCk(on, kind, cls) {
    return '<input type="checkbox" class="pm-ck ' + (cls || '') + '"' + (on ? ' checked' : '')
        + ' onchange="pmToggle(this, \'' + kind + '\')">';
}
function pmCk(on, cls) { return '<input type="checkbox" class="pm-ck ' + (cls || '') + '"' + (on ? ' checked' : '') + ' onchange="pmRecount()">'; }
/* Ô có phạm vi: checkbox + nhãn cấp. Tích checkbox → tự mở popup chọn phạm vi. */
function pmGateCell(on, lv, def, objName, kind) {
    var esc = objName.replace(/'/g, "\\'");
    if (!lv.length) return '<input type="checkbox" class="pm-ck pm-ck--gate"' + (on ? ' checked' : '')
        + ' onchange="pmToggle(this, \'' + kind + '\')">';
    return '<div class="pm-viewcell">'
        + '<input type="checkbox" class="pm-ck pm-ck--gate"' + (on ? ' checked' : '')
        + ' onchange="pmToggle(this, \'' + kind + '\')">'
        + '<button type="button" class="pm-scopebtn' + (on ? '' : ' pm-gatehide') + '"'
        + ' onclick="pmOpenScope(\'' + esc + '\', \'' + kind + '\')">'
        + '<i class="ri-focus-3-line"></i> <span>' + (def || 'Chọn phạm vi') + '</span></button>'
        + '</div>';
}

/* ---- Nguồn sự thật: đọc/ghi PM_DATA rồi VẼ LẠI dòng đó ---- */
function pmRowObj(el) {
    var tr = el.closest ? el.closest('tr.pm-obj') : null;
    return tr ? { tr: tr, o: pmFindObj(tr.dataset.obj) } : { tr: null, o: null };
}
function pmRefreshRow(tr) {
    var o = pmFindObj(tr.dataset.obj); if (!o) return;
    tr.innerHTML = pmCols().map(function (c) {
        return '<td class="' + (c.cls || '') + '">' + pmCell(c.k, o) + '</td>';
    }).join('');
}
/* checkbox bất kỳ → ghi vào data → vẽ lại dòng */
function pmToggle(ck, kind) {
    var r = pmRowObj(ck); if (!r.o) return;
    var on = ck.checked, o = r.o;
    if (kind === 'view' && o.view) {
        o.view.on = on;
        if (!on) o.view.def = '';                 /* bỏ quyền thì xoá luôn phạm vi, không giữ ngầm */
    } else if (kind === 'manage' && o.manage) {
        o.manage.on = on;
        if (!on && o.manage.lv) o.manage.def = '';
    } else if (kind === 'manage') {
        pmCrudParts(o).forEach(function (k) { o[k] = on; });
    } else if (kind === 'approve' && o.approve) {
        /* Ô Duyệt 1 loại: bật/tắt loại đó; bỏ tích thì xoá luôn phạm vi duyệt. */
        o.approve.steps.forEach(function (st, i) { st.on = on && i === 0; });
    } else if (kind === 'create' || kind === 'edit' || kind === 'del') {
        o[kind] = on;
    }
    pmRefreshRow(r.tr);
    pmRecount();
    /* tích quyền có phạm vi → bật popup chọn phạm vi ngay.
       Đối tượng gom CRUD không có o.manage nên phải guard, nếu không sẽ nổ TypeError. */
    if (on && (kind === 'view' || kind === 'manage')) {
        var slot = pmSlotOf(o, kind);
        if (slot && (slot.lv || []).length) pmOpenScope(o.n, kind);
    }
}
/* "Tất cả" trên 1 dòng */
function pmToggleAllRow(ck) {
    var r = pmRowObj(ck); if (!r.o) return;
    pmSetObj(r.o, ck.checked);
    pmRefreshRow(r.tr);
    pmRecount();
}
function pmSetObj(o, on) {
    if (o.view) { o.view.on = on; if (!on) o.view.def = ''; else if (o.view.lv.length && !o.view.def) o.view.def = o.view.lv[o.view.lv.length - 1]; }
    if (o.manage) { o.manage.on = on; if (!on && o.manage.lv) o.manage.def = ''; else if (o.manage.lv && !o.manage.def) o.manage.def = o.manage.lv[o.manage.lv.length - 1]; }
    ['create', 'edit', 'del'].forEach(function (k) { if (o[k] !== undefined) o[k] = on; });
    if (o.approve) o.approve.steps.forEach(function (st) { st.on = on; });
    if (o.other) o.other.forEach(function (x) { x.on = on; });
}
function pmObjAllOn(o) {
    var all = [];
    if (o.view) all.push(o.view.on);
    if (o.manage) all.push(o.manage.on);
    ['create', 'edit', 'del'].forEach(function (k) { if (o[k] !== undefined) all.push(o[k]); });
    if (o.approve) o.approve.steps.forEach(function (st) { all.push(st.on); });
    if (o.other) o.other.forEach(function (x) { all.push(x.on); });
    return all.length > 0 && all.every(Boolean);
}

/* Popup chọn phạm vi xem dữ liệu — đọc/ghi thẳng PM_DATA */
var PM_SCOPE_CTX = null;
function pmSlotOf(o, kind) {
    if (kind === 'manage') return o.manage;
    return o.view;
}
function pmOpenScope(objName, kind) {
    var o = pmFindObj(objName); if (!o) return;
    var slot = pmSlotOf(o, kind);
    if (!slot) return;
    var lv = slot.lv || [];
    if (!lv.length) return;
    PM_SCOPE_CTX = { obj: objName, kind: kind };
    var cur = slot.def || '';
    document.getElementById('pm-adv-title').textContent = 'Phạm vi xem dữ liệu';
    document.getElementById('pm-adv-obj').textContent = 'Đối tượng: ' + o.n;
    document.getElementById('pm-adv-body').innerHTML = ''
        + '<div class="pm-advgrp">'
        + lv.map(function (x, i) {
            return '<label class="pm-advrow" style="cursor:pointer">'
                + '<input type="radio" name="pm-scope" class="pm-ck"' + (x === cur ? ' checked' : '') + ' value="' + x + '"> '
                + '<span>' + x + '</span>'
                + '<span class="pm-rank">cấp ' + (i + 1) + '</span></label>';
        }).join('')
        + '</div>';
    pmBindApply('pmApplyScope()');
    openModal('pm-adv-modal');
}
function pmApplyScope() {
    if (PM_SCOPE_CTX) {
        var o = pmFindObj(PM_SCOPE_CTX.obj);
        var slot = o && pmSlotOf(o, PM_SCOPE_CTX.kind);
        var r = document.querySelector('#pm-adv-body input[name="pm-scope"]:checked');
        if (slot) { slot.def = r ? r.value : ''; slot.on = true; }
        pmRefreshObj(PM_SCOPE_CTX.obj);
    }
    PM_SCOPE_CTX = null;
    closeModal('pm-adv-modal');
    pmRecount();
}

/* Nút "Áp dụng" của modal dùng chung → phải gán lại handler MỖI LẦN mở,
   nếu không popup này sẽ chạy handler của popup mở trước đó. */
function pmBindApply(handler) {
    document.getElementById('pm-adv-apply').setAttribute('onclick', handler);
}
/* Vẽ lại mọi dòng của 1 đối tượng (có thể xuất hiện ở nhiều bản cột) */
function pmRefreshObj(objName) {
    document.querySelectorAll('tr.pm-obj').forEach(function (tr) {
        if (tr.dataset.obj === objName) pmRefreshRow(tr);
    });
}

/* Ô Duyệt — bản A gộp mọi bước vào 1 ô (phình ra khi >1 bước); bản C chỉ 1 checkbox */
function pmApproveCell(o) {
    if (!o.approve) return pmNA();
    var st = o.approve.steps;
    var esc = o.n.replace(/'/g, "\\'");
    if (st.length === 1) {
        var a = st[0];
        return '<div class="pm-viewcell">'
            + '<input type="checkbox" class="pm-ck pm-ck--gate-ap"' + (a.on ? ' checked' : '')
            + ' onchange="pmToggle(this, \'approve\')">'
            + pmApScopeTag(a, a.on ? '' : ' pm-gatehide')
            + '</div>';
    }
    var on = st.filter(function (x) { return x.on; }).length;
    return '<button class="pm-advbtn' + (on ? ' on' : '') + '" data-on="' + on + '" onclick="pmOpenList(\'approve\',\'' + esc + '\')">'
        + (on ? '<i class="ri-check-line"></i> ' + on + '/' + st.length : st.length + ' loại') + '</button>';
}

/* Ô Quyền khác — CHỈ bản D. Chứa quyền THẬT còn lại của chính đối tượng đó */
function pmOtherCell(o) {
    var arr = o.other || [];
    if (!arr.length) return pmNA();
    var on = arr.filter(function (x) { return x.on; }).length;
    return '<button class="pm-advbtn' + (on ? ' on' : '') + '" data-on="' + on + '" onclick="pmOpenList(\'other\',\'' + o.n.replace(/'/g, "\\'") + '\')">'
        + (on ? '<i class="ri-check-line"></i> ' + on + '/' + arr.length : arr.length + ' quyền') + '</button>';
}

function pmCols() {
    return [
        { k: 'obj', t: 'Đối tượng', cls: 'l c-obj', g: 'grpA' },
        { k: 'all', t: 'Tất cả', g: 'grpB' },
        { k: 'manage', t: 'Quản lý', g: 'grpB' },
        { k: 'view', t: 'Xem', g: 'grpB' },
        { k: 'approve', t: 'Duyệt', g: 'grpB' },
        { k: 'other', t: 'Quyền khác', g: 'grpC' }
    ];
}

function pmCell(k, o) {
    switch (k) {
        case 'obj':
            return '<div class="pm-obj-nm" title="Gộp từ ' + o.raw + ' quyền gốc trong CSDL">' + o.n
                + (o.note ? '<span class="pm-note">' + o.note + '</span>' : '') + '</div>';
        case 'all': return '<input type="checkbox" class="pm-ck pm-ck--all"' + (pmObjAllOn(o) ? ' checked' : '') + ' onchange="pmToggleAllRow(this)">';
        /* Xem: checkbox + nhãn phạm vi (chỉ hiện khi đã tích, bấm để đổi qua popup).
           Không còn cột Phạm vi riêng — nó vốn chỉ phục vụ quyền Xem. */
        case 'view': {
            if (!o.view) return pmNA();
            /* Trạng thái ô LUÔN đọc từ o.view.on. Trước đây suy từ o.view.def nên tích Xem
               mà chưa chọn phạm vi thì ô lại render rỗng → lệch với panel. */
            return pmGateCell(!!o.view.on, o.view.lv, o.view.def, o.n, 'view');
        }
        /* Quản lý = "phiếu chung / danh mục". Phiếu CÁ NHÂN không có cột này (ô "–").
           Đối tượng chỉ có Tạo/Sửa/Xóa rời trong CSDL được GOM vào đúng ô này. */
        case 'manage': {
            if (o.manage) return pmGateCell(o.manage.on, o.manage.lv || [], o.manage.def || '', o.n, 'manage');
            var b = pmCrudParts(o);
            if (!b.length) return pmNA();
            return '<input type="checkbox" class="pm-ck pm-ck--bundle"' + (pmCrudOn(o) ? ' checked' : '')
                + ' title="Gồm ' + b.length + ' quyền: ' + b.map(function (k) { return PM_CRUD_LABEL[k]; }).join(' · ') + '"'
                + ' onchange="pmToggle(this, \'manage\')">';
        }
        case 'approve': return pmApproveCell(o);
        case 'other': return pmOtherCell(o);
    }
    return '';
}

/* MỘT bảng duy nhất cho TẤT CẢ phân hệ.
   Trước đây mỗi phân hệ 1 <table> riêng → mỗi bảng tự tính độ rộng cột nên header lệch nhau,
   lại có N hàng tiêu đề cùng ghim. Nay: 1 <thead> duy nhất + phân hệ là DẢI NGANG (sticky). */
function pmRenderMatrix() {
    var cols = pmCols();
    var head = '<thead><tr>' + cols.map(function (c) {
        return '<th class="' + (c.cls || '') + ' ' + c.g + '">' + c.t + '</th>';
    }).join('') + '</tr></thead>';

    var body = PM_DATA.map(function (s, si) {
        var nObj = s.groups.reduce(function (a, g) { return a + g.objs.length; }, 0);
        var nRaw = s.groups.reduce(function (a, g) { return a + g.objs.reduce(function (b, o) { return b + o.raw; }, 0); }, 0);

        var h = pmHue(si);
        var srow = '<tbody class="pm-sec" data-si="' + si + '">'
            + '<tr class="pm-srow"><td colspan="' + cols.length + '" onclick="pmToggleSec(this)"'
            + ' style="--c-bg:' + h.bg + ';--c-fg:' + h.fg + ';--c-ac:' + h.ac + '"><div class="in">'
            + '<i class="ri-arrow-down-s-line pm-chev"></i>'
            + '<span class="nm">' + s.sub + '</span>'
            + '<span class="sp"></span>'
            + '<span class="pm-srow__n" data-si="' + si + '"></span>'
            + '<span class="ct">' + nRaw + ' quyền gốc → <b>' + nObj + ' đối tượng</b></span>'
            + '</div></td></tr></tbody>';

        var groups = s.groups.map(function (g, gi) {
            var grow = '<tr class="pm-grow"><td colspan="' + cols.length + '"><div class="in">'
                + '<span class="nm"><i class="ri-folder-3-fill"></i>' + g.g + '</span>'
                + '<span class="sp"></span>'
                + '<label class="pm-gsel">'
                + '<input type="checkbox" class="pm-ck pm-ck--all" onchange="pmBulkGroup(this)"> Chọn cả nhóm</label>'
                + '</div></td></tr>';
            var rows = g.objs.map(function (o) {
                return '<tr class="pm-obj" data-obj="' + o.n.replace(/"/g, '&quot;') + '">' + cols.map(function (c) {
                    return '<td class="' + (c.cls || '') + '">' + pmCell(c.k, o) + '</td>';
                }).join('') + '</tr>';
            }).join('');
            return '<tbody class="pm-body" data-si="' + si + '" data-gi="' + gi + '">' + grow + rows + '</tbody>';
        }).join('');

        return srow + groups;
    }).join('');

    return '<div class="pm-scroll"><table class="pm-tb">' + head + body + '</table></div>';
}

/* Thu/mở 1 phân hệ = ẩn/hiện mọi tbody.pm-body cùng data-si */
function pmToggleSec(td) {
    var sec = td.closest('tbody.pm-sec');
    var closed = sec.classList.toggle('collapsed');
    pmShowSec(+sec.dataset.si, !closed);
}
function pmShowSec(si, open) {
    document.querySelectorAll('tbody.pm-body[data-si="' + si + '"]').forEach(function (tb) {
        tb.classList.toggle('pm-hidden', !open);
    });
    var sec = document.querySelector('tbody.pm-sec[data-si="' + si + '"]');
    if (sec) sec.classList.toggle('collapsed', !open);
}

function pmRender() {
    var html = ''
        /* banner */
        + '<section class="tp-card p-3 mb-2">'
        + '  <div class="pm-banner">'
        + '    <i class="ri-shield-keyhole-line"></i>'
        + '    <span>Đang phân quyền cho chức vụ <b>' + PM_ROLE + '</b></span>'
        + '  </div>'
        + '  <div class="pm-filter">'
        + '    <div class="pm-ff"><label class="tp-label">Phân hệ</label>'
        + '      <select class="form-control form-control-sm" id="pm-f-sub" onchange="pmFilter()">'
        + '        <option value="">— Tất cả phân hệ —</option>' + PM_DATA.map(function (s) { return '<option>' + s.sub + '</option>'; }).join('')
        + '      </select></div>'
        + '    <div class="pm-ff"><label class="tp-label">Nhóm chức năng</label>'
        + '      <select class="form-control form-control-sm" id="pm-f-grp" onchange="pmFilter()"><option value="">— Tất cả nhóm —</option></select></div>'
        + '    <div class="pm-ff"><label class="tp-label">Hành động</label>'
        + '      <select class="form-control form-control-sm" id="pm-f-act" onchange="pmFilter()">'
        + '        <option value="">— Tất cả hành động —</option><option value="manage">Quản lý</option><option value="view">Xem</option>'
        + '        <option value="approve">Duyệt</option><option value="other">Quyền khác</option><option value="scope">Có phạm vi xem</option>'
        + '      </select></div>'
        + '    <div class="pm-ff" style="flex:2"><label class="tp-label">Tìm nhanh</label>'
        + '      <div class="quick-search"><i class="ri-search-line"></i>'
        + '        <input class="form-control form-control-sm" id="pm-f-kw" placeholder="Tìm theo tên đối tượng..." oninput="pmFilter()"></div></div>'
        + '    <div class="pm-bulkact" id="pm-bulkact" style="display:none">'
        + '      <button class="v2-btn v2-btn--sm v2-btn--primary-success" onclick="pmBulkByAction(true)">'
        + '        <i class="ri-checkbox-multiple-line"></i> <span id="pm-bulkact-t"></span></button>'
        + '      <button class="v2-btn v2-btn--sm v2-btn--secondary" onclick="pmBulkByAction(false)" title="Bỏ chọn hành động này ở các dòng đang hiện">'
        + '        <i class="ri-checkbox-multiple-blank-line"></i></button>'
        + '    </div>'
        + '    <button class="v2-btn v2-btn--sm v2-btn--secondary" onclick="pmClearFilter()"><i class="ri-refresh-line"></i> Xóa lọc</button>'
        + '    <button class="v2-btn v2-btn--sm v2-btn--secondary" onclick="pmToggleAll(true)"><i class="ri-arrow-down-s-line"></i> Mở tất cả</button>'
        + '    <button class="v2-btn v2-btn--sm v2-btn--secondary" onclick="pmToggleAll(false)"><i class="ri-arrow-up-s-line"></i> Thu gọn</button>'
        + '  </div>'
        + '</section>'
        /* ma trận */
        + '<div class="pm-grid">'
        + '  <section class="tp-card p-3">'
        + '    <div class="table-card-header">'
        + '      <div class="filter-header-left"><div class="tp-icon-chip"><i class="ri-grid-line"></i></div>'
        + '        <div><h5>Ma trận phân quyền</h5></div></div>'
        + '    </div>'
        + '    <div id="pm-matrix">' + pmRenderMatrix() + '</div>'
        + '  </section>'
        + '  <aside class="pm-panel tp-card p-3" id="pm-panel">' + pmPanelSkeleton() + '</aside>'
        + '</div>'
        /* popup quyền nâng cao */
        + '<div class="modal-backdrop-demo" id="pm-adv-modal">'
        + '  <div class="modal-dialog" style="max-width:560px">'
        + '    <div class="modal-header"><div class="filter-header-left"><div class="tp-icon-chip"><i class="ri-shield-star-line"></i></div>'
        + '      <div><h5 style="margin:0" id="pm-adv-title">Quyền nâng cao</h5><p class="tp-section-subtitle" id="pm-adv-obj"></p></div></div>'
        + '      <button class="v2-icon-btn v2-icon-btn--sm" onclick="closeModal(\'pm-adv-modal\')"><i class="ri-close-line"></i></button></div>'
        + '    <div class="modal-body" id="pm-adv-body"></div>'
        + '    <div class="modal-footer"><button class="v2-btn v2-btn--sm v2-btn--secondary" onclick="closeModal(\'pm-adv-modal\')">Đóng</button>'
        + '      <button class="v2-btn v2-btn--sm v2-btn--primary-success" id="pm-adv-apply" onclick="closeModal(\'pm-adv-modal\')"><i class="ri-check-line"></i> Áp dụng</button></div>'
        + '  </div>'
        + '</div>';

    pmInjectStyle();
    document.body.innerHTML = '';
    renderShell('permission', html);
    pmFillGroupFilter();
    pmRecount();
    pmMeasureStickyOffset();
    /* Mặc định THU GỌN hết, chỉ mở phân hệ đầu.
       Đây là cách "phân trang" của màn này: đơn vị là PHÂN HỆ, không phải dòng —
       phân quyền là MỘT form lưu một lần, cắt trang theo dòng sẽ làm rải rác trạng thái. */
    PM_DATA.forEach(function (x, si) { pmShowSec(si, si === 0); });
}

/* Đo chiều cao thật của header phân hệ → thead ghim khít bên dưới, không hở dòng */
function pmMeasureStickyOffset() {
    var th = document.querySelector('.pm-tb thead th');
    if (!th) return;
    var h = Math.floor(th.getBoundingClientRect().height);
    document.documentElement.style.setProperty('--pm-thead-h', h + 'px');
}
window.addEventListener('resize', pmMeasureStickyOffset);

/* ======================= TƯƠNG TÁC ======================= */
function pmToggleAll(open) {
    PM_DATA.forEach(function (s, si) { pmShowSec(si, open); });
}

/* "Chọn cả nhóm" — bật/tắt mọi checkbox + đưa select về cấp cao nhất khả dụng */
var PM_ACT_LABEL = { manage: 'Quản lý', view: 'Xem', approve: 'Duyệt', other: 'Quyền khác' };

/* Các dòng đối tượng ĐANG HIỆN (đã qua mọi bộ lọc) */
function pmVisibleRows() {
    return [].filter.call(document.querySelectorAll('tr.pm-obj'), function (tr) {
        if (tr.style.display === 'none') return false;
        var tb = tr.closest('tbody');
        return tb && !tb.classList.contains('pm-filtered-out');
    });
}

/* Đối tượng có dùng được hành động này không (ô không phải "–") */
function pmObjHasAction(o, act) {
    if (act === 'view') return !!o.view;
    if (act === 'manage') return !!o.manage || pmCrudParts(o).length > 0;
    if (act === 'approve') return !!o.approve;
    if (act === 'other') return (o.other || []).length > 0;
    return false;
}

/* Bật/tắt HÀNG LOẠT đúng hành động đang lọc, chỉ trên các dòng đang hiện */
function pmBulkByAction(on) {
    var act = document.getElementById('pm-f-act').value;
    if (!PM_ACT_LABEL[act]) return;
    pmVisibleRows().forEach(function (tr) {
        var o = pmFindObj(tr.dataset.obj);
        if (!o || !pmObjHasAction(o, act)) return;
        if (act === 'view') {
            o.view.on = on;
            if (!on) o.view.def = '';
            else if (o.view.lv.length && !o.view.def) o.view.def = o.view.lv[o.view.lv.length - 1];
        } else if (act === 'manage') {
            if (o.manage) {
                o.manage.on = on;
                if (!on && o.manage.lv) o.manage.def = '';
                else if (o.manage.lv && !o.manage.def) o.manage.def = o.manage.lv[o.manage.lv.length - 1];
            } else pmCrudParts(o).forEach(function (k) { o[k] = on; });
        } else if (act === 'approve') {
            o.approve.steps.forEach(function (st, i) { st.on = on && i === 0; });
        } else if (act === 'other') {
            o.other.forEach(function (x) { x.on = on; });
        }
        pmRefreshRow(tr);
    });
    pmRecount();
    toast((on ? 'Đã cấp' : 'Đã bỏ') + ' quyền ' + PM_ACT_LABEL[act] + ' cho các dòng đang hiện', on ? 'success' : 'warning');
}

/* Hiện/ẩn nút theo ô lọc Hành động + đếm số dòng sẽ bị tác động */
function pmSyncBulkAct() {
    var box = document.getElementById('pm-bulkact'); if (!box) return;
    var act = document.getElementById('pm-f-act').value;
    if (!PM_ACT_LABEL[act]) { box.style.display = 'none'; return; }
    var n = pmVisibleRows().filter(function (tr) {
        var o = pmFindObj(tr.dataset.obj);
        return o && pmObjHasAction(o, act);
    }).length;
    box.style.display = n ? '' : 'none';
    document.getElementById('pm-bulkact-t').textContent = 'Chọn tất cả ' + PM_ACT_LABEL[act] + ' (' + n + ')';
}

function pmBulkGroup(cb) {
    var tb = cb.closest('tbody'), on = cb.checked;
    tb.querySelectorAll('tr.pm-obj').forEach(function (tr) {
        var o = pmFindObj(tr.dataset.obj);
        if (o) { pmSetObj(o, on); pmRefreshRow(tr); }
    });
    pmRecount();
}

/* Đếm từ PM_DATA — không phụ thuộc bộ cột đang xem, nên đổi bản A/C/D số không nhảy.
   1 quyền = 1 hành động đã cấp. Phạm vi chỉ chọn biến thể của quyền Xem, KHÔNG tính riêng. */
function pmCountObj(o) {
    var n = 0;
    if (o.view && o.view.on) n++;
    if (o.manage && o.manage.on) n++;
    ['create', 'edit', 'del'].forEach(function (k) { if (o[k]) n++; });
    if (o.approve) o.approve.steps.forEach(function (st) { if (st.on) n++; });
    if (o.other) o.other.forEach(function (x) { if (x.on) n++; });
    return n;
}
function pmCountSub(sub) {
    return sub.groups.reduce(function (a, g) {
        return a + g.objs.reduce(function (b, o) { return b + pmCountObj(o); }, 0);
    }, 0);
}

/* Panel phải — liệt kê quyền ĐANG ĐƯỢC PHÂN cho chức vụ, gom Phân hệ → Đối tượng */
function pmGrantedTree() {
    return PM_DATA.map(function (sub, si) {
        var objs = [];
        sub.groups.forEach(function (g) {
            g.objs.forEach(function (o) {
                var items = [];
                if (o.manage && o.manage.on) items.push({ t: 'Quản lý', c: 'mg' });
                else if (!o.manage && pmCrudOn(o)) pmCrudParts(o).forEach(function (k) { items.push({ t: PM_CRUD_LABEL[k], c: 'mg' }); });
                else if (!o.manage) pmCrudParts(o).forEach(function (k) { if (o[k]) items.push({ t: PM_CRUD_LABEL[k], c: 'mg' }); });
                if (o.view && o.view.on) items.push({ t: 'Xem', c: 'vw', b: o.view.def });
                if (o.approve) o.approve.steps.forEach(function (st) {
                    if (st.on) items.push({ t: st.n, c: 'ap', b: pmApScope(st).t });
                });
                if (o.other) o.other.forEach(function (x) { if (x.on) items.push({ t: x.n, c: 'ot' }); });
                if (items.length) objs.push({ n: o.n, items: items });
            });
        });
        return objs.length ? { sub: sub.sub, si: si, objs: objs } : null;
    }).filter(Boolean);
}

/* Badge "đang cấp N" trên dải phân hệ — để thu gọn rồi vẫn thấy phân hệ nào đã phân quyền */
function pmUpdateSecBadges() {
    document.querySelectorAll('.pm-srow__n').forEach(function (el) {
        var n = pmCountSub(PM_DATA[+el.dataset.si]);
        el.innerHTML = n ? '<span class="pm-secn">đang cấp ' + n + '</span>' : '';
    });
}

var PM_PANEL_KW = '';
var PM_PANEL_KIND = '';          /* '' | mg | vw | ap | ot */
var PM_KIND_LABEL = { mg: 'Quản lý', vw: 'Xem', ap: 'Duyệt', ot: 'Khác' };

/* Khung panel dựng MỘT LẦN — nếu dựng lại cả panel mỗi lần đếm thì đang gõ ô lọc sẽ mất focus */
function pmPanelSkeleton() {
    return ''
        + '<div class="pm-panel__hd"><div class="n" id="pm-pn">0</div><div class="lb">quyền đã phân</div>'
        + '<span class="pm-sub__sp"></span>'
        + '<button class="v2-btn v2-btn--sm v2-btn--primary-success" onclick="pmSave()">'
        + '<i class="ri-save-3-line"></i> Lưu</button></div>'
        + '<div class="pm-panel__f">'
        + '  <div class="quick-search"><i class="ri-search-line"></i>'
        + '    <input class="form-control form-control-sm" id="pm-pkw" placeholder="Tìm trong quyền đã phân..." oninput="pmPanelSearch(this)"></div>'
        + '  <div class="pm-kinds" id="pm-kinds"></div>'
        + '</div>'
        + '<div class="pm-panel__bd" id="pm-panel-bd"></div>';
}
function pmPanelSearch(inp) { PM_PANEL_KW = (inp.value || '').trim().toLowerCase(); pmBuildPanel(); }
function pmPanelKind(k) { PM_PANEL_KIND = (PM_PANEL_KIND === k ? '' : k); pmBuildPanel(); }
function pmPanelToggle(el) { el.parentNode.classList.toggle('collapsed'); }

function pmBuildPanel() {
    var bd = document.getElementById('pm-panel-bd'); if (!bd) return;
    var tree = pmGrantedTree();
    var totalAll = 0, byKind = { mg: 0, vw: 0, ap: 0, ot: 0 };
    tree.forEach(function (t) {
        t.objs.forEach(function (o) {
            o.items.forEach(function (it) { totalAll++; byKind[it.c]++; });
        });
    });

    /* lọc theo loại + từ khoá (khớp tên đối tượng HOẶC tên quyền) */
    var shown = 0;
    var view = tree.map(function (t) {
        var objs = t.objs.map(function (o) {
            var hitObj = !PM_PANEL_KW || o.n.toLowerCase().indexOf(PM_PANEL_KW) >= 0;
            var items = o.items.filter(function (it) {
                if (PM_PANEL_KIND && it.c !== PM_PANEL_KIND) return false;
                if (!PM_PANEL_KW) return true;
                return hitObj || it.t.toLowerCase().indexOf(PM_PANEL_KW) >= 0;
            });
            return items.length ? { n: o.n, items: items } : null;
        }).filter(Boolean);
        shown += objs.reduce(function (a, o) { return a + o.items.length; }, 0);
        return objs.length ? { sub: t.sub, si: t.si, objs: objs } : null;
    }).filter(Boolean);

    document.getElementById('pm-pn').textContent = totalAll;
    document.getElementById('pm-kinds').innerHTML = ['mg', 'vw', 'ap', 'ot'].map(function (k) {
        return '<button class="pm-kind pm-kind--' + k + (PM_PANEL_KIND === k ? ' on' : '')
            + (byKind[k] ? '' : ' pm-kind--empty') + '" onclick="pmPanelKind(\'' + k + '\')">'
            + PM_KIND_LABEL[k] + ' <b>' + byKind[k] + '</b></button>';
    }).join('');

    if (!totalAll) { bd.innerHTML = '<div class="pm-panel__empty">Chưa phân quyền nào</div>'; return; }
    if (!view.length) { bd.innerHTML = '<div class="pm-panel__empty">Không có quyền nào khớp bộ lọc</div>'; return; }

    bd.innerHTML = view.map(function (t) {
        var h = pmHue(t.si);
        var n = t.objs.reduce(function (a, o) { return a + o.items.length; }, 0);
        return '<div class="pm-pg" style="--c-bg:' + h.bg + ';--c-fg:' + h.fg + ';--c-ac:' + h.ac + '">'
            + '<div class="pm-pg__hd" onclick="pmPanelToggle(this)">'
            + '<i class="ri-arrow-down-s-line pm-pg__chev"></i><span>' + t.sub + '</span>'
            + '<span class="pm-pg__n">' + n + '</span></div>'
            + '<div class="pm-pg__bd">'
            + t.objs.map(function (o) {
                return '<div class="pm-po"><div class="pm-po__n">' + o.n + '</div>'
                    + o.items.map(function (it) {
                        return '<div class="pm-pi pm-pi--' + it.c + '">'
                            + '<span class="pm-pi__t">' + it.t + '</span>'
                            + (it.b ? '<span class="pm-pi__b">' + it.b + '</span>' : '') + '</div>';
                    }).join('')
                    + '</div>';
            }).join('')
            + '</div></div>';
    }).join('');
}

function pmRecount() {
    var total = 0, pills = [];
    PM_DATA.forEach(function (sub) {
        var n = pmCountSub(sub);
        total += n;
        if (n) pills.push('<span class="pm-pill"><i class="ri-checkbox-circle-line"></i>'
            + sub.sub + ' <b>' + n + '</b></span>');
    });
    pmBuildPanel();
    pmUpdateSecBadges();
    pmSyncBulkAct();
}

/* ---------- bộ lọc ---------- */
function pmFillGroupFilter() {
    var sub = document.getElementById('pm-f-sub').value, seen = [];
    PM_DATA.forEach(function (s) {
        if (sub && s.sub !== sub) return;
        s.groups.forEach(function (g) { if (seen.indexOf(g.g) < 0) seen.push(g.g); });
    });
    document.getElementById('pm-f-grp').innerHTML = '<option value="">— Tất cả nhóm —</option>'
        + seen.map(function (g) { return '<option>' + g + '</option>'; }).join('');
}
function pmClearFilter() {
    ['pm-f-sub', 'pm-f-grp', 'pm-f-act', 'pm-f-kw'].forEach(function (id) { document.getElementById(id).value = ''; });
    pmFillGroupFilter(); pmFilter();
}
function pmObjMatchAct(o, act) {
    if (!act) return true;
    if (act === 'view') return !!o.view;
    if (act === 'manage') return !!o.manage || pmCrudParts(o).length > 0;
    if (act === 'other') return (o.other || []).length > 0;
    if (act === 'approve') return !!o.approve;
    if (act === 'scope') return !!((o.view && o.view.lv.length) || (o.manage && o.manage.lv));
    return true;
}
function pmFilter() {
    var sub = document.getElementById('pm-f-sub').value;
    var grp = document.getElementById('pm-f-grp').value;
    var act = document.getElementById('pm-f-act').value;
    var kw = (document.getElementById('pm-f-kw').value || '').trim().toLowerCase();
    var hasFilter = !!(sub || grp || act || kw);

    PM_DATA.forEach(function (s, si) {
        var subShown = 0;
        s.groups.forEach(function (g, gi) {
            var tb = document.querySelector('tbody.pm-body[data-si="' + si + '"][data-gi="' + gi + '"]');
            if (!tb) return;
            var shown = 0;
            tb.querySelectorAll('tr.pm-obj').forEach(function (tr, i) {
                var o = g.objs[i];
                var ok = (!sub || s.sub === sub) && (!grp || g.g === grp) && pmObjMatchAct(o, act)
                    && (!kw || o.n.toLowerCase().indexOf(kw) >= 0);
                tr.style.display = ok ? '' : 'none';
                if (ok) shown++;
            });
            tb.classList.toggle('pm-filtered-out', !shown);
            subShown += shown;
        });
        var sec = document.querySelector('tbody.pm-sec[data-si="' + si + '"]');
        if (sec) sec.classList.toggle('pm-filtered-out', !subShown);
        if (hasFilter && subShown) pmShowSec(si, true);   /* có lọc thì tự bung phân hệ khớp */
    });
    pmSyncBulkAct();
}

function pmFindObj(name) {
    var found = null;
    PM_DATA.forEach(function (s) {
        s.groups.forEach(function (g) {
            g.objs.forEach(function (o) { if (o.n === name) found = o; });
        });
    });
    return found;
}
function pmOpenList(kind, name) {
    var o = pmFindObj(name); if (!o) return;
    var isAp = kind === 'approve';
    var arr = isAp ? o.approve.steps : (o.other || []);
    var par = isAp && o.approve.parallel;
    document.getElementById('pm-adv-title').textContent = isAp ? 'Các loại duyệt' : 'Quyền khác';
    document.getElementById('pm-adv-obj').textContent = 'Đối tượng: ' + o.n;
    document.getElementById('pm-adv-body').innerHTML = ''
        + '<div class="quick-search" style="margin-bottom:10px"><i class="ri-search-line"></i>'
        + '<input class="form-control form-control-sm" placeholder="Tìm quyền..." oninput="pmAdvSearch(this)"></div>'
        + '<div class="pm-advgrp"><div class="pm-advgrp__hd">'
        + '<span class="nm">' + (isAp ? 'Loại duyệt' : 'Quyền nghiệp vụ') + '</span><span class="sp"></span>'
        + '<label style="display:inline-flex;align-items:center;gap:6px;font-size:11px;color:#475569;font-weight:600;margin:0;cursor:pointer">'
        + '<input type="checkbox" class="pm-ck" onchange="pmAdvAll(this)"> Chọn cả nhóm</label></div>'
        + arr.map(function (x) {
            var sc = isAp ? pmApScopeTag(x) : '';
            return '<div class="pm-advrow"><input type="checkbox" class="pm-ck"' + (x.on ? ' checked' : '')
                + '> <span class="pm-arn">' + x.n + '</span>' + sc + '</div>';
        }).join('')
        + '</div>';
    PM_LIST_CTX = { obj: o.n, kind: kind };
    pmBindApply('pmApplyList()');
    openModal('pm-adv-modal');
}

/* Lưu lựa chọn trong popup vào PM_DATA rồi vẽ lại dòng → nút trên bảng
   ("1/1", "3 loại") và số tổng cập nhật đúng; mở lại popup thấy đúng cái đã chọn. */
var PM_LIST_CTX = null;
function pmApplyList() {
    if (PM_LIST_CTX) {
        var o = pmFindObj(PM_LIST_CTX.obj);
        var arr = o && (PM_LIST_CTX.kind === 'approve' ? o.approve.steps : (o.other || []));
        var rows = document.querySelectorAll('#pm-adv-body .pm-advrow');
        if (arr) arr.forEach(function (x, i) {
            if (!rows[i]) return;
            x.on = rows[i].querySelector('.pm-ck').checked;
        });
        pmRefreshObj(PM_LIST_CTX.obj);
    }
    PM_LIST_CTX = null;
    closeModal('pm-adv-modal');
    pmRecount();
}
function pmAdvAll(cb) {
    cb.closest('.pm-advgrp').querySelectorAll('.pm-advrow .pm-ck').forEach(function (x) {
        x.checked = cb.checked;
    });
}
function pmAdvSearch(inp) {
    var kw = (inp.value || '').trim().toLowerCase();
    document.querySelectorAll('#pm-adv-body .pm-advrow').forEach(function (r) {
        r.style.display = r.textContent.toLowerCase().indexOf(kw) >= 0 ? '' : 'none';
    });
}

function pmSave() {
    var n = PM_DATA.reduce(function (a, sub) { return a + pmCountSub(sub); }, 0);
    toast('Đã lưu ' + n + ' quyền cho chức vụ ' + PM_ROLE + ' (demo)', 'success');
}
