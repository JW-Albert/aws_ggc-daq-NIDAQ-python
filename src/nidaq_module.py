"""
nidaq_module.py

This module provides a way to initialize and read data from NI DAQmx devices using an INI configuration file.
It supports multiple analog input types, including Voltage, Current, and Accelerometer channels.

Key Functions:
- config_filter(): Extracts INI section data into dictionaries.
- init_task(): Initializes a DAQmx Task and configures all channels and timing.
- read_task_data(): Reads data from the task and returns it in (X, Y, Z) format or similar tuple format.
"""

import nidaqmx
import configparser

# Filter and extract sections from INI file, return a list of dictionaries
def config_filter( ini_path: str ,sections: str ) -> list:
    config = configparser.ConfigParser()
    config.optionxform = str  # Preserve original key casing
    config.read( ini_path )

    content = []
    for section in config.sections():
        if section.startswith( sections ):  # Match sections that start with the specified prefix
            content_dict = dict( config.items(section) )  # Convert section items to dictionary
            content_dict["__section__"] = section  # Add section name for reference
            content.append( content_dict )

    return content


# Initialize DAQmx task and configure channels and sampling
def init_task( ini_path: str ) -> tuple:
    DAQmxChannel = config_filter(ini_path ,"DAQmxChannel")  # Get DAQ channel configurations
    DAQmxTask = config_filter(ini_path ,"DAQmxTask")        # Get DAQ task settings
    

    task = nidaqmx.Task()  # Create a new DAQmx task
    channel_names = []

    for ch in DAQmxChannel:
        ChanType = ch["ChanType"]  # Channel type, e.g., "Analog Input"
        measType = ch["AI.MeasType"]  # Measurement type, e.g., Voltage, Current, Accelerometer
        physical = ch["PhysicalChanName"]  # Physical channel name (e.g., cDAQ1Mod1/ai0)
        channel_names.append(physical)  # 加入通道名稱

        min_val = float( ch["AI.Min"] )  # Minimum expected value
        max_val = float( ch["AI.Max"] )  # Maximum expected value

        if ( ChanType == "Analog Input" ):
            match measType:
                case ( "Voltage" ):
                    # Add analog voltage input channel
                    task.ai_channels.add_ai_voltage_chan(physical, min_val=min_val, max_val=max_val)
                case ( "Current" ):
                    # Add analog current input channel
                    task.ai_channels.add_ai_current_chan(physical, min_val=min_val, max_val=max_val)
                case ( "Accelerometer" ):
                    # Add analog accelerometer input channel
                    task.ai_channels.add_ai_accel_chan(
                        physical_channel=physical,
                        min_val=min_val,
                        max_val=max_val,
                        units=nidaqmx.constants.AccelUnits.G,
                        sensitivity=float(ch["AI.Accel.Sensitivity"]),
                        sensitivity_units=nidaqmx.constants.AccelSensitivityUnits.MILLIVOLTS_PER_G,
                        current_excit_val=float(ch["AI.Excit.Val"])
                    )

    # Configure sampling clock with rate and number of samples per channel
    sample_rate = float( DAQmxTask[0]["SampClk.Rate"] )
    samples_per_read = int( DAQmxTask[0]["SampQuant.SampPerChan"] )
    task.timing.cfg_samp_clk_timing(
        rate=sample_rate,
        sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS,
        samps_per_chan=samples_per_read
    )

    return task ,samples_per_read ,sample_rate ,channel_names  # Return the task and sample size


# Read task data and return it as a list of tuples [(x1, y1, z1), ...]
def read_task_data( task ,samples_per_read ) -> list:
    data = task.read( number_of_samples_per_channel=samples_per_read )

    if isinstance( data[0] ,list ):  # Multiple channels
        return list( zip(*data) )  # Combine values from each channel as tuples
    else:  # Single channel
        return [(val,) for val in data]  # Return values as single-element tuples
