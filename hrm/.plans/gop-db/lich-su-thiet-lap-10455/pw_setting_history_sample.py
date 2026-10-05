import json, urllib.request, sys, time
from playwright.sync_api import sync_playwright
S='/tmp'
req=urllib.request.Request('http://127.0.0.1:8000/api/v1/users/auth/login',data=json.dumps({'email':'namdangit@gmail.com','password':'2025Dns@2'}).encode(),headers={'Content-Type':'application/json'})
tok=json.load(urllib.request.urlopen(req))['access_token']
res=[]
def ok(name,cond,extra=''):
    res.append((name,bool(cond),extra)); print(('PASS' if cond else 'FAIL'),name,extra,flush=True)
SEC="document.querySelector('.modal.show .system-info-section').__vue__"
def section_state(page):
    return page.evaluate(f"(()=>{{const v={SEC};return {{items:v.items.length,filtered:v.filteredItems.length,performers:v.options.performers.length,actions:v.actionOptions.map(a=>a.text)}}}})()")
def setf(page, **kw):
    page.evaluate(f"(f)=>{{const v={SEC}; Object.assign(v.filters,f); if(v.applyFilter) v.applyFilter(); }}", kw)
    page.wait_for_timeout(400)
    return page.evaluate(f"{SEC}.filteredItems.map(l=>l.action_label)")
