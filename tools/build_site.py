"""Build the Caribbean Guard site from one shared layout.

Every page's chrome comes from `page()` below, so the navigation and footer
cannot drift apart the way they do on the live site, where the header markup is
emitted three times per page and the footer points at two URLs that 404.

Body copy is Caribbean Guard's own, lifted verbatim from the live pages by
tools/extract_site_copy.py. Nothing here is invented. Where the live site says
something contradictory the contradiction is preserved and flagged for AJ rather
than silently resolved, because resolving it would mean guessing on a safety
organization's behalf.

Deliberately NOT changed in this pass, on instruction: lang stays "es-AR" and the
site stays Spanish only.
"""
import html, json, os, re, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "site")
COPY = json.load(open(os.path.join(HERE, "site_copy.json"), encoding="utf-8"))

PHONE = "+506 8339 6566"
PHONE_TEL = "+50683396566"
EMAIL = "caribbeanguard.pv@gmail.com"
IG = "https://www.instagram.com/caribbeanguard/"
FB = "https://www.facebook.com/people/Caribbean-Guard/100069778973007/"

# Seven, down from nine. Order matters: the map is first because it is the only
# thing on this site somebody might open twice, and the only one they might open
# standing in the water's edge.
NAV = [
    ("mapa",              "Mapa de Seguridad"),
    ("playa-organizada",  "Playa Organizada"),
    ("lifesaving-club",   "Lifesaving Club"),
    ("swim-club",         "Swim Club"),
    ("freediving-club",   "Freediving Club"),
    ("nosotros",          "Nosotros"),
    ("involucrate",       "Involúcrate"),
]


def esc(s):
    return html.escape(s, quote=False)


def paras(text, cls=""):
    """Verbatim copy into paragraphs, preserving the author's own breaks."""
    c = f' class="{cls}"' if cls else ""
    return "\n".join(f"<p{c}>{esc(b.strip())}</p>"
                     for b in re.split(r"\n\s*\n", text.strip()) if b.strip())


def page(slug, title, body, desc, depth=1, current=None):
    """One layout, one navigation, one footer. `depth` is how far to ../ back."""
    up = "../" * depth if depth else ""
    cur = current or slug

    nav = "\n".join(
        f'      <li><a href="{up}{s}/"{" aria-current=\"page\"" if s == cur else ""}>{esc(l)}</a></li>'
        for s, l in NAV)

    return f"""<!DOCTYPE html>
<html lang="es-AR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="theme-color" content="#0B1C2C">
<title>{esc(title)} — Caribbean Guard</title>
<meta name="description" content="{esc(desc)}">
<link rel="stylesheet" href="{up}assets/site.css">
</head>
<body>
<a class="skip" href="#main">Saltar al contenido</a>

<div class="emg">
  <div class="wrap">
    <span>¿Emergencia en el agua?</span>
    <a href="tel:911" class="num">Llama al 911</a>
  </div>
</div>

<header class="site">
  <div class="wrap">
    <a class="brand" href="{up}">Caribbean Guard<span>Caribe Sur, Costa Rica</span></a>
    <div class="spacer"></div>
    <nav class="main" id="nav-main" aria-label="Principal">
      <ul>
{nav}
      </ul>
    </nav>
    <a class="cta" href="{up}donar/">Donar</a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav-main">
      <span class="menu-label">Menú</span>
    </button>
  </div>
</header>

<main id="main">
{body}
</main>

<footer class="site">
  <div class="wrap">
    <div class="fgrid">
      <div>
        <h2>Caribbean Guard</h2>
        <p>Asociación de salvamento acuático del Caribe Sur. Puerto Viejo a
           Manzanillo, Limón, Costa Rica.</p>
        <p><strong>Emergencias: <a href="tel:911">911</a></strong></p>
      </div>
      <div>
        <h2>Contacto</h2>
        <ul>
          <li><a href="tel:{PHONE_TEL}">{PHONE}</a></li>
          <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
          <li><a href="{IG}" rel="noopener">Instagram</a></li>
          <li><a href="{FB}" rel="noopener">Facebook</a></li>
        </ul>
      </div>
      <div>
        <h2>Secciones</h2>
        <ul>
          <li><a href="{up}mapa/">Mapa de Seguridad</a></li>
          <li><a href="{up}nosotros/">Nosotros</a></li>
          <li><a href="{up}involucrate/">Involúcrate</a></li>
          <li><a href="{up}donar/">Donar</a></li>
        </ul>
      </div>
    </div>
    <div class="legal">
      <p>Asociación Caribbean Guard · Cédula Jurídica 3-002-881795</p>
    </div>
  </div>
</footer>

<script src="{up}assets/site.js"></script>
</body>
</html>
"""


