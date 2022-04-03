from dot_graph_builder import Builder, NodeStyles
from varname.helpers import Wrapper

b = Builder(name="Router")
b.set_node_style(NodeStyles.light_gray)

device = Wrapper("""device|
    const char* name;
    struct interface* interface;
    struct allocator* allocator;
    struct optimizer* optimizer;
    struct scheduler* scheduler;
    void* privacy;

""")
b.node(device)

print(b.source())
