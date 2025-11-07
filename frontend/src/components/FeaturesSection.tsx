import { Card } from "@/components/ui/card";
import { Activity, BookOpen, Shield, Zap } from "lucide-react";

const FeaturesSection = () => {
  const features = [
    {
      icon: <Activity className="w-8 h-8" />,
      title: "Symptom to Condition Mapping",
      description: "Advanced AI algorithms analyze your symptoms and map them to potential conditions using verified medical knowledge bases.",
      gradient: "from-primary to-secondary"
    },
    {
      icon: <BookOpen className="w-8 h-8" />,
      title: "Trusted Medical References",
      description: "Every response includes citations from peer-reviewed sources, ensuring transparency and reliability in health information.",
      gradient: "from-secondary to-accent"
    },
    {
      icon: <Shield className="w-8 h-8" />,
      title: "Privacy & Ethical AI",
      description: "Your health information stays private. We follow strict ethical AI guidelines and healthcare data protection standards.",
      gradient: "from-accent to-primary"
    },
    {
      icon: <Zap className="w-8 h-8" />,
      title: "24-Hour Hackathon Innovation",
      description: "Built during Hack A Cure 2025, showcasing rapid innovation in healthcare technology for the benefit of patients everywhere.",
      gradient: "from-success to-secondary"
    }
  ];

  return (
    <section className="py-20 px-4 bg-muted/30">
      <div className="container mx-auto max-w-7xl">
        <div className="text-center mb-16 space-y-4 animate-fade-in-up">
          <h2 className="text-4xl md:text-5xl font-bold text-foreground">
            Powerful Features
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            SymptomSense combines cutting-edge AI technology with medical expertise 
            to deliver accurate, trustworthy health information.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-8">
          {features.map((feature, index) => (
            <Card 
              key={index}
              className="group relative overflow-hidden p-8 border-border shadow-soft hover:shadow-strong transition-all duration-500 hover:-translate-y-2 animate-scale-in bg-card"
              style={{ animationDelay: `${index * 0.15}s` }}
            >
              {/* Gradient background on hover */}
              <div className={`absolute inset-0 bg-gradient-to-br ${feature.gradient} opacity-0 group-hover:opacity-5 transition-opacity duration-500`} />
              
              <div className="relative z-10">
                <div className={`w-16 h-16 rounded-2xl bg-gradient-to-br ${feature.gradient} flex items-center justify-center mb-6 text-white shadow-medium group-hover:scale-110 transition-transform duration-300`}>
                  {feature.icon}
                </div>
                
                <h3 className="text-2xl font-bold mb-4 text-foreground">
                  {feature.title}
                </h3>
                
                <p className="text-muted-foreground leading-relaxed">
                  {feature.description}
                </p>
              </div>

              {/* Decorative element */}
              <div className="absolute -bottom-4 -right-4 w-24 h-24 bg-gradient-to-br from-primary/10 to-secondary/10 rounded-full blur-2xl group-hover:scale-150 transition-transform duration-500" />
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
};

export default FeaturesSection;
