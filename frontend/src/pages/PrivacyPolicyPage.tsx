import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import { ArrowLeft } from "lucide-react";

const PrivacyPolicyPage = () => {
  return (
    <div className="min-h-screen bg-background bg-grid bg-radial-glow py-12 px-4">
      <div className="max-w-3xl mx-auto space-y-8">
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
        >
          <Link
            to="/"
            className="inline-flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground transition-colors mb-6"
          >
            <ArrowLeft size={16} />
            Back to Home
          </Link>

          <div className="glass-card glow-border p-8 sm:p-10 space-y-8">
            <div className="space-y-2">
              <h1 className="text-3xl font-bold text-foreground">Privacy Policy</h1>
              <p className="text-sm text-muted-foreground">
                Last updated: February 19, 2026
              </p>
            </div>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold text-foreground">1. Introduction</h2>
              <p className="text-sm text-muted-foreground leading-relaxed">
                bdcode ("we", "our", or "us") operates the Automated Review Generator
                service. This Privacy Policy explains how we collect, use, disclose, and
                safeguard your information when you use our service, including interactions
                via WhatsApp, email, and our website.
              </p>
            </section>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold text-foreground">2. Information We Collect</h2>
              <p className="text-sm text-muted-foreground leading-relaxed">
                We may collect the following types of information:
              </p>
              <ul className="list-disc list-inside text-sm text-muted-foreground space-y-1.5 ml-2">
                <li><span className="text-foreground font-medium">Personal Information:</span> Name, phone number, email address, and company name provided through feedback forms.</li>
                <li><span className="text-foreground font-medium">Feedback Data:</span> Ratings and open-text responses submitted through our forms.</li>
                <li><span className="text-foreground font-medium">Communication Data:</span> WhatsApp message metadata (message IDs, delivery status) and email interactions.</li>
                <li><span className="text-foreground font-medium">Usage Data:</span> Interactions with our landing pages, such as review copy events.</li>
              </ul>
            </section>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold text-foreground">3. How We Use Your Information</h2>
              <ul className="list-disc list-inside text-sm text-muted-foreground space-y-1.5 ml-2">
                <li>To generate personalized review drafts using AI based on your feedback.</li>
                <li>To send review drafts and approval requests via WhatsApp or email.</li>
                <li>To facilitate posting approved reviews on Google Business Profile.</li>
                <li>To send follow-up reminders for pending reviews.</li>
                <li>To improve our services and user experience.</li>
              </ul>
            </section>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold text-foreground">4. Third-Party Services</h2>
              <p className="text-sm text-muted-foreground leading-relaxed">
                We use the following third-party services that may process your data:
              </p>
              <ul className="list-disc list-inside text-sm text-muted-foreground space-y-1.5 ml-2">
                <li><span className="text-foreground font-medium">Meta (WhatsApp Business API):</span> For sending and receiving messages.</li>
                <li><span className="text-foreground font-medium">Google Cloud:</span> For data storage (Google Sheets) and AI services (Gemini).</li>
                <li><span className="text-foreground font-medium">Vercel:</span> For hosting our web application.</li>
              </ul>
            </section>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold text-foreground">5. Data Retention</h2>
              <p className="text-sm text-muted-foreground leading-relaxed">
                We retain your personal information only for as long as necessary to fulfill
                the purposes outlined in this policy. Review consent tokens expire after 14
                days, after which the associated links become inactive.
              </p>
            </section>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold text-foreground">6. Data Security</h2>
              <p className="text-sm text-muted-foreground leading-relaxed">
                We implement appropriate technical and organizational measures to protect
                your personal information, including encrypted communications (HTTPS/TLS),
                secure API authentication, and access controls on stored data.
              </p>
            </section>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold text-foreground">7. Your Rights</h2>
              <p className="text-sm text-muted-foreground leading-relaxed">
                Depending on your location, you may have the right to:
              </p>
              <ul className="list-disc list-inside text-sm text-muted-foreground space-y-1.5 ml-2">
                <li>Access the personal data we hold about you.</li>
                <li>Request correction or deletion of your data.</li>
                <li>Withdraw consent for data processing.</li>
                <li>Object to or restrict processing of your data.</li>
              </ul>
            </section>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold text-foreground">8. Contact Us</h2>
              <p className="text-sm text-muted-foreground leading-relaxed">
                If you have any questions about this Privacy Policy, please contact us at{" "}
                <a href="mailto:subscriptionoff12@gmail.com" className="text-primary hover:underline">
                  subscriptionoff12@gmail.com
                </a>.
              </p>
            </section>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default PrivacyPolicyPage;
