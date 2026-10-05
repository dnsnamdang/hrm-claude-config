from common import *
with browser_page() as page:
    page.goto(BASE+'/assign/solutions', wait_until='domcontentloaded'); page.wait_for_timeout(15000)
    print(page.evaluate("""()=>JSON.stringify((window.$nuxt.$store.state.employeeOptions||[]).filter(e=>e.department_id==55).map(e=>[e.id,e.text,e.working_position_name]))"""))
