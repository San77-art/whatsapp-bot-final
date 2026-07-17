#!/usr/bin/env python3
"""
Bot WhatsApp com Groq API - 100% GRÁTIS
Sem custos, sem limites
"""

from flask import Flask, request, jsonify
from groq import Groq
import os
from dotenv import load_dotenv
import json
import traceback
from datetime import datetime

load_dotenv()

app = Flask(__name__)
client = Groq(api_key=os.getenv("GROQ_API_KEY", ""))

# Histórico de conversas
conversas = {}

SYSTEM_PROMPT = """
Você é um assistente de IA profissional, amigável e eficiente.
Responda em português brasileiro.
Seja conciso e direto.
Mantenha tom profissional mas descontraído.
Se não sabe, diga que precisa transferir para um atendente.
"""

@app.route('/api/message', methods=['POST'])
def receber_mensagem():
    """Recebe mensagem, processa com Groq, retorna resposta"""
    try:
        data = request.json
        user_id = data.get('user_id', 'default')
        mensagem = data.get('message', '')
        
        if not mensagem:
            return jsonify({'erro': 'Mensagem vazia'}), 400
        
        # Inicializar histórico
        if user_id not in conversas:
            conversas[user_id] = []
        
        # Adicionar mensagem
        conversas[user_id].append({
            "role": "user",
            "content": mensagem
        })
        
        print(f"📨 [{datetime.now().strftime('%H:%M:%S')}] {user_id}: {mensagem}")
        
        # Verificar chave Groq
        groq_key = os.getenv("GROQ_API_KEY")
        if not groq_key or groq_key == "":
            print("❌ ERRO: GROQ_API_KEY não configurada!")
            return jsonify({
                'success': False,
                'erro': 'GROQ_API_KEY não configurada no ambiente'
            }), 500
        
        print(f"✅ Chave Groq detectada")
        
        # Chamar Groq
        try:
            print(f"🔄 Chamando Groq com modelo llama-3.3-70b-versatile...")
            
            resposta = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    *conversas[user_id][-10:]  # Últimas 10 mensagens
                ],
                temperature=0.7,
                max_tokens=256
            )
            
            # Extrair resposta
            assistant_message = resposta.choices[0].message.content
            
            # Guardar histórico
            conversas[user_id].append({
                "role": "assistant",
                "content": assistant_message
            })
            
            print(f"✅ Bot respondeu: {assistant_message[:100]}...")
            
            return jsonify({
                'success': True,
                'response': assistant_message,
                'timestamp': datetime.now().isoformat()
            })
            
        except Exception as groq_error:
            print(f"❌ ERRO GROQ: {str(groq_error)}")
            print(f"❌ Tipo de erro: {type(groq_error)}")
            traceback.print_exc()
            return jsonify({
                'success': False,
                'erro': f'Erro na API Groq: {str(groq_error)}'
            }), 500
        
    except Exception as e:
        print(f"❌ ERRO GERAL: {str(e)}")
        print(f"❌ Tipo de erro: {type(e)}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'erro': str(e)
        }), 500

@app.route('/', methods=['GET'])
def index():
    return """
    <h1>🤖 Bot IA com Groq (GRÁTIS!)</h1>
    <p><strong>API:</strong> POST /api/message</p>
    <p><strong>Body (JSON):</strong></p>
    <pre>{"user_id": "client123", "message": "sua mensagem aqui"}</pre>
    """

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'online', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    
    print("\n" + "="*50)
    print("🤖 Bot IA com Groq iniciando...")
    print(f"📍 http://0.0.0.0:{port}")
    print("="*50 + "\n")
    
    app.run(host='0.0.0.0', port=port, debug=False)