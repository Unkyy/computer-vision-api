
import os 

url=os.environ['URL']
print(url)
nmap="nmap -sS -T4 -p- "+ url
wpscan="wpscan --url "+url
nikto -h URL , bruteforce d'url

os.system(nmap)
os.system(wpscan)
FROM kalilinux/kali-rolling

ENTRYPOINT ["tail"]
CMD ["-f","/dev/null"]