# MetaShopper
Abstract
Based on Option 4b (MetaShopper), I crawled features such as images, names, links, ratings, and prices of
products from popular shopping websites like Amazon and eBay. As required, I read URLs and fields from the
configuration file during the process and provided a user interface for searching products. The crawler returns
a list of products ranked by price, and I used Flask to display the results.
### Brief Guide
1. Build a Python environment
```shell
$ python3 -m venv myenv
$ source myenv/bin/activate
```
2. Install dependencies
```shell
$ pip install -r dependecy.txt
```
3. Run the app file
```shell
$ python app.py
```
4. Open web browser and go to http://127.0.0.1:5000/
5. Start to search a product
### Achievement
1. Implemented two crawlers that can retrieve product information including image, name, link, price, and
rating.
2. Achieved a user-friendly interface that enables users to query and compare product prices and ratings
on both Amazon and eBay.
3. Implemented a page to display products ranked by price.
4. Create a configuration file that includes the required URLs and fields for posting to each store, allowing
users to easily replace them with URLs and fields for other online shops.
