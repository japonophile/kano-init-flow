# The wifi world stage
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

from gi.repository import Gtk, GdkPixbuf

from kano_init_flow.stage import Stage
from kano_init_flow.ui.scene import Scene, Placement, SCREEN_WIDTH, \
    SCREEN_HEIGHT
from kano_init_flow.ui.speech_bubble import SpeechBubble
from kano_init_flow.ui.drag_classes import DragSource, DropArea
from kano_init_flow.ui.components import NextButton


class DragAndDrop(Stage):
    """
        The tutorial for drag and drop
    """

    id = 'drag-and-drop'
    _root = __file__

    def __init__(self, ctl):
        super(DragAndDrop, self).__init__(ctl)

    def first_scene(self):
        s1 = self._setup_first_scene()
        self._ctl.main_window.push(s1)

    def second_scene(self):
        s2 = self._setup_second_scene()
        self._ctl.main_window.push(s2)

    def _setup_first_scene(self):
        scene = Scene()
        scene.set_background(self.media_path('cliff-file-1600x1200.png'),
                             self.media_path('cliff-file-1920x1080.png'))

        char_pixbuf = GdkPixbuf.Pixbuf.new_from_file(
            self.media_path('judoka-clicked.png')
        )
        char_pixbuf = scene.scale_pixbuf_to_scene(char_pixbuf, 0.92, 0.96)
        judoka = Gtk.Image.new_from_file(self.media_path('cliff-judoka.png'))
        judoka = scene.scale_image_to_scene(judoka, 0.92, 0.96)
        speechbubble = SpeechBubble(
            text=_('Click on me,\nhold down the mouse button,\nand drag me across!'),
            source=SpeechBubble.LEFT,
            source_align=0.0,
            scale=scene.scale_factor
        )
        keyboard = Gtk.Image.new_from_file(self.media_path('Keyboard-Drag.gif'))

        drag_source = DragSource(judoka, char_pixbuf, speechbubble, keyboard)

        # Send the second cb to the scene
        drop_area = DropArea(self.second_scene)
        drop_area.set_size_request(
            0.35 * SCREEN_WIDTH, 0.5 * SCREEN_HEIGHT
        )

        scene.add_widget(
            keyboard,
            Placement(0.5, 1, 0),
            Placement(0.5, 1, 0)
        )

        scene.add_widget(
            speechbubble,
            Placement(0.34, 0.23),
            Placement(0.4, 0.23),
            name='speech'
        )

        scene.add_widget(
            drag_source,
            Placement(0.15, 0.25),
            Placement(0.25, 0.25)
        )

        scene.add_widget(
            drop_area,
            Placement(1, 0),
            Placement(1, 0)
        )

        scene.schedule(40, self._scene_1_hint, speechbubble)

        return scene

    def _scene_1_hint(self, speechbubble):

        speechbubble.set_text(
            _('Pick me up with the cursor\nand hold the left button down\n' +
            'while dragging me over.')
        )

    def _setup_second_scene(self):
        scene = Scene(self._ctl.main_window)
        scene.set_background(self.media_path('cliff-file-1600x1200.png'),
                             self.media_path('cliff-file-1920x1080.png'))

        scene.add_widget(
            SpeechBubble(text=_('Thanks!'), source=SpeechBubble.BOTTOM,
                         scale=scene.scale_factor),
            Placement(0.845, 0.08),
            Placement(0.895, 0.1)
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('cliff-judoka.png')),
            Placement(0.85, 0.3, 0.92),
            Placement(0.9, 0.35, 0.96)
        )

        #scene.add_widget(
        #    NextButton(),
        #    Placement(0.5, 0.7, 0),
        #    Placement(0.5, 0.7, 0),
        #    self._ctl.next_stage
        #    # key=Gdk.KEY_space
        #)

        scene.schedule(3, self._ctl.next_stage)

        return scene
