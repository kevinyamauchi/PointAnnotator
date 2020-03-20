from skimage import data

from pointannotator import point_annotator


point_annotator(data.astronaut(), labels=['Spaceship', 'Astronaut'])
