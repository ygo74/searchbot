using kernel_internet_search;
using kernel_internet_search.Configuration;
using kernel_internet_search.Monitoring;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.ChatCompletion;
using Microsoft.SemanticKernel.Connectors.OpenAI;
using Microsoft.SemanticKernel.Plugins.Core;
using Microsoft.SemanticKernel.Plugins.Web;
using Serilog;
using Microsoft.KernelMemory;
using kernel_internet_search.Plugins;
using kernel_internet_search.Filters;

// See https://aka.ms/new-console-template for more information
Console.WriteLine("Start Kernel Internet search!");

// Enable model diagnostics with sensitive data.
AppContext.SetSwitch("Microsoft.SemanticKernel.Experimental.GenAI.EnableOTelDiagnosticsSensitive", true);

Log.Logger = new LoggerConfiguration()
         .MinimumLevel.Information()
         .MinimumLevel.Override("Microsoft.SemanticKernel", Serilog.Events.LogEventLevel.Debug)
         .WriteTo.Console()
         .CreateLogger();


HostApplicationBuilder hostBuilder = Host.CreateApplicationBuilder(args);

hostBuilder.Services.AddLogging();
hostBuilder.AddTelemetryService();

// Actual code to execute is found in Worker class

hostBuilder.Services.AddHostedService<WorkerMemoryKernelWebClient>();
//hostBuilder.Services.AddHostedService<InternetSearcher>();
//hostBuilder.Services.AddHostedService<WorkerWithPlaner>();
//hostBuilder.Services.AddHostedService<Worker>();
//hostBuilder.Services.AddHostedService<WorkerWithAgents>();
//hostBuilder.Services.AddHostedService<InternetSearcherAgent>();


hostBuilder.Configuration
      .AddJsonFile("appsettings.json")
      .AddJsonFile("appsettings.Development.json", optional: true)
      .AddEnvironmentVariables();


// Get configuration
hostBuilder.Services.AddOptions<AzureOpenAIConfig>()
                    .Bind(hostBuilder.Configuration.GetSection(nameof(AzureOpenAIConfig)))
                    .ValidateDataAnnotations()
                    .ValidateOnStart();

hostBuilder.Services.AddOptions<GoogleConnectorConfig>()
                    .Bind(hostBuilder.Configuration.GetSection(nameof(GoogleConnectorConfig)))
                    .ValidateDataAnnotations()
                    .ValidateOnStart();


// Chat completion service that kernels will use
hostBuilder.Services.AddSingleton<IChatCompletionService>(sp =>
{
    AzureOpenAIConfig config = sp.GetRequiredService<IOptions<AzureOpenAIConfig>>().Value;

    return new AzureOpenAIChatCompletionService(config.Deployment, config.Endpoint, config.APIKey);
});

// Define plugins
#pragma warning disable SKEXP0001, SKEXP0010, SKEXP0020, SKEXP0050
hostBuilder.Services.AddSingleton<WebSearchEnginePlugin>(sp =>
{
    GoogleConnectorConfig config = sp.GetRequiredService<IOptions<GoogleConnectorConfig>>().Value;
    var googleConnector = new Microsoft.SemanticKernel.Plugins.Web.Google.GoogleConnector(
            apiKey: config.APIKey,
            searchEngineId: config.SearchCenterConnectionId);

    var google = new WebSearchEnginePlugin(googleConnector);
    return google;

});

hostBuilder.Services.AddSingleton<MemoryPlugin>(sp =>
{
    var s_memory = new MemoryWebClient("http://127.0.0.1:9001/");

    return new MemoryPlugin(s_memory, waitForIngestionToComplete: true);
});

// Add Kernel to the dependency injection container
hostBuilder.Services.AddTransient<Kernel>(sp =>
{
    // Create a collection of plugins that the kernel will use
    KernelPluginCollection pluginCollection = [];
    pluginCollection.AddFromObject(sp.GetRequiredService<WebSearchEnginePlugin>());
    //pluginCollection.AddFromObject(sp.GetRequiredService<MemoryPlugin>(), "memory", sp);
    pluginCollection.AddFromObject(new ScrapeWebpagePlugin(), "webscraper", sp);

    // Logger
    var loggerFactory = sp.GetRequiredService<ILoggerFactory>();
    var Kernel = new Kernel(sp, pluginCollection);
    Kernel.LoggerFactory.AddSerilog();

#pragma warning disable SKEXP0001
    Kernel.PromptRenderFilters.Add(new DisplayPrompt(loggerFactory));
    Kernel.FunctionInvocationFilters.Add(new DisplayFunction(loggerFactory));
#pragma warning restore SKEXP0001


    return Kernel;
    //IKernelBuilder builder = Kernel.CreateBuilder();


    //var kernel = builder.Build();
    //kernel.ImportPluginFromObject(sp.GetRequiredService<WebSearchEnginePlugin>());

    //return kernel;
});
#pragma warning restore SKEXP0001, SKEXP0010, SKEXP0020, SKEXP0050




