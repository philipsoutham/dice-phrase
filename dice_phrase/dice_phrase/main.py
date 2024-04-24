"""
This script generates secure passphrases based on the EFF's diceware word lists.
It uses a combination of random dice rolls and word selection to ensure passphrase
strength. This script supports customization of passphrase length, word separation,
inclusion of numbers, and capitalization of words.
"""

import enum
import pickle
import secrets
import typing
import importlib.resources

import typer
from rich.console import Console

_CONSOLE: typing.Final = Console(color_system="256")
# https://rich.readthedocs.io/en/latest/appendix/colors.html
_SEPARATOR_COLOR: typing.Final[str] = "bright_red"
_NUMBER_COLOR: typing.Final[str] = "turquoise2"

app = typer.Typer()


class _DicewareWordList(str, enum.Enum):
    """
    Enumeration of available word lists for generating passphrases.
    Each member corresponds to a specific themed word list, with details
    such as expected dice rolls, sides, and separators for each list.
    These themes include popular media franchises for fans to enjoy.
    """

    large = "large"  # Designed for memorability and passphrase strength, for use with five dice
    short_1 = "short-1"  # Featuring only short words, for use with four dice
    short_2 = "short-2"  # For use with four dice, featuring longer words that may be more memorable.
    # Fandom lists from: https://www.eff.org/deeplinks/2018/08/dragon-con-diceware
    star_wars = "star-wars"
    harry_potter = "harry-potter"
    star_trek = "star-trek"
    game_of_thrones = "game-of-thrones"


class _WordListSettings(typing.TypedDict):
    """
    Metadata for each word list used in passphrase generation.
    Includes the database filename, number of dice rolls, dice sides,
    and any separators used between dice rolls.
    """

    db: str  # Name of the pkl file
    rolls: int  # how many dice rolls needed to choose a word
    dice_sides: int  # how many sides does the dice have
    separator: str  # are the rolls separated by anything


_DICELIST_DETAILS: typing.Final[dict[_DicewareWordList, _WordListSettings]] = {
    _DicewareWordList.large: {
        "db": "eff_large_wordlist.pkl",
        "rolls": 5,
        "dice_sides": 6,
        "separator": "",
    },  # Designed for memorability and passphrase strength, for use with five dice
    _DicewareWordList.short_2: {
        "db": "eff_short_wordlist_1.pkl",
        "rolls": 4,
        "dice_sides": 6,
        "separator": "",
    },  # Featuring only short words, for use with four dice
    _DicewareWordList.short_1: {
        "db": "eff_short_wordlist_2_0.pkl",
        "rolls": 4,
        "dice_sides": 6,
        "separator": "",
    },  # For use with four dice, featuring longer words that may be more memorable.
    _DicewareWordList.game_of_thrones: {
        "db": "gameofthrones_8k-2018.pkl",
        "rolls": 3,
        "dice_sides": 20,
        "separator": "-",
    },  # Game of Thrones fandom list, for use with 3 rolls of 20-sided die
    _DicewareWordList.harry_potter: {
        "db": "harrypotter_8k_3column-txt.pkl",
        "rolls": 3,
        "dice_sides": 20,
        "separator": "-",
    },  # Harry potter fandom list, for use with 3 rolls of 20-sided die
    _DicewareWordList.star_trek: {
        "db": "memory-alpha_8k_2018.pkl",
        "rolls": 3,
        "dice_sides": 20,
        "separator": "-",
    },  # Star Trek fandom list, for use with 3 rolls of 20-sided die
    _DicewareWordList.star_wars: {
        "db": "starwars_8k_2018.pkl",
        "rolls": 3,
        "dice_sides": 20,
        "separator": "-",
    },  # Star Wars fandom list, for use with 3 rolls of 20-sided die
}


def _dice_throws_as_key(
    word_list: _DicewareWordList,
):
    """
    Simulate dice throws based on the configuration of the given word list.
    Constructs a dice roll result by joining random numbers up to a specified maximum value,
    according to the dice configuration for the word list.

    Args:
        word_list (_DicewareWordList): The word list enum to use for determining dice configuration.

    Returns:
        str: A string representing the concatenated results of dice throws.

    Example:
        # Assuming the following configurations in _DICELIST_DETAILS:
        # _DICELIST_DETAILS[_DicewareWordList.large] = {"rolls": 5, "dice_sides": 6, "separator": ""}
        # _DICELIST_DETAILS[_DicewareWordList.game_of_thrones] = {"rolls": 3, "dice_sides": 20, "separator": "-"}

        >>> _dice_throws_as_key(_DicewareWordList.large)
        '43652'
        >>> _dice_throws_as_key(_DicewareWordList.game_of_thrones)
        '10-20-17'
    """

    return _DICELIST_DETAILS[word_list]["separator"].join(
        _simulate_dice_rolls(
            rolls=_DICELIST_DETAILS[word_list]["rolls"],
            max_val=_DICELIST_DETAILS[word_list]["dice_sides"],
        )
    )


