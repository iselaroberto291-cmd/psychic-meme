import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# --- 1. 页面基本配置 ---
st.set_page_config(page_title="影视硬盘助手", page_icon="🎬")
st.title("🎬 硬盘影片信息快速识别工具")
st.markdown("上传一张剧照，我帮你找回硬盘里的记忆。")

# --- 2. 侧边栏 API 配置 ---
with st.sidebar:
    st.header("设置")
    api_key = st.text_input("请输入 Gemini API Key", type="password", help="从 Google AI Studio 获取")
    if api_key:
        genai.configure(api_key=api_key)
    st.info("提示：此工具使用 Gemini 1.5 Flash 模型进行识别。")

# --- 3. 核心功能区 ---
uploaded_file = st.file_uploader("选择剧照 (JPG/PNG/WebP)...", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file is not None:
    try:
        image = Image.open(uploaded_file)
        st.image(image, caption='已上传剧照', use_container_width=True)
        
        # 定义发给 AI 的指令
        prompt = """
        你是一个专业的影视库助手。请根据这张图片识别以下内容：
        1. 识别影片内容：确认该剧照属于哪部电影或电视剧。
        2. 角色与演员：列出图片中出现的关键角色名称及其对应的演员姓名（格式：角色名 - 演员名）。
        3. 视频剧情简介：总结该影片的剧情大纲（300字以内）。
        
        请用中文回复，并保持格式清晰美观。
        """

        if st.button("🚀 开始识别内容"):
            if not api_key:
                st.warning("⚠️ 请先在侧边栏输入您的 API Key。")
            else:
                with st.spinner('正在分析图片并检索数据库...'):
                    # 调用多模态模型
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content([prompt, image])
                    
                    st.success("✅ 识别成功！")
                    st.divider()
                    
                    # 输出 AI 生成的内容
                    st.markdown(response.text)
                    
    except Exception as e:
        st.error(f"❌ 程序发生错误：{str(e)}")

# --- 4. 底部说明 ---
st.divider()
st.caption("提示：图片越清晰、人物面部特征越明显，识别的准确度越高。")
