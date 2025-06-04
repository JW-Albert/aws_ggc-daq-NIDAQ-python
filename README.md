# aws_ggc-daq-NIDAQ-python

A Python-based data acquisition system using National Instruments DAQ (Data Acquisition) hardware.

## Overview

This project implements a data acquisition system that interfaces with National Instruments DAQ hardware. It provides functionality for reading analog input signals and managing data acquisition processes.

## Project Structure

```
aws_ggc-daq-NIDAQ-python/
├── API/
│   └── NiDAQ.ini          # Configuration file for DAQ settings
├── src/
│   ├── main.py           # Main application entry point
│   └── nidaq_module.py   # Core DAQ functionality implementation
├── requirements.txt      # Python dependencies
├── recipe.yaml          # Project recipe configuration
└── gdk-config.json      # GDK configuration file
```

## Prerequisites

- Python 3.x
- National Instruments DAQ hardware
- NI-DAQmx driver installed

## Installation

1. Clone the repository:
```bash
git clone https://github.com/JW-Albert/aws_ggc-daq-NIDAQ-python.git
cd aws_ggc-daq-NIDAQ-python
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Configure your DAQ settings in `API/NiDAQ.ini`
2. Adjust parameters in `gdk-config.json` as needed

## Usage

Run the main application:
```bash
python src/main.py
```

## Development

### Local Deployment

To deploy locally:
```bash
./local_deploy.sh
```

To remove local deployment:
```bash
./remove_local_deploy.sh
```

## License

[Specify your license here]

## Contributing

[Add contribution guidelines here]