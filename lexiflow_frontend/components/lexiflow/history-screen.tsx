"use client"

import { Book, Bookmark, Settings, Trash2 } from "lucide-react"
import { Button } from "@/components/ui/button"

interface HistoryScreenProps {
  onNavigate: (screen: string) => void
}

const historyItems = [
  { word: "Serendipitous", time: "2 min ago", saved: true },
  { word: "Ephemeral", time: "5 min ago", saved: true },
  { word: "Provincial", time: "8 min ago", saved: false },
  { word: "Calligraphy", time: "12 min ago", saved: false },
  { word: "Meticulous", time: "15 min ago", saved: false },
  { word: "Pirouetted", time: "20 min ago", saved: false },
  { word: "Antiquarian", time: "Yesterday", saved: true },
  { word: "Melancholic", time: "Yesterday", saved: true },
  { word: "Poignant", time: "Mar 10", saved: true },
]

export function HistoryScreen({ onNavigate }: HistoryScreenProps) {
  return (
    <div className="h-full flex flex-col bg-background">
      {/* Header */}
      <div className="px-5 pt-3 pb-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-xl font-semibold text-foreground">Lookup History</h1>
            <p className="text-xs text-muted-foreground mt-1">{historyItems.length} words looked up</p>
          </div>
          <Button variant="ghost" size="sm" className="text-xs text-muted-foreground hover:text-destructive">
            Clear All
          </Button>
        </div>
      </div>

      {/* History list */}
      <div className="flex-1 overflow-y-auto px-5">
        <div className="space-y-2">
          {historyItems.map((item, index) => (
            <div 
              key={index}
              className="flex items-center justify-between p-3 bg-card rounded-xl border border-border"
            >
              <div className="flex-1 min-w-0">
                <div className="flex items-center gap-2">
                  <h3 className="font-medium text-foreground">{item.word}</h3>
                  {item.saved && (
                    <Bookmark className="h-3.5 w-3.5 text-primary fill-current" />
                  )}
                </div>
                <p className="text-xs text-muted-foreground mt-0.5">{item.time}</p>
              </div>
              <div className="flex items-center gap-1">
                {!item.saved && (
                  <Button variant="ghost" size="icon" className="h-8 w-8 text-muted-foreground hover:text-primary">
                    <Bookmark className="h-4 w-4" />
                  </Button>
                )}
                <Button variant="ghost" size="icon" className="h-8 w-8 text-muted-foreground hover:text-destructive">
                  <Trash2 className="h-4 w-4" />
                </Button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Stats */}
      <div className="px-5 py-3">
        <div className="grid grid-cols-3 gap-3">
          <div className="bg-card rounded-xl p-3 border border-border text-center">
            <p className="text-lg font-semibold text-foreground">23</p>
            <p className="text-xs text-muted-foreground">Today</p>
          </div>
          <div className="bg-card rounded-xl p-3 border border-border text-center">
            <p className="text-lg font-semibold text-foreground">89</p>
            <p className="text-xs text-muted-foreground">This Week</p>
          </div>
          <div className="bg-card rounded-xl p-3 border border-border text-center">
            <p className="text-lg font-semibold text-primary">342</p>
            <p className="text-xs text-muted-foreground">Total</p>
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
        <Button 
          variant="ghost" 
          size="sm" 
          className="flex flex-col items-center gap-1 h-auto py-2"
          onClick={() => onNavigate("vocabulary")}
        >
          <Bookmark className="h-5 w-5 text-muted-foreground" />
          <span className="text-xs text-muted-foreground">Vocabulary</span>
        </Button>
        <Button variant="ghost" size="sm" className="flex flex-col items-center gap-1 h-auto py-2">
          <svg className="h-5 w-5 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span className="text-xs text-primary font-medium">History</span>
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
