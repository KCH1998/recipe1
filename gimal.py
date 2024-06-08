import streamlit as st
import fitz  
import openai


openai.api_key = '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'

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text


def extract_dishes_from_text(text):
    lines = text.split('\n')
    dishes = [line.strip() for line in lines if line.strip()]
    return dishes


def get_recipe_from_openai(dish_name):
    prompt = f"{dish_name}의 레시피를 알려주세요."
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message['content'].strip()
    except Exception as e:
        return str(e)


def main():
    st.title("🍽️요리 레시피 검색기🍽️")
    file_path = "cook1.pdf"
    text = extract_text_from_pdf(file_path)
    
    dishes = extract_dishes_from_text(text)
    
    st.header("요리를 선택하세요:")
    dish_name = st.selectbox("요리", dishes)
    
    if st.button("레시피 보기"):
        recipe = get_recipe_from_openai(dish_name)
        st.write(f"**{dish_name}의 레시피**")
        st.write(recipe)

if __name__ == "__main__":
    main()
