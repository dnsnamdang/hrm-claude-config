const fs=require('fs');const c=require('vue-template-compiler');const b=require('@babel/parser')
const files=fs.readFileSync(process.argv[2],'utf8').split(/\r?\n/).filter(Boolean)
let bad=0,ok=0
for(const f of files){const s=fs.readFileSync(f,'utf8');if(!s.trim())continue
 const sfc=c.parseComponent(s);try{
  if(sfc.template){const r=c.compile(sfc.template.content);if(r.errors.length)throw new Error(r.errors[0])}
  if(sfc.script){b.parse(sfc.script.content,{sourceType:'module',plugins:['jsx','optionalChaining','nullishCoalescingOperator','dynamicImport','classProperties']})
   const n=(sfc.script.content.match(/^\s*layout:\s*'subsystem'/mg)||[]).length; if(f.startsWith('pages/')&&n!==1) throw new Error('layout count '+n)}
  ok++}catch(e){bad++;console.log('ERR',f,String(e.message||e).slice(0,150))}}
for(const f of ['components/menu.js','components/default-menu/rice.js','components/subsystem-menu/hub.js'])b.parse(fs.readFileSync(f,'utf8'),{sourceType:'module',plugins:['optionalChaining']})
console.log('ok',ok,'bad',bad)
