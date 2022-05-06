from dot_graph_builder import Builder, NodeStyles
from varname.helpers import Wrapper

b = Builder(name="tengine")
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

interface = Wrapper("""interface|
int (*init)(struct device* device);
int (*pre_run)(struct device* device, struct subgraph* subgraph, void* options)
int (*run)(struct device* device, struct subgraph* subgraph);
int (*post_run)(struct device* device, struct subgraph* subgraph);
int (*async_run)(struct device* device, struct subgraph* subgraph);
int (*async_wait)(struct device* device, struct subgraph* subgraph, int try_wait);
int (*release_graph)(struct device* device, void* device_graph);
int (*release_device)(struct device* device);
""")
b.node(interface)

subgraph = Wrapper("""subgraph|
uint8_t index;
uint8_t input_ready_count;
uint8_t input_wait_count;
uint8_t input_num;
uint8_t output_num;
uint8_t status;
uint16_t node_num;
uint16_t* node_list;
uint16_t* input_tensor_list;
uint16_t* output_tensor_list;
struct graph* graph;
struct device* device;
void* device_graph;
""")
b.node(subgraph)

graph = Wrapper("""graph|
struct tensor** tensor_list;
struct node** node_list;
int16_t* input_nodes;
int16_t* output_nodes;
uint16_t tensor_num;
uint16_t node_num;
uint16_t input_num;
uint16_t output_num;
int8_t graph_layout;
int8_t model_layout;
int8_t model_format;
uint8_t status;
struct serializer* serializer;
void* serializer_privacy;
struct device* device;
void* device_privacy;
struct attribute* attribute;
struct vector* subgraph_list;
""")
b.node(graph)

tensor = Wrapper("""tensor""")
b.node(tensor, NodeStyles.tomato)

allocator = Wrapper("""allocator|
""")
b.node(allocator)

optimizer = Wrapper("""optimizer|
int (*split_graph)(struct graph* ir_graph);
int (*optimize_graph)(struct graph* ir_graph, int precision);
""")
b.node(optimizer)

allocator = Wrapper("""allocator|
int (*describe)(struct device*,
    struct vector* allowed_ops,
    struct vector* blocked_ops,
    struct vector* precision);

int (*evaluation)(struct device*,
    struct subgraph*,
    struct vector* tensors,
    struct vector* nodes);

int (*allocate)(struct device*, struct subgraph*);
int (*release)(struct device*, struct subgraph*);
""")
b.node(allocator)

scheduler = Wrapper("""scheduler|
const char* name;
int (*prerun)(struct scheduler*, struct graph*);
int (*run)(struct scheduler*, struct graph*, int block);
int (*wait)(struct scheduler*, struct graph*);
int (*postrun)(struct scheduler*, struct graph*);
void (*release)(struct scheduler*);
""")
b.node(scheduler)

node = Wrapper("""node|
    uint16_t index;
    uint8_t dynamic_shape;
    uint8_t input_num;
    uint8_t output_num;
    uint8_t node_type;
    int8_t subgraph_idx;

    uint16_t* input_tensors;
    uint16_t* output_tensors;

    char* name;
    struct op op;
    struct graph* graph;
""")
b.node(node)

serializer = Wrapper("""serializer|
    const char* (*get_name)(struct serializer*);
    int (*load_model)(struct serializer*, 
        struct graph*, 
        const char* fname, va_list ap);

    int (*load_mem)(struct serializer*,
        struct graph*,
        const void* addr,
        int size, va_list ap);

    int (*unload_graph)(struct serializer*,
        struct graph*, 
        void* s_priv,
        void* dev_priv);

    int (*register_op_loader)(struct serializer*,
        int op_type,
        int op_ver,
        void* op_load_func,
        void* op_type_map_func,
        void* op_ver_map_func);

    int (*unregister_op_loader)(struct serializer*,
        int op_type, 
        int op_ver,
        void* op_load_func);

    int (*init)(struct serializer*);

    int (*release)(struct serializer*);
""")
b.node(serializer)

op = Wrapper("""op|
    uint16_t type;
    uint8_t version;
    uint8_t same_shape;
    uint16_t param_size;
    void* param_mem;
    int (*infer_shape)(struct node*);
""")
b.node(op, NodeStyles.tomato)

b.edge(device, [interface, subgraph, optimizer, allocator, scheduler])
b.edge(subgraph, graph)
b.edge(interface, subgraph)
b.edge(graph, [tensor, node, serializer])
b.edge(scheduler, [graph])
b.edge(optimizer, [graph])
b.edge(allocator, subgraph)
b.edge(node, [op])

print(b.source())
