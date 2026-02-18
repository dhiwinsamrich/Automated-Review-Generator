import { useSearchParams } from "react-router-dom";
import { motion } from "framer-motion";
import { Mail, Heart, AlertTriangle, Clock, CheckCircle2 } from "lucide-react";

const configs: Record<string, { icon: React.ReactNode; title: string; description: string }> = {
  regenerate: {
    icon: <Mail size={32} />,
    title: "New Draft on the Way!",
    description: "We're crafting a fresh review draft for you. Check your email shortly for the updated version.",
  },
  decline: {
    icon: <Heart size={32} />,
    title: "Thank You for Your Feedback",
    description: "We appreciate you taking the time to let us know. Your honesty helps us improve.",
  },
  "regen-limit": {
    icon: <AlertTriangle size={32} />,
    title: "Maximum Revisions Reached",
    description: "You've used all available revision requests. Please contact the business directly for further assistance.",
  },
  expired: {
    icon: <Clock size={32} />,
    title: "Link Expired",
    description: "This link is no longer active. Please reach out to the business for a new review link.",
  },
};

const defaultConfig = {
  icon: <CheckCircle2 size={32} />,
  title: "Action Recorded",
  description: "Your response has been noted. Thank you!",
};

const ActionConfirmedPage = () => {
  const [params] = useSearchParams();
  const type = params.get("type") || "";
  const config = configs[type] || defaultConfig;

  const iconColor =
    type === "regen-limit"
      ? "bg-warning/10 text-warning"
      : type === "expired"
      ? "bg-destructive/10 text-destructive"
      : type === "decline"
      ? "bg-primary/10 text-primary"
      : "bg-success/10 text-success";

  return (
    <div className="min-h-screen bg-background bg-grid bg-radial-glow flex items-center justify-center p-4">
      <motion.div
        initial={{ opacity: 0, y: 20, scale: 0.97 }}
        animate={{ opacity: 1, y: 0, scale: 1 }}
        transition={{ duration: 0.5 }}
        className="glass-card glow-border p-8 sm:p-10 max-w-md w-full text-center space-y-5"
      >
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
          className={`mx-auto w-16 h-16 rounded-2xl flex items-center justify-center ${iconColor}`}
        >
          {config.icon}
        </motion.div>

        <motion.h1
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
          className="text-xl sm:text-2xl font-bold text-foreground"
        >
          {config.title}
        </motion.h1>

        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.4 }}
          className="text-sm text-muted-foreground leading-relaxed"
        >
          {config.description}
        </motion.p>
      </motion.div>
    </div>
  );
};

export default ActionConfirmedPage;
