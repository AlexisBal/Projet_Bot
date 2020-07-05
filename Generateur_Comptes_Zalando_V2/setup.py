from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(
    packages=["idna", "json", "requests", "password_generator", "urllib3", "requests.adapters", "requests.packages.urllib3.util.retry",  'user_agent']
)

base = None
executables = [
    Executable(
        "Generateur_Compte_Zalando.py",
        base=base,
    )
]

setup(
    name="Generateur Compte Zalando",
    version="2.0",
    description="Generateur de comptes sur zalando",
    options=dict(build_exe=buildOptions),
    executables=executables,
)
