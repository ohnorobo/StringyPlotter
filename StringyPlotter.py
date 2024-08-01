import numpy as np
from scipy.spatial.distance import cdist
from PIL import Image
import sys
from pprint import pprint

input_image = sys.argv[1]
output_image = sys.argv[2]
divisor = int(sys.argv[3])
skip_paths_longer_than = int(sys.argv[4])

i = Image.open(input_image)
ii = np.array(i)
iii = np.where(ii==1)
iiii = np.column_stack(list(reversed(iii)))
iiiii = iiii[np.random.choice(iiii.shape[0],iiii.shape[0]//divisor,replace=False),:]

the_first = iiiii[0]
first_mask  = np.ones(iiiii.shape[0], dtype=bool)
first_mask[[0]] = False
the_rest = iiiii[first_mask]
point_collection = np.array([the_first])
distance_collection = np.array([0])

for x in range(iiiii.shape[0]-1):
    all_distances = cdist(the_rest, [the_first])
    next_distance = np.min(all_distances)
    distance_match = np.where(all_distances == next_distance)[0][0]
    found_next = the_rest[distance_match]

    #pprint(("distance", next_distance))
    #pprint(("coll", distance_collection))
    
    point_collection = np.concatenate([point_collection,np.array([found_next])])
    distance_collection = np.concatenate([distance_collection,np.array([next_distance])])
    
    next_mask  = np.ones(the_rest.shape[0], dtype=bool)
    next_mask[[distance_match]] = False
    next_rest  = the_rest[next_mask]
    next_first = found_next
    the_first = found_next
    the_rest  = next_rest

svg_template = '<svg width="{}" height="{}" xmlns="http://www.w3.org/2000/svg">{}</svg>'
path_template = '<path d="{}" fill="none" stroke="black" />"'
move_template = 'M {} {} '
line_template = 'L {} {} '


pprint(("points", point_collection))
pprint(("distances", distance_collection))

path_string = move_template.format(*point_collection[0])
for p, d in zip(point_collection[1:], distance_collection[1:]):
    # TODO if distance is too long use a move instead of a line

    if d > skip_paths_longer_than:
        path_string += move_template.format(*p)
    else:
        path_string += line_template.format(*p)

final_svg = svg_template.format(
        i.width,
        i.height,
        path_template.format(path_string)
        )

with open(output_image,'w') as f:
    f.write(final_svg)

