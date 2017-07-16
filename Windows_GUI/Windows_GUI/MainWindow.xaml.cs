using Microsoft.Win32;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Timers;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
//using System.Windows.Shapes;


namespace Windows_GUI
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private string imagepath;
        private string motherpath;

        public MainWindow()
        {
            InitializeComponent();
        }

        private void OpenFileButn_Click(object sender, RoutedEventArgs e)
        {
            OpenFileDialog ofd = new OpenFileDialog()
            {
                Filter = "Image files (*.bmp, *.jpg, *.png)|*.bmp;*.jpg;*.png"
            };

            if (ofd.ShowDialog() == true)
                imagepath = ofd.FileName;
            if (imagepath == null) return;
            else ViewResultButn.IsEnabled = true;

            BitmapImage pic = new BitmapImage();
            pic.BeginInit();
            pic.UriSource = new Uri(imagepath);
            pic.EndInit();

            ImgBox.Source = pic;
        }

        private void ViewResultButn_Click(object sender, RoutedEventArgs e)
        {
            List<string> arguments = new List<string>();
            motherpath = Directory.GetCurrentDirectory();
            for (int i = 0; i < 4; i++)
                motherpath = Directory.GetParent(motherpath).ToString();
            // motherpath-এর ভ্যালু এখন CSE499Project নামক ফোল্ডারের পাথ

            string labelpath = Path.Combine(motherpath, "Classifier\\Training\\retrained_labels.txt");
            string graphpath = Path.Combine(motherpath, "Classifier\\Training\\retrained_graph.pb");
            string scriptpath = Path.Combine(motherpath, "gui_linker.py");

            string args = scriptpath + " " + imagepath + " " + labelpath + " " + graphpath;

            string output = RunPythonScript(args);

            if (output != "ERROR")
                MessageBox.Show(output, "Output", MessageBoxButton.OK, MessageBoxImage.Information);
            else
                MessageBox.Show("Program not working. Contact maacpiash and tell him that the problem is" + Environment.NewLine + output,
                    "ERROR!", MessageBoxButton.OK, MessageBoxImage.Error);
        }

        private string RunPythonScript(string args)
        {
            string output;

            try
            {
                Process temp = new Process();

                string prog = string.Format(@"C:\\ProgramData\\Anaconda3\\python.exe");

                temp.StartInfo = new ProcessStartInfo(prog, args)
                {
                    UseShellExecute = false,
                    CreateNoWindow = true,
                    RedirectStandardOutput = true,
                    RedirectStandardError = false
                };

                Process running = Process.Start(temp.StartInfo);
                running.Start();

                output = running.StandardOutput.ReadToEnd();
                running.WaitForExit();
            }
            catch (Exception x)
            {
                output = x.GetType().ToString();
            }
            
            return output;
        }
    }
}
