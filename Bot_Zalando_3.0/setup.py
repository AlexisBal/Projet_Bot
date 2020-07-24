from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(
    packages=["idna", "json", "timeit", "re", "random",
              "threading", "colorama", "termcolor",
              "requests", "urllib3", "requests.adapters",
              "requests.packages.urllib3.util.retry",
              "user_agent", "bs4", "licensing.models",
              "licensing.methods", "datetime", "discord_webhook"]
)

setup(
    name="ScredAIO",
    version="0.0.3",
    description="Recherche et commande de produit",
    options=dict(build_exe=buildOptions),
    executables=[Executable("ScredAIO.py")],
)
