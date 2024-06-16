using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Connectors.OpenAI;
using Microsoft.SemanticKernel.Planning.Handlebars;
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
    internal class WorkerWithPlaner(
        IHostApplicationLifetime hostApplicationLifetime,
        Kernel kernel,
        ILogger<WorkerWithPlaner> logger) : BackgroundService
    {
        private readonly IHostApplicationLifetime _hostApplicationLifetime = hostApplicationLifetime;
        private readonly Kernel _kernel = kernel;
        private readonly ILogger<WorkerWithPlaner> _logger = logger;

        private static readonly ActivitySource s_activitySource = new(nameof(WorkerWithPlaner));

#pragma warning disable SKEXP0001, SKEXP0010, SKEXP0020, SKEXP0050, , SKEXP0060

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



            // Set the planner options
            var plannerOptions = new HandlebarsPlannerOptions()
            {
                // When using OpenAI models, we recommend using low values for temperature and top_p to minimize planner hallucinations.
                ExecutionSettings = new OpenAIPromptExecutionSettings()
                {
                    Temperature = 0.0,
                    TopP = 0.1,
                },
                // Use gpt-4 or newer models if you want to test with loops.
                // Older models like gpt-35-turbo are less recommended. They do handle loops but are more prone to syntax errors.
                // AllowLoops = ChatDeploymentName.Contains("gpt-4", StringComparison.OrdinalIgnoreCase),
               
            };

            // Instantiate the planner and create the plan
            var goal = "Qui a gagné la ligue des champions de football masculin en 2024?";
            var planner = new HandlebarsPlanner(plannerOptions);
            var plan = await planner.CreatePlanAsync(kernel, goal);

            // Execute the plan
            var result = await plan.InvokeAsync(_kernel, null, stoppingToken);

            PrintPlannerDetails(goal, plan, result, true);

            _hostApplicationLifetime.StopApplication();


        }

        private void PrintPlannerDetails(string goal, HandlebarsPlan plan, string result, bool shouldPrintPrompt)
        {
            Console.WriteLine($"Goal: {goal}");
            Console.WriteLine($"\nOriginal plan:\n{plan}");
            Console.WriteLine($"\nResult:\n{result}\n");

            // Print the prompt template
            if (shouldPrintPrompt && plan.Prompt is not null)
            {
                Console.WriteLine("\n======== CreatePlan Prompt ========");
                Console.WriteLine(plan.Prompt);
            }
        }


    }
}
