from dot_graph_builder import Builder, NodeStyles
from varname.helpers import Wrapper

b = Builder(name="Router")
b.set_node_style(NodeStyles.light_gray)

Handler = Wrapper("""trait Handler|
#[async_trait]
pub trait Handler<T, B = Body>: Clone + Send + Sized + 'static {

type Sealed: sealed::HiddenTrait;

async fn call(self, req: Request<B>) -> Response;

fn layer<L>(self, layer: L) -> Layered<L::Service, T>

fn into_service(self) -> IntoService<Self, T, B> 

fn into_make_service(self) -> IntoMakeService<IntoService<Self, T, B>> 

fn into_make_service_with_connect_info<C, Target>
""")
b.node(Handler, NodeStyles.grass_green)

impl_hanlder = Wrapper("""impl_hanlder!|
给Fnonce(T1,...Tn) -> Fut + Clone + Send + 'static 
实现Handler trait
其中T1..Tn要实现FromRequest trait

call 接口
会调用FromRequest将参数extract出来
然后使用它们调用FnOnce函数
""")
b.node(impl_hanlder, NodeStyles.light_green)

all_the_tuples = Wrapper("""all_the_tuples!|
依次展开，支持1~16个参数

macro_rules! all_the_tuples {
    ($name:ident) => {
        $name!(T1);
        $name!(T1, T2);
        ....
        $name!(T1, T2, T3, T4, T5, T6, 
            T7, T8, T9, T10, T11, 
            T12, T13, T14, T15, T16);
}
""")
b.node(all_the_tuples, NodeStyles.light_green)

impl_service = Wrapper("""impl_service!|
为HandleError<S, F, (T1...Tn)> 
实现Service trait

""")
b.node(impl_service, NodeStyles.light_green)

impl_from_request = Wrapper("""impl_from_request!|
给(T1,...Tn) 实现FromRequest

依次调用每个T的from_request

impl<B, $($ty,)*> FromRequest<B> for ($($ty,)*)
""")
b.node(impl_from_request, NodeStyles.light_green)

FromRequst = Wrapper("""trait FromRequst|
#[async_trait]
pub trait FromRequest<B>: Sized {
    type Rejection: IntoResponse;

    async fn from_request(req: &mut RequestParts<B>)
    -> Result<Self, Self::Rejection>;
}
""")
b.node(FromRequst, NodeStyles.grass_green)

HandleError_Service_call = Wrapper("""HandleError.call|
为HandlerError T类型为(T1, ...  Tn)
实现的 Service call接口:

依次调用每个T的from_request
组合成参数后调用FnOnce(...)函数
""")
b.node(HandleError_Service_call)

tower_Service = Wrapper("""trait tower.Service|
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
b.node(tower_Service, NodeStyles.grass_green)

IntoService = Wrapper("""IntoService|
pub struct IntoService<H, T, B> {
    handler: H,
    _marker: PhantomData<fn() -> (T, B)>,
}

An adapter that makes 
a [`Handler`] into a [`Service`].

call接口会调用handler.call(...)
""")
b.node(IntoService)

IntoServiceFuture = Wrapper("""IntoServiceFuture|
pub type IntoServiceFuture =
    Map<
        BoxFuture<'static, Response>,
        fn(Response) -> Result<Response, Infallible>,
    >;
""")
b.node(IntoServiceFuture)

Layered = Wrapper("""Layered|
pub struct Layered<S, T> {
    svc: S,
    _input: PhantomData<fn() -> T>,
}

用于apply Tower middleware
Layered也实现了Hanlder trait
""")
b.node(Layered)

Layer = Wrapper("""tower.Layer|
pub trait Layer<S> {
    type Service;
    fn layer(&self, inner: S) -> Self::Service;
}

 Wrap the given service with the middleware, 
 returning a new service

 that has been decorated with the middleware.
""")
b.node(Layer, NodeStyles.grass_green)

IntoMakeService = Wrapper("""IntoMakeService|
#[derive(Debug, Clone)]
pub struct IntoMakeService<S> {
    svc: S,
}
""")
b.node(IntoMakeService)

IntoMakeServiceFuture = Wrapper("""IntoMakeServiceFuture|
pub type IntoMakeServiceFuture<S> =
    std::future::Ready<Result<S, Infallible>>;
""")
b.node(IntoMakeServiceFuture)

opaque_future = Wrapper("""opaque_future!|
不太明白这个宏的作用
""")
b.node(opaque_future, NodeStyles.light_green)

b.edge(all_the_tuples, [impl_hanlder, impl_from_request, impl_service])
b.edge(impl_hanlder, Handler)
b.edge(impl_from_request, FromRequst)
b.edge(impl_service, [tower_Service, HandleError_Service_call])
b.edge(Handler, [IntoService, Layered, IntoMakeService])
b.edge(IntoMakeService, [tower_Service, IntoMakeServiceFuture])
b.edge(IntoService, [tower_Service, IntoServiceFuture])
b.edge(opaque_future, [IntoServiceFuture, IntoMakeServiceFuture])
b.edge(Handler, Layer)
b.edge(Layer, Layered)

print(b.source())
