import sys,pathlib;sys.path.insert(0,str(pathlib.Path(__file__).parent))
import h
from h import reg,URL
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={"width":360,"height":800}); errs=[]
    pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.goto(URL); reg(pg); pg.click("#pno"); pg.click("[data-t=ppl]"); pg.locator(".day").nth(0).click(); pg.wait_for_timeout(200)
    r=pg.evaluate("""()=>[...document.querySelectorAll('button,select')].filter(e=>e.offsetParent&&!e.closest('[hidden]')).map(e=>{const r=e.getBoundingClientRect();return [(e.id||e.className||e.tagName),Math.round(r.width),Math.round(r.height)]}).filter(x=>x[1]<44||x[2]<44)""")
    print("controles menores de 44px:",r); print("errores",errs)
    pg.evaluate("scrollTo(0,0)"); pg.screenshot(path="/tmp/m1.png"); b.close()
