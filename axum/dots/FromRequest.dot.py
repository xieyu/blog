from dot_graph_builder import Builder, NodeStyles
from varname.helpers import Wrapper

b = Builder(name="Router")
b.set_node_style(NodeStyles.light_gray)
#b.update_graph_attr(layout="circo")
b.update_graph_attr(layout="sfdp")

FromRequest = Wrapper("""FromRequest|
pub trait FromRequest<B>: Sized {
    type Rejection: IntoResponse;

    async fn from_request(req: &mut RequestParts<B>)
    -> Result<Self, Self::Rejection>;
}

""")
b.node(FromRequest)

RequestParts = Wrapper("""RequestParts|
#[derive(Debug)]
pub struct RequestParts<B> {
    method: Method,
    uri: Uri,
    version: Version,
    headers: Option<HeaderMap>,
    extensions: Option<Extensions>,
    body: Option<B>,
}
""")
b.node(RequestParts)

ContentLengthLimit = Wrapper("""ContentLengthLimit|
pub struct ContentLengthLimit<T, const N: u64>(pub T);
""")
b.node(ContentLengthLimit)

Multipart = Wrapper("""Multipart|
#[derive(Debug)]
pub struct Multipart {
    inner: multer::Multipart<'static>,
}

可以用于上传文件
""")
b.node(Multipart, NodeStyles.grass_green)

RawQuery = Wrapper("""RawQuery|
#[derive(Debug)]
pub struct RawQuery(pub Option<String>);
""")
b.node(RawQuery)

Form = Wrapper("""Form|
#[derive(Debug, Clone, Copy, Default)]
pub struct Form<T>(pub T);
""")
b.node(Form, NodeStyles.grass_green)

BodyStream = Wrapper("""BodyStream|
pub struct BodyStream(
    SyncWrapper<Pin<Box<dyn 
        HttpBody<Data = Bytes, 
        Error = Error> + Send + 'static>>>,
);
""")
b.node(BodyStream)

ConnectInfo = Wrapper("""ConnectInfo|
#[derive(Clone, Copy, Debug)]
pub struct ConnectInfo<T>(pub T);
""")
b.node(ConnectInfo)

Extension = Wrapper("""Extension|
#[derive(Debug, Clone, Copy)]
pub struct Extension<T>(pub T);
""")
b.node(Extension, NodeStyles.tomato)

Json = Wrapper("""Json|
#[derive(Debug, Clone, Copy, Default)]
#[cfg_attr(docsrs, doc(cfg(feature = "json")))]
pub struct Json<T>(pub T);

serde_json::from_slice解析Bytes
""")
b.node(Json, NodeStyles.grass_green)

MatchedPath = Wrapper("""MatchedPath|
pub struct MatchedPath(pub(crate) Arc<str>);
""")
b.node(MatchedPath)

Query = Wrapper("""Query|
#[derive(Debug, Clone, Copy, Default)]
pub struct Query<T>(pub T);

调用serde_urlecnode::from_str
解析query到类型T
""")
b.node(Query, NodeStyles.grass_green)

WebScoketUpgrade = Wrapper("""WebScoketUpgrade|
#[derive(Debug)]
pub struct WebSocketUpgrade {
    config: WebSocketConfig,
    protocol: Option<HeaderValue>,
    sec_websocket_key: HeaderValue,
    on_upgrade: OnUpgrade,
    sec_websocket_protocol: Option<HeaderValue>,
}
""")
b.node(WebScoketUpgrade)

Cached = Wrapper("""Cached|
#[derive(Debug, Clone, Default)]
pub struct Cached<T>(pub T);

Cache results of other extractors.
""")
b.node(Cached)

Version = Wrapper("""Version|
/// Represents a version of the HTTP spec.
#[derive(PartialEq, PartialOrd, Copy, 
Clone, Eq, Ord, Hash)]
pub struct Version(Http);

""")
b.node(Version)

Bytes = Wrapper("""Bytes|
Request的body
""")
b.node(Bytes)
TypeHeader = Wrapper("""TypeHeader|
#[cfg(feature = "headers")]
#[cfg_attr(docsrs, doc(cfg(feature = "headers")))]
#[derive(Debug, Clone, Copy)]
pub struct TypedHeader<T>(pub T);
""")
b.node(TypeHeader)

serde_json = Wrapper("""serde_json""")
b.node(serde_json, NodeStyles.orange)

serde_urlencode = Wrapper("""serde_urlencode""")
b.node(serde_urlencode, NodeStyles.orange)

b.edge(RequestParts, FromRequest)
b.edge(FromRequest, [
    ContentLengthLimit, Multipart, RawQuery, BodyStream, Extension,
    ConnectInfo, Form, Json, MatchedPath, WebScoketUpgrade, Version, Bytes,
    TypeHeader, Query, Cached
])
b.edge(Json, serde_json)
b.edge(Query, serde_urlencode)

print(b.source())
