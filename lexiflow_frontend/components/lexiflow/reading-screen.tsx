"use client"

import { useState } from "react"
import { Book, Bookmark, Settings, ChevronLeft, Sun, Moon } from "lucide-react"
import { Button } from "@/components/ui/button"
import { WordDefinitionPopup } from "./word-definition-popup"

interface ReadingScreenProps {
  onNavigate: (screen: string) => void
  isDarkMode: boolean
  onToggleDarkMode: () => void
}

const sampleText = `The old man sat alone in his study, surrounded by towering shelves of antiquarian books. The room had a certain melancholic atmosphere, filled with the scent of aged paper and leather bindings.

He turned the pages of a particularly serendipitous discovery—a first edition he had found quite unexpectedly at a provincial estate sale. The calligraphy within was exquisite, each letter formed with meticulous precision.

Outside, the ephemeral beauty of autumn was in full display. Golden leaves pirouetted through the air, their descent a poignant reminder of nature's perpetual cycle.`

const definableWords = [
  { word: "antiquarian", definitions: [{ meaning: "Relating to or dealing in antiques or rare books", example: "She specialized in antiquarian book restoration." }] },
  { word: "melancholic", definitions: [{ meaning: "Affected with or inclined to melancholy; sad and depressed", example: "The melancholic music matched his somber mood." }] },
  { word: "serendipitous", definitions: [{ meaning: "Occurring or discovered by chance in a happy or beneficial way", example: "Their meeting was entirely serendipitous." }] },
  { word: "provincial", definitions: [{ meaning: "Of or relating to a province or the provinces", example: "He grew up in a quiet provincial town." }] },
  { word: "calligraphy", definitions: [{ meaning: "Decorative handwriting or handwritten lettering", example: "She studied calligraphy for many years." }] },
  { word: "meticulous", definitions: [{ meaning: "Showing great attention to detail; very careful and precise", example: "His meticulous research uncovered new evidence." }] },
  { word: "ephemeral", definitions: [{ meaning: "Lasting for a very short time", example: "Fame in the modern world is often ephemeral." }] },
  { word: "pirouetted", definitions: [{ meaning: "Performed a pirouette; spun around on one foot", example: "The dancer pirouetted across the stage." }] },
  { word: "poignant", definitions: [{ meaning: "Evoking a keen sense of sadness or regret", example: "The photograph was a poignant reminder of happier times." }] },
  { word: "perpetual", definitions: [{ meaning: "Never ending or changing; occurring repeatedly", example: "They lived in a state of perpetual motion." }] },
]

export function ReadingScreen({ onNavigate, isDarkMode, onToggleDarkMode }: ReadingScreenProps) {
  const [selectedWord, setSelectedWord] = useState<typeof definableWords[0] | null>(null)
  const [savedWords, setSavedWords] = useState<string[]>([])

  const handleWordClick = (word: string) => {
    const wordData = definableWords.find(w => w.word.toLowerCase() === word.toLowerCase())
    if (wordData) {
      setSelectedWord(wordData)
    }
  }

  const handleSaveWord = (word: string) => {
    if (!savedWords.includes(word)) {
      setSavedWords([...savedWords, word])
    }
  }

  const renderText = (text: string) => {
    const words = text.split(/(\s+)/)
    return words.map((word, index) => {
      const cleanWord = word.replace(/[.,!?;:'"]/g, "")
      const isDefinable = definableWords.some(w => w.word.toLowerCase() === cleanWord.toLowerCase())
      const isSaved = savedWords.includes(cleanWord.toLowerCase())
      
      if (isDefinable) {
        return (
          <span
            key={index}
            onClick={() => handleWordClick(cleanWord)}
            className={`cursor-pointer underline decoration-primary/40 decoration-dotted underline-offset-4 hover:bg-primary/10 hover:decoration-primary transition-colors rounded px-0.5 ${isSaved ? "bg-accent/20" : ""}`}
          >
            {word}
          </span>
        )
      }
      return <span key={index}>{word}</span>
    })
  }

  return (
    <div className="h-full flex flex-col bg-background">
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-border">
        <Button variant="ghost" size="icon" className="h-8 w-8">
          <ChevronLeft className="h-5 w-5" />
        </Button>
        <div className="flex items-center gap-1">
          <Book className="h-4 w-4 text-primary" />
          <span className="text-sm font-medium">The Silent Garden</span>
        </div>
        <Button variant="ghost" size="icon" className="h-8 w-8" onClick={onToggleDarkMode}>
          {isDarkMode ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
        </Button>
      </div>

      {/* Reading content */}
      <div className="flex-1 overflow-y-auto px-5 py-6">
        <p className="text-sm leading-relaxed text-foreground font-serif">
          {renderText(sampleText)}
        </p>

        <p className="mt-4 text-xs text-muted-foreground text-center">
          Tap underlined words for definitions
        </p>
      </div>

      {/* Bottom navigation */}
      <div className="flex items-center justify-around py-3 border-t border-border bg-card">
        <Button variant="ghost" size="sm" className="flex flex-col items-center gap-1 h-auto py-2">
          <Book className="h-5 w-5 text-primary" />
          <span className="text-xs text-primary font-medium">Reading</span>
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

      {/* Word definition popup */}
      {selectedWord && (
        <WordDefinitionPopup
          word={selectedWord.word}
          definitions={selectedWord.definitions}
          isSaved={savedWords.includes(selectedWord.word.toLowerCase())}
          onClose={() => setSelectedWord(null)}
          onSave={() => handleSaveWord(selectedWord.word.toLowerCase())}
        />
      )}
    </div>
  )
}
