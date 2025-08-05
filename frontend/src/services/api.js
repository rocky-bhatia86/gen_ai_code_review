/**
 * API Service for AI Code Review System
 * Handles all communication with the backend
 */

const API_BASE_URL = "http://localhost:8001";

class ApiService {
  /**
   * Review code by sending it as text
   */
  async reviewCode(code) {
    try {
      const response = await fetch(`${API_BASE_URL}/review`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code }),
      });
      
      if (!response.ok) {
        throw new Error(`Review failed: ${response.statusText}`);
      }
      
      return response.json();
    } catch (error) {
      if (error.name === 'TypeError' && error.message.includes('fetch')) {
        throw new Error('Cannot connect to server. Please check if the backend is running on http://localhost:8001');
      }
      throw error;
    }
  }

  /**
   * Review code from uploaded file
   */
  async reviewFile(file) {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${API_BASE_URL}/review/file`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`File review failed: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Review a GitHub PR by URL
   */
  async reviewPR(prUrl, diffContent = "") {
    const response = await fetch(`${API_BASE_URL}/review/pr`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ 
        pr_url: prUrl, 
        diff_content: diffContent 
      }),
    });

    if (!response.ok) {
      throw new Error(`PR review failed: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Get system status
   */
  async getStatus() {
    const response = await fetch(`${API_BASE_URL}/status`);
    
    if (!response.ok) {
      throw new Error(`Status check failed: ${response.statusText}`);
    }
    
    return response.json();
  }
}

// Export singleton instance
export default new ApiService(); 