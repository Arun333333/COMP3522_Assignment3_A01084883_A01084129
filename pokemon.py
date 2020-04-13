class Pokemon:
    """
    pokemon class
    """

    def __init__(self, name=None, id_=None, height=None, weight=None,
                 stats=None, types=None, abilities=None, moves=None):

        """
        Initializes a pokemon
        """
        self._name = name

        self._id = id_

        self._height = height

        self._weight = weight

        self._stats = stats

        self._types = types

        self._abilities = abilities

        self._moves = moves

    @property
    def stats(self):

        return self._stats

    @property
    def abilities(self):

        return self._abilities

    @property
    def moves(self):

        return self._moves

    def __str__(self):
        """
           :return String
        """
        types = [type["type"]["name"] for type in self._types]

        moves = ""

        for move in self._moves:
            moves += f"{move}"

        abilities = ""

        for ability in self._abilities:
            abilities += f"{ability}"

        return f"Name: {self._name.title()}\n" \
               f"ID: {self._id}\n" \
               f"Height: {self._height} decimeters\n" \
               f"Weight: {self._weight} hectograms\n\n" \
               f"Stats: \n{self._stats}\n" \
               f"Type(s): \n{'/'.join(types)}\n\n" \
               f"Ability(s): \n{abilities}\n" \
               f"Move(s): \n{moves}\n"


class Stats:
    """
    contains info on stats
    """

    def __init__(self, speed=None, sp_def=None, sp_atk=None, defense=None,
                 attack=None, hp=None):
        """
       Initializer for stat

        """
        self._speed = speed

        self._sp_def = sp_def

        self._sp_atk = sp_atk

        self._defense = defense

        self._attack = attack

        self._hp = hp

    def __str__(self):
        """
        :return: String
        """
        return f"{self._speed}\n" \
               f"{self._sp_def}\n" \
               f"{self._sp_atk}\n" \
               f"{self._defense}\n" \
               f"{self._attack}\n" \
               f"{self._hp}\n"


class BaseStats:
    """
    BaseStats class
    """

    def __init__(self, name=None, base_stat=None, url=None, id_=None, is_battle_only=None):
        """
        Initializer
        """
        self._name = name

        self._base_stat = base_stat

        self._url = url

        self._id = id_

        self._is_battle_only = is_battle_only

    def __str__(self):
        return f"{self._name} : " \
               f"{self._base_stat}\n" \
               f"ID: {self._id}\n" \
               f"Is battle only: {self._is_battle_only}\n"


class Move:
    """
    accounts for move of a pokemon
    """

    def __init__(self, name=None, id_=None, generation=None, accuracy=None, pp=None, power=None, type_=None,
                 damage_class=None, effect_short=None, url=None, level=None):
        """
        Initializer for move
        """

        self._name = name
        self._id = id_
        self._generation = generation
        self._accuracy = accuracy
        self._pp = pp
        self._power = power
        self._type = type_
        self._damage_class = damage_class
        self._effect_short = effect_short
        self._url = url
        self._level = level

    def __str__(self):

        return f"Move: {self._name} " \
               f"(Level learned at: {self._level}) " \
               f"(URL: {self._url})\n"


class Ability:
    """
     Attr pokemon ability
    """

    def __init__(self, name=None, id_=None, generation=None, effect=None, effect_short=None, pokemon=None, url=None):

        self._name = name

        self._url = url

        self._id = id_

        self._generation = generation

        self._effect = effect

        self._effect_short = effect_short

        self._pokemon = pokemon

    def __str__(self):

        return f"{self._name} " \
               f"({self._url})\n"
