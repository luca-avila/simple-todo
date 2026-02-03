import axios from 'axios'

// Create a reusable Axios instance with a base URL
// All requests through 'api' will be prefixed with '/api/v1'
const api = axios.create({
  baseURL: '/api/v1',
})

// REQUEST INTERCEPTOR
// Runs before every request to automatically attach the auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// STATE FOR TOKEN REFRESH HANDLING
// Tracks if a token refresh is currently in progress
let isRefreshing = false
// Holds requests that are waiting for the token refresh to complete
let failedQueue = []

// QUEUE PROCESSOR
// Called after a token refresh attempt to resolve/reject all waiting requests
// - On success: resolves each waiting request with the new token
// - On failure: rejects each waiting request with the error
const processQueue = (error, token = null) => {
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error)
    } else {
      prom.resolve(token)
    }
  })
  failedQueue = []
}

// RESPONSE INTERCEPTOR
// Handles 401 errors by automatically refreshing the token and retrying requests
api.interceptors.response.use(
  // Success: just return the response unchanged
  (response) => response,

  // Error handler
  async (error) => {
    const originalRequest = error.config

    // Only handle 401 (Unauthorized) errors, and only if we haven't already retried
    // The _retry flag prevents infinite loops
    if (error.response?.status === 401 && !originalRequest._retry) {

      // CASE 1: Another request is already refreshing the token
      // Add this request to the queue and wait for the refresh to complete
      if (isRefreshing) {
        return new Promise((resolve, reject) => {
          // Store the resolve/reject functions so processQueue can call them later
          failedQueue.push({ resolve, reject })
        })
          .then((token) => {
            // Refresh succeeded - retry the original request with the new token
            originalRequest.headers.Authorization = `Bearer ${token}`
            return api(originalRequest)
          })
          .catch((err) => Promise.reject(err))
      }

      // CASE 2: This is the first 401 error - we need to refresh the token
      originalRequest._retry = true // Mark to prevent infinite retries
      isRefreshing = true // Signal to other requests that refresh is in progress

      const refreshToken = localStorage.getItem('refresh_token')
      if (!refreshToken) {
        // No refresh token available, can't refresh - just fail
        isRefreshing = false
        return Promise.reject(error)
      }

      try {
        // Call the refresh endpoint to get new tokens
        const response = await axios.post('/api/v1/auth/refresh', {
          refresh_token: refreshToken,
        })

        // Store the new tokens
        const { access_token, refresh_token } = response.data
        localStorage.setItem('access_token', access_token)
        localStorage.setItem('refresh_token', refresh_token)

        // Notify all queued requests that refresh succeeded
        processQueue(null, access_token)

        // Retry the original request with the new token
        originalRequest.headers.Authorization = `Bearer ${access_token}`
        return api(originalRequest)

      } catch (refreshError) {
        // Refresh failed - notify all queued requests to fail
        processQueue(refreshError, null)

        // Clear invalid tokens from storage
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')

        return Promise.reject(refreshError)

      } finally {
        // Always reset the flag when done, whether success or failure
        isRefreshing = false
      }
    }

    // For all other errors, just reject as normal
    return Promise.reject(error)
  }
)

export default api
