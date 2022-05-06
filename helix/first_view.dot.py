from dot_graph_builder import Builder, NodeStyles
from varname.helpers import Wrapper

b = Builder(name="Router")
b.set_node_style(NodeStyles.light_gray)

Picker = Wrapper("""Picker|
options: Vec<T>,
matcher: Box<Matcher>,
matches: Vec<(usize, i64)>,
filters: Vec<usize>,
completion_height: u16,
cursor: usize,
prompt: Prompt,
previous_pattern: String,
pub truncate_start: bool,
format_fn: Box<dyn Fn(&T) -> Cow<str>>,
callback_fn: Box<dyn Fn(&mut Context, &T, Action)>,
""")
b.node(Picker)

FilePicker = Wrapper("""FilePicker|
    picker: Picker<T>,
    pub truncate_start: bool,
    preview_cache: HashMap<PathBuf, CachedPreview>,
    read_buffer: Vec<u8>,
    file_fn: Box<dyn Fn(&Editor, &T) -> Option<FileLocation>>,
""")
b.node(FilePicker)

FileLocation = Wrapper("""FileLocation|
(PathBuf, Option<(usize, usize)>)""")
b.node(FileLocation)

Prompt = Wrapper("""Prompt|
prompt: Cow<'static, str>,
line: String,
cursor: usize,
completion: Vec<Completion>,
selection: Option<usize>,
history_register: Option<char>,
history_pos: Option<usize>,
completion_fn: Box<dyn FnMut(&Editor, &str) -> Vec<Completion>>,
callback_fn: Box<dyn FnMut(&mut Context, &str, PromptEvent)>,
pub doc_fn: Box<dyn Fn(&str) -> Option<Cow<str>>>,
""")
b.node(Prompt)

Completion = Wrapper("""Completion|
(RangeFrom<usize>, Cow<'static, str>);
""")
b.node(Completion)

PromptEvent = Wrapper("""PromptEvent|
pub enum PromptEvent {
Update,
Validate,
Abort,
}
""")

b.node(PromptEvent)

Component = Wrapper("""Component|
    fn handle_event
    fn should_update
    fn render
    fn cursor
    fn required_size
    fn type_name
""")
b.node(Component, NodeStyles.grass_green)

Text = Wrapper("""Text""")
b.node(Text)

Context = Wrapper("""Context|
    pub editor: &'a mut Editor,
    pub scroll: Option<usize>,
    pub jobs: &'a mut Jobs,
""")
b.node(Context)

Editor = Wrapper("""Editor|
    pub tree: Tree,
    pub next_document_id: DocumentId,
    pub documents: BTreeMap<DocumentId, Document>,
    pub count: Option<std::num::NonZeroUsize>,
    pub selected_register: Option<char>,
    pub registers: Registers,
    pub macro_recording: Option<(char, Vec<KeyEvent>)>,
    pub theme: Theme,
    pub language_servers: helix_lsp::Registry,
    pub debugger: Option<dap::Client>,
    pub debugger_events: SelectAll<UnboundedReceiverStream<dap::Payload>>,
    pub breakpoints: HashMap<PathBuf, Vec<Breakpoint>>,
    pub clipboard_provider: Box<dyn ClipboardProvider>,
    pub syn_loader: Arc<syntax::Loader>,
    pub theme_loader: Arc<theme::Loader>,
    pub status_msg: Option<(Cow<'static, str>, Severity)>,
    pub autoinfo: Option<Info>,
    pub config: Box<dyn DynAccess<Config>>,
    pub auto_pairs: Option<AutoPairs>,
    pub idle_timer: Pin<Box<Sleep>>,
    pub last_motion: Option<Motion>,
    pub pseudo_pending: Option<String>,
    pub last_completion: Option<CompleteAction>,
    pub exit_code: i32,
    pub config_events: (UnboundedSender<ConfigEvent>, UnboundedReceiver<ConfigEvent>),
""")
b.node(Editor)

