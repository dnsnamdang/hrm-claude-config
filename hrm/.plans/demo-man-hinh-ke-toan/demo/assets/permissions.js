/* ============================================================
   Demo Kế toán HRM — Màn "Phân quyền" (Quản trị hệ thống)
   Dùng shell + style.css chung. CSS riêng inject 1 lần vào <head>.
   Trạng thái màn lưu ở location.hash → reload không mất màn.
   ============================================================ */

var PQ_LEVELS = ['Tổng công ty', 'Công ty', 'Phòng ban', 'Bộ phận'];
/* Công ty của người dùng đang đăng nhập — cố định, KHÔNG cho chọn */
var PQ_MY_COMPANY = 'Cty Tân Phát Hà Nội';

var PQ_ROLES = [
    { n: 'Giám đốc điều hành', d: 'CEO', c: 214, s: 'active', by: 'Đặng Nam', at: '12/08/2026' },
    { n: 'Kế toán trưởng', d: 'Chief Accountant', c: 87, s: 'active', by: 'Đặng Nam', at: '11/08/2026' },
    { n: 'Nhân viên chấm công', d: 'Timekeeper', c: 23, s: 'active', by: 'Trần Quốc', at: '09/08/2026' },
    { n: 'Trưởng phòng kinh doanh', d: 'Sales Manager', c: 56, s: 'active', by: 'Lê Vân', at: '08/08/2026' },
    { n: 'Thực tập sinh', d: 'Intern', c: 4, s: 'cancel', by: 'Hệ thống', at: '01/08/2026' }
];

/* view = quyền Xem (có phạm vi cấp) ; act = quyền khác (approve=true → Duyệt) */
var PQ_SUB = [
    {
        grp: '1. Nhân sự', name: 'Chấm công', open: true, groups: [
            {
                g: 'Chấm công', views: [
                    { n: 'Bảng chấm công chi tiết', levels: ['Tổng công ty', 'Công ty', 'Phòng ban', 'Bộ phận'], def: 'Công ty' },
                    { n: 'Bảng chấm công tổng hợp', levels: ['Công ty', 'Phòng ban', 'Bộ phận'], def: '' },
                    { n: 'Dữ liệu chấm công', levels: ['Tổng công ty', 'Công ty', 'Phòng ban', 'Bộ phận'], def: 'Bộ phận' }
                ], acts: []
            },
            {
                g: 'Ca làm việc', views: [
                    { n: 'Phân ca chi tiết', levels: ['Tổng công ty', 'Công ty'], def: 'Công ty' },
                    { n: 'Danh mục ca làm việc', levels: ['Tổng công ty', 'Công ty'], def: '' },
                    { n: 'Bảng phân ca tổng hợp', levels: ['Công ty'], def: '' }
                ], acts: [
                    { l: 'Thêm mới phân ca chi tiết', on: true }, { l: 'Thêm mới ca làm việc' },
                    { l: 'Quản lý ca làm việc', on: true }, { l: 'Phân ca' }
                ]
            },
            {
                g: 'Phê duyệt', views: [], acts: [
                    { l: 'Duyệt đơn xin nghỉ', approve: true, on: true }, { l: 'Duyệt đăng ký đi muộn về sớm', approve: true },
                    { l: 'Duyệt đăng ký làm thêm', approve: true }, { l: 'Duyệt phiếu yêu cầu làm thêm', approve: true },
                    { l: 'Duyệt đề nghị tra soát công', approve: true }, { l: 'Xác nhận đề nghị tra soát công', approve: true }
                ]
            },
            {
                g: 'Quản lý đăng ký làm thêm', views: [], acts: [
                    { l: 'Sửa đăng ký làm thêm' }, { l: 'Xoá đăng ký làm thêm' }, { l: 'Duyệt đăng ký làm thêm', approve: true, on: true }
                ]
            }
        ]
    },
    {
        grp: '1. Nhân sự', name: 'Tính lương', open: false, groups: [
            { g: 'Bảng lương', views: [{ n: 'Bảng lương', levels: ['Tổng công ty', 'Công ty', 'Phòng ban', 'Bộ phận'], def: '' }], acts: [{ l: 'Khóa kỳ lương' }, { l: 'Xuất bảng lương' }] },
            { g: 'Tạm ứng lương', views: [{ n: 'Tạm ứng lương', levels: ['Công ty', 'Phòng ban', 'Bộ phận'], def: '' }], acts: [{ l: 'Tạo tạm ứng' }, { l: 'Duyệt tạm ứng', approve: true }] }
        ]
    },
    {
        grp: '4. Kinh doanh - Tài chính', name: 'Tài chính', open: false, groups: [
            { g: 'Yêu cầu chuyển hàng', views: [{ n: 'Yêu cầu chuyển hàng', levels: ['Tổng công ty', 'Công ty', 'Phòng ban', 'Bộ phận'], def: '' }], acts: [{ l: 'Tạo yêu cầu chuyển hàng' }, { l: 'Duyệt yêu cầu chuyển hàng', approve: true }] }
        ]
    }
];

