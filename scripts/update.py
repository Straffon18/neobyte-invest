"""Actualiza data.json con precios, objetivos de analistas y tipo de cambio.
Lo ejecuta GitHub Actions automáticamente (ver .github/workflows/actualizar.yml).
Fuente: Yahoo Finanzas vía la librería yfinance (retraso aprox. 15 min)."""
import json, math, os, time, datetime as dt
import yfinance as yf

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data.json")

# (ticker en Yahoo, ticker que se muestra, nombre, sector, moneda, mercado)
UNIVERSE = [
 ("NVDA","NVDA","NVIDIA","Chips para IA","USD","SIC"),("GOOGL","GOOGL","Alphabet (Google)","Buscador, nube e IA","USD","SIC"),
 ("AMZN","AMZN","Amazon","E-commerce y nube","USD","SIC"),("MSFT","MSFT","Microsoft","Software y nube","USD","SIC"),
 ("META","META","Meta (Facebook, Instagram)","Redes sociales","USD","SIC"),("AVGO","AVGO","Broadcom","Chips para IA","USD","SIC"),
 ("AMD","AMD","AMD","Procesadores y chips","USD","SIC"),("PLTR","PLTR","Palantir","Software de datos e IA","USD","SIC"),
 ("NFLX","NFLX","Netflix","Streaming","USD","SIC"),("TSLA","TSLA","Tesla","Autos eléctricos","USD","SIC"),
 ("AAPL","AAPL","Apple","iPhone y servicios","USD","SIC"),("KO","KO","Coca-Cola","Bebidas","USD","SIC"),
 ("LLY","LLY","Eli Lilly","Farmacéutica","USD","SIC"),("WMT","WMT","Walmart","Supermercados","USD","SIC"),
 ("COST","COST","Costco","Supermercados","USD","SIC"),("JPM","JPM","JPMorgan","Banco","USD","SIC"),
 ("V","V","Visa","Pagos","USD","SIC"),("MA","MA","Mastercard","Pagos","USD","SIC"),
 ("BRK-B","BRK.B","Berkshire Hathaway","Conglomerado","USD","SIC"),("JNJ","JNJ","Johnson & Johnson","Salud","USD","SIC"),
 ("PG","PG","Procter & Gamble","Productos del hogar","USD","SIC"),("PEP","PEP","PepsiCo","Bebidas y botanas","USD","SIC"),
 ("MCD","MCD","McDonald's","Restaurantes","USD","SIC"),("SBUX","SBUX","Starbucks","Restaurantes","USD","SIC"),
 ("NKE","NKE","Nike","Ropa deportiva","USD","SIC"),("DIS","DIS","Disney","Entretenimiento","USD","SIC"),
 ("ORCL","ORCL","Oracle","Software y nube","USD","SIC"),("CRM","CRM","Salesforce","Software","USD","SIC"),
 ("ADBE","ADBE","Adobe","Software","USD","SIC"),("INTC","INTC","Intel","Chips","USD","SIC"),
 ("TSM","TSM","TSMC","Chips","USD","SIC"),("MU","MU","Micron","Memorias","USD","SIC"),
 ("QCOM","QCOM","Qualcomm","Chips móviles","USD","SIC"),("UBER","UBER","Uber","Transporte","USD","SIC"),
 ("ABNB","ABNB","Airbnb","Viajes","USD","SIC"),("SHOP","SHOP","Shopify","E-commerce","USD","SIC"),
 ("MELI","MELI","Mercado Libre","E-commerce","USD","SIC"),("BABA","BABA","Alibaba","E-commerce","USD","SIC"),
 ("SPOT","SPOT","Spotify","Música","USD","SIC"),("COIN","COIN","Coinbase","Cripto","USD","SIC"),
 ("XOM","XOM","ExxonMobil","Petróleo","USD","SIC"),("BA","BA","Boeing","Aviones","USD","SIC"),
 ("AMXB.MX","AMX","América Móvil","Telecom (Telcel)","MXN","BMV"),("WALMEX.MX","WALMEX","Walmart de México","Supermercados","MXN","BMV"),
 ("GFNORTEO.MX","GFNORTE","Banorte","Banco","MXN","BMV"),("FEMSAUBD.MX","FEMSA","FEMSA (OXXO)","Comercio y bebidas","MXN","BMV"),
 ("GMEXICOB.MX","GMEXICO","Grupo México","Minería y trenes","MXN","BMV"),("CEMEXCPO.MX","CEMEX","Cemex","Cemento","MXN","BMV"),
 ("BIMBOA.MX","BIMBO","Grupo Bimbo","Alimentos","MXN","BMV"),("ASURB.MX","ASUR","ASUR","Aeropuertos","MXN","BMV"),
 ("GAPB.MX","GAP","Grupo Aeroportuario del Pacífico","Aeropuertos","MXN","BMV"),("OMAB.MX","OMA","OMA","Aeropuertos","MXN","BMV"),
 ("KOFUBL.MX","KOF","Coca-Cola FEMSA","Bebidas","MXN","BMV"),("AC.MX","AC","Arca Continental","Bebidas","MXN","BMV"),
 ("KIMBERA.MX","KIMBER","Kimberly-Clark de México","Productos del hogar","MXN","BMV"),("LIVEPOLC-1.MX","LIVEPOL","Liverpool","Tiendas departamentales","MXN","BMV"),
 ("GCARSOA1.MX","GCARSO","Grupo Carso","Conglomerado","MXN","BMV"),("GCC.MX","GCC","GCC","Cemento","MXN","BMV"),
 ("VESTA.MX","VESTA","Vesta","Naves industriales","MXN","BMV"),("ALFAA.MX","ALFA","Alfa","Conglomerado","MXN","BMV"),
 ("LACOMUBC.MX","LACOMER","La Comer","Supermercados","MXN","BMV"),("GENTERA.MX","GENTERA","Gentera","Microcréditos","MXN","BMV"),
 ("PINFRA.MX","PINFRA","Pinfra","Carreteras","MXN","BMV"),("ORBIA.MX","ORBIA","Orbia","Químicos","MXN","BMV"),
 ("PE&OLES.MX","PEÑOLES","Peñoles","Minería","MXN","BMV"),("CHDRAUIB.MX","CHEDRAUI","Chedraui","Supermercados","MXN","BMV"),
 ("FUNO11.MX","FUNO","Fibra Uno","Inmuebles (FIBRA)","MXN","BMV"),("FMTY14.MX","FMTY","Fibra MTY","Inmuebles (FIBRA)","MXN","BMV"),
 ("Q.MX","QUALITAS","Quálitas","Seguros","MXN","BMV"),("GFINBURO.MX","INBURSA","Inbursa","Banco","MXN","BMV"),
 ("MEGACPO.MX","MEGA","Megacable","Telecom","MXN","BMV"),
]
INDEX_FUNDS = [("VOO","VOO","Fondo S&P 500 (VOO)","Las 500 empresas grandes de EE.UU.","USD","SIC"),
               ("QQQ","QQQ","Fondo Nasdaq 100 (QQQ)","Las 100 tecnológicas más grandes","USD","SIC")]
