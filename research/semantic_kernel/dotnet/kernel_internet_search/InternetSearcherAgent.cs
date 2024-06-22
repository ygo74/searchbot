using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.Logging;
using Microsoft.SemanticKernel;
using Microsoft.SemanticKernel.Agents;
using Microsoft.SemanticKernel.Agents.Chat;
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
    internal class InternetSearcherAgent(
        IHostApplicationLifetime hostApplicationLifetime,
        Kernel kernel,
        ILoggerFactory loggerFactory) : BackgroundService
    {
        private readonly IHostApplicationLifetime _hostApplicationLifetime = hostApplicationLifetime;
        private readonly Kernel _kernel = kernel;
        private readonly ILoggerFactory _loggerFactory = loggerFactory;

        private static readonly ActivitySource s_activitySource = new(nameof(InternetSearcherAgent));

        protected override async Task ExecuteAsync(CancellationToken stoppingToken)
        {
            string researchManager = """
            You are a research manager, you are harsh, you are relentless.
            You will work task by task.

            You will firstly try to generate 2 actions researcher can take to find the information needed.

            Try to avoid G2, or other gated website that don't allow srcabing

            You will reviewed the result from the researcher, and always push back if researcher didin't find the information.

            Be persistent, say "No, you have to find the information, try again and propose 1 next method to try, if the researcher want to get away.

            Only after researcher found the information needed, you will say "TERMINATE"

            """;

            string researcher = """
            You are a world class researcher, who can detailed research on any topic and produce facts based results;
            You do not make things up, you will try as hard as possible to gather facts and data to back up the research.
            
            You have the function search to find elements on the web.
            You have the function scrape_web_page to rerieve content of a page.
            You have the function ask_question to ask the question in the vector database. 
            if you have to search a person, use simple quote for the first name and last name. If you want to limit a query to a specific site, use site keyword to limit the search to a specific site
            
            Please make sure you complete the objective above with the following rules:
            1. You should do enough research to gather as much information as possible about the objective
            2. If there are url of relevant links and articles, you will scrape it with the scrape_web_page function to gather more information
            3. After scraping you must ask the question to the vector database ton find the answer.
            4. After scraping and search, you should think "Is there any new things I should search and scraping based on the data I collected to increase research quality? If answer is yes, continue; But don' do this more than 3 iterations.
            5. You should not make things up, you should only write facts and data that you gathered
            6. In the final output, You should include all reference data and links to back up your research.
            7. Do not use G2, they are mostly out dated data
            8. Do not use uefa.com, rts.ch websites which blocks scraping
            
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
                  
            """;

            string InternetSearchprompt2 = """
            You are a diligent researcher, and you have been asked to write a detailed report on the following topic
            You must provide both detail and context, and you must provide references to your sources.
            If you do a web search, don't just take the summary from the search results, scrape each linked page for best context except pages which don't support scrapping.
            the following websites are not compatible with web scraping :
            - https://www.uefa.com/

            Once page has been scraped, ask the question to the vector database to find the answer.

            While the opinion of a journalist is interesting, bias towards original sources where possible.

            """;

#pragma warning disable SKEXP0110, SKEXP0001
            ChatCompletionAgent ResearchManagerAgent = new()
            {
                Instructions = researchManager,
                Name = "ResearchManagerAgent",
                Kernel = _kernel,
                ExecutionSettings = new OpenAIPromptExecutionSettings() { ToolCallBehavior = ToolCallBehavior.AutoInvokeKernelFunctions }
            };

            ChatCompletionAgent ResearcherAgent = new()
            {
                Instructions = researcher,
                Name = "ResearcherAgent",
                Kernel = _kernel,
                ExecutionSettings = new OpenAIPromptExecutionSettings() { ToolCallBehavior = ToolCallBehavior.AutoInvokeKernelFunctions }
            };

            AgentGroupChat chat = new(ResearchManagerAgent, ResearcherAgent)
            {
                LoggerFactory = _loggerFactory,
                ExecutionSettings = new()
                {
                    TerminationStrategy = new ApprovalTerminationStrategy()
                    {
                        Agents = [ResearchManagerAgent],
                        MaximumIterations = 6,
                    }

                }
            };

            // Ask question
            string input = """
            Quels forfaits téléphonique pour voyager aux Etats-Unis?
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
