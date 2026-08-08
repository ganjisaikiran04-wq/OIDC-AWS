from flask import Flask, render_template_string, request, redirect, url_for, session

app = Flask(__name__)

# In production, move this to an environment variable / AWS Secrets Manager.
app.secret_key = "multi-cloud-devops-secret-key"


# ============================================================
# PRODUCTS
# ============================================================

products = [
    {
        "id": 1,
        "name": "Cloud DevOps T-Shirt",
        "category": "Fashion",
        "price": 499,
        "original_price": 999,
        "rating": 4.5,
        "image": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500",
    },
    {
        "id": 2,
        "name": "DevOps Laptop",
        "category": "Electronics",
        "price": 54999,
        "original_price": 69999,
        "rating": 4.7,
        "image": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=500",
    },
    {
        "id": 3,
        "name": "Cloud Computing Book",
        "category": "Books",
        "price": 799,
        "original_price": 1299,
        "rating": 4.6,
        "image": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=500",
    },
    {
        "id": 4,
        "name": "Wireless Headphones",
        "category": "Electronics",
        "price": 1999,
        "original_price": 3999,
        "rating": 4.3,
        "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500",
    },
    {
        "id": 5,
        "name": "DevOps Backpack",
        "category": "Fashion",
        "price": 1299,
        "original_price": 2499,
        "rating": 4.4,
        "image": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500",
    },
    {
        "id": 6,
        "name": "Mechanical Keyboard",
        "category": "Electronics",
        "price": 2999,
        "original_price": 4999,
        "rating": 4.8,
        "image": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=500",
    },
]


# ============================================================
# HTML
# ============================================================

