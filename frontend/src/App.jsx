import React, { useState } from 'react';
import axios from 'axios';
import { Upload, FileImage, FileType, FileText, Download, AlertCircle, Loader2, Minimize2 } from 'lucide-react';


const API_BASE_URL = `http://${window.location.hostname}:8001/api`;

const ConversionCard = ({ title, icon: Icon, endpoint, showFormatSelect = false, showMergeToggle = false }) => {
  const [files, setFiles] = useState([]);
  const [targetFormat, setTargetFormat] = useState('JPG');
  const [merge, setMerge] = useState(false);
  const [processing, setProcessing] = useState(false);
  const [results, setResults] = useState([]);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    const selectedFiles = Array.from(e.target.files);
    setFiles(selectedFiles);
    setResults([]);
    setError(null);
  };

  const handleConvert = async () => {
    if (files.length === 0) {
      setError('Please select at least one file.');
      return;
    }

    setProcessing(true);
    setError(null);
    setResults([]);

    if (showMergeToggle && merge && files.length > 1) {
      // Handle merging multiple files into one PDF
      const formData = new FormData();
      files.forEach(f => formData.append('file', f));
      formData.append('merge', 'true');

      try {
        const response = await axios.post(`${API_BASE_URL}${endpoint}`, formData, {
          headers: { 'Content-Type': 'multipart/form-data' }
        });
        setResults([{
          name: `Merged Result (${files.length} images)`,
          url: response.data.converted_url,
          status: 'success'
        }]);
      } catch (err) {
        setError(err.response?.data?.error || 'Failed to merge files.');
      }
    } else {
      // Handle batch processing individually
      const newResults = [];
      for (const file of files) {
        const formData = new FormData();
        formData.append('file', file);
        if (showFormatSelect) {
          formData.append('target_format', targetFormat);
        }

        try {
          const response = await axios.post(`${API_BASE_URL}${endpoint}`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
          });
          newResults.push({
            name: file.name,
            url: response.data.converted_url,
            status: 'success'
          });
        } catch (err) {
          newResults.push({
            name: file.name,
            status: 'error',
            error: err.response?.data?.error || 'Failed'
          });
        }
        setResults([...newResults]);
      }
    }

    setProcessing(false);
  };

  const handleDownload = (url) => {
    // Use the backend's download endpoint to force attachment header
    // Use decodeURIComponent to avoid double encoding issues with special characters
    const relativePath = decodeURIComponent(url.split('/media/')[1]);
    const downloadUrl = `${API_BASE_URL}/download/?path=${encodeURIComponent(relativePath)}`;
    window.location.href = downloadUrl;
  };

  return (
    <div className="card">
      <div className="icon-wrapper">
        <Icon size={32} />
      </div>
      <h2>{title}</h2>

      {showFormatSelect && (
        <select value={targetFormat} onChange={(e) => setTargetFormat(e.target.value)}>
          <option value="JPG">Convert to JPG</option>
          <option value="PNG">Convert to PNG</option>
        </select>
      )}

      {showMergeToggle && files.length > 1 && (
        <div className="merge-toggle">
          <label>
            <input type="checkbox" checked={merge} onChange={(e) => setMerge(e.target.checked)} />
            Merge all into one PDF
          </label>
        </div>
      )}

      <div className="file-input-wrapper">
        <div className="file-input">
          <input type="file" onChange={handleFileChange} accept="image/*,.heic" multiple />
          <div className="file-info">
            {files.length > 0 ? (
              <span style={{ fontSize: '14px' }}>{files.length} files selected</span>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '4px' }}>
                <Upload size={20} />
                <span style={{ fontSize: '13px' }}>Click to upload multiple files</span>
              </div>
            )}
          </div>
        </div>
      </div>

      <button className="btn" onClick={handleConvert} disabled={processing}>
        {processing ? <Loader2 className="loader" /> : `Convert ${files.length > 0 ? files.length : ''} Files`}
      </button>

      {results.length > 0 && (
        <div className="results-list">
          {results.map((res, index) => (
            <div key={index} className={`result-item ${res.status}`}>
              <span className="file-name">{res.name}</span>
              {res.status === 'success' ? (
                <button className="download-icon-btn" onClick={() => handleDownload(res.url)}>
                  <Download size={16} />
                </button>
              ) : (
                <AlertCircle size={16} className="error-icon" title={res.error} />
              )}
            </div>
          ))}
        </div>
      )}

      {error && (
        <div className="error">
          <AlertCircle size={16} /> {error}
        </div>
      )}
    </div>
  );
};

const COMPRESSION_PRESETS = [
  {
    id: 'extreme',
    label: 'Extreme Compression',
    range: '10 – 30',
    quality: 30,
    desc: 'Smallest file size',
    color: '#a855f7',
    glowColor: 'rgba(168,85,247,0.25)',
  },
  {
    id: 'high',
    label: 'High Compression',
    range: '40 – 60',
    quality: 50,
    desc: 'Good balance',
    color: '#3b82f6',
    glowColor: 'rgba(59,130,246,0.25)',
  },
  {
    id: 'recommended',
    label: 'Recommended',
    range: '70 – 85',
    quality: 78,
    desc: 'Best quality',
    color: '#22c55e',
    glowColor: 'rgba(34,197,94,0.25)',
  },
];

