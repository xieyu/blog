from dot_graph_builder import Builder, NodeStyles
from varname.helpers import Wrapper

b = Builder(name="Router")
b.set_node_style(NodeStyles.light_gray)
#b.update_graph_attr(layout="sfdp")
b.update_graph_attr(layout="fdp")

tower_Layer = Wrapper("""tower.Layer|
pub trait Layer<S> {
    type Service;
    fn layer(&self, inner: S) -> Self::Service;
}
""")
b.node(tower_Layer, NodeStyles.grass_green)

MiddlewareFnLayer = Wrapper("""MiddlewareFnLayer|
#[derive(Clone, Copy)]
pub struct MiddlewareFnLayer<F> {
    f: F,
}

Create a middleware from an async function
""")
b.node(MiddlewareFnLayer)

AddExtensionLayer = Wrapper("""AddExtensionLayer|
#[derive(Clone, Copy, Debug)]
pub struct AddExtensionLayer<T> {
    value: T,
}

向req的extentions中插入shared value.clone
req.extensions_mut()
.insert(self.value.clone());
""")
b.node(AddExtensionLayer, NodeStyles.tea_green)

ExtractorMiddlewareLayer = Wrapper("""ExtractorMiddlewareLayer|
pub struct ExtractorMiddlewareLayer
<E>(PhantomData<fn() -> E>);

将extractor 转成中间件
如果extractor报错，则返回
""")
b.node(ExtractorMiddlewareLayer)

ResponseFuture = Wrapper("""ResponseFuture|
    state: State<ReqBody, S, E>,
   svc: Option<S>,
""")
b.node(ResponseFuture)

tower_Stack = Wrapper("""tower.Stack|
#[derive(Clone)]
pub struct Stack<Inner, Outer> {
    inner: Inner,
    outer: Outer,
}

Two middlewares chained together.
""")
b.node(tower_Stack)

HandleErrorLayer = Wrapper("""HandleErrorLayer|
pub struct HandleErrorLayer<F, T> {
    f: F,
    _extractor: PhantomData<fn() -> T>,
}

handles erros by 
converting them into responses

调用f处理error。
f(err).await.into_response()

有点像python flask里面处理各种Exception
的catch exception, 对于这些 error返回
对应的错误resp
""")
b.node(HandleErrorLayer)

LayerFn = Wrapper("""LayerFn|
#[derive(Clone, Copy)]
pub struct LayerFn<F> {
    f: F,
}

A Layer implemented by a closure.
""")

b.node(LayerFn)

Next = Wrapper("""Next|
pub struct Next<ReqBody> {
    inner: BoxCloneService<
    Request<ReqBody>, Response, Infallible>,
}

/// Execute the remaining middleware stack.
pub async fn run(mut self, req: Request<ReqBody>) -> Response
""")
b.node(Next)

ResponseFuture_fn = Wrapper("""ResponseFuture|
/// Response future for [`MiddlewareFn`].
pub struct ResponseFuture<F> {
    #[pin]
    inner: F,
}
""")
b.node(ResponseFuture_fn)

b.edge(tower_Layer, [
    MiddlewareFnLayer, AddExtensionLayer, ExtractorMiddlewareLayer,
    tower_Stack, HandleErrorLayer, LayerFn
])

b.edge(ExtractorMiddlewareLayer, ResponseFuture)
b.edge(MiddlewareFnLayer, Next)
b.edge(MiddlewareFnLayer, ResponseFuture_fn)

print(b.source())
