import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. 页面配置与防翻译补丁 ---
st.set_page_config(page_title="影视硬盘助手", page_icon="🎬")

# 注入 JS 强制禁用浏览器自动翻译，彻底解决 "removeChild" 报错
st.markdown(
    """
    <script>
        document.documentElement.setAttribute('class', 'notranslate');
        document.documentElement.setAttribute('translate', 'no');
    </script>
    """,
    unsafe_allow_html=True
)

st.title("🎬 影视信息快速识别工具")

# --- 2. 安全读取 API Key ---
# 优先从 Streamlit 控制台的 Secrets 读取
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.warning("⚠️ 请在 Streamlit Cloud 的 Secrets 中配置 GEMINI_API_KEY")
    st.stop()

# --- 3. 核心功能 ---
uploaded_file = st.file_uploader("上传剧照...", type=["jpg", "png", "webp"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption='待识别剧照', use_container_width=True)
    
    if st.button("🚀 开始识别"):
        with st.spinner('正在分析中...'):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                prompt = "请识别这张剧照的电影名称、角色演员表以及300字剧情简介，用中文回答。"
                response = model.generate_content([prompt, image])
                st.markdown(response.text)
            except Exception as e:
                st.error(f"识别失败: {str(e)}")
