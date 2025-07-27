from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import time
from config import API_ID, API_HASH, BOT_TOKEN, OWNER_ID, LOG_CHANNEL_ID, START_IMG_URL

SENDER_EMAIL = 'domainisgod8i@gmail.com'
EMAIL_PASSWORD = 'fdsq hqpz vhhn eckw'

SMTP_SETTINGS = {
    'gmail.com': ('smtp.gmail.com', 587),
    'outlook.com': ('smtp.office365.com', 587),
    'hotmail.com': ('smtp.office365.com', 587),
    'yahoo.com': ('smtp.mail.yahoo.com', 587)
}

def get_smtp_settings(email):
    domain = email.split('@')[-1]
    return SMTP_SETTINGS.get(domain)

def login_email(sender_email, sender_password):
    try:
        smtp_settings = get_smtp_settings(sender_email)
        if not smtp_settings:
            return False, 'Unsupported email provider.'

        smtp_server, smtp_port = smtp_settings
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.quit()
        return True, 'Login successful.'
    except smtplib.SMTPAuthenticationError:
        return False, 'Login failed. Please check your email or password.'
    except Exception as e:
        return False, f'Error: {str(e)}'

def send_email(recipient_email, subject, body, sender_email, sender_password):
    try:
        smtp_settings = get_smtp_settings(sender_email)
        if not smtp_settings:
            raise ValueError('Unsupported email provider.')

        smtp_server, smtp_port = smtp_settings

        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())
        server.quit()

        print(f"Email sent to {recipient_email}")
    except Exception as e:
        print(f"Error sending email: {e}")

MAIL_TO, SUBJECT, BODY, COUNT = range(4)

devine = Client(
    "devine",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

user_state = {}

authorized_users = [6440363814, 1374057577, 6716349855, 7392339658, 6338745050]

@devine.on_message(filters.command("start"))
async def start_command(client, message):
    if message.from_user.id not in authorized_users:
        await message.reply("ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀᴄᴄᴇss ᴛᴏ ᴜsᴇ ᴛʜɪs. ᴠɪsɪᴛ @devine_support")
        
        await client.send_message(
            chat_id=LOG_CHANNEL_ID,
            text=(
                f"{message.from_user.mention} ɪs ᴛʀʏɪɴɢ ᴛᴏ sᴛᴀʀᴛ ʙᴏᴛ.\n\n"
                f"• ɪᴅ : <code>{message.from_user.id}</code>\n"
                f"• ᴜsᴇʀɴᴀᴍᴇ : t.me/{message.from_user.username or 'No username'}"
            )
        )
        return

    await message.reply_photo(
        photo=START_IMG_URL,
        caption=(
            f"ʏᴏᴏ {message.from_user.mention}, ✨\n\n"
            "<a href='https://t.me/Tdnetworkk' target='_blank'><b>•</b></a>ᴛʜɪs ʙᴏᴛ ᴀʟʟᴏᴡs ʏᴏᴜ ᴛᴏ sᴇɴᴅ ᴇᴍᴀɪʟs ᴅɪʀᴇᴄᴛʟʏ ғʀᴏᴍ ʏᴏᴜʀ ᴛᴇʟᴇɢʀᴀᴍ ᴄʜᴀᴛ."
        ),
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("ᴄʀᴇᴀᴛᴏʀ", user_id=OWNER_ID),
                InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇs", url=f'https://t.me/Devine_Network')
            ],
            [
                InlineKeyboardButton("ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅs", callback_data='help_callback')
            ]
        ])
    )
    
    await client.send_message(
        chat_id=LOG_CHANNEL_ID,
        text=(
            f"<b>ʙᴏᴛ sᴛᴀʀᴛᴇᴅ ʙʏ {message.from_user.mention}.</b>\n\n"
            f"<b>• ɪᴅ :</b> <code>{message.from_user.id}</code>\n"
            f"<b>• ᴜsᴇʀɴᴀᴍᴇ :</b> t.me/{message.from_user.username or 'none'}"
        )
    )

