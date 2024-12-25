import streamlit as st
import json
import random

# Load all words and create a list of 34 lists each with 20 words
def create_word_sets(filepath, set_size=20, num_sets=34):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        all_words = data["gre_words"]
    except FileNotFoundError:
        st.error("Could not find the json file, please check the file path")
        return None
    except json.JSONDecodeError:
        st.error("The json file could not be decoded. Ensure that it is proper json and check encoding")
        return None
    if not all_words:
        st.error("The json file is empty.")
        return None

    random.shuffle(all_words)
    word_sets = []
    for i in range(num_sets):
        start = i * set_size
        end = start + set_size
        word_sets.append(all_words[start:end])

    return word_sets

st.set_page_config(
    page_title="Vocab",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] > .main {
        background-color: #000000; /* Red Background */
        color: #ffffff;
    }
        body {
            font-family: 'Roboto', sans-serif;  
        }
        .stButton>button {
            background-color: #000000; /* Pastel blue */
            color: #ffffff !important; /* Black text */
            border: 2px solid #87ceeb; /* Lighter blue border */
            border-radius: 15px !important;
            padding: 10px 15px !important;
            margin: 5px !important;
            transition: all 0.3s ease; /* Smooth hover effect */
        }
        .stButton>button:hover {
            background-color: #87ceeb; /* Slightly darker pastel blue on hover */
            border-color: #add8e6;
        }
         .stTextInput>div>div>input {
            background-color: #333333 !important; /* Dark grey */
            color: #ffffff !important; /* Light text */
            border: 1px solid #add8e6;
            border-radius: 10px;
        }
        h1, h2, h3, .css-10trblm {
            color: #ffffff; /* White text */
        }
        .card {
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            cursor: pointer;
            margin: 10px;
            border: 2px solid #add8e6; /* Pastel blue border */
            transition: transform 0.3s ease;
        }
        .card:hover {
            transform: scale(1.05); /* Enlarge card slightly on hover */
            border-color: #ffffff; /* White border on hover */
        }
        .card h2 {
            margin-bottom: 0;
            color: #ffffff; /* White text */
        }
         .css-10trblm{
            color: #ffffff; /* This also targets headers in markdown */
        }
    </style>
""", unsafe_allow_html=True)

def main():
    filepath = "final.json"
    word_sets = create_word_sets(filepath)

    if word_sets is None:
        return

    if 'current_card_index' not in st.session_state:
        st.session_state['current_card_index'] = 0

    if 'current_set_index' not in st.session_state:
        st.session_state['current_set_index'] = None

    if st.session_state['current_set_index'] is None: # Display the Home Screen
        st.title("Vocab Explorer") 
        st.header("Select a Day: ")

        cols = st.columns(6)

        for day in range(len(word_sets)):
            with cols[day % 6]:
                if st.button(f"Day {day + 1}", key=f"day_button_{day}", use_container_width=True):
                    st.session_state['current_set_index'] = day
                    st.session_state['current_card_index'] = 0
                    st.rerun()

    else:   # Display Flashcard content
        current_set = word_sets[st.session_state['current_set_index']]
        current_word = current_set[st.session_state['current_card_index']]

        st.header(f"{current_word['word']}")
        st.write(f"**Meaning:** {current_word['meaning']}")
        st.write(f"**Example:** {current_word['example']}")
        st.write(f"**Synonyms:** {', '.join(current_word['synonyms'])}")
        st.write(f"**Mnemonic:** {current_word['mnemonic']}")
        st.write("")  
        st.write("")
        st.write("")  
        st.write("") 
        col1, col2, col3 = st.columns(3)

        with col1:

            if st.button("Previous", disabled=st.session_state['current_card_index'] == 0):
                st.session_state['current_card_index'] -= 1
                st.rerun()

        with col3:
            if st.button("Next", disabled=st.session_state['current_card_index'] == len(current_set) - 1):
                st.session_state['current_card_index'] += 1
                st.rerun()
        with col2:
             st.markdown(f"Card: {st.session_state['current_card_index'] + 1} of {len(current_set)}")

        if st.session_state['current_card_index'] == len(current_set): # Redirect to home page
            st.session_state['current_set_index'] = None
            st.rerun()

if __name__ == "__main__":
    main()