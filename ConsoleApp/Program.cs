using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Text;
using System.Text.Json;
using System.Net;
using System.Net.Http;


namespace CubicSetupApp
{
    internal class Program
    {
        // Public HTTP Client to allow api calls from all methods
        public static HttpClient client { get; set; } = new HttpClient();

        static void Main(string[] args)
        {
            Console.WriteLine("What is the CubicCalendar's IP address?");
            string address = SetAddress(); 
            client.BaseAddress = new Uri(@"http://" + address + @":8000");
            Console.WriteLine("What would you like to do? \nAdd a meeting (add)\nEdit a meeting (edit)\nRemove a meeting (remove)");
            commands();
            Console.ReadLine();
        }

        /// <summary>
        /// Asks the user for a command to execute.
        /// If the command is not recognised it will recursively ask again
        /// 
        /// 
        /// </summary>
        static void commands()
        {
            string cmd = Console.ReadLine();
            cmd = cmd.ToLower();
            switch (cmd)
            {
                //  <Debugging>
                case "alert":
                    tts(Console.ReadLine());
                    break;
                //  </Debugging>

                case "add":
                    string meeting = CreateJson();
                    SendJson(meeting);
                    commands();
                    break;
                case "edit":
                    Console.WriteLine("sorry, not implemented yet");
                    commands();
                    break;
                case "remove":
                    Console.WriteLine("sorry, not implemented yet");
                    commands();
                    break;
                default:
                    Console.WriteLine("I don't recognise {0}, Please try again", cmd);
                    commands();
                    break;
            }
        }
        
        /// <summary>
        /// Sends a TTS command to the CubicCalendar
        /// </summary>
        /// <param name="text">Content of the message</param>
        static void tts(string text)
        {
            client.GetAsync("alert/"+text);
        }

        /// <summary>
        /// Recursive function that reads and validates an IP from the console.
        /// </summary>
        /// <returns>a validated IP in string format</returns>
        static string SetAddress()
        {
            string input = Console.ReadLine();

            IPAddress ip;
            if (IPAddress.TryParse(input, out ip))
            {
                return ip.ToString();
            }
            Console.WriteLine("Please enter a valid IP");
            return SetAddress();

        }

        /// <summary>
        /// Creates a Json file for adding a meeting
        /// </summary>
        /// <returns>Json serialised string with meeting details</returns>
        static string CreateJson()
        {
            string Title = meetingItem("title");
            string Description = meetingItem("description");
            string Location = meetingItem("location");
            string Date = meetingItem("date");
            string TimeStart = meetingItem("starting time");
            Meeting Meeting = new Meeting(Title, Description, Location, Date, TimeStart);
            string JsonString = JsonSerializer.Serialize(Meeting);
            return JsonString;
        }

        /// <summary>
        /// Small function to prevent repetitive code
        /// </summary>
        /// <param name="item">input subject</param>
        /// <returns>user given input</returns>
        static string meetingItem(string item)
        {
            string msg = "Please enter a "+item+" for the meeting";
            Console.WriteLine(msg);
            tts(msg);
            string result = Console.ReadLine();
            return result;
        }

        /// <summary>
        /// Sends the JSON string to the cube api
        /// </summary>
        /// <param name="json"> Json serialised string with meeting details</param>
        /// <param name="address"> IP address string </param>
        /// <returns></returns>
        static void SendJson(string json)
        {
            var content = new StringContent(json);
            try
            {
                var result = client.PostAsync("calendar/add", content).Result;
                Console.WriteLine(result);
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
            }
        }
    }
}
