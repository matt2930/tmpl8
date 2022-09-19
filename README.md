# tmpl8

This repository hosts code for the future of templating


## Usage
```
$ tmpl8 -h

usage: tmpl8 [-h] [-v] [-d DATA] [-f FILE] command

tmpl8 wrapper for cli commands

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit

command:
  command               command to run

data:
  data used when templating

  -d DATA, --data DATA  json data for templating. Overwrites data from file if -f/--file is specified
  -f FILE, --file FILE  file with data to use for templating
```

### Example Usages
```
$ tmpl8 -d '{"test": "data"}' kubectl apply -f file.yml

Running 'kubectl apply -f /tmp/dir/file.yml'

<output from kubectl command>

$ tmpl8 -f test.json docker build -t test:latest -f Dockerfile .

Running 'kubectl apply -t test:latest -f /tmp/dir/Dockerfile /tmp/dir'

<output from docker build>
```
