using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Text.Json;
using System.Net.Http;


namespace CubicSetupApp
{
    internal class Program
    {
        static void Main(string[] args)
        {
            string test = CreateJson();
            Console.WriteLine(test);
            SendJson(test);
            Console.ReadLine();
        }

        static string CreateJson()
        {
            Console.WriteLine("Please enter a title for the meeitng");
            string Title = Console.ReadLine();
            Console.WriteLine("Please enter a description for the meeting");
            string Description = Console.ReadLine();
            Console.WriteLine("Please enter a location for the meeting");
            string Location = Console.ReadLine();
            Console.WriteLine("Please enter a date for the meeting");
            string date = Console.ReadLine();
            Console.WriteLine("Please enter a starting time for the meeting");
            string timeStart = Console.ReadLine();
            Console.WriteLine("Please enter the end time for the meeting");
            string timeEnd = Console.ReadLine();
            Meeting Meeting = new Meeting(Title, Description, Location, date, timeStart, timeEnd);
            string JsonString = JsonSerializer.Serialize(Meeting);
            return JsonString;
        }

        static string SendJson(string json)
        {
            HttpClient client = new HttpClient();
            client.BaseAddress = new Uri(@"http://127.0.0.1:8000/");
            var content = new StringContent(json);
            var result = client.PostAsync("calendar/add", content).Result;
            Console.WriteLine(result);
            return "Success";
        }
    }
}
