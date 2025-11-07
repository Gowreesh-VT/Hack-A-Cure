import { Heart, Github, AlertTriangle } from "lucide-react";

const Footer = () => {
  return (
    <footer className="bg-gradient-hero text-white py-12 px-4">
      <div className="container mx-auto max-w-6xl">
        {/* Disclaimer */}
        <div className="bg-white/10 backdrop-blur-sm border border-white/20 rounded-2xl p-6 mb-8 animate-fade-in">
          <div className="flex items-start gap-3">
            <AlertTriangle className="w-6 h-6 flex-shrink-0 mt-1 text-yellow-300" />
            <div>
              <h3 className="font-semibold mb-2">Important Disclaimer</h3>
              <p className="text-sm text-white/80 leading-relaxed">
                ⚠️ MedAI is for educational purposes only and not a substitute for professional medical advice. 
                Always consult with qualified healthcare professionals for medical advice, diagnosis, or treatment.
              </p>
            </div>
          </div>
        </div>

        {/* Footer content */}
        <div className="grid md:grid-cols-3 gap-8 mb-8">
          <div>
            <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
              <Heart className="w-5 h-5" />
              MedAI
            </h3>
            <p className="text-sm text-white/80 leading-relaxed">
              Your intelligent medical assistant built with RAG technology for Hack A Cure 2025.
            </p>
          </div>

          <div>
            <h4 className="font-semibold mb-4">Quick Links</h4>
            <ul className="space-y-2 text-sm">
              <li>
                <a href="#about" className="text-white/80 hover:text-white transition-colors">
                  About
                </a>
              </li>
              <li>
                <a href="#features" className="text-white/80 hover:text-white transition-colors">
                  Features
                </a>
              </li>
              <li>
                <a href="#team" className="text-white/80 hover:text-white transition-colors">
                  Team
                </a>
              </li>
              <li>
                <a href="#" className="text-white/80 hover:text-white transition-colors">
                  Privacy Policy
                </a>
              </li>
            </ul>
          </div>

          <div>
            <h4 className="font-semibold mb-4">Connect</h4>
            <ul className="space-y-2 text-sm">
              <li>
                <a href="#" className="text-white/80 hover:text-white transition-colors flex items-center gap-2">
                  <Github className="w-4 h-4" />
                  GitHub Repository
                </a>
              </li>
              <li>
                <a href="#" className="text-white/80 hover:text-white transition-colors">
                  Hack A Cure 2025
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom bar */}
        <div className="pt-8 border-t border-white/20 text-center">
          <p className="text-sm text-white/80">
            © 2025 MedAI. Built with ❤️ for Hack A Cure 2025.
          </p>
          
          {/* Heartbeat animation */}
          <div className="mt-4 flex justify-center">
            <div className="relative w-24 h-8">
              <svg className="w-full h-full opacity-30" viewBox="0 0 100 30">
                <polyline
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                  points="0,15 20,15 25,5 30,25 35,15 100,15"
                  className="animate-pulse-slow"
                />
              </svg>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
