## IMPORT ##
import clear_cache 

from main import *
from shiny import App, reactive, render, ui
############

CSS_flexbox = "display:flex;justify-content:center;align-items:center;"
CSS_border = "border:solid 2px black;"

NUMBER_OF_TURBINES = 20
NUMBER_OF_TEAMS = 5
system = System(NUMBER_OF_TURBINES, NUMBER_OF_TEAMS)

app_ui = ui.page_fluid(
    ui.h1("MSSC"),
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
        ui.output_text_verbatim("main")
    )
)

def server(input, output, session) :
    
    @reactive.Effect
    @reactive.event(input.reset)
    def reset() :
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
    def main() :
        global system
        return system.display_txt()


app = App(app_ui, server, debug = False)
clear_cache.clear()
