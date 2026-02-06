import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# --- 1. 页面配置与防干扰补丁 ---
st.set_page_config(page_title="影视硬盘助手", page_icon="🎬", layout="centered")

# 核心：注入 JS 和 CSS 强制禁用浏览器自动翻译，防止 "removeChild" 报错
st.markdown(
    """
    <script>
        document.documentElement.setAttribute('class', 'notranslate');
        document.documentElement.setAttribute('translate', 'no');
    </script>
    <style>
        .notranslate { translate: no !important; }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🎬 硬盘影片信息识别工具")
st.markdown("上传一张剧照，AI 将为你精准匹配影片信息。")

# --- 2. API 配置 (安全模式) ---
with st.sidebar:
    st.header("⚙️ 设置")
    # 优先从 Streamlit Secrets 读取，如果没有则显示输入框
    if 'GEMINI_API_KEY' in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
        st.success("✅ 已从 Secrets 自动加载 API Key")
    else:
        api_key = st.text_input("请输入 Gemini API Key", type="password", help="在此输入你的 Google AI Studio 密钥")
    
    if api_key:
        genai.configure(api_key=api_key)
    
    st.divider()
    st.info("提示：图片识别由 Gemini 1.5 Flash 提供支持。")

# --- 3. 核心功能逻辑 ---
uploaded_file = st.file_uploader("点击上传或拖拽剧照...", type=["jpg", "jpeg", "png", "webp"], key="uploader")

if uploaded_file:
    try:
        image = Image.open(uploaded_file)
        # 居中展示预览图
        st.image(image, caption='待识别图像', use_container_width=True)
        
        # 优化后的 Prompt
        prompt = """
        你是一个专业的影视库助手。请根据这张图片识别以下内容：
        1. **影片识别**：确认该剧照属于哪部电影或电视剧。
        2. **角色与演员**：列出图片中出现的关键角色名称及其对应的演员姓名（格式：角色名 - 演员名）。
        3. **核心剧情**：总结该影片的剧情大纲（300字以内）。
        
        请务必用中文回复，并使用清晰的 Markdown 标题。
        """

        if st.button("🚀 开始深度识别", type="primary", key="recognize_btn"):
            if not api_key:
                st.warning("⚠️ 请先配置 API Key！")
            else:
                with st.spinner('🎬 AI 正在穿梭影库...'):
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    # 调用模型生成内容
                    response = model.generate_content([prompt, image])
                    
                    st.success("识别完成！")
                    st.divider()
                    # 渲染识别结果
                    st.markdown(response.text)
                    
    except Exception as e:
        st.error(f"❌ 程序遇到一点小麻烦：{str(e)}")

# --- 4. 底部声明 ---
st.divider()
st.caption("注：本工具仅供学习和个人管理硬盘资源使用。")
