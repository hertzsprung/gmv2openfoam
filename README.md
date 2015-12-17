# gmv2openfoam
Convert GMV meshes to OpenFOAM meshes.  This allows 2D cut cell meshes produced by [ASAM](https://www.tropos.de/en/research/projects-infrastructures-technology/technology-at-tropos/numerical-modeling/asam/) to be used in [OpenFOAM](http://www.openfoam.org/).

There are four steps to create an OpenFOAM mesh:

1. Generate a .out.gmvG file using the ASAM grid generator
2. Create plain text files for points, faces and cells using `gmvread`
3. Use `gmv2obj.py` to convert these text files to an [obj](https://en.wikipedia.org/wiki/Wavefront_.obj_file) file
4. Use OpenFOAM's `extrudeMesh` with `extrudeModel plane` to create the 2D mesh

The GMV reader C library was taken from [libMesh](https://github.com/libMesh/libmesh/tree/master/contrib/gmv).
