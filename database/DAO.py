from database.DB_connect import DBConnect
from model.daily_sales import Daily_sales
from model.products import Product
from model.retailers import Retailer


class DAO():

    @staticmethod
    def getAnni():
        cnx = DBConnect.get_connection()
        res = []
        if cnx is None:
            return res
        else:
            cursor = cnx.cursor()

            query = """select distinct year(Date) as year
                       from go_daily_sales gds 
            """
            cursor.execute(query)

            for row in cursor:
                res.append(row[0])
            cursor.close()
            cnx.close()
        return res

    @staticmethod
    def getBrandName():
        cnx = DBConnect.get_connection()
        res = []
        if cnx is None:
            return res
        else:
            cursor = cnx.cursor(dictionary=True)

            query = """select distinct Product_brand
                       from go_products gp 
            """
            cursor.execute(query)

            for row in cursor:
                res.append(row["Product_brand"])
            cursor.close()
            cnx.close()
        return res

    @staticmethod
    def getAllRetailers():
        cnx = DBConnect.get_connection()
        res = []
        if cnx is None:
            return res
        else:
            cursor = cnx.cursor(dictionary=True)

            query = """select *
                        from go_retailers gr
                    """
            cursor.execute(query)

            for row in cursor:
                res.append(Retailer(**(row)))
            cursor.close()
            cnx.close()
        return res


    @staticmethod
    def getTopSales(anno=None, brand=None, retailer=None):
        cnx = DBConnect.get_connection()
        res = []
        if cnx is None:
            return res

        else:
            cursor = cnx.cursor(dictionary=True)

            query = """SELECT gds.*
                       FROM go_daily_sales gds
                       JOIN go_products gp ON gds.Product_number = gp.Product_number
                       WHERE 
                           YEAR(gds.Date) = COALESCE(NULLIF(%s, ''), YEAR(gds.Date))
                           AND gp.Product_brand = COALESCE(NULLIF(%s, ''), gp.Product_brand)
                           AND gds.Retailer_Code = COALESCE(NULLIF(%s, ''), gds.Retailer_Code)
                       ORDER BY (gds.Unit_Sale_Price * gds.Quantity)  DESC
                    """

            # Converti None a stringa vuota per NULLIF
            params = (
                str(anno) if anno is not None else '',
                brand if brand is not None else '',
                retailer if retailer is not None else ''
            )

            cursor.execute(query, params)

            for row in cursor:
                res.append(Daily_sales(**row))
            cursor.close()
            cnx.close()

        return res



if __name__ == '__main__':
    print(DAO.getAnni())
    print(DAO.getBrandName())
    for s in DAO.getTopRetailers():
        print(s)
    print(DAO.getAllRetailers())
