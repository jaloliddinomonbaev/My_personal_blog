# MyBlog - Flask Blog Platform

MyBlog — bu Python Flask asosida yaratilgan yengil blog platformasi bo‘lib, unda foydalanuvchilar maqolalarni o‘qishlari, "Bog‘lanish" formasi orqali sizga xabar yuborishlari va administrator tomonidan blog postlarini boshqarishlari mumkin.

## 🚀 Xususiyatlari

- 📄 Maqolalarni qo‘shish, ko‘rish, o‘chirish (admin)
- 🖼️ Rasm yuklash va saqlash (mahalliy fayl tizimida)
- 📬 Foydalanuvchilarning xabarlari emailga yuboriladi (Gmail orqali)
- 🔐 Admin login orqali postlarni boshqarish
- 🌐 Bootstrap yordamida zamonaviy dizayn

## 🔧 Texnologiyalar

- Python 3.x
- Flask 2.3.3
- Firebase Admin SDK (ma'lumotlar bazasi yoki kengaytirish uchun)
- Gmail SMTP orqali email yuborish
- HTML/CSS + Bootstrap 5

## 📦 O‘rnatish

1. Repository’ni klonlang:
   ```bash
   git clone https://github.com/username/myblog.git
   cd myblog
   ```
2. Virtual muhit yaratish va kutubxonalarni o‘rnatish:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. .env fayl yarating va quyidagilarni yozing:
   ```bash
    EMAIL_ADDRESS=yourgmail@gmail.com
    EMAIL_PASSWORD=your_app_password
    ADMIN_KEY=abcd123
    ADMIN_USERNAME=name
    ADMIN_PASSWORD=abcd1234
   ```
4. Flask ilovasini ishga tushiring:
   ```bash
    flask run
   ```
5. Brauzerda oching:
   ```bash
    http://127.0.0.1:5000
   ```
🛡️ Xavfsizlik
Email yuborish uchun Gmail App Password ishlatiladi.

.env faylingizni hech qachon GitHub’ga joylamang!

Ruxsat berilmagan admin endpointlarga kirish faqat Admin-Key orqali amalga oshadi.
🤝 Hissa qo‘shish
Pull request yuboring yoki Issues orqali takliflaringizni bildiring!

📄 Litsenziya
Ushbu loyiha MIT License asosida tarqatiladi.

   
