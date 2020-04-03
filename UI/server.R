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
    
    # Latest Case
    output$latest_case <- renderUI({
        subdata <- data()[data()$Country_Region == input$country,]
        str0 <- paste("Latest Situation on", subdata[nrow(subdata), 'Date'], ":")
        str1 <- paste("New Confirmed Case: " , subdata[nrow(subdata), 'New_Confirmed_Cases'])
        str2 <- paste("New Recovered Case: " , subdata[nrow(subdata), 'New_Recovered_Cases'])
        str3 <- paste("New Fatalities: " , subdata[nrow(subdata), 'New_Fatalities'])
        str4 <- paste("Active Confirmed Case: " , subdata[nrow(subdata), 'Remaining_Confirmed_Cases'])
        str5 <- paste("Cumulative Confirmed Case: " , subdata[nrow(subdata), 'Total_Confirmed_Cases'])
        str6 <- paste("Cumulative Recovered Case: " , subdata[nrow(subdata), 'Total_Recovered_Cases'])
        str7 <- paste("Cumulative Fatalities: " , subdata[nrow(subdata), 'Total_Fatalities'])
        HTML(paste(str0, str1, str2, str3, str4, str5, str6, str7, sep = '<br/>'))
        
    })
    
    #Epidemic Model
    # SIR Model
    output$Country1 <- renderUI({
        selectInput("country1","Select Country/Region", choices=unique(data()[,"Country_Region"]), selected="New Zealand")
    })
    
    output$SIR <- renderPlot({
        subdata2 <- data()[data()$Country_Region == input$country1,]
        # Initial case numbers
        N = subdata2[nrow(subdata2), 'Population']
        I = 1
        S = N-I
        R = 0
        D = 0
        
        # Coefficient
        beta = input$beta
        gamma = input$gamma
        u = input$u
        T = 365
        
        #equation
        for (i in 1:(T-1)){
            S[i+1] = S[i] - beta*S[i]*I[i]/N
            I[i+1] = I[i] + beta*S[i]*I[i]/N - gamma*I[i] - u*I[i]
            R[i+1] = R[i] + gamma*I[i]
            D[i+1] = D[i] + u*I[i]
        }
        result <- data.frame(S, I, R, D)
        X_lim <- seq(1,T,by=1)
        plot(S~X_lim, pch=15, col="DarkTurquoise", main = "SIR Model", type = "l", xlab = "Day", ylab = "Number of Cases", xlim = c(0,T), ylim = c(0, N))
        lines(S, col="DeepPink", lty=1) 
        lines(I, col="RosyBrown", lty=1)
        lines(R, col="Green", lty=1)
        lines(D, col="DarkTurquoise", lty=1)
        legend(280,N,c("Susceptible","Infected","Recovered", "Dead"),col=c("DeepPink","RosyBrown","Green","DarkTurquoise"),text.col=c("DeepPink","RosyBrown","Green", "DarkTurquoise"),lty=c(1,1,1,1))
    })
    
    # SEIR Model
    output$Country2 <- renderUI({
        selectInput("country2","Select Country/Region", choices=unique(data()[,"Country_Region"]), selected="New Zealand")
    })
    
    output$SEIR <- renderPlot({
        subdata3 <- data()[data()$Country_Region == input$country2,]
        # Initial case numbers
        N = subdata3[nrow(subdata3), 'Population']
        I = 1
        E = 0
        S = N-I
        R = 0
        D = 0
        
        # Coefficient
        beta = input$beta2
        gamma = input$gamma2
        alpha = input$alpha
        u = input$u2
        T = 365
        
        #equation
        for (i in 1:(T-1)){
            S[i+1] = S[i] - beta*S[i]*I[i]/N
            E[i+1] = E[i] + beta*S[i]*I[i]/N - alpha*E[i]
            I[i+1] = I[i] + alpha*E[i] - gamma*I[i] - u*I[i]
            R[i+1] = R[i] + gamma*I[i]
            D[i+1] = D[i] + u*I[i]
        }
        result <- data.frame(S, E, I, R, D)
        X_lim <- seq(1,T,by=1)
        plot(S~X_lim, pch=15, col="DarkTurquoise", main = "SEIR Model", type = "l", xlab = "Day", ylab = "Number of Cases", xlim = c(0,T), ylim = c(0, N))
        lines(S, col="DeepPink", lty=1) 
        lines(E, col="Orange", lty=1)
        lines(I, col="RosyBrown", lty=1)
        lines(R, col="Green", lty=1)
        lines(D, col="DarkTurquoise", lty=1)
        legend(280,N,c("Susceptible","Exposed","Infected","Recovered", "Dead"),col=c("DeepPink","Orange","RosyBrown","Green","DarkTurquoise"),text.col=c("DeepPink","Orange","RosyBrown","Green", "DarkTurquoise"),lty=c(1,1,1,1,1))
    })
})
