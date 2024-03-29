# passwordgen

passwordgen is a command-line tool for generating strong passwords using various
algorithms.
It provides options for generating random strings or sequences of random words.

## Installation
Passwordgen was written in pure Python 3.11 and has no dependencies other than
the standard library, therefore there is no need to install it.
You can simply download the source code and run it directly:

```bash
git clone https://github.com/knkillname/passwordgen
cd passwordgen
bash passwordgen.sh -h
```

You can also install it in your home directory so that running the `passwordgen`
command is more convenient.
To do this you will need pip and git installed on your system.
Run the following command to install PasswordGen as a Python module:

```bash
pip3 install --user git+https://github.com/knkillname/passwordgen
```

On Debian-based systems, you must specify the `--break-system-packages` option
because the installation of external Python packages is disabled by default:

```bash
pip3 install --user --break-system-packages git+https://github.com/knkillname/passwordgen
```

This will install the PasswordGen module in your private bin directory; make
sure that this directory is in your `PATH` environment variable.
If after logging out and back in you still can't run the `passwordgen` command,
try adding the path to your local `.bashrc` file by running this command:

```bash
echo "
# set PATH so it includes user's private bin if it exists
if [ -d \"\$HOME/.local/bin\" ] ; then
    PATH=\"\$HOME/.local/bin:\$PATH\"
fi" >> ~/.bashrc
```

After installation, you can run the `passwordgen` command from anywhere.

### Uninstall

To uninstall `passwordgen` run the following command:

    pip3 uninstall passwordgen

Or, if you installed it with the `--break-system-packages` option:
    
```bash
pip3 uninstall --break-system-packages passwordgen
```

## Usage

To generate some random string passwords, use the `random` command:

    passwordgen random

To generate a sequence of random word password, use the xkcd command:

    passwordgen xkcd

To generate some password that mix words with special characters use the easy 
command:

    passwordgen easy

## Commands

PasswordGen provides the following commands:

- `random`: Generate a random string password.
- `xkcd`: Generate a sequence of random word password.
- `easy`: Generate easy to remember random passwords that mix words with
    special characters.

Use the `--help` option for each command to see a full list of options.

## Contributing

Contributions are welcome! If you'd like to contribute to PasswordGen, please
fork the repository and create a pull request.


## License

PasswordGen is licensed under the MIT License. See LICENSE for more information.
Credits

PasswordGen was created by [knkillname](https://github.com/knkillname).