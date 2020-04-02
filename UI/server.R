#
# This is the server logic of a Shiny web application. You can run the
# application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

#library(shiny)
#library(DT)
#library(MASS)
#library(mlbench)
#library(tidyverse)
#library(ggplot2)
#library(reshape2)
#library(caret)
#data(iris)
#data(Glass)

# Define server logic 
shinyServer(function(input, output) {
    # https://datatables.net/reference/option/dom
    
    # https://datatables.net/extensions/index
    ext <- list(Responsive = TRUE)
    
    # Get the data
    data <- reactive({
        if (input$data_select!='Null') {
            read.csv(input$data_select, header=TRUE)
        } else {
            read.csv(input$file)
        }
    })
    
    # DataTable
    output$Dataset <- DT::renderDataTable({
        DT::datatable(data = data(),
                      rownames = input$rownames,
                      selection = input$selection,
                      filter = list(position = input$filter),
                      options = list(searching = TRUE,
                                     pageLength = 10,
                                     lengthMenu = c(10, 100, 300),
                                     dom = paste(input$dom, collapse = ""),
                                     ordering = input$order
                      ),
                      extensions = ext
        )  %>%
        formatStyle(columns = 1, backgroundColor = "lightblue")  #%>%
        #formatCurrency(c(2), '$') %>%
        #formatPercentage(3, 2) %>%
        #formatRound(c("hp"), 3)
    })
    
    # Title of data structure
    output$Data_Str <- renderText({
        "Data Structure"
    })
    
    # Dataset structure
    output$Structure <- renderPrint({
        str(data())
    })
    
    # Summary statistics
    output$Summary <- renderPrint({
        summarytools::dfSummary(data(),
                  method = 'render',
                  omit.headings = TRUE,
                  bootstrap.css = FALSE)
    })
    
    # Description of summary
    output$Summary_result <- renderText({
        "Description - There is no missing data in the iris and Glass dataset and
        a total of 150 and 214 observations in iris and Glass dataset respectively.
        All the predictors are numeric in iris and Glass dataset.
        Outcome variable in iris dataset is a factor variable with 3 levels, 
        while in Glass dataset the outcome variable is a factor variable with 6 levels.
        "
    })
    
    # Target variable visualization using timeseries plot
    tar_name <- reactive({
        names(data() %>% select_if(is.numeric))
    })
    
    output$Country_select <- renderUI({
        selectInput("country","Country/Region", choices=unique(data()[,"Country_Region"]), selected="New Zealand")
    })
    
    output$Timeseries_select <- renderUI({
        selectInput("target1","Case", choices=tar_name(), selected=tar_name()[4])
    })
    
    # Timeseries plot
    output$time <- renderPlot({
        # choose the numeric columns
        subdata <- data()[data()[,'Country_Region'] == input$country, ]
        subdata$Date <- as.Date(subdata$Date)
        #tsdat <- ts(numData, frequency=6, start=c(2020, 1), end=c(2020,3))
        ggplot(data = subdata, aes(x = Date, y = get(input$target1))) + geom_line(linetype = "dashed") +
        geom_point() + xlab("Date") + ylab(input$target1)
            #tsdat, main="Timeseries of Numerical Variables", type = "l", col = alpha(rainbow(ncol(numData)), 0.4), xlab = "Date", ylab = "Values" ) 
    })
    
    #Epidemic Model
    # SIR Model
    output$Country <- renderUI({
        selectInput("country_epi","Select Country/Region", choices=unique(data()[,"Country_Region"]), selected=unique(data()[,"Country_Region"])[1])
    })
})
