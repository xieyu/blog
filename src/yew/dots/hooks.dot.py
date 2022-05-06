from dot_graph_builder import Builder, NodeStyles
from varname.helpers import Wrapper

b = Builder(name="Router")
b.set_node_style(NodeStyles.light_gray)

use_state = Wrapper("""use_state|

""")
b.node(use_state)

use_state_eq = Wrapper("""use_state_eq|

""")
b.node(use_state_eq)

use_reducer_eq = Wrapper("""use_reducer_eq|

""")
b.node(use_reducer_eq)

use_reducer = Wrapper("""use_reducer|

""")
b.node(use_reducer)

UseStateReducer = Wrapper("""UseStateReducer|

""")
b.node(UseStateReducer)

use_reducer_base = Wrapper("""use_reducer_base|

""")

use_hook = Wrapper("""use_hook|

""")
b.node(use_hook)
b.node(use_reducer_base)

UseReducer = Wrapper("""UseReducer|

""")
b.node(UseReducer)

CURRENT_HOOK = Wrapper("""CURRENT_HOOK|
scoped_thread_local!
static mut CURRENT_HOOK: HookState
""")
b.node(CURRENT_HOOK)

InternalHook = Wrapper("""InternalHook|

""")
b.node(InternalHook)

HookUpdater = Wrapper("""HookUpdater|

""")
b.node(HookUpdater)

HookState = Wrapper("""HookState|
    counter: usize,
    scope: AnyScope,
    process_message: ProcessMessage,
    hooks: Vec<Rc<RefCell<dyn std::any::Any>>>,
    destroy_listeners: Vec<Box<dyn FnOnce()>>,

""")
b.node(HookState)

FunctionComponent = Wrapper("""FunctionComponent|

""")
b.node(FunctionComponent)

MsgQueue = Wrapper("""MsgQueue|

""")
b.node(MsgQueue)

ProcessMessage = Wrapper("""ProcessMessage|

""")
b.node(ProcessMessage)

Msg = Wrapper("""Msg|
type Msg = Box<dyn FnOnce() -> bool>
""")
b.node(Msg)

MsgQueue = Wrapper("""MsgQueue|
struct MsgQueue(Rc<RefCell<Vec<Msg>>>)
""")
b.node(MsgQueue)

b.edge(use_state, [use_reducer, UseStateReducer])

b.edge(use_reducer, [use_reducer_base])

b.edge(use_reducer_base, [use_hook, UseReducer])

b.edge(use_hook, [CURRENT_HOOK, InternalHook, HookUpdater])
b.edge(CURRENT_HOOK, HookState)

b.edge(FunctionComponent, [HookState, MsgQueue])
b.edge(HookState, [ProcessMessage])
b.edge(ProcessMessage, [Msg])
b.edge(MsgQueue, [Msg])

b.edge(use_state_eq, [use_reducer_eq])
b.edge(use_state_eq, [use_reducer_base])

print(b.source())
