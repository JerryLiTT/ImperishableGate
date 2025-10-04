# 文件名: send_email.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(sender, password, receiver, subject, body):
    """
    发送邮件函数
    参数:
        sender (str): 发件人邮箱
        password (str): 发件人邮箱的应用专用密码
        receiver (str): 收件人邮箱
        subject (str): 邮件主题
        body (str): 邮件正文
    返回:
        bool: 发送成功返回 True，失败返回 False
    """
    # 创建邮件
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain", "utf-8"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, password)
        server.sendmail(sender, receiver, msg.as_string())
        return True
    except Exception as e:
        print("邮件发送失败:", e)
        return False
    finally:
        if server:
            server.quit() 
