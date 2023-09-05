import time
import psutil
import subprocess
from typing import Tuple, Optional
import re
from loguru import logger
import os
import socket
import win32api
import win32con
import win32file


class GenericHelper:
    def __init__(self) -> None:
        ...

    @staticmethod
    def get_hostname() -> str:
        return socket.gethostname()

    @staticmethod
    def get_ip():
        st = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            st.connect(("10.255.255.255", 1))
            ipaddr = st.getsockname()[0]
        except Exception:
            ipaddr = "127.0.0.1"
        finally:
            st.close()
        return ipaddr

    @staticmethod
    def get_username() -> str:
        return os.getlogin()

    @staticmethod
    def get_removable_drives() -> str:
        drives = [i for i in win32api.GetLogicalDriveStrings().split("\x00") if i]
        rdrives = [
            d for d in drives if win32file.GetDriveType(d) == win32con.DRIVE_REMOVABLE
        ]
        if len(rdrives) == 0:
            logger.error("No removable drives found!")
        return rdrives[0]

    @staticmethod
    def terminate(process: subprocess.Popen) -> None:
        parent = psutil.Process(process.pid)
        for child in parent.children(recursive=True):
            child.kill()
        parent.kill()
        if process.poll() is None:
            logger.info("Process is terminated.")
        else:
            logger.error("Fail to terminate process!")

    @staticmethod
    def prompt_command(cmd: str, timeout: float = 5.0) -> list:
        data = []
        start = time.time()
        logger.info("[{stream}] - {message}", stream="PromptTx", message=cmd)
        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True
        )
        out = process.stdout
        while time.time() - start < timeout:
            if process.poll() is not None:
                break
            line = out.readline().decode("utf-8").strip()
            if line:
                data.append(line)
                logger.debug("[{stream}] - {message}", stream="PromptRx", message=line)
        try:
            GenericHelper.terminate(process)
        except psutil.NoSuchProcess:
            logger.info("Process not exist.")
            pass
        return data

    @staticmethod
    def match_string(pattern: str, data: list) -> Tuple[bool, Optional[list]]:
        """
        match_string("(.+)\s+device\s+$", data)
        """
        matched = []
        for string in data:
            if type(string) == bytes:
                string = string.decode()
            match = re.search(pattern, string)
            if match:
                match_data = match.groups()
                logger.success(f"Regex matches: {match_data}")
                matched.append(match_data)
        if matched:
            return True, matched
        logger.warning(f"Not matched pattern {pattern}")
        return False, None


if __name__ == "__main__":
    g = GenericHelper()
