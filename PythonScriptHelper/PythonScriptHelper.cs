using System;
using System.Diagnostics;
using System.IO;
using System.Text;
using System.Windows.Forms;

namespace upload_torrents
{
    static class PythonScriptHelper
    {
        /// <summary>
        /// Just rename the .exe file to the .py file you want to execute
        /// </summary>
        [STAThread]
        public static void Main(string[] args)
        {
            var scriptName = Environment.GetCommandLineArgs()[0].Replace(".exe",".py");
            var scriptFileName = scriptName;
            var scriptFile = Path.Combine(Directory.GetCurrentDirectory(), scriptFileName);
            if(!File.Exists(scriptFile))
                scriptFile = Path.Combine(Path.GetDirectoryName(typeof(PythonScriptHelper).Assembly.Location), scriptFileName);
            if(!File.Exists(scriptFile))
            {
                MessageBox.Show(string.Format("Oops, couldn't find {0} in {1}", scriptName,  scriptFile));
                return;
            }
            
            var joinedArgs = new StringBuilder();
            foreach (var arg in args)
            {
                joinedArgs.AppendFormat(" \"{0}\"", arg);
            }
            var info = new ProcessStartInfo("pythonw", scriptFile + " " + joinedArgs.ToString());
            info.CreateNoWindow = true;
            info.WindowStyle = ProcessWindowStyle.Hidden;
            Process.Start(info);
        }
    }
}
