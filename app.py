## IMPORT ##
import clear_cache 
from pathlib import Path

from main import *
from shiny import App, reactive, render, ui
from shiny.types import ImgData
############

system = System(20, 5)

color_dict = {1:"#37e171",2:"#a2ec5c",3:"#feab43",4:"#ff4444"}
strategy = {"A":strategy_A,"B":strategy_B, "C": strategy_C, "D": strategy_D}

CSS_flex_center_center = "display:flex;justify-content:center;align-items:center;"
CSS_stat_box = "width:33.33%;border:solid;"
CSS_stat_subbox = "display:flex;height:50%;"
CSS_stat_info_large = "font-weight:bold;font-size:15px;margin:auto;"
CSS_stat_info_small = "font-weight:bold;font-size:25px;margin:auto;"
CSS_H200 = "height:200px;"
CSS_W200 = "height:200px;"
CSS_img = "max-width:90%;max-height:90%;margin:auto;"

CSS_T_box = "display:flex;height:70px;width:120px;border:solid"
CSS_T_left = "display:flex;height:70px;width:70px;"
CSS_T_right = "height:70px;width:50px;"
CSS_T_text = "margin:auto;font-size:10px;" 

app_ui = ui.page_fluid(
    ui.p({"style":"font-size:5vh;margin:0;"},"MSSC"),
    ui.layout_sidebar(
        ui.sidebar({"style":"height:90vh;"},
            ui.div({"style":CSS_flex_center_center},ui.input_action_button("reset","RESET SYSTEM",width="200px")),
            ui.div({"style":"border:solid 1px;border-radius:5px;padding-top:15px;"},
                ui.div({"style":CSS_flex_center_center},
                    ui.p({"style":"width:100px;"},"TURBINES"),
                    ui.div({"style":"width:75px;"},ui.input_numeric("nb_turbines",  label=None,value=20,min=1,max=100,step=1))
                ),
                ui.div({"style":CSS_flex_center_center},
                    ui.p({"style":"width:100px;"},"TEAMS"),
                    ui.div({"style":"width:75px;"},ui.input_numeric("nb_teams",     label=None,value=5,min=1,max=100,step=1))
                ),
                ui.div({"style":CSS_flex_center_center},
                    ui.p({"style":"width:100px;"},"WIDTH"),
                    ui.div({"style":"width:75px;"},ui.input_numeric("width",        label=None,value=5,min=1,max=100,step=1))
                )
            ),
            ui.div({"style":CSS_flex_center_center},ui.input_action_button("next_day",   "NEXT DAY",     width="200px")),
            ui.div({"style":CSS_flex_center_center},ui.input_action_button("next_month", "NEXT MONTH",   width="200px")),
            ui.div({"style":CSS_flex_center_center},ui.input_action_button("next_year",  "NEXT YEAR",    width="200px")),
            ui.div({"style":CSS_flex_center_center},ui.input_action_button("end_year",   "END YEAR",     width="200px")),
            ui.div({"style":CSS_flex_center_center},ui.input_select("strategy_select","STRATEGY",{"A":"STRATEGY A","B":"STRATEGY B","C":"STRATEGY C","D":"STRATEGY D"}, width="200px")),
            width="250px"
        ),
        ui.navset_tab(
            ui.nav("ICON DISPLAY",
                ui.output_ui("ICON_statistics"),
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
        system.next_day(strategy[input.strategy_select()])

    @reactive.Effect
    @reactive.event(input.next_month)
    def next_month() :
        global system
        for i in range(30) :
            system.next_day(strategy[input.strategy_select()])

    @reactive.Effect
    @reactive.event(input.next_year)
    def next_year() :
        global system
        for i in range(365) :
            system.next_day(strategy[input.strategy_select()])

    @reactive.Effect
    @reactive.event(input.end_year)
    def end_year() :
        global system
        while system.get_days_count() % 365 != 0 :
            system.next_day(strategy[input.strategy_select()])
    
    @output
    @render.ui
    @reactive.event(input.next_day, input.next_month, input.next_year, input.end_year, input.reset, input.width)
    def ICON_statistics() :
        global system
        wind = system.get_wind()
        match wind :
            case 1 :
                wind_img = "wind_low.gif"
            case 2 :
                wind_img = "wind_medium.gif"
            case 3 :
                wind_img = "wind_high.gif"
        information =   ui.div({"style":CSS_flex_center_center+CSS_H200},
                            ui.div({"style":CSS_flex_center_center+CSS_H200+CSS_W200+"border:solid;"},
                                ui.img({"style":CSS_img},src=wind_img)
                            ),
                            ui.div({"style":CSS_H200+"width:calc(100% - 200px);"},
                                ui.div({"style":CSS_stat_subbox},
                                    ui.div({"style":CSS_stat_box},
                                        ui.div({"style":CSS_stat_subbox},ui.p({"style":CSS_stat_info_large}, "PROD")),
                                        ui.div({"style":CSS_stat_subbox},ui.p({"style":CSS_stat_info_large}, "%d"%(system.get_total_prod()))),
                                    ),
                                    ui.div({"style":CSS_stat_box},
                                        ui.div({"style":CSS_stat_subbox},ui.p({"style":CSS_stat_info_large}, "COST")),
                                        ui.div({"style":CSS_stat_subbox},ui.p({"style":CSS_stat_info_large}, "%d"%(system.get_total_cost()))),
                                    ),
                                    ui.div({"style":CSS_stat_box},
                                        ui.div({"style":CSS_stat_subbox},ui.p({"style":CSS_stat_info_large}, "COST/PROD")),
                                        ui.div({"style":CSS_stat_subbox},ui.p({"style":CSS_stat_info_large}, "%d"%(system.get_total_cost()/system.get_total_prod() if system.get_total_prod() != 0 else 0)))
                                    ),
                                ),
                                ui.div({"style":CSS_stat_subbox},
                                    ui.div({"style":CSS_stat_box},
                                        ui.div({"style":CSS_stat_subbox},ui.p({"style":CSS_stat_info_small}, "TURBINE")),
                                        ui.div({"style":CSS_stat_subbox},ui.p({"style":CSS_stat_info_small}, "%d"%(system.get_turbine_occupation_percentage()) + "%"))
                                    ),
                                    ui.div({"style":CSS_stat_box},
                                        ui.div({"style":CSS_stat_subbox},ui.p({"style":CSS_stat_info_small}, "TEAM")),
                                        ui.div({"style":CSS_stat_subbox},ui.p({"style":CSS_stat_info_small}, "%d"%(system.get_team_occupation_percentage()) + "%"))
                                    ),
                                    ui.div({"style":CSS_stat_box},
                                        ui.div({"style":CSS_stat_subbox},ui.p({"style":CSS_stat_info_small}, "DAY")),
                                        ui.div({"style":CSS_stat_subbox},ui.p({"style":CSS_stat_info_small}, "%d"%(system.get_days_count())))
                                    ),
                                )
                            )
                        )
        return ui.div({"style":"display:block;margin-bottom:10px;"}, information)

    @output
    @render.ui
    @reactive.event(input.next_day, input.next_month, input.next_year, input.end_year, input.reset, input.width)
    def ICON_turbines() :
        global system
        turbines = system.get_turbines()
        necessary_lines = (len(turbines) - 1) // input.width() + 1
        all_lines = []
        for i in range(necessary_lines) :
            current_line = []
            for j in range(input.width()) :
                index = i*input.width() + j
                if index < len(turbines) :
                    if turbines[index].get_state() != 4 :   img = "turbine_on.png"
                    else :                                  img = "turbine_off.png"
                    operating_time_percentage = 100*turbines[index].get_operating_days_count()/system.get_wind_days_count() if system.get_wind_days_count() != 0 else 0
                    current_line.append (
                        ui.div({"style":CSS_T_box},
                            ui.div({"style":CSS_T_left},
                                ui.img({"style":CSS_img},src=img)
                            ),
                            ui.div({"style":CSS_T_right},
                                ui.div({"style":CSS_flex_center_center+"height:25%;"},
                                    ui.p({"style":CSS_T_text+"font-weight:bold;"},"n° "+str(turbines[index].get_id()))
                                ),
                                ui.div({"style":CSS_flex_center_center+"height:25%;margin-bottom:5px;"},
                                    ui.p({"style":CSS_T_text+"padding:2px;background-color:%s;border-radius:5px;"%(color_dict[turbines[index].get_state()])},"state "+str(turbines[index].get_state()))
                                ),
                                ui.div({"style":CSS_flex_center_center+"height:40%;"},
                                    ui.p({"style":CSS_T_text},"%2.2f"%(operating_time_percentage)+" %")
                                )
                            )
                        )
                    )
                else : 
                    current_line.append(ui.div({"style":CSS_T_box}))
            all_lines.append(ui.div({"style":"display:flex;margin-bottom:10px;justify-content:space-between;"},current_line))
        return ui.div({"style":"display:block;"},all_lines)

    @output
    @render.ui
    @reactive.event(input.next_day, input.next_month, input.next_year, input.end_year, input.reset, input.width)
    def ICON_teams() :
        global system
        teams = system.get_teams()
        necessary_lines = (len(teams) - 1) // input.width() + 1
        planning = system.get_planning()
        all_lines = []
        for i in range(necessary_lines) :
            current_line = []
            for j in range(input.width()) :
                index = i*input.width() + j
                if index < len(teams) :
                    if teams[index].get_availability() : img, display_info = "team_on.png", ""
                    else : 
                        img = "team_off.png"
                        for (team, turbine) in planning.get_attribution() :
                            if team == teams[index].get_id() : display_info = str(turbine)
                    operating_time_percentage = 100*teams[index].get_operating_days_count()/system.get_wind_days_count() if system.get_wind_days_count() != 0 else 0
                    current_line.append (
                        ui.div({"style":CSS_T_box},
                            ui.div({"style":CSS_T_left},
                                ui.img({"style":CSS_img},src=img)
                            ),
                            ui.div({"style":CSS_T_right},
                                ui.div({"style":CSS_flex_center_center+"height:25%;"},
                                    ui.p({"style":CSS_T_text+"font-weight:bold;"},"n° "+str(teams[index].get_id()))
                                ),
                                ui.div({"style":CSS_flex_center_center+"height:25%;margin-bottom:5px;"},
                                    ui.p({"style":CSS_T_text+"padding:2px;border:solid;border-radius:5px;"},display_info)
                                ),
                                ui.div({"style":CSS_flex_center_center+"height:40%;"},
                                    ui.p({"style":CSS_T_text},"%2.2f"%(operating_time_percentage)+" %")
                                )
                            )
                        )    
                    )
                else : 
                    current_line.append(ui.div({"style":CSS_T_box}))
            all_lines.append(ui.div({"style":"display:flex;margin-bottom:10px;justify-content:space-between;"},current_line))
        return ui.div({"style":"display:block;"},all_lines)


img_dir = Path(__file__).parent / "img_database"
app = App(app_ui, server, static_assets=img_dir, debug = False)
clear_cache.clear()
