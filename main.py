import requests
import json
import time
import os
import random
import base64
import re
import datetime
from urllib.parse import urlparse

# --- START OF FILE بوت رشق واسط الخارق والمهيكل - الإصدار الماسي النهائي الشامل أزرار الرجوع ---

Token = "8606949338:AAGQRzqeIQteaD4yACpsk2X7mipdD_By3uc"  # ضع توكن بوتك هنا
admin = 7475612907 # ضع ايدي الادمن الخاص بك هنا
API_KEY = Token

def bot(method, datas={}):
    Saied_Botate = f"https://api.telegram.org/bot{API_KEY}/{method}"
    saied_botate = None
    if datas:
        boundary = '----WebKitFormBoundary' + ''.join(random.sample('0123456789abcdef', 16))
        saied_botate = buildMultipartData(datas, boundary)
        headers = {'Content-Type': f'multipart/form-data; boundary={boundary}'}
        try:
            response = requests.post(Saied_Botate, data=saied_botate, headers=headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
    else:
        try:
            response = requests.get(Saied_Botate)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}

def buildMultipartData(data, boundary):
    SaiedData = []
    for key, value in data.items():
        if isinstance(value, tuple) and len(value) == 3:
            SaiedData.append(f"--{boundary}")
            SaiedData.append(f'Content-Disposition: form-data; name="{key}"; filename="{value[0]}"')
            SaiedData.append(f'Content-Type: {value[2]}')
            SaiedData.append('')
            SaiedData.append(value[1])
        else:
            SaiedData.append(f"--{boundary}")
            SaiedData.append(f'Content-Disposition: form-data; name="{key}"')
            SaiedData.append('')
            SaiedData.append(str(value))
    SaiedData.append(f"--{boundary}--")
    return "\r\n".join(SaiedData).encode('utf-8')

