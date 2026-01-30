using System;
using System.Collections.Generic;
using System.Globalization;
using System.Linq;
using System.Windows;
using System.Windows.Forms;

namespace Bimto3dPrint.UI
{
    /// <summary>
    /// WPF dialog for export configuration.
    /// </summary>
    public partial class ExportDialog : Window
    {
        /// <summary>
        /// Initializes a new instance of the <see cref="ExportDialog"/> class.
        /// </summary>
        public ExportDialog()
        {
            InitializeComponent();
            CancelButton.Click += (_, __) => DialogResult = false;
            ExportButton.Click += (_, __) => DialogResult = true;
            BrowseButton.Click += (_, __) => SelectOutputFolder();

            OutputFolderTextBox.Text = Environment.GetFolderPath(Environment.SpecialFolder.DesktopDirectory);
            MinWallThicknessTextBox.Text = "2.0";
        }

        /// <summary>
        /// Gets the selected preset name.
        /// </summary>
        public string SelectedPreset => PresetComboBox.SelectedItem as string ?? string.Empty;

        /// <summary>
        /// Gets the selected output format.
        /// </summary>
        public string SelectedOutputFormat => OutputFormatComboBox.SelectedItem as string ?? "stl";

        /// <summary>
        /// Gets the selected IFC version.
        /// </summary>
        public string SelectedIfcVersion => IfcVersionComboBox.SelectedItem as string ?? "IFC4";

        /// <summary>
        /// Gets the selected output folder.
        /// </summary>
        public string OutputFolder => OutputFolderTextBox.Text ?? string.Empty;

        /// <summary>
        /// Gets a value indicating whether to run the Python pipeline after export.
        /// </summary>
        public bool RunPipelineAfterExport => RunPipelineCheckBox.IsChecked == true;

        /// <summary>
        /// Gets a value indicating whether wall thickening should be skipped.
        /// </summary>
        public bool NoThicken => NoThickenCheckBox.IsChecked == true;

        /// <summary>
        /// Gets the minimum wall thickness in millimeters.
        /// </summary>
        public double MinWallThicknessMm
        {
            get
            {
                if (double.TryParse(MinWallThicknessTextBox.Text, NumberStyles.Float, CultureInfo.InvariantCulture, out var value))
                {
                    return value;
                }

                return 2.0;
            }
        }

        /// <summary>
        /// Loads available presets into the dialog.
        /// </summary>
        public void LoadPresets(IEnumerable<string> presets)
        {
            var presetList = presets?.Where(preset => !string.IsNullOrWhiteSpace(preset)).ToList()
                            ?? new List<string>();
            PresetComboBox.ItemsSource = presetList;
            PresetComboBox.SelectedIndex = presetList.Count > 0 ? 0 : -1;
        }

        /// <summary>
        /// Loads available output formats into the dialog.
        /// </summary>
        public void LoadOutputFormats(IEnumerable<string> formats)
        {
            var formatList = formats?.Where(format => !string.IsNullOrWhiteSpace(format)).ToList()
                            ?? new List<string>();
            OutputFormatComboBox.ItemsSource = formatList;
            OutputFormatComboBox.SelectedIndex = formatList.Count > 0 ? 0 : -1;
        }

        /// <summary>
        /// Loads available IFC versions into the dialog.
        /// </summary>
        public void LoadIfcVersions(IEnumerable<string> versions)
        {
            var versionList = versions?.Where(version => !string.IsNullOrWhiteSpace(version)).ToList()
                              ?? new List<string>();
            IfcVersionComboBox.ItemsSource = versionList;
            IfcVersionComboBox.SelectedIndex = versionList.Count > 0 ? 0 : -1;
        }

        private void SelectOutputFolder()
        {
            using (var dialog = new FolderBrowserDialog())
            {
                dialog.SelectedPath = OutputFolderTextBox.Text;
                var result = dialog.ShowDialog();
                if (result == DialogResult.OK)
                {
                    OutputFolderTextBox.Text = dialog.SelectedPath;
                }
            }
        }
    }
}
