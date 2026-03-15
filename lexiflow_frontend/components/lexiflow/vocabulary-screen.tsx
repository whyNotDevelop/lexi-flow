"use client"

import { Book, Bookmark, Settings, Search, Trash2 } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

interface VocabularyScreenProps {
  onNavigate: (screen: string) => void
}

const savedWords = [
  { word: "Serendipitous", meaning: "Occurring by chance in a happy way", savedAt: "Today" },
  { word: "Ephemeral", meaning: "Lasting for a very short time", savedAt: "Today" },
  { word: "Melancholic", meaning: "Sad and depressed", savedAt: "Yesterday" },
  { word: "Antiquarian", meaning: "Relating to antiques or rare books", savedAt: "Yesterday" },
  { word: "Poignant", meaning: "Evoking sadness or regret", savedAt: "Mar 10" },
  { word: "Perpetual", meaning: "Never ending or changing", savedAt: "Mar 9" },
]

export function VocabularyScreen({ onNavigate }: VocabularyScreenProps) {
  return (
    <div className="h-full flex flex-col bg-background">
      {/* Header */}
      <div className="px-5 pt-3 pb-4">
        <h1 className="text-xl font-semibold text-foreground">My Vocabulary</h1>
        <p className="text-xs text-muted-foreground mt-1">{savedWords.length} words saved</p>
        
        {/* Search */}
        <div className="relative mt-4">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input 
            placeholder="Search saved words..." 
            className="pl-9 bg-secondary border-0 h-10 text-sm"
          />
        </div>
      </div>

      {/* Word list */}
      <div className="flex-1 overflow-y-auto px-5">
        <div className="space-y-2">
          {savedWords.map((item, index) => (
            <div 
              key={index}
              className="flex items-center justify-between p-3 bg-card rounded-xl border border-border"
            >
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <h3 className="font-medium text-foreground">{item.word}</h3>
                  <span className="text-xs text-muted-foreground">{item.savedAt}</span>
                </div>
                <p className="text-xs text-muted-foreground mt-0.5 truncate">{item.meaning}</p>
              </div>
              <Button variant="ghost" size="icon" className="h-8 w-8 text-muted-foreground hover:text-destructive shrink-0">
                <Trash2 className="h-4 w-4" />
              </Button>
            </div>
          ))}
        </div>
      </div>

      {/* Stats card */}
      <div className="px-5 py-3">
        <div className="bg-primary/10 rounded-xl p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs text-muted-foreground">This Week</p>
              <p className="text-lg font-semibold text-foreground">12 words</p>
            </div>
            <div className="text-right">
              <p className="text-xs text-muted-foreground">Total</p>
              <p className="text-lg font-semibold text-primary">{savedWords.length}</p>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom navigation */}
      <div className="flex items-center justify-around py-3 border-t border-border bg-card">
        <Button 
          variant="ghost" 
          size="sm" 
          className="flex flex-col items-center gap-1 h-auto py-2"
          onClick={() => onNavigate("reading")}
        >
          <Book className="h-5 w-5 text-muted-foreground" />
          <span className="text-xs text-muted-foreground">Reading</span>
        </Button>
        <Button variant="ghost" size="sm" className="flex flex-col items-center gap-1 h-auto py-2">
          <Bookmark className="h-5 w-5 text-primary" />
          <span className="text-xs text-primary font-medium">Vocabulary</span>
        </Button>
        <Button 
          variant="ghost" 
          size="sm" 
          className="flex flex-col items-center gap-1 h-auto py-2"
          onClick={() => onNavigate("history")}
        >
          <svg className="h-5 w-5 text-muted-foreground" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span className="text-xs text-muted-foreground">History</span>
        </Button>
        <Button 
          variant="ghost" 
          size="sm" 
          className="flex flex-col items-center gap-1 h-auto py-2"
          onClick={() => onNavigate("settings")}
        >
          <Settings className="h-5 w-5 text-muted-foreground" />
          <span className="text-xs text-muted-foreground">Settings</span>
        </Button>
      </div>
    </div>
  )
}