HTML = """
<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="UTF-8">

    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <title>Multi Cloud DevOps</title>

    <style>

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: Arial, sans-serif;
        }

        body {
            background: #f1f3f6;
            color: #212121;
        }

        /* HEADER */

        .header {
            background: #2874f0;
            color: white;
            padding: 10px 5%;
            display: flex;
            align-items: center;
            gap: 25px;
            position: sticky;
            top: 0;
            z-index: 1000;
        }

        .logo {
            font-size: 24px;
            font-weight: bold;
            min-width: 210px;
        }

        .logo span {
            color: #ffe500;
        }

        .search {
            flex: 1;
            display: flex;
            max-width: 650px;
        }

        .search input {
            width: 100%;
            padding: 12px;
            border: none;
            outline: none;
            font-size: 15px;
        }

        .search button {
            width: 55px;
            border: none;
            background: white;
            color: #2874f0;
            font-size: 18px;
            cursor: pointer;
        }

        .header-button {
            background: white;
            color: #2874f0;
            padding: 10px 25px;
            font-weight: bold;
            border: none;
            cursor: pointer;
        }

        .cart {
            font-weight: bold;
            white-space: nowrap;
        }

        /* CATEGORIES */

        .categories {
            background: white;
            padding: 15px 5%;
            display: flex;
            justify-content: center;
            gap: 50px;
            box-shadow: 0 2px 4px #ddd;
        }

        .category {
            cursor: pointer;
            font-weight: bold;
        }

        .category:hover {
            color: #2874f0;
        }

        /* HERO */

        .hero {
            margin: 15px auto;
            width: 90%;
            min-height: 260px;
            background: linear-gradient(
                120deg,
                #2874f0,
                #00bcd4,
                #673ab7
            );
            color: white;
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 50px;
            overflow: hidden;
        }

        .hero h1 {
            font-size: 42px;
            margin-bottom: 15px;
        }

        .hero p {
            font-size: 19px;
            margin-bottom: 25px;
        }

        .hero button {
            background: #ff9f00;
            color: white;
            border: none;
            padding: 14px 30px;
            font-weight: bold;
            font-size: 16px;
            cursor: pointer;
        }

        .clouds {
            font-size: 100px;
            opacity: 0.8;
        }

        /* PRODUCTS */

        .container {
            width: 90%;
            margin: auto;
        }

        .section {
            background: white;
            margin-bottom: 20px;
            padding: 20px;
        }

        .section-title {
            font-size: 24px;
            font-weight: bold;
            margin-bottom: 20px;
        }

        .products {
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: 15px;
        }

        .product {
            background: white;
            border: 1px solid #eee;
            padding: 12px;
            transition: 0.2s;
        }

        .product:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px #ddd;
        }

        .product img {
            width: 100%;
            height: 170px;
            object-fit: cover;
        }

        .product-name {
            font-weight: bold;
            margin: 10px 0;
            height: 40px;
        }

        .rating {
            display: inline-block;
            background: #388e3c;
            color: white;
            padding: 4px 7px;
            font-size: 12px;
            border-radius: 3px;
        }

        .price {
            font-size: 19px;
            font-weight: bold;
            margin-top: 8px;
        }

        .old-price {
            color: #878787;
            text-decoration: line-through;
            margin-left: 5px;
            font-size: 13px;
        }

        .discount {
            color: #388e3c;
            font-size: 13px;
            margin-top: 5px;
        }

        .add-cart {
            width: 100%;
            margin-top: 10px;
            padding: 9px;
            border: none;
            background: #ff9f00;
            color: white;
            font-weight: bold;
            cursor: pointer;
        }

        /* FOOTER */

        footer {
            margin-top: 30px;
            background: #172337;
            color: white;
            padding: 40px 8%;
        }

        .footer-grid {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 30px;
        }

        footer h3 {
            color: #878787;
            margin-bottom: 15px;
        }

        footer p {
            margin: 8px 0;
            color: #ddd;
        }

        /* RESPONSIVE */

        @media(max-width: 1000px) {

            .products {
                grid-template-columns: repeat(3, 1fr);
            }

            .header {
                flex-wrap: wrap;
            }

            .logo {
                min-width: auto;
            }
        }

        @media(max-width: 600px) {

            .products {
                grid-template-columns: repeat(2, 1fr);
            }

            .categories {
                gap: 15px;
                overflow-x: auto;
                justify-content: flex-start;
            }

            .hero {
                padding: 25px;
            }

            .hero h1 {
                font-size: 28px;
            }

            .clouds {
                display: none;
            }

            .footer-grid {
                grid-template-columns: 1fr 1fr;
            }
        }

    </style>

</head>


<body>


<!-- ======================================================
     HEADER
====================================================== -->

<div class="header">

    <div class="logo">
        Multi Cloud <span>DevOps</span>
    </div>


    <form class="search" method="GET" action="/">

        <input
            type="text"
            name="search"
            placeholder="Search for products, cloud tools and more..."
            value="{{ search }}"
        >

        <button type="submit">
            🔍
        </button>

    </form>


    <button class="header-button">
        Login
    </button>


    <div class="cart">
        🛒
        <a href="/cart" style="color:white;text-decoration:none;">
            Cart ({{ cart_count }})
        </a>
    </div>

</div>


<!-- ======================================================
     CATEGORIES
====================================================== -->

<div class="categories">

    <div class="category">☁️ Cloud</div>

    <div class="category">💻 Electronics</div>

    <div class="category">👕 Fashion</div>

    <div class="category">📚 Books</div>

    <div class="category">🚀 DevOps</div>

    <div class="category">🔥 Offers</div>

</div>


<!-- ======================================================
     HERO
====================================================== -->

<div class="hero">

    <div>

        <h1>
            Multi Cloud DevOps
        </h1>

        <p>
            Everything you need for your Cloud & DevOps journey.
        </p>

        <button>
            SHOP NOW
        </button>

    </div>


    <div class="clouds">
        ☁️ ☁️ ☁️
    </div>

</div>


<!-- ======================================================
     PRODUCTS
====================================================== -->

<div class="container">

    <section class="section">

        <div class="section-title">
            Top Deals on DevOps Products
        </div>


        <div class="products">

            {% for product in products %}

            <div class="product">

                <img
                    src="{{ product.image }}"
                    alt="{{ product.name }}"
                >


                <div class="product-name">
                    {{ product.name }}
                </div>


                <span class="rating">
                    {{ product.rating }} ★
                </span>


                <div class="price">

                    ₹{{ "{:,}".format(product.price) }}

                    <span class="old-price">
                        ₹{{ "{:,}".format(product.original_price) }}
                    </span>

                </div>


                <div class="discount">

                    {{
                        ((product.original_price - product.price)
                        / product.original_price * 100)
                        | round
                    }}% off

                </div>


                <form
                    method="POST"
                    action="/add/{{ product.id }}"
                >

                    <button class="add-cart">
                        ADD TO CART
                    </button>

                </form>

            </div>

            {% endfor %}

        </div>

    </section>

</div>


<!-- ======================================================
     FOOTER
====================================================== -->

<footer>

    <div class="footer-grid">


        <div>

            <h3>ABOUT</h3>

            <p>
                About Multi Cloud DevOps
            </p>

            <p>
                Careers
            </p>

            <p>
                DevOps Community
            </p>

        </div>


        <div>

            <h3>HELP</h3>

            <p>
                Payments
            </p>

            <p>
                Shipping
            </p>

            <p>
                Cancellation
            </p>

            <p>
                FAQ
            </p>

        </div>


        <div>

            <h3>POLICY</h3>

            <p>
                Terms of Use
            </p>

            <p>
                Privacy Policy
            </p>

            <p>
                Security
            </p>

        </div>


        <div>

            <h3>CONTACT</h3>

            <p>
                support@multiclouddevops.com
            </p>

            <p>
                Cloud & DevOps Support
            </p>

        </div>


    </div>

</footer>


</body>

</html>
"""