function formatBytes(bytes) {
  if (bytes >= 1024 * 1024) return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
  return Math.round(bytes / 1024) + ' KB';
}

const CompressionCard = ({ title, endpoint, accept, iconColor = '#22c55e' }) => {
  const [file, setFile] = useState(null);
  const [selectedPreset, setSelectedPreset] = useState('recommended');
  const [processing, setProcessing] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const preset = COMPRESSION_PRESETS.find(p => p.id === selectedPreset);

  const handleFileChange = (e) => {
    setFile(e.target.files[0] || null);
    setResult(null);
    setError(null);
  };

  const handleCompress = async () => {
    if (!file) { setError('Please select a file.'); return; }
    setProcessing(true);
    setError(null);
    setResult(null);
    const formData = new FormData();
    formData.append('file', file);
    formData.append('quality', String(preset.quality));
    try {
      const res = await axios.post(`${API_BASE_URL}${endpoint}`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setResult(res.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Compression failed.');
    }
    setProcessing(false);
  };

  const handleDownload = (url) => {
    const relativePath = decodeURIComponent(url.split('/media/')[1]);
    const downloadUrl = `${API_BASE_URL}/download/?path=${encodeURIComponent(relativePath)}`;
    window.location.href = downloadUrl;
  };

  return (
    <div className="card compression-card">
      <div className="icon-wrapper" style={{ color: iconColor, background: `${iconColor}1a` }}>
        <Minimize2 size={32} />
      </div>
      <h2>{title}</h2>

      {/* Preset Tiles */}
      <div className="compression-presets">
        {COMPRESSION_PRESETS.map(p => (
          <button
            key={p.id}
            className={`preset-tile${selectedPreset === p.id ? ' active' : ''}`}
            style={selectedPreset === p.id ? {
              borderColor: p.color,
              boxShadow: `0 0 14px ${p.glowColor}`,
            } : {}}
            onClick={() => setSelectedPreset(p.id)}
          >
            <span className="preset-dot" style={{ background: p.color }} />
            <span className="preset-name">{p.label}</span>
            <span className="preset-range" style={{ color: p.color }}>{p.range}</span>
            <span className="preset-desc">{p.desc}</span>
          </button>
        ))}
      </div>

      {/* Upload */}
      <div className="file-input-wrapper">
        <div className="file-input">
          <input type="file" accept={accept} onChange={handleFileChange} />
          <div className="file-info">
            {file ? (
              <span style={{ fontSize: '14px' }}>{file.name} &nbsp; <span className="size-tag">{formatBytes(file.size)}</span></span>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '4px' }}>
                <Upload size={20} />
                <span style={{ fontSize: '13px' }}>Click to upload file</span>
              </div>
            )}
          </div>
        </div>
      </div>

      <button className="btn" onClick={handleCompress} disabled={processing}>
        {processing ? <Loader2 className="loader" /> : `Compress ${title.includes('PDF') ? 'PDF' : 'Image'}`}
      </button>

      {/* Result */}
      {result && (() => {
        const alreadyOptimal = result.saved_percent === 0;
        return (
          <div className="compression-result">
            <div className="size-comparison">
              <div className="size-box">
                <span className="size-label">Original</span>
                <span className="size-value">{formatBytes(result.original_size)}</span>
              </div>
              <div className="size-arrow">→</div>
              <div className="size-box">
                <span className="size-label">{alreadyOptimal ? 'Output' : 'Compressed'}</span>
                <span className={`size-value ${alreadyOptimal ? '' : 'compressed'}`}>
                  {formatBytes(result.compressed_size)}
                </span>
              </div>
            </div>
            {alreadyOptimal ? (
              <div className="saved-badge already-optimal">✅ Already optimized — no further reduction possible</div>
            ) : (
              <div className="saved-badge">🎉 You saved {result.saved_percent}%</div>
            )}
            <button className="download-icon-btn compress-download" onClick={() => handleDownload(result.converted_url)}>
              <Download size={16} /> Download
            </button>
          </div>
        );
      })()}

      {error && (
        <div className="error"><AlertCircle size={16} /> {error}</div>
      )}
    </div>
  );
};


function App() {
  return (
    <div className="container">
      <h1>SwiftConvert</h1>
      <p className="subtitle">Premium Image Conversion for iOS & Web</p>

      <div className="converter-grid">
        <ConversionCard
          title="Image Format"
          icon={FileImage}
          endpoint="/convert-image-format/"
          showFormatSelect={true}
        />
        <ConversionCard
          title="Image to PDF"
          icon={FileType}
          endpoint="/convert-to-pdf/"
          showMergeToggle={true}
        />
        <ConversionCard
          title="Image to Word"
          icon={FileText}
          endpoint="/convert-to-word/"
        />
        <CompressionCard
          title="Image Compression"
          endpoint="/compress-image/"
          accept="image/*,.heic"
        />
        <CompressionCard
          title="PDF Compression"
          endpoint="/compress-pdf/"
          accept=".pdf"
          iconColor="#f87171"
        />
      </div>


      <p style={{ marginTop: '3rem', textAlign: 'center', color: 'var(--text-muted)', fontSize: '0.9rem' }}>
        Supports HEIC, JPG, and PNG uploads. iOS compatible.
      </p>
    </div>
  );
}

export default App;
