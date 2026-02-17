import { motion } from "framer-motion";
import StarRating from "./StarRating";
import type { ReviewData } from "@/lib/api";

interface ReviewCardProps {
  review: ReviewData;
}

const ReviewCard = ({ review }: ReviewCardProps) => {
  const initials = review.client_name
    .split(" ")
    .map((n) => n[0])
    .join("")
    .toUpperCase();

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.2 }}
      className="glass-card glow-border p-6 space-y-4"
    >
      {/* Header — Google Review style */}
      <div className="flex items-center gap-3">
        <div className="h-10 w-10 rounded-full bg-primary/20 flex items-center justify-center text-sm font-semibold text-primary">
          {initials}
        </div>
        <div>
          <p className="text-sm font-medium text-foreground">{review.client_name}</p>
          <StarRating rating={review.rating} size={16} />
        </div>
        <div className="ml-auto">
          <svg width="20" height="20" viewBox="0 0 24 24" className="text-muted-foreground/50">
            <path
              fill="currentColor"
              d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z"
            />
            <path
              fill="currentColor"
              d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
            />
            <path
              fill="currentColor"
              d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
            />
            <path
              fill="currentColor"
              d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
            />
          </svg>
        </div>
      </div>

      {/* Review text */}
      <p className="text-sm leading-relaxed text-secondary-foreground/80">
        "{review.draft_text}"
      </p>

      {/* Footer */}
      <div className="flex items-center justify-between pt-2 border-t border-border/50">
        <span className="text-xs text-muted-foreground">
          Draft review for {review.business_name}
        </span>
        <span className="text-xs text-muted-foreground">Just now</span>
      </div>
    </motion.div>
  );
};

export default ReviewCard;
