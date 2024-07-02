ImageOverlayApp v6 bind for Gartic Phone

#To install:

Python 3.10+
```sh
pip install PySide6 Pillow
```
or
```sh
pip install -r requirements.txt
```

#Launch
```sh
python main.py
```
#Using
- Select an image.
- Use the mouse wheel to resize the image.
- Move the image by holding down the left mouse button.
- Press 'T` to pin the image.
- Press 'Y` to unpin the image.

#Compiling a Python file to an EXE

```sh
pip install pyinstaller
```
On the command line, navigate to the directory where your Python file is located (for example, main.py ):
```sh
cd path\to\your\main
```
Run PyInstaller:
```sh
pyinstaller --onefile --windowed --icon=app.png main.py
```
`--windowed` removes the console window (for GUI applications).
`--icon=app.png` adds an icon for your EXE file.
After successful execution, a file will appear in the dist directory main.exe .

Go to the Discord channel - https://discord.gg/n89PDURbTg
:D
