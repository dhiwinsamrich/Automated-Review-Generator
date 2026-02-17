import { motion } from "framer-motion";

const ReviewSkeleton = () => {
  return (
    <div className="w-full max-w-lg mx-auto space-y-6 p-4">
      {/* Greeting skeleton */}
      <div className="space-y-2">
        <div className="h-8 w-48 rounded-lg bg-muted animate-shimmer bg-[length:200%_100%] bg-gradient-to-r from-muted via-secondary to-muted" />
        <div className="h-4 w-64 rounded-md bg-muted animate-shimmer bg-[length:200%_100%] bg-gradient-to-r from-muted via-secondary to-muted" />
      </div>

      {/* Card skeleton */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="glass-card p-6 space-y-4"
      >
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-full bg-muted animate-shimmer bg-[length:200%_100%] bg-gradient-to-r from-muted via-secondary to-muted" />
          <div className="space-y-1.5">
            <div className="h-4 w-24 rounded bg-muted animate-shimmer bg-[length:200%_100%] bg-gradient-to-r from-muted via-secondary to-muted" />
            <div className="h-3 w-16 rounded bg-muted animate-shimmer bg-[length:200%_100%] bg-gradient-to-r from-muted via-secondary to-muted" />
          </div>
        </div>
        <div className="space-y-2">
          <div className="h-3 w-full rounded bg-muted animate-shimmer bg-[length:200%_100%] bg-gradient-to-r from-muted via-secondary to-muted" />
          <div className="h-3 w-full rounded bg-muted animate-shimmer bg-[length:200%_100%] bg-gradient-to-r from-muted via-secondary to-muted" />
          <div className="h-3 w-3/4 rounded bg-muted animate-shimmer bg-[length:200%_100%] bg-gradient-to-r from-muted via-secondary to-muted" />
        </div>
      </motion.div>

      {/* Button skeleton */}
      <div className="h-12 w-full rounded-xl bg-muted animate-shimmer bg-[length:200%_100%] bg-gradient-to-r from-muted via-secondary to-muted" />
    </div>
  );
};

export default ReviewSkeleton;
