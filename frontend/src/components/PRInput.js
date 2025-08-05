import React, { useState } from "react";

/**
 * PRInput Component
 * Allows users to manually review a GitHub PR by URL
 */
function PRInput({ onPRReview, disabled }) {
  const [prUrl, setPrUrl] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (prUrl.trim() && !disabled) {
      onPRReview(prUrl.trim());
    }
  };

  const isValidGitHubUrl = (url) => {
    return url.includes("github.com") && (url.includes("/pull/") || url.includes("/tree/") || url.includes("/compare/"));
  };

  return (
    <div className="w-full max-w-4xl">
      <label className="block text-sm font-medium text-gray-700 mb-2">
        🔗 Or Review a GitHub Pull Request / Branch
      </label>
      
      <form onSubmit={handleSubmit} className="space-y-3">
        <div className="flex space-x-3">
          <input
            type="url"
            placeholder="https://github.com/owner/repo/pull/123"
            value={prUrl}
            onChange={(e) => setPrUrl(e.target.value)}
            disabled={disabled}
            className="flex-1 px-4 py-2 border-2 border-gray-300 rounded-lg
                       focus:border-blue-500 focus:ring-2 focus:ring-blue-200
                       disabled:bg-gray-100 disabled:cursor-not-allowed"
          />
          <button
            type="submit"
            disabled={disabled || !prUrl.trim() || !isValidGitHubUrl(prUrl)}
            className="px-6 py-2 bg-purple-600 text-white rounded-lg font-medium
                       hover:bg-purple-700 focus:ring-2 focus:ring-purple-200
                       disabled:bg-gray-400 disabled:cursor-not-allowed
                       transition-colors"
          >
            Review PR
          </button>
        </div>
        
        <div className="text-xs text-gray-500">
          💡 Paste a GitHub PR URL to fetch and review the changes automatically
        </div>
      </form>
    </div>
  );
}

export default PRInput; 