INDICES = [("^GSPC","S&P 500"),("^IXIC","Nasdaq"),("^DJI","Dow Jones"),("^MXX","IPC México")]

def num(x):
    try:
        x = float(x)
        return x if math.isfinite(x) else None
    except (TypeError, ValueError):
        return None

def rating(rm, n):
    if rm is None or not n: return "Sin consenso"
    if rm <= 1.8: return "Compra fuerte"
    if rm <= 2.5: return "Compra"
    if rm <= 3.2: return "Mantener"
    return "Venta"

def risk(beta, vol_range):
    b = beta if beta is not None else None
    if b is None and vol_range is not None:
        b = 1.6 if vol_range > 0.9 else 1.0 if vol_range > 0.4 else 0.6
    if b is None: return "Medio"
    return "Alto" if b >= 1.4 else "Medio" if b >= 0.8 else "Bajo"

def notes(i, p, tg, n, cur):
    pro, con = [], []
    hi, lo = num(i.get("fiftyTwoWeekHigh")), num(i.get("fiftyTwoWeekLow"))
    if p and hi:
        off = (1 - p / hi) * 100
        if off >= 20: pro.append(f"Cotiza {off:.0f}% abajo de su máximo del último año")
        elif off <= 3: con.append("Está en su precio más alto del año: ya subió mucho")
    rg = num(i.get("revenueGrowth"))
    if rg is not None:
        (pro if rg >= 0.08 else con).append(f"Sus ventas {'crecen' if rg >= 0 else 'caen'} {abs(rg)*100:.0f}% contra el año pasado")
    pm = num(i.get("profitMargins"))
    if pm is not None:
        if pm >= 0.2: pro.append(f"Muy rentable: gana {pm*100:.0f} centavos de cada peso que vende")
        elif pm < 0: con.append("Hoy pierde dinero (margen negativo)")
    dy = num(i.get("trailingAnnualDividendYield"))
    if dy and dy >= 0.015: pro.append(f"Paga dividendos: ~{dy*100:.1f}% al año")
    fpe = num(i.get("forwardPE"))
    if fpe:
        if fpe >= 40: con.append(f"Cara: cuesta {fpe:.0f} veces lo que se espera que gane")
        elif fpe <= 15: pro.append(f"Barata frente a sus ganancias ({fpe:.0f} veces)")
    if n: pro.append(f"La siguen {int(n)} analistas") if n >= 10 else con.append(f"Pocos analistas la siguen ({int(n)})")
    else: con.append("No hay suficientes analistas para un precio objetivo confiable")
    if tg and p and tg < p: con.append("Ya cuesta más que su precio objetivo promedio")
    return pro[:4], con[:4]

