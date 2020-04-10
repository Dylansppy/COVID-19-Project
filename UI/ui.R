#
# This is the user-interface definition of a Shiny web application. You can
# run the application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

#library(shiny)
#library(shinyjs)
#data(iris)
#data(Glass)

domChoices <- c("l","f","r","t","i","p")
    
    
# Define UI for application 
shinyUI(fluidPage(
    # Application title
    #titlePanel("COVID-19 Visualization and Analysis Tool"),
    
    
    # Print Option
    tags$head(tags$style(HTML("
                            #Data_Str {
                              font-size: 20px;
                              font-weight: bold;
                            }
                            #Des_K-means {
                              font-size: 20px;
                              font-weight: bold;
                            }
                            #DBscan_title {
                              font-size: 20px;
                              font-weight: bold;
                            }
                            "))),
               
    # Tabset
    navbarPage(theme = shinytheme("flatly"), collapsible = TRUE,"COVID-19 Visualization and Analysis Tool", id="nav",
        tabPanel("Global Map",
             div(class="outer",
                 #tags$head(includeCSS("styles.css")),
                 tags$style(type = "text/css", ".outer {position: fixed; top: 0; left: 0; right: 0; bottom: 0; overflow: auto; padding: 0}"),
                 # Map Panel
                 htmlOutput("map"),
                 absolutePanel(id = "controls", class = "panel-default",
                               top = 268, left = -55, width = 250, fixed=TRUE,
                               draggable = TRUE, height = "auto",
                               h6(textOutput("reactive_date"), align = "middle"),
                               h3(textOutput("reactive_case_count"), align = "right"),
                               span(h4(textOutput("reactive_death_count"), align = "right"),style="color:#cc4c02"),
                               span(h4(textOutput("reactive_recovered_count"), align = "right"), style="color:#006d2c"),
                               span(h4(textOutput("reactive_active_count"), align = "right"))
                               #h6(textOutput("reactive_country_count"), align = "right"),
                               #tags$i(h6("Updated once daily. For more regular updates, refer to: ", tags$a(href="https://gisanddata.maps.arcgis.com/apps/opsdashboard/index.html#/bda7594740fd40299423467b48e9ecf6", "Johns Hopkins COVID-19 dashboard.")))
                 )
        )),
        
        # Data vasualization panel
        tabPanel(
            title = "Country-level Trend",
            # Timeseries Panel
            sidebarLayout(
                sidebarPanel(
                    uiOutput("Country_select"),
                    uiOutput("Timeseries_select"),
                    htmlOutput("latest_case")
                ),
                mainPanel(
                    plotlyOutput("time"),
                    tags$i(h6("Reported cases are subject to significant variation in testing capacity between countries.",
                              align = "right"))
                )
            )
        ),
        
        # Modelling Panel
        tabPanel(
            title = "Epidemic Model",
            tabsetPanel(
                #tabPanel(title = "Parameter Estimation",
                         #textOutput("Developing")
                #),
                tabPanel(title = "SIR Model",
                         sidebarLayout(
                             sidebarPanel(
                                 uiOutput("Country1"),
                                 sliderInput("beta",
                                             "Infection Coefficient",
                                             min = 0,
                                             max = 1,
                                             value = 0.8
                                 ),
                                 sliderInput("gamma",
                                             "Recovery Rate",
                                             min = 0,
                                             max = 1,
                                             value = 0.5
                                 ),
                                 sliderInput("u",
                                             "Motality Rate",
                                             min = 0,
                                             max = 1,
                                             value = 0.1
                                 )
                             ),
                             mainPanel(
                                 plotOutput("SIR")
                             )
                        )
                ),
                tabPanel(title = "SEIR Model",
                         sidebarLayout(
                             sidebarPanel(
                                 uiOutput("Country2"),
                                 sliderInput("beta2",
                                             "Infection Coefficient",
                                             min = 0,
                                             max = 1,
                                             value = 0.8
                                 ),
                                 sliderInput("alpha",
                                             "Overt Rate",
                                             min = 0,
                                             max = 1,
                                             value = 0.5
                                 ),
                                 sliderInput("gamma2",
                                             "Recovery Rate",
                                             min = 0,
                                             max = 1,
                                             value = 0.5
                                 ),
                                 sliderInput("u2",
                                             "Motality Rate",
                                             min = 0,
                                             max = 1,
                                             value = 0.1
                                 )
                             ),
                             mainPanel(
                                 plotOutput("SEIR")
                             )
                         )
                )
            )
        ),
        
        # Dataset Panel
        tabPanel(title = "About Data",
                 tabsetPanel(
                     tabPanel(
                         title = "Dataset",
                         sidebarLayout(
                             sidebarPanel(
                                 selectInput("data_select","My Dataset", choices=c('Country_Level_Info.csv','Null'), selected='Country_Level_Info.csv'),
                                 fileInput("file", label = "Or Import a CSV file"),
                                 checkboxInput("rownames", "Show Row Names", value=T),
                                 checkboxInput("order", "Column Ordering", value=T),
                                 selectInput("selection", "Selection Type", choices=c("none","single","multiple"), selected = "none"),
                                 selectInput("filter", "Filter Type", choices=c("none","top","bottom"), selected = "none"),
                                 selectInput("dom", "DOM", choices=domChoices, multiple = TRUE, selected=domChoices)
                             ),
                             mainPanel(DT::dataTableOutput("Dataset")
                             )
                         )
                     ),
                     
                     #Summary panel
                     tabPanel(
                         title = "Summary",
                         verbatimTextOutput("Summary")
                     )
                 )
        ),
        
        # About Author
        tabPanel(title = "About Author",
                 tags$h5("Peng Shen (Dylan)"),
                 tags$h5(a("Dataset", href="https://www.kaggle.com/dylansp/covid19-country-level-data-for-epidemic-model", target="_blank")),
                 tags$h5(a("Github", href="https://github.com/Dylansppy/COVID-19-Project", target="_blank")),
                 tags$h5(a("Website", href="https://dylan-portfolio-app.herokuapp.com", target="_blank")),
                 tags$h5(a("Linkedin", href="https://www.linkedin.com/in/dylan-shen-peng", target="_blank"))
        )
    )
))
