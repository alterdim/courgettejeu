import random
import json
import matplotlib.pyplot as plt

def charger_cartes(chemin_fichier):
    with open(chemin_fichier, 'r') as f:
        return json.load(f)

def piocher_cartes(cartes, n):
    # Si n est plus grand que le nombre de cartes disponibles, prendre toutes les cartes disponibles
    return random.sample(cartes, min(n, len(cartes)))

def verifier_satisfaction(client, ressources_disponibles):
    # Vérifier si nous avons suffisamment de ressources pour satisfaire la demande du client
    if len(ressources_disponibles) >= len(client["demande"]):
        return True
    return False

def repartition_ressources(ressources_piochées, clients_piochés):
    # Répartir les ressources entre les clients
    ressources_disponibles = []
    for carte in ressources_piochées:
        ressources_disponibles.extend(carte["ressources"])
    
    clients_satisfaits = 0
    for client in clients_piochés:
        if verifier_satisfaction(client, ressources_disponibles):
            # Allouer les ressources au client en les retirant de la liste des ressources disponibles
            for _ in range(len(client["demande"])):
                ressources_disponibles.pop()
            clients_satisfaits += 1

    return clients_satisfaits

def simuler_tour(ressources, clients, X, Y):
    ressources_piochées = piocher_cartes(ressources, X)
    clients_piochés = piocher_cartes(clients, Y)

    clients_satisfaits = repartition_ressources(ressources_piochées, clients_piochés)
    
    if Y > 0:
        pourcentage_satisfaction = (clients_satisfaits / Y) * 100
    else:
        pourcentage_satisfaction = 0
    return pourcentage_satisfaction

def simulation_multiples(ressources, clients, max_X, max_Y, repetitions=100):
    satisfaction = []
    
    for X in range(min_X, max_X + 1):  # Assurez-vous d'itérer sur toutes les valeurs de 1 à max_X
        ligne = []
        for Y in range(min_Y, max_Y + 1):  # Assurez-vous d'itérer sur toutes les valeurs de 1 à max_Y
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
min_X = int(input("Nombre minimal de ressources ?\n"))
min_Y = int(input("Nombre minimal de clients ?\n"))
max_X = int(input("Nombre maximal de ressources ?\n"))
max_Y = int(input("Nombre maximal de clients ?\n"))

if (min_X > max_X or min_Y > max_Y):
    print("oulah ça va merder")

# Effectuer la simulation
satisfaction = simulation_multiples(ressources, clients, max_X, max_Y, repetitions=100)

# Affichage du graphiques
X_values = list(range(min_X, max_X + 1))  # 1 à max_X
Y_values = list(range(min_Y, max_Y + 1))  # 1 à max_Y

plt.figure(figsize=(10, 6))
for i, X in enumerate(X_values):
    plt.plot(Y_values, satisfaction[i], label=f'{X} ressources')

plt.title("Satisfaction des clients en fonction du nombre de ressources et de clients piochés")
plt.xlabel("Nombre de clients piochés (Y)")
plt.ylabel("Pourcentage de satisfaction (%)")
plt.legend(title="Ressources piochées (X)")
plt.grid(True)
plt.show()
