from decimal import Decimal

from database.DAO import DAO


class Model:
    def __init__(self):
        pass

    def getAnni(self):
        return DAO.getAnni()

    def getAllBrandName(self):
        return DAO.getBrandName()

    def getAllRetailers(self):
        return DAO.getAllRetailers()

    def getTopSales(self, data, brand, retailer):
        return DAO.getTopSales(data, brand, retailer)[:5]

    def getAnalitics(self, data, brand, retailer):
        """
        Metodo che restituisce i parametri che servono per gestire il bottone
        analizza vendite

        return: float, int, list[int], list[int]
        """
        sales = DAO.getTopSales(data, brand, retailer)
        if len(sales) == 0:
            return

        revenue = Decimal('0.0')
        numVendite = 0
        retailers = []
        products = []

        for sale in sales:
            revenue += sale.Quantity * sale.Unit_sale_price
            numVendite += 1
            if sale.Retailer_code not in retailers:
                retailers.append(sale.Retailer_code)
            if sale.Product_number not in products:
                products.append(sale.Product_number)  # <-- anche qui avevi scritto 'Product_code'

        return revenue, numVendite, retailers, products







