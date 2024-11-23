import random
import json
import matplotlib.pyplot as plt

def charger_cartes(chemin_fichier):
    with open(chemin_fichier, 'r') as f:
        return json.load(f)

def piocher_cartes(cartes, n):
    # Si n est plus grand que le nombre de cartes disponibles, prendre toutes les cartes disponibles
    return random.sample(cartes, min(n, len(cartes)))

def verifier_satisfaction(client, ressources_piochées):
    # Compter le nombre total de ressources disponibles dans les cartes piochées
    ressources_disponibles = sum(len(carte["ressources"]) for carte in ressources_piochées)
    
    # Vérifier si le nombre total de ressources piochées est suffisant pour satisfaire la demande
    return ressources_disponibles >= len(client["demande"])

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
    
    if Y > 0:
        pourcentage_satisfaction = (clients_satisfaits / Y) * 100
    else:
        pourcentage_satisfaction = 0
    return pourcentage_satisfaction

def simulation_multiples(ressources, clients, max_X, max_Y, repetitions=100):
    satisfaction = []
    
    for X in range(1, max_X + 1):  # Assurez-vous d'itérer sur toutes les valeurs de 1 à max_X
        ligne = []
        for Y in range(1, max_Y + 1):  # Assurez-vous d'itérer sur toutes les valeurs de 1 à max_Y
            satisfaction_pourcentage = []
            for _ in range(repetitions):  # Nombre de simulations pour chaque combinaison
                satisfaction_pourcentage.append(simuler_tour(ressources, clients, X, Y))
            moyenne_satisfaction = sum(satisfaction_pourcentage) / len(satisfaction_pourcentage)
            ligne.append(moyenne_satisfaction)
        satisfaction.append(ligne)
    
    return satisfaction

# Charger les cartes depuis les fichiers JSON
ressources = charger_cartes('ressources.json')
clients = charger_cartes('clients.json')

# Paramètres de la simulation
max_X = 6  # Le nombre maximal de ressources piochées
max_Y = 6  # Le nombre maximal de clients piochés

# Effectuer la simulation
satisfaction = simulation_multiples(ressources, clients, max_X, max_Y, repetitions=100)

# Affichage du graphique
X_values = list(range(1, max_X + 1))  # 1 à max_X
Y_values = list(range(1, max_Y + 1))  # 1 à max_Y

plt.figure(figsize=(10, 6))
for i, X in enumerate(X_values):
    plt.plot(Y_values, satisfaction[i], label=f'{X} ressources')

plt.title("Satisfaction des clients en fonction du nombre de ressources et de clients piochés")
plt.xlabel("Nombre de clients piochés (Y)")
plt.ylabel("Pourcentage de satisfaction (%)")
plt.legend(title="Ressources piochées (X)")
plt.grid(True)
plt.show()