def write(path, contents):
    full = os.path.join(OUT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, "w", encoding="utf-8").write(contents)
    return path


def shot(slug, up="", caption=None):
    """Reserve the photograph's slot, at the ratio the layout expects.

    Nothing here pretends to be a photograph. The frame states which picture
    belongs in it and what it needs to show, so the gaps read as a shot list
    rather than as an oversight.
    """
    cap = f'<figcaption>{esc(caption)}</figcaption>' if caption else ""
    return (f'<figure class="shot"><img src="{up}assets/img/placeholder/{slug}.svg" '
            f'alt="" loading="lazy" decoding="async">{cap}</figure>')


def map_card(up="", reviewed=None, title="Mapa de Seguridad"):
    """The link card. Deliberately makes no claim of being live or lifeguard-authored.

    An earlier draft of this copy said "en tiempo real" and "marcado por nuestros
    guardavidas". Neither is true: nothing polls anything and no beach has been
    signed off yet. A real-time claim over stale data is worse than the static PNG
    it replaces, because the PNG never made the claim.
    """
    rev = reviewed or "Sin revisar aún. Pregunta a un guardavidas antes de entrar al mar."
    return f"""<a class="mapcard" href="{up}mapa/">
      <h2>{esc(title)}</h2>
      <p>Dónde se puede nadar en esta costa, playa por playa.
         Ábrelo en el teléfono antes de entrar al mar.</p>
      <span class="go">Abrir el mapa →</span>
      <p class="rev">Última revisión: {esc(rev)}</p>
    </a>"""


def hazard_summary():
    """Text equivalent of the hazard map, generated from the extracted data.

    The live site publishes two hazard graphics with empty alt text, so the rip
    current locations exist only as pixels: no text anywhere says where they are.
    This is that missing text, and it comes from the same file the map draws.
    """
    p = os.path.join(ROOT, "web", "data", "cg-hazards.geojson")
    if not os.path.exists(p):
        return ""
    d = json.load(open(p, encoding="utf-8"))
    kinds = {}
    for f in d["features"]:
        kinds.setdefault(f["properties"]["kind"], []).append(f)
    rips = kinds.get("rip_current", [])
    stations = kinds.get("rescue_station", [])

    def ll(f):
        g = f["geometry"]["coordinates"]
        lon, lat = (g[0] if isinstance(g[0], list) else g)[:2] if isinstance(g[0], list) else g
        return f"{lat:.4f}, {lon:.4f}"

    items = []
    for i, f in enumerate(sorted(rips, key=lambda x: x["geometry"]["coordinates"][0][0]), 1):
        items.append(f"<li>Corriente de resaca {i}: {ll(f)} "
                     f"(aprox. {f['properties']['length_m']} m, hacia mar abierto)</li>")
    for i, f in enumerate(sorted(stations, key=lambda x: x["geometry"]["coordinates"][0]), 1):
        items.append(f"<li>Estación de salvamento {i}: {ll(f)}</li>")

    return f"""<details class="equiv">
      <summary>Contenido del mapa en texto ({len(rips)} corrientes, {len(stations)} estaciones)</summary>
      <p>Coordenadas aproximadas, con un margen de unos 75 m. Provienen del mapa
         anotado por Caribbean Guard y <strong>están pendientes de confirmación</strong>.</p>
      <ul>
{chr(10).join("        " + i for i in items)}
      </ul>
    </details>"""


# ---------------------------------------------------------------- pages

