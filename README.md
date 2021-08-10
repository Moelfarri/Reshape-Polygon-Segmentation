# Reshape-Polygon-Segmentation
This algorithm uses OpenCV to demonstrate an example of how to let a user reshape a segmented polygon to their liking. If you are not happy with your initial segmentation whether the initial segmentation is done manually, by using a deep learning segmentation algorithm or some other traditional computer vision methods (edge detection, watershed segmentation etc), this algorithm is meant to supply the initial segmentation step so that the result is not completely thrown away.

This repository exists in two versions, a python notebook and a pythonscript. 

**How To Use The Interactive Window**
- Leftclick on green dots to modify segmentation at that particular point (enables EDIT_MODE)
- Double leftclick to verify final placement (disables EDIT_MODE)
- Press "d" when done and to see your final segmentation result

**Small Demo**


inspiration taken from https://github.com/saoalo/manual_polygon_drawer
