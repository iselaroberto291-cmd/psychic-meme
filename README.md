import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# --- 1. 配置界面 ---
st.set_page_config(page_title="影视硬盘助手", page_icon="🎬")
st.title("🎬 硬盘影片信息快速识别工具")
st.markdown("上传一张剧照，我帮你找回硬盘里的记忆。")

# --- 2. 配置 Gemini API ---
# 你可以直接在这里填入 Key，或者在侧边栏输入
with st.sidebar:
    api_key = st.text_input("请输入 Gemini API Key", type="password")
    if api_key:
        genai.configure(api_key=api_key)

# --- 3. 上传模块 ---
uploaded_file = st.file_uploader("选择剧照 (JPG/PNG/WebP)...", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='待识别剧照', use_container_width=True)
    
    # 构造 Prompt（提示词）
    prompt = """
    你是一个专业的影视库助手。请根据这张图片识别以下内容：
    1. 识别影片内容：确认该剧照属于哪部电影或电视剧。
    2. 角色与演员：列出图片中出现的关键角色名称及其对应的演员姓名（格式：角色名 - 演员名）。
    3. 视频剧情简介：总结该影片的剧情大纲（300字以内）。
    
    请用中文回复，并保持格式清晰。
    """

    if st.button("开始识别"):
        if not api_key:
            st.error("请先在左侧输入 API Key！")
        else:
            with st.spinner('正在检索影视库，请稍候...'):
                try:
                    # 使用最新的 Gemini 1.5 Flash 模型，识别速度最快且免费额度高
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content([prompt, image])
                    
                    st.success("识别完成！")
                    st.divider()
                    
                    # 显示结果
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"识别出错：{str(e)}")

# --- 4. 底部说明 ---
st.info("提示：图片越清晰、特征越明显（如主角脸部），识别准确度越高。")
