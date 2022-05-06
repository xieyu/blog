from dot_graph_builder import Builder, NodeStyles

from varname.helpers import Wrapper

b = Builder(name="op_registry")
b.set_node_style(NodeStyles.light_gray)

intialize_op_registry = Wrapper("""intialize_op_registry""")
b.node(intialize_op_registry)

internal_op_method_registry = Wrapper("""internal_op_method_registry""")
b.node(internal_op_method_registry, NodeStyles.tomato)

register_op_registry = Wrapper("""register_op_registry""")
b.node(register_op_registry)

initialize_op_name_registry = Wrapper("""initialize_op_name_registry""")
b.node(initialize_op_name_registry)

register_op = Wrapper("""register_op""")
b.node(register_op)

register_op_name = Wrapper("""register_op_name""")
b.node(register_op_name)

register_op_registry = Wrapper("""register_op_registry""")
b.node(register_op_registry)

push_vector_data = Wrapper("""push_vector_data""")
b.node(push_vector_data)

find_op_method = Wrapper("""find_op_method""")
b.node(find_op_method)

find_op_method_via_index = Wrapper("""find_op_method_via_index""")
b.node(find_op_method_via_index)

create_ir_node = Wrapper("""create_ir_node""")
b.node(create_ir_node)

destroy_ir_node = Wrapper("""destroy_ir_node""")
b.node(destroy_ir_node)

create_graph_node = Wrapper("""create_graph_node""")
b.node(create_graph_node)

load_graph_nodes = Wrapper("""load_graph_nodes""")
b.node(load_graph_nodes)

load_graph = Wrapper("""load_graph""")
b.node(load_graph)

b.edge(intialize_op_registry, [internal_op_method_registry])
b.edge(register_op_registry, [internal_op_method_registry])
b.edge(register_op,
       [intialize_op_registry, register_op_name, register_op_registry])

b.edge(register_op_name, [initialize_op_name_registry, push_vector_data])
b.edge(push_vector_data, [internal_op_method_registry])
b.edge(find_op_method, [internal_op_method_registry])
b.edge(find_op_method_via_index, [internal_op_method_registry])

b.edge(create_ir_node, [find_op_method])
b.edge(destroy_ir_node, [find_op_method])
b.edge(create_graph_node, [create_ir_node])
b.edge(load_graph_nodes, [create_ir_node])

b.edge(load_graph, [load_graph_nodes])
print(b.source())
