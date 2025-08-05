import React, { useState, useRef } from "react";

/**
 * FileUpload Component
 * Provides drag-and-drop file upload functionality
 */
function FileUpload({ onFileSelect, disabled }) {
  const [dragActive, setDragActive] = useState(false);
  const fileInputRef = useRef(null);

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (disabled) return;

    const files = e.dataTransfer.files;
    if (files && files[0]) {
      onFileSelect(files[0]);
    }
  };

  const handleFileInput = (e) => {
    if (disabled) return;
    
    const files = e.target.files;
    if (files && files[0]) {
      onFileSelect(files[0]);
    }
  };

  const openFileDialog = () => {
    if (!disabled) {
      fileInputRef.current?.click();
    }
  };

  return (
    <div className="w-full max-w-4xl">
      <label className="block text-sm font-medium text-gray-700 mb-2">
        📁 Or Upload a Code File
      </label>
      
      <div
        className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors
          ${dragActive 
            ? "border-blue-500 bg-blue-50" 
            : "border-gray-300 hover:border-gray-400"
          }
          ${disabled 
            ? "opacity-50 cursor-not-allowed" 
            : "cursor-pointer hover:bg-gray-50"
          }`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
        onClick={openFileDialog}
      >
        <div className="space-y-2">
          <div className="text-4xl">
            {dragActive ? "📥" : "📄"}
          </div>
          <div className="text-lg font-medium text-gray-600">
            {dragActive ? "Drop your file here" : "Click to select or drag & drop"}
          </div>
          <div className="text-sm text-gray-500">
            Supports: .py, .js, .ts, .java, .cpp, .c, .go, .rs, and more
          </div>
        </div>
      </div>

      <input
        ref={fileInputRef}
        type="file"
        className="hidden"
        onChange={handleFileInput}
        accept=".py,.js,.ts,.jsx,.tsx,.java,.cpp,.c,.h,.go,.rs,.php,.rb,.cs,.swift,.kt,.scala,.sh,.sql,.html,.css,.json,.xml,.yaml,.yml,.md,.txt"
        disabled={disabled}
      />
    </div>
  );
}

export default FileUpload; 