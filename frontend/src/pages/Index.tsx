import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import { ArrowRight, Star, Shield, Zap } from "lucide-react";
import { Button } from "@/components/ui/button";

const Index = () => {
  return (
    <div className="min-h-screen bg-background bg-grid bg-radial-glow flex items-center justify-center p-4">
      <div className="max-w-2xl w-full text-center space-y-10">
        {/* Hero */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="space-y-4"
        >
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-primary/10 border border-primary/20 text-xs font-medium text-primary">
            <Zap size={12} />
            Automated Review Generator
          </div>
          <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold tracking-tight text-foreground">
            Turn happy clients into{" "}
            <span className="gradient-text-primary">5-star reviews</span>
          </h1>
          <p className="text-base sm:text-lg text-muted-foreground max-w-lg mx-auto">
            AI-crafted, personalized review drafts your clients can approve and post in seconds.
          </p>
        </motion.div>

        {/* CTA */}
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3, duration: 0.5 }}
        >
          <Link to="/review/demo">
            <Button
              size="lg"
              className="h-12 px-8 text-base font-semibold rounded-xl bg-primary hover:bg-primary/90 text-primary-foreground animate-pulse-glow"
            >
              See Demo
              <ArrowRight size={18} className="ml-2" />
            </Button>
          </Link>
        </motion.div>

        {/* Feature pills */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="flex flex-wrap justify-center gap-3"
        >
          {[
            { icon: <Star size={14} />, label: "AI-Powered Drafts" },
            { icon: <Shield size={14} />, label: "Client Approved" },
            { icon: <Zap size={14} />, label: "One-Click Posting" },
          ].map((f) => (
            <div
              key={f.label}
              className="flex items-center gap-2 px-4 py-2 rounded-full glass-card text-xs font-medium text-muted-foreground"
            >
              {f.icon}
              {f.label}
            </div>
          ))}
        </motion.div>
      </div>
    </div>
  );
};

export default Index;
