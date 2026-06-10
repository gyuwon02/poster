import os
import base64
from openai import OpenAI
import streamlit as st

os.environ["OPENAI_API_KEY"] = st.secrets['OPENAI_API_KEY']

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

st.title('🎁 제품 홍보 포스터 생성기')
keyword = st.text_input("키워드를 입력하세요.")

if st.button('생성하기🔥'):
    if keyword:
        # 1. 텍스트 생성
        with st.spinner('홍보 문구 생성중🔥'):
            text_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "입력 받은 키워드에 대한 150자 이내의 솔깃한 제품 홍보 문구를 작성해줘."},
                    {"role": "user", "content": keyword}
                ],
                temperature=0.9,
            )
            result_text = text_response.choices[0].message.content
            st.write(result_text)

        # 2. 이미지 생성
        with st.spinner("포스터 이미지를 생성 중입니다... 🎨"):
            try:
                image_prompt = f"A high-quality, professional promotional poster for: {keyword}"
                
                result = client.images.generate(
                    model="gpt-image-2",
                    prompt=image_prompt
                )

                image_base64 = result.data[0].b64_json
                image_bytes = base64.b64decode(image_base64)
                    
                st.image(image_bytes, caption=f"홍보 키워드: '{keyword}'", use_container_width=True)
                
            except Exception as e:
                st.error(f"이미지 생성 중 오류가 발생했습니다: {e}")
    else:
        st.warning("먼저 키워드를 입력해 주세요!")