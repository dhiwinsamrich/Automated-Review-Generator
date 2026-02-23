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
            <div className="space-y-4">
              <h1 className="text-3xl font-bold text-foreground">Terms of Service</h1>
              <p className="text-sm text-muted-foreground">
                Last Updated: 20-02-2026
              </p>
              <p className="text-sm text-muted-foreground leading-relaxed mt-4">
                These Terms of Service (“Terms”) govern your access to and use of the website https://www.bdcode.in/ (the “Website”), operated by bdcode_ (“bdcode_”, “we”, “our”, or “us”).
              </p>
              <p className="text-sm font-semibold text-foreground uppercase">
                BY ACCESSING OR USING THIS WEBSITE, YOU AGREE TO BE BOUND BY THESE TERMS. IF YOU DO NOT AGREE, PLEASE DO NOT USE THIS WEBSITE.
              </p>
            </div>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold text-foreground">1. Acceptance of Terms</h2>
              <p className="text-sm text-muted-foreground leading-relaxed">
                bdcode_ reserves the right, at its sole discretion, to modify, update, or replace these Terms at any time. Changes will be effective immediately upon posting.
              </p>
              <p className="text-sm text-muted-foreground leading-relaxed">
                Your continued use of the Website after changes are posted constitutes acceptance of the revised Terms.
              </p>
            </section>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold text-foreground">2. Use of the Website</h2>
              <p className="text-sm text-muted-foreground leading-relaxed">
                You are granted a limited, non-exclusive, non-transferable, revocable license to access and use the Website solely for:
              </p>
              <ul className="list-disc list-inside text-sm text-muted-foreground space-y-1.5 ml-2">
                <li>Learning about bdcode_’s services</li>
                <li>Evaluating a potential business relationship</li>
                <li>Communicating with bdcode_</li>
                <li>Accessing permitted content</li>
              </ul>
              <p className="text-sm text-muted-foreground leading-relaxed mt-2">
                You agree that you will NOT:
              </p>
              <ul className="list-disc list-inside text-sm text-muted-foreground space-y-1.5 ml-2">
                <li>Copy, reproduce, modify, or distribute Website content without permission</li>
                <li>Reverse engineer or tamper with Website software or code</li>
                <li>Use the Website for unlawful purposes</li>
                <li>Upload malicious code, viruses, or harmful content</li>
                <li>Attempt unauthorized access to secure areas</li>
              </ul>
              <p className="text-sm text-muted-foreground leading-relaxed mt-2">
                Your use must comply with all applicable laws and regulations.
              </p>
            </section>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold text-foreground">3. Intellectual Property</h2>
              <p className="text-sm text-muted-foreground leading-relaxed">
                All content on this Website, including but not limited to:
              </p>
              <ul className="list-disc list-inside text-sm text-muted-foreground space-y-1.5 ml-2">
                <li>Text</li>
                <li>Graphics</li>
                <li>Logos</li>
                <li>Icons</li>
                <li>Design elements</li>
                <li>Software</li>
                <li>Code</li>
                <li>Layout</li>
                <li>Visual interfaces</li>
              </ul>
              <p className="text-sm text-muted-foreground leading-relaxed mt-2">
                (collectively, “Content”) is owned by or licensed to bdcode_ and is protected by copyright, trademark, and intellectual property laws.
              </p>
              <p className="text-sm text-muted-foreground leading-relaxed">
                Nothing in these Terms grants you ownership rights in the Content.
              </p>
              <p className="text-sm text-muted-foreground leading-relaxed mt-2">
                You may not:
              </p>
              <ul className="list-disc list-inside text-sm text-muted-foreground space-y-1.5 ml-2">
                <li>Republish or redistribute Content</li>
                <li>Create derivative works</li>
                <li>Use bdcode_ trademarks without written permission</li>
              </ul>
            </section>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold text-foreground">4. Services & Project Engagements</h2>
              <p className="text-sm text-muted-foreground leading-relaxed">
                bdcode_ provides technology development, consulting, and related services.
              </p>
              <p className="text-sm text-muted-foreground leading-relaxed">
                Any obligations related to services, payments, intellectual property ownership, deliverables, or timelines shall be governed solely by separate written agreements executed between bdcode_ and the client.
              </p>
              <p className="text-sm text-muted-foreground leading-relaxed">
                Nothing on this Website constitutes a binding offer unless formalized through a signed agreement.
              </p>
              <p className="text-sm text-muted-foreground leading-relaxed mt-2">
                bdcode_ reserves the right to:
              </p>
              <ul className="list-disc list-inside text-sm text-muted-foreground space-y-1.5 ml-2">
                <li>Modify or discontinue services</li>
                <li>Update pricing</li>
                <li>Refuse service at its discretion</li>
              </ul>
            </section>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold text-foreground">5. User Communications & Submissions</h2>
              <p className="text-sm text-muted-foreground leading-relaxed">
                Any feedback, suggestions, ideas, or communications submitted through the Website (“Submissions”), except personal data covered under our Privacy Policy, shall be considered non-confidential and non-proprietary.
              </p>
              <p className="text-sm text-muted-foreground leading-relaxed mt-2">
                By submitting content, you:
              </p>
              <ul className="list-disc list-inside text-sm text-muted-foreground space-y-1.5 ml-2">
                <li>Confirm you have the right to share it</li>
                <li>Grant bdcode_ the right to use it for business purposes</li>
                <li>Agree that bdcode_ is not obligated to compensate you</li>
              </ul>
              <p className="text-sm text-muted-foreground leading-relaxed mt-2">
                You are solely responsible for the legality and accuracy of your communications.
              </p>
              <p className="text-sm text-muted-foreground leading-relaxed mt-2">
                You may not submit content that is:
              </p>
              <ul className="list-disc list-inside text-sm text-muted-foreground space-y-1.5 ml-2">
                <li>Defamatory</li>
                <li>Unlawful</li>
                <li>Obscene</li>
                <li>Fraudulent</li>
                <li>Infringing third-party rights</li>
              </ul>
            </section>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold text-foreground">6. Privacy</h2>
              <p className="text-sm text-muted-foreground leading-relaxed">
                Your use of this Website is also governed by our Privacy Policy, which explains how we collect, use, and protect personal information.
              </p>
              <p className="text-sm text-muted-foreground leading-relaxed">
                By using the Website, you acknowledge that internet transmissions are never completely secure, and you assume this risk.
              </p>
            </section>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold text-foreground">7. Security & Password-Protected Areas</h2>
              <p className="text-sm text-muted-foreground leading-relaxed">
                If certain features require account access:
              </p>
              <ul className="list-disc list-inside text-sm text-muted-foreground space-y-1.5 ml-2">
                <li>You are responsible for maintaining password confidentiality</li>
                <li>You are responsible for all activity under your account</li>
                <li>You must notify us immediately of unauthorized access</li>
              </ul>
              <p className="text-sm text-muted-foreground leading-relaxed mt-2">
                Unauthorized access to secured areas may result in termination and legal action.
              </p>
            </section>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold text-foreground">8. Third-Party Links</h2>
              <p className="text-sm text-muted-foreground leading-relaxed">
                This Website may contain links to third-party websites.
              </p>
              <p className="text-sm text-muted-foreground leading-relaxed mt-2">
                bdcode_:
              </p>
              <ul className="list-disc list-inside text-sm text-muted-foreground space-y-1.5 ml-2">
                <li>Does not control third-party sites</li>
                <li>Is not responsible for their content or practices</li>
                <li>Does not endorse third-party products or services</li>
              </ul>
              <p className="text-sm text-muted-foreground leading-relaxed mt-2">
                Accessing third-party websites is at your own risk.
              </p>
            </section>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold text-foreground">9. Disclaimer of Warranties</h2>
              <p className="text-sm font-semibold text-foreground uppercase">
                TO THE MAXIMUM EXTENT PERMITTED BY LAW, THE WEBSITE AND ALL CONTENT ARE PROVIDED “AS IS” AND “AS AVAILABLE.”
              </p>
              <p className="text-sm text-muted-foreground leading-relaxed mt-2">
                bdcode_ makes no warranties, express or implied, including but not limited to:
              </p>
              <ul className="list-disc list-inside text-sm text-muted-foreground space-y-1.5 ml-2">
                <li>Accuracy</li>
                <li>Reliability</li>
                <li>Availability</li>
                <li>Fitness for a particular purpose</li>
                <li>Non-infringement</li>
              </ul>
              <p className="text-sm text-muted-foreground leading-relaxed mt-2">
                We do not guarantee uninterrupted or error-free operation.
              </p>
            </section>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold text-foreground">10. Limitation of Liability</h2>
              <p className="text-sm font-semibold text-foreground uppercase">
                TO THE MAXIMUM EXTENT PERMITTED BY LAW, bdcode_ SHALL NOT BE LIABLE FOR:
              </p>
              <ul className="list-disc list-inside text-sm text-muted-foreground space-y-1.5 ml-2 mt-2">
                <li>Indirect damages</li>
                <li>Incidental damages</li>
                <li>Consequential damages</li>
                <li>Loss of profits</li>
                <li>Loss of data</li>
                <li>Business interruption</li>
              </ul>
              <p className="text-sm text-muted-foreground leading-relaxed mt-2">
                If liability is established, bdcode_’s total liability shall not exceed the amount paid (if any) for accessing the Website.
              </p>
            </section>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold text-foreground">11. Indemnification</h2>
              <p className="text-sm text-muted-foreground leading-relaxed">
                You agree to indemnify and hold harmless bdcode_, its directors, employees, partners, and affiliates from any claims, damages, liabilities, costs, or expenses (including legal fees) arising from:
              </p>
              <ul className="list-disc list-inside text-sm text-muted-foreground space-y-1.5 ml-2">
                <li>Your use of the Website</li>
                <li>Your violation of these Terms</li>
                <li>Your violation of any third-party rights</li>
              </ul>
            </section>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold text-foreground">12. Termination</h2>
              <p className="text-sm text-muted-foreground leading-relaxed">
                bdcode_ reserves the right to:
              </p>
              <ul className="list-disc list-inside text-sm text-muted-foreground space-y-1.5 ml-2">
                <li>Suspend or terminate access</li>
                <li>Remove content</li>
                <li>Block users</li>
              </ul>
              <p className="text-sm text-muted-foreground leading-relaxed mt-2">
                If you violate these Terms or applicable laws.
              </p>
              <p className="text-sm text-muted-foreground leading-relaxed">
                Termination does not limit bdcode_’s right to pursue legal remedies.
              </p>
            </section>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold text-foreground">13. Governing Law & Jurisdiction</h2>
              <p className="text-sm text-muted-foreground leading-relaxed">
                These Terms shall be governed by and interpreted in accordance with the laws of India.
              </p>
              <p className="text-sm text-muted-foreground leading-relaxed">
                Any disputes arising from or related to these Terms shall be subject to the exclusive jurisdiction of the courts located in:
              </p>
              <p className="text-sm text-muted-foreground leading-relaxed font-semibold">
                Chennai, Tamil Nadu
              </p>
              <p className="text-sm text-muted-foreground leading-relaxed mt-2">
                The parties agree to attempt good faith negotiation before initiating formal legal proceedings.
              </p>
            </section>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold text-foreground">14. Severability</h2>
              <p className="text-sm text-muted-foreground leading-relaxed">
                If any provision of these Terms is found to be invalid or unenforceable, the remaining provisions shall remain in full force and effect.
              </p>
            </section>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold text-foreground">15. Entire Agreement</h2>
              <p className="text-sm text-muted-foreground leading-relaxed">
                These Terms, along with the Privacy Policy and any service agreements, constitute the entire agreement between you and bdcode_ regarding use of the Website.
              </p>
            </section>

            <section className="space-y-3">
              <h2 className="text-xl font-semibold text-foreground">16. Contact Information</h2>
              <p className="text-sm text-muted-foreground leading-relaxed">
                If you have questions regarding these Terms, please contact:
              </p>
              <div className="text-sm text-muted-foreground leading-relaxed mt-2 space-y-1">
                <p><strong>bdcode_</strong></p>
                <p>Website: <a href="https://www.bdcode.in/" className="text-primary hover:underline">https://www.bdcode.in/</a></p>
                <p>Email: <a href="mailto:sales@bdcode.in" className="text-primary hover:underline">sales@bdcode.in</a></p>
              </div>
            </section>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default TermsOfServicePage;