# ============================================================
# HOME
# ============================================================

@app.route("/", methods=["GET"])
def home():

    search = request.args.get("search", "").strip()

    if search:

        filtered_products = [
            product
            for product in products
            if (
                search.lower() in product["name"].lower()
                or search.lower() in product["category"].lower()
            )
        ]

    else:

        filtered_products = products


    cart = session.get("cart", [])


    return render_template_string(
        HTML,
        products=filtered_products,
        search=search,
        cart_count=len(cart),
    )


# ============================================================
# ADD TO CART
# ============================================================

@app.route("/add/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):

    # Make sure the product actually exists
    product_exists = any(
        product["id"] == product_id
        for product in products
    )

    if product_exists:

        cart = session.get("cart", [])

        cart.append(product_id)

        session["cart"] = cart


    return redirect(url_for("home"))


# ============================================================
# CART
# ============================================================

@app.route("/cart")
def cart():

    cart = session.get("cart", [])


    cart_products = [
        product
        for product in products
        if product["id"] in cart
    ]


    total = sum(
        product["price"]
        for product in cart_products
    )


    items_html = "".join(
        f"""
        <div class="item">
            {product['name']} -
            ₹{product['price']}
        </div>
        """
        for product in cart_products
    )


    if not items_html:

        items_html = "<p>Your cart is empty.</p>"


    return f"""
    <!DOCTYPE html>

    <html>

    <head>

        <title>Shopping Cart</title>

        <style>

            body {{
                font-family: Arial;
                background: #f1f3f6;
                padding: 40px;
            }}

            .cart {{
                background: white;
                padding: 30px;
                max-width: 800px;
                margin: auto;
            }}

            h1 {{
                color: #2874f0;
            }}

            .item {{
                padding: 15px;
                border-bottom: 1px solid #ddd;
            }}

            .total {{
                font-size: 25px;
                font-weight: bold;
                margin-top: 20px;
            }}

            a {{
                color: #2874f0;
            }}

        </style>

    </head>


    <body>

        <div class="cart">

            <h1>
                🛒 Your Cart
            </h1>

            {items_html}

            <div class="total">
                Total: ₹{total}
            </div>

            <br>

            <a href="/">
                ← Continue Shopping
            </a>

        </div>

    </body>

    </html>
    """


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/health")
def health():

    return {
        "status": "healthy",
        "application": "Multi Cloud DevOps"
    }


# ============================================================
# APPLICATION START
# ============================================================

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )