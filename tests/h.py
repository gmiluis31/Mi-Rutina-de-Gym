import pathlib
URL=(pathlib.Path(__file__).resolve().parent.parent/"www"/"index.html").as_uri()
from playwright.sync_api import Page
_click=Page.click; _fill=Page.fill
def _abrir(pg,sel):
    # abre automáticamente menús y hojas del nuevo diseño antes de usar sus controles
    if sel in ("#copiar","#reset","#tema") and not pg.is_visible("#menu"): _click(pg,"#menuBtn")
    elif (sel.startswith("[data-t=") or sel in ("[data-ok]","[data-no]","#avtxt")) and not pg.is_visible("#rut"): _click(pg,"#rutinasBtn")
    elif (sel in ("#nuevo button[type=submit]","#abrirLib","#n","#s","#r","#k","#nt")) and not pg.is_visible("#addsheet") and not pg.is_visible("#lib"): _click(pg,"#addBtn")
def _c(self,selector,*a,**k): _abrir(self,selector); return _click(self,selector,*a,**k)
def _f(self,selector,value,*a,**k): _abrir(self,selector); return _fill(self,selector,value,*a,**k)
Page.click=_c; Page.fill=_f
def reg(pg,email="ana@correo.com",pw="secreto1"):
    pg.fill("#gn","Ana"); pg.fill("#ge",email); pg.fill("#gp",pw); pg.fill("#gc",pw); pg.check("#gcheck"); _click(pg,"#gok"); pg.wait_for_timeout(400)