def build():
    if os.path.isdir(OUT):
        for n in os.listdir(OUT):
            if n != "assets":
                shutil.rmtree(os.path.join(OUT, n), ignore_errors=True) \
                    if os.path.isdir(os.path.join(OUT, n)) else os.remove(os.path.join(OUT, n))

    written = []
    c = COPY

    # ---- Inicio ----
    mission = c["home"]["body_blocks"][2]
    written.append(write("index.html", page("", "Salvando vidas en el Caribe Sur", f"""
<section class="hero">
  <div class="wrap narrow">
    <p class="eyebrow">Puerto Viejo a Manzanillo · Limón</p>
    <h1>Salvando vidas en el Caribe Sur</h1>
    <p>Desde 2021 nunca murió nadie durante nuestras guardias. Somos una asociación
       comunitaria de salvamento acuático: patrullamos playas, formamos guardavidas
       y enseñamos a la comunidad a estar segura en el agua.</p>
    <div class="actions">
      <a class="cta" href="mapa/">Ver el mapa de seguridad</a>
      <a class="cta ghost" href="involucrate/">Involúcrate</a>
    </div>
    {shot("hero")}
  </div>
</section>

<section>
  <div class="wrap">
    <p class="eyebrow">Antes de entrar al mar</p>
    {map_card()}
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <h2>Nuestra misión</h2>
    {paras(mission)}
    <p><a href="nosotros/historia/">Cómo empezó todo →</a></p>
  </div>
</section>

<section>
  <div class="wrap">
    <h2>Tres clubes, abiertos a la comunidad</h2>
    <div class="rows">
      <div class="row">
        {shot("lifesaving")}
        <div>
          <h3>Lifesaving Club</h3>
          <p>Guardias, entrenamiento de salvamento, educación continua y una red de
             alerta de emergencias con más de 70 miembros.</p>
          <a class="more" href="lifesaving-club/">Conocer el club →</a>
        </div>
      </div>
      <div class="row">
        {shot("swim")}
        <div>
          <h3>Swim Club</h3>
          <p>Natación en aguas abiertas y piscina, gratuita. Tres entrenamientos por
             semana en Punta Uva y Playa Negra, más la Swim School para la infancia.</p>
          <a class="more" href="swim-club/">Ver horarios →</a>
        </div>
      </div>
      <div class="row">
        {shot("freediving")}
        <div>
          <h3>Freediving Club</h3>
          <p>La unidad más nueva. Apnea con enseñanza segura, en una comunidad marina
             con amplia experiencia en buceo a pulmón.</p>
          <a class="more" href="freediving-club/">Conocer el club →</a>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="alt">
  <div class="wrap narrow">
    <h2>Sostener esto cuesta</h2>
    <p>Somos una organización voluntaria y autogestionada. Las clases de natación,
       la formación de guardavidas y el equipo de rescate se financian con
       donaciones y con el aporte de los negocios de la zona.</p>
    <p><a class="cta" href="donar/">Donar</a></p>
  </div>
</section>
""", "Asociación comunitaria de salvamento acuático en el Caribe Sur de Costa Rica.",
        depth=0, current="")))

    # ---- Mapa ----
    written.append(write("mapa/index.html", page("mapa", "Mapa de Seguridad", f"""
<section>
  <div class="wrap">
    <p class="eyebrow">Playa por playa</p>
    <h1>Mapa de Seguridad</h1>
    <p class="lede">Dónde se puede nadar en esta costa. Está hecho para el teléfono,
       para consultarlo parado en la playa, antes de entrar al agua.</p>
    {map_card(title="Abrir el mapa en el teléfono")}

    <h2 style="margin-top:2rem">Qué muestra</h2>
    <dl class="facts legend">
      <dt><span class="status danger">No nadar</span></dt>
      <dd>Corrientes de resaca frecuentes o fondo peligroso. En el mapa es la línea
          más gruesa y continua: la marca más fuerte es siempre la más peligrosa.</dd>
      <dt><span class="status caution">Precaución</span></dt>
      <dd>Seguro sólo en ciertas condiciones: marea, oleaje u hora del día.
          Línea entrecortada.</dd>
      <dt><span class="status safe">Se puede nadar</span></dt>
      <dd>La zona más protegida del tramo. Línea punteada fina. No es una promesa:
          el mar cambia.</dd>
    </dl>
    {shot("mapa", "../")}

    <h2 style="margin-top:2rem">Corrientes y estaciones registradas</h2>
    <p>Este es el contenido del mapa anotado, escrito en texto para que se pueda
       leer, buscar y escuchar con un lector de pantalla.</p>
    {hazard_summary()}

    <h2 style="margin-top:2rem">Códigos QR en la costa</h2>
    <p>Estamos colocando códigos QR en postes a lo largo de la playa. Cada uno abre
       el mapa directamente en la playa donde estás parado, sin tener que buscarla.</p>
  </div>
</section>
""", "Mapa de seguridad costera de Caribbean Guard: dónde se puede nadar entre Puerto Viejo y Manzanillo.")))

    # ---- Playa Organizada ----
    ppo = "\n".join(
        f'      <div class="item"><h2>{esc(s["title"])}</h2>{paras(s["body"])}</div>'
        for s in c["programa-playa-organizada"]["sections"])
    written.append(write("playa-organizada/index.html", page("playa-organizada",
        "Programa Playa Organizada", f"""
<section>
  <div class="wrap">
    <p class="eyebrow">Nuestro programa operativo</p>
    <h1>Programa Playa Organizada</h1>
    <p class="lede">Banderas, líneas de supervivencia, estaciones de salvamento y un
       plan de emergencia acordado con los negocios de cada playa. Es el sistema que
       el mapa de seguridad documenta.</p>
    {shot("playa-organizada", "../")}

    {map_card()}

    <h2 style="margin-top:2rem">El mapa anotado de la zona</h2>
    <figure>
      <div class="panx">
        <img src="../assets/img/mapa-anotado.webp" width="2500" height="1013" loading="lazy" decoding="async"
             alt="Mapa aéreo anotado de la costa entre Playa Chiquita y Punta Uva.
                  Flechas rojas marcan diez corrientes de resaca saliendo hacia mar
                  abierto; hexágonos naranjas marcan cuatro estaciones de salvamento;
                  líneas azules marcan la carretera principal y los accesos peatonales
                  a la playa; estrellas amarillas marcan hoteles y negocios con el
                  tiempo de caminata hasta la playa.">
      </div>
      <figcaption>Mapa anotado por Caribbean Guard. Cubre 1,8 km entre Playa Chiquita
        y Punta Uva, aproximadamente el 11 % de la costa que patrullamos.</figcaption>
    </figure>
    {hazard_summary()}

    <figure>
      <img src="../assets/img/zona-peligrosa.webp" width="842" height="596" loading="lazy" decoding="async"
           alt="Detalle aéreo de una playa con arrecife. Una zona rayada en rojo marca
                el área peligrosa junto al arrecife, con flechas rojas que muestran la
                corriente saliendo hacia mar abierto. Una línea de boyas amarillas
                cruza el agua: es la línea de supervivencia.">
      <figcaption>Zona de resaca junto al arrecife, con la línea de supervivencia
        —el mecate con boyas— cruzando por delante.</figcaption>
    </figure>

    <h2 style="margin-top:2rem">Cómo funciona</h2>
    <div class="stack">
{ppo}
    </div>
  </div>
</section>
""", "Banderas, líneas de supervivencia, estaciones de salvamento y plan de emergencia en las playas del Caribe Sur.")))

    # ---- clubs ----
    ls = "\n".join(f'      <div class="item"><h2>{esc(s["title"])}</h2>{paras(s["body"])}</div>'
                   for s in c["lifesaving-club"]["sections"])
    written.append(write("lifesaving-club/index.html", page("lifesaving-club",
        "Lifesaving Club", f"""
<section>
  <div class="wrap">
    <p class="eyebrow">Guardavidas y guardias de playa</p>
    <h1>Lifesaving Club</h1>
    <p class="lede">Desde la creación de la organización nunca murió nadie en nuestras
       guardias. Patrullamos los domingos, el día con más incidencias de ahogamiento
       del país.</p>
    {shot("lifesaving", "../")}
    <div class="stack">
{ls}
    </div>
    <p style="margin-top:2rem"><a class="cta" href="../involucrate/">Quiero unirme</a></p>
  </div>
</section>
""", "Guardias de playa, entrenamiento de salvamento y red de alerta de emergencias del Caribe Sur.")))

    written.append(write("swim-club/index.html", page("swim-club", "Swim Club", f"""
<section>
  <div class="wrap">
    <p class="eyebrow">Gratuito y abierto a la comunidad</p>
    <h1>Swim Club</h1>
    {paras(c["swim-club"]["body_blocks"][0], "lede")}
    {shot("swim", "../")}
    <h2 style="margin-top:2rem">Entrenamientos</h2>
    <dl class="facts">
      <dt>Punta Uva</dt><dd>Jueves, 7:15 h</dd>
      <dt>Playa Negra</dt><dd>Martes y viernes, 16:00 h</dd>
      <dt>Swim School</dt><dd>Clases gratuitas en piscina para niñas y niños de la comunidad</dd>
    </dl>
    <p style="margin-top:2rem"><a class="cta" href="../involucrate/">Quiero unirme</a></p>
  </div>
</section>
""", "Natación gratuita en aguas abiertas y piscina en Punta Uva y Playa Negra.")))

    written.append(write("freediving-club/index.html", page("freediving-club",
        "Freediving Club", f"""
<section>
  <div class="wrap">
    <p class="eyebrow">La unidad más nueva</p>
    <h1>Freediving Club</h1>
    {paras(c["freediving-club"]["body_blocks"][0], "lede")}
    {shot("freediving", "../")}
    <p style="margin-top:2rem"><a class="cta" href="../involucrate/">Quiero unirme</a></p>
  </div>
</section>
""", "Apnea y buceo a pulmón con enseñanza segura en el Caribe Sur de Costa Rica.")))

    # ---- Nosotros hub + children ----
    written.append(write("nosotros/index.html", page("nosotros", "Nosotros", f"""
<section>
  <div class="wrap">
    <h1>Nosotros</h1>
    <p class="lede">Una asociación comunitaria nacida en Semana Santa de 2021, cuando
       treinta vecinos salieron a patrullar seis playas para que nadie se muriera.</p>
    <div class="rows">
      <div class="row">{shot("historia", "../")}<div><h2>Historia</h2>
        <p>De una campaña de videos a una asociación con más de 70 miembros y 400
           personas formadas.</p>
        <a class="more" href="historia/">Leer la historia →</a></div></div>
      <div class="row"><div class="shot"></div><div><h2>Visión</h2>
        <p>Quién debe ser responsable del salvamento acuático en Costa Rica, y la
           ley de tercios.</p>
        <a class="more" href="vision/">Leer la visión →</a></div></div>
      <div class="row">{shot("equipo", "../")}<div><h2>Equipo</h2>
        <p>Quiénes patrullan, enseñan y coordinan.</p>
        <a class="more" href="equipo/">Ver el equipo →</a></div></div>
      <div class="row">{shot("proyectos", "../")}<div><h2>Proyectos</h2>
        <p>Lo que todavía necesitamos: bodega, guardia móvil y el centro acuático.</p>
        <a class="more" href="proyectos/">Ver los proyectos →</a></div></div>
    </div>
  </div>
</section>
""", "Historia, visión, equipo y proyectos de la Asociación Caribbean Guard.")))

    hist = "\n".join(paras(b) for b in c["nuestro-trabajo"]["body_blocks"][1:2])
    written.append(write("nosotros/historia/index.html", page("nosotros", "Historia", f"""
<section>
  <div class="wrap">
    <p class="eyebrow">Nosotros</p>
    <h1>Historia</h1>
    <p class="lede">“Quien salva una vida, salva al mundo entero.”</p>
    {shot("historia", "../../")}
    {hist}
  </div>
</section>
""", "Cómo nació Caribbean Guard en marzo de 2021 y cómo creció hasta hoy.", depth=2)))

    vis = "\n".join(paras(b) for b in c["vision"]["body_blocks"][:2])
    written.append(write("nosotros/vision/index.html", page("nosotros", "Visión", f"""
<section>
  <div class="wrap">
    <p class="eyebrow">Nosotros</p>
    <h1>Visión</h1>
    {vis}
  </div>
</section>
""", "La ley de tercios: comunidad, empresas y gobierno sosteniendo el salvamento acuático.", depth=2)))

    # Only people whose role the live site actually states. The rest still say
    # "Description goes here", and inventing roles for real people is not an option.
    roles = [(s["title"], s["body"]) for s in c["team"]["sections"]
             if s["body"] and "Description goes here" not in s["body"]]
    pending = [s["title"] for s in c["team"]["sections"]
               if not s["body"] or "Description goes here" in s["body"]]
    ppl = "\n".join(f'      <div class="person"><h2>{esc(n)}</h2><p>{esc(r)}</p></div>'
                    for n, r in roles)
    written.append(write("nosotros/equipo/index.html", page("nosotros", "Equipo", f"""
<section>
  <div class="wrap">
    <p class="eyebrow">Nosotros</p>
    <h1>Equipo</h1>
    <p class="lede">Guardavidas, instructores y coordinadores de la asociación.</p>
    <div class="people">
{ppl}
    </div>
    <p style="margin-top:2rem;color:var(--muted);font-size:15px">
      Y {len(pending)} integrantes más cuyo rol todavía no está publicado.</p>
  </div>
</section>
""", "Guardavidas, instructores y coordinadores de Caribbean Guard.", depth=2)))

    proj = "\n".join(f'      <div class="item"><h2>{esc(s["title"])}</h2>{paras(s["body"])}</div>'
                     for s in c["proyectos"]["sections"])
    written.append(write("nosotros/proyectos/index.html", page("nosotros", "Proyectos", f"""
<section>
  <div class="wrap">
    <p class="eyebrow">Nosotros</p>
    <h1>Proyectos</h1>
    <p class="lede">Lo que todavía necesitamos para trabajar mejor. La bodega es la
       prioridad número uno de la asociación.</p>
    {shot("proyectos", "../../")}
    <div class="stack">
{proj}
    </div>
    <p style="margin-top:2rem"><a class="cta" href="../../donar/">Donar</a></p>
  </div>
</section>
""", "Bodega de equipos, programa de guardia móvil y Centro Acuático de Alto Rendimiento.", depth=2)))

    # ---- Involúcrate: the page that had no way to make contact ----
    inv = paras(c["involcrate"]["body_blocks"][0].replace("INVOLÚCRATE", "").strip())
    written.append(write("involucrate/index.html", page("involucrate", "Involúcrate", f"""
<section>
  <div class="wrap">
    <h1>Involúcrate</h1>
    {inv}
    {shot("involucrate", "../")}
  </div>
</section>

<section class="alt">
  <div class="wrap">
    <h2>Escríbenos</h2>
    <p>Cuéntanos quién eres y qué te gustaría hacer. Te respondemos por correo.</p>
    <form class="contact" action="mailto:{EMAIL}" method="post" enctype="text/plain">
      <div class="field">
        <label for="nombre">Nombre</label>
        <input id="nombre" name="nombre" type="text" autocomplete="name" required>
      </div>
      <div class="field">
        <label for="correo">Correo electrónico</label>
        <input id="correo" name="correo" type="email" autocomplete="email" required>
      </div>
      <div class="field">
        <label for="interes">Me interesa</label>
        <select id="interes" name="interes">
          <option>Sumarme al Swim Club</option>
          <option>Sumarme al Lifesaving Club</option>
          <option>Sumarme al Freediving Club</option>
          <option>Ser socio local (hotel, restaurante, tienda)</option>
          <option>Donar o patrocinar</option>
          <option>Otra cosa</option>
        </select>
      </div>
      <div class="field">
        <label for="mensaje">Mensaje</label>
        <span class="hint">¿Cuáles son tus fortalezas? No hace falta ser guardavidas.</span>
        <textarea id="mensaje" name="mensaje"></textarea>
      </div>
      <button class="cta" type="submit">Enviar</button>
    </form>

    <h2 style="margin-top:2.5rem">O contáctanos directamente</h2>
    <dl class="facts">
      <dt>Teléfono</dt><dd><a href="tel:{PHONE_TEL}">{PHONE}</a></dd>
      <dt>Correo</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd>
      <dt>Instagram</dt><dd><a href="{IG}" rel="noopener">@caribbeanguard</a></dd>
      <dt>Emergencias</dt><dd><a href="tel:911">911</a></dd>
    </dl>
  </div>
</section>
""", "Únete a Caribbean Guard como voluntario, socio local o donante.")))

    # /unete used to 404 from the footer. It is the volunteer entry point.
    written.append(write("unete/index.html", """<!DOCTYPE html>
<html lang="es-AR">
<head>
<meta charset="utf-8">
<title>Únete — Caribbean Guard</title>
<link rel="canonical" href="../involucrate/">
<meta http-equiv="refresh" content="0; url=../involucrate/">
</head>
<body>
<p>Esta página se movió a <a href="../involucrate/">Involúcrate</a>.</p>
</body>
</html>
"""))

    # ---- Donar ----
    written.append(write("donar/index.html", page("donar", "Donar", f"""
<section>
  <div class="wrap">
    <h1>Donar</h1>
    <p class="lede">Tu donación nos ayuda a salvar vidas: clases de natación gratuitas,
       formación de guardavidas y talleres de seguridad para la comunidad. Con tu apoyo
       podemos ampliar los programas, mejorar las patrullas y avanzar con el centro
       acuático.</p>
    <p><a class="cta" href="https://www.paypal.com/donate/?hosted_button_id=C747QS8AQD8RL"
          target="_blank" rel="noopener">Donar por PayPal (se abre en otra pestaña)</a></p>

    <h2 style="margin-top:2.5rem">Transferencia bancaria</h2>
    <p>Banco Nacional de Costa Rica · Asociación Caribbean Guard ·
       Cédula Jurídica 3-002-881795</p>
    <dl class="facts">
      <dt>Cuenta en dólares</dt><dd>200-02-093-003288-9<br>IBAN CR93 0151 0932 0020 0328 81</dd>
      <dt>Cuenta en colones</dt><dd>200-01-093-008563-4<br>IBAN CR17 0151 0932 0010 0856 38</dd>
      <dt>PayPal</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd>
      <dt>Sinpe Móvil</dt><dd><a href="tel:{PHONE_TEL}">{PHONE}</a></dd>
    </dl>
  </div>
</section>
""", "Cómo donar a la Asociación Caribbean Guard: PayPal, transferencia bancaria o Sinpe Móvil.")))

    # ---- assets: the hazard maps, and the map app itself ----
    # Re-encode rather than copy. The live site serves these as PNG at 4.1 MB and
    # 668 KB, and serves the annotated map twice because it was uploaded twice.
    # They are photographs with drawn overlays, so PNG is the wrong container.
    from PIL import Image
    img = os.path.join(OUT, "assets", "img")
    os.makedirs(img, exist_ok=True)
    for src, dst in [("annotated-base-map-v5.png", "mapa-anotado.webp"),
                     ("dangerous-area-v4.png", "zona-peligrosa.webp")]:
        s = os.path.join(ROOT, "reference", "cg-existing-maps", src)
        d = os.path.join(img, dst)
        Image.open(s).convert("RGB").save(d, quality=82, method=6)
        print(f"   {dst}: {os.path.getsize(s)/1e6:.2f} MB -> {os.path.getsize(d)/1e6:.2f} MB")

    # The map ships standalone in production; copied in here so the whole thing is
    # navigable locally as one tree.
    app = os.path.join(OUT, "mapa", "app")
    shutil.rmtree(app, ignore_errors=True)
    shutil.copytree(os.path.join(ROOT, "web"), app)

    for p in written:
        print("  ", p)
    print(f"\n{len(written)} pages -> {OUT}")
    print(f"team roles published: {len(roles)}, pending: {len(pending)}")


if __name__ == "__main__":
    build()
