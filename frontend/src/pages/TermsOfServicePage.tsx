import { motion } from "framer-motion";
import { Link } from "react-router-dom";
import { ArrowLeft } from "lucide-react";

const TermsOfServicePage = () => {
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
              <h1 className="text-3xl font-bold text-foreground">Terms of Service</h1>
              <p className="text-sm text-muted-foreground">
                Last updated: February 19, 2026
              </p>
            </div>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold text-foreground">1. Acceptance of Terms</h2>
              <p className="text-sm text-muted-foreground leading-relaxed">
                These Terms of Service ("Terms") govern your use of the Automated Review
                Generator platform provided by bdcode. By using our platform, you
                acknowledge that you have read, understood, and agree to be bound by these
                Terms.
              </p>
            </section>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold text-foreground">2. Eligibility</h2>
              <p className="text-sm text-muted-foreground leading-relaxed">
                You must be at least 18 years old to use this service. By using the service,
                you represent that you meet this age requirement and have the legal capacity
                to enter into a binding agreement.
              </p>
            </section>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold text-foreground">3. Service Availability</h2>
              <p className="text-sm text-muted-foreground leading-relaxed">
                We strive to maintain continuous availability of our service but do not
                guarantee uninterrupted access. The service may be temporarily unavailable
                due to maintenance, updates, or circumstances beyond our control.
              </p>
            </section>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold text-foreground">4. Acceptable Use</h2>
              <p className="text-sm text-muted-foreground leading-relaxed">
                You agree not to:
              </p>
              <ul className="list-disc list-inside text-sm text-muted-foreground space-y-1.5 ml-2">
                <li>Use the service to generate fake, misleading, or fraudulent reviews.</li>
                <li>Attempt to manipulate or abuse the review generation system.</li>
                <li>Interfere with or disrupt the service infrastructure.</li>
                <li>Use the service in violation of any applicable laws or regulations.</li>
                <li>Share or distribute review links intended for other individuals.</li>
              </ul>
            </section>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold text-foreground">5. AI-Generated Content</h2>
              <p className="text-sm text-muted-foreground leading-relaxed">
                Review drafts are generated using artificial intelligence based on feedback
                you provide. While we strive for accuracy and quality, AI-generated content
                may not always perfectly reflect your intentions. You have the opportunity to
                review, edit, approve, or decline all drafts before they are posted.
              </p>
            </section>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold text-foreground">6. Third-Party Platforms</h2>
              <p className="text-sm text-muted-foreground leading-relaxed">
                Our service integrates with third-party platforms including Google Business
                Profile, WhatsApp (Meta), and email providers. Your use of these platforms is
                subject to their respective terms of service and privacy policies. We are not
                responsible for the actions or policies of third-party platforms.
              </p>
            </section>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold text-foreground">7. Disclaimer of Warranties</h2>
              <p className="text-sm text-muted-foreground leading-relaxed">
                The service is provided on an "as is" and "as available" basis without
                warranties of any kind, whether express or implied. We do not warrant that
                the service will meet your specific requirements or that the AI-generated
                content will be error-free.
              </p>
            </section>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold text-foreground">8. Termination</h2>
              <p className="text-sm text-muted-foreground leading-relaxed">
                We reserve the right to suspend or terminate your access to the service at
                any time, with or without notice, for conduct that we believe violates these
                Terms or is harmful to other users or the service.
              </p>
            </section>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold text-foreground">9. Governing Law</h2>
              <p className="text-sm text-muted-foreground leading-relaxed">
                These Terms shall be governed by and construed in accordance with the laws of
                India. Any disputes arising from these Terms shall be subject to the
                exclusive jurisdiction of the courts in India.
              </p>
            </section>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold text-foreground">10. Contact</h2>
              <p className="text-sm text-muted-foreground leading-relaxed">
                For questions about these Terms of Service, contact us at{" "}
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

export default TermsOfServicePage;
