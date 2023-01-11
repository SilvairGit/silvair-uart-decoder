<h1 align="center">Silvair UART Decoder</h1>

# About The Repository

Silvair UART Decoder is a python library for parsing Silvair UART protocol messages. It also includes two applications that 
could be used for message parsing:
* HLA Extension for `Saleae Logic 2`.
* Python script for parsing .csv file with serial values for `Saleae Logic 1`.

Recommended way is to use Logic 2 and HLA extension. Python script could be unstable in future versions.

### Built With

UART Decoder is using construct python library to parse all UART messages. Also, it validates CRC value using Crcmod package. 
All used packages can be obtained from setup.py file.

# Getting Started

## How to start with HLA Extension?

Tested on Ubuntu 20.04 with Python 3.8 and Windows 11 with Python 3.10. 
Make sure, you have `Python` with at least 3.6 version and installed pip.

### Installation:

#### Using Command line:

1. Install UART-Decoder using pip: `pip install silvair-uart-decoder`. WARNING:  If `The script is installed in directory, which is not PATH` will appear during installation, add this directory to PATH environment variable.
2. In terminal, call `generate_uart_decoder_extension <PATH>` executable, where `<PATH>` is directory when you want to install HLA Extension. Example: `generate_uart_decoder_extension .` to install in current directory. `SilvairUARTDecoder` folder should be generated in passed path.

#### Using 'install' file

1. Run script according to system are you using:
    - Windows: `install_windows.bat`
    - Linux: `install_linux.bat`
    - Mac: `install_mac.sh`

### Running Extension in Logic 2

1. Open Logic 2, click "Extensions" icon on right side. 
2. In upper-right corner should be three dots with "Load existing extensions" option. Click it.
3. Load `extension.json` located in previously generated `SilvairUARTDecoder` directory.
4. Click "Analyzers" icon on right side.
5. Load `Async Serial` analyzer for appropriate channel, and then load `Silvair UART Decoder`.
6. Hooray, Silvair UART messages should be described above waveforms! :)

### Screenshots

![](https://github.com/SilvairGit/silvair-uart-decoder/blob/master/readme_photos/Screenshot_20211001_121335.png?raw=true)
![](https://github.com/SilvairGit/silvair-uart-decoder/blob/master/readme_photos/Screenshot_20211001_121452.png?raw=true)


## How to start with Python script?

1. Make sure, you have `Python` with at least 3.6 version and installed pip.
2. Install UART-Decoder using pip: `pip install silvair-uart-decoder`. WARNING:  If `The script is installed in directory, which is not PATH` will appear during installation, add this directory to PATH environment variable.
3. Run application using command: 
```
silvair-uart-decoder
```
Pass `-h` parameter to show help with instruction how to use script.

Parameters:

- `-f` or `--format-converter`: input format converter (optional)
- `-O` or `--output-file`: output file path (result will be saved in this file) (optional)
- input csv file (required)

### Supported input format converters

Currently two input format decoders are available:

- `default` - data must be in format: `<timestamp>,<label>,<uart_command_frame>` 
- `saleae` - data must be in format: `<timestamp>,<label>,<byte>` (default Saleae export format).

### Example

Parse logs stored in `example.csv` from Logic 1, and save it to `example.txt`. `example.csv` is in saleae Logic 1 format:
```
silvair-uart-decoder -f saleae -O example.txt example.csv 
```

### How to export data from Logic 1?

1. Open Logic 1 with measurements
2. Add `Async Serial` analyzers for appropriate channels
3. Click on gear circle near `Decoded Protocols`
4. Click `Export search results`

### Screenshots

![](https://github.com/SilvairGit/silvair-uart-decoder/blob/master/readme_photos/Screenshot_20211001_122800.png?raw=true)