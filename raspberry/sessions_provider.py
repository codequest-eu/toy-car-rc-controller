import glob
import os
import datetime

class SessionsProvider:

    def __init__(self, directory):
        self.directory = directory

    def dict_from_session(self, session):
        name = os.path.basename(session)
        timestamp = datetime.datetime.strptime(name[8:], '%Y%m%d%H%M%S')
        return {
            'name': name,
            'timestamp': timestamp.strftime('%d.%m.%Y at %H:%M:%S')
        }

    def get_sessions(self):
        path = os.path.join(self.directory, 'session-*')
        sessions = [name for name in glob.glob(path) if os.path.isdir(name)]
        sessions = sorted(sessions)[::-1]
        return list(map(self.dict_from_session, sessions))

