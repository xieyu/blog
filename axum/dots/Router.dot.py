from dot_graph_builder import Builder, NodeStyles
from varname.helpers import Wrapper

b = Builder(name="Router")
b.set_node_style(NodeStyles.light_gray)

Router = Wrapper("""Router|
pub struct Router<B = Body> {
    routes: HashMap<RouteId, Endpoint<B>>,
    node: Node,
    fallback: Fallback<B>,
    nested_at_root: bool,
}
""")
b.node(Router, style=NodeStyles.dark_blue)

Body = Wrapper("""Body|
pub struct Body {
    kind: Kind,
    extra: Option<Box<Extra>>,
}
""")
b.node(Body, style=NodeStyles.light_blue)

Extra = Wrapper("""Extra|
struct Extra {
    delayed_eof: Option<DelayEof>,
}
""")
b.node(Extra, style=NodeStyles.tea_green)

RouterId = Wrapper("""RouterId|
    struct RouteId(u32);
""")
b.node(RouterId, style=NodeStyles.orange)

Fallback = Wrapper("""Fallback|
enum Fallback<B, E = Infallible> {
    Default(Route<B, E>),
    Custom(Route<B, E>),
}
""")
b.node(Fallback, style=NodeStyles.grass_green)

Node = Wrapper("""Node|
struct Node {
    inner: matchit::Node<RouteId>,
    route_id_to_path: HashMap<RouteId, Arc<str>>,
    path_to_route_id: HashMap<Arc<str>, RouteId>,
}
""")
b.node(Node, style=NodeStyles.tomato)

matchit_Node = Wrapper("""matchit.Node|
pub struct Node<T> {
    priority: u32,
    wild_child: bool,
    indices: Vec<u8>,
    node_type: NodeType,
    // See `at_inner` for why an unsafe cell is needed.
    value: Option<UnsafeCell<T>>,
    pub(crate) prefix: Vec<u8>,
    pub(crate) children: Vec<Self>,
}
""")
b.node(matchit_Node, style=NodeStyles.light_gray)

Route = Wrapper("""Route|
pub struct Route<B = Body, E = Infallible>
(pub(crate) BoxCloneService
<Request<B>, Response, E>);
""")
b.node(Route)

http_Request = Wrapper("""http.Request|
pub struct Request<T> {
    head: Parts,
    body: T,
}
""")
b.node(http_Request)

Response = Wrapper("""Response|
pub type Response<T = BoxBody>
= http::Response<T>;
""")
b.node(Response)

http_Response = Wrapper("""http.Response|
pub struct Response<T> {
    head: Parts,
    body: T,
}
""")
b.node(http_Response)

BoxCloneService = Wrapper("""tower.BoxCloneService|
pub struct BoxCloneService<T, U, E>(
    Box<
        dyn CloneService<T, 
            Response = U, 
            Error = E, 
            Future = BoxFuture<'static, Result<U, E>>>
            + Send,
    >,
);
""")
b.node(BoxCloneService)

CloneService = Wrapper("""tower.CloneService|
trait CloneService<R>: Service<R> {
    fn clone_box(...)
}
""")
b.node(CloneService)

Service = Wrapper("""tower.Service|
pub trait Service<Request> {
    type Response;
    type Error;
    type Future: Future<Output =
    Result<Self::Response, Self::Error>>;

    fn poll_ready(&mut self, cx: &mut Context<'_>) 
    -> Poll<Result<(), Self::Error>>;

    fn call(&mut self, req: Request) -> Self::Future;
}
""")
b.node(Service)

Endpoint = Wrapper("""Endpoint|
enum Endpoint<B> {
    MethodRouter(MethodRouter<B>),
    Route(Route<B>),
}
""")
b.node(Endpoint)

MethodRouter = Wrapper("""MethodRouter|
    get: Option<Route<B, E>>,
    head: Option<Route<B, E>>,
    delete: Option<Route<B, E>>,
    options: Option<Route<B, E>>,
    patch: Option<Route<B, E>>,
    post: Option<Route<B, E>>,
    put: Option<Route<B, E>>,
    trace: Option<Route<B, E>>,
    fallback: Fallback<B, E>,
    _request_body: PhantomData<fn() -> (B, E)>,
""")
b.node(MethodRouter, style=NodeStyles.light_green)

http_Parts = Wrapper("""http.Parts|
pub struct Parts {
    pub status: StatusCode,
    pub version: Version,
    pub headers: HeaderMap<HeaderValue>,
    pub extensions: Extensions,
    _priv: (),
}
""")
b.node(http_Parts)

Extensions = Wrapper("""Extensions|
pub struct Extensions {
    map: Option<Box<AnyMap>>,
}
""")
b.node(Extensions, NodeStyles.orange)

BoxBody = Wrapper("""BoxBody|
http_body
::combinators
::UnsyncBoxBody<Bytes, Error>;
""")
b.node(BoxBody)

Bytes = Wrapper("""Bytes|
    ptr: *const u8,
    len: usize,
    // inlined "trait object"
    data: AtomicPtr<()>,
    vtable: &'static Vtable,
""")
b.node(Bytes)

UnsyncBoxBody = Wrapper("""UnsyncBoxBody|
pub struct UnsyncBoxBody<D, E> {
    inner: Pin<Box<dyn 
        Body<Data = D, Error = E>
    + Send + 'static>>,
}
""")
b.node(UnsyncBoxBody)

http_HeaderValue = Wrapper("""http.HeaderValue|
pub struct HeaderValue {
    inner: Bytes,
    is_sensitive: bool,
}
""")
b.node(http_HeaderValue)

b.edge(Router, [Body, RouterId, Fallback, Node, Endpoint], style="dashed")
b.edge(Endpoint, [Route, MethodRouter])
b.edge(MethodRouter, [Route, Fallback])

b.edge(Body, Extra)
b.edge(Node, [RouterId, matchit_Node])
b.edge(Fallback, Route)
b.edge(Route, [http_Request, Response, BoxCloneService])
b.edge(Response, http_Response)

b.edge(BoxCloneService, CloneService)
b.edge(CloneService, Service)
b.edge(Service, [http_Request, Response])

b.edge(http_Request, [Body, http_Parts])
b.edge(http_Response, [Body, http_Parts])
b.edge(http_Parts, [Extensions, http_HeaderValue])

b.edge(Response, [BoxBody])
b.edge(BoxBody, [UnsyncBoxBody, Bytes])
b.edge(UnsyncBoxBody, Body)
b.edge(http_HeaderValue, Bytes)

print(b.source())
