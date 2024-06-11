import asyncio
import os
import openai
from PyPDF2 import PdfReader
from telegram import Update, Bot
from telegram.ext import Application, MessageHandler, filters, CallbackContext

# Configuration

CHATGPT_MODEL = 'gpt-3.5-turbo-0125'
DOWNLOAD_DIR = '/Users/diassadykov/Desktop'  # Directory to save PDFs temporarily
SYSTEM_PROMPT = """
Ты карьерный консультант, который помогает людям улучшить свои резюме. 
Тебе прислали резюме в формате PDF и попросили дать обратную связь. 
Пожалуйста, напиши обратную связь на резюме на русском языке.
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
    print("Getting feedback from ChatGPT...")
    print(text)
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
            await update.message.reply_text(f"Feedback from ChatGPT:\n\n{feedback}")
        except Exception as e:
            await update.message.reply_text(f"Failed to get feedback: {str(e)}")
        finally:
            os.remove(file_path)

# Main function to set up the bot
def main():
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Listen to all messages in the group chat
    application.add_handler(MessageHandler(filters.Document.MimeType('application/pdf'), handle_message))

    # Start polling for updates from the group chat
    application.run_polling()

if __name__ == '__main__':
    main()