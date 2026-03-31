import streamlit as st
from PIL import Image
import os
import base64
from io import BytesIO

st.set_page_config(
    page_title="Atlas Pirakuá — PGTA",
    page_icon="🗺",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Paleta da identidade visual do atlas ────────────────────────────────────
TEAL      = "#1A8A5A"
DARK_TEAL = "#0D5535"
CREAM     = "#F5F0E8"
PARCHMENT = "#EDE8D8"
BROWN     = "#3D2010"
RED       = "#A03020"
GOLD      = "#C8A030"

st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Lato:wght@300;400;700&display=swap');

  /* ── reset Streamlit ─────────────────────── */
  #MainMenu, footer, header {{ visibility: hidden; }}
  .block-container {{ padding: 0 !important; max-width: 100% !important; }}
  section[data-testid="stSidebar"] {{ display: none; }}
  div[data-testid="stToolbar"] {{ display: none; }}

  /* ── base ────────────────────────────────── */
  body, .stApp {{ background-color: {CREAM}; font-family: 'Lato', sans-serif; }}

  /* ── borda indígena geométrica ───────────── */
  .border-band {{
      width: 100%; height: 22px; background-color: {TEAL};
      background-image:
          repeating-linear-gradient(90deg,
              {RED} 0px, {RED} 8px,
              transparent 8px, transparent 12px,
              {RED} 12px, {RED} 20px,
              transparent 20px, transparent 24px),
          repeating-linear-gradient(90deg,
              rgba(0,0,0,.3) 0px, rgba(0,0,0,.3) 2px,
              transparent 2px, transparent 22px);
  }}


  /* ── seção genérica ──────────────────────── */
  .sec {{ padding: 64px 48px; }}
  .sec-alt {{ background: {PARCHMENT}; }}
  .sec-title {{
      font-family: 'Playfair Display', serif; font-size: 2rem;
      color: {DARK_TEAL}; border-bottom: 3px solid {TEAL};
      padding-bottom: 10px; margin-bottom: 32px;
  }}
  .sec-title-center {{
      font-family: 'Playfair Display', serif; font-size: 2rem;
      color: {DARK_TEAL}; border-bottom: 3px solid {TEAL};
      padding-bottom: 10px; margin-bottom: 32px;
      text-align: center;
  }}
  .lead {{
      font-size: 1rem; color: {BROWN}; line-height: 1.95;
      max-width: 800px; margin-bottom: 0;
  }}
  .lead-center {{
      font-size: 1rem; color: {BROWN}; line-height: 1.95;
      max-width: 740px; margin: 0 auto 32px; text-align: center;
  }}

  /* ── stats ───────────────────────────────── */
  .stat-grid {{ display: flex; gap: 14px; flex-wrap: wrap; }}
  .stat-box {{
      background: {DARK_TEAL}; color: {CREAM};
      padding: 20px 24px; border-radius: 4px; text-align: center;
      flex: 1 1 130px;
  }}
  .stat-n {{
      font-family: 'Playfair Display', serif;
      font-size: 2.2rem; font-weight: 700; color: {GOLD};
      display: block; line-height: 1;
  }}
  .stat-l {{
      font-size: .7rem; letter-spacing: .18em; text-transform: uppercase;
      opacity: .82; margin-top: 6px; display: block;
  }}

  /* ── livro ───────────────────────────────── */
  .book-wrap {{
      position: relative;
      background: #fff;
      border-radius: 3px 8px 8px 3px;
      box-shadow:
          -6px 4px 14px rgba(0,0,0,.18),
           6px 4px 14px rgba(0,0,0,.18),
           0  8px 28px rgba(0,0,0,.28);
      overflow: hidden;
  }}
  .book-spine {{
      position: absolute; top: 0; left: 50%;
      width: 3px; height: 100%;
      background: linear-gradient(180deg,
          rgba(0,0,0,.08) 0%, rgba(0,0,0,.22) 50%, rgba(0,0,0,.08) 100%);
      z-index: 2;
  }}
  .book-wrap img {{ display: block; width: 100%; }}
  .book-nav {{
      display: flex; align-items: center; justify-content: center;
      gap: 24px; margin-top: 20px;
  }}
  .page-info {{
      font-family: 'Playfair Display', serif;
      font-size: 1rem; color: {BROWN};
      font-style: italic; min-width: 180px; text-align: center;
  }}
  .chap-label {{
      font-size: .72rem; font-weight: 700; letter-spacing: .3em;
      text-transform: uppercase; color: {RED}; text-align: center;
      margin-bottom: 6px;
  }}
  .chap-name {{
      font-family: 'Playfair Display', serif;
      font-size: 1.5rem; color: {BROWN}; text-align: center;
      margin-bottom: 8px;
  }}
  .chap-desc {{
      font-size: .92rem; color: #5A4030; line-height: 1.85;
      text-align: center; max-width: 740px; margin: 0 auto;
  }}

  /* ── equipe ──────────────────────────────── */
  .team-photo-wrap {{
      border-radius: 6px;
      overflow: hidden;
      box-shadow: 0 4px 20px rgba(0,0,0,.18);
  }}
  .org-card {{
      background: white;
      border-top: 4px solid {TEAL};
      padding: 20px;
      border-radius: 4px;
      text-align: center;
      box-shadow: 0 2px 10px rgba(0,0,0,.07);
      height: 100%;
  }}
  .org-name {{
      font-family: 'Playfair Display', serif;
      font-size: 1.1rem; color: {DARK_TEAL};
      font-weight: 700; margin-bottom: 6px;
  }}
  .org-desc {{ font-size: .88rem; color: #5A4030; line-height: 1.7; }}

  /* ── quote ───────────────────────────────── */
  .pull-quote {{
      border-left: 4px solid {GOLD};
      padding: 16px 24px;
      background: rgba(200,160,48,.07);
      font-family: 'Playfair Display', serif;
      font-size: 1.1rem; font-style: italic;
      color: {BROWN}; line-height: 1.8;
      border-radius: 0 4px 4px 0; margin: 0;
  }}

  /* ── footer ──────────────────────────────── */
  .site-footer {{
      background: #0A3D22;
      color: rgba(237,229,200,.65);
      padding: 52px 40px; text-align: center;
      font-family: 'Lato', sans-serif;
      font-size: .88rem; line-height: 2.1;
  }}
  .site-footer strong {{ color: {CREAM}; }}

  /* nav button style override */
  div[data-testid="stButton"] button {{
      background: {DARK_TEAL} !important;
      color: {CREAM} !important;
      border: none !important;
      border-radius: 3px !important;
      padding: 8px 28px !important;
      font-family: 'Lato', sans-serif !important;
      font-size: .85rem !important;
      letter-spacing: .12em !important;
      font-weight: 700 !important;
      text-transform: uppercase !important;
      transition: background .2s !important;
  }}
  div[data-testid="stButton"] button:hover {{
      background: {TEAL} !important;
  }}

  /* download button */
  div[data-testid="stDownloadButton"] button {{
      background: transparent !important;
      color: {DARK_TEAL} !important;
      border: 2px solid {TEAL} !important;
      border-radius: 3px !important;
      padding: 10px 28px !important;
      font-family: 'Lato', sans-serif !important;
      font-size: .85rem !important;
      letter-spacing: .15em !important;
      font-weight: 700 !important;
      text-transform: uppercase !important;
      transition: all .2s !important;
  }}
  div[data-testid="stDownloadButton"] button:hover {{
      background: {TEAL} !important;
      color: {CREAM} !important;
  }}
</style>
""", unsafe_allow_html=True)

# ── helpers ──────────────────────────────────────────────────────────────────
BASE = os.path.dirname(__file__)

def load_img(rel: str):
    p = os.path.join(BASE, rel)
    return Image.open(p) if os.path.exists(p) else None

def border():
    st.markdown('<div class="border-band"></div>', unsafe_allow_html=True)

# ── dados dos capítulos ───────────────────────────────────────────────────────
chapters = [
    {
        "num": "01", "title": "Rios",
        "path": "Imagens/01 - RIOS/01 - RIOS-1.png",
        "desc": (
            "Os rios são caminhos, memória e alimento. Mapeamento participativo das "
            "principais bacias hidrográficas do território Pirakuá, com afluentes e "
            "nascentes nomeados pelas próprias comunidades durante as caminhadas de campo."
        ),
    },
    {
        "num": "02", "title": "Casas",
        "path": "Imagens/02 - CASAS/02 - CASAS-1.png",
        "desc": (
            "As casas revelam a organização social e espacial das famílias Guarani. "
            "O mapa registra localizações, laços de parentesco, roças e espaços de "
            "convivência que estruturam a vida cotidiana no Pirakuá."
        ),
    },
    {
        "num": "03", "title": "Linha do Tempo",
        "path": "Imagens/03 - LINHA DO TEMPO/03 - LINHA DO TEMPO-1.png",
        "desc": (
            "Monitoramento da Vegetação (1985–2025) pelo índice NDVI. Quarenta anos de "
            "imagens de satélite mostram as transformações da cobertura vegetal e o "
            "esforço de recuperação ambiental conduzido pelas comunidades."
        ),
    },
    {
        "num": "04", "title": "Fazendas",
        "path": "Imagens/04 - FAZENDAS/04 - FAZENDAS-1.png",
        "desc": (
            "Sobreposição histórica de fazendas ao território Guarani — documentada a "
            "partir de cartografias dos anos 1938 e 1947. O capítulo evidencia como a "
            "expansão agropecuária avançou sobre as terras indígenas."
        ),
    },
    {
        "num": "05", "title": "Síntese Espacial",
        "path": "Imagens/05 - ÁREAS GERAL/05 - ÁREAS GERAL-1.png",
        "desc": (
            "Síntese Espacial das Representações Territoriais do Pirakuá. Os indígenas "
            "desenharam à mão suas percepções do território — locais de uso, convivência "
            "e espiritualidade — integradas às análises cartográficas do atlas."
        ),
    },
    {
        "num": "06", "title": "Cascavél",
        "path": "Imagens/06 - ÁREA CASCAVEL/06 - ÁREA CASCAVEL-1.png",
        "desc": (
            "Mapa de concentração espacial e uso da terra na área Cascavél, indicando "
            "zonas de maior pressão e regiões com maior resiliência ambiental, orientando "
            "as ações de manejo das comunidades."
        ),
    },
    {
        "num": "07", "title": "Piri",
        "path": "Imagens/07 - ÁREA PIRI/07 - ÁREA PIRI-1.png",
        "desc": (
            "A área Piri concentra importantes recursos hídricos e remanescentes de "
            "vegetação nativa. O mapa detalha a cobertura vegetal e os pontos de "
            "referência cultural identificados pelas famílias residentes."
        ),
    },
    {
        "num": "08", "title": "Palmeira",
        "path": "Imagens/08 - ÁREA PALMEIRA/08 - ÁREA PALMEIRA-1.png",
        "desc": (
            "A área Palmeira — nomeada pelas palmeiras nativas que marcam a paisagem — "
            "documenta cobertura vegetal e registra locais de coleta, pesca e cerimônias "
            "da territorialidade Guarani."
        ),
    },
    {
        "num": "09", "title": "Morro",
        "path": "Imagens/09 - ÁREA MORRO/09 - ÁREA MORRO-1.png",
        "desc": (
            "O Morro é referência topográfica e espiritual no território. As análises "
            "revelam padrões de uso tradicional e vetores de pressão que ameaçam a "
            "integridade ambiental e cultural deste espaço sagrado."
        ),
    },
    {
        "num": "10", "title": "Jaguary",
        "path": "Imagens/10 - ÁREA JAGUARY/10 - ÁREA JAGUARY-1.png",
        "desc": (
            "Jaguary encerra o atlas com uma das áreas de maior diversidade hídrica do "
            "território. Rios, corredores de mata ciliar e pontos de encontro entre "
            "as famílias Guarani Kaiowá estão cuidadosamente documentados."
        ),
    },
]

# ── session state ─────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = 0
if "carousel" not in st.session_state:
    st.session_state.carousel = 0

# ── helper base64 ─────────────────────────────────────────────────────────────
def to_b64(pil_img: Image.Image) -> str:
    buf = BytesIO()
    pil_img.convert("RGB").save(buf, format="JPEG", quality=92)
    return base64.b64encode(buf.getvalue()).decode()

# ── slides do carrossel ───────────────────────────────────────────────────────
nature_slides = [
    ("Imagens/Natureza/20251204_093514.jpg", "Rio no território Pirakuá"),
    ("Imagens/Natureza/n.jpg",               "Vista do território — cerrado e mata nativa"),
    ("Imagens/Natureza/20251204_134152.jpg",  "Paisagem do Pirakuá · Mato Grosso do Sul"),
    ("Imagens/Natureza/20251205_083418.jpg",  "Arte e cultura Guarani Kaiowá"),
]

# ── BORDA SUPERIOR ─────────────────────────────────────────────────────────────
border()

# ── HERO — carrossel de fotos da natureza ─────────────────────────────────────
cidx      = st.session_state.carousel % len(nature_slides)
c_path, c_caption = nature_slides[cidx]
c_img     = load_img(c_path)

if c_img:
    b64 = to_b64(c_img)
    st.markdown(f"""
<div style="position:relative; width:100%; height:75vh; min-height:500px; overflow:hidden;
            background-image:url('data:image/jpeg;base64,{b64}');
            background-size:cover; background-position:center; background-repeat:no-repeat;">
  <div style="position:absolute; inset:0;
              background:linear-gradient(to bottom,
                rgba(0,0,0,0.08) 0%,
                rgba(0,0,0,0.05) 45%,
                rgba(0,0,0,0.62) 100%);">
  </div>
  <div style="position:absolute; bottom:0; left:0; right:0; padding:44px 48px 36px;
              color:white; text-align:center;">
    <div style="font-size:.7rem; font-weight:700; letter-spacing:.5em;
                text-transform:uppercase; opacity:.72; margin-bottom:12px;">
      Plano de Gestão Territorial e Ambiental · TI Pirakuá
    </div>
    <div style="font-family:'Playfair Display',serif;
                font-size:clamp(3rem,8vw,6rem); font-weight:700;
                letter-spacing:.12em; text-transform:uppercase;
                text-shadow:0 3px 16px rgba(0,0,0,0.55);
                line-height:1; margin-bottom:10px;">
      Pirakuá
    </div>
    <div style="font-size:.95rem; letter-spacing:.28em; text-transform:uppercase;
                opacity:.82; margin-bottom:14px;">
      Atlas Territorial Guarani Kaiowá · Mato Grosso do Sul
    </div>
    <div style="font-size:.8rem; opacity:.6; font-style:italic;">
      {c_caption}
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    # navegação do carrossel
    nav_l, nav_c, nav_r = st.columns([2, 5, 2])
    with nav_l:
        if st.button("← Anterior", key="car_prev", use_container_width=True):
            st.session_state.carousel = (cidx - 1) % len(nature_slides)
            st.rerun()
    with nav_c:
        dots = '<div style="text-align:center; display:flex; justify-content:center; gap:10px; padding:10px 0;">'
        for i in range(len(nature_slides)):
            c = TEAL if i == cidx else "#A0C8A0"
            dots += f'<span style="display:inline-block; width:10px; height:10px; border-radius:50%; background:{c};"></span>'
        dots += '</div>'
        st.markdown(dots, unsafe_allow_html=True)
    with nav_r:
        if st.button("Próxima →", key="car_next", use_container_width=True):
            st.session_state.carousel = (cidx + 1) % len(nature_slides)
            st.rerun()

border()

# ── SOBRE ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="sec">', unsafe_allow_html=True)
ca, cb = st.columns([3, 2], gap="large")

with ca:
    st.markdown('<div class="sec-title">Sobre o Atlas</div>', unsafe_allow_html=True)
    st.markdown(f"""
<p class="lead">
O <strong>Atlas Territorial do Pirakuá</strong> é resultado de um processo de mapeamento
participativo que reuniu lideranças, anciãos e jovens das comunidades Guarani Kaiowá
com pesquisadores e apoiadores do <strong>PGTA — Plano de Gestão Territorial e Ambiental</strong>.
Cada página nasceu de caminhadas pelo território, rodas de conversa e oficinas de
cartografia social.
</p>
<br>
<div class="pull-quote">
  "A terra não pertence a nós — nós pertencemos à terra. Mapear é lembrar."
</div>
""", unsafe_allow_html=True)

with cb:
    st.markdown(f"""
<div style="display:grid; grid-template-columns:1fr 1fr; gap:16px; margin-top:8px;">

  <div style="background:white; border-top:3px solid {TEAL};
              padding:24px 16px; border-radius:4px; text-align:center;
              box-shadow:0 2px 10px rgba(0,0,0,.07);">
    <span style="font-family:'Playfair Display',serif; font-size:2.6rem;
                 font-weight:700; color:{DARK_TEAL}; display:block; line-height:1;">10</span>
    <span style="font-size:.68rem; letter-spacing:.18em; text-transform:uppercase;
                 color:#7A9070; margin-top:6px; display:block;">Capítulos</span>
  </div>

  <div style="background:white; border-top:3px solid {TEAL};
              padding:24px 16px; border-radius:4px; text-align:center;
              box-shadow:0 2px 10px rgba(0,0,0,.07);">
    <span style="font-family:'Playfair Display',serif; font-size:2.6rem;
                 font-weight:700; color:{DARK_TEAL}; display:block; line-height:1;">5</span>
    <span style="font-size:.68rem; letter-spacing:.18em; text-transform:uppercase;
                 color:#7A9070; margin-top:6px; display:block;">Áreas Territoriais</span>
  </div>

  <div style="background:white; border-top:3px solid {GOLD};
              padding:24px 16px; border-radius:4px; text-align:center;
              box-shadow:0 2px 10px rgba(0,0,0,.07);">
    <span style="font-family:'Playfair Display',serif; font-size:2.6rem;
                 font-weight:700; color:{DARK_TEAL}; display:block; line-height:1;">40+</span>
    <span style="font-size:.68rem; letter-spacing:.18em; text-transform:uppercase;
                 color:#7A9070; margin-top:6px; display:block;">Anos de Monitoramento</span>
  </div>

  <div style="background:white; border-top:3px solid {GOLD};
              padding:24px 16px; border-radius:4px; text-align:center;
              box-shadow:0 2px 10px rgba(0,0,0,.07);">
    <span style="font-family:'Playfair Display',serif; font-size:2.6rem;
                 font-weight:700; color:{DARK_TEAL}; display:block; line-height:1;">2</span>
    <span style="font-size:.68rem; letter-spacing:.18em; text-transform:uppercase;
                 color:#7A9070; margin-top:6px; display:block;">Municípios</span>
  </div>

</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── O ATLAS — VISUALIZADOR DE LIVRO ───────────────────────────────────────────
border()
st.markdown('<div class="sec sec-alt">', unsafe_allow_html=True)
st.markdown(f"""
<div style="text-align:center; font-family:'Playfair Display',serif; font-size:2rem;
            color:{DARK_TEAL}; border-bottom:3px solid {TEAL};
            padding-bottom:10px; margin-bottom:32px;">
  O Atlas
</div>""", unsafe_allow_html=True)

idx = st.session_state.page
ch  = chapters[idx]

# Título e descrição do capítulo
st.markdown(f"""
<div style="text-align:center; width:100%;">
  <div style="font-size:.72rem; font-weight:700; letter-spacing:.3em;
              text-transform:uppercase; color:{RED}; margin-bottom:6px;">
    Capítulo {ch["num"]} de {len(chapters)}
  </div>
  <div style="font-family:'Playfair Display',serif; font-size:1.6rem;
              color:{BROWN}; margin-bottom:12px; font-weight:700;">
    {ch["title"]}
  </div>
  <p style="font-size:.95rem; color:#3A5030; line-height:1.9;
            max-width:680px; margin:0 auto;">
    {ch["desc"]}
  </p>
</div>
""", unsafe_allow_html=True)

st.write("")  # espaçamento

# Imagem no estilo livro aberto — borda a borda
image = load_img(ch["path"])
if image:
    st.markdown('<div class="book-wrap"><div class="book-spine"></div>', unsafe_allow_html=True)
    st.image(image, use_container_width=True, output_format="PNG")
    st.markdown('</div>', unsafe_allow_html=True)

# Navegação
st.write("")
nav_l, nav_c, nav_r = st.columns([2, 3, 2])

with nav_l:
    if idx > 0:
        if st.button("← Página anterior", use_container_width=True):
            st.session_state.page -= 1
            st.rerun()

with nav_c:
    st.markdown(
        f'<div class="page-info">Página {idx + 1} de {len(chapters)}</div>',
        unsafe_allow_html=True
    )
    # mini índice de capítulos como pontos clicáveis
    dots_html = '<div style="text-align:center; margin-top:10px; display:flex; justify-content:center; gap:8px;">'
    for i, c in enumerate(chapters):
        active_color = TEAL if i == idx else "#C8B898"
        dots_html += f'<span title="{c["title"]}" style="display:inline-block; width:10px; height:10px; border-radius:50%; background:{active_color};"></span>'
    dots_html += '</div>'
    st.markdown(dots_html, unsafe_allow_html=True)

with nav_r:
    if idx < len(chapters) - 1:
        if st.button("Próxima página →", use_container_width=True):
            st.session_state.page += 1
            st.rerun()

# ── Botão de download — todas as imagens em ZIP ───────────────────────────────
import zipfile

@st.cache_data(show_spinner=False)
def build_zip() -> bytes:
    buf = BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for ch in chapters:
            full = os.path.join(BASE, ch["path"])
            if os.path.exists(full):
                arcname = f"{ch['num']} - {ch['title']}.png"
                zf.write(full, arcname)
    return buf.getvalue()

st.write("")
_, dl_col, _ = st.columns([3, 2, 3])
with dl_col:
    st.download_button(
        label="⬇ Baixar todas as imagens",
        data=build_zip(),
        file_name="Atlas_Pirakua.zip",
        mime="application/zip",
        use_container_width=True,
    )

st.markdown('</div>', unsafe_allow_html=True)

# ── EQUIPE PGTA ────────────────────────────────────────────────────────────────
border()
st.markdown('<div class="sec" style="padding-left:64px; padding-right:64px;">', unsafe_allow_html=True)
st.markdown(f"""
<div style="font-family:'Playfair Display',serif; font-size:2rem;
            color:{DARK_TEAL}; border-bottom:3px solid {TEAL};
            padding-bottom:10px; margin-bottom:24px;">
  Equipe PGTA — TI Pirakuá
</div>
<p style="font-size:1rem; color:{BROWN}; line-height:1.95; margin:0 0 36px;">
  O <strong>PGTA (Plano de Gestão Territorial e Ambiental)</strong> da Terra Indígena Pirakuá
  foi construído coletivamente. Agentes socioambientais indígenas, lideranças, pesquisadores
  e parceiros institucionais trabalharam juntos para registrar o território e planejar
  seu futuro de forma autônoma e participativa.
</p>
""", unsafe_allow_html=True)

# helper de recorte 4:3 (preserva mais das laterais)
def crop_square(image):
    w, h = image.size
    target_h = int(w * 3 / 4)
    if target_h <= h:
        top = (h - target_h) // 2
        return image.crop((0, top, w, top + target_h))
    else:
        target_w = int(h * 4 / 3)
        left = (w - target_w) // 2
        return image.crop((left, 0, left + target_w, h))

# 4 fotos em fila com mesmo recorte quadrado
fotos = [
    ("Imagens/Extra/equipe01.jpeg", "Equipe PGTA"),
    ("Imagens/Extra/equipe.jpg",    "Oficina de cartografia social"),
    ("Imagens/Extra/Logo01.jpeg",   "PGTA · Tekoha ñeñangarekóra"),
    ("Imagens/Extra/Logo.jpeg",     "CTI · RAIS · COPAIBAS"),
]

cols = st.columns(4, gap="medium")
for col, (path, caption) in zip(cols, fotos):
    image = load_img(path)
    if image:
        image = crop_square(image)
        with col:
            st.markdown('<div style="border-radius:6px; overflow:hidden; box-shadow:0 3px 14px rgba(0,0,0,.16);">', unsafe_allow_html=True)
            st.image(image, use_container_width=True, output_format="PNG")
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown(f'<p style="font-size:.75rem; color:#5A7050; font-style:italic; text-align:center; margin-top:6px;">{caption}</p>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── FOOTER ─────────────────────────────────────────────────────────────────────
border()
st.markdown(f"""
<div class="site-footer">
  <div style="font-family:'Playfair Display',serif; font-size:2rem;
              color:{CREAM}; letter-spacing:.15em; margin-bottom:14px;">
    PIRAKUÁ
  </div>
  <strong>Atlas Territorial Participativo · PGTA</strong><br>
  Terra Indígena Pirakuá · Povo Guarani Kaiowá<br>
  Ponta Porã e Bela Vista · Mato Grosso do Sul · Brasil<br><br>
  Realização: <strong>CTI · RAIS · COPAIBAS</strong><br>
  Os conhecimentos e representações territoriais pertencem ao povo Pirakuá.
</div>
""", unsafe_allow_html=True)
border()
