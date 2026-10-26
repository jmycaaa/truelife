// Renders every <section class="slide" id="sN"> in an HTML file to <prefix>_sN.png at 1080x1350.
const {chromium}=require('playwright');
(async()=>{const [file,prefix]=process.argv.slice(2);const b=await chromium.launch();
const p=await b.newPage({viewport:{width:1080,height:1350}});
await p.goto('file://'+file,{waitUntil:'networkidle'});await p.evaluate(()=>document.fonts.ready);
for(const id of await p.$$eval('section.slide',s=>s.map(x=>x.id))){await (await p.$('#'+id)).screenshot({path:`${prefix}_${id}.png`});}
await b.close();})();
