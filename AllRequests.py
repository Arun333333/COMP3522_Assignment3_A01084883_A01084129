from enum import Enum

import apihandling

import pokemon as p

from abc import ABC, abstractmethod

from argparse import ArgumentParser


class pokemondexmode(Enum):

    POKEMON = "pokemon"

    ABILITY = "ability"

    MOVE = "move"


class Req:
    """
    Handles user req for POKE API
    """

    def __init__(self):
        self.mode = None
        self.string = None
        self.is_expanded = False
        self.output_path = None
        self.search_terms = []
        self.json = []
        self.sub_json = []
        self.subquery_urls = []
        self.results = []
        self.stat_urls = []
        self.ability_urls = []
        self.move_urls = []

    def __str__(self):
        return f"mode: {self.mode}\n" \
               f"String: {self.string}\n" \
               f"Is Expanded: {self.is_expanded}\n" \
               f"Output Path: {self.output_path}\n" \
               f"Search terms: {self.search_terms}\n" \
               f"Results: {self.results}\n"


class ReqHandle:
    """
    handles cmd args
    """

    @staticmethod
    def set_the_cli_req() -> Req:
        argparser = ArgumentParser()

        argparser.add_argument("mode", help="Wrong Mode Can be Pokemon, Ability, or MOve")

        argparser.add_argument("string", type=str.lower, help="The search input. only Pokemon id, name "
                                                              "or text file path")
        argparser.add_argument("-e", "--expanded", action="store_true",
                               help="to check if subqueries are performed "
                                    ".  By default "
                                    "set to false.")
        argparser.add_argument("-o", "--output", default="print", help="Set to print"
                                                                       "by def can be a text file")
        try:
            args = argparser.parse_args()
            print(f"args: {args.__dict__}")
            cli_req = Req()
            cli_req.mode = pokemondexmode(args.mode.lower())
            cli_req.string = args.string.replace(' ', '-')
            cli_req.is_expanded = args.expanded
            cli_req.output_path = args.output
            return cli_req
        except Exception as err:
            print(f"ERROR cant read args.\n{err}")
            quit()


class baseHandler(ABC):
    """
    Abstract base handler
    """

    def __init__(self, next_handler=None) -> None:
        self._next_handler = next_handler

    @abstractmethod
    def handle_request(self, request_: Req) -> None:
        """
        cmd line req is handled

        """
        pass

    @property
    def next_handler(self):
        """
         checks for the next handler
        """
        return self._next_handler

    @next_handler.setter
    def next_handler(self, next_handler):
        """
        calls the next handler
        """
        self._next_handler = next_handler


class ExtensionHandler(baseHandler):

    async def handle_request(self, request_: Req) -> None:

        if request_.string.endswith(".txt"):

            with open(request_.string, 'r') as file:

                request_.search_terms = list(file)

                request_.search_terms = [

                    term.strip('\n ').lower().replace(' ', '-')

                    for term in request_.search_terms]
        else:

            request_.search_terms.append(request_.string)

        if self.next_handler is None:
            return

        return await self.next_handler.handle_request(request_)


class HttpHandler(baseHandler):
    async def handle_request(self, request_: Req) -> None:

        some = apihandling.managingAPI()
        if len(request_.stat_urls) < 1:

            request_.json = await some.open_session(request_)

            request_.json = [json for json in request_.json if
                             json is not None]
        else:

            request_.sub_json = await some.open_session(request_)

            request_.sub_json = [json for json in request_.json if
                                 json is not None]

        if self.next_handler is None:
            return
        return await self.next_handler.handle_request(request_)


