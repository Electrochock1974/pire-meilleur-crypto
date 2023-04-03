#Pour installer les librarie ouvrez un terminal ou sur virtual studio code
#et faites ctrl+ù tapez ensuite les commandes suivantes:
#pip install requests
#json et os sont déjà inclus dans python.
#pour lancer le script faite la commande : 
#python script.py
#/!\ il est important que le fichier script.py sois dans un dossier pour
#plus de simplicité.
#/!\ tout les fichier sont supprimé si vous relancer le script.


import requests
import os
import json
import glob

# Supprimer le fichier data.json s'il existe
if os.path.exists('data.json'):
    os.remove('data.json')

# Supprimer tous les fichiers qui commencent par "top_5_crypto_" et se terminent par ".txt"
for file in glob.glob("top_5_crypto_*.txt"):
    os.remove(file)

# Supprimer les dossiers top_gainers et top_losers s'ils existent
if os.path.exists("top_gainers"):
    os.system("rmdir /s /q top_gainers")
if os.path.exists("top_losers"):
    os.system("rmdir /s /q top_losers")

# Durées disponibles
durees_disponibles = {'1h': 'priceChange1h',
                      '24h': 'priceChange24h',
                      '7d': 'priceChange7d',
                      '30d': 'priceChange30d'}

# Durée par défaut
duree_par_defaut = '7d'

# Demander la durée à l'utilisateur
print(f"Veuillez choisir la durée pour le classement (parmi {', '.join(durees_disponibles.keys())}, par défaut {duree_par_defaut}): ")
duree = input().strip()

# Vérifier si la durée est valide, sinon utiliser la durée par défaut
if duree not in durees_disponibles:
    print(f"Pas de durée valide selectionné. La durée de {duree_par_defaut} à été utilisé.")
    duree = duree_par_defaut

# Obtenir les données JSON de l'API CoinMarketCap
url = f'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/spotlight?dataType=2&limit=30&rankRange=100&timeframe={duree}'
response = requests.get(url)
data = response.json()

# Écrire les données JSON dans un fichier
with open('data.json', 'w') as f:
    json.dump(data, f, indent=2)

# Récupérer les données depuis le fichier JSON
with open('data.json', 'r') as f:
    data = json.load(f)

# Récupérer les 5 meilleures cryptos pour la durée demandée
gainers = sorted([item for item in data['data']['gainerList'] if item.get('priceChange', {}).get(durees_disponibles[duree]) is not None], key=lambda x: x['priceChange'][durees_disponibles[duree]], reverse=True)[:5]

# Récupérer les 5 pires cryptos pour la durée demandée
losers = sorted([item for item in data['data']['loserList'] if item.get('priceChange', {}).get(durees_disponibles[duree]) is not None], key=lambda x: x['priceChange'][durees_disponibles[duree]])[:5]

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


# Créer le fichier texte avec le classement pour la durée sélectionnée
if duree == '1h':
    timeframe_text = '1 heure'
    time_key = 'priceChange1h'
elif duree == '24h':
    timeframe_text = '24 heures'
    time_key = 'priceChange24h'
elif duree == '7d':
    timeframe_text = '7 jours'
    time_key = 'priceChange7d'
else:
    timeframe_text = '30 jours'
    time_key = 'priceChange30d'

with open(f'top_5_crypto_{duree}.txt', 'w', encoding='utf-8') as f:
    f.write(f"Les 5 meilleures cryptos pour la durée de {timeframe_text} :\n")
    for i, crypto in enumerate(gainers):
        rank = i + 1
        f.write(f"{rank}. [{crypto['id']}.png] {crypto['name']} ({crypto['symbol']}): {crypto['priceChange'][time_key]}% de gain\n")

    f.write(f"\nLes 5 pires cryptos pour la durée de {timeframe_text} :\n")
    for i, crypto in enumerate(losers):
        rank = i + 1
        f.write(f"{rank}. [{crypto['id']}.png] {crypto['name']} ({crypto['symbol']}): {crypto['priceChange'][time_key]}% de perte\n")
