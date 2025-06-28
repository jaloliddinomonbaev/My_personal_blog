from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime
import os
import uuid
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText

load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Mahalliy uploads papkasini yaratish
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

temp_posts = []
temp_messages = []

ADMIN_KEY = os.getenv('ADMIN_KEY', 'ac1234ca')
ADMIN_USERNAME = os.getenv('ADMIN_USERNAME', 'jaloliddin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'ac1234ca')

def upload_image_locally(file):
    try:
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        return f"/{app.config['UPLOAD_FOLDER']}/{unique_filename}"
    except Exception as e:
        print(f"Mahalliy rasm yuklashda xatolik: {e}")
        return None

@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            return jsonify({'success': True, 'message': 'Admin muvaffaqiyatli kirildi!', 'admin_key': ADMIN_KEY})
        else:
            return jsonify({'success': False, 'message': 'Noto\'g\'ri ma\'lumotlar!'})
    except Exception as e:
        print(f"Admin login xatosi: {e}")
        return jsonify({'success': False, 'message': 'Xatolik yuz berdi!'})

@app.route('/api/admin/upload-image', methods=['POST'])
def upload_image():
    try:
        admin_key = request.headers.get('Admin-Key')
        if admin_key != ADMIN_KEY:
            return jsonify({'success': False, 'message': 'Unauthorized request!'}), 401

        if 'image' not in request.files:
            return jsonify({'success': False, 'message': 'Rasm tanlanmagan!'})

        file = request.files['image']
        if file.filename == '':
            return jsonify({'success': False, 'message': 'Rasm tanlanmagan!'})

        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
        if not ('.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
            return jsonify({'success': False, 'message': 'Noto\'g\'ri fayl formati!'})

        image_url = upload_image_locally(file)
        if not image_url:
            return jsonify({'success': False, 'message': 'Rasm yuklanmadi!'})

        return jsonify({'success': True, 'image_url': image_url})
    except Exception as e:
        print(f"Rasm yuklash xatosi: {e}")
        return jsonify({'success': False, 'message': 'Xatolik yuz berdi!'})

@app.route('/api/admin/posts', methods=['POST'])
def add_post():
    try:
        admin_key = request.headers.get('Admin-Key')
        if admin_key != ADMIN_KEY:
            return jsonify({'success': False, 'message': 'Unauthorized request!'}), 401

        data = request.get_json()
        if not data or not data.get('title') or not data.get('content'):
            return jsonify({'success': False, 'message': 'Sarlavha va matn kiritilishi shart!'}), 400

        content = data.get('content', '')
        excerpt = content[:150] + '...' if len(content) > 150 else content

        post_data = {
            'title': data.get('title'),
            'content': content,
            'excerpt': excerpt,
            'image': data.get('image', ''),
            'date': datetime.now().strftime('%Y-%m-%d'),
            'timestamp': datetime.now().isoformat(),
            'id': str(uuid.uuid4())  # Har bir post uchun unikal ID
        }

        temp_posts.append(post_data)
        print(f"Post mahalliy saqlandi: {post_data['id']}")

        return jsonify({'success': True, 'message': 'Post qo\'shildi!', 'post': post_data})
    except Exception as e:
        print(f"Post qo'shish xatosi: {e}")
        return jsonify({'success': False, 'message': f'Xatolik yuz berdi! {e}'})

@app.route('/api/posts')
def get_posts():
    try:
        sorted_posts = sorted(temp_posts, key=lambda x: x.get('timestamp', ''), reverse=True)
        print(f"Postlar mahalliy olindi: {len(sorted_posts)} ta")
        return jsonify(sorted_posts)
    except Exception as e:
        print(f"Postlarni olish xatosi: {e}")
        return jsonify(temp_posts)

@app.route('/api/posts/<post_id>')
def get_single_post(post_id):
    try:
        for post in temp_posts:
            if str(post.get('id')) == post_id:
                print(f"Post {post_id} mahalliy olindi")
                return jsonify(post)
        return jsonify({'error': 'Post topilmadi'}), 404
    except Exception as e:
        print(f"Post olish xatosi: {e}")
        return jsonify({'error': 'Xatolik yuz berdi'}), 500

@app.route('/api/admin/posts/<post_id>', methods=['DELETE'])
def delete_post(post_id):
    try:
        admin_key = request.headers.get('Admin-Key')
        if admin_key != ADMIN_KEY:
            return jsonify({'success': False, 'message': 'Unauthorized request!'}), 401

        global temp_posts
        temp_posts = [post for post in temp_posts if str(post.get('id')) != post_id]
        print(f"Post {post_id} mahalliy o'chirildi")

        return jsonify({'success': True, 'message': 'Post o\'chirildi!'})
    except Exception as e:
        print(f"Post o'chirish xatosi: {e}")
        return jsonify({'success': False, 'message': f'Xatolik yuz berdi! {e}'})

@app.route('/api/admin/messages', methods=['GET'])
def get_all_messages():
    try:
        admin_key = request.headers.get('Admin-Key')
        if admin_key != ADMIN_KEY:
            return jsonify({'success': False, 'message': 'Unauthorized request!'}), 401

        print(f"Xabarlar mahalliy olindi: {len(temp_messages)} ta")
        return jsonify({'success': True, 'messages': temp_messages})
    except Exception as e:
        print(f"Xabarlarni olish xatosi: {e}")
        return jsonify({'success': False, 'messages': []})

@app.route('/api/admin/messages/<message_id>', methods=['DELETE'])
def admin_delete_message(message_id):
    try:
        admin_key = request.headers.get('Admin-Key')
        if admin_key != ADMIN_KEY:
            return jsonify({'success': False, 'message': 'Unauthorized request!'}), 401

        global temp_messages
        temp_messages = [msg for msg in temp_messages if msg.get('id') != message_id]
        print(f"Xabar {message_id} mahalliy o'chirildi")

        return jsonify({'success': True, 'message': 'Xabar o\'chirildi!'})
    except Exception as e:
        print(f"Xabar o'chirish xatosi: {e}")
        return jsonify({'success': False, 'message': f'Xatolik yuz berdi! {e}'})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/blog/<post_id>')
def blog_post(post_id):
    return render_template('blog_post.html', post_id=post_id)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')

@app.route('/api/contact', methods=['POST'])
def submit_contact():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        message = data.get('message')

        # Emailni tayyorlash
        subject = f"Yangi bog'lanish xabari: {name}"
        body = f"Ism: {name}\nEmail: {email}\n\nXabar:\n{message}"
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = os.getenv('EMAIL_ADDRESS')
        msg['To'] = os.getenv('EMAIL_ADDRESS')

        # SMTP orqali yuborish
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.login(os.getenv('EMAIL_ADDRESS'), os.getenv('EMAIL_PASSWORD'))
        smtp_server.send_message(msg)
        smtp_server.quit()

        print("Xabar emailga yuborildi!")
        return jsonify({'success': True, 'message': 'Xabaringiz muvaffaqiyatli yuborildi!'})
    except Exception as e:
        print(f"Kontakt yuborish xatosi: {e}")
        return jsonify({'success': False, 'message': 'Xatolik yuz berdi!'})

@app.route('/api/messages', methods=['GET'])
def get_messages():
    try:
        print(f"Xabarlar mahalliy olindi: {len(temp_messages)} ta")
        return jsonify(temp_messages)
    except Exception as e:
        print(f"Xabarlarni olish xatosi: {e}")
        return jsonify(temp_messages)

@app.route('/api/messages', methods=['POST'])
def send_message():
    try:
        data = request.get_json()
        if not data or not data.get('name') or not data.get('message'):
            return jsonify({'success': False, 'message': 'Ism va xabar kiritilishi shart!'}), 400

        message_data = {
            'name': data.get('name'),
            'message': data.get('message'),
            'timestamp': datetime.now().isoformat(),
            'id': str(uuid.uuid4())  # Har bir xabar uchun unikal ID
        }

        temp_messages.append(message_data)
        print(f"Xabar mahalliy saqlandi: {message_data['id']}")

        return jsonify({'success': True})
    except Exception as e:
        print(f"Xabar yuborish xatosi: {e}")
        return jsonify({'success': False})

if __name__ == '__main__':
    app.run(debug=True)