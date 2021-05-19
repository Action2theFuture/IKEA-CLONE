import csv
from product.models import *

def load_data():
    IMAGE_PATH='/images/products/lamps/'
    NULL_IMAGE='/images/products/null.png'
    # 배경 이미지 추가
    BackgroundImage.objects.create(url=NULL_IMAGE)
    BackgroundImage.objects.create(url="/images/bgimages/1.jpeg")
    BackgroundImage.objects.create(url="/images/bgimages/2.jpeg")

    # 색깔 추가
    with open('color.csv') as color_file:
        color_rows = list(csv.reader(color_file))
        for color_row in color_rows:
            Color.objects.create(
                korean_name = color_row[0],
                english_name = color_row[1]
            )

    with open('data.csv') as csv_file:
        with open('img.csv') as img_file:
            rows = list(csv.reader(csv_file))
            img_rows = list(csv.reader(img_file))

            for idx, row in enumerate(rows):
                if idx == 0:
                    continue
                ## 카테고리 추가
                if not Category.objects.filter(korean_name=row[0]).exists():
                    Category.objects.create(
                        korean_name  = row[0],
                        english_name = row[1]
                    )
                ## 세부 카테고리 추가
                if not SubCategory.objects.filter(korean_name=row[2]).exists():
                    SubCategory.objects.create(
                        korean_name  = row[2],
                        english_name = row[3],
                        category     = Category.objects.get(korean_name=row[0]),
                        content      = row[2]
                    )
                ## 시리즈 추가
                if not Series.objects.filter(korean_name=row[4]):
                    Series.objects.create(
                        korean_name  = row[4],
                        english_name = row[5]
                    )
                ## 상품 추가
                product = Product.objects.create(
                    korean_name      = row[10],
                    english_name     = row[11],
                    price            = row[12],
                    is_online        = row[13],
                    special_price    = row[14],
                    is_new           = row[15],
                    stock            = row[16],
                    background_image = BackgroundImage.objects.get(id = row[17]),
                    sub_category     = SubCategory.objects.get(korean_name=row[2]),
                    series           = Series.objects.get(korean_name=row[4])
                )
                product.color.add(Color.objects.get(korean_name=row[18]))
                ## 상품 설명 추가
                Description.objects.create(
                        content   = row[6],
                        package   = row[7],
                        material  = row[8],
                        recycling = row[9],
                        product   = product
                    )
                ## 이미지 추가
                try:
                    for i in range(6):
                        try:
                            url = IMAGE_PATH+img_rows[idx][i]
                        except:
                            url = NULL_IMAGE
                        Image.objects.create(
                                url     = url,
                                product = product
                            )
                except IndexError:
                    pass