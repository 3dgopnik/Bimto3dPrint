namespace Bimto3dPrint.Models
{
    /// <summary>
    /// Filter configuration model.
    /// </summary>
    public class FilterConfig
    {
        /// <summary>
        /// Included categories.
        /// </summary>
        public string[] IncludeCategories { get; set; } = new string[0];

        /// <summary>
        /// Excluded categories.
        /// </summary>
        public string[] ExcludeCategories { get; set; } = new string[0];
    }
}
