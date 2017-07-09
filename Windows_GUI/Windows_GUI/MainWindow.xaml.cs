using Microsoft.Win32;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;


namespace Windows_GUI
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private string imagepath;

        public MainWindow()
        {
            InitializeComponent();
        }

        private void OpenFileButn_Click(object sender, RoutedEventArgs e)
        {
            OpenFileDialog ofd = new OpenFileDialog();
            if (ofd.ShowDialog() == true)
                imagepath = ofd.FileName;

            BitmapImage pic = new BitmapImage();
            pic.BeginInit();
            pic.UriSource = new Uri(imagepath);
            pic.EndInit();

            ImgBox.Source = pic;
        }

        private void ViewResultButn_Click(object sender, RoutedEventArgs e)
        {
            List<string> arguments = new List<string>();
            string motherpath = Directory.GetCurrentDirectory();
            for (int i = 0; i < 4; i++)
                motherpath = Directory.GetParent(motherpath).ToString();
            // motherpath-এর ভ্যালু এখন CSE499Project নামক ফোল্ডারের পাথ

            string labelpath = System.IO.Path.Combine(motherpath, "Classifier\\Training\\retrained_labels.txt");
            string graphpath = System.IO.Path.Combine(motherpath, "Classifier\\Training\\retrained_graph.pb");
            string scriptpath = System.IO.Path.Combine(motherpath, "gui_linker.py");

            string args = scriptpath + " " + imagepath + " " + labelpath + " " + graphpath;

            string output = RunPythonScript(args);

            if(output != "ERROR")
                MessageBox.Show(output, "Output", MessageBoxButton.OK, MessageBoxImage.Information);
        }

        private string RunPythonScript(string args)
        {
            try
            {
                Process p = new Process();

                string prog = System.IO.Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData), "Local\\Programs\\Python\\Python35-32\\python.exe");

                MessageBox.Show(prog);
                MessageBox.Show(args);

                p.StartInfo = new ProcessStartInfo(prog, args);
                p.StartInfo.UseShellExecute = false;
                p.StartInfo.CreateNoWindow = true;
                p.StartInfo.RedirectStandardOutput = false;
                p.StartInfo.RedirectStandardError = false;

                Process processChild = Process.Start(p.StartInfo);
                string output = p.StandardOutput.ReadToEnd();
                p.WaitForExit();

                Console.ReadLine();
                return output;
            }
            catch (Exception x)
            {
                MessageBox.Show(x.GetType().ToString());
                return "ERROR";
            }
        }
    
    }
}
