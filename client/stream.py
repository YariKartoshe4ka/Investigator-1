from kivy.app import App
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.core.image import Image as CoreImage
from urllib.request import urlopen
from socket import setdefaulttimeout
from collections import deque
from PIL import Image as PILImage
import plyer
import datetime
import threading
import io
import os


class StreamViewer(Image):
    is_alive = False
    is_save_image = False

    def start(self):
        root = App.get_running_app().root
        self.url = f"http://{root.config.getdefault('network', 'host', root.config_defaults['network']['host'])}:81/stream"

        setdefaulttimeout(root.config.getdefaultint('network', 'timeout', root.config_defaults['network']['timeout']) / 1000.)

        self.is_alive = True
        self._queue = deque()
        self._thread = threading.Thread(target=self.read_stream)
        self._thread.daemon = True
        self._thread.start()
        self._image_lock = threading.Lock()
        self._image_buffer = None
        Clock.schedule_interval(self.update_image, 1 / max(1, root.config.getdefaultint('stream', 'fps', root.config_defaults['stream']['fps'])))

    def stop(self, close_thread=True):
        root = App.get_running_app().root

        self.is_alive = False
        self.is_save_image = False
        self.opacity = 0
        root.get_screen('main').ids['take_picture_button'].opacity = 0
        Clock.unschedule(self.update_image)

        if close_thread:
            self._thread.join()

    def read_stream(self):
        root = App.get_running_app().root
        
        try:
            stream = urlopen(self.url)
        except:
            self.stop(close_thread=False)
            return

        save_path = root.config.getdefault('stream', 'save_path', root.config_defaults['stream']['save_path'])
        rotation = root.config.getdefaultint('stream', 'rotation', root.config_defaults['stream']['rotation'])

        if not os.path.exists(save_path):
            os.makedirs(save_path)

        if not os.path.isdir(save_path):  
            save_path = root.config_defaults['stream']['save_path']

        root.get_screen('main').ids['take_picture_button'].opacity = 1
        self.opacity = 1

        self.is_save_image = False
        bytes = b''

        while self.is_alive:
            try:
                bytes += stream.read(5 * 1024)
            except:
                root.get_screen('main').ids['take_picture_button'].opacity = 0
                self.stop(close_thread=False)
                return

            a = bytes.find(b'\xff\xd8')
            b = bytes.find(b'\xff\xd9')

            if a != -1 and b != -1:
                jpg = bytes[a:b + 2]
                bytes = bytes[b + 2:]

                data = io.BytesIO(jpg)
                data.seek(0)

                try:
                    data_rotated = io.BytesIO()

                    img = PILImage.open(data)
                    img = img.rotate(rotation, expand=True)
                    img.save(data_rotated, 'jpeg')
                    data_rotated.seek(0)

                    img.close()
                    del data, img

                    im = CoreImage(data_rotated,
                                   ext='jpeg',
                                   nocache=True) 

                    if self.is_save_image:
                        self.is_save_image = False
                        date = datetime.datetime.now()
                        filename = date.strftime('%Y-%m-%d %H-%M-%S') + '.jpg'
                        full_path = os.path.join(save_path, filename)

                        
                        if os.path.exists(full_path):
                            i = 1
                            full_path = full_path[:-4] + f' ({i})' + '.jpg'

                            while os.path.exists(full_path):
                                full_path = full_path.replace(f'({i - 1})', f'({i})')
                                i += 1

                        im.save(full_path)

                        plyer.notification.notify(title='Image saved', timeout=2.5, toast=True)
                except:
                    continue

                with self._image_lock:
                    self._image_buffer = im


    def update_image(self, *args):
        im = None
        with self._image_lock:
            im = self._image_buffer
            self._image_buffer = None
        if im is not None:
            self.texture = im.texture
            self.texture_size = im.texture.size

    def save_image(self):
        self.is_save_image = True