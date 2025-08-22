import streamlit as st
import time

# initialize state
if "hunger" not in st.session_state:
    st.session_state.hunger = 50
    st.session_state.happiness = 50
    st.session_state.name = "Coco"
    st.session_state.alive = True

st.set_page_config(page_title="Virtual Pet Game", page_icon="🐾")
st.title("🐶 Virtual Pet Game 🐾")
st.write(f"Say hi to **{st.session_state.name}**!")

# show pet status
st.write("### Pet Status")
st.progress(st.session_state.hunger / 100)
st.write(f"Hunger: {st.session_state.hunger}/100")
st.progress(st.session_state.happiness / 100)
st.write(f"Happiness: {st.session_state.happiness}/100")

# action buttons
feed, play, rest = st.columns(3)

if feed.button("🍖 Feed"):
    st.session_state.hunger = max(0, st.session_state.hunger - 20)
    st.session_state.happiness = max(0, st.session_state.happiness - 5)
    st.success(f"You fed {st.session_state.name}!")

if play.button("🎾 Play"):
    st.session_state.happiness = min(100, st.session_state.happiness + 20)
    st.session_state.hunger = min(100, st.session_state.hunger + 10)
    st.success(f"You played with {st.session_state.name}!")

if rest.button("😴 Rest"):
    st.session_state.hunger = min(100, st.session_state.hunger + 2)
    st.session_state.happiness = min(100, st.session_state.happiness + 2)
    st.info(f"{st.session_state.name} is resting...")

# auto decay over time
time.sleep(1)
st.session_state.hunger = min(100, st.session_state.hunger + 1)
st.session_state.happiness = max(0, st.session_state.happiness - 1)

# game over conditions
if st.session_state.hunger >= 100:
    st.error(f"Oh no! {st.session_state.name} starved 💀")
    st.session_state.alive = False

if st.session_state.happiness <= 0:
    st.error(f"Oh no! {st.session_state.name} is too sad 💔")
    st.session_state.alive = False
