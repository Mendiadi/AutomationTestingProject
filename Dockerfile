
FROM python:3.9.7
COPY commons ./commons
COPY core ./core
COPY fixtures ./fixtures
COPY tests ./tests
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["pytest","tests","--lib","playwright","--browser","chrome","-m","smoke"]