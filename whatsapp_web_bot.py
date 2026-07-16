#!/usr/bin/env python3
"""
Bot WhatsApp Web com IA Groq
Conecta com seu WhatsApp e responde automaticamente
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from groq import Groq
import time
import os
import random
from dotenv import load_dotenv

load_dotenv()

# Configurar Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY", ""))

SYSTEM_PROMPT = """
Você é um assistente de IA profissional, amigável e eficiente.
Responda em português brasileiro.
Seja conciso e direto (máximo 3 linhas).
Mantenha tom profissional mas descontraído.
Se não sabe, diga que precisa transferir para um atendente.
"""

class WhatsAppBot:
    def __init__(self):
        self.driver = None
        self.processed_messages = set()
        
    def iniciar(self):
        """Inicia o navegador e conecta ao WhatsApp Web"""
        print("🚀 Iniciando WhatsApp Web Bot...")
        
        options = webdriver.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--user-data-dir=./whatsapp_cache')
        
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
        except Exception as e:
            print(f"❌ Erro ao iniciar Chrome: {e}")
            return False
        
        self.driver.get("https://web.whatsapp.com")
        
        print("📱 Escaneie o QR code com seu WhatsApp!")
        print("⏳ Esperando autenticação... (máximo 30 segundos)")
        
        # Esperar até que o chat esteja carregado
        try:
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div[role='listitem']"))
            )
            print("✅ WhatsApp conectado com sucesso!")
            time.sleep(2)
        except Exception as e:
            print(f"❌ Erro ao conectar: {e}")
            self.driver.quit()
            return False
        
        return True
    
    def processar_mensagens(self):
        """Monitora e responde mensagens"""
        print("\n🔄 Monitorando mensagens...")
        print("=" * 50)
        
        try:
            while True:
                try:
                    # Procurar por chats (conversas)
                    chat_elements = self.driver.find_elements(
                        By.XPATH, 
                        "//div[@role='listitem']"
                    )
                    
                    for chat in chat_elements:
                        try:
                            # Clique no chat
                            chat.click()
                            time.sleep(0.5)
                            
                            # Procurar mensagens
                            msg_elements = self.driver.find_elements(
                                By.XPATH,
                                "//div[@data-testid='msg-container']//span[@class='selectable-text copyable-text']"
                            )
                            
                            if msg_elements:
                                ultima_msg = msg_elements[-1]
                                texto_msg = ultima_msg.text
                                msg_id = hash(texto_msg)  # ID única da mensagem
                                
                                # Verificar se já foi processada
                                if texto_msg and len(texto_msg) > 2 and msg_id not in self.processed_messages:
                                    self.processed_messages.add(msg_id)
                                    
                                    print(f"\n📨 Mensagem recebida: {texto_msg}")
                                    
                                    # Gerar resposta com Groq
                                    resposta = self.gerar_resposta(texto_msg)
                                    
                                    # Delay aleatório (para parecer humano)
                                    time.sleep(random.randint(1, 3))
                                    
                                    # Enviar resposta
                                    if self.enviar_mensagem(resposta):
                                        print(f"✅ Resposta enviada: {resposta}\n")
                                    
                                    time.sleep(1)
                        
                        except Exception as e:
                            continue
                    
                    time.sleep(5)
                    
                except Exception as e:
                    print(f"⚠️  Erro: {e}")
                    time.sleep(5)
        
        except KeyboardInterrupt:
            print("\n\n👋 Bot encerrado pelo usuário")
            self.driver.quit()
    
    def gerar_resposta(self, mensagem):
        """Gera resposta usando Groq"""
        try:
            print("🤔 Gerando resposta com IA...")
            
            resposta = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": mensagem}
                ],
                temperature=0.7,
                max_tokens=150
            )
            
            return resposta.choices[0].message.content
        
        except Exception as e:
            print(f"❌ Erro ao gerar resposta: {e}")
            return "Desculpe, tive um problema. Tente novamente."
    
    def enviar_mensagem(self, mensagem):
        """Envia mensagem no WhatsApp"""
        try:
            # Procurar campo de texto
            input_field = self.driver.find_element(
                By.XPATH,
                "//div[@contenteditable='true'][@data-tab='10']"
            )
            
            # Digitar mensagem
            input_field.send_keys(mensagem)
            time.sleep(0.3)
            
            # Enviar (Enter)
            input_field.send_keys(Keys.RETURN)
            
            return True
            
        except Exception as e:
            print(f"❌ Erro ao enviar mensagem: {e}")
            return False
    
    def encerrar(self):
        """Encerra o navegador"""
        if self.driver:
            self.driver.quit()
            print("✅ Navegador fechado")

def main():
    bot = WhatsAppBot()
    
    try:
        if bot.iniciar():
            bot.processar_mensagens()
    except KeyboardInterrupt:
        print("\n👋 Encerrando...")
    finally:
        bot.encerrar()

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🤖 BOT WHATSAPP WEB COM IA GROQ - 100% GRÁTIS")
    print("="*60)
    print("\n✅ Certifique-se que:")
    print("   - Chrome está instalado")
    print("   - bot.py (API) está rodando em outro terminal")
    print("   - Sua chave Groq está em .env\n")
    
    main()
