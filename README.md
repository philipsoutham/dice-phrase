# Dice Phrase

Dice Phrase is a portable and easy-to-install command-line passphrase generator emulates dice rolls to use with a word list to create secure, memorable passphrases. Inspired by the concept of Diceware, Dice Phrase is designed to produce passphrases that are both secure and easy to remember, making it an excellent tool for anyone looking to create easy to use passwords/passphrases.

Frankly, I don't expect anyone but me to use this. I wanted something to use on the CLI so I built it.

## Features

- **Portable**: Comes as a single executable that you can run from anywhere on your system.
- **Customizable**: Supports standard [EFF word lists](https://www.eff.org/deeplinks/2016/07/new-wordlists-random-passphrases) as well as [fandom-based lists](https://www.eff.org/deeplinks/2018/08/dragon-con-diceware) for more personalized passphrases.
- **Secure**: Generates passphrases based on simulated dice rolls to ensure high entropy and security.
- **Easy to Use**: Simple command-line interface that does not require any installation and very little setup.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development, running, and testing purposes.

### Prerequisites

- Python 3.10+
- pip (Python package installer)

### Installing

Dice Phrase is distributed as a Python zipapp. To get started, you can build the zipapp using the provided `Makefile`.

1. Clone the repository:
    ```bash
    git clone https://github.com/philipsoutham/dice-phrase.git
    cd dice-phrase
    ```

2. Build the zipapp:
    ```bash
    make
    ```

This will create a file named `dice-phrase`, which is an executable zip application. No put it in your `$PATH`, I suggest some place like `~/bin`.

### Usage

To generate a passphrase, simply run the executable with the desired options. To see the options:

```bash
$ dice-phrase --help
```

#### Options

- `--num-passphrases`: The number of passphrases to generate. [default: 1]
- `--num-words`: The number of words to include in the passphrase. We suggest at least a six-word passphrase. [default: 6]
- `--separator`: The separator to use between the words. For whitespace use ' '. [default: -]
- `--include-a-number` OR `--no-include-a-number`: Include a number in the passphrase. [default: include-a-number]
- `--include-a-capital` OR `--no-include-a-capital`: Capitalize one of the words in the passphrase. [default: include-a-capital]
- `--word-list`: Which wordlist to use. [default: large]
- `--colorize` OR `--no-colorize`: Colorize the output. [default: colorize]

### Example(s)

Default options

```bash
$ dice-phrase
Caretaker-geologist56-stooge-unstitch-resonant-brought
```

Using the Harry Potter fandom list

```bash
$ dice-phrase --num-words 7 --word-list harry-potter
stolen-bludger-0kitchens-British-dancing-strikes-hufflepuff
```

<!-- 
## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.
-->

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/philipsoutham/dice-phrase/tags).

## Authors

- **Philip Southam** - *Initial work* - [philipsoutham](https://github.com/philipsoutham)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by the [EFF Dice-Generated Passphrase](https://www.eff.org/dice) methodology.
- OpenAI's ChatGPT 4 Turbo helped with the documentation, not the code.