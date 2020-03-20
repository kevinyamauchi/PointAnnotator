from enum import Enum
from itertools import cycle
from typing import List

import napari
import numpy as np
from magicgui import magicgui


def point_annotator(im: np.ndarray, labels: List[str]):
    with napari.gui_qt():
        viewer = napari.view_image(im)
        default_properties = {'label': np.array(labels)}
        points_layer = viewer.add_points(
            properties={'label': np.empty(0)},
            default_properties=default_properties,
            symbol='o',
            face_color='transparent',
            edge_width=8,
            edge_color='label',
            size=12,
        )
        points_layer.edge_color_mode = 'cycle'

        Labels = Enum('Labels', labels)

        # Create the label selection menu
        @magicgui()
        def label_selection(label=Labels[labels[0]]):
            return label
        label_menu = label_selection.Gui()

        def label_changed(result):
            """Update the Points layer when the label menu selection changes"""
            selected_label = result.name
            points_layer.current_properties = {'label': np.asarray([selected_label])}

        def update_label_menu(event):
            """Update the label menu when the point selection changes"""
            label = points_layer.current_properties['label'][0]
            index = label_menu.label_widget.findText(label)
            label_menu.label_widget.setCurrentIndex(index)

        # connect the events and add the label menu widget
        points_layer.events.current_properties.connect(update_label_menu)
        label_menu.label_changed.connect(label_changed)
        viewer.window.add_dock_widget(label_menu)
