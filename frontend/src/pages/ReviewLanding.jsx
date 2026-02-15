import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'

const API_BASE = import.meta.env.VITE_API_BASE || ''

function ReviewLanding() {
    const { token } = useParams()
    const [review, setReview] = useState(null)
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)
    const [copied, setCopied] = useState(false)
    const [redirecting, setRedirecting] = useState(false)
    const [countdown, setCountdown] = useState(3)

    // Fetch review data on mount
    useEffect(() => {
        async function fetchReview() {
            try {
                const res = await fetch(`${API_BASE}/api/review/${token}`)
                if (!res.ok) {
                    const data = await res.json().catch(() => ({}))
                    if (res.status === 410) {
                        throw new Error(data.detail || 'This review link has expired.')
                    }
                    throw new Error(data.detail || 'Review not found')
                }
                const data = await res.json()
                setReview(data)
            } catch (err) {
                setError(err.message)
            } finally {
                setLoading(false)
            }
        }

        if (token) {
            fetchReview()
        }
    }, [token])

    // Countdown + redirect after copy
    useEffect(() => {
        if (!redirecting || !review) return

        if (countdown <= 0) {
            window.location.href = review.gbp_review_url
            return
        }

        const timer = setTimeout(() => {
            setCountdown((c) => c - 1)
        }, 1000)

        return () => clearTimeout(timer)
    }, [redirecting, countdown, review])

    // Copy text to clipboard — works on both HTTPS and HTTP
    const copyToClipboard = async (text) => {
        // Method 1: Modern Clipboard API (requires HTTPS in production)
        if (navigator.clipboard && window.isSecureContext) {
            await navigator.clipboard.writeText(text)
            return true
        }

        // Method 2: Fallback using textarea + execCommand (works on HTTP)
        const textarea = document.createElement('textarea')
        textarea.value = text
        textarea.style.position = 'fixed'
        textarea.style.left = '-9999px'
        textarea.style.opacity = '0'
        document.body.appendChild(textarea)
        textarea.focus()
        textarea.select()

        try {
            document.execCommand('copy')
            return true
        } finally {
            document.body.removeChild(textarea)
        }
    }

    // Handle copy + redirect
    const handleCopyAndPost = async () => {
        if (!review) return

        try {
            const success = await copyToClipboard(review.draft_text)
            if (success) {
                setCopied(true)

                // Track the copy event (fire and forget)
                fetch(`${API_BASE}/api/review/${token}/copied`, { method: 'POST' }).catch(() => { })

                // Start countdown redirect
                setRedirecting(true)
            }
        } catch {
            alert('Could not copy automatically. Please select and copy the review text above, then click the link below to post it on Google.')
        }
    }

    // ─── Loading State ─────────────────────────────────────
    if (loading) {
        return (
            <div className="loading-container">
                <div className="loading-spinner" />
                <p className="loading-text">Loading your review...</p>
            </div>
        )
    }

    // ─── Error State ───────────────────────────────────────
    if (error) {
        return (
            <div className="error-container">
                <div className="error-icon">😟</div>
                <h2 className="error-title">Oops!</h2>
                <p className="error-message">{error}</p>
            </div>
        )
    }

    // ─── Main Landing Page ─────────────────────────────────
    return (
        <div className="landing-container">
            {/* Brand */}
            <div className="brand-header">
                <div className="brand-logo">bdcode</div>
                <div className="brand-tagline">Thank you for your partnership</div>
            </div>

            {/* Review Card */}
            <div className="review-card">
                <h2 className="review-greeting">
                    Hi {review.client_name} 👋
                </h2>
                <p className="review-subtitle">
                    Your review is ready! Just tap below to copy and post.
                </p>

                {/* Review Text */}
                <div className="review-text-block">
                    <p className="review-text">{review.draft_text}</p>
                </div>

                {/* CTA Button */}
                <button
                    className={`cta-button ${copied ? 'copied' : ''}`}
                    onClick={handleCopyAndPost}
                    disabled={copied}
                >
                    <span className="cta-button-icon">
                        {copied ? '✅' : '📋'}
                    </span>
                    {copied ? 'Copied! Redirecting...' : 'Copy & Post Review'}
                </button>

                {/* Redirect Notice */}
                {redirecting && (
                    <p className={`redirect-notice ${redirecting ? 'visible' : ''}`}>
                        Redirecting to Google in {countdown}s...
                    </p>
                )}
            </div>
        </div>
    )
}

export default ReviewLanding
