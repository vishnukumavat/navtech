from orders.models import Products, Orders
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.db.models import F
from django.db import connection

class GetOrderStatistics(object):
    def __init__(self) -> None:
        pass 

    def dictfetchall(self, cursor):
        # Return all rows from a cursor as a dict
        columns = [col[0] for col in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

    def get_data(self):
        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT 
                    UPPER(p.product_name) AS "Product Name" ,
                    SUM(quantity) AS "Ordered Quantity", 
                    o.price AS "At Price", 
                    (sum(quantity)*o.price) AS "Total Amount"
                FROM 
                    orders o
                JOIN products p ON
                    p.id  = o.product_id 
                WHERE 
                    created_at >= CURRENT_DATE - INTERVAL '3 months' 
                GROUP BY 
                    p.product_name,o.price ;
            ''')
            dataList = self.dictfetchall(cursor)
            return {"result": "success", "total_records": len(dataList), "stats":dataList}
