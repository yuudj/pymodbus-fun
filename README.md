
# WSL2 Y USB
Nos tan facil acceder a dispositiovs USB, que no son storage,  desde docker-desktop en Windows. Necesitamos el `usbipd`.
Es una herramienta que se instala en host Windows `winget install usbipd`

https://learn.microsoft.com/en-us/windows/wsl/connect-usb#prerequisites

https://github.com/dorssel/usbipd-win


Todos estos comandos se ejecutan en una condola de poweshell en HOST
``` bash
# Listamos los dipositivos USB en host.
$ usbipd list

Connected:
BUSID  VID:PID    DEVICE                                                        STATE
3-4    14cd:8168  USB Mass Storage Device                                       Not shared
4-3    1a86:7523  USB-SERIAL CH340                                              Not shared
4-4    046d:c52b  Logitech USB Input Device, USB Input Device                   Not shared

# hacemos bind bus-id del disposiivo que queremos vincular

$ usbipd bind -b 4-3

# al hacer un list nuevamente vemos uqe esta compartido
$ usbipd list

Connected:
BUSID  VID:PID    DEVICE                                                        STATE
3-4    14cd:8168  USB Mass Storage Device                                       Not shared
4-3    1a86:7523  USB-SERIAL CH340                                              Not shared
4-4    046d:c52b  Logitech USB Input Device, USB Input Device                   Shared
```
### Work arround docker.desktop
Ahora solo falta hacer attach del dispositivo a wsl. Las distribuciones wsl de Docker-Desktop (docker-deskto , docker.desktop-data) son especiales, y usbipd no funciona directamente. Es por eso que tenemos que instalar una distro wsl Ubuntu para que nos ayude, se puede hacer desde [Windows Store](https://apps.microsoft.com/detail/9PDXGNCFSCZV).

Fuente: https://github.com/dorssel/usbipd-win/issues/669#issuecomment-1686086810

Una vez instalada la diritribucion de Ubuntu se debe hacer un attach a wsl  con el siguiente comando

```bash
usbipd wsl attach --distribution <<nombre de la nueva distribucion>>
```

### Verificacion
Desde PowerShell ingresamos a la distribucion wsl `docker-desktop` con el siguiente comando

``` bash
wsl --distribution docker-desktop
```
Esto iniciara una consola dentro del linux que maneja docker-desktop dentro en esa linea de comando podemos hacer un `ls /dev/` y podrebos obervar un elemento `ttyUSB0` correspondiente a nuestro dispositivo USB.


### Detach
Para desasociar el dispositivo USB de wsl se debe ejecutar el siguiente comando en el HOST 

``` bash
usbipd detach -b <<bus-id>>
usbipd unbind -b <<bus-id>>
# Por ejemplo 
usbipd detach -b 4-3
usbipd unbind -b 4-3
```


## DEV CONTAINER CON USB

otra alternativa  en el devcontainer

```
 "runArgs": [
        "--device=/dev/ttyUSB0"
    ],

```

## SIMULADOR
pymodbus.simulator --json_file ./setup.json --modbus_server server_try_serial


USANDO TELEGRAPH

https://vleeckf.medium.com/weekend-project-energy-monitoring-with-telegraf-modbus-influxdb-flux-and-grafana-770480136410
