# Host a web application with Azure App Service

Hosting your web application using Azure App Service makes deploying and managing a web app easier when compared to managing a physical server. Azure App Service is a fully managed web application hosting platform. This platform as a service (PaaS) offered by Azure allows you to focus on designing and building your app while Azure takes care of the infrastructure to run and scale your applications.

The first step in hosting your web application is to create a web app (an Azure App Service app) inside your Azure subscription.
- There are several ways you can create a web app. You can use the Azure portal, the Azure Command Line Interface (CLI), a script, or an integrated development environment (IDE) like Visual Studio.

## Deployment

You can deploy your application to App Service as code or as a ready-to-run Docker Container. 
- Selecting Container activates the wizard's Container tab, where you provide information about the Docker registry from which App Service retrieves your image.
- If you choose to deploy your application as code, App Service needs to know what runtime your application uses (examples include Node.js, Python, Java, and .NET). 

The command az webapp up packages up our application and sends it to our App Service instance, where the app is built and deployed.

## Billing

The size of each App Service plan in your subscription, in addition to the bandwidth resources the apps deployed to those plans use, determines the price you pay. The number of web apps deployed to your App Service plans has no effect on your bill.

## Setup
- Create a Web App resource in portal.azure (App Service and App Service plan)
- Verify resource deployment by pasting the "Default domain URL" into the browser, giving the default landing page
- Start a terminal in portal.azure and run commands:
  - Linux:
    ```
    export APPNAME=$(az webapp list --query [0].name --output tsv)
    export APPRG=$(az webapp list --query [0].resourceGroup --output tsv)
    export APPPLAN=$(az appservice plan list --query [0].name --output tsv)
    export APPSKU=$(az appservice plan list --query [0].sku.name --output tsv)
    export APPLOCATION=$(az appservice plan list --query [0].location --output tsv)
    ```
  - PowerShell:
    ```
    $Env:APPNAME = (az webapp list --query "[0].name" --output tsv)
    $Env:APPRG = (az webapp list --query "[0].resourceGroup" --output tsv)
    $Env:APPPLAN = (az appservice plan list --query "[0].name" --output tsv)
    $Env:APPSKU = (az appservice plan list --query "[0].sku.name" --output tsv)
    $Env:APPLOCATION = (az appservice plan list --query "[0].location" --output tsv)
    ```
- Assuming the application files are located at `/code/templates/azure/web-app`, run
  ```
  Set-Location ~/code/templates/azure/web-app
  ```
- From the app directory, run:
    ```
    az webapp up `
    --name $Env:APPNAME `
    --resource-group $Env:APPRG `
    --plan $Env:APPPLAN `
    --sku $Env:APPSKU `
    --location "$Env:APPLOCATION"
    ```
