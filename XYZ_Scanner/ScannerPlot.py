#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as N
import matplotlib.pyplot  as P
from mpl_toolkits.mplot3d import Axes3D


class VisualScanner( object ):
    """
    """
    def __init__(self,scanner,
                 **kwargs):
        """
        scanner: is a Scanner object from Scanner.py
        
        **kwargs: Goes to _new_axis_
        """
        
        self.scan = scanner
        self._scannerbounds = N.asarray([N.max(self.scan._x_range),
                                         N.max(self.scan._y_range),
                                         N.max(self.scan._z_range)])
        
        self._new_axis_(**kwargs)
        self._load_kwargs_()
        
        
        if "current_coords" in dir(self.scan):
            self.draw()
        
        self.fig.show()
        self.formerscatter
        
    # ------------------- #
    # - MAIN FUNCTIONS  - #
    # ------------------- #
    def draw(self,keep=False,
             show_history=True,
             Nhistory=5,Nforward=3):
        """
        """
        # -- Remove the former points -- #        
        if keep is False:
            self.remove_former_points()
            
        # -- The Current Point -- #        
        s = self.ax.scatter(*self.scan.current_coords,
                            **self.kwargs_current)
        self.formerscatter.append(s)
        # - Projection
        axis_projections = [self.ax.get_xlim()[0],
                            self.ax.get_ylim()[1],
                            self.ax.get_zlim()[0],
                            ]
        for i in range(3):
            toto = self.scan.current_coords.copy()
            toto[i] = axis_projections[i]
            s = self.ax.scatter(*toto,
                                **self.kwargs_projected)
            
            self.formerscatter.append(s)
        
        # -- The history / Forward -- #        
        if show_history:
            self.add_history(Nhistory=Nhistory)
            self.add_forward(Nforward=Nforward)
        
        self.fig.canvas.draw()

    # ------------------------- #
    # -- Sub Function of draw - #
    # ------------------------- #
    
    # -- Cleaning
    def remove_former_points(self):
        """
        """
        for s in self.formerscatter:
            s.remove()
        self.formerscatter = []

    # -- History points
    def add_history(self,Nhistory=5):
        """
        """
        for i,ch in enumerate(self.scan._coord_history[::-1]):
            if i > Nhistory-1:
                break
                
            alpha = 1-N.float(i+1)/Nhistory
            s = self.ax.scatter(*ch,
                                alpha=alpha,
                                **self.kwargs_history)
            self.formerscatter.append(s)
            
    # -- Forward points
    def add_forward(self,Nforward=3):
        """
        """
        for i,ch in enumerate(self.scan._coord_forward[::-1]):
            if i > Nforward-1:
                break
                
            alpha = 1-N.float(i+1)/Nforward
            s = self.ax.scatter(*ch,
                                alpha=alpha,
                                **self.kwargs_forward)
            self.formerscatter.append(s)

    # -- Box
    def draw_box(self,updatecanvas=True,
                 color=P.cm.binary(0.7),alpha=0.5,**kwargs):
        """
        """
        from itertools import product, combinations
        if "_box" not in dir(self):
            self._box = []
        else:
            self.remove_box(updatecanvas=False)
            
        r = [0, 1]
        for s, e in combinations(N.array(list(product(r,r,r))), 2):
            if N.sum(N.abs(s-e)) == r[1]-r[0]:                
                s = N.asarray(s)*self._scannerbounds
                e = N.asarray(e)*self._scannerbounds
                self._box.append(self.ax.plot3D(*zip(s,e),
                                                color=color,alpha=alpha,
                                                **kwargs)[0])
                
        if updatecanvas:
            self.fig.canvas.draw()
            
    def remove_box(self,updatecanvas=True):
        """
        """
        for b in self._box:
            b.remove()
        self._box = []
        
        if updatecanvas:
            self.fig.canvas.draw()
        
            
    # ------------------- #
    # - Low Level Tools - #
    # ------------------- #
    def _load_kwargs_(self):
        """
        """

        self.kwargs_current = {"facecolors":P.cm.Blues(0.7),
                               "edgecolors":P.cm.Blues(0.9),
                               "s":50}
        self.kwargs_projected = self.kwargs_current.copy()
        self.kwargs_projected["marker"] = "."
        self.kwargs_projected["alpha"] = 0.5
        
        self.kwargs_history = {"facecolors":P.cm.binary(0.4),
                               "edgecolors":P.cm.binary(0.6),
                               "s":40}
        self.kwargs_forward = {"facecolors":P.cm.Oranges(0.4),
                               "edgecolors":P.cm.Oranges(0.6),
                               "s":30}

        
    def _new_axis_(self,axin=None,rect=None,
                   draw_box=True,**kwarg_box):
        """
        """
        if axin is not None:
            self.ax  = axin
            self.fig = self.ax.figure
        else:
            self.fig = P.figure(figsize=[6,4])
            self.ax  = Axes3D(self.fig,rect=rect)

        self.ax.set_xlim(*self.scan._x_range[::-1])
        self.ax.set_ylim(*self.scan._y_range[::-1])
        self.ax.set_zlim(*self.scan._z_range[::-1])
        if draw_box:
            self.draw_box(**kwarg_box)
            
        
        self.formerscatter = []
        
