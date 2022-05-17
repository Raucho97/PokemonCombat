import pickle
from requests_html import HTMLSession

# Creamos una biblioteca donde guardaremos los datos de los pokemons obtenidos de la web
pokemon_base = {
    "name": "",
    "current_health": 100,
    "base_health": 100,
    "level": 1,
    "type": None,
    "current_exp": 0
}

URL_BASE = "https://pokexperto.net/index2.php?seccion=nds/nationaldex/movimientos_nivel&pk="


# Función para entrar en la web y coger los datos de los pokemos de esta
def get_pokemon(index):
    url = "{}{}".format(URL_BASE, index)
    session = HTMLSession()

    new_pokemon = pokemon_base.copy()
    pokemon_page = session.get(url)

    # Obtenemos el nombre del pokemón
    new_pokemon["name"] = pokemon_page.html.find(".mini", first=True).text

    # Obtenemos el tipo del pokemon
    new_pokemon["type"] = []

    for img in pokemon_page.html.find(".pkmain", first=True).find(".bordeambos", first=True).find("img"):
        new_pokemon["type"].append(img.attrs["alt"])

    # Obtener ataques de pokemons
    new_pokemon["attacks"] = []

    for attack_item in pokemon_page.html.find(".pkmain")[-1].find("tr .check3"):
        attack = {
            "name": attack_item.find("td", first=True).find("a", first=True).text,
            "type": attack_item.find("td")[1].find("img", first=True).attrs["alt"],
            "min_lvl": attack_item.find("th", first=True).text,
            "damage": int(attack_item.find("td")[3].text.replace("--", "0"))
        }
        new_pokemon["attacks"].append(attack)

    return new_pokemon


# Leeemos todos los pokemons de la web o del archivo guardado
def get_all_pokemons():
    all_pokemons = []
    try:
        print("Cargando el archivo de pokemons...")
        #Si ya hemos creado pokefile anteriormente, lo cargamos en vez de leer la web
        with open("pokefile.pkl", "rb") as pokefile:
           all_pokemons = pickle.load(pokefile)

    except FileNotFoundError:
        print("Archivo no encontrado. Cargando de internet...")
        for index in range(151):
            all_pokemons.append(get_pokemon(index+1))
            print("*", end="")

        # Guardamos los pokemons en un archivo para no tener q leer de la web siempre
        with open("pokefile.pkl", "wb") as pokefile:
            pickle.dump(all_pokemons, pokefile)
            print("\n Todos los pokemons han dido descargados")

    print("Lista de pokemons cargada")
    return all_pokemons


