import streamlit as st

st.set_page_config(page_title="My First Streamlit App",page_icon="🤖")

st.title("🤖 My First Streamlit App")
st.write("This is a simple app to learn Streamlit basics.")

st.divider()

name=st.text_input("What is your name?")

if name:
    st.success(f"Hello,{name}! Welcom to streamlit.")
    
number=st.slider("Pick a number",min_value=1,max_value=100,value=50)
st.write(f"You picked:{number}")

if st.button("Click Me"):
    st.balloons()
    st.write("You clicked the button!")
    
st.divider()

st.sidebar.title("Settings")
theme=st.sidebar.selectbox("Choose a theme",["light","Dark",'Auto'])
st.sidebar.write(f"Selected theme:{theme}")

st.subheader("Two Column Layout")
col1,col2=st.columns(2)

with col1:
    st.write("**Left Column**")
    st.info("This is the left side")
    
with col2:
    st.write("**Right Column**")
    st.warning("This is the right side")
    
st.divider()
st.subheader("File Uploader")
uploaded_file=st.file_uploader('Upload a text file',type=['txt'])

if uploaded_file:
    content=uploaded_file.read().decode("utf-8")
    st.write(f"File name:{uploaded_file.name}")
    st.write(f"File size:{len(content)} characters")
    st.text_area("File contents:",content,height=200)