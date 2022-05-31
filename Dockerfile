FROM python:3.8
COPY . /api
WORKDIR /api
COPY requirement.txt requirement.txt                                                                                                                                  1.1s
RUN pip install --upgrade pip & pip install -r requirement.txt 
# COPY main.py /app                                                                                                                                                        2.6s
CMD [ "python","main.py" ]