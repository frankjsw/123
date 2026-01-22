import base64
import os
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

print("=" * 60)
print("Telegram Session 生成工具")
print("=" * 60)
print()

# 从环境变量获取 API_ID 和 API_HASH
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

# 如果没有获取到值，提示错误并退出
if not API_ID or not API_HASH:
    print("错误: API_ID 和 API_HASH 环境变量未设置，请检查配置。")
    exit(1)

print("正在启动 Telegram 登录... (将要求输入手机号和验证码)")

# 创建客户端
client = TelegramClient(
    StringSession(), 
    int(API_ID), 
    API_HASH
)

# 模拟手机号输入的回调
def phone_callback():
    # 从环境变量读取手机号
    return os.getenv("PHONE_NUMBER")  # 例如 "+1234567890"

# 自动输入验证码的回调
def code_callback():
    # 从环境变量读取验证码
    return os.getenv("SMS_CODE")  # 例如 "12345"

# 设置手机号和验证码回调
client.session.set_phone(phone_callback)
client.session.set_code(code_callback)

with client:
    # 启动客户端并登录
    me = client.get_me()
    print(f"✅ 登录成功！用户: {me.first_name} {me.last_name or ''}，用户名: @{me.username or 'N/A'}，ID: {me.id}")

    # 获取 StringSession
    string_session = StringSession.save(client.session)

    # 保存到 session.string 文件
    with open("session.string", "w") as f:
        f.write(string_session)

    # 生成 Base64 编码
    session_b64 = base64.b64encode(string_session.encode('utf-8')).decode('utf-8')

# 输出结果
print("=" * 60)
print("生成的文件:")
print("=" * 60)
print("1. telegram.session (SQLite 格式)")
print("2. session.string (StringSession 格式)")
print("=" * 60)
print("环境变量 SESSION_STRING (Base64 编码):")
print("=" * 60)
print(session_b64)
print("=" * 60)
