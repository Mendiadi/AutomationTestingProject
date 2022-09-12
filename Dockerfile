FROM python:3.9.7
COPY api_source ./api_source
COPY ui_source ./ui_source
COPY commons ./commons
COPY tests ./tests
COPY fixtures ./fixtures
ADD tests/data_api.json .
ADD tests/config_test.json .
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["pytest","tests","--lib","playwright","--browser","chrome","-m","smoke"]