﻿﻿# Introduction



Netdim is a network design and planning software. Created in April 2016, it is still at an early stage of its development.
A network in NetDim is made of:
- devices (router, optical switch, host machine or antenna)
- physical links (<a href="https://en.wikipedia.org/wiki/Link_aggregation">trunks</a>)
- routes
- traffic links
- [autonomous systems] (https://en.wikipedia.org/wiki/Autonomous_system_%28Internet%29) (AS)

A physical link in NetDim is called a trunk: 
it represents a set of physical links aggregated together. 
An autonomous system is a set of devices exchanging routing and signalization messages to carry the incoming traffic. 
The path of a data flow inside an AS depends on the [protocol] (https://en.wikipedia.org/wiki/Communications_protocol) used
in the AS.

![Netdim](https://github.com/mintoo/networks/raw/master/Readme/introduction.PNG)

# To be done

## Algorithms
- [ ] Kruskal and Prim to find the minimum spanning tree
- [ ] Minimum cut. Useful to find the bottleneck of the network, and also to partition the graph before applying a visualisation algorithm if the graph is too big. 
- [ ] K-means before graph drawing if the graph is too big.
- [ ] Edmond-Karps and Dinic to find the maximum flow (instead of Ford-Fulkerson)
- [ ] Bellman-Ford
- [ ] Loop detection algorithm with BFS
- [ ] K equal-cost links/links&amp;nodes-disjoint shortest paths (can be done with BFS in a first step)
- [ ] Suurbale to find the shortest links/links&amp;nodes-disjoint loop
- [ ] Bhandari algorithm to compare with Suurbale
- [ ] Fruchterman-Reingold: make it work. (velocity divergence to infinity so far)
- [ ] Use CPLEX and Genetic algorithm to solve RWA simle version
- [ ] Improved Suurbale/Bhandari to find the K (maximally) edge/edge&nodes disjoint paths

## Links
- [x] Possibility to change the cost of a link (UD-metric)
- [ ] Interface. Metrics depends on the interface for OSPF, RSTP, etc
- [ ] Different type of physical link: WDM Fiber, ETH, etc. Color per type of link.

## Canvas-related tasks
- [x] Multiple selection: all nodes/links contained in a rectangle
- [x] Icons for devices instead of a tkinter oval
- [x] Multiple nodes/links deletion
- [x] Dijkstra must consider the cost of the links
- [x] Fix the zoom that doesn't work well (zooming and unzooming)
- [x] Left-clicking on an object updates the property window if it is deiconified
- [x] Hide/show display per type of objects
- [ ] Draw an arc instead of a straigth line when there are several links between two nodes. 
The angle must depend on the number of links.
- [ ] Change the mouse pointeur when going over an object
- [ ] Per-layer 3D display with nodes duplication
- [ ] Modified Dijkstra to find the longest path/widest path
- [ ] Capacity label display: should be with an arrow
- [ ] Protection highlight: highlight first the protection path's links, then the working path's.
- [ ] Generate text and shapes on the canvas

## Routing
- [x] Traffic link routing. All nodes that belongs to an AS should be excluded.
- [ ] BGP routing
- [ ] subnet and filtering system on routes/traffic link
- [ ] G8032 ring with RPL protection
- [ ] Ring AS with steering/wrapping protection mode
- [ ] Dimensioning with Maximally redundant tree
- [ ] OSPF: route leaking, multi-ABR, multi-area links, etc (RFC 5086, ...)

## Protection
- [ ] FRR implementation for MPLS. A LSP can have a protection mode (Local Detour to Merge point, Local Detour to Destination, Next-Hop protection) or a user-defined back-up LSP.
- [ ] Protection by pruning the failed link(s): dimensioning considering IGP convergence
- [ ] Highlight the protection path with a different color
- [ ] K-failure AS dimensioning
- [ ] Failure simulation system to see where the traffic is going. Route's protection path highlight.

## AS
- [ ] Highlight all elements of a domain
- [ ] Improve the AS management window. Button with arrows instead of add/remvoe edge
- [ ] Add to/remove from AS should be done graphically only: no need for buttons.
- [ ] Use the K-shortest paths for load-balancing at the edge of an AS

## Other
- [x] Scenario system with multiple scenarii 
- [x] Possibiliy to rename objects
- [x] Delete scenario
- [ ] Scenario duplication
- [ ] Drawing for a selection of nodes only
- [ ] Add new devices: simple switch (non optical), firewall, splitter, regenerator/amplifier
- [ ] Message window (display log) + error window: catch error
- [ ] Dockable frame system
- [ ] Add regex for sanity checks in all user input entry boxes
- [ ] Network links/nodes statistics with plotlib: number of links per type, etc
- [ ] Save the default drawing parameters when modified. Update the window.
- [ ] compute the optimal pairwise distance for the spring length
- [ ] IP address management on interface.
- [ ] Help menu for links, nodes input
- [ ] Common top-level window for node property display to avoid having several windows at once
- [ ] Keyboard shortcut: Ctrl, Suppr, Ctrl Z/Y, etc
- [ ] Interface: could be a little oval at the end of a physical links
- [ ] Convert tk drop-down list into ttk combo box
- [ ] Graph generation: select the type of nodes
- [ ] Add new types of graph
- [ ] Treeview to display the list of object of the network
- [ ] when clicking on a link, window displaying all routes / traffic link mapped on it
- [ ] Right-click of the tree view equivalent to a right-click on the canvas
- [ ] Menu to generate complex graph: hypercube, square tiling in a special window
- [ ] Modify customlistbox to avoid the line to retrieve the index
- [ ] Merge Add to AS and Manage AS window 
- [ ] Delete AS button
- [ ] Use haversine formula to compute the distance of a link based on GPS coordinates

## Import/Export/Save
- [x] Import and export the graph with CSV
- [x] Import and export the graph with excel
- [ ] Consider all scenario when saving/opening a saved project
- [ ] Allow to import the property of nodes, so that they can be efficiently modified in excel for a big graph
- [ ] Save all scenario
- [ ] Import Export all scenario
- [ ] Import GML format and provide all files from the topology zoo