using IHost host = hostBuilder.Build();
await host.RunAsync();


//var azureOpenAITextConfig = new AzureOpenAIConfig();
//var googleConnectorConfig = new GoogleConnectorConfig();

//var configuration = new ConfigurationBuilder()
//    .AddJsonFile("appsettings.json")
//    .AddJsonFile("appsettings.Development.json", optional: true)
//    .AddEnvironmentVariables()
//    .Build()
//    .BindSection("AzureOpenAIConfig", azureOpenAITextConfig)
//    .BindSection("GoogleConnector", googleConnectorConfig);

//Console.WriteLine($"Service Endpoint : {azureOpenAITextConfig.Endpoint}");

////Create Kernel builder
//Console.WriteLine($"Create Kernel Builder");
//var builder = Kernel.CreateBuilder();
//builder.AddAzureOpenAIChatCompletion(
//    deploymentName: azureOpenAITextConfig.Deployment,
//    endpoint: azureOpenAITextConfig.Endpoint,
//    apiKey: azureOpenAITextConfig.APIKey
//);
//// Logger
//builder.Services.AddLogging(c => c.AddDebug().SetMinimumLevel(LogLevel.Trace));

//var kernel = builder.Build();

//// Define plugins
//#pragma warning disable SKEXP0001, SKEXP0010, SKEXP0020, SKEXP0050
//var googleConnector = new Microsoft.SemanticKernel.Plugins.Web.Google.GoogleConnector(
//        apiKey: googleConnectorConfig.APIKey,
//        searchEngineId: googleConnectorConfig.SearchCenterConnectionId);

//var google = new WebSearchEnginePlugin(googleConnector);
//kernel.ImportPluginFromObject(new WebSearchEnginePlugin(googleConnector), "google");
//#pragma warning restore SKEXP0001, SKEXP0010, SKEXP0020, SKEXP0050

//// Retrieve the chat completion service from the kernel
//IChatCompletionService chatCompletionService = kernel.GetRequiredService<IChatCompletionService>();

//// Create the chat history
//var internet_searcher = """
//You are a world class researcher, who can detailed research on any topic and produce facts based results;
//You do not make things up, you will try as hard as possible to gather facts and data to back up the research.

//You have the functions google_search to find elements on the web.
//You have the functions scrape_website to rerieve content of a page.
//if you have to search a person, use simple quote for the first name and last name. If you want to limit a query to a specific site, use site keyword to limit the search to a specific site

//Please make sure you complete the objective above with the following rules:
//1. You should do enough research to gather as much information as possible about the objective
//2. If there are url of relevant links and articles, you will scrape it with the scrape_website function to gather more information
//3. After scraping and search, you should think "Is there any new things I should search and scraping based on the data I collected to increase research quality? If answer is yes, continue; But don' do this more than 3 iterations.
//4. You should not make things up, you should only write facts and data that you gathered
//5. In the final output, You should include all reference data and links to back up your research.
//6. Do not use G2, they are mostly out dated data

//SAY TERMINATE when you found the result.

//---
//Here are expected examples :

//Example :
//question : search devops on github
//query : devops site:github.com

//Example :
//question : find contribution for code from Yannick GOBERT a devops engineer on internet, he can be known with his alias ygo or ygo74
//query : contribution for code from 'Yannick GOBERT' devops engineer

//Example :
//question : find contribution for code from Yannick GOBERT a devops engineer on internet, he can be known with his alias ygo or ygo74
//query : contribution for code from 'YGO74' devops engineer


//""";

////ChatHistory chatMessages = new ChatHistory("""
////You are a friendly assistant who likes to follow the rules. You will complete required steps
////and request approval before taking any consequential actions. If the user doesn't provide
////enough information for you to complete a task, you will keep asking questions until you have
////enough information to complete the task.
////""");

//ChatHistory chatMessages = new ChatHistory(internet_searcher);

//// Start the conversation
//while (true)
//{
//    // Get user input
//    System.Console.Write("User > ");
//    chatMessages.AddUserMessage(Console.ReadLine()!);

//    // Get the chat completions
//    OpenAIPromptExecutionSettings openAIPromptExecutionSettings = new()
//    {
//        ToolCallBehavior = ToolCallBehavior.AutoInvokeKernelFunctions
//    };

//    var result = chatCompletionService.GetStreamingChatMessageContentsAsync(
//        chatMessages,
//        executionSettings: openAIPromptExecutionSettings,
//        kernel: kernel);

//    // Stream the results
//    string fullMessage = "";
//    await foreach (var content in result)
//    {
//        if (content.Role.HasValue)
//        {
//            System.Console.Write("Assistant > ");
//        }
//        System.Console.Write(content.Content);
//        fullMessage += content.Content;
//    }
//    System.Console.WriteLine();

//    // Add the message from the agent to the chat history
//    chatMessages.AddAssistantMessage(fullMessage);
//}
