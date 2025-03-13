import streamlit as st
from chains import generate_blog, generate_title, generate_blog_tags, generate_blog_outline, suggest_blog_topics
from utils import clean_text
from datetime import datetime
import speech_recognition as sr
from streamlit_webrtc import webrtc_streamer
import av

# Main Streamlit App
def create_streamlit_app(llm):
    st.set_page_config(page_title="AI Blog Creator", page_icon="📝", layout="wide")
    css = """
    <style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Arial', sans-serif;
    }
    html {
        scroll-behavior: smooth;
    }

    body {
        background-color: #ffffff;
        color: #444;
        line-height: 1.6;
        overflow-x: hidden;
    }

    a {
        text-decoration: none;
        color: #444;
    }

    
    h1, h2, h3, h4 {
        color: #ff4c4c;
        margin-bottom: 20px;
    }

    h1 {
        font-size: 2.8em;
        font-weight: bold;
        text-align: center;
        letter-spacing: 1px;
    }

    h2, h3, h4 {
        border-bottom: 2px solid #ff4c4c;
        padding-bottom: 10px;
    }

    .stButton button {
        color: red;
        font-size: 1.2em;
        border: none;
        border-radius: 10px;
        padding: 12px 24px;
        cursor: pointer;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease, color 0.3s ease;
    }

    .stButton button:hover {
        background: #d43c3c;
        transform: translateY(-3px);
        color:white;

    }

    .stSelectbox, .stTextInput, .stSlider, .stTextArea, .stRadio {
        background-color: 000000;
        border: 1px solid #ccc;
        border-radius: 8px;
        padding: 12px;
        color: #444;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
        transition: background-color 0.3s ease;
    }

    .stSelectbox:focus, .stTextInput:focus, .stTextArea:focus {
        background-color: #e0e0e0;
        outline: none;
    }

    .stTextArea {
        background-color: #0000;
        border-radius: 8px;
        padding: 12px;
        color: #444;
        width: 100%;
        margin-bottom: 20px;
        border: none;
    }

    .share-button {
        background-color: #ff4c4c;
        color: white;
        padding: 10px 24px;
        border-radius: 5px;
        text-align: center;
        display: inline-block;
        font-size: 16px;
        margin: 10px;
        text-decoration: none;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease, background-color 0.3s ease;
    }

    .share-button:hover {
        background-color: #d43c3c;
        transform: translateY(-3px);
    }

    .button-container {
        text-align: center;
        margin-top: 20px;
        color: white;
    }

    .stTextArea:focus {
        background-color: #d0d0d0;
        outline: none;
    }

    .stDownloadButton button {
        background: #ff4c4c;
        color: white;
        padding: 12px 24px;
        border-radius: 8px;
        border: none;
        cursor: pointer;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
        transition: transform 0.3s ease;
    }

    .stDownloadButton button:hover {
        background: #d43c3c;
        transform: translateY(-3px);
    }

    footer {
        text-align: center;
        padding: 20px;
        background-color: #f0f0f0;
        color: #444;
        font-size: 1em;
        margin-top: 40px;
        border-top: 2px solid #ff4c4c;
    }

    footer p {
        margin: 0;
    }

    .blog-content {
        font-size: 1.2em;
        line-height: 1.8em;
        color: #f0f0f0;  
        text-align: justify;
        margin: 20px 0;  
        padding: 20px;  
        background-color: #1e1e1e;
        border-left: 4px solid #007bff;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.5);
        border-radius: 8px;  
    }

    .blog-content h1, 
    .blog-content h2, 
    .blog-content h3 {
        color: #fd6c6c; 
        margin-top: 15px;
    }

    .blog-content p {
        margin-bottom: 15px;
    }

    .blog-content a {
        color: #ff4c4c;  
        text-decoration: none;
    }

    .blog-content a:hover {
        text-decoration: underline;
    }

    .blog-tags {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin-top: 20px;
    }

    .tag {
        background-color: #ff4c4c;
        color: white;
        padding: 8px 12px;
        border-radius: 20px;
        font-size: 0.9em;
        cursor: default;
    }
    
    .tag:hover {
        background-color: #d43c3c;
        cursor: pointer;
    }

    .section-title {
        font-size: 1.8em;
        color: #fd6c6c;
        text-align: center;
        margin-bottom: 30px;
    }

    .divider {
        height: 1px;
        background-color: ##fd6c6c;
        margin: 40px 0;
        border: none;
    }

    
    </style>
    """
    
    st.markdown(css, unsafe_allow_html=True)

    st.title("📝 AI Blog Creator")
    st.markdown("""
    Effortlessly generate engaging blog content with AI. Choose a topic, style, and tone to create personalized blog posts within minutes!
    """, unsafe_allow_html=True)

    def get_voice_input():
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("Listening... Please ask your question.")
            audio = recognizer.listen(source)
            try:
                user_input = recognizer.recognize_google(audio)
                st.success(f"You said: {user_input}")
                return user_input
            except sr.UnknownValueError:
                st.error("Sorry, I could not understand the audio.")
            except sr.RequestError:
                st.error("Could not request results from the speech recognition service.")
        return None

    input_type = st.selectbox('Select Input Type', ['Enter Topic', 'Suggest Topics', 'Use Voice Command'])
    
    if input_type == 'Enter Topic':
        blog_topic = st.text_input("Enter the Blog Topic:")
    elif input_type == 'Suggest Topics':
        suggested_topics = suggest_blog_topics(llm)
        blog_topic = st.selectbox("Choose a Blog Topic", suggested_topics)
    else:
        if st.button("Ask with Voice"):
            user_input = get_voice_input()
            if user_input:
                st.session_state.voice_input = user_input

        else:
            st.write("Press the button to speak into the microphone to provide a topic.")

        if 'voice_input' in st.session_state:
            blog_topic = st.session_state['voice_input']
            st.write(f"**Recognized Topic**: {blog_topic}")
        else:
            st.write("No topic recognized yet.")
    
    col1, col2, col3 = st.columns(3)

    with col1:
        word_limit = st.slider("Word Limit", min_value=100, max_value=1000, step=50, value=200)
    with col2:
        blog_style = st.selectbox('Writing Style', ['Researchers', 'Data Scientist', 'Common People', 'Lifestyle Blogger', 'Tech Blogger'])
    with col3:
        tone = st.selectbox('Tone', ['Formal', 'Conversational', 'Humorous', 'Professional'])

    if st.button("Generate Blog Title"):
        blog_title = generate_title(llm, blog_topic)
        st.write(f"**Generated Title**: {blog_title}")
    
    generate_type = st.radio("Generate Full Blog or Outline", ['Blog', 'Outline'])

    if generate_type == 'Blog':
        generate_button = st.button("Generate Blog")
    else:
        generate_button = st.button("Generate Outline")

    if generate_button:
        if generate_type == 'Blog':
            blog_content = generate_blog(llm, blog_topic, word_limit, blog_style, tone)
            cleaned_blog_content = clean_text(blog_content)
        
            st.markdown(f"<div class='blog-content'>{blog_content}</div>", unsafe_allow_html=True)


            if 'previous_blogs' not in st.session_state:
                st.session_state['previous_blogs'] = []
            st.session_state['previous_blogs'].append(blog_content)

            tags = generate_blog_tags(llm, blog_content)
            st.write("**SEO Tags**: ", ", ".join(tags))
            
            now = datetime.now()
            file_name = f"{blog_topic.replace(' ', '_')}_{now.strftime('%Y%m%d_%H%M%S')}.txt"
            st.download_button(f"Download Blog as {file_name}", blog_content, file_name=file_name)

        elif generate_type == 'Outline':
            outline_content = generate_blog_outline(llm, blog_topic)
            st.write(outline_content)
            

    st.markdown("---")
    st.subheader("Previous Blogs")
    
    if 'previous_blogs' in st.session_state and st.session_state['previous_blogs']:
        for idx, blog in enumerate(st.session_state['previous_blogs']):
            with st.expander(f"Blog {idx + 1}"):
                
                st.markdown(f"<div class='blog-content'>{blog}</div>", unsafe_allow_html=True)
    else:
        st.write("No blogs generated yet.")

    st.markdown("---")
    st.subheader("Give Us Your Feedback")
    feedback = st.text_area("Share your feedback or suggestions:")

    if st.button("Submit Feedback"):
        if feedback:
            st.success("Thank you for your feedback!")
        else:
            st.warning("Please enter your feedback before submitting.")
    logout_url = 'http://127.0.0.1:5000/logout'  
    st.markdown(f"""
    <a href="{logout_url}" target="_self">
        <button style="
            color: red; 
            border: none; 
            padding: 10px 20px;  
            font-size: 16px; 
            cursor: pointer;
            border-radius: 5px;">
            Logout
        </button>
    </a>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("Tips for Writing Great Blogs:")
    st.markdown("""
    - Use clear, concise language.
    - Tailor your tone to your target audience.
    - Keep paragraphs short and to the point.
    - Make sure your content provides value and engages the reader.
    """)

    st.markdown("---")
    st.markdown("Made with ❤️ by Team A")

    st.markdown("---")
    st.subheader("Share Your Blog")
    share_url = f"https://www.example.com/blog"
    
    st.markdown(f"""
    <div class="button-container">
        <a href="https://twitter.com/share?url={share_url}" target="_blank" class="share-button">
            Share on Twitter
        </a>
        <a href="https://www.facebook.com/sharer/sharer.php?u={share_url}" target="_blank" class="share-button">
            Share on Facebook
        </a>
        <a href="https://www.linkedin.com/sharing/share-offsite/?url={share_url}" target="_blank" class="share-button">
            Share on LinkedIn
        </a>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    from langchain_groq import ChatGroq
    llm = ChatGroq(groq_api_key='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',temperature=0.7)
    create_streamlit_app(llm)