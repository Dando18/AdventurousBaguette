# Adventurous Baguette
------------------------

A tool to search git commits and identify changes in performance variation over them. 

It uses JSON files to specify most of the settings. For example:

```json
[
    {
        "repo": {
            "url": "",  # give one of these two to specify a git repo
            "path": "",
            "hashes": ["", "", ""], # give a list of commit hashes to search over (or "last x" for last x commits)
            "build": {
                "commands": [
                    "make clean",  # specify how to build 
                    "make"
                ]
            },
            "tests": [
                {
                    "name": "",       # specify an executable to run and measure
                    "executable": "",
                    "prefix": "",
                    "args": "",
                    "mpi": ""
                }
            ]
        },
        "profile": {
            "profiler": "hpctoolkit", # how to profile (hpctoolkit or gprof)
            "flags": "",
            "workspace": "",
            "search": "exhaustive"  # how to search commits listed (exhaustive, random, or binary)
        }
    }
]
```

This can then be run with `main.py -i input.json -v`.


Here's the full usage:

```
usage: main.py [-h] -i INPUT [--working-directory WORKING_DIRECTORY] [-p] [-v]

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        json file to read input settings
  --working-directory WORKING_DIRECTORY
                        where to store files
  -p, --preserve        don't remove scratch files
  -v, --verbose         verbose output
```