FIND = """(name) => { const out=[]; const walk=(vm)=>{ if(vm.$options.name===name) out.push(vm); vm.$children.forEach(walk)}; walk(window.$nuxt.$root); return out.length }"""
def vm_eval(page, name, body, arg=None):
    js = """([name, arg]) => { const out=[]; const walk=(vm)=>{ if(vm.$options.name===name) out.push(vm); vm.$children.forEach(walk)}; walk(window.$nuxt.$root); const vm=out[0]; if(!vm) return 'NOVM'; return (function(vm, arg){ %s })(vm, arg) }""" % body
    return page.evaluate(js, [name, arg])
