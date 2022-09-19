# tmpl8

This repository hosts code for the future of templating


## Usage
```
$ tmpl8

usage: tmpl8 [-h] [-v] ...

tmpl8 wrapper for cli commands

positional arguments:
  command        command to run

optional arguments:
  -h, --help     show this help message and exit
  -v, --version  show program's version number and exit
```

### Example Usages
```
$ tmpl8 kubectl apply -f file.yml

Running 'kubectl apply -f /tmp/dir/file.yml'

<output from kubectl command>

$ tmpl8 docker build -t test:latest -f Dockerfile .

Running 'kubectl apply -t test:latest -f /tmp/dir/Dockerfile /tmp/dir'

<output from docker build>
```
