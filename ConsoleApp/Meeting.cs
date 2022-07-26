using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;


namespace CubicSetupApp
{
    internal class Meeting
    {
        public Meeting(string title, string description, string location, string date, string timeBegin)
        {
            this.title = title;
            this.description = description;
            this.location = location;
            this.date = date;
            this.timeBegin = timeBegin;
        }
        public string title { get; set; }
        public string description { get; set; }
        public string location { get; set; }
        public string date { get; set; }
        public string timeBegin { get; set; }
    }
}
