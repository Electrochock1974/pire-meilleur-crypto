import requests
import os
import json
import os

# Supprimer le fichier data.json s'il existe
if os.path.exists('data.json'):
    os.remove('data.json')

# Supprimer le fichier top_5_crypto.txt s'il existe
if os.path.exists('top_5_crypto.txt'):
    os.remove('top_5_crypto.txt')

# Supprimer les dossiers top_gainers et top_losers s'ils existent
if os.path.exists("top_gainers"):
    os.system("rmdir /s /q top_gainers")
if os.path.exists("top_losers"):
    os.system("rmdir /s /q top_losers")



# Obtenir les données JSON de l'API CoinMarketCap
url = 'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/spotlight?dataType=2&limit=30&rankRange=100&timeframe=7d'
response = requests.get(url)
data = response.json()

# Écrire les données JSON dans un fichier
with open('data.json', 'w') as f:
    json.dump(data, f, indent=2)

# Récupérer les données depuis le fichier JSON
with open('data.json', 'r') as f:
    data = json.load(f)

# Récupérer les 5 meilleures cryptos pour la durée de 7 jours
gainers = sorted([item for item in data['data']['gainerList'] if item.get('priceChange', {}).get('priceChange7d') is not None], key=lambda x: x['priceChange']['priceChange7d'], reverse=True)[:5]

# Récupérer les 5 pires cryptos pour la durée de 7 jours
losers = sorted([item for item in data['data']['loserList'] if item.get('priceChange', {}).get('priceChange7d') is not None], key=lambda x: x['priceChange']['priceChange7d'])[:5]

# Créer les dossiers d'images s'ils n'existent pas
if not os.path.exists("top_gainers"):
    os.makedirs("top_gainers")
if not os.path.exists("top_losers"):
    os.makedirs("top_losers")

# Télécharger les images pour les 5 meilleures cryptos
for crypto in gainers:
    img_url = f"https://s2.coinmarketcap.com/static/img/coins/128x128/{crypto['id']}.png"
    img_data = requests.get(img_url).content
    with open(f"top_gainers/{crypto['id']}.png", 'wb') as f:
        f.write(img_data)

# Télécharger les images pour les 5 pires cryptos
for crypto in losers:
    img_url = f"https://s2.coinmarketcap.com/static/img/coins/128x128/{crypto['id']}.png"
    img_data = requests.get(img_url).content
    with open(f"top_losers/{crypto['id']}.png", 'wb') as f:
        f.write(img_data)

# Créer le fichier texte avec le classement pour les 7 jours
with open('top_5_crypto.txt', 'w', encoding='utf-8') as f:
    f.write("Les 5 meilleures cryptos pour la durée de 7 jours :\n")
    for i, crypto in enumerate(gainers):
        rank = i + 1
        f.write(f"{rank}. [{crypto['id']}] {crypto['name']} ({crypto['symbol']}): {crypto['priceChange']['priceChange7d']}% de gain\n")

    f.write("\nLes 5 pires cryptos pour la durée de 7 jours :\n")
    for i, crypto in enumerate(losers):
        rank = i + 1
        f.write(f"{rank}. [{crypto['id']}] {crypto['name']} ({crypto['symbol']}): {crypto['priceChange']['priceChange7d']}% de perte\n")
