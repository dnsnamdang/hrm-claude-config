from solfill import *
with browser_page() as page:
    page.goto(BASE+'/assign/solutions/add?prospective_project_id=151'); page.wait_for_timeout(15000)
    fill_solution(page)
    page.evaluate('window.scrollTo(0, 330)'); settle(page)
    page.screenshot(path=SH+'04_sol_add.png')
    tight(page, page.locator('button:has-text("Thêm nhân sự")'), IC+'btn_themnhansu.png')
    tight(page, page.locator('button:has-text("Lưu nháp")').first, IC+'btn_luunhap_gp.png')
    tight(page, page.locator('button:has-text("Lưu và gửi")').first, IC+'btn_luuvagui.png')
    resp=[]
    page.on('response', lambda r: resp.append((r.status, r.url, r.text()[:600])) if 'assign/solutions' in r.url and r.request.method=='POST' else None)
    page.locator('button:has-text("Lưu và gửi")').first.click(); page.wait_for_timeout(8000)
    for x in resp: print(x)
    print(page.url)
    page.screenshot(path='after_save.png')
