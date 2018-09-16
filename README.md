# Info

Programma per raccogliere dati su un libro via ISBN ricevuto da bluetooth (scansione tramite app smartphone o PDA dedicato)

## Preparazione sul PC (bluetooth seriale)

The steps bellow worked for me:

Firstly you have to pair the devices. Pairing is relatively easy. I will call client (who starts talking) and server (who replies)

You have to setup the server before: Server side (as root):

    sdptool add --channel=3 SP
    mknod -m 666 /dev/rfcomm0 c 216 0
    rfcomm watch /dev/rfcomm0 3 /sbin/agetty rfcomm0 115200 linux

Client side(as root):

    sdptool add --channel=3 SP
    rfcomm connect /dev/rfcomm0 [SERVER_ADDR] 3

Now to open a serial terminal on the client:

    screen /dev/rfcomm0 115200

Comments:
When you call the last command rfcomm connect... in the client, a device /dev/rfcomm0 will be created and associated to the server /dev/recomm0. This represents the serial link between both.
The last server command: rfcomm watch.... will 'listen' for incoming connections. In connection lost, the command will restart a new 'listen' state.