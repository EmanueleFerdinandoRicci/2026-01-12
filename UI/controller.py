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
            ft.Text(f"Grafo correttamente creato. Il grafo contiene {n} nodi e {e} archi")
        )
        self._view.update_page()

    def handleDettagli(self, e):
        pass

    def handleCerca(self, e):
        pass

