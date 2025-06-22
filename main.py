import requests
import time
import os

# Pegando dados das variáveis de ambiente
API_KEY = os.getenv('API_KEY')
TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

ligas_favoritas = [39, 140, 135]  # Premier League, La Liga, Serie A

def enviar_sinal(mensagem):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {'chat_id': CHAT_ID, 'text': mensagem}
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print("✅ Sinal enviado com sucesso!")
    else:
        print("❌ Erro ao enviar sinal:", response.text)

def buscar_estatisticas(fixture_id):
    url = f'https://v3.football.api-sports.io/fixtures/statistics?fixture={fixture_id}'
    headers = {'x-apisports-key': API_KEY}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        stats = response.json().get('response', [])
        escanteios = 0
        finalizacoes = 0
        ataques_perigosos = 0
        
        for equipe in stats:
            for estat in equipe['statistics']:
                if estat['type'] == 'Corner Kicks':
                    escanteios += estat['value'] or 0
                elif estat['type'] == 'Shots on Goal':
                    finalizacoes += estat['value'] or 0
                elif estat['type'] == 'Attacks':
                    ataques_perigosos += estat['value'] or 0
                    
        return escanteios, finalizacoes, ataques_perigosos
    else:
        print("Erro ao buscar estatísticas:", response.text)
        return 0, 0, 0

def checar_jogos_escanteios():
    url = 'https://v3.football.api-sports.io/fixtures?live=all'
    headers = {'x-apisports-key': API_KEY}

    try:
        response = requests.get(url, headers=headers)
        jogos = response.json().get('response', [])

        print(f"📊 Verificando {len(jogos)} jogos ao vivo...")

        for jogo in jogos:
            minuto = jogo['fixture']['status']['elapsed']
            liga_id = jogo['league']['id']
            fixture_id = jogo['fixture']['id']
            time_a = jogo['teams']['home']['name']
            time_b = jogo['teams']['away']['name']

            if liga_id in ligas_favoritas and 7 <= minuto <= 9:
                escanteios, finalizacoes, ataques_perigosos = buscar_estatisticas(fixture_id)
                print(f"{time_a} x {time_b} - {escanteios} escanteios, {finalizacoes} finalizações, {ataques_perigosos} ataques perigosos aos {minuto} min")
                
                if escanteios <= 2 and finalizacoes >= 2 and ataques_perigosos >= 8:
                    link_bet365 = f"https://www.bet365.com/#/AC/B1/C1/D1/E{fixture_id}/"
                    mensagem = f"🚩 Escanteios e Pressão!\n{time_a} x {time_b}\n🕒 {minuto} min\n📊 Escanteios: {escanteios} | Finalizações: {finalizacoes} | Ataques Perigosos: {ataques_perigosos}\n🎯 Veja o jogo ao vivo na Bet365: {link_bet365}"
                    enviar_sinal(mensagem)

    except Exception as e:
        print("Erro ao processar jogos:", e)

while True:
    checar_jogos_escanteios()
    time.sleep(300)

