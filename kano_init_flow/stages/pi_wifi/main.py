# The wifi world stage
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

from gi.repository import Gtk

from kano_init_flow.stage import Stage
from kano_init_flow.ui.scene import Scene, Placement, ActiveImage
from kano_init_flow.paths import common_media_path
from kano_init_flow.ui.speech_bubble import SpeechBubble
from kano.network import is_internet


class PiWifi(Stage):
    """
        The overscan setting window
    """

    id = 'pi-wifi'
    _root = __file__

    def __init__(self, ctl):
        super(PiWifi, self).__init__(ctl)

    def first_scene(self):

        if is_internet():
            self._ctl.set_var("has_internet", True)
            self._ctl.next_stage()
            return

        s = self._setup_first_scene()
        self._ctl.main_window.push(s)

    def next_stage(self):
        self._ctl.next_stage()

    def _setup_first_scene(self):

        self._scene = scene = Scene(self._ctl.main_window)
        scene.set_background(
            common_media_path('blueprint-bg-4-3.png'),
            common_media_path('blueprint-bg-16-9.png')
        )

        '''
        scene.add_arrow(
            "down",
            Placement(0.46, 0.31),
            Placement(0.46, 0.44)
        )

        scene.add_widget(
            ActiveImage(self.media_path('wifi.gif'),
                        hover=self.media_path('wifi-hover.gif')),
            Placement(0.48, 0.53),
            Placement(0.475, 0.6),
            self.next_stage
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('Pi-wifi.png')),
            Placement(0.83, 0),
            Placement(0.73, 0)
        )

        scene.add_widget(
            Gtk.Image.new_from_file(common_media_path('pi-judoka.png')),
            Placement(0.19, 0.6),
            Placement(0.18, 0.6)
        )

        sb = SpeechBubble('Let\'s set up WiFi',
                          scale=scene.scale_factor)
        scene.add_widget(
            sb,
            Placement(0.17, 0.32),
            Placement(0.165, 0.28)
        )
        '''

        scene.add_widget(
            Gtk.Image.new_from_file(common_media_path('pi-judoka.png')),
            Placement(0.5, 0.5),
            Placement(0.5, 0.5)
        )

        sb = SpeechBubble(_('Let\'s set up WiFi'),
                          source=SpeechBubble.BOTTOM,
                          scale=scene.scale_factor)
        scene.add_widget(
            sb,
            Placement(0.49, 0.2),
            Placement(0.49, 0.2)
        )

        # scene.schedule(20, self._show_hint, sb)
        scene.schedule(3, self.next_stage)

        return scene

    def _show_hint(self, sb):
        sb.set_text(_('Click on the green dongle\nto continue.'))
