using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Agents;
using Microsoft.SemanticKernel.Agents.Chat;
using Microsoft.SemanticKernel.ChatCompletion;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace kernel_internet_search
{
    internal class WorkerWithAgents(
        IHostApplicationLifetime hostApplicationLifetime,
        Kernel kernel,
        ILoggerFactory loggerFactory) : BackgroundService
    {
        private readonly IHostApplicationLifetime _hostApplicationLifetime = hostApplicationLifetime;
        private readonly Kernel _kernel = kernel;
        private readonly ILoggerFactory _loggerFactory = loggerFactory;

        private static readonly ActivitySource s_activitySource = new(nameof(WorkerWithAgents));


        protected override async Task ExecuteAsync(CancellationToken stoppingToken)
        {
            // Prepare agents
            string ProgamManager = """
            You are a program manager which will take the requirement and create a plan for creating app. Program Manager understands the 
            user requirements and form the detail documents with requirements and costing. 
""";

            string SoftwareEngineer = """
            You are Software Engieer, and your goal is develop web app using HTML and JavaScript (JS) by taking into consideration all
            the requirements given by Program Manager. 
""";

            string ProjectManager = """
            You are manager which will review software engineer code, and make sure all client requirements are completed.
            Once all client requirements are completed, you can approve the request by just responding "approve"
""";

            
#pragma warning disable SKEXP0110, SKEXP0001
            ChatCompletionAgent ProgaramManagerAgent = new()
            {
                Instructions = ProgamManager,
                Name = "ProgaramManagerAgent",
                Kernel = kernel
            };

            ChatCompletionAgent SoftwareEngineerAgent = new()
            {
                Instructions = SoftwareEngineer,
                Name = "SoftwareEngineerAgent",
                Kernel = kernel
            };

            ChatCompletionAgent ProjectManagerAgent = new()
            {
                Instructions = ProjectManager,
                Name = "ProjectManager",
                Kernel = kernel
            };

            AgentGroupChat chat = new(ProgaramManagerAgent, SoftwareEngineerAgent, ProjectManagerAgent)
            {
                LoggerFactory = _loggerFactory,
                ExecutionSettings = new()
                {
                    TerminationStrategy = new ApprovalTerminationStrategy()
                    {
                        Agents = [ProjectManagerAgent],
                        MaximumIterations = 6,
                    }
                }
            };

            // Ask question
            string input = """
            I want to develop calculator app. 
            Keep it very simple. And get final approval from manager.
            """;

            chat.AddChatMessage(new ChatMessageContent(AuthorRole.User, input));
            Console.WriteLine($"# {AuthorRole.User}: '{input}'");

            await foreach (var content in chat.InvokeAsync())
            {
                Console.WriteLine($"# {content.Role} - {content.AuthorName ?? "*"}: '{content.Content}'");
            }

            // Stop Worker
            _hostApplicationLifetime.StopApplication();

        }

        private sealed class ApprovalTerminationStrategy : TerminationStrategy
        {
            // Terminate when the final message contains the term "approve"
            protected override Task<bool> ShouldAgentTerminateAsync(Agent agent, IReadOnlyList<ChatMessageContent> history, CancellationToken cancellationToken)
                => Task.FromResult(history[history.Count - 1].Content?.Contains("approve", StringComparison.OrdinalIgnoreCase) ?? false);
        }
    }
}
