#!MC 1410
# 2D contour plot, full page: 6.5 x 1.5 in frame, Times 12/10 pt, grid lines, legend
#
# Styles the active frame for a figure a full page wide. Axis titles, ranges, grid
# spacing and the contour levels belong to each plot: set them in Tecplot, then save
# the layout, which keeps the style too.
#
# Play: Scripting > Play Macro/Script, with the frame to style active.

# frame: no border, 6.5 x 1.5 in, its top left corner at (1, 0.25) in on the paper
$!FRAMELAYOUT
  SHOWBORDER = NO
  WIDTH = 6.5
  HEIGHT = 1.5
  XYPOS
    {
    X = 1
    Y = 0.25
    }

# plot area in % of the frame, leaving room for the axis titles and tick labels
# (about 0.6 in on the left, for tick labels such as 0.02, and 0.38 in at the
# bottom, as in the line styles); a border around it; x and y scaled independently,
# so a long thin domain fills the frame
$!TWODAXIS
  VIEWPORTPOSITION
    {
    X1 = 9
    Y1 = 26
    X2 = 95
    Y2 = 95
    }
  GRIDAREA
    {
    DRAWBORDER = YES
    }
  AXISMODE = INDEPENDENT

# x axis: title in Times 12 pt, tick labels in Times 10 pt (offsets in % of the
# frame), major grid lines; one minor tick between major ticks once the plot's tick
# spacing is set (while it is automatic, Tecplot picks the minor ticks)
$!TWODAXIS
  XDETAIL
    {
    TITLE
      {
      TEXTSHAPE
        {
        FONTFAMILY = 'Times'
        ISBOLD = NO
        SIZEUNITS = POINT
        HEIGHT = 12
        }
      OFFSET = 8
      }
    TICKLABEL
      {
      TEXTSHAPE
        {
        FONTFAMILY = 'Times'
        ISBOLD = NO
        SIZEUNITS = POINT
        HEIGHT = 10
        }
      OFFSET = 2
      }
    TICKS
      {
      NUMMINORTICKS = 1
      }
    GRIDLINES
      {
      SHOW = YES
      }
    }

# y axis: the same fonts, ticks and grid lines
$!TWODAXIS
  YDETAIL
    {
    TITLE
      {
      TEXTSHAPE
        {
        FONTFAMILY = 'Times'
        ISBOLD = NO
        SIZEUNITS = POINT
        HEIGHT = 12
        }
      OFFSET = 6
      }
    TICKLABEL
      {
      TEXTSHAPE
        {
        FONTFAMILY = 'Times'
        ISBOLD = NO
        SIZEUNITS = POINT
        HEIGHT = 10
        }
      }
    TICKS
      {
      NUMMINORTICKS = 1
      }
    GRIDLINES
      {
      SHOW = YES
      }
    }

# contour legend: shown at the top right (94, 94) in % of the frame, Times 10 pt,
# in a filled box
$!GLOBALCONTOUR 1
  LEGEND
    {
    SHOW = YES
    XYPOS
      {
      X = 94
      Y = 94
      }
    HEADERTEXTSHAPE
      {
      FONTFAMILY = 'Times'
      ISBOLD = NO
      SIZEUNITS = POINT
      HEIGHT = 10
      }
    NUMBERTEXTSHAPE
      {
      FONTFAMILY = 'Times'
      ISBOLD = NO
      SIZEUNITS = POINT
      HEIGHT = 10
      }
    ROWSPACING = 1
    BOX
      {
      BOXTYPE = FILLED
      MARGIN = 5
      }
    }

# show the whole paper with the frame on it
$!WORKSPACEVIEW FITALLFRAMES
$!REDRAW
