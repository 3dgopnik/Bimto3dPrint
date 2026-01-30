using System.Collections.Generic;
using System.Linq;
using System.Windows;

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
    }
}
