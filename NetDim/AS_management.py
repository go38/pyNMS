# NetDim
# Copyright (C) 2016 Antoine Fourmy (antoine.fourmy@gmail.com)
# Released under the GNU General Public License GPLv3

import area
import tkinter as tk
from tkinter import ttk
from miscellaneous import ObjectListbox, FocusTopLevel

class ASManagement(FocusTopLevel):
    
    def __init__(self, scenario, AS, imp):
        super().__init__()
        self.scenario = scenario
        self.AS = AS
        self.failed_trunk = None
        self.title("Manage AS")
        self.obj_type = ("trunk", "node", "edge") 
        self.area_listbox = ("area names", "area trunks", "area nodes")
        
        self.label_name = ttk.Label(self, text="AS name")
        self.label_id = ttk.Label(self, text="AS ID")
        self.label_type = ttk.Label(self, text="AS Type")
        
        self.str_name = tk.StringVar()
        self.entry_name  = tk.Entry(self, textvariable=self.str_name, width=10)
        self.str_name.set(AS.name)
        self.str_id = tk.StringVar()
        self.entry_id  = tk.Entry(self, textvariable=self.str_id, width=10)
        self.str_id.set(AS.id)
        
        # the type of a domain cannot change after domain creation.
        self.AS_type = ttk.Label(self, text=AS.type)
        
        # interface to cost dictionnary. This is used for OSPF and IS-IS, 
        # because the cost of a trunk depends on the bandwidth.
        # Trunk_cost = Ref_BW / BW
        self.if_to_cost = {
        "FE": 10**7,
        "GE": 10**8,
        "10GE": 10**9,
        "40GE": 4*10**9,
        "100GE":10**10
        }
        
        # find edge nodes of the AS
        self.button_update_cost = ttk.Button(self, text="Update costs", 
                                command=lambda: self.update_cost())
        self.button_update_cost.grid(row=1, column=0, pady=5, padx=5, sticky="w")    
        
        self.button_update_topo = ttk.Button(self, text="Update topology", 
                                command=lambda: self.update_AS_topology())
        self.button_update_topo.grid(row=2, column=0, pady=5, padx=5, sticky="w")       
        
        self.label_name.grid(row=0, column=2, pady=5, padx=5, sticky="e")
        self.label_id.grid(row=1, column=2, pady=5, padx=5, sticky="e")
        self.label_type.grid(row=2, column=2, pady=5, padx=5, sticky="e")
        self.entry_name.grid(row=0, column=4, pady=5, padx=5, sticky="w")
        self.entry_id.grid(row=1, column=4, pady=5, padx=5, sticky="w")
        self.AS_type.grid(row=2, column=4, pady=5, padx=5, sticky="w")
        
        # listbox of all AS objects
        self.dict_listbox = {}
        for index, type in enumerate(self.obj_type):
            lbl = tk.Label(self, bg="#A1DBCD", text="".join(("AS ",type,"s")))
            listbox = ObjectListbox(self, activestyle="none", width=15, height=7)
            self.dict_listbox[type] = listbox
            yscroll = tk.Scrollbar(self, 
                    command=self.dict_listbox[type].yview, orient=tk.VERTICAL)
            listbox.configure(yscrollcommand=yscroll.set)
            listbox.bind("<<ListboxSelect>>", 
                            lambda e, type=type: self.highlight_object(e, type))
            lbl.grid(row=3, column=2*index)
            listbox.grid(row=4, column=2*index)
            yscroll.grid(row=4, column=1+2*index, sticky="ns")
            
        # populate the listbox with all objects from which the AS was created
        for obj_type in ("trunk", "node", "edge"):
            for obj in AS.pAS[obj_type]:
                self.dict_listbox[obj_type].insert(obj)
                            
        # listbox for areas
        for index, type in enumerate(self.area_listbox):
            lbl = tk.Label(self, bg="#A1DBCD", text=type.title())
            listbox = ObjectListbox(self, activestyle="none", width=15, height=7)
            self.dict_listbox[type] = listbox
            yscroll = tk.Scrollbar(self, 
                    command=self.dict_listbox[type].yview, orient=tk.VERTICAL)
            listbox.configure(yscrollcommand=yscroll.set)
            if type == "area names":
                listbox.bind("<<ListboxSelect>>", 
                            lambda e: self.display_area(e))
            else:
                listbox.bind("<<ListboxSelect>>", 
                            lambda e, type=type: self.highlight_object(e, type))
            lbl.grid(row=6, column=2*index)
            listbox.grid(row=7, column=2*index)
            yscroll.grid(row=7, column=1+2*index, sticky="ns")
        
        # find edge nodes of the AS
        self.button_find_edge_nodes = ttk.Button(self, text="Find edges", 
                                command=lambda: self.find_edge_nodes())
                                
        self.button_create_route = ttk.Button(self, text="Create route", 
                                command=lambda: self.create_routes())
        
        # find domain trunks: the trunks between nodes of the AS
        self.button_find_trunks = ttk.Button(self, text="Find trunks", 
                                command=lambda: self.find_trunks())
        
        # operation on nodes
        self.button_remove_node_from_AS = ttk.Button(self, text="Remove node", 
                                command=lambda: self.remove_selected("node"))
                                
        self.button_add_to_edges = ttk.Button(self, text="Add to edges", 
                                command=lambda: self.add_to_edges())
                                
        self.button_remove_from_edges = ttk.Button(self, text="Remove edge", 
                                command=lambda: self.remove_from_edges())
                                
        # button to create an area
        self.button_create_area = ttk.Button(self, text="Create area", 
                                command=lambda: area.CreateArea(self))
                                
        # button to delete an area
        self.button_delete_area = ttk.Button(self, text="Delete area", 
                                command=lambda: self.delete_area())
                                
        # combobox for the user to change the protection type
        self.var_pct_type = tk.StringVar()
        self.pct_type_list = ttk.Combobox(self, 
                                    textvariable=self.var_pct_type, width=20)
        self.pct_type_list["values"] = (
                                       "IGP convergence", 
                                       "FRR ECMP", 
                                       "FRR LFA"
                                       )
        self.var_pct_type.set("IGP convergence")
        
        # buttons under the trunks column
        self.button_create_route.grid(row=5, column=0)
        self.button_find_trunks.grid(row=6, column=0)
        
        # button under the nodes column
        self.button_remove_node_from_AS.grid(row=5, column=2)
        self.button_add_to_edges.grid(row=6, column=2)
        self.button_remove_from_edges.grid(row=7, column=2)
        
        # button under the edge column
        self.button_find_edge_nodes.grid(row=5, column=4)
        self.button_remove_from_edges.grid(row=6, column=4)
            
        # button under the area column
        self.button_create_area.grid(row=8, column=0)
        self.button_delete_area.grid(row=9, column=0)
        
        # protection type drop-down list
        # self.pct_type_list.grid(row=1, column=6)
        
        # at first, the backbone is the only area: we insert it in the listbox
        self.dict_listbox["area names"].insert("Backbone")
        
        # hide the window when closed
        self.protocol("WM_DELETE_WINDOW", self.withdraw)
        
        # if the AS is created from an import, close the management window
        if imp: 
            self.withdraw()
        
    ## Functions used directly from the AS Management window
        
    # function to highlight the selected object on the canvas
    def highlight_object(self, event, obj_type):
        selected_object = self.dict_listbox[obj_type].selected()
        selected_object = self.scenario.ntw.of(name=selected_object, _type=obj_type)
        self.scenario.unhighlight_all()
        self.scenario.highlight_objects(selected_object)
        
    # remove the object selected in "obj_type" listbox from the AS
    def remove_selected(self, obj_type):
        # remove and retrieve the selected object in the listbox
        selected_obj = self.dict_listbox[obj_type].pop_selected()
        # remove it from the AS as well
        self.AS.remove_from_AS(self.scenario.ntw.of(name=selected_obj, _type=obj_type))
        
    def add_to_edges(self):
        selected_node = self.dict_listbox["node"].selected()
        self.dict_listbox["edge"].insert(selected_node) 
        selected_node = self.scenario.ntw.nf(name=selected_node)
        self.AS.add_to_edges(selected_node)
            
    def remove_from_edges(self):
        selected_edge = self.dict_listbox["edge"].pop_selected()
        selected = self.scenario.ntw.nf(name=selected_edge) 
        self.AS.remove_from_edges(selected)
        
    def add_to_AS(self, area, *objects):
        self.AS.add_to_AS(self.AS.areas[area], *objects)
        for obj in objects:
            self.dict_listbox[obj.network_type].insert(obj)
            
    def find_edge_nodes(self):
        self.dict_listbox["edge"].clear()
        for edge in self.scenario.ntw.find_edge_nodes(self.AS):
            self.dict_listbox["edge"].insert(edge)
            
    def find_trunks(self):
        trunks_between_domain_nodes = set()
        for node in self.AS.pAS["node"]:
            for neighbor, adj_trunk in self.scenario.ntw.graph[node]["trunk"]:
                if neighbor in self.AS.pAS["node"]:
                    trunks_between_domain_nodes.add(adj_trunk)
        self.add_to_AS("Backbone", *trunks_between_domain_nodes)
        
    def create_routes(self):
        
        self.update_AS_topology()
        
        for eA in self.AS.pAS["edge"]:
            for eB in self.AS.pAS["edge"]:
                if eA != eB and eB not in self.AS.routes[eA]:
                    name = "->".join((str(eA), str(eB)))
                    route = self.scenario.ntw.lf(link_type="route", 
                                                        name=name, s=eA, d=eB)
                    _, route.path = self.AS.algorithm(eA, eB, self.AS)
                    route.AS = self.AS
                    self.AS.pAS["route"].add(route)
                    self.scenario.create_link(route)
                    
    def trigger_failure(self, trunk):
        self.failed_trunk = trunk
        self.failure_traffic()
                    
    def failure_traffic(self):
        for trunk in self.AS.pAS["trunk"]:
            trunk.trafficSD = trunk.trafficDS = 0.
        # this function is used for failure simulation. When a link is set in
        # failure, the traffic property display the traffic going over the link
        # considering this failure case.
        # It is also used when removing the failure, to update the trunk traffic 
        # back to the "normal mode" traffic
        for route in self.AS.pAS["route"]:
            s, d = route.source, route.destination
            prec_node = s
            ft = self.failed_trunk
            # if there is no failed trunk or the failed trunk is not on the
            # normal patf of the route, we consider the normal route
            if not ft or ft not in route.path:
                traffic_path = route.path
            else:
                traffic_path = route.r_path[ft]
            # if there is no link in failure, we add the route traffic 
            # of the trunk (normal dimensioning), but if there is a failure,
            # we add the traffic to the recovery path instead
            for trunk in traffic_path:
                sd = (trunk.source == prec_node)*"SD" or "DS"
                trunk.__dict__["traffic" + sd] += route.traffic
                # update of the previous node
                prec_node = trunk.source if sd == "DS" else trunk.destination
                    
    def link_dimensioning(self):
        for route in self.AS.pAS["route"]:
            s, d = route.source, route.destination
            for trunk in route.path:
                # list of allowed trunks: all AS trunks but the failed one
                a_t = self.AS.pAS["trunk"] - {trunk}
                if self.var_pct_type.get() == "IGP convergence":
                    # apply the AS routing algorithm, ignoring the failed trunk
                    _, recovery_path = self.AS.algorithm(s, d, self.AS, a_t=a_t)
                    route.r_path[trunk] = recovery_path
                elif self.var_pct_type.get() == "FRR ECMP":
                    pass

        # we call failure traffic, knowing that link dimensioning is 
        # called during "calculate all", and all failed trunk have been
        # previously reseted.
        # this means that failure traffic will trigger the normal procedure,
        # and the traffic computation will not consider any failure case.
        self.failure_traffic()
            
        # finally, we must compute the worst case traffic, that is the 
        # maximum amount of traffic that can be sent on the link, 
        # considering all possible failure cases
        # we initialize it to the normal case traffic which is a lower bound
        # of the worst case traffic.
        for trunk in self.AS.pAS["trunk"]:
            trunk.wctrafficSD = trunk.trafficSD
            trunk.wctrafficDS = trunk.trafficDS
            
        for failed_trunk in self.AS.pAS["trunk"]:
            # we create a dict of trunk, that contains for all trunks the 
            # resulting traffic, considering that failed_trunk is in failure
            trunk_traffic = {trunk: {"SD": 0, "DS": 0} 
                                        for trunk in self.AS.pAS["trunk"]}
            
            for route in self.AS.pAS["route"]:
                prec_node = route.source
                if failed_trunk not in route.path:
                    traffic_path = route.path
                else:
                    traffic_path = route.r_path[failed_trunk]
                for trunk in traffic_path:
                    sd = (trunk.source == prec_node)*"SD" or "DS"
                    trunk_traffic[trunk][sd] += route.traffic
                    # update of the previous node
                    prec_node = trunk.source if sd == "DS" else trunk.destination
            # we add the resulting traffic for the given failure case considered
            # to all_traffic, which contains all such resulting traffic
            for trunk in trunk_traffic:
                for sd in ("SD", "DS"):
                    new_wctraffic = trunk_traffic[trunk][sd]
                    if new_wctraffic > getattr(trunk, "wctraffic" + sd):
                        setattr(trunk, "wctraffic" + sd, new_wctraffic)
                
    def update_AS_topology(self):
        
        self.AS.border_routers.clear()
        # for OSPF, we reset all area nodes, for IS-IS, all area trunks
        if self.AS.type == "ISIS":
            self.AS.areas["Backbone"].pa["trunk"].clear()
        elif self.AS.type == "OSPF":
            self.AS.areas["Backbone"].pa["node"].clear()
        
        for node in self.AS.pAS["node"]:
            
            # In IS-IS, a router has only one area
            if self.AS.type == "ISIS":
                node_area ,= node.AS[self.AS]
                
            # in OSPF, a router is considered ABR if it has attached
            # trunks that are in different area. Since we just updated 
            # the router's areas, all we need to check is that it has
            # at least 2 distinct areas.
            # an ABR is automatically part of the backbone area.
            elif self.AS.type == "OSPF":
                if len(node.AS[self.AS]) > 1:
                    self.AS.border_routers.add(node)
                    self.AS.areas["Backbone"].add_to_area(node)
            
            for neighbor, adj_trunk in self.scenario.ntw.graph[node]["trunk"]:
                
                # A multi-area IS-IS AS is defined by the status of its nodes.
                # we automatically update the trunk area status, by considering 
                # that a trunk belong to an area as soon as both of its ends do.
                # A trunk between two L1/L2 routers that belong to different
                # areas will be considered as being part of the backbone.
                if self.AS.type == "ISIS":
                    # we check that the neighbor belongs to the AS
                    if self.AS in neighbor.AS:
                        # we retrieve the neighbor's area
                        neighbor_area ,= neighbor.AS[self.AS]
                        # if they are the same, we add the trunk to the area
                        if node_area == neighbor_area:
                            node_area.add_to_area(adj_trunk)
                        # if not, it is at the edge of two areas
                        # a router is considered L1/L2 if it has at least
                        # one neighbor which is in a different area.
                        else:
                            # we consider that the trunk belongs to the backbone,
                            # for interfaces to have IP addresses.
                            self.AS.areas["Backbone"].add_to_area(adj_trunk)
                            self.AS.border_routers.add(node)

                # OTOH, a multi-area OSPF AS is defined by the area of its trunk.
                # we automatically update the node area status, by considering that a 
                # node belongs to an area as soon as one of its adjacent trunk does.
                elif self.AS.type == "OSPF":
                    for area in adj_trunk.AS[self.AS]:
                        area.add_to_area(node)
                        

                
    def update_cost(self):
        for trunk in self.AS.pAS["trunk"]:
            bw = self.if_to_cost[trunk.interface]
            # the cost of a link cannot be less than 1. This also means that,
            # by default, all interfaces from GE to 100GE will result in the
            # same metric: 1.
            cost = max(1, self.AS.ref_bw / bw)
            trunk.costSD = trunk.costDS = cost
            
    def create_area(self, name, id):
        self.AS.area_factory(name, id)
        self.dict_listbox["area names"].insert(name)

    def delete_area(self):
        selected_area_name = self.dict_listbox["area names"].pop_selected()
        selected_area = self.AS.area_factory(name=selected_area_name)
        self.AS.delete_area(selected_area)
                
    def display_area(self, event):
        area = self.dict_listbox["area names"].selected()
        area = self.AS.area_factory(area)
        self.scenario.unhighlight_all()
        self.scenario.highlight_objects(*(area.pa["node"] | area.pa["trunk"]))
        self.dict_listbox["area nodes"].clear()
        self.dict_listbox["area trunks"].clear()
        for node in area.pa["node"]:
            self.dict_listbox["area nodes"].insert(node)
        for trunk in area.pa["trunk"]:
            self.dict_listbox["area trunks"].insert(trunk)
            
    ## Functions used to modify AS from the right-click menu
    
    def add_to_area(self, area, *objects):
        self.AS.areas[area].add_to_area(*objects)
            
    def remove_from_area(self, area, *objects):
        self.AS.areas[area].remove_from_area(*objects)
                
    def remove_from_AS(self, *objects):
        self.AS.remove_from_AS(*objects)
        for obj in objects:
            if obj.network_type == "node":
                # remove the node from nodes/edges listbox
                self.dict_listbox["node"].pop(obj)
                self.dict_listbox["edge"].pop(obj)
            elif obj.network_type == "trunk":
                self.dict_listbox["trunk"].pop(obj)