# The wifi world stage
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

from gi.repository import Gtk, Gdk

from kano.gtk3.buttons import KanoButton
from kano.utils import play_sound

from kano_init_flow.stage import Stage
from kano_init_flow.ui.scene import Scene, Placement
from kano_init_flow.ui.speech_bubble import SpeechBubble
from kano_init_flow.paths import common_media_path
from kano_init_flow.ui.utils import add_class, cb_wrapper, scale_image
from kano_init_flow.ui.css import apply_styling_to_screen

class AudioLab(Stage):
    """
        The overscan setting window
    """

    id = 'audio-lab'
    _root = __file__

    def __init__(self, ctl):
        super(AudioLab, self).__init__(ctl)

        apply_styling_to_screen(self.css_path('audio-lab.css'))

    def first_scene(self):
        s = self._setup_first_scene()
        self._ctl.main_window.push(s.widget)

    def help_leds(self):
        s = self._setup_help_leds()
        self._ctl.main_window.push(s.widget)

    def help_power(self):
        s = self._setup_help_power()
        self._ctl.main_window.push(s.widget)

    def help_jack(self):
        s = self._setup_help_jack()
        self._ctl.main_window.push(s.widget)

    def _setup_first_scene(self):
        scene = Scene(self._ctl.main_window)
        scene.set_background(self.media_path('audio-lab-bg-4-3.png'),
                             self.media_path('audio-lab-bg-16-9.png'))

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('button.png')),
            Placement(0.23, 0.4),
            Placement(0.387, 0.567),
            self._a_clicked,
            key=Gdk.KEY_a
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('button.png')),
            Placement(0.23, 0.4),
            Placement(0.549, 0.567),
            self._s_clicked,
            key=Gdk.KEY_s
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('button.png')),
            Placement(0.23, 0.4),
            Placement(0.7215, 0.567),
            self._d_clicked,
            key=Gdk.KEY_d
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('console.png')),
            Placement(0.23, 0.4),
            Placement(0.5, 1.0)
        )

        scene.add_widget(
            ConsoleScreen(self, scene, self._ctl.next_stage, self.help_leds),
            Placement(0.5155, 0.918),
            Placement(0.5155, 0.918)
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('judoka.png')),
            Placement(0.23, 0.4),
            Placement(0.95, 0.9)
        )

        copy = 'Welcome to the sound lab!\nPress the keys to play sounds.'
        scene.add_widget(
            SpeechBubble(text=copy, source=SpeechBubble.BOTTOM, source_align=0.8),
            Placement(0.23, 0.4),
            Placement(0.95, 0.45)
        )

        return scene

    def _a_clicked(self):
        play_sound('/usr/share/kano-media/sounds/kano_error.wav', True)

    def _s_clicked(self):
        play_sound('/usr/share/kano-media/sounds/kano_achievement_unlock.wav', True)

    def _d_clicked(self):
        play_sound('/usr/share/kano-media/sounds/kano_init.wav', True)

    def _setup_help_leds(self):
        scene = Scene()
        scene.set_background(common_media_path('blueprint-bg-4-3.png'),
                             common_media_path('blueprint-bg-16-9.png'))

        scene.add_widget(
            Notebook(
                self,
                self.media_path('leds.png'), 0.8, 0.3,
                'Can you see the light?',
                ['If the power plugs are connected correctly,',
                 'you should see a blue light.'],
                [{'label': 'YES', 'callback': self.help_jack, 'color': 'green'},
                 {'label': 'NO', 'callback': self.help_power, 'color': 'red'}]
            ),
            Placement(0.5, 0.5, 0.0),
            Placement(0.45, 0.5, 0.0)
        )

        return scene

    def _setup_help_power(self):
        scene = Scene()
        scene.set_background(common_media_path('blueprint-bg-4-3.png'),
                             common_media_path('blueprint-bg-16-9.png'))

        scene.add_widget(
            Notebook(
                self,
                self.media_path('power.png'), 0.8, 0.5,
                'No light? Check the GPIO',
                ['The cable has to be connected to these',
                 'pins exactly.'],
                [{'label': 'NEXT', 'callback': self.help_jack, 'color': 'green'}]
            ),
            Placement(0.5, 0.5, 0.0),
            Placement(0.45, 0.5, 0.0)
        )

        return scene

    def _setup_help_jack(self):
        scene = Scene()
        scene.set_background(common_media_path('blueprint-bg-4-3.png'),
                             common_media_path('blueprint-bg-16-9.png'))

        scene.add_widget(
            Notebook(
                self,
                self.media_path('jack.png'), 1.0, 0.5,
                'Plug in the blue cable',
                ['If you see the light, it\'s powered!',
                 'Now plug the audio.'],
                [{'label': 'FINISHED', 'callback': self.first_scene, 'color': 'green'}]
            ),
            Placement(0.5, 0.5, 0.0),
            Placement(0.45, 0.5, 0.0)
        )

        return scene

