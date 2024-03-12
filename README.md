# sgview
python stereogram as 3D anaglyph viewer
## Description
`sgview` (stereogram viewer) is a python script that converts standard, full color 2D stereogram image pairs into 3D anaglyphs that can be viewed with appropriate color filter glasses.  
Below is an example of a possible stereogram input followed by the processed *red-cyan* and *trioscopic* anaglyphs.  
  
**Input:**  
[stereogram example](examples/stereograms/stereograph.jpg)
  
**Output:**  
[red_cyan example](examples/anaglyphs/stereograph-red_cyan.jpg) [trioscopic example](examples/anaglyphs/stereograph-triscopic.jpg)  
  
## Usage
Run `sgview.py -h` to display the detailed syntax information. 
## How it works
`sgview` utilizes the `opencv-python` library to read, manipulate, and write image data. The purpose of this script is to allow its user to store stereogram image pairs in their raw, color-unaltered form, and only generate a 3D anaglyph when needed. This way of "3D" image storage is independent of the viewer's color filter combination and also preserves the original image pair for use in other methods of stereogram display.

### Stereogram pairs
A stereogram image pair is an image containing two separate views of the same subject, captured ideally at the exact same point in time but with a slight horizontal separation. To obtain the illusion of depth perception, each eye of the viewer is only allowed to see one of the two images.  
A simple way to achieve this on a standard 2D surface such as a screen or a print is to place a differently colored filter in front of each eye *(3D glasses)*, and adjust the color channels of each image accordingly.  
This process by nature alters and outright loses some of the color information, and often is far from perfect, resulting in ghosting and noticeable "double vision".  The color filters may also differ depending on the type of 3D glasses used; for example the most popular "red-cyan" anaglyphs will not work with the less often used "green-magenta (trioscopic)" glasses, even though the base method is the same. For these reasons - and those explained in the above section - it is better practice to store the color stereogram pairs containing both unaltered views and only generate an anaglyph composite *on the go*. This also has the added advantage of allowing viewers without special lenses to see the image without the anaglyph color distortion in the way.

### Image input
The input for `sgview` can be any standard image file format that contains the two perspectives. The most simple kind of this "double image" - and what `sgview` defaults to - are the two perspectives of equal size and aspect ratio side by side. The program can then just split any input down the middle and use its left side for the left eye and the right side for the right eye to create a functional anaglyph (assuming that the two perspectives have been correctly aligned by the author).  
There are however plenty of cases where this method isn't applicable. For example, most historical stereograms that can be found on the Internet are digital scans of physical paper photographs, often including information labels around the two views, scanned at a slight angle, and with the two views not being perfectly aligned and separated down the middle. Whenever an image input is being loaded by `sgview`, it checks for a second file of the same name but with an appended `.csv` extension (e.g. when `image.png` is being loaded, `image.png.csv` is looked for).  
This file can contain the pixel coordinates of the four corners of each view (so eight entries total), which `sgview` then uses to align the two views no matter how separated, rotated, skewed, or offset they are, even relative to each other. This for example allows historical stereogram scans to be stored in their original form while the program still knows how to compose a 3D anaglyph from them.  
If you wish to define your own stereograms, a detailed description of this supplemental file format can be found in a later secion.  

### Image output
The output created by `sgview` is a file called `sgview.png` that is saved in the system's temporary directory, from where it can be loaded by the system's default image viewer or an internet browser (on Windows it can be accessed as `%TEMP%/sgview.png`). If you wish to save this output permanently, simply copy it to any directory you want.

## Creating stereograms
The following section will be a brief description on how to create stereograms compatible with `sgview`. It assumes that you are already familiar with the process of capturing a stereo photograph from two angles (or rendering two 3D views, etc).

### Side by side
As mentioned above, the simplest way to create a stereogram viewable by this script is to just save your two perspectives side by side as any standard image file. As long as both halves are the exact same size and aspect ratio, a 3D anaglyph image should be generated. Left half of the image is used for the left eye, right half for the right eye. These kinds of images do not need a supplemental `.csv` file.

### From coordinates
If the two views in the stereogram are not perfectly aligned as two matching halves, and you do not wish to alter the original in any way to align them, a supplemental `.csv` file can be created that defines the coordinates of the four corners of each view. This file needs to have the exact same name as the image file it belongs to, so for example `image.png` will have an `image.png.csv` supplemental file. If the name doesn't match, the file will simply be ignored as if it wasn't there and the "side to side" will be used instead.  
The first eight rows of the `.csv` file are mapped to the eight total corners, with each row having two columns, one for the `x` and the other for the `y` coordinate. They are mapped in the following format:  

    LEFT_TOP_LEFT_X , LEFT_TOP_LEFT_Y
    LEFT_BOTTOM_LEFT_X , LEFT_BOTTOM_LEFT_Y
    LEFT_BOTTOM_RIGHT_X , LEFT_BOTTOM_RIGHT_Y
    LEFT_TOP_RIGHT_X , LEFT_TOP_RIGHT_Y
    RIGHT_TOP_LEFT_X , RIGHT_TOP_LEFT_Y
    RIGHT_BOTTOM_LEFT_X , RIGHT_BOTTOM_LEFT_Y
    RIGHT_BOTTOM_RIGHT_X , RIGHT_BOTTOM_RIGHT_Y
    RIGHT_TOP_RIGHT_X , RIGHT_TOP_RIGHT_Y
These coordinates are subsequently used to perform a perspective transform, which "straightens" each view into a square/rectangle, allowing them to be overlaid. There are several examples of this in the `examples/stereograms/` directory.  
It may be difficult to get the alignment right when using the coordinates, so it is recommended to double-check it using a program like GIMP or Photoshop, draw a bounding box with four corners around each view, and manually performing the perspective transform.

### Anaglyph types
The `sgv_types.csv` file contains the pre-defined anaglyph types that can be selected using the `-a` argument. If no argument is given, the first entry in this file is used. Each row starts with the name of the anaglyph, followed by six float numbers between 0 and 1. These define the RGB values of the color filters. For example, the entry  

    red_cyan,1,0,0,0,1,1
defines an anaglyph type called `red_cyan`, with the left filter RGB set to `1,0,0` (pure red) and right channel RGB to `0,1,1` (pure green+blue = cyan).
