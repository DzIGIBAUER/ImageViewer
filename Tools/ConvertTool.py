from subprocess import Popen, PIPE
from pathlib import Path
from sys import exit

def konvertuj(path):
    imeFajla = path.stem

    cmd = ("pyuic6", "-x", str(path), "-o", fr"{uiFolder}\{imeFajla}UI.py")

    proces = Popen(cmd, stdout=PIPE, stderr=PIPE)
    out, err = proces.communicate()
    exitcode = proces.returncode

    if exitcode == 0:
        print(f"Konvertovan fajl {imeFajla}")
        return

    print(f"Doslo je do greske: {out.decode('utf-8')}\n{err.decode('utf-8')}")

    if input("Nastavi dalje? y/any key: ") != 'y':
        exit(1)


if __name__ == '__main__':
    uiFolder = Path(r"..\UI")

    uiFajlovi = uiFolder.glob("*.ui")

    for fajlPath in uiFajlovi:
        konvertuj(fajlPath)
