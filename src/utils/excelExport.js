import * as XLSX from 'xlsx';

/**
 * Export citation data to Excel file
 * @param {Array} citations - Array of citation records
 * @param {string} filename - Name of the exported file
 */
export const exportCitationsToExcel = (citations, filename = 'citation_data') => {
  // Prepare data for Excel
  const excelData = citations.map((record, index) => ({
    'Sr. No.': index + 1,
    'Faculty Name': record.faculty_name,
    
    // Web of Science
    'WoS - Papers': record.web_of_science?.papers || 0,
    'WoS - Citations': record.web_of_science?.citations || 0,
    'WoS - h-index': record.web_of_science?.h_index || 0,
    
    // Scopus
    'Scopus - Papers': record.scopus?.papers || 0,
    'Scopus - Citations': record.scopus?.citations || 0,
    'Scopus - h-index': record.scopus?.h_index || 0,
    
    // Google Scholar
    'Google Scholar - Papers': record.google_scholar?.papers || 0,
    'Google Scholar - Citations': record.google_scholar?.citations || 0,
    'Google Scholar - h-index': record.google_scholar?.h_index || 0,
    'Google Scholar - i10-index': record.google_scholar?.i10_index || 0,
    
    // Links
    'Publons URL': record.publons_url || 'NIL',
    'Scopus URL': record.scopus_url || 'NIL',
    'Google Scholar URL': record.google_scholar_url || 'NIL',
    'ResearchGate URL': record.researchgate_url || 'NIL',
    
    // Researcher IDs
    'ORCID ID': record.orcid?.id || 'NIL',
    'ORCID URL': record.orcid?.url || 'NIL',
    'OpenAlex ID': record.openalex?.id || 'NIL',
    'OpenAlex URL': record.openalex?.url || 'NIL',
    
    // Metadata
    'Last Updated': record.updated_at ? new Date(record.updated_at).toLocaleString() : 'NIL',
    'Updated By': record.updated_by || 'NIL'
  }));

  // Create workbook and worksheet
  const wb = XLSX.utils.book_new();
  const ws = XLSX.utils.json_to_sheet(excelData);

  // Set column widths
  ws['!cols'] = [
    { wch: 8 },   // Sr. No.
    { wch: 30 },  // Faculty Name
    { wch: 12 },  // WoS - Papers
    { wch: 12 },  // WoS - Citations
    { wch: 12 },  // WoS - h-index
    { wch: 12 },  // Scopus - Papers
    { wch: 12 },  // Scopus - Citations
    { wch: 12 },  // Scopus - h-index
    { wch: 15 },  // Google Scholar - Papers
    { wch: 15 },  // Google Scholar - Citations
    { wch: 15 },  // Google Scholar - h-index
    { wch: 15 },  // Google Scholar - i10-index
    { wch: 30 },  // Publons URL
    { wch: 30 },  // Scopus URL
    { wch: 30 },  // Google Scholar URL
    { wch: 30 },  // ResearchGate URL
    { wch: 20 },  // ORCID ID
    { wch: 35 },  // ORCID URL
    { wch: 20 },  // OpenAlex ID
    { wch: 35 },  // OpenAlex URL
    { wch: 20 },  // Last Updated
    { wch: 25 }   // Updated By
  ];

  // Add worksheet to workbook
  XLSX.utils.book_append_sheet(wb, ws, 'Citation Data');

  // Generate timestamp for filename
  const timestamp = new Date().toISOString().slice(0, 10);
  const fullFilename = `${filename}_${timestamp}.xlsx`;

  // Write and download file
  XLSX.writeFile(wb, fullFilename);

  return fullFilename;
};

/**
 * Export citation history to Excel file
 * @param {Array} history - Array of history records
 * @param {string} facultyName - Name of the faculty
 * @param {string} filename - Name of the exported file
 */
export const exportHistoryToExcel = (history, facultyName, filename = 'citation_history') => {
  // Prepare data for Excel
  const excelData = history.map((record, index) => ({
    'Sr. No.': index + 1,
    'Date': new Date(record.created_at).toLocaleString(),
    'Change Source': record.change_source,
    'Source Platform': record.source_platform,
    'Changed Fields': record.changed_fields.join(', '),
    'Changed By': record.created_by || 'System',
    'Snapshot Data': JSON.stringify(record.snapshot, null, 2)
  }));

  // Create workbook and worksheet
  const wb = XLSX.utils.book_new();
  const ws = XLSX.utils.json_to_sheet(excelData);

  // Set column widths
  ws['!cols'] = [
    { wch: 8 },   // Sr. No.
    { wch: 20 },  // Date
    { wch: 15 },  // Change Source
    { wch: 15 },  // Source Platform
    { wch: 40 },  // Changed Fields
    { wch: 25 },  // Changed By
    { wch: 50 }   // Snapshot Data
  ];

  // Add worksheet to workbook
  XLSX.utils.book_append_sheet(wb, ws, 'History');

  // Generate timestamp for filename
  const timestamp = new Date().toISOString().slice(0, 10);
  const safeFacultyName = facultyName.replace(/[^a-z0-9]/gi, '_').toLowerCase();
  const fullFilename = `${filename}_${safeFacultyName}_${timestamp}.xlsx`;

  // Write and download file
  XLSX.writeFile(wb, fullFilename);

  return fullFilename;
};
