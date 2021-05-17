# Venµs data processing

## Description

Simple scripts for the data processing and retrieval for the Venµs satellite
imagery. Find all the scripts in the directory `scripts`.

## Data retrieval

Once you order the data through
the [Venµs data portal](https://venus.bgu.ac.il/venus/), you should receive
an e-mail with an ftp with all the data. Instead of downloading each of them
individually, you could run `download-results.sh`. See the following help:

```
download-results.sh
Download all Venus data from the link the user has been provided.

Syntax: download-results.sh [-h] url username
options:
url         The url the user has obtained from the Venus request
username    The username required to obtain the data
h           Print this help and exit
```

## Data processing

To unzip all the retrieved data, you could run `unzip-archives.sh`. See
the following help:

```
unzip-archives.sh
Unzip all downloaded archives and save them to the same directory.

Syntax: unzip-archives.sh [-h] data_dir
options:
data_dir    Path to the directory containing the archives
h           Print this help and exit
```

To filter the data based on the cloud coverage, you could run
`filter-cloud-coverage.py`. See the following help:

```
usage: filter-cloud-coverage.py [-h] --data_dir DATA_DIR [--cloud_min CC_MIN]
    [--cloud_max CC_MAX] [--operation {report,extract}] [--delete DELETE]

Print list of files with the desired cloud coverage or cleanup the directory
    from the undesired ones

optional arguments:
  -h, --help            show this help message and exit
  --data_dir DATA_DIR   Path to the directory containing Venus data
  --cloud_min CC_MIN    Minimal desired cloud coverage in percents (inclusive)
  --cloud_max CC_MAX    Maximal desired cloud coverage in percents (inclusive)
  --operation {report,extract}
                        An operation to perform: Either to print suiting files
                        on the standard output or to extract the DBL archives
                        for the suiting scenes
  --delete DELETE       Whether to delete the ones that do not suit the desired
  cloud coverage
```