Document = Wrapper("""Document|
    pub(crate) id: DocumentId,
    text: Rope,
    pub(crate) selections: HashMap<ViewId, Selection>,
    path: Option<PathBuf>,
    encoding: &'static encoding::Encoding,
    pub mode: Mode,
    pub restore_cursor: bool,
    pub indent_style: IndentStyle,
    pub line_ending: LineEnding,
    syntax: Option<Syntax>,
    pub(crate) language: Option<Arc<LanguageConfiguration>>,
    changes: ChangeSet,
    old_state: Option<State>,
     pub history: Cell<History>,
    pub savepoint: Option<Transaction>,
    last_saved_revision: usize,
    version: i32,
    pub(crate) modified_since_accessed: bool,
    diagnostics: Vec<Diagnostic>,
    language_server: Option<Arc<helix_lsp::Client>>,
""")
b.node(Document)


Mode = Wrapper("""Mode|
    Normal = 0,
    Select = 1,
    Insert = 2,
""")
b.node(Mode)

lsp_Client = Wrapper("""Client|
    id: usize,
    _process: Child,
    server_tx: UnboundedSender<Payload>,
    request_counter: AtomicU64,
    pub(crate) capabilities: OnceCell<lsp::ServerCapabilities>,
    offset_encoding: OffsetEncoding,
    config: Option<Value>,
    root_path: Option<std::path::PathBuf>,
    root_uri: Option<lsp::Url>,
    workspace_folders: Vec<lsp::WorkspaceFolder>,
""")
b.node(lsp_Client)


Tree = Wrapper("""Tree|
    root: ViewId,
    pub focus: ViewId,
    area: Rect,
    nodes: HopSlotMap<ViewId, Node>,
    stack: Vec<(ViewId, Rect)>,
""")
b.node(Tree)

DocumentId = Wrapper("""DocumentId|
pub struct DocumentId(NonZeroUsize)
""")
b.node(DocumentId)

Registry = Wrapper("""Registry|
    inner: HashMap<LanguageId, (usize, Arc<Client>)>,
    counter: AtomicUsize,
    pub incoming: SelectAll<UnboundedReceiverStream<(usize, Call)>>,
""")
b.node(Registry)

Rope = Wrapper("""ropey.Rope| """)
b.node(Rope)

Selection = Wrapper("""Selection
    ranges: SmallVec<[Range; 1]>,
    primary_index: usize,
""")
b.node(Selection)

Job = Wrapper("""Job|
pub struct Jobs {
    pub futures: FuturesUnordered<JobFuture>,
    /// These are the ones that need to complete before we exit.
    pub wait_futures: FuturesUnordered<JobFuture>,
}
""")
b.node(Job)

BreakPoint = Wrapper("""BreakPoint|
    pub id: Option<usize>,
    pub verified: bool,
    pub message: Option<String>,
    pub line: usize,
    pub column: Option<usize>,
    pub condition: Option<String>,
    pub hit_condition: Option<String>,
    pub log_message: Option<String>,
""")
b.node(BreakPoint)

Config = Wrapper("""Config|
""")
b.node(Config)

theme_Loader = Wrapper("""theme.Loader
    user_dir: PathBuf,
    default_dir: PathBuf,
""")
b.node(theme_Loader)

syntax_Loader = Wrapper("""syntax.Loader|
    language_configs: Vec<Arc<LanguageConfiguration>>,
    language_config_ids_by_file_type: HashMap<String, usize>,
    language_config_ids_by_shebang: HashMap<String, usize>,
    scopes: ArcSwap<Vec<String>>,
""")
b.node(syntax_Loader)

b.edge(Context, [Editor, Job])
b.edge(Editor, [Document, Tree, DocumentId,
       Registry, BreakPoint, Config,
                theme_Loader, syntax_Loader])
b.edge(Document, [Mode, lsp_Client, Rope, Selection])
b.edge(Registry, [lsp_Client])

b.edge(Component, [FilePicker, Text])
b.edge(FilePicker, [Picker, FileLocation])
b.edge(Picker, [Prompt])
b.edge(Prompt, [Completion, PromptEvent])

# static_commands
# command__file_picker -> ui__ficker
print(b.source())
