from poke_load import get_all_pokemons
import random


def get_player_profile(pokemon_list):  # Creamos el perfil del jugador tomando 3 pokemons aleatorios de la lista
    return {
        "player_name": input("¿Cuál es tu nombre?"),
        "pokemon_inventory": [random.choice(pokemon_list) for a in range(3)],
        "combats": 0,
        "pokeballs": 0,
        "health_potion": 0,
    }


def any_player_pokemon_lives(player_profile):  # Comprobamos que la suma de las vidas de nuestros pokemons es >0
    return sum([pokemon["current_health"] for pokemon in player_profile["pokemon_inventory"]]) > 0


def choose_pokemon(player_profile):
    chosen = None
    while not chosen:
        for index in range(len(player_profile["pokemon_inventory"])):
            print("{} - {}".format(index, get_pokemon_info(player_profile["pokemon_inventory"][index])))
        try:
            return player_profile["pokemon_inventory"][int(input("¿Qué pokemon eliges?(0/1/2) "))]
        except (ValueError, IndexError):
            print("Debes elegir entre entre 0, 1 o 2")



def get_pokemon_info(pokemon):
    return "{} | LVL {} | HP {}/{}".format(pokemon["name"],
                                           pokemon["level"],
                                           pokemon["current_health"],
                                           pokemon["base_health"])

def player_attack(player_pokemon, wild_pokemon):
    print("Es tu turno\n")
    print("Elige un ataque")



def wild_attack(wild_pokemon, player_pokemon):
    pass


def assign_experience(attack_history):
    for pokemon in attack_history:
        points = random.randint(1, 5)
        pokemon["current_exp"] += points

        while pokemon["current_exp"] > 20:
            pokemon["current_exp"] -= 20
            pokemon["level"] += 1
            pokemon["current_health"] = pokemon["base_health"]
            print("Tu pokemon ha subido al nivel {}".format(get_pokemon_info(pokemon)))


def fight(player_profile, wild_pokemon):
    print("----NUEVO COMBATE----")

    player_pokemon = choose_pokemon(player_profile)
    print("{}   VS   {}".format(get_pokemon_info(player_pokemon),
                                get_pokemon_info(wild_pokemon)))
    attack_history = []

    while any_player_pokemon_lives(player_profile) and wild_pokemon["current_health"] > 0:
        action = None
        while action not in ["A", "P", "R", "C"]:
            action = input("[A]tacar | [P]okeball | [C]urar | [R]elevo")
        if action == "A":
            player_attack(player_pokemon, wild_pokemon)
            attack_history.append(player_pokemon)

        elif action == "C":
            ##cure_pokemon(player_profile, player_pokemon)
            pass

        elif action == "P":
           ##capture_wild_pokemon(wild_pokemon, player_profile)
            pass

        elif action == "R":
            player_pokemon = choose_pokemon(player_profile)

        wild_attack(wild_pokemon, player_pokemon)

        if player_pokemon["current_health"] == 0 and any_player_pokemon_lives(player_profile):
            player_pokemon = choose_pokemon(player_profile)

    if wild_pokemon["current_health"] == 0:
        print("Has ganado!!")
        assign_experience(attack_history)

    print("----COMBATE TERMINADO----")
    input("Press ENTER to continue")


##def item_lottery(player_profile):


def main():
    pokemon_list = get_all_pokemons()
    player_profile = get_player_profile(pokemon_list)

    while any_player_pokemon_lives(player_profile):  # Luchamos contra pokemons aleatorios mientras alguno de nuestros
        wild_pokemon = random.choice(pokemon_list)   # pokemons tenga vida
        fight(player_profile, wild_pokemon)
        #item_lottery(player_profile)

    print("Has perdido en el {}".format(player_profile["combats"]) + "º combate")


if __name__ == '__main__':
    main()