def get_update(offset=None):
    try:
        params = {'timeout': 100, 'offset': offset}
        response = requests.get(f"https://api.telegram.org/bot{API_KEY}/getUpdates", params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching updates: {e}")
        return None

def process_update(update):
    global Token, admin, API_KEY

    message = update.get('message')
    callback_query = update.get('callback_query')

    chat_id = None
    from_id = None
    name = None
    user = None
    message_id = None
    text = None
    data = None

    if message:
        chat_id = message['chat']['id']
        from_id = message['from']['id']
        name = message['from'].get('first_name')
        user = message['from'].get('username')
        message_id = message['message_id']
        text = message.get('text')
    elif callback_query:
        chat_id = callback_query['message']['chat']['id']
        from_id = callback_query['from']['id']
        name = callback_query['from']['first_name']
        message_id = callback_query['message']['message_id']
        data = callback_query['data']
    else:
        return

    os.makedirs("data", exist_ok=True)
    os.makedirs("sudo", exist_ok=True)
    os.makedirs("RSHQ", exist_ok=True)

    def read_file(filename, default=""):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return default

    def write_file(filename, content):
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)

    rshq = {}
    try:
        with open("RSHQ/rshq.json", 'r', encoding='utf-8') as f:
            rshq = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        rshq = {
            "categories": {}, # {cat_id: {"name": "...", "services": {srv_id: {...}}}}
            "coin": {}, "mshark": {}, 
            "keys": {}, "tlby": {}, "cointlb": {}, "rshqG": "on", 
            "channels": [], "free_gift_val": 50, "ref_reward": 10,
            "apple_status": "on", "gift_status": "on", "apple_timers": {}
        }

    if "categories" not in rshq:
        rshq["categories"] = {}

    def SETJSON(INPUT):
        if INPUT:
            write_file("RSHQ/rshq.json", json.dumps(INPUT, indent=4, ensure_ascii=False))

    channels = rshq.get("channels", [])
    if message and channels and from_id != admin:
        for ch in channels:
            join_status = bot('getChatMember', {'chat_id': ch, 'user_id': from_id})
            if join_status and join_status.get('result', {}).get('status') in ['left', 'kicked'] or join_status and join_status.get('error_code') == 400:
                bot('sendMessage', {
                    'chat_id': chat_id,
                    'text': f"🤍| عذرا عزيزي\n🕊| عليك الاشتراك بقناة البوت لتتمكن من استخدامه\n\n- ({ch})\n\n🌼| اشترك ثم ارسل /start",
                    'parse_mode': "Markdown",
                    'disable_web_page_preview': True,
                })
                return

    users = []
    try:
        with open("arslan.json", 'r', encoding='utf-8') as f:
            users = f.read().splitlines()
    except FileNotFoundError:
        pass

    if message:
        if str(from_id) not in users:
            with open("arslan.json", 'a', encoding='utf-8') as f:
                f.write(str(from_id) + "\n")
            users.append(str(from_id))

    adminss = []
    try:
        with open("ad.json", 'r', encoding='utf-8') as f:
            adminss = f.read().splitlines()
    except FileNotFoundError:
        pass

    if message:
        if str(admin) not in adminss:
            with open("ad.json", 'a', encoding='utf-8') as f:
                f.write(str(admin) + "\n")
            adminss.append(str(admin))

    all_users_count = len(users)
    disp_user = f"@{user}" if user else "@FY6FT"

    if message and text and text.startswith("/start "):
        ref_id = text.split(" ")[1]
        if ref_id.isnumeric() and ref_id != str(from_id):
            ref_list_file = f"data/refs_{from_id}.txt"
            if not os.path.exists(ref_list_file):
                write_file(ref_list_file, "done")
                ref_reward = rshq.get("ref_reward", 10)
                rshq.setdefault("coin", {})[ref_id] = rshq["coin"].get(ref_id, 0) + ref_reward
                rshq.setdefault("mshark", {})[ref_id] = rshq["mshark"].get(ref_id, 0) + 1
                SETJSON(rshq)
                bot('sendMessage', {'chat_id': int(ref_id), 'text': f"🎁 ¦ انضم شخص جديد عبر رابط دعوتك وحصلت على *{ref_reward}* نقطة!", 'parse_mode': "markdown"})

    if message and text == "/start" and str(from_id) not in users:
        bot('sendmessage', {
            'chat_id': admin,
            'text': f"٭ تم دخول شخص جديد الى البوت الخاص بك 🤍\n\n• معلومات العضو الجديد .\n                 •--•\n• الاسم : {name}\n• المعرف : {disp_user}\n• الايدي : {from_id}\n                  •--•\n• عدد الاعضاء الكلي : {all_users_count}",
        })

    usrbot_info = bot("getme")
    usrbot = usrbot_info['result']['username'] if usrbot_info and usrbot_info.get('ok') else "UNKNOWN_BOT"

    e = data.split("|") if callback_query else []
    mode_file = f"data/mode_{from_id}.txt"
    current_mode = read_file(mode_file, "none")

    def set_mode(m):
        write_file(mode_file, m)

    # دالة إرسال لوحة التحكم الرئيسية للأدمن
    def send_admin_panel():
        set_mode("none")
        apple_st = rshq.get("apple_status", "on")
        gift_st = rshq.get("gift_status", "on")
        ref_val = rshq.get("ref_reward", 10)
        kb = {
            "inline_keyboard": [
                [{"text": "🚀 - لوحة تحكم الرشق والخدمات والـ API .", "callback_data": "rshqG"}],
                [{"text": f"🍏 - لعبة التفاحة ({apple_st})", "callback_data": "toggle_apple"}, {"text": f"🎁 - الهدية اليومية ({gift_st})", "callback_data": "toggle_gift"}],
                [{"text": "💰 - تعيين نقاط رابط الدعوة .", "callback_data": "set_ref_reward"}],
                [{"text": "📢 - قسم قنوات الاشتراك الإجباري .", "callback_data": "sub_channels"}],
                [{"text": "🎁 - إعدادات نقاط الهدية المجانية .", "callback_data": "set_gift"}],
                [{"text": "📊 - معلومات موقع الرشق والتفاصيل .", "callback_data": "infoRshq"}],
                [{"text": "- قفل البوت .", "callback_data": "abcd"}, {"text": "- فتح البوت .", "callback_data": "abcde"}],
                [{"text": "- اعضاء البوت .", "callback_data": "userd"}, {"text": "- قسم الاذاعة .", "callback_data": "for"}],
            ]
        }
        if callback_query:
            bot('EditMessageText', {
                'chat_id': chat_id, 'message_id': message_id,
                'text': f"👑 ¦ أهلاً بك مطوري في لوحة التحكم المركزية الماسيه للبوت 🤍\n\n🔗 ¦ نقاط رابط الدعوة الحالية: *{ref_val}* نقطة",
                'parse_mode': "markdown", 'reply_markup': json.dumps(kb)
            })
        else:
            bot('sendmessage', {
                'chat_id': chat_id,
                'text': f"👑 ¦ أهلاً بك مطوري في لوحة التحكم المركزية الماسيه للبوت 🤍\n\n🔗 ¦ نقاط رابط الدعوة الحالية: *{ref_val}* نقطة",
                'parse_mode': "markdown", 'reply_markup': json.dumps(kb)
            })

    if message and text == "/admin" and (str(from_id) in adminss or from_id == admin):
        send_admin_panel()

    if callback_query and data == "admin_home" and (str(from_id) in adminss or from_id == admin):
        send_admin_panel()

    if callback_query and data == "set_ref_reward" and (from_id == admin or str(from_id) in adminss):
        set_mode("waiting_ref_val")
        bot('EditMessageText', {
            'chat_id': chat_id, 'message_id': message_id,
            'text': "💰 ¦ أرسل الآن عدد النقاط الجديدة التي سيحصل عليها العضو مقابل كل شخص يدخل عبر رابط دعوته:",
            'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ إلغاء ورجوع للوحة الأدمن', 'callback_data': "admin_home"}]]})
        })

    if message and current_mode == "waiting_ref_val" and (from_id == admin or str(from_id) in adminss):
        if text.isnumeric():
            set_mode("none")
            val = int(text)
            rshq["ref_reward"] = val
            SETJSON(rshq)
            bot('sendMessage', {
                'chat_id': chat_id, 'text': f"✅ ¦ تم تحديث نقاط رابط الدعوة بنجاح إلى: *{val}* نقطة.", 'parse_mode': "markdown",
                'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ رجوع للوحة الأدمن', 'callback_data': "admin_home"}]]})
            })
        else:
            bot('sendMessage', {'chat_id': chat_id, 'text': "❌ ¦ يرجى إرسال أرقام صحيحة فقط."})

    if callback_query and data == "toggle_apple" and (from_id == admin or str(from_id) in adminss):
        current = rshq.get("apple_status", "on")
        rshq["apple_status"] = "off" if current == "on" else "on"
        SETJSON(rshq)
        bot('answerCallbackQuery', {'callback_query_id': update['callback_query']['id'], 'text': f"تم تغيير حالة لعبة التفاحة إلى: {rshq['apple_status']}", 'show_alert': True})
        send_admin_panel()

    if callback_query and data == "toggle_gift" and (from_id == admin or str(from_id) in adminss):
        current = rshq.get("gift_status", "on")
        rshq["gift_status"] = "off" if current == "on" else "on"
        SETJSON(rshq)
        bot('answerCallbackQuery', {'callback_query_id': update['callback_query']['id'], 'text': f"تم تغيير حالة الهدية اليومية إلى: {rshq['gift_status']}", 'show_alert': True})
        send_admin_panel()

    if callback_query and data == "abcde":
        bot('EditMessageText', {'chat_id': chat_id, 'message_id': message_id, 'text': "- تم فتح البوت بنجاح ✅", 'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ رجوع للوحة الأدمن', 'callback_data': "admin_home"}]]})})
        write_file("bot.txt", "مفتوح")

    if callback_query and data == "abcd":
        bot('EditMessageText', {'chat_id': chat_id, 'message_id': message_id, 'text': "- تم قفل البوت ❌", 'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ رجوع للوحة الأدمن', 'callback_data': "admin_home"}]]})})
        write_file("bot.txt", "متوقف")

    if callback_query and data == "userd":
        bot('EditMessageText', {'chat_id': chat_id, 'message_id': message_id, 'text': f"👥 ¦ عدد أعضاء البوت الكلي: ( {all_users_count} )", 'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ رجوع للوحة الأدمن', 'callback_data': "admin_home"}]]})})

    if callback_query and data == "for":
        bot('EditMessageText', {'chat_id': chat_id, 'message_id': message_id, 'text': "اختر نوع الإذاعة:", 'reply_markup': json.dumps({'inline_keyboard': [[{"text": "إذاعة رسالة عامة", "callback_data": "msg"}], [{"text": "⬅️ رجوع للوحة الأدمن", "callback_data": "admin_home"}]]})})

    if callback_query and data == "msg":
        set_mode("broadcast")
        bot('EditMessageText', {
            'chat_id': chat_id, 'message_id': message_id,
            'text': "قم بإرسال رسالة الإذاعة الآن لجميع المشتركين:",
            'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ إلغاء ورجوع', 'callback_data': "admin_home"}]]})
        })

    if message and current_mode == "broadcast" and (from_id == admin or str(from_id) in adminss):
        set_mode("none")
        for u_id in users:
            if u_id: bot('sendmessage', {'chat_id': u_id, 'text': text})
        bot('sendmessage', {
            'chat_id': chat_id, 'text': f"✅ ¦ تمت الإذاعة بنجاح إلى {all_users_count} مشترك.",
            'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ رجوع للوحة الأدمن', 'callback_data': "admin_home"}]]})
        })

    if callback_query and data == "sub_channels" and (from_id == admin or str(from_id) in adminss):
        ch_list = "\n".join(channels) if channels else "لا توجد قنوات مضافة حالياً."
        bot('EditMessageText', {
            'chat_id': chat_id,
            'message_id': message_id,
            'text': f"📢 ¦ قسم قنوات الاشتراك الإجباري:\n\nالقنوات الحالية:\n{ch_list}",
            'reply_markup': json.dumps({
                'inline_keyboard': [
                    [{"text": "➕ إضافة قناة اشتراك إجباري", "callback_data": "add_ch"}],
                    [{"text": "حذف جميع القنوات", "callback_data": "del_ch"}],
                    [{"text": "⬅️ رجوع للوحة الأدمن", "callback_data": "admin_home"}]
                ]
            })
        })

    if callback_query and data == "add_ch" and (from_id == admin or str(from_id) in adminss):
        set_mode("waiting_channel")
        bot('EditMessageText', {
            'chat_id': chat_id, 'message_id': message_id, 'text': "أرسل معرف القناة الآن (مثلاً @ChannelName):",
            'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ إلغاء ورجوع', 'callback_data': "sub_channels"}]]})
        })

    if message and current_mode == "waiting_channel" and (from_id == admin or str(from_id) in adminss):
        set_mode("none")
        ch_name = text.strip()
        if ch_name not in channels:
            channels.append(ch_name)
            rshq["channels"] = channels
            SETJSON(rshq)
            bot('sendMessage', {
                'chat_id': chat_id, 'text': f"✅ ¦ تمت إضافة القناة `{ch_name}` بنجاح.", 'parse_mode': "markdown",
                'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ رجوع لقسم القنوات', 'callback_data': "sub_channels"}]]})
            })
        else:
            bot('sendMessage', {
                'chat_id': chat_id, 'text': "⚠️ ¦ هذه القناة مضافة مسبقاً.",
                'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ رجوع لقسم القنوات', 'callback_data': "sub_channels"}]]})
            })

    if callback_query and data == "del_ch" and (from_id == admin or str(from_id) in adminss):
        rshq["channels"] = []
        SETJSON(rshq)
        bot('EditMessageText', {'chat_id': chat_id, 'message_id': message_id, 'text': "تم حذف جميع قنوات الاشتراك الإجباري بنجاح.", 'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ رجوع لقسم القنوات', 'callback_data': "sub_channels"}]]})})

    if callback_query and data == "set_gift" and (from_id == admin or str(from_id) in adminss):
        set_mode("waiting_gift_val")
        current_gift = rshq.get("free_gift_val", 50)
        bot('EditMessageText', {
            'chat_id': chat_id, 'message_id': message_id,
            'text': f"🎁 ¦ قيمة الهدية الحالية هي: *{current_gift}* نقطة.\n\nأرسل القيمة الجديدة بالرقم فقط:", 'parse_mode': "markdown",
            'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ إلغاء ورجوع للوحة الأدمن', 'callback_data': "admin_home"}]]})
        })

    if message and current_mode == "waiting_gift_val" and (from_id == admin or str(from_id) in adminss):
        if text.isnumeric():
            set_mode("none")
            val = int(text)
            rshq["free_gift_val"] = val
            SETJSON(rshq)
            bot('sendMessage', {
                'chat_id': chat_id, 'text': f"✅ ¦ تم تغيير قيمة الهدية إلى: *{val}* نقطة.", 'parse_mode': "markdown",
                'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ رجوع للوحة الأدمن', 'callback_data': "admin_home"}]]})
            })
        else:
            bot('sendMessage', {'chat_id': chat_id, 'text': "❌ ¦ أرسل أرقام صحيحة فقط."})

    Api_Tok = rshq.get("sToken")
    rsedi = {}
    if Api_Tok and rshq.get("sSite"):
        try:
            rsedi_response = requests.get(f"https://{rshq['sSite']}/api/v2?key={Api_Tok}&action=balance")
            rsedi = rsedi_response.json()
        except:
            rsedi = {"balance": 0, "currency": "$"}

    flos = rsedi.get("balance", 0)
    treqa = rsedi.get("currency", "$")

    if callback_query and data == "infoRshq" and (from_id == admin or str(from_id) in adminss):
        site_url = rshq.get("sSite", "غير محدد")
        bot('EditMessageText', {
            'chat_id': chat_id,
            'message_id': message_id,
            'text': f"📊 ¦ معلومات موقع الرشق المربوط:\n\n🌐 ¦ الرابط: `{site_url}`\n💰 ¦ الرصيد الحالي: *{flos} {treqa}*\n🔑 ¦ التوكن: `{Api_Tok if Api_Tok else 'غير مضبوط'}`",
            'parse_mode': "markdown",
            'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ رجوع للوحة الأدمن', 'callback_data': "admin_home"}]]})
        })

    adm_keyboard = [
        [{"text": "➕ - إضافة تطبيق/قسم جديد (مثل تليجرام، انستا)", "callback_data": "add_category"}],
        [{"text": "🚀 - إضافة خدمة داخل تطبيق/قسم", "callback_data": "add_service_to_cat"}],
        [{"text": "💰 - إضافة وخصم رصيد", "callback_data": "coins"}, {"text": "📛 - تصفير رصيد عضو", "callback_data": "msfrn"}],
        [{"text": "☢ - إنتاج كروت شحن", "callback_data": "hdiamk"}],
        [{"text": "♻️ - فتح قسم الرشق", "callback_data": "onrshq"}, {"text": "📛 - قفل قسم الرشق", "callback_data": "ofrshq"}],
        [{"text": "⚜ - تعيين توكن الموقع", "callback_data": "token"}, {"text": "🚾 - تعيين رابط الموقع", "callback_data": "SiteDomen"}],
        [{"text": "🏠 - القائمة الرئيسية للوحة", "callback_data": "admin_home"}],
    ]
    adm = {'inline_keyboard': adm_keyboard}

    if callback_query and data == "rshqG" and (from_id == admin or str(from_id) in adminss):
        bot('EditMessageText', {
            'chat_id': chat_id,
            'message_id': message_id,
            'text': f"👑 ¦ لوحة تحكم الرشق الهيكلية (أقسام وخدمات):\n\nرصيد الموقع : *{flos} {treqa}*",
            'parse_mode': "markdown",
            'reply_markup': json.dumps(adm)
        })

    # --- إدارة الأقسام والخدمات من قبل الأدمن مع أزرار رجوع كاملة ---
    if callback_query and data == "add_category" and (from_id == admin or str(from_id) in adminss):
        set_mode("waiting_cat_name")
        bot('EditMessageText', {
            'chat_id': chat_id, 'message_id': message_id,
            'text': "📁 ¦ أرسل اسم التطبيق/القسم الجديد (مثلاً: 🔹 قسم التيليجرام):",
            'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ إلغاء ورجوع للوحة الرشق', 'callback_data': "rshqG"}]]})
        })

    if message and current_mode == "waiting_cat_name" and (from_id == admin or str(from_id) in adminss):
        cat_id = str(random.randint(100, 999))
        cat_name = text.strip()
        rshq["categories"][cat_id] = {"name": cat_name, "services": {}}
        SETJSON(rshq)
        set_mode("none")
        bot('sendMessage', {
            'chat_id': chat_id, 'text': f"✅ ¦ تم إنشاء التطبيق/القسم `{cat_name}` بنجاح!",
            'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ رجوع للوحة الرشق', 'callback_data': "rshqG"}]]})
        })

    if callback_query and data == "add_service_to_cat" and (from_id == admin or str(from_id) in adminss):
        cats = rshq.get("categories", {})
        if not cats:
            bot('answerCallbackQuery', {'callback_query_id': update['callback_query']['id'], 'text': "❌ لا توجد أقسام/تطبيقات حالية. قم بإنشاء قسم أولاً!", 'show_alert': True})
            return
        
        btn_list = []
        for c_id, c_data in cats.items():
            btn_list.append([{"text": c_data["name"], "callback_data": f"select_cat_add|{c_id}"}])
        btn_list.append([{"text": "⬅️ رجوع للوحة الرشق", "callback_data": "rshqG"}])

        bot('EditMessageText', {
            'chat_id': chat_id,
            'message_id': message_id,
            'text': "اختر القسم/التطبيق الذي تريد إضافة الخدمة داخله:",
            'reply_markup': json.dumps({'inline_keyboard': btn_list})
        })

    if callback_query and e and e[0] == "select_cat_add" and (from_id == admin or str(from_id) in adminss):
        cat_id = e[1]
        write_file("data/target_cat.txt", cat_id)
        set_mode("srv_name")
        bot('EditMessageText', {
            'chat_id': chat_id, 'message_id': message_id,
            'text': "1️⃣ ¦ أرسل اسم الخدمة (مثلاً: أعضاء قنوات / اعضاء جروبات):",
            'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ إلغاء ورجوع للوحة الرشق', 'callback_data': "rshqG"}]]})
        })

    if message and current_mode == "srv_name" and (from_id == admin or str(from_id) in adminss):
        write_file("data/s_name.txt", text.strip())
        set_mode("srv_id")
        bot('sendMessage', {
            'chat_id': chat_id, 'text': "2️⃣ ¦ أرسل أيدي الخدمة (Service ID من موقع الرشق):",
            'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ إلغاء ورجوع', 'callback_data': "rshqG"}]]})
        })

    elif message and current_mode == "srv_id" and (from_id == admin or str(from_id) in adminss):
        write_file("data/s_id.txt", text.strip())
        set_mode("srv_token")
        bot('sendMessage', {
            'chat_id': chat_id, 'text': "3️⃣ ¦ أرسل توكن API الخدمة أو استخدم توكن الموقع الرئيسي بالضغط على /skip:",
            'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ إلغاء ورجوع', 'callback_data': "rshqG"}]]})
        })

    elif message and current_mode == "srv_token" and (from_id == admin or str(from_id) in adminss):
        tok_val = rshq.get("sToken", "") if text.strip() == "/skip" else text.strip()
        write_file("data/s_token.txt", tok_val)
        set_mode("srv_price")
        bot('sendMessage', {
            'chat_id': chat_id, 'text': "4️⃣ ¦ أرسل سعر الخدمة (لكل 1000 نقطة):",
            'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ إلغاء ورجوع', 'callback_data': "rshqG"}]]})
        })

    elif message and current_mode == "srv_price" and (from_id == admin or str(from_id) in adminss):
        write_file("data/s_price.txt", text.strip())
        set_mode("srv_min")
        bot('sendMessage', {
            'chat_id': chat_id, 'text': "5️⃣ ¦ أرسل الحد الأدنى للطلب:",
            'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ إلغاء ورجوع', 'callback_data': "rshqG"}]]})
        })

    elif message and current_mode == "srv_min" and (from_id == admin or str(from_id) in adminss):
        write_file("data/s_min.txt", text.strip())
        set_mode("srv_max")
        bot('sendMessage', {
            'chat_id': chat_id, 'text': "6️⃣ ¦ أرسل الحد الأقصى للطلب:",
            'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ إلغاء ورجوع', 'callback_data': "rshqG"}]]})
        })

    elif message and current_mode == "srv_max" and (from_id == admin or str(from_id) in adminss):
        s_name = read_file("data/s_name.txt")
        s_id = read_file("data/s_id.txt")
        s_token = read_file("data/s_token.txt")
        s_price = read_file("data/s_price.txt")
        s_min = read_file("data/s_min.txt")
        s_max = text.strip()
        target_cat = read_file("data/target_cat.txt")

        srv_key = str(random.randint(1000, 9999))
        if target_cat in rshq["categories"]:
            rshq["categories"][target_cat]["services"][srv_key] = {
                "name": s_name, "service_id": s_id, "token": s_token,
                "price": s_price, "min": s_min, "max": s_max
            }
            SETJSON(rshq)
            set_mode("none")
            bot('sendMessage', {
                'chat_id': chat_id, 'text': f"✅ ¦ تمت إضافة الخدمة `{s_name}` داخل القسم بنجاح وربطها مع الـ API!",
                'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ رجوع للوحة الرشق', 'callback_data': "rshqG"}]]})
            })
        else:
            set_mode("none")
            bot('sendMessage', {
                'chat_id': chat_id, 'text': "❌ حدث خطأ، القسم غير موجود.",
                'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ رجوع للوحة الرشق', 'callback_data': "rshqG"}]]})
            })

    coin = rshq.get("coin", {}).get(str(from_id), 0)
    share = rshq.get("mshark", {}).get(str(from_id), 0)
    tlby = rshq.get("tlby", {}).get(str(from_id), 0)

    RBEROO = {
        'inline_keyboard': [
            [{"text": "🌐 ¦ قسم الرشق الأقسام والتطبيقات", "callback_data": "service"}],
            [{"text": "🍏 ¦ لعبة التفاحة (اربح نقاط)", "callback_data": "apple_game"}],
            [{"text": "🎁 ¦ هدية النقاط المجانية", "callback_data": "free_gift"}],
            [{"text": "💰 ¦ ربح رصيد", "callback_data": "linkme"}, {"text": "💎 ¦ شحن رصيدك", "callback_data": "buy"}],
            [{"text": "💳 ¦ شحن كرت", "callback_data": "hdia"}, {"text": "🔄 ¦ تحويل رصيد", "callback_data": "transer"}],
            [{"text": "📦 ¦ حسابي", "callback_data": "acc"}, {"text": "📨 ¦ الدعم الفني", "url": "https://t.me/FY6FT"}]
        ]
    }

    def send_user_main():
        set_mode("none")
        if callback_query:
            bot('EditMessageText', {
                'chat_id': chat_id, 'message_id': message_id,
                'text': f"✅ ¦ أهلاً بك في بوت الرشق والتجميع Wasit 💠\n\n⚙ ¦ رصيدك : *{coin}*\n📺 ¦ أيديك : `{from_id}`\n\n⬇️ ¦ تحكم عبر الأزرار أدناه:",
                'parse_mode': "markdown", 'reply_markup': json.dumps(RBEROO)
            })
        else:
            bot('sendMessage', {
                'chat_id': chat_id,
                'text': f"✅ ¦ أهلاً بك في بوت الرشق والتجميع Wasit 💠\n\n⚙ ¦ رصيدك : *{coin}*\n📺 ¦ أيديك : `{from_id}`\n\n⬇️ ¦ تحكم عبر الأزرار أدناه:",
                'parse_mode': "markdown", 'reply_markup': json.dumps(RBEROO)
            })

    if callback_query and data == "tobot":
        send_user_main()

    if message and text == "/start" and not text.startswith("/start "):
        send_user_main()

    # --- استعراض التطبيقات والخدمات للمستخدم مع أزرار رجوع وسلاسة تامة ---
    if callback_query and data == "service":
        if rshq.get('rshqG', 'on') == "on":
            cats = rshq.get("categories", {})
            if not cats:
                bot('EditMessageText', {'chat_id': chat_id, 'message_id': message_id, 'text': "⚠️ لا توجد أقسام أو خدمات مضافة حالياً.", 'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ القائمة الرئيسية', 'callback_data': "tobot"}]]})})
                return

            keyboard = []
            for c_id, c_data in cats.items():
                keyboard.append([{'text': c_data["name"], 'callback_data': f"show_cat_services|{c_id}"}])
            keyboard.append([{'text': '⬅️ القائمة الرئيسية', 'callback_data': "tobot"}])

            bot('EditMessageText', {
                'chat_id': chat_id,
                'message_id': message_id,
                'text': f"👥 ¦ رصيدك: *{coin}*\nاختر التطبيق / القسم المطلوب:",
                'parse_mode': "markdown",
                'reply_markup': json.dumps({'inline_keyboard': keyboard})
            })
        else:
            bot('EditMessageText', {'chat_id': chat_id, 'message_id': message_id, 'text': "عذراً، قسم الرشق مغلق حالياً ❌", 'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ القائمة الرئيسية', 'callback_data': "tobot"}]]})})

    if callback_query and e and e[0] == "show_cat_services":
        cat_id = e[1]
        cats = rshq.get("categories", {})
        cat_data = cats.get(cat_id)

        if cat_data:
            srvs = cat_data.get("services", {})
            if not srvs:
                bot('answerCallbackQuery', {'callback_query_id': update['callback_query']['id'], 'text': "لا توجد خدمات داخل هذا القسم حالياً.", 'show_alert': True})
                return

            keyboard = []
            for s_id, s_info in srvs.items():
                keyboard.append([{'text': f"🔹 {s_info['name']} - ({s_info['price']} نقطة)", 'callback_data': f"select_srv|{cat_id}|{s_id}"}])
            keyboard.append([{'text': '⬅️ رجوع للأقسام', 'callback_data': "service"}])

            bot('EditMessageText', {
                'chat_id': chat_id,
                'message_id': message_id,
                'text': f"📱 ¦ قسم: *{cat_data['name']}*\nاختر الخدمة المطلوب طلبها:",
                'parse_mode': "markdown",
                'reply_markup': json.dumps({'inline_keyboard': keyboard})
            })

    if callback_query and e and e[0] == "select_srv":
        cat_id = e[1]
        srv_id = e[2]
        cats = rshq.get("categories", {})
        srv_data = cats.get(cat_id, {}).get("services", {}).get(srv_id)

        if srv_data:
            write_file(f"data/active_srv_{from_id}.json", json.dumps(srv_data))
            bot('EditMessageText', {
                'chat_id': chat_id,
                'message_id': message_id,
                'text': f"📌 ¦ خدمة: *{srv_data['name']}*\n💰 ¦ السعر لكل 1000: *{srv_data['price']}* نقطة\n📉 ¦ الحد الأدنى: {srv_data['min']}\n📈 ¦ الحد الأقصى: {srv_data['max']}\n\n🔗 ¦ أرسل الآن (رابط الطلب) المطلوب رشقـه:",
                'parse_mode': "markdown",
                'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ إلغاء ورجوع', 'callback_data': f"show_cat_services|{cat_id}"}]]})
            })
            set_mode("waiting_smm_link")

    if message and current_mode == "waiting_smm_link":
        write_file(f"data/smm_link_{from_id}.txt", text.strip())
        set_mode("waiting_smm_qty")
        bot('sendMessage', {
            'chat_id': chat_id, 'text': "🔢 ¦ أرسل الآن (الكمية المطلوبة للرشق):",
            'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ إلغاء ورجوع', 'callback_data': "service"}]]})
        })

    elif message and current_mode == "waiting_smm_qty":
        if text.isnumeric():
            qty = int(text.strip())
            srv_file = read_file(f"data/active_srv_{from_id}.json")
            if srv_file:
                srv = json.loads(srv_file)
                min_l = int(srv['min'])
                max_l = int(srv['max'])
                price_per_k = float(srv['price'])
                
                if min_l <= qty <= max_l:
                    total_cost = int((qty * price_per_k) / 1000)
                    if coin >= total_cost:
                        link_val = read_file(f"data/smm_link_{from_id}.txt")
                        api_url = f"https://{rshq.get('sSite', '')}/api/v2"
                        payload = {
                            'key': srv['token'] if srv['token'] else rshq.get('sToken', ''),
                            'action': 'add',
                            'service': srv['service_id'],
                            'link': link_val,
                            'quantity': qty
                        }
                        try:
                            resp = requests.post(api_url, data=payload).json()
                            if "order" in resp:
                                order_id = resp["order"]
                                rshq["coin"][str(from_id)] = coin - total_cost
                                rshq.setdefault("cointlb", {})[str(from_id)] = rshq["cointlb"].get(str(from_id), 0) + total_cost
                                rshq.setdefault("tlby", {})[str(from_id)] = rshq["tlby"].get(str(from_id), 0) + 1
                                SETJSON(rshq)
                                set_mode("none")
                                bot('sendMessage', {
                                    'chat_id': chat_id,
                                    'text': f"🎉 ¦ تم إرسال طلب الرشق بنجاح!\n\n🆔 ¦ رقم الطلب: `{order_id}`\n💸 ¦ التكلفة: *{total_cost}* نقطة",
                                    'parse_mode': "markdown",
                                    'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ القائمة الرئيسية', 'callback_data': "tobot"}]]})
                                })
                            else:
                                err_msg = resp.get("error", "خطأ من الموقع")
                                set_mode("none")
                                bot('sendMessage', {
                                    'chat_id': chat_id, 'text': f"❌ ¦ فشل إرسال الطلب:\n{err_msg}",
                                    'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ القائمة الرئيسية', 'callback_data': "tobot"}]]})
                                })
                        except Exception as ex:
                            set_mode("none")
                            bot('sendMessage', {
                                'chat_id': chat_id, 'text': f"❌ ¦ خطأ في الاتصال: {str(ex)}",
                                'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ القائمة الرئيسية', 'callback_data': "tobot"}]]})
                            })
                    else:
                        set_mode("none")
                        bot('sendMessage', {
                            'chat_id': chat_id, 'text': f"❌ ¦ رصيدك غير كافي! التكلفة المطلوبة {total_cost} ورصيدك {coin}.",
                            'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ القائمة الرئيسية', 'callback_data': "tobot"}]]})
                        })
                else:
                    bot('sendMessage', {'chat_id': chat_id, 'text': f"❌ ¦ الكمية يجب أن تكون بين ({min_l}) و ({max_l}). أرسل الكمية مجدداً:"})
        else:
            bot('sendMessage', {'chat_id': chat_id, 'text': "❌ ¦ أرسل أرقام صحيحة للكمية."})

    # باقي الأقسام كاملة مع أزرار رجوع
    if callback_query and data == "linkme":
        ref_val = rshq.get("ref_reward", 10)
        bot('EditMessageText', {
            'chat_id': chat_id,
            'message_id': message_id,
            'text': f"☑️ ¦ قسم ربح الرصيد عبر مشاركة رابط الدعوة:\n\n🔗 ¦ رابطك الخاص:\nhttps://t.me/{usrbot}?start={from_id}\n\n💡 ¦ هذا القسم مختص بمشاركة رابطك وتحصل على *{ref_val}* نقطة عن كل شخص يقوم بالدخلول إلى البوت عبر رابطك!",
            'parse_mode': "markdown",
            'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ القائمة الرئيسية', 'callback_data': "tobot"}]]})
        })

    if callback_query and data == "transer":
        set_mode("transfer_id")
        bot('EditMessageText', {
            'chat_id': chat_id,
            'message_id': message_id,
            'text': "🔄 ¦ أرسل الآن (أيدي الشخص) الذي تريد تحويل الرصيد إليه:",
            'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ إلغاء ورجوع', 'callback_data': "tobot"}]]})
        })

    if message and current_mode == "transfer_id":
        if text.isnumeric():
            write_file(f"data/trans_to_{from_id}.txt", text)
            set_mode("transfer_amount")
            bot('sendMessage', {
                'chat_id': chat_id, 'text': "💰 ¦ أرسل الآن (المبلغ) المطلوب تحويله:",
                'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ إلغاء ورجوع', 'callback_data': "tobot"}]]})
            })
        else:
            bot('sendMessage', {'chat_id': chat_id, 'text': "❌ ¦ يرجى إرسال أيدي صحيح (أرقام فقط)."})

    elif message and current_mode == "transfer_amount":
        if text.isnumeric():
            amount = int(text)
            to_user = read_file(f"data/trans_to_{from_id}.txt")
            current_coin = rshq.setdefault("coin", {}).get(str(from_id), 0)
            if current_coin >= amount:
                rshq["coin"][str(from_id)] = current_coin - amount
                rshq["coin"][to_user] = rshq.get("coin", {}).get(to_user, 0) + amount
                SETJSON(rshq)
                set_mode("none")
                bot('sendMessage', {
                    'chat_id': chat_id, 'text': f"✅ ¦ تم تحويل مبلغ {amount} بنجاح إلى العضو `{to_user}`!", 'parse_mode': "markdown",
                    'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ القائمة الرئيسية', 'callback_data': "tobot"}]]})
                })
                bot('sendMessage', {'chat_id': int(to_user), 'text': f"🎁 ¦ وصلت تحويلة مالية بقيمة *{amount}* إلى رصيدك.", 'parse_mode': "markdown"})
            else:
                set_mode("none")
                bot('sendMessage', {
                    'chat_id': chat_id, 'text': "❌ ¦ رصيدك غير كافي لإتمام عملية التحويل.",
                    'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ القائمة الرئيسية', 'callback_data': "tobot"}]]})
                })
        else:
            bot('sendMessage', {'chat_id': chat_id, 'text': "❌ ¦ يرجى إرسال مبلغ صحيح (أرقام فقط)."})

    if callback_query and data == "hdia":
        set_mode("redeem_card")
        bot('EditMessageText', {
            'chat_id': chat_id,
            'message_id': message_id,
            'text': "💳 ¦ أرسل الآن (كود الكرت) لشحن رصيدك:",
            'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ إلغاء ورجوع', 'callback_data': "tobot"}]]})
        })

    if message and current_mode == "redeem_card":
        set_mode("none")
        card_code = text.strip()
        keys = rshq.get("keys", {})
        if card_code in keys:
            val = keys[card_code]
            rshq.setdefault("coin", {})[str(from_id)] = rshq["coin"].get(str(from_id), 0) + val
            del rshq["keys"][card_code]
            SETJSON(rshq)
            bot('sendMessage', {
                'chat_id': chat_id, 'text': f"✅ ¦ مبروك! تم شحن الكرت بنجاح وإضافة *{val}* إلى رصيدك.", 'parse_mode': "markdown",
                'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ القائمة الرئيسية', 'callback_data': "tobot"}]]})
            })
        else:
            bot('sendMessage', {
                'chat_id': chat_id, 'text': "❌ ¦ الكود غير صحيح أو تم استخدامه مسبقاً.",
                'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ القائمة الرئيسية', 'callback_data': "tobot"}]]})
            })

    if callback_query and data == "apple_game":
        if rshq.get("apple_status", "on") == "off":
            bot('answerCallbackQuery', {'callback_query_id': update['callback_query']['id'], 'text': "عذراً، لعبة التفاحة معطلة حالياً ❌", 'show_alert': True})
            return

        timers = rshq.get("apple_timers", {})
        last_play = timers.get(str(from_id), 0)
        current_time = time.time()
        cooldown = 86400

        if current_time - last_play < cooldown:
            remaining = int((cooldown - (current_time - last_play)) / 3600)
            bot('answerCallbackQuery', {'callback_query_id': update['callback_query']['id'], 'text': f"عذراً، يمكنك اللعب مرة كل 24 ساعة فقط! انتظر {remaining} ساعة ⏳", 'show_alert': True})
            return

        bot('EditMessageText', {
            'chat_id': chat_id,
            'message_id': message_id,
            'text': "🍏 ¦ لعبة التفاحة السريعة:\nاختر تفاحة واكسب نقاطاً مجانية:",
            'reply_markup': json.dumps({
                'inline_keyboard': [
                    [{"text": "🍏 تفاحة 1", "callback_data": "pick_apple"}, {"text": "🍎 تفاحة 2", "callback_data": "pick_apple"}],
                    [{"text": "🍏 تفاحة 3", "callback_data": "pick_apple"}],
                    [{"text": "⬅️ القائمة الرئيسية", "callback_data": "tobot"}]
                ]
            })
        })

    if callback_query and data == "pick_apple":
        if rshq.get("apple_status", "on") == "off":
            return
        
        rshq.setdefault("apple_timers", {})[str(from_id)] = time.time()
        reward = random.randint(20, 200)
        rshq.setdefault("coin", {})[str(from_id)] = rshq["coin"].get(str(from_id), 0) + reward
        SETJSON(rshq)

        bot('EditMessageText', {
            'chat_id': chat_id,
            'message_id': message_id,
            'text': f"🎉 ¦ مبروك! كسبت *{reward}* نقطة أُضيفَت لرصيدك.\n📅 ¦ يمكنك اللعب مجدداً بعد 24 ساعة.",
            'parse_mode': "markdown",
            'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ القائمة الرئيسية', 'callback_data': "tobot"}]]})
        })

    if callback_query and data == "free_gift":
        if rshq.get("gift_status", "on") == "off":
            bot('answerCallbackQuery', {'callback_query_id': update['callback_query']['id'], 'text': "عذراً، الهدية اليومية معطلة حالياً ❌", 'show_alert': True})
            return

        gift_amt = rshq.get("free_gift_val", 50)
        rshq.setdefault("coin", {})[str(from_id)] = rshq["coin"].get(str(from_id), 0) + gift_amt
        SETJSON(rshq)
        bot('EditMessageText', {
            'chat_id': chat_id,
            'message_id': message_id,
            'text': f"🎁 ¦ حصلت على الهدية المجانية ({gift_amt} نقطة) بنجاح!",
            'parse_mode': "markdown",
            'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ القائمة الرئيسية', 'callback_data': "tobot"}]]})
        })

    if callback_query and data == "acc":
        bot('EditMessageText', {
            'chat_id': chat_id,
            'message_id': message_id,
            'text': f"📦 ¦ حسابك:\nرصيدك: {coin}\nالطلبات: {tlby}",
            'parse_mode': "markdown",
            'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ القائمة الرئيسية', 'callback_data': "tobot"}]]})
        })

    if callback_query and data == "buy":
        bot('EditMessageText', {
            'chat_id': chat_id,
            'message_id': message_id,
            'text': "👨‍✈️ ¦ للتواصل والشحن: @FY6FT",
            'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ القائمة الرئيسية', 'callback_data': "tobot"}]]})
        })

    if callback_query and data == "coins" and (from_id == admin or str(from_id) in adminss):
        set_mode("admin_coin_id")
        bot('EditMessageText', {
            'chat_id': chat_id, 'message_id': message_id,
            'text': "💰 ¦ أرسل أيدي العضو لتعديل رصيده:",
            'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ إلغاء ورجوع للوحة الرشق', 'callback_data': "rshqG"}]]})
        })

    if message and current_mode == "admin_coin_id" and (from_id == admin or str(from_id) in adminss):
        write_file("data/adm_target.txt", text.strip())
        set_mode("admin_coin_val")
        bot('sendMessage', {
            'chat_id': chat_id, 'text': "أرسل المبلغ المراد إضافته (أو خصمه بسالب مثل -50):",
            'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ إلغاء ورجوع', 'callback_data': "rshqG"}]]})
        })

    elif message and current_mode == "admin_coin_val" and (from_id == admin or str(from_id) in adminss):
        target_id = read_file("data/adm_target.txt")
        val = int(text.strip())
        rshq.setdefault("coin", {})[target_id] = rshq["coin"].get(target_id, 0) + val
        SETJSON(rshq)
        set_mode("none")
        bot('sendMessage', {
            'chat_id': chat_id, 'text': f"✅ ¦ تم تعديل رصيد العضو بنجاح.",
            'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ رجوع للوحة الرشق', 'callback_data': "rshqG"}]]})
        })

    if callback_query and data == "token" and (from_id == admin or str(from_id) in adminss):
        set_mode("set_token")
        bot('EditMessageText', {
            'chat_id': chat_id, 'message_id': message_id,
            'text': "ارسل توكن موقع الرشق الرئيسي الان:",
            'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ إلغاء ورجوع للوحة الرشق', 'callback_data': "rshqG"}]]})
        })

    if message and current_mode == "set_token" and (from_id == admin or str(from_id) in adminss):
        rshq["sToken"] = text.strip()
        set_mode("none")
        SETJSON(rshq)
        bot('sendMessage', {
            'chat_id': chat_id, 'text': "تم تعيين توكن الموقع الرئيسي بنجاح ✅",
            'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ رجوع للوحة الرشق', 'callback_data': "rshqG"}]]})
        })

    if callback_query and data == "SiteDomen" and (from_id == admin or str(from_id) in adminss):
        set_mode("set_domain")
        bot('EditMessageText', {
            'chat_id': chat_id, 'message_id': message_id,
            'text': "ارسل رابط موقع الرشق (مثل s3.mahratk.com):",
            'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ إلغاء ورجوع للوحة الرشق', 'callback_data': "rshqG"}]]})
        })

    if message and current_mode == "set_domain" and (from_id == admin or str(from_id) in adminss):
        parsed_url = urlparse(text.strip())
        domain = parsed_url.netloc if parsed_url.netloc else text.strip()
        rshq["sSite"] = domain
        set_mode("none")
        SETJSON(rshq)
        bot('sendMessage', {
            'chat_id': chat_id, 'text': f"تم تعيين الموقع بنجاح: {domain} ✅",
            'reply_markup': json.dumps({'inline_keyboard': [[{'text': '⬅️ رجوع للوحة الرشق', 'callback_data': "rshqG"}]]})
        })

def main():
    offset = None
    print("Advanced Structured SMM Bot with full Back Buttons is running successfully...")
    while True:
        updates_response = get_update(offset)
        if updates_response and updates_response.get('ok'):
            updates = updates_response.get('result', [])
            for update in updates:
                process_update(update)
                offset = update['update_id'] + 1
        time.sleep(1)

if __name__ == '__main__':
    main()
