from typing import List

from dask_image.imread import imread
import napari
import numpy as np
from magicgui import magicgui

COLOR_CYCLE = [
        '#1f77b4',
        '#ff7f0e',
        '#2ca02c',
        '#d62728',
        '#9467bd',
        '#8c564b',
        '#e377c2',
        '#7f7f7f',
        '#bcbd22',
        '#17becf'
]


def create_label_menu(points_layer, labels):
    """Create a label menu widget that can be added to the napari viewer dock

    Parameters:
    -----------
    points_layer : napari.layers.Points
        a napari points layer
    labels : List[str]
        list of the labels for each keypoint to be annotated (e.g., the body parts to be labeled).

    Returns:
    --------
    label_menu : QComboBox
        the label menu qt widget
    """
    # Create the label selection menu
    @magicgui(label={'choices': labels})
    def label_selection(label):
        return label

    label_menu = label_selection.Gui()

    def update_label_menu(event):
        """Update the label menu when the point selection changes"""
        label_menu.label = points_layer.current_properties['label'][0]

    points_layer.events.current_properties.connect(update_label_menu)

    def label_changed(result):
        """Update the Points layer when the label menu selection changes"""
        selected_label = result
        current_properties = points_layer.current_properties
        current_properties['label'] = np.asarray([selected_label])
        points_layer.current_properties = current_properties

    label_menu.label_changed.connect(label_changed)

    return label_menu


def point_annotator(
        im_path: str,
        labels: List[str],
):
    """Create a GUI for annotating points in a series of images.

    Parameters
    ----------
    im_path : str
        glob-like string for the images to be labeled.
    labels : List[str]
        list of the labels for each keypoint to be annotated (e.g., the body parts to be labeled).
    """
    stack = imread(im_path)
    with napari.gui_qt():
        viewer = napari.view_image(stack)
        points_layer = viewer.add_points(
            properties={'label': labels},
            edge_color='label',
            edge_color_cycle=COLOR_CYCLE,
            symbol='o',
            face_color='transparent',
            edge_width=8,
            size=12,
        )
        points_layer.edge_color_mode = 'cycle'

        # add the label menu widget to the viewer
        label_menu = create_label_menu(points_layer, labels)
        viewer.window.add_dock_widget(label_menu)

        @viewer.bind_key('.')
        def next_label(event=None):
            """Keybinding to advance to the next label with wraparound"""
            current_properties = points_layer.current_properties
            current_label = current_properties['label'][0]
            ind = list(labels).index(current_label)
            new_ind = (ind + 1) % len(labels)
            new_label = labels[new_ind]
            current_properties['label'] = np.array([new_label])
            points_layer.current_properties = current_properties

        def next_on_click(layer, event):
            """Mouse click binding to advance the label when a point is added"""
            if layer.mode == 'add':
                next_label()

                # by default, napari selects the point that was just added
                # disable that behavior, as the highlight gets in the way
                layer.selected_data = {}

        points_layer.mode = 'add'
        points_layer.mouse_drag_callbacks.append(next_on_click)

        @viewer.bind_key(',')
        def prev_label(event):
            """Keybinding to decrement to the previous label with wraparound"""
            current_properties = points_layer.current_properties
            current_label = current_properties['label'][0]
            ind = list(labels).index(current_label)
            n_labels = len(labels)
            new_ind = ((ind - 1) + n_labels) % n_labels
            new_label = labels[new_ind]
            current_properties['label'] = np.array([new_label])
            points_layer.current_properties = current_properties
