FROM kalilinux/kali-rolling

# RUN sudo usermod -aG docker $USER
# RUN newgrp docker

RUN apt update && \
    apt install -y nmap \
    wpscan nikto python3-pip
WORKDIR /secuscript
COPY . .
RUN pip3 install -r requirements.txt
EXPOSE 1212 1212

# RUN 
CMD python3 main.py