import { Button } from "@/components/ui/button";
import { ArrowRight, Bot } from "lucide-react";
import { useNavigate } from "react-router-dom";
import heroImage from "@/assets/hero-medical-ai.jpg";

const HeroSection = () => {
  const navigate = useNavigate();

  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden bg-gradient-hero">
      {/* Animated background patterns */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute top-20 left-20 w-72 h-72 bg-secondary rounded-full blur-3xl animate-pulse-slow" />
        <div className="absolute bottom-20 right-20 w-96 h-96 bg-accent rounded-full blur-3xl animate-pulse-slow" style={{ animationDelay: '1s' }} />
      </div>

      <div className="container mx-auto px-4 py-20 relative z-10">
        <div className="grid lg:grid-cols-2 gap-12 items-center">
          {/* Content */}
          <div className="text-white space-y-6 animate-fade-in">
            <div className="inline-flex items-center gap-2 bg-white/10 backdrop-blur-sm px-4 py-2 rounded-full border border-white/20">
              <Bot className="w-4 h-4" />
              <span className="text-sm font-medium">Hack A Cure 2025</span>
            </div>
            
            <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold leading-tight">
              MedAI — Your Intelligent Medical Assistant
            </h1>
            
            <p className="text-xl md:text-2xl text-white/90 leading-relaxed">
              Ask anything about medicine, diseases, anatomy, drugs, or treatments
            </p>
            
            <p className="text-lg text-white/80 leading-relaxed max-w-xl">
              Get fact-checked, citation-backed responses powered by advanced AI. Built for Hack A Cure 2025.
            </p>

            <div className="flex flex-wrap gap-4 pt-4">
              <Button 
                size="lg"
                variant="hero"
                onClick={() => navigate('/chat')}
                className="group"
              >
                Start Chatting
                <ArrowRight className="ml-2 w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </Button>
              
              <Button 
                size="lg" 
                variant="hero-outline"
              >
                Learn More
              </Button>
            </div>
          </div>

          {/* Hero Image */}
          <div className="relative animate-scale-in" style={{ animationDelay: '0.2s' }}>
            <div className="absolute inset-0 bg-gradient-accent rounded-3xl blur-2xl opacity-30 animate-pulse-slow" />
            <img 
              src={heroImage} 
              alt="Medical AI Assistant with healthcare technology"
              className="relative rounded-3xl shadow-strong w-full animate-float"
            />
          </div>
        </div>
      </div>

      {/* Scroll indicator */}
      <div className="absolute bottom-8 left-1/2 -translate-x-1/2 animate-bounce">
        <div className="w-6 h-10 border-2 border-white/30 rounded-full flex items-start justify-center p-2">
          <div className="w-1 h-2 bg-white/50 rounded-full animate-pulse" />
        </div>
      </div>
    </section>
  );
};

export default HeroSection;
