import sys,pathlib;sys.path.insert(0,str(pathlib.Path(__file__).parent))
import h
from h import reg,URL
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={"width":360,"height":740}); errs=[]
    pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.goto(URL); reg(pg); pg.click("#pno")
    pg.fill("#n","Press de banca"); pg.fill("#s","2"); pg.click("#nuevo button[type=submit]")
    print("visible antes:",pg.is_visible("#rest"))
    pg.locator(".set").first.click()
    print("visible:",pg.is_visible("#rest"),pg.inner_text("#rn"),pg.inner_text("#rl"))
    pg.click("#rmas"); print("+15:",pg.inner_text("#rn"))
    pg.click("#rmenos"); pg.click("#rmenos"); print("-30:",pg.inner_text("#rn"))
    pg.evaluate("rEnd=Date.now()+1500"); pg.wait_for_timeout(2300)
    print("fin:",pg.inner_text("#rn"),"|",pg.inner_text("#rl"))
    pg.click("#romitir"); print("omitido, visible:",pg.is_visible("#rest"))
    pg.locator(".set").nth(1).click(); pg.wait_for_timeout(100)
    print("día completo -> timer visible:",pg.is_visible("#rest"),"| aviso:",pg.inner_text("#toast"))
    pg.locator(".set").nth(1).click(); pg.locator(".set").nth(1).click()
    pg.click("#cfg"); pg.select_option("#pd","0"); pg.click("#pno"); pg.locator(".set").nth(1).click()
    print("con 'sin temporizador', visible:",pg.is_visible("#rest"))
    pg.reload(); pg.wait_for_timeout(200); print("persistió descanso:",pg.evaluate("st.descanso"))
    print("errores",errs); b.close()
