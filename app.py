## IMPORT ##
import clear_cache 

from main import *
from shiny import App, reactive, render, ui
############

app_ui = ui.page_fluid(
    ui.h1("MSSC"),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.p("Hello World")
        ),
        ui.panel_main(
            ui.output_text_verbatim("main")
        )
    )
)

def server(input, output, session) :

    @output
    @render.text
    def main() :
        return "Hello World"

app = App(app_ui, server, debug = False)
clear_cache.clear()
