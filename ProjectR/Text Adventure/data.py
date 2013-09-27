# XML Parser/Data Access Object C:\Users\wrinehart\PycharmProjects\ProjectR\Text Adventure\data.py
"""AUTO-GENERATED Source file for C:\\Users\\wrinehart\\PycharmProjects\\ProjectR\\Text Adventure\\data.py"""
import xml.sax
import Queue
import Q2API.xml.base_xml

rewrite_name_list = ("name", "value", "attrs", "flatten_self", "flatten_self_safe_sql_attrs", "flatten_self_to_utf8", "children")

def process_attrs(attrs):
    """Process sax attribute data into local class namespaces"""
    if attrs.getLength() == 0:
        return {}
    tmp_dict = {}
    for name in attrs.getNames():
        tmp_dict[name] = attrs.getValue(name)
    return tmp_dict

def clean_node_name(node_name):
    clean_name = node_name.replace(":", "_").replace("-", "_").replace(".", "_")

    if clean_name in rewrite_name_list:
        clean_name = "_" + clean_name + "_"

    return clean_name

class inspect_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 4
        self.path = [None, u'map', u'area', u'exit']
        Q2API.xml.base_xml.XMLNode.__init__(self, "inspect", attrs, None, [])

class interact_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 4
        self.path = [None, u'map', u'area', u'exit']
        Q2API.xml.base_xml.XMLNode.__init__(self, "interact", attrs, None, [])

class description_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 3
        self.path = [None, u'map', u'area']
        Q2API.xml.base_xml.XMLNode.__init__(self, "description", attrs, None, [])

class exit_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 3
        self.path = [None, u'map', u'area']
        self.interact = []
        self.inspect = []
        Q2API.xml.base_xml.XMLNode.__init__(self, "exit", attrs, None, [])

class object_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 3
        self.path = [None, u'map', u'area']
        self.interact = []
        self.inspect = []
        Q2API.xml.base_xml.XMLNode.__init__(self, "object", attrs, None, [])

class revisit_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 3
        self.path = [None, u'map', u'area']
        Q2API.xml.base_xml.XMLNode.__init__(self, "revisit", attrs, None, [])

class timeup_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 3
        self.path = [None, u'map', u'area']
        Q2API.xml.base_xml.XMLNode.__init__(self, "timeup", attrs, None, [])

class area_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 2
        self.path = [None, u'map']
        self.object = []
        self.description = []
        self.revisit = []
        self.timeup = []
        self.exit = []
        Q2API.xml.base_xml.XMLNode.__init__(self, "area", attrs, None, [])

class intro_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 2
        self.path = [None, u'map']
        Q2API.xml.base_xml.XMLNode.__init__(self, "intro", attrs, None, [])

class map_q2class(Q2API.xml.base_xml.XMLNode):
    def __init__(self, attrs):
        self.level = 1
        self.path = [None]
        self.area = []
        self.intro = []
        Q2API.xml.base_xml.XMLNode.__init__(self, "map", attrs, None, [])

class NodeHandler(xml.sax.handler.ContentHandler):
    """SAX ContentHandler to map XML input class/object"""
    def __init__(self, return_q):     # overridden in subclass
        self.obj_depth = [None]
        self.return_q = return_q
        self.last_processed = None
        self.char_buffer = []
        xml.sax.handler.ContentHandler.__init__(self)   # superclass init

    def startElement(self, name, attrs): # creating the node along the path being tracked
        """Override base class ContentHandler method"""
        name = clean_node_name(name)
        p_attrs = process_attrs(attrs)

        if name == "":
            raise ValueError, "XML Node name cannot be empty"

        elif name == "map":
            self.obj_depth.append(map_q2class(p_attrs))

        elif name == "object":
            self.obj_depth.append(object_q2class(p_attrs))

        elif name == "description":
            self.obj_depth.append(description_q2class(p_attrs))

        elif name == "area":
            self.obj_depth.append(area_q2class(p_attrs))

        elif name == "interact":
            self.obj_depth.append(interact_q2class(p_attrs))

        elif name == "inspect":
            self.obj_depth.append(inspect_q2class(p_attrs))

        elif name == "revisit":
            self.obj_depth.append(revisit_q2class(p_attrs))

        elif name == "timeup":
            self.obj_depth.append(timeup_q2class(p_attrs))

        elif name == "intro":
            self.obj_depth.append(intro_q2class(p_attrs))

        elif name == "exit":
            self.obj_depth.append(exit_q2class(p_attrs))

        self.char_buffer = []
        self.last_processed = "start"

    def endElement(self, name): # need to append the node that is closing in the right place
        """Override base class ContentHandler method"""
        name = clean_node_name(name)

        if (len(self.char_buffer) != 0) and (self.last_processed == "start"):
            self.obj_depth[-1].value = "".join(self.char_buffer)

        if name == "":
            raise ValueError, "XML Node name cannot be empty"

        elif name == "map":
            # root node is not added to a parent; stays on the "stack" for the return_object
            self.char_buffer = []
            self.last_processed = "end"
            return

        elif name == "object":
            self.obj_depth[-2].object.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "description":
            self.obj_depth[-2].description.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "area":
            self.obj_depth[-2].area.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "interact":
            self.obj_depth[-2].interact.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "inspect":
            self.obj_depth[-2].inspect.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "revisit":
            self.obj_depth[-2].revisit.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "timeup":
            self.obj_depth[-2].timeup.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "intro":
            self.obj_depth[-2].intro.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        elif name == "exit":
            self.obj_depth[-2].exit.append(self.obj_depth[-1]) #  make this object a child of the next object up...
            self.obj_depth[-2].children.append(self.obj_depth[-1]) #  put a reference in the children list as well
            self.obj_depth.pop() # remove this node from the list, processing is complete
            self.char_buffer = []

        self.last_processed = "end"


    def characters(self, in_chars):
        """Override base class ContentHandler method"""
        self.char_buffer.append(in_chars)

    def endDocument(self):
        """Override base class ContentHandler method"""
        self.return_q.put(self.obj_depth[-1])

def obj_wrapper(xml_stream):
    """Call the handler against the XML, then get the returned object and pass it back up"""
    try:
        return_q = Queue.Queue()
        xml.sax.parseString(xml_stream, NodeHandler(return_q))
        return (True, return_q.get())
    except Exception, e:
        return (False, (Exception, e))


