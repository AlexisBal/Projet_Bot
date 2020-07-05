from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(
    packages=["idna", "re", "urllib", "urllib.parse", "bs4", "user_agent", "time", "json", "requests", "password_generator", "urllib3", "requests.adapters", "requests.packages.urllib3.util.retry"]
)

setup(
    name="Recherche_Checkout_Produit",
    version="2.0",
    description="Recherche et commande du produit",
    options=dict(build_exe=buildOptions),
    executables=[Executable("Commande_Zalando.py")],
)
