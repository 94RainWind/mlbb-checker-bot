import telebot
import requests

# ⚠️ ဒီနေရာမှာ မိမိရဲ့ Telegram Bot Token ကို ထည့်ပါ
BOT_TOKEN = '8847386138:AAFAIbtJIFtAvrocKPi7vRDqIWDBti0RX2o'
bot = telebot.TeleBot(BOT_TOKEN)

# ℹ️ MLBB Region/Account စစ်ပေးမယ့် API URL (ဥပမာပုံစံ)
# သားကြီး သုံးမယ့် API Provider ရဲ့ URL နဲ့ Parameter အတိုင်း ပြန်ပြင်ပေးရပါမယ်။
API_URL = "https://api.example.com/mlbb/checker" 

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "👋 မင်္ဂလာပါ သားကြီး! MLBB Region Checker Bot မှ ကြိုဆိုပါတယ်။\n\n"
        "🔍 Region စစ်ချင်ရင် အောက်ပါ Format အတိုင်း ရိုက်ပို့ပေးပါ -\n"
        "`/check UserID ZoneID`\n\n"
        "💡 ဥပမာ - `/check 12345678 1234`"
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(commands=['check'])
def check_region(message):
    # User ပို့လိုက်တဲ့ message ကို ခွဲထုတ်ခြင်း
    input_text = message.text.split()
    
    # Format မှန်/မမှန် စစ်ဆေးခြင်း
    if len(input_text) < 3:
        bot.reply_to(message, "❌ Format မမှန်ဘူးသားကြီး။ `/check UserID ZoneID` ပုံစံအတိုင်း ပြန်ရိုက်ပေးပါ။")
        return
    
    user_id = input_text[1]
    zone_id = input_text[2]
    
    # ခဏစောင့်ပါ message ပြပေးခြင်း
    status_msg = bot.reply_to(message, "⏳ ခဏစောင့်ဗျာ... Data ရှာဖွေနေပါတယ်...")

    try:
        # API သို့ Request ပို့ခြင်း (သားကြီးဝယ်ထားတဲ့ API ရဲ့ header/params အပေါ်မူတည်ပြီး ပြင်ရမယ်)
        payload = {
            'id': user_id,
            'zone': zone_id
        }
        # ဥပမာ API request ပုံစံ
        response = requests.get(API_URL, params=payload, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # API ကနေ ပြန်လာတဲ့ JSON data ပေါ်မူတည်ပြီး ဆွဲထုတ်တာ ပြင်ပေးပါ
            # အောက်ပါအတိုင်း ပြန်လာတယ်လို့ ဥပမာထားထားပါတယ်
            if data.get('status') == 'success' or data.get('error') is None:
                username = data.get('username', 'N/A')
                region = data.get('region', 'Unknown')
                country = data.get('country', 'Unknown')
                
                result_text = (
                    "🎮 *MLBB Account Details*\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    f"👤 *Name:* {username}\n"
                    f"🆔 *ID:* {user_id} ({zone_id})\n"
                    f"🌍 *Region:* {region}\n"
                    f"🇲🇲 *Country:* {country}\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    "✅ စစ်ဆေးမှု အောင်မြင်ပါသည်။"
                )
                bot.edit_message_text(result_text, chat_id=message.chat.id, message_id=status_msg.message_id, parse_mode='Markdown')
            else:
                bot.edit_message_text("❌ Account ရှာမတွေ့ပါဘူး။ ID နဲ့ Zone ပြန်စစ်ပေးပါ။", chat_id=message.chat.id, message_id=status_msg.message_id)
        else:
            bot.edit_message_text("📶 Server API မှာ ပြဿနာတက်နေလို့ ခဏနေမှ ပြန်ကြိုးစားကြည့်ပါသတ်ကြီး။", chat_id=message.chat.id, message_id=status_msg.message_id)

    except requests.exceptions.Timeout:
        bot.edit_message_text("⏳ Connection timed out! API က အကြောင်းမပြန်တော့လို့ပါ။", chat_id=message.chat.id, message_id=status_msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"⚠️ Error တစ်ခုတက်သွားတယ် သားကြီး: {str(e)}", chat_id=message.chat.id, message_id=status_msg.message_id)

# Bot ကို တစ်သက်လုံး Run ထားစေမယ့် code
print("🤖 Bot က အလုပ်လုပ်နေပြီ သားကြီး...")
bot.infinity_polling()
