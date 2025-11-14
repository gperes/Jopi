import streamlit as st
from pathlib import Path
import random
import base64

st.set_page_config(page_title="Animais", page_icon="🐾", layout="centered")

ASSETS = Path("assets")

animals = {
    "cachorro": {"img": ASSETS / "cachorro.jpg", "sound": ASSETS / "cachorro.mp3"},
    "gato": {"img": ASSETS / "gato.jpg", "sound": ASSETS / "gato.mp3"},
    "passarinho": {"img": ASSETS / "passarinho.jpg", "sound": ASSETS / "passarinho.mp3"},
    "pato": {"img": ASSETS / "pato.jpg", "sound": ASSETS / "pato.mp3"},
}

# ---------------- ESTADO ----------------
if "target" not in st.session_state:
    st.session_state.target = None          # qual animal é o certo
if "phase" not in st.session_state:
    st.session_state.phase = "play"         # play -> choose -> win
if "winner" not in st.session_state:
    st.session_state.winner = None          # nome do vencedor ou False (erro)


# ---------------- HELPER: áudio invisível em loop ----------------
def audio_html(sound_path: Path) -> str:
    audio_bytes = open(sound_path, "rb").read()
    audio_b64 = base64.b64encode(audio_bytes).decode()

    # autoplay + loop + escondido
    return f"""
        <audio autoplay loop style="display:none;">
            <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
        </audio>
    """


# ---------------- LÓGICA ----------------
def start_round():
    """Inicia uma nova rodada."""
    st.session_state.target = random.choice(list(animals.keys()))
    st.session_state.phase = "choose"
    st.session_state.winner = None


def choose(animal: str):
    """Processa a escolha da criança."""
    if animal == st.session_state.target:
        st.session_state.winner = animal
        st.session_state.phase = "win"
    else:
        st.session_state.winner = False    # errou, mas continua na fase choose


# ---- Captura clique vindo dos links das imagens (?choice=animal) ----
params = st.experimental_get_query_params()
clicked = params.get("choice", [None])[0]
if clicked:
    choose(clicked)
    # limpa a URL para não ficar repetindo a escolha
    st.experimental_set_query_params()


# ---------------- LAYOUT ----------------
st.markdown("<h1 style='text-align:center;'>🐾</h1>", unsafe_allow_html=True)


# ---------- FASE PLAY (só o botão ▶️) ----------
if st.session_state.phase == "play":
    if st.button("▶️", use_container_width=True):
        start_round()

# ---------- FASE CHOOSE (som + imagens clicáveis) ----------
if st.session_state.phase == "choose":
    # toca o som do animal-alvo em loop
    st.markdown(
        audio_html(animals[st.session_state.target]["sound"]),
        unsafe_allow_html=True
    )

    # embaralha e mostra as imagens
    animal_keys = list(animals.keys())
    random.shuffle(animal_keys)

    cols = st.columns(2)

    for i, animal in enumerate(animal_keys):
        img_bytes = open(animals[animal]["img"], "rb").read()
        img_b64 = base64.b64encode(img_bytes).decode()

        # cada imagem é um link clicável: ?choice=animal
        img_html = f"""
        <div style="text-align:center; margin-bottom:20px;">
            <a href="?choice={animal}">
                <img src="data:image/jpeg;base64,{img_b64}"
                     style="width:100%; border-radius:10px; cursor:pointer;" />
            </a>
        </div>
        """

        with cols[i % 2]:
            st.markdown(img_html, unsafe_allow_html=True)

# ---------- FASE WIN (mostra só o vencedor) ----------
if st.session_state.phase == "win":
    # aqui o som para, porque não estamos mais renderizando a tag <audio>
    if st.session_state.winner:
        st.markdown(
            "<h1 style='text-align:center;'>🎉</h1>",
            unsafe_allow_html=True
        )
        st.image(animals[st.session_state.winner]["img"], width=300)
    else:
        st.markdown(
            "<h1 style='text-align:center;'>❌</h1>",
            unsafe_allow_html=True
        )
        # se quiser, pode voltar direto para choose aqui

    if st.button("🔁", use_container_width=True):
        st.session_state.phase = "play"
