Python Bittorrent Client
--------------------------------------------
This is a basic bittorrent client written in python. It downloads the file by connecting to the tracker. The peer list can be extracted and connections can be made by using socket .
The basic handshake and message formats have all been figured out. 
This client handles HTTP as well as UDP tracker so every torrent file can be processed easily.
This client implements a rarest-first piece download strategy. That is, the client will attempt to download those pieces that are least common in the swarm once the common pieces started downloading.
It also manages a log text file which can be easily found out in the folder which contains program file. This log file can be used to find out IP,ports and other information if any error 
occurs during the download.
It gives user freedom to select the download location for the torrent file and also shows the progress of download with percentage. 
----------------------------------------------
Help:
BitTorrent specification from BitTorrent.org

----------------------------------------------
Requirments :

1. bencode
2. bitarray
3. bitstring
4. progress

----------------------------------------------
Installation Details:

1.pip3 install bencode
2.pip3 install bitarray
3.pip3 install bitstring
4.pip3 install progress

----------------------------------------------