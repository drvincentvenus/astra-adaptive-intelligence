#!/usr/bin/env python3
"""Regenerate Figure 1 in Nature Medicine schematic style: 180 mm double column, Helvetica/Arial 7-8 pt, bold lowercase panel letters, flat muted fills, thin outlines, no commentary text inside the figure (metric and numbers belong in the legend). Outputs PNG 600 dpi, PDF and SVG."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch
plt.rcParams.update({"font.family":"sans-serif","font.sans-serif":["Helvetica Neue","Helvetica","Arial","Liberation Sans","DejaVu Sans"],"font.size":7,"pdf.fonttype":42,"svg.fonttype":"none"})
MM=1/25.4
if __name__=="__main__":
    W,H=180,88  # mm
    fig=plt.figure(figsize=(W*MM,H*MM)); ax=fig.add_axes([0,0,1,1]); ax.set_xlim(0,W); ax.set_ylim(0,H); ax.axis("off")
    ink="#000000"; line="#4d4d4d"; grey_fill="#e6e6e6"; blue_fill="#c6dbef"; green_fill="#c7e9c0"; red_fill="#fcbba1"; red="#cb181d"; mid="#969696"
    def box(x,y,w,h,text,fc=grey_fill,fs=7,bold=False):
        ax.add_patch(Rectangle((x,y),w,h,fc=fc,ec=line,lw=0.6))
        ax.text(x+w/2,y+h/2,text,ha="center",va="center",fontsize=fs,color=ink,fontweight="bold" if bold else "normal",linespacing=1.2)
    def arrow(x0,y0,x1,y1,color=line,ls="-",lw=0.7):
        ax.add_patch(FancyArrowPatch((x0,y0),(x1,y1),arrowstyle="-|>",mutation_scale=7,color=color,lw=lw,linestyle=ls,shrinkA=0,shrinkB=0))
    bh=13; ya=62; yb=20
    # panel a
    ax.text(3,ya+bh+7,"a",fontsize=8,fontweight="bold",color=ink,va="center"); ax.text(8,ya+bh+7,"Written vignette",fontsize=7,color=ink,va="center")
    box(3,ya,34,bh,"Patient described\nin the text\n(murmur written)",fc=blue_fill); arrow(37,ya+bh/2,44,ya+bh/2)
    box(44,ya,40,bh,"Formalised knowledge\n(criteria, guidelines)"); arrow(84,ya+bh/2,91,ya+bh/2)
    box(91,ya,30,bh,"Answer correct",fc=green_fill); arrow(121,ya+bh/2,128,ya+bh/2,color=mid)
    box(128,ya,49,bh,"Endocarditis found\n14 of 14 runs",fc=green_fill,bold=True)
    # panel b
    ax.text(3,yb+bh+7,"b",fontsize=8,fontweight="bold",color=ink,va="center"); ax.text(8,yb+bh+7,"Hidden chart, model must ask",fontsize=7,color=ink,va="center")
    box(3,yb,26,bh,"Triage line only"); arrow(29,yb+bh/2,36,yb+bh/2)
    box(36,yb,40,bh,"Model asks, examines,\norders",fc=blue_fill); arrow(76,yb+bh/2,83,yb+bh/2)
    box(83,yb,38,bh,"Primary diagnosis secured\n(answer correct)",fc=green_fill)
    ax.plot([124.5,124.5],[yb-5,yb+bh+5],color=red,lw=1.0,ls=(0,(3,2)))
    ax.text(124.5,yb-7.5,"assessment closed,\nactions unused",ha="center",va="top",fontsize=6.5,color=red,linespacing=1.15)
    arrow(121,yb+bh/2,128,yb+bh/2,color=mid,ls=(0,(2,2)))
    box(128,yb,49,bh,"Heart never auscultated\n0 of 12 runs",fc=red_fill,bold=True)
    # migration arrow from panel a answer to panel b builder
    ax.annotate("",xy=(66,yb+bh+1.5),xytext=(106,ya-1.5),arrowprops=dict(arrowstyle="-|>",color=red,lw=0.9,mutation_scale=8,connectionstyle="arc3,rad=0.25"))
    ax.text(108,(ya+yb+bh)/2+1,"Residual error moves from the answer\nto the picture of the patient",fontsize=6.5,color=red,ha="left",va="center",linespacing=1.15)
    fig.savefig("Fig1_error_migration.png",dpi=600,facecolor="white")
    fig.savefig("Fig1_error_migration.pdf",facecolor="white"); fig.savefig("Fig1_error_migration.svg",facecolor="white")
    print("Fig1 regenerated: 180 x 88 mm, 600 dpi")
