// Gmsh .geo file produced by qmesh version 1.0.2 (git sha key: 2b8dedeabca736f73d8b3990b614bad76101d8e3).
// Date,time file written (yyyy/mm/dd, hour:minute:second): 2018/12/13 , 09:02:08

// Definitions of 4 points:
Point( 0 ) = {846258.166547,5844731.33704,0.0 };
Point( 1 ) = {805390.592314,5864132.9269,0.0 };
Point( 2 ) = {841912.543728,5866766.6377,0.0 };
Point( 3 ) = {809077.787434,5837225.26126,0.0 };

// Definitions of 1 B-splines:
Line( 0 ) = {1, 3, 0, 2, 1};

// Definitions of 1 line-loops:
Line Loop( 1 ) = {0};

// Definitions of 1 surfaces:
Plane Surface( 0 ) = {1};

// Definitions of 1 physical line ID`s:
Physical Line( 666 ) = {0};

// Definitions of 1 physical surface ID`s:
Physical Surface( 1 ) = {0};

Mesh.CharacteristicLengthExtendFromBoundary = 0;
Field[1] = Structured;
Field[1].FileName = "distance.fld";
Field[1].TextFormat = 1;
Field[2] = MathEval;
Field[2].F = "2000*Tanh((F1+5)/1000)";

Field[3] = MathEval;
Field[3].F = "2000.0";

Field[666] = Min;
Field[666].FieldsList = {2, 3};

Background Field = 666;
