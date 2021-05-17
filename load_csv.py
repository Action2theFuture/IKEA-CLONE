import csv
from product.models import *

with open('product.csv') as csv_file:
    rows = csv.reader(csv_file)
    rows = list(rows)
    for row in rows[1:]:
        if not Category.objects.filter(ko_name=row[0]).exists():
            Category.objects.create(
                ko_name = row[0],
                en_name = row[1]
            )
        if not SubCategory.objects.filter(ko_name=row[2]).exists():
            SubCategory.objects.create(
                ko_name = row[2],
                en_name = row[3],
                category = Category.objects.get(ko_name=row[0])
            )
        if not Series.objects.filter(ko_name=row[4]):
            Series.objects.create(
                ko_name = row[4],
                en_name = row[5]
            )
        
        product = Product.objects.create(
            ko_name = row[10],
            en_name = row[11],
            price = row[12],
            is_online = row[13],
            special_price = row[14],
            is_new = row[15],
            stock = row[16],
            sub_category = SubCategory.objects.get(ko_name=row[2]),
            series = Series.objects.get(ko_name=row[4])
        )

        Description.objects.create(
            content   = row[6],
            package   = row[7],
            material  = row[8],
            recycling = row[9],
            product = product
        )
