using Microsoft.KernelMemory;
using Microsoft.SemanticKernel;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace kernel_internet_search.Plugins
{
    public class ScrapeWebpagePlugin
    {
        [Description("Scrape a webpage")]
        [KernelFunction("scrape_web_page")]
        public async Task<string> ScrapeWebPage(
            Kernel kernel,
            [Description("Webpage's url to scrape")]string url
            )
        {

            // Work around for pages which doesn't exist
            if (url.Contains("uefa.com/") | url.Contains("rts.ch/"))
            {
                return "NOT FOUND";
            }

            using var httpClient = new HttpClient();
            httpClient.BaseAddress = new Uri(url);

            using HttpRequestMessage request = new(HttpMethod.Get, url);
            using HttpResponseMessage response = await httpClient.SendAsync(request, HttpCompletionOption.ResponseHeadersRead).ConfigureAwait(false);

            if (response.StatusCode != System.Net.HttpStatusCode.OK)
            {
                return "NOT FOUND";
            }


            var s_memory = new MemoryWebClient("http://127.0.0.1:9001/");

            var documentId = url.GetHashCode().ToString();

            if (!await s_memory.IsDocumentReadyAsync(documentId: documentId, index: "web"))
            {

                var result = await s_memory.ImportWebPageAsync(
                    url: url,
                    documentId: documentId,
                    index: "web"
                );

                var count = 0;
                while (!await s_memory.IsDocumentReadyAsync(documentId: documentId, index: "web"))
                {
                    await Task.Delay(TimeSpan.FromSeconds(2));
                    count++;
                    if (count == 30)
                    {
                        break;
                        //throw new Exception("Unable to scrape this webpage, try with another page");
                    }
                }
            }

            return "FOUND INFORMATION, NOW ASK THE QUESTION TO VECTOR DATABASE";

        }

        [Description("Ask the user's question to the vector database")]
        [KernelFunction("ask_question")]
        public async Task<string> AskQuestion(
            Kernel kernel,
            [Description("the user's question to ask to the vector database")] string question
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
