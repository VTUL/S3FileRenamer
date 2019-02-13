# S3FileRenamer
Find and remove characters from directories and files that pose difficulty in Amazon S3.

## Getting Started

Download Python file and run with arguments.

### Prerequisites

Python 3

#### Usage

Run tool without rename argument to generate log file of directories and files to be renamed.
```
./S3FileRenamer.py --path /mnt/libnas/SpecScan --log ~/Downloads
```
Review log file to verify changes are acceptable.

Run with rename argument to rename files and directories.
```
./S3FileRenamer.py --path /mnt/libnas/SpecScan --log ~/Downloads --rename
```

View options.
```
./S3FileRenamer.py --help
usage: S3FileRenamer.py [-h] [-r] -p PATH -l LOG

Find and replace S3-illegal characters

optional arguments:
  -h, --help            show this help message and exit
  -r, --rename          Perform rename action.
  -p PATH, --path PATH  Path to data directory
  -l LOG, --log LOG     Path to log file directory
```

## Running the tests

Tests forthcoming


## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

