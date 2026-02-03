
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from src.config import LLM_MODEL_NAME, BASE_URL, LLM_TEMP

def get_llm():
    return ChatOllama(
        model=LLM_MODEL_NAME,
        base_url=BASE_URL,
        temperature=LLM_TEMP
    )

def generate_response(context, memory_context, question):
    llm = get_llm()
    
    # Updated System Prompt "AntiGravity Specialist"
    system_template = """Bạn là chuyên gia AntiGravity. Dưới đây là các mảnh thông tin đã được trích xuất (mỗi mảnh có Context đi kèm để bạn biết nó nằm ở mục nào trong tài liệu gốc). 
Hãy ưu tiên sự thật trong Context, kết hợp với sở thích người dùng từ Memory để đưa ra câu trả lời Markdown chuẩn xác nhất.

USER MEMORY (Sở thích/Lịch sử):
{memory_context}

CONTEXT (Thông tin tra cứu):
{context}
"""

    prompt = ChatPromptTemplate.from_messages([
        ("system", system_template),
        ("human", "{question}")
    ])
    
    chain = prompt | llm | StrOutputParser()
    
    return chain.stream({"context": context, "memory_context": memory_context, "question": question})
