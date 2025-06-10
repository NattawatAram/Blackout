@ECHO OFF
CLS
ECHO 1. Setup ADB 
ECHO 2. Disconnect adb from devices
ECHO.

CHOICE /C 12 /M "Enter your choice:"

IF ERRORLEVEL 2 GOTO Disconnect
IF ERRORLEVEL 1 GOTO Setup

:Disconnect
ECHO [*] Disconnecting ADB from all devices...
adb disconnect
GOTO End

:Setup
ECHO [*] Restarting ADB in TCP mode on port 5555...
adb tcpip 5555
TIMEOUT /T 2 > NUL

ECHO [*] getting device_ip...,.,,
adb shell ip route 

ECHO.
SET /P device_ip="enter the ip above (e.g. 192.168.1.50): "

ECHO [*] Connecting to %device_ip%:5555...
adb connect %device_ip%:5555
adb devices
ECHO.
ECHO [yippee yay :D] done! now unplug the charging cable from the computer!
GOTO End

:End
ECHO.
ECHO Press any key to exit...
PAUSE > NUL
EXIT
