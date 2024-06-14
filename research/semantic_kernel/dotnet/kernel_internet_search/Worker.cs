using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.ChatCompletion;
using Microsoft.SemanticKernel.Connectors.OpenAI;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace kernel_internet_search
{
    internal class Worker(
        IHostApplicationLifetime hostApplicationLifetime,
        Kernel kernel,
        ILogger<Worker> logger) : BackgroundService
    {
        private readonly IHostApplicationLifetime _hostApplicationLifetime = hostApplicationLifetime;
        private readonly Kernel _kernel = kernel;
        private readonly ILogger<Worker> _logger = logger;

        private static readonly ActivitySource s_activitySource = new(nameof(Worker));

        protected override async Task ExecuteAsync(CancellationToken stoppingToken)
        {

            _logger.LogInformation("Start chat");
            // Get chat completion service
            var chatCompletionService = _kernel.GetRequiredService<IChatCompletionService>();

            // Enable auto function calling
            OpenAIPromptExecutionSettings openAIPromptExecutionSettings = new()
            {
                ToolCallBehavior = ToolCallBehavior.AutoInvokeKernelFunctions
            };

            Console.WriteLine("Ask questions or give instructions to the copilot such as:\n" +
                              "- What time is it?\n" +
                              "- Turn on the porch light.\n" +
                              "- If it's before 7:00 pm, turn on the office light.\n" +
                              "- Which light is currently on?\n" +
                              "- Set an alarm for 6:00 am.\n");

            Console.Write("> ");

            string? input = null;
            while ((input = Console.ReadLine()) is not null)
            {
                Console.WriteLine();

                using var _ = s_activitySource.StartActivity("chat");
                ChatMessageContent chatResult = await chatCompletionService.GetChatMessageContentAsync(input,
                        openAIPromptExecutionSettings, _kernel, stoppingToken);

                Console.Write($"\n>>> Result: {chatResult}\n\n> ");
            }

            _hostApplicationLifetime.StopApplication();
        }

    }
}
