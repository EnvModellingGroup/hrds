import sys
sys.path.insert(0,"../../")

from hrds import HRDS

points = []
with open("test_mesh.csv",'r') as f:
    for line in f:
        row = line.split(",")
        # grab X and Y
        points.append([float(row[0]), float(row[1])])

bathy = HRDS("gebco_uk.tif", 
             rasters=("emod_utm.tif", 
                      "inspire_data.tif"), 
             distances=(700, 200))
bathy.set_bands()

print len(points)

with open("output.xyz","w") as f:
    for p in points:
        f.write(str(p[0])+"\t"+str(p[1])+"\t"+str(bathy.get_val(p))+"\n")

