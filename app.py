import streamlit as st
from pathlib import Path
import random
import base64

st.set_page_config(page_title="Animais", page_icon="🐾", layout="centered")

ASSETS = Path("assets")

animals = {
    "cachorro": {"img": ASSETS/"cachorro.jpg", "sound": ASSETS/"cachorro.mp3"},
    "gato": {"img": ASSETS/"gato.jpg", "sound": ASSETS/"gato.mp3"},
    "passarinho": {"img": ASSETS/"vaca.jpg", "sound": ASSETS/"passarinho.mp3"},
    "pato": {"img": ASSETS/"pato.jpg", "sound": ASSETS/"pato.mp3"},
}

if "target" not in st.session_state:
    st.session_state.target = None
if "phase" not in st.session_state:
    st.session_state.phase = "play"
if "winner" not in st.session_state:
    st.session_state.winner = None


def audio_html(sound_path: Path):
    audio_bytes = open(sound_path, "rb").read()
    audio_b64 = base64.b64encode(audio_bytes).decode()

    return f"""
        <audio autoplay style="display:none;">
            <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
        </audio>
    """


def start_round():
    st.session_state.target = random.choice(list(animals.keys()))
    st.session_state.phase = "choose"
    st.session_state.winner = None


def choose(animal):
    if animal == st.session_state.target:
        st.session_state.winner = animal
        st.session_state.phase = "win"
    else:
        st.session_state.winner = False


st.markdown("<h1 style='text-align:center;'>🐾</h1>", unsafe_allow_html=True)


# ---------------- FASE PLAY ----------------
if st.session_state.phase == "play":

    if st.button("▶️", use_container_width=True):
        start_round()

    st.stop()


# ---------------- FASE CHOOSE ----------------
if st.session_state.phase == "choose":

    # TOCA SOM APÓS O CLIQUE REAL DO BOTÃO (agora permitido pelo navegador)
    st.markdown(audio_html(animals[st.session_state.target]["sound"]), unsafe_allow_html=True)

    animal_keys = list(animals.keys())
    random.shuffle(animal_keys)

    cols = st.columns(2)

    for i, animal in enumerate(animal_keys):
        with cols[i % 2]:
            if st.button(" ", key=f"btn_{animal}"):
                choose(animal)
            st.image(str(animals[animal]["img"]), use_container_width=True)

    st.stop()


# ---------------- FASE WIN ----------------
if st.session_state.phase == "win":

    if st.session_state.winner:
        st.markdown("<h1 style='text-align:center;'>🎉</h1>", unsafe_allow_html=True)
        st.image(animals[st.session_state.winner]["img"], width=300)
    else:
        st.markdown("<h1 style='text-align:center;'>❌</h1>", unsafe_allow_html=True)
        st.session_state.phase = "choose"

    if st.button("🔁", use_container_width=True):
        st.session_state.phase = "play"

    st.stop()
