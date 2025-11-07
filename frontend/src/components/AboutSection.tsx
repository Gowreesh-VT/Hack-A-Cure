import { Card } from "@/components/ui/card";
import { CheckCircle, Search, Brain, Trophy } from "lucide-react";

const AboutSection = () => {
  const features = [
    {
      icon: <CheckCircle className="w-6 h-6" />,
      title: "RAG-based accuracy",
      description: "Powered by Retrieval-Augmented Generation"
    },
    {
      icon: <Search className="w-6 h-6" />,
      title: "Citation-backed answers",
      description: "Responses from trusted medical sources"
    },
    {
      icon: <Brain className="w-6 h-6" />,
      title: "Ethical AI",
      description: "Built with medical data privacy in mind"
    },
    {
      icon: <Trophy className="w-6 h-6" />,
      title: "Built for Hack A Cure 2025",
      description: "Innovation in healthcare technology"
    }
  ];

  return (
    <section id="about" className="py-20 px-4 bg-background">
      <div className="container mx-auto max-w-6xl">
        <div className="text-center mb-16 space-y-4 animate-fade-in-up">
          <h2 className="text-4xl md:text-5xl font-bold text-foreground">
            What is MedAI?
          </h2>
          <div className="max-w-3xl mx-auto">
            <p className="text-lg text-muted-foreground leading-relaxed">
              MedAI is a Retrieval-Augmented Generation (RAG) powered chatbot designed to provide reliable, 
              explainable, and reference-backed medical information. It's created for Hack A Cure 2025 to 
              explore ethical and accurate AI in healthcare education.
            </p>
          </div>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, index) => (
            <Card 
              key={index}
              className="p-6 bg-gradient-card border-border shadow-soft hover:shadow-medium transition-all duration-300 hover:-translate-y-1 animate-scale-in group"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <div className="w-12 h-12 rounded-lg bg-gradient-accent flex items-center justify-center mb-4 text-white group-hover:scale-110 transition-transform">
                {feature.icon}
              </div>
              <h3 className="text-lg font-semibold mb-2 text-foreground">
                {feature.title}
              </h3>
              <p className="text-sm text-muted-foreground">
                {feature.description}
              </p>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
};

export default AboutSection;
