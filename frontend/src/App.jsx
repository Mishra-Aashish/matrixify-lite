import { useState } from "react";
import Papa from "papaparse";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [previewRows, setPreviewRows] = useState([]);
  const [mergeStrategy] = useState("merge");

  const handleImport = async () => {
    if (!file) {
      alert("Please select a CSV or Excel file");
      return;
    }

    setLoading(true);
    setResult(null);
    setError(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/import/products",
        {
          method: "POST",
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Import failed");
      }

      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h2>Matrixify-Lite Product Import</h2>

      <div className="upload-section">
        <p><strong>Upload CSV or Excel file</strong></p>
        <input
          type="file"
          accept=".csv,.xlsx"
          onChange={(e) => {
            const selectedFile = e.target.files[0];
            setFile(selectedFile);

            if (selectedFile && selectedFile.name.endsWith(".csv")) {
              Papa.parse(selectedFile, {
                header: true,
                preview: 5,
                skipEmptyLines: true,
                complete: (results) => {
                  setPreviewRows(results.data);
                },
              });
            } else {
              setPreviewRows([]);
            }
          }}
        />
      </div>

      {previewRows.length > 0 && (
        <>
          <h4>CSV Preview (first 5 rows)</h4>
          <table className="table-preview">
            <thead>
              <tr>
                {Object.keys(previewRows[0]).map((key) => (
                  <th key={key}>{key}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {previewRows.map((row, index) => (
                <tr key={index}>
                  {Object.values(row).map((value, i) => (
                    <td key={i}>{value}</td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </>
      )}

      <div className="merge-info">
        Merge Strategy: <span>Merge (only)</span>
      </div>

      <button onClick={handleImport} disabled={loading}>
        {loading ? "Importing..." : "Start Import"}
      </button>

      {result && (
        <div className="result-box">
          <h4>Import Result</h4>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}

      {error && (
        <div className="error-box">
          Error: {error}
        </div>
      )}
    </div>
  );
}

export default App;