def reset(page):
    page.evaluate(f"{SEC}.resetFilters()"); page.wait_for_timeout(300)
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':1440,'height':900}); page=ctx.new_page()
    errs=[]; page.on('console', lambda m: errs.append(m.text) if m.type=='error' else None)
    bad=[]; page.on('response', lambda r: bad.append((r.status,r.url)) if 'setting-histories' in r.url and r.status>=400 else None)
    page.goto('http://127.0.0.1:3000/login',wait_until='domcontentloaded')
    page.evaluate("t=>localStorage.setItem('access_token',t)",tok)
    # ===== Quy định chung
    page.goto('http://127.0.0.1:3000/timesheet/setting/general',wait_until='domcontentloaded')
    page.get_by_role('button',name='Lịch sử thay đổi').first.wait_for(timeout=60000)
    page.wait_for_timeout(1500)
    page.get_by_role('button',name='Lịch sử thay đổi').first.click()
    page.locator('.modal.show .system-info-section').wait_for(timeout=20000)
    page.wait_for_timeout(2000)
    title=page.locator('.modal.show .modal-title').first.inner_text()
    ok('GR: tiêu đề', 'Lịch sử thay đổi: Quy định chung' in title, title)
    body=page.locator('.modal.show .modal-body').inner_text()
    ok('GR: log cũ hiện', 'Cập nhật quy định chung' in body and 'Nghỉ tuần' in body and 'Chủ Nhật' in body and 'Thứ 7 và CN' in body)
    ok('GR: người thực hiện', 'Người thực hiện: DNS Admin' in body)
    page.locator('.modal.show').get_by_role('button',name='Bộ lọc').click(); page.wait_for_timeout(600)
    fb=page.locator('.modal.show .si-filter-bar').inner_text()
    ok('GR: nhãn bộ lọc', all(x in fb for x in ['Loại hành động','Người thực hiện','Từ ngày','Đến ngày','Làm mới']), fb.replace('\n',' | '))
    st=section_state(page); ok('GR: 3 nhóm + performers', st['actions']==['Tạo mới','Thay đổi thông tin','Thay đổi trạng thái'] and st['performers']>100, str(st))
    ok('GR: nút Đóng', page.locator('.modal.show .modal-footer').get_by_text('Đóng').count()>0)
    page.screenshot(path=S+'/gr_popup.png')
    page.locator('.modal.show .modal-footer').get_by_text('Đóng').click(); page.wait_for_timeout(800)
    # đổi 1 trường thật: Khoảng cách chấm công tối đa 200 -> 1500
    inp=page.locator('label:has-text("Khoảng cách chấm công tối đa") input[type=number]').first
    inp.fill('1500'); inp.blur(); page.wait_for_timeout(2500)
    page.get_by_role('button',name='Lịch sử thay đổi').first.click()
    page.locator('.modal.show .system-info-section').wait_for(timeout=20000); page.wait_for_timeout(2000)
    first=page.locator('.modal.show .ho-timeline-item, .modal.show li').first.inner_text()
    ok('GR: dòng mới đúng', 'Khoảng cách chấm công tối đa (m)' in first and '200' in first and '1,500' in first, first.replace('\n',' | '))
    ok('GR: lọc status rỗng', setf(page, action='status')==[] )
    ok('GR: lọc update', len(setf(page, action='update'))>=2 )
    reset(page)
    ok('GR: lọc người 13', len(setf(page, performer=13))>=2 ); reset(page)
    ok('GR: lọc người khác', setf(page, performer=211)==[] ); reset(page)
    ok('GR: lọc từ ngày mai', setf(page, dateFrom='2026-10-01')==[] ); reset(page)
    ok('GR: lọc hôm nay', len(setf(page, dateFrom='2026-09-30', dateTo='2026-09-30'))>=2 ); reset(page)
    # select2 thật: chọn "Thay đổi trạng thái"
    page.locator('.modal.show').get_by_role('button',name='Bộ lọc').click(); page.wait_for_timeout(500)
    page.locator('.modal.show .si-filter-bar .select2-selection').first.click(); page.wait_for_timeout(400)
    page.locator('.select2-results__option', has_text='Thay đổi trạng thái').first.click(); page.wait_for_timeout(600)
    ok('GR: select2 lọc status -> rỗng', 'Không có lịch sử phù hợp bộ lọc' in page.locator('.modal.show .modal-body').inner_text())
    page.screenshot(path=S+'/gr_popup_filter.png')
    page.locator('.modal.show .modal-footer').get_by_text('Đóng').click(); page.wait_for_timeout(800)
    inp.fill('200'); inp.blur(); page.wait_for_timeout(2500)
    # ===== Loại nghỉ
    page.goto('http://127.0.0.1:3000/timesheet/setting/holiday',wait_until='domcontentloaded')
    page.get_by_role('tab',name='Loại nghỉ').wait_for(timeout=60000); page.wait_for_timeout(1500)
    page.get_by_role('tab',name='Loại nghỉ').click(); page.wait_for_timeout(2500)
    row=page.locator('tr', has_text='T10455').first
    row.locator('.dropdown-toggle, button').first.click(); page.wait_for_timeout(500)
    row.get_by_text('Lịch sử thay đổi').click()
    page.locator('.modal.show .system-info-section').wait_for(timeout=20000); page.wait_for_timeout(2000)
    title=page.locator('.modal.show .modal-title').first.inner_text()
    ok('LT: tiêu đề', 'Lịch sử thay đổi: T10455 - LT test 10455' in title, title)
    labels=page.evaluate(f"{SEC}.items.map(l=>l.action_label+'|'+l.action_group)")
    ok('LT: 4 dòng mới->cũ', labels==['Mở khóa loại nghỉ|status','Khóa loại nghỉ|status','Cập nhật loại nghỉ|update','Thêm loại nghỉ|create'], str(labels))
    body=page.locator('.modal.show .modal-body').inner_text()
    ok('LT: giá trị', all(x in body for x in ['Nghỉ không lương','Nghỉ hưởng BHXH','75.5','Ghi chú thử','Hoạt động','Khóa','1,500']))
    ok('LT: lọc status', setf(page, action='status')==['Mở khóa loại nghỉ','Khóa loại nghỉ']); reset(page)
    ok('LT: lọc create', setf(page, action='create')==['Thêm loại nghỉ']); reset(page)
    ok('LT: lọc update', setf(page, action='update')==['Cập nhật loại nghỉ']); reset(page)
    st=section_state(page); ok('LT: performers', st['performers']>100, str(st))
    page.screenshot(path=S+'/lt_popup.png', full_page=False)
    page.locator('.modal.show').get_by_role('button',name='Bộ lọc').click(); page.wait_for_timeout(500)
    page.screenshot(path=S+'/lt_popup_filter.png')
    ok('Không lỗi 4xx setting-histories', not bad, str(bad))
    ok('Console errors', not [e for e in errs if 'setting' in e.lower() or 'SystemInfo' in e], str(errs[:5]))
    b.close()
print('SUMMARY', sum(1 for r in res if r[1]), '/', len(res))
