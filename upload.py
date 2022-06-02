import os
import pathlib
import logging
import shutil

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
                if file_.is_dir():
                    continue
                # use os.path instead of pathlib.Path because the latter removes preceding dot in path
                destination = os.path.join(settings.paths['upload_destination'], file_.name)
                sftp.put(str(file_), str(destination))
                logging.info(f"Upload {file_} -> {destination} [OK]")
                # move files after upload
                archive_files(file_)
            delete_folder(settings.archives["upload_archive"])
    except socket.timeout as msg:
        logging.warning(f"A timeout was ignored: Actual exception message: {msg} [WARN]")
        pass

    return None


def archive_files(file_: pathlib.Path):
    """Create archive folder if it does not exist and move uploaded file there.

    :param file_: file to archive
    :return: None
    """
    archived_path = pathlib.Path(settings.archives["upload_archive"]).joinpath(file_.name)
    archived_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(file_, archived_path)
    logging.info(f"Moving file {file_} to {archived_path} [OK]")

    return None


def delete_folder(path: pathlib.Path):
    if path.is_dir():
        shutil.rmtree(path, ignore_errors=True)
        logging.info(f"Removing folder {path} [OK]")
    else:
        logging.info(f"{path} is not a directory.")

    return None


if __name__ == '__main__':
    upload_files()
