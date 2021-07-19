import os
import logging

import paramiko.util
import local_settings as settings

# paramiko has a named logger. Use it.
logging.basicConfig()
logging.getLogger('paramiko').setLevel(logging.DEBUG)
paramiko.util.log_to_file(settings.paths['logs'])
# create sftp object
with paramiko.Transport((settings.server['server'], settings.server['port'])) as transport:
    transport.connect(username=settings.login['user'], password=settings.login['password'])
    sftp = paramiko.SFTPClient.from_transport(transport)
    for file_name in settings.files:
        source = os.path.join(settings.paths['source'], file_name)
        destination = os.path.join(settings.paths['destination'], file_name)
        sftp.get(source, destination)
