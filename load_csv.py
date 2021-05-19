import csv
from product.models import *

IMAGE_PATH='/images/products/lamps'

with open('data.csv') as csv_file:
    rows = csv.reader(csv_file)
    with open('img.csv') as img_file:
        img_rows = csv.reader(img_file)
        img_rows = list(img_rows)
        rows = list(rows)
        for idx, row in enumerate(rows):
            if idx == 0:
                continue

            if not Category.objects.filter(korean_name=row[0]).exists():
                Category.objects.create(
                    korean_name = row[0],
                    english_name = row[1]
                )
            if not SubCategory.objects.filter(korean_name=row[2]).exists():
                SubCategory.objects.create(
                    korean_name = row[2],
                    english_name = row[3],
                    category = Category.objects.get(korean_name=row[0]),
                    content = row[2]
                )
            if not Series.objects.filter(korean_name=row[4]):
                Series.objects.create(
                    korean_name = row[4],
                    english_name = row[5]
                )
            
            product = Product.objects.create(
                korean_name       = row[10],
                english_name       = row[11],
                price         = row[12],
                is_online     = row[13],
                special_price = row[14],
                is_new        = row[15],
                stock         = row[16],
                sub_category  = SubCategory.objects.get(korean_name=row[2]),
                series        = Series.objects.get(korean_name=row[4])
            )

            Description.objects.create(
                    content   = row[6],
                    package   = row[7],
                    material  = row[8],
                    recycling = row[9],
                    product   = product
                )
            try:
                for i in range(len(img_rows[idx])):
                    Image.objects.create(
                        url     = IMAGE_PATH+img_rows[idx][i],
                        product = product
                        )
            except IndexError:
                pass