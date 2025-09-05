import os
import uuid
import google.generativeai as genai
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from PIL import Image
import qrcode
import io

# --- INTERRUPTOR DE SIMULAÇÃO ---
MODO_SIMULACAO = False
# -------------------------------

# --- CONFIGURAÇÕES ---
load_dotenv()
if not MODO_SIMULACAO:
    try:
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        print("Configuração da API GenAI bem-sucedida.")
    except Exception as e:
        print(f"ERRO CRÍTICO: Não foi possível configurar a API Key. Erro: {e}")

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BACKGROUNDS_PATH = os.path.join(BASE_DIR, 'assets', 'backgrounds')
OVERLAYS_PATH = os.path.join(BASE_DIR, 'assets', 'overlays')
FINAL_IMAGES_PATH = os.path.join(BASE_DIR, 'static', 'final_images')
QRCODES_PATH = os.path.join(BASE_DIR, 'static', 'qrcodes')

os.makedirs(FINAL_IMAGES_PATH, exist_ok=True)
os.makedirs(QRCODES_PATH, exist_ok=True)

def determine_background(answers):
    score = 0
    for answer in answers.values():
        if answer == 'A': score += 1
        elif answer == 'B': score += 2
        elif answer == 'C': score += 3
        elif answer == 'D': score += 4
    
    if score <= 5: return "cenario1.jpg"
    if score <= 10: return "cenario2.jpg"
    if score <= 15: return "cenario3.jpg"
    if score <= 20: return "cenario4.jpg"
    return "cenario4.jpg"

@app.route('/api/generate-image', methods=['POST'])
def generate_image_endpoint():
    if 'photo' not in request.files:
        return jsonify({'success': False, 'error': 'Nenhuma foto enviada'}), 400
    
    user_photo_file = request.files['photo']
    quiz_answers = request.form.to_dict()

    try:
        generated_image = None
        background_name = determine_background(quiz_answers)
        background_path = os.path.join(BACKGROUNDS_PATH, background_name)

        if MODO_SIMULACAO:
            print("--- MODO DE SIMULAÇÃO ATIVO ---")
            generated_image = Image.open(background_path)
        else:
            print("--- MODO REAL ATIVO ---")
            user_photo_img = Image.open(user_photo_file.stream)
            background_img = Image.open(background_path)
            
            model = genai.GenerativeModel('gemini-2.5-flash-image-preview')
            
            prompt = """
            Usando a imagem da pessoa e a imagem de fundo fornecidas, crie uma nova cena.
            OBJETIVO: O resultado final deve ser uma imagem da pessoa integrada ao cenário. O rosto da pessoa deve ser preservado. A pessoa deve estar vestindo uma roupa de minerador espacial futurista que combine com a estética do cenário.
            A imagem final deve ser realista e bem integrada. Retorne APENAS a imagem.
            """

            response = model.generate_content([prompt, user_photo_img, background_img])
            
            image_part = response.parts[0]
            if image_part.inline_data:
                image_data = image_part.inline_data.data
                generated_image = Image.open(io.BytesIO(image_data))
            else:
                error_text = image_part.text if image_part.text else "A IA não retornou uma imagem."
                raise Exception(error_text)

        logo_img = Image.open(os.path.join(OVERLAYS_PATH, 'logo.png')).convert("RGBA")
        logo_img.thumbnail((300, 300))
        logo_pos = (generated_image.width - logo_img.width - 50, generated_image.height - logo_img.height - 50)
        generated_image.paste(logo_img, logo_pos, logo_img)

        filename = f"{uuid.uuid4()}.png"
        final_image_path = os.path.join(FINAL_IMAGES_PATH, filename)
        generated_image.save(final_image_path)
        
        base_url = request.host_url
        image_url = f"{base_url}static/final_images/{filename}"
        
        qr = qrcode.make(image_url)
        qr_filename = f"qr_{filename}"
        qr_path = os.path.join(QRCODES_PATH, qr_filename)
        qr.save(qr_path)
        qr_url = f"{base_url}static/qrcodes/{qr_filename}"

        return jsonify({ 'success': True, 'imageUrl': image_url, 'qrCodeUrl': qr_url })
    
    except Exception as e:
        print(f"--- ERRO NO PROCESSAMENTO DA IMAGEM ---")
        print(f"Erro: {e}")
        print(f"------------------------------------")
        return jsonify({'success': False, 'error': f"Ocorreu um erro no servidor: {e}"}), 500

@app.route('/static/<path:folder>/<path:filename>')
def serve_static_files(folder, filename):
    return send_from_directory(os.path.join(BASE_DIR, 'static', folder), filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)