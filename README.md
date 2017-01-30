# 8dot3-brute
8dot3-brute is a script to brute force Windows 8.3 filenames and directories in web servers

# Usage
Usage: ./8dot3-brute.py -u [base url] -f [filename] -d [dirname] -l [length] -c [character set]

Usage: ./8dot3-brute.py -u http://example.com -d 'DOCUME' -v

Usage: ./8dot3-brute.py -u http://example.com -f 'BACKU.ZIP' -c 'P0123456789' -v

Usage: ./8dot3-brute.py -u http://example.com -d 'DOCUME' -c 'NTOS' -v

Usage: ./8dot3-brute.py -u http://example.com -d 'DOCUME' -l 3 -v

# References
https://github.com/irsdl/IIS-ShortName-Scanner
