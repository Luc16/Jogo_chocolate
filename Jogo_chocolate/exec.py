import cx_Freeze

executables = [cx_Freeze.Executable("Jogo_Final.py")]

cx_Freeze.setup(
    name="O fantastico pesadelo doce",
    options={"build_exe": {"packages":["pygame", "random"],
                           "include_files":["images/alpino.png", "images/arvore.png", "images/Caminho de biscoito.png",
                                            "images/cenoura.png", "images/diamante.png", "images/fundo.png",
                                            "images/menu.png", "images/nestle.png", "images/ovo.png",
                                            "images/remo_frente.png", "images/remo_tras.png", "images/toblerone.png",
                                            "images/umpalumpas.png", "max.txt"]}},
    executables = executables

    )