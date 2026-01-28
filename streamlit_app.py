import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# --- 1. 页面配置 ---
st.set_page_config(page_title="影视硬盘助手", page_icon="🎬")
st.title("🎬 硬盘影片信息快速识别工具")
st.markdown("上传一张剧照，我帮你找回硬盘里的记忆。")

# --- 2. 侧边栏配置 ---
with st.sidebar:
    st.header("设置")
    # 提醒：请在此处输入你在 Google AI Studio 获取的 API Key
    api_key = st.text_input("请输入 Gemini API Key", type="password")
    if api_key:
        genai.configure(api_key=api_key)
    st.info("提示：图片识别由 Gemini 1.5 Flash 提供支持。")

# --- 3. 核心功能 ---
uploaded_file = st.file_uploader("选择剧照 (JPG/PNG/WebP)...", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file is not None:
    try:
        # 打开并显示图片
        image = Image.open(uploaded_file)
        st.image(image, caption='待识别剧照', use_container_width=True)
        
        # 设定 AI 的角色和任务
        prompt = """
        你是一个专业的影视库助手。请根据这张图片识别以下内容：
        1. 识别影片内容：确认该剧照属于哪部电影或电视剧。
        2. 角色与演员：列出图片中出现的关键角色名称及其对应的演员姓名（格式：角色名 - 演员名）。
        3. 视频剧情简介：总结该影片的剧情大纲（300字以内）。
        
        请用中文回复，并保持格式清晰美观。
        """

        if st.button("🚀 开始识别"):
            if not api_key:
                st.warning("⚠️ 请先在左侧输入 API Key！")
            else:
                with st.spinner('正在分析图片内容...'):
                    # 运行 Gemini 1.5 Flash 模型
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content([prompt, image])
                    
                    st.success("✅ 识别完成！")
                    st.divider()
                    # 直接渲染 AI 返回的文本
                    st.markdown(response.text)
                    
    except Exception as e:
        st.error(f"❌ 运行出错：{str(e)}")

# --- 4. 底部提示 ---
st.divider()
st.caption("建议：使用包含主角面部的清晰剧照以获得最佳识别效果。")
