from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(
    packages=["idna", "json", "requests", "password_generator", "urllib3", "requests.adapters", "requests.packages.urllib3.util.retry"],
    include_files=["Comptes.json"],
)

base = None
executables = [
    Executable(
        "Commande_Zalando_V1.py",
        base=base,
    )
]

setup(
    name="Recherche-produit_mise-le-panier",
    version="1.0",
    description="Recherche du produit et mise dans le panier",
    options=dict(build_exe=buildOptions),
    executables=executables,
)