def _simulate_dice_rolls(rolls: int, max_val: int) -> list[str]:
    """
    Simulate a series of dice rolls.

    This function generates a list of random numbers, each representing the result of a dice roll.
    The number of rolls and the maximum value of each roll (like the number of sides on a die) are
    specified by the parameters.

    Args:
        rolls (int): The number of dice rolls to simulate.
        max_val (int): The maximum value for each roll, representing the number of sides on the die.

    Returns:
        list[str]: A list containing the result of each roll as a string.

    Example:
        >>> _simulate_dice_rolls(5, 6)
        ['4', '2', '6', '3', '5']
        >>> _simulate_dice_rolls(3, 20)
        ['10', '20', '17']
    """
    return [str(secrets.randbelow(max_val) + 1) for _ in range(rolls)]


def _create_word_list_from_dice(
    num_words: int = 6,
    word_list: _DicewareWordList = _DicewareWordList.large,
) -> list[str]:
    """
    Generate a list of diceware words based on random dice rolls.
    Args:
        num_words (int): The number of diceware words to generate.
        word_list (_DicewareWordList): Which word list to use, affects the randomness and word selection.

    Returns:
        list[str]: A list of diceware words.

    Example:
        # Assuming the word list for _DicewareWordList.large is configured for 5 rolls of a 6-sided dice
        # and the loaded word list has suitable entries:
        >>> _create_word_list_from_dice(3, _DicewareWordList.large)
        ['elephant', 'rocket', 'giraffe']

        # For a fantasy-themed word list configured for 3 rolls of a 20-sided dice:
        >>> _create_word_list_from_dice(2, _DicewareWordList.game_of_thrones)
        ['dragon', 'throne']
    """
    try:
        _dice_words: typing.Final[dict[str, str]] = pickle.loads(importlib.resources.read_binary(__package__, _DICELIST_DETAILS[word_list]["db"]))  # type: ignore
    except IOError as e:
        raise Exception(f"Failed to load word list: {e}")

    return [_dice_words[_dice_throws_as_key(word_list)] for _ in range(num_words)]


@app.command()
def generate_passphrase(
    num_passphrases: typing.Annotated[
        int,
        typer.Option(
            help="The number of passphrases to generate.",
            min=1,
        ),
    ] = 1,
    num_words: typing.Annotated[
        int,
        typer.Option(
            help="The number of words to include in the passphrase. We suggest at least a six-word passphrase.",
            min=1,
        ),
    ] = 6,
    separator: typing.Annotated[
        str,
        typer.Option(
            help="The separator to use between the words. For whitespace use ' '.",
        ),
    ] = "-",
    include_a_number: typing.Annotated[
        bool, typer.Option(help="Include a number in the passphrase.")
    ] = True,
    include_a_capital: typing.Annotated[
        bool, typer.Option(help="Capitalize one of the words in the passphrase.")
    ] = True,
    word_list: typing.Annotated[
        _DicewareWordList, typer.Option(help="Which wordlist to use.")
    ] = _DicewareWordList.large,
    colorize: typing.Annotated[bool, typer.Option(help="Colorize the output.")] = True,
):
    """
    Generates a secure passphrase based on the EFF diceware large word list.
    More information about the approach can be found here: https://www.eff.org/dice
    """
    for _ in range(num_passphrases):
        dw = _create_word_list_from_dice(
            num_words=num_words,
            word_list=word_list,
        )

        if include_a_capital:
            cap_idx = secrets.randbelow(
                len(dw)
            )  # Randomly select an index to capitalize.
            dw[cap_idx] = dw[cap_idx].capitalize()

        if include_a_number:
            num_idx = secrets.randbelow(
                len(dw)
            )  # Randomly select an index to insert a number.

            if secrets.choice(
                [0, 1]
            ):  # Randomly decide to prepend or append the number.
                val = (
                    f"{_colorize_text(secrets.randbelow(100), _NUMBER_COLOR)}{dw[num_idx]}"
                    if colorize
                    else f"{secrets.randbelow(100)}{dw[num_idx]}"
                )
            else:
                val = (
                    f"{dw[num_idx]}{_colorize_text(secrets.randbelow(100), _NUMBER_COLOR)}"
                    if colorize
                    else f"{dw[num_idx]}{secrets.randbelow(100)}"
                )
            dw[num_idx] = val
        if colorize:
            _CONSOLE.print(
                _colorize_text(separator, _SEPARATOR_COLOR).join(dw),
                style="white bold on black",
            )
        else:
            print(separator.join(dw))


def _colorize_text(text: str | int, color: str) -> str:
    """
    Apply a color style to the given text using Rich text formatting.

    This function wraps the provided text with Rich formatting tags to apply the specified color.
    This is particularly useful for enhancing the readability and visual appeal of text output in terminal applications.
    The function can handle both string and integer inputs for text.

    Args:
        text (str | int): The text (or number) to which the color style will be applied.
        color (str): The color name or specifier as accepted by Rich. This can be a named color, a hex code, or an RGB tuple formatted as a string.

    Returns:
        str: The text wrapped in Rich formatting tags to apply the specified color.

    Example:
        >>> _colorize_text("Hello, World!", "red")
        '[red]Hello, World![/red]'
        >>> _colorize_text(404, "green")
        '[green]404[/green]'
        >>> _colorize_text("Attention", "#FF5733")
        '[#FF5733]Attention[/#FF5733]'
    """
    return f"[{color}]{text}[/{color}]"


if __name__ == "__main__":
    app()
