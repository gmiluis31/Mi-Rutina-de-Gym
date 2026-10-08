import sys,pathlib;sys.path.insert(0,str(pathlib.Path(__file__).parent))
import h
from h import reg,URL
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={"width":320,"height":800}); errs=[]
    pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.goto(URL); reg(pg); pg.click("#pno")
    print("sin ejercicios, botón deshabilitado:",pg.is_disabled("#reset"))
    for n in ("Press de banca","Sentadilla"):
        pg.fill("#n",n); pg.click("#nuevo button[type=submit]")
    pg.locator(".set").first.click()
    print("ejercicios:",pg.locator(".ex").count())
    pg.click("#reset"); print("1er toque:",pg.inner_text("#reset"),"| ejercicios:",pg.locator(".ex").count())
    pg.wait_for_timeout(4300); print("tras 4s:",pg.inner_text("#reset"),"| ejercicios:",pg.locator(".ex").count())
    pg.click("#reset"); pg.click("#reset"); pg.wait_for_timeout(100)
    print("2º toque -> ejercicios:",pg.locator(".ex").count(),"| aviso:",pg.inner_text("#toast"),"| botón:",pg.inner_text("#reset"),"| deshabilitado:",pg.is_disabled("#reset"))
    pg.reload(); pg.wait_for_timeout(200); print("tras recargar ejercicios:",pg.locator(".ex").count())
    print("errores",errs); b.close()
