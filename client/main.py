from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.settings import Settings
from kivy.config import ConfigParser
from kivy.network.urlrequest import UrlRequest
from kivy.utils import platform
from urllib.parse import quote
from socket import gethostbyname
from stream import StreamViewer
import os
import plyer

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

    def send(self, command):
        root = App.get_running_app().root

        timeout = root.config.getdefaultint('network', 'timeout', root.config_defaults['network']['timeout'])
        host = root.config.getdefault('network', 'host', root.config_defaults['network']['host'])
        command = quote(command)

        url = f'http://{host}:80/api?cmd={command}'

        UrlRequest(url, on_success=self.set_online_true,
                        on_failure=self.set_online_false,
                        on_error=self.set_online_false,
                        on_redirect=self.set_online_false,
                        timeout=timeout / 1000)

    def change_stream_visibility(self):
        if self.ids['stream_viewer'].is_alive:
            self.ids['stream_viewer'].stop()
        else:
            self.ids['stream_viewer'].start()
        self.send('ping')



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
                                   'timeout': 3000},
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