class ConsoleScreen(Gtk.EventBox):
    def __init__(self, stage, scene, yes_cb, no_cb):
        super(ConsoleScreen, self).__init__()

        self.set_size_request(368*scene.scale_factor, 179*scene.scale_factor)
        add_class(self, 'console-screen')

        if scene.scale_factor > 0.8:
            add_class(self, 'font-large')
        else:
            add_class(self, 'font-small')

        vbox = Gtk.VBox(False, 0)
        vbox.set_halign(Gtk.Align.CENTER)
        #vbox.set_valign(Gtk.Align.CENTER)

        question = Gtk.Label('Can you hear the sound?')
        question.set_line_wrap(True)
        question.set_justify(Gtk.Justification.CENTER)
        question.set_valign(Gtk.Align.CENTER)
        add_class(question, 'console-screen-question')

        vbox.pack_start(question, True, False, 0)

        hbox = Gtk.HBox(False, 20)
        hbox.set_halign(Gtk.Align.CENTER)
        hbox.set_valign(Gtk.Align.CENTER)

        yes = KanoButton('YES')
        yes.connect('clicked', cb_wrapper, yes_cb)

        no = KanoButton('NO', color='red')
        no.connect('clicked', cb_wrapper, no_cb)

        hbox.pack_start(yes, False, False, 0)
        hbox.pack_start(no, False, False, 0)

        vbox.pack_start(hbox, True, False, 0)
        self.add(vbox)


class Notebook(Gtk.Overlay):
    def __init__(self, stage, image_path, image_scale, image_align, title, copy, buttons):
        super(Notebook, self).__init__()

        self.add(Gtk.Image.new_from_file(stage.media_path('notebook.png')))

        fixed = Gtk.Fixed()
        self.add_overlay(fixed)

        self._eb = Gtk.EventBox()
        add_class(self._eb, 'notebook-content-area')
        self._eb.set_size_request(415, 460)

        fixed.put(self._eb, 180, 70)

        vbox = Gtk.VBox(False, 0)
        vbox.set_vexpand(True)
        vbox.set_hexpand(True)
        vbox.set_margin_left(10)
        vbox.set_margin_right(10)

        img = scale_image(Gtk.Image.new_from_file(image_path), image_scale)
        img_align = Gtk.Alignment.new(image_align, 0.5, 0, 0)
        img_align.add(img)
        img_align.set_vexpand(True)
        img_align.set_hexpand(True)
        vbox.pack_start(img_align, False, False, 0)

        heading = Gtk.Label(title)
        add_class(heading, 'notebook-heading')

        copy_widgets = []
        for line in copy:
            l = Gtk.Label(line)
            l.set_line_wrap(False)
            l.set_justify(Gtk.Justification.CENTER)
            add_class(l, 'notebook-text')
            l.set_halign(Gtk.Align.CENTER)
            copy_widgets.append(l)

        # Pack heading
        vbox.pack_start(heading, False, False, 0)
        heading.set_margin_top(15)
        heading.set_margin_bottom(15)

        for w in copy_widgets:
            vbox.pack_start(w, False, False, 3)

        hbox = Gtk.HBox(False, 10)
        hbox.set_margin_top(15)
        hbox.set_halign(Gtk.Align.CENTER)
        for b in buttons:
            button = KanoButton(b['label'], color=b['color'])
            button.connect('clicked', cb_wrapper, b['callback'])
            hbox.pack_start(button, False, False, 0)
        vbox.pack_start(hbox, False, False, 0)

        self._eb.add(vbox)
