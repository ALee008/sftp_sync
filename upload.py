import pathlib
import logging

import paramiko.util
import socket

import local_settings as settings


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
# paramiko has a named logger. Use it.
logging.getLogger('paramiko')
paramiko.util.log_to_file(settings.paths['upload_logs'])


def upload_files():
    """Upload file based on configuration in local_settings.py
    :return: None
    """
    # create sftp object
    try:
        with paramiko.Transport((settings.server['server'], settings.server['port'])) as transport:
            transport.connect(username=settings.login['user'], password=settings.login['password'])
            sftp = paramiko.SFTPClient.from_transport(transport)
            for file_ in pathlib.Path(settings.paths['upload_source']).iterdir():
                destination = pathlib.Path(settings.paths['upload_destination']).joinpath(file_.name)
                print(file_, destination)
                sftp.put(str(file_), str(destination))
                logging.info(f"Upload {file_} -> {destination} [OK]")
    except socket.timeout as msg:
        logging.warning(f"A timeout was ignored: Actual exception message: {msg} [WARN]")
        pass

    return None


if __name__ == '__main__':
    upload_files()