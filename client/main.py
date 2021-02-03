from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen, NoTransition
from kivy.uix.settings import Settings
from kivy.config import ConfigParser
from kivy.network.urlrequest import UrlRequest
from kivy.utils import platform
from urllib.parse import quote
from webbrowser import open
from socket import gethostbyname


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

        host = root.config.get('network', 'host')
        port = root.config.get('network', 'port')
        command = quote(command)

        url = f'http://{host}:{port}/api?cmd={command}'

        UrlRequest(url, on_success=self.set_online_true,
                        on_failure=self.set_online_false,
                        on_error=self.set_online_false,
                        on_redirect=self.set_online_false)

    def stream(self):
        root = App.get_running_app().root

        host = root.config.get('network', 'host')
        port = root.config.get('network', 'port')

        open(f'http://{host}:{port}/')



class SettingsScreen(Screen):
    def close(self, settings):
        root = App.get_running_app().root
        root.current = 'main'

    def on_enter(self):
        root = App.get_running_app().root

        s = Settings(on_close=self.close)

        root.config.set('network', 'host', self.scan('Investigator-1'))
        s.add_json_panel('Network', root.config, 'panels/network.json')

        self.add_widget(s)

    def scan(self, name):
        root = App.get_running_app().root
        try:
            return gethostbyname(name)
        except:
            return root.config.get('network', 'host')



class InvestigatorClientApp(App):
    def build(self):
        sm = ScreenManager(transition=NoTransition())

        sm.config = ConfigParser()
        sm.config.read('config.ini')

        sm.add_widget(MainScreen(name='main'))
        sm.add_widget(SettingsScreen(name='settings'))

        return sm

    def on_pause(self):
        return True


if __name__ == '__main__':
    app = InvestigatorClientApp()
    app.run()
