import React from "react";

/**
 * CodeInput Component
 * Provides a textarea for users to paste code
 */
function CodeInput({ code, onChange, placeholder, disabled }) {
  return (
    <div className="w-full max-w-4xl">
      <label className="block text-sm font-medium text-gray-700 mb-2">
        📝 Paste Your Code Here
      </label>
      <textarea
        className="w-full h-64 p-4 border-2 border-gray-300 rounded-lg font-mono text-sm 
                   focus:border-blue-500 focus:ring-2 focus:ring-blue-200 
                   disabled:bg-gray-100 disabled:cursor-not-allowed
                   resize-y"
        placeholder={placeholder || "Paste your code here for review..."}
        value={code}
        onChange={(e) => onChange(e.target.value)}
        disabled={disabled}
        spellCheck={false}
      />
      <div className="mt-2 text-xs text-gray-500">
        💡 Tip: You can paste code in any programming language
      </div>
    </div>
  );
}

export default CodeInput; 