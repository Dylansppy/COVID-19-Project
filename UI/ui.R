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
    titlePanel("COVID-19 Visualization and Analysis Tool - Peng Shen (Dylan)"),
    
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
                    selectInput("data_select","Select a dataset", choices=c('Country_Level_Info.csv','Null'), selected='Country_Level_Info.csv'),
                    fileInput("file", label = "Or Import a CSV file"),
                    checkboxInput("rownames", "Show Row Names", value=T),
                    checkboxInput("order", "Column Ordering", value=T),
                    selectInput("selection", "Selection Type", choices=c("none","single","multiple"), selected = "none"),
                    selectInput("filter", "Filter Type", choices=c("none","top","bottom"), selected = "none"),
                    selectInput("dom", "DOM", choices=domChoices, multiple = TRUE, selected=domChoices)
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
            title = "Data Vasulization",
            tabsetPanel(
                # Timeseries Panel
                tabPanel(title="Timeseries",
                         icon=icon("chart-line"),
                         sidebarLayout(
                             sidebarPanel(
                                 uiOutput("Country_select"),
                                 uiOutput("Timeseries_select")
                             ),
                             mainPanel(
                                 plotOutput("time")
                             )
                         )
                )
            )
        ),
        
        # Modelling Panel
        tabPanel(
            title = "Epidemic Model",
            tabsetPanel(
                tabPanel(title = "SIR Model",
                         sidebarLayout(
                             sidebarPanel(
                                 uiOutput("Country"),
                                 sliderInput("β",
                                             "Infection Coefficient",
                                             min = 10,
                                             max = 100,
                                             value = 80
                                 ),
                                 sliderInput("gamma",
                                             "Recovery Rate",
                                             min = 10,
                                             max = 100,
                                             value = 80
                                 ),
                                 sliderInput("u",
                                             "Motality Rate",
                                             min = 10,
                                             max = 100,
                                             value = 80
                                 )
                             ),
                             mainPanel(
                                 
                             )
                        )
                ),
                tabPanel(title = "SEIR Model"
                )
            )
        )
    )
))
