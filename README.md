# wpup

A WordPress update tool written in Python being used to upgrade all WordPress sites hosted at koyu.space.

## Installation and setup

Run the `install.sh` script and create a configuration file at `~/.wpuprc` like this:

```
myhost:blog1
myhost:blog2
otherhost:blog
```

## Usage

```
--help or -h    :   Show help
--sysup or -s   :   Upgrade all host systems
--reboot or -r  :   Reboot all host systems
--puppyup -p    :   Upgrades to the latest version of wpup
```

## wpup in action

[![asciicast](https://asciinema.org/a/YEDGKMLrrAs4x4FyPomf3hiMc.svg)](https://asciinema.org/a/YEDGKMLrrAs4x4FyPomf3hiMc)
