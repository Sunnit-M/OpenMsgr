FROM python:3.11-slim

# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000
CMD [ "python","-m","eventlet","--listen", "0.0.0.0:5000","OpenMsgr-Server.py" ]