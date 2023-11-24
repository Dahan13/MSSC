## IMPORT ##
import clear_cache 
from pathlib import Path

from main import *
from shiny import App, reactive, render, ui
from shiny.types import ImgData
############

NUMBER_OF_TURBINES = 20
NUMBER_OF_TEAMS = 5

system = System(NUMBER_OF_TURBINES, NUMBER_OF_TEAMS)

WIDTH = 8
HEIGHT = 6

CSS_flexbox = "display:flex;justify-content:center;align-items:center;"
CSS_border = "border:solid 2px black;"
CSS_infobox = "display:flex;width:250px;height:150px;"
CSS_blue_border = "border:solid blue 2px;"
CSS_black_border = "border:solid black 2px;"
CSS_orange_border = "border:solid orange 2px;"
CSS_linebox = f"display:flex;width:{1000//(WIDTH+1)}px;height:{600//(HEIGHT+1)}px;"
CSS_flex_100_100 = "display:flex;height:100%;width:100%;"
CSS_flex_50_100 = "display:flex;height:50%;width:100%;"
CSS_flex_100_70 = "display:flex;height:100%;width:70%;"
CSS_maxbox = "max-width:90%;max-height:90%;margin:auto;"
CSS_completionbox = "display:flex;margin-bottom:20px;justify-content:space-between;"
CSS_t_text = "margin:auto;font-weight:bold;font-size:20px;"


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
            ui.div({"style":CSS_flexbox+CSS_border},ui.input_action_button("next_day","NEXT DAY")),
            width="300px"
        ),
        ui.navset_tab(
            ui.nav("ICON DISPLAY",
                ui.output_ui("ICON_current_day_info"),
                ui.output_ui("ICON_turbines"),
                ui.output_ui("ICON_teams")
            )
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
        system.next_day(strategy_B)

    @output
    @render.ui
    @reactive.event(input.next_day, input.reset)
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
        information =   ui.div({"style":CSS_completionbox},
                            ui.div({"style":CSS_infobox+CSS_blue_border},
                                ui.div({"style":CSS_flex_100_100},
                                    ui.img({"style":CSS_maxbox},src=wind_img)
                                )
                            ),
                            ui.div({"style":CSS_infobox+CSS_blue_border},
                                ui.div({"style":CSS_flex_100_100},
                                    ui.p({"style":CSS_maxbox+"font-weight:bold;font-size:40px;"},f"DAY {system.get_days_count()}")
                                )
                            ),
                            ui.div({"style":CSS_infobox+CSS_blue_border},
                                ui.div({"style":CSS_flex_100_100},
                                    ui.p({"style":CSS_maxbox+"font-weight:bold;font-size:15px;"},f"PRODUCTION {system.get_total_prod()}")
                                )
                            ),
                            ui.div({"style":CSS_infobox+CSS_blue_border},
                                ui.div({"style":CSS_flex_100_100},
                                    ui.p({"style":CSS_maxbox+"font-weight:bold;font-size:15px;"},f"COST {system.get_total_cost()}")
                                )
                            )
                        )
        return ui.div({"style":"display:block;"}, information)

    @output
    @render.ui
    @reactive.event(input.next_day, input.reset)
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
                                    ui.div({"style":CSS_linebox+CSS_black_border},
                                        ui.div({"style":CSS_flex_100_70},ui.img({"style":CSS_maxbox},src=img)),
                                        ui.div({"style":"height:100%;width:30%;"},
                                            ui.div({"style":CSS_flex_50_100},ui.p({"style":CSS_t_text},str(index+1))),
                                            ui.div({"style":CSS_flex_50_100},
                                                ui.div({"style":"display:flex;margin:auto;height:35px;width:35px;background-color:#55c9ff;border-radius:50%;"},
                                                    ui.p({"style":CSS_t_text},str(turbines[index].get_state()))))
                                        )
                                    )
                                )
                elif len(turbines)> j*WIDTH and len(turbines)< (j+1)*WIDTH : line.append(ui.div({"style":CSS_linebox}))
            if line != [] : all.append(ui.div({"style":CSS_completionbox},line))
        return ui.div({"style":"display:block;"},all)

    @output
    @render.ui
    @reactive.event(input.next_day, input.reset)
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
                    if teams[index].get_availability() : img, display_info = "team_on.png", ""
                    else : 
                        img = "team_off.png"
                        for (team, turbine) in planning.get_attribution() :
                            if team == teams[index].get_id() : display_info = str(turbine)
                    line.append (
                                    ui.div({"style":CSS_linebox+CSS_orange_border},
                                        ui.div({"style":CSS_flex_100_70},ui.img({"style":CSS_maxbox},src=img)),
                                        ui.div({"style":"height:100%;width:30%;"},
                                            ui.div({"style":CSS_flex_50_100},ui.p({"style":CSS_t_text},str(index+1))),
                                            ui.div({"style":CSS_flex_50_100},
                                                ui.div({"style":"display:flex;margin:auto;height:35px;width:30px;"+CSS_blue_border},
                                                    ui.p({"style":CSS_t_text},display_info)))
                                        )
                                    )
                                )
                elif len(teams) > j*WIDTH and len(teams) < (j+1)*WIDTH : line.append(ui.div({"style":CSS_linebox}))
            if line != [] : all.append(ui.div({"style":CSS_completionbox},line))
        return ui.div({"style":"display:block;"},all)


img_dir = Path(__file__).parent / "img_database"
app = App(app_ui, server, static_assets=img_dir, debug = False)
clear_cache.clear()
