from rich.console import Console
from rich.table import Table
from .utils import ConfigPathUtility

console = Console()

def draw_table():
    table: Table = Table(title="SSH Servers in Config File 📁")
    table.add_column("Hostname", justify="left", style="cyan", no_wrap=True)
    table.add_column("Host", style="magenta")
    table.add_column("Port", justify="right", style="green")
    table.add_column("User", justify="right", style="yellow")

    for i in ConfigPathUtility.get_config_file_row_data():
        table.add_row(i[0], i[1], i[2], i[3])

    console.print(table)
