FROM python
WORKDIR /api
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD python app.py
