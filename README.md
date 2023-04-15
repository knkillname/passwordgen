# PasswordGen

PasswordGen is a command-line tool for generating strong passwords using various
algorithms.
It provides options for generating random strings or sequences of random words.

## Installation
Passwordgen was written in pure Python 3.10 and has no dependencies other than
the standard library, therefore there is no need to install it.
You can simply download the source code and run it directly:

    git clone https://github.com/knkillname/passwordgen
    cd passwordgen
    bash passwordgen.sh -h

If you really want to install it, you can use pip:

    pip install .

After installation, you can run the `passwordgen` command from anywhere.

## Usage

To generate some random string passwords, use the `random` command:

    passwordgen random

To generate a sequence of random word password, use the xkcd command:


    passwordgen xkcd

## Commands

PasswordGen provides the following commands:

    random: Generate a random string password
    xkcd: Generate a sequence of random word password

Use the --help option for each command to see a full list of options.
Options

## Contributing

Contributions are welcome! If you'd like to contribute to PasswordGen, please
fork the repository and create a pull request.


## License

PasswordGen is licensed under the MIT License. See LICENSE for more information.
Credits

PasswordGen was created by [knkillname](https://github.com/knkillname).