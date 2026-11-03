// lê jobs.json [{svg, out, w, h, transparent}] e renderiza com chromium
const { chromium } = require('playwright'); const fs=require('fs');
(async()=>{const jobs=JSON.parse(fs.readFileSync(process.argv[2]));const b=await chromium.launch();const p=await b.newPage();
for(const j of jobs){await p.setViewportSize({width:j.w,height:j.h});
await p.setContent(`<html><body style="margin:0;background:transparent">${j.svg}</body></html>`);
await p.screenshot({path:j.out,clip:{x:0,y:0,width:j.w,height:j.h},omitBackground:!!j.transparent});}
await b.close();})();
