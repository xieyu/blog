from types import BuiltinFunctionType
from dot_graph_builder import Builder, NodeStyles
from graphviz import dot
from varname.helpers import Wrapper

b = Builder(name="Router")
b.set_node_style(NodeStyles.light_gray)

Router_route = Wrapper("""Router.route|
注册path路由
处理函数
""")
b.node(Router_route)

Router_call = Wrapper("""Router.call""")
b.node(Router_call)

Router_call_route = Wrapper("""Router.call_route""")
b.node(Router_call_route)

Node_insert = Wrapper("""Node.insert""")
b.node(Node_insert)

Node_path_to_route_id_insert = Wrapper("""Node.path_to_route_id.insert""")
b.node(Node_path_to_route_id_insert)

Node_route_id_to_path = Wrapper("""Node.route_id_to_path""")
b.node(Node_route_id_to_path)

Node_routers_insert = Wrapper("""Node.routers.insert""")
b.node(Node_routers_insert)

Node_routers = Wrapper("""Node.routers|
    routes: HashMap<RouteId, Endpoint<B>>,
 """)
b.node(Node_routers, NodeStyles.tomato)

Service = Wrapper("""Service|
impl<B> Service<Request<B>> for Router<B>{
    fn call(&mut self, mut req: Request<B>)
    -> Self::Future {...}
}
""")
b.node(Service)

MethodRouter_call = Wrapper("""MethodRouter.call|
调用用户注册handler
""")
b.node(MethodRouter_call)

RouteFuture = Wrapper("""RouteFuture|
    pub struct RouteFuture<B, E> {
        #[pin]
        future: Oneshot<
            BoxCloneService<Request<B>, Response, E>,
            Request<B>,
        >,
        strip_body: bool,
    }
""")
b.node(RouteFuture)

b.edge(Router_route, Node_insert)
b.edge(
    Node_insert,
    [Node_path_to_route_id_insert, Node_route_id_to_path, Node_routers_insert])
b.edge(Node_routers_insert, Node_routers)

b.edge(Service, Router_call)
b.edge(Router_call, Router_call_route)
b.edge(Router_call_route, Node_routers)
b.edge(Router_call_route, MethodRouter_call)
b.edge(MethodRouter_call, RouteFuture)

print(b.source())
