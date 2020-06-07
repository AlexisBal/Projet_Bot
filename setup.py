from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(
    packages=["idna", "rpa", "tagui", "PasswordGenerator"],
    include_files=["Comptes.json"],
)

base = "None"
executables = [
    Executable(
        "Generateur_Compte_Zalando.py",
        base=base,
    )
]

setup(
    name="Generateur Compte Zalando",
    version="1.0",
    description="Generateur de comptes sur zalando",
    options=dict(build_exe=buildOptions),
    executables=executables,
)
