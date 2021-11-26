# nmap-pyparser

It is tool for parsing nmap xml result.

## Usage

```
python3 nmap-parser.py [options]

Options:
-f,--filename           name of xml file for parsing, always required
-s, --services          create folder with files, which contains ips with founded service
-l                      generate log file
--ports-by-services     get ports with specified services
```

## Examples

```
python3 nmap-parser.py -f testdata.xml -l -s --ports-by-services http,https
```