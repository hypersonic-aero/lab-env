#!MC 1410
# XY line plot, full page: 6.5 x 1.25 in frame, Times 12/10 pt, grid lines, legend
#
# Styles the active frame for a figure a full page wide. Axis titles, ranges and
# grid spacing belong to each plot: set them in Tecplot, then save the layout,
# which keeps the style too.
#
# Play: Scripting > Play Macro/Script, with the frame to style active.

# frame: no border, 6.5 x 1.25 in, its top left corner at (1, 0.25) in on the paper
$!FRAMELAYOUT
  SHOWBORDER = NO
  WIDTH = 6.5
  HEIGHT = 1.25
  XYPOS
    {
    X = 1
    Y = 0.25
    }

# plot area in % of the frame, leaving room for the axis titles and tick labels;
# a border around it
$!XYLINEAXIS
  VIEWPORTPOSITION
    {
    X1 = 7
    Y1 = 30
    X2 = 96
    Y2 = 87
    }
  GRIDAREA
    {
    DRAWBORDER = YES
    }

# x axis: title in Times 12 pt, tick labels in Times 10 pt (offsets in % of the
# frame), major and minor grid lines; one minor tick between major ticks once the
# plot's tick spacing is set (while it is automatic, Tecplot picks the minor ticks)
$!XYLINEAXIS
  XDETAIL 1
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
      OFFSET = 17
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
      OFFSET = 6
      }
    TICKS
      {
      NUMMINORTICKS = 1
      }
    GRIDLINES
      {
      SHOW = YES
      }
    MINORGRIDLINES
      {
      SHOW = YES
      }
    }

# y axis: the same fonts, ticks and grid lines
$!XYLINEAXIS
  YDETAIL 1
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
      OFFSET = 4
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
    MINORGRIDLINES
      {
      SHOW = YES
      }
    }

# legend: shown, Times 10 pt, in a white box without a visible outline (COLOR is
# the outline, the fill is white)
$!GLOBALLINEPLOT
  LEGEND
    {
    SHOW = YES
    TEXTSHAPE
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
      COLOR = WHITE
      MARGIN = 0
      }
    }

# show the whole paper with the frame on it
$!WORKSPACEVIEW FITALLFRAMES
$!REDRAW
