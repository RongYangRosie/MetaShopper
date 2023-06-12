from crawler.ebayCrawler import EbayCrawler
from crawler.amazonCrawler import AmazonCrawler
from flask import Flask, render_template, request

'''
def search():
    #if request.method == 'POST':
        #search_query = request.form.get('query').strip()
        search_query = "apple"
        # Initialize eBay crawler

        ebay_crawler = EbayCrawler()

        # Perform scraping on eBay
        ebay_products = ebay_crawler.query(search_query)


        # Initialize Amazon crawler
        amazon_crawler = AmazonCrawler()

        # Perform scraping on Amazon
        amazon_products = amazon_crawler.query(search_query)

        # Print scraped data

        products = ebay_products + amazon_products
        products_sorted = sorted(products, key=lambda x: float(x[4]))
        
        print("sorted products:")
        
        for product in products_sorted:
            print(product)
        #return render_template('results.html', products=products_sorted)

    #return render_template('home.html')

if __name__ == '__main__':
    search()
'''



app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_query = request.form.get('query').strip()
        #search_query = "apple"
        # Initialize eBay crawler

        ebay_crawler = EbayCrawler()

        # Perform scraping on eBay
        ebay_products = ebay_crawler.query(search_query)


        # Initialize Amazon crawler
        amazon_crawler = AmazonCrawler()

        # Perform scraping on Amazon
        amazon_products = amazon_crawler.query(search_query)

        # Print scraped data

        products = ebay_products + amazon_products
        products_sorted = sorted(products, key=lambda x: float(x[4]))
        #for product in products_sorted:
        #    print(product)

        #    打个断点，用debug模式调试看看
        return render_template('results.html', products=products_sorted)

        #print("sorted products:")
        
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
