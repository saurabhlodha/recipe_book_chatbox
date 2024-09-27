import streamlit as st

all_cuisines = [
    {"name": "Indian", "image": f"assets/indian.jpg"},
    {"name": "Asian", "image": f"assets/asian.jpg"},
    {"name": "Healthy", "image": f"assets/healthy.jpg"},
    {"name": "Vegan", "image": f"assets/vegan.jpg"},
    {"name": "Desserts", "image": f"assets/desserts.jpg"},
    {"name": "Low Calorie", "image": f"assets/low-calorie.jpeg"}
]

def display_cuisine(cuisine, key):
    st.image(cuisine["image"], width=150)
    st.text(cuisine["name"])
    if st.button(f"{cuisine['name']} recipes", key=key):
        st.session_state.selected_cuisine = cuisine['name']
        st.switch_page("pages/Chat.py")

st.title("Choose your desired cuisine")

# Search bar
search_query = st.text_input("Search for a cuisine")

# Filter freedom cuisines based on search query
filtered_cuisines = [cuisine for cuisine in all_cuisines if search_query.lower() in cuisine['name'].lower()]

# Display freedom cuisines in rows of four
num_columns = 4
for i in range(0, len(filtered_cuisines), num_columns):
    cols = st.columns(num_columns)
    for j, col in enumerate(cols):
        if i + j < len(filtered_cuisines):
            with col:
                display_cuisine(filtered_cuisines[i + j], f"button_{i+j}")
