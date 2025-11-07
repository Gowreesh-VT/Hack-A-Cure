import { Card } from "@/components/ui/card";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Github, Linkedin, Mail } from "lucide-react";

const TeamSection = () => {
  const team = [
    {
      name: "Gowreesh",
      role: "AI/ML Engineer",
      initials: "TM",
      bio: "Specialized in RAG systems and healthcare AI"
    },
    {
      name: "Akash Vishnu",
      role: "Full Stack Developer",
      initials: "TM",
      bio: "Building seamless user experiences"
    },
    {
      name: "Rupan Vijay",
      role: "Medical Advisor",
      initials: "TM",
      bio: "Ensuring medical accuracy and ethics"
    },
    {
      name: "Sakthivel",
      role: "UX/UI Designer",
      initials: "TM",
      bio: "Creating intuitive healthcare interfaces"
    },
    {
      name: "Hari Ganesh",
      role: "Data Scientist",
      initials: "TM",
      bio: "Optimizing data pipelines for medical insights"
    }
  ];

  return (
    <section className="py-20 px-4 bg-background">
      <div className="container mx-auto max-w-6xl">
        <div className="text-center mb-16 space-y-4 animate-fade-in-up">
          <h2 className="text-4xl md:text-5xl font-bold text-foreground">
            Meet the Team
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Team participating in Hack A Cure 2025, bringing together medicine, AI, and innovation.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {team.map((member, index) => (
            <Card 
              key={index}
              className="p-6 text-center border-border shadow-soft hover:shadow-medium transition-all duration-300 hover:-translate-y-1 animate-scale-in group bg-card"
              style={{ animationDelay: `${index * 0.1}s` }}
            >
              <Avatar className="w-24 h-24 mx-auto mb-4 ring-4 ring-primary/10 group-hover:ring-primary/30 transition-all">
                <AvatarFallback className="text-2xl font-bold bg-gradient-accent text-white">
                  {member.initials}
                </AvatarFallback>
              </Avatar>
              
              <h3 className="text-xl font-bold mb-1 text-foreground">
                {member.name}
              </h3>
              
              <p className="text-sm font-medium text-primary mb-2">
                {member.role}
              </p>
              
              <p className="text-sm text-muted-foreground mb-4">
                {member.bio}
              </p>

              <div className="flex justify-center gap-2">
                <button className="p-2 rounded-full hover:bg-muted transition-colors">
                  <Github className="w-4 h-4 text-muted-foreground hover:text-foreground" />
                </button>
                <button className="p-2 rounded-full hover:bg-muted transition-colors">
                  <Linkedin className="w-4 h-4 text-muted-foreground hover:text-foreground" />
                </button>
                <button className="p-2 rounded-full hover:bg-muted transition-colors">
                  <Mail className="w-4 h-4 text-muted-foreground hover:text-foreground" />
                </button>
              </div>
            </Card>
          ))}
        </div>
      </div>
    </section>
  );
};

export default TeamSection;
