import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDYear(self):
        years = self._model.getAllYears()
        for y in years:
            self._view._ddAnno1.options.append(ft.dropdown.Option(y))
            self._view._ddAnno2.options.append(ft.dropdown.Option(y))
        self._view.update_page()

    def handleCreaGrafo(self, e):
        self._model.creaGrafo(self._view._ddAnno1.value, self._view._ddAnno2.value)
        n, e = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(
            ft.Text(f"Grafo correttamente creato:")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Nodi: {n} nodi")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Archi: {e}")
        )
        self._view.update_page()

    def handleDettagli(self, e):
        self._view.txt_result.controls.clear()
        edges = self._model.getEdgeGrandi()
        count = 0
        self._view.txt_result.controls.append(ft.Text(f"Archi di peso maggiore:"))
        for e in edges:
            if count < 3:
                self._view.txt_result.controls.append(
                    ft.Text(f"{e[0]} --> {e[1]}: {e[2]["weight"]}")
                )
                count += 1
        num, comp_max = self._model.getCompConnessa()
        self._view.txt_result.controls.append(
            ft.Text(f"Il grafo ha {num} componenti connesse.")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"La componente maggiore è composta da {len(comp_max)} nodi:")
        )
        for i in comp_max:
            self._view.txt_result.controls.append(
                ft.Text(f"{i}")
            )
        num, comp_max_ordinata = self._model.getCompConnessaOrd()
        self._view.txt_result.controls.append(
            ft.Text(f"La componente maggiore è composta da {len(comp_max_ordinata)} nodi:")
        )
        for nodo, grado in comp_max_ordinata:
            self._view.txt_result.controls.append(
                ft.Text(f"Nodo: {nodo} - Grado: {grado}")
            )
        self._view.update_page()


    def handleCerca(self, e):
        self._view.txt_result.controls.clear()

        y1 = self._view._ddAnno1.value
        y2 = self._view._ddAnno2.value

        if y1 is None or y2 is None:
            self._view.txt_result.controls.append(ft.Text("Errore: Seleziona prima gli anni!"))
            self._view.update_page()
            return

        try:
            k = int(self._view._txtInK.value)
        except ValueError:
            self._view.txt_result.controls.append(ft.Text("Errore: Inserisci un numero intero valido per K!"))
            self._view.update_page()
            return

        if len(self._model._graph.nodes) == 0:
            self._view.txt_result.controls.append(ft.Text("Errore: Devi prima creare il grafo!"))
            self._view.update_page()
            return

        opt_list, min_dist, min_dob, max_dob = self._model.calcolaPunto2Ricorsivo(k, y1, y2)

        if opt_list is None:
            self._view.txt_result.controls.append(
                ft.Text(f"Impossibile trovare {k} costruttori in componenti distinte con i dati attuali.")
            )
            self._view.update_page()
            return

        self._view.txt_result.controls.append(
            ft.Text(f"Trovati {k} costruttori!", color="green")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Scarto di età: {min_dist} giorni.")
        )

        self._view.txt_result.controls.append(
            ft.Text(f"Costruttore con veterano più anziano: {opt_list[0].name} (Nato il {min_dob})")
        )
        self._view.txt_result.controls.append(
            ft.Text(f"Costruttore con veterano più giovane: {opt_list[-1].name} (Nato il {max_dob})")
        )
        self._view.txt_result.controls.append(ft.Text("Lista dei costruttori selezionati:"))
        for c in opt_list:
            self._view.txt_result.controls.append(
                ft.Text(f"{c.name} | Data veterano: {c.oldest_driver_dob}")
            )
        self._view.update_page()