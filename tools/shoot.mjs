import { chromium } from 'playwright';
import fs from 'fs';
// 用法：npm i -D playwright && npx playwright install chromium && node tools/shoot.mjs（在仓库根目录）
const ROOT=new URL('..', import.meta.url);
const BASE=new URL('prototype/', ROOT).href;
const OUT=new URL('shots/', ROOT).pathname;
fs.mkdirSync(OUT,{recursive:true});
const M={width:390,height:844}, D={width:1440,height:900}, T={width:1024,height:768};
const S=[
 ['ui-01-home','ui-01-home.html',['m','d']],
 ['ui-02-lottery','ui-02-lottery.html#L001',['m','d']],
 ['ui-03-pick','ui-03-pick.html#L005',['m','d'],async p=>{await p.click('.tile[data-n="3"]');await p.click('#sh-pick');await p.click('.tile[data-n="5"]');await p.click('#sh-pick');}],
 ['ui-04-checkout','ui-04-checkout.html#L005-3-5',['m','d'],async p=>{await p.check('#agree');}],
 ['ui-05-my-slots','ui-05-my-slots.html#ready',['m','d']],
 ['ui-05-progress','ui-05-my-slots.html#p-L009',['m','d']],
 ['ui-07-recording','ui-07-recording.html#L011-t754',['m','d']],
 ['ui-08-result','ui-08-result.html#L011',['m','d']],
 ['ui-09-verify','ui-09-verify.html#L015',['m','d'],async p=>{await p.click('#run');await p.waitForSelector('.verdict',{timeout:15000});}],
 ['ui-10-collection','ui-10-collection.html#stored',['m','d']],
 ['ui-11-welcome','ui-11-welcome.html',['m','d']],
 ['ui-12-spending','ui-12-spending.html',['m','d']],
 ['ui-13-merchant-wizard','ui-13-merchant-wizard.html',['d'],async p=>{await p.click('[data-step="2"]');}],
 ['ui-14-station','ui-14-station.html',['t'],async p=>{await p.click('#scan');await p.click('#prep');await p.waitForTimeout(1000);await p.click('#c-rec');await p.click('#c-seal');await p.click('#go');for(let i=0;i<3;i++)await p.click('#add');}],
 ['ui-15-attribution','ui-15-attribution.html#L009',['d'],async p=>{await p.click('tr[data-row]');}],
 ['ui-16-warehouse','ui-16-warehouse.html#pack',['d'],async p=>{await p.press('#scan','Enter');await p.press('#scan','Enter');}],
 ['ui-17-dashboard','ui-17-dashboard.html',['d']],
];
const browser=await chromium.launch();
for(const [name,url,modes,act] of S){
  for(const m of modes){
    const vp=m==='m'?M:m==='t'?T:D;
    const ctx=await browser.newContext({viewport:vp,deviceScaleFactor:m==='m'?2:1,colorScheme:'light',locale:'ja-JP'});
    const p=await ctx.newPage();
    await p.goto(BASE+url,{waitUntil:'networkidle'});
    await p.evaluate(()=>document.fonts&&document.fonts.ready);
    if(act) await act(p);
    await p.waitForTimeout(400);
    const file=`${OUT}${name}-${m==='m'?'mobile':m==='t'?'tablet':'desktop'}.jpg`;
    await p.screenshot({path:file,type:'jpeg',quality:78,fullPage:m==='m'});
    console.log('ok',file.split('/').pop());
    await ctx.close();
  }
}
await browser.close();
