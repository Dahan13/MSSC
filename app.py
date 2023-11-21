## IMPORT ##
import clear_cache 
from pathlib import Path

from main import *
from shiny import App, reactive, render, ui
from shiny.types import ImgData
############

CSS_flexbox = "display:flex;justify-content:center;align-items:center;"
CSS_border = "border:solid 2px black;"

NUMBER_OF_TURBINES = 20
NUMBER_OF_TEAMS = 5
system = System(NUMBER_OF_TURBINES, NUMBER_OF_TEAMS)
WIDTH = 5
HEIGHT = 6

PATH = "C:/Users/dubou/Desktop/IMTA/A3-LOGIN/UE-MSSC/MSSC/turbine_img/"

app_ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.sidebar({"style":"display:flex;height:90vh;border:solid;"},
            ui.div({"style":CSS_flexbox+CSS_border},
                ui.input_action_button("reset","RESET SYSTEM")
            ),
            ui.div({"style":CSS_border+"padding-top:15px;"},
                ui.div({"style":CSS_flexbox},
                    ui.p({"style":"width:100px;"},"TURBINES"),
                    ui.div({"style":"width:70px;"},ui.input_numeric("nb_turbines",label="",value=NUMBER_OF_TURBINES,min=1,max=100,step=1))
                ),
                ui.div({"style":CSS_flexbox},
                    ui.p({"style":"width:100px;"},"TEAMS"),
                    ui.div({"style":"width:70px;"},ui.input_numeric("nb_teams",label="",value=NUMBER_OF_TEAMS,min=1,max=100,step=1))
                )
            ),
            ui.div({"style":CSS_flexbox+CSS_border},
                ui.div({"style":CSS_flexbox+"font-size:15px;padding-top:15px;"},ui.output_text_verbatim("day_indicator")),
                ui.div({"style":CSS_flexbox},ui.input_action_button("next_day","NEXT DAY"))
            ),
            ui.div({"style":CSS_border+"height:375px;overflow:scroll;"},
                ui.div({"style":CSS_flexbox+"height:10%;"},
                    ui.div({"style":CSS_flexbox+"width:50%;border-right:solid 1px;padding-top:10px;"},ui.p("TURBINES")),
                    ui.div({"style":CSS_flexbox+"width:50%;border-left:solid 1px;padding-top:10px;"},ui.p("TEAMS"))
                ),
                ui.div({"style":"display:flex;justify-items:center;height:90%;"},
                    ui.div({"style":"width:50%;padding:0 10px;border-right:solid 1px;"},ui.output_text_verbatim("turbines_status")),
                    ui.div({"style":"width:50%;padding:0 10px;border-left:solid 1px;"},ui.output_text_verbatim("teams_status"))
                )
            ),
            ui.div({"style":CSS_border+"padding-top:15px;"},
                ui.output_text_verbatim("total_cost"),
                ui.output_text_verbatim("total_prod")
            ),
            width="300px"
        ),
        ui.navset_tab(
            ui.nav("TEXT DISPLAY",
                ui.output_text_verbatim("text")
            ),
            ui.nav("ICON DISPLAY",
                ui.output_ui("icon")
            ),
        )
    )
)

def server(input, output, session) :
    
    @reactive.Effect
    @reactive.event(input.reset)
    def reset() :
        global system
        system = System(NUMBER_OF_TURBINES, NUMBER_OF_TEAMS)

    @reactive.Effect
    @reactive.event(input.nb_turbines)
    def nb_turbines() :
        global NUMBER_OF_TURBINES
        NUMBER_OF_TURBINES = input.nb_turbines()

    @reactive.Effect
    @reactive.event(input.nb_teams)
    def nb_teams() :
        global NUMBER_OF_TEAMS
        NUMBER_OF_TEAMS = input.nb_teams()
    
    @reactive.Effect
    @reactive.event(input.next_day)
    def next_day() :
        global system
        system.next_day()

    @output
    @render.text
    @reactive.event(input.next_day)
    def day_indicator() :
        global system
        return "DAY n°%d"%(system.get_day())
    
    output
    @render.text
    @reactive.event(input.nb_turbines)
    def turbines_status() :
        return "T0 - (0)\n"*NUMBER_OF_TURBINES
    
    output
    @render.text
    @reactive.event(input.nb_teams)
    def teams_status() :
        return "T0 - (0)\n"*NUMBER_OF_TEAMS

    output
    @render.text
    def total_cost() :
        return "TOTAL COST : %8d"%(0)
    
    output
    @render.text
    def total_prod() :
        return "TOTAL PROD : %8d"%(0)
    
    @output
    @render.text
    @reactive.event(input.next_day)
    def text() :
        global system
        return system.display_txt()

    @output
    @render.ui
    @reactive.event(input.next_day)
    def icon() :
        global system
        turbines = system.get_turbines()
        all = []
        for j in range(HEIGHT) :
            line = []
            for i in range(WIDTH) :
                index = j*WIDTH+i
                if index < len(turbines) :
                    img = "turbine_on.png"
                    if turbines[index].get_state() != 4 : img = "turbine_on.png"
                    else : img = "turbine_off.png"
                    line.append (
                                    ui.div({"style":"display:flex;width:180px;height:130px;border:solid;"},
                                        ui.div({"style":"height:100%;width:50%;"},
                                            ui.img({"style":"height:90%;margin-top:10%;"},src=img)
                                        ),
                                        ui.div({"style":"height:100%;width:50%;"},
                                            ui.div({"style":"display:flex;height:50%;width:100%;"},ui.p({"style":"margin:auto;font-weight:bold;font-size:20px;"},str(index+1))),
                                            ui.div({"style":"display:flex;height:50%;width:100%;"},ui.div({"style":"display:flex;margin:auto;height:70%;width:35%;border:solid 2px blue;"},ui.p({"style":"margin:auto;font-weight:normal;font-size:20px;"},str(turbines[index].get_state()))))
                                        )
                                    )
                                )
            all.append(ui.div({"style":"display:flex;margin-bottom:30px;justify-content:space-between;"},line))
        return ui.div({"style":"display:block;"},all)

img_dir = Path(__file__).parent / "turbine_img"
app = App(app_ui, server, static_assets=img_dir, debug = False)
clear_cache.clear()
