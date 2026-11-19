# Rebuild the tab bar of a space screen: 5 fixed tabs + "Thêm" menu + Trao đổi button on the right.
import re

MAIN = [('overview', 'Tổng quan', 'ri-dashboard-line'), ('tasks', 'Nhiệm vụ', 'ri-task-line'),
        ('issues', 'Vấn đề', 'ri-bug-line'), ('meetings', 'Meeting', 'ri-calendar-event-line'),
        ('files', 'File', 'ri-folder-3-line')]
MEMBERS = ('members', 'Thành viên', 'ri-team-line')
SETTINGS = ('settings', 'Cấu hình', 'ri-settings-3-line')
PROJECTS = ('projects', 'Dự án nội bộ', 'ri-folders-line')
MENU = {
    # Phòng làm việc: có Dự án nội bộ thuộc phòng
    'room': [(None, [MEMBERS, PROJECTS, SETTINGS])],
    # Dự án nội bộ: không có cấp con
    'iproj': [(None, [MEMBERS, SETTINGS])],
    'gp': [('Giải pháp', [('modules', 'Hạng mục', 'ri-stack-line'), ('info', 'Thông tin giải pháp', 'ri-information-line'),
                          ('profiles', 'Hồ sơ', 'ri-folder-user-line'), ('progress', 'Tiến độ', 'ri-line-chart-line'),
                          ('adjust', 'Yêu cầu điều chỉnh', 'ri-edit-box-line', '2')]),
           ('Quản lý', [MEMBERS, SETTINGS])],
    'tkt': [('Tiền khả thi', [('info', 'Thông tin dự án', 'ri-information-line'), ('collect', 'Thu thập thông tin', 'ri-survey-line'),
                              ('req', 'Yêu cầu', 'ri-file-list-3-line'), ('sol', 'Giải pháp', 'ri-lightbulb-line'),
                              ('profiles', 'Hồ sơ', 'ri-folder-user-line'), ('quote', 'Báo giá', 'ri-price-tag-3-line'),
                              ('ext', 'Gia hạn', 'ri-time-line')]),
            ('Quản lý', [MEMBERS, SETTINGS])],
}
DV = 'data-v-b87c17de=""'


def btn(key, label, icon, active=False, badge=None, extra='', caret=False):
    b = ('<span class="mk-tab-badge">%s</span>' % badge) if badge else ''
    c = ' <i %s class="ri-arrow-down-s-line mk-caret"></i>' % DV if caret else ''
    return ('<button %s type="button" class="v2-btn v2-btn--sm v2-btn--quaternary v2-btn--quaternary-info tab-btn-root%s%s" data-key="%s">'
            '<!----> <i %s class="%s tab-icon"></i><span %s class="tab-label">%s</span>%s%s <!----></button>') % (
        DV, ' active' if active else '', extra, key, DV, icon, DV, label, b, c)


def retab(body, kind, active, open_menu=False, chat_badge='12'):
    body = re.sub(r'<!--mk-tabs-->.*?<!--/mk-tabs-->', '', body, flags=re.S)
    root = body.find('class="tabs-root"')
    if root < 0:
        return body
    st = body.find('<button', root)
    en = body.find('</div> <button %s type="button" aria-label="Xem các tab phía trước"' % DV, st)
    groups = MENU[kind]
    items = [it for _, its in groups for it in its]
    sel = next((it for it in items if it[0] == active), None)
    html = ''.join(btn(k, l, i, k == active) for k, l, i in MAIN)
    if sel:
        html += btn('more', sel[1], sel[2], True, extra=' mk-more-btn', caret=True)
    else:
        html += btn('more', 'Thêm', 'ri-apps-2-line', False, extra=' mk-more-btn' + (' mk-open' if open_menu else ''), caret=True)
    body = body[:st] + html + body[en:]
    # menu + chat button: before closing </div> of surface-hd
    nx = body.find('tabs-arrow--next', root)
    p = body.find('</button>', nx) + len('</button>')
    assert body[p:p + 12] == '</div></div>', body[p:p + 40]
    p += 12
    menu = ''
    for title, its in groups:
        if title:
            menu += '<div class="mk-more-h">%s</div>' % title
        for it in its:
            k, l, i = it[:3]
            bd = ('<span class="mk-more-badge">%s</span>' % it[3]) if len(it) > 3 else ''
            menu += '<a class="mk-more-it%s"><i class="%s"></i><span>%s</span>%s</a>' % (' on' if k == active else '', i, l, bd)
    add = ('<!--mk-tabs--><div class="mk-more-menu"%s>%s</div>'
           '<div class="mk-chat-slot">%s</div>'
           '<script>(function(){var h=document.currentScript.parentElement,b=h.querySelector(".mk-more-btn"),m=h.querySelector(".mk-more-menu");'
           'function pos(){var r=b.getBoundingClientRect(),hr=h.getBoundingClientRect();m.style.left=(r.left-hr.left)+"px";m.style.top=(r.bottom-hr.top+4)+"px";}'
           'pos();b.addEventListener("click",function(){pos();m.style.display=m.style.display==="block"?"none":"block";});'
           'document.addEventListener("click",function(e){if(!b.contains(e.target)&&!m.contains(e.target))m.style.display="none";});})();</script><!--/mk-tabs-->') % (
        ' style="display:block"' if open_menu else '', menu,
        btn('chat', 'Trao đổi', 'ri-chat-3-line', active == 'chat', chat_badge, extra=' mk-chat-btn'))
    return body[:p] + add + body[p:]
