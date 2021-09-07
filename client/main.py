from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.settings import Settings
from kivy.config import ConfigParser
from kivy.network.urlrequest import UrlRequest
from kivy.utils import platform
from urllib.parse import quote
from socket import gethostbyname
import os
import plyer

from stream import StreamViewer


if platform == 'android':
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.WRITE_EXTERNAL_STORAGE,
                         Permission.READ_EXTERNAL_STORAGE,
                         Permission.INTERNET])


class MainScreen(Screen):

    def set_online_false(self, *args):
        online = self.ids['online']
        online.icon = 'icons/online_false.png'
        online.size = (30, 30)

    def set_online_true(self, *args):
        online = self.ids['online']
        online.icon = 'icons/online_true.png'
        online.size = (30, 30)

    def send(self, command: bytes):
        root = App.get_running_app().root

        timeout = root.config.getdefaultint('network', 'timeout', root.config_defaults['network']['timeout'])
        host = root.config.getdefault('network', 'host', root.config_defaults['network']['host'])
        command = quote(b'\x01' + command + b'\xff')

        url = f'http://{host}:80/api?cmd={command}'

        r = UrlRequest(url, on_success=self.set_online_true,
                            on_failure=self.set_online_false,
                            on_error=self.set_online_false,
                            on_redirect=self.set_online_false,
                            timeout=timeout / 1000)

    def send_speed(self, value):
        command = b''

        closer = lambda x, y, z: x if abs(x - y) <= abs(z - y) else z
        start = closer(closer(0, value, 127), value, 255)

        if start == 0:
            command += b'\x0a'
        elif start == 127:
            command += b'\x0b'
        else:
            command += b'\x0c'

        length = start - value

        if length > 0:
            for i in range(abs(length)):
                command += b'\x0e'
        elif length < 0:
            for i in range(abs(length)):
                command += b'\x0d'

        self.send(command)

    def send_angle(self, value):
        command = b''

        closer = lambda x, y, z: x if abs(x - y) <= abs(z - y) else z
        start = closer(closer(0, value, 67), value, 135)

        if start == 0:
            command += b'\x0f'
        elif start == 67:
            command += b'\x10'
        else:
            command += b'\x11'

        length = start - value

        if length > 0:
            for i in range(abs(length)):
                command += b'\x13'
        elif length < 0:
            for i in range(abs(length)):
                command += b'\x12'

        self.send(command)

    def change_stream_visibility(self):
        if self.ids['stream_viewer'].is_alive:
            self.ids['stream_viewer'].stop()
        else:
            self.ids['stream_viewer'].start()
        self.send(b'')


class SettingsScreen(Screen):
    def close(self, settings):
        root = App.get_running_app().root
        root.current = 'main'

    def on_enter(self):
        root = App.get_running_app().root

        s = Settings(on_close=self.close)

        s.add_json_panel('Network', root.config, 'panels/network.json')
        s.add_json_panel('Stream', root.config, 'panels/stream.json')

        self.add_widget(s)



class InvestigatorClientApp(App):
    try:
        host = gethostbyname('Investigator-1')
    except:
        host = ''
    save_path = os.path.join(plyer.storagepath.get_downloads_dir(), 'iClient')

    config_defaults = {'network': {'host': host,
                                   'timeout': 3000,
                                   'logging': False},
                       'stream': {'fps': 30,
                                  'save_path': save_path}}

    config_update = {'network': {'host': host}}


    def build(self):
        sm = ScreenManager(transition=NoTransition())

        sm.config = ConfigParser()
        sm.config.read('config.ini')

        for section, options in self.config_defaults.items():
            sm.config.setdefaults(section, options)

        for section, options in self.config_update.items():
            for option, value in options.items():
                if sm.config.get(section, option) == '':
                    sm.config.set(section, option, value)

        sm.config.write()
        sm.config_defaults = self.config_defaults

        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(SettingsScreen(name='settings'))

        return sm

    def on_pause(self):
        return True


if __name__ == '__main__':
    app = InvestigatorClientApp()
    app.run()
