using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace CubicSetupApp
{
    internal class Program
    {
        static void Main(string[] args)
        {
            string test = CreateJson();
            Console.WriteLine(test);
            Console.ReadLine();
        }

        static string CreateJson()
        {
            Console.WriteLine("Please enter a title for the meeitng");
            string Title = Console.ReadLine();
            Console.WriteLine("Please enter a description for the meeting");
            string Description = Console.ReadLine();
            string Location = Console.ReadLine();
            string date = Console.ReadLine();
            string timeStart = Console.ReadLine();
            string timeEnd = Console.ReadLine();
            Meeting Meeting = new Meeting(Title, Description, Location, date, timeStart, timeEnd);
            string JsonString = JsonSerializer.Serialize(Meeting);
            return JsonString;
        }
    }
}
