import sys,pathlib;sys.path.insert(0,str(pathlib.Path(__file__).parent))
import h
from h import reg,URL
from playwright.sync_api import sync_playwright
U=URL
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={"width":390,"height":844}); pg=ctx.new_page(); errs=[]
    pg.on("pageerror",lambda e:errs.append(str(e)))
    pg.goto(U); pg.wait_for_timeout(300)
    print("1) pantalla de registro:",pg.inner_text("#gtit"),"| visible:",pg.is_visible("#gate"))
    pg.screenshot(path="/tmp/g1.png")
    pg.click("#gok"); print("2) vacío ->",pg.inner_text("#gerr"))
    pg.fill("#gn","Ana"); pg.fill("#ge","mal"); pg.fill("#gp","123456"); pg.fill("#gc","123456"); pg.click("#gok"); print("3) correo inválido ->",pg.inner_text("#gerr"))
    pg.fill("#ge","ana@correo.com"); pg.fill("#gp","123"); pg.fill("#gc","123"); pg.click("#gok"); print("4) clave corta ->",pg.inner_text("#gerr"))
    pg.fill("#gp","secreto1"); pg.fill("#gc","otra123"); pg.click("#gok"); print("5) no coinciden ->",pg.inner_text("#gerr"))
    pg.fill("#gp","secreto1"); pg.fill("#gc","secreto1"); pg.check("#gcheck"); pg.click("#gok"); pg.wait_for_timeout(400)
    print("6) registrado; gate visible:",pg.is_visible("#gate"),"| ventana de datos:",pg.is_visible("#perfil"),"| nombre prellenado:",pg.input_value("#pn"))
    pg.click("#pno"); pg.fill("#n","Press de banca"); pg.click("#nuevo button[type=submit]")
    print("7) guardado en storage:",pg.evaluate("!!localStorage.getItem('rutina-gym-v1')"),"| hash guardado sin la clave:","secreto1" not in pg.evaluate("localStorage.getItem('rutina-gym-cuenta')"))
    pg.reload(); pg.wait_for_timeout(300); print("8) recargar con sesión -> gate visible:",pg.is_visible("#gate"),"| ejercicios:",pg.locator(".ex").count())
    pg.click("#cfg"); print("9) cuenta en ajustes:",pg.inner_text("#cuenta")); pg.click("#salir"); pg.wait_for_timeout(200)
    print("10) tras cerrar sesión:",pg.inner_text("#gtit"),"| visible:",pg.is_visible("#gate")); pg.screenshot(path="/tmp/g2.png")
    pg.fill("#ge","ana@correo.com"); pg.fill("#gp","incorrecta"); pg.click("#gok"); pg.wait_for_timeout(300); print("11) clave mala ->",pg.inner_text("#gerr"))
    pg.fill("#gp","secreto1"); pg.click("#gok"); pg.wait_for_timeout(400); print("12) login ok; gate:",pg.is_visible("#gate"),"| ejercicios:",pg.locator(".ex").count())
    pg.click("#cfg"); pg.click("#salir"); pg.click("#golv"); pg.click("#gborra"); pg.click("#gborra"); pg.wait_for_timeout(500)
    print("13) tras borrar cuenta:",pg.inner_text("#gtit"),"| cuenta en storage:",pg.evaluate("localStorage.getItem('rutina-gym-cuenta')"))
    print("errores",errs); b.close()
