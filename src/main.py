import time
import argparse
import logging
import sys
import re
import json

from nidaq_module import init_task, read_task_data

from awsiot.greengrasscoreipc.clientv2 import GreengrassCoreIPCClientV2
from awsiot.greengrasscoreipc.model import JsonMessage, PublishMessage


logger = logging.getLogger(__name__)


def configure_logging(log_level: str):
    numeric_level = getattr(logging, log_level.upper(), None)

    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {log_level}")

    logging.basicConfig(stream=sys.stdout, level=numeric_level)
    logger.setLevel(numeric_level)


def publish_message(
    ipc_client: GreengrassCoreIPCClientV2, topic: str, message: dict[str, any]
):
    publish_message = PublishMessage(json_message=JsonMessage(message=message))

    return ipc_client.publish_to_topic_async(
        topic=topic, publish_message=publish_message
    )


def fix_and_parse_rules(raw: str):
    # 1. 為鍵 (key) 加上雙引號，允許裡面出現 / - 等字元
    fixed = re.sub(r"([^\s\{\}\[\]:,]+)\s*:", r'"\1":', raw)
    # 2. 為值 (value) 加上雙引號，忽略數字、true/false/null
    fixed = re.sub(r":\s*([A-Za-z_][\w\-]*)", r':"\1"', fixed)

    # 解析成 Python 結構
    parsed = json.loads(fixed)
    logger.info("Parsed rules (before merge): %r", parsed)

    # 如果是 list，就把裡面的 dict 全部合併
    if isinstance(parsed, list):
        merged = {}
        for d in parsed:
            merged.update(d)
        logger.info("Merged rules: %r", merged)
        return merged

    # 否則直接回傳
    return parsed


def main() -> int:
    parser = argparse.ArgumentParser(description="DAQ and IPC publisher component")

    parser.add_argument(
        "--rawdata_topic", type=str, required=True, help="IPC topic to publish messages"
    )

    parser.add_argument(
        "--log_level",
        type=str,
        default="INFO",
        help="Logging level (default: INFO)",
    )

    parser.add_argument(
        "--header_mapping",
        type=str,
        required=True,
        help="Mapping physical channel names to header names",
    )

    args = parser.parse_args()

    # Configure logging
    configure_logging(args.log_level)

    rawdata_topic = args.rawdata_topic

    try:
        ipc_client = GreengrassCoreIPCClientV2()
    except Exception as e:
        logger.error("Failed to create Greengrass IPC client: %s", e)
        sys.exit(1)

    logger.info("Starting DAQ and publishing to topic: %s", rawdata_topic)

    ini_path = "/greengrass/v2/packages/artifacts-unarchived/imcloud.imphm.daq.NIDAQ/1.0.0/imphm-aws_ggc-daq-NIDAQ/API/NiDAQ.ini"  # 有問題

    task, samples_per_read, sample_rate, channel_names = init_task(ini_path)
    logger.info(
        "DAQ task initialized with sample rate: %s, samples per read: %s",
        sample_rate,
        samples_per_read,
    )

    HeaderMapping = fix_and_parse_rules(args.header_mapping)

    logger.info("Header mapping: %s", HeaderMapping)
    logger.info("Type of header mapping: %s", type(HeaderMapping))

    for i in channel_names:
        if i in HeaderMapping:
            channel_names[channel_names.index(i)] = HeaderMapping[i]
        else:
            logger.warning("Channel name %s not found in header mapping", i)

    logger.info("Mapped channel names: %s", channel_names)

    is_running = True
    while is_running:
        data = read_task_data(task, samples_per_read)
        # logger.info("Read data")

        message = {
            "timestamp": time.time(),
            "sample_rate": sample_rate,
            "data_len": len(data),
            "data_header": ",".join(channel_names),
            "data": data,
        }

        publish_message(ipc_client, rawdata_topic, message)

        # logger.info("Published message with timestamp: %s", message["timestamp"])

    return 0


if __name__ == "__main__":
    main()
