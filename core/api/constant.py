AUTHORS_URL = 'Authors'
ACCOUNT_URL = 'Account'
URL_SWAGGER = ':7017/api/'
BOOKS_URL = "Books"
URL = 'http://localhost'
api_links = {
    "register": "/register",
    "login": '/login',
    "token": '/refreshtoken',
    "findbyAuthor": "/findauthor/",
    "purchaseBook": "/purchase/"
    ,"search": '/search/'
}
ENDPOINTS = {
    "_books_": URL_SWAGGER + BOOKS_URL,
    "_account_":URL_SWAGGER + ACCOUNT_URL,
    "_authors_":URL_SWAGGER + AUTHORS_URL
}

