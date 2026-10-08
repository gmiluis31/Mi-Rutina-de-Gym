import sys,pathlib;sys.path.insert(0,str(pathlib.Path(__file__).parent))
import h
from h import reg,URL
import sys,random,re,json
from playwright.sync_api import sync_playwright
seed=int(sys.argv[1]); steps=int(sys.argv[2]); W=int(sys.argv[3]) if len(sys.argv)>3 else 390
rnd=random.Random(seed)
TXT=["","0","-1","9999","37.5","<b>x</b>","\"'><img src=x onerror=window.__xss=1>","A"*300,"😀 ejercicio","  espacios  ","1e9","Press de banca","NaN","null","0.1"]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={"width":W,"height":800}); errs=[]; log=[]
    pg.add_init_script("window.__errs=[];addEventListener('unhandledrejection',e=>__errs.push('rechazo: '+(e.reason&&e.reason.message||e.reason)));addEventListener('error',e=>__errs.push('error: '+e.message))")
    pg.on("pageerror",lambda e:errs.append("pageerror: "+str(e)))
    pg.on("dialog",lambda d:(errs.append("DIALOGO: "+d.message),d.dismiss()))
    pg.goto(URL); pg.wait_for_timeout(300); h.reg(pg)
    if pg.is_visible("#pno"): pg.locator("#pno").click(timeout=2000)
    pg.evaluate("sel='2026-10-05';pintar()")
    def check(i):
        t=pg.inner_text("body")
        for bad in ("NaN","undefined","[object","Infinity"):
            if bad in t: errs.append(f"paso {i}: aparece '{bad}' en pantalla")
        if pg.evaluate("document.documentElement.scrollWidth-innerWidth")>2: errs.append(f"paso {i}: desborde horizontal")
        r=pg.evaluate("""()=>{const o=[];try{JSON.stringify(st)}catch(e){o.push('st no serializable')}
          if(!Array.isArray(st.dias)||st.dias.length!==7)o.push('dias roto');
          if(!/^\\d{4}-\\d{2}-\\d{2}$/.test(sel))o.push('sel inválido '+sel);
          for(const d of Object.values(st.log))for(const a of Object.values(d))if(!Array.isArray(a)||a.length>12)o.push('marcas raras');
          if(window.__xss)o.push('XSS ejecutado');
          return o.concat(window.__errs.splice(0))}""")
        errs.extend(f"paso {i}: {x}" for x in r)
    for i in range(steps):
        a=rnd.random()
        try:
            if a<0.62:
                els=pg.locator("button:visible:not([disabled]), select:visible").all()
                els=[e for e in els if e.is_enabled()]
                if not els: continue
                e=rnd.choice(els); tag=e.evaluate("e=>e.id||e.className||e.tagName"); log.append("click "+str(tag)[:40])
                if e.evaluate("e=>e.tagName")=="SELECT":
                    opts=e.locator("option").all_inner_texts(); 
                    if opts: e.select_option(label=rnd.choice(opts),timeout=500)
                else: e.click(timeout=500,force=False)
            elif a<0.82:
                ins=pg.locator("input:visible:not([type=checkbox]):not([type=file])").all()
                if not ins: continue
                e=ins[rnd.randrange(len(ins))]; num=e.get_attribute("type")=="number"; v=rnd.choice(["","0","-1","9999","37.5","0.1","1e9","12","3"] if num else TXT); log.append(f"escribe {v[:15]!r}")
                e.fill(v,timeout=500)
                if rnd.random()<.5: e.press("Enter",timeout=500)
            elif a<0.88:
                k=rnd.choice(["Escape","Tab","ArrowUp","ArrowDown","Enter"]); log.append("tecla "+k); pg.keyboard.press(k)
            elif a<0.94:
                bb=pg.locator("#semana").bounding_box()
                if bb and pg.is_visible("#semana"):
                    y=bb["y"]+bb["height"]/2; x0=bb["x"]+bb["width"]*.8; log.append("swipe")
                    pg.mouse.move(x0,y); pg.mouse.down(); pg.mouse.move(x0-200,y,steps=6); pg.mouse.up()
            else:
                d=rnd.choice(["2026-12-31","2027-01-01","2026-03-29","2028-02-29","2026-10-12","2026-10-08","2026-11-01"]); log.append("ir "+d)
                pg.evaluate("f=>{sel=f;editId=null;pintar()}",d)
        except Exception as ex:
            if "Timeout" not in str(ex) and "detached" not in str(ex) and "not stable" not in str(ex) and "intercepts" not in str(ex) and "not visible" not in str(ex) and "outside" not in str(ex) and "not enabled" not in str(ex):
                errs.append(f"paso {i}: excepción de la prueba: {str(ex)[:120]}")
        if i%5==0: check(i)
        if i%30==0: print("paso",i,flush=True)
        if errs: 
            print("FALLO tras acciones:", log[-6:]); break
    print("seed",seed,"ancho",W,"pasos hechos",i+1,"| errores:",errs[:4] if errs else "ninguno")
    b.close()
