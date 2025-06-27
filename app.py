# app.py atualizado
import os
from flask import Flask, request, render_template, jsonify, url_for  # Importe url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

# 1. ATUALIZE O CAMINHO PARA A PASTA DE UPLOADS DENTRO DE 'static'
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload/image', methods=['POST'])
def uploadImage():
    if 'photo' not in request.files:
        return jsonify({'error': 'Nenhuma parte de arquivo na requisição'}), 400

    file = request.files['photo']

    if file.filename == '':
        return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
    
    if file:
        filename = secure_filename(file.filename)
        caminho_para_salvar = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(caminho_para_salvar)

        # 2. GERE A URL CORRETA USANDO url_for
        # Isso vai gerar uma URL como '/static/uploads/nome_do_arquivo.jpg'
        url_do_arquivo = url_for('static', filename=f'uploads/{filename}')

        return jsonify({
            'message': f'Arquivo "{filename}" enviado com sucesso!', 
            'path': url_do_arquivo
        })

if __name__ == '__main__':
    app.run(debug=True)