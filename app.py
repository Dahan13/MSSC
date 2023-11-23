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
WIDTH = 6
HEIGHT = 6

PATH = "C:/Users/dubou/Desktop/IMTA/A3-LOGIN/UE-MSSC/MSSC/turbine_img/"

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
        ui.navset_tab(
            ui.nav("TEXT DISPLAY",
                ui.output_text_verbatim("text")
            ),
            ui.nav("ICON DISPLAY",
                ui.output_ui("ICON_current_day_info"),
                ui.output_ui("ICON_turbines"),
                ui.output_ui("ICON_teams")
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
        return "DAY n°%d"%(system.get_days_count())
    
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
    def ICON_current_day_info() :
        global system
        wind = system.get_wind()
        match wind :
            case 1 :
                wind_img = "wind_low.gif"
            case 2 :
                wind_img = "wind_medium.gif"
            case 3 :
                wind_img = "wind_high.gif"
        information =   ui.div({"style":"display:flex;margin-bottom:30px;justify-content:space-between;"},
                            ui.div({"style":f"display:flex;width:250px;height:150px;border:solid blue 4px;"},
                                ui.div({"style":"display:flex;height:100%;width:100%;"},
                                    ui.img({"style":"max-width:100%;max-height:100%;margin:auto;"},src=wind_img)
                                )
                            ),
                            ui.div({"style":f"display:flex;width:250px;height:150px;border:solid blue 4px;"},
                                ui.div({"style":"display:flex;height:100%;width:100%;"},
                                    ui.p({"style":"max-width:100%;max-height:100%;margin:auto;font-weight:bold;font-size:50px;"},f"DAY {system.get_days_count()}")
                                )
                            ),
                            ui.div({"style":f"display:flex;width:250px;height:150px;border:solid blue 4px;"},
                                ui.div({"style":"display:flex;height:100%;width:100%;"},
                                    ui.p({"style":"max-width:100%;max-height:100%;margin:auto;font-weight:bold;font-size:15px;"},f"PRODUCTION {system.get_total_prod()}")
                                )
                            ),
                            ui.div({"style":f"display:flex;width:250px;height:150px;border:solid blue 4px;"},
                                ui.div({"style":"display:flex;height:100%;width:100%;"},
                                    ui.p({"style":"max-width:100%;max-height:100%;margin:auto;font-weight:bold;font-size:15px;"},f"COST {system.get_total_cost()}")
                                )
                            )
                        )
        return ui.div({"style":"display:block;"}, information)

    @output
    @render.ui
    @reactive.event(input.next_day)
    def ICON_turbines() :
        global system
        turbines = system.get_turbines()
        all = []
        for j in range(HEIGHT) :
            line = []
            for i in range(WIDTH) :
                index = j*WIDTH+i
                if index < len(turbines) :
                    if turbines[index].get_state() != 4 : img = "turbine_on.png"
                    else : img = "turbine_off.png"
                    line.append (
                                    ui.div({"style":f"display:flex;width:{1000//(WIDTH+1)}px;height:{600//(HEIGHT+1)}px;border:solid;"},
                                        ui.div({"style":"display:flex;height:100%;width:70%;"},
                                            ui.img({"style":"max-width:100%;max-height:100%;margin:auto;"},src=img)
                                        ),
                                        ui.div({"style":"height:100%;width:30%;"},
                                            ui.div({"style":"display:flex;height:50%;width:100%;"},ui.p({"style":"margin:auto;font-weight:bold;font-size:20px;"},str(index+1))),
                                            ui.div({"style":"display:flex;height:50%;width:100%;"},ui.div({"style":"display:flex;margin:auto;height:35px;width:35px;background-color:#55c9ff;border-radius:50%;"},ui.p({"style":"margin:auto;font-weight:bold;font-size:20px;"},str(turbines[index].get_state()))))
                                        )
                                    )
                                )
                else :
                    if len(turbines)> j*WIDTH and len(turbines)< (j+1)*WIDTH : 
                        line.append(ui.div({"style":f"display:flex;width:{1000//(WIDTH+1)}px;height:{600//(HEIGHT+1)}px;"}))
            if line != [] :
                all.append(ui.div({"style":"display:flex;margin-bottom:20px;justify-content:space-between;"},line))
        return ui.div({"style":"display:block;"},all)

    @output
    @render.ui
    @reactive.event(input.next_day)
    def ICON_teams() :
        global system
        teams = system.get_teams()
        planning = system.get_planning()
        all = []
        for j in range(HEIGHT) :
            line = []
            for i in range(WIDTH) :
                index = j*WIDTH+i
                if index < len(teams) :
                    if teams[index].get_availability() : 
                        img = "team_on.png"
                        display_info = ""
                    else : 
                        img = "team_off.png"
                        for (team, turbine) in planning.get_attribution() :
                            if team == teams[index].get_id() :
                                display_info = str(turbine)
                    line.append (
                                    ui.div({"style":f"display:flex;width:{1000//(WIDTH+1)}px;height:{600//(HEIGHT+1)}px;border:solid orange;"},
                                        ui.div({"style":"display:flex;height:100%;width:70%;"},
                                            ui.img({"style":"max-width:90%;max-height:90%;margin:auto;"},src=img)
                                        ),
                                        ui.div({"style":"height:100%;width:30%;"},
                                            ui.div({"style":"display:flex;height:50%;width:100%;"},ui.p({"style":"margin:auto;font-weight:bold;font-size:20px;"},str(index+1))),
                                            ui.div({"style":"display:flex;height:50%;width:100%;"},ui.div({"style":"display:flex;margin:auto;height:35px;width:30px;border:solid 2px blue;"},ui.p({"style":"margin:auto;font-weight:normal;font-size:20px;"},display_info)))
                                        )
                                    )
                                )
                else :
                    if len(teams) > j*WIDTH and len(teams) < (j+1)*WIDTH : 
                        line.append(ui.div({"style":f"display:flex;width:{1000//(WIDTH+1)}px;height:{600//(HEIGHT+1)}px;"}))
            if line != [] :
                all.append(ui.div({"style":"display:flex;margin-bottom:30px;justify-content:space-between;"},line))
        return ui.div({"style":"display:block;"},all)


img_dir = Path(__file__).parent / "img_database"
app = App(app_ui, server, static_assets=img_dir, debug = False)
clear_cache.clear()
