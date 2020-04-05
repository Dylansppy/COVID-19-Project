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
    titlePanel("COVID-19 Visualization and Analysis Tool"),
    
    
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
    tabsetPanel(
        # Dataset Panel
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
                    selectInput("dom", "DOM", choices=domChoices, multiple = TRUE, selected=domChoices),
                    tags$h5("Author: Peng Shen (Dylan)"),
                    tags$h5(a("Dataset", href="https://www.kaggle.com/dylansp/covid19-country-level-data-for-epidemic-model", target="_blank")),
                    tags$h5(a("Github", href="https://github.com/Dylansppy/COVID-19-Project", target="_blank")),
                    tags$h5(a("Website", href="https://dylan-portfolio-app.herokuapp.com", target="_blank")),
                    tags$h5(a("Linkedin", href="https://www.linkedin.com/in/dylan-shen-peng", target="_blank"))
                ),
                mainPanel(DT::dataTableOutput("Dataset"),
                          textOutput("Data_Str"),
                          verbatimTextOutput("Structure")
                          )
            )
        ),
        
        #Summary panel
        tabPanel(
            title = "Summary",
            verbatimTextOutput("Summary"),
            textOutput("Summary_result")
        ),
        
        # Data vasualization panel
        tabPanel(
            title = "Vasulization",
            tabsetPanel(
                # Map Panel
                tabPanel(title="Global Situation",
                         htmlOutput("map")
                ),
                # Timeseries Panel
                tabPanel(title="Country-Level Trend",
                         icon=icon("chart-line"),
                         sidebarLayout(
                             sidebarPanel(
                                 uiOutput("Country_select"),
                                 uiOutput("Timeseries_select")
                             ),
                             mainPanel(
                                 plotlyOutput("time"),
                                 htmlOutput("latest_case")
                             )
                         )
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
        )
    )
))
