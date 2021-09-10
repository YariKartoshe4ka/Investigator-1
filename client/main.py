from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.settings import Settings
from kivy.config import ConfigParser
from kivy.network.urlrequest import UrlRequest
from kivy.utils import platform
from urllib.parse import quote
import os


if platform == 'android':
    from android.permissions import request_permissions, Permission
    request_permissions([Permission.WRITE_EXTERNAL_STORAGE,
                         Permission.READ_EXTERNAL_STORAGE,
                         Permission.INTERNET])

    # Android notification fix
    import jnius
    original_autoclass = jnius.autoclass
    def patched_autoclass(clsname, *args, **kwargs):
        if clsname.endswith('R$drawable'):
            return None
        return original_autoclass(clsname, *args, **kwargs)
    jnius.autoclass = patched_autoclass

import plyer

from stream import StreamViewer


class MainScreen(Screen):

    def set_online_false(self, *args):
        online = self.ids['online']
        online.icon = 'icons/online_false.png'
        online.size_hint = (None, 1)
        online.size = (36, 0)

    def set_online_true(self, *args):
        online = self.ids['online']
        online.icon = 'icons/online_true.png'
        online.size_hint = (None, 1)
        online.size = (36, 0)

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

    def change_stream_visibility(self):
        if self.ids['stream_viewer'].is_alive:
            self.ids['stream_viewer'].stop()
        else:
            self.ids['stream_viewer'].start()
        self.send(b'')


class SettingsScreen(Screen):
    def close(self, settings):
        self.apply_changes()
        root = App.get_running_app().root
        root.current = 'main'

    def apply_changes(self):
        root = App.get_running_app().root

        stream_resolution_table = {"VGA (640x480)": 6,
                                   "CIF (400x296)": 5,
                                   "QVGA (320x240)": 4,
                                   "HQVGA (240x176)": 3,
                                   "QQVGA (160x120)": 0}

        queries = [
            ('framesize', stream_resolution_table[root.config.getdefault('stream', 'resolution', root.config_defaults['stream']['resolution'])])
        ]

        host = root.config.getdefault('network', 'host', root.config_defaults['network']['host'])
        timeout = root.config.getdefaultint('network', 'timeout', root.config_defaults['network']['timeout']) / 1000

        for query in queries:
            UrlRequest(f"http://{host}:80/control?var={query[0]}&val={query[1]}",
                       on_success=root.get_screen('main').set_online_true,
                       on_failure=root.get_screen('main').set_online_false,
                       on_error=root.get_screen('main').set_online_false,
                       on_redirect=root.get_screen('main').set_online_false,
                       timeout=timeout)

        stream_viewer = root.get_screen('main').ids['stream_viewer']
        if stream_viewer.is_alive:
            stream_viewer.stop()
            stream_viewer.start()

    def on_enter(self):
        root = App.get_running_app().root

        s = Settings(on_close=self.close)

        s.add_json_panel('Network', root.config, 'panels/network.json')
        s.add_json_panel('Stream', root.config, 'panels/stream.json')

        self.add_widget(s)


class InvestigatorClientApp(App):
    save_path = os.path.join(plyer.storagepath.get_documents_dir(), 'iClient')

    config_defaults = {'network': {'host': '',
                                   'timeout': 1500},
                       'stream': {'fps': 30,
                                  'save_path': save_path,
                                  'resolution': 'QVGA (320x240)',
                                  'rotation': -90}}

    def build(self):
        sm = ScreenManager(transition=NoTransition())

        sm.config = ConfigParser()
        sm.config.read('config.ini')

        for section, options in self.config_defaults.items():
            sm.config.setdefaults(section, options)

        sm.config.write()
        sm.config_defaults = self.config_defaults

        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(SettingsScreen(name='settings'))

        return sm

    def on_pause(self):
        return True

    def on_start(self):
        root = App.get_running_app().root
        root.get_screen('settings').apply_changes()



if __name__ == '__main__':
    app = InvestigatorClientApp()
    app.run()
