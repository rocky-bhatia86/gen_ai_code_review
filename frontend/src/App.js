
import React, { useState, useEffect } from "react";
import CodeInput from "./components/CodeInput";
import FileUpload from "./components/FileUpload";
import PRInput from "./components/PRInput";
import ReviewOutput from "./components/ReviewOutput";
import apiService from "./services/api";

function App() {
  // State management
  const [code, setCode] = useState("");
  const [review, setReview] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [reviewMode, setReviewMode] = useState("code"); // "code", "file", "pr"
  const [systemStatus, setSystemStatus] = useState(null);

  // Check system status on load
  useEffect(() => {
    apiService.getStatus()
      .then(status => setSystemStatus(status))
      .catch(err => console.warn("Could not fetch system status:", err));
  }, []);

  // Reset state when switching modes
  const resetState = () => {
    setReview("");
    setError("");
    setCode("");
  };

  // Handle code review (from textarea)
  const handleCodeReview = async () => {
    if (!code.trim()) {
      setError("Please enter some code to review");
      return;
    }

    setLoading(true);
    setError("");
    setReview("");

    try {
      const result = await apiService.reviewCode(code);
      setReview(result.review);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Handle file upload review
  const handleFileReview = async (file) => {
    if (!file) return;

    setLoading(true);
    setError("");
    setReview("");

    try {
      const result = await apiService.reviewFile(file);
      setReview(result.review);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Handle PR review
  const handlePRReview = async (prUrl) => {
    if (!prUrl.trim()) return;

    setLoading(true);
    setError("");
    setReview("");

    try {
      const result = await apiService.reviewPR(prUrl);
      setReview(result.review);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Handle mode switching
  const switchMode = (mode) => {
    if (mode !== reviewMode) {
      resetState();
      setReviewMode(mode);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-6 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">
            🤖 AI Code Review System
          </h1>
          <p className="text-gray-600 text-lg">
            Get intelligent code reviews powered by AI
          </p>
          
          {/* System Status */}
          {systemStatus && (
            <div className="mt-4 inline-flex items-center space-x-4 text-sm">
              <span className={`flex items-center ${systemStatus.openai_configured ? 'text-green-600' : 'text-yellow-600'}`}>
                <span className="w-2 h-2 rounded-full bg-current mr-2"></span>
                AI: {systemStatus.openai_configured ? 'Ready' : 'Mock Mode'}
              </span>
              <span className={`flex items-center ${systemStatus.github_configured ? 'text-green-600' : 'text-gray-600'}`}>
                <span className="w-2 h-2 rounded-full bg-current mr-2"></span>
                GitHub: {systemStatus.github_configured ? 'Connected' : 'Not Configured'}
              </span>
            </div>
          )}
        </div>

        {/* Mode Tabs */}
        <div className="flex justify-center mb-8">
          <div className="bg-white rounded-lg p-1 shadow-sm border">
            <button
              onClick={() => switchMode("code")}
              className={`px-4 py-2 rounded-md font-medium transition-colors ${
                reviewMode === "code"
                  ? "bg-blue-600 text-white"
                  : "text-gray-600 hover:text-gray-900"
              }`}
            >
              📝 Paste Code
            </button>
            <button
              onClick={() => switchMode("file")}
              className={`px-4 py-2 rounded-md font-medium transition-colors ${
                reviewMode === "file"
                  ? "bg-blue-600 text-white"
                  : "text-gray-600 hover:text-gray-900"
              }`}
            >
              📁 Upload File
            </button>
            <button
              onClick={() => switchMode("pr")}
              className={`px-4 py-2 rounded-md font-medium transition-colors ${
                reviewMode === "pr"
                  ? "bg-blue-600 text-white"
                  : "text-gray-600 hover:text-gray-900"
              }`}
            >
              🔗 Review PR
            </button>
          </div>
        </div>

        {/* Main Content */}
        <div className="flex flex-col items-center space-y-6">
          
          {/* Code Input Mode */}
          {reviewMode === "code" && (
            <>
              <CodeInput
                code={code}
                onChange={setCode}
                disabled={loading}
              />
              <button
                onClick={handleCodeReview}
                disabled={loading || !code.trim()}
                className="px-8 py-3 bg-blue-600 text-white rounded-lg font-medium text-lg
                           hover:bg-blue-700 focus:ring-2 focus:ring-blue-200
                           disabled:bg-gray-400 disabled:cursor-not-allowed
                           transition-colors"
              >
                {loading ? "🤖 Reviewing..." : "🚀 Review Code"}
              </button>
            </>
          )}

          {/* File Upload Mode */}
          {reviewMode === "file" && (
            <FileUpload
              onFileSelect={handleFileReview}
              disabled={loading}
            />
          )}

          {/* PR Review Mode */}
          {reviewMode === "pr" && (
            <PRInput
              onPRReview={handlePRReview}
              disabled={loading}
            />
          )}

          {/* Review Output */}
          <ReviewOutput
            review={review}
            loading={loading}
            error={error}
          />

        </div>

        {/* Footer */}
        <div className="text-center mt-12 text-gray-500 text-sm">
          <p>
            🛠️ Built with FastAPI + React | 
            💡 Supports all major programming languages |
            🔒 Your code is processed securely
          </p>
        </div>
      </div>
    </div>
  );
}

export default App;
