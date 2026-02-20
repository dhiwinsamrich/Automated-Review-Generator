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
                Last updated: 18-02-2026
              </p>
            </div>

            <section className="space-y-3">
              <p className="text-sm text-muted-foreground leading-relaxed">
                bdcode_ ("bdcode_", "we", "our", or "us") operates the website https://www.bdcode.in/ and provides technology, development, consulting, and related services (the "Services").
              </p>
              <p className="text-sm text-muted-foreground leading-relaxed">
                We value and respect the privacy of our clients, website visitors, partners, vendors, and job applicants. This Privacy Policy explains how we collect, use, disclose, store, and safeguard your personal information.
              </p>
            </section>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold text-foreground">Changes to This Privacy Policy</h2>
              <p className="text-sm text-muted-foreground leading-relaxed">
                We may update this Privacy Policy from time to time to reflect changes in our services, applicable laws, or privacy practices. Updates will be reflected by revising the "Last Updated" date. Continued use of the Website constitutes acceptance of the revised policy.
              </p>
            </section>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold text-foreground">Your Consent</h2>
              <ul className="list-disc list-inside text-sm text-muted-foreground space-y-1.5 ml-2">
                <li>Visiting our Website</li>
                <li>Submitting forms</li>
                <li>Contacting us via email or WhatsApp</li>
                <li>Applying for jobs</li>
                <li>Engaging our Services</li>
              </ul>
              <p className="text-sm text-muted-foreground leading-relaxed mt-2">
                You consent to the collection and use of your information as described in this Privacy Policy. You may withdraw consent at any time by contacting <a href="mailto:sales@bdcode.in" className="text-primary hover:underline">sales@bdcode.in</a>.
              </p>
            </section>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold text-foreground">Information We Collect</h2>

              <div className="space-y-2">
                <h3 className="text-md font-medium text-foreground">A. Personal Information</h3>
                <ul className="list-disc list-inside text-sm text-muted-foreground space-y-1.5 ml-2">
                  <li>Name</li>
                  <li>Email address</li>
                  <li>Phone number</li>
                  <li>Company name</li>
                  <li>Job title</li>
                  <li>Address</li>
                  <li>Resume and job application details</li>
                  <li>Information submitted via contact forms</li>
                  <li>Project-related communications</li>
                </ul>
              </div>

              <div className="space-y-2 mt-4">
                <h3 className="text-md font-medium text-foreground">B. Automatically Collected Information</h3>
                <ul className="list-disc list-inside text-sm text-muted-foreground space-y-1.5 ml-2">
                  <li>IP address</li>
                  <li>Browser and device information</li>
                  <li>Operating system</li>
                  <li>Pages visited and time spent</li>
                  <li>Referring URLs</li>
                </ul>
              </div>

              <div className="space-y-2 mt-4">
                <h3 className="text-md font-medium text-foreground">C. Analytics Information</h3>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  We may use analytics tools such as Google Analytics to understand website usage, improve performance, and enhance user experience.
                </p>
              </div>
            </section>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold text-foreground">How We Use Your Information</h2>
              <ul className="list-disc list-inside text-sm text-muted-foreground space-y-1.5 ml-2">
                <li>Provide and deliver Services</li>
                <li>Respond to inquiries and proposals</li>
                <li>Communicate about projects and contracts</li>
                <li>Process job applications</li>
                <li>Improve Website performance</li>
                <li>Ensure legal and regulatory compliance</li>
                <li>Prevent fraud and misuse</li>
              </ul>
            </section>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold text-foreground">How We Share Information</h2>
              <p className="text-sm text-muted-foreground leading-relaxed">
                We do not sell or rent your personal data. Information may be shared only:
              </p>
              <ul className="list-disc list-inside text-sm text-muted-foreground space-y-1.5 ml-2">
                <li>With trusted service providers (hosting, CRM, email tools)</li>
                <li>For legal or regulatory compliance</li>
                <li>During business transfers such as mergers or acquisitions</li>
                <li>With your explicit consent</li>
              </ul>
            </section>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold text-foreground">Data Security</h2>
              <p className="text-sm text-muted-foreground leading-relaxed">
                We implement reasonable administrative, technical, and physical safeguards including secure servers, encryption, access controls, and internal data restrictions.
              </p>
            </section>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold text-foreground">Data Retention</h2>
              <p className="text-sm text-muted-foreground leading-relaxed">
                Personal data is retained only as long as required for service delivery, legal obligations, or legitimate business purposes, after which it is securely deleted or anonymized.
              </p>
            </section>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold text-foreground">Your Rights (DPDP Act 2023)</h2>
              <ul className="list-disc list-inside text-sm text-muted-foreground space-y-1.5 ml-2">
                <li>Access your personal data</li>
                <li>Correct inaccurate data</li>
                <li>Request deletion</li>
                <li>Withdraw consent</li>
                <li>Grievance redressal</li>
                <li>Nominate a representative</li>
              </ul>
              <p className="text-sm text-muted-foreground leading-relaxed mt-2">
                To exercise these rights, contact <a href="mailto:sales@bdcode.in" className="text-primary hover:underline">sales@bdcode.in</a>.
              </p>
            </section>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold text-foreground">Children's Privacy</h2>
              <p className="text-sm text-muted-foreground leading-relaxed">
                Our Website and Services are not intended for individuals under 18 years of age. We do not knowingly collect personal data from children.
              </p>
            </section>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold text-foreground">Third-Party Links</h2>
              <p className="text-sm text-muted-foreground leading-relaxed">
                Our Website may contain links to third-party websites. We are not responsible for their privacy practices and encourage you to review their policies separately.
              </p>
            </section>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold text-foreground">International Data Transfers</h2>
              <p className="text-sm text-muted-foreground leading-relaxed">
                If you access our Website from outside India, your data may be transferred to and processed in India or other jurisdictions.
              </p>
            </section>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold text-foreground">No SMS / WhatsApp Marketing Disclosure</h2>
              <p className="text-sm text-muted-foreground leading-relaxed">
                Mobile numbers and opt-in data collected for communication purposes will not be shared with third parties for marketing or promotional activities.
              </p>
            </section>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold text-foreground">Contact Us</h2>
              <div className="text-sm text-muted-foreground leading-relaxed">
                <p className="font-medium text-foreground">bdcode_</p>
                <p>Website: <a href="https://www.bdcode.in/" className="text-primary hover:underline" target="_blank" rel="noopener noreferrer">https://www.bdcode.in/</a></p>
                <p>Email: <a href="mailto:sales@bdcode.in" className="text-primary hover:underline">sales@bdcode.in</a></p>
              </div>
            </section>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default PrivacyPolicyPage;
