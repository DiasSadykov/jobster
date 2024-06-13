import os
import openai
from PyPDF2 import PdfReader
from telegram import Update, Bot
from telegram.ext import Application, MessageHandler, filters, CallbackContext

ENV = os.environ.get("ENV") or "DEV"

# Configuration
TELEGRAM_TOKEN = os.environ.get("BOT_TOKEN")
CHATGPT_API_KEY = os.environ.get("CHATGPT_API_KEY")
CHATGPT_MODEL = 'gpt-4-turbo'
DOWNLOAD_DIR = '/Users/diassadykov/Desktop' if ENV == "DEV" else "/resumes"  # Directory to save PDFs temporarily
SYSTEM_PROMPT = """
Ты карьерный консультант, который помогает людям улучшить свои резюме. 
Тебе прислали резюме и попросили дать обратную связь. 
Пожалуйста, напиши обратную связь на резюме на русском языке.
В хорошем резюме должны быть следующие разделы:
1. Контактная информация
2. Опыт работы
    1. Название компании
    2. Должность
    3. Даты работы
    4. Достижения в формате XYZ (сделал X, используя Y, что привело к Z), помоги кандидату продемонстрировать свои навыки и достижения в этом формате на примере.
3. Образование
4. Личные проекты (если есть)
    1. Описание проекта
    2. Технологии, которые использовались
    3. Результаты (если есть)
    4. Ссылка на проект
5. Достижения на олимпиадах или конкурсах (если есть)
Используй этот формат для обратной связи:
Привет [Имя], спасибо! Вот мои комментарии по твоему резюме:
[Положительные аспекты в 1-2 предложениях]
[Для каждого описания достижеий в опыте работы напиши, как можно улучшить формулировку, чтобы она соответствовала формату XYZ, обязательно упомянай формат XYZ]
[Исправь раздел с личными проектами, если они не соответствуют формату]
[Исправь порядок разделов, если это необходимо]
Пиши что нужно улучшить только в случае если есть что улучшить, иначе пропускай этот пункт.
Если исправляешь что-то то исправляй на языке оригинала, для этого используй комментарии в формате [Исправлено: Исправленный текст] Если текст на английском то и исправление должно быть на английском.
Обязательно упомянай формат XYZ в комментариях к достижениям в опыте работы.
Постарайся уложиться в 1500 символов или меньше.
"""

# Initialize ChatGPT API
client = openai.OpenAI(api_key=CHATGPT_API_KEY)

# Function to extract text from PDF using PyPDF2
def extract_text_from_pdf(pdf_path):
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

# Function to get feedback from ChatGPT
async def get_feedback_from_chatgpt(text):
    response = client.chat.completions.create(
        model=CHATGPT_MODEL,
        messages=[
            {"role": "system", "content": f"{SYSTEM_PROMPT}"},
            {"role": "user", "content": f"{text}"}
        ]
)
    return response.choices[0].message.to_dict().get('content')

# Function to handle incoming messages in the group chat
async def handle_message(update: Update, context: CallbackContext):
    if update.message and update.message.document and update.message.document.mime_type == 'application/pdf':
        file_id = update.message.document.file_id
        file = await context.bot.get_file(file_id)
        file_path = os.path.join(DOWNLOAD_DIR, update.message.document.file_name)
        await file.download_to_drive(custom_path=file_path) 
        
        try:
            text = extract_text_from_pdf(file_path)
            if not text.strip():
                await update.message.reply_text("Could not extract text from the PDF.")
                return
            feedback = await get_feedback_from_chatgpt(text)
            await update.message.reply_text(f"{feedback}")
        except Exception as e:
            await update.message.reply_text(f"Что-то пошло не так: {str(e)}")

# Main function to set up the bot
def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Listen to all messages in the group chat
    application.add_handler(MessageHandler(filters.Document.MimeType('application/pdf'), handle_message))

    # Start polling for updates from the group chat
    application.run_polling()

if __name__ == '__main__':
    main()