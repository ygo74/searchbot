using kernel_internet_search.Filters;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.ChatCompletion;
using Microsoft.SemanticKernel.Connectors.OpenAI;
using Microsoft.SemanticKernel.PromptTemplates.Handlebars;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Threading.Tasks;

namespace kernel_internet_search
{
    internal class InternetSearcher(
        IHostApplicationLifetime hostApplicationLifetime,
        Kernel kernel, IChatCompletionService chatCompletionService,
        ILogger<WorkerWithPlaner> logger) : BackgroundService
    {
        private readonly IHostApplicationLifetime _hostApplicationLifetime = hostApplicationLifetime;
        private readonly Kernel _kernel = kernel;
        private readonly ILogger<WorkerWithPlaner> _logger = logger;
        private readonly IChatCompletionService _chatCompletionService = chatCompletionService;

        private static readonly ActivitySource s_activitySource = new(nameof(WorkerWithPlaner));

        private const string InternetSearchprompt = """"
        You are a world class researcher, who can detailed research on any topic and produce facts based results;
        You do not make things up, you will try as hard as possible to gather facts and data to back up the research.

        You have the functions google_search to find elements on the web.
        You have the functions scrape_web_page to rerieve content of a page.
        if you have to search a person, use simple quote for the first name and last name. If you want to limit a query to a specific site, use site keyword to limit the search to a specific site

        Please make sure you complete the objective above with the following rules:
        1. You should do enough research to gather as much information as possible about the objective
        2. If there are url of relevant links and articles, you will scrape it with the scrape_website function to gather more information
        3. After scraping and search, you should think "Is there any new things I should search and scraping based on the data I collected to increase research quality? If answer is yes, continue; But don' do this more than 3 iterations.
        4. You should not make things up, you should only write facts and data that you gathered
        5. In the final output, You should include all reference data and links to back up your research.
        6. Do not use G2, they are mostly out dated data

        SAY TERMINATE when you found the result.

        ---
        Here are expected examples :

        Example :
        question : search devops on github
        query : devops site:github.com

        Example :
        question : find contribution for code from Yannick GOBERT a devops engineer on internet, he can be known with his alias ygo or ygo74
        query : contribution for code from 'Yannick GOBERT' devops engineer

        Example :
        question : find contribution for code from Yannick GOBERT a devops engineer on internet, he can be known with his alias ygo or ygo74
        query : contribution for code from 'YGO74' devops engineer
       
"""";

        private const string InternetSearchprompt2 = """
        You are a diligent researcher, and you have been asked to write a detailed report on the following topic
        You must provide both detail and context, and you must provide references to your sources.
        If you do a web search, don't just take the summary from the search results, scrape each linked page for best context.
        While the opinion of a journalist is interesting, bias towards original sources where possible.
""";

        protected override async Task ExecuteAsync(CancellationToken stoppingToken)
        {


            // Load prompt from YAML
            var ressouresNames = Assembly.GetEntryAssembly()!.GetManifestResourceNames();
            var ressourceName = ressouresNames[0];
            var stream = Assembly.GetEntryAssembly()!.GetManifestResourceStream(ressourceName);
            using StreamReader reader = new(stream!);
            KernelFunction scrapeWebpage = kernel.CreateFunctionFromPromptYaml(
                await reader.ReadToEndAsync(),
                promptTemplateFactory: new HandlebarsPromptTemplateFactory()
            );

            _kernel.ImportPluginFromFunctions("urlscrape", "scrapes webpage based on the url", new KernelFunction[] { scrapeWebpage });

#pragma warning disable SKEXP0001
            _kernel.PromptRenderFilters.Add(new DisplayPrompt(_logger));
            _kernel.FunctionInvocationFilters.Add(new DisplayFunction(_logger));
#pragma warning restore SKEXP0001

            ChatHistory chatMessages = new ChatHistory(InternetSearchprompt2);
            chatMessages.AddUserMessage("Qui a gagné la ligue des champions de football masculin en 2024?");

            // Start the conversation
            while (true)
            {

                // Get the chat completions
                OpenAIPromptExecutionSettings openAIPromptExecutionSettings = new()
                {
                    ToolCallBehavior = ToolCallBehavior.AutoInvokeKernelFunctions
                };

                var result = chatCompletionService.GetStreamingChatMessageContentsAsync(
                    chatMessages,
                    executionSettings: openAIPromptExecutionSettings,
                    kernel: kernel);

                // Stream the results
                string fullMessage = "";
                await foreach (var content in result)
                {
                    if (content.Role.HasValue)
                    {
                        System.Console.Write("Assistant > ");
                    }
                    System.Console.Write(content.Content);
                    fullMessage += content.Content;
                }
                System.Console.WriteLine();

                // Add the message from the agent to the chat history
                chatMessages.AddAssistantMessage(fullMessage);

                // Get user input
                System.Console.Write("User > ");
                chatMessages.AddUserMessage(Console.ReadLine()!);

            }



            _hostApplicationLifetime.StopApplication();
        }

    }
}
