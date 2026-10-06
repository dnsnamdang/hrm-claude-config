from solfill import *
with browser_page() as page:
    page.goto(BASE+'/assign/solutions/add?prospective_project_id=151'); page.wait_for_timeout(15000)
    fill_solution(page)
    page.screenshot(path='sol_fill2.png', full_page=True)
