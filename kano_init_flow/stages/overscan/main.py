# The wifi world stage
#
# Copyright (C) 2015 Kano Computing Ltd.
# License: http://www.gnu.org/licenses/gpl-2.0.txt GNU GPL v2
#

from gi.repository import Gtk, Gdk

from kano.gtk3.buttons import KanoButton
from kano.utils import is_monitor, run_cmd
from kano_settings.system.display import get_overscan_status, \
    write_overscan_values, set_overscan_status, launch_pipe
from kano_profile.tracker import track_action


from kano_init_flow.stage import Stage
from kano_init_flow.ui.scene import Scene, Placement, ActiveImage
from kano_init_flow.paths import common_media_path
from kano_init_flow.ui.utils import add_class
from kano_init_flow.ui.css import apply_styling_to_screen
from kano_init_flow.ui.utils import cb_wrapper


class Overscan(Stage):
    """
        The overscan setting window
    """

    id = 'overscan'
    _root = __file__

    def __init__(self, ctl):
        super(Overscan, self).__init__(ctl)

        self._overscan_ctl = OverscanControl()

        apply_styling_to_screen(self.css_path('overscan.css'))

    def first_scene(self):
        if is_monitor():
            self._ctl.next_stage()
            return

        track_action('init-flow-overscan-needed')
        s1 = self._setup_first_scene()
        self._ctl.main_window.push(s1)

    def save_and_exit(self):
        self._overscan_ctl.reset() # TODO remove
        self._overscan_ctl.save_changes()
        self._ctl.next_stage()

    def _setup_first_scene(self):
        self._scene = scene = Scene(self._ctl.main_window)
        scene.set_background(common_media_path('blueprint-bg-4-3.png'),
                             common_media_path('blueprint-bg-16-9.png'))

        if scene.ratio == scene.RATIO_4_3:
            scene.add_widget(
                Gtk.Image.new_from_file(self.media_path('machine-4-3.png')),
                Placement(0, 0, 1),
                Placement(0, 0, 1)
            )
        else:
            scene.add_widget(
                Gtk.Image.new_from_file(self.media_path('machine-16-9.png')),
                Placement(0, 0, 1),
                Placement(0, 0, 1)
            )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('ok-button.png')),
            Placement(0.7, 0, 1),
            Placement(0.7, 0, 1),
            self.save_and_exit
        )

        scene.add_widget(
            Gtk.Image.new_from_file(self.media_path('help-button.png')),
            Placement(0.8, 0, 1),
            Placement(0.8, 0, 1),
            self.first_scene
        )

        scene.add_widget(
            ActiveImage(self.media_path('up-button.png'),
                        self.media_path('up-button.png'),
                        self.media_path('up-button.png')),
            Placement(0.5, 0.435, 1),
            Placement(0.51, 0.436, 1),
            self._overscan_ctl.zoom_out,
            key=Gdk.KEY_Up
        )

        scene.add_widget(
            ActiveImage(self.media_path('down-button.png'),
                        self.media_path('down-button.png'),
                        self.media_path('down-button.png')),
            Placement(0.5, 0.535, 1),
            Placement(0.51, 0.536, 1),
            self._overscan_ctl.zoom_in,
            key=Gdk.KEY_Down
        )

        self.show_notebook()

        return scene

    def show_notebook(self):
        self._scene.add_widget(
            Notebook(self, self.hide_notebook),
            Placement(0.45, 0.5, 0.0),
            Placement(0.45, 0.5, 0.0),
            modal=True,
            name='notebook'
        )

        self._overscan_ctl.disable()

    def hide_notebook(self):
        self._scene.remove_widget('notebook')
        self._overscan_ctl.enable()


class Notebook(Gtk.Overlay):
    def __init__(self, stage, next_cb):
        super(Notebook, self).__init__()

        self.add(Gtk.Image.new_from_file(stage.media_path('notebook.png')))

        fixed = Gtk.Fixed()
        self.add_overlay(fixed)

        self._eb = Gtk.EventBox()
        add_class(self._eb, 'notebook-content-area')
        self._eb.set_size_request(425, 570)

        fixed.put(self._eb, 200, 90)

        vbox = Gtk.VBox(False, 0)
        vbox.set_vexpand(True)
        vbox.set_hexpand(True)
        vbox.set_margin_left(10)
        vbox.set_margin_right(10)

        heading = Gtk.Label(_('Screen machine'))
        add_class(heading, 'heading')
        add_class(heading, 'notebook-heading')

        body_lines = [
            _("Use the up and down arrows on the"),
            _("keyboard to adjust the picture until the"),
            _("screen pushing machine lines up with the"),
            _("edges of your TV.")
        ]
        body_widgets = []
        for line in body_lines:
            body = Gtk.Label(line)
            body.set_line_wrap(False)
            body.set_justify(Gtk.Justification.LEFT)
            add_class(body, 'notebook-text')
            body.set_halign(Gtk.Align.START)
            body_widgets.append(body)

        # TODO: info
        legend_data = [
            {'icon': 'up-icon.png', 'desc': _('on your keyboard to increase')},
            {'icon': 'down-icon.png', 'desc': _('on your keyboard to decrease')},
            {'icon': 'ok-icon.png', 'desc': _('click the button to confirm')}
        ]
        legend_widgets = []
        for l in legend_data:
            legend = Gtk.HBox(False, 0)
            icon = Gtk.Image.new_from_file(stage.media_path(l['icon']))
            desc = Gtk.Label(l['desc'])
            add_class(desc, 'notebook-text')

            legend.pack_start(icon, False, False, 0)
            legend.pack_start(desc, False, False, 10)

            legend_widgets.append(legend)

        button = KanoButton(_('GO'))
        button.connect('clicked', cb_wrapper, next_cb)

        # Pack heading
        vbox.pack_start(heading, False, False, 10)
        heading.set_margin_bottom(20)

        for w in body_widgets:
            vbox.pack_start(w, False, False, 8)

        legend_widgets[0].set_margin_top(30)
        for w in legend_widgets:
            vbox.pack_start(w, False, False, 10)

        button.set_margin_top(30)
        vbox.pack_start(button, False, False, 0)

        self._eb.add(vbox)


class OverscanControl(object):
    def __init__(self):
        # launch_pipe()
        # The command below initialises the overscan pipe as root
        # TODO: This would be nice to refactor.
        run_cmd('sudo kano-init-flow-mknod')

        self._enabled = True
        self._step = 10
        self._original = get_overscan_status()
        self._current = get_overscan_status()

    def zoom_in(self):
        if self._enabled:
            if max(self._current.values()) < 250:
                self._change_overscan(self._step)

    def zoom_out(self):
        if self._enabled:
            self._change_overscan(-self._step)

    def reset(self, *_):
        """ Restore overscan if any changes were made """

        if self._original != self._current:
            self._current = self._original
            set_overscan_status(self._original)

    def enable(self):
        self._enabled = True

    def disable(self):
        self._enabled = False

    def save_changes(self):
        if self._original != self._current:
            write_overscan_values(self._current)

    def _change_overscan(self, change):
        """
        Increment (or decrement) the overscan setting
        :param change: Number to add to the overscan setting
        """

        for side, value in self._current.iteritems():
            # Do allow negative values
            self._current[side] = max(value + change, 0)

        set_overscan_status(self._current)
