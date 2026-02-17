import { Star } from "lucide-react";

interface StarRatingProps {
  rating: number;
  size?: number;
}

const StarRating = ({ rating, size = 20 }: StarRatingProps) => {
  return (
    <div className="flex gap-0.5">
      {Array.from({ length: 5 }, (_, i) => (
        <Star
          key={i}
          size={size}
          className={i < rating ? "star-filled" : "star-empty"}
          strokeWidth={0}
          fill={i < rating ? "currentColor" : "none"}
          stroke="currentColor"
        />
      ))}
    </div>
  );
};

export default StarRating;
