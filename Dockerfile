FROM python:3.9
ADD api_source .
ADD ui_source .
ADD commons .
ADD requirements.txt .
RUN pip install -r requirements.txt
CMD ['pytest./tests --lib selenium --browser chrome --url https://localhost/']