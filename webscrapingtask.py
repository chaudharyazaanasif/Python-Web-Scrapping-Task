import requests,re
from bs4 import BeautifulSoup

page_number = 50

while True:
    url = f"https://books.toscrape.com/catalogue/page-{page_number}.html"
    
    response=requests.get(url)
    html_response=response.text
    soup = BeautifulSoup(html_response, 'html.parser')

    li_items = soup.select("ol.row > li ")
    for item in li_items:
        product_info = item.find("article", class_="product_pod")
        product_title = product_info.find("h3").find("a")["title"]

        image_url = item.find("div", class_="image_container")
        image_urls = image_url.find("a")["href"]
        product_info_url = f"https://books.toscrape.com/{image_urls}"

        response_product_pg = requests.get(product_info_url)
        soup_prod_page = BeautifulSoup(response_product_pg.content, "html.parser")

        product_price_info=soup_prod_page.find("article", class_="product_page")
        price = product_price_info.find("p", class_="price_color").text

        product_stock=product_price_info.find("p", class_="instock availability").get_text(strip=True)
        match = re.search(r"\((\d+)\s+available\)", product_stock)
        if match:
            stock = int(match.group(1))

        product_availability_status=product_stock
        status = re.search(r"^[^(]+", product_availability_status).group().strip()

        description = soup_prod_page.select_one("article.product_page > p").get_text(strip=True)
    
        table = soup_prod_page.find("table", class_="table table-striped")
        upc = table.find("th", string="UPC").find_next("td").get_text(strip=True)
    

        rating_tag = soup_prod_page.find("p", class_="star-rating")
        rating_word = rating_tag["class"][1]
        ratings = {
            "One": 1,
            "Two": 2,
            "Three": 3,
            "Four": 4,
            "Five": 5
}
        review_stars = "⭐" * ratings[rating_word]
       
    
    '''product_object = {
                "title": product_title,
                "Image_url": image_urls,
                "product_Price": price
                "Available_stock": stock
                "product_availability": status
                "Product_upc": upc
                "Product_description": description
                "Product_review": review_stars
                
            }'''

    page_number += 1
    if response.status_code != 200:
        break
    