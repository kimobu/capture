#!/usr/bin/env python
import urllib

def logCommand(**kwargs):
    f = urllib.urlopen('http://localhost:8081/api/logging/command', data=urllib.urlencode(kwargs))
    f.read()
    f.close()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--position', dest='position', help='The computer position')
    parser.add_argument('--shell', dest='shell', help='The shell used to execute the command')
    parser.add_argument('--command', dest='command', help='The command executed by the shell')
    parser.add_argument('--output', dest='output', help='The output of the command')

    args = parser.parse_args()

    kwargs = {
        'position': args.position,
        'shell': args.shell,
        'command': args.position,
        'output': args.output,
        'hostname': 'localhost'
    }

    try:
        logCommand(**kwargs)
    except:
        print('error')
        raw_input()
