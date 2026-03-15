"use client"

import { LexiFlowApp } from "@/components/lexiflow/lexiflow-app"
import { BookOpen, Sparkles, Clock, BookmarkCheck, Zap, Globe } from "lucide-react"

export default function LexiFlowDesignPage() {
  return (
    <div className="min-h-screen bg-background">
      {/* Hero Section */}
      <header className="relative overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-primary/10 via-transparent to-transparent" />
        
        <div className="relative max-w-6xl mx-auto px-6 py-12 lg:py-20">
          <div className="flex flex-col lg:flex-row items-center gap-12 lg:gap-16">
            {/* Left content */}
            <div className="flex-1 text-center lg:text-left">
              <div className="inline-flex items-center gap-2 px-3 py-1.5 bg-primary/10 rounded-full text-primary text-sm font-medium mb-6">
                <Sparkles className="h-4 w-4" />
                <span>Mobile Reading Assistant</span>
              </div>
              
              <h1 className="text-4xl lg:text-5xl font-bold text-foreground leading-tight text-balance">
                Look up words
                <span className="text-primary"> instantly</span>
                <br />while reading
              </h1>
              
              <p className="mt-6 text-lg text-muted-foreground leading-relaxed max-w-xl">
                LexiFlow lets you tap any word to see its definition without leaving your book. 
                Save vocabulary, track your learning progress, and enhance your reading experience.
              </p>

              {/* Feature pills */}
              <div className="flex flex-wrap justify-center lg:justify-start gap-3 mt-8">
                <div className="flex items-center gap-2 px-4 py-2 bg-card border border-border rounded-full">
                  <Zap className="h-4 w-4 text-accent" />
                  <span className="text-sm text-foreground">Instant Lookup</span>
                </div>
                <div className="flex items-center gap-2 px-4 py-2 bg-card border border-border rounded-full">
                  <BookmarkCheck className="h-4 w-4 text-primary" />
                  <span className="text-sm text-foreground">Save Words</span>
                </div>
                <div className="flex items-center gap-2 px-4 py-2 bg-card border border-border rounded-full">
                  <Clock className="h-4 w-4 text-muted-foreground" />
                  <span className="text-sm text-foreground">Track Progress</span>
                </div>
              </div>
            </div>

            {/* Phone mockup */}
            <div className="flex-shrink-0">
              <LexiFlowApp />
            </div>
          </div>
        </div>
      </header>

      {/* Features Section */}
      <section className="py-16 lg:py-24 bg-secondary/30">
        <div className="max-w-6xl mx-auto px-6">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-foreground">Designed for Readers</h2>
            <p className="mt-3 text-muted-foreground max-w-2xl mx-auto">
              Every feature is crafted to keep you immersed in your reading while building your vocabulary.
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            <FeatureCard
              icon={<BookOpen className="h-6 w-6" />}
              title="Seamless Reading"
              description="Tap any word to instantly see its definition without leaving the page. No more switching between apps."
            />
            <FeatureCard
              icon={<BookmarkCheck className="h-6 w-6" />}
              title="Personal Vocabulary"
              description="Save words you want to remember. Build your personal word library over time."
            />
            <FeatureCard
              icon={<Clock className="h-6 w-6" />}
              title="Lookup History"
              description="Track every word you've looked up. Review your learning journey and patterns."
            />
            <FeatureCard
              icon={<Sparkles className="h-6 w-6" />}
              title="Rich Definitions"
              description="Get meanings, synonyms, and example sentences for better understanding."
            />
            <FeatureCard
              icon={<Globe className="h-6 w-6" />}
              title="Multiple Sources"
              description="Definitions sourced from trusted dictionaries for accuracy and depth."
            />
            <FeatureCard
              icon={<Zap className="h-6 w-6" />}
              title="Lightning Fast"
              description="Cached results ensure instant access to previously looked-up words."
            />
          </div>
        </div>
      </section>

      {/* Design System Section */}
      <section className="py-16 lg:py-24">
        <div className="max-w-6xl mx-auto px-6">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-foreground">Design System</h2>
            <p className="mt-3 text-muted-foreground max-w-2xl mx-auto">
              A cohesive design language built for readability and minimal friction.
            </p>
          </div>

          {/* Color Palette */}
          <div className="mb-12">
            <h3 className="text-lg font-semibold text-foreground mb-4">Color Palette</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
              <ColorSwatch name="Primary" className="bg-primary" textColor="text-primary-foreground" />
              <ColorSwatch name="Accent" className="bg-accent" textColor="text-accent-foreground" />
              <ColorSwatch name="Background" className="bg-background border border-border" textColor="text-foreground" />
              <ColorSwatch name="Card" className="bg-card border border-border" textColor="text-card-foreground" />
              <ColorSwatch name="Muted" className="bg-muted" textColor="text-muted-foreground" />
              <ColorSwatch name="Secondary" className="bg-secondary" textColor="text-secondary-foreground" />
            </div>
          </div>

          {/* Typography */}
          <div className="mb-12">
            <h3 className="text-lg font-semibold text-foreground mb-4">Typography</h3>
            <div className="space-y-4 bg-card p-6 rounded-xl border border-border">
              <div>
                <p className="text-xs text-muted-foreground mb-1">Heading 1</p>
                <p className="text-4xl font-bold text-foreground">The Silent Garden</p>
              </div>
              <div>
                <p className="text-xs text-muted-foreground mb-1">Heading 2</p>
                <p className="text-2xl font-semibold text-foreground">Chapter One</p>
              </div>
              <div>
                <p className="text-xs text-muted-foreground mb-1">Body Text</p>
                <p className="text-base text-foreground leading-relaxed">
                  The old man sat alone in his study, surrounded by towering shelves of antiquarian books.
                </p>
              </div>
              <div>
                <p className="text-xs text-muted-foreground mb-1">Caption</p>
                <p className="text-sm text-muted-foreground">Tap underlined words for definitions</p>
              </div>
            </div>
          </div>

          {/* Component Hierarchy */}
          <div>
            <h3 className="text-lg font-semibold text-foreground mb-4">Component Hierarchy</h3>
            <div className="bg-card p-6 rounded-xl border border-border">
              <div className="font-mono text-sm text-foreground space-y-2">
                <p className="text-primary">LexiFlowApp</p>
                <p className="pl-4">├── PhoneMockup</p>
                <p className="pl-4">├── LoginScreen</p>
                <p className="pl-4">├── ReadingScreen</p>
                <p className="pl-8">│   └── WordDefinitionPopup</p>
                <p className="pl-4">├── VocabularyScreen</p>
                <p className="pl-4">├── HistoryScreen</p>
                <p className="pl-4">└── SettingsScreen</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* UX Flow Section */}
      <section className="py-16 lg:py-24 bg-secondary/30">
        <div className="max-w-6xl mx-auto px-6">
          <div className="text-center mb-12">
            <h2 className="text-3xl font-bold text-foreground">User Flow</h2>
            <p className="mt-3 text-muted-foreground max-w-2xl mx-auto">
              Minimal steps from reading to understanding.
            </p>
          </div>

          <div className="flex flex-col md:flex-row items-center justify-center gap-4 md:gap-8">
            <FlowStep number={1} title="Tap Word" description="Select any word while reading" />
            <FlowArrow />
            <FlowStep number={2} title="View Definition" description="Instantly see meaning & examples" />
            <FlowArrow />
            <FlowStep number={3} title="Save to Library" description="Build your vocabulary collection" />
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 border-t border-border">
        <div className="max-w-6xl mx-auto px-6">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center">
                <BookOpen className="h-4 w-4 text-primary-foreground" />
              </div>
              <span className="font-semibold text-foreground">LexiFlow</span>
            </div>
            <p className="text-sm text-muted-foreground">
              UI Design Prototype — Built with React Native patterns
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}

