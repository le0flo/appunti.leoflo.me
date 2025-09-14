from pathlib import Path
import toml

config = {
    "home": {
        "content": """
        Questi appunti sono stati presi da [me](https://leoflo.me).
        Potrebbero esserci errori di qualunque genere, perciò attenti e confrontate sempre tutto ciò che leggete, specialmente da siti come questi.
        Se vuoi vedere come funziona questo sito, visita la repository su [GitHub](https://github.com/le0flo/appunti.leoflo.me).
        """,
    },
    "overrides": {
        "header": """
        <script
            id="MathJax-script"
            async
            src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"
        ></script>
        <script>
            MathJax = {
                tex: {
                    displayMath: [["\\$\\$", "\\$\\$"]],
                    inlineMath: [["\\$", "\\$"]],
                },
                loader: {
                    load: ["ui/safe"],
                },
            };
        </script>
        """,
    },
}

def init(path: Path):
    global config

    path = path.joinpath("configuration")
    path.mkdir(parents=True, exist_ok=True)

    file = path.joinpath("config.toml")

    if file.exists():
        toml_string = file.read_text()
    else:
        toml_string = toml.dumps(config)

    config.update(toml.loads(toml_string))
    file.write_text(toml.dumps(config))
