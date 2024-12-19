FROM python:3.9-slim

WORKDIR /app
COPY . .

RUN pip install grpcio grpcio-tools

RUN python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. glossary.proto

CMD ["python", "server.py"]