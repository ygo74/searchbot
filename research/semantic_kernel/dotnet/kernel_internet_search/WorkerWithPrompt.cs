using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using Microsoft.SemanticKernel;
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
    internal class WorkerWithPrompt(
        IHostApplicationLifetime hostApplicationLifetime,
        Kernel kernel,
        ILogger<WorkerWithPrompt> logger) : BackgroundService
    {
        private readonly IHostApplicationLifetime _hostApplicationLifetime = hostApplicationLifetime;
        private readonly Kernel _kernel = kernel;
        private readonly ILogger<WorkerWithPrompt> _logger = logger;

        private static readonly ActivitySource s_activitySource = new(nameof(WorkerWithPrompt));

        protected override async Task ExecuteAsync(CancellationToken stoppingToken)
        {
            // Load prompt from YAML
            var ressouresNames = Assembly.GetEntryAssembly().GetManifestResourceNames();
            var ressourceName = ressouresNames[0];
            var stream = Assembly.GetEntryAssembly().GetManifestResourceStream(ressourceName);
            using StreamReader reader = new(stream!);
            KernelFunction scrapeWebpage = kernel.CreateFunctionFromPromptYaml(
                await reader.ReadToEndAsync(),
                promptTemplateFactory: new HandlebarsPromptTemplateFactory()
            );

            //var result = await _kernel.InvokeAsync(
            //    pluginName: "webscraper",
            //    functionName: "scrape_web_page",
            //    arguments: new()
            //    {
            //        { "url", "https://ygo74.github.io/about/" },
            //        { "question", "What are the skills of ygo74 which are described in this webpage https://ygo74.github.io/about/?" }
            //    },
            //    cancellationToken: stoppingToken
            //);

            //var result2 = await _kernel.InvokeAsync(
            //    pluginName: "webscraper",
            //    functionName: "ask_question",
            //    arguments: new()
            //    {
            //        { "question", "What are the skills of ygo74" }
            //    },
            //    cancellationToken: stoppingToken
            //);

            // Enable auto function calling
            OpenAIPromptExecutionSettings openAIPromptExecutionSettings = new()
            {
                ToolCallBehavior = ToolCallBehavior.AutoInvokeKernelFunctions
            };

            var result3 = await _kernel.InvokeAsync(
                function: scrapeWebpage,
                arguments: new(openAIPromptExecutionSettings)
                {
                    { "url", "https://ygo74.github.io/platforms_support/artifacts_repository/" },
                    { "question", "What are the features required by an Artifact repository platform?" }
                },
                cancellationToken: stoppingToken
            );

            Console.WriteLine(result3.ToString() );

            _hostApplicationLifetime.StopApplication();

        }

    }
}
