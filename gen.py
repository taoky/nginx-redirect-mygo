#!/usr/bin/env python3
# zero dependency

def main():
    with open("mygo-list.txt") as f:
        l = f.read().splitlines()
    mygo = ""
    for i in l:
        mygo += f'"{i}",\n'
    FILES = ("mygo-lua.conf.template", "mygo.js.template")
    for file in FILES:
        with open(file) as f:
            content = f.read()
        content = content.replace("%%mygo%%", mygo)
        with open(file.replace(".template", ""), "w") as f:
            f.write(content)

if __name__ == "__main__":
    main()