@devine.on_callback_query(filters.create(lambda _, __, query: query.data == 'help_callback'))
async def help_callback(client, query):
    await query.answer()
    help_text = (
        "ʜᴇʟᴘ ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅs:\n\n"
        "/start - ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ.\n"
        "/sendmail - ᴜsᴇ ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴛᴏ sᴇɴᴅ ᴀɴ ᴇᴍᴀɪʟ.\n\n"
        "ᴜsᴇ ᴛʜᴇ ʙᴜᴛᴛᴏɴs ᴛᴏ ᴄᴏɴᴛᴀᴄᴛ ᴛʜᴇ ᴄʀᴇᴀᴛᴏʀ ᴀɴᴅ ᴄʜᴇᴄᴋ ᴜᴘᴅᴀᴛᴇs."
    )
    keyboard = [
        [
            InlineKeyboardButton("ʙᴀᴄᴋ", callback_data='back_to_main')
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text=help_text, reply_markup=reply_markup)

@devine.on_callback_query(filters.create(lambda _, __, query: query.data == 'back_to_main'))
async def back_to_main(client, query):
    await query.answer()
    await query.message.edit_text(
        text=f"ʏᴏᴏ {query.from_user.mention}, ✨\n\n"
             "ᴛʜɪs ʙᴏᴛ ᴀʟʟᴏᴡs ʏᴏᴜ ᴛᴏ sᴇɴᴅ ᴇᴍᴀɪʟs ᴅɪʀᴇᴄᴛʟʏ ғʀᴏᴍ ʏᴏᴜʀ ᴛᴇʟᴇɢʀᴀᴍ ᴄʜᴀᴛ.",
        reply_markup=InlineKeyboardMarkup([
            [
                InlineKeyboardButton("ᴄʀᴇᴀᴛᴏʀ", user_id=OWNER_ID),
                InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇs", url=f'https://t.me/Devine_Network')
            ],
            [
                InlineKeyboardButton("ʜᴇʟᴘ & ᴄᴏᴍᴍᴀɴᴅs", callback_data='help_callback')
            ]
        ])
    )


@devine.on_message(filters.command("sendmail"))
async def sendmail(client, message):
    if message.from_user.id not in authorized_users:
        await message.reply("ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀᴄᴄᴇss ᴛᴏ ᴜsᴇ ᴛʜɪs. ᴠɪsɪᴛ @devine_support")
        return

    chat_id = message.chat.id
    user_state[chat_id] = {'step': MAIL_TO}
    await client.send_message(chat_id, 'ᴘʀᴏᴠɪᴅᴇ ᴛʜᴇ ʀᴇᴄɪᴘɪᴇɴᴛ ᴇᴍᴀɪʟ ᴀᴅᴅʀᴇss:')

@devine.on_message(filters.text)
async def handle_response(client, message):
    chat_id = message.chat.id
    user_data = user_state.get(chat_id, {})

    if user_data.get('step') == MAIL_TO:
        user_state[chat_id]['mail_to'] = message.text
        user_state[chat_id]['step'] = SUBJECT
        await client.send_message(chat_id, 'ᴘʀᴏᴠɪᴅᴇ ᴛʜᴇ ᴇᴍᴀɪʟ sᴜʙᴊᴇᴄᴛ:')

    elif user_data.get('step') == SUBJECT:
        user_state[chat_id]['subject'] = message.text
        user_state[chat_id]['step'] = BODY
        await client.send_message(chat_id, 'ᴘʀᴏᴠɪᴅᴇ ᴛʜᴇ ᴇᴍᴀɪʟ ʙᴏᴅʏ:')

    elif user_data.get('step') == BODY:
        user_state[chat_id]['body'] = message.text
        user_state[chat_id]['step'] = COUNT
        await client.send_message(chat_id, 'ʜᴏᴡ ᴍᴀɴʏ ᴛɪᴍᴇs sʜᴏᴜʟᴅ ᴛʜᴇ ᴇᴍᴀɪʟ ʙᴇ sᴇɴᴛ?')

    elif user_data.get('step') == COUNT:
        try:
            count = int(message.text)

            if count > 100:
                await client.send_message(chat_id, "ʏᴏᴜ ᴄᴀɴ'ᴛ sᴇɴᴅ ᴍᴏʀᴇ ᴛʜᴀɴ 100 ᴇᴍᴀɪʟs ᴀᴛ ᴏɴᴄᴇ.")
                return

            recipient_email = user_state[chat_id]['mail_to']
            subject = user_state[chat_id]['subject']
            body = user_state[chat_id]['body']

            if not SENDER_EMAIL or not EMAIL_PASSWORD:
                await client.send_message(chat_id, 'ᴇᴍᴀɪʟ ᴄʀᴇᴅᴇɴᴛɪᴀʟs ᴀʀᴇ ɴᴏᴛ sᴇᴛ. Pʟᴇᴀsᴇ sᴇᴛ ᴛʜᴇᴍ ɪɴ ᴇɴᴠɪʀᴏɴᴍᴇɴᴛ ᴠᴀʀɪᴀʙʟᴇs.')
                return

            login_success, login_message = login_email(SENDER_EMAIL, EMAIL_PASSWORD)
            if not login_success:
                await client.send_message(chat_id, login_message)
                return

            for _ in range(count):
                send_email(recipient_email, subject, body, SENDER_EMAIL, EMAIL_PASSWORD)
                time.sleep(2)

            await client.send_message(chat_id, f"ᴇᴍᴀɪʟs sᴇɴᴛ {count} ᴛɪᴍᴇs ᴛᴏ {recipient_email} sᴜᴄᴄᴇssғᴜʟʟʏ!")

            if LOG_CHANNEL_ID:
                user = message.from_user
                await client.send_message(
                    chat_id=LOG_CHANNEL_ID,
                    text=(
                        f"<b>ᴇᴍᴀɪʟs sᴇɴᴛ</b>\n\n"
                        f"<b>• ʀᴇᴄɪᴘɪᴇɴᴛ :</b> {recipient_email}\n"
                        f"<b>• sᴜʙᴊᴇᴄᴛ :</b> {subject}\n"
                        f"<b>• ʙᴏᴅʏ :</b> {body}\n"
                        f"<b>• ᴛɪᴍᴇs :</b> {count}\n"
                        f"<b>• sᴇɴᴅᴇᴅ ʙʏ :</b> {SENDER_EMAIL}\n\n"
                        f"<b>• ʀᴇqᴜᴇsᴛᴇᴅ ʙʏ :</b> {user.mention}\n"
                        f"<b>• ᴜsᴇʀɴᴀᴍᴇ :</b> @{user.username}\n"
                        f"<b>• ɪᴅ :</b> <code>{user.id}</code>"
                    ),
                )
        except Exception as e:
            await client.send_message(chat_id, f"ғᴀɪʟᴇᴅ ᴛᴏ sᴇɴᴅ ᴇᴍᴀɪʟs: {str(e)}")
        
        user_state.pop(chat_id, None)
        
@devine.on_message(filters.command(["start", "sendmail"]) & ~filters.user(authorized_users))
async def restricted_access(client, message):
    await message.reply_text("ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀᴄᴄᴇss ᴛᴏ ᴜsᴇ ᴛʜɪs. ᴠɪsɪᴛ @devine_support", quote=True)


devine.run()
