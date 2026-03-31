import streamlit.components.v1 as components
import streamlit as st
from PIL import Image
import os
import base64
import zipfile
from io import BytesIO

st.set_page_config(
    page_title="Atlas Pirakua — PGTA",
    page_icon="🗺",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Paleta RAIS ───────────────────────────────────────────────────────────────
GREEN = "#3A6E3A"   # verde floresta RAIS
DARK_GREEN = "#1E4A1E"   # verde escuro
BG = "#FAFAF7"   # fundo quase branco
BG_ALT = "#F2F0EB"   # seção alternada
TEXT = "#2D2D2D"   # texto principal
MUTED = "#6B6B60"   # texto secundário
TERRA = "#8B3020"   # terracota (letras RAIS)
GOLD = "#B88A28"   # dourado suave
WHITE = "#FFFFFF"

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Roboto+Slab:wght@300;400;600;700&family=Roboto:wght@300;400;500;700&display=swap');

  #MainMenu, footer, header {{ visibility: hidden; }}
  .block-container {{ padding: 0 !important; max-width: 100% !important; }}
  section[data-testid="stSidebar"] {{ display: none; }}
  div[data-testid="stToolbar"] {{ display: none; }}

  body, .stApp {{
      background-color: {BG};
      font-family: 'Roboto', sans-serif;
      color: {TEXT};
  }}

  /* borda geométrica indígena */
  .border-band {{
      width: 100%; height: 20px;
      background-color: {GREEN};
      background-image:
          repeating-linear-gradient(90deg,
              {TERRA} 0px, {TERRA} 7px,
              transparent 7px, transparent 11px,
              {TERRA} 11px, {TERRA} 18px,
              transparent 18px, transparent 22px),
          repeating-linear-gradient(90deg,
              rgba(0,0,0,.25) 0px, rgba(0,0,0,.25) 2px,
              transparent 2px, transparent 20px);
  }}

  /* seções */
  .sec      {{ padding: 72px 80px; background: {BG}; }}
  .sec-alt  {{ padding: 72px 80px; background: {BG_ALT}; }}

  /* título de seção */
  .sec-h {{
      font-family: 'Roboto Slab', serif;
      font-size: 1.9rem; font-weight: 600;
      color: {DARK_GREEN};
      border-bottom: 2px solid {GREEN};
      padding-bottom: 10px; margin-bottom: 32px;
  }}
  .sec-h-center {{
      font-family: 'Roboto Slab', serif;
      font-size: 1.9rem; font-weight: 600;
      color: {DARK_GREEN};
      border-bottom: 2px solid {GREEN};
      padding-bottom: 10px; margin-bottom: 32px;
      text-align: center;
  }}

  /* texto corrido */
  .lead {{
      font-size: 1rem; color: {TEXT}; line-height: 1.9; max-width: 760px;
  }}

  /* destaque */
  .pull-quote {{
      border-left: 4px solid {GOLD};
      padding: 14px 22px;
      background: rgba(184,138,40,.06);
      font-family: 'Roboto Slab', serif;
      font-size: 1.05rem; font-style: italic;
      color: {TEXT}; line-height: 1.8;
      border-radius: 0 4px 4px 0; margin: 0;
  }}

  /* stats */
  .stat-card {{
      background: {WHITE};
      padding: 22px 12px; border-radius: 6px;
      text-align: center;
      box-shadow: 0 1px 6px rgba(0,0,0,.07);
      border-top: 3px solid {GREEN};
  }}
  .stat-n {{
      font-family: 'Roboto Slab', serif;
      font-size: 2.4rem; font-weight: 700;
      color: {DARK_GREEN}; display: block; line-height: 1;
  }}
  .stat-l {{
      font-size: .65rem; letter-spacing: .18em;
      text-transform: uppercase; color: {MUTED};
      margin-top: 6px; display: block;
  }}

  /* livro */
  .book-wrap {{
      position: relative; background: {WHITE};
      box-shadow: -4px 6px 18px rgba(0,0,0,.15),
                   4px 6px 18px rgba(0,0,0,.15),
                   0  10px 30px rgba(0,0,0,.22);
      overflow: hidden;
  }}
  .book-spine {{
      position: absolute; top: 0; left: 50%;
      width: 3px; height: 100%; z-index: 2;
      background: linear-gradient(180deg,
          rgba(0,0,0,.06) 0%, rgba(0,0,0,.18) 50%, rgba(0,0,0,.06) 100%);
  }}
  .page-info {{
      font-family: 'Roboto Slab', serif;
      font-size: .9rem; color: {MUTED};
      font-style: italic; text-align: center;
  }}

  /* footer */
  .site-footer {{
      background: {DARK_GREEN};
      color: rgba(255,255,255,.55);
      padding: 36px 80px;
      font-family: 'Roboto', sans-serif;
      font-size: .82rem; line-height: 1.5;
  }}
  .site-footer strong {{ color: #fff; }}

  /* botões navegação */
  div[data-testid="stButton"] button {{
      background: {DARK_GREEN} !important;
      color: #fff !important;
      border: none !important;
      border-radius: 4px !important;
      padding: 8px 24px !important;
      font-family: 'Roboto', sans-serif !important;
      font-size: .8rem !important;
      font-weight: 700 !important;
      letter-spacing: .12em !important;
      text-transform: uppercase !important;
      transition: background .2s !important;
  }}
  div[data-testid="stButton"] button:hover {{
      background: {GREEN} !important;
  }}

  /* botão download */
  div[data-testid="stDownloadButton"] button {{
      background: {TERRA} !important;
      color: #fff !important;
      border: none !important;
      border-radius: 4px !important;
      padding: 10px 24px !important;
      font-family: 'Roboto', sans-serif !important;
      font-size: .8rem !important;
      font-weight: 700 !important;
      letter-spacing: .15em !important;
      text-transform: uppercase !important;
      transition: all .2s !important;
  }}
  div[data-testid="stDownloadButton"] button:hover {{
      background: #6e2418 !important;
      color: #fff !important;
  }}

  /* lightbox modal */
  .lb-overlay {{
      position:fixed; top:0; left:0; width:100vw; height:100vh;
      background:rgba(0,0,0,.85); z-index:9999;
      display:none; align-items:center; justify-content:center;
      cursor:zoom-out;
  }}
  .lb-overlay.active {{ display:flex; }}
  .lb-overlay img {{
      max-width:90vw; max-height:90vh; object-fit:contain;
      border-radius:6px; box-shadow:0 0 40px rgba(0,0,0,.5);
  }}
  .lb-close {{
      position:fixed; top:18px; right:28px; font-size:2.4rem;
      color:#fff; cursor:pointer; z-index:10000;
      font-family:sans-serif; line-height:1;
  }}
  .lb-close:hover {{ color:#ccc; }}
  img.zoomable {{ cursor:zoom-in; transition:opacity .2s; }}
  img.zoomable:hover {{ opacity:.88; }}

  /* accordion equipe */
  details.equipe {{
      background: {WHITE};
      border-radius: 8px;
      box-shadow: 0 1px 6px rgba(0,0,0,.07);
      margin-bottom: 12px;
      border-left: 4px solid {GREEN};
      overflow: hidden;
  }}
  details.equipe[open] {{
      border-left-color: {TERRA};
  }}
  details.equipe summary {{
      padding: 16px 22px;
      font-family: 'Roboto Slab', serif;
      font-size: 1rem;
      font-weight: 600;
      color: {DARK_GREEN};
      cursor: pointer;
      list-style: none;
      display: flex;
      align-items: center;
      gap: 10px;
      transition: background .2s;
  }}
  details.equipe summary:hover {{
      background: rgba(58,110,58,.05);
  }}
  details.equipe summary::before {{
      content: "▸";
      font-size: 1.1rem;
      color: {GREEN};
      transition: transform .2s;
  }}
  details.equipe[open] summary::before {{
      transform: rotate(90deg);
      color: {TERRA};
  }}
  details.equipe summary::-webkit-details-marker {{ display: none; }}
  details.equipe .equipe-body {{
      padding: 4px 22px 20px 22px;
  }}
  details.equipe .equipe-body table {{
      width: 100%;
      border-collapse: collapse;
  }}
  details.equipe .equipe-body td {{
      padding: 8px 12px;
      font-size: .88rem;
      color: {TEXT};
      border-bottom: 1px solid #eee;
      vertical-align: top;
  }}
  details.equipe .equipe-body tr:last-child td {{
      border-bottom: none;
  }}
  details.equipe .equipe-body td:first-child {{
      font-weight: 500;
      white-space: nowrap;
  }}
  details.equipe .equipe-body td:last-child {{
      color: {MUTED};
      font-size: .82rem;
  }}
  .equipe-list {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
      gap: 6px 24px;
      padding: 0; margin: 0; list-style: none;
  }}
  .equipe-list li {{
      padding: 8px 0;
      font-size: .88rem;
      color: {TEXT};
      border-bottom: 1px solid #f0f0ec;
  }}
  .equipe-list li span {{
      font-size: .78rem;
      color: {MUTED};
  }}
</style>
""", unsafe_allow_html=True)

# ── lightbox JS (injeta no document principal do Streamlit) ───────────────────

components.html("""
<script>
(function(){
  var pd = window.parent.document;

  // Criar overlay se não existir
  if (!pd.getElementById('lbOverlay')) {
    var ov = pd.createElement('div');
    ov.id = 'lbOverlay';
    ov.style.cssText = 'position:fixed;top:0;left:0;width:100vw;height:100vh;background:rgba(0,0,0,.88);z-index:999999;display:none;align-items:center;justify-content:center;cursor:zoom-out;';
    ov.innerHTML = '<span id="lbClose" style="position:fixed;top:18px;right:28px;font-size:2.6rem;color:#fff;cursor:pointer;z-index:1000000;font-family:sans-serif;line-height:1;">&times;</span><img id="lbImg" src=\\\"\\\" style="max-width:90vw;max-height:90vh;object-fit:contain;border-radius:6px;box-shadow:0 0 40px rgba(0,0,0,.5);">';
    pd.body.appendChild(ov);

    ov.addEventListener('click', function(){ ov.style.display='none'; });
    pd.getElementById('lbClose').addEventListener('click', function(e){
      e.stopPropagation(); ov.style.display='none';
    });
    pd.addEventListener('keydown', function(e){
      if(e.key==='Escape') ov.style.display='none';
    });
  }

  // Anexar click handlers a todas imagens .zoomable
  function attach(){
    var imgs = pd.querySelectorAll('img.zoomable');
    for(var i=0;i<imgs.length;i++){
      if(!imgs[i].dataset.lbReady){
        imgs[i].dataset.lbReady='1';
        imgs[i].style.cursor='zoom-in';
        (function(img){
          img.addEventListener('click', function(){
            pd.getElementById('lbImg').src=img.src;
            pd.getElementById('lbOverlay').style.display='flex';
          });
        })(imgs[i]);
      }
    }
    setTimeout(attach, 2000);
  }
  setTimeout(attach, 800);
})();
</script>
""", height=0)

# ── helpers ───────────────────────────────────────────────────────────────────
BASE = os.path.dirname(__file__)


def load_img(rel: str) -> Image.Image | None:
    p = os.path.join(BASE, rel)
    return Image.open(p) if os.path.exists(p) else None


def to_b64(img: Image.Image, quality: int = 90) -> str:
    buf = BytesIO()
    img.convert("RGB").save(buf, format="JPEG", quality=quality)
    return base64.b64encode(buf.getvalue()).decode()


def to_b64_png(img: Image.Image) -> str:
    buf = BytesIO()
    img.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode()


def crop_43(img: Image.Image) -> Image.Image:
    w, h = img.size
    target_h = int(w * 3 / 4)
    if target_h <= h:
        top = (h - target_h) // 2
        return img.crop((0, top, w, top + target_h))
    target_w = int(h * 4 / 3)
    left = (w - target_w) // 2
    return img.crop((left, 0, left + target_w, h))


def border():
    st.markdown('<div class="border-band"></div>', unsafe_allow_html=True)


# ── capítulos ─────────────────────────────────────────────────────────────────
chapters = [
    {"num": "01", "title": "Rios",
     "path": "Imagens/01 - RIOS/01 - RIOS-1.png",
     "desc": "Os rios são caminhos, memória e alimento. Mapeamento participativo das principais bacias hidrográficas do território Pirakua, com afluentes e nascentes nomeados pelas próprias comunidades durante as caminhadas de campo."},
    {"num": "02", "title": "Casas",
     "path": "Imagens/02 - CASAS/02 - CASAS-1.png",
     "desc": "As casas revelam a organização social e espacial das famílias Guarani. O mapa registra localizações, laços de parentesco, roças e espaços de convivência que estruturam a vida cotidiana no Pirakua."},
    {"num": "03", "title": "Linha do Tempo",
     "path": "Imagens/03 - LINHA DO TEMPO/03 - LINHA DO TEMPO-1.png",
     "desc": "Monitoramento da Vegetação (1985–2025) pelo índice NDVI. Quarenta anos de imagens de satélite mostram as transformações da cobertura vegetal e o esforço de recuperação ambiental conduzido pelas comunidades."},
    {"num": "04", "title": "Fazendas",
     "path": "Imagens/04 - FAZENDAS/04 - FAZENDAS-1.png",
     "desc": "Sobreposição histórica de fazendas ao território Guarani — documentada a partir de cartografias dos anos 1938 e 1947. O capítulo evidencia como a expansão agropecuária avançou sobre as terras indígenas."},
    {"num": "05", "title": "Síntese Espacial",
     "path": "Imagens/05 - ÁREAS GERAL/05 - ÁREAS GERAL-1.png",
     "desc": "Síntese Espacial das Representações Territoriais do Pirakua. Os indígenas desenharam à mão suas percepções do território — locais de uso, convivência e espiritualidade — integradas às análises cartográficas."},
    {"num": "06", "title": "Cascavél",
     "path": "Imagens/06 - ÁREA CASCAVEL/06 - ÁREA CASCAVEL-1.png",
     "desc": "Mapa de concentração espacial e uso da terra na área Cascavél, indicando zonas de maior pressão e regiões com maior resiliência ambiental, orientando as ações de manejo das comunidades."},
    {"num": "07", "title": "Piri",
     "path": "Imagens/07 - ÁREA PIRI/07 - ÁREA PIRI-1.png",
     "desc": "A área Piri concentra importantes recursos hídricos e remanescentes de vegetação nativa. O mapa detalha a cobertura vegetal e os pontos de referência cultural identificados pelas famílias residentes."},
    {"num": "08", "title": "Palmeira",
     "path": "Imagens/08 - ÁREA PALMEIRA/08 - ÁREA PALMEIRA-1.png",
     "desc": "A área Palmeira — nomeada pelas palmeiras nativas que marcam a paisagem — documenta cobertura vegetal e registra locais de coleta, pesca e cerimônias da territorialidade Guarani."},
    {"num": "09", "title": "Morro",
     "path": "Imagens/09 - ÁREA MORRO/09 - ÁREA MORRO-1.png",
     "desc": "O Morro é referência topográfica e espiritual no território. As análises revelam padrões de uso tradicional e vetores de pressão que ameaçam a integridade ambiental e cultural deste espaço sagrado."},
    {"num": "10", "title": "Jaguary",
     "path": "Imagens/10 - ÁREA JAGUARY/10 - ÁREA JAGUARY-1.png",
     "desc": "Jaguary encerra o atlas com uma das áreas de maior diversidade hídrica do território. Rios, corredores de mata ciliar e pontos de encontro entre as famílias Guarani Kaiowá estão cuidadosamente documentados."},
]

# ── session state ─────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = 0
if "carousel" not in st.session_state:
    st.session_state.carousel = 0

# ── slides natureza ───────────────────────────────────────────────────────────
nature_slides = [
    ("Imagens/Natureza/20251204_093514.jpg", "Rio no território Pirakua"),
    ("Imagens/Natureza/n.jpg",
     "Vista do território — cerrado e mata nativa"),
    ("Imagens/Natureza/20251204_134152.jpg",
     "Paisagem do Pirakua · Mato Grosso do Sul"),
    ("Imagens/Natureza/20251205_083418.jpg",  "Arte e cultura Guarani Kaiowá"),
]

# ═══════════════════════════════════════════════════════════════════════════════
# HERO — carrossel de fotos
# ═══════════════════════════════════════════════════════════════════════════════
border()

cidx = st.session_state.carousel % len(nature_slides)
c_path, c_caption = nature_slides[cidx]
c_img = load_img(c_path)

if c_img:
    b64 = to_b64(c_img)
    st.markdown(f"""
<div style="position:relative; width:100%; height:75vh; min-height:500px; overflow:hidden;
            background-image:url('data:image/jpeg;base64,{b64}');
            background-size:cover; background-position:center;">
  <div style="position:absolute; inset:0;
              background:linear-gradient(to bottom,
                rgba(0,0,0,.05) 0%, rgba(0,0,0,.04) 40%, rgba(0,0,0,.60) 100%);">
  </div>
  <div style="position:absolute; bottom:0; left:0; right:0; padding:44px 60px 36px; text-align:center;">
    <div style="font-family:'Roboto',sans-serif; font-size:.7rem; font-weight:500;
                letter-spacing:.5em; text-transform:uppercase; color:rgba(255,255,255,.7); margin-bottom:12px;">
      Plano de Gestão Territorial e Ambiental · TI Pirakua
    </div>
    <div style="font-family:'Roboto Slab',serif; font-size:clamp(3rem,8vw,6rem); font-weight:700;
                letter-spacing:.1em; text-transform:uppercase; color:#fff;
                text-shadow:0 3px 16px rgba(0,0,0,.5); line-height:1; margin-bottom:10px;">
      Pirakua
    </div>
    <div style="font-family:'Roboto',sans-serif; font-size:.9rem; letter-spacing:.25em;
                text-transform:uppercase; color:rgba(255,255,255,.8); margin-bottom:12px;">
      Atlas Territorial Guarani Kaiowá · Mato Grosso do Sul
    </div>
    <div style="font-size:.78rem; color:rgba(255,255,255,.55); font-style:italic;">
      {c_caption}
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

    nav_l, nav_c, nav_r = st.columns([2, 5, 2])
    with nav_l:
        if st.button("← Anterior", key="car_prev", use_container_width=True):
            st.session_state.carousel = (cidx - 1) % len(nature_slides)
            st.rerun()
    with nav_c:
        dots = '<div style="text-align:center;display:flex;justify-content:center;gap:10px;padding:10px 0;">'
        for i in range(len(nature_slides)):
            c = GREEN if i == cidx else "#C0C8B8"
            dots += f'<span style="display:inline-block;width:9px;height:9px;border-radius:50%;background:{c};"></span>'
        dots += '</div>'
        st.markdown(dots, unsafe_allow_html=True)
    with nav_r:
        if st.button("Próxima →", key="car_next", use_container_width=True):
            st.session_state.carousel = (cidx + 1) % len(nature_slides)
            st.rerun()

border()

# ═══════════════════════════════════════════════════════════════════════════════
# SOBRE
# ═══════════════════════════════════════════════════════════════════════════════
_sc = f"font-family:'Roboto Slab',serif;font-size:1.9rem;font-weight:600;color:{DARK_GREEN};border-bottom:2px solid {GREEN};padding-bottom:10px;margin-bottom:28px;display:block;width:50vw;"
_pq = f"border-left:4px solid {GOLD};padding:14px 22px;background:rgba(184,138,40,.06);font-family:'Roboto Slab',serif;font-size:1.05rem;font-style:italic;color:{TEXT};line-height:1.8;border-radius:0 4px 4px 0;max-width:540px;"
st.markdown(f"""<div class="sec"><div style="display:flex;gap:60px;align-items:flex-start;flex-wrap:wrap;"><div style="flex:3;min-width:280px;"><div style="{_sc}">Sobre o Atlas</div><p style="font-size:1rem;color:{TEXT};line-height:1.9;max-width:580px;margin-bottom:24px;">O <strong>Atlas Territorial do Pirakua</strong> é resultado de um processo de mapeamento participativo que reuniu lideranças, anciãos e jovens das comunidades Guarani Kaiowá com pesquisadores e apoiadores do <strong>PGTA — Plano de Gestão Territorial e Ambiental</strong>. Cada página nasceu de caminhadas pelo território, rodas de conversa e oficinas de cartografia social.</p><div style="{_pq}">"A terra não pertence a nós — nós pertencemos à terra. Mapear é lembrar."</div></div><div style="flex:2;min-width:240px;"><div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:52px;"><div class="stat-card"><span class="stat-n">10</span><span class="stat-l">Capítulos</span></div><div class="stat-card"><span class="stat-n">5</span><span class="stat-l">Áreas Territoriais</span></div><div class="stat-card" style="border-top-color:{GOLD};"><span class="stat-n">40+</span><span class="stat-l">Anos de Monitoramento</span></div><div class="stat-card" style="border-top-color:{GOLD};"><span class="stat-n">2</span><span class="stat-l">Municípios</span></div></div></div></div></div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# O ATLAS — LIVRO
# ═══════════════════════════════════════════════════════════════════════════════
border()
st.markdown('<div class="sec-alt">', unsafe_allow_html=True)
st.markdown(f'<div class="sec-h-center">O Atlas</div>', unsafe_allow_html=True)

idx = st.session_state.page
ch = chapters[idx]

st.markdown(f"""
<div style="text-align:center; width:100%; margin-bottom:20px;">
  <div style="font-size:.7rem; font-weight:700; letter-spacing:.32em;
              text-transform:uppercase; color:{TERRA}; margin-bottom:6px;">
    Capítulo {ch["num"]} de {len(chapters)}
  </div>
  <div style="font-family:'Roboto Slab',serif; font-size:1.55rem; font-weight:600;
              color:{TEXT}; margin-bottom:10px;">
    {ch["title"]}
  </div>
  <p style="font-size:.95rem; color:{MUTED}; line-height:1.9;
            max-width:660px; margin:0 auto;">
    {ch["desc"]}
  </p>
</div>
""", unsafe_allow_html=True)

image = load_img(ch["path"])
if image:
    b64_atlas = to_b64_png(image)
    st.markdown(f'''
<div class="book-wrap"><div class="book-spine"></div>
  <img src="data:image/png;base64,{b64_atlas}" class="zoomable"
       style="width:100%; border-radius:0 6px 6px 0; display:block;">
</div>''', unsafe_allow_html=True)

st.write("")
nav_l, nav_c, nav_r = st.columns([2, 3, 2])

with nav_l:
    if idx > 0:
        if st.button("← Página anterior", use_container_width=True):
            st.session_state.page -= 1
            st.rerun()

with nav_c:
    st.markdown(
        f'<div class="page-info">Página {idx + 1} de {len(chapters)}</div>', unsafe_allow_html=True)
    dots_html = '<div style="text-align:center;margin-top:10px;display:flex;justify-content:center;gap:8px;">'
    for i, c in enumerate(chapters):
        col = GREEN if i == idx else "#C8C0B0"
        dots_html += f'<span title="{c["title"]}" style="display:inline-block;width:9px;height:9px;border-radius:50%;background:{col};"></span>'
    dots_html += '</div>'
    st.markdown(dots_html, unsafe_allow_html=True)

with nav_r:
    if idx < len(chapters) - 1:
        if st.button("Próxima página →", use_container_width=True):
            st.session_state.page += 1
            st.rerun()

# download


@st.cache_data(show_spinner=False)
def build_zip() -> bytes:
    buf = BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for ch in chapters:
            full = os.path.join(BASE, ch["path"])
            if os.path.exists(full):
                zf.write(full, f"{ch['num']} - {ch['title']}.png")
    return buf.getvalue()


st.write("")
_, dl_col, _ = st.columns([3, 2, 3])
with dl_col:
    st.download_button(
        label="↓  Baixar todas as imagens",
        data=build_zip(),
        file_name="Atlas_Pirakua.zip",
        mime="application/zip",
        use_container_width=True,
    )

st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# EQUIPE PGTA
# ═══════════════════════════════════════════════════════════════════════════════
border()
st.markdown('<div class="sec">', unsafe_allow_html=True)

st.markdown(f"""
<div class="sec-h">Equipe PGTA — TI Pirakua</div>
<p class="lead" style="margin-bottom:36px;text-align:center;max-width:700px;margin-left:auto;margin-right:auto;">
    O <strong>PGTA (Plano de Gestão Territorial e Ambiental)</strong> da Terra Indígena Pirakua
    foi construído coletivamente. Agentes socioambientais indígenas, lideranças, pesquisadores
    e parceiros institucionais trabalharam juntos para registrar o território e planejar
    seu futuro de forma autônoma e participativa.
  </p>
""", unsafe_allow_html=True)

# ── fotos em HTML puro (sem colunas Streamlit) ────────────────────────────────
img_main = load_img("Imagens/Extra/equipe01.jpeg")
img_sec = load_img("Imagens/Extra/equipe.jpg")

if img_main and img_sec:
    b64_main = to_b64(crop_43(img_main))
    b64_sec  = to_b64(crop_43(img_sec))
    st.markdown(f"""
<div style="display:grid; grid-template-columns:1fr 1fr; gap:20px; margin-bottom:56px;
            max-width:760px; margin-left:auto; margin-right:auto;">

  <div>
    <div style="overflow:hidden; border-radius:8px;
                box-shadow:0 4px 20px rgba(0,0,0,.12); height:220px;">
      <img src="data:image/jpeg;base64,{b64_main}" class="zoomable"
           style="width:100%; height:100%; display:block; object-fit:cover; object-position:center top;">
    </div>
    <p style="font-size:.75rem; color:{MUTED}; font-style:italic;
              text-align:center; margin-top:10px;">
      Equipe PGTA — Agentes Socioambientais e pesquisadores da TI Pirakua
    </p>
  </div>

  <div>
    <div style="overflow:hidden; border-radius:8px;
                box-shadow:0 4px 20px rgba(0,0,0,.12); height:220px;">
      <img src="data:image/jpeg;base64,{b64_sec}" class="zoomable"
           style="width:100%; height:100%; display:block; object-fit:cover; object-position:center top;">
    </div>
    <p style="font-size:.75rem; color:{MUTED}; font-style:italic;
              text-align:center; margin-top:10px;">
      Oficina de cartografia social e planejamento participativo
    </p>
  </div>

</div>
""", unsafe_allow_html=True)

# ── Membros da equipe (accordions) ────────────────────────────────────────────
st.markdown(f"""
<div style="max-width:900px; margin:0 auto 56px auto;">

  <div style="font-family:'Roboto Slab',serif; font-size:1.2rem; font-weight:600;
              color:{DARK_GREEN}; margin-bottom:20px; text-align:center;">
    Membros da Equipe
  </div>

  <details class="equipe">
    <summary>Coordenação e Técnicos</summary>
    <div class="equipe-body">
      <table>
        <tr><td>José Henrique Prado</td><td>Coordenador (RAIS)</td></tr>
        <tr><td>Arnulfo Morinigo Caballero</td><td>Consultor Técnico (RAIS)</td></tr>
        <tr><td>Graciela Alves</td><td>Administrativo e financeiro (RAIS)</td></tr>
        <tr><td>Levi Marques Pereira</td><td>RAIS — contrapartida</td></tr>
        <tr><td>Gustavo Costa do Carmo</td><td>RAIS</td></tr>
        <tr><td>Gabriel Ulian</td><td>Relatoria e sistematização de dados (dez. 2025)</td></tr>
        <tr><td>Andrey Gaspar Sorrilha</td><td>Geoprocessamento (dez. 2025)</td></tr>
      </table>
    </div>
  </details>

  <details class="equipe">
    <summary>Consultores Indígenas</summary>
    <div class="equipe-body">
      <table>
        <tr><td>Júnior Joel Lopes Machado</td><td>Pirakua</td></tr>
        <tr><td>Inair Lopes</td><td>Pirakua</td></tr>
        <tr><td>Jorge Gomes</td><td>Pirakua</td></tr>
      </table>
    </div>
  </details>

  <details class="equipe">
    <summary>Agentes Socioambientais</summary>
    <div class="equipe-body">
      <ul class="equipe-list">
        <li>Luzia <span>· Palmeiras</span></li>
        <li>Rosilene <span>· Palmeiras</span></li>
        <li>Marciano <span>· Ponte / Jaguari</span></li>
        <li>Lisandra <span>· Ponte / Jaguari</span></li>
        <li>Juvelina <span>· Piri</span></li>
        <li>Robeson <span>· Piri</span></li>
        <li>Esmeralda <span>· Piri</span></li>
        <li>Claines <span>· Piri</span></li>
        <li>Silvia <span>· Piri</span></li>
        <li>Sandro <span>· Morro</span></li>
        <li>Frank <span>· Morro</span></li>
        <li>Elda <span>· Cascavel</span></li>
      </ul>
    </div>
  </details>

</div>
""", unsafe_allow_html=True)

# ── logos parceiros em HTML puro ──────────────────────────────────────────────
logos_def = [
    ("Imagens/logos/RAIS.jpg.jpeg",      "RAIS"),
    ("Imagens/logos/CTI.jpg.jpeg",        "CTI"),
    ("Imagens/logos/Copaíbas.jpg.jpeg",   "COPAÍBAS"),
    ("Imagens/logos/Aty Guasu.jpg.jpeg",  "Aty Guasu"),
    ("Imagens/logos/FUNBIO.jpg.jpeg",     "FUNBIO"),
    ("Imagens/logos/NICFI.jpg.jpeg",      "NICFI"),
]

logos_items = ""
for path, name in logos_def:
    img_l = load_img(path)
    if img_l:
        b64_l = to_b64(img_l)
        logos_items += f"""
<div style="display:flex; flex-direction:column; align-items:center; gap:10px;
            flex:1 1 190px; max-width:260px;">
  <div style="background:{WHITE}; border-radius:8px; padding:24px 20px;
              box-shadow:0 1px 6px rgba(0,0,0,.07); width:100%;
              display:flex; align-items:center; justify-content:center;
              min-height:140px;">
    <img src="data:image/jpeg;base64,{b64_l}" alt="{name}" class="zoomable"
         style="max-height:120px; max-width:100%; width:auto; object-fit:contain;">
  </div>
  <span style="font-size:.8rem; font-weight:500; color:{MUTED};
               letter-spacing:.06em; text-align:center;">{name}</span>
</div>"""

st.markdown(f"""
<div style="border-top:1px solid #E0DDD6; padding-top:36px;">
  <div style="font-family:'Roboto',sans-serif; font-size:.75rem; font-weight:700;
              letter-spacing:.2em; text-transform:uppercase; color:{MUTED};
              margin-bottom:24px; text-align:center;">
    Parceiros e Realizadores
  </div>
  <div style="display:flex; align-items:flex-start; justify-content:center;
              gap:24px; flex-wrap:wrap;">
    {logos_items}
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════════
border()
_yt_icon = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="rgba(255,255,255,.8)"><path d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.5 3.5 12 3.5 12 3.5s-7.5 0-9.4.5A3 3 0 0 0 .5 6.2C0 8.1 0 12 0 12s0 3.9.5 5.8a3 3 0 0 0 2.1 2.1c1.9.5 9.4.5 9.4.5s7.5 0 9.4-.5a3 3 0 0 0 2.1-2.1C24 15.9 24 12 24 12s0-3.9-.5-5.8zM9.8 15.5V8.5l6.3 3.5-6.3 3.5z"/></svg>'
_ig_icon = '<svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="rgba(255,255,255,.8)"><path d="M12 2.2c3.2 0 3.6 0 4.9.1 3.3.1 4.8 1.7 4.9 4.9.1 1.3.1 1.6.1 4.8s0 3.6-.1 4.8c-.1 3.2-1.6 4.8-4.9 4.9-1.3.1-1.6.1-4.9.1s-3.6 0-4.8-.1c-3.3-.1-4.8-1.7-4.9-4.9C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.8C2.4 3.9 3.9 2.3 7.2 2.3 8.4 2.2 8.8 2.2 12 2.2zm0-2.2C8.7 0 8.3 0 7.1.1 2.7.3.3 2.7.1 7.1 0 8.3 0 8.7 0 12s0 3.7.1 4.9c.2 4.4 2.6 6.8 7 7C8.3 24 8.7 24 12 24s3.7 0 4.9-.1c4.4-.2 6.8-2.6 7-7C24 15.7 24 15.3 24 12s0-3.7-.1-4.9c-.2-4.4-2.6-6.8-7-7C15.7 0 15.3 0 12 0zm0 5.8a6.2 6.2 0 1 0 0 12.4A6.2 6.2 0 0 0 12 5.8zm0 10.2a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm6.4-11.8a1.4 1.4 0 1 0 0 2.8 1.4 1.4 0 0 0 0-2.8z"/></svg>'

_icon_style = "display:flex;align-items:center;justify-content:center;width:38px;height:38px;border-radius:50%;background:rgba(255,255,255,.1);text-decoration:none;"

st.markdown(
    f"""<div class="site-footer"><div style="display:flex;align-items:flex-start;justify-content:space-between;flex-wrap:wrap;gap:24px;"><div style="max-width:280px;"><div style="font-family:'Roboto Slab',serif;font-size:1.2rem;font-weight:700;color:#fff;letter-spacing:.1em;text-transform:uppercase;margin-bottom:6px;">Pirakua</div><div style="font-size:.78rem;color:rgba(255,255,255,.5);line-height:1.6;">Atlas Territorial Participativo · PGTA<br>Terra Indígena Pirakua · Povo Guarani Kaiowá<br>Ponta Porã e Bela Vista · MS · Brasil</div></div><div style="display:flex;flex-direction:column;align-items:center;gap:12px;"><div style="font-size:.65rem;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:rgba(255,255,255,.35);">Siga nas redes</div><div style="display:flex;gap:14px;align-items:center;"><a href="https://www.youtube.com/@rederais" target="_blank" style="{_icon_style}" title="YouTube RAIS">{_yt_icon}</a><a href="https://www.instagram.com/rederais/" target="_blank" style="{_icon_style}" title="Instagram RAIS">{_ig_icon}</a></div></div><div style="max-width:300px;text-align:right;"><div style="font-size:.65rem;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:rgba(255,255,255,.35);margin-bottom:6px;">Realização</div><div style="font-size:.78rem;color:rgba(255,255,255,.6);margin-bottom:14px;line-height:1.7;"><strong style="color:rgba(255,255,255,.85);">RAIS · CTI · COPAÍBAS</strong><br><strong style="color:rgba(255,255,255,.85);">Aty Guasu · FUNBIO · NICFI</strong></div><div style="font-size:.72rem;color:rgba(255,255,255,.3);line-height:1.6;">©2025 · Os conhecimentos e representações<br>territoriais pertencem ao povo Pirakua.</div></div></div></div>""", unsafe_allow_html=True)
border()
