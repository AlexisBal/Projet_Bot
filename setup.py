from cx_Freeze import setup, Executable

base = None
executables = [Executable("Generateur_Compte_Zalando/Generateur_Compte_Zalando.py", base=base)]
packages = ["idna", "rpa", "tagui", "PasswordGenerator"]
includefiles = ["Generateur_Compte_Zalando/Comptes.json"]

options = {
    'build_exe': {
        'packages': packages,
        'include_files': includefiles,
    },
}

setup(
    name="generateur_comptes_zalando",
    options=options,
    version="1.0",
    description='Générateur de comptes sur Zalando',
    executables=executables
)
