#!/usr/bin/env python
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import pylab
import random
import argparse


parser = argparse.ArgumentParser()

parser.add_argument("--abvlines",
                  nargs='+',
                  dest="abvlines",
                  help="Vertincal lines")

parser.add_argument("--noyaxis",
                  dest="noyaxis",
                  action="store_true",default=False,
                  help="Hide y-axsis")

parser.add_argument("--tick_line_length",
                  dest="tick_line_length",
                  type=float,
                  default=2,
                  help="Tick line width")

parser.add_argument("--tick_line_width",
                  dest="tick_line_width",
                  type=float,
                  default=0.5,
                  help="Tick line width")

parser.add_argument("--axis_line_width",
                  dest="axis_line_width",
                  type=float,
                  default=0.5,
                  help="Axis line width")

parser.add_argument("--axis_label_size",
                  dest="axis_label_size",
                  type=int,
                  default=8,
                  help="Axis label font size")

parser.add_argument("--tick_label_size",
                  dest="tick_label_size",
                  type=int,
                  default=8,
                  help="Axis tick label font size")

parser.add_argument("--density",
                  dest="density",
                  action="store_true",default=False,
                  help="Plot density")

parser.add_argument("--xticks",
                  dest="xticks",
                  help="CSV ints to tick and label")

parser.add_argument("--xtick_names",
                  dest="xtick_names",
                  help="CSV of xtick lables")


parser.add_argument("--numyticks",
                  dest="numyticks",
                  help="Number of Y ticks")

parser.add_argument("-t",
                  "--title",
                  dest="title",
                  help="Title")

parser.add_argument("-x",
                  "--xlabel",
                  dest="xlabel",
                  help="X axis label")

parser.add_argument("-y",
                  "--ylabel",
                  dest="ylabel",
                  help="Y axis label")

parser.add_argument("-o",
                  "--output_file",
                  dest="output_file",
                  help="Data file",
                  required=True)

parser.add_argument("-b",
                  "--bins",
                  dest="bins",
                  default=10,
                  help="Number of bins or csv of bins")

parser.add_argument("--x_max",
                  dest="max_x",
                  type=float,
                  help="Max x value")


parser.add_argument("--x_min",
                  dest="min_x",
                  type=float,
                  help="Min x value")

parser.add_argument("--y_max",
                  dest="max_y",
                  type=float,
                  help="Max y value")


parser.add_argument("--y_min",
                  dest="min_y",
                  type=float,
                  help="Min y value")

parser.add_argument("--color",
                  dest="color",
                  default=None,
                  help="Bar color")

parser.add_argument("-c",
                  "--column",
                  dest="col",
                  type=int,
                  default="0",
                  help="Column in the data")

parser.add_argument("-d",
                  "--delim",
                  dest="delim",
                  default="\t",
                  help="Field delimiter")

parser.add_argument("-l",
                  "--ylog",
                  action="store_true",default=False,
                  dest="ylog",
                  help="Set y-axis to be log scale")

parser.add_argument("--xlog",
                  action="store_true",default=False,
                  dest="xlog",
                  help="Set x-axis to be log scale")

parser.add_argument("--x_sci",
                  action="store_true",default=False,
                  dest="x_sci",
                  help="Use scientific notation for x-axis")

parser.add_argument("--y_sci",
                  action="store_true",default=False,
                  dest="y_sci",
                  help="Use scientific notation for y-axis")

parser.add_argument("--width",
                  dest="width",
                  type=float,
                  default=5,
                  help="Figure width")

parser.add_argument("--height",
                  dest="height",
                  type=float,
                  default=5,
                  help="Figure height")

parser.add_argument("--black",
                  action="store_true", 
                  default=False,
                  dest="black",
                  help="black background")

args = parser.parse_args()

Y=[]
for l in sys.stdin:
    a = l.rstrip().split(args.delim)
    if len(a) == 1:
        if len(a[args.col]) != 0 :
            Y.append(float(a[args.col]))

matplotlib.rcParams.update({'font.size': 12})
#fig = matplotlib.pyplot.figure(figsize=(10,5),dpi=300)

