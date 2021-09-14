## Przygotowanie plików

plik GasModulesReadingsTest.py nalezy uczynić wykonywalny oraz
zgodnym z systemem unix za pomocą poleceń
* sudo dos2unix GasModulesReadingsTest.py
* sudo chmod +x GasModulesReadingsTest.py

## Instalacja service

* skopiować GasModulesReadingTest.service do /usr/local/lib/systemd/system
* polecenia:
* cd /usr/local/lib/
* sudo mkdir systemd
* sudo mkdir system
* cp /home/pi/AirlySensorsProduction/service/GasModulesReadingTest.service /usr/local/lib/systemd/system/GasModulesReadingTest.service
* cd /usr/local/lib/systemd/system/
* sudo dos2unix GasModulesReadingTest.service
* utworzyć dowiązanie symboliczne
* sudo ln -s /usr/local/lib/systemd/system/GasModulesReadingTest.service /etc/systemd/system/GasModulesReadingTest.service
* reset demna
* sudo systemctl daemon-reload
nasz serwis powinien być już dostępny w systemie rpi

### Sterowanie serwisem
* Możliwe polecenia:
* sudo systemctl start GasModulesReadingTest.service - Startuje services, wykonanie tego kroku pozwala włączyć serwis ale po reboocie systemu będzie on wyłączony
* sudo systemctl stop GasModulesReadingTest.service - Zatrzymuje services, wykonanie tego kroku pozwala wyłączyć serwis
* sudo systemctl status GasModulesReadingTest.service - sprawdza status serwisu oraz pokazuje aktualne logi z działania programu
* sudo systemctl enable GasModulesReadingTest.service - polecenie powoduje stworzenie dowiązań symbolicznych pozwalających startować serwis po starcie systemu operacyjnego
* sudo systemctl disable GasModulesReadingTest.service - ma przeciwne działanie do polecenia wyżej, usuwa ono możliwość startu serwisu przy starcie systemu operacyjnego
* sudo systemctl restart GasModulesReadingTest.service - uruchamia ponownie serwis

Wydanie wiele razy pod rząd polecenia systemctl start GasModule.. nie powoduje powielenia uruchomionego programu
