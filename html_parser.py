from bs4 import BeautifulSoup


# with open("ui/header.html", mode="r") as f:
#     html = f.read()

# soup = BeautifulSoup(html, "html.parser")
# menu = soup.find(id="menu_create_wallet")
# print(menu.get_text())

# tag = soup.new_tag("b")
# tag.string = "be bold"
# menu.string.replace_with("Bob")
# menu.replace_with(tag)

# print(menu)
# print(soup.prettify())

# let's make a Python function for that


def get_menu_html(current_page_name):
    # each <li> tag has its own ID
    html = """
        <ul>
            <li id="menu_home"><a href="/">Home</a></li>
            <li id="menu_products"><a href="/products.html">Products</a></li>
            <li id="menu_about"><a href="/about.html">About</a></li>
        </ul>
    """

    soup = BeautifulSoup(html, "html.parser")

    # find the tag <li> by ID
    tag = soup.find(id="menu_" + current_page_name)

    # create a new tag <b> with the same text as in <li>
    newtag = soup.new_tag("b")
    newtag.string = tag.get_text()

    # replace <a> inside <li> to <b>
    # so <li><a>...</a></li> turns into <li><b>...</b></li>
    tag.find("a").replace_with(newtag)

    # return prettified HTML
    return soup.prettify()


# try it
print(get_menu_html("home"))
print(get_menu_html("products"))
print(get_menu_html("about"))