/* ---------- CSS riêng (inject 1 lần) ---------- */
function pqInjectStyle() {
    if (document.getElementById('pq-style')) return;
    var css = ''
        /* layout: tỷ lệ 8 : 4 (editor : tổng hợp) */
        + '.pq-grid{display:grid;grid-template-columns:minmax(0,2fr) minmax(0,1fr);gap:14px;align-items:start}'
        + '@media(max-width:1180px){.pq-grid{grid-template-columns:1fr}}'
        + '.pq-permcount{display:inline-flex;align-items:center;gap:5px;padding:3px 11px;border-radius:999px;font-size:11.5px;font-weight:600;color:#1d4ed8;background:#dbeafe;border:1px solid #bfdbfe;cursor:pointer;font-family:inherit}'
        + '.pq-permcount:hover{background:#bfdbfe;border-color:#93c5fd}'
        + '.pq-filter1{display:flex;gap:10px;align-items:flex-end;flex-wrap:wrap}'
        + '.pq-ff{display:flex;flex-direction:column;gap:3px;flex:1;min-width:145px}'
        + '.pq-ff .tp-label{margin-bottom:0}.pq-ff .quick-search{margin-bottom:0}'
        + '.pq-banner{display:flex;align-items:center;gap:12px}'
        + '.pq-banner .l1{font-size:0.85rem;font-weight:600;color:#0f172a}'
        + '.pq-banner .l2{font-size:12px;color:#6b7280;margin-top:2px;max-width:720px}'
        + '.pq-company{display:inline-flex;align-items:center;gap:8px;border:1px solid #e5e7eb;border-radius:8px;padding:6px 11px;background:#f8fafc}'
        + '.pq-company label{font-size:10px;text-transform:uppercase;letter-spacing:.04em;color:#94a3b8;font-weight:700;margin:0}'
        + '.pq-company b{font-size:12.5px;color:#0f172a}'
        + '.pq-company i{color:#16a34a}'
        /* accordion phân hệ — HEADER NỀN XANH để phân biệt với nhóm */
        + '.pq-sub{border:1px solid #cfe0d6;border-radius:10px;overflow:hidden;margin-bottom:12px;background:#fff}'
        + '.pq-sub__hd{display:flex;align-items:center;gap:9px;padding:10px 12px;cursor:pointer;background:#e6f4ec;border-bottom:1px solid #cfe0d6}'
        + '.pq-sub.collapsed .pq-sub__hd{border-bottom:0}'
        + '.pq-sub__hd:hover{background:#dcefe4}'
        + '.pq-chev{color:#15803d;font-size:16px;transition:transform .18s}'
        + '.pq-sub.collapsed .pq-chev{transform:rotate(-90deg)}'
        + '.pq-sub.collapsed .pq-sub__bd{display:none}'
        + '.pq-sub__name{font-weight:800;color:#14532d;font-size:13px}'
        + '.pq-sub__sp{flex:1}'
        + '.pq-sub__bd{padding:10px}'
        + '.pq-link{display:inline-flex;align-items:center;gap:4px;background:#fff;border:1px solid #cfe0d6;color:#16a34a;font-weight:600;font-size:11px;cursor:pointer;padding:3px 8px;border-radius:6px}'
        + '.pq-link:hover{background:#dcfce7;border-color:#bbf7d0}'
        + '.pq-link i{font-size:13px}'
        + '.pq-link--off{color:#64748b;border-color:#e2e8f0}.pq-link--off:hover{background:#f1f5f9;border-color:#e2e8f0}'
        /* group — HEADER NỀN XÁM NHẠT, khác hẳn phân hệ */
        + '.pq-group{border:1px solid #e5e7eb;border-radius:9px;overflow:hidden}'
        + '.pq-group+.pq-group{margin-top:10px}'
        + '.pq-group__hd{display:flex;align-items:center;gap:8px;padding:8px 11px;background:#f1f5f9;border-bottom:1px solid #e5e7eb}'
        + '.group-label{display:inline-flex;align-items:center;gap:6px;font-size:11.5px;font-weight:700;color:#334155}'
        + '.group-label i{font-size:14px;color:#64748b}'
        + '.pq-count{font-size:10.5px;color:#94a3b8;font-weight:600}'
        + '.pq-ghd-sp{flex:1}'
        /* permission row (chung cho mọi loại) — phạm vi inline */
        /* bảng chức năng trong card phân hệ */
        + '.pq-table{width:100%;border-collapse:collapse;margin:0}'
        + '.pq-table thead th{background:#eef2f6;color:#475569;font-size:10.5px;font-weight:800;text-transform:uppercase;letter-spacing:.04em;padding:7px 10px;border:1px solid #e5e7eb;text-align:left}'
        + '.pq-table thead th.text-right{text-align:right}'
        + '.pq-table td{border:1px solid #eef2f6;padding:6px 10px;font-size:12.5px;color:#334155;vertical-align:middle}'
        + '.pq-table tbody tr.pq-item:hover td{background:#f6fdf9}'
        + '.pq-c-type{width:84px;white-space:nowrap}'
        + '.pq-c-scope{text-align:right;white-space:nowrap}'
        + '.pq-nm{font-weight:400;color:#334155}'
        + '.pq-chkbox2{width:17px;height:17px;accent-color:#16a34a;cursor:pointer;vertical-align:middle}'
        + '.pq-table .pq-grow td{background:#dfe6ef;padding:0;border:1px solid #c3ceda}'
        + '.pq-grow-in{display:flex;align-items:center;gap:9px;padding:9px 11px}'
        + '.pq-grow-in .group-label{color:#0f172a;font-weight:800;font-size:12px}'
        + '.pq-grow-in .group-label i{font-size:17px;color:#16a34a}'
        + '.pq-footer{display:flex;justify-content:flex-end;gap:10px;padding:14px 2px 2px;margin-top:14px;border-top:1px solid #e5e7eb}'
        + '.pq-footer .v2-btn{height:40px;padding:0 22px;font-size:13px}'
        + '.pq-hint{color:#16a34a;cursor:help;font-size:15px;margin-left:5px;vertical-align:-2px}'
        + '.pq-item--chk{cursor:pointer}'
        + '.pq-chkbox{justify-self:end;display:inline-flex;align-items:center}'
        + '.pq-chkbox input{width:17px;height:17px;accent-color:#16a34a;cursor:pointer}'
        + '.pq-pf{display:flex;gap:8px;margin-bottom:12px;flex-wrap:wrap}'
        + '.pq-pf select{flex:1;min-width:150px}'
        /* tag loại quyền */
        + '.pq-tag{font-size:9px;font-weight:800;border-radius:5px;padding:1px 6px;text-transform:uppercase;flex:0 0 auto;white-space:nowrap}'
        + '.pq-tag--view{color:#15803d;background:#dcfce7;border:1px solid #bbf7d0}'
        + '.pq-tag--act{color:#475569;background:#f1f5f9;border:1px solid #e2e8f0}'
        + '.pq-tag--approve{color:#92400e;background:#fef3c7;border:1px solid #fde68a}'
        /* scope segmented */
        + '.pq-scope{display:flex;align-items:center;gap:7px;justify-self:end}'
        + '.pq-scope-lbl{font-size:10px;color:#94a3b8;text-transform:uppercase;letter-spacing:.03em;white-space:nowrap}'
        + '.pq-seg{display:inline-flex;flex-wrap:wrap;gap:3px;justify-content:flex-end}'
        + '.pq-seg button{border:1px solid #e5e7eb;background:#fff;border-radius:7px;font-family:inherit;font-size:11px;font-weight:600;color:#64748b;padding:4px 9px;cursor:pointer;transition:.12s}'
        + '.pq-seg button:hover{border-color:#86efac;color:#16a34a}'
        + '.pq-seg button.active{background:#16a34a;color:#fff;border-color:#16a34a}'
        + '.pq-seg .clr.active{background:#e2e8f0;color:#475569;border-color:#cbd5e1}'
        + '.pq-scope-sel{height:28px;border:1px solid #d1d5db;border-radius:7px;font-family:inherit;font-size:11.5px;font-weight:600;color:#334155;background:#fff;padding:0 8px;cursor:pointer;min-width:134px}'
        + '.pq-scope-sel:focus{outline:none;border-color:#16a34a;box-shadow:0 0 0 2px rgba(22,163,74,.15)}'
        + '.pq-scope-sel--on{border-color:#86efac;color:#15803d;background:#f0fdf4}'
        + '.pq-scope-sel--ap.pq-scope-sel--on{border-color:#fcd34d;color:#b45309;background:#fffbeb}'
        /* summary — tỷ lệ col-4, 1 cột */
        + '.pq-summary{position:sticky;top:calc(var(--topbar-h) + 12px)}'
        + '.pq-sumhead{display:flex;align-items:center;gap:10px;flex-wrap:wrap;padding-bottom:10px;border-bottom:1px solid #e5e7eb;margin-bottom:10px}'
        + '.pq-sumstat{display:flex;align-items:baseline;gap:7px}'
        + '.pq-sumstat b{font-size:23px;font-weight:800;color:#16a34a;line-height:1}'
        + '.pq-sumstat span{font-size:11.5px;color:#6b7280}'
        + '.pq-sumhead .sp{flex:1}'
        + '.pq-sumbtns{display:flex;gap:6px;width:100%}'
        + '.pq-sumchips{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:10px}'
        + '.pq-chip{display:inline-flex;align-items:center;gap:5px;font-size:11px;font-weight:600;padding:3px 9px;border-radius:999px;background:#f1f5f9;border:1px solid #e2e8f0;color:#334155;white-space:nowrap}'
        + '.pq-chip b{color:#15803d;font-weight:800}'
        + '.pq-sumlist{max-height:calc(100vh - 320px);overflow:auto;display:flex;flex-direction:column;gap:10px}'
        + '@media(max-width:1180px){.pq-summary{position:static}.pq-sumlist{max-height:none}}'
        + '.pq-info{border:1px solid #e5e7eb;border-radius:10px;background:#fff;overflow:hidden}'
        + '.pq-info__t{display:flex;align-items:center;gap:8px;font-size:12px;font-weight:700;color:#14532d;padding:8px 11px;background:#e6f4ec;border-bottom:1px solid #cfe0d6}'
        + '.pq-info__t .sp{flex:1}'
        + '.pq-info__b{padding:6px 11px 9px}'
        + '.pq-ksub{font-size:10px;font-weight:800;letter-spacing:.04em;text-transform:uppercase;color:#94a3b8;margin:7px 0 3px}'
        + '.pq-kv{display:flex;justify-content:space-between;align-items:center;gap:8px;padding:4px 0;border-bottom:1px dashed #eef2f6}'
        + '.pq-kv:last-child{border-bottom:0}'
        + '.pq-kv .kn{font-size:12px;color:#334155}'
        + '.pq-kv .kb{font-size:10px;font-weight:800;padding:2px 8px;border-radius:999px;white-space:nowrap;border:1px solid}'
        + '.kb-lv{color:#15803d;background:#dcfce7;border-color:#bbf7d0}'
        + '.kb-ap{color:#92400e;background:#fef3c7;border-color:#fde68a}'
        + '.kb-ac{color:#64748b;background:#f1f5f9;border-color:#e2e8f0}'
        + '.pq-empty{text-align:center;color:#94a3b8;font-size:12.5px;padding:30px 12px;border:1px dashed #e5e7eb;border-radius:10px}'
        + '.pq-empty i{font-size:30px;display:block;margin-bottom:8px;color:#cbd5e1}'
        + '.hidden{display:none!important}';
    var st = document.createElement('style');
    st.id = 'pq-style';
    st.textContent = css;
    document.head.appendChild(st);
}

function pqMount(html) {
    pqInjectStyle();
    document.body.innerHTML = '';
    renderShell('permission', html);
}
function pqEsc(s) { return (s || '').toLowerCase(); }
function pqSetHash(h) { try { history.replaceState(null, '', h || location.pathname); } catch (e) { location.hash = (h || '').replace(/^#/, ''); } }

/* Router: đọc hash khi load → giữ đúng màn sau reload (live-server) */
function pqRoute() {
    var m = (location.hash || '').match(/^#assign\/(.+)$/);
    if (m) pqOpenAssign(decodeURIComponent(m[1]), true);
    else renderPermissionsPage(true);
}

/* ======================= MÀN 1: DANH SÁCH CHỨC VỤ ======================= */
function renderPermissionsPage(silent) {
    if (!silent) pqSetHash('');
    var rows = PQ_ROLES.map(function (r, i) {
        var st = r.s === 'cancel'
            ? '<span class="status-pill st-cancel"><i class="ri-close-circle-line"></i> Khóa</span>'
            : '<span class="status-pill st-done"><i class="ri-checkbox-circle-line"></i> Hiệu lực</span>';
        return '<tr>'
            + '<td class="text-center">' + (i + 1) + '</td>'
            + '<td><div style="font-weight:600;color:#0f172a">' + r.n + '</div><div class="tp-small-text text-muted">' + r.d + '</div></td>'
            + '<td class="text-center"><button class="pq-permcount" onclick="pqShowRolePerms(\'' + r.n + '\')" title="Xem danh sách quyền đang có"><i class="ri-shield-keyhole-line"></i> ' + r.c + ' quyền <i class="ri-eye-line" style="opacity:.75"></i></button></td>'
            + '<td class="text-center">' + st + '</td>'
            + '<td>' + r.by + '</td>'
            + '<td class="text-center">' + r.at + '</td>'
            + '<td class="text-center"><div class="row-actions" style="opacity:1">'
            + '<button class="v2-icon-btn v2-icon-btn--sm" title="Phân quyền" onclick="pqOpenAssign(\'' + r.n + '\')"><i class="ri-key-2-line"></i></button>'
            + '<button class="v2-icon-btn v2-icon-btn--sm" title="Sửa"><i class="ri-edit-line"></i></button>'
            + '<button class="v2-icon-btn v2-icon-btn--sm" title="Lịch sử"><i class="ri-history-line"></i></button>'
            + '<button class="v2-icon-btn v2-icon-btn--sm v2-icon-btn--danger" title="Xóa"><i class="ri-delete-bin-6-line"></i></button>'
            + '</div></td></tr>';
    }).join('');

    var html = ''
        + '<section class="tp-card p-3 mb-2">'
        + '  <div class="filter-header">'
        + '    <div class="filter-header-left"><div class="tp-icon-chip"><i class="ri-filter-3-line"></i></div>'
        + '      <div><p class="tp-section-title">Bộ lọc chức vụ</p><p class="tp-section-subtitle">Tìm theo tên chức vụ, trạng thái</p></div></div>'
        + '  </div>'
        + '  <div class="quick-search-row">'
        + '    <div class="quick-search"><i class="ri-search-line"></i><input class="form-control form-control-sm" placeholder="Tìm chức vụ..."></div>'
        + '    <button class="v2-btn v2-btn--primary btn-compact"><i class="ri-search-line"></i> Tìm kiếm</button>'
        + '  </div>'
        + '</section>'
        + '<section class="tp-card p-3">'
        + '  <div class="table-card-header">'
        + '    <div class="filter-header-left"><div class="tp-icon-chip"><i class="ri-shield-keyhole-line"></i></div>'
        + '      <div><h5>Danh sách chức vụ</h5><p class="tp-section-subtitle">Nhấn <i class="ri-key-2-line"></i> để phân quyền cho từng chức vụ</p></div></div>'
        + '    <div class="table-actions">'
        + '      <button class="v2-btn v2-btn--sm v2-btn--secondary"><i class="ri-group-line"></i> Phân quyền hàng loạt</button>'
        + '      <button class="v2-btn v2-btn--sm v2-btn--secondary"><i class="ri-file-excel-2-line"></i> Xuất Excel</button>'
        + '      <button class="v2-btn v2-btn--sm v2-btn--primary-success"><i class="ri-add-line"></i> Thêm chức vụ</button>'
        + '    </div>'
        + '  </div>'
        + '  <div class="table-wrapper scrollbar-thin"><table class="data-table">'
        + '    <thead><tr>'
        + '      <th class="text-center" style="width:48px">STT</th><th>Chức vụ</th>'
        + '      <th class="text-center" style="width:160px">Quyền đang có</th>'
        + '      <th class="text-center" style="width:120px">Trạng thái</th><th style="width:140px">Người sửa</th>'
        + '      <th class="text-center" style="width:110px">Cập nhật</th><th class="text-center" style="width:150px">Thao tác</th>'
        + '    </tr></thead><tbody>' + rows + '</tbody>'
        + '  </table></div>'
        + '</section>'
        + '<div class="modal-backdrop-demo" id="pq-perm-modal"><div class="modal-dialog" style="max-width:660px">'
        + '  <div class="modal-header"><h5><span class="tp-icon-chip"><i class="ri-shield-keyhole-line"></i></span><span id="pq-perm-title">Quyền đang có</span></h5>'
        + '    <button type="button" class="close" onclick="closeModal(\'pq-perm-modal\')">×</button></div>'
        + '  <div class="modal-body" style="max-height:72vh;overflow:auto">'
        + '    <div class="pq-pf">'
        + '      <select class="form-control form-control-sm" id="pq-pf-sub" onchange="pqPopupSubChange()"></select>'
        + '      <select class="form-control form-control-sm" id="pq-pf-fn" onchange="pqRenderPopupBody()"></select>'
        + '      <select class="form-control form-control-sm" id="pq-pf-type" onchange="pqRenderPopupBody()"><option value="">— Tất cả loại —</option><option value="view">Xem</option><option value="act">Thao tác</option><option value="approve">Duyệt</option></select>'
        + '    </div>'
        + '    <div class="pq-sumchips" id="pq-pop-chips"></div>'
        + '    <div id="pq-perm-body"></div>'
        + '  </div>'
        + '  <div class="modal-footer"><button type="button" class="v2-btn v2-btn--sm v2-btn--tertiary" onclick="closeModal(\'pq-perm-modal\')"><i class="ri-close-line"></i> Đóng</button></div>'
        + '</div></div>';
    pqMount(html);
}

/* Popup danh sách quyền đang có của 1 chức vụ (demo: lấy theo bộ mặc định của cây quyền) */
function pqGrantedItems() {
    var arr = [];
    PQ_SUB.forEach(function (s) {
        s.groups.forEach(function (gr) {
            gr.views.forEach(function (v) { if (v.def !== '') arr.push({ sub: s.name, grp: gr.g, name: v.n, type: 'view', level: v.def }); });
            gr.acts.forEach(function (a) { if (a.on) arr.push({ sub: s.name, grp: gr.g, name: a.l, type: a.approve ? 'approve' : 'act', level: a.approve ? 'Công ty' : '' }); });
        });
    });
    return arr;
}
function pqPopupTag(t) {
    if (t === 'view') return '<span class="pq-tag pq-tag--view">Xem</span>';
    if (t === 'approve') return '<span class="pq-tag pq-tag--approve">Duyệt</span>';
    return '<span class="pq-tag pq-tag--act">Thao tác</span>';
}
function pqPopupSubChange() {
    var sv = document.getElementById('pq-pf-sub').value;
    var fns = pqUniq(pqGrantedItems().filter(function (i) { return !sv || i.sub === sv; }).map(function (i) { return i.grp; }));
    pqFill('pq-pf-fn', '— Tất cả chức năng —', fns);
    pqRenderPopupBody();
}
function pqRenderPopupBody() {
    var sv = document.getElementById('pq-pf-sub').value,
        fn = document.getElementById('pq-pf-fn').value,
        ty = document.getElementById('pq-pf-type').value;
    var items = pqGrantedItems().filter(function (i) {
        return (!sv || i.sub === sv) && (!fn || i.grp === fn) && (!ty || i.type === ty);
    });
    var html = '', chips = '';
    PQ_SUB.forEach(function (s) {
        var subItems = items.filter(function (i) { return i.sub === s.name; });
        if (!subItems.length) return;
        chips += '<span class="pq-chip">' + s.name + ' <b>' + subItems.length + '</b></span>';
        var inner = '';
        s.groups.forEach(function (gr) {
            var gi = subItems.filter(function (i) { return i.grp === gr.g; });
            if (!gi.length) return;
            inner += '<div class="pq-ksub">' + gr.g + '</div>';
            gi.forEach(function (i) {
                var badge = i.type === 'view' ? '<span class="kb kb-lv">' + i.level + '</span>' : (i.type === 'approve' ? '<span class="kb kb-ap">' + i.level + '</span>' : '');
                inner += '<div class="pq-kv"><span class="kn" style="display:flex;align-items:center;gap:6px">' + pqPopupTag(i.type) + i.name + '</span>' + badge + '</div>';
            });
        });
        html += '<div class="pq-info" style="margin-bottom:10px"><div class="pq-info__t"><i class="ri-stack-line" style="color:#16a34a"></i><span class="sp">' + s.name + '</span><span class="status-pill st-done">' + subItems.length + '</span></div><div class="pq-info__b">' + inner + '</div></div>';
    });
    document.getElementById('pq-pop-chips').innerHTML = chips;
    document.getElementById('pq-perm-body').innerHTML = html || '<div class="pq-empty"><i class="ri-inbox-line"></i>Không có quyền phù hợp bộ lọc.</div>';
}
function pqShowRolePerms(name) {
    document.getElementById('pq-perm-title').textContent = 'Quyền đang có — ' + name;
    document.getElementById('pq-pf-type').value = '';
    pqFill('pq-pf-sub', '— Tất cả phân hệ —', pqUniq(pqGrantedItems().map(function (i) { return i.sub; })));
    pqPopupSubChange();
    openModal('pq-perm-modal');
}

/* ======================= MÀN 2: PHÂN QUYỀN CHO CHỨC VỤ ======================= */
function pqOpenAssign(name, silent) {
    if (!silent) pqSetHash('#assign/' + encodeURIComponent(name));
    var html = ''
        + '<section class="tp-card p-3 mb-2 pq-banner">'
        + '  <div class="tp-icon-chip" style="width:34px;height:34px"><i class="ri-building-line"></i></div>'
        + '  <div style="flex:1">'
        + '    <div class="l1">Đang phân quyền cho chức vụ <u>' + name + '</u>'
        + '      <i class="ri-information-line pq-hint" title="Bạn chỉ phân quyền cho công ty của mình.&#10;• Quyền Xem có Phạm vi: chọn 1 cấp, cấp cao gồm cấp thấp.&#10;• Quyền Thao tác/Duyệt chỉ bật/tắt."></i></div>'
        + '  </div>'
        + '  <div class="pq-company"><i class="ri-building-4-line"></i><label>Công ty</label><b>' + PQ_MY_COMPANY + '</b></div>'
        + '  <a class="v2-btn v2-btn--sm v2-btn--tertiary" href="javascript:void(0)" onclick="renderPermissionsPage()"><i class="ri-arrow-left-line"></i> Danh sách</a>'
        + '</section>'
        + '<section class="tp-card p-3 mb-2">'
        + '  <div class="pq-filter1">'
        + '    <div class="pq-ff"><label class="tp-label">Nhóm phân hệ</label><select class="form-control form-control-sm" id="pq-f-grp" onchange="pqFilterGrp()"></select></div>'
        + '    <div class="pq-ff"><label class="tp-label">Phân hệ</label><select class="form-control form-control-sm" id="pq-f-sub" onchange="pqFilterSub()"></select></div>'
        + '    <div class="pq-ff"><label class="tp-label">Chức năng</label><select class="form-control form-control-sm" id="pq-f-fn" onchange="pqApplyFilter()"></select></div>'
        + '    <div class="pq-ff"><label class="tp-label">Loại quyền</label><select class="form-control form-control-sm" id="pq-f-type" onchange="pqApplyFilter()">'
        + '        <option value="">— Tất cả loại —</option><option value="view">Xem</option><option value="act">Thao tác</option><option value="approve">Duyệt</option></select></div>'
        + '    <div class="pq-ff" style="flex:1.5"><label class="tp-label">Tìm nhanh</label><div class="quick-search"><i class="ri-search-line"></i><input class="form-control form-control-sm" id="pq-search" placeholder="Tìm quyền theo tên..." oninput="pqApplyFilter()"></div></div>'
        + '    <button class="v2-btn v2-btn--sm v2-btn--tertiary" style="flex:0 0 auto" onclick="pqResetFilter()"><i class="ri-refresh-line"></i> Xóa lọc</button>'
        + '  </div>'
        + '</section>'
        + '<div class="pq-grid">'
        + '  <section class="tp-card p-3">'
        + '    <div class="table-card-header"><div class="filter-header-left"><div class="tp-icon-chip"><i class="ri-git-branch-line"></i></div>'
        + '      <div><h5>Cây quyền</h5><p class="tp-section-subtitle">Tick quyền cần cấp cho chức vụ</p></div></div>'
        + '      <div class="table-actions">'
        + '        <button class="v2-btn v2-btn--sm v2-btn--secondary" onclick="pqToggleAll(true)"><i class="ri-arrow-down-s-line"></i> Mở tất cả</button>'
        + '        <button class="v2-btn v2-btn--sm v2-btn--secondary" onclick="pqToggleAll(false)"><i class="ri-arrow-up-s-line"></i> Thu gọn</button>'
        + '      </div></div>'
        + '    <div id="pq-tree"></div>'
        + '  </section>'
        + '  <section class="tp-card p-3 pq-summary">'
        + '    <div class="pq-sumhead">'
        + '      <div class="tp-icon-chip"><i class="ri-list-check-2"></i></div>'
        + '      <div class="pq-sumstat"><b id="pq-total">0</b><span>quyền đã phân</span></div>'
        + '    </div>'
        + '    <div class="pq-sumchips" id="pq-sumchips"></div>'
        + '    <div class="pq-sumlist" id="pq-sumlist"></div>'
        + '  </section>'
        + '</div>'
        + '<div class="pq-footer"><button class="v2-btn v2-btn--primary-success" onclick="pqSave()"><i class="ri-save-3-line"></i> Lưu phân quyền</button></div>';
    pqMount(html);
    pqRenderTree();
    pqInitFilter();
}

/* mỗi quyền = 1 dòng .pq-item[data-type] ; trong nhóm xếp theo loại: Xem → Thao tác → Duyệt */
/* Dòng quyền có phạm vi (Xem hoặc Duyệt) — dùng select cấp */
function pqScopeRow(nm, levels, def, isApprove, gname, sname) {
    var type = isApprove ? 'approve' : 'view';
    var tag = isApprove ? '<span class="pq-tag pq-tag--approve">Duyệt</span>' : '<span class="pq-tag pq-tag--view">Xem</span>';
    var opts = '<option value=""' + (def === '' ? ' selected' : '') + '>— Không ' + (isApprove ? 'duyệt' : 'xem') + ' —</option>';
    levels.forEach(function (lv) {
        opts += '<option value="' + lv + '"' + (def === lv ? ' selected' : '') + '>' + lv + '</option>';
    });
    var cls = 'pq-scope-sel' + (isApprove ? ' pq-scope-sel--ap' : '') + (def !== '' ? ' pq-scope-sel--on' : '');
    return '<tr class="pq-item" data-type="' + type + '" data-s="' + pqEsc(nm + ' ' + gname + ' ' + sname) + '">'
        + '<td class="pq-c-type">' + tag + '</td>'
        + '<td class="pq-c-name"><span class="pq-nm">' + nm + '</span></td>'
        + '<td class="pq-c-scope"><select class="' + cls + '" onchange="pqScopeChange(this)">' + opts + '</select></td></tr>';
}
function pqViewRow(v, gname, sname) { return pqScopeRow(v.n, v.levels, v.def, false, gname, sname); }
function pqActRow(a, gname, sname) {
    return '<tr class="pq-item pq-item--chk" data-type="act" data-s="' + pqEsc(a.l + ' ' + gname + ' ' + sname) + '">'
        + '<td class="pq-c-type"><span class="pq-tag pq-tag--act">Thao tác</span></td>'
        + '<td class="pq-c-name"><span class="pq-nm">' + a.l + '</span></td>'
        + '<td class="pq-c-scope"><input type="checkbox" class="pq-chkbox2" ' + (a.on ? 'checked' : '') + ' onchange="pqRecount()"></td></tr>';
}

function pqRenderTree() {
    var wrap = document.getElementById('pq-tree'); wrap.innerHTML = '';
    var bulkBtns = '<button class="pq-link" onclick="event.stopPropagation();pqBulkSub({SI},true)"><i class="ri-checkbox-multiple-line"></i> Chọn cả</button>'
        + '<button class="pq-link pq-link--off" onclick="event.stopPropagation();pqBulkSub({SI},false)"><i class="ri-checkbox-blank-line"></i> Bỏ</button>';
    PQ_SUB.forEach(function (s, si) {
        var tbodies = '';
        s.groups.forEach(function (gr) {
            var rows = '';
            gr.views.forEach(function (v) { rows += pqViewRow(v, gr.g, s.name); });
            gr.acts.filter(function (a) { return !a.approve; }).forEach(function (a) { rows += pqActRow(a, gr.g, s.name); });
            gr.acts.filter(function (a) { return a.approve; }).forEach(function (a) { rows += pqScopeRow(a.l, PQ_LEVELS, a.on ? 'Công ty' : '', true, gr.g, s.name); });
            var nView = gr.views.length,
                nAct = gr.acts.filter(function (a) { return !a.approve; }).length,
                nAp = gr.acts.filter(function (a) { return a.approve; }).length;
            tbodies += '<tbody class="pq-group" data-fn="' + pqEsc(gr.g) + '">'
                + '<tr class="pq-grow"><td colspan="3"><div class="pq-grow-in">'
                + '<span class="group-label"><i class="ri-folder-2-fill"></i>' + gr.g + '</span>'
                + '<span class="pq-count">' + nView + ' xem · ' + nAct + ' thao tác · ' + nAp + ' duyệt</span><span class="pq-ghd-sp"></span>'
                + '<button class="pq-link" onclick="pqBulkGrp(this,true)"><i class="ri-checkbox-multiple-line"></i> Chọn cả</button>'
                + '<button class="pq-link pq-link--off" onclick="pqBulkGrp(this,false)"><i class="ri-checkbox-blank-line"></i> Bỏ</button>'
                + '</div></td></tr>' + rows + '</tbody>';
        });
        var body = '<table class="data-table pq-table"><thead><tr>'
            + '<th style="width:84px">Loại</th><th>Tên quyền</th><th class="text-right" style="width:190px">Phạm vi</th>'
            + '</tr></thead>' + tbodies + '</table>';
        wrap.innerHTML += '<div class="pq-sub ' + (s.open ? '' : 'collapsed') + '" data-si="' + si + '" data-grp="' + pqEsc(s.grp) + '" data-sub="' + pqEsc(s.name) + '">'
            + '<div class="pq-sub__hd" onclick="pqToggleSub(this)"><i class="ri-arrow-down-s-line pq-chev"></i>'
            + '<span class="tp-badge">' + s.grp + '</span><span class="pq-sub__name">' + s.name + '</span><span class="pq-sub__sp"></span>'
            + bulkBtns.replace(/\{SI\}/g, si)
            + '</div><div class="pq-sub__bd">' + body + '</div></div>';
    });
    pqRecount();
}

/* ---------- tương tác ---------- */
function pqScopeChange(sel) { sel.classList.toggle('pq-scope-sel--on', sel.value !== ''); pqRecount(); }
function pqToggleSub(h) { h.parentNode.classList.toggle('collapsed'); }
function pqToggleAll(open) { document.querySelectorAll('.pq-sub').forEach(function (s) { s.classList.toggle('collapsed', !open); }); }
function pqSetRegion(el, on) {
    el.querySelectorAll('.pq-scope-sel').forEach(function (sel) {
        sel.value = on ? (sel.options[1] ? sel.options[1].value : '') : '';
        sel.classList.toggle('pq-scope-sel--on', sel.value !== '');
    });
    el.querySelectorAll('.pq-item input[type=checkbox]').forEach(function (c) { c.checked = on; });
}
function pqBulkGrp(btn, on) { pqSetRegion(btn.closest('.pq-group'), on); pqRecount(); }
function pqBulkSub(si, on) { pqSetRegion(document.querySelector('.pq-sub[data-si="' + si + '"]'), on); pqRecount(); }
function pqClearAll() { document.querySelectorAll('.pq-sub').forEach(function (s) { pqSetRegion(s, false); }); pqRecount(); toast('Đã bỏ toàn bộ quyền (demo)', 'warning'); }

function pqCountRegion(el) {
    var n = 0;
    el.querySelectorAll('.pq-item .pq-scope-sel').forEach(function (s) { if (s.value !== '') n++; });
    n += el.querySelectorAll('.pq-item input[type=checkbox]:checked').length; return n;
}
function pqRecount() {
    var total = 0;
    PQ_SUB.forEach(function (s, si) { total += pqCountRegion(document.querySelector('.pq-sub[data-si="' + si + '"]')); });
    document.getElementById('pq-total').textContent = total; pqBuildSummary();
}
function pqBuildSummary() {
    var html = '', chips = '';
    PQ_SUB.forEach(function (s, si) {
        var sub = document.querySelector('.pq-sub[data-si="' + si + '"]');
        var cnt = pqCountRegion(sub); if (!cnt) return;
        chips += '<span class="pq-chip">' + s.name + ' <b>' + cnt + '</b></span>';
        var inner = '';
        sub.querySelectorAll('.pq-group').forEach(function (grp) {
            var items = '';
            grp.querySelectorAll('.pq-item').forEach(function (r) {
                var type = r.getAttribute('data-type');
                if (type === 'view' || type === 'approve') {
                    var sel = r.querySelector('.pq-scope-sel');
                    if (sel && sel.value !== '') {
                        items += '<div class="pq-kv"><span class="kn">' + r.querySelector('.pq-nm').textContent.trim() + '</span><span class="kb ' + (type === 'approve' ? 'kb-ap' : 'kb-lv') + '">' + sel.value + '</span></div>';
                    }
                } else {
                    var c = r.querySelector('input[type=checkbox]');
                    if (c && c.checked) {
                        items += '<div class="pq-kv"><span class="kn">' + r.querySelector('.pq-nm').textContent.trim() + '</span><span class="kb kb-ac">Thao tác</span></div>';
                    }
                }
            });
            if (items) inner += '<div class="pq-ksub">' + grp.querySelector('.group-label').textContent.trim() + '</div>' + items;
        });
        html += '<div class="pq-info"><div class="pq-info__t"><i class="ri-stack-line" style="color:#16a34a"></i><span class="sp">' + s.name + '</span><span class="status-pill st-done">' + cnt + '</span></div><div class="pq-info__b">' + inner + '</div></div>';
    });
    document.getElementById('pq-sumchips').innerHTML = chips;
    document.getElementById('pq-sumlist').innerHTML = html || '<div class="pq-empty"><i class="ri-inbox-line"></i>Chưa phân quyền nào.<br>Chọn phạm vi Xem hoặc bật quyền thao tác/duyệt bên trái.</div>';
}

/* ---------- bộ lọc phân tầng + loại quyền ---------- */
function pqUniq(a) { return a.filter(function (v, i) { return a.indexOf(v) === i; }); }
function pqFill(id, all, arr) { document.getElementById(id).innerHTML = '<option value="">' + all + '</option>' + arr.map(function (x) { return '<option>' + x + '</option>'; }).join(''); }
function pqInitFilter() { pqFill('pq-f-grp', '— Tất cả nhóm phân hệ —', pqUniq(PQ_SUB.map(function (s) { return s.grp; }))); pqFilterGrp(); }
function pqFilterGrp() { var g = document.getElementById('pq-f-grp').value; pqFill('pq-f-sub', '— Tất cả phân hệ —', pqUniq(PQ_SUB.filter(function (s) { return !g || s.grp === g; }).map(function (s) { return s.name; }))); pqFilterSub(); }
function pqFilterSub() { var g = document.getElementById('pq-f-grp').value, sv = document.getElementById('pq-f-sub').value; var fns = []; PQ_SUB.forEach(function (s) { if ((!g || s.grp === g) && (!sv || s.name === sv)) s.groups.forEach(function (gr) { fns.push(gr.g); }); }); pqFill('pq-f-fn', '— Tất cả chức năng —', pqUniq(fns)); pqApplyFilter(); }
function pqResetFilter() {
    document.getElementById('pq-f-grp').value = ''; document.getElementById('pq-f-type').value = '';
    document.getElementById('pq-search').value = ''; pqFilterGrp();
}
function pqApplyFilter() {
    var g = document.getElementById('pq-f-grp').value, sv = document.getElementById('pq-f-sub').value,
        fn = document.getElementById('pq-f-fn').value, ty = document.getElementById('pq-f-type').value,
        q = (document.getElementById('pq-search').value || '').trim().toLowerCase();
    document.querySelectorAll('.pq-sub').forEach(function (sub) {
        var okSub = (!g || sub.getAttribute('data-grp') === pqEsc(g)) && (!sv || sub.getAttribute('data-sub') === pqEsc(sv)); var anySub = false;
        sub.querySelectorAll('.pq-group').forEach(function (grp) {
            var okFn = okSub && (!fn || grp.getAttribute('data-fn') === pqEsc(fn)); var anyGrp = false;
            grp.querySelectorAll('.pq-item').forEach(function (r) {
                var hit = okFn && (!ty || r.getAttribute('data-type') === ty) && (!q || r.getAttribute('data-s').indexOf(q) > -1);
                r.classList.toggle('hidden', !hit); if (hit) anyGrp = true;
            });
            grp.classList.toggle('hidden', !anyGrp); if (anyGrp) anySub = true;
        });
        sub.classList.toggle('hidden', !anySub);
        if ((q || fn || sv || ty) && anySub) sub.classList.remove('collapsed');
    });
}

function pqSave() { toast('Đã lưu phân quyền cho ' + PQ_MY_COMPANY + ' (demo — không ghi dữ liệu thật)', ''); }

/* Back/forward hoặc chỉnh URL hash → điều hướng lại đúng màn */
window.addEventListener('hashchange', pqRoute);
