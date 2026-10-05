from common import *
with browser_page() as page:
    page.goto(BASE+'/assign/solutions/955/edit?mode=approve', wait_until='domcontentloaded'); page.wait_for_timeout(25000)
    print(page.evaluate("""()=>{const s=window.$nuxt.$store.state; const o=s.employeeOptions||[]; return [o.length, JSON.stringify(o.filter(e=>e.id==13||e.id==781)), JSON.stringify(s.current_employee&&{id:s.current_employee.id}), s.current_company_role]}"""))
