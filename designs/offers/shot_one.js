const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350}});
for(const f of process.argv.slice(2)){await p.goto('file://'+process.cwd()+'/'+f,{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);
const ids=await p.$$eval('section.slide',s=>s.map(x=>x.id));const base='out/'+f.replace('.html','');
if(ids.length){for(const id of ids){await (await p.$('#'+id)).screenshot({path:`${base}_${id}.png`});}}else{await p.screenshot({path:`${base}_c1.png`});}}
await b.close();})();
