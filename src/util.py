import flet as ft
from threading import Event

import core
from frontend import Chat, ConnBox, Layout
from network import Connection
from reactor import ReactorClient

logger = core.get_logger(__name__)

@core.uninterruptible
async def close_page(multiplexing_event: Event, page: ft.Page) -> None:
    """
    Handlers that closes the resources, and page.
    
    Args:
        multiplexing_event: Event
        page
    """
    logger.info("Closing application...")
    multiplexing_event.clear()
    
    page.window.prevent_close = False
    page.window.on_event = None
    await page.window.destroy()
    await page.window.close()

def add_conn(conn_data: tuple, reactor_client: ReactorClient, layout: Layout) -> None:
    """
    Receives the connection details and creates a new Connection.
    Sets up UI components (Chat, ConnBox), and enqueues the connection to the reactor.
    
    Args:
        conn_data (arr): A tuple containing connection arguments (host, port, user, pass, db).
        reactor_client (obj): The enqueuer of the connection creation.
        layout (obj): The application layout.
    """
    try:
        # We get the connection object but it remains in read mode.
        conn = reactor_client.enqueue_new_conn(conn_data)
    except core.ConnectionCountError:
        logger.error(
            "Can not add a new connection.\n"
            "Remove old connections or restart the application with a new \".env\" configuration.")
        return
    
    conn_host = conn_data[0]
    rem_conn_callback = lambda: rem_conn(conn, reactor_client, layout)

    conn_box = ConnBox(
        text=conn_host,
        on_click=lambda: layout.chat_frame.sel_chat(chat),
        on_close=rem_conn_callback)
    layout.agenda.add_box(conn_box)
    layout.conn_boxes_dict[conn] = conn_box

    chat = Chat(
        text=conn_host,
        on_enter=lambda cmd: reactor_client.enqueue_cmd(conn, cmd),
        exit_cmd_callback=rem_conn_callback)
    layout.chat_frame.sel_chat(chat)
    reactor_client.bind_chat(conn, chat)

def rem_conn(conn: Connection, reactor_client: ReactorClient, layout: Layout) -> None:
    """
    Enqueues a connection to be unregistered, closed, and removed from the UI.

    Args:
        conn (obj): The connection to be removed.
        reactor_client (obj): The enqueuer of the connection creation.
        layout (obj): The application layout.
    """
    reactor_client.enqueue_close_conn(conn)
    conn_box = layout.conn_boxes_dict[conn]
    layout.agenda.rem_box(conn_box)
    layout.chat_frame.rem_chat()
