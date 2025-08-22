import streamlit as st
import random
import time

# initialize pets
if "pets" not in st.session_state:
    st.session_state.pets = {}
if "active_pet" not in st.session_state:
    st.session_state.active_pet = None

st.set_page_config(page_title="Virtual Pet Game", page_icon="🐾")
st.title("🐶 Virtual Pet Game with Extras")

# --- Add or select pets ---
st.sidebar.header("🐾 Pet Management")

# add new pet
with st.sidebar.form("add_pet_form"):
    new_pet_name = st.text_input("Enter a name for your pet:")
    if st.form_submit_button("Add Pet") and new_pet_name.strip():
        if new_pet_name not in st.session_state.pets:
            st.session_state.pets[new_pet_name] = {
                "hunger": 50,
                "happiness": 50,
                "health": 100,
                "alive": True,
                "last_event": ""
            }
            st.session_state.active_pet = new_pet_name
        else:
            st.warning("Pet already exists!")

# choose active pet
if st.session_state.pets:
    chosen = st.sidebar.radio("Choose your pet:", list(st.session_state.pets.keys()))
    st.session_state.active_pet = chosen

# --- Gameplay for active pet ---
if st.session_state.active_pet:
    pet = st.session_state.pets[st.session_state.active_pet]

    if pet["alive"]:
        st.subheader(f"Meet {st.session_state.active_pet} 🐾")

        # display stats
        st.write("### Status")
        st.progress(pet["hunger"] / 100)
        st.write(f"Hunger: {pet['hunger']}/100")
        st.progress(pet["happiness"] / 100)
        st.write(f"Happiness: {pet['happiness']}/100")
        st.progress(pet["health"] / 100)
        st.write(f"Health: {pet['health']}/100")

        # actions
        col1, col2, col3, col4, col5 = st.columns(5)
        if col1.button("🍖 Feed"):
            pet["hunger"] = max(0, pet["hunger"] - 20)
            pet["happiness"] = max(0, pet["happiness"] - 5)
            st.success(f"You fed {st.session_state.active_pet}!")

        if col2.button("🎾 Play"):
            pet["happiness"] = min(100, pet["happiness"] + 20)
            pet["hunger"] = min(100, pet["hunger"] + 10)
            st.success(f"You played with {st.session_state.active_pet}!")

        if col3.button("😴 Rest"):
            pet["hunger"] = min(100, pet["hunger"] + 5)
            pet["happiness"] = min(100, pet["happiness"] + 5)
            st.info(f"{st.session_state.active_pet} is resting...")

        if col4.button("🎁 Toy"):
            pet["happiness"] = min(100, pet["happiness"] + 15)
            st.success(f"{st.session_state.active_pet} loved the toy!")

        if col5.button("💊 Medicine"):
            pet["health"] = min(100, pet["health"] + 20)
            pet["happiness"] = max(0, pet["happiness"] - 5)
            st.success(f"You gave medicine to {st.session_state.active_pet}!")

        # random events
        if random.random() < 0.2:  # 20% chance each run
            event = random.choice(["snack", "sick"])
            if event == "snack":
                pet["hunger"] = max(0, pet["hunger"] - 10)
                pet["last_event"] = f"{st.session_state.active_pet} found a snack 🍪!"
            elif event == "sick":
                pet["health"] = max(0, pet["health"] - 15)
                pet["last_event"] = f"Oh no! {st.session_state.active_pet} got sick 🤒"
        if pet["last_event"]:
            st.warning(pet["last_event"])
            pet["last_event"] = ""

        # natural decay
        time.sleep(1)
        pet["hunger"] = min(100, pet["hunger"] + 1)
        pet["happiness"] = max(0, pet["happiness"] - 1)
        pet["health"] = max(0, pet["health"] - 1 if pet["hunger"] > 80 else pet["health"])

        # game over conditions
        if pet["hunger"] >= 100:
            st.error(f"{st.session_state.active_pet} starved 💀")
            pet["alive"] = False
        elif pet["happiness"] <= 0:
            st.error(f"{st.session_state.active_pet} is too sad 💔")
            pet["alive"] = False
        elif pet["health"] <= 0:
            st.error(f"{st.session_state.active_pet} is too sick 💊💀")
            pet["alive"] = False
    else:
        st.error(f"{st.session_state.active_pet} has passed away. 🪦")
else:
    st.info("👉 Add a pet from the sidebar to start playing!")
