from skimage import data

from pointannotator import point_annotator

im_path = '/Users/yamauc0000/Documents/DeepLabCut/examples/openfield-Pranav-2018-10-30/labeled-data/m4s1/*.png'
output = '/Users/yamauc0000/Documents/PointAnnotator/examples/anno.csv'
point_annotator(im_path, labels=['ear_l', 'ear_r', 'tail'], output_path=output)
