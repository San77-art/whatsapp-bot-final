#!/usr/bin/env python3
"""
Script de teste - Testar o bot via HTTP
Execute enquanto bot.py está rodando
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def testar_bot():
    """Testa o bot com mensagens de exemplo"""
    
    mensagens_teste = [
        "Olá! Como você funciona?",
        "Qual é o melhor horário pra abrir um negócio?",
        "Me ajuda com uma estratégia de venda",
        "Qual é seu nome?"
    ]
    
    print("\n" + "="*60)
    print("🧪 TESTANDO BOT")
    print("="*60 + "\n")
    
    # Testar health
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print(f"✅ Bot online: {response.json()}\n")
    except Exception as e:
        print(f"❌ Bot não está rodando: {e}")
        print("   Execute: python bot.py")
        return
    
    # Testar mensagens
    for i, mensagem in enumerate(mensagens_teste, 1):
        print(f"📨 [{i}] Você: {mensagem}")
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/message",
                json={
                    "user_id": "teste_user",
                    "message": mensagem
                },
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                data = response.json()
                resposta = data['response']
                print(f"🤖 Bot: {resposta}\n")
            else:
                print(f"❌ Erro: {response.status_code} - {response.text}\n")
        
        except Exception as e:
            print(f"❌ Erro ao conectar: {e}\n")
            break
        
        time.sleep(1)  # Esperar 1 segundo entre mensagens
    
    print("="*60)
    print("✅ Teste concluído!")
    print("="*60 + "\n")

if __name__ == '__main__':
    testar_bot()
