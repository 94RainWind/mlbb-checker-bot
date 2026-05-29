import telebot
import requests

# ⚠️ မိမိရဲ့ Telegram Bot Token ကို ဒီမှာ အစားထိုးပါ
BOT_TOKEN = '8847386138:AAGsmgyLgkhoJxuUaB1LYQaX4wvKG99Z5-A'
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    welcome_text = (
        "👋 မင်္ဂလာပါ သားကြီး! MLBB Region Checker Bot မှ ကြိုဆိုပါတယ်။\n\n"
        "🔍 Account အချက်အလက် စစ်ချင်ရင် အောက်ပါ Format အတိုင်း ရိုက်ပို့ပေးပါ -\n"
        "`/check UserID ZoneID`\n\n"
        "💡 ဥပမာ - `/check 32133332 2045`"
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(commands=['check'])
def check_region(message):
    input_text = message.text.split()
    
    if len(input_text) < 3:
        bot.reply_to(message, "❌ Format မမှန်ဘူးသားကြီး။ `/check UserID ZoneID` ပုံစံအတိုင်း ပြန်ရိုက်ပေးပါ။")
        return
    
    user_id = input_text[1]
    zone_id = input_text[2]
    
    status_msg = bot.reply_to(message, "⏳ ခဏစောင့်ဗျာ... Data ရှာဖွေနေပါတယ်...")

    # Sacoli API URL
    API_URL = f"https://sacoliofficial.com/api/name-check/mlbb?user_id={user_id}&server_id={zone_id}"

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        response = requests.get(API_URL, headers=headers, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            
            # API က success: true ပြန်လာမှ Data ဆွဲထုတ်မယ်
            if data.get('success') == True:
                # သားကြီးပြပေးတဲ့ JSON Response Key နာမည်များအတိုင်း ဆွဲထုတ်ခြင်း
                username = data.get('username', 'N/A')
                country_code = data.get('country', 'Unknown')
                
                # Country Code ကို စာသားအလှပြောင်းခြင်း (ဥပမာ- MM ဆိုရင် Myanmar)
                country_name = "Myanmar 🇲🇲" if country_code == "MM" else country_code
                
                result_text = (
                    "🎮 *MLBB Account Details*\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    f"👤 *Name:* {username}\n"
                    f"🆔 *ID:* {user_id} ({zone_id})\n"
                    f"🌍 *Country:* {country_name}\n"
                    "━━━━━━━━━━━━━━━━━━━━\n"
                    "✅ စစ်ဆေးမှု အောင်မြင်ပါသည်။"
                )
                bot.edit_message_text(result_text, chat_id=message.chat.id, message_id=status_msg.message_id, parse_mode='Markdown')
            else:
                bot.edit_message_text("❌ Account ရှာမတွေ့ပါဘူး သားကြီး။ ID နဲ့ Zone ပြန်စစ်ပေးပါ။", chat_id=message.chat.id, message_id=status_msg.message_id)
        else:
            bot.edit_message_text(f"📶 Server က အကြောင်းမပြန်ပါဘူး။ (Status Code: {response.status_code})", chat_id=message.chat.id, message_id=status_msg.message_id)

    except requests.exceptions.Timeout:
        bot.edit_message_text("⏳ Connection timed out! Server ဘက်က ကြာနေလို့ပါ။", chat_id=message.chat.id, message_id=status_msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"⚠️ Error တစ်ခုခု တက်သွားတယ် သားကြီး: {str(e)}", chat_id=message.chat.id, message_id=status_msg.message_id)

print("🤖 Bot က Run နေပါပြီ သားကြီး...")
bot.infinity_polling()
