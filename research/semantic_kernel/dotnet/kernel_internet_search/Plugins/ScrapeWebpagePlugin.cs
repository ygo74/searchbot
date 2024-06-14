using Microsoft.KernelMemory;
using Microsoft.SemanticKernel;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace kernel_internet_search.Plugins
{
    public class ScrapeWebpagePlugin
    {
        [Description("Scrape a webpage")]
        [KernelFunction("scrape_web_page")]
        public async Task ScrapeWebPage(
            Kernel kernel,
            [Description("Webpage's url to scrape")]string url
            )
        {
            var s_memory = new MemoryWebClient("http://127.0.0.1:9001/");

            await s_memory.ImportWebPageAsync(
                url: url,
                documentId: "doc02",
                index: "web"
            );

            while(!await s_memory.IsDocumentReadyAsync(documentId: "doc02", index: "web"))
            {
                await Task.Delay(TimeSpan.FromSeconds(2));
            }

        }

        [Description("Ask question about the goal")]
        [KernelFunction("ask_question")]
        public async Task<string> AskQuestion(
            Kernel kernel,
            [Description("Question to ask")] string question
            )
        {
            var s_memory = new MemoryWebClient("http://127.0.0.1:9001/");

            var result = await s_memory.AskAsync(
                question: question,
                index: "web"
            );

            return result.Result;
        }

    }
}