class SubqueryHandler(baseHandler):

    async def handle_request(self, request_: Req) -> None:

        abilities = []
        moves = []
        stats = []

        for pok_json in request_.json:
            for i in range(len(pok_json['stats'])):
                stats.append(pok_json['stats'][i]['stat'][
                                'url'])

            for a in pok_json['abilities']:
                abilities.append(a['ability']['url'])

            for i in range(len(pok_json['moves'])):
                moves.append(pok_json['moves'][i]['move']['url'])

            request_.stat_urls.append(stats)
            request_.ability_urls.append(abilities)
            request_.move_urls.append(moves)

            # Reset for the next Pokemon
            stats = []
            moves = []
            abilities = []
            one_pokemon_urls = []

        if self.next_handler is None:
            return
        return await self.next_handler.handle_request(request_)


class JsonHandler(baseHandler):

    def __init__(self):
        super().__init__()
        self._mode_dict = {
            pokemondexmode.POKEMON: self.get_pokemon,
            pokemondexmode.ABILITY: self.get_ability,
            pokemondexmode.MOVE: self.get_move
        }

    def handle_request(self, request_: Req) -> None:
        """
        Convert  JSON  objects and appending

        """
        self._mode_dict.get(request_.mode)(request_)
        if self.next_handler is None:
            return
        return self.next_handler.handle_request(request_)

    def get_pokemon(self, request_: Req) -> None:
        """
        Converts JSON

        """
        for json in request_.json:
            # Create stats object
            base_list = []

            for some in json["stats"]:

                name = some["stat"]["name"]

                base_stats = some["base_stat"]

                url = some["stat"]["url"]

                base_list.append(p.BaseStats(name, base_stats, url))

            stats = p.Stats(base_list[0], base_list[1], base_list[2],

                            base_list[3], base_list[4], base_list[5])

            # Create list of Abilities
            abilities = []
            for i in range(len(json["abilities"])):
                name = json["abilities"][i]["ability"]["name"]
                url = json["abilities"][i]["ability"]["url"]
                abilities.append(p.Ability(name=name, url=url))

            # Create list of Moves
            moves = []
            for i in range(len(json["moves"])):
                name = json["moves"][i]["move"]["name"]
                level = json["moves"][i]["version_group_details"][0][
                    "level_learned_at"]
                move_url = json["moves"][i]["move"]["url"]
                moves.append(p.Move(name=name, level=level, url=move_url))

            # Create Pokemon
            pokemon = p.Pokemon(json["name"], json["id"], json["height"],
                                json["weight"], stats, json["types"],
                                abilities, moves)
            request_.results.append(pokemon)

    def get_ability(self, request_: Req) -> None:
        """
        gives Ability object

        """
        for j in request_.json:
            ability = p.Ability(j["name"], j["id"],
                                j["generation"],
                                j["effect_entries"][0]["effect"],
                                j["effect_entries"][0]["short_effect"],
                                j["pokemon"])
            request_.results.append(ability)

    def get_move(self, request_: Req) -> None:
        """
        gives Move object

        """
        for j in request_.json:
            move = p.Move(j["name"], j["id"], j["generation"]["name"],
                          j["accuracy"], j["pp"], j["power"],
                          j["type"], j["damage_class"],
                          j["effect_entries"][0]["short_effect"])
            request_.results.append(move)


class JsonQueryHandler(baseHandler):

    def handle_request(self, request_: Req) -> None:
        """
        Converts  JSON  and append to results.

        """
        print(request_.json[0][0][0])

        # Create stats object
        for pok in request_.sub_json[0]:
            for stat in pok:
                name = stat['name']


class OutcomeHandler(baseHandler):

    def handle_request(self, request_: Req) -> None:

        if request_.output_path.lower() == "print":

            for res in request_.results:
                print(res)

            if not request_.results:
                raise Exception

        elif request_.output_path.endswith(".txt"):

            with open(request_.output_path, "w+") as file:

                for result in request_.results:
                    file.write(result.__str__())
        else:
            raise FileNotFoundError(request_.output_path)


def main(request: Req):
    print(request)


if __name__ == "__main__":
    request = ReqHandle.set_the_cli_req()
    main(request)
