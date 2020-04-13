from argparse import ArgumentParser

from enum import Enum


class PokeMode(Enum):
    POKEMON = "pokemon"

    ABILITY = "ability"

    MOVE = "move"


class Req:

    def __init__(self):
        self._current_mode = None

        self._inp_query = None

        self._inp = None

        self._expansion = None

        self._out = None

    @property
    def mode(self):
        return self._current_mode

    @mode.setter
    def mode(self, mode):
        self._current_mode = mode

    @property
    def output(self):
        return self._out

    @property
    def is_expanded(self):
        return self._expansion

    @property
    def query(self):
        return self._inp_query

    @property
    def input(self):
        return self._inp

    def __str__(self):
        return f"String: {self._inp_query}\n" \
               f"Input file: {self._inp}\n" \
               f"Is Expanded: {self._expansion}\n" \
               f"Output: {self._out}\n"


def set_the_cli_req() -> Req:
    Added_parser = ArgumentParser()

    Added_parser.add_argument("mode", help="Mode of the Pokedex.")

    Added_parser.add_argument("-q", "--query", help="Input only id or name ")

    Added_parser.add_argument("-i", "--input", help="The .txt file that needs to be queried against PokeAPI.")

    Added_parser.add_argument("-e", "--expanded", default="false", help="Check for the  subqueries  "
                                                                        "on expandable attributes.")

    Added_parser.add_argument("-o", "--output", default="print", help="Output.  Setup to print "
                                                                      "can be changed to a txt file")

    try:

        arguments = Added_parser.parse_args()

        print(f"args: {arguments}")

        cli_req = Req()

        print(f"Pokemode: {PokeMode(arguments.mode)}")

        cli_req._current_mode = PokeMode(arguments.mode)

        print(f"cli request mode: {cli_req._current_mode}")

        cli_req._inp_query = arguments.query

        cli_req._inp = arguments.input

        cli_req._expansion = arguments.expanded

        cli_req._out = arguments.output

        return cli_req

    except Exception as e:

        print(f"Invalid arguments cannot read arguments\n{e}")

        quit()


def main(req: Req):
    print(req)


if __name__ == "__main__":
    request = set_the_cli_req()

    main(request)
