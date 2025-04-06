import os
import g4f
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message

# Configuration
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
MAX_HISTORY = 10  # Number of messages to keep in context

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Store conversation contexts
user_contexts = {}

def get_user_context(user_id: int) -> list:
    """Get or create user context"""
    if user_id not in user_contexts:
        user_contexts[user_id] = [
            {"role": "system", "content": "You are a helpful assistant"}
        ]
    return user_contexts[user_id]

def update_context(user_id: int, message: str, response: str):
    """Update user context with new messages"""
    context = get_user_context(user_id)
    
    # Add user message
    context.append({"role": "user", "content": message})
    
    # Add assistant response
    context.append({"role": "assistant", "content": response})
    
    # Keep only last MAX_HISTORY messages (plus system prompt)
    if len(context) > MAX_HISTORY * 2 + 1:
        user_contexts[user_id] = [context[0]] + context[-(MAX_HISTORY * 2):]

async def generate_gpt_response(context: list) -> str:
    """Generate response using g4f with error handling"""
    try:
        response = await g4f.ChatCompletion.create_async(
            model=g4f.models.gpt_4,
            messages=context,
            web_search = True
        )
        return response or "I didn't get a response. Please try again."
    except Exception as e:
        print(f"GPT Error: {e}")
        return "⚠️ Sorry, I'm having trouble responding right now."

@dp.message(Command("start", "help"))
async def handle_start(message: Message):
    """Welcome message with instructions"""
    text = "🤖 *GPT-4 Assistant*\n\n" + "Send me a message to start chatting!\n" + "Commands:\n" + "/clear - Reset conversation history\n" + "/help - Show this message" + "Web version - https://5557-20-61-127-58.ngrok-free.app/chat"
    
    await message.reply(text)

@dp.message(Command("clear"))
async def handle_clear(message: Message):
    """Clear conversation history"""
    user_id = message.from_user.id
    user_contexts.pop(user_id, None)
    await message.reply("🔄 Conversation history cleared!")

@dp.message(F.text)
async def handle_message(message: Message):
    """Handle all text messages"""
    user_id = message.from_user.id
    user_message = message.text
    
    # Get current context
    context = get_user_context(user_id)
    
    # Show typing indicator
    await bot.send_chat_action(message.chat.id, "typing")
    
    # Generate response
    gpt_response = await generate_gpt_response(context)
    
    # Update conversation history
    update_context(user_id, user_message, gpt_response)
    
    # Send response (split long messages)
    await message.reply(gpt_response)

if __name__ == "__main__":
    print("Bot is running...")
    dp.run_polling(bot)