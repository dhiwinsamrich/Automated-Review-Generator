import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { Copy, Check, ExternalLink, AlertCircle, ArrowRight } from "lucide-react";
import { fetchReview, markCopied, type ReviewData } from "@/lib/api";
import ReviewCard from "@/components/ReviewCard";
import ReviewSkeleton from "@/components/ReviewSkeleton";
import { Button } from "@/components/ui/button";

const ReviewPage = () => {
  const { token } = useParams<{ token: string }>();
  const [review, setReview] = useState<ReviewData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);
  const [countdown, setCountdown] = useState<number | null>(null);

  useEffect(() => {
    if (!token) return;
    fetchReview(token)
      .then(setReview)
      .catch((err) => {
        if (err?.status === 410) setError("expired");
        else setError("Something went wrong. Please try again later.");
      })
      .finally(() => setLoading(false));
  }, [token]);

  useEffect(() => {
    if (countdown === null) return;
    if (countdown <= 0 && review) {
      window.open(review.gbp_review_url, "_blank");
      return;
    }
    const t = setTimeout(() => setCountdown((c) => (c !== null ? c - 1 : null)), 1000);
    return () => clearTimeout(t);
  }, [countdown, review]);

  const handleCopy = async () => {
    if (!review || !token) return;
    try {
      await navigator.clipboard.writeText(review.draft_text);
      setCopied(true);
      await markCopied(token);
      setCountdown(3);
    } catch {
      // fallback
      const ta = document.createElement("textarea");
      ta.value = review.draft_text;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand("copy");
      document.body.removeChild(ta);
      setCopied(true);
      await markCopied(token);
      setCountdown(3);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-background bg-grid bg-radial-glow flex items-center justify-center p-4">
        <ReviewSkeleton />
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-background bg-grid bg-radial-glow flex items-center justify-center p-4">
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="glass-card glow-border p-8 max-w-md w-full text-center space-y-4"
        >
          <div className="mx-auto w-14 h-14 rounded-full bg-destructive/10 flex items-center justify-center">
            <AlertCircle className="text-destructive" size={28} />
          </div>
          <h2 className="text-xl font-semibold text-foreground">
            {error === "expired" ? "Link Expired" : "Something Went Wrong"}
          </h2>
          <p className="text-sm text-muted-foreground">
            {error === "expired"
              ? "This review link is no longer valid. Please contact the business for a new one."
              : error}
          </p>
        </motion.div>
      </div>
    );
  }

  if (!review) return null;

  return (
    <div className="min-h-screen bg-background bg-grid bg-radial-glow flex items-center justify-center p-4">
      <div className="w-full max-w-lg space-y-6">
        {/* Greeting */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
          className="space-y-1"
        >
          <h1 className="text-2xl sm:text-3xl font-bold text-foreground">
            Hi {review.client_name} 👋
          </h1>
          <p className="text-sm text-muted-foreground">
            Your review for <span className="text-foreground font-medium">{review.business_name}</span> is ready
          </p>
        </motion.div>

        {/* Review card */}
        <ReviewCard review={review} />

        {/* CTA */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4, delay: 0.4 }}
          className="space-y-3"
        >
          <AnimatePresence mode="wait">
            {!copied ? (
              <motion.div key="copy" exit={{ opacity: 0, scale: 0.95 }}>
                <Button
                  onClick={handleCopy}
                  className="w-full h-12 text-base font-semibold rounded-xl bg-primary hover:bg-primary/90 text-primary-foreground transition-all animate-pulse-glow"
                  size="lg"
                >
                  <Copy size={18} className="mr-2" />
                  Copy & Post to Google
                </Button>
              </motion.div>
            ) : (
              <motion.div
                key="success"
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="space-y-3"
              >
                <div className="flex items-center justify-center gap-2 py-3 rounded-xl bg-success/10 border border-success/20">
                  <Check size={20} className="text-success" />
                  <span className="text-sm font-medium text-success">
                    Copied to clipboard!
                  </span>
                </div>
                <Button
                  onClick={() => window.open(review.gbp_review_url, "_blank")}
                  className="w-full h-12 text-base font-semibold rounded-xl bg-primary hover:bg-primary/90 text-primary-foreground"
                  size="lg"
                >
                  <ExternalLink size={18} className="mr-2" />
                  {countdown !== null && countdown > 0
                    ? `Opening Google in ${countdown}s...`
                    : "Post on Google"}
                  <ArrowRight size={16} className="ml-2" />
                </Button>
              </motion.div>
            )}
          </AnimatePresence>

          <p className="text-xs text-center text-muted-foreground">
            Paste the copied text into the Google review form
          </p>
        </motion.div>
      </div>
    </div>
  );
};

export default ReviewPage;
