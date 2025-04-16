import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._retailer= None

    def fillddAnno(self):
        anni = self._model.getAnni()
        for y in anni:
            self._view._ddAnno.options.append(ft.dropdown.Option(y))

    def fillddBrand(self):
        for b in self._model.getAllBrandName():
            self._view._ddBrand.options.append(ft.dropdown.Option(b))

    def fillRetailer(self):
        for retailer in self._model.getAllRetailers():
            self._view._ddRetailer.options.append(ft.dropdown.Option(key=
                                                                     retailer.Retailer_code,
                                                                     text=retailer.Retailer_name,
                                                                     data=retailer, on_click=self.read_retailer))

    def read_retailer(self, e):
        self._retailer = e.control.data

    def handleTopVendite(self, e):
        anno = self._view._ddAnno.value
        brand = self._view._ddBrand.value
        retailer = self._view._ddRetailer.value
        self._view.txt_result.controls.clear()
        result = []
        if anno == "Nessun filtro":
            anno = None
        if brand == "Nessun filtro":
            brand = None
        if retailer == "Nessun filtro":
            retailer = None
        result = self._model.getTopSales(anno, brand, retailer)
        if len(result) == 0:
            self._view.create_alert("Nessuna vendita trovata!")
        else:
            for s in result:
                self._view.txt_result.controls.append(
                    ft.Text(str(s))
            )
        self._view.update_page()

    def handleAnalizzaVendite(self, e):
        anno = self._view._ddAnno.value
        brand = self._view._ddBrand.value
        retailer = self._view._ddRetailer.value
        self._view.txt_result.controls.clear()
        if anno == "Nessun filtro":
            anno = None
        if brand == "Nessun filtro":
            brand = None
        if retailer == "Nessun filtro":
            retailer = None
        revenue, numVendite, retailers, products = self._model.getAnalitics(anno, brand, retailer)
        if numVendite == 0:
            self._view.create_alert("Nessuna vendita trovata!")
            return

        self._view.txt_result.controls.append(
            ft.Text(f"Statistiche vendite:\n"
                    f"Giro d'affari: {revenue}\n"
                     f"Numero vendite: {numVendite}\n"
                     f"Numero retailers coinvolti: {len(retailers)}\n"
                     f"Numero prodotti coinvolti: {len(products)}"
                )
        )
        self._view.update_page()

