from subprocess import Popen, PIPE
from pathlib import Path
from sys import exit

def konvertuj(path):
    ime_fajla = path.stem
    proces = Popen(("pyuic6", "-x", str(path), "-o", f"{ime_fajla}.py"), stdout=PIPE, stderr=PIPE)
    out, err = proces.communicate()
    exitcode = proces.returncode

    if exitcode == 0:
        print(f"Konvertovan fajl {ime_fajla}")
        return

    print(f"Doslo je do greske: {out.decode('utf-8')}\n{err.decode('utf-8')}")

    if input("Nastavi dalje? y/any key: ") != 'y':
        exit(1)

if __name__ == '__main__':
    ui_folder = Path(r"..\UI")

    fajlovi = list(ui_folder.glob("*.ui"))

    for fajl_path in fajlovi:
        konvertuj(fajl_path)