def fetch(row, is_idx=False):
    y, t, name, sec, cur, mk = row
    tk = yf.Ticker(y)
    i = tk.info or {}
    p = num(i.get("currentPrice")) or num(i.get("regularMarketPrice"))
    if p is None:
        try: p = num(tk.fast_info["last_price"])
        except Exception: p = None
    if p is None: raise ValueError("sin precio")
    prev = num(i.get("regularMarketPreviousClose")) or num(i.get("previousClose"))
    chg = ((p / prev - 1) * 100) if prev else None
    n = num(i.get("numberOfAnalystOpinions")) or 0
    tg = num(i.get("targetMeanPrice")) if n else None
    hi, lo = num(i.get("fiftyTwoWeekHigh")), num(i.get("fiftyTwoWeekLow"))
    vr = (hi / lo - 1) if hi and lo else None
    pro, con = notes(i, p, tg, n, cur)
    s = {"t": t, "n": name, "sec": sec, "cur": cur, "mk": mk, "p": round(p, 4),
         "chg": round(chg, 2) if chg is not None else None, "tg": round(tg, 4) if tg else None,
         "tgLo": num(i.get("targetLowPrice")), "tgHi": num(i.get("targetHighPrice")), "nA": int(n),
         "rat": rating(num(i.get("recommendationMean")), n), "risk": risk(num(i.get("beta")), vr),
         "pe": num(i.get("forwardPE")), "pro": pro, "con": con}
    if is_idx:
        s.update({"idx": True, "rat": "Diversificado", "risk": "Bajo", "tg": None,
                  "pro": ["Repartes tu dinero en muchas empresas a la vez", "Ideal para empezar: menos riesgo que una sola acción"],
                  "con": ["También cae en crisis (-20% o más en años malos)", "Rinde en dólares: el tipo de cambio te afecta"]})
    return s

def main():
    prev = {}
    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8") as f:
            old = json.load(f)
        prev = {s["t"]: s for s in old.get("stocks", [])}
        prev_meta = old
    else:
        prev_meta = {}
    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    out, ok, fail = [], 0, 0
    for row, is_idx in [(r, False) for r in UNIVERSE] + [(r, True) for r in INDEX_FUNDS]:
        try:
            s = fetch(row, is_idx); s["at"] = now; out.append(s); ok += 1
        except Exception as e:
            fail += 1
            print("WARN", row[0], e)
            if row[1] in prev: out.append(prev[row[1]])  # conserva el último dato bueno
        time.sleep(0.4)
    fx = None
    try:
        fx = num(yf.Ticker("USDMXN=X").fast_info["last_price"])
    except Exception as e:
        print("WARN fx", e)
    fx = round(fx, 4) if fx else prev_meta.get("fx", 18.6)
    idx = []
    for y, n in INDICES:
        try:
            fi = yf.Ticker(y).fast_info
            last, pc = num(fi["last_price"]), num(fi["previous_close"])
            idx.append({"n": n, "v": round(last, 2), "c": round((last / pc - 1) * 100, 2) if pc else None})
        except Exception as e:
            print("WARN idx", y, e)
    if not idx: idx = prev_meta.get("idx", [])
    idx.append({"n": "Dólar (USD/MXN)", "v": fx, "c": None, "fx": True})
    if ok == 0:
        raise SystemExit("No se pudo descargar ningún dato; se conserva el archivo anterior")
    data = {"updatedAt": now, "fx": fx, "idx": idx, "stocks": out, "ok": ok, "fail": fail}
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
    print(f"OK {ok} acciones, {fail} con error, USD/MXN {fx}")

if __name__ == "__main__":
    main()