#fig = matplotlib.pyplot.figure(figsize=(args.width,args.height),dpi=300)

if args.black:
    fig = matplotlib.pyplot.figure(\
            figsize=(args.width,args.height),\
            dpi=300,\
            facecolor='black')
else:
    fig = matplotlib.pyplot.figure(\
            figsize=(args.width,args.height),\
            dpi=300)



fig.subplots_adjust(wspace=.05,left=.01,bottom=.01)

x_max = max(Y)
x_min = min(Y)

if args.max_x:
    x_max = args.max_x
if args.min_x:
    x_min = args.min_x

if args.black:
    ax = fig.add_subplot(1,1,1,facecolor='k')
else:
    ax = fig.add_subplot(1,1,1)

bins = None
if ',' in str(args.bins):
    bins = [int(x) for x in args.bins.split(',')]
else:
    bins = int(args.bins)

h = ax.hist(Y, \
            bins,
            density=args.density,
            log=args.ylog, \
            histtype='bar', \
            rwidth=0.8, \
            color=args.color)

print(h)

if args.xlog:
    ax.set_xscale('log')

#labels, counts = np.unique(Y, return_counts=True)
#print labels
#ax.bar(labels, counts, align='center')
#plt.gca().set_xticks(labels)


if args.max_x:
    ax.set_xlim(xmax=args.max_x)
if args.min_x:
    ax.set_xlim(xmin=args.min_x)
if args.max_y:
    ax.set_ylim(ymax=args.max_y)
if args.min_y:
    ax.set_ylim(ymin=args.min_y)

if args.x_sci:
    formatter = matplotlib.ticker.ScalarFormatter()
    formatter.set_powerlimits((-2,2))
    ax.xaxis.set_major_formatter(formatter)

if args.y_sci:
    formatter = matplotlib.ticker.ScalarFormatter()
    formatter.set_powerlimits((-2,2))
    ax.yaxis.set_major_formatter(formatter)

if args.xlabel:
    ax.set_xlabel(args.xlabel, fontsize=args.axis_label_size)

if args.ylabel:
    ax.set_ylabel(args.ylabel, fontsize=args.axis_label_size)

if args.title:
    ax.set_title(args.title)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(True)
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')

if args.xticks:
    xticks = [int(x) for x in args.xticks.split(',')]
    xmajorlocator = matplotlib.ticker.FixedLocator(xticks)
    ax.xaxis.set_major_locator(xmajorlocator)

if args.xtick_names:
    xtick_locs = []
    xtick_names = []

    i = 0
    for xtick_name in args.xtick_names.split(','):
        if xtick_name != '':
            xtick_locs.append(i)
            xtick_names.append(xtick_name)
        i+=1

    xmajorlocator = matplotlib.ticker.FixedLocator(xtick_locs)
    ax.xaxis.set_major_locator(xmajorlocator)
    ax.set_xticklabels(xtick_names)

if args.black:
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.title.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.xaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

ax.tick_params(axis='both',
               which='major',
               labelsize=args.axis_label_size,
               width=args.tick_line_width,
               length=args.tick_line_length)

ax.spines['bottom'].set_linewidth(args.axis_line_width)
ax.spines['left'].set_linewidth(args.axis_line_width)

if args.noyaxis:
    ax.spines['left'].set_visible(False)
    ax.yaxis.set_ticklabels([])
    ax.set_yticks([], minor=True)
    ax.set_yticks([])

if args.abvlines:
    for abvline in args.abvlines:
        #position, text, color, size = args.abvline.split(',')
        ax.axvline(float(abvline), color='red')
       # ax.text(float(position) + \
       #         (ax.get_xlim()[1]-ax.get_xlim()[0])*0.05,\
       #         ax.get_ylim()[1],
       #         text,
       #         va='top',\
       #         fontsize=float(size),\
       #         color=color)


if args.black:
    matplotlib.pyplot.savefig(args.output_file,bbox_inches='tight',\
            facecolor=fig.get_facecolor(),\
              transparent=True)
else:
    matplotlib.pyplot.savefig(args.output_file,bbox_inches='tight')
