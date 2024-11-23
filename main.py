import random
import json

def charger_cartes(chemin_fichier):
    with open(chemin_fichier, 'r') as f:
        return json.load(f)

def piocher_cartes(cartes, n):
    return random.sample(cartes, n)

def verifier_satisfaction(client, ressources_piochées):
    # Vérifier si toutes les ressources demandées par le client sont présentes dans les ressources piochées
    return all(ressource in ressources_piochées for ressource in client["demande"])

def calculer_satisfaction(ressources_piochées, clients_piochés):
    clients_satisfaits = 0
    for client in clients_piochés:
        if verifier_satisfaction(client, ressources_piochées):
            clients_satisfaits += 1
    return clients_satisfaits

def simuler_tour(ressources, clients, X, Y):
    ressources_piochées = piocher_cartes(ressources, X)
    clients_piochés = piocher_cartes(clients, Y)

    clients_satisfaits = calculer_satisfaction(ressources_piochées, clients_piochés)
    
    pourcentage_satisfaction = (clients_satisfaits / Y) * 100
    return pourcentage_satisfaction, clients_satisfaits, len(clients_piochés)

# Charger les cartes depuis les fichiers JSON
ressources = charger_cartes('ressources.json')
clients = charger_cartes('clients.json')

# Paramètres de la simulation
X = 3  # Nombre de ressources piochées
Y = 3  # Nombre de clients piochés

# Simuler un tour
pourcentage_satisfaction, clients_satisfaits, clients_total = simuler_tour(ressources, clients, X, Y)

print(f"Pourcentage de clients satisfaits: {pourcentage_satisfaction}%")
print(f"Nombre de clients satisfaits: {clients_satisfaits} sur {clients_total}")