function FeatureCard({ icon, title, description }: { icon: React.ReactNode; title: string; description: string }) {
  return (
    <div className="bg-card p-6 rounded-xl border border-border hover:border-primary/30 transition-colors">
      <div className="w-12 h-12 rounded-xl bg-primary/10 flex items-center justify-center text-primary mb-4">
        {icon}
      </div>
      <h3 className="text-lg font-semibold text-foreground mb-2">{title}</h3>
      <p className="text-sm text-muted-foreground leading-relaxed">{description}</p>
    </div>
  )
}

function ColorSwatch({ name, className, textColor }: { name: string; className: string; textColor: string }) {
  return (
    <div className={`${className} rounded-xl p-4 h-24 flex flex-col justify-end`}>
      <span className={`text-sm font-medium ${textColor}`}>{name}</span>
    </div>
  )
}

function FlowStep({ number, title, description }: { number: number; title: string; description: string }) {
  return (
    <div className="flex flex-col items-center text-center">
      <div className="w-12 h-12 rounded-full bg-primary flex items-center justify-center text-primary-foreground font-bold text-lg mb-3">
        {number}
      </div>
      <h3 className="font-semibold text-foreground">{title}</h3>
      <p className="text-sm text-muted-foreground mt-1">{description}</p>
    </div>
  )
}

function FlowArrow() {
  return (
    <svg className="h-6 w-6 text-muted-foreground hidden md:block" fill="none" stroke="currentColor" viewBox="0 0 24 24">
      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
    </svg>
  )
}
