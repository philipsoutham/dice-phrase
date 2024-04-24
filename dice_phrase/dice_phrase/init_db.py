"""
This script converts word lists from text format to Python pickle files for quicker access.
The script handles different types of word lists: standard EFF word lists and specialized fandom-based lists.
Each text file is expected to follow a specific formatting that matches predefined regular expressions,
which ensure the correct entries are processed and stored.

The standard word lists typically involve 4-5 sequential rolls of a 6-sided die, while the fandom word lists
involve three separated rolls of a 20-sided die. Pickle files are used for efficient loading during runtime.
"""

import importlib.resources
import io
import pathlib
import pickle
import re

# Regular expressions for matching the indices in the standard and fandom word lists
_four_to_five_rolls_of_6_sided = re.compile(r"\d{4,5}")
_three_rolls_of_20_sided = re.compile(rb"\d{1,2}-\d{1,2}-\d{1,2}")

# Lists of word list filenames
_wordlists = [
    "eff_large_wordlist.txt",
    "eff_short_wordlist_1.txt",
    "eff_short_wordlist_2_0.txt",
]

_fandom_word_lists = [
    "gameofthrones_8k-2018.txt",
    "harrypotter_8k_3column-txt.txt",
    "memory-alpha_8k_2018.txt",
    "starwars_8k_2018.txt",
]


def convert_standard_wordlists_to_pickle():
    """
    Converts standard word lists to pickle format.
    This function reads the text files, filters entries based on the regex for 4-5 consecutive numbers,
    and pickles the resulting dictionary of {index: word}.
    """
    for wl in _wordlists:
        wl_prefix = wl.split(".")[0]
        try:
            with open(
                pathlib.Path(__file__).parent.joinpath(f"{wl_prefix}.pkl"), "wb"
            ) as f:
                # Read, filter, and split the lines into (index, word) pairs
                pickle.dump(
                    {
                        idx: word.strip()
                        for idx, word in map(
                            lambda x: x.split(),
                            filter(
                                _four_to_five_rolls_of_6_sided.match,
                                io.StringIO(
                                    importlib.resources.read_text(__package__, wl)  # type: ignore
                                ).readlines(),
                            ),
                        )
                    },
                    f,
                    protocol=pickle.HIGHEST_PROTOCOL,
                )
        except Exception as e:
            print(f"Failed to convert {wl} due to {e}")


def convert_fandom_wordlists_to_pickle():
    """
    Converts fandom-specific word lists to pickle format.
    This function reads the binary text files, filters entries based on the regex for three separated numbers,
    and pickles the resulting dictionary of {index: word}.
    """
    for wl in _fandom_word_lists:
        wl_prefix = wl.split(".")[0]
        try:
            with open(
                pathlib.Path(__file__).parent.joinpath(f"{wl_prefix}.pkl"), "wb"
            ) as f:
                # Read, filter, and split the lines into (index, word) pairs
                pickle.dump(
                    {
                        idx: word.strip()
                        for idx, word in map(
                            lambda x: x.decode("latin").split(),
                            filter(
                                _three_rolls_of_20_sided.match,
                                io.BytesIO(
                                    importlib.resources.read_binary(__package__, wl)  # type: ignore
                                ).readlines(),
                            ),
                        )
                    },
                    f,
                    protocol=pickle.HIGHEST_PROTOCOL,
                )
        except Exception as e:
            print(f"Failed to convert {wl} due to {e}")


if __name__ == "__main__":
    convert_standard_wordlists_to_pickle()
    convert_fandom_wordlists_to_pickle()
