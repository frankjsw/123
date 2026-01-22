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

# 创建客户端并登录
# 这会在当前目录生成 telegram.session 文件
client = TelegramClient("telegram", int(API_ID), API_HASH)

with client:
    # 获取当前用户信息确认登录成功
    me = client.get_me()
    print()
    print(f"✅ 登录成功！")
    print(f"   用户: {me.first_name} {me.last_name or ''}")
    print(f"   用户名: @{me.username or 'N/A'}")
    print(f"   ID: {me.id}")
    print()

    # 获取 StringSession
    string_session = StringSession.save(client.session)

    # 保存到 session.string 文件
    with open("session.string", "w") as f:
        f.write(string_session)

    # 生成 Base64 编码
    session_b64 = base64.b64encode(string_session.encode('utf-8')).decode('utf-8')

print("=" * 60)
print("生成的文件:")
print("=" * 60)
print()
print("1. telegram.session (SQLite 格式)")
print("   用途: 上传到 Docker 容器的 /app/data/ 或 /app/data/session_data/")
print()
print("2. session.string (StringSession 格式)")
print("   用途: 上传到 Docker 容器的 /app/data/")
print()
print("=" * 60)
print("环境变量 SESSION_STRING (Base64 编码):")
print("=" * 60)
print()
print(session_b64)
print()
print("=" * 60)
print("复制上面的 Base64 字符串，设置为环境变量 SESSION_STRING")
print("适用于不支持文件上传的 PaaS 平台")
print("=" * 60)
